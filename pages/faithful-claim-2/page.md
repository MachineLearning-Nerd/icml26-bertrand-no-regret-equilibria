# Claim 2 — faithful finite-game verifier

## Verdict

**VERIFIED** under the explicit finite claim contract.

```json
{
  "instances": 24,
  "maximum_bound_excess": 0.0,
  "verdict": "VERIFIED"
}
```

# Source audit

Source: https://ar5iv.labs.arxiv.org/html/2602.21620

Retrieved: 2026-07-23

SHA-256: `6afd8846b3c183ec8ab86d7f8aa3ca0207b9ab3e8ffda0751b648d6f10a1a856`

Anchor: #S2.Thmtheorem2.1.1.1

Exact scope and quantifiers: For any non-increasing demand and any correlated equilibrium in the symmetric-cost duopoly, each utility is at most f(c+1/k)/k (or zero if c=1).

# Method

Maximize each player's utility over all k^2 joint distributions subject to every conditional (swap) deviation inequality.

## Durable evidence

All text artifacts are available under
`evidence/faithful/claim_2/`: contract, source audit, method, raw data,
verifier result, independent checker output, negative control, exact command,
limitations, and evaluation.

# Limitations and deviations

This verifies the equilibrium theorem directly; it does not assert a finite-time rate for a particular learner.

This local verdict is not a prediction of the live judge score. Universal
theorems remain proof-backed; the finite certificates do not replace proofs.
