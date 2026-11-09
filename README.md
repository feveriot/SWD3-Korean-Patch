# 헌원검 3: 구름과 산의 저편 (Steam) 한국어 패치

Xuan-Yuan Sword: Mists Beyond the Mountains (Steam, appid 1638230) 비공식 한국어 패치.
중문 번체 원문 기준 번역.

## 받기
[Releases](../../releases)에서 `SWD3_KoreanPatch_v*.zip`을 받으세요.

## 설치
1. zip을 게임 폴더(`swd3.exe`가 있는 곳, 예: `...\steamapps\common\SWD3`)에 풉니다.
2. `KoreanPatch_Install.bat` 실행
3. 게임 언어를 **English**로 두고 실행

제거: `KoreanPatch_Uninstall.bat` (또는 Steam '게임 파일 무결성 확인')

## 내용
- 대사·아이템·인물/지명·전투 문구 (영어 슬롯 교체 모드 `swd3_ko.ssmod`)
- 메뉴·시스템 그림 글자 한글화
- 메뉴 문자열 (`en\StringDB.txt`)
- 글꼴: 본명조 Noto Serif KR (SIL OFL 1.1)
- 편의 모드 `swd3_ko_qol.ssmod` (게임 중 단축키)

| 키 | 기능 |
|---|---|
| F4 | 설정표 표시 고정/해제 (F5~F8 누르면 3초간 표시) |
| F5 | 필드 전투 확률: 보통 → 2배 → 4배 → 끔 |
| F6 | 이동 속도: 보통 → 1.5배 → 2배 (다음 맵부터) |
| F7 | 전투 획득 돈: 보통 → 2배 → 4배 |
| F8 | 전투 획득 경험치: 보통 → 2배 → 4배 |

## 저장소 구성
- `translation/` 번역 정본(TSV), 메뉴 문자열, 그림 글자 설정
- `tools/` 모드 빌드·그림 생성 스크립트 (게임 원본 파일 필요)
- `convenience/KoQoL.lua` 편의 모드 스크립트
- `installer/` 설치·제거 스크립트
- `docs/WORKLOG.md` 작업 기록

게임 원본 데이터와 빌드 결과물(.ssmod, 이미지, 글꼴)은 저장소에 넣지 않았습니다.
비공식 팬 번역입니다. 원작 권리는 SOFTSTAR ENTERTAINMENT INC.에 있습니다.
