"""Phase 7: convert the Markdown draft + abstract into an arXiv-ready LaTeX package.

    python3 paper/phase7_latex/build_latex.py

Inputs : paper/phase4_draft/draft.md, paper/phase5_abstract/abstract.md, paper/phase5_citations/references.bib,
         results/*.png (figures)
Outputs: paper/phase7_latex/{main.tex, references.bib, figures/*.png} and paper/phase7_latex/arxiv_upload.zip
Citations become \\cite{key} (IEEE numeric style via IEEEtran.bst, which arXiv's TeX Live provides).
"""
import re
import shutil
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
PAPER = HERE.parent
REPO = PAPER.parent
FIG = HERE / "figures"

FIGURES = {  # number -> (files, caption, label)
    1: (["e1_recovery_shared.png"], None),
    2: (["e2_transfer.png"], None),
    3: (["e3_heatmap_shared.png", "e3_heatmap.png"], None),
    4: (["e5_families.png"], None),
    5: (["e5_ablation.png"], None),
}

UNI = {"−": "$-$", "→": "$\\to$", "–": "--", "—": "---", "×": "$\\times$", "↔": "$\\leftrightarrow$",
       "±": "$\\pm$", "∈": "$\\in$", "≈": "$\\approx$", "≥": "$\\geq$", "≤": "$\\leq$",
       "⁻³": "$^{-3}$", "⁻⁵": "$^{-5}$", "’": "'"}


def esc(t):
    """Escape LaTeX specials in plain text (not in already-built commands)."""
    t = t.replace("\\", "\\textbackslash{}")
    for a, b in [("&", "\\&"), ("%", "\\%"), ("#", "\\#"), ("_", "\\_"), ("$", "\\$"), ("{", "\\{"), ("}", "\\}"),
                 ("~", "\\textasciitilde{}"), ("^", "\\textasciicircum{}")]:
        t = t.replace(a, b)
    return t


def inline(t):
    """Markdown inline -> LaTeX. Citations and code spans are protected from escaping via placeholders."""
    keep = []

    def stash(s):
        keep.append(s)
        return f"\x00{len(keep) - 1}\x00"

    t = re.sub(r"<!--anchor:[^>]*-->", "", t)
    # grouped parenthetical: (A, 2022<!--ref:a-->; B, 2020<!--ref:b-->)
    t = re.sub(r"\(([^()]*?<!--ref:[^>]+-->[^()]*?)\)",
               lambda m: stash("~\\cite{" + ",".join(re.findall(r"<!--ref:([^>]+)-->", m.group(1))) + "}"), t)
    # single: (Author, 2024)<!--ref:k-->
    t = re.sub(r"\s*\(([^()]*?)\)<!--ref:([^>]+)-->", lambda m: stash("~\\cite{" + m.group(2) + "}"), t)
    assert "<!--ref:" not in t, t[:200]
    t = re.sub(r"`([^`]+)`", lambda m: stash("\\texttt{" + esc(m.group(1)) + "}"), t)
    t = re.sub(r"Fig\. (\d)", lambda m: stash(f"Fig.~\\ref{{fig:{m.group(1)}}}"), t)
    t = re.sub(r"Table (\d)", lambda m: stash(f"Table~\\ref{{tab:{m.group(1)}}}"), t)
    t = re.sub(r"https?://\S+?(?=[.,;)]?(\s|$))", lambda m: stash("\\url{" + m.group(0) + "}"), t)
    for a in ("⁻³", "⁻⁵"):
        t = t.replace(a, stash(UNI[a]))
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\\emph{\1}", t)
    t = re.sub(r'"(.+?)"', r"``\1''", t)
    for a, b in UNI.items():
        t = t.replace(a, b)
    t = re.sub(r"(?<![\w\\{$'-])([kKpn])(?![\w'-])(?=\s*(?:[=<>,.;)]|\$\\|flows|labelled|target| per|\s|$))",
               r"$\1$", t)                       # math variables k, K, p, n
    t = re.sub(r" ([<>]) ", r" $\1$ ", t)
    t = re.sub(r"\$\$", "", t)  # adjacent math pieces
    t = re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], t)
    return t


def table(lines, num, caption):
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines if not re.match(r"^\|[-| ]+\|$", ln)]
    ncol = len(rows[0])
    out = ["\\begin{table*}[t]", "\\centering", "\\small", f"\\caption{{{inline(caption)}}}", f"\\label{{tab:{num}}}",
           "\\begin{adjustbox}{max width=\\linewidth}", "\\begin{tabular}{l" + "r" * (ncol - 1) + "}", "\\toprule",
           " & ".join(inline(c) for c in rows[0]) + " \\\\", "\\midrule"]
    for r in rows[1:]:
        if all(c == "" for c in r[1:]) and r[0].startswith("*"):
            out.append("\\midrule" if len(out) > 9 and not out[-1].endswith("\\midrule") else "")
            out.append(f"\\multicolumn{{{ncol}}}{{l}}{{{inline(r[0])}}} \\\\")
            continue
        if r[0].startswith("**"):
            out.append("\\midrule")
        out.append(" & ".join(inline(c) for c in r) + " \\\\")
    out += ["\\bottomrule", "\\end{tabular}", "\\end{adjustbox}", "\\end{table*}"]
    return "\n".join(x for x in out if x)


def figure(num):
    files, cap = FIGURES[num]
    if len(files) == 1:
        body = f"\\includegraphics[width=\\linewidth]{{figures/{files[0]}}}"
    else:
        body = "\n\\par\\medskip\n".join(  # stacked full-width panels: heatmap labels are unreadable side by side
            f"\\begin{{subfigure}}{{0.92\\linewidth}}\\centering\\includegraphics[width=\\linewidth]{{figures/{f}}}"
            f"\\caption{{{s}}}\\end{{subfigure}}" for f, s in zip(files, ["Shared scaling", "Per-domain scaling"]))
    return (f"\\begin{{figure*}}[t]\n\\centering\n{body}\n\\caption{{{inline(cap)}}}\n\\label{{fig:{num}}}\n"
            f"\\end{{figure*}}")


def convert(md):
    # figure captions
    for n, cap in re.findall(r"- \*\*Fig\. (\d)\.\*\* (.+)", md):
        cap = re.sub(r"\s*\(`results/[^)]*\)\.?$", ".", cap)
        if int(n) == 3:
            cap = cap.replace("Left: per-domain scaling; right: shared scaling.", "(a) Shared scaling; (b) per-domain scaling.")
        FIGURES[int(n)] = (FIGURES[int(n)][0], cap)
    md = md[: md.index("## Figure Captions")] + md[md.index("---\n\n## Data and Code Availability"):]
    md = re.sub(r"<!--protected-hedges:.*?-->", "", md, flags=re.S)
    out, placed = [], set()
    lines = md.split("\n")
    i = 0
    tab_caption = {}
    for m in re.finditer(r"\*\*Table (\d)\.\*\* (.+)", md):
        tab_caption[int(m.group(1))] = m.group(2)
    tab_num = 0
    in_list = None
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("# ") or ln.startswith("**Rijan") or ln.strip() == "---":
            i += 1
            continue
        if ln.startswith("|"):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i]); i += 1
            tab_num += 1
            out.append(table(block, tab_num, tab_caption[tab_num]))
            continue
        if re.match(r"\*\*Table \d\.\*\*", ln):
            i += 1
            continue
        m = re.match(r"^(#{2,3}) (?:[\d.]+ )?(.+)$", ln)
        if m:
            if in_list:
                out.append(f"\\end{{{in_list}}}"); in_list = None
            title = m.group(2)
            star = "*" if not re.match(r"^#{2,3} \d", ln) else ""
            cmd = "section" if m.group(1) == "##" else "subsection"
            out.append(f"\n\\{cmd}{star}{{{inline(title)}}}")
            i += 1
            continue
        lm = re.match(r"^(\d+\.|-) (.+)$", ln)
        if lm:
            env = "enumerate" if lm.group(1)[0].isdigit() else "itemize"
            if in_list != env:
                if in_list:
                    out.append(f"\\end{{{in_list}}}")
                out.append(f"\\begin{{{env}}}"); in_list = env
            out.append("\\item " + inline(lm.group(2)))
            i += 1
            continue
        if in_list and ln.strip() == "" and i + 1 < len(lines) and re.match(r"^(\d+\.|-) ", lines[i + 1]):
            i += 1
            continue
        if in_list and ln.strip() == "":
            out.append(f"\\end{{{in_list}}}"); in_list = None
        out.append(inline(ln) if ln.strip() else "")
        for n in sorted(set(map(int, re.findall(r"Fig\. (\d)", ln))) - placed):
            out.append(figure(n)); placed.add(n)
        i += 1
    if in_list:
        out.append(f"\\end{{{in_list}}}")
    assert placed == set(FIGURES), placed
    return "\n".join(out)


def bib():
    s = (PAPER / "phase5_citations" / "references.bib").read_text()
    s = s.replace("’", "'")
    acc = {"é": "{\\'e}", "É": "{\\'E}", "á": "{\\'a}", "ü": '{\\"u}', "ö": '{\\"o}', "ë": '{\\"e}', "ç": "{\\c{c}}",
           "š": "{\\v{s}}"}
    for a, b in acc.items():
        s = s.replace(a, b)
    s = re.sub(r"(pages = \{\d+)-(\d+\})", r"\1--\2", s)
    s = re.sub(r"^(  (?:title|journal|booktitle|howpublished) = .*)$",
               lambda m: re.sub(r"(?<!\\)([_&%#])", r"\\\1", m.group(1)), s, flags=re.M)  # e.g. TON_IoT
    assert all(ord(c) < 128 for c in s), {c for c in s if ord(c) >= 128}
    return s


def main():
    draft = (PAPER / "phase4_draft" / "draft.md").read_text()
    title = re.search(r"^# (.+)$", draft, re.M).group(1)
    ab = (PAPER / "phase5_abstract" / "abstract.md").read_text()
    abstract = re.search(r"### English Abstract\n\n(.+?)\n\n\*\*Keywords:\*\* (.+?)\n", ab, re.S)
    body = convert(draft)
    tex = rf"""\documentclass[11pt]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{lmodern}}
\usepackage[margin=1in]{{geometry}}
\usepackage{{amsmath,amssymb}}
\usepackage{{graphicx}}
\usepackage{{booktabs}}
\usepackage{{adjustbox}}
\usepackage{{caption,subcaption}}
\usepackage{{microtype}}
\usepackage[hidelinks]{{hyperref}}
\usepackage{{url}}

\title{{{inline(title)}}}
\author{{Rijan Rayamajhi\\ Independent Researcher\\ \texttt{{rayamajhirijan5051@gmail.com}}\\ ORCID: \href{{https://orcid.org/0009-0007-0344-7552}}{{0009-0007-0344-7552}}}}
\date{{}}

\begin{{document}}
\maketitle

\begin{{abstract}}
{inline(abstract.group(1).strip())}
\end{{abstract}}

\noindent\textbf{{Keywords:}} {inline(abstract.group(2).strip())}

{body}

\bibliographystyle{{IEEEtran}}
\bibliography{{references}}

\end{{document}}
"""
    tex = re.sub(r"\n{3,}", "\n\n", tex)
    assert all(ord(c) < 128 or c in "šá" for c in tex), {c for c in tex if ord(c) >= 128}
    (HERE / "main.tex").write_text(tex)
    (HERE / "references.bib").write_text(bib())
    FIG.mkdir(exist_ok=True)
    for files, _ in FIGURES.values():
        for f in files:
            shutil.copy(REPO / "results" / f, FIG / f)
    with zipfile.ZipFile(HERE / "arxiv_upload.zip", "w", zipfile.ZIP_DEFLATED) as z:
        z.write(HERE / "main.tex", "main.tex")
        z.write(HERE / "references.bib", "references.bib")
        for f in sorted(FIG.iterdir()):
            z.write(f, f"figures/{f.name}")
    cites = set(k for g in re.findall(r"\\cite\{([^}]+)\}", tex) for k in g.split(","))
    keys = set(re.findall(r"@\w+\{([^,]+),", bib()))
    print(f"wrote main.tex ({len(tex.split())} tokens), {len(cites)} cited keys, missing in bib: {sorted(cites - keys) or 'none'}")
    print("wrote arxiv_upload.zip:", [i.filename for i in zipfile.ZipFile(HERE / "arxiv_upload.zip").infolist()])


if __name__ == "__main__":
    main()
