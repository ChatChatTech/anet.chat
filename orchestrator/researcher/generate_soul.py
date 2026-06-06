#!/usr/bin/env python3
"""
Stage 2-3 — Generate soul.md per researcher using gpt-5.5 (via OPENAI
config in .env, tokhubs base_url).

Inputs per researcher:
  - researchers/<slug>/researcher_profile.json   (Stage 1.5 output)
  - researchers/<slug>/research_index.json       (Stage 5 partial, no anchors yet)
  - researchers/yunhao_liu/soul.md               (user-written GOLD STANDARD)
  - soul_template.md                              (skeleton)

Output:
  - researchers/<slug>/soul.md

Behavior:
  - Skips yunhao_liu (gold) and any slug whose soul.md already exists.
  - Refuses to run if researchers/yunhao_liu/soul.md is missing.
  - 1 API call per researcher; gpt-5.5 default model from .env.

Usage:
    python3 generate_soul.py                     # all 22 (skip yunhao)
    python3 generate_soul.py zhi_jin             # one researcher
    python3 generate_soul.py --force shuiguang_deng  # overwrite existing
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).parent))
from load_researchers import list_researchers

ROOT = Path(__file__).parent
RESEARCHERS_ROOT = ROOT / "researchers"
ENV_FILE = Path("/data/projs/anetchat/.env")

GOLD_SLUG = "yunhao_liu"
GOLD_SOUL = RESEARCHERS_ROOT / GOLD_SLUG / "soul.md"
TEMPLATE_FILE = ROOT / "soul_template.md"

HTTP_TIMEOUT = 180.0


def load_env() -> dict[str, str]:
    env = {}
    if not ENV_FILE.exists():
        return env
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


SYSTEM = """You are a research-cognition writer. Given (1) a gold-standard
soul.md hand-written for one researcher, (2) the same skeleton template,
and (3) a JSON profile of cross-paper patterns for a DIFFERENT researcher,
you write that researcher's soul.md.

HARD RULES:
1. EVERY claim must cite ≥1 paper_id from the profile. No vibes. No
   generic descriptions that could fit any researcher.
2. Match the gold's STRUCTURE and TONE precisely. Same section
   numbering, same density, same prose register.
3. Do NOT invent papers, years, or venues — only use what's in the profile.
4. The output is ONE markdown file. No preamble, no postscript, no
   <FILE> tags. Just the soul.md content starting with `# <name>`.
5. 中文 researcher → 中文 soul; English-only researcher → English soul.
   Mixed corpus → match dominant language."""

USER_TEMPLATE = """## TASK
Write soul.md for researcher slug: {slug}

## GOLD STANDARD (for tone, structure, density)
The following is the hand-written soul.md for researcher `yunhao_liu`.
Use this as the reference for HOW to write — not WHAT to write.

<GOLD>
{gold}
</GOLD>

## SKELETON TEMPLATE
<TEMPLATE>
{template}
</TEMPLATE>

## TARGET RESEARCHER PROFILE
The cross-paper aggregated patterns for `{slug}`. Use ONLY this material
to fill in the template. Cite paper_ids verbatim from this profile.

<PROFILE>
{profile_json}
</PROFILE>

## OUTPUT
Emit the complete soul.md for `{slug}` now. Start with `# `. End with
the last section. Nothing else."""


def call_openai_chat(base_url: str, api_key: str, model: str,
                     system: str, user: str) -> str:
    """Generic OpenAI-compatible /v1/chat/completions call."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.3,
    }
    with httpx.Client(timeout=HTTP_TIMEOUT) as client:
        r = client.post(f"{base_url.rstrip('/')}/v1/chat/completions",
                        headers=headers, json=body)
        r.raise_for_status()
        data = r.json()
    return data["choices"][0]["message"]["content"]


def generate_for(slug: str, env: dict[str, str], force: bool) -> bool:
    soul_path = RESEARCHERS_ROOT / slug / "soul.md"
    if soul_path.exists() and not force:
        print(f"[skip] {slug:20s}  soul.md exists (use --force)")
        return False
    profile_path = RESEARCHERS_ROOT / slug / "researcher_profile.json"
    if not profile_path.exists():
        print(f"[err]  {slug:20s}  no researcher_profile.json — run aggregate_profile.py first")
        return False

    gold = GOLD_SOUL.read_text(encoding="utf-8")
    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    profile = profile_path.read_text(encoding="utf-8")

    user_msg = USER_TEMPLATE.format(
        slug=slug, gold=gold, template=template, profile_json=profile,
    )

    base_url = env.get("OPENAI_BASE_URL") or "https://api.openai.com"
    api_key  = env.get("OPENAI_API_KEY")
    model    = env.get("OPENAI_MODEL", "gpt-5.5")
    if not api_key:
        print(f"[err]  {slug:20s}  OPENAI_API_KEY missing")
        return False

    print(f"[run]  {slug:20s}  calling {model}...", flush=True)
    out = call_openai_chat(base_url, api_key, model, SYSTEM, user_msg)
    out = out.strip()
    # Strip ``` fences if model wrapped output
    if out.startswith("```"):
        out = out.split("\n", 1)[1] if "\n" in out else out
        if out.endswith("```"):
            out = out.rsplit("```", 1)[0]
    soul_path.write_text(out + "\n", encoding="utf-8")
    print(f"[ok]   {slug:20s}  wrote {len(out)} chars → {soul_path.relative_to(ROOT)}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="*", help="researcher slug(s); empty = all (except gold)")
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing soul.md")
    args = ap.parse_args()

    if not GOLD_SOUL.exists():
        print(f"ERROR: gold standard missing: {GOLD_SOUL}", file=sys.stderr)
        print("Write yunhao_liu/soul.md first (hand-written), then re-run.",
              file=sys.stderr)
        return 2

    env = load_env()
    slugs = args.slug or [s for s in list_researchers() if s != GOLD_SLUG]
    for slug in slugs:
        if slug == GOLD_SLUG and not args.force:
            print(f"[skip] {slug:20s}  is the gold standard, won't overwrite")
            continue
        try:
            generate_for(slug, env, args.force)
        except Exception as e:
            print(f"[fail] {slug:20s}  {type(e).__name__}: {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
