#!/usr/bin/env python3
"""run_ledger.py — regenerate runs/LEDGER.md: every compiler execution,
its method (commit-linked), and its outcome. The MANUS requirement of
2026-07-04: results tracked against method; any state restorable by
pasting its commit into the deploy box."""
import json, glob

rows = []
for f in sorted(glob.glob("runs/RUN-*.json")):
    r = json.load(open(f))
    a = r.get("artifacts", {})
    m = r.get("method", {})
    commit = m.get("commit") or r.get("code", "")
    short = commit[:12] if commit else "pre-provenance"
    link = f"[{short}](https://github.com/leesharks000/the-mandala-oracle/tree/{commit})" if commit else short
    ind = a.get("independent", {})
    rows.append((r["run_id"], link,
                 m.get("pipeline", "legacy_skeleton?"),
                 r.get("operator", "?"), r.get("cast_selection", "?"),
                 r.get("outcome", {}).get("gate", "?"),
                 str(ind.get("law_match", "?")), str(ind.get("terminal_consistency", "?")),
                 str(len(a.get("advisories", [])))))
with open("runs/LEDGER.md", "w") as out:
    out.write("# Run ledger — results against method\n\n")
    out.write("To restore any method-state: paste its commit into the Vercel deploy box.\n")
    out.write("`transform_py_sha` inside each record pins every prompt and gate at that instant.\n\n")
    out.write("| run | method (commit) | pipeline | operator | selection | outcome | law | terminal | advisories |\n")
    out.write("|---|---|---|---|---|---|---|---|---|\n")
    for row in rows:
        out.write("| " + " | ".join(row) + " |\n")
print(f"LEDGER.md: {len(rows)} runs")
