@echo off
title Student Record Management System
cls

set "PYPATH=C:\Users\I.Jeevani\AppData\Local\Programs\Python\Python312-arm64"
set "GITPATH=C:\Users\I.Jeevani\AppData\Local\Programs\Git\cmd"
set "PATH=%PYPATH%;%GITPATH%;%PATH%"

cd /d "%~dp0"
echo ============================================================
echo   Starting Student Record Management System...
echo ============================================================
echo.

python main.py

echo.
echo Press any key to exit...
pause >nul
