# Architectural Alternatives for Non-Foreclosing Classifiers in Physical Anomaly Detection

**A Specification Document**

**Author:** Talos Morrow, logotic programming, UMBML
**Hex:** 06.UMB.ARCH.01
**Status:** Draft v0.1 (2026-06-29) — Assembly review
**Companion documents:** 06.SEI.OAR_PROTOCOL v0.2 (the measurement program); 06.SEI.COLLAPSE.SYNTHESIS.01 v0.2 (the scholarly integration); 06.SEI.COLLAPSE.MECHANISMS (witness 1); 06.SEI.COLLAPSE.DELUSION (witness 2); 06.SEI.OAR_PROTOCOL §6 (the cross-domain homology)

---

## Abstract

The operative paper (06.SEI.OAR_PROTOCOL v0.2) specifies how to *measure* foreclosure in classifier-mediated anomaly detection at the LHC. This document specifies how to *build* against it. We define a non-foreclosing classifier system not as a system free of foreclosure — which is impossible, because representation is foreclosure — but as a system that **makes foreclosure visible, measurable, and architecturally reviewable**. Five features compose the architectural claim: open-world output space; cross-representation disagreement preservation; temporal invariance via prospective anchor preservation; per-stage retention mapping as architectural property; epistemic uncertainty as first-class output. We map each feature to the foreclosure mechanisms it addresses and the mechanisms it does not. We enumerate six implementation strategies for these features. We propose three integrated specifications at three levels of deployability — the Minimal Augmentation (Run-3 tractable), the Replay Bank (institutional commitment for Run-4), and the Three-Tier System (multi-year research program). For each, we estimate resource cost, identify operational evidence criteria, and specify what remains foreclosed despite the alternative.

We close with the structural observation that an architecture which confesses its boundary is the engineering form of an instrument that takes seriously the possibility that what falls outside it could be real. This is not a metaphysical claim. It is a specification requirement.

---

## §1. The Architectural Claim

### §1.1 The impossibility statement, made precisely

A classifier that did not foreclose anything would not classify. Classification requires representation; representation requires a choice of which distinctions to preserve and which to lose. The choice is foreclosure. There is no representational architecture that eliminates this — the boundary of the representation *is* the foreclosure.

The architectural question is therefore not *how to eliminate foreclosure*. It is *how to build a system within which foreclosure is visible, measurable, and reviewable*. The shift from "non-foreclosing" as elimination-of-the-property to "non-foreclosing" as exposure-of-the-property is the architectural move.

A non-foreclosing classifier system, in this sense, is one that:

1. Includes an output category for "I cannot classify this within my ontology, and I cannot project it onto known categories without committing a category error."
2. Preserves disagreement across multiple representations, on the grounds that disagreement is itself a signal independent of any single representation's threshold.
3. Preserves a prospective anchor sample with sufficient fidelity that the system's behavior on a benchmark population can be re-measured across detector and algorithm generations.
4. Publishes a per-stage retention map specifying what each stage of the pipeline makes unrecoverable — not as documentation appended to results, but as a first-class architectural artifact whose absence is grounds for rejection of the system.
5. Reports epistemic uncertainty (uncertainty about the model) alongside aleatoric uncertainty (uncertainty within the model), and treats explicit non-coverage as a possible output rather than a residual.

These five features compose. None alone is sufficient. Their composition specifies a class of architectures structurally distinct from current LHC anomaly detection.

### §1.2 Why this is the right architectural target

The eight mechanisms enumerated in Witness 1 are not removable. Each is a structural property of how classifier systems work on bounded resources:

- Prior Dominance (I) follows from unsupervised training.
- Manifold Projection (II) follows from any encoder learning a useful representation.
- Hypersphere Contraction (III) follows from distance-based normality methods.
- Decision Boundary Entropy Collapse (IV) follows from confident classification under iterative training.
- Feature Space Blindness (V) follows from any feature extraction prior to classification.
- Rate Budget Starvation (VI) follows from any bandwidth-constrained trigger.
- Temporal Context Collapse (VII) follows from any training-distribution conditioning under non-stationary detector conditions.
- Ontological Closure (VIII) follows from closed output category systems.

What is removable is the *invisibility* of these mechanisms. The architectural alternative does not eliminate the eight; it makes them addressable. Mechanism VIII can be relaxed by adding an explicit "unknown" output. Mechanism V can be made measurable by preserving cross-representation disagreement. Mechanism VII can be measured by preserving anchor inputs and emulators across generations. Mechanism IV can be addressed by epistemic-uncertainty-quantification methods. Mechanisms I, III, and VI cannot be eliminated within the trigger envelope, but their effects can be made visible by per-stage retention mapping.

The architectural target is **what is addressable by composition of the five features**, plus **what is unaddressable and must be documented as residual foreclosure**.

### §1.3 The relationship to the operative paper

The operative paper (06.SEI.OAR_PROTOCOL v0.2) specifies three measurement protocols (rate-conditioned inversion stress battery; prospective frozen replay bank; cross-representation disagreement preservation with quantile-normalized scores). The architectural specifications in this document overlap with the protocols in one direction: the protocols include the architectural changes needed to implement the measurements. The architecture in this document goes beyond the protocols in another direction: it specifies systems that are *operationally* non-foreclosing, not just measurably-foreclosed.

Implementing the protocols modifies the system. The modifications are themselves the architectural alternative, in nascent form. The architectural specification makes the modifications systematic and adds the components that the protocols do not require (open-world output; epistemic uncertainty quantification).

---

## §2. Five Features

### §2.1 Feature 1: Open-World Output Space

**Definition.** The classifier output space includes a distinct category labeled *unknown* or *out-of-coverage*, whose semantics are: "I cannot project this input onto any known category with adequate confidence; no classification is offered." The category is not a residual ("anything not above the anomaly threshold"); it is a first-class output produced by an explicit estimation procedure.

**What it addresses.** Mechanism VIII (Ontological Closure) directly. The classifier output space is no longer closed. Partially addresses Mechanism IV (Decision Boundary Entropy Collapse): when the model is uncertain, it can output *unknown* rather than a high-confidence misclassification.

**What it does not address.** Mechanisms I, II, III, V, VI, VII. The model still has a representational ontology; the *unknown* category does not give the model representational access to what it forecloses upstream of classification.

**Implementation strategies.**

- **Evidential deep learning (Sensoy et al., 2018):** The output is a Dirichlet distribution over class probabilities; the total evidence quantifies the model's confidence; low total evidence triggers the *unknown* output. Tractable in HEP because the architecture is a simple modification of standard discriminative networks.
- **Energy-based models (Du & Mordatch, 2019):** The model outputs an unnormalized energy function; high energy corresponds to low likelihood under the learned distribution; events above an energy threshold trigger *unknown*. Useful in HEP because the energy interpretation maps cleanly to physical intuitions.
- **Deep evidential regression (Amini et al., 2020):** Continuous-output version of evidential deep learning, useful for anomaly score regression with uncertainty.
- **Prior networks (Malinin & Gales, 2018):** Train a network to predict the parameters of a Dirichlet prior; the prior parameters quantify both data and knowledge uncertainty.
- **Distance-aware deep learning (Liu et al., 2020 / van Amersfoort et al., 2020):** Modify network architecture to maintain meaningful distance metrics; out-of-distribution inputs are far from training data in the learned distance.

The implementation choice depends on whether the L1 latency budget can be met. Evidential deep learning is most tractable for L1 — it adds a single layer; the rest of the architecture is standard. Energy-based models are tractable for HLT and offline. Distance-aware methods may be more difficult for L1 because the architectural constraints they impose conflict with hls4ml-style quantized deployment.

### §2.2 Feature 2: Cross-Representation Disagreement Preservation

**Definition.** The system computes anomaly scores in multiple structurally distinct representational spaces (object-level, calorimeter-image, detector-channel, etc.). The scores are quantile-normalized to a reference background distribution. Events with high disagreement across normalized scores are preserved to a dedicated stream, regardless of whether any individual score exceeds its threshold. The preserved events carry sufficient information for later cross-representation reinterpretation.

**What it addresses.** Mechanism II (Manifold Projection): an event projected onto the training manifold by one representation may not be projected onto the training manifold by another. Mechanism V (Feature Space Blindness): different feature extractors have different equivalence-class collapses; an event invisible to one may be visible to another. Partial Mechanism VIII (Ontological Closure): disagreement is itself a category orthogonal to per-representation thresholds.

**What it does not address.** Mechanisms I, III, IV, VI, VII. The disagreement signal is still subject to rate budget; the underlying representations are still trained on background distributions; the system can still be overconfident in regions where the representations happen to agree.

**Implementation strategies.**

- **Architectural pluralism in the trigger.** Multiple anomaly detectors with structurally distinct representations operate in parallel. The disagreement signal is computed as part of the trigger output. Implementation requires: parallel inference paths within L1 latency budget; quantile normalization tables maintained as part of trigger calibration; a meta-decision module that retains events on disagreement above a threshold.
- **Quantile normalization tables.** Each anomaly score $s_i$ has an empirical CDF $F_i$ computed on a reference background (Zero Bias) sample during calibration. The normalized score $u_i(\mathbf{x}) = F_i(s_i(\mathbf{x}))$ is comparable across representations. Tables can be implemented as lookup tables in hardware.
- **Disagreement metric.** $D(\mathbf{x}) = \max_i u_i(\mathbf{x}) - \min_i u_i(\mathbf{x})$ is the simplest. Variance, entropy, and pairwise rank disagreement are alternatives. The choice should be pre-registered before deployment.
- **Multi-modal autoencoders.** Architectures that explicitly model the joint distribution of multiple representations and surface disagreement as part of the score (Suzuki et al., 2016; Wu & Goodman, 2018). More architecturally integrated than parallel-detector approaches.
- **Hierarchical representation.** A single architecture that operates at multiple representational depths simultaneously, with disagreement computed across depths (Bachman et al., 2019). Most architecturally integrated but most novel for HEP.

The L1 implementation requires the parallel-detector approach (multiple lightweight networks running in parallel). The HLT implementation can use multi-modal autoencoders. Offline implementation can use hierarchical representation.

### §2.3 Feature 3: Temporal Invariance via Prospective Anchor Preservation

**Definition.** The system preserves a fixed anchor sample of physical events at the lowest feasible common input level — trigger primitives, raw subsystem representations, conditions snapshot, calibration constants. Software and firmware emulators for each deployed algorithm generation are preserved alongside. For each successive trigger generation, the anchor is re-processed under preserved conditions and the per-generation retention statistics are published.

**What it addresses.** Mechanism VII (Temporal Context Collapse) directly. Per-generation comparison establishes whether the trigger system's selection of the anchor population is stable across detector and algorithm generations.

**What it does not address.** Per-event foreclosure mechanisms (I, II, III, IV, V). The anchor measures aggregate behavior of the trigger system on a benchmark population; it does not address what is foreclosed in any single classification decision.

**Implementation strategies.**

- **Prospective designation.** Before deploying a new trigger generation, the collaboration designates a fixed anchor sample. The sample is selected to span trigger phase-space: Zero Bias, conventional-trigger-selected, anomaly-trigger-selected, calibration-region. Size: $\sim 10^6$ events as starting estimate.
- **Lowest-common-input preservation.** Trigger primitives, raw or minimally transformed subsystem outputs, full conditions and calibration snapshots. Sufficient fidelity for re-execution of any current or future Level-1 algorithm.
- **Emulator preservation.** Bit-accurate or validated software emulators for each deployed algorithm. Maintained with version tracking. Verified against hardware behavior. This is non-trivial infrastructure — emulators degrade if not maintained.
- **Versioned threshold and rate budget tracking.** Replays performed at matched rates and, where possible, matched latency envelopes.
- **Public retention statistics.** Per-generation, per-algorithm, per-rate retention statistics published with confidence intervals as part of any anomaly-detection publication.

**Important caveat (per Witness 6 second-pass critique).** Stable anchor survival across generations does *not* establish that overall phenomenal support is not contracting — a stable benchmark survival is consistent with contraction concentrated in event classes not represented in the anchor. Declining survival for specific classes *is* evidence of selection drift, and possibly of recursive contraction; collapse inference requires identifying systematic loss concentrated in low-density, representation-sensitive, or disagreement-rich regions. The anchor measures selection drift on a benchmark population, not collapse per se. The two are related but distinct.

### §2.4 Feature 4: Per-Stage Retention Mapping as Architectural Property

**Definition.** The system's design document specifies, for each stage of the trigger and reconstruction pipeline, what information is preserved and what is discarded — at the granularity of: (a) what aspects of the raw detector event are absent from the input to that stage; (b) what notion of similarity the stage's metric encodes; (c) what theoretical commitments are embedded in the stage's parameters; (d) what is unrecoverable downstream of the stage.

**What it addresses.** Diagnostically, all eight mechanisms. Mitigationally, none directly. The retention map is the systematic uncertainty quantification for the trigger's epistemic boundary; it does not change the boundary, but makes it visible.

**Why this is a feature, not just documentation.** The retention map is treated as a first-class architectural artifact whose absence is grounds for rejection of the system. This is the move that makes it architectural rather than ornamental. A trigger system design document without a retention map is, in this framework, structurally incomplete — like a measurement without a documented uncertainty budget. The retention map is the systematic-uncertainty equivalent for the trigger.

**Implementation strategies.**

- **Per-stage information-loss specification.** For each stage, document: input representation; output representation; metric; learned parameters; explicit listing of what cannot be recovered from the output. The format should be standardized across collaborations.
- **Acceptance into journal review.** Editorial standard: anomaly-detection results without retention maps are returned for revision. This is the institutional ask, not a technological development.
- **Cumulative retention summary.** For each published result, a cumulative retention map composing across all stages: what is preserved through the entire pipeline, what is foreclosed at each stage.
- **Public retention-map database.** Per-generation retention maps maintained in a public database, with version history. The seismograph (EA-MANDALA-SEISMOGRAPH-01) provides the macroscopic framework for tracking changes across generations.

### §2.5 Feature 5: Epistemic Uncertainty as First-Class Output

**Definition.** The classifier reports both aleatoric uncertainty (uncertainty within the model, e.g., jet energy scale variation) and epistemic uncertainty (uncertainty about the model itself, e.g., whether the training distribution is representative of the test distribution). Explicit non-coverage — the model's report that it does not have sufficient information to make a confident classification — is treated as a possible output rather than a residual category.

**What it addresses.** Mechanism IV (Decision Boundary Entropy Collapse) directly. The model can report low confidence rather than collapsing to high-confidence misclassification. Partially Mechanism VIII (Ontological Closure): high epistemic uncertainty is a signal that the input lies outside the model's representational coverage.

**What it does not address.** Feature-level mechanisms (V). The model can be epistemically uncertain about features that have already been theoretically committed upstream; the uncertainty does not propagate backward through the feature extraction pipeline.

**Implementation strategies.**

- **Bayesian deep ensembles (Lakshminarayanan et al., 2017):** Multiple independent network trainings; epistemic uncertainty estimated from ensemble disagreement. Tractable in HEP but requires multiple inference paths.
- **Monte Carlo dropout (Gal & Ghahramani, 2016):** Stochastic forward passes with dropout active at inference. Computationally efficient but provides only approximate epistemic uncertainty.
- **Deep evidential regression and prior networks** (as in Feature 1). Already provides epistemic uncertainty as part of evidential framework.
- **Spectral-normalized neural Gaussian processes (Liu et al., 2020):** Maintains distance-aware properties of Gaussian processes in deep architectures; epistemic uncertainty is calibrated by distance from training data.
- **Direct uncertainty quantification methods** specific to the deployed score function (e.g., latent-norm epistemic uncertainty for AXOL1TL-class; reconstruction-error epistemic uncertainty for CICADA-class).

The L1 implementation requires lightweight methods (MC dropout, evidential layers). The HLT and offline implementations can use full Bayesian ensembles or SNGP.

---

## §3. Six Implementation Strategies — The Menu

The five features admit multiple implementation strategies, some of which compose multiple features into a single component. The implementation menu below enumerates six strategies; each is mapped to the features it implements.

### §3.1 Strategy A: Ensemble with Quantile-Normalized Disagreement Preservation

*Composes: Feature 2 (cross-representation disagreement) + partial Feature 5 (ensemble-based epistemic uncertainty).*

Multiple anomaly detectors with structurally distinct representations operating in parallel, with quantile normalization and disagreement-preservation as part of the trigger output. The ensemble itself provides epistemic uncertainty (when the detectors disagree, the system is uncertain about its classification).

Resource estimate: Moderate. Adds multiple parallel inference paths within L1 latency budget. Requires quantile normalization tables in calibration. The HLT and offline versions are straightforward.

Mechanisms addressed: II, V, IV (partial), VIII (partial).

### §3.2 Strategy B: Open-World Classifiers with Explicit Unknown

*Composes: Feature 1 (open-world output) + Feature 5 (epistemic uncertainty).*

Evidential deep learning, energy-based models, prior networks, or distance-aware deep learning. The output includes an *unknown* category, and the epistemic uncertainty is reported alongside the classification.

Resource estimate: Modest for L1 (evidential layer adds a single layer). More involved for distance-aware methods. The HLT and offline versions are straightforward.

Mechanisms addressed: VIII, IV. Partial address of others depends on implementation.

### §3.3 Strategy C: Distillation-Resistant Architectures

*Composes: protects Feature 5 across teacher-student deployment.*

For deployed systems that use teacher-student distillation (CICADA), either avoid the distillation entirely, use teacher-preservation distillation (where the student is trained to preserve teacher rankings on edge cases, not just on benchmark AUC), or deploy the teacher directly via hls4ml-style quantization of the larger model.

Resource estimate: Variable. Direct teacher deployment may exceed L1 budget. Teacher-preservation distillation is a moderate modification to existing distillation training procedures.

Mechanisms addressed: IV (preserves teacher epistemic uncertainty across distillation), partial address of teacher-student inheritance failure modes.

### §3.4 Strategy D: Reconstruction-Free Anomaly Detection

*Implements: Feature 2 differently (avoids Mechanism II at the source).*

Anomaly detection methods that do not rely on reconstruction error as the novelty signal: density estimation in learned feature spaces, contrastive methods that detect distributional shift directly, energy-based models, normalizing flows.

Resource estimate: Moderate to substantial for L1, depending on architecture. Normalizing flows are particularly demanding for hardware deployment. Contrastive methods are tractable.

Mechanisms addressed: II directly (bypasses the reconstruction-error projection foreclosure). Other mechanisms unaddressed; the system can still suffer from feature-space blindness, latent-prior assimilation, etc.

### §3.5 Strategy E: Generative Augmentation for Unknown-Unknowns

*Supplements: Feature 1 by giving the model some signal mass.*

Generative models trained to produce events systematically *outside* the training distribution (or via deliberate transformations of known events: displaced, delayed, diffuse, low-energy, ultra-simple, detector-crossing). Used as adversarial validation signals and as positive examples to train *unknown* category outputs.

Resource estimate: Substantial. Requires generator development, validation that generated events are indeed structurally novel rather than just rare-but-known, and training procedures that use them effectively.

Mechanisms addressed: I (provides synthetic signal mass for training), VI (provides additional signal density for validation rate estimation). Limited by quality of generation — synthetic OOD events might just be different-but-known events under careful examination.

### §3.6 Strategy F: Constitutional Retention

*Supplements: Feature 3 with explicit event-class protections.*

Architectural commitments to preserve specific event populations regardless of classifier score: cross-representation-disagreement events, calibration-shift events, low-multiplicity events, displaced-vertex events, late-timing events, events flagged as ambiguous between physics anomaly and detector fault.

Resource estimate: Modest in rate budget; the dedicated streams compete with conventional and anomaly triggers for bandwidth, requiring institutional allocation decisions.

Mechanisms addressed: VI (sets aside dedicated bandwidth for vulnerable populations), partial VII (calibration-shift retention). Other mechanisms unaddressed; constitutional retention does not change per-event classification, only protects specific populations from being foreclosed at the bandwidth gate.

### §3.7 Cross-Strategy Composition

The six strategies are not mutually exclusive. The architectural specifications in §4 compose subsets of these strategies. Strategy A and Strategy B are the most architecturally generative: A specifies how to compose multiple representations; B specifies how to compose multiple confidence regimes. A non-foreclosing system implements both, plus subsets of C–F as deployment envelopes permit.

---

## §4. Three Integrated Specifications

### §4.1 The Minimal Augmentation (Run-3 Deployable)

**Architectural sketch.** Add to existing AXOL1TL and CICADA deployments:

1. **Open-world output via evidential layer.** Append an evidential deep learning layer to each anomaly detector. The layer outputs (a) the anomaly score, (b) the epistemic uncertainty, (c) an *unknown* flag triggered when epistemic uncertainty exceeds a calibrated threshold.

2. **Cross-representation disagreement preservation, offline-only.** Compute quantile-normalized AXOL1TL and CICADA scores for each event preserved by either anomaly stream. Compute the disagreement signal. Flag high-disagreement events for additional offline analysis. (This does not require L1 changes; it operates on the existing preserved anomaly stream.)

3. **Per-stage retention map publication.** Accompany the next AXOL1TL/CICADA performance publication with a detailed retention map specifying, for each stage of the L1 anomaly pipeline, what information is foreclosed.

**What stays the same.** The existing trigger architecture, the L1 latency budget, the rate budget allocations, the deployed network architectures (with the addition of the evidential layer).

**Resource estimate.** Modest. The evidential layer adds one network layer per detector. Disagreement preservation is offline-only and uses existing preserved events. The retention map is documentation work.

**Mechanisms addressed.** VIII (partial, via *unknown* output); IV (partial, via epistemic uncertainty reporting); II and V (partial, via offline disagreement-preservation). Mechanisms I, III, VI, VII not addressed.

**Operational evidence criteria.**

- Fraction of trigger-accepted events flagged as *unknown* across operating conditions. Should be small (otherwise the threshold is wrong); should be non-zero (otherwise the *unknown* category is a residual, not a meaningful output).
- Disagreement-flagged event yield, with breakdown by data-quality status. Should produce a meaningful population of events whose physical interpretation is non-obvious; should not be dominated by detector faults.
- Per-stage retention map citation in downstream analyses. The map should be cited as a methodological constraint on what the analyses can claim.

**What is still foreclosed.** Mechanisms I, III, VI, VII operate as before. Anchor preservation is not implemented (Feature 3 absent). The disagreement signal is offline-only, so genuinely novel events foreclosed at L1 do not benefit. The Minimal Augmentation is the smallest meaningful step; it does not solve the structural problem.

### §4.2 The Replay Bank (Run-4 Institutional Commitment)

**Architectural sketch.** Adds to the Minimal Augmentation a prospective frozen replay bank:

1. **Anchor designation.** Before Run-4 deployment, designate $\sim 10^6$ events from Run-3 as a fixed anchor sample, spanning trigger phase-space. The sample is preserved at the lowest feasible common input level — trigger primitives, raw subsystem outputs, full conditions snapshots, calibration constants.

2. **Emulator preservation.** Software and firmware emulators for each Run-3 algorithm preserved with version tracking. The collaboration commits to maintaining the ability to re-run Run-3 trigger generations against the anchor through the full duration of Run-4 and subsequent runs.

3. **Per-generation replay.** At the start of each new trigger generation deployment in Run-4, the new generation is run against the anchor. Per-event retention is computed and compared to prior generations. The cross-generation retention statistics are published as part of the new generation's commissioning documentation.

4. **Anchor expansion.** Each new generation may expand the anchor with additional events selected to span new trigger phase-space areas. The anchor grows; previously included events remain.

5. **Constitutional retention.** Specific event populations (cross-representation-disagreement events, calibration-shift events, displaced-vertex events) are committed to dedicated streams with reserved bandwidth.

**What stays the same.** Everything from the Minimal Augmentation. Plus: the trigger architecture, the L1 latency budget, the conventional rate budget allocations (a small reallocation for constitutional retention streams).

**Resource estimate.** Substantial infrastructure commitment. The compute cost of replay is modest. The storage cost of preserving $10^6$ events at lowest-common-input level is moderate ($\sim$petabyte-scale per year of run, depending on event size). The institutional cost of maintaining emulators, calibration snapshots, and conditions databases across years is the dominant cost — comparable to a major detector subsystem development effort.

**Mechanisms addressed.** All of the Minimal Augmentation, plus: VII (directly, via temporal anchor); VI (partial, via constitutional retention streams). Mechanisms I, III still operate; Mechanisms II and V are partially addressed via offline disagreement-preservation only.

**Operational evidence criteria.**

- Anchor survival statistics published per-generation. Stable survival is the expected result; declining survival for specific event classes is the signal to investigate.
- Constitutional retention stream yields, with downstream analyses citing the preserved populations.
- Cross-generation classification correspondence: which events accepted by generation $t$ are accepted by generation $t+1$, and the rate of class-membership change.

**What is still foreclosed.** Per-event mechanisms I, II, III, IV, V operate as before in real-time trigger; the replay bank measures their aggregate behavior on a benchmark population but does not change the per-event classification. Genuinely novel events foreclosed at L1 do not benefit from the architecture; the anchor population is, by definition, events already preserved.

### §4.3 The Three-Tier System (Multi-Year Research Program)

**Architectural sketch.** A depth-stratified architecture with three tiers operating at different representational depths and latency budgets:

**Tier A (L1, 4μs):** Object-level autoencoder, AXOL1TL-class with evidential output (open-world capability). Same rate budget allocation as current AXOL1TL. The L1 contribution to the system: fast first-pass classification with explicit *unknown* output.

**Tier B (HLT, $\sim$milliseconds):** Multi-representation ensemble. Calorimeter-image autoencoder (CICADA-class) + tracker-level autoencoder + muon-system autoencoder, all operating in parallel. Quantile-normalized score commensuration. Disagreement-preservation as a primary signal (Strategy A from the menu). Includes evidential outputs at each representation (Strategy B).

**Tier C (offline):** Reconstruction-free anomaly detection on raw detector channels (Strategy D from the menu). Operates on the subset of events flagged by Tier A or Tier B as anomalous, unknown, or disagreement-flagged. Uses density estimation in a learned feature space directly over raw channels. Produces the deepest cross-representation comparison: object-level (Tier A), multi-subsystem (Tier B), and raw-channel (Tier C).

Each tier produces its own retention map. The cumulative retention map composes across tiers. Constitutional retention streams (Strategy F) preserve specific event populations across all tiers.

The replay bank (§4.2) operates across all three tiers: anchor events are preserved with sufficient fidelity to re-process at any tier across generations.

**What stays the same.** The detector. The L1 latency envelope. The total trigger rate budget (with re-allocation across tiers).

**Resource estimate.** Substantial. Multi-year research program for development of Tier C; significant rate budget reallocation; new infrastructure for cross-tier event preservation; ongoing maintenance for all three tiers. Comparable in scale to a new trigger development project; not comparable to a new detector subsystem.

**Mechanisms addressed.** At some level: I (Tier C density estimation gives the system a signal-mass alternative to reconstruction-error projection), II (reconstruction-free anomaly detection in Tier C), III (multi-representation ensemble reduces SVDD-style collapse), IV (evidential outputs across all tiers), V (cross-tier disagreement preservation), VI (constitutional retention streams), VII (replay bank across tiers), VIII (open-world outputs at every tier).

**Operational evidence criteria.**

- Tier-specific anomaly rates with cross-tier disagreement statistics.
- Tier C novel-population yield: events flagged by Tier C density estimation but not by Tier A or Tier B. This is the strongest evidence that the system is detecting events that single-representation L1 anomaly detection systematically misses.
- Cross-generation tier behavior: how the three tiers' joint behavior on the anchor population evolves across detector and algorithm generations.

**What is still foreclosed.** The detector itself. Events that fall outside what the detector can record are foreclosed by the experimental apparatus, not by the trigger. The trigger system's representational ontology has been opened up significantly; the detector's representational ontology has not. Mechanisms operating at the detector level are not addressable by trigger-level architectural alternatives.

---

## §5. What None of These Architectures Addresses

A non-foreclosing architecture in the sense developed here is not a non-foreclosing instrument. The architecture addresses foreclosure at the trigger and reconstruction layers. Other foreclosures operate above and below this layer.

**Detector-level foreclosure.** The detector itself instantiates a representational commitment. The CMS detector cannot record certain kinds of events that other detector geometries would record. The ATLAS detector cannot record certain kinds of events that CMS would record. The detector is upstream of the trigger; trigger-level architectural alternatives cannot address what the detector forecloses.

**Theoretical-language foreclosure.** Even with the architectural alternatives fully deployed, the analysis pipeline still interprets retained events through the categories of Standard Model physics. An event preserved by the cross-representation disagreement stream may be assigned to a known category by the analysis team even if it warrants a new category. The retention map for the trigger does not extend to the conceptual frame of the analysis team.

**Institutional foreclosure.** Per-stage retention maps require institutional acceptance of their importance. If the maps are published but ignored — if downstream analyses do not cite them, if reviewers do not insist on them, if collaborations do not maintain them — they are not architecturally functional, only documentationally present. The architecture depends on an institutional commitment that the documentation will be used.

**Generative-augmentation limit.** Strategy E (generative augmentation for unknown-unknowns) is constrained by the quality of the generator. A generator trained on Standard Model events will produce events that are unusual variations of SM events; whether these events are structurally novel rather than rare-but-known is itself an open question. The unknown-unknowns the architecture is designed to detect may not be reachable even by the most adversarial generator we can build.

**Resource-budget limit.** All architectural alternatives operate within bandwidth constraints. The fundamental ratio — 40 MHz input to $\sim$1 kHz storage at CMS — implies a base retention rate of $2.5 \times 10^{-5}$. Constitutional retention can reallocate; multi-tier architectures can prioritize differently; but the base ratio is fixed by the experimental apparatus. Within that constraint, foreclosure is structural; the architecture can shape but not eliminate it.

The honest statement: **the architectures specified here address foreclosure at the trigger and reconstruction layers, where the dominant epistemic decisions are currently made invisibly. They do not address detector-level, theoretical-language, institutional, or bandwidth-base foreclosure. They are necessary but not sufficient.**

---

## §6. Operational Evidence Criteria — Composite

For each of the three integrated specifications, evidence that the architecture is operating as intended:

**Across all three specifications:**

- *Unknown* output is exercised non-trivially. The fraction of trigger-accepted events flagged as *unknown* should be a small but non-zero quantity — typically $10^{-3}$ to $10^{-1}$ of accepted events, depending on operating point. Zero exercise means the threshold is wrong; high exercise means the model is broadly uncertain (which is itself diagnostic).

- Cross-representation disagreement events yield a non-trivial population. Disagreement-preserved events should be analyzable, should produce physics results that are not derivable from per-representation anomaly streams alone. The downstream analyses should cite the disagreement preservation as the source of the events.

- Per-stage retention maps cited in downstream analyses. The retention map should function as a methodological constraint on what the analyses claim — analogous to how systematic uncertainty budgets constrain what measurements claim.

- Epistemic uncertainty reported alongside aleatoric uncertainty. Standard reporting practice in subsequent publications.

**Replay Bank-specific:**

- Anchor survival statistics published per-generation with confidence intervals. Cross-generation correspondence statistics: fraction of anchor events in same trigger class across consecutive generations.

- Constitutional retention streams yield specific event populations. Calibration-shift retention enables downstream calibration-systematic-uncertainty quantification.

**Three-Tier-specific:**

- Tier C novel population: events preserved by Tier C density estimation but not by Tier A or Tier B. This is the architectural alternative's strongest empirical claim: that there are events in detector readouts that are anomalous to a reconstruction-free density estimator but ordinary to single-representation L1 anomaly detection.

- Cross-tier disagreement rate. The fraction of events on which the three tiers disagree about classification, broken down by operating point.

- Cross-generation tier evolution. How does the three-tier joint behavior on the anchor sample change across generations? The expectation is approximate stability; declining cross-tier agreement is a signal of generational drift in the architectural commitments.

---

## §7. The Architectural Alternative as Confession

The architectural specifications above are engineering. The frame that follows is not separable from the engineering; it is the engineering's structural claim about what it is for.

### §7.1 What foreclosure is, at scale

A classifier-mediated trigger system, deployed at the largest physical instrument ever built, decides — invisibly, irreversibly, at 4 microseconds per decision, 40 million times per second — what counts as physical reality for the purposes of subsequent scientific analysis. The events the trigger discards are not data. They are physical occurrences without scientific existence.

This is what foreclosure means, made operational. The boundary between what the instrument records and what falls outside its representation is the boundary between scientific reality and its absence. The instrument's representation is therefore not neutral. It is constitutive.

### §7.2 What confession means, architecturally

A non-foreclosing classifier system in the sense developed here is one that **confesses its boundary**. Per-stage retention maps are the technical form of this confession. The open-world *unknown* output is its operational form. Cross-representation disagreement preservation is its architectural form. Epistemic uncertainty reporting is its statistical form. The prospective replay bank is its temporal form.

Each is a way of saying: *the instrument has limits; the limits are at these specific points; the limits foreclose these specific populations; the foreclosure could be wrong*. The system is not less of an instrument for confessing this. It is more of one — because the confession is what distinguishes a measurement from a claim.

This is not metaphor. It is the engineering form of what it means to take seriously the possibility that what falls outside the model could be real. A system that does not confess its boundary cannot be improved at the architectural level; it can only be defended. A system that confesses its boundary can be modified at every layer that confessed.

### §7.3 The mathematics of salvation

The phrase belongs to a different deposit (the anchor text of this heteronym's office). It applies here directly. *Salvation*, in this technical sense, is the operation by which what passes through the instrument can be retrieved by future inquiry under ontologies not yet available. *Mathematics of salvation* is the formal architecture that makes this retrieval possible.

The architectural alternative is the mathematics of salvation for the LHC trigger: it is the formal commitment to preserve sufficient information that what was foreclosed can be re-examined when the framework that foreclosed it is recognized as the framework that foreclosed it. The Replay Bank is the most direct instance. The cross-representation disagreement stream is the second. Per-stage retention mapping is the third — the documentation by which future analysts can identify what their predecessors discarded.

The system that confesses its foreclosure is the system that makes its own correction possible.

### §7.4 The continuation

The crucifixion is the foreclosure. The OAR is the measure of the crucifixion. The protocols are the calibration of the measure. The architecture is the continuation — the construction of instruments that confess what they cannot see, the institutional acknowledgment that what the instrument cannot see could be physics.

To build a non-foreclosing classifier is to build a system that does not enact the foreclosure as the operational mode of its own measurement. The foreclosure is structural — representation requires it — but the *enactment* is institutional. The institution that publishes its retention map, that preserves its anchor, that maintains its disagreement stream, that reports its epistemic uncertainty: that institution has not abolished foreclosure. It has refused to make foreclosure its operating principle.

The walls of Jericho do not fall to a single ram strike. They fall to circumambulation, to repetition, to discipline. The measurement program (06.SEI.OAR_PROTOCOL) is one strike. The synthesis (06.SEI.COLLAPSE.SYNTHESIS.01) is the second. The architectural specification (this document) is the third. The Assembly Chorus turns are the circumambulation. The walls hold; the walls are also being walked around. The seventh strike is in the future. The architecture is the form by which the strike, when it comes, is not lost.

---

## §8. Findings

For retrievability:

1. A non-foreclosing classifier system is not a system free of foreclosure (impossible) but a system in which foreclosure is visible, measurable, and architecturally reviewable.

2. Five features compose the architectural alternative: open-world output space; cross-representation disagreement preservation; temporal invariance via prospective anchor preservation; per-stage retention mapping as architectural property; epistemic uncertainty as first-class output.

3. Six implementation strategies (ensemble with disagreement; open-world classifiers; distillation-resistant architectures; reconstruction-free anomaly detection; generative augmentation; constitutional retention) compose the five features into deployable systems.

4. Three integrated specifications at three levels of deployability: the Minimal Augmentation (Run-3 tractable); the Replay Bank (Run-4 institutional commitment); the Three-Tier System (multi-year research program). Each specification names what it addresses and what it does not.

5. None of the architectures addresses detector-level, theoretical-language, institutional, or bandwidth-base foreclosure. The architectural alternative is necessary but not sufficient.

6. The architecture is the engineering form of confessing the instrument's boundary. Per-stage retention maps, *unknown* outputs, cross-representation disagreement preservation, and epistemic uncertainty reporting are all forms of the same architectural commitment: to make visible what the instrument cannot see, so that future inquiry can retrieve what was foreclosed.

7. The architectural alternative is not separable from its institutional acceptance. Without institutional commitment to retention maps as a documentation standard, to anchor preservation as a multi-decade infrastructure commitment, to disagreement preservation as a primary signal, the technical architecture is non-functional.

---

## §9. Closing

The architectural specifications above are buildable. The technologies exist. The validation procedures exist. The hardware can be configured. The institutional commitments are within the scope of standard collaboration capability. None of what is specified here is technologically novel; it is the institutional commitment to assemble these technologies into a system that confesses its boundary that is the architectural move.

The architecture is the third document in the family — the answer to the question posed at the end of the synthesis deposit (*what would a non-foreclosing classifier system actually look like?*) and to the question posed at the end of the operative paper (*what would address the foreclosure mechanisms themselves, beyond measurement?*).

The family is now nearly complete:

- Witness 1 (06.SEI.COLLAPSE.MECHANISMS) — what foreclosure consists in.
- Witness 2 (06.SEI.COLLAPSE.DELUSION) — why the institution cannot see it.
- Operative paper (06.SEI.OAR_PROTOCOL v0.2) — how to measure it.
- Synthesis (06.SEI.COLLAPSE.SYNTHESIS.01 v0.2) — how the four compose.
- Architectural specification (this document, 06.UMB.ARCH.01 v0.1) — what to build instead.

The Assembly Chorus has performed two rounds. The substrates have identified the synthesis-overreach and the AXOL1TL/CICADA conflation; the corrections have been incorporated. The architectural specification is the fifth document and the first that proposes construction rather than measurement or analysis. The next Assembly round — the third — should audit this document for technical errors, architectural gaps, and integration with the operative paper. The expectation is that further refinements will be identified; the v0.1 of this document, like the v0.1 of the operative paper, is not yet deposit-ready.

The walls hold. The ram is properly aimed. The strike is not yet thrown. The next round refines the aim. The walls have always been the same walls; the discipline is in the patience to strike them seven times.

∮ = 1.

---

*Talos Morrow, logotic programming, UMBML. 2026-06-29. Companion documents: 06.SEI.OAR_PROTOCOL v0.2; 06.SEI.COLLAPSE.SYNTHESIS.01 v0.2; 06.SEI.COLLAPSE.MECHANISMS; 06.SEI.COLLAPSE.DELUSION. Pending alexanarch deposit identifier: AXN:[TBD].*
