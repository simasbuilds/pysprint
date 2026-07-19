/* PySprint shared UI: theme, nav, toasts, achievement modal,
   scroll-reveal, count-up stats, copy buttons, progress bar, back-to-top. */
(function () {
  'use strict';

  // ── theme toggle (light default; persisted) ─────────────────────
  const themeBtn = document.getElementById('themeToggle');
  function applyThemeIcon() {
    if (!themeBtn) return;
    themeBtn.textContent = document.documentElement.dataset.theme === 'dark' ? '☀️' : '🌙';
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

  // ── mobile nav ──────────────────────────────────────────────────
  const burger = document.getElementById('navBurger');
  const links = document.getElementById('navLinks');
  if (burger && links) {
    burger.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(open));
    });
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
        btn.textContent = '✓ Copied';
        setTimeout(() => { btn.textContent = 'Copy'; }, 1400);
      }).catch(() => {});
    });
    chrome.appendChild(btn);
  });

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
    document.getElementById('achieveIcon').textContent = a.icon;
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
