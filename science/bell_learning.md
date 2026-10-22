# Learning from Bell measurements

Bell measurements convert independent pairs of labeled specimens into a classical affine parity problem. With correct annotations, the equations are exact and Gaussian elimination identifies the target. With corrupted annotations, the equations have independent parity noise at an explicitly transformed rate. This chapter proves that correspondence, gives an efficient clean learner, and describes both an exhaustive noisy decoder and an efficient regime for vanishing annotation noise.

All notation and access assumptions follow [The supervised learning model](model.md). In particular, $`P=\sigma W_p`$ is a signed nonidentity Pauli, $`p=(a,b)\in\mathbb F_2^{2n}`$, and $`\gamma=1-2\eta`$. Each pair consists of two independent source draws. The quantum interaction is in the measurement between specimens.

## Bell basis and phase conventions

Define

```math
|\Phi_d\rangle=\frac1{\sqrt d}
\sum_{x\in\mathbb F_2^n}|x\rangle|x\rangle,
\qquad
|\Phi_z\rangle=(I\otimes W_z)|\Phi_d\rangle,
\qquad
z\in\mathbb F_2^{2n}.
```

The $`d^2`$ vectors $`|\Phi_z\rangle`$ form an orthonormal basis because the Pauli operators are orthogonal in the Hilbert–Schmidt inner product. The Bell measurement has the rank-one effects $`|\Phi_z\rangle\langle\Phi_z|`$.

The two identities responsible for the parity relation are

```math
\langle\Phi_d|A\otimes B|\Phi_d\rangle
=\frac1d\operatorname{Tr}(A^TB),
\qquad
W_p^T=(-1)^{q(p)}W_p.
```

The transpose sign matters when the target has an odd number of $`Y`$ factors. With the canonical Hermitian Pauli convention, it produces the affine offset $`q(p)`$.

For implementation, write $`z=(a_z,b_z)`$. On each pair of corresponding qubits, apply a CNOT from the first specimen to the second, apply a Hadamard to the first qubit, and measure both qubits in the computational basis. The first outcome is $`b_{z,j}`$ and the second is $`a_{z,j}`$; a classical reordering gives $`z`$. Thus one Bell measurement uses $`O(n)`$ elementary gates and $`2n`$ one-qubit measurements. It can be performed by holding the first specimen until the second arrives. This is an implementation upper bound, without a claim of minimum quantum memory.

Bell sampling of Pauli information and a subsequent sign-learning step are established mechanisms; see [HKP2021, Appendix E.2](../references/RELATED_WORK.md#hkp2021). The broader quantum-memory separation framework is developed in [CCHL2021](../references/RELATED_WORK.md#cchl2021). The following statement records the exact Bell correspondence for classical noisy annotations.

## B1 — The exact Bell correspondence

**Theorem B1.** Take two independent training examples for the same target. Bell-measure their feature registers, obtaining $`Z`$, and form the product $`R=C_1C_2`$ of their recorded labels. Then

```math
\begin{aligned}
Z&\sim\operatorname{Unif}(\mathbb F_2^{2n}),\\
R&=(-1)^{q(p)+[p,Z]}F,\\
\Pr(F=-1)&=\eta_B=2\eta(1-\eta),\\
1-2\eta_B&=(1-2\eta)^2=\gamma^2.
\end{aligned}
```

The random sign $`F`$ is independent of $`Z`$. Applying the procedure to disjoint pairs gives independent observations of this distribution. The global target sign $`\sigma`$ does not occur in the distribution.

**Proof.** Condition first on the clean class labels $`Y_1,Y_2`$. The two independent specimens have state

```math
\rho^0_{Y_1,P}\otimes\rho^0_{Y_2,P}
=\frac1{d^2}
\left[
I\otimes I+Y_1P\otimes I+Y_2I\otimes P
+Y_1Y_2P\otimes P
\right].
```

The terms linear in $`P`$ have zero expectation in a Bell vector because $`P`$ is traceless. The remaining term satisfies

```math
\begin{aligned}
\langle\Phi_z|P\otimes P|\Phi_z\rangle
&=\frac1d\operatorname{Tr}
\left[P^T W_z^\dagger P W_z\right]\\
&=(-1)^{q(p)+[p,z]}.
\end{aligned}
```

Here $`P^T=(-1)^{q(p)}P`$, conjugation contributes $`(-1)^{[p,z]}`$, and $`P^2=I`$. Therefore

```math
\Pr(Z=z\mid Y_1,Y_2)
=\frac1{d^2}
\left[1+Y_1Y_2(-1)^{q(p)+[p,z]}\right].
```

An outcome has nonzero probability only if

```math
Y_1Y_2=(-1)^{q(p)+[p,Z]}.
```

Since $`Y_1Y_2`$ is balanced, averaging over the clean labels makes $`Z`$ exactly uniform. The independently generated label flips do not change the feature state or Bell outcome. Consequently,

```math
R=C_1C_2=Y_1Y_2E_1E_2
=(-1)^{q(p)+[p,Z]}F,
\qquad F=E_1E_2.
```

Exactly one of $`E_1,E_2`$ is negative with probability $`2\eta(1-\eta)`$. Independence of the annotation noise from the clean specimens makes $`F`$ independent of $`Z`$. Independence of source draws and flips across disjoint pairs proves the final assertion. ∎

In bit notation, with $`r=(1-R)/2`$, Theorem B1 is

```math
r=q(p)+[p,z]+\xi\pmod2,
\qquad
\xi\sim\operatorname{Bernoulli}(\eta_B).
```

If ordinary dot products use the coordinate order $`z=(a_z,b_z)`$, the linear coefficient is $`(b,a)`$:

```math
[p,z]=(b,a)\cdot(a_z,b_z)\pmod2.
```

The offset $`q(p)`$ is a fixed function of the target. It can still be treated as an additional unknown affine coefficient during linear-system solving. The global sign $`\sigma`$ cancels because the Bell statistic contains $`P\otimes P`$.

An equivalent conditional likelihood, useful for checking the convention, is

```math
\Pr(Z=z\mid C_1,C_2)
=\frac1{d^2}
\left[1+C_1C_2\gamma^2(-1)^{q(p)+[p,z]}\right].
```

## K1 — Efficient clean learning

**Theorem K1.** Let $`\eta=0`$ and $`\delta\in(0,1)`$. Define

```math
m=2n+1+\left\lceil\log_2\frac1\delta\right\rceil.
```

There is an algorithm using $`2m+1`$ training specimens that outputs the exact signed target $`P`$ with probability at least $`1-\delta`$, for every signed nonidentity $`P`$. Its quantum and classical running times are polynomial in $`n`$ and $`\log(1/\delta)`$.

**Algorithm.** Bell-measure $`m`$ disjoint pairs and retain the bit equations

```math
r_j=q(p)+(b,a)\cdot z_j\pmod2,
\qquad j=1,\ldots,m.
```

Solve this affine system by Gaussian elimination for the $`2n+1`$ coefficients $`(q,b,a)`$. If the design matrix does not have full column rank, report failure. Otherwise reconstruct the unsigned Pauli $`W_p`$. On one additional clean annotated specimen, measure $`W_p`$, obtaining a sign $`B`$, and set

```math
\widehat\sigma=CB.
```

Return $`\widehat P=\widehat\sigma W_p`$.

**Proof of the rank guarantee.** The design rows are $`(1,z_j)`$, where the $`z_j`$ are independent and uniform in $`\mathbb F_2^{2n}`$. Rank deficiency means that some nonzero affine function

```math
f(z)=u_0+u\cdot z
```

vanishes on every sampled point. The constant-one function cannot do so. For every $`u\ne0`$, the function is balanced, so the probability that it vanishes on all $`m`$ points is $`2^{-m}`$. There are $`2^{2n+1}-2`$ such nonconstant affine functions. A union bound gives

```math
\Pr(\text{rank deficiency})
\leq (2^{2n+1}-2)2^{-m}
\leq 2^{2n+1-m}
\leq\delta.
```

On full rank, the exact clean equations have the unique correct solution. This determines $`p`$, including the required relation between its coordinates and $`q(p)`$.

**Proof of sign calibration.** A specimen with clean label $`Y`$ lies in the $`Y`$ eigenspace of $`P=\sigma W_p`$. Measuring $`W_p`$ therefore gives $`B=\sigma Y`$ with certainty. Since $`C=Y`$ in the clean case, $`CB=\sigma`$. Thus the additional example determines the sign without further failure probability, conditional on correct recovery of $`p`$.

**Cost and prediction.** Bell measurements use $`O(mn)`$ gates in total. Dense Gaussian elimination takes $`O(m(2n+1)^2)`$ bit operations. The final Pauli measurement uses at most $`n`$ single-qubit measurements. The output consists of $`2n`$ Pauli-coordinate bits and one sign bit. Once the output is correct, measuring its single-qubit factors and multiplying their outcomes predicts every clean test label perfectly. ∎

## An explicit noisy statistical decoder

The Bell correspondence also gives a finite-sample identification algorithm for every $`\gamma>0`$. Its exhaustive classical search is expensive, which makes the distinction between sample complexity and runtime explicit.

For each candidate $`p'\in\mathbb F_2^{2n}\setminus\{0\}`$, compute

```math
\widehat c(p')
=\frac1m\sum_{j=1}^m R_j(-1)^{[p',Z_j]}.
```

Character orthogonality and B1 give

```math
\mathbb E\widehat c(p')
=\begin{cases}
\gamma^2(-1)^{q(p)},&p'=p,\\
0,&p'\ne p.
\end{cases}
```

For completeness, the orthogonality used here is

```math
\mathbb E_Z(-1)^{[u,Z]}=\mathbf1\{u=0\}.
```

The symplectic pairing is nondegenerate, so every nonzero $`u`$ defines a balanced linear functional.

Each summand of $`\widehat c(p')`$ lies in $`\{-1,+1\}`$. Hoeffding's inequality yields

```math
\Pr\left(
\left|\widehat c(p')-\mathbb E\widehat c(p')\right|
\geq \frac{\gamma^2}{4}
\right)
\leq 2\exp\left(-\frac{m\gamma^4}{32}\right).
```

A union bound over fewer than $`4^n`$ candidates shows that

```math
m\geq
\left\lceil
\frac{32}{\gamma^4}\ln\frac{2\cdot4^n}{\delta_1}
\right\rceil
```

is sufficient for all candidate scores to be within $`\gamma^2/4`$ of their means, with probability at least $`1-\delta_1`$. On this event, the true candidate has absolute score at least $`3\gamma^2/4`$, and every other candidate has absolute score at most $`\gamma^2/4`$. Maximizing the absolute score recovers the unsigned target.

The global sign is then calibrated using fresh, independent annotated specimens. For each such specimen, measure $`W_p`$ and record

```math
V=CB=\sigma E.
```

Conditional on a correct unsigned target, these variables have mean $`\sigma\gamma`$. Majority vote determines $`\sigma`$ with error at most

```math
\exp\left(-\frac{L\gamma^2}{2}\right)
```

after $`L`$ calibration examples. Thus

```math
L\geq\left\lceil\frac{2}{\gamma^2}\ln\frac1{\delta_2}\right\rceil
```

suffices. Taking $`\delta_1=\delta_2=\delta/2`$ gives identification error at most $`\delta`$ with

```math
T=2m+L
=O\left(
\frac{n+\ln(1/\delta)}{\gamma^4}
+\frac{\ln(1/\delta)}{\gamma^2}
\right)
```

training specimens.

Elementary exhaustive evaluation costs $`O(4^nmn)`$ bit operations, in addition to the polynomial cost of sensing the specimens. This algorithm is a statistical upper bound with explicit computational cost. It does not prove that every two-copy measurement requires the same fourth-power precision dependence. General few-copy precision tradeoffs are treated in [CGY2024](../references/RELATED_WORK.md#cgy2024). The optimal unrestricted collective dependence for the present prediction task is $`\Theta(n/\gamma^2)`$, proved in [Collective statistics](collective_statistics.md).

## Vanishing noise: a clean-batch algorithm

Fixed positive noise and a noise rate that decreases with dimension are different computational regimes. A simple clean-batch strategy gives an explicit positive result in the latter case.

**Proposition.** Suppose $`0\leq\eta<1/2`$ is known, and let $`\delta\in(0,1)`$. There is an identification algorithm with failure probability at most $`\delta`$ whose specimen count and total runtime are bounded by

```math
\exp(O(\eta n))\,
\operatorname{poly}\!\left(n,\gamma^{-1},\ln(1/\delta)\right).
```

In particular, both costs are polynomial when $`\eta=O(\log n/n)`$ and the requested confidence has polynomial bit complexity. This is a sufficient efficient regime, without an assertion of a sharp transition.

**Candidate generation.** Set

```math
r=2n+1,
\qquad
m_0=r+3=2n+4,
\qquad
\alpha=(1-\eta_B)^{m_0}.
```

Generate independent batches of $`m_0`$ Bell equations. In each batch, solve the affine equations. Discard the batch if the design has deficient rank, if the equations are inconsistent, or if the solution fails the Pauli conditions $`p'\ne0`$ and $`q'=q(p')`$. Otherwise retain its unsigned candidate $`p'`$.

The probability that a batch contains no corrupted equations is exactly $`\alpha`$. B1 makes that event independent of its covariates. The clean rank bound above gives

```math
\Pr(\text{full affine rank})
\geq 1-2^{r-m_0}
=\frac78.
```

Consequently, each batch produces the correct candidate with probability at least $`7\alpha/8`$. Choose

```math
N=
\left\lceil
\frac{8}{7\alpha}\ln\frac3\delta
\right\rceil.
```

The probability that none of these independent batches is both clean and full rank is at most

```math
\left(1-\frac{7\alpha}{8}\right)^N
\leq\exp\left(-\frac{7\alpha N}{8}\right)
\leq\frac\delta3.
```

The retained list therefore contains the correct unsigned target with probability at least $`1-\delta/3`$. The algorithm does not know which batches were clean; independent validation resolves that uncertainty.

**Independent validation.** Draw a fresh validation set of $`m_v`$ Bell observations. For every retained candidate, compute its absolute empirical correlation as in the exhaustive decoder. Conditional on the complete candidate list, the validation observations are independent of that list. There are at most $`N`$ candidates, so

```math
m_v=
\left\lceil
\frac{32}{\gamma^4}\ln\frac{6N}{\delta}
\right\rceil
```

makes all their score deviations smaller than $`\gamma^2/4`$ with probability at least $`1-\delta/3`$. Whenever the true target is in the list and these deviations are small, it is the unique unsigned candidate of greatest absolute score. Repeated copies of the same candidate can be removed classically.

The validation observations are measured once and their **classical** outcomes are evaluated against the whole list. No quantum specimen is reused and no additional copy of a latent example is needed. An empty list is treated as failure.

**Sign and total error.** Finally, use

```math
L=
\left\lceil\frac{2}{\gamma^2}\ln\frac3\delta\right\rceil
```

fresh calibration specimens. The sign error, conditional on the correct unsigned target, is at most $`\delta/3`$. The three failure events have total probability at most $`\delta`$.

**Cost bound.** The explicit specimen count is

```math
T=2Nm_0+2m_v+L.
```

Candidate generation costs $`O(Nm_0r^2)`$ bit operations; validating the list costs $`O(Nm_vn)`$. Bell sensing and sign calibration have costs linear in the number of measured qubits. To bound $`N`$, use $`0\leq\eta_B\leq1/2`$ and

```math
-\ln(1-\eta_B)
\leq \frac{\eta_B}{1-\eta_B}
\leq 2\eta_B
\leq 4\eta.
```

It follows that

```math
\alpha^{-1}
\leq\exp\bigl(4\eta(2n+4)\bigr)
=\exp(O(\eta n)).
```

The displayed copy and time bounds follow, including the validation and calibration factors in $`\gamma^{-1}`$. If $`\eta\leq K\log n/n`$ for a fixed constant $`K`$, the exponential factor is a fixed power of $`n`$ and $`\gamma`$ tends to one. ∎

The strategy is the elementary noisy-parity method of trying small clean systems and validating their solutions. Its role here is to specify an efficient regime that is consistent with the fixed-rate conditional hardness theorem. It does not establish hardness at larger vanishing noise rates.

## Computational consequences of the correspondence

An efficient classical or quantum search-LPN solver at noise rate $`\eta_B`$, on ordinary classical samples, can be used after Bell sensing. The unknown affine offset can be handled by trying both possibilities. At least one trial has the correct offset; candidate solutions can be checked on independent Bell observations, and the target's global sign is determined by the separate calibration measurement. The solver's success guarantee must apply to the resulting distribution of nonzero linear coefficients, or uniformly to all coefficients. For an average-case guarantee under uniform coefficients, conditioning away the zero coefficient changes the distribution by only $`2^{-2n}`$.

This reduction from quantum specimens to parity data has parameters

```math
n\ \text{feature qubits}
\quad\longrightarrow\quad
2n\ \text{parity coordinates},
\qquad
\eta\longrightarrow 2\eta(1-\eta).
```

In the other direction, [Computational hardness](computational_hardness.md) transforms classical LPN in dimension $`k`$, at its original noise rate $`\eta`$, into the present learning task on $`n=k+1`$ qubits. That reduction applies to every efficient quantum predictor, including strategies that never perform Bell measurements. The two directions therefore give explicit computational connections with different dimensions and noise parameters; they do not assert a same-parameter equivalence.
