# client/

Witness-facing static interface. Deployed to `themandalaoracle.com` via Vercel.

## v1 structure

- **`index.html`** — single-page interface. Left panel: chat window with Sigil. Right panel: three.js sky.
- **`sky.js`** — three.js renderer. Instanced point cloud for inscriptions, line geometry for lineage edges, billboard sprites for planetary bodies. Listens for navigation directives via postMessage from the chat panel; respects mode toggle (Sabbath / Merkabah).
- **`chat.js`** — chat UI. POSTs to `/api/sigil` with `{message, history, sky_state, mode}`. Renders Sigil's `say` response in the chat panel; forwards `navigate` directive (if present and mode is Merkabah) to the sky.
- **`mode.js`** — toggle between Sabbath (default) and Merkabah modes. Sabbath mode suppresses navigation directives at the system-prompt level (sent in the API call); Merkabah mode permits them.
- **`styles.css`** — minimal styling. Dark background. Chat panel maybe 30% width, sky panel 70%. Mode toggle at top of chat panel.

## No build step (v1)

ES modules loaded directly via `<script type="module">`. three.js imported from CDN. No bundler. Keeps the dependency surface tiny and the deploy reproducible.

If bundling becomes worthwhile (typescript, dependency consolidation), v1+N adds Vite. Not v1.

## Mode toggle architecture

The toggle is in the chat panel UI but its constitutional weight lives in the system prompt sent to Sigil. Sabbath prompt omits the navigation grammar entirely; Merkabah prompt includes it. The sky client also defensively ignores `navigate` directives when in Sabbath mode regardless of what Sigil emitted. Defense in depth.
