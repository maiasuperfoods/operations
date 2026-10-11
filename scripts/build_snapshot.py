#!/usr/bin/env python3
"""Turn an export of the page database into public/data/db.json.

The export is a folder with one sub-folder per collection and one JSON file per document:
  <export>/weeks/2026-09-28.json, <export>/items/<id>.json, <export>/plan/model.json, ...

usage: python3 scripts/build_snapshot.py <export folder> [YYYY-MM-DD]

The snapshot holds business data. Keep it out of a public repository (see .gitignore).
"""
import sys, os, json, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) < 2: raise SystemExit(__doc__)
exp = sys.argv[1]; day = sys.argv[2] if len(sys.argv) > 2 else datetime.date.today().isoformat()
cols = {}
for c in sorted(os.listdir(exp)):
    d = os.path.join(exp, c)
    if not os.path.isdir(d): continue
    docs = {f[:-5]: json.load(open(os.path.join(d, f), encoding='utf8')) for f in sorted(os.listdir(d)) if f.endswith('.json')}
    if docs: cols[c] = docs
out = os.path.join(ROOT, 'public', 'data', 'db.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump({'exportedAt': day, 'collections': cols}, open(out, 'w', encoding='utf8'), separators=(',', ':'))
print(out, os.path.getsize(out), 'bytes;', ', '.join('%s %d' % (k, len(v)) for k, v in cols.items()))
