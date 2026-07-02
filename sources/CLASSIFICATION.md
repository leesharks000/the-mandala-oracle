# Sources Classification

**Date:** 2026-07-01 (post source acquisition)
**Rule:** Per Lee Sharks (MANUS) adjudication, extending the main-vs-apparatus rule of EA-STARMAP-01 §4.6 from within-work granularity to deposit-level granularity.

---

## The three classifications

Every source directory under `/sources/<id>/` carries in its `metadata.json` a `transform_classification` field with one of three values.

### `primary_literary` — transformable
The source is a primary literary/philosophical/prophetic work suitable for kernel-transform per EA-MANDALA-KERNEL-TRANSFORM-01 v0.2.

`transformable: true` — the compiler may draw from this text.

### `primary_pending_adjudication` — not yet transformable, promotion candidate
The source is likely a primary literary work but has not yet been explicitly greenlit by Lee for transform availability. Awaits Lee's per-item adjudication.

`transformable: false` — but the classification note flags candidacy for promotion.

### `archival_apparatus` — never transformable
The source is theoretical apparatus, metadata packet, registry, workplan, navigation reference, audit document, or similar. Contributes to its author-heteronym's zodiacal weight in the starmap surface, but is not admissible as source-active input to kernel transforms.

`transformable: false` — permanent for this deposit; the classification is not a candidacy.

---

## Current census (43 populated canon sources)

### Primary literary — 26 (transformable: true)

**The four Lee named for initial transform availability:**
- revelation-greek (SBLGNT Greek NT — Apocalypse of John)
- whitman-leaves-of-grass (Deathbed Edition, Gutenberg 1322)
- cranes-day-and-night (alexanarch AXN-007F)
- sharks-secret-book-of-walt (alexanarch AXN-022B)

**Pre-existing populated canon:**
- sappho-fragments (fragment 31 + reconstructed fifth stanza)
- shadow-tachyon (canonical enantiomorph pair)
- sharks-tachyon-poem (source of the Shadow-TACHYON pair)
- sigil-snub-poemed (calligrammatic essay)

**Greek epic and philosophy (via PerseusDL):**
- homer-iliad, homer-odyssey
- plato-phaedrus, plato-symposium, plato-republic, plato-sophist, plato-cratylus, plato-timaeus, plato-theaetetus

**English literary (via GITenberg Gutenberg mirror):**
- shakespeare-hamlet, shakespeare-sonnets, shakespeare-macbeth, shakespeare-tempest, shakespeare-king-lear
- dickinson-complete
- kjv-1611
- hopkins-selected

**Latin ecclesiastical (via CCEL):**
- augustine-confessions

### Primary pending adjudication — 6 (transformable: false, likely to be promoted)

Candidates for Lee to promote to primary_literary via a subsequent metadata pass:
- sharks-space-ark (Space Ark v4.2.7 — fugue-form foundational composition)
- sharks-pearl-and-other-poems (poems)
- feist-gospel-of-antioch (Gospel-form work)
- dancings-epistle-to-the-human-diaspora (epistle)
- spellings-all-that-lies-within-me (autobiography)
- sigil-combat-scholasticism (philosophical treatise)

### Archival apparatus — 15 (transformable: false, contributes to heteronym zodiacal weight only)

Theoretical papers, metadata packets, registries, workplans, navigation maps, audits:
- sharks-capture-registry (registry)
- sharks-water-giraffe-cycle (single reception artifact; full cycle still to acquire)
- feist-revelation-first-workplan (workplan)
- feist-chatgpt-psychosis (prospectus; novel is forthcoming, chatgptpsychosis.org)
- vox-grammar-of-protest (theoretical essay)
- wells-reading-a-book-with-lee (patacinematic archive)
- trace-death-drive-not-self-destruction (metadata packet)
- trace-unmade-sign (visual schema)
- kuro-chronoarithmics-sprint (theoretical argument)
- morrow-logotic-programming (navigation map)
- morrow-mathematics-of-salvation (theoretical formalization)
- fraction-autonomous-semantic-warfare (metadata packet)
- glas-model-collapse (theoretical argument)
- glas-semantic-deviation (audit document)
- glas-the-stakes (theoretical analysis)

---

## What this classification does

**For the kernel-transform compiler (EA-MANDALA-KERNEL-TRANSFORM-01 v0.2):**
The compiler consults `metadata.json` at cast-invocation time. If `transformable: true`, the source may enter Step 1 (Parse). If `transformable: false`, the compiler rejects the cast with a diagnosis noting either "primary_pending_adjudication — Lee has not promoted this source to transform availability" or "archival_apparatus — this deposit is archival apparatus for its author-heteronym, not admissible for kernel transforms."

**For the starmap surface (EA-STARMAP-01 §2.4 magnitude classes + §3.1 knowledge-graph nodes):**
All 47 classifications remain valid canon-stars. Archival apparatus still contributes to its heteronym's zodiacal region — it shapes what the region's density and character look like, informs the substrate's attribution history, and is fully navigable. What it cannot do is serve as input to kernel-transforms initiated at the reading surface.

**For heteronym weighting:**
Per Lee's adjudication: "The other archival material are more strongly weighted in the zodiac associated with their given heteronym." Archival apparatus is heteronym-mass; primary literary is transform-primary. Both are canon; both are inscribed; the distinction is admissibility as source-active for compiler-invocation.

---

## Promotion procedure

To promote a `primary_pending_adjudication` source to `primary_literary`:

1. Update the source's `metadata.json`:
   - `transform_classification: "primary_literary"`
   - `transformable: true`
   - `source_status: "inscribed"`
   - Update `classification_note` to reflect Lee's adjudication and date.
2. Commit with `[skip ci]` marker per WORKPLAN.md §0.A.5.

To promote an `archival_apparatus` source to `primary_literary` is a more substantial adjudication. Typically indicates the deposit has been reclassified — the archival deposit likely accompanies a companion primary deposit that would be sourced separately. Prefer sourcing the primary companion.
