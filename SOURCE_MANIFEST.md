# Source and evidence manifest

## Paper identity

| Field | Value |
| --- | --- |
| Title | *Revisiting the Bertrand Paradox via Equilibrium Analysis of No-regret Learners* |
| Authors | Arnab Maiti; Junyan Liu; Kevin Jamieson; Lillian J. Ratliff |
| Venue | ICML 2026 |
| Authoritative source | [arXiv 2602.21620v2](https://arxiv.org/abs/2602.21620) |
| OpenReview identifier | `ZEP68RaUeR` |
| Audited PDF SHA-256 | `d8e4337c5c5910bf799d4b9ade203730b006dcdd9d77f32d8e0f3fc5732319a2` |
| Source-audit HTML SHA-256 | `6afd8846b3c183ec8ab86d7f8aa3ca0207b9ab3e8ffda0751b648d6f10a1a856` |
| HTML source retrieved | 2026-07-23 from ar5iv |

## Repository identity

- Original name: `icml26-repro-ZEP68RaUeR-bertrand-no-regret`
- Target name: `icml26-bertrand-no-regret-equilibria`
- Owner and commit attribution: `MachineLearning-Nerd`
- Default branch target: `main`

## Evidence locations

| Evidence | Location | Role |
| --- | --- | --- |
| Claim contracts and outputs | `evidence/faithful/claim_1/` through `claim_6/` | Canonical finite protocols, raw results, independent checks, controls, and limitations |
| Durable machine artifacts | `.openresearch/artifacts/claim_1/` through `claim_6/` | Machine-readable outputs used by the release |
| Cumulative release | `evidence/faithful/summary.json`, `evidence/faithful/EVAL.md` | Six-claim summary and runtime |
| Candidate validation | `release/old-new-subset-check.txt`, `release/upload-manifest.sha256` | Additive Space preservation and allowlisted publication |
| Judge state | `release/awaiting-judge.json` | Published revision, judged revision, and live score |
| Claim narrative | `reports/bertrand-reproduction/report.md` | Human-readable source audit and assessment |
| Reproduction notebook | `notebooks/bertrand_reproduction.py` | Self-contained explanation and executable entry point |
| Gate summary | `publication_gate.json` | Current scoped publication state |

The raw `VERIFIED` values in generated evidence mean that the declared finite contract passed. The repository-level status adds the scope qualifier and does not claim a universal proof replacement.
