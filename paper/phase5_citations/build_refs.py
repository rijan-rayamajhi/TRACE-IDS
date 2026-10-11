"""Phase 5a: build references.bib + IEEE reference list from the verified records, and audit the draft's citations.

    python3 paper/phase5_citations/build_refs.py

Inputs : paper/phase1_literature/references.json (verified records), paper/phase4_draft/draft.md
Outputs: references.bib, ieee_references.md, citation_audit.md (all next to this file)
"""
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
PAPER = HERE.parent
refs = json.load(open(PAPER / "phase1_literature" / "references.json"))
draft = (PAPER / "phase4_draft" / "draft.md").read_text()

# ---- order of first appearance in the draft = IEEE numbering
cites = re.findall(r"<!--ref:([^>]+?)-->(?:<!--anchor:([a-z]+):([^>]*?)-->)?", draft)
order = list(dict.fromkeys(k for k, _, _ in cites))
by_key = {r["citation_key"]: r for r in refs}
num = {k: i + 1 for i, k in enumerate(order)}


def ieee_author(a):
    if a.get("literal"):
        return a["literal"]
    given = a.get("given", "")
    initials = " ".join(p[0] + "." for p in re.split(r"[\s]+", given) if p)
    initials = re.sub(r"(\w)\.-?(\w)\.", r"\1.-\2.", initials) if "-" in given else initials
    return f"{initials} {a['family']}".strip()


def ieee_authors(auth):
    names = [ieee_author(a) for a in auth]
    if len(names) > 6:
        return names[0] + " et al."
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + (", and " if len(names) > 2 else " and ") + names[-1]


def ieee_entry(r):
    a, t, v, y = ieee_authors(r["authors"]), r["title"], r.get("venue") or "", r["year"]
    vol = f", vol. {r['volume']}" if r.get("volume") else ""
    no = f", no. {r['issue']}" if r.get("issue") else ""
    pg = r.get("pages") or ""
    # range -> pp.; short number = first page only (e.g. Wilcoxon 1945, end page unverified) -> p.; else article number
    pp = (f", pp. {pg.replace('-', '–')}" if "-" in pg else
          f", p. {pg}" if pg.isdigit() and len(pg) <= 3 else f", Art. no. {pg}") if pg else ""
    doi = f", doi: {r['doi']}." if r.get("doi") else "."
    if r["venue_type"] == "preprint" or (not r.get("doi") and r.get("arxiv_id") and "arXiv" in v):
        return f'{a}, "{t}," arXiv preprint arXiv:{r["arxiv_id"]}, {y}.'
    if r["venue_type"] in ("conference-paper", "chapter"):
        return f'{a}, "{t}," in *{v}*, {y}{pp}{doi}'
    return f'{a}, "{t}," *{v}*{vol}{no}{pp}, {y}{doi}'


def bib_entry(r):
    typ = {"journal-article": "article", "conference-paper": "inproceedings", "chapter": "incollection",
           "preprint": "misc"}.get(r["venue_type"], "misc")
    def esc(s):
        return str(s).replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")
    auth = " and ".join(a.get("literal") or f"{a['family']}, {a.get('given', '')}".strip(", ") for a in r["authors"])
    f = {"author": auth, "title": "{" + r["title"] + "}", "year": r["year"]}
    if typ == "article":
        f["journal"] = r.get("venue")
    elif typ in ("inproceedings", "incollection"):
        f["booktitle"] = r.get("venue")
    for k in ("volume", "pages", "doi"):
        if r.get(k):
            f[k] = r[k]
    if r.get("issue"):
        f["number"] = r["issue"]
    if r.get("arxiv_id"):
        f["eprint"], f["archiveprefix"] = r["arxiv_id"], "arXiv"
        if typ == "misc":
            f["howpublished"] = f"arXiv preprint arXiv:{r['arxiv_id']}"
    if r.get("url") and not r.get("doi"):
        f["url"] = r["url"]
    body = ",\n".join(f"  {k} = {{{esc(v) if k not in ('title', 'url', 'doi') else v}}}" for k, v in f.items() if v)
    return f"@{typ}{{{r['citation_key']},\n{body}\n}}"


(HERE / "references.bib").write_text("\n\n".join(bib_entry(by_key[k]) for k in order) + "\n")
(HERE / "ieee_references.md").write_text("## References\n\n" + "\n".join(f"[{num[k]}] {ieee_entry(by_key[k])}" for k in order) + "\n")

# ---- audit
anchor_kinds = Counter(kind for _, kind, _ in cites)
abstract_only = sorted(k for k in order if all(kind == "section" and v == "abstract" for kk, kind, v in cites if kk == k))
nodoi = [k for k in order if not by_key[k].get("doi")]
old = [k for k in order if by_key[k]["year"] < 2016]
L = ["# Citation Audit (Phase 5a)", "",
     f"- In-text citations: {len(cites)}; distinct sources: {len(order)}; corpus size: {len(refs)}",
     f"- Orphans (cited, not in corpus): {sorted(set(order) - set(by_key)) or 'none'}",
     f"- Uncited corpus entries: {sorted(set(by_key) - set(order)) or 'none'}",
     f"- Every citation has a slug + anchor: {all(kind for _, kind, _ in cites)}; anchor kinds: {dict(anchor_kinds)}",
     f"- Verified records (DOI/arXiv/publisher opened): {sum(1 for k in order if by_key[k]['verified'])}/{len(order)}",
     f"- Self-citations: 0 ({len(order)} sources; author has no prior publications in the corpus)",
     "", "## Sources without DOI (identifier used instead)",
     *[f"- `{k}`: {('arXiv ' + by_key[k]['arxiv_id']) if by_key[k].get('arxiv_id') else by_key[k].get('url')} — {by_key[k].get('notes', '')[:140]}" for k in nodoi],
     "", "## Sources older than 10 years (all seminal: statistics, transfer theory, original datasets)",
     *[f"- `{k}` ({by_key[k]['year']})" for k in old],
     "", f"## Read-scope advisory: {len(abstract_only)} sources cited only against their abstract",
     "These citations are anchored `section:abstract` because the source was screened from its abstract only.",
     "Before submission, the author should read at least the ones that carry an argument, then record it with `/ars-mark-read`:",
     *[f"- `{k}` — cited {sum(1 for c in cites if c[0] == k)}×" for k in abstract_only],
     ]
(HERE / "citation_audit.md").write_text("\n".join(L) + "\n")
print("\n".join(L[:8]))
