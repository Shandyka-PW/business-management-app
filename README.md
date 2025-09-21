Business Management App
Aplikasi manajemen bisnis offline yang lengkap untuk Windows. Dibangun dengan Python dan Tkinter, menggunakan database SQLite untuk penyimpanan data offline.

Fitur Utama
✅ Fitur yang Sudah Tersedia:
Sistem Lisensi - Proteksi dengan hardware ID untuk Windows
Manajemen Pelanggan - CRUD lengkap untuk data pelanggan
Manajemen Produk - CRUD lengkap untuk data produk dengan stok
Manajemen Order - Sistem pemesanan dengan tracking status
Dashboard - Overview bisnis dengan statistik real-time
Backup/Restore - Sistem backup database yang fleksibel
GUI Modern - Antarmuka yang user-friendly dengan Tkinter
🚧 Fitur dalam Pengembangan:
Manajemen Proses - Tracking proses bisnis
Manajemen Keuangan - Pencatatan transaksi keuangan
Pembuatan Nota - Generate invoice untuk pelanggan
Laporan - Berbagai laporan bisnis
Export Data - Export ke Excel/PDF
Persyaratan Sistem
Windows 7 atau lebih baru
Python 3.7+ (untuk development)
100MB ruang disk kosong
512MB RAM
Instalasi
Untuk Developer:
Clone atau download repository
Install dependencies:
bash

Line Wrapping

Collapse
Copy
1
pip install -r requirements.txt
Jalankan aplikasi:
bash

Line Wrapping

Collapse
Copy
1
python main.py
Untuk End User:
Download file installer
Ekstrak ke direktori yang diinginkan
Jalankan install.bat
Ikuti proses aktivasi lisensi
Aktivasi Lisensi
Aplikasi ini menggunakan sistem lisensi berbasis hardware ID:

Lisensi Demo:
Gunakan kode lisensi demo: DEMO-KEY-1234-5678

Lisensi Penuh:
Jalankan aplikasi
Catat Hardware ID yang ditampilkan
Kirim Hardware ID ke administrator untuk mendapatkan lisensi
Masukkan kode lisensi yang diberikan
Aplikasi siap digunakan
Panduan Penggunaan
1. Dashboard
Menampilkan overview bisnis
Statistik pelanggan, produk, order, dan revenue
Recent activities
2. Manajemen Pelanggan
Tambah pelanggan baru
Edit data pelanggan
Hapus pelanggan
Pencarian pelanggan
3. Manajemen Produk
Tambah produk baru
Edit informasi produk
Update stok produk
Kategorisasi produk
Pencarian produk
4. Manajemen Order
Buat order baru
Tambah item ke order
Tracking status order
Pembayaran order
Filter order berdasarkan status
5. Backup Database
Backup manual melalui menu File → Backup Database
Restore database dari backup
Auto-backup bisa diaktifkan di settings
Struktur Database
Aplikasi menggunakan SQLite dengan struktur tabel berikut:

customers - Data pelanggan
products - Data produk
orders - Data order/pemesanan
order_items - Item dalam order
processes - Proses bisnis
financial_transactions - Transaksi keuangan
invoices - Data invoice
settings - Pengaturan aplikasi
Build Executable
Untuk membuat file .exe:

Jalankan script build:
bash

Line Wrapping

Collapse
Copy
1
python build.py
Tunggu proses build selesai
File executable akan berada di dist/BusinessManagementApp.exe
Package installer ada di folder installer/
Konfigurasi
File konfigurasi disimpan di:

config.json - Konfigurasi utama
%APPDATA%\BusinessManagementApp\ - Data aplikasi
Database: %APPDATA%\BusinessManagementApp\business.db
Troubleshooting
Masalah Umum:
Lisensi tidak valid
Pastikan kode lisensi benar
Cek Hardware ID sesuai dengan komputer
Hubungi administrator untuk lisensi baru
Database error
Cek izin akses folder
Restore dari backup jika perlu
Pastikan tidak ada aplikasi lain yang mengakses database
GUI tidak muncul
Pastikan Python terinstall dengan benar
Cek dependencies Tkinter
Jalankan sebagai administrator jika perlu
Log Error:
Log aplikasi disimpan di logs/business_app_YYYYMMDD.log

Development
Struktur Proyek:

Line Wrapping

Collapse
Copy
1
2
3
4
5
6
7
8
9
10
11
12
13
business-management-app/
├── src/
│   ├── controllers/     # Logic controllers
│   ├── models/         # Data models
│   ├── views/          # GUI components
│   └── utils/          # Utility functions
├── database/           # Database files
├── resources/          # Icons and assets
├── backup/            # Backup files
├── logs/              # Log files
├── main.py            # Entry point
├── build.py           # Build script
└── requirements.txt   # Dependencies
Menambah Fitur Baru:
Buat model di src/models/
Buat controller di src/controllers/
Buat view di src/views/
Integrasikan ke MainWindow
Update database schema jika perlu
License
Aplikasi ini dilindungi oleh sistem lisensi. Penggunaan tanpa lisensi yang valid tidak diizinkan.

Support
Untuk support dan pertanyaan:

Email: shandyka@queenbee.biz.id
Documentation: Lihat folder docs/
Issues: Report via aplikasi
Changelog
v1.0.0 (Current)
✅ Sistem lisensi dengan hardware ID
✅ Manajemen pelanggan lengkap
✅ Manajemen produk dengan stok
✅ Manajemen order dasar
✅ Dashboard dengan statistik
✅ Backup/restore database
✅ GUI modern dengan Tkinter
Roadmap v1.1.0:
🚧 Manajemen proses bisnis
🚧 Sistem keuangan lengkap
🚧 Pembuatan invoice/nota
🚧 Export laporan
🚧 Multi-user support
© 2024 Business Management App. All rights reserved.