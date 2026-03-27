@echo off
REM InfraView — Jalankan aplikasi Flask
REM
REM Shortcut untuk menjalankan aplikasi di Windows
REM Double-klik file ini untuk start aplikasi

cd /d "%~dp0"

echo.
echo ========================================
echo   InfraView — Dashboard Hub
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python tidak ditemukan. Install Python terlebih dahulu.
    pause
    exit /b 1
)

REM Install/upgrade dependencies
echo [1/3] Menginstall dependencies...
pip install -q flask flask-sqlalchemy flask-login python-dotenv gunicorn 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Gagal install dependencies.
    pause
    exit /b 1
)

REM Create DB if not exists
if not exist "infraview.db" (
    echo [2/3] Membuat database...
    python seed.py
) else (
    echo [2/3] Database sudah ada.
)

echo [3/3] Menjalankan aplikasi...
echo.
echo ✓ Server berjalan di: http://localhost:5000
echo ✓ Login: admin / admin123
echo ✓ Tekan Ctrl+C untuk stop
echo.

python app.py
