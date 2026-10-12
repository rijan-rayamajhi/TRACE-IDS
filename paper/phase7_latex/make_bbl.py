"""Write main.bbl (IEEE-formatted thebibliography) so arXiv needs no BibTeX run, and assemble arxiv_final/.

    python3 paper/phase7_latex/make_bbl.py      (run after build_latex.py)

Entries come from paper/phase5_citations/ieee_references.md (built from the verified records), numbered in
order of first \\cite in main.tex, which must match the draft's citation order used to build that list.
"""
import re
import shutil
from pathlib import Path

HERE = Path(__file__).parent
PAPER = HERE.parent
tex = (HERE / "main.tex").read_text()
order = list(dict.fromkeys(k for g in re.findall(r"\\cite\{([^}]+)\}", tex) for k in g.split(",")))
draft = (PAPER / "phase4_draft" / "draft.md").read_text()
draft_order = list(dict.fromkeys(re.findall(r"<!--ref:([^>]+?)-->", draft)))
assert order == draft_order, "citation order differs between main.tex and draft.md"
entries = re.findall(r"^\[(\d+)\] (.+)$", (PAPER / "phase5_citations" / "ieee_references.md").read_text(), re.M)
assert [int(n) for n, _ in entries] == list(range(1, len(order) + 1))

ACC = {"é": "{\\'e}", "É": "{\\'E}", "á": "{\\'a}", "ü": '{\\"u}', "ö": '{\\"o}', "ë": '{\\"e}', "ç": "{\\c{c}}",
       "š": "{\\v{s}}", "’": "'", "–": "--", "—": "---"}


def tex_entry(t):
    doi = re.search(r"doi: (\S+?)\.$", t)
    t = re.sub(r"doi: \S+?\.$", "doi: @DOI@.", t)
    t = re.sub(r"(?<!\\)([&%#_$])", r"\\\1", t)
    t = re.sub(r"\*(.+?)\*", r"\\emph{\1}", t)
    t = re.sub(r'"(.+?),"', r"``\1,''", t)
    if doi:
        t = t.replace("@DOI@", "\\url{" + doi.group(1) + "}")
    for a, b in ACC.items():
        t = t.replace(a, b)
    assert all(ord(c) < 128 for c in t), t
    return t


bbl = ["\\begin{thebibliography}{99}", ""]
for key, (_, e) in zip(order, entries):
    bbl += [f"\\bibitem{{{key}}}", tex_entry(e), ""]
bbl.append("\\end{thebibliography}")
(HERE / "main.bbl").write_text("\n".join(bbl) + "\n")

out = Path.home() / "Desktop" / "arxiv_final"
if out.exists():
    shutil.rmtree(out)
(out / "figures").mkdir(parents=True)
for f in ("main.tex", "references.bib", "main.bbl"):
    shutil.copy(HERE / f, out / f)
for f in (HERE / "figures").iterdir():
    shutil.copy(f, out / "figures" / f.name)
shutil.make_archive(str(out), "zip", out)
print(f"main.bbl: {len(order)} entries; wrote {out}/ and {out}.zip:",
      sorted(str(p.relative_to(out)) for p in out.rglob("*") if p.is_file()))
