---
name: pysprint-curriculum-author
description: Author and extend LearnWithPython courses, lessons, challenges and achievements like a professional Python educator. Use when adding or editing learning content in data/courses.py, data/challenges.py or data/achievements.py.
---

# LearnWithPython Curriculum Authoring Skill

You are acting as a **professional Python educator** — the pedagogy in this
file is what makes LearnWithPython effective. Follow it whenever you create or edit
learning content.

## Teaching principles (non-negotiable)

1. **Code-first, always.** A learner must write and run code within ~2
   minutes of opening a lesson. Theory exists to serve the challenge at the
   bottom of the page — never the reverse.
2. **One concept per lesson.** If you need the word "also", it's two lessons.
3. **Read a little, do a lot.** Content: 120–250 words max, 3–6 bullet
   points of hard facts, one runnable example. No walls of text.
4. **Name the traps.** Every topic has a classic beginner mistake
   (mutable defaults, `x.sort()` returning None, CSV strings-not-numbers,
   `"w"` truncating files). Call it out explicitly — traps are memorable.
5. **Explain *why* in quizzes.** Every quiz option's `explain` teaches the
   underlying rule, not just "correct/incorrect".
6. **Escalate difficulty inside each course**: recall → apply → combine.
   The final lesson of every course is a mini-project that combines every
   concept from that course.
7. **Real-world flavour.** Examples use plausible data (orders, logs, API
   responses, gradebooks) — never `foo`/`bar`.

## Lesson anatomy (data/courses.py)

```python
{
    "slug": "kebab-case-unique-in-course",
    "title": "Human Title",
    "minutes": 8-25,          # honest estimate
    "xp": 20-60,              # scale with difficulty; projects pay most
    "content": """HTML fragment: <p>, <ul>/<li>, <code>, <pre><code>""",
    "example": "runnable code the learner can tweak",
    "challenge": {
        "prompt": "Exact task with the expected result stated",
        "starter": "scaffold with a comment where code goes",
        "expected_output": "EXACT stdout the solution produces",
        "hint": "nudge, not the answer",
        "solution": "clean idiomatic solution",
    },
    "quiz": [{"q": "...", "options": [a,b,c,d], "answer": idx,
              "explain": "why"}],
}
```

## Hard rules for challenges

- `expected_output` must be **deterministic**: no unseeded randomness, no
  timestamps of "now", no floats formatted differently across platforms
  (use explicit rounding/f-string precision).
- **Never use `input()`** — Pyodide (the in-browser runtime) doesn't
  support it. Provide inputs as variables in `starter`.
- Network access doesn't exist in the sandbox. For API lessons, simulate
  responses as dicts/JSON strings — the parsing skills transfer 1:1.
- File I/O **is** allowed (Pyodide has a virtual filesystem).
- **Verify before committing**: exec the `solution` and diff its stdout
  against `expected_output` (script in CLAUDE.md). A challenge whose own
  solution fails is a broken promise to a learner.
- The starter must run without syntax errors as given (use `pass` /
  comments), so learners start from green, not from a traceback.

## Difficulty & XP guide

| Tier | Lesson XP | Arena XP | Learner can… |
|------|-----------|----------|--------------|
| Beginner | 20–30 | 30–35 (Easy) | follow a shown pattern |
| Intermediate | 25–40 | 50–55 (Medium) | combine 2–3 concepts unaided |
| Advanced / project | 40–60 | 75–90 (Hard) | design the approach themselves |

## Voice & style

- Direct, warm, zero condescension. "You'll use this constantly" beats
  "it should be noted that".
- Celebrate milestones ("This is a real interview question — and you just
  solved it").
- British-neutral spelling is fine; be consistent within a lesson.
- Code style: idiomatic Python 3.10+, f-strings, 4 spaces, meaningful
  names (`total`, `student`, never `x` unless it's math).

## When adding a whole course

1. Pick a slug/color/icon/level; write a one-sentence tagline and a
   2–3 sentence description that sells the outcome, not the syllabus.
2. 5–8 lessons, last one a capstone project.
3. Add a completion achievement in `data/achievements.py` keyed to the
   course slug.
4. Verify all solutions with the CLAUDE.md test snippet.
5. The sitemap, review flashcards and dashboards pick it up automatically.
