# Claim 1 — faithful finite-game verifier

## Verdict

**VERIFIED** under the explicit finite claim contract.

```json
{
  "instances": 124,
  "minimum_ratio": 0.28529871914814614,
  "required": 0.033833820809153176,
  "verdict": "VERIFIED"
}
```

# Source audit

Source: https://ar5iv.labs.arxiv.org/html/2602.21620

Retrieved: 2026-07-23

SHA-256: `6afd8846b3c183ec8ab86d7f8aa3ca0207b9ab3e8ffda0751b648d6f10a1a856`

Anchor: #S2.Thmtheorem1.1.1.1

Exact scope and quantifiers: For every non-increasing f:P->[0,1] in the symmetric-cost duopoly, there exists a CCE giving each player at least monopoly/(4e^2).

# Method

Maximize utility over the exact symmetric-CCE polytope used by the authors; include canonical demands and seeded adversarial monotone sequences.

## Durable evidence

All text artifacts are available under
`evidence/faithful/claim_1/`: contract, source audit, method, raw data,
verifier result, independent checker output, negative control, exact command,
limitations, and evaluation.

# Limitations and deviations

Finite LP certificates reproduce the theorem on the audited instances; they are not a substitute for the paper's universal proof.

This local verdict is not a prediction of the live judge score. Universal
theorems remain proof-backed; the finite certificates do not replace proofs.
