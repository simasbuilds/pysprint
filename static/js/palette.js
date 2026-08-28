/* LearnwithPython command palette — ⌘K / Ctrl+K quick-jump to any course, lesson,
   project, challenge or page. The index is fetched once on first open and
   cached in sessionStorage; matching is a small fuzzy-subsequence scorer so
   "dictcomp" finds "Dictionary Comprehensions". */
(function () {
  'use strict';

  const modal = document.getElementById('palette');
  const input = document.getElementById('paletteInput');
  const list = document.getElementById('paletteList');
  const openBtn = document.getElementById('paletteBtn');
  const closeBtn = document.getElementById('paletteClose');
  const clearBtn = document.getElementById('paletteClear');
  if (!modal || !input || !list) return;

  const CACHE_KEY = 'pysprint-search-index';
  const KIND_ORDER = { Lesson: 0, Course: 1, Project: 2, Challenge: 3, Page: 4 };
  const isMac = /Mac|iP(hone|ad|od)/.test(navigator.platform || navigator.userAgent);
  const isTouch = window.matchMedia('(pointer: coarse)').matches;

  let items = null;
  let loading = false;
  let results = [];
  let sel = 0;
  let lastFocus = null;

  // Show the right modifier on the nav hint.
  const hint = document.getElementById('paletteHint');
  if (hint && !isMac) hint.textContent = 'Ctrl K';
  // the long placeholder truncates on a phone
  if (isTouch) input.placeholder = 'Search lessons, projects…';

  // ── index loading ────────────────────────────────────────────────
  async function loadIndex() {
    if (items || loading) return;
    loading = true;
    try {
      const cached = sessionStorage.getItem(CACHE_KEY);
      if (cached) { items = JSON.parse(cached); render(); return; }
    } catch (e) { /* private mode — just fetch */ }
    try {
      const r = await fetch('/api/search-index', { headers: { Accept: 'application/json' } });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      items = (await r.json()).items || [];
      try { sessionStorage.setItem(CACHE_KEY, JSON.stringify(items)); } catch (e) { /* quota */ }
    } catch (e) {
      items = [];
      list.innerHTML = '<div class="palette-empty">Could not load the search index. Check your connection.</div>';
      return;
    } finally {
      loading = false;
    }
    render();
  }

  // ── scoring: subsequence match, rewarding word-start hits ────────
  function score(query, text) {
    const q = query.toLowerCase(), t = text.toLowerCase();
    if (!q) return 1;
    const exact = t.indexOf(q);
    if (exact === 0) return 1000;
    if (exact > 0) return 700 - exact;

    let qi = 0, s = 0, streak = 0;
    for (let i = 0; i < t.length && qi < q.length; i++) {
      if (t[i] !== q[qi]) { streak = 0; continue; }
      s += 10 + streak * 4;
      if (i === 0 || t[i - 1] === ' ' || t[i - 1] === '-') s += 12;
      streak++; qi++;
    }
    return qi === q.length ? s : -1;
  }

  function search(query) {
    if (!items) return [];
    const q = query.trim();
    if (!q) {
      // Empty query: a short "jump to" starter set.
      return items.filter(it => it.kind === 'Page' || it.kind === 'Course').slice(0, 9);
    }
    const scored = items
      .map(it => {
        const titleScore = score(q, it.title);
        const subScore = score(q, it.sub || '') * 0.35;
        // slugs, weighted just under the title, so "lru" or "recommender"
        // find pages whose visible words differ from their url
        const kwScore = score(q, it.kw || '') * 0.8;
        const best = Math.max(titleScore, subScore, kwScore);
        return { it: it, s: best - (KIND_ORDER[it.kind] || 0) * 0.5 };
      })
      .filter(r => r.s > 0)
      .sort((a, b) => b.s - a.s)
      .slice(0, 20);

    // Keep each kind contiguous so its group heading appears exactly once,
    // with the kind that scored best listed first.
    const order = [];
    const buckets = {};
    scored.forEach(r => {
      const k = r.it.kind;
      if (!buckets[k]) { buckets[k] = []; order.push(k); }
      buckets[k].push(r.it);
    });
    return order.reduce((acc, k) => acc.concat(buckets[k]), []);
  }

  // ── rendering ────────────────────────────────────────────────────
  function esc(str) {
    return String(str).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }

  function highlight(text, query) {
    const q = query.trim().toLowerCase();
    if (!q) return esc(text);
    const i = text.toLowerCase().indexOf(q);
    if (i < 0) return esc(text);
    return esc(text.slice(0, i)) + '<mark>' + esc(text.slice(i, i + q.length)) +
           '</mark>' + esc(text.slice(i + q.length));
  }

  function render() {
    const q = input.value;
    results = search(q);
    if (!items) {
      list.innerHTML = '<div class="palette-empty">Loading…</div>';
      return;
    }
    if (!results.length) {
      list.innerHTML = '<div class="palette-empty">No matches for “' + esc(q.trim()) + '”.</div>';
      return;
    }
    sel = Math.min(sel, results.length - 1);
    let html = '', lastKind = null;
    results.forEach((it, i) => {
      if (it.kind !== lastKind) {
        html += '<div class="palette-group">' + esc(it.kind) + 's</div>';
        lastKind = it.kind;
      }
      html +=
        '<a class="palette-item' + (i === sel ? ' sel' : '') + '" role="option"' +
        ' aria-selected="' + (i === sel ? 'true' : 'false') + '"' +
        ' data-i="' + i + '" href="' + esc(it.url) + '">' +
        '<span class="palette-icon" aria-hidden="true">' +
        (window.psIcon ? window.psIcon(it.icon || 'dot', 17) : '') + '</span>' +
        '<span class="palette-text">' +
        '<span class="palette-title">' + highlight(it.title, q) + '</span>' +
        '<span class="palette-sub">' + esc(it.sub || '') + '</span>' +
        '</span>' + (isTouch ? '' : '<span class="palette-go">Open ↵</span>') + '</a>';
    });
    list.innerHTML = html;
  }

  function move(delta) {
    if (!results.length) return;
    sel = (sel + delta + results.length) % results.length;
    render();
    const el = list.querySelector('.palette-item.sel');
    if (el) el.scrollIntoView({ block: 'nearest' });
  }

  function open() {
    if (!modal.hidden) return;
    lastFocus = document.activeElement;
    modal.hidden = false;
    document.body.classList.add('nav-open');
    input.value = '';
    sel = 0;
    syncClear();
    render();
    loadIndex();
    input.focus();
    fitToViewport();
  }

  function close() {
    if (modal.hidden) return;
    modal.hidden = true;
    modal.style.height = '';
    modal.style.top = '';
    document.body.classList.remove('nav-open');
    input.blur();
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  // ── keep the sheet inside the *visual* viewport ──────────────────
  // On phones the software keyboard shrinks the visual viewport without
  // changing the layout viewport, so a 100vh sheet puts its results behind
  // the keyboard. visualViewport reports the space actually left.
  const vv = window.visualViewport;
  function fitToViewport() {
    if (!vv || modal.hidden) return;
    modal.style.height = vv.height + 'px';
    modal.style.top = vv.offsetTop + 'px';
  }
  if (vv) {
    vv.addEventListener('resize', fitToViewport);
    vv.addEventListener('scroll', fitToViewport);
  }

  // ── wiring ───────────────────────────────────────────────────────
  if (openBtn) openBtn.addEventListener('click', open);

  document.addEventListener('keydown', (e) => {
    const cmdK = (e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k';
    if (cmdK) { e.preventDefault(); modal.hidden ? open() : close(); return; }

    // "/" opens search, but not while typing somewhere.
    if (e.key === '/' && modal.hidden && !e.metaKey && !e.ctrlKey && !e.altKey) {
      const t = e.target;
      const typing = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
      if (!typing) { e.preventDefault(); open(); }
    }
  });

  modal.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { e.preventDefault(); close(); }
    else if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    else if (e.key === 'Enter') {
      const hit = results[sel];
      if (hit) { e.preventDefault(); window.location.href = hit.url; }
    } else if (e.key === 'Tab') {
      // Trap focus inside the dialog — it is the only focusable thing.
      e.preventDefault();
      input.focus();
    }
  });

  function syncClear() { if (clearBtn) clearBtn.hidden = !input.value; }
  input.addEventListener('input', () => { sel = 0; syncClear(); render(); });
  if (clearBtn) clearBtn.addEventListener('click', () => {
    input.value = ''; sel = 0; syncClear(); render(); input.focus();
  });
  if (closeBtn) closeBtn.addEventListener('click', close);
  modal.addEventListener('click', (e) => { if (e.target === modal) close(); });
  list.addEventListener('mousemove', (e) => {
    const item = e.target.closest('.palette-item');
    if (!item) return;
    const i = parseInt(item.dataset.i, 10);
    if (i !== sel) { sel = i; render(); }
  });
})();
