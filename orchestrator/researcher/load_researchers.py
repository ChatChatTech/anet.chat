#!/usr/bin/env python3
"""
Unified loader for the 23 researcher persona corpora at
orchestrator/researcher/researchers/<slug>/.

22 of 23 follow the standard layout (each paper dir contains
`doi.txt` + `oa_W<id>.md`). yunhao_liu is special: no doi.txt, the
.md file inside each paper dir is named identically to the dir.
This loader normalizes both into the same API:

    >>> for slug, paper_dir, md_path, doi in iter_researcher_papers("yunhao_liu"):
    ...     print(paper_dir.name, doi)
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional

ROOT = Path(__file__).parent / "researchers"


@dataclass
class PaperEntry:
    slug: str           # researcher slug, e.g. "yunhao_liu"
    paper_dir: Path     # absolute path of the paper dir
    md_path: Path       # path to the markdown file (always exists)
    doi: Optional[str]  # DOI string, or None if not present (yunhao_liu)
    title: str          # paper title derived from dir name


def _read_doi(paper_dir: Path) -> Optional[str]:
    doi_file = paper_dir / "doi.txt"
    if doi_file.exists():
        try:
            return doi_file.read_text(encoding="utf-8").strip() or None
        except Exception:
            return None
    return None


def _find_md(paper_dir: Path) -> Optional[Path]:
    # 1. Standard convention: oa_W*.md
    for p in paper_dir.glob("oa_W*.md"):
        return p
    # 2. yunhao_liu convention: filename matches dir name
    same_name = paper_dir / f"{paper_dir.name}.md"
    if same_name.exists():
        return same_name
    # 3. Fallback: any .md in the dir
    for p in sorted(paper_dir.glob("*.md")):
        return p
    return None


def list_researchers() -> list[str]:
    """Return slugs of all available researchers, sorted alphabetically."""
    if not ROOT.exists():
        return []
    return sorted(p.name for p in ROOT.iterdir() if p.is_dir())


def iter_researcher_papers(slug: str) -> Iterator[PaperEntry]:
    """Yield every paper under researchers/<slug>/.
    Skips paper dirs that contain no readable .md file."""
    base = ROOT / slug
    if not base.exists():
        return
    for paper_dir in sorted(base.iterdir()):
        if not paper_dir.is_dir():
            continue
        md = _find_md(paper_dir)
        if md is None:
            continue
        yield PaperEntry(
            slug=slug,
            paper_dir=paper_dir,
            md_path=md,
            doi=_read_doi(paper_dir),
            title=paper_dir.name,
        )


def researcher_stats() -> list[dict]:
    """One-line stat per researcher: { slug, paper_count, with_doi, with_md }."""
    stats = []
    for slug in list_researchers():
        papers = list(iter_researcher_papers(slug))
        stats.append({
            "slug": slug,
            "paper_count": len(papers),
            "with_doi": sum(1 for p in papers if p.doi),
            "with_md": sum(1 for p in papers if p.md_path.exists()),
        })
    return stats


if __name__ == "__main__":
    # Quick CLI: python load_researchers.py [slug]
    import sys
    if len(sys.argv) > 1:
        target = sys.argv[1]
        for entry in iter_researcher_papers(target):
            doi = entry.doi or "(no DOI)"
            print(f"{entry.slug:18s} | {doi:35s} | {entry.title}")
    else:
        print(f"{'slug':20s} {'papers':>8s} {'doi':>6s} {'md':>6s}")
        print("-" * 50)
        for s in researcher_stats():
            print(f"{s['slug']:20s} {s['paper_count']:>8d} {s['with_doi']:>6d} {s['with_md']:>6d}")
