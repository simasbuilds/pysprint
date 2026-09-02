# CLAUDE.md — LearnWithPython

Guidance for Claude Code (and any developer) working in this repository.

## What this is

**LearnWithPython** is a full-stack interactive Python learning platform:
Flask + Postgres (Supabase) backend, Jinja server-rendered multi-page
frontend, and real
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

Requires a Supabase project: set `DATABASE_URL` plus the three `SUPABASE_*`
keys. Schema changes are Supabase migrations, not created at app boot.
There is no local SQLite fallback — identity lives in Supabase's hosted
`auth.users`, which has no offline equivalent.

## Architecture

```
app.py               Flask app: all routes, auth, progress API, SEO routes
database.py          Postgres layer (psycopg, no ORM). Profiles + progress.
supabase_auth.py     GoTrue REST client: sign-up/in/out, OAuth, admin.
data/
  courses.py         THE CURRICULUM. 10 courses × lessons (content/example/
                     challenge/quiz). This is where 90% of edits happen.
  lesson_extras.py   Per-lesson deep-dive callouts (real_world / pitfalls /
                     pro_tip), keyed by (course_slug, lesson_slug)
  challenges.py      Standalone arena challenges (10)
  achievements.py    Achievement defs; each has a `check(stats)` lambda
templates/           Jinja pages, all extend base.html
static/css/style.css Whole design system, CSS custom properties, dark theme
static/js/
  main.js            Nav, toasts, achievement modal queue
  runner.js          Pyodide loader + code execution + challenge grading +
                     lesson/challenge/playground page initialisers
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
7. **Light theme is the default**; dark mode via `data-theme="dark"` on
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

## Content today

10 courses / 55 lessons, 9 projects (36 graded steps), 18 arena challenges.
Counts are never hardcoded in copy — `inject_globals` exposes `n_lessons`,
`n_courses`, `n_projects`, `n_project_steps` and `n_challenges`, and
`user_stats` exposes `total_projects` / `total_challenges` so achievements
scale with the data.

Every `expected_output` is produced by executing the paired `solution` and
capturing stdout, so the two cannot drift. Re-run the verification snippet
below over lessons, `data/challenges.py` and every step in
`data/projects.py` after touching content.

## Generated artwork

`static/images/*.png` feature art is generated (Recraft via Higgsfield) and
then colour-matched in post to the navy the hand-made pieces already use,
`#07152f` — the model will not hit an exact background, and mismatched
navies read as sloppy when two panels sit near each other. The recipe:
composite a flat navy over the image through a mask built from luminance
(`255 - v*6`), which repaints the dark field and leaves tiles and glow
edges untouched. `mesh-bg.jpg` is blurred and damped before use so white
text stays readable on top of it.

## /cheatsheet

A browsable reference: 92 snippets across 13 categories, filterable by
category and free text together. Each entry's `out` in `data/cheatsheet.py`
was produced by executing its `code`, so the page cannot display a result
the snippet does not actually produce — re-run the verification loop after
editing it. "Try it" hands the snippet to the playground via `?code=`,
which `initPlayground` applies after the saved draft is restored and then
strips from the URL, so a refresh does not silently overwrite what the
learner has since typed.

## Artwork on coloured panels

Generated art has a flat navy field. Laying it over a gradient panel at
partial opacity lightens that rectangle and leaves a visible seam — which
is what the login page looked like. Composite it with `mix-blend-mode:
screen` plus a radial `mask-image` instead: screen drops near-black to
nothing so only the lit tiles show, and the mask stops anything ending on
a straight edge.

## /start

Onboarding for someone who has never written code. The rest of the site
assumes you know what a lesson or a challenge is; `/start` assumes nothing.
It carries a graded first-line editor that checks the learner actually
edited the code before congratulating them, and names the four study
methods the product is built on (active recall, prediction, spaced
repetition, project-based). It is the first entry in the Learn menu and a
top-level nav item, because the visitor with the least context needs the
clearest door.

## Authentication (Supabase Auth)

Identity lives in Supabase's `auth.users`, not in this app. `supabase_auth.py`
is a small GoTrue REST client built on `requests` — no `supabase-py`, which
would add seven packages to make six HTTP calls and fights Flask's signed
cookie with its own session storage. Every call returns `(data, error)`
rather than raising, so routes stay flat.

`public.profiles` is keyed by the same UUID and holds only what GoTrue has no
concept of: username, display name, XP, streak, avatars, is_admin. Email and
Google identity are **read through** via joins to `auth.users` /
`auth.identities` — never copied, because a second copy is how they drift.

Profile rows are created by the `on_auth_user_created` trigger, not by the
app. With OAuth the user appears inside GoTrue during the callback and the
app only learns about it afterwards, so app-side creation would leave a
window where an auth user exists with no profile.

Google sign-in uses **PKCE**, not the implicit flow: implicit returns the
code in the URL fragment, which browsers never send to the server. The
provider is configured in the Supabase dashboard, not in this app — the only
local switch is `GOOGLE_ENABLED`.

`current_user()` is cached on `flask.g` and reads Postgres, not GoTrue, so a
page load makes no call to the auth service. The Flask cookie is the source
of truth for "signed in", which means revoking a Supabase session does not
log someone out immediately. Fine here; revisit if payments appear.

Login is **email-only** — GoTrue does not authenticate by username.

Required env: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`
(server-side only; it bypasses RLS). `DATABASE_URL` still uses the **session
pooler**, not the direct host: `db.<ref>.supabase.co` is IPv6-only and refuses
connections on free projects. The username is `postgres.<project_ref>` — the
pooler routes on it, and a wrong region fails with `tenant/user not found`.

RLS is enabled with correct policies, but the app connects as `postgres` and
bypasses them. They are inert today and exist so a future role switch is
configuration rather than a redesign.

## Accounts, profile and deletion

`/profile` lets someone change their display name and pick one of the 12
avatars in `static/images/avatars/` (generated, then centre-cropped so none
carries a baked-in frame). Presets and Google pictures share the same
`users.avatar_url` column, so the rest of the UI never asks which it is.

Deletion in `database.py` removes child rows explicitly rather than relying
`ON DELETE CASCADE` from `auth.users`: deleting the auth record removes the
profile and every progress row with it, so the export cannot describe data
the delete leaves behind. `/profile/delete`
requires the username typed back, plus the password for password accounts,
so a borrowed unlocked laptop cannot erase an account in one click.
`export_user()` and `delete_user()` are deliberately next to each other —
the export must not describe data the delete leaves behind.

## Touch targets

Controls are sized by input device, not viewport (`@media (pointer:
coarse)`): a 27px chip is fine with a mouse and too small for a thumb, and a
large phone is still a touch device. Everything interactive measures >=40px
there. Because larger controls made the 320px nav overflow, the brand and
nav gaps shrink below 400px — check that bar again if you add anything to
`.nav-right`.

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
- `gunicorn app:app` behind any reverse proxy. All state is in Supabase, so
  instances are stateless and can scale horizontally.
- `FLASK_DEBUG=0` in production.

## Social share card

`static/images/og-card.png` is 1200x630 — the ratio every platform crops to.
It is built by `python tools/make_og.py` from two layers, split by what each
medium is actually good at. The plate (`assets/og-plate.png`, generated, not
served) supplies the navy field, grid, aurora and the wordmark. Every word the
card has to *say* — headline, proof numbers, offer, URL — is drawn in real
Manrope from `static/fonts/`, because a misspelt wordmark or a wrong count is
unshippable and an image model cannot be trusted with text.

The shading ramp under the copy starts at 52% height on purpose: a plain
top-to-bottom gradient greys out the wordmark, which has to stay at full
strength. `og:image:width/height` are declared — without them scrapers often
render the small square card instead of the large one.

## Transactional email

`mailer.py` posts to Resend over HTTP with `requests` (already a dependency for
Google sign-in) on a daemon thread, so signup never waits on mail. Everything
is a no-op when `RESEND_API_KEY` is unset, and `send_welcome_email()` swallows
its own exceptions — a mail outage must not turn a successful signup into an
error page. The template in `templates/email/welcome.html` is table-based with
inline styles: Outlook renders through Word, and Gmail strips most of <head>.
