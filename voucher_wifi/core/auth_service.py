"""BR-11: password bcrypt. Login + buat user (dipakai CLI & seed script)."""

import bcrypt
import pymysql.err

from .. import db

ROLE_VALID = ("admin", "kasir")
MAX_PASSWORD_BYTE = 72  # batas keras bcrypt

_SQL_CARI = "SELECT id, username, password_hash, role, aktif FROM users WHERE username = %s"
_SQL_INSERT = "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)"


def login(username, password):
    """Kembalikan dict user tanpa hash bila kredensial valid dan user aktif."""
    user = db.fetch_one(_SQL_CARI, (username,))
    if not user or not user["aktif"]:
        return None
    if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return None
    return {"id": user["id"], "username": user["username"], "role": user["role"]}


def buat_user(username, password, role):
    if role not in ROLE_VALID:
        raise ValueError(f"role harus salah satu dari {ROLE_VALID}")
    if not username.strip():
        raise ValueError("username tidak boleh kosong")
    pw = password.encode()
    if not pw:
        raise ValueError("password tidak boleh kosong")
    if len(pw) > MAX_PASSWORD_BYTE:
        raise ValueError(f"password maksimal {MAX_PASSWORD_BYTE} byte")

    password_hash = bcrypt.hashpw(pw, bcrypt.gensalt()).decode()
    try:
        return db.execute(_SQL_INSERT, (username, password_hash, role))
    except pymysql.err.IntegrityError as e:
        raise ValueError(f"username '{username}' sudah dipakai") from e
