# InfraView — Quick Start Guide

## Cara Menjalankan Aplikasi

### Windows — Paling Mudah! 🎯

**Opsi 1: Double-klik file `run.bat`**
1. Buka folder InfraView
2. Double-klik **`run.bat`** (atau klik kanan → Open)
3. Tunggu sebentar, browser otomatis buka http://localhost:5000
4. Selesai! Siap login

**Opsi 2: Pakai PowerShell** (warna-warni 🌈)
```powershell
.\run.ps1
```

---

### Mac / Linux

```bash
# Pakai bash script
bash run.sh
```

---

## Login Default

| User    | Password     | Role    |
|---------|------------|---------|
| `admin` | `admin123` | Admin — akses semua fitur + upload |
| `viewer` | `viewer123` | Viewer — hanya lihat dashboard |

---

## Apa yang dilakukan script?

1. **Cek Python** — Pastikan Python terinstall
2. **Install dependencies** — Flask, SQLAlchemy, Flask-Login, etc
3. **Buat database** — Jika belum ada (pertama kali)
4. **Jalankan app** — Server di http://localhost:5000

---

## Akses Aplikasi

Setelah berjalan, buka browser:

```
http://localhost:5000
```

atau scan QR code di terminal untuk akses dari smartphone di network yang sama.

---

## Features

### Admin Panel
- ✅ Upload HTML dashboard (drag-drop)
- ✅ Kelola dashboard (tambah, edit, hapus)
- ✅ Kelola user (tambah, reset password, nonaktifkan)
- ✅ Lihat statistik

### Dashboard Hub
- ✅ Card grid dengan semua dashboard
- ✅ Status indikator (data ada/kosong)
- ✅ Last updated timestamp
- ✅ Responsive (mobile-friendly)

### Dashboard Viewer
- ✅ Full-page iframe
- ✅ Refresh button
- ✅ Responsive

---

## Upload Dashboard

1. Login sebagai **admin**
2. Klik **Admin Panel** (kanan atas)
3. Klik **Upload** di salah satu dashboard
4. Drag-drop file `.html` atau klik untuk pilih
5. File akan tersimpan otomatis
6. **Hub akan update**, viewer bisa lihat dashboard baru

---

## Struktur File

```
InfraView/
├── app.py              # Flask app factory
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── seed.py            # Buat DB + default users
├── run.bat            # ← Shortcut Windows (double-klik ini!)
├── run.ps1            # Shortcut PowerShell
├── run.sh             # Shortcut Linux/Mac
├── models/            # Database models
├── routes/            # API routes
├── templates/         # Jinja2 templates
├── static/            # CSS, JS
├── files/             # Dokumentasi + hub design
└── infraview.db       # Database (auto-created)
```

---

## Troubleshooting

### "Python tidak ditemukan"
→ Install Python dari https://python.org

### Port 5000 sudah dipakai
```bash
python -c "import os; os.environ['FLASK_ENV']='development'; from app import app; app.run(port=5001)"
```

### Database corrupt
Hapus `infraview.db`, jalankan `python seed.py` lagi

### Lupa password
Buka terminal di folder ini:
```bash
python -c "
from app import app
from models.user import User
from models import db

with app.app_context():
    user = User.query.filter_by(username='admin').first()
    user.set_password('newpassword123')
    db.session.commit()
    print('Password reset!')
"
```

---

## Deploy ke Render.com

1. Push ke GitHub: https://github.com/itsmhp/InfraView
2. Login ke https://render.com
3. Create Web Service → Connect GitHub
4. Render akan otomatis baca `render.yaml`
5. Selesai! Live di Render subdomain

---

## Dokumentasi Lengkap

Untuk info lebih detail, baca:
- `files/README.md` — Hub architecture & design
- `files/ARCHITECTURE.md` — Technical diagrams
- `plan.md` — Development plan & decisions

---

**Selamat menggunakan InfraView! 🚀**

Ada pertanyaan? Buka GitHub Issues atau hubungi admin.
