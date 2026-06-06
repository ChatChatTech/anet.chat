#!/usr/bin/env python3
"""
Export the 23 (+ 4 generic) personas as SillyTavern V2 character cards.

Each card is a JSON file containing:
- name: human-readable name (Chinese + English)
- description: one-line role/identity from soul.md
- personality: short personality blurb (we leave concise)
- system_prompt: FULL contents of orchestrator/personas/<slug>.md
                 (this is the runtime agent.md that anet.chat uses)
- first_mes: a neutral opener so ST UI shows something
- scenario: one-line setting
- mes_example: empty (we don't seed examples)
- creator: anet.chat
- tags: ["researcher", "anet.chat"]

ST V2 spec: outer envelope { spec: "chara_card_v2", spec_version: "2.0",
data: { name, description, personality, scenario, first_mes, mes_example,
system_prompt, post_history_instructions, tags, creator, ... } }

Output location: write each card to
  /data/projs/anetchat/sillytavern/data/default-user/characters/<slug>.json

The ST docker mount maps host:./data → container:/home/node/app/data,
so dropping files there is equivalent to importing them. ST loads
characters from this directory at next chat-list refresh.

Usage:
    python3 export_to_sillytavern.py             # all 27 personas
    python3 export_to_sillytavern.py yunhao_liu  # one
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ORCH = Path(__file__).parent.parent
PERSONAS_DIR = ORCH / "personas"
PERSONAS_JSON = ORCH / "personas.json"
RESEARCHERS_DIR = Path(__file__).parent / "researchers"
ST_CHAR_DIR = Path("/data/projs/anetchat/sillytavern/data/default-user/characters")

# Lorebook tuning
LORE_TOKEN_BUDGET = 1800        # cap on tokens ST injects from lorebook per turn
LORE_SCAN_DEPTH = 4             # scan the last N messages for keyword triggers
LORE_MAX_ENTRIES_PER_CARD = 80  # safety cap
LORE_MIN_PAPERS_PER_TAG = 2     # tags with single papers get bundled into misc
PAPERS_PER_TAG_ENTRY = 8        # cap papers listed in one entry
PAPER_LINE_FMT = "  - [{year}] {title} — {insight}"

# Bilingual key map — English topic tag prefix → Chinese alternates.
# Conservative: only common tags that anet.chat actually discusses in 中文.
# Anything not in this map is left English-only.
BILINGUAL_KEY_MAP = {
    "edge":          ["边缘", "边缘计算"],
    "federated":     ["联邦", "联邦学习"],
    "mobile":        ["移动", "移动端"],
    "satellite":     ["卫星", "星地"],
    "orbital":       ["卫星", "在轨"],
    "wireless":      ["无线", "无线感知"],
    "RFID":          ["RFID", "射频识别"],
    "WSN":           ["无线传感", "传感网"],
    "LLM":           ["大模型", "大语言模型"],
    "prompt":        ["提示", "提示学习"],
    "fine":          ["微调"],
    "privacy":       ["隐私"],
    "differential":  ["差分", "差分隐私"],
    "encryption":    ["加密", "同态加密"],
    "homomorphic":   ["同态", "同态加密"],
    "indoor":        ["室内", "室内定位"],
    "localization":  ["定位"],
    "scheduling":    ["调度"],
    "inference":     ["推理"],
    "code":          ["代码"],
    "graph":         ["图", "图神经网络"],
    "neural":        ["神经网络"],
    "reinforcement": ["强化学习"],
    "incremental":   ["增量", "增量学习"],
    "industrial":    ["工业", "工业互联网"],
    "blockchain":    ["区块链"],
    "agent":         ["代理", "智能代理"],
    "compress":      ["压缩"],
    "quantize":      ["量化"],
    "distill":       ["蒸馏", "知识蒸馏"],
}


def short_description(persona_md: str, fallback: str) -> str:
    """Pull the first 1-3 non-empty lines after the H1 as a description."""
    lines = persona_md.splitlines()
    # Skip H1 + blank
    for i, line in enumerate(lines):
        if line.startswith("# "):
            for nxt in lines[i+1:]:
                if nxt.strip() and not nxt.startswith("#"):
                    return nxt.strip()[:250]
            break
    return fallback


def _trunc(s: str | None, n: int) -> str:
    s = (s or "").strip()
    if len(s) <= n:
        return s
    return s[:n-1] + "…"


def build_lorebook(slug: str) -> dict | None:
    """Build a V2 character_book (lorebook) from the researcher's
    research_index.json + researcher_profile.json. Keys are derived from
    topic_tags so in-conversation mention of a tag triggers injection of
    that tag's paper list. Returns None if no index data exists (e.g.
    for generic personas feynman/munger/karpathy/musk).
    """
    idx_path = RESEARCHERS_DIR / slug / "research_index.json"
    profile_path = RESEARCHERS_DIR / slug / "researcher_profile.json"
    if not idx_path.exists():
        return None
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    profile = json.loads(profile_path.read_text(encoding="utf-8")) if profile_path.exists() else None

    by_id = idx.get("by_id", {})
    by_tag = idx.get("by_tag", {})
    anchors = idx.get("anchors", [])
    if not by_id:
        return None

    entries: list[dict] = []
    insertion_order = 100

    # 1) Anchors — always-on-ish entry keyed by the researcher's name/slug
    # so any mention of them surfaces their signature papers. Constant=true
    # would inject every turn; we leave constant=false to save tokens but
    # use the slug + name as keys.
    if anchors:
        lines = []
        for pid in anchors[:15]:
            info = by_id.get(pid, {})
            if info:
                lines.append(PAPER_LINE_FMT.format(
                    year=info.get("year") or "?",
                    title=_trunc(info.get("title") or pid, 80),
                    insight=_trunc(info.get("key_insight") or info.get("method_signature") or "", 90),
                ))
        if lines:
            entries.append({
                "id": insertion_order,
                "keys": [slug, slug.replace("_", " "), "anchor", "代表作", "signature paper"],
                "secondary_keys": [],
                "content": f"# {slug} signature papers\n" + "\n".join(lines),
                "comment": "Top-15 anchor papers (from soul.md §7)",
                "name": f"{slug} anchors",
                "enabled": True,
                "insertion_order": insertion_order,
                "case_sensitive": False,
                "selective": False,
                "constant": False,
                "position": "before_char",
                "priority": 10,
                "extensions": {},
            })
            insertion_order += 1

    # 2) Per-tag entries: one entry per topic_tag with ≥2 papers
    tag_papers = sorted(by_tag.items(), key=lambda kv: -len(kv[1]))
    used_pids: set[str] = set()
    for tag, pids in tag_papers:
        if len(pids) < LORE_MIN_PAPERS_PER_TAG:
            continue
        if len(entries) >= LORE_MAX_ENTRIES_PER_CARD - 5:
            break
        lines = []
        for pid in pids[:PAPERS_PER_TAG_ENTRY]:
            info = by_id.get(pid, {})
            if info:
                lines.append(PAPER_LINE_FMT.format(
                    year=info.get("year") or "?",
                    title=_trunc(info.get("title") or pid, 80),
                    insight=_trunc(info.get("key_insight") or info.get("method_signature") or "", 90),
                ))
            used_pids.add(pid)
        if not lines:
            continue
        # Derive key variants: e.g. "RFID-localization" → ["RFID-localization", "RFID localization", "RFID"]
        keys = {tag}
        if "-" in tag:
            keys.add(tag.replace("-", " "))
            # First chunk as a shorthand key (e.g. "RFID")
            keys.add(tag.split("-", 1)[0])
        if "_" in tag:
            keys.add(tag.replace("_", " "))
        # v22: bilingual aliases — if any token in the tag matches a known
        # English term, add its Chinese alternates. Allows 中文 questions
        # like "联邦学习的开放问题是什么" to trigger federated-learning entry.
        tag_lower = tag.lower()
        for en, zh_list in BILINGUAL_KEY_MAP.items():
            if en in tag_lower:
                keys.update(zh_list)
        entries.append({
            "id": insertion_order,
            "keys": sorted(keys),
            "secondary_keys": [],
            "content": f"# {tag} ({len(pids)} papers in {slug}'s corpus)\n" + "\n".join(lines),
            "comment": f"Topic cluster: {tag} ({len(pids)} papers)",
            "name": f"{tag}",
            "enabled": True,
            "insertion_order": insertion_order,
            "case_sensitive": False,
            "selective": False,
            "constant": False,
            "position": "before_char",
            "priority": 5,
            "extensions": {},
        })
        insertion_order += 1

    # 3) Recurring thinking moves (from profile) as a "how I think" entry
    if profile and profile.get("recurring_thinking_moves"):
        moves = profile["recurring_thinking_moves"][:8]
        body = "\n".join(
            f"  [×{m['count']}] {_trunc(m['move'], 120)}"
            for m in moves
        )
        entries.append({
            "id": insertion_order,
            "keys": [slug, "thinking", "认知", "方法论"],
            "secondary_keys": [],
            "content": f"# {slug} recurring thinking moves (cross-paper)\n{body}",
            "comment": "Recurring cognitive moves observed across the corpus.",
            "name": f"{slug} thinking moves",
            "enabled": True,
            "insertion_order": insertion_order,
            "case_sensitive": False,
            "selective": False,
            "constant": False,
            "position": "before_char",
            "priority": 8,
            "extensions": {},
        })
        insertion_order += 1

    if not entries:
        return None

    return {
        "name": f"{slug} corpus",
        "description": f"Auto-built world info from research_index.json + researcher_profile.json for {slug}. Per-tag entries fire when a tag keyword appears in recent messages.",
        "scan_depth": LORE_SCAN_DEPTH,
        "token_budget": LORE_TOKEN_BUDGET,
        "recursive_scanning": False,
        "extensions": {"source": "anet.chat researcher pipeline"},
        "entries": entries,
    }


def build_card(entry: dict) -> dict:
    """Construct a V2 character card dict from a personas.json entry."""
    slug = entry["slug"]
    name = entry["name"]
    color = entry["color"]
    description_oneline = entry.get("description", f"{name} — researcher persona")
    skill_path = PERSONAS_DIR / f"{slug}.md"
    if not skill_path.exists():
        raise FileNotFoundError(f"persona md not found: {skill_path}")
    persona_md = skill_path.read_text(encoding="utf-8")

    # First non-H1 line as personality blurb
    personality = short_description(persona_md, description_oneline)

    lorebook = build_lorebook(slug)

    return {
        "spec": "chara_card_v2",
        "spec_version": "2.0",
        "data": {
            "name": name,
            "description": description_oneline,
            "personality": personality,
            "scenario": "anet.chat 学术研讨会 — 一群被选上桌的研究者围着一块共享白板讨论研究问题。",
            "first_mes": "（在线，准备聆听问题。）",
            "mes_example": "",
            "system_prompt": persona_md.strip(),
            "post_history_instructions": "",
            "alternate_greetings": [],
            "character_book": lorebook,
            "tags": ["researcher", "anet.chat", slug],
            "creator": "anet.chat",
            "character_version": "1.0",
            "extensions": {
                "anet_chat": {
                    "slug": slug,
                    "color": color,
                }
            },
        },
        # Top-level mirrors for legacy V1 readers
        "name": name,
        "description": description_oneline,
        "personality": personality,
        "scenario": "anet.chat 学术研讨会",
        "first_mes": "（在线，准备聆听问题。）",
        "mes_example": "",
        "tags": ["researcher", "anet.chat", slug],
        "creator": "anet.chat",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="*", help="empty = all personas")
    args = ap.parse_args()

    registry = json.loads(PERSONAS_JSON.read_text(encoding="utf-8"))
    if args.slug:
        registry = [e for e in registry if e["slug"] in set(args.slug)]
        if not registry:
            print(f"no matching slugs in personas.json", file=sys.stderr)
            return 1

    ST_CHAR_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for entry in registry:
        try:
            card = build_card(entry)
        except FileNotFoundError as e:
            print(f"[skip] {entry['slug']:20s} {e}")
            continue
        out = ST_CHAR_DIR / f"{entry['slug']}.json"
        out.write_text(json.dumps(card, ensure_ascii=False, indent=2),
                       encoding="utf-8")
        print(f"[ok]   {entry['slug']:20s} {entry['name'][:40]:40s} {len(card['data']['system_prompt']):5d}B prompt")
        written += 1
    print(f"--- wrote {written} character cards to {ST_CHAR_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
