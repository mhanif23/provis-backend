# API DigiSehat

API DigiSehat adalah backend sistem yang dirancang untuk mengelola data kesehatan. Dibangun dengan FastAPI, proyek ini menyediakan endpoints untuk autentikasi pengguna, manajemen data dokter, pasien, dan obat.

## Fitur

- Autentikasi dan Manajemen Pengguna
- CRUD untuk dokter, pasien, dan obat
- Manajemen diagnosis dan resep
- Tracking order dan jadwal konsultasi

## Teknologi

Proyek ini menggunakan beberapa teknologi dan libraries berikut:

- FastAPI
- Uvicorn sebagai server ASGI
- SQLAlchemy untuk ORM
- Pydantic untuk validasi data
- SQLite untuk database
- Bcrypt untuk hashing password
- JOSE untuk token JWT

## Instalasi

Ikuti langkah-langkah berikut untuk melakukan setup project secara lokal:

### Prasyarat

Pastikan Python 3.6+ sudah terinstal pada sistem Anda. Anda juga perlu pip untuk mengelola pustaka Python.

### Langkah 1: Klon Repositori

Klon repositori ini menggunakan git:

```bash
git clone https://github.com/<username>/api-digisehat.git
cd api-digisehat
```

### Langkah 2: Instal Dependencies
Instal semua dependencies yang diperlukan dengan pip:

```bash
pip install -r requirements.txt
```

### Langkah 3: Jalankan Server
Jalankan server FastAPI menggunakan uvicorn:

```bash
python uvicorn main:app --reload
```

Server akan tersedia di http://127.0.0.1:8000.

### Penggunaan
Setelah server berjalan, Anda bisa mengakses dokumentasi API di http://127.0.0.1:8000/docs yang menyediakan antarmuka Swagger untuk mencoba API secara langsung.