#!/usr/bin/env python3
"""
End-to-end ST → LLM test for a researcher persona.

Flow:
  1. GET /csrf-token (cookie + token)
  2. POST /api/characters/get { avatar_url: "<slug>.png" }
     → returns persona's system_prompt + character_book
  3. Match a test user message against lorebook keys, collect the matched
     entries (capped at token budget approximate)
  4. Build messages: [
        {role: "system", content: system_prompt + matched_lore},
        {role: "user",   content: user_msg},
     ]
  5. POST directly to the tokhubs gpt-5.5 endpoint (our existing primary
     LLM — same one anet.chat uses). NOT through ST's /generate (which
     would require configuring ST's own LLM credentials).
  6. Print the response. Verify it sounds in-character.

Usage:
    python3 st_api_e2e_test.py <slug> "<user question>"
    python3 st_api_e2e_test.py yunhao_liu "大模型时代物联网研究还能做什么？"
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import httpx

ST_URL = "http://localhost:8000"
ENV_FILE = Path("/data/projs/anetchat/.env")


def load_env() -> dict[str, str]:
    env = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def fetch_character(slug: str) -> dict:
    """Pull character data from ST API."""
    with httpx.Client() as c:
        tok = c.get(f"{ST_URL}/csrf-token", timeout=10).json()["token"]
        r = c.post(f"{ST_URL}/api/characters/get",
                   headers={"x-csrf-token": tok, "Content-Type": "application/json"},
                   json={"avatar_url": f"{slug}.png"}, timeout=15)
        if r.status_code == 404:
            raise SystemExit(f"character not found: {slug}.png")
        r.raise_for_status()
        return r.json()


def match_lorebook(user_msg: str, lorebook: dict | None, budget_chars: int = 4000) -> list[dict]:
    """Naively match user_msg against entry.keys (case-insensitive substring).
    Returns the matched entries, ordered by priority, capped at budget."""
    if not lorebook:
        return []
    msg_l = user_msg.lower()
    matched = []
    for e in lorebook.get("entries", []):
        if not e.get("enabled", True):
            continue
        keys = [k.lower() for k in e.get("keys") or []]
        if any(k and k in msg_l for k in keys):
            matched.append(e)
    matched.sort(key=lambda e: -e.get("priority", 0))
    out, used = [], 0
    for e in matched:
        cost = len(e.get("content", ""))
        if used + cost > budget_chars:
            break
        out.append(e)
        used += cost
    return out


def call_tokhubs(env: dict, system: str, user: str) -> str:
    """Direct call to our primary LLM — same chain anet.chat uses."""
    base = env.get("OPENAI_BASE_URL", "https://tokhubs.com").rstrip("/")
    api_key = env["OPENAI_API_KEY"]
    model = env.get("OPENAI_MODEL", "gpt-5.5")
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        "max_tokens": 600,
    }
    effort = env.get("OPENAI_REASONING_EFFORT", "default")
    if effort and effort != "default":
        body["reasoning_effort"] = effort
    r = httpx.post(
        f"{base}/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json"},
        json=body,
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("user_msg")
    args = ap.parse_args()

    print(f"=== fetching character {args.slug} from ST ===")
    card = fetch_character(args.slug)
    name = card.get("name") or card.get("data", {}).get("name")
    sp = card.get("system_prompt") or card.get("data", {}).get("system_prompt") or ""
    cb = card.get("data", {}).get("character_book") or card.get("character_book")
    print(f"  name: {name}")
    print(f"  system_prompt: {len(sp)} chars")
    print(f"  lorebook entries: {len(cb['entries']) if cb else 0}")

    print(f"\n=== matching lorebook against user message ===")
    matched = match_lorebook(args.user_msg, cb)
    print(f"  matched entries: {len(matched)}")
    for e in matched[:5]:
        print(f"    + {e['name']:30s} keys={e['keys']}")

    # Assemble system prompt with matched lore appended
    lore_block = ""
    if matched:
        lore_block = "\n\n## RELEVANT REFERENCES (auto-pulled from your corpus)\n" + \
                     "\n".join(e["content"] for e in matched)
    full_system = sp + lore_block

    print(f"\n=== calling LLM (system={len(full_system)} chars, user={len(args.user_msg)} chars) ===")
    env = load_env()
    text = call_tokhubs(env, full_system, args.user_msg)
    print(f"\n=== RESPONSE ===")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
