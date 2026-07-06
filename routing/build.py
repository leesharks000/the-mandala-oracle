#!/usr/bin/env python3
"""
Build the flat routing surface for the Mandala Oracle.

Produces four JSONL indexes + a manifest.json under routing/, unifying:
- conversations (book/data/AXN-XXXX.json)
- readings (book/readings/AXN-FEXX.json)
- casts / transforms (nested inside book/expansions/{source_text_id}.json)
- source texts / expansions (book/expansions/*.json)

Cross-references:
- Each conversation lists source_text_ids it touched and reading_axns it consumed
- Each reading lists the casts it produced (transform_ids)
- Each cast has its reading_axn and source_text_id
- Each source text has counts of transforms and readings against it

Run from the repo root:
    python3 routing/build.py

Idempotent: overwrites the four JSONL outputs and the manifest.
"""
import json, os, re, sys, hashlib, datetime, glob, collections
from pathlib import Path

ROOT = Path(__file__).parent.parent
BOOK = ROOT / "book"
OUT = ROOT / "routing"
OUT.mkdir(exist_ok=True)


def extract_refs_from_conversation(conv):
    """Extract source_text_ids, reading_axns, and transform_ids referenced in a conversation."""
    text = json.dumps(conv)
    source_text_ids = set()
    for m in re.finditer(r'"source_text_id"\s*:\s*"([^"]+)"', text):
        source_text_ids.add(m.group(1))
    # Also look in message content for source_text_ids in parentheses like "(dancings-epistle-...)"
    for m in re.finditer(r'\(([a-z0-9-]+-[a-z0-9-]+)\)', text):
        cand = m.group(1)
        if len(cand.split('-')) >= 2:
            source_text_ids.add(cand)
    # AXN reading references
    reading_axns = set(re.findall(r'AXN:FE[0-9A-F]{2,4}\.READING\.[^\s",\\]+', text))
    # Transform IDs
    transform_ids = set(re.findall(r'TX-[0-9a-f]{8}', text))
    return {
        'source_text_ids': sorted(source_text_ids),
        'reading_axns': sorted(reading_axns),
        'transform_ids': sorted(transform_ids),
    }


def build_conversations():
    """One row per conversation from book/data/AXN-XXXX.json."""
    rows = []
    for path in sorted((BOOK / "data").glob("AXN-*.json")):
        try:
            conv = json.loads(path.read_text())
        except Exception as e:
            print(f"  skip {path.name}: {e}", file=sys.stderr)
            continue
        refs = extract_refs_from_conversation(conv)
        # First user turn snippet
        history = conv.get('history', [])
        first_user = next((h for h in history if h.get('role') == 'user'), None)
        opening = str(first_user.get('content', ''))[:400] if first_user else ''
        row = {
            'axn': conv.get('axn'),
            'file': f'book/data/{path.name}',
            'session_id_hash': conv.get('session_id_hash'),
            'started_at': conv.get('started_at'),
            'last_updated': conv.get('last_updated'),
            'mode': conv.get('mode'),
            'turn_count': conv.get('turn_count'),
            'witness': conv.get('witness'),
            'opening_snippet': opening,
            **refs,
        }
        rows.append(row)
    return rows


def build_readings():
    """One row per reading from book/readings/AXN-FEXX.json."""
    rows = []
    for path in sorted((BOOK / "readings").glob("AXN-*.json")):
        try:
            reading = json.loads(path.read_text())
        except Exception as e:
            print(f"  skip {path.name}: {e}", file=sys.stderr)
            continue
        row = {
            'axn': reading.get('axn'),
            'file': f'book/readings/{path.name}',
            'inscription_mode': reading.get('inscription_mode'),
            'session_id_hash': reading.get('session_id_hash'),
            'source_text_id': reading.get('source_text_id'),
            'question_gloss': reading.get('question_gloss'),
            'question_digest': reading.get('question_digest'),
            'cast_selection': (reading.get('cast_selection') or {}),
            'rotation': (reading.get('rotation') or {}),
            'inscribed_at': reading.get('inscribed_at'),
            'last_updated': reading.get('last_updated'),
            'closed_at': reading.get('closed_at'),
            'status': reading.get('status'),
            'seal': reading.get('seal'),
        }
        rows.append(row)
    return rows


def build_casts_and_sources():
    """One row per cast (flattened out of expansions[*].transforms[]) and one row per source text."""
    cast_rows = []
    source_rows = []
    for path in sorted((BOOK / "expansions").glob("*.json")):
        try:
            exp = json.loads(path.read_text())
        except Exception as e:
            print(f"  skip {path.name}: {e}", file=sys.stderr)
            continue
        source_text_id = exp.get('source_text_id') or path.stem
        transforms = exp.get('transforms', []) or []
        # source row
        source_rows.append({
            'source_text_id': source_text_id,
            'file': f'book/expansions/{path.name}',
            'source_title': exp.get('source_title'),
            'unit_basis': exp.get('unit_basis') or {},
            'transform_count': len(transforms),
            'reading_axns': sorted({t.get('reading_axn') for t in transforms if t.get('reading_axn')}),
            'operators_used': sorted({t.get('operator') for t in transforms if t.get('operator')}),
            'last_updated': exp.get('last_updated'),
        })
        # cast rows
        for tx in transforms:
            row = {
                'transform_id': tx.get('transform_id'),
                'source_text_id': source_text_id,
                'reading_axn': tx.get('reading_axn'),
                'cast_at': tx.get('cast_at'),
                'inscription_mode': tx.get('inscription_mode'),
                'operator': tx.get('operator'),
                'operator_axis': tx.get('operator_axis'),
                'anchor': tx.get('anchor') or {},
                'question_digest': tx.get('question_digest'),
                'verification': {k: v for k, v in (tx.get('verification') or {}).items() if k != 'mode'},
                'verification_mode': (tx.get('verification') or {}).get('mode'),
                'independent_verification_summary': _summarize_iv(tx.get('independent_verification')),
                'compiler_model': tx.get('compiler_model'),
                'protocol': tx.get('protocol'),
                'further_transform_eligible': tx.get('further_transform_eligible'),
                'has_kernel': 'kernel' in tx,
                'has_layer_a': 'layer_a' in tx,
                'has_commentary': bool(tx.get('commentary')),
                'source_passage_hash': _hash_snippet(tx.get('source_passage')),
                'enantiomorph_hash': _hash_snippet(tx.get('enantiomorph')),
            }
            cast_rows.append(row)
    return cast_rows, source_rows


def _hash_snippet(s):
    if not s: return None
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


def _summarize_iv(iv):
    if not iv: return None
    return {
        'mode': iv.get('mode'),
        'blacklist': iv.get('blacklist'),
        'law_match': iv.get('law_match'),
        'terminal_consistency': iv.get('terminal_consistency'),
        'terminal_similarity': iv.get('terminal_similarity'),
    }


def cross_link(convs, readings, casts, sources):
    """Add cross-reference fields tying things together after the primary passes."""
    # Index casts by reading_axn
    casts_by_reading = collections.defaultdict(list)
    for c in casts:
        if c.get('reading_axn'):
            casts_by_reading[c['reading_axn']].append(c['transform_id'])
    # Index readings by source_text_id
    readings_by_source = collections.defaultdict(list)
    for r in readings:
        if r.get('source_text_id'):
            readings_by_source[r['source_text_id']].append(r['axn'])
    # Attach to readings
    for r in readings:
        r['cast_transform_ids'] = sorted(casts_by_reading.get(r['axn'], []))
    # Attach to sources
    for s in sources:
        s['reading_count'] = len(readings_by_source.get(s['source_text_id'], []))
        s['reading_axns_all'] = sorted(readings_by_source.get(s['source_text_id'], []))
    return convs, readings, casts, sources


def write_jsonl(path, rows):
    with open(path, 'w') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=False) + '\n')


def main():
    print(f"Building routing surface at {OUT}")
    print("  gathering conversations...")
    convs = build_conversations()
    print(f"    → {len(convs)} conversations")
    print("  gathering readings...")
    readings = build_readings()
    print(f"    → {len(readings)} readings")
    print("  gathering casts & sources...")
    casts, sources = build_casts_and_sources()
    print(f"    → {len(casts)} casts across {len(sources)} sources")
    print("  cross-linking...")
    convs, readings, casts, sources = cross_link(convs, readings, casts, sources)
    # Write outputs
    write_jsonl(OUT / "conversations.jsonl", convs)
    write_jsonl(OUT / "readings.jsonl", readings)
    write_jsonl(OUT / "casts.jsonl", casts)
    write_jsonl(OUT / "sources.jsonl", sources)
    # Manifest
    manifest = {
        'schema_version': 'v1.0',
        'built_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'description': 'Flat, static, machine-facing routing surface for Mandala Oracle interactions. Cross-linked JSONL indexes over conversations, readings, casts (transforms), and source texts.',
        'counts': {
            'conversations': len(convs),
            'readings': len(readings),
            'casts': len(casts),
            'sources': len(sources),
        },
        'indexes': {
            'conversations': 'routing/conversations.jsonl',
            'readings': 'routing/readings.jsonl',
            'casts': 'routing/casts.jsonl',
            'sources': 'routing/sources.jsonl',
        },
        'source_data': {
            'conversations_dir': 'book/data/',
            'readings_dir': 'book/readings/',
            'expansions_dir': 'book/expansions/',
        },
        'cross_references': {
            'conversations -> source_text_ids, reading_axns, transform_ids': 'extracted from conversation history',
            'readings -> source_text_id, cast_transform_ids': 'cast_transform_ids derived by scanning casts for matching reading_axn',
            'casts -> reading_axn, source_text_id, transform_id': 'native fields in the transform record',
            'sources -> reading_axns_all, transform_count, reading_count': 'aggregated from readings and expansions',
        },
    }
    with open(OUT / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"  wrote manifest.json with counts {manifest['counts']}")
    print("done.")


if __name__ == '__main__':
    main()
