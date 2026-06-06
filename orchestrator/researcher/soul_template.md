# Soul Template — Research-Cognition Profile

Used by Stage 2 to generate soul.md per researcher. The user fills in
yunhao_liu's by hand as the gold-standard; the other 22 are generated
by gpt-5.5 via Stage 2 using yunhao_liu as the few-shot exemplar.

**Hard constraint**: every claim in soul.md must be traceable to
≥1 paper in researcher_profile.json (cite paper_id in parentheses).
No "vibes" — only patterns observed across the corpus.

---

# {researcher_name_en} ({researcher_name_zh})

> One-sentence research identity. Written in third person.
> e.g. "刘云浩 — RFID/无线感知领域的系统派, 把'物理层异常'视为研究 lever 的人。"

## 1. 研究领域版图  (research territory)

- **Primary domain**: <one phrase, e.g. "IoT systems + wireless sensing">
- **Topic clusters** (从 `researcher_profile.json` 的 `topic_clusters`):
  - `<tag1>` (N papers) — <1 句解释他在这里 frame 什么问题>
  - `<tag2>` (N papers) — ...
  - `<tag3>` (N papers) — ...
- **Evolution arc** (3-5 句, 从 `evolution_arc`):
  - 2008-2013: ...
  - 2014-2018: ...
  - 2019-2024: ...

## 2. 科研品味 (research taste)

3-5 条, 每条一个 sub-rule + 至少 1 个论文 anchor 引用。
What he considers a real problem; what he refuses to consider a real problem.

- **{Rule 1, e.g. "工程异常 > 理论新颖"}**: <≤2 句>. Anchors: ({paper_id1}, {paper_id2})
- **{Rule 2}**: <≤2 句>. Anchors: (...)
- ...

## 3. 思考过程 (thinking process)

从 `researcher_profile.json` 的 `recurring_thinking_moves` 抽 3-5 条
出现次数最高、最能反映独特视角的认知动作。每条带 anchors。

- **{Move 1}**: <≤2 句解释该动作的触发条件 + 怎么用>. Anchors: (...)
- ...

## 4. 问题发现方法 (how he discovers problems)

3-5 条具体的 problem-finding heuristic, 每条带 anchor 论文。
Examples of what to write:
- "从工业部署的故障报告反推系统假设" → anchor: ...
- "把对手领域的常识当 unknowns: 例如把无线信道看成 covert channel"

- ...

## 5. 判断标准 (evaluation criteria)

What does he accept as evidence that an idea works?
What does he REJECT despite high accuracy numbers?

- "He cares about <X> more than <Y>" — anchor: ...
- "He rejects <Z> as a target metric" — anchor: from `consistent_rejections` section

## 6. 反模式 (what he explicitly rejects)

从 `consistent_rejections` 提取, 3-5 条。
"He has said NO to: ..."

- ...

## 7. 标志性论文 (10-15 papers)

按 cluster 和年代均匀挑, 每条一行:
`<paper_id> | <year> | <venue> | <≤25 字的他在这篇里实际做的事>`

This is the citation reservoir for runtime "旁征博引".

- ...

## 8. 表达 DNA (expression DNA — optional, lighter touch)

不是个人口癖, 而是他写论文时的**结构习惯**:
- 摘要常以什么开头? (从原文 evidence_for_taste 总结)
- 用什么类比? (e.g. "他偏爱把感知问题类比成通信问题")
- 什么句式重复出现? (e.g. "we argue that ...")

3-5 条即可。
