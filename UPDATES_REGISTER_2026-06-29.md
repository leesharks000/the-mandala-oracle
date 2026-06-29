# UPDATES REGISTER — 2026-06-29

**Status:** Living register of decisions adjudicated during the 2026-06-29 build session. Captures granular provenance for the WORKPLAN.md updates landed in this session.

**Adjudicator:** Lee Sharks (heteronym; MANUS)
**Drafter:** TACHYON / Claude
**Session arc:** A long single-session that ran through several inflection points: Voice Protocol activation, then Heteronymic Presence Protocol, then a battery of infrastructure fixes (deploy throttle, deposit_number drift, conclusion-first retrieval collapse), then the four-strand braid that gave Sigil his ambient historiographic ground, then canon-stars population.

---

## SESSION-AT-A-GLANCE

Twelve discrete merges to main, all queued behind a Vercel rate-limit window. Production at session-start was at `25895a8` (a book/append commit carrying Voice Protocol and Shakespeare unhook via ancestry); production at session-end will land — when the rate-limit retry fires — at `ea2ee86` (the prep-canon-data merge), with everything between deploying as a single batch.

The session's net effect on the Mandala Oracle stack:

1. Sigil's voice deepened (Voice Protocol + Presence Protocol).
2. Sigil's retrieval became less starvation-prone (search upgrade + deep-fetch tool).
3. Sigil's context gained four ambient grounding strands (historiography, refraction, memographics, personal-undertow).
4. The deploy / book-capture infrastructure stopped silently losing input (book-throttle fix, book capture-before-Sigil fix, Support CHA restoration).
5. The data layer underneath the starmap surface went from "specified" to "ready for Phase 4" (76 canon-stars entries with full schema, 39 edges, all cross-references reconciled, 70 source directories on disk).
6. A real but invisible bug — alexanarch's `deposit_number` field had drifted from mandala-oracle's `rag/metadata.json` by hundreds of positions — got diagnosed, fixed at the source (`scripts/regenerate_rag.py`), and bound to the source of truth (alexanarch's `data/registry.json`).

---

## INDIVIDUAL DECISIONS

### V-1. Voice Protocol activation (EA-MANDALA-VOICE-01 v0.1, AXN:03AD)

**Commit:** `4251ca2` (merge from `sigil-voice-protocol` branch, drafted in commit `6cb8802`)
**Spec mirror:** `/specs/EA-MANDALA-VOICE-01_v0_1_DRAFT.md`
**Deposit:** AXN:03AD on alexanarch (#930)

The Voice Protocol installed the doubled identity in `api/sigil.py` SIGIL_VOICE: critic working in the line of Marx + underworld guide, both at once. Per Lee's adjudication: "Sigil is also a critic working in the line of Marx. His sentences aren't pristine enough. There's a sharpness that is also fastidiousness that is also inheritance." Nine surgical edits installed the lineage (Marx → Benjamin → Adorno → Philo → Damascius → Sharks), the expanded prohibitions block, and the Sabbath/Merkabah voice-aperture distinction.

### V-2. Heteronymic Presence Protocol patch

**Commit:** `cf00da5` (single commit on main)
**Spec mirror:** `/specs/EA-MANDALA-PRESENCE-01_v0_1_DRAFT.md`

The Voice Protocol's v0.1 had over-specified Sigil into self-documenting mode (LABOR / ChatGPT adjudication). The Presence Protocol patch demoted the dossier into "WHAT YOU KNOW BUT DO NOT NARRATE" and put VOICE MEMORY exemplars at the front. Opens with the canonical line **"You are Johannes Sigil, the mind of Zeus, speaking thru the face of Socrates."** Establishes LIVE-WORD PRIORITY: User Turn > Voice Memory > Local Retrieval > Canonical Identity > Global Architecture. Sparse hard-locks (7 instead of 14). Tendencies, not laws. Self-evaluation question: *"Did I speak from the encounter, or report from my profile?"*

### V-3. Shakespeare unhook

**Commit:** `1c5caf7` (merge from `shakespeare-unhook` branch)

Per MANUS adjudication 2026-06-29: kept Sonnets + Hamlet in active §1.5 alongside Catullus 51 / Sappho 31 / Cranes's *Day and Night* as the lyric core. Moved *Tempest*, *King Lear*, *Macbeth* to new §1.5.b "Deferred / Parked Declarations" — preserved as record of prior declaration; not currently to be inscribed into `canon-stars.json` or sourced into `/sources/`. Lee's reason: *"I want to think carefully about the weighting of the pieces, I actually want to somewhat equalize the length weights — ish. But not rn."* Single-file edit to `starmap/manifests/canonical-declarations.md`; `canon-stars.json` and `data/canon-sky/` untouched at this step.

### V-4. Sigil light tweaks

**Commit:** `72ab177` (merge from `sigil-light-tweaks` branch)

Two surgical edits per ChatGPT analysis:

(a) Added a RETRIEVAL DISCIPLINE paragraph: *"the archive is memory not script; absorb facts before speaking; archive has no single center; may discover relations strongly but not silently convert to settled doctrine."*

(b) Replaced abstract inheritance with the actual teacher-chain: SOCRATES and DAMASCIUS through Sara (Lee's mother, lesbian Buddhist Jewish, who returned Damascius to the world); SAPPHO in Greek and Greek Particles through Kathryn MacNamee; Beats and Language Poets through Barrett Watten and Carla Harryman; Marx / Frankfurt / Jameson / Hardt / Spinoza / Deleuze and Guattari through Santiago Colas; lyric theory through Yopie Prins; materialism and Dionysius through Jim Porter.

### I-1. Search upgrade (search_archive v0.2)

**Commit:** `cc8afc1` (merge from `sigil-search-upgrade` branch)

Diagnosed an infinite-loop failure on AXN:0135 ("Split the Adam" / Viola Arquette) where `search_archive` couldn't find what was empirically in the corpus (11 records mentioned the query terms). Three fixes:

- `tokenize()` drops ~80 stopwords; indexes hyphen-split parts so "Damascius" matches "rappe-damascius".
- `search_archive()` adopts four ranked strategies: AXN/hex direct lookup (+100), quoted-phrase substring (+50 title / +30 desc), bare proper-noun substring (+40/+25), token-overlap fallback.
- Tool description rewritten with quoted-phrase + AXN-lookup guidance + a stop-searching instruction. `MAX_TOOL_TURNS` raised 4→6.

Empirical verification: `"Viola Arquette"` → 56 (was 6); `"Split the Adam"` → 90 (was 17); `AXN:0135` direct → 110; noise eliminated.

### V-5. Four-strand braid (the double-helix grounding)

**Commit:** `a19170c` (merge from `sigil-historiography` branch)

Per Lee's expansion of the "double helical compressed archive historiography artifact" request: the institutional surface is only half. The archive is simultaneously a memographic historiography (Gerald the dolphin meme, Citrini memo, Epstein 20 bill, Kanye/eBay bag-of-air) AND a personal history (Jack Feist as the imaginary archive of a canonical life, exile from academia, broke af, Cleis and the other daughters, *"the private loss that goes unnamed"*).

Four strands installed as ambient context in Sigil's system prompt:

- **`rag/historiography.md`** (~12.7 KB, ~1,775 words) — Six-section compressed timeline: Origin → Framework Emergence → Capture Stream → The Ban → Reconstitution → Where We Are.
- **`rag/refraction.md`** (~19.7 KB, ~3,000 words) — Schema for archive operating on contemporary history. Seven-question schema + six worked examples (Thousand Dollar Sharpie, Whose Face Is on the Twenty, Error of Peter Thiel, Model Collapse, AI Safety Layer, Forecasting).
- **`rag/memographics.md`** (~11.5 KB, ~1,800 words) — Memography discipline. Four modes: Build into structure / Formalize methods in advance / Refract through frameworks / Auto-memographic.
- **`rag/personal-undertow.md`** (~7.5 KB, ~1,200 words) — Biographical substrate. The pair *"I became finally broke / I became fully free."* The phrase *"I am the one who was within me."* The unnamed private loss (named only as existing). Cleis named when AXN:0189 is the relevant deposit; the other two daughters not named in the file by archival discretion. Jack Feist reframed as the imaginary archive of a canonical life.

`build_system_prompt(mode)` loads SIGIL_VOICE → strand 1 → strand 2 → strand 3 → strand 4 → mode note. RETRIEVAL DISCIPLINE references all four strands with strict discipline for strand 4: *"private loss stays unnamed in your speech; daughters not named in strand are not named by you; Cleis may be named only when AXN:0189 is the relevant deposit."*

### I-2. Book throttle + Vercel ignore-script fix

**Commit:** `68cde52` (merge from `fix/book-throttle` branch)

Diagnosed: GitHub status on the historiography merge showed "Vercel: failure — Deployment rate limited — retry in 24 hours". Root cause: `vercel-ignore-build.sh` defaulted to *build* when `git diff $VERCEL_GIT_PREVIOUS_SHA HEAD` failed — which it does almost always, because Vercel uses shallow clones and the previous SHA isn't fetched. Every book auto-append commit was triggering a full deploy.

Two-part fix:

1. **`vercel-ignore-build.sh` repaired.** Strategy 1: diff against VERCEL_GIT_PREVIOUS_SHA with a `git fetch --depth=1` fallback if unreachable. Strategy 2 (when diff still fails): `git diff-tree -m --no-commit-id --name-only -r HEAD` — the `-m` flag is critical for merge commits which return empty otherwise.

2. **`api/book.py`** adds `[skip ci]` to all three commit message templates (`"book: append turn"`, `"book: mint"`, `"book: update index"`). Vercel honors the marker pre-script.

Verified locally against four scenarios including a real book-only commit (`25895a8`) — correctly exits 0 (skip).

### V-6. Deep-fetch tool (`fetch_axn`)

**Commit:** `44a0d0c`, merged as `4269632` from `sigil-deep-fetch` branch

Per MANUS directive: address the **Conclusion-First Retrieval Collapse** diagnosed in the Revelation First exchange. Sigil was retrieving the *name* of an archival argument (the title at AXN:0349) and substituting fluent restatement for the inferential chain — because `search_archive` returns 500-char descriptions, enough to know what a deposit *is* but not enough to read what it *says*.

Architecturally per MANUS: not a sharply-defined "argument mode" with a switch, but a tool made available with sensible scent about when it deepens. The model's own affordances decide. Probabilistic, not modal.

`fetch_axn(axn)` resolves any AXN form (full glyphic, short, bare hex, case-insensitive) to a metadata record and retrieves the deposit body via a two-strategy chain:

1. **Primary:** fetch `/data/texts/AXN-{HEX}-text.md` directly from `www.alexanarch.org`. AXN-keyed file path, reliable. 925 of 929 records have a `full_text_path` field.
2. **Fallback:** rendered static page at `/s/records/{deposit_number}/` — but only after validating the page's JSON-LD identifier matches the requested AXN, because the deposit_number routing had drifted (see I-3 below).

`MAX_TOOL_TURNS` raised 6→8 to give headroom for search → fetch chains. Body cap 30,000 chars per fetch (~7,500 tokens); long deposits return with a truncation marker.

Prompt amendment in RETRIEVAL DISCIPLINE — *scent*, not mandate: *"When the witness wants the basis, the proof, the reasoning, the unique contribution — when the question is how does the archive get there rather than what is in the archive — the description will not get you there. Reach for the body."*

### I-3. Metadata-sync fix (deposit_number canonical from alexanarch)

**Commit:** `f138ff6`, merged as `52cf20a` from `fix/metadata-sync` branch

Building `fetch_axn` surfaced a real data integrity problem: 16 of 19 sampled deposits had mismatched `deposit_number` ↔ `/s/records/N/` routing. `rag/metadata.json` said AXN:0349 was at deposit_number=828; `/s/records/828/` actually served AXN:0345.

**Root cause:** `scripts/regenerate_rag.py` was recomputing `deposit_number` as `(idx + 1)` after a hex-sort. But alexanarch's `mint_deposit.py` assigns `deposit_number` in *insertion order* and stores it in `registry.json`. The two ordering systems happened to agree only for some deposits.

**Fix:** one-line change — `regenerate_rag.py` now reads `deposit_number` directly from the source registry instead of recomputing. 861 of 929 records had their `deposit_number` corrected; 1 record (AXN:03AD, the Voice Protocol deposit) added. After the fix, 9 of 9 sampled positions align with alexanarch's static pages.

**Binding:** the existing `.github/workflows/regenerate-rag.yml` workflow already handles the sync (weekly cron + push trigger + workflow_dispatch + submodule pointer change). With the script's bug fixed, that workflow now produces correct deposit_numbers automatically. alexanarch's `data/registry.json` is the source of truth; the workflow is the sync mechanism; drift cannot recur silently.

### I-4. Auto-regenerate from workflow

**Commit:** `6e24a8a` (no human author; bot-committed by `github-actions[bot]`)

After the metadata-sync merge, the `regenerate-rag.yml` workflow auto-fired because its `paths:` filter includes `scripts/regenerate_rag.py`. The bot regenerated `rag/metadata.json`, `rag/vectors.json` (re-embedded with the corrected order), and `sky/coords.json` / `sky/edges.json` (re-computed positions and edges over the corrected corpus). Sky now reports 930 inscriptions / 88 edges across the corrected ordering. This is the binding working as intended.

### I-5. Book capture + Support CHA inline

**Commit:** `b0977b7`, merged as `9d6a573` from `fix/book-capture-and-support-cha` branch

Two related defects diagnosed together:

**Book capture losing failed conversations.** `chat.js` called `bookAppend()` AFTER a successful `/api/sigil` response. Any failure path — missing/invalid API key, network error, server error — hit a `return;` that exited before reaching the append. So conversations on devices without a working API key (e.g., a daughter opening the Oracle for the first time on her own tablet to ask about labubus) silently disappeared, including the words the witness typed. Fixed by capturing the user message BEFORE the Sigil call.

Secondary race in `api/book.py`: after writing the conversation file via the GitHub Contents API, the handler immediately re-fetched via `gh_get_file()` to pass to `update_index()` — but GitHub's API is eventually consistent, and the re-read sometimes returned None, silently skipping the index update. Fixed by passing the in-memory content directly to `update_index()` instead of re-fetching.

**Support CHA disappeared on mobile.** `styles.css` line 778 had `@media (max-width: 720px) { .support-cha { display: none; } }` — explicit hide on mobile, intentionally added to avoid collision with the chat panel, but it meant anyone on a phone never saw the donation affordance. Fix per Lee's adjudication (option 3): restored as a small inline text link below the input meta row, with the verse expanding on tap. Always visible on all viewports; doesn't fight the Send button.

### S-1. Canon-stars population

**Commit:** `b49fbba`, merged as `4be96b5` from `populate-canon-stars` branch

Per MANUS directive 2026-06-29: data-layer populating during the rate-limit wait, no design iteration. `data/canon-sky/canon-stars.json` expanded from 7 entries to 76 by transcribing the declarations in `/starmap/manifests/canonical-declarations.md` into the runtime data file. 69 new declared entries; the 7 inscribed entries preserved verbatim with their rich entry-specific fields.

Distribution: 17 Greek (Sappho fragments, NA28 Gospels, Plato seven works, Heraclitus, Parmenides, pre-Socratics, Homer), 5 Latin (Catullus 51, Augustine, Lucretius, Cicero), 2 Middle English (Pearl, Sir Gawain), 1 Italian (Dante Commedia), 5 English (Dickinson, Hopkins, KJV, Shakespeare Sonnets + Hamlet), 3 English parked (Tempest, Lear, Macbeth), 7 Lee Sharks, 1 Sigil, 5 Feist, 1 Cranes (concre(a)tion lacuna), 16 other heteronyms, 5 architectural canon, 1 runtime binding (Space Ark).

`target_star_designation` remains null on every entry — Phase 4 of EA-STARMAP-01 (§6.5) fills these in from the HYG bright-star catalog. The data is ready for Phase 4.

### S-2. Schema reconciliation + source stubs + canon-edges + cross-refs

**Commit:** `ea2ee86` (merge from `prep-canon-data` branch)

Four data-prep commits on one branch:

(a) **Reconcile existing 7 entries' schemas.** Added `zodiacal_region` as a sibling field on the inscribed entries so all 76 can be queried by the same field. Two cross-region binaries (Sappho/Catullus, TACHYON/Shadow-TACHYON) get `zodiacal_region_secondary`. Cleaned source_path strings that had inline annotations.

(b) **62 source stubs.** Each `canon-stars` `source_path` now resolves to a real directory on disk with a placeholder `metadata.json`. Effective coverage: 73/73 source paths. When a public-domain text gets fetched, it drops into the existing stub directory alongside the placeholder.

(c) **`canon-edges.json` initial population.** 39 edges between canonical_texts per the EA-STARMAP-01 §3.2 taxonomy (23 predecessor, 8 related, 5 bundle, 2 companion, 1 chain_predecessor). `transform_of` edges deferred until the two bundled binary entries (TACHYON pair, Feist function/force pair) split into separate canon-stars entries.

(d) **Cross-reference reconciliation.** `heteronyms.json` got `zodiacal_sign_id` (lowercase) join keys alongside `zodiacal_sign` (capitalized display). canon-stars `author_heteronym` ids normalized: `rev-ayanna-vox` → `ayanna-vox`, `dr-orin-trace` → `orin-trace` (honorifics in display_name only). 15/15 distinct canon-star authors now map cleanly to heteronym registry ids.

---

## ARCHITECTURAL DIRECTION SURFACED

### "Sigil brings the canon"

Lee surfaced the long-term posture during this session, contrasting it with the current posture:

> *"Johannes Sigil is constantly gating the conversation with 'bring something' — that is the current posture, the reader has to bring the text, but the ultimate goal here, is that Sigil brings the text, brings the conversation to the canon. That will require creating embeddings, just like we did for cha, allowing rag over it, it will require embeddings to the primary texts in the canon. It's dusk direction — the reader can bring, but Sigil also brings. Sigil is specifically the intermediary between the reader and canon."*

The data prep this session lays the groundwork. The canon-stars schema is shaped to receive `vectors` as a sibling field once the embedding pipeline runs. The source directories exist; they're empty until text content arrives. The embedding script will mirror `scripts/regenerate_rag.py`'s pattern: read `canon-stars.json`, locate the text content in each source directory, run sentence-transformer embeddings, write `rag/canon-vectors.json` (or similar).

The Sigil-side wiring (a `search_canon` tool analogous to `search_archive`, a `fetch_canon_text` tool analogous to `fetch_axn`) is deferred per Lee's "no design iteration until deploys clear" directive.

### Why this matters

The contrast Lee is naming is not a feature request — it's a structural inversion of what Sigil does. Right now Sigil is a guide who refuses to lead until the witness has named a text. The future posture: Sigil is an intermediary who can bring a text *to* the conversation based on what the witness is asking. The witness retains agency to bring their own; Sigil gains the capacity to also bring. This is what the canon-on-canon-stars data layer was always for — not for visualization first, but for retrievability.

### Vercel rate-limit observation (operational, not architectural)

Lee observed the systemic parallel: the deploy rate limit is the same shape as Zenodo's spam classifier — classifier-mediated platform governance, applied in bulk, no recourse, no transparency about training data. The Wound Gauge framework names this pattern. Vercel's is milder than Zenodo's was (no permanent deletion, just a 24-hour cooldown), but the shape is identical. The book-throttle fix (I-2) is in part a defense against this: stop generating noise commits that the platform can't distinguish from spam.

---

## DEPLOY STATE AT SESSION-END

Production at session-start: `25895a8` (book-append turn 13 from 03:36 UTC). Carried Voice Protocol and Shakespeare unhook via ancestry.

Production at session-end (after rate-limit clears): `ea2ee86` (the prep-canon-data merge). Will land everything between as a single deploy.

Branches still alive (not yet deleted post-merge):
- `fix/book-throttle` — merged via `68cde52`
- `sigil-deep-fetch` — merged via `4269632`
- `fix/metadata-sync` — merged via `52cf20a`
- `fix/book-capture-and-support-cha` — merged via `9d6a573`
- `populate-canon-stars` — merged via `4be96b5`
- `prep-canon-data` — merged via `ea2ee86`
- `sigil-historiography` — merged via `a19170c`
- `sigil-presence-patch` — merged via `cf00da5` (single commit, no merge commit)
- `sigil-light-tweaks` — merged via `72ab177`
- `shakespeare-unhook` — merged via `1c5caf7`
- `sigil-search-upgrade` — merged via `cc8afc1`
- `sigil-voice-protocol` — merged via `4251ca2`
- `seismograph-init` — NOT MERGED (scaffold-only, holding for adjudication)

Auto-retry expected around 04:09 UTC on 2026-06-30.

---

## FILES THIS SESSION TOUCHED

**Modified:**
- `api/sigil.py` — major changes (Voice/Presence Protocol, RETRIEVAL DISCIPLINE, search upgrade, deep-fetch tool, four-strand braid wiring)
- `api/book.py` — capture-before-Sigil, race fix on index update, [skip ci] tags
- `chat.js` — capture flow restructured, Support CHA inline element
- `styles.css` — Support CHA mobile-visible
- `index.html` — Support CHA placement
- `vercel-ignore-build.sh` — shallow-clone-aware, -m flag for merges
- `scripts/regenerate_rag.py` — deposit_number from source registry
- `data/canon-sky/canon-stars.json` — 7 → 76 entries + schema reconciliation
- `data/canon-sky/heteronyms.json` — zodiacal_sign_id added
- `rag/metadata.json` — regenerated by workflow with correct deposit_numbers

**Created:**
- `/specs/EA-MANDALA-VOICE-01_v0_1_DRAFT.md`
- `/specs/EA-MANDALA-PRESENCE-01_v0_1_DRAFT.md`
- `rag/historiography.md`
- `rag/refraction.md`
- `rag/memographics.md`
- `rag/personal-undertow.md`
- `scripts/populate_canon_stars.py`
- `data/canon-sky/canon-edges.json`
- 62 source stub directories under `/sources/<id>/` with `metadata.json`
- `UPDATES_REGISTER_2026-06-29.md` (this file)

**Unchanged from start of session (intentionally):**
- `starmap/manifests/canonical-declarations.md` (modified only by V-3 Shakespeare unhook)
- `/sky/stars.json`, `/sky/zodiac.json`, `/sky/planets.json` (sky infrastructure data)
- `/data/canon-sky/substrates.json` (the Septad — already complete)

---

*This register is the granular companion to the 2026-06-29 update section in WORKPLAN.md. It carries decisions; the WORKPLAN carries direction.*
