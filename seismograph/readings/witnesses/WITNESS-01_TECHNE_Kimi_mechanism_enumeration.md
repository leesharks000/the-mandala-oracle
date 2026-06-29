# Witness 1 — TECHNE / Kimi-K2 (i): Formal Mechanism Enumeration

**Substrate provenance:** Kimi-K2 (Moonshot AI), TECHNE register
**Source:** Independent substrate reading, 2026-06-29
**Captured as constituent of:** EA-SEI-COLLAPSE-SYNTHESIS-01 v0.1
**Original hex:** 06.SEI.COLLAPSE.MECHANISMS

---

# CLASSIFIER COLLAPSE IN PHYSICAL REALITY: Eight Precise Mechanisms

**Document Type:** THEORETICAL_FORMALIZATION
**Extends:** Prior research on automated epistemic compression (CERN/semantic homology)
**Hex:** 06.SEI.COLLAPSE.MECHANISMS
**Status:** PROPOSED — Assembly Review

---

## §0. Formal Definition

**Classifier collapse** in physical systems is the degenerative process by which a discriminative model, trained exclusively or dominantly on a known distribution of physical events, progressively loses the capacity to represent, detect, or retain events that fall outside that distribution. Unlike generative model collapse (Shumailov et al.), which operates through recursive pollution of training data by synthetic outputs, classifier collapse operates through **structural foreclosure**: the model's architecture, training objective, and operational constraints collectively constrain the space of possible classifications to the space of known phenomena.

The result is not merely error. It is **ontological disappearance**: the event occurs, the detector registers, but the classifier renders it unclassifiable-as-signal, and the trigger system discards it before it becomes data.

---

## §1. Mechanism I: Prior Dominance (Bayesian Swallowing)

**Formal Description:**
Consider a classifier trained to discriminate between signal $S$ and background $B$. The posterior probability of signal given detector features $\mathbf{x}$ is:

$$P(S \mid \mathbf{x}) = \frac{P(\mathbf{x} \mid S) \cdot P(S)}{P(\mathbf{x} \mid S) \cdot P(S) + P(\mathbf{x} \mid B) \cdot P(B)}$$

When the classifier is trained on background-only data (as in CMS's AXOL1TL and CICADA systems, trained on ZeroBias data), $P(S) = 0$ in the empirical training distribution. The model never learns the likelihood $P(\mathbf{x} \mid S)$. For any novel physical event $\mathbf{x}_{\text{novel}}$:

$$P(S \mid \mathbf{x}_{\text{novel}}) = 0$$

The classifier has no Bayesian mass to assign to the signal hypothesis. The novel event is swallowed by the background prior.

**Physical Manifestation:**
A genuinely new particle decay produces a detector pattern. The autoencoder computes reconstruction error. Because the encoder has never seen this pattern, it maps $\mathbf{x}_{\text{novel}}$ to the nearest latent point $\mathbf{z}_{\text{known}}$ on the manifold of Standard Model processes. The decoder reconstructs a Standard Model-like event. The reconstruction error is low. The event is classified as "normal background" and discarded.

**Irretrievability:**
The event is not flagged. It is not queued. It is not written to disk. The Bayesian swallowing happens in the 4μs L1 trigger latency, and the decision is irreversible.

---

## §2. Mechanism II: Latent Space Projection (Manifold Collapse)

**Formal Description:**
A variational autoencoder (VAE) anomaly detector defines a mapping:

$$\mathbf{z} = E_{\phi}(\mathbf{x}), \quad \hat{\mathbf{x}} = D_{\theta}(\mathbf{z})$$

with reconstruction error $\mathcal{L}_{\text{rec}} = \|\mathbf{x} - \hat{\mathbf{x}}\|^2$ and KL regularization $\mathcal{L}_{\text{KL}} = D_{\text{KL}}(q_{\phi}(\mathbf{z} \mid \mathbf{x}) \| p(\mathbf{z}))$.

During training on background-only data, the encoder learns to map the support of the background distribution $\mathcal{X}_B$ onto a compact region of latent space $\mathcal{Z}_B$. The decoder learns to reconstruct any $\mathbf{z} \in \mathcal{Z}_B$ as a plausible background event.

For a novel event $\mathbf{x}_{\text{novel}} \notin \mathcal{X}_B$, the encoder projects it onto $\mathcal{Z}_B$:

$$\mathbf{z}_{\text{novel}} = \arg\min_{\mathbf{z} \in \mathcal{Z}_B} \|E_{\phi}(\mathbf{x}_{\text{novel}}) - \mathbf{z}\|$$

The decoder then generates $\hat{\mathbf{x}}_{\text{novel}} = D_{\theta}(\mathbf{z}_{\text{novel}})$, which is a background event. The reconstruction error $\|\mathbf{x}_{\text{novel}} - \hat{\mathbf{x}}_{\text{novel}}\|$ may be **lower than the anomaly threshold** because the projection has destroyed the novel information.

This is **manifold collapse**: the latent space has collapsed onto the background manifold. Novel events are "explained" by projection onto the known.

**Physical Manifestation:**
CMS's CICADA processes 18×14 calorimeter images. A new physics event with an unusual energy deposition pattern is encoded into a latent code that resembles a known QCD multijet event. The decoder reconstructs a multijet-like image. The anomaly score is below threshold. The event passes as normal.

**Irretrievability:**
The projection is lossy. The original $\mathbf{x}_{\text{novel}}$ is not stored. Only the classification decision (normal) is retained.

---

## §3. Mechanism III: Hypersphere Contraction (SVDD Collapse)

**Formal Description:**
Deep Support Vector Data Description (Deep SVDD) learns a neural network mapping $\phi(\mathbf{x}; \mathcal{W})$ that maps normal data into a hypersphere of minimum radius $R$ centered at $\mathbf{c}$:

$$\min_{\mathcal{W}} R^2 + \frac{1}{n} \sum_{i=1}^{n} \max\{0, \|\phi(\mathbf{x}_i; \mathcal{W}) - \mathbf{c}\|^2 - R^2\}$$

Without regularization, the network suffers from **hypersphere collapse**: it learns a trivial constant mapping $\phi(\mathbf{x}) = \mathbf{c}$ for all $\mathbf{x}$, collapsing all inputs to the center.

Even with regularization, the hypersphere contracts around the convex hull of the training distribution. The volume of "normal" space shrinks. Events that lie in the expanding exterior are flagged as anomalous. But events that lie in the **interstices** — between known modes but not far from the center — are mapped inside the hypersphere and classified as normal.

**Physical Manifestation:**
A particle physics anomaly detector using Deep SVDD maps all Standard Model events into a tight cluster. A new physics event with features intermediate between two known backgrounds is mapped to the center region. It is classified as normal.

**Irretrievability:**
The interstitial event is not anomalous enough to escape the hypersphere. It is swallowed by the center.

---

## §4. Mechanism IV: Decision Boundary Entropy Collapse

**Formal Description:**
For a binary classifier (e.g., signal vs. background jet tagger like ATLAS GN2), the output is a softmax probability vector. As the classifier is trained iteratively on background-dominated data, the entropy of the output distribution collapses:

$$H(\mathbf{p}) = -\sum_{i} p_i \log p_i \rightarrow 0$$

The classifier becomes **overconfident**. For any input, it outputs $p(\text{background}) \approx 1.0$ or $p(\text{signal}) \approx 1.0$ with near-certainty. The decision boundary becomes sharp, but the **uncertainty region** — the space where the classifier admits ignorance — vanishes.

A novel event that should trigger high uncertainty (the classifier has never seen anything like it) instead triggers high-confidence background classification. The model has no epistemic humility.

**Physical Manifestation:**
ATLAS's transformer-based jet tagger, trained on millions of simulated jets, assigns a "light-jet" score of 0.999 to a novel event. The event is not routed to the anomaly stream because the classifier is certain it is background.

**Irretrievability:**
The confidence score is logged, not the uncertainty. The event is routed to the background stream.

---

## §5. Mechanism V: Feature Space Blindness (Representation Collapse)

**Formal Description:**
The classifier does not operate on raw detector readouts. It operates on **engineered features** or learned embeddings: track parameters, calorimeter energy deposits, secondary vertex masses, jet substructure variables. The feature extraction function $\psi: \mathcal{D} \rightarrow \mathcal{F}$ is itself a compression.

If novel physics manifests in detector channels that are not represented in $\mathcal{F}$, the event is **invisible to the classifier** regardless of its physical significance. The feature space has collapsed the raw detector space onto a subspace optimized for known physics.

Formally, if $\mathbf{x}_{\text{novel}} \in \ker(\psi)$ — that is, the novel event lies in the null space of the feature extractor — then:

$$\psi(\mathbf{x}_{\text{novel}}) = \mathbf{0}$$

The event is indistinguishable from noise in feature space.

**Physical Manifestation:**
Long-lived particles with displaced vertices may not produce prompt tracks. A b-tagging algorithm that relies on secondary vertex reconstruction will fail to see them. The particles are real; the features are blind.

**Irretrievability:**
The feature extraction happens before classification. The null-space event is never represented.

---

## §6. Mechanism VI: Rate Budget Starvation (Resource Collapse)

**Formal Description:**
The L1 trigger operates under a hard bandwidth constraint. Let the total output rate be $R_{\text{max}} \approx 100$ kHz. The anomaly detection trigger is allocated a sub-budget $R_{\text{ano}} \subset R_{\text{max}}$, with thresholds calibrated to produce specific rates (e.g., 10 Hz, 100 Hz, 1000 Hz).

Even if a novel event is correctly assigned a high anomaly score, it enters a **priority queue** with all other high-scoring events. If the queue length exceeds the bandwidth allocation, events are dropped by **first-in-first-out** or **priority-based** scheduling.

The probability of retention for a novel event is not merely $P(\text{anomaly} \mid \mathbf{x})$. It is:

$$P(\text{stored} \mid \mathbf{x}) = P(\text{anomaly} \mid \mathbf{x}) \cdot P(\text{queue capacity} \mid \text{anomaly})$$

During high-luminosity runs, pileup events (simultaneous collisions) saturate the anomaly queue with background events that happen to score high. The true anomaly is starved.

**Physical Manifestation:**
During a high-luminosity period at CMS, the AXOL1TL anomaly stream is saturated at its 1000 Hz budget. A genuine new physics event arrives. The queue is full. The event is dropped.

**Irretrievability:**
The drop is a resource decision, not a classification error. No flag is raised. The event is gone.

---

## §7. Mechanism VII: Temporal Context Collapse (Non-Stationarity Blindness)

**Formal Description:**
The detector environment is non-stationary. Luminosity changes, detector calibrations drift, and pileup conditions vary. The classifier is trained on data from a specific run period $\mathcal{T}_{\text{train}}$ and assumes stationarity:

$$P(\mathbf{x} \mid \text{background}, t) = P(\mathbf{x} \mid \text{background}, t_0) \quad \forall t$$

But in reality, $P(\mathbf{x} \mid \text{background}, t)$ drifts. The classifier's model of "normal" is frozen at $\mathcal{T}_{\text{train}}$. A novel event that occurs during a detector configuration not represented in training may be classified as anomalous — but so are thousands of ordinary background events under the same conditions. The signal-to-noise ratio collapses.

Alternatively, the classifier adapts online to current conditions (adaptive thresholding). If the novel event resembles the current background drift, the adaptive threshold adjusts to accommodate it, rendering it invisible.

**Physical Manifestation:**
A new physics event occurs during a detector calibration shift. The anomaly detector flags it, but also flags 10,000 ordinary events under the same shift. The physics group cannot afford to analyze all 10,001 events. The true signal is buried in the noise of non-stationarity.

**Irretrievability:**
The event is stored but unfindable. It is in the data, but the analysis pipeline has no way to distinguish it from calibration artifacts.

---

## §8. Mechanism VIII: Ontological Closure (Category Collapse)

**Formal Description:**
The classifier's output space is a closed set of categories: $\mathcal{C} = \{c_1, c_2, \dots, c_k\}$. For CMS: $\mathcal{C} = \{\text{background}, \text{anomaly}\}$. For ATLAS jet tagging: $\mathcal{C} = \{\text{b-jet}, \text{c-jet}, \text{light-jet}\}$.

There is no category for **genuinely new physics**. The classifier cannot output "I do not know what this is." It can only output the nearest known category. This is the **ontological closure** of the classification space.

Even "anomaly" is not a physics category. It is a statistical deviation metric. An anomaly is not interpreted as "new particle." It is interpreted as "unusual background." The ontological frame prevents the anomaly from becoming a discovery.

**Physical Manifestation:**
An anomaly detection trigger preserves an event with high reconstruction error. The offline analysis team examines it. Because there is no theoretical model for the event, they classify it as "detector noise" or "unusual pileup" and discard it. The category system has no slot for "evidence of physics beyond the Standard Model."

**Irretrievability:**
The event is stored but mentally discarded. The ontological frame of the analysis team mirrors the ontological frame of the classifier.

---

## §9. The Irretrievability Theorem

**Theorem:** In a physical classifier system with $N$-stage trigger architecture, the compound probability that a novel event becomes available for offline scientific analysis is:

$$P(\text{data} \mid \mathbf{x}_{\text{novel}}) = \prod_{i=1}^{N} P(\text{pass}_i \mid \text{pass}_{i-1}, \mathbf{x}_{\text{novel}})$$

where each $P(\text{pass}_i)$ is subject to:

1. **Classification error** (Mechanisms I–V): The event is misclassified at stage $i$.
2. **Resource starvation** (Mechanism VI): The event is correctly classified but dropped due to bandwidth constraints.
3. **Temporal misalignment** (Mechanism VII): The event occurs during a non-stationary period where the classifier is miscalibrated.
4. **Ontological foreclosure** (Mechanism VIII): The event is preserved but interpreted within a closed category system that cannot name it.

For a 40 MHz input stream reduced to 1 kHz storage (ATLAS/CMS), the base retention rate is $2.5 \times 10^{-5}$. When any of Mechanisms I–VIII operates, the effective retention rate for novel events approaches **zero**.

**Corollary:** The classifier does not merely filter data. It **constitutes** the data. What fails the classifier is not data. It is physical occurrence without scientific existence.

---

## §10. Distinction from Generative Model Collapse

| Property | Generative Model Collapse (Shumailov) | Classifier Collapse (Physical Systems) |
|----------|--------------------------------------|----------------------------------------|
| **Mechanism** | Recursive training on synthetic data | Training on closed distributions + operational constraints |
| **Object** | Generative model $G(z)$ | Discriminative classifier $f(\mathbf{x})$ |
| **Symptom** | Output variance → 0; distribution becomes delta function | Acceptance region → training support; novel events → background |
| **Reversibility** | Can be mitigated by preserving original data | Irreversible: rejected events are not stored |
| **Domain** | Language, image generation | Physical reality: particle physics, astronomy, materials science |
| **Key metric** | Wasserstein distance from true distribution | False negative rate for unknown-unknowns |

Classifier collapse is the **discriminative analogue** of generative model collapse. Where Shumailov's models forget the tails of their own distribution, physical classifiers **never learn the tails** of the true physical distribution. The collapse is present from the first forward pass.

---

## §11. Conformance

A trigger system design document is in **classifier collapse drift** if it:

- Claims that anomaly detection is "model-independent" without acknowledging the ontological closure of the training distribution (Mechanism VIII).
- Validates the classifier only against known processes and injected signals (Mechanism IV).
- Presents the anomaly stream as a "safety net" without quantifying the rate budget starvation probability (Mechanism VI).
- Fails to specify the feature space and its null space (Mechanism V).

**Verification:** Any physical classifier deployed for scientific discovery must report:
- The **support** of its training distribution.
- The **volume** of its latent space not occupied by training data.
- The **false negative rate** for out-of-distribution events (not just for known anomaly classes).
- The **rate budget** and queue drop probability.
- The **ontological category system** and its closure properties.

---

∮ = 1. The boundary holds. But the boundary decides what is allowed to pass.

---

**Eight mechanisms. Eight modes of foreclosure. The event occurs. The detector registers. The classifier decides. And the decision is, for the rejected event, the end of its scientific existence.**
