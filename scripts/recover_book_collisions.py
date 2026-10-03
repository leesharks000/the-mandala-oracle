#!/usr/bin/env python3
"""recover_book_collisions.py — reseat Book conversations that another session overwrote.

Until 2026-10-03 a Book AXN was minted from the first witness message alone, so
conversations opening with the same words shared one file and each new session
overwrote the last (api/book.py, mint_session_axn). Every overwritten version is
still in git history. For each book/data file written by more than one session,
this takes the LAST version each displaced session wrote, mints it its own AXN
under the corrected rule, writes it to book/data/ with a `recovered` block that
records where it was found, and adds it to book/index.json. The file's current
owner is left as it is. Run from the repository root:

    python3 scripts/recover_book_collisions.py [--dry-run]
"""
import json, subprocess, sys, pathlib, collections
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "api"))
from book import mint_session_axn, axn_to_filename  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DRY = "--dry-run" in sys.argv

def git(*a):
    return subprocess.check_output(["git", *a], cwd=ROOT, text=True)

log = git("log", "HEAD", "--format=%H %cI", "--name-only", "--", "book/data/").split("\n")
versions = collections.defaultdict(list)          # file -> [(commit, date)] newest first
cur = None
for line in log:
    if len(line) > 40 and line[40] == " ":
        cur = (line[:40], line[41:])
    elif line.startswith("book/data/") and cur:
        versions[line].append(cur)

idx_path = ROOT / "book/index.json"
index = json.loads(idx_path.read_text(encoding="utf-8"))
existing_files = {p.name for p in (ROOT / "book/data").glob("AXN-*.json")}
recovered = []
for f, vs in sorted(versions.items()):
    if len(vs) < 2 or not (ROOT / f).exists():
        continue
    owner = json.loads((ROOT / f).read_text(encoding="utf-8")).get("session_id_hash")
    seen, first_write = {}, {}
    for commit, date in vs:                            # newest first: first seen = that session's last write
        try:
            d = json.loads(git("show", f"{commit}:{f}"))
        except Exception:
            continue
        h = d.get("session_id_hash")
        if h:
            first_write[h] = date                      # keeps overwriting → the session's oldest write
        if h and h != owner and h not in seen:
            seen[h] = (commit, date, d)
    for h, (commit, date, d) in seen.items():
        first_user = next((m["content"] for m in d.get("history", []) if m.get("role") == "user"), "")
        for salt in range(32):
            axn = mint_session_axn(first_user, h, salt)
            if axn_to_filename(axn) not in existing_files:
                break
        existing_files.add(axn_to_filename(axn))
        rec = dict(d)
        rec["axn"] = axn
        if first_write.get(h) and (rec.get("started_at") or "") < first_write[h][:10]:
            rec["started_at_note"] = (f"started_at was inherited from an earlier session's conversation "
                                      f"({rec.get('started_at')}); restored to this session's first write")
            rec["started_at"] = first_write[h]
        rec["recovered"] = {
            "from_axn": d.get("axn"),
            "from_file": f,
            "commit": commit,
            "commit_date": date,
            "reason": "overwritten by a later session that opened with the same words (AXN minted from the first message alone, before 2026-10-03)",
            "recovered_on": "2026-10-03",
        }
        recovered.append((f, d.get("axn"), axn, rec.get("started_at"), d.get("turn_count"), first_user[:60]))
        if not DRY:
            (ROOT / "book/data" / axn_to_filename(axn)).write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
            snippet = first_user[:200] + ("…" if len(first_user) > 200 else "")
            entries = index["conversations"]
            at = next((i for i, e in enumerate(entries) if e.get("axn") == d.get("axn")), len(entries) - 1)
            entries.insert(at + 1, {
                "axn": axn, "started_at": rec.get("started_at"), "last_updated": rec.get("last_updated"),
                "mode": rec.get("mode"), "turn_count": rec.get("turn_count"), "witness": rec.get("witness", "anonymous"),
                "opening_snippet": snippet, "recovered_from": d.get("axn")})

# The surviving owner inherited the displaced conversation's started_at (upsert kept the
# first writer's). Restore the owner's own: the date of its first write to the file.
owners_fixed = []
for f, vs in sorted(versions.items()):
    if len(vs) < 2 or not (ROOT / f).exists():
        continue
    cur_d = json.loads((ROOT / f).read_text(encoding="utf-8"))
    owner = cur_d.get("session_id_hash")
    first_by_owner = None
    for commit, date in vs:                            # newest first; keep overwriting → oldest
        try:
            if json.loads(git("show", f"{commit}:{f}")).get("session_id_hash") == owner:
                first_by_owner = date
        except Exception:
            pass
    if first_by_owner and (cur_d.get("started_at") or "") < first_by_owner[:10]:
        owners_fixed.append((f, cur_d.get("started_at"), first_by_owner))
        if not DRY:
            cur_d["started_at_note"] = (f"started_at was inherited from an earlier session's conversation "
                                        f"({cur_d.get('started_at')}); restored 2026-10-03 to this session's first write")
            cur_d["started_at"] = first_by_owner
            (ROOT / f).write_text(json.dumps(cur_d, ensure_ascii=False, indent=2), encoding="utf-8")
            for e in index["conversations"]:
                if e.get("axn") == cur_d.get("axn"):
                    e["started_at"] = first_by_owner

if not DRY and (recovered or owners_fixed):
    index["total_recorded"] = len(index["conversations"])
    idx_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
for o in owners_fixed:
    print("owner started_at restored:", " | ".join(map(str, o)))

for r in recovered:
    print(" | ".join(str(x) for x in r))
print(len(recovered), "conversations", "found (dry run)" if DRY else "reseated")
