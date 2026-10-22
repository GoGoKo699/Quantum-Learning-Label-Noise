# Preparing the supervised source

The density operators in [Model](model.md) have an elementary realization: every draw can be a pure product state. The source chooses local eigenstates subject to one classical parity condition. The learner receives the resulting specimen and its possibly corrupted annotation, without the preparation choices.

This construction separates the cost of supplying the data from the cost of learning the hidden measurement. It also specifies precisely why a different ensemble used inside the computational reduction represents the same learning problem.

## 1. A parity-conditioned product ensemble

Write the signed target as

```math
P=\sigma\bigotimes_{i=1}^n R_i,
\qquad R_i\in\{I,X,Y,Z\},
\qquad \sigma=(-1)^s.
```

Let $`J=\{i:R_i\ne I\}`$ be its nonempty support, and choose one pivot $`j\in J`$. On an identity factor choose the computational basis; on a nonidentity factor choose the eigenbasis of $`R_i`$. Denote the chosen basis vector with eigenvalue bit $`b_i`$ by $`|b_i;R_i\rangle`$, with the convention $`|b_i;I\rangle=|b_i\rangle`$.

To prepare a clean example of class $`Y=(-1)^y`$:

1. Draw the $`n-1`$ bits $`b_i`$ with $`i\ne j`$ independently and uniformly.
2. Set the remaining bit to

```math
b_j=y\oplus s\oplus\bigoplus_{i\in J\setminus\{j\}}b_i.
```

3. Prepare the product vector

```math
|\psi_b\rangle=\bigotimes_{i=1}^n|b_i;R_i\rangle.
```

The resulting vector obeys $`P|\psi_b\rangle=Y|\psi_b\rangle`$. Exactly $`2^{n-1}`$ orthonormal product vectors satisfy this parity constraint, and the procedure chooses each with equal probability. Therefore

```math
\begin{aligned}
\mathbb E_b|\psi_b\rangle\langle\psi_b|
&=\frac{1}{2^{n-1}}\,\Pi_{Y,P}\\
&=\frac{I+YP}{d}
=\rho^0_{Y,P},
\end{aligned}
```

where $`\Pi_{Y,P}=(I+YP)/2`$ is the spectral projector. Identity factors pose no difficulty: their independent basis bits fill the unconstrained degrees of freedom in that eigenspace.

This proves the source claim for every signed nonidentity target, including targets whose support is only one qubit. It uses $`n-1`$ independent random bits after the class label is selected, $`O(n)`$ classical parity work, and $`O(n)`$ single-qubit Clifford operations. If a single-qubit Clifford is treated as one operation, the quantum preparation has one parallel layer; over the elementary gate set $`H,S,X`$ its depth remains constant. No entangling gate is needed.

### A complete two-qubit example

Take $`P=X\otimes Z`$ and use the first qubit as pivot. Write $`|+\rangle,|-\rangle`$ for the two $`X`$ eigenvectors.

| Clean label | Equally likely preparation choices | Conditional density operator |
|---|---|---|
| $`Y=+1`$ | $`|+0\rangle`$, $`|-1\rangle`$ | $`(I+X\otimes Z)/4`$ |
| $`Y=-1`$ | $`|+1\rangle`$, $`|-0\rangle`$ | $`(I-X\otimes Z)/4`$ |

Each individual vector is a product state. Measuring $`X`$ on the first qubit and $`Z`$ on the second gives two signs whose product is the clean label. A learner that does not know the local axes must discover which product of local measurements carries the label.

## 2. Adding annotation noise changes no prepared vector

After preparing the clean example, the source draws an independent flip bit $`e\sim\operatorname{Bernoulli}(\eta)`$ and records $`c=y\oplus e`$. Thus the quantum preparation and its latent clean class are unchanged. The state conditioned on the *recorded* sign is

```math
\begin{aligned}
\rho_{C,P,\gamma}
&=(1-\eta)\rho^0_{C,P}+\eta\rho^0_{-C,P}\\
&=\frac{I+C(1-2\eta)P}{d}
=\frac{I+C\gamma P}{d}.
\end{aligned}
```

The unannotated feature marginal is $`I/d`$ at every noise rate. Information about the target is in the correlation between annotations and specimens, rather than in the feature marginal alone.

For the example above, a specimen recorded as positive came from the first row with probability $`1-\eta`$ and the second with probability $`\eta`$. Each source realization remains a pure product vector. The conditional density operator becomes less distinguishable from its negative-label counterpart because the observer has an unreliable classical label.

## 3. Why alternative decompositions are operationally identical

Suppose two sources, for each fixed target and recorded label, prepare different ensembles with the same density operator $`\rho_{C,P,\gamma}`$. If all draws are independent conditional on the target, both sources supply the same joint classical–quantum training state

```math
\tau_{P,\gamma}^{\otimes T}.
```

For any allowed joint POVM $`\{F_o\}`$, both therefore give outcome probabilities

```math
\Pr(o\mid P)=\operatorname{Tr}\!\left(F_o\tau_{P,\gamma}^{\otimes T}\right).
```

The equality also holds for arbitrary quantum channels followed by measurements, including adaptive processing and retention of a quantum model. It is simply linearity of quantum operations applied to the identical input state. An analogous statement includes the independent test specimen.

The reduction in [Computational hardness](computational_hardness.md) uses an efficiently sampled Clifford to prepare a convenient hidden-parity ensemble. Some vectors in that ensemble can be entangled. This does not strengthen the learner's interface: conditional on the hidden target, the supplied density operators and all their independent tensor products are exactly those of the product preparation above.

The independence and access assumptions matter. A source that supplies a classical description of each prepared vector, a coherent preparation oracle, or repeated copies of the same latent pure draw supplies a different interface. In particular, averaging independent draws gives $`(\mathbb E|\psi\rangle\langle\psi|)^{\otimes r}`$, whereas repeated copies of one draw give $`\mathbb E(|\psi\rangle\langle\psi|)^{\otimes r}`$; these expressions need not agree. None of that extra information is present here.

## 4. Prediction after the target is known

The model output by the clean Bell learner is a classical list of local axes and one sign. On a fresh specimen, measure $`R_i`$ for each $`i\in J`$ and output the product of the outcomes times $`\sigma`$. This is a measurement of $`P`$, so its clean prediction error is exactly zero whenever the identified target is correct.

The learned description uses $`2n+1`$ bits in the symplectic representation. Prediction requires at most $`n`$ single-qubit Pauli measurements and a classical parity calculation. Consequently, the computational obstruction at fixed positive annotation noise concerns training, despite inexpensive source preparation and inexpensive deployment once the target is available.

For an additional reduction using only local Cliffords, at the price of changing the target prior, see [The local-prior variant](local_prior.md). The uniform-prior source proved here already uses product states; that variant is not needed to establish this fact.

## Verification and connections

The numerical checks in [Verification](../verification/README.md) explicitly construct the product vectors, average their projectors, and compare the result with the claimed density operator for all signed nonidentity Paulis through three qubits. These finite checks expose sign, normalization, and identity-factor mistakes; the eigenspace argument above proves the statement for arbitrary $`n`$.

Continue to [Bell learning](bell_learning.md) for the coherent measurement mechanism, or [Interpretation](interpretation.md) for the distinction between entanglement in data and coherent access during learning.
