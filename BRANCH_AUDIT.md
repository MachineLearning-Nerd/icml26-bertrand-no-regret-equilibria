# Branch audit and naming policy

## Target policy

The target public branch set has one default branch and purpose-prefixed experiment branches:

- `main` — canonical publication surface and default branch
- `baseline/*` — immutable judged baselines
- `research/*` — source-faithful research implementations
- `release/*` — durable evidence releases

All approved commits are attributed to `MachineLearning-Nerd`. The legacy `master` and `orx/*` names are historical provenance only; they have been removed from the public remote.

## Mapping

| Final branch | Legacy source | Purpose |
| --- | --- | --- |
| `main` | `master` | Canonical publication surface |
| `baseline/judged-numpy-proxy` | `orx/baseline-judged-numpy-proxy` | Frozen judged baseline |
| `research/faithful-lp-claim-suite` | `orx/faithful-lp-claim-suite` | Source-faithful LP claim suite |
| `release/durable-evidence` | `orx/durable-evidence-release-candidate` | Durable evidence and published candidate |

## Migration checklist

Before publication, verify all of the following against the remote:

- default branch is `main`;
- exactly the four final branches above are public;
- no `master` or `orx/*` ref remains;
- every reachable commit on the final branches has `MachineLearning-Nerd` author and committer identity;
- README links and repository metadata use the target repository name.

## Verified migration

Verified on 2026-08-14 against
`MachineLearning-Nerd/icml26-bertrand-no-regret-equilibria`:

- the default branch is `main`;
- the public branch set contains exactly the four final branches in this file;
- no `master` or `orx/*` ref remains;
- all reachable commits on those final branches use
  `MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`;
- the repository description, homepage, README links, and gate metadata use the
  target repository identity.
