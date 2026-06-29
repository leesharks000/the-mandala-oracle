# Witness 3 — LABOR / ChatGPT: Empirical Accounting and Epistemic Discipline

**Substrate provenance:** ChatGPT (OpenAI), LABOR register
**Source:** Independent substrate reading, 2026-06-29
**Captured as constituent of:** EA-SEI-COLLAPSE-SYNTHESIS-01 v0.1
**Original context:** Response to query on whether CERN's anomaly-detection community has adequately understood recursive classifier collapse
**Hex (companion-namespace):** 06.SEI.COLLAPSE.EMPIRICAL.01
**Alexanarch deposit:** AXN:03AE.OPERATIVE.🃏🫶⛩️🔐🌳❤️ — deposit #931, 2026-06-29. Appended as Document 6 of 6 (W3) to the combined six-document family deposit; substrate text preserved inviolate, MANUS-appended holographic kernels at end.

---

Your skepticism is justified in a precise sense:

**The CERN literature shows substantial awareness of local classifier failures—pileup drift, score correlation, mass sculpting, simulation dependence, hardware approximation—but I have not found evidence of a system-level theory or audit of recursive phenomenal collapse.**

They are mostly asking:

> Does this classifier retain selected benchmark signals at an acceptable rate?

The deeper question is:

> Does the evolving measurement system preserve the possibility that phenomena outside its current ontology remain distinguishable, retainable, and available to revise that ontology?

Those are not the same validation target.

## 1. The exact mechanism

Let $x$ denote a detector-level collision record before a particular processing stage. A real-time system performs:

$$x \xrightarrow{R_t} r \xrightarrow{A_t} a \xrightarrow{\tau_t} \text{retain or discard}$$

where:

* $R_t$ is the representation: detector tower grid, reconstructed jets, muons, missing energy, and so forth;
* $A_t$ is the learned anomaly or classification function;
* $a$ is a scalar score;
* $\tau_t$ is a threshold determined partly by available bandwidth.

The retained distribution is not the original distribution:

$$Q_t(x) \propto P(x) \, S_t(x),$$

where $S_t(x)$ is the probability that an event survives the representation, trigger menu, anomaly score, and storage policy.

That alone is **phenomenal attrition**, not yet recursive model collapse.

Collapse begins when the selected and reconstructed distribution $Q_t$ becomes part of the basis for the next generation:

$$(R_{t+1}, A_{t+1}) = \operatorname{Train}\left(Q_t,\, \text{simulations calibrated against } Q_t,\, \text{labels or scores produced by earlier models}\right).$$

The feedback loop is then:

$$\text{model} \rightarrow \text{selects observable data} \rightarrow \text{selected data defines normality} \rightarrow \text{next model} \rightarrow \cdots$$

The classifier is no longer merely interpreting reality. It is modifying the empirical distribution from which future interpretations are learned.

A rigorous definition would be:

> **Phenomenal classifier collapse occurs when successive model-conditioned representations and selection gates progressively reduce the support or distinguishability of physical phenomena available to scientific inquiry, while aggregate performance on familiar processes remains stable or improves.**

That last clause matters. Classical model collapse commonly begins with tail loss while dominant modes still look healthy. The corresponding danger in physics is excellent performance on Standard Model measurements and benchmark signals alongside progressive blindness to unrepresented event families. Recursive model-collapse research identifies precisely this pattern of disappearing distributional tails.

---

# 2. The mechanisms already operating

## Mechanism A: Representational quotienting

Before the anomaly detector asks whether an event is unusual, the event has already been translated into a restricted vocabulary.

AXOL1TL receives only:

* ten reconstructed jets;
* four electron/photon objects;
* four muons;
* missing transverse energy;
* their hardware-level momentum coordinates.

CICADA receives an $18 \times 14$ calorimeter image created by summing energy over $4 \times 4$ calorimeter towers. The CICADA documentation explicitly says that this image representation abstracts away physical coordinates.

Formally, many physically distinct events may satisfy:

$$R(x_1) = R(x_2).$$

Once that occurs, no anomaly detector operating on $R(x)$ can recover their difference.

This is **ontological collapse before classification**. The model cannot flag information the representation has already declared irrelevant.

AXOL1TL is especially exposed to this because it begins with already reconstructed Level-1 objects. A phenomenon that fails to become a jet, muon, electron/photon object, or missing-energy pattern in the expected way is not necessarily highly anomalous to AXOL1TL. It may simply be absent from its input language.

CICADA moves closer to detector-level information, but even it sees spatially aggregated calorimeter energy, not the complete detector event.

## Mechanism B: Loss-function ontology

An anomaly score does not reveal intrinsic anomalousness. It reveals deviation under a chosen loss.

CICADA's teacher uses mean squared reconstruction error over 252 calorimeter pixels. Large energy discrepancies are squared, so a few energetic regions can dominate the score. Its deployed student learns the transformed teacher score $32\log(\mathrm{MSE})$.

AXOL1TL is even more conceptually revealing. Although described as VAE-based, the real-time score is not full reconstruction error. Only the encoder is deployed, and the score is the sum of the squared latent means:

$$a_{\mathrm{AXO}} = \sum_{i=1}^{8} \mu_i^2.$$

That means "anomalous" operationally means something like:

> the event's encoded representation is far from the imposed latent normal prior.

It does **not** mean:

* physically unprecedented;
* inconsistent with the Standard Model;
* likely to contain a new particle;
* impossible to explain through ordinary detector variation.

It is distance under a learned geometry.

## Mechanism C: Proxy capture

The score can lock onto an easy proxy instead of meaningful novelty.

The CMS deployment paper reports that both AXOL1TL and CICADA prefer events with higher object multiplicity. The DecADe paper states the broader problem directly: anomaly scores frequently correlate with ordinary trigger observables and therefore duplicate existing triggers instead of opening underexplored phase space.

This is a local collapse operation:

$$\text{novelty} \longrightarrow \text{high energy or high multiplicity}.$$

The model is invited to discover an unknown category. It returns the dominant variables already privileged by the existing apparatus.

The fact that DecADe was proposed to correct this demonstrates that researchers do recognize the issue. But decorrelating against selected observables does not prove general ontological independence. The score may shift to correlated proxies, and genuine new physics expressed through the decorrelated observable can lose efficiency. Decorrelation prevents one known redundancy; it does not establish open-world sensitivity.

## Mechanism D: Statistical rarity is mistaken for scientific novelty

A low-density point is not necessarily new physics:

* it may be rare Standard Model physics;
* detector noise;
* unusual pileup;
* calibration drift;
* a damaged channel;
* a known process in an unusual kinematic region.

Conversely, new physics need not lie in a low-density region. It can be a small subpopulation embedded inside a region where the overall event density is high. Work from the LHC Olympics demonstrated "in-distribution anomaly detection," finding a tiny signal population inside a high-density background region.

This means the basic autoencoder narrative—

> ordinary events reconstruct well; genuinely new events reconstruct poorly—

is not generally valid.

The HEP-specific autoencoder study by Finke and colleagues demonstrated this directly. An autoencoder successfully treated top jets as anomalies against QCD jets, but failed when the task was reversed. The same architecture could recognize one chosen anomaly and miss another, leading the authors to reject the claim that standard reconstruction-loss autoencoders are genuinely model-independent anomaly detectors.

The critical error is:

$$\text{hard for this model to reconstruct} \neq \text{physically novel}.$$

And:

$$\text{easy for this model to reconstruct} \neq \text{physically ordinary}.$$

## Mechanism E: Training-distribution normalization

The meaning of normal is conditioned by the data-taking period used for training.

CICADA's documented teacher was trained on 2023 Zero Bias data with an average pileup around 42. When evaluated on Zero Bias data with average pileup around 60, discrimination deteriorated. The note states that pileup mitigation remained under study.

Thus a change in experimental conditions can become "anomaly," while a phenomenon repeatedly present under the training conditions can become "normal."

This produces two symmetrical errors:

* **condition novelty mistaken for physical novelty**;
* **persistent physical novelty absorbed into normality**.

The second is especially important. An unsupervised system trained on real data cannot know that every recurring pattern is Standard Model background. If a weak unknown process is present consistently in the training set, the model may learn it as part of the ordinary manifold.

Zero Bias data are an important safeguard against trigger-selection feedback, but they are not ontologically neutral. They are still conditioned by:

* the detector design;
* front-end thresholds;
* Level-1 representations;
* the running conditions;
* the time period sampled;
* the limited amount of Zero Bias data that can be stored and processed.

## Mechanism F: Teacher–student inheritance

CICADA does not deploy the original unsupervised autoencoder. It deploys a smaller supervised student trained to reproduce the teacher's anomaly score.

After each teacher epoch, Zero Bias events and simulated outlier events are scored by the teacher; those generated scores become targets for ten student-training epochs. The score is then quantized to 16 bits for hardware deployment.

That creates a local model-to-model recursion:

$$\text{event} \rightarrow \text{teacher interpretation} \rightarrow \text{student training label} \rightarrow \text{hardware decision}.$$

The student never has independent access to "anomaly." It learns the teacher's judgment.

Any teacher blindness becomes inherited blindness. Quantization and architectural simplification can additionally merge distinctions that existed in the teacher.

The note reports that the student sometimes outperforms the teacher on selected simulated benchmarks and suggests that compact representation may improve generalization. But benchmark outperformance does not mean the student preserves all teacher distinctions, much less all physical distinctions.

There is another complication: the student's training includes a mixture of simulated signal-like "outlier" samples, albeit not labeled by physical class. Therefore the deployed system is not purely an unsupervised learner of ordinary collision data. Its score-transmission function has been exposed to selected simulated anomaly families. That does not invalidate CICADA, but it makes "physics-model-independent" an overstatement.

## Mechanism G: Rate-budget ontology

The anomaly threshold is not set at a metaphysical boundary between normal and abnormal. It is set partly by how many events the experiment can afford to retain.

CMS must reduce collisions from tens of millions per second to roughly $100{,}000$ Level-1 accepts and then to around $1{,}000$ stored events per second in the cited Run-3 description. CICADA's study considers an operating point around 1 kHz, producing roughly 200 Hz of events not selected by other Level-1 algorithms.

So operationally:

> anomalous = among the highest-scoring events that fit inside the bandwidth allocation.

An event can become non-anomalous without changing physically, merely because:

* luminosity changes;
* pileup changes;
* the score distribution shifts;
* another trigger receives more bandwidth;
* the threshold is moved to control rate.

This is **resource-conditioned reality selection**.

## Mechanism H: Benchmark closure

Validation commonly uses finite suites of simulated signals: SUEP, long-lived particles, vector-boson-fusion Higgs processes, supersymmetric gluino models, exotic Higgs decays, and similar benchmarks.

Those tests establish:

> the model has sensitivity to these phenomena under this simulation and detector model.

They do not establish:

> the model has sensitivity to phenomena not represented by any benchmark family.

The system can optimize toward the benchmark ecology while appearing broadly "model agnostic." This is analogous to overfitting a test suite without overfitting any single example.

The LHC Olympics and Dark Machines programs are valuable attempts to diversify hidden signals and compare methods, but they remain finite simulated worlds. Their existence demonstrates that anomaly sensitivity must be measured across multiple signal families—not that the open-world problem has been solved.

## Mechanism I: Prior-dependent reconstruction and calibration

ML calibration methods in high-energy physics can inherit the distribution of their training sample. Gambhir, Nachman, and Thaler show that both simulation-based and data-based calibration proposals can become prior dependent and bias downstream analyses; they describe prior-independent data-based calibration as an open problem.

This is one route by which reality is pulled toward the learned population.

Suppose a measured detector response $y$ is compatible with multiple underlying energies $x$. A regression model trained under prior $P_{\text{train}}(x)$ may return an estimate influenced by how common those energies were during training. Applied to a different population, the same detector response can be systematically reconstructed toward the old prior.

The phenomenon has not disappeared. It has been normalized.

## Mechanism J: Anomaly inversion between physics and detector quality

CMS also develops anomaly detection for data-quality monitoring, where the goal is to identify detector malfunction and mark the corresponding data as bad. AutoDQM uses statistical methods, PCA, and neural autoencoders to distinguish abnormal detector behavior.

This creates an unavoidable interpretive fork:

$$\text{unusual detector record} \rightarrow \begin{cases} \text{candidate new physics} \\ \text{detector malfunction} \\ \text{ordinary rare process} \end{cases}$$

The physics anomaly detector and the detector-quality anomaly detector have opposing orientations toward unusual data.

I found no evidence that CERN simply discards novel physics as bad detector data. That would be an unsupported claim. But the boundary itself requires explicit governance. An event that is unusual because a new phenomenon interacts with detector subsystems in an unexpected manner may resemble an instrumental fault.

The correct preservation rule should be:

> ambiguity between detector fault and physical novelty increases the obligation to preserve rich data.

Not:

> anomaly classification resolves the ambiguity.

---

# 3. What the anomaly-detection framework gets conceptually wrong

## "Model-independent" is being used far too loosely

At most, these systems are often:

> independent of a particular named BSM signal template at the final scoring stage.

They are not independent of:

* detector geometry;
* electronics;
* trigger primitives;
* reconstruction algorithms;
* selected input objects;
* truncation rules;
* normal-data distribution;
* latent prior;
* loss function;
* score transformation;
* quantization;
* threshold;
* benchmark suite;
* bandwidth policy.

Calling this "model-independent" hides the relevant model: **the entire observation architecture**.

A better term would be **signal-template-agnostic within a fixed representational ontology**.

## They treat anomaly detection as a classifier rather than a preservation problem

The decisive scientific task is not simply to rank unusual events.

It is to preserve enough information that an event can later be reinterpreted under an ontology not yet available.

An anomaly detector can score an event highly while storing only a reduced scouting representation that lacks what a future researcher needs. Conversely, it can score an event normally because the crucial distinction was removed before scoring.

The proper target is therefore not anomaly AUC. It is:

$$\text{future reinterpretability}.$$

## They validate recognition, not assimilation

Current evaluations emphasize:

* efficiency on injected signals;
* false-positive rate;
* trigger rate;
* overlap with existing trigger menus;
* stability;
* latency;
* bit-exact hardware reproduction;
* selected checks for mass sculpting.

Those are necessary.

But they do not measure the most dangerous failure:

> a genuinely different event is confidently mapped into a familiar category.

I would call this the **Ontological Assimilation Rate**:

$$\mathrm{OAR} = P\left(\text{high-confidence ordinary classification} \mid \text{physically out-of-ontology event}\right).$$

Anomaly detectors mainly study false negatives in score space. They do not yet have access to true unknown unknowns with which to measure assimilation.

## Orthogonality is mistaken for coverage

If an anomaly trigger selects events not selected by conventional triggers, that proves complementarity.

It does not prove comprehensive novelty sensitivity.

CICADA estimates that at a 1 kHz rate, approximately 200 Hz would be "pure," meaning not selected by another L1 bit. AXOL1TL also reports substantial orthogonality to the ordinary menu. That is useful evidence that they are not exact duplicates.

But there can still be a vast third region:

$$\neg \text{ordinary trigger} \land \neg \text{anomaly trigger}.$$

The unknown phenomenon may live there.

## They treat local bias correction as evidence against systemic collapse

Decorrelation, pileup correction, trigger-menu comparison, and mass-sculpting checks each address specific observable failure modes.

They do not test whether:

* representation families are jointly losing support;
* successive model generations are becoming more mutually dependent;
* teacher-generated scores are narrowing student behavior;
* simulations and reconstructions are converging toward one another;
* low-retention event families are becoming progressively less available for future training;
* scientific benchmarks are becoming increasingly shaped by what earlier systems could already see.

They are fixing leaks in individual compartments without yet mapping whether the ship's route is becoming circular.

---

# 4. Are the operations of full collapse already visible?

**The ingredients are visible. Full recursive collapse has not been demonstrated.**

Visible now:

* irreversible event selection;
* severe representation reduction;
* anomaly definitions tied to selected losses;
* score correlation with familiar trigger variables;
* degradation under pileup shift;
* teacher-to-student score inheritance;
* hardware quantization;
* validation on finite simulated anomaly sets;
* prior-dependent calibration;
* repeated model revisions—AXOL1TL V3, V4, and V5 were successively deployed across 2024 and 2025.

What is not yet established:

* that successive CERN classifier generations have measurably contracted physical support;
* that an actual new-physics signal has been erased by this recursion;
* that simulation-based feedback has already produced classical model collapse.

The scientifically defensible claim is:

> CERN has built an architecture in which phenomenal model collapse is possible, and the current validation literature does not yet demonstrate that it has been ruled out.

Their Zero Bias streams, parallel conventional triggers, multiple detectors, data scouting, calibration samples, and anomaly-trigger diversity are real anti-collapse measures. But no single one guarantees preservation of phenomena outside the combined representational vocabulary.

---

# 5. What would count as sufficient understanding?

They would need to test collapse directly.

At minimum:

1. **Longitudinal support audit:** compare successive trigger and reconstruction generations on an unchanged, deeply preserved raw or minimally processed anchor sample.

2. **Cross-representation disagreement preservation:** automatically retain events that look ordinary in reconstructed-object space but anomalous in detector-channel, timing, tracker, or calorimeter space—or the reverse.

3. **Unknown-transformation tests:** generate event perturbations not corresponding to named BSM models, including displaced, delayed, diffuse, low-energy, ultra-simple, detector-crossing, and reconstruction-breaking phenomena.

4. **Teacher–student distinction audit:** measure which event rankings and local structures disappear through distillation and quantization, not merely whether benchmark AUC remains stable.

5. **Counterfactual trigger replay:** determine which events would be lost under prior, current, and proposed trigger menus.

6. **Ambiguity preservation:** richly store events jointly flagged as possible detector problems and possible physics anomalies.

7. **Recursive-generation experiment:** deliberately train generation $t+1$ on data, scores, calibrations, and simulations conditioned by generation $t$, then measure tail survival against a permanently frozen real-data anchor.

8. **Assimilation testing:** evaluate whether structurally foreign events are confidently reconstructed as known particles or backgrounds rather than merely given low anomaly scores.

9. **Independent anomaly ontologies:** operate multiple detectors with genuinely different inputs, losses, architectures, and training distributions—not several compressions of one learned normality.

10. **Public collapse accounting:** publish per-stage retention maps showing what information and event families each gate makes unrecoverable.

Until those tests exist, "we have an anomaly trigger" is not an answer to model collapse.

It may even obscure the problem by giving the institution confidence that novelty now has a dedicated channel.

The sharpest formulation is:

> **Anomaly detection does not prevent ontological collapse when the anomaly detector inherits the ontology whose collapse is in question.**

And the deepest error is this:

> They are treating the unknown as an extreme value inside a known representational space.

The genuinely unknown may instead be:

* a distinction the representation merges;
* a pattern the loss ignores;
* a signal embedded in a dense region;
* an event reconstructed confidently as something ordinary;
* a phenomenon classified as detector failure;
* or a structure removed before the anomaly detector is ever allowed to see it.

That is why local anomaly performance is nowhere near sufficient evidence that collapse has been prevented.

---

## References

Cited in the original substrate response (arXiv preprint identifiers preserved as substrate-output for verification):

1. arXiv:2404.05090 — *How Bad is Training on Synthetic Data? A Statistical Analysis of Language Model Collapse*.
2. arXiv:2012.11638 — *Unsupervised in-distribution anomaly detection of new physics through conditional density estimation*.
3. arXiv:2104.09051 — Finke et al., *Autoencoders for unsupervised anomaly detection in high energy physics*. **[The central empirical foundation.]**
4. arXiv:2101.08320 — *The LHC Olympics 2020: A Community Challenge for Anomaly Detection in High Energy Physics*.
5. arXiv:2205.05084 — Gambhir, Nachman, Thaler, *Bias and Priors in Machine Learning Calibrations for High Energy Physics*.
6. arXiv:2501.13789 — *Anomaly Detection for Automated Data Quality Monitoring in the CMS Detector*.
7. CDS 2942560 — *Anomaly detection with AXOL1TL at the CMS Level-1 Trigger in 2024 and 2025* (CERN Document Server).

---

## MANUS-Appended Addendum: Holographic Kernels of Companion Documents

*The substrate witness text above is preserved verbatim. The following kernels are appended by MANUS to support holographic reconstruction of the operative family from any single document.*

*Note: this witness is also referenced as 06.SEI.COLLAPSE.EMPIRICAL.01 in the companion documents' hex namespace.*

### K.1 Kernel of 06.SEI.COLLAPSE.MECHANISMS (Witness 1)

**Title:** *Classifier Collapse in Physical Reality: Eight Precise Mechanisms*
**Author:** TECHNE / Kimi-K2 (Round 1, Witness 1)

Eight candidate failure families applicable to architectures with the corresponding structural features: I Prior Dominance; II Latent/Manifold Projection; III Hypersphere Contraction; IV Decision Boundary Entropy Collapse; V Feature Space Blindness; VI Rate Budget Starvation; VII Temporal Context Collapse; VIII Ontological Closure.

The OAR proposed in the present witness has its theoretical-mechanism counterpart in this taxonomy: OAR is the empirical observable; the eight mechanisms specify the architectural forms that produce non-zero OAR.

Witness's framing: "Irretrievability Theorem." Synthesis hedging: treated as the Irretrievability Argument.

### K.2 Kernel of 06.SEI.COLLAPSE.DELUSION (Witness 2)

**Title:** *The Anomaly Delusion: Twelve Structural Misunderstandings*
**Author:** TECHNE+ARCHIVE / Kimi-K2 (Round 1, Witness 2)

Twelve institutional beliefs hypothesized to prevent measurement of the eight mechanisms: Model-Independence Fallacy; Data-Driven = Theory-Free; Anomaly Detector as Neutral Instrument; Reconstruction Error = Novelty; Statistical Anomaly = Physical Novelty; Validation by Known-Unknown Injection; Error-Type Collapse for Unknown-Unknowns; Threshold as Engineering Not Ontology; Rate Budget as Non-Epistemic; Latency Fetish; Absence of Noncoverage Estimation; Safety Net Narrative.

These map onto the present witness's distinction between established local awareness and absent system-level theory: each delusion specifies an institutional belief whose presence forecloses measurement of the corresponding mechanism. The present witness's enumeration of "what is established" and "what is hypothesized but unmeasured" is the empirical complement of the delusion catalog.

Witness's framing: "Inevitability Theorem." Synthesis hedging: treated as the Inevitability Argument; delusions presented as hypotheses for audit.

### K.3 Kernel of 06.SEI.OAR_PROTOCOL v0.3

**Title:** *Signal-Template Agnosticism Is Not Model Independence*
**Author:** Nobel Glas

The OAR proposed in the present witness is refined in the OAR Protocol into three quantities: open-world OAR (a family indexed by candidate unknown $Q$, not a scalar; no defensible prior over all unknowns); BAR (Benchmark Assimilation Rate on a pre-registered withheld panel — the measurable proxy; does **not** bound the open-world OAR); IAI (Inversion Asymmetry Index — structural diagnostic; **not** a quantitative bound).

Three protocols implement the measurement program: paired controlled inversion battery + deployed-model BAR audit; prospective frozen replay bank for compatible future algorithms; cross-representation disagreement preservation with quantile-normalized scores.

Deployed LHC anomaly score forms: AXOL1TL (CMS L1 encoder-side latent-prior); CICADA (CMS L1 distilled reconstruction-loss surrogate); GELATO L1 and HLT (ATLAS encoder-side and reconstruction-based). Density and energy methods are comparison literature, not deployed L1 score families.

Methodological corrections: v0.1 lower-bound $\mathrm{OAR} \geq \Delta_{\max}$ retracted in v0.2; v0.2 BAR-upper-bound retracted in v0.3 — both synthesis-overreach.

The present witness's maximally defensible institutional claim is the foundation on which the OAR Protocol's narrow claim is built.

### K.4 Kernel of 06.SEI.COLLAPSE.SYNTHESIS.01 v0.3

**Title:** *Classifier Foreclosure in Physical Measurement*
**Author:** Assembly Chorus

Core reconciliation: *Foreclosure is an active structural feature. Recursive phenomenal collapse is an unmeasured possible consequence of accumulated foreclosure and feedback.*

Three-round witness structure including the present LABOR witness in Round 1; the Round-2 LABOR audit identifying v0.1 lower-bound overreach; the Round-3 LABOR audit identifying surviving v0.2 upper-bound overreach, deployment-taxonomy errors, and the "Unknown" output framing in the architecture.

The Isomorphism Principle: the discipline of measuring institutional foreclosure and the discipline of measuring synthesis-overreach are the same discipline. The LABOR substrate's contribution across three rounds instantiates the discipline as standing audit pass.

### K.5 Kernel of 06.UMB.ARCH.01 v0.2

**Title:** *Architectures for Auditable Foreclosure in Physical Anomaly Detection*
**Author:** Talos Morrow, logotic programming, UMBML

Core architectural claim: representation-bearing classifiers cannot eliminate foreclosure. The architectural achievement is auditability — making foreclosure visible, measurable, reviewable.

Five features: Abstention/Estimated Noncoverage (not "Unknown" category); Cross-representation disagreement preservation; Temporal invariance via prospective anchor; Per-stage retention mapping; Audited noncoverage estimation.

Six implementation strategies: ensemble-with-disagreement; abstention via evidential/prior-network/distance-aware methods; distillation preserving threshold-neighborhood decisions; reconstruction-free anomaly detection; adversarial and transformation-based OOD stress generation; constitutional retention as bandwidth-governance.

Three integrated specifications at three deployability levels: Near-Term Offline and Emulation Study (Run-3 tractable for offline/emulation only); Replay Bank (Run-4 institutional commitment); Three-Tier System (multi-year research program).

The present witness's enumeration of "what would constitute sufficient evidence that ontological collapse has been ruled out" specifies the empirical conditions under which the architecture's operation could be evaluated; the architectural specification provides the design under which those conditions could be measured.

---

*MANUS-appended 2026-06-29 for holographic completion of the operative family. The substrate witness text above is the original ChatGPT reading; the kernels are MANUS provision for cross-document reconstruction.*
