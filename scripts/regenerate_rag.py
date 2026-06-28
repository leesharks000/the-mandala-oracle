#!/usr/bin/env python3
"""
regenerate_rag.py — Build the RAG index over alexanarch deposits.

Reads alexanarch/data/registry.json, locates each deposit's markdown file,
strips SPXI provenance blocks, constructs embedding inputs, and embeds via
sentence-transformers/all-MiniLM-L6-v2.

Writes:
    rag/vectors.json   — { "axn_to_index": {...}, "vectors": [[...], ...] }
    rag/metadata.json  — array of per-deposit metadata with origin tagging
    rag/config.json    — embedding model, chunking strategy, regen timestamp

Discipline:
    - Compact JSON per alexanarch convention (indent=None, separators=(',',':'), ensure_ascii=False)
    - Deterministic ordering (sorted by AXN hex) so output is reproducible
    - Idempotent (same input → same output modulo timestamp)
    - Origin-tagged for forward compatibility with the Book sub-area

Author: leesharks000 (co-drafted with TACHYON)
"""

import json
import re
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
ALEXANARCH = ROOT / "alexanarch"
REGISTRY_PATH = ALEXANARCH / "data" / "registry.json"
DEPOSITS_DIR = ALEXANARCH / "data" / "deposits"
RAG_DIR = ROOT / "rag"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNKING_STRATEGY = "deposit-level-v1"
EMBEDDING_INPUT_MAX_CHARS = 3000  # title + description + keywords + opening body

SPXI_BLOCK_RE = re.compile(
    r"<!--\s*SPXI PROVENANCE BLOCK.*?END SPXI PROVENANCE BLOCK\s*-->",
    re.DOTALL,
)

# JSON serialization discipline — matches alexanarch convention
JSON_KWARGS = {"separators": (",", ":"), "ensure_ascii": False}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def strip_provenance(text: str) -> str:
    """Remove SPXI provenance HTML-comment block(s); return body content."""
    return SPXI_BLOCK_RE.sub("", text).strip()


def locate_deposit_file(deposit: dict) -> Path | None:
    """Find the markdown file for a deposit. Prefer full_text_path, fall back to AXN-{hex}.md."""
    full_text_path = deposit.get("full_text_path")
    if full_text_path:
        # full_text_path may be like "/data/EA-FOO.md" — strip leading slash, resolve from alexanarch root
        candidate = ALEXANARCH / full_text_path.lstrip("/")
        if candidate.exists():
            return candidate

    # Fallback: AXN-{HEX}.md in data/deposits/
    hex_id = deposit.get("hex", "").upper()
    if hex_id:
        candidate = DEPOSITS_DIR / f"AXN-{hex_id}.md"
        if candidate.exists():
            return candidate

    return None


def build_embedding_input(deposit: dict, body: str) -> str:
    """Construct the embedding input for a deposit.

    Strategy (v1, deposit-level):
        title + description + keywords + opening body (capped at EMBEDDING_INPUT_MAX_CHARS)

    This represents what the deposit IS — its identity, its claims, its keywords —
    rather than its full text. Full text remains accessible via metadata.full_text_path.
    """
    parts = []
    if title := deposit.get("title"):
        parts.append(f"Title: {title}")
    if description := deposit.get("description"):
        parts.append(f"Description: {description}")
    if keywords := deposit.get("keywords"):
        if isinstance(keywords, list):
            parts.append(f"Keywords: {', '.join(keywords)}")
    if family := deposit.get("family"):
        parts.append(f"Family: {family}")
    if body:
        # Cap the body excerpt to leave room within EMBEDDING_INPUT_MAX_CHARS
        header = "\n".join(parts) + "\n\nContent: "
        budget = EMBEDDING_INPUT_MAX_CHARS - len(header)
        if budget > 200:
            parts.append("\nContent: " + body[:budget])

    return "\n".join(parts).strip()


def build_metadata_entry(deposit: dict, has_body: bool, deposit_number: int) -> dict:
    """Build the per-deposit metadata entry stored in metadata.json."""
    return {
        "axn": deposit.get("axn"),
        "hex": deposit.get("hex"),
        "family": deposit.get("family"),
        "title": deposit.get("title"),
        "creator": deposit.get("creator"),
        "date": deposit.get("date"),
        "description": deposit.get("description"),
        "keywords": deposit.get("keywords", []),
        "license": deposit.get("license"),
        "hash": deposit.get("hash"),
        "version": deposit.get("version"),
        "full_text_path": deposit.get("full_text_path"),
        "issue_url": deposit.get("issue_url"),
        "minted_at": deposit.get("minted_at"),
        "status": deposit.get("status"),
        # Deposit number in the alexanarch registry (1-based index). Used by the
        # Mandala Oracle client to build deep links to the record page at
        # alexanarch.org/s/records/{deposit_number}/. Lets witnesses click
        # through to the underlying scholarship.
        "deposit_number": deposit_number,
        # Origin discipline (M-2): every entry is tagged for forward compatibility
        # with the Book sub-area. v1: all archive. v2+: Mandala-originating mints get "book".
        "origin": "archive",
        # Whether we have actual body content for this deposit (or only registry metadata)
        "has_body_content": has_body,
    }


def corpus_hash(registry: dict) -> str:
    """Hash the registry's deposits array — invalidates cache when corpus changes."""
    deposits_repr = json.dumps(
        registry.get("deposits", []),
        sort_keys=True,
        **JSON_KWARGS,
    )
    return hashlib.sha256(deposits_repr.encode("utf-8")).hexdigest()[:16]


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    if not REGISTRY_PATH.exists():
        print(f"ERROR: Registry not found at {REGISTRY_PATH}", file=sys.stderr)
        print("       Has the alexanarch submodule been initialized?", file=sys.stderr)
        return 1

    print(f"Reading registry: {REGISTRY_PATH}")
    with REGISTRY_PATH.open(encoding="utf-8") as f:
        registry = json.load(f)

    deposits = registry.get("deposits", [])
    if not deposits:
        print("ERROR: No deposits found in registry.", file=sys.stderr)
        return 1

    print(f"Registry: {len(deposits)} deposit entries")
    print(f"Total deposits declared: {registry.get('total_deposits', 'unknown')}")

    # Sort deterministically by hex for reproducible output
    deposits = sorted(deposits, key=lambda d: d.get("hex", "ZZZZ"))

    # ── Build embedding inputs ──────────────────────────────────────────────
    embedding_inputs = []
    metadata_entries = []
    missing_bodies = 0

    for idx, deposit in enumerate(deposits):
        file_path = locate_deposit_file(deposit)
        body = ""
        has_body = False

        if file_path:
            try:
                raw = file_path.read_text(encoding="utf-8")
                body = strip_provenance(raw)
                has_body = bool(body.strip())
            except (OSError, UnicodeDecodeError) as e:
                print(f"WARN: Could not read {file_path}: {e}", file=sys.stderr)

        if not has_body:
            missing_bodies += 1

        embedding_input = build_embedding_input(deposit, body)
        embedding_inputs.append(embedding_input)
        # deposit_number is 1-based; this matches alexanarch's record-page URL pattern
        # /s/records/{deposit_number}/
        metadata_entries.append(build_metadata_entry(deposit, has_body, idx + 1))

    if missing_bodies:
        print(f"NOTE: {missing_bodies} deposits had no resolvable body file; "
              f"embedded from registry metadata only.")

    # ── Embed ───────────────────────────────────────────────────────────────
    print(f"\nLoading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print(f"Embedding {len(embedding_inputs)} deposits...")
    vectors = model.encode(
        embedding_inputs,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,  # cosine similarity becomes dot product
        convert_to_numpy=True,
    )
    print(f"Embeddings shape: {vectors.shape}")

    # ── Write outputs ───────────────────────────────────────────────────────
    RAG_DIR.mkdir(parents=True, exist_ok=True)

    # vectors.json: AXN-indexed lookup + flat vectors array
    axn_to_index = {entry["axn"]: i for i, entry in enumerate(metadata_entries)}
    vectors_data = {
        "axn_to_index": axn_to_index,
        "vectors": vectors.tolist(),  # list of list-of-floats
        "dim": int(vectors.shape[1]),
        "count": int(vectors.shape[0]),
    }

    vectors_path = RAG_DIR / "vectors.json"
    print(f"\nWriting {vectors_path} ...")
    with vectors_path.open("w", encoding="utf-8") as f:
        json.dump(vectors_data, f, **JSON_KWARGS)
    print(f"  size: {vectors_path.stat().st_size / 1024:.1f} KB")

    metadata_path = RAG_DIR / "metadata.json"
    print(f"Writing {metadata_path} ...")
    with metadata_path.open("w", encoding="utf-8") as f:
        json.dump(metadata_entries, f, **JSON_KWARGS)
    print(f"  size: {metadata_path.stat().st_size / 1024:.1f} KB")

    config = {
        "embedding_model": EMBEDDING_MODEL,
        "embedding_dim": int(vectors.shape[1]),
        "chunking_strategy": CHUNKING_STRATEGY,
        "embedding_input_max_chars": EMBEDDING_INPUT_MAX_CHARS,
        "deposit_count": len(metadata_entries),
        "deposits_with_body": len(metadata_entries) - missing_bodies,
        "deposits_metadata_only": missing_bodies,
        "corpus_hash": corpus_hash(registry),
        "registry_version": registry.get("version"),
        "regenerated_at": datetime.now(timezone.utc).isoformat(),
        "normalize_embeddings": True,
    }

    config_path = RAG_DIR / "config.json"
    print(f"Writing {config_path} ...")
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(config, f, **JSON_KWARGS)
    print(f"  size: {config_path.stat().st_size} B")

    print("\nDone.")
    print(f"  vectors:  {vectors.shape[0]} × {vectors.shape[1]}")
    print(f"  body:     {len(metadata_entries) - missing_bodies}/{len(metadata_entries)}")
    print(f"  hash:     {config['corpus_hash']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
