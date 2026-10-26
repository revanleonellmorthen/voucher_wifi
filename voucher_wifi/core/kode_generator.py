"""BR-01: kode voucher 8 karakter uppercase alfanumerik, tanpa 0/O/1/I/L."""
import re
import secrets

ALFABET = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
PANJANG = 8
_POLA = re.compile(rf"[{ALFABET}]{{{PANJANG}}}")


def buat_kode():
    return "".join(secrets.choice(ALFABET) for _ in range(PANJANG))


def valid_format(kode):
    return bool(_POLA.fullmatch(kode or ""))
