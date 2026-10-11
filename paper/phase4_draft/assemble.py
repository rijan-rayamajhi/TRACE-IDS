"""Assemble draft.md from section files and report word counts (markers and tables excluded)."""
import re
parts = ['s1_introduction.md', 's2_related.md', 's3_protocol.md', 's4_results_help.md', 's5_results_why.md', 's6_8_discussion_end.md']
txt = {p: open(p).read() for p in parts}
body = txt['s6_8_discussion_end.md']
i = body.index('---\n\n## Data and Code Availability')
txt['s6_8_discussion_end.md'] = body[:i] + open('figures.md').read() + '\n' + body[i:]
draft = '\n\n'.join(txt[p].strip() for p in parts) + '\n'
open('draft.md', 'w').write(draft)
target = {'1': 900, '2': 1300, '3': 1100, '4': 1300, '5': 1000, '6': 900, '7': 300, '8': 200}
clean = re.sub(r'<!--.*?-->', '', draft, flags=re.S)
tot = 0
for s in re.split(r'\n(?=## )', clean):
    m = re.match(r'## (\d)', s.strip())
    if not m:
        continue
    n = len(re.sub(r'^\|.*\|$', '', s, flags=re.M).split()); tot += n
    t = target[m.group(1)]
    print(f"{s.strip().splitlines()[0][:48]:<50}{n:>6} / {t:<5} {100*(n-t)/t:+.0f}%{'  <-- outside ±15%' if abs(n-t) > .15*t else ''}")
print(f"{'BODY TOTAL':<50}{tot:>6} / 7000  {100*(tot-7000)/7000:+.0f}%{'  <-- outside ±10%' if abs(tot-7000) > 700 else ''}")
