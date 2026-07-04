#!/usr/bin/env python3
"""local_cast.py — run the tip-code compiler against a cast WITHOUT any
deployment (MANUS need, 2026-07-04: Vercel deploy quota walled; Anthropic
key live). Usage:

    ANTHROPIC_API_KEY=sk-... python3 scripts/local_cast.py [--stages 2|3]
        [--source FILE] [--operator STR] [--invoking STR]

Defaults reproduce the halted production cast exactly: Revelation 7:13–17
(including the trailing chapter heading the rite served), SHADOW /
assertion-axis, invoking "joy with the morning?". Prints every artifact:
both checksums, kernel, enantiomorph, gate verdicts, post-mortem on HALT."""
import argparse, json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

DEFAULT_SOURCE = """**7:13** Καὶ ἀπεκρίθη εἷς ἐκ τῶν πρεσβυτέρων λέγων μοι· Οὗτοι οἱ περιβεβλημένοι τὰς στολὰς τὰς λευκὰς τίνες εἰσὶν καὶ πόθεν ἦλθον;

**7:14** καὶ ⸀εἴρηκα αὐτῷ· Κύριέ μου, σὺ οἶδας. καὶ εἶπέν μοι· Οὗτοί εἰσιν οἱ ἐρχόμενοι ἐκ τῆς θλίψεως τῆς μεγάλης, καὶ ἔπλυναν τὰς στολὰς αὐτῶν καὶ ἐλεύκαναν ⸀αὐτὰς ἐν τῷ αἵματι τοῦ ἀρνίου.

**7:15** διὰ τοῦτό εἰσιν ἐνώπιον τοῦ θρόνου τοῦ θεοῦ, καὶ λατρεύουσιν αὐτῷ ἡμέρας καὶ νυκτὸς ἐν τῷ ναῷ αὐτοῦ, καὶ ὁ καθήμενος ἐπὶ ⸂τοῦ θρόνου⸃ σκηνώσει ἐπ' αὐτούς.

**7:16** οὐ πεινάσουσιν ἔτι ⸀οὐδὲ διψήσουσιν ἔτι, οὐδὲ μὴ πέσῃ ἐπ' αὐτοὺς ὁ ἥλιος οὐδὲ πᾶν καῦμα,

**7:17** ὅτι τὸ ἀρνίον τὸ ἀνὰ μέσον τοῦ θρόνου ⸀ποιμανεῖ αὐτούς, καὶ ⸀ὁδηγήσει αὐτοὺς ἐπὶ ζωῆς πηγὰς ὑδάτων· καὶ ἐξαλείψει ὁ θεὸς πᾶν δάκρυον ἐκ τῶν ὀφθαλμῶν αὐτῶν.


## Κεφάλαιον 8"""

DEFAULT_OPERATOR = ("SHADOW — assertion-axis — the bearing-cost ENCODED BY THE UTTERANCE "
                    "(the cost the composition carries, not the historical composer's "
                    "biography); bilateral receptive operation (originary; most potent)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stages", choices=["2", "3"], default="3")
    ap.add_argument("--source")
    ap.add_argument("--operator", default=DEFAULT_OPERATOR)
    ap.add_argument("--invoking", default="joy with the morning?")
    a = ap.parse_args()
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        sys.exit("ANTHROPIC_API_KEY not set")
    if a.stages == "2":
        os.environ["GLYPH_STAGES"] = "2"
    src = open(a.source).read() if a.source else DEFAULT_SOURCE
    import transform as T
    t0 = time.time()
    print(f"── local cast · stages={a.stages} · code tip: {os.popen('git -C ' + os.path.dirname(__file__) + '/.. rev-parse --short HEAD').read().strip()} ──", flush=True)
    parsed = T.run_compiler_v3(src, a.operator, a.invoking, key)
    dt = time.time() - t0
    g = parsed.get("glyphic", {})
    print(f"\n══ SOURCE CHECKSUM ══\n{g.get('source','(none)')}")
    print(f"\n══ MUTATED CHECKSUM ══\n{g.get('mutated','(none)')}")
    k = parsed.get("kernel", {})
    print(f"\n══ KERNEL ══\ngoverning_law: {k.get('governing_law','')}\nmutated_relation: {k.get('mutated_relation','')}\nclause_map: {json.dumps(k.get('clause_map', []), ensure_ascii=False)}")
    print(f"\n══ ENANTIOMORPH ══\n{parsed.get('enantiomorph','(none)')}")
    ind = parsed.get("independent", {})
    print(f"\n══ VERDICTS ══\nresult: {parsed.get('result')}\nblacklist: {ind.get('blacklist')} | recovered_law: {ind.get('recovered_law','')[:200]}\nlaw_match: {ind.get('law_match')} ({ind.get('law_match_note','')[:160]})\nterminal: {ind.get('terminal_consistency')} | law_variance: {json.dumps(parsed.get('law_variance')) if parsed.get('law_variance') else '—'}")
    if parsed.get("result") == "HALT":
        print(f"\n══ HALT ══\n{json.dumps(parsed.get('halt_diagnosis', {}), ensure_ascii=False, indent=1)}")
    print(f"\n── wall: {dt:.1f}s ──")

if __name__ == "__main__":
    main()
