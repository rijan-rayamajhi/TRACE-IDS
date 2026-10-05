"""Phase 3 (the novelty): explanation-guided domain-invariant feature selection.

A feature only transfers if it matters in BOTH datasets AND points the same way in both.
Rank by SHAP importance in a CIC-trained and a UNSW-trained model (each z-scored by its
own stats), keep features high-importance in both with matching effect direction, retrain
on that subset, and check the cross-dataset gap.

    python src/invariant.py

Reuses baseline.py. Runs on data/processed/{cic,unsw}.parquet.
"""
from __future__ import annotations
import numpy as np, pandas as pd
import shap
from baseline import load, scores, fit, stats, z, scaled_splits, SEED

SHAP_N = 100_000  # subsample for the importance-ranking models; ranking is stable, fit is ~10x faster


def z_self(name):
    """Load a dataset, subsample for speed, z-score by its own stats."""
    X, y = load(name)
    if len(X) > SHAP_N:
        X = X.sample(SHAP_N, random_state=SEED)
        y = y.loc[X.index]
    m, s = stats(X)
    return z(X, m, s), y


def shap_importance(model, X) -> pd.Series:
    Xs = X.sample(min(500, len(X)), random_state=SEED)
    sv = shap.TreeExplainer(model).shap_values(Xs)
    if isinstance(sv, list):          # older shap: [class0, class1]
        sv = sv[1]
    elif np.ndim(sv) == 3:            # newer shap: (n, features, classes)
        sv = sv[:, :, 1]
    imp = pd.Series(np.abs(sv).mean(axis=0), index=X.columns)
    return imp / imp.sum()


def direction(X, y) -> pd.Series:
    return X[y == 1].mean() - X[y == 0].mean()    # sign = which way the feature pushes


def select():
    """Return (importance table, kept-feature list). Reused by evaluate.py."""
    Xc, yc = z_self("cic")
    Xu, yu = z_self("unsw")
    inv = pd.concat([shap_importance(fit(Xc, yc), Xc),
                     shap_importance(fit(Xu, yu), Xu)], axis=1, keys=["cic", "unsw"])
    inv["min"] = inv.min(axis=1)
    inv["agree"] = np.sign(direction(Xc, yc)) == np.sign(direction(Xu, yu))
    inv = inv.sort_values("min", ascending=False)
    cand = inv[inv["agree"]]
    keep = cand.index[cand["min"] >= cand["min"].mean()].tolist() or [cand["min"].idxmax()]
    return inv, keep


def run():
    inv, keep = select()
    print("SHAP importance per dataset (z-scored), sorted by cross-dataset min:")
    print(inv.round(3).to_string())
    print(f"\ninvariant features kept: {keep}")
    print(f"dropped: {[c for c in inv.index if c not in keep]}\n")

    def gap(cols):
        (Xtr, ytr), (Xte, yte), (Xu2, yu2) = scaled_splits(cols)
        m = fit(Xtr, ytr)
        return scores(yte, m.predict(Xte))["acc"], scores(yu2, m.predict(Xu2))["acc"]

    s0, c0 = gap(list(inv.index))
    s1, c1 = gap(keep)
    tbl = pd.DataFrame(
        {"same-dataset acc": [s0, s1], "cross-dataset acc": [c0, c1], "gap": [s0 - c0, s1 - c1]},
        index=["all features", "invariant features"],
    ).round(3)
    print(tbl.to_string())
    print(f"\ngap change: {s0 - c0:.3f} -> {s1 - c1:.3f}  (lower cross-dataset gap = better transfer)")
    return tbl


if __name__ == "__main__":
    run()
