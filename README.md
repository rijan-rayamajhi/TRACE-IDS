# TRACE-IDS
**Transferable, Reliability-Aware, Cross-dataset Explainable Intrusion Detection System**

ML-based network intrusion detection built to survive the *cross-dataset generalization gap* —
detectors that score >99% on their training dataset but drop below 40% on a different network.

## Problem

ML-NIDS over-report single-dataset accuracy. A detector scoring 0.98 on CIC-IDS2017 detects
**zero** attacks on UNSW-NB15 (predicts all-benign) because the datasets' raw feature scales
differ. TRACE-IDS shows that **per-dataset feature-distribution alignment**, not invariant-feature
selection, is what restores cross-dataset detection.

## Contributions (what's unique)

1. **Feature-distribution alignment.** Per-dataset z-score normalization that recovers
   cross-dataset attack detection — on real data it lifts cross-dataset F1 from 0.00 to 0.51
   and cuts the accuracy gap from 0.62 to 0.41, where a raw model detects nothing.
2. **Honest cross-dataset evaluation of feature selection.** Using cross-dataset SHAP importance
   + an effect-direction test, we show explanation-guided *invariant-feature selection* does NOT
   help on a minimal common feature set (every shared feature carries signal) — a negative result
   that reframes where the leverage actually is.

Stretch (after the core is written up): reliability/drift flag; unsupervised zero-day channel.

## Research questions

- RQ1: Does per-dataset feature-distribution alignment reduce the cross-dataset generalization gap?
- RQ2: Does explanation-guided invariant-feature selection further reduce it, or not?
- Stretch: reliability flag vs. error; unsupervised channel on unseen attacks.

## Datasets (not committed — download into `data/raw/`)

- CIC-IDS2017 — https://www.unb.ca/cic/datasets/ids-2017.html
- UNSW-NB15  — https://research.unsw.edu.au/projects/unsw-nb15-dataset

## Layout

```
data/raw/        downloaded datasets (gitignored)
data/processed/  cleaned, common-feature-mapped parquet/csv
notebooks/       exploration + experiments
src/             data loading, feature selection, models, evaluation
results/         metrics, SHAP figures
```

## Setup

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Scope

Offline/batch, single machine, no GPU. Real-time capture and adversarial-evasion robustness are
out of scope (future work).
