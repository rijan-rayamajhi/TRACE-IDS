"""E1 — the decisive experiments (PUBLICATION_PLAN Step 2).

For each direction (source -> target), seed, and k labeled target flows per class:
  * mode "source+k":   train on a source sample + k target flows/class  (k=0 is zero-shot)
  * mode "target-only": train on the k target flows/class alone          (RQ2: does source help?)
  * mode "source+k-weighted": source+k with equal weight per (domain, class) cell — the fair
    version of source+k, so source isn't judged on 100k source rows drowning 2k target rows
each under two feature sets:
  * "all":  all 47 shared features
  * "-TTL": without MIN_TTL / MAX_TTL                                      (RQ1: artifact reliance)

Protocol (leak-free):
  target is split 50/50 (stratified, per seed) into an unlabeled POOL and a TEST set.
  Source is z-scored by its own training sample; target by the POOL's statistics only.
  Few-shot flows are drawn from the pool; TEST is never touched except for scoring.

    python src/e1_fewshot.py                 # full run: both directions, 10 seeds
    python src/e1_fewshot.py --quick         # smoke test: 1 seed, small samples

Writes results/e1_runs.csv (per seed), results/e1_summary.csv (mean ± std), results/e1_recovery.png.
"""
from __future__ import annotations
import argparse, time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from common import (load, stats, z, stratified_sample, fit, domain_class_weights, scores,
                    summarize, SEEDS, TTL, RES)

K_VALUES = [0, 1, 5, 10, 50, 100, 500]
FEATURE_SETS = {"all": [], "-TTL": TTL}
DIRECTIONS = [("cic", "unsw"), ("unsw", "cic")]


def run_one(Xs, ys, Xt, yt, seed, source_n, test_n, n_trees):
    """All (k, mode, feature set) results for one direction and seed."""
    rng = np.random.default_rng(seed)
    src_idx = stratified_sample(ys, source_n, seed)
    Xpool, Xtest, ypool, ytest = train_test_split(Xt, yt, test_size=0.5, random_state=seed, stratify=yt)
    test_idx = stratified_sample(ytest, test_n, seed)
    Xtest, ytest = Xtest.loc[test_idx], ytest.loc[test_idx]

    # leak-free alignment: source by its training sample, target by the unlabeled pool
    ms, ss = stats(Xs.loc[src_idx]); Xsrc = z(Xs.loc[src_idx], ms, ss); ysrc = ys.loc[src_idx]
    mp, sp = stats(Xpool); Xpool_z = z(Xpool, mp, sp); Xtest_z = z(Xtest, mp, sp)

    atk = ypool.index[ypool == 1].to_numpy()
    ben = ypool.index[ypool == 0].to_numpy()
    # nested draws: the k=5 set contains the k=1 set, etc. — curves are comparable across k
    atk_order, ben_order = rng.permutation(atk), rng.permutation(ben)

    rows = []
    for k in K_VALUES:
        shot = np.concatenate([atk_order[:k], ben_order[:k]])
        for fs, drop in FEATURE_SETS.items():
            cols = [c for c in Xsrc.columns if c not in drop]
            Xmix = pd.concat([Xsrc[cols], Xpool_z.loc[shot, cols]])
            ymix = pd.concat([ysrc, ypool.loc[shot]])
            modes = {"source+k": (Xmix, ymix, None)}
            if k > 0:
                domain = np.r_[np.zeros(len(ysrc)), np.ones(len(shot))]
                modes["source+k-weighted"] = (Xmix, ymix, domain_class_weights(domain, ymix.to_numpy()))
                modes["target-only"] = (Xpool_z.loc[shot, cols], ypool.loc[shot], None)
            for mode, (Xtr, ytr, w) in modes.items():
                pred = fit(Xtr, ytr, seed, n_trees, sample_weight=w).predict(Xtest_z[cols])
                rows.append({"seed": seed, "k": k, "features": fs, "mode": mode, **scores(ytest, pred)})
    return rows


def plot(summary: pd.DataFrame, path):
    dirs = summary["direction"].unique()
    fig, axes = plt.subplots(1, len(dirs), figsize=(6 * len(dirs), 4.2), squeeze=False)
    style = {("source+k", "all"): ("C0", "-"), ("source+k", "-TTL"): ("C0", "--"),
             ("source+k-weighted", "all"): ("C2", "-"), ("source+k-weighted", "-TTL"): ("C2", "--"),
             ("target-only", "all"): ("C3", "-"), ("target-only", "-TTL"): ("C3", "--")}
    for ax, d in zip(axes[0], dirs):
        for (mode, fs), (c, ls) in style.items():
            s = summary[(summary.direction == d) & (summary["mode"] == mode) & (summary.features == fs)]
            s = s.sort_values("k")
            if s.empty:
                continue
            x = s["k"].replace(0, 0.5)                     # show k=0 on the log axis
            ax.plot(x, s["recall_mean"], ls, color=c, marker="o", ms=3, label=f"{mode}, {fs}")
            ax.fill_between(x, s["recall_mean"] - s["recall_std"], s["recall_mean"] + s["recall_std"],
                            color=c, alpha=0.12)
        ax.set_xscale("log"); ax.set_ylim(0, 1.02); ax.grid(alpha=0.3)
        ax.set_xlabel("labeled target flows per class (k; 0 shown at 0.5)")
        ax.set_ylabel("attack recall (mean ± std over seeds)"); ax.set_title(d)
    axes[0][0].legend(fontsize=8, loc="lower right")
    plt.tight_layout(); plt.savefig(path, dpi=130); plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="1 seed, small samples (smoke test)")
    a = ap.parse_args()
    seeds = SEEDS[:1] if a.quick else SEEDS
    source_n, test_n, n_trees = (20_000, 20_000, 50) if a.quick else (100_000, 200_000, 100)
    tag = "_quick" if a.quick else ""

    data = {n: load(n) for n in {d for pair in DIRECTIONS for d in pair}}
    for n, (X, y) in data.items():
        print(f"{n}: {len(X):,} rows, {X.shape[1]} features, attack rate {y.mean():.4f}")

    runs = []
    for src, tgt in DIRECTIONS:
        for seed in seeds:
            t = time.time()
            rows = run_one(*data[src], *data[tgt], seed, source_n, test_n, n_trees)
            runs += [{"direction": f"{src}->{tgt}", **r} for r in rows]
            print(f"{src}->{tgt} seed {seed} done in {time.time() - t:.0f}s", flush=True)

    RES.mkdir(exist_ok=True)
    runs = pd.DataFrame(runs)
    runs.to_csv(RES / f"e1_runs{tag}.csv", index=False)
    summary = summarize(runs, ["direction", "mode", "features", "k"])
    summary.to_csv(RES / f"e1_summary{tag}.csv", index=False)
    plot(summary, RES / f"e1_recovery{tag}.png")

    view = summary.pivot_table(index=["direction", "k"], columns=["mode", "features"],
                               values="recall_mean").round(3)
    print("\nattack recall (mean over seeds):\n", view.to_string())
    print(f"\nwrote {RES}/e1_runs{tag}.csv, e1_summary{tag}.csv, e1_recovery{tag}.png")


if __name__ == "__main__":
    main()
