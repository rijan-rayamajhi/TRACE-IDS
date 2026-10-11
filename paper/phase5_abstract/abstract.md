## Abstract

### English Abstract

Machine-learning network intrusion detectors fail when moved to a new network, and recent work reports that fine-tuning a source-trained model on a few labelled target flows restores detection. These studies credit the recovery to transfer without training on the same target labels alone. We test this assumption on the four NetFlow v3 benchmarks (NF-CICIDS2018, NF-UNSW-NB15, NF-ToN-IoT and NF-BoT-IoT). We use a leak-free protocol: 12 directed dataset pairs, random forest, gradient-boosted tree and neural-network models, and pooled, importance-weighted and fine-tuned adaptation, each compared with target-only training over 10 seeds with paired Wilcoxon tests. Across 540 comparisons, the source helps in 6% and hurts in 28%, with the largest losses at 5–10 labelled flows per class. Under a shared scaling of both domains the figures are 8% and 38%. Zero-shot transfer is weak and pair-dependent, and a published zero-shot F1 of 0.81 does not reproduce on v3. At a 5% label budget, target-only training matches fine-tuning. A domain classifier separates every pair of networks with AUC of at least 0.996, even within the same attack category. On raw features, 23–40 of 45 features must be removed before this falls below 0.9, so the separation is not a single artifact. Per-domain feature scaling adds a further, hidden confound. We recommend that cross-dataset studies always report target-only training at the same label budget.

**Keywords:** network intrusion detection; transfer learning; few-shot learning; cross-dataset generalization; negative transfer; NetFlow; shortcut learning

### Abstract Quality Report

| Check | Result |
|---|---|
| Regime | Standard paper, EN-only: 150–250 words, 5–7 keywords (`references/abstract_writing_guide.md`) |
| Length | 219 words (ARS markers removed; whitespace split) |
| Keywords | 7 |
| Structure | Background (sentences 1–2) → purpose (3) → method (4) → results (5–10) → conclusion (11) |
| Body alignment | Every figure appears in the draft body, and every figure traces to `phase3_argument/facts.md`: 540 tests; 6%/28%; 8%/38%; 0.81 → no reproduction; 5% budget; AUC ≥ 0.996; 23–40 of 45; <0.9 |
| Hedges | No novelty claim in the abstract, so no protected hedge is needed. "No consistent benefit" wording is preserved in substance ("helps in 6% and hurts in 28%"). |
| Acronyms | AUC appears once without expansion; it is standard in the field and is expanded at first use in the body. Venue style may require expanding it; the formatter will check. |
