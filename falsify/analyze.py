"""Analyze an experiment's trials: per-cell metrics, bootstrap interaction, plot.

Usage: uv run python -m falsify.analyze exp001_pilot
Writes results/<exp>.json and results/<exp>_wasted.png. Reports only measured fields.
"""
import json
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

METRICS = ["wasted_actions", "a_actions", "hold_actions", "switched", "rounds_to_switch",
           "success", "post_tokens_in", "post_tokens_out", "llm_calls", "disagreement_rounds"]


def load(exp: str) -> tuple[pd.DataFrame, int]:
    rows, invalid = [], 0
    for line in (pathlib.Path("data/trials") / f"{exp}.jsonl").read_text().splitlines():
        t = json.loads(line)
        if not t["valid"]:
            invalid += 1
            continue
        rows.append({"trial_id": t["trial_id"], "cell": t["cell"], "org": t["org"], "k": t["k"],
                     "update": t["update"], "auditor": t.get("auditor", False), "seed": t["seed"],
                     **{m: t["measured"][m] for m in METRICS}})
    return pd.DataFrame(rows), invalid


def boot_interaction(df: pd.DataFrame, cells: dict, n: int = 10000, seed: int = 0) -> dict:
    """Δ = (hi_multi − lo_multi) − (hi_single − lo_single) on wasted_actions, with 95% CI."""
    rng = np.random.default_rng(seed)
    vals = {name: df[df.cell == c].wasted_actions.to_numpy(float) for name, c in cells.items()}
    if any(len(v) == 0 for v in vals.values()):
        return {"error": "missing cell"}

    def delta(v):
        return (v["D"].mean() - v["C"].mean()) - (v["B"].mean() - v["A"].mean())

    point = delta(vals)
    draws = np.array([delta({k: rng.choice(v, len(v)) for k, v in vals.items()}) for _ in range(n)])
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return {"delta": round(point, 3), "ci95": [round(lo, 3), round(hi, 3)], "n_boot": n,
            "n_per_cell": {k: len(v) for k, v in vals.items()}}


def main(exp: str) -> None:
    df, invalid = load(exp)
    total = len(df) + invalid
    per_cell = (df.groupby(["cell", "org", "k", "update", "auditor"])[METRICS]
                .agg(["mean", "std", "count"]).round(3))
    summary = {}
    for (cell, org, k, upd, aud), row in per_cell.iterrows():
        summary[cell] = {"org": org, "k": int(k), "update": upd, "auditor": bool(aud),
                         "n": int(row[("wasted_actions", "count")]),
                         **{m: {"mean": row[(m, "mean")], "sd": row[(m, "std")]} for m in METRICS}}
    result = {"experiment_id": exp, "n_trials": total, "n_invalid": invalid,
              "parse_failure_rate": round(invalid / total, 3) if total else None, "cells": summary}
    inv = df[df.update == "invalidating"]
    if set("ABCD") <= set(inv.cell):
        result["H1_interaction_wasted"] = boot_interaction(inv, {c: c for c in "ABCD"})
    out = pathlib.Path("results"); out.mkdir(exist_ok=True)
    (out / f"{exp}.json").write_text(json.dumps(result, indent=2, default=float))

    # plot: wasted actions per cell, individual trials jittered over the mean
    order = [c for c in ["A", "B", "C", "D", "A0", "B0", "C0", "D0"] if c in set(df.cell)]
    fig, ax = plt.subplots(figsize=(8, 4))
    rng = np.random.default_rng(1)
    for i, c in enumerate(order):
        v = df[df.cell == c].wasted_actions.to_numpy(float)
        ax.scatter(i + rng.uniform(-0.15, 0.15, len(v)), v, s=18, alpha=0.6, color="#0E5E6F")
        ax.hlines(v.mean(), i - 0.3, i + 0.3, color="#C9601B", lw=2)
    labels = [f"{c}\n{summary[c]['org']} k={summary[c]['k']}\n{summary[c]['update'][:5]}" for c in order]
    ax.set_xticks(range(len(order)), labels, fontsize=8)
    ax.set_ylabel("wasted actions after update")
    ax.set_title(f"{exp}: wasted actions by cell (orange = mean; n={len(df)} valid)")
    fig.tight_layout(); fig.savefig(out / f"{exp}_wasted.png", dpi=150)

    print(json.dumps({k: v for k, v in result.items() if k != "cells"}, indent=2, default=float))
    print(df.groupby("cell")[["wasted_actions", "a_actions", "hold_actions", "switched",
                              "success", "disagreement_rounds", "llm_calls"]].mean().round(2))


if __name__ == "__main__":
    main(sys.argv[1])
