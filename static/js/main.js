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
    '.dash-course, .achieve-tile, .stat, .callout, .project-card, .feature-slab, ' +
    '.learn-card, .use-case-card, .how-card, .method-step, .about-principles article');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !reduceMotion) {
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
