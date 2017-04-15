@echo off
SETLOCAL ENABLEEXTENSIONS
for /f %%i in ('cd') do set org=%%i
set mypath=%~dp0
cd %mypath%
git pull
cd %org%
ENDLOCAL
