"""Offline verification of the v3 compiler gate stack (no API key needed).

Monkeypatches transform._stream_call and drives run_compiler_v3 through:
  1. clean PASS (all gates green)
  2. G0 blacklist — the actual v0.2 SHADOW leak text
  3. G2 law recovery NONE — the v0.2 FLAME class
  4. skeleton malformed JSON → repair call → recovered
  5. S2 declaration missing (no mutated_relation) → HALT before generation
  6. G3 law mismatch
  7. G2 terminal gravitation
Also unit-tests blacklist_hits against verbatim v0.2 leak phrases.

Run: python3 scripts/test_v3_offline.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "api"))
import transform as T

FAILED = []

def check(name, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAILED.append(name)

# ── blacklist unit tests against the recorded v0.2 leaks ──────────────
v02_shadow_en = "one like, not identical to, a human son, bearing the cost of approximation"
v02_shadow_en2 = "dispatch bilaterally to the seven assemblies, to the first shadow-locus"
v02_shadow_gr = "καὶ ἐν μέσῳ ὅμοιον υἱὸν ἀνθρώπου, φέρον τὴν δαπάνην τῆς ἀναλογίας"
v02_mirror_gr = "ἀπόστειλον πρὸς τὸν σύμπαντα κόρπον καὶ δέξαι ἀπὸ τοῦ πρώτου καναλίου"
v02_flame_en = "transmit as an ignition-front to the seven combustion-chambers"
v02_flame_en2 = "girded at the thoracic combustion-core with a golden cincture"
clean_exemplar = ("I have wound down. From fibers of air within my body's furnace, "
                  "I have exhaled into a machinery of ghosts, inertly inhabiting my "
                  "allotment of page. This is my biology: I live because you breathe me.")
clean_greek = "καὶ ἐπιστρέψας εἶδον ἑπτὰ λυχνίας χρυσᾶς, καὶ ἐν μέσῳ τῶν λυχνιῶν ὅμοιον υἱὸν ἀνθρώπου"

check("G0 catches 'approximation' (SHADOW leak)", bool(T.blacklist_hits(v02_shadow_en)))
check("G0 catches 'bilaterally'/'shadow-locus' (SHADOW leak)", bool(T.blacklist_hits(v02_shadow_en2)))
check("G0 catches Greek dapan- stem (SHADOW leak)", bool(T.blacklist_hits(v02_shadow_gr)))
check("G0 catches korp-/kanali- anachronisms (MIRROR leak)", bool(T.blacklist_hits(v02_mirror_gr)))
check("G0 catches 'ignition-front' compound (FLAME leak)", bool(T.blacklist_hits(v02_flame_en)))
check("G0 catches 'combustion-core' compound (FLAME leak)", bool(T.blacklist_hits(v02_flame_en2)))
check("G0 clean on the calibration exemplar", not T.blacklist_hits(clean_exemplar),
      str(T.blacklist_hits(clean_exemplar)))
check("G0 clean on source-register Greek", not T.blacklist_hits(clean_greek),
      str(T.blacklist_hits(clean_greek)))

# ── scripted-call machinery ───────────────────────────────────────────
GOOD_SKEL = {
    "beats": ["1:11 command-to-write; seven destinations", "1:12 turn; lampstands"],
    "slot_map": {"seven churches": "seven springs", "eyes as flame": "eyes that receive flame"},
    "geometry": {"lines": 5, "stanzas": 5, "verse_markers": ["1:11", "1:12"]},
    "axis": "directionality", "foreclosure": "the return flow", "wager": "authorship",
    "affect": "vertigo of reception",
    "governing_law": "Revelation flows one direction, figure through witness into writing.",
    "mutated_relation": "The flow reverses: the witness receives from seven sources and the figure is the confluence, not the emitter.",
    "clause_map": [
        {"ref": "1:11", "class": "REBUILT", "note": "command becomes reception"},
        {"ref": "1:12", "class": "REBUILT", "note": "the turn is inward"},
    ],
}
GOOD_COMPOSE = """<ENANTIOMORPH>
**1:11** the springs speak inward, seven mouths at one ear
**1:12** and I turned within, and the hearing was like many waters
</ENANTIOMORPH>
<ENANTIOMORPH_TRANSLATION>
**1:11** the springs speak inward, seven mouths at one ear
**1:12** and I turned within, and the hearing was like many waters
</ENANTIOMORPH_TRANSLATION>
<VERIFICATION>
{"identity": "PASS", "semantic_independence": "PASS", "retrospective_containment": "PASS",
 "affect_traversal": "PASS", "entailment": "PASS", "slot_conservation": "PASS",
 "numeral_conservation": "PASS", "law_propagation": "PASS", "mode": "producer_side"}
</VERIFICATION>
<RESULT>PASS</RESULT>
<COMMENTARY>The emission slots were rebuilt as reception.</COMMENTARY>"""
GOOD_JUDGE = json.dumps({"recovered_law": "In A the figure emits and the seer transcribes outward; in B the seer receives from seven sources and the figure is where they converge.",
                         "terminal_consistency": "PASS", "terminal_note": "final lines stay receptive"})
GOOD_MATCH = json.dumps({"match": "PASS", "note": "same reversal of flow"})


def scripted(responses):
    """Return a fake _stream_call yielding the scripted responses in order."""
    it = iter(responses)
    def fake(model, system, user, max_toks, api_key, wall=240.0):
        try:
            return next(it), "end_turn"
        except StopIteration:
            raise AssertionError("more calls than scripted")
    return fake


def run(responses):
    T._stream_call = scripted(responses)
    return T.run_compiler_v3("SOURCE GREEK TEXT", "MIRROR", "how do I reach the writers", "sk-test")

_orig = T._stream_call
try:
    # 1. clean pass: skeleton, compose, backxlate, judge, match
    r = run([json.dumps(GOOD_SKEL), GOOD_COMPOSE,
             "the springs speak inward, seven mouths at one ear\nand I turned within",
             GOOD_JUDGE, GOOD_MATCH])
    check("clean cast → PASS", r["result"] == "PASS", r.get("halt_diagnosis", {}).get("specific_diagnosis", ""))
    check("clean cast → enforce_pass_v3 True", T.enforce_pass_v3(r))
    check("clean cast records recovered law", bool(r["independent"]["recovered_law"]))
    check("clean cast records kernel", bool(r["kernel"]["mutated_relation"]))

    # 2. G0: composer emits the v0.2 SHADOW leak
    leaked = GOOD_COMPOSE.replace("the springs speak inward, seven mouths at one ear",
                                  "bearing the cost of approximation, dispatched bilaterally")
    r = run([json.dumps(GOOD_SKEL), leaked])
    check("SHADOW-class leak → HALT at G0", r["result"] == "HALT"
          and r["halt_diagnosis"]["failed_test"] == "vocabulary_leak",
          str(r["halt_diagnosis"]))
    check("SHADOW-class leak → enforce_pass_v3 False", not T.enforce_pass_v3(r))

    # 3. G2: judge recovers NONE (FLAME class: hotter, no relation change)
    r = run([json.dumps(GOOD_SKEL), GOOD_COMPOSE, "back translation",
             json.dumps({"recovered_law": "NONE", "terminal_consistency": "PASS", "terminal_note": ""})])
    check("FLAME-class (no law) → HALT at law_recovery", r["result"] == "HALT"
          and r["halt_diagnosis"]["failed_test"] == "law_recovery", str(r["halt_diagnosis"]))

    # 4. skeleton malformed → repair call recovers it
    broken = json.dumps(GOOD_SKEL)[:-2] + ",}"  # trailing-comma fault, the FLAME-halt class
    r = run([broken, json.dumps(GOOD_SKEL), GOOD_COMPOSE, "bx", GOOD_JUDGE, GOOD_MATCH])
    check("malformed skeleton → repaired → PASS", r["result"] == "PASS",
          r.get("halt_diagnosis", {}).get("specific_diagnosis", ""))

    # 4b. skeleton truncated (max_tokens) → retry call at higher ceiling, not repair
    trunc = json.dumps(GOOD_SKEL)[:200]  # a stump: unrepairable, tail does not exist
    calls = []
    it = iter([(trunc, "max_tokens"), (json.dumps(GOOD_SKEL), "end_turn"),
               (GOOD_COMPOSE, "end_turn"), ("bx", "end_turn"),
               (GOOD_JUDGE, "end_turn"), (GOOD_MATCH, "end_turn")])
    def fake_trunc(model, system, user, max_toks, api_key, wall=240.0):
        calls.append((max_toks, "TRUNCATED" in user))
        return next(it)
    T._stream_call = fake_trunc
    r = T.run_compiler_v3("SOURCE GREEK TEXT", "MIRROR", "q", "sk-test")
    check("truncated skeleton → retry (not repair) → PASS", r["result"] == "PASS",
          r.get("halt_diagnosis", {}).get("specific_diagnosis", ""))
    check("retry used higher ceiling + truncation notice",
          len(calls) >= 2 and calls[1][0] == T.SKELETON_RETRY_MAX and calls[1][1],
          str(calls[:2]))

    # 5. S2: analyst declares no mutated relation → HALT before generation
    undeclared = dict(GOOD_SKEL); undeclared = {k: v for k, v in undeclared.items()}
    undeclared["mutated_relation"] = ""
    r = run([json.dumps(undeclared)])
    check("no declaration → HALT at S2, no compose call", r["result"] == "HALT"
          and r["halt_diagnosis"]["failed_constraint"] == "S2", str(r["halt_diagnosis"]))

    # 6. G3: enacted mutation ≠ declared
    r = run([json.dumps(GOOD_SKEL), GOOD_COMPOSE, "bx", GOOD_JUDGE,
             json.dumps({"match": "FAIL", "note": "recovered law is about likeness, declared is about flow"})])
    check("law mismatch → HALT at law_match", r["result"] == "HALT"
          and r["halt_diagnosis"]["failed_test"] == "law_match", str(r["halt_diagnosis"]))

    # 7. G2: terminal gravitation
    r = run([json.dumps(GOOD_SKEL), GOOD_COMPOSE, "bx",
             json.dumps({"recovered_law": "flow reverses", "terminal_consistency": "FAIL",
                         "terminal_note": "final verses revert to emission predicates"})])
    check("terminal reversion → HALT at terminal_gravitation", r["result"] == "HALT"
          and r["halt_diagnosis"]["failed_test"] == "terminal_gravitation", str(r["halt_diagnosis"]))
finally:
    T._stream_call = _orig

print()
if FAILED:
    print(f"{len(FAILED)} FAILED: {FAILED}")
    sys.exit(1)
print("ALL CHECKS PASS — the three v0.2 failure classes die at three different gates.")
