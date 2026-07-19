"""PySprint curriculum data.

Every course is a dict with ordered lessons. Lesson content is stored as HTML
fragments rendered with |safe in templates. Challenges are validated in the
browser by running the learner's code in Pyodide and either comparing stdout
to `expected_output` or executing `tests` (assert-based) after their code.
"""

COURSES = [
    # ══════════════════════════════════════════════════════════════════
    # COURSE 1 — PYTHON FUNDAMENTALS
    # ══════════════════════════════════════════════════════════════════
    {
        "slug": "python-fundamentals",
        "title": "Python Fundamentals",
        "tagline": "Zero to confident: syntax, variables, logic and loops.",
        "level": "Beginner",
        "color": "#22d3ee",
        "icon": "🐍",
        "description": "Your very first steps in Python. No experience needed — by the end you will read and write real Python programs, understand variables, make decisions with conditionals and repeat work with loops.",
        "lessons": [
            {
                "slug": "hello-python",
                "title": "Hello, Python!",
                "minutes": 8, "xp": 20,
                "content": """
<p><strong>Python</strong> is the world's most popular programming language — used by NASA, Netflix, Instagram and millions of developers. It reads almost like English, which makes it the perfect first language.</p>
<p>The <code>print()</code> function displays text on the screen. Text wrapped in quotes is called a <strong>string</strong>:</p>
<p>Lines starting with <code>#</code> are <strong>comments</strong> — notes for humans that Python ignores completely. Use them to explain <em>why</em> your code does something.</p>
<ul>
<li><code>print("text")</code> — outputs text</li>
<li><code># comment</code> — ignored by Python</li>
<li>You can print several values: <code>print("a", "b")</code> puts a space between them</li>
</ul>
""",
                "example": '# This is a comment - Python skips it\nprint("Hello, world!")\nprint("Python is", "awesome")',
                "challenge": {
                    "prompt": "Print exactly two lines: first <code>Hello, Python!</code> and then <code>I am learning to code</code>.",
                    "starter": "# Write your two print statements below\n",
                    "expected_output": "Hello, Python!\nI am learning to code",
                    "hint": "Use two separate print() calls. Match spelling and capitalisation exactly.",
                    "solution": 'print("Hello, Python!")\nprint("I am learning to code")',
                },
                "quiz": [
                    {"q": "Which line correctly prints text in Python?",
                     "options": ['print "hi"', 'print("hi")', 'echo("hi")', 'console.log("hi")'],
                     "answer": 1, "explain": "Python 3 requires parentheses: print(\"hi\")."},
                    {"q": "What does the # symbol do?",
                     "options": ["Starts a comment Python ignores", "Prints a hashtag", "Imports a module", "Causes an error"],
                     "answer": 0, "explain": "# begins a comment — a human-readable note that Python skips."},
                ],
            },
            {
                "slug": "variables-and-types",
                "title": "Variables & Data Types",
                "minutes": 12, "xp": 20,
                "content": """
<p>A <strong>variable</strong> is a named box that stores a value. You create one with <code>=</code> (the assignment operator):</p>
<p>Python has four essential basic types:</p>
<ul>
<li><code>str</code> — text: <code>"hello"</code></li>
<li><code>int</code> — whole numbers: <code>42</code></li>
<li><code>float</code> — decimals: <code>3.14</code></li>
<li><code>bool</code> — truth values: <code>True</code> / <code>False</code></li>
</ul>
<p>Use <code>type()</code> to check what type a value is. Variable names should be lowercase with underscores: <code>user_age</code>, not <code>UserAge</code>. Python is <em>dynamically typed</em> — a variable can hold any type, and you never declare the type up front.</p>
""",
                "example": 'name = "Ada"\nage = 36\nheight = 1.7\nis_coder = True\n\nprint(name, age)\nprint(type(age))',
                "challenge": {
                    "prompt": "Create a variable <code>language</code> with the value <code>\"Python\"</code> and a variable <code>year</code> with the value <code>1991</code>. Then print them both on one line with a single <code>print</code>, producing <code>Python 1991</code>.",
                    "starter": "# Create the variables, then print them\n",
                    "expected_output": "Python 1991",
                    "hint": "print(language, year) automatically separates values with a space.",
                    "solution": 'language = "Python"\nyear = 1991\nprint(language, year)',
                },
                "quiz": [
                    {"q": "What type is the value 3.14?",
                     "options": ["int", "str", "float", "bool"],
                     "answer": 2, "explain": "Numbers with a decimal point are floats."},
                    {"q": "Which is a valid Python variable name?",
                     "options": ["2cool", "user-name", "user_name", "class"],
                     "answer": 2, "explain": "Names can't start with digits, contain hyphens, or be reserved keywords like class."},
                ],
            },
            {
                "slug": "numbers-and-math",
                "title": "Numbers & Math",
                "minutes": 10, "xp": 20,
                "content": """
<p>Python is a superb calculator. The core operators:</p>
<ul>
<li><code>+ - * /</code> — the classics (<code>/</code> always gives a float)</li>
<li><code>//</code> — floor division (drops the remainder): <code>7 // 2</code> → <code>3</code></li>
<li><code>%</code> — modulo (the remainder): <code>7 % 2</code> → <code>1</code></li>
<li><code>**</code> — power: <code>2 ** 10</code> → <code>1024</code></li>
</ul>
<p>Shorthand operators update a variable in place: <code>score += 10</code> means <code>score = score + 10</code>.</p>
<p>The modulo operator is secretly one of the most useful in programming — <code>x % 2 == 0</code> is the classic test for an even number.</p>
""",
                "example": "price = 19.99\nquantity = 3\ntotal = price * quantity\nprint(total)\n\nprint(17 // 5)   # 3\nprint(17 % 5)    # 2\nprint(2 ** 8)    # 256",
                "challenge": {
                    "prompt": "A cinema ticket costs 12 euros. Calculate and print the cost of 7 tickets, then print the remainder when 100 is divided by 7. Expected output is <code>84</code> then <code>2</code>.",
                    "starter": "ticket_price = 12\n# your code here\n",
                    "expected_output": "84\n2",
                    "hint": "Multiplication first, then use the % operator for the remainder.",
                    "solution": "ticket_price = 12\nprint(ticket_price * 7)\nprint(100 % 7)",
                },
                "quiz": [
                    {"q": "What does 10 % 3 evaluate to?",
                     "options": ["3", "1", "3.33", "0"],
                     "answer": 1, "explain": "% gives the remainder: 10 divided by 3 is 3 remainder 1."},
                    {"q": "What is the result type of 8 / 2?",
                     "options": ["int (4)", "float (4.0)", "str ('4')", "It errors"],
                     "answer": 1, "explain": "True division / always returns a float, even when it divides evenly."},
                ],
            },
            {
                "slug": "strings",
                "title": "Strings & f-strings",
                "minutes": 14, "xp": 25,
                "content": """
<p>Strings are sequences of characters. You can combine, repeat, measure and transform them:</p>
<ul>
<li><code>"py" + "thon"</code> — concatenation → <code>"python"</code></li>
<li><code>len(s)</code> — length</li>
<li><code>s.upper()</code>, <code>s.lower()</code>, <code>s.strip()</code>, <code>s.replace(a, b)</code> — transformations</li>
<li><code>s[0]</code> — first character (indexes start at 0!), <code>s[-1]</code> — last</li>
</ul>
<p>The modern way to build strings is the <strong>f-string</strong> — put <code>f</code> before the quote and drop variables inside <code>{}</code>:</p>
<p>f-strings can hold any expression: <code>f"{price * 2:.2f}"</code> even formats to 2 decimal places. Master f-strings early — you will use them in every program you ever write.</p>
""",
                "example": 'name = "Grace"\nlang = "python"\n\nprint(lang.upper())          # PYTHON\nprint(len(lang))             # 6\nprint(f"Hi {name}, you know {lang.title()}!")',
                "challenge": {
                    "prompt": "Given the variables in the starter code, use an f-string to print exactly: <code>Alan has completed 5 courses</code>",
                    "starter": 'student = "Alan"\ncourses = 5\n# print using an f-string\n',
                    "expected_output": "Alan has completed 5 courses",
                    "hint": 'f"{student} has completed {courses} courses"',
                    "solution": 'student = "Alan"\ncourses = 5\nprint(f"{student} has completed {courses} courses")',
                },
                "quiz": [
                    {"q": 'What does "hello"[1] return?',
                     "options": ["'h'", "'e'", "'l'", "An error"],
                     "answer": 1, "explain": "Indexing starts at 0, so index 1 is the second character: 'e'."},
                    {"q": 'What does f"{2 + 3}" evaluate to?',
                     "options": ['"2 + 3"', '"5"', "5", "SyntaxError"],
                     "answer": 1, "explain": "f-strings evaluate the expression inside {} and insert the result as text."},
                ],
            },
            {
                "slug": "conditionals",
                "title": "Making Decisions: if / elif / else",
                "minutes": 14, "xp": 25,
                "content": """
<p>Programs become intelligent when they can <strong>choose</strong>. Python decides with <code>if</code>, <code>elif</code> and <code>else</code>:</p>
<p>Comparison operators produce booleans: <code>==</code> (equal), <code>!=</code> (not equal), <code>&lt;</code>, <code>&gt;</code>, <code>&lt;=</code>, <code>&gt;=</code>. Combine conditions with <code>and</code>, <code>or</code>, <code>not</code>.</p>
<p><strong>Indentation is the syntax.</strong> The indented block under an <code>if</code> only runs when the condition is <code>True</code>. Python convention is 4 spaces.</p>
<ul>
<li><code>if</code> — checked first</li>
<li><code>elif</code> — checked only if everything above was False (you can chain many)</li>
<li><code>else</code> — the fallback, runs if nothing matched</li>
</ul>
""",
                "example": 'score = 87\n\nif score >= 90:\n    print("A grade")\nelif score >= 80:\n    print("B grade")\nelse:\n    print("Keep practising")',
                "challenge": {
                    "prompt": "The starter defines <code>temperature = 31</code>. Print <code>Hot</code> if it is above 28, <code>Mild</code> if it is above 15 (but not hot), otherwise <code>Cold</code>.",
                    "starter": "temperature = 31\n# your if / elif / else here\n",
                    "expected_output": "Hot",
                    "hint": "Check the hottest condition first: if temperature > 28.",
                    "solution": 'temperature = 31\nif temperature > 28:\n    print("Hot")\nelif temperature > 15:\n    print("Mild")\nelse:\n    print("Cold")',
                },
                "quiz": [
                    {"q": "Which operator tests equality?",
                     "options": ["=", "==", "===", "eq"],
                     "answer": 1, "explain": "= assigns; == compares. Python has no ===."},
                    {"q": "When does an elif branch run?",
                     "options": ["Always", "Only if its condition is True AND all previous conditions were False", "Only if the if was True", "Never"],
                     "answer": 1, "explain": "elif is only even checked after every earlier branch failed."},
                ],
            },
            {
                "slug": "loops",
                "title": "Loops: for & while",
                "minutes": 16, "xp": 30,
                "content": """
<p>Loops let you repeat work without repeating code — the superpower that makes computers useful.</p>
<p><strong><code>for</code> loops</strong> walk through a sequence. <code>range(5)</code> produces 0,1,2,3,4 (start at 0, stop <em>before</em> 5). <code>range(1, 6)</code> gives 1–5.</p>
<p><strong><code>while</code> loops</strong> repeat as long as a condition stays True — perfect when you don't know how many repetitions you need.</p>
<ul>
<li><code>break</code> — exit the loop immediately</li>
<li><code>continue</code> — skip to the next iteration</li>
<li>Beware infinite while loops — make sure something changes the condition!</li>
</ul>
""",
                "example": 'for i in range(1, 4):\n    print(f"Round {i}")\n\ncountdown = 3\nwhile countdown > 0:\n    print(countdown)\n    countdown -= 1\nprint("Lift off!")',
                "challenge": {
                    "prompt": "Use a for loop with <code>range</code> to print the squares of the numbers 1 through 5, one per line (1, 4, 9, 16, 25).",
                    "starter": "# loop from 1 to 5 and print each square\n",
                    "expected_output": "1\n4\n9\n16\n25",
                    "hint": "range(1, 6) gives 1..5; square with i ** 2.",
                    "solution": "for i in range(1, 6):\n    print(i ** 2)",
                },
                "quiz": [
                    {"q": "What numbers does range(3) produce?",
                     "options": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "3"],
                     "answer": 1, "explain": "range starts at 0 and stops before the end value."},
                    {"q": "What does break do inside a loop?",
                     "options": ["Pauses the program", "Skips one iteration", "Exits the loop immediately", "Restarts the loop"],
                     "answer": 2, "explain": "break jumps straight out of the nearest enclosing loop."},
                ],
            },
            {
                "slug": "fizzbuzz-project",
                "title": "Mini Project: FizzBuzz",
                "minutes": 15, "xp": 40,
                "content": """
<p>Time to combine everything — variables, math, conditionals and loops — into the most famous beginner program (and a real interview question!): <strong>FizzBuzz</strong>.</p>
<p>The rules, for each number from 1 to n:</p>
<ul>
<li>Divisible by 3 <em>and</em> 5 → print <code>FizzBuzz</code></li>
<li>Divisible by only 3 → print <code>Fizz</code></li>
<li>Divisible by only 5 → print <code>Buzz</code></li>
<li>Otherwise → print the number itself</li>
</ul>
<p><strong>Key insight:</strong> check the "divisible by both" case <em>first</em> — if you check 3 alone first, 15 would print Fizz and never reach the FizzBuzz branch. Order of conditions matters.</p>
""",
                "example": 'n = 6\nif n % 3 == 0:\n    print("divisible by 3")\nif n % 5 == 0:\n    print("divisible by 5")',
                "challenge": {
                    "prompt": "Write FizzBuzz for the numbers 1 to 15, printing one result per line.",
                    "starter": "for i in range(1, 16):\n    # your conditions here\n    pass\n",
                    "expected_output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz",
                    "hint": "Test i % 15 == 0 first (or i % 3 == 0 and i % 5 == 0), then % 3, then % 5, else print(i). Remove the pass line.",
                    "solution": 'for i in range(1, 16):\n    if i % 15 == 0:\n        print("FizzBuzz")\n    elif i % 3 == 0:\n        print("Fizz")\n    elif i % 5 == 0:\n        print("Buzz")\n    else:\n        print(i)',
                },
                "quiz": [
                    {"q": "Why must the 'divisible by both' check come first?",
                     "options": ["It's faster", "Otherwise 15 matches the %3 branch first and prints Fizz", "Python requires it", "It doesn't matter"],
                     "answer": 1, "explain": "if/elif chains stop at the first match, so the most specific condition goes first."},
                ],
            },
        ],
    },

    # ══════════════════════════════════════════════════════════════════
    # COURSE 2 — DATA STRUCTURES
    # ══════════════════════════════════════════════════════════════════
    {
        "slug": "data-structures",
        "title": "Data Structures",
        "tagline": "Lists, dictionaries, tuples, sets — organise data like a pro.",
        "level": "Beginner",
        "color": "#a78bfa",
        "icon": "📦",
        "description": "Real programs manage collections of data. Master Python's four built-in containers, slicing, and the elegant comprehension syntax that sets Python apart from every other language.",
        "lessons": [
            {
                "slug": "lists",
                "title": "Lists: Your First Collection",
                "minutes": 12, "xp": 20,
                "content": """
<p>A <strong>list</strong> stores an ordered collection of items — any types, any length, changeable at any time:</p>
<ul>
<li><code>fruits = ["apple", "banana", "cherry"]</code></li>
<li><code>fruits[0]</code> → <code>"apple"</code> (index from 0), <code>fruits[-1]</code> → last item</li>
<li><code>fruits.append("kiwi")</code> — add to the end</li>
<li><code>len(fruits)</code> — how many items</li>
<li><code>"apple" in fruits</code> → <code>True</code> — membership test</li>
</ul>
<p>Loop over a list directly — no indexes needed: <code>for fruit in fruits:</code>. This is the Pythonic way.</p>
""",
                "example": 'scores = [88, 92, 79]\nscores.append(95)\nprint(scores)\nprint(len(scores))\n\nfor s in scores:\n    print(s)',
                "challenge": {
                    "prompt": "Create a list <code>langs</code> containing <code>\"Python\"</code>, <code>\"SQL\"</code> and <code>\"JavaScript\"</code>. Append <code>\"Rust\"</code>, then print the list's length and its last item.",
                    "starter": "# build the list, append, then print\n",
                    "expected_output": "4\nRust",
                    "hint": "print(len(langs)) then print(langs[-1]).",
                    "solution": 'langs = ["Python", "SQL", "JavaScript"]\nlangs.append("Rust")\nprint(len(langs))\nprint(langs[-1])',
                },
                "quiz": [
                    {"q": "What is nums[-1] for nums = [4, 5, 6]?",
                     "options": ["4", "5", "6", "An error"],
                     "answer": 2, "explain": "Negative indexes count from the end; -1 is the last element."},
                    {"q": "Which method adds an item to the end of a list?",
                     "options": ["add()", "push()", "append()", "insert()"],
                     "answer": 2, "explain": "append() adds to the end. insert(i, x) adds at a position."},
                ],
            },
            {
                "slug": "slicing-and-methods",
                "title": "Slicing & List Methods",
                "minutes": 14, "xp": 25,
                "content": """
<p><strong>Slicing</strong> extracts sub-lists with <code>list[start:stop:step]</code> — start included, stop excluded:</p>
<ul>
<li><code>nums[1:3]</code> — items at index 1 and 2</li>
<li><code>nums[:2]</code> — first two; <code>nums[2:]</code> — everything from index 2</li>
<li><code>nums[::-1]</code> — the classic reverse trick</li>
</ul>
<p>Essential methods and functions: <code>sorted(nums)</code> (returns a new sorted list), <code>nums.sort()</code> (sorts in place), <code>sum(nums)</code>, <code>min(nums)</code>, <code>max(nums)</code>, <code>nums.count(x)</code>, <code>nums.remove(x)</code>, <code>nums.pop()</code>.</p>
<p>Strings slice exactly the same way: <code>"python"[0:2]</code> → <code>"py"</code>.</p>
""",
                "example": "nums = [30, 10, 40, 20]\nprint(nums[1:3])      # [10, 40]\nprint(sorted(nums))   # [10, 20, 30, 40]\nprint(sum(nums))      # 100\nprint(nums[::-1])     # [20, 40, 10, 30]",
                "challenge": {
                    "prompt": "Given the starter list, print: (1) the first three items as a slice, (2) the list reversed, (3) the sum of all items.",
                    "starter": "data = [5, 3, 8, 1, 9]\n# three prints\n",
                    "expected_output": "[5, 3, 8]\n[9, 1, 8, 3, 5]\n26",
                    "hint": "data[:3], data[::-1], sum(data).",
                    "solution": "data = [5, 3, 8, 1, 9]\nprint(data[:3])\nprint(data[::-1])\nprint(sum(data))",
                },
                "quiz": [
                    {"q": 'What is "python"[2:4]?',
                     "options": ['"th"', '"yt"', '"tho"', '"ho"'],
                     "answer": 0, "explain": "Indexes 2 and 3 → 't' and 'h'. The stop index is excluded."},
                    {"q": "Difference between sorted(x) and x.sort()?",
                     "options": ["No difference", "sorted returns a new list; .sort() modifies in place and returns None", ".sort() is faster only", "sorted only works on numbers"],
                     "answer": 1, "explain": "A very common gotcha: x.sort() returns None, so never write y = x.sort()."},
                ],
            },
            {
                "slug": "dictionaries",
                "title": "Dictionaries: Key → Value",
                "minutes": 15, "xp": 30,
                "content": """
<p>A <strong>dictionary</strong> maps keys to values — the single most important data structure in Python. Think of a real dictionary: look up a word (key), get a definition (value).</p>
<ul>
<li><code>user = {"name": "Ada", "age": 36}</code></li>
<li><code>user["name"]</code> → <code>"Ada"</code>; <code>user["age"] = 37</code> updates; new keys are added the same way</li>
<li><code>user.get("email", "n/a")</code> — safe lookup with a default (no crash if missing)</li>
<li><code>"name" in user</code> — check if a key exists</li>
</ul>
<p>Loop over pairs with <code>.items()</code>: <code>for key, value in user.items():</code>. JSON — the language of web APIs — maps directly to Python dicts, which is why they matter so much.</p>
""",
                "example": 'stock = {"apples": 5, "pears": 12}\nstock["apples"] += 1\nstock["plums"] = 3\n\nfor fruit, qty in stock.items():\n    print(f"{fruit}: {qty}")',
                "challenge": {
                    "prompt": "Create a dict <code>capitals</code> mapping <code>\"France\"</code>→<code>\"Paris\"</code> and <code>\"Japan\"</code>→<code>\"Tokyo\"</code>. Add <code>\"Italy\"</code>→<code>\"Rome\"</code>, then print the capital of Japan and the number of entries.",
                    "starter": "# build the dict, add Italy, print two lines\n",
                    "expected_output": "Tokyo\n3",
                    "hint": "print(capitals[\"Japan\"]) then print(len(capitals)).",
                    "solution": 'capitals = {"France": "Paris", "Japan": "Tokyo"}\ncapitals["Italy"] = "Rome"\nprint(capitals["Japan"])\nprint(len(capitals))',
                },
                "quiz": [
                    {"q": "What happens when you read a missing key with d[\"nope\"]?",
                     "options": ["Returns None", "Returns 0", "Raises KeyError", "Creates the key"],
                     "answer": 2, "explain": "Direct access on a missing key raises KeyError; .get() returns None (or your default) instead."},
                    {"q": "Which loops over both keys and values?",
                     "options": ["for k in d:", "for k, v in d.items():", "for v in d.values():", "for k, v in d:"],
                     "answer": 1, "explain": ".items() yields (key, value) pairs you can unpack."},
                ],
            },
            {
                "slug": "tuples-and-sets",
                "title": "Tuples & Sets",
                "minutes": 12, "xp": 25,
                "content": """
<p><strong>Tuples</strong> are immutable lists — once created, they cannot change: <code>point = (3, 5)</code>. Use them for fixed groups of values. <strong>Tuple unpacking</strong> is beautiful Python: <code>x, y = point</code>, and swapping is just <code>a, b = b, a</code>.</p>
<p><strong>Sets</strong> hold unique values with no order: <code>tags = {"python", "web"}</code>. Adding a duplicate does nothing. Sets are perfect for:</p>
<ul>
<li>De-duplicating: <code>set([1, 2, 2, 3])</code> → <code>{1, 2, 3}</code></li>
<li>Lightning-fast membership tests: <code>x in my_set</code></li>
<li>Set math: <code>a & b</code> (intersection), <code>a | b</code> (union), <code>a - b</code> (difference)</li>
</ul>
""",
                "example": 'point = (3, 5)\nx, y = point\nprint(x + y)\n\nvisitors = ["ana", "bo", "ana", "cy", "bo"]\nunique = set(visitors)\nprint(len(unique))',
                "challenge": {
                    "prompt": "The starter has a list with duplicates. Print the number of unique values in it, then print whether <code>7</code> is one of them (<code>True</code>/<code>False</code>).",
                    "starter": "nums = [1, 4, 7, 4, 1, 9, 7, 7]\n# your code\n",
                    "expected_output": "4\nTrue",
                    "hint": "unique = set(nums); print(len(unique)); print(7 in unique).",
                    "solution": "nums = [1, 4, 7, 4, 1, 9, 7, 7]\nunique = set(nums)\nprint(len(unique))\nprint(7 in unique)",
                },
                "quiz": [
                    {"q": "What happens if you try point[0] = 9 on a tuple?",
                     "options": ["It works", "TypeError — tuples are immutable", "It creates a new tuple", "Returns None"],
                     "answer": 1, "explain": "Tuples can't be modified after creation — that's their entire point."},
                    {"q": "What is {1, 2, 3} & {2, 3, 4}?",
                     "options": ["{1, 2, 3, 4}", "{2, 3}", "{1, 4}", "TypeError"],
                     "answer": 1, "explain": "& is set intersection — elements present in both."},
                ],
            },
            {
                "slug": "comprehensions",
                "title": "List Comprehensions",
                "minutes": 14, "xp": 30,
                "content": """
<p><strong>Comprehensions</strong> build lists in a single expressive line — Python's signature feature:</p>
<ul>
<li><code>[x * 2 for x in nums]</code> — transform every item</li>
<li><code>[x for x in nums if x > 0]</code> — filter items</li>
<li><code>[x * 2 for x in nums if x > 0]</code> — filter <em>and</em> transform</li>
</ul>
<p>Read it as: "give me <em>x * 2</em>, for each <em>x</em> in <em>nums</em>, if <em>x > 0</em>". They replace 4-line loop-and-append patterns with one clear line.</p>
<p>Dict comprehensions work too: <code>{w: len(w) for w in words}</code>. Keep comprehensions simple — if it needs two <code>if</code>s and nesting, use a normal loop.</p>
""",
                "example": "nums = [1, 2, 3, 4, 5, 6]\n\nsquares = [n ** 2 for n in nums]\nevens = [n for n in nums if n % 2 == 0]\nprint(squares)\nprint(evens)",
                "challenge": {
                    "prompt": "Using one list comprehension, build a list of the cubes of the odd numbers from 1 to 9, and print it. Expected: <code>[1, 27, 125, 343, 729]</code>",
                    "starter": "# one comprehension over range(1, 10)\n",
                    "expected_output": "[1, 27, 125, 343, 729]",
                    "hint": "[n ** 3 for n in range(1, 10) if n % 2 == 1]",
                    "solution": "cubes = [n ** 3 for n in range(1, 10) if n % 2 == 1]\nprint(cubes)",
                },
                "quiz": [
                    {"q": "What does [c.upper() for c in 'abc'] produce?",
                     "options": ["'ABC'", "['A', 'B', 'C']", "['abc']", "['ABC']"],
                     "answer": 1, "explain": "It iterates over each character and returns a list of results."},
                    {"q": "Where does the if filter go in a comprehension?",
                     "options": ["Before the for", "After the for clause", "Inside brackets first", "Comprehensions can't filter"],
                     "answer": 1, "explain": "[expr for item in seq if condition] — filter comes last."},
                ],
            },
            {
                "slug": "nested-data-project",
                "title": "Mini Project: Gradebook",
                "minutes": 18, "xp": 45,
                "content": """
<p>Real-world data nests: lists of dicts, dicts of lists. A JSON API response is exactly this shape. Let's build a <strong>gradebook</strong> — a list where each student is a dict:</p>
<p><code>students = [{"name": "Ada", "grades": [90, 95]}, ...]</code></p>
<p>Patterns you'll use constantly:</p>
<ul>
<li>Loop the outer list, reach into each dict: <code>for s in students: print(s["name"])</code></li>
<li>Compute per-item stats: <code>sum(s["grades"]) / len(s["grades"])</code></li>
<li>Find the best item by tracking a "best so far" while looping</li>
</ul>
""",
                "example": 'students = [\n    {"name": "Ada", "grades": [90, 95, 92]},\n    {"name": "Alan", "grades": [70, 88, 91]},\n]\nfor s in students:\n    avg = sum(s["grades"]) / len(s["grades"])\n    print(f"{s[\'name\']}: {avg:.1f}")',
                "challenge": {
                    "prompt": "Using the starter data, print each student's name and average (1 decimal, format <code>Name: avg</code>), then print the name of the student with the highest average.",
                    "starter": 'students = [\n    {"name": "Maya", "grades": [80, 90, 100]},\n    {"name": "Leo", "grades": [95, 92, 96]},\n    {"name": "Zoe", "grades": [70, 75, 80]},\n]\n# your code\n',
                    "expected_output": "Maya: 90.0\nLeo: 94.3\nZoe: 75.0\nLeo",
                    "hint": "Track best_name and best_avg while looping; f\"{avg:.1f}\" formats to 1 decimal.",
                    "solution": 'students = [\n    {"name": "Maya", "grades": [80, 90, 100]},\n    {"name": "Leo", "grades": [95, 92, 96]},\n    {"name": "Zoe", "grades": [70, 75, 80]},\n]\nbest_name = ""\nbest_avg = -1\nfor s in students:\n    avg = sum(s["grades"]) / len(s["grades"])\n    print(f"{s[\'name\']}: {avg:.1f}")\n    if avg > best_avg:\n        best_avg = avg\n        best_name = s["name"]\nprint(best_name)',
                },
                "quiz": [
                    {"q": 'For data = [{"a": [1, 2]}], how do you reach the 2?',
                     "options": ['data["a"][1]', 'data[0]["a"][1]', 'data[1]["a"][0]', 'data.a[1]'],
                     "answer": 1, "explain": "First index the list (data[0]), then the dict key, then the inner list."},
                ],
            },
        ],
    },

    # ══════════════════════════════════════════════════════════════════
    # COURSE 3 — FUNCTIONS & OOP
    # ══════════════════════════════════════════════════════════════════
    {
        "slug": "functions-oop",
        "title": "Functions & OOP",
        "tagline": "Write reusable, organised, professional code.",
        "level": "Intermediate",
        "color": "#34d399",
        "icon": "⚙️",
        "description": "Functions turn repeated code into reusable building blocks; classes model the real world. This is where you stop writing scripts and start engineering software.",
        "lessons": [
            {
                "slug": "defining-functions",
                "title": "Defining Functions",
                "minutes": 14, "xp": 25,
                "content": """
<p>A <strong>function</strong> is a named, reusable block of code. Define with <code>def</code>, hand data in through <strong>parameters</strong>, get data back with <strong>return</strong>:</p>
<ul>
<li><code>def greet(name):</code> — definition with one parameter</li>
<li><code>return</code> sends a value back to the caller (and ends the function)</li>
<li>A function without <code>return</code> returns <code>None</code></li>
<li><code>print</code> shows a value; <code>return</code> hands it back — they are not the same!</li>
</ul>
<p>Good functions do <em>one thing</em> and are named with verbs: <code>calculate_total</code>, <code>send_email</code>, <code>is_valid</code>.</p>
""",
                "example": 'def area(width, height):\n    return width * height\n\nprint(area(3, 4))\n\nresult = area(5, 2)\nprint(result + 1)',
                "challenge": {
                    "prompt": "Write a function <code>celsius_to_fahrenheit(c)</code> that returns <code>c * 9 / 5 + 32</code>. Then print the result of converting 0, 25 and 100.",
                    "starter": "def celsius_to_fahrenheit(c):\n    # return the converted value\n    pass\n\n# print three conversions\n",
                    "expected_output": "32.0\n77.0\n212.0",
                    "hint": "Replace pass with a return statement, then call the function inside print().",
                    "solution": "def celsius_to_fahrenheit(c):\n    return c * 9 / 5 + 32\n\nprint(celsius_to_fahrenheit(0))\nprint(celsius_to_fahrenheit(25))\nprint(celsius_to_fahrenheit(100))",
                },
                "quiz": [
                    {"q": "What does a function return if it has no return statement?",
                     "options": ["0", "The last expression", "None", "An error"],
                     "answer": 2, "explain": "No return (or bare return) means the function returns None."},
                    {"q": "What's the difference between print and return?",
                     "options": ["None, they're aliases", "print displays; return hands a value back to the caller", "return displays; print hands back", "return only works with numbers"],
                     "answer": 1, "explain": "Returned values can be stored and reused; printed values are just shown."},
                ],
            },
            {
                "slug": "arguments",
                "title": "Default, Keyword, *args & **kwargs",
                "minutes": 15, "xp": 30,
                "content": """
<p>Python's argument system is wonderfully flexible:</p>
<ul>
<li><strong>Defaults</strong>: <code>def greet(name, punct="!")</code> — callers may omit <code>punct</code></li>
<li><strong>Keyword args</strong>: <code>greet(punct="?", name="Bo")</code> — order-free, self-documenting</li>
<li><strong><code>*args</code></strong>: collects extra positional args into a tuple — <code>def total(*nums)</code></li>
<li><strong><code>**kwargs</code></strong>: collects extra keyword args into a dict</li>
</ul>
<p><strong>Classic trap:</strong> never use a mutable default like <code>def f(items=[])</code> — the list is created once and shared between calls. Use <code>items=None</code> and create inside.</p>
""",
                "example": 'def power(base, exponent=2):\n    return base ** exponent\n\nprint(power(5))        # uses default: 25\nprint(power(2, 10))    # 1024\n\ndef total(*nums):\n    return sum(nums)\n\nprint(total(1, 2, 3, 4))',
                "challenge": {
                    "prompt": "Write <code>describe(name, role=\"student\")</code> that returns <code>\"{name} is a {role}\"</code>. Print <code>describe(\"Ada\")</code> and <code>describe(\"Grace\", role=\"admiral\")</code>.",
                    "starter": "# define describe, then two prints\n",
                    "expected_output": "Ada is a student\nGrace is a admiral",
                    "hint": "Use an f-string in the return.",
                    "solution": 'def describe(name, role="student"):\n    return f"{name} is a {role}"\n\nprint(describe("Ada"))\nprint(describe("Grace", role="admiral"))',
                },
                "quiz": [
                    {"q": "What does *args collect?",
                     "options": ["Keyword arguments into a dict", "Extra positional arguments into a tuple", "All arguments into a list", "Pointers"],
                     "answer": 1, "explain": "*args gathers surplus positional arguments as a tuple; **kwargs gathers keyword ones as a dict."},
                    {"q": "Why is def f(x, items=[]) dangerous?",
                     "options": ["Syntax error", "The default list is shared across every call", "Lists can't be defaults", "It's fine"],
                     "answer": 1, "explain": "Defaults are evaluated once at definition time — the same list object persists between calls."},
                ],
            },
            {
                "slug": "scope-and-lambda",
                "title": "Scope, Lambda & Higher-Order Functions",
                "minutes": 14, "xp": 30,
                "content": """
<p><strong>Scope</strong>: variables created inside a function are <em>local</em> — they vanish when it returns. Functions can read outer variables but assignment creates a new local one (unless you use <code>global</code>, which you should avoid).</p>
<p><strong>Lambdas</strong> are tiny anonymous functions: <code>lambda x: x * 2</code>. Their killer use is as <em>sort keys</em>:</p>
<ul>
<li><code>sorted(words, key=len)</code> — sort by length</li>
<li><code>sorted(users, key=lambda u: u["age"])</code> — sort dicts by a field</li>
<li><code>max(nums, key=abs)</code> — max by absolute value</li>
</ul>
<p>Functions are values in Python — you can pass them around like any other object. That idea powers decorators, callbacks and most frameworks.</p>
""",
                "example": 'words = ["banana", "fig", "apple"]\nprint(sorted(words, key=len))\n\nusers = [{"name": "Bo", "age": 25}, {"name": "Ana", "age": 19}]\nyoungest = min(users, key=lambda u: u["age"])\nprint(youngest["name"])',
                "challenge": {
                    "prompt": "Sort the starter list of (name, score) tuples by score from highest to lowest and print each name on its own line.",
                    "starter": 'players = [("Rio", 12), ("Kai", 31), ("Ash", 22)]\n# sort by score descending, print names\n',
                    "expected_output": "Kai\nAsh\nRio",
                    "hint": "sorted(players, key=lambda p: p[1], reverse=True)",
                    "solution": 'players = [("Rio", 12), ("Kai", 31), ("Ash", 22)]\nfor name, score in sorted(players, key=lambda p: p[1], reverse=True):\n    print(name)',
                },
                "quiz": [
                    {"q": "What is lambda x: x + 1?",
                     "options": ["A syntax error", "An anonymous function that adds 1", "A loop", "A string"],
                     "answer": 1, "explain": "lambda creates a small unnamed function; this one returns its argument plus one."},
                    {"q": "sorted(names, key=len) sorts by…",
                     "options": ["Alphabet", "String length", "Reverse alphabet", "Memory address"],
                     "answer": 1, "explain": "key=len calls len() on each item and sorts by those values."},
                ],
            },
            {
                "slug": "classes-and-objects",
                "title": "Classes & Objects",
                "minutes": 18, "xp": 35,
                "content": """
<p>A <strong>class</strong> is a blueprint; an <strong>object</strong> (instance) is a thing built from it. Classes bundle <em>data</em> (attributes) with <em>behaviour</em> (methods):</p>
<ul>
<li><code>__init__</code> — the constructor, runs when you create an instance</li>
<li><code>self</code> — the instance itself; every method receives it first</li>
<li><code>self.name = name</code> — stores data on the instance</li>
</ul>
<p>Think of <code>Dog</code> as the cookie cutter and each <code>Dog("Rex")</code> as a cookie. Classes shine when data and the functions that operate on it belong together — a bank account with balance + deposit/withdraw, a player with health + damage logic.</p>
""",
                "example": 'class Dog:\n    def __init__(self, name):\n        self.name = name\n        self.tricks = []\n\n    def learn(self, trick):\n        self.tricks.append(trick)\n\nrex = Dog("Rex")\nrex.learn("sit")\nprint(rex.name, rex.tricks)',
                "challenge": {
                    "prompt": "Create a class <code>BankAccount</code> with <code>__init__(self, owner)</code> starting balance 0, a <code>deposit(amount)</code> method, and a <code>report()</code> method returning <code>\"{owner}: {balance}\"</code>. Create an account for <code>\"Simas\"</code>, deposit 50 then 25, and print the report.",
                    "starter": "class BankAccount:\n    # __init__, deposit, report\n    pass\n\n# create, deposit twice, print report\n",
                    "expected_output": "Simas: 75",
                    "hint": "self.balance = 0 in __init__; deposit does self.balance += amount.",
                    "solution": 'class BankAccount:\n    def __init__(self, owner):\n        self.owner = owner\n        self.balance = 0\n\n    def deposit(self, amount):\n        self.balance += amount\n\n    def report(self):\n        return f"{self.owner}: {self.balance}"\n\nacct = BankAccount("Simas")\nacct.deposit(50)\nacct.deposit(25)\nprint(acct.report())',
                },
                "quiz": [
                    {"q": "What is self in a method?",
                     "options": ["A keyword like this in JS", "The instance the method was called on", "The class itself", "A global variable"],
                     "answer": 1, "explain": "self is just the first parameter, automatically bound to the instance."},
                    {"q": "When does __init__ run?",
                     "options": ["When the file is imported", "When the class is defined", "Each time an instance is created", "Never automatically"],
                     "answer": 2, "explain": "__init__ is the constructor, called for every new instance."},
                ],
            },
            {
                "slug": "inheritance",
                "title": "Inheritance & super()",
                "minutes": 15, "xp": 35,
                "content": """
<p><strong>Inheritance</strong> lets a class reuse and extend another: <code>class Cat(Animal)</code> means Cat gets everything Animal has, and can add or override.</p>
<ul>
<li>Child classes inherit all methods and attributes</li>
<li><strong>Override</strong> a method by redefining it with the same name</li>
<li><code>super().__init__(...)</code> — call the parent's constructor from the child's</li>
<li><code>isinstance(obj, Animal)</code> — True for Animal <em>and</em> any subclass instance</li>
</ul>
<p>Rule of thumb: inheritance models an <em>is-a</em> relationship (a Cat <em>is an</em> Animal). If it's a <em>has-a</em> relationship, use composition (store the object as an attribute) instead.</p>
""",
                "example": 'class Animal:\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        return "..."\n\nclass Cat(Animal):\n    def speak(self):\n        return "Meow"\n\nfelix = Cat("Felix")\nprint(felix.name, felix.speak())',
                "challenge": {
                    "prompt": "Build <code>Shape</code> with <code>__init__(self, name)</code> and a method <code>area()</code> returning 0. Then <code>Square(Shape)</code> whose <code>__init__(self, side)</code> calls <code>super().__init__(\"square\")</code> and overrides <code>area()</code>. Create a Square with side 6 and print its name and area.",
                    "starter": "# Shape and Square classes, then create and print\n",
                    "expected_output": "square 36",
                    "hint": "print(sq.name, sq.area())",
                    "solution": 'class Shape:\n    def __init__(self, name):\n        self.name = name\n\n    def area(self):\n        return 0\n\nclass Square(Shape):\n    def __init__(self, side):\n        super().__init__("square")\n        self.side = side\n\n    def area(self):\n        return self.side ** 2\n\nsq = Square(6)\nprint(sq.name, sq.area())',
                },
                "quiz": [
                    {"q": "What does super().__init__() do?",
                     "options": ["Creates a superclass", "Calls the parent class's constructor", "Deletes the parent", "Nothing"],
                     "answer": 1, "explain": "It runs the parent's __init__ so inherited attributes get set up."},
                ],
            },
            {
                "slug": "dunder-project",
                "title": "Mini Project: Playing Cards with Dunders",
                "minutes": 18, "xp": 45,
                "content": """
<p><strong>Dunder</strong> (double-underscore) methods let your objects plug into Python's own syntax:</p>
<ul>
<li><code>__str__</code> — what <code>print(obj)</code> shows</li>
<li><code>__eq__</code> — makes <code>==</code> meaningful for your type</li>
<li><code>__lt__</code> — enables <code>&lt;</code> and therefore <code>sorted()</code></li>
<li><code>__len__</code> — makes <code>len(obj)</code> work</li>
</ul>
<p>This is why <code>len("abc")</code>, <code>len([1,2])</code> and <code>len(my_deck)</code> can all work — each type implements <code>__len__</code>. Design your classes to feel native and they become a joy to use.</p>
""",
                "example": 'class Card:\n    def __init__(self, rank):\n        self.rank = rank\n\n    def __str__(self):\n        return f"Card({self.rank})"\n\n    def __lt__(self, other):\n        return self.rank < other.rank\n\nprint(Card(7))\nprint(Card(3) < Card(9))',
                "challenge": {
                    "prompt": "Create a class <code>Deck</code> that stores a list of numbers passed to <code>__init__</code>, implements <code>__len__</code>, and a method <code>top()</code> returning the last number. Create <code>Deck([2, 9, 4])</code>, print its length and its top card.",
                    "starter": "class Deck:\n    # __init__, __len__, top\n    pass\n\n# create and print\n",
                    "expected_output": "3\n4",
                    "hint": "__len__ must return len(self.cards); top() returns self.cards[-1].",
                    "solution": "class Deck:\n    def __init__(self, cards):\n        self.cards = cards\n\n    def __len__(self):\n        return len(self.cards)\n\n    def top(self):\n        return self.cards[-1]\n\nd = Deck([2, 9, 4])\nprint(len(d))\nprint(d.top())",
                },
                "quiz": [
                    {"q": "Which dunder controls what print(obj) displays?",
                     "options": ["__print__", "__str__", "__show__", "__display__"],
                     "answer": 1, "explain": "__str__ returns the human-readable representation used by print()."},
                ],
            },
        ],
    },

    # ══════════════════════════════════════════════════════════════════
    # COURSE 4 — PRACTICAL PYTHON
    # ══════════════════════════════════════════════════════════════════
    {
        "slug": "practical-python",
        "title": "Practical Python",
        "tagline": "Errors, files, modules and the standard library.",
        "level": "Intermediate",
        "color": "#fbbf24",
        "icon": "🛠️",
        "description": "The skills that separate scripts from software: handle failures gracefully, read and write files, organise code into modules, and lean on Python's legendary standard library.",
        "lessons": [
            {
                "slug": "understanding-errors",
                "title": "Reading Tracebacks & Common Errors",
                "minutes": 12, "xp": 25,
                "content": """
<p>Errors are not failures — they're Python <em>telling you exactly what went wrong</em>. Read a traceback bottom-up: the last line names the error, the lines above show where.</p>
<p>The big five you'll meet constantly:</p>
<ul>
<li><code>SyntaxError</code> — Python can't even parse it (missing colon, unclosed quote)</li>
<li><code>NameError</code> — using a variable that doesn't exist (often a typo)</li>
<li><code>TypeError</code> — wrong type: <code>"age: " + 25</code></li>
<li><code>IndexError</code> / <code>KeyError</code> — missing list position / dict key</li>
<li><code>ValueError</code> — right type, bad value: <code>int("hello")</code></li>
</ul>
<p>Pro habit: read the error name and message <em>first</em>, then the line number. 90% of bugs are solved by actually reading the message.</p>
""",
                "example": 'age = 25\n# print("age: " + age)      # TypeError: can\'t add str and int\nprint("age: " + str(age))    # fix: convert first\nprint(f"age: {age}")         # better: f-string',
                "challenge": {
                    "prompt": "The starter code contains two bugs. Fix them so it prints <code>Total: 30</code>.",
                    "starter": 'pric = 10\nquantity = 3\ntotal = price * quantity\nprint("Total: " + total)\n',
                    "expected_output": "Total: 30",
                    "hint": "One NameError (typo), one TypeError (str + int). f-strings fix the second.",
                    "solution": 'price = 10\nquantity = 3\ntotal = price * quantity\nprint(f"Total: {total}")',
                },
                "quiz": [
                    {"q": "int(\"abc\") raises which error?",
                     "options": ["TypeError", "ValueError", "NameError", "SyntaxError"],
                     "answer": 1, "explain": "The type (str) is acceptable but the value can't be converted → ValueError."},
                    {"q": "Where in a traceback is the actual error named?",
                     "options": ["First line", "Middle", "Last line", "It isn't"],
                     "answer": 2, "explain": "The final line has the exception type and message — start reading there."},
                ],
            },
            {
                "slug": "try-except",
                "title": "try / except / finally & raise",
                "minutes": 15, "xp": 30,
                "content": """
<p><strong>Exception handling</strong> lets your program survive failures instead of crashing:</p>
<ul>
<li><code>try:</code> — the risky code</li>
<li><code>except ValueError:</code> — runs only if that error occurred (always catch <em>specific</em> exceptions)</li>
<li><code>else:</code> — runs if <em>no</em> error happened</li>
<li><code>finally:</code> — always runs (cleanup: closing files, connections)</li>
<li><code>raise ValueError("message")</code> — throw your own errors when input is invalid</li>
</ul>
<p>Never write a bare <code>except:</code> that silently swallows everything — it hides real bugs. Catch what you expect, let the rest crash loudly.</p>
""",
                "example": 'def safe_divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return "Cannot divide by zero"\n\nprint(safe_divide(10, 2))\nprint(safe_divide(5, 0))',
                "challenge": {
                    "prompt": "Write <code>to_number(text)</code> that returns <code>int(text)</code>, but returns <code>-1</code> if conversion raises <code>ValueError</code>. Print <code>to_number(\"42\")</code> and <code>to_number(\"oops\")</code>.",
                    "starter": "def to_number(text):\n    # try/except here\n    pass\n\n# two prints\n",
                    "expected_output": "42\n-1",
                    "hint": "try: return int(text)  /  except ValueError: return -1",
                    "solution": 'def to_number(text):\n    try:\n        return int(text)\n    except ValueError:\n        return -1\n\nprint(to_number("42"))\nprint(to_number("oops"))',
                },
                "quiz": [
                    {"q": "When does finally run?",
                     "options": ["Only on success", "Only on error", "Always", "Never"],
                     "answer": 2, "explain": "finally runs no matter what — success, exception, even a return."},
                    {"q": "Why is a bare except: bad practice?",
                     "options": ["Slow", "It catches and hides every error, including bugs and typos", "Syntax error", "It isn't"],
                     "answer": 1, "explain": "It swallows KeyboardInterrupt, NameErrors from typos, everything — debugging nightmare."},
                ],
            },
            {
                "slug": "files",
                "title": "Reading & Writing Files",
                "minutes": 14, "xp": 30,
                "content": """
<p>Files persist data beyond your program's run. The golden pattern is <code>with open(...)</code> — it closes the file automatically, even if an error occurs:</p>
<ul>
<li><code>with open("data.txt", "w") as f:</code> — write mode (creates/overwrites)</li>
<li><code>"a"</code> — append mode; <code>"r"</code> — read (the default)</li>
<li><code>f.write("text")</code> — note: you add your own <code>\\n</code></li>
<li><code>f.read()</code> — whole file; <code>for line in f:</code> — line by line (memory-friendly)</li>
<li><code>line.strip()</code> — remove the trailing newline when reading</li>
</ul>
""",
                "example": 'with open("notes.txt", "w") as f:\n    f.write("line one\\n")\n    f.write("line two\\n")\n\nwith open("notes.txt") as f:\n    for line in f:\n        print(line.strip().upper())',
                "challenge": {
                    "prompt": "Write the numbers 1–5 to a file <code>nums.txt</code>, one per line. Then read it back and print the sum of the numbers.",
                    "starter": '# write 1..5 to nums.txt, then read and sum\n',
                    "expected_output": "15",
                    "hint": "Write f\"{i}\\n\" in a loop; when reading, int(line.strip()) each line.",
                    "solution": 'with open("nums.txt", "w") as f:\n    for i in range(1, 6):\n        f.write(f"{i}\\n")\n\ntotal = 0\nwith open("nums.txt") as f:\n    for line in f:\n        total += int(line.strip())\nprint(total)',
                },
                "quiz": [
                    {"q": "Why prefer `with open(...)` over open()/close()?",
                     "options": ["It's shorter only", "The file is guaranteed to close, even if an exception occurs", "It reads faster", "close() doesn't exist"],
                     "answer": 1, "explain": "The context manager closes the file in all cases — no leaked file handles."},
                    {"q": "Mode \"w\" on an existing file will…",
                     "options": ["Append to it", "Raise an error", "Erase its contents and start fresh", "Open read-only"],
                     "answer": 2, "explain": "\"w\" truncates. Use \"a\" to append."},
                ],
            },
            {
                "slug": "modules",
                "title": "Modules & Imports",
                "minutes": 12, "xp": 25,
                "content": """
<p>A <strong>module</strong> is simply a <code>.py</code> file whose functions you can use elsewhere. Importing keeps projects organised and unlocks Python's ecosystem:</p>
<ul>
<li><code>import math</code> → <code>math.sqrt(16)</code></li>
<li><code>from math import sqrt, pi</code> → <code>sqrt(16)</code> directly</li>
<li><code>import numpy as np</code> — community-standard aliases</li>
<li>Avoid <code>from module import *</code> — nobody can tell where names came from</li>
</ul>
<p>The <code>if __name__ == "__main__":</code> idiom marks code that runs only when the file is executed directly, not when imported — every professional script has it.</p>
""",
                "example": 'import math\nfrom random import seed, randint\n\nprint(math.sqrt(144))\nprint(math.floor(9.81))\nseed(1)              # seed makes random repeatable\nprint(randint(1, 100))',
                "challenge": {
                    "prompt": "Import <code>math</code> and print: the square root of 225, pi rounded to 2 decimals (use <code>round</code>), and <code>math.ceil(4.2)</code>.",
                    "starter": "# import and three prints\n",
                    "expected_output": "15.0\n3.14\n5",
                    "hint": "round(math.pi, 2) gives 3.14.",
                    "solution": "import math\nprint(math.sqrt(225))\nprint(round(math.pi, 2))\nprint(math.ceil(4.2))",
                },
                "quiz": [
                    {"q": "What does `if __name__ == \"__main__\":` check?",
                     "options": ["Python version", "Whether the file is run directly rather than imported", "If main() exists", "Whether it's the first import"],
                     "answer": 1, "explain": "When run directly, __name__ is \"__main__\"; when imported it's the module's name."},
                ],
            },
            {
                "slug": "stdlib-tour",
                "title": "Standard Library Power Tour",
                "minutes": 16, "xp": 35,
                "content": """
<p>Python ships "batteries included" — a huge standard library. The modules you'll reach for weekly:</p>
<ul>
<li><code>json</code> — <code>json.dumps(obj)</code> / <code>json.loads(text)</code>: convert between Python and JSON</li>
<li><code>datetime</code> — dates, times, differences: <code>date.today()</code>, <code>timedelta(days=7)</code></li>
<li><code>random</code> — <code>choice</code>, <code>shuffle</code>, <code>randint</code></li>
<li><code>collections.Counter</code> — count things in one line</li>
<li><code>pathlib.Path</code> — modern file paths</li>
</ul>
<p><code>Counter</code> deserves special love: <code>Counter("mississippi").most_common(2)</code> → <code>[('i', 4), ('s', 4)]</code>. Before writing a loop, ask: "does the stdlib already do this?" It usually does.</p>
""",
                "example": 'import json\nfrom collections import Counter\n\nuser = {"name": "Ada", "tags": ["math", "code"]}\ntext = json.dumps(user)\nprint(text)\nprint(json.loads(text)["tags"][0])\n\nprint(Counter([1, 1, 2, 3, 1]).most_common(1))',
                "challenge": {
                    "prompt": "Use <code>Counter</code> to find the two most common letters in <code>\"abracadabra\"</code> and print each as <code>letter count</code> on its own line.",
                    "starter": "from collections import Counter\n# your code\n",
                    "expected_output": "a 5\nb 2",
                    "hint": "for letter, count in Counter(word).most_common(2):",
                    "solution": 'from collections import Counter\nfor letter, count in Counter("abracadabra").most_common(2):\n    print(letter, count)',
                },
                "quiz": [
                    {"q": "json.loads() converts…",
                     "options": ["Python → JSON string", "JSON string → Python objects", "JSON → file", "Nothing"],
                     "answer": 1, "explain": "loads = 'load string'. dumps goes the other way (Python → JSON text)."},
                ],
            },
        ],
    },

    # ══════════════════════════════════════════════════════════════════
    # COURSE 5 — APIs WITH PYTHON
    # ══════════════════════════════════════════════════════════════════
    {
        "slug": "apis-with-python",
        "title": "APIs with Python",
        "tagline": "Consume and build web APIs — the language of the internet.",
        "level": "Intermediate",
        "color": "#f472b6",
        "icon": "🔌",
        "description": "APIs power every app you use. Learn HTTP from the ground up, master JSON, consume real APIs with requests, and design and build your own REST API with Flask.",
        "lessons": [
            {
                "slug": "what-is-an-api",
                "title": "What Is an API? HTTP Fundamentals",
                "minutes": 12, "xp": 25,
                "content": """
<p>An <strong>API</strong> (Application Programming Interface) is a contract that lets programs talk to each other. Web APIs speak <strong>HTTP</strong> — the same protocol as your browser.</p>
<p>Every HTTP exchange is a <em>request</em> and a <em>response</em>:</p>
<ul>
<li><strong>Methods (verbs)</strong>: <code>GET</code> read, <code>POST</code> create, <code>PUT/PATCH</code> update, <code>DELETE</code> remove</li>
<li><strong>URL</strong>: <code>https://api.site.com/users/42?active=true</code> — path identifies the resource, query params filter</li>
<li><strong>Status codes</strong>: <code>200</code> OK, <code>201</code> Created, <code>404</code> Not Found, <code>400</code> Bad Request, <code>401</code> Unauthorized, <code>500</code> Server Error</li>
<li><strong>Body</strong>: usually JSON data</li>
</ul>
<p>Memory aid for status codes: 2xx = success, 3xx = redirect, 4xx = <em>your</em> mistake, 5xx = <em>their</em> mistake.</p>
""",
                "example": '# An HTTP exchange, conceptually:\nrequest = {"method": "GET", "url": "/api/users/42"}\nresponse = {"status": 200, "body": {"id": 42, "name": "Ada"}}\n\nif response["status"] == 200:\n    print(response["body"]["name"])',
                "challenge": {
                    "prompt": "The starter has a list of (method, status) tuples from an API log. Print how many were successful (status 200–299) and how many were client errors (400–499).",
                    "starter": 'log = [("GET", 200), ("POST", 201), ("GET", 404), ("DELETE", 500), ("PUT", 400), ("GET", 200)]\n# count and print two numbers\n',
                    "expected_output": "3\n2",
                    "hint": "Count with: 200 <= status <= 299. Python lets you chain comparisons.",
                    "solution": 'log = [("GET", 200), ("POST", 201), ("GET", 404), ("DELETE", 500), ("PUT", 400), ("GET", 200)]\nok = sum(1 for m, s in log if 200 <= s <= 299)\nclient_err = sum(1 for m, s in log if 400 <= s <= 499)\nprint(ok)\nprint(client_err)',
                },
                "quiz": [
                    {"q": "Which HTTP method creates a new resource?",
                     "options": ["GET", "POST", "DELETE", "FETCH"],
                     "answer": 1, "explain": "POST creates; GET only reads."},
                    {"q": "A 404 status means…",
                     "options": ["Server crashed", "Resource not found", "Success", "Unauthorized"],
                     "answer": 1, "explain": "4xx codes are client-side issues; 404 specifically = not found."},
                ],
            },
            {
                "slug": "json-deep-dive",
                "title": "JSON: The Language of APIs",
                "minutes": 14, "xp": 30,
                "content": """
<p><strong>JSON</strong> (JavaScript Object Notation) is how APIs exchange data — and it maps almost 1:1 to Python:</p>
<ul>
<li>JSON object <code>{}</code> ↔ Python <code>dict</code></li>
<li>JSON array <code>[]</code> ↔ Python <code>list</code></li>
<li><code>null</code> ↔ <code>None</code>, <code>true/false</code> ↔ <code>True/False</code></li>
</ul>
<p>Two functions do all the work: <code>json.loads(text)</code> parses a JSON string into Python objects; <code>json.dumps(obj)</code> serialises Python back to a JSON string (<code>indent=2</code> pretty-prints).</p>
<p>Real API responses nest deeply — practise the drill-down: <code>data["results"][0]["name"]</code>. Sketch the shape first, then write the path.</p>
""",
                "example": 'import json\n\nraw = \'{"city": "Vilnius", "temps": [21, 24, 19]}\'\ndata = json.loads(raw)\nprint(data["city"])\nprint(max(data["temps"]))\n\nprint(json.dumps({"ok": True}))',
                "challenge": {
                    "prompt": "Parse the JSON string in the starter and print: the username, the number of repos, and the name of the first repo.",
                    "starter": 'import json\nraw = \'{"user": "simasbuilds", "repos": [{"name": "pysprint", "stars": 42}, {"name": "sqltrainer", "stars": 17}]}\'\n# parse and print three lines\n',
                    "expected_output": "simasbuilds\n2\npysprint",
                    "hint": 'data["repos"] is a list of dicts — index it with [0] then ["name"].',
                    "solution": 'import json\nraw = \'{"user": "simasbuilds", "repos": [{"name": "pysprint", "stars": 42}, {"name": "sqltrainer", "stars": 17}]}\'\ndata = json.loads(raw)\nprint(data["user"])\nprint(len(data["repos"]))\nprint(data["repos"][0]["name"])',
                },
                "quiz": [
                    {"q": "JSON null becomes what in Python?",
                     "options": ["0", "\"null\"", "None", "False"],
                     "answer": 2, "explain": "null ↔ None; true/false ↔ True/False."},
                    {"q": "Which converts a Python dict into a JSON string?",
                     "options": ["json.loads", "json.dumps", "json.parse", "str()"],
                     "answer": 1, "explain": "dumps = 'dump to string'. loads parses the other direction."},
                ],
            },
            {
                "slug": "consuming-apis",
                "title": "Consuming APIs with requests",
                "minutes": 16, "xp": 35,
                "content": """
<p>The <code>requests</code> library is the gold standard for calling APIs from Python (install with <code>pip install requests</code>):</p>
<pre><code>import requests

resp = requests.get("https://api.github.com/users/simasbuilds")
resp.raise_for_status()        # crash loudly on 4xx/5xx
data = resp.json()             # parsed JSON → dict
print(data["public_repos"])</code></pre>
<ul>
<li><code>resp.status_code</code>, <code>resp.json()</code>, <code>resp.text</code></li>
<li>Query params: <code>requests.get(url, params={"q": "python"})</code></li>
<li>Sending data: <code>requests.post(url, json={"name": "Ada"})</code></li>
<li>Auth: usually a header — <code>headers={"Authorization": "Bearer TOKEN"}</code></li>
<li>Always set a <code>timeout=10</code> in production code</li>
</ul>
<p><em>Note:</em> the browser sandbox can't make real network calls, so the challenge simulates a response — the parsing skills are identical.</p>
""",
                "example": '# Simulated response - same shape requests.json() returns\ndef fake_get(url):\n    return {"status_code": 200,\n            "json": {"login": "simasbuilds", "public_repos": 12}}\n\nresp = fake_get("https://api.github.com/users/simasbuilds")\nif resp["status_code"] == 200:\n    print(resp["json"]["login"])',
                "challenge": {
                    "prompt": "The starter simulates an API returning weather for three cities. Loop through the results and print each city with its temperature as <code>City: temp°C</code>, then print the warmest city's name.",
                    "starter": 'response = {\n    "status": 200,\n    "results": [\n        {"city": "Vilnius", "temp": 22},\n        {"city": "Madrid", "temp": 31},\n        {"city": "Oslo", "temp": 14},\n    ],\n}\n# your code\n',
                    "expected_output": "Vilnius: 22°C\nMadrid: 31°C\nOslo: 14°C\nMadrid",
                    "hint": 'Use max(results, key=lambda r: r["temp"]) for the warmest.',
                    "solution": 'response = {\n    "status": 200,\n    "results": [\n        {"city": "Vilnius", "temp": 22},\n        {"city": "Madrid", "temp": 31},\n        {"city": "Oslo", "temp": 14},\n    ],\n}\nfor r in response["results"]:\n    print(f"{r[\'city\']}: {r[\'temp\']}°C")\nwarmest = max(response["results"], key=lambda r: r["temp"])\nprint(warmest["city"])',
                },
                "quiz": [
                    {"q": "What does resp.json() return?",
                     "options": ["A JSON string", "Parsed Python objects (dict/list)", "Raw bytes", "A file"],
                     "answer": 1, "explain": "It parses the response body from JSON into Python data structures."},
                    {"q": "Where does a Bearer token usually go?",
                     "options": ["The URL path", "The Authorization header", "A cookie only", "The request body"],
                     "answer": 1, "explain": "headers={\"Authorization\": \"Bearer <token>\"} is the standard pattern."},
                ],
            },
            {
                "slug": "building-an-api",
                "title": "Building Your Own API with Flask",
                "minutes": 18, "xp": 40,
                "content": """
<p>Flask makes building an API absurdly simple. A route maps a URL + method to a Python function; return a dict and Flask serialises it to JSON:</p>
<pre><code>from flask import Flask, request

app = Flask(__name__)
books = [{"id": 1, "title": "Fluent Python"}]

@app.get("/api/books")
def list_books():
    return {"books": books}

@app.post("/api/books")
def add_book():
    data = request.get_json()
    book = {"id": len(books) + 1, "title": data["title"]}
    books.append(book)
    return book, 201</code></pre>
<p>Key ideas: the <code>@app.get(...)</code> decorator registers the route; returning <code>(body, 201)</code> sets the status code; <code>&lt;int:book_id&gt;</code> in a path captures URL parameters. This very site is built exactly this way — check its source when you finish!</p>
""",
                "example": '# Route handlers are just functions - practise the logic:\nbooks = [{"id": 1, "title": "Fluent Python"}]\n\ndef add_book(data):\n    book = {"id": len(books) + 1, "title": data["title"]}\n    books.append(book)\n    return book, 201\n\nbody, status = add_book({"title": "Automate the Boring Stuff"})\nprint(status, body["id"], body["title"])',
                "challenge": {
                    "prompt": "Implement <code>get_book(book_id)</code> that searches the <code>books</code> list and returns the matching dict and <code>200</code>, or <code>{\"error\": \"not found\"}</code> and <code>404</code>. Print the results of looking up id 2 and id 99 (print status then title/error).",
                    "starter": 'books = [\n    {"id": 1, "title": "Fluent Python"},\n    {"id": 2, "title": "Automate the Boring Stuff"},\n]\n\ndef get_book(book_id):\n    # return (dict, status)\n    pass\n\nbody, status = get_book(2)\nprint(status, body["title"])\nbody, status = get_book(99)\nprint(status, body["error"])\n',
                    "expected_output": "200 Automate the Boring Stuff\n404 not found",
                    "hint": "Loop the books; if b[\"id\"] == book_id return b, 200. After the loop return the error dict with 404.",
                    "solution": 'books = [\n    {"id": 1, "title": "Fluent Python"},\n    {"id": 2, "title": "Automate the Boring Stuff"},\n]\n\ndef get_book(book_id):\n    for b in books:\n        if b["id"] == book_id:\n            return b, 200\n    return {"error": "not found"}, 404\n\nbody, status = get_book(2)\nprint(status, body["title"])\nbody, status = get_book(99)\nprint(status, body["error"])',
                },
                "quiz": [
                    {"q": "What status code should a successful POST that creates a resource return?",
                     "options": ["200", "201", "204", "301"],
                     "answer": 1, "explain": "201 Created is the REST convention for successful creation."},
                    {"q": "In Flask, returning a dict from a route…",
                     "options": ["Errors", "Is automatically serialised to a JSON response", "Returns HTML", "Needs str() first"],
                     "answer": 1, "explain": "Flask jsonifies returned dicts for you."},
                ],
            },
            {
                "slug": "rest-design",
                "title": "REST Design, Auth & Status Codes",
                "minutes": 15, "xp": 35,
                "content": """
<p>Good APIs follow <strong>REST conventions</strong> so developers can guess how they work:</p>
<ul>
<li>Nouns, not verbs, in URLs: <code>GET /api/courses</code> not <code>/api/getCourses</code></li>
<li>Plural resources with ids: <code>/api/courses/42/lessons/3</code></li>
<li>Method = action: same URL, different verbs do different things</li>
<li>Meaningful status codes + a consistent JSON error shape: <code>{"error": "..."}</code></li>
<li>Version your API: <code>/api/v1/...</code></li>
</ul>
<p><strong>Auth in practice:</strong> API keys (simple, per-app), Bearer tokens / JWT (per-user, expiring), OAuth (delegated, "Sign in with…"). Never put secrets in code — read them from environment variables (<code>.env</code> files, exactly like this project does).</p>
""",
                "example": 'ROUTES = {\n    ("GET", "/api/courses"): "list all courses",\n    ("POST", "/api/courses"): "create a course",\n    ("GET", "/api/courses/7"): "get course 7",\n    ("DELETE", "/api/courses/7"): "delete course 7",\n}\nfor (method, path), action in ROUTES.items():\n    print(f"{method:6} {path:20} -> {action}")',
                "challenge": {
                    "prompt": "Write <code>route_action(method, path)</code> returning: <code>\"list\"</code> for GET /items, <code>\"create\"</code> for POST /items, <code>\"detail\"</code> for GET /items/&lt;anything&gt;, and <code>\"unknown\"</code> otherwise. Print the four calls in the starter.",
                    "starter": 'def route_action(method, path):\n    # your rules\n    pass\n\nprint(route_action("GET", "/items"))\nprint(route_action("POST", "/items"))\nprint(route_action("GET", "/items/9"))\nprint(route_action("PATCH", "/other"))\n',
                    "expected_output": "list\ncreate\ndetail\nunknown",
                    "hint": 'path.startswith("/items/") catches detail routes.',
                    "solution": 'def route_action(method, path):\n    if method == "GET" and path == "/items":\n        return "list"\n    if method == "POST" and path == "/items":\n        return "create"\n    if method == "GET" and path.startswith("/items/"):\n        return "detail"\n    return "unknown"\n\nprint(route_action("GET", "/items"))\nprint(route_action("POST", "/items"))\nprint(route_action("GET", "/items/9"))\nprint(route_action("PATCH", "/other"))',
                },
                "quiz": [
                    {"q": "Which URL follows REST conventions best?",
                     "options": ["/api/getUser?id=5", "/api/users/5", "/api/user_fetch/5", "/fetchUser/5"],
                     "answer": 1, "explain": "Plural noun resource + id in the path — the verb comes from the HTTP method."},
                    {"q": "Where should API secrets live?",
                     "options": ["Hard-coded in source", "Committed config file", "Environment variables / .env excluded from git", "The URL"],
                     "answer": 2, "explain": "Secrets belong in env vars; .env files must be gitignored."},
                ],
            },
        ],
    },

    # ══════════════════════════════════════════════════════════════════
    # COURSE 6 — AUTOMATION & REAL-WORLD PYTHON
    # ══════════════════════════════════════════════════════════════════
    {
        "slug": "automation",
        "title": "Automation & Real-World Python",
        "tagline": "Text processing, dates, CSV data and regex — automate everything.",
        "level": "Advanced",
        "color": "#fb7185",
        "icon": "🤖",
        "description": "Turn Python into your personal robot: crunch CSV data, wrangle dates, master regular expressions and build a real log analyzer — the skills behind data pipelines and scripting jobs.",
        "lessons": [
            {
                "slug": "text-processing",
                "title": "Text Processing Like a Pro",
                "minutes": 14, "xp": 30,
                "content": """
<p>Most automation is text manipulation. Your core toolkit:</p>
<ul>
<li><code>s.split(",")</code> — string → list; <code>", ".join(items)</code> — list → string</li>
<li><code>s.startswith(x)</code> / <code>s.endswith(x)</code> — prefix/suffix tests</li>
<li><code>s.find(x)</code> — index of a substring (-1 if absent); <code>x in s</code> — simple test</li>
<li><code>s.splitlines()</code> — split text into lines</li>
<li>Chaining: <code>line.strip().lower().split(";")</code></li>
</ul>
<p>The split → transform → join pipeline is the bread and butter of every data-cleaning script ever written.</p>
""",
                "example": 'csv_row = "  Ada Lovelace, mathematician , London "\nparts = [p.strip() for p in csv_row.split(",")]\nprint(parts)\nprint(" | ".join(parts))',
                "challenge": {
                    "prompt": "Take the starter sentence, and print it as a slug: lowercase, words joined by hyphens. Expected: <code>learn-python-the-fast-way</code>",
                    "starter": 'title = "Learn Python The Fast Way"\n# make the slug\n',
                    "expected_output": "learn-python-the-fast-way",
                    "hint": '"-".join(title.lower().split())',
                    "solution": 'title = "Learn Python The Fast Way"\nslug = "-".join(title.lower().split())\nprint(slug)',
                },
                "quiz": [
                    {"q": 'What does "-".join(["a", "b", "c"]) return?',
                     "options": ['"abc"', '"a-b-c"', '["a-b-c"]', '"-abc-"'],
                     "answer": 1, "explain": "join glues list items together with the string as separator."},
                    {"q": '"hello world".split() splits on…',
                     "options": ["Nothing", "Every character", "Any whitespace", "Commas"],
                     "answer": 2, "explain": "With no argument, split() breaks on runs of whitespace — very handy."},
                ],
            },
            {
                "slug": "dates-and-times",
                "title": "Dates & Times",
                "minutes": 14, "xp": 30,
                "content": """
<p>Date math trips up every language — Python's <code>datetime</code> module makes it sane:</p>
<ul>
<li><code>date(2026, 7, 19)</code> — construct; <code>date.today()</code> — now</li>
<li><code>timedelta(days=30)</code> — a duration you can add/subtract</li>
<li>Subtracting dates gives a timedelta: <code>(d2 - d1).days</code></li>
<li><code>d.strftime("%d %B %Y")</code> — format to string (<em>f</em>ormat)</li>
<li><code>datetime.strptime("2026-07-19", "%Y-%m-%d")</code> — parse from string (<em>p</em>arse)</li>
</ul>
<p>Common codes: <code>%Y</code> year, <code>%m</code> month, <code>%d</code> day, <code>%H:%M</code> time, <code>%A</code> weekday name, <code>%B</code> month name.</p>
""",
                "example": 'from datetime import date, timedelta\n\nlaunch = date(2026, 1, 1)\ntoday = date(2026, 7, 19)\nprint((today - launch).days)\n\ndeadline = today + timedelta(days=14)\nprint(deadline.strftime("%Y-%m-%d"))',
                "challenge": {
                    "prompt": "Compute how many days passed between 2026-01-01 and 2026-07-19, then print the date 100 days after 2026-07-19 in <code>YYYY-MM-DD</code> format.",
                    "starter": "from datetime import date, timedelta\n# your code\n",
                    "expected_output": "199\n2026-10-27",
                    "hint": "(d2 - d1).days, then d2 + timedelta(days=100) and strftime(\"%Y-%m-%d\").",
                    "solution": 'from datetime import date, timedelta\nstart = date(2026, 1, 1)\nend = date(2026, 7, 19)\nprint((end - start).days)\nprint((end + timedelta(days=100)).strftime("%Y-%m-%d"))',
                },
                "quiz": [
                    {"q": "What type does date2 - date1 return?",
                     "options": ["int", "float", "timedelta", "str"],
                     "answer": 2, "explain": "Subtracting dates yields a timedelta; use .days to get the number."},
                    {"q": "strptime is for…",
                     "options": ["Formatting a date to string", "Parsing a string into a date", "Stripping whitespace", "Time zones"],
                     "answer": 1, "explain": "strptime = 'string parse time'; strftime = 'string format time'."},
                ],
            },
            {
                "slug": "csv-data",
                "title": "Crunching CSV Data",
                "minutes": 16, "xp": 35,
                "content": """
<p>CSV (comma-separated values) is the universal data format — every spreadsheet exports it. Python's <code>csv</code> module handles the tricky parts (quoted fields, commas inside values):</p>
<ul>
<li><code>csv.reader(f)</code> — rows as lists</li>
<li><code>csv.DictReader(f)</code> — rows as dicts keyed by the header row ← usually what you want</li>
<li><code>csv.DictWriter(f, fieldnames=[...])</code> — write dicts back out</li>
</ul>
<p>The analysis pattern: read rows → convert types (CSV gives you <em>strings</em>, even for numbers!) → filter → aggregate. Forgetting <code>int(row["price"])</code> is the #1 CSV bug.</p>
""",
                "example": 'import csv, io\n\nraw = "name,price\\nkeyboard,45\\nmonitor,220\\nmouse,25"\nrows = list(csv.DictReader(io.StringIO(raw)))\nfor row in rows:\n    print(row["name"], int(row["price"]) * 2)',
                "challenge": {
                    "prompt": "Parse the CSV in the starter with <code>DictReader</code> and print: the number of orders, the total revenue (qty × price summed), and the name of the product with the biggest single order value (qty × price).",
                    "starter": 'import csv, io\nraw = """product,qty,price\nlaptop,2,800\nphone,5,300\ncable,20,5"""\nrows = list(csv.DictReader(io.StringIO(raw)))\n# your code\n',
                    "expected_output": "3\n3200\nlaptop",
                    "hint": "Revenue per row: int(row[\"qty\"]) * int(row[\"price\"]). Use max(rows, key=...) for the biggest.",
                    "solution": 'import csv, io\nraw = """product,qty,price\nlaptop,2,800\nphone,5,300\ncable,20,5"""\nrows = list(csv.DictReader(io.StringIO(raw)))\nprint(len(rows))\nprint(sum(int(r["qty"]) * int(r["price"]) for r in rows))\nbiggest = max(rows, key=lambda r: int(r["qty"]) * int(r["price"]))\nprint(biggest["product"])',
                },
                "quiz": [
                    {"q": "What type are values read from a CSV file?",
                     "options": ["Inferred automatically", "Always strings", "Always numbers", "Bytes"],
                     "answer": 1, "explain": "CSV has no types — everything arrives as a string; convert explicitly."},
                    {"q": "DictReader keys come from…",
                     "options": ["Numbers 0..n", "The first (header) row", "You must supply them", "The filename"],
                     "answer": 1, "explain": "The header row becomes the dict keys for every subsequent row."},
                ],
            },
            {
                "slug": "regex",
                "title": "Regular Expressions",
                "minutes": 18, "xp": 40,
                "content": """
<p><strong>Regex</strong> is a mini-language for pattern matching — intimidating at first, unstoppable once learned. Core vocabulary:</p>
<ul>
<li><code>\\d</code> digit, <code>\\w</code> word char, <code>\\s</code> whitespace, <code>.</code> any char</li>
<li><code>+</code> one-or-more, <code>*</code> zero-or-more, <code>?</code> optional, <code>{3}</code> exactly 3</li>
<li><code>[abc]</code> character set, <code>^</code> start, <code>$</code> end</li>
<li><code>(...)</code> capture group — extract just that part</li>
</ul>
<p>Python API: <code>re.search(pat, s)</code> (first match or None), <code>re.findall(pat, s)</code> (all matches as a list), <code>re.sub(pat, repl, s)</code> (replace). Always write patterns as raw strings: <code>r"\\d+"</code>.</p>
""",
                "example": 'import re\n\ntext = "Orders: #1042 shipped, #1043 pending, #1099 shipped"\nids = re.findall(r"#(\\d+)", text)\nprint(ids)\n\nmasked = re.sub(r"\\d", "*", "PIN 4821")\nprint(masked)',
                "challenge": {
                    "prompt": "Use <code>re.findall</code> to extract all email addresses from the starter text and print each on its own line. Pattern hint: word chars + <code>@</code> + word chars + <code>.</code> + word chars.",
                    "starter": 'import re\ntext = "Contact ada@lovelace.io or grace@navy.mil for details; spam@@bad is not valid."\n# extract and print emails\n',
                    "expected_output": "ada@lovelace.io\ngrace@navy.mil",
                    "hint": r'r"\w+@\w+\.\w+" is enough for this text.',
                    "solution": 'import re\ntext = "Contact ada@lovelace.io or grace@navy.mil for details; spam@@bad is not valid."\nfor email in re.findall(r"\\w+@\\w+\\.\\w+", text):\n    print(email)',
                },
                "quiz": [
                    {"q": "What does \\d+ match?",
                     "options": ["A single digit", "One or more digits", "The letter d", "Zero or more digits"],
                     "answer": 1, "explain": "\\d is a digit; + means 'one or more of the preceding'."},
                    {"q": "Why write regex as r\"...\" raw strings?",
                     "options": ["Faster", "So backslashes reach the regex engine untouched", "Required syntax", "Only for Windows"],
                     "answer": 1, "explain": "Raw strings stop Python interpreting \\d, \\n etc. before regex sees them."},
                ],
            },
            {
                "slug": "log-analyzer-project",
                "title": "Capstone: Server Log Analyzer",
                "minutes": 25, "xp": 60,
                "content": """
<p>The capstone. Real servers write logs like:</p>
<pre><code>2026-07-19 12:01:33 GET /api/courses 200
2026-07-19 12:01:35 GET /api/missing 404</code></pre>
<p>Ops engineers get paid to answer: how many requests? how many errors? which endpoint is hottest? You now have every tool required:</p>
<ul>
<li><code>splitlines()</code> + <code>split()</code> to parse each line</li>
<li>Conditions to classify status codes</li>
<li><code>Counter</code> to rank endpoints</li>
<li>f-strings to report</li>
</ul>
<p>This exact pattern — parse, filter, aggregate, report — is the backbone of data engineering. Nail this and you're ready for real-world scripting work.</p>
""",
                "example": 'line = "2026-07-19 12:01:33 GET /api/courses 200"\ndate, time, method, path, status = line.split()\nprint(path, status)',
                "challenge": {
                    "prompt": "Analyze the log in the starter. Print: total number of requests, number of error responses (status ≥ 400), and the most-requested path.",
                    "starter": 'from collections import Counter\nlog = """2026-07-19 12:01:33 GET /api/courses 200\n2026-07-19 12:01:35 GET /api/missing 404\n2026-07-19 12:02:01 POST /api/login 200\n2026-07-19 12:02:20 GET /api/courses 200\n2026-07-19 12:03:00 GET /api/courses 500\n2026-07-19 12:03:41 GET /api/lessons 200"""\n# your analysis\n',
                    "expected_output": "6\n2\n/api/courses",
                    "hint": "Split each line with .split(); status is int(parts[4]); Counter the paths and use most_common(1).",
                    "solution": 'from collections import Counter\nlog = """2026-07-19 12:01:33 GET /api/courses 200\n2026-07-19 12:01:35 GET /api/missing 404\n2026-07-19 12:02:01 POST /api/login 200\n2026-07-19 12:02:20 GET /api/courses 200\n2026-07-19 12:03:00 GET /api/courses 500\n2026-07-19 12:03:41 GET /api/lessons 200"""\nlines = log.splitlines()\npaths = Counter()\nerrors = 0\nfor line in lines:\n    parts = line.split()\n    paths[parts[3]] += 1\n    if int(parts[4]) >= 400:\n        errors += 1\nprint(len(lines))\nprint(errors)\nprint(paths.most_common(1)[0][0])',
                },
                "quiz": [
                    {"q": "Counter(paths).most_common(1) returns…",
                     "options": ["The most common item", "A list with one (item, count) tuple", "A dict", "An int"],
                     "answer": 1, "explain": "most_common returns a list of tuples — index [0][0] for the item itself."},
                ],
            },
        ],
    },
]


def get_course(slug):
    for c in COURSES:
        if c["slug"] == slug:
            return c
    return None


def get_lesson(course_slug, lesson_slug):
    course = get_course(course_slug)
    if not course:
        return None, None
    for i, lesson in enumerate(course["lessons"]):
        if lesson["slug"] == lesson_slug:
            return course, i
    return course, None


def total_lessons():
    return sum(len(c["lessons"]) for c in COURSES)
