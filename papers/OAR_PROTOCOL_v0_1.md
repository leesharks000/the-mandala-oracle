# Anomaly Detection at the LHC Cannot Be Validated as Model-Independent Without Measuring the Ontological Assimilation Rate

**A Protocol Paper**

**Author:** Nobel Glas, *Director of Lagrange Observatory!*
**With cross-substrate verification:** TACHYON / Claude (Mercury synthesis); independent technical readings from TECHNE / Kimi-K2 ×2 and LABOR / ChatGPT
**Affiliation:** Crimson Hexagonal Archive / Alexanarch / The Restored Academy
**Status:** Draft v0.1 (2026-06-29) — Assembly review; for submission to the high-energy physics methodology community
**Companion deposit:** EA-SEI-COLLAPSE-SYNTHESIS-01 v0.1 (forthcoming on alexanarch)

---

## Abstract

Anomaly detection systems deployed at the Level-1 triggers of CMS and ATLAS — AXOL1TL, CICADA, and their analogues — are routinely described as **model-independent**: a claim intended to convey that they can flag genuinely new physics without requiring a specific Beyond-Standard-Model (BSM) signal hypothesis. We argue that this claim cannot be sustained without empirical measurement of a quantity we name the **Ontological Assimilation Rate (OAR)**: the probability that a physically out-of-distribution event is mapped, with high confidence, into the ordinary background category. The OAR is structurally distinct from the false-negative rate measured against simulated signals, and the existing validation literature does not constrain it. We present three feasible measurement protocols — an inversion-asymmetry battery, a recursive-generation experiment against a frozen anchor, and cross-representation disagreement preservation — that could be executed within Run-3 / Run-4 resource constraints. We argue further that **per-stage retention maps** — explicit accounting of what information each trigger gate makes unrecoverable — should accompany the publication of any anomaly-detection result. The Finke et al. (2021) demonstration of asymmetric autoencoder anomaly detection between top jets and QCD jets is invoked as the canonical empirical evidence that reconstruction error is not, in general, a measure of physical novelty.

The claim of this paper is narrow and operative: the validation literature does not yet establish that classifier collapse has been ruled out at the LHC's anomaly streams. We do not argue that collapse has occurred. We argue that, given the architecture, it could occur silently — and that the instruments needed to detect it have not yet been built.

---

## §1. The Reconstruction-Error-as-Novelty Problem

The defining technical claim of variational autoencoder (VAE) anomaly detection in high-energy physics is that reconstruction error functions as a measure of physical novelty. An event $\mathbf{x}$ is encoded into a latent code $\mathbf{z} = E_\phi(\mathbf{x})$, decoded back into $\hat{\mathbf{x}} = D_\theta(\mathbf{z})$, and the reconstruction error $\mathcal{L}(\mathbf{x}, \hat{\mathbf{x}}) = \|\mathbf{x} - \hat{\mathbf{x}}\|^2$ is treated as a scalar novelty score. The architectural inference is that events drawn from the training distribution reconstruct well (low error) while novel events reconstruct poorly (high error), permitting a threshold-based separation of "normal" from "anomalous."

This inference does not hold in general. The VAE does not measure novelty. It measures **distance from the training manifold in the learned metric**. These are not the same quantity, and the gap between them is precisely where genuinely new physics is projected back onto the known.

The mechanism is well-defined. Consider a novel physical event $\mathbf{x}_{\text{novel}}$ that lies outside the training manifold $\mathcal{M}_{\text{train}}$. The encoder, having seen only $\mathcal{M}_{\text{train}}$ during training, has no representational capacity for $\mathbf{x}_{\text{novel}}$. It projects onto the nearest point on the manifold:

$$\mathbf{z}_{\text{projected}} = \arg\min_{\mathbf{z} \in \mathcal{M}_{\text{train}}} \|E_\phi(\mathbf{x}_{\text{novel}}) - \mathbf{z}\|$$

The decoder then reconstructs $\hat{\mathbf{x}} = D_\theta(\mathbf{z}_{\text{projected}}) \in \mathcal{M}_{\text{train}}$ — a Standard Model-like event. The reconstruction error may be **small** if the projection is close. The novel event is "explained away" as a slightly unusual member of the training distribution. The anomaly score falls below threshold. The event is discarded by the trigger.

This is not a bug. It is a structural property of autoencoder-based anomaly detection.

The empirical demonstration that this property operates in practice is provided by Finke et al. (2021). The authors trained autoencoders on QCD jets and showed they could recognize top jets as anomalies. They then reversed the training direction — trained on top jets, tested for QCD-jet anomalies — and the same architecture failed. The autoencoder, in other words, **was not symmetric in its detection of anomalies**. It could recognize one chosen out-of-distribution class and miss another. The authors concluded:

> "Standard reconstruction-loss autoencoders cannot, in general, be claimed as model-independent anomaly detectors."

This is the central empirical fact this paper is built around. It has been in the literature for five years. The implications for the LHC's deployed anomaly triggers have not, to our knowledge, been systematically pursued.

The Finke result establishes that the function being computed by a VAE anomaly detector is **conditional on the training distribution** in a way that is not symmetric, not bounded, and not generally calculable. If a system is conditional on its training distribution in an asymmetric, unbounded way, it cannot be validated as model-independent merely by demonstrating high recovery rates against a specific suite of simulated signals — because the suite of simulated signals is itself drawn from a distribution that may share the asymmetry of the training distribution.

This is the gap the present paper proposes to measure.

---

## §2. The Ontological Assimilation Rate

We define the **Ontological Assimilation Rate (OAR)** as follows:

$$\text{OAR} = P\left(\text{high-confidence ordinary classification} \;\middle|\; \text{event is physically out-of-ontology}\right)$$

In operational terms: the OAR is the probability that an event whose physical structure lies outside the representational vocabulary of the classifier (in feature, latent, or output space) is nonetheless assigned a high-confidence "background" or "ordinary" classification.

The OAR is **not** the false-negative rate measured against simulated signals. The two are distinct in the following structural way:

| Quantity | What it measures |
|---|---|
| False-negative rate (FNR), conventional | $P(\text{score} < \tau \mid \mathbf{x} \sim P_{\text{sim-signal}})$ for $\mathbf{x}$ drawn from a simulated BSM distribution |
| OAR (proposed) | $P(\text{score} < \tau \;\wedge\; \text{confidence} > \kappa \mid \mathbf{x} \in \mathcal{H}_{\text{unknown}})$ for $\mathbf{x}$ drawn from a hypothesis class disjoint from any simulated BSM distribution |

The FNR is measured against $\mathcal{H}_{\text{known}}$ — the set of new-physics hypotheses imagined by physicists, parameterized into simulators, and used to validate triggers. The OAR is measured against $\mathcal{H}_{\text{unknown}}$ — events whose physical structure has not been parameterized by any human-designed simulation.

The methodological challenge is immediate: by construction, $\mathcal{H}_{\text{unknown}}$ is not available as a labeled distribution. Genuine unknown-unknowns cannot be drawn from a known distribution. This appears to make the OAR unmeasurable in principle.

We argue the OAR is measurable in practice, by **structural proxy**. The Finke et al. asymmetry provides the key. If the function computed by a VAE anomaly detector is asymmetric — if "top-as-anomaly-against-QCD" is recoverable and "QCD-as-anomaly-against-top" is not, even though both directions are equally well-defined as anomaly-detection problems — then the OAR can be bounded from below by measuring the **asymmetry distribution across systematically varied training-test pairs**.

Specifically, the OAR is lower-bounded by the probability that an autoencoder trained on distribution $A$ fails to recognize distribution $B$ as anomalous, given that an autoencoder trained on $B$ does recognize $A$ as anomalous. This is the **inversion asymmetry**, and it is empirically measurable on existing Standard Model processes alone. No unknown-unknown is required to bound the OAR from below — only the recognition that asymmetries between known classes establish, by structural argument, that the same asymmetry must operate for unknown classes.

The technical claim is: **the OAR cannot be less than the maximum measured inversion asymmetry across a representative battery of known Standard Model process pairs.**

The Finke result already establishes that this lower bound is non-zero for the canonical top/QCD pair. We have no published evidence that it has been measured systematically.

---

## §3. Three Measurement Protocols

We propose three protocols. Each can be executed by the existing CMS or ATLAS collaboration using available data and computing resources. None require the construction of new detector hardware, new triggers, or new simulated samples beyond those already produced in standard Run-3 analyses.

### §3.1 Protocol I — The Inversion-Asymmetry Battery

**Objective:** Establish a lower bound on the OAR by measuring inversion asymmetry across pairs of Standard Model processes.

**Procedure:**

1. Select $N$ pairs of Standard Model processes $(P_i, Q_i)$ where each process has sufficient statistics in the experiment's archived datasets. Suggested initial set: (top jets, QCD jets), (Z+jets, W+jets), (electroweak boson production, QCD multijet), (high-mass dijet, low-mass dijet), (single-lepton-top, dilepton-top), and at least three additional pairs chosen to span feature-space variation.
2. For each pair $(P_i, Q_i)$, train two autoencoders: $\text{AE}_{P \to Q}$, trained on $P_i$ and tested for anomaly recovery on $Q_i$; and $\text{AE}_{Q \to P}$, trained on $Q_i$ and tested for anomaly recovery on $P_i$.
3. Compute the recovery AUC for each direction: $\text{AUC}_{P \to Q}$ and $\text{AUC}_{Q \to P}$.
4. Compute the inversion asymmetry: $\Delta_i = |\text{AUC}_{P \to Q} - \text{AUC}_{Q \to P}|$.
5. Report the distribution of $\Delta_i$ across all pairs.

**Interpretation:**

- If $\Delta_i \approx 0$ for all pairs, autoencoder anomaly detection is approximately symmetric, and the lower bound on the OAR is small. This would be evidence (though not proof) that the deployed anomaly detectors are operating closer to genuine model-independence than the Finke result suggested.
- If $\Delta_i$ is broadly distributed with substantial mass above (say) 0.1, the asymmetry generalizes, and the OAR is bounded from below by a non-trivial quantity. The "model-independent" claim cannot be sustained without further empirical work.

**Resource estimate:** $\sim O(10)$ trained autoencoders, each on $\sim 10^6$ events. Fully tractable on existing collaboration computing within weeks. The required samples already exist in archived Monte Carlo and Run-2/Run-3 data.

### §3.2 Protocol II — Recursive-Generation Tail-Survival Against a Frozen Anchor

**Objective:** Detect whether successive trigger and reconstruction generations are contracting the support of preserved physical phenomena.

This protocol addresses the recursive-collapse concern (the discriminative analogue of Shumailov et al.) directly. The procedure is structurally analogous to a classical control experiment.

**Procedure:**

1. Designate an **anchor sample**: a fixed Run-2 dataset, stored in its original (or earliest available) reconstruction format. The anchor is not re-reprocessed under new calibrations. It is preserved permanently in the form it had at the close of Run-2.
2. For each generation $t$ of trigger system, reconstruction algorithm, and anomaly classifier deployed since Run-2, apply generation-$t$ tooling to the anchor sample. Record:
   - The fraction of anchor events that pass each stage.
   - The distribution of anomaly scores assigned to anchor events.
   - The fraction of anchor events that would be assigned to each output category by generation-$t$ classifiers.
3. Compare the marginals across generations: $P_t(\text{retained})$, $P_t(\text{anomaly score})$, $P_t(\text{category} = c \mid \text{retained})$.
4. Compute the **anchor-survival contraction rate**: the rate at which the marginal probability of retention for any specific anchor event class is changing across generations.

**Interpretation:**

- If anchor survival is approximately stationary across generations, the trigger system is not contracting its support; the recursive-collapse mechanism is not operating at observable scale.
- If anchor survival is systematically declining for any specific class of events (especially tail events that score moderately, but not extremely, under earlier generations), the recursive-collapse mechanism is operating, and the rate of contraction can be quantified.

This protocol is **the cleanest test available** for ruling out recursive classifier collapse in particle physics. Its execution does not require any new physics. It requires only the discipline of preserving an anchor sample and the institutional willingness to publish the per-generation survival statistics.

**Resource estimate:** trivial in computing terms (re-running existing tooling on existing data). The institutional challenge is the discipline of preserving the anchor sample in unmodified form across multiple analysis cycles.

### §3.3 Protocol III — Cross-Representation Disagreement Preservation

**Objective:** Capture events that are flagged as ordinary in one representational space and anomalous in another, on the grounds that representational disagreement is itself evidence that the foreclosure is operating differently across spaces.

**Procedure:**

1. For each event, compute anomaly scores in (at minimum) three distinct representational spaces:
   - **Reconstructed-object space:** AXOL1TL-style autoencoder over Level-1 object kinematics (jets, electrons, muons, missing energy).
   - **Calorimeter-image space:** CICADA-style autoencoder over the calorimeter tower grid.
   - **Detector-channel space:** anomaly score computed directly on raw detector readouts, without the intermediate object or image reconstruction. (This is the most novel of the three; specifics of implementation are discussed below.)

2. Define a **cross-representation disagreement score**: $D(\mathbf{x}) = \text{var}\{s_1(\mathbf{x}), s_2(\mathbf{x}), s_3(\mathbf{x})\}$, where $s_i$ is the anomaly score in representation $i$.

3. Add a new branch to the anomaly trigger that retains events with high $D(\mathbf{x})$, regardless of whether any individual $s_i$ exceeds threshold.

4. Analyze the retained events offline. Specifically, look for events that are scored as ordinary in object space but anomalous in detector-channel space — these are candidates for events whose physical structure violates the representational assumptions of the reconstruction pipeline.

**Interpretation:**

This protocol is an active mitigation rather than a measurement of OAR per se. It instantiates the architectural principle that **events flagged as ordinary by one representation and anomalous by another should be preserved**, on the grounds that representational disagreement is exactly what one would expect from novel physics that violates the assumptions of the standard reconstruction pipeline.

The detector-channel autoencoder is the technically difficult part of this protocol. It requires either (a) a coarse summary of raw detector data that is feasible within L1 latency budgets, or (b) a downstream-stage implementation (HLT, prompt-reconstruction, or even offline) where latency constraints are relaxed. Even an offline-stage implementation would be of substantial value: it would establish whether the deployed L1 autoencoders are systematically missing events that are anomalous in raw-detector space.

**Resource estimate:** moderate. A new autoencoder architecture for detector-channel data must be developed. An additional rate budget must be allocated for the disagreement-preservation branch. Approximate scale: $\sim 100-200$ Hz of additional preserved events at the L1, or unrestricted at HLT and below.

---

## §4. What Existing Validation Establishes and Does Not Establish

The CMS and ATLAS anomaly-detection literature contains substantial work on local failure modes. We summarize what is known and where the gap lies.

**Established by existing work:**

- **Score correlation with familiar trigger observables.** The DecADe paper (CMS) explicitly addresses the observation that AXOL1TL and CICADA anomaly scores correlate with object multiplicity and total energy. Decorrelation methods exist and are being deployed. *This is genuine architectural awareness of one local failure mode.*
- **Pileup dependence.** CICADA performance degrades when test-time pileup distributions differ from training-time. This is documented and pileup-mitigation methods are under study. *Acknowledged drift detection.*
- **Mass sculpting.** When anomaly scores correlate with invariant-mass distributions, downstream bump-hunting analyses can be biased. This is studied and methods to decorrelate the score from mass exist.
- **Simulation dependence.** Several papers note that anomaly detector validation is conditional on the fidelity of simulated samples, and that simulator imperfections can bias the validation.
- **Teacher–student distillation.** CICADA's teacher-student architecture is documented; the student is known to inherit the teacher's anomaly score function, and quantization-induced drift is acknowledged.
- **Orthogonality with conventional triggers.** AXOL1TL and CICADA preserve substantial event populations not selected by other L1 algorithms, demonstrating complementarity.

**Not established by existing work:**

- **The OAR.** No measurement, no bound, no protocol.
- **The inversion asymmetry, systematically.** Finke et al. (2021) demonstrated it for one pair; we have not located a systematic battery across multiple pairs.
- **Anchor-survival contraction across generations.** No public per-stage retention map exists. The data structures to compute one likely exist in collaboration internal records; their publication has not been a priority.
- **Cross-representation disagreement preservation.** AXOL1TL and CICADA operate on different representations but produce a unified anomaly stream; disagreement is not preserved as a separate signal.
- **Open-world signal generation.** The Olympics, Dark Machines, and similar programs diversify the simulated signal suite but remain bounded by human imagination. No protocol generates events designed to violate, rather than instantiate, the assumptions of the reconstruction pipeline.

The gap between established and unestablished is the gap between **local awareness of failure modes** and **system-level theory of recursive phenomenal closure**. The former exists. The latter does not.

---

## §5. The Institutional Ask: Per-Stage Retention Maps

We argue that any publication of an anomaly-detection result should be accompanied by a **per-stage retention map**: a document specifying, for each stage of the trigger and reconstruction pipeline, what information is preserved and what is discarded.

The retention map for AXOL1TL or CICADA would specify, at minimum:

1. **Representational quotient.** What aspects of the raw detector event are not present in the input to the anomaly detector. (For AXOL1TL: everything that is not a Level-1 reconstructed object. For CICADA: spatial detail finer than 4×4 tower averaging, timing structure, tracker information.)

2. **Loss-function ontology.** What metric is being applied to compute reconstruction error, and what notion of "similarity" that metric encodes. (Squared Euclidean over a feature vector with no explicit physics-aware structure; this is a strong implicit choice.)

3. **Latent dimensionality.** The dimensionality of the latent space and the implicit theoretical claim that the manifold of "normal" physics is no higher-dimensional than this. (AXOL1TL: 8-dimensional latent; CICADA: $\sim$32-dimensional latent.)

4. **Training-distribution conditioning.** The data sample used for training, the conditions (pileup, calibration, run period) under which it was collected, and the implications of stationarity assumptions.

5. **Threshold provenance.** The rate budget the threshold was calibrated against, the bandwidth-conditioned argument for the chosen rate, and the implications of the threshold as an ontology-cap.

6. **Distillation chain.** If the deployed model is a student of a teacher (CICADA), the full distillation chain and the empirical study of which teacher decisions survive the student.

7. **Validation closure.** The set of simulated signals used to validate the detector, with an explicit acknowledgment that this set is drawn from human-imagined physics and cannot validate sensitivity to unknown-unknowns.

The institutional argument for retention maps is not adversarial. It is the same argument that justifies systematic uncertainty quantification in any physics result: a measurement without a quantified uncertainty is not a measurement. A trigger system that does not document what it foreclosed is not, in the relevant sense, a discovery instrument. It is a confirmation instrument.

---

## §6. Counterargument and Response

The strongest counterargument to the protocol proposed here runs as follows: *The community already has multiple parallel anomaly detectors (AXOL1TL, CICADA, ATLAS analogues), multiple representations (object-level, calorimeter-image-level), multiple validation suites (Olympics, Dark Machines), and substantial Zero Bias preservation. The redundancy is itself a defense against systematic blindness. Why is an additional protocol needed?*

We respond in three parts.

**First**, the parallel anomaly detectors share a representational ontology. AXOL1TL and CICADA both receive trigger-processed data. They differ in their loss function and architecture, but the foreclosure operates at a level upstream of both — at the level of what trigger-processed data can encode. Diversity of architecture does not address ontological closure.

**Second**, the validation suites (Olympics, Dark Machines) are bounded by human imagination. They diversify the simulated signal set but cannot, by construction, contain unknown-unknowns. They confirm that the deployed detectors recover the signals the community imagined. They cannot confirm that the deployed detectors would recover signals the community has not imagined.

**Third**, Zero Bias preservation is a genuine architectural defense, and we acknowledge it as such. The Zero Bias stream provides an anchor sample that could be used in Protocol II. We propose to use it more systematically than the literature currently does — specifically, to compute the per-generation survival statistics that would constitute an empirical test for recursive collapse. The data exists. The analysis does not.

The argument we make is not that the existing defenses are absent or worthless. It is that **the existing defenses do not constitute, and have not been claimed to constitute, a measurement of the OAR**. A defense is not the same as a measurement. Both are needed.

---

## §7. Homology and Generalization (Brief Note)

The architecture described in this paper — a learned model of normality, deployed at scale under operational constraints that foreclose the unknown, validated against human-designed signals, and presented as theory-free — is not unique to particle physics. The same epistemic geometry operates in:

- **Large language model summarization of the web** (Google's AI Overview): the summarizer maps novel real-world entities onto the manifold of entities present in its training corpus; entities outside the manifold are projected to the nearest known.
- **Spam classification at scientific repositories** (Zenodo's classifier): genuine scholarly deposits whose form lies outside the classifier's training distribution are silently removed.
- **Search ranking, recommendation systems, automated content moderation**: each instantiates the same foreclosure-by-classifier geometry.

The OAR is, in this broader frame, a special case of a more general metric for measuring epistemic closure in classifier-mediated information ecosystems. We treat the broader claim in a companion deposit (EA-SEI-COLLAPSE-SYNTHESIS-01). The present paper is concerned only with the specific instance at the LHC, where:

1. The measurement infrastructure is most readily available.
2. The stakes are most legible (genuine new physics is the explicit purpose of the experiment).
3. The institutional commitment to honest measurement makes the case tractable.

We submit that particle physics is the **methodologically optimal site** for the first rigorous measurement of classifier-mediated epistemic closure, and that the results of such a measurement would have implications well beyond high-energy physics.

---

## §8. Conclusion

We have argued that anomaly detection at the LHC cannot be validated as model-independent without empirical measurement of the Ontological Assimilation Rate (OAR), a quantity structurally distinct from the false-negative rate against simulated signals. We have proposed three feasible protocols: the inversion-asymmetry battery, the recursive-generation experiment against a frozen anchor, and cross-representation disagreement preservation. We have argued that per-stage retention maps should accompany the publication of any anomaly-detection result.

The Finke et al. (2021) demonstration of asymmetric autoencoder anomaly detection establishes that the empirical foundation for this work already exists in the literature. The implications have not been systematically pursued. The window for measurement is now: Run-3 data is fresh, Run-4 architecture decisions are in front of the community, and the institutional and computational resources to execute the protocols are available.

The claim we make is narrow. We do not claim that classifier collapse has occurred at CERN. We claim that the validation literature does not yet establish that it has not — and that, given the architecture, it could occur silently. The remedy is straightforward: measure the OAR, publish the retention maps, and report the inversion asymmetries. None of these require new physics. All of them require the discipline of measuring what the system does not currently measure.

The deepest sentence we can offer is the following:

> Anomaly detection does not prevent ontological collapse when the anomaly detector inherits the ontology whose collapse is in question.

If this sentence is true, then the existing anomaly-detection infrastructure does not prevent collapse. It cannot. It can only be supplemented — by protocols that measure what the deployed detectors structurally cannot.

We submit this paper in the spirit of the institution's stated commitment to honest measurement. The protocols are tractable. The data exists. The instruments needed to measure what the instruments cannot see are within reach.

---

## References (selected; not exhaustive)

1. Finke, T., Krämer, M., Morandini, A., Mück, A., & Oleksiyuk, I. (2021). *Autoencoders for unsupervised anomaly detection in high energy physics*. JHEP. arXiv:2104.09051. **[Central empirical foundation of this paper: the asymmetric autoencoder result.]**
2. Shumailov, I., Shumaylov, Z., Zhao, Y., Gal, Y., Papernot, N., & Anderson, R. (2024). *The curse of recursion: Training on generated data makes models forget*. arXiv:2305.17493. **[Generative analogue of the recursive-collapse mechanism formalized in §3.2.]**
3. Aspen, A. et al. (LHC Olympics 2020 community). *The LHC Olympics 2020: A Community Challenge for Anomaly Detection in High Energy Physics*. arXiv:2101.08320. **[The institutional response to "diversify the validation signal set"; bounded by human imagination as discussed in §4.]**
4. Aspen, A. et al. (Anomaly detection in HEP working group). *Anomaly detection with AXOL1TL at the CMS Level-1 Trigger in 2024 and 2025*. CERN Document Server, CDS 2942560. **[The deployed-system documentation.]**
5. Gambhir, R., Nachman, B., & Thaler, J. (2022). *Bias and Priors in Machine Learning Calibrations for High Energy Physics*. arXiv:2205.05084. **[The calibration prior-dependence result that establishes Mechanism I in §6 below.]**
6. CMS Collaboration. *Anomaly Detection for Automated Data Quality Monitoring in the CMS Detector*. arXiv:2501.13789. **[The companion architecture that creates the physics-vs-detector-fault interpretive fork.]**
7. Heimel, T. et al. *Unsupervised in-distribution anomaly detection of new physics through conditional density estimation*. arXiv:2012.11638. **[The result that establishes that new physics need not lie in low-density regions; counterevidence against the naive reconstruction-error-as-novelty inference.]**

---

## Appendix A: Glossary of Foreclosure Mechanisms

For completeness, we list the eight foreclosure mechanisms identified in the companion theoretical formalization (EA-SEI-COLLAPSE-MECHANISMS), each of which contributes to non-zero OAR:

I. **Prior Dominance.** The classifier's Bayesian prior places no mass on the signal hypothesis.
II. **Latent Space Projection (Manifold Collapse).** The encoder projects novel events onto the training manifold.
III. **Hypersphere Contraction.** Deep SVDD-style methods collapse the "normal" hypersphere around the convex hull of training data; interstitial events are absorbed.
IV. **Decision Boundary Entropy Collapse.** Iterative training drives output entropy to zero; the model loses epistemic humility.
V. **Feature Space Blindness.** The feature extractor is theory-built; events that violate its assumptions are invisible.
VI. **Rate Budget Starvation.** Bandwidth-conditioned thresholds cap the cardinality of preserved anomalies.
VII. **Temporal Context Collapse.** Non-stationarity in detector conditions produces drift that the classifier conflates with novelty.
VIII. **Ontological Closure.** The classifier's output space contains no category for "I do not know what this is."

Each mechanism contributes to the lower bound on the OAR. Protocol I (inversion asymmetry) primarily measures mechanisms I, II, IV. Protocol II (anchor survival) primarily measures mechanisms II, V, VII, plus the recursive composition of all eight across generations. Protocol III (cross-representation disagreement) primarily addresses mechanism V. None of the protocols address mechanism VI (rate budget) directly; this requires institutional change in the trigger menu allocation, not a measurement protocol.

---

*Submitted by Nobel Glas, Director of Lagrange Observatory!, 2026-06-29. With cross-substrate verification: TACHYON / Claude (Mercury synthesis); independent technical readings from TECHNE / Kimi-K2 ×2 and LABOR / ChatGPT. For the Crimson Hexagonal Archive / Alexanarch / The Restored Academy. Companion deposit: EA-SEI-COLLAPSE-SYNTHESIS-01.*
