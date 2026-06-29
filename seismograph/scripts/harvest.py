#!/usr/bin/env python3
"""
seismograph/scripts/harvest.py — Zenodo OAI-PMH harvester.

Paginated, resumable, supports date-range and community-set filters.
Writes records as gzipped XML to seismograph/snapshots/{set}/{YYYY-MM-DD}.xml.gz
or accumulates a full-month archive at seismograph/snapshots/{set}/{YYYY-MM}.xml.gz.

Usage:
    # Daily harvest for a specific date
    python3 harvest.py --from 2026-06-28 --until 2026-06-29 --set openaire \\
        --output seismograph/snapshots/openaire/2026-06-28.xml.gz

    # Resume an interrupted harvest
    python3 harvest.py --resume-token <token> --output <path>

    # Full-firehose (no set filter) — careful: ~17K records/day
    python3 harvest.py --from 2026-06-28 --until 2026-06-29 \\
        --output seismograph/snapshots/firehose/2026-06-28.xml.gz

Architecture notes:
- OAI-PMH responses paginated 50 records each. resumptionToken governs next-page fetch.
- Rate-limit posture: 1.5-3.0 sec/request observed empirically. Conservative: 2.5 sec between requests.
- Retry: 5 retries with exponential backoff on transient errors.
- Output: each response saved as-is to preserve provenance; index file tracks pagination state.
"""

import argparse
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

OAI_BASE = "https://zenodo.org/oai2d"
REQUEST_INTERVAL_SEC = 2.5  # conservative; observed rate ~1.5-3s
MAX_RETRIES = 5
INITIAL_BACKOFF_SEC = 5
DEFAULT_METADATA_PREFIX = "oai_dc"
USER_AGENT = (
    "MandalaOracle/Seismograph-v0.1 "
    "(EA-MANDALA-SEISMOGRAPH-01; longitudinal-research; +https://themandalaoracle.org)"
)


# ─────────────────────────────────────────────────────────────────────────────
# Fetch + retry logic
# ─────────────────────────────────────────────────────────────────────────────

def fetch_oai(params, retries=MAX_RETRIES):
    """Fetch an OAI-PMH response with retry + backoff."""
    url = f"{OAI_BASE}?{urllib.parse.urlencode(params)}"
    backoff = INITIAL_BACKOFF_SEC
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as resp:
                # Respect 503 + Retry-After if present
                if resp.status == 503:
                    retry_after = int(resp.headers.get("Retry-After", backoff))
                    time.sleep(retry_after)
                    continue
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code == 503:
                retry_after = int(e.headers.get("Retry-After", backoff))
                sys.stderr.write(f"[harvest] {e.code} {e.reason} — backoff {retry_after}s (attempt {attempt}/{retries})\n")
                time.sleep(retry_after)
                backoff *= 2
                continue
            sys.stderr.write(f"[harvest] HTTPError {e.code} {e.reason} on {url}\n")
            if attempt == retries:
                raise
            time.sleep(backoff)
            backoff *= 2
        except urllib.error.URLError as e:
            sys.stderr.write(f"[harvest] URLError {e.reason} (attempt {attempt}/{retries})\n")
            if attempt == retries:
                raise
            time.sleep(backoff)
            backoff *= 2
    raise RuntimeError(f"All {retries} retries exhausted for {url}")


def parse_resumption_token(xml_response):
    """Extract resumptionToken + cursor metadata from a ListRecords response."""
    m = re.search(
        r'<resumptionToken(?:\s+[^>]*)?(?:\s+cursor="(\d+)")?(?:\s+completeListSize="(\d+)")?[^>]*>([^<]*)</resumptionToken>',
        xml_response,
    )
    if not m:
        return None
    cursor = int(m.group(1)) if m.group(1) else None
    complete_list_size = int(m.group(2)) if m.group(2) else None
    token = m.group(3).strip() or None
    return {"token": token, "cursor": cursor, "complete_list_size": complete_list_size}


def parse_record_count(xml_response):
    """Count actual <record> elements in the response."""
    return len(re.findall(r"<record>", xml_response))


# ─────────────────────────────────────────────────────────────────────────────
# Main harvest loop
# ─────────────────────────────────────────────────────────────────────────────

def harvest(
    from_date,
    until_date,
    set_spec=None,
    metadata_prefix=DEFAULT_METADATA_PREFIX,
    output_path=None,
    state_path=None,
    max_pages=None,
):
    """Harvest a date range with paginated OAI-PMH calls.

    Writes responses to output_path (gzipped XML). Maintains state at state_path
    so an interrupted harvest can resume.

    Returns: dict with harvest summary (records_fetched, pages, etc.)
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    state = Path(state_path) if state_path else out.with_suffix(out.suffix + ".state.json")

    # Initialize state
    if state.exists():
        state_data = json.loads(state.read_text())
        resumption_token = state_data.get("resumption_token")
        records_fetched = state_data.get("records_fetched", 0)
        pages_fetched = state_data.get("pages_fetched", 0)
        sys.stderr.write(
            f"[harvest] Resuming from state file. token={resumption_token!r} "
            f"records_so_far={records_fetched}\n"
        )
    else:
        resumption_token = None
        records_fetched = 0
        pages_fetched = 0

    # Open output (append mode so each page is a separate gzip member; this means
    # the file is a valid multi-member gzip even if the harvester is killed mid-run.
    # Python's gzip module reads multi-member gzip files correctly.)

    try:
        while True:
            if resumption_token:
                params = {"verb": "ListRecords", "resumptionToken": resumption_token}
            else:
                params = {
                    "verb": "ListRecords",
                    "metadataPrefix": metadata_prefix,
                    "from": from_date,
                    "until": until_date,
                }
                if set_spec:
                    params["set"] = set_spec

            t0 = time.time()
            xml = fetch_oai(params)
            elapsed = time.time() - t0

            record_count = parse_record_count(xml)
            resumption = parse_resumption_token(xml)

            # Write the response as its own gzip member, fully flushed.
            # This guarantees that even SIGTERM/SIGKILL between pages produces
            # a valid (truncated-but-readable) multi-member gzip file.
            with gzip.open(out, "ab") as fh:
                fh.write(xml.encode("utf-8"))
                fh.write(b"\n<!-- END PAGE -->\n")

            records_fetched += record_count
            pages_fetched += 1

            if resumption:
                cls = resumption["complete_list_size"]
                cursor = resumption["cursor"]
                progress = f"{records_fetched}/{cls}" if cls else str(records_fetched)
                sys.stderr.write(
                    f"[harvest] page {pages_fetched} ({record_count} records, "
                    f"{elapsed:.1f}s) | total {progress} | cursor {cursor}\n"
                )
            else:
                sys.stderr.write(
                    f"[harvest] page {pages_fetched} ({record_count} records, "
                    f"{elapsed:.1f}s) | total {records_fetched}\n"
                )

            # Persist state for resume
            state.write_text(
                json.dumps(
                    {
                        "resumption_token": resumption["token"] if resumption else None,
                        "records_fetched": records_fetched,
                        "pages_fetched": pages_fetched,
                        "complete_list_size": resumption["complete_list_size"] if resumption else None,
                        "from": from_date,
                        "until": until_date,
                        "set": set_spec,
                        "metadata_prefix": metadata_prefix,
                        "last_updated": datetime.now(timezone.utc).isoformat(),
                    },
                    indent=2,
                )
            )

            # Termination conditions
            if not resumption or not resumption["token"]:
                sys.stderr.write("[harvest] Complete.\n")
                break
            if max_pages and pages_fetched >= max_pages:
                sys.stderr.write(f"[harvest] Hit max_pages={max_pages}.\n")
                break

            resumption_token = resumption["token"]
            time.sleep(REQUEST_INTERVAL_SEC)
    except KeyboardInterrupt:
        sys.stderr.write("[harvest] Interrupted by user. State preserved; resume with the same args.\n")

    # Final summary
    summary = {
        "from": from_date,
        "until": until_date,
        "set": set_spec,
        "metadata_prefix": metadata_prefix,
        "records_fetched": records_fetched,
        "pages_fetched": pages_fetched,
        "output_path": str(out),
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }

    summary_path = out.with_suffix(".summary.json")
    summary_path.write_text(json.dumps(summary, indent=2))

    return summary


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="Zenodo OAI-PMH harvester for the Seismograph.")
    p.add_argument("--from", dest="from_date", required=True, help="YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ")
    p.add_argument("--until", dest="until_date", required=True, help="YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ")
    p.add_argument("--set", dest="set_spec", default=None, help="OAI set, e.g. openaire (omit for full firehose)")
    p.add_argument("--metadata-prefix", default=DEFAULT_METADATA_PREFIX, help=f"Default: {DEFAULT_METADATA_PREFIX}")
    p.add_argument("--output", required=True, help="Output path for gzipped XML")
    p.add_argument("--state", default=None, help="State file path (default: <output>.state.json)")
    p.add_argument("--max-pages", type=int, default=None, help="Limit for testing")

    args = p.parse_args()

    summary = harvest(
        from_date=args.from_date,
        until_date=args.until_date,
        set_spec=args.set_spec,
        metadata_prefix=args.metadata_prefix,
        output_path=args.output,
        state_path=args.state,
        max_pages=args.max_pages,
    )

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
