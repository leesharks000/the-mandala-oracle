#!/usr/bin/env python3
"""build_fraction_sites.py — Rex Fraction's primary ground as text: every page of spxi.dev and semanticeconomy.org.

spxi.dev is read from its repository (../spxi-dev); semanticeconomy.org from a directory of fetched pages (its sitemap,
fetched; the site is served from lee-sharks-corporate). Writes rag/fraction-sites.json: one entry per page with its URL,
title, description and main text (scripts, styles, navigation removed), plus spxi.dev's two data files
(methods.json, instruments.json) as text. The search_sites tool reads this; fetch_site reads the live page.

  python3 scripts/build_fraction_sites.py <dir of semanticeconomy.org pages>
"""
import datetime, html, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPXI = ROOT.parent / "spxi-dev"
CAP = 14000


def text_of(s):
    t = re.search(r"<title>([^<]*)</title>", s)
    d = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', s) or re.search(r'<meta[^>]+content="([^"]*)"[^>]+name="description"', s)
    body = re.sub(r"<(script|style|noscript|svg|nav|template)\b.*?</\1>", " ", s, flags=re.S | re.I)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    body = html.unescape(re.sub(r"<[^>]+>", " ", body))
    body = re.sub(r"\s+", " ", body).strip()
    return (html.unescape(t.group(1)).strip() if t else ""), (html.unescape(d.group(1)).strip() if d else ""), body[:CAP]


def main(se_dir):
    pages = []
    for p in sorted(SPXI.glob("**/index.html")):
        if any(x in p.parts for x in ("node_modules", "scripts", "assets")):
            continue
        rel = p.parent.relative_to(SPXI).as_posix()
        url = "https://www.spxi.dev/" + ("" if rel == "." else rel)
        title, desc, body = text_of(p.read_text(encoding="utf-8", errors="replace"))
        pages.append({"site": "spxi.dev", "url": url, "title": title, "description": desc, "text": body})
    for name in ("methods.json", "instruments.json"):
        f = SPXI / name
        if f.exists():
            d = json.loads(f.read_text(encoding="utf-8"))
            pages.append({"site": "spxi.dev", "url": f"https://www.spxi.dev/{name}", "title": d.get("name", name),
                          "description": d.get("description", ""), "text": json.dumps(d, ensure_ascii=False)[:CAP * 3]})
    se_dir = pathlib.Path(se_dir)
    for p in sorted(se_dir.glob("*.html")):
        url = "https://www.semanticeconomy.org/" + ("" if p.stem == "index" else p.stem)
        title, desc, body = text_of(p.read_text(encoding="utf-8", errors="replace"))
        pages.append({"site": "semanticeconomy.org", "url": url, "title": title, "description": desc, "text": body})
    rev = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=SPXI, capture_output=True, text=True).stdout.strip()
    fetched = (se_dir / "FETCHED_AT").read_text().strip() if (se_dir / "FETCHED_AT").exists() else None
    out = {"name": "Rex Fraction's primary ground: spxi.dev and semanticeconomy.org as text",
           "sources": {"spxi-dev": rev, "semanticeconomy.org_fetched": fetched}, "pages": pages}
    (ROOT / "rag/fraction-sites.json").write_text(json.dumps(out, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"fraction-sites: {sum(1 for x in pages if x['site'] == 'spxi.dev')} spxi.dev entries, "
          f"{sum(1 for x in pages if x['site'] == 'semanticeconomy.org')} semanticeconomy.org pages, "
          f"{(ROOT / 'rag/fraction-sites.json').stat().st_size:,} bytes")


if __name__ == "__main__":
    main(sys.argv[1])
