"""Regenerate _annotated_bibliography.md from references.json (the verified records).

    python3 paper/phase1_literature/build_bibliography.py
"""
import json
from pathlib import Path

HERE = Path(__file__).parent


def auth(a):
    n = [x.get('family') or x.get('literal') for x in a]
    return n[0] if len(n) == 1 else (f"{n[0]} & {n[1]}" if len(n) == 2 else f"{n[0]} et al.")


refs = json.load(open(HERE / 'references.json'))
out = []
for sec in ['introduction', 'related-work', 'method', 'discussion']:
    out.append(f"\n#### Section: {sec}\n")
    for r in [x for x in refs if x['section'] == sec]:
        ident = f"DOI {r['doi']}" if r.get('doi') else (f"arXiv {r['arxiv_id']}" if r.get('arxiv_id') else r.get('url'))
        loc = ", ".join(str(v) for v in [r.get('venue'), r.get('volume') and f"vol. {r['volume']}",
                                         r.get('issue') and f"no. {r['issue']}", r.get('pages') and f"pp. {r['pages']}"] if v)
        out += [f"##### {auth(r['authors'])} ({r['year']}). {r['title']}. `{r['citation_key']}`",
                f"- **Type**: {r['venue_type']} — {loc} — {ident}",
                f"- **Verified via**: {r['verified_via']}",
                f"- **Summary**: {r['abstract_summary']}",
                f"- **Relevance**: {r['relevance']}"]
        if r['read_scope'] == 'full_text' and r.get('method_weaknesses'):
            out.append("- **Method weaknesses** (read: full text by AI agent; NOT an author reading attestation)")
            out += [f"  - {w}" for w in r['method_weaknesses']]
        else:
            out.append(f"- **Method weaknesses**: not assessed (read scope: {r['read_scope']}; AI agent, not author)")
        if r.get('notes'):
            out.append(f"- **Notes**: {r['notes']}")
        out.append("")
(HERE / '_annotated_bibliography.md').write_text("\n".join(out))
print(len(refs), "annotated")
