"""BR-01: kode voucher 8 karakter uppercase, tanpa 0/O/1/I/L, pakai secrets."""

import re
import secrets

ALFABET = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
PANJANG = 8
POLA = re.compile(r"^[2-9A-HJ-KM-NP-Z]{8}$")


def buat_kode() -> str:
    return "".join(secrets.choice(ALFABET) for _ in range(PANJANG))


def valid_format(kode) -> bool:
    """Caller wajib strip + upper dulu; fungsi ini strict."""
    return bool(kode) and POLA.match(kode) is not None
