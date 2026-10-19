@echo off
setlocal
title Guestbook - Phien ban Vibe Code (Port 5001)

echo ============================================================
echo   KHOI DONG GUESTBOOK - PHIEN BAN VIBE CODE (Port 5001)
echo ============================================================

:: Tim trinh thong dich Python (uu tien py, sau do python)
set PYTHON_CMD=
where py >nul 2>nul && set PYTHON_CMD=py
if not defined PYTHON_CMD (
    where python >nul 2>nul && set PYTHON_CMD=python
)

if not defined PYTHON_CMD (
    echo [LOI] Khong tim thay Python tren may cua ban!
    echo Hay cai dat Python tai: https://www.python.org/
    echo Chu y: Nho tich vao o "Add Python to PATH" trong luc cai dat.
    echo ============================================================
    pause
    exit /b
)

echo [1/2] Dang kiem tra va cai dat thu vien can thiet...
%PYTHON_CMD% -m pip install -r "%~dp0requirements.txt" --quiet

echo [2/2] Dang khoi dong server Flask...
echo Server se mo tai dia chi: http://127.0.0.1:5001
echo Nhan Ctrl + C de dung server.
echo ============================================================

cd /d "%~dp0vibe_code"
%PYTHON_CMD% app.py

pause
