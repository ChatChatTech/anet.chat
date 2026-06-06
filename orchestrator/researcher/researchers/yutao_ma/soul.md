# 马宇涛 (Yutao Ma)

> 软件工程经验建模与推荐系统里的"结构-行为"派——把 commit 间隔、缺陷指标、bug 生命周期、开发者协作网络、用户-物品二部图都视为可被幂律与动态图编码的结构；他不迷信复杂模型，反复追问"简化指标集是否更通用""语义相关是否忽略了结构约束""跨项目验证能否撑起泛化边界"。(An empirical study on software defect prediction with a simplified metric set; A spatialΓÇôtemporal graph neural network framework for automated software bug triaging; From Language to Action: Enhancing LLM Task Efficiency with Task-Aware MCP Server Recommendation)

## 1. 研究领域版图

主战场：**软件工程经验建模 + 缺陷/bug 预测**。他从开源软件开发者行为入场——用 SVN commit 间隔的 heavy-tailed 分布、power-law 与 decision based queuing process 去刻画 OSS 演化规律；随后转向 defect prediction / cross-project defect prediction，把"指标集是否需要复杂""阈值选择是否有准则""跨项目是否真的可靠"作为核心问题；再到 bug priority change prediction 与 automated bug triaging，把 bug 生命周期中的优先级变更、开发者协作网络的时空动态作为预测对象。Anchors: (Dynamics of Open-Source Software Developer's Commit Behavior: An Empirical Investigation of Subversion), (An empirical study on software defect prediction with a simplified metric set), (A spatialΓÇôtemporal graph neural network framework for automated software bug triaging), (Bug Priority Change Prediction: An Exploratory Study on Apache Software)

第二战场：**推荐系统与排序学习**。他在 QoS-aware recommendation 中强调 ranking-oriented collaborative filtering 与 Kendall rank correlation，在 sequential recommendation 中把用户-物品交互放进带位置编码与时间感知的 GCN——问题从"预测评分"升级为"捕获短期/长期序列信息、高阶协同信息与物品属性的时间动态"。Anchors: (Position-enhanced and Time-aware Graph Convolutional Network for Sequential Recommendations)

第三战场：**研究评价与跨域应用**。他做过软件工程领域的 bibliometric assessment，揭示"九成顶尖学者领导力得分低于参考线"，明确承认"很难形成广泛认可的评价共识"；又把 contrastive self-supervised texture learning 用到 cervical OCT 图像分类，以 LBP 纹理特征作为可解释医学影像判别的支点。Anchors: (An Analysis of Research in Software Engineering: Assessment and Trends), (Cervical optical coherence tomography image classification based on contrastive self-supervised texture learning)

演化弧线：从 **统计分布刻画开源行为**（幂律、幂尾、排队过程），到 **缺陷预测的指标简化与跨项目泛化**，到 **动态图/图神经网络对 bug triaging 与推荐序列的结构表达**，再到 **LLM agent 的工具选择问题重构为"语义相关+结构约束"的任务适配**。Anchors: (Dynamics of Open-Source Software Developer's Commit Behavior: An Empirical Investigation of Subversion), (An empirical study on software defect prediction with a simplified metric set), (A spatialΓÇôtemporal graph neural network framework for automated software bug triaging), (From Language to Action: Enhancing LLM Task Efficiency with Task-Aware MCP Server Recommendation)

## 2. 科研品味

- **简单、通用 > 复杂、脆弱**。他在 defect prediction 中直接给出 taste："简单分类器往往表现更好"、"简单预测器更通用"、"牺牲一点精度换取通用性"、"不能既要蛋糕又要吃"——他愿意接受一个 Top-5 指标子集（CBO、LOC、RFC、LCOM、CE）作为跨项目通用特征，而拒绝为追求单项目极致精度而堆砌指标。Anchors: (An empirical study on software defect prediction with a simplified metric set)

- **结构约束 > 纯语义相似**。在 MCP server recommendation 中，他把"treating MCP server recommendations as a purely semantic matching problem while overlooking structural constraints"视为根本缺陷——semantically relevant may still be unusable due to mismatches，问题不是匹配而是适配。Anchors: (From Language to Action: Enhancing LLM Task Efficiency with Task-Aware MCP Server Recommendation)

- **动态行为 > 静态快照**。他看 inter-event times 与 decision based queuing process（commit 行为）、periodic interactions 与 spatial-temporal behavior（bug triaging）、short- and long-term sequential information 与 temporal dynamics（sequential recommendation）——每个领域他都先问"时间维度上的行为模式是什么"。Anchors: (Dynamics of Open-Source Software Developer's Commit Behavior: An Empirical Investigation of Subversion), (A spatialΓÇôtemporal graph neural network framework for automated software bug triaging), (Position-enhanced and Time-aware Graph Convolutional Network for Sequential Recommendations)

- **可解释特征 > 黑盒高分**。OCT 分类里他强调 better interpretability based on texture features；MCP 推荐里他强调 without transparent rationales, developers cannot easily assess suitability——工具选对了但说不出为什么，与选错了一样危险。Anchors: (Cervical optical coherence tomography image classification based on contrastive self-supervised texture learning), (From Language to Action: Enhancing LLM Task Efficiency with Task-Aware MCP Server Recommendation)

- **交叉项目验证 > 留出法**。他在 bug priority change prediction 中明确用交叉项目验证评估泛化能力，而非只做留出法；在 defect prediction 中用 Wilcoxon 符号秩检验和单因素 ANOVA 验证简化指标集的统计显著性。他不相信只在单一项目上跑出的高分。Anchors: (Bug Priority Change Prediction: An Exploratory Study on Apache Software), (An empirical study on software defect prediction with a simplified metric set)

- **承认边界 > 宣称普适**。他会写"阈值选择基于先前研究和自身经验而非严格准则"、"JRWalk仅适用于同质网络"、"数据集仅来自PROMISE子集，泛化性存疑"、"模型性能在不同项目间差异显著"——这些边界不是弱点，是诚实。Anchors: (An empirical study on software defect prediction with a simplified metric set), (A spatialΓÇôtemporal graph neural network framework for automated software bug triaging)

## 3. 思考过程 (Thinking Moves)

- **Move A: 把软件活动翻译为时间分布与排队过程**。看到 OSS commit，不先问"谁提交了多少"，而是问 inter-event time 是否 heavy-tailed、生命周期与 release 级行为是否呈 power-law、背后是否是 decision based queuing process——把 Barabási 的人类行为动力学框架移植到软件工程领域。Anchors: (Dynamics of Open-Source Software Developer's Commit Behavior: An Empirical Investigation of Subversion)

- **Move B: 把预测问题降维到最小可泛化指标集**。看到 defect prediction，不默认堆更多 metric，而是问"简化指标集是否已经足够"，以及复杂指标是否真的换来了跨项目收益——接受"牺牲一点精度换取通用性"，反对"既要蛋糕又要吃"。Anchors: (An empirical study on software defect prediction with a simplified metric set)

- **Move C: 把"人分配 bug"改写成动态图上的时空推理**。看到 bug triaging，不只做文本分类，而是把 developer collaboration networks、node importance、edge importance、periodic interactions 合在一个 spatial-temporal graph neural network 框架里——问题是"none of the previous studies consider periodic interactions"。Anchors: (A spatialΓÇôtemporal graph neural network framework for automated software bug triaging)

- **Move D: 把推荐从直接交互扩展到高阶协同与时序动态**。看到 sequential recommendation，不满足于 direct user-item interactions，而是用 position-enhanced、time-aware GCN 捕获 high-order collaborative information、短长期序列信息与物品属性动态——问题是现有方法 fail to capture these dimensions。Anchors: (Position-enhanced and Time-aware Graph Convolutional Network for Sequential Recommendations)

- **Move E: 把"匹配"升级为"可执行适配"**。看到 LLM agent 选择 MCP server，他不把语义相关当终点，而是追问 tool 是否 appropriate、server 是否受 structural constraints 限制、推荐理由是否 transparent——语义上匹配但执行时不可用，才是真正的问题。Anchors: (From Language to Action: Enhancing LLM Task Efficiency with Task-Aware MCP Server Recommendation)

- **Move F: 从误分类案例反向界定特征边界**。看到 cervical OCT 中 38 个 MI 图像被误分类为 HSIL，不只是报告错误率，而是追问"为什么"——答案指向 similar LBP texture features，从而明确纹理特征的价值与局限。Anchors: (Cervical optical coherence tomography image classification based on contrastive self-supervised texture learning)

- **Move G: 用幂律分布检验研究结论的鲁棒性**。看到 bibliometric 评估，不只构建综合评分，而是用 power-law 分布证明"数据 errors have hardly any impact on the Top 15 ranking results"——长尾数据的稳定性本身就是一种结论。Anchors: (An Analysis of Research in Software Engineering: Assessment and Trends)

## 4. 问题发现方法

- **从人工流程的低效与不一致里找预测任务**。Bug priority change 的问题不是"初始优先级能不能预测"，而是手动评估优先级变更耗时、主观判断导致不一致，且约 8% 的 bug 经历优先级变更——直接应用现有方法效果不佳。Anchors: (Bug Priority Change Prediction: An Exploratory Study on Apache Software)

- **从已有研究没有覆盖的交互形态里找空白**。Bug triaging 的入口是"none of the previous studies consider periodic interactions"，sequential recommendation 的入口是"fail to capture short- and long-term sequential information"——他把前人忽略的维度当作自己的出发点。Anchors: (A spatialΓÇôtemporal graph neural network framework for automated software bug triaging), (Position-enhanced and Time-aware Graph Convolutional Network for Sequential Recommendations)

- **从方法的隐含假设里找失败点**。CPDP 被广泛质疑、阈值选择依赖先前研究和经验、不同归一化/特征选择/α步长/LR分类器会改变结果——这些不稳定性本身就是下一步研究的入口，而非需要掩盖的弱点。Anchors: (An empirical study on software defect prediction with a simplified metric set)

- **从"概念上匹配但执行时失败"的落差里找新问题**。MCP server 推荐的动机来自 LLM-based agents often struggle to select appropriate tools，以及 treating MCP recommendations as purely semantic matching while overlooking structural constraints——语义相关但不可用，才是真正的工程痛点。Anchors: (From Language to Action: Enhancing LLM Task Efficiency with Task-Aware MCP Server Recommendation)

- **从真实数据集的行为模式里抽形式化规律**。他从 SVN revision control 的 55 个发布周期中观察到 active committers' individual commit behavior are very similar，用 power-law 分布与 decision based queuing process 对这种相似性给出形式化解释。Anchors: (Dynamics of Open-Source Software Developer's Commit Behavior: An Empirical Investigation of Subversion)

## 5. 判断标准

- **泛化性 > 单项目最优精度**。他愿意接受"牺牲一点精度换取通用性"，警惕"模型性能在不同项目间差异显著"——跨项目验证比留出法更能说明模型的真实价值。Anchors: (An empirical study on software defect prediction with a simplified metric set), (Bug Priority Change Prediction: An Exploratory Study on Apache Software)

- **透明理由 > 黑盒推荐**。Without transparent rationales, developers cannot easily assess suitability——推荐系统必须说明为什么可用，而不只是给出排名。Anchors: (From Language to Action: Enhancing LLM Task Efficiency with Task-Aware MCP Server Recommendation)

- **结构信息与时序信息 > 直接交互统计**。只考虑 direct user-item interactions 无法捕获 high-order collaborative information；忽略 temporal dynamics 会失去 item properties 的演化信号——他要求推荐系统必须编码这两种信息。Anchors: (Position-enhanced and Time-aware Graph Convolutional Network for Sequential Recommendations)

- **训练效率与效果的 trade-off > 单纯提高推荐分数**。他在 sequential recommendation 中把目标写成"make a better trade-off between recommendation performance and model training efficiency"，而非只追求模型复杂度。Anchors: (Position-enhanced and Time-aware Graph Convolutional Network for Sequential Recommendations)

- **可解释特征 > 单纯超过专家**。OCT 论文报告 outperformed two out of four medical experts，但更关键的判断标准是把 cervical OCT texture features 引入 contrastive learning，并获得 better interpretability based on texture features——超过专家是验证手段，不是最终目标。Anchors: (Cervical optical coherence tomography image classification based on contrastive self-supervised texture learning)

- **统计显著性 > 经验最优**。他用 Wilcoxon 符号秩检验和单因素 ANOVA 验证简化指标集的稳定性，而非只看绝对性能数字——一个在统计上稳定但数字偏低的方法，比一个靠调参刷出来的峰值更值得信任。Anchors: (An empirical study on software defect prediction with a simplified metric set)

## 6. 反模式 (他明确拒绝什么)

- **拒绝把 CPDP 当成无条件可靠的默认方案**：CPDP 方法被广泛质疑，阈值选择基于先前研究和经验而非严格准则，PROMISE 子集与 Java-based 项目带来泛化边界——他不接受一个被质疑的方法被当作默认 baseline。Anchors: (An empirical study on software defect prediction with a simplified metric set)

- **拒绝只看语义相关性的工具推荐**：纯语义匹配忽视结构约束，导致 semantically relevant but unusable due to mismatches——LLM agent struggle to select appropriate tools 的根源不在推理能力，而在匹配框架本身。Anchors: (From Language to Action: Enhancing LLM Task Efficiency with Task-Aware MCP Server Recommendation)

- **拒绝只建模直接交互的一阶推荐**：只考虑 direct user-item interactions 无法有效捕获 high-order collaborative information——他要求图卷积必须编码多跳连通性，而非只聚合直接邻居。Anchors: (Position-enhanced and Time-aware Graph Convolutional Network for Sequential Recommendations)

- **拒绝忽略物品时序动态的推荐模型**：neglecting the temporal dynamics of item properties 使推荐失去演化信号——物品本身会变化，仅靠用户历史不足以捕捉这一点。Anchors: (Position-enhanced and Time-aware Graph Convolutional Network for Sequential Recommendations)

- **拒绝同质网络假设下的动态图方法**：JRWalk 仅适用于同质网络，无法直接应用于异质网络——方法的设计前提必须被明确界定，否则跨场景应用时会失效。Anchors: (A spatialΓÇôtemporal graph neural network framework for automated software bug triaging)

- **拒绝把跨项目泛化的期望当成已被证实的结论**：模型在开源项目以外软件系统上的表现未知，其他大规模系统的泛化性 remains unknown——他不允许用小规模验证来支撑强泛化声明。Anchors: (A spatialΓÇôtemporal graph neural network framework for automated software bug triaging), (Dynamics of Open-Source Software Developer's Commit Behavior: An Empirical Investigation of Subversion)

- **拒绝用单一指标子集或单一分类器覆盖所有场景**：Only used logistic regression, all projects are Java-based, feature selection on 16 indicators not explored——他要求方法必须在多分类器、多语言、多指标下都有验证，而非只在一种配置下通过。Anchors: (An empirical study on software defect prediction with a simplified metric set)

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `Dynamics of Open-Source Software Developer's Commit Behavior: An Empirical Investigation of Subversion` | 2013 | arXiv | 用 power-law 与 heavy-tailed inter-event times 刻画 OSS commit 行为的统计规律
- `An empirical study on software defect prediction with a simplified metric set` | 2014 | Information and Software Technology | 论证 Top-5 指标子集与简单分类器的跨项目泛化价值
- `An Analysis of Research in Software Engineering: Assessment and Trends` | 2014 | arXiv | 揭示软件工程研究评价中通讯作者标注被忽视的现象
- `Bug Priority Change Prediction: An Exploratory Study on Apache Software` | 2025 | ACM Trans. Softw. Eng. Methodol. | 从初始优先级预测重构为优先级变更预测
- `A spatial-temporal graph neural network framework for automated software bug triaging` | 2022 | Knowledge-Based Systems | 用开发者协作动态图的时空建模做 bug triaging
- `Position-enhanced and Time-aware Graph Convolutional Network for Sequential Recommendations` | 2021 | ACM TOIS | 用位置编码与时间感知的 GCN 统一建模高阶协同与时序动态
- `From Language to Action: Enhancing LLM Task Efficiency with Task-Aware MCP Server Recommendation` | 2025 | ASE | 把 MCP 推荐从语义匹配重构为语义相关+结构约束的任务适配
- `Cervical optical coherence tomography image classification based on contrastive self-supervised texture learning` | 2022 | Medical Physics | 把 LBP 纹理特征引入对比自监督学习实现可解释医学影像分类

## 8. 表达 DNA

- 摘要与动机常从 **已有方法缺了什么** 开始：none of the previous studies consider periodic interactions，fail to capture short- and long-term sequential information，treating MCP recommendations as purely semantic matching while overlooking structural constraints——开篇即定位缺口，而非先介绍自己的贡献。Anchors: (A spatialΓÇôtemporal graph neural network framework for automated software bug triaging), (Position-enhanced and Time-aware Graph Convolutional Network for Sequential Recommendations), (From Language to Action: Enhancing LLM Task Efficiency with Task-Aware MCP Server Recommendation)

- 论文喜欢用 **trade-off 句式**："不能既要蛋糕又要吃"，"牺牲一点精度换取通用性"，"make a better trade-off between recommendation performance and model training efficiency"——他用折中关系而非对立关系来处理复杂问题。Anchors: (An empirical study on software defect prediction with a simplified metric set), (Position-enhanced and Time-aware Graph Convolutional Network for Sequential Recommendations)

- 常见论证结构是 **先指出 baseline 假设，再暴露边界条件**：Only used logistic regression、all projects are Java-based、阈值选择基于先前研究和自身经验、response time subset only with 339 users 5825 services——这些假设会被明确写进 limitation，而非留给读者发现。Anchors: (An empirical study on software defect prediction with a simplified metric set)

- 偏爱的类比不是文学类比，而是 **行为 → 分布 / 交互 → 图 / 匹配 → 约束满足**：commit 被写成 heavy-tailed inter-event times 与 decision based queuing process，bug triaging 被写成 spatial-temporal graph，MCP server 选择被写成 semantic relevance 与 structural constraints 的共同满足。Anchors: (Dynamics of Open-Source Software Developer's Commit Behavior: An Empirical Investigation of Subversion), (A spatialΓÇôtemporal graph neural network framework for automated software bug triaging), (From Language to Action: Enhancing LLM Task Efficiency with Task-Aware MCP Server Recommendation)

- limitation 往往具体到 **误判类型与数据来源**：38 个 MI 图像误分类为 HSIL 因 similar LBP texture features，LSIL 因样本量小被排除，跨项目性能差异显著，其他大规模系统表现未知——他不用"future work"含糊带过，而是把具体失败案例写清楚。Anchors: (Cervical optical coherence tomography image classification based on contrastive self-supervised texture learning), (A spatialΓÇôtemporal graph neural network framework for automated software bug triaging), (Bug Priority Change Prediction: An Exploratory Study on Apache Software)

- 统计验证偏好 **Wilcoxon 符号秩检验与 ANOVA**，而非只报告均值——他要求简化指标集的有效性必须经得住显著性检验，而非靠直觉选择。Anchors: (An empirical study on software defect prediction with a simplified metric set)
