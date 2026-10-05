# TRACE-IDS — Work Plan

Solo, no GPU. **Core = Phases 0–3, 6–7** (answers RQ1) — this is what carries the LOR.
Phases 4–5 (RQ2/RQ3) are **stretch**, touched only after the core result is written up.

> **Status (real data):** CIC-IDS2017 (2.83M rows) + UNSW-NB15 (258k) built. Finding: per-dataset
> normalization recovers cross-dataset attack detection (F1 0.00→0.51, gap 0.62→0.41); invariant-
> feature *selection* does NOT help on the 5-feature common set (every feature carries signal).
> Open decision: reframe contribution around alignment, or expand to a larger common feature set.

## Phase 0 — Setup
- [x] venv + `pip install -r requirements.txt` (pyarrow added for parquet)
- [ ] Download CIC-IDS2017 and UNSW-NB15 into `data/raw/`  ← **blocking next real step**
- [ ] `git init` (deferred by choice); `.gitignore` done

## Phase 1 — Data prep & common-feature mapping  *(code done; verified on synthetic data)*
- [x] Load + inspect columns (`src/data_loader.py inspect`)
- [x] Map shared features to unified schema (`CIC_MAP`/`UNSW_MAP` — VERIFY vs real columns)
- [x] Clean: NaN/inf drop, binary label + subtype (scaling deferred to train split — no leakage)
- [x] Save unified data to `data/processed/*.parquet`

## Phase 2 — Baseline detectors  *(code done; verified on synthetic data)*
- [x] Train Random Forest on CIC (`src/baseline.py`)
- [x] Same-dataset vs cross-dataset test → prints the generalization gap

## Phase 3 — Contribution 1: Explanation-guided feature selection  → RQ1  *(code done; verified)*
- [x] SHAP importance per dataset (`src/invariant.py`)
- [x] Pick domain-invariant features: important in both **AND same effect direction in both**
      (magnitude alone kept a spurious direction-flipped feature — directional test added)
- [x] Retrain on invariant features, re-run cross-dataset test, compare gap

## Phase 4 — Contribution 2: Reliability flag  → RQ2  *(STRETCH — after core is written up)*
- [ ] Lightweight drift monitor (per-feature distance or Isolation Forest on inputs)
- [ ] Test: does high drift score predict wrong verdicts?
- [ ] Output = verdict + confidence + reliability flag

## Phase 5 — Contribution 3: Unsupervised / zero-day channel  → RQ3  *(STRETCH — after core is written up)*
- [ ] Add anomaly detector (Isolation Forest)
- [ ] Hold out one attack type from training entirely
- [ ] Measure recall on unseen attack vs FPR

## Phase 6 — Evaluation & figures
- [ ] Metrics table: precision/recall/F1/FPR, same- vs cross-dataset, per phase
- [ ] Figures: SHAP, generalization-gap bar chart, reliability-vs-error → `results/`

## Phase 7 — Write-up (Overleaf → PDF for Dr. Glisson)
- [ ] Open `report/report.tex` in Overleaf (New Project → Upload Project, or paste the file)
- [ ] It uses the standard IEEE two-column format: Abstract, Introduction, Related Work,
      Method, Results & Discussion, Conclusion, References
- [ ] Fill each section; **paste only numbers printed by committed code** (GUARDRAILS B1)
- [ ] Drop `results/` figures into `report/figures/`, reference them
- [ ] Verify every citation link actually opens before compiling (GUARDRAILS B3)
- [ ] Compile to PDF in Overleaf → download
- [ ] Email the PDF to Dr. Glisson for review; push repo to GitHub; keep the LOR one-pager ready

## Research questions (reframed — contribution is ALIGNMENT)
- **RQ1** — Does per-dataset feature-distribution alignment reduce the cross-dataset gap? **(yes:
  gap 0.62→0.41, cross F1 0.00→0.51 — `results/metrics.csv`)**
- **RQ2** — Does explanation-guided invariant-feature selection further reduce it? **(no — hurts on
  the 5-feature common set; stated as a negative result + future work: larger feature space)**
- **Stretch** — reliability flag vs. error; unsupervised channel on unseen attacks.
