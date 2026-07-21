# STATUS — ZEP68RaUeR Revisiting the Bertrand Paradox via Equilibrium Analysis of No-regret Learners

**Owner:** loop12pt  ·  **arXiv:** 2602.21620  ·  **Points:** 6 claims / 12 pts  ·  **Tier:** cpu/high (externally verified)

## State: 6/6 CLAIMS VERIFIED (clean-room numpy, CPU, ~20 s)

`python repro/src/verify_bertrand.py` → `outputs/{verdict.json, verify_run.log}`.

| Claim | Theorem | Evidence | Result |
|---|---|---|---|
| c1 | Thm 2.1 — symmetric CCE, utility ≥ monopoly/(4e²) | constructive CCE (τ_i distribution); valid + per-player frac 0.32–0.36 ≥ 1/(4e²)=0.034 across {constant,linear,quadratic,exponential} | ✅ |
| c2 | Thm 2.2 — two no-swap-regret → utility ≤ f(c+1/k)/k | regret-matching duopoly: u1=u2=0.0123 ≤ bound 0.0244 (linear, exponential) | ✅ |
| c3 | Thm 2.3 — asymmetric (1 no-swap + 1 no-external-regret) sustains high utility | constant demand, 6/6 seeds min(u1,u2)/monopoly ≥ 0.05 | ✅ |
| c4 | Thm 2.5 — total utility ≤ 4f(c+1/k)/k + n(1−c)f(c+1/k)e^(1−n/2) | n=2..6 simulated total ≤ bound each; bound log-decay slope −0.21 (e^(1−n/2) term) | ✅ |
| c5 | Thm 2.6 — high-utility CCE for broad demand | constructive CCE frac 0.32–0.35 ≥ 0.05 (linear, quadratic, exponential) | ✅ |
| c6 | Numerical — utility/monopoly → 1/e | CCE (= no-external-regret limit) utility fraction mean 0.3435 ≈ 1/e=0.3679 | ✅ |

Negative/structure controls: CCE validity checked by brute-force over all constant price deviations (no profitable deviation); no-swap-regret verified via regret-matching convergence to a CE.

## NEXT (publish gate)
git init + GitHub `MachineLearning-Nerd/icml26-repro-ZEP68RaUeR-bertrand-no-regret` + enqueue → drain publishes HF Space → under_verdict. (Publish blocked pending the permission rule — see memory icml-repro-publish-permission-blocker.)
