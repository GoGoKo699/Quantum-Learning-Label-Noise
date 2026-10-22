# Individual-example measurement converse

This chapter bounds clean-test prediction when the learner measures each training example individually and keeps only classical information between examples. It permits adaptive measurements, unlimited classical computation, and arbitrary measurements within each example. The argument uses a signed-Pauli learning tree in the spirit of [Chen–Cotler–Huang–Li](../references/RELATED_WORK.md#cchl2021), with explicit clipping to include the noiseless endpoint and a heterogeneous-contrast extension for the clean held-out test.

## Definitions and allowed protocols

Use the [canonical model](model.md): $`n\geq1`$, $`d=2^n`$, $`D=2d`$, and a uniformly random signed nonidentity Hermitian Pauli $`P=\sigma Q`$. Here $`Q`$ is uniform over the $`d^2-1`$ unsigned nonidentity Paulis and $`\sigma\in\{\pm1\}`$ is an independent uniform sign. An annotated example with contrast $`\gamma_t\in[0,1]`$ has state

```math
\tau_P(\gamma_t)=\frac{I+\gamma_t Z_C\otimes P}{D}.
```

The target is the same for all examples. Conditional on it, the examples are independent. The null experiment supplies $`\tau_0=I/D`$ on every example.

An individual-example protocol measures the complete current example, records a classical outcome, and discards its quantum systems before proceeding. Its choice of measurement may depend on the entire preceding classical transcript and private classical randomness. Arbitrary temporary quantum ancillas and computation within one example are allowed. Quantum information cannot persist between examples or jointly from training to the test. A persistent quantum ancilla would change this resource model.

Representing the annotation by a qubit lets us consider arbitrary POVMs on label plus feature. This includes the actual protocol that first reads the classical annotation and then chooses a feature measurement. Allowing even more general POVMs only strengthens the lower-bound comparator.

For distributions $`p,q`$, use total variation

```math
\operatorname{TV}(p,q)=\frac12\int|dp-dq|.
```

## Theorem S2

Let $`n\geq1`$, $`0<\gamma\leq1`$, and $`T\geq0`$ be an integer. If an individual-example trainer using $`T`$ training examples of contrast $`\gamma`$ achieves expected advantage $`a\in(0,1/2)`$ on one independent clean test example, then

```math
a\leq\frac{5(T\gamma^2+1)}{d+1}.
\tag{S2.1}
```

In particular,

```math
T\geq
\max\left\{0,
\left\lceil\frac{a(d+1)/5-1}{\gamma^2}\right\rceil\right\}.
\tag{S2.2}
```

When its numerator is nonpositive, (S2.2) is a valid but uninformative bound. For fixed positive $`a`$ and sufficiently large $`n`$, it gives

```math
T=\Omega_a\!\left(\frac{2^n}{\gamma^2}\right),
\tag{S2.3}
```

uniformly for $`\gamma\in(0,1]`$. For example, if $`d+1\geq10/a`$, equation (S2.2) implies $`T\geq a(d+1)/(10\gamma^2)`$ before rounding.

Performance is averaged over the specified uniform signed-Pauli prior, training samples, and test sample. Thus the theorem also excludes a guarantee of the stated advantage uniformly for every target with fewer examples. It does not assert that every particular known Pauli is difficult. No computational restriction is imposed on the measurements or classical postprocessing.

The proof proceeds through an exact second-moment bound and a more general transcript lemma.

## 1. Exact Pauli second moment

For a normalized vector $`|\phi\rangle`$ on label plus feature, define

```math
a_\phi(Q)=\langle\phi|Z_C\otimes Q|\phi\rangle,
\qquad
\delta_*=\sup_{\|\phi\|=1}\mathbb E_Q[a_\phi(Q)^2].
```

Then

```math
\delta_*=\frac1{d+1}.
\tag{S2.4}
```

### Proof

Write

```math
|\phi\rangle=|0\rangle|u\rangle+|1\rangle|v\rangle,
\qquad \|u\|^2+\|v\|^2=1,
```

and set $`B=|u\rangle\langle u|-|v\rangle\langle v|`$. Then $`a_\phi(Q)=\operatorname{Tr}(BQ)`$. Unsigned Paulis, including the identity, form an orthogonal Hermitian operator basis with $`\operatorname{Tr}(QQ')=d\,\mathbf1\{Q=Q'\}`$. Hence

```math
\sum_{Q\ne I}\operatorname{Tr}(BQ)^2
=d\operatorname{Tr}(B^2)-\operatorname{Tr}(B)^2.
\tag{S2.5}
```

Put $`t=\|u\|^2-\|v\|^2\in[-1,1]`$. Directly,

```math
\operatorname{Tr}(B^2)
=\|u\|^4+\|v\|^4-2|\langle u|v\rangle|^2
\leq\frac{1+t^2}{2}.
```

Since $`d\geq2`$,

```math
\begin{aligned}
d\operatorname{Tr}(B^2)-\operatorname{Tr}(B)^2
&\leq\frac d2+\left(\frac d2-1\right)t^2\\
&\leq d-1.
\end{aligned}
```

Dividing by $`d^2-1`$ proves the upper bound in (S2.4). Equality is attained by every vector $`|0\rangle\otimes|u\rangle`$ with normalized $`u`$. The argument permits $`\phi`$ to be entangled between label and feature or among feature qubits.

## 2. Transcript bound with heterogeneous contrasts

### Lemma: signed-Pauli transcript comparison

Fix an integer $`m\geq0`$ and predetermined contrasts $`\gamma_1,\ldots,\gamma_m\in[0,1]`$. Let $`p`$ be the complete transcript distribution of any adaptive individual-example protocol when $`P`$ is sampled once from the signed-Pauli prior and the examples are $`\tau_P(\gamma_t)`$. Let $`q`$ be the transcript distribution of the same protocol on the null examples. Then

```math
\operatorname{TV}(p,q)
\leq\min\left\{1,
5\delta_*\sum_{t=1}^m\gamma_t^2\right\}.
\tag{S2.6}
```

The empty protocol has identical transcript laws. The result includes contrasts equal to one.

### 2.1 Refinement and likelihood at a fixed leaf

Refine every nonzero POVM effect into rank-one positive effects and retain the refinement outcome in the classical transcript. The original protocol is recovered by forgetting that extra information, so proving the bound for refined protocols is sufficient by data processing of total variation. Private randomness can also be recorded in the transcript; its likelihood ratio is one because its law is the same in both experiments.

At a fixed refined transcript leaf, the effect used at time $`t`$ has the form $`w_t|\phi_t\rangle\langle\phi_t|`$, with $`\|\phi_t\|=1`$. The choice of $`\phi_t`$ may depend on earlier outcomes, but after fixing the leaf it is a fixed vector. Its conditional outcome probabilities are

```math
\begin{aligned}
p_{\sigma,Q,t}&=\frac{w_t}{D}
\left[1+\sigma\gamma_t a_t(Q)\right],\\
q_t&=\frac{w_t}{D},
\qquad
a_t(Q)=\langle\phi_t|Z_C\otimes Q|\phi_t\rangle.
\end{aligned}
```

Therefore the likelihood ratio for that leaf under a fixed hidden $`\sigma Q`$ is

```math
L_{\sigma,Q}=\prod_{t=1}^m
\left[1+\sigma\gamma_t a_t(Q)\right].
\tag{S2.7}
```

All factors are nonnegative because $`|a_t(Q)|\leq1`$. The mixed-target likelihood ratio is $`L=\mathbb E_{\sigma,Q}L_{\sigma,Q}`$. Since the null state is strictly positive, every nonzero effect has positive null probability; there is no singular-support contribution missing from this likelihood representation.

The notation uses a finite or countable outcome tree for clarity. For a general finite-dimensional POVM, take its scalar trace measure as the reference measure, use the positive operator-valued Radon–Nikodym density, and refine that density spectrally. The same conditional likelihood equations hold almost everywhere, with sums replaced by integrals. The proof below is pointwise in the transcript and therefore applies unchanged.

### 2.2 Clipping the logarithmic endpoints

Define

```math
x=\delta_*\sum_{t=1}^m\gamma_t^2.
```

If $`x\geq1/5`$, the bound $`\operatorname{TV}(p,q)\leq1`$ proves (S2.6). Assume henceforth $`x<1/5`$.

For the fixed transcript leaf, discard unsigned Paulis for which at least one $`|\gamma_t a_t(Q)|>1/2`$. Markov's inequality, the union bound, and (S2.4) give

```math
\begin{aligned}
\Pr_Q\!\left[\exists t:\ |\gamma_ta_t(Q)|>\frac12\right]
&\leq4\sum_t\gamma_t^2\mathbb E_Q a_t(Q)^2\\
&\leq4x.
\end{aligned}
```

Let $`G`$ be the retained set and $`g=\Pr_Q(G)\geq1-4x>0`$. Both signs of every retained $`Q`$ remain in the average. On $`G`$, every likelihood factor lies in $`[1/2,3/2]`$, so all logarithms below are finite even when a contrast equals one.

### 2.3 A pointwise one-sided likelihood bound

Nonnegativity of the discarded likelihoods and Jensen's inequality give

```math
\begin{aligned}
L
&\geq g\,\mathbb E_{Q\mid G,\sigma}
\exp\left\{\sum_t\ln[1+\sigma\gamma_t a_t(Q)]\right\}\\
&\geq g\exp\left\{
\mathbb E_{Q\mid G}\frac12\sum_t
\ln[1-\gamma_t^2a_t(Q)^2]\right\}.
\end{aligned}
```

The independent uniform sign is essential in the second line. For $`0\leq u\leq1/4`$,

```math
\ln(1-u)\geq-2u.
```

For example, the derivative of $`\ln(1-u)+2u`$ is nonnegative on this interval and its value at zero is zero. Also,

```math
\mathbb E_{Q\mid G}\sum_t\gamma_t^2a_t(Q)^2
\leq\frac1g\sum_t\gamma_t^2\mathbb E_Qa_t(Q)^2
\leq\frac{x}{g}.
```

Consequently,

```math
L\geq g e^{-x/g}\geq g-x\geq1-5x,
\tag{S2.8}
```

where $`e^{-r}\geq1-r`$ for $`r\geq0`$ gives the middle inequality. This holds for every transcript leaf, although the clipped set $`G`$ can depend on that leaf.

Because $`p=Lq`$ and both laws are normalized,

```math
\operatorname{TV}(p,q)=\mathbb E_q[(1-L)_+]
\leq5x.
```

This proves (S2.6), including fully adaptive classical feedback and the endpoints $`\gamma_t=0,1`$.

## 3. From clean prediction to transcript distinguishability

Run the proposed trainer on $`T`$ examples of contrast $`\gamma`$. Append one independent clean annotated example of contrast one, but withhold its annotation from the classifier until it predicts. After prediction, read the annotation and record the event that the two signs agree.

This is a valid $`T+1`$-example individual protocol. Once training has ended, its retained information is classical. Its test operation is therefore a POVM chosen by that classical transcript, followed by reading the held-out annotation. The annotation being withheld before prediction preserves the original clean test task.

In the target experiment, the event has probability $`1/2+a`$ by the assumed expected clean advantage. In the null experiment, the final annotation is an independent balanced bit, independent of both the test feature and the entire training transcript. Its agreement probability is exactly $`1/2`$. An event-probability difference cannot exceed total variation. Applying (S2.6) with contrasts $`\gamma,\ldots,\gamma,1`$ therefore yields

```math
a\leq\operatorname{TV}(p,q)
\leq\min\left\{1,
5\delta_*(T\gamma^2+1)\right\}.
```

Substituting (S2.4) proves (S2.1), and rearrangement plus integrality proves (S2.2).

Using a clean held-out example is legitimate for this statistical converse: it is precisely the prediction task under study, and the proof defines two experiments for analysis. It does not claim that an algorithm supplied only noisy annotations can manufacture a clean annotation. The computational reduction uses its available noisy held-out annotations instead and accordingly incurs a factor $`\gamma`$ in its distinguishing advantage. These are different proof experiments.

## 4. Scope of the separation

The [collective-statistics theorem](collective_statistics.md) attains fixed clean advantage with $`\Theta_a(n/\gamma^2)`$ examples. The present converse concerns the identical target prior, annotation noise, and single clean test objective, with the additional restriction that examples are converted individually to classical information. It therefore establishes an exponential sample gap between these resource models.

The argument does not bound algorithms with persistent quantum memory, even if that memory interacts with examples sequentially. Nor does it impose or exploit a restriction on classical computation, individual measurement complexity, the form of the learned classifier, or the number of classical bits retained.

The underlying signed-Pauli learning-tree method and the clean quantum-memory separation are established in [Chen–Cotler–Huang–Li](../references/RELATED_WORK.md#cchl2021). Here the explicit label register, endpoint-safe clipping, and heterogeneous-contrast held-out-test argument provide a self-contained prediction converse for the stated supervised task.

The independent numerical checks in [verify_statistics.py](../verification/verify_statistics.py) evaluate the Pauli second moment on actual vectors, include entangled label–feature vectors, and enumerate small adaptive measurement trees using Born probabilities. They also test the elementary clipping inequalities on their stated domains. These finite checks supplement the analytic proof and are not a replacement for the universal bounds.
