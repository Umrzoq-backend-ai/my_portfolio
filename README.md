# Umrzoq Yulchiyev — Portfolio

> Backend & Data Engineering | Junior Developer | School 21

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Status](https://img.shields.io/badge/Status-Open%20to%20work-brightgreen?style=flat)

## About

Personal portfolio website with AI chatbot, admin panel, and contact form.  
Built with pure Python standard library — no external dependencies required.

**Live:** `http://localhost:8000` (run locally)

---

## Features

- **Dark starfield design** — animated stars with parallax scroll
- **AI Chatbot** — Gemini / OpenAI powered, answers questions about me
- **Admin Panel** — full CRUD for all content (skills, projects, experience, blog)
- **Photo Upload** — upload profile photo from admin panel
- **Contact Form** — messages saved to DB + email notification
- **Bilingual** — UZ / EN language toggle
- **Zero dependencies** — only Python 3 stdlib (sqlite3, http.server, smtplib)

---

## Stack

| Layer | Tech |
|-------|------|
| Backend | Python 3 (`http.server`, `sqlite3`) |
| Database | SQLite |
| Frontend | HTML + CSS + Vanilla JS |
| AI | Google Gemini / OpenAI GPT |
| Auth | HMAC signed cookies |

---

## Quick Start

```bash
git clone https://github.com/Umrzoq-backend-ai/my_portfolio.git
cd my_portfolio

# Create .env file
cp .env.example .env
# Edit .env and add your API keys

# Run
python3 app.py
```

Open in browser:
- **Site:** http://localhost:8000
- **Admin:** http://localhost:8000/admin — `admin / admin123`

---

## Configuration (`.env`)

```env
# AI (pick one or both)
GEMINI_API_KEY=your_gemini_key      # https://aistudio.google.com/apikey
OPENAI_API_KEY=your_openai_key      # https://platform.openai.com

# Email notifications (optional)
NOTIFY_EMAIL=your@gmail.com
GMAIL_USER=your@gmail.com
GMAIL_PASS=your_app_password        # Gmail App Password, not regular password
```

> `.env` is in `.gitignore` — never committed to git.

---

## Project Structure

```
portfolio/
├── app.py          # HTTP server, routing, REST API
├── database.py     # SQLite CRUD, auth, email
├── ai.py           # Gemini / OpenAI / fallback
├── seed_data.py    # Initial data
├── .env            # Secret keys (not in git)
└── web/
    ├── index.html  # Public site
    ├── admin.html  # Admin panel
    ├── css/        # Styles
    ├── js/         # Frontend logic
    └── assets/     # Images
```

---

## Contact

**Umrzoq Yulchiyev** — Backend & Data Engineer  
School 21 (Digital Engineering School), Jizzakh

[![GitHub](https://img.shields.io/badge/GitHub-Umrzoq--backend--ai-black?logo=github)](https://github.com/Umrzoq-backend-ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-umrzoqyulchiyevcode-blue?logo=linkedin)](https://www.linkedin.com/in/umrzoqyulchiyevcode)
