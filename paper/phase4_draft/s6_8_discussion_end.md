## 6. Discussion

### 6.1 Reconciling with prior recovery results

Our results do not contradict the recovery that TAN-IDS and Hakim et al. report; they reattribute it. Fine-tuning a source model on a few percent of target labels does restore detection (Ha Thanh, 2026)<!--ref:hathanh2026tanids--><!--anchor:section:Table%2010-->, and at the TAN-IDS budget we observe the same recovery. A model trained on those target labels alone recovers just as well, however, and at small budgets adding the source lowers F1 on average. The recovery is what the target labels deliver. The two prior studies with a target-only arm are partly in line with this. Xu et al.'s source pretraining lowers few-shot accuracy at the smallest budget in both transfer directions, though it helps slightly at larger budgets on CICIDS2017 (Xu et al., 2025)<!--ref:xu2025multimodal--><!--anchor:section:Tables%208-9-->; Kim's evidence on host logs is mixed, with target-only learning better in one direction and worse in the other (Kim, 2026)<!--ref:kim2026prototype--><!--anchor:section:4-->. Neither tested the comparison over repeated runs, which is what our protocol adds.

### 6.2 Negative transfer is the expected outcome here

Transfer helps when the domains are close enough that source error is informative about target error (Ben-David et al., 2010)<!--ref:bendavid2010theory--><!--anchor:section:abstract-->; when they are far apart, source data can pull the model away from the target's decision boundary (Pan & Yang, 2010<!--ref:pan2010survey--><!--anchor:section:abstract-->; Zhang et al., 2023<!--ref:zhang2023negative--><!--anchor:section:abstract-->). The four NetFlow v3 networks are about as far apart as a domain classifier can measure, including within shared attack categories, which is consistent with this explanation. Importance weighting does not bridge the gap: under shared scaling the weights collapse onto a few source flows, with an effective sample size of 0.1–3.8% of the source sample (median 0.8%). The exceptions do not follow a simple rule. UNSW→BoT, the most favourable pair under shared scaling, has the lowest feature-importance overlap of any pair and is helped at both small and large k, and its benefit grows when TTL is removed; helps overall are spread across k. Neither label scarcity nor shared feature reliance predicts when a source helps, and a domain AUC near 1.0 for every pair cannot either. Finer measures of domain distance are needed; until then, a small target-only pilot at the affordable label budget is the practical test.

### 6.3 What this means for NIDS benchmarks

If each benchmark occupies its own region of feature space, a cross-dataset score mostly measures how well the target labels are used. Benchmark construction plausibly contributes. The NetFlow v3 release documents that NF-UNSW-NB15-v3 contains only 40 distinct source and 40 destination IP addresses, that NF-BoT-IoT-v3 has only 20 source addresses, and that most attack classes in the other datasets were run on separate days (Luay et al., 2025)<!--ref:luay2025temporal--><!--anchor:section:Tables%204-5-->. Small host populations and separated capture periods are the kind of design choice that, as audits of other benchmarks show, leave learnable traces of how a dataset was made (Flood et al., 2024<!--ref:flood2024bad--><!--anchor:section:abstract-->; Goldschmidt & Chudá, 2025<!--ref:goldschmidt2025network--><!--anchor:section:abstract-->). The pitfalls Arp et al. describe, in particular spurious correlations and inappropriate baselines, apply directly to transfer claims made without a target-only arm (Arp et al., 2022)<!--ref:arp2022dos--><!--anchor:section:abstract-->.

### 6.4 Limitations

Our conclusions hold for four public testbed datasets in one NetFlow format and for the adaptation methods we tested, not for every possible method. The testbeds themselves may be the source of the separability we measure, so results may differ between production networks that share infrastructure. We study binary detection only. The three model families use fixed, untuned hyper-parameters and simple adaptation arms; appending trees, for instance, gives the source half of the forest's vote at every k. Deep sequence models, meta-learning and domain-adversarial training are not included, although the separability we measure is what such methods would need to overcome. Ten seeds suffice for a pooled estimate but not for any single comparison to survive correction, and seeds and pairs share datasets, so the per-cell tests are descriptive and the pooled interval may be optimistic; the balanced-accuracy effect in particular is small. Our separability sanity check uses random halves of one dataset; a split by capture time, which would show how far separability reflects capture sessions rather than networks, needs the timestamps we removed and is left for future work. The per-category recall analysis of Section 5.2 uses per-domain scaling only. Our replication of Atif and Ali reconstructs their feature sets from their description, on v3 rather than v2, with RF and GBT in place of XGBoost. The evaluation is offline; real-time deployment and adversarial robustness are out of scope.

## 7. Recommended Protocol

Our findings suggest six practices for cross-dataset and few-shot NIDS studies:

1. **Always report target-only at the same label budget.** Without it, transfer and target learning cannot be told apart; in our data, recovery that looks like transfer is matched by the target labels alone (Section 4.5).
2. **Use repeated runs, paired tests and a pooled estimate.** Report one pooled effect with a confidence interval that respects shared datasets, not only a tally of significant cells. With five seeds a two-sided Wilcoxon test cannot reach p < 0.05, and Holm correction over 540 tests needs at least 15.
3. **Report false-positive rate or balanced accuracy, not recall alone.** Zero-shot models reach high recall by flagging benign traffic (Section 4.4), and F1 is uninformative when the target is mostly attacks.
4. **Use shared normalization statistics from training-visible data.** Never normalize with target test data, and avoid per-domain scaling when measuring separability, because it shifts categorical codes to dataset-specific values (Section 5.4).
5. **Report domain separability on raw features, with a sanity check.** Report the domain AUC on benign traffic and within shared attack categories next to the AUC between two halves of one dataset.
6. **Ablate known artifacts across all pairs.** Report transfer results with and without documented artifact features such as TTL; in our data, a single-pair ablation under per-domain scaling pointed the wrong way (Section 5.3).

## 8. Conclusion

Recent work credits source datasets with recovering intrusion detection on new networks once a few target flows are labelled. On the four NetFlow v3 benchmarks, under a leak-free protocol with 10 seeds, the target labels alone achieve that recovery. Across 540 paired comparisons, three model families and three adaptation methods, the source gives no consistent benefit: averaged over pairs it lowers F1 by 0.044 (95% CI −0.066 to −0.022), the mean is negative for every source and target dataset, and under shared scaling significant harm is about five times as common as significant help on F1 and six times on balanced accuracy, where the effect is smaller. Zero-shot transfer is weak and pair-dependent, and a published strong zero-shot result does not reproduce on v3. These results are consistent with each network occupying its own region of feature space, even for the same attack type and across most features, and the TTL artifact is not the cause. Per-domain scaling adds a further, avoidable source of apparent separability. Future work should test these findings on production networks that share infrastructure, with time-based controls and multi-class detection, and develop measures of domain distance fine enough to predict when a source will help. Until then, the safest default for practitioners is to label a small sample of their own traffic and train on it.

---

## Data and Code Availability

The NetFlow v3 datasets are publicly available from the University of Queensland NIDS datasets page. Every number in the paper is printed by the committed code. All code, together with a script (`run_all.sh`) that rebuilds every table and figure from the raw comma-separated values (CSV) files, is available at https://github.com/rijan-rayamajhi/TRACE-IDS.

## Use of AI Tools

Generative AI (Claude, Anthropic) was used to assist with analysis code, checking references against their sources, and drafting and editing the text. The author designed the study, made all experimental decisions, reviewed the output and takes full responsibility for the content.

## Funding

This research received no external funding.

## Conflict of Interest

The author declares no conflict of interest.

## Author Contributions (CRediT)

Rijan Rayamajhi: Conceptualization, Methodology, Software, Investigation, Formal analysis, Data curation, Visualization, Writing – original draft, Writing – review & editing.

<!--protected-hedges: To our knowledge, based on web searches for cross-dataset, few-shot and transfer NIDS work covering 2020–2026 and the reference lists of the closest studies, with every hit verified against Crossref, arXiv or OpenAlex, as of 11 October 2026 | Within the sources we screened-->
