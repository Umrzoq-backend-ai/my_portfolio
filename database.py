# -*- coding: utf-8 -*-
"""
Ma'lumotlar bazasi qatlami (SQLite, faqat standart kutubxona).
Jadvallarni yaratadi, boshlang'ich ma'lumotni yozadi va CRUD funksiyalar beradi.
"""

import sqlite3
import os
import hashlib
import hmac
import secrets

import seed_data

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portfolio.db")

# Standart admin ma'lumotlari (BIRINCHI ISHGA TUSHIRISHDA yaratiladi).
# !!! Kirgandan keyin admin paneldan parolni ALBATTA o'zgartiring !!!
DEFAULT_ADMIN_USER = "admin"
DEFAULT_ADMIN_PASS = "admin123"


# ---------------------------------------------------------------------------
# Ulanish
# ---------------------------------------------------------------------------
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ---------------------------------------------------------------------------
# Parol xeshlash (pbkdf2, standart kutubxona)
# ---------------------------------------------------------------------------
def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200_000)
    return salt, dk.hex()


def verify_password(password, salt, expected_hash):
    _, actual = hash_password(password, salt)
    return hmac.compare_digest(actual, expected_hash)


# ---------------------------------------------------------------------------
# Sxema
# ---------------------------------------------------------------------------
SCHEMA = """
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    salt TEXT NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    name TEXT, nickname TEXT,
    role_uz TEXT, role_en TEXT,
    tagline_uz TEXT, tagline_en TEXT,
    headline_uz TEXT, headline_en TEXT,
    bio_uz TEXT, bio_en TEXT,
    location_uz TEXT, location_en TEXT,
    email TEXT, phone TEXT,
    github TEXT, linkedin TEXT, telegram TEXT, instagram TEXT,
    resume_url TEXT, avatar TEXT,
    available INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    level INTEGER NOT NULL,
    sort INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title_uz TEXT, title_en TEXT,
    desc_uz TEXT, desc_en TEXT,
    tags TEXT, github TEXT, demo TEXT,
    featured INTEGER DEFAULT 0,
    sort INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT, issuer TEXT, date TEXT, url TEXT,
    image TEXT DEFAULT '',
    sort INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS experience (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_label_uz TEXT, date_label_en TEXT,
    role_uz TEXT, role_en TEXT, org TEXT,
    points_uz TEXT, points_en TEXT,
    sort INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS blog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title_uz TEXT, title_en TEXT, slug TEXT,
    excerpt_uz TEXT, excerpt_en TEXT,
    body_uz TEXT, body_en TEXT,
    image TEXT DEFAULT '',
    telegram_msg_id TEXT DEFAULT '',
    published INTEGER DEFAULT 1,
    sort INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT, email TEXT, message TEXT,
    is_read INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);
"""


# ---------------------------------------------------------------------------
# Init + seed
# ---------------------------------------------------------------------------
def init_db():
    conn = get_conn()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
        _seed_if_empty(conn)
    finally:
        conn.close()


def _seed_if_empty(conn):
    # Admin
    if conn.execute("SELECT COUNT(*) c FROM admin").fetchone()["c"] == 0:
        salt, ph = hash_password(DEFAULT_ADMIN_PASS)
        conn.execute(
            "INSERT INTO admin (username, salt, password_hash) VALUES (?,?,?)",
            (DEFAULT_ADMIN_USER, salt, ph),
        )

    # Profile
    if conn.execute("SELECT COUNT(*) c FROM profile").fetchone()["c"] == 0:
        p = seed_data.PROFILE
        cols = ",".join(p.keys())
        qs = ",".join(["?"] * len(p))
        conn.execute(f"INSERT INTO profile (id,{cols}) VALUES (1,{qs})", list(p.values()))

    if conn.execute("SELECT COUNT(*) c FROM skills").fetchone()["c"] == 0:
        conn.executemany(
            "INSERT INTO skills (category,name,level,sort) VALUES (?,?,?,?)",
            seed_data.SKILLS,
        )

    if conn.execute("SELECT COUNT(*) c FROM projects").fetchone()["c"] == 0:
        for pr in seed_data.PROJECTS:
            _insert_dict(conn, "projects", pr)

    if conn.execute("SELECT COUNT(*) c FROM certificates").fetchone()["c"] == 0:
        for c in seed_data.CERTIFICATES:
            _insert_dict(conn, "certificates", c)

    if conn.execute("SELECT COUNT(*) c FROM experience").fetchone()["c"] == 0:
        for e in seed_data.EXPERIENCE:
            _insert_dict(conn, "experience", e)

    if conn.execute("SELECT COUNT(*) c FROM blog").fetchone()["c"] == 0:
        for b in seed_data.BLOG:
            _insert_dict(conn, "blog", b)

    conn.commit()


def _insert_dict(conn, table, d):
    cols = ",".join(d.keys())
    qs = ",".join(["?"] * len(d))
    conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({qs})", list(d.values()))


# ---------------------------------------------------------------------------
# Umumiy yordamchilar
# ---------------------------------------------------------------------------
def rows_to_dicts(rows):
    return [dict(r) for r in rows]


def fetch_all(table, order="id"):
    conn = get_conn()
    try:
        rows = conn.execute(f"SELECT * FROM {table} ORDER BY {order}").fetchall()
        return rows_to_dicts(rows)
    finally:
        conn.close()


def fetch_one(table, row_id):
    conn = get_conn()
    try:
        r = conn.execute(f"SELECT * FROM {table} WHERE id=?", (row_id,)).fetchone()
        return dict(r) if r else None
    finally:
        conn.close()


# Har bir jadval uchun ruxsat etilgan ustunlar (xavfsizlik: faqat shular yoziladi)
ALLOWED_FIELDS = {
    "projects": ["title_uz", "title_en", "desc_uz", "desc_en", "tags", "github",
                 "demo", "featured", "sort"],
    "skills": ["category", "name", "level", "sort"],
    "certificates": ["title", "issuer", "date", "url", "image", "sort"],
    "experience": ["date_label_uz", "date_label_en", "role_uz", "role_en", "org",
                   "points_uz", "points_en", "sort"],
    "blog": ["title_uz", "title_en", "slug", "excerpt_uz", "excerpt_en",
             "body_uz", "body_en", "image", "telegram_msg_id", "published", "sort"],
    "profile": ["name", "nickname", "role_uz", "role_en", "tagline_uz", "tagline_en",
                "headline_uz", "headline_en", "bio_uz", "bio_en", "location_uz",
                "location_en", "email", "phone", "github", "linkedin", "telegram",
                "instagram", "resume_url", "avatar", "available"],
}


def _clean(table, data):
    allowed = ALLOWED_FIELDS[table]
    return {k: data[k] for k in allowed if k in data}


def create(table, data):
    data = _clean(table, data)
    if not data:
        return None
    conn = get_conn()
    try:
        cols = ",".join(data.keys())
        qs = ",".join(["?"] * len(data))
        cur = conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({qs})", list(data.values()))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def update(table, row_id, data):
    data = _clean(table, data)
    if not data:
        return False
    conn = get_conn()
    try:
        sets = ",".join([f"{k}=?" for k in data.keys()])
        conn.execute(f"UPDATE {table} SET {sets} WHERE id=?", list(data.values()) + [row_id])
        conn.commit()
        return True
    finally:
        conn.close()


def delete(table, row_id):
    conn = get_conn()
    try:
        conn.execute(f"DELETE FROM {table} WHERE id=?", (row_id,))
        conn.commit()
        return True
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Profil
# ---------------------------------------------------------------------------
def get_profile():
    conn = get_conn()
    try:
        r = conn.execute("SELECT * FROM profile WHERE id=1").fetchone()
        return dict(r) if r else {}
    finally:
        conn.close()


def update_profile(data):
    data = _clean("profile", data)
    if not data:
        return False
    conn = get_conn()
    try:
        sets = ",".join([f"{k}=?" for k in data.keys()])
        conn.execute(f"UPDATE profile SET {sets} WHERE id=1", list(data.values()))
        conn.commit()
        return True
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Xabarlar (contact form)
# ---------------------------------------------------------------------------
def add_message(name, email, message):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO messages (name,email,message) VALUES (?,?,?)",
            (name, email, message),
        )
        conn.commit()
    finally:
        conn.close()
    # Email bildirishnoma yuborish (fon thread'da)
    _send_notify_email(name, email, message)


def _send_notify_email(name, sender_email, message):
    """Kimdir forma to'ldirganda admin emailiga xabar yuboradi"""
    import os, smtplib, threading
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    gmail_user = os.environ.get("GMAIL_USER", "")
    gmail_pass = os.environ.get("GMAIL_PASS", "")
    notify_to  = os.environ.get("NOTIFY_EMAIL", "")

    if not (gmail_user and gmail_pass and notify_to):
        return  # Email sozlanmagan

    def send():
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"📬 Portfolio: {name} dan yangi xabar"
            msg["From"]    = gmail_user
            msg["To"]      = notify_to

            text = (
                f"Yangi xabar keldi!\n\n"
                f"Ism:     {name}\n"
                f"Email:   {sender_email or 'ko`rsatilmagan'}\n"
                f"Xabar:\n{message}\n\n"
                f"Admin panel: http://localhost:8000/admin"
            )
            html = f"""
<div style="font-family:sans-serif;max-width:520px;padding:24px;background:#0d0e18;color:#e8eaf2;border-radius:12px">
  <h2 style="color:#00ffaa;margin-bottom:16px">📬 Yangi xabar</h2>
  <table style="width:100%;border-collapse:collapse">
    <tr><td style="padding:8px 0;color:#8b90a8;width:80px">Ism</td><td style="padding:8px 0"><strong>{name}</strong></td></tr>
    <tr><td style="padding:8px 0;color:#8b90a8">Email</td><td style="padding:8px 0">{sender_email or "ko'rsatilmagan"}</td></tr>
  </table>
  <div style="margin-top:16px;padding:16px;background:#1a1b2e;border-radius:8px;border-left:3px solid #00ffaa">
    <p style="margin:0;line-height:1.6">{message.replace(chr(10), "<br>")}</p>
  </div>
  <p style="margin-top:16px;font-size:13px;color:#656b82">
    <a href="http://localhost:8000/admin" style="color:#818cf8">Admin panelda ko'rish →</a>
  </p>
</div>"""

            msg.attach(MIMEText(text, "plain", "utf-8"))
            msg.attach(MIMEText(html, "html", "utf-8"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
                smtp.login(gmail_user, gmail_pass)
                smtp.sendmail(gmail_user, notify_to, msg.as_string())
            print(f"[EMAIL] Xabar yuborildi: {notify_to}")
        except smtplib.SMTPAuthenticationError:
            print("[EMAIL] Auth xato! Gmail App Password kerak (oddiy parol ishlamaydi).")
            print("[EMAIL] https://myaccount.google.com/apppasswords")
        except Exception as e:
            print(f"[EMAIL] Xato: {e}")

    # Fon thread'da yuborish — server kutib qolmasin
    threading.Thread(target=send, daemon=True).start()


def mark_message_read(msg_id):
    conn = get_conn()
    try:
        conn.execute("UPDATE messages SET is_read=1 WHERE id=?", (msg_id,))
        conn.commit()
    finally:
        conn.close()


def delete_message(msg_id):
    conn = get_conn()
    try:
        conn.execute("DELETE FROM messages WHERE id=?", (msg_id,))
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Admin auth
# ---------------------------------------------------------------------------
def get_admin(username):
    conn = get_conn()
    try:
        r = conn.execute("SELECT * FROM admin WHERE username=?", (username,)).fetchone()
        return dict(r) if r else None
    finally:
        conn.close()


def check_admin(username, password):
    admin = get_admin(username)
    if not admin:
        return False
    return verify_password(password, admin["salt"], admin["password_hash"])


def change_admin_password(username, new_password):
    salt, ph = hash_password(new_password)
    conn = get_conn()
    try:
        conn.execute(
            "UPDATE admin SET salt=?, password_hash=? WHERE username=?",
            (salt, ph, username),
        )
        conn.commit()
        return True
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
    print("Ma'lumotlar bazasi tayyor:", DB_PATH)
