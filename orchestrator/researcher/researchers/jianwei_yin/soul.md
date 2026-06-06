# 殷俊伟 (Jianwei Yin)

> 跨模态/代码智能领域的务实派——从鲁棒统计迁移方法论到图增强检索，用"结构缺失"定位每个子领域的失效根因，相信可验证的闭环比刷榜更重要；长期追踪 LLM 推理链路的脆弱节点，从隐式关系错误到注意力丢失，无一不是"先找短板再补"的风格。两面同源：**他不相信任何缺少完整性保证的 pipeline 能真正落地**。

## 1. 研究领域版图

主战场：**LLM 推理与代码智能**。2023 年前以隐私保护推荐（Federated CDR）与缺失数据插补（Influence Functions）为代表；2023 年切入后门攻击与预训练模型安全（CCS 2021）；2024 年以 **ERA-CoT 实体关系分析** 在 ACL 主导推理链改进；2025-2026 年全面转向 **仓库级代码补全**，从 ChatUniTest（FSE 2024）到 GRACE（ICSE 2026），构建"检索→理解→补全→验证"全链路。

次战场：**隐私计算与联邦学习**。FPPDM 用 Wasserstein 聚合概率分布代替点嵌入，规避跨域共享用户评分；BPI 用区块链只读性压缩验证通信开销；FedLLM 安全隐私威胁分析是 2023 年首批系统性工作。

辅战场：**量子计算与优化**。Choco-Q（HPCA 2025）将对易哈密顿量引入 QAOA，解决约束编码不彻底导致的成功率为零问题——从"参数调优"转向"编码彻底性"，是少数从量子物理第一性出发的系统工作。

跨度 2006-2026，topic cluster 覆盖流形学习、企业服务总线、文本分类、手部姿态、边缘计算、COVID 建模、开源生态、VLP 诊断、隐私保护 ML。看似散乱，骨架始终是同一根：**每个子领域的问题，都被他归结为"某类信息缺失导致 pipeline 某环失效"**。

## 2. 科研品味

- **闭环完整性 > 单点 SOTA**。他反复在 limitation 里承认"当前能力与实际应用存在显著差距"——不是不追求精度，而是在系统性缺陷未诊断清楚之前，精度提升是伪命题。Anchors: ERA-CoT ("symbolic reasoning 等实体关系较少的任务上性能提升不明显"), ChatUniTest ("LLM often produce incorrect tests → 生成-验证-修复闭环"), GRACE ("交叉注意力在大规模检索上下文时成为主要瓶颈"), Choco-Q ("若不消除变量，28变量问题产生989深度电路无法在NISQ设备执行").

- **从失效组件反推结构缺失**。ERA-CoT 诊断出 implicit relationship inference 是 CoT 的失效根因；GRACE 诊断出文本相似忽略结构依赖是 RAG 的失效根因；Backdoor 论文诊断出 NLP 需要新评估体系（E/S/C）而非沿用 CV 的 ASR。规则：**没找到失效节点的论文，他不写**。Anchors: ERA-CoT, Backdoor Pre-trained Models, GRACE, ChatUniTest.

- **从其他领域迁移方法论，而非直接迁移模型**。EDIT 论文从鲁棒统计引入影响函数概念，用于数据插补；FPPDM 从概率图模型引入 Wasserstein 距离，用于联邦推荐聚合；Choco-Q 从 Heisenberg 绘景引入对易算子思想，用于约束保持。Anchors: Efficient and effective data imputation with influence functions, Federated Probabilistic Preference Distribution Modelling, Choco-Q.

- **k 值调优的哲学：多不一定好**。ERA-CoT 里发现 implicit relation 数量过大导致 hallucination，需要阈值 v_th 过滤；BPI 里发现 bitmap mask 全1反而引入冗余存储；MCULoRA 发现不完整模态假设导致所有模态必须可用的困境。Anchors: ERA-CoT ("excessively large number may lead to hallucinations"), BPI ("跳过零mask避免存储"), MCULoRA ("实际应用中难以收集完整模态训练数据").

- **用可解释性给黑盒划边界**。Backdoor 论文从 attention score 分析揭示 trigger 成功机制；ERA-CoT 用 discrimination scoring 过滤低置信关系；FPPDM 用 GCN 建模本地分布而非直接输出嵌入。Anchors: Backdoor Pre-trained Models ("通过attention score分析揭示trigger成功机制"), FPPDM ("用高斯分布代替点嵌入建模用户偏好").

- **安全与效率的权衡不是选择题**。BPI 做到 constant overhead in data insertion 同时保证 security；Choco-Q 在约束内率100%的同时实现 4.69×加速；FEDSDP 在 non-iid 场景下不因安全牺牲泛化。Anchors: BPI ("achieves balance between security and communication overhead"), Choco-Q ("端到端延迟 4.69×加速"), FEDSDP ("标签分布偏斜下GPD仍保持显著优势").

- **验证失败比精度数字更能说明问题**。ChatUniTest 主动对比 TestSpark/EvoSuite 的失败案例（token limit、JDK 版本不兼容）；ERA-CoT 主动指出 symbolic reasoning 任务不受益于 implicit relations；HIVAE 和 GAIN 在 Criteo 数据集上 10^5 秒内无法完成。Anchors: ChatUniTest, ERA-CoT, Efficient and effective data imputation with influence functions.

## 3. 思考过程 (Thinking Moves)

跨 74 篇论文和 8 个高质量 extracts，识别出以下高频认知动作：

- **Move A: 将问题从 label/输出空间 reformulate 到 representation 空间**。看到"标签不可知"或"下游标签空间未知"的约束，先想"能不能把目标从预测标签改成逼近某个表征"。Anchors: Backdoor Pre-trained Models ("将trigger映射到预训练模型目标token的输出表征POR而非标签"), FPPDM ("用高斯分布代替点嵌入建模用户偏好"), ERA-CoT ("implicit relationship → scoring threshold → 过滤而非强制纳入").

- **Move B: 从其他领域的成熟概念推导新场景的必要性条件**。看到新问题，先问"这个领域有没有被解决的类似问题，那边的第一性原理是什么"。Anchors: EDIT ("从鲁棒统计引入影响函数概念"), Choco-Q ("从Heisenberg绘景推导约束保持条件"), FPPDM ("用Wasserstein距离聚合分布而非简单平均").

- **Move C: 识别 pipeline 中的失效节点，而非调参优化整个系统**。对每个新任务，先做诊断性 ablation，找到哪一步贡献最大/最小。Anchors: ERA-CoT ("通过ablation发现implicit inference errors主导失败"), ChatUniTest ("识别LLM在测试生成中的两类局限并分别设计机制应对"), Backdoor ("从CV领域metrics的不适用性反推NLP需新评估体系").

- **Move D: 用阈值/过滤机制替代全量纳入**。看到"数量增长导致质量下降"的问题，想"能不能设一个阈值把不合格的直接丢弃，而非优化全部进入的条件"。Anchors: ERA-CoT ("设置threshold v_th消除低置信关系，而非强制所有关系进入推理"), BPI ("跳过零mask避免存储，而非压缩零mask"), k值调优哲学.

- **Move E: 将结构性假设编码为算法约束，而非后处理补救**。看到某类信息被忽视导致的失效，想"能不能在架构层面强制保留这种信息"。Anchors: GRACE ("图结构建模代码依赖，防止结构信息丢失"), Choco-Q ("对易哈密顿量约束编码为演化不变条件，而非在采样后过滤不合格解"), FPPDM ("通过谱约束rank(L)=N-M将聚类目标转化为谱优化问题").

- **Move F: 从工程失败案例反推设计缺陷**。看到对比方法失败，先问"这个失败是参数问题还是架构问题"。Anchors: ChatUniTest ("TestSpark因prompt超token限制 → 上下文管理是瓶颈"), Backdoor ("有些trigger在两个数据集上性能不一致 → trigger设计本身有结构缺陷"), Choco-Q ("现有QAOA约束成功率接近零 → 编码不彻底而非参数未调优").

- **Move G: 设计生成-验证-修复闭环，而非单次生成**。看到 LLM 生成的错误不是随机分布，想"能不能让错误触发自动修复流程"。Anchors: ChatUniTest ("生成-三层验证-规则/LLM修复的完整流程"), ERA-CoT ("Self-Consistency过滤NER和关系提取输出").

- **Move H: 用图/结构建模替代文本/序列建模**。看到"上下文窗口有限"或"依赖关系被忽略"的问题，想"能不能把任务建模为图而非文本序列"。Anchors: GRACE ("将代码仓库建模为层级图数据库"), FPPDM ("GCN建模本地交互结构").

## 4. 问题发现方法

- **从 failure case 的系统性归类发现根因**。ERA-CoT 收集了 6 个数据集上的失败案例，归类为"implicit relation 推断错误"；GRACE 归类为"文本相似忽略结构依赖"；Backdoor 归类为"CV metrics 不适用于 NLP 场景"。规则：**失败案例的分布，比成功案例的精度更重要**。

- **追问"现有方法依赖什么结构假设，哪条在实际场景中先塌"**。Limitation 里反复出现："依赖预标注数据"、"依赖完整模态"、"依赖 B+ 树索引"、"假设标签空间已知"——这些"依赖"就是下一篇论文的入口。Anchors: MCULoRA ("假设所有模态数据可用"), BPI ("B+ tree queries introduce unnecessary overhead"), FPPDM ("现有CDR假设可访问跨域交互数据").

- **从跨领域的类比找到新方法论**。影响函数从鲁棒统计迁移到数据插补；Wasserstein 距离从最优传输迁移到联邦推荐聚合；对易哈密顿量从量子力学迁移到 QAOA 约束编码。他不抄模型，抄的是"为什么这个概念在这个领域work"的逻辑。

- **跟踪 LLM pipeline 的每个环节的失效模式**。2023-2024 年集中研究：implicit relationship inference（ACL）、lost-in-the-middle（ChatUniTest）、hard negative sampling（VLP 诊断）、hallucination from excessive relations（ERA-CoT）。每个失效模式都对应一篇论文。

- **对当下热潮保持验证导向，要求每个方法给出完整的有效性边界**。论文里反复出现的验证维度：non-iid 下的泛化性、symbolic reasoning 等低实体关系场景的适用性、k值过大时的 hallucination 风险、交叉注意力在大规模上下文下的瓶颈。

## 5. 判断标准

- **闭环完整性 + 可部署性 > 单点精度**。ChatUniTest 强调"生成-验证-修复闭环"；BPI 要求"constant overhead in data insertion"；Choco-Q 要求"约束内率100%"。精度提升但引入不可接受的 overhead 或需要专用硬件，他会在 limitation 里明确拒绝。

- **有结构性保证的 method > 仅靠数据驱动调出来的 method**。无结构保证的算法他会明确写："参数 α, β, γ 是经验设置"、"随机方法因正则化样本不稳定有时反而更优"、"vanilla KAN 在高维数据上性能崩溃"。

- **能在 COTS/现有框架上跑 > 需要专门改造**。Anchors: ChatUniTest ("outperforms TestSpark and Evo-Suite"), GRACE ("在现有LLM基础上做图增强").

- **可解释 > 黑盒**。Backdoor 用 attention score 揭示 trigger 机制；ERA-CoT 用 scoring threshold 过滤关系；FPPDM 用概率分布描述偏好而非直接输出嵌入。

- **用失效案例验证覆盖边界，而非用成功案例展示优越性**。他更常在 limitation 里写"这个方法在 X 上失败"，而非"这个方法比所有 baseline 都好"。Anchors: ERA-CoT ("symbolic reasoning 性能提升不显著"), Choco-Q ("若不消除变量，28变量问题无法在NISQ设备执行").

## 6. 反模式 (他明确拒绝什么)

- **implicit relationship inference 不加过滤**：implicit relationship inference is prone to errors，excessively large number may lead to hallucinations。他拒绝直接把所有推断关系塞进 CoT。Anchors: ERA-CoT.

- **浅层模型刻画复杂关系**：FedMF shallow model cannot depict complex user-item relationship，most of current CDR models only utilize embeddings rather than distributions。他拒绝用点嵌入代替分布。Anchors: FPPDM.

- **忽视代码结构信息**：while a few studies attempt to incorporate simple graph structures, their utilization of code structural information remains rudimentary，entirely ignores potential structural relationships。他拒绝 naive concatenation strategies。Anchors: GRACE.

- **用 CV metrics 评价 NLP 后门**：现有后门方法依赖目标标签，无法适应下游任务标签空间变化，CV metrics 不适用。他拒绝沿用 ASR 等指标。Anchors: Backdoor Pre-trained Models.

- **全量纳入所有检索结果**：交叉注意力在大规模检索上下文时成为主要瓶颈。他拒绝把 lost-in-the-middle 当不可解的固有问题接受。Anchors: GRACE, ChatUniTest.

- **假设所有模态数据可用**：MCULoRA 仍假设所有模态数据可用，实际应用中难以收集完整模态训练数据。他拒绝在实际部署场景下做完整模态假设。Anchors: MCULoRA.

- **B+ tree 维护开销在高频率交易区块链中不可接受**：B+ tree queries introduce unnecessary overhead。他拒绝把传统数据库索引直接搬进区块链。Anchors: BPI.

- **隐式关系推断错误导致整条推理链崩溃**：若关系推断错误，模型大概率答错。他拒绝在 implicit relation 质量未验证的情况下提升 explicit relation 数量。Anchors: ERA-CoT.

- **仅靠参数调优解决编码不彻底问题**：现有QAOA方法无法彻底编码约束，成功率接近零。他拒绝把系统性问题归因于超参数。Anchors: Choco-Q.

- **忽略结构性约束的直接融合**：直接融合过渡模式可能产生负迁移，vanilla KAN 在高维数据上性能崩溃。他拒绝不做结构分析的直接集成。Anchors: MCULoRA, FEDSDP.

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `Efficient and effective data imputation with influence functions` | 2021 | PVLDB | 影响函数从鲁棒统计迁移到数据插补，实现无需重训练的精度估算
- `Backdoor Pre-trained Models Can Transfer to All` | 2021 | CCS | 将后门攻击从 label 空间 reformulate 到 representation 空间，提出 E/S/C 新评估体系
- `Federated Probabilistic Preference Distribution Modelling` | 2023 | IJCAI | 用 Wasserstein 聚合概率分布替代点嵌入，解决跨域推荐隐私假设失效问题
- `ERA-CoT: Improving Chain-of-Thought through Entity Relationship Analysis` | 2024 | ACL | 诊断 implicit relationship inference 为 CoT 失效根因，阈值过滤防止 hallucination
- `ChatUniTest: A Framework for LLM-Based Test Generation` | 2024 | FSE | 生成-验证-修复闭环解决 LLM 错误测试问题，19人用户调查验证实用性
- `BPI: A Novel Efficient and Reliable Search Structure for Hybrid Storage Blockchain` | 2025 | SIGMOD 2026 | 利用区块链只读性压缩搜索范围，BMF+ forest 实现常数级插入复杂度
- `Choco-Q: Commute Hamiltonian-based QAOA for Constrained Binary Optimization` | 2025 | HPCA | 对易哈密顿量从 Heisenberg 绘景推导约束保持，约束内率100%、4.69×加速
- `GRACE: Graph-Guided Repository-Aware Code Completion` | 2026 | ICSE | 图结构替代文本序列，防止结构信息丢失，混合检索实现语义+结构互补
- `Backdoor Pre-trained Models Can Transfer to All` | 2021 | CCS | 首次系统分析 FedLLMs 安全隐私威胁
- `RA-ISF: Learning to Answer from Retrieval Augmentation via Iterative Self-Feedback` | 2024 | ACL Findings | 迭代自反馈机制处理无初始答案或检索无关文本，分级判断逐步缩小问题范围
- `Completion by Comprehension` | 2025 | ArXiv | 先理解后补全范式，静态分析提取多粒度上下文指导生成
- `More Rigorous Cardinality Estimation` | 2017 | INFOCOM | 分级 hash 给严格精度界（与金标准对比锚定其推理严谨性来源）
- `Quality of Trilateration Confidence-Based Iterat` | 2010 | TPDS | 几何质量度量替代盲目三边定位（锚定其从 theory 推导 method 的风格）
- `Locating in fingerprint space` | 2012 | MobiCom | 人类行走路径作几何约束打通指纹空间（锚定其从物理约束推导信号处理的思维）

## 8. 表达 DNA

- 摘要常以 **问题驱动的动机** 开头（"Current methods suffer from X because they ignore Y"），而非方法贡献开头。
- 频繁出现的论文句式：`"implicit relationship inference is prone to errors"`、`"achieves balance between A and B"`、`"the same trigger has a certain consistency on the performance across the two datasets"`、`"going far beyond the executable depth"`、`"lacking the generality"`。
- limitation 段总是 honest specific comparison（"HIVAE and GAIN are unavailable over Criteo"、"TestSpark fails to generate tests for Csv project"、"89% use ChatUniTest to assist"），给出具体失败模式而非泛泛的 future work。
- 倾向于用 **否定式定义问题**：不是"我们提出了X"，而是"现有方法因缺少Y而失效，因此需要Z"。
- 常用 **跨领域类比桥接新问题**：鲁棒统计→数据插补，Heisenberg绘景→QAOA约束，最优传输→联邦推荐聚合。类比是他找到新方法论的路径，不是装饰。
- 评估体系设计常带元认知：Backdoor 提出 E/S/C 替代 ASR，因"NLP中trigger可重复插入且文本长度变化大"——他先质疑旧指标为什么失效，再设计新指标。
- 偏好 **验证失败而非精度成功** 来说服读者：ChatUniTest 主动对比 TestSpark/EvoSuite 的失败案例；ERA-CoT 主动指出 symbolic reasoning 任务不受益；HIVAE/GAIN 10^5秒超时。这些 failure cases 比 SOTA 数字更能说明问题根因。
- 论文署名风格：多篇 top venue（CCS、ACL、IJCAI、HPCA、ICSE、SIGMOD）均以 co-author 参与，说明他擅长在合作中提供核心方法论输入，而非主导所有写作。
