# -*- coding: utf-8 -*-
"""
AI chatbot moduli — faqat standart kutubxona (urllib).

Ishlashi:
  1. Agar GROQ_API_KEY yoki OPENAI_API_KEY muhit o'zgaruvchisi bo'lsa —
     haqiqiy LLM (Groq yoki OpenAI) chaqiriladi.
  2. Kalit bo'lmasa — sodda "fallback" javob (knowledge base asosida).

Groq bepul va tez. Kalit olish: https://console.groq.com
Ishga tushirishdan oldin:
     export GROQ_API_KEY="gsk_..."
"""

import os
import json
import urllib.request
import urllib.error

import database as db


def _build_knowledge():
    """Ma'lumotlar bazasidan bot uchun kontekst yig'adi."""
    p = db.get_profile()
    skills = db.fetch_all("skills", order="category, sort")
    projects = db.fetch_all("projects", order="sort")
    experience = db.fetch_all("experience", order="sort")

    skill_str = ", ".join(f"{s['name']} ({s['level']}%)" for s in skills)
    proj_str = "; ".join(
        f"{pr['title_en']}: {pr['desc_en']}" for pr in projects
    )
    exp_str = "; ".join(
        f"{e['role_en']} @ {e['org']} ({e['date_label_en']})" for e in experience
    )

    return f"""You are the AI assistant on {p.get('name','Umrzoq Yulchiyev')}'s portfolio website.
Answer visitors' questions about him professionally, concisely and friendly.
Reply in the SAME language the user writes in (Uzbek or English or Russian).

FACTS ABOUT HIM:
- Name: {p.get('name')} (nickname: {p.get('nickname')})
- Role: {p.get('role_en')}
- Location: {p.get('location_en')}
- Bio: {p.get('bio_en')}
- Email: {p.get('email')}
- GitHub: {p.get('github')}
- LinkedIn: {p.get('linkedin')}
- Skills: {skill_str}
- Projects: {proj_str}
- Experience: {exp_str}
- Status: {"Open to work" if p.get('available') else "Not currently looking"}

If asked something not covered here, say you don't have that info and suggest contacting him via email.
Keep answers short (2-4 sentences)."""


def _fallback(user_message):
    """Kalit bo'lmaganda oddiy qoidaviy javob."""
    p = db.get_profile()
    msg = (user_message or "").lower()

    def has(*words):
        return any(w in msg for w in words)

    if has("salom", "assalom", "hello", "hi", "hey", "привет"):
        return f"Assalomu alaykum! Men {p.get('name')}ning AI yordamchisiman. Nima bilmoqchisiz? 😊"
    if has("skill", "ko'nikma", "konikma", "texnologi", "stack", "dastur", "til"):
        skills = db.fetch_all("skills", order="category, sort")
        top = ", ".join(s["name"] for s in skills[:8])
        return f"{p.get('name')} asosan quyidagilar bilan ishlaydi: {top}. Batafsil — Skills bo'limida."
    if has("project", "loyiha", "ish", "portfolio"):
        projects = db.fetch_all("projects", order="sort")
        names = ", ".join(pr["title_en"] for pr in projects)
        return f"Asosiy loyihalari: {names}. Projects bo'limida batafsil ko'rishingiz mumkin."
    if has("contact", "bog'lan", "boglan", "email", "aloqa", "telefon"):
        return f"Bog'lanish uchun: {p.get('email')}. GitHub: {p.get('github')}"
    if has("who", "kim", "haqida", "about", "kimsan"):
        return p.get("bio_en") or p.get("bio_uz") or "Backend & Data Engineer."
    if has("work", "ish", "vakansiya", "hire", "job", "yollash"):
        state = "yangi imkoniyatlarga ochiq (Open to work)" if p.get("available") else "hozircha band"
        return f"{p.get('name')} hozirda {state}. Taklif uchun: {p.get('email')}"
    return ("Bu savolga aniq javobim yo'q. Umrzoq haqida ko'proq bilish uchun "
            f"savolingizni boshqacharoq bering yoki {p.get('email')} orqali bog'laning.")


def _call_groq(api_key, messages):
    system = _build_knowledge()
    payload = {
        "model": os.environ.get("AI_MODEL", "llama-3.3-70b-versatile"),
        "messages": [{"role": "system", "content": system}] + messages,
        "temperature": 0.6,
        "max_tokens": 500,
    }
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip()


def _call_openai(api_key, messages):
    system = _build_knowledge()
    payload = {
        "model": os.environ.get("AI_MODEL", "gpt-4o-mini"),
        "messages": [{"role": "system", "content": system}] + messages,
        "temperature": 0.6,
        "max_tokens": 500,
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip()


def _call_gemini(api_key, messages):
    """Google Gemini API (gemini-2.0-flash)"""
    system = _build_knowledge()

    # Gemini formatiga o'tkazish
    contents = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": m["content"]}]})

    payload = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": contents,
        "generationConfig": {
            "temperature": 0.6,
            "maxOutputTokens": 500,
        },
    }
    model = os.environ.get("AI_MODEL", "gemini-2.0-flash")
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def chat(messages):
    """
    messages: [{"role":"user"/"assistant", "content": "..."}]
    Javob (str) qaytaradi.
    """
    if not messages:
        return "Savolingizni yozing 🙂"

    last_user = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user = m.get("content", "")
            break

    groq_key    = os.environ.get("GROQ_API_KEY")
    openai_key  = os.environ.get("OPENAI_API_KEY")
    gemini_key  = os.environ.get("GEMINI_API_KEY")

    try:
        if gemini_key:
            return _call_gemini(gemini_key, messages)
        if openai_key:
            return _call_openai(openai_key, messages)
        if groq_key:
            return _call_groq(groq_key, messages)
    except urllib.error.HTTPError as e:
        try:
            err = e.read().decode("utf-8")
        except Exception:
            err = str(e)
        print("[AI] HTTP xato:", e.code, err[:200])
        # 429 yoki limit bo'lsa — keyingi API ga o'tish
        if e.code in (429, 503):
            try:
                if gemini_key and openai_key:
                    return _call_openai(openai_key, messages)
                if groq_key:
                    return _call_groq(groq_key, messages)
            except Exception as e2:
                print("[AI] Zaxira API ham xato:", e2)
    except Exception as e:
        print("[AI] xato:", e)

    # Kalit yo'q yoki xato bo'lsa
    return _fallback(last_user)
