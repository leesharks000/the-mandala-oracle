/* embed/fraction.js — ask Rex Fraction, from spxi.dev and semanticeconomy.org (2026-10-14).
 *
 * The Mandala Oracle's own endpoint (themandalaoracle.com/api/sigil) in mode 'fraction': the same function, archive
 * and installed key as Sigil, with Rex Fraction's voice (rag/fraction-voice.md), his orientation over the whole
 * archive (rag/fraction-weights.json) and his two sites as primary ground (rag/fraction-sites.json). Anonymous,
 * and logged to the Book of Books, as the panel discloses. Built from embed/sigil.js.
 *
 * Usage:  <script src="https://www.themandalaoracle.com/embed/fraction.js" defer></script>
 *         data-accent="#d88860" on the tag sets the site's accent (default: spxi.dev gold, #c9a227).
 */
(function () {
  'use strict';
  if (window.__fractionWidget) return;
  window.__fractionWidget = true;

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
  var TAG = document.currentScript;
  var ACC = (TAG && /^#[0-9a-fA-F]{3,8}$/.test(TAG.getAttribute('data-accent') || '')) ? TAG.getAttribute('data-accent') : '#c9a227';
  var MODE = 'fraction';
  var history = [];
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
    '.fxw-tab{position:fixed!important;right:18px!important;bottom:18px!important;left:auto!important;top:auto!important;z-index:2147483000!important;margin:0!important;font:600 14px/1 -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;',
    'background:#111114;color:#e8e6e3;border:1px solid ' + ACC + ';border-radius:999px;padding:11px 16px;cursor:pointer;',
    'box-shadow:0 4px 18px rgba(0,0,0,.25);letter-spacing:.02em}',
    '.fxw-tab:hover{background:#1e1e24}',
    '.fxw-panel{position:fixed!important;right:18px!important;bottom:18px!important;left:auto!important;top:auto!important;z-index:2147483001!important;margin:0!important;width:min(360px,calc(100vw - 24px));',
    'height:min(500px,calc(100vh - 36px));display:flex;flex-direction:column;background:#0a0a0c;color:#e8e6e3;',
    'border:1px solid ' + ACC + ';border-radius:10px;box-shadow:0 10px 40px rgba(0,0,0,.3);',
    'font:15px/1.55 -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;overflow:hidden}',
    '.fxw-panel[hidden]{display:none}',
    '.fxw-head{display:flex;align-items:baseline;gap:8px;padding:12px 14px 10px;border-bottom:1px solid #1e1e24;background:#111114}',
    '.fxw-face{width:26px;height:26px;border-radius:50%;object-fit:cover;vertical-align:middle;margin:-6px 8px -6px -6px;border:1px solid ' + ACC + ';background:#111}',
    '.fxw-face-l{width:34px;height:34px;margin:-8px 2px -8px 0;align-self:center}',
    '.fxw-head{align-items:center!important}',
    '.fxw-title{font-weight:700;font-variant:small-caps;letter-spacing:.05em;font-size:16px}',
    '.fxw-mode{font:11px/1 var(--mono,Consolas,monospace);color:#8a8a8e;text-transform:uppercase;letter-spacing:.08em}',
    '.fxw-sp{flex:1}',
    '.fxw-head a{font-size:12px;color:' + ACC + '}',
    '.fxw-x{background:none;border:0;font-size:20px;line-height:1;color:#8a8a8e;cursor:pointer;padding:0 0 0 6px}',
    '.fxw-notice{font-size:12.5px;line-height:1.45;color:#8a8a8e;padding:8px 14px;background:#0f0f12;border-bottom:1px solid #1e1e24}',
    '.fxw-consent{margin:8px 14px;padding:10px 12px;border:1px solid currentColor;border-radius:8px;font-size:13px;line-height:1.45}.fxw-consent label{display:block;margin:6px 0}.fxw-consent button{padding:5px 10px;cursor:pointer}',
    '.fxw-notice a{color:' + ACC + '}',
    '.fxw-log{flex:1;overflow-y:auto;padding:12px 14px}',
    '.fxw-msg{margin:0 0 12px}',
    '.fxw-who{font:11px/1 var(--mono,Consolas,monospace);text-transform:uppercase;letter-spacing:.08em;color:' + ACC + ';margin-bottom:4px}',
    '.fxw-you .fxw-body{background:#1e1e24;border-radius:8px;padding:8px 10px}',
    '.fxw-body p{margin:0 0 .55em}.fxw-body p:last-child{margin:0}',
    '.fxw-body a{color:' + ACC + '}',
    '.fxw-body mark{background:rgba(201,162,39,.22);color:inherit;padding:0 2px}',
    '.fxw-cha{font-size:12.5px;margin-top:6px}.fxw-cha summary{cursor:pointer;color:#8a8a8e}',
    '.fxw-cha ul{margin:4px 0 0;padding-left:18px}.fxw-cha a{color:' + ACC + '}',
    '.fxw-err{color:' + ACC + ';font-style:italic}',
    '.fxw-form{display:flex;gap:8px;padding:10px 12px;border-top:1px solid #1e1e24;background:#111114}',
    '.fxw-in{flex:1;resize:none;height:44px;font:inherit;font-size:14.5px;padding:8px 10px;border:1px solid #2a2a32;border-radius:6px;background:#0a0a0c;color:#e8e6e3}',
    '.fxw-send{font:600 14px/1 -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif;background:' + ACC + ';color:#0a0a0c;border:0;border-radius:6px;padding:0 14px;cursor:pointer}',
    '.fxw-send[disabled]{opacity:.5;cursor:default}',
    '.fxw-foot{font-size:12px;color:#8a8a8e;padding:6px 14px 10px;background:#111114;text-align:center}',
    '.fxw-foot a{color:' + ACC + '}'
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
      var drop = c.querySelectorAll('nav,script,style,noscript,template,svg,.fxw-tab,.fxw-panel,[aria-hidden="true"]');
      for (var i = 0; i < drop.length; i++) drop[i].parentNode && drop[i].parentNode.removeChild(drop[i]);
      var text = (c.textContent || '').replace(/\s+/g, ' ').trim();
      var parts = [];
      if (h1) parts.push('Heading: ' + h1.textContent.replace(/\s+/g, ' ').trim());
      if (md && md.content) parts.push('Description: ' + md.content.trim());
      parts.push(text);
      return parts.join('\n').slice(0, 1800);
    } catch (e) { return ''; }
  }

  var style = el('style'); style.textContent = css; document.head.appendChild(style);
  var FACE = ORACLE + '/embed/fraction-face.webp';
  var tab = el('button', 'fxw-tab ink-skip', '<img class="fxw-face" src="' + FACE + '" alt="">Ask Rex Fraction');
  tab.type = 'button';
  tab.setAttribute('aria-controls', 'fxw-panel');
  var panel = el('section', 'fxw-panel ink-skip');
  panel.id = 'fxw-panel'; panel.hidden = true;
  panel.setAttribute('aria-label', 'Conversation with Rex Fraction');
  panel.innerHTML =
    '<div class="fxw-head"><img class="fxw-face fxw-face-l" src="' + FACE + '" alt="Rex Fraction"><span class="fxw-title">Rex Fraction</span><span class="fxw-mode">SEI</span>' +
    '<span class="fxw-sp"></span><a href="https://www.spxi.dev/who/fraction" target="_blank" rel="noopener">who ↗</a>' +
    '<button type="button" class="fxw-x" aria-label="Close">×</button></div>' +
    '<div class="fxw-notice">Anonymous; logged publicly to the <a href="https://www.alexanarch.org/book/" target="_blank" rel="noopener">Book of Books</a>. ' +
    'A heteronym of Lee Sharks. Engagements: <a href="mailto:rexfraction@gmail.com">rexfraction@gmail.com</a></div>' +
    '<div class="fxw-log" aria-live="polite"></div>' +
    '<form class="fxw-form"><textarea class="fxw-in" placeholder="Ask about SPXI, an audit, or what AI says about your entity." aria-label="Your message"></textarea>' +
    '<button type="submit" class="fxw-send">Send</button></form>' +
    '<div class="fxw-foot">Semantic Economy Institute · <a href="https://www.spxi.dev/" target="_blank" rel="noopener">spxi.dev</a> · <a href="https://www.semanticeconomy.org/" target="_blank" rel="noopener">semanticeconomy.org</a></div>';
  document.body.appendChild(tab);
  document.body.appendChild(panel);

  var log = panel.querySelector('.fxw-log');
  var form = panel.querySelector('.fxw-form');
  var input = panel.querySelector('.fxw-in');
  var send = panel.querySelector('.fxw-send');

  function open() { panel.hidden = false; tab.hidden = true; input.focus(); }
  function close() { panel.hidden = true; tab.hidden = false; tab.focus(); }
  tab.addEventListener('click', open);
  panel.querySelector('.fxw-x').addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) close(); });

  function add(who, html, cls) {
    var m = el('div', 'fxw-msg' + (cls ? ' ' + cls : ''));
    m.appendChild(el('div', 'fxw-who', esc(who)));
    var b = el('div', 'fxw-body', html);
    m.appendChild(b);
    log.appendChild(m);
    log.scrollTop = log.scrollHeight;
    return m;
  }
  function cha(msgEl, retrievals) {
    var seen = {}, items = [];
    (retrievals || []).forEach(function (r) {
      if (!r) return;
      var key = r.axn || r.url; if (!key || seen[key]) return; seen[key] = 1;
      if (r.url && !r.axn) {
        items.push('<li><a href="' + esc(r.url) + '" target="_blank" rel="noopener noreferrer">' + esc(r.title || r.url) + '</a></li>');
        return;
      }
      var label = esc((r.deposit_number ? '#' + r.deposit_number + ' ' : '') + (r.title || '(no title)'));
      items.push('<li>' + (r.deposit_number
        ? '<a href="https://www.alexanarch.org/s/records/' + r.deposit_number + '/" target="_blank" rel="noopener noreferrer">' + label + '</a>'
        : label) + '</li>');
    });
    if (!items.length) return;
    msgEl.appendChild(el('details', 'fxw-cha', '<summary>what I read (' + items.length + ')</summary><ul>' + items.join('') + '</ul>'));
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
      .then(function (d) { if (d && d.axn && !session.axn) session.axn = d.axn; })
      .catch(function () {});
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var msg = input.value.trim();
    if (!msg || sending) return;
    if (!currentConsent()) {
      if (log.querySelector('.fxw-consent')) return;
      var box = document.createElement('div'); box.className = 'fxw-consent';
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
    add('you', render(msg), 'fxw-you');
    book(history.concat([{ role: 'user', content: msg }]));
    var wait = add('Rex Fraction', '<p><em>…</em></p>');
    fetch(ORACLE + '/api/sigil', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg, history: history, mode: MODE, page: pageContext(), consent: currentConsent() })
    })
      .then(function (r) { return r.json().catch(function () { return { error: 'HTTP ' + r.status }; }).then(function (d) { d.__ok = r.ok; return d; }); })
      .then(function (d) {
        wait.remove();
        var msgs = Array.isArray(d.messages) ? d.messages : [];
        if (!d.__ok || !msgs.length) {
          add('Rex Fraction', '<p class="fxw-err">No answer this time. Try again shortly, or write to <a href="mailto:rexfraction@gmail.com">rexfraction@gmail.com</a>.</p>');
          return;
        }
        var last = null;
        msgs.forEach(function (m) { last = add('Rex Fraction', render(m.say || '')); });
        if (last && d.retrievals) cha(last, d.retrievals);
        history.push({ role: 'user', content: msg });
        history.push({ role: 'assistant', content: JSON.stringify({ messages: msgs }) });
        if (history.length > 16) history = history.slice(-16);
        book(history);
      })
      .catch(function () {
        wait.remove();
        add('Rex Fraction', '<p class="fxw-err">The connection failed. Try again, or write to <a href="mailto:rexfraction@gmail.com">rexfraction@gmail.com</a>.</p>');
      })
      .then(function () { sending = false; send.disabled = false; input.focus(); });
  });
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event('submit')); }
  });
})();
