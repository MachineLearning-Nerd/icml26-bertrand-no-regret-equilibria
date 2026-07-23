# Publication status — awaiting judge

Paper: *Revisiting the Bertrand Paradox via Equilibrium Analysis of No-regret
Learners* (`arXiv:2602.21620`, OpenReview `ZEP68RaUeR`).

- Current live judge score: **4/12**
- Judged Space revision: `48d0b6f9269cadf6ae6894187ee0b4e2c34be70c`
- Published candidate revision: `9aac9487ad799104d583ba1d63c8184b9ad7085e`
- State: **AWAITING JUDGE REEVALUATION**
- Winning experiment branch:
  `orx/durable-evidence-release-candidate`
- Winning experiment SHA:
  `3931ca85eb7fe7f3a9b405e297eba1d57e3e799e`

The fixed cumulative command is:

```bash
uv sync --frozen && uv run --frozen python repro/src/verify_bertrand.py
```

The final local-CPU run returned `VERIFIED` for all six explicit finite claim
contracts. These local verdicts are not a claimed judge-score increase.
