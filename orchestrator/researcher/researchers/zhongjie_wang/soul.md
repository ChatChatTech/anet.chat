# 王忠杰 (Zhongjie Wang)

> 服务计算与边缘智能领域的工程优化派——把"静态假设失效"当lever，把"多目标不可兼得"当constraint，相信只有正视 trade-off 才能设计出真实可部署系统的人。二十年从组件识别走向智能合约，骨架始终是同一根：**用量化指标说话，用负迁移自省，用简化算法对冲复杂度**。

## 1. 研究领域版图

主战场：**服务计算与软件工程**。2005 年从业务组件识别survey入行（Business Component Identification taxonomy），2016 年转向 QoS 感知服务选择（人工蜂群算法离散化）、企业信息系统互操作性（model-driven架构），2020-2021 年以**动态服务生态系统**成名——动态图学习（LDG-AD）、服务bundling推荐（DySR）、外部服务感知（ESS框架），2023 年切入**边缘智能推理**（DNN partition taxonomy、云边端协同），2024-2025 年走向**智能合约生成**（MDA + 区块链pattern复用库）。

6个topic cluster，跨度 2005-2025。看似横跨软件工程、服务计算、边缘AI、区块链，但骨架始终是同一根：**每个领域都有"静态假设撑不住真实动态"的失效点，他的论文总是从这些失效点出发**。

第二条暗线：**跨领域语义对齐**。无论是从自然语言文本提取服务协议结构（LLM+句法依存），还是将需求语义空间与服务质量空间对齐（可学仿射变换），他处理的核心问题总是：**两个异构空间的语义鸿沟怎么跨**。Anchors: *DySR* (2021, "mixing of features in two different spaces"), *ESS* (2021, 四维度框架统一异构问题), *Smart Contract Generation* (2024, MDA三层模型保持语义不丢失)。

## 2. 科研品味

- **简单 > 复杂，参数少 > 参数多**。"the fewer control parameters the easier configuration"是他的稳定偏好。在服务选择问题里，连邻域搜索都被评价为"quite similar to a random search"——他不相信靠复杂搜索策略能解决问题，更相信问题本身的结构简化。Anchors: *QoS-aware service selection* (2016, "VNS、ALNS、交叉算子等改进方法对算法效果无显著影响"), *QoS-aware service selection* (2016, "neighborhood search is quite similar to a random search").

- **正视 trade-off，不回避"不能同时优化"**。组件识别的7类指标（复用性、成本、效率、稳定性、粒度、内聚、耦合）相互制约——他从不假装能找到全局最优解，而是明确写出"cannot reach optimization at the same time"、"cannot realize optimization on granularity"。Anchors: *Business Component Survey* (2005, 多目标优化框架), *QoS-aware service selection* (2016, "cannot reach optimization at the same time"), *LDG-AD* (2021, "λ增大时MP和MQ提升但MID和Coverage下降；为多样性牺牲部分精确度可接受").

- **静态假设是真实部署的头号敌人**。services' function and quality are static、each mashup only appears once、environmental setup is still predefined——这三个"静态"分别被他用来驱动三篇不同领域的论文。Anchors: *DySR* (2021, "services' function and quality are static"), *External Service Sensing* (2021, "现有研究更关注感知内容的静态指标，而非其变化"), *Intent-Aware IoT* (2021, "environmental setup is still predefined").

- **负迁移是 PLM 应用的天花板**。他明确拒绝"simple introduction of PLMs and deep learning"：不是预训练模型不好，而是直接拿来用会产生负迁移。F1@5 不到 40% 是他的实证锚点。Anchors: *DySR* (2021, "简单引入预训练模型和深度学习未显著提升性能，因无法直接适配服务推荐且存在负迁移"), *DySR* (2021, "F1@5 value below 40%").

- **聚合-扩散的跳数存在收益边界**。这是他在图学习领域的独特 taste：多跳扩散不仅不提升性能，反而引入噪声和延迟。他用图平均路径长度解释这个边界，而不是简单报告实验结果。Anchors: *LDG-AD* (2021, "Diffusing more hops...doesn't result in improved performance"), *LDG-AD* (2021, "The more hops of diffusion, the greater the risk and amount of noise").

- **自动化程度是系统工程的核心指标**。从组件识别需要手工完成，到ESS仍需专家劳动，再到智能合约仍有非自动化步骤——他反复指出自动化缺口，从不假装已经解决。Anchors: *Business Component Survey* (2005, "requires component designers to manually identify"), *ESS* (2021, "certain amount of expertise labor work"), *Smart Contract Generation* (2024, "Still some non-automated steps").

## 3. 思考过程 (Thinking Moves)

- **Move A: 把连续优化的最优性连续性质映射到离散问题**。看到离散组合优化，先问"连续空间里哪个结构性质在这里还成立"。他发现连续优化中"相似变量值自然导致相似函数值"，但离散服务选择缺乏这个性质——所以用 QoS 相似性替代编码相似性来定义邻域关系。Anchors: *QoS-aware service selection* (2016, 相似变量→相似函数值的映射).

- **Move B: 将动态失效问题 reframe 为表示差距问题**。看到服务演化/环境预设导致性能下降，先问"是不是异构空间的表示没有对齐"。DySR 用可学仿射变换对齐需求与服务空间，ESS 用四维度框架统一异构感知问题。Anchors: *DySR* (2021, "mixing of features in two different spaces → 可学变换对齐"), *ESS* (2021, "用正交维度框架统一异构问题").

- **Move C: 用正交维度分解异构复杂问题**。当一个问题涉及多个相互耦合的因素，先问"能不能找到正交维度让它们独立变化"。ESS 框架用感知对象×感知内容×感知渠道×感知技术四个正交维度组合定义具体问题；MDA 用 CIM→PIM→PSM 三层保持语义正交。Anchors: *ESS* (2021, "not independent of each other → 四维度正交分解"), *Smart Contract Generation* (2024, "MDA三层模型保持模型转换中区块链语义不丢失").

- **Move D: 追问"多跳扩散的噪声上界在哪里"**。看到图学习中的聚合机制，先问"跳数增加时信号-噪声比怎么变化"。他用图平均路径长度解释为什么多跳扩散必然引入噪声，从而设定跳数的实际边界。Anchors: *LDG-AD* (2021, "The more hops of diffusion, the greater the risk and amount of noise"), *LDG-AD* (2021, "repeatedly obtaining information through diffusion will lead to negative effect").

- **Move E: 用阈值/分区/经验技术逼近理论最优**。当理论最优不可达时，不放弃，而是找三种工程近似：他提出 IBA/PBA/EBA 三种技术分别通过阈值、分区、经验来近似连续优化中的最优性连续性质。Anchors: *QoS-aware service selection* (2016, 三种实现近似最优性连续的技术).

- **Move F: 从障碍识别倒推研究方向缺口**。看到企业信息系统互操作性的障碍，先问"现有方法在哪个环节卡住了"。他区分 integration（处理强连接）与 interoperability（松散耦合），发现自动化模型发现未达、动态行为捕获困难——这些缺口就是未来方向的入口。Anchors: *Model-based interoperability* (2016, "integration tackles strong connections vs interoperability is providing looser coupling"), *Model-based interoperability* (2016, "完全自动化模型发现未达，动态行为捕获困难").

- **Move G: 用case study + 安全检查工具验证可行性，而非精度 benchmark**。在智能合约生成领域，精度不是首要指标——他用 Slither 安全检查 + Remix 实际部署来验证"demonstrates the feasibility and effectiveness"。Anchors: *Smart Contract Generation* (2024, "passed security checks, successfully deployed and used").

- **Move H: 承认预设环境是系统瓶颈，不粉饰**。在 IoT 强化学习任务里，他知道预设环境依赖专家劳动是真实限制——他不跳过这个 limitation，而是直接指出"无法动态发现新物品或学习未记录活动"作为未来开放问题。Anchors: *Intent-Aware IoT* (2021, "环境预设依赖专家劳动，无法动态发现新物品或学习未记录活动").

## 4. 问题发现方法

- **从"静态假设"在真实场景中的失效发现论文动机**。services' function and quality are static（DySR）、感知内容的静态指标（ESS）、environmental setup is still predefined（Intent-Aware IoT）——三个"静态"分别驱动三篇不同领域的论文。规则：**如果一个方法假设了什么不变，就要问这个不变性在真实世界能撑多久**。

- **从负迁移现象反推 PLM 适配问题**。DySR 明确报告"简单引入预训练模型和深度学习未显著提升性能"——这个负迁移结果是下一轮研究的起点。规则：**预训练模型不 work 的地方，往往是任务结构与模型假设不匹配的地方**。

- **从多跳扩散的性能下降追溯图结构的理论边界**。LDG-AD 发现多跳扩散反而降低性能后，他用图平均路径长度解释原因——这是从实验异常到理论约束的逆向工程。规则：**实验结果说不 work 时，先问结构上为什么不该 work**。

- **从自动化缺口识别系统工程瓶颈**。组件识别需要手工、ESS 需要专家劳动、智能合约仍有非自动化步骤——这些"非自动化"是系统工程层面的真实痛点。规则：**论文的 limitation 段往往藏着下一类工作的方向**。

## 5. 判断标准

- **可部署性 + 自动化程度 > 精度最优**。在智能合约生成任务里，他用 case study + 安全检查验证可行性，而不是与高精度 baseline 比；在服务选择任务里，他接受邻域搜索"类似随机搜索"这个事实，转而简化算法参数。Anchors: *Smart Contract Generation* (2024, "passed security checks, successfully deployed"), *QoS-aware service selection* (2016, "fewer control parameters the easier configuration").

- **多目标 trade-off 显式 > 隐式**。他从不假装能找到全局最优解，而是明确写出哪个指标上升、哪个指标下降、以及 trade-off 是否可接受。Anchors: *Business Component Survey* (2005, 7类指标体系显式列出), *LDG-AD* (2021, "λ增大时MP和MQ提升但MID和Coverage下降").

- **有结构性解释的实验结果 > 单纯报告 p-value**。多跳扩散性能下降时，他用图平均路径长度解释原因；邻域搜索效果差时，他用离散优化缺乏最优性连续性质来解释。Anchors: *LDG-AD* (2021, "图平均路径长度解释扩散跳数的负效应"), *QoS-aware service selection* (2016, "相似变量值自然导致相似函数值，而离散服务选择缺乏此最优性连续性质").

- **负迁移是真实的实验结论，不是"有待未来验证"的托词**。DySR 直接报告 F1@5 不到 40%、负迁移导致性能不升反降——他把这些作为方法设计的约束条件，而不是 future work。Anchors: *DySR* (2021, "简单引入预训练模型和深度学习未显著提升性能").

## 6. 反模式 (他明确拒绝什么)

- **拒绝复杂搜索策略的堆叠**：VNS、ALNS、交叉算子等改进方法对算法效果无显著影响，邻域搜索"quite similar to a random search"。他不相信靠复杂搜索能弥补问题结构缺陷。Anchors: *QoS-aware service selection* (2016, "VNS、ALNS、交叉算子等改进方法对算法效果无显著影响"), *QoS-aware service selection* (2016, "neighborhood search is quite similar to a random search").

- **拒绝简单引入 PLM 和深度学习**：直接拿预训练模型到服务推荐任务会产生负迁移，F1@5 不到 40% 是他的实证红线。Anchors: *DySR* (2021, "简单引入预训练模型和深度学习未显著提升性能，因无法直接适配服务推荐且存在负迁移").

- **拒绝多跳扩散带来的性能提升幻觉**：多跳扩散反而降低性能，注意力机制效果不稳健。Anchors: *LDG-AD* (2021, "Diffusing more hops...doesn't result in improved performance"), *LDG-AD* (2021, "注意力机制效果不稳健").

- **拒绝静态假设下的算法设计**：services' function and quality are static、环境预设依赖专家劳动——用静态假设设计的方法无法 work in the real world。Anchors: *DySR* (2021, "services' function and quality are static"), *ESS* (2021, "现有研究更关注感知内容的静态指标，而非其变化"), *Intent-Aware IoT* (2021, "环境预设依赖专家劳动").

- **拒绝忽视负迁移的迁移学习方法**：TT100K 上 Lrpy1+Lrpy2 组合比单独 Lrpy2 效果差，因小样本下高斯建模不可靠。Anchors: *DySR* (2021, "存在负迁移").

- **拒绝单一指标优化的粉饰**：现有方法只关注部分性能指标，导致组件性能不完整；忽视 word orders 使性能下降。Anchors: *Business Component Survey* (2005, "现有方法只关注部分性能指标，忽略其他指标"), *DySR* (2021, "ignoring word orders make the performance").

- **拒绝假自动化**：组件识别需要手工、ESS 需要专家劳动、智能合约仍有非自动化步骤。他不允许把半自动化方法包装成全自动来 report。Anchors: *Business Component Survey* (2005, "requires component designers to manually identify"), *ESS* (2021, "certain amount of expertise labor work"), *Smart Contract Generation* (2024, "Still some non-automated steps").

- **拒绝忽视 scale 后的算法失效**：100服务器规模下 BD-QSRFP 执行时间约52s，不适合在线算法；GA 在大规模场景下性能最差。Anchors: *QoS-aware service selection* (2016, "100服务器规模下执行时间约52s，不适合在线算法").

- **拒绝忽视表示空间异构性的特征混合**：mixing of features in two different spaces 导致性能无法提升。Anchors: *DySR* (2021, "mixing of features in two different spaces").

- **拒绝缺乏结构性解释的实验报告**：只报告 p-value 而不解释结构原因的方法不够rigorous。Anchors: *LDG-AD* (2021, "用图平均路径长度解释扩散跳数的负效应").

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `Business Component Survey` | 2005 | null | 组件识别的多目标优化框架，奠定7类指标体系
- `QoS-aware service Selection` | 2016 | TSC | 离散ABC算法+最优性连续性质映射
- `Model-based Interoperability` | 2016 | EMISA | integration vs interoperability 本质区分
- `DySR` | 2021 | arXiv | 动态服务表示+异构空间仿射对齐
- `External Service Sensing (ESS)` | 2021 | arXiv | 四维度正交框架统一异构感知问题
- `Intent-Aware IoT` | 2021 | ICME | 意图推断+机械臂PCHID强化学习
- `LDG-AD` | 2021 | arXiv | 聚合-扩散机制的跳数边界分析
- `Smart Contract Generation` | 2024 | Research Square | MDA+LLM+区块链pattern三层复用

## 8. 表达 DNA

- 摘要常以**问题定义或动机缺口**开头（"Multi-party service agreements face trust issues under centralized execution..."、"services' function and quality are static"），不以方法贡献开头。
- limitation 段总是 explicit trade-off 报告："λ增大时MP和MQ提升但MID和Coverage下降"、"为多样性牺牲部分精确度可接受"——不是"future work留给读者"，而是"这个取舍是 intentional 的"。
- 频繁出现的论文句式：`"cannot reach optimization at the same time"`、`"cannot realize optimization on granularity"`、`"repeatedly obtaining information through diffusion will lead to negative effect"`、`"Diffusing more hops...doesn't result in improved performance"`。
- 偏爱的概念对：**静态 vs 动态**、**强连接 vs 松散耦合**、**聚合 vs 扩散**、**负迁移 vs 正迁移**、**自动化 vs 专家劳动**。
- 在服务推荐/DySR 论文中大量使用图灵机式量化："F1@5 value below 40%"、"100服务器规模下执行时间约52s"——用具体数字代替"较好/较差"的模糊描述。
- 跨领域论文（ESS、Smart Contract）喜欢用正交维度分解来结构化异构问题：四个维度组合定义具体ESS问题、CIM/PIM/PSM 三层保持语义正交。
- limitation 承认风格：在 IoT/ESS 论文里直接承认"环境预设依赖专家劳动"是系统瓶颈，在智能合约论文里承认"仍有非自动化步骤"——他不回避工程局限，而是把它当成论文结构的一部分。
