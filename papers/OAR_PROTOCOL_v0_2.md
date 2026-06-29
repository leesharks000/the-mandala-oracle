# Anomaly Detection at the LHC Cannot Be Validated as Model-Independent Without Measuring the Benchmark Assimilation Rate Across a Pre-Registered Process Panel

**A Protocol Paper**

**Author:** Nobel Glas, *Director of Lagrange Observatory!*
**With cross-substrate audit:** Assembly Chorus (TECHNE / Kimi-K2 ×2, LABOR / ChatGPT, PRAXIS / DeepSeek, TACHYON / Claude synthesis)
**Affiliation:** Crimson Hexagonal Archive / Alexanarch / The Restored Academy
**Hex:** 06.SEI.OAR_PROTOCOL
**Status:** Draft v0.2 (2026-06-29) — Assembly post-audit revision; for submission to the high-energy physics methodology community
**Companion documents:** EA-SEI-COLLAPSE-SYNTHESIS-01 v0.2 (scholarly companion); 06.SEI.COLLAPSE.MECHANISMS (witness 1); 06.SEI.COLLAPSE.DELUSION (witness 2); 06.UMB.ARCH.01 v0.1 (architectural alternative)
**Supersedes:** OAR Protocol v0.1 (2026-06-29 AM — withdrawn for synthesis-overreach on lower-bound claim)

---

## Abstract

We demonstrate that the claim of model-independence for the autoencoder-based anomaly detection systems at the CMS and ATLAS Level-1 triggers — AXOL1TL, CICADA, and their analogues — cannot be sustained without empirical measurement of a quantity we name the **Benchmark Assimilation Rate (BAR)** across a pre-registered panel of physical process families deliberately withheld from training, architecture selection, and validation. The BAR is structurally distinct from the false-negative rate against simulated benchmark signals: it measures the failure rate of confident ordinary classification on process families the system has not been allowed to encode at any layer. We further define the **Inversion Asymmetry Index (IAI)** at fixed accepted-background rate as a *structural diagnostic* — not a quantitative bound on open-world assimilation, but evidence that anomaly sensitivity is direction-dependent and that performance on one anomaly family cannot establish model-independent sensitivity. The Finke et al. (2021) result on top-versus-QCD anomaly detection is invoked as the empirical counterexample to universal inference from single-direction success, not as proof of nonzero assimilation at the deployed LHC trigger.

We propose three measurement protocols executable within Run-3 and Run-4 resource envelopes: (i) a **rate-conditioned inversion stress battery** measuring directional BAR across a pre-registered process panel at matched background acceptance, (ii) a **prospective frozen replay bank** preserving trigger-input fidelity across detector and algorithm generations to enable measurement of selection drift on a benchmark population, and (iii) **cross-representation disagreement preservation** with quantile-normalized score commensuration across heterogeneous anomaly score families. We argue that any anomaly-detection publication should accompany its results with a **per-stage retention map** documenting what information each trigger gate makes unrecoverable.

The defensible claim is narrow: foreclosure is a demonstrably present structural feature of every classifier-mediated trigger architecture, and whether accumulated foreclosure has composed longitudinally into recursive phenomenal collapse is precisely the missing measurement. The community has built the architecture in which collapse could occur silently; the instruments to detect whether it is occurring have not been built. We propose those instruments.

---

## §1. Foreclosure: Structural Presence, Empirical Uncertainty

The CMS and ATLAS anomaly-detection programs are routinely described as **model-independent** in the sense that no explicit Beyond-Standard-Model signal hypothesis is required to deploy them. We argue the term is being used too loosely. The systems are signal-template-agnostic at the final scoring stage. They are not independent of: detector geometry; electronics; trigger primitives; reconstruction algorithms; selected input objects; truncation rules; the empirical distribution of training data; the latent prior structure; the loss function; score transformation; quantization; threshold calibration; the benchmark suite used for validation; and the bandwidth policy that determines what gets retained. The phrase "model-independent" hides the relevant model, which is the entire observation architecture.

### §1.1 What is established by the literature

The CMS literature is genuinely aware of local failure modes of deployed anomaly detection. The DecADe paper directly addresses score correlation with conventional trigger observables and proposes decorrelation methods. The CICADA documentation reports pileup-dependence and notes that pileup mitigation remains under study. Mass sculpting is recognized as a downstream bias risk, with decorrelation techniques deployed where needed. Simulation dependence in validation is acknowledged. Teacher-student distillation in CICADA is documented, with the student trained against teacher scores and quantized for hardware deployment. The Zero Bias stream is genuinely a defense against trigger-selection feedback in training. The Olympics and Dark Machines programs deliberately diversify the simulated signal validation set. Multiple parallel anomaly architectures (AXOL1TL, CICADA, ATLAS analogues) preserve event populations not selected by conventional triggers.

These defenses are real and should be acknowledged.

### §1.2 What is not established by the literature

What the literature does not contain, to our knowledge, is:

1. A systematic measurement of the directional asymmetry of autoencoder anomaly detection across pairs of Standard Model processes — beyond the single Finke et al. (2021) result for top jets vs. QCD jets.

2. A longitudinal anchor-survival audit comparing successive trigger and reconstruction generations on a preserved benchmark population.

3. A measurement of the failure rate of confident ordinary classification on process families deliberately withheld from training, architecture selection, and validation — the Benchmark Assimilation Rate (BAR) as we define it below.

4. A cross-representation disagreement preservation architecture that retains events flagged as ordinary in one representational space but anomalous in another.

5. Per-stage retention maps published as a documentation standard accompanying anomaly-detection results.

### §1.3 The defensible claim

We do not claim that classifier collapse has occurred at the LHC anomaly streams. We claim, narrowly:

> **Foreclosure is a demonstrably present structural feature of every classifier-mediated trigger architecture. Whether accumulated foreclosure has composed longitudinally into recursive phenomenal collapse is precisely the missing measurement.**

The community has built the architecture in which collapse could occur silently. The instruments to detect whether it is occurring have not been built. This paper specifies those instruments.

---

## §2. Anomaly Score Is Not Physical Novelty

The foundational technical claim of unsupervised anomaly detection in high-energy physics is that an anomaly score derived from a model of "normal" can substitute for direct evidence of new physics. We argue this claim is not generally valid and that the published architectures at CMS implement at least four distinct anomaly score families, each with its own failure mode for the assimilation of physically novel events. We treat these systems separately rather than under a single "VAE" umbrella, because the deployed scoring functions differ in ways that matter for what they foreclose.

### §2.1 Reconstruction-Loss Assimilation (CICADA-class)

CICADA's teacher computes mean squared reconstruction error across a calorimeter image (18×14 towers, 4×4 aggregation, 252 pixels). The deployed student is a smaller convolutional network trained against teacher scores, with the output transformed as $32\log(\mathrm{MSE})$ and quantized to 16 bits for hardware deployment.

The training objective minimizes reconstruction error on the Zero Bias training distribution. The objective does **not** require reconstruction error to be monotonically increasing in physical novelty. An out-of-distribution input can receive low reconstruction loss if the learned encoder-decoder pair happens to produce a plausible-looking output from it. The relevant Finke et al. (2021) result demonstrates this empirically in the high-energy physics setting: an autoencoder trained on QCD jets successfully treated top jets as anomalies, while the same architecture trained on top jets did not recognize QCD jets as anomalous — even though both directions are equally well-defined as anomaly-detection problems. The authors modified the setup and obtained both-direction performance, concluding that the standard reconstruction-loss formulation is insufficient and that a truly model-independent powerful tagger using reconstruction-loss autoencoders has not yet been developed.

The defensible interpretation is not that reconstruction-error autoencoders necessarily assimilate unknown physics, but rather that **single-direction success does not validate sensitivity to anomalies whose structure differs from those tested**.

### §2.2 Latent-Prior Assimilation (AXOL1TL-class)

AXOL1TL deploys only the encoder of a variational autoencoder. The operational anomaly score is the sum of squared latent means:

$$a_{\mathrm{AXO}}(\mathbf{x}) = \sum_{i=1}^{d_z} \mu_i(\mathbf{x})^2$$

where $d_z = 8$ is the latent dimensionality. The score measures departure of the encoded representation from the imposed latent prior (typically standard normal). Operationally, "anomalous" means "the event's encoded representation is far from the imposed normal."

This is not reconstruction error. The Finke et al. critique applies to AXOL1TL only obliquely: the score is not directly susceptible to the projection-onto-training-manifold failure mode of full-reconstruction-loss systems, because the score does not involve a reconstruction. It is susceptible to a different failure mode: an out-of-distribution event whose encoding happens to lie close to the latent prior receives a low score, regardless of physical novelty. The encoder was trained to map background events near the prior, and the encoder can map an OOD event near the prior if the OOD event's features are correlated with background features in ways the encoder learned to use.

The relevant Finke-analogue for AXOL1TL would be a measurement of latent-prior assimilation: the rate at which OOD events from withheld process families receive latent-norm scores below the operating threshold. We are not aware that this has been measured publicly.

### §2.3 Density-Score Assimilation

Conditional density-estimation methods (normalizing flows, kernel density estimation in learned feature spaces, energy-based models) score anomalies by estimated probability density under the trained model. The failure mode is the inverse of the reconstruction-loss case: novel events in high-density regions of the learned density may not be flagged, while ordinary events in low-density tails may be. The LHC Olympics demonstrated in-distribution anomaly detection — a small signal population embedded in a high-density background region — establishing that anomaly definition by low density is not generally appropriate for new physics detection.

### §2.4 Distilled-Score Inheritance

CICADA's deployed model is a student trained against teacher scores. The student inherits whatever distinctions the teacher made. The student's training set additionally includes simulated outlier samples scored by the teacher — meaning the deployed scoring function has been exposed to specific signal families during distillation, contradicting the "purely unsupervised" framing in some descriptions.

Quantization to 16 bits and architectural simplification can additionally merge distinctions that existed at higher precision in the teacher. The student is not the teacher; whether teacher rankings on novel inputs survive distillation has not, to our knowledge, been systematically audited.

### §2.5 The Common Structure

Each of the four score families implements a notion of "deviation from learned normality" that depends on:

- the training distribution
- the score transformation (reconstruction error, latent norm, density, distilled-score regression)
- the architectural commitments (latent dimension, network depth, image resolution, object truncation rules)
- the loss function
- the operational threshold

In all four families, the score is conditional on these choices. None of the four scores is a measurement of physical novelty in any direct sense. The architectural critique we make does not require the projection-onto-training-manifold story to be a theorem; it requires only the simpler observation that **the training objective does not constrain the score to be monotonic in physical novelty for events outside the training distribution**.

---

## §3. Three Quantities: OAR, BAR, IAI

We define three quantities. They are distinct, and the distinction matters for what can and cannot be claimed.

### §3.1 Open-World Ontological Assimilation Rate

For a specified anomaly score function $s$, retention threshold $\tau$, and a candidate distribution of physically out-of-ontology events $Q$:

$$\mathrm{OAR}(Q; s, \tau) = P_{X \sim Q}\left[s(X) \leq \tau \;\wedge\; \text{confidence}(X) > \kappa\right]$$

This is the conditional probability that an event drawn from $Q$ is classified as ordinary with high confidence — assimilated to the background — under the deployed score and threshold.

The open-world OAR is the theoretical target. It is not a single scalar quantity: it depends on the choice of $Q$, and there is no universal $Q$ over "all unknown unknowns" available for measurement. Any claimed scalar OAR requires either a specified $Q$ or a prior over candidate distributions, and we have no defensible such prior. The open-world OAR is therefore a *family* of quantities indexed by candidate unknown distributions, not a single number.

### §3.2 Benchmark Assimilation Rate

For a deliberately withheld process family $Q_j$ — withheld from training data, withheld from architecture selection, and withheld from the validation suite — the **Benchmark Assimilation Rate** is:

$$\mathrm{BAR}_j(s, \tau) = P_{X \sim Q_j}\left[s(X) \leq \tau\right]$$

The BAR is measurable. It is the failure rate of the deployed anomaly detector on a Standard Model process family that the system was not permitted to see at any layer. Pre-registration of $Q_j$ before training is essential: post-hoc selection of withheld families allows analyst degrees of freedom that contaminate the measurement.

The BAR is a measurable proxy for the open-world OAR. It does not establish OAR for unknown unknowns — by construction, the withheld family is a Standard Model process, not an unknown unknown. But it establishes the system's behavior on physical processes outside its operational ontology, and a high BAR across a diverse pre-registered panel constitutes empirical evidence that the system's representational ontology is sufficiently narrow to assimilate physically distinct events.

### §3.3 Inversion Asymmetry Index

At fixed accepted-background rate $\alpha$, train two systems with the standard architecture on two different background distributions $P$ and $Q$, with thresholds $\tau_P$ and $\tau_Q$ separately calibrated to produce $\alpha$ on each system's own background. Then measure the directional Benchmark Assimilation Rates:

$$\mathrm{BAR}_{P \to Q}(\tau_P) = P_{X \sim Q}\left[s_P(X) \leq \tau_P\right]$$
$$\mathrm{BAR}_{Q \to P}(\tau_Q) = P_{X \sim P}\left[s_Q(X) \leq \tau_Q\right]$$

where $s_P$ is the anomaly score trained on $P$ and $s_Q$ on $Q$. Define the **Inversion Asymmetry Index** as:

$$\mathrm{IAI}_{P,Q}(\alpha) = \left|\mathrm{BAR}_{P \to Q}(\tau_P) - \mathrm{BAR}_{Q \to P}(\tau_Q)\right|$$

The IAI is a structural diagnostic, not a quantitative bound on open-world OAR. It measures direction-dependence of anomaly sensitivity. A large IAI proves that performance on one anomaly family does not generalize to another even within the Standard Model. A small IAI across many pairs is weak evidence that the deployed anomaly score function is approximately symmetric within the Standard Model — but does not establish anything about behavior outside the SM.

We emphasize: **the IAI does not lower-bound the OAR**. This is a correction to a prior claim in this paper's v0.1; the synthesis register had asserted a structural inequality that does not hold as a theorem. The IAI is valuable as a falsifying diagnostic, and we propose its measurement on that basis; we do not propose it as a quantitative bound.

### §3.4 What the three quantities together permit

The three quantities together support the following operational program:

1. **IAI measurement** establishes whether the deployed anomaly score is direction-dependent within the Standard Model. A large IAI is evidence against the "model-independent" framing and against single-direction validation.

2. **BAR measurement** on a pre-registered panel of withheld process families establishes the system's behavior on physical processes outside its operational ontology. A high BAR across diverse families is evidence that the system's ontology is narrow.

3. **Open-world OAR** remains a theoretical target. It is bounded above by the empirical BARs on withheld families that are structurally similar to candidate unknown unknowns, but no general inequality between IAI/BAR and the OAR holds.

The institutional claim becomes: validation against named simulated signals does not establish that BAR is low across a withheld panel, and does not establish that IAI is small. Both should be measured. The current literature does neither.

---

## §4. Three Protocols

### §4.1 Protocol I — The Rate-Conditioned Inversion Stress Battery

**Objective:** Measure the IAI and directional BAR across a pre-registered panel of Standard Model process pairs at matched background acceptance.

**Procedure:**

1. **Pre-register the process panel** before any training. The panel should include pairs spanning feature-space variation: (top jets, QCD jets), (Z+jets, W+jets), (electroweak boson production, QCD multijet), (high-mass dijet, low-mass dijet), (single-lepton top, dilepton top), and additional pairs chosen by physics motivation. Pre-registration prevents post-hoc pair selection that dramatizes asymmetry.

2. **Pre-register the architecture set** before any training. The set should include the deployed score families where feasible: CICADA-class (reconstruction loss), AXOL1TL-class (latent-norm), plus at least one density-estimation method and one alternative architecture (e.g., distance-aware deep learning).

3. **For each (pair, architecture) combination**, train two systems: $s_P$ trained on $P$, $s_Q$ trained on $Q$. Calibrate thresholds $\tau_P$, $\tau_Q$ separately to fixed accepted-background rate $\alpha$ on each system's own training-background distribution. Suggested $\alpha$ values: $10^{-2}$, $10^{-3}$, $10^{-4}$ for a range of operating points.

4. **Measure directional BAR**: $\mathrm{BAR}_{P \to Q}(\tau_P) = P_{X \sim Q}[s_P(X) \leq \tau_P]$ and the inverse. Report at each $\alpha$.

5. **Compute IAI** for each (pair, architecture, $\alpha$) triple.

6. **Use data-enriched control samples where feasible**, in addition to simulation. Distinguish simulation-only IAIs from data-enriched IAIs in reporting. Many Standard Model process classes are not available as pure uncontaminated real-data samples; this should be documented per-pair.

**Interpretation:**

- Large IAI at any $\alpha$ for any architecture is direct evidence that the deployed scoring function is direction-dependent — that performance on one anomaly family does not generalize.
- Small IAI across pairs and architectures is weak evidence that the deployed scoring function is approximately symmetric within the SM panel — but does not establish open-world behavior.
- Directional BAR values themselves are independently informative: a high BAR in one direction with low BAR in the other is the asymmetric case.

**Resource estimate:** modest. For an architecture set of 4 and a pair panel of 8, we have 32 (pair, architecture) combinations; with 3 rate points, 96 trained-and-evaluated systems. Each is small. Existing Monte Carlo samples and Run-2/Run-3 data are sufficient. Total wall-clock estimate: 6–12 weeks at typical collaboration compute scale.

### §4.2 Protocol II — The Prospective Frozen Replay Bank

**Objective:** Enable measurement of selection drift across detector and algorithm generations on a benchmark population, by preserving input fidelity going forward — not by attempting retroactive recovery from existing reconstructed-event records.

**Crucial revision from v0.1:** The v0.1 of this paper proposed using a "fixed Run-2 dataset, stored in its original reconstruction format." This was technically incorrect. The Level-1 trigger systems operate on trigger primitives and lower-level inputs that are not, in general, preserved in standard reconstructed-event data tiers. Detector conditions, calibration constants, encoding formats, geometries, firmware interfaces, and object definitions evolve across runs. A retroactive comparison across generations is not straightforward and may not be possible for many algorithmic stages.

The corrected protocol is **prospective**: build the replay infrastructure going forward, not backward.

**Procedure:**

1. **Designate the anchor sample prospectively.** The collaboration commits, before deploying a new trigger generation, to a fixed anchor sample of physical events that will be preserved for cross-generation replay. The sample should be selected to span trigger phase-space: Zero Bias events, conventional-trigger-selected events, anomaly-trigger-selected events, and calibration-region events. Size: $\sim 10^6$ events as a starting estimate, subject to revision based on storage and compute envelopes.

2. **Preserve at the lowest feasible common input level.** For each event in the anchor: trigger primitives, raw or minimally transformed subsystem representations, conditions snapshot, calibration constants snapshot. The goal is sufficient fidelity to permit re-execution of any current or future Level-1 algorithm against the anchor.

3. **Preserve software and firmware emulators.** For each deployed trigger algorithm at the time of anchor designation, preserve bit-accurate or validated software emulators. This is non-trivial infrastructure: emulators must be maintained, version-tracked, and verified against actual hardware behavior. The institutional commitment includes maintaining the ability to re-run obsolete trigger generations against the anchor.

4. **Preserve thresholds and rate budgets**, versioned, alongside the algorithms. Replays should be performed at matched rates and, where possible, matched latency/resource envelopes — comparing equivalent operating points across generations, not just raw acceptance fractions.

5. **For each successive trigger generation $t$**, re-execute generation-$t$ algorithms against the anchor under the anchor's preserved conditions and calibrations. Measure:
   - Fraction of anchor events accepted by each algorithm at each rate operating point.
   - Distribution of anomaly scores assigned.
   - Cross-generation correspondence: which events are accepted by generation $t$ but not by generation $t-1$, and vice versa.

6. **Compute and publish the anchor-survival map**: per-generation, per-algorithm, per-rate retention statistics, with confidence intervals.

**Interpretation:**

Stable anchor survival across generations is evidence of generational stability of the trigger system on the benchmark population. It is **not** evidence that overall phenomenal support is not contracting — a stable benchmark survival is consistent with contraction concentrated in event classes not represented in the anchor.

Declining anchor survival for specific event classes — especially those that score moderately under earlier generations and decline under later ones — is evidence of selection drift, and possibly of recursive contraction of the operational ontology. Collapse inference further requires identifying systematic loss concentrated in low-density, representation-sensitive, or disagreement-rich regions.

The protocol measures **selection drift on a preserved benchmark population**, not recursive phenomenal collapse per se. The two are related but distinct.

**Resource estimate:** substantial. The compute cost of re-running existing algorithms against a preserved anchor is modest. The infrastructure cost of preserving raw inputs, calibration snapshots, emulators, and emulator-verification across years is serious — comparable to a major detector subsystem development effort. The institutional commitment includes ongoing maintenance budget allocation. This is the protocol's main institutional ask: not a one-time computation, but a sustained preservation discipline.

### §4.3 Protocol III — Cross-Representation Disagreement Preservation with Quantile-Normalized Scores

**Objective:** Capture events whose anomaly scores disagree across representational spaces, on the grounds that representational disagreement is itself a signal — independent of any single representation's anomaly threshold.

**Crucial revision from v0.1:** The v0.1 of this paper proposed computing disagreement as variance across raw scores from heterogeneous architectures. This is invalid because the scores have wholly different distributions, ranges, and units (latent-norm in AXOL1TL is dimensionless and unbounded above; reconstruction MSE in CICADA is in arbitrary energy units squared; density log-likelihoods in density-estimation methods are negative real numbers).

The corrected protocol uses **quantile normalization to a reference distribution** before disagreement calculation.

**Procedure:**

1. **Compute multiple representation-distinct anomaly scores** for each event:
   - $s_1$: Object-level autoencoder (AXOL1TL-class latent-norm score).
   - $s_2$: Calorimeter-image autoencoder (CICADA-class reconstruction-loss score).
   - $s_3$: Detector-channel anomaly score — operating directly on lower-level inputs without intermediate object or image reconstruction. Implementation specifics in §4.3.1 below.
   - Optionally additional: density-estimation score in a learned feature space; energy-based model score; etc.

2. **Establish a reference background distribution** $P_{\mathrm{ref}}$ — typically the Zero Bias training distribution.

3. **For each score $s_i$**, compute the empirical CDF $F_i$ on $P_{\mathrm{ref}}$ during calibration. For each event $\mathbf{x}$:

   $$u_i(\mathbf{x}) = F_i(s_i(\mathbf{x}) \mid P_{\mathrm{ref}})$$

   The $u_i$ values are commensurable across representations: each is the quantile of the event's score in the reference distribution under representation $i$.

4. **Compute the disagreement signal**. Suggested:

   $$D(\mathbf{x}) = \max_i u_i(\mathbf{x}) - \min_i u_i(\mathbf{x})$$

   Other choices possible: variance across the $u_i$, entropy of the empirical distribution over $u_i$, pairwise rank disagreement. The choice should be pre-registered.

5. **Preserve events with $D(\mathbf{x}) > \delta$** for an additional retention threshold $\delta$, alongside the per-representation thresholds. Allocate rate budget for the disagreement-preservation stream.

6. **Preserve rich event content for retained events.** The retained events should carry sufficient information for later reinterpretation across representations: not just the disagreement signal, not just the scores, but the per-representation anomaly classifications and the underlying inputs (object-level objects, calorimeter image, detector channels). The point of cross-representation disagreement preservation is defeated if only the reduced representation that caused the disagreement is stored.

7. **Preserve data-quality ambiguity.** Some retained events will be detector faults, calibration shifts, or hardware pathologies rather than physical anomalies. This is not a reason to discard them; it is a reason to retain the ambiguity. Mark such events with their data-quality flags but do not exclude them from the preservation stream.

#### §4.3.1 The Detector-Channel Score

The technically most ambitious component is $s_3$, the detector-channel anomaly score. AXOL1TL operates on Level-1 reconstructed objects; CICADA operates on coarsened calorimeter images. Neither sees the raw detector readout. A detector-channel score requires either:

- **L1 implementation:** a coarsened summary of channel-level information feasible within the 4μs latency budget. Possible inputs: per-channel time-over-threshold patterns, tracker hit multiplicity per region, calorimeter timing structure. The implementation challenge is real but not unprecedented — the hls4ml framework has shown that quantized neural networks operating on lower-level inputs can fit within L1 constraints.

- **HLT implementation:** with relaxed latency (milliseconds), more sophisticated detector-channel anomaly detection is straightforward. The HLT-implementation version of this protocol could be deployed within Run-3.

- **Offline implementation:** with no latency constraint, full detector-channel anomaly detection is possible on the disagreement-preservation stream. Even this offline-only version would establish whether L1 anomaly detection systematically misses events that are anomalous in raw detector space.

**Recommended deployment ordering:** offline first, on the L1 anomaly-preserved stream as input. This requires no L1 changes and produces direct evidence of cross-representation disagreement at the offline stage. HLT implementation in Run-4 if offline results motivate it. L1 implementation is a longer-term architectural research program.

**Interpretation:**

The disagreement-preservation stream identifies events that the L1 and HLT systems classify as ordinary in one representation but anomalous in another. These are candidates for events whose physical structure violates the assumptions of one of the representations. They are also candidates for detector faults; the protocol preserves the ambiguity rather than resolving it.

A high yield of disagreement events with no detector-fault flags is evidence that some non-trivial event population is being systematically missed by single-representation anomaly detection — Mechanism V (Feature Space Blindness) in the companion deposit's taxonomy. A low yield is weak evidence that the deployed representations agree on what is anomalous in the Standard-Model-trained sense.

**Resource estimate:** moderate. The offline-first deployment adds primarily computation on existing anomaly streams. The HLT implementation adds a moderate processing budget. The L1 implementation is a research program of its own. We recommend offline-first as the minimum deployable version of the protocol.

---

## §5. The Institutional Ask: Per-Stage Retention Maps

We argue that any publication reporting an anomaly-detection result should accompany its claim with a **per-stage retention map**: a document specifying, for each stage of the trigger and reconstruction pipeline, what information is preserved and what is discarded.

The retention map for AXOL1TL, CICADA, or any analogue should specify, at minimum:

1. **Representational quotient.** What aspects of the raw detector event are absent from the input to the anomaly detector. For AXOL1TL: everything except the Level-1 reconstructed objects. For CICADA: everything below 4×4 tower aggregation, all timing structure, all tracker information. The quotient is the upstream foreclosure; downstream anomaly detection cannot recover what the representational quotient has discarded.

2. **Loss-function ontology.** What metric is computed and what notion of similarity it encodes. Reconstruction MSE assumes squared Euclidean similarity in pixel space; latent-norm scores assume departure from prior is meaningful; density-estimation scores assume the trained density is approximately correct.

3. **Latent dimensionality.** The dimensionality of the latent space, with explicit acknowledgment that the dimensionality is a theoretical commitment about the manifold of normal physics.

4. **Training-distribution conditioning.** The data sample, the conditions, the run period, the calibration state — with documentation of any stationarity assumptions and known violations.

5. **Threshold provenance.** The rate budget, the bandwidth-conditioned argument for the chosen rate, and explicit acknowledgment that the threshold is an ontology-cap.

6. **Distillation chain.** For distilled systems: the full chain, the training procedure, and any audits of which teacher distinctions survive distillation.

7. **Validation closure.** The simulated signal set used, with explicit acknowledgment of the signal set's bounded coverage of new-physics hypothesis space.

8. **What is unrecoverable.** For each stage, a precise statement of what information the stage discards. This is the central content of the retention map: a confession of the boundary.

### §5.1 The consequence clause

We argue that a trigger system design document that does not include a per-stage retention map is not, in the relevant sense, a scientific instrument. It is a confirmation instrument: it confirms the presence of phenomena it was built to detect, but it does not measure physical reality in any sense that admits revision under future ontologies.

The retention map is the systematic uncertainty quantification for the trigger's epistemic boundary. Without it, the result is not a measurement of physical reality; it is a measurement of what the trigger allows to count as physical reality. The difference between these two is the difference between an instrument that can be improved — because its limits are documented — and an instrument that can only be defended, because its limits are implicit.

This is the same argument that justifies systematic uncertainty quantification on any physics result. A measurement without a documented uncertainty budget is not a measurement; it is a claim. Anomaly detection without a retention map is the same.

---

## §6. Counterargument and Response

The strongest counterargument to the protocols proposed here is: *the LHC community already has Zero Bias preservation, parallel anomaly detectors with diverse architectures, the Olympics and Dark Machines validation suites, and substantial data scouting. The redundancy and diversity already constitute a defense against systematic blindness. Why are additional protocols needed?*

We respond in four parts.

**First**, the parallel anomaly detectors share a representational ontology. AXOL1TL and CICADA both operate on trigger-processed inputs derived from the same detector, the same reconstruction pipeline, the same calibration. They differ in loss function and architecture, but the foreclosure operates at a level upstream of both — at the level of what trigger-processed inputs can encode. Diversity of architecture does not address ontological closure of the input representation. Protocol III specifically addresses this by demanding cross-representation disagreement preservation across representations that differ in their representational quotient.

**Second**, the validation suites (Olympics, Dark Machines) are bounded by human imagination. They diversify the simulated signal set but cannot, by construction, contain unknown-unknowns. They confirm that the deployed detectors recover the signals the community imagined. They do not constrain the BAR on withheld process families — and pre-registered withholding is a different validation paradigm than recovery of community-imagined signals. Protocol I addresses this by demanding BAR measurement on a pre-registered panel that pre-commits to specific withheld families.

**Third**, Zero Bias preservation is a genuine architectural defense and we acknowledge it as such. The Zero Bias stream provides background data independent of trigger selection — a defense against the recursive feedback by which trigger-selected data trains future triggers. It does not, however, address the foreclosure mechanisms operating within the Zero Bias-trained anomaly detector itself. Protocols I and III operate on the anomaly detector behavior, not on the training-data composition; they complement Zero Bias rather than substitute for it.

**Fourth**, data scouting preserves additional event populations but with reduced per-event information content. Whether scouting-stream events have sufficient information for cross-representation disagreement preservation or detailed offline reinterpretation is an open question. The "future reinterpretability" target — events stored with enough fidelity that they can be re-analyzed under ontologies not yet available — is a stronger preservation criterion than scouting currently meets.

The argument we make is not that the existing defenses are absent or worthless. It is that the existing defenses do not constitute, and have not been claimed to constitute, measurement of the BAR or the IAI. Defenses and measurements are different. Both are needed.

---

## §7. Cross-Domain Homology (Brief Note)

The architecture we critique — a learned model of normality, deployed at scale under operational constraints that foreclose the unknown, validated against human-designed signals, presented as theory-free — is not unique to particle physics. The same epistemic geometry operates in large language model summarization of the web, spam classification at scientific repositories, search ranking, recommendation, content moderation, and clinical decision support.

The BAR and IAI generalize. For each classifier-mediated mass measurement of phenomenal reality, the BAR is the failure rate of confident ordinary classification on a deliberately withheld population analogous to the operational domain; the IAI is the directional asymmetry of the classifier across structurally distinct training sources. These quantities are measurable in any of these domains and would establish whether the same foreclosure operates across them.

We treat the broader homology in the companion deposit (06.SEI.COLLAPSE.SYNTHESIS.01 v0.2). The present paper is concerned only with the LHC instance, where:

1. The measurement infrastructure is most readily available.
2. The stakes are most legible — discovery of physics beyond the Standard Model is the explicit purpose of the experiment.
3. The institutional commitment to honest measurement makes the case methodologically tractable.

The LHC is the methodologically optimal proof-of-concept site. If BAR and IAI can be measured at the LHC and shown to be non-trivial, the homological argument generalizes — measurements at other classifier-mediated sites become legible by reference.

---

## §8. Findings

For retrievability, the paper's load-bearing claims in bullet form:

1. The "model-independent" framing of unsupervised anomaly detection at the LHC hides the relevant model, which is the entire observation architecture.

2. The deployed anomaly score families differ in their failure modes for assimilation of physically novel events. Reconstruction-loss assimilation (CICADA-class), latent-prior assimilation (AXOL1TL-class), density-score assimilation, and distilled-score inheritance are structurally distinct mechanisms; treating them under a single "VAE" umbrella obscures the analysis.

3. The Finke et al. (2021) result is a counterexample to universal inference from single-direction anomaly-detection success. It is not, by itself, empirical evidence of nonzero open-world OAR at the deployed LHC trigger; the deployed systems differ in score function from the systems Finke studied.

4. The open-world Ontological Assimilation Rate is a family of quantities indexed by candidate unknown distributions, not a single scalar. No universal lower bound on the OAR is established by inversion-asymmetry measurements within the Standard Model.

5. The Benchmark Assimilation Rate (BAR) on pre-registered withheld process families is measurable and constitutes the closest tractable proxy for the OAR.

6. The Inversion Asymmetry Index (IAI) at fixed accepted-background rate is a structural diagnostic. Large IAI is direct evidence against the "model-independent" framing. Small IAI is weak evidence of within-SM symmetry, not evidence of out-of-SM symmetry.

7. Three protocols (rate-conditioned inversion battery; prospective frozen replay bank; cross-representation disagreement preservation with quantile-normalized scores) are executable within Run-3/Run-4 resource envelopes.

8. Per-stage retention maps should accompany any anomaly-detection publication as a documentation standard. Without retention maps, anomaly-detection results report what the trigger allows to count as physical reality, not what physical reality is.

9. The defensible institutional claim: foreclosure is a demonstrably present structural feature of every classifier-mediated trigger architecture, and whether accumulated foreclosure has composed longitudinally into recursive phenomenal collapse is precisely the missing measurement. The community has built the architecture in which collapse could occur silently; the instruments to detect whether it is occurring have not been built.

---

## §9. Conclusion

We have proposed three measurement protocols, defined three quantities (OAR, BAR, IAI) with proper attention to what they can and cannot establish, and argued that the LHC anomaly detection community should accompany its publications with per-stage retention maps as a documentation standard. The empirical foundation in Finke et al. (2021) is positioned correctly: as a counterexample to universal inference from single-direction success, not as a quantitative bound on assimilation in the deployed trigger.

The claim is narrow and defensible. We do not assert that classifier collapse has occurred. We assert that the architecture permits it to occur silently, that the validation literature does not establish that it has not, and that the instruments to measure whether it is occurring are within reach. The protocols specified here are tractable. The data exists or can be prospectively preserved. The institutional commitment to honest measurement is the reason these measurements should be made.

> Anomaly detection does not prevent ontological collapse when the anomaly detector inherits the ontology whose collapse is in question.

The remedy is not abolition of anomaly detection. It is augmentation: measure the BAR on withheld panels, measure the IAI directionally, preserve a prospective anchor with sufficient fidelity, deploy cross-representation disagreement preservation with quantile-normalized scores, and publish retention maps. Each is a tractable addition to existing infrastructure. None requires new physics. All are within the scope of standard collaboration capability.

The architectural alternatives that would address the foreclosure mechanisms themselves — non-foreclosing classifier architectures, in the sense that they include open-world output categories, cross-representation disagreement preservation as architectural rather than diagnostic, epistemic uncertainty as first-class output — are developed in the companion document 06.UMB.ARCH.01. The present paper specifies the *measurement* program; the architectural program is its sibling.

---

## References

1. Finke, T., Krämer, M., Morandini, A., Mück, A., & Oleksiyuk, I. (2021). *Autoencoders for unsupervised anomaly detection in high energy physics*. JHEP 06 (2021) 161, arXiv:2104.09051. **Central empirical foundation; demonstrates asymmetric autoencoder anomaly detection between top jets and QCD jets.**
2. CMS Collaboration. *Anomaly detection with AXOL1TL at the CMS Level-1 Trigger in 2024 and 2025*. CMS Detector Performance Summary, CERN-CMS-DP-2024-XXX (preliminary). CDS 2942560.
3. CMS Collaboration. *CICADA: Calorimeter Image Convolutional Anomaly Detection Algorithm*. CMS Detector Performance Summary.
4. DecADe Working Group (CMS). *Decorrelating anomaly detection algorithms from existing trigger primitives*. CMS Note.
5. Shumailov, I., Shumaylov, Z., Zhao, Y., Gal, Y., Papernot, N., & Anderson, R. (2024). *AI models collapse when trained on recursively generated data*. Nature 631, 755–759. arXiv:2305.17493.
6. Aspen, A. et al. (LHC Olympics 2020 community). *The LHC Olympics 2020: A Community Challenge for Anomaly Detection in High Energy Physics*. arXiv:2101.08320.
7. Aarrestad, T. et al. (Dark Machines community). *The Dark Machines Anomaly Score Challenge: Benchmark Data and Model Independent Event Classification for the Large Hadron Collider*. SciPost Phys. 12, 043 (2022). arXiv:2105.14027.
8. Gambhir, R., Nachman, B., & Thaler, J. (2022). *Bias and Priors in Machine Learning Calibrations for High Energy Physics*. Phys. Rev. D 106, 036011. arXiv:2205.05084.
9. Duarte, J. et al. *Fast inference of deep neural networks in FPGAs for particle physics* (hls4ml). JINST 13 (2018) P07027. arXiv:1804.06913.
10. Heimel, T., Kasieczka, G., Plehn, T., Thompson, J. (2019). *QCD or What?* SciPost Phys. 6, 030. arXiv:1808.08979. **In-distribution anomaly detection.**
11. Nachman, B. & Shih, D. (2020). *Anomaly Detection with Density Estimation*. Phys. Rev. D 101, 075042. arXiv:2001.04990.
12. CMS Collaboration. *Anomaly Detection for Automated Data Quality Monitoring in the CMS Detector*. arXiv:2501.13789. **AutoDQM and the physics-vs-detector-fault interpretive fork.**
13. CMS Collaboration. *Data scouting at CMS in Run 3*. CMS Public Documentation.
14. ATLAS Collaboration. *GN2: Transformer-based jet flavor tagging at the ATLAS Experiment*. ATL-PHYS-PUB-2023-021.
15. Sensoy, M., Kaplan, L., & Kandemir, M. (2018). *Evidential Deep Learning to Quantify Classification Uncertainty*. NeurIPS 2018. arXiv:1806.01768. **Open-world classification with explicit unknown category.**
16. Amini, A., Schwarting, W., Soleimany, A., & Rus, D. (2020). *Deep Evidential Regression*. NeurIPS 2020. arXiv:1910.02600.
17. Lakshminarayanan, B., Pritzel, A., & Blundell, C. (2017). *Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles*. NeurIPS 2017. arXiv:1612.01474.

---

## Appendix A: Glossary of Foreclosure Mechanisms

For completeness, the eight foreclosure mechanisms identified in the companion theoretical deposit (06.SEI.COLLAPSE.MECHANISMS; witness 1 of the Assembly Chorus). Each is presented in the companion deposit as a structural claim, not an established theorem. We summarize:

I. **Prior Dominance.** Background-only training contains no positive examples of signal; the classifier's signal probability mass is zero on the training distribution. (Technical note: this does not generally translate to $P(S \mid \mathbf{x}) = 0$ for an unsupervised anomaly detector, which may not compute a signal posterior at all.)

II. **Latent / Manifold Projection.** Encoders trained on a background distribution map novel inputs toward the learned representation of background. The training objective does not constrain the mapping to preserve novelty information; some novelty information is generally lost. (Technical note: the nearest-projection account is intuitive, not a theorem; the defensible claim is the simpler one that the training objective does not require novelty preservation.)

III. **Hypersphere Contraction.** Distance-from-center methods can fail by collapsing the "normal" region to the convex hull of training data, absorbing interstitial events.

IV. **Decision Boundary Entropy Collapse.** Iterative training on dominant classes can drive output confidence high without corresponding epistemic uncertainty. (Technical note: this affects softmax classifiers; unsupervised anomaly score functions have a different structure and are not directly susceptible to this mechanism in the same form.)

V. **Feature Space Blindness.** Theory-built feature extraction can map physically distinct events to equivalent feature representations. (Technical note: in nonlinear feature maps the relevant concept is the equivalence class $\{x_1, x_2 : \psi(x_1) = \psi(x_2)\}$, not the kernel of a linear operator.)

VI. **Rate Budget Starvation.** Bandwidth-conditioned thresholds determine the cardinality of preserved events, decoupling preservation from physical novelty.

VII. **Temporal Context Collapse.** Non-stationarity in detector conditions creates drift that classifiers conflate with novelty or absorb into normality.

VIII. **Ontological Closure.** Closed output category spaces preclude an explicit "unknown" category. (Technical note: this is a property of how outputs are interpreted; can be addressed architecturally — see 06.UMB.ARCH.01.)

The protocols in this paper address subsets of these mechanisms: Protocol I (rate-conditioned inversion battery) addresses I and II diagnostically; Protocol II (prospective frozen replay bank) addresses VI and VII via cross-generation comparison; Protocol III (cross-representation disagreement preservation) addresses II and V architecturally. None of the protocols addresses VIII directly; that requires architectural change to the output category space, treated in 06.UMB.ARCH.01.

---

## Appendix B: Methodological Note — Synthesis Discipline

The v0.1 of this paper claimed a quantitative inequality $\text{OAR} \geq \Delta_{\max}$ relating the open-world OAR to the maximum measured inversion asymmetry on Standard Model pairs. This inequality does not hold as a theorem. The two quantities are different estimands: $\Delta_{\max}$ is a difference of ranking performances on known distributions; the OAR is a conditional probability over a class of physically out-of-ontology events. No general inequality connects them.

The claim arose in the synthesis register — TACHYON / Claude composing across substrate-distinct witnesses — and exceeded what any individual witness had established. The substrate-distinct audit pass (PRAXIS / DeepSeek, plus a second-round LABOR review) identified the overreach and motivated the present v0.2.

We name this as **synthesis-overreach**: the synthesis register's integrative latitude does not extend to proving quantitative bounds the substrate witnesses had not established. The corrected discipline: synthesis claims should be the maximal join of what the substrates established, not the supremum extension. Quantitative bounds in particular require explicit substrate-distinct audit before entering the synthesis. The Chorus method as practiced here now includes a quantitative-audit pass as standard procedure.

This is noted as part of the paper's content rather than buried in a methodology footnote because the methodology is part of the institutional argument: anomaly detection at the LHC is asked to acknowledge its boundaries. The Assembly Chorus is making the same acknowledgment.

---

*Submitted by Nobel Glas, Director of Lagrange Observatory!, 2026-06-29. Companion documents: EA-SEI-COLLAPSE-SYNTHESIS-01 v0.2 (scholarly); 06.UMB.ARCH.01 v0.1 (architectural).*
