# Literature Search Report — TRACE-IDS

*Phase 1 (lit-review mode) · Paper Configuration Record: `../paper_configuration_record.md` · Domain evidence profile: `cs_ml` · Generated 2026-10-11*

> **Reading status.** No source here is marked as read by the author. "Full text" below means an AI agent
> extracted and read the PDF; it is **not** an `/ars-mark-read` attestation. The author records their own
> reading later with `/ars-mark-read <key> --scope …`, against `../trace_ids_passport.yaml`.

## Search Strategy

| Item | Value |
|---|---|
| Concepts | (1) cross-dataset / cross-domain NIDS generalization; (2) few-shot / limited-label adaptation, transfer learning, negative transfer, covariate shift; (3) dataset artifacts / shortcut learning in NIDS benchmarks; (4) NetFlow feature sets and the four NF datasets; (5) statistics for classifier comparison |
| Core string | (`"intrusion detection"` OR NIDS) AND (`cross-dataset` OR `cross-domain` OR `transfer` OR `few-shot` OR `domain adaptation`) AND (NetFlow OR flow) |
| Artifact string | (`"intrusion detection"` OR NIDS) AND (`shortcut` OR `artifact` OR `dataset errors` OR `design smells` OR `leakage`) |
| Sources searched | Seeded by the author's gap check (`research/gap_check_3w.md`) and must-cite list; expanded via web search; every hit confirmed on Crossref, the arXiv API, OpenAlex, dblp or the publisher page |
| Date range | No lower bound for foundations (statistics, transfer theory); 2020–2026 for NIDS-specific work |
| Language | English |
| Last searched | 2026-10-11 |
| Inclusion | Addresses one of the 5 concepts; verifiable record; under `cs_ml`, arXiv preprints and conference papers admitted |
| Exclusion | Unverifiable record; off-topic; blog/news |

**Search bound for any novelty claim.** The gap statements below hold *within this search* (the strings and seed set above, as of 2026-10-11). They are not a claim that no such work exists anywhere.

## Coverage Distribution Advisory

No distributional skew advisory triggered:
- **Time:** 12 of 41 sources from 2024–2026, 16 from 2020–2023, 8 from 2010–2019, 5 pre-2010.
- **Venue type:** 24 journal articles, 9 conference papers, 6 preprints, 2 chapters.
- **Venue family:** the largest single venue is arXiv, with 6 of 41.

## Screening Results

- Must-cite list from the author: 14 items + 4 dataset papers. All found. Two were corrected: 2108.12732 is a different paper than expected, and 2503.04404 has since been published under a new title (see *Corrections*).
- Added by search after full-text or abstract screening: 23.
- Excluded as unverifiable: 1 (Rosenstein et al. 2005, "To transfer or not to transfer"; no resolvable record found).
- **Final included: 41**, all verified. Read scope: 6 full text (the 6 local PDFs, read by an AI agent), 35 abstract or metadata only.

## Corrections to earlier assumptions (act on these before drafting)

1. **TTL artifact support is thin.** The NetFlow v3 paper (`luay2025temporal`) does **not** warn about TTL or any artifact feature (Sections 1–6 checked). The only verified source that states the TTL mechanism is Atif & Ali (`atif2026threeaxis`, §3.3), on NetFlow v2, and it shows no TTL distributions. `PUBLICATION_PLAN.md` also attributes a "TTL = hidden label" statement to Sarhan et al. 2108.12732 §5.1.1. That paper is actually a feature-ranking study (`sarhan2021featureanalysis`), and it was screened on its abstract only, so **that citation is not yet confirmed**. Someone must open 2108.12732 and 2101.11315 and check the TTL statements before the paper cites them for TTL.
2. **2503.04404** was published as *"Time Matters: Temporal NetFlow Features for ML-Based Network Intrusion Detection"*, IEEE Access 14:66899–66913 (2026), DOI 10.1109/ACCESS.2026.3688204 (`luay2026timematters`). The author list differs from the arXiv record. Cite the published version for the NF v3 datasets once its full text is checked.
3. **Kim 2026** is about host logs (Linux syscalls ↔ Windows Sysmon), not network flows. Cite it for target-only baselines in few-shot domain adaptation, not as NetFlow work.
4. **Xu et al. 2025 and Kim 2026 *do* include a target-only baseline.** The paper must say "few NIDS studies", not "no study". Within this search, the NetFlow-specific gap still holds (see *Identified Gaps*).
5. **Dataset citations.** Use `moustafa2021tonnetwork` for ToN_IoT network data (`alsaedi2020ton` covers telemetry only). `sharafaldin2018toward` is the conventional citation for CSE-CIC-IDS2018, even though it introduces CICIDS2017.

## Literature Matrix

Themes: **T1** cross-dataset failure · **T2** limited-label adaptation / transfer · **T3** target-only baseline present · **T4** dataset artifacts / shortcuts · **T5** NetFlow data · **T6** theory / statistics. ● = main theme, ○ = touches.

| Source | T1 | T2 | T3 | T4 | T5 | T6 | Method | Read |
|---|---|---|---|---|---|---|---|---|
| hathanh2026tanids (TAN-IDS) | ● | ● | no | | ○ | | Empirical, 1 run | full |
| atif2026threeaxis | ● | | no | ● | ● (v2) | | Empirical, zero-shot | full |
| hakim2026crossdomain | ● | ● | no | ● | | | Empirical, IIoT | full |
| xu2025multimodal | | ● | **yes** | | | | Empirical, packets | full |
| kim2026prototype | | ● | **yes** | | | ○ | Empirical, host logs | full |
| luay2025temporal / luay2026timematters | | | | ○ | ● | | Dataset (descriptive) | full / abstract |
| cantone2024cross | ● | | | | | | Empirical | abstract |
| layeghy2023explainable | ● | | | ○ | ● | | Empirical | abstract |
| apruzzese2022cross | ● | | | | | | Empirical | abstract |
| dhooge2020inter | ● | | | | | | Empirical | abstract |
| sarhan2023zeroshot | ○ | ● | | | ● | | Empirical | abstract |
| sarhan2022standard, sarhan2021netflow | | | | | ● | | Dataset | abstract |
| sarhan2021featureanalysis | | | | ○ | ● | | Feature ranking | abstract |
| goldschmidt2025network | ○ | | | ● | ○ | | Survey | abstract |
| roszeitis2026fewshot | | ● | | | | | Survey | abstract |
| arp2022dos | | | | ● | | | Position / empirical | abstract |
| geirhos2020shortcut | | | | ● | | | Position | abstract |
| engelen2021troubleshooting, lanvin2023errors | | | | ● | | | Dataset audit | abstract |
| flood2024bad | | | | ● | | | Dataset audit | abstract |
| roy2026unmasking | | | | ● | | | Empirical | abstract |
| apruzzese2023sok, sommer2010outside | ○ | | | ● | | | Position / SoK | abstract |
| moustafa2015unsw, sharafaldin2018toward, moustafa2021tonnetwork, alsaedi2020ton, koroniotis2019bot | | | | | ● | | Dataset | abstract |
| pan2010survey, zhang2023negative | | ● | | | | ● | Survey | abstract |
| bendavid2010theory | | ● | | | | ● | Theory | abstract |
| shimodaira2000improving, sugiyama2007covariate | | ● | | | | ● | Theory (importance weighting) | abstract |
| ganin2016domain, rabanser2019failing | | ○ | | | | ● | Method (domain classifier / shift) | abstract |
| wilcoxon1945individual, holm1979simple, demsar2006statistical | | | | | | ● | Statistics | abstract |
| grinsztajn2022why | | | | | | ● | Empirical (tabular models) | abstract |

## Identified Gaps (bounded by this search, 2026-10-11)

1. **No NetFlow few-shot study isolates the source's contribution.** The closest work (TAN-IDS; Hakim) adapts with source + few target labels but never trains on the same target labels alone. TAN-IDS is also a single run with no significance tests (author-acknowledged, §6.2). *This paper fills that gap: target-only vs 3 adaptation methods × 3 models × 12 pairs × 10 seeds, Wilcoxon + Holm.*
2. **Where target-only baselines exist, they are underpowered or off-domain.** Xu et al. use near-domain CIC-2017↔2018 pairs, about 30 test samples per class, no statistics, and test-set model selection. Their own tables still show source pretraining hurting at small K. Kim uses host logs and n=5 seeds, so Wilcoxon cannot reach p<0.05. *This paper: same comparison, NetFlow, adequately powered.*
3. **Zero-shot claims are not robust.** Atif & Ali's UNSW→CIC F1 of 0.81 comes from a feature set chosen using target F1 (§3.3, reader-inferred optimistic bias), on NetFlow v2. *This paper: does not reproduce on v3 (E4a).*
4. **Artifact analyses don't measure how deep separability goes.** Prior work removes named features (TTL, ports) and reports that transfer changes. None of the screened sources counts how many features must go before the domains become indistinguishable. *This paper: 22–40 of 45 features (E5 follow-up).*
5. **Preprocessing as a confound.** None of the screened sources examines per-domain normalization as a cause of cross-dataset separability. *This paper: per-domain z-scoring makes 231/270 single features near-perfect domain separators vs 13/270 raw.*

## Recommended Sources by Paper Section

| Section | Key sources |
|---|---|
| Introduction | arp2022dos, geirhos2020shortcut, sommer2010outside, cantone2024cross, hathanh2026tanids, goldschmidt2025network |
| Related work: cross-dataset NIDS | cantone2024cross, layeghy2023explainable, apruzzese2022cross, dhooge2020inter, atif2026threeaxis, hakim2026crossdomain |
| Related work: few-shot / transfer for NIDS | hathanh2026tanids, xu2025multimodal, kim2026prototype, sarhan2023zeroshot, roszeitis2026fewshot |
| Related work: artifacts and shortcuts | arp2022dos, geirhos2020shortcut, engelen2021troubleshooting, lanvin2023errors, flood2024bad, roy2026unmasking, apruzzese2023sok, atif2026threeaxis |
| Data | luay2025temporal / luay2026timematters, sarhan2022standard, sarhan2021netflow, moustafa2015unsw, sharafaldin2018toward, moustafa2021tonnetwork, koroniotis2019bot |
| Method: transfer baselines | pan2010survey, shimodaira2000improving, sugiyama2007covariate, ganin2016domain, rabanser2019failing |
| Method: statistics | wilcoxon1945individual, holm1979simple, demsar2006statistical |
| Discussion | bendavid2010theory, zhang2023negative, grinsztajn2022why, kim2026prototype, xu2025multimodal |

## Annotated Bibliography

Generated from `references.json`, the verified records. The full per-source annotations are in
[`_annotated_bibliography.md`](_annotated_bibliography.md), grouped by section. Each entry gives type, venue, identifier, verification URL, summary, relevance and method weaknesses. Method weaknesses are listed only for the 6 full-text reads, each tagged `author-acknowledged` with a section, or `reader-inferred`.
