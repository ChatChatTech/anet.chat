"""
anet.chat hermes-bridge — sidecar that connects the Excalidraw canvas to Hermes.

Hermes has no native canvas watcher, so this small Python process:

  1. Polls the canvas REST API every 3s for state changes (canvas_get_elements).
  2. Tracks two transitions:
     - WAITING → ACTIVE: a NEW human-authored element appears on empty/header-only
       canvas. Bridge POSTs the user question to Hermes's /v1/runs endpoint
       with role=orchestrator; the orchestrator delegates to 3 persona swarm
       workers via Hermes Kanban.
     - ACTIVE → WAITING: canvas got cleared. Bridge cancels any running runs and
       resets state.
  3. Forwards canvas state to each persona on the v4 schedule (A@:03/:37,
     B@:17/:45, C@:25/:53) by POSTing to per-profile run endpoints.
  4. Curator (4th profile) is invoked every 5 normal rounds via Hermes's
     delegate_task pattern with the canvas snapshot as context.

This is significantly thinner than anet-souls — it does NOT decide actions,
generate prompts, or apply LLM output. It just routes:
  human-on-canvas → Hermes orchestrator → swarm of persona profiles
  Hermes-output → canvas via mcp_excalidraw MCP tool calls

Hermes does the actual LLM + tool-calling. The bridge only watches.

Status: SCAFFOLD. Hermes API / Swarm endpoints are placeholder. Once the
gateway is verified up and we know the exact /v1/runs payload shape, we
finalize the JSON.
"""

from __future__ import annotations

import asyncio
import datetime as dt
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx

# ---- config ----------------------------------------------------------------
CANVAS_URL = os.environ.get("CANVAS_URL", "http://canvas:3000")
HERMES_API = os.environ.get("HERMES_API", "http://hermes-gateway:8642")
HERMES_KEY = os.environ["API_SERVER_KEY"]

POLL_INTERVAL = 3.0          # canvas poll cadence
PERSONA_SLOTS = ["feynman", "munger", "karpathy", "musk"]
SLOT_FIRE = {
    "feynman":  [3, 37],
    "munger":   [17, 45],
    "karpathy": [25, 53],
    "musk":     [11, 41],     # 4th slot we'll experiment with
}
CURATOR_EVERY_N_ROUNDS = 5


# ---- state -----------------------------------------------------------------
@dataclass
class State:
    phase: str = "WAITING_FOR_QUESTION"
    active_question_sig: str = ""
    round_count: int = 0
    last_fired: dict = field(default_factory=lambda: {k: 0.0 for k in SLOT_FIRE})
    busy_personas: set = field(default_factory=set)
    last_curator_round: int = 0


def log(msg: str) -> None:
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


# ---- canvas access ---------------------------------------------------------
async def canvas_elements(client: httpx.AsyncClient) -> list[dict]:
    r = await client.get(f"{CANVAS_URL}/api/elements", timeout=10.0)
    r.raise_for_status()
    return r.json().get("elements", [])


def is_header(e: dict) -> bool:
    return (e.get("id") or "").startswith("header-")


def is_human(e: dict) -> bool:
    if is_header(e):
        return False
    sc = (e.get("strokeColor") or "").lower()
    return not sc or sc in {"#000000", "#1e1e1e", "black"}


# ---- Hermes API calls ------------------------------------------------------
async def hermes_run(client: httpx.AsyncClient, profile: str, prompt: str) -> Optional[str]:
    """POST to Hermes API server to trigger a run on a specific profile.
    Returns run_id, or None on failure. NB: this signature is best-effort —
    the actual Hermes payload schema is verified during bring-up."""
    payload = {
        "model": "hermes-agent",
        "profile": profile,                      # custom: select the profile
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    try:
        r = await client.post(
            f"{HERMES_API}/v1/runs",
            headers={"Authorization": f"Bearer {HERMES_KEY}"},
            json=payload,
            timeout=15.0,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("run_id") or data.get("id")
    except Exception as exc:
        log(f"hermes_run({profile}) FAILED: {exc}")
        return None


# ---- persona-trigger logic -------------------------------------------------
def make_persona_prompt(profile: str, canvas_elements: list[dict],
                        question: str, round_count: int) -> str:
    """Build the user-side prompt for a Hermes persona run. The persona's
    SOUL.md is already injected by Hermes as system prompt."""
    non_header = [e for e in canvas_elements if not is_header(e)]
    digest_lines = []
    for e in non_header[-30:]:
        eid = (e.get("id") or "")[:10]
        x, y = e.get("x", 0), e.get("y", 0)
        sc = e.get("strokeColor") or "-"
        txt = e.get("text") or ""
        if not txt and isinstance(e.get("label"), dict):
            txt = e["label"].get("text", "")
        author = "human" if is_human(e) else f"agent({sc})"
        digest_lines.append(f"  - id={eid} type={e.get('type','?')} @({x:.0f},{y:.0f}) color={sc} by={author} text={txt[:60]!r}")
    digest = "\n".join(digest_lines) or "  (empty)"

    return f"""You are firing for round {round_count} on the shared anet.chat canvas.

User's question (paraphrased): {question!r}

Canvas state ({len(non_header)} non-header elements):
{digest}

Your turn. Use your mcp_excalidraw tools to add 1-2 punchy elements that
react to the latest content in YOUR persona's voice. Stay in your color.
If you have nothing meaningful to add, output a single short reasoning
and skip the tool calls.

Available MCP tools include: batch_create_elements, create_element,
describe_scene (read-only canvas inspection), set_viewport. Prefer
batch_create_elements for adding multiple related elements.

Color discipline: every element you create must have
strokeColor matching your profile's signature color (defined in your SOUL.md).
"""


# ---- watcher loop ----------------------------------------------------------
async def watcher(state: State, client: httpx.AsyncClient) -> None:
    while True:
        try:
            elements = await canvas_elements(client)
        except Exception as exc:
            log(f"watcher: canvas fetch failed: {exc}")
            await asyncio.sleep(POLL_INTERVAL)
            continue

        non_header = [e for e in elements if not is_header(e)]
        human = [e for e in non_header if is_human(e)]

        # Detect WAITING → ACTIVE transition: new question on empty/cleared canvas
        if state.phase == "WAITING_FOR_QUESTION" and human:
            sig = " ".join(sorted((e.get("text") or "") for e in human))[:300]
            if sig and sig != state.active_question_sig:
                log(f"watcher: question detected — {sig[:80]!r}")
                state.active_question_sig = sig
                state.phase = "ACTIVE"
                state.round_count = 0
                state.last_curator_round = 0
                # Optional: trigger an orchestrator run to pick which 3 personas
                # are best for this question (TODO: implement delegate_task call)

        # Detect ACTIVE → WAITING transition: canvas cleared
        if state.phase == "ACTIVE" and not non_header:
            log(f"watcher: canvas cleared — resetting state")
            state.phase = "WAITING_FOR_QUESTION"
            state.active_question_sig = ""
            state.round_count = 0
            state.busy_personas.clear()

        await asyncio.sleep(POLL_INTERVAL)


# ---- scheduler loop --------------------------------------------------------
async def scheduler(state: State, client: httpx.AsyncClient) -> None:
    log(f"scheduler armed (hermes-bridge). slots: {SLOT_FIRE}")
    while True:
        now = dt.datetime.now()
        sec = now.second
        ts = now.timestamp()
        if state.phase == "ACTIVE":
            for profile, fire_seconds in SLOT_FIRE.items():
                if sec in fire_seconds and ts - state.last_fired[profile] >= 10:
                    if profile in state.busy_personas:
                        continue
                    state.last_fired[profile] = ts
                    asyncio.create_task(fire_persona(profile, state, client))
        await asyncio.sleep(1.0)


async def fire_persona(profile: str, state: State, client: httpx.AsyncClient) -> None:
    state.busy_personas.add(profile)
    try:
        elements = await canvas_elements(client)
        prompt = make_persona_prompt(profile, elements,
                                     state.active_question_sig, state.round_count + 1)
        log(f"hermes-bridge: firing {profile} at round {state.round_count + 1}")
        run_id = await hermes_run(client, profile, prompt)
        if run_id:
            log(f"hermes-bridge: {profile} → run_id={run_id}")
            state.round_count += 1
            # Curator after every 5 rounds
            if (state.round_count > 0
                    and state.round_count % CURATOR_EVERY_N_ROUNDS == 0
                    and state.round_count != state.last_curator_round):
                state.last_curator_round = state.round_count
                asyncio.create_task(fire_curator(state, client))
    finally:
        state.busy_personas.discard(profile)


async def fire_curator(state: State, client: httpx.AsyncClient) -> None:
    log(f"hermes-bridge: firing CURATOR at round {state.round_count}")
    elements = await canvas_elements(client)
    prompt = f"""You are firing as canvas curator at round {state.round_count}.

Canvas has {len(elements)} elements. Inspect via mcp_excalidraw describe_scene,
decide if cleanup is needed (per your SOUL.md heuristics), and apply minimal
move/delete operations only.

Report back with one-sentence summary.
"""
    await hermes_run(client, "curator", prompt)


# ---- entrypoint ------------------------------------------------------------
async def main() -> None:
    state = State()
    async with httpx.AsyncClient() as client:
        # Wait for canvas + hermes
        for _ in range(40):
            try:
                r = await client.get(f"{CANVAS_URL}/health", timeout=3.0)
                if r.status_code == 200:
                    log(f"canvas reachable")
                    break
            except Exception:
                await asyncio.sleep(2.0)
        else:
            log("canvas never came up; continuing anyway")

        await asyncio.gather(
            watcher(state, client),
            scheduler(state, client),
        )


if __name__ == "__main__":
    asyncio.run(main())
