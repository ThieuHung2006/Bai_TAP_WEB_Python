@echo off
setlocal
echo ============================================================
echo   KHOI DONG GUESTBOOK - PHIEN BAN VIBE CODE (Port 5001)
echo ============================================================
cd /d "%~dp0\vibe_code"

where py >nul 2>nul
if %errorlevel% equ 0 (
    py app.py
    goto end
)

if exist "C:\Users\hieu\AppData\Local\Python\pythoncore-3.14-64\python.exe" (
    "C:\Users\hieu\AppData\Local\Python\pythoncore-3.14-64\python.exe" app.py
    goto end
)

python app.py

:end
pause
