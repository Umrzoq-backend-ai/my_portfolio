# -*- coding: utf-8 -*-
"""
Boshlang'ich (seed) ma'lumotlar — Umrzoq Yulchiyev portfolio uchun.
Ma'lumotlar bazasi birinchi marta yaratilganda shu ma'lumotlar yoziladi.
Keyinchalik hammasini ADMIN PANEL orqali tahrirlash mumkin.
"""

# --- Profil (bitta yozuv) ---
PROFILE = {
    "name": "Umrzoq Yulchiyev",
    "nickname": "umrzoq_dev",
    "role_uz": "Backend & Data Engineer",
    "role_en": "Backend & Data Engineer",
    "tagline_uz": "Backend va Data Engineering yo'nalishida junior developer",
    "tagline_en": "Junior developer focused on Backend & Data Engineering",
    "headline_uz": "Salom, men Umrzoq — mahsulotlar quraman va yetkazaman",
    "headline_en": "Hi, I'm Umrzoq — I Build & Ship Products",
    "bio_uz": (
        "Men Umrzoq Yulchiyevman — Jizzax viloyatidanman va hozirda School 21 "
        "(Digital Engineering School) da Data Engineering yo'nalishida o'qiyman. "
        "Backend va ma'lumotlar muhandisligiga ixtisoslashganman. Kwork platformasida "
        "frilanser sifatida real loyihalar ustida ishlaganman. Toza kod, aniq arxitektura "
        "va ishonchli tizimlar qurishni yaxshi ko'raman."
    ),
    "bio_en": (
        "I'm Umrzoq Yulchiyev from Jizzakh region, currently studying Data Engineering at "
        "School 21 (Digital Engineering School). I specialize in backend and data engineering. "
        "I've worked as a freelancer on Kwork on real projects. I love clean code, clear "
        "architecture, and building reliable systems."
    ),
    "location_uz": "Jizzax, O'zbekiston",
    "location_en": "Jizzakh, Uzbekistan",
    "email": "umrzoq.dev@gmail.com",
    "phone": "+998 00 000 00 00",
    "github": "https://github.com/Umrzoq-backend-ai",
    "linkedin": "https://www.linkedin.com/in/umrzoqyulchiyevcode",
    "telegram": "https://t.me/",
    "resume_url": "",
    "avatar": "",
    "available": 1,
}

# --- Ko'nikmalar (kategoriya, nom, daraja %, tartib) ---
SKILLS = [
    ("Backend", "Python", 85, 1),
    ("Backend", "FastAPI / Django", 72, 2),
    ("Backend", "PostgreSQL", 76, 3),
    ("Backend", "REST API", 78, 4),
    ("Backend", "Node.js", 55, 5),
    ("Data Engineering", "SQL", 82, 1),
    ("Data Engineering", "Pandas / NumPy", 72, 2),
    ("Data Engineering", "ETL Pipelines", 60, 3),
    ("Data Engineering", "Data Modeling", 65, 4),
    ("Tools & DevOps", "Git / GitHub", 88, 1),
    ("Tools & DevOps", "Docker", 62, 2),
    ("Tools & DevOps", "Linux / Terminal", 80, 3),
    ("Tools & DevOps", "VS Code", 92, 4),
    ("Frontend", "HTML / CSS", 75, 1),
    ("Frontend", "JavaScript", 68, 2),
    ("Frontend", "React (basics)", 45, 3),
]

# --- Loyihalar ---
PROJECTS = [
    {
        "title_uz": "REST API Backend",
        "title_en": "REST API Backend",
        "desc_uz": "FastAPI va PostgreSQL asosida qurilgan, autentifikatsiya va CRUD "
                   "imkoniyatlariga ega backend xizmat.",
        "desc_en": "A backend service built with FastAPI and PostgreSQL, featuring "
                   "authentication and full CRUD.",
        "tags": "Python,FastAPI,PostgreSQL,Docker",
        "github": "https://github.com/Umrzoq-backend-ai",
        "demo": "",
        "featured": 1,
        "sort": 1,
    },
    {
        "title_uz": "Data Pipeline (ETL)",
        "title_en": "Data Pipeline (ETL)",
        "desc_uz": "Turli manbalardan ma'lumot yig'ib, tozalab, tahlilga tayyorlaydigan ETL quvuri.",
        "desc_en": "An ETL pipeline that collects data from multiple sources, cleans it, "
                   "and prepares it for analysis.",
        "tags": "Python,Pandas,SQL",
        "github": "https://github.com/Umrzoq-backend-ai",
        "demo": "",
        "featured": 1,
        "sort": 2,
    },
    {
        "title_uz": "Telegram Bot",
        "title_en": "Telegram Bot",
        "desc_uz": "Ma'lumotlar bazasiga ulangan, foydalanuvchilar bilan ishlaydigan "
                   "avtomatlashtirilgan Telegram bot.",
        "desc_en": "An automated Telegram bot connected to a database that interacts with users.",
        "tags": "Python,aiogram,PostgreSQL",
        "github": "https://github.com/Umrzoq-backend-ai",
        "demo": "",
        "featured": 0,
        "sort": 3,
    },
]

# --- Sertifikatlar ---
CERTIFICATES = [
    {
        "title": "School 21 — Data Engineering",
        "issuer": "School 21 (Digital Engineering School)",
        "date": "2024",
        "url": "",
        "sort": 1,
    },
    {
        "title": "Python Backend Development",
        "issuer": "Online Course",
        "date": "2023",
        "url": "",
        "sort": 2,
    },
]

# --- Tajriba / ta'lim (timeline) ---
EXPERIENCE = [
    {
        "date_label_uz": "2024 - Hozir",
        "date_label_en": "2024 - Present",
        "role_uz": "Talaba — Data Engineering",
        "role_en": "Student — Data Engineering",
        "org": "School 21 (Digital Engineering School)",
        "points_uz": "Peer-to-peer o'qish metodikasi;Algoritmlar va tizimli dasturlash",
        "points_en": "Peer-to-peer learning methodology;Algorithms & systems programming",
        "sort": 1,
    },
    {
        "date_label_uz": "2023 - Hozir",
        "date_label_en": "2023 - Present",
        "role_uz": "Frilanser Developer",
        "role_en": "Freelance Developer",
        "org": "Kwork",
        "points_uz": "Mijozlar uchun backend yechimlar;Botlar va avtomatlashtirish",
        "points_en": "Backend solutions for clients;Bots & automation",
        "sort": 2,
    },
]

# --- Blog postlari ---
BLOG = [
    {
        "title_uz": "Backend'ni noldan o'rganish",
        "title_en": "Learning Backend from Scratch",
        "slug": "backend-from-scratch",
        "excerpt_uz": "Python bilan backend dasturlashni qanday boshlaganim haqida.",
        "excerpt_en": "How I started backend development with Python.",
        "body_uz": "Bu yerda backend yo'nalishida o'rganish tajribam, foydalangan resurslarim "
                   "va maslahatlarim haqida yozaman...",
        "body_en": "Here I share my experience learning backend development, the resources "
                   "I used, and my advice...",
        "published": 1,
        "sort": 1,
    },
]
