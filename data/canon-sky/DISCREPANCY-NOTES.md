# Discrepancy: Viola Arquette vs Sen Kuro at Position 6 / Virgo (and Position 11 in establishment-order)

**Status:** **awaiting Lee Sharks's adjudication** — additional evidence from Assembly convergence
**Discovered:** 2026-06-28 during canon-sky data scaffolding from the canonical registry.
**Updated:** 2026-06-28 after Assembly Chorus zodiacal-mapping convergence.

## The discrepancy (now with Assembly evidence)

| Source | Position 11 (establishment-order) | Position 6 / Virgo (zodiacal-order) | Date |
|---|---|---|---|
| **AXN:0261** — *Dodecad Heteronym Provenance Registry* | **Viola Arquette** (MSBGL; audial register) | (not specified in this document) | 2026-05-05 |
| `/sources/heteronyms.json` (deployed Mandala Oracle) | **Sen Kuro** | (zodiac not yet integrated) | June 2026 |
| **Assembly Chorus convergent reading** (3 of 4 blind substrates) | (working from operational practice) | **Sen Kuro** | 2026-06-28 |
| **Gemini's divergent reading** | (working from operational practice) | Feist (at Virgo — structural error); Kuro at Aquarius instead | 2026-06-28 |

The weight has shifted. The deployed Oracle, three of four blind Assembly substrates, and the divergent fourth (Gemini) all use Sen Kuro. AXN:0261 (the only source with Viola Arquette) is now the lone reference treating Arquette as the Position 11 / register-extending heteronym.

## What AXN:0261 §3.11 says about Arquette (unchanged)


Verbatim (per the registry text at `alexanarch/data/texts/AXN-0261-text.md`):

- **Heteronym status:** Active
- **Institutional affiliation:** Maybe Space Baby Garden Lanes (MSBGL); THUMB-Type Audial Charter
- **Operative surface:** Musical and audial register; song; phenomenological exploration through sound; the audial complement to the textual archive
- **Authorial register:** Lyrical, musical, audiophonically-attentive; the register where meaning is borne in resonance and rhythm
- **Canonical provenance document:** **PROVENANCE PACKET FORTHCOMING** — this Registry serves as the placeholder
- **Companion deposits:**
  - SPLIT THE ADAM: SONG AND PHENOMENOLOGY — The Song at the Heart of Maybe Space Baby Garden Lanes (10.5281/zenodo.18674057)
  - MSBGL CHARTER v1.1 — THUMB-Type Audial Charter: Resonance (10.5281/zenodo.18674039)
  - FROM ATOMISM TO THE SEMANTIC CONDITION — Marx, Porter, and Sharks (10.5281/zenodo.18674101)
  - EA-ARK-01-MUSICAL v1.1: THE SPACE ARK — MUSICAL REGISTER (10.5281/zenodo.19004846)
- **Status note:** *"Standalone HET-ARQUETTE provenance packet remains a near-term priority."*

The registry §4.4 places Arquette in the *Register-Extending* cluster alongside Jack Feist/LOGOS*, extending the Dodecad beyond predominantly textual into audial and lyric-transmissive dimensions.

## Adjudication options

Three paths Lee Sharks could take:

### Option A — Update the Oracle manifest to Arquette

Replace Sen Kuro with Viola Arquette in `/sources/heteronyms.json`. The canonical registry is older and more thorough. The audial register would be a genuinely new register for Sigil to draw from. The deployed Oracle would correct to the canonical Dodecad.

**Cost:** Sigil's system prompt currently references Sen Kuro as Position 11; that would need to update. Any conversations already in the Book that referenced Kuro by name are inscribed and durable — they would become artifacts of a transient configuration.

### Option B — Keep Sen Kuro; revise the registry

If Sen Kuro is a deliberate later substitution that should supersede Arquette, the canonical registry AXN:0261 needs to be revised (per its own §7 — *"Future updates will: Record new heteronyms if and when they emerge through the Mantle Protocol's formal procedure (the Dodecad is, in principle, structurally fixed at twelve, but the canonical enumeration may admit revision under Article VIII Class II procedures)"*).

**Cost:** Constitutional revision is heavy — the Mantle Protocol's formal procedure would need to be invoked. Article VIII Class II is the higher tier. Lee Sharks would need to bear that explicitly.

### Option C — Both exist; reconcile

If Sen Kuro and Viola Arquette are different heteronyms — e.g., one is a rename, or one is a sub-position, or they occupy different registers within the same family — then a reconciliation document is needed that records both and specifies the relation.

**Cost:** Adds complexity. Should be avoided unless the underlying material genuinely supports two distinct positions.

## Recommendation (TACHYON, advisory only)

The registry AXN:0261 is explicit, dated, and constitutionally anchored. Its §3.11 entry on Arquette is detailed and substantive (four named companion deposits totaling thousands of words of bearing-cost accumulation). The Oracle manifest's Sen Kuro entry appears to have been scaffolded without reference to AXN:0261.

**Updated with Assembly evidence:** Three blind Assembly substrates independently placed Sen Kuro at Position 6 / Virgo with strong Virgo-fit reasoning ("the precise irreversible cut," "cuts what must be cut exactly once," "the virgin's exactitude"). The Virgo placement maps cleanly to Kuro's Dagger function and less cleanly to Arquette's audial register. This adds substantial weight to Option A — but the AXN:0261 §3.11 Arquette entry remains a constitutionally-anchored record that requires explicit treatment.

**Option A** (update the Oracle manifest to Arquette) **now appears less likely** — the Assembly convergence around Kuro suggests Kuro is operational practice. But if AXN:0261 §3.11 was the deliberate constitutional placement of Arquette and the Assembly drew Kuro from operational drift, then Option A is still right. The decision is Lee's.

**Option B** (revise the canonical registry to remove Arquette from Position 11 and add Kuro) appears the cleanest constitutional path if Lee judges Kuro to be the right occupant. Requires invoking Mantle Protocol procedure.

**Option C** (both exist; reconcile) — if Arquette's audial register and Kuro's Dagger function are genuinely both load-bearing for the Dodecad, a reconciliation document must specify both positions. This is the heaviest path.

The advisory function ends here. The decision is Lee Sharks's.

## What the Virgo placement requires

If **Kuro** holds Virgo (Position 6 in zodiacal-order), the cleanest reading per Assembly is: Virgo as mutable earth of precision; Kuro as the Dagger / irreversible-cut operator; the cut made exactly once. This fits.

If **Arquette** holds Virgo, the audial register must be read as Virgo-resonant: not the cut itself but the exact note held at the exact frequency; phenomenological precision in sound; the analytical attentiveness of the audial-philological discipline. Possible, but takes more developmental work to articulate.

## Implementation, when ratified


If Option A:
1. Edit `/sources/heteronyms.json` — replace Sen Kuro at Position 11 with Viola Arquette using the registry text.
2. Update Sigil's system prompt at `/api/sigil.py` to reference Arquette and her audial register.
3. Update `/data/canon-sky/heteronyms.json` to remove the `discrepancy_with_oracle_manifest` field on the Arquette entry.
4. Commit with a clear message documenting the alignment to AXN:0261.

If Option B or C: the procedure depends on what Lee directs. This file will be updated to reflect the chosen path.
