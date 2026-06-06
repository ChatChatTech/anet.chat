#!/usr/bin/env python3
"""
Stage 1 — Per-paper research-cognition extraction.

Iterates every paper under researchers/<slug>/, calls claude-opus-4-7,
writes extract.json alongside source md. Resumable: skips papers whose
extract.json already exists and parses.

Usage:
    python3 extract_papers.py                    # all 23 researchers
    python3 extract_papers.py yunhao_liu         # single researcher
    python3 extract_papers.py --dry-run zhi_jin  # preview, no API calls
    python3 extract_papers.py --concurrency 4    # tune concurrency

Reads:
    /data/projs/anetchat/.env       — ANTHROPIC_BASE_URL, ANTHROPIC_API_KEY
    extract_spec.md                  — schema + prompt (this file mirrors)

Writes:
    <paper_dir>/extract.json         — per paper
    failures.jsonl                   — append-only log of unrecoverable
                                       failures (3 retries exhausted)
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

import httpx

sys.path.insert(0, str(Path(__file__).parent))
from load_researchers import (
    PaperEntry,
    iter_researcher_papers,
    list_researchers,
)

ROOT = Path(__file__).parent
RESEARCHERS_ROOT = ROOT / "researchers"
FAILURES_LOG = ROOT / "failures.jsonl"
ENV_FILE = Path("/data/projs/anetchat/.env")

MODEL = "claude-opus-4-7"
MAX_TOKENS = 2000
TEMPERATURE = 0.0
HTTP_TIMEOUT = 120.0
PER_CALL_TIMEOUT = 100.0
MAX_RETRIES = 3
DEFAULT_CONCURRENCY = 6

MD_HEAD = 40_000
MD_TAIL = 20_000
MD_MIN = 500           # below this → quality=thin, no LLM call


PROMPT_TEMPLATE = """You are extracting research-cognition signals from a single academic paper.
Your goal is NOT to summarize the paper. Your goal is to surface the
AUTHOR'S WAY OF THINKING — what they consider a problem, what counts as
insight to them, how they judge whether something works.

Researcher slug: {slug}
Paper directory: {paper_dir_name}
DOI: {doi_or_none}

Paper markdown follows between <PAPER> tags. It may be:
  - full text (intro + method + eval + conclusion)
  - partial (abstract only, or method missing)
  - in Chinese, English, or mixed

<PAPER>
{md_content}
</PAPER>

Extract into the JSON schema below. STRICT rules:

1. GROUNDING: every non-null field must have direct textual evidence in
   <PAPER>. If <PAPER> is too thin, write null / "unknown" / [] and set
   extraction_quality accordingly. DO NOT GUESS year, venue, DOI, or
   author intent.

2. evidence_for_taste must be VERBATIM short fragments (≤30 chars each),
   not paraphrase. Pick fragments that reveal JUDGMENT, not results.

3. thinking_moves describes the COGNITIVE MOVE in your own words.
   Examples of good moves:
     - "从工程异常反推底层物理假设失效"
     - "先证最坏情况下界, 再做经验改进"
     - "把一个 perception 问题重新 frame 成 communication 问题"
   Bad (REJECT): "propose new method", "improve accuracy".

4. negative_result_or_admitted_limitation: look for sentences where the
   author admits a method DOESN'T work, gives up on an approach, or
   criticizes the field. Often the strongest taste signal.

5. motivation / problem_framing / key_insight must each be DISTINCT.
   - motivation = WHY (动机, 现实痛点)
   - problem_framing = HOW THEY DEFINE IT (问题形式化)
   - key_insight = THE LEVER (吃饭的那句话)

6. topic_tags: 3-5 fine-grained tags (e.g. "RFID-localization",
   "screen-camera-comm"). Used for cross-paper clustering. Specific > generic.

7. Output exactly ONE JSON object, no surrounding prose, no markdown
   code fence. Schema:

{{
  "paper_id": "{paper_dir_name}",
  "doi": "{doi_or_none}",
  "title": "<paper title>",
  "year": <int or null>,
  "venue": "<venue or null>",
  "venue_tier": "<top | strong | regional | workshop | unknown>",
  "role": "<first | corresponding | co-author | senior | unknown>",
  "motivation": "<≤40 字>",
  "problem_framing": "<≤40 字>",
  "key_insight": "<≤50 字>",
  "method_signature": "<≤40 字>",
  "evaluation_criteria": "<≤40 字>",
  "negative_result_or_admitted_limitation": "<≤50 字 or null>",
  "evidence_for_taste": ["<verbatim ≤30 字>", "..."],
  "thinking_moves": ["<cognitive move>", "..."],
  "topic_tags": ["<tag1>", "<tag2>", "<tag3>"],
  "cites_own_work": [],
  "extraction_quality": "<full | partial | thin>",
  "extraction_notes": "<only if not full>"
}}
"""


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


def truncate_md(text: str) -> tuple[str, bool]:
    if len(text) <= MD_HEAD + MD_TAIL:
        return text, False
    head = text[:MD_HEAD]
    tail = text[-MD_TAIL:]
    return f"{head}\n\n[...TRUNCATED ({len(text) - MD_HEAD - MD_TAIL} chars)...]\n\n{tail}", True


def thin_extract(entry: PaperEntry, md_len: int) -> dict:
    return {
        "paper_id": entry.paper_dir.name,
        "doi": entry.doi,
        "title": entry.title,
        "year": None,
        "venue": None,
        "venue_tier": "unknown",
        "role": "unknown",
        "motivation": None,
        "problem_framing": None,
        "key_insight": None,
        "method_signature": None,
        "evaluation_criteria": None,
        "negative_result_or_admitted_limitation": None,
        "evidence_for_taste": [],
        "thinking_moves": [],
        "topic_tags": [],
        "cites_own_work": [],
        "extraction_quality": "thin",
        "extraction_notes": f"md only {md_len} chars (<{MD_MIN}); pre-filtered, no LLM call",
    }


_JSON_BLOCK_RE = re.compile(r"\{[\s\S]*\}")


def parse_json_blob(text: str) -> Optional[dict]:
    text = text.strip()
    # Strip ```json fences if present
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    try:
        return json.loads(text)
    except Exception:
        pass
    m = _JSON_BLOCK_RE.search(text)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


async def call_anthropic(
    client: httpx.AsyncClient,
    base_url: str,
    api_key: str,
    system: str,
    user: str,
) -> str:
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
        json=body,
        headers=headers,
        timeout=PER_CALL_TIMEOUT,
    )
    r.raise_for_status()
    data = r.json()
    parts = data.get("content", [])
    out = []
    for p in parts:
        if isinstance(p, dict) and p.get("type") == "text":
            out.append(p.get("text", ""))
    return "".join(out).strip()


async def extract_one(
    sem: asyncio.Semaphore,
    client: httpx.AsyncClient,
    base_url: str,
    api_key: str,
    entry: PaperEntry,
    stats: dict,
) -> None:
    out_path = entry.paper_dir / "extract.json"
    if out_path.exists():
        try:
            json.loads(out_path.read_text(encoding="utf-8"))
            stats["skipped_existing"] += 1
            return
        except Exception:
            pass  # corrupt → re-extract

    try:
        md_raw = entry.md_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        log_failure(entry, f"read_error: {e}")
        stats["failed"] += 1
        return

    if len(md_raw) < MD_MIN:
        out_path.write_text(json.dumps(thin_extract(entry, len(md_raw)),
                                       ensure_ascii=False, indent=2),
                            encoding="utf-8")
        stats["thin_skipped"] += 1
        return

    md_text, was_trunc = truncate_md(md_raw)
    user_prompt = PROMPT_TEMPLATE.format(
        slug=entry.slug,
        paper_dir_name=entry.paper_dir.name,
        doi_or_none=entry.doi or "null",
        md_content=md_text,
    )
    system = "You are a meticulous research-taste extractor. You output one JSON object, nothing else."

    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            async with sem:
                raw = await call_anthropic(client, base_url, api_key, system, user_prompt)
            obj = parse_json_blob(raw)
            if not obj:
                raise ValueError(f"JSON parse failed; raw[:200]={raw[:200]!r}")
            # Ensure required pass-through fields
            obj["paper_id"] = entry.paper_dir.name
            obj["doi"] = entry.doi  # always overwrite with truth (None or real DOI)
            if was_trunc:
                notes = obj.get("extraction_notes") or ""
                obj["extraction_notes"] = (notes + " | md truncated to head40k+tail20k").strip(" |")
            out_path.write_text(json.dumps(obj, ensure_ascii=False, indent=2),
                                encoding="utf-8")
            stats["ok"] += 1
            return
        except Exception as e:
            last_err = e
            stats["retries"] += 1
            await asyncio.sleep(2 ** attempt)  # 2s, 4s, 8s

    log_failure(entry, f"after {MAX_RETRIES} retries: {last_err}")
    stats["failed"] += 1


def log_failure(entry: PaperEntry, msg: str) -> None:
    rec = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "slug": entry.slug,
        "paper_dir": str(entry.paper_dir),
        "md_path": str(entry.md_path),
        "msg": msg,
    }
    with FAILURES_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


async def run_researcher(
    slug: str,
    sem: asyncio.Semaphore,
    client: httpx.AsyncClient,
    base_url: str,
    api_key: str,
    stats: dict,
    dry_run: bool,
) -> None:
    papers = list(iter_researcher_papers(slug))
    n_total = len(papers)
    if dry_run:
        existing = sum(1 for p in papers if (p.paper_dir / "extract.json").exists())
        print(f"[DRY] {slug:20s}  papers={n_total:4d}  existing_extract={existing}")
        return
    print(f"[RUN] {slug:20s}  papers={n_total}  starting...", flush=True)
    t0 = time.time()
    tasks = [
        extract_one(sem, client, base_url, api_key, p, stats)
        for p in papers
    ]
    # progress reporter
    async def progress():
        while True:
            await asyncio.sleep(30)
            done = stats["ok"] + stats["thin_skipped"] + stats["skipped_existing"] + stats["failed"]
            print(f"      [{slug}] +{int(time.time()-t0)}s  "
                  f"ok={stats['ok']} thin={stats['thin_skipped']} "
                  f"skip={stats['skipped_existing']} fail={stats['failed']} "
                  f"retries={stats['retries']}", flush=True)
    prog = asyncio.create_task(progress())
    try:
        await asyncio.gather(*tasks)
    finally:
        prog.cancel()
    dt = time.time() - t0
    print(f"[DONE] {slug:20s}  papers={n_total}  in {dt:.1f}s  "
          f"ok={stats['ok']} thin={stats['thin_skipped']} "
          f"skip={stats['skipped_existing']} fail={stats['failed']}", flush=True)


async def main_async(args: argparse.Namespace) -> int:
    env = load_env()
    api_key = env.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    base_url = env.get("ANTHROPIC_BASE_URL") or os.environ.get("ANTHROPIC_BASE_URL") \
               or "https://api.anthropic.com"
    if not api_key and not args.dry_run:
        print("ERROR: ANTHROPIC_API_KEY missing in /data/projs/anetchat/.env", file=sys.stderr)
        return 2

    if args.slug:
        slugs = [s for s in args.slug if (RESEARCHERS_ROOT / s).is_dir()]
        missing = [s for s in args.slug if s not in slugs]
        if missing:
            print(f"WARN: unknown slugs: {missing}", file=sys.stderr)
    else:
        slugs = list_researchers()

    sem = asyncio.Semaphore(args.concurrency)
    timeout = httpx.Timeout(HTTP_TIMEOUT, connect=15.0)
    limits = httpx.Limits(max_connections=args.concurrency * 2,
                          max_keepalive_connections=args.concurrency)

    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        for slug in slugs:
            stats = {"ok": 0, "thin_skipped": 0, "skipped_existing": 0,
                     "failed": 0, "retries": 0}
            await run_researcher(slug, sem, client, base_url, api_key,
                                 stats, args.dry_run)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="*", help="researcher slug(s); empty = all")
    ap.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
