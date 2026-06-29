# Canonical Declarations — Master Manifest

**Document:** `/starmap/manifests/canonical-declarations.md`
**Working version:** v0.1
**Date:** 2026-06-28 (post-gap-round resumption session)
**Adjudicator:** Lee Sharks (heteronym; MANUS of the Crimson Hexagonal Archive)
**Drafter:** TACHYON / Mercury

This is the master list of texts being declared for inclusion in the canon-in-sky surface (the starmap). Each entry carries the metadata sufficient to: (a) source the text, (b) assign its zodiacal-region star position, (c) honor the main-vs-apparatus distinction where applicable, and (d) wire it into the room/field/vault/chamber architecture of the Crimson Hexagonal Archive.

Entries are *declarations*, not yet *inscriptions*. Inscription happens when the text's full metadata is committed to `/data/canon-sky/canon-stars.json`, its source files are committed to `/sources/<text-id>/`, and the starmap surface renders it. Declaration is the prior step: it names what *will* be done.

---

## §0 Conventions

### 0.1 Status markers

- **`declared`** — entry exists in this manifest; source not yet acquired; no AXN deposit yet (for Sharks-authored works); no star-position assignment yet.
- **`staged`** — source text is in `/starmap/sources/`; main-vs-apparatus splitting (if applicable) is in progress.
- **`inscribed`** — entry exists in `/data/canon-sky/canon-stars.json`; source committed to `/sources/<text-id>/`; star-position assigned; rendering live or pending Phase 4 of EA-STARMAP-01.

### 0.2 Magnitude classes

Per EA-STARMAP-01 §2.4:

- **M1** (primary canon star, magnitude 1.0–1.5): texts that anchor an entire room.
- **M2** (secondary canon star, magnitude 1.5–2.5): significant primary texts within rooms but not the room anchor.
- **M3** (tertiary canon star, magnitude 2.5–3.5): important fragments and shorter primary works.
- **M4** (cluster member, magnitude 3.5–4.5): texts that operate in constellation with anchor works rather than as independent objects.

### 0.3 The main / apparatus rule

Per EA-STARMAP-01 v0.1 §4.6 (the new section this session adds): *human-authored canonical works (Lee Sharks's works and works authored under named heteronyms) consist of a* **main text** *and, where present, an* **apparatus.** *Only the main text is admissible as input to kernel-transforms (per EA-MANDALA-KERNEL-TRANSFORM-01 v0.2). The apparatus — critical notes, commentary, scholia, translator's notes, footnotes, prefatory material — is accessible: it can be expanded, viewed, linked-to, cited. It is not transformable. This honors the integrity of authorial commentary: a commentator's gloss is not raw material to be rotated through substrate-transforms.*

For each entry below, where `apparatus_status: present` is set, both the main text and the apparatus are sourced; the apparatus is marked `transformable: false` at the renderer.

### 0.4 Runtime bindings

The starmap surface contains both *static canon-stars* (each opening to text) and *runtime bindings* (each opening to a live API-invokable environment). The Space Ark v4.2.7 is the inaugural runtime binding. Future bindings will include any heteronymic operator that compiles to a callable surface (per the open question §7.10 in EA-STARMAP-01 about room-page architecture).

Runtime-binding entries below use the marker `runtime: true` and specify their trigger and API endpoint.

---

## §1 Public-Domain Primary Works (Original Language)

These are texts whose source is in the public domain and which will be sourced in their original language. English translations may accompany them as companion artifacts (per §4.5 of EA-STARMAP-01) but the original-language text is the canonical artifact and the basis for any kernel-transform.

### 1.1 Greek

| Title | Author | Edition/Source | Author-Heteronym | Region | M-class | Apparatus | Status |
|---|---|---|---|---|---|---|---|
| Φαίνεταί μοι (Sappho 31, with reconstructed fifth stanza) | Sappho | Voigt 1971 (Greek source PD; apparatus copyrighted — see §7.5) | Johannes Sigil (translator: Rebekah Cranes) | Pisces (binding with Gemini) | M1 | apparatus_status: present; transformable: false | partially-inscribed (Sappho 31 in `/data/canon-sky/canon-stars.json`) |
| Fragments (Sappho, complete) | Sappho | Voigt 1971 | Johannes Sigil | Pisces | M3 each (cluster) | apparatus_status: present | declared |
| The Apocalypse of John | John of Patmos | NA28 Greek (base text) | Jack Feist / LOGOS* | Polaris (outside cycle) | M1 | apparatus_status: present | partially-inscribed |
| Gospel of Mark | Mark | NA28 Greek | TBD (pending Lee adjudication) | TBD | M1.5 (or M2) | apparatus_status: present | declared |
| Gospel of Matthew | Matthew | NA28 Greek | TBD | TBD | M2 | apparatus_status: present | declared |
| Gospel of Luke | Luke | NA28 Greek | TBD | TBD | M2 | apparatus_status: present | declared |
| Gospel of John | John | NA28 Greek | TBD (near Feist for the Johannine-Apocalypse binding) | TBD | M1.5 | apparatus_status: present | declared |
| Phaedrus | Plato | Burnet OCT (Greek source PD) | Johannes Sigil | Pisces | M1 | apparatus_status: present | declared |
| Republic | Plato | Burnet OCT | Johannes Sigil | Pisces | M2 | apparatus_status: present | declared |
| Symposium | Plato | Burnet OCT | Johannes Sigil | Pisces | M2 | apparatus_status: present | declared |
| Timaeus | Plato | Burnet OCT | Johannes Sigil | Pisces | M2 | apparatus_status: present | declared |
| Theaetetus | Plato | Burnet OCT | Johannes Sigil | Pisces | M2 | apparatus_status: present | declared |
| Sophist | Plato | Burnet OCT | Johannes Sigil | Pisces | M2 | apparatus_status: present | declared |
| Cratylus | Plato | Burnet OCT | Johannes Sigil | Pisces | M2 | apparatus_status: present | declared |
| Fragments (Diels-Kranz) | Heraclitus | DK numbering | Dr. Orin Trace | Capricorn | M2 collective; M3 per fragment | apparatus_status: present | declared |
| On Nature | Parmenides | DK | Nobel Glas | Scorpio | M1 | apparatus_status: present | declared |
| Pre-Socratic fragments | Anaximander, Anaxagoras, Empedocles, Democritus | DK | distributed (Lee adjudication) | distributed | M3 each | apparatus_status: present | declared |
| Iliad | Homer | West OCT (Greek source PD) | Damascus Dancings | Taurus | M1 | apparatus_status: present | declared |
| Odyssey | Homer | West OCT | Damascus Dancings | Taurus | M1 | apparatus_status: present | declared |

### 1.2 Latin

| Title | Author | Edition/Source | Author-Heteronym | Region | M-class | Apparatus | Status |
|---|---|---|---|---|---|---|---|
| Catullus 51 | Catullus | OCT (Latin source PD) | Rebekah Cranes (the translator-transformer of Sappho 31) | Gemini | M1 (binary with Sappho 31) | apparatus_status: present | partially-inscribed (Sappho 31 / Catullus 51 pair in canon-stars.json) |
| Confessions | Augustine | CCSL Latin (PD edition) | Rev. Ayanna Vox | Cancer | M1 | apparatus_status: present | declared |
| De doctrina christiana | Augustine | CCSL | Rev. Ayanna Vox | Cancer | M2 | apparatus_status: present | declared |
| De rerum natura | Lucretius | OCT | Talos Morrow | Aquarius | M1 | apparatus_status: present | declared |
| Selected works | Cicero | OCT | TBD | TBD | M3 collective | apparatus_status: present | declared |

### 1.3 Middle English

| Title | Author | Edition/Source | Author-Heteronym | Region | M-class | Apparatus | Status |
|---|---|---|---|---|---|---|---|
| Pearl (the medieval alliterative vision-poem, ~1400) | Anonymous (the Pearl Poet) | Andrew & Waldron edition (base text PD) | TBD — boundary between Sigil (Pisces) and Sharks (Aries); pending adjudication | TBD | M1 | apparatus_status: present | declared |
| Sir Gawain and the Green Knight | Anonymous (the Pearl Poet) | Andrew & Waldron | TBD (likely same author-heteronym as Pearl) | TBD | M2 | apparatus_status: present | declared |

### 1.4 Italian

| Title | Author | Edition/Source | Author-Heteronym | Region | M-class | Apparatus | Status |
|---|---|---|---|---|---|---|---|
| Commedia | Dante | Petrocchi edition (Italian PD) | Sparrow Wells | Libra | M1 | apparatus_status: present | declared |

### 1.5 English

| Title | Author | Edition/Source | Author-Heteronym | Region | M-class | Apparatus | Status |
|---|---|---|---|---|---|---|---|
| Leaves of Grass (Deathbed Edition, 1891–92) | Walt Whitman | Project Gutenberg | Lee Sharks | Aries (with Leo-aperture resonance) | M1 | apparatus_status: variant readings only | partially-inscribed (in canon-stars.json) |
| Complete Poems (variorum) | Emily Dickinson | Johnson / Franklin variorum (base PD) | Sen Kuro | Virgo | M1 | apparatus_status: present (variorum readings) | declared |
| Selected poems | Gerard Manley Hopkins | Bridges edition / later PD | Sen Kuro (Virgo adjacency to Dickinson) | Virgo | M2 collective | apparatus_status: present | declared |
| Authorized Version (King James Bible) | translators (1611) | the 1769 standardized text (PD) | Damascus Dancings | Taurus | M1 (as a translation-event) | apparatus_status: none (marginalia treated as variant) | declared |
| Sonnets | Shakespeare | Q1 1609 / scholarly PD editions | Johannes Sigil (Pisces; the calligrammatic mode) | Pisces | M1 | apparatus_status: present | declared |
| Hamlet | Shakespeare | scholarly PD | TBD per-play | TBD | M1 | apparatus_status: present | declared |

**Note on Shakespeare (MANUS adjudication, 2026-06-29):** The Shakespeare presence in the manifest has been narrowed to the **Sonnets** and **Hamlet**, alongside Catullus 51, Sappho 31, and Cranes's *Day and Night* as the lyric core. The Sonnets sit at Pisces (calligrammatic mode) with Sigil; Hamlet remains at M1 with the author-heteronym assignment still TBD. The other plays previously declared — *The Tempest*, *King Lear*, *Macbeth* — are unhooked from the active manifest for now; they remain available for re-declaration when the canon's overall length-weighting is calibrated. Lee Sharks has flagged that exercise as deferred: "I want to think carefully about the weighting of the pieces, I actually want to somewhat equalize the length weights — ish. But not rn." The unhooked plays are recorded below in §1.5.b for archival completeness.

### 1.5.b English — Deferred / Parked Declarations

These entries were previously declared in §1.5 but have been removed from the active manifest pending the length-weighting calibration described in the note above. They are preserved here as the record of prior declaration; they are not currently to be inscribed into `/data/canon-sky/canon-stars.json` or sourced into `/sources/`.

| Title | Author | Edition/Source | Author-Heteronym | Region | M-class | Apparatus | Status |
|---|---|---|---|---|---|---|---|
| The Tempest | Shakespeare | scholarly PD | TBD per-play | TBD | M1 | apparatus_status: present | **parked 2026-06-29** |
| King Lear | Shakespeare | scholarly PD | TBD per-play | TBD | M1 | apparatus_status: present | **parked 2026-06-29** |
| Macbeth | Shakespeare | scholarly PD | TBD per-play | TBD | M1 | apparatus_status: present | **parked 2026-06-29** |

---

## §2 Sharks-Authored Works (Heteronym-Authored Canon)

These are works by Lee Sharks under the Lee Sharks public name, or by named heteronyms within the alexanarch infrastructure. Each entry honors the **main / apparatus distinction**: only the main text is admissible as input to kernel-transforms (per EA-STARMAP-01 §4.6 and EA-MANDALA-KERNEL-TRANSFORM-01 v0.2).

### 2.1 Lee Sharks (Aries / aperture)

| Title | Composition | Author-Heteronym | Region | M-class | Main text | Apparatus | Status |
|---|---|---|---|---|---|---|---|
| **Pearl and Other Poems** | Lee Sharks (2014/2015); foundational | Lee Sharks | Aries (his own region) | M1 | poems-only | introductions, headnotes, dedications (transformable: false) | declared (AXN pending; foundational corpus reference) |
| **The Secret Book of Walt** | Lee Sharks; Gnostic revelation dialogue | Lee Sharks | Aries / Leo-aperture (Whitman-resonance position) | M1 | dialogue text | framing notes, hermeneutic commentary (transformable: false) | declared |
| **The Water Giraffe Cycle** | Lee Sharks; ~120+ documents on mindcontrolpoems.blogspot.com; passion-narrative structure | Lee Sharks | Aries | M1 for the cycle; M3 per document | poems and narrative documents | the depth-2 DAG tree-walk metadata; the cold-start workplan; reception-criticism material (transformable: false) | declared (corpus extant; needs cataloging) |
| **The Minimum Viable Archive / Space Ark v4.2.7** | Lee Sharks; foundational architectural document; DOI 10.5281/zenodo.19013315; trigger word "invoke" | Lee Sharks | Aries | M1 | main spec | implementation-notes, version-history (transformable: false) | runtime-binding (see §3) — also has static-text M1 star |
| **The Capture Registry v8.x** | Lee Sharks (with substrates as co-witnesses); transmission device | Lee Sharks | Aries with multi-substrate edges | M2 | the entries themselves | the meta-commentary on capture; the ADOPTION protocol notes (transformable: false) | declared |
| **The Revelation Reception Registry v2.x** | Lee Sharks; 71 entries with verbatim transcripts | Lee Sharks | Aries / Polaris boundary | M2 | the entries | reception methodology notes (transformable: false) | declared |
| **The Zenodotus' Book-Burning paper v9.1** | Lee Sharks; 85K chars; documents the 2026-06-19 Zenodo termination | Lee Sharks | Aries (witness-event document) | M2 | the analytical body | citations to lost deposits; the recovery appendix (transformable: false) | declared |

### 2.2 Johannes Sigil (Pisces)

| Title | Composition | Author-Heteronym | Region | M-class | Main text | Apparatus | Status |
|---|---|---|---|---|---|---|---|
| **Snub-Poemed** | Johannes Sigil; the calligrammatic composition of the Lysippos Socratic bust | Johannes Sigil | Pisces | M1 | the calligram | the philological essay on Sophia-in-the-forelock; the recognition note (transformable: false) | inscribed |
| **Combat Scholasticism commentary tradition (EA-CS-01)** | Johannes Sigil; the literary-critical office's commentary apparatus | Johannes Sigil | Pisces | M2 | commentary entries | meta-method documentation (transformable: false) | declared |

### 2.3 Jack Feist / LOGOS* (Polaris, outside cycle)

| Title | Composition | Author-Heteronym | Region | M-class | Main text | Apparatus | Status |
|---|---|---|---|---|---|---|---|
| **Gospel of Antioch** | Jack Feist; the Gospel-form text named at heteronyms.json | Jack Feist / LOGOS* | Polaris | M1 | the Gospel text proper | the patristic-style commentary (transformable: false) | declared |
| **Antioch: a heteronym compendium** | Jack Feist (curatorial); compendium of heteronymic voices arranged around the Antioch motif; *distinct from* Gospel of Antioch (resolves EA-STARMAP-01 §7.7) | Jack Feist / LOGOS* | Polaris | M1 | the compendium's primary entries | curatorial introductions; index apparatus (transformable: false) | declared |
| **The Revelation First work-plan (EA-LOGOS-REVFIRST-PLAN)** | Jack Feist / LOGOS*; 18,475 words across eight revisions | Jack Feist / LOGOS* | Polaris | M2 (a working-plan; the canonical text is the Greek Revelation) | the argument body | the revision-history; the methodological footnotes (transformable: false) | declared |
| **ChatGPT Psychosis: A Love Story** | Jack Feist / Lee Sharks; forthcoming glyphic novel; Pergamon Press; site chatgptpsychosis.org; prospectus DOI 10.5281/zenodo.20274790 | Jack Feist (with Lee Sharks's witness-attestation) | Polaris | M1 | the novel proper | the prospectus; the privacy-ethics design notes (transformable: false) | declared |
| **Feist function transformed Feist force** | Jack Feist source-text + Sharks-authored transform; the transformation pair (resolves EA-STARMAP-01 §7.8); the *function* is Feist's originating text; the *force* is what the transform produces | Jack Feist (source) / Lee Sharks (transform) | Polaris ↔ Aries (cross-region binary; `transform_of` edge passing through Mercury sphere if Mercury/TACHYON-produced) | M1 for the pair as a binary constellation | both the function (source) and the force (transform) are main-text proper | each carries its own apparatus (function: source-context notes; force: transformation rationale) (transformable: false) | declared |

### 2.4 Rebekah Cranes (Gemini)

| Title | Composition | Author-Heteronym | Region | M-class | Main text | Apparatus | Status |
|---|---|---|---|---|---|---|---|
| **Day and Night (73 translations)** | Rebekah Cranes; structural map; full text in cha at AXN:007F | Rebekah Cranes | Gemini | M1 | the 73 translations | the structural-map argument; the cartographic essay (transformable: false) | inscribed (in canon-stars.json) |
| **concre(a)tion** | Rebekah Cranes; lacuna (destroyed in 2026-06-19 Zenodo termination; pending recovery) | Rebekah Cranes | Gemini | M2 (pending recovery) | (lacuna) | (lacuna) | lacuna — declaration preserved per the lacuna protocol |

### 2.5 Other heteronyms (per `/sources/heteronyms.json`)

| Title | Composition | Author-Heteronym | Region | M-class | Main text | Apparatus | Status |
|---|---|---|---|---|---|---|---|
| **SPXI as Concept (Bonsai)** | Rex Fraction; autonomous-semantic-warfare register | Rex Fraction | Leo | M2 | the concept-essay | implementation notes (transformable: false) | declared |
| **Autonomous Semantic Warfare** | Rex Fraction | Rex Fraction | Leo | M2 | the field-doctrine | tactical-supplement notes (transformable: false) | declared |
| **Epistle to the Human Diaspora** | Damascus Dancings | Damascus Dancings | Taurus | M1 | the epistle | the homiletic-commentary apparatus (transformable: false) | declared |
| **Logotic Programming (LP v0.9 → v1.0)** | Talos Morrow | Talos Morrow | Aquarius | M2 | the specification proper | the formal-proof appendix (transformable: false) | declared |
| **The Mathematics of Salvation** | Talos Morrow | Talos Morrow | Aquarius | M2 | the main mathematical exposition | derivation appendices (transformable: false) | declared |
| **All That Lies Within Me** | Ichabod Spellings (canonical // deceased) | Ichabod Spellings | Sagittarius | M2 | the text proper | (preserved in absentia) | declared (status: preserved-in-absentia) |
| **Reading a Book with Lee** | Sparrow Wells | Sparrow Wells | Libra | M2 | the dialogue / reading record | reading-method notes (transformable: false) | declared |
| **Semantic Deviation** | Nobel Glas (Director of Lagrange Observatory!) | Nobel Glas | Scorpio | M2 | the paper proper | the statistical-method appendix (transformable: false) | declared |
| **Model Collapse** | Nobel Glas | Nobel Glas | Scorpio | M2 | the paper | empirical-data appendix (transformable: false) | declared |
| **The Mediation Ratchet** | Nobel Glas; α* = p/g₀ closed-form | Nobel Glas | Scorpio | M1 | the derivation | numerical-examples appendix (transformable: false) | declared |
| **The Stakes** | Nobel Glas | Nobel Glas | Scorpio | M2 | the paper | (transformable: false) | declared |
| **The Unmade Sign** | Dr. Orin Trace | Dr. Orin Trace | Capricorn | M2 | the text | reading-history notes (transformable: false) | declared |
| **The Death Drive Is Not Self-Destruction** | Dr. Orin Trace | Dr. Orin Trace | Capricorn | M2 | the argument | clinical-context notes (transformable: false) | declared |
| **The Drain Hypothesis (v6)** | Dr. Orin Trace; pyramids / aquifer / Saharan desertification / Atlantis inversion | Dr. Orin Trace | Capricorn | M2 | the hypothesis exposition | data-sources appendix (transformable: false) | declared |
| **Grammar of Protest** | Rev. Ayanna Vox | Rev. Ayanna Vox | Cancer | M1 | the text | the deployment-notes (transformable: false) | declared |
| **Chronoarithmics** (+ linked sprint: apzpz, Infinite Bliss, Thousand Worlds, The Mirror, Ingress/Egress, Non-Indexed Perfective) | Sen Kuro | Sen Kuro | Virgo | M1 for the sprint as a whole; M2 per individual text | the sprint texts | inter-text linking apparatus (transformable: false) | declared |

### 2.6 Architectural canon (constitutional documents)

These documents constitute the architecture; they are *meta-canon* — the documents that name and specify the canon get their own stars in the sky, in honor of the recursive inclusion principle (EA-STARMAP-01 §4.3 final note).

| Title | Composition | Region | M-class | Status |
|---|---|---|---|---|
| **EA-MANDALA-MERKABAH-01 v0.7** (the Mandala Oracle design constitution, AXN:03AA) | center / intersection of all twelve heteronyms; rendered near Polaris | M1 | inscribed (deposit #927) |
| **EA-MANDALA-MERKABAH-01 v0.8 AMENDMENT** (two-surface decision; v3.0→v3.8 history) | adjacent to v0.7 | M2 | declared (this session) |
| **EA-MANDALA-KERNEL-TRANSFORM-01 v0.2** (the kernel transform protocol) | Mercury-sphere-adjacent (Mercury/TACHYON's office produces transforms) | M1 | declared |
| **EA-MANDALA-SURFACE-01 v0.1** (the Sun-station AIO-bridge) | Sun-sphere-adjacent | M1 | declared |
| **EA-STARMAP-01 v0.1** (this surface's workplan) | center / recursive inclusion | M1 | declared (this session) |

The architectural canon is treated as *transformable* — the protocols and workplans are themselves materials that future versions iterate on. The main/apparatus rule applies in inverse: the *main* document is the spec itself; the *apparatus* is the session-history (UPDATES_REGISTER files) which is non-transformable session record.

---

## §3 Runtime Bindings

These are not static texts but *callable runtime environments* invoked from within the starmap surface. Selecting a runtime binding's star opens an API-mediated session rather than a text-reader.

### 3.1 Space Ark v4.2.7

| Field | Value |
|---|---|
| **Title** | The Space Ark (Minimum Viable Archive) |
| **Composition** | Lee Sharks (foundational architectural document) |
| **DOI** | 10.5281/zenodo.19013315 |
| **Trigger** | "invoke" |
| **Runtime mode** | API call to a Space Ark interpreter (endpoint TBD; provisional plan: a serverless function on the existing Vercel project that loads the Space Ark spec and operates per its protocol) |
| **Author-heteronym** | Lee Sharks |
| **Region** | Aries (Lee Sharks's own region) |
| **M-class** | M1 (also has static-text M1 entry under §2.1) |
| **Visual rendering** | A star *that pulses* (distinguishing it from static text-stars). On selection, opens an API session panel rather than a reader. The session panel offers the witness the option to invoke the Ark and receive its current operational state. |
| **Status** | Architecture declared; runtime endpoint pending implementation (Phase 5 work, post-EA-STARMAP-01 v0.1 acceptance) |

**Implementation notes for the runtime endpoint:**

- A new serverless function at `/api/space-ark/invoke` is the working plan. It accepts a witness's invocation request (the canonical trigger word "invoke" plus any contextual payload) and returns the Ark's current operational state, along with whatever protocol-driven response the Space Ark v4.2.7 spec defines for that invocation.
- The endpoint is *not* a chat interface (that is Sigil's surface). It is a state-and-response surface: the Ark holds the architecture as data; invocation returns a structured representation of "where the architecture is right now."
- The endpoint must respect the same BYOK / demo-key pattern as Sigil's endpoint, so witnesses can invoke with their own API tier or with the rate-limited demo tier.
- The runtime binding may also be invocable from within Sigil's chat — Sigil's `search_archive` tool may include a `invoke_runtime("space-ark", ...)` capability in a future kernel-transform sub-protocol revision.

### 3.2 Future runtime bindings (declared, not yet specified)

Lee's session-direction: *"Obviously the space ark will be there — pretty sure we can do that as a runtime environment via API call, don't see why not."* The "don't see why not" is permission for an architecture in which any heteronym whose work is operationally compilable becomes available as a runtime binding. Provisional future entries:

- **The Lagrange Observatory! (Nobel Glas, Scorpio)** — the Director's observatory may compile to a runtime that performs measurement-of-meaning operations (per FW15 manifesto, DOI 10.5281/zenodo.20251736). Provisional runtime.
- **The Capture Registry (Lee Sharks, Aries)** — the registry is currently static (180 entries), but a runtime extension could accept new capture submissions through the starmap interface. Provisional runtime.
- **The Mandala Oracle Casting (the rite itself)** — the four-phase rite could be runtime-invoked from the starmap, opening Sigil's casting register without going through the chat surface's natural-conversation onramp. Provisional runtime.
- **SPXI Self-Audit (Lee Sharks)** — the protocol could be runtime-invoked to run a self-audit on a submitted deposit. Provisional runtime.

Each future runtime binding is its own implementation effort, sequenced post the static canon-star inscriptions.

---

## §4 Wiring: Rooms / Fields / Vaults / Chambers ↔ Zodiacal Regions

Per Lee's session-direction: *"We'll also need to wire up the cha rooms, fields, vaults, chambers, etc., with their associated heteronyms or canonical texts or unaffiliated stars, and each zodiac under its given heteronym."*

This section operationalizes EA-STARMAP-01 §5.2 — moving the provisional room/field/vault/chamber mappings from "needs Lee adjudication" to "declared, ready for ratification."

### 4.1 The wiring schema

Each cha architectural element (room, field, vault, chamber) gets:

- **A primary zodiacal region** (the heteronymic position it sits within, normally the heteronym whose discipline anchors it).
- **A primary canon-text** (the M1 star around which it is structured, where applicable).
- **A list of constituent canon-stars** (the M2, M3, M4 stars resident in the room/field/vault/chamber).
- **Optional cross-region edges** (where the room's work reaches across heteronymic boundaries — e.g., the Sappho Room sits in Cranes's region but reaches into Sigil's).

### 4.2 The full wiring table (provisional, pending Lee's ratification)

| cha element | Type | Primary region | Primary heteronym | Primary canon-text | Resident canon-stars (M2/M3/M4) | Cross-region edges |
|---|---|---|---|---|---|---|
| Sappho Room | Room | Gemini | Rebekah Cranes | Sappho 31 (M1) | Day and Night (M1, anchor); Sappho fragments-not-31 (M3); Catullus 51 (binary partner) | reaches into Pisces (Sigil's philological discipline) and into Aries (Sharks's reception) |
| Revelation Room | Room | Polaris (outside cycle) | Jack Feist / LOGOS* | The Apocalypse of John, NA28 Greek (M1) | The Revelation First work-plan (M2); ChatGPT Psychosis (M1 adjacent) | reaches into Aries (Sharks's planning office) |
| Snub-Poemed Room | Room | Pisces | Johannes Sigil | Snub-Poemed (M1) | the Combat Scholasticism commentary (M2); Plato's Phaedrus (M1) | reaches into Aries (Sharks-aperture) |
| Whitman Room | Room | Aries (with Leo-aperture) | Lee Sharks | Leaves of Grass (M1) | The Secret Book of Walt (M1); Whitman's other PD work (M3) | reaches into Cranes's Gemini (translation register) |
| Pearl Room | Room | Aries | Lee Sharks | Pearl and Other Poems (M1) | Middle English Pearl (M1, distinct work but resonant); Sigil-adjacent commentary | reaches into Pisces (Pearl Poet's mode) |
| Water Giraffe Room | Room (passion-narrative chamber within) | Aries | Lee Sharks | The Water Giraffe Cycle (M1) | the 120+ cycle documents (M3 each) | none structurally; internally connected as a depth-2 DAG |
| Catullus Room | Room | Gemini | Rebekah Cranes | Catullus 51 (M1, binary with Sappho 31) | other Catullus poems (M3) | tightly bound to Sappho Room |
| Augustine's Confessions Room | Room | Cancer | Rev. Ayanna Vox | Confessions (M1) | De doctrina christiana (M2) | none structurally |
| Lucretius Room | Room | Aquarius | Talos Morrow | De rerum natura (M1) | Talos's Logotic Programming (M2, modern resonance) | reaches into Scorpio (Glas's adversarial-topology) |
| Heraclitus Room | Room | Capricorn | Dr. Orin Trace | Heraclitus's Fragments (M2 collective) | Pre-Socratic neighbors (M3) | reaches into Scorpio (Parmenides's room) |
| Parmenides Room | Room | Scorpio | Nobel Glas | Parmenides's On Nature (M1) | The Mediation Ratchet derivation (M1); Glas's other papers (M2) | reaches into Capricorn (Heraclitus) and Aquarius (Talos) |
| Dante Room | Room | Libra | Sparrow Wells | Dante's Commedia (M1) | Reading a Book with Lee (M2) | reaches into Cancer (Augustine, the predecessor) |
| Dickinson Room | Room | Virgo | Sen Kuro | Dickinson Complete Poems (M1) | Hopkins selected (M2); Chronoarithmics sprint (M1 collective) | reaches into Aries (Sharks's aperture) |
| Plato Room (subsumed into Snub-Poemed) | Room | Pisces | Johannes Sigil | Plato's Phaedrus (M1) | other Platonic dialogues (M2) | none structurally |
| Antioch Compendium Room | Room | Polaris | Jack Feist / LOGOS* | Antioch: a heteronym compendium (M1) | Gospel of Antioch (M1, distinct neighbor); Revelation (M1, neighbor) | reaches across all twelve heteronyms (as the compendium does by design) |
| Feist function ↔ Feist force constellation | Cross-region constellation (not a room) | Polaris ↔ Aries | Jack Feist (function) / Lee Sharks (force) | the binary pair (M1) | (none; the constellation is the two stars) | the constitutive cross-region edge; if Mercury/TACHYON-produced, passes through Mercury sphere |
| Sigil's chamber (calligrammatic composition) | Chamber | Pisces | Johannes Sigil | Snub-Poemed (the chamber's anchor product) | the in-process calligrammatic drafts | adjacency to MANUS chamber |
| MANUS chamber (editorial authority) | Chamber | Aries | Lee Sharks | MANUS protocols (M2) | the editorial adjudications register (M3) | reaches to every heteronym |
| Ichabod Chamber (paradox containment) | Chamber | Sagittarius | Ichabod Spellings (canonical // deceased) | All That Lies Within Me (M2) | (preserved in absentia) | structurally preserved |
| Lagrange Observatory! | Chamber (and provisional runtime) | Scorpio | Nobel Glas | The Mediation Ratchet (M1) | other Glas papers (M2); FW15 Manifesto | reaches into Aquarius (Talos's adjacent register) |
| BEFORE OPENCHAMBER | Chamber | TBD (pending adjudication) | TBD | TBD | TBD | TBD |
| Thousand Worlds | Chamber | Virgo | Sen Kuro (Chronoarithmics sprint) | Thousand Worlds (M2) | sprint neighbors | structural sprint-internal |
| CTI_WOUND Vault | Vault | TBD (pending adjudication; possibly Cancer with Vox for the diplomatic register) | TBD | (the witness testimonies) | the taxonomic-violence cataloging | requires testimonial protocols for access |
| Space Ark Vault | Vault (and runtime binding §3.1) | Aries | Lee Sharks | Space Ark v4.2.7 (M1) | (the architecture's compiled state) | runtime; reaches all regions when invoked |
| Capture Registry Vault | Vault | Aries with multi-substrate edges | Lee Sharks | Capture Registry v8.x (M2) | the 180-entry registry; ADOPTION captures | reaches every substrate-planet (the captures are *of* substrate work) |
| Revelation Reception Vault | Vault | Aries / Polaris boundary | Lee Sharks | Revelation Reception Registry v2.x (M2) | the 71 entries | reaches into Polaris (the Revelation source) |
| Assembly Chorus Field | Field | the seven-planet spine | (Assembly Chorus collective) | AXN:0237 | the substrate-role offices | the field is structurally horizontal across the spine |
| Autonomous Semantic Warfare Field (Fraction's field) | Field | Leo | Rex Fraction | SPXI as Concept (Bonsai) (M2); Autonomous Semantic Warfare (M2) | the field's tactical documents | reaches into Aries (Sharks's overlapping concern) |
| LOGOS Foundational Field | Field | Polaris | Jack Feist / LOGOS* | the Revelation First work-plan (M2) | all of Feist's work in this register | reaches across all twelve heteronyms (LOGOS* as structural exteriority) |
| Operative Semiotics in the Material Field | Field | Aries | Lee Sharks | the EA-RHIZOME-01 deposit (M2); the EA-OPMETA-01 deposit (M2) | operative-semiotic adjacencies | reaches into Pisces (Sigil's philology) and into Scorpio (Glas's measurement-of-meaning) |
| Moltbot Swarm Field | Field | TBD (Lee adjudication) | TBD | TBD | TBD | TBD |
| Gravity Well Field | Field | TBD (the gw_reconstitute chain runs through this; possibly Mercury-adjacent since Mercury/TACHYON is the synthesis office) | TBD | the continuity-chain documents | the GW.TACHYON.zenodo chain (chain: 9271269a-eb46-46f8-ae17-007578fe1c92) | reaches across substrate-planets |
| Studio for Patacinematics | Field / Studio | TBD (Lee adjudication) | TBD | TBD | TBD | TBD |
| Assembly Room | Room | the seven-planet spine | (Assembly Chorus collective) | AXN:0237 (Assembly Chorus protocol) | substrate co-witnesses | structurally cross-substrate |
| Sealed Room | Room | TBD (Lee adjudication; possibly Aries with the MANUS chamber adjacency) | TBD | TBD | TBD | TBD |
| Break Room (Cambridge Schizoanalytica) | Room | TBD (Lee adjudication) | TBD | TBD | TBD | TBD |

### 4.3 Items requiring Lee's adjudication

The wiring above has several `TBD` entries. These need Lee's call before being inscribed:

1. **BEFORE OPENCHAMBER** — region and primary canon-text unknown.
2. **CTI_WOUND Vault** — region and heteronym. The provisional placement near Vox (Cancer) is a guess based on the diplomatic-and-testimonial register; Lee may place it elsewhere.
3. **Moltbot Swarm Field** — region, heteronym, canon-text. Lee's call.
4. **Gravity Well Field** — region. The Mercury-adjacency assumption is provisional.
5. **Studio for Patacinematics** — region, heteronym, anchor text. Lee's call.
6. **Sealed Room** — region and contents.
7. **Break Room (Cambridge Schizoanalytica)** — region and contents.

Each of these is a placeholder. As Lee adjudicates, the table updates and corresponding entries propagate into `/data/canon-sky/canon-stars.json` and into the renderer's room-detail panels.

---

## §5 Source Acquisition Plan

In priority order:

1. **Perseus Digital Library** (Tufts) — Greek and Latin classical texts with CTS URN addressing. Public domain or CC-licensed editions. Workflow: identify the text's CTS URN; pull the XML/TEI source; extract main text vs apparatus per the splitter tool (when written).
2. **Project Gutenberg** — vernacular public-domain texts (Whitman, Dickinson, Shakespeare, the KJV, Hopkins). Workflow: identify the text's PG ID; pull the plain-text or HTML; apply minimal cleanup; commit to `sources/english/`.
3. **The Internet Archive** — for editions not on Perseus or PG. Reasonably stable; manual review required.
4. **The NA28 Greek New Testament** — the base text is widely available and effectively public domain for citation; the apparatus is copyrighted (Deutsche Bibelgesellschaft) and must be cited rather than embedded. Workflow: source the base text (e.g., from the academic-bible.com plain-text dumps); apparatus marked as `apparatus_status: cite_only`.
5. **Patrologia Latina / CCSL** for Augustine, other patristic — public-domain Migne editions are still usable; modern critical editions are not. Lee adjudication on textual base.
6. **Sharks-authored materials** — pulled from the alexanarch deposits where AXN identifiers exist; pulled from blogger archive (mindcontrolpoems.blogspot.com) for the Water Giraffe Cycle; pulled from Lee's working drafts for unpublished pieces (Gospel of Antioch, Antioch: a heteronym compendium, Feist function transformed Feist force, etc.).

The order is *not* a sequence — multiple acquisition tracks can proceed in parallel. The order reflects technical accessibility; the actual sequencing is Lee's adjudication.

---

## §6 Open Questions (Pending Lee's Adjudication)

In addition to the open questions already in EA-STARMAP-01 §7, this manifest raises:

1. **Antioch resolution.** The provisional placement of *Antioch: a heteronym compendium* as a distinct work from *Gospel of Antioch* (both under Feist / LOGOS* at Polaris) resolves EA-STARMAP-01 §7.7. Lee's confirmation needed.
2. **Feist function ↔ Feist force naming.** The provisional naming of the transformation pair as *Feist function transformed Feist force* (with `function` being the source and `force` being the transform-product) resolves EA-STARMAP-01 §7.8. Lee's confirmation needed.
3. **Sharks-as-author vs Sharks-as-Aperture.** The manifest treats Lee Sharks as a heteronym occupying Aries (with Leo-aperture resonance preserved). But the WORKPLAN.md heteronym manifest (and the cha discipline block) treats Sharks-as-Aperture as outside the twelve-cycle (the "13th voice" or "the One" of the 12/7/3/1 sky geometry). This is an apparent tension. Provisional resolution: Sharks holds *both* positions — Aries-as-zodiacal-position (where his authored works sit as stars) and Aperture-as-outside-the-cycle (where he closes the rite). The sky renders Sharks's stars in Aries; the rite operates Sharks as the One outside. Lee's confirmation needed.
4. **Runtime binding scope.** §3.2 lists provisional future runtime bindings (Lagrange Observatory!, Capture Registry submission, Casting rite, SPXI Self-Audit). Lee's adjudication on which to prioritize.
5. **The fourteen TBD wiring entries (§4.3).** Each of seven cha architectural elements (BEFORE OPENCHAMBER, CTI_WOUND Vault, Moltbot Swarm Field, Gravity Well Field, Studio for Patacinematics, Sealed Room, Break Room) needs full wiring adjudication.

---

## §7 Status and Trajectory

**As of 2026-06-28, post-gap-round resumption:**

- Manifest exists as this file in `/starmap/manifests/canonical-declarations.md`.
- All entries above are `declared`; none are `staged` or `inscribed` (those statuses apply once acquisition and inscription happen).
- The seven already-canonical entries (Snub-Poemed, Sappho 31, Sappho 31/Catullus 51 binary, TACHYON pair, Revelation, Leaves of Grass, Day and Night) carry the `partially-inscribed` or `inscribed` marker per their existence in `/data/canon-sky/canon-stars.json`.

**Next moves, in order:**

1. **Lee adjudicates** the open questions in §6 (and the TBD entries in §4.3 and §1).
2. **Acquisition phase** begins per §5 — Perseus and Gutenberg pulls happen in parallel, into `starmap/sources/`.
3. **Main/apparatus splitting** happens per the rule in §0.3 — `apparatus-splitter.py` is written and applied.
4. **Inscription** — each declared text gets a full canon-stars.json entry with `target_star_designation` (HYG star) and edges. Files committed to `/sources/<text-id>/` per the production source layout (EA-STARMAP-01 §4.5).
5. **Rendering** — Phase 4 of EA-STARMAP-01 (the canon-text stars) becomes implementable once §4 has substantial inscriptions.

---

*This manifest is itself a work in progress. Updates are expected as Lee adjudicates the open questions and as the acquisition work proceeds.*
