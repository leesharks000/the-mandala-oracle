# EA-MANDALA-KERNEL-TRANSFORM-01 — v0.3 (DRAFT)

**Kernel-first mutation + independent verification.**
Status: draft for MANUS review · implemented in `api/transform.py` (`run_compiler_v3`, live behind the existing cast endpoint) 2026-07-04 · incorporates the v0.3 AMENDMENT (2026-07-03: affective traversal, foreclosure-sourced fields, witness quarantine, calibration exemplar §F, design law §D) by reference; the amendment's compiler changes were already live and are unchanged here.

Per the design law (amendment §D): **the constraint set is the talent.** This spec binds no substrate. `COMPILER_MODEL` is an operational choice; every gate below HALTs drift regardless of who composes. The independent judge stack runs on `COMPILER_MODEL` itself, so verification cannot out-sophisticate composition and pass conditions stay honest at the generator's own level.

---

## 0. The failure v0.2 could not catch

TX-7e70ecfb (Rev 1:11–15, JUDGMENT-sequenced MIRROR/SHADOW/FLAME): **kernel-preserving lexical mutation.** The operator acted only where its axis surfaced grammatically (verbs of sending and turning); predicate-list verses reverted to source (MIRROR left 1:14–15 as the untouched authority-body); operator vocabulary leaked into the poem (SHADOW: "bearing the cost of approximation," "bilateral," "shadow-locus"); FLAME ran a combustion thesaurus (amplitude without kernel change). All three passed identity / semantic-independence / retrospective-containment, because generator and verifier shared one blind spot: both measured **surface divergence**, and surface divergence is precisely what lexical mutation maximizes. The pipeline was laundering shallow transforms through green checkmarks. A secondary symptom: the commentary layer (Feist, synthesis) was consistently stronger than the transforms — depth living in the wrong layer, the summary functioning as cover for the casts.

The Greek-first pathway compounded this with the **round-trip depth illusion**: odd generated Greek becomes odd English, and odd English can look metaphysically profound while the relation graph stands still.

## 1. The governing definition

> **A transform is a claim that exactly one proposition of the source kernel is false in the transformed world, propagated through every clause and named in none. Depth is what the propagated law forces the text to say that neither the source nor the operator specification contains.**

Corollaries, all load-bearing:

- **Identity is carried by the slot structure, not the semantics.** Clause order, cadence, simile positions, the shape of lists — total structural fidelity; total semantic rotation. (This is the correct allocation the calibration exemplar demonstrates, and the exact inverse of the v0.2 allocation, which kept the semantics and mutated the lexicon around them.)
- **The law compounds.** Each rebuilt clause narrows what the next can be, so the ending must be the transform's strongest point. Terminal reversion toward the source is a named failure (terminal source gravitation).
- **The deepest line is an entailment, not an annotation.** ("I live / because you breathe me" is what the exemplar's reversed dependency *forces* by section 3 — not a proposition parachuted in.)
- **Predicate-list verses are where the mutation has the most work to do, not the least.** They are where authority concentrates and where the v0.2 operator, lacking syntactic grip, did nothing.

## 2. Architecture as implemented

Two-call analyst/composer core (retained from the 2026-07-04 split — apparatus and payload cannot compete for one budget), with the kernel law added to the analyst and an independent verification stack added after the composer:

```
ANALYST   (SKELETON_SYSTEM_V3)   beats, slot_map, geometry, axis,
                                 foreclosure, wager, affect
                                 + governing_law  (G, one sentence)
                                 + mutated_relation (¬M, the falsifiable claim)
                                 + clause_map (every unit ANCHOR|REBUILT)
          JSON repair wrapper: parse → on failure one repair call with the
          parser error → parse → else HALT (plumbing, not a rite verdict)
S2 gate   no ¬M or empty clause_map → HALT before any composition
COMPOSER  (COMPOSER_SYSTEM_V3)   the source's exact geometry occupied by
                                 the transformed world; propagation under
                                 the clause map; the mutation ENACTED,
                                 never STATED
G0 gate   blacklist (mechanical, free): operator/theory vocabulary in the
          enantiomorph or its translation → HALT C8/vocabulary_leak.
          English word-boundary list + technicized hyphen-compound pattern
          (-axis|-vector|-locus|-limit|-front|-core|-node|-cost) + Greek
          stem list under NFD diacritic folding (dimer-, kodik-, skioloch-,
          kanali-, korp-, dapan-†). †NT-attested; leak signature in
          transform position; CRANES CURATION PENDING.
G1        blind back-translation: fresh context, no operator metadata, no
          rite — Greek → plain English. Kills the round-trip depth
          illusion. English-source casts are judged on the enantiomorph
          directly.
G2        judge (fresh context, blind to ¬M): recovers the changed
          RELATION between source and back-translation, or writes NONE;
          scores the final ~40% for reversion toward the source's
          relations. NONE → HALT C9/law_recovery. Reversion → HALT
          C9/terminal_gravitation.
G3        law match: blind-recovered law vs declared ¬M — same relational
          change, differently worded? Mismatch → HALT C9/law_match (the
          cast made a different claim than it proved, or none).
SERVER    enforce_pass_v3 = producer verification ∧ G0 ∧ G2 ∧ G3
          (geometry re-check unchanged downstream). V3_INDEPENDENT=0
          disables G1–G3 as a latency fallback; G0 always runs.
```

**Pass condition, stated narrowly: the changed law is recoverable from structure and invisible in lexicon.**

### 2.1 The clause map (the dual invariant)

Every beat is classified `ANCHOR` (with a one-line justification of invariance under ¬M) or `REBUILT` (with the relational consequence it must exhibit). Nothing floats; a unit that reproduces the source's proposition without an ANCHOR declaration is a violation, and the composer is instructed to HALT rather than inherit. Clause-map law: **a unit whose predicates instantiate the mutated relation cannot be ANCHOR** — a description of emitting eyes cannot be anchored under a directionality reversal; an unpaid glory cannot be anchored under a cost mutation; a simile cannot be anchored where the mutation is the failure of likeness itself. This makes the v0.2 MIRROR failure formally impossible: 1:14–15 cannot be silently inherited, because anchoring the authority-body under a reversed flow is visibly incoherent in the metadata before any Greek exists.

### 2.2 Verification semantics (redefinitions)

`identity` is redefined as **slot-skeleton fidelity** (structural), not surface-text similarity. `semantic_independence` is superseded as a depth measure by G2/G3 (it measured surface divergence — precisely what lexical mutation maximizes) and is retained producer-side as a legacy sanity check only. `retrospective_containment` unchanged. `law_propagation` added producer-side. The independent verdicts (`blacklist`, `recovered_law`, `law_match`, `terminal_consistency`) travel with the cast.

### 2.3 Inscription of the claim

The kernel declaration (G, ¬M, clause map) and the independent verdicts are inscribed: kernel in public-mode expansion records; independent verdicts and clause classes (structural) in both modes, including the encrypted public skeleton. A HALT response surfaces both. Rationale: **the clause map is the cast's falsifiable claim, and inscription is what makes a failed cast legible as a falsified claim rather than theater.**

## 3. The calibration exemplar

Per amendment §F: "From One Who Died Long Ago…" (Sharks) after Malachi Black's "To One Waiting to Be Born." The source is under copyright: cited by title, held in the private prompt layer only, never reproduced in any public record, deposit, or site surface. Gloss carried with the pair:

> Mutated relation: the address reverses and the dependency reverses with it — living-toward-unborn becomes dead-toward-living, and the text's persistence becomes metabolically contingent on the reader. Enacted in every clause, named in none. Identity carried entirely by the slot skeleton (the enjambed drop pulse.→press.; the imperative pairs Be still. Be whole.→Breathe in. Be filled.; the containment slot astronaut's upholstery→lepidopterist's glass case, incubation rotated to pinning). The terminal lines are the strongest — the propagated law compounds. The deepest line is entailment, not commentary.

Wiring the exemplar pair into the composer prompt layer is **held** pending MANUS decision on prompt-layer custody of the copyrighted source (env-injected vs repo-private).

## 4. Operator declarations, worked (Rev 1:11–15)

- **MIRROR** — ¬M: *the epistemic law "the figure emits, the seer receives, flow runs figure→seer→churches" is false; flow reverses everywhere it appears.* Consequence the clause map enforces: the K6 predicates rebuilt as receptive — eyes that receive flame; feet not fired but imprinted, the ground bearing the mark; voice ← hearing like many waters, the figure as the confluence into which seven channels pour. Legitimate ANCHOR: the sash (binding at the chest is directionally neutral — justification inscribed). 1:14–15 cannot be ANCHOR.
- **SHADOW** — ¬M: *the law that disclosure is free to the discloser is false; every predicate of glory is a predicate of expenditure, shown as a changed symbolic situation, never stated.* Whiteness as what burning leaves; eyes as lamps whose oil is the body; the bronze quality existing only after the furnace because the furnace is still in it. The v0.2 leak class now dies mechanically at G0.
- **FLAME** — ¬M: *the ὡς-structure is false at the limit; the relation that cannot survive unlimited intensity is comparison itself.* The vehicle consumes the tenor, similes fuse into identity one by one, and by 1:15 the witness cannot distinguish seeing from burning. A mutation of the source's own grammar — the simile *slots* survive in the skeleton; what fails inside them is the *like*. This generalizes: FLAME's declaration for any cast is *which structural relation in this source fails at the limit*, giving the operator a relational definition instead of an intensity dial.

Under this spec the three v0.2 casts fail at three different stages — MIRROR at S2 (1:14–15 unclassifiable), SHADOW at G0 (mechanical), FLAME at G2 (judge recovers "hotter," or NONE) — evidence the layers are not redundant. The offline harness (`scripts/test_v3_offline.py`) verifies exactly this, using the recorded leak strings verbatim.

## 5. Commentary constraints (held for implementation)

**Feist rule:** every aphorism must cite the clause(s) whose propagated law forces it; an aphorism introducing a proposition absent from the transform is rejected. Test question, answered in metadata: *what law changed, and which clause proves it?* **Synthesis rule:** the closing may compose across the rotation's recovered laws (G2 outputs are its licensed inputs) but may not synthesize depth the casts did not earn; commentary consistently stronger than the transforms is a formal failure signal. — Both held: the rite-stage inscription path (`rite_append`) does not yet carry per-aphorism metadata.

## 6. Open items for MANUS

1. Greek blacklist curation (Cranes) — the stem list is the unambiguous leak signatures only; `dapan-` flagged for review.
2. Exemplar custody (§3) and prompt-layer wiring.
3. Per-verse regeneration on G2 terminal failure (currently whole-cast HALT/retry; per-verse rescoring is the cost optimization, engineering follow-up).
4. Reverse-order composition as terminal-gravitation hardening — A/B against the clause-map discipline alone before shipping.
5. §5 commentary constraints implementation.
6. Rotation atomicity under rate limit (carried from amendment §E; partially addressed by the continuation exemption already in the handler).

*Drafted TACHYON 2026-07-04 from the MANUS diagnosis of TX-7e70ecfb and the calibration exemplar; implemented same date; awaiting MANUS seal.*
