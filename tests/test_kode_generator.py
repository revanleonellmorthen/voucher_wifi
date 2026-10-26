from voucher_wifi.core import kode_generator


def test_kode_panjang_dan_alfabet():
    kode = kode_generator.buat_kode()
    assert len(kode) == 8
    assert all(c in kode_generator.ALFABET for c in kode)
    assert not set("01ILO") & set(kode)


def test_kode_unik():
    kode = {kode_generator.buat_kode() for _ in range(1000)}
    assert len(kode) == 1000


def test_valid_format():
    assert kode_generator.valid_format("AB2CD3EF")
    assert not kode_generator.valid_format("AB2CD3E")
    assert not kode_generator.valid_format("ab2cd3ef")
    assert not kode_generator.valid_format("AB2CD3E0")
    assert not kode_generator.valid_format("")
    assert not kode_generator.valid_format(None)
