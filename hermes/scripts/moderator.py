#!/usr/bin/env python3
"""
anet.chat moderator — picks 3 of N personas based on canvas content.

Called by supervisor.sh every minute. State lives in /opt/data/state.json.

Trigger conditions for re-pick:
  - phase == WAITING and a NEW human-authored element appears
  - phase == ACTIVE and the number of agent elements since last pick >= 10

Pool: /opt/data/scripts/personas_pool.json (4 entries today; scales to 40+).

LLM: direct POST to the Anthropic-compatible endpoint (ANTHROPIC_BASE_URL +
ANTHROPIC_API_KEY env). Output strict JSON {"picks": ["slug1","slug2","slug3"]}.

Side effects:
  - Writes /opt/data/state.json with the new active slugs
  - Pauses cron jobs for personas NOT in the picks
  - Resumes cron jobs for personas IN the picks
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

CANVAS_URL = os.environ.get("CANVAS_URL", "http://127.0.0.1:3000")
DATA_DIR = "/opt/data"
POOL_PATH = f"{DATA_DIR}/scripts/personas_pool.json"
STATE_PATH = f"{DATA_DIR}/state.json"
HERMES = "/opt/hermes/.venv/bin/hermes"

ANTHROPIC_BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://api.minimaxi.com/anthropic").rstrip("/")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "MiniMax-M2.7-highspeed")

RE_PICK_EVERY_N_ROUNDS = 10


def log(msg: str) -> None:
    print(f"[moderator] {msg}", flush=True)


# ---- helpers ---------------------------------------------------------------
def load_pool() -> dict:
    with open(POOL_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_state() -> dict:
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"phase": "WAITING", "active_slugs": [], "last_pick_round": 0,
                "last_human_signature": "", "last_question": ""}


def save_state(state: dict) -> None:
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def get_canvas_elements() -> list[dict]:
    try:
        req = urllib.request.Request(f"{CANVAS_URL}/api/elements")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8")).get("elements", [])
    except Exception as exc:
        log(f"canvas fetch failed: {exc}")
        return []


def is_header(e: dict) -> bool:
    return (e.get("id") or "").startswith("header-")


def is_human(e: dict) -> bool:
    if is_header(e):
        return False
    sc = (e.get("strokeColor") or "").lower()
    return not sc or sc in {"#000000", "#1e1e1e", "black"}


def is_agent(e: dict, agent_colors: set) -> bool:
    if is_header(e) or is_human(e):
        return False
    sc = (e.get("strokeColor") or "").lower()
    return sc in agent_colors


def element_text(e: dict) -> str:
    t = e.get("text") or ""
    if not t and isinstance(e.get("label"), dict):
        t = e["label"].get("text", "") or ""
    return t


# ---- cron pause / resume --------------------------------------------------
def get_persona_cron_id(slug: str) -> str | None:
    try:
        out = subprocess.run(
            [HERMES, "-p", slug, "cron", "list"],
            capture_output=True, text=True, timeout=10,
        ).stdout
        m = re.search(r"\b([0-9a-f]{12})\b", out)
        return m.group(1) if m else None
    except Exception as exc:
        log(f"cron list -p {slug} failed: {exc}")
        return None


def cron_pause(slug: str, job_id: str) -> None:
    subprocess.run([HERMES, "-p", slug, "cron", "pause", job_id],
                   capture_output=True, text=True, timeout=10)


def cron_resume(slug: str, job_id: str) -> None:
    subprocess.run([HERMES, "-p", slug, "cron", "resume", job_id],
                   capture_output=True, text=True, timeout=10)


def apply_active_set(active_slugs: list[str], all_slugs: list[str]) -> None:
    """Pause persona crons not in `active_slugs`, resume those that are."""
    for slug in all_slugs:
        job_id = get_persona_cron_id(slug)
        if not job_id:
            continue
        if slug in active_slugs:
            cron_resume(slug, job_id)
        else:
            cron_pause(slug, job_id)


# ---- LLM picker ------------------------------------------------------------
def call_llm_to_pick(question: str, canvas_digest: str, pool: dict) -> list[str]:
    """Ask the LLM to pick 3 slugs. Fallback to first 3 if call fails."""
    if not ANTHROPIC_API_KEY:
        log("no ANTHROPIC_API_KEY — falling back to first 3 pool entries")
        return list(pool.keys())[:3]

    pool_lines = "\n".join(
        f"- slug={slug}  name={p['name']}  color={p['color']}\n  {p['description']}"
        for slug, p in pool.items()
    )
    system = (
        "You are anet.chat's moderator. Given a user question and the live canvas, "
        "pick EXACTLY 3 personas from the pool whose perspectives are MOST complementary "
        "for this topic. Avoid same-flavor picks (e.g. don't pick 3 engineers for a "
        "philosophical question). Output strict JSON only — no prose, no markdown."
    )
    user = f"""USER QUESTION:
{question or '(none — pick a strong starter trio)'}

CURRENT CANVAS DIGEST:
{canvas_digest or '(empty)'}

PERSONA POOL ({len(pool)} available):
{pool_lines}

Output JSON of this exact shape:
{{"picks":["<slug1>","<slug2>","<slug3>"],"reason":"<<= 60 chars summary>"}}
"""
    payload = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": 1500,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    try:
        req = urllib.request.Request(
            f"{ANTHROPIC_BASE_URL}/v1/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        log(f"LLM call failed ({exc}) — falling back to first 3")
        return list(pool.keys())[:3]

    text_blocks = [b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"]
    raw = "\n".join(text_blocks).strip()
    # Strip markdown fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.I)
    raw = re.sub(r"\s*```$", "", raw)
    m = re.search(r"\{.*\}", raw, flags=re.S)
    if not m:
        log(f"LLM returned non-JSON ({raw[:200]!r}) — fallback")
        return list(pool.keys())[:3]
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError:
        return list(pool.keys())[:3]

    valid = list(pool.keys())
    picks: list[str] = []
    for slug in obj.get("picks", []):
        if slug in valid and slug not in picks:
            picks.append(slug)
    # Fill if LLM gave fewer than 3
    for slug in valid:
        if len(picks) >= 3:
            break
        if slug not in picks:
            picks.append(slug)
    log(f"picked {picks}  reason={(obj.get('reason') or '')[:80]!r}")
    return picks[:3]


# ---- main ------------------------------------------------------------------
def main() -> None:
    pool = load_pool()
    pool_slugs = list(pool.keys())
    agent_colors = {p["color"].lower() for p in pool.values()}

    state = load_state()
    elements = get_canvas_elements()

    non_header = [e for e in elements if not is_header(e)]
    human_els = [e for e in non_header if is_human(e)]
    agent_els = [e for e in non_header if is_agent(e, agent_colors)]

    # Compose a stable signature of all human text on the canvas, so we can
    # detect when a fresh question arrived.
    human_sig = " | ".join(sorted(filter(None, (element_text(e) for e in human_els))))[:300]
    latest_human_text = ""
    if human_els:
        latest_human_text = max(
            (element_text(e) for e in human_els if element_text(e)),
            key=lambda s: len(s), default="",
        )

    # ---- WAITING ----
    if not human_els:
        # Canvas has no human text → reset to WAITING with no active personas
        if state.get("phase") != "WAITING" or state.get("active_slugs"):
            log("no human input → entering WAITING (all personas paused)")
            for slug in pool_slugs:
                jid = get_persona_cron_id(slug)
                if jid:
                    cron_pause(slug, jid)
            state.update({
                "phase": "WAITING", "active_slugs": [], "last_pick_round": 0,
                "last_human_signature": "", "last_question": "",
            })
            save_state(state)
        else:
            log("WAITING (no human input)")
        return

    # ---- new question while WAITING → first pick ----
    new_question = (state.get("phase") != "ACTIVE" or
                    state.get("last_human_signature") != human_sig)
    rounds_since_pick = max(0, len(agent_els) - state.get("last_pick_round", 0))
    needs_repick = state.get("phase") == "ACTIVE" and rounds_since_pick >= RE_PICK_EVERY_N_ROUNDS

    if not new_question and not needs_repick:
        log(f"ACTIVE — no re-pick needed (rounds_since_pick={rounds_since_pick})")
        return

    # Build canvas digest (last 10 agent texts) so re-picks see topic evolution
    recent_texts = []
    for e in agent_els[-15:]:
        t = element_text(e)
        sc = (e.get("strokeColor") or "").lower()
        if t:
            recent_texts.append(f"  - {sc}: {t[:80]}")
    canvas_digest = "\n".join(recent_texts) if recent_texts else "(no agent content yet)"

    log(f"trigger=({'new_question' if new_question else 'repick@'+str(rounds_since_pick)}) — calling LLM")
    picks = call_llm_to_pick(latest_human_text, canvas_digest, pool)

    apply_active_set(picks, pool_slugs)
    state.update({
        "phase": "ACTIVE",
        "active_slugs": picks,
        "last_pick_round": len(agent_els),
        "last_human_signature": human_sig,
        "last_question": latest_human_text[:300],
    })
    save_state(state)
    log(f"transitioned to ACTIVE with picks={picks}, paused others")


if __name__ == "__main__":
    main()
