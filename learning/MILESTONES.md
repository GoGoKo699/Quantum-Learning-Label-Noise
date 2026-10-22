# A map of the scientific argument

This map has exactly 30 milestones, divided into two phases. Each milestone identifies a central question, an understanding target, its dependencies and role in the argument, a conceptual connection, and sources for the underlying science.

The first **14 milestones are background and preliminaries**. This allocation reflects the meeting of three subjects: quantum states and measurements, statistical learning, and computational reductions. The phase begins with bits and individual quantum objects, then assembles the framework needed to compare specimen count, coherent memory, and runtime.

The remaining **16 milestones form the narrative and innovation phase**. They begin with the source and its local preparation, build the Bell algorithms and the two statistical arguments, and then prove the computational reduction. The final milestone combines those results for one fixed supervised task. “Innovation” names this phase's role in explaining the project's contribution; the [related-work account](../references/RELATED_WORK.md) identifies the established ingredients throughout.

The map covers the load-bearing ideas and assumptions. Full proofs, exact constants, and specialist details remain in the canonical science chapters. Source pointers lead to those chapters and the primary literature.

## Phase I — Background and preliminaries

<a id="m01"></a>
### M01 — Bits, parities, and independent flips

**Central question.** How does a parity bit encode a relation among many bits, and how does independent label noise weaken that relation?

**Understanding target.** Interpret addition modulo two as XOR, distinguish a bit $`c`$ from its sign $`(-1)^c`$, and explain why an independent flip at rate $`\eta`$ multiplies a sign correlation by $`\gamma=1-2\eta`$. Recognize that multiplying two independently flipped signs squares this contrast.

**Dependencies and story role.** No earlier milestone is required. This establishes the classical language used by both the source labels and the later noisy-parity reduction.

**Conceptual connection.** A parity is simultaneously a linear equation over $`\mathbb F_2`$ and a product of signs. That translation connects binary linear algebra to quantum measurement outcomes.

**Source pointers.** [Model: Pauli conventions and corrupted annotations](../science/model.md); [Bell learning: B1](../science/bell_learning.md); [Computational hardness: decision-LPN definition](../science/computational_hardness.md).

<a id="m02"></a>
### M02 — Pauli operators and their binary coordinates

**Central question.** How can a tensor product of qubit measurements be represented by a short binary string without losing its phase or sign?

**Understanding target.** Relate $`I,X,Y,Z`$ to binary coordinates, distinguish the unsigned Hermitian representative $`W_p`$ from the signed target $`P=\sigma W_p`$, and explain the roles of the integer phase exponent, the transpose bit $`q(p)`$, and the symplectic commutation bracket. Understand why different unsigned Pauli words are orthogonal as operators.

**Dependencies and story role.** Uses [M01](#m01). This supplies the individual observables and algebraic identities on which every later construction rests.

**Conceptual connection.** Operator multiplication and commutation can be tracked through finite-field geometry, while the global sign still carries the orientation of a classifier's labels.

**Source pointers.** [Model: §1](../science/model.md); [Bell learning: Bell basis and phase conventions](../science/bell_learning.md).

<a id="m03"></a>
### M03 — Pure preparations, mixtures, and independent specimens

**Central question.** What information does a density operator retain about a source whose individual realizations are pure states?

**Understanding target.** Distinguish a hidden preparation ensemble from the density operator available to an observer. Explain why different ensembles with the same density operator give identical measurement probabilities, and why independent draws yield tensor powers of the average state. Distinguish this interface from repeated copies of one fixed latent draw.

**Dependencies and story role.** Uses [M02](#m02) for examples of eigenstates. This introduces the physical meaning of the data before discussing what a learner can do with it.

**Conceptual connection.** Classical uncertainty in preparation can make the accessible state mixed even when every realized specimen is pure and unentangled.

**Source pointers.** [Source preparation: §§1–3](../science/source_preparation.md); [Model: clean specimens and access](../science/model.md).

<a id="m04"></a>
### M04 — Measurements, channels, and retained quantum information

**Central question.** What changes when a learner can retain a quantum specimen until another specimen arrives?

**Understanding target.** Read a POVM as a rule assigning probabilities to outcomes, and understand that general processing followed by a classical output induces a POVM on the supplied inputs. Distinguish an adaptive sequence of individual-example measurements with classical storage from coherent processing with persistent quantum memory. Allow temporary ancillas within one measurement without confusing them with memory across examples.

**Dependencies and story role.** Uses [M03](#m03). This establishes the operational resource distinction that the sample lower bound will quantify.

**Conceptual connection.** A classical transcript records the result of a measurement choice; retaining a quantum system preserves access to other joint measurements that were not made at acquisition time.

**Source pointers.** [Model: access and resource accounting](../science/model.md); [Individual measurements: definitions and allowed protocols](../science/individual_measurements.md); [CCHL2021](../references/RELATED_WORK.md#cchl2021).

<a id="m05"></a>
### M05 — Prediction risk, target identification, and averaging

**Central question.** What exactly must a learner accomplish, and over which randomness is its performance evaluated?

**Understanding target.** Distinguish one fresh-label prediction from recovery of the hidden target. Interpret average clean advantage $`a=\Pr(\widehat Y=Y)-1/2`$, high-probability identification, and a guarantee for every target. Explain why correct identification implies good prediction, while a good predictor need not expose a reusable target description.

**Dependencies and story role.** Uses [M01](#m01), [M03](#m03), and [M04](#m04). This fixes the success criterion before importing statistical or computational techniques.

**Conceptual connection.** A trained quantum state can function as a consumable prediction program. Its performance is meaningful even when no classical hypothesis is extracted from it.

**Source pointers.** [Model: prediction and identification; single-test identity](../science/model.md); [Collective statistics: binary state-test formulation](../science/collective_statistics.md).

<a id="m06"></a>
### M06 — Classical annotations inside a quantum statistical model

**Central question.** How can a classical label be represented alongside a quantum feature without granting coherent access to labels?

**Understanding target.** Read a classical–quantum state as a block-diagonal mixture indexed by a recorded bit. Explain conditioning on a corrupted annotation, distinguish noise in that bit from noise on a quantum device, and use independence to obtain $`R_\eta=\eta+\gamma R_0`$ for an independently evaluated classifier.

**Dependencies and story role.** Uses [M01](#m01), [M03](#m03), and [M05](#m05). This combines the classical noise channel with the quantum data interface.

**Conceptual connection.** Annotation corruption can leave the population-optimal clean classifier unchanged while weakening the information available to discover it.

**Source pointers.** [Model: corrupted annotations and single-test identity](../science/model.md); [Interpretation: label noise and population risk](../science/interpretation.md).

<a id="m07"></a>
### M07 — Clifford transformations and hidden measurement bases

**Central question.** How does an efficiently implementable change of basis turn one Pauli direction into an unknown direction drawn from a prescribed prior?

**Understanding target.** Explain that Clifford conjugation permutes signed Pauli operators, that the action on nonidentity signed Paulis is transitive, and that a random Clifford can produce a uniform target without revealing its identity to the learner. Distinguish the preparer's knowledge of a circuit from the learner's access to that circuit.

**Dependencies and story role.** Uses [M02](#m02)–[M04](#m04). This supplies the bridge between an algebraic parity instance and a quantum specimen source.

**Conceptual connection.** Random basis changes preserve the structure that makes a reduction possible while making the resulting learning distribution match the target prior.

**Source pointers.** [Computational hardness: randomizing the target](../science/computational_hardness.md); [Koenig–Smolin2014](../references/RELATED_WORK.md#ks2014).

<a id="m08"></a>
### M08 — Bell measurements as measurements of correlations

**Central question.** What does a joint Bell measurement reveal that a predetermined single-specimen basis need not reveal?

**Understanding target.** Interpret the maximally entangled Bell basis and the identity $`\langle\Phi_d|A\otimes B|\Phi_d\rangle=\operatorname{Tr}(A^TB)/d`$. Explain how the transpose sign of a Pauli enters the outcome relation and why the Bell circuit acts across two independently supplied feature registers.

**Dependencies and story role.** Uses [M02](#m02)–[M04](#m04). This introduces the concrete coherent measurement that will make the clean algorithm efficient.

**Conceptual connection.** Entanglement can be a property of a measurement on independently prepared data, even when it is absent from every source specimen.

**Source pointers.** [Bell learning: Bell basis and phase conventions](../science/bell_learning.md); [HKP2021, Appendix E.2](../references/RELATED_WORK.md#hkp2021).

<a id="m09"></a>
### M09 — Random linear equations and reliable empirical correlations

**Central question.** When do random observations determine a hidden parity, and how can noisy observations certify a candidate?

**Understanding target.** Distinguish affine rank from the mere number of equations. Explain the balanced-affine-function union bound for random design rows, and understand how concentration plus a union bound controls many empirical correlations at once. Keep sample count, confidence, and the cost of enumerating candidates separate.

**Dependencies and story role.** Uses [M01](#m01) and [M05](#m05). This supplies the classical statistical tools for exact recovery, exhaustive decoding, and clean-batch validation.

**Conceptual connection.** A small number of observations can identify one of exponentially many candidates statistically, even when evaluating those candidates individually takes exponential time.

**Source pointers.** [Bell learning: K1, noisy statistical decoder, and clean-batch algorithm](../science/bell_learning.md).

<a id="m10"></a>
### M10 — Adaptive transcripts and statistical distinguishability

**Central question.** How can one bound every adaptive individual-example strategy without listing all its measurements?

**Understanding target.** Interpret a measurement protocol as a tree of classical outcomes. At a fixed transcript, treat the chosen measurement vectors as fixed and express the likelihood ratio as a product of conditional likelihoods. Explain total variation as the largest possible event-probability difference and why refining outcomes can only help distinguish distributions.

**Dependencies and story role.** Uses [M03](#m03), [M04](#m04), and [M09](#m09). This supplies a universal language for the individual-example lower bound.

**Conceptual connection.** Adaptivity changes the tree's branches but does not remove the possibility of a pointwise bound that holds at every leaf.

**Source pointers.** [Individual measurements: transcript comparison and likelihood refinement](../science/individual_measurements.md); [CCHL2021](../references/RELATED_WORK.md#cchl2021).

<a id="m11"></a>
### M11 — Quantum distinguishability and prediction operators

**Central question.** How can the best possible binary prediction be expressed directly as a property of two quantum states?

**Understanding target.** Explain equal-prior Helstrom discrimination, the trace norm, and the use of a Hilbert–Schmidt second moment to bound that norm. Distinguish trace distance from root fidelity, and distinguish root fidelity from the convention that calls its square “fidelity.”

**Dependencies and story role.** Uses [M03](#m03)–[M05](#m05). This provides the quantum counterpart of classical distinguishability and prepares both sides of the collective statistical theorem.

**Conceptual connection.** Prediction with an arbitrary trained quantum model can be studied as one state-discrimination problem on all training inputs and the fresh test register.

**Source pointers.** [Collective statistics: §§1–3](../science/collective_statistics.md); [Cheng et al.](../references/RELATED_WORK.md#cheng2024).

<a id="m12"></a>
### M12 — Many-hypothesis discrimination and the pretty-good measurement

**Central question.** How can one show that many possible targets are distinguishable without constructing an efficient decoder?

**Understanding target.** Read the pretty-good measurement as a POVM defined from an ensemble and its average state. Explain why small pairwise root fidelities of tensor powers give an identification-error bound, and why specifying that POVM does not establish a polynomial-size implementation. Understand why block-diagonal label states permit a label-conditioned measurement.

**Dependencies and story role.** Uses [M04](#m04), [M06](#m06), and [M11](#m11). This assembles the upper-bound machinery for unrestricted statistical learning.

**Conceptual connection.** A measurement-existence argument resolves data sufficiency while leaving the computation required to use that data open.

**Source pointers.** [Collective statistics: collective PGM](../science/collective_statistics.md); [Barnum–Knill2002](../references/RELATED_WORK.md#barnum-knill2002); [Cheng et al., Appendix J](../references/RELATED_WORK.md#cheng2024).

<a id="m13"></a>
### M13 — Classical LPN and quantum computational reductions

**Central question.** What assumption is needed to turn a hypothetical efficient quantum learner into a contradiction?

**Understanding target.** Distinguish search-LPN from decision-LPN, classical samples from coherent quantum examples, and quantum polynomial-time hardness from classical computational hardness. Explain what a reduction must preserve: distribution, success criterion, sample count, runtime, and the information actually supplied to the learner.

**Dependencies and story role.** Uses [M01](#m01), [M05](#m05), [M07](#m07), and [M09](#m09). This introduces the assumption-dependent component alongside the unconditional statistical tools.

**Conceptual connection.** Efficient quantum preparation of states from classical samples does not turn the input into a coherent example oracle. Reductions must account for the given access interface.

**Source pointers.** [Computational hardness: assumption and theorem H1](../science/computational_hardness.md); [GL2022](../references/RELATED_WORK.md#gl2022); [Cross–Smith–Smolin2015](../references/RELATED_WORK.md#css2015).

<a id="m14"></a>
### M14 — A complete framework for quantum learning resources

**Central question.** Which resources and success criteria must be held fixed before two learning procedures can be compared?

**Understanding target.** Assemble the source, target prior, classical annotations, fresh test interface, measurement memory, specimen count, and total runtime into one operational problem. Distinguish a statistical upper bound, a measurement-resource lower bound, and a conditional computational lower bound. Identify the separate roles of quantum data, coherent processing, and efficient deployment.

**Dependencies and story role.** Integrates [M03](#m03)–[M13](#m13). It closes the background phase by turning separate tools into a framework for reading the main theorem package.

**Conceptual connection.** Sample advantage, computational advantage, and ease of using an already learned model are different properties of the same learning task.

**Source pointers.** [Model: access, result index, and resource comparison](../science/model.md); [Interpretation: one task, three resource questions](../science/interpretation.md); [Related work: operational comparisons](../references/RELATED_WORK.md).

## Phase II — Narrative and innovation

<a id="m15"></a>
### M15 — The fixed supervised Pauli task

**Central question.** What remains fixed when the annotation noise changes?

**Understanding target.** Explain the balanced clean classes $`(I\pm P)/d`$, the signed-uniform nonidentity target prior, and the independent clean test. Identify why the sign is part of the target, why the identity is excluded, and why a known target gives perfect classification. Keep the target class and physical feature source fixed across noise rates.

**Dependencies and story role.** Uses [M02](#m02), [M05](#m05), [M06](#m06), and [M14](#m14). This begins the main narrative with the exact object whose resources will be compared.

**Conceptual connection.** The experiment changes the reliability of training annotations while preserving both the target measurement and the achievable clean test error.

**Source pointers.** [Model: §§1–4 and canonical result index](../science/model.md).

<a id="m16"></a>
### M16 — Preparing every specimen as a product state

**Central question.** How can a parity-conditioned source realize the class density operators using only local state preparation?

**Understanding target.** Follow the pivot-bit construction that chooses local Pauli eigenstates subject to one parity constraint. Explain why the allowed product vectors form an orthonormal basis of the desired eigenspace and why their uniform mixture has the stated normalization. Account for identity factors, independent draws, and hidden preparation information.

**Dependencies and story role.** Uses [M02](#m02), [M03](#m03), and [M15](#m15). This makes the source physically explicit before analyzing the learning algorithms.

**Conceptual connection.** The data can be inexpensive pure product preparations while the learner still benefits from coherent measurements across independent specimens. Ensemble equivalence will later connect this implementation to the hardness reduction.

**Source pointers.** [Source preparation: parity-conditioned ensemble and two-qubit example](../science/source_preparation.md); [Model: source access](../science/model.md).

<a id="m17"></a>
### M17 — What conditioning on a noisy annotation does

**Central question.** Where does the contrast $`\gamma`$ appear when the prepared feature vectors are unchanged?

**Understanding target.** Derive $`\rho_{C,P,\gamma}=(I+C\gamma P)/d`$ and $`\tau_{P,\gamma}=(I_D+\gamma Z_C\otimes P)/D`$. Explain why the unannotated feature marginal is $`I/d`$, why labels are classical, and why the remaining target information is a label–feature correlation.

**Dependencies and story role.** Uses [M01](#m01), [M06](#m06), [M15](#m15), and [M16](#m16). This produces the common noisy input state for every subsequent theorem.

**Conceptual connection.** The mixedness of an observer's conditional state can increase because an annotation becomes unreliable, without any physical noise being applied to the specimen.

**Source pointers.** [Model: clean specimens and corrupted annotations](../science/model.md); [Source preparation: adding annotation noise](../science/source_preparation.md); [Interpretation: population risk and thermal representation](../science/interpretation.md).

<a id="m18"></a>
### M18 — Exact Bell conversion to affine noisy parity

**Central question.** Why does pairing two independent annotated specimens produce a uniform covariate and one noisy parity equation?

**Understanding target.** Follow B1 from the Bell expectation of $`P\otimes P`$ to the deterministic clean relation, the uniform Bell outcome $`Z`$, and the independent noise product $`E_1E_2`$. Explain the affine offset $`q(p)`$, the rate $`\eta_B=2\eta(1-\eta)`$, and the loss of the target's global sign.

**Dependencies and story role.** Uses [M01](#m01), [M02](#m02), [M08](#m08), and [M17](#m17). This is the concrete measurement mechanism linking the quantum task to parity learning.

**Conceptual connection.** A coherent two-specimen measurement reveals a linear relation without requiring the learner to know the target's single-specimen basis in advance.

**Source pointers.** [Bell learning: theorem B1 and proof](../science/bell_learning.md); [HKP2021](../references/RELATED_WORK.md#hkp2021).

<a id="m19"></a>
### M19 — Efficient recovery with correct annotations

**Central question.** How do exact Bell relations become a complete efficient learner, including label orientation?

**Understanding target.** Explain why $`O(n+\log(1/\delta))`$ Bell pairs give full affine rank with high probability, how Gaussian elimination recovers the unsigned Pauli, and why one additional clean example determines its sign. Account for source draws, gates, classical processing, output length, and deployment measurements.

**Dependencies and story role.** Uses [M05](#m05), [M09](#m09), and [M18](#m18). This proves K1 and establishes the efficient clean baseline that annotation noise will be compared against.

**Conceptual connection.** The training procedure uses coherent measurements, but the learned description and its later use can be elementary and classical except for local test measurements.

**Source pointers.** [Bell learning: theorem K1](../science/bell_learning.md); [Source preparation: prediction after the target is known](../science/source_preparation.md).

<a id="m20"></a>
### M20 — Statistical learnability with exhaustive noisy decoding

**Central question.** Why do corrupted Bell equations remain statistically useful even when the clean linear solver no longer applies?

**Understanding target.** Explain character orthogonality, the true candidate's correlation of magnitude $`\gamma^2`$, and the zero mean of wrong candidates. Use concentration to understand the $`O(n/\gamma^4)`$ specimen scale at fixed confidence, followed by sign calibration. Keep the exponential candidate search explicit and avoid treating the Bell cost as an optimal collective lower bound.

**Dependencies and story role.** Uses [M09](#m09), [M18](#m18), and [M19](#m19). This first exhibits the separation between statistical sufficiency and the computational cost of a particular algorithm.

**Conceptual connection.** Weak correlation can be detected from enough data while locating which of exponentially many directions carries it remains expensive.

**Source pointers.** [Bell learning: noisy statistical decoder](../science/bell_learning.md); [CGY2024](../references/RELATED_WORK.md#cgy2024).

<a id="m21"></a>
### M21 — An efficient regime for vanishing annotation noise

**Central question.** When is it feasible to find an accidentally clean batch of noisy equations and verify its solution?

**Understanding target.** Explain the independent events of a batch being clean and having full affine rank, why a correct candidate appears after $`\exp(O(\eta n))`$ trials, and how fresh validation separates it from incorrect candidates. Account for classical reuse of validation outcomes and fresh sign calibration. Understand the sufficient polynomial regime $`\eta=O(\log n/n)`$.

**Dependencies and story role.** Uses [M09](#m09), [M13](#m13), and [M20](#m20). This qualifies the clean/noisy comparison before the fixed-rate hardness theorem is introduced.

**Conceptual connection.** A fixed positive noise assumption does not imply hardness for every nonzero noise sequence; algorithmic behavior depends on how noise scales with dimension.

**Source pointers.** [Bell learning: clean-batch proposition and proof](../science/bell_learning.md); [Interpretation: noise regimes and limits](../science/interpretation.md).

<a id="m22"></a>
### M22 — The exact information moment of one example

**Central question.** How strongly can one arbitrary measurement direction correlate, on average, with the hidden signed-Pauli ensemble?

**Understanding target.** Follow the decomposition of a label–feature vector into its two label blocks and the Pauli-basis identity for its effective Hermitian operator. Explain why the supremum second moment is exactly $`\delta_*=1/(d+1)`$, including vectors entangled across registers, and identify a vector that attains it.

**Dependencies and story role.** Uses [M02](#m02), [M04](#m04), [M10](#m10), and [M17](#m17). This supplies the local quantitative restriction that will survive arbitrary adaptive individual measurements.

**Conceptual connection.** An average over exponentially many unknown Pauli directions limits the information aligned with any single measurement vector.

**Source pointers.** [Individual measurements: exact Pauli second moment](../science/individual_measurements.md); [CCHL2021](../references/RELATED_WORK.md#cchl2021).

<a id="m23"></a>
### M23 — From the local moment to an adaptive transcript bound

**Central question.** Why can classical feedback not accumulate useful information faster than the signed-Pauli moment bound allows?

**Understanding target.** Explain rank-one refinement, the product likelihood at a fixed leaf, clipping of large local correlations, and averaging over both target signs. Follow the resulting one-sided likelihood bound and its conversion to total variation. Understand why the proof allows different contrasts at different times and remains valid at contrast one.

**Dependencies and story role.** Uses [M10](#m10) and [M22](#m22). This converts a one-example moment into a universal statement about a complete adaptive measurement protocol.

**Conceptual connection.** Sign symmetry removes the first-order likelihood effect, while clipping controls logarithmic endpoints without excluding clean examples.

**Source pointers.** [Individual measurements: heterogeneous-contrast transcript lemma and proof](../science/individual_measurements.md); [CCHL2021](../references/RELATED_WORK.md#cchl2021).

<a id="m24"></a>
### M24 — The individual-example prediction lower bound

**Central question.** How does a bound on transcript distinguishability constrain a classifier's success on one fresh clean specimen?

**Understanding target.** Append a clean held-out example in the proof experiment, withhold its label before prediction, and compare the agreement event against the null experiment. Explain the bound $`a\leq5(T\gamma^2+1)/(d+1)`$ and the resulting $`\Omega(2^n/\gamma^2)`$ requirement. Identify why the additive one is a test-example contribution.

**Dependencies and story role.** Uses [M05](#m05), [M17](#m17), and [M23](#m23). This completes S2 for the actual prediction objective, with unlimited classical computation permitted.

**Conceptual connection.** The converse tests prediction directly, rather than requiring the learner to identify the target. Its analytical clean held-out label is distinct from the noisy label available to the later computational reduction.

**Source pointers.** [Individual measurements: theorem S2 and clean-prediction reduction](../science/individual_measurements.md); [Model: prediction criterion](../science/model.md).

<a id="m25"></a>
### M25 — The best coherent predictor as one binary measurement

**Central question.** How can all possible quantum training strategies be represented in one statistical optimization?

**Understanding target.** Form the joint training-and-test states conditioned on the clean test sign. Explain why arbitrary coherent training and consumable inference are contained in a binary POVM on these inputs, and why retaining all inputs attains the unrestricted optimum. Derive $`a_T^*=\|X_T\|_1/2`$ and explain why block-diagonal classical labels suffice.

**Dependencies and story role.** Uses [M04](#m04)–[M06](#m06), [M11](#m11), and [M17](#m17). This begins the collective analysis with the same prediction objective used by S2.

**Conceptual connection.** A learning problem with a quantum deployment input can be recast as state discrimination without imposing a classical or reusable learned model.

**Source pointers.** [Collective statistics: reduction of prediction to a binary state test](../science/collective_statistics.md); [Model: single-test identity](../science/model.md).

<a id="m26"></a>
### M26 — A direct collective prediction converse

**Central question.** Why does arbitrary coherent processing still require order $`n/\gamma^2`$ examples for a fixed prediction advantage?

**Understanding target.** Explain why Pauli orthogonality removes all terms in the second moment except equal and opposite targets. Follow the exact expression for $`\operatorname{Tr}(X_T^2)`$ and the dimension-dependent trace-norm inequality. Distinguish the exact Hilbert–Schmidt identity from the resulting finite-sample bound on optimal advantage.

**Dependencies and story role.** Uses [M02](#m02), [M11](#m11), and [M25](#m25). This proves the lower half of S1 directly for prediction.

**Conceptual connection.** The target's independent sign both makes prediction impossible without training and produces the subtraction between equal-target and opposite-target contributions in the second moment.

**Source pointers.** [Collective statistics: exact second moment and prediction converse](../science/collective_statistics.md); [Model: S1](../science/model.md).

<a id="m27"></a>
### M27 — Matching collective achievability by identification

**Central question.** Why is the collective prediction lower bound attainable with the same asymptotic number of examples?

**Understanding target.** Distinguish the opposite, commuting, and anticommuting Pauli cases in the pairwise root-fidelity calculation. Apply tensor-product multiplicativity and the PGM error bound to obtain $`O((n+\ln(1/\delta))/\gamma^2)`$ identification. Explain how this stronger guarantee yields prediction and completes the $`\Theta(n/\gamma^2)`$ result without promising efficient implementation.

**Dependencies and story role.** Uses [M11](#m11), [M12](#m12), [M25](#m25), and [M26](#m26). This closes S1 and enables a direct comparison with S2 at the same contrast and prediction advantage.

**Conceptual connection.** A prediction converse and an identification construction can match in sample order even though their finite-sample success criteria differ.

**Source pointers.** [Collective statistics: pairwise fidelities and PGM upper bound](../science/collective_statistics.md); [Cheng et al., Appendix J](../references/RELATED_WORK.md#cheng2024); [Barnum–Knill2002](../references/RELATED_WORK.md#barnum-knill2002).

<a id="m28"></a>
### M28 — Exact simulation of the noisy source from classical LPN

**Central question.** How can a reduction prepare the learner's examples without knowing the parity secret or the true labels?

**Understanding target.** Follow the preparation $`U|x,b\oplus c\rangle`$ from an LPN sample and a fresh uniform annotation bit. Explain why $`y=e\oplus c`$ is balanced and independent of $`e`$, why the conditional feature state is the required eigenspace mixture, and why the target is signed-uniform after Clifford randomization. Verify that the null input gives $`I_D/D`$ independently of its annotation.

**Dependencies and story role.** Uses [M07](#m07), [M13](#m13), [M16](#m16), and [M17](#m17). This constructs the exact distributional bridge needed for an all-learner computational theorem.

**Conceptual connection.** Hidden-variable reasoning establishes independence and label-noise structure even though the reduction never learns those hidden variables. Ensemble equivalence transfers the result to the pure product source.

**Source pointers.** [Computational hardness: H1 simulation, steps 1–3](../science/computational_hardness.md); [Source preparation: operational ensemble equivalence](../science/source_preparation.md); [Koenig–Smolin2014](../references/RELATED_WORK.md#ks2014).

<a id="m29"></a>
### M29 — One consumable prediction yields an LPN distinguisher

**Central question.** Why would any efficient clean predictor contradict the stated fixed-rate quantum decision-LPN assumption?

**Understanding target.** Withhold the annotation of one additional simulated example, obtain one prediction, and compare it with that annotation. Explain the ideal acceptance gap $`\gamma a`$, the exact one-half null agreement, and the polynomial preparation and inference overhead. Account for the negligible sampling loss in a strict bounded-runtime implementation, and preserve the fixed-positive-noise and quantum-hardness qualifications.

**Dependencies and story role.** Uses [M05](#m05), [M06](#m06), [M13](#m13), [M25](#m25), and [M28](#m28). This completes H1 without identifying the learned target or querying a model repeatedly.

**Conceptual connection.** The ability to make one useful prediction is already an operational distinguishing resource. Improper or consumable output models do not evade this reduction.

**Source pointers.** [Computational hardness: H1, held-out test, and runtime accounting](../science/computational_hardness.md); [Model: single-test identity](../science/model.md); [GL2022](../references/RELATED_WORK.md#gl2022); [PQS2026](../references/RELATED_WORK.md#pqs2026).

<a id="m30"></a>
### M30 — The combined sample, memory, and time separation

**Central question.** What does the complete theorem package establish for one fixed supervised source, and where do its conclusions stop?

**Understanding target.** Combine K1, B1, S1, S2, and H1: efficient clean learning; an exact noisy-parity Bell transcript; optimal collective sample count; an exponential individual-example obstruction; and conditional failure of efficient learning at a fixed hard noise rate. Explain why the copy advantage survives while computational accessibility changes. Retain the vanishing-noise positive regime, the excluded half-noise endpoint, the average-case prior, ideal processing, and the lack of extra preparation access.

**Dependencies and story role.** Integrates [M14](#m14), [M19](#m19)–[M21](#m21), [M24](#m24), [M27](#m27), and [M29](#m29). This closes the narrative phase by comparing all resources under the same success criterion and data interface.

**Conceptual connection.** Easy preparation, unentangled specimens, a simple optimal measurement, and statistical learnability do not jointly guarantee efficient training. The local-prior variant illustrates how changing a prior can simplify a reduction while changing the quantitative memory bound; it is a separate comparison rather than a replacement for the main theorem.

**Source pointers.** [Model: canonical statements and resource table](../science/model.md); [Interpretation](../science/interpretation.md); [Local-prior variant](../science/local_prior.md); [Related work](../references/RELATED_WORK.md).
