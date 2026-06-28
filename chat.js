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
const apiKeyEl = document.getElementById('api-key-input');
const modeBtns = document.querySelectorAll('.mode-button');
const settingsToggle = document.getElementById('settings-toggle');
const settingsPanel = document.getElementById('settings-panel');
const settingsClose = settingsPanel.querySelector('.settings-close');

let mode = 'sabbath';
let history = [];  // [{role: 'user'|'assistant', content: str}, ...]
let isSending = false;
let emptyStateRemoved = false;

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
// Settings panel
// ─────────────────────────────────────────────────────────────────────────

settingsToggle.addEventListener('click', () => {
  const open = settingsPanel.classList.toggle('open');
  settingsPanel.setAttribute('aria-hidden', open ? 'false' : 'true');
  settingsToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  if (open) apiKeyEl.focus();
});

settingsClose.addEventListener('click', () => {
  settingsPanel.classList.remove('open');
  settingsPanel.setAttribute('aria-hidden', 'true');
  settingsToggle.setAttribute('aria-expanded', 'false');
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && settingsPanel.classList.contains('open')) {
    settingsPanel.classList.remove('open');
    settingsPanel.setAttribute('aria-hidden', 'true');
    settingsToggle.setAttribute('aria-expanded', 'false');
  }
});

// ─────────────────────────────────────────────────────────────────────────
// Sky readiness
// ─────────────────────────────────────────────────────────────────────────

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

  const apiKey = apiKeyEl.value.trim() || null;

  removeEmptyState();
  appendUserMessage(message);
  inputEl.value = '';
  inputEl.style.height = 'auto';

  isSending = true;
  sendBtn.disabled = true;
  setStatus('Sigil is reading...');

  const placeholder = appendHeteronymMessage('Johannes Sigil', '…', { dim: true });

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
    li.textContent = `${r.axn.split('.').slice(0, 2).join('.')} — ${r.title || '(no title)'}`;
    ul.appendChild(li);
  }
  details.appendChild(ul);
  messageEl.appendChild(details);
}

function setStatus(text) {
  statusEl.textContent = text;
}
