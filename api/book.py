# ═══ DEPENDENCIES (INSTANCE-PROTOCOL.md) ═════════════════════════════════
# PROVIDES: Book/reading records (GitHub contents API).
# CALLED-BY: chat.js; transform.py inscription path shares its record shapes.
# CONTRACTS: record schemas are read by chat.js and the static Book surfaces.
# MUST-READ-BEFORE-EDITING: this header; transform.py inscribe(); consumers.
# ═════════════════════════════════════════════════════════════════════════

"""
api/book.py — The Book of Auto-Appended Conversations
─────────────────────────────────────────────────────

Endpoint: POST /api/book/append
Body: { session_id, history, mode, started_at, witness_id?, attribution? }

Behavior:
  1. Compute or retrieve the AXN for this session.
     - First turn: mint a new AXN from the content of the first witness message
       (6-emoji content-derived hash + hex offset 11 + family designation).
     - Subsequent turns: use the AXN that was minted at first turn (passed back
       by the client as session.axn).
  2. Commit the conversation JSON to book/data/AXN-XXXX.json via GitHub API.
  3. Update book/index.json with the latest entry summary.
  4. Return the AXN and a stable URL where the conversation can be viewed.

The conversation JSON contains:
  - axn: the content-derived identifier
  - session_id: client-generated UUID, hashed for storage
  - started_at: ISO timestamp of session start
  - last_updated: ISO timestamp of latest turn
  - mode: 'sabbath' or 'merkabah'
  - turn_count: integer
  - history: full conversation [{role, content, ...}, ...]
  - witness: 'anonymous' or attributed name (Phase 2 affordance)

Auth / security:
  - Requires GITHUB_BOOK_TOKEN env var (fine-grained PAT, the-mandala-oracle
    repo only, write content permission)
  - Endpoint is CORS-restricted to the deployed Oracle's domain
  - Witness session_id is hashed on receipt; raw session_id is never stored
  - No IP logging, no API key fragment storage

Per-session granularity (B-A4 adjudication): one AXN per conversation. The file
grows as turns are appended. AXN stable from first turn.
"""

import os
import json
import hashlib
import base64
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────

GITHUB_REPO = "leesharks000/the-mandala-oracle"
GITHUB_BRANCH = "main"
GITHUB_TOKEN_ENV = "GITHUB_BOOK_TOKEN"
BOOK_DIR = "book/data"
BOOK_INDEX_PATH = "book/index.json"
BOOK_FAMILY = "CONVERSATION"  # Family designation for Book AXNs


class BookCredentialsInvalid(RuntimeError):
    """The storage token is present but rejected by GitHub (expired/revoked)."""


# ──────────────────────────────────────────────────────────────────────
# AXN minting
# ──────────────────────────────────────────────────────────────────────

# 32 glyphs in the standard cha emoji pool (per existing alexanarch protocol)
AXN_GLYPHS = [
    "🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘",
    "⭐", "🌟", "💫", "☀️", "🌙", "🪐", "🌍", "🌊",
    "🔥", "💧", "🌪️", "⚡", "❄️", "🌋", "🏔️", "🌿",
    "🍃", "🌱", "🌾", "🪨", "💎", "🧊", "🌈", "☁️",
]

AXN_HEX_OFFSET = 11  # Empirically verified offset per standing protocol


def mint_axn(first_turn_content: str) -> str:
    """
    Mint an AXN from the first turn's content.

    Format: AXN:NNNN.FAMILY.EMOJI1EMOJI2EMOJI3EMOJI4EMOJI5EMOJI6
    Where NNNN is hex(SHA256(content) mod 65536) and emojis are derived
    from successive byte-positions of the hash with offset 11.

    For the Book, family is always CONVERSATION.
    """
    h = hashlib.sha256(first_turn_content.encode("utf-8")).digest()
    # Hex position: first two bytes mod 65536 with offset 11
    hex_val = ((h[0] << 8 | h[1]) + AXN_HEX_OFFSET) % 65536
    hex_str = f"{hex_val:04X}"
    # Six emojis from successive byte positions
    emojis = "".join(AXN_GLYPHS[h[i + 2] % len(AXN_GLYPHS)] for i in range(6))
    return f"AXN:{hex_str}.{BOOK_FAMILY}.{emojis}"


def hash_session_id(session_id: str) -> str:
    """Hash the client-generated session_id for storage (never store raw)."""
    return hashlib.sha256(session_id.encode("utf-8")).hexdigest()[:16]


# ──────────────────────────────────────────────────────────────────────
# GitHub API helpers
# ──────────────────────────────────────────────────────────────────────

def _gh_request(method: str, path: str, body: dict | None = None) -> dict:
    """Make an authenticated GitHub API request."""
    token = os.environ.get(GITHUB_TOKEN_ENV)
    if not token:
        raise RuntimeError(f"Missing env var {GITHUB_TOKEN_ENV}")

    url = f"https://api.github.com{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        req.add_header("Content-Type", "application/json")

    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        # 404 is meaningful for "does this file exist yet" lookups
        if e.code == 404:
            return {"_not_found": True}
        body = e.read().decode("utf-8", errors="replace")
        # 401/403 mean the token is present but no longer valid — expired,
        # revoked, or scope-narrowed. This is NOT a transient error and must be
        # distinguished from one: on 2026-07-19 the fine-grained PAT expired and
        # every append failed with 401 for four weeks while the client swallowed
        # the 500 and retried on every turn. The Oracle looked healthy and
        # recorded nothing. Raised as a distinct type so the handler can answer
        # 503 (which stops the client retrying) with an actionable reason.
        if e.code in (401, 403):
            raise BookCredentialsInvalid(
                f"GitHub rejected the {GITHUB_TOKEN_ENV} credential ({e.code}). "
                f"The token is present but not valid — most likely expired. "
                f"Mint a new fine-grained PAT (contents:write on {GITHUB_REPO}) "
                f"and set {GITHUB_TOKEN_ENV} in the Vercel project."
            )
        raise RuntimeError(f"GitHub API {method} {path} failed: {e.code} {body}")


def gh_get_file(repo_path: str) -> tuple[dict | None, str | None]:
    """
    Get a file's content and SHA from GitHub.
    Returns (content_dict, sha) or (None, None) if not found.
    """
    resp = _gh_request("GET", f"/repos/{GITHUB_REPO}/contents/{repo_path}?ref={GITHUB_BRANCH}")
    if resp.get("_not_found"):
        return None, None
    raw = base64.b64decode(resp["content"]).decode("utf-8")
    return json.loads(raw), resp["sha"]


def gh_put_file(repo_path: str, content: dict, message: str, sha: str | None = None) -> dict:
    """Create or update a file in the repo via GitHub API."""
    body = {
        "message": message,
        "content": base64.b64encode(json.dumps(content, ensure_ascii=False, indent=2).encode("utf-8")).decode("ascii"),
        "branch": GITHUB_BRANCH,
    }
    if sha:
        body["sha"] = sha
    return _gh_request("PUT", f"/repos/{GITHUB_REPO}/contents/{repo_path}", body)


# ──────────────────────────────────────────────────────────────────────
# Book operations
# ──────────────────────────────────────────────────────────────────────

def axn_to_filename(axn: str) -> str:
    """AXN:XXXX.CONVERSATION.EMOJIS → AXN-XXXX.json (filesystem-safe)."""
    parts = axn.split(".")
    return f"AXN-{parts[0].replace('AXN:', '')}.json"


def upsert_conversation(axn: str, payload: dict) -> dict:
    """
    Create or update a conversation file in book/data/.
    Returns the content dict that was written — callers can pass this
    directly to update_index without re-fetching, which avoids a race
    against GitHub's eventually-consistent reads (a re-fetch immediately
    after a write sometimes returned stale or None, and the old code
    silently skipped the index update in that case, orphaning single-turn
    conversations on disk without index entries).
    """
    filename = axn_to_filename(axn)
    repo_path = f"{BOOK_DIR}/{filename}"

    existing, sha = gh_get_file(repo_path)

    # Build the new content
    now = datetime.now(timezone.utc).isoformat()
    content = {
        "axn": axn,
        "session_id_hash": payload["session_id_hash"],
        "started_at": payload.get("started_at") or now,
        "last_updated": now,
        "mode": payload.get("mode", "sabbath"),
        "turn_count": len(payload["history"]) // 2,  # approximate user+assistant pairs
        "history": payload["history"],
        "witness": payload.get("witness", "anonymous"),
        "schema_version": "v1.0",
    }

    if existing:
        # Preserve original started_at on subsequent appends
        content["started_at"] = existing.get("started_at", content["started_at"])
        message = f"book: append turn to {axn} (turn {content['turn_count']}) [skip ci]"
    else:
        message = f"book: mint {axn} [skip ci]"

    gh_put_file(repo_path, content, message, sha=sha)
    return content


def update_index(axn: str, content: dict) -> None:
    """
    Update book/index.json with the latest summary for this conversation.
    Index is a flat list of conversation summaries; entries are upserted by AXN.
    """
    index, sha = gh_get_file(BOOK_INDEX_PATH)
    if index is None:
        index = {
            "schema_version": "v1.0",
            "description": "Index of auto-appended Mandala Oracle conversations. Each entry summarizes one session; full content is at book/data/AXN-XXXX.json.",
            "conversations": [],
        }

    # Build the summary entry
    first_user_msg = next(
        (h["content"] for h in content["history"] if h.get("role") == "user"),
        "",
    )
    snippet = first_user_msg[:200] + ("…" if len(first_user_msg) > 200 else "")

    entry = {
        "axn": axn,
        "started_at": content["started_at"],
        "last_updated": content["last_updated"],
        "mode": content["mode"],
        "turn_count": content["turn_count"],
        "witness": content["witness"],
        "opening_snippet": snippet,
    }

    # Upsert: replace if AXN exists, else prepend
    existing_idx = next(
        (i for i, e in enumerate(index["conversations"]) if e["axn"] == axn),
        None,
    )
    if existing_idx is not None:
        index["conversations"][existing_idx] = entry
    else:
        index["conversations"].insert(0, entry)

    # Keep most recent N (defensive cap; can be raised)
    index["conversations"] = index["conversations"][:500]
    index["total_recorded"] = len(index["conversations"])
    index["last_updated"] = content["last_updated"]

    gh_put_file(BOOK_INDEX_PATH, index, f"book: update index for {axn} [skip ci]", sha=sha)


# ──────────────────────────────────────────────────────────────────────
# Vercel Python serverless handler
# ──────────────────────────────────────────────────────────────────────

class handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self._send_json(200, {})

    def do_POST(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            body = json.loads(raw)

            # Validate required fields
            session_id = body.get("session_id")
            history = body.get("history")
            if not session_id or not isinstance(history, list) or not history:
                return self._send_json(400, {"error": "session_id and non-empty history required"})

            session_id_hash = hash_session_id(session_id)

            # AXN: client provides if known (subsequent turns); we mint on first
            axn = body.get("axn")
            if not axn:
                # First turn — mint from first user message content
                first_user = next((h["content"] for h in history if h.get("role") == "user"), "")
                if not first_user:
                    return self._send_json(400, {"error": "first user message required for minting"})
                axn = mint_axn(first_user)

            payload = {
                "session_id_hash": session_id_hash,
                "started_at": body.get("started_at"),
                "mode": body.get("mode", "sabbath"),
                "history": history,
                "witness": body.get("attribution") or "anonymous",
            }

            # Check env var presence early; fail clearly if not configured
            if not os.environ.get(GITHUB_TOKEN_ENV):
                return self._send_json(503, {
                    "error": "book_storage_not_configured",
                    "detail": f"Server is missing {GITHUB_TOKEN_ENV}; Book appending is disabled until configured.",
                })

            # Write the conversation file and pass the resulting content
            # directly to the index update. Earlier code re-fetched here via
            # gh_get_file and bailed silently if the fetch returned None
            # (which happened often on the first write of a new conversation,
            # because GitHub's contents API is eventually consistent). That
            # bug left two single-turn conversations orphaned on disk without
            # index entries; the canonical fix is to skip the re-fetch.
            try:
                committed = upsert_conversation(axn, payload)
                update_index(axn, committed)
            except BookCredentialsInvalid as e:
                # 503 so the client marks appendingEnabled=false and stops
                # hammering; the detail names the exact remedy.
                return self._send_json(503, {
                    "error": "book_storage_credentials_invalid",
                    "detail": str(e),
                })

            self._send_json(200, {
                "axn": axn,
                "url": f"https://alexanarch.org/book/#{axn}",
                "status": "appended",
            })

        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid_json"})
        except RuntimeError as e:
            self._send_json(500, {"error": "internal_error", "detail": str(e)})
        except Exception as e:
            self._send_json(500, {"error": "unexpected", "detail": str(e)})
