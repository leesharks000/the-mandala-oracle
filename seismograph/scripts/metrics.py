#!/usr/bin/env python3
"""
seismograph/scripts/metrics.py — Compute the six core metrics on a harvest snapshot.

Reads a gzipped XML file containing one or more OAI-PMH ListRecords responses
(concatenated), parses oai_dc records, and computes:

  §5.1 Lexical Compression — Shannon entropy of vocabulary (normalized)
  §5.2 Citation Insularity — intra/inter-community reference ratio
  §5.3 Heterodoxy Migration — fraction of dc:relation pointing outside Zenodo
  §5.4 Geographic Concentration — Gini of publisher distribution
  §5.5 Retraction Patterns — withdrawal-marker frequency
  §5.6 Diotima Index — first-person + speculative-modal + metaphor-density

Outputs: metrics JSON file with per-day and aggregate measures.

Usage:
    python3 metrics.py --input seismograph/snapshots/openaire/2026-06.xml.gz \\
        --output seismograph/metrics/2026-06-openaire.json
"""

import argparse
import gzip
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Parsing
# ─────────────────────────────────────────────────────────────────────────────

DC_FIELD_RE = re.compile(r"<dc:(\w+)[^>]*>(.*?)</dc:\1>", re.DOTALL)
RECORD_RE = re.compile(r"<record>(.*?)</record>", re.DOTALL)
DATESTAMP_RE = re.compile(r"<datestamp>([^<]+)</datestamp>")
SETSPEC_RE = re.compile(r"<setSpec>([^<]+)</setSpec>")


def unescape_xml(s):
    """Decode XML/HTML entities, including double-encoded forms.

    Zenodo descriptions are often embedded HTML that has been XML-escaped — so
    e.g. `&amp;nbsp;` represents the original `&nbsp;`. We have to unescape
    twice: once XML-level, once HTML-level. Uses html.unescape for the second
    pass (handles named entities like &zwnj; &laquo; &oacute; &rsquo; etc.).
    """
    import html as _htmlmod
    # First pass: XML-level (un-escape the outer XML envelope)
    s = (
        s.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&apos;", "'")
    )
    # Second pass: HTML-level (un-escape entities inside the now-revealed HTML)
    return _htmlmod.unescape(s)


def parse_record(record_xml):
    """Parse a single <record>...</record> block into a structured dict.

    Returns: {
        identifier, datestamp, setSpec,
        creators: [str], date, descriptions: [str], identifiers: [str],
        publisher, relations: [str], rights: [str], subjects: [str],
        title, type, source, language
    }
    """
    rec = {
        "identifier": None, "datestamp": None, "set_specs": [],
        "creators": [], "date": None, "descriptions": [], "identifiers": [],
        "publisher": None, "relations": [], "rights": [], "subjects": [],
        "title": None, "type": None, "source": None, "language": None,
    }

    # Header fields
    m = re.search(r"<identifier>([^<]+)</identifier>", record_xml)
    if m:
        rec["identifier"] = m.group(1).strip()

    m = DATESTAMP_RE.search(record_xml)
    if m:
        rec["datestamp"] = m.group(1).strip()

    rec["set_specs"] = SETSPEC_RE.findall(record_xml)

    # Dublin Core fields (multiple of each possible)
    for field_match in DC_FIELD_RE.finditer(record_xml):
        field_name = field_match.group(1)
        value = unescape_xml(field_match.group(2).strip())

        if field_name == "creator":
            rec["creators"].append(value)
        elif field_name == "description":
            rec["descriptions"].append(value)
        elif field_name == "identifier":
            rec["identifiers"].append(value)
        elif field_name == "relation":
            rec["relations"].append(value)
        elif field_name == "rights":
            rec["rights"].append(value)
        elif field_name == "subject":
            rec["subjects"].append(value)
        elif field_name == "date":
            rec["date"] = value
        elif field_name == "publisher":
            rec["publisher"] = value
        elif field_name == "title":
            rec["title"] = value
        elif field_name == "type":
            rec["type"] = value
        elif field_name == "source":
            rec["source"] = value
        elif field_name == "language":
            rec["language"] = value

    return rec


def iter_records(input_path):
    """Yield parsed records from a gzipped XML file."""
    with gzip.open(input_path, "rt", encoding="utf-8", errors="replace") as fh:
        content = fh.read()

    for m in RECORD_RE.finditer(content):
        yield parse_record(m.group(1))


# ─────────────────────────────────────────────────────────────────────────────
# Tokenization
# ─────────────────────────────────────────────────────────────────────────────

# Strip HTML/markdown that often appears inside Zenodo descriptions
HTML_TAG_RE = re.compile(r"<[^>]+>")
WORD_RE = re.compile(r"\b[a-zA-Z][a-zA-Z'-]{1,}\b")

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

# First-person singular markers (Diotima index)
FIRST_PERSON_SINGULAR = frozenset(["i", "me", "my", "mine", "myself"])

# Speculative modal markers
SPECULATIVE_MODALS = frozenset(
    [
        "might", "could", "perhaps", "may", "possibly", "conceivably",
        "presumably", "supposedly", "ostensibly", "apparently", "seemingly",
        "purportedly", "tentatively", "potentially", "hypothetically",
        "speculatively", "arguably",
    ]
)


def tokenize(text, lowercase=True):
    """Strip HTML, then word-tokenize."""
    if not text:
        return []
    stripped = HTML_TAG_RE.sub(" ", text)
    tokens = WORD_RE.findall(stripped)
    if lowercase:
        tokens = [t.lower() for t in tokens]
    return tokens


# ─────────────────────────────────────────────────────────────────────────────
# Metric §5.1 — Lexical Compression (Shannon entropy)
# ─────────────────────────────────────────────────────────────────────────────

def lexical_compression(text_corpus, exclude_stopwords=True):
    """Shannon entropy of the vocabulary distribution, normalized.

    text_corpus: iterable of strings.

    Returns: {
        token_count, unique_tokens, entropy_bits, normalized_entropy
    }

    normalized_entropy = entropy / log2(unique_tokens), so it lies in [0,1]
    where 1 = uniform distribution (maximum diversity) and 0 = degenerate
    (single token).
    """
    freq = Counter()
    for text in text_corpus:
        for tok in tokenize(text):
            if exclude_stopwords and tok in ENGLISH_STOPWORDS:
                continue
            freq[tok] += 1

    total = sum(freq.values())
    if total == 0:
        return {"token_count": 0, "unique_tokens": 0, "entropy_bits": 0.0, "normalized_entropy": 0.0}

    entropy = 0.0
    for count in freq.values():
        p = count / total
        entropy -= p * math.log2(p)

    unique = len(freq)
    max_entropy = math.log2(unique) if unique > 1 else 1.0
    normalized = entropy / max_entropy

    return {
        "token_count": total,
        "unique_tokens": unique,
        "entropy_bits": entropy,
        "normalized_entropy": normalized,
        "top_20_terms": freq.most_common(20),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Metric §5.2 — Citation Insularity
# ─────────────────────────────────────────────────────────────────────────────

ZENODO_DOI_RE = re.compile(r"10\.5281/zenodo\.(\d+)")
DOI_RE = re.compile(r"(?:https?://(?:dx\.)?doi\.org/)?(10\.\d{4,9}/[^\s]+)")


def citation_insularity(records):
    """Ratio of intra-Zenodo references / total references with DOIs."""
    intra_zenodo = 0
    other_doi = 0
    non_doi_rel = 0

    for r in records:
        for rel in r.get("relations", []):
            if ZENODO_DOI_RE.search(rel):
                intra_zenodo += 1
            elif DOI_RE.search(rel):
                other_doi += 1
            else:
                non_doi_rel += 1

    total = intra_zenodo + other_doi + non_doi_rel
    return {
        "intra_zenodo_refs": intra_zenodo,
        "other_doi_refs": other_doi,
        "non_doi_refs": non_doi_rel,
        "total_relations": total,
        "intra_zenodo_ratio": (intra_zenodo / total) if total else 0,
        "doi_ratio": ((intra_zenodo + other_doi) / total) if total else 0,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Metric §5.3 — Heterodoxy Migration
# ─────────────────────────────────────────────────────────────────────────────

EXTERNAL_REPO_PATTERNS = {
    "figshare": re.compile(r"figshare\.com|10\.6084/m9\.figshare"),
    "osf": re.compile(r"osf\.io|10\.17605/osf\.io"),
    "github": re.compile(r"github\.com"),
    "arxiv": re.compile(r"arxiv\.org|10\.48550/arxiv"),
    "biorxiv": re.compile(r"biorxiv\.org|10\.1101/"),
    "ssrn": re.compile(r"ssrn\.com"),
    "hal": re.compile(r"hal\.science|hal-"),
    "preprints_org": re.compile(r"preprints\.org"),
    "psyarxiv": re.compile(r"psyarxiv\.com"),
}


def heterodoxy_migration(records):
    """Count references to external repositories."""
    repo_counts = Counter()
    total_external = 0
    total_with_relations = 0

    for r in records:
        rels = r.get("relations", [])
        if rels:
            total_with_relations += 1
        for rel in rels:
            for repo_name, pattern in EXTERNAL_REPO_PATTERNS.items():
                if pattern.search(rel):
                    repo_counts[repo_name] += 1
                    total_external += 1
                    break

    return {
        "external_repo_references": dict(repo_counts.most_common()),
        "total_external_refs": total_external,
        "records_with_relations": total_with_relations,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Metric §5.4 — Geographic Concentration (publisher Gini)
# ─────────────────────────────────────────────────────────────────────────────

def publisher_distribution(records):
    """Publisher histogram + Gini coefficient as concentration measure."""
    publisher_counts = Counter()
    for r in records:
        pub = r.get("publisher") or "(none)"
        publisher_counts[pub] += 1

    counts = sorted(publisher_counts.values())
    n = len(counts)
    if n == 0:
        return {"gini": 0, "unique_publishers": 0, "top_20": []}

    total = sum(counts)
    # Gini coefficient via ordered cumulative
    cumulative = 0
    cum_share = 0
    for i, c in enumerate(counts, 1):
        cumulative += c
        cum_share += cumulative
    gini = (n + 1 - 2 * (cum_share / total)) / n if total else 0

    return {
        "gini": gini,
        "unique_publishers": n,
        "total_deposits": total,
        "zenodo_default_pct": publisher_counts.get("Zenodo", 0) / total if total else 0,
        "top_20": publisher_counts.most_common(20),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Metric §5.5 — Retraction Patterns
# ─────────────────────────────────────────────────────────────────────────────

WITHDRAWAL_PATTERNS = re.compile(
    r"info:eu-repo/semantics/withdrawn|retraction|retracted|withdrawn|tombstone",
    re.IGNORECASE,
)


def retraction_patterns(records):
    """Detect withdrawal/retraction markers in rights/descriptions/titles."""
    flagged = 0
    by_marker = Counter()

    for r in records:
        marked = False
        # Rights tags
        for right in r.get("rights", []):
            if WITHDRAWAL_PATTERNS.search(right):
                by_marker["rights_tag"] += 1
                marked = True
                break
        # Title
        if not marked and r.get("title") and WITHDRAWAL_PATTERNS.search(r["title"]):
            by_marker["title_marker"] += 1
            marked = True
        # Descriptions
        if not marked:
            for d in r.get("descriptions", []):
                if WITHDRAWAL_PATTERNS.search(d):
                    by_marker["description_marker"] += 1
                    marked = True
                    break

        if marked:
            flagged += 1

    total = sum(1 for _ in records) if not isinstance(records, list) else len(records)
    # If records iterator was consumed above, fall through:
    return {
        "withdrawal_markers": dict(by_marker),
        "flagged_records": flagged,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Metric §5.6 — The Diotima Index
# ─────────────────────────────────────────────────────────────────────────────

def diotima_index(records):
    """Composite first-person + speculative + lexical-density measure.

    Calculated on English-language records' descriptions only.
    """
    total_tokens = 0
    first_person_count = 0
    modal_count = 0
    total_records_in_scope = 0

    for r in records:
        # Heuristic: skip if language explicitly non-English
        lang = (r.get("language") or "").lower()
        if lang and lang not in {"en", "eng", "english", "en-us", "en-gb"}:
            continue

        # Concatenate descriptions
        text = " ".join(r.get("descriptions", []) or [])
        if r.get("title"):
            text = r["title"] + ". " + text
        if not text.strip():
            continue

        tokens = tokenize(text)
        if len(tokens) < 10:  # too short to read
            continue

        # Heuristic English filter: at least 30% of tokens overlap basic English vocabulary
        eng_overlap = sum(1 for t in tokens if t in ENGLISH_STOPWORDS) / max(1, len(tokens))
        if eng_overlap < 0.05:
            # Likely non-English content even if not flagged
            continue

        total_records_in_scope += 1
        total_tokens += len(tokens)
        first_person_count += sum(1 for t in tokens if t in FIRST_PERSON_SINGULAR)
        modal_count += sum(1 for t in tokens if t in SPECULATIVE_MODALS)

    per_1000 = lambda n: (1000 * n / total_tokens) if total_tokens else 0

    fp_rate = per_1000(first_person_count)
    modal_rate = per_1000(modal_count)
    # Composite: simple sum of the two normalized rates (room for refinement in v0.2)
    composite = fp_rate + modal_rate

    return {
        "records_in_scope": total_records_in_scope,
        "total_tokens": total_tokens,
        "first_person_count": first_person_count,
        "speculative_modal_count": modal_count,
        "first_person_per_1000": fp_rate,
        "modal_per_1000": modal_rate,
        "diotima_composite": composite,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Spam-pattern detection (auxiliary)
# ─────────────────────────────────────────────────────────────────────────────

SPAM_DESC_PATTERNS = re.compile(
    r"bulk\s*uploaded\s*via\s*high[-\s]*speed\s*tool|bulk\s*upload|high[-\s]*speed\s*tool",
    re.IGNORECASE,
)


def spam_pattern_counts(records):
    """Count records with hallmark bulk-spam markers."""
    bulk_uploaded = 0
    zenodo_publisher = 0
    total = 0

    for r in records:
        total += 1
        descs = " ".join(r.get("descriptions", []) or [])
        if SPAM_DESC_PATTERNS.search(descs):
            bulk_uploaded += 1
        if r.get("publisher") == "Zenodo":
            zenodo_publisher += 1

    return {
        "total_records": total,
        "bulk_uploaded_markers": bulk_uploaded,
        "bulk_uploaded_pct": (bulk_uploaded / total) if total else 0,
        "zenodo_default_publisher": zenodo_publisher,
        "zenodo_default_pct": (zenodo_publisher / total) if total else 0,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Aggregator
# ─────────────────────────────────────────────────────────────────────────────

def compute_all_metrics(input_path):
    """Run all six metrics on a snapshot file.

    Note: we iterate the file once and materialize records into a list since
    several metrics need multi-pass iteration. For very large snapshots a
    streaming variant should be written.
    """
    records = list(iter_records(input_path))

    if not records:
        return {"error": "No records parsed", "input": str(input_path)}

    # All text for lexical compression: titles + descriptions
    text_corpus = []
    for r in records:
        if r.get("title"):
            text_corpus.append(r["title"])
        text_corpus.extend(r.get("descriptions", []) or [])

    # By date for daily breakdown
    by_date = defaultdict(list)
    for r in records:
        ds = (r.get("datestamp") or "")[:10]  # YYYY-MM-DD
        by_date[ds].append(r)

    out = {
        "input": str(input_path),
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": "EA-MANDALA-SEISMOGRAPH-01/v0.1",
        "summary": {
            "total_records": len(records),
            "unique_dates": len(by_date),
            "date_range": [min(by_date), max(by_date)] if by_date else [None, None],
        },
        "metrics": {
            "lexical_compression": lexical_compression(text_corpus),
            "citation_insularity": citation_insularity(records),
            "heterodoxy_migration": heterodoxy_migration(records),
            "publisher_distribution": publisher_distribution(records),
            "retraction_patterns": retraction_patterns(records),
            "diotima_index": diotima_index(records),
            "spam_patterns": spam_pattern_counts(records),
        },
        "daily": {},
    }

    # Daily breakdown for some metrics (lexical entropy + Diotima + spam)
    for ds, day_records in sorted(by_date.items()):
        day_corpus = []
        for r in day_records:
            if r.get("title"):
                day_corpus.append(r["title"])
            day_corpus.extend(r.get("descriptions", []) or [])

        out["daily"][ds] = {
            "record_count": len(day_records),
            "lexical_compression": lexical_compression(day_corpus),
            "diotima_index": diotima_index(day_records),
            "spam_patterns": spam_pattern_counts(day_records),
        }

    return out


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="Compute Seismograph metrics on a snapshot.")
    p.add_argument("--input", required=True, help="Gzipped XML harvest file")
    p.add_argument("--output", required=True, help="Output metrics JSON file")
    args = p.parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    results = compute_all_metrics(args.input)
    Path(args.output).write_text(json.dumps(results, indent=2, default=str))

    # Print a short summary to stderr
    s = results.get("summary", {})
    m = results.get("metrics", {})
    sys.stderr.write(
        f"[metrics] {args.input}: {s.get('total_records', 0)} records, "
        f"{s.get('unique_dates', 0)} dates\n"
        f"  Lexical entropy (normalized): {m.get('lexical_compression', {}).get('normalized_entropy', 0):.4f}\n"
        f"  Citation insularity (intra-Zenodo): {m.get('citation_insularity', {}).get('intra_zenodo_ratio', 0):.4f}\n"
        f"  Diotima index (composite): {m.get('diotima_index', {}).get('diotima_composite', 0):.4f}\n"
        f"  Spam markers: {m.get('spam_patterns', {}).get('bulk_uploaded_pct', 0):.4%}\n"
    )
    print(args.output)


if __name__ == "__main__":
    main()
