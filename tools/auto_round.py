"""헌원검3 번역 반복 작업 도우미 (예약 실행용)
사용 (작업 폴더 루트에서):
  python3 tools/auto_round.py lock      # 잠금 획득. 90분 이내 다른 실행이 있으면 'LOCKED' 출력 후 종료코드 3
  python3 tools/auto_round.py next      # 다음 회차 번호 + 미번역 Scene 100행/2,500자 출력 (zh_Hant | zh_Hans | en)
  python3 tools/auto_round.py apply translation/rounds/roundNN_*.json [review.json]
  python3 tools/auto_round.py finish N1 N2   # 이번 실행에서 한 회차 범위. XLSX 동기화·상태·MOD 빌드·설치·기록·잠금 해제
  python3 tools/auto_round.py unlock
"""
import csv, datetime, hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
TR = ROOT / 'translation'; TSV = TR / 'SWD3_translation_master.tsv'
LOCK = TR / '.auto_round.lock'; STATE = TR / 'lightweight_automation_state.json'
GAME = ROOT.parent; MODS = GAME / 'Mods'
PROGRESS = Path(os.environ.get('PROGRESS_MD', ''))
CTRL = re.compile(r'%[A-Za-z](?:-?\d+)?|~[SD]|\[[^\]]*\]')
cmd = sys.argv[1]
def rows():
    return list(csv.DictReader(open(TSV, encoding='utf-8-sig'), delimiter='\t'))
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
if cmd == 'lock':
    if LOCK.exists() and LOCK.read_text().strip() != 'FREE' and time.time() - LOCK.stat().st_mtime < 90 * 60:
        print('LOCKED', LOCK.read_text()); sys.exit(3)
    LOCK.write_text(datetime.datetime.now().isoformat()); print('LOCK OK')
elif cmd == 'unlock':
    LOCK.write_text('FREE'); print('UNLOCKED')
elif cmd == 'next':
    s = json.load(open(STATE, encoding='utf-8'))
    done = [int(m.group(1)) for m in (re.match(r'round(\d+)_Scene', f.name) for f in (TR / 'rounds').glob('round*_Scene_*.json')) if m]
    print('NEXT_ROUND', max(done + [s['round']]) + 1)
    tot = n = 0
    for r in rows():
        if r['file'] != 'Scene.txt' or r['ko'].strip(): continue
        if n >= 100 or tot + len(r['zh_Hant']) > 2500: break
        tot += len(r['zh_Hant']); n += 1
        print(r['key'], '|', r['zh_Hant'], '|', r['zh_Hans'], '|', r['en'])
    print('COUNT', n, tot)
    if n == 0: print('SCENE_DONE')
elif cmd == 'apply':
    LOCK.touch()
    args = ['python3', str(ROOT / 'tools/apply_round_json.py'), 'Scene.txt', os.path.abspath(sys.argv[2])] + [os.path.abspath(x) for x in sys.argv[3:4]]
    r = subprocess.run(args, cwd=TR, capture_output=True, text=True)
    print(r.stdout, r.stderr); sys.exit(r.returncode)
elif cmd == 'finish':
    a, b = int(sys.argv[2]), int(sys.argv[3])
    print(subprocess.run(['python3', str(ROOT / 'tools/sync_master_xlsx.py')], capture_output=True, text=True, check=True).stdout)
    R = rows(); ko = sum(1 for r in R if r['ko'].strip())
    bad = sum(1 for r in R if r['ko'].strip() and CTRL.findall(r['zh_Hant'] or r['en']) != CTRL.findall(r['ko']))
    assert len(R) == 12186 and len({(r['file'], r['key']) for r in R}) == 12186 and bad == 0
    sc = [r for r in R if r['file'] == 'Scene.txt']
    last = max((i for i, r in enumerate(sc) if r['ko'].strip()), default=0)
    nxt = next((r['key'] for r in sc if not r['ko'].strip()), 'DONE')
    s = json.load(open(STATE, encoding='utf-8'))
    s.update({'round': b, 'last_completed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'file': 'Scene.txt',
              'last_key': sc[last]['key'], 'next_key': nxt, 'total_korean_rows': ko, 'xlsx_sync_due': False,
              'xlsx_last_synced_round': b, 'xlsx_sha256_at_round': sha(TR / 'SWD3_translation_master.xlsx'), 'tsv_sha256_after': sha(TSV)})
    json.dump(s, open(STATE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    out = TR / 'mod_build' / ('ko_full_' + datetime.date.today().strftime('%Y%m%d'))
    r = subprocess.run(['python3', str(ROOT / 'tools/build_ko_ssmod.py'), str(out)], capture_output=True, text=True, check=True)
    assert '"roundtrip": true' in r.stdout
    data = (out / 'swd3_ko.ssmod').read_bytes(); (MODS / 'swd3_ko.ssmod').write_bytes(data)
    assert (MODS / 'swd3_ko.ssmod').read_bytes() == data
    rd = ROOT / '00_읽어보기.md'; t = rd.read_text(encoding='utf-8')
    t = re.sub(r'## 현재 상태 \(.*?\)', '## 현재 상태 (%s)' % datetime.date.today().isoformat(), t)
    t = re.sub(r'- 번역 [\d,]+ / 12,186행\..*', f'- 번역 {ko:,} / 12,186행. 대사(Scene)는 {sc[last]["key"]}까지. 다음: {nxt}부터', t)
    rd.write_text(t, encoding='utf-8')
    line = f'- {datetime.date.today().isoformat()} [헌원검3][자동] round{a}~{b} 반영, ko {ko:,}, 다음 {nxt}. MOD 재빌드·설치'
    with open(ROOT / 'CLAUDE_HANDOFF.md', 'a', encoding='utf-8') as f: f.write('\n' + line + '\n')
    if PROGRESS.is_file():
        with open(PROGRESS, 'a', encoding='utf-8') as f: f.write('\n' + line + '\n')
    LOCK.write_text('FREE')
    print('FINISH OK', line)
