"""E6 — robustness checks requested by the internal review (paper/phase6_review/phase6b_review.md).

A. bacc   — Table 2 recomputed on balanced accuracy instead of F1. F1 is uninformative when the target is
            almost all attacks (NF-BoT-IoT-v3 is 97.5% attacks: flagging everything scores F1 ~0.99).
B. pooled — one pooled estimate of the source effect with a 95% CI: mean ΔF1 (and Δbalanced accuracy) over
            all (model, method, k) cells, cluster-bootstrapped over the 12 directed pairs (cells within a
            pair share the target-only arm, so pairs are the independent unit).
C. control — negative control for the domain classifier: two disjoint random halves of the SAME dataset.
            AUC near 0.5 here is what makes AUC ~1.0 between datasets meaningful.

    python src/e6_robustness.py [bacc|pooled|control|all]

Reads results/e2_runs_all{,_shared,_nottl}.csv. Writes results/e6_*.csv.
"""
from __future__ import annotations
import sys
import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from common import load, stats, z, stratified_sample, RES
from e5_mechanism import DATASETS, SOURCE_N, domain_auc

RUNS = {"per-domain": "e2_runs_all.csv", "shared": "e2_runs_all_shared.csv", "no-TTL (shared)": "e2_runs_all_nottl_shared.csv"}
METHODS = ["pooled", "iw", "finetune"]


def load_runs(tag):
    p = RES / RUNS[tag]
    if not p.exists():
        return None
    r = pd.read_csv(p)
    return r.assign(bacc=(r.recall + 1 - r.fpr) / 2)


def verdicts(runs, metric):
    base = runs[runs.method == "target-only"].set_index(["direction", "model", "k", "seed"])[metric]
    rows = []
    for (d, mdl, meth, k), g in runs[(runs.k > 0) & runs.method.isin(METHODS)].groupby(["direction", "model", "method", "k"]):
        diff = g.set_index("seed")[metric] - base.loc[(d, mdl, k)]
        p = 1.0 if np.allclose(diff, 0) else wilcoxon(diff).pvalue
        v = "no diff" if p >= 0.05 else ("help" if diff.mean() > 0 else "hurt")
        rows.append({"direction": d, "model": mdl, "method": meth, "k": k, "delta": diff.mean(), "p": p, "verdict": v})
    return pd.DataFrame(rows)


def run_bacc():
    out = []
    for tag in RUNS:
        r = load_runs(tag)
        if r is None:
            print(f"[{tag}] runs file missing, skipped"); continue
        for metric in ("f1", "bacc"):
            v = verdicts(r, metric).assign(scaling=tag, metric=metric)
            out.append(v)
            c = v.verdict.value_counts()
            print(f"[{tag:10}] {metric:4}: help {c.get('help', 0):3}  no diff {c.get('no diff', 0):3}  hurt {c.get('hurt', 0):3}"
                  f"  | median Δ {v.delta.median():+.4f}")
            if metric == "bacc":
                bot = v[v.direction.str.endswith("->bot")].verdict.value_counts()
                print(f"             BoT-target cells (bacc): {bot.to_dict()}")
    pd.concat(out).to_csv(RES / "e6_verdicts_by_metric.csv", index=False)


def run_pooled(n_boot=10_000, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for tag in RUNS:
        r = load_runs(tag)
        if r is None:
            continue
        for metric in ("f1", "bacc"):
            cell = verdicts(r, metric)
            per_pair = cell.groupby("direction").delta.mean()          # independent unit = directed pair
            pairs = per_pair.to_numpy()
            boot = rng.choice(pairs, size=(n_boot, len(pairs)), replace=True).mean(axis=1)
            lo, hi = np.percentile(boot, [2.5, 97.5])
            by_k = cell.groupby("k").delta.mean().round(4).to_dict()
            rows.append({"scaling": tag, "metric": metric, "mean_delta": pairs.mean(), "ci_low": lo, "ci_high": hi,
                         "pairs_positive": int((pairs > 0).sum()), "n_pairs": len(pairs), "mean_delta_by_k": by_k})
            print(f"[{tag:10}] {metric:4}: pooled mean Δ {pairs.mean():+.4f}  95% CI [{lo:+.4f}, {hi:+.4f}]  "
                  f"pairs with Δ>0: {(pairs > 0).sum()}/{len(pairs)}  by k: {by_k}")
    pd.DataFrame(rows).to_csv(RES / "e6_pooled_effect.csv", index=False)


def run_control(seeds=(0, 1, 2)):
    rows = []
    for name in DATASETS:
        X, y = load(name)
        for seed in seeds:
            idx = stratified_sample(y, 2 * SOURCE_N, seed)
            perm = np.random.default_rng(seed).permutation(idx.to_numpy())
            a, b = perm[: len(perm) // 2], perm[len(perm) // 2:]
            for scaling in ("raw", "zscore"):
                A, B = X.loc[a], X.loc[b]
                if scaling == "zscore":
                    A, B = z(A, *stats(A)), z(B, *stats(B))
                auc = domain_auc(A, B, seed)
                rows.append({"dataset": name, "seed": seed, "scaling": scaling, "auc": auc})
                print(f"control {name} seed {seed} {scaling}: within-dataset AUC {auc:.4f}", flush=True)
    c = pd.DataFrame(rows)
    c.to_csv(RES / "e6_domain_control.csv", index=False)
    print("\nwithin-dataset domain AUC (two random halves of one dataset), mean over seeds:")
    print(c.groupby(["dataset", "scaling"]).auc.mean().unstack().round(4).to_string())


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("bacc", "all"):
        run_bacc()
    if what in ("pooled", "all"):
        run_pooled()
    if what in ("control", "all"):
        run_control()
