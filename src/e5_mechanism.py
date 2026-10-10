"""E5 — mechanism: WHY doesn't source data help? (PUBLICATION_PLAN, Step 6)

E3 showed source data gives no consistent benefit over target-only across 12 pairs. Three probes:

A. families — per attack category, recall of source-only / target-only / pooled / finetune (RF, GBT;
   k = 10, 100). Attack families are mapped to coarse categories shared across datasets (DoS, DDoS,
   scanning, brute force, web, backdoor, ...). If source knowledge transferred anywhere, it would be
   on categories the source ALSO contains. Also an "oracle" (RF on 100k labelled target flows) and
   the rank correlation of its feature importances with the source model's.
B. distance — how separable are source and target? Domain-classifier AUC (GBT, 5-fold), overall,
   within benign, within attacks, and within each shared attack category — in the exact z-scored
   representation the models see, and raw. AUC ~ 1.0 = the same attack type looks different on a
   different network. Spearman correlation of distance with E3's mean source benefit per pair.

Protocol as E1-E4 (leak-free split, z-scoring from source sample / target pool, nested shots).

    python src/data_loader.py families     # once: attack-family sidecars (verified row-aligned)
    python src/e5_mechanism.py families|distance|all [--quick]

Writes results/e5_families_{runs,summary}.csv, e5_distance.csv, e5_importance.csv, e5_families.png
"""
from __future__ import annotations
import argparse, time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from common import load, stats, z, stratified_sample, domain_class_weights, SEEDS, RES, OUT
from e2_transfer import pretrain, finetune, fit_weighted, rf

DATASETS = ["cic", "unsw", "ton", "bot"]
K_VALUES = [10, 100]
SOURCE_N, TEST_N = 100_000, 200_000

# coarse, cross-dataset attack categories (lower-cased family name -> category; first match wins)
CATEGORY_RULES = [("ddos", "ddos"), ("dos", "dos"), ("recon", "scanning"), ("scan", "scanning"),
                  ("brute", "bruteforce"), ("password", "bruteforce"), ("xss", "web"),
                  ("sql", "web"), ("injection", "web"), ("backdoor", "backdoor"), ("bot", "bot"),
                  ("benign", "benign")]


def category(family: str) -> str:
    f = family.lower()
    if f in ("brute_force_-web", "brute_force_-xss"):
        return "web"
    return next((c for key, c in CATEGORY_RULES if key in f), "other:" + f)


def load_with_category(name):
    X, y = load(name)
    cat = pd.read_parquet(OUT / f"{name}_family.parquet")["family"].map(category)
    cat.index = X.index
    assert ((cat == "benign") == (y == 0)).all()
    return X, y, cat


def split(Xt, yt, seed):
    Xpool, Xtest, ypool, ytest = train_test_split(Xt, yt, test_size=0.5, random_state=seed, stratify=yt)
    return Xpool, ypool, Xtest, ytest


# ---------------- A. per-category recall ----------------

def run_families(data, seeds):
    rows, imp_rows = [], []
    for src in DATASETS:
        for tgt in DATASETS:
            if src == tgt:
                continue
            (Xs, ys, cs), (Xt, yt, ct) = data[src], data[tgt]
            src_cats = set(cs[ys == 1].value_counts().loc[lambda v: v >= 100].index)
            for seed in seeds:
                t, rng = time.time(), np.random.default_rng(seed)
                si = stratified_sample(ys, SOURCE_N, seed)
                Xpool, ypool, Xtest, ytest = split(Xt, yt, seed)
                ti = stratified_sample(ytest, TEST_N, seed)
                ms, ss = stats(Xs.loc[si]); Xsrc, ysrc = z(Xs.loc[si], ms, ss), ys.loc[si]
                mp, sp = stats(Xpool); Xp = z(Xpool, mp, sp); Xte, cte = z(Xtest.loc[ti], mp, sp), ct.loc[ti]
                atk = rng.permutation(ypool.index[ypool == 1].to_numpy())
                ben = rng.permutation(ypool.index[ypool == 0].to_numpy())
                oi = stratified_sample(ypool, 100_000, seed)
                oracle = rf(seed).fit(Xp.loc[oi], ypool.loc[oi],
                                      sample_weight=domain_class_weights(np.ones(len(oi)), ypool.loc[oi].to_numpy()))
                preds = {("oracle", "RF", 0): oracle.predict(Xte)}
                for model in ("RF", "GBT"):
                    base = pretrain(model, Xsrc, ysrc, seed)
                    preds[("source-only", model, 0)] = base.predict(Xte)
                    if model == "RF":
                        r, _ = spearmanr(base.feature_importances_, oracle.feature_importances_)
                        imp_rows.append({"direction": f"{src}->{tgt}", "seed": seed, "importance_spearman": r})
                    for k in K_VALUES:
                        shot = np.concatenate([atk[:k], ben[:k]])
                        Xk, yk = Xp.loc[shot], ypool.loc[shot]
                        Xmix, ymix = pd.concat([Xsrc, Xk]), pd.concat([ysrc, yk])
                        dom = np.r_[np.zeros(len(ysrc)), np.ones(len(yk))]
                        preds[("target-only", model, k)] = fit_weighted(model, Xk, yk, np.ones(len(yk)), seed).predict(Xte)
                        preds[("pooled", model, k)] = fit_weighted(
                            model, Xmix, ymix, domain_class_weights(dom, ymix.to_numpy()), seed).predict(Xte)
                        preds[("finetune", model, k)] = finetune(model, base, Xk, yk, seed).predict(Xte)
                for (method, model, k), p in preds.items():
                    for c, idx in cte.groupby(cte).groups.items():
                        rows.append({"direction": f"{src}->{tgt}", "seed": seed, "model": model,
                                     "method": method, "k": k, "category": c, "n_test": len(idx),
                                     "in_source": c in src_cats, "detected": p[cte.index.get_indexer(idx)].mean()})
                print(f"families {src}->{tgt} seed {seed} done in {time.time() - t:.0f}s", flush=True)
    runs = pd.DataFrame(rows)
    runs.to_csv(RES / "e5_families_runs.csv", index=False)
    pd.DataFrame(imp_rows).to_csv(RES / "e5_importance.csv", index=False)
    return runs


def report_families(runs):
    atk = runs[runs.category != "benign"]
    summ = (atk.groupby(["direction", "category", "in_source", "model", "method", "k"])
               .agg(recall=("detected", "mean"), recall_std=("detected", "std"), n_test=("n_test", "mean"))
               .reset_index())
    summ.to_csv(RES / "e5_families_summary.csv", index=False)
    # benefit of the source on each category: pooled/finetune minus target-only, same seed
    key = ["direction", "seed", "model", "k", "category"]
    to = atk[atk.method == "target-only"].set_index(key)["detected"]
    diffs = []
    for meth in ("pooled", "finetune"):
        g = atk[atk.method == meth].set_index(key)
        diffs.append(g.assign(method=meth, delta=g["detected"] - to.reindex(g.index)).reset_index())
    d = pd.concat(diffs)
    d = d[d.n_test >= 20]                                  # skip categories too rare to measure
    print("\nsource benefit on attack recall (method − target-only), by whether the source has the category:")
    print(d.groupby(["in_source", "method", "model", "k"])["delta"].agg(["mean", "median", "count"]).round(3).to_string())
    so = atk[(atk.method == "source-only") & (atk.n_test >= 20)]
    print("\nsource-only (zero-shot) recall on categories the source HAS vs LACKS:")
    print(so.groupby(["in_source", "model"])["detected"].agg(["mean", "median", "count"]).round(3).to_string())
    print("\nsource-only recall per shared category (mean over pairs & seeds):")
    print(so[so.in_source].groupby(["category", "model"])["detected"].mean().unstack().round(3).to_string())
    ben = runs[runs.category == "benign"].groupby(["method", "model", "k"])["detected"].mean().round(3)
    print("\nfalse-positive rate on benign flows (mean over pairs):\n", ben.to_string())
    imp = pd.read_csv(RES / "e5_importance.csv").groupby("direction")["importance_spearman"].mean().round(3)
    print("\nRF feature-importance rank correlation, source model vs target oracle:\n", imp.to_string())

    fig, ax = plt.subplots(figsize=(8, 4.5))
    s = d[(d.k == 10)].groupby(["in_source", "method", "model"])["delta"].mean().unstack(["method", "model"])
    s.T.plot.bar(ax=ax, color=["C3", "C0"], rot=0)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("Δ attack recall vs target-only (k=10)")
    ax.set_title("Source benefit per attack category: source lacks (False) vs has (True) the category")
    ax.legend(title="category in source")
    plt.tight_layout(); plt.savefig(RES / "e5_families.png", dpi=120); plt.close()


# ---------------- B. domain distance ----------------

def domain_auc(A, B, seed, n=20_000):
    n = min(n, len(A), len(B))
    if n < 50:
        return np.nan
    X = pd.concat([A.sample(n, random_state=seed), B.sample(n, random_state=seed)])
    d = np.r_[np.zeros(n), np.ones(n)]
    clf = HistGradientBoostingClassifier(max_iter=100, random_state=seed)
    return cross_val_score(clf, X, d, cv=5, scoring="roc_auc").mean()


def run_distance(data, seeds):
    rows = []
    for i, src in enumerate(DATASETS):
        for tgt in DATASETS[i + 1:]:                       # z-scoring is per domain -> symmetric
            (Xs, ys, cs), (Xt, yt, ct) = data[src], data[tgt]
            shared = sorted((set(cs[ys == 1]) & set(ct[yt == 1])))
            for seed in seeds:
                t = time.time()
                si = stratified_sample(ys, SOURCE_N, seed)
                Xpool, ypool, _, _ = split(Xt, yt, seed)
                for scaling in ("zscore", "raw"):
                    A, B = Xs.loc[si], Xpool
                    if scaling == "zscore":
                        A, B = z(A, *stats(A)), z(B, *stats(B))
                    subsets = {"all": (A.index, B.index),
                               "benign": (A.index[ys.loc[A.index] == 0], B.index[ypool.loc[B.index] == 0]),
                               "attack": (A.index[ys.loc[A.index] == 1], B.index[ypool.loc[B.index] == 1])}
                    for c in shared:
                        subsets[f"cat:{c}"] = (A.index[cs.loc[A.index] == c], B.index[ct.loc[B.index] == c])
                    for sub, (ia, ib) in subsets.items():
                        rows.append({"pair": f"{src}-{tgt}", "seed": seed, "scaling": scaling, "subset": sub,
                                     "n": min(len(ia), len(ib)), "auc": domain_auc(A.loc[ia], B.loc[ib], seed)})
                print(f"distance {src}-{tgt} seed {seed} done in {time.time() - t:.0f}s", flush=True)
    dist = pd.DataFrame(rows)
    dist.to_csv(RES / "e5_distance.csv", index=False)
    return dist


def report_distance(dist):
    print("\ndomain-classifier AUC (0.5 = indistinguishable, 1.0 = perfectly separable), mean over seeds:")
    print(dist.groupby(["pair", "subset", "scaling"])["auc"].mean().unstack().round(4).to_string())
    e3 = RES / "e3_significance.csv"
    if e3.exists():
        sig = pd.read_csv(e3)
        benefit = sig.groupby("direction")["delta_f1"].mean()
        auc = dist[(dist.subset == "all") & (dist.scaling == "zscore")].groupby("pair")["auc"].mean()
        pair_auc = benefit.index.map(lambda d: auc.get("-".join(sorted(d.split("->"),
                                     key=DATASETS.index)), np.nan))
        r, p = spearmanr(pair_auc, benefit.to_numpy(), nan_policy="omit")
        print(f"\nSpearman(domain AUC, mean E3 source benefit) over 12 pairs: r = {r:.3f}, p = {p:.3f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", nargs="?", default="all", choices=["families", "distance", "all"])
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    seeds = SEEDS[:1] if a.quick else SEEDS
    RES.mkdir(exist_ok=True)
    data = {n: load_with_category(n) for n in DATASETS}
    for n, (_, y, c) in data.items():
        print(n, c[y == 1].value_counts().to_dict())
    if a.what in ("distance", "all"):
        report_distance(run_distance(data, seeds[:5]))
    if a.what in ("families", "all"):
        report_families(run_families(data, seeds))


if __name__ == "__main__":
    main()
