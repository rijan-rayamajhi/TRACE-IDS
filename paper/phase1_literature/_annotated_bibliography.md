
#### Section: introduction

##### Arp et al. (2022). Dos and Don'ts of Machine Learning in Computer Security. `arp2022dos`
- **Type**: conference-paper — 31st USENIX Security Symposium (USENIX Security 22), pp. 3971-3988 — arXiv 2010.09470
- **Verified via**: https://www.usenix.org/conference/usenixsecurity22/presentation/arp (BibTeX on page: pages 3971--3988, ISBN 978-1-939133-31-1); also http://export.arxiv.org/api/query?id_list=2010.09470
- **Summary**: Systematically catalogues ten recurring pitfalls in learning-based security research (e.g., sampling bias, spurious correlations, data snooping, inappropriate baselines, lab-only evaluation) and measures their prevalence in top-tier security papers. Shows through case studies how these pitfalls inflate reported performance.
- **Relevance**: Supports the framing that spurious correlations/dataset artifacts and inappropriate baselines (here: omitting a target-only baseline) are recognised ML-in-security pitfalls.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: No DOI (USENIX open proceedings). Distinguished Paper Award per USENIX page.

##### Geirhos et al. (2020). Shortcut learning in deep neural networks. `geirhos2020shortcut`
- **Type**: journal-article — Nature Machine Intelligence, vol. 2, no. 11, pp. 665-673 — DOI 10.1038/s42256-020-00257-z
- **Verified via**: https://api.crossref.org/works/10.1038/s42256-020-00257-z
- **Summary**: Perspective arguing that many deep-learning failures share one cause: shortcuts, i.e. decision rules that score well on standard benchmarks but fail to transfer to harder or real-world test conditions. Offers recommendations for interpretation and out-of-distribution benchmarking.
- **Relevance**: Conceptual anchor for describing TTL/categorical-code separability as shortcut features that give high in-dataset accuracy but do not transfer across NetFlow datasets.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Crossref title is sentence case 'Shortcut learning in deep neural networks'; arXiv title is 'Shortcut Learning in Deep Neural Networks'. Published online 10 Nov 2020.

##### Apruzzese et al. (2023). SoK: Pragmatic Assessment of Machine Learning for Network Intrusion Detection. `apruzzese2023sok`
- **Type**: conference-paper — 2023 IEEE 8th European Symposium on Security and Privacy (EuroS&P), pp. 592-614 — DOI 10.1109/EuroSP57164.2023.00042
- **Verified via**: https://api.crossref.org/works/10.1109/EuroSP57164.2023.00042
- **Summary**: Argues research evaluations of ML for NID ignore deployment factors and proposes 'pragmatic assessment', then re-assesses methods across many configurations, adversarial scenarios and hardware, validated with a practitioner user study.
- **Relevance**: Supports the methodological framing that NIDS evaluation must reflect deployment conditions (here: realistic small target-label budgets).
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Full author names and pages 592-614 confirmed via Crossref DOI lookup.

##### Sommer & Paxson (2010). Outside the Closed World: On Using Machine Learning for Network Intrusion Detection. `sommer2010outside`
- **Type**: conference-paper — 2010 IEEE Symposium on Security and Privacy, pp. 305-316 — DOI 10.1109/SP.2010.25
- **Verified via**: https://api.crossref.org/works/10.1109/SP.2010.25
- **Summary**: Explains why ML anomaly detection is rarely deployed operationally: intrusion detection differs fundamentally from typical ML tasks (cost of errors, semantic gap, diversity of traffic, evaluation difficulty).
- **Relevance**: Classic framing of the gap between lab evaluation and deployment on new networks.
- **Method weaknesses**: not assessed (read scope: abstract_only)


#### Section: related-work

##### Goldschmidt & Chudá (2025). Network intrusion datasets: A survey, limitations, and recommendations. `goldschmidt2025network`
- **Type**: journal-article — Computers & Security, vol. 156, pp. 104510 — DOI 10.1016/j.cose.2025.104510
- **Verified via**: https://api.crossref.org/works/10.1016/j.cose.2025.104510 ; http://export.arxiv.org/api/query?id_list=2502.06688
- **Summary**: Systematic literature review of 89 public NIDS datasets compared on 13 properties, with a discussion of domain-specific challenges and common data limitations. Adds a dataset-popularity analysis and best-practice recommendations for dataset selection, generation and use.
- **Relevance**: Supports background claims that NIDS benchmark datasets have documented quality limitations and that dataset choice affects robustness conclusions.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: arXiv v3 is the accepted version; journal article number 104510, September 2025 issue.

##### Roszeitis et al. (2026). Few-Shot Learning for Network Intrusion Detection: Methods, Datasets, and Performance. `roszeitis2026fewshot`
- **Type**: preprint — arXiv preprint — arXiv 2609.11275
- **Verified via**: http://export.arxiv.org/api/query?id_list=2609.11275
- **Summary**: PRISMA-2020-style systematic review of few-shot NIDS work 2022-2026 (1,358 records screened down to 21 studies). Finds meta-learning and CNNs dominate, most studies use five or fewer shots, CIC-IDS2017/CSE-CIC-IDS2018 dominate, and missing parameters/code limit reproducibility.
- **Relevance**: Supports the few-shot NIDS background and the claim that the field rarely uses common protocols or baselines, motivating a target-only k-shot baseline.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Preprint, v1 10 Sep 2026; not peer reviewed as far as the arXiv record shows. I only read the abstract, so I have not checked whether it reports how many of the 21 studies include a target-only baseline.

##### Sarhan et al. (2021). Feature Analysis for Machine Learning-based IoT Intrusion Detection. `sarhan2021featureanalysis`
- **Type**: preprint — arXiv preprint — arXiv 2108.12732
- **Verified via**: http://export.arxiv.org/api/query?id_list=2108.12732
- **Summary**: Ranks NIDS features with chi-square, information gain and correlation, then measures the marginal benefit of adding features for DFF and RF classifiers on UNSW-NB15, CSE-CIC-IDS2018 and ToN-IoT in both original and NetFlow formats. Accuracy rises quickly and saturates after a few features.
- **Relevance**: Supports the observation that a small number of NetFlow features carries most of the predictive signal, which is relevant to why removing a few dataset-identifying features (e.g. TTL) changes behaviour.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: CHECK: this is NOT the NetFlow-v2 datasets paper. If you meant the NetFlow datasets paper, use sarhan2022standard (2101.11315) or sarhan2021netflow (2011.09144). The arXiv record (v2, Nov 2022) lists no journal DOI. A Crossref search found only a Research Square preprint with the same title (DOI 10.21203/rs.3.rs-2035633/v1, 2022), which I did not open separately. arXiv admin note: substantial overlap with 2108.12722, which was published in Digital Communications and Networks as 'Feature extraction for machine learning-based intrusion detection in IoT networks' (DOI 10.1016/j.dcan.2022.08.012).

##### Ha Thanh (2026). A transfer-aware, deployment-oriented evaluation framework for NetFlow-based intrusion detection systems (TAN-IDS). `hathanh2026tanids`
- **Type**: journal-article — PLOS One, vol. 21, no. 4, pp. e0346801 — DOI 10.1371/journal.pone.0346801
- **Verified via**: https://api.crossref.org/works/10.1371/journal.pone.0346801 ; local PDF read in full
- **Summary**: An evaluation framework (not a new model) that maps UNSW-NB15 and NF-CSE-CIC-IDS2018 to an 8-D flow interface (duration, packets, bytes, ports, protocol, flags, packet rate) and runs four scenarios: in-dataset, cross-dataset, mixed-domain and fine-tuning with 5% labelled target data. Models are RF, XGBoost, MLP and FlowTransformer-lite on a binary task. In-dataset F1-macro is 0.97-0.99 (Table 7). Cross-dataset transfer collapses, e.g. RF CIC->UNSW attack recall 0.00 and XGB 0.0035 (Table 8). 5% fine-tuning restores RF/XGB to F1 about 0.98 (Table 10), while MLP CIC->UNSW stays poor (recall 0.31).
- **Relevance**: The closest related work. It reports the same deployment scenario (source plus a few labelled target flows) and concludes that source-aware fine-tuning 'recovers' performance. However, it has no target-only baseline and uses a single run without significance tests, which is exactly the gap this study fills.
- **Method weaknesses** (read: full text by AI agent; NOT an author reading attestation)
  - No target-only baseline. The 'fine-tuning' scenario (5% labelled target data, source-pretrained) is compared only with zero-shot cross-dataset transfer and with in-dataset training on the full 70% target split. No model is trained on the same 5% target subset alone, so the source's contribution is not isolated. Checked Sections 3.5, 4.2, 4.2.1, 5.4 and Tables 7-10. [reader-inferred]
  - Single run per scenario, fixed seed, no confidence intervals or significance tests. [author-acknowledged, section: 6.2]
  - Sensitivity to which 5% target subset is drawn is not quantified. [author-acknowledged, section: 6.2]
  - Binary labels only; attack families are merged. [author-acknowledged, section: 6.1]
  - Only two domains (UNSW-NB15 and NF-CSE-CIC-IDS2018) and one transfer pair. [author-acknowledged, section: 6.3]
  - Mixed-domain training uses natural proportions and is dominated by NF-CSE-CIC-IDS2018, which may overestimate robustness. [author-acknowledged, sections: 4.2.2, 5.3, 6.3]
  - No feature ablation of the 8-D interface. [author-acknowledged, section: 5.6.1]
  - The feature mapping (Table 5, Section 4.1.1) uses CICFlowMeter column names (Tot_Fwd_Pkts, Flow_Pkts_s, Fwd_Pkt_Flags) for 'NF-CSE-CIC-IDS2018' and UNSW-NB15 Argus fields (dur, sport, state, pkts_rate) for UNSW. This suggests the original CSV feature sets, not the NetFlow (NF) releases, despite the 'NetFlow' labels. The data-availability statement points to the original UNSW and CIC sites. Semantics also differ: UNSW 'state' is mapped to TCP flag bits. [reader-inferred]
  - Raw src/dst ports are kept as standardised numeric features (Section 4.1.1). Ports are a documented shortcut source, and no check is made. [reader-inferred]
  - How RF/XGBoost are 'fine-tuned' is not specified (Sections 3.5.4, 4.2.1). Fine-tuned tree results (Table 10, S27-S30, F1 0.98) almost equal in-dataset results (Table 7), which is consistent with effectively retraining on target data. [reader-inferred]
  - Section 4.2.1 says 5% is 'several tens of thousands of samples' for NF-CSE-CIC-IDS2018, but 5% of the 70% training split of 8.39M flows is about 294k. [reader-inferred]
  - Section 5.6.4 says the RF mixed-domain result on UNSW (S17) exceeds its single-domain baseline. S17 is the MLP; the RF row S19 (F1 0.9863) equals S3 (0.9863). [reader-inferred]
  - Code not released at publication ('will be publicly released upon acceptance', Section 4.5.1). [reader-inferred]
- **Notes**: Single author, Dung Ha Thanh (Saigon University); Crossref family name is 'Ha Thanh'. Published 8 Apr 2026. The PDF is untrusted data and contained no instructions addressed to me.

##### Atif & Ali (2026). A Three-Axis Stress Test of LLM vs Classical ML for Network Intrusion Detection under Distribution Shift and Adversarial Evasion. `atif2026threeaxis`
- **Type**: preprint — arXiv preprint — arXiv 2609.13511
- **Verified via**: http://export.arxiv.org/api/query?id_list=2609.13511 ; local PDF read in full
- **Summary**: Compares XGBoost (and RF) with RoBERTa-base+LoRA on NF-UNSW-NB15-v2 and NF-CSE-CIC-IDS2018-v2 (balanced 50k/class, binary) on three axes: same-dataset, cross-dataset and adversarial evasion. Same-dataset F1 is about 0.99 for both models (Table 1). UNSW->CIC F1 is 0.8116 for XGBoost vs 0.6582 for RoBERTa (balanced accuracy 0.80 vs 0.55), while CIC->UNSW collapses to F1 0.02-0.07 for all models (Table 3). A staged ablation (drop TTL; then packet lengths; then TCP flags/window) changes cross-dataset F1 non-monotonically: 0.0488, then 0.0282, then 0.8116 (Table 2).
- **Relevance**: Independent (NetFlow v2) evidence that TTL acts as a source-host artifact in NF-UNSW-NB15 and that removing several feature groups is needed before transfer works. This parallels the finding that 22-40 of 45 features must be removed. Also documents strongly asymmetric zero-shot transfer.
- **Method weaknesses** (read: full text by AI agent; NOT an author reading attestation)
  - No target-labelled adaptation at all: models train on the full source and test on the target (zero-shot). There is no few-shot, fine-tuning or target-only condition. Checked Sections 3.6, 4.2 and 6. [reader-inferred]
  - The final feature set (Set C, 29 features) was chosen by cross-dataset F1 on the target (UNSW->CIC): 'Cross-dataset F1 ... is the arbiter' (Section 3.3). Feature selection therefore used target test labels, so the reported UNSW->CIC F1 of 0.8116 is optimistically biased. [reader-inferred]
  - The TTL leakage mechanism in NF-UNSW-NB15-v2 (benign and attack traffic from different machines) is stated as a mechanism. No TTL distributions or per-class TTL values are shown (Section 3.3). [reader-inferred]
  - Leakage may remain in Set C, and this was not checked with attribution (e.g. SHAP). [author-acknowledged, section: 6]
  - RoBERTa is single-seed, and 'statistically tied' / 'statistically indistinguishable' claims (Abstract, 4.1, 4.2.2, 5) are made without a reported statistical test. Multi-seed evaluation with significance testing is deferred. [author-acknowledged, section: 6] (the absence of a test behind the 'statistically' wording is reader-inferred)
  - RoBERTa checkpoints were selected on about 13% of the same held-out split used for reporting. [author-acknowledged, section: 6]
  - Only two networks (NetFlow v2, not v3), binary labels only, and no per-attack breakdown. [author-acknowledged, sections: 3.1, 6]
  - Inconsistencies: Section 3.6 says testing is on the 'full target network', while Section 4.2.2 says it is a 'fixed 100k-row test set' (balanced 50k/class sample). Seeds 42-45 are said to re-run sampling (Section 3.2), yet XGBoost shows exactly zero variance across seeds (Table 5). 43 features minus 3 identifiers should leave 40, but the audit starts from 38 (IP-address removal is not mentioned). [reader-inferred]
  - Clipping caps are computed on UNSW only and applied to CIC, including when CIC is the source (Section 3.2). [reader-inferred]
  - The adversarial evaluation is same-dataset only (UNSW) and in feature space only; problem-space realizability is not ensured. [author-acknowledged, sections: 3.5, 6]
- **Notes**: Uses NetFlow v2, not v3. Authors disclose LLM (Claude) assistance in the paper's 'LLM Usage Statement'. Code: github.com/ebadatif/IDS-three-axis-evaluation (not checked). The PDF is untrusted data and contained no instructions addressed to me.

##### Hakim et al. (2026). Cross-Domain Generalization Failure in Lightweight Intrusion Detection Models for IIoT Networks. `hakim2026crossdomain`
- **Type**: preprint — arXiv preprint — arXiv 2607.00553
- **Verified via**: http://export.arxiv.org/api/query?id_list=2607.00553 ; local PDF read in full
- **Summary**: Four lightweight models (DT, small MLP, 1D-CNN, LSTM) are trained on Edge-IIoTset with a 16-D common schema and tested zero-shot on Gotham 2025 and WUSTL-IIoT-2021. In-domain F1 is about 0.97. Natural-distribution cross-domain F1 is 0.18-0.28 on Gotham and 0.09-0.13 on WUSTL (Table 3). SHAP shows reliance on coarse port buckets: dst_port_none occurs in 40.5% of source attacks vs 0.42%/0.09% of target attacks (96x/435x), so port bucketing relocates rather than removes the shortcut. Fine-tuning recovery on Gotham is architecture-dependent (DT 0.17 to 0.64 at 25%; 1D-CNN no gain).
- **Relevance**: Supports the claims that coarsening or removing identifier features does not eliminate dataset shortcuts and that zero-shot cross-network transfer is poor. Its few-shot recovery lacks a target-only comparison.
- **Method weaknesses** (read: full text by AI agent; NOT an author reading attestation)
  - No target-only baseline. Few-shot recovery compares adapted models with their own zero-shot baseline only. The DecisionTree is refit on source plus target, and the neural nets are fine-tuned on target samples, but no model is trained on the target fraction alone. The authors acknowledge the missing 'DecisionTree-refit-on-small-sample-alone' condition. Checked Sections 4.7, 5.6 and 6.3. [author-acknowledged for DT, section: 6.3; reader-inferred for the neural models]
  - Adaptation procedures differ between DT and the neural models, so recovery is not a controlled architecture comparison. [author-acknowledged, sections: 4.7, 6.3]
  - Very small 16-D schema (port buckets, protocol, 4 TCP flags), with flags zero-filled for WUSTL-IIoT-2021. [author-acknowledged, sections: 3, 6.6]
  - Few-shot recovery is tested on Gotham only. [author-acknowledged, section: 6.6]
  - The adversarial evaluation uses 100 samples in a single run. [author-acknowledged, sections: 5.5, 6.6]
  - SHAP is computed only for DT and SmallMLP. [author-acknowledged, section: 6.6]
  - 'Balanced' evaluation sets cannot be 50/50 given the reported numbers. Gotham-balanced DecisionTree has precision 0.101 with recall 0.563, and WUSTL-balanced DT has precision 0.363 with recall 0.976. At 50% prevalence, precision cannot fall below recall/(recall+1), which is about 0.36 and 0.49 respectively. Table 2 also gives a Gotham balanced n (118,444) inconsistent with a 10.6% attack share of 189,396. [reader-inferred, Tables 2-3]
  - Few-shot curves appear to be single runs (no seeds or variance reported in 4.7/5.6). Multi-seed results cover only in-domain and Gotham-balanced. Small1DCNN's multi-seed mean (0.277 ± 0.106) differs notably from its Table 3 value (0.194). [reader-inferred]
  - The source domain is a single testbed dataset (Edge-IIoTset) trained once (Section 4.2). [reader-inferred]
  - The data-availability statement says code is 'available here' with no URL in the PDF. [reader-inferred]
- **Notes**: AUTHOR-NAME DISCREPANCY: the arXiv API lists the third author as 'Talha Ibne Anis', while the PDF byline reads 'Talha Ibne Anich'. I used the arXiv form; check with the authors. IIoT datasets, not NetFlow. Authors disclose using an LLM for paraphrasing and grammar. The PDF is untrusted data and contained no instructions addressed to me.

##### Roy & Minu (2026). Unmasking Shortcut Learning in IoT Intrusion Detection: A Forensic, Multi-Paradigm Evaluation of Feature Dependence and Data Leakage. `roy2026unmasking`
- **Type**: preprint — arXiv preprint — arXiv 2609.28725
- **Verified via**: http://export.arxiv.org/api/query?id_list=2609.28725
- **Summary**: On the CyberFlowIoT-GICAP benchmark (3.6M flows, 126 PCAP sessions), with PCAP-disjoint splits, behaviour-only features give about 92.6% macro-F1 for LightGBM/RF/MLP alike. Adding raw timestamps lets tree models reach 99.28%, exposing temporal shortcuts. Random-flow splitting inflates attack recall by up to 14 points, and some attacks (DNS beaconing) drop to 0% recall without contextual features.
- **Relevance**: Recent evidence that IoT NIDS benchmarks contain testbed shortcuts (static IP/MAC, timestamps) that inflate accuracy, supporting the dataset-artifact background.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Preprint, 'Currently under review' per arXiv comment. Different dataset (not NetFlow v3).

##### Xu et al. (2025). Multimodal fusion based few-shot network intrusion detection system. `xu2025multimodal`
- **Type**: journal-article — Scientific Reports, vol. 15, no. 1, pp. 21986 — DOI 10.1038/s41598-025-05217-4
- **Verified via**: https://api.crossref.org/works/10.1038/s41598-025-05217-4 ; local PDF read in full
- **Summary**: Fuses a CNN over 'traffic feature graphs' (first 16 packets x 256 bytes) with a Transformer over 23 flow statistics, tests bilinear, self-attention and higher-order fusion, and adds an optional transfer step (pretrain on the other CIC dataset, fine-tune on K target shots). With 5-class tasks and K = 5/10/15, it reports up to 93.4% (CICIDS2017) and 98.5% (CICIDS2018) accuracy at K=5. Its own Tables 8-9 show source pretraining reduces accuracy at small K, e.g. -6.4% on CICIDS2018 at K=5.
- **Relevance**: Rare few-shot NIDS study with an explicit target-only comparison, and its own numbers show source pretraining often does not help or hurts at small K, consistent with this study's main finding (though on CIC-IDS2017<->2018, packet bytes, and without statistics).
- **Method weaknesses** (read: full text by AI agent; NOT an author reading attestation)
  - It DOES include a target-only baseline: the 'Self-Sufficient Model' is trained only on K target samples per class, while the 'Transfer-Enhanced Model' is pretrained on 100 samples/class of the other CIC dataset and fine-tuned (Experiments; Tables 8-9, pp.12-13). Transfer hurt on CICIDS2018 at every K (-6.4%, -1.3%, -0.9% accuracy) and on CICIDS2017 at K=5 (-2.0%); it helped only at K=10/15 on CICIDS2017 (+1.3%). The authors attribute the K=5 drop to source-target discrepancy. [author-acknowledged, section: Sample sensitivity experiment / Summary of results]
  - No repeated runs, variance or significance tests are reported for any comparison. I checked Experiments, Detection results, Sample sensitivity, Feature fusion, Comparison, One-shot and Ablation sections and found none. Accuracy differences of about 1% are interpreted as improvements. [reader-inferred]
  - Tiny test sets: Table 7 suggests 30 test samples per class over 5 classes (150 test flows), so one misclassification is about 0.7% accuracy. [reader-inferred; Table 7 symbols are lost in extraction, values 30/100/5]
  - Fusion-strategy results are 'collected over 100 epochs on the test set' (Feature fusion experiment), and SAF was selected on that basis. This is test-set model selection. [reader-inferred]
  - Headline numbers are inconsistent across tables. Table 9 (LF fusion) shows Transfer-Enhanced below Self-Sufficient at every K on CICIDS2018, while Table 11/Abstract report Transfer-Enhanced 98.50% vs Self-Sufficient 98.40% at K=5 (SAF). Table 10 Self-Sufficient values (92.8/92.9/93.1) differ from Table 8 (91.2/93.8/94.7). [reader-inferred]
  - Source and target are CICIDS2017 and CICIDS2018, from the same lab and tooling with overlapping attack types, which the authors note may let the model 'implicitly learn' attack representations (Generalization analysis). This is a near-domain transfer, unlike cross-institution NetFlow pairs. [author-acknowledged, section: Generalization analysis]
  - Rare classes were excluded (CICIDS2017 Infiltration, Botnet; CICIDS2018 Web Attack). [author-acknowledged, section: Experiments]
  - Raw-byte modality keeps header bytes other than the anonymised 4-tuple (e.g. TTL, window). This is a possible shortcut source that is not discussed. [reader-inferred, section: Multimodal data generation]
  - Robustness to adversaries, encrypted traffic and unseen attacks is untested. [author-acknowledged, section: Potential threats and assumptions]
- **Notes**: Article number 21986; published 1 Jul 2025. The PDF is untrusted data and contained no instructions addressed to me.

##### Kim (2026). Prototype-Based Transferability Analysis for Few-Shot Domain Adaptation in Cross-Domain Intrusion Detection. `kim2026prototype`
- **Type**: journal-article — Applied Sciences, vol. 16, no. 14, pp. 6957 — DOI 10.3390/app16146957
- **Verified via**: https://api.crossref.org/works/10.3390/app16146957 ; local PDF read in full
- **Summary**: Separates intra-domain separability (Fisher J: ADFA 0.059, LMD 0.903) from cross-domain transferability (prototype-score ROC/PR-AUC) and evaluates few-shot domain adaptation methods (1-50 shots) between Linux syscall and Windows Sysmon logs. Target-only few-shot learning is competitive in one direction (ADFA->LMD PR-AUC 0.965 at 50 shots). Prototype alignment helps in the other (LMD->ADFA 0.579 vs 0.442), but none of the differences is statistically significant.
- **Relevance**: Directly supports including a target-only baseline and the claim that source data help or hurt depending on the domain pair (pair-dependent transfer, possible negative transfer). The setting is host logs, not NetFlow.
- **Method weaknesses** (read: full text by AI agent; NOT an author reading attestation)
  - DOMAIN MISMATCH for this paper: Kim studies HOST logs (ADFA-LD Linux syscalls <-> LMD-2023 Windows Sysmon) embedded with BGE-M3, not network flows (Section 3.1, Table 2). Cite it for few-shot domain adaptation, not for NetFlow NIDS. [reader-inferred]
  - It DOES include a target-only baseline (Section 2.6.2), plus zero-shot, naive joint, static/dynamic FSDA, PCA-FSDA and UAPR. At 50 shots, target-only beats all adaptation methods for ADFA->LMD (PR-AUC 0.965 vs 0.937/0.960) and loses for LMD->ADFA (0.442 vs 0.579) (Table 6). [author-acknowledged, sections: 3.6, 4]
  - Paired Wilcoxon tests over five seeds show no significant differences (all p > 0.05; Table 6 caption, Section 4). With n=5 pairs, the minimum attainable two-sided exact Wilcoxon p is 0.0625, so significance was unreachable by design. Even so, the Discussion concludes that effectiveness 'depends primarily on source-target transferability'. [reader-inferred]
  - Only two transfer directions and one dataset pair, so the findings are a two-direction case study. [author-acknowledged, sections: 3.5, 3.6, 4, 5]
  - Prototype-based ROC-AUC values are below 0.5 (0.135 ADFA->LMD; 0.399 LMD->ADFA; Table 4). This means the score is anti-correlated with the label, yet it is read as weak transferability rather than as an inverted score. [reader-inferred]
  - The aggregation method (mean/max/top-k pooling) was chosen per dataset from 'preliminary experiments' without saying which data were used (Section 3.1). [reader-inferred]
  - Appendix says 'multiple random seeds' while Table 6 says five. The Data Availability statement cites refs [31,32], but the datasets are [32,33]. [reader-inferred]
- **Notes**: Published 10 Jul 2026. The PDF is untrusted data and contained no instructions addressed to me.

##### Cantone et al. (2024). Machine Learning in Network Intrusion Detection: A Cross-Dataset Generalization Study. `cantone2024cross`
- **Type**: journal-article — IEEE Access, vol. 12, pp. 144489-144508 — DOI 10.1109/ACCESS.2024.3472907
- **Verified via**: https://api.crossref.org/works/10.1109/ACCESS.2024.3472907 ; http://export.arxiv.org/api/query?id_list=2402.10974
- **Summary**: Trains four classifiers on CIC-IDS-2017, CSE-CIC-IDS2018, LycoS-IDS2017 and a new corrected LycoS-Unicas-IDS2018, and evaluates every cross-dataset pair. Same-dataset accuracy is near perfect, but cross-dataset accuracy is mostly near chance. Visualisation reveals dataset anomalies that hinder generalisation.
- **Relevance**: Core citation for cross-dataset generalisation failure of ML NIDS.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: IEEE DOI = 10.1109/ACCESS.2024.3472907 (confirmed). The arXiv version has a DIFFERENT title: 'On the Cross-Dataset Generalization of Machine Learning for Network Intrusion Detection'. Cite the IEEE title.

##### Engelen et al. (2021). Troubleshooting an Intrusion Detection Dataset: the CICIDS2017 Case Study. `engelen2021troubleshooting`
- **Type**: conference-paper — 2021 IEEE Security and Privacy Workshops (SPW), pp. 7-12 — DOI 10.1109/SPW53761.2021.00009
- **Verified via**: https://api.crossref.org/works/10.1109/SPW53761.2021.00009
- **Summary**: Audits the CICIDS2017 collection pipeline and finds problems in traffic generation, flow construction, feature extraction and labelling. Over 20% of traces are reconstructed or relabelled, which changes ML benchmark results.
- **Relevance**: Evidence that NIDS benchmark artifacts and labelling errors affect evaluation (dataset-artifact background).
- **Method weaknesses**: not assessed (read scope: abstract_only)

##### Lanvin et al. (2023). Errors in the CICIDS2017 Dataset and the Significant Differences in Detection Performances It Makes. `lanvin2023errors`
- **Type**: chapter — Risks and Security of Internet and Systems (CRiSIS 2022), Lecture Notes in Computer Science, pp. 18-33 — DOI 10.1007/978-3-031-31108-6_2
- **Verified via**: https://api.crossref.org/works/10.1007/978-3-031-31108-6_2
- **Summary**: Identifies labelling and capture flaws in CICIDS2017 (packet misordering, duplication, mislabelled attacks) and measures how correcting them changes supervised detection results.
- **Relevance**: Supports the claim that benchmark labelling and capture artifacts materially change NIDS evaluation.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Abstract obtained via Semantic Scholar API; metadata via Crossref.

##### Flood et al. (2024). Bad Design Smells in Benchmark NIDS Datasets. `flood2024bad`
- **Type**: conference-paper — 2024 IEEE 9th European Symposium on Security and Privacy (EuroS&P), pp. 658-675 — DOI 10.1109/EuroSP60621.2024.00042
- **Verified via**: https://api.crossref.org/works/10.1109/EuroSP60621.2024.00042
- **Summary**: Manual analysis of seven highly cited NIDS benchmarks finds six 'data design smells', proposes heuristics to measure them, and shows how they bias experiments and downstream literature.
- **Relevance**: Best available peer-reviewed support that benchmark design choices create exploitable artifacts. I could not confirm from the abstract whether it specifically discusses TTL in UNSW-NB15.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Full author names and pages 658-675 confirmed via Crossref DOI lookup.

##### Layeghy & Portmann (2023). Explainable Cross-domain Evaluation of ML-based Network Intrusion Detection Systems. `layeghy2023explainable`
- **Type**: journal-article — Computers and Electrical Engineering, vol. 108, pp. 108692 — DOI 10.1016/j.compeleceng.2023.108692
- **Verified via**: https://api.crossref.org/works/10.1016/j.compeleceng.2023.108692 ; http://export.arxiv.org/api/query?id_list=2205.04112 (arXiv record links this DOI)
- **Summary**: Evaluates seven supervised and unsupervised models across four benchmark NIDS datasets in cross-domain settings. No model generalises across all datasets, and generalisation is highly asymmetric when source and target are swapped. SHAP attributes failures to features strongly tied to class in one dataset but not others.
- **Relevance**: Direct prior evidence (NetFlow-based datasets from the same group) for pair-dependent, asymmetric zero-shot transfer and dataset-specific feature-label correspondences.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Summary is from the arXiv abstract. The arXiv preprint has a different title: 'On Generalisability of Machine Learning-based Network Intrusion Detection Systems'. Its record links this journal DOI, but I did not compare the two versions' contents.

##### Sarhan et al. (2023). From zero-shot machine learning to zero-day attack detection. `sarhan2023zeroshot`
- **Type**: journal-article — International Journal of Information Security, vol. 22, no. 4, pp. 947-959 — DOI 10.1007/s10207-023-00676-0
- **Verified via**: https://api.crossref.org/works/10.1007/s10207-023-00676-0
- **Summary**: Proposes a zero-shot learning evaluation for ML NIDS, in which models map NetFlow features to semantic attributes, to measure detection of attack classes unseen in training (zero-day).
- **Relevance**: Related NetFlow-dataset work on generalisation beyond training conditions. It concerns unseen classes rather than unseen networks, which helps position this study.
- **Method weaknesses**: not assessed (read scope: abstract_only)

##### Apruzzese et al. (2022). The Cross-Evaluation of Machine Learning-Based Network Intrusion Detection Systems. `apruzzese2022cross`
- **Type**: journal-article — IEEE Transactions on Network and Service Management, vol. 19, no. 4, pp. 5152-5169 — DOI 10.1109/TNSM.2022.3157344
- **Verified via**: https://api.crossref.org/works/10.1109/tnsm.2022.3157344
- **Summary**: Proposes the first formal model (XeNIDS) for cross-evaluating ML-NIDS across existing labelled datasets, showing it extends detection coverage and exposes risks hidden by single-dataset evaluation.
- **Relevance**: Supports cross-dataset evaluation as a necessary protocol and the observation that cross-dataset results differ from in-dataset results.
- **Method weaknesses**: not assessed (read scope: abstract_only)

##### D’hooge et al. (2020). Inter-dataset generalization strength of supervised machine learning methods for intrusion detection. `dhooge2020inter`
- **Type**: journal-article — Journal of Information Security and Applications, vol. 54, pp. 102564 — DOI 10.1016/j.jisa.2020.102564
- **Verified via**: https://api.crossref.org/works/10.1016/j.jisa.2020.102564
- **Summary**: Trains 12 supervised learners on CIC-IDS2017 and CSE-CIC-IDS2018 and tests inter-dataset generalisation on the shared DoS and botnet classes. Models that classify well within a dataset generalise poorly to the related dataset.
- **Relevance**: Early evidence of cross-dataset generalisation failure for NIDS.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Abstract via Semantic Scholar; the family name uses a typographic apostrophe (D’hooge).

##### Pan & Yang (2010). A Survey on Transfer Learning. `pan2010survey`
- **Type**: journal-article — IEEE Transactions on Knowledge and Data Engineering, vol. 22, no. 10, pp. 1345-1359 — DOI 10.1109/TKDE.2009.191
- **Verified via**: https://api.crossref.org/works/10.1109/TKDE.2009.191
- **Summary**: Defines transfer learning settings (inductive, transductive, unsupervised) and categorises instance-, feature-, parameter- and relational-knowledge transfer. It also discusses negative transfer.
- **Relevance**: Standard definition of the transfer setting (labelled source plus few labelled target) and of instance re-weighting approaches.
- **Method weaknesses**: not assessed (read scope: abstract_only)


#### Section: method

##### Sarhan et al. (2022). Towards a Standard Feature Set for Network Intrusion Detection System Datasets. `sarhan2022standard`
- **Type**: journal-article — Mobile Networks and Applications, vol. 27, no. 1, pp. 357-370 — DOI 10.1007/s11036-021-01843-0
- **Verified via**: https://api.crossref.org/works/10.1007/s11036-021-01843-0 ; http://export.arxiv.org/api/query?id_list=2101.11315
- **Summary**: Argues that dataset-specific proprietary feature sets prevent cross-dataset comparison of ML-based NIDS and proposes standard NetFlow-based feature sets. Evaluates a 12-feature and a 43-feature NetFlow variant (the NetFlow v2 feature set).
- **Relevance**: Primary citation for the standardised NetFlow feature set that makes the four NF datasets share a common schema, which this study relies on.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Online 10 Nov 2021, issue Feb 2022. Cite year 2022 for the issue (or 2021 for online-first). arXiv admin note: substantial overlap with arXiv:2011.09144.

##### Luay et al. (2025). Temporal Analysis of NetFlow Datasets for Network Intrusion Detection Systems. `luay2025temporal`
- **Type**: preprint — arXiv preprint — arXiv 2503.04404
- **Verified via**: http://export.arxiv.org/api/query?id_list=2503.04404 (arXiv record links DOI 10.1109/ACCESS.2026.3688204); local PDF v3 read in full
- **Summary**: Releases the NetFlow v3 (NF3) versions of UNSW-NB15, BoT-IoT, ToN-IoT and CSE-CIC-IDS2018, regenerated from PCAPs with nProbe. They keep the 43 v2 features and add flow start/end timestamps and src/dst inter-arrival-time statistics (Table 1). The paper describes the data (flow-length and IAT distributions, per-minute time series, unique IP/port counts, spectrograms) but trains no classifier. Key numbers: totals of 2.37M / 20.1M / 27.5M / 16.9M flows, with malicious shares of 5.40% / 12.93% / 38.98% / 99.7% (Table 2). Attacks run on separate days except UNSW-NB15, where they run simultaneously (Table 4).
- **Relevance**: Primary citation for the four NetFlow v3 datasets used in this study (feature list, class composition). Its tables also document source-host and day-level confounds (few unique IPs, attacks on separate days) relevant to the domain-separability findings.
- **Method weaknesses** (read: full text by AI agent; NOT an author reading attestation)
  - No ML model is trained or evaluated; the paper is descriptive only (Section 5 intro: 'This analysis is not aimed at classifying or predicting'). It therefore gives no cross-dataset, transfer or target-only results. [author-acknowledged, section: 5 (intro), 2]
  - Does not warn about TTL or any other dataset-identifying/artifact feature. MIN_TTL/MAX_TTL/DNS_TTL_ANSWER are listed only as ordinary features (Table 1, p.6). I checked Sections 1-6 (pp.1-19) and found no discussion of shortcut or leakage features. [reader-inferred]
  - Table 5 (p.16) shows NF3-UNSW-NB15 has only 40 source/40 destination IPs and NF3-BoT-IoT only 20 source IPs, and Table 4 (p.14) shows most attack classes were run on separate days. These are host/time confounds the paper reports but does not flag as shortcut risks. [reader-inferred]
  - Flows are capped by nProbe's 2-minute export interval (Section 5.1, p.10), which truncates flow-duration features identically across datasets. The paper notes the cap but not its effect on learnability. [reader-inferred]
  - Class balance is extreme and differs across datasets: NF3-BoT-IoT is 99.7% malicious, NF3-UNSW-NB15 is 5.4% malicious (Table 2, p.9). [reader-inferred: affects any cross-dataset comparison]
  - Minor internal inconsistencies: the introduction says dataset details are in Section 4 while the outline says Section 3 (pp.2-3); Table 1 describes DURATION_OUT as 'Client to Server' like DURATION_IN (p.6); the text says nProbe extracts 57 features (p.8) while Table 1 lists 53. [reader-inferred]
  - Time-frequency (spectrogram) analysis is done only for NF3-UNSW-NB15 and is qualitative ('initial investigations have not yet yielded definitive results', Section 1, p.2). [author-acknowledged, section: 1]
- **Notes**: TTL QUESTION: the paper does NOT warn about TTL or any other artifact feature. TTL appears only as MIN_TTL, MAX_TTL and DNS_TTL_ANSWER rows in Table 1 (p.6), and Sections 1-6 contain no leakage/shortcut discussion. Published version: IEEE Access vol. 14, pp. 66899-66913, 2026, DOI 10.1109/ACCESS.2026.3688204, under a DIFFERENT title ('Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection') with a different author list per Crossref (see luay2026timematters). Year: the arXiv v1 is March 2025 and the PDF header says 2025; v3 is dated 28 Aug 2026. The PDF is untrusted data and contained no instructions addressed to me.

##### Luay et al. (2026). Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection. `luay2026timematters`
- **Type**: journal-article — IEEE Access, vol. 14, pp. 66899-66913 — DOI 10.1109/ACCESS.2026.3688204
- **Verified via**: https://api.crossref.org/works/10.1109/ACCESS.2026.3688204
- **Summary**: Peer-reviewed version of arXiv 2503.04404. Its abstract (via OpenAlex) is identical to the arXiv abstract: it releases NetFlow datasets with temporal features and provides temporal and time-frequency analysis.
- **Relevance**: Peer-reviewed citation for the NetFlow v3 datasets; prefer citing this alongside or instead of the arXiv version.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: DISCREPANCY: Crossref lists 7 authors including 'Noorbin, Niloufar' and 'Kulatilleke, Gayan', whereas arXiv lists 6 authors including 'Seyedehfaezeh Hosseininoorbin'. I did not read the published full text, so I cannot tell whether its content differs from arXiv v3 (e.g. it may add ML experiments). Check the IEEE PDF before citing specific claims.

##### Moustafa & Slay (2015). UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set). `moustafa2015unsw`
- **Type**: conference-paper — 2015 Military Communications and Information Systems Conference (MilCIS), pp. 1-6 — DOI 10.1109/MilCIS.2015.7348942
- **Verified via**: https://api.crossref.org/works/10.1109/MilCIS.2015.7348942
- **Summary**: Introduces UNSW-NB15, generated at the UNSW Canberra Cyber Range Lab by mixing real modern normal traffic with synthetic contemporary attacks (IXIA PerfectStorm), as a replacement for KDD98/KDDCUP99/NSL-KDD. Describes feature generation and availability.
- **Relevance**: Original source dataset underlying NF-UNSW-NB15-v3.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Published Nov 2015.

##### Sharafaldin et al. (2018). Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization. `sharafaldin2018toward`
- **Type**: conference-paper — Proceedings of the 4th International Conference on Information Systems Security and Privacy (ICISSP), pp. 108-116 — DOI 10.5220/0006639801080116
- **Verified via**: https://api.crossref.org/works/10.5220/0006639801080116
- **Summary**: Reviews eleven IDS datasets since 1998 as outdated or unrealistic and presents a new dataset generated from profiled benign behaviour and common attack scenarios, with flow features extracted by CICFlowMeter.
- **Relevance**: Standard citation for the CIC dataset family underlying NF-CSE-CIC-IDS2018-v3.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: CAUTION: this ICISSP 2018 paper introduces CICIDS2017. CSE-CIC-IDS2018 has no separate peer-reviewed paper and is conventionally cited to this paper plus the UNB/CIC dataset web page. The NF3 paper does the same (its ref [23]). Crossref author family name: 'Habibi Lashkari'.

##### Moustafa (2021). A new distributed architecture for evaluating AI-based security systems at the edge: Network TON_IoT datasets. `moustafa2021tonnetwork`
- **Type**: journal-article — Sustainable Cities and Society, vol. 72, pp. 102994 — DOI 10.1016/j.scs.2021.102994
- **Verified via**: https://api.crossref.org/works/10.1016/j.scs.2021.102994
- **Summary**: Presents the UNSW Canberra IoT testbed (SDN/NFV, edge-fog-cloud) used to execute normal and attack scenarios and collect the network portion of the TON_IoT datasets.
- **Relevance**: Primary citation for the network traffic of ToN-IoT, the source of NF-ToN-IoT-v3 (also the reference used by the NF3 paper).
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Use together with or instead of alsaedi2020ton (the telemetry part).

##### Alsaedi et al. (2020). TON_IoT Telemetry Dataset: A New Generation Dataset of IoT and IIoT for Data-Driven Intrusion Detection Systems. `alsaedi2020ton`
- **Type**: journal-article — IEEE Access, vol. 8, pp. 165130-165150 — DOI 10.1109/ACCESS.2020.3022862
- **Verified via**: https://api.crossref.org/works/10.1109/ACCESS.2020.3022862
- **Summary**: Introduces the telemetry (IoT/IIoT sensor) part of TON_IoT with binary and attack-type labels and evaluates ML IDSs on it.
- **Relevance**: Companion ToN_IoT dataset paper; cite alongside moustafa2021tonnetwork.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: This covers telemetry data, not the network flows used by NF-ToN-IoT.

##### Koroniotis et al. (2019). Towards the development of realistic botnet dataset in the Internet of Things for network forensic analytics: Bot-IoT dataset. `koroniotis2019bot`
- **Type**: journal-article — Future Generation Computer Systems, vol. 100, pp. 779-796 — DOI 10.1016/j.future.2019.05.041
- **Verified via**: https://api.crossref.org/works/10.1016/j.future.2019.05.041
- **Summary**: Presents Bot-IoT, combining legitimate and simulated IoT traffic with botnet attacks captured in a realistic testbed, and evaluates it with statistical and ML methods.
- **Relevance**: Original source dataset underlying NF-BoT-IoT-v3.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Nov 2019 issue. arXiv version 1811.00701 (not opened).

##### Sarhan et al. (2021). NetFlow Datasets for Machine Learning-Based Network Intrusion Detection Systems. `sarhan2021netflow`
- **Type**: chapter — Big Data Technologies and Applications (BDTA 2020), LNICST, pp. 117-135 — DOI 10.1007/978-3-030-72802-1_9
- **Verified via**: https://api.crossref.org/works/10.1007/978-3-030-72802-1_9 ; http://export.arxiv.org/api/query?id_list=2011.09144
- **Summary**: Generates NetFlow-format versions of UNSW-NB15, BoT-IoT, ToN-IoT and CSE-CIC-IDS2018 from their PCAPs (the v1 NF datasets) to provide a common feature set for cross-dataset evaluation.
- **Relevance**: Origin of the NF dataset series (v1) that NF-v3 extends.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Part B addition.

##### Shimodaira (2000). Improving predictive inference under covariate shift by weighting the log-likelihood function. `shimodaira2000improving`
- **Type**: journal-article — Journal of Statistical Planning and Inference, vol. 90, no. 2, pp. 227-244 — DOI 10.1016/S0378-3758(00)00115-4
- **Verified via**: https://api.crossref.org/works/10.1016/S0378-3758(00)00115-4
- **Summary**: Introduces covariate shift and shows that weighting the log-likelihood by the density ratio of test to training inputs corrects estimation under misspecification.
- **Relevance**: Foundational citation for the importance-weighted transfer variant.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Abstract not available through the APIs (publisher elides it); summary is from general knowledge of this paper's well-known content. Metadata verified.

##### Sugiyama et al. (2007). Covariate Shift Adaptation by Importance Weighted Cross Validation. `sugiyama2007covariate`
- **Type**: journal-article — Journal of Machine Learning Research, vol. 8, no. 35, pp. 985-1005 — https://jmlr.org/papers/v8/sugiyama07a.html
- **Verified via**: https://jmlr.org/papers/v8/sugiyama07a.html
- **Summary**: Proposes importance-weighted cross-validation (IWCV), which is unbiased under covariate shift, for model selection when training and test input distributions differ.
- **Relevance**: Supports importance weighting under covariate shift (method background) and the need for weighted validation.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: JMLR page shows '8(35):985-1005, 2007'; no DOI.

##### Ganin et al. (2016). Domain-Adversarial Training of Neural Networks. `ganin2016domain`
- **Type**: journal-article — Journal of Machine Learning Research, vol. 17, no. 59, pp. 1-35 — arXiv 1505.07818
- **Verified via**: https://jmlr.org/papers/v17/15-239.html ; http://export.arxiv.org/api/query?id_list=1505.07818
- **Summary**: Learns features that are discriminative for the task but indistinguishable between source and target domains, using a gradient-reversal layer against a domain classifier, motivated by domain-adaptation theory.
- **Relevance**: Motivates the domain classifier as a measure of shift: if a classifier separates domains (AUC about 1), invariant features have not been found.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: The JMLR page renders the 7th author as 'Mario March' (truncated). arXiv lists 'Mario Marchand', which I use.

##### Rabanser et al. (2019). Failing Loudly: An Empirical Study of Methods for Detecting Dataset Shift. `rabanser2019failing`
- **Type**: conference-paper — Advances in Neural Information Processing Systems 32 (NeurIPS 2019) — arXiv 1810.11953
- **Verified via**: https://proceedings.neurips.cc/paper_files/paper/2019/hash/846c260d715e5b854ffad5f70a516c88-Abstract.html ; http://export.arxiv.org/api/query?id_list=1810.11953
- **Summary**: Compares methods for detecting dataset shift (dimensionality reduction plus two-sample tests, and domain classifiers) across shift types. A domain-discriminating classifier is useful for characterising shift, and simple approaches often work well.
- **Relevance**: Supports using a domain classifier as a shift detector and characteriser (the AUC about 1 separability analysis).
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: NeurIPS page lists the author as 'Zachary Lipton' and arXiv as 'Zachary C. Lipton'. Page numbers not recorded; no DOI.

##### Wilcoxon (1945). Individual Comparisons by Ranking Methods. `wilcoxon1945individual`
- **Type**: journal-article — Biometrics Bulletin, vol. 1, no. 6, pp. 80 — DOI 10.2307/3001968
- **Verified via**: https://api.crossref.org/works/10.2307/3001968
- **Summary**: Introduces rank-based tests for paired and unpaired comparisons, including the signed-rank test for paired differences.
- **Relevance**: Citation for the paired Wilcoxon signed-rank tests (540 tests).
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Crossref gives first page 80 only; the commonly cited range 80-83 is UNVERIFIED here.

##### Holm (1979). A Simple Sequentially Rejective Multiple Test Procedure. `holm1979simple`
- **Type**: journal-article — Scandinavian Journal of Statistics, vol. 6, pp. 65-70 — https://www.jstor.org/stable/4615733
- **Verified via**: https://api.openalex.org/works?search=simple%20sequentially%20rejective%20multiple%20test%20procedure (record W2121044470)
- **Summary**: Introduces the step-down (Holm) procedure, which controls the family-wise error rate and is uniformly more powerful than plain Bonferroni.
- **Relevance**: Citation for the Holm correction applied to the Wilcoxon tests.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Verified via OpenAlex only (title, author, year, vol 6, pp 65-70); the JSTOR page blocked automated access. OpenAlex lists DOI 10.2307/4615733, but doi.org returned HTTP 404, so doi is set to null. Issue number (2) is UNVERIFIED and left null.

##### Demšar (2006). Statistical Comparisons of Classifiers over Multiple Data Sets. `demsar2006statistical`
- **Type**: journal-article — Journal of Machine Learning Research, vol. 7, no. 1, pp. 1-30 — https://jmlr.org/papers/v7/demsar06a.html
- **Verified via**: https://jmlr.org/papers/v7/demsar06a.html
- **Summary**: Reviews practice and recommends non-parametric tests for comparing classifiers over multiple data sets: the Wilcoxon signed-ranks test for two classifiers and Friedman with post-hoc tests (CD diagrams) for more.
- **Relevance**: Justifies using Wilcoxon signed-rank tests for paired classifier/strategy comparisons.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: JMLR page shows 7(1):1-30, 2006; no DOI.

##### Grinsztajn et al. (2022). Why do tree-based models still outperform deep learning on typical tabular data?. `grinsztajn2022why`
- **Type**: conference-paper — Advances in Neural Information Processing Systems 35 (NeurIPS 2022), Datasets and Benchmarks Track — arXiv 2207.08815
- **Verified via**: https://papers.nips.cc/paper_files/paper/2022/hash/0378c7692da36807bdec87ab043cdadc-Abstract-Datasets_and_Benchmarks.html ; http://export.arxiv.org/api/query?id_list=2207.08815
- **Summary**: Benchmarks deep learning against tree ensembles (XGBoost, RF) on 45 medium-sized tabular datasets with extensive tuning. Trees remain state of the art, and the paper analyses the inductive biases behind this.
- **Relevance**: Optional: justifies RF/GBT as strong tabular baselines alongside an MLP.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: TITLE DIFFERS: the NeurIPS proceedings title includes 'typical' ('...on typical tabular data?'); arXiv v1 omits it. Use the NeurIPS title. Author names have accents on the NeurIPS page omitted; arXiv uses Léo/Gaël.


#### Section: discussion

##### Ben-David et al. (2010). A theory of learning from different domains. `bendavid2010theory`
- **Type**: journal-article — Machine Learning, vol. 79, no. 1-2, pp. 151-175 — DOI 10.1007/s10994-009-5152-4
- **Verified via**: https://api.crossref.org/works/10.1007/s10994-009-5152-4
- **Summary**: Bounds target error by source error plus a classifier-induced divergence between domains that can be estimated from unlabelled data. Also analyses how to weight a small labelled target set against a large source set.
- **Relevance**: Theoretical basis for using a domain classifier as a divergence measure, and for why combining source and few target labels can fail when divergence is large. Directly matches this study's design.
- **Method weaknesses**: not assessed (read scope: abstract_only)
- **Notes**: Online Oct 2009, issue May 2010; cite 2010.

##### Zhang et al. (2023). A Survey on Negative Transfer. `zhang2023negative`
- **Type**: journal-article — IEEE/CAA Journal of Automatica Sinica, vol. 10, no. 2, pp. 305-329 — DOI 10.1109/JAS.2022.106004
- **Verified via**: https://api.crossref.org/works/10.1109/JAS.2022.106004
- **Summary**: Defines negative transfer (source data reducing target performance), reviews its causes, and surveys over fifty mitigation approaches grouped into domain-similarity estimation, safe transfer and NT mitigation.
- **Relevance**: Supports interpreting cases where pooled, weighted or fine-tuned source data underperform target-only training as negative transfer.
- **Method weaknesses**: not assessed (read scope: abstract_only)
