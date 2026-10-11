# Paper Outline — TRACE-IDS

*✅ Approved by the author 2026-10-11 ("approve outline"). Phase 2 (structure). Inputs: `../paper_configuration_record.md`, `../phase1_literature/literature_search_report.md`. Generated 2026-10-11. Needs the author's approval before any drafting.*

**Working title:** *Is It Transfer? Source Data Adds Nothing to Few-Shot Cross-Dataset Intrusion Detection on NetFlow*
(Alternative: *Few Labels, No Transfer: …*. The title is the author's choice.)

**Author:** Rijan Rayamajhi (sole author) · **Target:** arXiv cs.CR → *Computers & Security* · **IEEE citations, LaTeX, ~7,000 words, English abstract**

Review criteria binding: `criteria_binding_unavailable`. No venue criteria profile was declared, so this outline makes no claim about fitting a venue.

---

## Structure Pattern: IMRaD, with a separate "Mechanism" results section and a short "Recommended Protocol" section

## Overview

The paper tests the assumption behind recent few-shot cross-dataset NIDS work (TAN-IDS; Hakim et al.): that when a detector moves to a new network and a few target flows are labelled, the source dataset helps.

1. **Data and protocol.** We use the four NetFlow v3 datasets and a leak-free, 10-seed protocol. Each adaptation method is compared against the baseline those works omit: training on the same k target flows alone.
2. **Results.** The source gives no consistent benefit and often hurts (540 paired tests, 12 pairs, 3 models, 3 methods). Zero-shot transfer is weak and pair-dependent. A positive zero-shot result from prior work does not reproduce.
3. **Mechanism.** Each network occupies its own region of feature space. Two robustness checks show the result is not an artifact: it holds on raw features (23–40 of 45 features must go before the domains blur) and under shared scaling. The shared-scaling check also exposes per-domain normalization as a hidden confound.
4. **Practical message.** Before crediting a source dataset, compare against target-only training at the same label budget.

## Sub-questions (each section names the one it serves)

- **SQ1:** With k labelled target flows per class, does adding source data (pooled, importance-weighted, fine-tuned) beat training on those k flows alone?
- **SQ2:** How well does zero-shot transfer work, and do published positive results reproduce on NetFlow v3?
- **SQ3:** Why doesn't the source help? How separable are the domains, and does the source help on attack types it shares with the target?
- **SQ4:** Is the result an artifact, either of a few known artifact features (TTL) or of preprocessing (per-domain scaling)?

---

## ⚠️ Decisions needed from the author before drafting

| # | Decision | Options | Recommendation |
|---|---|---|---|
| D1 | ✅ **Author chose A (2026-10-11).** **Which scaling is the "main" setting?** E1, E4 and E5 ran with per-domain scaling only; E2/E3 ran with both. | **A.** Per-domain is the main setting, with shared scaling as a side-by-side robustness column in the main table. No new compute; every experiment uses one consistent setting. **B.** Shared is the main setting; re-run E1, E4 and E5 under shared scaling (about 4–5 h). | **A.** It is consistent across all experiments, and the shared-scaling check is reported in full next to the main result, where it strengthens the claim. |
| D2 | **TTL citations** | ✅ Resolved 2026-10-11: both Sarhan papers read; TTL claims verified with locators (see literature report, Correction 1). | Done |
| D3 | **Dataset table (Table 1)** | There is no committed script yet that prints row counts and attack rates for all four processed datasets (GUARDRAILS B1). | Add a 10-line `src/dataset_table.py` before drafting §3. |

---

## Detailed Outline

### Abstract (~200 words, English)
**Serves:** all SQs. Covers the problem (prior work credits the source without a target-only baseline), the setup (4 NF v3 datasets, 12 pairs, 3 models × 3 methods, 10 seeds), the headline result (source helps in 6% of 540 tests and hurts in 28%; 8% / 38% under shared scaling), the mechanism (domains are separable, AUC ≥ 0.996), and the recommendation (always report target-only).

### 1. Introduction (~900 words)
**Purpose:** Establish why "does the source help?" is an open and consequential question, and state contributions.
**Serves:** framing (no sub-question binding).
- 1.1 *Cross-dataset failure is well documented.* ML-NIDS models collapse on unseen networks. → cantone2024cross, apruzzese2022cross, dhooge2020inter, layeghy2023explainable, sommer2010outside
- 1.2 *The current remedy (adapt with a few target labels) is evaluated without the obvious baseline.* TAN-IDS reports recovery with 5% target labels but never trains on those labels alone, in a single run. Hakim et al. likewise; their authors acknowledge the missing condition (§6.3). → hathanh2026tanids, hakim2026crossdomain, roszeitis2026fewshot
- 1.3 *Why this matters.* Shortcut learning and benchmark artifacts can make apparent transfer illusory. → arp2022dos, geirhos2020shortcut, goldschmidt2025network
- 1.4 *Contributions* (numbered):
  - (C1) a leak-free, multi-seed protocol with a target-only baseline;
  - (C2) a 12-pair, 3-model, 3-method test showing no consistent source benefit;
  - (C3) a non-reproduction of a published zero-shot result on NF v3;
  - (C4) a mechanism: domain separability, feature-ablation depth, and the scaling confound;
  - (C5) a recommended evaluation protocol.
- **Transition:** the paper positions these against three bodies of prior work.

### 2. Related Work (~1,300 words)
**Purpose:** Show precisely what prior work did and did not test; set up the gap.
**Serves:** SQ1, SQ2, SQ4 (positioning).
- 2.1 *Cross-dataset generalization in NIDS* → cantone2024cross, layeghy2023explainable, apruzzese2022cross, dhooge2020inter, atif2026threeaxis (zero-shot UNSW→CIC 0.81; feature set chosen on target F1, §3.3), hakim2026crossdomain
- 2.2 *Few-shot and transfer adaptation for NIDS* → hathanh2026tanids, sarhan2023zeroshot, roszeitis2026fewshot. Studies that do include a target-only baseline: xu2025multimodal (packets, near-domain CIC-2017↔2018; source pretraining hurts at K=5) and kim2026prototype (host logs; n=5 seeds, so no test can reach p<0.05). **Gap statement (search-bounded, 2026-10-11):** no screened NetFlow study isolates the source's contribution with an adequately powered target-only comparison.
- 2.3 *Dataset artifacts and shortcut learning* → arp2022dos, geirhos2020shortcut, engelen2021troubleshooting, lanvin2023errors, flood2024bad, roy2026unmasking, apruzzese2023sok, goldschmidt2025network; TTL → sarhan2021featureanalysis (§5.1.1, 'hidden label', original UNSW-NB15), sarhan2022standard (§4: dropped for extreme label correlation, NF-UNSW-NB15-v2), atif2026threeaxis (§3.3, NF v2); none check NF v3; NetFlow feature sets → sarhan2022standard, sarhan2021featureanalysis
- 2.4 *Transfer learning, negative transfer, covariate shift* (brief theory anchor) → pan2010survey, bendavid2010theory, zhang2023negative, shimodaira2000improving, sugiyama2007covariate, ganin2016domain
- **Transition:** none of these isolate the source with target-only training under repeated, tested runs. Section 3 builds that protocol.

### 3. Data and Experimental Protocol (~1,100 words)
**Purpose:** Make every result reproducible and the comparison fair.
**Serves:** SQ1–SQ4 (method).
- 3.1 *Datasets.* NF-CICIDS2018-v3, NF-UNSW-NB15-v3, NF-ToN-IoT-v3, NF-BoT-IoT-v3: 45 shared features after dropping identifiers and 2 sparse columns, subsampled to ~2M flows each, all benign flows kept for BoT. **Table 1** (needs D3). Attack families are mapped to shared categories. → luay2025temporal / luay2026timematters, sarhan2021netflow, moustafa2015unsw, sharafaldin2018toward, moustafa2021tonnetwork, alsaedi2020ton, koroniotis2019bot
- 3.2 *Leak-free protocol.* Per seed, the target is split 50/50 into an unlabelled pool and a test set; normalization statistics come only from the source sample and the pool; few-shot draws are nested across k ∈ {1, 5, 10, 50, 100}; 10 seeds. Scaling: per-domain (main, per D1) and shared (robustness). → `src/common.py`
- 3.3 *Models and adaptation methods.* RF, histogram GBT, MLP. Methods: target-only, pooled (equal weight per domain and class), importance-weighted (domain-classifier density ratio, effective sample size reported), fine-tuned (RF warm start, GBT frozen init, MLP continued SGD). Hyper-parameters are fixed in advance; GBT leaf size is scaled to the training-set size so target-only is not handicapped. → shimodaira2000improving, sugiyama2007covariate, grinsztajn2022why; `src/e2_transfer.py`
- 3.4 *Statistics.* Paired two-sided Wilcoxon over seeds per (pair, model, method, k); Holm correction over 540; verdict counts; F1, recall, FPR and balanced accuracy. → wilcoxon1945individual, holm1979simple, demsar2006statistical; `src/e3_analysis.py`
- 3.5 *Mechanism probes.* Domain-classifier AUC (all flows / benign / within attack category); per-attack-category recall; RF importance overlap; greedy feature ablation; single-feature raw vs z-scored AUC. → ganin2016domain, rabanser2019failing; `src/e5_mechanism.py`, `src/e5_ablation.py`
- **Transition:** with the protocol fixed, Section 4 answers SQ1 and SQ2.

### 4. Results: Does the Source Help? (~1,300 words)
**Purpose:** Answer SQ1 and SQ2 with the main numbers.
- 4.1 *Single pair, single model (E1).* CIC↔UNSW with RF: source + k is within noise of target-only at every k. → `results/e1_summary.csv`, **Fig. 1** `e1_recovery.png`
- 4.2 *Stronger baselines (E2).* 3 models × 3 methods on CIC↔UNSW: 90 tests, source better 0, worse 25. → `e3_significance.csv` (CIC↔UNSW rows), **Fig. 2** `e2_transfer.png`
- 4.3 *All 12 pairs (E3).* **Table 2**, the core result: verdict counts by method, model and k, with a per-domain column (help 34 / no diff 353 / hurt 153) and a shared column (41 / 294 / 205). Median ΔF1 −0.011 / −0.025. Holm: no single cell significant, so the claim is stated as a pattern. Fine-tuning is worst under per-domain scaling (72 hurt / 10 help); under shared scaling, fine-tuning and importance weighting hurt about equally (73 vs 74). **Fig. 3** heatmaps (`e3_heatmap.png`, `e3_heatmap_shared.png`).
- 4.4 *Zero-shot (SQ2).* Best-model balanced accuracy is 0.61–0.71 on 5 pairs and ~0.5 elsewhere (shared scaling: 0.68–0.76 on 4); target-only at k=10 reaches 0.78–0.94 and beats zero-shot on every pair under both scalings (`e3_zeroshot*.csv`, `e3_targetonly_bacc*.csv`). Atif & Ali's Set C 0.81 does not reproduce (Set C F1 0.21, balanced accuracy ≤ 0.55 for every feature set; `e4_zeroshot_summary.csv`).
- 4.5 *TAN-IDS budget (E4b).* At a 5% label budget, target-only ≈ pooled ≈ fine-tune (`e4_budget_summary.csv`).
- **Transition:** if the source carries no usable signal, Section 5 asks why.

### 5. Results: Why Doesn't the Source Help? (~1,000 words)
**Purpose:** Answer SQ3 and SQ4.
- 5.1 *Domains are separable* (E5-B): AUC ≥ 0.996 for every pair (minimum: DoS vs DoS), including benign-only and the same attack category (`e5_distance.csv`).
- 5.2 *Shared attack types don't transfer* (E5-A): there is no gain on categories the source contains; adding the source lowers FPR but costs recall (`e5_families_summary.csv`, **Fig. 4** `e5_families.png`). RF importance overlap of 0.25–0.83 loosely tracks benefit; this is exploratory, n=12.
- 5.3 *Not one artifact column* (SQ4): on raw features, 23–40 of 45 features must be removed before AUC < 0.9 (all flows; 17–39 benign-only); TTL is among the first removed. In E1, removing TTL lowers few-shot F1 for every method alike (CIC→UNSW k=5: 0.70→0.54 source+k, 0.70→0.50 target-only), so it does not change the source-vs-target comparison (`e5_ablation_summary.csv`, **Fig. 5** `e5_ablation.png`).
- 5.4 *The scaling confound* (SQ4): single features with AUC ≥ 0.99 number 13/270 raw vs 231/270 after per-domain z-scoring (`e5_single_feature.csv`). Under shared scaling the source still doesn't help, and the ToN→CIC exception disappears (9 helps → 0).
- **Transition:** Section 6 interprets these findings against prior claims.

### 6. Discussion (~900 words)
**Purpose:** Interpret, reconcile with prior work, state limits.
- 6.1 *Reconciling with TAN-IDS and Hakim:* their "recovery" is what the target labels alone achieve. → hathanh2026tanids, hakim2026crossdomain, xu2025multimodal, kim2026prototype
- 6.2 *Negative transfer as the expected outcome under large domain divergence.* → bendavid2010theory, zhang2023negative, pan2010survey
- 6.3 *Implications for NIDS benchmarks:* the networks differ across most features, so cross-dataset "transfer" numbers mostly measure the target labels. → arp2022dos, flood2024bad, goldschmidt2025network, luay2025temporal (few IPs, attacks on separate days)
- 6.4 *Limitations:* four public testbeds; binary task; three model families (no deep sequence models); 10 seeds limit per-cell power (none survive Holm); fixed hyper-parameters; NetFlow v3 only; offline evaluation.

### 7. Recommended Protocol (~300 words)
**Purpose:** The citable, practical takeaway.
- Always report target-only at the same label budget.
- Use multiple seeds and paired tests.
- Report FPR or balanced accuracy, not recall alone.
- Compute normalization from training-visible data only, and check per-domain scaling.
- Report domain-classifier AUC.
- Ablate known artifact features.

### 8. Conclusion (~200 words)
One paragraph restating C1–C5. Future work: real-network data and multiclass tasks.

### Back matter
Data availability (public datasets plus the GitHub repo and `run_all.sh`) · Code availability · AI-use disclosure · Funding: none · Conflict of interest: none · CRediT: sole author.

---

## Evidence Map (all 41 sources assigned)

| Section | Sources |
|---|---|
| 1 Introduction | cantone2024cross, apruzzese2022cross, dhooge2020inter, layeghy2023explainable, sommer2010outside, hathanh2026tanids, hakim2026crossdomain, roszeitis2026fewshot, arp2022dos, geirhos2020shortcut, goldschmidt2025network |
| 2.1 Cross-dataset | cantone2024cross, layeghy2023explainable, apruzzese2022cross, dhooge2020inter, atif2026threeaxis, hakim2026crossdomain |
| 2.2 Few-shot / transfer NIDS | hathanh2026tanids, sarhan2023zeroshot, roszeitis2026fewshot, xu2025multimodal, kim2026prototype |
| 2.3 Artifacts / shortcuts | arp2022dos, geirhos2020shortcut, engelen2021troubleshooting, lanvin2023errors, flood2024bad, roy2026unmasking, apruzzese2023sok, goldschmidt2025network, atif2026threeaxis, sarhan2022standard, sarhan2021featureanalysis |
| 2.4 Transfer theory | pan2010survey, bendavid2010theory, zhang2023negative, shimodaira2000improving, sugiyama2007covariate, ganin2016domain |
| 3.1 Datasets | luay2025temporal, luay2026timematters, sarhan2021netflow, sarhan2022standard, moustafa2015unsw, sharafaldin2018toward, moustafa2021tonnetwork, alsaedi2020ton, koroniotis2019bot |
| 3.3 Methods | shimodaira2000improving, sugiyama2007covariate, grinsztajn2022why |
| 3.4 Statistics | wilcoxon1945individual, holm1979simple, demsar2006statistical |
| 3.5 Mechanism probes | ganin2016domain, rabanser2019failing |
| 6 Discussion | hathanh2026tanids, hakim2026crossdomain, xu2025multimodal, kim2026prototype, bendavid2010theory, zhang2023negative, pan2010survey, arp2022dos, flood2024bad, goldschmidt2025network, luay2025temporal |

## Result-to-Section Map (every number must trace to a committed output; GUARDRAILS B1)

| Claim | Output file | Script |
|---|---|---|
| E1 single-pair curves, ±TTL | `results/e1_summary.csv`, `e1_recovery.png` | `e1_fewshot.py` |
| 90 / 540 verdict counts, ΔF1 | `e3_significance.csv`, `e3_significance_shared.csv` | `e3_analysis.py` |
| Zero-shot balanced accuracy, target-only balanced accuracy | `e3_zeroshot*.csv`, `e3_targetonly_bacc*.csv` | `e3_analysis.py` |
| Atif & Ali replication, TAN-IDS budget | `e4_zeroshot_summary.csv`, `e4_budget_summary.csv` | `e4_checks.py` |
| Domain AUC, families, importance | `e5_distance.csv`, `e5_families_summary.csv`, `e5_importance.csv` | `e5_mechanism.py` |
| Ablation depth, single-feature confound | `e5_ablation_summary.csv`, `e5_single_feature.csv` | `e5_ablation.py` |
| Table 1 dataset stats | **missing (D3)** | to add |

## Word Count Summary

| Section | Words |
|---|---|
| Abstract | 200 (not counted) |
| 1 Introduction | 900 |
| 2 Related Work | 1,300 |
| 3 Data & Protocol | 1,100 |
| 4 Results: Does the source help? | 1,300 |
| 5 Results: Why not? | 1,000 |
| 6 Discussion | 900 |
| 7 Recommended Protocol | 300 |
| 8 Conclusion | 200 |
| **Total (body)** | **7,000** |

No section exceeds 35% of the total. Figures: 5. Tables: 2 main (+ appendix per-pair tables).

`criteria_binding_unavailable`
