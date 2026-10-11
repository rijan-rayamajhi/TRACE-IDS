## Abstract

### English Abstract

Machine-learning network intrusion detectors fail when moved to a new network, and recent work reports that fine-tuning a source-trained model on a few labelled target flows restores detection. These studies do not train on the same target labels alone, so they cannot tell whether the recovery comes from the source. We test this on the four NetFlow v3 benchmarks (NF-CICIDS2018, NF-UNSW-NB15, NF-ToN-IoT and NF-BoT-IoT) with a leak-free protocol: 12 directed dataset pairs, random forest, gradient-boosted tree and neural-network models, and pooled, importance-weighted and fine-tuned adaptation, each compared with target-only training over 10 seeds with paired Wilcoxon tests. Across 540 comparisons, the source significantly helps in 8% and hurts in 38% (uncorrected), and averaged over pairs it lowers F1 by 0.044 (95% CI −0.066 to −0.022). The direction holds on balanced accuracy and under per-domain scaling. Benefit is rare and pair-dependent. Zero-shot transfer is weak, a published zero-shot F1 of 0.81 does not reproduce on v3, and at a 5% label budget target-only training matches fine-tuning. A domain classifier separates every pair of networks with AUC of at least 0.996 on raw features, even within the same attack category, against 0.50 for two halves of one dataset; 23–40 of 45 features must be removed before this falls below 0.9. Removing the documented TTL artifact does not change the conclusion. Per-domain feature scaling makes even halves of one dataset separable. Cross-dataset studies should report target-only training at the same label budget.

**Keywords:** network intrusion detection; transfer learning; few-shot learning; cross-dataset generalization; negative transfer; NetFlow; shortcut learning

### Abstract Quality Report

| Check | Result |
|---|---|
| Regime | Standard paper, EN-only: 150–250 words, 5–7 keywords (`references/abstract_writing_guide.md`) |
| Length | 241 words (ARS markers removed; whitespace split) — revision round 1 |
| Keywords | 7 |
| Structure | Background (sentences 1–2) → purpose (3) → method (4) → results (5–10) → conclusion (11) |
| Body alignment | Every figure appears in the draft body and traces to `phase3_argument/facts.md`: 540 tests; 8%/38%; −0.044 [−0.066, −0.022]; 0.81 → no reproduction; 5% budget; AUC ≥ 0.996; control 0.50; 23–40 of 45; <0.9 |
| Hedges | No novelty claim in the abstract. Verdicts are labelled "uncorrected" (review Finding 20); the TTL counter-result is stated (Finding 1). |
| Acronyms | AUC appears once without expansion; it is standard in the field and is expanded at first use in the body. Venue style may require expanding it; the formatter will check. |
