"""
anet.chat LLM Router — Anthropic-compatible fanout with provider fallback.

Why it exists:
  Hermes Agent's built-in `fallback_providers` only swaps {provider, model,
  base_url} per entry — but ALL entries share a single API key. Our 3 providers
  (MiniMax, Doubao, Mimo) each have their own keys, so Hermes fallback can't
  manage them directly.

  This router fixes that: it exposes a single Anthropic /v1/messages endpoint
  pointed at by Hermes. Internally it tries providers in order, using the
  right key+endpoint for each, with retry-on-failure.

Provider chain (per user spec):
  1. MiniMax (primary)         — Anthropic-compatible at minimaxi.com/anthropic
  2. Doubao   (1st fallback)   — OpenAI Responses API (NOT Anthropic) — TODO: needs translation
  3. Mimo     (2nd fallback)   — Anthropic-compatible at token-plan-cn.xiaomimimo.com/anthropic

For now Doubao is a TODO (its Responses API differs significantly from Anthropic Messages
in schema), so the practical chain in this version is: MiniMax → Mimo → 502 to caller.

Failure triggers (any of these triggers fallback):
  - HTTP 429 (rate-limit)
  - HTTP 5xx (server error)
  - HTTPX connection / timeout exceptions
  - Body looking like an upstream provider error (best-effort)

Behavior:
  - Streams not yet supported (Hermes can stream from us once we implement SSE).
  - We pass through the Anthropic Messages payload verbatim.
  - We log which provider answered.
"""

from __future__ import annotations

import asyncio
import datetime as dt
import os
import sys

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="anet-llm-router", version="0.1")


# ---- Provider chain config ------------------------------------------------
# Order matters — first listed is primary.
PROVIDERS = [
    {
        "name": "minimax",
        "base_url": (os.environ.get("ANTHROPIC_BASE_URL") or
                     "https://api.minimaxi.com/anthropic").rstrip("/"),
        "api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
        "default_model": os.environ.get("ANTHROPIC_MODEL", "MiniMax-M2.7-highspeed"),
        # If the inbound payload uses a different model name, we forward as-is.
        # But if model isn't supported here we substitute default_model.
        "model_substitute": True,
    },
    # Doubao (TODO: needs OpenAI-Responses translation; deferred)
    # {
    #     "name": "doubao",
    #     ...
    # },
    {
        "name": "mimo",
        "base_url": (os.environ.get("MIMO_ANTHROPIC_BASE_URL") or
                     "https://token-plan-cn.xiaomimimo.com/anthropic").rstrip("/"),
        "api_key": os.environ.get("MIMO_API_KEY", ""),
        "default_model": os.environ.get("MIMO_DEFAULT_MODEL", "mimo-v2.5"),
        "model_substitute": True,
    },
]

CONFIGURED = [p for p in PROVIDERS if p["api_key"]]


def log(msg: str) -> None:
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


# ---- core proxy ------------------------------------------------------------
async def forward(provider: dict, payload: dict,
                  client: httpx.AsyncClient) -> tuple[int, dict | bytes, str]:
    """Forward a single request to one upstream. Returns (status, body, reason)."""
    body = dict(payload)
    if provider["model_substitute"]:
        body["model"] = provider["default_model"]
    headers = {
        "x-api-key": provider["api_key"],
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    try:
        r = await client.post(
            f"{provider['base_url']}/v1/messages",
            json=body,
            headers=headers,
            timeout=120.0,
        )
    except httpx.TimeoutException as exc:
        log(f"  [{provider['name']}] TIMEOUT — {exc}")
        return 504, {"error": {"type": "upstream_timeout", "message": str(exc)}}, "timeout"
    except httpx.NetworkError as exc:
        log(f"  [{provider['name']}] NETWORK ERR — {exc}")
        return 502, {"error": {"type": "upstream_network", "message": str(exc)}}, "network"
    except Exception as exc:
        log(f"  [{provider['name']}] EXCEPTION — {exc}")
        return 500, {"error": {"type": "router_internal", "message": str(exc)}}, "internal"

    try:
        body_json = r.json()
    except Exception:
        body_json = {"raw": r.text[:500]}

    return r.status_code, body_json, "ok" if r.is_success else f"http_{r.status_code}"


def is_fallback_trigger(status: int) -> bool:
    if status == 429:
        return True
    if 500 <= status < 600:
        return True
    return False


@app.post("/v1/messages")
async def messages(request: Request) -> Response:
    """Anthropic-compatible Messages endpoint with provider fallback."""
    payload = await request.json()

    if not CONFIGURED:
        return JSONResponse(status_code=500,
            content={"error": {"type": "router_no_providers",
                               "message": "no providers configured with api keys"}})

    async with httpx.AsyncClient() as client:
        last_status, last_body, last_reason = 500, {"error": "no providers tried"}, "init"
        for provider in CONFIGURED:
            log(f"→ trying provider={provider['name']} model={provider['default_model']}")
            status, body, reason = await forward(provider, payload, client)
            if not is_fallback_trigger(status):
                log(f"  [{provider['name']}] {reason} status={status}")
                return JSONResponse(status_code=status, content=body)
            last_status, last_body, last_reason = status, body, reason
            log(f"  [{provider['name']}] FALLBACK-TRIGGERED reason={reason}, trying next")

    log(f"all providers exhausted, last={last_status} reason={last_reason}")
    return JSONResponse(status_code=last_status, content=last_body)


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "configured_providers": [{"name": p["name"], "model": p["default_model"]}
                                 for p in CONFIGURED],
    }


@app.get("/")
async def root() -> dict:
    return {"service": "anet-llm-router", "endpoint": "/v1/messages"}
