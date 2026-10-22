# From quantum specimens to a noisy parity problem

## 1. A two-qubit learning task

Imagine an apparatus that hands a learner two qubits and a label, positive or negative. For this worked example, the hidden rule is: measure the first qubit in the $`X`$ basis, measure the second in the $`Z`$ basis, and multiply their two signs. The learner must discover this rule from examples and use it to label a fresh pair of qubits.

A $`Z`$ measurement gives $`+1`$ on the state $`|0\rangle`$ and $`-1`$ on $`|1\rangle`$. An $`X`$ measurement gives those respective signs on

```math
|+\rangle=\frac{|0\rangle+|1\rangle}{\sqrt2},
\qquad
|-\rangle=\frac{|0\rangle-|1\rangle}{\sqrt2}.
```

The notation $`|+0\rangle`$ means that the first qubit is prepared as $`|+\rangle`$ and the second as $`|0\rangle`$. This is a product state: each qubit has its own pure state, without entanglement between them.

The source chooses the clean class sign $`Y`$ by a fair coin and then chooses equally between the two preparations in its row:

| Clean class | Possible specimens | Product of the correct measurement outcomes |
|---|---|---|
| $`Y=+1`$ | $`\lvert+0\rangle`$ or $`\lvert-1\rangle`$ | $`(+1)(+1)=(-1)(-1)=+1`$ |
| $`Y=-1`$ | $`\lvert+1\rangle`$ or $`\lvert-0\rangle`$ | $`(+1)(-1)=(-1)(+1)=-1`$ |

The learner receives the physical specimen and its recorded label. The preparation names in this table are explanatory information for us; the apparatus does not disclose them. Every example is an independent draw, and the learner gets one specimen from that draw.

The hidden measurement is written $`P=X\otimes Z`$. The tensor product $`\otimes`$ assigns an operator to each qubit. Once $`P`$ is known, prediction is easy and perfectly accurate on this clean source. The scientific question concerns the resources needed to learn it when the measurement rule is initially unknown.

### Describing an unknown preparation

A density operator is a matrix that summarizes the probabilities of every possible measurement on a quantum system. A pure vector $`|\psi\rangle`$ has density operator $`|\psi\rangle\langle\psi|`$. Randomly choosing pure preparations gives their probability-weighted average. For the positive row,

```math
\rho^0_{+,P}
=\frac12|+0\rangle\langle+0|
+\frac12|-1\rangle\langle-1|
=\frac{I+X\otimes Z}{4}.
```

The negative row similarly gives $`\rho^0_{-,P}=(I-X\otimes Z)/4`$. The identity $`I`$ acts on the four-dimensional two-qubit space. The denominator makes the trace, the sum of the diagonal entries, equal to one.

A general measurement is described by positive operators $`F_o`$, one for each outcome, summing to $`I`$. Its outcome probability is $`\Pr(o)=\mathrm{Tr}(F_o\rho)`$. Such a collection is called a POVM. This linear dependence on $`\rho`$ explains why two different preparation ensembles with the same density operator are indistinguishable through their supplied specimens. Independence matters too: two fresh draws have state $`\rho\otimes\rho`$, which can differ from two replicas of one hidden draw.

The educational anchor is John Watrous's [*The Theory of Quantum Information* (2018)](https://cs.uwaterloo.ca/~watrous/TQI/). The author-hosted [Chapter 2 manuscript](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf), particularly §§2.1.2 and 2.3.1, supplies the state and measurement framework. The [anchor bridge](ANCHOR_BRIDGE.md) gives precise reading locations and translates notation. The explanations here supply the ingredients as they become necessary.

The same source extends to $`n`$ qubits. A target $`P`$ is a tensor product of Pauli operators, with an overall sign. A factor $`I`$ means that qubit does not enter the outcome product. Choosing local eigenstates with one parity constraint gives

```math
\rho^0_{Y,P}=\frac{I+YP}{d},
\qquad d=2^n.
```

Every realized specimen can still be a pure product state. The main theorem draws $`P`$ uniformly from all $`M=2(4^n-1)`$ signed nonidentity Paulis. Its lower bounds concern average performance over that prior, rather than a promise that every individually specified target is difficult.

**Further connections:** [M02–M05](MILESTONES.md#m02), [M15–M16](MILESTONES.md#m15); [source preparation and ensemble equivalence](../science/source_preparation.md); [canonical model](../science/model.md).

## 2. Corrupting the annotation leaves the specimen unchanged

After preparing a clean specimen, let the source flip its recorded label with probability $`\eta<1/2`$. Write

```math
C=YE,
\qquad
\Pr(E=-1)=\eta,
\qquad
\gamma=1-2\eta.
```

Here $`C`$ is the recorded sign and $`E`$ is an independent error sign. The contrast $`\gamma`$ measures how much correlation remains between the recorded and clean labels. With ten-percent annotation errors, $`\gamma=0.8`$.

Conditioning on a recorded positive label mixes the two clean classes with weights $`1-\eta`$ and $`\eta`$. For either recorded sign,

```math
\rho_{C,P,\gamma}
=(1-\eta)\rho^0_{C,P}+\eta\rho^0_{-C,P}
=\frac{I+C\gamma P}{d}.
```

Thus the observer's conditional state becomes less informative even though the source prepares exactly the same vectors. Ignoring the annotations altogether gives the feature marginal $`I/d`$, independent of the target. The useful information lies in the label–feature correlation.

For the proofs, a recorded sign can be stored as a classical bit $`c`$, with $`C=(-1)^c`$. Including that bit produces

```math
\tau_{P,\gamma}
=\frac12\sum_{c=0}^1|c\rangle\langle c|
\otimes\frac{I+(-1)^c\gamma P}{d}
=\frac{I_D+\gamma Z_C\otimes P}{D},
\qquad D=2d.
```

The label register is block diagonal: it represents an ordinary recorded bit. This notation gives the learner no superposition of labels or coherent example oracle.

The test task always uses a fresh clean label. We measure performance by the advantage $`a=\Pr(\widehat Y=Y)-1/2`$, averaged over the target, source draws, and learner's outcomes. A model may be a quantum state that is consumed by one prediction. Identifying $`P`$ with error at most $`\delta`$ is a stronger sufficient guarantee: it gives clean prediction success at least $`1-\delta`$. The lower bounds will address prediction itself. The noise rate may be known to the learner; the computational hardness statement allows that knowledge too.

**Further connections:** [M01](MILESTONES.md#m01), [M06](MILESTONES.md#m06), [M17](MILESTONES.md#m17); [model and single-test identity](../science/model.md).

## 3. Bell measurements reveal relations between examples

Suppose two independent specimens arrive. An individual-example learner measures the first and retains only classical outcomes. A coherent learner may keep its quantum state until the second arrives and perform a joint measurement. Bell measurement is a particularly useful joint measurement.

On a pair of qubits, the two operators $`X\otimes X`$ and $`Z\otimes Z`$ commute, even though $`X`$ and $`Z`$ on one qubit do not. A Bell measurement reads their two signs simultaneously. Calling those signs $`u`$ and $`v`$, it also determines the sign of the third Pauli correlation, because

```math
(X\otimes X)(Z\otimes Z)
=-Y_{\mathrm P}\otimes Y_{\mathrm P}.
```

Here $`Y_{\mathrm P}`$ denotes the Pauli operator, distinct from the class sign $`Y`$. Its correlation sign is $`-uv`$. The minus sign is essential.

For our two-qubit specimens, Bell-measure the first qubit of one specimen together with the first qubit of the other, and do the same for the second qubits. If the hidden target is $`X\otimes Z`$, the first Bell outcome supplies the $`X\otimes X`$ sign and the second supplies the $`Z\otimes Z`$ sign. Their product equals $`Y_1Y_2`$. The operation has extracted an exact relation between the two clean labels.

### Keeping track of the Pauli $`Y`$ sign

Binary coordinates make this general. At each site, encode $`I,X,Z,Y_{\mathrm P}`$ by $`(a_j,b_j)=(0,0),(1,0),(0,1),(1,1)`$. A Pauli word has coordinates $`p=(a,b)`$. Its canonical Hermitian representative is

```math
W_p=i^{\sum_j a_jb_j}X^aZ^b.
```

Here $`i^2=-1`$, and the exponent is an integer sum. Define $`q(p)=\sum_j a_jb_j\pmod2`$, the parity of its number of Pauli $`Y`$ factors. Matrix transposition preserves $`X`$ and $`Z`$ but reverses $`Y_{\mathrm P}`$, so $`W_p^T=(-1)^{q(p)}W_p`$.

Label Bell outcomes by $`z=(a_z,b_z)`$, so their local $`X\otimes X`$ and $`Z\otimes Z`$ signs are $`(-1)^{b_{z,j}}`$ and $`(-1)^{a_{z,j}}`$. The exact clean relation is

```math
Y_1Y_2=(-1)^{q(p)+[p,z]},
\qquad
[p,z]=a\cdot b_z+b\cdot a_z\pmod2.
```

The dot products and addition here are modulo two. A useful phase check is the Bell state $`(|00\rangle+|11\rangle)/\sqrt2`$: its $`X\otimes X`$ and $`Z\otimes Z`$ signs are positive, while its $`Y_{\mathrm P}\otimes Y_{\mathrm P}`$ sign is negative. The offset $`q(p)`$ accounts for precisely this effect.

The Bell outcome $`z`$ is uniform when averaged over the two balanced clean labels. Disjoint pairs give independent uniform covariates. The overall target sign $`\sigma`$ in $`P=\sigma W_p`$ cancels when the two specimens are paired.

**Further connections:** [M08](MILESTONES.md#m08), [M18](MILESTONES.md#m18); [B1 and its Bell-basis proof](../science/bell_learning.md#b1--the-exact-bell-correspondence).

## 4. With correct labels, the equations determine the rule

Turn a product of label signs into a bit $`r`$ by writing $`Y_1Y_2=(-1)^r`$. Every clean Bell pair supplies an affine linear equation

```math
r=q(p)+(b,a)\cdot z\pmod2.
```

“Affine” means a linear equation with an additional constant term. There are $`2n`$ unknown linear coefficients and one constant. Gaussian elimination solves them once the observed equations have full rank.

For the two-qubit target, use the coordinate order $`z=(a_{z,1},a_{z,2},b_{z,1},b_{z,2})`$. The following is one possible full-rank set of clean observations:

| Bell covariate $`z`$ | Label-product bit $`r`$ |
|---|---:|
| $`0000`$ | $`0`$ |
| $`1000`$ | $`0`$ |
| $`0100`$ | $`1`$ |
| $`0010`$ | $`1`$ |
| $`0001`$ | $`0`$ |

The first row fixes the constant. Each remaining row isolates one coefficient. They recover $`r=a_{z,2}\oplus b_{z,1}`$, hence $`a=(1,0)`$, $`b=(0,1)`$, and $`W_p=X\otimes Z`$. These particular covariates need not appear; any full-rank set works.

One extra clean specimen determines the missing global sign. Measuring $`W_p`$ gives $`B=\sigma Y`$, so $`CB=\sigma`$ when annotations are correct. The five-pair example plus this calibration uses eleven specimens and produces a complete signed target description.

In general, $`O(n+\log(1/\delta))`$ random Bell pairs give full rank with probability at least $`1-\delta`$. Each Bell measurement uses $`O(n)`$ gates, and elimination is polynomial time. This proves the efficient clean learner K1. Prediction afterwards requires only the indicated local Pauli measurements and a product of their signs.

**Further connections:** [M09](MILESTONES.md#m09), [M19](MILESTONES.md#m19); [K1, including its rank bound](../science/bell_learning.md#k1--efficient-clean-learning).

## 5. Annotation errors turn the equations into noisy parity

With noisy annotations, the learner observes $`R=C_1C_2`$. Exactly one annotation flip reverses the relation; zero or two flips preserve it. Therefore

```math
R=(-1)^{q(p)+[p,z]}F,
\qquad
\Pr(F=-1)=\eta_B=2\eta(1-\eta),
\qquad
\mathbb EF=\gamma^2.
```

The noise is independent of the uniform covariate. At $`\eta=0.1`$, the Bell equation is wrong with probability $`0.18`$ and retains contrast $`0.64`$.

In bits, these are affine **learning-parity-with-noise**, or LPN, observations. A fixed hidden parity labels uniformly random inputs, and independent flips corrupt its answers. Exact elimination no longer guarantees the target: the observed equations may be inconsistent or select a wrong candidate.

Statistically, useful information remains. For each candidate $`p'`$, average the correlation $`R(-1)^{[p',z]}`$. The true candidate has mean of magnitude $`\gamma^2`$; every wrong unsigned candidate has mean zero. Concentration and a union bound over fewer than $`4^n`$ candidates give recovery with $`O(n/\gamma^4)`$ pairs at fixed confidence. Fresh annotated measurements calibrate the global sign.

This explicit decoder scans exponentially many candidates. Its modest specimen count does not make its runtime efficient. Also, its fourth-power contrast dependence describes this protocol; the unrestricted collective optimum will have a second-power dependence.

The Bell correspondence alone says nothing decisive about a different quantum strategy. A separate reduction is needed to constrain every efficient learner.

**Further connections:** [M13](MILESTONES.md#m13), [M20](MILESTONES.md#m20); [explicit noisy decoder and computational connections](../science/bell_learning.md).

## 6. Measuring specimens separately has an exponential cost

An individual-example learner may choose any POVM on each incoming example, adapt its choice using all previous outcomes, and perform unlimited classical computation. Its restriction is that quantum information cannot persist between examples. A persistent quantum ancilla interacting with successive specimens would change that model.

Why can this matter when the source uses product states? For one fixed target, the two class density operators commute. Across the possible unknown targets, the relevant measurements do not all commute. The learner must acquire data before knowing which measurement direction will carry the label. Bell measurements preserve and compare information across specimens during acquisition.

The universal lower bound requires more than this intuition. The proof first shows that any normalized measurement vector has average squared Pauli overlap at most $`1/(d+1)`$. The average is over the unknown unsigned target. It then represents an adaptive protocol by its tree of classical outcomes. At a fixed transcript, the likelihood is a product of conditional factors. Averaging both target signs and controlling the few large overlaps gives a bound on the transcript's total variation from a target-independent null source. Total variation limits the probability difference of every event.

Append a clean test specimen to this proof experiment and consider the event “prediction agrees with its withheld label.” Its probability is $`1/2+a`$ for the learning source and exactly $`1/2`$ for the null. The result is

```math
a\leq\frac{5(T\gamma^2+1)}{d+1}.
```

The extra one accounts for that clean test. For a fixed positive average advantage and sufficiently large $`n`$, this requires $`T=\Omega(2^n/\gamma^2)`$ training specimens. Here $`\Omega`$ means a lower bound up to a constant factor. Even unlimited classical processing cannot overcome this acquisition restriction.

The clean label used in this analytical comparison is part of the clean prediction objective. It does not give an actual learner a way to manufacture clean labels from noisy training data.

**Further connections:** [M04](MILESTONES.md#m04), [M10](MILESTONES.md#m10), [M22–M24](MILESTONES.md#m22); [S2 and the complete adaptive proof](../science/individual_measurements.md).

## 7. Coherent prediction needs and suffices with a linear sample count

The unrestricted coherent learner can retain training registers and perform a joint measurement when the test arrives. Its optimum is $`\Theta(n/\gamma^2)`$ specimens for any fixed positive advantage: both an upper and a lower bound of that order hold. Two different discrimination arguments establish this result.

### Showing that enough data exists

Consider all $`M`$ possible target states $`\tau_{P,\gamma}^{\otimes T}`$ as a known list of hypotheses. The learner knows the list, although it does not know which entry generated its data. A **pretty-good measurement**, or PGM, turns this list and its average state into a valid identification POVM. It is a mathematical specification of a measurement; finding or implementing an efficient circuit for it is a further problem.

Pairwise overlap controls its error. The relevant overlap is root fidelity,

```math
f(\rho,\sigma)=\|\sqrt\rho\sqrt\sigma\|_1.
```

For normalized states it lies between zero and one; identical states have value one, and orthogonal supports give zero. Independent copies multiply this overlap. For distinct targets here, $`f\leq\sqrt{1-\gamma^2/2}`$, so their $`T`$-copy overlaps shrink exponentially with $`T\gamma^2`$. The operative PGM bound gives

```math
\Pr(\text{identification error})
\leq(M-1)e^{-T\gamma^2/4}.
```

Although $`M`$ is exponential in $`n`$, its logarithm is linear. Thus $`O((n+\log(1/\delta))/\gamma^2)`$ examples suffice for identification error $`\delta`$, and therefore for good clean prediction. All states and measurement effects can remain block diagonal in the annotations: the measurement reads the classical labels and acts conditionally on the feature registers.

Watrous's [Chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf), §§3.1.2 and 3.2, explains the PGM and fidelity framework. His symbol $`F`$ denotes the root fidelity called $`f`$ here. The particular pairwise-error inequality used above is sourced separately in the [canonical collective proof](../science/collective_statistics.md); it is not a consequence attributed to the book's PGM performance theorem alone.

### Bounding prediction without demanding identification

A learner might predict well while never naming the target. To include it, compare the joint input states for the two possible clean test labels:

```math
\Omega_\pm=
\frac1M\sum_P\tau_{P,\gamma}^{\otimes T}
\otimes\frac{I\pm P}{d}.
```

These states include all training inputs and the fresh test feature. Any training procedure followed by one prediction is a binary measurement on these inputs. This includes a stored quantum model consumed during prediction.

The Holevo–Helstrom theorem, Watrous §3.1.1, Theorem 3.4, says that the optimal advantage is $`\|\Omega_+-\Omega_-\|_1/4`$. For a Hermitian matrix, the trace norm is the sum of the absolute values of its eigenvalues; here it measures the best observable distinction between the two possibilities.

Let $`X_T=(\Omega_+-\Omega_-)/2`$. Pauli orthogonality makes its squared trace calculation particularly simple: only equal and opposite targets survive. An exact calculation of $`\mathrm{Tr}(X_T^2)`$, followed by a norm inequality, gives

```math
a_T^*\leq\frac12
\sqrt{\frac{(1+\gamma^2)^T-(1-\gamma^2)^T}{M}}
\qquad(T\geq1).
```

This is a bound on optimal advantage, not its exact finite-sample value. For fixed positive advantage, the growing numerator must compensate for exponentially large $`M`$, requiring order $`n/\gamma^2`$ samples. Together with the PGM construction, this proves S1 directly for the prediction objective.

**Further connections:** [M11–M12](MILESTONES.md#m11), [M25–M27](MILESTONES.md#m25); [S1, exact second moment, and PGM proof](../science/collective_statistics.md); [notation and source bridge](ANCHOR_BRIDGE.md).

## 8. A single useful quantum prediction would distinguish classical LPN

The runtime theorem starts from ordinary **classical** samples

```math
(x,b),\qquad b=s\cdot x\oplus e,
```

where $`s`$ is a fixed hidden $`k`$-bit secret, $`x`$ is uniform, and $`e`$ is an independent noise bit. Decision-LPN asks whether the samples have this form or whether every $`b`$ is an independent fair bit. The assumption is that, at the chosen fixed positive noise rate, no quantum polynomial-time algorithm using polynomially many classical samples can distinguish those cases with nonnegligible advantage. “Negligible” means eventually smaller than the reciprocal of every polynomial. This is an assumption about quantum algorithms, beyond hardness for classical computation alone.

To connect it to our task, set $`n=k+1`$. Choose one random Clifford circuit $`U`$ and keep its description from the learner. Clifford conjugation maps Pauli operators to Pauli operators; uniform randomization makes

```math
P=UZ^{(s,1)}U^\dagger
```

uniform over the signed nonidentity targets. Here $`Z^{(s,1)}`$ places a $`Z`$ factor wherever the bit string $`(s,1)`$ has a one and an identity elsewhere; its final one ensures a nonidentity target. The reduction does not know $`s`$ or $`P`$. Nevertheless, for each observed pair $`(x,b)`$ it can draw a fair bit $`c`$, prepare

```math
U|x,b\oplus c\rangle,
\qquad C=(-1)^c,
```

and supply that specimen with its annotation.

The key independence check uses the latent clean bit $`y=e\oplus c`$. Since $`c`$ is fair, $`y`$ is fair and independent of $`e`$. The prepared vector is $`U|x,s\cdot x\oplus y\rangle`$. Averaging over $`x`$ at fixed $`y`$ gives exactly $`(I+YP)/d`$, and $`c=y\oplus e`$ gives the required independent annotation flip. Under the uniform null, the feature is $`I/d`$ independently of $`c`$.

This simulation uses a convenient ensemble whose individual vectors may be entangled. It supplies the same conditional density operators and independent tensor products as the product source in Section 1. Because no hidden preparation descriptions or replicas are supplied, every allowed learner has the same probabilities on those ensembles.

Now suppose an efficient learner achieved clean success $`1/2+a`$. Prepare one additional example, withhold its annotation, and ask for one prediction. Accept the LPN case if that prediction matches the withheld recorded sign. In the LPN case,

```math
\Pr(\widehat Y=C)
=(1-\eta)\left(\frac12+a\right)
+\eta\left(\frac12-a\right)
=\frac12+\gamma a.
```

In the null case, the withheld label is fair and independent of the whole model and test specimen, so agreement is exactly $`1/2`$. One useful prediction therefore gives an ideal distinguishing gap $`\gamma|a|`$. The model can be arbitrary and can be consumed completely: no repeated inference or extraction of a classical hypothesis is required.

The simulation has polynomial overhead. Strict bounded-runtime Clifford sampling incurs only negligible loss, as detailed in H1. At a fixed rate $`\eta\in(0,1/2)`$, $`\gamma`$ is a positive constant, so a nonnegligible clean advantage contradicts the quantum decision-LPN assumption. This rules out every efficient learner under that assumption, rather than only decoders of Bell observations.

**Further connections:** [M07](MILESTONES.md#m07), [M13](MILESTONES.md#m13), [M28–M29](MILESTONES.md#m28); [H1 and complete simulation](../science/computational_hardness.md).

## 9. Putting samples, memory, and time together

For the same target prior, source, and fixed positive clean prediction advantage, the proved comparison is:

| Training setting | Specimen requirement | Computational statement |
|---|---:|---|
| Correct annotations and Bell learning | $`O(n)`$ | Polynomial training time |
| Noisy annotations and unrestricted coherent processing | $`\Theta(n/\gamma^2)`$ | A successful collective measurement exists |
| Noisy annotations and individual-example measurements | $`\Omega(2^n/\gamma^2)`$ | Unlimited classical computation is allowed |
| Fixed positive noisy annotations and polynomial-time coherent processing | Polynomially many specimens give only negligible advantage under H1 | Conditional on quantum decision-LPN hardness |

At fixed noise below one half, coherent processing retains an exponential sample advantage. Under the computational assumption, that advantage cannot be accessed by an efficient learner at the specified hard rate. These are compatible statements about different resources. The individual-example baseline already permits quantum measurements; the sample comparison measures the value of coherent access across specimens.

There is also a positive regime between clean labels and fixed noise. An algorithm can try small batches of Bell equations, solve batches that are consistent, and validate their candidates on fresh observations. A batch has a useful chance of being entirely uncorrupted when noise is sufficiently small. The resulting cost is

```math
\exp(O(\eta n))\,
\mathrm{poly}(n,\gamma^{-1},\log(1/\delta)).
```

It is polynomial when $`\eta=O(\log n/n)`$. Thus the fixed-rate hardness theorem does not imply hardness for every positive noise sequence. At the other endpoint, $`\eta=1/2`$, training becomes target-independent and no amount of data restores average prediction advantage.

The scope remains specific: ideal quantum operations, independent annotation flips, one independent specimen per datum, a prescribed target prior, and clean quantum-input prediction. No latent descriptions, repeated preparations of a requested hidden vector, or coherent example oracle are available. The source can be prepared locally, and an identified target can be deployed through local measurements. Those conveniences coexist with the conditional obstruction to discovering the target efficiently.

The [interpretation chapter](../science/interpretation.md) develops these boundaries. The [related-work account](../references/RELATED_WORK.md) attributes Bell sampling, quantum-memory separations, state-discrimination bounds, and noisy-parity reductions to their antecedents. The [local-prior variant](../science/local_prior.md) shows how a different prior permits a local-only reduction while changing the quantitative memory bound.

**Further connections:** [M14](MILESTONES.md#m14), [M21](MILESTONES.md#m21), [M30](MILESTONES.md#m30); [clean-batch proof](../science/bell_learning.md#vanishing-noise-a-clean-batch-algorithm); [canonical result index](../science/model.md); [Watrous bridge](ANCHOR_BRIDGE.md).
