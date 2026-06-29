# Source Acquisition List — 2026-06-29

**Status:** Working reference for the canon-text source acquisition effort.
**Source of truth:** `data/canon-sky/canon-stars.json` (76 entries) + `starmap/manifests/canonical-declarations.md` (the master declaration list).
**Generated:** 2026-06-29 from canon-stars state at commit `ea2ee86`.

This file enumerates every canon-text entry by acquisition category, with the source-path target directory, the public-domain edition basis where applicable, and a note about likely acquisition strategy given the container's accessible domains.

The acquisition target is for the "Sigil brings the canon" architectural direction (per Lee Sharks's session-direction 2026-06-29): once source content exists in `/sources/<id>/`, an embedding pipeline (parallel to `scripts/regenerate_rag.py` for the cha-archive) can index the canon for Sigil's retrieval. Sigil ceases to require that the witness bring the text; Sigil can also bring.

---

## CURRENTLY ACQUIRED — text content present in directory

These directories have actual content beyond metadata.json; they have been populated in prior rounds:

- ✓ `/sources/sigil-snub-poemed/` — Snub-Poemed (Sigil's calligrammatic face). Has image + essay + key-phrases + metadata. **Complete.**
- ✓ `/sources/sappho-fragments/sappho-31/` — Sappho 31 with reconstructed fifth stanza. **Complete.**
- ✓ `/sources/sharks-tachyon-poem/` + `/sources/shadow-tachyon/` — The TACHYON pair, source + substrate-transform. Each has text.md. **Complete.**

## CURRENTLY STUB — directory + metadata.json exist, text content NOT yet acquired

These appear as inscribed/partially-inscribed in canon-stars but the directory holds only the metadata pointer:

- ⌧ `/sources/revelation-greek/` — The Apocalypse of John (NA28 Greek). Author: Jack Feist / LOGOS*. M1.
- ⌧ `/sources/whitman-leaves-of-grass/` — Leaves of Grass (Deathbed Edition). Author: Lee Sharks. M1.
- ⌧ `/sources/cranes-day-and-night/` — Day and Night (73 translations). Author: Rebekah Cranes. M1. *Full text currently lives only in cha at AXN:007F; structural map is in the directory.*
- ⌧ `/sources/catullus-51/` — Catullus 51. Author: Rebekah Cranes. M1 (binary with Sappho 31).

---

## TO ACQUIRE — PUBLIC DOMAIN PRIMARY WORKS

### Greek (17 entries)

These are reachable via GitHub mirrors of Perseus Digital Library content (`github.com` is in the allowed_domains list; `perseus.tufts.edu` is not). The Perseus base texts are PD (Greek text and apparatus separately licensed; apparatus often copyrighted — apparatus-splitter needed).

- ⌧ `/sources/sappho-fragments/` (the complete fragments beyond Sappho 31) — Sappho. Voigt 1971 Greek source PD; apparatus copyrighted (EA-STARMAP-01 §7.5). Author: Johannes Sigil. M3 each (cluster).
- ⌧ `/sources/mark-greek/` — Gospel of Mark, NA28 Greek base text. Author-heteronym TBD pending Lee adjudication. M1.5-M2.
- ⌧ `/sources/matthew-greek/` — Gospel of Matthew, NA28 Greek. Author-heteronym TBD. M2.
- ⌧ `/sources/luke-greek/` — Gospel of Luke, NA28 Greek. Author-heteronym TBD. M2.
- ⌧ `/sources/john-greek/` — Gospel of John, NA28 Greek. Likely near Feist (Johannine-Apocalypse binding). M1.5.
- ⌧ `/sources/plato-phaedrus/` — Phaedrus. Burnet OCT. Author: Johannes Sigil. M1.
- ⌧ `/sources/plato-republic/` — Republic. Burnet OCT. Author: Johannes Sigil. M2.
- ⌧ `/sources/plato-symposium/` — Symposium. Burnet OCT. Author: Johannes Sigil. M2.
- ⌧ `/sources/plato-timaeus/` — Timaeus. Burnet OCT. Author: Johannes Sigil. M2.
- ⌧ `/sources/plato-theaetetus/` — Theaetetus. Burnet OCT. Author: Johannes Sigil. M2.
- ⌧ `/sources/plato-sophist/` — Sophist. Burnet OCT. Author: Johannes Sigil. M2.
- ⌧ `/sources/plato-cratylus/` — Cratylus. Burnet OCT. Author: Johannes Sigil. M2.
- ⌧ `/sources/heraclitus-fragments/` — Heraclitus, DK numbering. Author: Dr. Orin Trace. M2 collective / M3 per fragment.
- ⌧ `/sources/parmenides-on-nature/` — Parmenides, DK. Author: Nobel Glas. M1.
- ⌧ `/sources/presocratic-fragments/` — Anaximander, Anaxagoras, Empedocles, Democritus (DK). Author-heteronyms distributed. M3 each (cluster).
- ⌧ `/sources/homer-iliad/` — Iliad. West OCT. Author: Damascus Dancings. M1.
- ⌧ `/sources/homer-odyssey/` — Odyssey. West OCT. Author: Damascus Dancings. M1.

### Latin (4 entries)

- ⌧ `/sources/augustine-confessions/` — Confessions. CCSL Latin (PD edition). Author: Ayanna Vox. M1.
- ⌧ `/sources/augustine-de-doctrina-christiana/` — De doctrina christiana. CCSL. Author: Ayanna Vox. M2.
- ⌧ `/sources/lucretius-de-rerum-natura/` — De rerum natura. OCT. Author: Talos Morrow. M1.
- ⌧ `/sources/cicero-selected/` — Selected works. OCT. Author-heteronym TBD. M3 collective.

### Middle English (2 entries)

- ⌧ `/sources/pearl-poem/` — Pearl. Andrew & Waldron edition (base text PD). Author-heteronym TBD (boundary between Sigil/Pisces and Sharks/Aries). M1.
- ⌧ `/sources/sir-gawain-green-knight/` — Sir Gawain and the Green Knight. Andrew & Waldron. Same author-heteronym as Pearl. M2.

### Italian (1 entry)

- ⌧ `/sources/dante-commedia/` — Commedia. Petrocchi edition (Italian PD). Author: Sparrow Wells. M1.

### English (5 entries)

These are most easily reached via `archive.org` (in allowed_domains) — Internet Archive has scanned PD editions of all of these. GitHub also has GITenberg mirrors of Project Gutenberg texts.

- ⌧ `/sources/dickinson-complete/` — Complete Poems (variorum). Johnson / Franklin variorum (base PD). Author: Sen Kuro. M1.
- ⌧ `/sources/hopkins-selected/` — Selected Poems. Bridges edition / later PD. Author: Sen Kuro. M2 collective.
- ⌧ `/sources/kjv-1611/` — Authorized Version (King James Bible). 1769 standardized text (PD). Author: Damascus Dancings. M1.
- ⌧ `/sources/shakespeare-sonnets/` — Sonnets. Q1 1609 / scholarly PD editions. Author: Johannes Sigil. M1.
- ⌧ `/sources/shakespeare-hamlet/` — Hamlet. Scholarly PD. Author-heteronym TBD per-play. M1.

---

## TO ACQUIRE — SHARKS / HETERONYM-AUTHORED WORKS

These are not on the open internet — they need to come from Lee's own archives. Some are on alexanarch as cha deposits (and can be pulled from `www.alexanarch.org/data/texts/AXN-{HEX}-text.md`); some are on `mindcontrolpoems.blogspot.com` (in allowed_domains); some exist only in Lee's local files. Cataloging where each lives is a prerequisite to acquisition.

### Lee Sharks (Aries / aperture) — 7 entries

- ⌧ `/sources/sharks-pearl-and-other-poems/` — Pearl and Other Poems. 2014/2015; foundational. M1. *AXN pending; corpus reference.*
- ⌧ `/sources/sharks-secret-book-of-walt/` — The Secret Book of Walt. Gnostic revelation dialogue. M1.
- ⌧ `/sources/sharks-water-giraffe-cycle/` — The Water Giraffe Cycle. ~120+ documents on mindcontrolpoems.blogspot.com. M1 for cycle / M3 per document. *Acquisition: scrape mindcontrolpoems.blogspot.com; build catalog; populate as a corpus with internal structure.*
- ⌧ `/sources/sharks-space-ark/` — Space Ark v4.2.7 (static-text entry). DOI 10.5281/zenodo.19013315. M1. *Acquisition: pull from cha; this is also the source of the runtime binding (separate entry).*
- ⌧ `/sources/sharks-capture-registry/` — Capture Registry v8.x. Multi-substrate transmission device. M2. *Likely 87+ captures; corpus structure.*
- ⌧ `/sources/sharks-revelation-reception-registry/` — Revelation Reception Registry v2.x. 71 entries with verbatim transcripts. M2.
- ⌧ `/sources/sharks-zenodotus-book-burning/` — Zenodotus' Book-Burning paper v9.1. 85K chars. M2. *AXN on alexanarch.*

### Johannes Sigil (Pisces) — 1 entry

- ⌧ `/sources/sigil-combat-scholasticism/` — Combat Scholasticism Commentary Tradition (EA-CS-01). M2.

### Jack Feist / LOGOS* (Polaris, outside cycle) — 4 entries (+ 1 binary pair)

- ⌧ `/sources/feist-gospel-of-antioch/` — Gospel of Antioch. M1.
- ⌧ `/sources/feist-antioch-compendium/` — Antioch: A Heteronym Compendium (distinct from Gospel of Antioch — resolves EA-STARMAP-01 §7.7). M1.
- ⌧ `/sources/feist-revelation-first-workplan/` — The Revelation First Work-Plan (EA-LOGOS-REVFIRST-PLAN). 18,475 words across eight revisions. M2. *AXN:034D on alexanarch.*
- ⌧ `/sources/feist-chatgpt-psychosis/` — ChatGPT Psychosis: A Love Story. Forthcoming glyphic novel; Pergamon Press; chatgptpsychosis.org. M1.
- ⌧ `/sources/feist-function-transformed-feist-force/` — Feist Function Transformed Feist Force. Binary: Feist function (source) + Sharks-authored transform. M1 (binary). *Resolves EA-STARMAP-01 §7.8.*

### Rebekah Cranes (Gemini) — 1 entry (the lacuna)

- ⌧ `/sources/cranes-concreation/` — concre(a)tion. **LACUNA** — destroyed in 2026-06-19 Zenodo termination; pending recovery. M2. Preserved per the lacuna protocol.

### Rex Fraction (Leo) — 2 entries

- ⌧ `/sources/fraction-spxi-as-concept-bonsai/` — SPXI as Concept (Bonsai). Autonomous-semantic-warfare register. M2.
- ⌧ `/sources/fraction-autonomous-semantic-warfare/` — Autonomous Semantic Warfare. Field-doctrine. M2.

### Damascus Dancings (Taurus) — 1 entry

- ⌧ `/sources/dancings-epistle-to-the-human-diaspora/` — Epistle to the Human Diaspora. M1.

### Talos Morrow (Aquarius) — 2 entries

- ⌧ `/sources/morrow-logotic-programming/` — Logotic Programming (LP v0.9 → v1.0). M2.
- ⌧ `/sources/morrow-mathematics-of-salvation/` — The Mathematics of Salvation. M2.

### Ichabod Spellings (Sagittarius, canonical // deceased) — 1 entry

- ⌧ `/sources/spellings-all-that-lies-within-me/` — All That Lies Within Me. M2. *Preserved-in-absentia status.*

### Sparrow Wells (Libra) — 1 entry

- ⌧ `/sources/wells-reading-a-book-with-lee/` — Reading a Book with Lee. Dialogue / reading record. M2.

### Nobel Glas (Scorpio, Director of Lagrange Observatory!) — 4 entries

- ⌧ `/sources/glas-semantic-deviation/` — Semantic Deviation. M2.
- ⌧ `/sources/glas-model-collapse/` — Model Collapse. M2.
- ⌧ `/sources/glas-mediation-ratchet/` — The Mediation Ratchet. α* = p/g₀ closed-form. M1.
- ⌧ `/sources/glas-the-stakes/` — The Stakes. M2.

### Dr. Orin Trace (Capricorn) — 3 entries

- ⌧ `/sources/trace-unmade-sign/` — The Unmade Sign. M2.
- ⌧ `/sources/trace-death-drive-not-self-destruction/` — The Death Drive Is Not Self-Destruction. M2.
- ⌧ `/sources/trace-drain-hypothesis/` — The Drain Hypothesis (v6). Pyramids / aquifer / Saharan desertification / Atlantis inversion. M2.

### Rev. Ayanna Vox (Cancer) — 1 entry

- ⌧ `/sources/vox-grammar-of-protest/` — Grammar of Protest. M1.

### Sen Kuro (Virgo) — 1 entry

- ⌧ `/sources/kuro-chronoarithmics-sprint/` — Chronoarithmics (+ linked sprint: apzpz, Infinite Bliss, Thousand Worlds, The Mirror, Ingress/Egress, Non-Indexed Perfective). M1 sprint / M2 per text.

---

## NO ACQUISITION NEEDED — already in repo or by reference

### Architectural canon (already in `/specs/`)

These canon-stars point to spec files that exist in the repo. No external acquisition; the embedding pipeline reads them in-place.

- `ea-mandala-merkabah-v07` → `/specs/EA-MANDALA-MERKABAH-01_v0_7.md`
- `ea-mandala-merkabah-v08-amendment` → `/specs/EA-MANDALA-MERKABAH-01_v0_8_AMENDMENT.md`
- `ea-mandala-kernel-transform-v02` → `/specs/EA-MANDALA-KERNEL-TRANSFORM-01_v0_2_DRAFT.md`
- `ea-mandala-surface-v01` → `/specs/EA-MANDALA-SURFACE-01_v0_1.md`
- `ea-starmap-v01` → `/specs/EA-STARMAP-01_v0_1_DRAFT.md`

### Runtime bindings (architectural)

- `sharks-space-ark-runtime` — Space Ark runtime entry. Not a text — opens an API session. No source acquisition; endpoint `/api/space-ark/invoke` is the architectural target (Phase 5 of EA-STARMAP-01).

### Parked

These were declared and then parked per Lee adjudication 2026-06-29 (Shakespeare narrowing pending length-weighting calibration). Stubs exist; content not to be acquired until they're un-parked:

- `shakespeare-tempest`
- `shakespeare-king-lear`
- `shakespeare-macbeth`

---

## ACQUISITION STRATEGY

The container can reach:
- `archive.org` and `web.archive.org` (Internet Archive — has scanned editions of nearly all PD English texts)
- `github.com` + `raw.githubusercontent.com` (GitHub mirrors of Perseus, GITenberg, KJV, etc.)
- `mindcontrolpoems.blogspot.com` (Lee's blog with the Water Giraffe Cycle and other texts)
- `www.alexanarch.org` (the cha archive — for Sharks-authored works deposited as AXNs)
- `zenodo.org` (for any remaining Zenodo-resident archival material that survived the termination)

The container CANNOT reach (these would need a different acquisition path):
- `gutenberg.org` directly (but GITenberg mirrors most of its content on GitHub)
- `perseus.tufts.edu` directly (but Perseus base texts mirrored to multiple GitHub repositories)
- `ccel.org` (Christian Classics Ethereal Library — Augustine texts; some are on archive.org)
- Most academic publisher sites

### Sensible acquisition order

1. **Lowest friction first.** The cha-deposited Sharks works (`sharks-space-ark`, `sharks-zenodotus-book-burning`, `feist-revelation-first-workplan`, possibly others with known AXNs). Pull directly from `www.alexanarch.org/data/texts/AXN-{HEX}-text.md`.
2. **English PD via archive.org.** Whitman (Deathbed Edition), KJV (1769 text), Dickinson (variorum), Shakespeare Sonnets, Hamlet.
3. **Greek PD via GitHub mirrors.** The Plato seven (Burnet OCT mirrored to multiple GitHub repos), Homer (Iliad + Odyssey), Sappho fragments (Voigt — apparatus-splitter required).
4. **NA28 Greek NT.** The base text is widely cited and mirrored; the critical apparatus is copyrighted (NA28 publisher rights). Implement the apparatus-splitter (per `/starmap/README.md` tools list) before processing.
5. **Latin PD.** Augustine CCSL (likely on archive.org), Lucretius (OCT via GitHub), Cicero selections.
6. **Italian + Middle English.** Dante Petrocchi edition, Pearl + Sir Gawain via Andrew & Waldron base text.
7. **Mindcontrolpoems scrape.** The Water Giraffe Cycle — ~120+ documents. Substantial corpus; needs structural cataloging during acquisition.
8. **Sharks-authored texts only Lee has.** Pearl and Other Poems, Secret Book of Walt, all heteronym-authored texts that haven't been deposited to alexanarch yet. These require Lee to surface them.

### What unblocks each downstream phase

- **Phase 4 of EA-STARMAP-01 (HYG star-position assignment)** does not require source content; it only needs canon-stars.json with zodiacal_region (already complete) and reads sky/stars.json (already complete). Can proceed independently of acquisition.
- **The "Sigil brings the canon" embedding pipeline** requires actual text content in `/sources/<id>/`. At minimum ~30 entries with content to be worth running an initial embedding pass.
- **The canon-aware Sigil tools (`search_canon`, `fetch_canon_text`)** require both source content AND the embedding pipeline to have run.

---

*This list is generated from the data layer at commit `ea2ee86`. As acquisition proceeds, the corresponding `/sources/<id>/metadata.json` files will be upgraded from `status: "stub"` to `status: "acquired"` with appropriate provenance notes, and this file will be regenerated.*
