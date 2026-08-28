"""Standalone challenge arena — graded, XP-bearing coding problems."""

CHALLENGES = [
    {
        "slug": "sum-of-evens",
        "title": "Sum of Evens",
        "difficulty": "Easy", "xp": 30,
        "prompt": "Print the sum of all even numbers from 1 to 100 inclusive.",
        "starter": "# print one number\n",
        "expected_output": "2550",
        "hint": "sum(range(2, 101, 2)) — or a loop with i % 2 == 0.",
        "solution": "print(sum(range(2, 101, 2)))",
    },
    {
        "slug": "vowel-counter",
        "title": "Vowel Counter",
        "difficulty": "Easy", "xp": 30,
        "prompt": "Count the vowels (a, e, i, o, u) in the string <code>\"programming in python is productive\"</code> and print the count.",
        "starter": 'text = "programming in python is productive"\n# print the vowel count\n',
        "expected_output": "10",
        "hint": "sum(1 for ch in text if ch in \"aeiou\")",
        "solution": 'text = "programming in python is productive"\nprint(sum(1 for ch in text if ch in "aeiou"))',
    },
    {
        "slug": "palindrome-check",
        "title": "Palindrome Check",
        "difficulty": "Easy", "xp": 35,
        "prompt": "Write <code>is_palindrome(s)</code> returning True if <code>s</code> reads the same reversed (ignore case). Print the result for <code>\"Level\"</code> and <code>\"Python\"</code>.",
        "starter": "def is_palindrome(s):\n    pass\n\nprint(is_palindrome(\"Level\"))\nprint(is_palindrome(\"Python\"))\n",
        "expected_output": "True\nFalse",
        "hint": "Lowercase first: s = s.lower(); compare s == s[::-1].",
        "solution": 'def is_palindrome(s):\n    s = s.lower()\n    return s == s[::-1]\n\nprint(is_palindrome("Level"))\nprint(is_palindrome("Python"))',
    },
    {
        "slug": "second-largest",
        "title": "Second Largest",
        "difficulty": "Medium", "xp": 50,
        "prompt": "Print the second-largest distinct value in the starter list.",
        "starter": "nums = [17, 42, 8, 42, 23, 4, 23]\n# print one number\n",
        "expected_output": "23",
        "hint": "Deduplicate with set(), sort, take index [-2].",
        "solution": "nums = [17, 42, 8, 42, 23, 4, 23]\nprint(sorted(set(nums))[-2])",
    },
    {
        "slug": "word-frequency",
        "title": "Word Frequency",
        "difficulty": "Medium", "xp": 50,
        "prompt": "Print the three most common words in the starter text, one per line as <code>word count</code>.",
        "starter": 'text = "the quick fox and the lazy dog and the sleepy cat and the fox"\n# top three words\n',
        "expected_output": "the 4\nand 3\nfox 2",
        "hint": "Counter(text.split()).most_common(3)",
        "solution": 'from collections import Counter\ntext = "the quick fox and the lazy dog and the sleepy cat and the fox"\nfor word, count in Counter(text.split()).most_common(3):\n    print(word, count)',
    },
    {
        "slug": "caesar-cipher",
        "title": "Caesar Cipher",
        "difficulty": "Medium", "xp": 55,
        "prompt": "Shift every lowercase letter in <code>\"hello world\"</code> forward by 3 (wrapping z→c), keep spaces, and print the result.",
        "starter": 'message = "hello world"\nshift = 3\n# print the encoded message\n',
        "expected_output": "khoor zruog",
        "hint": "chr((ord(ch) - ord('a') + shift) % 26 + ord('a')) for letters; keep spaces as-is.",
        "solution": 'message = "hello world"\nshift = 3\nresult = ""\nfor ch in message:\n    if ch == " ":\n        result += ch\n    else:\n        result += chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))\nprint(result)',
    },
    {
        "slug": "fibonacci",
        "title": "Fibonacci Sequence",
        "difficulty": "Medium", "xp": 50,
        "prompt": "Print the first 10 Fibonacci numbers (starting 0, 1) on one line separated by spaces.",
        "starter": "# 0 1 1 2 3 5 8 13 21 34\n",
        "expected_output": "0 1 1 2 3 5 8 13 21 34",
        "hint": "Track a, b = 0, 1; append to a list; print(\" \".join(map(str, fibs))).",
        "solution": 'fibs = []\na, b = 0, 1\nfor _ in range(10):\n    fibs.append(a)\n    a, b = b, a + b\nprint(" ".join(map(str, fibs)))',
    },
    {
        "slug": "prime-sieve",
        "title": "Prime Hunter",
        "difficulty": "Hard", "xp": 75,
        "prompt": "Print all prime numbers between 2 and 50 on one line separated by spaces.",
        "starter": "# primes up to 50\n",
        "expected_output": "2 3 5 7 11 13 17 19 23 29 31 37 41 43 47",
        "hint": "A number n is prime if no i in range(2, int(n**0.5)+1) divides it.",
        "solution": 'primes = []\nfor n in range(2, 51):\n    is_prime = True\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            is_prime = False\n            break\n    if is_prime:\n        primes.append(str(n))\nprint(" ".join(primes))',
    },
    {
        "slug": "matrix-diagonal",
        "title": "Matrix Diagonals",
        "difficulty": "Hard", "xp": 75,
        "prompt": "For the 3×3 matrix in the starter, print the sum of the main diagonal, then the sum of the anti-diagonal.",
        "starter": "matrix = [\n    [5, 1, 3],\n    [2, 8, 4],\n    [7, 6, 9],\n]\n# two prints\n",
        "expected_output": "22\n18",
        "hint": "Main: matrix[i][i]. Anti: matrix[i][len(matrix)-1-i].",
        "solution": "matrix = [\n    [5, 1, 3],\n    [2, 8, 4],\n    [7, 6, 9],\n]\nn = len(matrix)\nprint(sum(matrix[i][i] for i in range(n)))\nprint(sum(matrix[i][n - 1 - i] for i in range(n)))",
    },
    {
        "slug": "api-rate-limiter",
        "title": "API Rate Limiter",
        "difficulty": "Hard", "xp": 90,
        "prompt": "Implement <code>allow(timestamps, window, limit)</code>: given sorted request timestamps (seconds), return how many requests would be <em>rejected</em> if only <code>limit</code> requests are allowed per rolling <code>window</code> seconds. Process requests in order; a request is rejected if the number of <em>accepted</em> requests in the last <code>window</code> seconds (inclusive) has reached <code>limit</code>. Print the result for the starter data.",
        "starter": "def allow(timestamps, window, limit):\n    # return number of rejected requests\n    pass\n\nrequests = [1, 2, 2, 3, 4, 10, 10, 11, 12, 12]\nprint(allow(requests, window=5, limit=3))\n",
        "expected_output": "4",
        "hint": "Keep a list of accepted timestamps; for each request count accepted ones with t > current - window; reject if count >= limit.",
        "solution": "def allow(timestamps, window, limit):\n    accepted = []\n    rejected = 0\n    for t in timestamps:\n        recent = [a for a in accepted if a > t - window]\n        if len(recent) >= limit:\n            rejected += 1\n        else:\n            accepted.append(t)\n    return rejected\n\nrequests = [1, 2, 2, 3, 4, 10, 10, 11, 12, 12]\nprint(allow(requests, window=5, limit=3))",
    },
    {
        "slug": 'roman-numerals',
        "title": 'Roman Numerals',
        "difficulty": 'Medium', "xp": 55,
        "prompt": ('Write <code>to_roman(n)</code> converting an integer (1–3999) to a Roman numeral. Print the '
 'result for <code>4</code>, <code>44</code>, <code>1994</code> and <code>3999</code>.'),
        "starter": 'def to_roman(n):\n    pass\n\nfor n in (4, 44, 1994, 3999):\n    print(to_roman(n))\n',
        "expected_output": 'IV\nXLIV\nMCMXCIV\nMMMCMXCIX',
        "hint": ('Walk a value→symbol table from largest to smallest, including the subtractive pairs (900 CM, 400 '
 'CD, 90 XC, 40 XL, 9 IX, 4 IV).'),
        "solution": ('def to_roman(n):\n'
 '    table = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),\n'
 '             (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),\n'
 '             (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]\n'
 '    out = ""\n'
 '    for value, symbol in table:\n'
 '        while n >= value:\n'
 '            out += symbol\n'
 '            n -= value\n'
 '    return out\n'
 '\n'
 'for n in (4, 44, 1994, 3999):\n'
 '    print(to_roman(n))'),
    },
    {
        "slug": 'balanced-brackets',
        "title": 'Balanced Brackets',
        "difficulty": 'Medium', "xp": 55,
        "prompt": ('Write <code>is_balanced(s)</code> returning True when every bracket <code>()[]{}</code> is '
 'closed in the right order. Print the result for four test strings.'),
        "starter": ('def is_balanced(s):\n'
 '    pass\n'
 '\n'
 'for test in ("{[()]}", "{[(])}", "((()))", "(]"):\n'
 '    print(f"{test} {is_balanced(test)}")\n'),
        "expected_output": '{[()]} True\n{[(])} False\n((())) True\n(] False',
        "hint": ('Push opening brackets onto a stack; on a closer, the popped item must be its partner. The stack '
 'must be empty at the end.'),
        "solution": ('def is_balanced(s):\n'
 '    pairs = {")": "(", "]": "[", "}": "{"}\n'
 '    stack = []\n'
 '    for ch in s:\n'
 '        if ch in "([{":\n'
 '            stack.append(ch)\n'
 '        elif ch in pairs:\n'
 '            if not stack or stack.pop() != pairs[ch]:\n'
 '                return False\n'
 '    return not stack\n'
 '\n'
 'for test in ("{[()]}", "{[(])}", "((()))", "(]"):\n'
 '    print(f"{test} {is_balanced(test)}")'),
    },
    {
        "slug": 'run-length',
        "title": 'Run-Length Encoding',
        "difficulty": 'Medium', "xp": 50,
        "prompt": ('Compress a string so <code>aaabccddd</code> becomes <code>a3b1c2d3</code>, then write the '
 'decoder and prove it round-trips.'),
        "starter": ('def encode(s):\n'
 '    pass\n'
 '\n'
 'def decode(s):\n'
 '    pass\n'
 '\n'
 'text = "aaabccddd"\n'
 'print(encode(text))\n'
 'print(decode(encode(text)))\n'
 'print(decode(encode(text)) == text)\n'),
        "expected_output": 'a3b1c2d3\naaabccddd\nTrue',
        "hint": ('Walk the string tracking the current character and a count; flush when it changes. For decode, '
 'pair each letter with the digits that follow it.'),
        "solution": ('def encode(s):\n'
 '    out = ""\n'
 '    count = 1\n'
 '    for i in range(1, len(s) + 1):\n'
 '        if i < len(s) and s[i] == s[i - 1]:\n'
 '            count += 1\n'
 '        else:\n'
 '            out += s[i - 1] + str(count)\n'
 '            count = 1\n'
 '    return out\n'
 '\n'
 'def decode(s):\n'
 '    out = ""\n'
 '    i = 0\n'
 '    while i < len(s):\n'
 '        ch = s[i]\n'
 '        j = i + 1\n'
 '        while j < len(s) and s[j].isdigit():\n'
 '            j += 1\n'
 '        out += ch * int(s[i + 1:j])\n'
 '        i = j\n'
 '    return out\n'
 '\n'
 'text = "aaabccddd"\n'
 'print(encode(text))\n'
 'print(decode(encode(text)))\n'
 'print(decode(encode(text)) == text)'),
    },
    {
        "slug": 'two-sum',
        "title": 'Two Sum',
        "difficulty": 'Medium', "xp": 60,
        "prompt": ('Given a list and a target, return the <em>indices</em> of the two numbers summing to it — in one '
 'pass, not nested loops. Print the result for three cases.'),
        "starter": ('def two_sum(nums, target):\n'
 '    pass\n'
 '\n'
 'print(two_sum([2, 7, 11, 15], 9))\n'
 'print(two_sum([3, 2, 4], 6))\n'
 'print(two_sum([1, 2, 3], 99))\n'),
        "expected_output": '[0, 1]\n[1, 2]\n[]',
        "hint": ('Keep a dict of value→index as you go. For each number, check whether target - number is already '
 'in it.'),
        "solution": ('def two_sum(nums, target):\n'
 '    seen = {}\n'
 '    for i, n in enumerate(nums):\n'
 '        if target - n in seen:\n'
 '            return [seen[target - n], i]\n'
 '        seen[n] = i\n'
 '    return []\n'
 '\n'
 'print(two_sum([2, 7, 11, 15], 9))\n'
 'print(two_sum([3, 2, 4], 6))\n'
 'print(two_sum([1, 2, 3], 99))'),
    },
    {
        "slug": 'group-anagrams',
        "title": 'Group Anagrams',
        "difficulty": 'Hard', "xp": 75,
        "prompt": ('Group words that are anagrams of each other. Print one line per group: the sorted words joined '
 'by spaces, groups ordered by first appearance.'),
        "starter": ('words = ["eat", "tea", "tan", "ate", "nat", "bat"]\n'
 '# group anagrams, print each group as space-joined sorted words\n'),
        "expected_output": 'ate eat tea\nnat tan\nbat',
        "hint": 'The sorted letters of a word make a key every anagram shares: "".join(sorted(word)).',
        "solution": ('words = ["eat", "tea", "tan", "ate", "nat", "bat"]\n'
 'groups = {}\n'
 'for word in words:\n'
 '    groups.setdefault("".join(sorted(word)), []).append(word)\n'
 'for key, group in groups.items():\n'
 '    print(" ".join(sorted(group)))'),
    },
    {
        "slug": 'binary-search',
        "title": 'Binary Search',
        "difficulty": 'Medium', "xp": 55,
        "prompt": ('Implement binary search returning the index of a target in a sorted list, or -1. Print the index '
 'for four targets and the number of comparisons for one of them.'),
        "starter": ('def binary_search(values, target):\n'
 '    pass\n'
 '\n'
 'values = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]\n'
 'for t in (1, 9, 19, 8):\n'
 '    print(binary_search(values, t))\n'),
        "expected_output": '0\n4\n9\n-1',
        "hint": 'Keep lo and hi bounds; compare the middle and discard half each step.',
        "solution": ('def binary_search(values, target):\n'
 '    lo, hi = 0, len(values) - 1\n'
 '    while lo <= hi:\n'
 '        mid = (lo + hi) // 2\n'
 '        if values[mid] == target:\n'
 '            return mid\n'
 '        if values[mid] < target:\n'
 '            lo = mid + 1\n'
 '        else:\n'
 '            hi = mid - 1\n'
 '    return -1\n'
 '\n'
 'values = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]\n'
 'for t in (1, 9, 19, 8):\n'
 '    print(binary_search(values, t))'),
    },
    {
        "slug": 'merge-intervals',
        "title": 'Merge Intervals',
        "difficulty": 'Hard', "xp": 80,
        "prompt": ('Merge overlapping intervals and print each surviving interval as <code>start-end</code>, one per '
 'line.'),
        "starter": ('intervals = [(1, 3), (8, 10), (2, 6), (15, 18), (9, 12)]\n'
 '# sort, merge overlaps, print each as start-end\n'),
        "expected_output": '1-6\n8-12\n15-18',
        "hint": ('Sort by start. If the next interval starts at or before the current end, extend the end to the '
 'max of the two.'),
        "solution": ('intervals = [(1, 3), (8, 10), (2, 6), (15, 18), (9, 12)]\n'
 'merged = []\n'
 'for start, end in sorted(intervals):\n'
 '    if merged and start <= merged[-1][1]:\n'
 '        merged[-1][1] = max(merged[-1][1], end)\n'
 '    else:\n'
 '        merged.append([start, end])\n'
 'for start, end in merged:\n'
 '    print(f"{start}-{end}")'),
    },
    {
        "slug": 'word-ladder-cost',
        "title": 'Edit Distance',
        "difficulty": 'Hard', "xp": 90,
        "prompt": ('Compute Levenshtein distance — the fewest single-character insertions, deletions or '
 'substitutions turning one word into another. Print it for four pairs.'),
        "starter": ('def edit_distance(a, b):\n'
 '    pass\n'
 '\n'
 'for x, y in (("kitten", "sitting"), ("flaw", "lawn"), ("abc", "abc"), ("", "hello")):\n'
 '    print(f"{x!r} -> {y!r}: {edit_distance(x, y)}")\n'),
        "expected_output": "'kitten' -> 'sitting': 3\n'flaw' -> 'lawn': 2\n'abc' -> 'abc': 0\n'' -> 'hello': 5",
        "hint": ('Build a (len(a)+1) x (len(b)+1) table. Each cell is 1 + the cheapest of '
 'delete/insert/substitute, or the diagonal when the characters match.'),
        "solution": ('def edit_distance(a, b):\n'
 '    prev = list(range(len(b) + 1))\n'
 '    for i, ca in enumerate(a, 1):\n'
 '        cur = [i]\n'
 '        for j, cb in enumerate(b, 1):\n'
 '            if ca == cb:\n'
 '                cur.append(prev[j - 1])\n'
 '            else:\n'
 '                cur.append(1 + min(prev[j], cur[j - 1], prev[j - 1]))\n'
 '        prev = cur\n'
 '    return prev[-1]\n'
 '\n'
 'for x, y in (("kitten", "sitting"), ("flaw", "lawn"), ("abc", "abc"), ("", "hello")):\n'
 '    print(f"{x!r} -> {y!r}: {edit_distance(x, y)}")'),
    },
]


def get_challenge(slug):
    for c in CHALLENGES:
        if c["slug"] == slug:
            return c
    return None
