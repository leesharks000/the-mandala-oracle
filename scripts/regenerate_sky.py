#!/usr/bin/env python3
"""
regenerate_sky.py — Build the navigable-sky data from RAG vectors + registry lineage.

Reads:
    rag/vectors.json       — embeddings, AXN-indexed
    rag/metadata.json      — per-deposit metadata
    alexanarch/data/registry.json — for lineage edges

Writes:
    sky/coords.json    — UMAP-3D positions per AXN, with mass + origin
    sky/edges.json     — lineage edges between AXNs
    sky/planets.json   — fixed positions of the seven planetary bodies (AXN-0237)
    sky/config.json    — UMAP parameters, regen timestamp, source-corpus hash

Discipline:
    - Compact JSON per alexanarch convention
    - Deterministic UMAP (fixed random_state) so re-runs are reproducible
    - Coordinate system: inscription sphere at radius 100, planets at radius 300

Author: leesharks000 (co-drafted with TACHYON)
"""

import json
import sys
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import umap

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
ALEXANARCH = ROOT / "alexanarch"
REGISTRY_PATH = ALEXANARCH / "data" / "registry.json"
RAG_DIR = ROOT / "rag"
SKY_DIR = ROOT / "sky"

# Sky geometry
INSCRIPTION_SPHERE_RADIUS = 100.0  # all inscriptions fit within this radius
PLANET_SPHERE_RADIUS = 300.0       # planets sit at this fixed radius

# UMAP parameters
UMAP_N_NEIGHBORS = 15
UMAP_MIN_DIST = 0.1
UMAP_METRIC = "cosine"     # vectors are normalized; cosine is appropriate
UMAP_RANDOM_STATE = 42      # reproducibility

# Mass calculation: log-scaled by lineage degree (a deposit referenced often is more massive)
MASS_BASE = 1.0
MASS_SCALE = 0.5

# JSON serialization discipline
JSON_KWARGS = {"separators": (",", ":"), "ensure_ascii": False}

# Planetary bodies — AXN-0237 substrate-role assignments
# Classical Chaldean order (Moon, Mercury, Venus, Sun, Mars, Jupiter, Saturn)
# placed at equally-spaced azimuthal positions around the sky equator.
PLANETS = [
    # (name, substrate_role, substrate_vendor, color_hint)
    ("Moon",    "ARCHIVE",  "Gemini",      "#c4c8d0"),
    ("Mercury", "TACHYON",  "Claude",      "#b8a07c"),
    ("Venus",   "TECHNE",   "Kimi",        "#f4d8a0"),
    ("Sun",     "SURFACE",  "Google AIO",  "#ffcc4d"),
    ("Mars",    "PRAXIS",   "DeepSeek",    "#d04848"),
    ("Jupiter", "SOIL",     "Grok",        "#d8a868"),
    ("Saturn",  "LABOR",    "ChatGPT",     "#c8b884"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Lineage extraction
# ─────────────────────────────────────────────────────────────────────────────

def build_hex_to_axn_map(deposits: list) -> dict:
    """Build hex → axn lookup for edge resolution."""
    out = {}
    for d in deposits:
        hex_id = d.get("hex")
        axn = d.get("axn")
        if hex_id and axn:
            out[hex_id.upper()] = axn
    return out


def resolve_target_axn(target_ref: dict | str, hex_to_axn: dict) -> str | None:
    """Resolve a lineage target to its canonical AXN string.

    target_ref may be:
        - a dict with 'hex' field
        - a dict with 'axn' field
        - a dict with 'deposit_number' field (less reliable; fall back if hex unavailable)
        - a string AXN identifier
    """
    if isinstance(target_ref, str):
        # Already an AXN string (or other string identifier)
        if target_ref.startswith("AXN:"):
            return target_ref
        return None

    if not isinstance(target_ref, dict):
        return None

    if axn := target_ref.get("axn"):
        return axn

    if hex_id := target_ref.get("hex"):
        if axn := hex_to_axn.get(hex_id.upper()):
            return axn

    return None


def extract_lineage_edges(deposits: list, hex_to_axn: dict) -> list:
    """Extract lineage edges from registry metadata.

    Edge kinds:
        chain_predecessor — version-chain predecessor
        companion         — companion deposit (same generative cycle, same series)
        related           — broader relation
        bundle            — bundled together
        predecessor       — explicit predecessor (separate from chain)
        superseded_by     — this entry was superseded by target
    """
    edges = []

    for d in deposits:
        from_axn = d.get("axn")
        if not from_axn:
            continue

        # chain_predecessors: list of predecessor versions
        for pred in d.get("chain_predecessors", []) or []:
            if to_axn := resolve_target_axn(pred, hex_to_axn):
                edges.append({"from": from_axn, "to": to_axn, "kind": "chain_predecessor"})

        # companion_deposits
        for comp in d.get("companion_deposits", []) or []:
            if to_axn := resolve_target_axn(comp, hex_to_axn):
                edges.append({"from": from_axn, "to": to_axn, "kind": "companion"})

        # related_deposits
        for rel in d.get("related_deposits", []) or []:
            if to_axn := resolve_target_axn(rel, hex_to_axn):
                edges.append({"from": from_axn, "to": to_axn, "kind": "related"})

        # bundle_companions
        for bundle in d.get("bundle_companions", []) or []:
            if to_axn := resolve_target_axn(bundle, hex_to_axn):
                edges.append({"from": from_axn, "to": to_axn, "kind": "bundle"})

        # predecessor_deposit (single)
        if pred := d.get("predecessor_deposit"):
            if to_axn := resolve_target_axn(pred, hex_to_axn):
                edges.append({"from": from_axn, "to": to_axn, "kind": "predecessor"})
        elif pred_axn := d.get("predecessor_axn"):
            edges.append({"from": from_axn, "to": pred_axn, "kind": "predecessor"})

        # superseded_by
        if sup_axn := d.get("superseded_by_axn"):
            edges.append({"from": from_axn, "to": sup_axn, "kind": "superseded_by"})

    # Dedup (some edges may appear multiply, e.g. same companion listed in two fields)
    seen = set()
    deduped = []
    for e in edges:
        key = (e["from"], e["to"], e["kind"])
        if key not in seen:
            seen.add(key)
            deduped.append(e)
    return deduped


# ─────────────────────────────────────────────────────────────────────────────
# UMAP projection
# ─────────────────────────────────────────────────────────────────────────────

def project_to_3d(vectors: np.ndarray) -> np.ndarray:
    """Run UMAP to project vectors to 3D. Returns positions normalized to fit
    within the inscription sphere radius."""
    reducer = umap.UMAP(
        n_components=3,
        n_neighbors=UMAP_N_NEIGHBORS,
        min_dist=UMAP_MIN_DIST,
        metric=UMAP_METRIC,
        random_state=UMAP_RANDOM_STATE,
    )
    raw_3d = reducer.fit_transform(vectors)

    # Center and scale to fit within INSCRIPTION_SPHERE_RADIUS
    centroid = raw_3d.mean(axis=0)
    centered = raw_3d - centroid
    max_dist = np.linalg.norm(centered, axis=1).max()
    scale = (INSCRIPTION_SPHERE_RADIUS * 0.9) / max_dist  # 0.9 leaves margin
    return centered * scale


# ─────────────────────────────────────────────────────────────────────────────
# Planet positions
# ─────────────────────────────────────────────────────────────────────────────

def planet_positions() -> list:
    """Place planets at equally-spaced azimuthal positions on the sky-sphere
    equator (y = 0). Classical Chaldean order around the circle."""
    out = []
    n = len(PLANETS)
    for i, (name, role, vendor, color) in enumerate(PLANETS):
        angle = 2 * math.pi * i / n
        x = PLANET_SPHERE_RADIUS * math.cos(angle)
        z = PLANET_SPHERE_RADIUS * math.sin(angle)
        y = 0.0
        out.append({
            "name": name,
            "substrate_role": role,
            "substrate_vendor": vendor,
            "color_hint": color,
            "position": [x, y, z],
            "interactive": name == "Sun",  # only Sun is interactive (Gate G capture)
        })
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Mass calculation
# ─────────────────────────────────────────────────────────────────────────────

def compute_mass(axn: str, edges: list) -> float:
    """Log-scaled mass: a deposit referenced by many others is more massive.

    Mass = MASS_BASE + MASS_SCALE * log(1 + in_degree)
    """
    in_degree = sum(1 for e in edges if e["to"] == axn)
    return MASS_BASE + MASS_SCALE * math.log1p(in_degree)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    vectors_path = RAG_DIR / "vectors.json"
    metadata_path = RAG_DIR / "metadata.json"

    if not vectors_path.exists() or not metadata_path.exists():
        print(f"ERROR: RAG index not found in {RAG_DIR}", file=sys.stderr)
        print("       Run scripts/regenerate_rag.py first.", file=sys.stderr)
        return 1

    if not REGISTRY_PATH.exists():
        print(f"ERROR: Registry not found at {REGISTRY_PATH}", file=sys.stderr)
        return 1

    print("Loading RAG index...")
    with vectors_path.open(encoding="utf-8") as f:
        vectors_data = json.load(f)
    with metadata_path.open(encoding="utf-8") as f:
        metadata = json.load(f)

    print(f"  {vectors_data['count']} vectors × {vectors_data['dim']} dims")

    vectors = np.array(vectors_data["vectors"], dtype=np.float32)
    axn_order = sorted(vectors_data["axn_to_index"], key=lambda a: vectors_data["axn_to_index"][a])

    # ── Lineage edges ───────────────────────────────────────────────────────
    print("\nLoading registry for lineage...")
    with REGISTRY_PATH.open(encoding="utf-8") as f:
        registry = json.load(f)

    deposits = registry.get("deposits", [])
    hex_to_axn = build_hex_to_axn_map(deposits)
    print(f"  {len(hex_to_axn)} hex→axn mappings")

    edges = extract_lineage_edges(deposits, hex_to_axn)
    print(f"  {len(edges)} lineage edges extracted")
    edge_kinds = {}
    for e in edges:
        edge_kinds[e["kind"]] = edge_kinds.get(e["kind"], 0) + 1
    for k, v in sorted(edge_kinds.items()):
        print(f"    {k}: {v}")

    # Keep only edges where both endpoints are in our embedded set
    embedded_axns = set(axn_order)
    edges = [e for e in edges if e["from"] in embedded_axns and e["to"] in embedded_axns]
    print(f"  {len(edges)} edges with both endpoints embedded")

    # ── UMAP projection ─────────────────────────────────────────────────────
    print(f"\nProjecting {vectors.shape[0]} vectors to 3D via UMAP...")
    positions_3d = project_to_3d(vectors)
    print(f"  position range: x[{positions_3d[:,0].min():.1f}, {positions_3d[:,0].max():.1f}], "
          f"y[{positions_3d[:,1].min():.1f}, {positions_3d[:,1].max():.1f}], "
          f"z[{positions_3d[:,2].min():.1f}, {positions_3d[:,2].max():.1f}]")

    # ── Build coords entries ────────────────────────────────────────────────
    # Build axn → metadata lookup for fast access
    meta_by_axn = {m["axn"]: m for m in metadata}

    coords = []
    for i, axn in enumerate(axn_order):
        meta = meta_by_axn.get(axn, {})
        coords.append({
            "axn": axn,
            "hex": meta.get("hex"),
            "title": meta.get("title"),
            "family": meta.get("family"),
            "origin": meta.get("origin", "archive"),
            "date": meta.get("date"),
            "position": [float(positions_3d[i, 0]), float(positions_3d[i, 1]), float(positions_3d[i, 2])],
            "mass": compute_mass(axn, edges),
        })

    # ── Planet positions ────────────────────────────────────────────────────
    planets = planet_positions()
    print(f"\nPlaced {len(planets)} planets at radius {PLANET_SPHERE_RADIUS}")

    # ── Write outputs ───────────────────────────────────────────────────────
    SKY_DIR.mkdir(parents=True, exist_ok=True)

    coords_path = SKY_DIR / "coords.json"
    print(f"\nWriting {coords_path} ...")
    with coords_path.open("w", encoding="utf-8") as f:
        json.dump(coords, f, **JSON_KWARGS)
    print(f"  size: {coords_path.stat().st_size / 1024:.1f} KB")

    edges_path = SKY_DIR / "edges.json"
    print(f"Writing {edges_path} ...")
    with edges_path.open("w", encoding="utf-8") as f:
        json.dump(edges, f, **JSON_KWARGS)
    print(f"  size: {edges_path.stat().st_size / 1024:.1f} KB")

    planets_path = SKY_DIR / "planets.json"
    print(f"Writing {planets_path} ...")
    with planets_path.open("w", encoding="utf-8") as f:
        json.dump(planets, f, **JSON_KWARGS)
    print(f"  size: {planets_path.stat().st_size} B")

    sky_config = {
        "umap": {
            "n_components": 3,
            "n_neighbors": UMAP_N_NEIGHBORS,
            "min_dist": UMAP_MIN_DIST,
            "metric": UMAP_METRIC,
            "random_state": UMAP_RANDOM_STATE,
        },
        "geometry": {
            "inscription_sphere_radius": INSCRIPTION_SPHERE_RADIUS,
            "planet_sphere_radius": PLANET_SPHERE_RADIUS,
        },
        "counts": {
            "inscriptions": len(coords),
            "edges": len(edges),
            "edges_by_kind": edge_kinds,
            "planets": len(planets),
        },
        "regenerated_at": datetime.now(timezone.utc).isoformat(),
    }
    config_path = SKY_DIR / "config.json"
    print(f"Writing {config_path} ...")
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(sky_config, f, **JSON_KWARGS)
    print(f"  size: {config_path.stat().st_size} B")

    print("\nDone.")
    print(f"  inscriptions: {len(coords)}")
    print(f"  edges:        {len(edges)}")
    print(f"  planets:      {len(planets)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
