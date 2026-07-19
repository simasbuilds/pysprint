"""Animated line-by-line walkthroughs of lesson example code.

Keyed by (course_slug, lesson_slug). Each step: {"line": 1-based line in
the lesson's `example` code, "text": what happens at that moment}.
The lesson page renders these as a step-through animation player.
"""

WALKTHROUGHS = {
    ("python-fundamentals", "hello-python"): [
        {"line": 1, "text": "Python reads top to bottom. Line 1 starts with # — a comment. Python skips it completely; it exists only for humans."},
        {"line": 2, "text": "print() is called with the string \"Hello, world!\". Python sends that text to the screen and moves on."},
        {"line": 3, "text": "print() gets TWO values separated by a comma — it prints both with a single space between them: Python is awesome."},
    ],
    ("python-fundamentals", "variables-and-types"): [
        {"line": 1, "text": "The = sign stores the string \"Ada\" in a box named `name`. From now on, typing `name` means \"Ada\"."},
        {"line": 2, "text": "36 has no quotes, so it's stored as an int — a number Python can do math with."},
        {"line": 3, "text": "1.7 has a decimal point → stored as a float."},
        {"line": 4, "text": "True (capital T, no quotes) is a bool — one of Python's two truth values."},
        {"line": 6, "text": "print reads both boxes and shows their current contents: Ada 36."},
        {"line": 7, "text": "type(age) asks \"what kind of value is in this box?\" — it answers <class 'int'>."},
    ],
    ("python-fundamentals", "numbers-and-math"): [
        {"line": 1, "text": "price holds the float 19.99."},
        {"line": 2, "text": "quantity holds the int 3."},
        {"line": 3, "text": "The RIGHT side runs first: 19.99 × 3 = 59.97. Only then is the result stored in total."},
        {"line": 4, "text": "print shows what's in total: 59.97."},
        {"line": 6, "text": "// is floor division: 17 ÷ 5 = 3 remainder 2 — keep the 3, drop the rest."},
        {"line": 7, "text": "% is modulo — it keeps only the remainder: 2."},
        {"line": 8, "text": "** is power: 2 multiplied by itself 8 times = 256."},
    ],
    ("python-fundamentals", "strings"): [
        {"line": 1, "text": "name stores the string \"Grace\"."},
        {"line": 2, "text": "lang stores \"python\"."},
        {"line": 4, "text": ".upper() creates a NEW uppercase copy — \"PYTHON\" — and print shows it. The original lang is untouched."},
        {"line": 5, "text": "len() counts the characters in \"python\": 6."},
        {"line": 6, "text": "The f-string scans for {curly braces} and swaps each for its value — {name} → Grace, {lang.title()} → Python. One readable line."},
    ],
    ("python-fundamentals", "conditionals"): [
        {"line": 1, "text": "score is set to 87."},
        {"line": 3, "text": "First check: is 87 >= 90? No — this branch is skipped entirely; its indented line never runs."},
        {"line": 5, "text": "elif runs only because the first check failed. Is 87 >= 80? Yes!"},
        {"line": 6, "text": "The indented body of the winning branch runs: prints \"B grade\"."},
        {"line": 7, "text": "else never even gets looked at — the chain stopped at the first True condition."},
    ],
    ("python-fundamentals", "loops"): [
        {"line": 1, "text": "range(1, 4) produces 1, 2, 3 (stops BEFORE 4). The loop will run once per value, with i taking each in turn."},
        {"line": 2, "text": "The indented body runs 3 times: Round 1, Round 2, Round 3. Then the loop is done."},
        {"line": 4, "text": "countdown starts at 3 — this variable will control the while loop."},
        {"line": 5, "text": "while asks: is countdown > 0? 3 > 0 → yes, enter the body."},
        {"line": 6, "text": "Print the current countdown value."},
        {"line": 7, "text": "countdown -= 1 shrinks it by one — WITHOUT this line the condition never changes and the loop runs forever."},
        {"line": 5, "text": "Back to the top! 2 > 0 → loop again… then 1 > 0… then 0 > 0 is False → exit."},
        {"line": 8, "text": "Execution continues after the loop: Lift off!"},
    ],
    ("python-fundamentals", "fizzbuzz-project"): [
        {"line": 1, "text": "n is 6 — our test number."},
        {"line": 2, "text": "6 % 3 is 0 (6 divides evenly by 3), so this condition is True."},
        {"line": 3, "text": "The body runs: prints \"divisible by 3\"."},
        {"line": 4, "text": "This is a separate if (not elif!), so it's ALSO checked: 6 % 5 is 1, not 0 → False."},
        {"line": 5, "text": "Body skipped. In FizzBuzz you'll chain if/elif instead — order matters!"},
    ],
    ("data-structures", "lists"): [
        {"line": 1, "text": "A list is born with three scores in order. Index 0 is 88, index 1 is 92, index 2 is 79."},
        {"line": 2, "text": ".append(95) grows the list in place — it now has four items."},
        {"line": 3, "text": "Printing a list shows all items in brackets: [88, 92, 79, 95]."},
        {"line": 4, "text": "len() reports 4 items."},
        {"line": 6, "text": "The for loop visits each item in order — s becomes 88, then 92, then 79, then 95."},
        {"line": 7, "text": "The body prints the current s each pass: four lines of output."},
    ],
    ("data-structures", "dictionaries"): [
        {"line": 1, "text": "A dict maps keys to values: \"apples\" → 5, \"pears\" → 12."},
        {"line": 2, "text": "stock[\"apples\"] looks up 5, adds 1, stores 6 back under the same key."},
        {"line": 3, "text": "Assigning to a NEW key simply creates it — \"plums\" → 3 joins the dict."},
        {"line": 5, "text": ".items() hands out (key, value) pairs; the loop unpacks each into fruit and qty."},
        {"line": 6, "text": "Each pass prints one pair — apples: 6, pears: 12, plums: 3."},
    ],
    ("data-structures", "comprehensions"): [
        {"line": 1, "text": "Start with a plain list of six numbers."},
        {"line": 3, "text": "Read it right to left: FOR each n in nums → compute n² → collect results into a new list. Six in, six out."},
        {"line": 4, "text": "This one adds a filter: only n's where n % 2 == 0 survive. Six in, three out — the transform (just n) keeps them as-is."},
        {"line": 5, "text": "squares is [1, 4, 9, 16, 25, 36]."},
        {"line": 6, "text": "evens is [2, 4, 6]. Two loops of logic, two readable lines."},
    ],
    ("functions-oop", "defining-functions"): [
        {"line": 1, "text": "def creates a function named area with two parameters — but the body does NOT run yet. Python just memorises the recipe."},
        {"line": 2, "text": "This line is part of the recipe: when called, multiply the two inputs and hand the result back."},
        {"line": 4, "text": "NOW it runs: area(3, 4) jumps into the function with width=3, height=4, returns 12, and print shows it."},
        {"line": 6, "text": "A second call with different inputs: returns 10 — and this time the result is CAUGHT in a variable instead of printed."},
        {"line": 7, "text": "Because we returned (not printed), we can keep computing with it: 10 + 1 = 11. That's the power of return."},
    ],
    ("functions-oop", "classes-and-objects"): [
        {"line": 1, "text": "class Dog defines a blueprint. Nothing is created yet — it's the cookie cutter, not the cookie."},
        {"line": 2, "text": "__init__ is the setup recipe that will run for every new Dog."},
        {"line": 3, "text": "self.name = name stores the given name ON the instance being built."},
        {"line": 4, "text": "Every new dog also starts with its own empty tricks list."},
        {"line": 6, "text": "learn is a method — a function that lives on the class and receives the instance as self."},
        {"line": 9, "text": "Dog(\"Rex\") builds an actual dog: Python creates a blank instance, runs __init__ with name=\"Rex\", and hands the finished object to rex."},
        {"line": 10, "text": "rex.learn(\"sit\") calls the method — self is rex, so \"sit\" lands in rex's own tricks list."},
        {"line": 11, "text": "Reading rex.name and rex.tricks shows the state this one dog carries: Rex ['sit']."},
    ],
}


def get_walkthrough(course_slug, lesson_slug):
    return WALKTHROUGHS.get((course_slug, lesson_slug))
