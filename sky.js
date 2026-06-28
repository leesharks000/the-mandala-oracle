// sky.js — v2.0 — static photographic backdrop mode.
//
// The WebGL real-stars renderer is preserved at sky-real-stars.js.deferred
// for future reactivation. In v2.0 the sky is a static photographic image
// applied via CSS to #sky-canvas-container (see styles.css). No WebGL, no
// three.js, no render loop. Just an image.
//
// This file remains as a tiny stub so chat.js's optional window.sky.setMode
// calls don't throw. The Sabbath/Merkabah toggle becomes inert visually in
// this iteration — both modes look the same (the photo). It'll become
// meaningful again when we layer interactive sky behavior back on top.

function setMode(_mode) { /* no-op in static backdrop mode */ }

window.sky = { setMode, mode: 'static-backdrop' };
window.dispatchEvent(new CustomEvent('sky-ready', {
  detail: { backdrop: 'static', version: 'v2.0' },
}));

console.log('[sky] v2.0 — static photographic backdrop; WebGL deferred to sky-real-stars.js.deferred');
