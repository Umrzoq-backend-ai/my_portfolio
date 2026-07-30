"""
POST /api/telegram-webhook
Telegram bot webhook — kanal postlarini blogga avtomatik qo'shadi.
Botni kanalga admin qilib qo'shing, u har yangi postni saytga yuboradi.
"""
from http.server import BaseHTTPRequestHandler
import json, os, sys, sqlite3, time, hashlib, secrets

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "portfolio.db")

# Vercel'da /tmp papkasi yozish mumkin
TMP_DB = "/tmp/portfolio_blog.json"


def _load_blog():
    """Vercel'da SQLite yo'q — /tmp da JSON saqlaymiz"""
    try:
        if os.path.exists(TMP_DB):
            with open(TMP_DB) as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _save_blog(posts):
    try:
        with open(TMP_DB, "w") as f:
            json.dump(posts, f, ensure_ascii=False)
    except Exception as e:
        print(f"[TG] save error: {e}")


def _get_existing_ids():
    posts = _load_blog()
    return {str(p.get("telegram_msg_id","")) for p in posts}


def _add_post(msg_id, title, excerpt, body, image_url, date_str):
    posts = _load_blog()
    post = {
        "id": int(time.time()),
        "title_uz": title, "title_en": title,
        "slug": f"tg-{msg_id}",
        "excerpt_uz": excerpt, "excerpt_en": excerpt,
        "body_uz": body, "body_en": body,
        "image": image_url,
        "telegram_msg_id": str(msg_id),
        "published": 1,
        "sort": 0,
        "created_at": date_str,
    }
    posts.insert(0, post)
    _save_blog(posts)
    return post


class handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type,X-Telegram-Bot-Api-Secret-Token")

    def _json(self, data, status=200):
        b = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self._cors()
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        # Blog postlarini qaytarish (Vercel /tmp dan)
        posts = _load_blog()
        self._json(posts)

    def do_POST(self):
        # Webhook secret tekshirish
        secret = os.environ.get("TELEGRAM_WEBHOOK_SECRET", "")
        req_secret = self.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if secret and req_secret != secret:
            print(f"[TG] Wrong secret: {req_secret!r} != {secret!r}")
            return self._json({"error": "forbidden"}, 403)

        length = int(self.headers.get("Content-Length", 0) or 0)
        if not length:
            return self._json({"ok": True})

        try:
            data = json.loads(self.rfile.read(length).decode())
        except Exception:
            return self._json({"ok": True})

        print(f"[TG] Update: {json.dumps(data)[:200]}")

        # channel_post yoki message
        msg = data.get("channel_post") or data.get("message")
        if not msg:
            return self._json({"ok": True})

        msg_id = str(msg.get("message_id", ""))
        text = msg.get("text") or msg.get("caption") or ""
        date_ts = msg.get("date", int(time.time()))
        import datetime as _dt
        date_str = _dt.datetime.utcfromtimestamp(date_ts).strftime("%Y-%m-%d %H:%M:%S")
        photo = msg.get("photo")  # list of photo sizes

        if not text and not photo:
            return self._json({"ok": True})

        # Duplicate check
        if msg_id in _get_existing_ids():
            return self._json({"ok": True, "status": "duplicate"})

        # Sarlavha va matn
        lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
        title = lines[0][:120] if lines else f"Post #{msg_id}"
        excerpt = lines[1][:300] if len(lines) > 1 else text[:300]
        tg_ch = os.environ.get("TELEGRAM_CHANNEL", "Umrzoq_dev")
        tg_link = f"https://t.me/{tg_ch}/{msg_id}"
        body = text + f"\n\n🔗 [Telegram'da ko'rish]({tg_link})"

        # Rasm URL — Telegram file_id orqali
        image_url = ""
        if photo:
            # Eng katta rasmni ol
            biggest = max(photo, key=lambda x: x.get("file_size", 0))
            file_id = biggest.get("file_id", "")
            bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
            if file_id and bot_token:
                try:
                    import urllib.request
                    r = urllib.request.urlopen(
                        f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}",
                        timeout=10
                    )
                    fd = json.loads(r.read())
                    file_path = fd.get("result", {}).get("file_path", "")
                    if file_path:
                        image_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
                except Exception as e:
                    print(f"[TG] photo error: {e}")

        post = _add_post(msg_id, title, excerpt, body, image_url, date_str)
        print(f"[TG] Yangi post qo'shildi: {title[:50]}")
        self._json({"ok": True, "status": "created", "title": title})

    def log_message(self, *a):
        pass
