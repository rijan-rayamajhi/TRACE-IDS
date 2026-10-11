# TRACE-IDS

**Does source data help few-shot cross-dataset intrusion detection?** A leak-free, multi-seed study
on the four NetFlow v3 datasets (NF-CICIDS2018-v3, NF-UNSW-NB15-v3, NF-ToN-IoT-v3, NF-BoT-IoT-v3).

> **Status (2026-10-11): experiments complete, paper in preparation.** Plan and full results log:
> [`PUBLICATION_PLAN.md`](PUBLICATION_PLAN.md).
>
> **The earlier version of this project is withdrawn.** Its headline ("per-dataset z-score alignment
> lifts cross-dataset F1 from 0.00 to 0.51"), the few-shot numbers in `report/report.tex`, and
> `report/TRACE-IDS.pdf` are invalid: the old loader dropped 28% of UNSW-NB15 attacks, normalization
> leaked target-test statistics, and results came from a single seed. Per-domain z-scoring is now a
> known *confound* (see finding 4), not a contribution.

## Question

When a detector trained on one network is moved to another and a few target flows get labelled
(k per class), does the **source** dataset add anything over training on those k target flows alone?

## Findings

Every number below is printed by committed code into `results/` (see [Reproduce](#reproduce)).
10 seeds per setting; paired two-sided Wilcoxon over seeds; F1 on a held-out target test split.

1. **Source data gives no consistent benefit, and often hurts.** All 12 directed dataset pairs ×
   {RF, gradient-boosted trees, MLP} × {pooled, importance-weighted, fine-tuned} × k ∈ {1, 5, 10, 50, 100}
   = 540 comparisons against target-only. Shared scaling (main setting): source helps in 41 (8%),
   no difference in 294 (54%), hurts in 205 (38%); median ΔF1 −0.025
   (`results/e3_significance_shared.csv`). Per-domain scaling: 34 / 353 / 153
   (`results/e3_significance.csv`; its CIC↔UNSW rows are the 90 E2 tests: 0 / 65 / 25). No single
   comparison can survive Holm correction over 540 with 10 seeds, so the main estimate is pooled: averaged
   over the 12 pairs the source lowers F1 by 0.044 (95% pair-bootstrap CI −0.066 to −0.022; per-domain
   −0.038, CI −0.064 to −0.017). On balanced accuracy: 35 helps / 214 hurts, mean −0.018
   (`results/e6_pooled_effect.csv`, `e6_verdicts_by_metric.csv`). Benefit is rare and pair-dependent:
   the best pair under shared scaling is UNSW→BoT (9 helps, 3 hurts).
2. **Zero-shot transfer is weak and pair-dependent.** Best-model balanced accuracy 0.61–0.71 on 5 of
   12 pairs (0.68–0.76 on 4 under shared scaling), about 0.5 on the rest; target-only with 10 labelled flows per class (0.78–0.94) beats the
   best zero-shot model on every pair (`results/e3_zeroshot_shared.csv`, `e3_targetonly_bacc_shared.csv`). A reported zero-shot F1 of 0.81 (Atif & Ali, NetFlow v2) does not reproduce on v3
   (their Set C: F1 0.21; balanced accuracy ≤ 0.55 for every feature set; `results/e4_zeroshot_summary.csv`). At TAN-IDS's 5% label budget, target-only matches
   pooled and fine-tuned models (`results/e4_budget_summary.csv`).
3. **Consistent with this, every network sits in its own region of feature space.** A domain classifier separates
   every pair with AUC ≥ 0.996, also within benign traffic and within the *same* attack category
   (`results/e5_distance.csv`). On raw features this is not one artifact column: 23–40 of the 45
   features must be removed (most-relied-on first; TTL is among the first five in 24 of 36 runs) before
   AUC falls below 0.9 (`results/e5_ablation_summary.csv`). Negative control: two random halves of one
   dataset give AUC 0.50 on raw features (`results/e6_domain_control.csv`). Without MIN_TTL/MAX_TTL,
   across all 12 pairs (shared scaling) the source does slightly worse: 42 helps / 228 hurts, mean ΔF1
   −0.056 (CI −0.080 to −0.030; `results/e2_runs_all_nottl_shared.csv`, `e6_pooled_effect.csv`), A per-domain
   RF check (CIC→UNSW, `results/e1_runs.csv`) favoured the source at k = 5 and 10 without TTL, but under
   shared scaling the same check shows the source worse (−0.263 F1 at k = 5, p = 0.002; `results/e1_runs_shared.csv`).
4. **Per-domain z-scoring is a confound.** Scaling each dataset by its own statistics maps the same
   code (e.g. `PROTOCOL` = 6, or an all-zero FTP column) to different values per dataset. Single
   features that alone separate two datasets with AUC ≥ 0.99: 13 of 270 (6 pairs × 45) on raw values,
   231 after per-domain z-scoring (`results/e5_single_feature.csv`). Even two halves of the *same*
   dataset, each z-scored on its own, separate with AUC 1.00 (`results/e6_domain_control.csv`). With one shared scaling the
   transfer result holds and strengthens, and the one pair where the source seemed to help
   (ToN→CIC: 9 helps → 0, 18 hurts) turns out to be a scaling artifact.

## Data (not committed)

Download the four NetFlow v3 CSVs from the
[UQ NIDS datasets page](https://staff.itee.uq.edu.au/marius/NIDS_datasets/) and place (or symlink)
them as:

```
data/raw/cic_NF-CICIDS2018-v3.csv
data/raw/unsw_NF-UNSW-NB15-v3.csv
data/raw/ton_NF-ToN-IoT-v3.csv
data/raw/bot_NF-BoT-IoT-v3.csv
```

`src/data_loader.py build` drops identifier columns (IPs, ports, timestamps, attack name) and two
sparse columns, keeps 45 flow features + binary label, and subsamples the large datasets to ~2M flows
(BoT-IoT keeps all benign flows).

## Reproduce

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # Python 3.9, pinned versions
./run_all.sh                 # every stage, ~10 h on an 8-core laptop (keep it on AC power)
./run_all.sh e3shared        # or one stage at a time: data e1 e2 e3 e3shared e4 e5 ablation
```

| Stage | Script | Question | Main outputs (`results/`) |
|---|---|---|---|
| data | `data_loader.py build`, `families` | unified parquet + attack-family sidecars | `data/processed/*.parquet` |
| e1 | `e1_fewshot.py` | CIC↔UNSW, RF: source+k vs target-only, ±TTL | `e1_summary.csv`, `e1_recovery.png` |
| e2 | `e2_transfer.py` | CIC↔UNSW, 3 models × 4 methods | `e2_summary.csv`, `e2_transfer.png` |
| e3 | `e2_transfer.py --out all`, `e3_analysis.py` | all 12 pairs, significance | `e3_significance.csv`, `e3_heatmap.png` |
| e3shared | same, `--scaling shared` / `--tag shared` | scaling-confound check | `e3_significance_shared.csv`, `e3_heatmap_shared.png` |
| e4 | `e4_checks.py all` | Atif & Ali zero-shot; TAN-IDS 5% budget | `e4_zeroshot_summary.csv`, `e4_budget_summary.csv` |
| e5 | `e5_mechanism.py all` | domain distance, per-attack-family recall | `e5_distance.csv`, `e5_families_summary.csv` |
| ablation | `e5_ablation.py` | is separability one column? | `e5_ablation_summary.csv`, `e5_ablation.png` |

Protocol (all stages, `src/common.py`): per seed the target is split 50/50 into an unlabelled pool
and a test set; normalization statistics come only from the source sample and the unlabelled pool;
few-shot draws are nested across k; seeds 0–9.

`baseline.py`, `fewshot.py`, `invariant.py`, `reliability.py`, `evaluate.py` belong to the withdrawn
earlier version and are kept only for history.

## Scope

Offline, batch, single machine, no GPU. Measured: binary flow classification on four public NetFlow v3
datasets. Not measured: real-time deployment, adversarial evasion, other feature sets or deep models
beyond a small MLP. A cross-dataset result on public testbeds is not a claim about real networks.
