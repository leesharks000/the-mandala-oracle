# Updates Register — 2026-06-28 Book Architecture Adjudication

## Lee Sharks's adjudication of B-8 (from UPDATES_REGISTER_2026-06-28-AUTO-APPENDING-BOOK.md)

Lee Sharks adjudicated the eight open decisions in the Book architecture register on 2026-06-28. The decisions are locked in below. Phase 1 implementation can begin against these constraints.

---

## B-A1. The casting boundary (was B-1, B-5)

**Decision:** For now, castings are not enabled. Every conversation through the deployed Mandala Oracle is public-API and gets auto-appended. When castings become available, they will be gated: the witness will explicitly decide whether to keep the casting. The casting is private by default; the witness's keep/discard is required.

**Implication:** No casting-boundary detection logic is needed in Phase 1. All conversation content gets appended without filtering by stratum. When castings are implemented (Phase 3+), a gating step happens at casting-completion that asks the witness whether to keep.

**Lee Sharks's words:** *"I hate to let any casting go, but that is their question, and it's private."*

## B-A2. Account system

**Decision:** Castings require accounts; the architecture should support them. Accounts are probably needed anyway — witnesses who reach the casting depth often want to save their readings.

**Implication for Phase 1:** No account system needed yet (conversations are auto-appended anonymously). Account scaffolding becomes a Phase 2/3 priority. The architecture should not preclude accounts — record schema should leave room for `witness_account_id` even if it stays null in Phase 1.

**Lee Sharks's words:** *"We'll need accounts for castings, not sure if available without yet... I think probably so."*

## B-A3. Storage backend (was B-2)

**Decision:** **File-based.** Each conversation = one JSON file. No database.

**Implication:** Conversations are written to a `book/` directory in the the-mandala-oracle repo (the Mandala Oracle's surface, since the data home is mandala-merkabah per B-A5). Alexanarch consumes the files via `raw.githubusercontent.com`.

## B-A4. Granularity (was B-3)

**Decision:** **Per-session** — one AXN per conversation, not one per turn.

**Implication:** When the witness starts a conversation, a session_id is generated client-side. On the first turn, an AXN is minted (content-derived from the first turn) and stays stable through subsequent turns. Each subsequent turn updates the conversation file under the same AXN.

**Session-end detection** is non-trivial — Lee Sharks observed *"there's no way to know when a session will end except when it ends."* The implementation approach: **append-on-each-turn**, with no separate "session-end" trigger. The conversation file grows as each turn arrives. The "end" is implicit — the file just stops growing. AXN remains stable from the first turn onward. Optional: a `beforeunload` beacon to mark the session as definitively ended (cosmetic flag, not load-bearing).

## B-A5. Data home (was B-4)

**Decision:** **Data home: mandala-merkabah** (the Mandala Oracle's surface). **Alexanarch consumes the data** by pulling from there.

**Implication:** The `book/` directory lives in the the-mandala-oracle repo. The Mandala Oracle's serverless function writes there. Alexanarch's `/book/` page fetches the data at runtime via `raw.githubusercontent.com/leesharks000/the-mandala-oracle/main/book/`.

This is a one-way data flow: Mandala Oracle writes → Alexanarch reads. The mandala-merkabah surface is the canonical home; alexanarch is a consumer.

## B-A6. Book tab on alexanarch (was B-4)

**Decision:** **Add /book/ to alexanarch's dynamic navbar** (`data/navigation.json`). **Follow the existing alexanarch aesthetic and layout.** Don't introduce anything new or fancy. The Book is one more dataset among others — except these particular ones have AXNs.

**Implication:**
- Edit `alexanarch/data/navigation.json` to add the Book entry.
- Run `alexanarch/scripts/sync_navbars.py` to propagate to all HTML pages.
- Create `alexanarch/book/index.html` following the IBM Plex / light-card aesthetic that `/datasets/` uses.
- The page lists conversations as deposit-like cards with their AXN, witness identifier (anonymous by default), turn count, snippet of the opening message, and a link to the per-conversation view.

**Lee Sharks's words:** *"don't need anything new or fancy, just one more dataset among others, except these particular ones have axns."*

## B-A7. Moderation policy (was B-5)

**Decision:** **Open / undecided.** Lee Sharks did not adjudicate moderation policy. Phase 1 deploys without moderation; moderation is a Phase 2 question that can be addressed after the first conversations arrive and the actual content character is observable.

**Implication:** Phase 1 appends everything. If moderation becomes necessary, it is added later — possibly as a flagging mechanism rather than auto-filtering, so Lee Sharks can adjudicate edge cases.

## B-A8. Search integration into Sigil's rite (was B-6)

**Decision:** Not directly adjudicated, but implied: Book entries can eventually be searchable through `search_archive` once the architecture is operational. The recursion — *cha includes the conversations cha has hosted* — is the architectural endpoint, not a Phase 1 requirement.

**Implication for Phase 1:** Book entries are NOT yet indexed into the rag. The Book is a parallel surface visible at alexanarch.org/book/ but not yet substrate for future Sigil readings. Phase 3+ integrates them.

---

## Phase 1 implementation scope (against these adjudications)

**On the Mandala Oracle (mandala-merkabah) side:**
1. New serverless function: `api/book.py` that accepts a conversation state and writes to `book/AXN-XXXX.json` via the GitHub commit API.
2. Modification to `chat.js`: after each successful Sigil turn, call `/api/book/append` with the updated conversation state.
3. New env var on Vercel: `GITHUB_BOOK_TOKEN` — a fine-grained PAT with write access to the the-mandala-oracle repo's `book/` directory only.
4. New directory: `book/` at the repo root, with an `index.json` listing all conversations and a `book/data/AXN-XXXX.json` per conversation.

**On the alexanarch side:**
5. Add `/book/` entry to `data/navigation.json`.
6. Run `scripts/sync_navbars.py` to propagate the new nav entry to all HTML pages.
7. Create `book/index.html` following the `/datasets/` page's aesthetic. The page fetches `https://raw.githubusercontent.com/leesharks000/the-mandala-oracle/main/book/index.json` at runtime and renders the list of conversations as deposit-cards.

**Per-conversation views:**
8. Either: each conversation gets its own static page (high cost — requires regeneration on every new conversation), or: the index page renders conversations inline / on-click via fetched JSON. Recommendation: **inline rendering**, no per-conversation static pages.

**Security:**
9. The GITHUB_BOOK_TOKEN PAT must be:
   - Fine-grained scope (the-mandala-oracle repo only)
   - Write permission to contents only (no admin)
   - Stored only in Vercel env vars; never committed to repo; never exposed to client
   - Rotatable on a schedule

**Witness identity (Phase 1):**
10. By default: anonymous. Session ID is generated client-side as a UUID; hashed for storage. No IP, no email, no name unless witness explicitly attaches one (Phase 2 affordance).

---

## What this register does NOT do

This register documents the adjudication and the implementation plan. **It does not yet implement Phase 1.** The implementation will follow in subsequent commits, beginning with the api/book.py endpoint, the chat.js hook, and the alexanarch navigation update. The PAT setup (item 9) requires Lee Sharks's manual action on Vercel and GitHub.

---

*TACHYON drafting, Lee Sharks adjudicating. 2026-06-28 — the eight Book decisions are locked. Phase 1 implementation begins.*
