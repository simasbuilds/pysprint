"""Deep-dive extras rendered on every lesson page.

Keyed by (course_slug, lesson_slug). Each entry:
  real_world : where this concept shows up in professional work
  pitfalls   : list of classic mistakes (HTML allowed)
  pro_tip    : one expert-level habit or trick
"""

LESSON_EXTRAS = {
    # ── python-fundamentals ──────────────────────────────────────────
    ("python-fundamentals", "hello-python"): {
        "real_world": "print() is a developer's first debugging tool — professionals sprinkle prints to inspect running programs before reaching for real debuggers, and every CLI tool you've ever used writes its output exactly this way.",
        "pitfalls": [
            "Forgetting the parentheses: <code>print \"hi\"</code> worked in Python 2 but is a SyntaxError in Python 3.",
            "Mismatched quotes: <code>print(\"hello')</code> — start and end with the same quote character.",
            "Writing code after a comment on the same line and expecting it to run — everything after <code>#</code> is ignored.",
        ],
        "pro_tip": "print() accepts a sep= and end= argument: print(\"a\", \"b\", sep=\"-\", end=\"!\") gives a-b!. You'll use end=\"\" whenever you want to print without a newline.",
    },
    ("python-fundamentals", "variables-and-types"): {
        "real_world": "Every configuration file, user record and shopping cart is variables of these four types. Type confusion (a \"5\" that should be a 5) is the single most common bug class in real codebases — banks have lost money to it.",
        "pitfalls": [
            "Using a variable before assigning it → NameError. Python reads top-to-bottom.",
            "Confusing <code>=</code> (assign) with <code>==</code> (compare).",
            "Expecting <code>\"5\" + 5</code> to work — Python never silently converts between str and int the way JavaScript does. Convert explicitly with <code>int()</code> or <code>str()</code>.",
        ],
        "pro_tip": "Name variables for what they contain, not their type: total_price beats tp beats x. Six months from now, the reader of your code is you.",
    },
    ("python-fundamentals", "numbers-and-math"): {
        "real_world": "Modulo drives real systems: 'every 15th request gets logged', hash tables, round-robin load balancing, cyclic calendars. Floor division powers pagination — page = item_index // page_size.",
        "pitfalls": [
            "Floating point surprises: <code>0.1 + 0.2 == 0.3</code> is <strong>False</strong> (it's 0.30000000000000004). Use <code>round()</code> for display and the <code>decimal</code> module for money.",
            "Integer division habits from other languages: in Python, <code>7 / 2</code> is 3.5, never 3. Use <code>//</code> when you want the floor.",
            "Operator precedence: <code>2 + 3 * 4</code> is 14, not 20 — use parentheses generously.",
        ],
        "pro_tip": "Python ints have no maximum size — 2 ** 10000 just works. Also: underscores make big numbers readable: population = 8_100_000_000.",
    },
    ("python-fundamentals", "strings"): {
        "real_world": "f-strings are everywhere in production Python: log messages, SQL parameters, API URLs, email templates. Since Python 3.6 they've replaced every older formatting style in new code.",
        "pitfalls": [
            "Strings are immutable: <code>s[0] = \"H\"</code> is a TypeError. Methods like <code>.upper()</code> return a <em>new</em> string — <code>s.upper()</code> alone does nothing unless you assign it.",
            "Off-by-one indexing: the first character is <code>s[0]</code>, and <code>s[len(s)]</code> is an IndexError.",
            "Forgetting the <code>f</code> prefix and printing literal braces: <code>\"{name}\"</code> vs <code>f\"{name}\"</code>.",
        ],
        "pro_tip": "f-strings have a debug shorthand: f\"{price=}\" prints price=19.99 — name and value. Format specs go after a colon: f\"{total:.2f}\" (2 decimals), f\"{n:,}\" (thousands separators).",
    },
    ("python-fundamentals", "conditionals"): {
        "real_world": "Every access check ('is this user an admin?'), price rule ('free shipping over €50') and form validation in every app you use is an if/elif chain. Reading them fluently is reading business logic.",
        "pitfalls": [
            "Using <code>=</code> instead of <code>==</code> in a condition — Python catches this as a SyntaxError, unlike C.",
            "Forgetting the colon at the end of <code>if</code>/<code>elif</code>/<code>else</code> lines.",
            "Inconsistent indentation — mixing tabs and spaces breaks the block structure. Configure your editor to insert 4 spaces per Tab.",
            "Chaining that never triggers: checking <code>score >= 80</code> before <code>score >= 90</code> means the 90 branch is unreachable.",
        ],
        "pro_tip": "Python chains comparisons naturally: 18 <= age < 65 works exactly like the math notation. Also, empty containers are falsy — 'if my_list:' is the Pythonic way to test non-emptiness.",
    },
    ("python-fundamentals", "loops"): {
        "real_world": "Loops process every row of a spreadsheet, every user in a database, every line of a log file. 'For each order, send an email' — that sentence is a for loop, and automation careers are built on it.",
        "pitfalls": [
            "Off-by-one with range: <code>range(5)</code> is 0–4. Want 1–5? <code>range(1, 6)</code>.",
            "Infinite while loops — forgetting to change the loop variable inside the body.",
            "Modifying a list while looping over it — skips elements unpredictably. Loop over a copy: <code>for x in items[:]</code>.",
        ],
        "pro_tip": "Need the index AND the value? Never do range(len(items)) — use enumerate: for i, item in enumerate(items). Looping two lists together? zip(names, scores).",
    },
    ("python-fundamentals", "fizzbuzz-project"): {
        "real_world": "FizzBuzz is a genuine screening question at real companies — interviewers use it because a surprising share of applicants can't order the conditions correctly. You now can, on demand.",
        "pitfalls": [
            "Checking <code>% 3</code> before <code>% 15</code> — the most specific condition must come first in any if/elif chain.",
            "Printing <code>\"15\"</code>-style strings instead of the number for the default case — <code>print(i)</code>, not <code>print(\"i\")</code>.",
        ],
        "pro_tip": "A slicker variant builds the word: word = \"Fizz\" * (i % 3 == 0) + \"Buzz\" * (i % 5 == 0); print(word or i). Understand why that works (bool × str, empty string is falsy) and you've leveled up.",
    },

    # ── data-structures ──────────────────────────────────────────────
    ("data-structures", "lists"): {
        "real_world": "API responses arrive as lists of records; every table, feed and search result you render starts life as a list. append() inside a loop is the fundamental 'collect results' pattern of data processing.",
        "pitfalls": [
            "<code>IndexError: list index out of range</code> — a 4-item list has indexes 0–3, and an empty list has none at all.",
            "Copy confusion: <code>b = a</code> makes both names point to the <em>same</em> list; changing one changes 'both'. Real copy: <code>b = a.copy()</code> or <code>b = a[:]</code>.",
            "<code>append()</code> vs <code>extend()</code>: append([4,5]) adds one nested list; extend([4,5]) adds two numbers.",
        ],
        "pro_tip": "Lists have a fast membership test but for thousands of 'x in collection' checks, convert to a set first — it's hundreds of times faster on large data.",
    },
    ("data-structures", "slicing-and-methods"): {
        "real_world": "Slicing is data science's daily bread: first 100 rows to preview (rows[:100]), last week of readings (data[-7:]), every second sample (signal[::2]). Pandas and NumPy extend this exact syntax.",
        "pitfalls": [
            "<code>y = x.sort()</code> — .sort() sorts in place and returns <strong>None</strong>, so y is None. Use <code>y = sorted(x)</code> to keep the original.",
            "Expecting the stop index to be included: <code>nums[1:3]</code> is two items, not three.",
            "<code>reverse=True</code> vs <code>[::-1]</code>: .sort(reverse=True) sorts descending; [::-1] merely reverses current order.",
        ],
        "pro_tip": "Slices never raise IndexError — \"abc\"[10:20] is just \"\". That makes truncation safe in one line: preview = text[:280].",
    },
    ("data-structures", "dictionaries"): {
        "real_world": "Every JSON API payload, every database row, every config file becomes a dict in Python. Redis, MongoDB and Python's own objects (via __dict__) are key–value stores — this shape runs the internet.",
        "pitfalls": [
            "KeyError from direct access on a maybe-missing key — use <code>.get(key, default)</code> when absence is normal.",
            "Using a list as a key → TypeError: keys must be hashable (str, int, tuple are fine).",
            "Counting without initialising: <code>counts[word] += 1</code> crashes on the first sighting. Use <code>counts[word] = counts.get(word, 0) + 1</code> — or Counter.",
        ],
        "pro_tip": "dict.setdefault(key, []).append(item) builds grouped data in one line, and {**defaults, **overrides} merges two dicts (right side wins). Both appear constantly in real code.",
    },
    ("data-structures", "tuples-and-sets"): {
        "real_world": "Functions that 'return two values' actually return one tuple — divmod(17, 5) gives (3, 2). Sets power tag systems, deduplicating email lists, and 'which users are in group A but not B' queries.",
        "pitfalls": [
            "A one-item tuple needs a comma: <code>(5)</code> is just the number 5; <code>(5,)</code> is a tuple.",
            "<code>{}</code> creates an empty <strong>dict</strong>, not a set — empty set is <code>set()</code>.",
            "Sets are unordered: never rely on the order you see when printing one.",
        ],
        "pro_tip": "Tuple unpacking works in loop headers: for name, score in pairs: — and the swap idiom a, b = b, a needs no temp variable. Interviewers notice when you use it.",
    },
    ("data-structures", "comprehensions"): {
        "real_world": "Comprehensions are the mark of fluent Python — code reviewers at top companies flag 4-line append loops that should be one comprehension. They also map directly onto SQL's SELECT-WHERE mental model.",
        "pitfalls": [
            "Nesting too much: a comprehension with multiple <code>for</code>s and <code>if</code>s is harder to read than the loop it replaced. Two clauses max.",
            "Using one for side effects: <code>[print(x) for x in items]</code> builds a useless list of Nones — use a plain loop when you don't need the result.",
            "Filter goes after the for: <code>[x if x > 0 for x in nums]</code> is a SyntaxError; <code>[x for x in nums if x > 0]</code> is right. (x if cond else y <em>before</em> the for is a different, valid pattern.)",
        ],
        "pro_tip": "Generator expressions — the same syntax with () — process items lazily without building a list: sum(n * n for n in range(10**6)) uses almost no memory.",
    },
    ("data-structures", "nested-data-project"): {
        "real_world": "This gradebook shape — a list of dicts — is byte-for-byte what you get from requests.get(...).json(), a CSV DictReader, or a database ORM. Master the drill-down and every API is readable.",
        "pitfalls": [
            "Guessing the structure instead of checking: print one element (<code>print(data[0])</code>) before writing access code.",
            "Deep chains with no safety: <code>d[\"a\"][\"b\"][\"c\"]</code> crashes on the first missing level — use <code>.get()</code> with defaults for optional branches.",
            "Tracking 'best so far' but initialising best_avg to 0 — fails when all averages are negative. Initialise to the first element or -infinity.",
        ],
        "pro_tip": "max(students, key=lambda s: sum(s['grades'])/len(s['grades'])) finds the top student in one line — the key= pattern replaces the whole tracking loop.",
    },

    # ── functions-oop ────────────────────────────────────────────────
    ("functions-oop", "defining-functions"): {
        "real_world": "Every library you'll ever import — requests, pandas, Flask — is a box of functions. Professional codebases enforce small single-purpose functions in code review; it's the #1 readability rule.",
        "pitfalls": [
            "Confusing print with return: a function that prints but returns None can't be used in further calculations — <code>total = get_price() * 2</code> breaks.",
            "Code after <code>return</code> never runs.",
            "Calling with the wrong argument count → TypeError telling you exactly what's missing. Read it.",
        ],
        "pro_tip": "Give every function a one-line docstring — def area(w, h): \"\"\"Return the area of a w × h rectangle.\"\"\" — then help(area) works, and so does your editor's tooltip.",
    },
    ("functions-oop", "arguments"): {
        "real_world": "Open any library's docs: requests.get(url, params=None, timeout=None, **kwargs) — defaults, keywords and kwargs everywhere. Understanding this lesson is understanding how every Python API is designed.",
        "pitfalls": [
            "The mutable default trap: <code>def add(item, items=[])</code> shares ONE list across all calls. It's the most famous Python gotcha — use <code>items=None</code> then <code>items = items or []</code>.",
            "Positional after keyword: <code>f(x=1, 2)</code> is a SyntaxError — keywords go last.",
            "Forgetting that *args is a tuple inside the function — you can loop it and len() it.",
        ],
        "pro_tip": "The * also unpacks at call time: print(*[1, 2, 3]) is print(1, 2, 3), and merge = {**d1, **d2} for dicts. Packing and unpacking are the same symbol in opposite directions.",
    },
    ("functions-oop", "scope-and-lambda"): {
        "real_world": "key= functions drive real product features: 'sort products by price', 'newest first', 'closest to you' — each is one lambda. Callbacks in GUIs and web frameworks are this same functions-as-values idea.",
        "pitfalls": [
            "Assigning to an outer variable inside a function creates a new local one instead — the outer stays unchanged (use return values, not <code>global</code>).",
            "Multi-line logic crammed into a lambda — if it doesn't fit on one line, def a named function.",
            "sorted() vs .sort() again: sorted returns the new list; .sort() mutates and returns None.",
        ],
        "pro_tip": "min/max/sorted all share key=, and the operator module replaces common lambdas: sorted(users, key=itemgetter('age')) reads better and runs faster than the lambda version.",
    },
    ("functions-oop", "classes-and-objects"): {
        "real_world": "Django models, game entities, GUI widgets, bank accounts — anywhere data and behaviour travel together, there's a class. Frameworks hand you base classes and your entire job is filling in methods.",
        "pitfalls": [
            "Forgetting <code>self</code> in the method signature → 'takes 0 positional arguments but 1 was given', the most-googled Python error.",
            "Writing <code>name = name</code> instead of <code>self.name = name</code> in __init__ — the data vanishes when the method ends.",
            "Class-level mutable attributes shared by every instance — define per-instance data inside __init__, not in the class body.",
        ],
        "pro_tip": "For data-carrying classes, @dataclass writes __init__, __repr__ and __eq__ for you: @dataclass class Point: x: int; y: int. Modern Python uses it constantly.",
    },
    ("functions-oop", "inheritance"): {
        "real_world": "Flask views, Django models, unittest.TestCase, PyTorch nn.Module — professional Python is largely subclassing framework base classes and overriding the methods they document.",
        "pitfalls": [
            "Forgetting <code>super().__init__(...)</code> in the child — parent attributes silently never get created, then explode later as AttributeError.",
            "Inheriting for code reuse when there's no is-a relationship — a Car is not an Engine; it <em>has</em> one. Prefer composition.",
            "Deep inheritance towers (A→B→C→D) — two levels is usually the sane maximum.",
        ],
        "pro_tip": "isinstance(obj, Animal) is True for subclasses too — that's the point of polymorphism: code written for Animal automatically works with every Cat and Dog ever subclassed.",
    },
    ("functions-oop", "dunder-project"): {
        "real_world": "len(df), dict[key], obj1 == obj2, with open(...) — every piece of 'built-in' Python syntax is a dunder call under the hood. Pandas and NumPy feel native precisely because they implement these.",
        "pitfalls": [
            "Defining __str__ but returning a non-string → TypeError when printing.",
            "Implementing __eq__ without thinking about __hash__ — custom-equal objects may behave oddly in sets/dicts.",
            "Calling dunders directly (<code>x.__len__()</code>) — always use the built-in (<code>len(x)</code>); it's faster and idiomatic.",
        ],
        "pro_tip": "Implement __repr__ first on every class — it's what the debugger, lists and error messages show. Aim for output a developer could paste back into Python: Card(rank=7).",
    },

    # ── practical-python ─────────────────────────────────────────────
    ("practical-python", "understanding-errors"): {
        "real_world": "Reading tracebacks fast is the highest-leverage debugging skill — seniors resolve in seconds what juniors google for an hour, purely by reading the last line first and walking the stack.",
        "pitfalls": [
            "Reading only 'something went wrong' and re-running unchanged code — the message literally names the problem and line.",
            "Fixing the traceback's <em>top</em> frame — the deepest frame (bottom) is where it actually raised; upper frames are just the call path.",
            "Shipping code with silent failure paths because an error 'went away' — understand <em>why</em> before moving on.",
        ],
        "pro_tip": "Paste the final line of any traceback into a search engine verbatim — TypeError: can only concatenate str (not \"int\") to str has been solved a million times. That's not cheating; it's the professional workflow.",
    },
    ("practical-python", "try-except"): {
        "real_world": "Production services wrap every network call, file read and JSON parse in try/except — a payment API that crashes on one malformed record instead of logging and continuing loses real money.",
        "pitfalls": [
            "Bare <code>except:</code> swallowing everything including typo-NameErrors and Ctrl-C — always name the exception you expect.",
            "Wrapping 50 lines in one try — narrow the try block to the single risky call so you know what failed.",
            "Using exceptions for normal flow control when an if would do: check <code>if key in d</code> rather than catching KeyError you expect half the time.",
        ],
        "pro_tip": "except ValueError as e: print(f\"bad input: {e}\") — binding the exception gives you its message for logs. Multiple types in one clause: except (ValueError, KeyError):.",
    },
    ("practical-python", "files"): {
        "real_world": "Log writers, report generators, config loaders, data pipelines — file I/O is the connective tissue of ops and data work. The with-statement pattern here is verbatim what runs in production.",
        "pitfalls": [
            "Opening with <code>\"w\"</code> when you meant <code>\"a\"</code> — write mode instantly erases the existing file, no confirmation.",
            "Forgetting newlines: <code>f.write(\"line\")</code> does not add <code>\\n</code> — unlike print.",
            "Reading numbers and forgetting they're strings-with-newlines: always <code>int(line.strip())</code>.",
            "Hardcoded absolute paths that break on any other machine — use relative paths or pathlib.",
        ],
        "pro_tip": "pathlib makes quick jobs one-liners: Path(\"notes.txt\").read_text() and Path(\"out.txt\").write_text(data) — no open/close ceremony at all.",
    },
    ("practical-python", "modules"): {
        "real_world": "pip's 500,000+ packages all arrive through import. Splitting a growing script into modules is the first act of software architecture you'll perform on any real project.",
        "pitfalls": [
            "Naming your file after a stdlib module — a local <code>random.py</code> shadows the real one and breaks imports mysteriously. Never name files json.py, csv.py, math.py…",
            "<code>from module import *</code> — nobody (including you) can tell where names came from.",
            "Circular imports: A imports B which imports A. Restructure shared code into a third module.",
        ],
        "pro_tip": "Standard import order (enforced by pro linters): stdlib first, third-party second, your own modules third — alphabetical within each group, one blank line between groups.",
    },
    ("practical-python", "stdlib-tour"): {
        "real_world": "'Batteries included' is why Python won ops and data: json for every API, datetime for every schedule, csv for every export, Counter for every 'top N' feature — zero installs required.",
        "pitfalls": [
            "Rebuilding what exists: hand-rolled JSON parsing, manual date math across month boundaries, DIY counting loops — the stdlib version is tested against edge cases yours will miss.",
            "json.load vs json.loads (and dump/dumps): the s means string, the plain one takes a file object.",
            "random for anything security-related — passwords and tokens need the <code>secrets</code> module.",
        ],
        "pro_tip": "Before writing any utility function, spend 30 seconds checking: does itertools, collections, functools or pathlib already do this? The answer is yes more often than any other language.",
    },

    # ── apis-with-python ─────────────────────────────────────────────
    ("apis-with-python", "what-is-an-api"): {
        "real_world": "Your weather app, your bank app, 'Sign in with Google', every checkout — all API calls with these exact verbs and status codes. Backend engineering interviews open with precisely this material.",
        "pitfalls": [
            "Using GET for actions that change data — GETs get cached, prefetched and retried by infrastructure; mutations belong in POST/PUT/DELETE.",
            "Treating all non-200s the same: a 404 (ask differently) needs different handling than a 500 (their outage) or 429 (slow down).",
            "Putting secrets in URLs — URLs land in server logs and browser history; secrets go in headers.",
        ],
        "pro_tip": "Learn the memorable codes cold: 200 OK, 201 Created, 301 Moved, 400 your request is malformed, 401 who are you, 403 you can't, 404 not found, 429 too fast, 500 their bug, 503 they're down.",
    },
    ("apis-with-python", "json-deep-dive"): {
        "real_world": "JSON is the wire format of the modern web — REST APIs, webhooks, config files (VS Code settings!), NoSQL documents. Data engineers spend whole careers reshaping exactly this.",
        "pitfalls": [
            "JSON syntax is stricter than Python: double quotes only, no trailing commas, no comments — valid Python dict literals can be invalid JSON.",
            "json.loads(f) on a file object — that's json.<strong>load</strong>(f); loads takes a string.",
            "Assuming a field exists: real APIs omit optional fields — <code>data.get(\"email\")</code> beats <code>data[\"email\"]</code> for anything not guaranteed.",
        ],
        "pro_tip": "Debug any nested payload instantly with print(json.dumps(data, indent=2)) — structure jumps out. From a terminal, piping curl output through python -m json.tool does the same.",
    },
    ("apis-with-python", "consuming-apis"): {
        "real_world": "requests is the most-downloaded Python package in history. Fetch-parse-handle is the core loop of price trackers, chatbots, data pipelines and every integration ('sync our CRM with our billing').",
        "pitfalls": [
            "No timeout: <code>requests.get(url)</code> can hang forever on a dead server — production code always passes <code>timeout=</code>.",
            "Calling .json() on an error page → JSONDecodeError; check <code>resp.status_code</code> or call <code>resp.raise_for_status()</code> first.",
            "Building query strings by hand with f-strings — <code>params={...}</code> handles encoding of spaces and special characters correctly.",
        ],
        "pro_tip": "Hammering an API in a loop gets you rate-limited (429) or banned. Real integrations add a small time.sleep() between calls and back off exponentially on 429/5xx responses.",
    },
    ("apis-with-python", "building-an-api"): {
        "real_world": "Flask and FastAPI power countless production microservices; a route returning a dict is the atom of backend work. The site you're using right now is these exact patterns — read its app.py on GitHub.",
        "pitfalls": [
            "Trusting client input: request.get_json() can be None or missing keys — validate before indexing, return 400 with a clear message.",
            "Returning 200 for errors — clients and monitoring rely on honest status codes.",
            "Global mutable state (a list of books) resets on restart and breaks with multiple workers — real apps persist to a database.",
        ],
        "pro_tip": "Design the route table on paper before coding — method + path + response shape for each endpoint. Ten minutes of design saves hours of refactoring; it's also exactly how teams spec real services.",
    },
    ("apis-with-python", "rest-design"): {
        "real_world": "Good REST design is why Stripe's API is famously pleasant and legacy SOAP APIs are famously not. API design interviews for backend roles are this lesson, spoken aloud.",
        "pitfalls": [
            "Verbs in URLs (<code>/getUser</code>, <code>/createOrder</code>) — the HTTP method already is the verb.",
            "Inconsistent error shapes — every error should return the same JSON structure so clients can handle all of them with one code path.",
            "Breaking existing clients with changes — that's what /v1/ → /v2/ versioning is for.",
            "Committing API keys to git — they get scraped from public repos within minutes. Environment variables, always.",
        ],
        "pro_tip": "Before designing anything, skim the Stripe or GitHub API docs for 15 minutes — you'll absorb naming, pagination, error and versioning conventions from the best in the business.",
    },

    # ── automation ───────────────────────────────────────────────────
    ("automation", "text-processing"): {
        "real_world": "Data cleaning is famously 80% of data work, and it's split/strip/join all the way down: normalising user input, parsing log lines, generating URL slugs (this site's lesson URLs were made exactly like your challenge).",
        "pitfalls": [
            "Forgetting strip() on user input or file lines — invisible whitespace and newlines break comparisons: <code>\"cat\\n\" != \"cat\"</code>.",
            "join's calling direction: it's <code>\", \".join(items)</code> — separator first — and every item must already be a string (map(str, items) if not).",
            "replace() returns a new string; the original is untouched unless you reassign.",
        ],
        "pro_tip": "Chain transformations left-to-right for readable pipelines: line.strip().lower().replace(\",\", \"\") — each step returns a string, so they compose forever.",
    },
    ("automation", "dates-and-times"): {
        "real_world": "Billing cycles, subscription expiry, 'posted 3 hours ago', report ranges, cron schedules — nearly every business rule has a date in it, and naive date math (day+1) breaks on month ends and leap years. timedelta doesn't.",
        "pitfalls": [
            "Doing calendar math by hand — adding 1 to the day number fails on the 31st. Always use timedelta.",
            "Mixing up strftime (format → string) and strptime (parse ← string).",
            "Comparing dates as strings: as text, \"2026-2-1\" > \"2026-10-1\" — parse to date objects first.",
            "Ignoring timezones in anything user-facing — store UTC, convert at display time.",
        ],
        "pro_tip": "Log and store dates as ISO 8601 (YYYY-MM-DD) — it's unambiguous internationally and sorts correctly even as plain text. date.fromisoformat() parses it in one call.",
    },
    ("automation", "csv-data"): {
        "real_world": "Every ERP, bank, ad platform and spreadsheet exports CSV — it's the lingua franca between systems that don't share an API. This read → convert → aggregate pattern is the seed of every data pipeline (pandas industrialises exactly it).",
        "pitfalls": [
            "The #1 CSV bug: forgetting values are strings — <code>\"5\" * \"2\"</code> errors and <code>\"10\" &lt; \"9\"</code> is True. Convert types immediately.",
            "Naive parsing with .split(\",\") — real CSVs contain quoted fields with commas inside; the csv module exists because of them.",
            "Writing CSVs without <code>newline=\"\"</code> in open() on Windows — you get blank rows between every record.",
        ],
        "pro_tip": "When a CSV outgrows the csv module (millions of rows, joins, pivots), the upgrade path is pandas: pd.read_csv(f) gives you a DataFrame — and your DictReader mental model transfers directly.",
    },
    ("automation", "regex"): {
        "real_world": "Log mining, input validation, scraping, bulk find-and-replace across a codebase, extracting order IDs from emails — regex is the universal text power tool, identical in Python, JavaScript, grep and your editor's search box.",
        "pitfalls": [
            "Forgetting the raw string: <code>\"\\d\"</code> may work by luck but <code>\"\\b\"</code> silently becomes backspace — always <code>r\"...\"</code>.",
            "Greedy matching surprises: <code>&lt;.*&gt;</code> eats from the first &lt; to the LAST &gt;. The non-greedy version is <code>&lt;.*?&gt;</code>.",
            "re.match only checks the start of the string — you almost always want re.search or re.findall.",
            "Validating emails 'perfectly' with regex — a pragmatic pattern plus a confirmation email is the professional answer.",
        ],
        "pro_tip": "Build every non-trivial pattern interactively on regex101.com (set flavor to Python) — it explains each token live and saves you from blind trial and error. Bookmark it; professionals use it weekly.",
    },
    ("automation", "log-analyzer-project"): {
        "real_world": "This is a junior DevOps/data task verbatim: 'how many 5xx errors since the deploy?' Splunk, Datadog and the ELK stack are this loop at planetary scale — you just built the core of an observability product.",
        "pitfalls": [
            "Assuming every line is well-formed — production logs contain partial lines and garbage; guard with a length check or try/except per line.",
            "Reading a huge file into one string — iterate line by line and it streams in constant memory (works on files bigger than RAM).",
            "Counting with nested ifs when Counter does it declaratively — less code, fewer bugs.",
        ],
        "pro_tip": "Add argparse and your script becomes a real CLI tool: python analyze.py access.log --since 12:00. That jump — from script to tool a teammate can run — is what gets automation adopted.",
    },

    # ── python-games ─────────────────────────────────────────────────
    ("python-games", "guessing-game"): {
        "real_world": "The check-and-respond loop you just built is the event loop inside every interactive program: games, chat apps, even web servers do exactly this — receive input, branch, respond, repeat.",
        "pitfalls": [
            "Getting the branch order wrong so a case can never be reached — test all three paths (low, high, equal).",
            "Using <code>=</code> where you mean <code>==</code> inside a condition — assignment vs comparison.",
            "Forgetting to indent the if/elif/else inside the for loop, so only the last guess is checked.",
        ],
        "pro_tip": "When logic misbehaves, print the state each turn: print(guess, 'vs', secret). Watching values flow through a loop fixes most bugs faster than staring at the code.",
    },
    ("python-games", "dice-luck"): {
        "real_world": "Seeded randomness runs the world's simulations: game worlds (a Minecraft world is a seed), scientific Monte-Carlo models, and every automated test of 'random' behaviour. Reproducible luck is a professional tool.",
        "pitfalls": [
            "Calling random.seed() inside the loop — that restarts the sequence and every 'roll' becomes identical.",
            "Expecting randint(1, 6) to exclude 6 — unlike range(), it includes both endpoints.",
            "Rolling one die and doubling it: <code>2 * randint(1, 6)</code> can never produce 7 and has completely different odds from two real dice.",
        ],
        "pro_tip": "random.choice(list) and random.shuffle(list) cover most game needs without index math — picking a random enemy is one readable line.",
    },
    ("python-games", "ascii-art"): {
        "real_world": "Progress bars, terminal dashboards, board-game grids and even the loading spinners in CLI tools are all 'draw with loops'. htop and git's progress output are professional ASCII art.",
        "pitfalls": [
            "Off-by-one ranges: range(1, 5) gives four rows, not five — check your endpoints against the shape.",
            "Forgetting the third argument of range() for counting down: range(3, 0, -1), not range(3, 0).",
            "Building one giant string when a print-per-row loop is clearer and easier to debug.",
        ],
        "pro_tip": "Center shapes with str.center(): print((\"*\" * i).center(9)) turns your triangle into a pyramid — width math handled for you.",
    },
    ("python-games", "word-games"): {
        "real_world": "Normalise-then-compare powers case-insensitive logins, search engines, duplicate detection and spell checkers. DNA analysis uses the same reversal tricks on genetic sequences.",
        "pitfalls": [
            "Comparing without normalising case first — 'Level' != 'level' to Python.",
            "Confusing word.reverse() (doesn't exist for strings) with the slice word[::-1].",
            "Testing the original word instead of the cleaned one after lowering it — clean, then use the clean value everywhere.",
        ],
        "pro_tip": "For phrase palindromes ('Never odd or even'), strip non-letters first: clean = \"\".join(ch for ch in text.lower() if ch.isalpha()). One comprehension makes the test bulletproof.",
    },
    ("python-games", "adventure-game"): {
        "real_world": "Data-driven design — world as data, engine as code — is how real games ship: level editors write data files, the engine stays unchanged. It's also how CMSs, chatbots and workflow tools scale content without new code.",
        "pitfalls": [
            "A typo between a path entry and a room key → KeyError. Keys must match exactly, including case.",
            "Putting story text in the loop instead of the dict — then every new room needs new code, defeating the design.",
            "Printing the final message inside the loop (indented) so it repeats after every room.",
        ],
        "pro_tip": "Give each room a dict of exits — \"hall\": {\"desc\": ..., \"exits\": {\"north\": \"library\"}} — and your walk can become a real free-roaming game with about ten more lines.",
    },

    # ── algorithms ───────────────────────────────────────────────────
    ("algorithms", "decomposition"): {
        "real_world": "Ticket breakdowns, pseudocode in design docs, TODO-comment skeletons — decomposition is the daily bread of professional programming. Interviewers score the way you split the problem before they score your syntax.",
        "pitfalls": [
            "Starting to type before you can say the steps out loud — blank-editor paralysis is a planning gap, not a skill gap.",
            "Steps that are too big ('process the data') — a good step maps to one or two lines of code.",
            "Skipping the 'what comes out?' question and coding toward the wrong output format.",
        ],
        "pro_tip": "If a step feels hard to code, decompose that step again. Recursion isn't only for functions — it's how you plan.",
    },
    ("algorithms", "searching"): {
        "real_world": "Database indexes, autocomplete, DNS resolution and git bisect all live on binary search. 'Can I halve this?' is the question behind almost every system that answers instantly at scale.",
        "pitfalls": [
            "Running binary search on unsorted data — it silently returns nonsense rather than erroring.",
            "Writing while low < high instead of low <= high and missing the last candidate.",
            "Forgetting the +1/-1 when moving low or high, which loops forever on some targets.",
        ],
        "pro_tip": "Python ships binary search as the bisect module: bisect.bisect_left(sorted_list, target) — use it in real code, write it by hand in interviews.",
    },
    ("algorithms", "sorting"): {
        "real_world": "Every table header you've ever clicked runs a key-based sort. Timsort — invented for Python — now also sorts Java and Android. The tuple-key trick handles real reporting: department, then salary, then name.",
        "pitfalls": [
            "Confusing sorted(items) (returns a new list) with items.sort() (in place, returns None) — printing the result of .sort() gives None.",
            "Sorting strings expecting numeric order: \"10\" < \"9\" alphabetically. Convert first or use key=int.",
            "Reaching for cmp-style comparison logic — Python only does key functions, which are simpler anyway.",
        ],
        "pro_tip": "Sort descending on one field and ascending on another by negating numbers: key=lambda r: (-r[\"score\"], r[\"name\"]).",
    },
    ("algorithms", "recursion"): {
        "real_world": "File-tree walkers, JSON serialisers, comment threads, org charts, compilers — anything nested is naturally recursive. os.walk and json.dumps are recursion you already use.",
        "pitfalls": [
            "No reachable base case → RecursionError at ~1000 frames.",
            "Forgetting <code>return</code> on the recursive call: <code>digit_sum(n // 10)</code> computes the value and throws it away — you need <code>return n % 10 + digit_sum(...)</code>.",
            "Recursing on the same input instead of a smaller one — shrinkage is what guarantees termination.",
        ],
        "pro_tip": "Trust the recursive call. Verify the base case, verify one step, and stop mentally unrolling five levels — that discipline is what makes recursion easy.",
    },
    ("algorithms", "counting-steps"): {
        "real_world": "Big-O is the shared language of code review and system design: 'this endpoint is O(n²) on cart size' is a complete bug report. It predicts at design time what profilers confirm in production.",
        "pitfalls": [
            "Judging speed by lines of code — one nested loop outweighs fifty straight-line statements.",
            "Hiding a loop inside a loop accidentally: <code>if x in big_list</code> inside a for is O(n²) in disguise. Use a set.",
            "Optimising an O(n) function when the real cost is an O(n²) block elsewhere — count first, optimise second.",
        ],
        "pro_tip": "Memorise three growth feelings: log n (barely notices data), n (scales linearly), n² (fine at 100, dead at 100,000). Most day-to-day performance calls need nothing more.",
    },

    # ── data-analysis ────────────────────────────────────────────────
    ("data-analysis", "describing-data"): {
        "real_world": "'Median household income', 'average response time', 'most common error' — every metrics dashboard and news statistic is these three functions. Choosing mean vs median honestly is half of data literacy.",
        "pitfalls": [
            "Reporting the mean of skewed data (salaries, house prices, response times) — one outlier misleads everyone downstream.",
            "Calling mode() on data with no repeats — in older Pythons it raised; modern statistics.mode returns the first value, which may surprise you.",
            "Doing sum(x)/len(x) on an empty list → ZeroDivisionError. Guard empty datasets before describing them.",
        ],
        "pro_tip": "statistics.quantiles(data, n=4) gives quartiles — the p25/p50/p75 shape of your data. Engineers report p95 latency, not the average, for exactly the outlier reasons above.",
    },
    ("data-analysis", "cleaning-data"): {
        "real_world": "Analysts genuinely spend most of their time here: exported CSVs with stray spaces, 'N/A', euro signs and thousands separators. Robust cleaning is why senior analysts' numbers are trusted.",
        "pitfalls": [
            "Cleaning while iterating the same list you're modifying — build a new clean list instead.",
            "int(\"3.5\") raises ValueError — parse decimals with float() first if decimals are possible.",
            "Silently dropping bad rows without counting them — in real work, the skip count is itself a data-quality metric.",
        ],
        "pro_tip": "Normalise aggressively before converting: value.strip().lower().replace(\",\", \"\").removeprefix(\"€\") handles most European CSV horrors in one chain.",
    },
    ("data-analysis", "grouping-data"): {
        "real_world": "GROUP BY in SQL, groupby() in pandas, pivot tables in Excel — the dict accumulator is the same operation with the curtain pulled back. Understanding it here means those tools become syntax, not magic.",
        "pitfalls": [
            "totals[key] += value without initialising → KeyError on the first sighting of each key. Use .get(key, 0) or defaultdict.",
            "Assuming dict iteration order is sorted — it's insertion order. Sort explicitly when reporting.",
            "Accumulating floats and being surprised by 0.30000000000000004 — round at display time, not during accumulation.",
        ],
        "pro_tip": "from collections import defaultdict; totals = defaultdict(float) removes the .get dance entirely: totals[key] += value just works.",
    },
    ("data-analysis", "rankings"): {
        "real_world": "Top-N queries power every leaderboard, 'best sellers' shelf, alerting system ('5 slowest endpoints') and recommendation panel. It's among the most-run query shapes in industry.",
        "pitfalls": [
            "Sorting the dict instead of its .items() — you'll rank keys alphabetically and wonder where the numbers went.",
            "Forgetting reverse=True and shipping a bottom-3 as your top-3.",
            "Slicing before sorting — [:3] on unsorted items is just the first three, not the best three.",
        ],
        "pro_tip": "For huge datasets, heapq.nlargest(3, units.items(), key=lambda p: p[1]) finds the podium without fully sorting a million rows.",
    },
    ("data-analysis", "insight-report"): {
        "real_world": "This is the nightly job at thousands of companies: parse yesterday's transactions, skip the garbage, total by region, email the summary. You've written the core of a BI pipeline in ~15 lines.",
        "pitfalls": [
            "Counting a row as valid before it survives conversion — increment inside the try, after int() succeeds.",
            "row.split(\",\") assuming exactly two fields — a stray comma shifts everything; in real work check the field count.",
            "Reporting totals but not the denominator — '490 revenue' means little without 'from 5 valid rows of 6'.",
        ],
        "pro_tip": "Structure real pipelines as three functions — parse(rows), aggregate(records), report(totals) — so each stage is testable alone. The csv module then replaces your split(\",\") for free.",
    },

    # ── expert-python ────────────────────────────────────────────────
    ("expert-python", "generators"): {
        "real_world": "Generators are how Python streams anything bigger than RAM: Django querysets, csv.reader, database cursors and every line-by-line log processor are lazy iterators. Data engineers chain generators into pipelines that crunch terabytes on a laptop.",
        "pitfalls": [
            "A generator is <strong>exhausted</strong> after one pass — looping over it a second time silently yields nothing. Recreate it or store the results if you need them twice.",
            "Calling a generator function doesn't run any of its code: <code>countdown(3)</code> returns a generator object; the body only runs when you iterate.",
            "Using <code>len()</code> on a generator → TypeError. A lazy stream has no length until it's consumed.",
        ],
        "pro_tip": "yield from delegates to another iterable in one line: def walk(tree): yield from tree.left; yield tree.value; yield from tree.right. It's the secret to elegant recursive generators.",
    },
    ("expert-python", "decorators"): {
        "real_world": "Open any production codebase and the decorators pile up: @app.route in Flask, @pytest.fixture, @login_required, @retry, @celery.task. Whole frameworks are decorator-driven because they add behaviour without touching business logic.",
        "pitfalls": [
            "Forgetting to <code>return wrapper</code> from the decorator — the decorated function becomes <code>None</code> and every call raises TypeError.",
            "Forgetting to return the inner function's result from the wrapper — the wrapped function suddenly returns None everywhere.",
            "Losing the function's name and docstring: wrap the wrapper with <code>@functools.wraps(func)</code> so introspection and debugging still work.",
        ],
        "pro_tip": "A decorator that takes arguments, like @retry(times=3), is a function that returns a decorator — three nested defs. Write the plain decorator first, then wrap it once more for the arguments.",
    },
    ("expert-python", "context-managers"): {
        "real_world": "Database transactions (commit/rollback), file handles, thread locks, temporary directories, test mocks (unittest.mock.patch) and even changing directories — professional code wraps every setup/teardown pair in with so cleanup survives exceptions.",
        "pitfalls": [
            "Returning <code>True</code> from <code>__exit__</code> without meaning to — that <em>swallows</em> the exception and the caller never learns something failed.",
            "Doing risky work in <code>__init__</code> instead of <code>__enter__</code> — resources should be acquired when the with block starts, not when the object is created.",
            "Forgetting that <code>as</code> binds <code>__enter__</code>'s return value — return <code>self</code> unless you have a better handle to give.",
        ],
        "pro_tip": "One with statement can manage several resources: with open(a) as f, open(b) as g:. And contextlib.suppress(FileNotFoundError) replaces a try/except/pass in one readable line.",
    },
    ("expert-python", "data-model"): {
        "real_world": "pathlib overloads / to join paths, NumPy overloads every operator for arrays, Django models compare by value — Python's most loved libraries feel native precisely because they implement the data model instead of inventing method names.",
        "pitfalls": [
            "Defining <code>__eq__</code> without thinking about <code>__hash__</code> — Python sets <code>__hash__</code> to None, and your objects can no longer live in sets or dict keys. Implement both or use @dataclass(frozen=True).",
            "Returning a plain tuple from <code>__add__</code> instead of a new instance of your class — addition should stay closed over the type.",
            "Writing <code>__repr__</code> that hides information: aim for eval-able output like Vector(4, 6), not '&lt;Vector object&gt;'.",
        ],
        "pro_tip": "Implement __repr__ on every class you write, first thing. Debugging a list of '<Order object at 0x7f...>' is misery; a list of Order(id=7, total=99.5) reads itself.",
    },
    ("expert-python", "functional-tools"): {
        "real_world": "@lru_cache turns expensive API lookups and recursive algorithms into O(1) repeats — it's a one-line performance patch used all over production code. itertools powers scheduling (cycle), pagination (islice), and combinatorics in testing and pricing engines.",
        "pitfalls": [
            "Caching a function with <strong>mutable</strong> or unhashable arguments — @lru_cache needs hashable args and will TypeError on lists.",
            "Using reduce where sum(), max() or a comprehension is clearer — reduce is for genuinely custom folds, not a badge of honour.",
            "Printing an itertools result and seeing <code>&lt;itertools.combinations object&gt;</code> — iterators must be consumed (list(), a loop) to see their values.",
        ],
        "pro_tip": "functools.partial shines with callbacks and key functions: sorted(rows, key=partial(score, weights=w)). It's cleaner than a lambda when you're just pinning arguments.",
    },
    ("expert-python", "modern-python"): {
        "real_world": "Type hints are mandatory in most professional Python teams — mypy/pyright run in CI at Google, Meta, Stripe and Dropbox. Dataclasses (and their cousin pydantic) define API payloads, configs and domain models in nearly every modern service.",
        "pitfalls": [
            "Mutable default fields: <code>tags: list = []</code> raises ValueError in a dataclass — use <code>field(default_factory=list)</code>.",
            "Assuming hints validate at runtime: <code>age: int = \"forty\"</code> runs happily. Enforcement needs mypy or a validation library like pydantic.",
            "Ordering fields wrong: fields with defaults must come after fields without, exactly like function parameters.",
        ],
        "pro_tip": "@dataclass(frozen=True, slots=True) gives you an immutable, hashable, memory-lean record type — the closest Python gets to a value type, perfect for keys, coordinates and money.",
    },
}


def get_extras(course_slug, lesson_slug):
    return LESSON_EXTRAS.get((course_slug, lesson_slug))
