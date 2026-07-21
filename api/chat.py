from http.server import BaseHTTPRequestHandler
import json, os, sys, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import seed_data as sd

def _knowledge():
    p = sd.PROFILE
    skills   = ", ".join(f"{s[1]} ({s[2]}%)" for s in sd.SKILLS)
    projects = "; ".join(f"{pr['title_en']}: {pr['desc_en']}" for pr in sd.PROJECTS)
    exp      = "; ".join(f"{e['role_en']} @ {e['org']}" for e in sd.EXPERIENCE)
    return f"""You are the AI assistant on {p['name']}'s portfolio website.
IMPORTANT: Always reply in the SAME language the user writes in.
- If user writes in Uzbek → reply in Uzbek
- If user writes in Russian → reply in Russian
- If user writes in English → reply in English
Keep answers short (2-4 sentences).
FACTS:
- Name: {p['name']} (umrzoq_dev)
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
    uz = any(w in msg for w in ["salom","qanday","umrzoq","haqida","loyiha","ko'nikma","uzbcha","o'zbek","uzbek"])
    ru = any(w in msg for w in ["привет","как","навык","проект","умрзок"])
    if any(w in msg for w in ["salom","привет","hello","hi"]):
        if uz: return f"Salom! 👋 Men Umrzoq Yulchiyevning AI yordamchisiman. Ko'nikmalar, loyihalar haqida so'rang."
        if ru: return f"Привет! 👋 Я AI-ассистент Умрзока Юлчиева. Спрашивайте о навыках и проектах."
        return f"Hi! 👋 I'm Umrzoq's AI assistant. Ask about skills or projects."
    if any(w in msg for w in ["skill","tech","ko'nikma","навык","stack"]):
        top = ", ".join(s[1] for s in sd.SKILLS[:8])
        if uz: return f"Asosiy texnologiyalar: {top}."
        if ru: return f"Основные технологии: {top}."
        return f"Main skills: {top}."
    if any(w in msg for w in ["project","loyiha","проект"]):
        names = ", ".join(pr["title_en"] for pr in sd.PROJECTS)
        if uz: return f"Loyihalar: {names}."
        return f"Projects: {names}."
    if uz: return f"Umrzoq haqida savolingizni bering — ko'nikmalar, loyihalar yoki tajriba."
    if ru: return f"Задайте вопрос об Умрзоке — навыки, проекты или опыт."
    return f"Ask me about {p['name']}'s skills, projects, or experience!"

def _gemini(key, messages):
    contents = [{"role":"user" if m["role"]=="user" else "model","parts":[{"text":m["content"]}]} for m in messages]
    body = json.dumps({"system_instruction":{"parts":[{"text":_knowledge()}]},"contents":contents,"generationConfig":{"temperature":0.6,"maxOutputTokens":400}}).encode()
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",data=body,headers={"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=25) as r:
        return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"].strip()

def _openai(key, messages):
    body = json.dumps({"model":"gpt-4o-mini","messages":[{"role":"system","content":_knowledge()}]+messages,"temperature":0.6,"max_tokens":400}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions",data=body,headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=25) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"].strip()

class handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
    def _json(self, data, status=200):
        b = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(b)))
        self._cors(); self.end_headers(); self.wfile.write(b)
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_POST(self):
        length = int(self.headers.get("Content-Length",0) or 0)
        body = json.loads(self.rfile.read(length).decode()) if length else {}
        msgs = body.get("messages",[])
        if not msgs and body.get("message"):
            msgs = [{"role":"user","content":body["message"]}]
        msgs = [m for m in msgs[-8:] if m.get("role") in ("user","assistant") and m.get("content")]
        last = next((m["content"] for m in reversed(msgs) if m["role"]=="user"),"")
        gk = os.environ.get("GEMINI_API_KEY","")
        ok = os.environ.get("OPENAI_API_KEY","")
        print(f"[CHAT] gemini_key={'YES' if gk else 'NO'} openai_key={'YES' if ok else 'NO'}")
        reply = ""
        try:
            if gk: reply = _gemini(gk, msgs)
            elif ok: reply = _openai(ok, msgs)
        except urllib.error.HTTPError as e:
            print(f"[AI] HTTP {e.code}")
            try:
                err = e.read().decode()
                print(f"[AI] err: {err[:200]}")
            except: pass
            if e.code in (429,503) and ok:
                try: reply = _openai(ok, msgs)
                except: pass
        except Exception as ex:
            print(f"[AI] error: {ex}")
        if not reply: reply = _fallback(last)
        self._json({"reply": reply})
    def log_message(self,*a): pass
