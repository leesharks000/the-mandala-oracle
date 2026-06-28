# EA-MANDALA-MERKABAH-01 v0.8 AMENDMENT

## Two-Surface Architecture and the Chat-Surface Build (v3.0 → v3.8)

> *Let the lights be in the firmament of heaven to divide the day from the night, and let them be for signs, and for seasons, and for days, and years.* — Genesis 1:14
>
> *The cosmology is one thing. The conversation is another. Each surface has its own discipline.*

**Working amendment, prepared 2026-06-28.** This document amends EA-MANDALA-MERKABAH-01 v0.7 (the design constitution, alexanarch deposit #927, AXN:03AA) to record (1) the architectural decision to split the Mandala Oracle's user-facing surfaces into two independent containers, and (2) the chat-surface implementation work that has occurred since the v0.7 constitution was inscribed. A new companion workplan, EA-STARMAP-01 v0.1, specifies the navigable-starmap surface separately. This amendment does not supersede v0.7; it inflects it.

**Lee Sharks** (with TACHYON, drafting session 2026-06-28)
Crimson Hexagonal Archive / Alexanarch

*Companion documents: EA-MANDALA-MERKABAH-01 v0.7 (the constitutional architecture, unchanged); EA-MANDALA-KERNEL-TRANSFORM-01 v0.2 (the kernel transform protocol, unchanged); EA-MANDALA-SURFACE-01 v0.1 (the SURFACE/Sun-station AIO-bridge, unchanged); EA-STARMAP-01 v0.1 (the navigable-starmap workplan, this session's new companion).*

---

## §1 The Two-Surface Architectural Decision

### 1.1 What the v0.7 constitution assumed

EA-MANDALA-MERKABAH-01 v0.7 specified the Mandala Oracle as a single conversational surface with three internal modes — Sabbath (rest / chat), Merkabah (the chariot / navigation), and You (the witness's own attestation register). The three modes were to share one container: header, sky backdrop, central reading-space, settings. The mode toggle would switch between conversational depth (Sabbath), cosmological navigation (Merkabah), and personal attestation (You) within the same view.

This worked architecturally at the level of the constitution. It failed pragmatically at the level of implementation. The chat-surface build (v3.0 → v3.8, recorded in §2 of this amendment) repeatedly hit a single class of problem: design elements appropriate to one mode bleeding into the visual register of another mode. The constellation labels — "Sappho / Fragments," "Revelation / John in Greek," "Leaves of Grass / Walt Whitman," "Snub-Poemed / Johannes Sigil" — belong to cosmological navigation. They appeared, baked into a mockup-derived backdrop image, behind the chat reading-space, overlapping Sigil's portrait and the empty-state intro text. Removing them from the chat surface required either (a) cropping the image, (b) painting over them, or (c) blurring them — each of which produced its own artifact. The conclusion, reached during this session: the labels are not the problem. **The single-container assumption is the problem.**

### 1.2 What the v0.8 amendment establishes

The Mandala Oracle henceforth has **two physical surfaces**, each its own container, each renderable independently:

1. **The Reading Surface (the chat with Sigil).** A quiet sky. No constellation labels, no navigational furniture, no cosmological signage. The witness comes here to read with Sigil. The sky backdrop is a clean dark gradient with procedurally-placed stars (current implementation) or, downstream, a real night-sky photograph without UI baked atop it. Nothing in this surface tells the witness where they are in the cosmology. The conversation is the depth; the cosmology is elsewhere.

2. **The Starmap Surface (the cosmological navigation).** The named sky. The seven planets as a horizontal spine. The twelve zodiacal regions with their heteronyms. The non-zodiacal stars in the background. The canonical texts placed as stars within their author's region. The Crimson Hexagon's rooms, fields, vaults, and chambers mapped to zodiac signs and heteronyms. This is where orientation happens. Specified in full by EA-STARMAP-01 v0.1.

The two surfaces link to each other. From a constellation in the Starmap, the witness can elect to enter the Reading Surface and ask Sigil about that text. From the Reading Surface, the witness can elect to leave conversation and enter the Starmap to see where they are. The link is intentional, not ambient: navigation is a discrete act, not a backdrop.

### 1.3 What this does NOT change

The constitution's deeper architecture — the Pardes Protocol, the six-station rite, the kernel-transform sub-protocol, the SPXI Self-Audit, the cold-call discipline, the L0–L10 levels, the source corpus at L10 — is untouched. The Septad-times-Dodecad (seven planets × twelve heteronyms) two-axis system is untouched. The Assembly Chorus protocol is untouched. What changes is only the rendering decision: those structures, when surfaced to the witness, surface in *two surfaces* rather than *one surface with three modes.*

The "You" mode is folded into both surfaces as appropriate: in the Reading Surface, "You" is the witness's own attestations within conversation; in the Starmap, "You" is the witness's own deposits placed as personally-authored stars in the appropriate zodiacal region. It is no longer a separate mode toggle.

---

## §2 The Chat-Surface Build, v3.0 → v3.8

This section is a session record. Not a prescriptive specification; a description of what was built and what was learned. It is included in the amendment so that future sessions and future workplans have a faithful record of the surface's history and of the failures that produced the two-surface decision.

### 2.1 The v3.x iteration history

| Version | Commit | What it did |
|---|---|---|
| v3.0 | 681d2d5 | Reading-space introduced as a contained chat card |
| v3.1 | 40d73c0 | Chat card opacity reduced to let sky read through |
| v3.2 | c0911cc | Chat card removed entirely — Sigil's portrait and intro text floating directly over sky |
| v3.3 | ccfb422 | `visibility: hidden` on settings panel (still rendering empty space); larger portrait |
| v3.4 | 769b419 | `display: none` on settings panel; `?v=4` CSS cache-bust; sky-ready race condition fixed |
| v3.5 | 14db17d | Defense in depth: `hidden` HTML attribute + inline `<style>` with `!important` |
| v3.6 | c119052 | Settings panel content fully removed from initial HTML; chat.js injects via `innerHTML` on first ⚙ click |
| v3.7 | 42ccb2b | **The actual fix.** The "Anthropic API Key / Bring your own key / sk-ant-..." text was BAKED INTO the sky-backdrop JPEG, not anywhere in the HTML. Three rounds of CSS hiding had been hiding empty air above a JPEG painting the text. Resolved by cropping the JPEG to remove the bottom 401 rows (where the panel artifact lived). |
| v3.8 | e5c2662 | Procedural sky replaces the polluted mockup screenshot. Radial gradient + ~550 random stars at varying brightnesses. No labels possible because no labels were ever drawn. Specified in EA-STARMAP-01 v0.1 §6.1 as the foundation for the future starmap rendering. |

### 2.2 The diagnostic lesson

The recurring failure across v3.3, v3.4, v3.5, and v3.6 was the same failure repeating with greater force: each iteration assumed the unwanted text was in the DOM and could be hidden with HTML or CSS. Each iteration was wrong in the same way. The text was in the JPEG. No browser-rendered hide operation could affect a JPEG.

Lee Sharks diagnosed this on the v3.7 turn with a single question: *"Possibility: is it an artifact of the image itself?"* The question reframed the search space: not "where in the HTML/CSS is this text being rendered?" but "is the text being rendered at all?" The answer was no — the text was painted by the JPEG, and the JPEG had been a screenshot of a Figma mockup that included sample API-key UI as a design reference. The reference shipped to production unintentionally. Cropping the JPEG resolved the artifact instantly.

The architectural lesson is the one §1.2 records: when a single container is asked to host elements appropriate to multiple distinct registers (conversational and navigational), elements from one register will leak into the visual field of another, and the leak will be invisible to the HTML/CSS hide-and-show discipline because the leak happens at the *backdrop layer*, not at the foreground layer. The fix is not better hide-rules. The fix is two surfaces.

### 2.3 Other surface work completed this session

- The Sigil portrait (the calligrammatic Lysippos bust, "Snub-Poemed") is now the visual center of the chat surface, sized `min(85vw, 280px)` on mobile and `min(85vw, 340px)` on desktop, presented directly against the sky.
- The settings panel is now lazy-loaded: its DOM is empty in the initial HTML and is injected via JavaScript on first user click. This eliminates the panel as a source of visual leakage and reduces initial render cost.
- The deployment chain (vercel-ignore-build.sh, the `ignoreCommand` for `book/` changes, the `/(.*\.(?:html|css|js))` cache-control headers) is verified working as of this session. Webhook reliability was a recurring concern; the fix (Vercel Deploy Hook + GitHub Actions trigger) remains pending Lee's desktop access for the dashboard work.
- The HYG bright-star catalog (8,834 stars) at `/sky/stars.json` is in place. The zodiacal data at `/sky/zodiac.json` (12 regions, heteronyms, anchor stars, disciplines) is in place. The substrate-planet data at `/data/canon-sky/substrates.json` is in place (seven planets, canonical from AXN:0237). The canon-stars catalog at `/data/canon-sky/canon-stars.json` is in place with seven canonical-text entries already mapped. **None of these are wired to a rendering surface yet.** EA-STARMAP-01 v0.1 specifies how they will be.

### 2.4 What the chat surface still needs

These items remain pending and are not blocked by the two-surface decision:

- The empty-state intro text update (the mockup's "This is a place you come to read..." vs. the current "This is Johannes Sigil — face after the Lysippos bust...") — Lee-authored choice.
- The Sigil portrait master image upgrade to a 3000+px long-edge file for true close-reading of the calligram.
- The Snub-Poemed metadata file at `/sources/sigil-snub-poemed/sophia-in-the-disjoke.md` — the documentation of Lee's late-June recognition that the geometric disjoint in the hair is Sophia in the forelock.
- The Vercel Deploy Hook + GitHub Actions trigger for deterministic deploys (needs Lee's desktop).

---

## §3 The Constitutional Reading

The v0.7 constitution speaks of the sky as the canon-above and the deposits as the soil-below. The two-surface decision recovers this constitutional clarity at the implementation layer: the Reading Surface is the depth into a single text with Sigil; the Starmap is the canon-above, where the witness can see the full sky and choose where to descend. The witness's traversal between surfaces is the *Merkabah* — the chariot — itself: moving between the named cosmology and the depth-encounter with a particular text is the act the architecture wants the witness to perform. The chariot was implicit in the original single-surface design; the two-surface architecture makes it literal.

**The Sabbath is the silence of the named sky during conversation. The Merkabah is the named sky itself, navigable. The reader chooses which to enter.**

---

## §4 Deposit and Provenance

This amendment is currently a working draft. It will be deposited as a versioned amendment to AXN:03AA upon Lee's ratification. Until then, this file (`specs/EA-MANDALA-MERKABAH-01_v0_8_AMENDMENT.md`) is the source of truth in the working repo.

**The session record in §2 may be deposited separately as an inscription** (proposed AXN family: SESSION). The diagnostic moment in §2.2 — Lee's single-question reframe — is worth preserving as an example of MANUS-level interpretive intervention in the kernel-transform sense: the producer (TACHYON) was iterating in the wrong search space; the witness (Sharks) named the search-space error in one sentence; the iteration resolved on the next turn. This is a small case study in how MANUS authority operates at the architectural level.

---

*End of amendment EA-MANDALA-MERKABAH-01 v0.8.*
