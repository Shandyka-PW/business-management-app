---

````markdown
# Business Management App

**Aplikasi manajemen bisnis offline yang lengkap untuk Windows.**  
Dibangun dengan **Python** dan **Tkinter**, menggunakan **SQLite** sebagai database offline yang ringan namun andal.

---

## ✨ Fitur Utama

### ✅ Fitur Tersedia
- **Sistem Lisensi** – Proteksi dengan Hardware ID untuk Windows  
- **Manajemen Pelanggan** – CRUD lengkap untuk data pelanggan  
- **Manajemen Produk** – CRUD lengkap untuk data produk dengan stok  
- **Manajemen Order** – Sistem pemesanan dengan tracking status  
- **Dashboard** – Overview bisnis dengan statistik real-time  
- **Backup/Restore** – Sistem backup database yang fleksibel  
- **GUI Modern** – Antarmuka user-friendly dengan Tkinter  

### 🚧 Fitur dalam Pengembangan
- **Manajemen Proses** – Tracking proses bisnis  
- **Manajemen Keuangan** – Pencatatan transaksi keuangan  
- **Pembuatan Nota** – Generate invoice untuk pelanggan  
- **Laporan** – Berbagai laporan bisnis  
- **Export Data** – Ekspor ke Excel/PDF  

---

## 🖥 Persyaratan Sistem
- Windows 7 atau lebih baru  
- Python 3.7+ (untuk development)  
- Ruang disk kosong minimal **100 MB**  
- RAM minimal **512 MB**  

---

## ⚙️ Instalasi

### Untuk Developer
1. Clone atau download repository  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
````

3. Jalankan aplikasi:

   ```bash
   python main.py
   ```

### Untuk End User

1. Download file installer
2. Ekstrak ke direktori yang diinginkan
3. Jalankan `install.bat`
4. Ikuti proses aktivasi lisensi

---

## 🔑 Aktivasi Lisensi

Aplikasi ini menggunakan sistem lisensi berbasis Hardware ID.

**Lisensi Demo**

* Gunakan kode lisensi demo:

  ```
  DEMO-KEY-1234-5678
  ```

**Lisensi Penuh**

1. Jalankan aplikasi
2. Catat Hardware ID yang ditampilkan
3. Kirim Hardware ID ke administrator untuk mendapatkan lisensi
4. Masukkan kode lisensi yang diberikan
5. Aplikasi siap digunakan

---

## 📘 Panduan Penggunaan

### 1. Dashboard

* Overview bisnis
* Statistik pelanggan, produk, order, dan revenue
* Recent activities

### 2. Manajemen Pelanggan

* Tambah, edit, hapus, dan cari data pelanggan

### 3. Manajemen Produk

* Tambah produk baru
* Edit informasi produk
* Update stok
* Kategorisasi produk
* Pencarian produk

### 4. Manajemen Order

* Buat order baru
* Tambah item ke order
* Tracking status order
* Pembayaran order
* Filter order berdasarkan status

### 5. Backup Database

* Backup manual melalui menu **File → Backup Database**
* Restore dari backup
* Auto-backup (opsional)

---

## 🗄 Struktur Database

Menggunakan **SQLite** dengan tabel:

* `customers` – Data pelanggan
* `products` – Data produk
* `orders` – Data pemesanan
* `order_items` – Item dalam order
* `processes` – Proses bisnis
* `financial_transactions` – Transaksi keuangan
* `invoices` – Data invoice
* `settings` – Pengaturan aplikasi

---

## 📦 Build Executable

Untuk membuat file `.exe`:

```bash
python build.py
```

* File executable: `dist/BusinessManagementApp.exe`
* Package installer: `installer/`

---

## ⚙️ Konfigurasi

* File konfigurasi utama: `config.json`
* Lokasi data aplikasi:

  ```
  %APPDATA%\BusinessManagementApp\
  ```
* Database:

  ```
  %APPDATA%\BusinessManagementApp\business.db
  ```

---

## 🛠 Troubleshooting

**Lisensi tidak valid**

* Pastikan kode lisensi benar
* Cocokkan Hardware ID
* Hubungi administrator untuk lisensi baru

**Database error**

* Cek izin akses folder
* Restore dari backup jika perlu
* Pastikan tidak ada aplikasi lain yang mengakses database

**GUI tidak muncul**

* Pastikan Python terinstal
* Cek dependencies Tkinter
* Jalankan sebagai administrator

**Log Error**
Tersimpan di: `logs/business_app_YYYYMMDD.log`

---

## 📂 Struktur Proyek

```
business-management-app/
├── src/
│   ├── controllers/     # Logic controllers
│   ├── models/          # Data models
│   ├── views/           # GUI components
│   └── utils/           # Utility functions
├── database/            # Database files
├── resources/           # Icons and assets
├── backup/              # Backup files
├── logs/                # Log files
├── main.py              # Entry point
├── build.py             # Build script
└── requirements.txt     # Dependencies
```

**Menambah Fitur Baru**

1. Buat model di `src/models/`
2. Buat controller di `src/controllers/`
3. Buat view di `src/views/`
4. Integrasikan ke `MainWindow`
5. Update database schema jika diperlukan

---

## 📜 License

Aplikasi ini dilindungi oleh sistem lisensi.
Penggunaan tanpa lisensi yang valid **tidak diizinkan**.

---

## 💬 Support

* Email: **[shandyka@queenbee.biz.id](mailto:shandyka@queenbee.biz.id)**
* Dokumentasi: folder `docs/`
* Issues: report via aplikasi

---

## 📝 Changelog

### v1.0.0 (Current)

* ✅ Sistem lisensi berbasis Hardware ID
* ✅ Manajemen pelanggan lengkap
* ✅ Manajemen produk dengan stok
* ✅ Manajemen order dasar
* ✅ Dashboard dengan statistik
* ✅ Backup/restore database
* ✅ GUI modern dengan Tkinter

### Roadmap v1.1.0

* 🚧 Manajemen proses bisnis
* 🚧 Sistem keuangan lengkap
* 🚧 Pembuatan invoice/nota
* 🚧 Export laporan
* 🚧 Multi-user support

---

© 2025 Business Management App — All rights reserved.

```

```
