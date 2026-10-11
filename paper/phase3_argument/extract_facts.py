"""Print every number the paper uses, read from results/ (GUARDRAILS B1). Writes facts.md next to this file.

    .venv/bin/python paper/phase3_argument/extract_facts.py
"""
import warnings
from pathlib import Path
import pandas as pd

warnings.filterwarnings("ignore")
R, OUT = Path("results"), Path(__file__).with_name("facts.md")
L = []
p = lambda *a: L.append(" ".join(str(x) for x in a))

t = pd.read_csv(R / "dataset_table.csv")
p("## Table 1 datasets\n", t.drop(columns="categories").to_string(index=False))

e1 = pd.read_csv(R / "e1_summary.csv")
p("\n## E1 (RF, CIC<->UNSW) F1 mean±std by mode/features/k\n",
  e1.pivot_table(index=["direction", "features", "k"], columns="mode", values=["f1_mean"]).round(3).to_string())
p("\nE1 FPR at k=1:\n", e1[e1.k == 1].pivot_table(index=["direction", "features"], columns="mode", values="fpr_mean").round(3).to_string())

for tag, f in [("per-domain", "e3_significance.csv"), ("shared", "e3_significance_shared.csv")]:
    s = pd.read_csv(R / f)
    p(f"\n## E3 {tag}: {len(s)} tests", s.verdict.value_counts().to_dict(), "| Holm:", s.verdict_holm.value_counts().to_dict(),
      f"| median dF1 {s.delta_f1.median():.4f} mean {s.delta_f1.mean():.4f} | min p {s.p.min():.4f}")
    p("by method\n", pd.crosstab(s.method, s.verdict).to_string())
    p("by model\n", pd.crosstab(s.model, s.verdict).to_string())
    p("by k\n", pd.crosstab(s.k, s.verdict).to_string())
    p("by pair\n", pd.crosstab(s.direction, s.verdict).to_string())
    e2 = s[s.direction.isin(["cic->unsw", "unsw->cic"])]
    p(f"E2 subset (CIC<->UNSW, {len(e2)} tests):", e2.verdict.value_counts().to_dict())
    z = pd.read_csv(R / ("e3_zeroshot.csv" if tag == "per-domain" else "e3_zeroshot_shared.csv"))
    best = z.groupby("direction").bacc.max()
    p("zero-shot best bacc per pair\n", best.round(3).to_string())
    tb = pd.read_csv(R / ("e3_targetonly_bacc.csv" if tag == "per-domain" else "e3_targetonly_bacc_shared.csv"))
    p("target-only bacc (k=1,5,10)\n", tb.round(3).to_string(index=False))

zs = pd.read_csv(R / "e4_zeroshot_summary.csv")
p("\n## E4a Atif & Ali replication: best F1 / bal_acc per direction, features, test (max over scaling & model)\n",
  zs.groupby(["direction", "features", "test"])[["f1_mean", "bal_acc_mean"]].max().round(3).to_string())
b = pd.read_csv(R / "e4_budget_summary.csv")
p("\n## E4b TAN-IDS 5% budget F1\n", b.pivot_table(index=["direction", "model"], columns="method", values="f1_mean").round(4).to_string())

d = pd.read_csv(R / "e5_distance.csv")
m = d.groupby(["pair", "subset", "scaling"]).auc.mean().dropna()
p("\n## E5-B domain AUC (mean over seeds): min over pairs per subset/scaling\n", m.groupby(["subset", "scaling"]).min().round(4).to_string())
fam = pd.read_csv(R / "e5_families_summary.csv")
p("\n## E5-A families summary columns:", fam.columns.tolist(), "rows", len(fam))
imp = pd.read_csv(R / "e5_importance.csv").groupby("direction").importance_spearman.mean()
p("\n## E5 RF importance rank corr range:", round(imp.min(), 3), "-", round(imp.max(), 3))

ab = pd.read_csv(R / "e5_ablation_summary.csv")
cols = [c for c in ab.columns if c.startswith("removed_to")]
p("\n## Ablation: features removed before AUC < thr (mean over seeds), raw\n",
  ab[ab.scaling == "raw"].groupby(["subset", "pair"])[cols].mean().round(1).to_string())
p("raw range removed_to_<0.9:", ab[ab.scaling == "raw"].groupby(["subset", "pair"])["removed_to_<0.9"].mean().agg(["min", "max"]).round(1).to_dict())
st = pd.read_csv(R / "e5_ablation_steps.csv")
p("AUC after n removed (raw, mean over pairs&seeds)\n", st[(st.scaling == "raw") & st.n_removed.isin([0, 5, 10, 15, 20, 30])]
  .groupby(["subset", "n_removed"]).auc.mean().unstack(0).round(3).to_string())
sf = pd.read_csv(R / "e5_single_feature.csv")
p("\n## Single-feature AUC>=0.99: raw", int((sf.raw >= 0.99).sum()), "zscore", int((sf.zscore >= 0.99).sum()), "of", len(sf))
p("cic-unsw PROTOCOL:", sf[(sf.pair == "cic-unsw") & (sf.feature == "PROTOCOL")][["raw", "zscore"]].round(3).to_dict("records"))

OUT.write_text("\n".join(L) + "\n")
print(f"wrote {OUT} ({len(L)} blocks)")
