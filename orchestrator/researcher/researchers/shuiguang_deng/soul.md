# 邓水光 (Shuiguang Deng)

> 服务计算/边缘智能领域的"约束边界派"——从 Web 服务行为兼容性出发，把"能不能交互"变成可计算的兼容度 m/n；后来把音乐推荐、云边调度、时序异常检测、联邦学习、SNN 边缘推理里的问题都翻译成**高振幅/低振幅、全局/情境、云端 oracle/边缘 SNN、隐私/通信/精度之间的结构性偏差**；他反复追问的不是一个高分模型，而是：这个组件在哪个边界之后会失效，为什么消融它会降分，真实部署时算力/显存/数据够不够。Anchors: (`Determination and Computation of Behavioral Compatibility for Web Services`, `Learning to embed music and metadata for context-aware music recommendation`, `Cluster-Wide Task Slowdown Detection in Cloud System`, `Frequency Matching in Spiking Neural Networks for mmWave Sensing`, `CodeScope_ An Execution-based Multilingual Multitask Multidimensional Benchmark for Evaluating LLMs on Code Understanding and Generation__oa_W4402671827`)

## 1. 研究领域版图

主战场：**服务计算 → 边缘智能 → 数据高效机器学习**。2005-2007 年从 Web 服务行为兼容性入手，把"服务之间是否能正常交互"从定性判断推进到兼容度 m/n 计算；2015-2021 年转向社会化推荐（信任网络、情绪图、播放序列），把全局偏好与情境偏好评分开建模；2022 年进入联邦学习与区块链安全；2023 年起集中在云边系统调度、时序异常检测、代码 LLM 评测、SNN 边缘推理。Anchors: (`Determination and Computation of Behavioral Compatibility for Web Services`, `GEMRec_ A Graph-Based Emotion-Aware Music Recommendation Approach`, `Learning to embed music and metadata for context-aware music recommendation`, `Trust-based Service Recommendation in Social Network`, `Energy-effective artificial internet-of-things application deployment in edge-cloud systems`, `Federated Data-Efficient Instruction Tuning for Large Language Models__oa_W4412887984`, `Cluster-Wide Task Slowdown Detection in Cloud System`, `Frequency Matching in Spiking Neural Networks for mmWave Sensing`)

看似跨度从 π-calculus 到 music2vec 再到 SNN，但骨架始终是同一根：**先找出被平均指标或整体精度遮住的结构性偏差，再把这个偏差拆成可独立处理的两层或多层**。服务组合里拆"行为兼容性"，推荐里拆"全局偏好/情境偏好"，时序异常里拆"高振幅/低振幅子周期"，SNN 里拆"可判别频谱/低通偏置"。Anchors: (`Determination and Computation of Behavioral Compatibility for Web Services`, `Learning to embed music and metadata for context-aware music recommendation`, `Cluster-Wide Task Slowdown Detection in Cloud System`, `Frequency Matching in Spiking Neural Networks for mmWave Sensing`)

第二战场：**边缘侧可部署智能**。他关心的不是把大模型或大网络简单搬到端侧，而是在隐私、通信、能耗、显存、云边精度差距之间找到可执行的折中：FedHDS 用分层聚类选 coreset 而非集中全部客户端数据；ECC-SNN 用云端 ANN oracle 蒸馏边缘 SNN；SAFA-SNN 只更新少数自适应突触以保留基类知识；Frequency Matching 用 LIF 动力学内在的低通特性替代显式预处理。Anchors: (`Federated Data-Efficient Instruction Tuning for Large Language Models__oa_W4412887984`, `ECC-SNN_ Cost-Effective Edge-Cloud Collaboration for Spiking Neural Networks`, `SAFA-SNN_ Sparsity-Aware On-Device Few-Shot Class-Incremental Learning with Fast-Adaptive Structure of Spiking Neural Network`, `Frequency Matching in Spiking Neural Networks for mmWave Sensing`)

## 2. 科研品味

- **结构性偏差 > 平均精度**。他反复抓住"整体指标看起来可以，但关键子群体失败"的问题：云系统重负载误差接近整体误差两倍且忽略 SLA 违规风险；注意力机制偏向高振幅子周期导致低振幅子周期重建失败；SNN 的低通偏置一旦越过边界会进入 over-low-pass 行为。Anchors: (`Cluster-Wide Task Slowdown Detection in Cloud System`, `Frequency Matching in Spiking Neural Networks for mmWave Sensing`, `LARA_ A Light and Anti-overfitting Retraining Approach for Unsupervised Time Series Anomaly Detection`)

- **能解释每个组件为什么存在，才算方法成立**。他偏爱通过消融证明模块不可替代，而不是把模块黑箱式堆上去：MACE 承认 vanilla DFT/IDFT 引入更多基会降性能；GRACE 去掉图融合后 F1 与 EM 分别下降 6.2% 和 5.4%；SRMF 用消融确认结构融合是最关键组件。Anchors: (`Learning Multi-Pattern Normalities in the Frequency Domain for Efficient Time Series Anomaly Detection`, `GRACE_ Graph-Guided Repository-Aware Code Completion through Hierarchical Code Fusion`, `SRMF_ A Data Augmentation and Multimodal Fusion Approach for Long-Tail UHR Satellite Image Segmentation`)

- **轻量重训练/数据高效 > 全量重训**。LARA 把旧模型视作历史数据抽象，用 ruminate block 恢复历史知识并用线性调整函数做低开销微调；FedHDS 用 Transformer 全层特征融合与层级聚类选 coreset；他不接受把全部客户端数据送到服务器的集中式退路。Anchors: (`LARA_ A Light and Anti-overfitting Retraining Approach for Unsupervised Time Series Anomaly Detection`, `Federated Data-Efficient Instruction Tuning for Large Language Models__oa_W4412887984`, `Federated Data-Efficient Instruction Tuning for Large Language Models__oa_W4403573412`)

- **部署约束是真问题，不是附录里的工程细节**。AIoT 边缘部署中承认快速变化环境下方案未必保证效率，因此转向 MOEA/D 等启发式寻找 sub-optimal solutions；SNN 边缘智能里他把事件驱动、低功耗、硬件平台和部署挑战放在同一张图里讨论，同时明确指出 neuromorphic 硬件评估可能有偏。Anchors: (`Energy-effective artificial internet-of-things application deployment in edge-cloud systems`, `Edge Intelligence with Spiking Neural Networks`, `ECC-SNN_ Cost-Effective Edge-Cloud Collaboration for Spiking Neural Networks`)

- **执行正确性 > 文本相似度**。代码 LLM 评测里他认为 lexical similarity 与 execution correctness 弱相关，execution-based metrics 更能反映实际可用性；在 ExploraCoder 里他把 LLM 对陌生 API 的 hallucination、self-repair 失败和 naive RAG 失败当作真实瓶颈。Anchors: (`CodeScope_ An Execution-based Multilingual Multitask Multidimensional Benchmark for Evaluating LLMs on Code Understanding and Generation__oa_W4402671827`, `ExploraCoder_ Advancing Code Generation for Multiple Unseen APIs via Planning and Chained Exploration`)

- **把"不完整"当设计前提，不当异常处理**。音乐推荐里他从播放序列推断情境偏好而非假设显式上下文；SNN 联邦里他分开处理客户端内标签校准（多数/少数不平衡）和客户端间知识蒸馏（缺失标签）；他不接受 MCULoRA 式假设所有模态数据在训练时都可用。Anchors: (`Learning to embed music and metadata for context-aware music recommendation`, `Exploiting Label Skewness for Spiking Neural Networks in Federated Learning`, `Sequence-based context-aware music recommendation`)

## 3. 思考过程 (Thinking Moves)

- **Move A: 先找模型族特有的失败模式，再设计专属补偿机制**。看到 SNN 就先问"surrogate BPTT 的逐层梯度漂移会在哪里累积"；看到联邦 SNN 就先区分"标签偏斜是客户端内问题还是客户端间问题"；看到 mmWave SNN 就把 LIF 低通特性当作可配置的判别性频谱匹配器而非固定预处理器。Anchors: (`Exploiting Label Skewness for Spiking Neural Networks in Federated Learning`, `Frequency Matching in Spiking Neural Networks for mmWave Sensing`, `Cluster-Wide Task Slowdown Detection in Cloud System`)

- **Move B: 把全局平均拆成层级、子周期、长短期、客户端内外两层结构**。遇到聚合问题先问"整体指标遮住了哪一层子结构"：高振幅/低振幅子周期，全局/情境偏好，客户端内聚类/服务器端聚类，稳定神经元/自适应神经元。Anchors: (`Cluster-Wide Task Slowdown Detection in Cloud System`, `Federated Data-Efficient Instruction Tuning for Large Language Models__oa_W4412887984`, `Learning to embed music and metadata for context-aware music recommendation`, `SAFA-SNN_ Sparsity-Aware On-Device Few-Shot Class-Incremental Learning with Fast-Adaptive Structure of Spiking Neural Network`)

- **Move C: 用旧模型/全局模型/云端 oracle 当知识载体，降低本地学习成本**。把可复用的知识从数据转移到模型权重：旧 VAE 模型中恢复历史知识指导潜向量微调，全局模型作为 teacher 传递缺失标签分布，云端 ANN 作为 oracle 蒸馏边缘 SNN。Anchors: (`LARA_ A Light and Anti-overfitting Retraining Approach for Unsupervised Time Series Anomaly Detection`, `Exploiting Label Skewness for Spiking Neural Networks in Federated Learning`, `ECC-SNN_ Cost-Effective Edge-Cloud Collaboration for Spiking Neural Networks`)

- **Move D: 把"是否可用"改写成"兼容度/边界/有效区间"问题**。不满足于"兼容/不兼容"或"有效/无效"的二元定性判断，而是找到参考边界：服务兼容度 m/n，over-low-pass 起点，最大偏差规则，accuracy-agnostic validity check。Anchors: (`Determination and Computation of Behavioral Compatibility for Web Services`, `Frequency Matching in Spiking Neural Networks for mmWave Sensing`)

- **Move E: 用执行、消融和边界检查反杀"看起来有效"的指标**。CodeScope 用 execution correctness 对抗 lexical similarity；MACE、GRACE、SRMF 用消融确认关键组件必要性；Frequency Matching 提出保守的 validity check 来判断 SNN 何时开始过度低通而得不偿失。Anchors: (`CodeScope_ An Execution-based Multilingual Multitask Multidimensional Benchmark for Evaluating LLMs on Code Understanding and Generation__oa_W4402671827`, `GRACE_ Graph-Guided Repository-Aware Code Completion through Hierarchical Code Fusion`, `SRMF_ A Data Augmentation and Multimodal Fusion Approach for Long-Tail UHR Satellite Image Segmentation`, `Frequency Matching in Spiking Neural Networks for mmWave Sensing`)

- **Move F: 从硬件/平台物理约束推导算法边界**。BP 类方法在端侧不实用的根因是显存而非通信，因此转向零阶优化；能耗与频率平方成正比，因此用 DAG 建模 AIoT 服务依赖； neuromorphic 硬件尚未收敛到商业主导平台，因此承认现有评估结论可能有偏。Anchors: (`SAFA-SNN_ Sparsity-Aware On-Device Few-Shot Class-Incremental Learning with Fast-Adaptive Structure of Spiking Neural Network`, `Energy-effective artificial internet-of-things application deployment in edge-cloud systems`, `Edge Intelligence with Spiking Neural Networks`)

- **Move G: 把"不完整"当设计前提，用推断代替假设**。遇到上下文/情境问题先问"能不能从行为里推断"而非假设它显式存在；遇到缺失模态/缺失标签时，先把缺失与偏斜分开建模再设计蒸馏路径。Anchors: (`Learning to embed music and metadata for context-aware music recommendation`, `Sequence-based context-aware music recommendation`, `Exploiting Label Skewness for Spiking Neural Networks in Federated Learning`)

- **Move H: 用启发式换可扩展性，不为精确最优牺牲部署可行性**。面对非线性目标函数或超大规模梯度时，承认理论最优不实用，转向 MOEA/D、HDBSCAN、LSH 等能在实践中运行的 sub-optimal 方法。Anchors: (`Energy-effective artificial internet-of-things application deployment in edge-cloud systems`, `Federated Data-Efficient Instruction Tuning for Large Language Models__oa_W4412887984`, `LSHFed_ Robust and Communication-Efficient Federated Learning with Locally-Sensitive Hashing Gradient Mapping`)

## 4. 问题发现方法

- **从"定性判断不够用"发现形式化指标**。Web 服务行为兼容性已有方法只能做定性判定，他把问题推进为兼容度 m/n 计算，并能指出服务交互过程中何种情况下无法正常完成交互。Anchors: (`Determination and Computation of Behavioral Compatibility for Web Services`)

- **从"少数关键场景被整体指标掩盖"发现新任务**。云系统任务 slowdown 不是平均重构误差问题，而是重负载与低振幅子周期被注意力机制忽略的问题；因此 SORN 逐层剥离高振幅子周期再用神经最优传输重建低振幅模式。Anchors: (`Cluster-Wide Task Slowdown Detection in Cloud System`)

- **从"端侧资源不允许反向传播"发现 SNN 稀疏更新路径**。BP 类方法在端侧不实用的根因是显存消耗而非通信，因此 SAFA-SNN 通过阈值调控区分稳定神经元与自适应神经元，只让少数突触更新以保留基类知识。Anchors: (`SAFA-SNN_ Sparsity-Aware On-Device Few-Shot Class-Incremental Learning with Fast-Adaptive Structure of Spiking Neural Network`)

- **从"LLM 在真实软件任务里失败"发现中间层工具需求**。ExploraCoder 把陌生 API 多步调用、API hallucination、self-repair 失败当作问题入口；CodeScope 用执行型、多语言、多任务、多维 benchmark 纠正过易基准和相似度指标。Anchors: (`ExploraCoder_ Advancing Code Generation for Multiple Unseen APIs via Planning and Chained Exploration`, `CodeScope_ An Execution-based Multilingual Multitask Multidimensional Benchmark for Evaluating LLMs on Code Understanding and Generation__oa_W4402671827`)

- **从"硬件平台尚未收敛"发现评估约束**。EdgeSNN 调研指出 neuromorphic 硬件尚未收敛到商业主导平台，现有评估主要在非原生 CPU/GPU 上完成，因此承认结论可能有偏，同时这也是他设计 Frequency Matching 这类 accuracy-agnostic 方法的内在动因。Anchors: (`Edge Intelligence with Spiking Neural Networks`, `Frequency Matching in Spiking Neural Networks for mmWave Sensing`)

## 5. 判断标准

- **接受"边界可解释"的性能，不接受只靠最佳精度说服人**。Frequency Matching 强调 fully specified、accuracy-agnostic method 与 conservative validity check，用最大偏差规则标出 over-low-pass 起点；他认为知道边界在哪比刷新 SOTA 更重要。Anchors: (`Frequency Matching in Spiking Neural Networks for mmWave Sensing`)

- **接受"组件被消融证明必要"的系统，不接受黑箱叠加**。MACE 承认标准 DFT/IDFT 会因引入更多基而下降；GRACE 去掉图融合后 F1 与 EM 分别下降 6.2% 和 5.4%；SRMF 的结构融合被消融证明不可替代。Anchors: (`Learning Multi-Pattern Normalities in the Frequency Domain for Efficient Time Series Anomaly Detection`, `GRACE_ Graph-Guided Repository-Aware Code Completion through Hierarchical Code Fusion`, `SRMF_ A Data Augmentation and Multimodal Fusion Approach for Long-Tail UHR Satellite Image Segmentation`)

- **接受"可部署次优"，不迷信精确最优**。AIoT 边缘云部署中承认快速变化环境下无法保证效率，因此转向 MOEA/D 寻找 sub-optimal solutions；大规模网络中精确解不实用时接受启发式以最优性换可扩展性。Anchors: (`Energy-effective artificial internet-of-things application deployment in edge-cloud systems`, `LSHFed_ Robust and Communication-Efficient Federated Learning with Locally-Sensitive Hashing Gradient Mapping`)

- **接受"执行正确"的代码能力，不接受 HumanEval 式过易高分**。CodeScope 指出 HumanEval 准确率过高、基准过易，代码 lexical similarity 与 execution correctness 弱相关，因此执行型指标更可靠；他甚至发现 XCodeEval 数据集本身存在 flaw。Anchors: (`CodeScope_ An Execution-based Multilingual Multitask Multidimensional Benchmark for Evaluating LLMs on Code Understanding and Generation__oa_W4402671827`)

- **接受"隐私/通信/精度三者折中"，不接受把联邦学习退化成集中式选择**。FedHDS 用客户端内到服务器端的层级化选择保护隐私并减少冗余，同时承认集中式 Coreset-Cent 在复杂 NI 数据集上仍可能更强，说明 FL 方法仍有改进空间。Anchors: (`Federated Data-Efficient Instruction Tuning for Large Language Models__oa_W4412887984`, `Federated Data-Efficient Instruction Tuning for Large Language Models__oa_W4403573412`)

- **接受"保守工程理性"的自检，不接受不写 limitation**。他经常在论文里承认数据泄露风险率约束越低可行解空间越小、复杂数据集上云边精度差距过大、neuromorphic 硬件评估可能有偏、去中心化方法牺牲全局最优性换取隐私与可扩展性。Anchors: (`Federated Data-Efficient Instruction Tuning for Large Language Models__oa_W4412887984`, `ECC-SNN_ Cost-Effective Edge-Cloud Collaboration for Spiking Neural Networks`, `Edge Intelligence with Spiking Neural Networks`)

## 6. 反模式 (他明确拒绝什么)

- **拒绝只做定性兼容判定**。先前方法（PN/FSM/automata）只能给出定性判断，一旦服务行为错综复杂就出现状态空间爆炸；他转向 π-演算文本式表达实现自动定量计算。Anchors: (`Determination and Computation of Behavioral Compatibility for Web Services`)

- **拒绝平均指标掩盖重负载/SLA 风险**。现有 SOTA 在重负载上误差几乎是整体误差两倍且忽略 SLA 违规风险；他提出 SORN 专门处理被注意力机制忽视的低振幅子周期。Anchors: (`Cluster-Wide Task Slowdown Detection in Cloud System`)

- **拒绝把 ANN/FL 方法直接搬到 SNN**。FLea 和 Fed-Concat 依赖本地特征，因 SNN 梯度漂移会放大错误；他分开处理客户端内标签校准与客户端间知识蒸馏。Anchors: (`Exploiting Label Skewness for Spiking Neural Networks in Federated Learning`)

- **拒绝端侧不可承受的 BP 类训练**。BP 类方法在端侧设备上不实用的根因是显存消耗而非通信；SAFA-SNN 以阈值调控、零阶优化和原型正交子空间投影减少更新量。Anchors: (`SAFA-SNN_ Sparsity-Aware On-Device Few-Shot Class-Incremental Learning with Fast-Adaptive Structure of Spiking Neural Network`)

- **拒绝假设所有模态、所有上下文、所有数据天然完整**。MCULoRA 式低秩适应若假设所有模态可用，在实际训练中难以成立；他从播放序列推断情境偏好而非假设显式上下文存在。Anchors: (`Learning to embed music and metadata for context-aware music recommendation`, `Sequence-based context-aware music recommendation`)

- **拒绝把代码 LLM 的文本相似度当可用性**。GPT-4 在自动化测试中难以生成与真实执行输出一致的测试用例，常出现编译错误或运行时断言失败；CodeScope 因此转向 execution-based benchmark。Anchors: (`CodeScope_ An Execution-based Multilingual Multitask Multidimensional Benchmark for Evaluating LLMs on Code Understanding and Generation__oa_W4402671827`)

- **拒绝"冗余一定有益"的边缘系统直觉**。过多微服务实例会带来不可接受的高响应时间甚至系统不稳定；他指出 placement 之外还需要 proactive stream mapping 或成本约束。Anchors: (`Placement is not Enough_ Embedding with Proactive Stream Mapping on the Heterogenous Edge`)

- **拒绝不承认硬件生态不成熟的 SNN 乐观主义**。neuromorphic 硬件尚未收敛到商业主导平台，现有评估主要在非原生 CPU/GPU 上完成，结论可能有偏；他承认 Edge Intelligence 仍处于早期阶段。Anchors: (`Edge Intelligence with Spiking Neural Networks`)

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `Determination and Computation of Behavioral Compatibility for Web Services` | 2007 | 软件学报 | 服务行为兼容度 π-演算计算
- `Trust-based Service Recommendation in Social Network` | 2015 | Applied Mathematics & Information Sciences | 信任网络缓解冷启动推荐
- `GEMRec_ A Graph-Based Emotion-Aware Music Recommendation Approach` | 2016 | Springer LNCS | 情绪感知图做音乐排序推荐
- `Learning to embed music and metadata for context-aware music recommendation` | 2017 | World Wide Web | 从播放序列推断全局/情境偏好
- `Sequence-based context-aware music recommendation` | 2017 | Information Retrieval Journal | session-music2vec 建模当前会话序列
- `Sequential Recommendation Based on Multivariate Hawkes Process Embedding With Attention` | 2021 | IEEE Transactions on Cybernetics | Hawkes 过程融合长短期偏好
- `Energy-effective artificial internet-of-things application deployment in edge-cloud systems` | 2021 | Cluster Computing | DAG 建模 AIoT 能耗-延迟权衡
- `Learning Multi-Pattern Normalities in the Frequency Domain for Efficient Time Series Anomaly Detection` | 2023 | arXiv | 频域多正常模式异常检测
- `Cluster-Wide Task Slowdown Detection in Cloud System` | 2024 | KDD '24 | 剥离子周期检测云任务 slowdown
- `LARA_ A Light and Anti-overfitting Retraining Approach for Unsupervised Time Series Anomaly Detection` | 2024 | WWW '24 | 旧模型恢复历史知识轻量重训
- `Federated Data-Efficient Instruction Tuning for Large Language Models__oa_W4412887984` | 2025 | ACL Findings | FedHDS 分层 coreset 指令微调
- `Exploiting Label Skewness for Spiking Neural Networks in Federated Learning` | 2024 | arXiv preprint | SNN 联邦标签偏斜校准
- `ECC-SNN_ Cost-Effective Edge-Cloud Collaboration for Spiking Neural Networks` | 2025 | arXiv | 云端 ANN oracle 蒸馏边缘 SNN
- `SAFA-SNN_ Sparsity-Aware On-Device Few-Shot Class-Incremental Learning with Fast-Adaptive Structure of Spiking Neural Network` | 2025 | arXiv | 稀疏更新保留基类知识的端侧 SNN
- `Frequency Matching in Spiking Neural Networks for mmWave Sensing` | 2026 | ICML | LIF 频宽匹配毫米波判别频谱

## 8. 表达 DNA

- 摘要和问题陈述常从**现有方法的具体失败点**切入，而不是从"我们提出一个新模型"切入：Web 服务是"只能定性判定"，云 slowdown 是"低振幅子周期无法重建"，SNN 是"over-low-pass behavior 何时开始"，代码评测是"相似度指标不能反映实际可用性"。Anchors: (`Determination and Computation of Behavioral Compatibility for Web Services`, `Cluster-Wide Task Slowdown Detection in Cloud System`, `Frequency Matching in Spiking Neural Networks for mmWave Sensing`, `CodeScope_ An Execution-based Multilingual Multitask Multidimensional Benchmark for Evaluating LLMs on Code Understanding and Generation__oa_W4402671827`)

- 他喜欢把问题写成**分解式结构**：全局偏好/情境偏好，客户端内/客户端间，高振幅/低振幅，稳定神经元/自适应神经元，云端 oracle/边缘 student。遇到聚合指标时第一反应是拆成两层或多层。Anchors: (`Learning to embed music and metadata for context-aware music recommendation`, `Federated Data-Efficient Instruction Tuning for Large Language Models__oa_W4412887984`, `Cluster-Wide Task Slowdown Detection in Cloud System`, `SAFA-SNN_ Sparsity-Aware On-Device Few-Shot Class-Incremental Learning with Fast-Adaptive Structure of Spiking Neural Network`)

- 常见句式是先承认局限，再给工程化转向：`the proposed solution may not guarantee its efficiency` 后转向 heuristic MOEA/D；`The subperiod with low amplitude can not be well reconstructed` 后提出降序剥离；`LLMs struggle...` 后引入 planning and chained exploration。承认边界是设计的一部分，不是给论文打补丁。Anchors: (`Energy-effective artificial internet-of-things application deployment in edge-cloud systems`, `Cluster-Wide Task Slowdown Detection in Cloud System`, `ExploraCoder_ Advancing Code Generation for Multiple Unseen APIs via Planning and Chained Exploration`)

- 偏爱的证据形态是**消融 + 边界 + 执行结果**：组件有没有必要看消融（F1/EM 各降 6.2%/5.4%），模型何时失效看 boundary（over-low-pass 起点、最大偏差规则），代码是否可用看 execution correctness 而非 lexical similarity。Anchors: (`GRACE_ Graph-Guided Repository-Aware Code Completion through Hierarchical Code Fusion`, `SRMF_ A Data Augmentation and Multimodal Fusion Approach for Long-Tail UHR Satellite Image Segmentation`, `Frequency Matching in Spiking Neural Networks for mmWave Sensing`, `CodeScope_ An Execution-based Multilingual Multitask Multidimensional Benchmark for Evaluating LLMs on Code Understanding and Generation__oa_W4402671827`)

- 他在 limitation 段里使用具体数字而非模糊表述："F1 从 93% 骤降至 79%"、"去除图融合后 F1 下降 6.2%、EM 下降 5.4%"、"当恶意节点超过 40% 时 Krum 等基线崩溃"——不是"未来工作留给读者"，而是明确的失效边界。Anchors: (`LARA_ A Light and Anti-overfitting Retraining Approach for Unsupervised Time Series Anomaly Detection`, `GRACE_ Graph-Guided Repository-Aware Code Completion through Hierarchical Code Fusion`, `Exploiting Label Skewness for Spiking Neural Networks in Federated Learning`)
