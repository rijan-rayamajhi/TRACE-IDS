# TRACE-IDS — Work Plan

Solo, no GPU. **Core = Phases 0–3, 6–7** (answers RQ1) — this is what carries the LOR.
Phases 4–5 (RQ2/RQ3) are **stretch**, touched only after the core result is written up.

> **Status (FINAL — NetFlow v3):** NF-CICIDS2018-v3 (~2M used) + NF-UNSW-NB15-v3 (~2.2M), 47 shared
> features. Zero-shot cross-dataset transfer FAILS (recall 0.00); alignment, balanced weights, and
> invariant selection do not fix it. Few-shot recovery works: 5 labeled/class → 0.88 recall, 10 →
> 0.93, 50 → 0.99. Reliability flag tried but FAILED on this data (AUC 0.40) → dropped from paper.
> Paper rewritten + humanized around zero-shot-fails / few-shot-recovers. Remaining: outreach.

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

---

# Path to LOR + Funded MS/PhD (ponytail-ordered: leverage ÷ effort)

Goal is not a grade. It is a professor who wants you in their lab (RA funding = their grant)
and a citable result. Ordered so the cheapest high-leverage moves go first.

## Step 1 — Email Dr. Glisson NOW (cost: ~0, leverage: highest)
- [ ] Send the current PDF + a 5-line note: your result, that it aligns with his work, and a
      direct ask about RA/PhD openings. Do NOT wait for a perfect paper — outreach is the
      bottleneck for funding, not code. Mention you are extending it (Steps 3–4).

## Step 2 — Reliability flag / RQ2 (cost: ~1 day, reuses current data)
- [ ] Drift score: distance of UNSW flows from CIC training distribution
- [ ] Show the score predicts WHERE the detector is wrong (flag vs error correlation)
- [ ] Output = verdict + "trust/distrust" flag. Practical, less-obvious than normalization.

## Step 3 — Larger feature set / rescue RQ1 (cost: ~1 week, the publishable lever)
- [ ] Download NF-CIC-IDS2017 + NF-UNSW-NB15 (NetFlow-standardized, ~40 shared features)
- [ ] Re-run alignment + invariant selection with many features (selection can finally help/fail
      meaningfully) — this is what makes the study novel and defensible
- [ ] Update results table + figures

## Step 4 — Publish (cost: ~1 day, citable)
- [ ] Fold Steps 2–3 into report.tex
- [ ] Put on arXiv (cs.CR / cs.LG) — a preprint is citable and signals productivity
- [ ] Link the arXiv + GitHub in your SOP and outreach

## Step 5 — Broaden outreach (cost: low, parallel)
- [ ] Same sharp email to 3–5 more professors whose FUNDED research matches (cross-dataset ML,
      NIDS, domain adaptation). Funding = fit with an active grant.

Reality check: this improves odds, it does not guarantee funding. The combination that works is
a professor advocate + a preprint + strong SOP/LORs. Steps 1 and 3 move the needle most.
