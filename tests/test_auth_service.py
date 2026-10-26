import bcrypt
import pymysql.err
import pytest

from voucher_wifi import db
from voucher_wifi.core import auth_service


def _user(password="rahasia", aktif=1):
    return {
        "id": 1,
        "username": "admin",
        "password_hash": bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
        "role": "admin",
        "aktif": aktif,
    }


@pytest.fixture
def patched_fetch(monkeypatch):
    def pasang(hasil):
        monkeypatch.setattr(db, "fetch_one", lambda sql, params=(): hasil)

    return pasang


def test_login_sukses_tanpa_hash(patched_fetch):
    patched_fetch(_user())
    hasil = auth_service.login("admin", "rahasia")
    assert hasil == {"id": 1, "username": "admin", "role": "admin"}


def test_login_password_salah(patched_fetch):
    patched_fetch(_user())
    assert auth_service.login("admin", "salah") is None


def test_login_user_tidak_ada(patched_fetch):
    patched_fetch(None)
    assert auth_service.login("hantu", "rahasia") is None


def test_login_user_nonaktif(patched_fetch):
    patched_fetch(_user(aktif=0))
    assert auth_service.login("admin", "rahasia") is None


def test_buat_user_role_invalid(monkeypatch):
    monkeypatch.setattr(db, "execute", lambda *a, **k: pytest.fail("db tidak boleh dipanggil"))
    with pytest.raises(ValueError):
        auth_service.buat_user("x", "pass", "owner")


@pytest.mark.parametrize("username,password", [("   ", "pass"), ("admin", "")])
def test_buat_user_input_kosong(monkeypatch, username, password):
    monkeypatch.setattr(db, "execute", lambda *a, **k: pytest.fail("db tidak boleh dipanggil"))
    with pytest.raises(ValueError):
        auth_service.buat_user(username, password, "kasir")


def test_buat_user_password_terlalu_panjang(monkeypatch):
    monkeypatch.setattr(db, "execute", lambda *a, **k: pytest.fail("db tidak boleh dipanggil"))
    with pytest.raises(ValueError):
        auth_service.buat_user("admin", "x" * 73, "admin")


def test_buat_user_hash_bcrypt(monkeypatch):
    tertangkap = {}

    def fake_execute(sql, params=()):
        tertangkap["params"] = params
        return 7

    monkeypatch.setattr(db, "execute", fake_execute)
    user_id = auth_service.buat_user("kasir1", "kasir1", "kasir")

    username, password_hash, role = tertangkap["params"]
    assert user_id == 7
    assert (username, role) == ("kasir1", "kasir")
    assert password_hash != "kasir1"
    assert bcrypt.checkpw(b"kasir1", password_hash.encode())


def test_buat_user_username_duplikat(monkeypatch):
    def fake_execute(sql, params=()):
        raise pymysql.err.IntegrityError(1062, "Duplicate entry")

    monkeypatch.setattr(db, "execute", fake_execute)
    with pytest.raises(ValueError, match="sudah dipakai"):
        auth_service.buat_user("admin", "admin", "admin")
