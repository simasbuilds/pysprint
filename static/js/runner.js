/* PySprint code runner — real Python 3 in the browser via Pyodide.
   Exposes:
     PyRunner.run(code) -> {ok, output}
     PyRunner.wireSimple(runBtnId, codeId, outId)
     PySprint.initLesson(cfg) / initChallenge(cfg) / initPlayground()
*/
(function () {
  'use strict';

  const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js';
  let pyodideReady = null;

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
    return i >= 0 ? text.slice(i) : text;
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

  async function execInto(codeEl, outEl, btn) {
    btn.disabled = true;
    const original = btn.textContent;
    btn.textContent = '⏳ Running…';
    outEl.classList.remove('error');
    if (!pyodideReady) outEl.textContent = 'Loading Python engine (first run only, ~5s)…';
    const result = await run(codeEl.value);
    outEl.textContent = result.output;
    if (!result.ok) outEl.classList.add('error');
    btn.disabled = false;
    btn.textContent = original;
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

    enableTabKey(code);
    hintBtn && hintBtn.addEventListener('click', () => { hintBox.hidden = !hintBox.hidden; });
    solBtn && solBtn.addEventListener('click', () => { solBox.hidden = !solBox.hidden; });

    async function check() {
      const result = await execInto(code, out, btn);
      resultBox.hidden = false;
      if (result.ok && normalize(result.output) === normalize(opts.expected)) {
        resultBox.className = 'check-result pass';
        resultBox.innerHTML = '✅ <strong>Correct!</strong> Output matches exactly.';
        opts.onPass && opts.onPass();
      } else {
        resultBox.className = 'check-result fail';
        resultBox.innerHTML = result.ok
          ? '❌ Not quite — your output doesn\'t match.<small>Expected:\n' +
            escapeHtml(opts.expected) + '</small>'
          : '❌ Your code raised an error — read the traceback above, fix it, and run again.';
      }
    }
    btn.addEventListener('click', check);
    code.addEventListener('pysprint:run', check);
  }

  function escapeHtml(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
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
      toast('✅ ' + passedMsg + ' — log in to bank the XP!', 'success');
      return;
    }
    postJSON(url, body).then(({ status, data }) => {
      if (status !== 200) return;
      if (data.first_time && data.xp_gained) {
        toast('⚡ +' + data.xp_gained + ' XP earned!', 'success');
      }
      celebrateAchievements(data.new_achievements);
    }).catch(() => {});
  }

  // ── page initialisers ──────────────────────────────────────────────
  const PySprint = {
    initLesson(cfg) {
      // Example runner
      const exCode = document.getElementById('exampleCode');
      PyRunner.wireSimple('exampleRun', 'exampleCode', 'exampleOut');
      const reset = document.getElementById('exampleReset');
      reset && reset.addEventListener('click', () => { exCode.value = cfg.example; });

      // Challenge (expected output embedded as JSON to survive newlines)
      const spec = JSON.parse(document.getElementById('challengeSpec').textContent);
      let challengePassed = false;
      wireChallenge({
        expected: spec.expected,
        onPass() { challengePassed = true; },
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
          document.getElementById('quizScore').textContent = right + '/' + total + ' correct';
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
          toast('Pass the challenge first — that\'s where the learning happens! 💪', 'error');
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
              toast('⚡ +' + data.xp_gained + ' XP — lesson complete!', 'success');
              completeBtn.textContent = '✓ Completed';
              completeBtn.dataset.done = '1';
            } else {
              toast('Already completed — nice revision session! 🔁', '');
            }
            celebrateAchievements(data.new_achievements);
          })
          .catch(() => toast('Network error saving progress.', 'error'));
      });
    },

    initChallenge(cfg) {
      wireChallenge({
        expected: cfg.expected,
        onPass() {
          reportProgress('/api/complete-challenge', { challenge: cfg.challenge },
            cfg.loggedIn, 'Challenge solved');
        },
      });
    },

    initPlayground() {
      const code = document.getElementById('pgCode');
      const saved = localStorage.getItem('pysprint-playground');
      if (saved) code.value = saved;
      code.addEventListener('input', () => localStorage.setItem('pysprint-playground', code.value));
      PyRunner.wireSimple('pgRun', 'pgCode', 'pgOut');
      const clear = document.getElementById('pgClear');
      clear && clear.addEventListener('click', () => {
        document.getElementById('pgOut').textContent = 'Output cleared.';
      });
    },
  };

  window.PyRunner = PyRunner;
  window.PySprint = PySprint;
})();
