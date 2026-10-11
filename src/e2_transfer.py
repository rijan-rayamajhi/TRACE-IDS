"""E2 — is "source adds nothing" just a weak-baseline artifact? (PUBLICATION_PLAN, RQ2 robustness)

E1 showed pooled source+k ~= target-only for a Random Forest. A reviewer will say pooling is a weak
way to use source data. E2 gives the source every reasonable chance: 3 model families x 4 methods.

Models:  RF (random forest), GBT (histogram gradient boosting), MLP (neural network)
Methods:
  target-only  k target flows/class alone (the baseline to beat; needs k >= 1)
  pooled       source + k, equal total weight per (domain, class) cell
  iw           importance weighting (covariate-shift correction, unsupervised domain adaptation):
               source flows reweighted by p(target|x)/p(source|x) from a domain classifier trained on
               source vs. the UNLABELED target pool; + k target flows. k=0 = unsupervised DA zero-shot.
  finetune     pretrain on source, then adapt on the k flows:
                 RF  - keep the 100 source trees, add 100 trees grown on the k flows (warm start)
                 GBT - frozen source model as the boosting init; 50 residual trees fit on the k flows
                 MLP - continue SGD (partial_fit) from the source weights on the k flows

Protocol identical to E1 (leak-free): per seed, target split 50/50 into unlabeled pool / test;
source z-scored by its training sample, target by the pool; few-shot draws nested across k.
--scaling shared instead z-scores both domains with ONE set of statistics (source sample + unlabeled
target pool; still leak-free). Per-domain scaling maps the same categorical code (e.g. PROTOCOL = 6)
to a different value per domain (E5 follow-up); shared scaling removes that. For RF/GBT it is
equivalent to raw features (trees are invariant to a monotone transform shared by all rows).

    python src/e2_transfer.py            # full: both directions, 10 seeds
    python src/e2_transfer.py --quick    # smoke test
    python src/e2_transfer.py --datasets cic unsw ton bot --out all   # all 12 directed pairs
                                         # (pairs already in results/e2_runs_all.csv are skipped)
    python src/e2_transfer.py --datasets cic unsw ton bot --scaling shared --out all_shared

Writes results/e2_runs.csv, results/e2_summary.csv, results/e2_transfer.png
"""
from __future__ import annotations
import argparse, copy, time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import (RandomForestClassifier, HistGradientBoostingClassifier,
                              GradientBoostingClassifier)
from sklearn.frozen import FrozenEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from common import (load, stats, z, stratified_sample, domain_class_weights, scores, summarize,
                    SEEDS, RES)

K_VALUES = [0, 1, 5, 10, 50, 100]
DIRECTIONS = [("cic", "unsw"), ("unsw", "cic")]
IW_CLIP = (0.01, 100.0)
MLP_EPOCHS, MLP_FT_EPOCHS = 15, 50


# ---------- models: each takes (X, y, sample_weight) and returns a fitted classifier ----------

def rf(seed, n=100):
    return RandomForestClassifier(n_estimators=n, random_state=seed, n_jobs=-1)


def gbt(seed, n=None):
    # default min_samples_leaf=20 can't split a 2-20 flow training set, which would make
    # target-only GBT a constant predictor and unfairly favour the source; scale it down.
    leaf = 20 if n is None else max(1, min(20, n // 10))
    return HistGradientBoostingClassifier(max_iter=200, random_state=seed, early_stopping=False,
                                          min_samples_leaf=leaf)


def mlp(seed):
    return MLPClassifier(hidden_layer_sizes=(64, 32), alpha=1e-4, batch_size=256,
                         learning_rate_init=1e-3, max_iter=MLP_EPOCHS, random_state=seed)


def resample(X, y, w, n, seed):
    """Weighted bootstrap — how weighting is applied to the MLP (no sample_weight support)."""
    idx = np.random.default_rng(seed).choice(len(y), size=n, replace=True, p=w / w.sum())
    return X.iloc[idx], y.iloc[idx]


def fit_weighted(model, X, y, w, seed):
    if model == "RF":
        return rf(seed).fit(X, y, sample_weight=w)
    if model == "GBT":
        return gbt(seed, len(y)).fit(X, y, sample_weight=w)
    Xr, yr = resample(X, y, w, min(len(y), 100_000) if len(y) > 1_000 else 2_000, seed)
    return mlp(seed).fit(Xr, yr)


def importance_weights(Xsrc, Xpool, seed):
    """p(target|x)/p(source|x) from a domain classifier on source vs. unlabeled target pool."""
    n = min(len(Xsrc), len(Xpool), 50_000)
    Xd = pd.concat([Xsrc.sample(n, random_state=seed), Xpool.sample(n, random_state=seed)])
    d = np.r_[np.zeros(n), np.ones(n)]
    clf = LogisticRegression(max_iter=1000, C=1.0).fit(Xd.clip(-10, 10), d)
    p = clf.predict_proba(Xsrc.clip(-10, 10))[:, 1]
    w = np.clip(p / np.clip(1 - p, 1e-9, None), *IW_CLIP)
    ess = w.sum() ** 2 / (w ** 2).sum() / len(w)          # effective sample size fraction
    return w, ess


def pretrain(model, Xs, ys, seed):
    w = domain_class_weights(np.zeros(len(ys)), ys.to_numpy())   # class-balanced
    if model == "RF":
        return RandomForestClassifier(n_estimators=100, random_state=seed, n_jobs=-1,
                                      warm_start=True).fit(Xs, ys, sample_weight=w)
    if model == "GBT":
        return gbt(seed).fit(Xs, ys, sample_weight=w)
    return mlp(seed).fit(*resample(Xs, ys, w, len(ys), seed))


def finetune(model, base, Xk, yk, seed):
    if model == "GBT":
        return GradientBoostingClassifier(init=FrozenEstimator(base), n_estimators=50, max_depth=2,
                                          learning_rate=0.1, random_state=seed).fit(Xk, yk)
    m = copy.deepcopy(base)                 # never mutate the shared source model
    if model == "RF":                       # warm start: keep 100 source trees, grow 100 on the k flows
        return m.set_params(n_estimators=200).fit(Xk, yk)
    for _ in range(MLP_FT_EPOCHS):          # continue SGD from the source weights
        m.partial_fit(Xk, yk)
    return m


def run_one(Xs, ys, Xt, yt, seed, source_n, test_n, scaling="domain"):
    rng = np.random.default_rng(seed)
    src_idx = stratified_sample(ys, source_n, seed)
    Xpool, Xtest, ypool, ytest = train_test_split(Xt, yt, test_size=0.5, random_state=seed, stratify=yt)
    test_idx = stratified_sample(ytest, test_n, seed)
    Xtest, ytest = Xtest.loc[test_idx], ytest.loc[test_idx]
    if scaling == "shared":
        ms, ss = stats(pd.concat([Xs.loc[src_idx], Xpool])); mp, sp = ms, ss
    else:
        (ms, ss), (mp, sp) = stats(Xs.loc[src_idx]), stats(Xpool)
    Xsrc, ysrc = z(Xs.loc[src_idx], ms, ss), ys.loc[src_idx]
    Xpool, Xtest = z(Xpool, mp, sp), z(Xtest, mp, sp)

    iw, ess = importance_weights(Xsrc, Xpool, seed)
    atk_order = rng.permutation(ypool.index[ypool == 1].to_numpy())
    ben_order = rng.permutation(ypool.index[ypool == 0].to_numpy())

    rows = []
    for model in ["RF", "GBT", "MLP"]:
        base = pretrain(model, Xsrc, ysrc, seed)
        for k in K_VALUES:
            shot = np.concatenate([atk_order[:k], ben_order[:k]])
            Xk, yk = Xpool.loc[shot], ypool.loc[shot]
            Xmix, ymix = pd.concat([Xsrc, Xk]), pd.concat([ysrc, yk])
            dom = np.r_[np.zeros(len(ysrc)), np.ones(len(yk))]
            fits = {}
            if k == 0:
                fits["pooled"] = base                                    # = source-only
                w = domain_class_weights(np.zeros(len(ysrc)), ysrc.to_numpy()) * iw
                fits["iw"] = fit_weighted(model, Xsrc, ysrc, w, seed)
            else:
                fits["target-only"] = fit_weighted(model, Xk, yk, np.ones(len(yk)), seed)
                fits["pooled"] = fit_weighted(model, Xmix, ymix,
                                              domain_class_weights(dom, ymix.to_numpy()), seed)
                w = domain_class_weights(dom, ymix.to_numpy()) * np.r_[iw, np.ones(len(yk))]
                fits["iw"] = fit_weighted(model, Xmix, ymix, w, seed)
                fits["finetune"] = finetune(model, base, Xk, yk, seed)
            for method, m in fits.items():
                rows.append({"seed": seed, "model": model, "method": method, "k": k, "iw_ess": ess,
                             **scores(ytest, m.predict(Xtest))})
    return rows


def plot(summary, path):
    models, dirs = ["RF", "GBT", "MLP"], summary["direction"].unique()
    fig, axes = plt.subplots(len(dirs), len(models), figsize=(15, 4 * len(dirs)), squeeze=False)
    colors = {"target-only": "C3", "pooled": "C0", "iw": "C2", "finetune": "C1"}
    for i, d in enumerate(dirs):
        for j, mdl in enumerate(models):
            ax = axes[i][j]
            for meth, c in colors.items():
                s = summary[(summary.direction == d) & (summary.model == mdl) & (summary.method == meth)]
                s = s.sort_values("k")
                if s.empty:
                    continue
                x = s["k"].replace(0, 0.5)
                ax.plot(x, s["f1_mean"], "-o", ms=3, color=c, label=meth)
                ax.fill_between(x, s["f1_mean"] - s["f1_std"], s["f1_mean"] + s["f1_std"], color=c, alpha=0.12)
            ax.set_xscale("log"); ax.set_ylim(0, 1.02); ax.grid(alpha=0.3)
            ax.set_title(f"{d} · {mdl}"); ax.set_xlabel("k (0 shown at 0.5)"); ax.set_ylabel("F1 (mean ± std)")
    axes[0][0].legend(fontsize=8)
    plt.tight_layout(); plt.savefig(path, dpi=120); plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--datasets", nargs="+", default=["cic", "unsw"])
    ap.add_argument("--out", default="", help="output tag, e.g. 'all' -> e2_runs_all.csv")
    ap.add_argument("--scaling", choices=["domain", "shared"], default="domain")
    a = ap.parse_args()
    seeds = SEEDS[:1] if a.quick else SEEDS
    source_n, test_n = (20_000, 20_000) if a.quick else (100_000, 200_000)
    tag = "_quick" if a.quick else (f"_{a.out}" if a.out else "")
    pairs = [(s_, t_) for s_ in a.datasets for t_ in a.datasets if s_ != t_]

    RES.mkdir(exist_ok=True)
    out_runs = RES / f"e2_runs{tag}.csv"
    runs = pd.read_csv(out_runs) if out_runs.exists() and not a.quick else pd.DataFrame()
    data = {n: load(n) for n in a.datasets}
    for src, tgt in pairs:
        for seed in seeds:
            d = f"{src}->{tgt}"
            if len(runs) and ((runs.direction == d) & (runs.seed == seed)).any():
                continue                                    # resumable: skip finished work
            t = time.time()
            new = pd.DataFrame([{"direction": d, **r}
                                for r in run_one(*data[src], *data[tgt], seed, source_n, test_n, a.scaling)])
            runs = pd.concat([runs, new], ignore_index=True)
            runs.to_csv(out_runs, index=False)              # checkpoint after every seed
            print(f"{d} seed {seed} done in {time.time() - t:.0f}s", flush=True)
    summary = summarize(runs, ["direction", "model", "method", "k"])
    summary.to_csv(RES / f"e2_summary{tag}.csv", index=False)
    plot(summary, RES / f"e2_transfer{tag}.png")
    print("\nimportance-weight effective sample size (fraction of source):",
          runs.groupby("direction")["iw_ess"].mean().round(4).to_dict())
    print("\nF1 (mean over seeds):\n", summary.pivot_table(index=["direction", "model", "k"],
          columns="method", values="f1_mean").round(3).to_string())
    print(f"\nwrote {RES}/e2_runs{tag}.csv, e2_summary{tag}.csv, e2_transfer{tag}.png")


if __name__ == "__main__":
    main()
