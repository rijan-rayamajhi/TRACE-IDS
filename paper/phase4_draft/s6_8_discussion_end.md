## 6. Discussion

### 6.1 Reconciling with prior recovery results

Our results do not contradict the recovery that TAN-IDS and Hakim et al. report; they reattribute it. Fine-tuning a source model on a few percent of target labels does restore detection (Ha Thanh, 2026)<!--ref:hathanh2026tanids--><!--anchor:section:Table%2010-->, and at the TAN-IDS budget we observe the same recovery. A model trained on those target labels alone recovers just as well, however, and at small budgets the median change from adding the source is negative. The recovery is what the target labels deliver; the source's contribution, measured against that control, is on average negative, with rare and pair-dependent exceptions. The two studies in our survey that did include a target-only arm point the same way. Xu et al.'s source pretraining lowers few-shot accuracy at the smallest budget in both of their transfer directions, although it helps slightly at larger budgets on CICIDS2017 (Xu et al., 2025)<!--ref:xu2025multimodal--><!--anchor:section:Tables%208-9-->. Kim finds target-only learning better than every adaptation method in one direction and clearly worse in the other, on host logs (Kim, 2026)<!--ref:kim2026prototype--><!--anchor:section:4-->. Different data, models and adaptation methods point the same way: in cross-network intrusion detection, a few target labels go further on their own than prior work assumed, and the source adds less.

### 6.2 Negative transfer is the expected outcome here

From the perspective of transfer-learning theory, the result is unsurprising. Transfer helps when the domains are close enough that source error is informative about target error (Ben-David et al., 2010)<!--ref:bendavid2010theory--><!--anchor:section:abstract-->. When they are far apart, source data can pull the model away from the target's decision boundary: negative transfer (Pan & Yang, 2010<!--ref:pan2010survey--><!--anchor:section:abstract-->; Zhang et al., 2023<!--ref:zhang2023negative--><!--anchor:section:abstract-->). Section 5 shows that the four NetFlow v3 networks are about as far apart as a domain classifier can measure, including within shared attack categories, which is consistent with this explanation. Importance weighting cannot bridge this gap, because it assumes the source covers the target's input distribution (Shimodaira, 2000)<!--ref:shimodaira2000improving--><!--anchor:section:abstract-->. Our importance weights show the consequence. Under shared scaling they collapse onto a few source flows: the effective sample size is 0.1–3.8% of the source sample across pairs (median 0.8%). Per-domain scaling removes mean and scale differences first, and leaves 5–68% (median 34%), but the weighted source still does not help (Table 2). Our measurement of separability is coarse, however: a domain AUC near 1.0 for every pair cannot say *which* pairs will transfer, and finer measures of domain distance are needed for that.

### 6.3 When might a source help?

The exceptions in our data do not follow a simple rule. Under shared scaling, the most favourable pair, UNSW→BoT, has the lowest feature-importance overlap of any pair, and its helps occur at both small and large k. BoT→CIC is helped only at k ≤ 10, but across all pairs helps are spread over every k rather than concentrated at the smallest budgets. ToN→CIC, the pair with the highest overlap, was favourable only under per-domain scaling. Neither label scarcity nor shared feature reliance therefore predicts when a source helps. Two features of our results are more robust. First, the source clearly helps one pair under shared scaling (UNSW→BoT, 9 helps against 3 hurts), so benefit is possible. Second, without the TTL artifact that pair's benefit grows to 15 helps and no hurts, while the average effect becomes more negative (Section 5.3), so artifacts shape which pairs benefit without explaining the overall result. A practitioner can check whether a source helps their own network with a small target-only pilot at the label budget they can afford.

### 6.4 What this means for NIDS benchmarks

Our results also bear on how cross-dataset evaluations are read. If each benchmark occupies its own region of feature space, a cross-dataset score mostly measures how well the target labels are used. Benchmark construction plausibly contributes. The NetFlow v3 release documents that NF-UNSW-NB15-v3 contains only 40 distinct source and 40 destination IP addresses, that NF-BoT-IoT-v3 has only 20 source addresses, and that most attack classes in the other datasets were run on separate days (Luay et al., 2025)<!--ref:luay2025temporal--><!--anchor:section:Tables%204-5-->. Small host populations and separated capture periods are the kind of design choice that, as audits of other benchmarks show, leave learnable traces of how a dataset was made (Flood et al., 2024<!--ref:flood2024bad--><!--anchor:section:abstract-->; Goldschmidt & Chudá, 2025<!--ref:goldschmidt2025network--><!--anchor:section:abstract-->). The pitfalls Arp et al. describe, in particular spurious correlations and inappropriate baselines, apply directly to transfer claims made without a target-only arm (Arp et al., 2022)<!--ref:arp2022dos--><!--anchor:section:abstract-->.

### 6.5 Limitations

Our conclusions are bounded by the study design. We use four public testbed datasets, all in one NetFlow format, and our conclusion holds for the adaptation methods we tested, not for every possible method. The four testbeds are themselves the source of the separability we measure, so the result may differ between real production networks that share infrastructure. We study binary detection only. We test three model families with fixed, untuned hyper-parameters and simple adaptation arms. Appending trees, for instance, gives the source half of the forest's vote at every k. Deep sequence models, meta-learning and domain-adversarial training are not included, although the separability we measure is the quantity such methods would need to overcome. Ten seeds give enough power for a pooled estimate, but not to make any single comparison significant after correcting for 540 tests, and seeds are not fully independent because they share the underlying datasets. The per-category and feature-importance analyses of Section 5.2 use per-domain scaling only. Our TTL ablation removes two documented artifact features; other, undocumented artifacts may remain. Our replication of Atif and Ali reconstructs their feature sets from their description, uses v3 rather than v2, and uses RF and GBT in place of XGBoost. The evaluation is offline; real-time deployment and adversarial robustness are out of scope.

## 7. Recommended Protocol

Our findings suggest six practices for cross-dataset and few-shot NIDS studies:

1. **Always report target-only at the same label budget.** Any claim that a source dataset helps must be measured against a model trained on the same target labels alone. Without this control, transfer and target learning cannot be told apart. In our data the control changes the conclusion: recovery that looks like transfer is matched by the target labels alone.
2. **Use repeated runs, paired tests and a pooled estimate.** Report results over multiple seeds with paired tests, and give one pooled effect with a confidence interval rather than only a tally of significant cells. Single-run differences of a few points are within seed-to-seed noise, and a significance test needs enough seeds to be able to reject at all: with five seeds, a two-sided Wilcoxon test cannot reach p < 0.05, and Holm correction over 540 tests needs at least 15.
3. **Report false-positive rate or balanced accuracy, not recall alone.** Few-shot and zero-shot models often reach high recall by flagging benign traffic; one of our zero-shot models reaches recall 1.0 at an FPR of 1.0.
4. **Take normalization statistics only from training-visible data, and check the scaling.** Never use target test data for normalization. Compare per-domain and shared scaling, because per-domain scaling makes even two halves of one dataset perfectly separable.
5. **Report domain separability with a negative control.** A domain classifier's AUC on raw features, on benign traffic and within shared attack categories, shows how far apart two networks are. Report it next to the AUC between two halves of one dataset, which should be 0.5. An AUC near 1.0 within the same attack category warns that the source's attack examples may not resemble the target's.
6. **Ablate known artifacts.** Report transfer results with and without documented artifact features such as TTL. In our data, removing TTL reversed the comparison on one pair, but only under per-domain scaling and not across all pairs, so a single-pair ablation can mislead.

## 8. Conclusion

Recent work credits source datasets with recovering intrusion detection on new networks once a few target flows are labelled. On the four NetFlow v3 benchmarks, under a leak-free protocol with 10 seeds, the target labels alone achieve that recovery. Across 540 paired comparisons, three model families and three adaptation methods, the source gives no consistent benefit: averaged over pairs it lowers F1 by 0.044 (95% CI −0.066 to −0.022), and significant harm is about five times as common as significant help, under both shared and per-domain scaling and on both F1 and balanced accuracy. Zero-shot transfer is weak and pair-dependent, and a published strong zero-shot result does not reproduce on v3. These results are consistent with each network occupying its own region of feature space, even for the same attack type and across most features. Neither that separation nor the absence of benefit is due to the TTL artifact: without it, the source does slightly worse on average. Per-domain scaling adds a further, avoidable source of separability. Future work should test whether these findings hold on production networks that share infrastructure and in multi-class detection, and should develop measures of domain distance fine enough to predict when a source will help. Until then, the safest default for practitioners is to label a small sample of their own traffic and train on it.

---

## Data and Code Availability

The NetFlow v3 datasets are publicly available from the University of Queensland NIDS datasets page. All code, together with a script (`run_all.sh`) that rebuilds every table and figure from the raw comma-separated values (CSV) files, is available at https://github.com/rijan-rayamajhi/TRACE-IDS.

## Use of AI Tools

The author used Anthropic's Claude (Claude Code) to help write analysis code, verify references and draft and edit the text. The author designed the study, approved every experimental decision and is responsible for the content. Every number in the paper is printed by committed code in the repository.

## Funding

This research received no external funding.

## Conflict of Interest

The author declares no conflict of interest.

## Author Contributions (CRediT)

Rijan Rayamajhi: Conceptualization, Methodology, Software, Investigation, Formal analysis, Data curation, Visualization, Writing – original draft, Writing – review & editing.

<!--protected-hedges: To our knowledge, based on web searches for cross-dataset, few-shot and transfer NIDS work covering 2020–2026 and the reference lists of the closest studies, with every hit verified against Crossref, arXiv or OpenAlex, as of 11 October 2026 | Within the sources we screened-->
