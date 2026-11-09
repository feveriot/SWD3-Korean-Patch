"""회차 JSON({key: ko})을 정본 TSV에 반영. 빈 ko만 채움, 제어코드 검사, 원자적 저장.
사용: python3 tools/apply_round_json.py <file> <round.json> [review.json]"""
import csv, hashlib, json, os, re, sys
from pathlib import Path
T = Path(__file__).resolve().parent.parent / 'translation' / 'SWD3_translation_master.tsv'
fn, rj = sys.argv[1], json.load(open(sys.argv[2], encoding='utf-8'))
review = json.load(open(sys.argv[3], encoding='utf-8')) if len(sys.argv) > 3 else {}
CTRL = re.compile(r'%[A-Za-z](?:-?\d+)?|~[SD]|\[[^\]]*\]')
raw = T.read_bytes(); before = hashlib.sha256(raw).hexdigest()
rd = csv.DictReader(raw.decode('utf-8-sig').splitlines(), delimiter='\t'); fields = rd.fieldnames; rows = list(rd)
old_ko = {(r['file'], r['key']): r['ko'] for r in rows}
idx = {(r['file'], r['key']): r for r in rows}
for k, v in rj.items():
    r = idx[(fn, k)]
    assert not r['ko'].strip(), ('already', k)
    assert CTRL.findall(r['zh_Hant']) == CTRL.findall(v), ('ctrl', k, CTRL.findall(r['zh_Hant']), CTRL.findall(v))
    assert '\t' not in v and '\n' not in v
    r['ko'] = v
    if k in review: r['status'] = '검수필요'; r['note'] = review[k]
    else: r['status'] = '자동번역'
assert len(rows) == 12186 and len(idx) == 12186
for key, v in old_ko.items():
    if v.strip(): assert idx[key]['ko'] == v
tmp = T.with_suffix('.tsv.tmp')
with open(tmp, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\r\n' if b'\r\n' in raw[:5000] else '\n'); w.writeheader(); w.writerows(rows)
os.replace(tmp, T)
after = hashlib.sha256(T.read_bytes()).hexdigest()
n = sum(1 for r in rows if r['ko'].strip())
print(json.dumps({'applied': len(rj), 'korean_rows': n, 'chars': sum(len(idx[(fn,k)]['zh_Hant']) for k in rj), 'before': before, 'after': after}, ensure_ascii=False))
