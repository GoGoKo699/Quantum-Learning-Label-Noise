# Learning this project

The central question is how the same learning task can require few quantum examples, many individually measured examples, and substantial computation once its annotations become unreliable. The learning route connects a concrete two-qubit example to the complete sample, memory, and time comparison.

## One educational anchor

The selected educational anchor is **John Watrous, *The Theory of Quantum Information* (Cambridge University Press, 2018)**. The [author's official page](https://cs.uwaterloo.ca/~watrous/TQI/) provides an authorized prepublication manuscript and errata. The freely accessible manuscript is distinct from the final typeset edition; it is linked here, not redistributed.

Use the relevant sections alongside the project's explanations. The route does not require reading the entire book first. Watrous supplies the mathematical foundations for states, measurements, discrimination, and fidelity. The local bridge supplies the Pauli, Bell, learning-theory, and noisy-parity steps needed for this particular problem.

| Reading need | Start here |
|---|---|
| A connected explanation of the task and why its resource requirements differ | [Tutorial](TUTORIAL.md) |
| Exact book sections, notation translation, and the derivations the book does not supply for this problem | [Watrous-to-project bridge](ANCHOR_BRIDGE.md) |
| The complete conceptual structure and dependencies | [30-milestone map](MILESTONES.md) |
| Formal assumptions and all canonical theorem statements | [Scientific model](../science/model.md) |
| Detailed proofs and numerical reproduction | [Scientific reading route](../README.md#read-the-scientific-account) and [verification](../verification/README.md) |

## A path from the example to the complete result

Begin with the [tutorial](TUTORIAL.md). Its two-qubit source makes the clean classification task concrete: each example is a product state, and a known product of local Pauli measurements predicts its label perfectly. Bell measurements then show why jointly processing independent examples can reveal a hidden parity. Corrupted annotations turn exact equations into noisy equations, making the distinction between enough information and efficient decoding unavoidable.

The map organizes the remaining ideas into exactly 30 understanding targets. Its first phase joins the background objects into a complete resource model; its second phase builds and combines the actual arguments.

| Milestones | Role in the story | Main scientific connection |
|---|---|---|
| [M01–M06](MILESTONES.md#m01) | Bits, Paulis, mixtures, measurements, prediction, and classical annotations | Establish what the data means and what the learner receives. |
| [M07–M10](MILESTONES.md#m07) | Clifford transformations, Bell measurements, random equations, and adaptive transcripts | Identify the constructions and classical statistical tools. |
| [M11–M14](MILESTONES.md#m11) | Quantum discrimination, the pretty-good measurement, LPN, and resource accounting | Assemble the framework for comparing specimen count, memory, and runtime. |
| [M15–M21](MILESTONES.md#m15) | Fixed source, product preparation, annotation noise, and Bell algorithms | Derive clean learning, noisy decoding, and a sufficient efficient regime for vanishing noise. |
| [M22–M24](MILESTONES.md#m22) | Pauli moment, adaptive clipping, and prediction reduction | Prove the exponential individual-example obstruction. |
| [M25–M27](MILESTONES.md#m25) | Helstrom prediction, exact second moment, and collective identification | Prove the matching collective sample bounds. |
| [M28–M30](MILESTONES.md#m28) | Exact LPN simulation, one held-out prediction, and synthesis | Explain the conditional all-quantum runtime barrier and the full separation. |

These targets describe the science rather than an assessment schedule. They remain the same for every reader. Detailed lemmas live in the scientific chapters, and the [bridge](ANCHOR_BRIDGE.md) maps the book's material onto the targets without replacing the project's structure with a textbook table of contents.

## Three distinctions to keep visible

**Preparation and access.** A source can prepare each specimen efficiently without revealing the preparation choices to the learner. Independent draws from a mixture differ from repeated copies of one fixed unknown pure state. The [source chapter](../science/source_preparation.md) makes this distinction explicit.

**Statistics and computation.** A collective POVM can be mathematically specified and need only a linear number of examples, while its implementation or decoder can still be expensive. The [collective-statistics proof](../science/collective_statistics.md) establishes data sufficiency; the [hardness reduction](../science/computational_hardness.md) constrains efficient use under its stated assumption.

**The proved task and nearby tasks.** The main results use a signed-uniform Pauli prior, independent classical annotation flips, ideal quantum operations, and one fresh clean quantum-input prediction. Primary research citations remain in [Related work](../references/RELATED_WORK.md) for attribution and proof dependencies. They are not additional educational anchors.
