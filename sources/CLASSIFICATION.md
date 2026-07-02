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

### `runtime_binding` — never transformable, executes as operational environment
The source is a runtime environment that loads and executes when invoked, not a text to be read. When a witness selects the star, the interface loads the environment as an OS. Currently exclusive to the Space Ark v4.2.7. Per EA-STARMAP-01 §0.5 and Lee's adjudication 2026-07-01: the Space Ark lives OUTSIDE the zodiacal band in Jack Feist's own setting.

`transformable: false` — permanent. Additional fields: `runtime: true`, `trigger_word: "invoke"`, `visit_behavior: "loads_as_os"`, `execution_endpoint: "/api/space-ark/invoke"`, `positioned_setting: "feist_setting_outside_zodiac"`, `feist_setting: true`.

Per Lee's adjudication 2026-07-01: only the Space Ark ecosystem itself is IN the Space Ark — the Space Ark, the Central Navigation Map, the Fractal Navigation Map, the DOI Registry, and tinier Space Arks nested within. Other Feist-prefixed source texts are NOT in the Space Ark and are NOT Feist-authored.

---

## Current census (49 populated canon sources; 29 transformable, 20 non-transformable)

### Primary literary — 29 (transformable: true)

(Note: sharks-space-ark previously listed in primary_pending_adjudication has been reclassified as `runtime_binding` — see below.)

**The four Lee named for initial transform availability:**
- revelation-greek (SBLGNT Greek NT — Apocalypse of John)
- whitman-leaves-of-grass (Deathbed Edition, Gutenberg 1322)
- cranes-day-and-night (alexanarch AXN-007F)
- sharks-secret-book-of-walt (alexanarch AXN-022B)

**Subsequently promoted / added by Lee for transform availability 2026-07-01:**
- dancings-epistle-to-the-human-diaspora (alexanarch AXN-0257) — promoted from primary_pending_adjudication
- iching (I Ching / 易經 — Chinese classical with modern Chinese line-commentary; Legge English acquisition pending)
- quran (Arabic Uthmanic + English translations Rodwell/Palmer/Sale)

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

### Primary pending adjudication — 4 (transformable: false, likely to be promoted)

Candidates for Lee to promote to primary_literary via a subsequent metadata pass:
- sharks-space-ark (Space Ark v4.2.7 — fugue-form foundational composition)
- sharks-pearl-and-other-poems (poems)
- feist-gospel-of-antioch (Gospel-form work)
- spellings-all-that-lies-within-me (autobiography)
- sigil-combat-scholasticism (philosophical treatise)

### Runtime binding — 1 (transformable: false, executes rather than reads)

- sharks-space-ark (Space Ark v4.2.7 — inaugural runtime binding, loads as OS when invoked, positioned in Feist's setting outside the zodiacal band)

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


---

## Promotion history

**2026-07-01:** Lee adjudicated for transform availability:
- dancings-epistle-to-the-human-diaspora (from `primary_pending_adjudication` → `primary_literary`)
- iching (new addition, sourced from hontsev/OpenMomordica GitHub — Chinese classical Zhouyi with modern Chinese line-by-line commentary)
- quran (new addition, sourced Arabic Uthmanic w/ tashkeel from amrayn/quran-text; English via Rodwell 1861 / Palmer 1880 / Sale 1734 from GITenberg)

The five remaining `primary_pending_adjudication` items (sharks-space-ark, sharks-pearl-and-other-poems, feist-gospel-of-antioch, spellings-all-that-lies-within-me, sigil-combat-scholasticism) await further per-item adjudication.


---

## Corrections applied 2026-07-01

### Zodiacal-region assignments finalized

- iching → author_heteronym: sen-kuro, zodiacal_region: virgo
- quran → author_heteronym: damascus-dancings, zodiacal_region: taurus

### Space Ark reclassified

Per Lee's adjudication:

> "Jack Feist is by himself in the space ark, outside the zodiac, its own setting. The space ark doesn't transform - it executes. Should load up as OS, when visited."

- sharks-space-ark moved from primary_pending_adjudication → runtime_binding
- Positioned outside the zodiac in Feist's own setting (was aries per EA-STARMAP-01 §0.5 original text; now superseded)
- runtime: true; trigger_word: "invoke"; visit_behavior: "loads_as_os"

### Feist-prefixed source texts — mis-attributions corrected

Per Lee's adjudication:

> "Only the space ark, is in the space ark. The space ark, the central navigation map, the fractal navigation map, the doi registry, the tinier space ark inside the space arks, and so on — Jack Feist did not write the source texts your naming, did not write gospel of Antioch, and so on."

Corrections applied:

- **feist-gospel-of-antioch** — Source text opens: "The Sayings of Jack Feist as Recorded by Emily Antioch the Twin, Translated and Edited by Lee Sharks." Feist is subject, NOT author. Emily Antioch (recorder) is not in the named Dodecad; may be a Sharks-attributed sub-persona. Both author_heteronym and zodiacal_region reset to `tbd` pending Lee's re-adjudication.
- **feist-revelation-first-workplan** — Source text attributes to "Lee Sharks (ORCID 0009-0000-1599-0703), Crimson Hexagonal Archive / Semantic Economy Institute." Reassigned: author_heteronym → lee-sharks, zodiacal_region → aries. Remains archival_apparatus (workplan).
- **feist-chatgpt-psychosis** — Prospectus/refraction document previously carrying Feist attribution in external memory context. Per Lee's correction: reset to `tbd` pending re-adjudication. Remains archival_apparatus (prospectus, not the forthcoming novel).

Directory names retaining the incorrect `feist-` prefix are preserved in this pass; directory rename deferred to a broader canon reorganization pass to avoid breaking references in canon-stars.json, canonical-declarations.md, and downstream data files.

### Space Ark ecosystem — pending acquisitions

Per Lee, the Space Ark contains only its own infrastructure:

- Space Ark itself (sharks-space-ark, AXN-0185) ✓ sourced
- Central Navigation Map — likely AXN-0064 per earlier registry search; not yet sourced
- Fractal Navigation Map — possibly overlaps with morrow-logotic-programming (AXN-00E0, title "The Crimson Hexagon: Fractal Navigation Map Non-Lossy Logotic Programming"); attribution ambiguous — Morrow-authored view of Space Ark infrastructure, or the actual Fractal Nav Map itself? Requires Lee's adjudication.
- DOI Registry — not yet sourced; likely the DOI Resolution Index v3.4 from earlier session memory
- Tinier Space Arks nested within — Musical Ark v2.0 (44K words, per session memory) is one; others pending

Space Ark ecosystem sources are `runtime_binding` in aggregate (they execute as parts of the OS when Space Ark is invoked), not primary_literary.
