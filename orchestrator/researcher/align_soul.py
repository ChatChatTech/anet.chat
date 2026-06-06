#!/usr/bin/env python3
"""
Stage 2.5 — Opus 4.7 alignment-refinement of soul.md against yunhao_liu gold.

Handles two cases:
  1. soul.md missing → generates from scratch (Opus 4.7 from profile + extracts)
  2. soul.md exists → refines for alignment with gold (preserves existing
     paper anchors, tightens register, adds missing sections)

Why Opus 4.7 here (not gpt-5.5):
  - Higher fidelity to subtle stylistic register of the gold
  - Better at preserving paper_id anchors verbatim
  - Better at distinguishing "distillation" vs "summary"

Usage:
    python3 align_soul.py                  # all 22 non-gold
    python3 align_soul.py jianwei_yin      # one
    python3 align_soul.py --force ge_li    # overwrite existing
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Optional

import httpx

sys.path.insert(0, str(Path(__file__).parent))
from load_researchers import iter_researcher_papers, list_researchers

ROOT = Path(__file__).parent
RESEARCHERS_ROOT = ROOT / "researchers"
ENV_FILE = Path("/data/projs/anetchat/.env")

GOLD_SLUG = "yunhao_liu"
GOLD_SOUL = RESEARCHERS_ROOT / GOLD_SLUG / "soul.md"

MODEL = "claude-opus-4-7"
MAX_TOKENS = 8000
TEMPERATURE = 0.2
TOP_EXTRACTS = 8       # # of highest-signal extracts to include as evidence
MAX_RETRIES = 4
HTTP_TIMEOUT = 240.0


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


def signal_score(ex: dict) -> int:
    """Same heuristic as aggregate_profile."""
    s = 0
    if ex.get("extraction_quality") == "full": s += 5
    elif ex.get("extraction_quality") == "partial": s += 2
    s += min(len(ex.get("thinking_moves") or []), 4)
    s += min(len(ex.get("evidence_for_taste") or []), 4)
    if ex.get("negative_result_or_admitted_limitation"): s += 3
    if ex.get("venue_tier") == "top": s += 4
    elif ex.get("venue_tier") == "strong": s += 2
    if ex.get("role") in ("first", "corresponding"): s += 2
    return s


def collect_top_extracts(slug: str, n: int) -> list[dict]:
    extracts = []
    for entry in iter_researcher_papers(slug):
        p = entry.paper_dir / "extract.json"
        if not p.exists():
            continue
        try:
            extracts.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            pass
    extracts.sort(key=signal_score, reverse=True)
    return extracts[:n]


SYSTEM = """You are a research-cognition writer. Your task is to take a target
researcher's cross-paper aggregated profile + a handful of high-signal
per-paper extracts, and produce (or refine) a soul.md that DISTILLES their
research thinking process — NOT summarizes their research.

You will be shown ONE gold-standard soul.md (for `yunhao_liu`) as the
required style + structure + density reference.

HARD RULES — every output must satisfy these:

1. STRUCTURE: 8 sections numbered 1-8, headings exactly:
   `## 1. 研究领域版图`
   `## 2. 科研品味`
   `## 3. 思考过程 (Thinking Moves)`
   `## 4. 问题发现方法`
   `## 5. 判断标准`
   `## 6. 反模式 (他明确拒绝什么)`
   `## 7. 标志性论文 (用于"旁征博引"的弹药库)`
   `## 8. 表达 DNA`
   (For very small corpora <5 papers, §7 may have fewer items — but
   sections must still all exist.)

2. EVERY non-trivial claim must end with `Anchors: (<paper_id>, ...)`
   citing real paper_ids from the provided profile. No claim may stand
   without anchors. No invented paper_ids.

3. DISTILL, do not summarize. §2 = taste rules (WHY he cares about X);
   §3 = COGNITIVE MOVES (the verb he applies when seeing a new problem);
   NOT "他研究了 X" but "他遇到 X 时, 倾向先问 Y".

4. §3 thinking moves: each move follows pattern
   `**Move X: <one-line action>**. <≤2 sentence elaboration>. Anchors: ...`
   Aim for 4-8 distinct moves. Generic moves like "propose new method"
   are REJECTED — every move must be specific enough that it could only
   plausibly apply to THIS researcher.

5. §6 反模式: 5-10 specific rejections, each with anchor. Reject items
   that could fit any researcher (e.g. "rejects bad code") — list only
   what the profile's `consistent_rejections` or extracts' negative_results
   actually evidence.

6. §7 lists 10-15 anchor papers (or fewer for tiny corpora) in the gold's
   exact format:
   `\\`<paper_id>\\` | <year> | <venue> | <≤30字 — what this paper anchors`

7. §8 expression DNA: 4-8 bullets capturing
   - opening style of abstracts
   - recurring rhetorical patterns / signature句式
   - preferred analogies / metaphors
   - admission-of-limitation style (specific numbers? vague?)
   NOT personality / personal quirks.

8. LANGUAGE: match the dominant language in the profile.
   - Chinese researcher with Chinese tags → Chinese soul
   - English-only corpus → English soul
   - Mixed: match gold (use Chinese for connective tissue, keep English
     paper_ids and technical terms verbatim).

9. The header is exactly 2 lines:
   `# <Name> (<English name if applicable>)`
   `> <one-sentence research identity, third-person>`
   Nothing else before §1.

10. NO meta-prose. No "this soul.md attempts to ...", no "based on the
    profile ...". Open §1 directly with substance.

OUTPUT: emit only the soul.md content. No fences, no preamble."""


USER_TEMPLATE = """## GOLD STANDARD (style + structure + density reference)
This is the hand-written soul.md for `{gold_slug}`. Use as STYLE reference.
Do NOT copy its content — only its register and tightness.

<GOLD>
{gold}
</GOLD>

## TARGET RESEARCHER: `{slug}`

### Cross-paper aggregated profile (Stage 1.5 output)
<PROFILE>
{profile_json}
</PROFILE>

### Top high-signal per-paper extracts ({n_extracts})
These give you VERBATIM taste quotes + negative_results to anchor §2/§6.
<EXTRACTS>
{extracts_json}
</EXTRACTS>

### EXISTING draft soul.md (may exist or be empty)
If non-empty, your job is REFINEMENT: preserve correct anchors,
fix any structural drift, tighten any prose that explains rather
than distills, ensure every section meets the HARD RULES.

<EXISTING>
{existing_soul}
</EXISTING>

## OUTPUT
Emit the complete, refined soul.md for `{slug}` now. Start with `# `,
end with §8's last bullet. Nothing else."""


async def call_anthropic(client: httpx.AsyncClient, base_url: str,
                          api_key: str, system: str, user: str) -> str:
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    r = await client.post(
        f"{base_url.rstrip('/')}/v1/messages",
        json=body, headers=headers, timeout=HTTP_TIMEOUT,
    )
    r.raise_for_status()
    data = r.json()
    out = []
    for p in data.get("content", []):
        if isinstance(p, dict) and p.get("type") == "text":
            out.append(p.get("text", ""))
    return "".join(out).strip()


async def align_one(slug: str, client: httpx.AsyncClient,
                    base_url: str, api_key: str, force: bool) -> bool:
    soul_path = RESEARCHERS_ROOT / slug / "soul.md"
    profile_path = RESEARCHERS_ROOT / slug / "researcher_profile.json"
    if not profile_path.exists():
        print(f"[err]  {slug:20s}  no researcher_profile.json")
        return False
    if slug == GOLD_SLUG and not force:
        print(f"[skip] {slug:20s}  gold standard, won't overwrite (use --force)")
        return False

    existing = soul_path.read_text(encoding="utf-8") if soul_path.exists() else "(none)"
    profile = profile_path.read_text(encoding="utf-8")
    gold = GOLD_SOUL.read_text(encoding="utf-8")
    top_extracts = collect_top_extracts(slug, TOP_EXTRACTS)

    user = USER_TEMPLATE.format(
        gold_slug=GOLD_SLUG,
        gold=gold,
        slug=slug,
        profile_json=profile,
        n_extracts=len(top_extracts),
        extracts_json=json.dumps(top_extracts, ensure_ascii=False, indent=2),
        existing_soul=existing,
    )

    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[run]  {slug:20s}  Opus 4.7 align (attempt {attempt})...", flush=True)
            out = await call_anthropic(client, base_url, api_key, SYSTEM, user)
            out = out.strip()
            if out.startswith("```"):
                out = out.split("\n", 1)[1] if "\n" in out else out
                if out.endswith("```"):
                    out = out.rsplit("```", 1)[0]
            if not out.startswith("# "):
                raise ValueError(f"output doesn't start with '# '; first 80 chars: {out[:80]!r}")
            # quick structural sanity check
            required = ["## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6.", "## 7.", "## 8."]
            missing = [s for s in required if s not in out]
            if missing:
                raise ValueError(f"missing sections: {missing}")
            soul_path.write_text(out + "\n", encoding="utf-8")
            print(f"[ok]   {slug:20s}  wrote {len(out)} chars", flush=True)
            return True
        except Exception as e:
            last_err = e
            print(f"[retry] {slug:20s}  attempt {attempt}: {type(e).__name__}: {str(e)[:120]}", flush=True)
            await asyncio.sleep(2 ** attempt)

    print(f"[fail] {slug:20s}  after {MAX_RETRIES} retries: {last_err}", flush=True)
    return False


async def main_async(args: argparse.Namespace) -> int:
    if not GOLD_SOUL.exists():
        print(f"ERROR: gold missing: {GOLD_SOUL}", file=sys.stderr)
        return 2

    env = load_env()
    base_url = env.get("ANTHROPIC_BASE_URL") or "https://api.anthropic.com"
    api_key = env.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY missing", file=sys.stderr)
        return 2

    slugs = args.slug or [s for s in list_researchers() if s != GOLD_SLUG]
    timeout = httpx.Timeout(HTTP_TIMEOUT, connect=15.0)
    sem = asyncio.Semaphore(args.concurrency)

    async def run_with_sem(slug):
        async with sem:
            return await align_one(slug, client, base_url, api_key, args.force)

    async with httpx.AsyncClient(timeout=timeout) as client:
        await asyncio.gather(*[run_with_sem(s) for s in slugs])
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="*")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--concurrency", type=int, default=3)
    args = ap.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
