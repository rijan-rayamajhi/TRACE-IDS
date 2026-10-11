<!-- Phase 6b: evaluator review with the paper visible. Contract: academic_paper/evaluator_full/v1. Round 1.
     Inputs: phase6a_precommitment.md (own <phase6a_output>), phase4_draft/phase4a_precommitment.md (<phase4a_output>), phase4_draft/draft.md,
     phase5_abstract/abstract.md, phase2_outline/outline.md, phase3_argument/argument_blueprint.md, phase3_argument/facts.md,
     ../results/e5_log.txt, phase1_literature/references.json, phase5_citations/citation_audit.md, ../README.md.
     Spot checks against raw results: ../results/e3_significance{,_shared}.csv, e1_summary.csv, e1_runs.csv, e4_budget_runs.csv, e5_ablation_summary.csv.
     Writer 4a check: the draft keeps the search-bounded novelty form it committed to (Section 2.2, with a protected hedge). The body has 6,948 words (sections 1–8, excluding comments and captions), inside the 6,300–7,700 band.
     Section 3 has 1,322 words against an outline allocation of about 1,100 (+20%), which is outside the writer's ±15% per-section band. -->

## Dimension Scores

### D1: originality
**pass.** The Introduction names a specific gap: prior few-shot "recovery" results (TAN-IDS, Hakim et al.) never train on the same target labels alone, so the source's contribution is not isolated (§1, ¶3). The contributions list turns this into a testable protocol (§1, items 1–5). Related Work engages the closest studies on their merits rather than listing them. It checks which tables of TAN-IDS do and do not contain a target-only arm, gives Xu et al.'s own per-K deltas, and notes Kim's five-seed power limit (§2.2). The novelty claim is search-bounded, gives its provenance (sources, years, verification route and date) and names TAN-IDS as the nearest prior work, which satisfies the #548 exception. One small issue: Xu et al. already includes a target-only control and arguably sits closer than TAN-IDS (Finding 18). It does not undermine the contribution, which is differentiated by its 12 pairs, repeated seeds and NetFlow v3 scope.

### D2: methodological_rigor
**warn.** The method is fundamentally sound but insufficiently detailed in places. It has a matched target-only control on identical target flows, nested k draws, normalization from training-visible data only, and 10 seeds. The code and a rebuild script are released. However, some choices lack justification, and limitations are mentioned but not engaged with:
- Inference: the 540 paired verdicts are uncorrected per-cell tests. They are not independent: the target-only arm is shared by every pair with the same target, and the same models and methods recur. Holm over 540 tests cannot reject anything by design, because the minimum p is 0.002 against a threshold of about 9×10⁻⁵. No aggregate test is reported, such as a hierarchical or clustered estimate of ΔF1 or a sign test across cells. No equivalence test is reported either (Findings 3, 7).
- The "fine-tuning" variants are ad hoc (for the RF, 100 trees grown on target flows are appended to the 100 source trees) and the hyper-parameters are untuned (Finding 8).
- F1 is computed on a target that is 97.5% attacks (Finding 9).
- The domain classifier has no within-dataset negative control (Finding 5).
- §4.5 is described as "repeating" TAN-IDS although the feature interface and splits differ (Finding 10).

None of these is a mismatch between method and question, and all can be fixed by reanalysis or added runs. That is why this is a warn and not a block.

### D3: evidence_sufficiency
**block.** The core count claims match the logs exactly (Table 2, §4.3, §4.4, §5.1–5.4; see check (a)). Even so, several inferences exceed what the data supports:
- **Contradicted TTL claim.** §5.3 states that removing TTL "lowers few-shot F1 for every method" and that "the source-versus-target comparison is unchanged". The paper's own E1 runs contradict both statements. In UNSW→CIC, removing TTL *raises* F1 for every method at k = 1–10. In CIC→UNSW, with TTL removed, the weighted source beats target-only by +0.167 F1 at k = 5 and +0.147 at k = 10. These differences are significant at p = 0.037 and p = 0.014 under the paper's own exact paired Wilcoxon rule. On these feature sets, therefore, the source *helps*, which the text omits (Finding 1).
- **Selective exceptions.** The exceptions discussion cherry-picks favourable evidence. Under shared scaling it omits UNSW→BoT, which has 9 helps and 3 hurts and is the most net-favourable pair. That pair has the *lowest* feature-importance overlap (0.253), which contradicts the feature-overlap hypothesis in §5.2/§6.3. Aggregate helps are not concentrated at small k (per-domain: 9, 3, 4, 8, 10 helps for k = 1, 5, 10, 50, 100), which contradicts the "extremely scarce labels" hypothesis (Finding 4).
- **Title.** The title claims "Source Data Adds Nothing", but the evidence is 34–41 significant helps (more than the roughly 11–13 per direction expected by chance) and no equivalence test (Finding 2).

There are also secondary misattributions: Demšar (Finding 7), and Sarhan 2022 and Alsaedi (Finding 17).

### D4: argument_coherence
**warn.** The overall logic holds. The question "is it transfer?" is posed in §1 and answered the same way in the Abstract, §4–§6 and §8, and every section ends with a transition. There are, however, minor inconsistencies between section claims or between abstract and body:
- The title says "adds nothing" while the body says "no consistent benefit".
- §5.4 calls per-domain scaling a confound that "inflates separability", yet removing it (shared scaling) makes transfer *worse*. This is in tension with the separability→no-transfer mechanism, and the text does not reconcile it (Finding 6).
- §2.2 names TAN-IDS as the nearest prior work, although Xu et al. already has the target-only arm (Finding 18).
- The README calls shared scaling the "main setting", while the paper and blueprint use per-domain (Finding 19).
- §4.3 says the source does most damage "at exactly the small budgets", but its own k = 1 median and the shared-scaling hurt counts do not support this (Finding 12).

### D5: writing_quality
**pass.** The register is a consistent academic register, plain and precise, with no promotional language. Grammar errors are rare. All figures (Fig. 1–5) and tables (Table 1–2) are referenced in the text, and every acronym is expanded at first use. The body has 6,948 words, close to the 7,000 target. There are minor issues, none at the warn level for a pre-formatting draft: the citation style is author-year in the draft while the outline targets IEEE (`phase5_citations/ieee_references.md` exists, so this is pending conversion); Table 2 stacks method and model rows without a separator, so the bold "All" row can be misread as a sum of all six rows; and §3 is about 20% over its allocation (Finding 20).

## Failure Condition Checks

### F1
**Fired.** Mandatory dimension D3 (evidence_sufficiency) scores `block`. Action: `evaluator_decision=request_revision`.

### F2
**Fired.** Mandatory dimension D2 (methodological_rigor) scores `warn`. Action: `evaluator_decision=request_revision`.

### F3
**Not fired.** No high-priority dimension (D1, D4) scores `block`. D4 is `warn`, and D1 is `pass`.

### F6
**Not fired.** The normal-priority dimension D5 scores `pass`.

### F4
**Not fired.** D4, a high-priority dimension, triggers `warn`, but F4 requires that no mandatory dimension scores `block` or `warn`. D3 is `block` and D2 is `warn`.

### F5
**Not fired.** This is round 1, and there has been no prior writer revise_in_phase_4b attempt.

### F0
**Not fired.** Not every mandatory dimension passes, and D3 scores `block`.

## Review Body

**Summary judgement.** The study is worth publishing. Its central empirical result is correct as counted: under a leak-free protocol with a target-only control, source-based adaptation shows no consistent F1 benefit, and uncorrected significant harm outnumbers help by 4.5–5×. Every count in Table 2 and §4.3 matches `facts.md`, and the Table 2 rows and columns sum correctly (each row sums to 180; method rows and model rows each sum to 34/353/153 and 41/294/205). The problems are in what the text says beyond those counts:
- one result section misreports the paper's own ablation in the direction of the thesis;
- the exceptions are discussed selectively;
- the statistical framing does not support the strength of the title;
- the mechanism lacks a negative control.

A hostile reviewer at *Computers & Security* would find Findings 1–5 within the first reading.

### Numbered findings

**1. Critical. §5.3, "Because both drop together, the source-versus-target comparison is unchanged."**
- *Problem:* Both the claim and its premise are contradicted by the paper's own E1 data, and the contradiction favours transfer.
- *Evidence (facts.md E1; recomputed from `results/e1_runs.csv`):*
  - Premise ("removing MIN_TTL and MAX_TTL lowers few-shot F1 for every method"): in UNSW→CIC, removing TTL *raises* F1 for all three arms at k = 1, 5 and 10 (e.g. k = 10: source 0.530→0.573, weighted 0.531→0.614, target-only 0.555→0.539 is the only drop). In CIC→UNSW at k = 1, target-only rises (0.154→0.162).
  - Comparison: in CIC→UNSW with TTL removed, the weighted source beats target-only by +0.167 F1 at k = 5 (8/10 seeds) and +0.147 at k = 10 (8/10 seeds). Exact two-sided Wilcoxon p = 0.037 and 0.014. Under §3.4's rule these are *helps*. In UNSW→CIC the gaps are +0.048 and +0.076 (p = 0.16, 0.065). With all features the CIC→UNSW gaps are only +0.056 and +0.020.
  - So in the one pair studied, the artifact ablation *widens* the source's advantage.
- *Suggested fix:*
  - Report the −TTL comparison with its paired tests and correct the "every method" sentence.
  - Discuss honestly that TTL may mask a transfer benefit on CIC↔UNSW.
  - Ideally, rerun E3 (or at least E2) with TTL removed across all pairs before claiming the result is artifact-independent.
  - Adjust the Conclusion's "rather than a single artifact" accordingly. The domain-AUC ablation shows separability is not one artifact, but that is a different claim from transfer being unaffected.

**2. Major. Title, "Source Data Adds Nothing to Few-Shot Cross-Dataset Intrusion Detection".**
- *Problem:* The title asserts an absence of effect that the analysis cannot establish.
- *Evidence:*
  - The source significantly helps in 34 (per-domain) and 41 (shared) of 540 cells. With n = 10 and α = 0.05, roughly 11–13 helps per direction are expected under a global null, so helps are about three times the chance rate.
  - 65% and 54% of cells are "no difference", which is non-rejection, not equivalence. No CI or equivalence bound on ΔF1 is reported.
  - The body itself says "no consistent benefit" (§4.3, §8).
  - Finding 1 adds significant helps.
- *Suggested fix:* Use body-faithful wording, e.g. "…Source Data Gives No Consistent Benefit…" or "…Is Not Transfer". Alternatively, add an equivalence analysis (TOST on ΔF1 with a stated margin) if "adds nothing" is to be kept.

**3. Major. §3.4 / §4.3, "we therefore interpret the uncorrected verdicts as a pattern".**
- *Problem:* The "pattern" is a tally of non-independent uncorrected tests with no inferential test of its own. Holm cannot reject anything with 10 seeds (the floor p = 0.002 is above 0.05/540 ≈ 9.3×10⁻⁵), so "the correction is strict" understates the issue: it is infeasible by design.
- *Evidence:*
  - `e3_significance.csv` has min p 0.0020, and every Holm verdict is "no diff".
  - Target-only bacc is identical for every pair with the same target (facts.md "target-only bacc"), so the 540 cells share control arms.
- *Suggested fix:*
  - Add a pooled analysis: a mixed-effects or meta-analytic estimate of ΔF1 with CIs, with random effects for target, pair and seed, or a cluster bootstrap over targets and seeds.
  - Report per-method/model/k mean ΔF1 with CIs.
  - State plainly that per-cell FWER control was unattainable, and consider Benjamini–Hochberg as a secondary analysis.
  - Recommendation 2 in §7 should then say how many seeds make correction feasible.

**4. Major. §4.3 / §5.2 / §6.3, "Under shared scaling the most favourable pair is BoT→CIC".**
- *Problem:* The exceptions are selected and then used to build hypotheses that the omitted data contradict.
- *Evidence:*
  - Shared scaling, by pair (facts.md): UNSW→BoT has 9 helps and 3 hurts (net +6), which is more favourable than BoT→CIC (14/16, net −2). §4.3 calls BoT→CIC "most favourable" by help count alone.
  - UNSW→BoT has the *lowest* source–target importance correlation of all pairs (0.253; facts.md E5). This directly contradicts §5.2/§6.3's "shared feature reliance may be a precondition for benefit".
  - Its helps occur at k = 1, 10, 50 and 100, contradicting "a source may help when target labels are extremely scarce".
  - Aggregate helps by k are flat or rising (per-domain 9/3/4/8/10; shared 11/6/5/8/11).
- *Suggested fix:* Report UNSW→BoT, rank pairs by net verdict, and either drop the two hypotheses in §6.3 or state the counter-evidence next to them.

**5. Major. §5.1 / §8, "The reason is that each network occupies its own region of feature space".**
- *Problem:* The causal language rests on a separability measure that has no negative control and that saturates.
- *Evidence:*
  - Domain AUC is ≥ 0.996 everywhere and does not correlate with benefit (ρ = 0.06, p = 0.85; §5.1).
  - No within-dataset baseline is given, for example two capture days of the same dataset or two halves of one testbed. A gradient-boosted discriminator on 45 tabular features may approach AUC 1.0 for many pairs of captures. If so, "AUC ≈ 1" does not distinguish networks that transfer from ones that do not.
  - Ben-David's bound also contains the joint-error term λ, which separability does not measure.
- *Suggested fix:*
  - Add a within-dataset temporal-split domain AUC as a reference point.
  - Soften "The reason is" to "consistent with" (§8; also "can't help because" in the blueprint wording).
  - Acknowledge that marginal separability is neither necessary nor sufficient for negative transfer.

**6. Major. §5.4, "Per-domain scaling is a hidden confound".**
- *Problem:* The framing is in tension with the mechanism argument. Per-domain z-scoring is feature-wise moment matching, a mild form of domain alignment. By the paper's own data it *reduces* importance-weight degeneracy: ESS median 34% versus 0.8% under shared scaling (§6.2). Removing it makes transfer worse (153→205 hurts), even though it was said to "inflate separability". If separability drove harm, lower separability should not increase harm.
- *Evidence:* facts.md IW ESS; Table 2; §5.4's single-feature counts (13 vs 231 of 270).
- *Suggested fix:*
  - Present per-domain scaling as having two effects: it aligns continuous marginals but creates spurious separability through categorical and constant columns.
  - Narrow the "confound" claim to separability measurement and to the ToN→CIC exception.
  - Reconcile it explicitly with §5.1.

**7. Major. §3.4, "This is the test recommended for comparing two classifiers over repeated measurements (Demšar, 2006)".**
- *Problem:* Misattribution. Demšar recommends the Wilcoxon signed-rank test for comparing two classifiers over *multiple data sets*, and argues that repeated runs on one data set are not independent samples.
- *Evidence:* references.json `demsar2006statistical` summary ("comparing classifiers over multiple data sets"). The citation is abstract-only per citation_audit.md.
- *Suggested fix:* Cite Demšar for the across-dataset use only. Justify the seed-level test separately, and acknowledge that resampled splits overlap. Nadeau–Bengio corrected resampled t-tests are the usual reference, but the author must verify and add it, since it is not in the corpus.

**8. Major. §3.3, "The RF keeps its 100 source trees and grows 100 more on the target flows".**
- *Problem:* The adaptation arms are not established methods and their hyper-parameters are not tuned, so a hostile reviewer will call them straw men. The title's generality amplifies the risk.
  - Appending trees gives the source half the vote regardless of k.
  - GBT residual fitting on 2–10 flows and an MLP fine-tune with no stated learning rate or freezing are not standard either.
  - Domain-adversarial training (cited in §2.4) and other modern methods are absent.
- *Evidence:* §3.3; §6.5 lists these exclusions but does not engage with their effect on the conclusion.
- *Suggested fix:*
  - Justify each arm, or add at least one standard method (e.g. DANN for the MLP, or refitting the RF with source/target sample weights tuned on a target validation split).
  - State the learning rate and other fine-tuning details.
  - Scope the title and abstract to "the adaptation methods tested".

**9. Major. §3.4, "We report F1 on the attack class".**
- *Problem:* The Table 2 verdicts use attack-class F1 at the natural test prevalence. When BoT is the target (97.5% attacks), flagging everything gives F1 ≈ 0.987. F1 there is insensitive to false alarms, and 3 of the 12 pairs have BoT as the target.
- *Evidence:* Table 1 attack rate; §4.4 itself shows recall 1.0 at FPR 1.0. Under per-domain scaling, the BoT-target pairs contribute 48 of the 153 hurts (CIC→BoT 24, ToN→BoT 14, UNSW→BoT 10).
- *Suggested fix:* Repeat the verdict tally on balanced accuracy or MCC as a robustness column, or exclude the BoT-target pairs in a sensitivity check.

**10. Minor. §4.5, "we repeat the TAN-IDS setting".**
- *Problem:* The setting is not repeated. TAN-IDS uses an 8-D interface, a 70% training split, XGBoost and (per its notes) likely the original CSV feature sets. Here the setup is 45 v3 features, a 50% pool, GBT and only two of the three adaptation methods. The blueprint's concession ("we test the assumption, not their exact numbers") was dropped. §1 also calls TAN-IDS "an evaluation framework for NetFlow-based detectors", although references.json notes it likely uses non-NetFlow columns.
- *Evidence:* references.json `hathanh2026tanids` method_weaknesses; argument_blueprint SA3 counter-argument.
- *Suggested fix:* Use "emulate TAN-IDS's 5% label budget". Restore the concession. Qualify "NetFlow-based".

**11. Minor. §5.1, "Under per-domain scaling the separation is the same or higher."**
- *Problem:* The statement is false in several cells.
- *Evidence:* e5_log.txt: unsw-bot DoS 0.9990→0.9983; cic-unsw DoS 1.0000→0.9998; ton-bot DoS 1.0000→0.9997; unsw-bot scanning 0.9997→0.9996; unsw-ton scanning 0.9998→0.9997.
- *Suggested fix:* "essentially unchanged (within ±0.001)".

**12. Minor. §4.3, "The source does the most damage at exactly the small budgets where it is supposed to help".**
- *Problem:* Over-statement.
- *Evidence:* The per-domain median at k = 1 (−0.015) is smaller in magnitude than at k = 5 and 10. Hurt counts do not fade with k (per-domain 27/31/35/31/29). Under shared scaling, hurts peak at k = 50 (56) and k = 100 (49).
- *Suggested fix:* Restrict the claim to median ΔF1 under per-domain scaling at k = 5–10, and report the hurt-count trend.

**13. Minor. §5.2, "Adding the source mainly makes the model more conservative… shifts the decision threshold".**
- *Problem:* The claim holds only for pooling. Fine-tuning *raises* FPR at k = 10 (GBT 0.226 vs 0.197 target-only; RF 0.183 vs 0.163). "Decision threshold" is an interpretation with no ROC or threshold analysis behind it.
- *Evidence:* e5_log.txt FPR table.
- *Suggested fix:* Say "Pooling makes the model more conservative". Report the fine-tuning FPRs. Either drop "threshold" or support it with an AUROC comparison.

**14. Minor. §6.1, "at small budgets it usually does better" / "Kim finds target-only learning competitive with… every adaptation method".**
- *Problem:* Both statements over-claim.
  - Target-only is *significantly* better in only 28–38% of cells, so "usually" is defensible only for the sign of the median.
  - In Kim's LMD→ADFA direction, target-only clearly loses (0.442 vs 0.579), so it is not "competitive".
  - Xu et al.'s headline Table 11 shows transfer +0.1 pp at K = 5, which conflicts with their Tables 8–9, and transfer helped at K = 10/15 on CICIDS2017. Neither point is mentioned.
- *Evidence:* references.json `kim2026prototype` and `xu2025multimodal` method_weaknesses.
- *Suggested fix:* Use "the median change is negative". Write "better in one direction, worse in the other" for Kim. Note Xu's internal inconsistency and the K = 10/15 gains.

**15. Minor. §4.4, "the best F1 is 0.21 on a balanced test set… balanced accuracy never exceeds 0.55".**
- *Problem:* The replication is reported selectively. Their set A (TTL removed only) reaches F1 0.540 on the balanced UNSW→CIC test, though at bacc 0.541. The all-features baseline reaches bacc 0.552, which is above 0.55.
- *Evidence:* facts.md E4a.
- *Suggested fix:* Report set A, and note that its F1 comes with near-chance bacc. Write "≤ 0.55 for their feature sets A–C". The README already scopes "0.21" to Set C.

**16. Minor. §3.5, "within each attack category the two datasets share (20,000 flows per side, 5 seeds)".**
- *Problem:* Several shared categories have fewer than 20,000 flows on one side (UNSW backdoor 4,659 and DoS 5,980; CIC web 261). The CIC–ToN web category returns NaN and is silently dropped from §5.1's list.
- *Evidence:* e5_log.txt category counts and the `cat:web NaN` row.
- *Suggested fix:* Write "up to 20,000 per side". State that web was omitted (too few CIC flows).

**17. Minor. Citation attributions beyond the source summaries.**
- (a) §5.4, "in-dataset evaluations normalize each dataset on its own terms (Sarhan et al., 2022)". The verified §4 locator supports only the TTL drop.
- (b) §3.1 cites Alsaedi et al. for "the network portion of ToN_IoT", but references.json says it covers telemetry, not network flows.
- (c) §2.3 says Roy & Minu's scores "vanish". The summary gives 99.28% vs 92.6%, which is a reduction, and "static identifiers" is not in the summary.
- (d) §1 says Goldschmidt & Chudá "document design limitations that make such shortcuts available", which stretches "common data limitations".
- (e) §1 calls Hakim's recovery "similar". DT goes 0.17→0.64 at 25% labels and the 1D-CNN shows no gain, which is not similar to TAN-IDS's 0.98 at 5%.
- (f) §2.3 attributes "full 38-feature set" to Sarhan 2021, but this is not in the notes.
- (g) 33 of 41 sources are abstract-only (citation_audit.md). Several of them, such as Arp, Ben-David and Shimodaira (whose summary is "from general knowledge"), carry argument weight.
- *Suggested fix:* Re-anchor or soften each case. For (a), find a source or present it as the author's observation. Drop Alsaedi from the network-data citation. Read the argument-bearing sources and record them with `/ars-mark-read`.

**18. Minor. §2.2, "TAN-IDS is the nearest prior work, and the difference is precisely that control."**
- *Problem:* Inconsistent with the preceding paragraph. Xu et al. already includes a target-only control, so the difference from TAN-IDS is not "precisely that control" for the field as a whole.
- *Evidence:* §2.2 ¶2; references.json `xu2025multimodal`.
- *Suggested fix:* Name TAN-IDS as the nearest *NetFlow recovery* study and Xu et al. as the nearest *target-only-controlled* study. State the difference from each (repeated tested runs, NetFlow v3, 12 pairs).

**19. Minor. ../README.md, "Shared scaling (main setting)" and "(most-relied-on first, TTL first)".**
- *Problem:* The README contradicts the paper and blueprint, where per-domain is the main setting (author decision D1 = A). It also says TTL is removed first, whereas the paper reports TTL among the first five removed in 24 of 36 runs. The README's "28% of UNSW-NB15 attacks" is the only source for the §3.1 figure, which does not appear in facts.md.
- *Suggested fix:* Align the README with the paper. Have `extract_facts.py` print the 28% figure.

**20. Minor. Table 2, the abstract, and formatting.**
- *Problem:*
  - Table 2 stacks method rows and model rows with a single bold "All" row, which reads as a sum over six rows.
  - The abstract's "helps in 6% and hurts in 28%" does not say these are uncorrected p < 0.05 verdicts.
  - The citation style is author-year while IEEE is the stated target.
  - §3 runs 1,322 words against about 1,100.
- *Suggested fix:*
  - Split Table 2 into "By method" and "By model" panels, and add a "By k" panel, as the blueprint planned.
  - Add "(uncorrected paired tests)" to the abstract.
  - Convert the citation style.
  - Trim §3.

### Check (a): numbers not exactly supported
Every other number in the draft and abstract matches facts.md or e5_log.txt exactly, or is a correct rounding. This covers Table 1, Table 2, all §4.1–4.5 values, §5.1–5.4, §6.2 ESS, and the abstract's 6%/28%/8%/38%/0.81/0.996/23–40.
- The BoT→CIC by-k claims (12 of 14 helps at k ≤ 5; all 16 hurts at k ≥ 10) are not in facts.md but were verified against `results/e3_significance_shared.csv`.
- Mismatches or unsupported values are in Findings 1 (§5.3 "every method"), 11 (§5.1 "same or higher"), 15 (§4.4 "never exceeds 0.55" if the all-features row counts) and 16 (§3.5 "20,000 per side").
- Unverified against printed facts: §3.1 "28%" (README only); §4.1 "far higher" recall at k = 1; §4.1 "smaller than the seed-to-seed spread" (true per `e1_summary.csv` f1_std of about 0.10–0.29, but not printed in facts.md); §4.5 "tens of thousands" (82,789 in `e4_budget_runs.csv`); §5.4 "never falls below AUC 0.95 … with 44 of 45 removed" (consistent with empty thresholds in `e5_ablation_summary.csv`, not printed in facts.md).
- §4.5 "within ±0.006": MLP fine-tuned UNSW→CIC is +0.0062. This is acceptable after rounding.

## Evaluator Decision

evaluator_decision=request_revision

Revision priorities, in order:
1. Finding 1: correct §5.3 and report the −TTL paired tests. Rerunning the main comparison without TTL is strongly advised.
2. Findings 2–4: retitle; add an aggregate or equivalence analysis; report the omitted exceptions and revise the §6.3 hypotheses.
3. Findings 5–9: methodological framing and robustness (domain-AUC negative control, the scaling-confound framing, the Demšar citation, justification of the adaptation arms, a bacc/MCC verdict column).
4. Findings 10–20: precision edits.

criteria_binding_unavailable
