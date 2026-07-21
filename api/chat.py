"""POST /api/chat — AI chatbot — Vercel serverless"""
import json, os, sys, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import seed_data as sd

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
    if any(w in msg for w in ["skill","tech","stack","python","language","ko'nikma"]):
        top = ", ".join(s[1] for s in sd.SKILLS[:8])
        return f"{p['name']} mainly works with: {top}."
    if any(w in msg for w in ["project","loyiha","work"]):
        names = ", ".join(pr["title_en"] for pr in sd.PROJECTS)
        return f"Main projects: {names}. Check the Projects section for details."
    if any(w in msg for w in ["contact","email","bog'lan","phone"]):
        return f"Contact: {p['email']} | GitHub: {p['github']}"
    if any(w in msg for w in ["who","kim","haqida","about"]):
        return p['bio_en']
    return f"Ask me about {p['name']}'s skills, projects, or experience!"

def _gemini(key, messages):
    contents = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})
    payload = json.dumps({
        "system_instruction": {"parts": [{"text": _knowledge()}]},
        "contents": contents,
        "generationConfig": {"temperature": 0.6, "maxOutputTokens": 400}
    }).encode()
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",
        data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"].strip()

def _openai(key, messages):
    payload = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [{"role": "system", "content": _knowledge()}] + messages,
        "temperature": 0.6, "max_tokens": 400
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"].strip()

def handler(request, response):
    # CORS
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Content-Type"] = "application/json; charset=utf-8"

    if request.method == "OPTIONS":
        response.status_code = 204
        return response

    if request.method != "POST":
        response.status_code = 405
        response.body = json.dumps({"error": "Method not allowed"})
        return response

    try:
        body = json.loads(request.body or "{}")
    except Exception:
        body = {}

    msgs = body.get("messages", [])
    if not msgs and body.get("message"):
        msgs = [{"role": "user", "content": body["message"]}]
    msgs = [m for m in msgs[-8:] if m.get("role") in ("user", "assistant") and m.get("content")]
    last = next((m["content"] for m in reversed(msgs) if m["role"] == "user"), "")

    reply = ""
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    openai_key  = os.environ.get("OPENAI_API_KEY", "")

    try:
        if gemini_key:
            reply = _gemini(gemini_key, msgs)
        elif openai_key:
            reply = _openai(openai_key, msgs)
    except urllib.error.HTTPError as e:
        err_body = ""
        try: err_body = e.read().decode()
        except: pass
        print(f"[AI] HTTP {e.code}: {err_body[:200]}")
        if e.code in (429, 503) and openai_key and gemini_key:
            try: reply = _openai(openai_key, msgs)
            except: pass
    except Exception as e:
        print(f"[AI] error: {e}")

    if not reply:
        reply = _fallback(last)

    response.status_code = 200
    response.body = json.dumps({"reply": reply}, ensure_ascii=False)
    return response
