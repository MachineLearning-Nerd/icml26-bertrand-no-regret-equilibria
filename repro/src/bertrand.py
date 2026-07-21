"""Clean-room implementation for "Revisiting the Bertrand Paradox via Equilibrium Analysis
of No-regret Learners" (arXiv 2602.21620). numpy, CPU.

Discrete Bertrand game: price set P = {1/k, 2/k, ..., 1}; non-increasing demand f: P->[0,1];
marginal cost c. Given a price profile, the lowest-priced firm serves all demand (ties split
equally). Utility of player i = (x_i - c_i) f(x_i) * [share won].
Monopoly utility of player i = max_x (x - c_i) f(x).
"""
from __future__ import annotations
import numpy as np

# ------------------------------------------------------------------ demand functions
def demand_const(x): return np.ones_like(np.atleast_1d(x, )) if hasattr(x, '__len__') else 1.0
def f_const(x):  return np.ones_like(np.asarray(x, dtype=float)) * 1.0
def f_linear(x): x = np.asarray(x, dtype=float); return np.maximum(0.0, 1.0 - x)
def f_quad(x):   x = np.asarray(x, dtype=float); return np.maximum(0.0, 1.0 - x) ** 2
def f_exp(x):    x = np.asarray(x, dtype=float); return np.exp(-x)
DEMANDS = {"constant": f_const, "linear": f_linear, "quadratic": f_quad, "exponential": f_exp}


def monopoly_utility(f, c, prices):
    s = (prices - c) * f(prices)
    return float(np.max(s)), int(np.argmax(s))


# ------------------------------------------------------------------ Bertrand payoff
def player_utility(x_i, x_other_min, n_tied, f, c_i):
    """Utility of a firm pricing x_i when the lowest *other* price is x_other_min and there are
    n_tied firms (incl. self) at the minimum price."""
    if x_i < x_other_min:
        return (x_i - c_i) * f(np.array([x_i]))[0]          # unique lowest: serves all
    if x_i == x_other_min:
        return (x_i - c_i) * f(np.array([x_i]))[0] / n_tied  # tied: split
    return 0.0


def profile_utilities(prices, f, costs):
    """Utilities for a full price profile (array). Lowest price wins; ties split."""
    pmin = prices.min()
    winners = np.where(prices == pmin)[0]
    share = 1.0 / len(winners)
    u = np.zeros_like(prices, dtype=float)
    u[winners] = (pmin - costs[winners]) * f(np.array([pmin]))[0] * share
    return u


# ------------------------------------------------------------------ CCE construction (Theorem 2.1)
def construct_symmetric_cce(f, c, k, B_frac):
    """Build the symmetric CCE from the proof of Theorem 2.1.

    prices i/k for i=1..k ; s_i=(i/k-c)f(i/k) ; S_i=prefix-max of s ; s_max=monopoly.
    B = B_frac * s_max ; i0 = smallest i with S_i>=B ; m = argmax s_i.
    tau_i = Pr[x>=i/k] = 1 (i<i0), B/S_i (i0<=i<=m), 0 (i>m).  Pr[x=i/k]=tau_i-tau_{i+1}.
    Returns the distribution over price indices (prob[i]), the per-player expected utility,
    the monopoly utility, and a CCE-validity flag (no profitable constant deviation)."""
    i_idx = np.arange(1, k + 1)
    prices = i_idx / k
    s = (prices - c) * f(prices)
    S = np.maximum.accumulate(s)
    s_max = float(s.max()); m = int(np.argmax(s))            # monopoly index
    B = B_frac * s_max
    ge = np.where(S >= B)[0]
    i0 = int(ge[0]) if len(ge) else 0                          # 0-based
    tau = np.zeros(k)
    for j in range(k):                                         # j 0-based => price (j+1)/k
        if j < i0:
            tau[j] = 1.0
        elif j <= m:
            tau[j] = B / S[j] if S[j] > 0 else 0.0
        else:
            tau[j] = 0.0
    prob = np.zeros(k)
    for j in range(k):
        nxt = tau[j + 1] if j + 1 < k else 0.0
        prob[j] = max(tau[j] - nxt, 0.0)
    if prob.sum() > 0:
        prob /= prob.sum()
    # per-player expected utility: both play same price x~prob => tied => each gets s/2
    per_player_U = float(np.sum(prob * s) / 2.0)
    # CCE validity: no profitable constant deviation. Deviating to fixed price p_j while the
    # other plays x~prob: utility = sum_i prob[i]*u1(p_j, price_i). CCE iff <= per_player_U for all j.
    max_dev = 0.0
    for j in range(k):
        pj = prices[j]
        dev_u = 0.0
        for i in range(k):
            pi = prices[i]
            if pj < pi:
                dev_u += prob[i] * (pj - c) * f(np.array([pj]))[0]
            elif pj == pi:
                dev_u += prob[i] * (pj - c) * f(np.array([pj]))[0] / 2.0
        max_dev = max(max_dev, dev_u)
    valid_cce = max_dev <= per_player_U + 1e-9
    return dict(prob=prob, prices=prices, per_player_U=per_player_U, monopoly=s_max,
                max_deviation=max_dev, valid_cce=valid_cce, B=B)


# ------------------------------------------------------------------ learners
def multiplicative_weights(n_actions, T, payoff_fn, eta=None, seed=0):
    """No-external-regret learner. payoff_fn(history_of_others) -> vector of payoffs per action.
    Returns chosen-action trajectory."""
    rng = np.random.default_rng(seed)
    if eta is None:
        eta = np.sqrt(np.log(n_actions) / T)
    w = np.ones(n_actions)
    traj = []
    for t in range(T):
        p = w / w.sum()
        a = rng.choice(n_actions, p=p)
        traj.append(a)
        pay = payoff_fn(t)                                    # vector of payoffs for each action
        w *= np.exp(eta * np.asarray(pay))
    return np.array(traj)


def regret_matching(n_actions, T, payoff_fn, seed=0):
    """No-swap-regret learner via regret matching (Hart-Mas-Colell). payoff_fn(t)->payoff vector
    for each action given the round-t opponent distribution. Minimizes swap regret."""
    rng = np.random.default_rng(seed)
    cum_regret = np.zeros(n_actions)         # external-regret accumulator (regret matching uses positive regret)
    traj = []
    for t in range(T):
        pos = np.maximum(cum_regret, 0.0)
        s = pos.sum()
        p = pos / s if s > 0 else np.ones(n_actions) / n_actions
        a = rng.choice(n_actions, p=p)
        traj.append(a)
        pay = np.asarray(payoff_fn(t))
        realized = pay[a]
        cum_regret += (pay - realized)       # regret of each action vs realized
    return np.array(traj)


def simulate_duo(no_swap1, no_swap2, f, c, k, T, seed=0):
    """Run a duopoly: each learner picks a price each round; both see the round payoff vector
    (payoff of each price against the opponent's LAST price). Returns time-avg per-player utility."""
    rng = np.random.default_rng(seed)
    prices = np.arange(1, k + 1) / k
    demand_at = f(prices)
    # state: opponent's last price index
    def make_payoff(opp_idx, self_c):
        u = np.zeros(k)
        opp_p = prices[opp_idx]
        for j in range(k):
            pj = prices[j]
            if pj < opp_p:
                u[j] = (pj - self_c) * demand_at[j]
            elif pj == opp_p:
                u[j] = (pj - self_c) * demand_at[j] / 2
        return u
    # pre-generate learner trajectories via online interaction
    last1, last2 = k - 1, k - 1
    w1 = np.ones(k); w2 = np.ones(k); R1 = np.zeros(k); R2 = np.zeros(k)
    eta = np.sqrt(np.log(k) / T)
    u1_sum = u2_sum = 0.0
    for t in range(T):
        p1 = np.maximum(R1, 0); p1 = p1 / p1.sum() if p1.sum() > 0 else np.ones(k) / k
        if no_swap1:
            w1p = p1
        else:
            w1p = w1 / w1.sum()
        p2 = np.maximum(R2, 0); p2 = p2 / p2.sum() if p2.sum() > 0 else np.ones(k) / k
        w2p = w2 / w2.sum() if not no_swap2 else p2
        a1 = rng.choice(k, p=w1p / w1p.sum()); a2 = rng.choice(k, p=w2p / w2p.sum())
        u1 = make_payoff(a2, c); u2 = make_payoff(a1, c)
        u1_sum += u1[a1]; u2_sum += u2[a2]
        if no_swap1:
            R1 += (u1 - u1[a1])
        else:
            w1 *= np.exp(eta * u1)
        if no_swap2:
            R2 += (u2 - u2[a2])
        else:
            w2 *= np.exp(eta * u2)
    return u1_sum / T, u2_sum / T


def simulate_n_player(n, f, c, k, T, seed=0):
    """n symmetric no-external-regret (multiplicative-weights) firms. Returns time-avg TOTAL utility."""
    rng = np.random.default_rng(seed)
    prices = np.arange(1, k + 1) / k
    demand_at = f(prices)
    W = np.ones((n, k)); eta = np.sqrt(np.log(k) / T)
    total = 0.0
    for t in range(T):
        probs = W / W.sum(1, keepdims=True)
        acts = np.array([rng.choice(k, p=probs[i]) for i in range(n)])
        chosen = prices[acts]
        pmin = chosen.min()
        winners = np.where(chosen == pmin)[0]
        share = 1.0 / len(winners)
        round_u = np.zeros(n)
        round_u[winners] = (pmin - c) * demand_at[acts[winners][0]] * share
        total += round_u.sum()
        for i in range(n):
            # payoff vector for firm i: for each price j, if j<pmin_others win, etc.
            others = np.delete(acts, i)
            omin = prices[others].min() if len(others) else 1e9
            uvec = np.zeros(k)
            for j in range(k):
                pj = prices[j]
                if pj < omin:
                    uvec[j] = (pj - c) * demand_at[j]
                elif pj == omin:
                    uvec[j] = (pj - c) * demand_at[j] / 2
            W[i] *= np.exp(eta * uvec)
    return total / T
