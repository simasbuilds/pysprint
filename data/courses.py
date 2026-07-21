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
        "icon": "terminal",
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
    # COURSE — PLAYFUL PYTHON: GAMES & PUZZLES
    # ══════════════════════════════════════════════════════════════════
    {
        "slug": "python-games",
        "title": "Playful Python: Games & Puzzles",
        "tagline": "Learn logic the fun way — build tiny games from your very first week.",
        "level": "Beginner",
        "color": "#f59e0b",
        "icon": "gamepad",
        "description": "The most fun way to cement the basics. Build a guessing game, roll (reproducible) dice, draw ASCII art, play word games and ship a tiny text adventure — while quietly mastering conditionals, loops, strings and dictionaries.",
        "lessons": [
            {
                "slug": "guessing-game",
                "title": "The Guessing Game: Your First Game Logic",
                "minutes": 10, "xp": 25,
                "content": """
<p>Almost every game is the same three-beat loop: the player acts, the game <strong>checks</strong>, the game <strong>responds</strong>. You already know enough Python to build that:</p>
<ul>
<li><code>if guess &lt; secret:</code> — the check</li>
<li><code>print("Too low!")</code> — the response</li>
<li>A <code>for</code> loop — one turn per guess</li>
</ul>
<p>Real games read the player's input live; here we simulate a player with a list of guesses so the game runs the same way every time. Everything else — the logic — is identical to the real thing.</p>
<p>Notice the order matters: check <em>too low</em>, then <em>too high</em>, and let <code>else</code> handle the win. When you can predict which branch runs for any guess, you think like a game programmer.</p>
""",
                "example": 'secret = 7\nguess = 5\n\nif guess < secret:\n    print("Too low!")\nelif guess > secret:\n    print("Too high!")\nelse:\n    print("You got it!")',
                "challenge": {
                    "prompt": "The secret number is <code>7</code>. A player guesses <code>3</code>, then <code>9</code>, then <code>7</code>. Loop over the guesses and print <code>Too low!</code>, <code>Too high!</code> or <code>You got it!</code> for each one.",
                    "starter": "secret = 7\nguesses = [3, 9, 7]\n\n# loop over guesses and respond to each one\n",
                    "expected_output": "Too low!\nToo high!\nYou got it!",
                    "hint": "for guess in guesses: then the same if / elif / else from the example, indented inside the loop.",
                    "solution": 'secret = 7\nguesses = [3, 9, 7]\n\nfor guess in guesses:\n    if guess < secret:\n        print("Too low!")\n    elif guess > secret:\n        print("Too high!")\n    else:\n        print("You got it!")',
                },
                "quiz": [
                    {"q": "In if guess < secret: ... elif guess > secret: ... else: ..., when does else run?",
                     "options": ["Never", "When the guess equals the secret", "When the guess is too low", "Always"],
                     "answer": 1, "explain": "If it's neither lower nor higher, the only possibility left is equal — that's the win."},
                    {"q": "Why simulate the player with a list of guesses here?",
                     "options": ["Python has no input", "So the program runs the same way every time and can be checked", "Lists are faster", "It's the only way to loop"],
                     "answer": 1, "explain": "Deterministic input makes the game testable — the same trick professionals use in automated game tests."},
                ],
            },
            {
                "slug": "dice-luck",
                "title": "Dice, Luck & random (with a Seed)",
                "minutes": 12, "xp": 25,
                "content": """
<p>Games need luck, and Python's <code>random</code> module provides it: <code>random.randint(1, 6)</code> is a die roll. But there's a professional secret hiding here:</p>
<p><strong><code>random.seed(n)</code> makes randomness repeatable.</strong> Seed the generator and the "random" sequence is exactly the same every run. That sounds like cheating — it's actually how games are tested, how Minecraft shares worlds (a world <em>is</em> a seed), and how scientists make simulations reproducible.</p>
<ul>
<li><code>random.randint(a, b)</code> — whole number from a to b, inclusive</li>
<li><code>random.choice(items)</code> — pick one item from a list</li>
<li><code>random.seed(n)</code> — same seed → same sequence, every time</li>
</ul>
""",
                "example": 'import random\n\nrandom.seed(42)          # same seed = same "luck" every run\nfor _ in range(3):\n    print("You rolled", random.randint(1, 6))\n\nprint(random.choice(["goblin", "dragon", "slime"]), "appears!")',
                "challenge": {
                    "prompt": "Seed the generator with <code>random.seed(1)</code>, then roll two dice three times. For each round print <code>Roll N: A + B = total</code> (roll both dice with <code>randint(1, 6)</code>, first die first).",
                    "starter": "import random\n\nrandom.seed(1)\n# roll two dice, three times, printing each round\n",
                    "expected_output": "Roll 1: 2 + 5 = 7\nRoll 2: 1 + 3 = 4\nRoll 3: 1 + 4 = 5",
                    "hint": "for i in range(1, 4): roll a = randint(1, 6) then b = randint(1, 6), then print(f\"Roll {i}: {a} + {b} = {a + b}\").",
                    "solution": 'import random\n\nrandom.seed(1)\nfor i in range(1, 4):\n    a = random.randint(1, 6)\n    b = random.randint(1, 6)\n    print(f"Roll {i}: {a} + {b} = {a + b}")',
                },
                "quiz": [
                    {"q": "What does random.seed(1) guarantee?",
                     "options": ["Rolls of only 1", "The same sequence of random numbers every run", "Fairer dice", "Faster random numbers"],
                     "answer": 1, "explain": "Seeding fixes the starting point of the generator — identical sequence, every run. Great for tests and shareable game worlds."},
                    {"q": "random.randint(1, 6) can return…",
                     "options": ["1 to 5", "0 to 6", "1 to 6, including both ends", "2 to 6"],
                     "answer": 2, "explain": "Unusually for Python, randint includes both endpoints — perfect for dice."},
                ],
            },
            {
                "slug": "ascii-art",
                "title": "Draw with Loops: ASCII Art",
                "minutes": 10, "xp": 25,
                "content": """
<p>Multiplying a string repeats it: <code>"*" * 4</code> is <code>"****"</code>. Combine that with a loop counter and you can <em>draw</em>:</p>
<ul>
<li><code>range(1, 5)</code> counts 1, 2, 3, 4 — a growing shape</li>
<li><code>range(3, 0, -1)</code> counts 3, 2, 1 — a shrinking one (the third number is the step)</li>
<li><code>print("*" * i)</code> turns the count into a row</li>
</ul>
<p>This is the gym where loops become intuition. When you can look at a shape and <em>see</em> the loop that draws it, iteration has clicked — and that's the exact skill behind rendering game boards, progress bars and terminal dashboards.</p>
""",
                "example": '# A growing triangle\nfor i in range(1, 5):\n    print("*" * i)\n\n# A brick wall\nfor row in range(3):\n    print("# " * 5)',
                "challenge": {
                    "prompt": "Draw an arrow: a triangle growing from 1 to 4 stars, then shrinking from 3 back to 1 (each row on its own line).",
                    "starter": "# grow 1 -> 4, then shrink 3 -> 1\n",
                    "expected_output": "*\n**\n***\n****\n***\n**\n*",
                    "hint": "Two loops: range(1, 5) growing, then range(3, 0, -1) shrinking. Each prints \"*\" * i.",
                    "solution": 'for i in range(1, 5):\n    print("*" * i)\nfor i in range(3, 0, -1):\n    print("*" * i)',
                },
                "quiz": [
                    {"q": "What does \"ha\" * 3 produce?",
                     "options": ["An error", "hahaha", "ha3", "ha ha ha"],
                     "answer": 1, "explain": "Multiplying a string by an int repeats it back-to-back."},
                    {"q": "What does range(3, 0, -1) generate?",
                     "options": ["3, 2, 1", "3, 2, 1, 0", "0, 1, 2, 3", "An empty range"],
                     "answer": 0, "explain": "Start 3, stop before 0, stepping by -1: 3, 2, 1."},
                ],
            },
            {
                "slug": "word-games",
                "title": "Word Games: Palindromes & Flips",
                "minutes": 12, "xp": 30,
                "content": """
<p>Strings hide a whole toy box. The star trick is <strong>slicing with a negative step</strong>: <code>word[::-1]</code> reads the string backwards.</p>
<p>A <strong>palindrome</strong> reads the same both ways ("racecar"). The test writes itself — but real words have capital letters, so normalise first:</p>
<ul>
<li><code>word.lower()</code> — level the playing field</li>
<li><code>word[::-1]</code> — the reversed string</li>
<li><code>clean == clean[::-1]</code> — the palindrome test</li>
</ul>
<p>This normalise-then-compare pattern is everywhere in real code: case-insensitive logins, search matching, de-duplicating names. You're learning it with toys; you'll use it at work.</p>
""",
                "example": 'word = "Racecar"\nclean = word.lower()\nprint(clean[::-1])                 # backwards\nprint(clean == clean[::-1])        # palindrome?',
                "challenge": {
                    "prompt": "For each word in <code>[\"Level\", \"python\", \"Racecar\"]</code>, print <code>word -&gt; palindrome!</code> if it reads the same backwards (ignoring case), otherwise <code>word -&gt; not a palindrome</code>. Keep the word's original capitalisation in the output.",
                    "starter": 'words = ["Level", "python", "Racecar"]\n\n# test each word, ignoring case\n',
                    "expected_output": "Level -> palindrome!\npython -> not a palindrome\nRacecar -> palindrome!",
                    "hint": "clean = word.lower(), then compare clean == clean[::-1]. Print with f\"{word} -> ...\".",
                    "solution": 'words = ["Level", "python", "Racecar"]\n\nfor word in words:\n    clean = word.lower()\n    if clean == clean[::-1]:\n        print(f"{word} -> palindrome!")\n    else:\n        print(f"{word} -> not a palindrome")',
                },
                "quiz": [
                    {"q": "What does \"python\"[::-1] evaluate to?",
                     "options": ["python", "nohtyp", "p", "An error"],
                     "answer": 1, "explain": "A slice with step -1 walks the string backwards."},
                    {"q": "Why call .lower() before the palindrome test?",
                     "options": ["It's required by slicing", "So 'Level' matches 'level' — comparisons are case-sensitive", "It removes spaces", "It reverses the string"],
                     "answer": 1, "explain": "\"L\" != \"l\" in Python. Normalising case first makes the comparison fair."},
                ],
            },
            {
                "slug": "adventure-game",
                "title": "Capstone: Tiny Text Adventure",
                "minutes": 15, "xp": 40,
                "content": """
<p>Time to ship a game. Every text adventure — from 1977's Zork to modern interactive fiction — is built on one idea: <strong>the world is a dictionary</strong>.</p>
<ul>
<li>Keys are room names: <code>"hall"</code>, <code>"library"</code>, <code>"vault"</code></li>
<li>Values are what the player sees there</li>
<li>The player's journey is just a list of keys to visit</li>
</ul>
<p>Walk the path with a loop, look each room up with <code>rooms[name]</code>, and narrate. That's the whole engine. Want more rooms, items, or monsters? Add keys. The <em>data</em> grows; the <em>code</em> stays the same — that separation of data from logic is one of the biggest ideas in software, and you're about to use it.</p>
""",
                "example": 'rooms = {\n    "cave": "Drip. Drip. Something glitters ahead.",\n    "chamber": "A chest! It creaks open...",\n}\n\nfor name in ["cave", "chamber"]:\n    print(f"You enter the {name}.")\n    print(rooms[name])',
                "challenge": {
                    "prompt": "Using the rooms and path in the starter, print <code>You enter the {room}.</code> followed by the room's description for each stop on the path — then print <code>Quest complete!</code> at the end.",
                    "starter": 'rooms = {\n    "hall": "A dusty hall. Doors lead north and east.",\n    "library": "Shelves of ancient Python books.",\n    "vault": "The vault! Treasure: 100 XP.",\n}\npath = ["hall", "library", "vault"]\n\n# walk the path, narrating each room\n',
                    "expected_output": "You enter the hall.\nA dusty hall. Doors lead north and east.\nYou enter the library.\nShelves of ancient Python books.\nYou enter the vault.\nThe vault! Treasure: 100 XP.\nQuest complete!",
                    "hint": "for name in path: print the f-string, then print(rooms[name]). The final print goes after the loop (unindented).",
                    "solution": 'rooms = {\n    "hall": "A dusty hall. Doors lead north and east.",\n    "library": "Shelves of ancient Python books.",\n    "vault": "The vault! Treasure: 100 XP.",\n}\npath = ["hall", "library", "vault"]\n\nfor name in path:\n    print(f"You enter the {name}.")\n    print(rooms[name])\nprint("Quest complete!")',
                },
                "quiz": [
                    {"q": "In this game, what does rooms[\"vault\"] do?",
                     "options": ["Creates a new room", "Looks up the vault's description by its key", "Deletes the vault", "Returns the room number"],
                     "answer": 1, "explain": "Square brackets on a dict fetch the value stored under that key."},
                    {"q": "Why is separating the world (data) from the walk (logic) powerful?",
                     "options": ["It runs faster", "You can grow the game by adding data without changing the code", "Python requires it", "It uses less memory"],
                     "answer": 1, "explain": "Ten more rooms is just ten more dict entries — the loop already handles them. Data-driven design scales."},
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
        "icon": "data",
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
        "icon": "function",
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
    # COURSE — THINK LIKE A PROGRAMMER (ALGORITHMS)
    # ══════════════════════════════════════════════════════════════════
    {
        "slug": "algorithms",
        "title": "Think Like a Programmer",
        "tagline": "Decomposition, searching, sorting and recursion — the thinking behind the code.",
        "level": "Intermediate",
        "color": "#f43f5e",
        "icon": "search",
        "description": "Syntax gets you started; algorithmic thinking gets you hired. Learn to break problems into steps, search and sort like the standard library does, wield recursion without fear, and build an intuition for why some code is fast and some is hopeless.",
        "lessons": [
            {
                "slug": "decomposition",
                "title": "Break Problems Down Before You Code",
                "minutes": 12, "xp": 30,
                "content": """
<p>Staring at a blank editor isn't a coding problem — it's a <strong>decomposition</strong> problem. Professionals never solve "the task"; they solve a chain of tiny steps:</p>
<ul>
<li><strong>What comes in?</strong> (a list of numbers)</li>
<li><strong>What goes out?</strong> (a count, a total, an average)</li>
<li><strong>What are the steps between?</strong> — each one small enough to be one or two lines</li>
</ul>
<p>Write the steps as comments first, then turn each comment into code. This "comment skeleton" technique feels almost too simple, and it is exactly how experienced developers start anything unfamiliar. A problem you can list, you can code.</p>
""",
                "example": "# Task: report on quiz scores\nscores = [80, 95, 60]\n\n# step 1: how many scores?\ncount = len(scores)\n# step 2: what's the total?\ntotal = sum(scores)\n# step 3: average = total / count\nprint(count, total, total / count)",
                "challenge": {
                    "prompt": "Decompose and solve: for <code>nums = [4, 8, 15, 16, 23, 42]</code>, print the count of numbers, then the total, then the average — one per line.",
                    "starter": "nums = [4, 8, 15, 16, 23, 42]\n\n# step 1: count\n# step 2: total\n# step 3: average = total / count\n",
                    "expected_output": "6\n108\n18.0",
                    "hint": "len(nums), sum(nums), and their division. Print each on its own line.",
                    "solution": "nums = [4, 8, 15, 16, 23, 42]\n\ncount = len(nums)\ntotal = sum(nums)\nprint(count)\nprint(total)\nprint(total / count)",
                },
                "quiz": [
                    {"q": "What's the first question to ask about any programming task?",
                     "options": ["Which library to import", "What goes in and what should come out", "How to make it fast", "What to name the file"],
                     "answer": 1, "explain": "Inputs and outputs frame the problem; the algorithm is just the path between them."},
                    {"q": "Why write steps as comments before coding?",
                     "options": ["Comments run faster", "Each comment becomes a small, obvious piece of code to write", "Python requires comments", "To pass code review"],
                     "answer": 1, "explain": "The comment skeleton turns one scary problem into five trivial ones."},
                ],
            },
            {
                "slug": "searching",
                "title": "Searching: Linear vs Binary",
                "minutes": 15, "xp": 35,
                "content": """
<p>How do you find one value among a hundred? Two classic answers:</p>
<p><strong>Linear search</strong> — check every item front to back. Simple, works on anything, needs up to <em>n</em> checks.</p>
<p><strong>Binary search</strong> — needs <strong>sorted</strong> data, and it's a superpower: look at the middle, decide which half the target is in, throw the other half away. Repeat.</p>
<ul>
<li>100 items → at most 7 checks</li>
<li>1,000,000 items → at most 20 checks</li>
<li>Each step: <code>mid = (low + high) // 2</code>, then move <code>low</code> or <code>high</code></li>
</ul>
<p>Halving beats scanning by absurd margins, and "can I halve this?" is one of the most valuable questions in all of programming — it's how databases find rows and how <code>git bisect</code> finds the commit that broke everything.</p>
""",
                "example": '# Linear: check everything\nnames = ["ada", "alan", "grace", "linus"]\nfor i, name in enumerate(names):\n    if name == "grace":\n        print("found at position", i)\n\n# Binary halves the range each step: 100 -> 50 -> 25 -> 13 -> 7 -> 4 -> 2 -> 1\nn = 100\nsteps = 0\nwhile n >= 1:\n    n //= 2\n    steps += 1\nprint(steps, "halvings")',
                "challenge": {
                    "prompt": "Binary-search for <code>87</code> in <code>list(range(1, 101))</code>, counting the loop passes. Print <code>Found 87 in N steps</code>, then <code>Linear search: M steps</code> where M is how many checks a front-to-back scan would need (position + 1).",
                    "starter": "numbers = list(range(1, 101))\ntarget = 87\n\nlow, high = 0, len(numbers) - 1\nsteps = 0\n# while low <= high: check the middle, halve the range, count steps\n",
                    "expected_output": "Found 87 in 7 steps\nLinear search: 87 steps",
                    "hint": "mid = (low + high) // 2. If numbers[mid] == target print and break; if it's smaller, low = mid + 1; otherwise high = mid - 1. Linear steps: numbers.index(target) + 1.",
                    "solution": 'numbers = list(range(1, 101))\ntarget = 87\n\nlow, high = 0, len(numbers) - 1\nsteps = 0\nwhile low <= high:\n    steps += 1\n    mid = (low + high) // 2\n    if numbers[mid] == target:\n        print(f"Found {target} in {steps} steps")\n        break\n    elif numbers[mid] < target:\n        low = mid + 1\n    else:\n        high = mid - 1\nprint(f"Linear search: {numbers.index(target) + 1} steps")',
                },
                "quiz": [
                    {"q": "What does binary search require that linear search doesn't?",
                     "options": ["A bigger list", "Sorted data", "A dictionary", "Recursion"],
                     "answer": 1, "explain": "Throwing half away only works if you know which half the target must be in — that's what sorted order gives you."},
                    {"q": "Roughly how many checks does binary search need for 1,000,000 items?",
                     "options": ["~500,000", "~1,000", "~20", "~2"],
                     "answer": 2, "explain": "Each check halves the range: 2^20 ≈ 1,000,000, so about 20 checks."},
                ],
            },
            {
                "slug": "sorting",
                "title": "Sorting: sorted(), Keys & Custom Order",
                "minutes": 14, "xp": 35,
                "content": """
<p>You'll rarely write a sorting algorithm — Python's <code>sorted()</code> (Timsort, invented for Python, adopted by Java and Android) is world-class. The real skill is <strong>telling it what order means</strong>:</p>
<ul>
<li><code>sorted(words)</code> — alphabetical</li>
<li><code>sorted(words, key=len)</code> — by length; the key function is called on each item and the results are compared instead</li>
<li><code>sorted(words, key=lambda w: (len(w), w))</code> — by length, <em>ties broken alphabetically</em> — tuples compare position by position</li>
<li><code>reverse=True</code> — flip any of the above</li>
</ul>
<p>The tuple-key trick is the professional move: 'sort by department, then salary descending, then name' is one line in Python.</p>
""",
                "example": 'words = ["fig", "banana", "kiwi"]\nprint(sorted(words))                # alphabetical\nprint(sorted(words, key=len))       # shortest first\nprint(sorted(words, key=len, reverse=True))',
                "challenge": {
                    "prompt": "For <code>words = [\"banana\", \"fig\", \"cherry\", \"kiwi\", \"apple\"]</code>: first print them sorted alphabetically, joined by <code>\", \"</code>. Then print them sorted by length with alphabetical tie-breaks, joined the same way.",
                    "starter": 'words = ["banana", "fig", "cherry", "kiwi", "apple"]\n\n# line 1: alphabetical\n# line 2: by (length, word)\n',
                    "expected_output": "apple, banana, cherry, fig, kiwi\nfig, kiwi, apple, banana, cherry",
                    "hint": "\", \".join(sorted(words)) for line one; key=lambda w: (len(w), w) for line two.",
                    "solution": 'words = ["banana", "fig", "cherry", "kiwi", "apple"]\n\nprint(", ".join(sorted(words)))\nprint(", ".join(sorted(words, key=lambda w: (len(w), w))))',
                },
                "quiz": [
                    {"q": "What does the key argument of sorted() do?",
                     "options": ["Encrypts the list", "Transforms each item into the value actually compared", "Removes duplicates", "Speeds up sorting"],
                     "answer": 1, "explain": "sorted compares key(item) instead of item — sort by anything you can compute."},
                    {"q": "How do tuples like (len(w), w) compare?",
                     "options": ["By total size", "Position by position — later positions break earlier ties", "Randomly", "They can't be compared"],
                     "answer": 1, "explain": "First elements are compared first; only ties fall through to the next element — perfect for multi-level sorts."},
                ],
            },
            {
                "slug": "recursion",
                "title": "Recursion: Functions That Call Themselves",
                "minutes": 16, "xp": 40,
                "content": """
<p>A recursive function solves a problem by solving a <em>smaller copy</em> of the same problem. Every correct one has exactly two parts:</p>
<ul>
<li><strong>Base case</strong> — an input so small the answer is immediate: <code>if n &lt; 10: return n</code></li>
<li><strong>Recursive step</strong> — shrink the input and delegate: <code>return n % 10 + digit_sum(n // 10)</code></li>
</ul>
<p>The mental model: <em>trust the recursive call</em>. Don't trace every level — assume <code>digit_sum(198)</code> already works, and just add the last digit. If the base case is right and each step genuinely shrinks the input, the whole thing is right.</p>
<p>Recursion is the natural language of nested things: folders inside folders, JSON inside JSON, comments replying to comments.</p>
""",
                "example": 'def countdown(n):\n    if n == 0:              # base case\n        print("Liftoff!")\n        return\n    print(n)\n    countdown(n - 1)        # smaller copy of the same problem\n\ncountdown(3)',
                "challenge": {
                    "prompt": "Write a recursive <code>digit_sum(n)</code> that adds up the digits of a non-negative number (digit_sum(1984) → 1+9+8+4 = 22). Print <code>digit_sum(1984)</code> and <code>digit_sum(7)</code>.",
                    "starter": "def digit_sum(n):\n    # base case: n < 10\n    # recursive step: last digit + digit_sum(rest)\n    pass\n\nprint(digit_sum(1984))\nprint(digit_sum(7))\n",
                    "expected_output": "22\n7",
                    "hint": "n % 10 is the last digit; n // 10 is the number without it. Base case: if n < 10: return n.",
                    "solution": "def digit_sum(n):\n    if n < 10:\n        return n\n    return n % 10 + digit_sum(n // 10)\n\nprint(digit_sum(1984))\nprint(digit_sum(7))",
                },
                "quiz": [
                    {"q": "What happens to a recursive function with no (reachable) base case?",
                     "options": ["It returns None", "It loops forever until Python raises RecursionError", "It returns 0", "Python refuses to define it"],
                     "answer": 1, "explain": "Every call spawns another; Python gives up at the recursion limit with RecursionError."},
                    {"q": "In digit_sum, why must the recursive call use n // 10?",
                     "options": ["It's faster", "The input must genuinely shrink toward the base case", "// is required in recursion", "To avoid floats"],
                     "answer": 1, "explain": "Progress toward the base case is what guarantees the recursion ends."},
                ],
            },
            {
                "slug": "counting-steps",
                "title": "Capstone: Counting Steps & Big-O Intuition",
                "minutes": 15, "xp": 45,
                "content": """
<p>Why does one script finish instantly and another hang forever on the same data? Count the <strong>steps</strong>, not the lines:</p>
<ul>
<li>One loop over n items → about <strong>n</strong> steps — double the data, double the time</li>
<li>A loop <em>inside</em> a loop → <strong>n × n</strong> steps — double the data, <em>quadruple</em> the time</li>
<li>Halving like binary search → <strong>log n</strong> steps — a million items feels like twenty</li>
</ul>
<p>Engineers write these as O(n), O(n²) and O(log n) — "Big-O" — but the notation is just shorthand for the growth you can now measure yourself. The instinct to ask <em>"how does this grow when the data grows?"</em> is the single most interview-tested skill in programming, and you can build it with two counters.</p>
""",
                "example": "items = list(range(8))\nops = 0\nfor a in items:          # one loop: n steps\n    ops += 1\nprint(ops)\n\nops = 0\nfor a in items:          # nested loops: n * n steps\n    for b in items:\n        ops += 1\nprint(ops)",
                "challenge": {
                    "prompt": "For 20 items, count the operations a single loop performs, then the operations a nested (loop-in-loop) pass performs. Print both counts, then print <code>Nested loops grow fast!</code>",
                    "starter": "items = list(range(20))\n\n# count single-loop ops, then nested-loop ops\n",
                    "expected_output": "20\n400\nNested loops grow fast!",
                    "hint": "Increment a counter inside each loop body. The nested version increments inside the inner loop.",
                    "solution": 'items = list(range(20))\n\nops = 0\nfor a in items:\n    ops += 1\nprint(ops)\n\nops = 0\nfor a in items:\n    for b in items:\n        ops += 1\nprint(ops)\nprint("Nested loops grow fast!")',
                },
                "quiz": [
                    {"q": "Data doubles from 1,000 to 2,000 items. Roughly what happens to an O(n²) algorithm's runtime?",
                     "options": ["Doubles", "Quadruples", "Stays the same", "Halves"],
                     "answer": 1, "explain": "n² growth: (2n)² = 4n². Nested loops punish growing data brutally."},
                    {"q": "Which growth pattern does binary search have?",
                     "options": ["O(n)", "O(n²)", "O(log n)", "O(1)"],
                     "answer": 2, "explain": "Halving the range each step means even huge inputs need few steps — logarithmic growth."},
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
        "icon": "tools",
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
        "icon": "api",
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
        "icon": "automation",
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

    # ══════════════════════════════════════════════════════════════════
    # COURSE — DATA ANALYSIS ESSENTIALS
    # ══════════════════════════════════════════════════════════════════
    {
        "slug": "data-analysis",
        "title": "Data Analysis Essentials",
        "tagline": "Turn messy numbers into answers: stats, cleaning, grouping and rankings.",
        "level": "Intermediate",
        "color": "#10b981",
        "icon": "chart",
        "description": "The everyday superpower. Describe datasets with real statistics, clean the messy values every spreadsheet hides, group and total by category, rank the top performers, and ship an insight report — pure Python, the same moves you'd later make in pandas.",
        "lessons": [
            {
                "slug": "describing-data",
                "title": "Describing Data: Mean, Median & Mode",
                "minutes": 12, "xp": 30,
                "content": """
<p>Before charts, before machine learning, analysis starts with three questions — and Python's built-in <code>statistics</code> module answers all of them:</p>
<ul>
<li><code>mean(data)</code> — the average. Honest for balanced data, easily dragged around by one extreme value</li>
<li><code>median(data)</code> — the middle value. Robust: one billionaire in the room changes the mean salary wildly, the median barely</li>
<li><code>mode(data)</code> — the most common value. The only one that also works on words and categories</li>
</ul>
<p>Knowing <em>which</em> to reach for is the analysis skill: report medians for incomes and house prices, means for balanced measurements, modes for "what's most popular?".</p>
""",
                "example": 'import statistics\n\nprices = [12, 15, 11, 14, 250]      # one luxury outlier\nprint(statistics.mean(prices))       # dragged to 60.4\nprint(statistics.median(prices))     # still honest: 14\nprint(statistics.mode(["tea", "coffee", "tea"]))',
                "challenge": {
                    "prompt": "For <code>scores = [72, 88, 95, 64, 88, 79]</code> print three lines: the mean shown with 1 decimal place, the median, and the mode.",
                    "starter": "import statistics\n\nscores = [72, 88, 95, 64, 88, 79]\n# mean (formatted to 1 decimal place), median, mode\n",
                    "expected_output": "81.0\n83.5\n88",
                    "hint": "print(f\"{statistics.mean(scores):.1f}\") formats to one decimal place, then statistics.median(scores), then statistics.mode(scores).",
                    "solution": 'import statistics\n\nscores = [72, 88, 95, 64, 88, 79]\nprint(f"{statistics.mean(scores):.1f}")\nprint(statistics.median(scores))\nprint(statistics.mode(scores))',
                },
                "quiz": [
                    {"q": "House prices in a street: eight around €300k, one at €5M. Which average should you report?",
                     "options": ["Mean — it uses all the data", "Median — it resists the outlier", "Mode", "Sum"],
                     "answer": 1, "explain": "The mansion drags the mean far above what a typical house costs; the median stays representative."},
                    {"q": "Which statistic works on non-numeric data like [\"red\", \"blue\", \"red\"]?",
                     "options": ["mean", "median", "mode", "None of them"],
                     "answer": 2, "explain": "Mode just counts frequency — no arithmetic needed, so categories are fine."},
                ],
            },
            {
                "slug": "cleaning-data",
                "title": "Cleaning Messy Data",
                "minutes": 14, "xp": 35,
                "content": """
<p>Real datasets arrive filthy: stray spaces, empty cells, <code>"n/a"</code>, numbers stored as text. Analysts joke that the job is 80% cleaning — and the pattern is always the same funnel:</p>
<ul>
<li><code>value.strip()</code> — cut the whitespace first</li>
<li>Skip empties early: <code>if not value: continue</code></li>
<li>Convert inside a safety net: <code>try: int(value) except ValueError: skip</code></li>
</ul>
<p>The golden rule: <strong>never let one bad value kill the whole run</strong>. Quarantine what you can't parse, keep what you can, and (in real jobs) count what you skipped — a spike in bad rows is itself a finding.</p>
""",
                "example": 'raw = [" 19 ", "", "twenty", "21"]\nclean = []\nfor value in raw:\n    value = value.strip()\n    if not value:\n        continue\n    try:\n        clean.append(int(value))\n    except ValueError:\n        print("skipped:", value)\nprint(clean)',
                "challenge": {
                    "prompt": "Clean <code>raw = [\" 42 \", \"17\", \"oops\", \"\", \"23 \", \"n/a\", \"8\"]</code> into a list of ints, silently skipping anything that isn't a number. Print the clean list, then its sum.",
                    "starter": 'raw = [" 42 ", "17", "oops", "", "23 ", "n/a", "8"]\nclean = []\n# strip, skip, convert with try/except\n',
                    "expected_output": "[42, 17, 23, 8]\n90",
                    "hint": "Loop, strip each value, try int(value) and append; except ValueError: pass. Empty strings raise ValueError too, so the try handles them.",
                    "solution": 'raw = [" 42 ", "17", "oops", "", "23 ", "n/a", "8"]\nclean = []\nfor value in raw:\n    try:\n        clean.append(int(value.strip()))\n    except ValueError:\n        pass\nprint(clean)\nprint(sum(clean))',
                },
                "quiz": [
                    {"q": "What does \" 42 \".strip() return?",
                     "options": ["\" 42 \"", "\"42\"", "42", "An error"],
                     "answer": 1, "explain": "strip() removes leading/trailing whitespace but returns a string — converting is a separate step."},
                    {"q": "Why wrap int(value) in try/except when cleaning?",
                     "options": ["It's faster", "So one unparseable value doesn't crash the whole run", "int() requires it", "To convert floats"],
                     "answer": 1, "explain": "Bad values are expected in real data; the pipeline must survive them."},
                ],
            },
            {
                "slug": "grouping-data",
                "title": "Grouping: Totals by Category",
                "minutes": 14, "xp": 35,
                "content": """
<p>"Revenue <em>by product</em>", "signups <em>by country</em>", "errors <em>by endpoint</em>" — the words <strong>by category</strong> always mean the same code: accumulate into a dictionary.</p>
<ul>
<li><code>totals[key] = totals.get(key, 0) + value</code> — the one-line accumulator: start at 0 if the key is new, add if it exists</li>
<li>Loop the pairs once; the dict grows itself</li>
<li><code>sorted(totals.items())</code> — report in a stable, readable order</li>
</ul>
<p>This is the pure-Python version of SQL's <code>GROUP BY</code> and pandas' <code>groupby()</code> — learn the pattern here and those tools will feel obvious later.</p>
""",
                "example": 'visits = ["home", "shop", "home", "blog", "home"]\ncounts = {}\nfor page in visits:\n    counts[page] = counts.get(page, 0) + 1\nfor page, n in sorted(counts.items()):\n    print(page, n)',
                "challenge": {
                    "prompt": "Total the sales per product in <code>sales = [(\"coffee\", 3.5), (\"tea\", 2.0), (\"coffee\", 4.0), (\"cake\", 3.0), (\"tea\", 2.5)]</code> and print one line per product in alphabetical order, formatted <code>product: total</code>.",
                    "starter": 'sales = [("coffee", 3.5), ("tea", 2.0), ("coffee", 4.0), ("cake", 3.0), ("tea", 2.5)]\ntotals = {}\n# accumulate, then print sorted\n',
                    "expected_output": "cake: 3.0\ncoffee: 7.5\ntea: 4.5",
                    "hint": "for product, amount in sales: totals[product] = totals.get(product, 0) + amount. Then loop sorted(totals.items()).",
                    "solution": 'sales = [("coffee", 3.5), ("tea", 2.0), ("coffee", 4.0), ("cake", 3.0), ("tea", 2.5)]\ntotals = {}\nfor product, amount in sales:\n    totals[product] = totals.get(product, 0) + amount\nfor product, total in sorted(totals.items()):\n    print(f"{product}: {total}")',
                },
                "quiz": [
                    {"q": "What does totals.get(key, 0) return when the key is missing?",
                     "options": ["It raises KeyError", "0 — the fallback you provided", "None", "An empty dict"],
                     "answer": 1, "explain": "get with a default never crashes — perfect for 'start at zero' accumulation."},
                    {"q": "This grouping pattern is the pure-Python equivalent of…",
                     "options": ["SQL's GROUP BY", "a web framework", "list slicing", "regular expressions"],
                     "answer": 0, "explain": "GROUP BY, pandas groupby, spreadsheet pivot tables — all the same idea: accumulate by key."},
                ],
            },
            {
                "slug": "rankings",
                "title": "Rankings: Top-N with sorted & max",
                "minutes": 13, "xp": 35,
                "content": """
<p>Every dashboard has a leaderboard: best sellers, slowest pages, biggest customers. In Python a ranking is three moves:</p>
<ul>
<li><code>items.items()</code> — get (name, number) pairs out of a dict</li>
<li><code>sorted(..., key=lambda pair: pair[1], reverse=True)</code> — order by the number, biggest first</li>
<li><code>[:3]</code> — slice the podium</li>
</ul>
<p>Need just the single winner? <code>max(data, key=data.get)</code> reads almost like English. And <code>enumerate(top, start=1)</code> numbers your report lines without a manual counter.</p>
""",
                "example": 'speeds = {"/home": 120, "/shop": 340, "/api": 45}\nslowest = max(speeds, key=speeds.get)\nprint("Slowest:", slowest)\n\nfor rank, (page, ms) in enumerate(\n        sorted(speeds.items(), key=lambda p: p[1], reverse=True), start=1):\n    print(rank, page, ms)',
                "challenge": {
                    "prompt": "From <code>units = {\"laptop\": 12, \"mouse\": 41, \"monitor\": 9, \"keyboard\": 25, \"webcam\": 17}</code>, print the top 3 sellers as <code>1. mouse (41 sold)</code>, <code>2. keyboard (25 sold)</code>, <code>3. webcam (17 sold)</code>.",
                    "starter": 'units = {"laptop": 12, "mouse": 41, "monitor": 9, "keyboard": 25, "webcam": 17}\n\n# sort by units sold (descending), take 3, print with ranks\n',
                    "expected_output": "1. mouse (41 sold)\n2. keyboard (25 sold)\n3. webcam (17 sold)",
                    "hint": "top = sorted(units.items(), key=lambda p: p[1], reverse=True)[:3], then enumerate(top, start=1).",
                    "solution": 'units = {"laptop": 12, "mouse": 41, "monitor": 9, "keyboard": 25, "webcam": 17}\n\ntop = sorted(units.items(), key=lambda pair: pair[1], reverse=True)[:3]\nfor rank, (product, sold) in enumerate(top, start=1):\n    print(f"{rank}. {product} ({sold} sold)")',
                },
                "quiz": [
                    {"q": "What does max(units, key=units.get) return?",
                     "options": ["The largest value", "The key with the largest value", "A (key, value) tuple", "An error"],
                     "answer": 1, "explain": "max iterates the dict's keys and compares units.get(key) — so you get the winning key."},
                    {"q": "What does enumerate(top, start=1) add to the loop?",
                     "options": ["Sorting", "A rank counter starting at 1 alongside each item", "Reversal", "Filtering"],
                     "answer": 1, "explain": "enumerate pairs each item with a rising index — start=1 makes it human-friendly for rankings."},
                ],
            },
            {
                "slug": "insight-report",
                "title": "Capstone: From Raw Rows to Insight Report",
                "minutes": 18, "xp": 45,
                "content": """
<p>Time to run the full pipeline every analyst runs, whatever the tool:</p>
<ul>
<li><strong>Parse</strong> — split each <code>"region,amount"</code> row into fields</li>
<li><strong>Clean</strong> — convert amounts, quarantine garbage with try/except</li>
<li><strong>Aggregate</strong> — total by region with the dict accumulator</li>
<li><strong>Report</strong> — row count, grand total, top region</li>
</ul>
<p>Parse → clean → aggregate → report is the same skeleton whether the data is 6 rows in a list or 6 billion in a warehouse; only the tools scale up. Ship this and you've done real analysis — the kind that answers an actual business question.</p>
""",
                "example": 'row = "north,120"\nregion, amount = row.split(",")\nprint(region, int(amount))',
                "challenge": {
                    "prompt": "Analyse <code>rows = [\"north,120\", \"south,95\", \"north,80\", \"west,x\", \"east,150\", \"south,45\"]</code>, skipping rows whose amount isn't a number. Print three lines: the number of valid rows, the grand total, and the region with the highest total.",
                    "starter": 'rows = ["north,120", "south,95", "north,80", "west,x", "east,150", "south,45"]\ntotals = {}\nvalid = 0\n# parse, clean, aggregate - then report\n',
                    "expected_output": "5\n490\nnorth",
                    "hint": "Split each row on \",\"; int() the amount inside try/except; accumulate totals and count valid rows. Top region: max(totals, key=totals.get).",
                    "solution": 'rows = ["north,120", "south,95", "north,80", "west,x", "east,150", "south,45"]\ntotals = {}\nvalid = 0\nfor row in rows:\n    region, raw_amount = row.split(",")\n    try:\n        amount = int(raw_amount)\n    except ValueError:\n        continue\n    valid += 1\n    totals[region] = totals.get(region, 0) + amount\nprint(valid)\nprint(sum(totals.values()))\nprint(max(totals, key=totals.get))',
                },
                "quiz": [
                    {"q": "Put the analysis pipeline in order:",
                     "options": ["report → parse → clean → aggregate", "parse → clean → aggregate → report", "aggregate → parse → report → clean", "clean → report → parse → aggregate"],
                     "answer": 1, "explain": "You can't clean what you haven't parsed, or total what you haven't cleaned. The funnel narrows toward the answer."},
                    {"q": "Why 'continue' on a bad row instead of letting it crash?",
                     "options": ["continue is faster", "Real datasets always contain garbage; the report must still ship", "Python requires it", "To keep the row for later"],
                     "answer": 1, "explain": "Skipping (and in real work, counting) bad rows keeps one typo from killing the whole report."},
                ],
            },
        ],
    },

    # ══════════════════════════════════════════════════════════════════
    # COURSE 7 — EXPERT PYTHON
    # ══════════════════════════════════════════════════════════════════
    {
        "slug": "expert-python",
        "title": "Expert Python",
        "tagline": "Generators, decorators, dunders — the Python that professionals write.",
        "level": "Advanced",
        "color": "#a78bfa",
        "icon": "crown",
        "description": "The course that turns working Python into elegant Python. Master lazy iteration with generators, wrap behaviour with decorators, manage resources with context managers, hook into the data model with dunder methods, and wield functools, itertools, type hints and dataclasses like a senior engineer.",
        "lessons": [
            {
                "slug": "generators",
                "title": "Generators & Lazy Iteration",
                "minutes": 16, "xp": 40,
                "content": """
<p>A <strong>generator</strong> is a function that produces values one at a time instead of building a whole list in memory. Swap <code>return</code> for <code>yield</code> and Python gives you a <em>pausable</em> function:</p>
<ul>
<li><code>yield value</code> — hands one value to the caller and <strong>freezes</strong> the function right there, local variables intact</li>
<li><code>next(gen)</code> — resumes execution until the next <code>yield</code></li>
<li>A <code>for</code> loop calls <code>next()</code> for you until the generator is exhausted</li>
</ul>
<p>This is <strong>lazy evaluation</strong>: values are computed only when asked for. A generator over a 10&nbsp;GB log file uses a few kilobytes of memory, because only one line exists at a time.</p>
<p>Generator <em>expressions</em> look like list comprehensions with round brackets: <code>(n * n for n in range(10**9))</code> is created instantly — nothing is computed until you iterate.</p>
""",
                "example": 'def fibonacci():\n    a, b = 0, 1\n    while True:          # an INFINITE sequence - impossible with a list\n        yield a\n        a, b = b, a + b\n\nfib = fibonacci()\nfor _ in range(8):\n    print(next(fib), end=" ")\nprint()\n\nsquares = (n * n for n in range(1_000_000))  # nothing computed yet\nprint(next(squares), next(squares), next(squares))',
                "challenge": {
                    "prompt": "Write a generator function <code>countdown(n)</code> that yields the numbers from <code>n</code> down to <code>1</code>. Loop over <code>countdown(3)</code> printing each value on its own line, then print <code>Liftoff!</code>.",
                    "starter": "def countdown(n):\n    # yield n, n-1, ... 1\n    pass\n\n# loop over countdown(3), then print Liftoff!\n",
                    "expected_output": "3\n2\n1\nLiftoff!",
                    "hint": "Use a while loop inside the generator: while n > 0: yield n; n -= 1. Then: for value in countdown(3): print(value).",
                    "solution": 'def countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\n\nfor value in countdown(3):\n    print(value)\nprint("Liftoff!")',
                },
                "quiz": [
                    {"q": "What makes a function a generator?",
                     "options": ["Calling it with next()", "Containing at least one yield", "Returning a list", "The @generator decorator"],
                     "answer": 1, "explain": "Any function containing yield becomes a generator function — calling it returns a generator object without running the body."},
                    {"q": "Why can a generator represent an infinite sequence?",
                     "options": ["It can't — Python would crash", "Values are produced one at a time, only when requested", "It compresses the values", "Python allocates infinite memory lazily"],
                     "answer": 1, "explain": "Laziness is the trick: only the current value exists. The caller decides when to stop asking."},
                ],
            },
            {
                "slug": "decorators",
                "title": "Closures & Decorators",
                "minutes": 18, "xp": 45,
                "content": """
<p>In Python, functions are values: you can pass them around, store them and return them. A <strong>closure</strong> is an inner function that remembers variables from the function that created it — even after that outer function has finished.</p>
<p>A <strong>decorator</strong> uses closures to wrap extra behaviour around a function without touching its body:</p>
<ul>
<li><code>@decorator</code> above a <code>def</code> is pure sugar for <code>func = decorator(func)</code></li>
<li>The decorator returns a <code>wrapper</code> function that runs code <em>before and after</em> calling the original</li>
<li><code>*args, **kwargs</code> in the wrapper lets it wrap any signature</li>
</ul>
<p>This is how <code>@app.get(...)</code> in Flask, <code>@lru_cache</code>, <code>@dataclass</code> and pytest fixtures all work — decorators are the backbone of professional Python APIs.</p>
""",
                "example": 'def log_calls(func):\n    def wrapper(*args, **kwargs):\n        print(f"-> calling {func.__name__}{args}")\n        result = func(*args, **kwargs)\n        print(f"<- {func.__name__} returned {result!r}")\n        return result\n    return wrapper\n\n@log_calls\ndef add(a, b):\n    return a + b\n\nadd(2, 3)',
                "challenge": {
                    "prompt": "Write a decorator <code>shout</code> that uppercases whatever string the wrapped function returns. Apply it to <code>greet(name)</code>, which returns <code>f\"hello, {name}\"</code>, then print <code>greet(\"ada\")</code> and <code>greet(\"grace\")</code>.",
                    "starter": 'def shout(func):\n    # return a wrapper that uppercases func\'s result\n    pass\n\n@shout\ndef greet(name):\n    return f"hello, {name}"\n\n# print greet("ada") and greet("grace")\n',
                    "expected_output": "HELLO, ADA\nHELLO, GRACE",
                    "hint": "The wrapper calls func(*args, **kwargs), then returns result.upper(). Don't forget to return the wrapper from shout.",
                    "solution": 'def shout(func):\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs).upper()\n    return wrapper\n\n@shout\ndef greet(name):\n    return f"hello, {name}"\n\nprint(greet("ada"))\nprint(greet("grace"))',
                },
                "quiz": [
                    {"q": "@timer above def slow(): is equivalent to…",
                     "options": ["slow = timer(slow)", "timer(slow())", "slow.timer()", "timer.slow()"],
                     "answer": 0, "explain": "Decorator syntax replaces the function with whatever the decorator returns: slow = timer(slow)."},
                    {"q": "Why do wrappers use (*args, **kwargs)?",
                     "options": ["It's required syntax", "So one wrapper can forward any combination of arguments", "It makes calls faster", "To rename the arguments"],
                     "answer": 1, "explain": "*args/**kwargs capture whatever the caller passes and forward it unchanged, so the decorator works on any function."},
                ],
            },
            {
                "slug": "context-managers",
                "title": "Context Managers & the with Statement",
                "minutes": 15, "xp": 40,
                "content": """
<p>Every time you write <code>with open(...) as f:</code> you're using a <strong>context manager</strong> — an object that promises to <em>set something up</em> on entry and <em>clean it up</em> on exit, even if the body raises an exception.</p>
<p>The protocol is two dunder methods:</p>
<ul>
<li><code>__enter__(self)</code> — runs at the start of the <code>with</code> block; its return value is bound by <code>as</code></li>
<li><code>__exit__(self, exc_type, exc, tb)</code> — <strong>always</strong> runs at the end, exception or not</li>
</ul>
<p>Files, database transactions, locks, temporary directories, mocked tests — anything with a setup/teardown pair belongs in a context manager. The <code>contextlib.contextmanager</code> decorator lets you write one as a generator: code before <code>yield</code> is the entry, code after is the exit.</p>
""",
                "example": 'from contextlib import contextmanager\n\n@contextmanager\ndef transaction(name):\n    print(f"BEGIN {name}")\n    try:\n        yield\n        print(f"COMMIT {name}")\n    except Exception as error:\n        print(f"ROLLBACK {name}: {error}")\n\nwith transaction("transfer"):\n    print("moving funds...")\n\nwith transaction("bad-transfer"):\n    raise ValueError("insufficient balance")',
                "challenge": {
                    "prompt": "Write a class <code>Tag</code> whose constructor takes a tag name. As a context manager it prints <code>&lt;b&gt;</code> on enter and <code>&lt;/b&gt;</code> on exit (for name <code>\"b\"</code>). Use <code>with Tag(\"b\"):</code> around a line printing <code>bold text</code>.",
                    "starter": 'class Tag:\n    def __init__(self, name):\n        self.name = name\n\n    # add __enter__ and __exit__\n\nwith Tag("b"):\n    print("bold text")\n',
                    "expected_output": "<b>\nbold text\n</b>",
                    "hint": "__enter__ prints f\"<{self.name}>\" and returns self; __exit__(self, exc_type, exc, tb) prints f\"</{self.name}>\".",
                    "solution": 'class Tag:\n    def __init__(self, name):\n        self.name = name\n\n    def __enter__(self):\n        print(f"<{self.name}>")\n        return self\n\n    def __exit__(self, exc_type, exc, tb):\n        print(f"</{self.name}>")\n        return False\n\nwith Tag("b"):\n    print("bold text")',
                },
                "quiz": [
                    {"q": "When does __exit__ run?",
                     "options": ["Only if the block succeeds", "Only if the block raises", "Always — success or exception", "Only when you call it"],
                     "answer": 2, "explain": "That guarantee is the whole point: cleanup always happens, like finally."},
                    {"q": "In a @contextmanager generator, what does the code before yield represent?",
                     "options": ["The cleanup phase", "The setup phase (__enter__)", "Error handling", "It never runs"],
                     "answer": 1, "explain": "Everything before yield runs on entry; everything after yield runs on exit."},
                ],
            },
            {
                "slug": "data-model",
                "title": "Dunder Methods & the Python Data Model",
                "minutes": 18, "xp": 45,
                "content": """
<p>Why does <code>len(\"abc\")</code> work? Because <code>str</code> implements <code>__len__</code>. Python's operators and built-ins are a thin layer over <strong>dunder (double-underscore) methods</strong> — implement them and your own classes plug straight into the language:</p>
<ul>
<li><code>__repr__</code> — how the object prints (aim for something a developer could paste back into code)</li>
<li><code>__add__</code> — powers <code>a + b</code></li>
<li><code>__eq__</code> — powers <code>==</code> (by default Python compares identity, not value!)</li>
<li><code>__len__</code>, <code>__getitem__</code>, <code>__contains__</code> — make objects sliceable, iterable and <code>in</code>-testable</li>
</ul>
<p>This is called the <strong>data model</strong>, and it's the most Pythonic idea in the language: instead of inventing <code>.equals()</code> or <code>.plus()</code> methods, you teach your objects to speak Python's native vocabulary.</p>
""",
                "example": 'class Playlist:\n    def __init__(self, *songs):\n        self.songs = list(songs)\n\n    def __len__(self):\n        return len(self.songs)\n\n    def __getitem__(self, index):\n        return self.songs[index]\n\nmix = Playlist("Blue Monday", "Around the World", "One More Time")\nprint(len(mix))\nprint(mix[0])\nfor song in mix:          # __getitem__ makes it iterable too!\n    print("-", song)',
                "challenge": {
                    "prompt": "Build a <code>Vector</code> class with <code>x</code> and <code>y</code>. Implement <code>__repr__</code> returning <code>Vector(x, y)</code>, <code>__add__</code> for coordinate-wise addition, and <code>__eq__</code> for value equality. Print <code>Vector(1, 2) + Vector(3, 4)</code>, then print <code>Vector(1, 2) == Vector(1, 2)</code>.",
                    "starter": "class Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    # add __repr__, __add__, __eq__\n\nprint(Vector(1, 2) + Vector(3, 4))\nprint(Vector(1, 2) == Vector(1, 2))\n",
                    "expected_output": "Vector(4, 6)\nTrue",
                    "hint": "__repr__ returns f\"Vector({self.x}, {self.y})\"; __add__ returns Vector(self.x + other.x, self.y + other.y); __eq__ compares both coordinates.",
                    "solution": 'class Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __repr__(self):\n        return f"Vector({self.x}, {self.y})"\n\n    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)\n\n    def __eq__(self, other):\n        return self.x == other.x and self.y == other.y\n\nprint(Vector(1, 2) + Vector(3, 4))\nprint(Vector(1, 2) == Vector(1, 2))',
                },
                "quiz": [
                    {"q": "Without __eq__, what does obj1 == obj2 compare?",
                     "options": ["All attributes", "Their identity (are they the same object?)", "Their string forms", "It raises TypeError"],
                     "answer": 1, "explain": "The default __eq__ is identity — two equal-looking objects compare False unless you define value equality."},
                    {"q": "Which dunder does a + b call?",
                     "options": ["a.__plus__(b)", "a.__add__(b)", "a.__sum__(b)", "add(a, b)"],
                     "answer": 1, "explain": "Operators map to dunders: + is __add__ (with __radd__ as the right-hand fallback)."},
                ],
            },
            {
                "slug": "functional-tools",
                "title": "Functional Power Tools: functools & itertools",
                "minutes": 16, "xp": 45,
                "content": """
<p>Two standard-library modules hold the tools that make expert Python so compact:</p>
<p><strong>functools</strong> — tools that operate on functions:</p>
<ul>
<li><code>@lru_cache</code> — memoize a function in one line; exponential recursions become instant</li>
<li><code>reduce(f, seq)</code> — fold a sequence into a single value: <code>reduce(lambda a, b: a * b, [1, 2, 3, 4])</code> → 24</li>
<li><code>partial(f, x)</code> — pre-fill some arguments, get a new function back</li>
</ul>
<p><strong>itertools</strong> — an iterator algebra:</p>
<ul>
<li><code>combinations(\"ABC\", 2)</code> — every unordered pair</li>
<li><code>chain(a, b)</code> — one stream from many iterables</li>
<li><code>count()</code>, <code>cycle()</code>, <code>islice()</code> — infinite streams, safely sliced</li>
</ul>
<p>Everything in itertools is lazy — these tools compose into data pipelines that process millions of items in constant memory.</p>
""",
                "example": 'from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)\n\nprint(fib(80))       # instant - would take years without the cache\n\nfrom itertools import islice, count\nevens = (n for n in count() if n % 2 == 0)   # infinite stream\nprint(list(islice(evens, 5)))                 # safely take 5',
                "challenge": {
                    "prompt": "Use <code>functools.reduce</code> to print the product of the numbers 1–5. Then use <code>itertools.combinations</code> on the string <code>\"ABC\"</code> to print every 2-letter combination joined as a string, one per line.",
                    "starter": "from functools import reduce\nfrom itertools import combinations\n\n# product of 1..5 with reduce\n\n# every 2-letter combination of \"ABC\", one per line\n",
                    "expected_output": "120\nAB\nAC\nBC",
                    "hint": "reduce(lambda a, b: a * b, range(1, 6)) gives the product. combinations(\"ABC\", 2) yields tuples — join each with \"\".join(pair).",
                    "solution": 'from functools import reduce\nfrom itertools import combinations\n\nprint(reduce(lambda a, b: a * b, range(1, 6)))\nfor pair in combinations("ABC", 2):\n    print("".join(pair))',
                },
                "quiz": [
                    {"q": "What does @lru_cache do?",
                     "options": ["Limits recursion depth", "Stores results so repeated calls with the same arguments return instantly", "Compresses return values", "Runs the function in parallel"],
                     "answer": 1, "explain": "It memoizes: each unique argument set is computed once, then served from cache."},
                    {"q": "Why is itertools memory-efficient?",
                     "options": ["It uses C arrays", "Everything is lazy — items are produced one at a time on demand", "It compresses lists", "It isn't"],
                     "answer": 1, "explain": "itertools returns iterators, not lists — only the current item exists in memory."},
                ],
            },
            {
                "slug": "modern-python",
                "title": "Type Hints, Dataclasses & Modern Python",
                "minutes": 18, "xp": 50,
                "content": """
<p>Modern professional Python is <em>annotated</em> and <em>declarative</em>. Two features define the style:</p>
<p><strong>Type hints</strong> document what a function expects and returns — <code>def price(qty: int, unit: float) -&gt; float:</code>. Python doesn't enforce them at runtime, but editors autocomplete with them and tools like <code>mypy</code> catch bugs before the code runs. Every major codebase now requires them.</p>
<p><strong>Dataclasses</strong> kill boilerplate. Add <code>@dataclass</code> to a class of annotated fields and Python generates <code>__init__</code>, <code>__repr__</code> and <code>__eq__</code> for you:</p>
<ul>
<li>Fields can have defaults; mutable defaults use <code>field(default_factory=list)</code></li>
<li><code>frozen=True</code> makes instances immutable (hashable, safe to share)</li>
<li>They compose beautifully with type hints, sorting and serialization</li>
</ul>
<p>This lesson caps the course: generators, decorators, dunders and dataclasses are the vocabulary of every senior Python code review.</p>
""",
                "example": 'from dataclasses import dataclass, field\n\n@dataclass\nclass Task:\n    title: str\n    done: bool = False\n    tags: list[str] = field(default_factory=list)\n\nfirst = Task("Ship the release", tags=["work"])\nprint(first)                                    # readable repr, free\nprint(first == Task("Ship the release", tags=["work"]))  # value equality, free',
                "challenge": {
                    "prompt": "Define a <code>@dataclass Book</code> with fields <code>title: str</code> and <code>pages: int</code>. Create <code>Book(\"Fluent Python\", 792)</code> and <code>Book(\"Clean Code\", 464)</code> in a list, sort the list by page count, and print each as <code>title (pages)</code>.",
                    "starter": 'from dataclasses import dataclass\n\n# define Book, build the list, sort by pages, print "title (pages)"\n',
                    "expected_output": "Clean Code (464)\nFluent Python (792)",
                    "hint": "sorted(shelf, key=lambda book: book.pages) sorts ascending. Print with f\"{book.title} ({book.pages})\".",
                    "solution": 'from dataclasses import dataclass\n\n@dataclass\nclass Book:\n    title: str\n    pages: int\n\nshelf = [Book("Fluent Python", 792), Book("Clean Code", 464)]\nfor book in sorted(shelf, key=lambda book: book.pages):\n    print(f"{book.title} ({book.pages})")',
                },
                "quiz": [
                    {"q": "What does Python do with type hints at runtime?",
                     "options": ["Raises TypeError on mismatch", "Converts values to the hinted type", "Essentially nothing — they're for tools and readers", "Slows the program down significantly"],
                     "answer": 2, "explain": "Hints are metadata. Enforcement comes from external tools like mypy and pyright, not the interpreter."},
                    {"q": "Which methods does @dataclass generate from the field annotations?",
                     "options": ["__init__, __repr__, __eq__", "__add__ and __sub__", "__enter__ and __exit__", "Only __init__"],
                     "answer": 0, "explain": "The big three of boilerplate — constructor, readable repr and value equality — are generated automatically."},
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
