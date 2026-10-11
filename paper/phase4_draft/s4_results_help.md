## 4. Results: Does the Source Help?

### 4.1 One pair, one model

We begin with the setting closest to prior work: a random forest transferred between NF-CICIDS2018-v3 and NF-UNSW-NB15-v3 in both directions (Fig. 1). Adding the source (unweighted, or with equal weight per domain and class) does not improve on the target-only model in a consistent way. With 10 labelled flows per class, F1 for CIC→UNSW is 0.775 with the source, 0.832 with the weighted source and 0.811 with target-only training. For UNSW→CIC the figures are 0.530, 0.531 and 0.555. Differences of this size change sign across k and directions, and they are smaller than the seed-to-seed spread.

The one place where the source appears to win is misleading. At k = 1, target-only CIC→UNSW recall is far higher than recall with the source, but its FPR is 0.400 against 0.005. The target-only model labels a large share of benign traffic as attacks, and the source-trained model labels almost nothing as an attack. Neither is a usable detector, which is why we report FPR and balanced accuracy alongside recall.

### 4.2 Stronger models and adaptation methods

A random forest pooled with source data is a weak use of the source. We therefore give the source every reasonable chance: three model families and three adaptation methods, including importance weighting, which corrects for covariate shift, and fine-tuning, which is the method TAN-IDS uses. On CIC↔UNSW the 90 paired comparisons with target-only give zero cases where the source is significantly better and 25 where it is significantly worse; the remaining 65 show no difference. Under shared scaling the counts are 0 better and 38 worse (Fig. 2).

### 4.3 All twelve dataset pairs

Table 2 extends the comparison to all 12 directed pairs of the four datasets. Under per-domain scaling, the source helps in 34 of 540 comparisons (6%), makes no significant difference in 353 (65%) and hurts in 153 (28%). The median change in F1 from adding the source is −0.011, and the mean is −0.039. Under shared scaling the pattern strengthens: 41 helps (8%), 294 no differences (54%) and 205 hurts (38%), with a median change of −0.025. Harm outnumbers help for every method, every model and every k under both scalings. Fine-tuning is the most harmful method under per-domain scaling (72 hurts against 10 helps). The random forest is hurt most often under shared scaling (99 of 180 comparisons).

**Table 2.** Source-based adaptation vs target-only training: paired Wilcoxon verdicts (p < 0.05) over 10 seeds, 12 directed pairs × 3 models × 3 methods × 5 values of k = 540 comparisons per scaling.

| | Per-domain: help | no diff. | hurt | Shared: help | no diff. | hurt |
|---|---|---|---|---|---|---|
| Pooled | 15 | 125 | 40 | 17 | 105 | 58 |
| Importance-weighted | 9 | 130 | 41 | 12 | 94 | 74 |
| Fine-tuned | 10 | 98 | 72 | 12 | 95 | 73 |
| RF | 11 | 102 | 67 | 3 | 78 | 99 |
| GBT | 4 | 144 | 32 | 13 | 128 | 39 |
| MLP | 19 | 107 | 54 | 25 | 88 | 67 |
| **All** | **34 (6%)** | **353 (65%)** | **153 (28%)** | **41 (8%)** | **294 (54%)** | **205 (38%)** |

The harm depends on how many target labels are available. Under per-domain scaling, the median change in F1 is −0.015 at k = 1, −0.025 at k = 5 and −0.029 at k = 10. It then shrinks to −0.003 at k = 50 and to almost zero (−0.0002) at k = 100. The source does the most damage at exactly the small budgets where it is supposed to help, and it fades as target labels accumulate and outweigh it. Under shared scaling the median change stays negative at every k, from −0.037 at k = 5 to −0.017 at k = 100.

Fig. 3 shows the verdicts for each pair. Benefit is rare and pair-dependent. Under per-domain scaling the most favourable pair is ToN→CIC, with 9 helps and 5 hurts; Section 5 shows that this exception does not survive shared scaling. Under shared scaling the most favourable pair is BoT→CIC, with 14 helps and 16 hurts. Twelve of its helps occur at k ≤ 5 and all 16 hurts at k ≥ 10, so the source helps only until a few dozen target labels are available.

No individual comparison survives Holm correction over 540 tests in either setting: the smallest p-value, 0.002, is the floor attainable with 10 seeds. We therefore do not claim that the source significantly hurts in any particular cell. The claim the data support is narrower and, for practice, more important: across a large and varied set of conditions, the source gives no consistent benefit over training on the same target labels, and significant harm is four to five times as common as significant help.

### 4.4 Zero-shot transfer

Without any target labels, transfer is weak and depends on the pair. Under per-domain scaling, the best model's balanced accuracy is 0.66–0.71 on four pairs (BoT→CIC, ToN→BoT, UNSW→BoT and UNSW→ToN) and 0.61 on BoT→ToN. On the other seven it is at most 0.56, close to the 0.5 of chance. Under shared scaling the best pairs reach 0.68–0.76. In every pair and under both scalings, a target-only model trained on just 10 labelled flows per class does better than the best zero-shot model, with balanced accuracy of 0.78–0.94.

The zero-shot failures take two opposite forms, which recall alone would hide. A random forest trained on NF-BoT-IoT-v3, which is 97.5% attacks after sampling, flags almost every target flow: for BoT→CIC its recall is 1.000 at an FPR of 1.000. The same model trained on NF-CICIDS2018-v3 flags almost nothing in UNSW, ToN or BoT, with recall and FPR both at or near zero. In both cases balanced accuracy is 0.5, and the model has learned the source's base rate rather than any notion of an attack. The better zero-shot results come mostly from the MLP, for example UNSW→BoT with balanced accuracy 0.710 at an FPR of 0.156.

The strongest published zero-shot result on these datasets does not reproduce on v3. Atif and Ali report UNSW→CIC F1 of 0.81 with their pruned feature set C on NetFlow v2 (Atif & Ali, 2026)<!--ref:atif2026threeaxis--><!--anchor:section:4.2-->. With the same pruning reconstructed on v3, the best F1 is 0.21 on a balanced test set and 0.13 on a natural-rate test set. Across all their feature sets, balanced accuracy never exceeds 0.55 in either direction. Our replication differs in dataset version (v3 rather than v2), in models (RF and GBT rather than XGBoost) and in the exact feature lists, which we reconstructed from their description. Their feature set was also chosen using cross-dataset F1 on the target (Atif & Ali, 2026)<!--ref:atif2026threeaxis--><!--anchor:section:3.3-->, which would favour that pair.

### 4.5 The TAN-IDS label budget

Finally, we repeat the TAN-IDS setting, in which models are fine-tuned on 5% of the target training split (Ha Thanh, 2026)<!--ref:hathanh2026tanids--><!--anchor:section:3.5-->, and add the target-only arm it omits. At this budget (tens of thousands of labelled target flows) every method recovers. Target-only F1 is 0.959–1.000 across the two directions and three models, and pooling and fine-tuning are within ±0.006 of it, except for GBT fine-tuned UNSW→CIC, which is lower at 0.914. The recovery reported for source-aware fine-tuning is therefore matched by the target labels alone: at TAN-IDS's budget the source is not needed, and at small budgets (Sections 4.1–4.3) it does not help.

If the source carries no usable signal about the target, the next question is why. Section 5 examines what separates the networks.
