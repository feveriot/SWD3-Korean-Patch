@echo off
setlocal
cd /d "%~dp0"
set B=KoreanPatch\backup
if not exist "%B%\StringDB.txt" (
  echo [ERROR] Backup not found. Use Steam "Verify integrity of game files" instead.
  pause & exit /b 1
)
copy /y "%B%\StringDB.txt" "en\StringDB.txt" >nul
copy /y "%B%\fontType_index.ext" "Resource\fontType_index.ext" >nul
powershell -NoProfile -ExecutionPolicy Bypass -File "KoreanPatch\modlist_off.ps1" "%CD%"
if exist "Mods\swd3_ko.ssmod" del /q "Mods\swd3_ko.ssmod"
if exist "Mods\swd3_ko_qol.ssmod" del /q "Mods\swd3_ko_qol.ssmod"
if exist "Resource\NanumGothic-Regular.ttf" del /q "Resource\NanumGothic-Regular.ttf"
if exist "Resource\NotoSerifKR-Medium.otf" del /q "Resource\NotoSerifKR-Medium.otf"
echo [OK] Korean patch removed.
pause
