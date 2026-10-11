
## Figure Captions

- **Fig. 1.** CIC↔UNSW, random forest: F1 against k labelled target flows per class for source+k, weighted source+k and target-only, with all features and without TTL; mean ± std over 10 seeds (`results/e1_recovery.png`).
- **Fig. 2.** CIC↔UNSW: F1 against k for target-only, pooled, importance-weighted and fine-tuned RF, GBT and MLP; mean ± std over 10 seeds (`results/e2_transfer.png`).
- **Fig. 3.** All 12 directed pairs: for each pair, model and method, the number of k values at which the source significantly helps minus the number at which it hurts (paired Wilcoxon, p < 0.05). Left: per-domain scaling; right: shared scaling (`results/e3_heatmap.png`, `results/e3_heatmap_shared.png`).
- **Fig. 4.** Change in attack recall from adding the source (k = 10), split by whether the source contains the attack category (`results/e5_families.png`).
- **Fig. 5.** Greedy feature ablation: held-out domain-classifier AUC against the number of features removed, per pair, on raw and per-domain-scaled features, for all flows and benign flows (`results/e5_ablation.png`).
