<!-- Phase 6b: evaluator review with the paper visible. Contract: academic_paper/evaluator_full/v1. Round 2.
     Pre-commitment used unchanged: phase6a_precommitment.md. It records the OLD title ("Is It Transfer? Source Data Adds Nothing to ...").
     The revised title is "Is It Transfer? A Target-Only Control Finds No Consistent Source Benefit in Few-Shot Cross-Dataset Intrusion Detection on NetFlow".
     Inputs: phase4_draft/draft.md (revised), phase5_abstract/abstract.md, phase3_argument/facts.md, phase1_literature/references.json,
     phase5_citations/citation_audit.md, ../README.md, phase6b_review.md (round 1).
     Spot checks against raw results: e1_runs_shared.csv, e2_runs_all_nottl_shared.csv, e3_significance_shared.csv, e3_zeroshot{,_shared}.csv,
     e5_distance.csv, e5_ablation_steps.csv, e5_log.txt, e6_pooled_effect.csv, e6_verdicts_by_metric.csv, e6_domain_control.csv;
     code read: src/e5_mechanism.py (report_distance), src/e6_robustness.py, src/common.py (stats, z, TTL).
     Body word count (sections 1–8, excluding HTML comments, headings and table rows): 7,797. That is above the writer's 6,300–7,700 band.
     Section 3 has 1,517 words against an outline allocation of about 1,100 (+38%). -->

## Dimension Scores

### D1: originality
**pass.** The gap is named precisely: the source's contribution has not been isolated with a target-only control under repeated, tested runs (§1 ¶3, §2.2). Related Work now separates the two nearest studies correctly. TAN-IDS is named as "the nearest flow-based recovery study" and Xu et al. as "the nearest study with a target-only control", and the paper's difference from each is stated (§2.2, last ¶). The novelty claim is still search-bounded and gives its provenance, which meets #548. The new negative-control and shared-versus-per-domain results add evidence that is not in prior NIDS work.

### D2: methodological_rigor
**warn.** The revision repairs most of the round-1 rigor problems. It adds a pooled estimate with a CI, BH as a secondary analysis, an explicit statement that Holm is infeasible, bacc verdicts, a negative control, a 12-pair no-TTL rerun, and shared scaling as the main setting. Four problems remain, and all can be fixed without new main runs:
- The pooled CI resamples the 12 directed pairs as if they were independent. Pairs share target datasets (and so share test sets and near-identical target-only arms) as well as source datasets (R2-3).
- The negative control is an i.i.d. random split, which gives AUC 0.5 by construction. It does not calibrate the cross-network AUC (R2-4; round-1 Finding 5 asked for a temporal or capture split).
- The per-domain negative control (AUC 1.00) most plausibly comes from tree splits on tiny floating-point offsets. Even so, it is the headline justification for demoting per-domain scaling (R2-5).
- The adaptation arms are still simple and untuned, and no standard domain-adaptation method was added. This is now scoped in §1 item 2 and §6.5 (round-1 Finding 8 is partly resolved).

### D3: evidence_sufficiency
**warn.** Every core claim checks out against facts.md or the raw CSVs:
- Table 2: all 36 cells and both totals.
- §4.1–4.3, §4.5, §5.3–5.4, §6.2 ESS.
- The pooled means and CIs, the BH counts, the no-TTL counts and CI.
- The abstract's 8%/38%/0.044/CI/0.996/0.50/23–40.

The round-1 block causes are resolved. The TTL result is now reported honestly and rerun across 12 pairs. The exceptions are ranked by net verdict, and the falsified hypotheses were withdrawn. A number of number/provenance mismatches remain in secondary claims:
- In §4.4, per-domain zero-shot numbers are presented without a label in a shared-scaling section (R2-1).
- The §5.1 ρ is computed from the per-domain AUC that §5.4 disowns (R2-2).
- §8's "about five times … on both F1 and balanced accuracy" is wrong for bacc (R2-6).
- The §6.1 convergence sentence overclaims (R2-8).

These are warn-level ("isolated number mismatches", "some secondary claims … over-claim"), not block. None of them changes the central result.

### D4: argument_coherence
**warn.** The "is it transfer?" question gets the same answer in the Title, Abstract, §1, §4.3, §6.1 and §8. The TTL story is now consistent across §5.3, §6.3, §7 item 6, §8, the abstract and the README. The revision did introduce several inconsistencies, however:
- §4.4 calls BoT→CIC the best zero-shot pair under shared scaling (bacc 0.76). The next paragraph says the BoT-trained RF on BoT→CIC has recall 1.000, FPR 1.000 and bacc 0.5, which is the per-domain value; the shared value is 0.918/0.477/0.720 (R2-1).
- §3.3 still says "we repeat the TAN-IDS setting", while §4.5 says "emulate" (R2-7).
- §5.3 calls the per-domain sensitivity run "an earlier version" of the experiment (R2-14).
- Fig. 2 and Fig. 4 do not state their scaling (R2-12).
- The README still leads its zero-shot finding with per-domain numbers and points to the per-domain budget file (R2-15).

### D5: writing_quality
**warn.** The register is clear and appropriate. Table 2 now has method, model and k panels, and every figure and table is referenced. The text is longer, though:
- The body is 7,797 words, which is above the 7,700 ceiling of the band the writer committed to and 11% over the 7,000 target.
- §3 is 38% over its allocation.
- Several results are stated three times: §4.3/§6.3/§7, §5.1/§6.2 (Ben-David and ESS), and §5.3/§6.3/§8 (TTL).
- The citation style is still author-year while IEEE is the target.

None of this reaches block.

## Failure Condition Checks

### F1
**Not fired.** No mandatory dimension (D2, D3) scores `block`.

### F2
**Fired.** The mandatory dimensions D2 and D3 score `warn`. Action: `evaluator_decision=request_revision`.

### F3
**Not fired.** No high-priority dimension (D1, D4) scores `block`.

### F6
**Not fired.** The normal-priority dimension D5 scores `warn`, not `block`.

### F4
**Not fired.** F4 requires that no mandatory dimension scores `block` or `warn`, but D2 and D3 are `warn`.

### F5
**Not fired.** Round 2 shows no mandatory-dimension `block`.

### F0
**Not fired.** Not every mandatory dimension passes.

## Round-1 Findings: Resolution

| # | Verdict | Evidence in revised draft |
|---|---|---|
| 1 | resolved | §5.3 ¶2 reports the per-domain −TTL gains (+0.167, p = 0.037; +0.147, p = 0.014), the shared reversal (−0.263, p = 0.002) and a 12-pair no-TTL rerun (42/228, −0.056 [−0.080, −0.030]). All match facts.md. §8 now reads "without it, the source does slightly worse on average". |
| 2 | resolved | The title now reads "…Finds No Consistent Source Benefit…". §4.3 ¶5 states that "no difference … not that the two arms are equivalent". No TOST was added; the wording no longer needs one. |
| 3 | partly resolved | §3.4 ¶3 states plainly that per-cell FWER is unattainable, adds BH (§4.3: 179 and 129) and a pair-bootstrap pooled CI, and §7 item 2 gives "at least 15" seeds (this is correct: 2/2¹⁵ < 9.3×10⁻⁵). The pooled CI still treats pairs as independent, although pairs share targets and sources (R2-3). |
| 4 | resolved | §4.3 ¶5 ranks pairs by net verdict (UNSW→BoT 9/3 first). §5.2 ¶3 and §6.3 state that UNSW→BoT has the lowest overlap and that helps are spread across k, and the two hypotheses are withdrawn. |
| 5 | partly resolved | The language is now "consistent with" (§5.1 ¶2, §8), λ is acknowledged (§5.1 ¶2), and a negative control has been added. The control is an i.i.d. random split (0.5 by construction), not the temporal or capture split that was asked for (R2-4). |
| 6 | resolved | §5.4 ¶2 now reads "Per-domain scaling has a second, opposite effect … a mild form of domain alignment", with the ESS 34% vs 0.8% and the hurt counts 153 vs 205. A new issue about the per-domain control is raised in R2-5. |
| 7 | resolved | §3.4 ¶2 now reads "Demšar recommends this test for comparing two classifiers over multiple data sets …; we apply it to paired seeds within one pair … best read as descriptive." |
| 8 | partly resolved | §3.3 ¶2 justifies the arms as "deliberately simple" and untuned because there are no target validation labels. The MLP and GBT fine-tune details are given, and the scope is stated in §1 item 2 and §6.5. No standard domain-adaptation method was added, and the title is not scoped. |
| 9 | resolved | §3.4 ¶1 and §4.3 ¶2 repeat the verdicts on bacc, including the BoT-target cells (32/15 per-domain, 13/36 shared), and all of these match e6_verdicts_by_metric.csv. |
| 10 | partly resolved | §4.5 now says "emulate" and restores the concession, but §3.3 ¶4 still says "we repeat the TAN-IDS setting" (R2-7). |
| 11 | resolved | The "same or higher" claim has been removed from §5.1. |
| 12 | resolved | §4.3 ¶4 replaces "most damage at small budgets" with the by-k means and hurt counts. A residual wording issue is raised in R2-9. |
| 13 | resolved | §5.2 ¶2 now reads "Pooling makes the model more conservative … Fine-tuning does the opposite and raises the FPR, to 0.183 … 0.226". "Threshold" has been dropped. |
| 14 | partly resolved | §6.1 now uses "the median change … is negative", writes "better in one direction and clearly worse in the other" for Kim, and notes Xu's K = 10/15 gains. Xu's Table 11 versus Tables 8–9 inconsistency is still not mentioned, and the last sentence of §6.1 overclaims convergence (R2-8). |
| 15 | resolved | §4.4 ¶3 reports set A (F1 0.54 at bacc 0.54) and "at most 0.55" for A–C. The Cv2 variant is omitted (R2-10, new). |
| 16 | resolved | §3.5 now reads "up to 20,000 flows per side … web attacks are omitted". |
| 17 | partly resolved | (a) is resolved: §5.4 now reads "In our experience…" with no citation. (b) is resolved: Alsaedi is now cited as the "telemetry portion". (c) is resolved: Roy & Minu is cited as 92.6%→99.28%. (d) is resolved: "documents common data limitations". (e) is resolved: "partial, architecture-dependent". (f) is resolved. (g) is not resolved: citation_audit.md still lists 33 abstract-only sources. New attribution issues are raised in R2-13. |
| 18 | resolved | §2.2 last ¶: "TAN-IDS is the nearest flow-based recovery study … Xu et al. is the nearest study with a target-only control". |
| 19 | partly resolved | The README now says shared is the main setting, and the TTL ordering now reads "among the first five in 24 of 36 runs". The 28% figure is still not printed by extract_facts.py, and the README's zero-shot and budget lines still lead with per-domain numbers (R2-15). |
| 20 | partly resolved | Table 2 is split into method/model/k panels and the abstract says "(uncorrected)". The citation style is still author-year, and §3 has grown from 1,322 to 1,517 words (R2-16). |

**Tally:** 12 resolved, 8 partly resolved, 0 not resolved.

## Review Body

**Summary judgement.** The revision is substantial and honest. Every round-1 Critical/Major issue that bore on the central claim has been fixed:
- the TTL misreport;
- the selective exceptions;
- the absence of an aggregate estimate;
- F1 on the BoT target;
- the Demšar misattribution.

The new shared-scaling main setting is applied consistently in Table 2, §4.1–4.3, §4.5 and §5.3. What remains is (i) leftover per-domain numbers in places the revision did not reach (§4.4 ¶2, §5.1's ρ, §7 item 3), (ii) two inferential points a *Computers & Security* statistician would raise (pair dependence, and an i.i.d. negative control), and (iii) a weakly argued rationale for the change of main setting. A hostile reviewer would hit R2-1, R2-3, R2-4 and R2-5 first.

### Numbered findings (round 2)

**R2-1. Major. §4.4 ¶2, "for BoT→CIC its recall is 1.000 at an FPR of 1.000 … In both cases balanced accuracy is 0.5 … UNSW→BoT with balanced accuracy 0.710 at an FPR of 0.156."**
- *Problem:* This paragraph prints per-domain zero-shot numbers in a section whose first paragraph uses shared scaling. Nothing in the paragraph says it is per-domain, and it contradicts that first paragraph.
- *Evidence (facts.md, "E3 shared" vs "E3 per-domain" zero-shot tables):*

  | Claim | Per-domain | Shared |
  |---|---|---|
  | RF BoT→CIC (recall / FPR / bacc) | 1.000 / 1.000 / 0.500 | 0.918 / 0.477 / 0.720 |
  | CIC-trained RF "recall and FPR at or near zero … bacc 0.5" | holds (0/0/0.5) | CIC→ToN 0.071 / 0.134 / 0.469; CIC→BoT 0.063 / 0.068 / 0.498 |
  | MLP UNSW→BoT (bacc / FPR) | 0.710 / 0.156 | 0.689 / 0.241 |

  - Under shared scaling, the best models on the four good pairs are GBT, MLP, MLP and RF, so "mostly from the MLP" does not hold.
  - ¶1 names BoT→CIC as the best shared pair (0.76), while ¶2 says the BoT-trained RF on that pair is at chance.
  - §7 item 3 ("recall 1.0 at an FPR of 1.0") is also per-domain only.
- *Suggested fix:* Rewrite ¶2 from the shared table and label any per-domain example as such. For example, under shared scaling the CIC→UNSW RF reaches recall 0.001 at FPR 0.001, and BoT→UNSW RF reaches recall 0.743 at FPR 0.792, bacc 0.476. Scope §7 item 3.

**R2-2. Major. §5.1 ¶2, "the rank correlation between domain AUC and the mean source benefit is 0.06 (p = 0.85)".**
- *Problem:* The number comes from the measurement that §5.4 rejects, under the setting that §3.2 demotes. It is also not printed in facts.md.
- *Evidence:*
  - `src/e5_mechanism.py` `report_distance` correlates the **z-scored (per-domain)** "all"-subset AUC with the **per-domain** `e3_significance.csv` benefit (output in `e5_log.txt`: r = 0.060, p = 0.853).
  - §5.4 says separability after per-domain scaling "says nothing about the traffic, and we report separability on raw features only".
  - Recomputed: raw AUC vs shared benefit gives ρ = 0.03 (p = 0.93), and raw AUC vs per-domain benefit gives ρ = −0.44 (p = 0.15).
- *Suggested fix:* Report raw-AUC vs shared-benefit (ρ = 0.03, p = 0.93) and have extract_facts.py print it. The conclusion does not change.

**R2-3. Major. §3.4 ¶3 / §4.3, "treat the 12 pairs as the independent units … 95% CI from 10,000 bootstrap resamples of pairs".**
- *Problem:* The 12 directed pairs are not independent:
  - Each target dataset appears in 3 pairs with the same test-set construction and a near-identical target-only arm. facts.md shows target-only bacc of 0.607/0.607/0.610 for the three →CIC pairs under shared scaling. For trees, shared scaling equals raw features, so those arms are identical.
  - Each source dataset also appears in 3 pairs.
  - A percentile bootstrap over 12 correlated units understates the uncertainty. §3.4 cites within-pair sharing as the reason for pooling, but ignores the same sharing across pairs.
- *Evidence (computed from `e6_verdicts_by_metric.csv`):*
  - The direction is robust: under shared scaling every target-dataset mean is negative (BoT −0.055, CIC −0.025, ToN −0.022, UNSW −0.074), and so is every source-dataset mean.
  - The strength is weaker than the CI suggests. A Wilcoxon test across the 12 pair means gives p = 0.016 (F1, shared) but p = 0.077 (bacc, shared), and a sign test gives 9/12 negative (p = 0.15).
  - The shared bacc CI upper bound (−0.002) is fragile. Yet §4.3 ¶5 states that "the source lowers F1 and balanced accuracy" as "the claim the data support".
- *Suggested fix:* Acknowledge the dependence. Add per-target and per-source means (4/4 negative) as the robustness statement, or fit a crossed random-effects model (source + target + pair). Soften the shared-bacc claim to "direction consistent, CI barely excludes zero". A two-way (source, target) cluster bootstrap would be the cleanest single fix.

**R2-4. Major. §3.5 / §5.1 ¶1 / §1 item 4 / Abstract, "two random halves of one dataset give 0.50".**
- *Problem:* `src/e6_robustness.py` `run_control` draws one stratified sample of 200,000 flows and splits it at random. Two i.i.d. halves give AUC 0.5 for *any* non-leaking classifier. The control therefore only shows that the domain classifier does not overfit or leak. It does not show that AUC ≈ 1 is specific to *different networks*, as opposed to different capture sessions, days or attack campaigns of the same network. That was the point of round-1 Finding 5 ("two capture days … or two halves of one testbed"). The abstract and §1 present the control as though it calibrates the cross-network AUC.
- *Evidence:* `e6_domain_control.csv` (raw 0.491–0.507; 3 seeds; 100,000 per half). The seeds and sizes are not stated in the draft. Luay et al. (references.json) report that most attack classes were run on separate days, so a temporal split is both feasible and the relevant comparison.
- *Suggested fix:* Add a temporal control: split each dataset by flow-start timestamp (first vs second half, or by capture day). The timestamp is dropped as a feature but is still available for splitting. Compute the AUC on benign flows. If the result is close to 0.5, the claim becomes strong. If it is high, the "own region of feature space" interpretation must be weakened. In the meantime, describe the current control as a "sanity check of the classifier", not as a calibration, and state its seeds and n.

**R2-5. Major. §3.2 ¶2, §5.4 ¶1, §1 item 4, §7 item 4, Abstract, "per-domain scaling makes even two halves of one dataset perfectly separable".**
- *Problem:* Two i.i.d. halves of 100,000 flows have almost identical means and SDs. AUC 1.00 after per-domain z-scoring can therefore only arise because discrete or near-constant columns (PROTOCOL, flags, codes) land on slightly different floating-point values in each half, and a histogram GBT can split exactly on those values. This is an artifact of the *separability measurement* with tree classifiers. By itself it does not show that per-domain-scaled *transfer models* are invalid: the MLP is insensitive to such offsets, and the labels are within-domain. The revision uses this result as its headline reason for demoting per-domain scaling, which a reviewer may read either as a bug or as a non sequitur. The real cross-dataset argument is the one in §5.4 ¶1 (the same raw code maps to *different* values across datasets, 13 → 231 of 270 single features), together with the ToN→CIC flip. There is also an unexplained tension. Under per-domain scaling, the logistic-regression domain classifier inside IW finds the domains *less* separable (ESS median 34% vs 0.8%), while the GBT domain classifier finds them *perfectly* separable.
- *Evidence:* `e6_domain_control.csv` zscore 0.99998–1.0 on random halves. `src/common.py` `stats` replaces zero SD with 1. Facts: IW ESS figures.
- *Suggested fix:*
  - State the mechanism (exact-value splits on discrete columns), and say that it invalidates per-domain *separability measurement* in particular.
  - Ground the choice of main setting on cross-dataset code misalignment and the ToN→CIC flip.
  - Reconcile the IW-ESS observation with the AUC result in one sentence (a linear versus a tree domain classifier).
  - Soften the abstract and §7 item 4 accordingly.

**R2-6. Minor. §8, "significant harm is about five times as common as significant help, under both shared and per-domain scaling and on both F1 and balanced accuracy".**
- *Problem:* The ratio holds for F1 only.
- *Evidence:* F1: 205/41 = 5.0 (shared) and 153/34 = 4.5 (per-domain). Bacc: 214/35 = 6.1 (shared) and 147/49 = 3.0 (per-domain) (facts.md, E6 verdicts).
- *Suggested fix:* "about five times as common on F1 (three to six times on balanced accuracy)".

**R2-7. Minor. §3.3 ¶4, "Second, we repeat the TAN-IDS setting".**
- *Problem:* This is a leftover from the round-1 wording and contradicts §4.5 ("emulate … not their exact numbers").
- *Suggested fix:* "Second, we emulate the TAN-IDS label budget …".

**R2-8. Minor. §6.1, "Different data, models and adaptation methods point the same way" and §4.5, "at small budgets … it does not help".**
- *Problem:* Overclaim.
  - Kim's evidence is split by direction and is not significant.
  - Xu's transfer helps at K = 10/15 on CICIDS2017, and Xu's headline Table 11 conflicts with Tables 8–9 (references.json `xu2025multimodal`). This was asked for in round-1 Finding 14 and is still absent.
  - "Does not help" ignores the 41 significant helps.
- *Suggested fix:* "Xu et al. point the same way at small budgets; Kim's evidence is mixed". Note the Xu inconsistency. In §4.5, write "does not help on average".

**R2-9. Minor. §4.3 ¶4, "the hurt count rises with k and peaks at k = 50".**
- *Problem:*
  - The shared hurt counts (28, 37, 35, 56, 49) are not monotone.
  - The paragraph compares shared *means* by k with per-domain *medians* by k. The per-domain mean by k (−0.052 … −0.018) is available in e6_pooled_effect.csv.
- *Suggested fix:* "Hurt counts do not fall with k and peak at k = 50". Use the same statistic (mean) for both scalings.

**R2-10. Minor. §4.4 ¶3, "the best F1 is 0.21 on a balanced test set and 0.13 on a natural-rate test set".**
- *Problem:* The Cv2 variant described in §3.3 ("drops the v3-only inter-arrival features to match their v2 schema") is arguably the closer reconstruction. It reaches F1 0.250 (balanced) UNSW→CIC.
- *Evidence:* facts.md E4a (Cv2 balanced 0.250, bacc 0.506).
- *Suggested fix:* "0.21 (set C) and 0.25 (set C restricted to v2 features), at balanced accuracy ≤ 0.53".

**R2-11. Minor. §3.5 / §5.1, within-category domain AUC.**
- *Problem:* "Up to 20,000 flows per side" hides very small samples. The lowest AUC reported (DoS 0.9966) is computed on as few as about 226 flows per side, and backdoor on 188–213. Five-fold GBT on 45 features with about 200 flows per side is a small-sample estimate.
- *Evidence:* `e5_distance.csv` `n` column: backdoor 188–213; DoS 226–1,574; scanning 698–4,995; web 6–16.
- *Suggested fix:* Report n per category (a one-line range is enough) and the across-seed SD.

**R2-12. Minor. §5.2 / §6.5 scope of the per-domain caveat; figure captions.**
- *Problem:* The caveat is too broad in one place and too narrow in another:
  - *Too broad:* the RF importance correlation is invariant to per-domain affine scaling, because each RF is trained on one domain only. That analysis therefore needs no per-domain caveat, and saying so strengthens the UNSW→BoT counter-evidence.
  - *Too narrow:* zero-shot per-category recall (0.28 vs 0.43) *is* scaling-dependent, as R2-1 shows.
  - Fig. 2 (`results/e2_transfer.png`, the per-domain E2 run) and Fig. 4 do not state their scaling, while §4.2 leads with shared counts.
- *Suggested fix:* Split the §6.5 caveat into the two cases. Add the scaling to the Fig. 2 and Fig. 4 captions, or regenerate Fig. 2 from shared runs.

**R2-13. Minor. Citation attributions and reading claims.**
- (a) §1: Roszeitis et al. "describes few-shot learning as a promising route". The summary in references.json reports only review findings about practice.
- (b) §6.2: "it assumes the source covers the target's input distribution (Shimodaira, 2000)". The summary is marked "from general knowledge", and the support assumption is not in it.
- (c) §5.1: the Ben-David λ term is beyond the abstract-only summary.
- (d) §2.2 "in the sections and tables we checked (3.5, 4.2, 5.4, Tables 7–10)" and "on our reading of their Table 7". references.json records that this full-text reading was done by an AI agent. The first-person phrasing attributes the check to the paper's author, which is a disclosure-accuracy risk.
- (e) 33 of 41 sources remain abstract-only (citation_audit.md).
- *Suggested fix:*
  - Re-anchor (a)–(c) to verified passages or soften them.
  - For (d), either have the author verify those sections and record it with `/ars-mark-read`, or rephrase ("the sections and tables examined").
  - Extend the AI-use statement if AI-performed source reading stays the basis.

**R2-14. Minor. §5.3 ¶2, "In an earlier version of the CIC↔UNSW experiment of Section 4.1 that used per-domain scaling" and the TTL feature list.**
- *Problem:*
  - "Earlier version" makes the sensitivity analysis sound like a discarded run.
  - Only MIN_TTL/MAX_TTL are removed (`src/common.py` `TTL`). DNS_TTL_ANSWER is kept without comment, although Luay et al. list it alongside them.
- *Suggested fix:* "Under per-domain scaling (our sensitivity setting) …". State why DNS_TTL_ANSWER is kept.

**R2-15. Minor. README.md.**
- *Problem:*
  - Finding 2 leads with the per-domain zero-shot range ("0.61–0.71 on 5 of 12 pairs"), puts the shared range in parentheses, and cites `e4_budget_summary.csv` (per-domain), while the paper uses shared.
  - Finding 3 has a run-on sentence (", A per-domain RF check").
  - The 28% figure in §3.1 is still not printed by extract_facts.py.
  - "Per-domain z-scoring is a confound" differs from the paper's narrower framing.
- *Suggested fix:* Put shared numbers first, point to `e4_budget_summary_shared.csv`, fix the sentence, have extract_facts.py print the 28%, and align the framing with §5.4.

**R2-16. Minor. Length and style.**
- *Problem:*
  - The body is 7,797 words, above the 6,300–7,700 band and 11% over target.
  - §3 has 1,517 words against about 1,100.
  - Several results are stated three times.
  - The citation style is still author-year.
- *Suggested fix:* See the cut plan below, and convert to IEEE.

### Check (a): numbers verified

Every number listed below matches facts.md or a raw CSV, or is a correct rounding:
- §1 items 2–4.
- §3.1/Table 1.
- §3.4 (p_min = 0.002; 0.05/540 ≈ 9×10⁻⁵; 15 seeds needed for Holm).
- §4.1. The k = 1 recall 0.666 vs 0.022 and FPR 0.400 vs 0.001 are verified from `e1_runs_shared.csv` (0.666 / 0.0223; 0.3996 / 0.0011), and 0 helps / 10 hurts was recounted from facts.md.
- §4.2 (0/52/38; 0/65/25).
- §4.3 and Table 2: every cell, totals and percentages, median −0.025, pooled −0.044 [−0.0655, −0.0224], 3/12 positive, per-domain −0.0385 [−0.0645, −0.0169], bacc counts and CIs, BoT-target 32/15 and 13/36, BH 179 (29/150) and 129 (19/110), pair ranking and BoT→CIC by-k.
- §4.4 ¶1 (0.68–0.76; ≤ 0.58; 0.66–0.71; 0.78–0.94) and ¶3 (except R2-10).
- §4.5 (70,404 / 82,789; 0.961–1.000; ±0.006 except GBT UNSW→CIC 0.942 and RF CIC→UNSW 0.981, checked cell by cell).
- §5.1 AUCs (0.9993 / 0.9992 / 0.9966; control 0.50).
- §5.2 (0.28 / 0.43, 0.26 / 0.31, medians, FPRs, overlaps 0.25–0.83). These are all per-domain, as the text states.
- §5.3 (24/36; 0.999; 0.997; 23–40; 17–39; 0.86; ±TTL E1 deltas and p; no-TTL 42/228, −0.056 [−0.080, −0.030], bacc 35/254, CIC→UNSW 0/13, UNSW→BoT 15/0).
- §5.4 (13 / 231 of 270; PROTOCOL 0.565 / 1.000; per-domain ablation floor 0.956 ≥ 0.95 at 44 removed, from `e5_ablation_steps.csv`; control 1.00).
- §6.2 ESS (0.1–3.8%, 0.8%; 5–68%, 34%).
- Abstract: all numbers. The abstract has 239 words.

The mismatches are in R2-1, R2-2, R2-6 and R2-10. One figure is still unverified against printed facts: §3.1 "28%".

### Word count (sections 1–8; excluding HTML comments, headings and table rows)

| Section | Words | Subsections |
|---|---|---|
| 1 Introduction | 859 | — |
| 2 Related Work | 1,301 | 2.1: 318 · 2.2: 464 · 2.3: 319 · 2.4: 200 |
| 3 Data and Protocol | 1,517 | 3.1: 297 · 3.2: 234 · 3.3: 466 · 3.4: 294 · 3.5: 226 |
| 4 Results: Does the Source Help? | 1,369 | 4.1: 170 · 4.2: 91 · 4.3: 603 · 4.4: 338 · 4.5: 167 |
| 5 Results: Why Not? | 1,281 | 5.1: 253 · 5.2: 289 · 5.3: 416 · 5.4: 323 |
| 6 Discussion | 916 | 6.1: 196 · 6.2: 190 · 6.3: 174 · 6.4: 142 · 6.5: 214 |
| 7 Recommended Protocol | 332 | — |
| 8 Conclusion | 222 | — |
| **Total** | **7,797** | (figure captions 157, back matter 120, abstract 239, all excluded) |

**Where to cut about 900 words with the least loss:**

| Location | Cut | What to cut |
|---|---|---|
| §3.3 | ~130 | Compress the four arm bullets. Move the GBT leaf-size and MLP optimiser details to a one-line parameter list or the code. Shorten the Atif/TAN-IDS "two further checks" paragraph to one sentence that points to §4.4/§4.5, which repeat the details. |
| §2.2 | ~120 | The Xu/Kim details are repeated almost verbatim in §6.1. Keep them in one place (§2.2) and reduce §6.1 to one sentence. Shorten the provenance hedge, but keep its protected text. |
| §2.1 + §2.3 | ~120 | Condense the four-study list in §2.1 ¶1 to two sentences. Merge the Engelen/Lanvin/Flood/Goldschmidt sentence in §2.3 with §6.4, which cites the same sources. |
| §4.3 | ~110 | ¶4 (by-k) restates the new "By k" panel of Table 2. Keep one sentence. ¶5 and §6.3 both rank exceptions; keep the ranking here only. |
| §6.2 + §6.3 | ~150 | §6.2 repeats §5.1's Ben-David argument and §5.4's ESS figures. §6.3 repeats §4.3 ¶5 and §5.3. Merge them into one ~200-word "When might a source help, and why mostly not" subsection. |
| §5.3 ¶2 | ~70 | Drop the per-domain/shared E1 p-values that §7 item 6 and §8 restate. Keep the 12-pair result. |
| §1 | ~100 | ¶4 ("The question matters …") repeats §2.3. Shorten contributions 2 and 4, which repeat the abstract's numbers. |
| §7 | ~70 | Cut each item's evidence clause to a cross-reference. |
| §4.4 ¶2 | ~40 | This paragraph must be rewritten anyway (R2-1); make it shorter. |
| **Total** | **~910** | This would bring the body to about 6,890 words, inside the band. |

## Evaluator Decision

evaluator_decision=request_revision

Revision priorities, in order:
1. R2-1, R2-2 and R2-6: correct the leftover per-domain numbers and the §8 ratio. These are text-only fixes.
2. R2-3: acknowledge the dependence between pairs, and add per-target/per-source means or a crossed model. This is reanalysis of existing CSVs only.
3. R2-4 and R2-5: add a temporal (capture-time) negative control, and re-ground the per-domain demotion on the cross-dataset code misalignment. The control needs one short added run; the rest is text.
4. R2-7 to R2-16: precision edits, the README, and the ~900-word cut.

criteria_binding_unavailable
