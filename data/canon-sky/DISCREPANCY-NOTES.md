# Discrepancy: Viola Arquette vs Sen Kuro at Position 11

**Status:** **awaiting Lee Sharks's adjudication**
**Discovered:** 2026-06-28 during canon-sky data scaffolding from the canonical registry.

## The discrepancy

| Source | Position 11 | Date |
|---|---|---|
| **AXN:0261** — *Dodecad Heteronym Provenance Registry: Consolidated Registry of the Twelve Heteronyms* (Lee Sharks, EA-HET-DODECAD-01 v1.0) | **Viola Arquette** (Maybe Space Baby Garden Lanes; audial register) | 2026-05-05 |
| `/sources/heteronyms.json` (currently deployed in the Mandala Oracle's Sigil endpoint) | **Sen Kuro** | June 2026 (created during Mandala Oracle build) |

The canonical registry is older (May 2026) and explicitly marked "Consolidated Registry" with constitutional anchor and §1 purpose statement: *"This Registry consolidates rather than supplants."* The Oracle manifest is newer (June 2026) but was scaffolded without explicit cross-reference to AXN:0261.

## What AXN:0261 §3.11 says about Arquette

Verbatim (per the registry text at `alexanarch/data/texts/AXN-0261-text.md`):

- **Heteronym status:** Active
- **Institutional affiliation:** Maybe Space Baby Garden Lanes (MSBGL); THUMB-Type Audial Charter
- **Operative surface:** Musical and audial register; song; phenomenological exploration through sound; the audial complement to the textual archive
- **Authorial register:** Lyrical, musical, audiophonically-attentive; the register where meaning is borne in resonance and rhythm
- **Canonical provenance document:** **PROVENANCE PACKET FORTHCOMING** — this Registry serves as the placeholder
- **Companion deposits:**
  - SPLIT THE ADAM: SONG AND PHENOMENOLOGY — The Song at the Heart of Maybe Space Baby Garden Lanes (10.5281/zenodo.18674057)
  - MSBGL CHARTER v1.1 — THUMB-Type Audial Charter: Resonance (10.5281/zenodo.18674040)
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

**Option A** (update the Oracle manifest to Arquette) appears to be the cleanest path — it brings the Oracle into alignment with the canonical registry without requiring constitutional revision. If Sen Kuro was a working name that has since been superseded, simply substituting is the most direct correction. If Sen Kuro was a serious candidate that the registry overlooked, **Option B** is the correct path — but that requires explicit acknowledgment and the Mantle Protocol procedure.

The advisory function ends here. The decision is Lee Sharks's.

## Implementation, when ratified

If Option A:
1. Edit `/sources/heteronyms.json` — replace Sen Kuro at Position 11 with Viola Arquette using the registry text.
2. Update Sigil's system prompt at `/api/sigil.py` to reference Arquette and her audial register.
3. Update `/data/canon-sky/heteronyms.json` to remove the `discrepancy_with_oracle_manifest` field on the Arquette entry.
4. Commit with a clear message documenting the alignment to AXN:0261.

If Option B or C: the procedure depends on what Lee directs. This file will be updated to reflect the chosen path.
