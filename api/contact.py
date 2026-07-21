from http.server import BaseHTTPRequestHandler
import json, os, smtplib, threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def _send(name, email, message):
    gu = os.environ.get("GMAIL_USER",""); gp = os.environ.get("GMAIL_PASS",""); nt = os.environ.get("NOTIFY_EMAIL","")
    if not (gu and gp and nt): return
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📬 Portfolio: {name} dan yangi xabar"
        msg["From"] = gu; msg["To"] = nt
        msg.attach(MIMEText(f"Ism: {name}\nEmail: {email}\n\nXabar:\n{message}","plain","utf-8"))
        with smtplib.SMTP_SSL("smtp.gmail.com",465,timeout=10) as s:
            s.login(gu,gp); s.sendmail(gu,nt,msg.as_string())
    except Exception as ex: print(f"[EMAIL] {ex}")

class handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
    def _json(self,data,status=200):
        b=json.dumps(data,ensure_ascii=False).encode()
        self.send_response(status); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(b))); self._cors(); self.end_headers(); self.wfile.write(b)
    def do_OPTIONS(self): self.send_response(204); self._cors(); self.end_headers()
    def do_POST(self):
        length=int(self.headers.get("Content-Length",0) or 0)
        data=json.loads(self.rfile.read(length).decode()) if length else {}
        name=(data.get("name") or "").strip(); msg=(data.get("message") or "").strip()
        if not name or not msg: return self._json({"error":"Ism va xabar majburiy"},400)
        threading.Thread(target=_send,args=(name,data.get("email",""),msg),daemon=True).start()
        self._json({"ok":True})
    def log_message(self,*a): pass
