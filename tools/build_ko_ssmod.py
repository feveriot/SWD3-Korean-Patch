"""정본 TSV의 한국어를 영어 슬롯(LangID 2) 4개 파일에 반영하고 .ssmod를 직접 만든다.
- 원본 영어 파일의 바이트 구조(BOM, CRLF, 끝 줄바꿈)를 그대로 유지하고 값만 교체
- .ssmod 구조: 실기 성공한 v4(SS2Dtool 출력+주입)와 동일 배치
사용: python3 tools/build_ko_ssmod.py <출력폴더> [--tsw]  (--tsw: translation/images/ko 의 한국어 UI 이미지를 LangID 2 TSW로 포함)
"""
import csv, hashlib, json, re, struct, subprocess, sys, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
TR = ROOT / 'translation'
SRC = TR / 'mod_probe' / 'out_data_2'          # 공식 영어 원본(script_index.ssmod에서 추출)
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
WITH_TSW = '--tsw' in sys.argv
FILES = [('name.txt', '名詞'), ('BattleScriptString.txt', ''), ('ItemString.txt', ''), ('Scene.txt', '劇情腳本文字')]
CTRL = re.compile(r'%[A-Za-z](?:-?\d+)?|~[SD]|\[[^\]]*\]')

rows = list(csv.DictReader(open(TR / 'SWD3_translation_master.tsv', encoding='utf-8-sig'), delimiter='\t'))
ko = {}
for r in rows:
    if r['ko'].strip():
        assert CTRL.findall(r['zh_Hant'] or r['en']) == CTRL.findall(r['ko']), (r['file'], r['key'])
        assert '\t' not in r['ko'] and '\n' not in r['ko'] and '\r' not in r['ko'], r['key']
        ko[(r['file'], r['key'])] = r['ko']

report = {}
datas = []
for fn, desc in FILES:
    raw = (SRC / fn).read_bytes()
    lines = raw.split(b'\r\n')
    n = 0
    for i, ln in enumerate(lines):
        bom = b''
        if i == 0 and ln.startswith(b'\xef\xbb\xbf'):
            bom, ln = b'\xef\xbb\xbf', ln[3:]
        if not ln or ln.startswith(b';') or b' ' not in ln:
            continue
        k = ln.split(b' ', 1)[0].decode('utf-8')
        v = ko.get((fn, k))
        if v is not None:
            lines[i] = bom + k.encode() + b' ' + v.encode('utf-8'); n += 1
    exp = sum(1 for (f, _) in ko if f == fn)
    assert n == exp, (fn, n, exp)
    new = b'\r\n'.join(lines)
    if fn == 'name.txt':  # 편의 모드(KoQoL) 표시 문자열 — lua 안 한글 리터럴은 깨지므로 StringDB로 전달
        QOL = [('KoQoL_Field', '필드 전투'), ('KoQoL_Auto', '자동 전투'), ('KoQoL_Money', '전투 돈'), ('KoQoL_Exp', '경험치'),
               ('KoQoL_Speed', '전투 속도'), ('KoQoL_Move', '이동 속도'), ('KoQoL_On', '켬'), ('KoQoL_Off', '끔'), ('KoQoL_X', '배'), ('KoQoL_Normal', '보통')]
        tail = new.endswith(b'\r\n')
        new = new.rstrip(b'\r\n') + b'\r\n' + b'\r\n'.join((k + ' ' + v).encode('utf-8') for k, v in QOL) + (b'\r\n' if tail else b'')
    assert len(new.split(b'\r\n')) >= len(raw.split(b'\r\n'))
    (OUT / fn).write_bytes(new)
    datas.append((fn, desc, new))
    report[fn] = {'korean_rows': n, 'bytes': len(new), 'sha256': hashlib.sha256(new).hexdigest()}

def zblob(b):
    c = subprocess.run(['zstd', '-19', '-q', '-c'], input=b, capture_output=True, check=True).stdout
    return b'Z' + struct.pack('<II', len(c), len(b)) + c
def lp32(s): b = s.encode('utf-8'); return struct.pack('<I', len(b)) + b
def lp16(b): return struct.pack('<H', len(b)) + b

# ── TSW(이미지) ──
tsw_groups = []   # (gid, a, type, desc, [(name, blob_bytes, rawsize)])
if WITH_TSW:
    IMG = TR / 'images'; KO = IMG / 'ko'
    meta2 = json.load(open(IMG / 'x' / 'images_2.json', encoding='utf-8'))
    tf = open(ROOT.parent / 'tsw_index.ssmod', 'rb'); to, ts = struct.unpack_from('<QQ', tf.read(0x40), 0x30); tf.seek(to); td = tf.read(ts)
    q = 4; orig = {}
    for _ in range(struct.unpack_from('<I', td, 0)[0]):
        gid, a, t, lang, cnt = struct.unpack_from('<IHBHH', td, q); q += 11; es = []
        for _ in range(cnt):
            off, sz, st = struct.unpack_from('<QIB', td, q); q += 13; l = struct.unpack_from('<H', td, q)[0]; nm = td[q+2:q+2+l]; q += 2 + l; es.append((off, sz, st, nm))
        l = struct.unpack_from('<H', td, q)[0]; desc = td[q+2:q+2+l]; q += 2 + l
        if lang == 2: orig[gid] = (a, t, es, desc)
    gids = sorted({m['id'] for m in meta2 if (KO / m['out']).exists()})
    for gid in gids:
        a, t, es, desc = orig[gid]; ents = []
        for sn, (off, sz, st, nm) in enumerate(es):
            m = next((m for m in meta2 if m['id'] == gid and m['sn'] == sn), None)
            kp = KO / m['out'] if m else KO / '_none_'
            if kp.exists():
                raw = kp.read_bytes(); assert raw[:4] == b'\x89PNG'
                blob = b'\x20' + struct.pack('<I', len(raw)) + raw; rs = len(raw)
            elif off == 0 and sz == 0:
                blob = b''; rs = 0   # 빈 슬롯
            else:
                tf.seek(off); hd = tf.read(9)
                ln = (9 + struct.unpack_from('<I', hd, 1)[0]) if hd[0] == 0x5a else (5 + struct.unpack_from('<I', hd, 1)[0])
                tf.seek(off); blob = tf.read(ln); rs = sz
            ents.append((nm, blob, rs))
        tsw_groups.append((gid, a, t, desc, ents))
    report['tsw'] = {'groups': len(tsw_groups), 'entries': sum(len(g[4]) for g in tsw_groups), 'korean_png': sum(1 for m in meta2 if (KO / m['out']).exists())}

today = datetime.date.today()
ext_name = 'swd3_ko.ext'
ext = '﻿MODName SWD3 Korean\r\nMODAuthor local\r\nMODDate %d,%d,%d\r\nMODVersion 0,3\r\nMODinfo Korean localization (English slot).%%Q\r\nMODGameVersion 2,3\r\nMODpicture\r\nMODsystemMOD 0\r\nMODbundleSave 1\r\n;Datas TYPE ,LangID ,FileName ,Comment\r\n' % (today.year, today.month, today.day)
ext += ''.join('DAT 0,2,%s,%s\r\n' % (fn, d) for fn, d, _ in datas)
if tsw_groups:
    ext += '; TSW ID ,SN ,TYPE , LangID, FileName ,Comment\r\n'
    for gid, a, t, desc, ents in tsw_groups:
        for sn, (nm, _, _) in enumerate(ents):
            ext += 'TSW %d,%d,%d,2,%s,%s\r\n' % (gid, sn, t, nm.decode('utf-8'), desc.decode('utf-8'))
ext = ext.encode('utf-8')
(OUT / ext_name).write_bytes(ext)

hdr = bytearray(0x90)
hdr[0:4] = b'SMOD'; struct.pack_into('<I', hdr, 4, 4); struct.pack_into('<I', hdr, 8, 0x90)
meta = lp32('SWD3 Korean') + lp32('local') + lp32('Korean localization (English slot).')
meta += struct.pack('<IIIIHBB', 0, 3, 2, 3, today.year, today.month, today.day) + b'\0' * 12
meta += bytes([0, 1]) + lp32(ext_name) + zblob(ext)
body = bytes(hdr) + meta
entries = []
for fn, d, b in datas:
    entries.append((fn.encode(), len(body), len(b), d.encode('utf-8')))
    body += zblob(b)
idx = struct.pack('<I', len(entries))
for name, off, sz, d in entries:
    idx += struct.pack('<I', 0) + lp16(name) + bytes([0]) + struct.pack('<HHQI', 2, 1, off, sz) + bytes([0]) + lp16(name) + lp16(d)
tsw_tab = b''
if tsw_groups:
    tsw_tab = struct.pack('<I', len(tsw_groups)); placed = []
    for gid, a, t, desc, ents in tsw_groups:
        offs = []
        for nm, blob, rs in ents: offs.append(len(body) if blob else 0); body += blob
        placed.append(offs)
    for (gid, a, t, desc, ents), offs in zip(tsw_groups, placed):
        tsw_tab += struct.pack('<IHBHH', gid, a, t, 2, len(ents))
        for (nm, blob, rs), o in zip(ents, offs): tsw_tab += struct.pack('<QIB', o, rs, 0) + lp16(nm)
        tsw_tab += lp16(desc)
idx_off = len(body)
out = bytearray(body + idx + tsw_tab)
struct.pack_into('<QQ', out, 0x20, idx_off, len(idx))
if tsw_tab: struct.pack_into('<QQ', out, 0x30, idx_off + len(idx), len(tsw_tab))
ss = OUT / 'swd3_ko.ssmod'; ss.write_bytes(out)

# 재검증: 다시 읽어 모든 엔트리 왕복
d = bytes(out); io, isz = struct.unpack_from('<QQ', d, 0x20); assert io + isz + len(tsw_tab) == len(d)
for name, off, sz, _ in entries:
    z, cs, us = struct.unpack_from('<BII', d, off); assert z == 0x5a and us == sz
    back = subprocess.run(['zstd', '-dc'], input=d[off+9:off+9+cs], capture_output=True).stdout
    assert back == (OUT / name.decode()).read_bytes(), name
report['ssmod'] = {'bytes': len(d), 'sha256': hashlib.sha256(d).hexdigest(), 'roundtrip': True}
print(json.dumps(report, ensure_ascii=False, indent=1))
