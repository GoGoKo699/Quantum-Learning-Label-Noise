# What the separation means

The central distinction is between the amount of data a learning task needs and the amount of computation needed to use that data. In this model, random errors in the training annotations preserve the optimal collective sample complexity up to a noise-dependent factor. Under an explicit hardness assumption, the same errors remove the efficient learner available with correct annotations.

All statements refer to the direct specimen interface and clean prediction task in [Model](model.md). They concern an idealized mathematical source with independent annotation flips. They do not estimate the performance of a particular experimental device or a general machine-learning workload.

## 1. One task, three resource questions

The target is a hidden signed Pauli measurement on $`n`$ qubits. A clean positive specimen lies in its positive eigenspace, a clean negative specimen in its negative eigenspace. Training labels are flipped independently with rate $`\eta`$, and $`\gamma=1-2\eta>0`$ is the remaining correlation with the clean label. The test label is clean.

The following results use a fixed average prediction advantage $`a\in(0,1/2)`$ and the signed-uniform target prior. Constants can depend on that fixed advantage.

| Question | Answer | Meaning of the guarantee |
|---|---|---|
| How many examples suffice if arbitrary coherent computation is allowed? | $`\Theta(n/\gamma^2)`$ | A matching prediction lower bound and a collective identification construction; no efficient implementation of that construction is asserted. |
| How many examples are necessary if training examples are measured separately? | $`\Omega(2^n/\gamma^2)`$ | Arbitrary adaptive POVMs and unlimited classical computation are allowed, but quantum memory cannot persist between examples. |
| Can coherent training be efficient with correct labels? | Yes: $`O(n)`$ examples and polynomial time | Bell measurements yield exact binary linear constraints. |
| Can coherent training be efficient at a fixed positive noise rate? | No nonnegligible advantage under the stated quantum decision-LPN assumption | The reduction covers arbitrary coherent processing and consumable quantum models. |

The first two rows establish an exponential sample advantage at every fixed $`\eta<1/2`$. The last two distinguish the computational accessibility of that advantage. The noisy collective measurement is an existence proof at the statistical level; the conditional computational theorem explains why implementing a successful learner efficiently would resolve a hard noisy-parity problem.

This comparison does not identify an unconditional separation between efficient classical and quantum computation. The individual-example baseline already performs arbitrary quantum measurements within each example, and its limitation is the absence of coherent memory across examples. The runtime obstruction assumes quantum hardness of ordinary decision-LPN.

## 2. What Bell measurements reveal

A Bell measurement on a pair of independently drawn specimens turns their quantum correlation into a classical parity equation. If the target is $`P=\sigma W_p`$, the exact relation is

```math
R=(-1)^{q(p)+[p,Z]}F,
\qquad Z\sim\operatorname{Unif}(\mathbb F_2^{2n}),
\qquad \mathbb E F=\gamma^2.
```

Here $`R`$ is the product of the two recorded signs and $`q(p)`$ is the transposition phase. The global sign $`\sigma`$ disappears when two copies are paired and is calibrated separately. The derivation and algorithms are in [Bell learning](bell_learning.md).

At $`\eta=0`$, the equations are exact. A linear number of pairs supplies enough independent equations to recover the unsigned target by Gaussian elimination. Annotation errors turn those same equations into affine noisy parity with error rate

```math
\eta_B=2\eta(1-\eta),
\qquad 1-2\eta_B=\gamma^2.
```

This explains the computational change in the explicit Bell algorithm. It does not alone rule out a different efficient quantum learner. The separate reduction in [Computational hardness](computational_hardness.md) is what excludes every efficient learner under the assumption.

The elementary Bell decoder based on exhaustive correlation search uses $`O(n/\gamma^4)`$ pairs at fixed confidence. This is a property of that protocol. The optimal unrestricted collective rate is $`\Theta(n/\gamma^2)`$. No claim here makes the Bell protocol optimal among all two-example measurements or all bounded-memory strategies. The broader precision–memory tradeoffs belong to the literature reviewed in [Related work](../references/RELATED_WORK.md#cgy2024).

## 3. Product data can still reward coherent acquisition

The explicit [source preparation](source_preparation.md) prepares a pure product vector on every realized draw, using only local basis rotations and classical parity. The task therefore does not require entangled data, expensive generic state loading, or a QRAM oracle.

For each fixed $`P`$, the two class density operators commute. Across possible hidden targets, however, the relevant Pauli observables do not all commute. A learner must acquire information before it knows which observable will matter. Bell measurements extract target-dependent relations from pairs without first choosing the hidden single-example basis. This is the operational origin of the memory advantage, consistent with the established Pauli-ensemble quantum-learning results [CCHL2021](../references/RELATED_WORK.md#cchl2021).

An individual-example learner cannot retain the unmeasured quantum information for comparison with later examples. Even an arbitrary POVM and unlimited classical processing leave the exponential lower bound intact. The [individual-measurement proof](individual_measurements.md) quantifies this information loss through an exact Pauli second moment and a bound on adaptive transcript distributions.

The word “collective” refers to processing multiple examples coherently. It does not imply that an optimal learner must hold all examples simultaneously. The clean construction requires coherent access to two feature registers at a time, together with ordinary classical storage. The statistical upper bound permits general collective processing and does not supply an efficient memory or gate implementation.

## 4. Label noise does not change the population-optimal target

For any fixed classifier evaluated on an independent example, let $`R_0`$ be its clean error probability and $`R_\eta`$ its disagreement probability with an independently flipped annotation. Then

```math
R_\eta=\eta+(1-2\eta)R_0=\eta+\gamma R_0.
```

Since $`\gamma>0`$, minimizing the noisy-label population risk selects the same classifiers as minimizing clean risk. The target remains a simple product Pauli measurement and the clean Bayes error remains zero.

The hard part is finding that target from finite noisy observations with feasible computation. A population objective can preserve its minimizer while the task of obtaining useful information about that minimizer becomes computationally difficult. The reduction proves this for the full quantum learning procedure, without requiring a particular loss function, optimization method, or variational circuit.

There is consequently no barren-plateau claim here. Neither the statistical lower bounds nor the computational reduction concern the gradient of a specified parametrized circuit. They constrain learning through the information supplied and the computation allowed.

## 5. Noise regimes and limits

At zero annotation noise, the efficient Bell algorithm applies. At a fixed positive noise rate where the quantum decision-LPN assumption holds, H1 rules out nonnegligible average advantage for polynomial-time learners using polynomially many examples.

These statements do not create a discontinuous hardness theorem at every nonzero noise rate. The clean-batch algorithm in [Bell learning](bell_learning.md#vanishing-noise-a-clean-batch-algorithm) has cost

```math
\exp(O(\eta n))\,
\operatorname{poly}(n,\gamma^{-1},\log(1/\delta)).
```

It is polynomial when $`\eta=O(\log n/n)`$. It is an elementary noisy-parity strategy, not a sharp threshold result. Intermediate noise scalings and the best possible runtime across all regimes remain outside the proved classification.

As $`\eta\to1/2`$, the contrast tends to zero and both statistical bounds become more demanding. At the excluded endpoint $`\eta=1/2`$,

```math
\tau_{P,0}=I_D/D
```

for every target. The entire training set is then independent of $`P`$, and sign symmetry gives zero average clean prediction advantage for any sample count. The endpoint is an information-theoretic failure, regardless of computational power.

## 6. A limited thermal interpretation

For $`0\leq\gamma<1`$, put $`\beta=\operatorname{artanh}\gamma`$. The state conditioned on a recorded label can be written

```math
\rho_{C,P,\gamma}
=\frac{e^{\beta CP}}{\operatorname{Tr}(e^{\beta CP})}.
```

This follows from $`P^2=I`$ and $`e^{\beta CP}=\cosh\beta\,I+C\sinh\beta\,P`$. Its two eigenvalues are $`(1-\eta)/2^{n-1}`$ and $`\eta/2^{n-1}`$, each with multiplicity $`2^{n-1}`$, so its entropy in bits is

```math
S(\rho_{C,P,\gamma})=n-1+h_2(\eta),
```

where $`h_2`$ is the binary entropy. The formula extends continuously to zero noise and the half-noise endpoint.

This is a useful algebraic representation of the observer's conditional state. The physical source has not been heated: it prepares the same product vectors before corrupting the classical annotation. Furthermore, $`P`$ can have extensive support, so a one-term Hamiltonian proportional to $`P`$ need not be geometrically local. The thermal representation adds no claim about laboratory thermalization or efficient general Hamiltonian learning.

## 7. Scope of the combined result

The source is highly structured, the prior is explicit, and the classification task is average-case. The scientific statement is a controlled example in which three questions can be answered for the same data interface: optimal collective sample complexity, an exponential individual-measurement obstruction, and conditional computational hardness after annotation corruption.

The component techniques have important antecedents: Pauli quantum-memory separations, Bell sampling, pretty-good measurement bounds, noisy-parity reductions, and adaptive learning trees. [Related work](../references/RELATED_WORK.md) gives theorem-level comparisons and source versions. The contribution is the joint account under one fixed supervised source, with a clean test task and a hardness reduction that permits arbitrary quantum predictions. The repository does not assert an exhaustive priority claim or infer general practical quantum advantage from this construction.

The [local-prior variant](local_prior.md) makes the reduction itself local at the cost of a different prior and a smaller exponential individual-measurement bound. It is a supplementary comparison, separate from the main signed-uniform theorem.
