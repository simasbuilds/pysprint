/* LearnWithPython — inline glossary.

   Auto-links the first mention of each jargon term inside lesson content
   and shows a plain-English definition in a popover. Nobody has to leave
   the lesson (or the site) to find out what "iterable" means.

   Deliberately conservative: only real prose is touched — never code
   blocks, headings, links or anything already interactive — and each term
   is linked once per lesson so the page doesn't turn into a sea of dots.
*/
(function () {
  'use strict';

  var dataEl = document.getElementById('glossaryData');
  var scope = document.querySelector('.lesson-content');
  if (!dataEl || !scope) return;

  var TERMS;
  try { TERMS = JSON.parse(dataEl.textContent); } catch (_) { return; }
  if (!TERMS || !TERMS.length) return;

  var used = Object.create(null);
  var SKIP = /^(CODE|PRE|A|BUTTON|H1|H2|H3|H4|SCRIPT|STYLE|KBD|TEXTAREA)$/;

  function walk(node) {
    for (var i = 0; i < node.childNodes.length; i++) {
      var child = node.childNodes[i];
      if (child.nodeType === 3) {
        i += linkify(child);
      } else if (child.nodeType === 1 && !SKIP.test(child.tagName) &&
                 !child.classList.contains('gloss')) {
        walk(child);
      }
    }
  }

  /** Wrap the first unused term found in this text node. Returns nodes added. */
  function linkify(textNode) {
    var text = textNode.nodeValue;
    if (!text || text.length < 4) return 0;

    for (var i = 0; i < TERMS.length; i++) {
      var term = TERMS[i][0];
      if (used[term]) continue;
      // whole word(s), case-insensitive, allow a trailing plural "s"
      var re = new RegExp('\\b(' + term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')(s?)\\b', 'i');
      var m = re.exec(text);
      if (!m) continue;

      used[term] = true;
      var before = text.slice(0, m.index);
      var after = text.slice(m.index + m[0].length);

      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'gloss';
      btn.textContent = m[0];
      btn.setAttribute('aria-label', m[0] + ' — what does this mean?');
      btn.dataset.term = term;

      var parent = textNode.parentNode;
      parent.replaceChild(btn, textNode);
      if (before) parent.insertBefore(document.createTextNode(before), btn);
      if (after) parent.insertBefore(document.createTextNode(after), btn.nextSibling);
      return 1;
    }
    return 0;
  }

  walk(scope);

  // ── popover ────────────────────────────────────────────────────────
  var defs = {};
  TERMS.forEach(function (t) { defs[t[0]] = t[1]; });

  var pop = document.createElement('div');
  pop.className = 'gloss-pop';
  pop.setAttribute('role', 'dialog');
  pop.hidden = true;
  document.body.appendChild(pop);
  var openFor = null;

  function show(btn) {
    var term = btn.dataset.term;
    pop.innerHTML = '<strong>' + btn.textContent + '</strong><p>' + (defs[term] || '') + '</p>' +
      '<span class="gloss-pop-foot">Plain-English glossary</span>';
    pop.hidden = false;
    openFor = btn;

    var r = btn.getBoundingClientRect();
    var pw = Math.min(320, window.innerWidth - 24);
    pop.style.width = pw + 'px';
    var left = Math.min(Math.max(12, r.left + r.width / 2 - pw / 2), window.innerWidth - pw - 12);
    var top = r.bottom + window.scrollY + 10;
    // flip above when it would fall off the bottom of the screen
    if (r.bottom + pop.offsetHeight + 24 > window.innerHeight) {
      top = r.top + window.scrollY - pop.offsetHeight - 10;
    }
    pop.style.left = left + 'px';
    pop.style.top = top + 'px';
    btn.setAttribute('aria-expanded', 'true');
  }

  function hide() {
    if (!openFor) return;
    openFor.setAttribute('aria-expanded', 'false');
    pop.hidden = true;
    openFor = null;
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.gloss');
    if (btn) {
      e.preventDefault();
      if (openFor === btn) { hide(); return; }
      hide();
      show(btn);
      return;
    }
    if (!e.target.closest('.gloss-pop')) hide();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && openFor) { var b = openFor; hide(); b.focus(); }
  });
  window.addEventListener('scroll', hide, { passive: true });
  window.addEventListener('resize', hide);

  // Hover is a nice shortcut on desktop, but never the only way in.
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    scope.addEventListener('mouseover', function (e) {
      var btn = e.target.closest('.gloss');
      if (btn && openFor !== btn) { hide(); show(btn); }
    });
  }
})();
