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
      PyRunner.wireSimple('exampleRun', 'exampleCode', 'exampleOut');
      const reset = document.getElementById('exampleReset');
      reset && reset.addEventListener('click', () => { exCode.value = cfg.example; });

      // Challenge (expected output embedded as JSON to survive newlines)
      const spec = JSON.parse(document.getElementById('challengeSpec').textContent);
      let challengePassed = false;
      wireChallenge({
        expected: spec.expected,
        onPass() {
          challengePassed = true;
          confetti(document.getElementById('challengeResult'));
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
          confetti(document.getElementById('challengeResult'));
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
          state.textContent = isDone ? '✅' : (isOpen ? '🔓' : '🔒');
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
        enableTabKey(code);

        const check = async () => {
          const result = await execInto(code, out, btn);
          resultBox.hidden = false;
          if (result.ok && normalize(result.output) === normalize(spec.steps[i])) {
            resultBox.className = 'check-result pass';
            resultBox.innerHTML = '✅ <strong>Step complete!</strong>' +
              (i + 1 < total ? ' The next step is unlocked.' : ' That was the last one — project shipped! 🎉');
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
              ? '❌ Not quite — output doesn\'t match.<small>Expected:\n' + escapeHtml(spec.steps[i]) + '</small>'
              : '❌ Your code raised an error — read the traceback above and try again.';
          }
        };
        btn.addEventListener('click', check);
        code.addEventListener('pysprint:run', check);
      }

      render();
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
