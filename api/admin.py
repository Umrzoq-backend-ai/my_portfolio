from http.server import BaseHTTPRequestHandler
import json, os, sys, base64, time, hashlib, hmac
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import seed_data as sd

# ---- Auth ----
def _secret():
    s = os.environ.get("SECRET_KEY","")
    if s: return s.encode()
    return (os.environ.get("ADMIN_PASSWORD","admin123")+"_pf_secret").encode()

def _make_token(user):
    exp = int(time.time())+43200
    p = base64.urlsafe_b64encode(json.dumps({"u":user,"exp":exp}).encode()).decode().rstrip("=")
    sig = base64.urlsafe_b64encode(hmac.new(_secret(),p.encode(),hashlib.sha256).digest()).decode().rstrip("=")
    return f"{p}.{sig}"

def _verify(token):
    try:
        p,sig = token.split(".",1)
        exp_sig = base64.urlsafe_b64encode(hmac.new(_secret(),p.encode(),hashlib.sha256).digest()).decode().rstrip("=")
        if not hmac.compare_digest(sig, exp_sig): return None
        data = json.loads(base64.urlsafe_b64decode(p+"="*(-len(p)%4)))
        return data["u"] if data["exp"] > int(time.time()) else None
    except: return None

def _get_cookie(headers, name):
    for part in headers.get("Cookie","").split(";"):
        part = part.strip()
        if part.startswith(name+"="):
            return part[len(name)+1:]
    return ""

# ---- Seed data as dicts ----
def _profile():
    p = dict(sd.PROFILE)
    if not p.get("avatar"): p["avatar"] = "/assets/photo.jpg"
    return p

def _skills():
    return [{"id":i+1,"category":s[0],"name":s[1],"level":s[2],"sort":s[3]} for i,s in enumerate(sd.SKILLS)]

def _projects():
    return [{**p,"id":i+1} for i,p in enumerate(sd.PROJECTS)]

def _certificates():
    return [{**c,"id":i+1} for i,c in enumerate(sd.CERTIFICATES)]

def _experience():
    return [{**e,"id":i+1} for i,e in enumerate(sd.EXPERIENCE)]

def _blog():
    return [{**b,"id":i+1,"created_at":"2024-01-01"} for i,b in enumerate(sd.BLOG)]

def _messages():
    return []  # Vercel'da xabarlar saqlanmaydi

class handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","GET,POST,PUT,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type,Cookie")

    def _json(self, data, status=200, extra=None):
        b = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        if extra:
            for k,v in extra.items(): self.send_header(k,v)
        self._cors(); self.end_headers(); self.wfile.write(b)

    def _auth(self):
        token = _get_cookie(self.headers, "pf_session")
        return _verify(token)

    def _read(self):
        n = int(self.headers.get("Content-Length",0) or 0)
        if not n: return {}
        try: return json.loads(self.rfile.read(n).decode())
        except: return {}

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")

        # Session check (no auth needed)
        if path.endswith("session"):
            token = _get_cookie(self.headers,"pf_session")
            return self._json({"authenticated": bool(_verify(token))})

        # All other GET routes require auth
        if not self._auth():
            return self._json({"error":"unauthorized"}, 401)

        if path.endswith("profile"):
            return self._json(_profile())
        if path.endswith("skills"):
            return self._json(_skills())
        if path.endswith("projects"):
            return self._json(_projects())
        if path.endswith("certificates"):
            return self._json(_certificates())
        if path.endswith("experience"):
            return self._json(_experience())
        if path.endswith("blog"):
            return self._json(_blog())
        if path.endswith("messages"):
            return self._json(_messages())

        self._json({"error":"not found"}, 404)

    def do_POST(self):
        path = self.path.split("?")[0].rstrip("/")
        data = self._read()

        # Login
        if path.endswith("login"):
            u = os.environ.get("ADMIN_USERNAME","admin")
            p = os.environ.get("ADMIN_PASSWORD","admin123")
            iu = (data.get("username") or "").strip()
            ip = (data.get("password") or "")
            if not (hmac.compare_digest(iu,u) and hmac.compare_digest(ip,p)):
                return self._json({"error":"Login yoki parol xato"}, 401)
            token = _make_token(iu)
            cookie = f"pf_session={token}; HttpOnly; Path=/; SameSite=Lax; Max-Age=43200"
            return self._json({"ok":True}, extra={"Set-Cookie":cookie})

        if not self._auth():
            return self._json({"error":"unauthorized"}, 401)

        if path.endswith("logout"):
            return self._json({"ok":True}, extra={"Set-Cookie":"pf_session=; HttpOnly; Path=/; Max-Age=0"})

        if path.endswith("password"):
            return self._json({"ok":True, "message":"Parolni Vercel Environment Variables dan o'zgartiring"})

        # CRUD create — Vercel'da DB yo'q, faqat OK qaytaramiz
        self._json({"ok":True, "id":1, "note":"Vercel read-only. O'zgartirishlar local versiyada saqlanadi."})

    def do_PUT(self):
        if not self._auth():
            return self._json({"error":"unauthorized"}, 401)
        self._json({"ok":True, "note":"Vercel read-only. O'zgartirishlar local versiyada saqlanadi."})

    def do_DELETE(self):
        if not self._auth():
            return self._json({"error":"unauthorized"}, 401)
        self._json({"ok":True, "note":"Vercel read-only."})

    def log_message(self, *a): pass
