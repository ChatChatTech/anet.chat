# C004 — nuwa-skill（女娲）调研文档

> 仓库：https://github.com/alchaincyf/nuwa-skill
> 本地路径：`/data/projs/anetchat/refs/nuwa-skill`
> License：MIT
> 最后提交：2026-05-23（非常新鲜，仍在活跃迭代）
> 调研日期：2026-05-25
> 用户场景：用 **数十名教授的 research papers** 作为蒸馏语料，构建学术 advisory board

---

## 1. 一句话定位

> 女娲不复制人，是**提炼"此人怎么思考"的认知操作系统**。

它是一个 **Claude Code / Codex / Cursor / Hermes / OpenClaw 等任意 Agent Skills 标准** 都能装载的 **元 Skill（生成 Skill 的 Skill）**：给它一个人名（+ 可选的本地语料），它通过一套 6-Phase + 三重验证的工作流，自动产出一个"该人物的思维 Skill"。

灵感来自 [colleague-skill](https://github.com/titanwings/colleague-skill)（蒸馏同事，5k+ star），女娲把目标倒转：**不蒸馏身边人，蒸馏历史上最强的大脑或专家**——他们已经留下数十年的公开著作、演讲、访谈这些"高纯度认知矿脉"。

---

## 2. 仓库布局

```
nuwa-skill/
├── SKILL.md                                 ★ 女娲本身的 Skill（645 行，6-Phase 工作流）
├── README.md / README_EN/ES/JA/KO.md        多语种 README
├── x-thread-en.md                           产品故事
│
├── references/
│   ├── extraction-framework.md  (152 行)    ★ 提炼方法论（核心算法）
│   └── skill-template.md         (116 行)    标准化输出模板
│
├── scripts/                                 ★ 4 个自动化脚本
│   ├── download_subtitles.sh    (bash 56)   yt-dlp 拉字幕
│   ├── srt_to_transcript.py     (py 108)    SRT/VTT → 干净 transcript
│   ├── merge_research.py        (py 151)    汇总 6 个 Agent 调研、出 Phase 1.5 检查表
│   └── quality_check.py         (py 153)    Phase 4 自动质量验证
│
├── examples/                                15 个完整案例
│   ├── munger-perspective/                  ✅ 含 25-biases.md + 中文深度调研
│   ├── steve-jobs-perspective/              ⭐ 含实战对话记录
│   ├── elon-musk-perspective/
│   ├── feynman-perspective/
│   ├── naval-perspective/
│   ├── taleb-perspective/                   ✅ 含深度调研
│   ├── paul-graham-perspective/
│   ├── zhang-yiming-perspective/
│   ├── andrej-karpathy-perspective/
│   ├── ilya-sutskever-perspective/
│   ├── mrbeast-perspective/
│   ├── trump-perspective/
│   ├── sun-yuchen-perspective/
│   ├── zhangxuefeng-perspective/
│   └── x-mastery-mentor/                    （主题型 Skill，非人物）
│
├── assets/
├── 6-agents-parallel.png                    架构图（6 Agent 并行采集）
├── advisory-board.png                       多人 Advisory Board 协作示意
├── cover-distill-minds.png
├── LICENSE                                  MIT 2026
└── wechat-qrcode.jpg
```

总计 ~2000 行代码 + ~3500 行文档 + ~50MB 数据（15 个 example 含完整 references/research）。

---

## 3. 核心方法论：三层蒸馏 + 三重验证

### 3.1 蒸馏的对象（SKILL.md L14-25）

> 女娲不是复制人，是**提炼思维框架**。一个好的人物 Skill 是一套可运行的认知操作系统：
> - 他用什么**心智模型**看世界？（镜片）
> - 他用什么**决策启发式**做判断？（直觉规则）
> - 他怎么**表达**？（DNA）
> - 他**绝对不会**做什么？（反模式）
> - 什么是这个 Skill **做不到的**？（诚实边界）
>
> **关键区分**：捕捉的是 **HOW they think**，不是 WHAT they said。

5 层递进：

| 层 | 内容 | 例子（芒格） |
|---|---|---|
| 1. 镜片（Mental Models） | 此人观察世界的框架 | 多元思维模型、逆向思考、护城河 |
| 2. 规则（Heuristics） | 快速判断的 if-then | 「看激励结构、看最大下行」 |
| 3. 表达 DNA | 语气/句式/词汇/节奏 | 极短句 + 否定句先行 + 干燥幽默 |
| 4. 反模式 | 此人明确拒绝的 | 拒绝"凯恩斯主义""精确预测" |
| 5. 诚实边界 | Skill 做不到什么 | 不能预测全新问题、不能替代真人创造 |

### 3.2 三重验证（references/extraction-framework.md L5-34）

**核心算法**——一个候选心智模型必须同时通过 3 个测试才入选：

```
验证 1: 跨域复现 (Cross-Domain Recurrence)
  同一个思维框架在 ≥2 个不同领域出现过？
  例：Naval 的"杠杆"在财富、成长、职业选择中都讲过

验证 2: 有生成力 (Generative Power)
  用这个模型能推断此人对新问题的可能立场？
  例：知道芒格"逆向思维" → 能推断他面对"如何成功"会先问"如何失败"

验证 3: 有排他性 (Exclusivity)
  这不是所有聪明人都会想的通用真理？
  例："反脆弱"是塔勒布独特的，"努力工作"则不算

3/3 通过 → 心智模型 ✅
1-2/3 → 降级为决策启发式（较弱）
0/3 → 丢弃
```

**意义**：把"语录收集"和"思想提炼"分开。LLM 默认会收集语录，女娲强制它过这三道关——大幅降低"鹦鹉学舌"的概率。

---

## 4. 6-Phase 完整工作流

### Phase 0 — 分流入口

**路径 A（用户指定人名）**：澄清范围 → 是否有本地素材 → 建目录 → 进 Phase 1
**路径 B（用户只说需求）**：从 9 维度表格（决策/表达/创业/教学/批判/内容/人生/风险/设计）追问 → 推荐 2-3 个候选 → 用户选

### Phase 1 — ⭐ 6 Agent 并行采集

这是女娲最特别的设计：**6 个 Sub-Agent 并行跑采集任务**，每个分工不同（SKILL.md L173-312）：

| Agent | 目标语料 | 提取重点 | 输出文件 |
|---|---|---|---|
| **1 著作** | 书、长文、论文、newsletter | 反复论点 (≥3 次)、自创术语、推荐书单 | `01-writings.md` |
| **2 对话** | 播客、长视频、AMA、深度采访 | 被追问时的回答方式、即兴类比、立场变化 | `02-conversations.md` |
| **3 表达** | Twitter/X、短帖 | 高频词、争议立场、幽默方式、辩论模式 | `03-expression-dna.md` |
| **4 他者** | 他人分析、批评、传记 | 外部观察、批评、同行对比 | `04-external-views.md` |
| **5 决策** | 重大决策、转折点、争议行为 | 决策背景、事后反思、言行一致性 | `05-decisions.md` |
| **6 时间线** | 出生到现在的完整历程 | 关键里程碑、思想转折、最近 12 个月动态 | `06-timeline.md` |

**铁律**（SKILL.md L161-170）：
- 6 个文件**必须写到 `skill目录/references/research/0X-xxx.md`**，绝对不能外置——Skill 必须自包含可复制分发
- 标注来源 + 可信度（一手 > 二手 > 推测）
- **矛盾保留不和稀泥**

**本地语料优先模式**（SKILL.md L178-204）：如果用户给了 PDF 书、演讲 transcript、视频字幕：
1. 6 Agent 先吃本地素材
2. 识别覆盖缺口
3. 只对缺失维度启动网络搜索
4. 来源标记「本地」vs「网搜」

来源权重（L286-296）：
```
用户提供一手素材 > 本人著作 > 长对话 > 实际决策
> 社交媒体 > 他人评价 > 二手转述
```

中文人物特化：B 站原视频 > 小宇宙播客；偏好 36 氪 / 极客公园 / 晚点 LatePost / 财新 / 虎嗅；**永远排除知乎、微信公众号、百度百科**。

### Phase 1.5 — 调研 Review 检查点

跑完 6 Agent 后，调 `scripts/merge_research.py` 生成检查表（每个 Agent 的来源数、关键发现、矛盾点、信息不足维度），**给用户人工 review**。不通过 → 回 Phase 1 补；通过才进 Phase 2。

**目的**：在花精力提炼之前先把"原料质量"卡住——"垃圾进垃圾出，这里拦截比 Phase 4 返工成本低得多。"

### Phase 2 — 框架提炼（Synthesis）

| 子步骤 | 内容 |
|---|---|
| 2.1 心智模型提取 | 扫描 01-05 列候选 → 三重验证筛选 → 排序取前 3-7 个（**宁少勿多**） |
| 2.2 决策启发式 | 5-10 条 if-then 规则，每条要有具体案例 |
| 2.3 表达 DNA 6 维度 | 句式 / 词汇 / 节奏 / 幽默 / 确定性 / 引用习惯（量化方法见 framework.md L37-71） |
| 2.4 内在张力 / 矛盾 | **保留矛盾不调和**（三类：时间性 / 领域性 / 本质性） |
| 2.5 价值观 / 反模式 / 智识谱系 | 受谁影响 → 影响了谁 |
| 2.6 诚实边界 | 至少 3 条明确局限 |

### Phase 2.5 — 提炼确认检查点

把 Phase 2 结果摘要给用户看一遍（模型列表 / DNA 关键特征 / 核心张力），用户确认 → Phase 3，否则回 Phase 2 调整。

### Phase 3 — Skill 构建

按 `references/skill-template.md` 标准模板填入 Phase 2 结果，产出最终的 `SKILL.md`。

**这一步最大的创新：自动生成 Agentic Protocol**（SKILL.md L439-496）

```markdown
## 回答工作流（Agentic Protocol）

### Step 1: 问题分类
- 涉及具体公司/人物/事件 → 走 Step 2
- 纯框架问题 → 走 Step 3
- 混合 → 先 2 后 3

### Step 2: [人物]式研究
**⚠️ 必须使用 WebSearch 获取真实信息，不可跳过。**
[根据 Phase 2 的心智模型推导出 3-5 个研究维度，
 每个维度 4-6 个具体研究点]

### Step 3: [人物]式回答
基于 Step 2 的事实，运用心智模型和表达 DNA 输出
```

这就把 Skill 从"风格扮演"升级成"思维顾问"——**强制做功课，禁止编造**。

研究维度怎么推导？从蒸馏出的心智模型反推此人最关心什么：

| 人物 | 核心心智模型 | 推导出的研究维度 |
|---|---|---|
| 芒格 | 多元思维 + 逆向 + 激励 | 看护城河 / 看激励结构 / 看最大下行 / 看历史类比 |
| 费曼 | 第一性原理 + 权威怀疑 | 看基本约束 / 看官方说法漏洞 / 看实验数据 |
| 塔勒布 | 反脆弱 + 尾部风险 + 知识僭妄 | 看极端情况 / 看谁承担尾部风险 / 看专家预测历史 |
| **教授** | 例：贝叶斯认知科学 | 看先验分布 / 看样本量 / 看 effect size / 看复现实验 |

### Phase 4 — 质量验证

3 项测试 + 6 项通过标准，全靠 `scripts/quality_check.py` 自动跑：

| 检查项 | 通过标准 | 失败信号 |
|---|---|---|
| 心智模型数量 | 3-7 个，每个有来源证据 | <3 或 >10 |
| 模型局限 | 明确写出失效条件 | 只写优点 |
| 表达 DNA 辨识度 | 读 100 字能认出是谁 | 像通用 ChatGPT |
| 诚实边界 | ≥3 条具体局限 | 只写「不能替代本人」 |
| 内在张力 | ≥2 对矛盾 | 观点高度一致（太假） |
| 一手来源占比 | >50% | 主要靠二手转述 |

外加：
- **已知测试**：3 个此人公开表态过的问题，比对方向
- **边缘测试**：1 个未公开过的相关问题，期望「基于 X 和 Y 推断…但不确定」（≠ 斩钉截铁）
- **风格测试**：100 字分析读起来像不像本人

**最多 Phase 2↔4 循环 2 次**，仍不通过则在诚实边界中标注薄弱维度，交付当前最优版本——不无限打磨。

### Phase 5 — 双 Agent 精炼

Phase 4 通过后，并行两个 Sub-Agent 做后置工序：
- **Agent A（auto-skill-optimizer 视角）**：8 维度结构评估（工作流清晰度、边界条件、检查点设计、指令具体性…），干跑 3 个典型 prompt
- **Agent B（skill-creator 视角）**：评激活触发条件、角色扮演规则可操作性

主 Agent 综合两份报告，应用不冲突的改进。改动目标：**让 Skill「激活即执行」，知道先做什么、碰到什么停下来**。

---

## 5. 4 个自动化脚本

| 脚本 | 用途 | 何时调 |
|---|---|---|
| `download_subtitles.sh` | yt-dlp 拉 YouTube 字幕，优先级：人工 zh > 人工 en > 自动 zh > 自动 en | Phase 1 用户给了 YouTube 链接 |
| `srt_to_transcript.py` | SRT/VTT → 去时间戳/重复行/HTML 的干净 transcript（合段、统计字数） | Phase 1 字幕清洗 |
| `merge_research.py` | 扫 `references/research/01-06.md`，统计来源数 / 一手二手比 / 矛盾点 / 关键发现，输出 Phase 1.5 检查表 | Phase 1.5 检查点 |
| `quality_check.py` | 对 SKILL.md 跑 6 项检查，输出 PASS/FAIL 表 + 总分 | Phase 4 验证 |

**最大价值**：把女娲流程的两个最易塌方的环节（调研质量评估、最终质量验证）**自动化**——人工失误率显著降低。

---

## 6. 多 Agent Advisory Board 模式

`advisory-board.png` + `6-agents-parallel.png` 暗示一个**并行咨询团**的使用模式：

```
用户："OpenAI 和 Anthropic 谁赢？"
   ↓
   并行调用：
     乔布斯 Skill：「这是品味竞赛，Apple 会赢」
     马斯克 Skill：「关键是芯片控制」
     Naval Skill：「长期看，创造稀有技能的人赢」
   ↓
   主 Agent 综合：呈现三人视角对比
```

SKILL.md 没有把 advisory board 流程写成显式协议，**但这是女娲生态的天然用法**：每个蒸馏出的 Skill 都是独立的 Claude/Codex skill，可以被并行 spawn（在 Hermes 中就是 `kanban_swarm` 直接派多个 worker，每个用一个人物 profile）。

→ **anet.chat 集成时，advisory board 不用自己实现，直接复用 [C003 Hermes](./C003-hermes-agent.md) 的 swarm 拓扑**。每个 worker 装载一个不同的教授 Skill，verifier 做交叉验证，synthesizer 出综合判断。

---

## 7. 已蒸馏的 15 个 examples 价值

每个 example 不仅有 SKILL.md，**还保留完整 `references/research/` 调研数据**——可以学到：

- **如何写一个高分 Agentic Protocol**：看 `munger-perspective/SKILL.md` 的「芒格式研究」工作流
- **如何处理矛盾人物**：看 `taleb-perspective/`（塔勒布反复打脸自己）
- **如何蒸馏中文人物**：看 `zhang-yiming-perspective/`、`sun-yuchen-perspective/`
- **如何处理活人（最近言论持续更新）**：看 `elon-musk-perspective/`
- **主题型 Skill 怎么和人物型不同**：看 `x-mastery-mentor/`

`steve-jobs-perspective/` 还含**实战多轮对话记录**——一手观察 Skill 在真实交互中的表现。

---

## 8. 跨 Agent 运行时兼容（核心卖点）

女娲遵循 [Agent Skills](https://agentskills.io) 标准 frontmatter：

```yaml
---
name: nuwa-skill
description: |
  ... (描述 + 触发词)
---
```

支持 55+ 运行时（README_EN.md）：
- Claude Code (`~/.claude/skills/`)
- Codex CLI (`~/.codex/skills/`)
- Cursor (`~/.cursor/skills/`)
- OpenClaw
- **Hermes Agent**（C003）
- CodeBuddy / Workbuddy / Gemini CLI / OpenCode / …

**降级方案**：连 Skill 系统都不用，直接把 SKILL.md 内容粘贴进任何 chat 系统当 system prompt 就行。

外部依赖：
- 必需：Python 3.6+ / bash
- 推荐：`yt-dlp`、`git`、WebSearch 工具
- 不需要：数据库 / GPU / 外部 API（WebSearch 可选）

---

## 9. ⭐ 学术论文场景的适配方案（核心需求）

> 用户场景：**有几十名教授的 research papers，要构建学术 advisory board**。

### 9.1 学术语料 vs 通用人物的差异

女娲 default 流程为公众人物设计，应用到学术场景需要做几处调整：

| 维度 | 通用人物 | 教授（学术） |
|---|---|---|
| 一手语料权重 | 著作 > 对话 > 社媒 | **论文 ≫ 学术演讲 > 访谈 > 个人页面** |
| 网络源排除 | 知乎 / 微信公众号 / 百度百科 | 反而要**主动加** Google Scholar / Semantic Scholar / dblp / arXiv / ResearchGate |
| 矛盾处理 | 时间性 / 领域性 / 本质性 | **方法论演化 / 跨学科应用 / 假设修正**（更结构化） |
| 表达 DNA | 句式 / 幽默 / 口癖 | **论证结构 / 引用密度 / 不确定性表述 / 数据 vs 理论倾向** |
| 反模式 | 价值观禁忌 | **驳斥过的具体假说 / 反对的方法论流派** |

### 9.2 推荐工作流（每位教授）

```
第 1 步：准备语料包
  per-professor 目录：
    sources/
      papers/          (3-5 篇代表作 PDF)
      talks/           (学术报告 transcript / SRT)
      interviews/      (深度访谈，如 Lex Fridman 类播客)
      cv.md            (学术简历)

第 2 步：触发女娲
  /skill nuwa-skill
  "蒸馏 [教授 X]，我有完整论文集，在 sources/ 下"
  → Phase 0 自动识别本地素材，进本地优先模式
  → Phase 1 6 Agent 优先吃 PDF/transcript，缺口补网搜
  → Phase 1.5 人工 review
  → Phase 2-4 自动跑完
  → Phase 5 双 Agent 精炼

第 3 步：检查产出
  python3 scripts/quality_check.py professor-X-skill/SKILL.md
  目标：6/6 通过，一手来源占比应 ≥ 70%（学术语料）

第 4 步：批量处理
  数十位教授 = 数十次重复
  可并行：每位教授占用一个 Hermes worker（C003）
```

### 9.3 学术化的 Agent 1 / 5 / 6 重定向

调研 Agent 在学术场景的「分工」要重写：

| Agent | 学术化重定向 |
|---|---|
| **Agent 1 著作** | 期刊论文为主——核心假设 / 方法 / 数据集 / 主要 finding；优先**高引论文** |
| **Agent 2 对话** | 学术报告 / 答辩 / workshop / Lex Fridman 类深度访谈 |
| **Agent 3 表达** | 论文写作风格：抽象 vs 具体、数据 vs 理论、不确定性表述、引用密度 |
| **Agent 4 他者** | 后续引用此人的论文、综述、批评、修正 |
| **Agent 5 决策** | **研究方向转折**——early-career → mid-career → recent 的范式转换 |
| **Agent 6 时间线** | 研究轨迹：第一篇论文 → 主要贡献 → 最新方向（追到当前 grant / preprint） |

### 9.4 学术心智模型的三重验证特化

- **跨域复现** → 同一方法论在多少个 subfield 出现过？（贝叶斯方法在视觉、语言、决策都用 = 通过）
- **生成力** → 知道这个方法论能推断此教授对未审稿论文的可能评价
- **排他性** → 不是所有同领域学者都这样做（如果是 field 共识，那是 field-level 而非 person-level 心智模型）

### 9.5 学术化的诚实边界（必须写）

```
- 调研截止 [日期]，之后发表的论文未纳入
- 此教授的方法论主要在 [子领域]，跨领域适用性有限
- Skill 不能预测此教授对全新方法的评价
- 个人 Twitter/blog 表达严谨度可能低于论文
- 假设 A 在 [论文链接] 中被明确驳斥，但近期发言可能软化立场
```

### 9.6 学术 Advisory Board 的 swarm 拓扑（与 C003 集成）

```
root: "评审 paper X 的核心假设"
  ├─ worker[prof-A-skill]: 用 prof A 的统计方法论视角看
  ├─ worker[prof-B-skill]: 用 prof B 的认知科学视角看
  ├─ worker[prof-C-skill]: 用 prof C 的哲学/方法论视角看
  ├─ worker[prof-D-skill]: 用 prof D 的实证主义视角看
verifier:   交叉检验 4 个视角的矛盾点
synthesizer: 综合输出 + 标注分歧
```

每个 worker 都是 **Hermes worker 进程** 装载 **女娲蒸馏出的教授 Skill** → **持久化在 SQLite Kanban**。

### 9.7 衡量学术 Skill 质量的额外指标

`quality_check.py` 默认 6 项之外，建议自加 4 项学术化指标：

| 指标 | 含义 |
|---|---|
| **跨论文复现率** | 一个论点是否在 ≥3 篇论文中出现 |
| **引用权重** | 高引论文（top 10% citation）的观点优于低引 |
| **方法论转移** | 此教授的方法被其他领域采用的案例数 |
| **弟子继承** | 此教授指导的学生后续研究的方向（间接验证 generative power） |

---

## 10. 关键引用（直接来自 SKILL.md）

> 女娲不是复制人，是**提炼思维框架**。一个好的人物 Skill 是一套可运行的认知操作系统。（L14-23）

> 关键区分：捕捉的是 **HOW they think**，不是 WHAT they said。（L25）

> 调研质量决定了最终 Skill 的上限。垃圾进垃圾出，在这里拦截比在 Phase 4 返工成本低得多。（L337）

> 宁可生成一个诚实标注了局限的 60 分 Skill，也不要生成一个看起来完美但实际上在编造的 90 分 Skill。（L312）

> 女娲造的不是人，是一面镜子。一个好的人物 Skill，让你用另一个人的眼睛看自己的问题。不是为了模仿他们，而是为了拓展你自己的思维边界。（L642-644）

---

## 11. 与 RAG / 微调对比

| 维度 | RAG | 微调 | **女娲 Skill** |
|---|---|---|---|
| 方法 | 检索 + 上下文注入 | 改模型参数 | 提示工程 + 结构化框架 |
| 单 Skill 成本 | 中（embedding + 向量库） | 高（GPU 训练） | **极低（纯文本 ~50KB）** |
| 透明度 | 半透明（可看检索结果） | 黑盒 | **完全透明（所有框架可读）** |
| 维护 | 重新 embed | 重新训练 | **编辑 markdown** |
| 风格捕捉 | 弱 | 强但贵 | **强（DNA 显式编码）** |
| 思维框架捕捉 | 几乎没有 | 隐式 | **显式建模** |
| 多 Skill 编排 | 难（多向量库） | 难（多 adapter） | **易（多 markdown）** |

→ 对**数十名教授**这种"中小规模、多人物、可解释"场景，**Skill 路线性价比远超 RAG/微调**。

---

## 12. 与 anet.chat / C001-C003 的协同

整合栈：

```
┌──────────────────────────────────────────────────────────────┐
│ anet.chat UI (chat / canvas)                                  │
│  - Excalidraw component (C001)                                │
└────────────┬─────────────────────────────────────────────────┘
             │
┌────────────▼──────────────────────────────────────────────┐
│ Hermes Agent (C003)                                       │
│  - SQLite Kanban + WAL                                    │
│  - Embedded Dispatcher (60s tick + CAS)                   │
│  - Swarm: root → workers → verifier → synthesizer         │
│  - Per-worker profile = 装载一个女娲 Skill                │
└──┬───────────────────────┬────────────────────────────────┘
   │                       │
   │ (装载)                │ (调工具)
   ▼                       ▼
┌──────────────┐    ┌─────────────────────────────┐
│ 女娲 Skills  │    │ MCP Tools                   │
│ (C004 产出)  │    │  - mcp_excalidraw (C002)    │
│              │    │  - shadcn / 其他            │
│ professor-A  │    │                             │
│ professor-B  │    └─────────────────────────────┘
│ professor-C  │
│ ...          │
└──────────────┘
```

落地节奏：

1. **Week 0**：跑通女娲——蒸馏 1 位教授端到端（含 Phase 1.5 / 4 / 5）
2. **Week 1-2**：批量蒸馏数十位教授（Hermes swarm 并行加速）
3. **Week 3**：构建 advisory board UI（chat 入口选 N 位教授 → 触发 Hermes swarm → 在 Excalidraw 上把分歧画成图）
4. **Week 4+**：循环优化（quality_check.py 跑分 → 用户反馈 → Phase 5 二次精炼）

---

## 13. 已知坑 / 注意事项

- **shi LLM 调研容易跑偏**：Phase 1 必须人工 Phase 1.5 review 把关，不能跳
- **学术 vs 通用排除源不同**：默认 SKILL.md 排除知乎/微信，但学术 ResearchGate 之类要主动加白
- **「最近 12 个月动态」对活跃教授难**：preprint / arXiv / Twitter 滚动很快，Skill 需要定期 Phase 2 部分更新
- **诚实边界写不好会让 Skill 显得"什么都不能"**：参考 munger-perspective 写法——边界要具体不要泛泛
- **多语言混合**：中文论文 + 英文论文混存时 Agent 3（表达 DNA）会失焦，建议为同一教授分中文/英文两套 DNA
- **私有论文不能上公网搜**：若教授有未发表 working paper，本地素材必须先放好；网络搜索 Agent 不能泄露

---

## 14. 许可

**MIT License**（2026 Huashu）。
- ✅ 商业使用 / 修改 / 分发 / 私用
- ⚠️ 用户自担生成 Skill 的质量责任，不保证就是该人物的真实观点

---

## 15. 关键文件索引（本地）

- [`SKILL.md`](../refs/nuwa-skill/SKILL.md) — 645 行女娲本体（6-Phase + 检查点）
- [`references/extraction-framework.md`](../refs/nuwa-skill/references/extraction-framework.md) — 152 行核心算法（三重验证 + DNA 量化 + 矛盾处理）
- [`references/skill-template.md`](../refs/nuwa-skill/references/skill-template.md) — 116 行输出模板
- [`scripts/download_subtitles.sh`](../refs/nuwa-skill/scripts/download_subtitles.sh)
- [`scripts/srt_to_transcript.py`](../refs/nuwa-skill/scripts/srt_to_transcript.py)
- [`scripts/merge_research.py`](../refs/nuwa-skill/scripts/merge_research.py)
- [`scripts/quality_check.py`](../refs/nuwa-skill/scripts/quality_check.py)
- [`examples/munger-perspective/`](../refs/nuwa-skill/examples/munger-perspective/) — Agentic Protocol 范本
- [`examples/steve-jobs-perspective/`](../refs/nuwa-skill/examples/steve-jobs-perspective/) — 实战对话范本
- [`examples/taleb-perspective/`](../refs/nuwa-skill/examples/taleb-perspective/) — 矛盾人物范本

参见：
- [C001 Excalidraw](./C001-excalidraw.md) — 画板组件
- [C002 mcp_excalidraw](./C002-mcp_excalidraw.md) — 画板的 MCP 通道
- [C003 Hermes Agent](./C003-hermes-agent.md) — 持久化多 Agent 编排（女娲 Skill 的运行时之一）

---

## 16. 一句话总结

> **女娲 = 把"几十年的人类智识"压缩成"一个可调用的 markdown"**。
>
> 对 anet.chat 来说，它是 C003 Hermes worker 的"人格供应商"——批量为多 Agent swarm 提供专业化人设。
> 对用户的学术 advisory board 场景来说，它是**把数十位教授变成可并行查询的智慧资源**的最低成本路径。
