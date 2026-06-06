# Researcher-persona pipeline (anet.chat Stage 1→5)

Goal: distill 23 academic researchers' RESEARCH COGNITION
(not personal quirks) from 1453 papers into runtime personas
that "旁征博引" their own work on the anet.chat whiteboard.

## Layout

```
orchestrator/researcher/
├── load_researchers.py        # unified iterator (handles yunhao_liu special-case)
├── extract_spec.md            # Stage 1 schema + prompt doc
├── extract_papers.py          # Stage 1   — Opus 4.7 per-paper extraction
├── aggregate_profile.py       # Stage 1.5 — cross-paper pattern aggregation
├── soul_template.md           # Stage 2   — soul.md skeleton
├── generate_soul.py           # Stage 2-3 — gpt-5.5 soul.md generator
├── agent_template.md          # Stage 4   — agent.md skeleton
├── generate_agent.py          # Stage 4   — gpt-5.5 agent.md generator
├── research_index_schema.md   # Stage 5   — runtime index schema
├── build_index.py             # Stage 5   — mechanical index builder
├── run_stage1.sh              # batch driver for Stage 1
├── logs/                      # per-researcher batch logs
├── failures.jsonl             # failed-paper audit (append-only)
└── researchers/
    └── <slug>/
        ├── <paper_dir>/
        │   ├── doi.txt            (or absent for yunhao_liu)
        │   ├── *.md               (source paper)
        │   └── extract.json       ← Stage 1 output
        ├── researcher_profile.json ← Stage 1.5 output
        ├── soul.md                 ← Stage 2-3 output (or user-written for gold)
        ├── agent.md                ← Stage 4 output
        └── research_index.json     ← Stage 5 output
```

## Run order

```bash
# 1. Extract (long-running, resumable). Already automated via run_stage1.sh
bash run_stage1.sh

# 1.5 Aggregate cross-paper patterns
python3 aggregate_profile.py

# 5. Build runtime index (also re-runs after Stage 2 to pick up anchors from soul.md)
python3 build_index.py

# --- USER WRITES yunhao_liu/soul.md BY HAND HERE (gold standard) ---

# 2-3. Generate soul.md for the other 22 using yunhao_liu as few-shot
python3 generate_soul.py

# 4. Generate agent.md per researcher
python3 generate_agent.py

# 5 again. Re-build index so research_index.anchors picks up soul.md §7 entries.
python3 build_index.py

# Finally: wire into orchestrator/personas.json (manual or scripted).
```

## Why this shape

User's critique of pure one-by-one extraction was right: cross-paper
signal is where research taste lives. Stage 1.5 (`aggregate_profile.py`)
addresses this by clustering papers by topic_tags, surfacing recurring
thinking_moves (≥3 papers), and tracking evolution_arc + consistent
rejections. Stage 2 reads ONLY the aggregated profile, never the raw
600 extracts — so cross-paper patterns become the primary input.

## Models

- **Stage 1**: claude-opus-4-7 (Anthropic API via .env ANTHROPIC_*)
- **Stage 2-4**: gpt-5.5 via OPENAI_* (tokhubs base_url)
- **Stage 1.5 + 5**: pure Python, no LLM

## Pre-filtering

Papers with md < 500 chars get `extraction_quality=thin` with no LLM
call. These still appear in researcher_profile (as count) but don't
pollute clusters or thinking_moves.
