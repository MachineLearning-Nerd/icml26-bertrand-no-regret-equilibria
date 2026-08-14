# ICML 2026 reproduction — Revisiting the Bertrand Paradox via Equilibrium Analysis of No-regret Learners

**Collection status:** `VERIFIED_SCOPED`

**Evidence-release gate:** `PASSED`

**Strict paper-level gate:** `NOT_READY` because finite LP certificates do not replace the paper's universal proofs.

**Owner and attribution:** `MachineLearning-Nerd`

This repository audits *Revisiting the Bertrand Paradox via Equilibrium Analysis of No-regret Learners* by Arnab Maiti, Junyan Liu, Kevin Jamieson, and Lillian J. Ratliff. The authoritative source is [arXiv 2602.21620v2](https://arxiv.org/abs/2602.21620), listed as an ICML 2026 paper. The OpenReview identifier is `ZEP68RaUeR`.

The downloaded arXiv PDF SHA-256 is `d8e4337c5c5910bf799d4b9ade203730b006dcdd9d77f32d8e0f3fc5732319a2`. The source-audit HTML hash is recorded in [`SOURCE_MANIFEST.md`](SOURCE_MANIFEST.md).

The original repository name was `icml26-repro-ZEP68RaUeR-bertrand-no-regret`. The target public name is `icml26-bertrand-no-regret-equilibria`.

## What the paper is doing

The paper studies a discrete Bertrand pricing game in which firms choose prices from a finite grid. The lowest-price firm captures demand, ties split demand, and demand is non-increasing in price. The central question is whether repeated price selection by no-regret learners must reproduce the classical low-price Bertrand outcome.

The answer depends on the regret notion. External regret leads to coarse correlated equilibrium (CCE) constraints that can retain high-utility outcomes. Swap regret imposes the stronger correlated-equilibrium (CE) constraints and can force competitive outcomes. The paper analyzes CCE, CE, mixed Phi-equilibrium constraints, asymmetric costs, many-firm decay, and a numerical 1/e phenomenon.

## Evidence status by paper claim

The labels below describe the finite grid, demand family, cost, and firm-count contracts actually run. They are not replacements for universal theorem proofs.

| Claim | Paper target | Scoped status | Recorded evidence |
| --- | --- | --- | --- |
| C1 | Theorem 2.1 — each firm has a CCE utility fraction at least 1/(4e^2) | `VERIFIED_SCOPED_FINITE_LP` | 124 canonical/stress instances; minimum ratio 0.285299 versus 0.033834 floor; independent residual checks |
| C2 | Theorem 2.2 — CE utility is bounded by f(c+1/k)/k | `VERIFIED_SCOPED_FINITE_LP` | 24 player-specific LP maxima; maximum bound excess 0 |
| C3 | Theorem 2.3 — mixed swap/external equilibrium retains a k-independent positive fraction | `VERIFIED_SCOPED_FINITE_LP` | k = 20, 40, 60; lower envelope 0.169306; full deviation enumeration |
| C4 | Theorem 2.5 and Section 3 — many-firm utility obeys the exponential bound/decay | `VERIFIED_SCOPED_FINITE_NUMERICAL` | 12 demand/cost fits at k=100; least-negative slope -0.2344; worst R2 0.8283; bound excess -0.004348 |
| C5 | Theorems 2.6–2.7 — asymmetric CCE can retain high-cost utility while CE eliminates it | `VERIFIED_SCOPED_CONDITIONAL_NUMERICAL` | 12 k=30 demand/cost cases; minimum CCE fraction 0.314040; maximum high-cost CE utility 0 |
| C6 | Section 3.1 — best symmetric-CCE utility approaches roughly 1/e | `VERIFIED_SCOPED_NUMERICAL` | 12 curves over k = 10..100; all k=100 endpoints within 0.05 and 12/12 within 0.03; worst error 0.022891 |

All six finite contracts pass and no claim is marked falsified. C5 is explicitly conditional on the theorem's asymmetric-demand assumptions. C6 uses a declared tolerance because the source says “roughly” without specifying one. The full evidence records every scope and limitation.

## Claim-to-evidence production paths

| Claim | Producer path | Canonical evidence |
| --- | --- | --- |
| C1 CCE lower bound | `repro/src/verify_bertrand.py::claim1` and `repro/src/equilibria.py::symmetric_cce` | `evidence/faithful/claim_1/` and `.openresearch/artifacts/claim_1/` |
| C2 CE bound | `verify_bertrand.py::claim2` and `equilibria.py::joint_equilibrium(..., "ce", "ce")` | `evidence/faithful/claim_2/` |
| C3 mixed Phi equilibrium | `verify_bertrand.py::claim3` with CE/CCE mixed constraints and independent deviations | `evidence/faithful/claim_3/` |
| C4 many-firm decay | `verify_bertrand.py::claim4` with symmetric-CCE LPs and log-linear fits | `evidence/faithful/claim_4/` |
| C5 asymmetric costs | `verify_bertrand.py::claim5` with CCE max-min and high-cost CE maximization | `evidence/faithful/claim_5/` |
| C6 1/e numerical section | `verify_bertrand.py::claim6` over four source demands and three costs | `evidence/faithful/claim_6/` |
| Aggregate release | `repro/src/verify_bertrand.py` writes durable artifacts and the release manifest | `evidence/faithful/`, `.openresearch/artifacts/`, `release/` |

The current `repro/src/verify_bertrand.py` is byte-identical to `repro/faithful/verify_bertrand.py`. The raw machine verdicts intentionally remain `VERIFIED` for their finite contracts; this README supplies the necessary scoped interpretation.

## Experiment branches

Every formal experiment uses:

```bash
uv sync --frozen && uv run --frozen python repro/src/verify_bertrand.py
```

| Final branch | Purpose | Outcome |
| --- | --- | --- |
| `main` | Canonical publication surface | README, report, notebook, source, and gate metadata |
| `baseline/judged-numpy-proxy` | Frozen judged baseline | Preserves the original proxy reproduction |
| `research/faithful-lp-claim-suite` | Source-faithful LP implementation | Six finite claim contracts and controls |
| `release/durable-evidence` | Durable evidence and additive Space candidate | Published candidate awaiting judge reevaluation |

The old `master` and `orx/*` names are retained only as provenance in [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md); they are not the final public branch policy.

## Recorded release evidence

- Scientific verifier runtime: 13.388 seconds; orchestration recorded as approximately 35 seconds.
- Environment: Python 3.12.11, NumPy 2.5.1, SciPy 1.18.0, eight Apple ARM CPU threads, deterministic seed `260221620`.
- No GPU or paid Hugging Face compute was used.
- Judged Space revision: `48d0b6f9269cadf6ae6894187ee0b4e2c34be70c`.
- Published additive candidate: `9aac9487ad799104d583ba1d63c8184b9ad7085e`.
- The candidate preserves all 19 old Space paths, with 18 byte-identical files and the expected logbook update.
- The current live judge result remains `4/12`; no score increase is claimed.

## Reproduce and inspect

The locked environment is declared in `pyproject.toml` and `uv.lock`.

```bash
uv sync --frozen
uv run --frozen python repro/src/verify_bertrand.py
uv run --frozen marimo edit notebooks/bertrand_reproduction.py
```

Use the claim evidence directories and `publication_gate.json` to inspect the recorded release without rerunning the campaign. The command exits nonzero if a scientific contract or its negative control behaves incorrectly.

## Repository contents

- `repro/src/` — sparse LP formulation, payoff construction, and cumulative verifier.
- `repro/faithful/` — source-faithful verifier copy used to build the durable release.
- `evidence/faithful/` — claim contracts, source audits, methods, raw CSVs, independent checks, negative controls, commands, and limitations.
- `.openresearch/artifacts/` — durable machine-readable claim outputs.
- `reports/bertrand-reproduction/report.md` — illustrated claim-by-claim narrative.
- `pages/` — published Space navigation and claim pages.
- `release/` — candidate revisions, allowlist, hash manifest, and judge state.
- `outputs/` — historical compatibility outputs; see [`outputs/README.md`](outputs/README.md).

## Citation

```bibtex
@article{maiti2026bertrand,
  title   = {Revisiting the Bertrand Paradox via Equilibrium Analysis of No-regret Learners},
  author  = {Maiti, Arnab and Liu, Junyan and Jamieson, Kevin and Ratliff, Lillian J.},
  journal = {arXiv preprint arXiv:2602.21620},
  year    = {2026},
  note    = {ICML 2026}
}
```

## Thank you

Thank you to Arnab Maiti, Junyan Liu, Kevin Jamieson, and Lillian J. Ratliff for making the equilibrium formulations, regret distinctions, and numerical targets precise enough to support a transparent clean-room audit. This repository is unofficial; the authors did not review or endorse these results.
