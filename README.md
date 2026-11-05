# Lab Equipment Loan System

Backend REST API untuk mengelola peminjaman alat laboratorium. Sistem mencatat master alat, transaksi peminjaman, pengembalian alat, dan riwayat peminjaman mahasiswa. Stok alat berkurang otomatis saat dipinjam dan pulih saat dikembalikan.

Dokumen kebutuhan dan rancangan ada di folder `markdown/`.

## Teknologi

- Python 3.x
- Flask
- SQLite
- JSON

## Struktur Proyek

```text
.
├── app/
│   ├── __init__.py          # application factory
│   ├── database.py          # koneksi SQLite, init-db
│   ├── errors.py            # error domain + JSON error handler
│   ├── schema.sql           # DDL tabel item dan loan
│   ├── validators.py        # validasi input
│   ├── routes/
│   │   ├── item_routes.py
│   │   └── loan_routes.py
│   ├── services/
│   │   ├── item_service.py
│   │   └── loan_service.py
│   └── repositories/
│       ├── item_repository.py
│       └── loan_repository.py
├── instance/                # database SQLite (dibuat otomatis)
├── markdown/                # dokumen requirement, PRD, arsitektur, tugas, review
├── tests/                   # pytest
├── run.py
└── README.md
```

## Instalasi

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r markdown/requirements.txt
```

Catatan: `requirements.txt` berada di `markdown/` mengikuti lokasi file saat ini.

## Menyiapkan Database

Database SQLite dibuat di `instance/lab_equipment.db`.

```bash
python -m flask --app run init-db
```

Perintah ini membuat tabel `item` dan `loan`. Jalankan sekali sebelum aplikasi dipakai. Database yang sudah ada tidak ditimpa.

## Menjalankan Aplikasi

```bash
python run.py
```

Server berjalan di `http://127.0.0.1:5000`.

Mode debug hanya aktif jika variabel lingkungan `FLASK_DEBUG=1`.

```bash
FLASK_DEBUG=1 python run.py
```

## Endpoint

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/items` | Daftar alat dan stok terkini |
| POST | `/items` | Tambah master alat |
| POST | `/loans` | Buat transaksi peminjaman |
| PUT | `/loans/{id}/return` | Kembalikan alat |
| GET | `/loans/student/{student_id}` | Riwayat pinjaman satu NIM |

Respons sukses memakai bentuk `{"data": ...}`. Respons error memakai bentuk `{"error": "..."}`.

### Contoh

Tambah alat:

```bash
curl -X POST http://127.0.0.1:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Multimeter", "total_stock": 10}'
```

Pinjam alat:

```bash
curl -X POST http://127.0.0.1:5000/loans \
  -H "Content-Type: application/json" \
  -d '{"student_id": "20240001", "item_id": 1, "quantity": 2}'
```

Kembalikan alat:

```bash
curl -X PUT http://127.0.0.1:5000/loans/1/return
```

Riwayat mahasiswa:

```bash
curl http://127.0.0.1:5000/loans/student/20240001
```

## Status Code

| Kondisi | Status |
|---|---|
| Input tidak valid | 400 Bad Request |
| Stok tidak mencukupi | 400 Bad Request |
| Transaksi sudah `RETURNED` | 400 Bad Request |
| Item atau transaksi tidak ditemukan | 404 Not Found |
| Item atau peminjaman berhasil dibuat | 201 Created |
| GET atau pengembalian berhasil | 200 OK |

## Pengujian

```bash
python -m pytest -v
```

Test memakai database SQLite sementara per test, sehingga database utama tidak tersentuh.

## Batasan

Autentikasi, otorisasi, pembatalan transaksi, jatuh tempo, denda, pagination, dan deployment production belum termasuk ruang lingkup. Lihat `markdown/architecture.md` bagian 10.
