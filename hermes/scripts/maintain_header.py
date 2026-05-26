#!/usr/bin/env python3
"""
anet.chat header maintainer.

Called by supervisor.sh every minute. Idempotent — if the header card is
missing (because user cleared canvas, or an agent went rogue), it repaints
the full card with locked=True on every element so the user can't move/edit it.

Header layout (top-right, 4 personas + 1 logo square + title):

    x=920                                        x=1380
y=20  ┌─────────────────────────────────────────┐
      │  anet.chat                       [▢]   │  y=30 title, y=35 logo
y=90  │  ─── 1. Richard Feynman                │
      │  ─── 2. Charlie Munger                 │
      │  ─── 3. Andrej Karpathy                │
y=210 │  ─── 4. Elon Musk                      │
y=260 └─────────────────────────────────────────┘

All header element IDs start with "header-" so they're filterable.
"""
import json
import os
import sys
import urllib.request

CANVAS_URL = os.environ.get("CANVAS_URL", "http://127.0.0.1:3000")

BLACK = "#1e1e1e"

# 4 active personas in display order. Curator is intentionally NOT shown — it's
# a system role, not a discussion participant.
PERSONAS = [
    ("feynman",  "1. Richard Feynman",  "#fa5252"),
    ("munger",   "2. Charlie Munger",   "#1c7ed6"),
    ("karpathy", "3. Andrej Karpathy",  "#37b24d"),
    ("musk",     "4. Elon Musk",        "#ff8c00"),
]

# Geometry
H = {
    "x": 920, "y": 20, "w": 460, "h": 240,
    "title_x": 940, "title_y": 30, "title_size": 24,
    "logo_x": 1330, "logo_y": 35, "logo_w": 32, "logo_h": 36,
    "line_x": 940, "line_w": 360,
    "row_ys": [90, 130, 170, 210],
    "name_y_offset": -18,
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


def expected_header_payloads():
    """Return all elements that the header card should contain."""
    elems = []

    # Outer frame
    elems.append({
        "id": "header-frame", "type": "rectangle",
        "x": H["x"], "y": H["y"], "width": H["w"], "height": H["h"],
        "strokeColor": BLACK, "backgroundColor": "transparent",
        "strokeWidth": 2, "locked": True,
    })
    # Title
    elems.append({
        "id": "header-title", "type": "text",
        "x": H["title_x"], "y": H["title_y"],
        "text": "anet.chat", "fontSize": H["title_size"], "fontFamily": "1",
        "strokeColor": BLACK, "locked": True,
    })
    # Logo (the small hollow square at top-right inside the frame)
    elems.append({
        "id": "header-logo", "type": "rectangle",
        "x": H["logo_x"], "y": H["logo_y"],
        "width": H["logo_w"], "height": H["logo_h"],
        "strokeColor": BLACK, "backgroundColor": "transparent",
        "strokeWidth": 2, "locked": True,
    })

    # 4 underline + name + color-stripe rows
    n = len(PERSONAS)
    stripe_h = H["logo_h"] // n
    for i, (slug, name, color) in enumerate(PERSONAS):
        ly = H["row_ys"][i]
        # Underline
        elems.append({
            "id": f"header-line-{i+1}", "type": "line",
            "x": H["line_x"], "y": ly,
            "width": H["line_w"], "height": 0,
            "points": [[0, 0], [H["line_w"], 0]],
            "strokeColor": color, "strokeWidth": 3, "locked": True,
        })
        # Name above underline
        elems.append({
            "id": f"header-name-{i+1}", "type": "text",
            "x": H["line_x"], "y": ly + H["name_y_offset"],
            "text": name, "fontSize": 18, "fontFamily": "1",
            "strokeColor": color, "locked": True,
        })
        # Color stripe inside the logo
        elems.append({
            "id": f"header-stripe-{i+1}", "type": "rectangle",
            "x": H["logo_x"] + 4, "y": H["logo_y"] + 4 + i * stripe_h,
            "width": H["logo_w"] - 8, "height": max(stripe_h - 2, 4),
            "strokeColor": color, "backgroundColor": color,
            "fillStyle": "solid", "strokeWidth": 1, "locked": True,
        })

    return elems


def main():
    try:
        data = http_get_json(f"{CANVAS_URL}/api/elements")
    except Exception as exc:
        print(f"[header] canvas fetch failed: {exc}", file=sys.stderr)
        return

    elements = data.get("elements", [])
    existing_ids = {e.get("id") for e in elements if (e.get("id") or "").startswith("header-")}

    expected = expected_header_payloads()
    expected_ids = {e["id"] for e in expected}

    missing = [e for e in expected if e["id"] not in existing_ids]
    stale = existing_ids - expected_ids   # any header-* that's no longer in the canonical set

    # Delete stale header elements (from older 3-slot version, etc)
    for eid in stale:
        http_delete(f"{CANVAS_URL}/api/elements/{eid}")

    if missing:
        # Paint missing elements
        for payload in missing:
            status, body = http_post_json(f"{CANVAS_URL}/api/elements", payload)
            if status >= 300:
                print(f"[header] POST {payload['id']} failed: {status} {body[:120]}", file=sys.stderr)
        print(f"[header] repainted {len(missing)} missing element(s); cleared {len(stale)} stale")
    elif stale:
        print(f"[header] cleared {len(stale)} stale element(s)")
    # else: silent — header intact


if __name__ == "__main__":
    main()
