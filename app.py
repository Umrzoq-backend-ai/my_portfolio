#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Portfolio backend — Umrzoq Yulchiyev.
Faqat Python standart kutubxonasi (tashqi paket kerak emas).

Ishga tushirish:
    python3 app.py
Keyin brauzerda oching:
    Sayt:        http://localhost:8000
    Admin panel: http://localhost:8000/admin   (login: admin / admin123)

AI chatbot uchun (ixtiyoriy) kalit qo'shing:
    export GROQ_API_KEY="gsk_..."   # https://console.groq.com (bepul)
    python3 app.py
"""

import os
import json
import base64
import hmac
import hashlib

# .env fayldan kalitlarni yuklaymiz (agar mavjud bo'lsa)
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))
import time
import mimetypes
import posixpath
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from http.cookies import SimpleCookie
from urllib.parse import urlparse

import database as db
import ai

# --- Sozlamalar ---
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Render.com uchun: agar __file__ yo'li noto'g'ri bo'lsa cwd ishlatamiz
if not os.path.exists(os.path.join(BASE_DIR, "web")):
    BASE_DIR = os.getcwd()
WEB_DIR = os.path.join(BASE_DIR, "web")
SESSION_HOURS = 12
COOKIE_NAME = "pf_session"

# CRUD uchun ruxsat etilgan jadvallar (admin API)
CRUD_TABLES = {"projects", "skills", "certificates", "experience", "blog"}


# ---------------------------------------------------------------------------
# Maxfiy kalit (cookie imzolash uchun) — faylga saqlanadi
# ---------------------------------------------------------------------------
def _load_secret():
    env = os.environ.get("SECRET_KEY")
    if env:
        return env.encode("utf-8")
    path = os.path.join(BASE_DIR, ".secret_key")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    key = os.urandom(32)
    with open(path, "wb") as f:
        f.write(key)
    try:
        os.chmod(path, 0o600)
    except Exception:
        pass
    return key


SECRET = _load_secret()


# ---------------------------------------------------------------------------
# Sessiya (imzolangan token)
# ---------------------------------------------------------------------------
def _b64e(b):
    return base64.urlsafe_b64encode(b).decode("ascii").rstrip("=")


def _b64d(s):
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


def make_token(username):
    exp = int(time.time()) + SESSION_HOURS * 3600
    payload = json.dumps({"u": username, "exp": exp}).encode("utf-8")
    p = _b64e(payload)
    sig = _b64e(hmac.new(SECRET, p.encode("ascii"), hashlib.sha256).digest())
    return f"{p}.{sig}"


def verify_token(token):
    try:
        p, sig = token.split(".", 1)
        expected = _b64e(hmac.new(SECRET, p.encode("ascii"), hashlib.sha256).digest())
        if not hmac.compare_digest(sig, expected):
            return None
        data = json.loads(_b64d(p))
        if int(data["exp"]) < int(time.time()):
            return None
        return data["u"]
    except Exception:
        return None


# ---------------------------------------------------------------------------
# HTTP Handler
# ---------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "PortfolioServer/1.0"

    # --- Loglarni sokinroq qilish ---
    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

    # ================= Yordamchilar =================
    def _send_json(self, obj, status=200, extra_headers=None):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        """JSON body'ni o'qi — Content-Length va chunked encoding'ni qo'llab-quvvatlaydi"""
        # Content-Length tekshirish (case-insensitive)
        cl_val = None
        for key in self.headers:
            if key.lower() == "content-length":
                cl_val = self.headers[key]
                break

        try:
            length = int(cl_val or 0)
        except (ValueError, TypeError):
            length = 0

        # Transfer-Encoding: chunked tekshirish
        te = ""
        for key in self.headers:
            if key.lower() == "transfer-encoding":
                te = self.headers[key].lower()
                break

        if length > 0:
            raw = self.rfile.read(length)
        elif "chunked" in te:
            # Chunked encoding decode
            chunks = []
            while True:
                line = self.rfile.readline().decode("ascii", errors="ignore").strip()
                if not line:
                    break
                try:
                    chunk_size = int(line, 16)
                except ValueError:
                    break
                if chunk_size == 0:
                    break
                chunk = self.rfile.read(chunk_size)
                chunks.append(chunk)
                self.rfile.read(2)  # \r\n
            raw = b"".join(chunks)
        else:
            return {}

        if not raw:
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}
        if not raw:
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}

    def _current_user(self):
        cookie = SimpleCookie(self.headers.get("Cookie", ""))
        if COOKIE_NAME in cookie:
            return verify_token(cookie[COOKIE_NAME].value)
        return None

    def _require_auth(self):
        user = self._current_user()
        if not user:
            self._send_json({"error": "unauthorized"}, 401)
            return None
        return user

    # ================= Static fayllar =================
    def _serve_static(self, url_path):
        # index / admin
        if url_path == "/" or url_path == "":
            url_path = "/index.html"
        elif url_path == "/admin" or url_path == "/admin/":
            url_path = "/admin.html"

        # xavfsiz yo'l (directory traversaldan himoya)
        clean = posixpath.normpath(url_path).lstrip("/")
        file_path = os.path.join(WEB_DIR, clean)
        if not os.path.abspath(file_path).startswith(os.path.abspath(WEB_DIR)):
            self._send_json({"error": "forbidden"}, 403)
            return
        if not os.path.isfile(file_path):
            self.send_error(404, "Not Found")
            return

        ctype, _ = mimetypes.guess_type(file_path)
        ctype = ctype or "application/octet-stream"
        try:
            with open(file_path, "rb") as f:
                data = f.read()
        except OSError:
            self.send_error(404, "Not Found")
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # ================= GET =================
    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/portfolio":
            return self._api_portfolio()
        if path == "/api/admin/session":
            return self._send_json({"authenticated": bool(self._current_user())})
        if path.startswith("/api/admin/"):
            return self._admin_get(path)
        if path.startswith("/api/"):
            return self._send_json({"error": "not found"}, 404)

        return self._serve_static(path)

    # ================= POST =================
    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/contact":
            return self._api_contact()
        if path == "/api/chat":
            return self._api_chat()
        if path == "/api/admin/login":
            return self._api_login()
        if path == "/api/admin/logout":
            return self._api_logout()
        if path == "/api/admin/password":
            return self._api_change_password()
        if path == "/api/admin/upload":
            return self._api_upload()
        if path == "/api/admin/blog-upload":
            return self._api_blog_upload()
        if path == "/api/admin/cert-upload":
            return self._api_cert_upload()
        if path == "/api/telegram-webhook":
            return self._api_telegram_webhook()
        if path.startswith("/api/admin/"):
            return self._admin_post(path)
        return self._send_json({"error": "not found"}, 404)

    # ================= PUT =================
    def do_PUT(self):
        path = urlparse(self.path).path
        if path.startswith("/api/admin/"):
            return self._admin_put(path)
        return self._send_json({"error": "not found"}, 404)

    # ================= DELETE =================
    def do_DELETE(self):
        path = urlparse(self.path).path
        if path.startswith("/api/admin/"):
            return self._admin_delete(path)
        return self._send_json({"error": "not found"}, 404)

    # ================= PUBLIC API =================
    def _api_portfolio(self):
        profile = db.get_profile()
        profile.pop("id", None)
        skills = db.fetch_all("skills", order="category, sort, id")
        projects = db.fetch_all("projects", order="sort, id")
        certificates = db.fetch_all("certificates", order="sort, id")
        experience = db.fetch_all("experience", order="sort, id")
        blog = [b for b in db.fetch_all("blog", order="sort, id") if b.get("published")]
        self._send_json({
            "profile": profile,
            "skills": skills,
            "projects": projects,
            "certificates": certificates,
            "experience": experience,
            "blog": blog,
        })

    def _api_contact(self):
        data = self._read_json()
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        message = (data.get("message") or "").strip()
        if not name or not message:
            return self._send_json({"error": "Ism va xabar majburiy"}, 400)
        if len(message) > 5000:
            return self._send_json({"error": "Xabar juda uzun"}, 400)
        db.add_message(name, email, message)
        self._send_json({"ok": True})

    def _api_chat(self):
        data = self._read_json()
        messages = data.get("messages")
        if not messages and data.get("message"):
            messages = [{"role": "user", "content": data["message"]}]
        if not isinstance(messages, list):
            return self._send_json({"error": "messages kerak"}, 400)
        # faqat kerakli maydonlar, oxirgi 10 ta xabar
        clean = []
        for m in messages[-10:]:
            role = m.get("role")
            content = (m.get("content") or "")[:2000]
            if role in ("user", "assistant") and content:
                clean.append({"role": role, "content": content})
        reply = ai.chat(clean)
        self._send_json({"reply": reply})

    # ================= AUTH API =================
    def _api_login(self):
        data = self._read_json()
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""
        if not db.check_admin(username, password):
            return self._send_json({"error": "Login yoki parol xato"}, 401)
        token = make_token(username)
        cookie = (
            f"{COOKIE_NAME}={token}; HttpOnly; Path=/; SameSite=Lax; "
            f"Max-Age={SESSION_HOURS * 3600}"
        )
        self._send_json({"ok": True}, extra_headers={"Set-Cookie": cookie})

    def _api_logout(self):
        cookie = f"{COOKIE_NAME}=; HttpOnly; Path=/; Max-Age=0"
        self._send_json({"ok": True}, extra_headers={"Set-Cookie": cookie})

    def _api_change_password(self):
        user = self._require_auth()
        if not user:
            return
        data = self._read_json()
        new = data.get("new_password") or ""
        if len(new) < 6:
            return self._send_json({"error": "Parol kamida 6 belgi"}, 400)
        db.change_admin_password(user, new)
        self._send_json({"ok": True})

    def _api_upload(self):
        """Rasm yuklash — multipart/form-data"""
        if not self._require_auth():
            return
        ctype = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in ctype:
            return self._send_json({"error": "multipart kerak"}, 400)

        # boundary topish
        boundary = None
        for part in ctype.split(";"):
            part = part.strip()
            if part.startswith("boundary="):
                boundary = part[9:].strip().encode("utf-8")
                break
        if not boundary:
            return self._send_json({"error": "boundary yo'q"}, 400)

        length = int(self.headers.get("Content-Length", 0) or 0)
        if length > 10 * 1024 * 1024:  # 10 MB limit
            return self._send_json({"error": "Rasm 10MB dan kichik bo'lishi kerak"}, 413)

        body = self.rfile.read(length)

        # Multipart bo'laklarini ajratish
        delimiter = b"--" + boundary
        parts = body.split(delimiter)
        for part in parts:
            if b"Content-Disposition" not in part:
                continue
            if b'name="photo"' not in part:
                continue
            # Header va mazmunni ajratish
            sep = b"\r\n\r\n"
            idx = part.find(sep)
            if idx == -1:
                continue
            header_raw = part[:idx].decode("utf-8", errors="ignore")
            content = part[idx + 4:]
            # Oxirgi \r\n ni olib tashlash
            if content.endswith(b"\r\n"):
                content = content[:-2]

            # Kengaytma aniqlash
            ext = ".jpg"
            if "filename=" in header_raw:
                fn_part = [x for x in header_raw.split(";") if "filename=" in x]
                if fn_part:
                    fname = fn_part[0].strip().split("=", 1)[1].strip().strip('"')
                    _, e = os.path.splitext(fname)
                    if e.lower() in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
                        ext = e.lower()

            # Saqlash
            assets_dir = os.path.join(WEB_DIR, "assets")
            os.makedirs(assets_dir, exist_ok=True)
            save_path = os.path.join(assets_dir, "photo" + ext)
            with open(save_path, "wb") as f:
                f.write(content)

            # Profilni yangilash
            url = "/assets/photo" + ext
            db.update_profile({"avatar": url})
            return self._send_json({"ok": True, "url": url})

        self._send_json({"error": "photo maydoni topilmadi"}, 400)

    def _api_blog_upload(self):
        """Blog uchun rasm yuklash — /api/admin/blog-upload"""
        if not self._require_auth():
            return
        ctype = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in ctype:
            return self._send_json({"error": "multipart kerak"}, 400)

        boundary = None
        for part in ctype.split(";"):
            part = part.strip()
            if part.startswith("boundary="):
                boundary = part[9:].strip().encode("utf-8")
                break
        if not boundary:
            return self._send_json({"error": "boundary yo'q"}, 400)

        length = int(self.headers.get("Content-Length", 0) or 0)
        if length > 20 * 1024 * 1024:
            return self._send_json({"error": "Rasm 20MB dan kichik bo'lishi kerak"}, 413)

        body = self.rfile.read(length)
        delimiter = b"--" + boundary
        for part in body.split(delimiter):
            if b"Content-Disposition" not in part:
                continue
            if b'name="image"' not in part:
                continue
            sep = b"\r\n\r\n"
            idx = part.find(sep)
            if idx == -1:
                continue
            header_raw = part[:idx].decode("utf-8", errors="ignore")
            content = part[idx + 4:]
            if content.endswith(b"\r\n"):
                content = content[:-2]

            ext = ".jpg"
            if "filename=" in header_raw:
                fn_parts = [x for x in header_raw.split(";") if "filename=" in x]
                if fn_parts:
                    fname = fn_parts[0].strip().split("=", 1)[1].strip().strip('"')
                    _, e = os.path.splitext(fname)
                    if e.lower() in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
                        ext = e.lower()

            import time as _time
            filename = f"blog_{int(_time.time())}{ext}"
            blog_dir = os.path.join(WEB_DIR, "assets", "blog")
            os.makedirs(blog_dir, exist_ok=True)
            save_path = os.path.join(blog_dir, filename)
            with open(save_path, "wb") as f:
                f.write(content)

            url = f"/assets/blog/{filename}"
            return self._send_json({"ok": True, "url": url})

        self._send_json({"error": "image maydoni topilmadi"}, 400)

    def _api_cert_upload(self):
        """Sertifikat uchun rasm yuklash"""
        if not self._require_auth():
            return
        ctype = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in ctype:
            return self._send_json({"error": "multipart kerak"}, 400)
        boundary = None
        for part in ctype.split(";"):
            part = part.strip()
            if part.startswith("boundary="):
                boundary = part[9:].strip().encode("utf-8")
                break
        if not boundary:
            return self._send_json({"error": "boundary yo'q"}, 400)
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length > 20 * 1024 * 1024:
            return self._send_json({"error": "Rasm 20MB dan kichik bo'lishi kerak"}, 413)
        body = self.rfile.read(length)
        for part in body.split(b"--" + boundary):
            if b"Content-Disposition" not in part:
                continue
            if b'name="image"' not in part:
                continue
            sep = b"\r\n\r\n"
            idx = part.find(sep)
            if idx == -1:
                continue
            header_raw = part[:idx].decode("utf-8", errors="ignore")
            content = part[idx + 4:]
            if content.endswith(b"\r\n"):
                content = content[:-2]
            ext = ".jpg"
            if "filename=" in header_raw:
                fn_parts = [x for x in header_raw.split(";") if "filename=" in x]
                if fn_parts:
                    fname = fn_parts[0].strip().split("=", 1)[1].strip().strip('"')
                    _, e = os.path.splitext(fname)
                    if e.lower() in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
                        ext = e.lower()
            import time as _t
            filename = f"cert_{int(_t.time())}{ext}"
            cert_dir = os.path.join(WEB_DIR, "assets", "certs")
            os.makedirs(cert_dir, exist_ok=True)
            with open(os.path.join(cert_dir, filename), "wb") as f:
                f.write(content)
            url = f"/assets/certs/{filename}"
            return self._send_json({"ok": True, "url": url})
        self._send_json({"error": "image maydoni topilmadi"}, 400)
        """Telegram bot webhook — kanal postlarini blogga avtomatik qo'shish"""
        # Telegram webhook secret tekshirish
        tg_secret = os.environ.get("TELEGRAM_WEBHOOK_SECRET", "")
        req_secret = self.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if tg_secret and req_secret != tg_secret:
            return self._send_json({"error": "forbidden"}, 403)

        data = self._read_json()
        # Channel post
        msg = data.get("channel_post") or data.get("message")
        if not msg:
            return self._send_json({"ok": True})

        msg_id = str(msg.get("message_id", ""))
        text = msg.get("text") or msg.get("caption") or ""
        date = msg.get("date", 0)
        photo = msg.get("photo")

        if not text and not photo:
            return self._send_json({"ok": True})

        # Sarlavha — birinchi qator
        lines = text.strip().split("\n")
        title = lines[0][:100] if lines else "Yangi post"
        excerpt = lines[1][:200] if len(lines) > 1 else text[:200]
        body = text

        # Telegram post URL
        tg_channel = os.environ.get("TELEGRAM_CHANNEL", "Umrzoq_dev")
        tg_link = f"https://t.me/{tg_channel}/{msg_id}"

        # Bir xil telegram_msg_id bo'lsa qo'shma
        existing = db.fetch_all("blog", order="id")
        for b in existing:
            if b.get("telegram_msg_id") == msg_id:
                return self._send_json({"ok": True, "status": "duplicate"})

        import datetime as _dt
        db.create("blog", {
            "title_uz": title, "title_en": title,
            "slug": f"tg-{msg_id}",
            "excerpt_uz": excerpt, "excerpt_en": excerpt,
            "body_uz": body + f"\n\n[Telegram'da ko'rish]({tg_link})",
            "body_en": body + f"\n\n[View on Telegram]({tg_link})",
            "image": "",
            "telegram_msg_id": msg_id,
            "published": 1,
            "sort": 0,
        })
        print(f"[TELEGRAM] Yangi blog post: {title[:40]}")
        self._send_json({"ok": True, "status": "created"})

    # ================= ADMIN CRUD =================
    def _admin_get(self, path):
        if not self._require_auth():
            return
        parts = path.strip("/").split("/")  # ['api','admin', <res>, <id?>]
        res = parts[2] if len(parts) > 2 else ""
        if res == "profile":
            return self._send_json(db.get_profile())
        if res == "messages":
            return self._send_json(db.fetch_all("messages", order="created_at DESC, id DESC"))
        if res in CRUD_TABLES:
            return self._send_json(db.fetch_all(res, order="sort, id"))
        self._send_json({"error": "not found"}, 404)

    def _admin_post(self, path):
        if not self._require_auth():
            return
        parts = path.strip("/").split("/")
        res = parts[2] if len(parts) > 2 else ""
        # /api/admin/messages/read
        if res == "messages" and len(parts) > 3 and parts[3] == "read":
            data = self._read_json()
            db.mark_message_read(data.get("id"))
            return self._send_json({"ok": True})
        if res in CRUD_TABLES:
            data = self._read_json()
            new_id = db.create(res, data)
            return self._send_json({"ok": True, "id": new_id})
        self._send_json({"error": "not found"}, 404)

    def _admin_put(self, path):
        if not self._require_auth():
            return
        parts = path.strip("/").split("/")
        res = parts[2] if len(parts) > 2 else ""
        if res == "profile":
            db.update_profile(self._read_json())
            return self._send_json({"ok": True})
        if res in CRUD_TABLES and len(parts) > 3:
            try:
                row_id = int(parts[3])
            except ValueError:
                return self._send_json({"error": "bad id"}, 400)
            db.update(res, row_id, self._read_json())
            return self._send_json({"ok": True})
        self._send_json({"error": "not found"}, 404)

    def _admin_delete(self, path):
        if not self._require_auth():
            return
        parts = path.strip("/").split("/")
        res = parts[2] if len(parts) > 2 else ""
        if len(parts) > 3:
            try:
                row_id = int(parts[3])
            except ValueError:
                return self._send_json({"error": "bad id"}, 400)
            if res in CRUD_TABLES:
                db.delete(res, row_id)
                return self._send_json({"ok": True})
            if res == "messages":
                db.delete_message(row_id)
                return self._send_json({"ok": True})
        self._send_json({"error": "not found"}, 404)


def main():
    db.init_db()
    # Papkalarni tekshirish (debug)
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"WEB_DIR: {WEB_DIR}")
    print(f"WEB_DIR exists: {os.path.exists(WEB_DIR)}")
    print(f"index.html exists: {os.path.exists(os.path.join(WEB_DIR, 'index.html'))}")
    # Port band bo'lsa SO_REUSEADDR bilan hal qilish
    import socket
    ThreadingHTTPServer.allow_reuse_address = True
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ai_keys = []
    if os.environ.get("GEMINI_API_KEY"): ai_keys.append("Gemini")
    if os.environ.get("OPENAI_API_KEY"): ai_keys.append("OpenAI")
    if os.environ.get("GROQ_API_KEY"):   ai_keys.append("Groq")
    ai_status = " → ".join(ai_keys) if ai_keys else "Fallback (kalitsiz)"
    print("=" * 56)
    print("  Umrzoq Yulchiyev — Portfolio Server")
    print("=" * 56)
    print(f"  Sayt:        http://localhost:{PORT}")
    print(f"  Admin panel: http://localhost:{PORT}/admin")
    print(f"  Login:       admin / admin123  (parolni o'zgartiring!)")
    print(f"  AI rejimi:   {ai_status}")
    print("=" * 56)
    print("  To'xtatish uchun: Ctrl+C")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer to'xtatildi.")
        server.shutdown()


if __name__ == "__main__":
    main()
