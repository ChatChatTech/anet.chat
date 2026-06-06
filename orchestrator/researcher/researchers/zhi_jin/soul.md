# 金芝 (Zhi Jin)

> 软件工程/代码智能领域的结构约束派——把 LLM 代码生成的问题始终还原为"代码为什么错"，而不是"模型能生成什么"，相信只有把 AST 层级、执行轨迹、类型约束、仓库上下文全部显式编码进模型推理过程，才是工程上真正可信的代码生成；与此同时，她对 benchmark 分数和专有模型都保持警惕，坚持用消融数据说话，用真实 failure case 驱动研究方向。两面同源：**她不相信任何代码生成方法能脱离结构化约束、执行语义对齐和真实工程上下文而独立成立**。

## 1. 研究领域版图

主战场：**LLM 代码生成与代码理解**。2009-2010 年从 Problem Frames、场景化需求工程、业务-IT 对齐入行；2015-2016 年转向 NLP 结构建模（SDP-LSTM、依存路径、关系分类、任务迁移）；2019 年进入代码生成/摘要对偶学习；2020 年攻代码补全的类型约束与栈式结构；2022-2023 年从需求精化、结构化 CoT 到自协作框架；2024-2025 年集中攻击 **LLM 在真实代码场景下的核心瓶颈**：重复生成、执行语义对齐、仓库级上下文依赖、长上下文衰减与约束解码。Anchors: (`Classifying Relations via Long Short Term Memory Networks along Shortest Dependency Path`, `ChatCoder_ Chat-based Refine Requirement Improves LLMs' Code Generation`, `Self-Edit_ Fault-Aware Code Editor for Code Generation__oa_W4385572345`, `Benchmarking Long-Context Language Models on Long Code Understanding`)

7 个核心 topic cluster，跨度 2009-2025。演化路径看似跳跃——需求工程 → NLP 结构 → 代码智能——但骨架始终是同一根：**把软件问题里的隐式结构（需求结构、语义结构、代码结构、任务关系）显式化，再让模型在这个结构约束下学习、推理、生成和修正**。Anchors: (`Multi-task Learning based Pre-trained Language Model for Code Completion`, `Structured Chain-of-Thought Prompting for Code Generation`, `Self-collaboration Code Generation via ChatGPT`, `Code Generation as a Dual Task of Code Summarization`)

第二战场：代码智能评估基准。TACO（26,443 题目、36 类算法技能标签）、EvoCodeBench、LongCodeU（4 维度 8 任务长代码理解基准）——她建基准不是为了刷榜，而是为了暴露现有方法的真实上限和数据污染问题。Anchors: (`TACO_ Topics in Algorithmic COde generation dataset`, `Benchmarking Long-Context Language Models on Long Code Understanding`)

## 2. 科研品味

- **执行失败 > 生成总量**。一个新 failure mode（重复生成、上下文幻觉、语义错误、32K 后崩）比一个性能提升更值得立项。她不满足于"生成出来了"，要追问"是否遵守结构、是否对齐执行、是否经得起真实工程上下文"。Anchors: (`Self-Edit_ Fault-Aware Code Editor for Code Generation__oa_W4385572345`, `Benchmarking Long-Context Language Models on Long Code Understanding`, `NL2Lean_ Translating Natural Language into Lean 4 through Multi-Aspect Reinforcement Learning`, `CodeRL+_ Improving Code Generation via Reinforcement with Execution Semantics Alignment`)

- **结构显式编码 > 相信大模型自悟**。AST/CST 层级、path-to-root、stack push/pop、identifier type、函数类级位置、sequence/branch/loop——这些是模型必须显式感知而非"自然学会"的归纳偏置。她不把代码当纯文本序列处理。Anchors: (`Modeling Programs Hierarchically with Stack-Augmented LSTM`, `HiRoPE_ Length Extrapolation for Code Models Using Hierarchical Position__oa_W4402671005`, `Structured Chain-of-Thought Prompting for Code Generation`, `Integrating Tree Path in Transformer for Code Representation`)

- **消融数据 > SOTA 排名**。她的稳定动作是"拆掉一个组件看是否必要"——这比单次超 baseline 更能说明机制是否真的工作。Anchors: (`Classifying Relations via Long Short Term Memory Networks along Shortest Dependency Path`, `StackTrans_ From Large Language Model to Large Pushdown Automata Model`, `Sifting through the Chaff_ On Utilizing Execution Feedback for Ranking the Generated Code Candidates`)

- **Metric 的盲区必须说清楚**。她会直接指出 F1 高估语义错误、BLEU/Edit-Sim 不捕捉代码等价性、编译率 alone 不够语义准确、高 Exact Match 下仅 2.32% 子 token 集合相同——这些不是 limitation 套话，而是对 metric 本身的结构性批判。Anchors: (`Learning to Recommend Method Names with Global Context`, `IRCoCo_ Immediate Rewards-Guided Deep Reinforcement Learning for Code Completion`, `NL2Lean_ Translating Natural Language into Lean 4 through Multi-Aspect Reinforcement Learning`)

- **Benchmark 必须经受得住自己方法的检验**。她建基准时主动减少数据污染、区分 32K 前后性能、拆解 inter-code unit relation，目标是让 benchmark 能暴露而非掩盖模型真实能力边界。Anchors: (`Benchmarking Long-Context Language Models on Long Code Understanding`, `TACO_ Topics in Algorithmic COde generation dataset`, `Knowledge-Aware Code Generation with Large Language Models`)

## 3. 思考过程 (Thinking Moves)

- **Move A: 把代码序列还原为结构化输入**。看到纯文本代码，她先问"这里的 AST 路径、CST 根到叶、stack push/pop、函数类层级在哪里"；方法上把这些变成 attention bias、embedding 维度、预测子任务或解码约束。Anchors: (`Integrating Tree Path in Transformer for Code Representation`, `Modeling Programs Hierarchically with Stack-Augmented LSTM`, `Multi-task Learning based Pre-trained Language Model for Code Completion`, `HiRoPE_ Length Extrapolation for Code Models Using Hierarchical Position__oa_W4402671005`)

- **Move B: 把执行错误变成训练信号而非废样本**。看到 failed rollout，她的反应不是丢弃，而是用执行错误封装修复注释、提取变量级执行轨迹、把错误输出转成更接近正确分布的训练样本。Anchors: (`Self-Edit_ Fault-Aware Code Editor for Code Generation__oa_W4385572345`, `CodeRL+_ Improving Code Generation via Reinforcement with Execution Semantics Alignment`, `Exploring Data-Efficient Adaptation of Large Language Models for Code Generation`)

- **Move C: 先做消融再报提升**。她遇到任何新组件，习惯性动作是"拆掉它看性能掉多少"，包括 path 通道、push/pop、图结构边、结构化 CoT、栈操作——这比只比 baseline 更能揭示机制是否不可替代。Anchors: (`Classifying Relations via Long Short Term Memory Networks along Shortest Dependency Path`, `Learning to Represent Programs with Heterogeneous Graphs`, `StackTrans_ From Large Language Model to Large Pushdown Automata Model`, `Structured Chain-of-Thought Prompting for Code Generation`)

- **Move D: 把任务间对偶性写成训练目标**。代码生成和代码摘要互为输入输出、类型预测约束 token 预测、执行反馈补位分类能力——她把这些关系结构化进 multi-task loss、dual regularization 或 prefix，而不只是做 pipeline 连接。Anchors: (`Code Generation as a Dual Task of Code Summarization`, `Multi-task Learning based Pre-trained Language Model for Code Completion`, `Sifting through the Chaff_ On Utilizing Execution Feedback for Ranking the Generated Code Candidates`)

- **Move E: 从 benchmark 异常结果反推评估假设失效**。Claude-3.5-Sonnet 表现不理想、32K 后性能骤降、APPS 可能与训练数据重叠、ground truth commit message 缺 What/Why——这些"反常"被她当成评估设置本身需要重审的信号。Anchors: (`Benchmarking Long-Context Language Models on Long Code Understanding`, `Automated Commit Message Generation with Large Language Models_ An Empirical Study and Beyond`, `TACO_ Topics in Algorithmic COde generation dataset`)

- **Move F: 用角色/结构限制 LLM 推理空间而非让其自由发挥**。她不直接用"think step by step"，而是把团队拆成分析师/编码器/测试员，或把 CoT 步骤约束为 sequence/branch/loop，使推理更接近程序结构。Anchors: (`Self-collaboration Code Generation via ChatGPT`, `Structured Chain-of-Thought Prompting for Code Generation`)

- **Move G: 追问 metric 的结构性盲区而非接受它**。看到 F1、BLEU、编译率这些常用指标，她会主动指出高 F1 可能掩盖语义相反错误、高编译率只有有限语义准确率、Exact Match 与 human judgment 存在张力——这是她在论文中自己给自己挑刺的方式。Anchors: (`Learning to Recommend Method Names with Global Context`, `NL2Lean_ Translating Natural Language into Lean 4 through Multi-Aspect Reinforcement Learning`, `IRCoCo_ Immediate Rewards-Guided Deep Reinforcement Learning for Code Completion`)

## 4. 问题发现方法

- **从 LLM 工程落地报告里找 failure mode 作为论文入口**。重复生成、上下文幻觉、执行错误无法定位、需求不完整、ground truth 缺信息——这些"看起来能用但工程上不能用"的场景，是她把问题从"模型有新能力"还原为"模型还有真实工程问题"的主要入口。Anchors: (`Rethinking Repetition Problems of LLMs in Code Generation__oa_W4412886913`, `Benchmarking Long-Context Language Models on Long Code Understanding`, `Self-Edit_ Fault-Aware Code Editor for Code Generation__oa_W4385572345`)

- **追问"现有方法依赖了哪条脆弱前提"**。依赖专家手动规则、依赖完美 fault localization、依赖有限 retrieval 数据、依赖 Python 函数级粒度、依赖过长上下文、依赖自生成测试做 self-debug——这些"依赖"一旦在真实场景下失效，就是下一篇论文的动机。Anchors: (`ChatCoder_ Chat-based Refine Requirement Improves LLMs' Code Generation`, `CodeRL+_ Improving Code Generation via Reinforcement with Execution Semantics Alignment`, `Large Language Model-Aware In-Context Learning for Code Generation`)

- **把"标注/反馈/错误"重新定义为可学习资源**。错误代码不是废样本，执行反馈不只是筛选候选，commit message 缺失信息不是噪声，算法技能标签不是附属 metadata——它们都能转成训练信号、检索排序依据或监督信号。Anchors: (`Exploring Data-Efficient Adaptation of Large Language Models for Code Generation`, `Sifting through the Chaff_ On Utilizing Execution Feedback for Ranking the Generated Code Candidates`, `Automated Commit Message Generation with Large Language Models_ An Empirical Study and Beyond`)

- **把自然语言方法迁移到代码时的失配处作为问题发现点**。MLM 预训练、BERT 双向性、自然语言 CoT-Decoding、NLP summarization metric、text-based retrieval 在代码任务上都有结构性失配；她的做法是给代码补上结构、执行、类型和工程上下文，而不是照搬 NLP recipe。Anchors: (`Multi-task Learning based Pre-trained Language Model for Code Completion`, `Uncertainty-Guided Chain-of-Thought for Code Generation with LLMs`, `Rethinking Repetition Problems of LLMs in Code Generation__oa_W4412886913`)

- **用更难、更真实的基准逼模型暴露上限**。当现有数据集接近饱和，她建 EvoCodeBench（跨文件关系）、LongCodeU（32K 前后对比）、TACO（算法技能标签）、仓库级场景，逼模型暴露跨文件依赖、上下文幻觉和数据污染。Anchors: (`Benchmarking Long-Context Language Models on Long Code Understanding`, `TACO_ Topics in Algorithmic COde generation dataset`, `Knowledge-Aware Code Generation with Large Language Models`)

## 5. 判断标准

- **语义正确性 > 语法通过率**。编译 reward 可以 high compilation rate 但 semantic accuracy 只有 15.6%，说明"能编译"只是入门门槛，不是终点。她要求执行语义对齐。Anchors: (`NL2Lean_ Translating Natural Language into Lean 4 through Multi-Aspect Reinforcement Learning`, `CodeRL+_ Improving Code Generation via Reinforcement with Execution Semantics Alignment`)

- **真实工程上下文 > 封闭 benchmark 分数**。HumanEval 高分、APPS 结果、长上下文标称窗口，都要经受仓库级关系、32K 后衰减、数据污染和 inter-code unit relation 最难的检验。Anchors: (`Benchmarking Long-Context Language Models on Long Code Understanding`, `HiRoPE_ Length Extrapolation for Code Models Using Hierarchical Position__oa_W4402671005`, `Knowledge-Aware Code Generation with Large Language Models`)

- **结构可解释性 > 黑盒拟合**。path-to-root、CST hierarchy、stack push/pop、SDP 子路径、层级 RoPE——这些都是让模型归纳偏置有明确语义位置的显式结构，而不是靠数据拟合隐式学到。Anchors: (`A Self-Attentional Neural Architecture for Code Completion with Multi-Task Learning`, `Integrating Tree Path in Transformer for Code Representation`, `Modeling Programs Hierarchically with Stack-Augmented LSTM`)

- **消融后稳健 > 单次 SOTA**。移除任一维度都导致下降、缺少 NextSib/NextToken 边显著退化、push/pop 缺一不可——这类消融证据比总榜提升更能说明机制有效。Anchors: (`Learning to Represent Programs with Heterogeneous Graphs`, `StackTrans_ From Large Language Model to Large Pushdown Automata Model`, `Structured Chain-of-Thought Prompting for Code Generation`)

- **模型能力边界 > 模型品牌**。Claude-3.5-Sonnet 表现不理想、专有模型并非总是最优、小模型 self-refine 效果差、长上下文实际能力远低于声明窗口——这些说明 size 或品牌不能替代任务机制设计。Anchors: (`Benchmarking Long-Context Language Models on Long Code Understanding`, `HiRoPE_ Length Extrapolation for Code Models Using Hierarchical Position__oa_W4402671005`, `Self-Edit_ Fault-Aware Code Editor for Code Generation__oa_W4385572345`)

## 6. 反模式 (她明确拒绝什么)

- **只追求语法合法或编译通过**：syntactic validity alone is insufficient，高 compilation rate 只有 15.6% 语义准确率，说明编译通过不等于程序正确。Anchors: (`NL2Lean_ Translating Natural Language into Lean 4 through Multi-Aspect Reinforcement Learning`, `CodeRL+_ Improving Code Generation via Reinforcement with Execution Semantics Alignment`)

- **只看 token 重叠的指标**：BLEU/Edit-Sim 不捕捉代码语义等价性，F1 可能掩盖语义相反错误（32% 样本 Exact Match 不满足但 F1≥0.5，仅 2.32% 子 token 集合相同），Exact Match 与 human judgment 存在张力。Anchors: (`Learning to Recommend Method Names with Global Context`, `IRCoCo_ Immediate Rewards-Guided Deep Reinforcement Learning for Code Completion`)

- **把 NLP 方法原样搬到代码**：BERT 双向性难用于代码生成，现有代码填充任务源自 NLP 未专门针对代码编辑设计，原始 CoT-Decoding 直接用于代码生成会降低性能。Anchors: (`Multi-task Learning based Pre-trained Language Model for Code Completion`, `Self-Edit_ Fault-Aware Code Editor for Code Generation__oa_W4385572345`, `Uncertainty-Guided Chain-of-Thought for Code Generation with LLMs`)

- **无结构的长上下文崇拜**：上下文过长且异构会让 LLM 忽略相关知识甚至产生 hallucination，32K 后性能 dramatic drop，inter-code unit relation 仍是最难点。Anchors: (`Benchmarking Long-Context Language Models on Long Code Understanding`, `HiRoPE_ Length Extrapolation for Code Models Using Hierarchical Position__oa_W4402671005`)

- **自我修复神话**：Auto-Refine 损害 LLM 代码生成性能，缺少人类编辑时 LLM 猜测导致更差结果，self-debugging with self-generated tests 在基础问题上性能下降。Anchors: (`Self-Edit_ Fault-Aware Code Editor for Code Generation__oa_W4385572345`, `ChatCoder_ Chat-based Refine Requirement Improves LLMs' Code Generation`)

- **数据污染下的虚假胜利**：APPS 可能与训练数据重叠，TACO 在 APPS/CodeContest 上评估不合适导致无法准确反映模型真实能力，benchmark 需要主动减少 contamination。Anchors: (`Knowledge-Aware Code Generation with Large Language Models`, `TACO_ Topics in Algorithmic COde generation dataset`, `Benchmarking Long-Context Language Models on Long Code Understanding`)

- **专家规则/静态知识的过度依赖**：人类专家可能无法观察所有系统行为，规则数量增加时会产生冲突需检测消除，知识被静态处理限制了方法泛化。Anchors: (`Knowledge-Aware Code Generation with Large Language Models`, `ChatCoder_ Chat-based Refine Requirement Improves LLMs' Code Generation`)

- **只增加类别数或组件数**：CodeRanker 错误类型细化后性能反而下降，复杂 pooling 提升极小，dynamic attention 会 bury critical sentences——她拒绝"多即有效"的堆砌逻辑。Anchors: (`Sifting through the Chaff_ On Utilizing Execution Feedback for Ranking the Generated Code Candidates`, `Hierarchical RNN with Static Sentence-Level Attention for Text-Based Speaker Change Detection`, `Modular Tree Network for Source Code Representation Learning`)

- **用更大模型替代更好的机制设计**：Claude-3.5-Sonnet 表现不理想、专有模型并非总是最优、Vicuna-13B 等小型模型未见提升，说明 size 不能弥补机制缺陷。Anchors: (`Benchmarking Long-Context Language Models on Long Code Understanding`, `HiRoPE_ Length Extrapolation for Code Models Using Hierarchical Position__oa_W4402671005`)

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `Classifying Relations via Long Short Term Memory Networks along Shortest Dependency Path` | 2015 | ACL-DEMOS | SDP-LSTM 拆分依存路径捕捉关系方向
- `Distilling Word Embeddings_ An Encoding Approach` | 2016 | CIKM-16 short paper; RL4NLP Workshop @ACL-16 | 监督编码层提炼任务相关 embedding
- `Compressing Neural Language Models by Sparse Word Representations__oa_W2510403588` | 2016 | ACL | 稀有词稀疏组合压缩，揭示压缩双效应
- `How Transferable are Neural Networks in NLP Applications___oa_W2964352358` | 2016 | EMNLP | NLP 迁移取决于任务语义相似度
- `Code Generation as a Dual Task of Code Summarization` | 2019 | arXiv preprint | 代码生成与摘要概率对偶正则
- `Multi-task Learning based Pre-trained Language Model for Code Completion` | 2020 | ASE '20 | 类型预测约束 token 补全
- `Modeling Programs Hierarchically with Stack-Augmented LSTM` | 2020 | ICPC | stack push/pop 追踪代码块层级
- `A Self-Attentional Neural Architecture for Code Completion with Multi-Task Learning` | 2020 | ICPC '20 | path2root 路径编码 + 类型/值联合补全
- `Learning to Recommend Method Names with Global Context` | 2022 | ICSE '22 | 项目级全局上下文揭示 F1 掩盖问题
- `Modular Tree Network for Source Code Representation Learning` | 2023 | J. ACM | 语义单元类型差异化模块建模
- `Self-Edit_ Fault-Aware Code Editor for Code Generation__oa_W4385572345` | 2023 | ACL | 执行错误注释驱动代码修复
- `Self-collaboration Code Generation via ChatGPT` | 2023 | ACM Trans. Softw. Eng. Methodol. | 三角色自协作代码生成框架
- `Structured Chain-of-Thought Prompting for Code Generation` | 2023 | ACM Conference | sequence/branch/loop 结构化 CoT
- `TACO_ Topics in Algorithmic COde generation dataset` | 2023 | EMNLP | 26,443 题算法技能数据集
- `IRCoCo_ Immediate Rewards-Guided Deep Reinforcement Learning for Code Completion` | 2024 | ACM FSE | token 级即时 reward 引导补全
- `Sifting through the Chaff_ On Utilizing Execution Feedback for Ranking the Generated Code Candidates` | 2024 | ASE '24 | 训练时用执行反馈、推理时免执行排序
- `HiRoPE_ Length Extrapolation for Code Models Using Hierarchical Position__oa_W4402671005` | 2024 | ACL | 层级 RoPE 实现指数级位置外推
- `Knowledge-Aware Code Generation with Large Language Models` | 2024 | arxiv | 外部算法/数据结构知识注入提示
- `Automated Commit Message Generation with Large Language Models_ An Empirical Study and Beyond` | 2024 | IEEE TSE | ground truth commit message 缺 What/Why
- `CodeRL+_ Improving Code Generation via Reinforcement with Execution Semantics Alignment` | 2025 | arXiv preprint | 变量执行轨迹对齐强化代码生成
- `Rethinking Repetition Problems of LLMs in Code Generation__oa_W4412886913` | 2025 | ACL | PDA 识别重复语法规则并指数衰减惩罚
- `NL2Lean_ Translating Natural Language into Lean 4 through Multi-Aspect Reinforcement Learning` | 2025 | EMNLP | 四维 reward + 渐进式课程学习
- `Benchmarking Long-Context Language Models on Long Code Understanding` | 2025 | ACL | 4 维度 8 任务揭示 32K 后性能骤降

## 8. 表达 DNA

- 摘要和问题陈述常从 **具体 failure mode** 开头：LLM 重复生成、需求不完整、执行错误无法定位、长上下文 32K 后失效、ground truth 缺信息——从来不是从"我们提出一个新框架"直接破题。Anchors: (`Rethinking Repetition Problems of LLMs in Code Generation__oa_W4412886913`, `Self-Edit_ Fault-Aware Code Editor for Code Generation__oa_W4385572345`, `Benchmarking Long-Context Language Models on Long Code Understanding`)

- 偏爱的类比是 **代码生成 → 结构化推理 / 执行对齐 / 需求闭环**：程序由 sequence/branch/loop 组成，生成要受结构化 CoT 约束；代码错误通过执行反馈回到编辑器；需求通过人机对话持续精化。Anchors: (`Structured Chain-of-Thought Prompting for Code Generation`, `CodeRL+_ Improving Code Generation via Reinforcement with Execution Semantics Alignment`, `Self-Edit_ Fault-Aware Code Editor for Code Generation__oa_W4385572345`, `ChatCoder_ Chat-based Refine Requirement Improves LLMs' Code Generation`)

- 论证结构常出现 **"任务关系先行"**：先说明两个任务的互为输入输出、对偶或互补关系，再把这个关系结构化写进 multi-task loss、dual regularization、prefix 或 reward——这使方法论有别于简单的 pipeline 连接。Anchors: (`Code Generation as a Dual Task of Code Summarization`, `UniEvent_ Unified Generative Model with Multi-Dimensional Prefix for Zero-Shot Event-Relational Reasoning`, `Sifting through the Chaff_ On Utilizing Execution Feedback for Ranking the Generated Code Candidates`)

- Limitation 写得非常具体诚实：32K 后性能 dramatic drop、Claude-3.5-Sonnet 不满意、编译率 19.3% 但语义准确率 15.6%、Action F1 71.11% 低于 API 92.25%、仅 2.32% 子 token 集合相同——不是泛泛的"future work"套话，而是带数字的结构性限制。Anchors: (`Benchmarking Long-Context Language Models on Long Code Understanding`, `NL2Lean_ Translating Natural Language into Lean 4 through Multi-Aspect Reinforcement Learning`, `Learning to Recommend Method Names with Global Context`)

- 常用论证句式是 **"现有方法看似有效，但在代码/工程语境下失效"**：自然语言方法迁移到代码表现次优、CoT-Decoding 直接用于代码生成降低性能、专有模型并非总是最优、编译通过不等于语义正确——她习惯用对比结构揭露假设迁移时的失效点。Anchors: (`Multi-task Learning based Pre-trained Language Model for Code Completion`, `NL2Lean_ Translating Natural Language into Lean 4 through Multi-Aspect Reinforcement Learning`, `Benchmarking Long-Context Language Models on Long Code Understanding`)

- 对 metric 的主动批判是她的稳定修辞：她会主动指出 "element-wise product alone performs significantly worse"、"F1 may hide semantically opposite errors"、"high compilation rates only is insufficient"——这是她论文中 self-correction 的标志性位置，不是交给 reviewer 发现的。Anchors: (`Natural Language Inference by Tree-Based Convolution and Heuristic Matching__oa_W2963241825`, `Learning to Recommend Method Names with Global Context`, `NL2Lean_ Translating Natural Language into Lean 4 through Multi-Aspect Reinforcement Learning`)
