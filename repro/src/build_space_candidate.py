"""Build an additive, text-only Hugging Face Space release candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / ".openresearch" / "artifacts"
TEXT_SUFFIXES = {
    ".md",
    ".json",
    ".csv",
    ".txt",
    ".py",
    ".toml",
    ".lock",
    ".sha256",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def claim_page(claim: int) -> str:
    result = json.loads(
        (ARTIFACTS / f"claim_{claim}" / "verifier_output.json").read_text()
    )
    method = (ARTIFACTS / f"claim_{claim}" / "method.md").read_text().strip()
    audit = (ARTIFACTS / f"claim_{claim}" / "source_audit.md").read_text().strip()
    limitations = (
        ARTIFACTS / f"claim_{claim}" / "limitations.md"
    ).read_text().strip()
    formatted = json.dumps(result, indent=2)
    return f"""# Claim {claim} — faithful finite-game verifier

## Verdict

**{result["verdict"]}** under the explicit finite claim contract.

```json
{formatted}
```

{audit}

{method}

## Durable evidence

All text artifacts are available under
`evidence/faithful/claim_{claim}/`: contract, source audit, method, raw data,
verifier result, independent checker output, negative control, exact command,
limitations, and evaluation.

{limitations}

This local verdict is not a prediction of the live judge score. Universal
theorems remain proof-backed; the finite certificates do not replace proofs.
"""


def release_page() -> str:
    return """# Faithful cumulative release candidate

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
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protected", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    protected = args.protected.resolve()
    output = args.output.resolve()

    if not (protected / "logbook.json").exists():
        raise SystemExit("protected source does not contain logbook.json")
    if output.exists():
        raise SystemExit(f"refusing to overwrite existing candidate: {output}")

    shutil.copytree(protected, output, ignore=shutil.ignore_patterns(".git"))
    output.chmod(0o755)
    for path in output.rglob("*"):
        if path.is_dir():
            path.chmod(0o755)
    for path in output.rglob("*"):
        if path.is_file():
            path.chmod(0o644)

    old_logbook = json.loads((protected / "logbook.json").read_text())
    new_logbook = json.loads(json.dumps(old_logbook))
    new_entries = []
    for claim in range(1, 7):
        relative = f"pages/faithful-claim-{claim}/page.md"
        write(output / relative, claim_page(claim))
        new_entries.append(
            {
                "slug": f"faithful-claim-{claim}",
                "title": f"Faithful claim {claim}",
                "file": relative,
                "children": [],
            }
        )
    release_relative = "pages/faithful-release/page.md"
    write(output / release_relative, release_page())
    new_entries.append(
        {
            "slug": "faithful-release",
            "title": "Faithful cumulative release",
            "file": release_relative,
            "children": [],
        }
    )
    new_logbook["root"]["children"].extend(new_entries)
    new_logbook["updated_at"] = datetime.now(UTC).isoformat()
    write(output / "logbook.json", json.dumps(new_logbook, indent=2) + "\n")

    additions: list[Path] = [output / "logbook.json"]
    for claim in range(1, 7):
        source = ARTIFACTS / f"claim_{claim}"
        destination = output / "evidence" / "faithful" / f"claim_{claim}"
        destination.mkdir(parents=True)
        for path in sorted(source.iterdir()):
            if path.is_file() and path.suffix in TEXT_SUFFIXES:
                target = destination / path.name
                shutil.copy2(path, target)
                additions.append(target)
        additions.append(output / f"pages/faithful-claim-{claim}/page.md")

    root_evidence = output / "evidence" / "faithful"
    for name in ("EVAL.md", "environment.json", "summary.json", "manifest.sha256"):
        target = root_evidence / name
        shutil.copy2(ARTIFACTS / name, target)
        additions.append(target)

    faithful_source = output / "repro" / "faithful"
    faithful_source.mkdir(parents=True)
    for name in ("equilibria.py", "verify_bertrand.py"):
        target = faithful_source / name
        shutil.copy2(ROOT / "repro" / "src" / name, target)
        additions.append(target)
    for name in ("pyproject.toml", "uv.lock", ".python-version"):
        target = output / "evidence" / "faithful" / "environment" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
        additions.append(target)
    additions.append(output / release_relative)

    protected_copy = output / "evidence" / "protected" / "judged-logbook.json"
    protected_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(protected / "logbook.json", protected_copy)
    additions.append(protected_copy)

    old_paths = sorted(
        p.relative_to(protected)
        for p in protected.rglob("*")
        if p.is_file() and ".git" not in p.parts
    )
    missing = [str(p) for p in old_paths if not (output / p).exists()]
    hash_changes = [
        str(p)
        for p in old_paths
        if (output / p).exists() and digest(protected / p) != digest(output / p)
    ]
    old_children = old_logbook["root"]["children"]
    new_children_prefix = new_logbook["root"]["children"][: len(old_children)]
    semantic_nav_preserved = old_children == new_children_prefix
    if missing or hash_changes != ["logbook.json"] or not semantic_nav_preserved:
        raise SystemExit(
            f"subset gate failed: missing={missing}, changed={hash_changes}, "
            f"nav={semantic_nav_preserved}"
        )

    subset_text = f"""PROTECTED_SPACE_REVISION 48d0b6f9269cadf6ae6894187ee0b4e2c34be70c
OLD_FILE_COUNT {len(old_paths)}
OLD_PATHS_PRESENT {len(old_paths)}
MISSING_OLD_PATHS 0
BYTE_IDENTICAL_OLD_FILES {len(old_paths) - 1}
EXPECTED_MODIFIED_OLD_FILE logbook.json
OLD_NAVIGATION_PREFIX_PRESERVED {str(semantic_nav_preserved).lower()}
PROTECTED_LOGBOOK_COPY evidence/protected/judged-logbook.json
RESULT PASS
"""
    subset_path = output / "release" / "old-new-subset-check.txt"
    write(subset_path, subset_text)
    additions.append(subset_path)

    unique_additions = sorted(set(additions), key=lambda p: str(p.relative_to(output)))
    non_text = [
        str(path.relative_to(output))
        for path in unique_additions
        if path.suffix not in TEXT_SUFFIXES and path.name != ".python-version"
    ]
    if non_text:
        raise SystemExit(f"non-text file in upload allowlist: {non_text}")
    allowlist = output / "release" / "upload-allowlist.txt"
    write(
        allowlist,
        "\n".join(str(path.relative_to(output)) for path in unique_additions) + "\n",
    )
    manifest = output / "release" / "upload-manifest.sha256"
    write(
        manifest,
        "\n".join(
            f"{digest(path)}  {path.stat().st_size}  {path.relative_to(output)}"
            for path in unique_additions
        )
        + "\n",
    )
    print(subset_text, end="")
    print(f"UPLOAD_ALLOWLIST_COUNT {len(unique_additions)}")
    print(f"CANDIDATE {output}")


if __name__ == "__main__":
    main()
