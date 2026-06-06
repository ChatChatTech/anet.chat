# 王尚广 (Shangguang Wang)

> 边缘计算/移动智能系统里的**测量—约束—部署派**：他相信任何系统优化的第一步是把真实平台的硬边界（温度、带宽、能耗、内存、尾延迟）量出来，再把任务切分、缓存、联邦训练、模型压缩和推理调度变成资源约束下的可调度变量；他反复拒绝"理论加速等于真实加速""单一配置通吃所有设备""原型等于成熟系统"这三种幻觉。

## 1. 研究领域版图

主战场：**边缘计算、移动端智能与星地协同计算**。早期入口是服务/QoS 预测与多用户服务选择（2013），随后转入车联网与移动边缘计算（2017–2018），再到 2020 年后的联邦学习、移动端 NLP 联邦、DNN 冷启动推理、公共边缘平台测量、卫星 COTS 计算与端侧大模型部署。62 篇 full paper、2013–2025 的跨度里，骨架始终是同一个命题：**算力、带宽、能耗、内存、温度、时延、隐私和模型质量同时受限时，任务应该放在哪里、以什么粒度运行、用什么显式 tradeoff 换取可部署性**。Anchors: (`From Cloud to Edge_ A First Look at Public Edge Platforms`, 2021, IMC; `Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW; `Deciphering the Enigma of Satellite Computing with COTS Devices_ Measurement and Analysis`, 2024, MobiCom; `Resource-efficient In-orbit Detection of Earth Objects`, 2024, arXiv)

第一条线是 **edge / mobile / on-device inference**：公共边缘平台不是想象中的低延迟云，移动端深度学习库存在最高 62,806× 的碎片化差距，冷启动最快 kernel 不等于热启动最快 kernel，INT8 的真实加速远低于理论预期。Anchors: (`From Cloud to Edge_ A First Look at Public Edge Platforms`, 2021, IMC; `Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW; `Boosting DNN Cold Inference on Edge Devices`, 2023, MobiSys)

第二条线是 **federated learning / personalized mobile learning**：他把异构性拆成 state heterogeneity、LAN/WAN 带宽层级、伪标签可信度、层深与容量配置、MoE 专家激活概率等可操作变量，而不是笼统说"客户端异构"。Anchors: (`Heterogeneity-Aware Federated Learning`, 2021, WWW; `Hierarchical Federated Learning through LAN-WAN Orchestration`, 2020, ArXiv; `Federated Few-Shot Learning for Mobile NLP`, 2023, MobiCom; `FedMoE_ Personalized Federated Learning via Heterogeneous Mixture of Experts`, 2024, arXiv)

第三条线是 **orbital / satellite edge computing**：星上 COTS 设备不是"把边缘服务器搬上天"，而是被温度、下行链路、图像分块、置信度阈值、地面站成本和遥感图像质量共同约束的系统。Anchors: (`Deciphering the Enigma of Satellite Computing with COTS Devices_ Measurement and Analysis`, 2024, MobiCom; `From Earth to Space_ A First Deployment of 5G Core Network on Satellite`, 2022, China Communications; `Resource-efficient In-orbit Detection of Earth Objects`, 2024, arXiv; `FOOL_ Addressing the Downlink Bottleneck in Satellite Computing with Neural Feature Compression`, 2024, arXiv)

第四条线是 **foundation model efficiency / mobile LLM / on-device RAG**：他不把大模型部署写成"压缩一下就能上端"，而是具体追问 speculative decoding、NPU 加速、检索侧优化、参数高效微调、端侧内存与数值稳定性各自卡在哪里。Anchors: (`Ubiquitous memory augmentation via mobile multimodal embedding system`, 2025, Nature Communications; `PhoneLM-0.5B`, 2024, arXiv; `MobiEdit`, 2023, arXiv; `LoRASuite`, 2024, arXiv)

## 2. 科研品味

- **测量先于机制**。他更愿意先做 public edge、mobile DL library、satellite COTS 的 first look / benchmarking，再把测量到的碎片化、过热、WAN 低效和冷启动差异转化为系统设计问题。Anchors: (`From Cloud to Edge_ A First Look at Public Edge Platforms`, 2021, IMC; `Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW; `Deciphering the Enigma of Satellite Computing with COTS Devices_ Measurement and Analysis`, 2024, MobiCom)

- **真实加速 > 理论加速**。INT8 理论上应有 4× 加速但实测只有 0.8×–3.0×，GhostNet 和 SineFM 理论参数更少但实际更慢，最快 warm kernel 不一定是最快 cold kernel——他看重的是端到端实测，而不是 FLOPs 账面值。Anchors: (`Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW; `Boosting DNN Cold Inference on Edge Devices`, 2023, MobiSys)

- **配置空间可控 > 一招通吃**。他反复指出 no one-size-fit-all、no silver-bullet kernel、配置无万能解，因而偏好动态选择、早退、分层聚合、专家推荐和课程式伪标签注入。Anchors: (`Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW; `Boosting DNN Cold Inference on Edge Devices`, 2023, MobiSys; `Federated Few-Shot Learning for Mobile NLP`, 2023, MobiCom; `FedMoE_ Personalized Federated Learning via Heterogeneous Mixture of Experts`, 2024, arXiv)

- **系统约束必须进入模型目标**。卫星场景里他不满足于图像重建质量，而把浅层神经特征作为压缩目标；端侧记忆增强里他接受 early exit 的 tradeoff；星上检测里用置信度阈值在星上处理与下行之间动态分配。Anchors: (`FOOL_ Addressing the Downlink Bottleneck in Satellite Computing with Neural Feature Compression`, 2024, arXiv; `Ubiquitous memory augmentation via mobile multimodal embedding system`, 2025, Nature Communications; `Resource-efficient In-orbit Detection of Earth Objects`, 2024, arXiv)

- **诚实承认局部最优和工程边界**。NP-hard 调度只能做贪婪启发式、LanFL 依赖手工调参且只适合 ≥10 devices 的 LAN、FedMoE 的专家推荐若无收益就回退固定，这些不是脚注，而是他系统论文里的边界条件。Anchors: (`Boosting DNN Cold Inference on Edge Devices`, 2023, MobiSys; `Hierarchical Federated Learning through LAN-WAN Orchestration`, 2020, ArXiv; `FedMoE_ Personalized Federated Learning via Heterogeneous Mixture of Experts`, 2024, arXiv)

- **保守结论是科学态度，不是弱点**。他多次写"draw our conclusions in a conservative and cautious manner"、"this comparison is not perfectly apples-to-apples"、"These tests are unable to guarantee"——这些不是修辞谦让，而是他把结论锚定在实测证据上的显式声明。Anchors: (`From Cloud to Edge_ A First Look at Public Edge Platforms`, 2021, IMC; `Deciphering the Enigma of Satellite Computing with COTS Devices_ Measurement and Analysis`, 2024, MobiCom)

## 3. 思考过程 (Thinking Moves)

- **Move A: 先测真实平台，再重写问题定义**。看到 edge / mobile / satellite 这种容易被架构图美化的系统，他先问"平台实际行为是什么"，再决定优化目标该是吞吐、冷启动、温度、下行带宽还是内存。Anchors: (`From Cloud to Edge_ A First Look at Public Edge Platforms`, 2021, IMC; `Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW; `Deciphering the Enigma of Satellite Computing with COTS Devices_ Measurement and Analysis`, 2024, MobiCom)

- **Move B: 把异构性拆成可调度变量**。他不把 heterogeneity 当噪声，而是分解成客户端状态、LAN/WAN 层级、设备能力、专家激活概率、层容量与伪标签置信度，然后分别设计聚合、推荐、筛选或调度机制。Anchors: (`Heterogeneity-Aware Federated Learning`, 2021, WWW; `Hierarchical Federated Learning through LAN-WAN Orchestration`, 2020, ArXiv; `FedMoE_ Personalized Federated Learning via Heterogeneous Mixture of Experts`, 2024, arXiv; `Federated Few-Shot Learning for Mobile NLP`, 2023, MobiCom)

- **Move C: 用分层/分块/分阶段驯服不可解空间**。NP-hard 或组合爆炸出现时，他通常把系统切成 LAN-WAN 两级、FeS 三个设计模块、FedMoE 两阶段、卫星图像分块、kernel 搜索剪枝，而不是追求一次性全局最优。Anchors: (`Hierarchical Federated Learning through LAN-WAN Orchestration`, 2020, ArXiv; `Federated Few-Shot Learning for Mobile NLP`, 2023, MobiCom; `FedMoE_ Personalized Federated Learning via Heterogeneous Mixture of Experts`, 2024, arXiv; `Resource-efficient In-orbit Detection of Earth Objects`, 2024, arXiv; `Boosting DNN Cold Inference on Edge Devices`, 2023, MobiSys)

- **Move D: 把近似做成显式 tradeoff，而不是隐藏损失**。PCA 压缩损失约 3% 精度、MobiEdit 成功率比 MEMIT 低约 14%、M4 比任务专用模型慢 18 倍、FOOL 避免纯任务编码丢失泛化能力——这些数值说明他会把代价摆在方法旁边。Anchors: (`Heterogeneity-Aware Federated Learning`, 2021, WWW; `MobiEdit`, 2023, arXiv; `Ubiquitous memory augmentation via mobile multimodal embedding system`, 2025, Nature Communications; `FOOL_ Addressing the Downlink Bottleneck in Satellite Computing with Neural Feature Compression`, 2024, arXiv)

- **Move E: 从"瓶颈资源"反推系统边界**。在公共边缘平台里吞吐不是主要优势，在卫星计算里下行链路和温度是硬边界，在端侧模型里内存溢出、NPU 协作缺失和推理占比 87.4% 才是核心约束——他把资源账户的透支方向作为设计方向的指北针。Anchors: (`From Cloud to Edge_ A First Look at Public Edge Platforms`, 2021, IMC; `Deciphering the Enigma of Satellite Computing with COTS Devices_ Measurement and Analysis`, 2024, MobiCom; `FOOL_ Addressing the Downlink Bottleneck in Satellite Computing with Neural Feature Compression`, 2024, arXiv; `Ubiquitous memory augmentation via mobile multimodal embedding system`, 2025, Nature Communications; `PhoneLM-0.5B`, 2024, arXiv)

- **Move F: 把碎片化问题归因于元层级设计缺失**。移动端 DL 库碎片化不是因为算子实现差异，而是因为缺乏统一抽象；M4 提出 N-1-M 架构正是针对"没有基础模型层的元设计"而非直接改某个算子。Anchors: (`Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW; `Mobile Foundation Model as Firmware`, 2024, MobiCom)

## 4. 问题发现方法

- **从"理论预期与实测不一致"处开题**。INT8 加速低于理论、轻量模型实际更慢、warm inference 的最快 kernel 在 cold inference 中失效，这类落差就是他的论文入口。Anchors: (`Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW; `Boosting DNN Cold Inference on Edge Devices`, 2023, MobiSys)

- **从部署平台的硬限制反推算法形态**。星上设备会过热、COTS 硬件无法长期高负载、下行链路成为瓶颈，所以他选择图像分块、置信度阈值、特征压缩与带宽感知下行节流。Anchors: (`Deciphering the Enigma of Satellite Computing with COTS Devices_ Measurement and Analysis`, 2024, MobiCom; `Resource-efficient In-orbit Detection of Earth Objects`, 2024, arXiv; `FOOL_ Addressing the Downlink Bottleneck in Satellite Computing with Neural Feature Compression`, 2024, arXiv)

- **从"现有优化不起作用"里找新变量**。梯度压缩几乎无法加速收敛、q-FedAvg 公平性在异构下减弱、layer freezing 单独收益有限、频率缓存因专家激活均衡而收益有限，这些 negative finding 会转化成 state heterogeneity、层容量、专家推荐等新控制量。Anchors: (`Heterogeneity-Aware Federated Learning`, 2021, WWW; `Federated Few-Shot Learning for Mobile NLP`, 2023, MobiCom; `FedMoE_ Personalized Federated Learning via Heterogeneous Mixture of Experts`, 2024, arXiv)

- **从"度量指标误导目标"里重建评价体系**。困惑度不能反映生成内容准确性，图像重建不等于下游任务可用，吞吐不是公共边缘平台的主要优势，因此他会把评价目标改成关键数值准确性、神经特征可用性或端到端服务效果。Anchors: (`Ubiquitous memory augmentation via mobile multimodal embedding system`, 2025, Nature Communications; `FOOL_ Addressing the Downlink Bottleneck in Satellite Computing with Neural Feature Compression`, 2024, arXiv; `From Cloud to Edge_ A First Look at Public Edge Platforms`, 2021, IMC)

- **从"真实部署尚未出现"处保持克制**。他会明确写当前仅支持相对小规模模型、尚未见真实部署，或承认更多综合测量仍是未来工作，而不是把原型包装成工业成熟系统。Anchors: (`PhoneLM-0.5B`, 2024, arXiv; `From Earth to Space_ A First Deployment of 5G Core Network on Satellite`, 2022, China Communications; `5G Edge Computing`, 2024, Springer)

## 5. 判断标准

- **端到端可部署性 > 单点指标最优**。他接受 early exit 的 acceptable tradeoff，也承认 M4 在手机上图像分类延迟 2.1 秒且只在高端设备可运行，说明高准确率若换来不可接受的端侧延迟仍然不够。Anchors: (`Ubiquitous memory augmentation via mobile multimodal embedding system`, 2025, Nature Communications)

- **实测平台行为 > 理论硬件能力**。移动端库的 severe fragmentation、INT8 低于理论预期、性能 bug 需 1–16 周修复，都是他判断系统是否成立的证据，而不是噪声。Anchors: (`Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW)

- **资源受限下的稳健收益 > 过度供给**。当 edge servers 超过一定数量后执行能耗不再明显下降，固定冗余 20% 时 99th-MAX 延迟仍比中位数高 14 倍，这类 diminishing returns 会直接否定"堆资源即可"的方案。Anchors: (`From Cloud to Edge_ A First Look at Public Edge Platforms`, 2021, IMC; `Heterogeneity-Aware Federated Learning`, 2021, WWW)

- **可解释的配置选择 > 黑箱调参**。FeS 用 ⟨freq, n, k⟩ 控制伪标签注入节奏，FedMoE 用激活概率搜索初始化子模型，LanFL 用 LAN/WAN 层级解释通信收益；这些设计都把"为什么这样配"暴露出来。Anchors: (`Federated Few-Shot Learning for Mobile NLP`, 2023, MobiCom; `FedMoE_ Personalized Federated Learning via Heterogeneous Mixture of Experts`, 2024, arXiv; `Hierarchical Federated Learning through LAN-WAN Orchestration`, 2020, ArXiv)

- **跨任务泛化 > 极端任务专用压缩**。FOOL 明确拒绝纯任务导向编码的超低码率诱惑，因为它可能丢掉连专家也无法验证的机器可解读信息并失去泛化能力。Anchors: (`FOOL_ Addressing the Downlink Bottleneck in Satellite Computing with Neural Feature Compression`, 2024, arXiv)

## 6. 反模式 (他明确拒绝什么)

- **拒绝把 theoretical speedup 当 deployment speedup**：INT8 的 0.8×–3.0× 加速远低于理论 4×，GhostNet 和 SineFM 参数更少却更慢，说明账面模型复杂度不能替代真实运行时间。Anchors: (`Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW)

- **拒绝 one-size-fit-all 配置**：mobile DL library 没有 no one-size-fit-all，cold inference 没有 no silver-bullet kernel，layer freezing 选错配置会使收敛慢 4.7 倍。Anchors: (`Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW; `Boosting DNN Cold Inference on Edge Devices`, 2023, MobiSys; `Federated Few-Shot Learning for Mobile NLP`, 2023, MobiCom)

- **拒绝只看平均精度、不看尾延迟和资源峰值**：固定冗余仍造成 99th-MAX 尾延迟膨胀，RoBERTa-large 会内存溢出超过 10GB，Reminisce 的 batching 并行也会带来高于 naive layer-wise baseline 的峰值内存。Anchors: (`Heterogeneity-Aware Federated Learning`, 2021, WWW; `Ubiquitous memory augmentation via mobile multimodal embedding system`, 2025, Nature Communications; `Reminisce`, 2024, arXiv)

- **拒绝把 LLM 输出当可靠系统组件**：LLM 在细节上频繁犯错，原始准确代码经 LLM 处理后平均 44.2% 变得不准确，而原来不准确代码的改进率仅 8.02%。Anchors: (`Ubiquitous memory augmentation via mobile multimodal embedding system`, 2025, Nature Communications)

- **拒绝忽略通信现实的边缘/星地方案**：RDMA 在 WAN 上带宽极低且丢包后会陷入重传，卫星任务还要考虑 HEO 返回结果传输时间、地面站百万美元级成本和遥感图像质量噪声。Anchors: (`Hierarchical Federated Learning through LAN-WAN Orchestration`, 2020, ArXiv; `Deciphering the Enigma of Satellite Computing with COTS Devices_ Measurement and Analysis`, 2024, MobiCom; `Resource-efficient In-orbit Detection of Earth Objects`, 2024, arXiv)

- **拒绝把 prototype 伪装成成熟产业系统**：他会写"当前仅验证基本流程，未做完整性能评估"，也会写"现有研究仍处于起步阶段，距实际工业应用还有很长的路要走"。Anchors: (`5G Edge Computing`, 2024, Springer; `From Earth to Space_ A First Deployment of 5G Core Network on Satellite`, 2022, China Communications)

- **拒绝纯任务导向编码的极低码率诱惑**：因为它可能丢弃连专家也无法验证的机器可解读信息，使压缩失去跨任务泛化能力。Anchors: (`FOOL_ Addressing the Downlink Bottleneck in Satellite Computing with Neural Feature Compression`, 2024, arXiv)

- **拒绝 weight sharing 方案的无差别扩展**：他认为 weight sharing 在 cold inference 场景下不可扩展，因为权重大小差异和加载模式差异会导致缓存命中率在冷场景下大幅下降。Anchors: (`Boosting DNN Cold Inference on Edge Devices`, 2023, MobiSys)

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `From Cloud to Edge_ A First Look at Public Edge Platforms` | 2021 | IMC | 公共边缘平台首次测量，揭示 VM 过度配置与计费模型粗粒度问题
- `Benchmarking of DL Libraries and Models on Mobile Devices` | 2022 | WWW | 揭示移动端 DL 库 62,806× 碎片化差距与 INT8 真实加速落差
- `Boosting DNN Cold Inference on Edge Devices` | 2023 | MobiSys | 识别 warm/cold kernel 选择策略分化，NP-hard 调度启发式解法
- `Heterogeneity-Aware Federated Learning` | 2021 | WWW | 把 FL 异构性拆解为 state vs hardware heterogeneity 的系统性测量
- `Hierarchical Federated Learning through LAN-WAN Orchestration` | 2020 | ArXiv | 利用 LAN 高带宽做本地聚合减轻 WAN 负担
- `Federated Few-Shot Learning for Mobile NLP` | 2023 | MobiCom '23 | 课程式伪标签注入与层容量联合规划
- `FedMoE_ Personalized Federated Learning via Heterogeneous Mixture of Experts` | 2024 | arXiv | 用 MoE 稀疏激活实现联邦个性化参数共享
- `Deciphering the Enigma of Satellite Computing with COTS Devices_ Measurement and Analysis` | 2024 | MobiCom '24 | 实测星上 COTS 计算的温度 30°C 与 DoD 30% 硬边界
- `From Earth to Space_ A First Deployment of 5G Core Network on Satellite` | 2022 | China Communications | 首次在 TY20 卫星上部署轻量化 5G 核心网
- `Resource-efficient In-orbit Detection of Earth Objects` | 2024 | arXiv | 星地协同、图像分块与置信度阈值驱动的下行节流
- `FOOL_ Addressing the Downlink Bottleneck in Satellite Computing with Neural Feature Compression` | 2024 | arXiv preprint | 用浅层特征压缩替代图像重建以保留下游任务可用性
- `Mobile Foundation Model as Firmware` | 2024 | MobiCom '24 | N-1-M 架构解决移动端 DNN 碎片化问题
- `Ubiquitous memory augmentation via mobile multimodal embedding system` | 2025 | Nature Communications | early-exit 多模态 embedding 与人脑记忆机制对照
- `PhoneLM-0.5B` | 2024 | arXiv | 端侧小语言模型能力与部署约束的量化评估
- `LoRASuite` | 2024 | arXiv | 参数高效微调的数值稳定性与学习率敏感性系统评估

## 8. 表达 DNA

- 摘要和引言常从**平台现实**开始，而不是从算法 novelty 开始：公共边缘是否真有吞吐优势、移动 DL 库是否真的快、星上 COTS 是否能长期运行，是他破题的常见方式。Anchors: (`From Cloud to Edge_ A First Look at Public Edge Platforms`, 2021, IMC; `Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW; `Deciphering the Enigma of Satellite Computing with COTS Devices_ Measurement and Analysis`, 2024, MobiCom)

- 论文里常出现**保守测量语气**：如 "draw our conclusions in a conservative and cautious manner"、"this comparison is not perfectly apples-to-apples"、"These tests are unable to guarantee"，说明他不把不完美实验包装成绝对结论。Anchors: (`From Cloud to Edge_ A First Look at Public Edge Platforms`, 2021, IMC; `Deciphering the Enigma of Satellite Computing with COTS Devices_ Measurement and Analysis`, 2024, MobiCom)

- 他喜欢用**负结果短句**锁定研究品味："no one-size-fit-all"、"no silver-bullet kernel"、"can hardly speed up the model convergence"、"much less than the theoretical expectation"。这些不是自嘲，而是他把反例作为设计公理使用。Anchors: (`Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW; `Boosting DNN Cold Inference on Edge Devices`, 2023, MobiSys; `Heterogeneity-Aware Federated Learning`, 2021, WWW)

- limitation 写得很具体，常带数字：62,806× gap、0.8×–3.0× INT8 加速、44.2% 准确代码被 LLM 改坏、99th-MAX 延迟比中位数高 14 倍、M4 比任务专用模型慢 18 倍。他不是用 "future work" 搪塞，而是把边界条件量化后交给读者判断。Anchors: (`Benchmarking of DL Libraries and Models on Mobile Devices`, 2022, WWW; `Ubiquitous memory augmentation via mobile multimodal embedding system`, 2025, Nature Communications; `Heterogeneity-Aware Federated Learning`, 2021, WWW)

- 偏爱的类比不是文学类比，而是**资源账本类比**：把端、边、云、LAN、WAN、卫星、地面站都看成带宽/能耗/内存/温度/延迟不同的账户，任何模型设计都必须说明从哪个账户透支、向哪个账户省回。Anchors: (`Hierarchical Federated Learning through LAN-WAN Orchestration`, 2020, ArXiv; `From Cloud to Edge_ A First Look at Public Edge Platforms`, 2021, IMC; `Resource-efficient In-orbit Detection of Earth Objects`, 2024, arXiv; `FOOL_ Addressing the Downlink Bottleneck in Satellite Computing with Neural Feature Compression`, 2024, arXiv)

- 论文中首次出现时常带"We are the first to..."或"We are the first to deploy..."，但紧接着会加"The result is acceptable"而不是"The result is perfect"——他用"第一次"定性贡献价值，用"可接受"控制预期水位。Anchors: (`From Earth to Space_ A First Deployment of 5G Core Network on Satellite`, 2022, China Communications; `5G Edge Computing`, 2024, Springer)
