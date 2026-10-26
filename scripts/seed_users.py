"""Seed/ubah user CLI.

Contoh:
    python scripts/seed_users.py --username admin --password admin --role admin
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import bcrypt  # noqa: E402

from voucher_wifi import db  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Buat/ubah user voucher_wifi.")
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--role", required=True, choices=["admin", "kasir"])
    args = parser.parse_args()

    username = args.username.strip()
    if not username:
        sys.exit("Username kosong.")
    if len(args.password.encode("utf-8")) > 72:
        sys.exit("Password > 72 byte (batas bcrypt).")

    password_hash = bcrypt.hashpw(
        args.password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    with db.koneksi() as conn:
        db.execute(
            conn,
            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)"
            " ON DUPLICATE KEY UPDATE password_hash = VALUES(password_hash),"
            " role = VALUES(role), aktif = TRUE",
            (username, password_hash, args.role),
        )

    print(f"user '{username}' siap (role {args.role})")


if __name__ == "__main__":
    main()
