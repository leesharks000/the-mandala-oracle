# /starmap/ — The Starmap Preparation Container

This directory is the **working container** for the navigable-starmap surface of the Mandala Oracle. Per Lee Sharks's session-direction (2026-06-28, post-gap-round resumption), this is a *separate container* from both the deployed starmap rendering (which will live at `/starmap` route in production) and from the chat surface (`/`, the reading surface).

The container holds the *preparation and population work*: the manifests that declare what is in the canon, the public-domain source texts being staged for inclusion, and the tools that fetch and process them. When a canon-text is ready for inscription, its rendering metadata is committed up to `/data/canon-sky/canon-stars.json` and its source text is committed to `/sources/<text-id>/` per the rendering surface's source-storage convention (EA-STARMAP-01 v0.1 §4.5).

## Architectural Companion Documents

The working specifications that this container implements:

- **`/specs/EA-STARMAP-01_v0_1_DRAFT.md`** — The Navigable Starmap workplan. The architecture, the visual layout (horizontal spine of seven + zodiacal band of twelve + non-zodiacal star field), the knowledge-graph edge taxonomy, the room↔zodiac wiring, the implementation phasing.
- **`/specs/EA-MANDALA-MERKABAH-01_v0_8_AMENDMENT.md`** — The two-surface architectural decision (reading surface vs starmap surface). The companion that establishes *why* this container exists.
- **`/specs/EA-MANDALA-KERNEL-TRANSFORM-01_v0_2_DRAFT.md`** — The kernel-transform protocol. Per the new main-vs-apparatus rule (EA-STARMAP-01 §4.6, this update), only main-text portions of human-authored works are admissible as input to kernel-transforms. Apparatus is accessible but not transformable. This container's manifests carry the main/apparatus distinction at the source.
- **`/WORKPLAN.md`** — The master workplan that contextualizes everything.

## Subdirectory Function

### `manifests/`

The *canonical declaration list*. Plain-text and Markdown files that enumerate which texts are in the canon, in what original language they will be sourced, what their author-heteronym attribution is, what magnitude class they receive, and whether they have main-text and apparatus components (with the apparatus marked as `transformable: false`). The manifest is the authoritative scope document; everything in `sources/` must be backed by a manifest entry.

Key files (to be populated):

- `canonical-declarations.md` — the human-readable master list. Includes both public-domain primary texts and Sharks-authored / heteronym-authored works. Each entry carries: title, original language, author-heteronym (or anonymous), zodiacal region assignment, M-class, main/apparatus split (where applicable), source availability, AXN identifier (if Sharks-authored).
- `public-domain-greek.md` — Greek-language texts (Sappho, Plato, Heraclitus, Parmenides, Pre-Socratics, Homer, NA28 Greek New Testament).
- `public-domain-latin.md` — Latin-language texts (Augustine, Lucretius, Cicero, Catullus).
- `public-domain-vernacular.md` — Middle English Pearl, Italian Dante, English Whitman / Dickinson / Hopkins / KJV / Shakespeare.
- `sharks-authored.md` — Lee-authored works (Pearl and Other Poems, Secret Book of Walt, Water Giraffe Cycle, Snub-Poemed, Gospel of Antioch, Antioch: a heteronym compendium, Feist function transformed Feist force, etc.). Each entry marks the main-text portion vs. the apparatus (which is accessible but not transformable).
- `runtime-bindings.md` — the entries that are not static texts but *runtime environments callable from the starmap surface*. The Space Ark v4.2.7 is the inaugural entry (trigger word "invoke"; DOI 10.5281/zenodo.19013315). Future runtime bindings include any heteronymic operator that compiles to a callable API surface.

### `sources/`

The staging area for public-domain text fetches. Files are organized by language and provenance:

```
sources/
  ├── greek/
  │   ├── sappho-voigt-edition.txt
  │   ├── plato-phaedrus.txt
  │   ├── heraclitus-diels-kranz.txt
  │   ├── parmenides-on-nature.txt
  │   ├── homer-iliad.txt
  │   ├── homer-odyssey.txt
  │   └── na28-new-testament/
  │       ├── apocalypse-of-john.txt
  │       └── ...
  ├── latin/
  │   ├── augustine-confessions.txt
  │   ├── lucretius-de-rerum-natura.txt
  │   └── catullus-51.txt
  ├── middle-english/
  │   └── pearl-anonymous.txt
  ├── italian/
  │   └── dante-commedia-petrocchi.txt
  ├── english/
  │   ├── whitman-leaves-of-grass-deathbed.txt
  │   ├── dickinson-variorum.txt
  │   ├── kjv-authorized-version.txt
  │   └── shakespeare-sonnets.txt
  └── README.md
```

The source texts in `/starmap/sources/` are *staging* — they exist here to be reviewed for textual quality, encoding, and apparatus-handling before being moved or copied to the production `/sources/<text-id>/` layout that the rendering surface consumes. The staging step matters: many public-domain editions on the web carry critical-apparatus material that is itself under copyright (the Voigt apparatus issue per EA-STARMAP-01 §7.5). The staging directory is the place where apparatus is identified and either independently transcribed or marked for citation-by-reference only.

### `tools/`

Scripts and small utilities for the prep work. None exist yet; the directory exists in anticipation. Future entries will include:

- `fetch-perseus.py` — Pull from the Perseus Digital Library (CTS URN-addressable Greek and Latin source texts, MIT/Tufts).
- `fetch-gutenberg.py` — Pull from Project Gutenberg (vernacular public-domain texts).
- `na28-extractor.py` — Process the NA28 Greek New Testament base text (which itself has licensing nuances; the Nestle-Aland 28th edition's *text* is widely cited but the *apparatus* is copyrighted).
- `apparatus-splitter.py` — For sources that arrive as a single file with critical apparatus interleaved, the splitter produces a `main.txt` and an `apparatus.md` to honor the main-vs-apparatus rule (EA-STARMAP-01 §4.6).
- `validate-manifest.py` — Cross-check that every entry in `manifests/canonical-declarations.md` has a corresponding source file (or a `[stub]` marker) and that the metadata is well-formed.

## Workflow

1. **Declare.** A text is named in `manifests/canonical-declarations.md` (or in one of the language-specific sub-manifests). The declaration includes attribution, magnitude class proposal, and where the source will come from.
2. **Stage.** The source text is acquired (Perseus, Gutenberg, archive.org, scholarly editions in PD) and placed in `sources/<language>/<text-name>.txt` (or appropriate subdirectory).
3. **Split (if needed).** Where the source includes critical apparatus that must be separated per §4.6, the apparatus splitter produces clean `main.txt` and `apparatus.md` files.
4. **Promote.** Once reviewed, the source moves (or copies) to `/sources/<text-id>/` in the production source layout. The corresponding entry is added to `/data/canon-sky/canon-stars.json` with its `target_star_designation` (the HYG star it will be rendered at) and edges (per §3.2 edge taxonomy).
5. **Render.** The starmap surface picks up the new canon-star on next deploy.

## Status

**As of 2026-06-28, post-gap-round resumption:** Container created with subdirectory structure. Manifests are stubs awaiting Lee Sharks's adjudication on:

- The complete first-issue text list (EA-STARMAP-01 §4.2 and §4.3 catalog the candidates; §7 open questions list 10 items needing adjudication).
- The Antioch question (§7.7 — provisionally resolved this session: Gospel of Antioch and Antioch: a heteronym compendium are distinct works; needs Lee's ratification).
- The Feist transformation pair (§7.8 — now named *Feist function transformed Feist force*; needs Lee's confirmation that this is the canonical naming).
- The Voigt apparatus problem (§7.5).
- The heteronym discipline-lines for the six positions still marked TBD (§7.9).
- The blessed-translations question (§7.6).

No source texts have been staged yet. No tools have been written. The container is scaffolding for the work that follows.

---

*This README is itself a kind of canonical declaration: a declaration that this container exists, with this scope, for this purpose. Updates to scope are appended below as the work proceeds.*
