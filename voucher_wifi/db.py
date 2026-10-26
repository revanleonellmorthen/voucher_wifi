"""Wrapper MySQL. Satu koneksi per pemanggilan, autocommit OFF."""

import pymysql

from . import config


def _koneksi():
    return pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def fetch_one(sql, params=()):
    conn = _koneksi()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()
    finally:
        conn.close()


def fetch_all(sql, params=()):
    conn = _koneksi()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        conn.close()


def execute(sql, params=()):
    """Operasi tulis: commit eksplisit, kembalikan id baris baru."""
    conn = _koneksi()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            lastrowid = cur.lastrowid
        conn.commit()
        return lastrowid
    finally:
        conn.close()
