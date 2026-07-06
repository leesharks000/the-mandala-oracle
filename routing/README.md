# routing/

Flat, static, machine-facing surface for Mandala Oracle interactions.

Four cross-linked JSONL indexes + a manifest, built once from `book/` and served static.

## Contents

| File | Description | Cardinality |
|---|---|---|
| `manifest.json` | Points at all indexes, records counts and build time | 1 |
| `conversations.jsonl` | One row per witness session (from `book/data/AXN-*.json`) | 90 |
| `readings.jsonl` | One row per reading (from `book/readings/AXN-*.json`) | 45 |
| `casts.jsonl` | One row per transform (flattened from `book/expansions/*.json`) | 91 |
| `sources.jsonl` | One row per source-text corpus (from `book/expansions/`) | 6 |
| `index.html` | Browseable overlay for humans; loads the four JSONL files client-side | — |
| `build.py` | Script that assembles all of the above from `book/` | — |

## Cross-references

- **conversations** → source_text_ids, reading_axns, transform_ids (extracted from turn history)
- **readings** → source_text_id, cast_transform_ids (derived by scanning casts for matching reading_axn)
- **casts** → reading_axn, source_text_id, transform_id (native fields)
- **sources** → reading_axns_all, transform_count, reading_count (aggregated)

The result: pick any node in the graph, walk to any related node in one hop.

## Regeneration

```bash
python3 routing/build.py
```

Idempotent. Overwrites the four JSONL files and the manifest. Run whenever `book/` changes.

## Design principles

- **Flat** — one row per artifact, JSONL not nested JSON. Streamable, greppable, cross-referenceable without traversal.
- **Static** — no runtime state, no API, no build-on-request. Serve as static files.
- **Machine-facing** — JSON is primary; the HTML index is a thin browse overlay for humans. Agents consume the JSONL.
- **Cross-linked** — every reference is resolvable in one hop. Given a conversation, jump to its source texts, readings, and casts. Given a cast, jump to its reading and source. Given a source, walk to every reading and cast made against it.

## Related surfaces

- `book/index.json` — the source-of-truth conversation index (schema v1.0) that `alexanarch.org/book/` fetches for its render. Not replaced; supplemented here.
- `starmap/` — visual/navigable 3D skin over the same underlying data. Consumes conversation, reading, and cast records; renders them as stars, edges, and novae.

The routing surface is the substrate. The Book tab on alexanarch is one view. The Starmap is another view. Both draw from the same rows.
