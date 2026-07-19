"""Real-life guided projects.

Each project is built step by step: every step is graded in the browser
(like challenges) and unlocks the next. `how_it_works` explains the
real-world architecture before the learner writes a line.
"""

PROJECTS = [
    {
        "slug": "personal-budget",
        "title": "Personal Budget Analyzer",
        "level": "Beginner",
        "icon": "wallet",
        "color": "#10b981",
        "xp": 80,
        "minutes": 30,
        "summary": "Turn a month of raw expenses into a full spending report with category totals, percentages and a text bar chart — the same analysis every budgeting app performs.",
        "how_it_works": """
<p>Every budgeting app (YNAB, Revolut analytics, your bank's spending view) runs this exact pipeline:</p>
<ol>
<li><strong>Ingest</strong> — raw transactions arrive as (category, amount) records.</li>
<li><strong>Aggregate</strong> — sum per category with a dictionary.</li>
<li><strong>Analyse</strong> — turn totals into percentages and find the biggest drain.</li>
<li><strong>Present</strong> — format a report humans actually read.</li>
</ol>
<p>You'll build each stage as its own step — by the end you have a working analyzer you could point at your own bank export.</p>
""",
        "steps": [
            {
                "title": "Total up the month",
                "prompt": "Loop over <code>expenses</code> and print the total as <code>Total spent: 1295</code>.",
                "starter": 'expenses = [("rent", 800), ("food", 240), ("transport", 90), ("fun", 120), ("subscriptions", 45)]\n# sum the amounts and print the total\n',
                "expected_output": "Total spent: 1295",
                "hint": "Unpack in the loop: for category, amount in expenses: — add each amount to a running total.",
                "solution": 'expenses = [("rent", 800), ("food", 240), ("transport", 90), ("fun", 120), ("subscriptions", 45)]\ntotal = 0\nfor category, amount in expenses:\n    total += amount\nprint(f"Total spent: {total}")',
            },
            {
                "title": "Group by category",
                "prompt": "Real data has repeat categories. Build a dict of per-category totals and print each as <code>category: total</code> (in first-seen order).",
                "starter": 'expenses = [("food", 120), ("rent", 800), ("food", 95), ("transport", 60), ("fun", 150), ("transport", 40)]\ntotals = {}\n# fill totals, then print each line\n',
                "expected_output": "food: 215\nrent: 800\ntransport: 100\nfun: 150",
                "hint": "totals[category] = totals.get(category, 0) + amount — then loop totals.items().",
                "solution": 'expenses = [("food", 120), ("rent", 800), ("food", 95), ("transport", 60), ("fun", 150), ("transport", 40)]\ntotals = {}\nfor category, amount in expenses:\n    totals[category] = totals.get(category, 0) + amount\nfor category, amount in totals.items():\n    print(f"{category}: {amount}")',
            },
            {
                "title": "Percentages & the biggest drain",
                "prompt": "Print each category as <code>category: XX.X%</code> of total spending (1 decimal), then <code>Biggest: rent</code> for the largest category.",
                "starter": 'totals = {"food": 215, "rent": 800, "transport": 100, "fun": 150}\ngrand = sum(totals.values())\n# percentages, then the biggest category\n',
                "expected_output": "food: 17.0%\nrent: 63.2%\ntransport: 7.9%\nfun: 11.9%\nBiggest: rent",
                "hint": 'f"{amount / grand * 100:.1f}%" formats the share; max(totals, key=totals.get) finds the biggest key.',
                "solution": 'totals = {"food": 215, "rent": 800, "transport": 100, "fun": 150}\ngrand = sum(totals.values())\nfor category, amount in totals.items():\n    print(f"{category}: {amount / grand * 100:.1f}%")\nprint(f"Biggest: {max(totals, key=totals.get)}")',
            },
            {
                "title": "The final report",
                "prompt": "Ship it: print a header <code>=== July Budget ===</code>, one aligned line per category (<code>{category:&lt;12}{amount}</code> plus a bar of <code>#</code> per full 100), and <code>Total: 1265</code>.",
                "starter": 'totals = {"food": 215, "rent": 800, "transport": 100, "fun": 150}\n# header, aligned rows with # bars, total\n',
                "expected_output": "=== July Budget ===\nfood        215 ##\nrent        800 ########\ntransport   100 #\nfun         150 #\nTotal: 1265",
                "hint": 'f"{category:<12}{amount} " + "#" * (amount // 100) — the :<12 pads the name to 12 characters.',
                "solution": 'totals = {"food": 215, "rent": 800, "transport": 100, "fun": 150}\nprint("=== July Budget ===")\nfor category, amount in totals.items():\n    print(f"{category:<12}{amount} " + "#" * (amount // 100))\nprint(f"Total: {sum(totals.values())}")',
            },
        ],
    },
    {
        "slug": "password-auditor",
        "title": "Password Strength Auditor",
        "level": "Beginner",
        "icon": "lock",
        "color": "#6366f1",
        "xp": 90,
        "minutes": 35,
        "summary": "Build the password checker every signup form runs: length rules, character variety, a scoring engine, and a batch audit that flags weak passwords.",
        "how_it_works": """
<p>When a signup form says "password too weak", this is the code behind it:</p>
<ol>
<li><strong>Rules</strong> — small boolean functions, one per rule (length, digits, case…).</li>
<li><strong>Scoring</strong> — combine rule results into a score, map score → rating.</li>
<li><strong>Batch audit</strong> — run the scorer over many passwords and report the weak ones, exactly what a security team does after a breach.</li>
</ol>
<p>Small pure functions composed into a pipeline — this is professional code structure in miniature.</p>
""",
        "steps": [
            {
                "title": "The length rule",
                "prompt": "Write <code>is_long_enough(pw)</code> returning True when the password has at least 10 characters. Print the result for <code>\"secret\"</code> and <code>\"correcthorse\"</code>.",
                "starter": 'def is_long_enough(pw):\n    # return a boolean\n    pass\n\nprint(is_long_enough("secret"))\nprint(is_long_enough("correcthorse"))\n',
                "expected_output": "False\nTrue",
                "hint": "return len(pw) >= 10 — a comparison already IS a boolean; no if needed.",
                "solution": 'def is_long_enough(pw):\n    return len(pw) >= 10\n\nprint(is_long_enough("secret"))\nprint(is_long_enough("correcthorse"))',
            },
            {
                "title": "The variety rule",
                "prompt": "Write <code>has_variety(pw)</code>: True only if the password contains at least one digit, one uppercase and one lowercase letter. Test on <code>\"password1\"</code> and <code>\"Password1\"</code>.",
                "starter": 'def has_variety(pw):\n    # any() + str methods: .isdigit(), .isupper(), .islower()\n    pass\n\nprint(has_variety("password1"))\nprint(has_variety("Password1"))\n',
                "expected_output": "False\nTrue",
                "hint": "any(ch.isdigit() for ch in pw) checks digits — combine three of these with and.",
                "solution": 'def has_variety(pw):\n    has_digit = any(ch.isdigit() for ch in pw)\n    has_upper = any(ch.isupper() for ch in pw)\n    has_lower = any(ch.islower() for ch in pw)\n    return has_digit and has_upper and has_lower\n\nprint(has_variety("password1"))\nprint(has_variety("Password1"))',
            },
            {
                "title": "The scoring engine",
                "prompt": "Write <code>strength(pw)</code>: score +1 each for length ≥ 10, any digit, any uppercase, any symbol from <code>!@#$%^&*</code>. Return <code>\"weak\"</code> (0–1), <code>\"okay\"</code> (2–3) or <code>\"strong\"</code> (4). Test the three prints.",
                "starter": 'def strength(pw):\n    score = 0\n    # four rules, then map score to a rating\n    pass\n\nprint(strength("cat"))\nprint(strength("Tr0ub4dor!"))\nprint(strength("password123"))\n',
                "expected_output": "weak\nstrong\nokay",
                "hint": "score += len(pw) >= 10 works — True counts as 1! Symbols: any(ch in \"!@#$%^&*\" for ch in pw).",
                "solution": 'def strength(pw):\n    score = 0\n    score += len(pw) >= 10\n    score += any(ch.isdigit() for ch in pw)\n    score += any(ch.isupper() for ch in pw)\n    score += any(ch in "!@#$%^&*" for ch in pw)\n    if score <= 1:\n        return "weak"\n    if score <= 3:\n        return "okay"\n    return "strong"\n\nprint(strength("cat"))\nprint(strength("Tr0ub4dor!"))\nprint(strength("password123"))',
            },
            {
                "title": "The batch audit",
                "prompt": "Run the auditor over the list: print each <em>weak</em> password as <code>name: weak</code>, then a summary <code>2 of 4 passwords need changing</code>.",
                "starter": 'def strength(pw):\n    score = 0\n    score += len(pw) >= 10\n    score += any(ch.isdigit() for ch in pw)\n    score += any(ch.isupper() for ch in pw)\n    score += any(ch in "!@#$%^&*" for ch in pw)\n    if score <= 1:\n        return "weak"\n    if score <= 3:\n        return "okay"\n    return "strong"\n\npasswords = ["hunter2", "Sup3rSecret!", "letmein", "N1nja#Warrior"]\n# audit and summarise\n',
                "expected_output": "hunter2: weak\nletmein: weak\n2 of 4 passwords need changing",
                "hint": "Count the weak ones while looping, print each as you find it, then the summary line.",
                "solution": 'def strength(pw):\n    score = 0\n    score += len(pw) >= 10\n    score += any(ch.isdigit() for ch in pw)\n    score += any(ch.isupper() for ch in pw)\n    score += any(ch in "!@#$%^&*" for ch in pw)\n    if score <= 1:\n        return "weak"\n    if score <= 3:\n        return "okay"\n    return "strong"\n\npasswords = ["hunter2", "Sup3rSecret!", "letmein", "N1nja#Warrior"]\nweak = 0\nfor pw in passwords:\n    if strength(pw) == "weak":\n        print(f"{pw}: weak")\n        weak += 1\nprint(f"{weak} of {len(passwords)} passwords need changing")',
            },
        ],
    },
    {
        "slug": "todo-manager",
        "title": "To-Do Manager with File Persistence",
        "level": "Intermediate",
        "icon": "checklist",
        "color": "#06b6d4",
        "xp": 100,
        "minutes": 40,
        "summary": "A real CRUD app in miniature: add and complete tasks, persist them to disk so nothing is lost on restart, and report progress — the heart of Todoist, Trello and every task app.",
        "how_it_works": """
<p>Every task app is CRUD — <strong>C</strong>reate, <strong>R</strong>ead, <strong>U</strong>pdate, <strong>D</strong>elete — plus persistence:</p>
<ol>
<li><strong>State</strong> — tasks live in memory as a list of dicts (like a mini database table).</li>
<li><strong>Operations</strong> — add and complete are functions that modify state.</li>
<li><strong>Persistence</strong> — state is serialised to a file and reloaded on startup; without this, a restart wipes everything.</li>
<li><strong>Reporting</strong> — aggregate state into stats users care about.</li>
</ol>
<p>Swap the file for SQLite and the print for HTML and you literally have a web app — that's the whole secret.</p>
""",
        "steps": [
            {
                "title": "Create & read",
                "prompt": "Implement <code>add_task(title)</code> appending <code>{\"id\": next_id, \"title\": title, \"done\": False}</code> (ids start at 1). Add the three tasks, then print each as <code>1. [ ] buy milk</code>.",
                "starter": 'tasks = []\n\ndef add_task(title):\n    # append a dict with id, title, done\n    pass\n\nadd_task("buy milk")\nadd_task("walk dog")\nadd_task("write code")\n# print the list\n',
                "expected_output": "1. [ ] buy milk\n2. [ ] walk dog\n3. [ ] write code",
                "hint": "id is len(tasks) + 1. The checkbox: 'x' if t[\"done\"] else ' ' inside an f-string.",
                "solution": 'tasks = []\n\ndef add_task(title):\n    tasks.append({"id": len(tasks) + 1, "title": title, "done": False})\n\nadd_task("buy milk")\nadd_task("walk dog")\nadd_task("write code")\nfor t in tasks:\n    box = "x" if t["done"] else " "\n    print(f"{t[\'id\']}. [{box}] {t[\'title\']}")',
            },
            {
                "title": "Update: complete a task",
                "prompt": "Implement <code>complete_task(task_id)</code> that marks the matching task done. Complete task 2, then print the list — task 2 shows <code>[x]</code>.",
                "starter": 'tasks = [\n    {"id": 1, "title": "buy milk", "done": False},\n    {"id": 2, "title": "walk dog", "done": False},\n    {"id": 3, "title": "write code", "done": False},\n]\n\ndef complete_task(task_id):\n    # find the task and set done = True\n    pass\n\ncomplete_task(2)\nfor t in tasks:\n    box = "x" if t["done"] else " "\n    print(f"{t[\'id\']}. [{box}] {t[\'title\']}")\n',
                "expected_output": "1. [ ] buy milk\n2. [x] walk dog\n3. [ ] write code",
                "hint": "Loop the tasks; when t[\"id\"] == task_id, set t[\"done\"] = True.",
                "solution": 'tasks = [\n    {"id": 1, "title": "buy milk", "done": False},\n    {"id": 2, "title": "walk dog", "done": False},\n    {"id": 3, "title": "write code", "done": False},\n]\n\ndef complete_task(task_id):\n    for t in tasks:\n        if t["id"] == task_id:\n            t["done"] = True\n\ncomplete_task(2)\nfor t in tasks:\n    box = "x" if t["done"] else " "\n    print(f"{t[\'id\']}. [{box}] {t[\'title\']}")',
            },
            {
                "title": "Persistence: save & load",
                "prompt": "Save each task to <code>todo.txt</code> as <code>id|done|title</code> (done as 0/1), then load the file back into a new list and print the count and the second task's title: <code>3 walk dog</code>.",
                "starter": 'tasks = [\n    {"id": 1, "title": "buy milk", "done": False},\n    {"id": 2, "title": "walk dog", "done": True},\n    {"id": 3, "title": "write code", "done": False},\n]\n\n# 1) write tasks to todo.txt as id|done|title lines\n# 2) read the file into loaded = [...]\n# 3) print(len(loaded), loaded[1]["title"])\n',
                "expected_output": "3 walk dog",
                "hint": 'Write f"{t[\'id\']}|{int(t[\'done\'])}|{t[\'title\']}\\n". Read with line.strip().split("|") and rebuild each dict.',
                "solution": 'tasks = [\n    {"id": 1, "title": "buy milk", "done": False},\n    {"id": 2, "title": "walk dog", "done": True},\n    {"id": 3, "title": "write code", "done": False},\n]\n\nwith open("todo.txt", "w") as f:\n    for t in tasks:\n        f.write(f"{t[\'id\']}|{int(t[\'done\'])}|{t[\'title\']}\\n")\n\nloaded = []\nwith open("todo.txt") as f:\n    for line in f:\n        task_id, done, title = line.strip().split("|")\n        loaded.append({"id": int(task_id), "title": title, "done": done == "1"})\n\nprint(len(loaded), loaded[1]["title"])',
            },
            {
                "title": "The progress report",
                "prompt": "Print one summary line: <code>3 tasks: 1 done, 2 pending (33% complete)</code> — percentage rounded to a whole number.",
                "starter": 'tasks = [\n    {"id": 1, "title": "buy milk", "done": False},\n    {"id": 2, "title": "walk dog", "done": True},\n    {"id": 3, "title": "write code", "done": False},\n]\n# one print\n',
                "expected_output": "3 tasks: 1 done, 2 pending (33% complete)",
                "hint": "done = sum(1 for t in tasks if t[\"done\"]) — then round(done / len(tasks) * 100).",
                "solution": 'tasks = [\n    {"id": 1, "title": "buy milk", "done": False},\n    {"id": 2, "title": "walk dog", "done": True},\n    {"id": 3, "title": "write code", "done": False},\n]\ndone = sum(1 for t in tasks if t["done"])\npending = len(tasks) - done\npct = round(done / len(tasks) * 100)\nprint(f"{len(tasks)} tasks: {done} done, {pending} pending ({pct}% complete)")',
            },
        ],
    },
    {
        "slug": "sales-dashboard",
        "title": "Sales Report Generator",
        "level": "Intermediate",
        "icon": "chart",
        "color": "#f59e0b",
        "xp": 110,
        "minutes": 45,
        "summary": "From raw CSV export to an executive report: parse sales data, compute revenue by product and month, find the winners, and generate the summary a manager actually reads.",
        "how_it_works": """
<p>This is the daily reality of data analysts and the core of every BI tool (Tableau, Power BI, Excel pivot tables):</p>
<ol>
<li><strong>Extract</strong> — parse the CSV export (with the csv module — never by hand).</li>
<li><strong>Transform</strong> — convert types (CSV is all strings!) and aggregate revenue by product and by month.</li>
<li><strong>Analyse</strong> — rank: top product, best month.</li>
<li><strong>Load/Report</strong> — output the formatted summary.</li>
</ol>
<p>Data engineers call this pipeline <strong>ETL</strong>. You're about to build one end-to-end.</p>
""",
        "steps": [
            {
                "title": "Extract: parse the CSV",
                "prompt": "Parse <code>raw</code> with <code>csv.DictReader</code>, then print the number of rows and the first row's product: <code>6</code> then <code>laptop</code>.",
                "starter": 'import csv, io\nraw = """month,product,units,price\nJan,laptop,3,900\nJan,mouse,10,25\nFeb,laptop,2,900\nFeb,keyboard,5,60\nMar,laptop,4,900\nMar,mouse,8,25"""\n\nrows = list(csv.DictReader(io.StringIO(raw)))\n# two prints\n',
                "expected_output": "6\nlaptop",
                "hint": 'print(len(rows)) then print(rows[0]["product"]).',
                "solution": 'import csv, io\nraw = """month,product,units,price\nJan,laptop,3,900\nJan,mouse,10,25\nFeb,laptop,2,900\nFeb,keyboard,5,60\nMar,laptop,4,900\nMar,mouse,8,25"""\n\nrows = list(csv.DictReader(io.StringIO(raw)))\nprint(len(rows))\nprint(rows[0]["product"])',
            },
            {
                "title": "Transform: revenue per product",
                "prompt": "Revenue for a row is <code>units × price</code> (convert to int!). Total it per product and print each as <code>product: revenue</code> in first-seen order.",
                "starter": 'import csv, io\nraw = """month,product,units,price\nJan,laptop,3,900\nJan,mouse,10,25\nFeb,laptop,2,900\nFeb,keyboard,5,60\nMar,laptop,4,900\nMar,mouse,8,25"""\nrows = list(csv.DictReader(io.StringIO(raw)))\n\nby_product = {}\n# aggregate, then print\n',
                "expected_output": "laptop: 8100\nmouse: 450\nkeyboard: 300",
                "hint": 'rev = int(row["units"]) * int(row["price"]); by_product[p] = by_product.get(p, 0) + rev.',
                "solution": 'import csv, io\nraw = """month,product,units,price\nJan,laptop,3,900\nJan,mouse,10,25\nFeb,laptop,2,900\nFeb,keyboard,5,60\nMar,laptop,4,900\nMar,mouse,8,25"""\nrows = list(csv.DictReader(io.StringIO(raw)))\n\nby_product = {}\nfor row in rows:\n    rev = int(row["units"]) * int(row["price"])\n    by_product[row["product"]] = by_product.get(row["product"], 0) + rev\nfor product, rev in by_product.items():\n    print(f"{product}: {rev}")',
            },
            {
                "title": "Analyse: revenue per month",
                "prompt": "Aggregate revenue per month, print each as <code>month: revenue</code>, then <code>Best month: Mar</code>.",
                "starter": 'import csv, io\nraw = """month,product,units,price\nJan,laptop,3,900\nJan,mouse,10,25\nFeb,laptop,2,900\nFeb,keyboard,5,60\nMar,laptop,4,900\nMar,mouse,8,25"""\nrows = list(csv.DictReader(io.StringIO(raw)))\n\nby_month = {}\n# aggregate, print months, then the best one\n',
                "expected_output": "Jan: 2950\nFeb: 2100\nMar: 3800\nBest month: Mar",
                "hint": "Same .get() pattern keyed on row[\"month\"]; best = max(by_month, key=by_month.get).",
                "solution": 'import csv, io\nraw = """month,product,units,price\nJan,laptop,3,900\nJan,mouse,10,25\nFeb,laptop,2,900\nFeb,keyboard,5,60\nMar,laptop,4,900\nMar,mouse,8,25"""\nrows = list(csv.DictReader(io.StringIO(raw)))\n\nby_month = {}\nfor row in rows:\n    rev = int(row["units"]) * int(row["price"])\n    by_month[row["month"]] = by_month.get(row["month"], 0) + rev\nfor month, rev in by_month.items():\n    print(f"{month}: {rev}")\nprint(f"Best month: {max(by_month, key=by_month.get)}")',
            },
            {
                "title": "Report: the executive summary",
                "prompt": "Combine everything into the final report — exactly:<br><code>=== Q1 Sales Report ===</code><br><code>Total revenue: 8850</code><br><code>Top product: laptop (8100)</code><br><code>Best month: Mar (3800)</code>",
                "starter": 'import csv, io\nraw = """month,product,units,price\nJan,laptop,3,900\nJan,mouse,10,25\nFeb,laptop,2,900\nFeb,keyboard,5,60\nMar,laptop,4,900\nMar,mouse,8,25"""\nrows = list(csv.DictReader(io.StringIO(raw)))\n\nby_product = {}\nby_month = {}\n# aggregate both, then print the 4-line report\n',
                "expected_output": "=== Q1 Sales Report ===\nTotal revenue: 8850\nTop product: laptop (8100)\nBest month: Mar (3800)",
                "hint": "top = max(by_product, key=by_product.get) — then f\"Top product: {top} ({by_product[top]})\".",
                "solution": 'import csv, io\nraw = """month,product,units,price\nJan,laptop,3,900\nJan,mouse,10,25\nFeb,laptop,2,900\nFeb,keyboard,5,60\nMar,laptop,4,900\nMar,mouse,8,25"""\nrows = list(csv.DictReader(io.StringIO(raw)))\n\nby_product = {}\nby_month = {}\nfor row in rows:\n    rev = int(row["units"]) * int(row["price"])\n    by_product[row["product"]] = by_product.get(row["product"], 0) + rev\n    by_month[row["month"]] = by_month.get(row["month"], 0) + rev\n\ntop = max(by_product, key=by_product.get)\nbest = max(by_month, key=by_month.get)\nprint("=== Q1 Sales Report ===")\nprint(f"Total revenue: {sum(by_product.values())}")\nprint(f"Top product: {top} ({by_product[top]})")\nprint(f"Best month: {best} ({by_month[best]})")',
            },
        ],
    },
    {
        "slug": "webhook-processor",
        "title": "Webhook Event Processor",
        "level": "Advanced",
        "icon": "webhook",
        "color": "#f43f5e",
        "xp": 130,
        "minutes": 50,
        "summary": "Build what Stripe and PayPal integrations run in production: receive a batch of JSON events, validate them, compute per-user balances, and answer with a proper API response.",
        "how_it_works": """
<p>When a customer pays through Stripe, Stripe <strong>POSTs a webhook</strong> — a JSON event — to the shop's server. The server must:</p>
<ol>
<li><strong>Parse</strong> — decode the JSON payload into Python objects.</li>
<li><strong>Validate</strong> — real traffic contains junk: unknown event types, impossible amounts. Filter, never crash.</li>
<li><strong>Process</strong> — apply business logic: payments add to a balance, refunds subtract.</li>
<li><strong>Respond</strong> — return a JSON summary with an honest status code so the sender knows what happened.</li>
</ol>
<p>This parse → validate → process → respond loop is the beating heart of every backend integration you'll ever build.</p>
""",
        "steps": [
            {
                "title": "Parse the payload",
                "prompt": "Parse the JSON in <code>raw</code> with <code>json.loads</code>. Print how many events arrived and the type of the first one: <code>5</code> then <code>payment</code>.",
                "starter": 'import json\nraw = \'[{"type": "payment", "user": "ana", "amount": 120}, {"type": "refund", "user": "ana", "amount": 30}, {"type": "login", "user": "bo", "amount": 0}, {"type": "payment", "user": "bo", "amount": 80}, {"type": "payment", "user": "ana", "amount": -5}]\'\n\n# parse and print two lines\n',
                "expected_output": "5\npayment",
                "hint": 'events = json.loads(raw) gives a list of dicts — len() and events[0]["type"].',
                "solution": 'import json\nraw = \'[{"type": "payment", "user": "ana", "amount": 120}, {"type": "refund", "user": "ana", "amount": 30}, {"type": "login", "user": "bo", "amount": 0}, {"type": "payment", "user": "bo", "amount": 80}, {"type": "payment", "user": "ana", "amount": -5}]\'\n\nevents = json.loads(raw)\nprint(len(events))\nprint(events[0]["type"])',
            },
            {
                "title": "Validate the events",
                "prompt": "An event is valid when its type is <code>payment</code> or <code>refund</code> AND its amount is > 0. Build the <code>valid</code> list; print how many are valid and how many were rejected: <code>3</code> then <code>2</code>.",
                "starter": 'import json\nraw = \'[{"type": "payment", "user": "ana", "amount": 120}, {"type": "refund", "user": "ana", "amount": 30}, {"type": "login", "user": "bo", "amount": 0}, {"type": "payment", "user": "bo", "amount": 80}, {"type": "payment", "user": "ana", "amount": -5}]\'\nevents = json.loads(raw)\n\n# valid = [...] then two prints\n',
                "expected_output": "3\n2",
                "hint": 'valid = [e for e in events if e["type"] in ("payment", "refund") and e["amount"] > 0]',
                "solution": 'import json\nraw = \'[{"type": "payment", "user": "ana", "amount": 120}, {"type": "refund", "user": "ana", "amount": 30}, {"type": "login", "user": "bo", "amount": 0}, {"type": "payment", "user": "bo", "amount": 80}, {"type": "payment", "user": "ana", "amount": -5}]\'\nevents = json.loads(raw)\n\nvalid = [e for e in events if e["type"] in ("payment", "refund") and e["amount"] > 0]\nprint(len(valid))\nprint(len(events) - len(valid))',
            },
            {
                "title": "Process: per-user balances",
                "prompt": "Payments add to a user's balance; refunds subtract. Compute balances from the valid events and print each user as <code>user: balance</code> (first-seen order): <code>ana: 90</code> then <code>bo: 80</code>.",
                "starter": 'valid = [\n    {"type": "payment", "user": "ana", "amount": 120},\n    {"type": "refund", "user": "ana", "amount": 30},\n    {"type": "payment", "user": "bo", "amount": 80},\n]\n\nbalances = {}\n# apply events, then print\n',
                "expected_output": "ana: 90\nbo: 80",
                "hint": "delta = amount if type == \"payment\" else -amount; balances[user] = balances.get(user, 0) + delta.",
                "solution": 'valid = [\n    {"type": "payment", "user": "ana", "amount": 120},\n    {"type": "refund", "user": "ana", "amount": 30},\n    {"type": "payment", "user": "bo", "amount": 80},\n]\n\nbalances = {}\nfor e in valid:\n    delta = e["amount"] if e["type"] == "payment" else -e["amount"]\n    balances[e["user"]] = balances.get(e["user"], 0) + delta\nfor user, balance in balances.items():\n    print(f"{user}: {balance}")',
            },
            {
                "title": "Respond like an API",
                "prompt": "Build the response dict — <code>{\"status\": 200, \"processed\": 3, \"skipped\": 2, \"balances\": {...}}</code> — and print it with <code>json.dumps</code>. Expected exactly:<br><code>{\"status\": 200, \"processed\": 3, \"skipped\": 2, \"balances\": {\"ana\": 90, \"bo\": 80}}</code>",
                "starter": 'import json\nbalances = {"ana": 90, "bo": 80}\nprocessed = 3\nskipped = 2\n\n# build the response dict in that key order and print json.dumps(response)\n',
                "expected_output": '{"status": 200, "processed": 3, "skipped": 2, "balances": {"ana": 90, "bo": 80}}',
                "hint": "Dicts keep insertion order — create keys in the order shown, then json.dumps(response).",
                "solution": 'import json\nbalances = {"ana": 90, "bo": 80}\nprocessed = 3\nskipped = 2\n\nresponse = {"status": 200, "processed": processed, "skipped": skipped, "balances": balances}\nprint(json.dumps(response))',
            },
        ],
    },
]


def get_project(slug):
    for p in PROJECTS:
        if p["slug"] == slug:
            return p
    return None
