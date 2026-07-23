import marimo

__generated_with = "0.23.14"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Bertrand competition after regret minimization

    **Reproduction evidence first.** The fixed local-CPU verifier returned
    `VERIFIED` for all six finite claim contracts:

    | Claim | Decisive observed quantity | Verdict |
    |---|---:|---|
    | 1 — high-utility CCE | minimum ratio 0.285299 vs 0.033834 floor | VERIFIED |
    | 2 — swap-regret bound | maximum bound excess 0 | VERIFIED |
    | 3 — mixed learners | lower envelope 0.169306 | VERIFIED |
    | 4 — many firms | all 12 slopes negative; worst R² 0.8283 | VERIFIED |
    | 5 — asymmetric costs | CCE ≥0.314040; CE high-cost maximum 0 | VERIFIED |
    | 6 — 1/e phenomenon | 12/12 endpoints within 0.03 | VERIFIED |

    These are local computational verdicts, not a prediction of the external
    judge score. The live score remains 4/12 until a published candidate is
    independently evaluated.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Why regret type changes prices

    A coarse correlated equilibrium (CCE) blocks only deviations to one
    fixed price—the equilibrium object produced by vanishing external
    regret. A correlated equilibrium (CE) blocks every action-to-action
    remapping—the stronger object associated with vanishing swap regret.

    \[
    \text{swap regret constraints} \supset
    \text{external regret constraints}
    \quad\Longrightarrow\quad
    \mathrm{CE}\subseteq\mathrm{CCE}.
    \]

    The reproduction constructs these polytopes explicitly. It then
    maximizes the utility relevant to each theorem and independently
    recomputes every deviation residual from the returned distribution.
    """)
    return


@app.cell
def _():
    endpoint_rows = {
        0.0: {
            "constant": 0.3678657424,
            "linear": 0.3676391026,
            "quadratic": 0.3678176140,
            "exponential": 0.3677910652,
        },
        0.5: {
            "constant": 0.3677990300,
            "linear": 0.3667174627,
            "quadratic": 0.3670709634,
            "exponential": 0.3678028045,
        },
        0.9: {
            "constant": 0.3662790698,
            "linear": 0.3456000000,
            "quadratic": 0.3449884860,
            "exponential": 0.3676671103,
        },
    }
    target = 0.3678794412
    return endpoint_rows, target


@app.cell
def _(mo):
    cost = mo.ui.dropdown(
        options={"c = 0": 0.0, "c = 0.5": 0.5, "c = 0.9": 0.9},
        value="c = 0",
        label="Marginal cost",
    )
    cost
    return (cost,)


@app.cell
def _(cost, endpoint_rows, mo, target):
    selected = endpoint_rows[cost.value]
    lines = "\n".join(
        f"| {name} | {value:.6f} | {abs(value - target):.6f} |"
        for name, value in selected.items()
    )
    mo.md(
        f"""
        ## Explore the 1/e endpoints

        At grid resolution `k=100`, the paper compares the best symmetric-CCE
        utility with `1/e = {target:.6f}`.

        | Demand | Observed ratio | Absolute error |
        |---|---:|---:|
        {lines}

        The source quadratic demand is **1 − x²**. The legacy reproduction used
        **(1 − x)²**, which is a different game.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## The asymmetric-cost mechanism

    With the low-cost firm fixed at \(c_1=0\), four demand families and
    \(c_2\in\{0.2,0.4,0.6\}\) give:

    * external-regret / CCE: the high-cost firm's smallest normalized
      utility is **0.314040**;
    * swap-regret / CE: its largest possible utility is **exactly zero**.

    Weakening the CE constraints to CCE is the negative control. Positive
    high-cost utility returns, so the checker rejects it. This is the
    missing distinction between Theorems 2.6 and 2.7 in the previous
    logbook.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Reproduce locally

    The formal command is fixed across the experiment tree:

    ```bash
    uv sync --frozen && uv run --frozen python repro/src/verify_bertrand.py
    ```

    It writes raw CSVs, contracts, source audits, independent checker
    outputs, negative controls, environment metadata, and verdicts beneath
    `.openresearch/artifacts/`. The recorded scientific computation took
    13.39 seconds on an 8-thread Apple ARM CPU. No GPU was used.

    The finite certificates align with all six audited consequences, but
    they do not replace the paper's universal proofs.
    """)
    return


if __name__ == "__main__":
    app.run()
