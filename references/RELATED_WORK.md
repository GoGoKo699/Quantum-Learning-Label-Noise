# Related work and attribution

This document identifies the mechanisms used in this project and the limits of its comparison with prior work. The literature check includes primary sources available on 22 October 2026. Theorem and equation numbers refer to the explicitly identified versions below. Bibliographic records are in [references.bib](references.bib).

## Scope of the contribution

The [model](../science/model.md) supplies independent quantum specimens with a classical label. For a hidden signed Pauli observable $`P`$, the clean conditional states are

```math
\rho^0_{y,P}=\frac{I+yP}{2^n}.
```

Independent annotation errors change the observed label from $`Y`$ to $`C=YE`$, with $`\Pr(E=-1)=\eta`$. Thus the state conditional on the recorded label is $`(I+C\gamma P)/2^n`$, where $`\gamma=1-2\eta`$. The objective is to predict the clean label of a fresh quantum specimen.

The contribution investigated here is a conjunction within this single source and prediction objective: efficient clean-label learning, a copy advantage from coherent processing, conditional computational hardness after constant annotation noise, and a characterization of unrestricted collective prediction sample complexity. Neither the general usefulness of quantum memory nor noisy-parity hardness is introduced here. The computational statement is conditional on quantum hardness of ordinary decision-LPN with classical samples; it is not an unconditional lower bound on quantum computation.

| Ingredient | Prior mechanism being used | Project-specific calculation or reduction |
| --- | --- | --- |
| Bell measurements | Pauli second moments and two-copy learning in [HKP](#hkp2021) | The exact labeled transcript is an affine parity equation whose noise contrast is $`\gamma^2`$. |
| Individual-example measurement lower bounds | Adaptive measurement trees and Pauli second moments in [CCHL](#cchl2021) | Their method is adapted to fresh-input classification and to the stated source priors. |
| Annotation-noise hardness | Classical parity/LPN embeddings, including [GL](#gl2022) and the special-case reductions in [PQS](#pqs2026) | An ordinary decision-LPN reduction covers arbitrary efficiently usable quantum prediction models. |
| Collective upper bound | Ensemble discrimination and pretty-good measurements in [Barnum–Knill](#barnum-knill2002) and [Cheng et al.](#cheng2024) | Pairwise fidelities of the labeled Pauli states give the sample bound. |
| Prediction lower bound | Binary state discrimination and operator norm inequalities | The average training-and-test discrimination operator is evaluated directly, without requiring the learner to identify $`P`$. |
| Clifford randomization | Efficient Clifford indexing and sampling in [Koenig–Smolin](#ks2014) | Randomization transfers the reduction to the specified Pauli prior. |

This attribution map describes the claims proved in the accompanying chapters. It does not establish a priority claim over every possible reformulation of earlier results.

## Quantum memory and Pauli measurements

<a id="cchl2021"></a>
### CCHL: learning with and without quantum memory

**Sitan Chen, Jordan Cotler, Hsin-Yuan Huang, and Jerry Li.** *Exponential Separations Between Learning With and Without Quantum Memory.* FOCS 2021 proceedings, pp. 574–585, published 2022. [DOI: 10.1109/FOCS52979.2021.00063](https://doi.org/10.1109/FOCS52979.2021.00063). Expanded version: [arXiv:2111.05881v2](https://arxiv.org/html/2111.05881v2), 18 November 2021.

**Source statement.** Section 4.4 defines the access models. Theorem 5.5 gives a shadow-tomography lower bound through an observable second-moment parameter. Lemma 5.8 and Corollary 5.9 specialize it to Paulis, obtaining an exponential single-copy sample requirement even for adaptive measurements. The proof uses alternatives of the form $`(I+3\varepsilon O_x)/2^n`$. Section 6 studies bounded quantum memory.

**Use here.** The adaptive-tree representation, signed-observable averaging, and second-moment strategy are imported. The [individual-measurement proof](../science/individual_measurements.md) adapts the resulting distinction bound to fresh-specimen prediction and evaluates it for the local preparation prior. The existence of an exponential Pauli memory advantage is prior work. Section 5.1.3 concerns a classical-memory upper bound; it should not be cited as the Bell-measurement construction.

<a id="hkp2021"></a>
### HKP: information-theoretic quantum learning advantage

**Hsin-Yuan Huang, Richard Kueng, and John Preskill.** *Information-Theoretic Bounds on Quantum Advantage in Machine Learning.* Physical Review Letters **126**, 190505 (2021). [DOI: 10.1103/PhysRevLett.126.190505](https://doi.org/10.1103/PhysRevLett.126.190505). [arXiv:2101.02464v2](https://arxiv.org/html/2101.02464v2), 2 April 2021.

**Source statement.** Appendix E.2 constructs the Pauli-learning protocol using Bell measurements for magnitudes and a subsequent sign-learning step. The paper also proves an average-prediction comparison in Theorem 1 for classical descriptors $`x`$, a known output observable, and queries to an unknown process.

**Comparison.** The Bell second-moment identity is established machinery. This project's test input is an unknown quantum specimen, with no classical descriptor revealing its latent preparation. Consequently, its average classification error is not the function-prediction objective of Theorem 1. The comparison must retain this difference in deployment access; an average-error exponential gap should not be presented as contradicting that theorem.

<a id="cgy2024"></a>
### CGY: precision and memory tradeoffs

**Sitan Chen, Weiyuan Gong, and Qi Ye.** *Optimal Tradeoffs for Estimating Pauli Observables.* FOCS 2024, pp. 1086–1105. [DOI: 10.1109/FOCS61266.2024.00072](https://doi.org/10.1109/FOCS61266.2024.00072). [arXiv:2404.19105v2](https://arxiv.org/abs/2404.19105v2), 15 November 2024; [full text](https://arxiv.org/pdf/2404.19105).

**Source statement.** Theorem 1 characterizes Pauli shadow-tomography sample complexity for specified measurement families, up to logarithmic factors. Theorems 5 and 6, with the detailed bound in Theorem 17, establish precision and memory tradeoffs beyond a fixed Bell protocol. For example, the stated $`c`$-copy lower bound under $`\varepsilon<1/c`$ contains $`\Omega(\min\{2^n/(c\varepsilon^2),1/(c^3\varepsilon^4)\})`$.

**Comparison.** An inverse-fourth-power Bell cost is not itself a new measurement limitation. The project separately permits a joint measurement on all training copies for its unrestricted collective bound. One cannot apply a bounded-block precision theorem outside its hypotheses to rule out that measurement, or describe the Bell cost as optimal among all collective learners.

<a id="kgkb2025"></a>
### King–Gosset–Kothari–Babbush: efficient Pauli-query retrieval

**Robbie King, David Gosset, Robin Kothari, and Ryan Babbush.** *Triply Efficient Shadow Tomography.* PRX Quantum **6**, 010336 (2025). [DOI: 10.1103/PRXQuantum.6.010336](https://doi.org/10.1103/PRXQuantum.6.010336). [arXiv:2404.19211v1](https://arxiv.org/html/2404.19211v1), 30 April 2024.

**Source statement.** The paper combines Bell measurements and commutation-graph methods. Its efficiency definition allows polynomial dependence on the number of requested observables. Corollary 12 constructs a polynomial-size representation with polynomial-time Pauli-query retrieval, using polynomially many copies and $`2^{O(n)}`$ preprocessing time. Section 3.1 states the exponential dependence of the all-Pauli construction explicitly.

**Comparison.** A compact answer to a supplied Pauli query does not provide a polynomial-time search algorithm for an unknown Pauli. The all-Pauli family has $`4^n`$ members. These algorithms therefore do not supply an efficient noisy decoder or a classifier for an undescribed fresh quantum specimen in this project.

## Noise, parity, and computational hardness

<a id="gl2022"></a>
### GL: noisy PAC learning from classical measurement records

**Aravind Gollakota and Daniel Liang.** *On the Hardness of PAC-learning Stabilizer States with Noise.* Quantum **6**, 640 (2022). [Publisher and DOI: 10.22331/q-2022-02-02-640](https://quantum-journal.org/papers/q-2022-02-02-640/). [arXiv:2102.05174v3](https://arxiv.org/html/2102.05174v3), 31 January 2022.

**Source statement.** Definition 2.1 supplies classical descriptions of measurements and their outcomes for an unknown fixed state. It permits an output state $`\sigma`$ without requiring $`\sigma`$ to be a stabilizer state. Proposition 4.10 identifies computational-basis states under parity measurements with parity learning. Corollary 4.12 transfers LPN hardness to noisy PAC learning under the uniform parity-measurement distribution.

**Comparison.** The noisy-parity mechanism is close prior art. Allowing an improper hypothesis is not, by itself, a distinction from this work. The present reduction changes the operational input to quantum specimens, permits coherent training, and targets clean-label prediction on a fresh quantum input. Its scope is demonstrated by the reduction in [computational_hardness.md](../science/computational_hardness.md), rather than inferred merely from a hidden-Pauli identification problem.

<a id="pqs2026"></a>
### PQS: Learning Stabilizers with Noise

**Alexander Poremba, Yihui Quek, and Peter Shor.** *The Learning Stabilizers with Noise Problem.* ITCS 2026, LIPIcs **362**, 108:1–108:19. [DOI and proceedings](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2026.108). The following locators refer to the extended [arXiv:2410.18953v5](https://arxiv.org/html/2410.18953v5), 14 April 2025, not the shorter proceedings numbering.

**Source statement.** Section 4 introduces LSN and its multi-shot variant. Theorems 5.2–5.3 reduce LPN to specified variants with bit-flip noise and matrix-multiplication Clifford encoders. They should not be silently read as reductions to every random-code/depolarizing-noise formulation. Definition 9.1 and Theorem 9.3 give a sample-versus-time separation for proper learning of state-preparation processes, conditional on multi-shot LSN hardness.

**Comparison.** Quantum-data learning with a statistical/computational separation is already present. Here the computational assumption is ordinary classical-sample decision-LPN, and the output task is binary quantum-input prediction, including efficiently usable improper or consumable quantum models. The same source also supports the clean/noisy and individual/coherent comparisons.

<a id="css2015"></a>
<a id="cross2015"></a>
### Cross–Smith–Smolin: noisy coherent parity examples

**Andrew W. Cross, Graeme Smith, and John A. Smolin.** *Quantum learning robust against noise.* Physical Review A **92**, 012327 (2015). [DOI: 10.1103/PhysRevA.92.012327](https://doi.org/10.1103/PhysRevA.92.012327). The preprint is titled *Quantum learning robust to noise*: [arXiv:1407.5088v1](https://arxiv.org/html/1407.5088v1), 18 July 2014.

**Source statement.** Section II, Eq. (2), gives the coherent example $`2^{-n/2}\sum_x|x,f(x)\rangle`$. Section IV proves efficient parity learning with noisy versions of this access, including depolarizing noise, while dephased classical examples lead to LPN.

**Comparison.** The ordinary LPN assumption here supplies classical samples. Encoding each sampled pair into a quantum register does not create a coherent superposition over all examples. Nor do independent quantum specimens supply a reusable preparation unitary or coherent example oracle. The positive result therefore concerns stronger source access than the assumption used by this project's reduction.

<a id="cghq2025"></a>
### CGHQ: low-degree evidence for information–computation gaps

**Sitan Chen, Weiyuan Gong, Jonas Haferkamp, and Yihui Quek.** *Information-Computation Gaps in Quantum Learning via Low-Degree Likelihood.* [arXiv:2505.22743v2](https://arxiv.org/html/2505.22743v2), 17 June 2025. [DOI: 10.48550/arXiv.2505.22743](https://doi.org/10.48550/arXiv.2505.22743).

**Source statement.** Section 8.3 studies Gibbs states of sparse nonlocal Hamiltonians. Section 10.1, Theorem 10.1, proves low-degree hardness for an average-case LSN model, including a restriction on how measurements depend on the classical input. The authors explain that their low-degree obstruction also occurs without noise, when algebraic algorithms can succeed.

**Comparison.** This is substantial prior evidence for quantum statistical/computational gaps, including Pauli and noisy-stabilizer settings. The present conditional reduction addresses all polynomial-time quantum predictors under decision-LPN, rather than a low-degree family. The one-Pauli density matrix can also be expressed as a Gibbs state, but that algebraic observation would not establish a new result about geometrically local thermal systems.

<a id="noisy-learning2026"></a>
### Cotler–Gong–Kannan: noise at the quantum interface

**Jordan Cotler, Weiyuan Gong, and Ishaan Kannan.** *Noisy quantum learning theory.* Nature Communications **17**, 6979 (2026). [DOI: 10.1038/s41467-026-73693-x](https://doi.org/10.1038/s41467-026-73693-x). [arXiv:2512.10929v2](https://arxiv.org/html/2512.10929v2), 14 January 2026.

**Source statement.** The paper models noisy access to uncharacterized quantum systems. Section 2.3 and Appendix F analyze noisy Pauli shadow tomography and the decision problem with states $`(I+P)/2^n`$. Local depolarization can remove an exponential sample advantage; Appendix F gives memory-dependent lower bounds and algorithms.

**Comparison.** The project changes a classical annotation bit while holding specimen preparation and quantum operations ideal. This preserves a constant conditional Pauli contrast for constant $`\eta<1/2`$. Local noise on every feature qubit can instead attenuate a weight-$`w`$ Pauli by a factor exponential in $`w`$. The present result therefore does not establish robustness to that physical noise model.

## Recent structure-learning algorithms

<a id="tang-steckmann2026"></a>
### Tang–Steckmann: noisy stabilizer structure

**Letian Tang and Thomas Steckmann.** *Learning Noise-Robust Stabilizer Structure via Bell Sampling.* [arXiv:2610.03307v2](https://arxiv.org/html/2610.03307v2), 5 October 2026. [DOI: 10.48550/arXiv.2610.03307](https://doi.org/10.48550/arXiv.2610.03307).

**Source statement.** Problem II.1 assumes copies of a Pauli-noisy image of one underlying pure state with bounded stabilizer nullity. Its output is a commuting approximate weak-stabilizer group, with an absolute projected-purity-loss criterion. Section IV.3 treats degeneracies from maximally mixed factors; the centralizer of a mixed state's Pauli support need not commute.

**Comparison.** For the source here, a Clifford frame gives

```math
U\rho_{C,P,\gamma}U^\dagger=\frac{I+C\gamma Z}{2}\otimes\left(\frac I2\right)^{\otimes(n-1)},
\qquad \mathrm{tr}(\rho_{C,P,\gamma}^2)=\frac{1+\gamma^2}{2^n}.
```

Thus it contains many maximally mixed factors, and retaining a constant absolute amount of purity is not the classification guarantee required here. There is also a direct noise-strength check: if this state were a Pauli-noisy image of a pure target with total error probability $`\lambda`$, positivity of the no-error contribution would imply $`1-\lambda\leq\lambda_{\max}(\rho)=(1+\gamma)/2^n`$. Its required total error probability is therefore close to one. This comparison checks the source promises; it does not assert that the cited algorithms fail on every mixed input.

<a id="haug2026"></a>
### Haug: Clifford-scrambled product states

**Tobias Haug.** *Efficient Learning of Clifford-Scrambled Product States.* [arXiv:2609.27128v1](https://arxiv.org/html/2609.27128v1), 22 September 2026. [DOI: 10.48550/arXiv.2609.27128](https://doi.org/10.48550/arXiv.2609.27128).

**Source statement.** Equation (3) defines a class of pure states obtained by applying a Clifford to pure product blocks. Theorem 4 gives efficient approximate learning under the stated block-size and stabilizer-gap conditions. Appendix F.3 explicitly keeps the original input exactly pure and identifies arbitrary noisy inputs as requiring an additional stability argument.

**Comparison.** Each specimen in the local realization of this project can be a pure product stabilizer state, but different examples use independent hidden preparation bits. The learner receives samples from a class-conditional mixture, not repeated copies of one unknown pure product state. Efficiently learning a fixed pure Clifford-scrambled state therefore does not furnish an efficient learner for this source.

## Standard tools used in the proofs

<a id="ks2014"></a>
### Koenig–Smolin: efficient Clifford selection

**Robert Koenig and John A. Smolin.** *How to efficiently select an arbitrary Clifford group element.* Journal of Mathematical Physics **55**, 122202 (2014). [DOI: 10.1063/1.4903507](https://doi.org/10.1063/1.4903507). [arXiv:1406.2170v1](https://arxiv.org/abs/1406.2170v1), 9 June 2014.

The paper gives an $`O(n^3)`$-operation indexing algorithm and symplectic-transvection factorization, supporting efficient selection of random Clifford elements. This is a standard implementation ingredient for the reduction's randomization. It does not grant the learner knowledge of the hidden source basis or oracle access to source preparation.

<a id="barnum-knill2002"></a>
<a id="bk2002"></a>
### Barnum–Knill: pretty-good discrimination

**Howard Barnum and Emanuel Knill.** *Reversing quantum dynamics with near-optimal quantum and classical fidelity.* Journal of Mathematical Physics **43**, 2097–2106 (2002). [DOI: 10.1063/1.1459754](https://doi.org/10.1063/1.1459754). Corrected manuscript: [arXiv:quant-ph/0004088v2](https://arxiv.org/html/quant-ph/0004088v2), 18 January 2026.

Section V relates the reversal construction to the pretty-good measurement for arbitrary state ensembles. Theorem 5 bounds discrimination performance using pairwise fidelities. The arXiv revision corrects a proof issue concerning ensembles with more than one density matrix. This project uses established discrimination machinery; it does not claim the pretty-good measurement or its pairwise bound as a new result.

<a id="cheng2024"></a>
<a id="cheng2025"></a>
### Cheng et al.: sample complexity of hypothesis testing

**Hao-Chung Cheng, Nilanjana Datta, Nana Liu, Theshani Nuradha, Robert Salzmann, and Mark M. Wilde.** *An invitation to the sample complexity of quantum hypothesis testing.* npj Quantum Information **11**, 94 (2025). [DOI: 10.1038/s41534-025-00980-8](https://doi.org/10.1038/s41534-025-00980-8). Proof locators here use [arXiv:2403.17868v2](https://arxiv.org/html/2403.17868v2), 26 April 2024.

Theorem 11 and Appendix J, Eqs. (206)–(213), give the operative ensemble-discrimination bound. Writing root fidelity as $`f(\rho,\sigma)=\|\sqrt\rho\sqrt\sigma\|_1`$, it yields

```math
p_{\rm err}^{\rm PGM}\leq\sum_{i\ne j}\sqrt{p_i p_j}\,f(\rho_i,\rho_j).
```

Their $`F`$ is squared fidelity, so their $`\sqrt F`$ is the $`f`$ above. For tensor powers, $`f`$ is multiplicative. The [collective-statistics proof](../science/collective_statistics.md) uses this information-theoretic measurement bound. It does not, without further analysis of the ensemble and its representation, establish a polynomial-time implementation.

## Interpretation boundaries

The comparisons above depend on three distinctions that should remain explicit in summaries of this project:

1. **Sample availability and source access.** Independent specimens, classical preparation descriptions, and coherent example oracles are different resources. Efficient preparation by the source does not reveal its hidden random choices to the learner.
2. **Training and prediction objectives.** Identifying an unknown state, answering a supplied Pauli query, and classifying an undescribed fresh quantum specimen have different success criteria. The prediction lower bounds must be proved for prediction itself.
3. **Statistical and computational efficiency.** A polynomial number of copies, a compact hypothesis, or an existing collective POVM does not by itself give a polynomial-time learner. Conversely, the LPN-based computational result remains an explicit assumption-dependent statement.

These boundaries are part of the model and proofs, rather than empirical claims about all quantum learning algorithms or all noise processes.
