# Argument Blueprint — TRACE-IDS

*Phase 3. Inputs: approved outline (`../phase2_outline/outline.md`), literature report, `facts.md`. Every number below comes from `facts.md` (printed by `extract_facts.py` from `results/`) or from `results/e5_log.txt` (printed by `e5_mechanism.py`). Main setting: per-domain scaling (author decision D1 = A). `criteria_binding_unavailable`.*

## Central Thesis

In few-shot cross-dataset intrusion detection on NetFlow v3, the source dataset does not add measurable value over training on the same few labelled target flows, and it more often hurts. The reasons:
- each network occupies a separable region of feature space, even for the same attack type;
- that separability runs across most features, not one artifact column;
- the "recovery" reported by prior work is what the target labels achieve on their own.

Evidence: 540 paired tests over 12 dataset pairs, 3 models and 3 adaptation methods with 10 seeds, plus mechanism probes and two robustness checks.

## Sub-Arguments

### SA1 (SQ1): Source data gives no consistent benefit over target-only and hurts more often than it helps.
- **Evidence:**
  - E3, per-domain scaling, 540 tests: help 34 (6%), no difference 353 (65%), hurt 153 (28%); median ΔF1 −0.011.
  - E3, shared scaling: help 41 (8%), no difference 294 (54%), hurt 205 (38%); median ΔF1 −0.025.
  - E2 (CIC↔UNSW, 90 tests): better 0, worse 25 (per-domain); 0 / 38 (shared).
  - Fine-tuning is the worst method under per-domain scaling (72 hurt / 10 help).
  - E1 (RF): source+k vs target-only within noise; e.g. CIC→UNSW k=10 F1 0.775 vs 0.811, UNSW→CIC 0.530 vs 0.555.
- **Reasoning:** if source knowledge transferred, adding it would raise F1 at small k, where target data is scarcest. Across every method, model and k, "hurt" outnumbers "help" by roughly 4–5 to 1.
- **Counter-argument 1:** "No single cell survives Holm, so nothing is shown."
  **Rebuttal (concede and limit):** we claim the *absence of a consistent benefit* and a *pattern* of harm, not per-cell harm. The minimum attainable p with 10 seeds is 0.002, so Holm over 540 is very conservative. Wording must stay at "no consistent benefit; harm outnumbers help".
- **Counter-argument 2:** "Your baselines are too weak to give the source a fair chance."
  **Rebuttal (refute):**
  - three model families and three ways of using the source, including importance weighting (a classical covariate-shift correction) and domain-balanced pooling;
  - GBT leaf size is scaled so target-only isn't handicapped;
  - the TAN-IDS budget check shows the same pattern.
- **Counter-argument 3:** "There are pairs where the source helps (ToN→CIC; BoT→CIC under shared scaling)."
  **Rebuttal (concede and limit):**
  - report the exceptions;
  - ToN→CIC's 9 helps disappear under shared scaling (0 help, 18 hurt), which makes it a scaling quirk;
  - BoT→CIC's shared-scaling helps cluster at k=1;
  - say clearly that benefit is pair-dependent and rare.

### SA2 (SQ2): Zero-shot transfer is weak and pair-dependent, and a published strong zero-shot result does not reproduce on v3.
- **Evidence:**
  - Best-model zero-shot balanced accuracy per pair, per-domain: 0.66–0.71 on BoT→CIC, ToN→BoT, UNSW→BoT, UNSW→ToN; 0.61 on BoT→ToN; ≤ 0.56 on the other 7.
  - Target-only at k=10 reaches 0.78–0.94 and beats the best zero-shot model on every pair, under both scalings.
  - Atif & Ali's Set C: F1 0.21 on a balanced test (they reported 0.81 on v2), and balanced accuracy ≤ 0.55 for every feature set (E4a).
- **Reasoning:** if the source encoded transferable attack knowledge, zero-shot would beat chance broadly. It does so on a minority of pairs and is overtaken by 10 labels per class.
- **Counter-argument:** "Atif & Ali used v2 and XGBoost; it's not a fair replication."
  **Rebuttal (acknowledge as limitation, then reframe):**
  - note v3 vs v2, RF/GBT vs XGBoost, and that the feature sets are reconstructed;
  - add that their Set C was chosen using cross-dataset F1 on the target (their §3.3), so their 0.81 is optimistically biased by design (reader-inferred; phrase as such).

### SA3 (SQ1, applied): Prior "recovery" results are what the target labels achieve alone.
- **Evidence:**
  - E4b at TAN-IDS's 5% budget: target-only F1 0.959–1.000 matches pooled and fine-tuned to within ±0.006. The exception is GBT fine-tuned UNSW→CIC at 0.914, which is worse.
  - TAN-IDS: single run, no target-only arm (author-acknowledged §6.2; target-only absence reader-inferred, sections checked: 3.5, 4.2, 4.2.1, 5.4, Tables 7–10).
  - Hakim et al.: missing condition acknowledged (§6.3).
  - Xu et al.'s own Tables 8–9 show transfer hurting at K=5 (−6.4% CICIDS2018).
  - Kim (host logs): target-only competitive.
- **Reasoning:** where the target-only arm exists (Xu, Kim, ours), the source advantage is absent or negative. Where it is missing (TAN-IDS, Hakim), recovery is credited to the source without a test.
- **Counter-argument:** "TAN-IDS used different features or data."
  **Rebuttal (concede and limit):** their Table 5 suggests the original CICFlowMeter/Argus columns (reader-inferred). We test the *assumption*, not their exact numbers, and on the standardized NetFlow release.

### SA4 (SQ3): The source can't help because each network is separable, including within the same attack category.
- **Evidence:**
  - E5-B domain-classifier AUC ≥ 0.996 for every pair, for all flows, benign-only, and within shared categories (DoS, DDoS, scanning, brute force, backdoor; minimum DoS vs DoS 0.9966 raw).
  - E5-A: zero-shot recall on categories the source *has* is no higher than on categories it *lacks* (RF 0.276 vs 0.432; GBT 0.263 vs 0.307; `e5_log.txt`).
  - Adding the source gives a slightly negative median change in recall on shared categories (k=10).
  - Pooling lowers FPR at k=10 but costs recall.
  - RF importance rank correlation, source vs target oracle: 0.25–0.83.
- **Reasoning:** domain-adaptation theory bounds target error by source error plus a divergence term (Ben-David et al.). Near-perfect separability means a large divergence, so source examples carry little information about the target's decision boundary. Negative transfer is the expected outcome.
- **Counter-argument:** "High AUC is trivial for any two datasets; it doesn't explain the transfer results."
  **Rebuttal (reframe):** the within-category result is the point. The *same attack type* is separable, so the source's attack examples do not cover the target's. The ablation (SA5) shows this is not a shallow cue.

### SA5 (SQ4): The result isn't an artifact of one feature or of preprocessing.
- **Evidence:**
  - Raw features: 23–40 of 45 features must be removed, most-relied-on first, before domain AUC < 0.9 (all flows; 17–39 benign-only). Mean AUC after removing 15 is still 0.997, and after 30 it is 0.864.
  - TTL is among the first removed. It is a documented artifact in original UNSW-NB15 (Sarhan 2108.12732 §5.1.1, "hidden label") and in NF-v2 (Sarhan 2101.11315 §4; Atif & Ali §3.3), and no prior source checks v3.
  - In E1, removing TTL lowers few-shot F1 for every method alike (CIC→UNSW k=5: 0.70→0.54 source+k, 0.70→0.50 target-only), so it doesn't change the comparison.
  - Per-domain z-scoring confound: 13/270 single features alone separate the domains with AUC ≥ 0.99 on raw values, against 231/270 after per-domain scaling. For example, CIC vs UNSW `PROTOCOL` goes from 0.565 to 1.000.
  - The main claim holds under shared scaling and strengthens: hurt rises from 28% to 38%.
- **Reasoning:** if separability were one artifact, removing it would collapse separability. If the "no benefit" result were caused by per-domain scaling, shared scaling would restore a benefit. Neither happens.
- **Counter-argument:** "Per-domain scaling is your own design flaw."
  **Rebuttal (reframe):** it is common practice (Sarhan 2101.11315 §4 uses per-dataset min-max), and identifying it as a confound is a contribution. We report both settings side by side.

## Logical Flow

1. **Intro:** cross-dataset failure → the remedy (few labels + source) → its untested assumption (no target-only arm) → RQ → contributions.
2. **Related work:** what each line of work tested and didn't → bounded gap.
3. **Protocol:** a leak-free, multi-seed, target-only-controlled design.
4. **Results 4:** SA1 (E1 → E2 → E3), then SA2 (zero-shot, E4a), then SA3 (E4b).
5. **Results 5:** SA4 (separability, families), then SA5 (ablation, scaling).
6. **Discussion:** reconcile SA3 with prior work → theory (SA4) → benchmark implications → limitations.
7. **Protocol recommendations**, which follow directly from SA1–SA5.
8. **Conclusion.**

## Argument Strength Assessment

| Sub-argument | Evidence strength | Logic | Counter-argument risk |
|---|---|---|---|
| SA1 | Strong (540 tests, both scalings, 3 models, 3 methods) | Valid; stated as a pattern | Medium (Holm) |
| SA2 | Moderate–strong | Valid | Medium (replication fidelity) |
| SA3 | Moderate (one budget check + literature reading) | Qualified | Medium |
| SA4 | Strong | Valid with theory anchor | Low–medium |
| SA5 | Strong | Valid | Low |

## Notes for Draft Writer

- **Hedging:**
  - Say "no consistent benefit" and "harm outnumbers help", never "the source always hurts".
  - Per-cell significance must not be implied (Holm).
  - Novelty claims must be search-bounded: "within the literature we screened (search of 2026-10-11)".
- **Prior work:** describe it fairly. TAN-IDS and Hakim are *not* wrong about recovery; they credit it to the source without the control. Mark reader-inferred points as such ("their Table 5 suggests…").
- **Numbers:** every number must appear in `facts.md` or `e5_log.txt`. Use per-domain as the main figure, with shared in parentheses or in the second table column.
- **Terminology:**
  - "source" and "target"; "k labelled target flows per class";
  - "per-domain scaling" vs "shared scaling";
  - "balanced accuracy" (the mean of TPR and TNR).
- **Register:** plain, active voice, no hype words. The CS/security audience expects concrete numbers early.
- **Back matter:** include an AI-use disclosure, funding none, conflict of interest none, and data and code availability (GitHub + `run_all.sh`).
