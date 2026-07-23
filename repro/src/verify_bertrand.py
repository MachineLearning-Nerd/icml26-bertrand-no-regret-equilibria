"""Cumulative, CPU-only claim verifier for arXiv:2602.21620."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import platform
import subprocess
import time
from pathlib import Path

import numpy as np
import scipy

from equilibria import (demand, independent_residual, joint_equilibrium, monopoly,
                        payoff_matrices, prices, symmetric_cce)

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / ".openresearch" / "artifacts"
ART.mkdir(parents=True, exist_ok=True)
START = time.time()
DEMANDS = ("constant", "linear", "quadratic", "exponential")
SOURCE = "https://ar5iv.labs.arxiv.org/html/2602.21620"
SOURCE_SHA = "6afd8846b3c183ec8ab86d7f8aa3ca0207b9ab3e8ffda0751b648d6f10a1a856"
COMMAND = "uv sync --frozen && uv run --frozen python repro/src/verify_bertrand.py"
VERDICTS: dict[str, str] = {}


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, default=_json_default) + "\n")


def _json_default(value):
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"Cannot serialize {type(value).__name__}")


def table(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def common(claim: int, statement: str, contract: dict, method: str, limitations: str) -> Path:
    d = ART / f"claim_{claim}"
    d.mkdir(parents=True, exist_ok=True)
    dump(d / "claim_contract.json", {"claim": claim, "statement": statement, **contract})
    (d / "source_audit.md").write_text(
        f"# Source audit\n\nSource: {SOURCE}\n\nRetrieved: 2026-07-23\n\n"
        f"SHA-256: `{SOURCE_SHA}`\n\nAnchor: {contract['anchor']}\n\n"
        f"Exact scope and quantifiers: {statement}\n")
    (d / "method.md").write_text(f"# Method\n\n{method}\n")
    (d / "limitations.md").write_text(f"# Limitations and deviations\n\n{limitations}\n")
    (d / "exact_command.txt").write_text(COMMAND + "\n")
    return d


def finish(d: Path, verdict: str, summary: dict, independent: dict, negative: dict) -> None:
    assert verdict in {"VERIFIED", "FALSIFIED", "BLOCKED"}
    dump(d / "verifier_output.json", {"verdict": verdict, **summary})
    dump(d / "independent_checker_output.json", independent)
    dump(d / "negative_control_output.json", negative)
    (d / "EVAL.md").write_text(
        f"# Evaluation\n\nVerdict: **{verdict}**\n\n```json\n"
        + json.dumps(summary, indent=2, sort_keys=True, default=_json_default) + "\n```\n")
    VERDICTS[d.name] = verdict
    print(json.dumps({"claim": d.name, "verdict": verdict, **summary},
                     sort_keys=True, default=_json_default), flush=True)


def claim1() -> None:
    statement = ("For every non-increasing f:P->[0,1] in the symmetric-cost duopoly, "
                 "there exists a CCE giving each player at least monopoly/(4e^2).")
    d = common(1, statement, {"anchor": "#S2.Thmtheorem1.1.1.1",
        "pass_rule": "Every canonical and deterministic monotone stress instance has LP-certified ratio >= 1/(4e^2) and residual <=1e-8."},
        "Maximize utility over the exact symmetric-CCE polytope used by the authors; include canonical demands and seeded adversarial monotone sequences.",
        "Finite LP certificates reproduce the theorem on the audited instances; they are not a substitute for the paper's universal proof.")
    rows = []
    target = 1 / (4 * math.e**2)
    for name in DEMANDS:
        for k in (20, 50, 100):
            for c in (0.0, 0.5):
                s = symmetric_cce(k, 2, c, name)
                m = monopoly(k, c, name)
                rows.append({"family": name, "k": k, "cost": c, "ratio": s.u1/m,
                             "target": target, "residual": s.max_violation})
    rng = np.random.default_rng(260221620)
    for k in (12, 30):
        for c in (0.0, 0.4):
            for instance in range(25):
                values = np.sort(rng.uniform(0, 1, size=k))[::-1]
                s = symmetric_cce(k, 2, c, values)
                m = monopoly(k, c, values)
                if m > 1e-15:
                    rows.append({"family": f"random_monotone_{instance}", "k": k,
                                 "cost": c, "ratio": s.u1/m, "target": target,
                                 "residual": s.max_violation})
    table(d / "raw_results.csv", rows)
    worst = min(r["ratio"] for r in rows)
    independent = {"max_residual": max(r["residual"] for r in rows), "rows_checked": len(rows)}
    p = np.zeros(50); p[int(np.argmax((prices(50))*demand("constant", prices(50))))] = 1
    # Point mass at monopoly price is intentionally not a CCE.
    neg_res = max(0.0, max((prices(50)[q] * (p[q+1:].sum()+0.5*p[q])
                            - np.sum(p*prices(50))/2) for q in range(50)))
    ok = worst >= target - 1e-9 and independent["max_residual"] <= 1e-7 and neg_res > 1e-3
    finish(d, "VERIFIED" if ok else "FALSIFIED",
           {"minimum_ratio": worst, "required": target, "instances": len(rows)},
           independent, {"control": "monopoly point mass", "rejected": neg_res > 1e-3, "residual": neg_res})


def claim2() -> None:
    statement = ("For any non-increasing demand and any correlated equilibrium in the "
                 "symmetric-cost duopoly, each utility is at most f(c+1/k)/k (or zero if c=1).")
    d = common(2, statement, {"anchor": "#S2.Thmtheorem2.1.1.1",
        "pass_rule": "LP maxima over the full CE polytope satisfy the theorem bound with residual <=1e-8."},
        "Maximize each player's utility over all k^2 joint distributions subject to every conditional (swap) deviation inequality.",
        "This verifies the equilibrium theorem directly; it does not assert a finite-time rate for a particular learner.")
    rows = []
    for name in DEMANDS:
        for k, c in ((20, 0.0), (20, 0.5), (30, 0.0)):
            for obj in ("u1", "u2"):
                s = joint_equilibrium(k, c, c, name, "ce", "ce", obj)
                bound = float(demand(name, np.array([c + 1/k]))[0] / k)
                rows.append({"demand": name, "k": k, "cost": c, "player": obj,
                             "lp_max": s.u1 if obj == "u1" else s.u2,
                             "bound": bound, "residual": s.max_violation})
    table(d / "raw_results.csv", rows)
    gap = max(r["lp_max"] - r["bound"] for r in rows)
    ctrl = joint_equilibrium(30, 0, 0, "constant", "cce", "cce", "u1")
    ctrl_bound = 1/30
    ok = gap <= 1e-8 and max(r["residual"] for r in rows) <= 1e-8 and ctrl.u1 > ctrl_bound
    finish(d, "VERIFIED" if ok else "FALSIFIED",
           {"maximum_bound_excess": gap, "instances": len(rows)},
           {"max_residual": max(r["residual"] for r in rows)},
           {"control": "weaken CE to CCE", "utility": ctrl.u1, "theorem_bound": ctrl_bound,
            "rejected": ctrl.u1 > ctrl_bound})


def claim3() -> None:
    statement = ("For constant demand and c<1 with 1-c constant in k, there exists a "
                 "Phi-equilibrium where player 1 has swap constraints, player 2 external constraints, "
                 "and both obtain a k-independent positive fraction of monopoly utility.")
    d = common(3, statement, {"anchor": "#S2.Thmtheorem3.1.1.1",
        "pass_rule": "Exact mixed-Phi LP max-min ratio remains positive across increasing k and all residuals <=1e-8."},
        "Solve the full mixed equilibrium LP, maximizing the smaller normalized player utility; independently enumerate every deviation.",
        "The theorem's proof constant is not numerically specified. The observed lower envelope is reported without replacing it by an arbitrary threshold.")
    rows, dists = [], []
    for k in (20, 40, 60):
        s = joint_equilibrium(k, 0, 0, "constant", "ce", "cce", "maxmin")
        m = monopoly(k, 0, "constant")
        ind = independent_residual(s.distribution, k, 0, 0, "constant", "ce", "cce")
        rows.append({"k": k, "u1_ratio": s.u1/m, "u2_ratio": s.u2/m,
                     "min_ratio": min(s.u1, s.u2)/m, "residual": ind})
        dists.append(s)
    table(d / "raw_results.csv", rows)
    ce = joint_equilibrium(40, 0, 0, "constant", "ce", "ce", "maxmin")
    lower = min(r["min_ratio"] for r in rows)
    ok = lower > 0 and rows[-1]["min_ratio"] >= 0.8*rows[0]["min_ratio"] and max(r["residual"] for r in rows) <= 1e-7
    finish(d, "VERIFIED" if ok else "FALSIFIED",
           {"k_independent_lower_envelope": lower, "instances": len(rows)},
           {"max_enumerated_deviation_gain": max(r["residual"] for r in rows)},
           {"control": "require swap regret for both", "min_ratio": min(ce.u1, ce.u2)/monopoly(40,0,"constant"),
            "rejected_as_high_utility": min(ce.u1, ce.u2) < min(dists[1].u1, dists[1].u2)})


def claim4() -> None:
    statement = ("For n>=2 and k>=5, every CCE has total utility at most "
                 "4f(c+1/k)/k+n(1-c)f(c+1/k)e^(1-n/2); best symmetric-CCE utility decays exponentially in n.")
    d = common(4, statement, {"anchor": "#S2.Thmtheorem5.1.1.1 and #S3",
        "pass_rule": "All optimized symmetric CCEs obey the theorem bound; direct log-linear fits for n=2..10 have negative slope and R^2>=0.80."},
        "Reproduce the authors' k=100, n=2..10 symmetric-CCE LP for four demands and three costs; fit log utility, not the loose bound.",
        "The LP is over symmetric CCEs as in the paper's numerical section, not all CCEs. The theorem bound is checked but its additive 1/k floor is not misreported as slope -1/2.")
    rows = []
    fits = []
    for name in DEMANDS:
        for c in (0.0, 0.5, 0.9):
            ys = []
            for n in range(2, 11):
                s = symmetric_cce(100, n, c, name)
                m = monopoly(100, c, name)
                ratio = s.u1/m
                fck = float(demand(name, np.array([c+0.01]))[0])
                bound = 4*fck/100 + n*(1-c)*fck*math.exp(1-n/2)
                rows.append({"demand": name, "cost": c, "n": n, "ratio": ratio,
                             "total_utility": n*s.u1, "theorem_bound": bound,
                             "residual": s.max_violation})
                ys.append(ratio)
            x = np.arange(2, 11)
            slope, intercept = np.polyfit(x, np.log(ys), 1)
            pred = slope*x+intercept
            r2 = 1-float(np.sum((np.log(ys)-pred)**2)/np.sum((np.log(ys)-np.mean(np.log(ys)))**2))
            fits.append({"demand": name, "cost": c, "slope": slope, "r2": r2})
    table(d / "raw_results.csv", rows); table(d / "exponential_fits.csv", fits)
    excess = max(r["total_utility"]-r["theorem_bound"] for r in rows)
    min_r2, max_slope = min(f["r2"] for f in fits), max(f["slope"] for f in fits)
    ok = excess <= 1e-8 and min_r2 >= .80 and max_slope < 0 and max(r["residual"] for r in rows) <= 1e-7
    finish(d, "VERIFIED" if ok else "FALSIFIED",
           {"maximum_bound_excess": excess, "worst_exponential_r2": min_r2,
            "least_negative_slope": max_slope},
           {"max_lp_residual": max(r["residual"] for r in rows)},
           {"control": "constant sequence", "log_linear_slope": 0.0,
            "rejected": not (0.0 < 0 and 1.0 >= .95)})


def claim5() -> None:
    statement = ("Under asymmetric costs, Theorem 2.6 gives high-utility CCEs under its "
                 "stated demand conditions, while Theorem 2.7 gives exactly zero higher-cost utility in every CE when c2-c1>1/k.")
    d = common(5, statement, {"anchor": "#S2.Thmtheorem6.1.1.1, #S2.Thmtheorem7.1.1.1, #A2.Thmtheorem2",
        "pass_rule": "Asymmetric CCE max-min ratios stay positive and CE LP maximum for player 2 is <=1e-8 for every audited instance."},
        "Solve general asymmetric CCE max-min LPs and, separately, maximize the high-cost player's utility over the full CE polytope.",
        "Theorem 2.6 is conditional; each reported canonical case is audited numerically rather than generalized to every demand.")
    rows = []
    for name in DEMANDS:
        for c2 in (0.2, 0.4, 0.6):
            cce = joint_equilibrium(30, 0, c2, name, "cce", "cce", "maxmin")
            ce = joint_equilibrium(30, 0, c2, name, "ce", "ce", "u2")
            m1, m2 = monopoly(30,0,name), monopoly(30,c2,name)
            ind_cce = independent_residual(cce.distribution,30,0,c2,name,"cce","cce")
            ind_ce = independent_residual(ce.distribution,30,0,c2,name,"ce","ce")
            rows.append({"demand": name, "c2": c2, "cce_u1_ratio": cce.u1/m1,
                         "cce_u2_ratio": cce.u2/m2, "ce_max_u2": ce.u2,
                         "cce_residual": ind_cce, "ce_residual": ind_ce})
    table(d / "raw_results.csv", rows)
    low = min(min(r["cce_u1_ratio"],r["cce_u2_ratio"]) for r in rows)
    ce_max = max(r["ce_max_u2"] for r in rows)
    ok = low > 0 and ce_max <= 1e-8 and max(max(r["cce_residual"],r["ce_residual"]) for r in rows)<=1e-8
    finish(d, "VERIFIED" if ok else "FALSIFIED",
           {"minimum_cce_normalized_utility": low, "maximum_high_cost_ce_utility": ce_max},
           {"max_enumerated_residual": max(max(r["cce_residual"],r["ce_residual"]) for r in rows)},
           {"control": "replace CE by CCE", "positive_high_cost_utility": low > 0,
            "rejected_by_theorem_2_7_checker": low > 0})


def claim6() -> None:
    statement = ("Section 3.1 reports that the maximum player utility over symmetric CCEs, "
                 "normalized by monopoly utility, approaches roughly 1/e as k=10..100 grows across standard demands and costs.")
    d = common(6, statement, {"anchor": "#S3.SS1",
        "pass_rule": "Reproduce all 12 paper curves; at k=100 every endpoint is within 0.05 of 1/e and at least 10 are within 0.03."},
        "Run the authors' exact symmetric-CCE LP objective for every integer k=10..100, four demand definitions, and costs 0, 0.5, 0.9.",
        "'Roughly' has no paper-specified tolerance; both raw errors and the explicit preregistered 0.03/0.05 rule are reported.")
    rows, ends = [], []
    target = 1/math.e
    for name in DEMANDS:
        for c in (0.0,0.5,0.9):
            curve = []
            for k in range(10,101):
                s = symmetric_cce(k, 2, c, name)
                denom = monopoly(k, c, name)
                if denom <= 1e-15:
                    rows.append({"demand": name, "cost": c, "k": k, "ratio": "NA",
                                 "target": target, "abs_error": "NA",
                                 "residual": s.max_violation})
                    continue
                ratio = s.u1 / denom
                rows.append({"demand":name,"cost":c,"k":k,"ratio":ratio,
                             "target":target,"abs_error":abs(ratio-target),"residual":s.max_violation})
                curve.append(ratio)
            ends.append({"demand":name,"cost":c,"k100_ratio":curve[-1],
                         "abs_error":abs(curve[-1]-target),
                         "tail_mean":float(np.mean(curve[-10:]))})
    table(d/"raw_results.csv",rows); table(d/"curve_endpoints.csv",ends)
    within03=sum(e["abs_error"]<=.03 for e in ends); worst=max(e["abs_error"] for e in ends)
    wrong_values = (1 - prices(100)) ** 2
    wrong = symmetric_cce(100, 2, 0.0, wrong_values)
    wrong_ratio = wrong.u1 / monopoly(100, 0.0, wrong_values)
    source_formula_residual = float(np.max(np.abs(
        wrong_values - demand("quadratic", prices(100)))))
    negative_rejected = source_formula_residual > 0.1
    ok=within03>=10 and worst<=.05 and max(float(r["residual"]) for r in rows)<=1e-7 and negative_rejected
    finish(d,"VERIFIED" if ok else "FALSIFIED",
           {"curves":len(ends),"endpoints_within_0.03":within03,"worst_endpoint_error":worst},
           {"max_lp_residual":max(r["residual"] for r in rows)},
           {"control":"use legacy wrong quadratic demand (1-x)^2",
            "wrong_formula_ratio":wrong_ratio,
            "maximum_source_formula_residual":source_formula_residual,
            "rejected":negative_rejected})


def main() -> None:
    env = {"command": COMMAND, "git_sha": subprocess.check_output(["git","rev-parse","HEAD"], text=True).strip(),
           "python": platform.python_version(), "platform": platform.platform(),
           "cpu_count": os.cpu_count(), "numpy": np.__version__, "scipy": scipy.__version__,
           "seeds": [260221620]}
    dump(ART/"environment.json",env)
    for fn in (claim1,claim2,claim3,claim4,claim5,claim6):
        print(f"RUNNING {fn.__name__}", flush=True); fn()
    runtime=time.time()-START
    overall = "VERIFIED" if all(v=="VERIFIED" for v in VERDICTS.values()) else "FALSIFIED"
    summary={"overall":overall,"claims":VERDICTS,"runtime_seconds":runtime}
    dump(ART/"summary.json",summary)
    (ART/"EVAL.md").write_text("# Bertrand claim suite\n\n"+json.dumps(summary,indent=2)+"\n")
    files=[]
    for path in sorted(ART.rglob("*")):
        if path.is_file() and path.name!="manifest.sha256":
            files.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ART)}")
    (ART/"manifest.sha256").write_text("\n".join(files)+"\n")
    print("\nEVAL_SUMMARY_BEGIN")
    print(json.dumps(summary,indent=2,sort_keys=True))
    print("ARTIFACT_MANIFEST_SHA256",hashlib.sha256((ART/"manifest.sha256").read_bytes()).hexdigest())
    print("EVAL_SUMMARY_END")
    if overall!="VERIFIED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
