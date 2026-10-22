# A variant with a local preparation reduction

The main theorem uses a signed-uniform nonidentity Pauli target. Its physical source already admits [pure product preparation](source_preparation.md). Its hardness reduction, however, uses a random global Clifford to produce that uniform target prior. This chapter gives a supplementary variant in which the reduction itself uses only local basis changes. The target prior changes, and the individual-measurement lower bound has a different exponential base.

This variant is not needed for K1, B1, S1, S2, or H1 in [Model](model.md). Those canonical statements retain their original prior.

## 1. The prior and its source

Write $`n=k+1`$, with $`k\geq1`$. Independently choose a uniform bit string $`s\in\mathbb F_2^k`$, a uniform sign bit $`t`$, and axes $`R_i\in\{X,Y,Z\}`$ uniformly for $`1\leq i\leq k`$. Let

```math
P=(-1)^t\left(\bigotimes_{i=1}^kR_i^{s_i}\right)\otimes Z.
```

The final factor is fixed and nonidentity. Each preceding factor is identity with probability $`1/2`$ and each of $`X,Y,Z`$ with probability $`1/6`$. The unsigned prior $`w_Q`$ is therefore nonuniform, with support size $`4^k`$; the signed support has size $`2\cdot4^k`$.

Choose a single-qubit Clifford $`V_i`$ with $`V_iZV_i^\dagger=R_i`$. For a clean class bit $`y`$, draw $`x\in\mathbb F_2^k`$ uniformly and prepare

```math
\left(\bigotimes_{i=1}^kV_i|x_i\rangle\right)
\otimes|s\cdot x\oplus y\oplus t\rangle.
```

Its $`P`$ eigenvalue is $`(-1)^y`$. The $`2^k`$ vectors obtained by varying $`x`$ form an orthonormal basis of that eigenspace, including when some $`s_i=0`$. Their uniform mixture is exactly $`(I+YP)/d`$. Independent annotation flips again give $`(I+C\gamma P)/d`$.

## 2. Ordinary LPN gives the source through local gates

Given ordinary classical LPN samples $`(x,b=s\cdot x\oplus e)`$, choose the axes and sign bit once, draw a new uniform annotation bit $`c`$ for each sample, and prepare

```math
\left(\bigotimes_{i=1}^kV_i|x_i\rangle\right)
\otimes|b\oplus c\oplus t\rangle,
\qquad C=(-1)^c.
```

Setting $`y=e\oplus c`$ gives the clean source above, with independent annotation flip $`e`$. Conditional on $`y`$, the feature vector depends only on $`x,y,s,t,V`$; the noise bit disappears. The simulation is exact and uses only product states and local Clifford gates.

For the decision-LPN null distribution, $`b`$ is a fresh independent uniform bit. Averaging over $`x,b`$ gives $`I/d`$, independently of the recorded annotation. The one-held-out-example reduction in [Computational hardness](computational_hardness.md) applies without change: a learner's clean advantage $`a`$ gives distinguishing advantage $`\gamma|a|`$. The prior is now precisely the one in this chapter, instead of the main uniform prior.

The clean Bell algorithm also applies, because its identification guarantee holds for every nonidentity target, regardless of the prior.

## 3. The individual-measurement moment

For a rank-one vector $`|\phi\rangle`$ on annotation and feature registers, define

```math
\delta_{\mathrm{loc}}
=\sup_\phi\mathbb E_{Q\sim w}
\langle\phi|Z_C\otimes Q|\phi\rangle^2.
```

For any one of the first $`k`$ sites, the doubled-space moment is

```math
\begin{aligned}
\mathbb E(R_i^{s_i}\otimes R_i^{s_i})
&=\frac12I\otimes I+
\frac16(X\otimes X+Y\otimes Y+Z\otimes Z)\\
&=\frac{I+\mathrm{SWAP}}3
=\frac23\Pi_{\mathrm{sym}}.
\end{aligned}
```

Here $`\Pi_{\mathrm{sym}}`$ is the projector onto the symmetric two-qubit subspace. The doubled annotation and final feature factors are each $`Z\otimes Z`$, whose operator norm is one. Independence of the sites bounds the full moment operator's norm by $`(2/3)^k`$. Taking its expectation in $`|\phi\rangle\otimes|\phi\rangle`$ therefore gives the same upper bound on $`\delta_{\mathrm{loc}}`$.

Equality is attained by choosing a product vector across all physical registers, with arbitrary pure states on the first $`k`$ feature qubits and $`Z`$ eigenstates on the annotation and final feature registers. Each doubled pure local vector lies in the symmetric subspace, so

```math
\delta_{\mathrm{loc}}=\left(\frac23\right)^k.
```

The clipping and likelihood proof in [Individual measurements](individual_measurements.md) uses sign symmetry and the moment bound; it does not require a uniform unsigned prior. Applying it here, with $`T`$ training contrasts $`\gamma`$ and one clean test contrast, yields

```math
a\leq5\left(\frac23\right)^k(T\gamma^2+1),
\qquad
T\geq\frac{a(3/2)^k/5-1}{\gamma^2}.
```

For a fixed positive advantage this is $`\Omega((3/2)^k/\gamma^2)`$, for sufficiently large $`k`$. It remains exponential, but is weaker than the main uniform-prior bound.

## 4. Collective prediction still needs and suffices with a linear sample count

The unsigned collision probability is

```math
\sum_Qw_Q^2
=\left[\left(\frac12\right)^2+
3\left(\frac16\right)^2\right]^k
=3^{-k}.
```

Let $`p_P=w_Q/2`$ for each signed target $`P=\pm Q`$, and define the prediction operator as in [Collective statistics](collective_statistics.md), but with this prior. Pauli orthogonality again removes all pairs other than $`Q=\pm P`$. Direct expansion gives

```math
\operatorname{Tr}(X_T^2)
=\frac{3^{-k}}{2dD^T}
\left[(1+\gamma^2)^T-(1-\gamma^2)^T\right].
```

The trace-norm inequality on a space of dimension $`dD^T`$ yields

```math
a_T^*\leq\frac12
\sqrt{\frac{(1+\gamma^2)^T-(1-\gamma^2)^T}{2\cdot3^k}}.
```

For any fixed positive advantage this implies $`T=\Omega(k/\gamma^2)`$ as $`k\to\infty`$.

Conversely, the pairwise root fidelities have the same bound as for the main Pauli family:

```math
F_{\mathrm{root}}(\tau_P,\tau_Q)
\leq\sqrt{1-\gamma^2/2}
\quad(P\ne Q).
```

The pretty-good measurement bound with arbitrary priors gives

```math
\begin{aligned}
p_{\mathrm{err}}
&\leq\sum_{P\ne Q}\sqrt{p_Pp_Q}
F_{\mathrm{root}}(\tau_P,\tau_Q)^T\\
&\leq(2\cdot4^k-1)e^{-T\gamma^2/4}.
\end{aligned}
```

The last step uses $`(\sum_P\sqrt{p_P})^2\leq2\cdot4^k`$. Identification with fixed small error therefore needs only $`O(k/\gamma^2)`$ examples, proving $`\Theta(k/\gamma^2)`$ collective prediction complexity. This is again a statistical measurement construction without a polynomial-time implementation guarantee.

## 5. What changes from the main theorem

| Property | Main model | Local-prior variant |
|---|---|---|
| Target prior | Uniform over signed nonidentity $`n`$-qubit Paulis | Independent biased local factors and a known final $`Z`$ factor |
| Physical source | Pure product preparation is possible | Pure product preparation is possible |
| LPN simulation | A random global Clifford | Only local Cliffords |
| Collective examples | $`\Theta(n/\gamma^2)`$ | $`\Theta(k/\gamma^2)`$, with $`n=k+1`$ |
| Individual-example lower bound | $`\Omega(2^n/\gamma^2)`$ | $`\Omega((3/2)^k/\gamma^2)`$ |
| Conditional runtime barrier | Quantum decision-LPN at dimension $`n-1`$ | Quantum decision-LPN at dimension $`k`$ |

The variant shows that the reduction can be made local without losing an exponential memory advantage. It does not transfer the main theorem's exact uniform prior or its stronger exponential base to a local-only randomization scheme.
