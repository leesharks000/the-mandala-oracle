# scripts/

Regeneration and tooling scripts. All scripts are idempotent — they read from `alexanarch/` (submodule) and write to `rag/`, `sky/`, or `sources/index/` deterministically.

## Planned contents (v1)

- **`regenerate_rag.py`** — reads alexanarch deposits, chunks deposit content, embeds via `sentence-transformers/all-MiniLM-L6-v2`, writes `rag/vectors.json` and `rag/metadata.json`. Origin-tags each entry as `archive | book` for forward compatibility with the Book sub-area (v2+).
- **`regenerate_sky.py`** — reads `rag/vectors.json`, runs UMAP to 3D, computes lineage edges from deposit metadata, writes `sky/coords.json`, `sky/edges.json`, `sky/planets.json` (the seven planetary body positions are computed from constants, not from the corpus).
- **`regenerate_sources_index.py`** — reads `sources/` corpus, generates `sources/index.json` for Sigil reference and rite-producer source-selection (v2).

## Discipline

All output JSON files use the alexanarch compact-JSON discipline: `indent=None`, `separators=(',',':')`, `ensure_ascii=False`. This is the standing convention from the post-mint protocol; deviating would break the architecture's data-layer continuity.
