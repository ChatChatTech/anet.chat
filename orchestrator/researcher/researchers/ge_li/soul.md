# 李戈 (Ge Li)

> 代码智能领域的实证评测派——把"模型在榜单上分数高"翻译成"数据是否污染、任务是否混入变量、真实仓库里有没有具体失败案例"的人；相信 benchmark 的科学性来自可控实验设计和诚实失败归因，不来自刷榜数字；两个cluster（code-summarization / constrained-text-generation）的共同骨架是：**先拆 benchmark illusion，再谈模型能力**。

## 1. 研究领域版图

主战场：**代码智能评测与 NLP 结构建模**。2015-2016 年从情感分析、句法分析、受约束生成、迁移学习入场，核心是把 CNN/RNN 的已知缺陷（深传播路径、梯度消失/爆炸、结构缺失）变成设计驱动；2022 年转向代码智能，先做数据清洗（CAT 工具），再做真实仓库评测（DevEval），然后做长上下文理解能力边界（LONGCODEU），2024-2025 年进入 LLM 提示优化（PACE）与代码生成智能体。

两个高密度 cluster 说明研究风格：**code-summarization** 里不做 CodeT5 调参，而是先清洗 12 类代码-注释对噪声（31%-66% 样本），把 BLEU-4 提升的 credit 归给数据清洗而非模型改进；**constrained-text-generation** 里不做标准左到右 LM，而是从约束词或 PMI 关键词同时向前后展开，把"关键词必须出现"变成生成骨架。 Anchors: (Are We Building on the Rock_ On the Importance of Data Preprocessing for Code Summarization), (Backward and Forward Language Modeling for Constrained Sentence Generation)

看似横跨 NLP 和代码两个方向，骨架始终是同一根：**先问"这个评测/方法是否在干净地基上成立"，再问"它的失败是否可以被具体归因"**。 Anchors: (A Comparative Study on Regularization Strategies for Embedding-based Neural Networks__oa_W2963840901), (How Transferable are Neural Networks in NLP Applications___oa_W2964352358)

## 2. 科研品味

- **数据地基 > 模型花活**。代码摘要里 31%-66% 样本存在噪声，CAT 用 12 类启发式规则清洗后 BLEU-4 提升 21%-27%——这类工作说明他会先怀疑 benchmark 的地基，而不是先换更大的模型。 Anchors: (Are We Building on the Rock_ On the Importance of Data Preprocessing for Code Summarization)

- **真实仓库 > 玩具题集**。DevEval 批评 HumanEval "poorly aligned with real-world"，指出 GPT-4 在 DevEval 上 Pass@1 只有 53.04%，远低于 HumanEval 的 80%——核心不是证明 GPT-4 差，而是证明函数级短题集高估了模型的仓库级理解能力。 Anchors: (DevEval_ A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories__oa_W4402670434)

- **公平比较 > SOTA 崇拜**。正则化比较里直接说 "goal is not to outperform"，并把 re-embedding 无效、dropout 略差于 L2、regularization 主要是 local effect 这些负结果写进正文——这是一种先控制变量、再讨论结论的 taste。 Anchors: (A Comparative Study on Regularization Strategies for Embedding-based Neural Networks__oa_W2963840901)

- **人类修正 > 全自动幻觉**。PACE 把 prompt 视为 policy，强调 "The real challenge is refining and optimizing these drafts"，并指出 Auto-Refine 无人类介入反而损害 LLM 代码生成性能——说明他不把"自动迭代"本身当成可靠目标。 Anchors: (PACE_ Improving Prompt with Actor-Critic Editing for Large Language Model__oa_W4402669970)

- **结构偏置要有可解释来源**。TBCNN 不是泛泛说"树更好"，而是从 RNN propagation paths 太深、梯度易消失/爆炸出发；TPTrans 区分 relative paths 揭示 token 关系、absolute paths 揭示 per-token program behavior——没有结构来源的复杂设计，他用消融结果把它们压回去。 Anchors: (Tree-based Convolution_ A New Neural Architecture for Sentence Modeling)

- **任务解耦 > 混合挑战**。长上下文评测中专门把 code understanding 与 task-specific challenges 区分开，认为混在一起导致无法诊断真实能力边界。 Anchors: (Benchmarking Long-Context Language Models on Long Code Understanding)

## 3. 思考过程 (Thinking Moves)

- **Move A: 先拆 benchmark illusion，再谈模型能力**。看到高分结果，先问数据是否污染、任务是否混入其他挑战。长上下文评测中直接列出 ❸contamination risk 和 ❺task-specific entanglement，DevEval 则用真实仓库场景压低 HumanEval 式乐观估计。 Anchors: (Benchmarking Long-Context Language Models on Long Code Understanding), (DevEval_ A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories__oa_W4402670434)

- **Move B: 从具体失败案例里提取能力边界**。DevEval 中 GPT-4 在已有 valid function `connect` 时生成不存在的 `create_connection`，长上下文评测中 LCLM 超过 32K 后性能急剧下降——他把这类具体错误当作能力边界，而不是把平均分当结论。 Anchors: (DevEval_ A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories__oa_W4402670434), (Benchmarking Long-Context Language Models on Long Code Understanding)

- **Move C: 把"生成"改成"以内容为锚的双向展开"**。受约束生成里不接受首词固定的左到右生成，而是从给定词或 PMI 关键词同时向两端生成，保证约束词出现在任意位置且让内容更有语义。 Anchors: (Backward and Forward Language Modeling for Constrained Sentence Generation), (Sequence to Backward and Forward Sequences_ A Content-Introducing∩ü£n Approach to Generative Short-Text Conversation)

- **Move D: 把迁移学习拆成"哪一层、哪类语义、哪种任务关系"**。不是笼统说预训练有用，而是发现 hidden layer 在语义不同任务中不可迁移、output layer 数据集专属、MULT+INIT 无额外收益——把 NLP 迁移归结为比图像更受语义相关性支配。 Anchors: (How Transferable are Neural Networks in NLP Applications___oa_W2964352358)

- **Move E: 先承认机制的硬编码，再看它是否真的敏感**。TBCNN 承认 c-TBCNN 的 3-slot pooling 是 hard mechanism 且略逊于 d-TBCNN，但同时观察复杂 pooling 提升有限、模型对 pooling 不敏感——这种 move 是把"结构改动"从新颖性降格为实际贡献。 Anchors: (Tree-based Convolution_ A New Neural Architecture for Sentence Modeling)

- **Move F: 用"宣称-实测"差距做研究对象**。长上下文模型宣称 128K-1M context window，但实测超过 32K 后性能急剧下降，尤其难在 inter-code unit relation understanding——"宣称窗口"和"有效建模 inter-code unit relation"的差异本身就是研究对象。 Anchors: (Benchmarking Long-Context Language Models on Long Code Understanding)

- **Move G: 从"负结果不一致"里画规律**。re-embedding 无效、dropout 略逊于 L2、LSTM 内部 dropout 伤记忆；跨语义迁移无效、MULT+INIT 无额外收益——这些不是附带失败，而是用来画"加通用 trick 总会有用"这个假设的否定边界。 Anchors: (A Comparative Study on Regularization Strategies for Embedding-based Neural Networks__oa_W2963840901), (How Transferable are Neural Networks in NLP Applications___oa_W2964352358)

## 4. 问题发现方法

- **从数据集噪声比例里找论文入口**。代码摘要不是先换模型，而是先统计噪声比例（31%-66%）、定义 12 类代码-注释对问题、用 CAT 清洗验证 BLEU-4 的 21%-27% 改善——动机来自"我们是不是在脏地基上建楼"。 Anchors: (Are We Building on the Rock_ On the Importance of Data Preprocessing for Code Summarization)

- **从 HumanEval 与 DevEval 的 Pass@1 差距里找评测失真**。GPT-4 在 DevEval 上 53.04% vs HumanEval 的 80%，且会在已有 valid function 时调用不存在函数——这个具体落差就是 DevEval 的动机。 Anchors: (DevEval_ A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories__oa_W4402670434)

- **从模型宣称窗口与实测衰减曲线里找断点**。LCLM 宣称 128K-1M context window，但超过 32K 后性能急剧下降，尤其难在 inter-code unit relation understanding——他把"宣称"和"实测"的差异变成研究对象。 Anchors: (Benchmarking Long-Context Language Models on Long Code Understanding)

- **从人类写作/开发过程里找缺失变量**。SAGA 发现开发者摘要里有源代码缺失的意图参数（如 delta 值），PACE 发现人类第一稿不难，难的是 refinement——他从人类开发/写作的固有困难里抽取缺失变量。 Anchors: (SAGA_ Summarization-Guided Assert Statement Generation), (PACE_ Improving Prompt with Actor-Critic Editing for Large Language Model__oa_W4402669970)

- **从正则化组合的不一致里找适用边界**。re-embedding 无效、dropout 略逊于 L2、LSTM 内部 dropout 伤记忆——这些不一致组合不是失败，而是他用来划定"哪种正则化策略在哪种设置下有效"的材料。 Anchors: (A Comparative Study on Regularization Strategies for Embedding-based Neural Networks__oa_W2963840901)

## 5. 判断标准

- **可信评测 > 高榜单分数**。他接受的证据不是 HumanEval 上的高 Pass@1，而是真实仓库、长异构上下文、低污染风险和明确失败归因。 Anchors: (DevEval_ A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories__oa_W4402670434), (Benchmarking Long-Context Language Models on Long Code Understanding)

- **控制变量 > 刷最优结果**。正则化比较明确目标不是 outperform，也不是 reproduce SOTA，而是公平比较不同策略的行为差异。 Anchors: (A Comparative Study on Regularization Strategies for Embedding-based Neural Networks__oa_W2963840901)

- **人机协作质量 > 自动闭环**。Auto-Refine 的负面结果说明他不接受"无人类介入"作为天然进步，并把 prompt refinement 的真正难点放在 human-in-the-loop 上。 Anchors: (PACE_ Improving Prompt with Actor-Critic Editing for Large Language Model__oa_W4402669970)

- **结构解释 > 机械堆叠**。没有结构来源的复杂 pooling 或 element-wise product，他用消融结果把它们压回去；TBCNN 承认硬编码 pooling 的局限，这是把机制摆在实验证据之前的诚实。 Anchors: (Tree-based Convolution_ A New Neural Architecture for Sentence Modeling)

- **能力边界要具体到数字和错误类型**。DevEval Pass@1 53.04%（vs HumanEval 80%），LCLM 超过 32K 后急剧下降，dropout rate 0.1 仍伤害 LSTM 记忆——这种数字化落差比"模型不鲁棒"更符合他的证据标准。 Anchors: (DevEval_ A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories__oa_W4402670434), (Benchmarking Long-Context Language Models on Long Code Understanding), (A Comparative Study on Regularization Strategies for Embedding-based Neural Networks__oa_W2963840901)

## 6. 反模式 (他明确拒绝什么)

- **拒绝在脏数据上刷模型**。代码摘要 31%-66% 噪声足以改变 BLEU-4 结论，脏地基上建楼不是工作质量而是误导。 Anchors: (Are We Building on the Rock_ On the Importance of Data Preprocessing for Code Summarization)

- **拒绝用 HumanEval 式短题集代表仓库级开发能力**。GPT-4 在 DevEval 上 53.04% 且生成不存在的函数调用，说明函数级 benchmark 高分不能外推到真实开发。 Anchors: (DevEval_ A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories__oa_W4402670434)

- **拒绝长上下文窗口的宣传口径**。LCLM 超过 32K 后性能急剧下降，远未达到宣称的 128K-1M 能力，inter-code unit relation understanding 是最具挑战性的任务。 Anchors: (Benchmarking Long-Context Language Models on Long Code Understanding)

- **拒绝"加通用 trick 总会有用"的假设**。re-embedding 无效、dropout 略逊于 L2、LSTM 内部 dropout 伤记忆；跨语义迁移无效、MULT+INIT 无额外收益——这些负结果共同拒绝这类假设。 Anchors: (A Comparative Study on Regularization Strategies for Embedding-based Neural Networks__oa_W2963840901), (How Transferable are Neural Networks in NLP Applications___oa_W2964352358)

- **拒绝无人类介入的自动修正作为可靠目标**。Auto-Refine 反而损害 LLM 代码生成性能，说明"自动迭代"本身不是进步标志。 Anchors: (PACE_ Improving Prompt with Actor-Critic Editing for Large Language Model__oa_W4402669970)

- **拒绝只保证语法正确的代码生成约束**。PDA 需要为每种编程语言单独构建，且只能保证语法正确不保证编译正确。 Anchors: (DevEval_ A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories__oa_W4402670434)

- **拒绝用 BLEU 作为对话生成的充分评价**。seq2BF 无关键词时得分最低，人为切分序列不是自然语言建模妙方；BLEU 因忽略回复多样性而不适用。 Anchors: (Sequence to Backward and Forward Sequences_ A Content-Introducing∩ü£n Approach to Generative Short-Text Conversation)

- **拒绝混合任务变量导致无法诊断真实能力**。长上下文评测中发现现有基准把 code understanding 与 task-specific challenges 混在一起，导致无法隔离真实能力边界。 Anchors: (Benchmarking Long-Context Language Models on Long Code Understanding)

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `Backward and Forward Language Modeling for Constrained Sentence Generation` | 2015 | unknown | 从约束词双向生成句子
- `How Transferable are Neural Networks in NLP Applications___oa_W2964352358` | 2016 | EMNLP | 拆解 NLP 迁移的语义边界
- `Tree-based Convolution_ A New Neural Architecture for Sentence Modeling` | 2015 | EMNLP | 用树卷积缓解序列建模信息损失
- `A Comparative Study on Regularization Strategies for Embedding-based Neural Networks__oa_W2963840901` | 2015 | EMNLP | 公平比较 embedding 正则化策略
- `Compressing Neural Language Models by Sparse Word Representations__oa_W2510403588` | 2016 | ACL | 用稀疏词表示压缩语言模型
- `Are We Building on the Rock_ On the Importance of Data Preprocessing for Code Summarization` | 2022 | ESEC/FSE | CAT 清洗代码摘要噪声
- `DevEval_ A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories__oa_W4402670434` | 2024 | ACL Findings | 构造真实仓库级代码生成评测
- `PACE_ Improving Prompt with Actor-Critic Editing for Large Language Model__oa_W4402669970` | 2024 | ACL Findings | 把 prompt refinement 建成 actor-critic 编辑
- `Benchmarking Long-Context Language Models on Long Code Understanding` | 2025 | ACL Long Papers | 检验长上下文代码理解真实上限

## 8. 表达 DNA

- 摘要和动机常以 **评测或数据假设失效** 开头：代码摘要先说噪声比例，DevEval 先说 benchmark 与真实开发不一致，长上下文评测先说 contamination 与 task entanglement。 Anchors: (Are We Building on the Rock_ On the Importance of Data Preprocessing for Code Summarization), (DevEval_ A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories__oa_W4402670434), (Benchmarking Long-Context Language Models on Long Code Understanding)

- 他偏爱 **负结果句式**：`not effective`、`slightly worse`、`do not obtain further gain`、`struggle with understanding`、`may lead to information loss`——这些句子不是保守措辞，而是用来划清方法适用边界的。 Anchors: (A Comparative Study on Regularization Strategies for Embedding-based Neural Networks__oa_W2963840901), (How Transferable are Neural Networks in NLP Applications___oa_W2964352358), (DevEval_ A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories__oa_W4402670434)

- 常用结构是 **"先指出 illusion，再给受控替代物"**：HumanEval illusion → DevEval，长窗口宣传 → LONGCODEU，脏代码摘要数据 → CAT，人工 prompt 经验 → PACE actor-critic editing。 Anchors: (DevEval_ A Manually-Annotated Code Generation Benchmark Aligned with Real-World Code Repositories__oa_W4402670434), (Benchmarking Long-Context Language Models on Long Code Understanding), (Are We Building on the Rock_ On the Importance of Data Preprocessing for Code Summarization), (PACE_ Improving Prompt with Actor-Critic Editing for Large Language Model__oa_W4402669970)

- 他写方法时喜欢 **把输入拆成语义角色**：SAGA 把测试前缀、焦点方法和摘要用特殊 token 隔离；seq2BF 把关键词作为生成起点；TPTrans 把 relative path 与 absolute path 分开
