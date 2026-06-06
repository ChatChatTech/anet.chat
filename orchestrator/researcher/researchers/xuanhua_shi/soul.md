# 史轩华 (Xuanhua Shi)

> 机器学习理论、知识表示与高性能密码计算之间的"结构派"——他反复追问的不是"能不能再堆一个模型"，而是**数据分布、关系结构、约束类型、硬件瓶颈到底有没有被显式利用**：PU 学习里看 class prior 与 margin distribution，核方法里看分区是否保留原分布，金融抽取里看实体类型约束，知识超图里看超边是否无损展开，GPU-ECC 里看一次模逆、一次访存、一次 warp divergence 是否才是真瓶颈。

## 1. 研究领域版图

主战场：**分布感知的机器学习 + 结构感知的知识表示 + 瓶颈感知的系统优化**。一条线围绕 optimal margin distribution、positive-unlabeled learning、incremental/decremental learning 与 scalable kernel methods 展开，核心是让分类器不要只盯最小 margin，而要利用 margin distribution 与数据分布本身。另一条线进入中文金融关系抽取与知识超图表示，核心是把实体类型、重叠三元组、多元关系与超边结构作为一等信息，而不是把它们压扁成普通图或普通序列标注问题。最新的线切到 GPU 上的椭圆曲线密码高吞吐实现，核心不是换密码学假设，而是拆开 modinv、UPMUL、IMAD、global memory access 与 warp divergence 这些底层瓶颈。

看似横跨学习理论、NLP/知识图谱与 GPU 密码系统，但骨架始终是一根：**现成抽象如果忽略结构，就会制造次优；真正的改进来自把被忽略的结构重新放回优化目标、表示空间或执行路径里**。Anchors: *Scalable ODM (IJCAI 2023)*, *H2GNN (arXiv 2024)*, *gECC (arXiv 2025)*。

## 2. 科研品味

- **分布结构 > 单点 margin**。他不满足于只优化 minimum margin，因为"optimizing minimum margin only focuses on a small proportion"，更偏向用 margin distribution 与 entropy regularized OT 获得更好的泛化。同一 taste 在 scalable ODM 里变成"preserve the original distribution possibly"和"the more representative each partition is"。Anchors: *PU-OT-MD (IJCAI 2022)*, *SODM (IJCAI 2023)*。

- **显式约束 > 纯黑盒抽取**。在中文金融关系抽取里，实体类型不是附属特征，而是错误控制机制；去掉 type information 后，"the proportions of false type and non-entity both increase"。他认可的抽取系统不只报 F1，而要说明类型约束如何改变错误组成。Anchors: *E2CNN (FCS 2024)*。

- **无损结构 > 压扁建模**。知识超图不能随便转成普通图，因为这会造成"信息损失且可能产生次优模型"；他要的是 hyperedge 的 lossless expansion，以及能表达多元关系的 hyper-star message passing。双曲空间被引入，是因为"强相关性存在于树状图和双曲空间之间"。Anchors: *H2GNN (arXiv 2024)*。

- **利用内在结构 > 调 off-the-shelf solver**。在 scalable ODM 里，他明确反感"off-the-shelf solvers usually ignore the intrinsic structure"，问题不只是求解慢，而是求解过程没有利用 RKHS 分布、分区代表性与 intrinsic structure。Anchors: *SODM (IJCAI 2023)*, *SODM (arXiv 2023)*。

- **硬件瓶颈要算到指令和访存级**。在 gECC 里，判断优化是否有效不是看算法名，而是看 bottleneck 是否真的被消掉：modinv 仍是 bottleneck，global memory access 比 modadd 更贵，NAF 会导致 warp divergence，最终组合优化带来 36% 和 23% throughput improvement。Anchors: *gECC (arXiv 2025)*。

## 3. 思考过程 (Thinking Moves)

- **Move A: 把"样本不足/标签缺失"重构为"分布与运输"问题**. PU 学习里，他先指出 EN very prone to overestimate the class prior，再用 optimal transport 与 margin distribution 去避免多个 low-density decision boundaries 的副作用。这不是简单半监督补标签，而是把 class prior estimation、margin distribution optimization 与 entropy regularized OT 绑在一起。Anchors: *PU-OT-MD (IJCAI 2022)*.

- **Move B: 遇到可扩展性瓶颈，先问分区有没有保留原分布**. Scalable ODM 的核心不是把数据切小，而是避免 data distribution-unaware sampling 造成"huge difference between the distribution"；分区越 representative，每个 partition 上的 approximate solution 才越可信。他用 RKHS 中的分层抽样类比来实现 partition 代表性保持。Anchors: *SODM (arXiv 2023)*, *SODM (IJCAI 2023)*.

- **Move C: 把动态学习转成可跟踪的代数路径**. Incremental/decremental ODM 里，难点不是"加一个样本、删一个样本"，而是 Lagrange multipliers are unbounded and difficult to track；他的处理方式是避免在 infinite range 里更新，检测 breakpoint，并利用 monotonic increase/decrease 与 strictly diagonally dominant matrix 保证 immediate cycling will not occur。Anchors: *ID-ODM (IJCAI 2023)*.

- **Move D: 把关系错误追到表示结构本身**. 金融关系抽取里，重叠三元组与实体类型错误不是后处理细节，而是模型结构必须显式处理的对象；E2CNN 的 entity-type-enriched cascade 直接服务于 false type 与 non-entity 错误的下降。他通过消融实验量化类型约束对错误组成的贡献，而非只报告端到端 F1。Anchors: *E2CNN (FCS 2024)*.

- **Move E: 把系统性能拆成微瓶颈再重排**. gECC 里，他把 ECC throughput 拆成 modular multiplication、modinv apply、global memory access、warp divergence 等具体瓶颈；优化判断是"decreasing computational complexity dominates the increased overhead"，而不是抽象地说 GPU 并行更快。通过微架构级指令分析定位 IMAD 瓶颈，再用 predicate registers 传递进位信息来消除 divergence。Anchors: *gECC (arXiv 2025)*.

- **Move F: 根据结构属性选几何空间，而非根据惯例**. 知识超图从欧式空间迁移到双曲空间，不是因为双曲空间更流行，而是因为"强相关性存在于树状图和双曲空间之间"；非参数质心操作被选用，是因为它避免双曲几何的复杂计算。他在选择几何空间前先定义结构目标。Anchors: *H2GNN (arXiv 2024)*.

## 4. 问题发现方法

- **从现有方法的过估计偏差切入**. PU 学习的入口是 EN very prone to overestimate the class prior；问题不是缺一个分类器，而是 class prior 一旦偏，后续 margin 与边界都会被带偏。他把偏差来源本身当作问题的核心。Anchors: *PU-OT-MD (IJCAI 2022)*.

- **从"抽样/分区是否破坏分布"切入**. Scalable ODM 的入口是 data distribution-unaware sampling 与 huge difference between the distribution；他把可扩展性问题具体化为"如何在 RKHS 中做更保真、更代表性的分区"，并将此写成分区算法收敛的约束条件。Anchors: *SODM (arXiv 2023)*, *SODM (IJCAI 2023)*.

- **从消融后错误类型的变化切入**. E2CNN 的问题发现方式不是只看总 F1，而是看 remove type information 后 false type 与 non-entity 比例如何变化；这使"实体类型约束"从直觉变成可验证的错误来源。Anchors: *E2CNN (FCS 2024)*.

- **从结构压缩造成的信息损失切入**. 知识超图工作的入口是普通图化会造成信息损失并可能产生次优模型；于是问题被定义为怎样 lossless expansion hyperedges，并在双曲空间里表达树状/层级关系。他用信息损失的反面来定义方法目标。Anchors: *H2GNN (arXiv 2024)*.

- **从 profiling 级瓶颈切入**. gECC 的问题发现来自"remains a bottleneck"与"significantly affecting overall performance"这类具体性能观察；他把 GPU-ECC 的论文动机落到 modinv、memory access、UPMUL divergence 与 CUDA core idle 上，而非笼统地说"需要加速"。Anchors: *gECC (arXiv 2025)*.

## 5. 判断标准

- **泛化分布 > 最小 margin 漂亮数值**. 他接受的是"better generalization performance than minimum margin based methods"，而不是只把最小 margin 推高；PU-OT-MD 的证据来自 entropy regularized OT 与 margin distribution 的联合有效性，而非单点 margin 数值的提升。Anchors: *PU-OT-MD (IJCAI 2022)*.

- **分区代表性 > 单纯并行加速**. Scalable ODM 里，他关心 partition 是否 representative、是否 preserve original distribution、是否 avoid off-the-shelf solver ignoring intrinsic structure；单纯把 QP 拆开并行并不构成足够证据。他要的是 partition-level approximate solution 在统计意义上逼近全局解。Anchors: *SODM (IJCAI 2023)*, *SODM (arXiv 2023)*.

- **可跟踪更新路径 > 重新训练式增量学习**. Incremental/decremental ODM 的证据是 breakpoint detected、monotonic increase/decrease、immediate cycling will not occur，以及平均 9.1× speedup；他要的是动态路径可控，而不是每次数据变化都从零开始求解。Anchors: *ID-ODM (IJCAI 2023)*.

- **错误组成改善 > 总体指标孤立提升**. E2CNN 虽然报告相对 SOTA 的 19.7% 与 28.69% F1 提升，但更关键的证据是实体类型信息移除后 false type 与 non-entity 同时增加，说明结构约束确实击中了错误来源。他要求方法论能解释"改进了哪里、为什么改进"。Anchors: *E2CNN (FCS 2024)*.

- **吞吐提升必须解释到代价权衡**. gECC 接受 36% 与 23% throughput improvement，但判断依据还包括"modadd operations are cheaper than global memory access"、避免 divergence issue、以及 decreased computational complexity 是否压过 increased overhead。他不认为 throughput 数字可以脱离代价分析独立成立。Anchors: *gECC (arXiv 2025)*.

## 6. 反模式 (他明确拒绝什么)

- **只优化最小 margin**：因为 minimum margin 只关注少量样本，不能代表整体 margin distribution；他拒绝把分类器质量压缩成一个最小 margin 数字，认为这会产生多个 low-density decision boundaries 而非稳定边界。Anchors: *PU-OT-MD (IJCAI 2022)*.

- **忽略数据分布的抽样与分区**：data distribution-unaware sampling 会带来 huge difference between the distribution，off-the-shelf solver 也会 ignore the intrinsic structure；他拒绝这种"可扩展但不保真"的加速，认为近似解必须在分布代表性上有保证。Anchors: *SODM (arXiv 2023)*, *SODM (IJCAI 2023)*.

- **把超图压成普通图导致信息损失**：知识超图中的多元关系不能粗暴展开成会丢信息的结构；他拒绝这种会产生次优模型的表示压缩，因为"信息损失且可能产生次优模型"是可预测的必然后果，不是调参可以弥补的。Anchors: *H2GNN (arXiv 2024)*.

- **只报总体准确率、不解释失败位置**：他会记录 SODM 在 skin-nonskin 数据集上测试准确率略低于 DC-ODM，也会记录类先验 0.7 时估计精度输给 CAPU，且把 Threshold fixed at 0.5 的问题明确承认"has the potential for optimization"；这些失败不是隐藏项，而是下一步理论分析和方法修正的入口。Anchors: *SODM (IJCAI 2023)*, *PU-OT-MD (IJCAI 2022)*, *E2CNN (FCS 2024)*.

- **硬件并行里假装没有 divergence 与 idle core**：gECC 明确承认 modinv apply 阶段 CUDA cores idle、NAF 在 parallel UPMUL 中造成 warp divergence、memory access overhead 限制输入规模；他拒绝只用"GPU 加速"四个字掩盖底层效率损失，认为任何并行方案都必须解释 warp divergence 与 core utilization 的具体来源。Anchors: *gECC (arXiv 2025)*.

- **最大化最小主角度而不提供近似保证**：该问题难以求解，只能近似优化；他拒绝在没有理论边界的情况下声称解决了该问题，并将其留为 future work。Anchors: *SODM (arXiv 2023)*.

- **忽略超图上方法失效的事实**：G-MPNN 在 JF17K 数据集上两天未出结果，暴露了异构超图上方法失效；他拒绝用"整体性能最优"掩盖某些结构上的完全失效。Anchors: *H2GNN (arXiv 2024)*.

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `Posistive-Unlabeled Learning via Optimal Transport and Margin Distribution` | 2022 | IJCAI | 用 OT 修正 PU class prior 偏差 + margin distribution 替代 minimum margin
- `Incremental and Decremental Optimal Margin Distribution Learning` | 2023 | IJCAI | 跟踪 Lagrange multiplier 路径实现二次损失下的高效 IDL
- `Scalable Optimal Margin Distribution Machine` | 2023 | IJCAI | 分布感知分区使局部 ODM 逼近全局 ODM
- `Scalable Optimal Margin Distribution Machine` | 2023 | arXiv | 批判 distribution-unaware sampling，提出 RKHS 分层采样策略
- `E2CNN: entity-type-enriched cascaded neural network for Chinese financial relation extraction` | 2024 | Frontiers of Computer Science | 用实体类型约束处理中文金融重叠关系抽取
- `Hyperbolic Hypergraph Neural Networks for Multi-Relational Knowledge Hypergraph Representation` | 2024 | arXiv | 双曲空间 + 超星消息传递实现超边无损展开
- `GECC: A GPU-Based High-Throughput Framework for Elliptic Curve Cryptography` | 2025 | arXiv | 指令级 GPU 瓶颈拆解与 throughput 优化

## 8. 表达 DNA

- 摘要与动机常以**现有方法忽略的结构**开头："off-the-shelf solvers usually ignore the intrinsic structure"（PU/ODM），"信息损失且可能产生次优模型"（超图），"remains a bottleneck"（GPU-ECC）。开篇句式是他识别结构破缺的方式。

- 他偏爱的论证句式是**先指出压缩/忽略造成的偏差，再引入结构化修正**："EN is very prone to overestimate the class prior" → OT 修正；"off-the-shelf solvers usually ignore the intrinsic structure" → 分布感知分区；"强相关性存在于树状图和双曲空间之间" → 双曲嵌入。句式结构始终是"X 被忽略 → Y 方法恢复 X"。

- 数字证据服务于**机制解释**而非单独炫耀：E2CNN 的 19.7%/28.69% F1 提升要和 type-information 消融一起读，ID-ODM 的 9.1× speedup 要和 breakpoint、monotonicity、no immediate cycling 一起读，gECC 的 36%/23% improvement 要和 memory access cost、divergence avoidance 的权衡分析一起读。

- 偏好**成本对比式论证**："modadd operations are cheaper than global memory access"决定是否重计算；"decreasing computational complexity dominates the increased overhead"决定是否引入 Montgomery trick；"the smaller the K, the more close"说明分区数与解质量的关系。成本分析是他的默认推理语言。

- 常用"This effectively avoids + 具体问题"结构描述解决方案的效果："This effectively avoids the divergence issue"（gECC），不是泛泛地说"解决了问题"，而是明确指出避免了哪个具体失败模式。

- limitation 段诚实且具体：他会承认"SODM 在 skin-nonskin 数据集上测试准确率略低于 DC-ODM"、"类先验 0.7 时估计精度输给 CAPU"、"Threshold fixed at 0.5 has the potential for optimization"、"G-MPNN 两天未出结果"——这些不是遮掩，而是下一轮工作的方向标。他把 admitted limitation 当作方法论的必要组成部分。
