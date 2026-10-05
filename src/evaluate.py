"""Phase 6: produce the reportable metrics table + figures into results/.

Every number in the report comes from here (GUARDRAILS B1/B2). Three configs tell the
whole story: no alignment collapses, per-dataset alignment recovers detection, and
explanation-guided selection does not add value on the minimal common feature set.

    python src/evaluate.py
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from baseline import scaled_splits, fit, scores
from invariant import select

RES = Path("results")


def evaluate(cols, normalize) -> dict:
    (Xtr, ytr), (Xte, yte), (Xu, yu) = scaled_splits(cols, normalize=normalize)
    m = fit(Xtr, ytr)
    s, c = scores(yte, m.predict(Xte)), scores(yu, m.predict(Xu))
    return {"same_acc": s["acc"], "cross_acc": c["acc"], "cross_f1": c["f1"], "gap": s["acc"] - c["acc"]}


def main():
    RES.mkdir(exist_ok=True)
    inv, keep = select()
    configs = {
        "no alignment (raw)": (None, False),
        "per-dataset alignment": (None, True),
        "alignment + invariant selection": (keep, True),
    }
    tbl = pd.DataFrame({k: evaluate(cols, norm) for k, (cols, norm) in configs.items()}).T.round(3)
    tbl.to_csv(RES / "metrics.csv")
    print(f"invariant features selected: {keep}\n")
    print(tbl.to_string())

    tbl["gap"].plot.bar(color="#c0392b", figsize=(6, 4), rot=15)
    plt.ylabel("generalization gap (acc)"); plt.title("Cross-dataset generalization gap")
    plt.tight_layout(); plt.savefig(RES / "gap.png", dpi=120); plt.close()

    inv[["cic", "unsw"]].plot.bar(figsize=(6, 4), rot=20)
    plt.ylabel("mean |SHAP| (normalized)"); plt.title("Feature importance per dataset")
    plt.tight_layout(); plt.savefig(RES / "shap_importance.png", dpi=120); plt.close()

    print(f"\nwrote {RES}/metrics.csv, gap.png, shap_importance.png")


if __name__ == "__main__":
    main()
