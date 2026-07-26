/* LearnWithPython — guest progress.

   Anyone can work through the entire curriculum without an account:
   completions are stored on the device, the UI reflects them everywhere
   (course roadmap, sidebar, catalogue), and signing in merges that work
   into the real account via /api/sync-progress — so "log in to save your
   progress" is a promise we actually keep.
*/
(function () {
  'use strict';

  var KEY = 'lwp-guest-progress';

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; }
    catch (_) { return {}; }
  }

  function write(data) {
    try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (_) {}
  }

  var GuestProgress = {
    isDone: function (course, lesson) {
      var all = read();
      return !!(all[course] && all[course][lesson]);
    },
    doneIn: function (course) {
      return Object.keys(read()[course] || {});
    },
    /** Returns true the first time a lesson is completed. */
    complete: function (course, lesson, xp) {
      var all = read();
      if (!all[course]) all[course] = {};
      if (all[course][lesson]) return false;
      all[course][lesson] = { xp: Number(xp) || 0, at: Date.now() };
      write(all);
      return true;
    },
    totals: function () {
      var all = read(), lessons = 0, xp = 0;
      Object.keys(all).forEach(function (c) {
        Object.keys(all[c]).forEach(function (l) {
          lessons += 1;
          xp += (all[c][l] && all[c][l].xp) || 0;
        });
      });
      return { lessons: lessons, xp: xp };
    },
    /** Flat list for syncing: [{course, lesson}, …] */
    list: function () {
      var all = read(), out = [];
      Object.keys(all).forEach(function (c) {
        Object.keys(all[c]).forEach(function (l) {
          out.push({ course: c, lesson: l });
        });
      });
      return out;
    },
    clear: function () { try { localStorage.removeItem(KEY); } catch (_) {} },
  };

  window.GuestProgress = GuestProgress;

  var loggedIn = document.body && document.body.dataset.loggedIn === '1';

  // ── signed in: fold any device progress into the account, once ─────
  function syncToAccount() {
    var pending = GuestProgress.list();
    if (!pending.length) return;
    fetch('/api/sync-progress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completions: pending }),
    })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) {
        if (!data) return;
        GuestProgress.clear();                    // only drop it once saved
        if (data.synced > 0) {
          if (window.toast) {
            toast('Synced ' + data.synced + ' lesson' + (data.synced === 1 ? '' : 's') +
                  ' from this device' + (data.xp_gained ? ' — +' + data.xp_gained + ' XP' : '') + '!',
                  'success');
          }
          if (window.celebrateAchievements) celebrateAchievements(data.new_achievements);
          // Reflect the freshly-synced state without a manual refresh.
          setTimeout(function () { window.location.reload(); }, 2200);
        }
      })
      .catch(function () { /* keep local copy for the next attempt */ });
  }

  // ── guest: hydrate the server-rendered UI from device progress ─────
  function hydrateCourseRoadmap() {
    var list = document.querySelector('.lesson-list[data-course]');
    if (!list) return;
    var slug = list.dataset.course;
    var done = GuestProgress.doneIn(slug);
    var rows = Array.prototype.slice.call(list.querySelectorAll('[data-lesson-slug]'));
    if (!rows.length) return;

    var completed = 0, nextRow = null;
    rows.forEach(function (row) {
      var isDone = done.indexOf(row.dataset.lessonSlug) !== -1;
      row.classList.remove('is-next');
      row.querySelectorAll('.next-up-badge').forEach(function (b) { b.remove(); });
      if (isDone) {
        completed += 1;
        row.classList.add('is-done');
        var num = row.querySelector('.lesson-num');
        if (num && !num.querySelector('.ui-icon')) num.innerHTML = iconMarkup('check');
        var go = row.querySelector('.course-row-go');
        if (go) go.textContent = 'Review →';
      } else if (!nextRow) {
        nextRow = row;
      }
    });

    if (nextRow) {
      nextRow.classList.add('is-next');
      var h3 = nextRow.querySelector('h3');
      if (h3 && !h3.querySelector('.next-up-badge')) {
        var badge = document.createElement('span');
        badge.className = 'next-up-badge';
        badge.textContent = completed ? 'Next up' : 'Start here';
        h3.appendChild(document.createTextNode(' '));
        h3.appendChild(badge);
      }
    }

    updateCourseHeader(completed, rows.length, nextRow);
  }

  function updateCourseHeader(completed, total, nextRow) {
    if (!completed) return;
    var wrap = document.querySelector('[data-guest-progress]');
    if (wrap) {
      var pct = Math.round(completed / total * 100);
      wrap.hidden = false;
      var fill = wrap.querySelector('.progress-fill');
      var track = wrap.querySelector('.progress-track');
      var label = wrap.querySelector('.progress-label');
      if (fill) fill.style.width = pct + '%';
      if (track) track.setAttribute('aria-valuenow', String(pct));
      if (label) {
        label.textContent = completed + ' / ' + total + ' lessons complete · saved on this device';
      }
    }
    // "Start the course" → "Resume course"
    var resume = document.querySelector('[data-course-resume]');
    if (resume && nextRow) {
      resume.setAttribute('href', nextRow.getAttribute('href'));
      resume.textContent = 'Resume course →';
    }
  }

  function hydrateCourseCatalogue() {
    document.querySelectorAll('[data-course-card]').forEach(function (card) {
      var slug = card.dataset.courseCard;
      var total = Number(card.dataset.courseLessons) || 0;
      var completed = GuestProgress.doneIn(slug).length;
      if (!completed || !total) return;
      var pct = Math.round(completed / total * 100);
      var wrap = card.querySelector('[data-guest-progress]');
      if (!wrap) return;
      wrap.hidden = false;
      var fill = wrap.querySelector('.progress-fill');
      if (fill) fill.style.width = pct + '%';
      var label = wrap.querySelector('.progress-label');
      if (label) label.textContent = pct + '% complete · on this device';
    });
  }

  function hydrateLessonSidebar() {
    var nav = document.querySelector('[data-course-nav]');
    if (!nav) return;
    var done = GuestProgress.doneIn(nav.dataset.courseNav);
    document.querySelectorAll('.side-lesson[data-lesson-slug]').forEach(function (link) {
      if (done.indexOf(link.dataset.lessonSlug) === -1) return;
      link.classList.add('is-done');
      var badge = link.querySelector('span');
      if (badge && !badge.querySelector('.ui-icon')) badge.innerHTML = iconMarkup('check');
    });
  }

  /** A returning guest should see this lesson already ticked off. */
  function hydrateLessonComplete() {
    var btn = document.getElementById('completeBtn');
    if (!btn || btn.dataset.done) return;
    if (!GuestProgress.isDone(btn.dataset.course, btn.dataset.lesson)) return;
    btn.dataset.done = '1';
    btn.innerHTML = iconMarkup('check') + ' Completed — mark again';
  }

  function iconMarkup(name) {
    return '<svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true">' +
      '<use href="/static/images/pysprint-icons.svg#ps-' + name + '"></use></svg>';
  }

  if (loggedIn) {
    syncToAccount();
  } else {
    hydrateCourseRoadmap();
    hydrateCourseCatalogue();
    hydrateLessonSidebar();
    hydrateLessonComplete();
  }
})();
