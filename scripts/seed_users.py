"""Seed user admin/kasir.

Pakai: python scripts/seed_users.py --username admin --password admin --role admin
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from voucher_wifi.core import auth_service  # noqa: E402


def main():
    p = argparse.ArgumentParser(description="Buat user admin/kasir")
    p.add_argument("--username", required=True)
    p.add_argument("--password", required=True)
    p.add_argument("--role", required=True, choices=auth_service.ROLE_VALID)
    args = p.parse_args()

    try:
        user_id = auth_service.buat_user(args.username, args.password, args.role)
    except ValueError as e:
        print(f"gagal: {e}", file=sys.stderr)
        return 1

    print(f"user dibuat: id={user_id} username={args.username} role={args.role}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
