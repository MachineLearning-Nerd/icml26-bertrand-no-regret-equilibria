# Claim 6 — faithful finite-game verifier

## Verdict

**VERIFIED** under the explicit finite claim contract.

```json
{
  "curves": 12,
  "endpoints_within_0.03": 12,
  "verdict": "VERIFIED",
  "worst_endpoint_error": 0.022890955145419944
}
```

# Source audit

Source: https://ar5iv.labs.arxiv.org/html/2602.21620

Retrieved: 2026-07-23

SHA-256: `6afd8846b3c183ec8ab86d7f8aa3ca0207b9ab3e8ffda0751b648d6f10a1a856`

Anchor: #S3.SS1

Exact scope and quantifiers: Section 3.1 reports that the maximum player utility over symmetric CCEs, normalized by monopoly utility, approaches roughly 1/e as k=10..100 grows across standard demands and costs.

# Method

Run the authors' exact symmetric-CCE LP objective for every integer k=10..100, four demand definitions, and costs 0, 0.5, 0.9.

## Durable evidence

All text artifacts are available under
`evidence/faithful/claim_6/`: contract, source audit, method, raw data,
verifier result, independent checker output, negative control, exact command,
limitations, and evaluation.

# Limitations and deviations

'Roughly' has no paper-specified tolerance; both raw errors and the explicit preregistered 0.03/0.05 rule are reported.

This local verdict is not a prediction of the live judge score. Universal
theorems remain proof-backed; the finite certificates do not replace proofs.
