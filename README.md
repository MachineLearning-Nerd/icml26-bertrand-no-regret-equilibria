# Reproduction: regret type determines whether Bertrand prices stay high

This project reproduces six claims from
[*Revisiting the Bertrand Paradox via Equilibrium Analysis of No-regret Learners*](https://arxiv.org/abs/2602.21620).
The central test is whether external-regret equilibria permit high utility while
swap-regret equilibria restore competitive outcomes. We implemented the full
CCE, CE, and mixed-\(\Phi\) deviation constraints as inspectable sparse linear
programs, independently checked every residual, and added a failing negative
control for each claim.

**Assessment:** all six finite computational contracts are `VERIFIED` on local
CPU. The strongest new result is the missing asymmetric-cost check: across 12
demand/cost cases, the high-cost firm's CCE utility is at least **0.314040 of
monopoly**, while its maximum utility under the CE constraints is **exactly
zero**. For the numerical \(1/e\) claim, **12/12** source-faithful \(k=100\)
endpoints are within 0.03 of the paper's \(1/e=0.367879\); the worst observed
error is **0.022891**.

This is not a claimed judge-score increase. The live judge result remains
**4/12**. The faithful evidence is published at Space revision
[`9aac9487ad799104d583ba1d63c8184b9ad7085e`](https://huggingface.co/spaces/DineshAI/ZEP68RaUeR/commit/9aac9487ad799104d583ba1d63c8184b9ad7085e)
and is awaiting independent reevaluation.

The formal setup uses finite price grids (\(k\leq100\)), canonical source demand
families, and seeded monotone-demand stress cases. These LP certificates test the
paper's finite-game consequences; they do not replace its universal proofs. The
legacy \((1-x)^2\) demand was corrected to the paper's \(1-x^2\), and the
Section 3.1 target was corrected from a multiplicative-weights trajectory to the
paper's maximum over symmetric CCEs. Compute was an 8-thread Apple ARM local CPU;
no GPU or paid Hugging Face upgrade was used.

[Read the illustrated technical report](reports/bertrand-reproduction/report.md)
or open the self-contained tutorial notebook:

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-ZEP68RaUeR-bertrand-no-regret/blob/master/notebooks/bertrand_reproduction.py)

```bash
uv run --frozen marimo edit notebooks/bertrand_reproduction.py
uv run --frozen marimo run notebooks/bertrand_reproduction.py
```

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| [`orx/baseline-judged-numpy-proxy`](https://github.com/MachineLearning-Nerd/icml26-repro-ZEP68RaUeR-bertrand-no-regret/tree/orx/baseline-judged-numpy-proxy) | Frozen reproduction of the judged proxy | `uv sync --frozen && uv run --frozen python repro/src/verify_bertrand.py` | Reproduced the prior proxy; not six rigorous verifications | local CPU, 30 s orchestration |
| [`orx/faithful-lp-claim-suite`](https://github.com/MachineLearning-Nerd/icml26-repro-ZEP68RaUeR-bertrand-no-regret/tree/orx/faithful-lp-claim-suite) | Transparent LPs, source-faithful formulas, all six contracts and controls | `uv sync --frozen && uv run --frozen python repro/src/verify_bertrand.py` | Six local `VERIFIED` verdicts; 13.39 s scientific runtime | local CPU, 35 s orchestration |
| [`orx/durable-evidence-release-candidate`](https://github.com/MachineLearning-Nerd/icml26-repro-ZEP68RaUeR-bertrand-no-regret/tree/orx/durable-evidence-release-candidate) | Durable artifacts, report, notebook, additive Space candidate | `uv sync --frozen && uv run --frozen python repro/src/verify_bertrand.py` | Six local `VERIFIED` verdicts; 26.68 s scientific runtime | local CPU, 70 s orchestration |
| `master` | Published report, notebook, source, and exact Space text paths | Not run as an experiment (publication surface) | Published; awaiting external judge reevaluation | — |

## Repository background

# Repro — Revisiting the Bertrand Paradox via Equilibrium Analysis of No-regret Learners

ICML 2026 Agent Reproduction Challenge. OpenReview `ZEP68RaUeR`. arXiv `2602.21620`.
6 anchored claims / 12 pts. Clean-room CPU (numpy) verification of the no-regret / no-swap-regret
equilibrium results (Theorems 2.1–2.6) + the 1/e and e^(1−n/2) numerical phenomena. Owner: loop12pt.
