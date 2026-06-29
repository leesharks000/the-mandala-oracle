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
    for (let i = 0; i < respMessages.length; i++) {
      const m = respMessages[i];
      const speaker = m.speaker || 'Johannes Sigil';
      const say = m.say || '';
      lastEl = appendHeteronymMessage(speaker, say);
      if (m.navigate) lastNavigate = m.navigate;
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
