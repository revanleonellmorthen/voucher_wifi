"""Autentikasi user (BR-11: password bcrypt)."""
import bcrypt

from .. import db


def authenticate(username, password):
    """Return {id, username, role} bila valid, None bila gagal."""
    # bcrypt hanya memakai 72 byte pertama; tolak lebih awal supaya tidak menyesatkan.
    if not username or not password or len(password.encode("utf-8")) > 72:
        return None

    with db.koneksi() as conn:
        user = db.fetch_one(
            conn,
            "SELECT id, username, password_hash, role FROM users"
            " WHERE username = %s AND aktif = TRUE",
            (username,),
        )

    if user is None:
        return None
    if not bcrypt.checkpw(
        password.encode("utf-8"), user["password_hash"].encode("utf-8")
    ):
        return None
    return {"id": user["id"], "username": user["username"], "role": user["role"]}
