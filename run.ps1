# InfraView — PowerShell script untuk menjalankan aplikasi
# Usage: .\run.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  InfraView — Dashboard Hub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    python --version 2>$null
} catch {
    Write-Host "ERROR: Python tidak ditemukan." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "[1/3] Menginstall dependencies..." -ForegroundColor Yellow
pip install -q flask flask-sqlalchemy flask-login python-dotenv gunicorn 2>$null

# Create DB if not exists
if (-not (Test-Path "infraview.db")) {
    Write-Host "[2/3] Membuat database..." -ForegroundColor Yellow
    python seed.py
} else {
    Write-Host "[2/3] Database sudah ada." -ForegroundColor Yellow
}

Write-Host "[3/3] Menjalankan aplikasi..." -ForegroundColor Yellow
Write-Host ""
Write-Host "✓ Server berjalan di: http://localhost:5000" -ForegroundColor Green
Write-Host "✓ Login: admin / admin123" -ForegroundColor Green
Write-Host "✓ Tekan Ctrl+C untuk stop" -ForegroundColor Green
Write-Host ""

python app.py
