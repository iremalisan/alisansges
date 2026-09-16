@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set "DIAGRAM=%~dp0og-vaziyet-plani.drawio"

if not exist "%DIAGRAM%" (
  echo Dosya bulunamadi: og-vaziyet-plani.drawio
  pause
  exit /b 1
)

set "DRAWIO="
set "PF86=%ProgramFiles(x86)%"
if exist "%LOCALAPPDATA%\Programs\draw.io\draw.io.exe" set "DRAWIO=%LOCALAPPDATA%\Programs\draw.io\draw.io.exe"
if exist "%ProgramFiles%\draw.io\draw.io.exe" set "DRAWIO=%ProgramFiles%\draw.io\draw.io.exe"
if exist "%PF86%\draw.io\draw.io.exe" set "DRAWIO=%PF86%\draw.io\draw.io.exe"

if defined DRAWIO (
  start "" "!DRAWIO!" "%DIAGRAM%"
  exit /b 0
)

where draw.io >nul 2>&1
if not errorlevel 1 (
  start "" draw.io "%DIAGRAM%"
  exit /b 0
)

echo Draw.io masaustu uygulamasi bulunamadi.
echo Yine de .drawio dosyasi varsayilan uygulamayla acilacak.
echo Yazilari degistirmek icin kutuya cift tiklayin.
pause
start "" "%DIAGRAM%"
exit /b 0
