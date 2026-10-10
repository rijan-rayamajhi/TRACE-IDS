"""Shared helpers for the multi-seed experiments (E1+).

Leakage rule: normalization statistics come only from data the model is allowed to see at
training time — the source training sample, and the UNLABELED target pool. The target test
split is never used for statistics, sampling, or fitting.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

OUT = Path("data/processed")
RES = Path("results")
SEEDS = list(range(10))                 # GUARDRAILS B5: fixed seeds, reported as mean ± std
TTL = ["MIN_TTL", "MAX_TTL"]            # IP-header TTL: known UNSW testbed artifact (Sarhan et al.)


def load(name: str) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_parquet(OUT / f"{name}.parquet")
    y = df.pop("attack").astype(int)
    return df.astype("float32"), y


def stats(X: pd.DataFrame):
    return X.mean(), X.std().replace(0, 1)


def z(X: pd.DataFrame, m, s) -> pd.DataFrame:
    return (X - m) / s


def stratified_sample(y: pd.Series, n: int, seed: int) -> pd.Index:
    """Index of a class-stratified random sample of size ~n (all rows if n >= len)."""
    if n >= len(y):
        return y.index
    frac = n / len(y)
    return (y.groupby(y, group_keys=False)
             .apply(lambda g: g.sample(max(1, round(len(g) * frac)), random_state=seed))
             .index)


def fit(X, y, seed: int, n_estimators: int = 100, sample_weight=None):
    """Balanced class weights by default; with sample_weight, the caller sets all weighting."""
    return RandomForestClassifier(n_estimators=n_estimators, random_state=seed, n_jobs=-1,
                                  class_weight=None if sample_weight is not None else "balanced"
                                  ).fit(X, y, sample_weight=sample_weight)


def domain_class_weights(domain: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Equal total weight per (domain, class) cell, so k target flows count as much as the
    whole source sample. Fairer than plain pooling, where 100k source rows drown 2k target rows."""
    w = np.empty(len(y), dtype="float64")
    for d in np.unique(domain):
        for c in np.unique(y):
            m = (domain == d) & (y == c)
            if m.any():
                w[m] = 1.0 / m.sum()
    return w * len(y) / w.sum()


def scores(y_true, y_pred) -> dict:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    return {"recall": rec, "precision": prec,
            "f1": 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0,
            "fpr": fp / (fp + tn) if (fp + tn) else 0.0}


def summarize(runs: pd.DataFrame, keys: list[str], metrics=("recall", "precision", "f1", "fpr")):
    """Mean ± std over seeds."""
    g = runs.groupby(keys)[list(metrics)]
    out = g.mean().add_suffix("_mean").join(g.std().add_suffix("_std"))
    out["n_seeds"] = g.size()
    return out.reset_index()
