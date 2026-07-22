/* LearnWithPython Smart Review — a lightweight spaced-repetition engine (SM-2 style).
   Card state lives in localStorage: {ease, intervalMin, due, reps}.
   Grades: 0 Again (<1m) · 1 Hard (10m) · 2 Good (1d) · 3 Easy (4d) */
(function () {
  'use strict';

  const STORE_KEY = 'pysprint-review-v1';
  const cards = JSON.parse(document.getElementById('cardData').textContent);

  function cardId(c) {
    // Stable id from the question text
    let h = 0;
    const s = c.course + '|' + c.q;
    for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
    return 'c' + (h >>> 0).toString(36);
  }

  function loadState() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY)) || {}; }
    catch (e) { return {}; }
  }
  function saveState(state) { localStorage.setItem(STORE_KEY, JSON.stringify(state)); }

  const state = loadState();
  const now = () => Date.now();

  function schedule(st, grade) {
    // minutes for the next interval
    st.reps = (st.reps || 0) + 1;
    st.ease = st.ease || 2.5;
    if (grade === 0) { st.intervalMin = 1; st.ease = Math.max(1.3, st.ease - 0.2); }
    else if (grade === 1) { st.intervalMin = 10; st.ease = Math.max(1.3, st.ease - 0.05); }
    else if (grade === 2) {
      st.intervalMin = st.intervalMin && st.intervalMin >= 10
        ? Math.round(st.intervalMin * st.ease) : 60 * 24;
    } else {
      st.ease += 0.1;
      st.intervalMin = st.intervalMin && st.intervalMin >= 10
        ? Math.round(st.intervalMin * st.ease * 1.4) : 60 * 24 * 4;
    }
    st.due = now() + st.intervalMin * 60 * 1000;
    return st;
  }

  function dueCards() {
    return cards.filter(c => {
      const st = state[cardId(c)];
      return !st || st.due <= now();
    });
  }

  // UI
  const elQ = document.getElementById('cardQuestion');
  const elA = document.getElementById('cardAnswer');
  const elE = document.getElementById('cardExplain');
  const elCourse = document.getElementById('cardCourse');
  const front = document.getElementById('cardFront');
  const back = document.getElementById('cardBack');
  const flashcard = document.getElementById('flashcard');
  const actions = document.getElementById('reviewActions');
  const doneMsg = document.getElementById('reviewDone');

  let queue = [];
  let current = null;
  let flipped = false;

  function updateStats() {
    const due = dueCards().length;
    const learned = Object.keys(state).filter(k => state[k].reps >= 3).length;
    const seen = Object.keys(state).length;
    document.getElementById('statDue').textContent = due;
    document.getElementById('statNew').textContent = cards.length - seen;
    document.getElementById('statLearned').textContent = learned;
    document.getElementById('statTotal').textContent = cards.length;
  }

  function next() {
    updateStats();
    queue = dueCards();
    flipped = false;
    back.hidden = true;
    front.hidden = false;
    actions.hidden = true;
    if (!queue.length) {
      flashcard.style.display = 'none';
      doneMsg.hidden = false;
      return;
    }
    doneMsg.hidden = true;
    flashcard.style.display = '';
    flashcard.classList.remove('deal', 'flipping');
    void flashcard.offsetWidth;              // restart the deal animation
    flashcard.classList.add('deal');
    current = queue[Math.floor(Math.random() * Math.min(queue.length, 5))];
    elCourse.textContent = current.course;
    elQ.textContent = current.q;
    elA.textContent = current.a;
    elE.textContent = current.explain;
  }

  function flip() {
    if (!current || flipped) return;
    flipped = true;
    flashcard.classList.remove('deal');
    flashcard.classList.add('flipping');
    // Swap the faces at the animation's midpoint (90° — edge-on).
    setTimeout(() => {
      front.hidden = true;
      back.hidden = false;
      actions.hidden = false;
    }, 220);
    setTimeout(() => flashcard.classList.remove('flipping'), 500);
  }

  flashcard.addEventListener('click', flip);
  flashcard.addEventListener('keydown', (e) => {
    if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); flip(); }
  });

  actions.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = cardId(current);
      state[id] = schedule(state[id] || {}, Number(btn.dataset.grade));
      saveState(state);
      next();
    });
  });

  document.addEventListener('keydown', (e) => {
    if (!flipped) return;
    const map = { '1': 0, '2': 1, '3': 2, '4': 3 };
    if (e.key in map) {
      const id = cardId(current);
      state[id] = schedule(state[id] || {}, map[e.key]);
      saveState(state);
      next();
    }
  });

  next();
})();
