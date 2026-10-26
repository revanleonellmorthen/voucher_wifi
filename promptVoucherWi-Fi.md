# DOKUMENTASI PROYEK — VOUCHER WIFI (PROTOTYPE)

> **Tujuan dokumen:** Handoff lengkap agar AI/senior engineer baru dapat melanjutkan proyek **tanpa perlu membaca ulang chat sebelumnya**. Semua keputusan, aturan, dan status sudah final kecuali ditandai **TBD**.

---

## 1. IDENTITAS PROYEK

| Item | Nilai |
|---|---|
| Nama | **voucher_wifi** |
| Deskripsi | Sistem voucher WiFi dengan **CLI** (admin/kasir) + **captive portal** (customer) untuk area gedung |
| Target pengguna | Pengunjung gedung yang ingin internet cepat; kasir/admin sebagai operator |
| Teknologi | Python 3.11+, MySQL 8.0, Flask |
| Target akhir | **Prototype** |
| Metode kerja | Vibe Coding — bertahap, per roadmap, tidak melompat tahap |

---

## 2. ATURAN KERJA (WAJIB DIPATUHI AI BARU)

1. Jangan langsung membuat seluruh aplikasi sekaligus.
2. Kerjakan per tahap sesuai roadmap.
3. Pahami kebutuhan & aturan bisnis sebelum menulis kode.
4. Jangan mengarang kebutuhan baru — tanyakan jika belum jelas.
5. Gunakan solusi **sederhana, maintainable, sesuai kebutuhan**.
6. Jangan ubah fitur/arsitektur tanpa alasan jelas.
7. Perhatikan keamanan, validasi input, error handling, konsistensi DB.
8. Sertakan testing yang relevan tiap fitur.
9. Jangan klaim kode sudah diuji jika belum dijalankan.
10. Jangan lanjut tahap berikutnya sebelum tahap saat ini selesai & ditinjau.

**Format jawaban AI:** Tujuan tahap → Langkah → Hasil/file → Cara verifikasi → Masalah/keputusan yang masih diperlukan.

---

## 3. ROADMAP & STATUS

| # | Tahap | Status |
|---|---|---|
| 1 | Analisis kebutuhan & masalah | ✅ **SELESAI** |
| 2 | Spesifikasi, user flow, aturan bisnis | ✅ **SELESAI** |
| 3 | Arsitektur & teknologi | ✅ **SELESAI** |
| 4 | Struktur folder & DDL database | ✅ **SELESAI** |
| 5 | Implementasi fitur bertahap | 🔨 **BERJALAN** — 5a ✅, 5b–5d belum |
| 6 | Testing & debugging | ⏳ Belum |
| 7 | Review keamanan & kualitas | ⏳ Belum |
| 8 | Dokumentasi & deployment | ⏳ Belum |

---

## 4. KEPUTUSAN BISNIS FINAL (Tahap 1)

| Aspek | Keputusan |
|---|---|
| Aktor | **Admin**, **Kasir** (via CLI), **Customer** (via portal web) |
| Akses CLI | Hanya Admin & Kasir. Customer **tidak** menyentuh CLI |
| Alur penjualan voucher | **Flow B (On-demand)** — voucher di-generate saat kasir memproses pembayaran |
| Masa aktif voucher | Mulai **saat pembelian/pembayaran** |
| Paket voucher | **12 jam – Rp5.000** & **24 jam – Rp7.000** (hardcoded seed; CRUD paket **deferred**) |
| Definisi "terpakai" | **B3** — voucher yang **pernah divalidasi** di portal (≥1 baris di `sesi_voucher`) |
| Model konsumsi | **K2 (multi-sesi)** — voucher bisa divalidasi berkali-kali selama masih `AKTIF` |
| Status voucher | `AKTIF` & `KEDALUWARSA` — **dihitung**, **tidak disimpan** sebagai kolom |
| Integrasi router | **TIDAK ADA** (out of scope) — portal hanya gerbang validasi, tidak membuka internet |
| Definisi "sesi" di `sesi_voucher` | = **log pemakaian**, bukan sesi aktif/berakhir (konsekuensi tanpa router) |
| Web framework | **Flask** |
| URL portal | `http://localhost:5000` (lokal saja untuk prototype) |

### Di Luar Scope (Out of Scope)
- Integrasi router / captive portal yang benar-benar membuka internet
- Payment gateway
- CRUD paket (M-05) & kelola user (M-06) — **deferred**
- Web admin/kasir (mereka pakai CLI)
- Manajemen stok voucher massal

---

## 5. ATURAN BISNIS (BR) — ACUAN IMPLEMENTASI & TEST CASE

| Kode | Aturan |
|---|---|
| **BR-01** | Kode voucher unik, format **8 karakter uppercase alfanumerik**, hindari `0/O/1/I/L`. Unik di DB (constraint). Generate pakai `secrets`, **bukan** `random`. |
| **BR-02** | `waktu_kedaluwarsa = waktu_beli + durasi_jam(paket)`. Diisi saat insert, **tidak berubah**. |
| **BR-03** | Status voucher **dihitung**: `AKTIF` jika `NOW() < waktu_kedaluwarsa`, selain itu `KEDALUWARSA`. **Tidak disimpan** sebagai kolom. |
| **BR-04** | Voucher hanya bisa divalidasi sukses di portal jika berstatus `AKTIF`. |
| **BR-05** | Setiap validasi **sukses** di portal dicatat ke `sesi_voucher` (1 baris per validasi). |
| **BR-06** | Voucher multi-sesi: **tidak dibatasi** jumlah validasi selama status `AKTIF`. |
| **BR-07** | Definisi "terpakai" untuk laporan = voucher **memiliki ≥1 baris** di `sesi_voucher`. |
| **BR-08** | Laporan harian: `terjual` dihitung dari `DATE(waktu_beli)`, `terpakai` dihitung dari `DATE(validated_at)` **pertama**. |
| **BR-09** | Role `kasir` **tidak boleh** mengakses M-05 / M-06 (dicek di level menu, bukan hanya UI). |
| **BR-10** | Rate limit portal: **maks 5 percobaan validasi per IP per menit**. |
| **BR-11** | Password user di-hash pakai **bcrypt**. Plain password tidak pernah disimpan. |
| **BR-12** | Paket & user di-**seed** manual untuk iterasi 1 (karena M-05/M-06 di-defer). |

---

## 6. MODUL & FITUR

### CLI (Admin & Kasir)

| Kode | Fitur | Admin | Kasir |
|---|---|---|---|
| M-01 | Login / Logout | ✅ | ✅ |
| M-02 | Jual voucher (on-demand) | ✅ | ✅ |
| M-03 | Cek status voucher (by kode) | ✅ | ✅ |
| M-04 | Laporan harian (terjual vs terpakai, dipisah per paket) | ✅ | ✅ (harian) |
| M-05 | CRUD paket | ⏸ **deferred** | ❌ |
| M-06 | Kelola user | ⏸ **deferred** | ❌ |

### Captive Portal (Customer)

| Kode | Fitur |
|---|---|
| P-01 | Halaman form input kode voucher |
| P-02 | Validasi kode → tampilkan `AKTIF` / `KEDALUWARSA` / `TIDAK DITEMUKAN` |
| P-03 | Bila `AKTIF`: tampilkan paket, sisa masa aktif, pesan sukses |
| P-04 | Mencatat setiap validasi sukses ke `sesi_voucher` |
| P-05 | Rate limit sederhana per IP (BR-10) |

---

## 7. USER FLOW (RINGKAS)

**Login CLI:**
`jalankan CLI → prompt username/password → validasi ke users → menu sesuai role` (gagal maks 3x → keluar).

**Jual Voucher (Flow B):**
`menu → pilih paket → generate kode unik → waktu_kedaluwarsa = now + durasi → simpan → tampilkan kode ke layar`.

**Cek Voucher:**
`input kode → cari di DB → hitung status dari waktu_kedaluwarsa → tampilkan detail`.

**Portal (Customer):**
`buka http://localhost:5000 → input kode → cek rate limit → validasi format → cari voucher → AKTIF: insert sesi_voucher + tampilkan sukses | KEDALUWARSA/tidak ada: pesan sesuai`.

**Laporan Harian:**
`input tanggal (default hari ini) → query agregat terjual (by waktu_beli) & terpakai (by sesi pertama) → tampilkan per paket`.

---

## 8. ARSITEKTUR (Tahap 3)

### Stack Final

| Komponen | Pilihan |
|---|---|
| Bahasa | Python 3.11+ |
| DB Driver | **PyMySQL ≥1.1** (bukan mysql-connector) |
| Web framework | **Flask ≥3.0** |
| Hash password | **bcrypt ≥4.0** |
| Konfigurasi | **python-dotenv ≥1.0** |
| Tabel CLI | **tabulate ≥0.9** |
| Testing | **pytest ≥8.0** |
| WSGI | Flask dev server (prototype lokal) |
| Dependency | `pip` + `requirements.txt` |
| **ORM** | **TIDAK PAKAI** — query SQL eksplisit |
| MySQL | **Docker Compose** (`mysql:8.0`) |

### Pola Layer (ditegakkan)

```
CLI ──┐              ┌── Portal (Flask)
      └──► core/ ────┘   ← semua BR-01..BR-12 di sini
              │
              ▼
           db.py ──── MySQL
```

- **`core/`** = satu-satunya tempat aturan bisnis, dipanggil CLI **dan** Portal (tanpa duplikasi).
- **`db.py`** = wrapper koneksi + `fetch_one`, `fetch_all`, `execute`.
- CLI & Portal **tidak boleh** import `db.py` langsung — hanya lewat `core/`.
- Koneksi **per unit kerja** (per perintah CLI / per-request), bukan pool. Autocommit OFF, commit eksplisit per operasi tulis.
- Cursor `DictCursor`.
- **Timezone:** semua `DATETIME` = waktu lokal server (asumsi 1 mesin).

### Konfigurasi `.env` (kunci wajib)

```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=voucher_app
DB_PASS=change_me
DB_NAME=voucher_wifi

FLASK_SECRET_KEY=change_me_random
FLASK_HOST=127.0.0.1
FLASK_PORT=5000

PORTAL_RATE_LIMIT=5
```

`.env.example` disertakan; `.env` **di-ignore**. Aplikasi **gagal cepat** bila variabel wajib tidak ada.

### Strategi Testing

- **L1 (unit, `core/`):** kode_generator, voucher_service, laporan_service, rate_limiter — tanpa DB (mock/inject).
- **L2 (integration DB):** ditunda ke **Tahap 6**.
- **L3 (portal smoke):** Flask test client untuk route validasi.
- Konvensi: `tests/test_*.py`, satu file per modul.

### Entry Point

| Peran | Perintah |
|---|---|
| CLI | `python -m voucher_wifi.cli` |
| Portal | `flask --app voucher_wifi.portal run --host 127.0.0.1 --port 5000` |
| Seed user | `python scripts/seed_users.py --username … --password … --role …` |
| Seed schema/paket | otomatis via Docker init script |

---

## 9. STRUKTUR FOLDER (Tahap 4)

```
voucher_wifi/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── docker-compose.yml
├── pytest.ini
│
├── sql/
│   ├── schema.sql
│   └── seed.sql
│
├── scripts/
│   └── seed_users.py
│
├── voucher_wifi/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── kode_generator.py
│   │   ├── voucher_service.py
│   │   ├── laporan_service.py
│   │   └── rate_limiter.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── menus.py
│   │   └── views.py
│   └── portal/
│       ├── __init__.py
│       ├── __main__.py
│       ├── routes.py
│       ├── templates/
│       │   ├── base.html
│       │   ├── index.html
│       │   └── result.html
│       └── static/
│           └── style.css
│
└── tests/
    ├── __init__.py
    ├── test_kode_generator.py
    ├── test_voucher_service.py
    ├── test_laporan_service.py
    └── test_rate_limiter.py
```

**Aturan struktur:** `cli/` dan `portal/` **hanya** boleh import dari `core/`, tidak langsung `db.py`.

---

## 10. SKEMA DATABASE (FINAL — DDL di `sql/schema.sql`)

**Database:** `voucher_wifi` (utf8mb4)

### `users`
| Kolom | Tipe | Constraint |
|---|---|---|
| id | INT UNSIGNED | PK AUTO |
| username | VARCHAR(50) | NOT NULL, UNIQUE |
| password_hash | VARCHAR(255) | NOT NULL |
| role | ENUM('admin','kasir') | NOT NULL |
| aktif | BOOLEAN | DEFAULT TRUE |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### `paket`
| Kolom | Tipe | Constraint |
|---|---|---|
| id | INT UNSIGNED | PK AUTO |
| nama | VARCHAR(50) | NOT NULL |
| durasi_jam | INT UNSIGNED | NOT NULL |
| harga | INT UNSIGNED | NOT NULL (rupiah) |
| aktif | BOOLEAN | DEFAULT TRUE |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### `voucher` — **TIDAK ada kolom status** (BR-03)
| Kolom | Tipe | Constraint |
|---|---|---|
| id | INT UNSIGNED | PK AUTO |
| kode | VARCHAR(16) | NOT NULL, **UNIQUE** |
| paket_id | INT UNSIGNED | FK → paket.id |
| kasir_id | INT UNSIGNED | FK → users.id (audit trail) |
| waktu_beli | DATETIME | NOT NULL, indexed |
| waktu_kedaluwarsa | DATETIME | NOT NULL |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP |

### `sesi_voucher` — log pemakaian
| Kolom | Tipe | Constraint |
|---|---|---|
| id | INT UNSIGNED | PK AUTO |
| voucher_id | INT UNSIGNED | FK → voucher.id **ON DELETE CASCADE** |
| ip_address | VARCHAR(45) | NOT NULL |
| user_agent | VARCHAR(255) | NULL |
| validated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP, indexed |

### Seed `paket`
```sql
INSERT INTO paket (nama, durasi_jam, harga, aktif) VALUES
  ('12 Jam', 12, 5000, TRUE),
  ('24 Jam', 24, 7000, TRUE);
```

### Seed users
Dibuat via `scripts/seed_users.py` (bukan SQL) karena wajib bcrypt.

---

## 11. DOCKER COMPOSE

```yaml
services:
  db:
    image: mysql:8.0
    container_name: voucher_wifi_db
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: voucher_wifi
      MYSQL_USER: voucher_app
      MYSQL_PASSWORD: change_me
    ports: ["3306:3306"]
    volumes:
      - db_data:/var/lib/mysql
      - ./sql/schema.sql:/docker-entrypoint-initdb.d/01_schema.sql:ro
      - ./sql/seed.sql:/docker-entrypoint-initdb.d/02_seed.sql:ro
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "127.0.0.1", "-uroot", "-prootpass"]
      interval: 5s
      timeout: 5s
      retries: 10
volumes:
  db_data:
```

**Reset DB:** `docker compose down -v && docker compose up -d` (init script hanya jalan saat volume kosong).

---

## 12. KEAMANAN (ringkasan — detail di Tahap 7)

- Kode voucher pakai `secrets`, bukan `random` (bisa ditebak dari portal publik).
- Password: bcrypt.
- Portal: form POST, validasi regex format kode sebelum query DB.
- Rate limit in-memory dict per IP, reset tiap 60 detik (**bukan** Redis — prototype).
- Pesan error ke customer tidak membocorkan info berlebihan.
- `.env` di-ignore Git.
- Role `kasir` dicek di **level menu** (bukan hanya UI).

---

## 13. STATUS FILE (per akhir Tahap 5a)

| File | Status |
|---|---|
| `sql/schema.sql` | ✅ Ditulis penuh (Tahap 4) |
| `sql/seed.sql` | ✅ Ditulis penuh (Tahap 4) |
| `docker-compose.yml` | ✅ Ditulis penuh (Tahap 4) — tidak dipakai (Docker belum terpasang) |
| `.env.example`, `.gitignore`, `pytest.ini`, `requirements.txt` | ✅ Final (Tahap 4) |
| `README.md` | ✅ Diperbarui setelah 5a |
| `voucher_wifi/__init__.py` | ✅ Kosong (package marker) |
| `voucher_wifi/config.py` | ✅ 5a — load `.env` + gagal cepat + `DB_CONFIG` |
| `voucher_wifi/db.py` | ✅ 5a — `koneksi()`, `fetch_one`, `fetch_all`, `execute` |
| `voucher_wifi/core/__init__.py` | ✅ Kosong (package marker) |
| `voucher_wifi/core/kode_generator.py` | ✅ 5a — `buat_kode()`, `valid_format()` (BR-01) |
| `voucher_wifi/core/auth_service.py` | ✅ 5a — `authenticate()` (BR-11) |
| `voucher_wifi/core/voucher_service.py` | ❌ 5b |
| `voucher_wifi/core/laporan_service.py` | ❌ 5d |
| `voucher_wifi/core/rate_limiter.py` | ❌ 5c |
| `voucher_wifi/cli/*` | ❌ 5b |
| `voucher_wifi/portal/*` + template/CSS | ❌ 5c |
| `scripts/seed_users.py` | ✅ 5a — idempotent (`ON DUPLICATE KEY UPDATE`) |
| `tests/test_kode_generator.py`, `tests/test_auth_service.py` | ✅ 5a — 7 test lulus |

**Catatan 5a:** kode & unit test selesai dan lulus tanpa DB. Seed user ke DB **belum berhasil** karena MySQL lokal menolak login `voucher_app` (error 1045) — perlu perbaikan user/grant manual di luar repo.

---

## 14. RENCANA TAHAP 5 — IMPLEMENTASI BERTAHAP

Urutan yang disepakati (kerjakan berurutan, **tinjau per sub-tahap**):

| Sub | Isi | Status |
|---|---|---|
| **5a** | `config.py`, `db.py`, `core/kode_generator.py`, `core/auth_service.py`, `scripts/seed_users.py` (+ unit test) | ✅ **SELESAI** (kode + 7 test lulus; seed DB tertunda, lihat §13) |
| **5b** | `core/voucher_service.py` (jual, cek status) + CLI login → menu → jual & cek (+ unit test) | ⏳ **BERIKUTNYA** |
| **5c** | Portal Flask (P-01…P-05) + `core/rate_limiter.py` (+ unit test) | ⏳ Belum |
| **5d** | `core/laporan_service.py` + menu laporan CLI | ⏳ Belum |

**Status kode Python:** 5a sudah ada (lihat §13). 5b–5d belum.

---

## 15. KEPUTUSAN YANG MASIH TERBUKA (sebelum mulai 5a)

| # | Pertanyaan | Usulan |
|---|---|---|
| 1 | Akun seed default iterasi 1? | ✅ **DIPUTUSKAN:** `admin`/`admin` (role admin), `kasir1`/`kasir1` (role kasir) — prototype |
| 2 | Harga sebagai INT rupiah (bukan DECIMAL)? | Ya |
| 3 | Simpan `user_agent` di `sesi_voucher`? | Ya (untuk debug) |
| 4 | Lebar `kode` VARCHAR(16) (longgar) atau VARCHAR(8) (ketat)? | Longgar (future-proof) |
| 5 | Urutan sub-tahap 5a–5d? | Sesuai tabel §14 |

**Catatan:** Item 1 sudah dikonfirmasi user. Item 2–5 disetujui sesuai usulan.

---

## 16. CONTOH PERINTAH VERIFIKASI DB (untuk Tahap 5+)

```bash
docker compose up -d
docker compose ps
docker compose exec db mysql -uvoucher_app -pchange_me voucher_wifi -e "SHOW TABLES;"
docker compose exec db mysql -uvoucher_app -pchange_me voucher_wifi -e "SELECT * FROM paket;"
# Ekspektasi: users, paket, voucher, sesi_voucher + 2 baris paket
```

---

## 17. INSTRUKSI UNTUK AI DI CHAT BARU

1. Baca dokumen ini **seluruhnya** sebelum menjawab.
2. **Peran Anda:** Senior Software Engineer (Vibe Coding) + Project Manager pendamping.
3. **Tahap saat ini:** Tahap 5a **SELESAI** → siap masuk **Tahap 5b**.
4. **Langkah pertama Anda:** Konfirmasi izin masuk 5b, lalu implementasikan **hanya** file yang termasuk 5b. Akun seed sudah final (§15 item 1).
5. **Jangan** menulis kode di luar scope 5a. Jangan melompat ke 5b–5d.
6. **Selalu** pakai format jawaban §2 (Tujuan → Langkah → Hasil → Verifikasi → Masalah).
7. Jika user meminta perubahan scope, catat dampaknya terhadap **BR**, **skema**, dan **Tahap** — jangan mengubah diam-diam.
8. Semua file harus konsisten dengan §9 (struktur) dan §10 (DDL). Penyimpangan wajib dijustifikasi.
9. Testing wajib menyertai setiap fitur (unit test per modul `core/`).
10. Jangan klaim sudah diuji tanpa benar-benar dijalankan; tunjukkan perintah/argumen pengujian.

---

**Dokumen ini adalah source of truth. Jika ada konflik antara chat lama dan dokumen ini, dokumen ini yang menang.**