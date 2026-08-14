# Reproduction audit report

## Executive assessment

This is a clean-room, claim-by-claim audit of the ICML 2026 paper *Revisiting the Bertrand Paradox via Equilibrium Analysis of No-regret Learners*. The evidence-release package passes: six claim contracts, independent residual checks, deliberately invalid controls, durable artifacts, and the additive Space manifest are present. The scientific assessment is `VERIFIED_SCOPED`: all six finite contracts pass, but none replaces the paper's universal proofs.

The external judge remains authoritative. The recorded live score is `4/12`, and the published candidate is awaiting reevaluation; no score increase is claimed.

## Paper-to-repository association

The paper studies discrete Bertrand price competition under no-regret learning. The repository turns CCE, CE, and mixed Phi-equilibrium conditions into sparse linear programs over price distributions, recomputes residuals with an independent loop-based checker, and rejects intentionally invalid controls. It also corrects two earlier protocol substitutions: the quadratic demand is `1-x^2`, and Section 3.1 maximizes symmetric-CCE utility rather than a learning-trajectory output.

## Claim production ledger

| Claim | Producer | Evidence product | Assessment |
| --- | --- | --- | --- |
| C1 / CCE lower bound | `repro/src/verify_bertrand.py::claim1` and `symmetric_cce` | 124 rows, minimum normalized utility 0.285299, negative monopoly-point-mass control | `VERIFIED_SCOPED_FINITE_LP` |
| C2 / CE bound | `claim2` and `joint_equilibrium` with CE constraints | 24 player maxima, exact bound excess 0, weakened-CCE control | `VERIFIED_SCOPED_FINITE_LP` |
| C3 / mixed Phi | `claim3` with one CE-constrained and one CCE-constrained player | k=20,40,60 lower envelope 0.169306, full deviation enumeration | `VERIFIED_SCOPED_FINITE_LP` |
| C4 / many-firm decay | `claim4` with k=100 symmetric-CCE LPs and log-linear fits | 12 fits, negative slopes, theorem-bound checks, constant-sequence control | `VERIFIED_SCOPED_FINITE_NUMERICAL` |
| C5 / asymmetric costs | `claim5` with CCE max-min and high-cost CE objective | 12 k=30 cases, CCE fraction floor 0.314040, high-cost CE maximum 0 | `VERIFIED_SCOPED_CONDITIONAL_NUMERICAL` |
| C6 / 1/e section | `claim6` with k=10..100 source-demand curves | 12/12 endpoints within 0.03 and 0.05 rule, wrong-quadratic control rejected | `VERIFIED_SCOPED_NUMERICAL` |

## Controls and limitations

- C1 checks 100 seeded monotone stress sequences in addition to canonical demand/cost/grid cases, but finite checks cannot establish a universal quantifier.
- C2 checks the equilibrium polytope directly and does not claim a finite-time convergence rate for a particular learner.
- C3 reports the observed positive lower envelope without inventing an unspecified theorem constant.
- C4 fits the optimized symmetric-CCE utility and preserves the additive 1/k floor; a negative slope is not relabeled as a universal -1/2 exponent.
- C5 is conditional on the source assumptions and covers the declared four demand families and three high-cost values at k=30.
- C6 uses a declared 0.03/0.05 tolerance because the paper's word “roughly” has no numerical tolerance; the source curves and raw endpoint errors remain available.

## Published release

The candidate is additive: all 19 judged Space paths are present, 18 are byte-identical, and the expected logbook update is isolated. The published candidate revision is `9aac9487ad799104d583ba1d63c8184b9ad7085e`; the judged parent is `48d0b6f9269cadf6ae6894187ee0b4e2c34be70c`.

## Reproduction entry point

```bash
uv sync --frozen && uv run --frozen python repro/src/verify_bertrand.py
```

The environment and recorded runtime are in `evidence/faithful/environment.json` and `evidence/faithful/summary.json`.
