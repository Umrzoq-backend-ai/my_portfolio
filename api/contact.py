"""POST /api/contact — email yuborish"""
import json, os, smtplib, threading
from http.server import BaseHTTPRequestHandler
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def _send_email(name, email, message):
    gmail_user = os.environ.get("GMAIL_USER","")
    gmail_pass = os.environ.get("GMAIL_PASS","")
    notify_to  = os.environ.get("NOTIFY_EMAIL","")
    if not (gmail_user and gmail_pass and notify_to):
        return
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📬 Portfolio: {name} dan yangi xabar"
        msg["From"]    = gmail_user
        msg["To"]      = notify_to
        text = f"Yangi xabar!\n\nIsm: {name}\nEmail: {email or 'yo`q'}\n\nXabar:\n{message}"
        html = f"""<div style="font-family:sans-serif;max-width:500px;padding:20px;background:#0d0e18;color:#e8eaf2;border-radius:12px">
<h2 style="color:#00ffaa">📬 Yangi xabar — Portfolio</h2>
<p><b>Ism:</b> {name}</p>
<p><b>Email:</b> {email or "ko`rsatilmagan"}</p>
<div style="padding:14px;background:#1a1b2e;border-radius:8px;border-left:3px solid #00ffaa;margin-top:12px">
<p style="margin:0">{message.replace(chr(10),"<br>")}</p></div></div>"""
        msg.attach(MIMEText(text,"plain","utf-8"))
        msg.attach(MIMEText(html,"html","utf-8"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as s:
            s.login(gmail_user, gmail_pass)
            s.sendmail(gmail_user, notify_to, msg.as_string())
    except Exception as e:
        print(f"[EMAIL] xato: {e}")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        try:
            data = json.loads(self.rfile.read(length).decode()) if length else {}
        except Exception:
            data = {}
        name    = (data.get("name") or "").strip()
        email   = (data.get("email") or "").strip()
        message = (data.get("message") or "").strip()

        if not name or not message:
            body = json.dumps({"error": "Ism va xabar majburiy"}).encode()
            self.send_response(400)
        else:
            threading.Thread(target=_send_email, args=(name, email, message), daemon=True).start()
            body = json.dumps({"ok": True}).encode()
            self.send_response(200)

        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()

    def log_message(self, *a): pass
