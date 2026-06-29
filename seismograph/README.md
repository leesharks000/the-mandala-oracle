# Zenodo Seismograph

**EA-MANDALA-SEISMOGRAPH-01 v0.1 — Longitudinal tracking of global science output under classifier-mediated repositories.**

> The platform that terminated the archive publishes its own complete metadata in bulk. The Seismograph reads it.

## What This Is

A scientific instrument that uses the platform's own published output to measure the contraction of global scientific surface area as classifier-mediated governance propagates. Monthly snapshots → longitudinal metrics → empirical record of the hollowing-out.

Six core metrics, two substrates:

- **Bulk dumps (primary)**: OpenAIRE Research Graph quarterly releases (17 versions back to 2019, ~350 GB latest). Processing the full set yields a 7-year empirical record across pre- and post-classifier-deployment periods.
- **OAI-PMH realtime (secondary)**: Daily polling of Zenodo's OAI endpoint to fill the 3–6 month gap between bulk dump releases.

## Quick Start

```bash
# 1. One-day realtime probe of openaire (curated science substream)
python3 seismograph/scripts/harvest.py \
    --from 2026-06-28 --until 2026-06-29 --set openaire \
    --output seismograph/snapshots/openaire/2026-06-28.xml.gz
python3 seismograph/scripts/metrics.py \
    --input seismograph/snapshots/openaire/2026-06-28.xml.gz \
    --output seismograph/metrics/2026-06-28-openaire.json

# 2. Bulk-dump processor (organization tar, 40 MB, 494K records, ~5 sec)
curl -sL -o /tmp/organization.tar \
    https://zenodo.org/records/20428976/files/organization.tar
python3 seismograph/scripts/bulk_process.py \
    --tar /tmp/organization.tar --record-type organization \
    --output seismograph/openaire-bulk/v11.1.1-organizations.json

# 3. Stream a publication tar without local storage (10 GB, ~5 min)
python3 seismograph/scripts/bulk_process.py \
    --url https://zenodo.org/records/20428976/files/publication_1.tar/content \
    --record-type product \
    --output seismograph/openaire-bulk/v11.1.1-publications-part1.json
```

## Architecture

See [`EA-MANDALA-SEISMOGRAPH-01_v0_1_DRAFT.md`](EA-MANDALA-SEISMOGRAPH-01_v0_1_DRAFT.md) for the full design document.

Five tiers:
- **Tier 0**: OpenAIRE Research Graph bulk dumps — primary substrate
- **Tier 1**: OAI-PMH realtime polling — fallback + recent-window coverage
- **Tier 2**: Firehose stratified sampling — spam/depositor demographics
- **Tier 3**: Derived metrics — the analytic record
- **Tier 4**: Records of interest — pattern-matched verbatim retention

## The Six Metrics

| § | Metric | What it Measures | Hypothesis |
|---|--------|------------------|------------|
| §5.1 | Lexical Compression (Shannon entropy) | Vocabulary diversity of titles + descriptions | Decreasing as classifier rewards safe terms |
| §5.2 | Citation Insularity | Ratio of intra-Zenodo / external references | Increasing as classifier discourages cross-platform |
| §5.3 | Heterodoxy Migration | Records pointing to external repos | Increasing as speculative work flees the platform |
| §5.4 | Geographic Concentration | Gini of publisher/country distribution | Increasing as classifier's training distribution dominates |
| §5.5 | Retraction Patterns | Withdrawal-marker frequency | Spike during classifier-deployment periods |
| §5.6 | The Diotima Index | First-person + speculative-modal density | Decreasing — the daimonic voice retreats |

## v0.1 Baseline Findings (2026-06-28)

The realtime probe established the first reading. From [`baseline/BASELINE-2026-06-28.md`](baseline/BASELINE-2026-06-28.md):

- **Spam-marker delta**: openaire **0.00%** vs firehose **64.26%** — the classifier's discriminating signal directly measured
- **Diotima Index**: openaire **1.30** vs firehose **0.82** — daimonic voice 60% stronger in curated stream
- **Lexical entropy**: 0.853 normalized (effectively identical between sets — this is the baseline; future contraction will be visible here first)
- **Publisher concentration**: Gini 0.91 (curated), 0.95 (raw); 94-95% Zenodo-default branding

The bulk-dump probe (organization tar, v11.1.1) confirms the streaming pipeline runs at ~115K records/sec. The full longitudinal sweep across 17 OpenAIRE versions is v0.2 work.

## Cadence

- **Daily**: realtime OAI-PMH polling (when v0.2 deploys the automation)
- **Monthly**: cron-triggered snapshot rollup + metrics computation
- **Quarterly**: OpenAIRE Research Graph bulk-dump release → process new version, update longitudinal trace
- **Quarterly**: Heteronymic Analysis — the Dodecad reads the quarter's trace

## Files

```
seismograph/
├── EA-MANDALA-SEISMOGRAPH-01_v0_1_DRAFT.md   # Architectural spec
├── README.md                                  # This file
├── scripts/
│   ├── harvest.py        # OAI-PMH harvester (Tier 1)
│   ├── metrics.py        # Six-metric computer (oai_dc input)
│   └── bulk_process.py   # OpenAIRE bulk-dump processor (Tier 0)
├── baseline/
│   ├── BASELINE-2026-06-28.md           # First analytical reading
│   ├── openaire-2026-06-28.xml.gz       # Curated-set raw
│   ├── firehose-2026-06-28-sample.xml.gz  # Firehose 11% sample raw
│   └── *-metrics.json                   # Computed metrics
├── openaire-bulk/                       # Tier 0 outputs (not raw tars)
│   └── openaire-v11.1.1-organizations.json  # First bulk-dump result
├── snapshots/                           # Tier 1 monthly aggregates
├── samples/                             # Tier 2 stratified firehose samples
└── metrics/                             # Tier 3 derived measurements
```

## Provenance

The Seismograph participates in the Machine-Mediated Reception Studies (MMRS) program of the Crimson Hexagonal Archive. The corpus deposit for this protocol is at **AXN:03AE** (forthcoming) on alexanarch.org. The instrument is operated as a public good; metrics are CC-BY-4.0; raw OpenAIRE dumps inherit CC-BY-4.0 from upstream.

The platform thought it was banning us. The platform is now publishing a quarterly seismic record of itself.

The clock has started.
