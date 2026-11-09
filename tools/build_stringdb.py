"""StringDB 한국어화: en 원본 구조(BOM·CRLF·줄 순서) 유지, 값만 교체 → 게임 en\\StringDB.txt
사용: python3 tools/build_stringdb.py [--install]"""
import json, re, sys, shutil, datetime, csv
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; S = ROOT / 'translation' / 'stringdb'
ko = {}
for p in sorted(S.glob('ko_part*.json')): ko.update(json.load(open(p, encoding='utf-8')))
raw = (S / 'en_StringDB.orig.txt').read_bytes(); nl = b'\r\n' if b'\r\n' in raw else b'\n'
lines = raw.split(nl); n = 0
for i, l in enumerate(lines):
    bom = b''
    if l.startswith(b'\xef\xbb\xbf'): bom, l = l[:3], l[3:]
    if not l or l.startswith(b';') or b' ' not in l: continue
    k = l.split(b' ', 1)[0].decode()
    if k in ko: lines[i] = bom + k.encode() + b' ' + ko[k].encode('utf-8'); n += 1
# 편의 모드(KoQoL) 표시 문자열 (lua 안 한글 리터럴은 ? 로 깨지므로 StringDB로 전달)
QOL = [('9901', '필드 전투'), ('9902', '자동 전투'), ('9903', '전투 돈'), ('9904', '전투 속도'), ('9905', '켬'), ('9906', '끔'), ('9907', '배'), ('9908', '보통'), ('9909', '편의 설정'), ('9910', '경험치')]
while lines and lines[-1] == b'': lines.pop()
lines += [(k + ' ' + v).encode('utf-8') for k, v in QOL] + [b'']
out = nl.join(lines); (S / 'StringDB.ko.txt').write_bytes(out)
rows = list(csv.DictReader(open(S / 'StringDB_master.tsv', encoding='utf-8'), delimiter='\t'))
with open(S / 'StringDB_master.tsv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter='\t', lineterminator='\n'); w.writeheader()
    for r in rows: r['ko'] = ko.get(r['key'], ''); w.writerow(r)
print('replaced', n, 'lines', len(lines), len(raw.split(nl)), '+KoQoL', len(QOL))
if '--install' in sys.argv:
    game = ROOT.parent / 'en' / 'StringDB.txt'
    bk = ROOT / 'backups' / ('StringDB.en.before_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.txt')
    shutil.copyfile(game, bk); game.write_bytes(out); assert game.read_bytes() == out
    print('installed, backup', bk.name)
