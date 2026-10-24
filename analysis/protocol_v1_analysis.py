"""Test Protocol v1 — analysis pipeline.

Input: a CSV of logged samples with columns
    trial_id, condition, t_ms, pm10, flow_lpm
where condition is "baseline" (no suppression or continuous spray)
or "vdss" (closed-loop).

Output (printed + saved to outputs/):
    per-trial summary, then per-condition mean ± SD and 95% CI for
    mean PM10 and water used, plus the VDSS-vs-baseline deltas.

Usage:
    python protocol_v1_analysis.py data/raw/*.csv     # one or many files
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REQUIRED = {"trial_id", "condition", "t_ms", "pm10", "flow_lpm"}
OUT_DIR = Path(__file__).parent / "outputs"


def per_trial(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (trial, cond), g in df.sort_values("t_ms").groupby(["trial_id", "condition"]):
        t_min = g["t_ms"].to_numpy() / 60_000.0
        water_l = float(np.trapezoid(g["flow_lpm"].to_numpy(), t_min)) if len(g) > 1 else 0.0
        rows.append({
            "trial_id": trial,
            "condition": cond,
            "n_samples": len(g),
            "duration_s": (g["t_ms"].max() - g["t_ms"].min()) / 1000.0,
            "pm10_mean": g["pm10"].mean(),
            "water_l": water_l,
        })
    return pd.DataFrame(rows)


def ci95(x: pd.Series) -> tuple[float, float, float, float]:
    x = x.dropna()
    n = len(x)
    mean = x.mean()
    sd = x.std(ddof=1) if n > 1 else float("nan")
    if n < 2:
        return mean, sd, float("nan"), float("nan")
    half = stats.t.ppf(0.975, n - 1) * sd / np.sqrt(n)
    return mean, sd, mean - half, mean + half


def summarise(trials: pd.DataFrame) -> pd.DataFrame:
    out = []
    for cond, g in trials.groupby("condition"):
        for metric in ("pm10_mean", "water_l"):
            m, sd, lo, hi = ci95(g[metric])
            out.append({"condition": cond, "metric": metric, "n_trials": len(g),
                        "mean": m, "sd": sd, "ci95_lo": lo, "ci95_hi": hi})
    return pd.DataFrame(out)


def main(paths: list[str]) -> None:
    srcs = [Path(p) for p in paths]
    df = pd.concat([pd.read_csv(p) for p in srcs], ignore_index=True)
    stem = srcs[0].stem if len(srcs) == 1 else f"combined_{len(srcs)}_files"
    missing = REQUIRED - set(df.columns)
    if missing:
        sys.exit(f"Missing columns: {sorted(missing)}")

    if any("synthetic" in p.name.lower() for p in srcs):
        print("=" * 64)
        print("SYNTHETIC PIPELINE-TEST DATA — NOT A MEASUREMENT. DO NOT CITE.")
        print("=" * 64)

    trials = per_trial(df)
    summary = summarise(trials)

    pd.set_option("display.float_format", "{:.2f}".format)
    print("\nPer-trial:\n", trials.to_string(index=False))
    print("\nPer-condition (mean ± SD, 95% CI):\n", summary.to_string(index=False))

    piv = summary.pivot(index="metric", columns="condition", values="mean")
    if {"baseline", "vdss"} <= set(piv.columns):
        print("\nVDSS vs baseline:")
        for metric in piv.index:
            b, v = piv.loc[metric, "baseline"], piv.loc[metric, "vdss"]
            pct = (b - v) / b * 100 if b else float("nan")
            print(f"  {metric:10s} baseline={b:.2f}  vdss={v:.2f}  reduction={pct:.1f}%")

        b = trials.loc[trials.condition == "baseline", "pm10_mean"]
        v = trials.loc[trials.condition == "vdss", "pm10_mean"]
        if len(b) > 1 and len(v) > 1:
            t, p = stats.ttest_ind(b, v, equal_var=False)
            print(f"  Welch t-test on PM10: t={t:.2f}, p={p:.4f}")

    OUT_DIR.mkdir(exist_ok=True)
    trials.to_csv(OUT_DIR / f"{stem}_trials.csv", index=False)
    summary.to_csv(OUT_DIR / f"{stem}_summary.csv", index=False)
    print(f"\nSaved to {OUT_DIR}/")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
