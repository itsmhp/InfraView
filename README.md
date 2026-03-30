# InfraView by PIN

> **Dashboard hub untuk monitoring anggaran & pengadaan IT Infrastructure BRI.**
> Dibangun oleh tim **PIN** (IT Infrastructure PMO).

---

## Tentang

InfraView adalah aplikasi web yang menyatukan semua dashboard monitoring IT Infrastructure ke dalam satu platform terpusat. Dashboard HTML yang dihasilkan oleh berbagai tools internal (Laporan CJE0, Laporan RKA-IT, dll.) dapat di-upload dan ditampilkan dalam viewer yang aman dan responsif.

### Mengapa InfraView?

- **Satu pintu masuk** — Semua dashboard bisa diakses dari satu tempat
- **DLP Compliant** — Tidak ada data sensitif yang diproses di server; semua pemrosesan Excel dilakukan di laptop lokal
- **Multi-role** — Admin mengupload dashboard, Viewer hanya melihat
- **Responsive** — Bisa diakses dari laptop maupun HP

---

## Fitur

| Fitur | Deskripsi |
|-------|-----------|
| Dashboard Hub | Grid card dengan status freshness (terbaru / aging / stale) |
| KPI Summary | Ringkasan jumlah dashboard, data terbaru, dan yang perlu update |
| Iframe Viewer | Viewer dashboard HTML dengan sandbox isolation |
| Stale Warning | Peringatan otomatis jika data sudah lama tidak diupdate |
| Collapsible Sidebar | Sidebar bisa diminimize, state tersimpan di localStorage |
| Drag-Drop Upload | Upload file HTML via drag-drop atau paste (DLP-friendly) |
| User Management | Admin bisa kelola user, reset password, toggle status |
| Keyboard Shortcuts | `Alt+H` Hub, `Alt+R` Refresh, `Alt+F` Fullscreen, `Alt+P` Print |
| Responsive Design | Tampilan optimal di desktop, tablet, dan mobile |
| Custom Error Pages | Halaman 404 dan 403 yang branded |
| Print Support | Cetak dashboard langsung dari viewer |
| Fullscreen Mode | Tampilkan dashboard dalam mode fullscreen |

---

## Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Backend | Python 3.11+, Flask 3.x, Flask-Login, SQLAlchemy |
| Frontend | Tailwind CSS (CDN), Vanilla JavaScript |
| Database | SQLite (development) / PostgreSQL (production) |
| Server | Gunicorn (production) |
| Hosting | Render.com / VPS / Lokal |

---

## Quick Start

### Prasyarat

- Python 3.11 atau lebih baru
- pip (package manager)

### Instalasi

```bash
# 1. Clone repository
git clone https://github.com/itsmhp/InfraView.git
cd InfraView

# 2. Buat virtual environment
python -m venv venv

# 3. Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. (Opsional) Buat file .env
# Salin .env.example ke .env dan sesuaikan konfigurasi

# 6. Seed database (buat user dan dashboard default)
python seed.py

# 7. Jalankan aplikasi
python app.py
```

Buka **http://localhost:5000** di browser.

### Shortcut (Windows)

Double-click `start.bat` di folder root untuk langsung menjalankan aplikasi.

### Default Login

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Viewer | `viewer` | `viewer123` |

> **Penting:** Segera ganti password default setelah setup pertama!

---

## Struktur Proyek

```
InfraView/
├── app.py                  # Flask app factory + error handlers
├── config.py               # Konfigurasi (SQLite/PostgreSQL)
├── seed.py                 # Seeder database (user & dashboard default)
├── requirements.txt        # Python dependencies
├── start.bat               # Shortcut untuk menjalankan (Windows)
│
├── models/
│   ├── __init__.py         # SQLAlchemy instance
│   ├── user.py             # Model User (login, role, last_login)
│   └── dashboard.py        # Model Dashboard (content, freshness)
│
├── routes/
│   ├── auth.py             # Login / Logout
│   ├── main.py             # Hub & Dashboard viewer
│   └── admin.py            # Admin panel (CRUD dashboard & user)
│
├── templates/
│   ├── base.html           # Master template (header, sidebar)
│   ├── login.html          # Halaman login
│   ├── hub.html            # Dashboard grid + KPI summary
│   ├── view.html           # Dashboard viewer (iframe)
│   ├── admin/              # Template admin panel
│   └── errors/             # Custom 404, 403
│
└── static/
    ├── css/style.css       # Custom styles
    ├── js/admin.js         # Drag-drop upload handler
    └── img/                # Logo BRI (SVG)
```

---

## Arsitektur

```
┌─────────────┐     ┌──────────────────┐     ┌────────────────┐
│  Excel SAP  │────>│  Python Scripts   │────>│  HTML Dashboard │
│  (Lokal)    │     │  (Laporan CJE0,  │     │  (Self-contained│
│             │     │   Laporan RKA)   │     │   + Chart.js)  │
└─────────────┘     └──────────────────┘     └───────┬────────┘
                                                      │ Upload
                                                      v
                    ┌──────────────────────────────────────────┐
                    │           InfraView (Flask)               │
                    │                                          │
                    │  ┌──────┐  ┌──────┐  ┌───────────────┐  │
                    │  │ Auth │  │ Hub  │  │ Viewer(iframe)│  │
                    │  │      │  │ +KPI │  │ + Stale Warn  │  │
                    │  └──────┘  └──────┘  └───────────────┘  │
                    │         ┌──────────┐                     │
                    │         │  Admin   │                     │
                    │         │  Panel   │                     │
                    │         └──────────┘                     │
                    │              │                            │
                    │         ┌────v─────┐                     │
                    │         │ SQLite/  │                     │
                    │         │ Postgres │                     │
                    │         └──────────┘                     │
                    └──────────────────────────────────────────┘
```

### Alur Data

1. **Lokal (Laptop):** Excel SAP export diproses oleh Python script menjadi HTML dashboard
2. **Upload:** Admin login ke InfraView, upload HTML via drag-drop atau paste
3. **Tampilkan:** Semua user bisa melihat dashboard via iframe viewer

---

## Role & Hak Akses

| Kemampuan | Admin | Viewer |
|-----------|:-----:|:------:|
| Lihat dashboard hub | O | O |
| Lihat dashboard viewer | O | O |
| Fullscreen, Print, Refresh | O | O |
| Upload/update HTML dashboard | O | X |
| Kelola dashboard (CRUD) | O | X |
| Kelola user | O | X |
| Akses admin panel | O | X |

---

## Dashboard

InfraView mengelola 4 dashboard utama:

| # | Dashboard | Slug | Deskripsi |
|---|-----------|------|-----------|
| 1 | CJE0 Budget Monitoring | `cje0` | Tracking budget real-time dari SAP CJE0 |
| 2 | Laporan RKA IT | `rka` | Realisasi anggaran TI bulanan & kumulatif |
| 3 | Status Pengadaan | `pengadaan` | Analisis status pengadaan INF |
| 4 | Tracking Pengadaan PLO | `tracking-plo` | Tracking pengadaan PLO Group |

---

## DLP Compliance

InfraView dirancang untuk mematuhi kebijakan DLP (Data Loss Prevention):

- **Tidak ada data Excel yang diproses di server** — semua pemrosesan dilakukan di laptop lokal
- **Upload HTML saja** — file yang di-upload hanya HTML statis (sudah jadi dashboard)
- **Opsi Paste HTML** — untuk menghindari upload file jika diblokir DLP, bisa paste HTML secara langsung
- **Database hanya menyimpan HTML output** — bukan raw data keuangan

---

## Deployment

### Lokal (Development)

```bash
python app.py
# Server berjalan di http://localhost:5000
```

### Production (Render.com)

1. Push repository ke GitHub
2. Buat Web Service baru di [Render](https://render.com)
3. Connect ke GitHub repository
4. Render akan otomatis mendeteksi `render.yaml`
5. Set environment variables:
   - `SECRET_KEY` — random string yang panjang
   - `DATABASE_URL` — PostgreSQL connection string (dari Render PostgreSQL addon)

### Production (VPS/Server)

```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan dengan Gunicorn
gunicorn app:app --bind 0.0.0.0:8000 --workers 2
```

---

## Keyboard Shortcuts

| Shortcut | Aksi |
|----------|------|
| `Alt + H` | Kembali ke Hub |
| `Alt + R` | Refresh dashboard (di viewer) |
| `Alt + F` | Fullscreen (di viewer) |
| `Alt + P` | Print dashboard (di viewer) |
| `Esc` | Tutup sidebar (mobile) / tutup modal |
| `?` | Tampilkan bantuan shortcut (klik icon di header) |

---

## Contributing

InfraView dikembangkan oleh tim PIN (IT Infrastructure PMO) BRI.

1. Fork repository
2. Buat feature branch (`git checkout -b feature/nama-fitur`)
3. Commit perubahan (`git commit -m 'Tambah fitur baru'`)
4. Push ke branch (`git push origin feature/nama-fitur`)
5. Buat Pull Request

---

## License

Internal use only — PT Bank Rakyat Indonesia (Persero) Tbk, Divisi IT Infrastructure.

---

<p align="center">
  <strong>InfraView</strong> by PIN — IT Infrastructure PMO<br>
  <em>Built with Flask + Tailwind CSS</em>
</p>
