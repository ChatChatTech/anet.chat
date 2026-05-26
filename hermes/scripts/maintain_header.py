#!/usr/bin/env python3
"""
anet.chat header maintainer.

Reads /opt/data/state.json (written by moderator.py) to know which 3
personas are currently active. Paints the header card accordingly:

  - state.phase == "WAITING" (no human input yet) or 0 actives:
      Frame + title + small hollow logo + 3 EMPTY underlines.
      No names, no color stripes — pure caption window.

  - state.phase == "ACTIVE" with 3 actives:
      Frame + title + 3 colored stripes inside the logo +
      3 colored underlines with persona names above them.

All header elements are written with `locked: true` so the user cannot
move / edit / delete them via the Excalidraw UI.

Geometry: top-right corner, x=920..1380, y=20..240.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

CANVAS_URL = os.environ.get("CANVAS_URL", "http://127.0.0.1:3000")
DATA_DIR = "/opt/data"
STATE_PATH = f"{DATA_DIR}/state.json"
POOL_PATH = f"{DATA_DIR}/scripts/personas_pool.json"

BLACK = "#1e1e1e"

# Geometry — 3 underline rows (display is always 3 slots, regardless of pool size).
H = {
    "x": 920, "y": 20, "w": 460, "h": 240,
    "title_x": 940, "title_y": 30, "title_size": 24,
    "logo_x": 1330, "logo_y": 35, "logo_w": 32, "logo_h": 36,
    "line_x": 940, "line_w": 360,
    "row_ys": [110, 160, 210],
    "name_y_offset": -22,
}


def http_get_json(url, timeout=5):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_post_json(url, body, timeout=10):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")


def http_delete(url, timeout=5):
    req = urllib.request.Request(url, method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code


def load_state() -> dict:
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"phase": "WAITING", "active_slugs": []}


def load_pool() -> dict:
    try:
        with open(POOL_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def expected_header_payloads(state: dict, pool: dict) -> list[dict]:
    """Return the canonical list of header elements for the given state."""
    elems: list[dict] = []
    actives = state.get("active_slugs", []) or []

    # --- frame ---
    elems.append({
        "id": "header-frame", "type": "rectangle",
        "x": H["x"], "y": H["y"], "width": H["w"], "height": H["h"],
        "strokeColor": BLACK, "backgroundColor": "transparent",
        "strokeWidth": 2, "locked": True,
    })

    # --- title ---
    elems.append({
        "id": "header-title", "type": "text",
        "x": H["title_x"], "y": H["title_y"],
        "text": "anet.chat", "fontSize": H["title_size"], "fontFamily": "1",
        "strokeColor": BLACK, "locked": True,
    })

    # --- logo (small hollow square; gets color stripes only when ACTIVE) ---
    elems.append({
        "id": "header-logo", "type": "rectangle",
        "x": H["logo_x"], "y": H["logo_y"],
        "width": H["logo_w"], "height": H["logo_h"],
        "strokeColor": BLACK, "backgroundColor": "transparent",
        "strokeWidth": 2, "locked": True,
    })

    # --- 3 rows ---
    for i, ly in enumerate(H["row_ys"]):
        slug = actives[i] if i < len(actives) else None
        p = pool.get(slug) if slug else None
        # WAITING / unused slot → black underline, no name, no stripe
        if p is None:
            elems.append({
                "id": f"header-line-{i+1}", "type": "line",
                "x": H["line_x"], "y": ly,
                "width": H["line_w"], "height": 0,
                "points": [[0, 0], [H["line_w"], 0]],
                "strokeColor": BLACK, "strokeWidth": 2, "locked": True,
            })
            continue

        # ACTIVE slot — colored underline + name + stripe inside logo
        elems.append({
            "id": f"header-line-{i+1}", "type": "line",
            "x": H["line_x"], "y": ly,
            "width": H["line_w"], "height": 0,
            "points": [[0, 0], [H["line_w"], 0]],
            "strokeColor": p["color"], "strokeWidth": 3, "locked": True,
        })
        elems.append({
            "id": f"header-name-{i+1}", "type": "text",
            "x": H["line_x"], "y": ly + H["name_y_offset"],
            "text": f"{i+1}. {p['name']}", "fontSize": 18, "fontFamily": "1",
            "strokeColor": p["color"], "locked": True,
        })
        stripe_h = H["logo_h"] // 3
        elems.append({
            "id": f"header-stripe-{i+1}", "type": "rectangle",
            "x": H["logo_x"] + 4, "y": H["logo_y"] + 4 + i * stripe_h,
            "width": H["logo_w"] - 8, "height": max(stripe_h - 2, 4),
            "strokeColor": p["color"], "backgroundColor": p["color"],
            "fillStyle": "solid", "strokeWidth": 1, "locked": True,
        })

    return elems


def main():
    try:
        data = http_get_json(f"{CANVAS_URL}/api/elements")
    except Exception as exc:
        print(f"[header] canvas fetch failed: {exc}")
        return

    state = load_state()
    pool = load_pool()
    elements = data.get("elements", [])
    existing_ids = {e.get("id") for e in elements if (e.get("id") or "").startswith("header-")}

    expected = expected_header_payloads(state, pool)
    expected_ids = {e["id"] for e in expected}

    # IDs that exist on canvas but aren't in the canonical set → stale, delete
    stale = existing_ids - expected_ids
    for eid in stale:
        http_delete(f"{CANVAS_URL}/api/elements/{eid}")

    # IDs missing from canvas → paint them
    missing = [e for e in expected if e["id"] not in existing_ids]
    for payload in missing:
        status, body = http_post_json(f"{CANVAS_URL}/api/elements", payload)
        if status >= 300:
            print(f"[header] POST {payload['id']} failed: {status} {body[:120]}")

    # For elements that DO exist but might have wrong text/color/locked (e.g. an
    # active slot transitioned to a different persona), force-update them.
    for e in expected:
        if e["id"] not in existing_ids:
            continue
        existing = next((x for x in elements if x.get("id") == e["id"]), None)
        if not existing:
            continue
        # Detect any change worth re-POSTing
        text_changed = (existing.get("text") or "") != (e.get("text") or "")
        color_changed = (existing.get("strokeColor") or "").lower() != (e.get("strokeColor") or "").lower()
        if text_changed or color_changed:
            # Delete + recreate (canvas server may have schema gaps via PUT)
            http_delete(f"{CANVAS_URL}/api/elements/{e['id']}")
            http_post_json(f"{CANVAS_URL}/api/elements", e)

    if missing or stale:
        print(f"[header] phase={state.get('phase')} actives={state.get('active_slugs')} "
              f"painted={len(missing)} cleared={len(stale)}")


if __name__ == "__main__":
    main()
