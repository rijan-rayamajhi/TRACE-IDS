# Gap check — three-way scan (WHY / HOW / WHAT)

**Question:** Has prior work already shown that source data adds nothing over a target-only baseline in
few-shot cross-dataset network intrusion detection?

**Date:** 2026-10-10 · **Mode:** ARS deep-research `three-way-scan` · **Scan scope:** 6 named papers + 2 found by search.

**Read scope (honest):** papers were read through automated web retrieval and summaries of the fetched
text, not read by the author. Per ARS rules, method weaknesses are marked `reader-inferred` and stay
provisional until the author reads each paper and records it with `/ars-mark-read`.

---

## Per-paper scan

### 1. Hakim, Uddin & Anis — *Cross-Domain Generalization Failure in Lightweight Intrusion Detection Models for IIoT Networks*
Source: arXiv | 2026 | https://arxiv.org/abs/2607.00553
- **WHY:** Lightweight IIoT IDS models fail on unseen networks. The paper asks whether recovery is possible with limited target exposure.
- **HOW:** Train on Edge-IIoTset, test on Gotham (and WUSTL-IIoT-2021); recovery uses fractions of a Gotham adaptation pool (5%–25%).
- **WHAT:** Recovery varies strongly by architecture; models lean on port-category shortcut features.
  - **Method weaknesses** (empirical; read: HTML via automated retrieval)
    - No target-only baseline. The authors state that the study "does not include a DecisionTree-refit-on-small-sample-alone condition". [author-acknowledged, quote]
    - Recovery is evaluated on Gotham only. [author-acknowledged, quote: "few-shot recovery is evaluated on Gotham only"]
    - Tree and neural models are adapted differently (refit vs fine-tune), so architecture and adaptation method are confounded. [reader-inferred]

### 2. Roy & Minu — *Unmasking Shortcut Learning in IoT Intrusion Detection*
Source: arXiv | 2026 | https://arxiv.org/abs/2609.28725
- **WHY:** IoT NIDS benchmarks reward shortcuts (static IP/MAC addresses, timestamps).
- **HOW:** One dataset (CyberFlowIoT-GICAP), PCAP-disjoint splits, 4 learning paradigms × 4 feature configurations.
- **WHAT:** About 92.6% macro-F1 from flow behaviour alone; random flow splitting inflates recall by up to 14 points; proposes a 4-point evaluation checklist.
  - **Method weaknesses:** not assessed (read scope: abstract_only)

### 3. Atif & Ali — *A Three-Axis Stress Test of LLM vs Classical ML for NIDS under Distribution Shift and Adversarial Evasion*
Source: arXiv | 2026 | https://arxiv.org/abs/2609.13511
- **WHY:** Same-dataset evaluation hides opposite conclusions across axes (shift vs adversarial).
- **HOW:** NF-UNSW-NB15-**v2** ↔ NF-CSE-CIC-IDS2018-**v2**; XGBoost/RF (4 seeds) vs RoBERTa-LoRA (1 seed); balanced 50k flows/class; staged leakage ablation: Set A (−TTL), B (−packet length), C (−SERVER_TCP_FLAGS, TCP_WIN_MAX_IN/OUT).
- **WHAT:** Zero-shot UNSW→CIC XGBoost F1 jumps from 0.05 (Set A) to **0.81 (Set C)**; CIC→UNSW stays at 0.07. Transfer is "strongly directional". No labeled target data, no few-shot, no target-only baseline.
  - **Method weaknesses** (empirical; read: HTML via automated retrieval)
    - Target-domain F1 was used to decide which features "leak", so the target set shaped the final schema. [reader-inferred, from Sec. III-C description]
    - The test set is balanced 50k/class, which inflates F1 compared with real base rates. [reader-inferred]
    - The authors limit the claims to two networks and binary labels. [author-acknowledged, section: Sec. VI]
  - ⚠️ **Conflicts with our zero-shot ≈ chance finding for UNSW→CIC.** Its feature schema (Set C) must be replicated on v3 before we claim zero-shot fails.

### 4. Sarhan, Layeghy & Portmann — *Towards a Standard Feature Set for NIDS Datasets*
Source: arXiv | 2021 | https://arxiv.org/abs/2101.11315
- **WHY:** Benchmark NIDS datasets use incompatible feature sets, which blocks cross-dataset evaluation.
- **HOW:** Re-extract datasets into a shared NetFlow feature set (NF-v2).
- **WHAT:** Shared schema; **TTL-based features are dropped for UNSW-NB15 and NF-UNSW-NB15-v2** because they correlate almost perfectly with the labels.
  - **Method weaknesses:** not assessed (read scope: abstract + search snippets only)

### 5. Luay, Layeghy, Hosseininoorbin, Sarhan, Moustafa & Portmann — *Temporal Analysis of NetFlow Datasets for NIDS* (NetFlow v3)
Source: arXiv | 2025 | https://arxiv.org/abs/2503.04404
- **WHY:** Existing NetFlow datasets lack temporal features.
- **HOW:** Re-extract UNSW-NB15, BoT-IoT, ToN-IoT and CSE-CIC-IDS2018 with nProbe; add timing and inter-arrival-time features; descriptive analysis only.
- **WHAT:** The four NF-v3 datasets we use. **No ML experiments, no transfer experiments, no TTL warning**: MIN_TTL and MAX_TTL are listed as ordinary features.
  - **Method weaknesses** (dataset paper; read: HTML via automated retrieval)
    - Only one representative day is analysed per dataset. [author-acknowledged, section: 5.3]

### 6. *Multimodal fusion based few-shot network intrusion detection system* (Scientific Reports, 2025)
Source: Nature Sci. Rep. | 2025 | https://www.nature.com/articles/s41598-025-05217-4
- **WHY:** Few-shot NIDS for scarce labels.
- **HOW:** Packet bytes rendered as image-like tensors; compares a "Transfer-Enhanced" model (source-pretrained) with a "Self-Sufficient" model (target only).
- **WHAT (from search snippets):** the Self-Sufficient model was *more stable with fewer samples*; Transfer-Enhanced gains as target size grows.
  - **Method weaknesses:** not assessed (read scope: search snippets only; full text blocked)
  - ⚠️ **Closest prior evidence for our claim**, in a different modality (packets, not NetFlow). Must be read and cited.

### 7. Ha Thanh — *TAN-IDS: transfer-aware evaluation framework for NetFlow-based IDS* (PLOS ONE, 2026) — found by search
Source: PLOS ONE 21(4): e0346801 | 2026 | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0346801
- **WHY:** In-dataset scores don't survive domain shift; evaluation should be transfer-aware.
- **HOW:** UNSW-NB15 ↔ NF-CSE-CIC-IDS2018 in a shared **8-feature** NetFlow space; RF, XGBoost, MLP, Transformer; zero-shot, mixed-domain, and fine-tuning with **5% of the target labels** (tens of thousands of flows).
- **WHAT:** RF CIC→UNSW zero-shot recall collapses to 0; fine-tuning with 5% target labels exceeds 95% in several scenarios. Concludes that domain-aware training helps.
  - **Method weaknesses** (empirical; read: HTML via automated retrieval, ~75% of text)
    - No target-only baseline visible, so "fine-tuning recovers" can't be separated from "the target labels alone suffice". [reader-inferred; checked: Sec. 4.2, 5.2–5.4; not checked: the remaining 25%]
    - Single runs, no confidence intervals. [author-acknowledged, section: 6.2]
  - ⚠️ **The paper our result most directly challenges.**

### 8. Kim — *Prototype-Based Transferability Analysis for Few-Shot Domain Adaptation in Cross-Domain Intrusion Detection* (Applied Sciences, 2026) — found by search
Source: MDPI Appl. Sci. 16(14): 6957 | 2026 | https://doi.org/10.3390/app16146957
- **WHY:** Few-shot domain adaptation behaves inconsistently across transfer directions.
- **HOW:** Windows ↔ Linux host-log intrusion detection; prototype alignment; **defines a target-only few-shot baseline as the lower bound**.
- **WHAT (snippet):** target-only is competitive in one direction; adaptation helps more in the other.
  - **Method weaknesses:** not assessed (read scope: abstract/snippets; full text blocked to automated retrieval)
  - Adjacent prior evidence (host logs, not network flows). Must cite.

---

## Cross-paper synthesis

- **Common WHY:** NIDS that score >95% in-dataset fail on new networks, and the field needs honest cross-domain evaluation.
- **Divergent HOW:** zero-shot only (Atif, Hakim zero-shot part, Roy single-dataset), source + fine-tune (TAN-IDS, Hakim), source vs target-only (Sci. Rep. on packets, Kim on host logs). **No NetFlow study compares source-based adaptation with a target-only baseline across several methods and seeds.**
- **Strongest WHAT:** Atif & Ali's zero-shot UNSW→CIC F1 0.81 after feature pruning is the strongest counter-evidence to "no transfer".
- **Unresolved gap:** On standardized NetFlow data, does source data add anything once a few target labels exist, and under which adaptation method? TAN-IDS and Hakim assume it does without testing target-only. Sci. Rep. and Kim hint it may not, in other modalities.

## Verdict for TRACE-IDS

**The gap is open but narrower than "first to notice".** The defensible novelty is:
> the first leak-free, multi-seed, multi-method, multi-dataset test on standardized NetFlow v3 showing that,
> with few target labels, source data (pooled, reweighted, importance-weighted, fine-tuned) gives no
> consistent benefit over target-only — directly testing the assumption behind TAN-IDS and Hakim et al.

**Must do before writing:**
1. **Replicate Atif & Ali's Set C feature schema on v3** (zero-shot). If UNSW→CIC transfers with Set C, then "zero-shot ≈ chance" is wrong as stated and must become "depends on the feature schema".
2. **Add a target-only baseline at TAN-IDS's budget** (5% of target labels), so their setup is tested directly.
3. **Read in full and `/ars-mark-read`:** Sci. Rep. 2025, TAN-IDS, Kim 2026, Hakim 2026, Atif 2026. Two of these are blocked to automated retrieval, so the author must open them.
4. Report base rates: balanced vs natural test sets change F1 a lot (Atif's balanced 50/50 vs our natural rates).
