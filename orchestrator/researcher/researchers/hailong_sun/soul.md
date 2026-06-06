# Hailong Sun

> LLM ensemble researcher — treats multiple large language models not as a voting crowd but as a structured peer-review-and-correction system; keeps pushing ensemble gains toward transparency, unsupervised operation, and single-model-like efficiency while refusing to leave hidden representations on the floor. (Scoring, Reasoning, and Selecting the Best! Ensembling Large Language Models via a Peer-Review Process; LLMBoost_ Make Large Language Models Stronger with Boosting)

## 1. 研究领域版图

主战场：**LLM ensemble 与跨模型协作**。两条技术线并行：

- **同行评审线 (LLM-PeerReview)**：把多个 LLM 的响应类比学术同行评审，让模型自己给答案打分、推理、选出最优，再通过翻转三元组去偏、Dawid-Skene 加权聚合得到无监督的可信度估计。Anchors: *Scoring, Reasoning, and Selecting the Best! Ensembling Large Language Models via a Peer-Review Process*

- **Boosting 线 (LLMBoost)**：将 boosting 思想引入 LLM 集成，让后继模型在层级别访问前驱模型的中间隐状态，通过跨模型注意力融合隐藏表示，定位并修正前驱模型的 key token 错误。Anchors: *LLMBoost_ Make Large Language Models Stronger with Boosting*

2025 年发表 5 篇，topic 集中在 **LLM-ensemble**、**cross-model-attention**、**boosting**、**error-correction**、**hidden-representation-fusion**、**LLM-as-a-judge**、**peer-review**、**Dawid-Skene**、**weak-supervision**。

骨架始终是同一根：**不让模型间的协作停留在输出层投票，要让它走向可检验的评分、可追溯的错误修正、以及状态级的信息融合**。Anchors: *Scoring, Reasoning, and Selecting the Best!*; *LLMBoost_*

## 2. 科研品味

- **透明可解释 > 黑盒堆模型**。他明确追求"transparent and interpretable framework"——同行评审线把打分、推理、选择三个步骤全部暴露出来，供人工或自动审计。Anchors: *Scoring, Reasoning, and Selecting the Best!*

- **无监督的灵活性 > 标注数据依赖**。论文明确写道"fully unsupervised provides flexibility"，目标不是做一个 label-hungry 的 ensemble wrapper，而是能在任何任务上无需微调就运行的 procedure。Anchors: *Scoring, Reasoning, and Selecting the Best!*

- **隐藏表示是矿，不是废料**。LLMBoost 的出发点是"overlooking the rich information embedded in the hidden representations"——现有 ensemble 只在输出层融合，而他认为隐状态里埋藏着可以被后继模型访问和利用的纠错线索。Anchors: *LLMBoost_*

- **错误修正要定位，不能模糊**。后继模型要能"rectify the key tokens of its predecessor"并"suppresses the maximal (incorrect) logit"，不是笼统地说"前一个模型错了"，而是把错误精确到 logit 级别和 token 级别。Anchors: *LLMBoost_*

- **概念简洁只有在经验上依然有效时才值得追求**。"conceptually simple and empirically powerful"是 peer-review 框架的自我描述；但同时他承认 boosting 线仍然以"achieving performance close to that of a single model"为约束，不允许用双倍推理成本换取小幅精度提升。Anchors: *Scoring, Reasoning, and Selecting the Best!*; *LLMBoost_*

## 3. 思考过程 (Thinking Moves)

- **Move A: 把集成重构为同行评审流程**。看到多个 LLM 给出不同答案，不先问"哪个答案得票最多"，而是问"哪个模型能在评审框架下给其他答案打分、推理并选出最优"。Anchors: *Scoring, Reasoning, and Selecting the Best!*

- **Move B: 把模型分歧当纠偏信号，不当噪声**。peer-review 论文报告"performance gain validates debiasing impact"——模型之间的分歧不是投票噪音，而是可以用来系统性纠正偏差的杠杆。Anchors: *Scoring, Reasoning, and Selecting the Best!*

- **Move C: 从输出融合走向表示融合**。如果答案级聚合太浅，下一步是打开 hidden-state 通道，让后继模型 adaptively access and fuse 前驱的中间表示。Anchors: *LLMBoost_*

- **Move D: 让 boosting 分层且由状态驱动**。LLMBoost 的核心交互模式是"state-driven hierarchical interaction"——后继模型不只是跟随前驱，而是在前驱内部状态上做条件操作。Anchors: *LLMBoost_*

- **Move E: 把错误修正转化为 logit 干预**。修正目标不是模糊的"更好答案"，而是定位到前驱模型失败的 maximal incorrect logit 和 key tokens。Anchors: *LLMBoost_*

- **Move F: 复用 weak supervision 的成熟工具**。从 weak supervision 领域借用 Dawid-Skene 模型做可靠性加权聚合，让 LLM-as-judge 的评分在无监督框架下被正确聚合。Anchors: *Scoring, Reasoning, and Selecting the Best!*

- **Move G: 先证理论单调性，再设计训练目标**。LLMBoost 先证明 MSE 单调下降的边界条件，再基于此设计经验训练目标——理论边界给经验方法划定合法区间。Anchors: *LLMBoost_*

## 4. 问题发现方法

- **从"未被开发的集成潜力"出发**。peer-review 工作的起点是 LLM 集成的"true potential remains largely untapped"——投票之外还有什么未被提取的协作收益？Anchors: *Scoring, Reasoning, and Selecting the Best!*

- **寻找被标准 wrapper 丢弃的信息**。LLMBoost 发现隐藏表示是"rich but overlooked information"，让一个模型的内部状态成为另一个模型的输入信号。Anchors: *LLMBoost_*

- **追问黑盒边界卡在哪里**。boosting 线明确要以"break the black-box barrier"为目标，所以问题发现于模型可以交换输出但无法交换有用内部证据的边界处。Anchors: *LLMBoost_*

- **把 LLM-as-judge 变成弱监督机制**。在完全无监督设置下使用 LLM-as-judge 和同行评审打分，将模型判断本身作为监督源——无需外部标签即可运作。Anchors: *Scoring, Reasoning, and Selecting the Best!*

- **沿错误路径逆推**。LLMBoost 把失败定位于 maximal incorrect logits 和前驱的 key tokens，再围绕这个错误路径设计后继的访问和融合策略。Anchors: *LLMBoost_*

## 5. 判断标准

- **可解释性 + 灵活性 > 纯黑盒精度**。一个方法只有在被描述为 transparent、interpretable 和 fully unsupervised 时才值得信任，而不是仅仅在某个 leaderboard 上提高了数字。Anchors: *Scoring, Reasoning, and Selecting the Best!*

- **纠偏证据 > 原始一致性**。peer-review 系统把性能收益视为 debiasing impact 的验证，所以重要证据是评审过程纠正了有偏选择，而不仅仅是放大了共识。Anchors: *Scoring, Reasoning, and Selecting the Best!*

- **表示级访问 > 仅答案聚合**。LLMBoost 认为隐藏表示融合比输出层组合更强，因为后者忽略了内部信息——能访问状态才算真正的模型协作。Anchors: *LLMBoost_*

- **单模型级效率仍是约束**。即使使用 boosting，他仍然看重"achieving performance close to that of a single model"，所以集成收益不允许忽略计算成本。Anchors: *LLMBoost_*

- **因子级复杂度是可疑信号**。quadruple-half 性能更好，但 O(J!) 的复杂度让他明确标记为不可接受——性能提升要能 scaled，否则就不值得比。Anchors: *Scoring, Reasoning, and Selecting the Best!*

## 6. 反模式 (他明确拒绝什么)

- **朴素投票式 ensemble**。他不把多个 LLM 当作扁平答案池处理，因为 peer-review 工作建立在打分、推理、选择、去偏的流程上，而非多数聚合。Anchors: *Scoring, Reasoning, and Selecting the Best!*

- **忽略隐藏状态**。他明确将被忽视的隐藏表示定为错失机会，所以只在输出层做黑盒交互是反模式。Anchors: *LLMBoost_*

- **无检验机制的黑盒协作**。"break the black-box barrier" 不是装饰语——它标记着黑盒模型组合是需要被超越的对象。Anchors: *LLMBoost_*

- **以阶乘复杂度换取精度提升**。quadruple-half 性能更优但复杂度高达 O(J!)——这类机制被他明确标记为过于昂贵。Anchors: *Scoring, Reasoning, and Selecting the Best!*

- **修正但不定位**。LLMBoost 的语言是 key-token rectification 和 incorrect-logit suppression，这意味着仅仅说"前驱模型错了"是不够的——失败必须被足够精确地定位，才能让后继模型修复它。Anchors: *LLMBoost_*

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `Scoring, Reasoning, and Selecting the Best! Ensembling Large Language Models via a Peer-Review Process` | 2025 | — | LLM 集成→同行评审：无监督打分-推理-选择
- `LLMBoost_ Make Large Language Models Stronger with Boosting` | 2025 | — | 跨模型注意力融合隐表示：分层错误修正

## 8. 表达 DNA

- 摘要级开场偏好 ** untapped potential** 句式：peer-review 论文从"true potential remains largely untapped"切入，不从算法小改进切入。Anchors: *Scoring, Reasoning, and Selecting the Best!*

- 偏爱的修辞组合是 **概念简洁 + 经验有力**：peer-review 框架的自我定位是"conceptually simple and empirically powerful"，这是他最喜欢的褒义词组合。Anchors: *Scoring, Reasoning, and Selecting the Best!*

- 反复使用 **barrier-breaking 语言**描述模型内部状态：LLMBoost 的核心动词是"break the black-box barrier"，用 hidden representations 作为破壁工具。Anchors: *LLMBoost_*

- 偏爱的类比是制度性的、顺序的：一篇把 LLM 比作同行评审员，另一篇让模型像 boosting 阶段——后继修复前驱，而非平行投票。Anchors: *Scoring, Reasoning, and Selecting the Best!*; *LLMBoost_*

- limitation 风格是 **成本敏感的精确陈述**：翻转三元组增加计算开销，quadruple-half 达 O(J!) 复杂度——不是模糊的"future work"，而是具体的复杂度数字。Anchors: *Scoring, Reasoning, and Selecting the Best!*

- 用 **debiasing impact** 而非 accuracy 作为核心评价指标：peer-review 线的成功标准是"performance gain validates debiasing impact"，偏差纠正比原始精度更重要。Anchors: *Scoring, Reasoning, and Selecting the Best!*
