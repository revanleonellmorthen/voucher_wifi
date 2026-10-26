"""Wrapper koneksi MySQL. Satu koneksi per unit kerja, autocommit OFF."""
from contextlib import contextmanager

import pymysql
from pymysql.cursors import DictCursor

from .config import DB_CONFIG


@contextmanager
def koneksi():
    """Commit bila blok sukses, rollback bila error, selalu tutup."""
    conn = pymysql.connect(**DB_CONFIG, cursorclass=DictCursor, autocommit=False)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def fetch_one(conn, sql, params=()):
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()


def fetch_all(conn, sql, params=()):
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def execute(conn, sql, params=()):
    with conn.cursor() as cur:
        cur.execute(sql, params)
