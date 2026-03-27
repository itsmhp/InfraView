#!/bin/bash
# InfraView — Bash script untuk menjalankan aplikasi
# Usage: bash run.sh  atau  ./run.sh

echo ""
echo "========================================"
echo "  InfraView — Dashboard Hub"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 tidak ditemukan."
    exit 1
fi

# Install dependencies
echo "[1/3] Menginstall dependencies..."
pip install -q flask flask-sqlalchemy flask-login python-dotenv gunicorn

# Create DB if not exists
if [ ! -f "infraview.db" ]; then
    echo "[2/3] Membuat database..."
    python3 seed.py
else
    echo "[2/3] Database sudah ada."
fi

echo "[3/3] Menjalankan aplikasi..."
echo ""
echo "✓ Server berjalan di: http://localhost:5000"
echo "✓ Login: admin / admin123"
echo "✓ Tekan Ctrl+C untuk stop"
echo ""

python3 app.py
