# 冯晓程 (Xiaocheng Feng)

> 自然语言生成与大模型可信性的"连接派"——把摘要、翻译、跨语言、RAG、知识编辑都看成**信息是否被正确连接、压缩、拒答与迁移**的问题；他不满足于模型给出流畅文本，而反复追问：上下文有没有接上、知识有没有错配、跨语言连接有没有变成英语自循环、检索有没有把幻觉带进来。

## 1. 研究领域版图

主战场：**自然语言生成、摘要、跨语言迁移与大模型可信性**。2016 年以 Bi-LSTM+CNN 事件检测入场（`A Language-Independent Neural Network for Event Detection`），核心问题是"词与上下文如何建立有效关系"——单向 RNN 丢失 following clues 导致无法建立 court-release 关系。2017 年进入关系抽取（`Effective Deep Memory Networks for Distant Supervised Relation Extraction`），用 memory network 处理多跳推理但承认 hop 超过 6 会因 gradient vanishing 退化。2019-2021 年转向数据到文本生成与会议摘要（`Dialogue Discourse-Aware Graph Model and Data Augmentation for Meeting Summarization__oa_W3188385856`），把 discourse relation 建模为图结构，拒绝"uniformly accepting information from different discourse relations"。

2022 年后问题重心转到**可控生成、幻觉、RAG、跨语言 SFT、长上下文、知识编辑与多语言推理**。他把幻觉看成 knowledge misalignment，把选择性拒答（[REJ] token）看成 factuality signal；把跨语言微调看成 FFN/中间层 latent-level connection，而不是输入输出层的显式对齐；把长上下文看成 distributional perturbation minimization，批评单靠经验扩窗缺乏 profound understanding 与 interpretability。（`Alleviating Hallucinations from Knowledge Misalignment in Large Language Models via Selective Abstention Learning`; `CC-Tuning_ A Cross-Lingual Connection Mechanism for Improving Joint Multilingual Supervised Fine-Tuning__oa_W4412944828`; `Extending Context Window of Large Language Models from a Distributional Perspective__oa_W4404783110`）

10 年跨度 2015-2025，看似横跨事件检测、关系抽取、机器翻译、摘要、可控生成、幻觉、RAG、跨语言、长上下文、知识编辑——骨架始终是同一根：**不要只看模型输出，要看信息在模型内部、语言之间、检索链条和 discourse 结构里是否发生了正确连接**。

## 2. 科研品味

- **连接质量 > 表面流畅性**。事件检测里，单向 RNN/LSTM 丢掉后续线索会导致 cannot establish a relation between court and release；会议摘要里，不同 discourse relations 不能被均匀接收，因为 a question often sparks a discussion，Conditional/Result 等 relation 对摘要贡献更大。（`A Language-Independent Neural Network for Event Detection`; `Dialogue Discourse-Aware Graph Model and Data Augmentation for Meeting Summarization__oa_W3188385856`）

- **承认不知道 > 盲目高置信生成**。在知识错配场景里，他把 selective abstention 作为减少幻觉的核心机制，强调 acknowledging the insufficiency of knowledge 而不是 blindly assigning high probability；REJ 与 factuality 显著相关，说明拒答信号可被显式利用。（`Alleviating Hallucinations from Knowledge Misalignment in Large Language Models via Selective Abstention Learning`）

- **跨语言不是把英语搬过去，而是建立 latent-level interaction**。CC-Tuning 的动机正是现有方法 overlook deeper, latent-level cross-lingual interactions；当 +EN 设置把 cross-lingual connection 变成 EN2EN connection 时，性能下降反而证明原问题不是"多加英语"，而是"连接是否真的跨语言"。Feed-forward activations contribute the most，中间层捕获的泛化知识最具价值。（`CC-Tuning_ A Cross-Lingual Connection Mechanism for Improving Joint Multilingual Supervised Fine-Tuning__oa_W4412944828`）

- **结构关系必须被显式建模，均匀接收是错误抽象**。会议摘要里，忽略 rich interactive relations 会 hindering the exploration；多文档新闻摘要里，把 diverse perspectives 之间的 conflict 视为系统必须处理的显式对象，redundancies tend to persist or exacerbate。（`Dialogue Discourse-Aware Graph Model and Data Augmentation for Meeting Summarization__oa_W3188385856`; `GlobeSumm_ A Challenging Benchmark Towards Unifying Multi-lingual, Cross-lingual and Multi-document News Summarization__oa_W4404792986`）

- **强模型不是免检通行证**。他同时承认 neural-based methods are extremely strong performer，DMN provides superior performance to all other methods；也会指出 hop 过深带来的 gradient vanishing、protocol prompting depends on the model's capabilities、RAG system itself has limitations and may hallucinate。（`Effective Deep Memory Networks for Distant Supervised Relation Extraction`; `GlobeSumm_ A Challenging Benchmark Towards Unifying Multi-lingual, Cross-lingual and Multi-document News Summarization__oa_W4404792986`; `Alleviating Hallucinations from Knowledge Misalignment in Large Language Models via Selective Abstention Learning`）

## 3. 思考过程 (Thinking Moves)

- **Move A: 把文本任务重构为"连接是否成立"**。看到事件检测/摘要/跨语言迁移，先问目标词与上下文、话语单元与 discourse relation、不同语言 hidden states 之间有没有建立有效连接，而不是问"分类器够不够强"。（`A Language-Independent Neural Network for Event Detection`; `Dialogue Discourse-Aware Graph Model and Data Augmentation for Meeting Summarization__oa_W3188385856`; `CC-Tuning_ A Cross-Lingual Connection Mechanism for Improving Joint Multilingual Supervised Fine-Tuning__oa_W4412944828`）

- **Move B: 从生成错误反推知识状态不匹配**。看到幻觉，不先归因于 decoding 策略，而是问模型是否 overfitting to misaligned knowledge，是否应该把 [REJ] 信号转化为 factuality signal，让模型主动承认 insufficiency of knowledge。（`Alleviating Hallucinations from Knowledge Misalignment in Large Language Models via Selective Abstention Learning`）

- **Move C: 用结构约束修正端到端模型的盲区**。关系抽取里 memory hops 不能无限加深（超过 6 则 gradient vanishing）；会议摘要里 discourse graph 不能被当作平面序列；多文档摘要里 perspective conflict 不能被普通 prompting 消化，必须显式建模。（`Effective Deep Memory Networks for Distant Supervised Relation Extraction`; `Dialogue Discourse-Aware Graph Model and Data Augmentation for Meeting Summarization__oa_W3188385856`; `GlobeSumm_ A Challenging Benchmark Towards Unifying Multi-lingual, Cross-lingual and Multi-document News Summarization__oa_W4404792986`）

- **Move D: 把"扩展能力"写成扰动最小化问题**。长上下文不是简单 extrapolation，而是从 distributional perspective 分析现有方法为何 sub-optimal 与 lacks interpretability，并以 minimizing the perturbation 作为设计目标，用 KL 散度替代经验超参数。（`Extending Context Window of Large Language Models from a Distributional Perspective__oa_W4404783110`）

- **Move E: 先找任务里被忽略的中间层信号**。CC-Tuning 里他把 FFN activations、middle layers、easy-to-learn Transform Matrix 当作跨语言连接位置，而不是只在输入输出层做迁移；观察到 Feed-forward activations contribute the most 后，将此发现转化为架构设计决策。（`CC-Tuning_ A Cross-Lingual Connection Mechanism for Improving Joint Multilingual Supervised Fine-Tuning__oa_W4412944828`）

- **Move F: 用失败边界验证方法正确性**。CC-Tuning 发现 +EN 退化为 EN2EN 时性能下降，这反而 underscores CC-TUNING's alignment with its motivation；关系抽取里 hop 超过 6 退化被当作 gradient vanishing 的信号而非设计缺陷。（`CC-Tuning_ A Cross-Lingual Connection Mechanism for Improving Joint Multilingual Supervised Fine-Tuning__oa_W4412944828`; `Effective Deep Memory Networks for Distant Supervised Relation Extraction`）

## 4. 问题发现方法

- **从"模型看似会做但关键关系断掉"处找问题**。事件检测的入口不是分类器不够复杂，而是 model cannot establish a relation between court and release；这类失败直接暴露上下文连接机制不足，需要双向建模而非单向序列。（`A Language-Independent Neural Network for Event Detection`）

- **从"强模型仍然犯错"的边界处找问题**。关系抽取中 memory network 很强但 hop 超过 6 会退化；多文档新闻摘要中 protocol-guided prompting 有 preferential performance 但 depends on the model's capabilities，且 redundancies tend to persist or exacerbate；长上下文里 sub-optimal performance 持续存在因缺乏 distributional understanding。（`Effective Deep Memory Networks for Distant Supervised Relation Extraction`; `GlobeSumm_ A Challenging Benchmark Towards Unifying Multi-lingual, Cross-lingual and Multi-document News Summarization__oa_W4404792986`; `Extending Context Window of Large Language Models from a Distributional Perspective__oa_W4404783110`）

- **从"评价指标无法区分真实进步"处找问题**。AI-driven research support survey 指出 lack of standardized benchmarks and evaluation metrics hinders direct comparison；长上下文论文里 lack a profound understanding 与 lacks interpretability 被明确列为问题，说明 benchmark 可比性是系统可靠性的前提。（`From Hypothesis to Publication_ A Comprehensive Survey of AI-Driven Research Support Systems__oa_W4416034580`; `Extending Context Window of Large Language Models from a Distributional Perspective__oa_W4404783110`）

- **从"跨语言系统偷偷回到英语中心"处找问题**。CC-Tuning 发现 +EN 设置可能把 cross-lingual connection 变成 EN2EN connection，导致性能反而下降；LLM 对低资源语言存在偏见说明语言间数据不平衡是系统性问题。（`CC-Tuning_ A Cross-Lingual Connection Mechanism for Improving Joint Multilingual Supervised Fine-Tuning__oa_W4412944828`; `GlobeSumm_ A Challenging Benchmark Towards Unifying Multi-lingual, Cross-lingual and Multi-document News Summarization__oa_W4404792986`）

- **从"外部知识链条本身会污染生成"处找问题**。他不把 RAG 当作自动事实性保证，而是承认 RAG system itself has limitations and may hallucinate；输入编辑方法只能增补事实，无法纠正 LLM 中的错误；检索文档可能含无关噪声，生成式检索无法获取实时信息。（`Alleviating Hallucinations from Knowledge Misalignment in Large Language Models via Selective Abstention Learning`）

## 5. 判断标准

- **事实性与拒答校准 > 强行回答**。如果模型知识不足，他接受 selective abstention，因为 REJ 与 factuality 显著相关；他拒绝 blindly assigning high probability 的生成方式，认为 acknowledging insufficiency of knowledge 才是可信生成的前提。（`Alleviating Hallucinations from Knowledge Misalignment in Large Language Models via Selective Abstention Learning`）

- **结构解释 > 黑盒堆层数**。Hop 超过 6 会因 gradient vanishing 变差被当作真实约束而非调参空间；长上下文里 lack interpretability 被明确列为问题；因此"更深/更长/更宽"本身不是质量证据，需要揭示机制。（`Effective Deep Memory Networks for Distant Supervised Relation Extraction`; `Extending Context Window of Large Language Models from a Distributional Perspective__oa_W4404783110`）

- **跨语言连接是否真实发生 > 英语资源是否更多**。CC-Tuning 认为 deeper latent-level cross-lingual interactions 是关键；当 cross-lingual connection 退化成 EN2EN connection 时，设置本身就偏离目标，评测不仅看平均分更要看连接方向。（`CC-Tuning_ A Cross-Lingual Connection Mechanism for Improving Joint Multilingual Supervised Fine-Tuning__oa_W4412944828`）

- **人类标注与 ground truth 仍是上界参照**。会议摘要里 Ground truth obtains the highest scores，corpus scale is significant to performance；这使他不会把自动生成的高分误读为任务已解决——生成结果仍存在重复和自相矛盾，grammar limitation 依然存在。（`Dialogue Discourse-Aware Graph Model and Data Augmentation for Meeting Summarization__oa_W3188385856`）

- **Benchmark 可比性 > 单篇系统自证**。AI 研究支持系统 survey 把 lack of standardized benchmarks and evaluation metrics 视为阻碍 direct comparison 的根因；该领域仍 remain at an experimental stage，in actual scenarios effective application still requires substantial progress。（`From Hypothesis to Publication_ A Comprehensive Survey of AI-Driven Research Support Systems__oa_W4416034580`）

## 6. 反模式 (他明确拒绝什么)

- **只看前向序列**：RNN/LSTM 只看 preceding context 会丢掉 following clue，release 后的 "20 million euros" 等后续线索不能被利用，导致 court 与 release 无法建立关系。（`A Language-Independent Neural Network for Event Detection`）

- **把所有关系一视同仁**：uniformly accepting information from different discourse relations is not suitable，不同 relation 对摘要贡献不同，Conditional/Result 等更关键。（`Dialogue Discourse-Aware Graph Model and Data Augmentation for Meeting Summarization__oa_W3188385856`）

- **盲目高置信生成**：知识错配时继续 high probability 输出会 overfit to misaligned knowledge，他明确偏向 acknowledging insufficiency of knowledge 与 selective abstention；直接最小化熵会导致模型学习捷径，产生尖锐的输出分布。（`Alleviating Hallucinations from Knowledge Misalignment in Large Language Models via Selective Abstention Learning`）

- **把跨语言训练做成英语自循环**：+EN 设置下 cross-lingual connection 可能变成 EN2EN connection，被他视为偏离跨语言目标的失败模式；LLM 对低资源语言存在偏见说明简单堆砌英文资源不能解决结构性问题。（`CC-Tuning_ A Cross-Lingual Connection Mechanism for Improving Joint Multilingual Supervised Fine-Tuning__oa_W4412944828`; `GlobeSumm_ A Challenging Benchmark Towards Unifying Multi-lingual, Cross-lingual and Multi-document News Summarization__oa_W4404792986`）

- **把 prompting 当万能胶**：Protocol-guided prompting depends on the model's capabilities，且 redundancies tend to persist or exacerbate；因此提示词增强不是解决多文档、多语言冲突的充分条件。（`GlobeSumm_ A Challenging Benchmark Towards Unifying Multi-lingual, Cross-lingual and Multi-document News Summarization__oa_W4404792986`）

- **把长上下文外推当经验技巧**：已有方法 lack a profound understanding、sub-optimal performance、lacks interpretability；单靠经验扩窗被他明确拒绝，需要从分布视角给出扰动最小化解释。（`Extending Context Window of Large Language Models from a Distributional Perspective__oa_W4404783110`）

- **把 RAG 当自动事实性保证**：RAG system itself has limitations and may hallucinate；输入编辑方法只能增补事实无法纠正错误；检索文档含无关噪声，生成式检索无法获取实时信息。（`Alleviating Hallucinations from Knowledge Misalignment in Large Language Models via Selective Abstention Learning`）

- **无标准 benchmark 的系统性宣称**：lack of standardized benchmarks and evaluation metrics hinders direct comparison；该领域仍 remain at an experimental stage，in actual scenarios effective application still requires substantial progress。（`From Hypothesis to Publication_ A Comprehensive Survey of AI-Driven Research Support Systems__oa_W4416034580`）

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `A Language-Independent Neural Network for Event Detection` | 2016 | ACL | Bi-LSTM+CNN 捕捉双向上下文线索，解决跨语言事件触发词识别
- `Effective Deep Memory Networks for Distant Supervised Relation Extraction` | 2017 | IJCAI | 双层 attention memory networks 处理噪声远监督关系抽取
- `Dialogue Discourse-Aware Graph Model and Data Augmentation for Meeting Summarization__oa_W3188385856` | 2021 | IJCAI | Levi graph 建模会议话语结构，QA relation 构建伪摘要语料
- `Alleviating Hallucinations from Knowledge Misalignment in Large Language Models via Selective Abstention Learning` | 2025 | ACL | [REJ] token 吸收知识不确定性，abstention-aware 解码缓解幻觉
- `CC-Tuning_ A Cross-Lingual Connection Mechanism for Improving Joint Multilingual Supervised Fine-Tuning__oa_W4412944828` | 2025 | ACL | FFN 激活融合+中间层选择实现 latent-level 跨语言连接
- `Extending Context Window of Large Language Models from a Distributional Perspective__oa_W4404783110` | 2024 | EMNLP | 从旋转角分布扰动最小化视角统一长上下文扩展策略
- `GlobeSumm_ A Challenging Benchmark Towards Unifying Multi-lingual, Cross-lingual and Multi-document News Summarization__oa_W4404792986` | 2024 | EMNLP | 统一 MCMS 任务，协议引导提示显式处理多文档冲突
- `From Hypothesis to Publication_ A Comprehensive Survey of AI-Driven Research Support Systems__oa_W4416034580` | 2025 | EMNLP Findings | 三阶段框架整合 AI 科研支持系统，指出 benchmark 缺口

## 8. 表达 DNA

- 摘要与动机常从**现有模型漏掉的关系**开头：事件检测写 preceding/following clue 与"court-release"关系断掉，会议摘要写 question sparks a discussion 与 discourse relation 不均，跨语言写 overlook deeper latent-level interactions，长上下文写 lack a profound understanding 与 sub-optimal performance。

- 论文论证喜欢用**失败边界**收束：hop 超过 6 则 gradient vanishing 变差，+EN 退化为 EN2EN 则偏离跨语言目标，protocol prompting depends on model capability 则增强受限，Ground truth 仍得最高分则任务未解决。

- 常用的判断词不是"更大/更新"，而是 **alignment、connection、interaction、perturbation、factuality、interpretability**：这些词分别对应知识错配校准、跨语言激活连接、discourse 交互、长上下文分布扰动、拒答事实性和可解释性。

- Limitation 写得非常具体：hop count exceeds 6 时结果变差因 gradient vanishing，α=1 与 β=32 是 empirically suggest 的经验设置，Ground truth obtains the highest scores，ChatGLM3 无法理解复杂协议导致性能下降。

- 偏爱的类比是**信息流类比**：上下文线索要接上，discourse relation 要加权，跨语言 FFN/中间层要连通，知识不足时要拒答，长上下文扩展要最小化扰动。不是物理世界类比，而是通信/网络式的"连接-通道-信号"框架。
