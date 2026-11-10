#!/usr/bin/env python3
"""regenerate_positions.py — every AXN position that is not a formal deposit, for Sigil's search.

MANUS, 2026-11-10: "captures arent yet available to him, and captures and /nons should be. anything with an axn".
Reads alexanarch's central AXN registry (data/axn-central-registry.json) and the Capture Registry, and writes
rag/positions.json: one entry per position (capture addresses, /non entries, /non panels, releases, symbolon
witnessings), in the shape of rag/metadata.json plus `kind` and `record_url`, with no deposit_number. The
deposits stay in rag/metadata.json, which the sky, the Fraction weights and the lectionary read as deposits only.
Standard library only; regenerate_rag.py calls it at the end of its run.

    python3 scripts/regenerate_positions.py [alexanarch root]   (default: the alexanarch submodule)"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
A = "https://www.alexanarch.org"
JSON_KWARGS = dict(indent=None, separators=(",", ":"), ensure_ascii=False)


def _abs(u):
    return u if not u or u.startswith("http") else A + u


def build(alex: Path) -> list[dict]:
    central = json.loads((alex / "data/axn-central-registry.json").read_text(encoding="utf-8"))
    caps = {e["slug"]: e for e in json.loads((alex / "data/EA-WG-CAPTURES-01.json").read_text(encoding="utf-8"))["entries"]}
    out = []
    for hx, p in sorted(central["positions"].items()):
        src = p.get("source")
        e = {"axn": p.get("root") or p.get("axn"), "hex": hx, "family": p.get("family"), "kind": src, "origin": "archive",
             "deposit_number": None, "record_url": _abs(p.get("record")), "full_text_path": None, "creator": None, "keywords": []}
        if src == "capture":
            slugs = list(p.get("observations") or {}) + [(p.get("record") or "").rstrip("/").rsplit("/", 1)[-1]]
            obs = list({s: caps[s] for s in slugs if s in caps}.values())
            if not obs:
                e.update(title=f"Capture: «{p.get('q')}»", date=p.get("allocated"), description=f"A capture address in the Capture Registry: «{p.get('q')}».")
                out.append(e)
                continue
            obs.sort(key=lambda c: c.get("date") or "")
            last = obs[-1]
            head = last.get("mt") if len(last.get("mt") or "") >= 12 else (last.get("d") or "").split(":")[0][:220]
            e.update(title=head or p.get("q"), date=last.get("date"),
                     description=(f"A capture: {last.get('surface')} composing at the address «{p.get('q') or last.get('q')}» "
                                  f"({len(obs)} observation{'s' if len(obs) > 1 else ''}, {obs[0].get('date')} to {last.get('date')}; section {last.get('s')}). "
                                  + (last.get("d") or "")),
                     keywords=[last.get("surface") or "", last.get("s") or ""],
                     full_text_path=f"/data/captures/sealed/{last['slug']}.json" if (alex / "data/captures/sealed" / f"{last['slug']}.json").exists() else None)
        elif src == "non-entry":
            row = {}
            if p.get("row") and (alex / p["row"]).exists():
                row = json.loads((alex / p["row"]).read_text(encoding="utf-8"))
            d = row.get("delta") or {}
            e.update(title=f"/non: {row.get('address') or p.get('entity')} — the negative of the negative", date=p.get("minted"),
                     description=(f"The /non entry for «{row.get('address') or p.get('entity')}»: the composition on {row.get('surface') or 'the surface'} "
                                  f"read against its field and the archive's kernel. " + " ".join(str(v) for v in d.values())[:1600]),
                     keywords=["/non", "negative of the negative", row.get("surface") or ""],
                     full_text_path="/" + p["row"] if p.get("row") else None)
        elif src == "non-register":
            e.update(title=f"/non panel: «{p.get('q')}»", date=p.get("allocated"),
                     description=f"The /non register's panel observation at the address «{p.get('q')}» (entity {p.get('entity')}).", keywords=["/non", "panel"])
        elif src == "release":
            e.update(title=p.get("name") or p.get("object"), date=p.get("allocated"),
                     description=f"The archive's {p.get('kind')} release position for {p.get('object')} ({len(p.get('releases') or [])} releases).", keywords=[p.get("kind") or ""])
        elif src == "symbolon-witness":
            e.update(title=f"Symbolon witnessing: {p.get('filename')}", date=(p.get("registered") or "")[:10],
                     description=f"A witnessing in the symbolon registry ({p.get('status')}; {p.get('reconstruction_class')}).",
                     keywords=["symbolon"], full_text_path=p.get("entry"), record_url=_abs(p.get("entry")))
        else:
            continue   # deposits live in metadata.json; contested positions resolve through their claimants
        out.append(e)
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    alex = Path(argv[0]) if argv else ROOT / "alexanarch"
    if not (alex / "data/axn-central-registry.json").exists():
        print(f"ERROR: no central registry under {alex}", file=sys.stderr)
        return 1
    out = build(alex)
    path = ROOT / "rag/positions.json"
    path.write_text(json.dumps(out, **JSON_KWARGS), encoding="utf-8")
    from collections import Counter
    print(f"Wrote {path}: {len(out)} positions {dict(Counter(e['kind'] for e in out))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
