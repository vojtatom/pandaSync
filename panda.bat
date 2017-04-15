@echo off
SETLOCAL ENABLEEXTENSIONS
for /f %%i in ('cd') do set loc=%%i
set mypath=%~dp0
cd %mypath%
python . %*
cd %loc%
ENDLOCAL