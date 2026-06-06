#!/usr/bin/env python3
"""
Stage 1.5 — Per-researcher cross-paper aggregator.

Reads every extract.json under researchers/<slug>/ and synthesizes
ONE researcher_profile.json that captures CROSS-PAPER patterns:

  - topic_clusters:        papers grouped by topic_tags overlap
  - recurring_thinking_moves: moves that appear in ≥ THRESHOLD papers
  - evolution_arc:         year-bucketed snapshots of topic focus
  - consistent_rejections: negative_result patterns clustered
  - exemplar_papers:       top-N highest-signal per cluster

This is what Stage 2 (soul.md) and Stage 5 (research_index) feed from —
NOT the raw 600+ extracts. Solves the "lost cross-paper signal" problem
of pure one-by-one extraction.

Usage:
    python3 aggregate_profile.py                # all researchers
    python3 aggregate_profile.py yunhao_liu     # single researcher
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))
from load_researchers import (
    iter_researcher_papers,
    list_researchers,
)

ROOT = Path(__file__).parent
RESEARCHERS_ROOT = ROOT / "researchers"

# Tunables
RECURRING_MOVE_MIN = 3            # a move must appear in ≥3 papers to be "recurring"
EXEMPLARS_PER_CLUSTER = 5         # representative papers per topic cluster
CLUSTER_MIN_PAPERS = 3            # don't create a singleton cluster < 3 papers
MOVE_FUZZY_LEN = 8                # min char-prefix for fuzzy move dedup
TOP_TAGS = 30                     # cap on tags surfaced in profile


def load_extracts(slug: str) -> list[dict]:
    """Load every extract.json for a researcher. Skips missing/corrupt."""
    extracts = []
    for entry in iter_researcher_papers(slug):
        ep = entry.paper_dir / "extract.json"
        if not ep.exists():
            continue
        try:
            obj = json.loads(ep.read_text(encoding="utf-8"))
            obj["_paper_dir"] = str(entry.paper_dir.relative_to(RESEARCHERS_ROOT))
            extracts.append(obj)
        except Exception:
            continue
    return extracts


def _norm_move(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def cluster_thinking_moves(extracts: list[dict]) -> list[dict]:
    """Find thinking_moves that recur across ≥ RECURRING_MOVE_MIN papers.

    Fuzzy: two moves with same first MOVE_FUZZY_LEN chars (after norm)
    count as the same."""
    bucket: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for ex in extracts:
        seen_in_paper = set()
        for m in (ex.get("thinking_moves") or []):
            if not isinstance(m, str) or not m.strip():
                continue
            key = _norm_move(m)[:MOVE_FUZZY_LEN] or _norm_move(m)
            if key in seen_in_paper:
                continue
            seen_in_paper.add(key)
            bucket[key].append((ex.get("paper_id", "?"), m))

    out = []
    for key, occurrences in sorted(bucket.items(), key=lambda kv: -len(kv[1])):
        if len(occurrences) < RECURRING_MOVE_MIN:
            continue
        # canonical phrasing = longest one (assumed richest)
        canonical = max((m for _, m in occurrences), key=len)
        out.append({
            "move": canonical,
            "count": len(occurrences),
            "variants": sorted({m for _, m in occurrences}),
            "papers": [pid for pid, _ in occurrences],
        })
    return out


def cluster_by_topic(extracts: list[dict]) -> list[dict]:
    """Group papers by topic_tag co-occurrence using a simple
    union-find on shared tags. Tag-set size matters; we pick the
    'dominant tag' per cluster as its label."""
    tag_count = Counter()
    paper_tags: dict[str, set[str]] = {}
    for ex in extracts:
        tags = {t.strip() for t in (ex.get("topic_tags") or []) if isinstance(t, str) and t.strip()}
        if not tags:
            continue
        paper_tags[ex.get("paper_id", "?")] = tags
        tag_count.update(tags)

    if not paper_tags:
        return []

    # Use most-common tag as the cluster label, papers grouped by their
    # most-frequent tag (greedy, not perfect, but fast + interpretable).
    tag_to_papers: dict[str, list[str]] = defaultdict(list)
    for pid, tags in paper_tags.items():
        # pick the rarest tag (most discriminative) that still has ≥ CLUSTER_MIN_PAPERS total
        sorted_tags = sorted(tags, key=lambda t: tag_count[t])  # rarest first
        chosen = next((t for t in sorted_tags if tag_count[t] >= CLUSTER_MIN_PAPERS), sorted_tags[0])
        tag_to_papers[chosen].append(pid)

    clusters = []
    for tag, papers in sorted(tag_to_papers.items(), key=lambda kv: -len(kv[1])):
        if len(papers) < CLUSTER_MIN_PAPERS:
            continue
        clusters.append({
            "tag": tag,
            "paper_count": len(papers),
            "papers": papers,
        })
    return clusters


def signal_score(ex: dict) -> int:
    """Heuristic 'signal density' for ranking exemplars within a cluster.
    Higher = paper extract has more cognition-bearing content."""
    score = 0
    if ex.get("extraction_quality") == "full": score += 5
    elif ex.get("extraction_quality") == "partial": score += 2
    score += min(len(ex.get("thinking_moves") or []), 4)
    score += min(len(ex.get("evidence_for_taste") or []), 4)
    if ex.get("negative_result_or_admitted_limitation"): score += 3
    if ex.get("venue_tier") == "top": score += 4
    elif ex.get("venue_tier") == "strong": score += 2
    if ex.get("role") in ("first", "corresponding"): score += 2
    return score


def pick_exemplars(extracts: list[dict], clusters: list[dict]) -> list[dict]:
    by_id = {ex.get("paper_id"): ex for ex in extracts}
    out = []
    for c in clusters:
        ranked = sorted(
            (by_id[pid] for pid in c["papers"] if pid in by_id),
            key=signal_score,
            reverse=True,
        )[:EXEMPLARS_PER_CLUSTER]
        out.append({
            "tag": c["tag"],
            "paper_count": c["paper_count"],
            "exemplars": [
                {
                    "paper_id": ex.get("paper_id"),
                    "year": ex.get("year"),
                    "venue": ex.get("venue"),
                    "key_insight": ex.get("key_insight"),
                    "method_signature": ex.get("method_signature"),
                    "score": signal_score(ex),
                }
                for ex in ranked
            ],
        })
    return out


def evolution_arc(extracts: list[dict]) -> list[dict]:
    """Year-bucketed top-3 tags."""
    by_year: dict[int, Counter] = defaultdict(Counter)
    for ex in extracts:
        y = ex.get("year")
        if not isinstance(y, int) or y < 1990 or y > 2030:
            continue
        for t in (ex.get("topic_tags") or []):
            if isinstance(t, str) and t.strip():
                by_year[y][t.strip()] += 1
    return [
        {"year": y, "paper_count": sum(c.values()), "top_tags": c.most_common(3)}
        for y, c in sorted(by_year.items())
    ]


def cluster_rejections(extracts: list[dict]) -> list[str]:
    """Collect non-null negative_result strings (deduped)."""
    seen = []
    seen_norm = set()
    for ex in extracts:
        v = ex.get("negative_result_or_admitted_limitation")
        if not isinstance(v, str) or not v.strip():
            continue
        key = _norm_move(v)[:30]
        if key in seen_norm:
            continue
        seen_norm.add(key)
        seen.append(v.strip())
    return seen


def collect_evidence_quotes(extracts: list[dict], limit: int = 40) -> list[dict]:
    """Pull verbatim taste-signal quotes, sorted by paper signal score."""
    out = []
    for ex in sorted(extracts, key=signal_score, reverse=True):
        for q in (ex.get("evidence_for_taste") or []):
            if isinstance(q, str) and q.strip():
                out.append({"quote": q.strip(), "paper_id": ex.get("paper_id")})
                if len(out) >= limit:
                    return out
    return out


def build_profile(slug: str) -> Optional[dict]:
    extracts = load_extracts(slug)
    if not extracts:
        return None

    tag_counter = Counter()
    for ex in extracts:
        for t in (ex.get("topic_tags") or []):
            if isinstance(t, str) and t.strip():
                tag_counter[t.strip()] += 1

    clusters = cluster_by_topic(extracts)
    profile = {
        "slug": slug,
        "n_extracts": len(extracts),
        "n_full": sum(1 for ex in extracts if ex.get("extraction_quality") == "full"),
        "n_partial": sum(1 for ex in extracts if ex.get("extraction_quality") == "partial"),
        "n_thin": sum(1 for ex in extracts if ex.get("extraction_quality") == "thin"),
        "year_range": _year_range(extracts),
        "top_tags": tag_counter.most_common(TOP_TAGS),
        "topic_clusters": pick_exemplars(extracts, clusters),
        "recurring_thinking_moves": cluster_thinking_moves(extracts),
        "evolution_arc": evolution_arc(extracts),
        "consistent_rejections": cluster_rejections(extracts),
        "taste_quotes": collect_evidence_quotes(extracts),
    }
    return profile


def _year_range(extracts: list[dict]) -> Optional[list[int]]:
    years = [ex.get("year") for ex in extracts
             if isinstance(ex.get("year"), int) and 1990 <= ex["year"] <= 2030]
    if not years:
        return None
    return [min(years), max(years)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="*", help="researcher slug(s); empty = all")
    args = ap.parse_args()

    slugs = args.slug or list_researchers()
    for slug in slugs:
        prof = build_profile(slug)
        if not prof:
            print(f"[skip] {slug:20s}  no extracts yet")
            continue
        out_path = RESEARCHERS_ROOT / slug / "researcher_profile.json"
        out_path.write_text(json.dumps(prof, ensure_ascii=False, indent=2),
                            encoding="utf-8")
        print(f"[ok]   {slug:20s}  extracts={prof['n_extracts']:4d}  "
              f"full={prof['n_full']:4d}  partial={prof['n_partial']:4d}  "
              f"thin={prof['n_thin']:4d}  "
              f"clusters={len(prof['topic_clusters'])}  "
              f"recurring_moves={len(prof['recurring_thinking_moves'])}  "
              f"rejections={len(prof['consistent_rejections'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
