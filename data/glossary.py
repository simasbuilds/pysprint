"""Plain-English glossary.

Every term a beginner might trip over, explained the way you'd explain it
to a friend — no circular definitions, no jargon inside the definition.
Lesson pages link the first occurrence of each term automatically
(static/js/glossary.js), so nobody has to leave the lesson to look it up.

Keep definitions to one or two short sentences. If a definition needs
another glossary word to make sense, explain that word here too.
"""

GLOSSARY = {
    # ── the absolute basics ────────────────────────────────────────────
    "variable": "A name you give to a value so you can use it later. <code>age = 30</code> stores 30 under the name <code>age</code>.",
    "string": "Text. In Python you write it inside quotes, like <code>\"hello\"</code>.",
    "integer": "A whole number with no decimal point, like <code>7</code> or <code>-2</code>.",
    "float": "A number with a decimal point, like <code>3.14</code>.",
    "boolean": "A value that is either <code>True</code> or <code>False</code> — nothing else.",
    "function": "A named block of code you can run whenever you want, so you don't repeat yourself.",
    "argument": "A value you hand to a function when you run it. In <code>print(\"hi\")</code>, <code>\"hi\"</code> is the argument.",
    "parameter": "The name a function gives to a value it expects. It becomes a variable inside that function.",
    "return": "How a function hands a result back to whoever called it.",
    "loop": "Code that repeats. A <code>for</code> loop repeats once per item; a <code>while</code> loop repeats while something stays true.",
    "comment": "A note for humans, starting with <code>#</code>. Python ignores it completely.",
    "syntax": "The grammar rules of Python — where the colons, brackets and spaces have to go.",
    "indentation": "The spaces at the start of a line. Python uses them to know which lines belong inside an <code>if</code>, loop or function.",
    "expression": "Any piece of code that produces a value, like <code>2 + 2</code>.",

    # ── collections ────────────────────────────────────────────────────
    "list": "An ordered collection you can change, written in square brackets: <code>[1, 2, 3]</code>.",
    "dictionary": "A collection of key → value pairs, written in curly braces: <code>{\"name\": \"Ada\"}</code>. You look things up by key instead of by position.",
    "tuple": "Like a list, but it can never be changed after you create it. Written with round brackets: <code>(3, 5)</code>.",
    "set": "A collection that automatically throws away duplicates and has no order.",
    "index": "The position of an item in a list or string. Counting starts at 0, so the first item is index 0.",
    "slice": "Taking a section out of a list or string, like <code>items[1:4]</code>.",
    "iterable": "Anything you can loop over one item at a time — a list, a string, a dictionary, a file.",
    "immutable": "Cannot be changed once created. If you want a different value you have to make a new one.",
    "mutable": "Can be changed in place after you create it — a list, for example.",

    # ── errors & flow ──────────────────────────────────────────────────
    "exception": "Python's way of saying something went wrong. If you don't handle it, the program stops.",
    "traceback": "The error report Python prints when something breaks. Read it from the bottom up — the last line says what went wrong.",
    "debugging": "Finding out why code doesn't do what you expected, and fixing it.",

    # ── code organisation ──────────────────────────────────────────────
    "module": "A Python file you can use from another Python file.",
    "library": "A bundle of ready-made code someone else wrote so you don't have to.",
    "import": "Bringing code from another file or library into yours so you can use it.",
    "class": "A blueprint for creating objects that share the same data and behaviour.",
    "object": "One specific thing built from a class — a class is the cookie cutter, an object is the cookie.",
    "method": "A function that belongs to an object, called with a dot: <code>text.upper()</code>.",
    "attribute": "A piece of data stored on an object, read with a dot: <code>dog.name</code>.",
    "inheritance": "Letting one class start from another class's behaviour instead of rewriting it.",

    # ── working with the outside world ─────────────────────────────────
    "api": "A way for one program to ask another program for data or actions, usually over the internet.",
    "json": "A simple text format for sending data between programs. It looks almost exactly like Python dictionaries and lists.",
    "http": "The set of rules browsers and servers use to talk to each other on the web.",
    "endpoint": "One specific web address an API responds to, such as <code>/api/books</code>.",
    "request": "A message your program sends asking a server for something.",
    "response": "What the server sends back, usually some data plus a status code.",
    "status code": "A three-digit number saying how a request went: 200 fine, 404 not found, 500 server broke.",
    "parse": "Read text and pull structured meaning out of it — turning a date string into a real date, for example.",
    "regex": "A tiny pattern language for finding and extracting text, like \"a word followed by 4 digits\".",

    # ── expert-course vocabulary ───────────────────────────────────────
    "generator": "A function that produces values one at a time as you ask for them, instead of building a whole list up front. Saves memory.",
    "lazy": "Work that only happens when the result is actually needed, rather than immediately.",
    "closure": "An inner function that remembers the variables around it, even after the outer function has finished running.",
    "decorator": "A wrapper that adds behaviour to a function without changing the function's own code. Written as <code>@name</code> above a <code>def</code>.",
    "comprehension": "A compact one-line way to build a list, dictionary or set from something you loop over.",
    "dunder": 'A method with double underscores around its name, like <code>__len__</code>. Python calls these for you when you use built-ins like <code>len()</code>.',
    "type hint": "An optional note saying what kind of value is expected, like <code>name: str</code>. Python doesn't enforce it; it helps humans and editors.",
    "dataclass": "A shortcut for classes that mainly hold data — Python writes the boilerplate for you.",
    "recursion": "A function that calls itself to solve a smaller version of the same problem.",
    "algorithm": "A step-by-step recipe for solving a problem.",
}


def get_glossary():
    """Terms sorted longest-first so multi-word terms match before their parts."""
    return sorted(GLOSSARY.items(), key=lambda kv: -len(kv[0]))
