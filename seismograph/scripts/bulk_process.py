#!/usr/bin/env python3
"""
seismograph/scripts/bulk_process.py — OpenAIRE Research Graph bulk dump processor.

Streams a TAR archive of gzipped JSONL files from the OpenAIRE Research Graph
release (Zenodo community: openaire-research-graph) without full extraction.
Computes Seismograph metrics on the streamed records.

Architecture:
  TAR archive → gzipped JSONL partition → JSON record → metric accumulator

The TAR is processed without writing extracted files to disk — each partition is
streamed through gzip → json line-by-line, so memory usage stays bounded
regardless of dump size. Designed to process tens-of-GB archives on commodity
hardware.

Usage:
    # Process a local tar file
    python3 bulk_process.py --tar /tmp/software.tar \\
        --record-type product \\
        --output seismograph/metrics/openaire-v11.1.1-software.json

    # Stream directly from a Zenodo URL (no local storage needed for the tar)
    python3 bulk_process.py \\
        --url https://zenodo.org/records/20428976/files/software.tar/content \\
        --record-type product \\
        --output seismograph/metrics/openaire-v11.1.1-software.json

Record types supported:
    product       — publications, datasets, software, other research products
    organization  — organizations
    project       — funded projects
    relation      — graph edges (citations, etc.)
    datasource    — repositories that contributed records

References:
    Schema: 10.5281/zenodo.20559578 (OpenAIRE Graph JSON Schemas)
    Concept DOI: 10.5281/zenodo.20428976 (OpenAIRE Graph Dataset, all versions)
    Per: EA-MANDALA-SEISMOGRAPH-01 v0.1
"""

import argparse
import gzip
import io
import json
import sys
import tarfile
import time
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Reuse the metrics primitives from the OAI-PMH-side script.
# Inline minimal versions here so this script is self-contained.

WORD_RE = __import__("re").compile(r"\b[a-zA-Z][a-zA-Z'-]{1,}\b")
HTML_TAG_RE = __import__("re").compile(r"<[^>]+>")

ENGLISH_STOPWORDS = frozenset(
    [
        "the", "a", "an", "and", "or", "but", "of", "in", "on", "at", "to",
        "from", "by", "with", "for", "as", "is", "are", "was", "were", "be",
        "been", "being", "have", "has", "had", "do", "does", "did", "this",
        "that", "these", "those", "it", "its", "if", "then", "than", "so",
        "not", "no", "yes", "we", "you", "they", "he", "she", "his", "her",
        "their", "our", "your", "which", "who", "whom", "whose", "what",
        "when", "where", "why", "how", "all", "any", "some", "such", "only",
        "own", "same", "other", "more", "most", "less", "least", "very",
        "just", "also", "out", "up", "down", "over", "under", "into",
        "through", "between", "among", "without", "within",
    ]
)
FIRST_PERSON_SINGULAR = frozenset(["i", "me", "my", "mine", "myself"])
SPECULATIVE_MODALS = frozenset(
    [
        "might", "could", "perhaps", "may", "possibly", "conceivably",
        "presumably", "supposedly", "ostensibly", "apparently", "seemingly",
        "purportedly", "tentatively", "potentially", "hypothetically",
        "speculatively", "arguably",
    ]
)


def tokenize(text, lowercase=True):
    if not text:
        return []
    stripped = HTML_TAG_RE.sub(" ", text)
    tokens = WORD_RE.findall(stripped)
    return [t.lower() for t in tokens] if lowercase else tokens


# ─────────────────────────────────────────────────────────────────────────────
# Streaming TAR → gzip → JSONL
# ─────────────────────────────────────────────────────────────────────────────

def iter_tar_partitions(tar_source, mode="r|"):
    """Yield (member_name, file-like) pairs from a streaming tar.

    Use mode='r|' for sequential streaming (no random seeking). This allows
    processing tars that are larger than available disk if streamed from a URL
    (with a tee to disk for caching only when --keep-tar is set).
    """
    with tarfile.open(fileobj=tar_source, mode=mode) as tf:
        for member in tf:
            if not member.isfile():
                continue
            if not member.name.endswith(".json.gz"):
                continue
            fh = tf.extractfile(member)
            if fh is None:
                continue
            yield member.name, fh


def iter_records(tar_source):
    """Yield parsed JSON records from a tar of gzipped JSONL partitions."""
    partition_count = 0
    record_count = 0
    last_log = time.time()

    for name, fh in iter_tar_partitions(tar_source):
        partition_count += 1
        try:
            with gzip.GzipFile(fileobj=fh) as gz:
                # gz is bytes; wrap in TextIOWrapper for utf-8 line iteration
                text = io.TextIOWrapper(gz, encoding="utf-8", errors="replace")
                for line in text:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                        record_count += 1
                    except json.JSONDecodeError as e:
                        sys.stderr.write(
                            f"[bulk] decode error in {name}: {e} (line skipped)\n"
                        )

                    # Progress log every 5 seconds
                    if time.time() - last_log > 5.0:
                        sys.stderr.write(
                            f"[bulk] {partition_count} partitions, "
                            f"{record_count:,} records\n"
                        )
                        last_log = time.time()
        except Exception as e:
            sys.stderr.write(f"[bulk] error reading {name}: {e}\n")
            continue

    sys.stderr.write(
        f"[bulk] FINAL: {partition_count} partitions, {record_count:,} records\n"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Record-type specific metric accumulators
# ─────────────────────────────────────────────────────────────────────────────

class ProductMetrics:
    """Accumulator for product records (publications, datasets, software, other).

    Computes the six Seismograph metrics in streaming fashion.
    """

    def __init__(self):
        # Lexical
        self.vocab_counter = Counter()
        self.token_total = 0

        # Citations
        self.intra_zenodo_refs = 0
        self.other_doi_refs = 0
        self.non_doi_refs = 0
        self.external_repos = Counter()

        # Publishers / geography
        self.publisher_counter = Counter()
        self.country_counter = Counter()
        self.collected_from_counter = Counter()  # The source repository (Zenodo, etc.)

        # Diotima Index
        self.diotima_tokens = 0
        self.diotima_first_person = 0
        self.diotima_modal = 0
        self.diotima_records_in_scope = 0

        # Spam patterns + retractions
        self.bulk_uploaded = 0
        self.withdrawn = 0
        self.records_seen = 0

        # By-type and by-OA-color breakdown
        self.by_type = Counter()
        self.oa_color = Counter()
        self.diamond_journal = 0
        self.is_green = 0

        # Temporal
        self.by_pub_year = Counter()

    def update(self, rec):
        self.records_seen += 1
        rtype = rec.get("type") or "unknown"
        self.by_type[rtype] += 1

        # Title + descriptions for lexical analysis
        title = rec.get("mainTitle") or ""
        descriptions = rec.get("descriptions") or []
        if isinstance(descriptions, list):
            descs = " ".join(d for d in descriptions if isinstance(d, str))
        else:
            descs = str(descriptions) if descriptions else ""

        text = title + ". " + descs if title else descs

        # Lexical compression
        tokens = tokenize(text)
        for tok in tokens:
            if tok not in ENGLISH_STOPWORDS:
                self.vocab_counter[tok] += 1
                self.token_total += 1

        # Diotima — English-language records only
        language = rec.get("language") or {}
        if isinstance(language, dict):
            lang_code = (language.get("code") or "").lower()
        else:
            lang_code = str(language).lower()
        if lang_code in {"", "eng", "en", "english"} and len(tokens) >= 10:
            # Heuristic English filter (handles missing language tags)
            eng_overlap = sum(1 for t in tokens if t in ENGLISH_STOPWORDS) / max(1, len(tokens))
            if eng_overlap >= 0.05:
                self.diotima_records_in_scope += 1
                self.diotima_tokens += len(tokens)
                self.diotima_first_person += sum(1 for t in tokens if t in FIRST_PERSON_SINGULAR)
                self.diotima_modal += sum(1 for t in tokens if t in SPECULATIVE_MODALS)

        # Spam pattern (carries over from OAI-PMH side)
        if "bulk uploaded" in descs.lower() or "high-speed tool" in descs.lower():
            self.bulk_uploaded += 1

        # Publisher
        pub = rec.get("publisher") or "(none)"
        self.publisher_counter[pub] += 1

        # Countries
        for c in rec.get("countries") or []:
            if isinstance(c, dict):
                code = c.get("code") or c.get("label") or "?"
            else:
                code = str(c)
            self.country_counter[code] += 1

        # Source repository — instances[*].collectedFrom
        for inst in rec.get("instances") or []:
            cf = inst.get("collectedFrom")
            if isinstance(cf, dict):
                src = cf.get("value") or cf.get("key") or "?"
                self.collected_from_counter[src] += 1
            elif cf:
                self.collected_from_counter[str(cf)] += 1

        # Publication year (for longitudinal stratification)
        pub_date = rec.get("publicationDate") or ""
        if pub_date and len(pub_date) >= 4:
            self.by_pub_year[pub_date[:4]] += 1

        # Open Access posture
        oac = rec.get("openAccessColor")
        if oac:
            self.oa_color[oac] += 1
        if rec.get("isInDiamondJournal"):
            self.diamond_journal += 1
        if rec.get("isGreen"):
            self.is_green += 1

        # Best access right — withdrawn detection
        bar = rec.get("bestAccessRight") or {}
        if isinstance(bar, dict):
            code = (bar.get("code") or bar.get("label") or "").lower()
            if "withdraw" in code or "tombstone" in code:
                self.withdrawn += 1

    def finalize(self):
        """Compute final aggregate metrics."""
        import math

        # Lexical entropy
        total = sum(self.vocab_counter.values())
        if total > 0:
            entropy = 0.0
            for c in self.vocab_counter.values():
                p = c / total
                entropy -= p * math.log2(p)
            unique = len(self.vocab_counter)
            normalized = entropy / math.log2(unique) if unique > 1 else 0
        else:
            entropy = 0.0
            normalized = 0.0
            unique = 0

        # Publisher Gini
        pub_counts = sorted(self.publisher_counter.values())
        n = len(pub_counts)
        if n > 0:
            total_pub = sum(pub_counts)
            cum_share = 0
            cumulative = 0
            for c in pub_counts:
                cumulative += c
                cum_share += cumulative
            gini = (n + 1 - 2 * (cum_share / total_pub)) / n if total_pub else 0
        else:
            gini = 0

        per_1000 = lambda x: (1000 * x / self.diotima_tokens) if self.diotima_tokens else 0
        fp_rate = per_1000(self.diotima_first_person)
        modal_rate = per_1000(self.diotima_modal)

        return {
            "summary": {
                "total_records": self.records_seen,
                "by_type": dict(self.by_type),
                "by_pub_year": dict(sorted(self.by_pub_year.items())),
            },
            "metrics": {
                "lexical_compression": {
                    "token_count": self.token_total,
                    "unique_tokens": unique,
                    "entropy_bits": entropy,
                    "normalized_entropy": normalized,
                    "top_30_terms": self.vocab_counter.most_common(30),
                },
                "publisher_distribution": {
                    "unique_publishers": n,
                    "gini": gini,
                    "top_30": self.publisher_counter.most_common(30),
                },
                "geographic_distribution": {
                    "unique_countries": len(self.country_counter),
                    "top_30_countries": self.country_counter.most_common(30),
                },
                "source_repositories": {
                    "unique_sources": len(self.collected_from_counter),
                    "top_30_sources": self.collected_from_counter.most_common(30),
                },
                "diotima_index": {
                    "records_in_scope": self.diotima_records_in_scope,
                    "total_tokens": self.diotima_tokens,
                    "first_person_count": self.diotima_first_person,
                    "modal_count": self.diotima_modal,
                    "first_person_per_1000": fp_rate,
                    "modal_per_1000": modal_rate,
                    "diotima_composite": fp_rate + modal_rate,
                },
                "open_access_distribution": {
                    "by_color": dict(self.oa_color),
                    "diamond_journal_count": self.diamond_journal,
                    "diamond_journal_pct": self.diamond_journal / self.records_seen if self.records_seen else 0,
                    "is_green_count": self.is_green,
                    "is_green_pct": self.is_green / self.records_seen if self.records_seen else 0,
                },
                "spam_patterns": {
                    "bulk_uploaded": self.bulk_uploaded,
                    "bulk_uploaded_pct": self.bulk_uploaded / self.records_seen if self.records_seen else 0,
                },
                "retraction_patterns": {
                    "withdrawn_count": self.withdrawn,
                    "withdrawn_pct": self.withdrawn / self.records_seen if self.records_seen else 0,
                },
            },
        }


class OrganizationMetrics:
    """Accumulator for organization records — much simpler schema."""

    def __init__(self):
        self.records_seen = 0
        self.country_counter = Counter()
        self.has_pids = 0
        self.has_website = 0

    def update(self, rec):
        self.records_seen += 1
        c = rec.get("country")
        if isinstance(c, dict):
            code = c.get("code") or c.get("label") or "?"
        elif c:
            code = str(c)
        else:
            code = "(none)"
        self.country_counter[code] += 1
        if rec.get("pids"):
            self.has_pids += 1
        if rec.get("websiteUrl"):
            self.has_website += 1

    def finalize(self):
        return {
            "summary": {
                "total_records": self.records_seen,
            },
            "metrics": {
                "geographic_distribution": {
                    "unique_countries": len(self.country_counter),
                    "top_30_countries": self.country_counter.most_common(30),
                },
                "metadata_completeness": {
                    "has_pids_pct": self.has_pids / self.records_seen if self.records_seen else 0,
                    "has_website_pct": self.has_website / self.records_seen if self.records_seen else 0,
                },
            },
        }


METRIC_ACCUMULATORS = {
    "product": ProductMetrics,
    "organization": OrganizationMetrics,
}


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def process(tar_path=None, tar_url=None, record_type="product"):
    accum_cls = METRIC_ACCUMULATORS.get(record_type)
    if not accum_cls:
        raise ValueError(f"Unknown record type: {record_type}. Use one of {list(METRIC_ACCUMULATORS)}")
    accum = accum_cls()

    if tar_path:
        with open(tar_path, "rb") as fh:
            for rec in iter_records(fh):
                accum.update(rec)
    elif tar_url:
        # Stream over HTTP — no full local copy
        req = urllib.request.Request(
            tar_url,
            headers={"User-Agent": "MandalaOracle/Seismograph-v0.1 (+https://themandalaoracle.org)"},
        )
        with urllib.request.urlopen(req, timeout=900) as resp:
            for rec in iter_records(resp):
                accum.update(rec)
    else:
        raise ValueError("Provide --tar or --url")

    return accum.finalize()


def main():
    p = argparse.ArgumentParser(description="OpenAIRE bulk dump processor.")
    p.add_argument("--tar", help="Local tar file path")
    p.add_argument("--url", help="Remote tar URL (streaming)")
    p.add_argument(
        "--record-type",
        choices=list(METRIC_ACCUMULATORS.keys()),
        default="product",
        help="Schema of records in the tar",
    )
    p.add_argument("--output", required=True, help="Output metrics JSON path")
    args = p.parse_args()

    if not (args.tar or args.url):
        p.error("Provide --tar or --url")

    sys.stderr.write(
        f"[bulk] Processing {args.tar or args.url} as {args.record_type}...\n"
    )
    t0 = time.time()
    result = process(tar_path=args.tar, tar_url=args.url, record_type=args.record_type)
    elapsed = time.time() - t0

    result["meta"] = {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": "EA-MANDALA-SEISMOGRAPH-01/v0.1",
        "source": args.tar or args.url,
        "record_type": args.record_type,
        "elapsed_sec": round(elapsed, 1),
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2, default=str))

    s = result.get("summary", {})
    sys.stderr.write(
        f"[bulk] Done: {s.get('total_records', 0):,} records in {elapsed:.1f}s\n"
        f"       → {args.output}\n"
    )
    print(args.output)


if __name__ == "__main__":
    main()
