#!/bin/bash
# anet.chat supervisor — runs every minute as a Hermes cron (--no-agent).
#
# Job: decide when to pause the 4 persona crons + curator cron.
# Termination conditions (per user spec):
#   1. HARD CAP: > 200 total non-human, non-header elements → pause all
#   2. SOFT CAP: > 50 agent elements since the last human-authored element
#      AND latest 8 agent texts show >= 5 identical-or-near-duplicate pairs
#      (repetition detector) → pause all
#
# When pausing, also drops a single gray "🔒 SESSION CLOSED" text on the canvas
# so the user can see we stopped.
#
# Resumption: when the user clears the canvas or posts a new human element,
# the cron jobs need to be RESUMED. Currently manual:
#   for p in feynman munger karpathy musk curator; do
#     hermes -p $p cron list | grep -oE '[0-9a-f]{12}' | head -1 | xargs hermes -p $p cron resume
#   done

set -e

CANVAS_URL="${CANVAS_URL:-http://127.0.0.1:3000}"
HARD_CAP=200
SOFT_CAP=50
HERMES="/opt/hermes/.venv/bin/hermes"

# Pull canvas JSON. Be defensive — silent exit on transient errors.
JSON=$(curl -sS -m 5 "$CANVAS_URL/api/elements" 2>/dev/null) || exit 0

# All decisions are in Python (jq isn't installed in the Hermes image).
DECISION=$(python3 - <<PY
import json, sys, re

data = json.loads("""$JSON""")
els = data.get("elements", [])

def is_header(e): return (e.get("id") or "").startswith("header-")
def is_human(e):
    if is_header(e): return False
    sc = (e.get("strokeColor") or "").lower()
    return not sc or sc in {"#000000","#1e1e1e","black"}
def is_agent(e):
    if is_header(e) or is_human(e): return False
    return bool(e.get("strokeColor"))

non_header = [e for e in els if not is_header(e)]
agents = [e for e in els if is_agent(e)]
humans = [e for e in els if is_human(e)]

# Already-stopped marker on canvas → noop
if any((e.get("text") or "").startswith("SESSION CLOSED") for e in els):
    print("ALREADY_STOPPED")
    sys.exit()

# HARD CAP
if len(agents) > $HARD_CAP:
    print("STOP_HARD_CAP", len(agents))
    sys.exit()

# SOFT CAP: count agent elements added AFTER the latest human element.
# Heuristic: order by createdAt if available; else by element list order.
def created_ts(e):
    return e.get("createdAt", "") or ""
els_by_age = sorted([e for e in non_header], key=created_ts)
if humans:
    last_human_ts = max(created_ts(e) for e in humans)
    agents_since_human = [e for e in agents if created_ts(e) > last_human_ts]
else:
    agents_since_human = agents

if len(agents_since_human) <= $SOFT_CAP:
    print("OK", len(agents), len(agents_since_human))
    sys.exit()

# Repetition detector: among last 8 agent texts, are >=5 pairs near-dupe?
def text_of(e):
    t = e.get("text") or ""
    if not t and isinstance(e.get("label"), dict):
        t = e["label"].get("text", "")
    return re.sub(r"\s+", " ", t.lower()).strip()[:120]
last8 = [text_of(e) for e in agents_since_human[-8:] if text_of(e)]
dupes = 0
for i in range(len(last8)):
    for j in range(i+1, len(last8)):
        a, b = last8[i], last8[j]
        if not a or not b: continue
        # cheap Jaccard on word sets
        wa, wb = set(a.split()), set(b.split())
        if not wa or not wb: continue
        sim = len(wa & wb) / len(wa | wb)
        if sim > 0.4:
            dupes += 1
if dupes >= 5:
    print("STOP_REPETITION", dupes)
    sys.exit()

print("OK", len(agents), len(agents_since_human), "dupes", dupes)
PY
)

DECIDED=$(echo "$DECISION" | awk '{print $1}')
echo "[supervisor] $(date -u +%H:%M:%S) decision=$DECISION"

case "$DECIDED" in
  ALREADY_STOPPED|OK)
    exit 0
    ;;
  STOP_HARD_CAP|STOP_REPETITION)
    # Pause every persona + curator cron.
    for p in feynman munger karpathy musk curator; do
      JOB=$("$HERMES" -p "$p" cron list 2>/dev/null | grep -oE '\b[0-9a-f]{12}\b' | head -1)
      [ -z "$JOB" ] && continue
      "$HERMES" -p "$p" cron pause "$JOB" 2>&1 | head -1 || true
    done
    # Drop a marker so the next supervisor tick is a noop.
    curl -sS -X POST "$CANVAS_URL/api/elements" \
      -H 'content-type: application/json' \
      -d "{\"type\":\"text\",\"x\":150,\"y\":1500,\"text\":\"SESSION CLOSED ($DECIDED)\",\"fontSize\":28,\"fontFamily\":\"1\",\"strokeColor\":\"#868e96\"}" > /dev/null
    echo "[supervisor] paused all persona crons. reason=$DECIDED"
    ;;
esac
