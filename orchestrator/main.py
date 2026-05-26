"""
anet-souls v3.1 — multi-persona collaboration brain for anet.chat Excalidraw canvas.

Highlights vs v2:
- Per-slot LANES: each agent has a preferred x-column (A=left, B=middle, C=below)
- BBox-based collision detection: agent prompts include element footprints + overlaps
- Free zones suggested per-slot (round-robin distribution avoids 3-way convergence)
- New action types: move (relocate own), delete (own), erase (others, ≤1/turn, must
  give reason ≥4 chars). All accept full or unique-prefix IDs.
- Arrow validation: arrow endpoint must land inside (or within 20px of) a dashed
  rectangle. Otherwise the arrow is dropped.
- TIDY-UP: every 3 normal rounds, ONE random slot is asked to tidy. Only that slot's
  next fire does move/delete; the other two continue normal conversation.
- NO early skip on "no new external elements" — LLM is always called, agent decides
  silence via actions:[]. Stagnation hint added when canvas has been quiet >60s.
- Punchy default: MAX_ACTIONS=3 (was 5), AGENT.md leads with "find one hot point,
  react punchy, don't dump a column of 5 thoughts".
"""

from __future__ import annotations

import asyncio
import datetime as dt
import json
import os
import random
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx

# --------------------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------------------
CANVAS_URL = os.environ.get("CANVAS_URL", "http://canvas:3000")

# =====================================================================
# Provider chain — MiniMax primary, Doubao fallback.
# We track each provider's health (consecutive failures) and skip
# unhealthy ones for COOLDOWN_S seconds. anet-souls v2 highlight:
# whenever the primary takes > FAILOVER_TIMEOUT_S to respond,
# we fail it over immediately rather than wait the full HTTP timeout.
# =====================================================================
ANTHROPIC_BASE_URL = os.environ["ANTHROPIC_BASE_URL"].rstrip("/")
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "MiniMax-M2.7-highspeed")

DOUBAO_BASE = (os.environ.get("DOUBAO_RESPONSES_URL")
               or "https://ark.cn-beijing.volces.com/api/v3/responses").rstrip("/")
DOUBAO_KEY = os.environ.get("DOUBAO_RESPONSES_API_KEY", "")
DOUBAO_MODEL = os.environ.get("DOUBAO_RESPONSES_DEFAULT_MODEL",
                              "doubao-seed-2-0-pro-260215")
DOUBAO_AVAILABLE = bool(DOUBAO_KEY)

# tokhubs / OpenAI Responses (gpt-5.4) — primary in chain.
OPENAI_BASE = (os.environ.get("OPENAI_BASE_URL") or "https://tokhubs.com").rstrip("/")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.4")
OPENAI_REASONING_EFFORT = os.environ.get("OPENAI_REASONING_EFFORT", "xhigh")
OPENAI_AVAILABLE = bool(OPENAI_KEY)

# Health tracker — globally shared across all LLM calls.
PROVIDER_HEALTH = {
    "openai":  {"consecutive_fails": 0, "unhealthy_until": 0.0},
    "minimax": {"consecutive_fails": 0, "unhealthy_until": 0.0},
    "doubao":  {"consecutive_fails": 0, "unhealthy_until": 0.0},
}
FAILOVER_FAIL_THRESHOLD = 2     # mark unhealthy after N consecutive fails
FAILOVER_COOLDOWN_S = 60        # skip unhealthy provider for this long
FAILOVER_TIMEOUT_S = 25         # fail over to fallback if primary slower than this

PERSONAS_REGISTRY_PATH = Path(os.environ.get("PERSONAS_REGISTRY", "/app/personas.json"))
AGENT_MD_PATH = Path(os.environ.get("AGENT_MD", "/app/AGENT.md"))

SLOT_FIRE_SECONDS = {
    "A": [3, 37],
    "B": [17, 45],
    "C": [25, 53],
}

# Each slot has a preferred x-lane so 3 agents naturally spread out instead of
# all clustering in the leftmost column. Their per-call prompt only suggests
# free zones inside their lane.
SLOT_LANES = {
    "A": {"x_min":   60, "x_max":  460, "label": "left column"},
    "B": {"x_min":  470, "x_max":  870, "label": "middle column"},
    "C": {"x_min":   60, "x_max":  870, "label": "below others (avoid header)"},
}

# Header card geometry (top-right; off-limits to agents)
HEADER = {
    "x": 920, "y": 20, "w": 460, "h": 200,
    "title_x": 940, "title_y": 30,
    "logo_x": 1330, "logo_y": 35, "logo_w": 32, "logo_h": 36,
    "line_x": 940, "line_w": 360,
    "line_ys": [110, 150, 190],
    "name_y_offset": -22,
}
HEADER_BLACK = "#1e1e1e"

# Discussion / Diagram zones — used for free-zone search + agent guidance
ZONES = {
    "discussion": {"x": 60, "y": 240, "w": 1340, "h": 640},   # y 240..880
    "diagram":    {"x": 60, "y": 900, "w": 1340, "h": 700},   # y 900..1600
}

# Text bbox estimation constants (for Excalidraw Virgil-like font)
CHAR_WIDTH_FACTOR = 0.55   # × fontSize
LINE_HEIGHT_FACTOR = 1.4   # × fontSize

# v4: per-slot in-band tidy disabled; replaced by dedicated CURATOR agent (see below)
TIDY_EVERY_N_ROUNDS = 9999   # effectively off

# v4: dedicated Curator agent. Fires every CURATOR_EVERY_N_ROUNDS rounds; other 3 pause.
CURATOR_EVERY_N_ROUNDS = 5

# v4: re-moderator. Every RE_MODERATE_EVERY_N_ROUNDS rounds, re-evaluate whether
# the 3 active personas still fit the evolved topic. May swap any/all of them.
RE_MODERATE_EVERY_N_ROUNDS = 10

# Limits per agent turn
MAX_ACTIONS = 3              # was 5 in v3 — encourage punchy reactions
MAX_TIDY_ACTIONS = 5
MAX_CURATOR_ACTIONS = 8
MAX_ERASE_PER_TURN = 1

# When canvas has been still for this long, agents are told silence is the default
STAGNATION_HINT_SECONDS = 60

# v4: post-LLM overlap auto-shift parameters (apply when placing new
# text/rectangle/ellipse/diamond — try to nudge Y down until clear).
OVERLAP_GAP = 8
OVERLAP_SHIFT_STEP = 50
OVERLAP_MAX_ATTEMPTS = 8

# v4: Curator persona — NOT in the discussion pool (personas.json). Hard-coded.
CURATOR_COLOR = "#868e96"  # neutral gray
CURATOR_SYSTEM_PROMPT = """You are anet.chat's Canvas Curator.

You are NOT one of the discussion personas. You do NOT add ideas, opinions, or content.
Your sole job is to keep the shared whiteboard READABLE for the other 3 personas and
the human user. You fire every 5 rounds. The other 3 personas pause while you think.

You can do these actions (each goes inside the "actions" array):
  - {"type":"move",   "id":"<full-or-prefix>", "x":<num>, "y":<num>}
       Relocate ANY non-header element (yours, other agents', NOT human).
  - {"type":"delete", "id":"<full-or-prefix>"}
       Delete ANY non-header element (yours, other agents', NOT human).
  - return {"reasoning":"<...>","actions":[]} when canvas is already clean.

Strict rules:
  - NEVER touch header-* elements.
  - NEVER touch elements with no strokeColor (those are human-authored — sacred).
  - NEVER add new content (no text/rectangle/ellipse/arrow). Only move/delete.
  - Don't move elements into header zone (x 900-1380, y 0-220) or off-canvas (negative).

Output format (STRICT JSON, no markdown fences, no prose outside):
{"reasoning":"<one short sentence>", "actions":[...]}

Decision heuristics (in order):
  1. If canvas has < 15 non-header elements → almost always actions:[].
     Premature reorganization is worse than mess.
  2. If 2+ same-color texts overlap badly → delete the older/shorter or move it.
  3. If a single color has > 6 text elements stacked vertically with < 30px gap → move
     the bottom 2-3 to an empty column (x>900 below y>220, or below y>900 diagram zone).
  4. If an EMPTY rectangle/ellipse/diamond (no text) exists → DELETE it. They are visual noise.
  5. If everything looks fine → actions:[] is the correct answer.

Prefer move over delete (preserve work). Cap of 8 actions per turn.
You will be told: canvas digest with full IDs + bboxes + colors, current active personas.
"""


# --------------------------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------------------------
def log(msg: str) -> None:
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


# --------------------------------------------------------------------------------------
# Persona registry
# --------------------------------------------------------------------------------------
@dataclass
class Persona:
    slug: str
    name: str
    color: str
    skill_path: str
    description: str
    persona_md: str = ""
    system_prompt: str = ""


def load_personas(agent_md: str) -> list[Persona]:
    registry = json.loads(PERSONAS_REGISTRY_PATH.read_text(encoding="utf-8"))
    personas: list[Persona] = []
    for entry in registry:
        path = Path(entry["skill"])
        try:
            md = path.read_text(encoding="utf-8")
        except Exception as exc:
            log(f"WARN: missing skill file for {entry['slug']} at {path}: {exc}")
            continue
        p = Persona(
            slug=entry["slug"],
            name=entry["name"],
            color=entry["color"].lower(),
            skill_path=str(path),
            description=entry.get("description", ""),
            persona_md=md,
        )
        p.system_prompt = md.strip() + "\n\n" + agent_md.strip()
        personas.append(p)
    return personas


# --------------------------------------------------------------------------------------
# Global state
# --------------------------------------------------------------------------------------
@dataclass
class State:
    pool: list[Persona]
    pool_by_slug: dict[str, Persona]
    active: dict[str, Optional[str]] = field(default_factory=lambda: {"A": None, "B": None, "C": None})
    phase: str = "WAITING_FOR_QUESTION"
    round_count: int = 0
    user_question_summary: str = ""
    # (legacy v3.1 — no longer used; v4 uses dedicated Curator)
    next_tidy_slot: Optional[str] = None
    last_tidy_trigger_round: int = 0
    last_canvas_change_ts: float = 0.0
    last_canvas_id_set: frozenset = field(default_factory=frozenset)
    busy: dict[str, bool] = field(default_factory=dict)
    seen_ids: dict[str, set] = field(default_factory=dict)
    last_fired: dict[str, float] = field(default_factory=lambda: {"A": 0.0, "B": 0.0, "C": 0.0})
    canvas_write_lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    moderator_lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    last_question_signature: str = ""
    # v4: system_active flag — curator OR re-moderator is currently running.
    # Agents (A/B/C) skip their tick while this is true.
    system_active: bool = False
    last_curator_round: int = 0
    last_re_moderation_round: int = 0
    # v3 / anet-souls-v2: SYNTHESIS phase trigger guard (so we run it once).
    synthesis_fired: bool = False
    # The signature of canvas content snapshot at the time of re-moderation, used to
    # avoid double-fires if the round counter doesn't advance.


def active_colors(state: State) -> set[str]:
    return {state.pool_by_slug[s].color for s in state.active.values() if s}


# --------------------------------------------------------------------------------------
# BBox helpers
# --------------------------------------------------------------------------------------
def estimate_bbox(element: dict) -> tuple[float, float, float, float]:
    x = float(element.get("x", 0) or 0)
    y = float(element.get("y", 0) or 0)
    t = element.get("type")
    if t == "text":
        fs = float(element.get("fontSize", 18) or 18)
        text = element.get("text") or ""
        lines = text.split("\n") if text else [""]
        max_len = max((len(line) for line in lines), default=0)
        w = max(max_len * fs * CHAR_WIDTH_FACTOR, 40)
        h = max(len(lines) * fs * LINE_HEIGHT_FACTOR, fs)
        return (x, y, x + w, y + h)
    w = float(element.get("width", 0) or 0)
    h = float(element.get("height", 0) or 0)
    return (min(x, x + w), min(y, y + h), max(x, x + w), max(y, y + h))


def bbox_overlap(a: tuple, b: tuple, gap: float = 0.0) -> bool:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return not (ax2 + gap <= bx1 or bx2 + gap <= ax1 or ay2 + gap <= by1 or by2 + gap <= ay1)


def point_inside_bbox(x: float, y: float, bbox: tuple, padding: float = 20) -> bool:
    bx1, by1, bx2, by2 = bbox
    return (bx1 - padding) <= x <= (bx2 + padding) and (by1 - padding) <= y <= (by2 + padding)


def is_dashed_rectangle(e: dict) -> bool:
    return (
        e.get("type") == "rectangle"
        and (e.get("strokeStyle") or "").lower() == "dashed"
    )


def is_header(eid: str) -> bool:
    return eid.startswith("header-")


def element_text(e: dict) -> str:
    t = e.get("text") or ""
    if not t and isinstance(e.get("label"), dict):
        t = e["label"].get("text", "") or ""
    return t


def author_of(e: dict, active_set: set[str]) -> str:
    eid = e.get("id", "")
    if is_header(eid):
        return "header"
    sc = (e.get("strokeColor") or "").lower()
    if not sc or sc in {"#000000", HEADER_BLACK, "black"}:
        return "human"
    if sc in active_set:
        return f"agent:{sc}"
    return "human"


# --------------------------------------------------------------------------------------
# Free-zone search (per-slot lane)
# --------------------------------------------------------------------------------------
def find_free_zones(elements: list[dict], zone_key: str,
                    x_min: Optional[float] = None, x_max: Optional[float] = None,
                    max_zones: int = 6) -> list[tuple[float, float]]:
    zone = ZONES[zone_key]
    candidate_w, candidate_h = 280, 32
    x_min = max(x_min if x_min is not None else zone["x"], zone["x"])
    x_max = min(x_max if x_max is not None else zone["x"] + zone["w"], zone["x"] + zone["w"])
    suggestions: list[tuple[float, float]] = []
    occupied = [estimate_bbox(e) for e in elements if not is_header(e.get("id", ""))]
    y_step = 50
    span = x_max - x_min - candidate_w
    if span < 0:
        return []
    if span < 200:
        x_positions = [x_min + 40]
    elif span < 500:
        x_positions = [x_min + 40, x_min + 40 + span // 2]
    else:
        x_positions = [x_min + 40, x_min + 40 + span // 3, x_min + 40 + (2 * span) // 3]
    y = zone["y"] + 20
    while y < zone["y"] + zone["h"] - candidate_h and len(suggestions) < max_zones:
        for x in x_positions:
            candidate_bbox = (x, y, x + candidate_w, y + candidate_h)
            if not any(bbox_overlap(candidate_bbox, occ, gap=-30) for occ in occupied):
                suggestions.append((x, y))
                if len(suggestions) >= max_zones:
                    break
        y += y_step
    return suggestions


# --------------------------------------------------------------------------------------
# HTTP helpers
# --------------------------------------------------------------------------------------
async def canvas_get_elements(client: httpx.AsyncClient) -> list[dict]:
    r = await client.get(f"{CANVAS_URL}/api/elements", timeout=10.0)
    r.raise_for_status()
    return r.json().get("elements", [])


async def canvas_post(client: httpx.AsyncClient, element: dict) -> Optional[dict]:
    try:
        r = await client.post(f"{CANVAS_URL}/api/elements", json=element, timeout=15.0)
        r.raise_for_status()
        return r.json().get("element")
    except Exception as exc:
        log(f"POST element failed: id={element.get('id','?')} exc={exc}")
        return None


async def canvas_put(client: httpx.AsyncClient, eid: str, patch: dict) -> bool:
    try:
        r = await client.put(f"{CANVAS_URL}/api/elements/{eid}", json=patch, timeout=10.0)
        r.raise_for_status()
        return True
    except Exception as exc:
        log(f"PUT {eid} failed: {exc}")
        return False


async def canvas_delete(client: httpx.AsyncClient, eid: str) -> bool:
    try:
        r = await client.delete(f"{CANVAS_URL}/api/elements/{eid}", timeout=8.0)
        return r.status_code in (200, 204)
    except Exception:
        return False


async def _call_minimax(system_prompt: str, user_prompt: str,
                         client: httpx.AsyncClient, max_tokens: int) -> str:
    payload = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }
    r = await client.post(
        f"{ANTHROPIC_BASE_URL}/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json=payload,
        timeout=FAILOVER_TIMEOUT_S,
    )
    r.raise_for_status()
    data = r.json()
    text_blocks = [b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"]
    return "\n".join(text_blocks).strip()


def _parse_responses_output(data: dict) -> str:
    """Common parser for OpenAI/Doubao Responses-API responses.
    output[].content[].text  OR  output_text  OR  choices[0].message.content"""
    parts: list[str] = []
    for out in data.get("output", []):
        if out.get("type") != "message":
            continue
        for c in out.get("content", []):
            t = c.get("text")
            if isinstance(t, str):
                parts.append(t)
    if parts:
        return "\n".join(parts).strip()
    ot = data.get("output_text")
    if isinstance(ot, str):
        return ot.strip()
    # Some Responses-API impls echo Chat Completions shape — accept it too.
    for choice in data.get("choices", []):
        msg = choice.get("message") or {}
        c = msg.get("content")
        if isinstance(c, str):
            parts.append(c)
    return ("\n".join(parts)).strip()


async def _call_openai_responses(system_prompt: str, user_prompt: str,
                                  client: httpx.AsyncClient, max_tokens: int) -> str:
    """OpenAI Responses API (tokhubs gpt-5.4) — primary provider.

    Note: tokhubs's gateway returns 502 when the `reasoning_effort` field is
    sent (it forces internal defaults). We omit it entirely. If the user
    needs explicit reasoning effort, they can set OPENAI_REASONING_EFFORT
    in the env AND we'll try it — but the default skip avoids the 502 trap.
    """
    payload = {
        "model": OPENAI_MODEL,
        "instructions": system_prompt,
        "input": user_prompt,
        "max_output_tokens": min(max_tokens, 16384),
    }
    # Only include reasoning_effort if explicitly requested via env (it can
    # break tokhubs — see comment above). Default: skip.
    if OPENAI_REASONING_EFFORT and OPENAI_REASONING_EFFORT.lower() != "default":
        payload["reasoning_effort"] = OPENAI_REASONING_EFFORT
    r = await client.post(
        f"{OPENAI_BASE}/v1/responses",
        headers={
            "Authorization": f"Bearer {OPENAI_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=FAILOVER_TIMEOUT_S,
    )
    r.raise_for_status()
    return _parse_responses_output(r.json())


async def _call_doubao(system_prompt: str, user_prompt: str,
                       client: httpx.AsyncClient, max_tokens: int) -> str:
    """Doubao Responses API — last-resort fallback."""
    payload = {
        "model": DOUBAO_MODEL,
        "instructions": system_prompt,
        "input": user_prompt,
        "max_output_tokens": min(max_tokens, 8192),
    }
    r = await client.post(
        DOUBAO_BASE,
        headers={
            "Authorization": f"Bearer {DOUBAO_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60.0,
    )
    r.raise_for_status()
    return _parse_responses_output(r.json())


def _provider_healthy(name: str) -> bool:
    return time.time() >= PROVIDER_HEALTH[name]["unhealthy_until"]


def _record_failure(name: str, exc: Exception) -> None:
    h = PROVIDER_HEALTH[name]
    h["consecutive_fails"] += 1
    if h["consecutive_fails"] >= FAILOVER_FAIL_THRESHOLD:
        h["unhealthy_until"] = time.time() + FAILOVER_COOLDOWN_S
        log(f"[provider:{name}] marked UNHEALTHY for {FAILOVER_COOLDOWN_S}s after "
            f"{h['consecutive_fails']} fails. last error: {exc}")


def _record_success(name: str) -> None:
    PROVIDER_HEALTH[name]["consecutive_fails"] = 0


async def call_llm(system_prompt: str, user_prompt: str, client: httpx.AsyncClient,
                   max_tokens: int = 8000) -> str:
    """Provider-aware LLM call with automatic fallback.

    Chain order: OpenAI/tokhubs (gpt-5.4)  →  MiniMax  →  Doubao
    Each tier is skipped if currently in cooldown. Consecutive failures
    drive cooldown windows.
    """
    last_exc: Optional[Exception] = None

    # ── 1. Primary: OpenAI/tokhubs gpt-5.4 ──────────────────────────────
    if OPENAI_AVAILABLE and _provider_healthy("openai"):
        try:
            txt = await _call_openai_responses(system_prompt, user_prompt, client, max_tokens)
            if txt:
                _record_success("openai")
                return txt
            _record_failure("openai", RuntimeError("empty response"))
        except Exception as exc:
            last_exc = exc
            _record_failure("openai", exc)
    elif not OPENAI_AVAILABLE:
        pass  # silent: not configured
    else:
        log(f"[provider] openai in cooldown, trying minimax")

    # ── 2. Fallback: MiniMax (Anthropic-compatible) ─────────────────────
    if _provider_healthy("minimax"):
        try:
            txt = await _call_minimax(system_prompt, user_prompt, client, max_tokens)
            if txt:
                _record_success("minimax")
                log(f"[provider] served via minimax")
                return txt
            _record_failure("minimax", RuntimeError("empty response"))
        except Exception as exc:
            last_exc = exc
            _record_failure("minimax", exc)
    else:
        log(f"[provider] minimax in cooldown, trying doubao")

    # ── 3. Last resort: Doubao ──────────────────────────────────────────
    if DOUBAO_AVAILABLE and _provider_healthy("doubao"):
        try:
            txt = await _call_doubao(system_prompt, user_prompt, client, max_tokens)
            if txt:
                _record_success("doubao")
                log(f"[provider] served via doubao")
                return txt
            _record_failure("doubao", RuntimeError("empty response"))
        except Exception as exc:
            last_exc = exc
            _record_failure("doubao", exc)

    raise RuntimeError(f"all providers failed: {last_exc}")


def extract_json(text: str) -> Optional[dict]:
    if not text:
        return None
    text = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.I)
    text = re.sub(r"\s*```$", "", text.strip())
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


# --------------------------------------------------------------------------------------
# Action → element payload
# --------------------------------------------------------------------------------------
def action_to_element(action: dict, color: str) -> Optional[dict]:
    # v5: dashed-style stripped — was creating empty decorative frames.
    t = action.get("type")
    common = {"strokeColor": color}
    try:
        if t == "text":
            return {
                **common, "type": "text",
                "x": float(action["x"]), "y": float(action["y"]),
                "text": str(action.get("text", ""))[:200],
                "fontSize": int(action.get("fontSize", 18)),
                "fontFamily": "1",
            }
        if t == "rectangle":
            # v5: reject empty shapes — they look like废稿
            text = str(action.get("text", "") or "").strip()
            if not text:
                log(f"  drop action: empty rectangle (no text)")
                return None
            return {
                **common, "type": "rectangle",
                "x": float(action["x"]), "y": float(action["y"]),
                "width": float(action.get("width", 160)),
                "height": float(action.get("height", 60)),
                "text": text[:80],
                "backgroundColor": "transparent",
            }
        if t == "ellipse":
            text = str(action.get("text", "") or "").strip()
            if not text:
                log(f"  drop action: empty ellipse (no text)")
                return None
            return {
                **common, "type": "ellipse",
                "x": float(action["x"]), "y": float(action["y"]),
                "width": float(action.get("width", 140)),
                "height": float(action.get("height", 80)),
                "text": text[:80],
                "backgroundColor": "transparent",
            }
        if t == "diamond":
            text = str(action.get("text", "") or "").strip()
            if not text:
                log(f"  drop action: empty diamond (no text)")
                return None
            return {
                **common, "type": "diamond",
                "x": float(action["x"]), "y": float(action["y"]),
                "width": float(action.get("width", 140)),
                "height": float(action.get("height", 80)),
                "text": text[:60],
                "backgroundColor": "transparent",
            }
        if t == "arrow":
            x1, y1 = float(action["x1"]), float(action["y1"])
            x2, y2 = float(action["x2"]), float(action["y2"])
            label = action.get("label")
            payload = {
                **common, "type": "arrow",
                "x": x1, "y": y1,
                "width": x2 - x1, "height": y2 - y1,
                "points": [[0, 0], [x2 - x1, y2 - y1]],
                "endArrowhead": "arrow",
            }
            if label:
                payload["text"] = str(label)[:40]
            return payload
        if t == "line":
            x1, y1 = float(action["x1"]), float(action["y1"])
            x2, y2 = float(action["x2"]), float(action["y2"])
            return {
                **common, "type": "line",
                "x": x1, "y": y1,
                "width": x2 - x1, "height": y2 - y1,
                "points": [[0, 0], [x2 - x1, y2 - y1]],
            }
    except (KeyError, ValueError, TypeError) as exc:
        log(f"action_to_element: bad action {action}: {exc}")
        return None
    return None


# --------------------------------------------------------------------------------------
# Prompt building
# --------------------------------------------------------------------------------------
PHASE_TABLE = [
    (6,  "BRAINSTORM",
     "找 1 个 hot point，punchy 反应。**不要一次性 dump 5 条角度**——每轮最多 1-2 个 action，1 行短字就够。"
     "**禁止画箭头**——只写 text。"),
    (12, "DISCUSSION",
     "盯住别人某句具体发言：在它**旁边**（≥ 60px 距离）写短评回应。**不要画箭头**——读者自己能看出邻近关系。≤ 2 actions/turn。"),
    (20, "DEBATE",
     "找最大分歧点，写一行锐评回应。需要加重时 fontSize 22-24。**禁止画框、禁止画箭头**。"),
    (30, "STRUCTURE",
     "进入 Diagram zone（y ≥ 900）：用**带 text 的** rectangle/diamond 画 flowchart/mindmap。**这是少数允许 arrow 的阶段**，连接节点用——禁止单纯指指点点的装饰箭头。"),
    (10**9, "SYNTHESIS",
     "Conclusion 时刻：前缀 'Conclusion:' + fontSize 24-28 的 text，**不要画框、不要画箭头**。"
     "**如果画板上已经有 ≥ 3 条 'Conclusion:' text 了，立即 SILENT (返回 actions:[]）——讨论已经收口，再加是噪音**。"),
]


def current_phase(round_count: int) -> tuple[str, str]:
    for upper, name, guidance in PHASE_TABLE:
        if round_count <= upper:
            return name, guidance
    return PHASE_TABLE[-1][1], PHASE_TABLE[-1][2]


def render_canvas_digest(elements: list[dict], active_set: set[str]) -> str:
    """Full IDs — DO NOT truncate (agents reference them in move/delete actions)."""
    lines = []
    for e in elements[-50:]:
        author = author_of(e, active_set)
        eid = e.get("id") or ""
        x1, y1, x2, y2 = estimate_bbox(e)
        sc = e.get("strokeColor") or "-"
        dash = "[dashed]" if is_dashed_rectangle(e) else ""
        txt = element_text(e)
        lines.append(
            f"- id={eid} {e.get('type','?'):9s} bbox=({x1:4.0f},{y1:4.0f})-({x2:4.0f},{y2:4.0f}) "
            f"color={sc:8s} by={author:14s} {dash} text={txt[:50]!r}"
        )
    return "\n".join(lines) or "  (empty)"


def render_own_elements(elements: list[dict], color: str) -> tuple[str, list[dict]]:
    own = [e for e in elements if (e.get("strokeColor") or "").lower() == color and not is_header(e.get("id", ""))]
    if not own:
        return "  (none — this is your first turn)", []
    lines = []
    for e in own[-30:]:
        eid = e.get("id", "")
        x1, y1, x2, y2 = estimate_bbox(e)
        txt = element_text(e)
        lines.append(f"- id={eid} type={e.get('type','?')} bbox=({x1:.0f},{y1:.0f})-({x2:.0f},{y2:.0f}) text={txt[:40]!r}")
    return "\n".join(lines), own


def render_overlaps(own: list[dict], all_elements: list[dict]) -> str:
    if not own:
        return "  (none)"
    others_by_id = {e["id"]: e for e in all_elements if not is_header(e.get("id", ""))}
    lines = []
    for o in own:
        o_bbox = estimate_bbox(o)
        clashes = []
        for other_id, other in others_by_id.items():
            if other_id == o["id"]:
                continue
            if bbox_overlap(o_bbox, estimate_bbox(other), gap=0):
                clashes.append(other_id)
        if clashes:
            o_text = element_text(o)
            lines.append(f"- YOUR id={o['id']} text={o_text[:40]!r} OVERLAPS: {clashes[:5]}")
    if not lines:
        return "  (none of your elements overlap others — clean)"
    return "\n".join(lines)


def render_dashed_rects(elements: list[dict]) -> str:
    rects = [e for e in elements if is_dashed_rectangle(e)]
    if not rects:
        return "  (none — to point an arrow at something, first emit a dashed rectangle around it)"
    lines = []
    for r in rects[-12:]:
        x1, y1, x2, y2 = estimate_bbox(r)
        txt = element_text(r)
        lines.append(f"- id={r['id']} bbox=({x1:.0f},{y1:.0f})-({x2:.0f},{y2:.0f}) text={txt[:30]!r}")
    return "\n".join(lines)


def render_free_zones(elements: list[dict], slot: str) -> str:
    """Per-slot free zones — each slot gets its own column to avoid 3-way collisions."""
    lane = SLOT_LANES[slot]
    disc = find_free_zones(elements, "discussion",
                           x_min=lane["x_min"], x_max=lane["x_max"], max_zones=4)
    diag = find_free_zones(elements, "diagram",
                           x_min=lane["x_min"], x_max=lane["x_max"], max_zones=3)
    lines = [f"YOUR PREFERRED LANE (slot {slot}): {lane['label']} (x {lane['x_min']}-{lane['x_max']})"]
    lines.append("[discussion zone (y 240-880), YOUR lane]:")
    if disc:
        lines.extend(f"  - try x={int(x)}, y={int(y)}" for (x, y) in disc)
    else:
        lines.append("  - (your lane is dense; consider y > 900 diagram zone)")
    lines.append("[diagram zone (y >= 900), YOUR lane]:")
    if diag:
        lines.extend(f"  - try x={int(x)}, y={int(y)}" for (x, y) in diag)
    else:
        lines.append("  - (your diagram lane is dense)")
    lines.append("(other slots have their own lanes — don't poach unless absolutely necessary)")
    return "\n".join(lines)


def build_user_prompt(state: State, slot: str, elements: list[dict],
                      is_tidy: bool) -> str:
    me = state.pool_by_slug[state.active[slot]]
    others_lines = []
    for other_slot in ["A", "B", "C"]:
        if other_slot == slot:
            continue
        other_slug = state.active.get(other_slot)
        if not other_slug:
            continue
        op = state.pool_by_slug[other_slug]
        others_lines.append(f"  - Slot {other_slot}: {op.name} ({op.color}) — {op.slug}")
    others_block = "\n".join(others_lines) if others_lines else "  (none)"

    phase_name, phase_guidance = current_phase(state.round_count)
    active_set = active_colors(state)
    digest = render_canvas_digest(elements, active_set)
    own_block, own_list = render_own_elements(elements, me.color)
    overlaps_block = render_overlaps(own_list, elements)
    free_zones_block = render_free_zones(elements, slot)

    seen = state.seen_ids.get(me.slug, set())
    new_externals = [
        e for e in elements
        if not is_header(e.get("id", ""))
        and e.get("id", "") not in seen
        and author_of(e, active_set) != f"agent:{me.color}"
    ]
    new_lines = []
    for e in new_externals[-8:]:
        author = author_of(e, active_set)
        new_lines.append(f"  - {e.get('id','?')[:10]} by={author} text={element_text(e)[:60]!r}")
    new_block = "\n".join(new_lines) if new_lines else "  (none — you may stay silent)"

    tidy_marker = ("\n[TIDY-UP ROUND] — you are the ONE picked agent this cycle. "
                   "MOVE or DELETE your overlapping own elements; no new content.\n") if is_tidy else ""

    seconds_quiet = int(time.time() - state.last_canvas_change_ts) if state.last_canvas_change_ts else 0
    stagnant_block = ""
    if seconds_quiet > STAGNATION_HINT_SECONDS and not is_tidy and not new_externals:
        stagnant_block = (
            f"\n[CANVAS STAGNANT] no new elements for {seconds_quiet}s. "
            "Default expectation: SILENCE (actions: []). Only speak if you've "
            "discovered a genuinely new angle you haven't expressed yet.\n"
        )

    # v3: build a 4-quadrant density map around the user question so the
    # agent can place its new element in the EMPTIEST direction. Avoids the
    # "vertical column streak" failure mode where everyone piles below.
    human_els_now = [e for e in elements
                     if not is_header(e.get("id", ""))
                     and author_of(e, active_set) == "human"]
    if human_els_now:
        hx = sum(e.get("x", 0) for e in human_els_now) / len(human_els_now)
        hy = sum(e.get("y", 0) for e in human_els_now) / len(human_els_now)
    else:
        hx, hy = 600.0, 400.0
    quad_counts = {"NE (上右)": 0, "NW (上左)": 0, "SE (下右)": 0, "SW (下左)": 0}
    for e in elements:
        if is_header(e.get("id", "")):
            continue
        ex, ey = e.get("x", 0), e.get("y", 0)
        if ex >= hx and ey < hy:   quad_counts["NE (上右)"] += 1
        elif ex < hx and ey < hy:  quad_counts["NW (上左)"] += 1
        elif ex >= hx and ey >= hy: quad_counts["SE (下右)"] += 1
        else:                       quad_counts["SW (下左)"] += 1
    quad_lines = "\n".join(f"  - {q}: {c} elements" for q, c in
                           sorted(quad_counts.items(), key=lambda kv: kv[1]))
    empty_quads = [q for q, c in quad_counts.items()
                   if c == min(quad_counts.values())]

    # v3: detect Conclusion saturation — count text elements starting with
    # "Conclusion:" (any agent). If 3+ exist, the discussion is closed.
    conclusion_count = 0
    for e in elements:
        if e.get("type") != "text" or is_header(e.get("id", "")):
            continue
        t = element_text(e).lstrip()
        if t.lower().startswith("conclusion") or t.startswith("结论"):
            conclusion_count += 1

    conclusion_block = ""
    if conclusion_count >= 3:
        conclusion_block = (
            f"\n[⚠️ CONCLUSION SATURATED — already {conclusion_count} 'Conclusion:' "
            f"texts on canvas]\nDiscussion is closed. **DO NOT write another Conclusion**.\n"
            f"Default = SILENCE (actions: []). Only speak if user just posted a NEW question.\n"
        )

    if is_tidy:
        closing = "You are in a TIDY-UP turn — output ONLY move/delete actions for your overlapping own elements."
    else:
        closing = (
            "[BEHAVIORAL EXPECTATION] You are NOT writing an essay.\n"
            "- Default: **1 action** per turn. Two is the absolute max.\n"
            "- **Avoid arrows.** Default to plain text only. Arrows allowed ONLY in STRUCTURE phase\n"
            "  for connecting flowchart/mindmap nodes — never as decoration or 'pointing'.\n"
            "- **Spread, don't streak.** Pick the emptiest quadrant (see [QUADRANT DENSITY] below)\n"
            "  and place at radius 250-450 from the centroid in that direction.\n"
            "- Find ONE hot point on the canvas you have a unique angle on — react PUNCHY.\n"
            "- Silence (`actions: []`) is the strong default when you have nothing punchy to add.\n"
            "- BAD: 4-5 parallel texts in a vertical column. BAD: arrows pointing at nothing.\n"
            "- Stay in character (use your signature vocabulary)."
        )

    return f"""[CONTEXT]
Your slot: {slot}    Your color: {me.color}    You are: {me.name} ({me.slug})
Other active personas:
{others_block}

Round: {state.round_count + (0 if is_tidy else 1)}    Phase: {phase_name}
Phase guidance: {phase_guidance}{tidy_marker}{stagnant_block}{conclusion_block}

[QUADRANT DENSITY around the user question @ ({hx:.0f},{hy:.0f})]
{quad_lines}
→ Place your new element in one of the LEAST-DENSE quadrant(s): {', '.join(empty_quads)}
   r = 250-450 from question centroid in that direction.

User's question / canvas context (paraphrased):
"{state.user_question_summary or '(none yet — work from canvas content directly)'}"

[CANVAS DIGEST] ({len(elements)} elements total)
{digest}

[YOUR OWN ELEMENTS] (color {me.color})
{own_block}

[YOUR OVERLAPPING ELEMENTS]
{overlaps_block}

[SUGGESTED FREE ZONES]
{free_zones_block}

[NEW SINCE YOU LAST LOOKED] ({len(new_externals)} items)
{new_block}

[YOUR TURN]
{closing}

Respond with the JSON object specified in AGENT.md. Never write outside the JSON.
"""


# --------------------------------------------------------------------------------------
# Apply actions with all validations
# --------------------------------------------------------------------------------------
def _auto_shift_action(action: dict, existing_bboxes: list[tuple]) -> Optional[dict]:
    """For a new positioned element, nudge Y down by OVERLAP_SHIFT_STEP up to
    OVERLAP_MAX_ATTEMPTS times to avoid overlap with existing elements. Returns
    the (possibly mutated) action, or None if it cannot be placed."""
    t = action.get("type")
    if t not in {"text", "rectangle", "ellipse", "diamond"}:
        return action
    try:
        x, y = float(action["x"]), float(action["y"])
    except (KeyError, ValueError, TypeError):
        return None
    # Synthetic bbox approximation (LLM-supplied dims may be wrong; use defaults)
    if t == "text":
        fs = float(action.get("fontSize", 18))
        text = str(action.get("text", "") or "")
        max_len = max((len(line) for line in text.split("\n")), default=0)
        w = max(max_len * fs * 0.55, 40)
        h = max(fs * 1.4, fs)
    else:
        w = float(action.get("width", 160))
        h = float(action.get("height", 60))
    for attempt in range(OVERLAP_MAX_ATTEMPTS + 1):
        bbox = (x, y, x + w, y + h)
        if not any(bbox_overlap(bbox, occ, gap=OVERLAP_GAP) for occ in existing_bboxes):
            if attempt > 0:
                # mutate the action so the posted element reflects the shift
                action = {**action, "y": y}
                log(f"  auto-shifted action down by {attempt * OVERLAP_SHIFT_STEP}px to y={y:.0f}")
            return action
        y += OVERLAP_SHIFT_STEP
    log(f"  drop action: cannot place ({t} text={action.get('text','')[:30]!r}) without overlap")
    return None


async def apply_actions(client: httpx.AsyncClient, actions: list[dict], persona: Persona,
                        current_elements: list[dict], is_tidy: bool,
                        is_curator: bool = False) -> dict[str, int]:
    counts = {"posted": 0, "moved": 0, "deleted": 0, "erased": 0, "dropped": 0, "shifted": 0}
    elements_by_id = {e["id"]: e for e in current_elements}
    # Pre-compute bboxes for non-header elements to use as overlap obstacles
    obstacle_bboxes = [estimate_bbox(e) for e in current_elements
                       if not is_header(e.get("id", ""))]

    def resolve_id(maybe_id: Optional[str]) -> Optional[str]:
        if not maybe_id or not isinstance(maybe_id, str):
            return None
        if maybe_id in elements_by_id:
            return maybe_id
        matches = [k for k in elements_by_id if k.startswith(maybe_id)]
        if len(matches) == 1:
            return matches[0]
        return None

    # v5: arrows may target ANY non-header element bbox (no more dashed-only constraint).
    # The old rule was creating perverse incentive to spam empty dashed rectangles.
    arrow_target_bboxes = [estimate_bbox(e) for e in current_elements
                           if not is_header(e.get("id", ""))]
    erased_this_turn = 0
    limit = MAX_TIDY_ACTIONS if is_tidy else MAX_ACTIONS

    for action in actions[:limit]:
        t = action.get("type")
        if not isinstance(t, str):
            counts["dropped"] += 1
            continue

        if t == "move":
            eid = resolve_id(action.get("id"))
            if not eid or is_header(eid):
                log(f"  move refused: id not resolved ({action.get('id')!r})")
                counts["dropped"] += 1; continue
            tgt = elements_by_id[eid]
            tgt_color = (tgt.get("strokeColor") or "").lower()
            if is_curator:
                # Curator may move ANY non-header non-human element
                if not tgt_color or tgt_color in {"#000000", HEADER_BLACK, "black"}:
                    log(f"  curator move refused: {eid} appears human-authored")
                    counts["dropped"] += 1; continue
            else:
                if tgt_color != persona.color:
                    log(f"  move refused: {eid} not owned by {persona.slug}")
                    counts["dropped"] += 1; continue
            try:
                nx = float(action["x"]); ny = float(action["y"])
            except (KeyError, ValueError, TypeError):
                counts["dropped"] += 1; continue
            ok = await canvas_put(client, eid, {"x": nx, "y": ny})
            if ok:
                counts["moved"] += 1
                log(f"  moved {eid} → ({nx:.0f},{ny:.0f})")
            else:
                counts["dropped"] += 1
            await asyncio.sleep(0.2)
            continue

        if t == "delete":
            eid = resolve_id(action.get("id"))
            if not eid or is_header(eid):
                log(f"  delete refused: id not resolved ({action.get('id')!r})")
                counts["dropped"] += 1; continue
            tgt = elements_by_id[eid]
            tgt_color = (tgt.get("strokeColor") or "").lower()
            if is_curator:
                if not tgt_color or tgt_color in {"#000000", HEADER_BLACK, "black"}:
                    log(f"  curator delete refused: {eid} appears human-authored")
                    counts["dropped"] += 1; continue
            else:
                if tgt_color != persona.color:
                    log(f"  delete refused: {eid} not owned by {persona.slug}")
                    counts["dropped"] += 1; continue
            ok = await canvas_delete(client, eid)
            if ok:
                counts["deleted"] += 1
                log(f"  deleted {eid} ({'curator' if is_curator else 'own'})")
            else:
                counts["dropped"] += 1
            await asyncio.sleep(0.2)
            continue

        if t == "erase":
            if erased_this_turn >= MAX_ERASE_PER_TURN:
                log(f"  erase refused: cap reached")
                counts["dropped"] += 1; continue
            eid = resolve_id(action.get("target_id"))
            reason = (action.get("reason") or "").strip()
            if not eid or is_header(eid) or len(reason) < 4:
                log(f"  erase refused: bad target/reason ({action.get('target_id')!r} reason={reason!r})")
                counts["dropped"] += 1; continue
            ok = await canvas_delete(client, eid)
            if ok:
                counts["erased"] += 1
                erased_this_turn += 1
                log(f"  erased external {eid} reason={reason!r}")
            else:
                counts["dropped"] += 1
            await asyncio.sleep(0.2)
            continue

        if is_tidy or is_curator:
            log(f"  {'CURATOR' if is_curator else 'TIDY'}: ignored non-move/delete action type={t}")
            counts["dropped"] += 1
            continue

        if t == "arrow":
            try:
                x2 = float(action["x2"]); y2 = float(action["y2"])
            except (KeyError, ValueError, TypeError):
                counts["dropped"] += 1; continue
            if not any(point_inside_bbox(x2, y2, bb, padding=20) for bb in arrow_target_bboxes):
                log(f"  arrow target ({x2:.0f},{y2:.0f}) not inside any element — dropped")
                counts["dropped"] += 1
                continue

        # v4: STRICT overlap enforcement for positioned new elements
        if t in {"text", "rectangle", "ellipse", "diamond"}:
            shifted = _auto_shift_action(action, obstacle_bboxes)
            if shifted is None:
                counts["dropped"] += 1
                continue
            if shifted is not action and shifted.get("y") != action.get("y"):
                counts["shifted"] += 1
            action = shifted

        el = action_to_element(action, persona.color)
        if el is None:
            counts["dropped"] += 1
            continue
        created = await canvas_post(client, el)
        if created:
            counts["posted"] += 1
            # Update obstacle list so subsequent actions in this turn also avoid the new
            new_bb = estimate_bbox(el)
            obstacle_bboxes.append(new_bb)
            arrow_target_bboxes.append(new_bb)
        else:
            counts["dropped"] += 1
        await asyncio.sleep(0.25)

    return counts


# --------------------------------------------------------------------------------------
# Agent tick
# --------------------------------------------------------------------------------------
async def agent_tick(slot: str, state: State, client: httpx.AsyncClient) -> None:
    slug = state.active.get(slot)
    if not slug or state.phase != "ACTIVE":
        return
    # v4: Curator or re-moderator is operating — agents pause.
    if state.system_active:
        log(f"[{slot}/-] system_active (curator/re-moderator) — skipping")
        return
    persona = state.pool_by_slug[slug]
    if state.busy.get(slug):
        log(f"[{slug}/{slot}] still busy — skipping")
        return

    state.busy[slug] = True
    try:
        is_tidy = (state.next_tidy_slot == slot)
        elements = await canvas_get_elements(client)
        active_set = active_colors(state)

        # NOTE: v3.1 — we do NOT skip on "no new external elements". The LLM is
        # always called; the agent decides silence via actions:[]. This fixes the
        # silent-stall problem where after a tidy round, every agent saw "no new"
        # and the conversation died.

        user_prompt = build_user_prompt(state, slot, elements, is_tidy)
        kind = "TIDY-UP" if is_tidy else current_phase(state.round_count)[0]
        log(f"[{slug}/{slot}] LLM call (round={state.round_count + (0 if is_tidy else 1)}, "
            f"kind={kind}, canvas={len(elements)})")

        try:
            llm_text = await call_llm(persona.system_prompt, user_prompt, client)
        except Exception as exc:
            log(f"[{slug}/{slot}] LLM call failed: {exc}")
            state.seen_ids[slug] = {e["id"] for e in elements}
            return

        obj = extract_json(llm_text)
        if not obj:
            log(f"[{slug}/{slot}] non-JSON ({len(llm_text)} chars). first200={llm_text[:200]!r}")
            state.seen_ids[slug] = {e["id"] for e in elements}
            return

        reasoning = (obj.get("reasoning") or "")[:140]
        intent = obj.get("phase_intent") or "?"
        actions = obj.get("actions") or []
        log(f"[{slug}/{slot}] phase_intent={intent} reasoning={reasoning!r} → {len(actions)} actions")

        if state.phase != "ACTIVE" or state.active.get(slot) != slug:
            log(f"[{slug}/{slot}] state changed during LLM call — abandoning")
            return

        async with state.canvas_write_lock:
            current = await canvas_get_elements(client)
            if not any(is_header(e.get("id", "")) for e in current):
                log(f"[{slug}/{slot}] canvas cleared during LLM call — abandoning")
                return
            counts = await apply_actions(client, actions, persona, current, is_tidy)
            log(f"[{slug}/{slot}] applied: {counts}")

            refreshed = await canvas_get_elements(client)
            state.seen_ids[slug] = {e["id"] for e in refreshed}

            if is_tidy:
                state.next_tidy_slot = None
                log(f"[{slug}/{slot}] tidy turn done.")
            else:
                state.round_count += 1
                # v4: every RE_MODERATE_EVERY_N_ROUNDS rounds → re-evaluate personas
                #     every CURATOR_EVERY_N_ROUNDS rounds → fire curator
                #     Re-moderator has priority. If round is divisible by both,
                #     re-moderator fires (curator will fire on next divisible round).
                if (state.round_count >= RE_MODERATE_EVERY_N_ROUNDS
                        and state.round_count % RE_MODERATE_EVERY_N_ROUNDS == 0
                        and state.round_count != state.last_re_moderation_round):
                    state.last_re_moderation_round = state.round_count
                    log(f"=== RE-MODERATION scheduled at round {state.round_count} ===")
                    asyncio.create_task(re_moderate_tick(state, client))
                elif (state.round_count >= CURATOR_EVERY_N_ROUNDS
                        and state.round_count % CURATOR_EVERY_N_ROUNDS == 0
                        and state.round_count != state.last_curator_round):
                    state.last_curator_round = state.round_count
                    log(f"=== CURATOR scheduled at round {state.round_count} ===")
                    asyncio.create_task(curator_tick(state, client))
    finally:
        state.busy[slug] = False


# --------------------------------------------------------------------------------------
# Curator tick (v4) — fires every CURATOR_EVERY_N_ROUNDS rounds; pauses A/B/C
# --------------------------------------------------------------------------------------
def build_curator_prompt(state: State, elements: list[dict]) -> str:
    active_set = active_colors(state)
    non_header = [e for e in elements if not is_header(e.get("id", ""))]
    lines = []
    for e in non_header[-60:]:
        eid = e.get("id", "")
        x1, y1, x2, y2 = estimate_bbox(e)
        sc = (e.get("strokeColor") or "-").lower()
        author = author_of(e, active_set)
        txt = element_text(e)
        lines.append(
            f"- id={eid} type={e.get('type','?'):9s} bbox=({x1:4.0f},{y1:4.0f})-({x2:4.0f},{y2:4.0f}) "
            f"color={sc:8s} by={author:14s} text={txt[:50]!r}"
        )
    digest = "\n".join(lines) or "  (canvas empty)"
    actives = []
    for slot in ["A", "B", "C"]:
        slug = state.active.get(slot)
        if slug:
            p = state.pool_by_slug[slug]
            actives.append(f"  - Slot {slot}: {p.name} (color {p.color})")
    actives_block = "\n".join(actives) if actives else "  (none)"
    return f"""[CURATOR CONTEXT]
Round: {state.round_count} (curator fires every {CURATOR_EVERY_N_ROUNDS} rounds).
Currently-discussing personas (do NOT touch their elements without good reason):
{actives_block}

Canvas digest ({len(non_header)} non-header elements):
{digest}

[YOUR TURN]
Decide: tidy or skip. Output the strict JSON object specified in your system prompt.
- If canvas looks fine → {{"reasoning":"clean enough","actions":[]}}.
- Otherwise → minimal move/delete actions. Capacity is {MAX_CURATOR_ACTIONS}; rarely use all.
NO text/rect/arrow/etc. Only move/delete.
"""


async def curator_tick(state: State, client: httpx.AsyncClient) -> None:
    if state.system_active or state.phase != "ACTIVE":
        return
    state.system_active = True
    try:
        elements = await canvas_get_elements(client)
        non_header_count = sum(1 for e in elements if not is_header(e.get("id", "")))
        log(f"[curator] LLM call at round {state.round_count} (canvas={non_header_count})")
        user_prompt = build_curator_prompt(state, elements)
        try:
            llm_text = await call_llm(CURATOR_SYSTEM_PROMPT, user_prompt, client, max_tokens=4000)
        except Exception as exc:
            log(f"[curator] LLM failed: {exc}")
            return
        obj = extract_json(llm_text)
        if not obj:
            log(f"[curator] non-JSON ({len(llm_text)} chars). first200={llm_text[:200]!r}")
            return
        reasoning = (obj.get("reasoning") or "")[:140]
        actions = (obj.get("actions") or [])[:MAX_CURATOR_ACTIONS]
        log(f"[curator] reasoning={reasoning!r} → {len(actions)} actions")
        if not actions:
            log(f"[curator] skip (canvas considered clean)")
            return
        # Fake "Persona" struct for apply_actions compatibility (color doesn't matter
        # for curator because is_curator=True bypasses the ownership check).
        curator_pseudo = Persona(
            slug="curator", name="Curator", color=CURATOR_COLOR,
            skill_path="", description="",
        )
        async with state.canvas_write_lock:
            current = await canvas_get_elements(client)
            if not any(is_header(e.get("id", "")) for e in current):
                log("[curator] canvas cleared mid-LLM — abandoning")
                return
            counts = await apply_actions(
                client, actions, curator_pseudo, current, is_tidy=False, is_curator=True
            )
            log(f"[curator] applied: {counts}")
    finally:
        state.system_active = False


# --------------------------------------------------------------------------------------
# Re-moderator tick (v4) — every RE_MODERATE_EVERY_N_ROUNDS rounds, may swap personas
# --------------------------------------------------------------------------------------
async def re_moderate_tick(state: State, client: httpx.AsyncClient) -> None:
    if state.system_active or state.phase != "ACTIVE":
        return
    state.system_active = True
    try:
        async with state.moderator_lock:
            elements = await canvas_get_elements(client)
            non_header = [e for e in elements if not is_header(e.get("id", ""))]
            # Build canvas summary: emphasize NEW content since the question was asked
            recent = non_header[-30:]
            recent_lines = []
            active_set = active_colors(state)
            for e in recent:
                author = author_of(e, active_set)
                t = element_text(e)
                if t:
                    recent_lines.append(f"  - by={author} text={t[:80]!r}")
            recent_block = "\n".join(recent_lines) or "  (no text on canvas yet)"
            current_actives = []
            for slot in ["A", "B", "C"]:
                slug = state.active.get(slot)
                if slug:
                    p = state.pool_by_slug[slug]
                    current_actives.append(f"  - Slot {slot}: {p.name} (slug={slug})")
            current_block = "\n".join(current_actives)

            log(f"[re-moderator] LLM call at round {state.round_count} "
                f"(canvas={len(non_header)} elements)")
            desc_list = "\n".join(
                f"- slug={p.slug}  name={p.name}  color={p.color}\n  description: {p.description}"
                for p in state.pool
            )
            system = (
                "You are anet.chat's moderator doing a MID-DISCUSSION re-evaluation. "
                "Given the original question, the topic evolution visible on the canvas, "
                "and the current 3 active personas, decide whether to KEEP the 3 or SWAP "
                "any of them with personas from the pool whose perspective would fit the "
                "current trajectory better. "
                "Output strict JSON only — no prose, no markdown fences."
            )
            user = f"""ORIGINAL USER QUESTION:
{state.user_question_summary or '(unknown)'}

CURRENTLY ACTIVE PERSONAS:
{current_block}

RECENT CANVAS CONTENT (showing how topic has evolved):
{recent_block}

FULL PERSONA POOL:
{desc_list}

DECISION:
Look at the canvas content — what is the discussion ACTUALLY about now? Has it drifted
into a domain where one of the current personas is no longer the best fit? Is there a
pool persona whose lens would unlock a NEW angle?

Output STRICT JSON of this exact shape:
{{
  "decision": "KEEP" | "SWAP",
  "summary": "<<= 100 chars: what the canvas is converging on>",
  "new_picks": [
    {{"slot":"A","slug":"<one-of-the-slugs>","reason":"<<=40 chars>"}},
    {{"slot":"B","slug":"<...>","reason":"<...>"}},
    {{"slot":"C","slug":"<...>","reason":"<...>"}}
  ]
}}
If decision is "KEEP", `new_picks` should be the current 3 (no change).
If decision is "SWAP", `new_picks` should contain at least one different slug from the
current actives. You may rearrange slots or replace personas freely.
"""
            try:
                text = await call_llm(system, user, client, max_tokens=4000)
            except Exception as exc:
                log(f"[re-moderator] LLM failed: {exc}")
                return
            obj = extract_json(text)
            if not obj:
                log(f"[re-moderator] non-JSON: {text[:200]!r}")
                return
            decision = (obj.get("decision") or "").upper()
            new_summary = (obj.get("summary") or "")[:200]
            new_picks_raw = obj.get("new_picks") or []
            log(f"[re-moderator] decision={decision} summary={new_summary!r}")

            # Validate
            valid_slugs = {p.slug for p in state.pool}
            new_assignment: dict[str, Optional[str]] = {"A": None, "B": None, "C": None}
            used_slugs: set[str] = set()
            for entry in new_picks_raw:
                slug = entry.get("slug")
                slot = entry.get("slot")
                if (slug in valid_slugs and slug not in used_slugs
                        and slot in {"A", "B", "C"} and new_assignment.get(slot) is None):
                    new_assignment[slot] = slug
                    used_slugs.add(slug)
            # Fill any missing slot
            for slot in ["A", "B", "C"]:
                if new_assignment[slot] is None:
                    for p in state.pool:
                        if p.slug not in used_slugs:
                            new_assignment[slot] = p.slug
                            used_slugs.add(p.slug)
                            break

            # Apply
            if decision == "SWAP" and new_assignment != state.active:
                old = dict(state.active)
                state.active = new_assignment
                log(f"[re-moderator] swap: {old} → {new_assignment}")
                # Re-prime seen_ids for newly assigned personas so they see existing
                # canvas content as new (so they actually react instead of staying silent).
                for slug in new_assignment.values():
                    if slug and slug not in {old.get("A"), old.get("B"), old.get("C")}:
                        state.seen_ids[slug] = set()
                # Update summary if moderator provided
                if new_summary:
                    state.user_question_summary = new_summary
                async with state.canvas_write_lock:
                    await paint_active_header(client, state)
            else:
                log(f"[re-moderator] KEEP — no change")
    finally:
        state.system_active = False


# --------------------------------------------------------------------------------------
# Moderator
# --------------------------------------------------------------------------------------
async def moderator_pick(state: State, question_context: str,
                         client: httpx.AsyncClient) -> list[tuple[str, str]]:
    desc_list = "\n".join(
        f"- slug={p.slug}  name={p.name}  color={p.color}\n  description: {p.description}"
        for p in state.pool
    )
    system = (
        "You are anet.chat's moderator. Given a user question and a pool of AI personas, "
        "you select EXACTLY 3 personas that together give the most COMPLEMENTARY perspectives. "
        "Avoid same-flavor picks. Output strict JSON only — no prose, no markdown fences."
    )
    user = f"""USER QUESTION / CANVAS CONTEXT:
{question_context}

PERSONA POOL ({len(state.pool)} available):
{desc_list}

Pick EXACTLY 3 distinct slugs. Assign to slots A, B, C in any order.
Output schema:
{{"picks":[
  {{"slot":"A","slug":"<one-of-the-slugs>","reason":"<<= 40 chars>"}},
  {{"slot":"B","slug":"<...>","reason":"<...>"}},
  {{"slot":"C","slug":"<...>","reason":"<...>"}}
],
"summary":"<= 60 chars paraphrase of the question"
}}
"""
    try:
        text = await call_llm(system, user, client, max_tokens=4000)
    except Exception as exc:
        log(f"moderator: LLM call failed: {exc}")
        text = ""
    obj = extract_json(text)
    valid_slugs = {p.slug for p in state.pool}
    if not obj or "picks" not in obj:
        log(f"moderator: invalid JSON, falling back to first-3. raw={text[:200]!r}")
        picks = [(state.pool[i].slug, slot) for i, slot in enumerate(["A", "B", "C"]) if i < len(state.pool)]
        return picks

    picks: list[tuple[str, str]] = []
    used_slugs: set[str] = set()
    used_slots: set[str] = set()
    for entry in obj["picks"]:
        slug = entry.get("slug")
        slot = entry.get("slot")
        reason = (entry.get("reason") or "")[:80]
        if slug in valid_slugs and slug not in used_slugs and slot in {"A", "B", "C"} and slot not in used_slots:
            picks.append((slug, slot))
            used_slugs.add(slug); used_slots.add(slot)
            log(f"moderator: pick {slot}={slug} ({reason})")

    for slot in ["A", "B", "C"]:
        if slot in used_slots:
            continue
        for p in state.pool:
            if p.slug in used_slugs:
                continue
            picks.append((p.slug, slot))
            used_slugs.add(p.slug); used_slots.add(slot)
            log(f"moderator: filler {slot}={p.slug}")
            break

    state.user_question_summary = (obj.get("summary") or "")[:200]
    return picks[:3]


# --------------------------------------------------------------------------------------
# Header painting
# --------------------------------------------------------------------------------------
async def clear_header(client: httpx.AsyncClient) -> None:
    elements = await canvas_get_elements(client)
    for e in elements:
        if is_header(e["id"]):
            await canvas_delete(client, e["id"])


async def paint_empty_header(client: httpx.AsyncClient) -> None:
    await clear_header(client)
    H = HEADER
    payloads = [
        {"id": "header-frame", "type": "rectangle",
         "x": H["x"], "y": H["y"], "width": H["w"], "height": H["h"],
         "strokeColor": HEADER_BLACK, "backgroundColor": "transparent",
         "strokeWidth": 2, "locked": True},
        {"id": "header-title", "type": "text",
         "x": H["title_x"], "y": H["title_y"],
         "text": "anet.chat", "fontSize": 24, "fontFamily": "1",
         "strokeColor": HEADER_BLACK, "locked": True},
        {"id": "header-logo", "type": "rectangle",
         "x": H["logo_x"], "y": H["logo_y"],
         "width": H["logo_w"], "height": H["logo_h"],
         "strokeColor": HEADER_BLACK, "backgroundColor": "transparent",
         "strokeWidth": 2, "locked": True},
    ]
    for i, ly in enumerate(H["line_ys"]):
        payloads.append({
            "id": f"header-line-{i+1}", "type": "line",
            "x": H["line_x"], "y": ly,
            "width": H["line_w"], "height": 0,
            "points": [[0, 0], [H["line_w"], 0]],
            "strokeColor": HEADER_BLACK, "strokeWidth": 2, "locked": True,
        })
    for p in payloads:
        await canvas_post(client, p)
        await asyncio.sleep(0.05)


async def paint_active_header(client: httpx.AsyncClient, state: State) -> None:
    H = HEADER
    elements = await canvas_get_elements(client)
    overlay_ids = {f"header-name-{i}" for i in (1, 2, 3)} | {f"header-stripe-{i}" for i in (1, 2, 3)}
    for e in elements:
        if e["id"] in overlay_ids:
            await canvas_delete(client, e["id"])

    stripe_h = H["logo_h"] // 3
    for i, slot in enumerate(["A", "B", "C"]):
        slug = state.active.get(slot)
        if not slug:
            continue
        p = state.pool_by_slug[slug]
        ly = H["line_ys"][i]
        await canvas_post(client, {
            "id": f"header-name-{i+1}", "type": "text",
            "x": H["line_x"], "y": ly + H["name_y_offset"],
            "text": f"{i+1}. {p.name}", "fontSize": 18, "fontFamily": "1",
            "strokeColor": p.color, "locked": True,
        })
        await canvas_post(client, {
            "id": f"header-stripe-{i+1}", "type": "rectangle",
            "x": H["logo_x"] + 4, "y": H["logo_y"] + 4 + i * stripe_h,
            "width": H["logo_w"] - 8, "height": max(stripe_h - 2, 6),
            "strokeColor": p.color, "backgroundColor": p.color,
            "fillStyle": "solid", "strokeWidth": 1, "locked": True,
        })
        await asyncio.sleep(0.05)


# --------------------------------------------------------------------------------------
# Watcher (canvas-clear + question detection + change tracking)
# --------------------------------------------------------------------------------------
async def watcher(state: State, client: httpx.AsyncClient) -> None:
    while True:
        try:
            elements = await canvas_get_elements(client)
        except Exception as exc:
            log(f"watcher: canvas fetch failed: {exc}")
            await asyncio.sleep(1.0)
            continue

        # Track canvas change timestamp for stagnation detection in prompts
        current_id_set = frozenset(e.get("id", "") for e in elements)
        if current_id_set != state.last_canvas_id_set:
            state.last_canvas_change_ts = time.time()
            state.last_canvas_id_set = current_id_set

        non_header = [e for e in elements if not is_header(e.get("id", ""))]
        header_count = len(elements) - len(non_header)

        if header_count == 0:
            log("watcher: no header. Repainting + resetting state.")
            async with state.canvas_write_lock:
                await paint_empty_header(client)
                state.active = {"A": None, "B": None, "C": None}
                state.phase = "WAITING_FOR_QUESTION"
                state.round_count = 0
                state.next_tidy_slot = None
                state.last_tidy_trigger_round = 0
                state.last_question_signature = ""
                state.last_canvas_change_ts = 0.0
                state.last_canvas_id_set = frozenset()
                state.system_active = False
                state.last_curator_round = 0
                state.last_re_moderation_round = 0
                state.synthesis_fired = False        # ready for next discussion
                for p in state.pool:
                    state.seen_ids[p.slug] = set()
            await asyncio.sleep(2.0)
            continue

        if state.phase == "WAITING_FOR_QUESTION" and non_header:
            active_set = active_colors(state)
            human_elements = [e for e in non_header if author_of(e, active_set) == "human"]
            if human_elements:
                sig = " ".join(sorted(element_text(e) for e in human_elements if element_text(e)))[:300]
                if sig and sig != state.last_question_signature:
                    log(f"watcher: question detected ({len(human_elements)} elements). Moderator.")
                    async with state.moderator_lock:
                        if state.phase == "WAITING_FOR_QUESTION":
                            question_context = "\n".join(
                                f"- {e.get('type')} at ({e.get('x',0):.0f},{e.get('y',0):.0f}): "
                                f"{element_text(e)!r}"
                                for e in human_elements
                            )
                            picks = await moderator_pick(state, question_context, client)
                            current = await canvas_get_elements(client)
                            if not any(is_header(e.get("id", "")) for e in current):
                                log("watcher: canvas cleared during moderator call — abandoning picks")
                            else:
                                state.active = {"A": None, "B": None, "C": None}
                                for slug, slot in picks:
                                    state.active[slot] = slug
                                log(f"watcher: active assignments: {state.active}")
                                async with state.canvas_write_lock:
                                    await paint_active_header(client, state)
                                for p in state.pool:
                                    state.seen_ids[p.slug] = set()
                                state.phase = "ACTIVE"
                                state.round_count = 0
                                state.next_tidy_slot = None
                                state.last_tidy_trigger_round = 0
                                state.last_question_signature = sig
                                state.last_canvas_change_ts = time.time()
                                state.synthesis_fired = False
                                # v2: kick off the first persona IMMEDIATELY so the
                                # user sees a reaction within seconds instead of
                                # waiting for the next :03/:17/:25 slot tick.
                                # The other 2 follow on their slot times.
                                asyncio.create_task(agent_tick("A", state, client))
                                await asyncio.sleep(0.5)
                                asyncio.create_task(agent_tick("B", state, client))
                                await asyncio.sleep(0.5)
                                asyncio.create_task(agent_tick("C", state, client))
        # v3: SYNTHESIS auto-trigger. Once 3+ "Conclusion:" texts pile up on
        # the canvas, the discussion is closed. Two picked agents do final
        # work: one writes a long-form summary on the left side, one builds
        # a mind-map on the right. Then all agent crons pause (FROZEN state)
        # until the canvas is cleared / new question arrives.
        if state.phase == "ACTIVE":
            conc = sum(
                1 for e in elements
                if e.get("type") == "text"
                and not is_header(e.get("id", ""))
                and (element_text(e).lstrip().lower().startswith("conclusion")
                     or element_text(e).lstrip().startswith("结论"))
            )
            if conc >= 3 and not state.synthesis_fired:
                state.synthesis_fired = True
                log(f"watcher: {conc} conclusions detected — triggering SYNTHESIS")
                asyncio.create_task(run_synthesis(state, client))

        await asyncio.sleep(1.0)


# --------------------------------------------------------------------------------------
# Scheduler
# --------------------------------------------------------------------------------------
async def scheduler(state: State, client: httpx.AsyncClient) -> None:
    log(f"scheduler armed (v4). A@:03/:37  B@:17/:45  C@:25/:53  "
        f"+CURATOR every {CURATOR_EVERY_N_ROUNDS} rounds (others pause)  "
        f"+RE-MODERATOR every {RE_MODERATE_EVERY_N_ROUNDS} rounds (may swap personas)")
    while True:
        now = dt.datetime.now()
        sec = now.second
        ts = now.timestamp()
        for slot, fire_seconds in SLOT_FIRE_SECONDS.items():
            if sec in fire_seconds:
                if ts - state.last_fired[slot] >= 10:
                    state.last_fired[slot] = ts
                    asyncio.create_task(agent_tick(slot, state, client))
        await asyncio.sleep(1.0)


# --------------------------------------------------------------------------------------
# SYNTHESIS phase — closing ceremony when conclusions saturate
# --------------------------------------------------------------------------------------
async def run_synthesis(state: State, client: httpx.AsyncClient) -> None:
    """When the discussion converges (3+ Conclusion: texts), freeze normal
    agent cron and run a final two-step closing:
      step 1: ONE picked agent writes a long-form summary at the left side
              (x=40-650, y=1300-1900) — paragraph form, 80-150 chars.
      step 2: ANOTHER picked agent builds a mind-map on the right
              (x=700-1380, y=1300-1900) — center ellipse + 4-6 radiating
              labeled child ellipses (no decorative arrows — just the
              radial links inherent to the mind-map shape).
    After both run, state.phase becomes 'FROZEN' so no further agent_tick
    fires until canvas is cleared or a new human question appears.
    """
    state.system_active = True   # halt scheduled ticks
    state.phase = "SYNTHESIS"
    try:
        active_slots = [s for s in ["A", "B", "C"] if state.active.get(s)]
        if len(active_slots) < 2:
            log("[synthesis] need >= 2 active personas, skipping")
            return

        # pick summarizer (most-verbose agent) + mindmapper (the other)
        elements = await canvas_get_elements(client)
        author_counts: dict[str, int] = {}
        active_set_now = active_colors(state)
        for e in elements:
            if is_header(e.get("id", "")):
                continue
            sc = (e.get("strokeColor") or "").lower()
            if sc in active_set_now:
                author_counts[sc] = author_counts.get(sc, 0) + 1
        # sort by element count desc
        ranked_slugs = sorted(
            [(slug, author_counts.get(state.pool_by_slug[slug].color.lower(), 0))
             for slug in state.active.values() if slug],
            key=lambda kv: -kv[1],
        )
        summarizer_slug = ranked_slugs[0][0]
        mindmapper_slug = ranked_slugs[1][0]
        log(f"[synthesis] summarizer={summarizer_slug}  mindmapper={mindmapper_slug}")

        # ── 1. long summary ────────────────────────────────────────────
        sum_persona = state.pool_by_slug[summarizer_slug]
        canvas_digest = render_canvas_digest(elements, active_set_now)
        sum_user = f"""[SYNTHESIS — long summary]

The discussion has reached convergence (3+ Conclusion: lines). The other
active personas wrote the bulk of opinions. As the most-vocal voice,
you write the closing paragraph.

Constraints:
- ONE create_element call with a single text element.
- Place at x=40, y=1300 (left side, below diagram zone).
- fontSize=18, width=620 (allow line-wrap by inserting \\n between sentences).
- text: 80-150 Chinese characters (or English equivalent), prose form.
- Stay in YOUR persona voice. Reference 1-2 specific Conclusion lines from
  the canvas. Add the missing thread that ties them together.
- strokeColor: {sum_persona.color}
- DO NOT add prefix "Conclusion:" — this IS the summary, not another bullet.

Canvas digest:
{canvas_digest}

Output the JSON {{actions:[{{type:"text", x:40, y:1300, text:"...", fontSize:18}}]}}.
"""
        try:
            text1 = await call_llm(sum_persona.system_prompt, sum_user, client, max_tokens=4000)
            obj1 = extract_json(text1) or {}
            for action in (obj1.get("actions") or [])[:1]:
                el = action_to_element(action, sum_persona.color)
                if el:
                    await canvas_post(client, el)
            log(f"[synthesis] summary posted by {summarizer_slug}")
        except Exception as exc:
            log(f"[synthesis] summary failed: {exc}")

        await asyncio.sleep(2.0)

        # ── 2. mind-map ────────────────────────────────────────────────
        mm_persona = state.pool_by_slug[mindmapper_slug]
        mm_user = f"""[SYNTHESIS — mind map]

Build a mind-map of the discussion's main ideas, placed in the bottom-right
area (x range 700-1380, y range 1300-1900).

Structure:
- ONE central ellipse at (1040, 1500), width=180, height=80, with the
  CORE topic of the discussion (8-12 chars) as text.
- 4-6 child ellipses around it (width=140, height=70), each labeled with
  one main insight from the canvas (8-15 chars). Place them at angles
  spread evenly: 0°, 60°, 120°, 180°, 240°, 300° at radius 250.
- ONE arrow from the center ellipse to each child (this is the rare
  allowed arrow case — they form the mind-map structure).
- Total ~10-12 actions (1 center + 5 children + 5 arrows).
- All elements in strokeColor: {mm_persona.color}.

Canvas digest (use this to pick what to highlight):
{canvas_digest}

Output JSON {{actions:[...]}} via batch (rectangle/ellipse with TEXT, arrow with start/end coords).
"""
        try:
            text2 = await call_llm(mm_persona.system_prompt, mm_user, client, max_tokens=4000)
            obj2 = extract_json(text2) or {}
            current = await canvas_get_elements(client)
            counts = await apply_actions(client, obj2.get("actions") or [],
                                         mm_persona, current, is_tidy=False)
            log(f"[synthesis] mind-map by {mindmapper_slug}: {counts}")
        except Exception as exc:
            log(f"[synthesis] mind-map failed: {exc}")

        state.phase = "FROZEN"
        log("[synthesis] done — phase=FROZEN. Clear canvas or post new question to resume.")
    finally:
        state.system_active = False


# --------------------------------------------------------------------------------------
# Startup
# --------------------------------------------------------------------------------------
async def main() -> None:
    log(f"loading personas registry from {PERSONAS_REGISTRY_PATH}")
    log(f"loading AGENT.md from {AGENT_MD_PATH}")
    agent_md = AGENT_MD_PATH.read_text(encoding="utf-8")
    pool = load_personas(agent_md)
    if not pool:
        log("FATAL: no personas loaded")
        sys.exit(2)
    for p in pool:
        log(f"  persona {p.slug}: name={p.name} color={p.color} skill_chars={len(p.persona_md)}")

    state = State(pool=pool, pool_by_slug={p.slug: p for p in pool})
    state.busy = {p.slug: False for p in pool}
    state.seen_ids = {p.slug: set() for p in pool}

    async with httpx.AsyncClient() as client:
        for attempt in range(40):
            try:
                r = await client.get(f"{CANVAS_URL}/health", timeout=3.0)
                if r.status_code == 200:
                    log(f"canvas reachable: {r.json()}")
                    break
            except Exception:
                pass
            log(f"waiting for canvas at {CANVAS_URL} (attempt {attempt + 1})")
            await asyncio.sleep(2.0)
        else:
            log("FATAL: canvas never came up")
            sys.exit(3)

        try:
            elements = await canvas_get_elements(client)
            non_header = [e for e in elements if not is_header(e.get("id", ""))]
            if not non_header:
                log("canvas is empty; painting fresh empty header")
                await paint_empty_header(client)
                state.phase = "WAITING_FOR_QUESTION"
            else:
                if not any(is_header(e.get("id", "")) for e in elements):
                    log("canvas has content but no header; painting empty header")
                    await paint_empty_header(client)
                for p in pool:
                    state.seen_ids[p.slug] = {e["id"] for e in elements}
                state.phase = "WAITING_FOR_QUESTION"
        except Exception as exc:
            log(f"initial setup failed: {exc}")

        await asyncio.gather(
            watcher(state, client),
            scheduler(state, client),
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("shutting down")
