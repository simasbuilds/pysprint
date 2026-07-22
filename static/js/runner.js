/* LearnWithPython code runner — real Python 3 in the browser via Pyodide.
   Exposes:
     PyRunner.run(code) -> {ok, output}
     PyRunner.wireSimple(runBtnId, codeId, outId)
     PySprint.initLesson(cfg) / initChallenge(cfg) / initPlayground()
*/
(function () {
  'use strict';

  const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js';
  const ICONS_URL = '/static/images/pysprint-icons.svg';
  let pyodideReady = null;

  function iconMarkup(name) {
    const safe = /^[a-z0-9-]+$/.test(name) ? name : 'info';
    return '<svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true">' +
      '<use href="' + ICONS_URL + '#ps-' + safe + '"></use></svg>';
  }

  function loadPyodideOnce() {
    if (pyodideReady) return pyodideReady;
    pyodideReady = new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = PYODIDE_URL;
      s.onload = async () => {
        try { resolve(await loadPyodide()); } catch (e) { reject(e); }
      };
      s.onerror = () => reject(new Error('Could not load the Python engine. Check your connection.'));
      document.head.appendChild(s);
    });
    return pyodideReady;
  }

  async function run(code) {
    const py = await loadPyodideOnce();
    // Fresh globals each run so lessons don't leak state into each other.
    const capture =
      'import sys, io\n' +
      '_pysprint_out = io.StringIO()\n' +
      'sys.stdout = _pysprint_out\n' +
      'sys.stderr = _pysprint_out\n';
    const restore =
      'sys.stdout = sys.__stdout__\n' +
      'sys.stderr = sys.__stderr__\n' +
      '_pysprint_out.getvalue()';
    try {
      const ns = py.globals.get('dict')();
      await py.runPythonAsync(capture, { globals: ns });
      let error = null;
      try {
        await py.runPythonAsync(code, { globals: ns });
      } catch (e) {
        error = e;
      }
      const output = await py.runPythonAsync(restore, { globals: ns });
      ns.destroy();
      if (error) {
        const msg = formatPyError(error);
        return { ok: false, output: (output ? output + '\n' : '') + msg };
      }
      return { ok: true, output: output || '(no output — did you forget print()?)' };
    } catch (e) {
      return { ok: false, output: String(e.message || e) };
    }
  }

  function formatPyError(e) {
    // Pyodide errors embed the full Python traceback; trim JS noise.
    const text = String(e.message || e);
    const i = text.indexOf('Traceback');
    const trace = i >= 0 ? text.slice(i) : text;
    const hint = friendlyErrorHint(trace);
    return hint ? trace + '\n\n\u{1F4A1} In plain English: ' + hint : trace;
  }

  // Plain-English translations of the errors beginners hit most.
  const ERROR_HINTS = [
    ['IndentationError', 'The spaces at the start of a line are off. Lines inside if / for / while / def must be indented by 4 spaces, and lines outside must not be.'],
    ['SyntaxError', "Python couldn't read one of your lines. Check for a missing colon (:) at the end of if/for/def lines, and make sure every quote and bracket is closed."],
    ['NameError', "You used a name Python doesn't know yet. Check the spelling and capitalisation (Python treats name and Name as different), and make sure you created the variable before using it."],
    ['TypeError', "Two different types of value collided — like adding text to a number. Convert first with int(), float() or str(), e.g. int(\"5\") + 5."],
    ['IndexError', "You asked for a position that doesn't exist in the list. Remember: positions start at 0, so the last item of 3 is at position 2."],
    ['KeyError', "That key isn't in the dictionary. Check the spelling, or use .get(key) which returns None instead of crashing."],
    ['ValueError', 'The value was the right type but the wrong content — like int("hello"). Check what you\'re converting.'],
    ['ZeroDivisionError', 'Your code divided by zero somewhere. Check the value on the right side of the /.'],
    ['AttributeError', "That value doesn't have the method you called. Check its type with print(type(x)) and the method's spelling."],
    ['UnboundLocalError', 'You used a variable inside a function before giving it a value there.'],
    ['RecursionError', 'Your function keeps calling itself and never stops — make sure it has a base case that returns without another call.'],
  ];

  function friendlyErrorHint(trace) {
    for (const [name, hint] of ERROR_HINTS) {
      if (trace.includes(name)) return hint;
    }
    return null;
  }

  function enableTabKey(textarea) {
    textarea.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        e.preventDefault();
        const s = textarea.selectionStart, epos = textarea.selectionEnd;
        textarea.value = textarea.value.slice(0, s) + '    ' + textarea.value.slice(epos);
        textarea.selectionStart = textarea.selectionEnd = s + 4;
      }
      if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        textarea.dispatchEvent(new CustomEvent('pysprint:run', { bubbles: true }));
      }
    });
  }

  function setupWorkspace(opts) {
    const code = opts.code;
    if (!code) return;
    code.spellcheck = false;
    code.setAttribute('autocorrect', 'off');
    code.setAttribute('autocapitalize', 'none');
    code.setAttribute('autocomplete', 'off');
    const loadBtn = opts.loadId && document.getElementById(opts.loadId);
    const blankBtn = opts.blankId && document.getElementById(opts.blankId);
    const state = opts.stateId && document.getElementById(opts.stateId);

    function setState(message) {
      if (state) state.textContent = message;
    }

    function save(message) {
      try { localStorage.setItem(opts.storageKey, code.value); } catch (_) {}
      setState(message || (code.value.trim() ? 'Saved on this device' : 'Blank · autosaved'));
    }

    function replace(next, action) {
      if (code.value.trim() && code.value !== next &&
          !window.confirm(action + ' will replace the code currently in this editor. Continue?')) return;
      code.value = next;
      save(next.trim() ? 'Starter loaded · autosaved' : 'Blank · autosaved');
      code.dispatchEvent(new Event('input', { bubbles: true }));
      code.focus({ preventScroll: true });
      code.setSelectionRange(code.value.length, code.value.length);
    }

    let saved = null;
    try { saved = localStorage.getItem(opts.storageKey); } catch (_) {}
    if (saved !== null) {
      code.value = saved;
      setState(code.value.trim() ? 'Restored · autosaved' : 'Blank · autosaved');
    } else if (opts.prefill) {
      // First visit: beginners should see runnable code, not an empty box.
      code.value = opts.prefill;
      setState('Example loaded · autosaved');
    } else {
      code.value = '';
      setState('Blank · autosaved');
    }
    code.addEventListener('input', () => save());

    loadBtn && loadBtn.addEventListener('click', () => replace(opts.starter || '', 'Loading the starter'));
    blankBtn && blankBtn.addEventListener('click', () => replace('', 'Starting blank'));
  }

  async function execInto(codeEl, outEl, btn) {
    if (!codeEl.value.trim()) {
      outEl.classList.remove('error');
      outEl.textContent = 'Your workspace is blank. Write some Python or load the starter, then run it.';
      codeEl.focus({ preventScroll: true });
      return { ok: false, output: '' };
    }
    const heroVisual = btn.closest('.hero-visual');
    const liveStatus = heroVisual && heroVisual.querySelector('.editor-live');
    const setHeroStatus = (label, state) => {
      if (!heroVisual || !liveStatus) return;
      heroVisual.classList.remove('is-executing', 'is-complete', 'is-failed');
      if (state) heroVisual.classList.add(state);
      liveStatus.innerHTML = '<i></i> ' + label;
    };
    btn.disabled = true;
    const original = btn.textContent;
    btn.textContent = 'Running…';
    setHeroStatus('Running', 'is-executing');
    outEl.classList.remove('error');
    if (!pyodideReady) outEl.textContent = 'Loading Python engine (first run only, ~5s)…';
    const result = await run(codeEl.value);
    outEl.textContent = result.output;
    if (!result.ok) outEl.classList.add('error');
    outEl.classList.remove('flash');
    void outEl.offsetWidth;              // restart the highlight animation
    outEl.classList.add('flash');
    btn.disabled = false;
    btn.textContent = original;
    setHeroStatus(result.ok ? 'Complete' : 'Check error', result.ok ? 'is-complete' : 'is-failed');
    setTimeout(() => setHeroStatus('Ready', ''), 2200);
    return result;
  }

  function normalize(text) {
    return (text || '').replace(/\r\n/g, '\n').trimEnd()
      .split('\n').map(l => l.trimEnd()).join('\n');
  }

  // ── public: simple runner (hero, examples) ─────────────────────────
  const PyRunner = {
    run: run,
    wireSimple(runId, codeId, outId) {
      const btn = document.getElementById(runId);
      const code = document.getElementById(codeId);
      const out = document.getElementById(outId);
      if (!btn || !code || !out) return;
      enableTabKey(code);
      const go = () => execInto(code, out, btn);
      btn.addEventListener('click', go);
      code.addEventListener('pysprint:run', go);
    },
  };

  // ── graded challenge wiring (lesson + arena share this) ────────────
  function wireChallenge(opts) {
    const code = document.getElementById('challengeCode');
    const out = document.getElementById('challengeOut');
    const btn = document.getElementById('challengeRun');
    const resultBox = document.getElementById('challengeResult');
    const hintBtn = document.getElementById('hintBtn');
    const hintBox = document.getElementById('hintBox');
    const solBtn = document.getElementById('solutionBtn');
    const solBox = document.getElementById('solutionBox');
    if (!code || !btn) return;

    setupWorkspace({
      code: code,
      storageKey: opts.storageKey,
      starter: opts.starter,
      prefill: opts.starter,
      loadId: 'challengeLoad',
      blankId: 'challengeBlank',
      stateId: 'challengeSaveState',
    });
    enableTabKey(code);
    hintBtn && hintBtn.addEventListener('click', () => { hintBox.hidden = !hintBox.hidden; });
    solBtn && solBtn.addEventListener('click', () => { solBox.hidden = !solBox.hidden; });

    async function check() {
      const result = await execInto(code, out, btn);
      resultBox.hidden = false;
      if (result.ok && normalize(result.output) === normalize(opts.expected)) {
        resultBox.className = 'check-result pass';
        resultBox.innerHTML = iconMarkup('check') + ' <strong>Correct!</strong> Output matches exactly.';
        opts.onPass && opts.onPass();
      } else {
        resultBox.className = 'check-result fail';
        resultBox.innerHTML = result.ok
          ? iconMarkup('warning') + ' Not quite — compare the highlighted lines below.' +
            renderDiff(opts.expected, result.output)
          : iconMarkup('warning') + ' Your code raised an error — read the traceback above, fix it, and run again.';
      }
    }
    btn.addEventListener('click', check);
    code.addEventListener('pysprint:run', check);
  }

  function escapeHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  // Line-by-line comparison shown when output doesn't match the target.
  function renderDiff(expected, got) {
    const want = normalize(expected).split('\n');
    const have = normalize(got).split('\n');
    const rows = [];
    const count = Math.max(want.length, have.length);
    for (let i = 0; i < count; i++) {
      const w = i < want.length ? want[i] : null;
      const h = i < have.length ? have[i] : null;
      let cls = 'diff-ok';
      if (w === null) cls = 'diff-extra';
      else if (h === null) cls = 'diff-missing';
      else if (w !== h) cls = 'diff-bad';
      rows.push(
        '<div class="diff-row ' + cls + '">' +
        '<span class="diff-ln">' + (i + 1) + '</span>' +
        '<code>' + (w === null ? '<em>— nothing expected —</em>' : (escapeHtml(w) || '&nbsp;')) + '</code>' +
        '<code>' + (h === null ? '<em>— line missing —</em>' : (escapeHtml(h) || '&nbsp;')) + '</code>' +
        '</div>');
    }
    const wrong = rows.length && (normalize(expected) !== normalize(got));
    return '<div class="diff-view"' + (wrong ? '' : ' hidden') + '>' +
      '<div class="diff-row diff-head"><span class="diff-ln">#</span>' +
      '<code>Target output</code><code>Your output</code></div>' +
      rows.join('') + '</div>';
  }

  async function postJSON(url, body) {
    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    return { status: resp.status, data: await resp.json().catch(() => ({})) };
  }

  function reportProgress(url, body, loggedIn, passedMsg) {
    if (!loggedIn) {
      toast(passedMsg + ' — log in to bank the XP!', 'success');
      return;
    }
    postJSON(url, body).then(({ status, data }) => {
      if (status !== 200) return;
      if (data.first_time && data.xp_gained) {
        toast('+' + data.xp_gained + ' XP earned!', 'success');
      }
      celebrateAchievements(data.new_achievements);
    }).catch(() => {});
  }

  // ── confetti (no libraries) ────────────────────────────────────────
  function confetti(anchor) {
    const colors = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#f43f5e', '#a78bfa'];
    const rect = (anchor || document.body).getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    for (let i = 0; i < 46; i++) {
      const p = document.createElement('div');
      const size = 5 + Math.random() * 7;
      p.style.cssText =
        'position:fixed;z-index:99;pointer-events:none;border-radius:2px;' +
        'left:' + cx + 'px;top:' + cy + 'px;width:' + size + 'px;height:' + size * 0.6 + 'px;' +
        'background:' + colors[i % colors.length] + ';';
      document.body.appendChild(p);
      const angle = Math.random() * Math.PI * 2;
      const dist = 90 + Math.random() * 220;
      p.animate([
        { transform: 'translate(0,0) rotate(0deg)', opacity: 1 },
        { transform: 'translate(' + Math.cos(angle) * dist + 'px,' +
          (Math.sin(angle) * dist + 160) + 'px) rotate(' + (Math.random() * 720 - 360) + 'deg)', opacity: 0 },
      ], { duration: 900 + Math.random() * 700, easing: 'cubic-bezier(.16,1,.3,1)' })
        .onfinish = () => p.remove();
    }
  }

  // ── walkthrough player: animated line-by-line execution ────────────
  function initWalkthrough(example, steps) {
    const codeEl = document.getElementById('wlCode');
    const textEl = document.getElementById('wlText');
    const countEl = document.getElementById('wlCount');
    const playBtn = document.getElementById('wlPlay');
    const stepBtn = document.getElementById('wlStep');
    const restartBtn = document.getElementById('wlRestart');
    if (!codeEl || !steps || !steps.length) return;

    const lines = example.split('\n');
    codeEl.innerHTML = lines.map((l, i) =>
      '<span class="wl-line" data-line="' + (i + 1) + '"><span class="wl-ln">' +
      (i + 1) + '</span>' + escapeHtml(l || ' ') + '</span>').join('');

    let idx = -1, timer = null;

    function show(i) {
      idx = i;
      codeEl.querySelectorAll('.wl-line').forEach(el => el.classList.remove('active'));
      if (i >= 0 && i < steps.length) {
        const target = codeEl.querySelector('.wl-line[data-line="' + steps[i].line + '"]');
        if (target) target.classList.add('active');
        textEl.textContent = steps[i].text;
        textEl.classList.remove('wl-fade');
        void textEl.offsetWidth;           // restart the fade animation
        textEl.classList.add('wl-fade');
        countEl.textContent = (i + 1) + ' / ' + steps.length;
      }
    }

    function stop() {
      if (timer) { clearInterval(timer); timer = null; }
      playBtn.textContent = '▶ Play';
    }

    function advance() {
      if (idx + 1 >= steps.length) { stop(); return; }
      show(idx + 1);
      if (timer && idx + 1 >= steps.length) stop();
    }

    playBtn.addEventListener('click', () => {
      if (timer) { stop(); return; }
      if (idx < 0 || idx + 1 >= steps.length) show(0); else advance();
      playBtn.textContent = '⏸ Pause';
      timer = setInterval(advance, 2600);
    });
    stepBtn.addEventListener('click', () => { stop(); advance(); });
    restartBtn.addEventListener('click', () => { stop(); show(0); });
  }

  // ── page initialisers ──────────────────────────────────────────────
  const PySprint = {
    initLesson(cfg) {
      // Animated walkthrough player (only some lessons have one)
      if (cfg.walkthrough) initWalkthrough(cfg.example, cfg.walkthrough);

      // Example runner
      const exCode = document.getElementById('exampleCode');
      setupWorkspace({
        code: exCode,
        storageKey: 'pysprint-example-' + cfg.course + '-' + cfg.lesson,
        starter: cfg.example,
        prefill: cfg.example,
        loadId: 'exampleLoad',
        blankId: 'exampleBlank',
        stateId: 'exampleSaveState',
      });
      PyRunner.wireSimple('exampleRun', 'exampleCode', 'exampleOut');

      // Challenge (expected output embedded as JSON to survive newlines)
      const spec = JSON.parse(document.getElementById('challengeSpec').textContent);
      let challengePassed = false;
      wireChallenge({
        expected: spec.expected,
        starter: cfg.starter,
        storageKey: 'pysprint-challenge-' + cfg.course + '-' + cfg.lesson,
        onPass() {
          challengePassed = true;
          const resultBox = document.getElementById('challengeResult');
          confetti(resultBox);
          if (window.xpFly) xpFly(resultBox, cfg.xp ? '+' + cfg.xp + ' XP unlocked' : 'Challenge passed!');
        },
      });

      // Quiz
      const quizBtn = document.getElementById('quizCheck');
      if (quizBtn) {
        quizBtn.addEventListener('click', () => {
          let right = 0, total = 0;
          document.querySelectorAll('.quiz-q').forEach(q => {
            total++;
            const answer = Number(q.dataset.answer);
            const opts = q.querySelectorAll('.quiz-opt');
            const chosen = q.querySelector('input:checked');
            opts.forEach((o, i) => {
              o.classList.remove('correct', 'wrong');
              if (i === answer) o.classList.add('correct');
            });
            if (chosen && Number(chosen.value) === answer) right++;
            else if (chosen) opts[Number(chosen.value)].classList.add('wrong');
            q.querySelector('.quiz-explain').hidden = false;
          });
          const score = document.getElementById('quizScore');
          score.textContent = right + '/' + total + ' correct';
          score.classList.remove('perfect');
          if (right === total && total > 0) {
            score.classList.add('perfect');
            score.textContent += ' — perfect!';
            confetti(score);
          }
        });
      }

      // Notes (device-local)
      const notes = document.getElementById('lessonNotes');
      const notesKey = 'pysprint-notes-' + cfg.course + '-' + cfg.lesson;
      notes.value = localStorage.getItem(notesKey) || '';
      notes.addEventListener('input', () => localStorage.setItem(notesKey, notes.value));

      // Complete button
      const completeBtn = document.getElementById('completeBtn');
      completeBtn.addEventListener('click', () => {
        if (!challengePassed && !completeBtn.dataset.done) {
          toast('Pass the challenge first — that is where the learning happens.', 'error');
          return;
        }
        if (!cfg.loggedIn) {
          toast('Log in (free) to save progress and earn XP!', '');
          setTimeout(() => { window.location = '/login?next=' + encodeURIComponent(location.pathname); }, 1200);
          return;
        }
        postJSON('/api/complete-lesson', { course: cfg.course, lesson: cfg.lesson })
          .then(({ status, data }) => {
            if (status !== 200) { toast('Could not save progress.', 'error'); return; }
            if (data.first_time) {
              toast('+' + data.xp_gained + ' XP — lesson complete!', 'success');
              if (window.xpFly) xpFly(completeBtn, '+' + data.xp_gained + ' XP');
              confetti(completeBtn);
              completeBtn.textContent = 'Completed';
              completeBtn.dataset.done = '1';
            } else {
              toast('Already completed — nice revision session!', '');
            }
            celebrateAchievements(data.new_achievements);
          })
          .catch(() => toast('Network error saving progress.', 'error'));
      });
    },

    initChallenge(cfg) {
      wireChallenge({
        expected: cfg.expected,
        starter: cfg.starter,
        storageKey: 'pysprint-arena-' + cfg.challenge,
        onPass() {
          const resultBox = document.getElementById('challengeResult');
          confetti(resultBox);
          if (window.xpFly) xpFly(resultBox, cfg.xp ? '+' + cfg.xp + ' XP unlocked' : 'Challenge solved!');
          reportProgress('/api/complete-challenge', { challenge: cfg.challenge },
            cfg.loggedIn, 'Challenge solved');
        },
      });
    },

    // ── real-life project stepper ────────────────────────────────────
    initProject(cfg) {
      const spec = JSON.parse(document.getElementById('projectSpec').textContent);
      const total = spec.steps.length;
      const saveKey = 'pysprint-project-' + cfg.project;
      let unlocked = cfg.completed ? total
        : Math.min(parseInt(localStorage.getItem(saveKey) || '0', 10), total);

      const bar = document.getElementById('stepBar');
      const count = document.getElementById('stepCount');
      const finish = document.getElementById('projectFinish');

      function render() {
        for (let i = 0; i < total; i++) {
          const card = document.getElementById('step-' + i);
          const state = document.getElementById('state-' + i);
          const isDone = i < unlocked;
          const isOpen = i <= unlocked;
          card.classList.toggle('locked', !isOpen);
          card.classList.toggle('done', isDone);
          state.innerHTML = iconMarkup(isDone ? 'check' : (isOpen ? 'target' : 'lock'));
        }
        bar.style.width = (unlocked / total * 100) + '%';
        count.textContent = unlocked + ' / ' + total + ' steps';
        if (finish) finish.hidden = unlocked < total;
      }

      // hint / solution toggles
      document.querySelectorAll('[data-toggle]').forEach(btn => {
        btn.addEventListener('click', () => {
          const el = document.getElementById(btn.dataset.toggle);
          if (el) el.hidden = !el.hidden;
        });
      });

      // wire each step's editor
      for (let i = 0; i < total; i++) {
        const code = document.getElementById('code-' + i);
        const out = document.getElementById('out-' + i);
        const btn = document.getElementById('run-' + i);
        const resultBox = document.getElementById('result-' + i);
        setupWorkspace({
          code: code,
          storageKey: 'pysprint-project-code-' + cfg.project + '-' + i,
          starter: spec.starters[i],
          loadId: 'load-' + i,
          blankId: 'blank-' + i,
          stateId: 'save-' + i,
        });
        enableTabKey(code);

        const check = async () => {
          const result = await execInto(code, out, btn);
          resultBox.hidden = false;
          if (result.ok && normalize(result.output) === normalize(spec.steps[i])) {
            resultBox.className = 'check-result pass';
            resultBox.innerHTML = iconMarkup('check') + ' <strong>Step complete!</strong>' +
              (i + 1 < total ? ' The next step is unlocked.' : ' That was the last one — project shipped!');
            confetti(resultBox);
            if (i + 1 > unlocked) {
              unlocked = i + 1;
              localStorage.setItem(saveKey, String(unlocked));
              render();
              if (i + 1 < total) {
                const nextCard = document.getElementById('step-' + (i + 1));
                nextCard.classList.add('just-unlocked');
                setTimeout(() => nextCard.scrollIntoView({ behavior: 'smooth', block: 'center' }), 350);
              }
            }
            if (unlocked >= total) {
              reportProgress('/api/complete-project', { project: cfg.project },
                cfg.loggedIn, 'Project shipped');
            }
          } else {
            resultBox.className = 'check-result fail';
            resultBox.innerHTML = result.ok
              ? iconMarkup('warning') + ' Not quite — compare the highlighted lines below.' +
                renderDiff(spec.steps[i], result.output)
              : iconMarkup('warning') + ' Your code raised an error — read the traceback above and try again.';
          }
        };
        btn.addEventListener('click', check);
        code.addEventListener('pysprint:run', check);
      }

      render();
    },

    initPlayground() {
      const code = document.getElementById('pgCode');
      const out = document.getElementById('pgOut');
      const runBtn = document.getElementById('pgRun');
      const runtime = document.getElementById('pgRuntime');
      const runtimeText = document.getElementById('pgRuntimeText');
      const runStatus = document.getElementById('pgRunStatus');
      const runMeta = document.getElementById('pgRunMeta');
      const lines = document.getElementById('pgLines');
      const stats = document.getElementById('pgCodeStats');
      const filename = document.getElementById('pgFilename');
      const ide = document.querySelector('.playground-ide');
      const historyEl = document.getElementById('pgHistory');
      const historyKey = 'pysprint-playground-history';
      filename.value = localStorage.getItem('pysprint-playground-filename') || 'playground.py';

      setupWorkspace({
        code: code,
        storageKey: 'pysprint-playground',
        blankId: 'pgBlank',
        stateId: 'pgSaveState',
      });
      enableTabKey(code);

      const recipes = {
        data: `orders = [
    {"product": "Keyboard", "qty": 2, "price": 45},
    {"product": "Monitor", "qty": 1, "price": 220},
    {"product": "Mouse", "qty": 3, "price": 25},
]

# Calculate total revenue and find the largest order
revenue = sum(order["qty"] * order["price"] for order in orders)
largest = max(orders, key=lambda order: order["qty"] * order["price"])

print(f"Revenue: €{revenue}")
print(f"Largest order: {largest['product']}")
`,
        text: `raw_names = ["  ADA lovelace ", "grace  hopper", "  Alan TURING"]

# Normalize whitespace and capitalization
clean_names = [" ".join(name.split()).title() for name in raw_names]

for name in clean_names:
    print(name)
`,
        api: `import json

response = """{
    "city": "New York",
    "temp_c": 27,
    "conditions": ["sunny", "humid"]
}"""

weather = json.loads(response)
conditions = ", ".join(weather["conditions"])

print(f"{weather['city']}: {weather['temp_c']}°C, {conditions}")
`,
        automation: `from pathlib import Path

filenames = [
    "invoice-july.pdf",
    "team-photo.jpg",
    "invoice-august.pdf",
    "logo.png",
]

# Group filenames by extension, like a file organizer would
groups = {}
for name in filenames:
    extension = Path(name).suffix.lstrip(".")
    groups.setdefault(extension, []).append(name)

for extension, files in sorted(groups.items()):
    print(f"{extension.upper()}: {len(files)} file(s)")
`,
        debug: `rows = ["Ada,92", "Grace,N/A", "Alan,87", "Linus,95"]
valid_scores = []

for row in rows:
    name, raw_score = row.split(",")
    try:
        valid_scores.append((name, int(raw_score)))
    except ValueError:
        print(f"Skipped invalid score for {name}")

average = sum(score for _, score in valid_scores) / len(valid_scores)
print(f"Valid records: {len(valid_scores)}")
print(f"Average: {average:.1f}")
`,
      };

      function updateEditorMeta() {
        const count = code.value.split('\n').length;
        lines.textContent = Array.from({ length: count }, (_, i) => i + 1).join('\n');
        stats.textContent = count + (count === 1 ? ' line' : ' lines') +
          ' · ' + code.value.length + (code.value.length === 1 ? ' character' : ' characters');
        document.getElementById('pgDirty').title = 'Saved on this device';
      }

      code.addEventListener('input', updateEditorMeta);
      code.addEventListener('scroll', () => { lines.scrollTop = code.scrollTop; });
      updateEditorMeta();

      function replaceCode(next, action) {
        if (code.value.trim() && code.value !== next &&
            !window.confirm(action + ' will replace your current code. Continue?')) return false;
        code.value = next;
        code.dispatchEvent(new Event('input', { bubbles: true }));
        code.focus({ preventScroll: true });
        code.setSelectionRange(0, 0);
        return true;
      }

      document.querySelectorAll('[data-recipe]').forEach(btn => {
        btn.addEventListener('click', () => {
          const recipe = recipes[btn.dataset.recipe];
          if (!recipe) return;
          if (!replaceCode(recipe, 'Loading this recipe')) return;
          document.querySelectorAll('[data-recipe]').forEach(item => item.classList.remove('active'));
          btn.classList.add('active');
        });
      });

      function getHistory() {
        try { return JSON.parse(localStorage.getItem(historyKey) || '[]'); }
        catch (_) { return []; }
      }

      function saveHistory(items) {
        try { localStorage.setItem(historyKey, JSON.stringify(items.slice(0, 5))); }
        catch (_) {}
      }

      function renderHistory() {
        const history = getHistory();
        historyEl.textContent = '';
        if (!history.length) {
          const empty = document.createElement('p');
          empty.className = 'history-empty';
          empty.textContent = 'Your five most recent runs will appear here.';
          historyEl.appendChild(empty);
          return;
        }
        history.forEach((item, index) => {
          const row = document.createElement('article');
          row.className = 'history-item ' + (item.ok ? 'success' : 'failed');

          const state = document.createElement('span');
          state.className = 'history-state';
          state.textContent = item.ok ? 'Passed' : 'Needs attention';

          const body = document.createElement('div');
          const title = document.createElement('strong');
          title.textContent = item.filename || 'playground.py';
          const summary = document.createElement('small');
          const when = new Date(item.at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
          summary.textContent = (item.ok ? 'Completed' : 'Error') + ' · ' + item.ms + ' ms · ' + when;
          body.append(title, summary);

          const restore = document.createElement('button');
          restore.type = 'button';
          restore.textContent = 'Restore';
          restore.addEventListener('click', () => {
            if (replaceCode(item.code, 'Restoring this run')) {
              filename.value = item.filename || 'playground.py';
              window.scrollTo({ top: document.querySelector('.playground-ide').offsetTop - 90, behavior: 'smooth' });
            }
          });

          row.append(state, body, restore);
          historyEl.appendChild(row);
        });
      }

      async function runPlayground() {
        if (!code.value.trim()) {
          out.classList.remove('error');
          out.textContent = '› Your editor is blank. Write Python or load a recipe, then run it.';
          code.focus({ preventScroll: true });
          return;
        }
        runBtn.disabled = true;
        runBtn.innerHTML = '⏳ Running…';
        runtime.className = 'ide-runtime loading';
        runtimeText.textContent = pyodideReady ? 'Running your code' : 'Loading Python engine';
        runStatus.textContent = 'Running…';
        runMeta.textContent = 'Fresh process started';
        out.classList.remove('error');
        out.textContent = pyodideReady ? '› Running…' : '› Loading Python for the first time…';

        const started = performance.now();
        const result = await run(code.value);
        const elapsed = Math.max(1, Math.round(performance.now() - started));

        out.textContent = result.output;
        out.classList.toggle('error', !result.ok);
        runtime.className = 'ide-runtime ' + (result.ok ? 'ready' : 'failed');
        runtimeText.textContent = result.ok ? 'Python ready' : 'Run finished with an error';
        runStatus.textContent = result.ok ? 'Completed successfully' : 'Needs attention';
        runMeta.textContent = elapsed + ' ms · ' + result.output.split('\n').length + ' output line(s)';
        runBtn.disabled = false;
        runBtn.innerHTML = '▶ Run Python <kbd>⌘↵</kbd>';

        const history = getHistory();
        history.unshift({
          ok: result.ok,
          code: code.value,
          output: result.output.slice(0, 1200),
          ms: elapsed,
          at: Date.now(),
          filename: filename.value,
        });
        saveHistory(history);
        renderHistory();
      }

      runBtn.addEventListener('click', runPlayground);
      code.addEventListener('pysprint:run', runPlayground);

      const clear = document.getElementById('pgClear');
      clear && clear.addEventListener('click', () => {
        out.classList.remove('error');
        out.textContent = '› Console cleared.';
        runStatus.textContent = 'No active output';
        runMeta.textContent = 'Fresh process every run';
      });

      document.getElementById('pgCopyOut').addEventListener('click', (e) => {
        const copyBtn = e.currentTarget;   // currentTarget is null inside the async callback
        navigator.clipboard.writeText(out.textContent).then(() => {
          const original = copyBtn.textContent;
          copyBtn.textContent = 'Copied';
          setTimeout(() => { copyBtn.textContent = original; }, 1200);
        }).catch(() => {});
      });

      document.getElementById('pgDownload').addEventListener('click', () => {
        const safeName = (filename.value || 'playground.py')
          .replace(/[^a-zA-Z0-9._-]/g, '-')
          .replace(/\.py$/i, '') + '.py';
        filename.value = safeName;
        const blob = new Blob([code.value], { type: 'text/x-python;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = safeName;
        link.click();
        URL.revokeObjectURL(url);
      });

      document.getElementById('pgImport').addEventListener('change', (e) => {
        const file = e.target.files && e.target.files[0];
        if (!file) return;
        if (file.size > 1024 * 1024) {
          toast('Choose a Python file smaller than 1 MB.', 'error');
          e.target.value = '';
          return;
        }
        const reader = new FileReader();
        reader.onload = () => {
          if (replaceCode(String(reader.result || ''), 'Importing ' + file.name)) {
            filename.value = file.name.endsWith('.py') ? file.name : file.name + '.py';
          }
          e.target.value = '';
        };
        reader.readAsText(file);
      });

      filename.addEventListener('blur', () => {
        let value = filename.value.trim() || 'playground.py';
        if (!value.endsWith('.py')) value += '.py';
        filename.value = value;
        try { localStorage.setItem('pysprint-playground-filename', value); } catch (_) {}
      });

      let fontSize = Number(localStorage.getItem('pysprint-playground-font') || 15);
      function applyFontSize() {
        fontSize = Math.max(12, Math.min(20, fontSize));
        ide.style.setProperty('--pg-font-size', fontSize + 'px');
        try { localStorage.setItem('pysprint-playground-font', String(fontSize)); } catch (_) {}
      }
      document.getElementById('pgFontDown').addEventListener('click', () => { fontSize--; applyFontSize(); });
      document.getElementById('pgFontUp').addEventListener('click', () => { fontSize++; applyFontSize(); });
      applyFontSize();

      const wrapBtn = document.getElementById('pgWrap');
      const savedWrap = localStorage.getItem('pysprint-playground-wrap');
      let wraps = savedWrap === null ? true : savedWrap === '1';
      function applyWrap() {
        code.wrap = wraps ? 'soft' : 'off';
        code.classList.toggle('wrap-enabled', wraps);
        wrapBtn.classList.toggle('active', wraps);
        wrapBtn.setAttribute('aria-pressed', String(wraps));
        try { localStorage.setItem('pysprint-playground-wrap', wraps ? '1' : '0'); } catch (_) {}
      }
      wrapBtn.addEventListener('click', () => { wraps = !wraps; applyWrap(); });
      applyWrap();

      document.getElementById('pgClearHistory').addEventListener('click', () => {
        saveHistory([]);
        renderHistory();
      });
      renderHistory();
    },
  };

  window.PyRunner = PyRunner;
  window.PySprint = PySprint;
})();
