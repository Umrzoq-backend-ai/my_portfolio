# -*- coding: utf-8 -*-
"""Seed ma'lumotlar — Umrzoq Yulchiyev portfolio (CV asosida yangilangan)"""

PROFILE = {
    "name": "Umrzoq Yulchiyev",
    "nickname": "umrzoq_dev",
    "role_uz": "Data Scientist | Backend Developer",
    "role_en": "Data Scientist | Backend Developer",
    "tagline_uz": "Backend va Data Science | School 21",
    "tagline_en": "Backend & Data Science Developer | School 21",
    "headline_uz": "Salom, men Umrzoq — mahsulotlar quraman va yetkazaman",
    "headline_en": "Hi, I'm Umrzoq — I Build & Ship Products",
    "bio_uz": (
        "Men Umrzoq Yulchiyevman — Samarqandda yashayman, hozirda School 21 "
        "da Data Science yo'nalishida o'qiyman. Python, FastAPI, Django, "
        "PostgreSQL, ML va Data Engineering bilan ishlayman."
    ),
    "bio_en": (
        "I'm Umrzoq Yulchiyev from Samarkand, Uzbekistan. Currently studying Data Science "
        "at School 21. I specialize in backend development and data engineering using "
        "Python, FastAPI, Django, PostgreSQL, and ML. I love clean code and reliable systems."
    ),
    "location_uz": "Samarqand, O'zbekiston",
    "location_en": "Samarkand, Uzbekistan",
    "email": "school21dev@gmail.com",
    "phone": "+998 91 593 30 18",
    "github": "https://github.com/Umrzoq-backend-ai",
    "linkedin": "https://www.linkedin.com/in/umrzoqyulchiyevcode",
    "telegram": "https://t.me/",
    "resume_url": "/assets/resume.pdf",
    "avatar": "/assets/photo.jpg",
    "available": 1,
}

SKILLS = [
    ("Backend",       "Python",           90, 1),
    ("Backend",       "FastAPI",          78, 2),
    ("Backend",       "Django",           75, 3),
    ("Backend",       "PostgreSQL",       80, 4),
    ("Backend",       "MySQL",            72, 5),
    ("Backend",       "REST API",         85, 6),
    ("Backend",       "JWT Auth",         70, 7),
    ("Data Science",  "Pandas",           80, 1),
    ("Data Science",  "NumPy",            78, 2),
    ("Data Science",  "Jupyter Notebook", 82, 3),
    ("Data Science",  "Big Data",         65, 4),
    ("Data Science",  "Deep Learning",    60, 5),
    ("Data Science",  "Machine Learning", 65, 6),
    ("Tools & DevOps","Git / GitHub",     88, 1),
    ("Tools & DevOps","Docker",           65, 2),
    ("Tools & DevOps","Linux",            80, 3),
    ("Tools & DevOps","MongoDB",          68, 4),
    ("Tools & DevOps","PyCharm",          85, 5),
]

PROJECTS = [
    {
        "title_uz": "REST API Backend",
        "title_en": "REST API Backend",
        "desc_uz": "FastAPI va PostgreSQL asosida qurilgan, JWT autentifikatsiya va CRUD imkoniyatlariga ega backend xizmat.",
        "desc_en": "A backend service built with FastAPI and PostgreSQL, featuring JWT authentication and full CRUD.",
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
        "desc_en": "An ETL pipeline that collects, cleans, and prepares data from multiple sources for analysis.",
        "tags": "Python,Pandas,NumPy,SQL",
        "github": "https://github.com/Umrzoq-backend-ai",
        "demo": "",
        "featured": 1,
        "sort": 2,
    },
    {
        "title_uz": "Telegram Bot",
        "title_en": "Telegram Bot",
        "desc_uz": "PostgreSQL bazasiga ulangan, foydalanuvchilar bilan ishlaydigan avtomatlashtirilgan Telegram bot.",
        "desc_en": "An automated Telegram bot connected to PostgreSQL that interacts with users.",
        "tags": "Python,aiogram,PostgreSQL",
        "github": "https://github.com/Umrzoq-backend-ai",
        "demo": "",
        "featured": 0,
        "sort": 3,
    },
]

CERTIFICATES = [
    {
        "title": "School 21 — Data Science",
        "issuer": "School 21 (Digital Engineering School)",
        "date": "2026",
        "url": "",
        "sort": 1,
    },
    {
        "title": "Python Backend Development",
        "issuer": "Online Course",
        "date": "2024",
        "url": "",
        "sort": 2,
    },
]

EXPERIENCE = [
    {
        "date_label_uz": "2025 Iyul - Hozir",
        "date_label_en": "Jul 2025 - Present",
        "role_uz": "Data Science | Backend Developer",
        "role_en": "Data Science | Backend Developer",
        "org": "School 21 (Digital Engineering School)",
        "points_uz": (
            "Python, Django va FastAPI orqali backend API'lar yaratish;"
            "PostgreSQL/MySQL bazalarini loyihalash va optimallashtirish;"
            "Pandas va NumPy yordamida ma'lumotlarni qayta ishlash va tahlil;"
            "ML modellarini yaratish (bashorat va tavsiya tizimlari);"
            "JWT va session autentifikatsiya integratsiyasi;"
            "Docker va Linux serverlarda deploy qilish"
        ),
        "points_en": (
            "Developed backend APIs using Python, Django, and FastAPI;"
            "Designed and optimized PostgreSQL/MySQL databases;"
            "Data preprocessing and analysis using Pandas and NumPy;"
            "Developed ML models for prediction and recommendation systems;"
            "Integrated JWT and session-based authentication;"
            "Deployed services on Linux servers with Docker"
        ),
        "sort": 1,
    },
]

BLOG = [
    {
        "title_uz": "Backend'ni noldan o'rganish",
        "title_en": "Learning Backend from Scratch",
        "slug": "backend-from-scratch",
        "excerpt_uz": "Python bilan backend dasturlashni qanday boshlaganim haqida.",
        "excerpt_en": "How I started backend development with Python.",
        "body_uz": "Backend yo'nalishida o'rganish tajribam va maslahatlarim...",
        "body_en": "My experience learning backend development and advice for beginners...",
        "published": 1,
        "sort": 1,
    },
]
