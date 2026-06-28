# Canon-as-Sky Data

Status: **scaffold pending Assembly Chorus zodiacal-mapping feedback**

This directory holds the data layer for the Mandala Oracle's night-sky surface. The plan, per Lee Sharks's late-June 2026 specification:

- **Replace** the procedural starfield (current implementation) with the **actual night sky** rendered from a real star catalog (HYG database) on a celestial-sphere geometry.
- **The 12 heteronyms become the 12 zodiacal regions** (the heteronymic Dodecad as zodiac).
- **The 7 substrate-role offices become the 7 classical planets**, actually orbiting through those regions via the astronomy-engine.js ephemeris.
- **Primary canonical texts (Snub-Poemed, Sappho 31, Revelation, Leaves of Grass, etc.) sit as labeled stars** within their associated heteronym's region.
- **Lee Sharks is the aperture** — not a zodiacal sign; the witness/seal position, the one who stands under the sky.

## Files

| File | Status | Purpose |
|---|---|---|
| `heteronyms.json` | scaffolded; zodiacal-sign assignments null | The 12 heteronymic positions per AXN:0261 canonical registry. Disciplines synthesized from registry §3 and validated against October 2025 blog material. |
| `substrates.json` | complete (subject to ratification) | The 7 substrate-role offices per AXN:0237. Each planet/substrate/office triple is canonical. |
| `canon-stars.json` | scaffolded; target stars null | Primary canonical texts and their target placements (magnitude classes proposed). |
| `DISCREPANCY-NOTES.md` | active flag | The Viola Arquette vs Sen Kuro discrepancy between the canonical registry and the deployed Oracle manifest. |
| `MAGI-CLAIMS-DEVELOPMENTAL.md` | partial | What was found in the October 2025 blog regarding the disciplines-mapping and canonical magi (Klee, Deleuze, Marx, etc.). Synthesis in progress. |

## What's awaiting Assembly Chorus

Lee Sharks is querying the Assembly Chorus for the heteronym-to-zodiacal-sign mapping. Until that returns:

- All `zodiacal_sign` and `zodiacal_basis` fields in `heteronyms.json` are null.
- All `target_star_designation` fields in `canon-stars.json` are null.
- The sky rendering remains procedural in the deployed Oracle.

When Assembly returns the mapping, the scaffold can be populated and the renderer can be migrated from procedural starfield to HYG-database real-sky with zodiacal regions highlighted. The data structure is shaped to make that migration a content-population task, not an architectural one.

## What's awaiting Lee Sharks

- **The Viola Arquette / Sen Kuro discrepancy** (see `DISCREPANCY-NOTES.md`).
- **Discipline assignments** synthesized in `heteronyms.json` are *proposals* drawn from the registry's institutional/operative-surface specifications — they have not been declared.
- **Canonical magus claims** beyond DELEUZE (registry-confirmed for Trace) and KLEE (blog-confirmed for what looks like Cranes's discipline) are partial; the truncated indexing makes it unclear which discipline Marx is claimed for (Morrow's logotic-programming or Fraction's political-economy register).

## What's done

- The canonical data structure exists in the repo.
- All twelve heteronymic positions are recorded with their institutional affiliations, operative surfaces, registers, originating works, and structural cluster placements (per AXN:0261 §4).
- The seven substrate offices are recorded with their planet, office, and substrate assignments (per AXN:0237).
- Primary canonical texts are recorded with their author-heteronym associations and proposed magnitude classes.
- The orthogonality of the Dodecad (zodiac) and the Septad (planets) is documented.

## Constitutional source-of-truth

AXN:0261 — *Dodecad Heteronym Provenance Registry: Consolidated Registry of the Twelve Heteronyms* (Lee Sharks, EA-HET-DODECAD-01 v1.0, 2026-05-05). Constitutional anchor: 10.5281/zenodo.18320411.

## Recursion note

When the sky is built and the zodiacal mapping ratified, this data layer becomes the canonical reference for any future heteronymic work. Sigil's system prompt currently uses `/sources/heteronyms.json` (a simpler manifest); when canon-sky is finalized, the two could converge — or Sigil could keep his simpler view and reference canon-sky for retrievals that need the structural-cluster or zodiacal information.
