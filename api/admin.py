from http.server import BaseHTTPRequestHandler
import json, os, sys, base64, time, hashlib, hmac
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _secret():
    s = os.environ.get("SECRET_KEY","")
    if s: return s.encode()
    return (os.environ.get("ADMIN_PASSWORD","admin123")+"_portfolio_secret").encode()

def _make_token(user):
    exp = int(time.time())+43200
    p = base64.urlsafe_b64encode(json.dumps({"u":user,"exp":exp}).encode()).decode().rstrip("=")
    sig = base64.urlsafe_b64encode(hmac.new(_secret(),p.encode(),hashlib.sha256).digest()).decode().rstrip("=")
    return f"{p}.{sig}"

def _verify(token):
    try:
        p,sig=token.split(".",1)
        exp_sig=base64.urlsafe_b64encode(hmac.new(_secret(),p.encode(),hashlib.sha256).digest()).decode().rstrip("=")
        if not hmac.compare_digest(sig,exp_sig): return None
        data=json.loads(base64.urlsafe_b64decode(p+"="*(-len(p)%4)))
        return data["u"] if data["exp"]>int(time.time()) else None
    except: return None

def _get_cookie(headers, name):
    cookie_str = headers.get("Cookie","")
    for part in cookie_str.split(";"):
        part=part.strip()
        if part.startswith(name+"="):
            return part[len(name)+1:]
    return ""

class handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type,Cookie")
    def _json(self,data,status=200,extra_headers=None):
        b=json.dumps(data,ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(b)))
        if extra_headers:
            for k,v in extra_headers.items(): self.send_header(k,v)
        self._cors(); self.end_headers(); self.wfile.write(b)
    def do_OPTIONS(self): self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]
        if "session" in path:
            token = _get_cookie(self.headers,"pf_session")
            self._json({"authenticated": bool(_verify(token))})
        else:
            self._json({"error":"not found"},404)

    def do_POST(self):
        path = self.path.split("?")[0]
        length=int(self.headers.get("Content-Length",0) or 0)
        data=json.loads(self.rfile.read(length).decode()) if length else {}

        if "login" in path:
            u = os.environ.get("ADMIN_USERNAME","admin")
            p = os.environ.get("ADMIN_PASSWORD","admin123")
            inp_u=(data.get("username") or "").strip()
            inp_p=(data.get("password") or "")
            u_ok=hmac.compare_digest(inp_u,u)
            p_ok=hmac.compare_digest(inp_p,p)
            if not (u_ok and p_ok):
                return self._json({"error":"Login yoki parol xato"},401)
            token=_make_token(inp_u)
            cookie=f"pf_session={token}; HttpOnly; Path=/; SameSite=Lax; Max-Age=43200"
            self._json({"ok":True},extra_headers={"Set-Cookie":cookie})

        elif "logout" in path:
            cookie="pf_session=; HttpOnly; Path=/; Max-Age=0"
            self._json({"ok":True},extra_headers={"Set-Cookie":cookie})

        elif "password" in path:
            token=_get_cookie(self.headers,"pf_session")
            if not _verify(token): return self._json({"error":"unauthorized"},401)
            # Vercel'da parol o'zgartirib bo'lmaydi (env variables)
            self._json({"ok":True,"message":"Parolni Vercel Environment Variables dan o'zgartiring"})

        else:
            self._json({"error":"not found"},404)

    def log_message(self,*a): pass
