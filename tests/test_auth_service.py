import bcrypt
import pytest

from voucher_wifi.core import auth_service

HASH = bcrypt.hashpw(b"rahasia", bcrypt.gensalt()).decode("utf-8")


class _Koneksi:
    def __enter__(self):
        return object()

    def __exit__(self, *exc):
        return False


@pytest.fixture
def db_palsu(monkeypatch):
    def pasang(user):
        monkeypatch.setattr(auth_service.db, "koneksi", lambda: _Koneksi())
        monkeypatch.setattr(
            auth_service.db, "fetch_one", lambda conn, sql, params=(): user
        )

    return pasang


def test_login_benar(db_palsu):
    db_palsu(
        {"id": 1, "username": "admin", "password_hash": HASH, "role": "admin"}
    )
    assert auth_service.authenticate("admin", "rahasia") == {
        "id": 1,
        "username": "admin",
        "role": "admin",
    }


def test_password_salah(db_palsu):
    db_palsu(
        {"id": 1, "username": "admin", "password_hash": HASH, "role": "admin"}
    )
    assert auth_service.authenticate("admin", "salah") is None


def test_user_tidak_ada(db_palsu):
    db_palsu(None)
    assert auth_service.authenticate("hantu", "rahasia") is None


def test_password_kepanjangan():
    assert auth_service.authenticate("admin", "x" * 73) is None
