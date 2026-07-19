/* PySprint shared UI: nav, toasts, achievement modal. */
(function () {
  'use strict';

  // Mobile nav
  const burger = document.getElementById('navBurger');
  const links = document.getElementById('navLinks');
  if (burger && links) {
    burger.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(open));
    });
  }

  // Toasts
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

  // Achievement modal — queue so multiple unlocks show one after another
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
