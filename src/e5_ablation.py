"""E5 follow-up — is source/target separability one artifact column, or deep?

E5-B showed a domain classifier separates every pair of datasets with AUC ~ 1.0, even within benign
traffic and within a shared attack category. A reviewer will ask whether that is one or two odd
columns (e.g. TTL). Greedy backward elimination answers it: fit the domain classifier, drop the
feature it relies on most (permutation importance on a held-out split), refit, repeat. Record the
held-out AUC after every removal and count how many features must go before the domains become
hard to tell apart.

Representation as E5-B: source = stratified 100k sample, target = unlabeled pool (50% split).
Run both raw and per-domain z-scored: z-scoring each domain with its own statistics maps the same
categorical code (e.g. PROTOCOL = 6) to a different value per domain, which by itself makes such
columns near-perfectly separable (cic-unsw PROTOCOL: raw AUC 0.57, z-scored 1.00). Raw answers
"do the networks differ"; z-scored is what the E1-E5 models see. Subsets: all flows, benign only.

    python src/e5_ablation.py [--quick]

Writes results/e5_ablation_{steps,summary}.csv, e5_ablation.png
"""
from __future__ import annotations
import argparse, time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from common import load, stats, z, stratified_sample, SEEDS, RES
from e5_mechanism import DATASETS, SOURCE_N, split

N_PER_DOMAIN = 10_000
STOP_AUC = 0.55                      # stop once the domains are near-indistinguishable
THRESHOLDS = [0.95, 0.9, 0.75, 0.6]


def eliminate(A, B, seed):
    n = min(N_PER_DOMAIN, len(A), len(B))
    X = pd.concat([A.sample(n, random_state=seed), B.sample(n, random_state=seed)])
    d = np.r_[np.zeros(n), np.ones(n)]
    Xtr, Xho, dtr, dho = train_test_split(X, d, test_size=0.3, random_state=seed, stratify=d)
    feats, rows = list(X.columns), []
    while feats:
        clf = HistGradientBoostingClassifier(max_iter=100, random_state=seed).fit(Xtr[feats], dtr)
        auc = roc_auc_score(dho, clf.predict_proba(Xho[feats])[:, 1])
        rows.append({"n_removed": len(X.columns) - len(feats), "auc": auc})
        if auc < STOP_AUC or len(feats) == 1:
            break
        pi = permutation_importance(clf, Xho[feats], dho, scoring="roc_auc", n_repeats=3,
                                    random_state=seed, n_jobs=-1)
        top = feats[int(np.argmax(pi.importances_mean))]
        rows[-1]["next_removed"] = top
        feats.remove(top)
    return rows


def run(data, seeds):
    rows = []
    for i, src in enumerate(DATASETS):
        for tgt in DATASETS[i + 1:]:
            (Xs, ys), (Xt, yt) = data[src], data[tgt]
            for seed in seeds:
                t = time.time()
                si = stratified_sample(ys, SOURCE_N, seed)
                Xpool, ypool, _, _ = split(Xt, yt, seed)
                for scaling in ("raw", "zscore"):
                    A, B = Xs.loc[si], Xpool
                    if scaling == "zscore":
                        A, B = z(A, *stats(A)), z(B, *stats(B))
                    for sub, (ia, ib) in {"all": (A.index, B.index),
                                          "benign": (A.index[ys.loc[A.index] == 0],
                                                     B.index[ypool.loc[B.index] == 0])}.items():
                        for r in eliminate(A.loc[ia], B.loc[ib], seed):
                            rows.append({"pair": f"{src}-{tgt}", "seed": seed, "scaling": scaling,
                                         "subset": sub, **r})
                print(f"ablation {src}-{tgt} seed {seed} done in {time.time() - t:.0f}s", flush=True)
    steps = pd.DataFrame(rows)
    steps.to_csv(RES / "e5_ablation_steps.csv", index=False)
    return steps


def report(steps):
    def first_below(g, thr):
        hit = g[g.auc < thr]
        return hit.n_removed.min() if len(hit) else np.nan        # nan = never got below

    summ = []
    for (pair, sc, sub, seed), g in steps.groupby(["pair", "scaling", "subset", "seed"]):
        r = {"pair": pair, "scaling": sc, "subset": sub, "seed": seed, "auc_full": g.auc.iloc[0]}
        r.update({f"removed_to_<{t}": first_below(g, t) for t in THRESHOLDS})
        summ.append(r)
    summ = pd.DataFrame(summ)
    summ.to_csv(RES / "e5_ablation_summary.csv", index=False)
    cols = ["auc_full"] + [f"removed_to_<{t}" for t in THRESHOLDS]
    print("\nfeatures removed (greedy, most-relied-on first) before domain AUC drops below threshold;"
          " mean over seeds (NaN = never, of 45):")
    print(summ.groupby(["scaling", "subset", "pair"])[cols].mean().round(2).to_string())
    print("\nAUC after removing the top-k features, mean over pairs & seeds:")
    print(steps[steps.n_removed.isin([0, 1, 2, 3, 5, 10, 15, 20, 30])]
          .groupby(["scaling", "subset", "n_removed"])["auc"].agg(["mean", "min", "max"]).unstack([0, 1]).round(3).to_string())
    first = steps[steps.n_removed < 5].dropna(subset=["next_removed"])
    print("\nfeatures most often among the first 5 removed (count over pairs, seeds, subsets):")
    print(first.groupby("scaling").next_removed.value_counts().groupby(level=0).head(12).to_string())

    fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=True, sharey=True)
    for i, sc in enumerate(["raw", "zscore"]):
        for j, sub in enumerate(["all", "benign"]):
            ax = axes[i, j]
            m = steps[(steps.scaling == sc) & (steps.subset == sub)]
            m.groupby(["pair", "n_removed"])["auc"].mean().unstack(0).plot(ax=ax, marker=".", legend=i + j == 0)
            ax.axhline(0.5, color="k", lw=0.8, ls="--")
            ax.set_title(f"{sc}, {sub} flows")
            ax.set_xlabel("features removed (greedy)")
        axes[i, 0].set_ylabel("domain-classifier AUC (held-out)")
    plt.tight_layout(); plt.savefig(RES / "e5_ablation.png", dpi=120); plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    seeds = SEEDS[:1] if a.quick else SEEDS[:3]
    RES.mkdir(exist_ok=True)
    data = {n: load(n) for n in DATASETS}
    report(run(data, seeds))


if __name__ == "__main__":
    main()
