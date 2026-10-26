"""Konfigurasi dari .env. Gagal cepat bila variabel wajib hilang."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

_WAJIB = (
    "DB_HOST",
    "DB_PORT",
    "DB_USER",
    "DB_PASS",
    "DB_NAME",
    "FLASK_SECRET_KEY",
    "FLASK_HOST",
    "FLASK_PORT",
    "PORTAL_RATE_LIMIT",
)

_hilang = [k for k in _WAJIB if not os.environ.get(k)]
if _hilang:
    raise RuntimeError(f"Variabel .env belum diset: {', '.join(_hilang)}")

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": int(os.environ["DB_PORT"]),
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASS"],
    "database": os.environ["DB_NAME"],
    "charset": "utf8mb4",
}
