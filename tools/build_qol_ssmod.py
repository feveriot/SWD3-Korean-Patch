"""편의 모드(swd3_ko_qol.ssmod): convenience/src 의 수정 lua로 같은 이름 원본 스크립트를 덮어쓴다.
사용: python3 tools/build_qol_ssmod.py <출력폴더>"""
import struct, subprocess, sys, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'convenience' / 'src'
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
FILES = [('KoQoL.lua', 'KoQoL convenience'), ('ItemPicData.lua', 'KoQoL appended')]
def zblob(b):
    c = subprocess.run(['zstd', '-19', '-q', '-c'], input=b, capture_output=True, check=True).stdout
    return b'Z' + struct.pack('<II', len(c), len(b)) + c
def lp32(s): b = s.encode('utf-8'); return struct.pack('<I', len(b)) + b
def lp16(b): return struct.pack('<H', len(b)) + b
t = datetime.date.today(); ext_name = 'swd3_ko_qol.ext'
info = 'Korean patch QoL: auto battle default, F9 field battle on/off, battle money x2.'
ext = '﻿MODName SWD3 Korean QoL\r\nMODAuthor local\r\nMODDate %d,%d,%d\r\nMODVersion 2,1\r\nMODinfo %s%%Q\r\nMODGameVersion 2,3\r\nMODpicture\r\nMODsystemMOD 1\r\nMODbundleSave 1\r\n;Datas TYPE ,LangID ,FileName ,Comment\r\n' % (t.year, t.month, t.day, info)
ext += ''.join('DAT 2,0,%s,%s\r\n' % (f, d) for f, d in FILES)
ext = ext.encode('utf-8'); (OUT / ext_name).write_bytes(ext)
hdr = bytearray(0x90); hdr[0:4] = b'SMOD'; struct.pack_into('<I', hdr, 4, 4); struct.pack_into('<I', hdr, 8, 0x90)
meta = lp32('SWD3 Korean QoL') + lp32('local') + lp32(info)
meta += struct.pack('<IIIIHBB', 1, 1, 2, 3, t.year, t.month, t.day) + b'\0' * 12 + bytes([1, 1]) + lp32(ext_name) + zblob(ext)
body = bytes(hdr) + meta; ents = []
for f, d in FILES:
    b = (SRC / f).read_bytes(); ents.append((f.encode(), len(body), len(b), d.encode())); body += zblob(b)
idx = struct.pack('<I', len(ents))
for n, o, s, d in ents:
    idx += struct.pack('<I', 0) + lp16(n) + bytes([2]) + struct.pack('<HHQI', 0, 1, o, s) + bytes([0]) + lp16(n) + lp16(d)
out = bytearray(body + idx); struct.pack_into('<QQ', out, 0x20, len(body), len(idx))
(OUT / 'swd3_ko_qol.ssmod').write_bytes(out)
for n, o, s, d in ents:
    z, cs, us = struct.unpack_from('<BII', out, o); back = subprocess.run(['zstd', '-dc'], input=bytes(out[o+9:o+9+cs]), capture_output=True).stdout
    assert back == (SRC / n.decode()).read_bytes()
print('ok', len(out))
