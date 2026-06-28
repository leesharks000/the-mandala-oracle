# The Book

Auto-appended Mandala Oracle conversations. Per UPDATES_REGISTER_2026-06-28-BOOK-ADJUDICATION.md (B-A1 through B-A8):

- **Data home:** here, on the Mandala Oracle's surface.
- **Storage:** file-based; one JSON file per session at `data/AXN-XXXX.json`.
- **Granularity:** per-session — one AXN per conversation, minted from the first witness turn, stable through all subsequent turns.
- **Witness identity:** anonymous by default. Session IDs are hashed before storage; raw IDs never reach disk.
- **Castings:** not yet enabled. When they are, castings will be gated — the witness decides whether to keep.
- **Consumed by:** `alexanarch.org/book/`, which fetches `https://raw.githubusercontent.com/leesharks000/the-mandala-oracle/main/book/index.json` at runtime and renders the conversations as deposit-cards.

## Structure

```
book/
  README.md              ← this file
  index.json             ← flat list of conversation summaries (auto-generated)
  data/
    AXN-XXXX.json        ← one file per conversation
    AXN-YYYY.json
    ...
```

## Schema (per file)

```json
{
  "schema_version": "v1.0",
  "axn": "AXN:XXXX.CONVERSATION.EMOJI1EMOJI2EMOJI3EMOJI4EMOJI5EMOJI6",
  "session_id_hash": "16-char hex",
  "started_at": "2026-06-28T01:00:00Z",
  "last_updated": "2026-06-28T01:15:00Z",
  "mode": "sabbath" | "merkabah",
  "turn_count": 4,
  "witness": "anonymous" | "<attributed-name>",
  "history": [
    { "role": "user", "content": "..." },
    { "role": "assistant", "content": "..." },
    ...
  ]
}
```

## Why an empty .gitkeep instead of seed data

The directory must exist for the first append's GitHub commit to succeed against a known path. No seed conversations are checked in — Phase 1 begins empty and grows as witnesses use the Mandala Oracle.
