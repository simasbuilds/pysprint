# CLAUDE.md — LearnwithPython

Guidance for Claude Code (and any developer) working in this repository.

## What this is

**LearnwithPython** is a full-stack interactive Python learning platform
(repo/folder still named `pysprint`, and the DB file is still `pysprint.db`):
Flask + SQLite backend, Jinja server-rendered multi-page frontend, and real
Python 3 running **in the browser** via Pyodide (WebAssembly). Learners take
courses, pass graded coding challenges, take quizzes, earn XP/streaks/
achievements, and retain knowledge with a built-in spaced-repetition
flashcard engine.

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env        # then edit SECRET_KEY
python app.py               # http://127.0.0.1:5000
```

The SQLite database (`pysprint.db`) is created automatically on first start.
No migrations, no seed step.

## Architecture

```
app.py               Flask app: all routes, auth, progress API, SEO routes
database.py          SQLite layer (stdlib sqlite3, no ORM). Schema lives here.
data/
  icons.py           ICONS: the whole SVG icon set (name -> path markup)
  courses.py         THE CURRICULUM. 6 courses × lessons (content/example/
                     challenge/quiz). This is where 90% of edits happen.
  lesson_extras.py   Per-lesson deep-dive callouts (real_world / pitfalls /
                     pro_tip), keyed by (course_slug, lesson_slug)
  challenges.py      Standalone arena challenges (10)
  achievements.py    Achievement defs; each has a `check(stats)` lambda
templates/           Jinja pages, all extend base.html
  _brand.html        brand_mark() macro — the inline SVG logo (nav + footer)
  _icons.html        sprite() renders the <symbol> set once; icon(name) uses it
  _art.html          art(slug, color) — the per-course/project artwork
static/css/style.css Whole design system, CSS custom properties, dark theme
static/img/
  favicon.svg        Standalone copy of the logo mark
static/js/
  main.js            Nav (incl. mobile menu), toasts, achievement modal queue
  runner.js          Pyodide loader + code execution + challenge grading +
                     lesson/challenge/playground page initialisers
  palette.js         ⌘K command palette (fed by /api/search-index)
  review.js          Spaced-repetition engine (SM-2-lite, localStorage)
```

## Key design decisions (don't accidentally undo these)

1. **Challenge grading happens client-side.** User code runs in Pyodide;
   stdout is normalized (trailing whitespace stripped per line) and compared
   to `expected_output`. The server never executes user code — that's the
   security model. The `/api/complete-*` endpoints only record completion.
2. **Fresh Pyodide globals per run** (`runner.js`) so state can't leak
   between runs and confuse learners.
3. **Progress requires login; learning doesn't.** All lessons are public
   (good for SEO); XP/streaks/achievements need a session.
4. **XP is only granted on first completion** (`INSERT OR IGNORE` + rowcount
   check) — re-running a lesson can't farm XP.
5. **Achievements are computed, not event-sourced**: after any completion,
   `award_new_achievements()` recomputes stats and grants anything newly
   matched. Adding a new achievement is just appending to
   `data/achievements.py`.
6. **No frontend build step.** Vanilla JS + CSS, CDN only for fonts and
   Pyodide. Keep it that way — it's a feature.
7. **The logo is inline SVG, not an emoji or an image file.** It lives in
   `templates/_brand.html` as a macro so the nav and footer share one
   source; `uid` keeps its gradient ids unique per instance. Inline is what
   lets it animate on hover and stay crisp in both themes. `favicon.svg`
   is a hand-kept copy — change one, change the other.
8. **The ⌘K palette index is a public endpoint** (`/api/search-index`),
   cached for 10 minutes and again in `sessionStorage`. It carries titles
   and URLs only, never lesson bodies, so it stays small and needs no auth.
   New courses, lessons, projects and challenges appear in it automatically.
9. **Pyodide is pre-warmed on idle** on any page with an editor, so the
   first Run is instant. Skipped on save-data/2g. Editor bars get a status
   chip fed by the `pysprint:engine` event.
10. **No emoji anywhere in the UI.** Every glyph is an SVG from
   `data/icons.py`, rendered once per page as a `<symbol>` sprite and
   referenced with `<use>` — so JS (`window.psIcon(name, size)`) and Jinja
   (`ic.icon(name, size)`) draw from one set. Data files store icon *names*
   (`"icon": "terminal"`), never glyphs. Courses and projects additionally
   get bespoke artwork from `_art.html`, keyed by slug and tinted with the
   subject's `color`. Adding a course means adding an `art()` branch.
11. **The home page is a product surface, not a brochure.** `next_lesson_for()`
   in `app.py` finds the first uncompleted lesson in curriculum order, and
   the hero renders one of three states: resume (returning learner, leads
   with their next lesson), finished (whole curriculum done), or marketing
   (first visit). The hero editor is a *graded* first task — it checks the
   learner actually edited the name before showing the success panel — so
   time-to-first-real-Python is about ten seconds with no signup.
12. **Light theme is the default**; dark mode via `data-theme="dark"` on
   `<html>`, toggled in the nav and persisted in localStorage. All colors
   come from CSS custom properties in `:root` / `[data-theme="dark"]` —
   never hardcode a color in a component rule. Code editors deliberately
   stay dark in both themes.

## Adding content

**New lesson:** append a dict to a course's `lessons` list in
`data/courses.py`. Required keys: `slug`, `title`, `minutes`, `xp`,
`content` (HTML fragment), `example`, `challenge`
(`prompt/starter/expected_output/hint/solution`), `quiz` (list of
`q/options/answer/explain`). Everything else (nav, sitemap, review
flashcards, progress %, course XP totals) updates automatically.

**Challenge rules:** `expected_output` must be deterministic — no
randomness without a seed, no timing, no dict-ordering assumptions (dicts
preserve insertion order, that's fine). Test the solution actually produces
`expected_output` exactly. Avoid `input()` — it doesn't work in Pyodide.

**New course:** append to `COURSES` with `slug/title/tagline/level/color/
icon/description/lessons`, and add a matching completion achievement in
`data/achievements.py`.

## Conventions

- Python: stdlib-first, no ORM, 4-space indent, f-strings.
- Lesson `content` is trusted HTML written by us (rendered with `|safe`) —
  never put user input through it.
- CSS: use existing custom properties (`--surface`, `--accent`…); the
  per-course accent color flows via `style="--accent: …"`.
- SEO: every template overrides `title` and `description` blocks; new pages
  should be added to the `sitemap()` route in `app.py`.

## Testing quickly

```bash
python -c "import app"                        # imports + data validation
python - <<'EOF'                              # verify challenge solutions
from data.courses import COURSES
import io, contextlib
for c in COURSES:
    for l in c["lessons"]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(l["challenge"]["solution"], {})
        got = "\n".join(x.rstrip() for x in buf.getvalue().rstrip().splitlines())
        want = l["challenge"]["expected_output"]
        assert got == want, f"{c['slug']}/{l['slug']}:\n{got!r}\n!=\n{want!r}"
print("all lesson solutions verified")
EOF
```

Run the same pattern over `data/challenges.py` when editing the arena.

## Deployment notes

- Set a real `SECRET_KEY` and `SITE_URL` in the environment.
- `gunicorn app:app` behind any reverse proxy; SQLite is fine for this
  write volume. `DATABASE_PATH` moves the DB file (e.g. a mounted volume).
- `FLASK_DEBUG=0` in production.
