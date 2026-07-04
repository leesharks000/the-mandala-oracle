"""share.py — mint a public, permanent link to a thread (MANUS request, 2026-07-04).

POST {session_id, title, items:[{who, text}]} → writes shares/SH-<id>.json to
the Book repo ([skip ci]) → returns the viewer URL /t/SH-<id>. The share is a
public artifact by design; the button says so. Text-only payload; the viewer
escapes everything (no HTML transits)."""
import base64, hashlib, json, os, re, time, urllib.request
from http.server import BaseHTTPRequestHandler

GH_REPO = "leesharks000/the-mandala-oracle"
GH_TOKEN_ENV = "GITHUB_BOOK_TOKEN"
MAX_ITEMS, MAX_TOTAL, MAX_ITEM = 400, 250_000, 40_000

def _tok():
    return os.environ.get(GH_TOKEN_ENV, "") or os.environ.get("GITHUB_TOKEN", "")

def _clean(s: str, cap: int) -> str:
    s = re.sub(r"[\u0000-\u0008\u000B\u000C\u000E-\u001F\u202A-\u202E\u2066-\u2069]", "", str(s))
    return s[:cap]

def gh_put(path: str, content: dict, message: str):
    url = f"https://api.github.com/repos/{GH_REPO}/contents/{path}"
    body = {"message": message,
            "content": base64.b64encode(json.dumps(content, ensure_ascii=False, indent=1).encode()).decode()}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="PUT",
        headers={"Authorization": f"Bearer {_tok()}", "Accept": "application/vnd.github+json",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status

class handler(BaseHTTPRequestHandler):
    def _json(self, status, payload):
        b = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        self._json(200, {"ok": True})

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:
            return self._json(400, {"ok": False, "error": "unreadable body"})
        items = body.get("items") or []
        if not isinstance(items, list) or not items:
            return self._json(400, {"ok": False, "error": "no thread items"})
        clean, total = [], 0
        for it in items[:MAX_ITEMS]:
            who = _clean((it or {}).get("who", ""), 120)
            text = _clean((it or {}).get("text", ""), MAX_ITEM)
            if not text.strip():
                continue
            total += len(text)
            if total > MAX_TOTAL:
                break
            clean.append({"who": who, "text": text})
        if not clean:
            return self._json(400, {"ok": False, "error": "empty thread"})
        sid = _clean(body.get("session_id", ""), 80)
        share_id = "SH-" + hashlib.sha256(f"{sid}|{time.time()}".encode()).hexdigest()[:10]
        rec = {"id": share_id, "schema": "share/v1",
               "title": _clean(body.get("title", "The Mandala Oracle — a thread"), 200),
               "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "session_id_hash": hashlib.sha256(sid.encode()).hexdigest()[:16] if sid else "",
               "items": clean}
        try:
            code = gh_put(f"shares/{share_id}.json", rec,
                          f"share: mint {share_id} [skip ci]")
        except Exception as e:
            return self._json(502, {"ok": False, "error": f"inscription failed ({e})"})
        if code not in (200, 201):
            return self._json(502, {"ok": False, "error": f"inscription failed (HTTP {code})"})
        return self._json(200, {"ok": True, "id": share_id, "url": f"/t/{share_id}"})
