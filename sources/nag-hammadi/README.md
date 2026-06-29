# Nag Hammadi Library — Source Acquisition Pending

## Status

This directory is a **declaration container** for the Nag Hammadi Library
(NHL). The Coptic source text is not yet staged here; per Lee Sharks's
adjudication 2026-06-28, transforms work from the Coptic originals, so any
full inscription requires the Coptic critical text.

## Priority codices for staging

See `metadata.json` for the full 13-codex priority list. The highest-priority
items for staging are:

1. **Apocryphon of John** (NHC II,1) — Sethian revelation dialogue;
   cosmogony; the longest of the Sethian texts
2. **Gospel of Thomas** (NHC II,2) — 114 sayings; arguably the most
   independent of the canonical Gospels
3. **Gospel of Philip** (NHC II,3) — Valentinian sacramental discourse
4. **Gospel of Truth** (NHC I,3) — Valentinian homily

## Source pathways

- **Coptic Gnostic Library** (Brill, 1975-1995) — 5 volumes; the
  standard scholarly Coptic transcription
- **Facsimile Edition of the Nag Hammadi Codices** (Brill, 1972-1984;
  12 vols.) — high-resolution facsimile images for direct transcription
- **The Nag Hammadi Library in English**, ed. Robinson (Brill, 1988) —
  English translations only; not the canonical source for transformation
- **The Nag Hammadi Scriptures**, ed. Meyer (HarperOne, 2007) — newer
  English translations; also not canonical source

## Per Lee's adjudication 2026-06-28

> "We also need [...] nag hammadi [...] transforms work from the original
> language"

The transformation operations require the Coptic original. English
translations may accompany as companion artifacts but are not transformable.

## Why this is staged as declaration-only

Acquiring the full Coptic text of all 52 NHL texts requires either:
1. Manual transcription from the Brill facsimile editions (which are
   physical/scanned-not-easily-machine-readable)
2. Licensed access to the CGL critical edition
3. Existing digital corpora (e.g., the
   [Coptic Scriptorium](https://copticscriptorium.org/) project) which has
   some but not all NHL texts in TEI XML

The Coptic Scriptorium is the most promising machine-accessible source.
A future session should fetch their `corpora` repo and identify NHL texts.
