#!/usr/bin/env python3
"""
Quality-check pass over extract.json files.

Flags:
  - motivation == problem_framing (prompt says they must be distinct)
  - motivation == key_insight
  - empty thinking_moves AND extraction_quality != thin
  - empty evidence_for_taste AND extraction_quality == full
  - paper_id mismatch (extract.paper_id != paper_dir name)
  - JSON parse errors

Usage:
    python3 qc_extracts.py                  # all researchers
    python3 qc_extracts.py yunhao_liu       # one
    python3 qc_extracts.py --fix-paper-id   # rewrite mismatched paper_id

Output: prints flagged paths + reason, exits 0 (informational).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from load_researchers import iter_researcher_papers, list_researchers

ROOT = Path(__file__).parent
RESEARCHERS_ROOT = ROOT / "researchers"


def check_one(extract_path: Path, paper_dir_name: str) -> list[str]:
    issues = []
    try:
        ex = json.loads(extract_path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"json-parse-error: {e}"]

    qual = ex.get("extraction_quality")
    motiv = (ex.get("motivation") or "").strip()
    frame = (ex.get("problem_framing") or "").strip()
    insight = (ex.get("key_insight") or "").strip()
    moves = ex.get("thinking_moves") or []
    evidence = ex.get("evidence_for_taste") or []

    if motiv and frame and motiv == frame:
        issues.append("motivation==problem_framing")
    if motiv and insight and motiv == insight:
        issues.append("motivation==key_insight")
    if frame and insight and frame == insight:
        issues.append("problem_framing==key_insight")
    if qual != "thin" and not moves:
        issues.append("empty-thinking_moves (not-thin)")
    if qual == "full" and not evidence:
        issues.append("empty-evidence (full)")
    if ex.get("paper_id") != paper_dir_name:
        issues.append(f"paper_id-mismatch (got '{ex.get('paper_id')}', expected '{paper_dir_name}')")
    return issues


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="*", help="empty = all")
    ap.add_argument("--fix-paper-id", action="store_true")
    args = ap.parse_args()
    slugs = args.slug or list_researchers()

    total = 0
    flagged = 0
    by_reason: dict[str, int] = {}

    for slug in slugs:
        for entry in iter_researcher_papers(slug):
            ep = entry.paper_dir / "extract.json"
            if not ep.exists():
                continue
            total += 1
            issues = check_one(ep, entry.paper_dir.name)
            if not issues:
                continue
            flagged += 1
            print(f"[{slug}] {entry.paper_dir.name}")
            for i in issues:
                print(f"    - {i}")
                by_reason[i.split()[0]] = by_reason.get(i.split()[0], 0) + 1

            if args.fix_paper_id and any("paper_id-mismatch" in i for i in issues):
                obj = json.loads(ep.read_text(encoding="utf-8"))
                obj["paper_id"] = entry.paper_dir.name
                ep.write_text(json.dumps(obj, ensure_ascii=False, indent=2),
                              encoding="utf-8")
                print(f"    + fixed paper_id")

    print(f"\n--- {flagged}/{total} extracts flagged ---")
    for k, v in sorted(by_reason.items(), key=lambda kv: -kv[1]):
        print(f"  {v:5d}  {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
