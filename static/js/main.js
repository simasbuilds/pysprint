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
    '.dash-course, .achieve-tile, .stat, .callout, .project-card, .feature-slab');
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
        btn.textContent = 'Copied';
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
