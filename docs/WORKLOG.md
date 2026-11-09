# 헌원검 3 스팀판 한국어화 — Claude 인계 문서

작성 기준일: 2026-10-13 (Asia/Seoul)

이 문서는 `Q:\SteamLibrary\steamapps\common\SWD3\SWD3_Korean_Localization` 안의 자료만으로 다음 작업자가 분석과 작업을 이어갈 수 있게 정리한 인계서다. 실제 Steam 설치 폴더는 분석 대상으로만 취급하고, 명시적인 시험 적용 요청 전에는 수정하지 않는다.

## 1. 목표와 확정된 방향

- 대상 게임: Steam판 『헌원검 3: 구름과 산의 저편』
- 실제 설치 경로: `Q:\SteamLibrary\steamapps\common\SWD3`
- 한국어화 작업 경로: `Q:\SteamLibrary\steamapps\common\SWD3\SWD3_Korean_Localization`
- 번역 기준 원문: `translation\source\zh-Hant`
- 교차검수 언어: `zh-Hans`, `en`, `ja`
- 중국어 원문을 우선해 번역하며, 영문판은 문맥 확인과 게임 적용용 언어 슬롯으로만 사용한다.
- 원본 덮어쓰기보다 MOD 방식을 우선한다.
- 화면 시험은 기본 메뉴와 환경설정부터 시작한다. 즉시 확인할 수 있고 되돌리기 쉬운 문자열을 먼저 사용한다.

## 2. 현재 확인된 결과

### 한국어 표시 능력

- 기본 메뉴/환경설정 문자열을 이용한 과거 시험에서 한국어 글리프 출력에 성공했다.
- `효과음` 등 한국어가 실제 화면에 표시되었고 글자 자체는 출력 가능했다.
- 다만 기본 폰트는 한국어 가독성에 맞지 않아 향후 폰트 교체 또는 조정이 필요하다.
- 긴 한국어 문자열은 기존 UI 너비 때문에 겹칠 수 있다. 예: `매우 빠르게`와 `구름과 산의 저편`이 겹쳤다. 번역 축약 또는 UI 위치/너비 조정이 필요하다.

### 현재 게임 적용 상태

- 현재 게임은 영어로 정상 실행되는 상태다.
- 완성 번역을 실제 게임에 적용한 상태가 아니다.
- 최근 만든 시험 MOD를 활성화하면 게임이 시작 직후 종료되었다.
- 이후 `modlist.txt`를 백업본으로 복구해 게임을 정상 상태로 돌렸다.
- 따라서 현재 기준의 성공 판정은 “한국어 글리프 출력 가능”까지만 해당한다. 전체 번역 MOD 적용 성공으로 해석하면 안 된다.

## 3. 번역 장부의 현재 상태

정본은 아래 두 파일 한 벌이다. 번호가 붙은 별도 장부를 만들지 않는다.

- `translation\SWD3_translation_master.tsv`
- `translation\SWD3_translation_master.xlsx`

2026-10-13 확인 수치:

- 전체 행: 12,186
- 한국어 입력 행: 4,236
- `(file, key)` 중복: 0
- 제어코드 불일치: 0
- `검수필요`: 419
- `보류`: 1

파일별 진행 상황:

| 파일 | 한국어 입력 | 상태 |
|---|---:|---|
| `name.txt` | 857 | 완료 |
| `BattleScriptString.txt` | 121 | 완료 |
| `ItemString.txt` | 2,742 | 완료 |
| `Scene.txt` | 516 | 진행 중 |

다음 미번역 위치:

- 파일: `Scene.txt`
- 키: `ESS507`
- 번체 원문: `被妮可耽誤了不少時間，我得趕快去%C2修道院%C4找%C2航海圖%C4才行。`
- 그 다음 키: `ESS508`, `ESS509`, `ESS510`, `ESS511` 순서

현재 TSV SHA-256:

`2BFD2560BAC72E1122C0A001B5D51AD26A1767D72C8DF7CE3B40E2E51AB60330`

현재 XLSX SHA-256:

`21CFABF3926DF6B4AF60AD6DADC010DEE0740D02258A7B8ECDA916BD1F74ADEE`

## 4. 번역 작업 규칙

1. `translation\source\zh-Hant`를 기준 원문으로 삼는다.
2. `zh-Hans`, `en`, `ja`는 뜻과 고유명사를 교차 확인할 때만 사용한다.
3. 기존 `ko` 값은 절대 덮어쓰지 않는다.
4. 한 회차는 최대 100행 또는 번체 원문 합계 2,500자 중 먼저 도달하는 지점에서 끝낸다.
5. 현재는 `ItemString.txt`가 끝났으므로 `Scene.txt`의 다음 미번역 항목부터 진행한다.
6. 고유명사, 역사 인명, 언어별 의미 불일치가 확실하지 않으면 `status=검수필요`로 두고 `note`에 근거를 남긴다.
7. 대사 제어코드는 종류, 개수, 순서를 그대로 보존한다.
8. 사용 중인 제어코드 검사식은 `%[A-Za-z](?:-?\d+)?|~[SD]`의 대괄호 표현을 포함하는 기존 검증 도구를 기준으로 한다. 실제 구현은 `tools\validate_lightweight_round.py`를 확인한다.
9. 매 회차마다 다음을 검사한다.
   - 전체 행 수 유지
   - `(file, key)` 중복 0
   - 한국어 행 수의 예상 증가
   - 제어코드 종류·개수·순서 일치
   - 기존 번역 보존
10. TSV는 매 회차 저장한다. XLSX는 3회 성공마다 동기화하되, 종료 전에는 TSV와 XLSX 수치가 일치하는지 다시 확인한다.

현재 진행 상태 파일:

- `translation\lightweight_automation_state.json`
- 현재 기록: round 28, `Scene.txt`의 `ESS393`~`ESS506`에서 93행/2,469자 처리
- `xlsx_sync_due=false`, `xlsx_last_synced_round=27`

## 5. 폴더와 핵심 자료

### 원문과 정본

- `translation\source\zh-Hant\`
- `translation\source\zh-Hans\`
- `translation\source\en\`
- `translation\source\ja\`
- 각 언어 폴더에는 `name.txt`, `BattleScriptString.txt`, `ItemString.txt`, `Scene.txt`가 있다.
- `translation\SWD3_translation_master.tsv`
- `translation\SWD3_translation_master.xlsx`

### MOD 분석 자료

- `translation\mod_source\data_2\`
  - 한국어 시험용으로 생성한 문자열 파일들
- `translation\mod_source\swd3_ko_test_index.ext`
  - 직접 활성화했을 때 게임이 종료된 실패 시험물
- `translation\mod_source\modlist.test.txt`
- `translation\mod_probe\script_index.ssmod`
  - 기존 공식/샘플 MOD 분석용 복사본
- `translation\mod_probe\out_data*\`
  - `script_index.ssmod`를 여러 방식으로 풀어 확인한 결과와 Lua 자료
- `SteamMods.txt`
- `TRANSLATION_PLAN.md`

### 백업

- `backups\apply_test_20261013\`
  - 적용 시험 전 파일과 복구용 자료
- `backups\apply_test_20261013\modlist.original.txt`
- `backups\apply_test_20261013\quarantined_from_game\`
  - 게임 폴더에서 비활성화해 옮긴 시험 파일
- `backups\render_test_original\`
  - 최초 한글 표시 시험 전 원본

### 도구

- `tools\build_translation_master.mjs`
- `tools\sync_master_xlsx.mjs`
- `tools\validate_lightweight_round.py`
- `tools\apply_lightweight_round.py`
- `tools\build_test_mod_source.py`
- `tools\extract_swd3_raw_entry.py`
- `tools\list_smod_index.py`
- `tools\scan_process_strings.py`

`tools` 폴더에는 `apply_lightweight_round2.py`부터 `round28.py`까지 과거 회차별 스크립트가 남아 있다. 이것들을 순서대로 재실행하지 말고, 정본 TSV와 상태 JSON을 먼저 확인한 뒤 필요한 최신 로직만 사용하거나 통합한다.

## 6. 공식 MOD 도구에서 확인된 내용

실제 설치 폴더의 공식 도구:

`Q:\SteamLibrary\steamapps\common\SWD3\Tools\SS2Dtool.exe`

도움말을 CP950으로 읽어 확인한 기능:

- `p`: ssmod 패킹
- `x`: ssmod 언패킹
- `-i[path]`: 입력 경로
- `-o[path]`: 출력 경로
- `-I[file]`: 입력 파일
- `-O[file]`: 출력 파일

다음 적용 시험에서는 임의 `.ext` 직접 로딩을 반복하지 말고, 기존 `script_index.ssmod`의 구조와 인덱스 규칙을 분석한 후 공식 `SS2Dtool.exe`로 정상적인 `.ssmod` 패키지를 만들어야 한다.

현재 정상 복구된 `modlist.txt`의 핵심 내용은 아래와 같다.

```text
;
;  SW0=Off 1=On -1 Does not exist, MODFileNamemodFile name
1 tsw_2x.ssmod
```

## 7. 실패한 접근과 반복 금지 사항

- `swd3_ko_test_index.ext`를 `modlist.txt`에 직접 추가해 활성화하는 방식은 게임을 즉시 종료시켰다.
- 구조가 검증되지 않은 `.ext` 또는 `.ssmod`를 실제 게임 폴더에 바로 넣어 시험하지 않는다.
- 영어로 게임이 실행되었다는 사실만으로 한국어 적용 성공이라고 판정하지 않는다.
- TSV/XLSX의 한국어 입력 수가 늘었다는 사실도 게임 적용 성공을 뜻하지 않는다.
- 설치 폴더의 원본 파일을 백업 없이 덮어쓰지 않는다.
- 회차별 스크립트 전부를 다시 돌리거나 이미 번역된 `ko`를 재번역하지 않는다.
- 번역 자동화를 다시 켜기 전에 중복 실행과 파일 잠금을 막는 단일 실행 방식부터 마련한다.

## 8. 자동화 상태와 문제

- 기존 자동화 이름: `헌원검3 경량 번역 계속`
- 자동화 ID: 3
- 주기: 30분
- 현재 상태: `PAUSED`
- 반복 실행 중 `stream disconnected before completion`과 원격 compact 오류가 계속 발생했다.
- 긴 대화 문맥과 한 번에 많은 번역을 처리하는 방식이 토큰과 연결 안정성 면에서 비효율적이었다.
- 이후에는 Claude 쪽에서 작은 입력 묶음과 짧은 JSON 결과를 사용하고, 파일 적용·검증은 로컬에서 수행하는 구조가 적합하다.

권장 저비용 흐름:

1. 정본 TSV에서 `ko`가 비어 있는 다음 행만 최대 100행/2,500자로 추출한다.
2. Claude에는 해당 행의 `file`, `key`, `zh-Hant`, 필요한 교차검수 텍스트와 최소 용어집만 전달한다.
3. Claude는 `{key: ko}` 또는 `{file, key, ko, status, note}` 형태의 짧은 JSON만 반환한다.
4. 로컬 도구가 정본 TSV에 안전하게 반영한다.
5. 로컬 검증을 통과한 뒤 상태 JSON과 XLSX를 갱신한다.
6. 실패 시 저장된 정본을 먼저 검사하고, 이미 반영된 행은 다시 요청하지 않는다.

## 9. 안전한 다음 작업 순서

### A. 번역을 계속할 경우

1. `translation\SWD3_translation_master.tsv`와 `lightweight_automation_state.json`을 읽는다.
2. TSV의 해시와 위 기록을 비교해 외부 변경 여부를 확인한다.
3. `Scene.txt / ESS507`부터 미번역 행을 추출한다.
4. 최대 100행 또는 2,500자만 번역한다.
5. 기존 `ko` 보존과 제어코드 검사를 수행한다.
6. TSV를 원자적으로 저장하고 재검증한다.
7. 필요할 때만 XLSX를 동기화한다.

### B. 실제 게임 적용을 연구할 경우

1. `translation\mod_probe`의 공식 샘플 구조부터 분석한다.
2. 공식 `SS2Dtool.exe`의 패킹 형식과 요구 인덱스/경로를 확정한다.
3. 메뉴/환경설정의 1~3개 즉시 보이는 문자열만 넣은 최소 MOD를 작업 폴더 안에 만든다.
4. 패키지 내부 파일 목록, 경로, 인코딩, 제어코드, 해시를 정적으로 검증한다.
5. 시험 적용 전 실제 설치 폴더의 대상 파일과 `modlist.txt`를 새 시각의 백업 폴더에 복사한다.
6. 사용자가 명시적으로 시험 적용을 요청한 경우에만 MOD를 설치하고 활성화한다.
7. 게임 시작, 메뉴 한국어 표시, 환경설정 진입, 종료 후 재실행을 화면으로 확인한다.
8. 문제가 생기면 즉시 백업본으로 복구하고 실패 파일은 프로젝트의 격리 폴더로 옮긴다.

## 10. 성공 판정 기준

번역 장부 성공:

- 행 수와 키가 유지됨
- 제어코드 불일치 0
- 기존 번역 손실 0
- TSV와 XLSX 동기화 확인

MOD 패키지 성공:

- 공식 도구로 정상 패킹됨
- 공식/샘플 MOD와 일관된 내부 구조를 가짐
- 설치 전 정적 검사를 통과함

실제 한국어 적용 성공:

- 게임이 종료되지 않고 실행됨
- 기본 메뉴 또는 환경설정에서 의도한 한국어 문자열이 실제 화면에 보임
- 글자 깨짐과 겹침 여부를 확인함
- 설정 화면 진입/복귀와 게임 재실행이 정상임

## 11. Claude에게 바로 전달할 요청문

```text
Q:\SteamLibrary\steamapps\common\SWD3\SWD3_Korean_Localization\CLAUDE_HANDOFF.md를 먼저 끝까지 읽고, 같은 폴더 안의 자료만 기준으로 현재 상태를 검증해 주세요. 실제 Steam 설치 폴더는 읽기 전용으로 취급하고, 사용자 요청 전에는 수정하지 마세요.

우선 과제는 두 갈래입니다.
1) 번역을 이어갈 때는 translation\SWD3_translation_master.tsv의 기존 ko를 보존하고 Scene.txt의 ESS507부터 최대 100행 또는 번체 원문 2,500자만 처리합니다. zh-Hant를 기준으로 하고 zh-Hans/en/ja는 교차검수에만 사용합니다. 제어코드와 키를 바꾸지 마세요.
2) 게임 적용을 연구할 때는 translation\mod_probe와 공식 SS2Dtool.exe 형식을 분석해, 기본 메뉴/환경설정의 몇 개 문자열만 포함하는 최소 정상 .ssmod를 먼저 작업 폴더 안에 만드세요. 이전의 .ext 직접 활성화 방식은 게임을 종료시켰으므로 반복하지 마세요.

파일 수정 전후에 행 수, 중복 키, 한국어 행 수, 기존 번역 보존, 제어코드 종류·개수·순서를 검사하고 결과를 짧게 기록해 주세요. 한국어 적용 성공은 실제 게임 화면에서 한국어가 보일 때만 선언하세요.
```

## 12. 마지막 주의사항

- 모든 신규 분석물, 추출물, 시험 패키지, 로그는 `Q:\SteamLibrary\steamapps\common\SWD3\SWD3_Korean_Localization` 아래에 둔다.
- 실제 게임 설치 폴더는 배포 대상이지 작업 저장소가 아니다.
- 현재 게임 상태는 정상 영어 실행 상태로 유지한다.
- 다음 실기 시험 전에는 반드시 새 백업과 복구 절차를 준비한다.

## 13. 쨈 점검 메모 (2026-10-13 22시대)

### 장부
- TSV/XLSX 해시 = 인계 기록과 일치. 12,186행, ko 4,236, 중복 0, 제어코드 불일치 0. 장부 쪽 문제 없음.

### MOD 종료 원인 (정적 분석, 실기 미검증)
1. `swd3_ko_test_index.ext`는 SS2Dtool "Create SSMOD"에 넣을 **패킹 입력용 인덱스**인데, 패킹 없이 modlist.txt에 직접 등록됨. modlist는 .ssmod 패키지를 읽는다.
2. 서식이 공식 script_index.ext와 다름: BOM 없음·LF 줄바꿈, MODGameVersion 2,0(공식 2,3), 경로에 `data_2/` 접두(공식은 맨 파일명).
3. 격리된 log에 "program is running. exit." 6회 → 이전 프로세스가 남은 상태에서 재실행하면 단일 실행 검사로 즉시 종료됨. 일부 "시작 직후 종료"는 MOD와 무관했을 가능성.

### 인계서와 실제 설치 폴더의 차이
- `Resource\fontType_index.ext` : 아직 KoreanUI.ttf 지정 상태(BOM 제거됨). 원본 아님.
- `en\StringDB.txt` : 설정 메뉴 한국어 15줄 적용 상태. 원본 아님.
- `Resource\KoreanUI.ttf`, `KoreanTest.ttf` 추가 파일 존재.
- 즉 "정상 영어 상태"가 아니라 "환경설정 일부 한국어 + 한국어 폰트 적용 상태"다. 원본은 backups\render_test_original.
- `Mods\modlist.txt`는 tsw_2x.ssmod(워크숍 3013725485)만 활성 — 정상.

### 참고
- `tools\list_smod_index.py`는 엔트리 앞 reserved 4바이트를 엔트리 뒤로 읽어 깨짐(첫 엔트리부터 어긋남).
- 문자열 계층 정리: 메뉴/UI = en\StringDB.txt(낱개 파일, 교체로 표시 성공), 본문 4종 = script_index.ssmod 내부 → MOD 패킹 필요.

### 새로 만든 것
- `translation\mod_build\ko_name_test_v2\` : 공식 서식 맞춘 최소 인덱스 + name.txt. 패킹·시험 절차는 폴더 README.

### 14. 실기 성공 (2026-10-13 22:39)
- `Mods\swd3_ko_name_test.ssmod`(v4, 8,980B) + modlist 등록 상태로 게임 실행 → 시작 화면 인물명 한국어 표시 확인(운쌤).
- 확정 경로: SS2Dtool로 .ext만 패킹(빈 엔트리) → `tools\patch_ssmod_fill.py`로 실제 txt를 zstd blob(`Z`+u32 압축+u32 원본+프레임)으로 주입.
- MODsystemMOD 0 일반 MOD로 영어 슬롯(LangID 2) 텍스트 교체가 됨.

### 15. 2026-10-14 작업
- 정본 위치: Q:\SteamLibrary\steamapps\common\SWD3\SWD3_Korean_Localization (D:\ 사본 삭제됨)
- `tools\build_ko_ssmod.py`: TSV → 영어 슬롯 4개 파일(원본 바이트 구조 유지) → .ssmod 직접 생성. 헤더 작성기는 SS2Dtool 출력과 바이트 일치 검증. SS2Dtool 불필요
- 설치: Mods\swd3_ko.ssmod (modlist 1), swd3_ko_name_test 0으로 끔. 백업 backups\mod_install_20261014_*
- round 29: Scene ESS507~ESS606 99행/2,481자. ko 4,335, 제어코드 불일치 0, 변경 행 99줄만. 검수필요 4건(ESS513 세이렌, ESS526 신드바드, ESS543 요르단, ESS551 한시)
- `tools\apply_round_json.py`: 회차 JSON 반영기. `tools\sync_master_xlsx.py`: openpyxl 동기화(기존 .mjs는 Codex 런타임 의존이라 사용 불가)
- XLSX는 round 27 값(4,143)에 머물러 있었음 → round 29로 동기화
- 다음: Scene ESS607부터

### 16. 2026-10-23 작업
- round 30~32: Scene ESS607~ESS893 289행(베네치아 헨리·재시 심부름, 보석상, 교회 잠입, 묘비 수학 퍼즐, 화형장·마일스·릴리안·니콜 번개 사건). ko 4,624, 제어코드 불일치 0
- `tools\next_batch.py`(다음 100행/2,500자 추출) 추가. ESS693 원문 '和和' 중복 → 1회 번역
- 표기: 賈西=재시(NAME135), 丕平=피핀, 矮子丕平=땅딸보 피핀, 波爾=보르, 菲力斯=펠릭스, 高盧=갈리아, 無酵餅=무교병, %T코드 획득문은 "%T###. 획득"
- XLSX round 32 동기화, MOD 재빌드·설치(Mods\swd3_ko.ssmod 288,742B). 대사 화면 표시는 여전히 실기 미확인
- 다음: ESS894부터
- (같은 날 추가) round 33~35: ESS894~ESS1174 281행(무스펠 소환·니콜 동행, 트로이 책장, 마계 상점, 지하감옥 666 퍼즐, 출항, 이동섬·코르넬리우스·릴리안 제물 장면). ko 4,905. 姆斯比爾=무스펠, 康那里士=코르넬리우스, 藍魔神=푸른 마신, 阿丹=아르단. 다음: ESS1175
- (같은 날 추가) round 36~38: ESS1175~ESS1451 277행(릴리안 죽음·마일스의 신 증오, 이동섬 석상 정령 4체(미카엘·아테나·스핑크스·포세이돈), 빙산섬·푸른 마신 봉인, 위다드 첫 등장). ko 5,182. 藍人=푸른 인간(NAME174 맞춤, en Kelpy), 冰山島=빙산섬, 恐懼之王=공포의 왕. 다음: ESS1452

### 17. 2026-10-27 작업
- round 39~41: ESS1452~ESS1740 289행(빙산섬 탈출·위다드 합류, 포세이돈 석상, 베네치아 호민관과 기사단, 이동섬 상점·아고스 합류, 타드무르·켄디의 집, 다마스쿠스 우마이야 왕궁·혜언 첫 등장). ko 5,471
- 표기: 凱利賓瓦力德=할리드 빈 왈리드(역사 인물, 영문판 Kelly는 오기), 老衲=소승, 列拉=레일라, 薩西=사시, 蘇里曼=술레이만. 絕情貓袖箭은 ItemName533 "절정묘 수전" 따름(아이템명 재검토 필요)
- MOD 재빌드·설치(ko_full_20261027). 다음: ESS1741
- 2026-10-28 운쌤 확정: 번역은 중문(zh-Hant)을 무조건 기준으로 한다. 영문판과 다르면 중문을 따른다. 絕情貓袖箭=절정묘 수전 유지, 혜언 말투(소승·여시주) 확정

- 2026-10-28 [헌원검3][자동] round42~44 반영, ko 5,743, 다음 ESS2013. MOD 재빌드·설치

- 2026-10-28 [헌원검3][자동] round45~46 반영, ko 5,937, 다음 ESS2207. MOD 재빌드·설치

- 2026-10-28 [헌원검3][자동] round47~49 반영, ko 6,162, 다음 ESS2432. MOD 재빌드·설치

- 2026-10-28 [헌원검3][자동] round50~52 반영, ko 6,442, 다음 ESS2711. MOD 재빌드·설치

- 2026-10-28 [헌원검3][자동] round53~55 반영, ko 6,732, 다음 ESS3001. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round58~60 반영, ko 7,180, 다음 ESS3449. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round61~63 반영, ko 7,475, 다음 ESS3743. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round64~66 반영, ko 7,754, 다음 ESS4022. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round67~69 반영, ko 8,008, 다음 ESS4276. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round70~72 반영, ko 8,236, 다음 ESS4504. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round73~75 반영, ko 8,484, 다음 ESS4752. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round76~78 반영, ko 8,784, 다음 ESS5052. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round79~81 반영, ko 9,068, 다음 ESS5336. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round82~84 반영, ko 9,275, 다음 ESS5543. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round85~87 반영, ko 9,554, 다음 ESS5797. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round88~90 반영, ko 9,854, 다음 ESS6087. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round91~93 반영, ko 10,154, 다음 ESS6383. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round94~96 반영, ko 10,454, 다음 ESS6671F. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round97~99 반영, ko 10,754, 다음 ESS6958. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round100~102 반영, ko 11,052, 다음 ESS7273. MOD 재빌드·설치

- 2026-10-29 [헌원검3][자동] round103~105 반영, ko 11,352, 다음 ESS7578. MOD 재빌드·설치

- 2026-10-30 [헌원검3][자동] round106~108 반영, ko 11,652, 다음 ESS7874. MOD 재빌드·설치

- 2026-10-30 [헌원검3][자동] round109~111 반영, ko 11,952, 다음 ESS8167. MOD 재빌드·설치

- 2026-10-30 [헌원검3][자동] round112~114 반영, ko 12,185, 다음 ESS5767b. MOD 재빌드·설치

- 2026-10-30 [헌원검3][자동] round115~115 반영, ko 12,186, 다음 DONE. MOD 재빌드·설치

### 18. 2026-10-30 메뉴·상태 문자열(StringDB) 한국어화
- 대상: 게임 en\StringDB.txt (낱개 파일, MOD 아님). 원본은 translation\stringdb\en_StringDB.orig.txt, 중문 기준은 zh-Hant_StringDB.orig.txt(=게임 zh-Hant\StringDB - 복사본.txt)
- 게임 zh-Hant\StringDB.txt는 10-16에 다른 작업으로 일부 한국어(185줄)가 들어간 UTF-16 파일 → 건드리지 않음, 참고용 사본만 보관
- 567줄 번역(키보드 키 이름 100~384는 영문 유지). ko_part1/2.json → tools\build_stringdb.py --install. 서식코드(%d %s %% $n \r\n) 원문과 일치 검증
- 기존 en\StringDB.txt 백업: backups\StringDB.en.before_20261030_131250.txt
- 탭 이름(New/Recover/…)·상단 메뉴(Items/Equip/Skill/System)·Buy/Sell 버튼은 이미지라 미포함

### 19. 2026-10-30 워크샵 배포판
- tools\build_workshop_ssmod.py → workshop\upload\swd3_korean.ssmod (본문4+StringDB+NanumGothic(OFL)+fontType_index.ext, 단일 모드). 업로드 안내 workshop\README_업로드.md
- 기존 KoreanUI.ttf=함초롬바탕(한컴), KoreanTest.ttf=맑은 고딕(MS) → 재배포 불가/불명확이라 배포판에 미포함
- 깨끗한 설치 상태 모의 시험 중: en\StringDB.txt·Resource\fontType_index.ext 원본 복원, swd3_ko 끄고 swd3_korean 켬. 백업 backups\workshop_test_*
- 미검증: 모드 안의 StringDB.txt / 글꼴 / fontType_index.ext 가 실제로 적용되는지

### 20. 2026-11-09 일반 배포본
- release\SWD3_KoreanPatch_v1.0.zip (게임 폴더에 풀고 KoreanPatch_Install.bat 실행). 낱개 파일 방식(검증된 방식): Mods\swd3_ko.ssmod + en\StringDB.txt + Resource\NanumGothic-Regular.ttf + fontType_index.ext, modlist 자동 등록(PowerShell), 원본 백업·제거 배치 포함
- 시험 위해 게임은 원본 상태로 둠(swd3_ko 0, swd3_korean 0). 설치 배치 실기 미검증
- release 폴더의 빈 SWD3_Korean_Patch_v1.0.zip, ziYbfZuz 는 zip 실패 잔여물(삭제 대상)

## 21. 이미지 한글화(TSW) + 본명조 (2026-11-09)
- 생성: `python3 tools/make_ko_images.py [접두어]` (설정 translation/images/labels.json, 결과 translation/images/ko)
  - 배경 모드: 기본 inpaint / mode:comp(영·중 합성) / med:1·3(그룹 중앙값+거울타일) / fillsrc(띠 텍스처 복사) / bgfile / bgclear / items(한 이미지 여러 글자)
- 패킹: `python3 tools/build_ko_ssmod.py <출력> --tsw` → ko 이미지가 있는 그룹 전체를 LangID 2 TSW로 추가(나머지 sn은 원본 블롭 복사, 빈 슬롯은 off0/size0)
- 폰트: Resource/fontType_index.ext 전각(0) → NotoSerifKR-Medium.otf

## 22. 편의 모드(KoQoL) 시도 + 진행 메모 (2026-11-09)
### 상태: 미완료 — 게임에서 스크립트가 실행된 흔적 없음
- 목표(운쌤 요청): ①자동전투 기본 ②대사 즉시 표시 ③인카운터 조절(→F9 끄기/켜기 선택) ④돈 조정(→전투 획득 2배) ⑤퀘스트 목표 화면 표시
- 게임 로직은 script_index.ssmod 안 lua(45개, 추출본 convenience/orig). 훅: OnEvent.PlayerMove(인카운터), Battle_PlayerInit(AImode 1=종합자동), BattleGain(돈·경험치), InputKeyDown
- 1차: 같은 이름 lua 덮어쓰기(swd3_ko_qol.ssmod) → 효과 없음
- 2차: 별도 KoQoL.lua가 원본 함수를 감싸는 방식(swd3_koqol.ssmod, tools/build_qol_ssmod.py) → 실행 확인 지표인 Save/setting_v2.lua의 KB_F9가 계속 0 = 스크립트 미실행으로 판단
- 다음 확인: 모드 lua가 실제 로드되는 조건(워크샵 tsw_2x의 BattleGraphics2x.lua 사례 비교, DAT 타입·LangID·ext 형식), Mods 폴더 파일 잠김(게임 실행 중엔 교체 불가 → 새 이름으로 설치함)
- ② 대사 즉시 표시: TypeSpeed는 이미 0(최고속). 글자 출력은 swd3.exe 내부 → exe 패치 필요
- ⑤ 퀘스트 화면 표시: 필드 그리기 훅 없음(DrawMenuAfter, Battle_DrawBGI뿐) → exe 패치 필요
- Mods 현황: swd3_ko_qol.ssmod=0(1차), swd3_koqol.ssmod=1(2차). 배포본 v1.1에는 미포함

### 진행 막힘 문의 메모
- 수도원 밀실 보물상자 전투(BS55)는 일반 상자 전투(호피 옷). 이겨도 정상
- 마물정련(플래그 73)·항해도: '수도원 안' 맵의 수도원장(NPC 207, 좌표 101,67)과 대화 → TALK207. 선행 플래그 101 필요(TALK366 이벤트)
- '문이 잠겨 있다' 문 = 수도원 미로 출구(NPC 269), 수도원장 이벤트(플래그 102) 후 열림
- [갱신 2026-11-09] 원인 확인: 모드 lua는 ext·메타의 MODsystemMOD=1 이어야 실행됨. systemMOD 1 판(swd3_koqol3.ssmod)에서 F9 효과음 동작 확인(운쌤). 자동전투·돈 2배는 확인 대기
- [v1.2 배포본 2026-11-09] release\SWD3_KoreanPatch_v1.2.zip = 한글 모드(name.txt에 KoQoL_* 표시 문자열 포함) + 편의 모드 swd3_ko_qol.ssmod(KoQoL.lua + ItemPicData.lua 덧붙임, systemMOD 1) + StringDB + 본명조
  - 편의 키: F4 표시, F5 필드 전투(보통/2/4배/끔, 걸음 수 가산), F6 이동 속도(MapDetail.BasicSpeed 배율), F7 돈, F8 경험치(BattleGain 배율). 자동전투(AImode)·전투속도(SPD 배율)는 효과 없어 제외
  - 메뉴 화면 종류를 스크립트가 알 수 없어(DrawMenuAfter 인자 없음) 설정표는 키 입력 후 3초/F4 고정 표시
  - lua 안 한글 리터럴은 '?'로 깨짐 → StringDB 키로 전달
