"""GET /api/portfolio — Vercel serverless function"""
import json, sys, os
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import seed_data as sd

PROFILE = dict(sd.PROFILE)
if not PROFILE.get("avatar"):
    PROFILE["avatar"] = "/assets/photo.jpg"

SKILLS = [
    {"id": i+1, "category": s[0], "name": s[1], "level": s[2], "sort": s[3]}
    for i, s in enumerate(sd.SKILLS)
]
PROJECTS  = [{**p, "id": i+1} for i, p in enumerate(sd.PROJECTS)]
CERTS     = [{**c, "id": i+1} for i, c in enumerate(sd.CERTIFICATES)]
EXPERIENCE= [{**e, "id": i+1} for i, e in enumerate(sd.EXPERIENCE)]
BLOG      = [{**b, "id": i+1, "created_at": "2024-01-01"} for i, b in enumerate(sd.BLOG) if b.get("published")]

DATA = json.dumps({
    "profile": PROFILE,
    "skills": SKILLS,
    "projects": PROJECTS,
    "certificates": CERTS,
    "experience": EXPERIENCE,
    "blog": BLOG,
}, ensure_ascii=False)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = DATA.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, *a): pass
