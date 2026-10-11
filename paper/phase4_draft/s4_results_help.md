## 4. Results: Does the Source Help?

### 4.1 One pair, one model

We begin with the setting closest to prior work: a random forest transferred between NF-CICIDS2018-v3 and NF-UNSW-NB15-v3 in both directions (Fig. 1). Adding the source, unweighted or with equal weight per domain and class, never improves on the target-only model. With 10 labelled flows per class, F1 for CIC→UNSW is 0.726 with the source, 0.661 with the weighted source and 0.811 with target-only training. For UNSW→CIC the figures are 0.454, 0.430 and 0.555. Over k ∈ {1, 5, 10, 50, 100} and both directions, the source is significantly better than target-only in none of the 20 paired comparisons and significantly worse in 10.

Recall alone would tell a different story at k = 1. There, target-only CIC→UNSW recall is 0.666 against 0.022 with the source, but its FPR is 0.400 against 0.001. The target-only model labels a large share of benign traffic as attacks, and the source-trained model labels almost nothing as an attack. Neither is a usable detector, which is why we report FPR and balanced accuracy alongside recall.

### 4.2 Stronger models and adaptation methods

A random forest pooled with source data is a weak use of the source. We therefore give the source every reasonable chance: three model families and three adaptation methods, including importance weighting, which corrects for covariate shift, and fine-tuning, which is the method TAN-IDS uses. On CIC↔UNSW, under shared scaling, the 90 paired comparisons with target-only give zero cases where the source is significantly better and 38 where it is significantly worse; the remaining 52 show no difference. Under per-domain scaling the counts are 0 better and 25 worse (Fig. 2).

### 4.3 All twelve dataset pairs

Table 2 extends the comparison to all 12 directed pairs of the four datasets. Under shared scaling, the source significantly helps in 41 of 540 comparisons (8%), makes no significant difference in 294 (54%) and hurts in 205 (38%). The median change in F1 from adding the source is −0.025. Averaged within each pair and then over the 12 pairs, the source lowers F1 by 0.044 (95% CI −0.066 to −0.022), and only 3 of the 12 pairs have a positive mean change. Under per-domain scaling the counts are 34 helps (6%), 353 no differences (65%) and 153 hurts (28%), and the mean change is −0.038 (95% CI −0.064 to −0.017). Hurts outnumber helps for every method, every model and every k under both scalings. The random forest is hurt most often under shared scaling (99 of 180 comparisons), and fine-tuning is the most harmful method under per-domain scaling (72 hurts against 10 helps).

The direction does not depend on F1. Repeated on balanced accuracy, the verdicts are 35 helps and 214 hurts under shared scaling (49 and 147 under per-domain scaling), and the mean change over pairs is −0.018 (95% CI −0.033 to −0.002; per-domain −0.014, CI −0.022 to −0.006). Balanced accuracy matters most when NF-BoT-IoT-v3 is the target, where F1 is close to 0.99 for any model that flags most flows. There it changes the picture under per-domain scaling: the BoT-target comparisons show 32 helps and 15 hurts on balanced accuracy. Under shared scaling they show 13 helps and 36 hurts.

**Table 2.** Source-based adaptation vs target-only training: paired Wilcoxon verdicts on F1 (p < 0.05, uncorrected) over 10 seeds; 12 directed pairs × 3 models × 3 methods × 5 values of k = 540 comparisons per scaling. Each panel sums to 540.

| | Shared: help | no diff. | hurt | Per-domain: help | no diff. | hurt |
|---|---|---|---|---|---|---|
| *By method* | | | | | | |
| Pooled | 17 | 105 | 58 | 15 | 125 | 40 |
| Importance-weighted | 12 | 94 | 74 | 9 | 130 | 41 |
| Fine-tuned | 12 | 95 | 73 | 10 | 98 | 72 |
| *By model* | | | | | | |
| RF | 3 | 78 | 99 | 11 | 102 | 67 |
| GBT | 13 | 128 | 39 | 4 | 144 | 32 |
| MLP | 25 | 88 | 67 | 19 | 107 | 54 |
| *By k* | | | | | | |
| k = 1 | 11 | 69 | 28 | 9 | 72 | 27 |
| k = 5 | 6 | 65 | 37 | 3 | 74 | 31 |
| k = 10 | 5 | 68 | 35 | 4 | 69 | 35 |
| k = 50 | 8 | 44 | 56 | 8 | 69 | 31 |
| k = 100 | 11 | 48 | 49 | 10 | 69 | 29 |
| **Total** | **41 (8%)** | **294 (54%)** | **205 (38%)** | **34 (6%)** | **353 (65%)** | **153 (28%)** |

The harm does not fade simply because more target labels are available. Under shared scaling, the mean change over pairs is largest at k = 5 (−0.069) and smallest at k = 100 (−0.026), but the hurt count rises with k and peaks at k = 50 (56 hurts). Under per-domain scaling, the median change is −0.025 at k = 5 and −0.029 at k = 10 and close to zero at k = 100, while hurt counts stay between 27 and 35 at every k. Helps, in contrast, are spread across k rather than concentrated at the smallest budgets.

Fig. 3 shows the verdicts for each pair. Benefit is rare and pair-dependent. Ranked by helps minus hurts under shared scaling, the most favourable pair is UNSW→BoT, with 9 helps and 3 hurts, at k = 1, 10, 50 and 100; then UNSW→ToN (3 and 3) and BoT→CIC (14 and 16). The BoT→CIC helps all occur at k ≤ 10 and its hurts at k ≥ 10. Every other pair is clearly net negative, from −12 to −25. Under per-domain scaling the only net-favourable pair is ToN→CIC (9 helps, 5 hurts), which becomes 0 helps and 18 hurts under shared scaling (Section 5.4).

No individual comparison can survive Holm correction (Section 3.4), so we do not claim that the source significantly hurts in any particular cell. With false-discovery-rate control instead, 179 of 540 comparisons remain significant under shared scaling (29 helps, 150 hurts), and 129 under per-domain scaling (19 helps, 110 hurts). The claim the data support is the pooled one: averaged over the 12 pairs, the source lowers F1 and balanced accuracy, and significant harm is about five times as common as significant help. "No difference" in a single cell means only that 10 seeds could not detect one, not that the two arms are equivalent.

### 4.4 Zero-shot transfer

Without any target labels, transfer is weak and depends on the pair. Under shared scaling, the best model's balanced accuracy is 0.68–0.76 on four pairs (BoT→CIC, UNSW→ToN, UNSW→BoT and BoT→ToN). On the other eight it is at most 0.58, close to the 0.5 of chance. Under per-domain scaling the best pairs reach 0.66–0.71. In every pair and under both scalings, a target-only model trained on just 10 labelled flows per class does better than the best zero-shot model, with balanced accuracy of 0.78–0.94.

The zero-shot failures take two opposite forms, which recall alone would hide. A random forest trained on NF-BoT-IoT-v3, which is 97.5% attacks after sampling, flags almost every target flow: for BoT→CIC its recall is 1.000 at an FPR of 1.000. The same model trained on NF-CICIDS2018-v3 flags almost nothing in UNSW, ToN or BoT, with recall and FPR both at or near zero. In both cases balanced accuracy is 0.5, and the model has learned the source's base rate rather than any notion of an attack. The better zero-shot results come mostly from the MLP, for example UNSW→BoT with balanced accuracy 0.710 at an FPR of 0.156.

The strongest published zero-shot result on these datasets does not reproduce on v3. Atif and Ali report UNSW→CIC F1 of 0.81 with their pruned feature set C on NetFlow v2 (Atif & Ali, 2026)<!--ref:atif2026threeaxis--><!--anchor:section:4.2-->. With the same pruning reconstructed on v3, the best F1 is 0.21 on a balanced test set and 0.13 on a natural-rate test set. Their set A, which removes TTL only, reaches F1 0.54 on the balanced test set, but at a balanced accuracy of 0.54, barely above chance. Across their feature sets A–C, balanced accuracy is at most 0.55 in either direction. Our replication differs in dataset version (v3 rather than v2), in models (RF and GBT rather than XGBoost) and in the exact feature lists, which we reconstructed from their description. Their feature set was also chosen using cross-dataset F1 on the target (Atif & Ali, 2026)<!--ref:atif2026threeaxis--><!--anchor:section:3.3-->, which would favour that pair.

### 4.5 The TAN-IDS label budget

Finally, we emulate the TAN-IDS label budget, in which models are fine-tuned on 5% of the target training split (Ha Thanh, 2026)<!--ref:hathanh2026tanids--><!--anchor:section:3.5-->, and add the target-only arm it omits. We test the assumption behind their result, not their exact numbers: TAN-IDS uses an eight-dimensional feature interface, a 70% training split and XGBoost, whereas we use the 45 v3 features, our 50% pool and GBT. At this budget (70,404 and 82,789 labelled target flows) every method recovers. Target-only F1 is 0.961–1.000 across the two directions and three models, and pooling and fine-tuning are within ±0.006 of it, except for two fine-tuned models that are lower: GBT UNSW→CIC at 0.942 and RF CIC→UNSW at 0.981. The recovery reported for source-aware fine-tuning is therefore matched by the target labels alone: at TAN-IDS's budget the source is not needed, and at small budgets (Sections 4.1–4.3) it does not help.

If the source carries no usable signal about the target, the next question is why. Section 5 examines what separates the networks.
