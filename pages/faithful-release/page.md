# Faithful cumulative release candidate

## What changed

The candidate preserves every file from judged Space revision
`48d0b6f9269cadf6ae6894187ee0b4e2c34be70c` and adds transparent CCE, CE, and
mixed-Phi linear programs with six claim contracts. The old logbook pages are
unchanged and remain in the navigation.

The source quadratic demand is `1-x^2`, not the legacy `(1-x)^2`. Section 3.1
maximizes symmetric-CCE utility; it is not a multiplicative-weights trajectory.

## Cumulative local result

| Claim | Verdict | Decisive quantity |
|---|---|---|
| 1 | VERIFIED | minimum ratio 0.285299 vs 0.033834 floor |
| 2 | VERIFIED | maximum CE-bound excess 0 |
| 3 | VERIFIED | mixed-equilibrium lower envelope 0.169306 |
| 4 | VERIFIED | all 12 decay slopes negative; worst R2 0.8283 |
| 5 | VERIFIED | CCE minimum 0.314040; high-cost CE maximum 0 |
| 6 | VERIFIED | 12/12 k=100 endpoints within 0.03 of 1/e |

The fixed command is:

```bash
uv sync --frozen && uv run --frozen python repro/src/verify_bertrand.py
```

No GPU or paid Hugging Face compute was used. The live judged score remains
4/12 until this candidate is approved, published, and independently evaluated.
