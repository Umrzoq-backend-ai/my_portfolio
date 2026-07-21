from http.server import BaseHTTPRequestHandler
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import seed_data as sd

PROFILE = dict(sd.PROFILE)
if not PROFILE.get("avatar"):
    PROFILE["avatar"] = "/assets/photo.jpg"

DATA = json.dumps({
    "profile": PROFILE,
    "skills": [{"id":i+1,"category":s[0],"name":s[1],"level":s[2],"sort":s[3]} for i,s in enumerate(sd.SKILLS)],
    "projects":     [{**p,"id":i+1} for i,p in enumerate(sd.PROJECTS)],
    "certificates": [{**c,"id":i+1} for i,c in enumerate(sd.CERTIFICATES)],
    "experience":   [{**e,"id":i+1} for i,e in enumerate(sd.EXPERIENCE)],
    "blog":         [{**b,"id":i+1,"created_at":"2024-01-01"} for i,b in enumerate(sd.BLOG) if b.get("published")],
}, ensure_ascii=False)

class handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_GET(self):
        b = DATA.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(b)))
        self._cors(); self.end_headers(); self.wfile.write(b)
    def log_message(self,*a): pass
