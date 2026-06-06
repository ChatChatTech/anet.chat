#!/usr/bin/env python3
"""
Import the JSON character cards in
  /data/projs/anetchat/sillytavern/data/default-user/characters/*.json
into SillyTavern via its /api/characters/import endpoint.

ST only reads .png files (with embedded character JSON in tEXt chunks).
The /api/characters/import endpoint accepts a JSON upload and writes
the corresponding .png to the characters directory.

Flow:
  1. GET /csrf-token (sets cookie, returns token)
  2. POST /api/characters/import (multipart) with file_type=json + the file
  3. Verify via /api/characters/all

Usage:
    python3 import_into_sillytavern.py             # all *.json
    python3 import_into_sillytavern.py yunhao_liu  # one slug
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import sys
import time
from pathlib import Path

import httpx

ST_URL = "http://localhost:8000"
CARDS_DIR = Path("/data/projs/anetchat/sillytavern/data/default-user/characters")


def get_csrf(client: httpx.Client) -> str:
    r = client.get(f"{ST_URL}/csrf-token", timeout=10)
    r.raise_for_status()
    return r.json()["token"]


def list_characters(client: httpx.Client, token: str) -> list[dict]:
    r = client.post(f"{ST_URL}/api/characters/all",
                    headers={"x-csrf-token": token, "Content-Type": "application/json"},
                    json={}, timeout=15)
    r.raise_for_status()
    return r.json()


def import_card(client: httpx.Client, token: str, card_path: Path) -> tuple[bool, str]:
    """POST one JSON card. Returns (ok, file_name_or_error)."""
    data = card_path.read_bytes()
    files = {
        "avatar": (card_path.name, data, "application/json"),
    }
    form = {"file_type": "json", "preserved_name": card_path.stem}
    r = client.post(
        f"{ST_URL}/api/characters/import",
        headers={"x-csrf-token": token},
        files=files,
        data=form,
        timeout=30,
    )
    if r.status_code != 200:
        return False, f"HTTP {r.status_code}: {r.text[:200]}"
    try:
        body = r.json()
    except Exception:
        return False, f"non-JSON response: {r.text[:200]}"
    if body.get("error"):
        return False, f"import error: {body}"
    return True, body.get("file_name", "?")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="*")
    args = ap.parse_args()

    files = sorted(CARDS_DIR.glob("*.json"))
    if args.slug:
        wanted = set(args.slug)
        files = [f for f in files if f.stem in wanted]
    if not files:
        print("no cards to import", file=sys.stderr)
        return 1

    with httpx.Client() as client:
        token = get_csrf(client)
        print(f"csrf: ok ({token[:12]}...)")
        ok = 0
        fail = 0
        for f in files:
            success, info = import_card(client, token, f)
            tag = "ok " if success else "FAIL"
            print(f"[{tag}] {f.stem:24s} → {info}")
            if success:
                ok += 1
            else:
                fail += 1
            time.sleep(0.15)  # light pacing
        print(f"--- imported {ok}/{len(files)} ({fail} failed)")

        # Verify
        token = get_csrf(client)   # token may have rotated
        chars = list_characters(client, token)
        print(f"--- /api/characters/all now returns {len(chars)} characters")
        names = sorted(c.get("name", "?") for c in chars)
        for n in names[:30]:
            print(f"    {n}")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
