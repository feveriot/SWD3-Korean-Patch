"""tsw_index.ssmod에서 언어별 UI 이미지 추출. 사용: python3 extract_tsw_lang.py <tsw_index.ssmod> <outdir>"""
import struct, subprocess, os, json, sys
fn, out = sys.argv[1], sys.argv[2]
LANGS = tuple(int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else '0,2').split(','))
f = open(fn, 'rb'); h = f.read(0x40)
to, ts = struct.unpack_from('<QQ', h, 0x30); f.seek(to); d = f.read(ts)
p = 0; n = struct.unpack_from('<I', d, p)[0]; p += 4; G = []
for _ in range(n):
    gid, a = struct.unpack_from('<IH', d, p); p += 6; t = d[p]; p += 1; lang, cnt = struct.unpack_from('<HH', d, p); p += 4; es = []
    for _ in range(cnt):
        off, sz = struct.unpack_from('<QI', d, p); p += 12; st = d[p]; p += 1; l = struct.unpack_from('<H', d, p)[0]; p += 2; nm = d[p:p+l].decode('utf-8', 'replace'); p += l; es.append((off, sz, st, nm))
    l = struct.unpack_from('<H', d, p)[0]; p += 2; desc = d[p:p+l].decode('utf-8', 'replace'); p += l
    G.append((gid, a, t, lang, es, desc))
ids2 = {g[0] for g in G if g[3] == 2}
def get(off):
    f.seek(off); hd = f.read(9)
    if hd[0] == 0x5a:
        cs, us = struct.unpack_from('<II', hd, 1); f.seek(off + 9)
        return subprocess.run(['zstd', '-dc'], input=f.read(cs), capture_output=True).stdout, hd[0]
    cs = struct.unpack_from('<I', hd, 1)[0]; f.seek(off + 5); return f.read(cs), hd[0]
meta = []
for gid, a, t, lang, es, desc in G:
    if gid not in ids2 or lang not in LANGS: continue
    sub = os.path.join(out, 'en' if lang == 2 else 'cht'); os.makedirs(sub, exist_ok=True)
    for sn, (off, sz, st, nm) in enumerate(es):
        data, flag = get(off); fn2 = f'{gid}_{sn:02d}__{nm}'
        open(os.path.join(sub, fn2), 'wb').write(data)
        meta.append({'lang': lang, 'id': gid, 'a': a, 'type': t, 'sn': sn, 'file': nm, 'out': fn2, 'desc': desc, 'flag': flag, 'st': st, 'png': data[:4] == b'\x89PNG', 'bytes': len(data)})
json.dump(meta, open(os.path.join(out, 'images_%s.json' % '_'.join(map(str, LANGS))), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('done', len(meta))
