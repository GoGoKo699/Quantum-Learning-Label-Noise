#!/usr/bin/env python3
"""Independent finite-dimensional checks for statistical Theorems S1 and S2.

Run with Python 3.12 and numpy==2.3.5. The repository dependency file is the
installation authority; the versions actually used are recorded in the JSON.

Inputs are built from spectral Pauli eigenspaces and a classical annotation-flip
channel. We then compare actual matrices and Born probabilities with the stated
closed expressions. These checks do not replace the analytic universal proofs.
No dense matrix in this suite has dimension greater than 256.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import product
import json
import math
import platform
import sys
from typing import Any

import numpy as np


NUMPY_PIN = "2.3.5"
SEED = 20261022
MATRIX_ATOL = 1e-10
SCALAR_RTOL = 1e-8
FIDELITY_ATOL = 2e-10
SPECTRAL_CUTOFF = 1e-12

I2 = np.eye(2, dtype=np.complex128)
X2 = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y2 = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z2 = np.diag([1, -1]).astype(np.complex128)
H2 = np.array([[1, 1], [1, -1]], dtype=np.complex128) / math.sqrt(2)
LOCAL_PAULIS = {"I": I2, "X": X2, "Y": Y2, "Z": Z2}


def kron_all(matrices: list[np.ndarray]) -> np.ndarray:
    result = np.ones((1, 1), dtype=np.complex128)
    for matrix in matrices:
        result = np.kron(result, matrix)
    return result


def tensor_power(matrix: np.ndarray, exponent: int) -> np.ndarray:
    return kron_all([matrix] * exponent)


def max_abs(matrix: np.ndarray) -> float:
    return float(np.max(np.abs(matrix), initial=0.0))


def near(actual: float, expected: float, atol: float = MATRIX_ATOL) -> bool:
    return bool(abs(actual - expected) <= atol + SCALAR_RTOL * abs(expected))


@dataclass(frozen=True)
class PauliFamily:
    n: int
    d: int
    names: tuple[str, ...]
    unsigned: np.ndarray
    signed: np.ndarray
    clean_classes: np.ndarray

    @property
    def M(self) -> int:
        return len(self.signed)

    @property
    def D(self) -> int:
        return 2 * self.d


@lru_cache(maxsize=None)
def family(n: int) -> PauliFamily:
    """Generate Pauli matrices; derive class states from spectral projectors."""
    words = [
        "".join(word)
        for word in product("IXYZ", repeat=n)
        if any(letter != "I" for letter in word)
    ]
    unsigned = np.stack(
        [kron_all([LOCAL_PAULIS[letter] for letter in word]) for word in words]
    )
    signed = np.stack([sign * pauli for pauli in unsigned for sign in (1, -1)])
    names = tuple(sign + word for word in words for sign in ("+", "-"))
    d = 2**n
    classes = np.zeros((len(signed), 2, d, d), dtype=np.complex128)
    for j, pauli in enumerate(signed):
        values, vectors = np.linalg.eigh(pauli)
        for label_index, positive in enumerate((True, False)):
            selected = values > 0.5 if positive else values < -0.5
            basis = vectors[:, selected]
            if basis.shape[1] != d // 2:
                raise ValueError("A nonidentity Pauli must have balanced eigenspaces")
            classes[j, label_index] = basis @ basis.conj().T / basis.shape[1]
    return PauliFamily(n, d, names, unsigned, signed, classes)


def conditional_features(fam: PauliFamily, gamma: float) -> np.ndarray:
    """Observed-label feature states, from actual flips of balanced clean labels."""
    eta = (1.0 - gamma) / 2.0
    return (
        (1.0 - eta) * fam.clean_classes
        + eta * fam.clean_classes[:, ::-1, :, :]
    )


def annotated_examples(fam: PauliFamily, gamma: float) -> np.ndarray:
    conditional = conditional_features(fam, gamma)
    result = np.zeros((fam.M, fam.D, fam.D), dtype=np.complex128)
    result[:, : fam.d, : fam.d] = 0.5 * conditional[:, 0]
    result[:, fam.d :, fam.d :] = 0.5 * conditional[:, 1]
    return result


def psd_sqrt(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2)
    if float(np.min(values)) < -MATRIX_ATOL:
        raise ValueError("Nonpositive matrix in a PSD square root")
    values = np.where(values > SPECTRAL_CUTOFF, values, 0.0)
    return (vectors * np.sqrt(values)) @ vectors.conj().T


def root_fidelity_from_sqrts(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.sum(np.linalg.svd(left @ right, compute_uv=False)))


def check_helstrom_moments() -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    for n, exponents in ((1, (0, 1, 2, 3)), (2, (0, 1, 2)), (3, (1,))):
        fam = family(n)
        for gamma in (0.0, 0.23, 0.71, 1.0):
            inputs = annotated_examples(fam, gamma)
            for T in exponents:
                dimension = fam.d * fam.D**T
                omega_plus = np.zeros((dimension, dimension), dtype=np.complex128)
                omega_minus = np.zeros_like(omega_plus)
                for j in range(fam.M):
                    training = tensor_power(inputs[j], T)
                    omega_plus += np.kron(training, fam.clean_classes[j, 0]) / fam.M
                    omega_minus += np.kron(training, fam.clean_classes[j, 1]) / fam.M
                difference_half = (omega_plus - omega_minus) / 2.0
                actual_second_moment = float(
                    np.vdot(difference_half, difference_half).real
                )
                numerator = (
                    (1.0 + gamma**2) ** T - (1.0 - gamma**2) ** T
                    if T > 0
                    else 0.0
                )
                expected_second_moment = numerator / (
                    fam.d * fam.M * fam.D**T
                )
                eigenvalues = np.linalg.eigvalsh(difference_half)
                actual_advantage = float(np.sum(np.abs(eigenvalues)) / 2.0)
                claimed_upper = min(
                    0.5, 0.5 * math.sqrt(max(0.0, numerator / fam.M))
                )
                trace_residual = max(
                    abs(float(np.trace(omega_plus).real) - 1.0),
                    abs(float(np.trace(omega_minus).real) - 1.0),
                )
                hermiticity_residual = max_abs(
                    difference_half - difference_half.conj().T
                )
                residual = abs(actual_second_moment - expected_second_moment)
                # An independent one-example trace-norm check: sum_Q Q⊗Q=d SWAP-I.
                one_example_residual = (
                    abs(actual_advantage - gamma / (2.0 * fam.d))
                    if T == 1
                    else None
                )
                passed = (
                    near(actual_second_moment, expected_second_moment)
                    and actual_advantage <= claimed_upper + MATRIX_ATOL
                    and trace_residual <= MATRIX_ATOL
                    and hermiticity_residual <= MATRIX_ATOL
                    and (
                        one_example_residual is None
                        or one_example_residual <= MATRIX_ATOL
                    )
                )
                cases.append(
                    {
                        "n": n,
                        "T": T,
                        "gamma": gamma,
                        "matrix_dimension": dimension,
                        "second_moment_from_matrices": actual_second_moment,
                        "second_moment_formula": expected_second_moment,
                        "absolute_residual": residual,
                        "helstrom_advantage_from_eigenvalues": actual_advantage,
                        "theorem_upper_bound": claimed_upper,
                        "one_example_advantage_residual": one_example_residual,
                        "state_trace_residual": trace_residual,
                        "hermiticity_residual": hermiticity_residual,
                        "passed": passed,
                    }
                )
    return {
        "passed": all(case["passed"] for case in cases),
        "case_count": len(cases),
        "cases": cases,
    }


@lru_cache(maxsize=None)
def fidelity_data(n: int, gamma: float) -> tuple[np.ndarray, dict[str, Any]]:
    fam = family(n)
    states = annotated_examples(fam, gamma)
    square_roots = [psd_sqrt(state) for state in states]
    values = np.eye(fam.M)
    counts = {"opposite": 0, "commuting_distinct": 0, "anticommuting": 0}
    residuals = {key: 0.0 for key in counts}
    diagonal_residual = 0.0
    for i in range(fam.M):
        diagonal_residual = max(
            diagonal_residual,
            abs(root_fidelity_from_sqrts(square_roots[i], square_roots[i]) - 1.0),
        )
        P = fam.signed[i]
        for j in range(i + 1, fam.M):
            Q = fam.signed[j]
            actual = root_fidelity_from_sqrts(square_roots[i], square_roots[j])
            values[i, j] = values[j, i] = actual
            if max_abs(P + Q) < MATRIX_ATOL:
                relation = "opposite"
                expected = math.sqrt(max(0.0, 1.0 - gamma**2))
            elif max_abs(P @ Q - Q @ P) < MATRIX_ATOL:
                relation = "commuting_distinct"
                expected = (1.0 + math.sqrt(max(0.0, 1.0 - gamma**2))) / 2.0
            else:
                if max_abs(P @ Q + Q @ P) > MATRIX_ATOL:
                    raise ValueError("Pauli pair is neither commuting nor anticommuting")
                relation = "anticommuting"
                expected = math.sqrt(1.0 - gamma**2 / 2.0)
            counts[relation] += 1
            residuals[relation] = max(residuals[relation], abs(actual - expected))
    summary = {
        "n": n,
        "gamma": gamma,
        "matrix_dimension": fam.D,
        "unordered_pair_counts": counts,
        "maximum_formula_residual_by_relation": residuals,
        "same_state_fidelity_residual": diagonal_residual,
        "passed": (
            max(residuals.values()) <= FIDELITY_ATOL
            and diagonal_residual <= FIDELITY_ATOL
        ),
    }
    return values, summary


def check_fidelities() -> dict[str, Any]:
    cases = [
        fidelity_data(n, gamma)[1]
        for n in (1, 2)
        for gamma in (0.0, 0.23, 0.71, 1.0)
    ]
    return {
        "passed": all(case["passed"] for case in cases),
        "case_count": len(cases),
        "cases": cases,
    }


def matrix_pgm(states: np.ndarray) -> dict[str, Any]:
    """Construct the PGM by spectral inversion, with uniform hypothesis weights."""
    M = len(states)
    subnormalized = states / M
    average = np.sum(subnormalized, axis=0)
    values, vectors = np.linalg.eigh((average + average.conj().T) / 2.0)
    if float(np.min(values)) < -MATRIX_ATOL:
        raise ValueError("Negative ensemble average")
    support = values > SPECTRAL_CUTOFF
    support_vectors = vectors[:, support]
    inverse_sqrt = (
        support_vectors / np.sqrt(values[support])
    ) @ support_vectors.conj().T
    support_projector = support_vectors @ support_vectors.conj().T
    effects = inverse_sqrt[None, :, :] @ subnormalized @ inverse_sqrt[None, :, :]
    successes = np.einsum("pij,pji->p", effects, states).real
    completeness_residual = max_abs(np.sum(effects, axis=0) - support_projector)
    support_residual = max_abs(
        support_projector[None, :, :] @ states @ support_projector[None, :, :]
        - states
    )
    minimum_effect_eigenvalue = float(np.min(np.linalg.eigvalsh(effects)))
    return {
        "effects": effects,
        "successes": successes,
        "completeness_residual": completeness_residual,
        "support_residual": support_residual,
        "minimum_effect_eigenvalue": minimum_effect_eigenvalue,
    }


def label_block_pgm(
    fam: PauliFamily, gamma: float, T: int, enumerate_all: bool = False
) -> dict[str, Any]:
    conditional = conditional_features(fam, gamma)
    successes = np.zeros(fam.M)
    completeness_residual = 0.0
    support_residual = 0.0
    minimum_effect_eigenvalue = 0.0
    if enumerate_all:
        weighted_patterns = [
            (tuple(pattern), 1.0 / 2**T)
            for pattern in product((0, 1), repeat=T)
        ]
    else:
        # Permuting examples unitarily conjugates every hypothesis and its PGM.
        # This sums all annotation strings using their Hamming-weight multiplicity.
        weighted_patterns = [
            ((0,) * (T - r) + (1,) * r, math.comb(T, r) / 2**T)
            for r in range(T + 1)
        ]
    for pattern, weight in weighted_patterns:
        states = np.stack(
            [
                kron_all([conditional[j, c] for c in pattern])
                for j in range(fam.M)
            ]
        )
        result = matrix_pgm(states)
        successes += weight * result["successes"]
        completeness_residual = max(
            completeness_residual, result["completeness_residual"]
        )
        support_residual = max(support_residual, result["support_residual"])
        minimum_effect_eigenvalue = min(
            minimum_effect_eigenvalue, result["minimum_effect_eigenvalue"]
        )
    return {
        "successes": successes,
        "block_count_evaluated": len(weighted_patterns),
        "completeness_residual": completeness_residual,
        "support_residual": support_residual,
        "minimum_effect_eigenvalue": minimum_effect_eigenvalue,
    }


def check_pgms() -> dict[str, Any]:
    cases = []
    configurations = (
        (1, 2, 0.23, True),
        (1, 3, 0.71, True),
        (1, 6, 0.95, False),
        (1, 6, 1.0, False),
        (2, 2, 0.71, True),
    )
    for n, T, gamma, check_full_cq in configurations:
        fam = family(n)
        result = label_block_pgm(fam, gamma, T)
        error = 1.0 - float(np.mean(result["successes"]))
        root_fidelities, _ = fidelity_data(n, gamma)
        mask = ~np.eye(fam.M, dtype=bool)
        pairwise_bound = float(np.sum(root_fidelities[mask] ** T) / fam.M)
        max_fidelity_bound = (fam.M - 1) * (1.0 - gamma**2 / 2.0) ** (T / 2.0)
        exponential_bound = (fam.M - 1) * math.exp(-T * gamma**2 / 4.0)
        target_success_spread = float(np.ptp(result["successes"]))
        full_cq_residual = None
        off_annotation_block_residual = None
        annotation_permutation_residual = None
        if check_full_cq:
            inputs = annotated_examples(fam, gamma)
            full_states = np.stack([tensor_power(state, T) for state in inputs])
            full = matrix_pgm(full_states)
            full_cq_residual = float(
                np.max(np.abs(full["successes"] - result["successes"]))
            )
            indices = np.arange(fam.D**T)
            coordinates = np.unravel_index(indices, (fam.D,) * T)
            label_ids = np.zeros_like(indices)
            for coordinate in coordinates:
                label_ids = 2 * label_ids + coordinate // fam.d
            label_mask = label_ids[:, None] == label_ids[None, :]
            off_annotation_block_residual = max_abs(
                full["effects"] * (~label_mask)[None, :, :]
            )
            all_patterns = label_block_pgm(fam, gamma, T, enumerate_all=True)
            annotation_permutation_residual = float(
                np.max(np.abs(all_patterns["successes"] - result["successes"]))
            )
        passed = (
            error >= -MATRIX_ATOL
            and error <= min(1.0, pairwise_bound) + MATRIX_ATOL
            and pairwise_bound <= max_fidelity_bound + MATRIX_ATOL
            and max_fidelity_bound <= exponential_bound + MATRIX_ATOL
            and result["completeness_residual"] <= MATRIX_ATOL
            and result["support_residual"] <= MATRIX_ATOL
            and result["minimum_effect_eigenvalue"] >= -MATRIX_ATOL
            and target_success_spread <= MATRIX_ATOL
            and (full_cq_residual is None or full_cq_residual <= MATRIX_ATOL)
            and (
                off_annotation_block_residual is None
                or off_annotation_block_residual <= MATRIX_ATOL
            )
            and (
                annotation_permutation_residual is None
                or annotation_permutation_residual <= MATRIX_ATOL
            )
        )
        cases.append(
            {
                "n": n,
                "T": T,
                "gamma": gamma,
                "feature_block_dimension": fam.d**T,
                "annotation_blocks_evaluated": result["block_count_evaluated"],
                "annotation_blocks_represented": 2**T,
                "error_from_matrix_pgm": error,
                "pairwise_root_fidelity_bound": pairwise_bound,
                "maximum_fidelity_bound": max_fidelity_bound,
                "exponential_bound": exponential_bound,
                "pairwise_bound_is_nontrivial": pairwise_bound < 1.0,
                "completeness_residual": result["completeness_residual"],
                "hypothesis_support_residual": result["support_residual"],
                "minimum_effect_eigenvalue": result["minimum_effect_eigenvalue"],
                "target_success_spread": target_success_spread,
                "full_cq_vs_conditioned_residual": full_cq_residual,
                "off_annotation_block_residual": off_annotation_block_residual,
                "annotation_permutation_residual": annotation_permutation_residual,
                "passed": passed,
            }
        )
    return {
        "passed": all(case["passed"] for case in cases),
        "case_count": len(cases),
        "cases": cases,
    }


def normalized_complex_vector(rng: np.random.Generator, dimension: int) -> np.ndarray:
    vector = rng.normal(size=dimension) + 1j * rng.normal(size=dimension)
    return vector / np.linalg.norm(vector)


def check_pauli_moments() -> dict[str, Any]:
    cases = []
    for n in (1, 2, 3, 4):
        fam = family(n)
        rng = np.random.default_rng(np.random.SeedSequence([SEED, 200, n]))
        observables = np.stack([np.kron(Z2, Q) for Q in fam.unsigned])
        product_vectors = [
            np.kron(np.array([1.0, 0.0]), normalized_complex_vector(rng, fam.d))
            for _ in range(4)
        ]
        entangled = np.zeros(fam.D, dtype=np.complex128)
        entangled[0] = entangled[fam.d + 1] = 1.0 / math.sqrt(2.0)
        vectors = product_vectors + [entangled] + [
            normalized_complex_vector(rng, fam.D) for _ in range(16)
        ]
        moments = []
        parseval_residual = 0.0
        imaginary_residual = 0.0
        saturation_residual = 0.0
        for index, phi in enumerate(vectors):
            coefficients = np.einsum("i,qij,j->q", phi.conj(), observables, phi)
            imaginary_residual = max(
                imaginary_residual, float(np.max(np.abs(coefficients.imag)))
            )
            sum_from_paulis = float(np.sum(coefficients.real**2))
            moment = sum_from_paulis / (fam.d**2 - 1)
            moments.append(moment)
            u, v = phi[: fam.d], phi[fam.d :]
            B = np.outer(u, u.conj()) - np.outer(v, v.conj())
            parseval = float(
                (fam.d * np.trace(B @ B) - np.trace(B) ** 2).real
            )
            parseval_residual = max(
                parseval_residual, abs(sum_from_paulis - parseval)
            )
            if index < len(product_vectors):
                saturation_residual = max(
                    saturation_residual, abs(moment - 1.0 / (fam.d + 1))
                )
        bound = 1.0 / (fam.d + 1)
        passed = (
            max(moments) <= bound + MATRIX_ATOL
            and saturation_residual <= MATRIX_ATOL
            and parseval_residual <= MATRIX_ATOL
            and imaginary_residual <= MATRIX_ATOL
        )
        cases.append(
            {
                "n": n,
                "vector_count": len(vectors),
                "product_saturators": len(product_vectors),
                "entangled_label_feature_vectors": len(vectors) - len(product_vectors),
                "minimum_observed_moment": min(moments),
                "maximum_observed_moment": max(moments),
                "delta_star": bound,
                "saturation_residual": saturation_residual,
                "parseval_identity_residual": parseval_residual,
                "imaginary_coefficient_residual": imaginary_residual,
                "passed": passed,
            }
        )
    return {
        "passed": all(case["passed"] for case in cases),
        "case_count": len(cases),
        "cases": cases,
    }


def adaptive_basis(fam: PauliFamily, history: tuple[int, ...]) -> np.ndarray:
    if not history:
        return np.eye(fam.D, dtype=np.complex128)
    selector = (
        len(history) + sum((j + 1) * (outcome + 1) for j, outcome in enumerate(history))
    ) % 3
    if selector == 0:
        return np.eye(fam.D, dtype=np.complex128)
    if selector == 1:
        return np.kron(I2, tensor_power(H2, fam.n))
    rng = np.random.default_rng(
        np.random.SeedSequence([SEED, 300, fam.n, len(history), *history])
    )
    matrix = rng.normal(size=(fam.D, fam.D)) + 1j * rng.normal(
        size=(fam.D, fam.D)
    )
    unitary, triangular = np.linalg.qr(matrix)
    phases = np.diag(triangular)
    phases = phases / np.abs(phases)
    return unitary * phases.conj()


def actual_adaptive_tree(n: int, contrasts: tuple[float, ...]) -> dict[str, Any]:
    """Enumerate Born probabilities of an adaptive rank-one projective protocol."""
    fam = family(n)
    states = [annotated_examples(fam, gamma) for gamma in contrasts]
    leaves_p: list[float] = []
    leaves_q: list[float] = []
    statistics: dict[str, Any] = {
        "internal_nodes": 0,
        "minimum_raw_born_probability": 1.0,
        "zero_born_probabilities": 0,
        "row_normalization_residual": 0.0,
        "basis_unitarity_residual": 0.0,
    }

    def visit(
        history: tuple[int, ...], hidden_probabilities: np.ndarray, null_probability: float
    ) -> None:
        depth = len(history)
        if depth == len(contrasts):
            leaves_p.append(float(np.mean(hidden_probabilities)))
            leaves_q.append(null_probability)
            return
        unitary = adaptive_basis(fam, history)
        statistics["internal_nodes"] += 1
        statistics["basis_unitarity_residual"] = max(
            statistics["basis_unitarity_residual"],
            max_abs(unitary.conj().T @ unitary - np.eye(fam.D)),
        )
        born = np.einsum(
            "ki,pkl,li->pi", unitary.conj(), states[depth], unitary, optimize=True
        ).real
        statistics["minimum_raw_born_probability"] = min(
            statistics["minimum_raw_born_probability"], float(np.min(born))
        )
        statistics["zero_born_probabilities"] += int(
            np.count_nonzero(np.abs(born) < SPECTRAL_CUTOFF)
        )
        statistics["row_normalization_residual"] = max(
            statistics["row_normalization_residual"],
            float(np.max(np.abs(np.sum(born, axis=1) - 1.0))),
        )
        # Remove only roundoff-scale negative probabilities of exact PSD states.
        born = np.maximum(born, 0.0)
        for outcome in range(fam.D):
            visit(
                history + (outcome,),
                hidden_probabilities * born[:, outcome],
                null_probability / fam.D,
            )

    visit((), np.ones(fam.M), 1.0)
    p = np.asarray(leaves_p)
    q = np.asarray(leaves_q)
    total_variation = float(np.sum(np.abs(p - q)) / 2.0)
    likelihood_minimum = float(np.min(p / q))
    x = sum(gamma**2 for gamma in contrasts) / (fam.d + 1)
    tv_bound = min(1.0, 5.0 * x)
    pointwise_floor = max(0.0, 1.0 - 5.0 * x)
    normalization_residual = max(
        abs(float(np.sum(p)) - 1.0), abs(float(np.sum(q)) - 1.0)
    )
    endpoint_exercised = (
        statistics["zero_born_probabilities"] > 0 if 1.0 in contrasts else None
    )
    passed = (
        total_variation <= tv_bound + MATRIX_ATOL
        and likelihood_minimum >= pointwise_floor - MATRIX_ATOL
        and normalization_residual <= MATRIX_ATOL
        and statistics["row_normalization_residual"] <= MATRIX_ATOL
        and statistics["basis_unitarity_residual"] <= MATRIX_ATOL
        and statistics["minimum_raw_born_probability"] >= -MATRIX_ATOL
        and (endpoint_exercised is None or endpoint_exercised)
    )
    return {
        "n": n,
        "contrasts": list(contrasts),
        "leaves": len(p),
        "x": x,
        "total_variation_from_born_probabilities": total_variation,
        "theorem_tv_bound": tv_bound,
        "minimum_averaged_likelihood": likelihood_minimum,
        "theorem_pointwise_floor": pointwise_floor,
        "distribution_normalization_residual": normalization_residual,
        "noiseless_zero_probability_endpoint_exercised": endpoint_exercised,
        **statistics,
        "passed": passed,
    }


def check_clipping() -> dict[str, Any]:
    u = np.linspace(0.0, 0.25, 10001)
    log_margin = np.log1p(-u) + 2.0 * u
    x_grid = np.linspace(0.0, 0.1999, 501)
    minimum_exp_margin = math.inf
    minimum_combined_margin = math.inf
    for x in x_grid:
        for g in np.linspace(1.0 - 4.0 * x, 1.0, 31):
            ratio = x / g
            minimum_exp_margin = min(
                minimum_exp_margin, math.exp(-ratio) - (1.0 - ratio)
            )
            minimum_combined_margin = min(
                minimum_combined_margin,
                g * math.exp(-ratio) - (1.0 - 5.0 * x),
            )
    elementary = {
        "log_domain": [0.0, 0.25],
        "log_grid_points": len(u),
        "minimum_log_inequality_margin": float(np.min(log_margin)),
        "x_domain": [0.0, 0.1999],
        "x_grid_points": len(x_grid),
        "g_grid_points_per_x": 31,
        "g_domain": "1 - 4*x <= g <= 1",
        "minimum_exponential_inequality_margin": float(minimum_exp_margin),
        "minimum_combined_inequality_margin": float(minimum_combined_margin),
        "passed": bool(
            float(np.min(log_margin)) >= -MATRIX_ATOL
            and minimum_exp_margin >= -MATRIX_ATOL
            and minimum_combined_margin >= -MATRIX_ATOL
        ),
    }
    trees = [
        actual_adaptive_tree(1, (0.12, 0.18, 0.22)),
        actual_adaptive_tree(2, (0.10, 0.20, 0.30)),
        actual_adaptive_tree(3, (0.35, 1.0)),
        actual_adaptive_tree(3, (0.20, 0.30, 1.0)),
    ]
    return {
        "passed": elementary["passed"] and all(case["passed"] for case in trees),
        "elementary_inequalities": elementary,
        "adaptive_born_probability_trees": trees,
    }


def run_checks() -> dict[str, Any]:
    checks = {
        "helstrom_moments": check_helstrom_moments(),
        "root_fidelities": check_fidelities(),
        "pretty_good_measurements": check_pgms(),
        "individual_pauli_moments": check_pauli_moments(),
        "heterogeneous_clipping": check_clipping(),
    }
    return {
        "schema_version": 1,
        "suite": "statistics",
        "passed": all(check["passed"] for check in checks.values()),
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "numpy_pin": NUMPY_PIN,
        },
        "fixed_seed": SEED,
        "tolerances": {
            "matrix_absolute": MATRIX_ATOL,
            "scalar_relative": SCALAR_RTOL,
            "fidelity_absolute": FIDELITY_ATOL,
            "spectral_zero_cutoff": SPECTRAL_CUTOFF,
        },
        "resource_limits": {
            "largest_dense_matrix_dimension": 256,
            "largest_adaptive_tree_leaves": 4096,
        },
        "checks": checks,
    }


if __name__ == "__main__":
    try:
        report = run_checks()
    except Exception as error:
        report = {
            "schema_version": 1,
            "suite": "statistics",
            "passed": False,
            "error_type": type(error).__name__,
            "error": str(error),
        }
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))
    sys.exit(0 if report["passed"] else 1)
