# Collective statistical complexity

This chapter proves the optimal number of training examples for unrestricted coherent prediction in the [supervised model](model.md). The lower bound applies directly to prediction on one fresh clean test system. The upper bound identifies the target with a collective measurement whose implementation is not claimed to be efficient.

## Definitions

Let $`n\geq 1`$ be an integer, $`d=2^n`$, $`D=2d`$, and $`M=2(d^2-1)`$. The target $`P`$ is uniform over the $`M`$ signed nonidentity Hermitian $`n`$-qubit Paulis. A clean label $`Y\in\{+1,-1\}`$ is balanced, and its conditional feature state is

```math
\rho^0_{Y,P}=\frac{I+YP}{d}.
```

Training annotations are independently flipped with probability $`\eta\in[0,1/2)`$. Write $`\gamma=1-2\eta\in(0,1]`$. Represent the observed classical annotation $`C`$ by a computational-basis register whose Pauli $`Z_C`$ has eigenvalue $`C`$. One annotated training example is the classical–quantum state

```math
\tau_P=\frac{I+\gamma Z_C\otimes P}{D}.
```

For an integer $`T\geq0`$, let $`a_T^*`$ be the largest expected clean-test advantage over $`1/2`$, averaged over the uniform target, the independent training examples, and one independent clean test example. The learner may keep all training systems until the test arrives, use any joint measurement, and consume its model. Thus this is a statistical optimum with unrestricted computation. It includes every training-and-deployment procedure permitted by the model.

## Theorem S1

For $`n\geq1`$, $`0<\gamma\leq1`$, and an integer $`T\geq1`$,

```math
\begin{aligned}
a_T^*\leq
\min\left\{\frac12,
\frac12\sqrt{\frac{(1+\gamma^2)^T-(1-\gamma^2)^T}{M}}\right\}.
\end{aligned}
\tag{S1.1}
```

For $`T=0`$, $`a_0^*=0`$. Consequently, any learner attaining a prescribed advantage $`a\in(0,1/2)`$ must use

```math
\begin{aligned}
T\geq
\max\left\{1,
\left\lceil\frac{\ln(4a^2M)}{\ln(1+\gamma^2)}\right\rceil\right\}.
\end{aligned}
\tag{S1.2}
```

The logarithmic bound can be weak for small $`n`$ and small $`a`$; equation (S1.1) is the stronger finite-parameter statement.

Conversely, for every $`\delta\in(0,1)`$, a collective pretty-good measurement identifies the signed target with average error at most $`\delta`$ whenever

```math
\begin{aligned}
T\geq
\left\lceil\frac{4}{\gamma^2}
\ln\frac{M-1}{\delta}\right\rceil.
\end{aligned}
\tag{S1.3}
```

On successful identification, measuring $`P`$ on the fresh test predicts its clean label perfectly. Choosing $`\delta=1/2-a`$ therefore gives clean-test advantage at least $`a`$. For each fixed $`a\in(0,1/2)`$, the optimal training-example complexity is

```math
\begin{aligned}
T_{\mathrm{coh}}(n,\gamma,a)=\Theta_a\!\left(\frac{n}{\gamma^2}\right)
\qquad(n\longrightarrow\infty),
\end{aligned}
\tag{S1.4}
```

uniformly over $`\gamma\in(0,1]`$, including choices of $`\gamma`$ that depend on $`n`$. The constants and the sufficiently large $`n`$ threshold may depend on the fixed requested advantage.

### Average and worst-case interpretation

The converse bounds the average success under the specified prior. In particular, no learner can attain an advantage exceeding this bound for every target. It is not a claim that every fixed, individually known target requires these samples.

The PGM construction below is covariant under Clifford conjugation, which acts transitively on the signed nonidentity Paulis. Its identification success is therefore the same for every target. The stated upper bound can consequently be taken uniformly over $`P`$, even though only the average guarantee is needed for the separation.

## 1. Reduction of arbitrary prediction to a binary state test

Condition on the fresh clean label being $`y\in\{+1,-1\}`$. The joint state of all training inputs and the unlabeled test feature is

```math
\Omega_y=
\frac1M\sum_P\tau_P^{\otimes T}\otimes\frac{I+yP}{d}.
```

Every procedure that trains a model and later produces one prediction is a binary POVM on these inputs. Conversely, unrestricted quantum retention permits the learner to keep the training systems and perform any such POVM when the test arrives. This remains true when the model is consumed during inference.

Define the Hermitian operator

```math
\begin{aligned}
X_T=\frac1M\sum_P\tau_P^{\otimes T}\otimes\frac{P}{d}.
\end{aligned}
\tag{S1.5}
```

Then $`\Omega_+-\Omega_-=2X_T`$. Equal-prior binary state discrimination gives

```math
\begin{aligned}
a_T^*=\frac14\|\Omega_+-\Omega_-\|_1
=\frac12\|X_T\|_1.
\end{aligned}
\tag{S1.6}
```

Here $`\|\cdot\|_1`$ is the trace norm. The binary-discrimination formula and the general measurement framework are reviewed in [Cheng et al.](../references/RELATED_WORK.md#cheng2024).

There is no assumption of quantum coherence in the classical annotations. Both hypotheses are block diagonal in all annotation registers. Pinching any candidate POVM in those registers preserves its outcome probabilities, and the optimal Helstrom POVM can itself be chosen block diagonal. It can therefore be implemented by reading the annotations and choosing the appropriate conditional measurement on the feature systems.

For $`T=0`$, the independent sign symmetry gives $`X_0=\mathbb E_P[P]/d=0`$, proving $`a_0^*=0`$.

## 2. Exact second moment and the prediction converse

The Pauli trace identities imply

```math
\mathrm{Tr}(PQ)=
\begin{cases}
d,&Q=P,\\
-d,&Q=-P,\\
0,&Q\notin\{P,-P\}.
\end{cases}
```

The corresponding one-example overlaps are

```math
\mathrm{Tr}(\tau_P^2)=\frac{1+\gamma^2}{D},
\qquad
\mathrm{Tr}(\tau_P\tau_{-P})=\frac{1-\gamma^2}{D}.
```

Using multiplicativity of the trace under tensor products in (S1.5),

```math
\begin{aligned}
\mathrm{Tr}(X_T^2)
&=\frac1{M^2}\sum_{P,Q}
\bigl[\mathrm{Tr}(\tau_P\tau_Q)\bigr]^T
\frac{\mathrm{Tr}(PQ)}{d^2}\\
&=\frac1{dM}\left[
\left(\frac{1+\gamma^2}{D}\right)^T
-\left(\frac{1-\gamma^2}{D}\right)^T\right]\\
&=\frac{(1+\gamma^2)^T-(1-\gamma^2)^T}{dMD^T}.
\end{aligned}
\tag{S1.7}
```

This is an exact identity for $`T\geq1`$, including $`\gamma=1`$. At $`T=0`$, its numerator should be read as $`1-1=0`$; we use the separate zero-example argument to avoid a $`0^0`$ convention at the endpoint.

The operator $`X_T`$ acts in dimension $`dD^T`$. Cauchy–Schwarz for its singular values gives

```math
\|X_T\|_1^2\leq dD^T\mathrm{Tr}(X_T^2).
```

Combining this with (S1.6) and (S1.7) proves (S1.1). In particular, $`a_T^*\geq a`$ implies

```math
(1+\gamma^2)^T\geq
(1+\gamma^2)^T-(1-\gamma^2)^T\geq4a^2M.
```

Taking logarithms, enforcing integrality, and excluding $`T=0`$ proves (S1.2). Since $`\ln(1+\gamma^2)\leq\gamma^2`$ and $`\ln M=\Theta(n)`$, this is $`\Omega_a(n/\gamma^2)`$ for fixed positive advantage and sufficiently large $`n`$.

The exact object in this proof is the second moment (S1.7). Equation (S1.1) is an upper bound on optimal advantage, not an exact closed form for its finite-$`T`$ value.

## 3. Pairwise root fidelities

Use the root-fidelity convention

```math
f(\rho,\sigma)=\|\sqrt{\rho}\sqrt{\sigma}\|_1.
```

Some references instead call $`F(\rho,\sigma)=f(\rho,\sigma)^2`$ the fidelity. Every occurrence below is explicitly the root fidelity. For two distinct signed targets,

| Relation between targets | Root fidelity |
|---|---|
| $`Q=-P`$ | $`\sqrt{1-\gamma^2}`$ |
| $`[P,Q]=0`$ and $`Q\ne\pm P`$ | $`(1+\sqrt{1-\gamma^2})/2`$ |
| $`\{P,Q\}=0`$ | $`\sqrt{1-\gamma^2/2}`$ |

To prove these formulas, set $`A=Z_C\otimes P`$ and $`B=Z_C\otimes Q`$. They are traceless Hermitian involutions and $`\tau_P=(I+\gamma A)/D`$.

If $`Q=-P`$, then $`B=-A`$. The states commute and the product of their square roots is $`\sqrt{1-\gamma^2}\,I/D`$, giving the first row.

If $`P,Q`$ commute and $`Q\ne\pm P`$, then $`A,B`$ commute and $`\mathrm{Tr}(A)=\mathrm{Tr}(B)=\mathrm{Tr}(AB)=0`$. Each joint eigenspace, with eigenvalues $`u,v\in\{\pm1\}`$, has dimension $`D/4`$. Consequently,

```math
\begin{aligned}
f(\tau_P,\tau_Q)
&=\frac14\sum_{u,v\in\{\pm1\}}
\sqrt{(1+\gamma u)(1+\gamma v)}\\
&=\frac14\bigl(\sqrt{1+\gamma}+\sqrt{1-\gamma}\bigr)^2
=\frac{1+\sqrt{1-\gamma^2}}2.
\end{aligned}
```

For $`n=1`$, distinct unsigned nonidentity Paulis anticommute, so this commuting case simply does not arise.

If $`P,Q`$ anticommute, then $`A,B`$ generate a qubit algebra with a maximally mixed multiplicity space. Their two reduced qubit states have perpendicular Bloch vectors of length $`\gamma`$. For qubit states $`r,s`$,

```math
f(r,s)^2=\mathrm{Tr}(rs)+2\sqrt{\det(r)\det(s)}.
```

Here $`\mathrm{Tr}(rs)=1/2`$ and $`\det(r)=\det(s)=(1-\gamma^2)/4`$. Thus $`f^2=1-\gamma^2/2`$, and adjoining an identical maximally mixed multiplicity factor does not change fidelity.

The largest of the three values is

```math
\begin{aligned}
f_{\max}=\sqrt{1-\gamma^2/2}.
\end{aligned}
\tag{S1.8}
```

For the commuting value, this comparison is the arithmetic-mean–quadratic-mean inequality applied to $`1`$ and $`\sqrt{1-\gamma^2}`$.

## 4. A collective PGM attaining the upper bound

Define the subnormalized hypothesis operators and their sum by

```math
A_P=\frac1M\tau_P^{\otimes T},
\qquad G=\sum_P A_P.
```

On the support of $`G`$, the pretty-good measurement has effects

```math
\begin{aligned}
E_P=G^{-1/2}A_PG^{-1/2},
\end{aligned}
\tag{S1.9}
```

where the inverse is restricted to the support. Any positive completion on the kernel yields a POVM on the full space. Every hypothesis is supported on $`G`$, so that completion has zero outcome probability on the ensemble.

The standard mixed-state PGM bound gives

```math
\begin{aligned}
P_{\mathrm{err}}^{\mathrm{PGM}}
\leq\sum_{P\ne Q}\sqrt{p_Pp_Q}\,
f(\tau_P^{\otimes T},\tau_Q^{\otimes T}),
\qquad p_P=\frac1M.
\end{aligned}
\tag{S1.10}
```

An explicit statement and derivation appear in [Cheng et al., Appendix J](../references/RELATED_WORK.md#cheng2024). That reference uses squared fidelity, so its square-root-fidelity term is precisely the $`f`$ in (S1.10). The PGM method is also associated with [Barnum and Knill](../references/RELATED_WORK.md#barnum-knill2002); (S1.10) is the particular modern bound used here.

Root fidelity is multiplicative on tensor products. Equations (S1.8) and (S1.10) therefore give

```math
\begin{aligned}
P_{\mathrm{err}}^{\mathrm{PGM}}
&\leq(M-1)(1-\gamma^2/2)^{T/2}\\
&\leq(M-1)e^{-T\gamma^2/4}.
\end{aligned}
\tag{S1.11}
```

The last inequality uses $`\ln(1-u)\leq-u`$. This proves (S1.3). If the identification is correct, the test-label prediction is exact. Assigning the worst possible test outcome to every identification failure still leaves prediction success at least $`1-P_{\mathrm{err}}^{\mathrm{PGM}}`$.

Every $`A_P`$, their sum $`G`$, and the spectral function $`G^{-1/2}`$ are block diagonal in the classical training labels. The PGM therefore acts conditionally on the observed annotation string. It requires no coherent control of a superposition of annotations.

For Clifford covariance, let $`U`$ be a Clifford and apply $`I_C\otimes U`$ to each training example. This permutes the hypotheses and leaves their uniform average $`G`$ invariant. Equation (S1.9) transforms in the same way. Thus the correct-identification probability is constant on the Clifford orbit, which is the entire signed nonidentity Pauli family. This proves the stated uniform-target upper guarantee.

The construction is a finite-dimensional measurement specification. The hypothesis matrices can be explicitly generated, but the argument does not provide a polynomial-time circuit or decoder. In particular, statistical attainability does not resolve efficient learning under noisy annotations.

## 5. Relation to other resource statements

The [individual-measurement converse](individual_measurements.md) requires $`\Omega_a(2^n/\gamma^2)`$ examples for the same clean prediction objective. The comparison therefore concerns measurement resources at the same noise level and the same fixed advantage.

The Bell transcript gives a separate explicit upper bound of order $`n/\gamma^4`$ for noisy identification by exhaustive parity decoding. Its squared contrast explains that cost, but does not establish optimality among all two-copy protocols. The PGM above proves the unrestricted $`\gamma^{-2}`$ statistical scaling without claiming an efficient implementation.

The numerical checks in [verify_statistics.py](../verification/verify_statistics.py) construct small-dimensional input matrices, compare the resulting Helstrom second moments with (S1.7), evaluate the three root-fidelity cases, and check direct and label-conditioned PGM constructions. These checks supplement the proofs; they do not establish computational hardness or novelty.
