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
GH_TOKEN_ENV = "GITHUB_TOKEN"
READINGS_DIR = "book/readings"
READINGS_INDEX = "book/readings-index.json"

SOURCES_ROOT = Path(__file__).resolve().parent.parent / "sources"

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
MAX_ROTATION_PER_READING = 12

_rate_bucket: dict[str, list[float]] = {}


# ──────────────────────────────────────────────────────────────────────
# Source loading (Layer 1.3 — source-index-by-canon-star lookup)
# ──────────────────────────────────────────────────────────────────────

def load_source(source_text_id: str, cast_selection: str | None) -> tuple[str, dict]:
    """Load the transformable main text for a canon source.

    Enforces the classification rule (sources/CLASSIFICATION.md): only
    `primary_literary` sources with `transformable: true` are admissible.
    Returns (text, metadata). Raises ValueError with a witness-legible
    message otherwise.
    """
    src_dir = SOURCES_ROOT / source_text_id
    meta_path = src_dir / "metadata.json"
    if not meta_path.exists():
        raise ValueError(f"unknown source_text_id: {source_text_id}")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    classification = meta.get("transform_classification", "archival_apparatus")
    if classification != "primary_literary" or not meta.get("transformable", classification == "primary_literary"):
        raise ValueError(
            f"source '{source_text_id}' is classified {classification} — "
            "not admissible to kernel transforms (EA-STARMAP-01 §4.6 as extended)."
        )

    # main text file: prefer main.*, then original.*, then declared, then largest text-like file
    candidates = ["main.txt", "main.grc", "main.la", "main.en",
                  "original.txt", "original.grc", "original.la", "original.en",
                  "original.zh", "original.ar"]
    declared = meta.get("main_text_file")
    if declared:
        candidates.insert(0, declared)

    def read_text_any(p: Path) -> str:
        raw = p.read_bytes()
        for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue
        return raw.decode("utf-8", errors="replace")

    text = None
    for c in candidates:
        p = src_dir / c
        if p.exists():
            text = read_text_any(p)
            break
    if text is None:
        # any text-like file at top level or one directory down (e.g. sappho-fragments/sappho-31/)
        pool = [p for pat in ("*.txt", "*.en", "*.grc", "*.la", "*.zh", "*.ar", "*.md")
                for p in list(src_dir.glob(pat)) + list(src_dir.glob(f"*/{pat}"))
                if p.name not in ("metadata.json", "CLASSIFICATION.md", "README.md")
                and "apparatus" not in p.name and "essay" not in p.name and "key-phrases" not in p.name]
        pool.sort(key=lambda p: p.stat().st_size, reverse=True)
        if pool:
            text = read_text_any(pool[0])
    if text is None:
        if meta.get("canonical_artifact_modality") == "image" or (src_dir / f"{source_text_id.split('-',1)[-1]}.jpg").exists() or list(src_dir.glob("*.jpg")) + list(src_dir.glob("*.png")):
            raise ValueError(
                f"source '{source_text_id}' is image-canonical (calligrammatic): its composition "
                "is not machine-text and is compiler-inadmissible until the spatial_form pipeline "
                "can carry it (EA-PROVENANCE-METADATA-01 v0.2: compositionally_reduced; "
                "compiler_accessible: false)."
            )
        raise ValueError(f"source '{source_text_id}' has no main text file on disk.")

    # cast_selection: named selection from metadata, else a simple stanza-range grammar
    if cast_selection:
        selections = meta.get("cast_selections", {})
        if cast_selection in selections:
            sel = selections[cast_selection]
            text = text[sel["start_char"]:sel["end_char"]] if "start_char" in sel else text
        else:
            m = re.match(r"stanzas?_(\d+)(?:_(\d+))?$", cast_selection)
            if m:
                a = int(m.group(1)); b = int(m.group(2) or m.group(1))
                stanzas = re.split(r"\n\s*\n", text.strip())
                text = "\n\n".join(stanzas[a - 1 : b])
    if len(text.strip()) < 40:
        raise ValueError("cast selection resolved to too little text to transform.")
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
    tok = os.environ.get(GH_TOKEN_ENV, "")
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

        transform_block = {
            "operator": operator,
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
            except Exception as e:
                inscription_result = {"inscribed": False, "mode": mode,
                                      "error": f"inscription failed: {type(e).__name__} — transform returned uninscribed"}

        return self._json(200, {
            "result": "PASS",
            "transform": {
                "primary_output": parsed["enantiomorph"],
                "operator_specification": f"{operator} — {OPERATORS[operator]}",
                "layer_a_declaration": parsed["layer_a"],
                "layer_b_declaration": parsed["layer_b"],
                "spatial_form": parsed["layer_a"].get("spatial_form", {}),
                "verification_results": parsed["verification"],
                "commentary_apparatus": parsed["commentary"],
            },
            "inscription": inscription_result,
        })
