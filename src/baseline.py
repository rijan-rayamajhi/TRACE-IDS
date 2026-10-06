"""Phase 2: RF baseline + the honest cross-dataset test, with per-dataset z-scoring.

Each dataset is standardized by ITS OWN training statistics so features live in a
comparable space. This is required for a fair cross-dataset comparison: raw units
differ (CIC Flow Duration in microseconds, UNSW dur in seconds; byte scales differ),
so a model trained on CIC's raw ranges sees UNSW values as out-of-range.

    python src/baseline.py

Runs on data/processed/{cic,unsw}.parquet. Shared helpers here are reused by invariant.py.
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, recall_score, confusion_matrix

OUT = Path("data/processed")
SEED = 42  # GUARDRAILS B5: fixed seed so results reproduce.


def load(name: str):
    df = pd.read_parquet(OUT / f"{name}.parquet")
    return df.drop(columns="attack"), df["attack"]


def stats(X):
    return X.mean(), X.std().replace(0, 1)       # std=0 -> 1 avoids divide-by-zero


def z(X, m, s):
    return (X - m) / s                            # keeps DataFrame + column names


def scaled_splits(cols=None, normalize=True):
    """CIC train/test and UNSW. With normalize=True each dataset is z-scored by its OWN stats
    (the alignment step); with False the features stay raw (the no-alignment baseline)."""
    Xc, yc = load("cic")
    Xu, yu = load("unsw")
    if cols is not None:
        Xc, Xu = Xc[cols], Xu[cols]
    Xtr, Xte, ytr, yte = train_test_split(Xc, yc, test_size=0.3, random_state=SEED, stratify=yc)
    if not normalize:
        return (Xtr, ytr), (Xte, yte), (Xu, yu)
    mc, sc = stats(Xtr)
    mu, su = stats(Xu)
    return (z(Xtr, mc, sc), ytr), (z(Xte, mc, sc), yte), (z(Xu, mu, su), yu)


def fit(X, y):
    # class_weight balanced: datasets are heavily imbalanced (UNSW-v3 ~4% attacks), so an
    # unweighted forest just predicts "benign" and scores high accuracy while catching nothing.
    return RandomForestClassifier(n_estimators=200, random_state=SEED, n_jobs=-1,
                                  class_weight="balanced").fit(X, y)


def fpr(y_true, y_pred) -> float:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return fp / (fp + tn) if (fp + tn) else 0.0


def scores(y_true, y_pred) -> dict:
    return {"acc": accuracy_score(y_true, y_pred),
            "recall": recall_score(y_true, y_pred, zero_division=0),  # attack detection rate
            "f1": f1_score(y_true, y_pred, zero_division=0),
            "fpr": fpr(y_true, y_pred)}


def run() -> pd.DataFrame:
    (Xtr, ytr), (Xte, yte), (Xu, yu) = scaled_splits()
    clf = fit(Xtr, ytr)
    table = pd.DataFrame({
        "same-dataset (CIC test)": scores(yte, clf.predict(Xte)),
        "cross-dataset (CIC->UNSW)": scores(yu, clf.predict(Xu)),
    }).T.round(3)
    gap = table.loc["same-dataset (CIC test)", "acc"] - table.loc["cross-dataset (CIC->UNSW)", "acc"]
    print(table.to_string())
    print(f"\ngeneralization gap (acc): {gap:.3f}")
    return table


if __name__ == "__main__":
    run()
