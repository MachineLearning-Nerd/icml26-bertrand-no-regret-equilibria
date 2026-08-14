# Audit status

## Current assessment

- Overall: `VERIFIED_SCOPED`
- Evidence-release gate: `PASSED`
- Strict paper-level gate: `NOT_READY`
- Claims: 6/6 finite contracts pass; 0 falsified; 0 blocked
- Attribution target: `MachineLearning-Nerd`

The six results are finite LP or numerical contracts over declared price grids,
demand families, costs, and firm counts. They do not replace the paper's
universal proofs or constitute a predicted judge-score increase.

## Source and release

- Paper: *Revisiting the Bertrand Paradox via Equilibrium Analysis of No-regret Learners*
- Authors: Arnab Maiti, Junyan Liu, Kevin Jamieson, and Lillian J. Ratliff
- Source: [arXiv 2602.21620v2](https://arxiv.org/abs/2602.21620)
- OpenReview identifier: `ZEP68RaUeR`
- Audited PDF SHA-256: `d8e4337c5c5910bf799d4b9ade203730b006dcdd9d77f32d8e0f3fc5732319a2`
- Published candidate revision: `9aac9487ad799104d583ba1d63c8184b9ad7085e`
- Judged Space revision: `48d0b6f9269cadf6ae6894187ee0b4e2c34be70c`
- Current live judge score: `4/12`; no increase is claimed

The canonical machine-readable record is [`publication_gate.json`](publication_gate.json).
The detailed evidence release is under [`evidence/faithful/`](evidence/faithful/),
and the claim narrative is [`reports/bertrand-reproduction/report.md`](reports/bertrand-reproduction/report.md).

## Reproduce

```bash
uv sync --frozen && uv run --frozen python repro/src/verify_bertrand.py
```
