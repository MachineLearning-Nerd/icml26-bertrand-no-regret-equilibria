# Claim 3 — faithful finite-game verifier

## Verdict

**VERIFIED** under the explicit finite claim contract.

```json
{
  "instances": 3,
  "k_independent_lower_envelope": 0.16930595471632093,
  "verdict": "VERIFIED"
}
```

# Source audit

Source: https://ar5iv.labs.arxiv.org/html/2602.21620

Retrieved: 2026-07-23

SHA-256: `6afd8846b3c183ec8ab86d7f8aa3ca0207b9ab3e8ffda0751b648d6f10a1a856`

Anchor: #S2.Thmtheorem3.1.1.1

Exact scope and quantifiers: For constant demand and c<1 with 1-c constant in k, there exists a Phi-equilibrium where player 1 has swap constraints, player 2 external constraints, and both obtain a k-independent positive fraction of monopoly utility.

# Method

Solve the full mixed equilibrium LP, maximizing the smaller normalized player utility; independently enumerate every deviation.

## Durable evidence

All text artifacts are available under
`evidence/faithful/claim_3/`: contract, source audit, method, raw data,
verifier result, independent checker output, negative control, exact command,
limitations, and evaluation.

# Limitations and deviations

The theorem's proof constant is not numerically specified. The observed lower envelope is reported without replacing it by an arbitrary threshold.

This local verdict is not a prediction of the live judge score. Universal
theorems remain proof-backed; the finite certificates do not replace proofs.
