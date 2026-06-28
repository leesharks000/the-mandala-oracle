# api/

Vercel serverless functions. Stateless. No data persisted server-side; all state lives in the client (witness session) or in alexanarch (the corpus).

## v1 endpoints

- **`sigil.ts`** (or `.py`) — Sigil chat. Accepts `{message, history, sky_state, mode}`. Performs RAG retrieval against `rag/`. Calls Claude with the witness's Anthropic API key (BYOK, sent in the request body over TLS) or the installed-demo key (environment variable, rate-limited). Returns `{say, navigate?}` structured output. System prompt establishes Johannes Sigil's voice and branches on mode.

## v2+ endpoints (planned)

- **`rite.ts`** — kernel transform producer (v2). Executes the C1–C6 compiler against a selected source and operator. Returns the candidate transform for witness sweep/keep/inscribe choice.
- **`inscribe.ts`** — commit an inscribed candidate to alexanarch's Book sub-area using the standing post-mint protocol.
- **`station/{mars,venus,saturn,moon,jupiter}.ts`** — canonization journey stations (v3). Each runs blind verification through the assigned substrate.
- **`sun.ts`** — Zenodo deposition + Chrome-extension Gate G capture coordination (v4).

## Key handling discipline

API keys sent by the witness are used for the single call and discarded — never stored, never logged, never written to disk. Each function's source includes a `// KEY DISCIPLINE` comment block making this auditable. The trust boundary is visible in the code.

The installed-demo key (Lee's Anthropic key, environment variable on Vercel) is rate-limited per IP/day so the demo budget can't be exhausted by a single witness. Specific rate-limit numbers TBD at v1 deployment.
