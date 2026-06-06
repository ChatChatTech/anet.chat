# Stage 5 — research_index.json schema

Per-researcher lightweight runtime lookup table. The agent at runtime
references papers by `paper_id` (short); the orchestrator resolves
those into full citation details from this index BEFORE injecting
into the prompt or rendering on the whiteboard.

This solves: agent must "旁征博引" fast, but we don't want to bloat
the system_prompt with 600+ paper entries. Solution:
1. soul.md §7 lists 10-15 anchor papers IN the prompt
2. research_index.json contains ALL papers, queryable by topic_tag
3. When agent says "see {paper_id}", caller looks it up and inlines the
   1-line key_insight from this index.

## Schema

```json
{
  "slug": "yunhao_liu",
  "n_papers": 674,
  "by_id": {
    "<paper_id>": {
      "title": "<paper title>",
      "year": <int or null>,
      "venue": "<venue or null>",
      "key_insight": "<from extract.json>",
      "method_signature": "<from extract.json>",
      "tags": ["<tag1>", "<tag2>", ...]
    }
  },
  "by_tag": {
    "<topic_tag>": ["<paper_id>", "<paper_id>", ...]
  },
  "anchors": [
    "<paper_id of soul.md §7 entries>"
  ]
}
```

## Use at runtime

```python
# In orchestrator main.py, when an agent message mentions paper_ids:
idx = json.load(open(f"researcher/researchers/{slug}/research_index.json"))
for pid in extracted_paper_refs:
    info = idx["by_id"].get(pid)
    if info:
        rendered_citation = f"[{info['year']}|{info['venue']}] {info['title']}"
        # caller renders this on the whiteboard or in agent's sticky note
```

## On-disk size

For yunhao_liu (674 papers): expect ~150-250 KB of JSON, totally fine
to keep in memory. For the smaller researchers: < 50 KB each.
Total across 23: < 3 MB.
