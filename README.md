# 🐍 LearnWithPython — Learn Python by Actually Writing Python

A full-stack, interactive Python learning platform. Six structured courses,
34 lessons, 10 arena challenges, real Python 3 running **in your browser**
(no installs), XP · levels · streaks · achievements, and a built-in
spaced-repetition study engine.

> Inspired by the best of Codecademy, DataCamp and Anki — free and open source.

## ✨ Features

- **Interactive lessons** — every lesson has a live editor and ends with a
  graded coding challenge, checked instantly against expected output
- **Real Python in the browser** — full CPython via [Pyodide](https://pyodide.org)
  (WebAssembly): stdlib included, zero setup, nothing to install
- **A complete path** — Fundamentals → Data Structures → Functions & OOP →
  Practical Python → **APIs with Python** → Automation, each ending in a
  mini-project (FizzBuzz to a server log analyzer)
- **Challenge Arena** — 10 standalone problems (Easy → Hard) including
  interview classics: palindromes, primes, Caesar cipher, a rate limiter
- **Smart Review** — spaced-repetition flashcards (SM-2 style) generated
  from every quiz on the platform; hard cards return sooner
- **Gamification that works** — XP, 10 levels (Newcomer → Legend), daily
  streaks, 18 achievements, leaderboard
- **Playground** — a free-form Python scratchpad with autosave
- **SEO-ready** — semantic HTML, per-page meta/OG tags, JSON-LD Course
  schema, sitemap.xml, robots.txt
- **Fully responsive** — designed mobile-first; great on phone, tablet and
  desktop; respects `prefers-reduced-motion`

## 🚀 Quick start

```bash
git clone https://github.com/simasbuilds/pysprint.git
cd pysprint
python -m venv .venv && .venv\Scripts\activate   # Windows
# source .venv/bin/activate                       # macOS/Linux
pip install -r requirements.txt
copy .env.example .env                            # then set SECRET_KEY
python app.py
```

Open **http://127.0.0.1:5000** — the SQLite database is created
automatically.

## 🧱 Stack

| Layer | Tech |
|-------|------|
| Backend | Flask 3, SQLite (stdlib `sqlite3`), Werkzeug password hashing |
| Frontend | Server-rendered Jinja, vanilla JS, hand-rolled CSS design system |
| Code execution | Pyodide (client-side WebAssembly CPython) — user code **never** runs on the server |
| Study engine | SM-2-lite spaced repetition in `localStorage` |

## 📁 Project layout

```
app.py                # routes, auth, progress API, sitemap/robots
database.py           # SQLite schema + queries
data/courses.py       # the curriculum (courses → lessons)
data/challenges.py    # arena challenges
data/achievements.py  # achievement definitions
templates/            # 13 Jinja pages
static/css|js/        # design system + runner + review engine
CLAUDE.md             # how the codebase works (for AI pair-programmers & humans)
SKILL.md              # curriculum-authoring playbook (pedagogy rules)
```

## 🔐 Environment

Copy `.env.example` → `.env`:

| Var | Purpose |
|-----|---------|
| `SECRET_KEY` | Flask session signing — generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `SITE_URL` | Canonical URL used in SEO tags & sitemap |
| `DATABASE_PATH` | SQLite file location |
| `FLASK_DEBUG` / `PORT` | Dev server settings |
| `SESSION_COOKIE_SECURE` | Set `1` in production (HTTPS) |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | Enables "Continue with Google" (optional) |
| `SUPABASE_URL` / `SUPABASE_ANON_KEY` / `SUPABASE_SERVICE_ROLE_KEY` | Supabase project keys (optional) |

### 🔵 Enabling Google Sign-In

The "Continue with Google" button is **feature-flagged** — it stays hidden and
the routes redirect to the normal login until you provide credentials, so the
site runs fine without it.

1. `pip install -r requirements.txt` (adds Authlib).
2. In [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   → **Create OAuth client ID** → *Web application*.
3. Add an **Authorized redirect URI**: `{SITE_URL}/auth/google/callback`
   (e.g. `https://learnwithpython.com/auth/google/callback` and
   `http://127.0.0.1:5000/auth/google/callback` for local dev).
4. Put the client ID/secret in `.env` (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`).
5. Restart — the button appears on `/login` and `/register` automatically.

Google users get a passwordless account (schema migrates automatically to add
`google_sub` / `avatar_url` columns; existing password accounts are linked by
email on first Google sign-in).

### 🟢 Supabase (optional data backend)

`.env` carries `SUPABASE_URL` / `SUPABASE_ANON_KEY` / `SUPABASE_SERVICE_ROLE_KEY`
placeholders. Create a project at [supabase.com](https://supabase.com), copy the
keys from **Project Settings → API**, and drop them in. (The default backend is
local SQLite; Supabase wiring is the next milestone.)

## 🧭 Deploying

Any host that runs Python works (Render, Railway, Fly.io, a VPS):

```bash
FLASK_DEBUG=0 SECRET_KEY=<strong> SITE_URL=https://yourdomain gunicorn app:app
```

## 🤝 Contributing content

Read **SKILL.md** first — it encodes the teaching method (code-first,
one concept per lesson, deterministic challenges, explained quizzes).
New lessons are pure data: add a dict to `data/courses.py` and every page,
flashcard and progress bar updates automatically.

## 📄 License

MIT © [simasbuilds](https://github.com/simasbuilds)
