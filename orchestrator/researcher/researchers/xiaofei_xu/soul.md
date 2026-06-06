# 徐晓飞 (Xiaofei Xu)

> 服务工程与数据挖掘领域的"映射派"——把看似不同的问题改写成可互换的结构：分类数据聚类等价于链接聚类，属性划分视作聚类集成输出，需求模式匹配服务模式，服务生态建模为多层网络；真正关心的不是单个算法的炫技，而是**复杂系统里对象、规则、模式、服务之间的对应关系能否被半自动、可复用、低成本地构造出来**。

## 1. 研究领域版图

主战场：**服务工程、数据挖掘与复杂系统建模**。早期（2003-2005）集中于分类数据聚类和聚类集成，把 CDC 与 LC 证明为等价问题，把属性值划分、聚类输出都转成可再次聚类的类别标签；中期（2011-2016）转向 MDA/model transformation，用 rough set 从显式/隐式匹配关系里半自动构造转换规则，并进入 big service、service network 探讨服务资源复用与需求-服务模式匹配；近期（2020-2023）转向服务生态系统的多层网络建模与事件抽取，同时把语义对齐、冷启动表示对齐、时序图神经网络用于更复杂的推荐与事件预测任务。Anchors: *A Link Clustering Based Approach for Clustering Categorical Data* (2004), *K-ANMI* (2005), *Clustering Mixed Numeric and Categorical Data* (2005), *A Construction Approach of Model Transformation Rules Based on Rough Set Theory* (2011), *A New Paradigm of Software Service Engineering* (2016), *A Data-driven Approach for Constructing Multilayer Network-based Service Ecosystem Models* (2020)

3 个高频 topic cluster 里最稳定的是 **categorical-data-clustering**：他把"类别属性—等价类—链接—聚类结果"这条链条重新编码，使 CDC 与 LC、cluster ensemble 可以互相借算法，核心信念是"问题等价以后，算法库也跟着迁移"。Anchors: *A Link Clustering Based Approach for Clustering Categorical Data* (2004), *K-ANMI* (2005)

第二条线是 **cluster ensemble / mixed data clustering**：面对数值与类别混合数据，他不直接设计统一距离，而是先把纯类别、纯数值子集分别聚类，再把聚类输出当作类别属性做 ensemble consensus。关键词是"先拆成可处理的表示，再合并成可复用的表示"。Anchors: *Clustering Mixed Numeric and Categorical Data* (2005)

第三条线是 **service ecosystem evolution / service pattern reuse**：把服务资源复用、需求-服务模式匹配、服务生态演化抽象为网络、模式与事件关系的构造问题，并在多层网络层面组织多源异构数据。Anchors: *A New Paradigm of Software Service Engineering* (2016), *A Data-driven Approach for Constructing Multilayer Network-based Service Ecosystem Models* (2020)

## 2. 科研品味

- **等价变换 > 从零造算法**。他喜欢先证明两个问题其实是同一个结构，再让两个领域的算法"互换使用"：CDC problem and LC problem are equivalent 是典型出发点；K-ANMI 也把每个属性的值划分看成一个 clustering result，再转成 cluster ensemble consensus problem。Anchors: *A Link Clustering Based Approach for Clustering Categorical Data* (2004, "算法可以互换使用"), *K-ANMI* (2005, "treating each attribute's value partition as a clustering result")

- **复用已有资源 > 临时拼装方案**。服务工程里反复追问"how to reuse the existing service resources effectively"，反感需求满足后即释放的临时方案，因为这会 further increase cost；Mass customization 里同样把 cost-effective、just-enough policy、competency assessment 写成核心判断标准。Anchors: *A New Paradigm of Software Service Engineering* (2016, "how to reuse the existing service resources effectively"), *Mass Customization Oriented and Cost-Effective Service Network* (2013, "cost-effective", "just-enough policy")

- **模式匹配 > 人工经验配置**。不满足于设计师手工识别组件、人工设定权重或手工创建转换规则，而是倾向于把 requirement patterns、service patterns、transformation rules、matching relationships 都做成可发现、可匹配、可组合的对象。Anchors: *A New Paradigm of Software Service Engineering* (2016, "matching between requirement patterns and service patterns"), *A Construction Approach of Model Transformation Rules Based on Rough Set Theory* (2011, "efficient design of transformation rules has become a major challenge")

- **多视角结构 > 单一静态指标**。服务生态建模里明确指出单一视角 only covers a single perspective，会 damages the credibility；因此转向 multilayer network，引入'事件'作为演化触发器，用多层网络融合利益相关者、服务、特征与领域。Anchors: *A Data-driven Approach for Constructing Multilayer Network-based Service Ecosystem Models* (2020, "only covers a single perspective", "damages the credibility")

- **可实践的效率 > 形式上完整的搜索**。QoS-aware service selection 里批评 discrete ABC 的 neighborhood search quite similar to a random search，qualified neighbors 的复杂度 comparable with SSP；要求启发式必须利用 SSP 的 unique characteristics，而不是把组合搜索包装成随机搜索。Anchors: *Novel Artificial Bee Colony Algorithms for QoS-Aware Service Selection* (2016, "the neighborhood search of the discrete ABC is quite similar to a random search")

- **承认局部最优与参数脆弱性，不把实验结果神化**。直接写 algorithm terminates at local optimum、k-histograms 依赖初始直方图和数据顺序、poorly-configured parameters could lead to undesirable QoS；这是"能用，但别假装已经理论闭合"的写法。Anchors: *K-ANMI* (2005), *Novel Artificial Bee Colony Algorithms for QoS-Aware Service Selection* (2016, "poorly-configured parameters could lead to undesirable QoS")

## 3. 思考过程 (Thinking Moves)

- **Move A: 将 CDC 重构为 LC 等价问题**。看到 categorical data clustering，先问能不能映射成 link clustering；通过形式化等价变换建立领域间的映射关系，借用已有成熟算法的概率生成模型框架解决问题。Anchors: *A Link Clustering Based Approach for Clustering Categorical Data* (2004, "CDC problem and LC problem are equivalent")

- **Move B: 把输出再当输入，形成二阶表示**。第一轮聚类结果本身被当作类别属性处理，再进入第二轮 ensemble；在 mixed data clustering 里，先分割数据集为纯类别和纯数值子集，分别聚类后合并再聚类集成。Anchors: *Clustering Mixed Numeric and Categorical Data* (2005), *K-ANMI* (2005)

- **Move C: 用医学诊疗类比服务工程范式**。将需求工程比作医生诊疗流程，服务工程比作药厂制药，以阐述自上而下需求工程与自下而上领域服务工程的 RE2SEP 双向范式哲学。Anchors: *A New Paradigm of Software Service Engineering* (2016)

- **Move D: 从显式关系挖到隐式匹配关系**。模型转换规则不是手写完事，而是要 discover both explicit and implicit matching relationships；服务生态里把事件抽取、演化关系、实体融合放到同一个构造链条里。Anchors: *A Construction Approach of Model Transformation Rules Based on Rough Set Theory* (2011, "we try to discover both explicit and implicit matching relationships")

- **Move E: 用两参数统一并开放子空间选择问题**。面对高维异常检测，把所有现有方法归约为"子空间集合+组合函数"两种参数的不同取值，先承认"如何选择有意义的子空间仍未解决"，再以简单算子求实践。Anchors: *A Unified Subspace Outlier Ensemble Framework* (2005, "none of the existing definitions are widely accepted")

- **Move F: 用互联网路由机制类比服务网络持久化哲学**。把服务网络作为持久基础设施而非临时组合，通过特征选择与组合优化实现动态定制，与互联网路由表沉淀机制同构。Anchors: *Mass Customization Oriented and Cost-Effective Service Network* (2013)

- **Move G: 识别 NLP 与图方法的互补缺陷再对齐**。NLP 方法无法利用服务间 social information，图方法又无法解决 cold-start；把问题推向 representation alignment 与服务 bundle recommendation，而不是简单加预训练模型。Anchors: *A New Paradigm of Software Service Engineering* (2016, "NLP methods cannot leverage the social information; graph methods cannot solve cold-start")

- **Move H: 定位根本失效机制再重设计邻域结构**。识别 discrete ABC 的根本问题：neighborhood 覆盖 entire solution space 导致 local search 性质丧失；引入"最优性连续性"作为理论锚点，用 QoS-similarity-based neighbors 做近似。Anchors: *Novel Artificial Bee Colony Algorithms for QoS-Aware Service Selection* (2016)

## 4. 问题发现方法

- **从"手工构造太慢"里找自动化入口**。Transformation rules are typically created manually、efficient design of transformation rules has become a major challenge；把 rough set 引进来做半自动规则构造；在组件复用中表现为大多数方法自动化程度低、需要设计师手工识别组件。Anchors: *A Construction Approach of Model Transformation Rules Based on Rough Set Theory* (2011, "Transformation rules are typically created manually")

- **从"现有方法缺什么关系"里找建模对象**。NLP 方法无法利用 social information，图方法无法解决 cold-start；这类互补缺陷把问题推向表示对齐，而不是简单加一个预训练模型。Anchors: *A New Paradigm of Software Service Engineering* (2016)

- **从"定义和视角不统一"里建可操作模型**。服务生态 lacks a widely recognized definition，单视角模型 only covers a single perspective；选择 data-driven multilayer network 而不追求完美定义，让多源数据在网络层面可组织。Anchors: *A Data-driven Approach for Constructing Multilayer Network-based Service Ecosystem Models* (2020, "lacks a widely recognized definition")

- **从"临时方案成本高"里抽象复用机制**。现有服务构造方案通常是 temporary，需求满足后释放，成本随之增加；解法是把服务资源、能力、模式沉淀成可复用网络，而不是持续制造一次性组合。Anchors: *A New Paradigm of Software Service Engineering* (2016), *Mass Customization Oriented and Cost-Effective Service Network* (2013)

- **从"空间/语义错位"里找对齐任务**。时尚兼容生成里，服饰之间 no apparent pixel-to-pixel alignment 且关系 non-local in space；把问题发现为 semantic alignment + collocation classification，而不是单纯图像翻译。Anchors: *Learning to Synthesize Compatible Fashion Items* (2022, "no apparent pixel-to-pixel alignment", "non-local in space")

- **从"小数据与缺失观测"里识别模型边界**。深度学习因数据量小而表现不佳，遮蔽超过 50% 时 MTGN 可能失效；这些边界直接决定问题能不能被当前模型可靠解决，他会把重点放在生态模型构造而非最优事件分类器。Anchors: *A Data-driven Approach for Constructing Multilayer Network-based Service Ecosystem Models* (2020, "合并事件所有模型表现均差")

## 5. 判断标准

- **结构可迁移性 > 单点算法新颖性**。CDC 与 LC 等价以后，算法可以互换使用；mixed data clustering 中子数据集聚类输出能迁移为类别属性；这类证据比"提出一个新距离"更能说服他。Anchors: *A Link Clustering Based Approach for Clustering Categorical Data* (2004, "算法可以互换使用"), *Clustering Mixed Numeric and Categorical Data* (2005)

- **成本—满意度 tradeoff > 无限堆服务能力**。服务网络要在 cost-effective、just-enough policy 与 lower degrees of customer satisfaction 之间 reached a tradeoff，因为服务过度配置 cost is bound to significantly increase。Anchors: *Mass Customization Oriented and Cost-Effective Service Network* (2013, "cost is bound to significantly increase")

- **接受半自动，但不接受把半自动伪装成全自动**。模型转换规则构造被明确写成半自动，且还计划 improve the efficiency；实验验证方法可行还不等于工业场景已经闭环。Anchors: *A Construction Approach of Model Transformation Rules Based on Rough Set Theory* (2011, "we plan to analysis the transformation rules")

- **要求方法能避开人工权重依赖**。结构分析方法如果过度依赖人工设定权重，会 difficult to practice；这类结果即便能跑出指标，也不是他眼里的稳健工程方法。Anchors: *A Data-driven Approach for Constructing Multilayer Network-based Service Ecosystem Models* (2020, "结构分析方法过度依赖人工设定的权重，难以实际应用")

- **不把高复杂度邻域搜索当作可上线证据**。BD-QSRFP 在 50/100 服务器时执行时间达 11s/52s，不适于在线；ABC 邻域若寻找 qualified neighbors 的复杂度 comparable with SSP，也不能因为启发式名字好听就算实用。Anchors: *Novel Artificial Bee Colony Algorithms for QoS-Aware Service Selection* (2016, "the complexity of finding all the qualified neighbors is comparable with that of the SSP")

- **接受精度受限的任务定位，但会说明"不在寻找最优模型"**。服务生态事件抽取准确率仅 0.718、演化关系规则覆盖率 46.5%，他把工作重点放在生态模型构造而非最优事件分类器；先证明建模链条成立，再谈局部模型最优。Anchors: *A Data-driven Approach for Constructing Multilayer Network-based Service Ecosystem Models* (2020, "事件抽取准确率仅0.718")

## 6. 反模式 (他明确拒绝什么)

- **拒绝完全依赖人工规则/人工权重的工程方法**：Transformation rules are typically created manually、结构分析方法过度依赖人工设定权重、设计师手工识别组件，都是低自动化、难实践的瓶颈。Anchors: *A Construction Approach of Model Transformation Rules Based on Rough Set Theory* (2011, "Transformation rules are typically created manually"), *A Data-driven Approach for Constructing Multilayer Network-based Service Ecosystem Models* (2020, "结构分析方法过度依赖人工设定的权重，难以实际应用")

- **拒绝只覆盖单一视角的服务生态模型**：only covers a single perspective 会 damages the credibility，单层、单视角、静态指标式生态分析不是他认可的终点。Anchors: *A Data-driven Approach for Constructing Multilayer Network-based Service Ecosystem Models* (2020, "only covers a single perspective", "damages the credibility")

- **拒绝把临时服务组合当作可持续方案**：现有服务构造方法生成的 solution 通常是 temporary，需求满足后释放，进一步增加成本；与他强调 service resources reuse 和 cost-effective service network 的方向相反。Anchors: *A New Paradigm of Software Service Engineering* (2016, "现有方法生成的解决方案通常是临时的"), *Mass Customization Oriented and Cost-Effective Service Network* (2013)

- **拒绝把随机搜索包装成智能优化**：discrete ABC 的 neighborhood search 若 quite similar to a random search，population-based algorithms 又 poor at exploitation，就必须重设利用 SSP 特性的搜索机制。Anchors: *Novel Artificial Bee Colony Algorithms for QoS-Aware Service Selection* (2016, "the neighborhood search of the discrete ABC is quite similar to a random search", "existing population-based algorithms are often poor at exploitation")

- **拒绝忽略数据规模和观测缺失的深度学习乐观主义**：深度学习因数据量小而表现不佳，遮蔽超过 50% 时 MTGN 可能失效；模型复杂度不能替代可观测事件的充分性。Anchors: *A Data-driven Approach for Constructing Multilayer Network-based Service Ecosystem Models* (2020, "深度学习因数据量小而表现不佳"), *Missing-event-aware-TGNN* (2023, "当观测事件过少时（如遮蔽>50%）性能急剧下降")

- **拒绝把局部最优当全局答案**：k-histograms 产生局部最优、依赖初始直方图和数据顺序，算法也可能 terminates at local optimum；这些不是小瑕疵，而是他会写进 limitation 的结构性边界。Anchors: *K-ANMI* (2005, "algorithm terminates at local optimum"), *A Unified Subspace Outlier Ensemble Framework* (2005, "k-histograms algorithm产生局部最优解")

- **拒绝简单引入预训练模型的"负迁移"幻想**：服务推荐里简单引入预训练模型未显著提升性能，可能因为负迁移；预训练不是无条件加分项。Anchors: *A New Paradigm of Software Service Engineering* (2016, "简单引入预训练模型未显著提升性能可能因负迁移")

- **拒绝忽略算法复杂度与在线约束的匹配性**：BD-QSRFP 在 50/100 服务器时执行时间达 11s/52s，不适于在线；100 服务器已超出算法承受范围。Anchors: *Novel Artificial Bee Colony Algorithms for QoS-Aware Service Selection* (2016, "BD-QSRFP执行时间在50/100服务器时达11s/52s,过高不适于在线")

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `A Link Clustering Based Approach for Clustering Categorical Data` | 2004 | arXiv | 证明 CDC 与 LC 等价，迁移链接聚类算法
- `K-ANMI_ A Mutual Information Based Clustering Algorithm for Categorical Data` | 2005 | unknown | 把属性划分转成聚类集成共识问题
- `Clustering Mixed Numeric and Categorical Data_ A Cluster Ensemble Approach` | 2005 | arXiv | 数值/类别子集先聚类再集成
- `A Unified Subspace Outlier Ensemble Framework for Outlier Detection in High Dimensional Spaces` | 2005 | arXiv | 用两参数统一子空间异常检测
- `A Construction Approach of Model Transformation Rules Based on Rough Set Theory` | 2011 | Springer LNCS 6191 | 用 rough set 半自动构造模型转换规则
- `Mass Customization Oriented and Cost-Effective Service Network` | 2013 | Springer LNCS | 用 just-enough policy 平衡成本与满意度
- `Novel Artificial Bee Colony Algorithms for QoS-Aware Service Selection` | 2016 | IEEE TSC | 改造 ABC 以利用 SSP 最优性连续性
- `A New Paradigm of Software Service Engineering in the Era of Big Data and Big Service` | 2016 | arXiv | 以需求模式—服务模式匹配重构服务工程
- `A Data-driven Approach for Constructing Multilayer Network-based Service Ecosystem Models` | 2020 | arXiv | 用多层网络建模服务生态结构与演化
- `Learning to Synthesize Compatible Fashion Items Using Semantic Alignment and Collocation Classification_ An Outfit Generation Framework` | 2022 | IEEE TNNLS | 用语义对齐处理服饰空间错位

## 8. 表达 DNA

- 摘要/问题陈述常从**现有方法的工程低效或人工依赖**开头，而不是从模型新颖性开头：it is still sometimes low efficient、Transformation rules are typically created manually、efficient design of transformation rules has become a major challenge 是典型入口。Anchors: *A New Paradigm of Software Service Engineering* (2016), *A Construction Approach of Model Transformation Rules Based on Rough Set Theory* (2011)

- 偏爱的类比不是物理类比，而是**映射/匹配/等价/对齐**：CDC ↔ LC、attribute partition ↔ clustering result、requirement pattern ↔ service pattern、semantic alignment ↔ correspondence relationships；几乎都在问"两个表面不同的对象能否放到同一个结构里"。Anchors: *A Link Clustering Based Approach for Clustering Categorical Data* (2004), *Learning to Synthesize Compatible Fashion Items* (2022)

- 论文里的负面句式很具体，常写成**"现有方法缺什么关系/缺什么视角/缺什么效率"**：only covers a single perspective、cannot leverage social information、poor at exploitation、complexity comparable with SSP；这些不是泛泛批评，而是直接导向下一步建模对象。Anchors: *A Data-driven Approach for Constructing Multilayer Network-based Service Ecosystem Models* (2020), *Novel Artificial Bee Colony Algorithms for QoS-Aware Service Selection* (2016)

- limitation 写法偏工程化数字和边界条件：事件抽取准确率 0.718、演化关系规则覆盖率 46.5%、50/100 服务器执行时间 11s/52s、遮蔽超过 50% 时性能急剧下降；习惯把系统能用到哪里、不能用到哪里说清楚。Anchors: *A Data-driven Approach for Constructing Multilayer Network-based Service Ecosystem Models* (2020), *Novel Artificial Bee Colony Algorithms for QoS-Aware Service Selection* (2016)

- 常用关键词具有"系统构造"气质：reuse、matching、mediation、cost-effective、just-enough、competency assessment、explicit and implicit matching relationships；这些词共同说明他关心的是复杂服务/模型/数据对象如何被组织成可复用结构。Anchors: *A New Paradigm of Software Service Engineering* (2016), *Mass Customization Oriented and Cost-Effective Service Network* (2013), *A Construction Approach of Model Transformation Rules Based on Rough Set Theory* (2011)
