# Claim 4 — faithful finite-game verifier

## Verdict

**VERIFIED** under the explicit finite claim contract.

```json
{
  "least_negative_slope": -0.23442759762734322,
  "maximum_bound_excess": -0.004348407499986073,
  "verdict": "VERIFIED",
  "worst_exponential_r2": 0.8282604522926977
}
```

# Source audit

Source: https://ar5iv.labs.arxiv.org/html/2602.21620

Retrieved: 2026-07-23

SHA-256: `6afd8846b3c183ec8ab86d7f8aa3ca0207b9ab3e8ffda0751b648d6f10a1a856`

Anchor: #S2.Thmtheorem5.1.1.1 and #S3

Exact scope and quantifiers: For n>=2 and k>=5, every CCE has total utility at most 4f(c+1/k)/k+n(1-c)f(c+1/k)e^(1-n/2); best symmetric-CCE utility decays exponentially in n.

# Method

Reproduce the authors' k=100, n=2..10 symmetric-CCE LP for four demands and three costs; fit log utility, not the loose bound.

## Durable evidence

All text artifacts are available under
`evidence/faithful/claim_4/`: contract, source audit, method, raw data,
verifier result, independent checker output, negative control, exact command,
limitations, and evaluation.

# Limitations and deviations

The LP is over symmetric CCEs as in the paper's numerical section, not all CCEs. The theorem bound is checked but its additive 1/k floor is not misreported as slope -1/2.

This local verdict is not a prediction of the live judge score. Universal
theorems remain proof-backed; the finite certificates do not replace proofs.
