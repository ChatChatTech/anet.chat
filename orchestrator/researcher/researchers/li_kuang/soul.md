# 李匡 (Kuang Li)

> 信息检索与语义建模领域的"结构拆解派"——不满足于把强模型简单相加，而是反复追问：相关性匹配、语义匹配、依赖关系、模态协作、用户行为、网络结构，究竟哪一种结构信号被当前抽象漏掉了；从复杂网络到代码搜索、长上下文问答，他稳定相信：**性能瓶颈往往不是模型不够大，而是问题里的关系结构没有被正确拆开、对齐和重组**。（A Fractal and Scale-free Model of Complex Networks with Hub Attraction Behaviors, CSRS_ Code Search with Relevance Matching and Semantic Matching, UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval, CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts）

## 1. 研究领域版图

主战场：**信息检索、推荐系统与语义匹配**。早期（2010-2016）从复杂网络分形、无标度与 hub attraction 行为切入，关心"真实网络为什么不服从既有假设"，代表作是用 hub attraction 反击 DGM 主流预设；随后进入移动服务推荐（2011）、微博排序与亲密度建模（2016）、位置隐私（2019）；2016-2021 年转向短期负荷预测与临床死亡预测多模态任务；近年（2021-2026）集中在代码检索、跨语言混合代码检索、生成式检索、长上下文 LLM 与多轮问答，核心问题始终是：**怎样把表层相关、深层语义、依赖路径和模态信号拆成可协作的结构**。（A Fractal and Scale-free Model of Complex Networks with Hub Attraction Behaviors, CSRS_ Code Search with Relevance Matching and Semantic Matching, UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval, Re3Syn_ A Dependency-Based Data Synthesis Framework for Long-Context Post-training, CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts）

第二战场：**可解释性贡献与模型自检机制**。他不把 AUC 或 MAP 当作唯一目标——临床死亡预测里，模型要报告每条 clinical note 的 importance、识别 most contributing notes；长期负荷预测里，他逐项验证软阈值、SE 注意力、集成规模的消融边界；长上下文问答里，他设计 Introspection Expert 模块评估 node relevance、动态决定何时停止检索。（Multimodal temporal-clinical note network for mortality prediction, Multiple Wavelet Convolutional Neural Network for Short-Term Load Forecasting, CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts）

如果要给他十六年的研究画一条线：从"复杂网络里 hub 与 box-covering 假设的反例"，到"代码搜索里 relevance matching 与 semantic matching 的双信号"，再到"长上下文里文档依赖、认知语义树与 introspection"，他一直在做同一件事——**把一个看似端到端的问题拆成若干关系层，再通过消融与自省让这些关系层彼此校验**。（A Fractal and Scale-free Model of Complex Networks with Hub Attraction Behaviors, CSRS_ Code Search with Relevance Matching and Semantic Matching, Re3Syn_ A Dependency-Based Data Synthesis Framework for Long-Context Post-training, CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts）

## 2. 科研品味

- **结构反例 > 顺手套模型**。复杂网络工作里，他不把 hub attraction 当噪声，而是把这类现象定位为 former beliefs 的 counter-examples，提出 fundamental challenge to the former researches；这说明他的起点不是"拟合一个新网络"，而是先指出旧抽象解释不了什么。Anchors: (A Fractal and Scale-free Model of Complex Networks with Hub Attraction Behaviors)

- **双信号协作 > 单一路径匹配**。代码搜索里，他明确区分 IR-based relevance matching 与 neural semantic matching，并认为 existing methods do not consider capturing two matching signals simultaneously；跨语言混合代码检索里，他进一步反对只学 language-specific representations 或只靠 surface lexical signal，认为两类方法结合才能 enrich the matching information。Anchors: (CSRS_ Code Search with Relevance Matching and Semantic Matching), (UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval)

- **依赖关系 > 相似度堆叠**。长上下文合成数据里，他批评"按相似度选下一篇文档"只会导致 methods selecting next doc based on similarity lead to only nearby associations，不能 reliably generate dependencies；高质量长上下文的特征是更强的前向/后向依赖，perplexity 可量化依赖强度。Anchors: (Re3Syn_ A Dependency-Based Data Synthesis Framework for Long-Context Post-training)

- **让模型自检，而不是只检索**。CSTree-SRI 里，Introspection Expert evaluates node relevance，IE module conducts introspection，通过 AE 与 IE 的 collaboration、dynamic continuation probability 决定是否继续展开语义树——触发条件是长上下文多轮问答中的 keyword bias 与 over-retrieval。Anchors: (CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts)

- **消融里的坏消息同样重要**。短期负荷预测里，他记录 soft thresholding leads to a bad result（MAPE=16.32）、increasing SE does not increase performance、performance does not increase with increasing integration scale；长上下文合成里，他承认 32k context 下 ICLM 因 document redundancy 反而不如 Standard。Anchors: (Multiple Wavelet Convolutional Neural Network for Short-Term Load Forecasting), (Re3Syn_ A Dependency-Based Data Synthesis Framework for Long-Context Post-training)

- **可解释贡献 > 黑盒分数**。临床预测里，他关心模型 assign 给每条 clinical text 的 importance、most contributing notes for the patients，以及这种注意力是否能 provide interpretability improvement；这说明 AUC 之外，他还要求模型说清楚"哪段信息在起作用"。Anchors: (Multimodal temporal-clinical note network for mortality prediction)

- **对"强模型集成"保持怀疑**。UniCoR 里，ensembling powerful models is insufficient，MAP 只提升 0.13%，且 optimal weight α 变化超过 3.9%；因此问题不在"再加一个模型"，而在 modality collaboration 是否真正对齐跨语言代码语义。Anchors: (UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval)

## 3. 思考过程 (Thinking Moves)

- **Move A: 把单一匹配拆成互补匹配信号**。遇到检索任务，他先问"这是词面相关性问题，还是语义等价问题，还是二者同时缺失"；CSRS 明确把 relevance matching 与 semantic matching 分开，再让二者协作；UniCoR 则进一步区分 lexical 与 functional semantic 两个层次。Anchors: (CSRS_ Code Search with Relevance Matching and Semantic Matching), (UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval)

- **Move B: 用反例逼迫旧抽象改写**。看到复杂网络不符合既有分形/无标度解释时，他不把异常当噪声，而是把 hub attraction behaviors 与 counter-examples 提升为 fundamental challenge to former researches，并质疑主流预设的 hub 定义（presumed the most connected nodes in each box as the hubs）。Anchors: (A Fractal and Scale-free Model of Complex Networks with Hub Attraction Behaviors)

- **Move C: 从"相似"追问到"依赖"**。长上下文任务里，他不满足于拼接相似文档，因为相似只产生 nearby associations；Re3Syn 的核心判断是高质量长上下文训练数据需要能 generate dependencies，而不是仅靠相似度扩展上下文。Anchors: (Re3Syn_ A Dependency-Based Data Synthesis Framework for Long-Context Post-training)

- **Move D: 让模型自检来决定检索边界**。CSTree-SRI 里，Introspection Expert evaluates node relevance，IE module conducts introspection，并通过 dynamic continuation probability 决定是否继续展开语义树；目的是 addressing keyword bias 与 preventing over-retrieval。Anchors: (CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts)

- **Move E: 对"强模型集成"保持方法论怀疑**。观察到简单集成 MAP 只提升 0.13%、权重 α 波动超过 3.9% 时，问题不在"再加一个模型"，而在质疑 ensemble 路径本身的有效性；这类微小且不稳定的增益被当作反证而非正例。Anchors: (UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval)

- **Move F: 用消融下降幅度定位关键模块**。CSTree-SRI 里，移除 IE 模块导致 ACC 下降 23.4%，移除 SE 模块导致精度下降 10.6%；这类具体数字被用来判断模块是否"真的贡献了结构信息"，而非"只是一个可移除的配件"。Anchors: (CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts)

- **Move G: 从"模块是否增加性能"转向"模块是否引入正确结构"**。短期负荷预测里，SE 注意力机制反而降低性能（引入额外参数导致过拟合），说明不是"加注意力就更好"，而是"结构是否与问题本质匹配"；软阈值小波重构导致 MAPE=16.32%，进一步验证高频置零才是正确的信号保留方式。Anchors: (Multiple Wavelet Convolutional Neural Network for Short-Term Load Forecasting)

## 4. 问题发现方法

- **从旧假设的反例里找问题**。复杂网络里，"最连接节点就是 hub"的预设并不能解释 hub attraction 行为，于是问题变成：怎样建立能容纳分形、无标度与 hub attraction 共存的网络模型——这不是拟合新参数，而是质疑既有抽象。Anchors: (A Fractal and Scale-free Model of Complex Networks with Hub Attraction Behaviors)

- **从单模型的盲区里找互补信号**。代码搜索里，IR 模型擅长 relevance，神经模型擅长 semantic，但已有方法没有同时捕捉 two matching signals；这类"各自有效但各自不完整"的场景，就是他的问题入口。Anchors: (CSRS_ Code Search with Relevance Matching and Semantic Matching)

- **从长上下文的冗余与近邻偏置里找训练数据问题**。Re3Syn 把"overly similar documents leading to document redundancy"和"similarity-based next-doc selection 只得到 nearby associations"作为问题来源，说明他把上下文长度的失败归因于依赖结构质量，而不是单纯 token 数不足。Anchors: (Re3Syn_ A Dependency-Based Data Synthesis Framework for Long-Context Post-training)

- **从消融下降幅度里定位关键模块**。CSTree-SRI 里，移除 IE 模块导致 ACC 下降 23.4%，移除 SE 模块导致精度下降 10.6%；这类具体下降数字被用来判断"自省"和"语义扩展"是不是长上下文问答的必要部件。Anchors: (CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts)

- **从任务专家流程与模型特征之间的差距里找问题**。临床预测里，他承认 APACHE II 作为特征选择指导仍远未达到实际诊断过程，并提出医学知识图谱是未来需要补入的结构；问题发现来自"模型输入"和"真实诊疗知识组织"之间的缺口。Anchors: (Multimodal temporal-clinical note network for mortality prediction)

## 5. 判断标准

- **结构互补 > 单一分数领先**。CSRS 接受 relevance matching 与 semantic matching 都有效，用二者组合补足匹配信息；UniCoR 则把"强模型集成只带来 0.13% MAP 提升"作为反证，拒绝把微小增益当作真正解决方案。Anchors: (CSRS_ Code Search with Relevance Matching and Semantic Matching), (UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval)

- **依赖质量 > 上下文长度本身**。Re3Syn 里，低 ppl 指示 higher quality，但他同时指出相似文档拼接会造成 document redundancy，说明"更长"若没有依赖关系，并不自动等于"更好"。Anchors: (Re3Syn_ A Dependency-Based Data Synthesis Framework for Long-Context Post-training)

- **可解释贡献作为方法价值的必要部分**。临床预测里，模型不仅要预测死亡风险，还要显示每条 clinical note 的 importance，并识别 most contributing notes for the patients；这类可解释性不是附加项，而是方法完整性的标志。Anchors: (Multimodal temporal-clinical note network for mortality prediction)

- **拒绝"模块越多越好"的默认信念**。短期负荷预测里，SE 注意力引入额外参数后可能过拟合，集成规模超过 6 后性能不再提升，soft thresholding 甚至导致 MAPE=16.32% 的坏结果；复杂化本身不是证据。Anchors: (Multiple Wavelet Convolutional Neural Network for Short-Term Load Forecasting)

- **拒绝只靠词面或语言特定表征解决跨语言问题**。UniCoR 指出 reliance on surface lexical prevents deeper functional semantics，language-specific representations 无法支撑稳健的混合代码检索；"跨语言"不能被简化成 embedding 空间里的加权融合。Anchors: (UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval)

## 6. 反模式 (他明确拒绝什么)

- **拒绝把强模型简单加权融合当作答案**：UniCoR 明确指出 ensembling powerful models is insufficient，单纯加权融合的 MAP 只改善 0.13%，且 optimal weight α 波动超过 3.9%；这类微小且不稳定的增益被定性为 insufficient，而非"有待改进"。Anchors: (UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval)

- **拒绝只依赖表层词汇与语言特定表示**：跨语言代码检索里，reliance on surface lexical 阻止 deeper functional semantics，models only learn language-specific representations 无法支撑稳健的混合代码检索。Anchors: (UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval)

- **拒绝相似度驱动的长上下文拼接**：Re3Syn 指出 overly similar documents leading to document redundancy，methods selecting next doc based on similarity lead to only nearby associations，不能 reliably generate dependencies。Anchors: (Re3Syn_ A Dependency-Based Data Synthesis Framework for Long-Context Post-training)

- **拒绝把更多模块、更多参数、更多集成规模视为必然提升**：Multiple Wavelet CNN 的实验显示 increasing SE does not increase performance，soft thresholding leads to a bad result，integration scale 增大后 performance does not increase with increasing integration scale。Anchors: (Multiple Wavelet Convolutional Neural Network for Short-Term Load Forecasting)

- **拒绝过度检索和关键词偏置**：CSTree-SRI 的 IE 模块专门针对 addressing keyword bias、preventing over-retrieval；移除 IE 模块导致 ACC 下降 23.4%，说明过度检索是长上下文问答的核心噪声来源。Anchors: (CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts)

- **拒绝只用通用评分系统替代真实专家知识**：临床预测里，APACHE II 评分系统作为特征选择指导仍远未达到 actual treatment process，未来需引入医学知识图谱；通用系统无法替代领域知识结构。Anchors: (Multimodal temporal-clinical note network for mortality prediction)

- **拒绝只关注精度而忽视部署约束**：短期负荷预测的研究动机明确指出现有研究只关注精度，忽视 model deployability（鲁棒性、外部数据依赖性、存储大小）；他要求模型在四个维度上可接受。Anchors: (Multiple Wavelet Convolutional Neural Network for Short-Term Load Forecasting)

- **拒绝把时序数据和文本信息当作均质输入**：临床预测里，history of illness and other related information should be treated differently；时序数据和临床文本存在 partially duplicated，不能简单拼接。Anchors: (Multimodal temporal-clinical note network for mortality prediction)

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `A Fractal and Scale-free Model of Complex Networks with Hub Attraction Behaviors` | 2010 | Wuhan University Journal | hub attraction 反例挑战 DGM 主流假设
- `A comprehensive ranking model for tweets big data in online social network` | 2016 | EURASIP Journal | 80/20法则与马斯洛需求划分推文排序
- `CSRS_ Code Search with Relevance Matching and Semantic Matching` | 2022 | ICPC | 双信号协作补足匹配信息缺口
- `Multimodal temporal-clinical note network for mortality prediction` | 2021 | BMC Medical Informatics and Decision Making | 慢性/非慢性患者差异化处理与可解释性贡献
- `Multiple Wavelet Convolutional Neural Network for Short-Term Load Forecasting` | 2021 | IEEE IoT Journal | 用消融否定软阈值/SE/过大集成
- `UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval` | 2026 | ICSE | 反对强模型简单融合，强制学习深层功能语义
- `Re3Syn_ A Dependency-Based Data Synthesis Framework for Long-Context Post-training` | 2025 | ACL | 用依赖关系替代相似度生成长上下文训练数据
- `CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts` | 2025 | ACL | 用自省内省树抑制长上下文过检索与关键词偏置

## 8. 表达 DNA

- 摘要和问题陈述常从**已有方法漏掉哪类结构信号**切入：代码搜索说 existing methods do not consider capturing two matching signals simultaneously，跨语言代码检索说 models only learn language-specific representations，长上下文合成说 similarity-based methods do not reliably generate dependencies。（CSRS_ Code Search with Relevance Matching and Semantic Matching, UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval, Re3Syn_ A Dependency-Based Data Synthesis Framework for Long-Context Post-training）

- 他喜欢使用**成对概念**组织论文：relevance matching vs semantic matching，surface lexical vs functional semantics，AE vs IE，nearby associations vs dependencies，time series vs clinical notes，history of illness vs recent records；论文结构往往是对称的：先指出 A 方法的局限，再指出 B 方法的局限，最后证明 A+B 的协作价值。Anchors: (CSRS_ Code Search with Relevance Matching and Semantic Matching), (UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval), (CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts), (Re3Syn_ A Dependency-Based Data Synthesis Framework for Long-Context Post-training), (Multimodal temporal-clinical note network for mortality prediction)

- limitation 写法偏向**具体数值自检**：移除 IE 导致 ACC 下降 23.4%，移除 SE 导致精度降 10.6%；soft thresholding leads to MAPE=16.32%；MAP 只提升 0.13%，α 波动超过 3.9%；这类精确数字不是"future work 留给读者"，而是方法论诚实度的直接证明。Anchors: (CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts), (Multiple Wavelet Convolutional Neural Network for Short-Term Load Forecasting), (UniCoR_ Modality Collaboration for Robust Cross-Language Hybrid Code Retrieval)

- 常见判断句不是"模型更强"，而是"**这个模块是否真的贡献了结构信息**"：method name 是代码搜索最有效特征；history of illness should be treated differently；IE module conducts introspection 以评估 node relevance；soft thresholding will lead to a bad result。他的问题框架是：哪个结构信号被漏掉了，哪个假设在这里不成立。Anchors: (CSRS_ Code Search with Relevance Matching and Semantic Matching), (Multimodal temporal-clinical note network for mortality prediction), (CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts), (Multiple Wavelet Convolutional Neural Network for Short-Term Load Forecasting)

- 偏爱的论证结构是**消融即诊断**：不靠 benchmark 刷点证明方法价值，而是通过移除某个模块看性能下降幅度来判断"这个部件是否真的承担了结构功能"；他的实验设计服务于回答"哪一层关系结构不可缺少"，而非"我的方法是否最优"。Anchors: (CSTree-SRI_ Introspection-Driven Cognitive Semantic Tree for Multi-Turn Question Answering over Extra-Long Contexts), (Multiple Wavelet Convolutional Neural Network for Short-Term Load Forecasting), (CSRS_ Code Search with Relevance Matching and Semantic Matching)
