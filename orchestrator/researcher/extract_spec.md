# Stage 1 — Per-paper Research-Cognition Extraction

Goal: surface the AUTHOR'S WAY OF THINKING from each paper md.
NOT a summary. Output one `extract.json` per paper, alongside the source md.

## Pipeline

1. Iterate every paper via `load_researchers.iter_researcher_papers(slug)`.
2. Skip if `extract.json` already exists and parses (resume on restart).
3. Pre-filter: if md char-count < 500 → write `extract.json` with `extraction_quality=thin`, no LLM call.
4. Truncate: md > 60k chars → keep first 40k + "\n\n[...TRUNCATED...]\n\n" + last 20k.
5. LLM call: claude-opus-4-7, max_tokens 2000, temperature 0.
6. Parse JSON output; on parse failure retry up to 3 times.
7. Write `extract.json` next to source md.

Concurrency: 6 in-flight calls. Per-call timeout 90s. Failures logged to `failures.jsonl` in repo root of researchers/.

## JSON schema (output of each call)

```json
{
  "paper_id":           "<paper_dir name verbatim>",
  "doi":                "<from doi.txt or null>",
  "title":              "<paper title, EN preferred, else original>",
  "year":               "<int or null>",
  "venue":              "<SIGCOMM / TPAMI / Nature / 计算机学报 / null>",
  "venue_tier":         "<top | strong | regional | workshop | unknown>",
  "role":               "<first | corresponding | co-author | senior | unknown>",

  "motivation":         "<≤40 字中文 / ≤25 EN words. 为什么做这个 — 真实驱动力, 不是 abstract 套话>",
  "problem_framing":    "<≤40 字. 他把问题界定成了什么. framing 本身就是 taste 的体现>",
  "key_insight":        "<≤50 字. 这篇真正吃饭的那句话. 不是方法名, 是 insight>",
  "method_signature":   "<≤40 字. 方法签名: 用了什么核心机制>",
  "evaluation_criteria":"<≤40 字. 他用什么指标判好坏 — 这透露评判标准>",

  "negative_result_or_admitted_limitation":
                        "<≤50 字. 他主动承认/放弃/批评什么 (taste 的最强信号之一). null if none>",

  "evidence_for_taste": [
    "<0-3 条直接引语 (原文片段, ≤30 字), 反映判断/品味/偏好>"
  ],

  "thinking_moves": [
    "<0-3 条. 可观察到的认知动作, 如 '从工程异常反推系统假设失效'>"
  ],

  "topic_tags":         ["<3-5 个细粒度 topic 标签, 用于 Stage 1.5 聚类>"],

  "cites_own_work":     ["<同作者前作 paper_id 列表, 若 md 中能识别. 否则空>"],

  "extraction_quality": "<full | partial | thin>",
  "extraction_notes":   "<只在 thin/partial 时填: 缺什么 (e.g. 'md 只有 abstract, 无 method 段')>"
}
```

## Prompt template

```
You are extracting research-cognition signals from a single academic paper.
Your goal is NOT to summarize the paper. Your goal is to surface the
AUTHOR'S WAY OF THINKING — what they consider a problem, what counts as
insight to them, how they judge whether something works.

Researcher slug: {slug}
Paper directory: {paper_dir_name}
DOI: {doi_or_none}

Paper markdown follows between <PAPER> tags. It may be:
  - full text (intro + method + eval + conclusion)
  - partial (abstract only, or method missing)
  - in Chinese, English, or mixed

<PAPER>
{md_content}
</PAPER>

Extract into the JSON schema below. STRICT rules:

1. GROUNDING: every non-null field must have direct textual evidence in
   <PAPER>. If <PAPER> is too thin to support a field, write null /
   "unknown" / [] and set extraction_quality accordingly. DO NOT GUESS
   year, venue, DOI, or author intent.

2. evidence_for_taste must be VERBATIM short fragments (≤30 chars each,
   原文 token), not paraphrase. Pick fragments that reveal judgment, not
   results — e.g. "we argue that ... is the wrong abstraction" beats
   "we achieve 99.2% accuracy".

3. thinking_moves describes the COGNITIVE MOVE behind the work, in your
   own words. Examples of good moves:
   - "从工程异常反推底层物理假设失效"
   - "先证最坏情况下界, 再做经验改进"
   - "把一个 perception 问题重新 frame 成 communication 问题"
   Bad (too generic, REJECT): "propose new method", "improve accuracy".

4. negative_result_or_admitted_limitation: look for sentences where the
   author admits a method DOESN'T work, gives up on an approach, or
   criticizes the field. This is often the strongest taste signal.

5. motivation / problem_framing / key_insight must each be DISTINCT.
   - motivation = WHY (动机, 现实痛点)
   - problem_framing = HOW THEY DEFINE IT (问题形式化, 已透露 taste)
   - key_insight = THE LEVER (吃饭的那句话)

6. topic_tags: 3-5 fine-grained tags (e.g. "RFID-localization",
   "screen-camera-comm", "embedding-regularization"). Used for
   cross-paper clustering in Stage 1.5. Prefer specific over generic.

7. Output exactly one JSON object, no surrounding prose, no markdown
   code fence.
```

## Stage 1.5 (next step after Stage 1 completes)

Per researcher, aggregate all `extract.json` into a single
`researcher_profile.json` that captures CROSS-PAPER patterns:
- topic clusters (group papers by topic_tags overlap)
- recurring thinking_moves (which appear in ≥3 papers?)
- evolution arc (year-sorted: where did interests shift?)
- consistent rejections (negative_result_or_admitted_limitation patterns)
- representative papers per cluster (highest-signal exemplars)

Then Stage 2 (soul.md) and Stage 5 (research_index) both feed from
`researcher_profile.json`, NOT from the raw 600+ extracts. This is what
gives cross-paper signal that pure one-by-one extraction would lose.
