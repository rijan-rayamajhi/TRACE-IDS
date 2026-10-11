# TRACE-IDS → Publication Plan (ponytail-ordered)

**Working title:** *Few Labels, Wrong Reasons: Shortcut Learning in Few-Shot Cross-Dataset Intrusion Detection*

**Ordering rule (ponytail):** leverage ÷ effort. Cheapest, highest-impact moves first. Every step has a
done-when and, where it applies, a kill rule.

**Target:** arXiv preprint in ~5 weeks → peer-reviewed venue (AISec 2027 / *Computers & Security* /
IEEE Access).

Last verified against the literature: 2026-10-10.

---

## ⚡ Status (2026-10-10) — E1 done, story revised

**E1 ran** (`src/e1_fewshot.py`, RF, 10 seeds, both directions, leak-free; `results/e1_summary.csv`).
Three methods: source+k, source+k with equal (domain, class) weighting, target-only. Two feature sets: all / −TTL.

| Finding | Evidence (mean over 10 seeds) |
|---|---|
| No zero-shot transfer | CIC→UNSW recall 0.00; UNSW→CIC recall 0.56 at FPR 0.46 (≈ chance, F1 0.24) |
| Source data adds no consistent benefit | F1 of the 3 methods within noise at every k, both directions (e.g. CIC→UNSW k=10: 0.78 / 0.83 / 0.81) |
| TTL doesn't drive few-shot recovery | −TTL curves close to all-feature curves |

**Revised claim:** *Cross-dataset few-shot NIDS on NetFlow v3 isn't transfer — once a few target labels exist,
the source dataset contributes nothing measurable, even when reweighted.* TTL becomes a supporting point.
Working title candidate: *"Is It Transfer? Source Data Adds Nothing to Few-Shot Cross-Dataset Intrusion Detection"*.

**Also fixed:** the old loader dropped 122k UNSW flows (28% of attacks) over two sparse columns; those columns
are now dropped instead (45 features, attack rate 5.4%). **All numbers in the old `report.tex` are invalid.**

### Update (2026-10-10 evening) — E2, E3, E4 done; claim survives every check

| Experiment | Result |
|---|---|
| **E2** CIC↔UNSW, RF/GBT/MLP × pooled/IW/finetune (`e2_transfer.py`) | 90 paired Wilcoxon tests: source better 0, worse 25, n.s. 65 |
| **E3** all 12 directed pairs of 4 NF-v3 datasets (`e3_analysis.py`, `results/e3_heatmap.png`) | 540 tests (p<0.05): **help 34 (6%), no diff 353 (65%), hurt 153 (28%)**; median ΔF1 −0.011; fine-tuning worst (72 hurt / 10 help). Exception: ToN→CIC RF, source +0.10–0.13 F1 at k=5–10. Zero-shot fails on every pair (all-attack or all-benign). Caveat: none survive Holm over 540 (min p = 0.002 with 10 seeds) → claim "no consistent benefit; harm ≫ help", not per-cell harm |
| **E4a** Atif & Ali Set C zero-shot, v3 (`e4_checks.py zeroshot`) | UNSW→CIC best F1 0.21 (balanced test), balanced accuracy ≤ 0.52 → their 0.81 does **not** reproduce; balanced test roughly doubles F1 vs natural rates. Caveats: v3 not v2, RF/GBT not XGBoost, feature sets reconstructed |
| **E4b** TAN-IDS 5%-label budget (`e4_checks.py budget`; 70k–83k target labels) | target-only F1 0.96–1.00 ≈ pooled ≈ fine-tune (all within ±0.006, except GBT fine-tune −0.053 UNSW→CIC). The target labels alone explain TAN-IDS's recovery |

| **E5** mechanism (`e5_mechanism.py`; attack-family sidecars via `data_loader.py families`) | (1) Domain-classifier AUC 0.997–1.000 for every pair, also benign-vs-benign and **within the same attack category** (DoS vs DoS, DDoS, scanning, brute force, backdoor), z-scored or raw → the same attack looks different on every network. (2) Source doesn't help even on categories it shares with the target (median Δrecall ≤ 0; RF k=10 median −0.02); zero-shot recall on shared categories (~0.28) is no better than on unshared (~0.31–0.43). (3) Pooled lowers FPR but costs recall (more conservative). (4) RF importance rank-correlation source vs target oracle 0.25–0.83; higher overlap loosely tracks source benefit (RF Spearman 0.59, p=0.04, n=12, exploratory — ToN→CIC has 0.83 and is the one pair where the source helps). Domain AUC can't predict benefit (ceiling, r=0.06) |

| **E5 follow-up** greedy feature ablation of the domain classifier (`e5_ablation.py`; 6 pairs × 3 seeds, 10k flows/domain, held-out AUC, drop top permutation-importance feature each step) | **Raw features:** separability is deep, not one column. AUC stays ≥ 0.999 after removing the top 5 (first removed: MIN/MAX_TTL, FLOW_DURATION, OUT_BYTES, TCP_WIN_MAX_IN) and ≥ 0.997 after 15; dropping below 0.9 takes 22–40 of 45 features (all flows; 17–39 benign-only); mean AUC with 30 removed still 0.86. **Per-domain z-scored (what E1–E5 models see):** AUC never drops below 0.95 even with 44 of 45 removed, because per-domain scaling maps the same categorical code (e.g. PROTOCOL=6) to a different value per domain (cic-unsw PROTOCOL single-feature AUC: raw 0.57 → z 1.00). **Open:** this scaling artifact could itself suppress transfer in E1–E5; not yet tested (would need E2/E3 rerun with raw or shared scaling for trees) |

| **E3-shared** scaling-confound check (`e2_transfer.py --scaling shared --out all_shared`, `e3_analysis.py --tag shared`): both domains z-scored with ONE set of stats (source sample + unlabeled target pool; = raw features for RF/GBT) | **Claim survives, stronger.** 540 tests: help 41 (8%), no diff 294 (54%), **hurt 205 (38%)** vs per-domain 34 / 353 / 153; median ΔF1 −0.025 (was −0.011); none survive Holm (same as before). RF hurt 99/180. **The ToN→CIC exception disappears** (help 9 → 0, hurt 5 → 18) → it was a per-domain-scaling quirk. New helps cluster at k=1 on BoT→CIC (14). **Zero-shot correction:** balanced accuracy (recall+TNR)/2 is NOT chance everywhere — best model 0.66–0.71 on 4 pairs already under per-domain scaling, 0.68–0.76 on 4 pairs under shared (BoT→CIC, BoT→ToN, UNSW→BoT, UNSW→ToN); ~0.5 elsewhere. But target-only with k=5–10 per class (bal. acc 0.73–0.94) matches or beats the best zero-shot on every pair. → rephrase "zero-shot ≈ chance" to "zero-shot is weak and pair-dependent; ≤10 labelled target flows/class beat it" |

**Next:** (a) ~~scaling-confound rerun~~ done (E3-shared); reword zero-shot claim in write-up; (b) author reads 5 key papers + `/ars-mark-read`; (c) write with ARS.

---

## 0. The claim (verified, scoped)

> TTL features are a **known** artifact in UNSW-NB15 (Sarhan et al.). NetFlow v3 **still ships them**
> (MIN_TTL / MAX_TTL), and few-shot cross-dataset NIDS work does not control for them. We measure how
> much few-shot recovery depends on known artifacts, and whether the source dataset helps at all
> compared with target-only training.

**Do NOT claim:** discovering the TTL artifact. It is prior work — cite it.

### Research questions
- **RQ1:** How much of few-shot cross-dataset recovery comes from known artifact features (TTL, …)?
- **RQ2:** Does the source dataset help, or do the k target labels alone do the same job?
- **RQ3:** Which attack families transfer, and why?

### Literature check (what is and isn't taken)
| Paper | Covers | Leaves open |
|---|---|---|
| Hakim et al., [arXiv 2607.00553](https://arxiv.org/abs/2607.00553) (Jul 2026) | Cross-network failure, port shortcut, limited-target recovery | No artifact ablation in recovery, **no target-only baseline** (stated by authors), IIoT not NetFlow v3 |
| Roy & Minu, [arXiv 2609.28725](https://arxiv.org/abs/2609.28725) (Sep 2026) | Shortcut learning in IoT NIDS | Single dataset, no transfer, no few-shot |
| Atif & Ali, [arXiv 2609.13511](https://arxiv.org/abs/2609.13511) (Sep 2026) | Cross-dataset transfer, staged leakage ablation | NetFlow **v2**, no few-shot |
| Sarhan et al., [arXiv 2101.11315](https://arxiv.org/pdf/2101.11315) | Drops TTL from NF-UNSW-NB15-v2 for extreme label correlation | No few-shot, no transfer study |
| Sarhan et al., [arXiv 2108.12732](https://arxiv.org/html/2108.12732) §5.1.1 | TTL = "hidden label", testbed artifact (original UNSW-NB15) | Same |
| [Sci. Reports 2025](https://www.nature.com/articles/s41598-025-05217-4) | Source+target vs target-only (packet images) | Not NetFlow |

**Honest ceiling:** workshop / IEEE Access / *Computers & Security* level, not a top-tier main track.

**Risk:** two adjacent papers appeared in Jul–Sep 2026. Speed matters.

---

## 1. Ponytail order — the plan

| # | Step | Effort | Leverage | Why this position |
|---|---|---|---|---|
| 1 | Gap check: read the 6 papers above | 4 h | 🔥🔥🔥 | Can kill the idea before any code |
| 2 | Decisive experiments E1 (target-only + no-TTL) | 1–2 d | 🔥🔥🔥 | Decides the whole story |
| 3 | Email Dr. Glisson with E1 result | 1 h | 🔥🔥🔥 | Advisor + co-author + arXiv endorser |
| 4 | Hygiene fixes | 1 d | 🔥🔥 | Without them no number is reportable |
| 5 | Scale to 4 datasets | ~1 wk | 🔥🔥 | Generality — reviewers expect it |
| 6 | Mechanism analysis | 3–4 d | 🔥 | Explains *why*; makes it a paper, not a table |
| 7 | Write + integrity check | ~1 wk | 🔥🔥 | Turns results into a paper |
| 8 | Simulated review → revise | 2–3 d | 🔥 | Catches weaknesses before real reviewers |
| 9 | Publish (arXiv + venue + outreach) | 1 d | 🔥🔥🔥 | Citable + visible |

### Step 1 — Gap check (4 h) · ARS: `/ars-3w`
- [ ] `/ars-3w` on: 2607.00553, 2609.28725, 2609.13511, 2101.11315, 2108.12732, 2503.04404 (NetFlow v3 paper)
- [ ] Specifically confirm: does anyone do few-shot recovery **with artifact ablation** on NetFlow?
- [ ] Does the v3 paper (2503.04404) warn about TTL? If yes, adjust framing.
- [ ] `/ars-mark-read <key> --scope full_text` for each paper actually read
- **Kill rule:** if the gap is taken → pivot to RQ3 (per-attack-family transfer) as the headline.

### Step 2 — Decisive experiments E1 (1–2 days) · code in `src/`
- [ ] `src/target_only.py` — train on k target samples/class only, vs source + k
- [ ] `src/ablation.py` — few-shot sweep: all features / −TTL / −top-3 SHAP / −top-5 SHAP
- [ ] 10 seeds, both directions (CIC→UNSW, UNSW→CIC), report mean ± std
- **Decision gate:**

| Result | Story |
|---|---|
| Recovery collapses without TTL | Few-shot recovery on NetFlow v3 rides a known artifact |
| Target-only ≈ source + target | Source data adds nothing — "transfer" is target training |
| Recovery survives both | A protocol that verifies real recovery |

### Step 3 — Email Dr. Glisson (1 hour)
- [ ] 5 lines + 1 figure from E1: "NetFlow v3 still ships known TTL artifacts; few-shot work ignores them."
- [ ] Ask: review? co-author? arXiv endorsement (cs.CR first-time submitters often need one)?

### Step 4 — Hygiene fixes (1 day) · required before any number is reported
- [ ] Fix target-test leakage in normalization (`fewshot.py`, `baseline.py`) — stats from pool only
- [ ] `src/common.py`: seed loop, mean ± std helper
- [ ] SHAP top-15 figure generated by code (current figure isn't — GUARDRAILS B1)
- [ ] Explain UNSW attack rate: ours 4% vs UQ page 5.4%
- [ ] Pin versions in `requirements.txt`; add `run_all.sh` (raw data → all tables/figures)
- [ ] Rewrite README / PLAN / GUARDRAILS for the new paper (remove old 0.51 claims)
- [ ] Fix citations in `report.tex`:
  - Cantone et al. → published title *"Machine learning in network intrusion detection: A cross-dataset generalization study,"* IEEE Access 12:144489–144508 (or cite arXiv 2402.10974 only)
  - Add NetFlow v3 dataset paper (arXiv 2503.04404); current `netflow` cite is v1
  - Kılıç & Şengül → add DOI 10.1109/ACCESS.2026.3703481
  - Verify DI-NIDS (arXiv 2210.08252) yourself

### Step 5 — Scale to 4 datasets (~1 week)
- [ ] Download NF-ToN-IoT-v3, NF-BoT-IoT-v3 ([UQ page](https://staff.itee.uq.edu.au/marius/NIDS_datasets/))
- [ ] `data_loader.py`: configurable dataset list; keep `Attack` column for RQ3
- [ ] 12 directed pairs × (target-only, ablation) × 10 seeds → `results/all_pairs.csv` + heatmap
- [ ] Ablate other SHAP-flagged suspects beyond TTL
- **Fallback (laptop too slow):** 6 most informative pairs or 5 seeds; state it in Limitations.

### Step 6 — Mechanism (3–4 days)
- [ ] `src/shap_over_k.py` — do artifact features take over as k grows?
- [ ] `src/per_family.py` — per-attack-family recall; family overlap across datasets
- [ ] XGBoost as second model (one line in `baseline.py`; note in GUARDRAILS why)

### Step 7 — Write + integrity (~1 week) · ARS: `academic-paper`
- [ ] `deep-research` socratic → lock RQ brief
- [ ] `/ars-lit-review "shortcut learning and few-shot cross-dataset NIDS"` → ~25 verified refs
  - Must-cite: Arp et al. "Dos and Don'ts" ([USENIX Sec '22](https://www.usenix.org/system/files/sec22-arp.pdf)), Geirhos et al. "Shortcut Learning" (2020), [NIDS datasets survey 2502.06688](https://arxiv.org/abs/2502.06688), [few-shot NIDS survey 2609.11275](https://arxiv.org/abs/2609.11275), all papers in §0
- [ ] `/ars-plan` → `/ars-outline` → draft → `/ars-abstract`
- [ ] Stage 2.5 integrity check (refs vs Crossref/OpenAlex/arXiv) must PASS
- Paper (8 pp, IEEE): Intro · Related Work · Data & Artifact Audit · Protocol · Results (RQ1–3) ·
  **Recommended Protocol** (the citable part) · Limitations · Conclusion

### Step 8 — Simulated review → revise (2–3 days) · ARS
- [ ] `/ars-reviewer` (5 reports incl. Devil's Advocate) — before Dr. Glisson sees the full draft
- [ ] `/ars-revision` → re-review → `/ars-citation-check` (final integrity must PASS)
- [ ] Fold in Dr. Glisson's feedback via `/ars-revision-coach`

### Step 9 — Publish (1 day + ongoing)
- [ ] **AI-use disclosure** in acknowledgements — required by arXiv/ACM/IEEE-style policies.
      `/ars-disclosure` doesn't cover ACM/IEEE → read the venue policy yourself.
- [ ] arXiv: cs.CR (cross-list cs.LG)
- [ ] GitHub release tag `v1.0-arxiv`, README links paper + `run_all.sh`
- [ ] Email 5–10 professors (NIDS / ML security / domain adaptation) with arXiv link + 3-line summary
- [ ] Submit: AISec 2027 (AISec 2026 @ CCS, Nov 15–19 2026, is past deadline) or *Computers & Security* / IEEE Access (rolling). **Check deadlines yourself.**
- [ ] Keep the ARS Stage 6 process record — your honest answer to "how much was AI-assisted?"

---

## 2. Cut (not worth the effort now)
- ❌ Active learning for sample selection
- ❌ Deep models beyond XGBoost
- ❌ Reliability / drift flag (already failed, AUC 0.40)
- ❌ Top-tier main-track submission

## 3. Timeline
| Week | Steps | Gate |
|---|---|---|
| 1 | 1, 2, 3, 4 | Gap confirmed · story chosen · Glisson emailed |
| 2 | 5 | All pairs run |
| 3 | 6 | Mechanism figures done |
| 4 | 7 | Draft passes integrity check |
| 5 | 8, 9 | On arXiv |

## 4. Ground rules
1. Every number comes from committed code (GUARDRAILS B1). ARS can't verify your numbers — only you can.
2. Every citation is one **you** opened and read. Never `/ars-mark-read` a paper you didn't read.
3. ARS polishes writing; it doesn't create novelty. If E1 is weak, writing won't save it.
4. Disclose AI assistance. Always.
5. A smaller honest claim beats an inflated one — reviewers and advisors catch inflation.
