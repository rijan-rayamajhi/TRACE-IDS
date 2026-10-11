"""E4 — two checks raised by the gap analysis (research/gap_check_3w.md).

A. zeroshot — Atif & Ali (arXiv 2609.13511) report zero-shot UNSW->CIC F1 0.81 on NetFlow v2 after a
   staged feature ablation. We reconstruct their feature sets on v3 and test zero-shot transfer on
   BOTH a balanced 50/50 test set (their protocol) and a natural-base-rate test set (ours).
   Their column lists aren't given exactly; reconstruction from their description (Sec. III-C):
     A   = all minus TTL fields                       (MIN_TTL, MAX_TTL, DNS_TTL_ANSWER)
     B   = A minus packet-length fields               (LONGEST/SHORTEST_FLOW_PKT, MIN/MAX_IP_PKT_LEN)
     C   = B minus SERVER_TCP_FLAGS, TCP_WIN_MAX_IN, TCP_WIN_MAX_OUT
     Cv2 = C minus the v3-only inter-arrival-time fields (to match their v2 schema)

B. budget — TAN-IDS (PLOS ONE 2026, e0346801) fine-tunes with 5% of the target training split
   (= 3.5% of the target with their 70/15/15 split) and concludes source-aware training helps, without
   a target-only baseline. We run target-only vs pooled vs fine-tune at that budget.

Both: leak-free protocol as in E1/E2, 10 seeds, CIC<->UNSW (the pair both papers use).

    python src/e4_checks.py zeroshot
    python src/e4_checks.py budget
    python src/e4_checks.py all

Writes results/e4_zeroshot_{runs,summary}.csv and results/e4_budget_{runs,summary}.csv.
"""
from __future__ import annotations
import sys, time
import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import train_test_split
from common import load, stats, z, pair_stats, SCALING_TAG, stratified_sample, domain_class_weights, scores, summarize, SEEDS, RES
from e2_transfer import pretrain, finetune, fit_weighted, rf, gbt

DIRECTIONS = [("cic", "unsw"), ("unsw", "cic")]
SOURCE_N, TEST_N = 100_000, 200_000

TTL_F = ["MIN_TTL", "MAX_TTL", "DNS_TTL_ANSWER"]
PKTLEN_F = ["LONGEST_FLOW_PKT", "SHORTEST_FLOW_PKT", "MIN_IP_PKT_LEN", "MAX_IP_PKT_LEN"]
TCP_F = ["SERVER_TCP_FLAGS", "TCP_WIN_MAX_IN", "TCP_WIN_MAX_OUT"]
IAT_F = [f"{d}_IAT_{s}" for d in ("SRC_TO_DST", "DST_TO_SRC") for s in ("MIN", "MAX", "AVG", "STDDEV")]
FEATURE_SETS = {"all": [], "A": TTL_F, "B": TTL_F + PKTLEN_F, "C": TTL_F + PKTLEN_F + TCP_F,
                "Cv2": TTL_F + PKTLEN_F + TCP_F + IAT_F}


def split_target(Xt, yt, seed):
    Xpool, Xtest, ypool, ytest = train_test_split(Xt, yt, test_size=0.5, random_state=seed, stratify=yt)
    return Xpool, ypool, Xtest, ytest


def balanced_index(y, per_class, seed):
    n = min(per_class, y.value_counts().min())
    return y.groupby(y, group_keys=False).apply(lambda g: g.sample(n, random_state=seed)).index


def run_zeroshot(data):
    rows = []
    for src, tgt in DIRECTIONS:
        (Xs, ys), (Xt, yt) = data[src], data[tgt]
        for seed in SEEDS:
            t = time.time()
            si = stratified_sample(ys, SOURCE_N, seed)
            Xpool, _, Xtest, ytest = split_target(Xt, yt, seed)
            tests = {"natural": stratified_sample(ytest, TEST_N, seed),
                     "balanced": balanced_index(ytest, 50_000, seed)}
            ms, ss = stats(Xs.loc[si]); mp, sp = stats(Xpool)
            frames = {"zscore": (z(Xs.loc[si], ms, ss), z(Xtest, mp, sp)),
                      "raw": (Xs.loc[si], Xtest)}
            w = domain_class_weights(np.zeros(len(si)), ys.loc[si].to_numpy())
            for scaling, (Xsrc, Xte) in frames.items():
                for fs, drop in FEATURE_SETS.items():
                    cols = [c for c in Xsrc.columns if c not in drop]
                    for model, make in (("RF", rf), ("GBT", gbt)):
                        m = make(seed).fit(Xsrc[cols], ys.loc[si], sample_weight=w)
                        for test, ti in tests.items():
                            pred = m.predict(Xte.loc[ti, cols])
                            rows.append({"direction": f"{src}->{tgt}", "seed": seed, "scaling": scaling,
                                         "features": fs, "n_features": len(cols), "model": model,
                                         "test": test, "bal_acc": balanced_accuracy_score(ytest.loc[ti], pred),
                                         **scores(ytest.loc[ti], pred)})
            print(f"zeroshot {src}->{tgt} seed {seed} done in {time.time() - t:.0f}s", flush=True)
    runs = pd.DataFrame(rows)
    runs.to_csv(RES / "e4_zeroshot_runs.csv", index=False)
    summ = summarize(runs, ["direction", "scaling", "features", "model", "test"],
                     ("f1", "recall", "fpr", "bal_acc"))
    summ.to_csv(RES / "e4_zeroshot_summary.csv", index=False)
    print("\nzero-shot F1 (mean over seeds), z-scored:\n",
          summ[summ.scaling == "zscore"].pivot_table(index=["direction", "model", "features"],
                                                     columns="test", values="f1_mean").round(3).to_string())
    print("\nzero-shot F1 (mean over seeds), raw:\n",
          summ[summ.scaling == "raw"].pivot_table(index=["direction", "model", "features"],
                                                  columns="test", values="f1_mean").round(3).to_string())


def run_budget(data, frac=0.035):
    rows = []
    for src, tgt in DIRECTIONS:
        (Xs, ys), (Xt, yt) = data[src], data[tgt]
        n_lab = int(len(yt) * frac)
        for seed in SEEDS:
            t = time.time()
            si = stratified_sample(ys, SOURCE_N, seed)
            Xpool, ypool, Xtest, ytest = split_target(Xt, yt, seed)
            ti = stratified_sample(ytest, TEST_N, seed)
            (ms, ss), (mp, sp) = pair_stats(Xs.loc[si], Xpool); Xsrc, ysrc = z(Xs.loc[si], ms, ss), ys.loc[si]
            Xte = z(Xtest.loc[ti], mp, sp); yte = ytest.loc[ti]
            li = stratified_sample(ypool, n_lab, seed)        # stratified, like TAN-IDS
            Xk, yk = z(Xpool.loc[li], mp, sp), ypool.loc[li]
            Xmix, ymix = pd.concat([Xsrc, Xk]), pd.concat([ysrc, yk])
            dom = np.r_[np.zeros(len(ysrc)), np.ones(len(yk))]
            for model in ("RF", "GBT", "MLP"):
                base = pretrain(model, Xsrc, ysrc, seed)
                fits = {"source-only": base,
                        "target-only": fit_weighted(model, Xk, yk,
                                                    domain_class_weights(np.ones(len(yk)), yk.to_numpy()), seed),
                        "pooled": fit_weighted(model, Xmix, ymix, domain_class_weights(dom, ymix.to_numpy()), seed),
                        "finetune": finetune(model, base, Xk, yk, seed)}
                for method, m in fits.items():
                    rows.append({"direction": f"{src}->{tgt}", "seed": seed, "model": model, "method": method,
                                 "n_target_labels": len(yk), **scores(yte, m.predict(Xte))})
            print(f"budget {src}->{tgt} seed {seed} done in {time.time() - t:.0f}s", flush=True)
    runs = pd.DataFrame(rows)
    runs.to_csv(RES / f"e4_budget_runs{SCALING_TAG}.csv", index=False)
    summ = summarize(runs, ["direction", "model", "method"])
    summ.to_csv(RES / f"e4_budget_summary{SCALING_TAG}.csv", index=False)
    print("\nF1 at the TAN-IDS budget (mean over seeds):\n",
          summ.pivot_table(index=["direction", "model"], columns="method", values="f1_mean").round(3).to_string())


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    RES.mkdir(exist_ok=True)
    data = {n: load(n) for n in ("cic", "unsw")}
    if what in ("zeroshot", "all"):
        run_zeroshot(data)
    if what in ("budget", "all"):
        run_budget(data)


if __name__ == "__main__":
    main()
