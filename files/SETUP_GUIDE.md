# 🚀 Quick Start Guide: Dashboard Hub Deployment

## ✅ Apa yang Sudah Siap

```
✓ index.html          - Hub utama dengan navigation & iframe loader
✓ dashboards/cje0.html        - CJE0 Budget Monitoring
✓ dashboards/pengadaan.html   - Status Pengadaan  
✓ dashboards/inf.html         - Infrastructure Dashboard
✓ README.md          - Documentation lengkap
✓ .gitignore         - Git config
```

---

## 📋 SETUP GITHUB PAGES (5 Menit)

### **Step 1: Siapkan di GitHub**

1. Buka https://github.com/new
2. **Repository name:** `dashboard-hub`
3. **Description:** "Multi-dashboard hub untuk IT Infrastructure monitoring"
4. **Visibility:** Public (agar bisa diakses)
5. ✅ Initialize with README ✓
6. **Create repository**

---

### **Step 2: Clone ke Komputer**

```bash
# Buka terminal/command prompt
cd Desktop  # atau folder pilihan kamu

# Clone repo
git clone https://github.com/YOUR_USERNAME/dashboard-hub.git
cd dashboard-hub
```

---

### **Step 3: Copy Files**

Sebelumnya dari `/outputs/` kamu, copy:

```bash
# Copy index.html, dashboards/, README.md, .gitignore ke folder lokal
# Struktur akhir:
# dashboard-hub/
# ├── index.html
# ├── dashboards/
# │   ├── cje0.html
# │   ├── pengadaan.html
# │   └── inf.html
# ├── README.md
# └── .gitignore
```

---

### **Step 4: Push ke GitHub**

```bash
# Di folder dashboard-hub/
git add .
git commit -m "Initial commit: Multi-dashboard hub setup"
git push origin main
```

**Expected output:**
```
[main abc1234] Initial commit: Multi-dashboard hub setup
 6 files changed, 1234 insertions(+)
 create mode 100644 index.html
 create mode 100644 dashboards/cje0.html
 ...
```

---

### **Step 5: Aktifkan GitHub Pages**

1. Buka repo di GitHub
2. Klik **Settings** (tab di atas)
3. Scroll ke **Pages** (sidebar kiri)
4. **Source:** Pilih `main` branch
5. **Folder:** Root `/`
6. Klik **Save**

**Status akan berubah:**
```
✓ Your site is published at:
  https://YOUR_USERNAME.github.io/dashboard-hub
```

---

### **Step 6: Share & Test**

Buka URL di browser:
```
https://YOUR_USERNAME.github.io/dashboard-hub
```

**Test checklist:**
- [ ] Hub page load dengan baik
- [ ] Sidebar navigation terlihat
- [ ] Click pada "Budget (CJE0)" → iframe load
- [ ] Click pada "Pengadaan" → dashboard switch
- [ ] Click pada "Infrastructure" → dashboard switch
- [ ] Refresh button berfungsi
- [ ] Keyboard shortcuts work (Ctrl+1, Ctrl+2, Ctrl+3)

---

## 🔄 Update Dashboard (Setiap Kali Ada Data Baru)

```bash
# 1. Edit file dashboard lokal atau copy file baru
# Misal: ada update CJE0 data

# 2. Copy ke dashboards/cje0.html
cp /path/ke/new-dashboard.html dashboards/cje0.html

# 3. Commit & Push
git add dashboards/cje0.html
git commit -m "Update: CJE0 dashboard - latest SAP data"
git push origin main

# Done! Dashboard updated otomatis dalam 1-2 menit
```

---

## 🎯 Optional: Custom Domain

Kalau mau URL cantik (misal `dashboard.bandobrothers.com`):

### **Step 1: Beli Domain**

- Registrar: Niagahoster, Rumahweb, atau GoDaddy
- Budget: ~Rp 50-100rb/tahun
- Domain: `dashboard.bandobrothers.com`

### **Step 2: Setup DNS**

Di GitHub Pages settings:
1. **Custom domain:** Input `dashboard.bandobrothers.com`
2. GitHub akan kasih DNS records yang harus di-update di registrar

Di Registrar (contoh Niagahoster):
```
Type: CNAME
Host: dashboard.bandobrothers.com
Points to: YOUR_USERNAME.github.io
```

### **Step 3: Wait & Verify**

```bash
# Test DNS propagation (5-30 menit)
nslookup dashboard.bandobrothers.com

# Atau cek di: https://dnschecker.org
```

Setelah valid, HTTPS auto-enable via Let's Encrypt.

---

## 🛡️ Security Checklist

✅ **No API keys exposed** (embed sudah aman)  
✅ **HTTPS auto** (GitHub Pages + Let's Encrypt)  
✅ **Sandbox iframe** (scripts isolated)  
✅ **Version control** (track all changes)  
✅ **Auto backup** (Git history)  

---

## 🎨 Customization Tips

### **Change Header Color**

Di `index.html`, cari section CSS:
```css
.header {
    background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%);
    /* ^-- Change these hex colors */
}
```

### **Add New Dashboard**

1. Copy new dashboard ke `dashboards/new.html`
2. Di `index.html`, add di bagian dashboards config:
```javascript
const dashboards = {
    cje0: { ... },
    pengadaan: { ... },
    inf: { ... },
    newdash: {  // ← ADD THIS
        path: 'dashboards/new.html',
        title: 'New Dashboard',
        description: 'Description'
    }
};
```

3. Add nav item:
```html
<div class="nav-item" data-dashboard="newdash">
    <span class="nav-icon">🆕</span>
    <span>New Dashboard</span>
</div>
```

4. Commit & push:
```bash
git add .
git commit -m "Add: New dashboard"
git push origin main
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Dashboard tidak muncul | Clear cache: `Ctrl+Shift+Delete` atau buka private/incognito window |
| CORS error di console | Pastikan path di `dashboards/` benar |
| Sidebar tidak responsive | Update browser ke latest version |
| Changes tidak muncul | Wait 2-3 menit untuk GitHub Pages rebuild |
| Keyboard shortcuts tidak work | Click di header dulu, jangan di iframe |

---

## 📊 Performance Tips

Semua dashboard sudah optimized, tapi:

- **Safari issue dengan iframe scroll?** → Add `scrolling="yes"` di iframe tag
- **Mobile performance slow?** → Minify dashboard HTML (~gzip auto di GitHub Pages)
- **Want to track analytics?** → Add Google Analytics ke `index.html`:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'GA_ID');
</script>
```

---

## 🚀 Next Steps

1. **Deploy ke GitHub Pages** ← Do this first (5 menit)
2. Share URL dengan tim: `https://username.github.io/dashboard-hub`
3. Setup custom domain (optional, 10 menit)
4. Automate dashboard updates dari SAP (future, 1-2 hours)

---

## 💡 For Pak Robi & Team

```
📧 Send this link ke team:
https://YOUR_USERNAME.github.io/dashboard-hub

🔗 For BandoBrothers marketing:
https://dashboard.bandobrothers.com  (if custom domain setup)

📊 All dashboards di satu tempat
✨ Professional, modern, secure
```

---

**Questions?** Check README.md atau reach out!

**Version:** 1.0 Quick Start  
**Status:** Ready to Deploy ✅
