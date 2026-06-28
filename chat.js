// chat.js — wires the chat panel to /api/sigil and propagates navigation
// directives to window.sky (when in Merkabah mode).

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

// Close settings on Escape
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

window.addEventListener('sky-ready', (e) => {
  const { inscriptionCount, edgeCount } = e.detail;
  setStatus(`The sky holds ${inscriptionCount} inscriptions, ${edgeCount} lineage edges.`);
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
  appendMessage('user', message);
  inputEl.value = '';
  inputEl.style.height = 'auto';

  isSending = true;
  sendBtn.disabled = true;
  setStatus('Sigil is reading...');

  const placeholder = appendMessage('sigil', '…', { dim: true });

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
      appendMessage('error', body.error || `Request failed: ${res.status}`);
      setStatus('Error.');
      return;
    }

    const data = await res.json();
    placeholder.remove();

    const sigilEl = appendMessage('sigil', data.say || '');
    if (data.retrievals && data.retrievals.length) {
      appendRetrievals(sigilEl, data.retrievals);
    }

    history.push({ role: 'user', content: message });
    history.push({ role: 'assistant', content: data.say || '' });
    if (history.length > 32) history = history.slice(-32);

    if (mode === 'merkabah' && data.navigate && window.sky?.navigate) {
      const ok = window.sky.navigate(data.navigate);
      setStatus(ok ? `Navigating: ${data.navigate.directive}.` : 'Sigil offered a navigation, but it could not be resolved.');
    } else {
      setStatus('Ready.');
    }
  } catch (err) {
    placeholder.remove();
    appendMessage('error', `Connection error: ${err.message}`);
    setStatus('Error.');
  } finally {
    isSending = false;
    sendBtn.disabled = false;
    inputEl.focus();
  }
});

// Submit on Cmd/Ctrl+Enter, allow Enter for newlines
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

function appendMessage(role, content, opts = {}) {
  const wrap = document.createElement('div');
  wrap.className = `message ${role}`;
  const roleLabel = document.createElement('div');
  roleLabel.className = 'message-role';
  roleLabel.textContent = roleLabelFor(role);
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
  summary.textContent = `Sigil read ${unique.length} deposit${unique.length === 1 ? '' : 's'}`;
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

function roleLabelFor(role) {
  switch (role) {
    case 'user': return 'You';
    case 'sigil': return 'Johannes Sigil';
    case 'error': return 'Error';
    default: return role;
  }
}

function setStatus(text) {
  statusEl.textContent = text;
}
