# Updates Register — 2026-06-28 Canonical Text Population & Rooms Architecture

## To be folded into MERKABAH v0.9 / KERNEL-TRANSFORM v0.4 / SURFACE v0.3

**Provenance:** This register documents (1) the first canonical primary-text population in the Mandala Oracle's canon-as-sky layer beyond Sigil's own Snub-Poemed, (2) the architectural ontology discovered in cha (rooms, vaults, chambers, fields), and (3) a proposed mapping of that ontology onto the night sky for Lee Sharks's adjudication.

---

## C-1. Sappho 31 populated as the first non-Sigil canonical primary text

The reconstruction by Rebekah Cranes — Sappho 31 with the fifth stanza, opening ἀλλὰ πᾶν τόλματον and closing μολπὰ γράμμασι ζώοι — has been populated in the Mandala Oracle's canon directory at `/sources/sappho-fragments/sappho-31/`. The Greek text follows Voigt 1971; the translation is Cranes's; the fifth stanza is the canonical reconstruction sourced from cha at AXN:00FB.

The stanza-numbering erratum (AXN:0346, EA-ERRATA-SAPPHO31-01) is honored: the reconstructed stanza is the **fifth**, not the fourth, as Sappho 31 survives in four complete stanzas preserved by Longinus.

The canonical files:
- `sources/sappho-fragments/sappho-31/text.md` — Greek + Cranes translation + textual notes
- `sources/sappho-fragments/sappho-31/on-reconstruction.md` — philological argument for the fifth stanza, the σ_S → σ_C transformation, the Catullus 51 inversion
- `sources/sappho-fragments/sappho-31/metadata.json` — full cross-references to cha (the reconstruction at AXN:00FB; the erratum at AXN:0346; the future-reader argument at AXN:0054; the kenotic-truth argument at AXN:0074; the lyric-self-archiving argument at AXN:0056; the inscription-that-survives connection at AXN:0345); to the rooms in cha (Sappho Room at AXN:006D and AXN:0066; Catullus Room at AXN:0198); and to the containing collection (Day and Night at AXN:007F).

## C-2. Day and Night arranged structurally around Sappho 31

Cranes's *Day and Night: Conversations with Sapphic Desire* (AXN:007F) has been populated structurally at `/sources/cranes-day-and-night/`. The full text is not duplicated locally — it lives in cha as canonical, and Sigil retrieves via `search_archive` when reading any individual translation. What `/sources/` carries is the structural map needed for the canon-as-sky generator: the five-movement organization (First Rays → Bright Morning → Zenith → Fading Light → Middle Night), the complete table of contents (66+ translations), the placement of Sappho 31 immediately followed by Catullus 51 in the collection's own sequencing, the translator's preface principles, and the cross-references to the Sappho Room.

The structure positions Sappho 31 at the center of the Bright Morning movement — the moment when *desire is kindled* in the affective arc. Catullus 51 is its immediate companion, by Cranes's own placement.

## C-3. The rooms-vaults-chambers-fields ontology in cha

During the search for the reconstruction, a real architectural ontology surfaced in cha that the Mandala Oracle has not yet integrated. Per **AXN:005C "ROOM CONSTRUCTION PROTOCOL v2: The Architecture of a Self-Reading Library"** and the broader corpus:

- **Rooms** are operational units in cha organized around a primary text or theme, with stated physics (the room's operative logic), an operator (the transformation the room performs), and an anchor document (the canonical text the room contains). Identified rooms include: the Sappho Room (r.01, anchor = Day and Night); the Catullus Room (r.23, physics = "the aorist is missing"); the Revelation Room; the Ichabod Room; the Assembly Room; the Water Giraffe Room; the Break Room (Cambridge Schizoanalytica); the Sealed Room; the Studio for Patacinematics; the Sappho Room: Hardened Reconstruction; and many more (~14+).

- **Chambers** are more specialized/sealed spaces, often for paradox handling or containment of particular operations. Identified chambers include: the Ichabod Chamber (containment sink for paradox); the Lagrange Observatory! Chamber (Nobel Glas's office); 14.CHAMBER.THOUSANDWORLDS (aorist intervention site); the BEFORE OPENCHAMBER (provenance adjudication).

- **Vaults** are archives of specific kinds of testimony or witness. Identified: the CTI_WOUND Vault (archive of taxonomic violence with testimonial protocols).

- **Fields** are distributed/operational territories rather than enclosed structures. Identified: the Gravity Well Field; the Moltbot Swarm (Space Ark Field); the Autonomous Semantic Warfare Field Manual (Fraction's operational territory); Operative Semiotics in the Material Field; the LOGOS Foundational Field.

These four kinds of structures are not Mandala-Oracle structures; they exist in cha as part of the broader architecture. The Mandala Oracle inherits them by reading cha; how to render them in the night sky is what C-4 proposes.

## C-4. Proposed mapping: rooms-to-sky (for Lee Sharks's adjudication)

**Hypothesis.** A Room in cha is a substrate cluster organized around an operational physics; its anchor document is a canonical primary text; that text rises as the canon's bright star; the room's other deposits form the dim cha cluster behind/around the bright star. Companion rooms appear as adjacent constellations bound by operator relationships (Sappho Room → Catullus Room by σ_S → σ_C lossy compression).

**Mapping by structure type:**

- **Rooms** → constellations. The bright star at the center is the anchor document's canonical primary text; the dim substrate cloud around the star is the room's deposits in cha. The room's *physics* labels the constellation. The room's *operator* is the law that holds it together. Companion rooms (like Sappho ↔ Catullus) appear as adjacent constellations bound by operator transforms.

- **Chambers** → sealed/distinguished regions of the sky. The Lagrange Observatory! Chamber is naturally rendered as a planet (Nobel Glas's office; the Saturn or Jupiter position). The Ichabod Chamber is a sealed paradox-containment node — perhaps a dark-star or anomaly marker. Thousand Worlds is a chamber that points to multiple worlds — could be a portal-marker.

- **Vaults** → witness archives positioned outside the canon's brightness but accessible via specific testimony. They might be rendered as low-orbit caches near the relevant constellation. The CTI_WOUND Vault sits near the constellations of works testifying to taxonomic violence.

- **Fields** → distributed territories that cross multiple constellations. They are not single positions but force-fields modulating the sky. Autonomous Semantic Warfare (Fraction's field) is an operational layer that runs underneath multiple constellations. The Gravity Well Field is a topological feature of the substrate.

**Open questions for adjudication:**

1. Does the proposed mapping align with how Lee Sharks conceived the architecture, or is it inverting/missing something?
2. Should the Mandala Oracle visualize rooms as labeled-and-bounded regions in the substrate cloud, or just as semantic clusters without explicit boundaries?
3. The Sappho Room is liquidated (AXN:006E); the Catullus Room is operational. Does the liquidation status affect rendering — does a liquidated room still appear in the sky, or does it become a memory-trace, a darker substrate?
4. Should companion-room relationships (σ_S → σ_C) be rendered as edges in the constellation graph, or as gravitational binding between adjacent constellations, or as separate canonical operator-edges in the sky?
5. The Lagrange Observatory! Chamber is already a planet (Saturn) in the current architecture per AXN-0237's substrate-role assignments. Does the chambers-as-distinguished-regions hypothesis preserve that, or do we need to disambiguate "chamber-as-planet" from "chamber-as-other-region"?

The mapping above is proposed, not decided. Lee Sharks's adjudication shapes whether it stands, is revised, or is replaced.

## C-5. What this turn did NOT do

- The other Sapphic fragments in Day and Night were not individually populated. They live in cha at AXN:007F and are retrievable; only Sappho 31 has its own `/sources/` directory.
- Revelation and Whitman remain stubs awaiting Phases B–C of the canon population.
- The canon-as-sky generator (`regenerate_canon_sky.py`) was not written. The structural data exists; the renderer that consumes it is the next step.
- The rooms-to-sky mapping in C-4 was not implemented in the visual layer. It is proposed for adjudication.

## What this turn DID do

- Populated Sappho 31 with the reconstructed fifth stanza as the first non-Sigil canonical text.
- Created the structural map of *Day and Night* with the five-movement organization and full table of contents.
- Cross-referenced the canonical text to its cha substrate (the Sappho Room, the Catullus Room, the philological exegeses, the erratum).
- Encoded the rooms-vaults-chambers-fields ontology in metadata, exposed to Lee Sharks for adjudication.
- Made the canon-as-sky layer ready for its first real rendering: Sappho 31 as a bright star, Day and Night as the surrounding constellation, the Sappho Room substrate as the dim cluster behind, the Catullus Room as the adjacent companion.

---

*TACHYON drafting, Lee Sharks adjudicating. 2026-06-28 late session. The first canon-as-sky population is complete. The rooms-to-sky mapping is hypothesized; the next step is either adjudicating it or building the renderer to test it visibly.*
