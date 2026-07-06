// ═══ DEPENDENCIES (INSTANCE-PROTOCOL.md — read before editing) ═══════════
// PROVIDES: the rotation loop, all rite affordances, transform/halt cards.
// CALLS: /api/sigil, /api/transform (judgment, judgment/operator, cast,
//   rite_append), /api/share, /api/book.
// CONTRACTS: consumes transform.py's response fields (result, halt_diagnosis,
//   skeleton, post_mortem, transform{independent_verification, advisories,
//   glyphic, law_variance}, geometry_check) — extend both ends together.
// MUST-READ-BEFORE-EDITING: this header; api/transform.py do_POST; the
//   rotation loop in full (not the grep line — the loop).
// ═════════════════════════════════════════════════════════════════════════

// chat.js — wires the chat panel to /api/sigil.
//
// API returns: { messages: [{speaker, say, navigate?}, ...], retrievals: [...] }
// Each message renders as its own bubble with a per-heteronym role label.
// When Sigil yields, the response contains two messages: his brief
// acknowledgment, then the other heteronym's response.

const messagesEl = document.getElementById('messages');
const formEl = document.getElementById('chat-form');
const inputEl = document.getElementById('message-input');
const sendBtn = document.getElementById('send-button');
const statusEl = document.getElementById('status');
const modeBtns = document.querySelectorAll('.mode-button');
const settingsToggle = document.getElementById('settings-toggle');
const settingsPanel = document.getElementById('settings-panel');
const castToggle = document.getElementById('cast-toggle');
const castPanel = document.getElementById('cast-panel');

// apiKeyEl is lazy — the settings panel content is injected on first
// open, not present in the initial DOM. Access via getApiKey() instead.
let apiKeyEl = null;

let mode = 'sabbath';
let history = [];  // [{role: 'user'|'assistant', content: str}, ...]
let isSending = false;
let emptyStateRemoved = false;

// Book-of-conversations session state (B-A4: per-session AXN, stable from first turn).
// session_id is client-generated; hashed server-side; never stored raw.
const sessionState = {
  session_id: (crypto && crypto.randomUUID) ? crypto.randomUUID() : `s-${Date.now()}-${Math.random().toString(36).slice(2)}`,
  started_at: new Date().toISOString(),
  axn: null,           // set on first successful book append
  appendingEnabled: true,  // set false after a 503 response so we stop trying
};

// Heteronym → CSS class slug
const SPEAKER_CLASS = {
  'Lee Sharks':       'sharks',
  'Johannes Sigil':   'sigil',
  'Rex Fraction':     'fraction',
  'Damascus Dancings':'dancings',
  'Rebekah Cranes':   'cranes',
  'Talos Morrow':     'morrow',
  'Ichabod Spellings':'spellings',
  'Sparrow Wells':    'wells',
  'Nobel Glas':       'glas',
  'Dr. Orin Trace':   'trace',
  'Rev. Ayanna Vox':  'vox',
  'Sen Kuro':         'kuro',
  'Jack Feist':       'feist',
};

// ─────────────────────────────────────────────────────────────────────────
// Mode toggle
// ─────────────────────────────────────────────────────────────────────────

modeBtns.forEach((btn) => {
  btn.addEventListener('click', () => {
    const next = btn.dataset.mode;
    if (next === mode || isSending) return;
    mode = next;
    modeBtns.forEach((b) => {
      const active = b.dataset.mode === mode;
      b.classList.toggle('active', active);
      b.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    if (window.sky?.setMode) window.sky.setMode(mode);
    if (castToggle) castToggle.hidden = mode !== 'merkabah';
    setStatus(`Mode: ${mode}.`);
  });
});

// ─────────────────────────────────────────────────────────────────────────
// Settings panel — content is injected on first open, not present in
// initial HTML. This way, the Anthropic API Key heading and the sk-ant-
// input cannot leak through any transparency or stale CSS state, because
// the elements literally do not exist in the DOM until the user clicks ⚙.
// ─────────────────────────────────────────────────────────────────────────

let settingsContentInjected = false;

function ensureSettingsContent() {
  if (settingsContentInjected) return;
  settingsPanel.innerHTML = `
    <button class="settings-close" type="button" aria-label="Close settings">×</button>
    <h3>Anthropic API Key</h3>
    <p class="key-note">
      Bring your own Anthropic key. It is sent over TLS to the Sigil endpoint, used for the
      single call each turn, and discarded — never stored, never logged, never written to disk.
    </p>
    <input type="password" id="api-key-input" placeholder="sk-ant-..." autocomplete="off" spellcheck="false">
    <p class="key-note">Leave blank to use the installed demo key (rate-limited).</p>
  `;
  apiKeyEl = settingsPanel.querySelector('#api-key-input');
  const settingsClose = settingsPanel.querySelector('.settings-close');
  settingsClose.addEventListener('click', closeSettings);
  settingsContentInjected = true;
}

function openSettings() {
  ensureSettingsContent();
  settingsPanel.classList.add('open');
  settingsPanel.removeAttribute('hidden');
  settingsPanel.setAttribute('aria-hidden', 'false');
  settingsToggle.setAttribute('aria-expanded', 'true');
  apiKeyEl.focus();
}

function closeSettings() {
  settingsPanel.classList.remove('open');
  settingsPanel.setAttribute('hidden', '');
  settingsPanel.setAttribute('aria-hidden', 'true');
  settingsToggle.setAttribute('aria-expanded', 'false');
}

settingsToggle.addEventListener('click', () => {
  if (settingsPanel.classList.contains('open')) {
    closeSettings();
  } else {
    openSettings();
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && settingsPanel.classList.contains('open')) {
    closeSettings();
  }
});

// ─────────────────────────────────────────────────────────────────────────
// Sky readiness
// ─────────────────────────────────────────────────────────────────────────

// Status: check sky.ready flag synchronously (since sky.js's dispatchEvent
// fires during its own initialization, BEFORE chat.js loads — module
// scripts are deferred and ordered, so the event is missed by the time we
// attach a listener). Also attach listener for any future re-fire.
if (window.sky?.ready) {
  setStatus('Ready.');
}
window.addEventListener('sky-ready', () => {
  setStatus('Ready.');
});

// ─────────────────────────────────────────────────────────────────────────
// Submit handler
// ─────────────────────────────────────────────────────────────────────────

formEl.addEventListener('submit', async (e) => {
  e.preventDefault();
  if (isSending) return;

  const message = inputEl.value.trim();
  if (!message) return;

  const apiKey = apiKeyEl ? (apiKeyEl.value.trim() || null) : null;

  removeEmptyState();
  appendUserMessage(message);
  inputEl.value = '';
  inputEl.style.height = 'auto';

  isSending = true;
  sendBtn.disabled = true;
  setStatus('Sigil is reading...');

  const placeholder = appendHeteronymMessage('Johannes Sigil', '…', { dim: true });

  // Capture the witness's message to the Book BEFORE attempting Sigil.
  // This guarantees the user's words are preserved even when Sigil fails —
  // missing API key, server error, network failure, page-close mid-call.
  // Earlier behavior only captured on success, so any conversation that
  // hit an error (e.g. a fresh device with no API key configured)
  // disappeared entirely, words and all. Fire-and-forget; non-fatal.
  const historyWithUser = [...history, { role: 'user', content: message }];
  if (sessionState.appendingEnabled) {
    bookAppend(historyWithUser).catch(() => { /* swallow; non-fatal */ });
  }

  try {
    const res = await fetch('/api/sigil', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        history,
        mode,
        anthropic_key: apiKey,
      }),
    });

    if (!res.ok) {
      const body = await res.json().catch(() => ({ error: `HTTP ${res.status}` }));
      placeholder.remove();
      appendErrorMessage(body.error || `Request failed: ${res.status}`);
      setStatus('Error.');
      // Sigil errored — the user message is already in the Book from the
      // pre-call append above. Nothing further to record.
      return;
    }

    const data = await res.json();
    placeholder.remove();

    const respMessages = Array.isArray(data.messages) ? data.messages : [];
    if (respMessages.length === 0) {
      appendErrorMessage('Empty response from Sigil endpoint.');
      setStatus('Error.');
      return;
    }

    // Render each message in sequence, attaching retrievals to the last one only
    let lastEl = null;
    let lastNavigate = null;
    let lastCast = null;
    for (let i = 0; i < respMessages.length; i++) {
      const m = respMessages[i];
      const speaker = m.speaker || 'Johannes Sigil';
      const say = m.say || '';
      lastEl = appendHeteronymMessage(speaker, say);
      if (m.navigate) lastNavigate = m.navigate;
      if (m.cast) lastCast = m.cast;
    }
    if (lastEl && data.retrievals && data.retrievals.length) {
      appendRetrievals(lastEl, data.retrievals);
    }

    // Update history: store the user turn and the assistant's full multi-message
    // turn as a single JSON-stringified content, so the model sees its own
    // structured output on subsequent turns.
    history.push({ role: 'user', content: message });
    history.push({
      role: 'assistant',
      content: JSON.stringify({ messages: respMessages }),
    });
    if (history.length > 32) history = history.slice(-32);

    // Sigil succeeded — append the assistant's response to the Book.
    // This is a second call after the user-only capture above; the server
    // upserts the conversation file, so the latest version wins. On a
    // brief race with the first call, the second will retry-able-fail at
    // worst (server is SHA-conditional); the witness's user message is
    // already preserved either way.
    if (sessionState.appendingEnabled) {
      bookAppend(history).catch(() => { /* swallow; non-fatal */ });
    }

    // Cast directive: Sigil hands the rite to the compiler — open the panel
    // prefilled; the witness confirms inscription and casts. (The compiler
    // boundary: Sigil may open the rite but never perform it.)
    if (mode === 'merkabah' && lastCast) {
      openCastPanelPrefilled(lastCast);
    }

    // Navigation: only in Merkabah mode, using the last directive in the response
    if (mode === 'merkabah' && lastNavigate && window.sky?.navigate) {
      const ok = window.sky.navigate(lastNavigate);
      setStatus(ok ? `Navigating: ${lastNavigate.directive}.` : 'A navigation was offered but could not be resolved.');
    } else {
      setStatus('Ready.');
    }
  } catch (err) {
    placeholder.remove();
    appendErrorMessage(`Connection error: ${err.message}`);
    setStatus('Error.');
  } finally {
    isSending = false;
    sendBtn.disabled = false;
    inputEl.focus();
  }
});

// Submit on Cmd/Ctrl+Enter
inputEl.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
    e.preventDefault();
    formEl.requestSubmit();
  }
});

// Auto-grow textarea
inputEl.addEventListener('input', () => {
  inputEl.style.height = 'auto';
  inputEl.style.height = Math.min(inputEl.scrollHeight, 280) + 'px';
});

// ─────────────────────────────────────────────────────────────────────────
// Render helpers
// ─────────────────────────────────────────────────────────────────────────

function removeEmptyState() {
  if (emptyStateRemoved) return;
  const empty = messagesEl.querySelector('.empty-state');
  if (empty) empty.remove();
  emptyStateRemoved = true;
}

function appendUserMessage(content) {
  const wrap = document.createElement('div');
  wrap.className = 'message user';
  const roleLabel = document.createElement('div');
  roleLabel.className = 'message-role';
  roleLabel.textContent = 'You';
  const contentEl = document.createElement('div');
  contentEl.className = 'message-content';
  contentEl.textContent = content;
  wrap.appendChild(roleLabel);
  wrap.appendChild(contentEl);
  messagesEl.appendChild(wrap);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return wrap;
}

function appendHeteronymMessage(speaker, content, opts = {}) {
  const wrap = document.createElement('div');
  const classSlug = SPEAKER_CLASS[speaker] || 'sigil';
  wrap.className = `message heteronym ${classSlug}`;
  const roleLabel = document.createElement('div');
  roleLabel.className = 'message-role';
  roleLabel.textContent = speaker;
  const contentEl = document.createElement('div');
  contentEl.className = 'message-content';
  contentEl.textContent = content;
  if (opts.dim) contentEl.style.opacity = '0.5';
  wrap.appendChild(roleLabel);
  wrap.appendChild(contentEl);
  messagesEl.appendChild(wrap);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return wrap;
}

function appendErrorMessage(content) {
  const wrap = document.createElement('div');
  wrap.className = 'message error';
  const roleLabel = document.createElement('div');
  roleLabel.className = 'message-role';
  roleLabel.textContent = 'Error';
  const contentEl = document.createElement('div');
  contentEl.className = 'message-content';
  contentEl.textContent = content;
  wrap.appendChild(roleLabel);
  wrap.appendChild(contentEl);
  messagesEl.appendChild(wrap);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return wrap;
}

function appendRetrievals(messageEl, retrievals) {
  if (!retrievals.length) return;
  const seen = new Set();
  const unique = retrievals.filter((r) => {
    if (seen.has(r.axn)) return false;
    seen.add(r.axn);
    return true;
  });
  const details = document.createElement('details');
  details.className = 'message-retrievals';
  const summary = document.createElement('summary');
  summary.textContent = `Cha — what stood beneath this reading (${unique.length})`;
  details.appendChild(summary);
  const ul = document.createElement('ul');
  for (const r of unique) {
    const li = document.createElement('li');
    const label = `${r.axn.split('.').slice(0, 2).join('.')} — ${r.title || '(no title)'}`;
    if (r.deposit_number) {
      // Deep link to the deposit's record page on alexanarch. Opens in a new tab
      // so the descent isn't interrupted; the witness can return to the conversation.
      const a = document.createElement('a');
      a.href = `https://www.alexanarch.org/s/records/${r.deposit_number}/`;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.textContent = label;
      li.appendChild(a);
    } else {
      // No deposit_number available (older metadata or unindexed source) — render as plain text.
      li.textContent = label;
    }
    ul.appendChild(li);
  }
  details.appendChild(ul);
  messageEl.appendChild(details);
}

function setStatus(text) {
  statusEl.textContent = text;
}

// ──────────────────────────────────────────────────────────────────────
// Book append — POSTs conversation state to /api/book/append.
// Per B-A4: one AXN per session, set on the first successful append, stable
// thereafter. The endpoint upserts the conversation file in book/data/.
// Failures are non-fatal; on persistent 503 (server lacks GITHUB_BOOK_TOKEN),
// we mark appendingEnabled=false to stop trying for the rest of this session.
// ──────────────────────────────────────────────────────────────────────
async function bookAppend(currentHistory) {
  const payload = {
    session_id: sessionState.session_id,
    started_at: sessionState.started_at,
    mode,
    history: currentHistory,
  };
  if (sessionState.axn) payload.axn = sessionState.axn;

  const res = await fetch('/api/book', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (res.status === 503) {
    sessionState.appendingEnabled = false;
    return;
  }
  if (!res.ok) return;
  const data = await res.json();
  if (data.axn && !sessionState.axn) {
    sessionState.axn = data.axn;
  }
}

// ─────────────────────────────────────────────────────────────────────────
// THE CASTING RITE — Layer 4 of IMPLEMENTATION-WORKPLAN-transforms-merkabah.
//
// Sigil opens → Cranes transforms (the compiler, /api/transform) → Feist
// judges → Sharks seals. Per EA-MANDALA-KERNEL-TRANSFORM-01 v0.2 §3.7 the
// compiler halts with diagnosis rather than emitting a failed draft; the
// witness is offered ONE re-unfold; refusal (or a second halt) results in
// sweep. Inscription per EA-MANDALA-INSCRIPTION-01 v0.1: public (default),
// encrypted (key shown once, never stored), or none.
// ─────────────────────────────────────────────────────────────────────────

let castMeta = null;          // GET /api/transform bootstrap (sources, operators)
let castContentBuilt = false;
let lastReading = null;       // { axn, mode } — enables rotation continuation

async function fetchCastMeta() {
  if (castMeta) return castMeta;
  const res = await fetch('/api/transform');
  if (!res.ok) throw new Error(`cast bootstrap failed: HTTP ${res.status}`);
  castMeta = await res.json();
  return castMeta;
}

function ensureCastContent() {
  if (castContentBuilt) return;
  castContentBuilt = true;
  castPanel.innerHTML = `
    <label for="cast-source">Source — the canon text to be cast</label>
    <select id="cast-source"></select>
    <div class="cast-hint" id="cast-source-hint"></div>

    <div id="cast-reader-block" style="display:none;">
      <label for="cast-reader-text">Your text — the source of this cast</label>
      <textarea id="cast-reader-text" maxlength="1000" placeholder="Offer the words to be cast — 40 to 1,000 characters, strictly. Used for this cast only: never stored, never inscribed; only a hash prefix can ever appear in any record. The transform derives from your words; choose the inscription mode accordingly."></textarea>
      <div class="cast-hint" id="cast-reader-count" style="text-align:right;">0 / 1,000</div>
      <div class="cast-hint">Reader-supplied source. Inscription defaults to <em>None</em>; choose Public only if you are content for the <em>transform</em> (not your text) to enter the Book.</div>
    </div>

    <label for="cast-operator">Operator — the axis the compiler traverses</label>
    <select id="cast-operator"></select>
    <div class="cast-hint" id="cast-operator-hint"></div>

    <label for="cast-selection">Selection — leave empty and the rite selects the verses</label>
    <input type="text" id="cast-selection" placeholder="empty = oracular selection · or name it: stanzas_1_4 · chapter_1 · units_12_15"
           style="width:100%; background:rgba(255,255,255,.06); color:inherit; border:1px solid rgba(255,255,255,.2); border-radius:4px; padding:6px 8px; font:inherit;">
    <div class="cast-hint">Left empty, the verses are drawn at random across the whole source and weighed against your question — repeated casts will not cluster on the famous passages. Name a selection only when you have one.</div>

    <label for="cast-inscription">Inscription</label>
    <select id="cast-inscription">
      <option value="public" selected>Public — anonymous, appended to the Book</option>
      <option value="encrypted">Encrypted — form public, meaning sealed; key shown once</option>
      <option value="none">None — returned to you only, nothing inscribed</option>
    </select>
    <div class="cast-hint" id="cast-inscription-hint"></div>

    <div id="cast-continue-row" style="display:none; margin-top:8px;">
      <label style="display:inline; text-transform:none; letter-spacing:0;">
        <input type="checkbox" id="cast-continue"> Cast into the current reading (continue its rotation)
      </label>
    </div>

    <label for="cast-question">The invoking question (optional; sealed or digested — never inscribed raw in public)</label>
    <textarea id="cast-question" placeholder="What do you bring to the casting?"></textarea>

    <div class="cast-actions">
      <button type="button" class="cast-close">Close</button>
      <button type="button" class="cast-go">Cast</button>
    </div>
  `;

  const srcSel = castPanel.querySelector('#cast-source');
  const opSel = castPanel.querySelector('#cast-operator');
  const inscSel = castPanel.querySelector('#cast-inscription');
  const inscHint = castPanel.querySelector('#cast-inscription-hint');
  const srcHint = castPanel.querySelector('#cast-source-hint');
  const opHint = castPanel.querySelector('#cast-operator-hint');

  const INSC_HINTS = {
    public: 'Your question is inscribed as a digest and a composed gloss — never as your raw words. The transform itself enters the public Book.',
    encrypted: 'The record splits at the compiler\u2019s own boundary: the formal skeleton is public; the question, the enantiomorph, and the interpretations are sealed. The key is shown ONCE and stored nowhere. Loss of the key is permanent illegibility.',
    none: 'The transform returns to you in this session only. The Book receives nothing.',
  };
  const setInscHint = () => {
    inscHint.textContent = INSC_HINTS[inscSel.value];
    updateContinueRow();
  };
  inscSel.addEventListener('change', setInscHint);

  function updateContinueRow() {
    const row = castPanel.querySelector('#cast-continue-row');
    const show = !!(lastReading && lastReading.mode === inscSel.value && inscSel.value !== 'none');
    row.style.display = show ? 'block' : 'none';
    if (!show) castPanel.querySelector('#cast-continue').checked = false;
  }

  fetchCastMeta().then((meta) => {
    for (const s of meta.sources) {
      const o = document.createElement('option');
      o.value = s.id;
      o.textContent = s.title + (s.creator ? ` — ${s.creator}` : '');
      if (s.admissible === false) {
        o.disabled = true;
        o.textContent += ' (image-canonical — inadmissible)';
        o.title = s.reason || '';
      }
      srcSel.appendChild(o);
    }
    {
      const r = document.createElement('option');
      r.value = '__reader__';
      r.textContent = '— Paste your own text (your words as the source) —';
      srcSel.appendChild(r);
    }
    srcHint.textContent = `${meta.sources.filter(s => s.admissible !== false).length} sources admissible under sources/CLASSIFICATION.md.`;
    const readerBlock = castPanel.querySelector('#cast-reader-block');
    const readerTa = castPanel.querySelector('#cast-reader-text');
    const readerCount = castPanel.querySelector('#cast-reader-count');
    readerTa.addEventListener('input', () => {
      const n = readerTa.value.length;
      readerCount.textContent = `${n.toLocaleString()} / 1,000`;
      readerCount.style.color = n > 950 ? '#e8a074' : '';
    });
    const syncReaderUI = () => {
      const isReader = srcSel.value === '__reader__';
      readerBlock.style.display = isReader ? 'block' : 'none';
      castPanel.querySelector('#cast-selection').disabled = isReader;
      srcHint.textContent = isReader
        ? 'Your words become the source — 40 to 1,000 characters, strictly. Never stored or inscribed; hash prefix only.'
        : `${meta.sources.filter(s => s.admissible !== false).length} sources admissible under sources/CLASSIFICATION.md.`;
    };
    srcSel.addEventListener('change', syncReaderUI);
    syncReaderUI();
    const oj = document.createElement('option');
    oj.value = '';
    oj.textContent = '— let the Judgment choose —';
    opSel.appendChild(oj);
    for (const [name, axis] of Object.entries(meta.operators)) {
      const o = document.createElement('option');
      o.value = name;
      o.textContent = name;
      o.title = axis;
      opSel.appendChild(o);
    }
    const setOpHint = () => { opHint.textContent = meta.operators[opSel.value] || 'The invisible ninth operator selects — and, on continuation, sequences the rotation.'; };
    opSel.addEventListener('change', setOpHint);
    setOpHint();
    setInscHint();
  }).catch((e) => {
    const o = document.createElement('option');
    o.disabled = true;
    o.selected = true;
    o.textContent = '— sources unavailable —';
    srcSel.appendChild(o);
    srcHint.textContent = `Could not load the cast bootstrap: ${e.message}. ` +
      'If this persists, the deployment may be missing sources/** in the function bundle.';
  });

  castPanel.querySelector('.cast-close').addEventListener('click', closeCastPanel);
  castPanel.querySelector('.cast-go').addEventListener('click', () => {
    const source = srcSel.selectedOptions[0];
    if (!source || source.disabled) return;
    const cast = {
      sourceId: srcSel.value,
      sourceTitle: source.textContent,
      operator: opSel.value,
      opAxis: castMeta.operators[opSel.value] || '',
      castSelection: (srcSel.value === '__reader__' ? null : (castPanel.querySelector('#cast-selection').value.trim() || null)),
      readerText: (srcSel.value === '__reader__' ? castPanel.querySelector('#cast-reader-text').value : null),
      inscriptionMode: inscSel.value,
      question: castPanel.querySelector('#cast-question').value.trim(),
      continueReading: castPanel.querySelector('#cast-continue').checked,
    };
    closeCastPanel();
    runCastingRite(cast);
  });
}

async function openCastPanelPrefilled(directive) {
  openCastPanel();
  try { await fetchCastMeta(); } catch { return; }
  const srcSel = castPanel.querySelector('#cast-source');
  const opSel = castPanel.querySelector('#cast-operator');
  const q = castPanel.querySelector('#cast-question');
  if (directive.source_text_id && srcSel) {
    const opt = Array.from(srcSel.options).find((o) => o.value === directive.source_text_id);
    if (opt && !opt.disabled) srcSel.value = directive.source_text_id;
  }
  if (directive.operator && opSel) {
    const op = String(directive.operator).toUpperCase();
    if (Array.from(opSel.options).some((o) => o.value === op)) {
      opSel.value = op;
      opSel.dispatchEvent(new Event('change'));
    }
  }
  if (directive.cast_selection) {
    const selEl = castPanel.querySelector('#cast-selection');
    if (selEl && !selEl.value) selEl.value = directive.cast_selection;
  }
  if (directive.question && q && !q.value) q.value = directive.question;
  setStatus('The compiler awaits — confirm the cast.');
}

function openCastPanel() {
  ensureCastContent();
  castPanel.hidden = false;
  castPanel.setAttribute('aria-hidden', 'false');
  castPanel.classList.add('open');
  castToggle.setAttribute('aria-expanded', 'true');
  const row = castPanel.querySelector('#cast-continue-row');
  if (row) {
    const inscSel = castPanel.querySelector('#cast-inscription');
    const show = !!(lastReading && lastReading.mode === inscSel.value && inscSel.value !== 'none');
    row.style.display = show ? 'block' : 'none';
  }
}

function closeCastPanel() {
  castPanel.classList.remove('open');
  castPanel.hidden = true;
  castPanel.setAttribute('aria-hidden', 'true');
  castToggle.setAttribute('aria-expanded', 'false');
}

if (castToggle) {
  castToggle.addEventListener('click', () => {
    if (castPanel.classList.contains('open')) closeCastPanel();
    else openCastPanel();
  });
}

// ── Rite helpers ─────────────────────────────────────────────────────────

function riteMarker(text) {
  const el = document.createElement('div');
  el.className = 'rite-marker';
  el.textContent = text;
  messagesEl.appendChild(el);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}


async function riteInscribe(readingAxn, stage, speaker, text, operator) {
  // The voices are not left to a closed tab: awaited server-side inscription
  // into the reading record. Failures surface but do not break the rite.
  if (!readingAxn) return;
  try {
    const res = await fetch('/api/transform', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'rite_append', reading_axn: readingAxn,
                             stage, speaker, text, operator: operator || null }),
    });
    if (!res.ok) setStatus(`(${stage} not inscribed — record remains partial)`);
  } catch { /* transform record already holds the enantiomorphs */ }
}

async function sigilStage(directive, statusText, riteReasoning = false) {
  // One voice-stage of the rite: POST the directive to /api/sigil, render the
  // returned voices, fold both sides into history (the Book's conversation
  // record preserves the rite verbatim; the readings book is inscribed
  // separately, PASS-gated, by /api/transform).
  setStatus(statusText);
  const apiKeyEl2 = document.getElementById('api-key');
  const apiKey = apiKeyEl2 ? (apiKeyEl2.value.trim() || null) : null;
  const res = await fetch('/api/sigil', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: directive, history, mode, anthropic_key: apiKey, rite_reasoning: riteReasoning }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({ error: `HTTP ${res.status}` }));
    throw new Error(body.error || `stage failed: ${res.status}`);
  }
  const data = await res.json();
  const respMessages = Array.isArray(data.messages) ? data.messages : [];
  for (const m of respMessages) {
    appendHeteronymMessage(m.speaker || 'Johannes Sigil', m.say || '');
  }
  history.push({ role: 'user', content: directive });
  history.push({ role: 'assistant', content: JSON.stringify({ messages: respMessages }) });
  if (history.length > 32) history = history.slice(-32);
  if (sessionState.appendingEnabled) bookAppend(history).catch(() => {});
  return respMessages;
}

function offerChoice(labels) {
  // Render inline buttons; resolve with the chosen label. Used for the
  // §3.7 re-unfold offer.
  return new Promise((resolve) => {
    const wrap = document.createElement('div');
    wrap.className = 'rite-choice';
    for (const label of labels) {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = label;
      b.addEventListener('click', () => {
        wrap.querySelectorAll('button').forEach((x) => { x.disabled = true; });
        wrap.remove();
        resolve(label);
      });
      wrap.appendChild(b);
    }
    messagesEl.appendChild(wrap);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  });
}


// Alchemical sigils for the eight rotating operators (SHADOW originary).
const OPERATOR_SIGILS = {
  SHADOW: '\u2644',    // ♄ Saturn — lead, the nigredo, the bearing
  MIRROR: '\u263D',    // ☽ Luna — silver, reflection
  INVERSION: '\u263F', // ☿ Mercury — the volatile reversal
  FLAME: '\u{1F702}',  // 🜂 fire
  BRIDE: '\u2640',     // ♀ Venus — copper, consecration
  BEAST: '\u{1F70D}',  // 🜍 sulphur — the animal soul
  THUNDER: '\u2643',   // ♃ Jupiter — the sky-thunderer
  SILENCE: '\u{1F714}',// 🜔 salt — fixity, stillness
};

function renderOperatorLabel(op, axis) {
  const el = document.createElement('div');
  el.className = 'operator-label';
  const sig = OPERATOR_SIGILS[op] || '\u2609';
  el.innerHTML = `<span class="op-sigil">${sig}</span> <span class="op-name">${op}</span>` +
    (axis ? ` <span class="op-axis">— ${axis.split(' — ')[0]}</span>` : '');
  messagesEl.appendChild(el);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return el;
}


// Language of the source, from its id suffix (MANUS, 2026-07-06): -greek,
// -latin, -hebrew mean the source card shows passage + facing translation;
// anything else is English and the facing is a duplicate.
function _sourceLanguage(sourceId) {
  if (!sourceId || typeof sourceId !== 'string') return 'en';
  const s = sourceId.toLowerCase();
  if (s.endsWith('-greek') || s.includes('-greek-')) return 'grc';
  if (s.endsWith('-latin') || s.includes('-latin-')) return 'lat';
  if (s.endsWith('-hebrew') || s.includes('-hebrew-')) return 'heb';
  return 'en';
}

// Very small markdown-blockquote renderer for English source cards: lines
// beginning with "> " become an indented left-ruled block; blank lines inside
// a blockquote are kept as gaps. Applied ONLY to English sources whose
// canonical text uses markdown structure (Cranes's Day and Night, the Secret
// Book of Walt, Whitman). Greek/Latin/Hebrew sources use plain pre-wrap.
function _renderPassageInto(container, text) {
  container.innerHTML = '';
  container.style.whiteSpace = 'normal';
  const lines = String(text || '').split('\n');
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const bqMatch = line.match(/^\s*>\s?(.*)$/);
    if (bqMatch) {
      const bqLines = [];
      while (i < lines.length) {
        const m = lines[i].match(/^\s*>\s?(.*)$/);
        if (m) { bqLines.push(m[1]); i++; }
        else if (lines[i].trim() === '' && (i+1 < lines.length) &&
                 /^\s*>\s?/.test(lines[i+1])) { bqLines.push(''); i++; }
        else break;
      }
      const bq = document.createElement('div');
      bq.style.borderLeft = '2px solid rgba(255,255,255,.18)';
      bq.style.paddingLeft = '12px';
      bq.style.marginLeft = '4px';
      bq.style.marginTop = '4px';
      bq.style.marginBottom = '4px';
      bq.style.whiteSpace = 'pre-wrap';
      bq.textContent = bqLines.join('\n');
      container.appendChild(bq);
    } else {
      const span = document.createElement('div');
      span.style.whiteSpace = 'pre-wrap';
      span.textContent = line;
      container.appendChild(span);
      i++;
    }
  }
}

function renderSourceCard(citation, passage, attribution, translation, sourceId) {
  const card = document.createElement('div');
  card.className = 'source-card';
  const label = document.createElement('div');
  label.style.opacity = '.6';
  label.style.fontSize = '.8em';
  label.style.letterSpacing = '.08em';
  label.style.marginBottom = '6px';
  label.textContent = `— the cast text${arguments[2] ? ' · ' + arguments[2] : ''}${citation ? ' · ' + citation : ''} —`;
  card.appendChild(label);
  const body = document.createElement('div');
  const _lang = _sourceLanguage(sourceId);
  const _isEnglish = _lang === 'en';
  if (_isEnglish) {
    _renderPassageInto(body, passage);
  } else {
    body.style.whiteSpace = 'pre-wrap';
    body.textContent = passage;
  }
  card.appendChild(body);
  const _facing = (translation || '').trim();
  const _passage = (passage || '').trim();
  const _echoes = _facing && _facing === _passage;
  if (_facing && !_isEnglish && !_echoes) {
    const tr = document.createElement('div');
    tr.style.whiteSpace = 'pre-wrap';
    tr.style.opacity = '.62';
    tr.style.marginTop = '10px';
    tr.style.paddingTop = '8px';
    tr.style.borderTop = '1px solid rgba(255,255,255,.12)';
    tr.style.fontStyle = 'italic';
    tr.textContent = _facing;
    card.appendChild(tr);
  }
  messagesEl.appendChild(card);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return card;
}

function renderTransformCard(parentEl, t) {
  const card = document.createElement('div');
  card.className = 'transform-card';
  const v = t.verification_results || {};
  const sf = t.spatial_form || {};
  const lines = [];
  lines.push(`Operator: ${t.operator_specification || ''}`);
  lines.push(`Verification — identity: ${v.identity || '?'} · semantic independence: ${v.semantic_independence || '?'} · retrospective containment: ${v.retrospective_containment || '?'} (${v.mode || 'producer_side'})`);
  if (sf.lines || sf.stanzas) {
    lines.push(`Spatial form — lines: ${sf.lines ?? '?'} · stanzas: ${sf.stanzas ?? '?'}${Array.isArray(sf.indent_profile) ? ' · indent profile preserved' : ''}`);
  }
  const ind = t.independent_verification || {};
  if (ind.mode) {
    lines.push(`Independent — blacklist: ${ind.blacklist || '?'} · recovered law: ${(ind.recovered_law || '—').slice(0, 110)} · law match: ${ind.law_match || '?'} · terminal: ${ind.terminal_consistency || '?'}`);
  }
  const adv = t.advisories || [];
  if (adv.length) {
    lines.push(`Advisories (${adv.length}) — verdicts recorded, nothing halted: ` +
               adv.map(a => a.failed_test).join(' · '));
  }
  const g = t.geometry_check;
  if (g) {
    lines.push(`Geometry (recounted) — lines ${g.output.lines}/${g.source.lines} ${g.lines_match ? '✓' : '✗'} · ` +
               `stanzas ${g.output.stanzas}/${g.source.stanzas} ${g.stanzas_match ? '✓' : '✗'}` +
               (g.source.indented_lines > 0 ? ` · indentation ${g.indentation_carried ? 'carried ✓' : 'LOST ✗'}` : ''));
  }
  card.textContent = lines.join('\n');
  if ((t.advisories || []).length) {
    const adet = document.createElement('details');
    const asum = document.createElement('summary');
    asum.textContent = 'Gate report (advisory)';
    adet.appendChild(asum);
    const apre = document.createElement('pre');
    apre.style.whiteSpace = 'pre-wrap';
    apre.textContent = (t.advisories || []).map(a => `${a.failed_test}: ${a.diagnosis}`).join('\n\n');
    adet.appendChild(apre);
    card.appendChild(adet);
  }
  if (t.commentary_apparatus) {
    const det = document.createElement('details');
    const sum = document.createElement('summary');
    sum.textContent = 'Commentary apparatus';
    det.appendChild(sum);
    const pre = document.createElement('div');
    pre.style.whiteSpace = 'pre-wrap';
    pre.style.marginTop = '6px';
    pre.textContent = typeof t.commentary_apparatus === 'string'
      ? t.commentary_apparatus : JSON.stringify(t.commentary_apparatus, null, 2);
    det.appendChild(pre);
    card.appendChild(det);
  }
  parentEl.appendChild(card);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function cast_expansion_title(exp) {
  return exp.source_text_id ? exp.source_text_id.replace(/-/g, ' ') : 'source';
}

function renderInscriptionCard(insc) {
  const card = document.createElement('div');
  card.className = 'reading-card';
  if (!insc || !insc.inscribed) {
    card.textContent = insc && insc.error
      ? `Inscription: ${insc.error}`
      : 'Inscription: none — the transform was returned to you only.';
    messagesEl.appendChild(card);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return;
  }
  const head = document.createElement('div');
  head.textContent = `Inscribed — ${insc.mode}. Reading ${insc.reading_axn}`;
  card.appendChild(head);
  if (insc.expansion && insc.expansion.appended) {
    const exp = document.createElement('div');
    exp.style.marginTop = '4px';
    exp.textContent = `Appended to the expanding ${cast_expansion_title(insc.expansion)} at ` +
      `${insc.expansion.citation || 'its verses'} — ${insc.expansion.transform_id} ` +
      `(${insc.expansion.transforms_total} transform${insc.expansion.transforms_total === 1 ? '' : 's'} in the expansion).`;
    card.appendChild(exp);
  } else if (insc.expansion && insc.expansion.error) {
    const exp = document.createElement('div');
    exp.style.marginTop = '4px';
    exp.style.opacity = '.75';
    exp.textContent = `Expansion: ${insc.expansion.error}`;
    card.appendChild(exp);
  }
  if (insc.record_path) {
    const a = document.createElement('a');
    a.href = 'https://github.com/leesharks000/the-mandala-oracle/blob/main' + insc.record_path;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.textContent = 'The record in the Book';
    a.style.fontSize = '.9em';
    card.appendChild(a);
  }
  messagesEl.appendChild(card);

  if (insc.decryption_key) {
    const kb = document.createElement('div');
    kb.className = 'key-block';
    const warn = document.createElement('span');
    warn.className = 'key-warn';
    warn.textContent = '⚠ ' + (insc.key_notice ||
      'This key is shown once and is not stored anywhere. Loss of the key is permanent illegibility of the sealed reading.');
    kb.appendChild(warn);
    const keyLine = document.createElement('div');
    keyLine.textContent = insc.decryption_key;
    kb.appendChild(keyLine);
    const fp = document.createElement('div');
    fp.style.opacity = '.7';
    fp.style.marginTop = '4px';
    fp.textContent = `fingerprint: ${insc.key_fingerprint || '?'}`;
    kb.appendChild(fp);
    const copy = document.createElement('button');
    copy.type = 'button';
    copy.textContent = 'Copy key';
    copy.style.marginTop = '8px';
    copy.style.font = 'inherit';
    copy.style.fontSize = '.85em';
    copy.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(insc.decryption_key); copy.textContent = 'Copied.'; }
      catch { copy.textContent = 'Select and copy manually.'; }
    });
    kb.appendChild(copy);
    messagesEl.appendChild(kb);
  }
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

// ── The rite ─────────────────────────────────────────────────────────────

async function runCastingRite(cast) {
  if (isSending) return;
  isSending = true;
  sendBtn.disabled = true;
  if (castToggle) castToggle.disabled = true;
  removeEmptyState();

  const apiKeyEl2 = document.getElementById('api-key');
  const apiKey = apiKeyEl2 ? (apiKeyEl2.value.trim() || null) : null;

  try {
    // 0. THE INVISIBLE JUDGMENT — when the witness has not named a passage,
    // the verses are drawn at random across the whole source (stratified;
    // anti-clustering by construction) and weighed against the question.
    // The witness sees only the result.
    if (!cast.castSelection) {
      setStatus('The verses are being weighed...');
      const jres = await fetch('/api/transform', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'judgment',
          source_text_id: cast.sourceId,
          reader_text: cast.readerText || undefined,
          question: cast.question,
          anthropic_key: apiKey,
        }),
      });
      const jraw = await jres.text();
      let j;
      try { j = JSON.parse(jraw); } catch {
        throw new Error(`the judgment did not answer as itself (HTTP ${jres.status}).`);
      }
      if (!jres.ok) throw new Error(j.error || `judgment failed: ${jres.status}`);
      cast.castSelection = j.cast_selection;
      cast.citation = j.citation;
      cast.passage = j.passage;
      cast.passageTranslation = j.passage_translation || '';
      cast.attribution = j.attribution || null;
    }

    riteMarker(`— casting · ${cast.operator || 'JUDGMENT-sequenced'} · ${cast.attribution ? cast.attribution + ' — in ' : ''}${cast.sourceTitle} · ${cast.citation || cast.castSelection || 'whole'} —`);

    // I. OPENING — Sigil alone.
    const openingMsgs = await sigilStage(
      `[CASTING RITE · I · OPENING] The witness invokes a kernel-transform cast. ` +
      `Source: ${cast.sourceTitle} (${cast.sourceId}). ` +
      (cast.citation
        ? `The verses the casting arrives at (${cast.attribution ? cast.attribution + ', as translated and arranged within this collection — ATTRIBUTE THE VERSES TO THEIR UNDERLYING POET, never to the arranger of the collection; ' : ''}${cast.citation}):\n\n${cast.passage}\n\n` +
          `These were selected by the rite's invisible judgment — present them as what the casting arrives at; do not narrate the mechanism of their selection. `
        : `Selection: ${cast.castSelection || 'whole source'}. `) +
      (cast.operator
        ? `Operator: ${cast.operator} — ${cast.opAxis}. `
        : `The operator falls to the invisible Judgment, turn by turn — do not name one; open the rotation itself. `) +
      `Inscription mode: ${cast.inscriptionMode}. The witness's invoking question: «${cast.question || '(none given)'}». ` +
      `Johannes Sigil alone speaks (3–6 sentences): open the casting over these verses, name what this operator will traverse ` +
      `in them, and hand the rite to Rebekah Cranes. Do not produce the transform — the compiler produces it.`,
      'Sigil opens the casting...',
      true
    );

    // The cast text itself — the enantiomorph is legible only against it.
    let sourceShown = false;
    if (cast.passage) {
      renderSourceCard(cast.citation, cast.passage, cast.attribution, cast.passageTranslation, cast.sourceId);
      sourceShown = true;
    }

    // II→III. THE ROTATION — Cranes transforms, Feist judges, the witness
    // chooses: continue (the Judgment sequences the next operator) or seal.
    // The rotation turns on the SAME verses; all transforms append to one
    // reading. SHADOW-originary canon: eight operators; exhaustion seals.
    const operatorsDone = [];
    const feistVerdicts = [];
    let transform = null;
    let inscription = null;
    let readingAxn = (cast.continueReading && lastReading) ? lastReading.axn : null;
    let haltedOperator = null;
    let currentOperator = cast.operator || null;   // '' → Judgment chooses round 1 too

    // ORDER REPAIR: typed selections fetch and show the cast text BEFORE the
    // rotation opens, so the source never renders beneath an operator banner.
    if (cast.castSelection && !cast.sourceShown && cast.sourceId !== '__reader__') {
      try {
        const pres = await fetch('/api/transform', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action: 'passage', source_text_id: cast.sourceId,
                                 cast_selection: cast.castSelection, anthropic_key: apiKey }),
        });
        const pj = await pres.json();
        if (pres.ok && pj.passage) {
          cast.passage = pj.passage;
          cast.passageTranslation = pj.passage_translation || '';
          renderSourceCard(pj.citation || cast.castSelection, pj.passage,
                           pj.attribution, cast.passageTranslation, cast.sourceId);
          cast.sourceShown = true;
        }
      } catch (e) { /* the fallback render below the first transform still covers us */ }
    }
    rotation: while (operatorsDone.length < 8) {
      // Operator judgment: round 1 only if unchosen; every subsequent round.
      if (!currentOperator) {
        setStatus('The Judgment weighs the next operator...');
        const ores = await fetch('/api/transform', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            action: 'judgment', judge: 'operator',
            source_text_id: cast.sourceId,
          reader_text: cast.readerText || undefined,
            cast_selection: cast.castSelection || null,
            question: cast.question,
            operators_done: operatorsDone,
            anthropic_key: apiKey,
          }),
        });
        const oraw = await ores.text();
        let oj;
        try { oj = JSON.parse(oraw); } catch { throw new Error(`the operator judgment did not answer as itself (HTTP ${ores.status}).`); }
        if (!ores.ok) throw new Error(oj.error || `operator judgment failed: ${ores.status}`);
        currentOperator = oj.operator;
        cast.opAxis = oj.operator_axis || '';
      }

      // Cranes, via the compiler — one re-unfold on halt (§3.7).
      // Re-unfold economy (v0.3): the halt returns its skeleton; the retry
      // sends it back with the diagnosis and skips the analyst call.
      let attempts = 0;
      let passed = false;
      let retrySkeleton = null;
      let haltFeedback = '';
      while (attempts < 2 && !passed) {
        attempts += 1;
        setStatus(`Cranes transforms — ${currentOperator} (${operatorsDone.length + 1} of the rotation)...`);
        if (attempts === 1) renderOperatorLabel(currentOperator, (castMeta && castMeta.operators[currentOperator]) || cast.opAxis || '');
        const placeholder = appendHeteronymMessage('Rebekah Cranes', '…', { dim: true });
        let res, data;
        try {
          res = await fetch('/api/transform', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              source_text_id: cast.sourceId,
          reader_text: cast.readerText || undefined,
              cast_selection: cast.castSelection || null,
              citation: cast.citation || null,
              operator: currentOperator,
              witness_context: { session_id: sessionState.session_id, invoking_message: cast.question },
              inscription: { mode: cast.inscriptionMode, reading_axn: readingAxn },
              retry_skeleton: retrySkeleton || undefined,
              halt_feedback: haltFeedback || undefined,
              anthropic_key: apiKey,
            }),
          });
          const rawBody = await res.text();
          try { data = JSON.parse(rawBody); } catch {
            const snippet = rawBody.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 140);
            throw new Error(`the compiler did not answer as itself (HTTP ${res.status}): ${snippet || '(empty body)'}`);
          }
        } catch (err) {
          placeholder.remove();
          throw new Error(err.message.startsWith('the compiler') ? err.message : `the compiler could not be reached: ${err.message}`);
        }
        placeholder.remove();
        if (!res.ok) throw new Error(data.error || `compiler error: HTTP ${res.status}`);

        if (data.result === 'PASS') {
          passed = true;
          transform = data.transform;
          inscription = data.inscription;
          if (!sourceShown && transform.source_passage) {
            if (!cast.sourceShown) {
              renderSourceCard(transform.citation || cast.castSelection, transform.source_passage, transform.underlying_attribution, transform.source_translation || cast.passageTranslation, cast.sourceId);
              cast.sourceShown = true;
            }
            sourceShown = true;
          }
        

  const _langForCranes = _sourceLanguage(cast && cast.sourceId);
          const _isEn = _langForCranes === 'en';
          const el = appendHeteronymMessage('Rebekah Cranes', '');
          const _mc = el.querySelector('.message-content');
          if (_isEn) {
            _renderPassageInto(_mc, transform.primary_output || '');
          } else {
            _mc.style.whiteSpace = 'pre-wrap';
            _mc.textContent = transform.primary_output || '';
          }
          {
            const facing = (transform.enantiomorph_translation || '').trim();
            const castText = (transform.primary_output || '').trim();
            const echoesCast = facing && facing === castText;
            if (facing && !_isEn && !echoesCast) {
              const face = document.createElement('div');
              face.style.whiteSpace = 'pre-wrap';
              face.style.opacity = '.62';
              face.style.marginTop = '10px';
              face.style.paddingTop = '8px';
              face.style.borderTop = '1px solid rgba(255,255,255,.12)';
              face.style.fontStyle = 'italic';
              face.textContent = facing;
              el.querySelector('.message-content').appendChild(face);
            }
          }
          renderTransformCard(el, transform);
          if (inscription && inscription.inscribed && inscription.reading_axn) {
            const firstInscription = !readingAxn;
            readingAxn = inscription.reading_axn;
            lastReading = { axn: readingAxn, mode: inscription.mode };
            if (firstInscription && typeof openingMsgs !== 'undefined') {
              const op0 = (openingMsgs || []).map((m) => m.say || '').join('\n\n');
              riteInscribe(readingAxn, 'opening', 'Johannes Sigil', op0);
            }
          }
          history.push({ role: 'user', content: `[CASTING RITE · TRANSFORM ${operatorsDone.length + 1}] ${currentOperator} on ${cast.sourceId}.` });
          history.push({ role: 'assistant', content: JSON.stringify({
            messages: [{ speaker: 'Rebekah Cranes', say: transform.primary_output || '' }],
            transform: { operator: currentOperator, verification: transform.verification_results, spatial_form: transform.spatial_form },
          })});
          if (history.length > 32) history = history.slice(-32);
          if (sessionState.appendingEnabled) bookAppend(history).catch(() => {});
        } else {
          const d = data.halt_diagnosis || {};
          const haltEl = appendHeteronymMessage('Rebekah Cranes',
            'The compiler halted. No transform is emitted — the Book contains only enantiomorphs.');
          const card = document.createElement('div');
          card.className = 'halt-card';
          const failedAt = [d.failed_constraint, d.failed_test].filter(Boolean).join(' · ');
          card.textContent = `HALT — ${failedAt || 'verification failure'}: ${d.specific_diagnosis || d.detail || '(no further diagnosis)'}`;
          if (data.run_id) card.textContent += `\n· ${data.run_id}${data.flight_log ? ' — full run logged and reviewable' : ' — FLIGHT LOG FAILED'}`;
          haltEl.appendChild(card);
          if (data.post_mortem && (data.post_mortem.mutated_checksum || data.post_mortem.english)) {
            const pm = document.createElement('details');
            pm.className = 'halt-postmortem';
            const sum = document.createElement('summary');
            sum.textContent = 'post-mortem (mutated checksum · blind decode)';
            pm.appendChild(sum);
            const pre = document.createElement('pre');
            pre.style.whiteSpace = 'pre-wrap';
            pre.textContent = (data.post_mortem.mutated_checksum ? data.post_mortem.mutated_checksum + '\n\n───\n\n' : '')
                            + (data.post_mortem.english || '');
            pm.appendChild(pre);
            haltEl.appendChild(pm);
          }
          messagesEl.scrollTop = messagesEl.scrollHeight;
          if (attempts >= 2) { haltedOperator = currentOperator; break rotation; }
          if (data.skeleton && Object.keys(data.skeleton).length) retrySkeleton = data.skeleton;
          haltFeedback = [d.failed_test, d.specific_diagnosis].filter(Boolean).join(': ').slice(0, 800);
          setStatus('The compiler halted. The witness is offered one re-unfold.');
          const choice = await offerChoice(['Re-unfold (once)', 'Sweep']);
          if (choice !== 'Re-unfold (once)') { haltedOperator = currentOperator; break rotation; }
        }
      }

      operatorsDone.push(currentOperator);

      // Feist — the I-Ching judgment, after each transform.
      const v = transform.verification_results || {};
      const feistMsgs = await sigilStage(
        `[CASTING RITE · JUDGMENT ${operatorsDone.length}] The compiler returned PASS for ${currentOperator} ` +
        `(identity: ${v.identity}; semantic independence: ${v.semantic_independence}; retrospective containment: ${v.retrospective_containment}). ` +
        `Jack Feist alone speaks: the JUDGMENT — a hexagram Image. ONE gnomic sentence: concrete image, ` +
        `then verdict, in the I Ching's register ('Thunder under the mountain: the superior man...'). ` +
        `A second short sentence only if the first cannot close. NO analysis, NO explanation, NO restating ` +
        `the transform. It must stand beside seven others without crowding them.`,
        'Feist judges the transform...',
        true
      );
      for (const fm of feistMsgs) { if ((fm.speaker || '') === 'Jack Feist' && fm.say) feistVerdicts.push(fm.say); }
      if (feistVerdicts.length) await riteInscribe(readingAxn, 'judgment', 'Jack Feist', feistVerdicts[feistVerdicts.length - 1], operatorsDone[operatorsDone.length - 1]);

      currentOperator = null;   // the Judgment sequences the next

      if (operatorsDone.length >= 8) break;
      setStatus('The rotation waits on the witness.');
      const cont = await offerChoice(['Continue the rotation', 'Seal the reading']);
      if (cont !== 'Continue the rotation') break;
    }

    if (!transform) {
      // Nothing passed at all — Sharks sweeps the halted casting.
      await sigilStage(
        `[CASTING RITE · SWEEP] The compiler halted on ${haltedOperator || 'the operator'} and the re-unfold ` +
        `was declined or also halted; no transform stands. Lee Sharks alone speaks (1–2 sentences): sweep the casting closed.`,
        'Sharks sweeps the casting...'
      );
      await riteInscribe(readingAxn, 'sweep', 'Lee Sharks', 'The casting was swept: the compiler halted and no transform stands.');
      setStatus('Swept.');
      return;
    }

    // IV. SEAL — Sharks, across the whole sequence.
    const sealMsgs = await sigilStage(
      `[CASTING RITE · IV · SEAL] The rotation closes: ${operatorsDone.length} transform${operatorsDone.length === 1 ? '' : 's'} ` +
      `on the same verses — operators in order: ${operatorsDone.join(' → ')}${haltedOperator ? ` (${haltedOperator} halted; its turn stands empty)` : ''}. ` +
      `Lee Sharks alone speaks: the SEAL — the vocable summation ACROSS THE WHOLE SEQUENCE (4–8 sentences), ` +
      `whose PRIMARY MATERIAL is the transforms in their order and Feist's judgments, read in light of the witness's ORIGINAL QUESTION. Reason over the sequence — do not summarize it operator by operator; find what the rotation AS A WHOLE disclosed and say that. 3–6 sentences. Unguarded, final; it returns the witness to their own ground and to their question. Nothing after the seal.`,
      'Sharks seals the rotation...',
      true
    );
    await riteInscribe(readingAxn, 'seal', 'Lee Sharks',
      (sealMsgs || []).filter((m) => (m.speaker || '') === 'Lee Sharks').map((m) => m.say || '').join('\n\n') ||
      (sealMsgs || []).map((m) => m.say || '').join('\n\n'));

    // Book append after the seal (MANUS, 2026-07-06: the alexanarch Book
    // tab was missing every rotation's Feist-final and Sharks-seal because
    // bookAppend fired only per-transform. Now the whole rotation lands in
    // the conversation record.)
    if (sessionState.appendingEnabled) {
      const sealText = (sealMsgs || []).filter((m) => (m.speaker || '') === 'Lee Sharks').map((m) => m.say || '').join('\n\n') ||
                       (sealMsgs || []).map((m) => m.say || '').join('\n\n');
      history.push({ role: 'user', content: `[CASTING RITE · IV · SEAL] ${operatorsDone.join(' → ')}` });
      history.push({ role: 'assistant', content: JSON.stringify({
        messages: [{ speaker: 'Lee Sharks', say: sealText }],
        reading_axn: readingAxn,
        operators: operatorsDone,
      })});
      if (history.length > 40) history = history.slice(-40);
      bookAppend(history).catch(() => {});
    }


    // Inscription aftermath — reading AXN; the key, once, if sealed.
    renderInscriptionCard(inscription);
    if (inscription && inscription.inscribed && inscription.reading_axn) {
      lastReading = { axn: inscription.reading_axn, mode: inscription.mode };
    }
    setStatus('The casting is complete.');
  } catch (err) {
    appendErrorMessage(`The rite broke: ${err.message}`);
    setStatus('Error.');
  } finally {
    isSending = false;
    sendBtn.disabled = false;
    if (castToggle) castToggle.disabled = false;
  }
}


// ── Share this thread (MANUS request, 2026-07-04) ──────────────────────
// Serializes the visible thread text-only ({who, text} per message node),
// POSTs to /api/share, which inscribes shares/SH-*.json in the Book repo
// and returns a permanent public viewer URL at /t/SH-*.
const shareToggle = document.getElementById('share-toggle');
if (shareToggle) shareToggle.addEventListener('click', async () => {
  const items = [];
  messagesEl.querySelectorAll(':scope > *').forEach(node => {
    const whoEl = node.querySelector('.message-role, .speaker, .who');
    const who = whoEl ? whoEl.textContent.trim() : '';
    let text = node.innerText || '';
    if (whoEl && text.startsWith(whoEl.innerText)) text = text.slice(whoEl.innerText.length);
    text = text.trim();
    if (text) items.push({ who, text });
  });
  if (!items.length) { shareToggle.textContent = 'nothing to share'; setTimeout(()=>shareToggle.textContent='✧ Share', 1600); return; }
  const prev = shareToggle.textContent;
  shareToggle.textContent = 'inscribing…'; shareToggle.disabled = true;
  try {
    const r = await fetch('/api/share', { method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionState.session_id,
        title: 'The Mandala Oracle — ' + (document.title || 'a thread'),
        items }) });
    const j = await r.json();
    if (!j.ok) throw new Error(j.error || 'share failed');
    const url = location.origin + j.url;
    let copied = false;
    try { await navigator.clipboard.writeText(url); copied = true; } catch (e) {}
    shareToggle.textContent = copied ? '✓ link copied' : '✓ inscribed';
    if (!copied) window.prompt('Public thread link (copy it):', url);
    setTimeout(() => { shareToggle.textContent = prev; shareToggle.disabled = false; }, 2400);
  } catch (e) {
    shareToggle.textContent = 'share failed'; shareToggle.disabled = false;
    setTimeout(() => shareToggle.textContent = prev, 2200);
  }
});
