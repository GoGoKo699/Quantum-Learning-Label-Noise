"""Independent finite-size checks of the source, Bell law, and LPN simulation.

The inputs below are explicit vectors/matrices. These checks diagnose convention
and normalization errors; the general statements are proved in science/.
"""

from __future__ import annotations

from itertools import product
import json

import numpy as np


TOL = 2e-10
SEED = 20261022
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S = np.diag([1, 1j]).astype(complex)
PAULI = (I, X, Y, Z)


def tensor(items):
    result = np.array([1.0 + 0j])
    for item in items:
        result = np.kron(result, item)
    return result


def bits(x, n):
    return tuple((x >> (n - 1 - j)) & 1 for j in range(n))


def index(bs):
    value = 0
    for b in bs:
        value = 2 * value + int(b)
    return value


def paulis(n):
    return [(w, tensor([PAULI[j] for j in w]))
            for w in product(range(4), repeat=n)]


def coordinates(word):
    return (tuple(int(j in (1, 2)) for j in word),
            tuple(int(j in (2, 3)) for j in word))


def bell_character(word, outcome_word):
    a, b = coordinates(word)
    az, bz = coordinates(outcome_word)
    exponent = sum(j == 2 for j in word)
    exponent += sum(x * y for x, y in zip(a, bz))
    exponent += sum(x * y for x, y in zip(b, az))
    return (-1) ** exponent


def eigenvector(axis, bit):
    if axis in (0, 3):
        return np.eye(2, dtype=complex)[:, bit]
    if axis == 1:
        return np.array([1, (-1) ** bit], dtype=complex) / np.sqrt(2)
    return np.array([1, 1j * (-1) ** bit], dtype=complex) / np.sqrt(2)


def product_source(word, sign, label):
    n = len(word)
    pivot = next(j for j, axis in enumerate(word) if axis)
    free = [j for j in range(n) if j != pivot]
    result = np.zeros((2**n, 2**n), dtype=complex)
    for assignment in product((0, 1), repeat=n - 1):
        bs = [0] * n
        for j, value in zip(free, assignment):
            bs[j] = value
        parity = sum(bs[j] for j in free if word[j]) & 1
        bs[pivot] = int(label == -1) ^ int(sign == -1) ^ parity
        vec = tensor([eigenvector(axis, bit) for axis, bit in zip(word, bs)])
        result += np.outer(vec, vec.conj()) / 2 ** (n - 1)
    return result


def cnot(n, control, target):
    unitary = np.zeros((2**n, 2**n), dtype=complex)
    for x in range(2**n):
        bs = list(bits(x, n))
        bs[target] ^= bs[control]
        unitary[index(bs), x] = 1
    return unitary


def check(residual, label):
    residual = float(residual)
    if not np.isfinite(residual) or residual > TOL:
        raise AssertionError(f"{label}: residual {residual:.3e} > {TOL}")
    return residual


def run_checks() -> dict:
    rng = np.random.default_rng(SEED)
    errors = {name: 0.0 for name in (
        "product_source", "annotation_mixture", "bell_orthonormality",
        "bell_born_law", "bell_lpn_joint", "bell_readout",
        "lpn_source", "lpn_null", "prediction_noise_identity",
        "local_collision", "local_moment", "local_second_moment")}
    counts = {name: 0 for name in errors}

    def record(name, residual):
        errors[name] = max(errors[name], check(residual, name))
        counts[name] += 1

    # Enumerate every signed nonidentity target through three qubits.
    for n in (1, 2, 3):
        d = 2**n
        for word, unsigned in paulis(n)[1:]:
            for sign in (-1, 1):
                target = sign * unsigned
                clean = {}
                for label in (-1, 1):
                    clean[label] = product_source(word, sign, label)
                    expected = (np.eye(d) + label * target) / d
                    record("product_source", np.max(np.abs(clean[label] - expected)))
                for eta in (0.0, 0.125, 0.3, 0.5):
                    for observed in (-1, 1):
                        mixed = ((1 - eta) * clean[observed]
                                 + eta * clean[-observed])
                        expected = (np.eye(d) + observed * (1 - 2 * eta) * target) / d
                        record("annotation_mixture", np.max(np.abs(mixed - expected)))

    # Construct Bell vectors explicitly; evaluate Born probabilities from them.
    # All targets at n=1,2; eight structured targets at n=3 include odd/even Y.
    for n in (1, 2, 3):
        d = 2**n
        family = paulis(n)
        phi = np.eye(d, dtype=complex).reshape(-1) / np.sqrt(d)
        basis = np.column_stack([np.kron(np.eye(d), op) @ phi for _, op in family])
        record("bell_orthonormality",
               np.max(np.abs(basis.conj().T @ basis - np.eye(d * d))))
        readout = np.eye(d * d, dtype=complex)
        for j in range(n):
            readout = cnot(2 * n, j, n + j) @ readout
        readout = np.kron(tensor([H] * n), np.eye(d)) @ readout
        for column, (word, _) in enumerate(family):
            az, bz = coordinates(word)
            probs = np.abs(readout @ basis[:, column]) ** 2
            expected = np.zeros(d * d)
            expected[index(bz + az)] = 1
            record("bell_readout", np.max(np.abs(probs - expected)))

        targets = family[1:] if n < 3 else [family[j] for j in (1, 2, 6, 10, 21, 27, 42, 63)]
        for word, unsigned in targets:
            character = np.array([bell_character(word, zword) for zword, _ in family])
            for sign in (-1, 1):
                target = sign * unsigned
                clean_born = {}
                for c1, c2 in product((-1, 1), repeat=2):
                    for gamma in (0.0, 0.25, 0.8, 1.0):
                        rho1 = (np.eye(d) + c1 * gamma * target) / d
                        rho2 = (np.eye(d) + c2 * gamma * target) / d
                        joint = np.kron(rho1, rho2)
                        born = np.einsum("ik,ij,jk->k", basis.conj(), joint,
                                         basis, optimize=True).real
                        predicted = (1 + c1 * c2 * gamma**2 * character) / d**2
                        record("bell_born_law", np.max(np.abs(born - predicted)))
                        if gamma == 1.0:
                            clean_born[c1, c2] = born
                for eta in (0.0, 0.1, 0.375, 0.5):
                    joint_rz = np.zeros((2, d * d))
                    for y1, y2, e1, e2 in product((-1, 1), repeat=4):
                        weight = 0.25 * (eta if e1 == -1 else 1 - eta)
                        weight *= eta if e2 == -1 else 1 - eta
                        r = y1 * y2 * e1 * e2
                        joint_rz[int(r == 1)] += weight * clean_born[y1, y2]
                    expected = np.vstack([
                        (1 - (1 - 2 * eta)**2 * character) / (2 * d**2),
                        (1 + (1 - 2 * eta)**2 * character) / (2 * d**2)])
                    record("bell_lpn_joint", np.max(np.abs(joint_rz - expected)))

    # Enumerate classical LPN samples, prepare actual Clifford-transformed basis
    # vectors, and average. The simulator never receives the unknown secret.
    for k in (1, 2, 3):
        n, d = k + 1, 2 ** (k + 1)
        unitary = tensor([S @ H if j % 2 else H for j in range(n)])
        for j in range(n - 1):
            unitary = cnot(n, j, j + 1) @ unitary
        for s in product((0, 1), repeat=k):
            ztarget = tensor([Z if bit else I for bit in s] + [Z])
            target = unitary @ ztarget @ unitary.conj().T
            trial = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
            observable = (trial + trial.conj().T) / 2
            observable /= max(1.0, np.max(np.abs(np.linalg.eigvalsh(observable))))
            clean_adv = np.trace(observable @ target).real / (2 * d)
            for eta in (0.0, 0.125, 0.3, 0.5):
                noisy_success = 0.0
                for c in (0, 1):
                    actual = np.zeros((d, d), dtype=complex)
                    null = np.zeros((d, d), dtype=complex)
                    for x in product((0, 1), repeat=k):
                        parity = sum(a * b for a, b in zip(s, x)) & 1
                        for e in (0, 1):
                            b = parity ^ e
                            vec = unitary[:, index(x + (b ^ c,))]
                            weight = (eta if e else 1 - eta) / 2**k
                            actual += weight * np.outer(vec, vec.conj())
                        for b in (0, 1):
                            vec = unitary[:, index(x + (b ^ c,))]
                            null += np.outer(vec, vec.conj()) / d
                    label = (-1)**c
                    expected = (np.eye(d) + label * (1 - 2 * eta) * target) / d
                    record("lpn_source", np.max(np.abs(actual - expected)))
                    record("lpn_null", np.max(np.abs(null - np.eye(d) / d)))
                    effect = (np.eye(d) + label * observable) / 2
                    noisy_success += 0.5 * np.trace(effect @ actual).real
                record("prediction_noise_identity",
                       abs(noisy_success - (0.5 + (1 - 2 * eta) * clean_adv)))

    # Check the supplementary nonuniform prior independently of its tensor proof.
    for k in (1, 2):
        n, d = k + 1, 2 ** (k + 1)
        D = 2 * d
        weighted = []
        for word, op in paulis(k):
            weight = np.prod([0.5 if j == 0 else 1 / 6 for j in word])
            weighted.append((float(weight), np.kron(op, Z)))
        record("local_collision", abs(sum(w * w for w, _ in weighted) - 3.0**(-k)))
        moment = sum(w * np.kron(np.kron(Z, op), np.kron(Z, op))
                     for w, op in weighted)
        delta = (2 / 3)**k
        record("local_moment", abs(np.max(np.abs(np.linalg.eigvalsh(moment))) - delta))
        phi = tensor([np.array([1.0, 0.0])] +
                     [np.array([1.0, 1j]) / np.sqrt(2)] * k +
                     [np.array([1.0, 0.0])])
        attained = sum(w * np.vdot(phi, np.kron(Z, op) @ phi).real**2
                       for w, op in weighted)
        record("local_moment", abs(attained - delta))
        # One-example X_T at both sizes, plus two examples at the smaller size.
        for T in ((1, 2) if k == 1 else (1,)):
            for gamma in (0.2, 0.8, 1.0):
                dim = d * D**T
                prediction = np.zeros((dim, dim), dtype=complex)
                for weight, unsigned in weighted:
                    for sign in (-1, 1):
                        target = sign * unsigned
                        tau = (np.eye(D) + gamma * np.kron(Z, target)) / D
                        prediction += weight / 2 * tensor([tau] * T + [target / d])
                actual = np.vdot(prediction, prediction).real
                expected = (3.0**(-k) / (2 * d * D**T)
                            * ((1 + gamma**2)**T - (1 - gamma**2)**T))
                record("local_second_moment", abs(actual - expected))

    return {
        "status": "passed",
        "seed": SEED,
        "absolute_tolerance": TOL,
        "source_qubits": [1, 2, 3],
        "bell_qubits": [1, 2, 3],
        "lpn_dimensions": [1, 2, 3],
        "local_prior_parity_dimensions": [1, 2],
        "case_counts": counts,
        "maximum_absolute_residuals": errors,
    }


if __name__ == "__main__":
    print(json.dumps(run_checks(), indent=2, sort_keys=True))
