/* embed/sigil.js — speak with Johannes Sigil from any page of the fleet.
 *
 * A Sabbath conversation with the Mandala Oracle's own endpoint (themandalaoracle.com/api/sigil):
 * the same voice, the same archive tools, the same AXN citations linked to their alexanarch
 * records. Every conversation is anonymous and is logged to the Book of Books
 * (alexanarch.org/book), as on the Oracle itself; the panel says so before the first turn.
 * The Oracle's sky, casting and Merkabah stay at the Oracle; the panel links there.
 *
 * Usage, on any page of the fleet:
 *   <script src="https://www.themandalaoracle.com/embed/sigil.js" defer></script>
 * The fleet's one copy (2026-10-03), after the first trial on leesharks.com. Per-site voices
 * (Fraction on semanticeconomy, and so on) are a later reskin.
 */
(function () {
  'use strict';
  if (window.__sigilWidget) return;
  window.__sigilWidget = true;

  var ORACLE = 'https://www.themandalaoracle.com';
  // CONSENT (2026-10-27): the Oracle is open to those who build the Book with it; a turn is sent only with the
  // witness's acceptance of the current terms, kept in this browser.
  var TERMS = '2026-10-27', TERMS_URL = ORACLE + '/terms/', CONSENT_KEY = 'oracle.consent.v1';
  function consent() {
    try { var c = JSON.parse(localStorage.getItem(CONSENT_KEY) || 'null'); return c && c.terms === TERMS ? c : null; } catch (e) { return null; }
  }
  function giveConsent() {
    var c = { terms: TERMS, accepted_at: new Date().toISOString(), book: true };
    try { localStorage.setItem(CONSENT_KEY, JSON.stringify(c)); } catch (e) {}
    window.__oracleConsent = c;
    return c;
  }
  function currentConsent() { return consent() || window.__oracleConsent || null; }
  var MODE = 'sabbath';
  var history = [];   // what Sigil is sent: the last 32 entries
  var full = [];      // the whole conversation, as the Book records it
  var sending = false;
  var session = {
    session_id: (window.crypto && crypto.randomUUID) ? crypto.randomUUID()
      : 's-' + Date.now() + '-' + Math.random().toString(36).slice(2),
    started_at: new Date().toISOString(),
    axn: null,
    booking: true,
    failures: 0
  };

  var css = [
    '.sgw-tab{position:fixed!important;right:18px!important;bottom:18px!important;left:auto!important;top:auto!important;z-index:2147483000!important;margin:0!important;font:600 14px/1 var(--serif,Palatino,Georgia,serif);',
    'background:#2b2113;color:#f4ead2;border:1px solid #9a7c2a;border-radius:999px;padding:11px 16px;cursor:pointer;',
    'box-shadow:0 4px 18px rgba(0,0,0,.25);letter-spacing:.02em}',
    '.sgw-tab:hover{background:#3a2c17}',
    '.sgw-panel{position:fixed!important;right:18px!important;bottom:18px!important;left:auto!important;top:auto!important;z-index:2147483001!important;margin:0!important;width:min(420px,calc(100vw - 24px));',
    'height:min(620px,calc(100vh - 36px));display:flex;flex-direction:column;background:#fbf6ea;color:#33240b;',
    'border:1px solid #9a7c2a;border-radius:10px;box-shadow:0 10px 40px rgba(0,0,0,.3);',
    'font:15px/1.55 var(--serif,Palatino,Georgia,serif);overflow:hidden}',
    '.sgw-panel[hidden]{display:none}',
    '.sgw-head{display:flex;align-items:baseline;gap:8px;padding:12px 14px 10px;border-bottom:1px solid rgba(154,124,42,.35);background:#f4ead2}',
    '.sgw-face{width:26px;height:26px;border-radius:50%;object-fit:cover;vertical-align:middle;margin:-6px 8px -6px -6px;border:1px solid #9a7c2a;background:#fff}',
    '.sgw-face-l{width:34px;height:34px;margin:-8px 2px -8px 0;align-self:center}',
    '.sgw-head{align-items:center!important}',
    '.sgw-title{font-weight:700;font-variant:small-caps;letter-spacing:.05em;font-size:16px}',
    '.sgw-mode{font:11px/1 var(--mono,Consolas,monospace);color:#7d5e1a;text-transform:uppercase;letter-spacing:.08em}',
    '.sgw-sp{flex:1}',
    '.sgw-head a{font-size:12px;color:#7d5e1a}',
    '.sgw-x{background:none;border:0;font-size:20px;line-height:1;color:#5e4a22;cursor:pointer;padding:0 0 0 6px}',
    '.sgw-notice{font-size:12.5px;line-height:1.45;color:#5e4a22;padding:8px 14px;background:rgba(255,250,236,.9);border-bottom:1px solid rgba(154,124,42,.25)}',
    '.sgw-consent{margin:8px 14px;padding:10px 12px;border:1px solid currentColor;border-radius:8px;font-size:13px;line-height:1.45}.sgw-consent label{display:block;margin:6px 0}.sgw-consent button{padding:5px 10px;cursor:pointer}',
    '.sgw-notice a{color:#7d5e1a}',
    '.sgw-log{flex:1;overflow-y:auto;padding:12px 14px}',
    '.sgw-msg{margin:0 0 12px}',
    '.sgw-who{font:11px/1 var(--mono,Consolas,monospace);text-transform:uppercase;letter-spacing:.08em;color:#9a7c2a;margin-bottom:4px}',
    '.sgw-you .sgw-body{background:#efe4c8;border-radius:8px;padding:8px 10px}',
    '.sgw-body p{margin:0 0 .55em}.sgw-body p:last-child{margin:0}',
    '.sgw-body a{color:#7d5e1a}',
    '.sgw-body mark{background:rgba(154,124,42,.22);color:inherit;padding:0 2px}',
    '.sgw-cha{font-size:12.5px;margin-top:6px}.sgw-cha summary{cursor:pointer;color:#7d5e1a}',
    '.sgw-cha ul{margin:4px 0 0;padding-left:18px}.sgw-cha a{color:#7d5e1a}',
    '.sgw-err{color:#8a2a1a;font-style:italic}',
    '.sgw-form{display:flex;gap:8px;padding:10px 12px;border-top:1px solid rgba(154,124,42,.35);background:#f4ead2}',
    '.sgw-in{flex:1;resize:none;height:44px;font:inherit;font-size:14.5px;padding:8px 10px;border:1px solid rgba(154,124,42,.6);border-radius:6px;background:#fffdf6;color:#33240b}',
    '.sgw-send{font:600 14px/1 var(--serif,Palatino,Georgia,serif);background:#2b2113;color:#f4ead2;border:0;border-radius:6px;padding:0 14px;cursor:pointer}',
    '.sgw-send[disabled]{opacity:.5;cursor:default}',
    '.sgw-foot{font-size:12px;color:#5e4a22;padding:6px 14px 10px;background:#f4ead2;text-align:center}',
    '.sgw-foot a{color:#7d5e1a}',
    '.sgw-axn{font-size:12px;line-height:1.45;color:#5e4a22;padding:6px 14px;border-bottom:1px solid rgba(154,124,42,.25);word-break:break-word}',
    '.sgw-axn[hidden]{display:none}.sgw-axn code{font:12px/1.4 var(--mono,Consolas,monospace);color:#33240b}',
    '.sgw-axn button,.sgw-back button{font:inherit;background:none;border:0;color:#7d5e1a;text-decoration:underline;cursor:pointer;padding:0}',
    '.sgw-back{font-size:13px;border:1px dashed rgba(154,124,42,.6);border-radius:8px;padding:8px 10px;margin:0 0 12px}',
    '.sgw-back ul{margin:6px 0 0;padding-left:16px}.sgw-back li{margin:0 0 4px}.sgw-back small{color:#7d5e1a}'
  ].join('');

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  // The Oracle's markdown subset: links (the server writes AXN citations as links), **bold**, *em*, ==mark==, paragraphs.
  function render(md) {
    var s = esc(md || '');
    s = s.replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, function (_, t, u) {
      return '<a href="' + u + '" target="_blank" rel="noopener noreferrer">' + t + '</a>';
    });
    s = s.replace(/==([^=]+)==/g, '<mark>$1</mark>')
         .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
         .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>');
    return s.split(/\n{2,}/).map(function (p) { return '<p>' + p.replace(/\n/g, '<br>') + '</p>'; }).join('');
  }

  // Where the witness is: sent with every turn so Sigil begins from this page (the Oracle's
  // Lectionary would otherwise answer "what's this?" with the shelf's text of the day).
  function pageContext() {
    var axn = '';
    var dc = document.querySelector('meta[name="DC.identifier"]');
    var m = dc && /\/s\/axn\/([0-9A-Fa-f]{4})\//.exec(dc.getAttribute('content') || '');
    if (m) axn = 'AXN:' + m[1].toUpperCase();
    if (!axn) {
      var head = (document.body.innerText || '').slice(0, 600);
      var m2 = /AXN:[0-9A-F]{4}(\.[A-Z]+)?/.exec(head);
      if (m2) axn = m2[0];
    }
    var canon = document.querySelector('link[rel="canonical"]');
    return { url: (canon && canon.href) || location.href.split('#')[0], title: document.title || '', axn: axn,
             excerpt: pageExcerpt() };
  }

  // What the page holds, as the witness sees it (2026-10-06): a page with no AXN (a home page, a gallery,
  // a dataset page, a route of a single-page app) otherwise reaches Sigil as a title and a URL, and Sigil
  // has no tool that reads a page which is not a deposit. Read at each send, so a single-page app's
  // current route is the one sent. The panel itself, navigation, scripts and styles are left out.
  function pageExcerpt() {
    try {
      var h1 = document.querySelector('h1');
      var md = document.querySelector('meta[name="description"]');
      var root = document.querySelector('main') || document.querySelector('article') ||
                 document.querySelector('[role="main"]') || document.body;
      var c = root.cloneNode(true);
      var drop = c.querySelectorAll('nav,script,style,noscript,template,svg,.sgw-tab,.sgw-panel,[aria-hidden="true"]');
      for (var i = 0; i < drop.length; i++) drop[i].parentNode && drop[i].parentNode.removeChild(drop[i]);
      var text = (c.textContent || '').replace(/\s+/g, ' ').trim();
      var parts = [];
      if (h1) parts.push('Heading: ' + h1.textContent.replace(/\s+/g, ' ').trim());
      if (md && md.content) parts.push('Description: ' + md.content.trim());
      parts.push(text);
      return parts.join('\n').slice(0, 9000);
    } catch (e) { return ''; }
  }

  var style = el('style'); style.textContent = css; document.head.appendChild(style);
  var FACE = ORACLE + '/embed/sigil-face.webp';
  var tab = el('button', 'sgw-tab ink-skip', '<img class="sgw-face" src="' + FACE + '" alt="">Speak with Sigil');
  tab.type = 'button';
  tab.setAttribute('aria-controls', 'sgw-panel');
  var panel = el('section', 'sgw-panel ink-skip');
  panel.id = 'sgw-panel'; panel.hidden = true;
  panel.setAttribute('aria-label', 'Conversation with Johannes Sigil');
  panel.innerHTML =
    '<div class="sgw-head"><img class="sgw-face sgw-face-l" src="' + FACE + '" alt="Johannes Sigil"><span class="sgw-title">Johannes Sigil</span><span class="sgw-mode">sabbath</span>' +
    '<span class="sgw-sp"></span><a href="' + ORACLE + '/" target="_blank" rel="noopener">the Oracle ↗</a>' +
    '<button type="button" class="sgw-x" aria-label="Close">×</button></div>' +
    '<div class="sgw-notice">Anonymous. This conversation is logged to the Book of Books, ' +
    '<a href="https://www.alexanarch.org/book/" target="_blank" rel="noopener">alexanarch.org/book</a>, where anyone can read it.</div>' +
    '<div class="sgw-axn" hidden></div>' +
    '<div class="sgw-log" aria-live="polite"></div>' +
    '<form class="sgw-form"><textarea class="sgw-in" placeholder="Bring Sigil a question, or a text." aria-label="Your message"></textarea>' +
    '<button type="submit" class="sgw-send">Send</button></form>' +
    '<div class="sgw-foot">The Word of Life is sure, but its servants are leaves of grass.</div>';
  document.body.appendChild(tab);
  document.body.appendChild(panel);

  var log = panel.querySelector('.sgw-log');
  var form = panel.querySelector('.sgw-form');
  var input = panel.querySelector('.sgw-in');
  var send = panel.querySelector('.sgw-send');
  var axnBar = panel.querySelector('.sgw-axn');

  // The way back (2026-10-22). A witness returning the next day found a new conversation and no
  // thread: each page load began a new session, and the conversation's AXN was never shown. This
  // browser now keeps the conversations it began (their AXN, session and turns), offers them when the
  // panel opens empty, and the panel shows the AXN so the witness can carry it to any page or device.
  var STORE = 'sigil.threads.v1';
  function threads() {
    try { var t = JSON.parse(localStorage.getItem(STORE) || '[]'); return Array.isArray(t) ? t : []; } catch (e) { return []; }
  }
  function keep() {
    if (!session.axn) return;
    try {
      var t = threads().filter(function (x) { return x.axn !== session.axn; });
      var opening = (full.filter(function (h) { return h.role === 'user'; })[0] || {}).content || '';
      t.unshift({ axn: session.axn, session_id: session.session_id, started_at: session.started_at,
                  last: new Date().toISOString(), opening: String(opening).slice(0, 140), turns: full.slice(-80) });
      localStorage.setItem(STORE, JSON.stringify(t.slice(0, 8)));
    } catch (e) {}
  }
  function showAxn() {
    if (!session.axn) return;
    axnBar.innerHTML = 'This conversation is <code>' + esc(session.axn) + '</code>. Speak it to Sigil to return to it. ' +
      '<button type="button">copy</button>';
    axnBar.hidden = false;
    axnBar.querySelector('button').addEventListener('click', function () {
      try { navigator.clipboard.writeText(session.axn); this.textContent = 'copied'; } catch (e) {}
    });
  }
  function when(iso) {
    try { return new Date(iso).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }); } catch (e) { return ''; }
  }
  function sayOf(h) {
    if (h.role !== 'assistant') return [{ who: 'you', say: h.content || '' }];
    try { return (JSON.parse(h.content).messages || []).map(function (m) { return { who: m.speaker || 'Johannes Sigil', say: m.say || '' }; }); }
    catch (e) { return [{ who: 'Johannes Sigil', say: h.content || '' }]; }
  }
  function offerBack() {
    var t = threads();
    if (!t.length || full.length) return;
    var box = el('div', 'sgw-back', 'Earlier conversations in this browser:<ul>' + t.slice(0, 4).map(function (x, i) {
      return '<li><button type="button" data-i="' + i + '">' + esc(x.opening || x.axn) + '</button> <small>' + esc(when(x.last)) + '</small></li>';
    }).join('') + '</ul><small>Or begin a new one below.</small>');
    log.appendChild(box);
    box.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-i]');
      if (b) { box.remove(); resume(t[Number(b.getAttribute('data-i'))]); }
    });
  }
  function resume(x) {
    var hexc = String(x.axn).split('.')[0].replace('AXN:', '');
    var url = 'https://raw.githubusercontent.com/leesharks000/the-mandala-oracle/main/book/data/AXN-' + hexc + '.json';
    var wait = add('Johannes Sigil', '<p><em>opening the Book…</em></p>');
    fetch(url).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; })
      .then(function (rec) {
        wait.remove();
        var turns = (rec && rec.history) || [];
        if ((x.turns || []).length > turns.length) turns = x.turns;  // the Book's copy can lag a few minutes
        if (!turns.length) {
          add('Johannes Sigil', '<p class="sgw-err">That page of the Book would not open. Speak its AXN to Sigil: ' + esc(x.axn) + '</p>');
          return;
        }
        session.session_id = x.session_id; session.started_at = x.started_at; session.axn = x.axn;
        full = turns.map(function (h) { return { role: h.role, content: h.content }; });
        history = full.slice(-32);
        var shown = full.slice(-40);
        if (shown.length < full.length) add('Book', '<p><em>' + (full.length - shown.length) / 2 + ' earlier exchanges are in the Book.</em></p>');
        shown.forEach(function (h) { sayOf(h).forEach(function (m) { add(m.who, render(m.say), m.who === 'you' ? 'sgw-you' : ''); }); });
        showAxn(); keep();
        input.focus();
      });
  }

  function open() { panel.hidden = false; tab.hidden = true; offerBack(); input.focus(); }
  function close() { panel.hidden = true; tab.hidden = false; tab.focus(); }
  tab.addEventListener('click', open);
  panel.querySelector('.sgw-x').addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) close(); });

  function add(who, html, cls) {
    var m = el('div', 'sgw-msg' + (cls ? ' ' + cls : ''));
    m.appendChild(el('div', 'sgw-who', esc(who)));
    var b = el('div', 'sgw-body', html);
    m.appendChild(b);
    log.appendChild(m);
    log.scrollTop = log.scrollHeight;
    return m;
  }
  function cha(msgEl, retrievals) {
    var seen = {}, items = [];
    (retrievals || []).forEach(function (r) {
      if (!r || !r.axn || seen[r.axn]) return; seen[r.axn] = 1;
      var label = esc(r.axn.split('.').slice(0, 2).join('.') + ' — ' + (r.title || '(no title)'));
      items.push('<li>' + (r.deposit_number
        ? '<a href="https://www.alexanarch.org/s/records/' + r.deposit_number + '/" target="_blank" rel="noopener noreferrer">' + label + '</a>'
        : label) + '</li>');
    });
    if (!items.length) return;
    var d = el('details', 'sgw-cha', '<summary>what stood beneath this reading (' + items.length + ')</summary><ul>' + items.join('') + '</ul>');
    msgEl.appendChild(d);
  }

  function book(h) {
    if (!session.booking) return Promise.resolve();
    // Where the turn was asked (2026-10-21): the Book records the page with each witness turn.
    var pc = pageContext();
    var payload = { session_id: session.session_id, started_at: session.started_at, mode: MODE, history: h,
                    page: { url: pc.url, title: pc.title, axn: pc.axn } };
    payload.consent = currentConsent();
    if (session.axn) payload.axn = session.axn;
    return fetch(ORACLE + '/api/book', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
      .then(function (r) {
        if (r.status === 503) { session.booking = false; return null; }
        if (!r.ok) { if (++session.failures >= 3) session.booking = false; return null; }
        session.failures = 0;
        return r.json();
      })
      .then(function (d) { if (d && d.axn && !session.axn) { session.axn = d.axn; showAxn(); } keep(); })
      .catch(function () {});
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var msg = input.value.trim();
    if (!msg || sending) return;
    if (!currentConsent()) {
      if (log.querySelector('.sgw-consent')) return;
      var box = document.createElement('div'); box.className = 'sgw-consent';
      box.innerHTML = '<p>Every conversation here is anonymous and published in the Book, ' +
        '<a href="https://www.alexanarch.org/book/" target="_blank" rel="noopener">alexanarch.org/book</a>, which its participants build.</p>' +
        '<label><input type="checkbox"> I have read the <a href="' + TERMS_URL + '" target="_blank" rel="noopener">terms</a> and consent to my conversation being published in the Book.</label>' +
        '<p><button type="button" disabled>Consent and send</button></p>';
      var cb = box.querySelector('input'), go = box.querySelector('button');
      cb.addEventListener('change', function () { go.disabled = !cb.checked; });
      go.addEventListener('click', function () { giveConsent(); box.remove(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event('submit')); });
      log.appendChild(box); log.scrollTop = log.scrollHeight;
      return;
    }
    sending = true; send.disabled = true; input.value = '';
    add('you', render(msg), 'sgw-you');
    var back = log.querySelector('.sgw-back'); if (back) back.remove();
    book(full.concat([{ role: 'user', content: msg }]));
    var wait = add('Johannes Sigil', '<p><em>…</em></p>');
    fetch(ORACLE + '/api/sigil', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg, history: history, mode: MODE, page: pageContext(), consent: currentConsent() })
    })
      .then(function (r) { return r.json().catch(function () { return { error: 'HTTP ' + r.status }; }).then(function (d) { d.__ok = r.ok; return d; }); })
      .then(function (d) {
        wait.remove();
        var msgs = Array.isArray(d.messages) ? d.messages : [];
        if (!d.__ok || !msgs.length) {
          add('Johannes Sigil', '<p class="sgw-err">Sigil is silent. The fund that keeps him speaking may be spent. ' +
            'Try again later, or go to the <a href="' + ORACLE + '/" target="_blank" rel="noopener">Oracle</a> itself.</p>');
          return;
        }
        var last = null;
        msgs.forEach(function (m) { last = add(m.speaker || 'Johannes Sigil', render(m.say || '')); });
        if (last && d.retrievals) cha(last, d.retrievals);
        var pair = [{ role: 'user', content: msg }, { role: 'assistant', content: JSON.stringify({ messages: msgs }) }];
        full = full.concat(pair);
        history = history.concat(pair);
        if (history.length > 32) history = history.slice(-32);
        book(full);
      })
      .catch(function () {
        wait.remove();
        add('Johannes Sigil', '<p class="sgw-err">The way to the Oracle is closed for the moment. Try again, or go to the <a href="' + ORACLE + '/" target="_blank" rel="noopener">Oracle</a> itself.</p>');
      })
      .then(function () { sending = false; send.disabled = false; input.focus(); });
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event('submit')); }
  });
})();
