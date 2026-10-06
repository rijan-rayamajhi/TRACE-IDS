"""Phase RQ2: a reliability flag — does the detector know when to distrust its own verdict?

Idea: fit a novelty detector (Isolation Forest) on the CIC training distribution. For any new
flow, its novelty score is a "drift" signal: how unlike the training data it looks. If high drift
predicts where the Random Forest is wrong, the flag is useful — the system can say "distrust this".

    python src/reliability.py

Reuses baseline.py. Runs on data/processed/{cic,unsw}.parquet.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from baseline import load, stats, z, fit, scores, SEED

RES = Path("results")


def run():
    Xc, yc = load("cic")
    Xu, yu = load("unsw")
    Xtr, Xte, ytr, yte = train_test_split(Xc, yc, test_size=0.3, random_state=SEED, stratify=yc)

    mc, sc = stats(Xtr)                      # CIC-train frame (reference distribution)
    mu, su = stats(Xu)                       # UNSW's own frame (per-dataset alignment for the RF)

    rf = fit(z(Xtr, mc, sc), ytr)            # detector: trained CIC-aligned (paper's method)
    iso = IsolationForest(random_state=SEED).fit(z(Xtr, mc, sc))  # drift model on CIC-train

    # Pool held-out CIC (should be low-drift, reliable) + UNSW (high-drift, unreliable).
    frames = []
    for name, X, y, m, s in [("cic", Xte, yte, mc, sc), ("unsw", Xu, yu, mu, su)]:
        pred = rf.predict(z(X, m, s))        # RF sees each dataset in its own aligned frame
        drift = -iso.score_samples(z(X, mc, sc))   # drift measured in the CIC frame; higher = stranger
        frames.append(pd.DataFrame({"dataset": name, "wrong": (pred != y).astype(int), "drift": drift}))
    df = pd.concat(frames, ignore_index=True)

    auc = roc_auc_score(df["wrong"], df["drift"])
    print(f"AUC(drift predicts error) = {auc:.3f}   (0.5 = useless, 1.0 = perfect flag)\n")

    print("mean drift by dataset:")
    print(df.groupby("dataset")["drift"].mean().round(3).to_string(), "\n")

    df["bucket"] = pd.qcut(df["drift"], 4, labels=["low", "med", "high", "very high"])
    acc = (1 - df.groupby("bucket", observed=True)["wrong"].mean()).round(3)
    print("accuracy by drift bucket (reliable when drift is low):")
    print(acc.to_string())

    # Operating point: flag the top-drift quartile as "distrust"; report what it buys.
    thr = df["drift"].quantile(0.75)
    trusted = df[df["drift"] <= thr]
    trusted_acc = 1 - trusted["wrong"].mean()
    print(f"\nif we distrust the top 25% drift: trusted accuracy = {trusted_acc:.3f} "
          f"on {len(trusted)/len(df):.0%} of traffic")

    RES.mkdir(exist_ok=True)
    pd.DataFrame({"metric": ["auc_drift_vs_error", "trusted_acc_at_75pct_coverage"],
                  "value": [round(auc, 3), round(trusted_acc, 3)]}).to_csv(RES / "reliability.csv", index=False)
    acc.plot.bar(color="#2c7fb8", figsize=(6, 4), rot=0)
    plt.ylabel("accuracy"); plt.xlabel("drift level")
    plt.title(f"Detector accuracy vs. drift (AUC={auc:.2f})"); plt.ylim(0, 1)
    plt.tight_layout(); plt.savefig(RES / "reliability.png", dpi=120); plt.close()
    print(f"\nwrote {RES}/reliability.csv, reliability.png")
    return df


if __name__ == "__main__":
    run()
