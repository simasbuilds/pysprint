"""Curated free Python resources from elsewhere on the web.

Deliberately short. A list of forty links is a way of avoiding the
decision; these are the ones worth a beginner's time, each with an honest
note on what it is actually good for — and where something is only partly
free, it says so rather than sending people into a paywall.
"""

RESOURCES = [
    {
        "group": "When you are stuck on what the code is doing",
        "items": [
            {
                "name": "Python Tutor",
                "url": "https://pythontutor.com",
                "icon": "eye",
                "note": "Paste code and step through it one line at a time, watching variables, "
                        "lists and function calls change. The single best way to fix a wrong "
                        "mental model of how a loop or a reference actually works.",
                "cost": "Free, no signup",
            },
            {
                "name": "Official Python tutorial",
                "url": "https://docs.python.org/3/tutorial/",
                "icon": "book",
                "note": "The canonical explanation, written by the people who build the language. "
                        "Drier than a course, but it is right, and it stays right.",
                "cost": "Free",
            },
            {
                "name": "Standard library reference",
                "url": "https://docs.python.org/3/library/",
                "icon": "layers",
                "note": "What is already installed, before you go looking for a package. Worth "
                        "skimming the contents page once so you know what exists.",
                "cost": "Free",
            },
        ],
    },
    {
        "group": "When you want more practice",
        "items": [
            {
                "name": "Exercism — Python track",
                "url": "https://exercism.org/tracks/python",
                "icon": "target",
                # Exercism blocks automated requests, so the exercise count could
                # not be checked here — kept to what its model reliably is.
                "note": "Exercises solved in your own editor against a real test suite, with "
                        "volunteer mentors who review your solution and suggest a more "
                        "idiomatic one.",
                "cost": "Free, account needed",
            },
            {
                "name": "Advent of Code",
                "url": "https://adventofcode.com",
                "icon": "star",
                "note": "A December puzzle calendar, but every past year stays open. The early "
                        "days of each year are approachable once you are comfortable with loops "
                        "and dictionaries.",
                "cost": "Free",
            },
            {
                "name": "CS50P — Harvard",
                "url": "https://cs50.harvard.edu/python/",
                "icon": "graduation",
                "note": "A full university introduction to programming with Python, lectures and "
                        "problem sets included. Slower and more rigorous than a lesson here.",
                "cost": "Free to audit",
            },
        ],
    },
    {
        "group": "When you want to go deeper",
        "items": [
            {
                "name": "Automate the Boring Stuff",
                "url": "https://automatetheboringstuff.com",
                "icon": "tools",
                "note": "A complete book, free to read online, on pointing Python at tedious real "
                        "work — files, spreadsheets, email, the web. The natural next step after "
                        "the projects here.",
                "cost": "Free to read online",
            },
            {
                "name": "PEP 8 — the style guide",
                "url": "https://peps.python.org/pep-0008/",
                "icon": "note",
                "note": "How Python code is conventionally written and spaced. Read it once you "
                        "can write code that works; it is about being readable to other people.",
                "cost": "Free",
            },
            {
                "name": "Real Python",
                "url": "https://realpython.com",
                "icon": "bulb",
                "note": "Long, careful articles on specific topics — decorators, virtual "
                        "environments, async. Many are free to read; some tutorials and the "
                        "video courses are paid, so check before you commit time.",
                "cost": "Partly free",
            },
            {
                "name": "PyPI",
                "url": "https://pypi.org",
                "icon": "blocks",
                "note": "The index of installable packages. Once you leave the browser and run "
                        "Python locally, this is where the rest of the ecosystem lives.",
                "cost": "Free",
            },
        ],
    },
]


def resource_count():
    return sum(len(g["items"]) for g in RESOURCES)
