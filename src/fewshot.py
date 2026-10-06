"""Phase RQ3: few-shot recovery. Zero-shot cross-dataset transfer fails (recall ~0).
How little labeled target data brings detection back?

Protocol: train on source (CIC), then add k labeled samples PER CLASS from the target (UNSW)
and retrain. Evaluate on a held-out target test set as k grows. k=0 is zero-shot.
Both datasets are z-scored by their own stats so they share a comparable space.

    python src/fewshot.py

Free / laptop-only: source is subsampled for speed; the curve is what matters, not absolute scale.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from baseline import load, stats, z, fit, scores, SEED

RES = Path("results")
SOURCE_N = 150_000                       # subsample source for speed (free/laptop)
K_VALUES = [0, 1, 5, 10, 50, 100, 500]   # labeled target samples per class


def run():
    Xc, yc = load("cic")
    Xu, yu = load("unsw")
    mc, sc = stats(Xc); Xc = z(Xc, mc, sc)      # align each dataset by its own stats
    mu, su = stats(Xu); Xu = z(Xu, mu, su)
    if len(Xc) > SOURCE_N:
        Xc = Xc.sample(SOURCE_N, random_state=SEED); yc = yc.loc[Xc.index]

    # split target into a pool (to draw few-shot examples) and a fixed held-out test set
    Xpool, Xtest, ypool, ytest = train_test_split(Xu, yu, test_size=0.5, random_state=SEED, stratify=yu)
    atk = ypool.index[ypool == 1].to_numpy()
    ben = ypool.index[ypool == 0].to_numpy()
    rng = np.random.default_rng(SEED)

    rows = []
    for k in K_VALUES:
        if k == 0:
            Xtr, ytr = Xc, yc
        else:
            idx = np.concatenate([rng.choice(atk, min(k, len(atk)), replace=False),
                                  rng.choice(ben, min(k, len(ben)), replace=False)])
            Xtr = pd.concat([Xc, Xpool.loc[idx]])
            ytr = pd.concat([yc, ypool.loc[idx]])
        s = scores(ytest, fit(Xtr, ytr).predict(Xtest))
        rows.append({"k_per_class": k, "recall": s["recall"], "f1": s["f1"], "acc": s["acc"]})
        print(f"k={k:<4} recall={s['recall']:.3f}  f1={s['f1']:.3f}  acc={s['acc']:.3f}")

    df = pd.DataFrame(rows)
    RES.mkdir(exist_ok=True)
    df.to_csv(RES / "fewshot.csv", index=False)
    plt.figure(figsize=(6, 4))
    plt.plot(df["k_per_class"], df["recall"], "o-", label="recall (attack detection)")
    plt.plot(df["k_per_class"], df["f1"], "s--", label="F1")
    plt.xlabel("labeled target samples per class (k)"); plt.ylabel("score"); plt.ylim(0, 1)
    plt.title("Few-shot recovery: CIC-2018 -> UNSW-NB15"); plt.legend(); plt.grid(alpha=0.3)
    plt.tight_layout(); plt.savefig(RES / "fewshot.png", dpi=120); plt.close()
    print(f"\nwrote {RES}/fewshot.csv, fewshot.png")
    return df


if __name__ == "__main__":
    run()
