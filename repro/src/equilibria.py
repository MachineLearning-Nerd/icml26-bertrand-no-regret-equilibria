"""Transparent LP formulations for the finite Bertrand games in arXiv:2602.21620."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_matrix, hstack, vstack


def prices(k: int) -> np.ndarray:
    return np.arange(1, k + 1, dtype=float) / k


def demand(name: str | np.ndarray, x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if not isinstance(name, str):
        values = np.asarray(name, dtype=float)
        if values.shape != x.shape:
            raise ValueError("Explicit demand values must match the price grid")
        return values
    if name == "constant":
        return np.ones_like(x)
    if name == "linear":
        return np.maximum(0.0, 1.0 - x)
    if name == "quadratic":
        return np.maximum(0.0, 1.0 - x * x)
    if name == "exponential":
        return np.exp(-x)
    raise KeyError(name)


def monopoly(k: int, cost: float, name: str | np.ndarray) -> float:
    p = prices(k)
    return float(np.max((p - cost) * demand(name, p)))


def payoff_matrices(k: int, c1: float, c2: float, name: str) -> tuple[np.ndarray, np.ndarray]:
    p = prices(k)
    f = demand(name, p)
    g1, g2 = (p - c1) * f, (p - c2) * f
    a, b = p[:, None], p[None, :]
    u1 = np.where(a < b, g1[:, None], np.where(a == b, g1[:, None] / 2, 0.0))
    u2 = np.where(b < a, g2[None, :], np.where(a == b, g2[None, :] / 2, 0.0))
    return u1, u2


@dataclass
class LPSolution:
    distribution: np.ndarray
    u1: float
    u2: float
    objective: float
    max_violation: float
    status: str


def symmetric_cce(k: int, n: int, cost: float, name: str | np.ndarray) -> LPSolution:
    p = prices(k)
    g = (p - cost) * demand(name, p)
    realized = g / n
    rows = np.empty((k, k))
    for q in range(k):
        dev = np.zeros(k)
        dev[q] = g[q] / n
        dev[q + 1 :] = g[q]
        rows[q] = dev - realized
    res = linprog(-realized, A_ub=rows, b_ub=np.zeros(k),
                  A_eq=np.ones((1, k)), b_eq=[1.0], bounds=(0, 1), method="highs")
    if not res.success:
        raise RuntimeError(res.message)
    x = res.x
    violation = float(max(0.0, np.max(rows @ x), abs(x.sum() - 1), -x.min()))
    u = float(realized @ x)
    return LPSolution(x, u, u, u, violation, res.message)


def _equilibrium_matrix(k: int, c1: float, c2: float, name: str,
                        player1: str, player2: str) -> tuple[csr_matrix, np.ndarray, np.ndarray]:
    """Rows encode deviation payoff minus realized payoff <= 0."""
    u1, u2 = payoff_matrices(k, c1, c2, name)
    nvar = k * k
    rr: list[int] = []
    cc: list[int] = []
    dd: list[float] = []
    row = 0

    def add(indices: np.ndarray, values: np.ndarray) -> None:
        nonlocal row
        nz = np.flatnonzero(np.abs(values) > 0)
        rr.extend([row] * len(nz))
        cc.extend(indices[nz].tolist())
        dd.extend(values[nz].tolist())
        row += 1

    if player1 == "cce":
        real = u1.reshape(-1)
        for q in range(k):
            dev = np.tile(payoff_matrices(k, c1, c2, name)[0][q], k)
            add(np.arange(nvar), dev - real)
    else:
        for a in range(k):
            idx = a * k + np.arange(k)
            for q in range(k):
                add(idx, u1[q, :] - u1[a, :])

    if player2 == "cce":
        real = u2.reshape(-1)
        for q in range(k):
            dev = np.repeat(u2[:, q], k)
            add(np.arange(nvar), dev - real)
    else:
        for b in range(k):
            idx = np.arange(k) * k + b
            for q in range(k):
                add(idx, u2[:, q] - u2[:, b])
    mat = coo_matrix((dd, (rr, cc)), shape=(row, nvar)).tocsr()
    return mat, u1.reshape(-1), u2.reshape(-1)


def joint_equilibrium(k: int, c1: float, c2: float, name: str,
                      player1: str = "cce", player2: str = "cce",
                      objective: str = "maxmin") -> LPSolution:
    a, u1, u2 = _equilibrium_matrix(k, c1, c2, name, player1, player2)
    nvar = k * k
    eq = csr_matrix(np.ones((1, nvar)))
    if objective == "maxmin":
        m1, m2 = monopoly(k, c1, name), monopoly(k, c2, name)
        extra = csr_matrix(np.vstack((-u1 / m1, -u2 / m2)))
        aub = vstack((hstack((a, csr_matrix((a.shape[0], 1)))),
                      hstack((extra, np.ones((2, 1)))))).tocsr()
        obj = np.zeros(nvar + 1)
        obj[-1] = -1
        aeq = hstack((eq, csr_matrix((1, 1)))).tocsr()
        bounds = [(0, 1)] * nvar + [(None, None)]
    else:
        target = u1 if objective == "u1" else u2
        aub, obj, aeq = a, -target, eq
        bounds = [(0, 1)] * nvar
    res = linprog(obj, A_ub=aub, b_ub=np.zeros(aub.shape[0]),
                  A_eq=aeq, b_eq=[1.0], bounds=bounds, method="highs")
    if not res.success:
        raise RuntimeError(f"{player1}/{player2} {objective}: {res.message}")
    x = res.x[:nvar]
    violation = float(max(0.0, np.max(a @ x), abs(x.sum() - 1), -x.min()))
    eu1, eu2 = float(u1 @ x), float(u2 @ x)
    value = float(-res.fun)
    return LPSolution(x.reshape(k, k), eu1, eu2, value, violation, res.message)


def independent_residual(dist: np.ndarray, k: int, c1: float, c2: float, name: str,
                         player1: str, player2: str) -> float:
    """Loop-based checker independent of the sparse LP builder."""
    u1, u2 = payoff_matrices(k, c1, c2, name)
    eu1, eu2 = float(np.sum(dist * u1)), float(np.sum(dist * u2))
    worst = max(abs(float(dist.sum()) - 1), float(max(0, -dist.min())))
    if player1 == "cce":
        for q in range(k):
            worst = max(worst, float(np.sum(dist * u1[q, :][None, :]) - eu1))
    else:
        for a in range(k):
            for q in range(k):
                worst = max(worst, float(np.sum(dist[a, :] * (u1[q, :] - u1[a, :]))))
    if player2 == "cce":
        for q in range(k):
            worst = max(worst, float(np.sum(dist * u2[:, q][:, None]) - eu2))
    else:
        for b in range(k):
            for q in range(k):
                worst = max(worst, float(np.sum(dist[:, b] * (u2[:, q] - u2[:, b]))))
    return max(0.0, worst)
