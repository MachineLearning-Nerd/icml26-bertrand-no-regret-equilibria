# Claim 5 — faithful finite-game verifier

## Verdict

**VERIFIED** under the explicit finite claim contract.

```json
{
  "maximum_high_cost_ce_utility": 0.0,
  "minimum_cce_normalized_utility": 0.3140403806292739,
  "verdict": "VERIFIED"
}
```

# Source audit

Source: https://ar5iv.labs.arxiv.org/html/2602.21620

Retrieved: 2026-07-23

SHA-256: `6afd8846b3c183ec8ab86d7f8aa3ca0207b9ab3e8ffda0751b648d6f10a1a856`

Anchor: #S2.Thmtheorem6.1.1.1, #S2.Thmtheorem7.1.1.1, #A2.Thmtheorem2

Exact scope and quantifiers: Under asymmetric costs, Theorem 2.6 gives high-utility CCEs under its stated demand conditions, while Theorem 2.7 gives exactly zero higher-cost utility in every CE when c2-c1>1/k.

# Method

Solve general asymmetric CCE max-min LPs and, separately, maximize the high-cost player's utility over the full CE polytope.

## Durable evidence

All text artifacts are available under
`evidence/faithful/claim_5/`: contract, source audit, method, raw data,
verifier result, independent checker output, negative control, exact command,
limitations, and evaluation.

# Limitations and deviations

Theorem 2.6 is conditional; each reported canonical case is audited numerically rather than generalized to every demand.

This local verdict is not a prediction of the live judge score. Universal
theorems remain proof-backed; the finite certificates do not replace proofs.
