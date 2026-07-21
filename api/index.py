"""
Vercel Flask API — portfolio backend
"""
import json, os, sys, urllib.request, urllib.error, smtplib, threading
from flask import Flask, request, jsonify
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import seed_data as sd

app = Flask(__name__)

# ---- CORS ----
@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"]  = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return resp

@app.route("/api/portfolio", methods=["GET","OPTIONS"])
def portfolio():
    if request.method == "OPTIONS":
        return "", 204
    profile = dict(sd.PROFILE)
    if not profile.get("avatar"):
        profile["avatar"] = "/assets/photo.jpg"
    return jsonify({
        "profile": profile,
        "skills": [
            {"id": i+1, "category": s[0], "name": s[1], "level": s[2], "sort": s[3]}
            for i, s in enumerate(sd.SKILLS)
        ],
        "projects":     [{**p, "id": i+1} for i, p in enumerate(sd.PROJECTS)],
        "certificates": [{**c, "id": i+1} for i, c in enumerate(sd.CERTIFICATES)],
        "experience":   [{**e, "id": i+1} for i, e in enumerate(sd.EXPERIENCE)],
        "blog": [
            {**b, "id": i+1, "created_at": "2024-01-01"}
            for i, b in enumerate(sd.BLOG) if b.get("published")
        ],
    })

# ---- AI ----
def _knowledge():
    p = sd.PROFILE
    skills   = ", ".join(f"{s[1]} ({s[2]}%)" for s in sd.SKILLS)
    projects = "; ".join(f"{pr['title_en']}: {pr['desc_en']}" for pr in sd.PROJECTS)
    exp      = "; ".join(f"{e['role_en']} @ {e['org']}" for e in sd.EXPERIENCE)
    return f"""You are the AI assistant on {p['name']}'s portfolio website.
Reply in the SAME language the user writes in (Uzbek, English or Russian).
Keep answers short (2-4 sentences).
FACTS:
- Name: {p['name']} (nickname: {p['nickname']})
- Role: {p['role_en']}
- Location: {p['location_en']}
- Bio: {p['bio_en']}
- Email: {p['email']}
- GitHub: {p['github']}
- Skills: {skills}
- Projects: {projects}
- Experience: {exp}
- Status: Open to work"""

def _fallback(msg):
    msg = (msg or "").lower()
    p = sd.PROFILE
    if any(w in msg for w in ["salom","hello","hi","hey","привет"]):
        return f"Hi! 👋 I'm {p['name']}'s AI assistant. Ask me about his skills or projects."
    if any(w in msg for w in ["skill","tech","stack","python","ko'nikma","навык"]):
        top = ", ".join(s[1] for s in sd.SKILLS[:8])
        return f"{p['name']} mainly works with: {top}."
    if any(w in msg for w in ["project","loyiha","work","проект"]):
        names = ", ".join(pr["title_en"] for pr in sd.PROJECTS)
        return f"Main projects: {names}."
    if any(w in msg for w in ["contact","email","bog'lan","phone"]):
        return f"Contact: {p['email']} | GitHub: {p['github']}"
    if any(w in msg for w in ["who","kim","about","кто"]):
        return p["bio_en"]
    return f"Ask me about {p['name']}'s skills, projects, or experience!"

def _gemini(key, messages):
    contents = [
        {"role": "user" if m["role"]=="user" else "model",
         "parts": [{"text": m["content"]}]}
        for m in messages
    ]
    body = json.dumps({
        "system_instruction": {"parts": [{"text": _knowledge()}]},
        "contents": contents,
        "generationConfig": {"temperature": 0.6, "maxOutputTokens": 400}
    }).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",
        data=body, headers={"Content-Type":"application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"].strip()

def _openai(key, messages):
    body = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [{"role":"system","content":_knowledge()}] + messages,
        "temperature": 0.6, "max_tokens": 400
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=body,
        headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"].strip()

@app.route("/api/chat", methods=["POST","OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return "", 204
    data = request.get_json(silent=True) or {}
    msgs = data.get("messages", [])
    if not msgs and data.get("message"):
        msgs = [{"role":"user","content":data["message"]}]
    msgs = [m for m in msgs[-8:] if m.get("role") in ("user","assistant") and m.get("content")]
    last = next((m["content"] for m in reversed(msgs) if m["role"]=="user"), "")

    reply = ""
    gk = os.environ.get("GEMINI_API_KEY","")
    ok = os.environ.get("OPENAI_API_KEY","")
    try:
        if gk:
            reply = _gemini(gk, msgs)
        elif ok:
            reply = _openai(ok, msgs)
    except urllib.error.HTTPError as e:
        print(f"[AI] HTTP {e.code}")
        if e.code in (429, 503) and ok and gk:
            try: reply = _openai(ok, msgs)
            except: pass
    except Exception as ex:
        print(f"[AI] error: {ex}")
    if not reply:
        reply = _fallback(last)
    return jsonify({"reply": reply})

# ---- Contact ----
def _send_email(name, email, message):
    gu = os.environ.get("GMAIL_USER","")
    gp = os.environ.get("GMAIL_PASS","")
    nt = os.environ.get("NOTIFY_EMAIL","")
    if not (gu and gp and nt):
        return
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"📬 Portfolio: {name} dan yangi xabar"
        msg["From"] = gu
        msg["To"]   = nt
        text = f"Yangi xabar!\n\nIsm: {name}\nEmail: {email}\n\nXabar:\n{message}"
        msg.attach(MIMEText(text,"plain","utf-8"))
        with smtplib.SMTP_SSL("smtp.gmail.com",465,timeout=10) as s:
            s.login(gu,gp); s.sendmail(gu,nt,msg.as_string())
    except Exception as ex:
        print(f"[EMAIL] {ex}")

@app.route("/api/contact", methods=["POST","OPTIONS"])
def contact():
    if request.method == "OPTIONS":
        return "", 204
    data = request.get_json(silent=True) or {}
    name    = (data.get("name") or "").strip()
    email   = (data.get("email") or "").strip()
    message = (data.get("message") or "").strip()
    if not name or not message:
        return jsonify({"error": "Ism va xabar majburiy"}), 400
    threading.Thread(target=_send_email, args=(name,email,message), daemon=True).start()
    return jsonify({"ok": True})

@app.route("/api/admin/session", methods=["GET","OPTIONS"])
def admin_session():
    if request.method == "OPTIONS":
        return "", 204
    return jsonify({"authenticated": False})

# Vercel uchun
handler = app
