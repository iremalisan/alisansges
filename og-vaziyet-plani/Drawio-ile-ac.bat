@echo off
setlocal
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
  start "" "%DRAWIO%" "%DIAGRAM%"
  exit /b 0
)

start "" "%DIAGRAM%"
exit /b 0
