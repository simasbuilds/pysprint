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
        "icon": "shield-key",
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
        "icon": "bar-chart",
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
        "icon": "bolt",
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
    {
        "slug": 'log-analyzer',
        "title": 'Server Log Analyzer',
        "level": 'Intermediate',
        "icon": 'activity',
        "color": '#0ea5e9',
        "xp": 110,
        "minutes": 40,
        "summary": ('Turn a raw access log into the report an on-call engineer actually reads: request volume, error '
 'rate, per-endpoint traffic and p95 latency — the same four numbers every observability dashboard '
 'leads with.'),
        "how_it_works": """
<p>Every monitoring tool — Datadog, Grafana, CloudWatch — runs this pipeline over your logs:</p>
<ol>
<li><strong>Parse</strong> — split unstructured log lines into typed fields.</li>
<li><strong>Aggregate</strong> — group by endpoint and count requests and failures.</li>
<li><strong>Summarise</strong> — collapse thousands of latencies into percentiles, because an average hides the slow tail that users feel.</li>
<li><strong>Report</strong> — rank the endpoints so the worst offender is on the first line.</li>
</ol>
<p>You'll build all four stages. p95 is the number that matters: it means 95% of requests were faster, so it captures the pain an average smooths away.</p>
""",
        "steps": [
            {
                "title": 'Parse and count failures',
                "prompt": ('Split each log line into <code>method path status ms</code>. Print the request count, how many '
 'had a status of 400 or more, and the error rate to one decimal.'),
                "starter": ('logs = [\n'
 '    "GET /api/users 200 143",\n'
 '    "POST /api/orders 201 310",\n'
 '    "GET /api/users 200 98",\n'
 '    "GET /api/health 200 12",\n'
 '    "POST /api/orders 500 842",\n'
 '    "GET /api/users 404 55",\n'
 ']\n'
 '# split each line, count errors (status >= 400), print the three lines\n'),
                "expected_output": 'Requests: 6\nErrors: 2\nError rate: 33.3%',
                "hint": 'line.split() gives four strings; int(status) >= 400 marks a failure.',
                "solution": ('logs = [\n'
 '    "GET /api/users 200 143",\n'
 '    "POST /api/orders 201 310",\n'
 '    "GET /api/users 200 98",\n'
 '    "GET /api/health 200 12",\n'
 '    "POST /api/orders 500 842",\n'
 '    "GET /api/users 404 55",\n'
 ']\n'
 'errors = 0\n'
 'for line in logs:\n'
 '    method, path, status, ms = line.split()\n'
 '    if int(status) >= 400:\n'
 '        errors += 1\n'
 'print(f"Requests: {len(logs)}")\n'
 'print(f"Errors: {errors}")\n'
 'print(f"Error rate: {errors / len(logs) * 100:.1f}%")'),
            },
            {
                "title": 'Traffic per endpoint',
                "prompt": ('Count requests per path and print <code>path count</code>, busiest first. Break ties '
 'alphabetically so the output is stable.'),
                "starter": ('logs = [\n'
 '    "GET /api/users 200 143",\n'
 '    "POST /api/orders 201 310",\n'
 '    "GET /api/users 200 98",\n'
 '    "GET /api/health 200 12",\n'
 '    "POST /api/orders 500 842",\n'
 '    "GET /api/users 404 55",\n'
 ']\n'
 'counts = {}\n'
 '# tally per path, then print sorted by count desc, path asc\n'),
                "expected_output": '/api/users 3\n/api/orders 2\n/api/health 1',
                "hint": 'sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])) sorts by count descending then name.',
                "solution": ('logs = [\n'
 '    "GET /api/users 200 143",\n'
 '    "POST /api/orders 201 310",\n'
 '    "GET /api/users 200 98",\n'
 '    "GET /api/health 200 12",\n'
 '    "POST /api/orders 500 842",\n'
 '    "GET /api/users 404 55",\n'
 ']\n'
 'counts = {}\n'
 'for line in logs:\n'
 '    path = line.split()[1]\n'
 '    counts[path] = counts.get(path, 0) + 1\n'
 'for path, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):\n'
 '    print(f"{path} {n}")'),
            },
            {
                "title": 'Latency percentiles',
                "prompt": ('Write <code>percentile(values, pct)</code> using nearest-rank: sort, then take index '
 '<code>ceil(pct/100 * n) - 1</code>. Print the count, p50, p95 and max.'),
                "starter": ('import math\n'
 '\n'
 'latencies = [143, 310, 98, 12, 842, 55, 201, 77, 460, 133]\n'
 '\n'
 'def percentile(values, pct):\n'
 '    pass\n'
 '\n'
 '# print count, p50, p95, max\n'),
                "expected_output": 'count: 10\np50: 133ms\np95: 842ms\nmax: 842ms',
                "hint": 'math.ceil(pct / 100 * len(ordered)) gives the rank; subtract 1 for the index.',
                "solution": ('import math\n'
 '\n'
 'latencies = [143, 310, 98, 12, 842, 55, 201, 77, 460, 133]\n'
 '\n'
 'def percentile(values, pct):\n'
 '    ordered = sorted(values)\n'
 '    rank = math.ceil(pct / 100 * len(ordered))\n'
 '    return ordered[rank - 1]\n'
 '\n'
 'print(f"count: {len(latencies)}")\n'
 'print(f"p50: {percentile(latencies, 50)}ms")\n'
 'print(f"p95: {percentile(latencies, 95)}ms")\n'
 'print(f"max: {max(latencies)}ms")'),
            },
            {
                "title": 'Ship the report',
                "prompt": ('Combine everything into an aligned table: header <code>=== Traffic Report ===</code>, a column '
 'row, one line per endpoint (busiest first) with requests, errors and p95, then a TOTAL row.'),
                "starter": ('import math\n'
 '\n'
 'logs = [\n'
 '    "GET /api/users 200 143",\n'
 '    "POST /api/orders 201 310",\n'
 '    "GET /api/users 200 98",\n'
 '    "GET /api/health 200 12",\n'
 '    "POST /api/orders 500 842",\n'
 '    "GET /api/users 404 55",\n'
 '    "GET /api/health 200 9",\n'
 '    "POST /api/orders 502 1200",\n'
 ']\n'
 '\n'
 'def percentile(values, pct):\n'
 '    ordered = sorted(values)\n'
 '    return ordered[math.ceil(pct / 100 * len(ordered)) - 1]\n'
 '\n'
 '# build per-endpoint stats, then print the aligned report\n'),
                "expected_output": ('=== Traffic Report ===\n'
 'endpoint       reqs  err    p95\n'
 '/api/users        3    1   143ms\n'
 '/api/orders       3    2  1200ms\n'
 '/api/health       2    0    12ms\n'
 'TOTAL             8    3  1200ms'),
                "hint": ('f"{path:<14}{n:>5}" left-pads names to 14 and right-aligns numbers in 5. setdefault keeps the '
 'per-path accumulator tidy.'),
                "solution": ('import math\n'
 '\n'
 'logs = [\n'
 '    "GET /api/users 200 143",\n'
 '    "POST /api/orders 201 310",\n'
 '    "GET /api/users 200 98",\n'
 '    "GET /api/health 200 12",\n'
 '    "POST /api/orders 500 842",\n'
 '    "GET /api/users 404 55",\n'
 '    "GET /api/health 200 9",\n'
 '    "POST /api/orders 502 1200",\n'
 ']\n'
 '\n'
 'def percentile(values, pct):\n'
 '    ordered = sorted(values)\n'
 '    return ordered[math.ceil(pct / 100 * len(ordered)) - 1]\n'
 '\n'
 'stats = {}\n'
 'for line in logs:\n'
 '    method, path, status, ms = line.split()\n'
 '    s = stats.setdefault(path, {"n": 0, "errors": 0, "ms": []})\n'
 '    s["n"] += 1\n'
 '    s["ms"].append(int(ms))\n'
 '    if int(status) >= 400:\n'
 '        s["errors"] += 1\n'
 '\n'
 'print("=== Traffic Report ===")\n'
 'print(f"{\'endpoint\':<14}{\'reqs\':>5}{\'err\':>5}{\'p95\':>7}")\n'
 'for path, s in sorted(stats.items(), key=lambda kv: -kv[1]["n"]):\n'
 '    print(f"{path:<14}{s[\'n\']:>5}{s[\'errors\']:>5}{percentile(s[\'ms\'], 95):>6}ms")\n'
 'total = sum(s["n"] for s in stats.values())\n'
 'errs = sum(s["errors"] for s in stats.values())\n'
 'print(f"{\'TOTAL\':<14}{total:>5}{errs:>5}{percentile([int(l.split()[3]) for l in logs], '
 '95):>6}ms")'),
            },
        ],
    },
    {
        "slug": 'search-engine',
        "title": 'Mini Search Engine',
        "level": 'Advanced',
        "icon": 'search',
        "color": '#8b5cf6',
        "xp": 140,
        "minutes": 50,
        "summary": ('Build the machinery behind every search box: an inverted index, boolean matching, and TF-IDF '
 'ranking that puts the most relevant document first — the core of Elasticsearch in about forty '
 'lines.'),
        "how_it_works": """
<p>Searching by scanning every document is hopeless at scale. Real engines invert the problem:</p>
<ol>
<li><strong>Index</strong> — map each <em>term</em> to the set of documents containing it. Lookup becomes a dictionary hit instead of a scan.</li>
<li><strong>Match</strong> — intersect those sets to find documents containing every query word.</li>
<li><strong>Weight</strong> — a word in every document tells you nothing; a rare word is a strong signal. That is <em>inverse document frequency</em>.</li>
<li><strong>Rank</strong> — score each match by term frequency times IDF and sort.</li>
</ol>
<p>This is genuinely how Lucene, Elasticsearch and Postgres full-text search begin. You'll build all four stages against a tiny corpus.</p>
""",
        "steps": [
            {
                "title": 'Build the inverted index',
                "prompt": ('Map every word to the set of document ids containing it. Print the number of distinct terms, '
 'then the sorted posting list for <code>python</code>, <code>data</code> and '
 '<code>language</code>.'),
                "starter": ('docs = {\n'
 '    1: "python is a great language for data work",\n'
 '    2: "the python language is easy to read",\n'
 '    3: "data pipelines move data between systems",\n'
 '    4: "reading code is a skill you build",\n'
 '}\n'
 '\n'
 'index = {}\n'
 '# fill index: word -> set of doc ids, then print the three lookups\n'),
                "expected_output": 'terms: 21\npython -> [1, 2]\ndata -> [1, 3]\nlanguage -> [1, 2]',
                "hint": 'index.setdefault(word, set()).add(doc_id) creates the set on first sight.',
                "solution": ('docs = {\n'
 '    1: "python is a great language for data work",\n'
 '    2: "the python language is easy to read",\n'
 '    3: "data pipelines move data between systems",\n'
 '    4: "reading code is a skill you build",\n'
 '}\n'
 'index = {}\n'
 'for doc_id, text in docs.items():\n'
 '    for word in text.split():\n'
 '        index.setdefault(word, set()).add(doc_id)\n'
 '\n'
 'print(f"terms: {len(index)}")\n'
 'for term in ("python", "data", "language"):\n'
 '    print(f"{term} -> {sorted(index[term])}")'),
            },
            {
                "title": 'Boolean AND search',
                "prompt": ('Write <code>search_all(query)</code> returning the sorted ids of documents containing '
 '<em>every</em> query word. Print the result for four queries, including one that matches '
 'nothing.'),
                "starter": ('docs = {\n'
 '    1: "python is a great language for data work",\n'
 '    2: "the python language is easy to read",\n'
 '    3: "data pipelines move data between systems",\n'
 '    4: "reading code is a skill you build",\n'
 '}\n'
 '\n'
 'index = {}\n'
 'for doc_id, text in docs.items():\n'
 '    for word in text.split():\n'
 '        index.setdefault(word, set()).add(doc_id)\n'
 '\n'
 'def search_all(query):\n'
 '    pass\n'
 '\n'
 'for q in ("python language", "data", "python data", "missing"):\n'
 '    print(f"{q!r} -> {search_all(q)}")\n'),
                "expected_output": "'python language' -> [1, 2]\n'data' -> [1, 3]\n'python data' -> [1]\n'missing' -> []",
                "hint": ("Start with the first word's set and intersect (&) the rest. index.get(w, set()) handles unknown "
 'words.'),
                "solution": ('docs = {\n'
 '    1: "python is a great language for data work",\n'
 '    2: "the python language is easy to read",\n'
 '    3: "data pipelines move data between systems",\n'
 '    4: "reading code is a skill you build",\n'
 '}\n'
 'index = {}\n'
 'for doc_id, text in docs.items():\n'
 '    for word in text.split():\n'
 '        index.setdefault(word, set()).add(doc_id)\n'
 '\n'
 'def search_all(query):\n'
 '    words = query.split()\n'
 '    hits = index.get(words[0], set())\n'
 '    for w in words[1:]:\n'
 '        hits = hits & index.get(w, set())\n'
 '    return sorted(hits)\n'
 '\n'
 'for q in ("python language", "data", "python data", "missing"):\n'
 '    print(f"{q!r} -> {search_all(q)}")'),
            },
            {
                "title": 'Score terms with IDF',
                "prompt": ('Document frequency is how many docs contain a term; IDF is <code>log(N / df)</code>. Print df '
 'and idf (3 decimals) for <code>python</code>, <code>data</code> and <code>the</code> — note the '
 'rare word scores highest.'),
                "starter": ('docs = {\n'
 '    1: "python is a great language for data work",\n'
 '    2: "the python language is easy to read",\n'
 '    3: "data pipelines move data between systems",\n'
 '    4: "reading code is a skill you build",\n'
 '}\n'
 '\n'
 'import math\n'
 '\n'
 'index = {}\n'
 'for doc_id, text in docs.items():\n'
 '    for word in text.split():\n'
 '        index.setdefault(word, set()).add(doc_id)\n'
 '\n'
 'N = len(docs)\n'
 '# print df and idf for each term\n'),
                "expected_output": 'python    df=2 idf=0.693\ndata      df=2 idf=0.693\nthe       df=1 idf=1.386',
                "hint": 'df = len(index[term]); idf = math.log(N / df). Format with f"{idf:.3f}".',
                "solution": ('docs = {\n'
 '    1: "python is a great language for data work",\n'
 '    2: "the python language is easy to read",\n'
 '    3: "data pipelines move data between systems",\n'
 '    4: "reading code is a skill you build",\n'
 '}\n'
 'import math\n'
 '\n'
 'index = {}\n'
 'for doc_id, text in docs.items():\n'
 '    for word in text.split():\n'
 '        index.setdefault(word, set()).add(doc_id)\n'
 '\n'
 'N = len(docs)\n'
 'for term in ("python", "data", "the"):\n'
 '    df = len(index[term])\n'
 '    idf = math.log(N / df)\n'
 '    print(f"{term:<9} df={df} idf={idf:.3f}")'),
            },
            {
                "title": 'Rank with TF-IDF',
                "prompt": ('Score each matching document as the sum over query words of <code>tf * idf</code>, where tf is '
 "the word's share of that document's words. Print results for <code>data python</code>, best "
 'first.'),
                "starter": ('docs = {\n'
 '    1: "python is a great language for data work",\n'
 '    2: "the python language is easy to read",\n'
 '    3: "data pipelines move data between systems",\n'
 '    4: "reading code is a skill you build",\n'
 '}\n'
 '\n'
 'import math\n'
 '\n'
 'index = {}\n'
 'for doc_id, text in docs.items():\n'
 '    for word in text.split():\n'
 '        index.setdefault(word, set()).add(doc_id)\n'
 '\n'
 'N = len(docs)\n'
 '\n'
 'def score(query):\n'
 '    pass\n'
 '\n'
 'print("query: data python")\n'
 '# print each scored doc\n'),
                "expected_output": ('query: data python\n'
 '  0.2310  [3] data pipelines move data between systems\n'
 '  0.1733  [1] python is a great language for data work\n'
 '  0.0990  [2] the python language is easy to read'),
                "hint": ('tf = docs[doc_id].split().count(word) / len(docs[doc_id].split()). Accumulate per doc, then sort '
 'by (-score, doc_id).'),
                "solution": ('docs = {\n'
 '    1: "python is a great language for data work",\n'
 '    2: "the python language is easy to read",\n'
 '    3: "data pipelines move data between systems",\n'
 '    4: "reading code is a skill you build",\n'
 '}\n'
 'import math\n'
 '\n'
 'index = {}\n'
 'for doc_id, text in docs.items():\n'
 '    for word in text.split():\n'
 '        index.setdefault(word, set()).add(doc_id)\n'
 '\n'
 'N = len(docs)\n'
 '\n'
 'def score(query):\n'
 '    ranked = {}\n'
 '    for word in query.split():\n'
 '        if word not in index:\n'
 '            continue\n'
 '        idf = math.log(N / len(index[word]))\n'
 '        for doc_id in index[word]:\n'
 '            tf = docs[doc_id].split().count(word) / len(docs[doc_id].split())\n'
 '            ranked[doc_id] = ranked.get(doc_id, 0) + tf * idf\n'
 '    return sorted(ranked.items(), key=lambda kv: (-kv[1], kv[0]))\n'
 '\n'
 'print("query: data python")\n'
 'for doc_id, s in score("data python"):\n'
 '    print(f"  {s:.4f}  [{doc_id}] {docs[doc_id]}")'),
            },
        ],
    },
    {
        "slug": 'lru-cache',
        "title": 'LRU Cache & Rate Limiter',
        "level": 'Advanced',
        "icon": 'database',
        "color": '#f97316',
        "xp": 145,
        "minutes": 50,
        "summary": ('Two pieces of infrastructure every backend runs: a least-recently-used cache that evicts cold '
 'keys under a memory ceiling, and a token-bucket rate limiter that decides who gets a 429.'),
        "how_it_works": """
<p>Caches and rate limiters answer the same question — <em>what do I do when I cannot serve everything?</em></p>
<ol>
<li><strong>Cache</strong> — remember expensive results so the second call is free.</li>
<li><strong>Evict</strong> — memory is finite, so when full, drop the <em>least recently used</em> key. Recency is a good proxy for what you'll need next.</li>
<li><strong>Measure</strong> — a cache with a poor hit rate is pure overhead, so count hits and misses.</li>
<li><strong>Limit</strong> — a token bucket refills at a steady rate and allows a burst up to its size. Stripe, GitHub and Cloudflare all shape traffic this way.</li>
</ol>
<p><code>OrderedDict</code> gives you O(1) recency tracking, which is exactly how <code>functools.lru_cache</code> works underneath.</p>
""",
        "steps": [
            {
                "title": 'A cache with hit tracking',
                "prompt": ('Cache <code>slow_lookup</code> results in a dict. Count hits and misses across the call '
 'sequence, then print both and the hit rate to one decimal.'),
                "starter": ('calls = ["a", "b", "a", "c", "a", "b"]\n'
 'cache = {}\n'
 'hits = misses = 0\n'
 '\n'
 'def slow_lookup(key):\n'
 '    return key.upper() * 3\n'
 '\n'
 '# check the cache before calling slow_lookup; count hits and misses\n'),
                "expected_output": 'hits: 3\nmisses: 3\nhit rate: 50.0%',
                "hint": "if key in cache: it's a hit. Otherwise call slow_lookup and store the result.",
                "solution": ('calls = ["a", "b", "a", "c", "a", "b"]\n'
 'cache = {}\n'
 'hits = misses = 0\n'
 '\n'
 'def slow_lookup(key):\n'
 '    return key.upper() * 3\n'
 '\n'
 'for key in calls:\n'
 '    if key in cache:\n'
 '        hits += 1\n'
 '    else:\n'
 '        misses += 1\n'
 '        cache[key] = slow_lookup(key)\n'
 '\n'
 'print(f"hits: {hits}")\n'
 'print(f"misses: {misses}")\n'
 'print(f"hit rate: {hits / len(calls) * 100:.1f}%")'),
            },
            {
                "title": 'Evict the least recently used',
                "prompt": ('With a capacity of 3, evict the least recently used key whenever a new one arrives full. A '
 'repeat access counts as a use. Print the evicted keys in order and what remains.'),
                "starter": ('from collections import OrderedDict\n'
 '\n'
 'CAPACITY = 3\n'
 'cache = OrderedDict()\n'
 'evicted = []\n'
 '\n'
 'for key in ["a", "b", "c", "a", "d", "e", "b"]:\n'
 '    pass\n'
 '\n'
 'print(f"evicted: {evicted}")\n'
 'print(f"remaining: {list(cache)}")\n'),
                "expected_output": "evicted: ['b', 'c', 'a']\nremaining: ['d', 'e', 'b']",
                "hint": 'cache.move_to_end(key) marks a use; cache.popitem(last=False) removes the oldest.',
                "solution": ('from collections import OrderedDict\n'
 '\n'
 'CAPACITY = 3\n'
 'cache = OrderedDict()\n'
 'evicted = []\n'
 '\n'
 'for key in ["a", "b", "c", "a", "d", "e", "b"]:\n'
 '    if key in cache:\n'
 '        cache.move_to_end(key)\n'
 '    else:\n'
 '        if len(cache) >= CAPACITY:\n'
 '            evicted.append(cache.popitem(last=False)[0])\n'
 '        cache[key] = key.upper()\n'
 '\n'
 'print(f"evicted: {evicted}")\n'
 'print(f"remaining: {list(cache)}")'),
            },
            {
                "title": 'Wrap it in a class',
                "prompt": ('Build an <code>LRUCache</code> class with <code>get</code> and <code>put</code>, tracking hits '
 'and misses. Exercise it with capacity 2 and print the lookups, the counters and the surviving '
 'keys.'),
                "starter": ('from collections import OrderedDict\n'
 '\n'
 'class LRUCache:\n'
 '    def __init__(self, capacity):\n'
 '        self.capacity = capacity\n'
 '        self.store = OrderedDict()\n'
 '        self.hits = 0\n'
 '        self.misses = 0\n'
 '\n'
 '    def get(self, key):\n'
 '        pass\n'
 '\n'
 '    def put(self, key, value):\n'
 '        pass\n'
 '\n'
 'cache = LRUCache(2)\n'
 'cache.put("x", 1)\n'
 'cache.put("y", 2)\n'
 'print(cache.get("x"))\n'
 'cache.put("z", 3)\n'
 'print(cache.get("y"))\n'
 'print(cache.get("z"))\n'
 'print(f"hits={cache.hits} misses={cache.misses}")\n'
 'print(f"keys={list(cache.store)}")\n'),
                "expected_output": "1\nNone\n3\nhits=2 misses=1\nkeys=['x', 'z']",
                "hint": ('get: on a hit, move_to_end and return; on a miss return None. put: evict with '
 'popitem(last=False) when at capacity.'),
                "solution": ('from collections import OrderedDict\n'
 '\n'
 'class LRUCache:\n'
 '    def __init__(self, capacity):\n'
 '        self.capacity = capacity\n'
 '        self.store = OrderedDict()\n'
 '        self.hits = 0\n'
 '        self.misses = 0\n'
 '\n'
 '    def get(self, key):\n'
 '        if key in self.store:\n'
 '            self.hits += 1\n'
 '            self.store.move_to_end(key)\n'
 '            return self.store[key]\n'
 '        self.misses += 1\n'
 '        return None\n'
 '\n'
 '    def put(self, key, value):\n'
 '        if key in self.store:\n'
 '            self.store.move_to_end(key)\n'
 '        elif len(self.store) >= self.capacity:\n'
 '            self.store.popitem(last=False)\n'
 '        self.store[key] = value\n'
 '\n'
 'cache = LRUCache(2)\n'
 'cache.put("x", 1)\n'
 'cache.put("y", 2)\n'
 'print(cache.get("x"))\n'
 'cache.put("z", 3)\n'
 'print(cache.get("y"))\n'
 'print(cache.get("z"))\n'
 'print(f"hits={cache.hits} misses={cache.misses}")\n'
 'print(f"keys={list(cache.store)}")'),
            },
            {
                "title": 'Token-bucket rate limiting',
                "prompt": ('Each user gets a bucket of 3 tokens refilling at 3/second. A request costs one token; with none '
 "left, answer 429. Print each request's verdict."),
                "starter": ('RATE = 3          # tokens refilled per second\n'
 'BURST = 3         # bucket size\n'
 '\n'
 'requests = [\n'
 '    ("ana", 0.0), ("ana", 0.1), ("ana", 0.2), ("ana", 0.3),\n'
 '    ("bo", 0.3), ("ana", 1.5), ("bo", 1.6),\n'
 ']\n'
 '\n'
 'buckets = {}\n'
 '# refill by elapsed time, spend a token if one is available\n'),
                "expected_output": (' 0.0 ana  200 OK\n'
 ' 0.1 ana  200 OK\n'
 ' 0.2 ana  200 OK\n'
 ' 0.3 ana  429 Too Many Requests\n'
 ' 0.3 bo   200 OK\n'
 ' 1.5 ana  200 OK\n'
 ' 1.6 bo   200 OK'),
                "hint": 'tokens = min(BURST, tokens + (now - last) * RATE) refills; spend one if tokens >= 1.',
                "solution": ('RATE = 3          # tokens refilled per second\n'
 'BURST = 3         # bucket size\n'
 '\n'
 'requests = [\n'
 '    ("ana", 0.0), ("ana", 0.1), ("ana", 0.2), ("ana", 0.3),\n'
 '    ("bo", 0.3), ("ana", 1.5), ("bo", 1.6),\n'
 ']\n'
 '\n'
 'buckets = {}\n'
 'for user, now in requests:\n'
 '    tokens, last = buckets.get(user, (BURST, 0.0))\n'
 '    tokens = min(BURST, tokens + (now - last) * RATE)\n'
 '    if tokens >= 1:\n'
 '        allowed, tokens = True, tokens - 1\n'
 '    else:\n'
 '        allowed = False\n'
 '    buckets[user] = (tokens, now)\n'
 '    print(f"{now:>4} {user:<4} {\'200 OK\' if allowed else \'429 Too Many Requests\'}")'),
            },
        ],
    },
    {
        "slug": 'recommender',
        "title": 'Recommendation Engine',
        "level": 'Advanced',
        "icon": 'sparkles',
        "color": '#ec4899',
        "xp": 150,
        "minutes": 55,
        "summary": ("Build collaborative filtering from scratch — the algorithm behind 'customers also bought' and "
 'your Netflix row — using cosine similarity to find your taste-twins and recommend what they '
 "loved that you haven't seen."),
        "how_it_works": """
<p>Collaborative filtering makes a bet: <em>people who agreed in the past will agree again.</em> No genres, no tags, just ratings.</p>
<ol>
<li><strong>Represent</strong> — every user is a sparse vector of item ratings.</li>
<li><strong>Compare</strong> — cosine similarity measures the angle between two users, so it captures taste rather than how generously someone rates.</li>
<li><strong>Neighbour</strong> — rank everyone by similarity to the target user.</li>
<li><strong>Recommend</strong> — score unseen items by each neighbour's rating weighted by similarity.</li>
</ol>
<p>This is the algorithm that won early recommender competitions, and it still underpins production systems. You'll implement it with nothing but <code>math</code>.</p>
""",
        "steps": [
            {
                "title": 'Explore the ratings matrix',
                "prompt": ('Print how many users and distinct items exist, then one line per user (alphabetical) with how '
 'many items they rated and their average to two decimals.'),
                "starter": ('ratings = {\n'
 '    "ana":  {"dune": 5, "arrival": 4, "matrix": 5, "her": 2},\n'
 '    "bo":   {"dune": 4, "arrival": 5, "matrix": 4},\n'
 '    "cleo": {"her": 5, "amelie": 5, "arrival": 3},\n'
 '    "dev":  {"dune": 5, "matrix": 4, "amelie": 1},\n'
 '}\n'
 '\n'
 'items = set()\n'
 '# collect every item, then summarise each user\n'),
                "expected_output": ('users: 4  items: 5\n'
 'ana   rated 4  avg 4.00\n'
 'bo    rated 3  avg 4.33\n'
 'cleo  rated 3  avg 4.33\n'
 'dev   rated 3  avg 3.33'),
                "hint": 'items |= set(seen) unions the keys; sum(seen.values()) / len(seen) is the average.',
                "solution": ('ratings = {\n'
 '    "ana":  {"dune": 5, "arrival": 4, "matrix": 5, "her": 2},\n'
 '    "bo":   {"dune": 4, "arrival": 5, "matrix": 4},\n'
 '    "cleo": {"her": 5, "amelie": 5, "arrival": 3},\n'
 '    "dev":  {"dune": 5, "matrix": 4, "amelie": 1},\n'
 '}\n'
 'items = set()\n'
 'for user, seen in ratings.items():\n'
 '    items |= set(seen)\n'
 '\n'
 'print(f"users: {len(ratings)}  items: {len(items)}")\n'
 'for user in sorted(ratings):\n'
 '    seen = ratings[user]\n'
 '    avg = sum(seen.values()) / len(seen)\n'
 '    print(f"{user:<5} rated {len(seen)}  avg {avg:.2f}")'),
            },
            {
                "title": 'Cosine similarity',
                "prompt": ('Write <code>cosine(a, b)</code>: dot product over shared items, divided by the product of both '
 "vectors' magnitudes. Print ana's similarity to each other user, 3 decimals."),
                "starter": ('ratings = {\n'
 '    "ana":  {"dune": 5, "arrival": 4, "matrix": 5, "her": 2},\n'
 '    "bo":   {"dune": 4, "arrival": 5, "matrix": 4},\n'
 '    "cleo": {"her": 5, "amelie": 5, "arrival": 3},\n'
 '    "dev":  {"dune": 5, "matrix": 4, "amelie": 1},\n'
 '}\n'
 '\n'
 'import math\n'
 '\n'
 'def cosine(a, b):\n'
 '    pass\n'
 '\n'
 'for other in ("bo", "cleo", "dev"):\n'
 '    print(f"ana vs {other:<5} {cosine(ratings[\'ana\'], ratings[other]):.3f}")\n'),
                "expected_output": 'ana vs bo    0.950\nana vs cleo  0.342\nana vs dev   0.830',
                "hint": ('shared = set(a) & set(b); dot = sum(a[i] * b[i] for i in shared); divide by sqrt of each '
 "vector's sum of squares."),
                "solution": ('ratings = {\n'
 '    "ana":  {"dune": 5, "arrival": 4, "matrix": 5, "her": 2},\n'
 '    "bo":   {"dune": 4, "arrival": 5, "matrix": 4},\n'
 '    "cleo": {"her": 5, "amelie": 5, "arrival": 3},\n'
 '    "dev":  {"dune": 5, "matrix": 4, "amelie": 1},\n'
 '}\n'
 'import math\n'
 '\n'
 'def cosine(a, b):\n'
 '    shared = set(a) & set(b)\n'
 '    if not shared:\n'
 '        return 0.0\n'
 '    dot = sum(a[i] * b[i] for i in shared)\n'
 '    na = math.sqrt(sum(v * v for v in a.values()))\n'
 '    nb = math.sqrt(sum(v * v for v in b.values()))\n'
 '    return dot / (na * nb)\n'
 '\n'
 'for other in ("bo", "cleo", "dev"):\n'
 '    print(f"ana vs {other:<5} {cosine(ratings[\'ana\'], ratings[other]):.3f}")'),
            },
            {
                "title": 'Rank the neighbours',
                "prompt": ('Sort every other user by similarity to <code>ana</code>, most similar first, breaking ties by '
 'name. Print the ranked list.'),
                "starter": ('ratings = {\n'
 '    "ana":  {"dune": 5, "arrival": 4, "matrix": 5, "her": 2},\n'
 '    "bo":   {"dune": 4, "arrival": 5, "matrix": 4},\n'
 '    "cleo": {"her": 5, "amelie": 5, "arrival": 3},\n'
 '    "dev":  {"dune": 5, "matrix": 4, "amelie": 1},\n'
 '}\n'
 '\n'
 'import math\n'
 '\n'
 'def cosine(a, b):\n'
 '    shared = set(a) & set(b)\n'
 '    if not shared:\n'
 '        return 0.0\n'
 '    dot = sum(a[i] * b[i] for i in shared)\n'
 '    na = math.sqrt(sum(v * v for v in a.values()))\n'
 '    nb = math.sqrt(sum(v * v for v in b.values()))\n'
 '    return dot / (na * nb)\n'
 '\n'
 'target = "ana"\n'
 '# build and sort the neighbour list, then print it\n'),
                "expected_output": 'nearest to ana:\n  bo    0.950\n  dev   0.830\n  cleo  0.342',
                "hint": 'Build (score, user) pairs then sort with key=lambda pair: (-pair[0], pair[1]).',
                "solution": ('ratings = {\n'
 '    "ana":  {"dune": 5, "arrival": 4, "matrix": 5, "her": 2},\n'
 '    "bo":   {"dune": 4, "arrival": 5, "matrix": 4},\n'
 '    "cleo": {"her": 5, "amelie": 5, "arrival": 3},\n'
 '    "dev":  {"dune": 5, "matrix": 4, "amelie": 1},\n'
 '}\n'
 'import math\n'
 '\n'
 'def cosine(a, b):\n'
 '    shared = set(a) & set(b)\n'
 '    if not shared:\n'
 '        return 0.0\n'
 '    dot = sum(a[i] * b[i] for i in shared)\n'
 '    na = math.sqrt(sum(v * v for v in a.values()))\n'
 '    nb = math.sqrt(sum(v * v for v in b.values()))\n'
 '    return dot / (na * nb)\n'
 '\n'
 'target = "ana"\n'
 'neighbours = [(cosine(ratings[target], ratings[u]), u)\n'
 '              for u in ratings if u != target]\n'
 'neighbours.sort(key=lambda pair: (-pair[0], pair[1]))\n'
 'print(f"nearest to {target}:")\n'
 'for score, user in neighbours:\n'
 '    print(f"  {user:<5} {score:.3f}")'),
            },
            {
                "title": 'Recommend what to watch',
                "prompt": ("For every item ana hasn't rated, sum <code>similarity * neighbour_rating</code> across all "
 'positively-similar users. Print the recommendations, best first, 3 decimals.'),
                "starter": ('ratings = {\n'
 '    "ana":  {"dune": 5, "arrival": 4, "matrix": 5, "her": 2},\n'
 '    "bo":   {"dune": 4, "arrival": 5, "matrix": 4},\n'
 '    "cleo": {"her": 5, "amelie": 5, "arrival": 3},\n'
 '    "dev":  {"dune": 5, "matrix": 4, "amelie": 1},\n'
 '}\n'
 '\n'
 'import math\n'
 '\n'
 'def cosine(a, b):\n'
 '    shared = set(a) & set(b)\n'
 '    if not shared:\n'
 '        return 0.0\n'
 '    dot = sum(a[i] * b[i] for i in shared)\n'
 '    na = math.sqrt(sum(v * v for v in a.values()))\n'
 '    nb = math.sqrt(sum(v * v for v in b.values()))\n'
 '    return dot / (na * nb)\n'
 '\n'
 'target = "ana"\n'
 'seen = ratings[target]\n'
 'scores = {}\n'
 "# weight each neighbour's unseen items by similarity\n"),
                "expected_output": 'recommendations for ana:\n  amelie   2.542',
                "hint": 'Skip items already in `seen`; scores[item] = scores.get(item, 0.0) + sim * rating.',
                "solution": ('ratings = {\n'
 '    "ana":  {"dune": 5, "arrival": 4, "matrix": 5, "her": 2},\n'
 '    "bo":   {"dune": 4, "arrival": 5, "matrix": 4},\n'
 '    "cleo": {"her": 5, "amelie": 5, "arrival": 3},\n'
 '    "dev":  {"dune": 5, "matrix": 4, "amelie": 1},\n'
 '}\n'
 'import math\n'
 '\n'
 'def cosine(a, b):\n'
 '    shared = set(a) & set(b)\n'
 '    if not shared:\n'
 '        return 0.0\n'
 '    dot = sum(a[i] * b[i] for i in shared)\n'
 '    na = math.sqrt(sum(v * v for v in a.values()))\n'
 '    nb = math.sqrt(sum(v * v for v in b.values()))\n'
 '    return dot / (na * nb)\n'
 '\n'
 'target = "ana"\n'
 'seen = ratings[target]\n'
 'scores = {}\n'
 'for user, their in ratings.items():\n'
 '    if user == target:\n'
 '        continue\n'
 '    sim = cosine(seen, their)\n'
 '    if sim <= 0:\n'
 '        continue\n'
 '    for item, rating in their.items():\n'
 '        if item in seen:\n'
 '            continue\n'
 '        scores[item] = scores.get(item, 0.0) + sim * rating\n'
 '\n'
 'print(f"recommendations for {target}:")\n'
 'for item, score in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0])):\n'
 '    print(f"  {item:<8} {score:.3f}")'),
            },
        ],
    },
]


# Listed easiest-first. sort() is stable, so projects keep their authored
# order within a level.
_LEVEL_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
PROJECTS.sort(key=lambda p: _LEVEL_ORDER[p["level"]])


def get_project(slug):
    for p in PROJECTS:
        if p["slug"] == slug:
            return p
    return None
