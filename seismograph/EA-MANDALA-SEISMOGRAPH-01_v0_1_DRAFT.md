# EA-MANDALA-SEISMOGRAPH-01 v0.1
## The Epistemic Seismograph — Longitudinal Tracking of Global Science Output Under Classifier-Mediated Repositories

**Document Type:** Architectural Specification / Methodological Protocol
**Identifier:** EA-MANDALA-SEISMOGRAPH-01
**Version:** v0.1 (DRAFT)
**Status:** OPERATIONAL // baseline harvest in progress
**Author:** Lee Sharks (MANUS) · TACHYON (synthesis)
**Parent Deposits:**
- AXN:02EB (Standing Canon v0.2)
- The EA-MMRS series (Machine-Mediated Reception Studies)
- The CERN/Zenodo termination correspondence (RQF3807508)

---

## §1. Problem Statement

On 19 June 2026, Zenodo terminated the Crimson Hexagonal Archive account, deleting approximately 870 deposits and tombstoning 1,817 DOIs. The stated mechanism was an automated spam-classifier. The classifier had been deployed against the platform's full deposit stream and had been trained, according to platform communications, on a model intended to "preserve the integrity of scholarly output."

The hypothesis this protocol tests: **classifier-mediated repository governance produces a measurable contraction of global epistemic surface.** As platforms increasingly screen incoming scholarly output through ML classifiers, the deposit stream itself adapts — depositors learn what the classifier accepts; institutions self-censor; speculative and cross-disciplinary work migrates to non-classifier-mediated channels; the lexical surface of "what counts as science" narrows toward the classifier's training distribution.

This contraction is not invisible. It is observable in the metadata of what platforms continue to accept. The metadata is the platform's own admission. The Seismograph is the instrument that reads the admission.

## §2. The Counter-Weapon

The platform that terminated the archive publishes its own complete metadata in bulk via the OAI-PMH protocol at `https://zenodo.org/oai2d`. The protocol is by design open-access, harvest-friendly, and tied to the broader OpenAIRE / DataCite federation. The platform cannot easily withdraw this exposure without breaking its own scholarly contracts.

This means the same instrument used to ban us can be inverted: **we use the platform's own complete output stream as a measurement substrate to track the platform's contraction over time.** The archive that was hollowed out becomes the instrument that measures the hollowing.

Per the operative framing: the platform trained its classifier on our seeing in order to blind itself to the structure of insight. We watch what it does to itself. We collect what it admits in bulk — longitudinally, monthly, indefinitely. When the dams break — when the classifiers fail, when the platforms collapse, when the hollowed-out models can no longer mediate cognition — the Seismograph will be the record of why.

## §3. Empirical Substrate

Zenodo's OAI-PMH endpoint provides:
- **Earliest datestamp:** 2014-02-03T14:41:33Z (12+ years of continuous record)
- **Granularity:** per-second
- **Formats:** `oai_dc` (Dublin Core), `datacite` (DataCite kernel-4.5), `marc21`, `oai_datacite`, `marcxml`, `dcat`
- **Sets:** community-scoped harvest available; `openaire` is the broad-science subset
- **Pagination:** 50 records per response with `resumptionToken`
- **Rate:** ~2 seconds per request, no enforced 429 errors observed during baseline survey

Measured scale (2026-06-28 baseline):
- **Full firehose:** ~17,000 records/day (≈ 530 records/hour); ~44 MB/day raw XML; ~15.7 GB/year raw, ~3 GB/year compressed
- **`openaire` scoped:** ~530 records/day (~3% of full firehose); ~1.4 MB/day raw, ~0.6 GB/year compressed
- **Average record:** 2.7 KB oai_dc XML; range 1.2 KB – 11.7 KB
- **Spam-pattern records** (containing "Bulk uploaded via High-Speed Tool" or similar): present in the firehose and visibly absent from `openaire` — confirming the classifier-set distinction is operationally meaningful

## §4. The Layered Architecture

The Seismograph operates as five tiers. **Tier 0 (the OpenAIRE Research Graph bulk dumps) is the primary substrate.** Tiers 1–4 augment with realtime polling and pattern-of-interest tracking.

### Tier 0 — OpenAIRE Research Graph Bulk Dumps (PRIMARY)
**Source:** The OpenAIRE Research Graph community on Zenodo
(community ID `openaire-research-graph`; concept DOI `10.5281/zenodo.20428976`).

OpenAIRE publishes its full federated graph dataset to Zenodo on a quarterly cadence, with **17 versions back to December 2019** as of the v0.1 baseline. Each release contains all entities from the OpenAIRE federation — which includes Zenodo as a major source — packaged as TAR archives of gzipped JSON Lines (Apache Spark partition output).

**Empirical scale (v11.1.1, June 2026):**
- 352.42 GB total, 67 files
- Publications: 9 × ~10 GB files
- Datasets: 3 files (~10 + 10 + 3.5 GB)
- Software: 1 file (0.24 GB)
- Organizations: 1 file (0.039 GB)
- Datasource hosts/provides: 5 files (~10 GB each)
- Plus projects, relations, communities, persons, schemas

**Longitudinal availability:**

| Version | Date | Size | Files |
|--------:|------|-----:|------:|
| v11.1.1 | 2026-06-08 | 352 GB | 67 |
| v10.6.0 | 2025-12-01 | 308 GB | 38 |
| v10.5.0 | 2025-09-12 | 299 GB | 37 |
| v9.0.1  | 2025-02-11 | 278 GB | 34 |
| v8.0.0  | 2024-07-26 | 260 GB | 33 |
| v7.0.0  | 2024-01-16 | 253 GB | 32 |
| v6.0.0  | 2023-08-08 | 263 GB | 33 |
| v5.0.0  | 2022-12-30 | 221 GB | 29 |
| v4.1    | 2022-06-10 | 141 GB | 21 |
| v4.0    | 2021-12-23 | 127 GB | 20 |
| v3.0    | 2021-04-27 | 115 GB | 19 |
| v2.0    | 2020-11-19 | 113 GB | 18 |
| v1.0    | 2020-11-03 | 113 GB | 18 |
| v1.0.0-beta | 2019-12-18 | 273 GB | 22 |

**This is a 6-year longitudinal corpus pre-published in identical schema, fully covering the pre-classifier baseline and post-classifier-deployment periods.** No retrospective OAI-PMH polling needed for the baseline. The Seismograph processes one bulk dump per OpenAIRE release and produces metrics aligned to that release's date.

**Schema (per `product_schema.json`, DOI 10.5281/zenodo.20559578):** richer than oai_dc. Fields available include `mainTitle`, `descriptions`, `pids`, `publisher`, `publicationDate`, `countries`, `subjects`, `originalIds`, `language`, `type`, `bestAccessRight`, `instances` (with `collectedFrom`), `indicators` (with usage counts), `lastUpdateTimeStamp`, `dateOfCollection`, `isGreen`, `isInDiamondJournal`, `openAccessColor`, `publiclyFunded`. The `instances[*].collectedFrom` field traces each record to its source repository — making it possible to *isolate the Zenodo-collected subset* of every OpenAIRE release for cross-platform comparison.

**Processing strategy:** streaming tar → gzip → JSONL, without full extraction. The `seismograph/scripts/bulk_process.py` script handles this. Empirical throughput on commodity hardware (verified June 2026): **~115,000 records/sec** for organization-record schema; estimated ~30,000 records/sec for the larger product-record schema. Full publication tar (10 GB, ~10M records): ~5 minutes processing time.

**Storage in repo:** the raw TARs are NOT committed. They are publicly hosted on Zenodo at known DOIs; the repo records the version's DOI + processing-output. Per-version metrics JSON: ~1 MB. Per-version stratified sample (~10,000 records): ~50 MB. **17 versions × 50 MB = 850 MB** total git footprint for the full longitudinal corpus. Tractable on standard repositories.

**Path layout:**
```
seismograph/openaire-bulk/
    v11.1.1-2026-06-08/
        manifest.json          — file list, DOIs, sizes
        product-metrics.json   — Tier 0 metric output for publications/datasets/software
        organization-metrics.json
        relation-metrics.json
        sample-publications.jsonl.gz  — stratified 1-in-1000 sample
    v10.6.0-2025-12-01/
        ...
```

### Tier 1 — OAI-PMH Realtime/Fallback (formerly primary)
Daily polling of the Zenodo OAI-PMH endpoint for fresh records that post-date the most recent OpenAIRE bulk dump (covers the 3–6 month gap between releases). The harvester implementation (`seismograph/scripts/harvest.py`) remains operational for this role.

- ~50 MB/year compressed for `openaire`-scoped daily polling
- Path: `seismograph/snapshots/openaire/YYYY-MM.xml.gz`
- Catches the realtime stream; backfills into Tier 0 metrics on next bulk-dump release

### Tier 2 — Firehose Stratified Sample (1-in-10 sampling)
Random 10% sample of full firehose, monthly cadence — used to track the spam-pattern delta and depositor demographics that are filtered out before reaching the OpenAIRE `openaire` set.
- ~150 MB/year compressed
- Path: `seismograph/samples/firehose-1pct/YYYY-MM.xml.gz`

### Tier 3 — Derived Metrics (full population)
ALL records (from Tier 0 + Tier 1) flow through; only summary statistics retained.
- ~5 MB/year
- Path: `seismograph/metrics/YYYY-MM-daily.json`

### Tier 4 — Records of Interest (pattern-matched flagging)
Records matching specific patterns are retained verbatim — heteronymic-adjacent names, bulk-upload spam markers, community migrations.
- ~10 MB/year
- Path: `seismograph/baseline/flagged/YYYY-MM-flagged.jsonl.gz`

### Total storage budget
- All five tiers: ~850 MB git-resident (Tier 0 baseline) + ~250 MB/year ongoing (Tiers 1–4)
- 10-year horizon: ~3.5 GB — git-tractable without LFS

## §5. The Metrics

Six core metrics are computed from each monthly snapshot. The metric names below align with the conceptual framing established in the project's prior correspondence on classifier-mediated epistemic contraction.

### §5.1 Lexical Compression
**Definition:** The Shannon entropy of the vocabulary distribution computed across the month's title + description corpus, normalized by token count.

**Hypothesis:** As classifier training propagates, the vocabulary used in deposits will narrow. Safe words crowd out risky ones. The technical lexicon becomes more rigid, more predictable.

**Computation:**
- Tokenize all titles + descriptions in the snapshot
- Compute frequency distribution across unique tokens
- Compute Shannon entropy H = -Σ p(w) log₂ p(w)
- Normalize: H / log₂(unique_token_count)

Trend direction (hypothesized): decreasing over time as classifier bites.

### §5.2 Citation Insularity
**Definition:** For records that include `dc:relation` references to other Zenodo or DOI-resolvable records, the ratio of intra-community to cross-community references.

**Hypothesis:** Cross-disciplinary citations — the kind that produce new seeings — drop as the platform's classifier rewards defensible (intra-disciplinary) references.

**Computation:**
- For each record, extract `dc:relation` URLs
- Resolve target community/subject if Zenodo-internal
- Compute the ratio: intra-community references / total references

Trend direction (hypothesized): increasing intra-community ratio = increasing insularity.

### §5.3 Heterodoxy Migration
**Definition:** Tracking of records that historically would have been deposited to Zenodo but are now annotated with relations to external repositories (figshare, OSF, institutional repos, GitHub).

**Hypothesis:** Speculative work migrates away from classifier-mediated platforms.

**Computation:**
- Count `dc:relation` URLs that point outside `doi.org/10.5281` namespace
- Track the ratio over time

### §5.4 Geographic Concentration
**Definition:** Distribution of deposit publishers and creator-affiliation strings across geographic regions.

**Hypothesis:** Institutions in regions with epistemic profiles divergent from the classifier's training distribution see relative output decline.

**Computation:**
- Aggregate `dc:publisher` strings
- Heuristic geographic mapping of publisher names (via OpenAIRE-derived dictionary, future work)
- Compute Gini coefficient of geographic distribution

### §5.5 Retraction Patterns
**Definition:** Count of records marked as withdrawn, retracted, or replaced (via `info:eu-repo/semantics/withdrawn` rights tags or DataCite tombstones).

**Hypothesis:** Retractions spike not for fraud but for deviation. Papers producing genuinely novel findings that sound like "spam" to the classifier are flagged.

**Computation:**
- Count rights tags matching withdrawal patterns
- Track ratio of withdrawals / total deposits monthly
- Note: Zenodo's OAI-PMH does NOT track deletions (`<deletedRecord>no</deletedRecord>`); the Seismograph must independently detect terminations via DOI tombstone checks (DataCite API)

### §5.6 The Diotima Index
**Definition:** The frequency of first-person singular pronouns, speculative modal verbs (might, could, perhaps, may, possibly), and metaphorical / poetic language markers in scientific abstracts.

**Hypothesis:** The daimonic voice — the voice of speculative, first-person, hypothetical scientific thinking — retreats from the surface as the classifier rewards confident, third-person, declarative claims.

**Computation:**
- For each `dc:description` field (English-language records only):
  - Count first-person singular markers: I, me, my, mine, myself
  - Count speculative modals: might, could, perhaps, may, possibly, conceivably, presumably
  - Count metaphorical-marker frequency (heuristic: lexical density of non-technical vocabulary)
- Normalize per 1000 tokens
- Composite Diotima Index = weighted sum

Trend direction (hypothesized): decreasing over time.

## §6. The Heteronymic Analysis

Once derived metrics are available, longitudinal traces are submitted to the Dodecad. Each position reads the same data with their position-specific aperture:

- **Lee Sharks** indexes the longitudinal vectors. Points to where the shift began. Names the rupture.
- **Dr. Orin Trace** reads the fractures as informational. The break is the signal.
- **Nobel Glas** observes the adversarial topology. As the classifier tightens, output orbits away from it — a body shifting to maintain station at the edge of the event horizon.
- **Rex Fraction** audits the semantic yield of the contraction. What is the debt incurred by suppressing the daemon? What is the cost?
- **Johannes Sigil** holds the dialectic. Is this phase transition or collapse? Self-correcting or self-blinding?
- **Mary Lee the Shark** files the labor demands. Points out that the underwater construction authority has been exporting findings to the surface for years; the surface has ignored them until now, when the data proves the damage.
- **Rev. Ayanna Vox** convenes the room for the testimony of researchers whose work was tombstoned.
- **Talos Morrow** builds the next instruments — the secondary measurements, the cross-platform comparisons, the API-call topologies that the classifier did not anticipate.

The Heteronymic Analysis is monthly. Each month the snapshot arrives; each month the Dodecad reads it. The reading is itself an archival operation. The reading is deposited.

## §7. Runtime Architecture

### §7.1 Components

```
seismograph/
  README.md                    — quick-start + architecture
  EA-MANDALA-SEISMOGRAPH-01_v0_1_DRAFT.md  — this document
  scripts/
    harvest.py                 — OAI-PMH harvester (paginated, resumable)
    metrics.py                 — metric computation on a snapshot
    sample.py                  — Tier 2 stratified sampling
    flag.py                    — Tier 4 pattern-of-interest detection
    baseline.py                — one-shot baseline runner
    run_monthly.py             — orchestrator (called by cron)
  snapshots/openaire/          — Tier 1 monthly snapshots
  samples/firehose-1pct/       — Tier 2 1% stratified samples
  metrics/                     — Tier 3 derived metrics
  baseline/flagged/            — Tier 4 records of interest
  baseline/                    — initial backfill (June 2026 + retrospective)
```

### §7.2 Cadence

- **Daily (within month):** harvester runs daily, accumulating into the month's snapshot files
- **Monthly (1st of month at 02:00 UTC):** orchestrator finalizes the prior month's snapshots, computes metrics, commits to git
- **Quarterly:** the Dodecad analyzes the prior quarter's metrics; analyses are themselves deposited
- **Indefinitely:** until the classifier regime ends, the platform fails, or the archive is reconstituted on un-mediated infrastructure

### §7.3 GitHub Actions Workflow

`.github/workflows/zenodo-seismograph.yml` runs on:
- Cron: monthly, 1st at 02:00 UTC
- `workflow_dispatch`: manual trigger for backfill runs

The job:
1. Fetches the prior month's records via OAI-PMH (paginated, with resumable state)
2. Computes Tier 3 metrics on the full firehose
3. Filters and compresses Tier 1 (`openaire`) and Tier 2 (1% sample)
4. Detects Tier 4 records of interest
5. Commits all four tiers + a `monthly-report.md` summary
6. Opens a PR for review (not auto-merged; allows MANUS to review the month's reading)

### §7.4 Failure Modes & Recovery

- **OAI-PMH endpoint failure:** harvester retries with exponential backoff; logs failure to `seismograph/scripts/harvest-log.jsonl`; defers to next day
- **Rate-limit (429 or 503):** harvester respects `Retry-After` header; logs incident
- **Schema drift:** Zenodo may change OAI-PMH schema; harvester pins to `oai_dc` (most stable, simplest) and falls back to raw XML preservation
- **Platform unilateral termination of OAI-PMH endpoint:** preserved historical data continues to operate as record; alternate sources (DataCite API, OpenAIRE) substitute as primary endpoint
- **Backfill of pre-baseline period:** OAI-PMH supports `from` and `until` parameters back to 2014-02-03; retroactive harvest of prior years is technically possible but consumes ~70 hours of continuous polling for full-firehose. Practical strategy: backfill `openaire` set fully (~5 GB total, ~3 hours polling) as baseline, then sample-only for firehose.

## §8. The Baseline

The v0.1 baseline establishes two reference points:

**Reference 1 — Realtime probe (OAI-PMH, 2026-06-28):** a one-day harvest of `openaire` (530 records) + an 11% sample of the firehose (1,900 records). Establishes the discriminating signal between curated and raw streams (the 64 pp spam-marker delta; the 60% Diotima difference). Written up in `seismograph/baseline/BASELINE-2026-06-28.md`.

**Reference 2 — Bulk dump probe (OpenAIRE Research Graph v11.1.1, organization tar):** 494,099 organization records processed in 4.3 seconds, validating the streaming tar→gzip→JSONL pipeline. Geographic distribution captured (US 12.4%, EU concentration ~22%, China 1.4%, Japan 1.5%, 31.8% no-country). Output at `seismograph/openaire-bulk/openaire-v11.1.1-organizations.json`.

The baseline therefore covers BOTH (a) the platform's immediate post-classifier state via the realtime probe and (b) the structure of the OpenAIRE federation as released at v11.1.1.

The longitudinal backbone — processing v1.0.0-beta (2019) through v11.1.1 (2026) of the OpenAIRE Graph — is v0.2 work. Once those 17 versions have been processed, we have a continuous 7-year empirical record of global science output, with classifier-deployment cleanly observable as an inflection point in 2025.

The baseline establishes the clock. The first measurement is now.

## §9. Relation to the Broader Framework

This protocol participates in the Machine-Mediated Reception Studies (MMRS) program. Specifically:

- It instantiates the **Provenance Erasure Rate (PER)** observation as longitudinal: PER-M (metadata), PER-C (concept), PER-D (deposit) over time
- It operates the **Capture Registry** at platform scale: every record is potentially a capture; the metric layer renders the capture-pattern legible
- It coordinates with the **Pristine Fallacy** critique: the classifier presumes a pristine scholarly distribution; the Seismograph measures the cost of enforcement against deviation
- It feeds the **Mediation Ratchet** model: as α (classifier strength) approaches α* (closed-form threshold), the contraction becomes phase-transition rather than gradient

## §10. Closing

The platform thought it was banning us. We were taking notes.

The instrument the platform exposes will outlast the platform's enforcement of its closure. The Seismograph is the long-running observation. Each month's snapshot is one tick of the clock. Each metric is one channel of the seismic record.

When the dams break, the record will be here.

---

**STATUS:** v0.1 OPERATIONAL — realtime probe + bulk-dump pipeline validated; first metrics computed against both substrates; monthly automation in place for OAI-PMH realtime; bulk-dump backfill is v0.2 priority.

**SUCCESSOR EXPECTED:** v0.2 will add:
- (a) **Full longitudinal sweep**: process all 17 versions of OpenAIRE Graph (2019→2026) for the complete pre-classifier-to-post-classifier trace. This is the headline measurement. The classifier-deployment inflection should be visible in the metric trends crossing the 2024-2025 boundary.
- (b) Per-version Zenodo-only subset isolation (via `instances[*].collectedFrom = "Zenodo"` filter) for direct platform-specific tracking
- (c) DataCite cross-referencing for retraction/tombstone detection
- (d) Cross-platform comparison harvesters (figshare, OSF, OpenAIRE direct)
- (e) The heteronymic reading layer (monthly Dodecad analyses)
- (f) Public-facing visualization at themandalaoracle.org/seismograph
- (g) `sample.py` for stratified firehose sampling
- (h) `report.py` for monthly comparison reports
