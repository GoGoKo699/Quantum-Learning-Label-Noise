# Reproducing the finite checks

The scientific results are proved analytically in [science/](../science/model.md). This directory supplies deterministic, small-dimensional checks of the identities and conventions that enter those proofs. The numerical routines construct the quantum objects explicitly rather than merely substituting numbers into the claimed bounds.

## Run

From the repository root:

```bash
python -m pip install -r verification/requirements.txt
python verification/run_all.py
```

The tested environment is Python 3.12.14 and NumPy 2.3.5. NumPy is the only third-party dependency and is pinned in [requirements.txt](requirements.txt). The runner prints a complete JSON report and returns a nonzero exit status if a check fails. Each of the three modules can also be run directly.

To save a fresh report:

```bash
python verification/run_all.py --output verification/verified_results.json
```

[verified_results.json](verified_results.json) records an actual passing run in the stated environment. No network access, quantum hardware, or source datasets are needed. The scripts do not modify the scientific chapters or contact external services.

## What is checked

| Suite | Independently constructed objects | Compared quantities |
|---|---|---|
| [Source, Bell, and reduction](verify_source_bell.py) | Product eigenvectors; Bell basis vectors and their readout circuits; Clifford-transformed basis vectors from enumerated classical LPN samples | Exact source density matrices, annotation mixtures, Bell probabilities and joint affine-LPN law, null simulation, and the held-out noise identity |
| [Collective and individual statistics](verify_statistics.py) | Small training-and-test matrices; full labeled and conditional PGM effects; arbitrary pure vectors; adaptive measurement trees | Helstrom second moment, three pairwise root fidelities, PGM validity and error bound, label conditioning, Pauli moment, and heterogeneous transcript inequalities |
| [Repository integrity](verify_repository.py) | Local documentation, heading maps, and the learning route | Local links and fragments; unique anchors; closed math and code delimiters; table-safe mathematical notation; exactly M01–M30 with the 14+16 phase split, required fields, and earlier-only dependencies; selected-anchor navigation |

### Source, Bell, and reduction coverage

The source check enumerates every signed nonidentity target through three qubits and both clean labels. This gives 324 product-state mixtures, with four annotation-noise rates giving another 1,296 conditional-mixture checks. Identity factors, global signs, and both odd and even numbers of $`Y`$ factors occur.

Bell checks evaluate the Born rule using explicitly constructed basis vectors. They cover every target at one and two qubits and eight structured targets at three qubits, with both target signs, all label pairs, and four contrasts including zero and one. The circuit check verifies the order of the two measured bit strings. The joint transcript calculation independently sums over clean labels and flip bits to recover the affine-LPN law.

The LPN check enumerates samples at parity dimensions one through three. It prepares the actual vectors from those samples and several Clifford circuits, averages them, and compares both the LPN and uniform experiments with their claimed density operators. It also evaluates prediction agreement for general bounded Hermitian test observables.

The supplementary [local-prior variant](../science/local_prior.md) is checked at parity dimensions one and two: the prior collision probability, doubled-space moment, its saturating product vector, and the weighted Helstrom second moment. These are different priors from the main theorem, and the code keeps them separate.

### Statistical coverage

The statistical suite includes 32 Helstrom moment cases, eight complete pairwise fidelity ensembles, five PGM cases, 84 vectors for the Pauli moment, and four adaptive trees with 4,928 leaves in total. Its largest dense matrix has dimension 256. PGM checks include support-restricted inverses, positivity, completeness, equal target success, and agreement between a full classical–quantum construction and measurements conditioned on observed annotation strings. Two of the PGM cases have nontrivial error bounds below one.

The adaptive trees compute every leaf probability by the Born rule, average over the same fixed target throughout each path, and compare with a maximally mixed null. Some paths include a clean final specimen. The noiseless cases exercise exact zero probabilities, which are why the proof's clipping argument is useful. Separate finite grids check the elementary inequalities used in clipping; the analytic inequalities are proved in the chapter.

## Tolerances and reproducibility

Each report includes the fixed random seeds, every case's parameters, and the relevant absolute or relative tolerances. The source/Bell suite uses absolute tolerance $`2\times10^{-10}`$. The statistical suite reports its matrix, scalar, fidelity, and support-cutoff tolerances separately; support inversion and square roots can amplify roundoff near zero eigenvalues.

Reproducibility means that the cases and pass criteria are fixed. Floating-point residuals can vary slightly with the numerical library or platform, so exact byte equality of reports is not required. All tolerance comparisons occur before the report is written.

## Limits

Finite checks cannot prove the asymptotic statements, universal measurement bounds, or hardness assumption. They do not search for efficient general decoders, claim a quantum speedup on the computer running these scripts, or certify the contribution's novelty. The analytic proofs and cited research dependencies remain authoritative.

The documentation checker validates local destinations and the repository's heading slugs. It also rejects observed rendering hazards: literal vertical bars inside table-cell mathematics, the unsupported `\operatorname` macro, and numbered equations without an `aligned` group. Roman mathematical names use `\mathrm`, while table-cell kets and absolute values use `\lvert` and `\rvert`. Grouping numbered formulas prevents GitHub from stacking their individual terms vertically. These checks do not verify external URLs or substitute for inspecting GitHub's rendered equations and pages. The recorded report is scientific reproducibility material, rather than a development log.
