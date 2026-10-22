# Label Noise Separates Quantum Sample Advantage from Efficient Learning

**Can a quantum learner retain an exponential sample advantage while losing its efficient training algorithm?** This repository gives a controlled example: learning a hidden Pauli measurement from labeled quantum specimens. Correct annotations allow polynomial-time learning from a linear number of examples. Independent annotation errors preserve the optimal collective sample complexity, but make efficient prediction hard under an explicit quantum learning-parity-with-noise assumption.

The source, hypothesis class, and clean test task stay fixed as the annotation error rate changes. Every supplied specimen can be a pure product state. The distinction is between the information available to a collective measurement and the computation needed to use it.

## The task

The hidden target $`P`$ is uniformly distributed over the signed nonidentity Pauli operators on $`n`$ qubits. A balanced clean label $`Y\in\{+1,-1\}`$ determines the feature state

```math
\rho^0_{Y,P}=\frac{I+YP}{2^n}.
```

The training annotation is independently flipped with probability $`\eta<1/2`$. Writing $`C`$ for the recorded sign and $`\gamma=1-2\eta`$, the conditional training state is

```math
\rho_{C,P,\gamma}=\frac{I+C\gamma P}{2^n}.
```

The learner receives one independently drawn specimen per example and its classical annotation. It must predict the clean label of one fresh specimen. It may retain an arbitrary quantum model and consume that model during the prediction. A known target is measured using local Pauli measurements, with zero clean error.

There is no coherent preparation oracle, classical description of a latent specimen, QRAM access, or repeated-copy access to a latent pure draw. Quantum operations are ideal; $`\eta`$ concerns annotations alone. The [model chapter](science/model.md) gives all quantifiers, priors, and resource definitions.

## Results at a glance

The sample bounds below concern any fixed positive average clean prediction advantage, with constants independent of $`n`$ and $`\gamma`$.

| Result | Training examples and computation | Precise statement and proof |
|---|---|---|
| **K1: efficient clean learning** | $`O(n)`$ examples and polynomial time at $`\eta=0`$ | [Bell pairs produce exact linear equations](science/bell_learning.md#k1--efficient-clean-learning); one extra example fixes the global sign. |
| **S1: optimal collective statistics** | $`\Theta(n/\gamma^2)`$ examples with unrestricted coherent processing | [Prediction converse and collective measurement](science/collective_statistics.md); the upper bound does not provide an efficient circuit. |
| **S2: individual-example obstruction** | $`\Omega(2^n/\gamma^2)`$ examples, even with unlimited classical computation | [Adaptive-measurement converse](science/individual_measurements.md); no quantum memory persists between examples. |
| **H1: conditional computational hardness** | No nonnegligible advantage from polynomial-time quantum learning with polynomially many examples at a fixed hard noise rate | [Reduction from ordinary classical decision-LPN](science/computational_hardness.md); arbitrary coherent training and consumable quantum models are included. |
| **B1: the Bell mechanism** | Bell observations are exactly affine noisy-parity data with contrast $`\gamma^2`$ | [Exact correspondence](science/bell_learning.md#b1--the-exact-bell-correspondence), with noise rate $`2\eta(1-\eta)`$. |

**The computational statement is conditional:** H1 assumes quantum polynomial-time hardness of decision-LPN supplied as ordinary classical samples at the specified fixed positive noise rate. It does not claim unconditional hardness or a sharp threshold at every nonzero noise rate. An explicit [clean-batch algorithm](science/bell_learning.md#vanishing-noise-a-clean-batch-algorithm) remains polynomial when $`\eta=O(\log n/n)`$.

The statistical separation concerns the same prediction accuracy and noise level on both sides. The individual-example baseline can choose arbitrary POVMs adaptively and retain unlimited classical information; its restriction is coherent memory between specimens. The optimal collective measurement may be computationally expensive.

## Read the scientific account

The main argument is distributed by topic. Each theorem has one canonical proof, and the model chapter indexes the statements.

| Question | Authoritative chapter |
|---|---|
| What exactly is supplied, predicted, and averaged? | [Model and canonical result index](science/model.md) |
| Can these states be supplied without entangled data or difficult state loading? | [Product-state source preparation](science/source_preparation.md), including a complete two-qubit example |
| Why does coherent pairing turn learning into parity solving? | [Bell learning](science/bell_learning.md), including clean, exhaustive noisy, and vanishing-noise algorithms |
| Why is $`n/\gamma^2`$ the optimal collective sample scaling for prediction itself? | [Collective statistical complexity](science/collective_statistics.md) |
| Why can unlimited classical processing fail to remove the sample gap? | [Individual-example measurement converse](science/individual_measurements.md) |
| Why does the computational barrier cover every efficient quantum predictor? | [Computational hardness](science/computational_hardness.md) |
| What physical and computational conclusions follow, and where do they stop? | [Interpretation](science/interpretation.md) |
| Can the hardness simulation itself use only local basis changes? | [A supplementary local-prior variant](science/local_prior.md), with a different prior and exponential base |
| Which ingredients are inherited from earlier work? | [Related work and theorem-level comparisons](references/RELATED_WORK.md), with [BibTeX records](references/references.bib) |

The Pauli-memory separation, Bell sampling, learning-tree method, noisy-parity mechanism, and pretty-good measurement bounds all have established antecedents. The account here joins them under one fixed supervised source, proves matching collective prediction complexity, and supplies a direct hardness reduction for a single quantum prediction. The [literature comparison](references/RELATED_WORK.md) distinguishes these ingredients and nearby access models; no exhaustive priority claim is made.

## Learning route

The selected educational anchor is **John Watrous, *The Theory of Quantum Information* (2018)**. The [learning guide](learning/README.md) connects its relevant material to this project through a [worked tutorial](learning/TUTORIAL.md), an [exact source-to-project bridge](learning/ANCHOR_BRIDGE.md), and the [30-milestone map](learning/MILESTONES.md). The bridge identifies the book sections, translates notation, and supplies the project-specific steps between quantum-information foundations and the learning result. The author's [official page](https://cs.uwaterloo.ca/~watrous/TQI/) provides an authorized prepublication manuscript.

The map's first 14 milestones connect the background objects into the learning framework. Its next 16 connect the source, algorithms, statistical converses, and computational reduction into the complete resource comparison. Each milestone states an understanding target, dependencies, conceptual connection, and source pointers. These are project-defined targets for any reader.

For a short first pass, begin with the [tutorial](learning/TUTORIAL.md), then read [the interpretation](science/interpretation.md). For a theorem-focused pass, begin with [the canonical result index](science/model.md#5-canonical-result-index). The [two-qubit source example](science/source_preparation.md#a-complete-two-qubit-example) and [exact Bell correspondence](science/bell_learning.md#b1--the-exact-bell-correspondence) provide direct entries into the constructions.

An LLM or other automated reader can use [llms.txt](llms.txt) to locate authoritative statements and preserve the model's important distinctions.

## Reproduce the finite checks

The analytic proofs hold for arbitrary problem size. The verification suite independently constructs small quantum states and measurements to check the normalization, phase conventions, reduction identities, and finite-dimensional statistical formulas.

```bash
python -m pip install -r verification/requirements.txt
python verification/run_all.py
```

The tested environment is Python 3.12 with NumPy 2.3.5. The scripts use deterministic seeds and report their case counts and numerical residuals. They also check local documentation links and the 30-milestone structure. See [verification details](verification/README.md) for exact coverage and [the recorded check output](verification/verified_results.json).

These checks support the mathematical account; they do not establish the LPN assumption, certify novelty, or benchmark a scalable quantum implementation.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).

The repository is distributed under the [MIT License](LICENSE).
