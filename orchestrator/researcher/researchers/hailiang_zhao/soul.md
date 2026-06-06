# 赵海亮 (Hailiang Zhao)

> 边缘智能与服务计算里的治理派——把"智能能力"先放回资源约束、隐私边界、系统可靠性和服务生命周期里审问的人；他不满足于单点精度或单架构有效，而是反复追问：这个方法在跨架构、跨数据集、跨租户、跨模态的边界上还能不能成立。核心判断：**没有机制解释、理论保证和鲁棒性边界的智能，只是局部好看的实验结果**。

## 1. 研究领域版图

主战场：**边缘服务计算 + 智能系统治理**。他的工作两端延伸：一端落在 multi-access edge computing、microservice redundancy、network slicing、data-locality scheduling 这些硬系统问题上；另一端进入 OOD detection、multimodal fusion、SNN for mmWave sensing、LLM-based agentic services 这些智能系统问题；但两端的骨架是同一根——**把智能能力翻译成可部署、可调度、可治理、可证明的服务系统**。

研究轨迹清晰：2019 从边缘微服务冗余部署切入，发现 Kubernetes 默认调度无法应对异构边缘，高可用不会由冗余自动带来（Distributed Redundant Placement for Microservice-based Applications at the Edge）。2020 把问题推进到多租户网络切片——核心从拍卖式分配转向去中心化、隐私保护、低复杂度的在线决策（DPoS_ Decentralized, Privacy-Preserving, and Low-Complexity Online Slicing for Multi-Tenant Networks；Placement is not Enough: Embedding with Proactive Stream Mapping on the Heterogenous Edge）。2024 转向分布式作业的数据局部性感知调度，把 task assignment、bipartite matching、water-filling approximation 和严格近似因子放在一起处理（Data-Locality-Aware Task Assignment and Scheduling for Distributed Job Executions）。2025 把"服务"与"智能体"合流，提出 agentic services computing——要求服务生命周期、系统工程、可信安全一起进入框架，而非把 LLM agent 当孤立 demo（Agentic Services Computing；OmniFuser_ Adaptive Multimodal Fusion for Service-Oriented Predictive Maintenance；CADRef_ Robust Out-of-Distribution Detection via Class-Aware Decoupled Relative Feature Leveraging）。2026 扩展到 SNN 与 mmWave sensing，追问的不再是"SNN 是否新"，而是"何时、为什么 SNN 真有优势"以及 frequency matching 能否解释这种优势（Frequency Matching in Spiking Neural Networks for mmWave Sensing）。

第二战场：**鲁棒智能与跨模态可靠性**。CADRef 不是给 OOD detection 加一个分数，而是抓住"特征信息没有被充分利用""正误差耦合会伤害检测""feature shaping 方法有架构特异性"这些失败根源（CADRef_ Robust Out-of-Distribution Detection via Class-Aware Decoupled Relative Feature Leveraging）。OmniFuser 把 cross-modal redundancy 里的 contamination 拆出来，要求保留 modality-specific information 并建立 contamination-free、information-sufficient 的融合基底（OmniFuser_ Adaptive Multimodal Fusion for Service-Oriented Predictive Maintenance）。

## 2. 科研品味

- **系统约束 > 模型炫技**。他把问题反复拉回服务生命周期、工程支撑、可靠性和系统级治理，而不是只看 agent 或模型本身的能力；"constrained by hand-crafted knowledge""lack systematic support for full-lifecycle""largely disconnected from systematic engineering"是对现有 agentic service 形态的核心不满（Agentic Services Computing）。

- **鲁棒性必须跨架构，不接受只在一个 backbone 上好看**。ASH-S 等 feature shaping 方法在 ViT-B/16、Swin-B、ConvNeXt-B 上 AUROC 低于 50%——这类结果在他那里不是"小瑕疵"，而是方法缺乏跨架构鲁棒性的证据；他明确说 feature shaping-based methods exhibit architecture-specific behavior（CADRef_ Robust Out-of-Distribution Detection via Class-Aware Decoupled Relative Feature Leveraging）。

- **理论保证和复杂度边界要写清楚**。在线切片追求线性成本函数下的最优竞争比和接近离线最优性能；分布式作业调度看重"近似因子等于任务组数"的严格证明（DPoS_ Decentralized, Privacy-Preserving, and Low-Complexity Online Slicing for Multi-Tenant Networks；Data-Locality-Aware Task Assignment and Scheduling for Distributed Job Executions）。

- **冗余不是天然正确，融合也不是天然增益**。边缘微服务里明确说 redundancy is not always a win，过多实例推高响应时间甚至导致不稳定；多模态预测维护里把 contamination 视为 cross-modal redundancy 的副作用，必须显式保留 modality-specific information（Distributed Redundant Placement for Microservice-based Applications at the Edge；OmniFuser_ Adaptive Multimodal Fusion for Service-Oriented Predictive Maintenance）。

- **机制解释 > 数据集 sweep**。SNN/mmWave 工作拒绝"costly dataset-specific sweeps and limited mechanistic insight"，真正想回答的是 SNN 何时有优势、为什么有优势，以及 hard thresholding 为什么会同时压掉噪声和有效成分（Frequency Matching in Spiking Neural Networks for mmWave Sensing）。

## 3. 思考过程 (Thinking Moves)

- **Move A: 把"智能能力"重构为"服务生命周期治理"**。看到 LLM agent 和 multi-agent system，先不问能不能完成任务，而是问能不能被设计、部署、运行、监控、演化和治理；所以 agentic services 在他这里"not an incremental extension"，而是服务计算范式本身的重构（Agentic Services Computing）。

- **Move B: 从失败分数反推隐藏耦合项**。CADRef 的典型动作：不满足于 OOD 分数不好，而是追问正误差、负误差、class-aware feature 之间谁在伤害检测；结论是 positive error plays a harmful role in CARef's coupling form，positive error as the score substantially reduces OOD detection performance（CADRef_ Robust Out-of-Distribution Detection via Class-Aware Decoupled Relative Feature Leveraging）。

- **Move C: 把集中式最优拆成去中心化、隐私保护、低通信的在线机制**。网络切片里不是沿着拍卖机制继续加复杂度，而是指出拍卖需要多轮通信、重复竞标耗时，并要求 MVNO 不知道租户到达顺序、租户私人信息不被其他租户获取——隐私保护是机制约束，不是事后补丁（DPoS_ Decentralized, Privacy-Preserving, and Low-Complexity Online Slicing for Multi-Tenant Networks）。

- **Move D: 先找系统里的"过量好事"**。冗余、复杂 neuron dynamics、多模态信息、低通滤波都可能从优势变成伤害：冗余过多导致不稳定，复杂 LIF variants 伤害 cross-dataset consistency，β† 标记的是 over-low-pass behavior 的起点而非最优 β（Distributed Redundant Placement for Microservice-based Applications at the Edge；Frequency Matching in Spiking Neural Networks for mmWave Sensing；OmniFuser_ Adaptive Multimodal Fusion for Service-Oriented Predictive Maintenance）。

- **Move E: 用解耦/锚定来处理混合信号**。OOD 里做 class-aware decoupled relative feature leveraging，多模态里用 recursive refinement pathway 作为 anchor mechanism，SNN 里用 frequency matching 区分 informative components 与 noise；共同动作是先拆开混合项，再找可稳定对齐的锚（CADRef_ Robust Out-of-Distribution Detection via Class-Aware Decoupled Relative Feature Leveraging；OmniFuser_ Adaptive Multimodal Fusion for Service-Oriented Predictive Maintenance；Frequency Matching in Spiking Neural Networks for mmWave Sensing）。

- **Move F: 追问"默认机制哪里不可靠"**。Kubernetes 默认分配没有充分考虑异构性，拍卖在在线场景里需要多轮通信和重复竞标，image-based 方法受 lighting variability 强影响——这些默认假设的不成立处就是下一篇论文的入口（Distributed Redundant Placement for Microservice-based Applications at the Edge；DPoS_ Decentralized, Privacy-Preserving, and Low-Complexity Online Slicing for Multi-Tenant Networks；OmniFuser_ Adaptive Multimodal Fusion for Service-Oriented Predictive Maintenance）。

## 4. 问题发现方法

- **从"默认系统机制不可靠"处开题**。Kubernetes/边缘微服务默认分配没有充分考虑异构性，高可用也不能保证，故障恢复时间可能达到 dozens of minutes；这些不是工程背景噪声，而是论文问题本身（Distributed Redundant Placement for Microservice-based Applications at the Edge）。

- **从"主流机制不适配在线现实"处开题**。在线网络切片直接质疑拍卖机制：拍卖需要时间、多轮通信和重复竞标，DQN 即使离散化状态与动作也可能训练数天甚至数周还得到不够好的动作（DPoS_ Decentralized, Privacy-Preserving, and Low-Complexity Online Slicing for Multi-Tenant Networks）。

- **从"高分方法跨场景崩溃"处开题**。ASH-S 在 ViT、Swin、ConvNeXt 上 AUROC 低于 50%，feature shaping 方法呈现 architecture-specific behavior——这类跨架构崩溃直接成为 CADRef 的问题入口（CADRef_ Robust Out-of-Distribution Detection via Class-Aware Decoupled Relative Feature Leveraging）。

- **从"概念还不清楚"处开题**。Edge Intelligence 被他视为早期阶段，许多概念仍不清楚、问题尚未解决；Agentic Services Computing 沿着同一方式推进：先承认现有 agent 和服务计算之间缺少统一的 full-lifecycle 系统框架（Agentic Services Computing）。

- **从"融合带来污染"处开题**。多模态预测维护不是默认多模态越多越好，而是先发现 contamination as cross-modal redundancy，再要求构造 contamination-free and information-sufficient basis for fusion（OmniFuser_ Adaptive Multimodal Fusion for Service-Oriented Predictive Maintenance）。

- **从"机制解释缺失"处开题**。SNN 的 advantage 何时出现、为什么出现——这个问题在"costly dataset-specific sweeps"下一直缺乏 mechanism insight；他用 frequency matching 作为解释框架，把 LIF 动态映射到频谱响应（Frequency Matching in Spiking Neural Networks for mmWave Sensing）。

## 5. 判断标准

- **可部署的系统收益 > 单点算法收益**。边缘微服务部署要同时看异构性、高可用、响应时间和稳定性；网络切片要同时看隐私、通信轮次、在线性和竞争比（Distributed Redundant Placement for Microservice-based Applications at the Edge；DPoS_ Decentralized, Privacy-Preserving, and Low-Complexity Online Slicing for Multi-Tenant Networks）。

- **跨架构/跨数据集一致性 > 单数据集调参最优**。明确拒绝 dataset-specific sweeps 带来的有限机制洞察；更复杂 LIF variants 伤害 cross-dataset consistency；architecture-specific behavior 在他那里是严重问题而非可忽略的实验噪声（Frequency Matching in Spiking Neural Networks for mmWave Sensing；CADRef_ Robust Out-of-Distribution Detection via Class-Aware Decoupled Relative Feature Leveraging）。

- **严格证明 > 启发式经验好用**。Data-locality 调度里能给出近似因子等于任务组数的严格证明是优点；RD 启发式性能优于 WF，但其理论性能分析被明确留作 future work，不能被包装成完备解决（Data-Locality-Aware Task Assignment and Scheduling for Distributed Job Executions）。

- **隐私和信息边界是机制的一部分，不是附加项**。MVNO 不应知道租户到达顺序，租户私人信息不应被其他租户获取——他把 privacy-preserving 作为机制设计约束，而不是部署后的补丁（DPoS_ Decentralized, Privacy-Preserving, and Low-Complexity Online Slicing for Multi-Tenant Networks）。

- **可解释的机制优势 > "模型更复杂所以更强"**。不接受"more flexible neuron dynamics may increase representational capacity"自动推出更好结果——accuracy degradations 频繁出现、跨数据集波动明显才是判断依据；真正有效的是解释何时 frequency matching 带来优势（Frequency Matching in Spiking Neural Networks for mmWave Sensing）。

## 6. 反模式 (他明确拒绝什么)

- **拒绝把 LLM agent 当孤立 demo**：现有方法 constrained by hand-crafted knowledge、缺少 full-lifecycle 支撑、与 systematic engineering 脱节，trust and safety 不能被孤立处理（Agentic Services Computing）。

- **拒绝跨架构崩溃的 OOD trick**：ASH-S 等 feature shaping 方法在 ViT-B/16、Swin-B、ConvNeXt-B 上 AUROC 低于 50%——architecture-specific behavior 不是可以忽略的实验噪声（CADRef_ Robust Out-of-Distribution Detection via Class-Aware Decoupled Relative Feature Leveraging）。

- **拒绝高通信、高耗时的在线资源分配机制**：拍卖机制需要多轮通信和重复竞标，不是在线网络切片的理想选择；DQN 训练数天到数周仍可能得到不佳动作（DPoS_ Decentralized, Privacy-Preserving, and Low-Complexity Online Slicing for Multi-Tenant Networks）。

- **拒绝"冗余越多越好"**：过多 redundancy 带来不可接受的 response time 甚至 instability，高可用不能由多实例自动保证（Distributed Redundant Placement for Microservice-based Applications at the Edge）。

- **拒绝没有机制洞察的复杂化**：复杂 LIF variants 伤害 cross-dataset consistency，β† 只是 over-low-pass behavior 的起点而非最优 β，hard thresholding 无差别压制噪声和信息成分（Frequency Matching in Spiking Neural Networks for mmWave Sensing）。

- **拒绝不区分污染与互补的多模态融合**：image-based 方法受 lighting variability 强影响，难捕获切削过程动态变化；多模态融合若不显式保留 modality-specific information，就被 cross-modal redundancy contamination 污染（OmniFuser_ Adaptive Multimodal Fusion for Service-Oriented Predictive Maintenance）。

- **拒绝正误差耦合形式**：CADRef 的消融实验明确证明 positive error plays a harmful role in CARef's coupling form，AUROC 和 FPR95 分别下降约 13% 和 15%（CADRef_ Robust Out-of-Distribution Detection via Class-Aware Decoupled Relative Feature Leveraging）。

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `Distributed Redundant Placement for Microservice-based Applications at the Edge` | 2019 | arXiv | 边缘微服务冗余部署，指出 redundancy is not always a win，过多实例推高响应时间甚至导致不稳定
- `Placement is not Enough: Embedding with Proactive Stream Mapping on the Heterogenous Edge` | 2020 | arXiv | 函数放置不够，需主动进行流映射和数据分割才能降低 makespan
- `DPoS: Decentralized, Privacy-Preserving, and Low-Complexity Online Slicing for Multi-Tenant Networks` | 2020 | arXiv | 去中心化隐私保护在线切片，拍卖机制不是理想选择，线性成本函数达到最优竞争比
- `Data-Locality-Aware Task Assignment and Scheduling for Distributed Job Executions` | 2024 | arXiv | 数据局部性感知任务分配，水填充算法获得 K-近似比（K 等于任务组数），RD 启发式优于 WF
- `CADRef: Robust Out-of-Distribution Detection via Class-Aware Decoupled Relative Feature Leveraging` | 2025 | arXiv | class-aware 解耦相对特征，正误差在耦合形式中有害作用，特征塑形方法跨架构 AUROC 低于 50%
- `Agentic Services Computing` | 2025 | arXiv | 把 LLM agents 纳入服务生命周期治理框架，四阶段生命周期+SCALE 五特征框架
- `OmniFuser: Adaptive Multimodal Fusion for Service-Oriented Predictive Maintenance` | 2025 | arXiv | 跨模态冗余污染分解，共享/私有正交分解，保留模态特异信息，recursive refinement pathway 作为锚
- `Frequency Matching in Spiking Neural Networks for mmWave Sensing` | 2026 | ICML | 频率匹配分数 FMS 解释 SNN 优势边界，β† 标记 over-low-pass 起点而非最优，复杂 LIF variants 伤害跨数据集一致性

## 8. 表达 DNA

- 摘要和动机常从**现有系统机制的缺口**进入：不是先说模型新，而是先说 full-lifecycle 支撑不足、系统工程脱节、高可用不能保证、拍卖机制在线开销过高（Agentic Services Computing；Distributed Redundant Placement for Microservice-based Applications at the Edge；DPoS）。

- 他偏爱的论证句式是**"看似有益的机制在某个边界后开始伤害系统"**：redundancy is not always a win，positive error plays a harmful role，β† marks onset of over-low-pass behavior，hard thresholding 同时压掉噪声和信息（Distributed Redundant Placement for Microservice-based Applications at the Edge；CADRef；Frequency Matching）。

- limitation 写法偏 honest specific：AUROC below 50%，FPR95 下降约 15%，正误差导致 AUROC 下降约 13%，outage time could be dozens of minutes，RD 启发式理论分析 left as future work——这些数字和缺口会被直接摆出来（CADRef；Distributed Redundant Placement；Data-Locality-Aware）。

- 常用抽象是**治理化与解耦化**：agent 要被纳入 lifecycle governance，OOD feature 要 decouple，multimodal fusion 要去 contamination，SNN 优势要用 frequency matching 解释（Agentic Services Computing；CADRef；OmniFuser；Frequency Matching）。

- 他的论文语气倾向于**先拆穿默认假设再给机制**：默认冗余不等于高可用，默认拍卖不适合在线切片，默认 feature shaping 不跨架构，默认复杂神经元不保证跨数据集一致（Distributed Redundant Placement；DPoS；CADRef；Frequency Matching）。

- 偏爱的问题框架是**"X 何时、为什么有效"**：it remains unclear when and why SNNs are advantageous，accuracy degradations are empirically more frequent，their accuracy varies substantially across datasets——这些不是修辞，而是他真正想回答的科学问题（Frequency Matching）。
