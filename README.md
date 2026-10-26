# voucher_wifi

Sistem voucher WiFi: CLI untuk admin/kasir, captive portal untuk customer. Prototype lokal.

Stack: Python 3.11+, MySQL 8.0 (Docker), Flask, PyMySQL, bcrypt. Tanpa ORM.

## Setup

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

DB: pakai MySQL lokal yang sudah jalan (`MySQL80` service) — Docker belum terpasang di mesin ini.

```bash
mysql -uroot -p -e "create database voucher_wifi character set utf8mb4"
mysql -uroot -p voucher_wifi < sql/schema.sql
mysql -uroot -p voucher_wifi < sql/seed.sql
```

`docker-compose.yml` disimpan untuk nanti kalau Docker terpasang: `docker compose up -d`.

## Status

Tahap 1-5a selesai. 5a: `config.py`, `db.py`, `core/kode_generator.py`, `core/auth_service.py`,
`scripts/seed_users.py` + unit test (24 passed).

Tahap 5b berikutnya: `core/voucher_service.py` (jual, cek status) + CLI login → menu → jual & cek.

Dokumen acuan: `promptVoucherWi-Fi.md`.
