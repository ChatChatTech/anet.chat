#!/usr/bin/env python3
"""
Stage 6 — Wire the 23 researcher personas into orchestrator/personas.json.

For each researcher slug:
  1. Copy researchers/<slug>/agent.md → orchestrator/personas/<slug>.md
  2. Extract name + one-line description from researchers/<slug>/soul.md
  3. Assign a color from the 23-distinct palette
  4. Emit personas.json entry: {slug, name, color, skill, description}

Output:
  - Updates orchestrator/personas.json (preserves existing 4 generic
    personas: feynman, munger, karpathy, musk — by default appends).
  - Writes copies into orchestrator/personas/<slug>.md

Usage:
    python3 wire_personas.py                 # all (with confirmation diff)
    python3 wire_personas.py --apply         # actually write
    python3 wire_personas.py yunhao_liu      # single
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from load_researchers import list_researchers

ROOT = Path(__file__).parent
RESEARCHERS_ROOT = ROOT / "researchers"
ORCH = ROOT.parent
PERSONAS_DIR = ORCH / "personas"
PERSONAS_JSON = ORCH / "personas.json"

# Stable 23-color palette (kept distinct from 4 generics:
# feynman=#fa5252, munger=#1c7ed6, karpathy=#37b24d, musk=#ff8c00)
RESEARCHER_PALETTE = [
    "#845EF7", "#5C7CFA", "#22B8CF", "#15AABF", "#12B886",
    "#40C057", "#82C91E", "#FAB005", "#FD7E14", "#E64980",
    "#BE4BDB", "#7048E8", "#4263EB", "#1098AD", "#0CA678",
    "#74B816", "#F59F00", "#F76707", "#D6336C", "#AE3EC9",
    "#5F3DC4", "#364FC7", "#0B7285",
]


def extract_name_and_desc(soul_path: Path, slug: str) -> tuple[str, str]:
    """Parse soul.md:
       - name: text after first `# ` heading (strip trailing emoji etc.)
       - description: the first '> ...' blockquote line, OR if absent,
         the first non-empty non-heading paragraph.

    Falls back to slug if parsing fails."""
    if not soul_path.exists():
        return slug, f"researcher persona for {slug} (soul.md missing)"
    text = soul_path.read_text(encoding="utf-8")
    name = slug
    desc = f"researcher persona for {slug}"

    # name from first H1
    m = re.search(r"^#\s+(.+?)$", text, flags=re.MULTILINE)
    if m:
        name = m.group(1).strip().rstrip("#").strip()

    # description: first blockquote line after the H1
    m = re.search(r"^>\s+(.+?)$", text, flags=re.MULTILINE)
    if m:
        desc = m.group(1).strip()
    else:
        # fallback: first non-empty, non-heading line
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith(">"):
                continue
            desc = line[:200]
            break

    # cap description length
    if len(desc) > 200:
        desc = desc[:197] + "..."
    return name, desc


def slug_color(slug: str, palette_idx: int) -> str:
    return RESEARCHER_PALETTE[palette_idx % len(RESEARCHER_PALETTE)]


def build_entry(slug: str, palette_idx: int) -> dict | None:
    agent_src = RESEARCHERS_ROOT / slug / "agent.md"
    if not agent_src.exists():
        print(f"[skip] {slug:20s}  no agent.md")
        return None
    soul_path = RESEARCHERS_ROOT / slug / "soul.md"
    name, desc = extract_name_and_desc(soul_path, slug)
    return {
        "slug": slug,
        "name": name,
        "color": slug_color(slug, palette_idx),
        "skill": f"/app/personas/{slug}.md",
        "description": desc,
    }


def apply_changes(entries: list[dict], dry_run: bool) -> None:
    # 1. Load existing personas.json, preserve generic 4
    if PERSONAS_JSON.exists():
        existing = json.loads(PERSONAS_JSON.read_text(encoding="utf-8"))
    else:
        existing = []
    keep_slugs = {"feynman", "munger", "karpathy", "musk"}
    base = [p for p in existing if p.get("slug") in keep_slugs]
    new_slugs = {e["slug"] for e in entries}
    base = [p for p in base if p["slug"] not in new_slugs]
    merged = base + entries

    print(f"[plan] personas.json: {len(base)} generic + {len(entries)} researchers"
          f" = {len(merged)} total")
    for e in entries:
        agent_src = RESEARCHERS_ROOT / e["slug"] / "agent.md"
        agent_dst = PERSONAS_DIR / f"{e['slug']}.md"
        size = agent_src.stat().st_size
        action = "COPY" if not agent_dst.exists() else "OVERWRITE"
        print(f"  {action:9s}  {agent_dst.relative_to(ORCH)}  ({size} B)")

    if dry_run:
        print("[dry-run] no changes written. Re-run with --apply.")
        return

    PERSONAS_DIR.mkdir(exist_ok=True)
    for e in entries:
        shutil.copy2(RESEARCHERS_ROOT / e["slug"] / "agent.md",
                     PERSONAS_DIR / f"{e['slug']}.md")
    PERSONAS_JSON.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    print(f"[done] wrote {PERSONAS_JSON.relative_to(ORCH)} + "
          f"{len(entries)} persona files in personas/")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="*", help="researcher slug(s); empty = all")
    ap.add_argument("--apply", action="store_true",
                    help="actually write (default: dry-run)")
    args = ap.parse_args()

    slugs = args.slug or list_researchers()
    entries = []
    for i, slug in enumerate(slugs):
        e = build_entry(slug, i)
        if e:
            entries.append(e)

    if not entries:
        print("nothing to wire (no agent.md files found)")
        return 1
    apply_changes(entries, dry_run=not args.apply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
