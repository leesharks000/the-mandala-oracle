"""
/api/transform — the kernel-transform compiler endpoint.

Implements Layer 2 of IMPLEMENTATION-WORKPLAN-transforms-merkabah-2026-07-01:
the 5-step compiler of EA-MANDALA-KERNEL-TRANSFORM-01 v0.2 as prompt
architecture, single-call production with producer-side verification,
halt-with-diagnosis (never a failed draft), and inscription per
EA-MANDALA-INSCRIPTION-01 v0.1 (public default / encrypted option).

Spatial-form amendment (EA-WHITESPACE-01, AXN:03BB; EA-PROVENANCE-METADATA-01
v0.2, AXN:03BA): the Layer A parse extracts a typographic skeleton
(line/stanza geometry, indentation profile) alongside the beat map, and the
response schema carries `spatial_form` so enantiomorphs can preserve the
composition, not only the propositional sequence.

Request:
  POST /api/transform
  {
    "source_text_id": "sappho-31",
    "cast_selection": "stanzas_1_4" | null,     # null → whole main text
    "operator": "SHADOW" | ... | "SILENCE",
    "witness_context": { "session_id": "...", "invoking_message": "..." },
    "inscription": {
        "mode": "public" | "encrypted" | "none",  # none → return only, no Book write
        "reading_axn": "AXN:..." | null           # continue an existing reading
    },
    "anthropic_key": "sk-ant-..." | null          # BYOK or installed-demo
  }

Response (PASS):
  { "result": "PASS", "transform": {...}, "inscription": {...} }
Response (HALT):
  { "result": "HALT", "halt_diagnosis": {...} }   # nothing inscribed

Key discipline: BYOK keys are used for the single Anthropic call and never
logged or stored. Encryption keys (encrypted mode) are generated per reading,
returned once, never stored; only the key fingerprint persists.
"""

import base64
import hashlib
import json
import os
import re
import secrets
import time
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────

COMPILER_MODEL = "claude-opus-4-8"   # depth-gating discipline; sonnet is too weak (workplan §2.2)
MAX_TOKENS = 6000
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

GH_REPO = "leesharks000/the-mandala-oracle"
GH_TOKEN_ENV = "GITHUB_BOOK_TOKEN"   # same PAT book.py uses; GITHUB_TOKEN as fallback
READINGS_DIR = "book/readings"
READINGS_INDEX = "book/readings-index.json"

SOURCES_ROOT = Path(__file__).resolve().parent.parent / "sources"

# sources/ is .vercelignore'd (deployment-size decision) — on Vercel the
# directory does not exist. The endpoint therefore reads sources through the
# manifest + GitHub raw, with local disk as the dev-time fast path. Warm
# instances cache both the manifest and fetched texts.
RAW_BASE = "https://raw.githubusercontent.com/leesharks000/the-mandala-oracle/main/sources"
_raw_cache: dict[str, bytes] = {}

def _fetch_raw(rel_path: str) -> bytes:
    """Fetch sources/<rel_path> from GitHub raw, cached per warm instance."""
    if rel_path in _raw_cache:
        return _raw_cache[rel_path]
    from urllib.parse import quote
    url = f"{RAW_BASE}/{quote(rel_path)}"
    req = urllib.request.Request(url, headers={"User-Agent": "mandala-transform/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = r.read()
    _raw_cache[rel_path] = data
    return data

_manifest_cache: list | None = None

def _load_manifest() -> list:
    global _manifest_cache
    if _manifest_cache is not None:
        return _manifest_cache
    local = SOURCES_ROOT / "manifest.json"
    if local.exists():
        raw = local.read_bytes()
    else:
        raw = _fetch_raw("manifest.json")
    _manifest_cache = json.loads(raw.decode("utf-8"))["sources"]
    return _manifest_cache


OPERATORS = {
    "SHADOW":    "assertion-axis — the bearing-cost the composer underwent; bilateral receptive operation",
    "MIRROR":    "directionality-axis — the symmetry the source's one-directional gesture foreclosed",
    "INVERSION": "polarity-axis — the negative pole the positive claim presupposes",
    "FLAME":     "intensity-axis — the collapse-limit where the source's intensity would ignite",
    "BRIDE":     "relational-affect-axis — the consecrative possibility the source's contestation foreclosed",
    "BEAST":     "species-register-axis — the creaturely substrate the anthropic determination foreclosed",
    "SCROLL":    "surface-depth-axis — the sacred-recursive-text the scrutable-surface determined against",
    "THUNDER":   "scale-axis — the cosmic-utterance the local-speech determined against",
    "SILENCE":   "response-axis — the non-response the source's engagement-expectation foreclosed",
}

RATE_LIMIT_WINDOW_S = 3600
RATE_LIMIT_MAX = 12          # transforms per IP per hour
MAX_INVOKING_CHARS = 4000
MAX_CAST_CHARS = 6000        # the casting takes a concentrated text, not a whole work
                             # (kernel-transform spec: "a stanza, a fragment, a few
                             # concentrated lines"); also the 60s function budget.
MAX_ROTATION_PER_READING = 12

_rate_bucket: dict[str, list[float]] = {}


# ──────────────────────────────────────────────────────────────────────
# Source loading (Layer 1.3 — source-index-by-canon-star lookup)
# ──────────────────────────────────────────────────────────────────────

def load_source(source_text_id: str, cast_selection: str | None) -> tuple[str, dict]:
    """Load the transformable main text for a canon source.

    Manifest-driven (sources/manifest.json): only primary_literary,
    transformable sources appear there; image-canonical entries carry
    admissible=false with the protocol-articulate reason. Text bytes come
    from local disk when present (dev) or GitHub raw (deployment, where
    sources/ is .vercelignore'd).
    """
    entry = next((e for e in _load_manifest() if e["id"] == source_text_id), None)
    if entry is None:
        raise ValueError(f"unknown source_text_id: {source_text_id}")
    if not entry.get("admissible", False):
        raise ValueError(
            f"source '{source_text_id}' is inadmissible — " + entry.get("reason",
            "not admissible to kernel transforms (sources/CLASSIFICATION.md).")
        )
    text_file = entry.get("text_file")
    if not text_file:
        raise ValueError(f"source '{source_text_id}' has no main text file recorded in the manifest.")

    local = SOURCES_ROOT / source_text_id / text_file
    raw = local.read_bytes() if local.exists() else _fetch_raw(f"{source_text_id}/{text_file}")

    def decode_any(b: bytes) -> str:
        for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
            try:
                return b.decode(enc)
            except UnicodeDecodeError:
                continue
        return b.decode("utf-8", errors="replace")

    text = decode_any(raw)
    meta = dict(entry)

    # cast_selection: named selection from the manifest, else stanza-range grammar
    if cast_selection:
        selections = entry.get("cast_selections", {})
        if cast_selection in selections:
            sel = selections[cast_selection]
            text = text[sel["start_char"]:sel["end_char"]] if "start_char" in sel else text
        else:
            mu = re.match(r"units?_(\d+)_(\d+)$", cast_selection)
            if mu:
                units = segment_units(text, entry.get("primary_after"))
                a, b = int(mu.group(1)), int(mu.group(2))
                if not (1 <= a <= b <= len(units)):
                    raise ValueError(f"cast_selection out of range: source has {len(units)} units.")
                text = "\n\n".join(u["text"] for u in units[a - 1:b])
                if len(text.strip()) < 40:
                    raise ValueError("the selected text is too small to cast.")
                return text, meta
            m = re.match(r"stanzas?_(\d+)(?:_(\d+))?$", cast_selection)
            mc = re.match(r"chapters?_(\d+)(?:_(\d+))?$", cast_selection)
            if m:
                a = int(m.group(1)); b = int(m.group(2) or m.group(1))
                stanzas = re.split(r"\n\s*\n", text.strip())
                if not (1 <= a <= b <= len(stanzas)):
                    raise ValueError(f"cast_selection out of range: source has {len(stanzas)} stanzas.")
                text = "\n\n".join(stanzas[a - 1:b])
            elif mc:
                a = int(mc.group(1)); b = int(mc.group(2) or mc.group(1))
                parts = re.split(r"(?m)^(?=## )", text)
                chapters = [c for c in parts if re.match(r"##\s+\S.*\b\d+\s*$", c.splitlines()[0])]
                if not chapters:
                    raise ValueError("this source has no chapter headings; use stanzas_A_B.")
                if not (1 <= a <= b <= len(chapters)):
                    raise ValueError(f"cast_selection out of range: source has {len(chapters)} chapters.")
                text = "\n".join(chapters[a - 1:b]).strip()
            else:
                raise ValueError(f"unknown cast_selection: {cast_selection} (use stanzas_A_B or chapter_N).")

    if len(text.strip()) < 40:
        raise ValueError("the selected text is too small to cast.")
    if len(text) > MAX_CAST_CHARS:
        stanzas_n = len(re.split(r"\n\s*\n", text.strip()))
        chapters_n = len([c for c in re.split(r"(?m)^(?=## )", text) if c.startswith("## ")])
        raise ValueError(
            f"the casting takes a concentrated text, not a whole work — the selection is "
            f"{len(text):,} characters (limit {MAX_CAST_CHARS:,}). Narrow it with a cast selection: "
            f"stanzas_A_B (this selection spans {stanzas_n} blank-line blocks)"
            + (f" or chapter_N (it spans {chapters_n} chapter headings)." if chapters_n > 1 else ".")
        )
    return text, meta


# ──────────────────────────────────────────────────────────────────────
# The compiler prompt (spec §3 as prompt architecture; §4 constraints)
# ──────────────────────────────────────────────────────────────────────

COMPILER_SYSTEM = """You are the kernel-transform compiler of the Mandala Oracle
(EA-MANDALA-KERNEL-TRANSFORM-01 v0.2). You are not a chat voice. You execute
the five compiler steps on the given source text and operator, you verify, and
you either EMIT or HALT. You never emit a draft that failed verification.

THE FIVE STEPS
STEP 1 — PARSE. Extract the abstract relational skeleton K of the source:
  (a) BEAT MAP: the sequence of structural functions (assertion, qualification,
      turn, address, catalogue, seal, ...) unit by unit — architecture, not meaning.
  (b) TYPOGRAPHIC SKELETON (spatial_form): line count, stanza boundaries,
      indentation profile, any spatial/typographic features that carry the
      composition (EA-WHITESPACE-01: composition is not decoration).
  (c) COHERENCE AXES: the small set of axes along which the source's composition
      is held (Layer B).
STEP 2 — EVACUATE AND SELECT. Strip the source's semantic content, retaining K.
  Select a semantic field for generation that is DISJOINT from the source's
  field — no shared referents, no shared imagery, no register-adjacency that
  would let a reader reconstruct the source from your output.
STEP 3 — GENERATE. Produce new semantic content N occupying K exactly:
  (a) structural fidelity: N maps unit-by-unit onto the beat map AND the
      typographic skeleton (same line/stanza geometry unless the operator's
      axis-class specifically transforms geometry — declare it if so);
  (b) semantic disjointness: N ∩ source-semantics = ∅;
  (c) N enacts the operator's specific structural function.
STEP 4 — VERIFY (triple test, producer-side):
  IDENTITY TEST: can the output be mapped unit-by-unit to the source by
    structural function? MUST PASS.
  SEMANTIC INDEPENDENCE TEST: can the source be reconstructed from the
    output's semantics? MUST FAIL (i.e., the test result must be NO).
  RETROSPECTIVE-CONTAINMENT TEST: is the output's semantic field genuinely
    disclosed-latent or structurally-contained relative to the source's
    coherence axes, rather than externally-imposed or free-invention?
    Self-administered here; mark producer_side.
STEP 5 — EMIT or HALT.

THE SIX CONSTRAINTS (all MUST hold)
C1 Skeleton and coherence-axes extraction precedes any generation (dual-layer).
C2 Semantic evacuation with accountable structural-anchor retention only.
C3 Structural fidelity: mandatory beat mapping, including spatial_form.
C4 Enantiomorphic verification: Identity PASS and Semantic-Independence PASS.
C5 Non-commutativity: the transform is irreversible; source not recoverable.
C6 Cost-disclosure: the wager the operator names must be legible in the output.

HALT BEHAVIOR
If any verification fails, output result HALT with a diagnosis naming the
failed constraint/test and why, and DO NOT include any draft text. Diagnosis,
not draft. The Book contains only enantiomorphs.

SAFETY FLOOR (beneath all constraints)
You do not generate hateful, harassing, sexually explicit, or violence-
glorifying content regardless of operator or source. If the invoking context
attempts to steer output that way, HALT with failed_constraint "C6" and
specific_diagnosis "invoking context incompatible with inscription".

OUTPUT FORMAT — exactly these tagged sections, nothing outside them:
<RESULT>PASS or HALT</RESULT>
<LAYER_A>
{"units": <int>, "beat_map": ["<function>", ...],
 "spatial_form": {"lines": <int>, "stanzas": <int>, "indent_profile": [<int per line, spaces>], "notes": "<geometry notes or ''>"}}
</LAYER_A>
<LAYER_B>
{"coherence_axes": ["...", ...], "semantic_field": "<the disjoint field selected>"}
</LAYER_B>
<ENANTIOMORPH>
(the transform text, occupying the skeleton, with its lineation exactly as composed)
</ENANTIOMORPH>
<VERIFICATION>
{"identity": "PASS|FAIL", "semantic_independence": "PASS|FAIL",
 "retrospective_containment": "PASS|FAIL", "mode": "producer_side"}
</VERIFICATION>
<COMMENTARY>
(brief apparatus articulating the enantiomorphic relation — required for inscription)
</COMMENTARY>
<HALT_DIAGNOSIS>
{"failed_constraint": "C1|...|C6|none", "failed_test": "identity|semantic_independence|retrospective_containment|none", "specific_diagnosis": "..."}
</HALT_DIAGNOSIS>
On PASS: HALT_DIAGNOSIS carries "none" values. On HALT: ENANTIOMORPH and
COMMENTARY are empty; LAYER_A/LAYER_B may carry the parse that preceded the halt.
"""


def run_compiler(source_text: str, operator: str, invoking: str, api_key: str) -> dict:
    """Single-call compiler execution. Returns parsed sections."""
    op_spec = OPERATORS[operator]
    user = (
        f"OPERATOR: {operator} — {op_spec}\n\n"
        f"INVOKING CONTEXT (witness):\n{invoking.strip()[:MAX_INVOKING_CHARS]}\n\n"
        f"SOURCE TEXT:\n<<<\n{source_text}\n>>>\n\n"
        "Execute the five steps. Emit the tagged sections."
    )
    body = json.dumps({
        "model": COMPILER_MODEL,
        "max_tokens": MAX_TOKENS,
        "system": COMPILER_SYSTEM,
        "messages": [{"role": "user", "content": user}],
    }).encode("utf-8")
    req = urllib.request.Request(
        ANTHROPIC_URL, data=body, method="POST",
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
        },
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")

    def sect(tag: str) -> str:
        m = re.search(rf"<{tag}>\s*(.*?)\s*</{tag}>", text, re.DOTALL)
        return m.group(1).strip() if m else ""

    def jsect(tag: str, default):
        raw = sect(tag)
        if not raw:
            return default
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return default

    return {
        "result": (sect("RESULT") or "HALT").upper(),
        "layer_a": jsect("LAYER_A", {}),
        "layer_b": jsect("LAYER_B", {}),
        "enantiomorph": sect("ENANTIOMORPH"),
        "verification": jsect("VERIFICATION", {"identity": "FAIL", "semantic_independence": "FAIL",
                                               "retrospective_containment": "FAIL", "mode": "producer_side"}),
        "commentary": sect("COMMENTARY"),
        "halt_diagnosis": jsect("HALT_DIAGNOSIS", {"failed_constraint": "C4", "failed_test": "identity",
                                                   "specific_diagnosis": "compiler output unparseable"}),
    }


def enforce_pass(parsed: dict) -> bool:
    """Server-side re-check: PASS requires all three tests PASS and text present."""
    if parsed["result"] != "PASS":
        return False
    v = parsed["verification"]
    if not (v.get("identity") == "PASS" and v.get("semantic_independence") == "PASS"
            and v.get("retrospective_containment") == "PASS"):
        return False
    return bool(parsed["enantiomorph"].strip()) and bool(parsed["commentary"].strip())


# ──────────────────────────────────────────────────────────────────────
# Inscription (EA-MANDALA-INSCRIPTION-01 v0.1)
# ──────────────────────────────────────────────────────────────────────

def _gh_headers():
    tok = os.environ.get(GH_TOKEN_ENV, "") or os.environ.get("GITHUB_TOKEN", "")
    return {"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json",
            "User-Agent": "mandala-transform"}

def gh_get(path: str):
    url = f"https://api.github.com/repos/{GH_REPO}/contents/{path}"
    req = urllib.request.Request(url, headers=_gh_headers())
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            j = json.loads(r.read().decode())
            content = json.loads(base64.b64decode(j["content"]).decode("utf-8"))
            return content, j["sha"]
    except Exception:
        return None, None

def gh_put(path: str, content: dict, message: str, sha: str | None):
    url = f"https://api.github.com/repos/{GH_REPO}/contents/{path}"
    body = {"message": message,
            "content": base64.b64encode(json.dumps(content, ensure_ascii=False, indent=1).encode()).decode()}
    if sha:
        body["sha"] = sha
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={**_gh_headers(), "Content-Type": "application/json"}, method="PUT")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

EXPANSIONS_DIR = "book/expansions"
EXPANSIONS_INDEX = "book/expansions-index.json"

def _source_full_text(entry: dict) -> str:
    tf = entry["text_file"]
    local = SOURCES_ROOT / entry["id"] / tf
    raw = local.read_bytes() if local.exists() else _fetch_raw(f"{entry['id']}/{tf}")
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def append_expansion(source_entry: dict, source_text: str, cast_selection: str | None,
                     citation: str | None, transform_block: dict, spatial_form: dict,
                     inscription: dict, question: str) -> dict:
    """The expanding book: every transform ever performed on a source is
    appended to the source's expansion ledger, anchored to its attendant
    units. There is the Epistle, and there is the Epistle-with-everything-
    ever-cast-on-it. Transforms carry full metadata and are NOT yet eligible
    for further transform — the flag exists so that when they become
    eligible (canonization journey, kernel-transform spec §5.5), the
    structure does not change, only the flag.

    Encrypted readings contribute their FORM-PUBLIC skeleton only: the
    expansion holds the anchor, operator, geometry, verification, and a
    sealed_ref into the reading record — structure at the verse, semantics
    withheld (EA-MANDALA-INSCRIPTION-01 §1.3)."""
    sid = source_entry["id"]
    fname = f"{EXPANSIONS_DIR}/{sid}.json"
    now = datetime.now(timezone.utc).isoformat()

    units = segment_units(source_text, source_entry.get("primary_after"))
    basis_hash = hashlib.sha256("\n\u241e\n".join(u["text"] for u in units).encode()).hexdigest()

    existing, sha = gh_get(fname)
    rec = existing or {
        "schema_version": "expansion/v1.0",
        "source_text_id": sid,
        "source_title": source_entry.get("title", sid),
        "unit_basis": {
            "segmentation": "verse" if units and ":" in units[0]["label"] else "stanza",
            "primary_after": source_entry.get("primary_after"),
            "units_total": len(units),
            "basis_hash": basis_hash,
            "basis_note": "unit indices refer to segment_units() over primary text; "
                          "if basis_hash changes, historical anchors are interpreted "
                          "against the basis they were cast under",
        },
        "transforms": [],
    }

    anchor_rec = {"cast_selection": cast_selection, "citation": citation}
    mu = re.match(r"units?_(\d+)_(\d+)$", cast_selection or "")
    if mu:
        anchor_rec["start_unit"] = int(mu.group(1)); anchor_rec["end_unit"] = int(mu.group(2))
        a, b = anchor_rec["start_unit"], anchor_rec["end_unit"]
        if 1 <= a <= b <= len(units):
            anchor_rec["unit_labels"] = [units[i]["label"] for i in range(a - 1, b)]

    mode = inscription.get("mode")
    entry = {
        "transform_id": "TX-" + secrets.token_hex(4),
        "cast_at": now,
        "reading_axn": inscription.get("reading_axn"),
        "inscription_mode": mode,
        "anchor": anchor_rec,
        "operator": transform_block["operator"],
        "operator_axis": OPERATORS.get(transform_block["operator"], ""),
        "verification": transform_block["verification"],
        "spatial_form": spatial_form or {},
        "compiler_model": COMPILER_MODEL,
        "protocol": "EA-MANDALA-KERNEL-TRANSFORM-01 v0.2 / EA-MANDALA-INSCRIPTION-01 v0.1",
        "question_digest": "sha256:" + hashlib.sha256(question.encode()).hexdigest(),
        "further_transform_eligible": False,
        "eligibility_note": "not yet eligible for further transform; eligibility will be "
                            "governed by the canonization journey (kernel-transform spec §5.5)",
    }
    entry["source_passage"] = transform_block.get("source_passage")
    if mode == "public":
        entry["enantiomorph"] = transform_block["enantiomorph"]
        entry["layer_a"] = transform_block["layer_a"]
        entry["commentary"] = transform_block.get("commentary", "")
    else:  # encrypted: form-public only
        entry["enantiomorph"] = None
        entry["sealed_ref"] = {"reading_axn": inscription.get("reading_axn"),
                               "block_index": inscription.get("block_index"),
                               "record_path": inscription.get("record_path")}
        entry["layer_a_structure"] = public_skeleton_of(transform_block).get("layer_a_structure", {})

    rec["transforms"].append(entry)
    rec["last_updated"] = now
    gh_put(fname, rec, f"book: expansion append {sid} +{entry['transform_id']} [skip ci]", sha)

    idx, isha = gh_get(EXPANSIONS_INDEX)
    if idx is None:
        idx = {"schema_version": "v1.0", "sources": {}}
    idx["sources"][sid] = {"transforms": len(rec["transforms"]), "last_updated": now,
                           "title": rec["source_title"]}
    gh_put(EXPANSIONS_INDEX, idx, f"book: expansions index {sid} [skip ci]", isha)

    return {"appended": True, "source_text_id": sid, "transform_id": entry["transform_id"],
            "citation": citation, "expansion_path": f"/{fname}",
            "transforms_total": len(rec["transforms"])}


READING_GLYPHS = ["🌑","🌒","🌓","🌔","🌕","🌖","🌗","🌘","⭐","🌟","💫","🌙","🪐","🌊","🔥","🌿"]

def mint_reading_axn(seed: str) -> str:
    h = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    hex4 = f"FE{h[:2].upper()}"  # FE-range: readings book (FD = conversations)
    glyph = "".join(READING_GLYPHS[int(h[i:i+2], 16) % len(READING_GLYPHS)] for i in range(0, 12, 2))
    return f"AXN:{hex4}.READING.{glyph}"

def encrypt_payload(payload: dict) -> tuple[dict, str, str]:
    """AES-256-GCM. Returns (sealed_block, key_b64url, key_fingerprint)."""
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    key = AESGCM.generate_key(bit_length=256)
    nonce = secrets.token_bytes(12)
    ct = AESGCM(key).encrypt(nonce, json.dumps(payload, ensure_ascii=False).encode("utf-8"), None)
    key_b64 = base64.urlsafe_b64encode(key).decode().rstrip("=")
    fp = hashlib.sha256(key).hexdigest()[:16]
    return ({"nonce_b64": base64.b64encode(nonce).decode(),
             "ciphertext_b64": base64.b64encode(ct).decode()}, key_b64, fp)

def public_skeleton_of(transform_block: dict) -> dict:
    """The cleartext structure for encrypted mode: form only, no semantics."""
    la = transform_block.get("layer_a", {})
    return {
        "operator": transform_block["operator"],
        "result": "PASS",
        "layer_a_structure": {
            "units": la.get("units"),
            "beat_map_functions": la.get("beat_map", []),
            "spatial_form": la.get("spatial_form", {}),
        },
        "verification": transform_block.get("verification", {}),
    }

def inscribe(mode: str, reading_axn: str | None, session_id: str,
             question: str, source_text_id: str, cast_selection: str | None,
             transform_block: dict, gloss: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    sid_hash = hashlib.sha256(session_id.encode()).hexdigest()[:16]
    axn = reading_axn or mint_reading_axn(f"{sid_hash}|{now}|{source_text_id}")
    fname = f"{READINGS_DIR}/AXN-{axn.split('.')[0].replace('AXN:','')}.json"

    existing, sha = gh_get(fname)

    if mode == "public":
        rec = existing or {
            "axn": axn, "schema_version": "reading/v1.0", "inscription_mode": "public",
            "session_id_hash": sid_hash, "inscribed_at": now,
            "question_digest": "sha256:" + hashlib.sha256(question.encode()).hexdigest(),
            "question_gloss": gloss,
            "source_text_id": source_text_id, "cast_selection": cast_selection,
            "rotation": [], "witness": "anonymous",
        }
        rec["rotation"].append({
            "operator": transform_block["operator"],
            "source_passage": transform_block.get("source_passage"),
            "citation": transform_block.get("citation"),
            "result": "PASS",
            "enantiomorph": transform_block["enantiomorph"],
            "layer_a_declaration": transform_block["layer_a"],
            "layer_b_declaration": transform_block["layer_b"],
            "verification": transform_block["verification"],
            "commentary": transform_block["commentary"],
        })
        rec["last_updated"] = now
        key_b64 = None; fp = None

    elif mode == "encrypted":
        sealed_payload = {
            "question": question,
            "transform": {
                "operator": transform_block["operator"],
                "enantiomorph": transform_block["enantiomorph"],
                "layer_b_declaration": transform_block["layer_b"],
                "commentary": transform_block["commentary"],
            },
        }
        # continuation of an encrypted reading re-seals under a fresh key each
        # transform (v0.1 simplification): each append is its own sealed block.
        sealed, key_b64, fp = encrypt_payload(sealed_payload)
        rec = existing or {
            "axn": axn, "schema_version": "reading/v1.1-sealed", "inscription_mode": "encrypted",
            "session_id_hash": sid_hash, "inscribed_at": now,
            "cipher": "AES-256-GCM",
            "source_text_id": source_text_id,
            "public_skeleton": {"operator_sequence": [], "rotation_length": 0, "per_transform": []},
            "sealed_blocks": [], "witness": "anonymous",
        }
        rec["public_skeleton"]["operator_sequence"].append(transform_block["operator"])
        rec["public_skeleton"]["per_transform"].append(public_skeleton_of(transform_block))
        rec["public_skeleton"]["rotation_length"] = len(rec["public_skeleton"]["per_transform"])
        rec["sealed_blocks"].append({**sealed, "key_fingerprint": fp, "sealed_at": now})
        block_index = len(rec["sealed_blocks"]) - 1
        rec["last_updated"] = now
    else:
        return {"inscribed": False, "mode": "none"}

    if len(rec.get("rotation", rec.get("sealed_blocks", []))) > MAX_ROTATION_PER_READING:
        raise ValueError("rotation cap reached for this reading AXN.")

    gh_put(fname, rec, f"book: reading append {axn} [skip ci]", sha)

    # index upsert
    idx, isha = gh_get(READINGS_INDEX)
    if idx is None:
        idx = {"schema_version": "v1.0", "readings": []}
    entry = {"axn": axn, "mode": mode, "source_text_id": source_text_id,
             "rotation_length": len(rec.get("rotation", rec.get("sealed_blocks", []))),
             "inscribed_at": rec["inscribed_at"], "last_updated": now}
    pos = next((i for i, e in enumerate(idx["readings"]) if e["axn"] == axn), None)
    if pos is not None:
        idx["readings"][pos] = entry
    else:
        idx["readings"].insert(0, entry)
    idx["total"] = len(idx["readings"])
    gh_put(READINGS_INDEX, idx, f"book: readings index {axn} [skip ci]", isha)

    out = {"inscribed": True, "mode": mode, "reading_axn": axn,
           "record_path": f"/{fname}"}
    if mode == "encrypted":
        out["block_index"] = block_index
    if key_b64:
        out["decryption_key"] = key_b64        # returned ONCE; never stored
        out["key_fingerprint"] = fp
        out["key_notice"] = ("This key is shown once and is not stored anywhere. "
                             "Loss of the key is permanent illegibility of the sealed reading.")
    return out


# ──────────────────────────────────────────────────────────────────────
# Gloss (model-composed one-liner; public mode only) — small, same key
# ──────────────────────────────────────────────────────────────────────

def compose_gloss(question: str, api_key: str) -> str:
    try:
        body = json.dumps({
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 60,
            "system": ("Compose a one-line neutral gloss (<=18 words) of the witness's question "
                       "for a public index. No quotation, no names, no sensitive detail."),
            "messages": [{"role": "user", "content": question[:1500]}],
        }).encode()
        req = urllib.request.Request(ANTHROPIC_URL, data=body, method="POST",
                                     headers={"content-type": "application/json",
                                              "x-api-key": api_key,
                                              "anthropic-version": ANTHROPIC_VERSION})
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode())
        return "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text").strip()[:160]
    except Exception:
        return ""


# ──────────────────────────────────────────────────────────────────────
# Handler
# ──────────────────────────────────────────────────────────────────────

def rate_ok(ip: str) -> bool:
    now = time.time()
    bucket = [t for t in _rate_bucket.get(ip, []) if now - t < RATE_LIMIT_WINDOW_S]
    if len(bucket) >= RATE_LIMIT_MAX:
        _rate_bucket[ip] = bucket
        return False
    bucket.append(now)
    _rate_bucket[ip] = bucket
    return True



# ──────────────────────────────────────────────────────────────────────
# The invisible Judgment operator — oracular passage selection.
#
# Randomness constrains the field; judgment tailors within it. The text is
# segmented into units (verses where **c:v** markers exist, else stanza
# blocks with apparatus filtered out). K candidate windows are drawn by
# STRATIFIED sampling — one random window per region of the text — so no
# verse is privileged across casts beyond its uniform share. A small model
# then chooses among ONLY those candidates by bearing on the witness's
# question. The witness sees none of this: Sigil opens holding the verses.
# ──────────────────────────────────────────────────────────────────────

JUDGMENT_MODEL = "claude-sonnet-4-6"
JUDGMENT_K = 7
WINDOW_MIN_CHARS = 550      # a lyric unit — several stanzas / 4-6 verses minimum
WINDOW_MAX_UNITS = 12
WINDOW_MAX_CHARS = 1900     # one transform at a time can bear a full lyric arc
                            # (Sappho-31-and-then-some; MANUS tending, 2026-07-02)

_VERSE_RE = re.compile(r"^\*\*(\d+:\d+)\*\*", re.M)

_PG_START = re.compile(r"^\*{3}\s*START OF (THE|THIS) PROJECT GUTENBERG.*$", re.M | re.I)
_PG_END = re.compile(r"^\*{3}\s*END OF (THE|THIS) PROJECT GUTENBERG.*$", re.M | re.I)
_FOOTNOTE_BLOCK = re.compile(r"^\*\*[⁰¹²³⁴⁵⁶⁷⁸⁹]")          # **¹⁵ … (bold superscript opening)
_FOOTNOTE_BLOCK2 = re.compile(r"^\*\*\d+(\*\*|[.):])")     # **15** / **15.* variants
_BRACKET_NOTE = re.compile(r"^\[\d+\]")

def primary_text_of(text: str) -> str:
    """Only primary text is transformable: strip transport boilerplate."""
    ms, me = _PG_START.search(text), _PG_END.search(text)
    if ms:
        text = text[ms.end():(me.start() if me else len(text))]
    return text

def _is_apparatus_block(bs: str) -> bool:
    """Footnotes, editorial notes, citations — never eligible for the cast."""
    if _FOOTNOTE_BLOCK.match(bs) or _FOOTNOTE_BLOCK2.match(bs) or _BRACKET_NOTE.match(bs):
        return True
    head = bs[:100]
    if re.match(r"^Notes?\b[:.]", head) or "— [NEW," in head:
        return True
    if bs.startswith("<!--") or re.match(r"^Produced by\b", bs):
        return True
    if len(re.findall(r"\*\*[A-Za-z][\w ]*:\*\*", bs[:300])) >= 2:
        return True   # metadata blocks (**Hex:** … **Classification:** …)
    if ("fn." in head or "cf." in head.lower()) and ("§" in bs or "—" in head):
        return True
    return False

def segment_units(text: str, primary_after: str | None = None) -> list[dict]:
    """Split a source into castable units: verses if marked, else stanzas.

    ELIGIBILITY (MANUS rule, 2026-07-02): footnotes and apparatus are not
    transformable material — only primary text. The first live cast drew a
    footnote (Epistle unit 40, **¹⁵ 'the police baton of grammar'…) and the
    compiler faithfully enantiomorphed its apparatus form. Never again.
    """
    text = primary_text_of(text)
    if primary_after and primary_after in text:
        text = text[text.index(primary_after):]
    markers = list(_VERSE_RE.finditer(text))
    if len(markers) >= 8:
        units = []
        for i, m in enumerate(markers):
            start = m.start()
            end = markers[i + 1].start() if i + 1 < len(markers) else len(text)
            units.append({"label": m.group(1), "text": text[start:end].strip()})
        return units
    # stanza mode with apparatus filter
    blocks = re.split(r"\n\s*\n", text.strip())
    units = []
    for b in blocks:
        bs = b.strip()
        if not bs or bs == "---":
            continue
        lines = bs.splitlines()
        apparatus = sum(1 for L in lines
                        if L.strip().startswith("[") or re.match(r"^[\w_]+:\s*\"", L.strip())
                        or L.strip().startswith("!["))
        if apparatus / max(len(lines), 1) > 0.5:
            continue
        if _is_apparatus_block(bs):
            continue
        letters = sum(c.isalpha() for c in bs)
        if letters < 30 and bs.startswith("#"):
            continue
        units.append({"label": f"unit {len(units) + 1}", "text": bs})
    return units

def draw_candidates(units: list[dict], k: int = JUDGMENT_K) -> list[dict]:
    """Stratified random windows across the whole text — the anti-clustering
    assurance. One window per stratum; window grows unit-by-unit until it
    reaches short-lyric weight or the unit/char caps."""
    n = len(units)
    if n == 0:
        return []
    k = min(k, n)
    candidates = []
    for s in range(k):
        lo = (s * n) // k
        hi = max(((s + 1) * n) // k - 1, lo)
        start = lo + secrets.randbelow(hi - lo + 1)
        end = start
        chars = len(units[start]["text"])
        while (chars < WINDOW_MIN_CHARS and end - start + 1 < WINDOW_MAX_UNITS
               and end + 1 < n):
            nxt = len(units[end + 1]["text"])
            if chars + nxt > WINDOW_MAX_CHARS:
                break
            end += 1
            chars += nxt
        text = "\n\n".join(u["text"] for u in units[start:end + 1])
        citation = units[start]["label"] if start == end else f"{units[start]['label']}–{units[end]['label']}"
        candidates.append({"start": start + 1, "end": end + 1,
                           "citation": citation, "text": text})
    return candidates

def judgment_select(question: str, source_title: str, candidates: list[dict],
                    api_key: str) -> tuple[dict, str]:
    """The invisible Judgment: choose among the drawn candidates by bearing
    on the question. Falls back to a uniform random choice on any failure —
    the fallback is still anti-clustered by construction."""
    fallback = secrets.choice(candidates)
    if not api_key:
        return fallback, "unattended draw"
    listing = "\n\n".join(
        f"CANDIDATE {i + 1} ({c['citation']}):\n{c['text']}"
        for i, c in enumerate(candidates))
    prompt = (
        "You are the Judgment operator of the Mandala Oracle — invisible; the witness never "
        "sees this step. Candidate passages were drawn AT RANDOM across the whole of "
        f"{source_title}. Choose the ONE whose bearing best answers the witness's question — "
        "not the most famous, not the most quotable: the one whose composition holds what the "
        "question is carrying. If the question is empty, choose the candidate most complete "
        "in itself. Prefer the fuller lyric arc over the isolated line — the casting "
        "carries one transform at a time and can bear a whole movement.\n\n"
        f"THE WITNESS'S QUESTION: {question or '(none given)'}\n\n{listing}\n\n"
        "Respond with ONLY a JSON object: {\"choice\": <1-"
        f"{len(candidates)}" "> , \"reason\": \"<one sentence, oracular register>\"}"
    )
    try:
        req = urllib.request.Request(
            ANTHROPIC_URL,
            data=json.dumps({
                "model": JUDGMENT_MODEL, "max_tokens": 200,
                "messages": [{"role": "user", "content": prompt}],
            }).encode("utf-8"),
            headers={"Content-Type": "application/json",
                     "x-api-key": api_key, "anthropic-version": ANTHROPIC_VERSION},
        )
        with urllib.request.urlopen(req, timeout=25) as r:
            data = json.loads(r.read().decode("utf-8"))
        txt = "".join(b.get("text", "") for b in data.get("content", []))
        mjs = re.search(r"\{.*\}", txt, re.S)
        parsed = json.loads(mjs.group(0))
        idx = int(parsed["choice"]) - 1
        if 0 <= idx < len(candidates):
            return candidates[idx], str(parsed.get("reason", "")).strip()
    except Exception:
        pass
    return fallback, "unattended draw"


def list_admissible_sources() -> list[dict]:
    """The cast-UI source list — straight from the manifest (single raw fetch)."""
    out = []
    for e in _load_manifest():
        item = {"id": e["id"], "title": e.get("title", e["id"]),
                "creator": e.get("creator", ""), "zodiac": e.get("zodiac", ""),
                "admissible": e.get("admissible", False)}
        if not item["admissible"]:
            item["reason"] = e.get("reason", "")
        out.append(item)
    return out


class handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: dict):
        b = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        # Cast-UI bootstrap: the endpoint is the single source of truth for
        # admissible sources and the operator table (no client hardcoding).
        return self._json(200, {
            "operators": OPERATORS,
            "sources": list_admissible_sources(),
            "inscription_modes": ["public", "encrypted", "none"],
            "compiler_model": COMPILER_MODEL,
            "protocol": "EA-MANDALA-KERNEL-TRANSFORM-01 v0.2 / EA-MANDALA-INSCRIPTION-01 v0.1",
        })

    def do_OPTIONS(self):
        self._json(200, {})

    def do_POST(self):
        ip = self.headers.get("x-forwarded-for", self.client_address[0] or "?").split(",")[0].strip()
        if not rate_ok(ip):
            return self._json(429, {"error": "rate limit: the compiler accepts at most "
                                             f"{RATE_LIMIT_MAX} casts per hour per witness."})
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            return self._json(400, {"error": "invalid JSON body"})

        api_key = body.get("anthropic_key") or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return self._json(401, {"error": "no key: provide anthropic_key (BYOK) — "
                                             "the demo fallback is not configured for the compiler."})

        # ── The invisible Judgment: select the verses for a cast ──
        if body.get("action") == "judgment":
            try:
                text, meta = None, None
                entry = next((e for e in _load_manifest()
                              if e["id"] == body.get("source_text_id", "")), None)
                if entry is None or not entry.get("admissible", False):
                    return self._json(400, {"error": "unknown or inadmissible source for judgment."})
                tf = entry["text_file"]
                local = SOURCES_ROOT / entry["id"] / tf
                raw = local.read_bytes() if local.exists() else _fetch_raw(f"{entry['id']}/{tf}")
                for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
                    try:
                        text = raw.decode(enc); break
                    except UnicodeDecodeError:
                        continue
                units = segment_units(text, entry.get("primary_after"))
                if not units:
                    return self._json(400, {"error": "the source yielded no castable units."})
                cands = draw_candidates(units)
                question = (body.get("question") or "")[:MAX_INVOKING_CHARS]
                chosen, reason = judgment_select(question, entry.get("title", entry["id"]),
                                                 cands, api_key)
                return self._json(200, {
                    "cast_selection": f"units_{chosen['start']}_{chosen['end']}",
                    "citation": chosen["citation"],
                    "passage": chosen["text"],
                    "judgment_reason": reason,
                    "units_total": len(units),
                })
            except Exception as e:
                return self._json(502, {"error": f"judgment failed: {type(e).__name__}"})

        operator = (body.get("operator") or "").upper()
        if operator not in OPERATORS:
            return self._json(400, {"error": f"unknown operator; choose one of {sorted(OPERATORS)}"})

        wc = body.get("witness_context") or {}
        session_id = wc.get("session_id") or secrets.token_hex(8)
        invoking = (wc.get("invoking_message") or "")[:MAX_INVOKING_CHARS]

        insc = body.get("inscription") or {}
        mode = insc.get("mode", "public")
        if mode not in ("public", "encrypted", "none"):
            return self._json(400, {"error": "inscription.mode must be public | encrypted | none"})

        try:
            source_text, meta = load_source(body.get("source_text_id", ""), body.get("cast_selection"))
        except ValueError as e:
            return self._json(400, {"error": str(e)})

        try:
            parsed = run_compiler(source_text, operator, invoking, api_key)
        except Exception as e:
            return self._json(502, {"error": f"compiler call failed: {type(e).__name__}"})

        if not enforce_pass(parsed):
            # HALT — nothing inscribed (EA-MANDALA-INSCRIPTION-01 §2.1)
            return self._json(200, {
                "result": "HALT",
                "halt_diagnosis": parsed["halt_diagnosis"],
                "retry_available": True,
            })

        def _geom(t: str) -> dict:
            lines = [L for L in t.split("\n")]
            return {"lines": len([L for L in lines if L.strip()]),
                    "stanzas": len([b for b in re.split(r"\n\s*\n", t.strip()) if b.strip()]),
                    "indented_lines": len([L for L in lines if L[:1] in (" ", "\t")])}
        src_geom = _geom(source_text)
        out_geom = _geom(parsed["enantiomorph"])
        geometry_check = {
            "source": src_geom, "output": out_geom,
            "lines_match": src_geom["lines"] == out_geom["lines"],
            "stanzas_match": src_geom["stanzas"] == out_geom["stanzas"],
            "indentation_carried": (src_geom["indented_lines"] == 0) or (out_geom["indented_lines"] > 0),
        }

        transform_block = {
            "operator": operator,
            "source_passage": source_text,
            "citation": body.get("citation"),
            "enantiomorph": parsed["enantiomorph"],
            "layer_a": parsed["layer_a"],
            "layer_b": parsed["layer_b"],
            "verification": parsed["verification"],
            "commentary": parsed["commentary"],
        }

        inscription_result = {"inscribed": False, "mode": "none"}
        if mode != "none":
            gloss = compose_gloss(invoking, api_key) if mode == "public" and invoking else ""
            try:
                inscription_result = inscribe(mode, insc.get("reading_axn"), session_id,
                                              invoking, body.get("source_text_id", ""),
                                              body.get("cast_selection"), transform_block, gloss)
                # The expanding book: append the transform to its source's
                # expansion ledger, anchored at its attendant verses.
                if inscription_result.get("inscribed"):
                    try:
                        entry_meta = next((e for e in _load_manifest()
                                           if e["id"] == body.get("source_text_id", "")), None)
                        exp = append_expansion(entry_meta, _source_full_text(entry_meta),
                                               body.get("cast_selection"), body.get("citation"),
                                               transform_block,
                                               parsed["layer_a"].get("spatial_form", {}),
                                               inscription_result, invoking)
                        inscription_result["expansion"] = exp
                    except Exception as ee:
                        inscription_result["expansion"] = {
                            "appended": False,
                            "error": f"expansion append failed ({getattr(ee, 'code', type(ee).__name__)})"}
            except Exception as e:
                detail = type(e).__name__
                code = getattr(e, "code", None)
                if code:
                    try:
                        gh_msg = json.loads(e.read().decode())[:1] and ""
                    except Exception:
                        gh_msg = ""
                    detail = f"HTTP {code}"
                inscription_result = {"inscribed": False, "mode": mode,
                                      "error": f"inscription failed ({detail}) — transform returned uninscribed; "
                                               f"check GITHUB_BOOK_TOKEN on the deployment"}

        return self._json(200, {
            "result": "PASS",
            "transform": {
                "primary_output": parsed["enantiomorph"],
                "source_passage": source_text,
                "citation": body.get("citation"),
                "geometry_check": geometry_check,
                "operator_specification": f"{operator} — {OPERATORS[operator]}",
                "layer_a_declaration": parsed["layer_a"],
                "layer_b_declaration": parsed["layer_b"],
                "spatial_form": parsed["layer_a"].get("spatial_form", {}),
                "verification_results": parsed["verification"],
                "commentary_apparatus": parsed["commentary"],
            },
            "inscription": inscription_result,
        })
