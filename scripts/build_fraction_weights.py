#!/usr/bin/env python3
"""build_fraction_weights.py — how Rex Fraction leans over the archive (draft 0.2, 2026-10-14).

The whole archive is open to him. Rex Fraction is an authorial function that organizes the archive to particular effect
(operator, 2026-10-14: "it is not to be achieved by artificial boundedness. rex fraction is an authorial function that
organizes the archive to particular effect"). This file gives his search two things, neither of which excludes a record:

  w      ORIENTATION, one number per deposit in [0,1]: how near the record stands to the ground he works from.
         Seeds: what spxi.dev and semanticeconomy.org link, and his own deposits. Spread: a random walk with restart
         over the archive's citation graph (alexanarch data/citation-graph.json), forward along citations and, more
         weakly, back to citers discounted by how much each cites; scored as LIFT over the same walk from a uniform
         start, so records everything cites (room anchors, registries, maps) do not rise on that alone. Versions: a
         superseded record passes most of its weight to its successor. Reception does NOT add to w: a machine citing a
         record records reception, mistaken reception included, not authority.
  roles  WHAT WORK THE RECORD DOES, from where the sites place it (the page that links it), then from its title:
         definition, specification, instrument, service, theory, case, record; plus `observed` when machine answers
         have cited it (the capture join). A record may hold several.

In search: score = keyword_score * (1 + K*w) * (ROLE_BOOST if the requested role is among the record's roles else 1).
Fraction names the role a question asks for (a 'what is' question asks for definition; an audit question for service).
"""
import collections, datetime, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
AX = ROOT.parent / "alexanarch"
SPXI = ROOT.parent / "spxi-dev"
K, ROLE_BOOST = 1.0, 1.6
REC = re.compile(r"alexanarch\.org/s/records/(\d+)")

# the page that links a record says what work the record does there
SPXI_ROLE = {"": None, "what-is-spxi": "definition", "disambiguation": "definition", "who": None, "where": None,
             "methods": "specification", "standing-protocol": "specification", "tlp": "specification", "csp": "specification",
             "how-it-works": "specification", "v0.2": "specification", "symbolon": "specification", "holographic-kernel": "specification",
             "compression-arsenal": "specification", "conformance": "instrument", "canary-registry": "instrument", "evidence": "instrument",
             "overview-watch": "instrument", "encounters": "case", "analog": "case", "case-study": "case", "field-notes": "case",
             "retrieval-basin": "case", "geocoded-basin": "case", "lateral-field-bleed": "case", "retrieval-settlement": "case",
             "after-syntax": "case", "phase-i": "case", "aeo": "theory", "the-substrate": "theory"}
SE_ROLE = {"index": None, "brief": "definition", "semantic-economy-framework": "definition", "faq": "definition",
           "disambiguation": "definition", "library": None, "position": None, "practice": "service",
           "erasure-skew": "instrument", "snw": "instrument", "rtt": "instrument", "mediation-ratchet": "instrument",
           "composition-layer-capture": "instrument", "tpa": "instrument", "mfgl": "instrument", "measurement-sovereignty": "instrument"}
TITLE_ROLE = [(r"encyclotron audit|sample encyclotron|what we build", "service"),
              (r"\bprotocol\b|specification|metadata packet", "specification"),
              (r"capture registry|registry|index v|resolution index|census|ledger", "record"),
              (r"instrument|measure|metric|rate\b|diagnostic|observatory|test\b", "instrument"),
              (r"canonical definition|disambiguation|≠| is not |: a (formal )?(specification|definition)|framework for", "definition")]


def rev(path):
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=path, text=True).strip()
    except Exception:
        return None


def main(se_dir):
    se_dir = pathlib.Path(se_dir)
    meta = json.loads((ROOT / "rag/metadata.json").read_text(encoding="utf-8"))
    by = {r["deposit_number"]: r for r in meta if isinstance(r.get("deposit_number"), int)}
    N = set(by)
    roles = collections.defaultdict(set)
    spxi, se = set(), set()
    for p in SPXI.glob("**/index.html"):
        if "node_modules" in p.parts or "scripts" in p.parts:
            continue
        top = p.parent.relative_to(SPXI).parts[0] if p.parent != SPXI else ""
        for n in {int(x) for x in REC.findall(p.read_text(encoding="utf-8", errors="replace"))} & N:
            spxi.add(n)
            if SPXI_ROLE.get(top, "theory"):
                roles[n].add(SPXI_ROLE.get(top, "theory"))
    for p in se_dir.glob("*.html"):
        for n in {int(x) for x in REC.findall(p.read_text(encoding="utf-8", errors="replace"))} & N:
            se.add(n)
            if SE_ROLE.get(p.stem, "theory"):
                roles[n].add(SE_ROLE.get(p.stem, "theory"))
    for n, r in by.items():
        t = (r.get("title") or "").lower()
        for pat, role in TITLE_ROLE:
            if re.search(pat, t):
                roles[n].add(role)
        if not roles[n]:
            roles[n].add("case" if r.get("family") == "GENERATIVE" else "theory")
    rex = {n for n, r in by.items() if "Fraction" in (r.get("creator") or "")}
    seed = collections.Counter()
    for n in spxi | se:
        seed[n] += 3.0
    for n in spxi & se:
        seed[n] += 1.0
    for n in rex:
        seed[n] += 1.0

    g = json.loads((AX / "data/citation-graph.json").read_text(encoding="utf-8"))
    fwd, back = collections.defaultdict(set), collections.defaultdict(set)
    for e in g["edges"]:
        s, t = e.get("source_deposit"), e.get("target_deposit")
        if s in N and t in N and s != t:
            fwd[s].add(t); back[t].add(s)
    outdeg = {n: len(fwd.get(n, ())) for n in N}

    def walk(P):
        r = dict(P)
        for _ in range(40):
            nxt = collections.Counter({n: 0.25 * p for n, p in P.items()})
            for n, v in r.items():
                outs = [(t, 0.8 / max(1, len(fwd[n]))) for t in fwd.get(n, ())]
                outs += [(c, 0.2 / max(1.0, outdeg[c] / 10)) for c in back.get(n, ())]
                if not outs:
                    nxt[n] += 0.75 * v; continue
                z = sum(w for _, w in outs)
                for t, w in outs:
                    nxt[t] += 0.75 * v * w / z
            r = dict(nxt)
        return r
    tot = sum(seed.values())
    ppr = walk({n: v / tot for n, v in seed.items()})
    glob = walk({n: 1 / len(N) for n in N})
    raw = {n: ppr.get(n, 0.0) * (ppr.get(n, 0.0) / glob[n]) ** 0.5 if glob.get(n) else 0.0 for n in N}

    reg = {d["deposit_number"]: d for d in json.loads((AX / "data/registry.json").read_text(encoding="utf-8"))["deposits"]}
    for n in N:
        d = reg.get(n) or {}
        if (d.get("status") or "").upper() != "SUPERSEDED":
            continue
        succ = d.get("superseded_by"); succ = succ[0] if isinstance(succ, list) and succ else succ
        succ = int(succ) if str(succ or "").isdigit() else None
        while succ is not None and succ not in raw and str((reg.get(succ) or {}).get("superseded_by") or "").isdigit():
            succ = int(reg[succ]["superseded_by"])
        if succ in raw:
            raw[succ] += 0.6 * raw[n]
        raw[n] *= 0.4   # with no successor in the oracle's index, the record keeps 40% until the index catches up

    joins = json.loads((AX / "data/capture-joins.json").read_text(encoding="utf-8"))
    observed = collections.defaultdict(set)
    for j in joins["relations"]:
        if j["verb"] == "appeared_in" and j["state"] == "confirmed" and j["object"].startswith("deposit:"):
            n = int(j["object"][8:])
            if n in N:
                observed[n].add(j["obs_id"])
    for n in observed:
        roles[n].add("observed")

    ranked = sorted(N, key=lambda n: raw[n], reverse=True)
    nz = [n for n in ranked if raw[n] > 0]
    w = {n: (round(1 - i / len(nz), 4) if raw[n] > 0 else 0.0) for i, n in enumerate(ranked)}
    hist = collections.Counter(min(9, int(v * 10)) for v in w.values())
    out = {"name": "Rex Fraction — orientation and roles over the archive (draft 0.2)",
           "rule": "Orientation, never a bound. search: score * (1 + K*w) * (ROLE_BOOST if the asked role is among the record's roles).",
           "K": K, "ROLE_BOOST": ROLE_BOOST,
           "recipe": {"seeds": "records linked from spxi.dev and semanticeconomy.org pages (3.0; +1.0 if both), Rex Fraction as creator (+1.0)",
                      "walk": "restart 0.25; forward 0.8 split by out-degree; back 0.2 per citer, divided by max(1, citer out-degree/10); 40 iterations",
                      "score": "lift = ppr * sqrt(ppr / uniform-start walk)", "versions": "superseded keeps 0.4, successor +0.6",
                      "normalise": "rank among non-zero records -> 1 - rank/count", "reception": "role 'observed' only; no weight"},
           "sources": {"alexanarch": rev(AX), "spxi-dev": rev(SPXI), "semanticeconomy.org_fetched": (se_dir / "FETCHED_AT").read_text().strip() if (se_dir / "FETCHED_AT").exists() else None,
                       "oracle_metadata_records": len(N), "oracle_metadata_max_deposit": max(N)},
           "inputs": {"spxi.dev_links": len(spxi), "semanticeconomy.org_links": len(se), "rex_fraction_deposits": len(rex),
                      "citation_edges": sum(len(v) for v in fwd.values()), "observed_deposits": len(observed)},
           "distribution": {f"{k/10:.1f}-{(k+1)/10:.1f}": hist[k] for k in range(10)},
           "role_counts": dict(collections.Counter(r for n in N for r in roles[n]).most_common()),
           "records": {str(n): {"w": w[n], "roles": sorted(roles[n])} for n in ranked}}
    (ROOT / "rag/fraction-weights.json").write_text(json.dumps(out, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("sources", "inputs", "distribution", "role_counts")}, ensure_ascii=False))
    return ranked, raw, by, spxi, se, rex, observed, roles, w


if __name__ == "__main__":
    main(sys.argv[1])
