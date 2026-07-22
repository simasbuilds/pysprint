/* PySprint shared UI: theme, nav, toasts, achievement modal,
   scroll-reveal, count-up stats, copy buttons, progress bar, back-to-top. */
(function () {
  'use strict';

  // ── theme toggle (light default; persisted) ─────────────────────
  const themeBtn = document.getElementById('themeToggle');
  function applyThemeIcon() {
    if (!themeBtn) return;
    const dark = document.documentElement.dataset.theme === 'dark';
    const use = themeBtn.querySelector('use');
    if (use) use.setAttribute('href', themeBtn.dataset.iconBase + '#ps-' + (dark ? 'sun' : 'moon'));
    themeBtn.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
  }
  applyThemeIcon();
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = next;
      localStorage.setItem('pysprint-theme', next);
      applyThemeIcon();
    });
  }

  // ── sticky nav shadow on scroll ─────────────────────────────────
  const nav = document.querySelector('.nav');
  const readBar = document.getElementById('readProgress');
  const toTop = document.getElementById('toTop');
  function onScroll() {
    const y = window.scrollY;
    if (nav) nav.classList.toggle('scrolled', y > 8);
    if (readBar) {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      readBar.style.width = h > 0 ? (y / h * 100) + '%' : '0';
    }
    if (toTop) toTop.classList.toggle('show', y > 600);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  // ── hero depth: restrained pointer parallax on capable devices ──
  const heroVisual = document.querySelector('.hero-visual');
  if (heroVisual &&
      window.matchMedia('(pointer: fine)').matches &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    let frame = 0;
    heroVisual.addEventListener('pointermove', (event) => {
      if (frame) cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const rect = heroVisual.getBoundingClientRect();
        const x = (event.clientX - rect.left) / rect.width - 0.5;
        const y = (event.clientY - rect.top) / rect.height - 0.5;
        heroVisual.style.setProperty('--hero-x', (x * 10).toFixed(2) + 'px');
        heroVisual.style.setProperty('--hero-y', (y * 8).toFixed(2) + 'px');
        heroVisual.style.setProperty('--hero-rx', (-y * 2.2).toFixed(2) + 'deg');
        heroVisual.style.setProperty('--hero-ry', (x * 2.2).toFixed(2) + 'deg');
        heroVisual.style.setProperty('--console-x', (-x * 5).toFixed(2) + 'px');
        heroVisual.style.setProperty('--console-y', (-y * 4).toFixed(2) + 'px');
      });
    });
    heroVisual.addEventListener('pointerleave', () => {
      heroVisual.style.setProperty('--hero-x', '0px');
      heroVisual.style.setProperty('--hero-y', '0px');
      heroVisual.style.setProperty('--hero-rx', '0deg');
      heroVisual.style.setProperty('--hero-ry', '0deg');
      heroVisual.style.setProperty('--console-x', '0px');
      heroVisual.style.setProperty('--console-y', '0px');
    });
  }

  // ── mobile nav ──────────────────────────────────────────────────
  const burger = document.getElementById('navBurger');
  const links = document.getElementById('navLinks');
  const menuButtons = Array.from(document.querySelectorAll('.nav-menu-trigger[data-menu]'));

  function closeMenus(exceptButton) {
    menuButtons.forEach(button => {
      if (button === exceptButton) return;
      const panel = document.getElementById(button.dataset.menu);
      if (panel) panel.hidden = true;
      button.setAttribute('aria-expanded', 'false');
    });
  }

  menuButtons.forEach(button => {
    const panel = document.getElementById(button.dataset.menu);
    if (!panel) return;
    button.addEventListener('click', (e) => {
      e.stopPropagation();
      const opening = panel.hidden;
      closeMenus(button);
      panel.hidden = !opening;
      button.setAttribute('aria-expanded', String(opening));
    });
    panel.addEventListener('click', e => e.stopPropagation());
  });
  document.addEventListener('click', () => closeMenus());
  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    const openButton = menuButtons.find(button => button.getAttribute('aria-expanded') === 'true');
    closeMenus();
    if (openButton) openButton.focus();
  });

  if (burger && links) {
    burger.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('nav-open', open);
      if (!open) closeMenus();
    });
    links.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
      links.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('nav-open');
      closeMenus();
    }));
  }

  // ── scroll-reveal: cards & rows animate in as they enter view ───
  const revealTargets = document.querySelectorAll(
    '.course-card, .feature, .challenge-card, .course-row, .lesson-row, ' +
    '.dash-course, .achieve-tile, .stat, .callout, .project-card, .feature-slab, ' +
    '.learn-card, .use-case-card, .how-card, .method-step, .about-principles article, ' +
    '.usecase-card, .proof-strip > div');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !reduceMotion && revealTargets.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -30px 0px' });

    revealTargets.forEach((el, i) => {
      if (el.dataset.reveal) return;               // handled below
      el.classList.add('reveal');
      el.style.transitionDelay = (i % 6) * 60 + 'ms';
      io.observe(el);
    });

    // Directional reveals: any element with data-reveal="left|right|scale|up"
    document.querySelectorAll('[data-reveal]').forEach((el, i) => {
      const kind = { left: 'reveal-left', right: 'reveal-right', scale: 'reveal-scale' }[el.dataset.reveal];
      el.classList.add(kind || 'reveal');
      el.style.transitionDelay = (i % 4) * 80 + 'ms';
      io.observe(el);
    });

    // Progress bars grow from zero the first time they're seen.
    document.querySelectorAll('.progress-fill').forEach(fill => {
      const target = fill.style.width;
      if (!target) return;
      fill.style.width = '0%';
      const pio = new IntersectionObserver((entries) => {
        entries.forEach(e => {
          if (!e.isIntersecting) return;
          pio.unobserve(e.target);
          requestAnimationFrame(() => { fill.style.width = target; });
        });
      }, { threshold: 0.4 });
      pio.observe(fill.parentElement || fill);
    });
  }

  // ── count-up numbers (elements with data-count) ─────────────────
  const counters = document.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    const cio = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        cio.unobserve(e.target);
        const target = parseInt(e.target.dataset.count, 10);
        const t0 = performance.now(), dur = 1100;
        (function tick(t) {
          const p = Math.min((t - t0) / dur, 1);
          e.target.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(tick);
        })(t0);
      });
    }, { threshold: 0.5 });
    counters.forEach(el => cio.observe(el));
  }

  // ── copy buttons on every editor ────────────────────────────────
  document.querySelectorAll('.editor-chrome').forEach(chrome => {
    const block = chrome.parentElement;
    const source = block && block.querySelector('.code-input');
    if (!source) return;
    const btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.type = 'button';
    btn.textContent = 'Copy';
    btn.addEventListener('click', () => {
      navigator.clipboard.writeText(source.value).then(() => {
        btn.textContent = 'Copied';
        setTimeout(() => { btn.textContent = 'Copy'; }, 1400);
      }).catch(() => {});
    });
    chrome.appendChild(btn);
  });

  // ── 3D tilt on hero card & course cards (pointer devices only) ──
  if (window.matchMedia('(pointer: fine)').matches && !reduceMotion) {
    document.querySelectorAll('.course-card, .project-card').forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform =
          'perspective(700px) rotateY(' + (x * 6) + 'deg) rotateX(' + (-y * 6) + 'deg) translateY(-4px)';
      });
      card.addEventListener('mouseleave', () => { card.style.transform = ''; });
    });
  }

  // ── cursor spotlight: cards glow toward the pointer ─────────────
  if (window.matchMedia('(pointer: fine)').matches && !reduceMotion) {
    document.querySelectorAll(
      '.course-card, .project-card, .challenge-card, .feature, .dash-course, ' +
      '.use-case-card, .achieve-tile, .learn-card, .how-card').forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const r = card.getBoundingClientRect();
        card.style.setProperty('--spot-x', (e.clientX - r.left) + 'px');
        card.style.setProperty('--spot-y', (e.clientY - r.top) + 'px');
      });
    });
  }

  // ── button press ripple ─────────────────────────────────────────
  if (!reduceMotion) {
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('.btn');
      if (!btn) return;
      const r = btn.getBoundingClientRect();
      const size = Math.max(r.width, r.height);
      const ripple = document.createElement('span');
      ripple.className = 'btn-ripple';
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = (e.clientX - r.left - size / 2) + 'px';
      ripple.style.top = (e.clientY - r.top - size / 2) + 'px';
      btn.appendChild(ripple);
      setTimeout(() => ripple.remove(), 650);
    });
  }

  // ── XP fly-up: rewards float away from the action that earned them
  window.xpFly = function (anchor, label) {
    if (reduceMotion || !anchor) return;
    const r = anchor.getBoundingClientRect();
    const el = document.createElement('div');
    el.className = 'xp-fly';
    el.textContent = label;
    el.style.left = (r.left + r.width / 2) + 'px';
    el.style.top = (r.top - 6) + 'px';
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 1600);
  };

  // ── rotating word in the hero headline ──────────────────────────
  const rotator = document.querySelector('.word-rotate[data-words]');
  if (rotator && !reduceMotion) {
    let words = [];
    try { words = JSON.parse(rotator.dataset.words) || []; } catch (_) {}
    const inner = rotator.querySelector('span');
    if (inner && words.length > 1) {
      let i = 0;
      setInterval(() => {
        inner.classList.add('out');
        setTimeout(() => {
          i = (i + 1) % words.length;
          inner.textContent = words[i];
          inner.classList.remove('out');
        }, 260);
      }, 2800);
    }
  }

  // ── ⌘K command palette ──────────────────────────────────────────
  (function initCmdk() {
    const overlay = document.getElementById('cmdk');
    const input = document.getElementById('cmdkInput');
    const list = document.getElementById('cmdkList');
    const trigger = document.getElementById('cmdkBtn');
    const dataEl = document.getElementById('cmdkData');
    if (!overlay || !input || !list || !dataEl) return;

    let data;
    try { data = JSON.parse(dataEl.textContent); } catch (_) { return; }

    const iconBase = (themeBtn && themeBtn.dataset.iconBase) || '/static/images/pysprint-icons.svg';
    const actions = [
      { label: 'Toggle light / dark theme', hint: 'Action', icon: 'moon',
        run: () => { themeBtn && themeBtn.click(); } },
      { label: 'Back to top', hint: 'Action', icon: 'rocket',
        run: () => window.scrollTo({ top: 0, behavior: 'smooth' }) },
    ];
    const items = [
      ...data.pages.map(p => ({ ...p, group: 'Pages' })),
      ...data.courses.map(c => ({ ...c, group: 'Courses' })),
      // The full curriculum is searchable but only shown once you type,
      // so the default view stays scannable.
      ...(data.lessons || []).map(l => ({ ...l, group: 'Lessons', searchOnly: true })),
      ...actions.map(a => ({ ...a, group: 'Actions' })),
    ];

    let visible = [];
    let active = 0;

    function iconSvg(name, color) {
      return '<svg class="ui-icon"' + (color ? ' style="color:' + color + '"' : '') +
        ' viewBox="0 0 24 24" aria-hidden="true"><use href="' + iconBase + '#ps-' + name + '"></use></svg>';
    }

    function render(query) {
      const q = (query || '').trim().toLowerCase();
      visible = q
        ? items.filter(it => (it.label + ' ' + (it.hint || '') + ' ' + it.group).toLowerCase().includes(q))
        : items.filter(it => !it.searchOnly);
      active = 0;
      list.textContent = '';
      if (!visible.length) {
        const empty = document.createElement('p');
        empty.className = 'cmdk-empty';
        empty.textContent = 'Nothing matches “' + query + '” — try “courses” or “playground”.';
        list.appendChild(empty);
        return;
      }
      let lastGroup = null;
      visible.forEach((it, i) => {
        if (it.group !== lastGroup) {
          lastGroup = it.group;
          const label = document.createElement('div');
          label.className = 'cmdk-group';
          label.textContent = it.group;
          list.appendChild(label);
        }
        const row = document.createElement('button');
        row.type = 'button';
        row.className = 'cmdk-item' + (i === active ? ' active' : '');
        row.setAttribute('role', 'option');
        row.dataset.index = i;
        row.innerHTML = iconSvg(it.icon || 'spark', it.color) +
          '<span class="cmdk-label"></span><small class="cmdk-hint"></small>' +
          (it.href ? '<b>↵</b>' : '<b>run</b>');
        row.querySelector('.cmdk-label').textContent = it.label;
        row.querySelector('.cmdk-hint').textContent = it.hint || '';
        row.addEventListener('click', () => choose(i));
        row.addEventListener('pointermove', () => setActive(i));
        list.appendChild(row);
      });
    }

    function setActive(i) {
      active = Math.max(0, Math.min(i, visible.length - 1));
      list.querySelectorAll('.cmdk-item').forEach(el => {
        el.classList.toggle('active', Number(el.dataset.index) === active);
      });
      const el = list.querySelector('.cmdk-item.active');
      if (el) el.scrollIntoView({ block: 'nearest' });
    }

    function choose(i) {
      const it = visible[i];
      if (!it) return;
      close();
      if (it.href) window.location.href = it.href;
      else if (it.run) it.run();
    }

    function open() {
      overlay.hidden = false;
      document.body.classList.add('cmdk-open');
      input.value = '';
      render('');
      input.focus();
    }

    function close() {
      overlay.hidden = true;
      document.body.classList.remove('cmdk-open');
    }

    trigger && trigger.addEventListener('click', open);
    overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });
    input.addEventListener('input', () => render(input.value));
    input.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') { e.preventDefault(); setActive(active + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(active - 1); }
      else if (e.key === 'Enter') { e.preventDefault(); choose(active); }
    });
    document.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        overlay.hidden ? open() : close();
      } else if (e.key === 'Escape' && !overlay.hidden) {
        close();
      }
    });
  })();

  // ── resume where you left off (works without an account) ───────
  (function initResume() {
    const RESUME_KEY = 'pysprint-last-lesson';
    const layout = document.querySelector('.lesson-layout[data-lesson-title]');
    if (layout) {
      try {
        localStorage.setItem(RESUME_KEY, JSON.stringify({
          href: location.pathname,
          title: layout.dataset.lessonTitle,
          course: layout.dataset.courseTitle,
          color: getComputedStyle(layout).getPropertyValue('--accent').trim(),
          at: Date.now(),
        }));
      } catch (_) {}
    }
    const slot = document.getElementById('resumeSlot');
    if (!slot) return;
    let last = null;
    try { last = JSON.parse(localStorage.getItem(RESUME_KEY) || 'null'); } catch (_) {}
    if (!last || !last.href || last.href === location.pathname) return;
    const link = document.createElement('a');
    link.className = 'resume-chip';
    link.href = last.href;
    if (last.color) link.style.setProperty('--accent', last.color);
    link.innerHTML = '<i></i><small>Continue where you left off</small><strong></strong><b>→</b>';
    link.querySelector('strong').textContent = last.title +
      (last.course ? ' · ' + last.course : '');
    slot.appendChild(link);
    slot.hidden = false;
  })();

  // ── lesson keyboard nav: ← previous, → next ─────────────────────
  (function initLessonKeys() {
    const prev = document.querySelector('[data-lesson-prev]');
    const next = document.querySelector('[data-lesson-next]');
    if (!prev && !next) return;
    document.addEventListener('keydown', (e) => {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target;
      if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
      if (e.key === 'ArrowLeft' && prev) window.location.href = prev.href;
      if (e.key === 'ArrowRight' && next) window.location.href = next.href;
    });
  })();

  // ── scroll-spy for on-page section nav (.spy-nav) ───────────────
  (function initSpy() {
    const nav = document.querySelector('.spy-nav');
    if (!nav || !('IntersectionObserver' in window)) return;
    const links = Array.from(nav.querySelectorAll('a[href^="#"]'));
    const sections = links
      .map(a => document.getElementById(a.getAttribute('href').slice(1)))
      .filter(Boolean);
    if (!sections.length) return;
    const byId = {};
    links.forEach(a => { byId[a.getAttribute('href').slice(1)] = a; });
    const inView = new Set();
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) inView.add(en.target.id);
        else inView.delete(en.target.id);
      });
      // Highlight the first visible section in document order.
      let current = null;
      for (const s of sections) { if (inView.has(s.id)) { current = s.id; break; } }
      links.forEach(a => a.classList.toggle('on', a === byId[current]));
    }, { rootMargin: '-15% 0px -55% 0px' });
    sections.forEach(s => io.observe(s));
  })();

  // ── toasts ──────────────────────────────────────────────────────
  window.toast = function (msg, type) {
    const wrap = document.getElementById('toasts');
    if (!wrap) return;
    const el = document.createElement('div');
    el.className = 'toast ' + (type || '');
    el.textContent = msg;
    wrap.appendChild(el);
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transition = 'opacity .3s';
      setTimeout(() => el.remove(), 350);
    }, 3800);
  };

  // ── achievement modal queue ─────────────────────────────────────
  const modal = document.getElementById('achieveModal');
  const queue = [];
  let showing = false;

  function showNext() {
    if (!queue.length) { showing = false; modal.hidden = true; return; }
    showing = true;
    const a = queue.shift();
    const iconName = /^[a-z0-9-]+$/.test(a.icon || '') ? a.icon : 'trophy';
    const iconUse = document.querySelector('#achieveIcon use');
    const iconBase = themeBtn ? themeBtn.dataset.iconBase : '/static/images/pysprint-icons.svg';
    if (iconUse) iconUse.setAttribute('href', iconBase + '#ps-' + iconName);
    document.getElementById('achieveTitle').textContent = a.title;
    document.getElementById('achieveDesc').textContent = a.desc;
    modal.hidden = false;
  }

  window.celebrateAchievements = function (list) {
    (list || []).forEach(a => queue.push(a));
    if (!showing && queue.length) showNext();
  };

  if (modal) {
    document.getElementById('achieveClose').addEventListener('click', showNext);
    modal.addEventListener('click', (e) => { if (e.target === modal) showNext(); });
  }
})();
