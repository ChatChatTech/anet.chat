#!/usr/bin/env python3
"""
Stage 5 — Build per-researcher research_index.json.

Mechanical: reads every extract.json under researchers/<slug>/ and
materializes a fast lookup table:

  by_id   : paper_id → {title, year, venue, key_insight, method_signature, tags}
  by_tag  : topic_tag → [paper_id, ...]
  anchors : populated separately when soul.md §7 exists; for now empty

Used at runtime by orchestrator/main.py to expand `<paper_id>` refs
emitted by a researcher persona into full citations on the whiteboard.

Usage:
    python3 build_index.py            # all researchers
    python3 build_index.py yunhao_liu # single
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from load_researchers import iter_researcher_papers, list_researchers

ROOT = Path(__file__).parent
RESEARCHERS_ROOT = ROOT / "researchers"


def extract_anchors_from_soul(soul_path: Path) -> list[str]:
    """Parse soul.md §7 (标志性论文 / signature papers). One paper_id per line.

    Accepted formats:
      - `<paper_id> | <year> | <venue> | <note>`
      - `- <paper_id>: <note>`
    Lines outside §7 are ignored. Returns [] if soul.md missing or §7 not found."""
    if not soul_path.exists():
        return []
    text = soul_path.read_text(encoding="utf-8")
    # Find §7 header (## 7. ... or # 7 ...)
    m = re.search(r"##\s*7\.\s*\S.*$", text, flags=re.MULTILINE)
    if not m:
        return []
    section = text[m.end():]
    # Stop at next ## or end of file
    next_h = re.search(r"^##\s", section, flags=re.MULTILINE)
    if next_h:
        section = section[:next_h.start()]
    anchors = []
    for line in section.splitlines():
        line = line.strip().lstrip("-*• \t").strip()
        if not line:
            continue
        # paper_id is the first "|"-segment or "<paper_id>:" prefix
        if "|" in line:
            pid = line.split("|", 1)[0].strip()
        elif ":" in line:
            pid = line.split(":", 1)[0].strip()
        else:
            pid = line
        pid = pid.strip("`").strip()
        if pid and len(pid) >= 4:
            anchors.append(pid)
    return anchors


def build_index(slug: str) -> dict:
    by_id = {}
    by_tag = defaultdict(list)
    n_total = 0
    n_with_extract = 0
    for entry in iter_researcher_papers(slug):
        n_total += 1
        ep = entry.paper_dir / "extract.json"
        if not ep.exists():
            continue
        try:
            ex = json.loads(ep.read_text(encoding="utf-8"))
        except Exception:
            continue
        n_with_extract += 1
        pid = ex.get("paper_id") or entry.paper_dir.name
        by_id[pid] = {
            "title":            ex.get("title"),
            "year":             ex.get("year"),
            "venue":            ex.get("venue"),
            "doi":              ex.get("doi") or entry.doi,
            "key_insight":      ex.get("key_insight"),
            "method_signature": ex.get("method_signature"),
            "tags":             ex.get("topic_tags") or [],
            "quality":          ex.get("extraction_quality"),
        }
        for t in (ex.get("topic_tags") or []):
            if isinstance(t, str) and t.strip():
                by_tag[t.strip()].append(pid)

    anchors = extract_anchors_from_soul(RESEARCHERS_ROOT / slug / "soul.md")

    return {
        "slug": slug,
        "n_papers": n_total,
        "n_indexed": n_with_extract,
        "anchors": anchors,
        "by_id": by_id,
        "by_tag": {k: sorted(v) for k, v in sorted(by_tag.items(), key=lambda kv: -len(kv[1]))},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="*", help="researcher slug(s); empty = all")
    args = ap.parse_args()
    slugs = args.slug or list_researchers()
    for slug in slugs:
        idx = build_index(slug)
        out_path = RESEARCHERS_ROOT / slug / "research_index.json"
        out_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2),
                            encoding="utf-8")
        print(f"[ok] {slug:20s}  papers={idx['n_papers']:4d}  "
              f"indexed={idx['n_indexed']:4d}  "
              f"tags={len(idx['by_tag']):3d}  anchors={len(idx['anchors'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
