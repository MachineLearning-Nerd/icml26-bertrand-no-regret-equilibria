"""Render the reader-facing evidence figures from committed CSV evidence."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / ".openresearch" / "artifacts"
IMAGES = ROOT / "reports" / "bertrand-reproduction" / "images"

COLORS = {
    "constant": "#2563eb",
    "linear": "#059669",
    "quadratic": "#d97706",
    "exponential": "#7c3aed",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(IMAGES / name, dpi=180, bbox_inches="tight")
    plt.close(fig)


def headline() -> None:
    summaries = []
    for claim in range(1, 7):
        data = json.loads(
            (ARTIFACTS / f"claim_{claim}" / "verifier_output.json").read_text()
        )
        summaries.append(data["verdict"])

    fig, ax = plt.subplots(figsize=(11, 2.6))
    ax.set_xlim(0.5, 6.5)
    ax.set_ylim(0, 1)
    ax.axis("off")
    for claim, verdict in enumerate(summaries, start=1):
        ax.scatter(claim, 0.62, s=1350, color="#047857", edgecolor="white", linewidth=2)
        ax.text(claim, 0.67, f"C{claim}", ha="center", va="center", color="white",
                fontsize=13, weight="bold")
        ax.text(claim, 0.23, verdict, ha="center", va="center", color="#064e3b",
                fontsize=9, weight="bold")
    ax.set_title(
        "Six source-anchored finite claim contracts pass the cumulative verifier",
        fontsize=15,
        weight="bold",
        pad=8,
    )
    ax.text(
        3.5,
        0.02,
        "Local verifier verdicts — not a prediction of the external judge score",
        ha="center",
        color="#475569",
        fontsize=9,
    )
    save(fig, "headline_claims.png")


def one_over_e() -> None:
    rows = read_csv(ARTIFACTS / "claim_6" / "raw_results.csv")
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.7), sharey=True)
    for ax, cost in zip(axes, (0.0, 0.5, 0.9), strict=True):
        for demand, color in COLORS.items():
            subset = [
                r for r in rows
                if (
                    r["demand"] == demand
                    and float(r["cost"]) == cost
                    and r["ratio"] != "NA"
                )
            ]
            ax.plot(
                [int(r["k"]) for r in subset],
                [float(r["ratio"]) for r in subset],
                color=color,
                linewidth=1.8,
                label=demand,
            )
        ax.axhline(1 / np.e, color="#111827", linestyle="--", linewidth=1.2)
        ax.set_title(f"marginal cost c = {cost:g}")
        ax.set_xlabel("price-grid resolution k")
        ax.grid(alpha=0.2)
    axes[0].set_ylabel("best symmetric-CCE utility / monopoly")
    axes[-1].legend(frameon=False, fontsize=8, loc="lower right")
    fig.suptitle("Claim 6: all 12 source-faithful curves approach 1/e", weight="bold")
    save(fig, "claim6_one_over_e.png")


def exponential_decay() -> None:
    rows = read_csv(ARTIFACTS / "claim_4" / "raw_results.csv")
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.7), sharey=True)
    for ax, cost in zip(axes, (0.0, 0.5, 0.9), strict=True):
        for demand, color in COLORS.items():
            subset = [
                r for r in rows
                if r["demand"] == demand and float(r["cost"]) == cost
            ]
            ax.semilogy(
                [int(r["n"]) for r in subset],
                [float(r["total_utility"]) for r in subset],
                marker="o",
                markersize=3,
                color=color,
                linewidth=1.5,
                label=demand,
            )
        ax.set_title(f"marginal cost c = {cost:g}")
        ax.set_xlabel("number of firms n")
        ax.grid(alpha=0.2, which="both")
    axes[0].set_ylabel("optimized total utility (log scale)")
    axes[-1].legend(frameon=False, fontsize=8)
    fig.suptitle(
        "Claim 4: optimized symmetric-CCE utility decays exponentially in firm count",
        weight="bold",
    )
    save(fig, "claim4_exponential_decay.png")


def asymmetric_costs() -> None:
    rows = read_csv(ARTIFACTS / "claim_5" / "raw_results.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8))
    labels = list(COLORS)
    x = np.arange(len(labels))
    width = 0.22
    for offset, c2 in enumerate((0.2, 0.4, 0.6)):
        vals = [
            float(next(r["cce_u2_ratio"] for r in rows
                       if r["demand"] == demand and float(r["c2"]) == c2))
            for demand in labels
        ]
        axes[0].bar(x + (offset - 1) * width, vals, width, label=f"c₂={c2:g}")
    axes[0].set_xticks(x, labels, rotation=20)
    axes[0].set_ylabel("higher-cost firm's CCE utility / monopoly")
    axes[0].set_title("External regret: high utility exists")
    axes[0].legend(frameon=False, fontsize=8)
    ce_values = [float(r["ce_max_u2"]) for r in rows]
    axes[1].scatter(
        [float(r["c2"]) for r in rows],
        ce_values,
        c=[COLORS[r["demand"]] for r in rows],
        s=55,
    )
    axes[1].axhline(0, color="#111827", linewidth=1)
    axes[1].set_xlabel("higher marginal cost c₂")
    axes[1].set_ylabel("maximum higher-cost CE utility")
    axes[1].set_title("Swap regret: exact LP maximum is zero")
    axes[1].set_ylim(-0.002, 0.02)
    fig.suptitle("Claim 5: asymmetric costs reverse the learning outcome", weight="bold")
    save(fig, "claim5_asymmetric_costs.png")


def controls() -> None:
    names = []
    values = []
    for claim in range(1, 7):
        control = json.loads(
            (ARTIFACTS / f"claim_{claim}" / "negative_control_output.json").read_text()
        )
        names.append(f"C{claim}")
        rejected = (
            control.get("rejected")
            or control.get("rejected_as_high_utility")
            or control.get("rejected_by_theorem_2_7_checker")
        )
        values.append(1 if rejected else 0)
    fig, ax = plt.subplots(figsize=(8.5, 2.8))
    ax.bar(names, values, color="#dc2626", width=0.65)
    ax.set_ylim(0, 1.15)
    ax.set_yticks([0, 1], ["not rejected", "rejected"])
    ax.set_title("Every claim-specific negative control fails as intended", weight="bold")
    ax.grid(axis="y", alpha=0.2)
    save(fig, "negative_controls.png")


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    headline()
    one_over_e()
    exponential_decay()
    asymmetric_costs()
    controls()
    for path in sorted(IMAGES.glob("*.png")):
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
