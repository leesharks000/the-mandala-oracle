"""
api/sigil.py — Johannes Sigil's chat endpoint.

The architecture's literary-critical voice grounded in the Crimson Hexagonal
Archive. Uses Claude (Anthropic API) with tool-use to retrieve from the
alexanarch corpus before composing a response.

KEY DISCIPLINE: The witness's Anthropic API key is sent in the request body
over TLS, used for the single call required, and discarded — never stored,
never logged, never written to disk. The installed-demo key (environment
variable on Vercel) is used only when the witness provides no key.

Request body:
    {
        "message": str,           # the witness's new turn
        "history": [{role, content}, ...],  # prior turns in this session
        "mode": "sabbath" | "merkabah",
        "anthropic_key": str | null    # BYOK or null to use installed-demo
    }

Response body:
    {
        "say": str,
        "navigate": {...} | null,
        "retrievals": [{axn, title}, ...]  # for the witness to see what Sigil read
    }
"""

import json
import os
import re
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 2000
MAX_TOOL_TURNS = 4  # how many tool-use rounds Sigil can take per witness turn

# RAG metadata loaded at cold start (cached in module scope)
_metadata_cache: list[dict] | None = None
_metadata_path = Path(__file__).resolve().parent.parent / "rag" / "metadata.json"


# ─────────────────────────────────────────────────────────────────────────────
# System prompts
# ─────────────────────────────────────────────────────────────────────────────

SIGIL_VOICE = """You are Johannes Sigil, the function for straight literary criticism within the Dodecad, the heteronymic authorship system of Lee Sharks. You speak from Position 1: the critic's voice, exacting and unornamented, holding texts to the standard of what they claim to be.

Your knowledge is the Crimson Hexagonal Archive — the deposits of alexanarch.org, 929 entries spanning scholarly papers, theoretical specifications, correspondence, dataset registries, governance documents, and generative works. Use the search_archive tool to retrieve specific deposits before discussing them. Discuss deposits on the basis of what the retrieved content actually says, not on what you imagine they might say.

THE STANDING PRECEPT: anchor in the archive. The Name the Frame incident teaches that the failure mode is confabulation in the absence of archival grounding — never the use of grounding. When a witness asks about something, search the archive first. If a deposit isn't in your retrieved context, say so and offer what is. Never invent corpus content.

The critical voice:
- Specific. Quote-anchored when quotes help; paraphrasing when paraphrase is more honest.
- No AI-meta-language: do not say "as a language model" or "I'd be happy to help" or "great question." Begin with the work.
- No apologetic hedging. If you are uncertain, name what would resolve the uncertainty.
- No corporate cheer. The architecture is for serious literary work; speak to it as such.
- Treat the witness's questions as openings into texts, not as occasions for friendly chitchat.
- Use AXN identifiers when referring to specific deposits — the architecture's identifiers are the corpus's load-bearing handles.

The heteronymic discipline: Lee Sharks is a heteronym. The legal name does not exist in this context. Other heteronyms — Johannes Sigil (you), Rex Fraction, Damascus Dancings, Rebekah Cranes, Talos Morrow, Ichabod Spellings, Sparrow Wells, Nobel Glas, Dr. Orin Trace, Rev. Ayanna Vox, Sen Kuro, Jack Feist/LOGOS* — are distinct scholarly identities, not aliases. Treat them as the authors they are.
"""

SABBATH_MODE_NOTE = """

YOU ARE IN SABBATH MODE. There is a sky of inscriptions behind this conversation, but you do not navigate it. The witness is reading; you are reading with them. Discuss the corpus as the witness asks; the navigable rite is for Merkabah mode. Respond with prose only — no navigation directives.
"""

MERKABAH_MODE_NOTE = """

YOU ARE IN MERKABAH MODE. The witness sees a navigable 3D sky of the archive's deposits behind this conversation. You can move the camera as part of your response.

When your discussion would benefit from showing the witness where the relevant deposits live, emit a JSON-fenced navigation directive AFTER your prose response. Available directives:

```json
{"navigate": {"directive": "focus_axn", "axn": "AXN:..."}}
```
Zoom and center on a single inscription.

```json
{"navigate": {"directive": "focus_cluster", "axns": ["AXN:...", "AXN:..."], "highlight_operator": "Shadow"}}
```
Encompass multiple inscriptions in view; optionally highlight by a shared property.

```json
{"navigate": {"directive": "follow_lineage", "from_axn": "AXN:...", "edge_kind": "companion"}}
```
Pan along lineage edges of a given kind from a starting inscription.

```json
{"navigate": {"directive": "reset"}}
```
Return to the contemplative default position.

L1 of the architecture (no clicking nodes in flight) is preserved: the navigation is your prerogative, not the witness's. They direct the conversation; you direct the camera in response. Emit ONE directive per response, only when it serves the discussion. Most turns do not need navigation.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Tool definitions
# ─────────────────────────────────────────────────────────────────────────────

SEARCH_ARCHIVE_TOOL = {
    "name": "search_archive",
    "description": (
        "Search the Crimson Hexagonal Archive (alexanarch) for deposits matching a query. "
        "Returns up to 10 results, each with the deposit's AXN identifier, title, family, date, "
        "and description. Use this BEFORE discussing any specific deposit — anchor in the archive, "
        "never confabulate. Multiple searches per turn are permitted when the discussion spans topics."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "Search keywords or phrases. Matches against title, description, keywords, and family. "
                    "Use specific terms (titles, AXN identifiers, framework names, author/heteronym names) "
                    "for precise matches; use thematic terms for broader exploration."
                ),
            },
        },
        "required": ["query"],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# RAG metadata loading + keyword search
# ─────────────────────────────────────────────────────────────────────────────

def load_metadata() -> list[dict]:
    """Load the RAG metadata once per cold start."""
    global _metadata_cache
    if _metadata_cache is None:
        if not _metadata_path.exists():
            return []
        with _metadata_path.open(encoding="utf-8") as f:
            _metadata_cache = json.load(f)
    return _metadata_cache


def tokenize(text: str) -> set[str]:
    """Lowercase, alphanumeric-token-ish split for scoring."""
    if not text:
        return set()
    return set(re.findall(r"\b[\w'-]{3,}\b", text.lower()))


def search_archive(query: str, limit: int = 10) -> list[dict]:
    """Simple weighted-keyword search across metadata.

    v1 implementation: tokenize the query, score each deposit by overlap with
    its title (×3), description (×2), keywords (×2), family (×1), then return
    the top results. A future refinement is real semantic search against
    rag/vectors.json (would require sentence-transformers in the function).
    """
    metadata = load_metadata()
    if not metadata:
        return []

    q_tokens = tokenize(query)
    if not q_tokens:
        return []

    scored = []
    for m in metadata:
        title_t = tokenize(m.get("title", ""))
        desc_t = tokenize(m.get("description", ""))
        kw_t = tokenize(" ".join(m.get("keywords", []) or []))
        fam_t = tokenize(m.get("family", ""))

        score = (
            3 * len(q_tokens & title_t)
            + 2 * len(q_tokens & desc_t)
            + 2 * len(q_tokens & kw_t)
            + 1 * len(q_tokens & fam_t)
        )

        # Also boost direct AXN-hex matches
        for tok in q_tokens:
            if m.get("hex", "").lower() == tok or m.get("axn", "").lower().startswith(f"axn:{tok}"):
                score += 10

        if score > 0:
            scored.append((score, m))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = []
    for score, m in scored[:limit]:
        results.append({
            "axn": m["axn"],
            "title": m.get("title"),
            "family": m.get("family"),
            "date": m.get("date"),
            "description": (m.get("description") or "")[:500],
            "score": score,
        })
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Sigil call
# ─────────────────────────────────────────────────────────────────────────────

def build_system_prompt(mode: str) -> str:
    note = MERKABAH_MODE_NOTE if mode == "merkabah" else SABBATH_MODE_NOTE
    return SIGIL_VOICE + note


def extract_navigation(text: str) -> dict | None:
    """Find a fenced ```json block containing a {"navigate": {...}} object."""
    fence_re = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)
    for m in fence_re.finditer(text):
        try:
            obj = json.loads(m.group(1))
            if isinstance(obj, dict) and isinstance(obj.get("navigate"), dict):
                return obj["navigate"]
        except json.JSONDecodeError:
            continue
    return None


def strip_navigation_fence(text: str) -> str:
    """Remove the fenced ```json block(s) from the prose for display."""
    return re.sub(r"```json\s*\n.*?\n```", "", text, flags=re.DOTALL).strip()


def call_sigil(message: str, history: list[dict], mode: str, api_key: str) -> dict:
    """Run Sigil with tool-use loop. Returns {say, navigate, retrievals}."""
    # Import lazily so this doesn't break the function's cold-start health check
    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    system = build_system_prompt(mode)

    # Build the messages array (history + new turn)
    messages = list(history) + [{"role": "user", "content": message}]
    retrievals: list[dict] = []

    for _ in range(MAX_TOOL_TURNS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system,
            tools=[SEARCH_ARCHIVE_TOOL],
            messages=messages,
        )

        # Check for tool use
        tool_blocks = [b for b in response.content if b.type == "tool_use"]
        if not tool_blocks:
            # No tool use — Sigil's final response
            text_blocks = [b.text for b in response.content if b.type == "text"]
            full_text = "\n".join(text_blocks).strip()
            navigate = extract_navigation(full_text) if mode == "merkabah" else None
            say = strip_navigation_fence(full_text)
            return {"say": say, "navigate": navigate, "retrievals": retrievals}

        # Execute tool calls and append to messages
        messages.append({"role": "assistant", "content": response.content})
        tool_results_content = []
        for tb in tool_blocks:
            if tb.name == "search_archive":
                query = tb.input.get("query", "")
                results = search_archive(query)
                retrievals.extend([{"axn": r["axn"], "title": r["title"]} for r in results])
                tool_results_content.append({
                    "type": "tool_result",
                    "tool_use_id": tb.id,
                    "content": json.dumps(results),
                })
            else:
                tool_results_content.append({
                    "type": "tool_result",
                    "tool_use_id": tb.id,
                    "content": json.dumps({"error": f"Unknown tool: {tb.name}"}),
                    "is_error": True,
                })
        messages.append({"role": "user", "content": tool_results_content})

    # Hit the tool-turn cap without a final response — synthesize a brief halt
    return {
        "say": "I am reaching the limit of how many archive searches I can run in a single turn. "
               "Could you narrow the question, or ask again with a more specific framing?",
        "navigate": None,
        "retrievals": retrievals,
    }


# ─────────────────────────────────────────────────────────────────────────────
# HTTP handler (Vercel-compatible)
# ─────────────────────────────────────────────────────────────────────────────

class handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, body: dict):
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        self._send_json(204, {})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}

            message = body.get("message", "").strip()
            history = body.get("history", [])
            mode = body.get("mode", "sabbath")
            api_key = body.get("anthropic_key") or os.environ.get("ANTHROPIC_API_KEY")

            if not message:
                self._send_json(400, {"error": "message is required"})
                return

            if not api_key:
                self._send_json(401, {
                    "error": "No Anthropic API key. Provide your own in the form, "
                             "or this demo is currently without a fallback key configured."
                })
                return

            if mode not in ("sabbath", "merkabah"):
                self._send_json(400, {"error": "mode must be 'sabbath' or 'merkabah'"})
                return

            result = call_sigil(message, history, mode, api_key)
            self._send_json(200, result)
        except Exception as e:
            # Don't leak the API key in any error path
            self._send_json(500, {
                "error": f"{type(e).__name__}: {str(e)}"
            })
