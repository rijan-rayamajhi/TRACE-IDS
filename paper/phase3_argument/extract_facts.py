"""Print every number the paper uses, read from results/ (GUARDRAILS B1). Writes facts.md next to this file.

    .venv/bin/python paper/phase3_argument/extract_facts.py
"""
import warnings
from pathlib import Path
import numpy as np
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
    p("median dF1 by k:", s.groupby("k").delta_f1.median().round(4).to_dict())
    e2 = s[s.direction.isin(["cic->unsw", "unsw->cic"])]
    p(f"E2 subset (CIC<->UNSW, {len(e2)} tests):", e2.verdict.value_counts().to_dict())
    z = pd.read_csv(R / ("e3_zeroshot.csv" if tag == "per-domain" else "e3_zeroshot_shared.csv"))
    p("zero-shot per pair/model (f1, recall, fpr, bacc)\n", z.round(3).to_string(index=False))
    best = z.groupby("direction").bacc.max()
    p("zero-shot best bacc per pair\n", best.round(3).to_string())
    tb = pd.read_csv(R / ("e3_targetonly_bacc.csv" if tag == "per-domain" else "e3_targetonly_bacc_shared.csv"))
    p("target-only bacc (k=1,5,10)\n", tb.round(3).to_string(index=False))

for tag, f in [("per-domain", "e2_runs_all.csv"), ("shared", "e2_runs_all_shared.csv")]:
    ess = pd.read_csv(R / f).groupby("direction").iw_ess.mean()
    p(f"\n## IW effective sample size (fraction of source), {tag}: min {ess.min():.4f} max {ess.max():.4f} median {ess.median():.4f}")
zs = pd.read_csv(R / "e4_zeroshot_summary.csv")
p("\n## E4a Atif & Ali replication: best F1 / bal_acc per direction, features, test (max over scaling & model)\n",
  zs.groupby(["direction", "features", "test"])[["f1_mean", "bal_acc_mean"]].max().round(3).to_string())
for btag, bfile in [("per-domain", "e4_budget_summary.csv"), ("shared", "e4_budget_summary_shared.csv")]:
    b = pd.read_csv(R / bfile)
    p(f"\n## E4b TAN-IDS 5% budget F1 ({btag})\n", b.pivot_table(index=["direction", "model"], columns="method", values="f1_mean").round(4).to_string())
p("E4b target labels per run (shared):", pd.read_csv(R / "e4_budget_runs_shared.csv").groupby("direction").n_target_labels.first().to_dict())

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
f5 = st[(st.scaling == "raw") & (st.n_removed < 5)].groupby(["pair", "seed", "subset"]).next_removed
p("Runs with MIN_TTL or MAX_TTL among first 5 removed (raw):", int(f5.apply(lambda x: bool({"MIN_TTL", "MAX_TTL"} & set(x))).sum()),
  "of", f5.ngroups)
sf = pd.read_csv(R / "e5_single_feature.csv")
p("\n## Single-feature AUC>=0.99: raw", int((sf.raw >= 0.99).sum()), "zscore", int((sf.zscore >= 0.99).sum()), "of", len(sf))
p("cic-unsw PROTOCOL:", sf[(sf.pair == "cic-unsw") & (sf.feature == "PROTOCOL")][["raw", "zscore"]].round(3).to_dict("records"))

OUT.write_text("\n".join(L) + "\n")
print(f"wrote {OUT} ({len(L)} blocks)")

# ---- revision round 1 (review findings 3, 4, 9, 12): verdicts by k / by pair, BH, E6 robustness


def bh(pv, q=0.05):
    """Benjamini-Hochberg step-up: boolean rejections at FDR q."""
    pv = np.asarray(pv); o = np.argsort(pv); m = len(pv)
    ok = pv[o] <= q * np.arange(1, m + 1) / m
    r = np.zeros(m, bool)
    if ok.any():
        r[o[: np.max(np.nonzero(ok)) + 1]] = True
    return r

for tag, f in [("per-domain", "e3_significance.csv"), ("shared", "e3_significance_shared.csv")]:
    s = pd.read_csv(R / f)
    p(f"\n## Verdicts by k, {tag}\n", s.groupby("k").verdict.value_counts().unstack(fill_value=0).to_string())
    bp = s.groupby("direction").verdict.value_counts().unstack(fill_value=0)
    bp["net"] = bp.get("help", 0) - bp.get("hurt", 0)
    p(f"verdicts by pair (sorted by net), {tag}\n", bp.sort_values("net", ascending=False).to_string())
    for d in ("unsw->bot", "bot->cic"):
        p(f"{d} helps at k, {tag}:", s[(s.direction == d) & (s.verdict == "help")].k.value_counts().sort_index().to_dict(),
          "hurts at k:", s[(s.direction == d) & (s.verdict == "hurt")].k.value_counts().sort_index().to_dict())
    rej = bh(s.p)
    p(f"Benjamini-Hochberg (q=0.05) rejections, {tag}:", int(rej.sum()), "help", int((rej & (s.delta_f1 > 0)).sum()),
      "hurt", int((rej & (s.delta_f1 < 0)).sum()))
pe = pd.read_csv(R / "e6_pooled_effect.csv")
p("\n## E6 pooled mean delta over pairs, pair-bootstrap 95% CI\n", pe.round(4).to_string(index=False))
vm = pd.read_csv(R / "e6_verdicts_by_metric.csv")
p("\n## E6 verdicts by metric\n", vm.groupby(["scaling", "metric"]).verdict.value_counts().unstack(fill_value=0).to_string())
bb = vm[(vm.metric == "bacc") & vm.direction.str.endswith("->bot")]
p("BoT-target cells, bacc\n", bb.groupby("scaling").verdict.value_counts().unstack(fill_value=0).to_string())
ct = pd.read_csv(R / "e6_domain_control.csv")
p("\n## E6 within-dataset domain AUC control (two random halves), mean over seeds\n",
  ct.groupby(["dataset", "scaling"]).auc.mean().unstack().round(4).to_string())
from scipy.stats import wilcoxon  # noqa: E402
for e1tag, e1file in [("per-domain", "e1_runs.csv"), ("shared", "e1_runs_shared.csv")]:
  e1 = pd.read_csv(R / e1file)
  rows = []
  for (d, feat, k), g in e1[e1.k.between(1, 100)].groupby(["direction", "features", "k"]):
      t = g[g["mode"] == "target-only"].set_index("seed").f1
      for m in ("source+k", "source+k-weighted"):
          diff = g[g["mode"] == m].set_index("seed").f1 - t
          rows.append({"direction": d, "features": feat, "k": k, "mode": m, "delta": round(diff.mean(), 3),
                       "seeds_pos": int((diff > 0).sum()), "p": round(wilcoxon(diff).pvalue, 3)})
  p(f"\n## E1 ({e1tag}) paired source-vs-target-only, F1 (Wilcoxon over 10 seeds), all features vs -TTL\n",
    pd.DataFrame(rows).to_string(index=False))
  p(f"E1 ({e1tag}) mean F1 by direction/features/mode, k=1..10\n", e1[e1.k.between(1, 10)].pivot_table(
    index=["direction", "k"], columns=["features", "mode"], values="f1").round(3).to_string())
  OUT.write_text("\n".join(L) + "\n")
  print(f"wrote {OUT} ({len(L)} blocks)")
nt = vm[(vm.scaling == "no-TTL (shared)") & (vm.metric == "f1")].groupby("direction").verdict.value_counts().unstack(fill_value=0)
nt["net"] = nt.get("help", 0) - nt.get("hurt", 0)
p("\n## No-TTL (shared) F1 verdicts by pair\n", nt.sort_values("net", ascending=False).to_string())
OUT.write_text("\n".join(L) + "\n")
