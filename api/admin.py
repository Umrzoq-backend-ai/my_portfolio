"""
/api/admin/* — Vercel serverless admin API
Vercel'da persistent storage yo'q — seed_data dan o'qish.
To'liq admin uchun Render.com ishlatiladi.
"""
import json, os, sys
from http.server import BaseHTTPRequestHandler
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import seed_data as sd

ADMIN_PASS = os.environ.get("ADMIN_PASSWORD", "admin123")

def _json(data):
    return json.dumps(data, ensure_ascii=False).encode("utf-8")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.rstrip("/")

        if path == "/api/admin/session":
            body = _json({"authenticated": False, "message": "Admin panel Render.com da ishlaydi"})
            self.send_response(200)
        elif path == "/api/admin/portfolio":
            body = _json({
                "profile": sd.PROFILE,
                "skills": sd.SKILLS,
                "projects": sd.PROJECTS,
            })
            self.send_response(200)
        else:
            body = _json({"error": "not found"})
            self.send_response(404)

        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        body = _json({"message": "Admin panel Render.com da mavjud: https://umrzoq-yulchiyev.onrender.com/admin"})
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
