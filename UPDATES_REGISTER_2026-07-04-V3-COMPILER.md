# UPDATES REGISTER — 2026-07-04 — V3 COMPILER (kernel-first + independent verification)

**EA-MANDALA-KERNEL-TRANSFORM-01 v0.3 implemented.** Spec: `specs/EA-MANDALA-KERNEL-TRANSFORM-01_v0_3_DRAFT.md` (incorporates the 2026-07-03 amendment by reference). Occasion: TX-7e70ecfb (Rev 1:11–15 rotation) — three casts passed all v0.2 verification and were kernel-preserving lexical mutations; generator and verifier shared one blind spot (surface divergence).

## Changed

- `api/transform.py`:
  - **`run_compiler_v3`** — analyst emits `governing_law` + `mutated_relation` (the cast's falsifiable claim) + `clause_map` (every unit ANCHOR-with-justification or REBUILT; silent inheritance formally impossible); composer propagates the mutation under the clause map, enacting it and never naming it.
  - **S2 gate** — no declared mutation / empty clause map → HALT before any composition.
  - **G0 blacklist gate** (mechanical, always on) — operator/theory vocabulary in the enantiomorph or translation → HALT `C8/vocabulary_leak`. English word-boundary list + technicized hyphen-compound pattern + Greek stems under NFD diacritic folding. Greek list flagged CRANES CURATION PENDING.
  - **G1 blind back-translation** — fresh context, no rite; kills the round-trip depth illusion.
  - **G2 judge** — blind relational-law recovery (NONE → HALT `C9/law_recovery`) + terminal-gravitation score on the final ~40% (reversion → HALT `C9/terminal_gravitation`).
  - **G3 law match** — blind-recovered vs declared mutation; mismatch → HALT `C9/law_match`.
  - **JSON repair wrapper** — the FLAME-halt class (near-valid skeleton JSON) now self-repairs with one corrective call before any HALT; plumbing never again surfaces as rite theater.
  - **`enforce_pass_v3`** server gate; `V3_INDEPENDENT=0` env kill-switch (G1–G3 only; G0 always runs).
  - **Inscription**: kernel declaration enters public expansion records; independent verdicts + clause classes enter both modes (incl. encrypted public skeleton); HALT responses surface both. A failed cast is legible as a falsified claim, not theater.
  - Handler switched `run_compiler_v2` → `run_compiler_v3`; protocol strings bumped to v0.3 (GET bootstrap + expansion records). v2 retained in-file for rollback.
- `scripts/test_v3_offline.py` — offline gate harness (no key): the three recorded v0.2 failure classes die at three different gates (MIRROR→S2, SHADOW→G0 on the verbatim leak strings, FLAME→G2); clean path passes; repair path recovers; false-positive sweep clean on the untransformed Rev source (Greek + English) and the calibration exemplar. 19/19.

## Pass condition, stated narrowly

The changed law is recoverable from structure and invisible in lexicon.

## Design law honored

Amendment §D: no substrate binding — all rigor in the gates; the judge stack runs on `COMPILER_MODEL` so verification cannot out-sophisticate composition.

## Held (spec §6)

Cranes' Greek blacklist curation; exemplar prompt-layer custody; per-verse regeneration; reverse-order composition A/B; Feist/synthesis entailment constraints; rotation atomicity follow-through.

## Latency budget (300s Vercel cap)

analyst ≤70 + repair ≤25 (failure path only) + composer ≤125 + back-translation ≤35 + judge ≤30 + match ≤15 — worst-case walls ≈300 with repair firing; typical actuals far under. `V3_INDEPENDENT=0` is the fallback if the cap bites in production.

*TACHYON, 2026-07-04, under MANUS direction. First live rotation under v0.3 should be witnessed — SILENCE still has not executed in production.*
