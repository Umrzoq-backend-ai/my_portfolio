"""POST /api/chat — AI chatbot (Gemini / OpenAI fallback)"""
import json, os, sys, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import seed_data as sd

# ---- Knowledge base ----
def _knowledge():
    p = sd.PROFILE
    skills = ", ".join(f"{s[1]} ({s[2]}%)" for s in sd.SKILLS)
    projects = "; ".join(f"{pr['title_en']}: {pr['desc_en']}" for pr in sd.PROJECTS)
    exp = "; ".join(f"{e['role_en']} @ {e['org']}" for e in sd.EXPERIENCE)
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
    if any(w in msg for w in ["salom","hello","hi","hey"]):
        return f"Hi! 👋 I'm {p['name']}'s AI assistant. Ask me about his skills or projects."
    if any(w in msg for w in ["skill","tech","stack","python","language"]):
        top = ", ".join(s[1] for s in sd.SKILLS[:8])
        return f"{p['name']} mainly works with: {top}."
    if any(w in msg for w in ["project","loyiha"]):
        names = ", ".join(pr["title_en"] for pr in sd.PROJECTS)
        return f"Main projects: {names}. Check the Projects section for details."
    if any(w in msg for w in ["contact","email","bog'lan"]):
        return f"Contact: {p['email']} | GitHub: {p['github']}"
    return f"Ask me about {p['name']}'s skills, projects or experience!"

def _gemini(key, messages):
    contents = []
    for m in messages:
        contents.append({"role": "user" if m["role"]=="user" else "model",
                         "parts": [{"text": m["content"]}]})
    payload = json.dumps({
        "system_instruction": {"parts": [{"text": _knowledge()}]},
        "contents": contents,
        "generationConfig": {"temperature": 0.6, "maxOutputTokens": 400}
    }).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",
        data=payload, headers={"Content-Type":"application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"].strip()

def _openai(key, messages):
    payload = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [{"role":"system","content":_knowledge()}] + messages,
        "temperature": 0.6, "max_tokens": 400
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"].strip()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        body = json.loads(self.rfile.read(length).decode()) if length else {}
        msgs = body.get("messages", [])
        if not msgs and body.get("message"):
            msgs = [{"role":"user","content":body["message"]}]
        msgs = [m for m in msgs[-8:] if m.get("role") in ("user","assistant") and m.get("content")]
        last = next((m["content"] for m in reversed(msgs) if m["role"]=="user"), "")

        reply = ""
        gemini_key = os.environ.get("GEMINI_API_KEY","")
        openai_key  = os.environ.get("OPENAI_API_KEY","")
        try:
            if gemini_key:
                reply = _gemini(gemini_key, msgs)
            elif openai_key:
                reply = _openai(openai_key, msgs)
        except urllib.error.HTTPError as e:
            if e.code == 429 and openai_key:
                try: reply = _openai(openai_key, msgs)
                except: pass
        except Exception: pass
        if not reply:
            reply = _fallback(last)

        resp = json.dumps({"reply": reply}, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp)))
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(resp)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()

    def log_message(self, *a): pass
