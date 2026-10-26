"""Konfigurasi dari .env. Gagal cepat bila variabel wajib tidak ada."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _wajib(nama: str) -> str:
    nilai = os.environ.get(nama)
    if not nilai:
        raise RuntimeError(f"Variabel .env wajib tidak ada: {nama}")
    return nilai


DB_HOST = _wajib("DB_HOST")
DB_PORT = int(_wajib("DB_PORT"))
DB_USER = _wajib("DB_USER")
DB_PASS = _wajib("DB_PASS")
DB_NAME = _wajib("DB_NAME")

FLASK_SECRET_KEY = _wajib("FLASK_SECRET_KEY")
FLASK_HOST = _wajib("FLASK_HOST")
FLASK_PORT = int(_wajib("FLASK_PORT"))

PORTAL_RATE_LIMIT = int(_wajib("PORTAL_RATE_LIMIT"))
