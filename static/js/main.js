/* LearnwithPython shared UI: theme, nav, toasts, achievement modal,
   scroll-reveal, count-up stats, copy buttons, progress bar, back-to-top. */
(function () {
  'use strict';

  // ── icons ───────────────────────────────────────────────────────
  // Markup pointing at the <symbol> sprite base.html renders once, so JS
  // and Jinja draw from the same icon set.
  function psIcon(name, size, cls) {
    var s = size || 16;
    return '<svg class="icon ' + (cls || '') + '" width="' + s + '" height="' + s +
           '" aria-hidden="true" focusable="false"><use href="#i-' + name + '"/></svg>';
  }
  window.psIcon = psIcon;

  // ── theme toggle (light default; persisted) ─────────────────────
  // Two toggles exist — one in the bar, one in the mobile drawer, because a
  // narrow phone bar has no room for three 44px controls.
  const themeBtns = document.querySelectorAll('.theme-toggle');
  // Each button holds both icons; CSS shows whichever matches the theme.
  function applyThemeIcon() {
    const dark = document.documentElement.dataset.theme === 'dark';
    themeBtns.forEach(b => b.setAttribute(
      'aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme'));
  }
  applyThemeIcon();
  themeBtns.forEach(btn => btn.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    localStorage.setItem('pysprint-theme', next);
    applyThemeIcon();
  }));

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

  // ── mobile nav ──────────────────────────────────────────────────
  // Closes on link click, Escape, outside click and on resize back to
  // desktop, and locks body scroll while open.
  const burger = document.getElementById('navBurger');
  const links = document.getElementById('navLinks');
  if (burger && links) {
    const setMenu = (open) => {
      links.classList.toggle('open', open);
      burger.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('nav-open', open);
    };
    const isOpen = () => links.classList.contains('open');

    burger.addEventListener('click', (e) => { e.stopPropagation(); setMenu(!isOpen()); });
    links.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('click', (e) => {
      if (isOpen() && !links.contains(e.target) && !burger.contains(e.target)) setMenu(false);
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && isOpen()) { setMenu(false); burger.focus(); }
    });
    window.addEventListener('resize', () => { if (window.innerWidth > 900 && isOpen()) setMenu(false); });
  }

  // ── scroll-reveal: cards & rows animate in as they enter view ───
  const revealTargets = document.querySelectorAll(
    '.course-card, .feature, .challenge-card, .course-row, .lesson-row, ' +
    '.dash-course, .achieve-tile, .stat, .callout');
  if ('IntersectionObserver' in window && revealTargets.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e, i) => {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -30px 0px' });
    revealTargets.forEach((el, i) => {
      el.classList.add('reveal');
      el.style.transitionDelay = (i % 6) * 60 + 'ms';
      io.observe(el);
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
        btn.innerHTML = psIcon('check', 13) + ' Copied';
        setTimeout(() => { btn.textContent = 'Copy'; }, 1400);
      }).catch(() => {});
    });
    chrome.appendChild(btn);
  });

  // ── 3D tilt on hero card & course cards (pointer devices only) ──
  if (window.matchMedia('(pointer: fine)').matches &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
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

  // ── toasts ──────────────────────────────────────────────────────
  const TOAST_ICONS = { success: 'check-circle', error: 'alert', '': 'sparkles' };
  window.toast = function (msg, type) {
    const wrap = document.getElementById('toasts');
    if (!wrap) return;
    const el = document.createElement('div');
    el.className = 'toast ' + (type || '');
    el.setAttribute('role', 'status');
    el.title = 'Click to dismiss';

    const icon = document.createElement('span');
    icon.className = 'toast-icon';
    icon.setAttribute('aria-hidden', 'true');
    icon.innerHTML = psIcon(TOAST_ICONS[type || ''] || TOAST_ICONS[''], 17);
    const body = document.createElement('span');
    body.className = 'toast-msg';
    body.textContent = msg;
    el.append(icon, body);

    const dismiss = () => {
      el.style.opacity = '0';
      el.style.transform = 'translateX(40px)';
      el.style.transition = 'opacity .3s, transform .3s';
      setTimeout(() => el.remove(), 350);
    };
    el.addEventListener('click', dismiss);
    wrap.appendChild(el);
    // Keep at most four on screen so a burst of XP toasts cannot bury the page.
    while (wrap.children.length > 4) wrap.firstElementChild.remove();
    setTimeout(dismiss, 3800);
  };

  // ── achievement modal queue ─────────────────────────────────────
  const modal = document.getElementById('achieveModal');
  const queue = [];
  let showing = false;

  function showNext() {
    if (!queue.length) { showing = false; modal.hidden = true; return; }
    showing = true;
    const a = queue.shift();
    document.getElementById('achieveIcon').innerHTML = psIcon(a.icon, 40);
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
