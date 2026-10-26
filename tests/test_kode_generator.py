import pytest

from voucher_wifi.core import kode_generator as kg


def test_alfabet_tanpa_karakter_ambigu():
    assert len(kg.ALFABET) == 31
    for c in "0O1IL":
        assert c not in kg.ALFABET


def test_buat_kode_format_dan_panjang():
    for _ in range(200):
        kode = kg.buat_kode()
        assert len(kode) == 8
        assert kg.valid_format(kode)
        assert set(kode) <= set(kg.ALFABET)


def test_buat_kode_acak():
    kode = {kg.buat_kode() for _ in range(200)}
    assert len(kode) == 200


@pytest.mark.parametrize(
    "kode",
    ["", None, "ABCDEFG", "ABCDEFGHJ", "abcdefgh", "ABCD0FGH", "ABCDOFGH", "ABCD1FGH", "ABCDFGHI", "ABCDEFGL"],
)
def test_valid_format_tolak(kode):
    assert not kg.valid_format(kode)


def test_valid_format_terima():
    assert kg.valid_format("ABCD2345")
