"""E3 analysis — does source data help, over all 12 directed pairs of the 4 NetFlow v3 datasets?

Reads results/e2_runs_all.csv (from `e2_transfer.py --datasets cic unsw ton bot --out all`).
For every (pair, model, method, k>=1): paired two-sided Wilcoxon over the 10 seeds of
F1(method) - F1(target-only). Verdict: help / hurt if p < 0.05, else no difference; also Holm-corrected
over all comparisons. Also reports zero-shot (k=0) F1, recall and FPR per pair.

    python src/e3_analysis.py
    python src/e3_analysis.py --tag shared    # reads e2_runs_all_shared.csv, writes e3_*_shared.*

Writes results/e3_significance.csv, results/e3_zeroshot.csv, results/e3_heatmap.png
"""
from __future__ import annotations
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from common import RES

ALPHA = 0.05
METHODS, MODELS = ["pooled", "iw", "finetune"], ["RF", "GBT", "MLP"]


def holm(p):
    order = np.argsort(p)
    adj = np.empty(len(p))
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (len(p) - rank) * p[i])
        adj[i] = min(1.0, running)
    return adj


def compare(runs):
    base = runs[runs.method == "target-only"].set_index(["direction", "model", "k", "seed"])["f1"]
    rows = []
    for (d, mdl, meth, k), g in runs[(runs.k > 0) & runs.method.isin(METHODS)].groupby(
            ["direction", "model", "method", "k"]):
        diff = g.set_index("seed")["f1"] - base.loc[(d, mdl, k)]
        p = 1.0 if np.allclose(diff, 0) else wilcoxon(diff).pvalue
        rows.append({"direction": d, "model": mdl, "method": meth, "k": k,
                     "delta_f1": diff.mean(), "p": p})
    sig = pd.DataFrame(rows)
    sig["p_holm"] = holm(sig.p.to_numpy())
    for col, pc in (("verdict", "p"), ("verdict_holm", "p_holm")):
        sig[col] = np.where(sig[pc] >= ALPHA, "no diff", np.where(sig.delta_f1 > 0, "help", "hurt"))
    return sig


def heatmap(sig, path):
    # one cell per (pair, model x method): net count over k of help (+1) / hurt (-1)
    score = sig.assign(s=sig.verdict.map({"help": 1, "hurt": -1, "no diff": 0}))
    table = score.pivot_table(index="direction", columns=["model", "method"], values="s", aggfunc="sum")
    table = table.reindex(columns=pd.MultiIndex.from_product([MODELS, METHODS]))
    nk = sig.k.nunique()
    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(table.to_numpy(), cmap="RdBu", vmin=-nk, vmax=nk, aspect="auto")
    ax.set_xticks(range(table.shape[1]), [f"{m}\n{t}" for m, t in table.columns], fontsize=8)
    ax.set_yticks(range(table.shape[0]), table.index)
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            ax.text(j, i, int(table.iat[i, j]), ha="center", va="center", fontsize=8)
    fig.colorbar(im, label=f"#k where source helps − #k where it hurts (of {nk}, Wilcoxon p<{ALPHA})")
    ax.set_title("Source data vs target-only, F1, 12 directed pairs (blue = source helps, red = hurts)")
    plt.tight_layout(); plt.savefig(path, dpi=120); plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="", help="'shared' -> e2_runs_all_shared.csv, e3_*_shared.*")
    tag = ap.parse_args().tag
    t = f"_{tag}" if tag else ""
    runs = pd.read_csv(RES / f"e2_runs_all{t}.csv")
    sig = compare(runs)
    sig.to_csv(RES / f"e3_significance{t}.csv", index=False)
    heatmap(sig, RES / f"e3_heatmap{t}.png")

    zs = (runs[(runs.k == 0) & (runs.method == "pooled")]
          .groupby(["direction", "model"])[["f1", "recall", "fpr"]].mean().round(3))
    zs.to_csv(RES / f"e3_zeroshot{t}.csv")

    print(f"{len(sig)} comparisons (source method vs target-only, paired Wilcoxon over 10 seeds)\n")
    for col in ("verdict", "verdict_holm"):
        print(col, sig[col].value_counts().to_dict())
    print("\nby method:\n", pd.crosstab(sig.method, sig.verdict).to_string())
    print("\nby model:\n", pd.crosstab(sig.model, sig.verdict).to_string())
    print("\nby k:\n", pd.crosstab(sig.k, sig.verdict).to_string())
    print("\nby pair:\n", pd.crosstab(sig.direction, sig.verdict).to_string())
    print("\nlargest helps:\n", sig[sig.verdict == "help"].nlargest(10, "delta_f1").round(4).to_string())
    print("\nzero-shot (k=0, source-only) mean over seeds:\n", zs.to_string())
    print(f"\nwrote {RES}/e3_significance{t}.csv, e3_zeroshot{t}.csv, e3_heatmap{t}.png")


if __name__ == "__main__":
    main()
