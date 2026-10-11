# Citation Audit (Phase 5a)

- In-text citations: 83; distinct sources: 41; corpus size: 41
- Orphans (cited, not in corpus): none
- Uncited corpus entries: none
- Every citation has a slug + anchor: True; anchor kinds: {'section': 83}
- Verified records (DOI/arXiv/publisher opened): 41/41
- Self-citations: 0 (41 sources; author has no prior publications in the corpus)

## Sources without DOI (identifier used instead)
- `hakim2026crossdomain`: arXiv 2607.00553 — AUTHOR-NAME DISCREPANCY: the arXiv API lists the third author as 'Talha Ibne Anis', while the PDF byline reads 'Talha Ibne Anich'. I used th
- `roszeitis2026fewshot`: arXiv 2609.11275 — Preprint, v1 10 Sep 2026; not peer reviewed as far as the arXiv record shows. I only read the abstract, so I have not checked whether it rep
- `arp2022dos`: arXiv 2010.09470 — No DOI (USENIX open proceedings). Distinguished Paper Award per USENIX page.
- `luay2025temporal`: arXiv 2503.04404 — TTL QUESTION: the paper does NOT warn about TTL or any other artifact feature. TTL appears only as MIN_TTL, MAX_TTL and DNS_TTL_ANSWER rows 
- `atif2026threeaxis`: arXiv 2609.13511 — Uses NetFlow v2, not v3. Authors disclose LLM (Claude) assistance in the paper's 'LLM Usage Statement'. Code: github.com/ebadatif/IDS-three-
- `roy2026unmasking`: arXiv 2609.28725 — Preprint, 'Currently under review' per arXiv comment. Different dataset (not NetFlow v3).
- `sarhan2021featureanalysis`: arXiv 2108.12732 — CHECK: this is NOT the NetFlow-v2 datasets paper. If you meant the NetFlow datasets paper, use sarhan2022standard (2101.11315) or sarhan2021
- `sugiyama2007covariate`: https://jmlr.org/papers/v8/sugiyama07a.html — JMLR page shows '8(35):985-1005, 2007'; no DOI.
- `ganin2016domain`: arXiv 1505.07818 — The JMLR page renders the 7th author as 'Mario March' (truncated). arXiv lists 'Mario Marchand', which I use.
- `grinsztajn2022why`: arXiv 2207.08815 — TITLE DIFFERS: the NeurIPS proceedings title includes 'typical' ('...on typical tabular data?'); arXiv v1 omits it. Use the NeurIPS title. A
- `demsar2006statistical`: https://jmlr.org/papers/v7/demsar06a.html — JMLR page shows 7(1):1-30, 2006; no DOI.
- `holm1979simple`: https://www.jstor.org/stable/4615733 — Verified via OpenAlex only (title, author, year, vol 6, pp 65-70); the JSTOR page blocked automated access. OpenAlex lists DOI 10.2307/46157
- `rabanser2019failing`: arXiv 1810.11953 — NeurIPS page lists the author as 'Zachary Lipton' and arXiv as 'Zachary C. Lipton'. Page numbers not recorded; no DOI.

## Sources older than 10 years (all seminal: statistics, transfer theory, original datasets)
- `sommer2010outside` (2010)
- `pan2010survey` (2010)
- `bendavid2010theory` (2010)
- `shimodaira2000improving` (2000)
- `sugiyama2007covariate` (2007)
- `moustafa2015unsw` (2015)
- `wilcoxon1945individual` (1945)
- `demsar2006statistical` (2006)
- `holm1979simple` (1979)

## Read-scope advisory: 33 sources cited only against their abstract
These citations are anchored `section:abstract` because the source was screened from its abstract only.
Before submission, the author should read at least the ones that carry an argument, then record it with `/ars-mark-read`:
- `alsaedi2020ton` — cited 1×
- `apruzzese2022cross` — cited 2×
- `apruzzese2023sok` — cited 1×
- `arp2022dos` — cited 3×
- `bendavid2010theory` — cited 3×
- `cantone2024cross` — cited 2×
- `demsar2006statistical` — cited 1×
- `dhooge2020inter` — cited 2×
- `engelen2021troubleshooting` — cited 1×
- `flood2024bad` — cited 2×
- `ganin2016domain` — cited 2×
- `geirhos2020shortcut` — cited 2×
- `goldschmidt2025network` — cited 3×
- `grinsztajn2022why` — cited 1×
- `holm1979simple` — cited 1×
- `koroniotis2019bot` — cited 1×
- `lanvin2023errors` — cited 1×
- `layeghy2023explainable` — cited 2×
- `luay2026timematters` — cited 1×
- `moustafa2015unsw` — cited 1×
- `moustafa2021tonnetwork` — cited 1×
- `pan2010survey` — cited 2×
- `rabanser2019failing` — cited 1×
- `roszeitis2026fewshot` — cited 2×
- `roy2026unmasking` — cited 1×
- `sarhan2021netflow` — cited 1×
- `sarhan2023zeroshot` — cited 1×
- `sharafaldin2018toward` — cited 1×
- `shimodaira2000improving` — cited 3×
- `sommer2010outside` — cited 1×
- `sugiyama2007covariate` — cited 2×
- `wilcoxon1945individual` — cited 1×
- `zhang2023negative` — cited 2×
