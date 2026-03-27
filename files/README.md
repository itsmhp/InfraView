# 📊 BRI IT Infrastructure Dashboard Hub

Multi-dashboard hub untuk monitoring dan reporting IT Infrastructure di Bank Rakyat Indonesia.

## 📦 Struktur Folder

```
dashboard-hub/
├── index.html                    ← Hub utama (navigation + iframe loader)
├── dashboards/
│   ├── cje0.html                ← CJE0 Budget Monitoring
│   ├── pengadaan.html           ← Status Pengadaan
│   └── inf.html                 ← Infrastructure Dashboard
├── README.md
└── .gitignore
```

## 🚀 Deployment Options

### **Option 1: GitHub Pages (Recommended)**

**Pros:** Gratis, otomatis HTTPS, CDN global, version control  
**Cons:** Static hanya (tapi sudah cukup untuk kasus kamu)

```bash
# 1. Create repo di GitHub
# 2. Clone
git clone https://github.com/USERNAME/dashboard-hub.git
cd dashboard-hub

# 3. Copy files (sudah ada di outputs/)
# index.html + dashboards/ folder

# 4. Push
git add .
git commit -m "Initial: Multi-dashboard hub"
git push origin main

# 5. Enable Pages di Settings → Pages
#    Source: main branch, folder: /
#    Publish ke: https://USERNAME.github.io/dashboard-hub

# 6. (Optional) Setup custom domain
#    Dashboard tersedia di: https://dashboard.bandobrothers.com
```

**Update & Maintenance:**
```bash
# Setiap ada update dashboard:
git add dashboards/cje0.html
git commit -m "Update: CJE0 dashboard $(date +%Y-%m-%d)"
git push origin main
# Auto-deploy dalam 1-2 menit
```

---

### **Option 2: Vercel (Modern Alternative)**

```bash
# 1. Push ke GitHub dulu
# 2. Import ke Vercel (vercel.com)
# 3. Connect GitHub repo
# 4. Auto-deploy on every push
# Live di: https://dashboard-hub.vercel.app
```

---

### **Option 3: Traditional VPS/Shared Hosting**

```bash
# 1. SSH ke server
ssh user@your-server.com

# 2. Create folder
mkdir /var/www/dashboard-hub
cd /var/www/dashboard-hub

# 3. Upload files (via SCP)
scp -r ./* user@server:/var/www/dashboard-hub/

# 4. Configure web server (Nginx/Apache)
# Point domain ke folder ini

# 5. Done! Access via: https://dashboard.company.com
```

**Nginx config example:**
```nginx
server {
    listen 443 ssl http2;
    server_name dashboard.company.com;
    
    root /var/www/dashboard-hub;
    index index.html;
    
    # GZIP compression
    gzip on;
    gzip_types text/html text/css application/javascript;
    
    # Cache headers
    location ~* \.(html|css|js)$ {
        expires 1h;
        add_header Cache-Control "public, must-revalidate";
    }
    
    # Fallback untuk SPA routing (if needed)
    try_files $uri $uri/ /index.html;
}
```

---

## ⚙️ Features

✅ **Multi-Dashboard Support** - Easy switch antar dashboard via sidebar  
✅ **Iframe Isolation** - Dashboard isolated dari hub, tidak saling interrupt  
✅ **Real-time Clock** - Timestamp display update every second  
✅ **Refresh Functionality** - Reload dashboard tanpa reload hub  
✅ **Keyboard Shortcuts**:
- `Ctrl/Cmd + 1` → Switch to CJE0
- `Ctrl/Cmd + 2` → Switch to Pengadaan  
- `Ctrl/Cmd + 3` → Switch to Infrastructure
- `Ctrl/Cmd + R` → Refresh dashboard

✅ **Persistent Selection** - Remember last dashboard via localStorage  
✅ **Responsive Design** - Works on desktop, tablet, mobile  
✅ **Professional UI** - Modern design dengan Teal color scheme  

---

## 🔧 Customization

### **Add New Dashboard**

1. Copy new dashboard HTML ke `dashboards/new-dashboard.html`

2. Update `index.html` - tambah di section script (bagian `dashboards` object):
```javascript
const dashboards = {
    // ... existing dashboards ...
    newdash: {
        path: 'dashboards/new-dashboard.html',
        title: 'New Dashboard Title',
        description: 'Description here'
    }
};
```

3. Tambah nav item di HTML (sebelum `</div>` yang close `.sidebar`):
```html
<div class="nav-item" data-dashboard="newdash" data-title="New Dashboard Title">
    <span class="nav-icon">🆕</span>
    <span>New Dashboard</span>
</div>
```

4. Update keyboard shortcuts di script jika diperlukan:
```javascript
if (e.key === '4') loadDashboard('newdash');
```

---

### **Change Color Scheme**

Di bagian CSS header:
```css
.header {
    background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%);
    /* Change #0D9488 dan #0F766E ke color hex kamu */
}
```

Common colors:
- **BRI Green:** `#0D9488` (current)
- **Blue:** `#0066CC`
- **Purple:** `#7C3AED`
- **Orange:** `#EA580C`

---

### **Add Logo/Branding**

Modify header section di `index.html`:
```html
<div class="header">
    <div>
        <img src="logo.png" height="40" style="margin-right: 12px; vertical-align: middle;" alt="Logo">
        <div class="header-title">Dashboard Hub</div>
        ...
    </div>
</div>
```

---

## 🛡️ Security Notes

✅ **No API Keys Exposed** - Chart.js dan library sudah embedded  
✅ **HTTPS Auto** - GitHub Pages/Vercel provide free SSL  
✅ **Sandbox Isolation** - Iframe punya sandbox attribute untuk security  
✅ **No External CDN Risk** - Semua resources sudah embedded dalam dashboard files  

---

## 📊 Future Enhancements

### **Auto-Refresh Dashboard Data**

Add GitHub Actions untuk auto-generate dashboard dari SAP:

```yaml
# .github/workflows/update-dashboards.yml
name: Update Dashboards
on:
  schedule:
    - cron: '0 * * * *'  # Every hour

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run SAP sync script
        run: python scripts/sync_sap_data.py
      - name: Commit & push
        run: |
          git config user.name "Dashboard Bot"
          git config user.email "bot@bri.com"
          git add dashboards/
          git commit -m "Auto-update: Dashboards $(date)"
          git push
```

---

### **Add Real-time Data via WebSocket**

Jika dashboard perlu real-time sync dari backend:

```javascript
// Di index.html script section
const ws = new WebSocket('wss://your-api.com/dashboards');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    // Broadcast ke iframe
    iframeEl.contentWindow.postMessage(data, '*');
};
```

---

## 📱 Mobile Optimization

Responsive design sudah included. Di mobile:
- Sidebar berubah jadi horizontal tab
- Touch-friendly navigation
- Optimized spacing & font sizes

---

## 🚨 Troubleshooting

### **Dashboard tidak muncul di iframe**

- Check browser console (F12) untuk CORS errors
- Pastikan file path di `dashboards/` benar
- Cek localStorage jika issue persist: `localStorage.clear()`

### **Sidebar tidak responsive**

- Clear browser cache: `Ctrl+Shift+Delete`
- Check media queries di CSS

### **Keyboard shortcuts tidak work**

- Pastikan focus bukan di iframe (click di header dulu)
- Test di browser yang berbeda

---

## 📝 Usage Examples

**For Internal Sharing:**
```
https://dashboard.bandobrothers.com
→ Share link dengan colleagues
→ Mereka bisa akses semua 3 dashboard dari 1 URL
```

**For Executive Reports:**
```
CJE0 → Share untuk budget review
Pengadaan → Share untuk procurement status
INF → Share untuk infrastructure health check
```

---

## 📞 Support

Issues atau questions? Update README ini atau contact Pak Robi.

---

**Version:** 1.0  
**Last Updated:** 2026-03-25  
**Status:** ✅ Production Ready
