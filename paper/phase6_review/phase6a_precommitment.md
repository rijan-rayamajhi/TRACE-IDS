<!-- Phase 6a — evaluator paper-blind pre-commitment. Inputs: evaluator_full contract (academic_paper/evaluator_full/v1) + paper metadata + writer <phase4a_output> only.
     title = "Is It Transfer? Source Data Adds Nothing to Few-Shot Cross-Dataset Intrusion Detection on NetFlow"
     field = Computer security — machine learning for network intrusion detection
     word_count = 7,000 (body)
     Writer 4a check (check_writer_artifact = pre_commitment_artifacts): the writer paraphrased all seven writer_full dimensions (D1 section_completeness ... D7 register_consistency), ends with the terminal tag, and commits to search-bounded novelty claims naming nearest prior work. This matches the evaluator's D3 #548 exception, so the two contracts align on how absence claims are judged. The writer's ±10% body word-count band (6,300–7,700) is noted for the D5 check. No drift found between the writer's paraphrase and this contract. -->

## Contract Paraphrase

### D1: originality
The paper must add something the field does not already have: new evidence, a new framing, or a new test, and not a restatement of known findings. For this title the claimed contribution is a negative/control result: in few-shot cross-dataset NetFlow intrusion detection, the source dataset adds nothing beyond what the few labelled target samples give. I will judge whether that gap is named precisely, whether prior transfer/cross-dataset work is engaged with on its merits rather than listed, and whether any novelty claim is search-bounded and names the closest prior work. Priority: high.

### D2: methodological_rigor
The design must fit the question. To show that "source data adds nothing", the paper needs a target-only baseline with the same few-shot budget, the same model and the same evaluation as the transfer arms. It also needs multiple seeds or splits, a stated statistical test, and enough detail (datasets, feature set, preprocessing, shot counts, label mapping, metrics) for someone to replicate it. Limitations must be stated and engaged with, not just listed. Priority: mandatory.

### D3: evidence_sufficiency
Every factual claim needs support: claims about prior work need a citation that actually says what is attributed to it, and claims about this study need the paper's own logged results. Discussion inferences must stay within what the data shows. A null result must be framed as "no detectable gain under these conditions" with uncertainty or equivalence evidence, not as proof of absence. Cells must not be cherry-picked. Search-bounded novelty claims are acceptable with documented search provenance plus the named nearest prior work (#548). Priority: mandatory.

### D4: argument_coherence
The question posed in the Introduction ("is it transfer?") must be answered in the Conclusion, with the same thesis in the Abstract, Introduction and Conclusion. Sections must connect logically, numbers must agree between abstract, body and tables, cross-references must resolve, and no passage may contradict another. Priority: high.

### D5: writing_quality
The prose must be clear, precise and in an academic register suited to a security/ML venue, with few grammar errors, a consistent citation style, and every figure and table referenced in the text. Length should be near the 7,000-word body target. Priority: normal.

## Scoring Plan

### D1: originality
- dimension_id: D1
- what_to_look_for: The Introduction names a specific gap (whether few-shot cross-dataset NIDS gains are attributable to source data rather than to the target shots) and the Related Work and Discussion engage the closest transfer/cross-dataset NetFlow studies substantively, with a search-bounded novelty claim.
- what_triggers_block: The contribution statement is vague or absent, the Discussion lists prior work without engagement, or the paper restates known conclusions with no added evidence.
- what_triggers_warn: The contribution exists but is weakly differentiated from cited prior work, or the novelty claim is broader than the documented search bound, or engagement is uneven across cited sources.

### D2: methodological_rigor
- dimension_id: D2
- what_to_look_for: A matched target-only control, multiple seeds, a named statistical test with correction or uncertainty intervals, and full replication detail (datasets, features, shots, model, metrics), with explicit and engaged limitations.
- what_triggers_block: The method does not match the research question (no matched target-only control), a significant design flaw such as leakage, limitations not discussed, or analysis that cannot be replicated from the description.
- what_triggers_warn: The method is fundamentally sound but insufficiently detailed, some choices lack justification, or limitations are mentioned but not engaged with.

### D3: evidence_sufficiency
- dimension_id: D3
- what_to_look_for: Every number traces to the logged results, every attributed claim matches its source, and the null is stated as "no detectable gain under these conditions" with appropriate uncertainty.
- what_triggers_block: Multiple core claims lack evidence, numbers in the text do not match the logged results, Discussion inferences exceed what the data supports, or there is cherry-picking of favourable evidence.
- what_triggers_warn: Core claims have evidence but some secondary claims lack support or over-claim a source, isolated number mismatches, or citation density is uneven across sections.

### D4: argument_coherence
- dimension_id: D4
- what_to_look_for: The "is it transfer?" question is answered consistently in the Abstract, Introduction and Conclusion, with resolving cross-references and matching numbers across abstract, body and tables.
- what_triggers_block: Multiple logical gaps between sections, a conclusion disconnected from the research question, or self-contradictory passages.
- what_triggers_warn: The overall logic holds but some transitions feel forced, or there are minor inconsistencies between section claims or between abstract and body.

### D5: writing_quality
- dimension_id: D5
- what_to_look_for: A consistent academic register, rare grammar errors, a consistent citation format, all figures and tables referenced in the text, and a body near 7,000 words.
- what_triggers_block: The text is difficult to understand, there are numerous grammar errors, the register is colloquial, or the citation format is inconsistent across the manuscript.
- what_triggers_warn: The text is readable but has several grammar or word-choice issues, some paragraphs are overly long, or there are minor citation format inconsistencies.

criteria_binding_unavailable

[PRE-COMMITMENT-ACKNOWLEDGED]
