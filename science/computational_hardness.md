# Computational hardness from classical noisy parity

An efficient predictor for the noisy quantum task would distinguish ordinary classical learning-parity-with-noise samples from independent random bits. The reduction prepares each supplied quantum example using only a classical LPN sample, a fresh random annotation bit, and a randomly chosen Clifford circuit. It does not need the unknown parity secret.

The reduction tests the learner through one fresh prediction. It therefore applies to a learner that retains an arbitrary quantum model, returns no explicit Pauli description, and consumes its model during that prediction. The resulting hardness statement is conditional on a quantum computational assumption for classical LPN.

## The decision-LPN assumption

Fix a constant $`\eta\in(0,1/2)`$. In dimension $`k`$, consider two classical sampling experiments.

**LPN experiment.** Draw one hidden secret $`S\sim\mathrm{Unif}(\mathbb F_2^k)`$. Each sample is

```math
(X,B),
\qquad
X\sim\mathrm{Unif}(\mathbb F_2^k),
\qquad
B=S\cdot X+e\pmod2,
\qquad
e\sim\mathrm{Bernoulli}(\eta).
```

The covariates and noise bits are independent across samples, conditioned on $`S`$.

**Uniform experiment.** Each sample $`(X,B)`$ is independent and uniform in $`\mathbb F_2^{k+1}`$.

A distinguisher receives polynomially many such **classical** samples and may process them with a quantum computer. Its distinguishing advantage is

```math
\mathrm{Adv}_{\mathrm{LPN}}(D;k,\eta)
=\left|
\Pr(D\text{ accepts in the LPN experiment})
-\Pr(D\text{ accepts in the uniform experiment})
\right|.
```

The assumption used here is:

> For this fixed noise rate, every uniform quantum polynomial-time distinguisher using polynomially many classical samples has negligible distinguishing advantage as $`k\to\infty`$.

A function is negligible if it is eventually smaller than the reciprocal of every positive polynomial. The noise rate may be known to the distinguisher and to the learner. If one instead chooses a nonuniform circuit model, the corresponding nonuniform quantum-LPN assumption is required; no change of uniformity convention is implicit.

This is an assumption about quantum computation on classical LPN data. It is stronger than merely assuming that classical algorithms cannot solve LPN. It supplies no coherent access to the example-generation procedure, no quantum superposition of examples, and no access to the hidden noise bits. Coherent quantum examples can change noisy-parity learnability, as illustrated by [Cross, Smith, and Smolin](../references/RELATED_WORK.md#css2015); those are different inputs from the samples assumed here.

## H1 — Hardness of single-test prediction

**Theorem H1.** Assume quantum decision-LPN hardness at a fixed $`\eta\in(0,1/2)`$ as above, and set $`\gamma=1-2\eta`$. In the supervised model of [model.md](model.md), every uniform quantum polynomial-time learner, using polynomially many training specimens and polynomial total training-and-prediction time, has negligible average clean prediction advantage under the uniform signed-Pauli target prior.

The learner may use arbitrary coherent training, retain a quantum model, and consume it on the single test specimen. Its hypothesis need not be a Pauli measurement or a classical description.

More quantitatively, a learner on $`n`$ qubits with average clean advantage $`a_n`$ gives a decision-LPN test in dimension $`k=n-1`$ whose ideal distinguishing advantage is

```math
\gamma|a_n|.
```

The test uses the learner's training sample count plus one held-out LPN sample, with polynomial preparation overhead. A bounded-runtime implementation of uniform Clifford sampling changes this advantage by at most a negligible amount.

### 1. Randomizing the target

Let $`n=k+1`$, and draw an $`n`$-qubit Clifford operator $`U`$ uniformly, ignoring its physically irrelevant global phase. Choose it once for the entire experiment and keep its description from the learner. Uniform Clifford selection and circuit construction have efficient implementations; see [Koenig and Smolin](../references/RELATED_WORK.md#ks2014).

For a fixed parity secret $`s`$, define

```math
P_0(s)=Z^{(s,1)},
\qquad
P=UP_0(s)U^\dagger.
```

The last component of $`(s,1)`$ guarantees that $`P_0(s)`$ is nonidentity, including when $`s=0`$. The Clifford group acts transitively on the signed nonidentity Pauli operators. Transitivity on unsigned Paulis is the usual symplectic action; both signs occur because conjugation by an anticommuting Pauli reverses the sign. Uniformity on the finite group therefore makes $`P`$ uniform over all $`M=2(4^n-1)`$ signed nonidentity Paulis, for **every fixed** $`s`$.

The reduction does not compute $`P_0(s)`$ or $`P`$. They specify the hidden target induced by the samples and the chosen Clifford circuit.

### 2. Preparing a training example without the secret

For each available classical sample $`(x,b)`$, independently draw a uniform bit $`c`$. Prepare

```math
U|x,b\oplus c\rangle
```

and supply it to the learner with the recorded classical sign $`C=(-1)^c`$.

This preparation uses only the observed sample, the fresh bit, and the chosen circuit. In the LPN experiment, write $`b=s\cdot x\oplus e`$ and introduce the latent bit

```math
y=e\oplus c.
```

Because $`c`$ is independent and uniform, $`y`$ is uniform and independent of $`e`$. Explicitly,

```math
\Pr(y=u,e=v)=\frac12\Pr(e=v).
```

Also, $`x`$ is independent of both. The prepared vector becomes

```math
U|x,s\cdot x\oplus y\rangle.
```

Before the Clifford, it has $`P_0(s)`$ eigenvalue $`(-1)^y`$, since

```math
s\cdot x\oplus(s\cdot x\oplus y)=y.
```

As $`x`$ ranges uniformly over $`\mathbb F_2^k`$, these vectors form the computational basis of that eigenspace. Thus, conditioned on $`Y=(-1)^y`$, their average state is

```math
\begin{aligned}
\frac1{2^k}\sum_x
U|x,s\cdot x\oplus y\rangle
\langle x,s\cdot x\oplus y|U^\dagger
&=U\frac{I+YP_0(s)}{d}U^\dagger\\
&=\frac{I+YP}{d}.
\end{aligned}
```

Finally, $`c=y\oplus e`$, so the supplied sign obeys $`C=YE`$ with $`E=(-1)^e`$ independent of the clean label and feature specimen. This is precisely the independent random annotation-noise model.

One can also verify the entire conditional density directly. For each recorded bit $`c`$,

```math
\begin{aligned}
&\frac1{2^k}\sum_x\sum_{e=0}^1
\Pr(e)\,
U|x,s\cdot x\oplus e\oplus c\rangle
\langle x,s\cdot x\oplus e\oplus c|U^\dagger\\
&\hspace{4em}=\frac{I+(-1)^c\gamma P}{d}.
\end{aligned}
```

Including the classical annotation gives exactly

```math
\tau_{P,\gamma}
=\frac{I_D+\gamma Z_C\otimes P}{D}.
```

For fixed $`s,U`$, independent LPN samples and fresh independent bits $`c`$ give independent copies of this state. Their density operators depend on $`s,U`$ only through $`P`$. Therefore, conditioning merely on the induced target $`P`$ still gives exactly $`\tau_{P,\gamma}^{\otimes T}`$; the hidden common Clifford introduces no additional observable correlation beyond the common target.

### 3. What the uniform experiment produces

In the uniform experiment, $`x`$ and $`b`$ are independent and uniform. For either fixed value of $`c`$, the string $`(x,b\oplus c)`$ is uniform in $`\mathbb F_2^n`$. Hence its quantum state is $`I/d`$, before and after applying $`U`$, independently of the recorded annotation.

Every supplied annotated example is therefore

```math
\frac{I_D}{D}.
```

This holds for each fixed Clifford, so all training examples and the later test example are independent of their annotations even when the learner keeps quantum memory from training.

### 4. Turning one prediction into a distinguisher

Run the learner on its required number of simulated training examples. Obtain one fresh LPN sample and prepare one more example by the same rule, but withhold its recorded bit $`c`$. Supply only the feature register for the learner's prediction. Accept the LPN experiment if and only if

```math
\widehat Y=(-1)^c.
```

In the LPN experiment, the clean label and specimen of this held-out example have exactly the clean test distribution for the induced target. Its withheld annotation is independently flipped at rate $`\eta`$. The single-test identity from [model.md](model.md#a-single-test-identity) gives

```math
\begin{aligned}
\Pr(\text{accept}\mid\mathrm{LPN})
&=(1-\eta)\left(\frac12+a_n\right)
+\eta\left(\frac12-a_n\right)\\
&=\frac12+\gamma a_n.
\end{aligned}
```

The averaging here is exactly over the signed-uniform target prior because the random Clifford produces that prior for every original secret.

In the uniform experiment, the withheld bit is uniform and independent of the entire trained model and test feature. Any prediction therefore agrees with it with probability exactly one half:

```math
\Pr(\text{accept}\mid\mathrm{uniform})=\frac12.
```

The ideal distinguishing advantage is $`\gamma|a_n|`$. The decoder is invoked only once. No copy of the trained model, repeated query to it, or classical extraction of its effective measurement is involved.

### 5. Runtime and the hardness conclusion

Each example is prepared from an observed bit string with $`O(n)`$ basis-state preparation work followed by the same polynomial-size Clifford circuit. The reduction samples and stores that circuit once. If the learner uses $`T(n)`$ specimens, the reduction requests $`T(n)+1`$ LPN samples, performs polynomial work per sample, and then runs the learner and its one-test decoder. Polynomial training and inference cost therefore gives polynomial total reduction cost.

Exact sampling from a finite group whose order is not a power of two can use rejection sampling with polynomial expected cost. For a strict bounded-runtime quantum algorithm, the sampler can be truncated after a polynomial budget with negligible failure probability. On failure the distinguisher may output a fair coin. The resulting distribution differs from the ideal uniform-Clifford experiment by negligible total variation, so the acceptance probabilities above change by at most a negligible amount. This standard implementation detail leaves every nonnegligible distinguishing gap intact.

Since $`\eta`$ is a fixed constant below one half, $`\gamma>0`$ is a constant. A nonnegligible clean advantage $`a_n`$ would yield a nonnegligible distinguishing advantage in dimension $`k=n-1`$, contradicting the stated quantum decision-LPN assumption. This proves H1. ∎

## Why the source simulation covers the physical model

The simulation uses a Clifford-rotated computational-basis ensemble. Some realized vectors in that ensemble can be entangled. The same conditional density operators also admit the pure product preparation described in [Source preparation](source_preparation.md).

These descriptions are operationally identical under the stipulated access. For every target and sequence of recorded annotations, both preparations supply the same tensor product of conditional feature density operators. The learner receives one independently drawn specimen at a time and none of the ensemble's hidden classical preparation variables. By linearity of quantum probabilities, every joint processing strategy has the same outcome distribution on the two preparations.

Thus the reduction establishes hardness for the source specified in the model, including its implementation using pure product specimens. It does not assume that an entangled state has a distinguishable “product preparation label,” and it grants no way to request replicas of a particular hidden vector. Supplying such preparation information or replicas would define a different access model.

## The two computational reductions have different parameters

| Direction | Input | Output | Noise relation | What is preserved |
|---|---|---|---|---|
| H1 simulation | Classical LPN in dimension $`k`$ | Quantum supervised learning on $`n=k+1`$ qubits | Same $`\eta`$ | Any efficient clean predictor gives a distinguisher with gap $`\gamma\lvert a\rvert`$ |
| B1 Bell sensing | Quantum supervised learning on $`n`$ qubits | Classical affine noisy parity in dimension $`2n`$ | $`\eta_B=2\eta(1-\eta)`$ | An appropriate parity solver recovers the unsigned target; fresh calibration recovers its sign |

The first direction is the all-learner lower-bound reduction. The second supplies algorithms through a particular measurement and proves an exact data correspondence. Treating the Bell transcript as noisy parity alone would only show a barrier for decoders of that transcript; it would not rule out a different coherent quantum learner. H1 supplies that missing quantifier.

The hardness theorem applies at a fixed positive rate for which the quantum decision-LPN assumption is made. It does not prove hardness for every positive sequence $`\eta(n)`$. Indeed, the clean-batch algorithm in [Bell learning](bell_learning.md#vanishing-noise-a-clean-batch-algorithm) is polynomial when $`\eta=O(\log n/n)`$. Correct annotations admit the efficient algorithm K1 without a computational assumption.

## Relation to previous noisy quantum-learning hardness

LPN-based hardness already appears in noisy stabilizer learning. [Gollakota and Liang](../references/RELATED_WORK.md#gl2022) study PAC learning from measurement descriptions and noisy outcomes, including an LPN reduction. Their learning formulation permits a general output state, so allowing an improper output is not by itself a distinction from that work.

[Poremba, Quek, and Shor](../references/RELATED_WORK.md#pqs2026) study Learning Stabilizers with Noise and derive quantum-data learning consequences. The proper multi-shot learning formulation in their extended treatment has its own access and output requirements. These results establish earlier computational barriers for noisy quantum learning; the present theorem should be read with those antecedents in view.

The operational statement proved here concerns a balanced class-conditional Pauli source, classical annotation flips, and a fresh clean prediction task. It combines the exact simulation above with a test of one arbitrary quantum predictor. For this same source and target prior, [S1](collective_statistics.md) gives optimal collective sample complexity $`\Theta(n/\gamma^2)`$ and [S2](individual_measurements.md) gives the individual-example lower bound $`\Omega(2^n/\gamma^2)`$. At fixed positive noise, statistical sample advantage therefore survives even when efficient learning is ruled out by the specified computational assumption.

The ingredients and the closest operational comparisons are set out in [Related work](../references/RELATED_WORK.md). The theorem makes no unconditional assertion that LPN is hard for quantum computers and no claim that noisy annotations generically destroy quantum learning advantages.
