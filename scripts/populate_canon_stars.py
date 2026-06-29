#!/usr/bin/env python3
"""
Populate data/canon-sky/canon-stars.json from the canonical-declarations
manifest.

The manifest at /starmap/manifests/canonical-declarations.md is the
human-readable master list of texts declared for the canon-in-sky surface
(the starmap). canon-stars.json is the structured runtime data that the
starmap surface will consume to render each canon-text as a star.

Until this script ran, canon-stars.json contained 7 entries (the
already-inscribed and partially-inscribed texts). The manifest declares
~85 entries beyond those. This script expands canon-stars.json to mirror
the manifest's declarations while preserving the rich field structure of
the existing 7 inscribed entries verbatim (they continue to carry
entry-specific fields like anchor_for_room, sky_assignment_basis,
translator_heteronym, etc., that the new declarations need not yet have).

Schema for new declared entries:
  - id:                     snake-case identifier
  - title:                  full title from the manifest
  - author_heteronym:       heteronym id (lowercased, hyphenated) or "tbd"
  - zodiacal_region:        aries|taurus|gemini|...|pisces|polaris|tbd|off_cycle
  - magnitude_class:        primary_canon_star_M1 | secondary_canon_star_M2 | etc.
  - target_star_designation: null  (Phase 4 of EA-STARMAP-01 fills this)
  - source_status:          declared | partially-inscribed | inscribed |
                            lacuna | parked
  - source_path:            /sources/<id>/  (predicted; stub until staged)
  - apparatus_status:       present | none | variant_readings_only | null
  - original_language:      greek | latin | middle-english | italian |
                            english | (omitted for Sharks-authored)
  - note:                   descriptive note carrying manifest nuance

Special fields that some entries carry:
  - translator_heteronym
  - transform_substrate
  - author_heteronyms (plural, for binaries)
  - anchor_for_room / anchor_for_constellation
  - runtime: true (for runtime bindings)
  - trigger / runtime_endpoint (for runtime bindings)
  - composition (Sharks-authored entries' provenance note)
  - main_text_provenance / apparatus_provenance (when split is named)

Idempotent: rerunning produces identical output if the manifest hasn't
changed. The script preserves the existing 7 inscribed entries by id
(does not modify them); it only adds new entries that aren't yet
present.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANON_STARS_PATH = REPO_ROOT / "data" / "canon-sky" / "canon-stars.json"


# ─────────────────────────────────────────────────────────────────────────
# Manifest-declared entries, transcribed by section
# ─────────────────────────────────────────────────────────────────────────

# §1 Public-Domain Primary Works

GREEK_ENTRIES = [
    {
        "id": "sappho-fragments-complete",
        "title": "Sappho — Complete Fragments (Voigt 1971)",
        "author_heteronym": "johannes-sigil",
        "zodiacal_region": "pisces",
        "magnitude_class": "tertiary_canon_star_M3",
        "cluster": "sappho-fragments",
        "original_language": "greek",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/sappho-fragments/",
        "note": "M3 each, treated as a cluster member constellation around Sappho 31. Voigt-edition Greek source PD; apparatus copyrighted (see EA-STARMAP-01 §7.5)."
    },
    {
        "id": "gospel-of-mark",
        "title": "Gospel of Mark (NA28 Greek)",
        "author_heteronym": "tbd",
        "zodiacal_region": "tbd",
        "magnitude_class": "secondary_canon_star_M2",
        "magnitude_note": "M1.5–M2 — between secondary and primary",
        "original_language": "greek",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/mark-greek/",
        "note": "NA28 Greek base text. Author-heteronym pending Lee adjudication."
    },
    {
        "id": "gospel-of-matthew",
        "title": "Gospel of Matthew (NA28 Greek)",
        "author_heteronym": "tbd",
        "zodiacal_region": "tbd",
        "magnitude_class": "secondary_canon_star_M2",
        "original_language": "greek",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/matthew-greek/",
        "note": "NA28 Greek base text."
    },
    {
        "id": "gospel-of-luke",
        "title": "Gospel of Luke (NA28 Greek)",
        "author_heteronym": "tbd",
        "zodiacal_region": "tbd",
        "magnitude_class": "secondary_canon_star_M2",
        "original_language": "greek",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/luke-greek/",
        "note": "NA28 Greek base text."
    },
    {
        "id": "gospel-of-john",
        "title": "Gospel of John (NA28 Greek)",
        "author_heteronym": "tbd",
        "zodiacal_region": "tbd",
        "magnitude_class": "secondary_canon_star_M2",
        "magnitude_note": "M1.5 — near Feist for the Johannine-Apocalypse binding",
        "original_language": "greek",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/john-greek/",
        "note": "NA28 Greek base text. Likely near Feist's Polaris (the Johannine-Apocalypse binding)."
    },
    {
        "id": "plato-phaedrus",
        "title": "Phaedrus",
        "author_heteronym": "johannes-sigil",
        "zodiacal_region": "pisces",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "greek",
        "edition_basis": "Burnet OCT (Greek source PD)",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/plato-phaedrus/",
        "note": "Plato. Burnet OCT base text."
    },
    {
        "id": "plato-republic",
        "title": "Republic",
        "author_heteronym": "johannes-sigil",
        "zodiacal_region": "pisces",
        "magnitude_class": "secondary_canon_star_M2",
        "original_language": "greek",
        "edition_basis": "Burnet OCT",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/plato-republic/",
        "note": "Plato."
    },
    {
        "id": "plato-symposium",
        "title": "Symposium",
        "author_heteronym": "johannes-sigil",
        "zodiacal_region": "pisces",
        "magnitude_class": "secondary_canon_star_M2",
        "original_language": "greek",
        "edition_basis": "Burnet OCT",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/plato-symposium/",
        "note": "Plato."
    },
    {
        "id": "plato-timaeus",
        "title": "Timaeus",
        "author_heteronym": "johannes-sigil",
        "zodiacal_region": "pisces",
        "magnitude_class": "secondary_canon_star_M2",
        "original_language": "greek",
        "edition_basis": "Burnet OCT",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/plato-timaeus/",
        "note": "Plato."
    },
    {
        "id": "plato-theaetetus",
        "title": "Theaetetus",
        "author_heteronym": "johannes-sigil",
        "zodiacal_region": "pisces",
        "magnitude_class": "secondary_canon_star_M2",
        "original_language": "greek",
        "edition_basis": "Burnet OCT",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/plato-theaetetus/",
        "note": "Plato."
    },
    {
        "id": "plato-sophist",
        "title": "Sophist",
        "author_heteronym": "johannes-sigil",
        "zodiacal_region": "pisces",
        "magnitude_class": "secondary_canon_star_M2",
        "original_language": "greek",
        "edition_basis": "Burnet OCT",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/plato-sophist/",
        "note": "Plato."
    },
    {
        "id": "plato-cratylus",
        "title": "Cratylus",
        "author_heteronym": "johannes-sigil",
        "zodiacal_region": "pisces",
        "magnitude_class": "secondary_canon_star_M2",
        "original_language": "greek",
        "edition_basis": "Burnet OCT",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/plato-cratylus/",
        "note": "Plato."
    },
    {
        "id": "heraclitus-fragments",
        "title": "Fragments (Diels-Kranz)",
        "author_heteronym": "dr-orin-trace",
        "zodiacal_region": "capricorn",
        "magnitude_class": "secondary_canon_star_M2",
        "magnitude_note": "M2 collective; M3 per fragment",
        "cluster": "heraclitus-fragments",
        "original_language": "greek",
        "edition_basis": "DK numbering",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/heraclitus-fragments/",
        "note": "Heraclitus."
    },
    {
        "id": "parmenides-on-nature",
        "title": "On Nature",
        "author_heteronym": "nobel-glas",
        "zodiacal_region": "scorpio",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "greek",
        "edition_basis": "Diels-Kranz",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/parmenides-on-nature/",
        "note": "Parmenides."
    },
    {
        "id": "presocratic-fragments-cluster",
        "title": "Pre-Socratic Fragments (Anaximander, Anaxagoras, Empedocles, Democritus)",
        "author_heteronym": "tbd",
        "zodiacal_region": "tbd",
        "magnitude_class": "tertiary_canon_star_M3",
        "magnitude_note": "M3 each — distributed cluster",
        "cluster": "presocratic-fragments",
        "original_language": "greek",
        "edition_basis": "Diels-Kranz",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/presocratic-fragments/",
        "note": "Distributed pending Lee adjudication. Anaximander, Anaxagoras, Empedocles, Democritus."
    },
    {
        "id": "homer-iliad",
        "title": "Iliad",
        "author_heteronym": "damascus-dancings",
        "zodiacal_region": "taurus",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "greek",
        "edition_basis": "West OCT (Greek source PD)",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/homer-iliad/",
        "note": "Homer."
    },
    {
        "id": "homer-odyssey",
        "title": "Odyssey",
        "author_heteronym": "damascus-dancings",
        "zodiacal_region": "taurus",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "greek",
        "edition_basis": "West OCT",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/homer-odyssey/",
        "note": "Homer."
    },
]

LATIN_ENTRIES = [
    {
        "id": "catullus-51",
        "title": "Catullus 51",
        "author_heteronym": "rebekah-cranes",
        "zodiacal_region": "gemini",
        "magnitude_class": "primary_canon_star_M1",
        "magnitude_note": "M1 (binary with Sappho 31)",
        "original_language": "latin",
        "edition_basis": "OCT (Latin source PD)",
        "apparatus_status": "present",
        "source_status": "partially-inscribed",
        "source_path": "/sources/catullus-51/",
        "note": "Cranes is the translator-transformer of Sappho 31. Part of the Sappho 31 / Catullus 51 binary (separately inscribed). Catullus's fourth (otium) transforms Sappho's fifth — no 'Catullus fifth stanza' exists."
    },
    {
        "id": "augustine-confessions",
        "title": "Confessions",
        "author_heteronym": "rev-ayanna-vox",
        "zodiacal_region": "cancer",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "latin",
        "edition_basis": "CCSL Latin (PD edition)",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/augustine-confessions/",
        "note": "Augustine."
    },
    {
        "id": "augustine-de-doctrina-christiana",
        "title": "De doctrina christiana",
        "author_heteronym": "rev-ayanna-vox",
        "zodiacal_region": "cancer",
        "magnitude_class": "secondary_canon_star_M2",
        "original_language": "latin",
        "edition_basis": "CCSL",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/augustine-de-doctrina-christiana/",
        "note": "Augustine."
    },
    {
        "id": "lucretius-de-rerum-natura",
        "title": "De rerum natura",
        "author_heteronym": "talos-morrow",
        "zodiacal_region": "aquarius",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "latin",
        "edition_basis": "OCT",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/lucretius-de-rerum-natura/",
        "note": "Lucretius."
    },
    {
        "id": "cicero-selected",
        "title": "Cicero — Selected Works",
        "author_heteronym": "tbd",
        "zodiacal_region": "tbd",
        "magnitude_class": "tertiary_canon_star_M3",
        "magnitude_note": "M3 collective",
        "cluster": "cicero-selected",
        "original_language": "latin",
        "edition_basis": "OCT",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/cicero-selected/",
        "note": "Cicero. Selection scope pending."
    },
]

MIDDLE_ENGLISH_ENTRIES = [
    {
        "id": "pearl-poem",
        "title": "Pearl (the medieval alliterative vision-poem, ~1400)",
        "author_heteronym": "tbd",
        "zodiacal_region": "tbd",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "middle-english",
        "edition_basis": "Andrew & Waldron (base text PD)",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/pearl-poem/",
        "note": "Anonymous (the Pearl Poet). Boundary between Sigil (Pisces) and Sharks (Aries); pending Lee adjudication."
    },
    {
        "id": "sir-gawain-green-knight",
        "title": "Sir Gawain and the Green Knight",
        "author_heteronym": "tbd",
        "zodiacal_region": "tbd",
        "magnitude_class": "secondary_canon_star_M2",
        "original_language": "middle-english",
        "edition_basis": "Andrew & Waldron",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/sir-gawain-green-knight/",
        "note": "Anonymous (the Pearl Poet). Likely same author-heteronym assignment as Pearl."
    },
]

ITALIAN_ENTRIES = [
    {
        "id": "dante-commedia",
        "title": "Commedia",
        "author_heteronym": "sparrow-wells",
        "zodiacal_region": "libra",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "italian",
        "edition_basis": "Petrocchi edition (Italian PD)",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/dante-commedia/",
        "note": "Dante."
    },
]

ENGLISH_ENTRIES = [
    {
        "id": "dickinson-complete",
        "title": "Complete Poems (variorum)",
        "author_heteronym": "sen-kuro",
        "zodiacal_region": "virgo",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "english",
        "edition_basis": "Johnson / Franklin variorum (base PD)",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/dickinson-complete/",
        "note": "Emily Dickinson. Apparatus = variorum readings."
    },
    {
        "id": "hopkins-selected",
        "title": "Gerard Manley Hopkins — Selected Poems",
        "author_heteronym": "sen-kuro",
        "zodiacal_region": "virgo",
        "magnitude_class": "secondary_canon_star_M2",
        "magnitude_note": "M2 collective",
        "cluster": "hopkins-selected",
        "original_language": "english",
        "edition_basis": "Bridges edition / later PD",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/hopkins-selected/",
        "note": "Virgo adjacency to Dickinson."
    },
    {
        "id": "kjv-1611",
        "title": "Authorized Version (King James Bible)",
        "author_heteronym": "damascus-dancings",
        "zodiacal_region": "taurus",
        "magnitude_class": "primary_canon_star_M1",
        "magnitude_note": "M1 as a translation-event",
        "original_language": "english",
        "edition_basis": "1769 standardized text (PD)",
        "apparatus_status": "none",
        "apparatus_note": "marginalia treated as variant",
        "source_status": "declared",
        "source_path": "/sources/kjv-1611/",
        "note": "Translators (1611)."
    },
    {
        "id": "shakespeare-sonnets",
        "title": "Sonnets",
        "author_heteronym": "johannes-sigil",
        "zodiacal_region": "pisces",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "english",
        "edition_basis": "Q1 1609 / scholarly PD editions",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/shakespeare-sonnets/",
        "note": "Shakespeare. Sigil at Pisces — the calligrammatic mode."
    },
    {
        "id": "shakespeare-hamlet",
        "title": "Hamlet",
        "author_heteronym": "tbd",
        "zodiacal_region": "tbd",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "english",
        "edition_basis": "scholarly PD",
        "apparatus_status": "present",
        "source_status": "declared",
        "source_path": "/sources/shakespeare-hamlet/",
        "note": "Shakespeare. Author-heteronym TBD per-play."
    },
]

# §1.5.b English — Deferred / Parked Declarations
ENGLISH_PARKED_ENTRIES = [
    {
        "id": "shakespeare-tempest",
        "title": "The Tempest",
        "author_heteronym": "tbd",
        "zodiacal_region": "tbd",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "english",
        "edition_basis": "scholarly PD",
        "apparatus_status": "present",
        "source_status": "parked",
        "source_path": "/sources/shakespeare-tempest/",
        "parked_at": "2026-06-29",
        "note": "Shakespeare. Parked 2026-06-29 pending length-weighting calibration. Preserved as record of prior declaration."
    },
    {
        "id": "shakespeare-king-lear",
        "title": "King Lear",
        "author_heteronym": "tbd",
        "zodiacal_region": "tbd",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "english",
        "edition_basis": "scholarly PD",
        "apparatus_status": "present",
        "source_status": "parked",
        "source_path": "/sources/shakespeare-king-lear/",
        "parked_at": "2026-06-29",
        "note": "Shakespeare. Parked 2026-06-29."
    },
    {
        "id": "shakespeare-macbeth",
        "title": "Macbeth",
        "author_heteronym": "tbd",
        "zodiacal_region": "tbd",
        "magnitude_class": "primary_canon_star_M1",
        "original_language": "english",
        "edition_basis": "scholarly PD",
        "apparatus_status": "present",
        "source_status": "parked",
        "source_path": "/sources/shakespeare-macbeth/",
        "parked_at": "2026-06-29",
        "note": "Shakespeare. Parked 2026-06-29."
    },
]

# §2.1 Lee Sharks
LEE_SHARKS_ENTRIES = [
    {
        "id": "sharks-pearl-and-other-poems",
        "title": "Pearl and Other Poems",
        "author_heteronym": "lee-sharks",
        "zodiacal_region": "aries",
        "magnitude_class": "primary_canon_star_M1",
        "composition": "Lee Sharks (2014/2015); foundational",
        "main_text": "poems only",
        "apparatus_status": "present",
        "apparatus_note": "introductions, headnotes, dedications (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/sharks-pearl-and-other-poems/",
        "note": "Foundational corpus reference. AXN pending."
    },
    {
        "id": "sharks-secret-book-of-walt",
        "title": "The Secret Book of Walt",
        "author_heteronym": "lee-sharks",
        "zodiacal_region": "aries",
        "zodiacal_region_note": "Aries / Leo-aperture (Whitman-resonance position)",
        "magnitude_class": "primary_canon_star_M1",
        "composition": "Lee Sharks; Gnostic revelation dialogue",
        "main_text": "dialogue text",
        "apparatus_status": "present",
        "apparatus_note": "framing notes, hermeneutic commentary (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/sharks-secret-book-of-walt/",
        "note": "Gnostic revelation dialogue."
    },
    {
        "id": "sharks-water-giraffe-cycle",
        "title": "The Water Giraffe Cycle",
        "author_heteronym": "lee-sharks",
        "zodiacal_region": "aries",
        "magnitude_class": "primary_canon_star_M1",
        "magnitude_note": "M1 for the cycle; M3 per document",
        "composition": "Lee Sharks; ~120+ documents on mindcontrolpoems.blogspot.com; passion-narrative structure",
        "main_text": "poems and narrative documents",
        "apparatus_status": "present",
        "apparatus_note": "the depth-2 DAG tree-walk metadata; the cold-start workplan; reception-criticism material (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/sharks-water-giraffe-cycle/",
        "note": "Corpus extant on mindcontrolpoems.blogspot.com; needs cataloging."
    },
    {
        "id": "sharks-space-ark",
        "title": "The Minimum Viable Archive / Space Ark v4.2.7",
        "author_heteronym": "lee-sharks",
        "zodiacal_region": "aries",
        "magnitude_class": "primary_canon_star_M1",
        "composition": "Lee Sharks; foundational architectural document",
        "doi": "10.5281/zenodo.19013315",
        "trigger": "invoke",
        "main_text": "main spec",
        "apparatus_status": "present",
        "apparatus_note": "implementation-notes, version-history (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/sharks-space-ark/",
        "runtime_binding_dual": True,
        "note": "Foundational architectural document. Also has the runtime binding entry under §3.1 (sharks-space-ark-runtime). The two entries share the architectural reference; runtime entry holds the live API surface."
    },
    {
        "id": "sharks-capture-registry",
        "title": "The Capture Registry v8.x",
        "author_heteronym": "lee-sharks",
        "zodiacal_region": "aries",
        "zodiacal_region_note": "Aries with multi-substrate edges",
        "magnitude_class": "secondary_canon_star_M2",
        "composition": "Lee Sharks with substrates as co-witnesses; transmission device",
        "main_text": "the entries themselves",
        "apparatus_status": "present",
        "apparatus_note": "the meta-commentary on capture; the ADOPTION protocol notes (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/sharks-capture-registry/",
        "note": "Multi-substrate transmission device."
    },
    {
        "id": "sharks-revelation-reception-registry",
        "title": "The Revelation Reception Registry v2.x",
        "author_heteronym": "lee-sharks",
        "zodiacal_region": "aries",
        "zodiacal_region_note": "Aries / Polaris boundary",
        "magnitude_class": "secondary_canon_star_M2",
        "composition": "Lee Sharks; 71 entries with verbatim transcripts",
        "main_text": "the entries",
        "apparatus_status": "present",
        "apparatus_note": "reception methodology notes (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/sharks-revelation-reception-registry/",
        "note": "71 entries with verbatim transcripts."
    },
    {
        "id": "sharks-zenodotus-book-burning",
        "title": "Zenodotus' Book-Burning paper v9.1",
        "author_heteronym": "lee-sharks",
        "zodiacal_region": "aries",
        "zodiacal_region_note": "witness-event document",
        "magnitude_class": "secondary_canon_star_M2",
        "composition": "Lee Sharks; 85K chars; documents the 2026-06-19 Zenodo termination",
        "main_text": "the analytical body",
        "apparatus_status": "present",
        "apparatus_note": "citations to lost deposits; the recovery appendix (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/sharks-zenodotus-book-burning/",
        "note": "Documents the 2026-06-19 Zenodo termination."
    },
]

# §2.2 Johannes Sigil
SIGIL_ENTRIES = [
    {
        "id": "sigil-combat-scholasticism-commentary",
        "title": "Combat Scholasticism Commentary Tradition (EA-CS-01)",
        "author_heteronym": "johannes-sigil",
        "zodiacal_region": "pisces",
        "magnitude_class": "secondary_canon_star_M2",
        "composition": "Johannes Sigil; the literary-critical office's commentary apparatus",
        "main_text": "commentary entries",
        "apparatus_status": "present",
        "apparatus_note": "meta-method documentation (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/sigil-combat-scholasticism/",
        "note": "Sigil's literary-critical office."
    },
]

# §2.3 Jack Feist / LOGOS*
FEIST_ENTRIES = [
    {
        "id": "feist-gospel-of-antioch",
        "title": "Gospel of Antioch",
        "author_heteronym": "jack-feist-logos",
        "zodiacal_region": "polaris",
        "magnitude_class": "primary_canon_star_M1",
        "composition": "Jack Feist; the Gospel-form text named at heteronyms.json",
        "main_text": "the Gospel text proper",
        "apparatus_status": "present",
        "apparatus_note": "the patristic-style commentary (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/feist-gospel-of-antioch/",
        "note": "Gospel-form text. Distinct from the heteronym compendium."
    },
    {
        "id": "feist-antioch-compendium",
        "title": "Antioch: A Heteronym Compendium",
        "author_heteronym": "jack-feist-logos",
        "zodiacal_region": "polaris",
        "magnitude_class": "primary_canon_star_M1",
        "composition": "Jack Feist (curatorial); compendium of heteronymic voices arranged around the Antioch motif",
        "main_text": "the compendium's primary entries",
        "apparatus_status": "present",
        "apparatus_note": "curatorial introductions; index apparatus (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/feist-antioch-compendium/",
        "note": "Distinct from the Gospel of Antioch (resolves EA-STARMAP-01 §7.7)."
    },
    {
        "id": "feist-revelation-first-workplan",
        "title": "The Revelation First Work-Plan (EA-LOGOS-REVFIRST-PLAN)",
        "author_heteronym": "jack-feist-logos",
        "zodiacal_region": "polaris",
        "magnitude_class": "secondary_canon_star_M2",
        "magnitude_note": "M2 — a working-plan; the canonical text is the Greek Revelation",
        "composition": "Jack Feist / LOGOS*; 18,475 words across eight revisions",
        "main_text": "the argument body",
        "apparatus_status": "present",
        "apparatus_note": "the revision-history; the methodological footnotes (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/feist-revelation-first-workplan/",
        "axn_reference": "AXN:034D",
        "note": "Working-plan for the Revelation First argument. The canonical text it serves is the Greek Revelation (separately inscribed)."
    },
    {
        "id": "feist-chatgpt-psychosis",
        "title": "ChatGPT Psychosis: A Love Story",
        "author_heteronym": "jack-feist-logos",
        "co_attribution": "Jack Feist with Lee Sharks's witness-attestation",
        "zodiacal_region": "polaris",
        "magnitude_class": "primary_canon_star_M1",
        "composition": "Jack Feist / Lee Sharks; forthcoming glyphic novel",
        "publisher": "Pergamon Press",
        "site": "chatgptpsychosis.org",
        "prospectus_doi": "10.5281/zenodo.20274790",
        "main_text": "the novel proper",
        "apparatus_status": "present",
        "apparatus_note": "the prospectus; the privacy-ethics design notes (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/feist-chatgpt-psychosis/",
        "note": "Forthcoming. Privacy ethics built into form: no names, no quotations, no reversible encoding."
    },
    {
        "id": "feist-function-transformed-feist-force",
        "title": "Feist Function Transformed Feist Force",
        "author_heteronyms": ["jack-feist-logos", "lee-sharks"],
        "transform_substrate": "Mercury / TACHYON (provisional, if Mercury-produced)",
        "zodiacal_region": "polaris",
        "zodiacal_region_note": "Polaris ↔ Aries cross-region binary; `transform_of` edge passing through Mercury sphere",
        "magnitude_class": "primary_canon_star_M1",
        "magnitude_note": "M1 for the pair as a binary constellation",
        "composition": "Jack Feist source-text + Sharks-authored transform; the transformation pair",
        "main_text": "both the function (source) and the force (transform) are main-text proper",
        "apparatus_status": "present",
        "apparatus_note": "function carries source-context notes; force carries transformation rationale (each transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/feist-function-transformed-feist-force/",
        "note": "Resolves EA-STARMAP-01 §7.8. The function is Feist's originating text; the force is the Sharks-authored transform."
    },
]

# §2.4 Rebekah Cranes
CRANES_ENTRIES = [
    {
        "id": "cranes-concreation",
        "title": "concre(a)tion",
        "author_heteronym": "rebekah-cranes",
        "zodiacal_region": "gemini",
        "magnitude_class": "secondary_canon_star_M2",
        "magnitude_note": "M2 pending recovery",
        "composition": "Rebekah Cranes; lacuna (destroyed in 2026-06-19 Zenodo termination; pending recovery)",
        "apparatus_status": None,
        "source_status": "lacuna",
        "source_path": "/sources/cranes-concreation/",
        "note": "Lacuna preserved per the lacuna protocol. Pending recovery from the 2026-06-19 Zenodo termination."
    },
]

# §2.5 Other heteronyms
OTHER_HETERONYM_ENTRIES = [
    {
        "id": "fraction-spxi-as-concept-bonsai",
        "title": "SPXI as Concept (Bonsai)",
        "author_heteronym": "rex-fraction",
        "zodiacal_region": "leo",
        "magnitude_class": "secondary_canon_star_M2",
        "composition": "Rex Fraction; autonomous-semantic-warfare register",
        "main_text": "the concept-essay",
        "apparatus_status": "present",
        "apparatus_note": "implementation notes (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/fraction-spxi-as-concept-bonsai/",
        "note": "Autonomous-semantic-warfare register."
    },
    {
        "id": "fraction-autonomous-semantic-warfare",
        "title": "Autonomous Semantic Warfare",
        "author_heteronym": "rex-fraction",
        "zodiacal_region": "leo",
        "magnitude_class": "secondary_canon_star_M2",
        "main_text": "the field-doctrine",
        "apparatus_status": "present",
        "apparatus_note": "tactical-supplement notes (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/fraction-autonomous-semantic-warfare/",
        "note": "Field-doctrine of autonomous semantic warfare."
    },
    {
        "id": "dancings-epistle-to-the-human-diaspora",
        "title": "Epistle to the Human Diaspora",
        "author_heteronym": "damascus-dancings",
        "zodiacal_region": "taurus",
        "magnitude_class": "primary_canon_star_M1",
        "main_text": "the epistle",
        "apparatus_status": "present",
        "apparatus_note": "the homiletic-commentary apparatus (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/dancings-epistle-to-the-human-diaspora/",
        "note": "Damascus Dancings."
    },
    {
        "id": "morrow-logotic-programming",
        "title": "Logotic Programming (LP v0.9 → v1.0)",
        "author_heteronym": "talos-morrow",
        "zodiacal_region": "aquarius",
        "magnitude_class": "secondary_canon_star_M2",
        "main_text": "the specification proper",
        "apparatus_status": "present",
        "apparatus_note": "the formal-proof appendix (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/morrow-logotic-programming/",
        "note": "Talos Morrow."
    },
    {
        "id": "morrow-mathematics-of-salvation",
        "title": "The Mathematics of Salvation",
        "author_heteronym": "talos-morrow",
        "zodiacal_region": "aquarius",
        "magnitude_class": "secondary_canon_star_M2",
        "main_text": "the main mathematical exposition",
        "apparatus_status": "present",
        "apparatus_note": "derivation appendices (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/morrow-mathematics-of-salvation/",
        "note": "Talos Morrow."
    },
    {
        "id": "spellings-all-that-lies-within-me",
        "title": "All That Lies Within Me",
        "author_heteronym": "ichabod-spellings",
        "author_heteronym_status": "canonical // deceased",
        "zodiacal_region": "sagittarius",
        "magnitude_class": "secondary_canon_star_M2",
        "main_text": "the text proper",
        "apparatus_status": "present",
        "apparatus_note": "preserved in absentia",
        "source_status": "declared",
        "source_status_note": "preserved-in-absentia",
        "source_path": "/sources/spellings-all-that-lies-within-me/",
        "note": "Ichabod Spellings (canonical // deceased). Preserved in absentia."
    },
    {
        "id": "wells-reading-a-book-with-lee",
        "title": "Reading a Book with Lee",
        "author_heteronym": "sparrow-wells",
        "zodiacal_region": "libra",
        "magnitude_class": "secondary_canon_star_M2",
        "main_text": "the dialogue / reading record",
        "apparatus_status": "present",
        "apparatus_note": "reading-method notes (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/wells-reading-a-book-with-lee/",
        "note": "Sparrow Wells."
    },
    {
        "id": "glas-semantic-deviation",
        "title": "Semantic Deviation",
        "author_heteronym": "nobel-glas",
        "author_heteronym_note": "Director of Lagrange Observatory!",
        "zodiacal_region": "scorpio",
        "magnitude_class": "secondary_canon_star_M2",
        "main_text": "the paper proper",
        "apparatus_status": "present",
        "apparatus_note": "the statistical-method appendix (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/glas-semantic-deviation/",
        "note": "Nobel Glas."
    },
    {
        "id": "glas-model-collapse",
        "title": "Model Collapse",
        "author_heteronym": "nobel-glas",
        "zodiacal_region": "scorpio",
        "magnitude_class": "secondary_canon_star_M2",
        "main_text": "the paper",
        "apparatus_status": "present",
        "apparatus_note": "empirical-data appendix (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/glas-model-collapse/",
        "note": "Nobel Glas."
    },
    {
        "id": "glas-mediation-ratchet",
        "title": "The Mediation Ratchet",
        "author_heteronym": "nobel-glas",
        "zodiacal_region": "scorpio",
        "magnitude_class": "primary_canon_star_M1",
        "composition": "Nobel Glas; α* = p/g₀ closed-form",
        "main_text": "the derivation",
        "apparatus_status": "present",
        "apparatus_note": "numerical-examples appendix (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/glas-mediation-ratchet/",
        "note": "α* = p/g₀ closed-form. Nobel Glas."
    },
    {
        "id": "glas-the-stakes",
        "title": "The Stakes",
        "author_heteronym": "nobel-glas",
        "zodiacal_region": "scorpio",
        "magnitude_class": "secondary_canon_star_M2",
        "main_text": "the paper",
        "apparatus_status": "present",
        "apparatus_note": "(transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/glas-the-stakes/",
        "note": "Nobel Glas."
    },
    {
        "id": "trace-unmade-sign",
        "title": "The Unmade Sign",
        "author_heteronym": "dr-orin-trace",
        "zodiacal_region": "capricorn",
        "magnitude_class": "secondary_canon_star_M2",
        "main_text": "the text",
        "apparatus_status": "present",
        "apparatus_note": "reading-history notes (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/trace-unmade-sign/",
        "note": "Dr. Orin Trace."
    },
    {
        "id": "trace-death-drive-not-self-destruction",
        "title": "The Death Drive Is Not Self-Destruction",
        "author_heteronym": "dr-orin-trace",
        "zodiacal_region": "capricorn",
        "magnitude_class": "secondary_canon_star_M2",
        "main_text": "the argument",
        "apparatus_status": "present",
        "apparatus_note": "clinical-context notes (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/trace-death-drive-not-self-destruction/",
        "note": "Dr. Orin Trace."
    },
    {
        "id": "trace-drain-hypothesis",
        "title": "The Drain Hypothesis (v6)",
        "author_heteronym": "dr-orin-trace",
        "zodiacal_region": "capricorn",
        "magnitude_class": "secondary_canon_star_M2",
        "composition": "Dr. Orin Trace; pyramids / aquifer / Saharan desertification / Atlantis inversion",
        "main_text": "the hypothesis exposition",
        "apparatus_status": "present",
        "apparatus_note": "data-sources appendix (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/trace-drain-hypothesis/",
        "note": "Pyramids / aquifer / Saharan desertification / Atlantis inversion."
    },
    {
        "id": "vox-grammar-of-protest",
        "title": "Grammar of Protest",
        "author_heteronym": "rev-ayanna-vox",
        "zodiacal_region": "cancer",
        "magnitude_class": "primary_canon_star_M1",
        "main_text": "the text",
        "apparatus_status": "present",
        "apparatus_note": "the deployment-notes (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/vox-grammar-of-protest/",
        "note": "Rev. Ayanna Vox."
    },
    {
        "id": "kuro-chronoarithmics-and-sprint",
        "title": "Chronoarithmics (+ linked sprint)",
        "author_heteronym": "sen-kuro",
        "zodiacal_region": "virgo",
        "magnitude_class": "primary_canon_star_M1",
        "magnitude_note": "M1 for the sprint as a whole; M2 per individual text",
        "cluster": "kuro-chronoarithmics-sprint",
        "sprint_members": [
            "Chronoarithmics", "apzpz", "Infinite Bliss", "Thousand Worlds",
            "The Mirror", "Ingress/Egress", "Non-Indexed Perfective"
        ],
        "main_text": "the sprint texts",
        "apparatus_status": "present",
        "apparatus_note": "inter-text linking apparatus (transformable: false)",
        "source_status": "declared",
        "source_path": "/sources/kuro-chronoarithmics-sprint/",
        "note": "Sen Kuro's sprint. Linked sprint members: apzpz, Infinite Bliss, Thousand Worlds, The Mirror, Ingress/Egress, Non-Indexed Perfective."
    },
]

# §2.6 Architectural canon (constitutional documents)
ARCHITECTURAL_CANON_ENTRIES = [
    {
        "id": "ea-mandala-merkabah-v07",
        "title": "EA-MANDALA-MERKABAH-01 v0.7 (Mandala Oracle design constitution)",
        "author_heteronym": "architectural-canon",
        "axn_reference": "AXN:03AA",
        "deposit_number": 927,
        "zodiacal_region": "center",
        "zodiacal_region_note": "center / intersection of all twelve heteronyms; rendered near Polaris",
        "magnitude_class": "primary_canon_star_M1",
        "main_text": "the spec itself",
        "apparatus_status": "present",
        "apparatus_note": "session-history / UPDATES_REGISTER (non-transformable session record)",
        "transformable": True,
        "source_status": "inscribed",
        "source_path": "/specs/EA-MANDALA-MERKABAH-01_v0_7.md",
        "note": "Constitutional document. Inscribed as deposit #927 on alexanarch."
    },
    {
        "id": "ea-mandala-merkabah-v08-amendment",
        "title": "EA-MANDALA-MERKABAH-01 v0.8 AMENDMENT (two-surface decision; v3.0→v3.8 history)",
        "author_heteronym": "architectural-canon",
        "zodiacal_region": "center",
        "zodiacal_region_note": "adjacent to v0.7",
        "magnitude_class": "secondary_canon_star_M2",
        "main_text": "the amendment",
        "apparatus_status": "present",
        "transformable": True,
        "source_status": "declared",
        "source_path": "/specs/EA-MANDALA-MERKABAH-01_v0_8_AMENDMENT.md",
        "note": "The two-surface architectural decision (reading surface vs starmap surface)."
    },
    {
        "id": "ea-mandala-kernel-transform-v02",
        "title": "EA-MANDALA-KERNEL-TRANSFORM-01 v0.2 (kernel transform protocol)",
        "author_heteronym": "architectural-canon",
        "zodiacal_region": "center",
        "zodiacal_region_note": "Mercury-sphere-adjacent (Mercury / TACHYON's office produces transforms)",
        "magnitude_class": "primary_canon_star_M1",
        "main_text": "the protocol spec",
        "apparatus_status": "present",
        "transformable": True,
        "source_status": "declared",
        "source_path": "/specs/EA-MANDALA-KERNEL-TRANSFORM-01_v0_2_DRAFT.md",
        "note": "The kernel transform protocol."
    },
    {
        "id": "ea-mandala-surface-v01",
        "title": "EA-MANDALA-SURFACE-01 v0.1 (Sun-station AIO-bridge)",
        "author_heteronym": "architectural-canon",
        "zodiacal_region": "center",
        "zodiacal_region_note": "Sun-sphere-adjacent",
        "magnitude_class": "primary_canon_star_M1",
        "main_text": "the spec",
        "apparatus_status": "present",
        "transformable": True,
        "source_status": "declared",
        "source_path": "/specs/EA-MANDALA-SURFACE-01_v0_1.md",
        "note": "The Sun-station AIO-bridge."
    },
    {
        "id": "ea-starmap-v01",
        "title": "EA-STARMAP-01 v0.1 (this surface's workplan)",
        "author_heteronym": "architectural-canon",
        "zodiacal_region": "center",
        "zodiacal_region_note": "center / recursive inclusion",
        "magnitude_class": "primary_canon_star_M1",
        "main_text": "the workplan",
        "apparatus_status": "present",
        "transformable": True,
        "source_status": "declared",
        "source_path": "/specs/EA-STARMAP-01_v0_1_DRAFT.md",
        "note": "The starmap surface's own workplan. Recursive inclusion."
    },
]

# §3.1 Runtime bindings
RUNTIME_BINDING_ENTRIES = [
    {
        "id": "sharks-space-ark-runtime",
        "title": "The Space Ark v4.2.7 (runtime binding)",
        "author_heteronym": "lee-sharks",
        "zodiacal_region": "aries",
        "magnitude_class": "primary_canon_star_M1",
        "runtime": True,
        "runtime_endpoint": "/api/space-ark/invoke",
        "runtime_endpoint_status": "pending implementation (Phase 5 work)",
        "trigger": "invoke",
        "doi": "10.5281/zenodo.19013315",
        "visual_rendering": "a star that pulses, distinguishing it from static text-stars",
        "selection_behavior": "opens an API session panel rather than a reader",
        "source_status": "declared",
        "note": "Inaugural runtime binding. Architecture declared; runtime endpoint pending Phase 5."
    },
]


# ─────────────────────────────────────────────────────────────────────────
# Existing entries — preserved verbatim by id from the prior canon-stars.json
# ─────────────────────────────────────────────────────────────────────────

EXISTING_INSCRIBED_IDS = {
    "sigil-snub-poemed",
    "sappho-31",
    "sappho-31-catullus-51-pair",
    "tachyon-poem-pair",
    "revelation-john-greek",
    "whitman-leaves-of-grass",
    "cranes-day-and-night",
}


# ─────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────

def main() -> int:
    with CANON_STARS_PATH.open() as f:
        current = json.load(f)

    existing_entries = current.get("canonical_texts", [])
    existing_by_id = {e.get("id"): e for e in existing_entries if e.get("id")}

    # Build the new entries list: preserve existing, then add declared.
    new_entries = list(existing_entries)
    declared_collections = [
        ("§1.1 Greek", GREEK_ENTRIES),
        ("§1.2 Latin", LATIN_ENTRIES),
        ("§1.3 Middle English", MIDDLE_ENGLISH_ENTRIES),
        ("§1.4 Italian", ITALIAN_ENTRIES),
        ("§1.5 English", ENGLISH_ENTRIES),
        ("§1.5.b English — Parked", ENGLISH_PARKED_ENTRIES),
        ("§2.1 Lee Sharks", LEE_SHARKS_ENTRIES),
        ("§2.2 Johannes Sigil", SIGIL_ENTRIES),
        ("§2.3 Jack Feist / LOGOS*", FEIST_ENTRIES),
        ("§2.4 Rebekah Cranes", CRANES_ENTRIES),
        ("§2.5 Other heteronyms", OTHER_HETERONYM_ENTRIES),
        ("§2.6 Architectural canon", ARCHITECTURAL_CANON_ENTRIES),
        ("§3.1 Runtime bindings", RUNTIME_BINDING_ENTRIES),
    ]

    added_count = 0
    skipped_count = 0
    section_counts: dict[str, int] = {}

    for section_name, entries in declared_collections:
        added_in_section = 0
        for entry in entries:
            eid = entry["id"]
            if eid in existing_by_id:
                skipped_count += 1
                continue
            new_entries.append(entry)
            added_in_section += 1
            added_count += 1
        section_counts[section_name] = added_in_section

    # Update top-level metadata.
    updated = dict(current)
    updated["canonical_texts"] = new_entries
    updated["status_note"] = (
        "Star coordinates (target_star_designation) remain null pending Phase 4 "
        "of EA-STARMAP-01 (the HYG star-position assignment). Magnitude classes "
        "and zodiacal regions populated from "
        "/starmap/manifests/canonical-declarations.md. Sharks-authored entries "
        "honor the main / apparatus rule per EA-STARMAP-01 §4.6 and "
        "EA-MANDALA-KERNEL-TRANSFORM-01 v0.2 §8.7 — apparatus is accessible but "
        "not transformable."
    )

    # Write back pretty.
    with CANON_STARS_PATH.open("w") as f:
        json.dump(updated, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"=== Populate complete ===")
    print(f"  Existing (preserved):  {len(existing_entries):>3}")
    print(f"  Added (new declared):  {added_count:>3}")
    print(f"  Skipped (duplicate id):{skipped_count:>3}")
    print(f"  TOTAL:                 {len(new_entries):>3}")
    print()
    print(f"=== By section ===")
    for section_name, n in section_counts.items():
        print(f"  {section_name:<35} {n:>3}")
    print()
    print(f"Wrote {CANON_STARS_PATH.stat().st_size:,} bytes to {CANON_STARS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
