## 4. Results: Does the Source Help?

### 4.1 One pair, one model

We begin with the setting closest to prior work: a random forest transferred between NF-CICIDS2018-v3 and NF-UNSW-NB15-v3 in both directions (Fig. 1). Adding the source, unweighted or with equal weight per domain and class, never significantly improves on the target-only model. With 10 labelled flows per class, F1 for CIC→UNSW is 0.726 with the source, 0.661 with the weighted source and 0.811 with target-only training; for UNSW→CIC it is 0.454, 0.430 and 0.555. Over k ∈ {1, 5, 10, 50, 100} and both directions, the source is significantly better in none of the 20 paired comparisons and significantly worse in 10.

Recall alone would tell a different story at k = 1. Target-only CIC→UNSW recall is 0.666 against 0.022 with the source, but its FPR is 0.400 against 0.001: one model flags much benign traffic, the other almost nothing. Neither is a usable detector, which is why we report FPR and balanced accuracy alongside recall.

### 4.2 Stronger models and adaptation methods

We next give the source every reasonable chance: three model families and three adaptation methods, including importance weighting, which corrects for covariate shift, and fine-tuning, the method TAN-IDS uses. On CIC↔UNSW, the 90 paired comparisons with target-only give no case where the source is significantly better and 38 where it is significantly worse (25 under per-domain scaling, the run shown in Fig. 2).

### 4.3 All twelve dataset pairs

Table 2 extends the comparison to all 12 directed pairs. Under shared scaling, the source significantly helps in 41 of 540 comparisons (8%), makes no significant difference in 294 (54%) and hurts in 205 (38%), with a median change in F1 of −0.025. Hurts outnumber helps for every method, model and k under both scalings. Averaged within each pair and then over pairs, the source lowers F1 by 0.044 (95% CI −0.066 to −0.022); 9 of the 12 pair means are negative (Wilcoxon across pairs, p = 0.016). Because pairs share datasets, the more telling check is by dataset: the mean change is negative for every source (−0.010 to −0.081) and every target (−0.022 to −0.074). Under per-domain scaling the counts are 34 helps, 353 no differences and 153 hurts, and the mean change is −0.038 (95% CI −0.064 to −0.017).

On balanced accuracy the direction is the same but the evidence is weaker: 35 helps and 214 hurts under shared scaling (49 and 147 under per-domain scaling), and a mean change of −0.018 (95% CI −0.033 to −0.002) whose upper bound barely excludes zero; across the 12 pair means the Wilcoxon p is 0.077. Balanced accuracy matters most when NF-BoT-IoT-v3 is the target, where F1 is close to 0.99 for any model that flags most flows. There it reverses the per-domain picture, to 32 helps and 15 hurts, while under shared scaling the BoT-target comparisons show 13 helps and 36 hurts.

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

**Table 2.** Source-based adaptation vs target-only training: paired Wilcoxon verdicts on F1 (p < 0.05, uncorrected) over 10 seeds; 12 directed pairs × 3 models × 3 methods × 5 values of k = 540 comparisons per scaling. Each panel sums to 540.

The harm does not fade as target labels accumulate. Hurt counts do not fall with k (under shared scaling they peak at k = 50), while helps are spread across all k (Table 2). The mean change over pairs is most negative at small budgets (−0.069 at k = 5 under shared scaling, −0.052 at k = 1 under per-domain scaling) and least negative at k = 100 (−0.026 and −0.018).

Benefit is rare and pair-dependent (Fig. 3). Ranked by helps minus hurts under shared scaling, the most favourable pair is UNSW→BoT (9 helps, 3 hurts, at k = 1, 10, 50 and 100), followed by UNSW→ToN (3 and 3) and BoT→CIC (14 and 16, with every help at k ≤ 10). Every other pair is clearly net negative, from −12 to −25. Under per-domain scaling the only net-favourable pair is ToN→CIC (9 helps, 5 hurts), which becomes 0 helps and 18 hurts under shared scaling (Section 5.4).

No individual comparison can survive Holm correction (Section 3.4), so we make no claim about any particular cell. With false-discovery-rate control, 179 of 540 comparisons remain significant under shared scaling (29 helps, 150 hurts), and 129 under per-domain scaling (19 helps, 110 hurts). "No difference" in a cell means only that 10 seeds could not detect one, not that the arms are equivalent. The supported claim is pooled: on average the source lowers F1, consistently across source and target datasets, and significant harm is about five times as common as significant help.

### 4.4 Zero-shot transfer

Without any target labels, transfer is weak and depends on the pair. Under shared scaling, the best model's balanced accuracy is 0.68–0.76 on four pairs (BoT→CIC, UNSW→ToN, UNSW→BoT and BoT→ToN) and at most 0.58 on the other eight (0.66–0.71 on the best pairs under per-domain scaling). In every pair and under both scalings, a target-only model trained on 10 labelled flows per class beats the best zero-shot model, with balanced accuracy of 0.78–0.94.

The zero-shot failures take two opposite forms, which recall alone would hide. The random forest trained on NF-CICIDS2018-v3 flags almost nothing in NF-UNSW-NB15-v3 (recall 0.001 at FPR 0.001), whereas the one trained on NF-BoT-IoT-v3, which is 97.5% attacks, flags most UNSW flows (recall 0.743 at FPR 0.792); both have balanced accuracy near 0.5. The best zero-shot results come from different models on different pairs, for example GBT on BoT→CIC (balanced accuracy 0.760 at FPR 0.217) and the MLP on UNSW→ToN (0.742 at FPR 0.138).

The strongest published zero-shot result does not reproduce on v3. Atif and Ali report UNSW→CIC F1 of 0.81 with their pruned feature set C on NetFlow v2 (Atif & Ali, 2026)<!--ref:atif2026threeaxis--><!--anchor:section:4.2-->. Reconstructed on v3, set C reaches F1 0.21 on a balanced test set and 0.13 at the natural rate, and set C restricted to v2 features reaches 0.25, all at balanced accuracy of at most 0.53. Their set A, which removes TTL only, reaches F1 0.54 on the balanced test set, but at balanced accuracy 0.54. Our replication differs in dataset version, in models (RF and GBT rather than XGBoost) and in the exact feature lists, which we reconstructed from their description; their feature set was also chosen using cross-dataset F1 on the target (Atif & Ali, 2026)<!--ref:atif2026threeaxis--><!--anchor:section:3.3-->, which would favour that pair.

### 4.5 The TAN-IDS label budget

Finally, we emulate the TAN-IDS label budget of 5% of the target training split (Ha Thanh, 2026)<!--ref:hathanh2026tanids--><!--anchor:section:3.5--> and add the target-only arm. We test the assumption behind their result, not their exact numbers: TAN-IDS uses an eight-dimensional feature interface, a 70% training split and XGBoost, whereas we use the 45 v3 features, our 50% pool and GBT. At this budget (70,404 and 82,789 labelled target flows) every method recovers. Target-only F1 is 0.961–1.000 across both directions and three models, and pooling and fine-tuning are within ±0.006 of it, except two fine-tuned models that are lower: GBT UNSW→CIC (0.942) and RF CIC→UNSW (0.981). The recovery reported for fine-tuning is matched by the target labels alone: at this budget the source is not needed, and at small budgets it does not help on average (Sections 4.1–4.3).

If the source carries no usable signal about the target, the next question is why.
