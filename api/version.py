"""Live-deployment witness: GET /api/version returns the commit actually serving.
So the MANUS never has to wonder what is live (2026-07-04)."""
import json, os
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({
            "commit": os.environ.get("VERCEL_GIT_COMMIT_SHA", "unknown")[:12],
            "message": os.environ.get("VERCEL_GIT_COMMIT_MESSAGE", "")[:100],
            "deployed": True,
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
