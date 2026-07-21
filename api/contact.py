"""POST /api/contact — Vercel serverless"""
import json, os, smtplib, threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def _send_email(name, email, message):
    gmail_user = os.environ.get("GMAIL_USER", "")
    gmail_pass = os.environ.get("GMAIL_PASS", "")
    notify_to  = os.environ.get("NOTIFY_EMAIL", "")
    if not (gmail_user and gmail_pass and notify_to):
        return
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📬 Portfolio: {name} dan yangi xabar"
        msg["From"]    = gmail_user
        msg["To"]      = notify_to
        text = f"Yangi xabar!\n\nIsm: {name}\nEmail: {email or 'yo`q'}\n\nXabar:\n{message}"
        html = f"""<div style="font-family:sans-serif;max-width:500px;padding:20px">
<h2 style="color:#00ffaa">📬 Yangi xabar — Portfolio</h2>
<p><b>Ism:</b> {name}</p><p><b>Email:</b> {email or 'ko`rsatilmagan'}</p>
<div style="padding:14px;background:#f5f5f5;border-radius:8px;border-left:3px solid #00ffaa">
<p>{message.replace(chr(10),'<br>')}</p></div></div>"""
        msg.attach(MIMEText(text, "plain", "utf-8"))
        msg.attach(MIMEText(html, "html",  "utf-8"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as s:
            s.login(gmail_user, gmail_pass)
            s.sendmail(gmail_user, notify_to, msg.as_string())
        print(f"[EMAIL] sent to {notify_to}")
    except Exception as e:
        print(f"[EMAIL] error: {e}")

def handler(request, response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Content-Type"] = "application/json; charset=utf-8"

    if request.method == "OPTIONS":
        response.status_code = 204
        return response

    try:
        data = json.loads(request.body or "{}")
    except Exception:
        data = {}

    name    = (data.get("name") or "").strip()
    email   = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not message:
        response.status_code = 400
        response.body = json.dumps({"error": "Ism va xabar majburiy"})
        return response

    threading.Thread(target=_send_email, args=(name, email, message), daemon=True).start()
    response.status_code = 200
    response.body = json.dumps({"ok": True})
    return response
