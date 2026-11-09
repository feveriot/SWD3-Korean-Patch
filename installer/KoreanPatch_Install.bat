@echo off
setlocal
cd /d "%~dp0"
echo ===========================================================================
echo  Xuan-Yuan Sword III: Mists Beyond the Mountains (Steam) - Korean Patch v1.2
echo ===========================================================================
if not exist "swd3.exe" (
  echo [ERROR] swd3.exe not found. Extract this zip into the game folder
  echo         ^(steamapps\common\SWD3^) and run again.
  pause & exit /b 1
)
set B=KoreanPatch\backup
if not exist "%B%" mkdir "%B%"
if not exist "%B%\StringDB.txt" copy /y "en\StringDB.txt" "%B%\StringDB.txt" >nul
if not exist "%B%\fontType_index.ext" copy /y "Resource\fontType_index.ext" "%B%\fontType_index.ext" >nul
if not exist "%B%\modlist.txt" if exist "Mods\modlist.txt" copy /y "Mods\modlist.txt" "%B%\modlist.txt" >nul
if not exist "Mods" mkdir "Mods"
copy /y "KoreanPatch\files\Mods\swd3_ko.ssmod" "Mods\" >nul || goto fail
copy /y "KoreanPatch\files\Mods\swd3_ko_qol.ssmod" "Mods\" >nul || goto fail
copy /y "KoreanPatch\files\en\StringDB.txt" "en\" >nul || goto fail
copy /y "KoreanPatch\files\Resource\NotoSerifKR-Medium.otf" "Resource\" >nul || goto fail
copy /y "KoreanPatch\files\Resource\fontType_index.ext" "Resource\" >nul || goto fail
powershell -NoProfile -ExecutionPolicy Bypass -File "KoreanPatch\modlist_on.ps1" "%CD%" || goto fail
echo.
echo [OK] Installed. Set the game language to English and start the game.
pause & exit /b 0
:fail
echo [ERROR] Install failed. Close the game and launcher, then try again.
pause & exit /b 1
