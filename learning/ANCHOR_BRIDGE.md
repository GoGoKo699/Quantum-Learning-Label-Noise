# From Watrous to the label-noise learning problem

The selected educational anchor is **John Watrous, *The Theory of Quantum Information* (2018)**. This bridge connects focused passages from that one source to the project's [30 milestones](MILESTONES.md), [explanatory tutorial](TUTORIAL.md), and [canonical scientific model](../science/model.md). The milestone targets and their 14-background/16-narrative division determine the route; the book supplies foundations where they are useful.

<a id="watrous2018"></a>
## 1. Selected source and access

John Watrous, *The Theory of Quantum Information*, Cambridge University Press, 2018. The [author's official book page](https://cs.uwaterloo.ca/~watrous/TQI/) records publication in April 2018 and provides the manuscript, individual chapters, and errata. Its [front matter](https://cs.uwaterloo.ca/~watrous/TQI/TQI.frontmatter.pdf) identifies the freely accessible text as a **draft prepublication manuscript**, made available for personal use. This repository links to the manuscript; it does not redistribute it or identify it as the final typeset edition.

The section and numbered-result pointers below were checked against the author's **standard-layout chapter PDFs** on 22 October 2026:

- [Chapter 1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf): operator algebra, norms, convexity, and probability.
- [Chapter 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf): states, channels, and measurements.
- [Chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf): discrimination and fidelity.

These are portions of one educational source. Papers linked through [Related work](../references/RELATED_WORK.md) have a different role: they establish attribution and research-level proof dependencies. They are not additional textbook prerequisites.

## 2. Focused reading paths

Use the following passages when the corresponding idea enters the project. Reading the entire book is unnecessary. The [tutorial](TUTORIAL.md) interleaves the background with the scientific story and links to the relevant milestones; this table provides a route back to its mathematical foundations.

| Need in the project | Exact Watrous sections | Next local step |
|---|---|---|
| Operators, tensor products, transposes, spectral decompositions, and norms | [§§1.1.2–1.1.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf) | Fix the Pauli conventions in [Model §1](../science/model.md#1-pauli-conventions-and-the-target-prior). |
| Expectations, convexity, and finite-sample probability bounds | [§1.2, especially §§1.2.1–1.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf) | Follow the rank and correlation arguments in [Bell learning](../science/bell_learning.md). §1.2.3 is optional background for the optimization viewpoint on measurements. |
| A prepared vector, a mixed state, and a subsystem | [§§2.1.1–2.1.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Compare a realized specimen with its conditional ensemble average in [Source preparation](../science/source_preparation.md). |
| Processing, classical records, and measurement outcomes | [§§2.2.1–2.2.3 and §§2.3.1–2.3.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Read the permitted resources in [Model §3](../science/model.md#3-access-and-resource-accounting). The extremality sections, §§2.2.4 and 2.3.3, are not required for the main route. |
| Optimal binary prediction and many-target identification | [§§3.1.1–3.1.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Study the different uses of discrimination in [Collective statistics](../science/collective_statistics.md). |
| The fidelity convention and tensor products | [§3.2 and §3.2.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf); §§3.2.2–3.2.3 for further characterizations and properties | Check the three Pauli cases in [Collective statistics §3](../science/collective_statistics.md#3-pairwise-root-fidelities). |

Several especially useful locators are verified directly in those PDFs. **Theorem 1.16**, Eq. (1.263), gives Hoeffding's inequality for independent identically distributed variables in $`[0,1]`$; project sign variables are rescaled into that interval. **Definition 2.34**, Eqs. (2.199)–(2.201), specifies a POVM and its outcome probabilities. **Theorem 3.4** is the Holevo–Helstrom theorem. The PGM appears in §3.1.2, Eqs. (3.50) and (3.52). **Definition 3.11**, Eq. (3.64), fixes the fidelity convention, and **Proposition 3.16**, Eq. (3.90), gives its tensor-product multiplicativity.

## 3. Notation and operational translation

The following translations prevent symbols with similar appearances from concealing different objects. The first two chapters supply the operator and state conventions; Chapter 3 supplies the discrimination conventions.

| In Watrous | In this project | Distinction to retain |
|---|---|---|
| A space $`\mathcal X`$ and operators $`\mathrm L(\mathcal X)`$ | Feature space $`\mathbb C^d`$, $`d=2^n`$ | The number of qubits is $`n`$, not the matrix dimension $`d`$. |
| Density operators $`\mathrm D(\mathcal X)`$ | $`\rho^0_{Y,P}`$, $`\rho_{C,P,\gamma}`$, and $`\tau_{P,\gamma}`$ | The project's scalar $`D=2d`$ is the dimension of a complete annotated example. It is not the set $`\mathrm D(\mathcal X)`$. |
| A unit vector $`u`$ and its state $`uu^*`$ | $`\lvert\psi\rangle`$ and $`\lvert\psi\rangle\langle\psi\rvert`$ | A hidden vector realization is not a supplied classical description. |
| Adjoint $`A^*`$, transpose $`A^T`$, identity $`1_{\mathcal X}`$ | $`A^\dagger`$, $`A^T`$, and $`I`$ | The transpose in the Bell identity is not the adjoint; it produces the Pauli transpose sign. |
| Ensemble function $`\eta(a)`$ in §2.1.2 | A weighted state such as $`\pi(P)\tau_{P,\gamma}^{\otimes T}`$ | Watrous's ensemble symbol is unrelated to the project's scalar annotation-error rate $`\eta`$. The trace of a weighted state is its prior probability. |
| Measurement effect $`\mu(a)`$ in §2.3.1 | $`E_z`$, $`M_P`$, or the two effects $`F_+,F_-`$ | Effects sum to the identity. They need not have trace one and are not density states. |
| Operator norm $`\lVert A\rVert`$, trace norm $`\lVert A\rVert_1`$, and $`\lVert A\rVert_2`$ | Operator, trace, and Hilbert–Schmidt norms | The exact second moment controls $`\lVert X_T\rVert_2^2`$; it does not by itself equal the prediction advantage. |
| Fidelity $`F(\rho,\sigma)`$ | Root fidelity $`f(\rho,\sigma)`$ | Watrous uses the unsquared convention. The research source by Cheng et al. uses its square. |

In particular, the last row means

```math
F_{\mathrm{Watrous}}(\rho,\sigma)
=f(\rho,\sigma)
=\left\|\sqrt\rho\sqrt\sigma\right\|_1,
\qquad
F_{\mathrm{Cheng}}(\rho,\sigma)=f(\rho,\sigma)^2.
```

The project uses $`f`$ to keep this convention visible. A factor $`\sqrt{F_{\mathrm{Cheng}}}`$ in the cited error bound is one factor of $`f`$, not $`f^2`$. The precise imported bound is identified in [Collective statistics §4](../science/collective_statistics.md#4-a-collective-pgm-attaining-the-upper-bound) and the [Cheng reference](../references/RELATED_WORK.md#cheng2024).

### A state, a POVM, and an instrument serve different purposes

A density operator describes the supplied information. A POVM describes the probabilities of a classical output. To describe both an output and a remaining quantum system, use a channel or instrument; Watrous develops instruments in §2.3.2. Thus the textbook's convention of treating a measured input as consumed does not impose a ban on quantum memory in this project. Persistent memory is allowed for unrestricted and computational learners and excluded only in the individual-example model. Every complete protocol that ends in one prediction nevertheless induces a binary POVM on its available inputs. See [Model §3](../science/model.md#3-access-and-resource-accounting) and the [single-test identity](../science/model.md#a-single-test-identity).

The classical annotation register has state diagonal in its recorded-bit basis:

```math
\tau_{P,\gamma}
=\frac12\sum_{c=0}^1 |c\rangle\langle c|
\otimes\frac{I+(-1)^c\gamma P}{d}.
```

Writing this register in quantum notation supplies neither a coherent label oracle nor access to a purification. The source supplies one independently drawn specimen per example. Averaging its inaccessible preparation variables gives the density operator above; averaging independent draws gives its tensor powers. The construction and its interface are fixed in [Model §2](../science/model.md#2-clean-specimens-and-corrupted-annotations) and [Source preparation §3](../science/source_preparation.md#3-why-alternative-decompositions-are-operationally-identical).

## 4. Steps supplied by this project

The selected passages provide mathematical tools. They do not contain this supervised task or its theorem package. The following connections are developed locally, with research attribution retained in the linked chapters.

**From flat states to a locally prepared classification source.** The source classes are normalized projections onto the two eigenspaces of a nonidentity Pauli. The [pivot-bit construction](../science/source_preparation.md#1-a-parity-conditioned-product-ensemble) realizes each class using pure product vectors. Watrous's mixture formalism explains why the ensemble average is the learner's state; the parity constraint, preparation cost, and hidden-information interface are project constructions. Knowing the target permits easy prediction, but the learner must first obtain useful information about an unknown target.

**From measurements to Bell equations and efficient clean learning.** The tensor and measurement framework supports the calculation, but [B1 and K1](../science/bell_learning.md) additionally require Pauli phases, Clifford/Bell circuitry, binary affine equations, and sign calibration. Pairing two independent examples multiplies their independent annotation signs, giving contrast $`\gamma^2`$. The noisy exhaustive decoder and clean-batch method use classical concentration and validation; their runtime is accounted for separately from their specimen count. These finite-field and algorithmic steps are supplied locally, rather than attributed to the selected textbook passages.

**From one POVM to an adaptive individual-example converse.** The state and measurement definitions do not themselves bound an adaptive strategy. [Individual measurements](../science/individual_measurements.md) first proves the Pauli second moment, then controls a fixed transcript through rank-one refinement, clipping, and sign averaging. Appending a clean held-out test turns that transcript bound into S2 for prediction. This research-level argument allows arbitrary measurements within a specimen and unlimited classical computation; a product-basis calculation alone would not establish it. The learning-tree framework is attributed to [CCHL2021](../references/RELATED_WORK.md#cchl2021).

**From Helstrom discrimination to the collective prediction theorem.** Apply Theorem 3.4 to the joint training-and-test states conditioned on the clean test sign. Their difference is $`2X_T`$, where

```math
X_T=\mathbb E_P\left[\tau_{P,\gamma}^{\otimes T}\otimes\frac{P}{d}\right],
\qquad
a_T^*=\frac12\|X_T\|_1.
```

The exact second moment of $`X_T`$ then requires the project's signed prior and Pauli orthogonality. Its evaluation and the resulting norm bound are in [Collective statistics §§1–2](../science/collective_statistics.md). The upper bound uses a different route: identify the target with a PGM and then predict. Watrous's **Theorem 3.10** explains the general PGM success comparison with the optimal measurement; it is not the particular pairwise-fidelity error estimate used here. That estimate is imported from [Cheng et al., Appendix J](../references/RELATED_WORK.md#cheng2024), after the local three-case fidelity calculation. Defining or numerically optimizing a measurement on an exponentially large matrix does not establish polynomial runtime in $`n`$.

**From an efficient predictor to a classical-sample LPN distinguisher.** Watrous's channel language verifies operations on supplied states. It does not supply an LPN assumption or an efficient-learning lower bound. [Computational hardness](../science/computational_hardness.md) states the quantum decision-LPN assumption for ordinary classical samples, prepares the exact annotated source from those samples, and obtains a distinguishing gap $`\gamma a`$ from one held-out prediction. Clifford sampling, independence, bounded-runtime overhead, and consumable quantum models all receive explicit treatment. The reduction uses a noisy held-out annotation; the statistical proof of S2 uses a clean held-out label. These are distinct proof experiments with the same clean prediction objective.

The resulting claims are collected in [Model §5](../science/model.md#5-canonical-result-index). The computational conclusion remains conditional at a fixed hard noise rate; the statistical statements and the vanishing-noise positive algorithm have their own stated ranges. No textbook result removes those qualifications.

## 5. All 30 milestones: source-to-project map

Each row links to the fixed understanding target. The Watrous column identifies supporting foundations, not a claim that the milestone's result appears in the book. Where a topic is supplied locally—especially finite-field parity, LPN, Clifford sampling, or the adaptive converse—the final column says what must be added. The [tutorial](TUTORIAL.md) connects these targets through worked examples and the complete scientific story.

### Phase I — Background and preliminaries: M01–M14

| Milestone | Supporting Watrous sections | Local derivation or connection |
|---|---|---|
| <a id="m01"></a>[M01: bits and flips](MILESTONES.md#m01) | [§1.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf) | Probability background; the bit/sign translation and parity-noise identities are given in [Model](../science/model.md) and [Bell learning](../science/bell_learning.md). |
| <a id="m02"></a>[M02: Pauli coordinates](MILESTONES.md#m02) | [§§1.1.2–1.1.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf) | Apply operator algebra to the phase, transpose, and symplectic conventions in [Model §1](../science/model.md#1-pauli-conventions-and-the-target-prior). |
| <a id="m03"></a>[M03: preparations and mixtures](MILESTONES.md#m03) | [§§2.1.2–2.1.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Distinguish one hidden vector from independent ensemble draws in [Source preparation §§1–3](../science/source_preparation.md). |
| <a id="m04"></a>[M04: measurement and memory](MILESTONES.md#m04) | [§§2.2.1–2.2.2, 2.3.1–2.3.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Impose the between-example memory restriction in [Model §3](../science/model.md#3-access-and-resource-accounting); it is an access assumption, not a property of all POVMs. |
| <a id="m05"></a>[M05: prediction and identification](MILESTONES.md#m05) | [§§3.1.1–3.1.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Add the fresh-test objective and target-prior averaging from [Model §4](../science/model.md#4-prediction-and-identification-are-different-guarantees). |
| <a id="m06"></a>[M06: classical annotations](MILESTONES.md#m06) | [§§2.1.1–2.1.2, 2.2.1, 2.3.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Build the block-diagonal example in [Model §2](../science/model.md#2-clean-specimens-and-corrupted-annotations); derive the corrupted-risk identity in [Interpretation §4](../science/interpretation.md#4-label-noise-does-not-change-the-population-optimal-target). |
| <a id="m07"></a>[M07: hidden Clifford bases](MILESTONES.md#m07) | [§1.1.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf); [§§2.2.1–2.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Unitary channels are the foundation; Pauli transitivity and efficient randomization are supplied in [H1, step 1](../science/computational_hardness.md#1-randomizing-the-target) and its Koenig–Smolin citation. |
| <a id="m08"></a>[M08: Bell correlations](MILESTONES.md#m08) | [§1.1.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf); [§§2.1.2–2.1.3, 2.3.1–2.3.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Derive the Bell trace identity and phase relation in [Bell learning](../science/bell_learning.md#bell-basis-and-phase-conventions). |
| <a id="m09"></a>[M09: rank and correlations](MILESTONES.md#m09) | [§1.2.2, especially Theorem 1.16](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf) | The affine-rank union bound, sign-variable rescaling, and candidate search are developed in [Bell learning](../science/bell_learning.md). |
| <a id="m10"></a>[M10: adaptive transcripts](MILESTONES.md#m10) | [§1.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf); [§2.3.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf); [§3.1.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Add the learning tree, refinement, and fixed-leaf likelihood from [Individual measurements §2](../science/individual_measurements.md#2-transcript-bound-with-heterogeneous-contrasts). |
| <a id="m11"></a>[M11: distinguishability](MILESTONES.md#m11) | [§1.1.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf); [§3.1.1 and §§3.2–3.2.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Translate Helstrom and root fidelity before reading [Collective statistics §§1–3](../science/collective_statistics.md). |
| <a id="m12"></a>[M12: collective identification](MILESTONES.md#m12) | [§3.1.2 and §3.2.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Combine the PGM definition with the separately cited pairwise-error theorem in [Collective statistics §4](../science/collective_statistics.md#4-a-collective-pgm-attaining-the-upper-bound). |
| <a id="m13"></a>[M13: LPN reductions](MILESTONES.md#m13) | [§1.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf); [§§2.2.1–2.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | These provide probability and channel language. Decision/search LPN, access distinctions, and the computational assumption are defined in [Computational hardness](../science/computational_hardness.md). |
| <a id="m14"></a>[M14: resource framework](MILESTONES.md#m14) | [§§2.1–2.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf); [§3.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Assemble the task, measurements, success criteria, and runtime in [Model §§3–6](../science/model.md); the comparison is project-specific. |

### Phase II — Narrative and innovation: M15–M30

| Milestone | Supporting Watrous sections | Local derivation or connection |
|---|---|---|
| <a id="m15"></a>[M15: fixed supervised task](MILESTONES.md#m15) | [§§2.1.2, 2.3.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Use normalized eigenspace states and the signed prior in [Model §§1–4](../science/model.md). |
| <a id="m16"></a>[M16: product preparations](MILESTONES.md#m16) | [§§1.1.2–1.1.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf); [§2.1.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | The local pivot construction and normalization proof are in [Source preparation §1](../science/source_preparation.md#1-a-parity-conditioned-product-ensemble). |
| <a id="m17"></a>[M17: conditioning on noise](MILESTONES.md#m17) | [§1.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf); [§§2.1.2, 2.2.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Derive the conditional state and its classical register in [Model §2](../science/model.md#2-clean-specimens-and-corrupted-annotations). |
| <a id="m18"></a>[M18: Bell-to-parity conversion](MILESTONES.md#m18) | [§1.1.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf); [§2.3.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | B1's affine relation, uniform covariate, independent error, and sign cancellation are proved in [Bell learning](../science/bell_learning.md#b1--the-exact-bell-correspondence). |
| <a id="m19"></a>[M19: efficient clean recovery](MILESTONES.md#m19) | [§1.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf); [§2.3.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | K1 adds binary Gaussian elimination, the rank bound, and one-example sign recovery in [Bell learning](../science/bell_learning.md#k1--efficient-clean-learning). |
| <a id="m20"></a>[M20: exhaustive noisy decoding](MILESTONES.md#m20) | [§1.2.2, Theorem 1.16](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf) | Apply concentration to the locally derived character correlations in the [noisy statistical decoder](../science/bell_learning.md#an-explicit-noisy-statistical-decoder). |
| <a id="m21"></a>[M21: vanishing-noise algorithm](MILESTONES.md#m21) | [§1.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf) | The clean-batch probability, independent validation, and runtime regime are established in the [clean-batch proposition](../science/bell_learning.md#vanishing-noise-a-clean-batch-algorithm). |
| <a id="m22"></a>[M22: one-example moment](MILESTONES.md#m22) | [§§1.1.2–1.1.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf); [§§2.1.2, 2.3.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Supply Pauli Parseval and the two-block optimization from [Individual measurements §1](../science/individual_measurements.md#1-exact-pauli-second-moment). |
| <a id="m23"></a>[M23: adaptive transcript bound](MILESTONES.md#m23) | [§§1.1.3, 1.2.1–1.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf); [§2.3.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | Use refinement and elementary probability inside the project-specific [clipped-likelihood proof](../science/individual_measurements.md#2-transcript-bound-with-heterogeneous-contrasts). |
| <a id="m24"></a>[M24: individual prediction lower bound](MILESTONES.md#m24) | [§3.1.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Convert transcript distinguishability to prediction by the clean held-out experiment in [Individual measurements §3](../science/individual_measurements.md#3-from-clean-prediction-to-transcript-distinguishability). |
| <a id="m25"></a>[M25: coherent prediction as a test](MILESTONES.md#m25) | [§§2.2.1–2.2.2, 2.3.1–2.3.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf); [§3.1.1, Theorem 3.4](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Form the project-specific test states and $`X_T`$ in [Collective statistics §1](../science/collective_statistics.md#1-reduction-of-arbitrary-prediction-to-a-binary-state-test). |
| <a id="m26"></a>[M26: collective prediction converse](MILESTONES.md#m26) | [§§1.1.2–1.1.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf); [§3.1.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Evaluate equal/opposite Pauli contributions before applying the norm inequality in [Collective statistics §2](../science/collective_statistics.md#2-exact-second-moment-and-the-prediction-converse). |
| <a id="m27"></a>[M27: matching collective upper bound](MILESTONES.md#m27) | [§3.1.2 and §§3.2–3.2.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Add the three-case fidelity calculation and Cheng's research-level error bound in [Collective statistics §§3–4](../science/collective_statistics.md). |
| <a id="m28"></a>[M28: exact LPN source simulation](MILESTONES.md#m28) | [§§2.1.2–2.1.3, 2.2.1–2.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf) | The hidden-variable independence, Clifford prior, and null experiment are proved in [H1, steps 1–3](../science/computational_hardness.md). |
| <a id="m29"></a>[M29: one prediction distinguishes LPN](MILESTONES.md#m29) | [§1.2.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.1.pdf); [§§2.3.1–2.3.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf); [§3.1.1](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | The noisy held-out agreement and polynomial reduction are in [H1, steps 4–5](../science/computational_hardness.md#4-turning-one-prediction-into-a-distinguisher). |
| <a id="m30"></a>[M30: combined separation](MILESTONES.md#m30) | [§§2.1–2.3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf); [§§3.1–3.2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf) | Combine the canonical results in [Model](../science/model.md) and [Interpretation](../science/interpretation.md); keep the [local-prior variant](../science/local_prior.md) a separately quantified comparison. |

The bridge's endpoint is understanding how the theorem package fits together. Exact constants, all-target versus average guarantees, and proof details remain authoritative in the linked science chapters. The anchor explains the foundations; it does not turn a statistical measurement construction into an efficient algorithm or turn a conditional hardness statement into an unconditional one.
