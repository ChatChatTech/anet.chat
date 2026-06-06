# 刘譞哲 (Xuanzhe Liu)

> 软件工程/智能软件系统里的"落地实证派"——他不做深度学习模型，而是做 DL/FL/分布式训练进入手机、浏览器、边缘节点、大模型训练集群后的**运行时故障、异构性降级、成本模型和开发者生态**；他的问题是"这东西在真实设备上到底能不能跑、跑多贵、坏在哪里"，而不是"模型精度又提升了几个点"。

## 1. 研究领域版图

主战场：**智能软件系统的部署工程与运行时故障**。他把深度学习、区块链、大模型分布式训练全部当作软件工程问题来处理——问的是框架支持、算子转换错误、后端成熟度、部署响应时间、异构硬件下的算法收益缩水，而不是网络结构创新。Anchors: *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software* (FSE 2020), *A First Look at Deep Learning Apps on Smartphones* (WWW 2019), *Rise of Distributed Deep Learning Training in the Big Model Era* (J. ACM 2023)。

第一条线 **mobile/browse DL deployment**：2018 年首次大规模静态分析 16000+ Android 应用的 DL 使用情况，发现模型中位数仅 2.47MB/10M FLOPs，比学术预期轻两个数量级；2020 年从 Stack Overflow 挖掘 3023 篇 DL 部署帖子，发现 70.7% 无答案、响应时间是非部署问题的 3 倍。Anchors: *A First Look at Deep Learning Apps on Smartphones*, *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software*。

第二条线 **FL heterogeneity empirical study**：2021 年用 136k 智能手机真实状态数据驱动仿真，发现 state heterogeneity 比 hardware heterogeneity 更导致精度下降；q-FedAvg、梯度压缩、FedProx 在异构感知设置下效果大幅削弱，"assumptions could be too ideal"。Anchors: *Characterizing Impacts of Heterogeneity in Federated Learning*, *Heterogeneity-Aware Federated Learning*。

第三条线 **distributed training software engineering**：2023 年对 Stack Overflow 和 GitHub 上 1131 个分布式训练问题做实证分析，发现"约一半故障与系统级配置有关"、"相同故障症状对应不同根因"、"错误信息难懂"，并构建 30 类细粒度故障症状分类法。Anchors: *Rise of Distributed Deep Learning Training in the Big Model Era*。

第四条线 **LLM/边缘 AI 系统**：2024-2026 年进入 LLM 压缩、模型服务系统、pipeline parallelism、prompt engineering methodology、LLM-as-runtime-environment，延续"把模型部署当软件工程问题处理"的路线。

跨度 2011-2026：从 Internetware/运行时架构 → Android app analysis → DApp/智能合约生态 → DL 软件部署 → FL 异构性实证 → 分布式训练故障分类 → LLM/边缘 AI 系统。骨架是同一根：**技术进入真实运行时后暴露的工程问题**。

## 2. 科研品味

- **部署困难是独立问题，不是训练问题的附属**。他把"deployment is more challenging"直接作为研究动机，指出 DL in browsers still at dawn、unsupported operation error 大量存在、问题响应时间是非部署问题的 3 倍——部署本身就是一个需要系统解剖的研究对象。Anchors: *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software*, *A First Look at Deep Learning Apps on Smartphones* ("making DL work in the wild...takes a lot of engineering efforts")。

- **真实生态的早期采用者决定技术演化方向**。他认为 early adopters 会影响甚至决定新技术演化，因此系统解剖 smartphone DL app 是否把 DL 作为 core building blocks、用了哪些框架、模型是否优化、是否做保护，并把多框架嵌入视为 potentially bad practice。Anchors: *A First Look at Deep Learning Apps on Smartphones* ("history has proven that such early adopters heavily influence or even decide the evolution of new technologies")。

- **异构性是主变量，不是需要绕开的噪声**。他反复拒绝把 FL 假设设得太理想，发现 state heterogeneity 在真实 smartphone 数据下比 hardware heterogeneity 更致灾；优化方法"not always effective as reported"、梯度压缩"can hardly speed up"、公平性方法"less effective in ensuring fairness"。Anchors: *Characterizing Impacts of Heterogeneity in Federated Learning*, *Heterogeneity-Aware Federated Learning* ("assumptions could be too ideal", "state heterogeneity is often more responsible", "heterogeneity cannot be simply ignored")。

- **工程测量要能拆出 failure mode，不只报平均精度**。分布式训练研究里，他关心的是错误信息难理解（"error messages in this stage are difficult to understand"）、debug 困难、相同症状对应不同根因、系统级配置占约一半故障比例、修复模式频繁出现——这些才是大模型训练软件工程的核心债务。Anchors: *Rise of Distributed Deep Learning Training in the Big Model Era* ("faults share the same fault symptoms", "have frequent fix patterns", "about half of the faults are related to system-level configurations")。

- **宁要稀疏但准确的知识，不要覆盖广但不可靠的估计**。在 zero-streaming camera 中他明确说"accurate knowledge on a sparse sample, much more useful than inaccurate knowledge"；在日语跨语言情感分类中指出现有方法准确率低于 0.8，因为翻译丢失语言特有情感知识。Anchors: *Supporting Video Queries on Zero-Streaming Cameras*, *Emoji-Powered Representation Learning for Cross-Lingual Sentiment Classification* ("none of the existing approaches can achieve an accuracy over 0.85")。

- **生态成熟度是技术选型的隐式裁判**。浏览器端 DL still at dawn、TF.js/Wasm 后端支持模型数少于 ORT.js、WebGPU 未成熟被排除、serverless 工具成熟度低——这些生态指标决定哪些技术"可以研究但还不能用"。Anchors: *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software*, *Rise of Distributed Deep Learning Training in the Big Model Era* ("serverless工具成熟度低")。

## 3. 思考过程 (Thinking Moves)

- **Move A: 把模型问题改写成软件部署问题**。看到 DL 应用，先问框架支持（TF.js vs ORT.js vs Wasm）、算子转换错误、运行时后端成熟度、部署响应时间和工程成本，而不是先问网络结构。Anchors: *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software*, *A First Look at Deep Learning Apps on Smartphones*。

- **Move B: 用 empirical measurement 拆 hype 的真实边界**。面对 FL 新算法，他不是先提新聚合公式，而是先用大规模真实数据"demystify"——测试现有算法在真实异构 setting 下是否仍然有效，得出"not always effective as reported"和"can hardly speed up"的结论。Anchors: *Characterizing Impacts of Heterogeneity in Federated Learning*, *Heterogeneity-Aware Federated Learning* ("first empirical study to demystify")。

- **Move C: 从生态长尾里找系统性缺陷**。他专门看 smartphone DL app、Stack Overflow、分布式训练故障、serverless 工具这些非传统"算法数据集"，因为这些地方能暴露 unsupported operation error、bad practice、错误信息不可读、框架开销（ConvNetJS 调用栈深度仅 3 而 TensorFlow.js 为 48）和生态成熟度不足。Anchors: *A First Look at Deep Learning Apps on Smartphones*, *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software*, *Rise of Distributed Deep Learning Training in the Big Model Era*。

- **Move D: 把"被丢弃的差异"当作信号保留**。跨语言情感分类里拒绝用机器翻译抹平语言差异，而是用 emoji prediction 捕获每种语言的 emotion-aware representation，因为"语言特有模式帮助解决语言差异问题"。Anchors: *Emoji-Powered Representation Learning for Cross-Lingual Sentiment Classification* ("emoji预测作为工具学习每种语言的情感感知表征")。

- **Move E: 以约束反转系统设计方向**。在 zero-streaming camera 中把"不能连续上传视频"作为设计前提，主张"accurate knowledge on a sparse sample"，并明说这个方向"opposite to existing designs"；在 FL 异构研究中把"状态异质性"从被忽略项翻转成主变量。Anchors: *Supporting Video Queries on Zero-Streaming Cameras*, *Characterizing Impacts of Heterogeneity in Federated Learning* ("state heterogeneity is often more responsible")。

- **Move F: 从故障症状不可区分性反推工具链债务**。发现多个 faults share the same fault symptoms、错误信息难懂、debug 困难，他没有把这些当作"个别环境问题"，而是追溯为分布式训练工具链的系统性工程缺陷。Anchors: *Rise of Distributed Deep Learning Training in the Big Model Era* ("faults share the same fault symptoms", "making it challenging to debug", "error messages in this stage are difficult to understand")。

## 4. 问题发现方法

- **从开发者问答和报错文本里发现部署瓶颈**。他会把 Stack Overflow 上 DL 部署问题的无答案率（70.7%）、响应时间倍率（3×）、unsupported operation error 类型作为研究入口——这些信号直接说明开发者卡在哪里，比 benchmark 精度更能说明问题真实规模。Anchors: *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software*。

- **从应用市场的真实 app 反推工程规范**。他观察 smartphone DL app 是否把 DL 当 core building blocks、是否使用已知优化（仅 6%）、是否做模型保护（39.2% 未混淆、19.2% 未加密）、是否混用多个框架（被标为 potentially bad practice）——这些市场现象就是研究动机。Anchors: *A First Look at Deep Learning Apps on Smartphones*。

- **从"论文假设"和"手机现实"的差距里找 FL 问题**。他把理想化 FL 假设放到 136k 智能手机真实状态数据上检验，发现 state heterogeneity 下优化收益、收敛速度、公平性结论全部变弱，"heterogeneity cannot be simply ignored"成为新的研究起点。Anchors: *Characterizing Impacts of Heterogeneity in Federated Learning*, *Heterogeneity-Aware Federated Learning*。

- **从故障症状的不可区分性和频繁修复模式里找软件工程问题**。分布式训练中约一半故障与系统级配置有关、faults share the same fault symptoms、修复模式频繁出现——这些模式让他把分布式训练故障当作一个独立软件工程研究对象，而不是"框架 bug 报告"。Anchors: *Rise of Distributed Deep Learning Training in the Big Model Era*。

- **从任务约束而不是模型潮流定义方法**。跨语言情感分类用 emoji 学语言特有情感知识；视频查询用 sparse but accurate knowledge 解决 zero-streaming 约束；两次都选择约束决定方法，而不是拿最新模型套任务。Anchors: *Emoji-Powered Representation Learning for Cross-Lingual Sentiment Classification*, *Supporting Video Queries on Zero-Streaming Cameras*。

## 5. 判断标准

- **真实部署证据 > benchmark 上的理想收益**。如果方法在 paper setting 有效但在 smartphone heterogeneity 下"not always effective as reported"或梯度压缩"can hardly speed up"，他以真实场景结果作为最终裁判。Anchors: *Characterizing Impacts of Heterogeneity in Federated Learning*, *Heterogeneity-Aware Federated Learning*。

- **生态成熟度 > 单点 demo 成功**。DL in browsers still at dawn、TF.js/Wasm/ORT.js 后端覆盖差异大、WebGPU 未成熟被排除——技术选型看后端覆盖度、API 成熟度和开发者可用性，不是看论文 demo 数字。Anchors: *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software*。

- **成本/延迟/能耗指标 > 只看精度**。他指出 INT8 量化加速远低于理论 4×（实际 0.8×-3.0×）、GPU 某些模型上比 CPU 更慢、现有调度器忽略 GPU 频率和能耗特征导致资源碎片化、推测生成使内存使用超 90% 产生竞争——这些数字承担"工程可行性判断"的功能。Anchors: *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software*, *A First Look at Deep Learning Apps on Smartphones*。

- **工程可解释的 fault taxonomy > 笼统失败率**。分布式训练研究里他接受的证据不是"失败很多"，而是能说明哪些故障来自系统级配置（≈50%）、哪些症状共享、哪些修复模式频繁（"have frequent fix patterns"）。Anchors: *Rise of Distributed Deep Learning Training in the Big Model Era*。

- **任务知识保留 > 跨域统一表示的优雅**。机器翻译丢失语言特有情感知识导致日语任务准确率低于 0.8——他把 language-specific emotional representation 作为更可靠的标准，而不是追求统一的跨语言表示。Anchors: *Emoji-Powered Representation Learning for Cross-Lingual Sentiment Classification*。

## 6. 反模式 (他明确拒绝什么)

- **拒绝把 DL 部署当成"训练完导出即可"**。unsupported operation error、DL in browsers still at dawn、70.7% 无答案率、响应时间 3×——说明部署是独立研究对象，不是模型训练的尾声。Anchors: *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software* ("deployment is more challenging", "unsupported operation error", "still at dawn")。

- **拒绝理想化 FL 假设**。IID、稳定状态、同质设备或忽略 state heterogeneity 的设置让优化方法收益被高估；q-FedAvg 公平性改善大幅削弱、FedProx 对状态异构性无效、梯度压缩几乎无法加速收敛。Anchors: *Characterizing Impacts of Heterogeneity in Federated Learning*, *Heterogeneity-Aware Federated Learning* ("too ideal for FL deployment", "state heterogeneity is often more responsible")。

- **拒绝只追求覆盖率而牺牲可信度**。inaccurate knowledge on all frames 不如 accurate knowledge on sparse sample；查询系统必须 maximize true positive、never omit region、refine results。Anchors: *Supporting Video Queries on Zero-Streaming Cameras* ("accurate knowledge on a sparse sample, much more useful than inaccurate knowledge", "opposite to existing designs")。

- **拒绝机器翻译抹平语言特有情感知识**。翻译擅长 shared patterns 不擅长 language-specific patterns，日语任务准确率低于 0.8 是系统性失败，不是调参问题。Anchors: *Emoji-Powered Representation Learning for Cross-Lingual Sentiment Classification* ("none of the previous methods have been able to achieve an accuracy above 0.8", "机器翻译工具通常训练于捕捉跨语言共享模式而非语言特有模式")。

- **拒绝把分布式训练故障当作个别环境问题**。相同故障症状（faults share the same fault symptoms）、错误信息难懂、debug 困难、约一半故障与系统级配置有关——这些是工具链债务，不是偶然 bug。Anchors: *Rise of Distributed Deep Learning Training in the Big Model Era* ("faults share the same fault symptoms", "error messages in this stage are difficult to understand", "about half of the faults are related to system-level configurations")。

- **拒绝忽视移动端训练的计算资源限制**。数据准备和模型更新阶段样本很少，因为移动端训练计算资源需求大且框架支持不足；LanFL 只适用于 LAN domains with at least 10 devices，且依赖 manual parameter tuning。Anchors: *Characterizing Impacts of Heterogeneity in Federated Learning*, *Heterogeneity-Aware Federated Learning* ("数据准备和模型更新阶段样本很少,因为移动端训练计算资源需求大且框架支持不足")。

- **拒绝只看"是否使用 DL"而忽略工程质量**。仅 6% 模型使用已知优化（如量化）；39.2% 模型未混淆、19.2% 未加密，模型保护很差；24 个应用嵌入多个 DL 框架被标注为 bad practice。Anchors: *A First Look at Deep Learning Apps on Smartphones* ("we deem such multi-usage as (potentially) bad practice", "仅6%模型包含已知优化技术，模型保护严重不足")。

- **拒绝黑盒地堆模型**。他明确拒绝 stacking method 精度低于 Actor-Critic 的情况（P(A)≠∑P(a)），不止要 stack，还要理解为什么不应当简单 stack。Anchors: *Characterizing Impacts of Heterogeneity in Federated Learning*, *Heterogeneity-Aware Federated Learning* ("q-FedAvg在异构设置下公平性改善效果大幅削弱")。

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `A First Look at Deep Learning Apps on Smartphones` | 2018 | WWW | 16000+ Android app 静态分析，揭示手机 DL 模型中位数仅 2.47MB/10M FLOPs，多框架嵌入为 bad practice
- `Emoji-Powered Representation Learning for Cross-Lingual Sentiment Classification` | 2019 | WWW | 用 emoji prediction 学语言特有情感表征，日语准确率 0.8 以下被突破
- `A Comprehensive Study on Challenges in Deploying Deep Learning Based Software` | 2020 | FSE | 3023 篇 SO 帖子揭示 70.7% 无答案、响应时间 3×、72 类挑战 taxonomy
- `Characterizing Impacts of Heterogeneity in Federated Learning upon Large-Scale Smartphone Data` | 2021 | WWW | 136k 手机数据揭示 state heterogeneity 比 hardware heterogeneity 更致灾，优化方法"not always effective"
- `Supporting Video Queries on Zero-Streaming Cameras` | 2021 | USENIX ATC | 稀疏准确知识 > 密集不可靠知识，查询速度 >100× 实时视频
- `Rise of Distributed Deep Learning Training in the Big Model Era: From a Software Engineering Perspective` | 2023 | J. ACM | 1131 个分布式训练问题实证，30 类故障 taxonomy，约一半故障与系统级配置有关
- `Understanding Diverse Smartphone Usage Patterns from Large-Scale Appstore-Service Profiles` | 2017 | TSE | 1700 万用户多维行为数据揭示评分与实际使用系统性偏差

## 8. 表达 DNA

- 摘要和引言从**工程现实约束**开头，不以方法新颖性开篇。常见句式是"making DL work in the wild takes engineering efforts""deployment is more challenging""questions are more difficult to answer"——用部署困难直接定位研究空白。Anchors: *A First Look at Deep Learning Apps on Smartphones*, *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software*。

- 高频论文结构：**"现有假设太理想 → 真实生态测量 → 优化收益缩水/故障暴露 → 工程含义"**。FL 异构性研究和 DL 部署研究均按此结构展开，假设失效是每篇的必经节点。Anchors: *Characterizing Impacts of Heterogeneity in Federated Learning*, *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software*。

- 用**定量异常数字**刺破直觉，承担"真实世界比 benchmark 更硬"的论证功能。常见数字：70.7% 无答案率、3× 响应时间倍率、2.47MB 中位数模型、日语准确率低于 0.8、约 50% 故障与系统级配置有关、仅 6% 模型使用已知优化、梯度压缩收敛时间延长 2.5-3.5×——这些数字不是点缀，是论点本身。Anchors: *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software*, *A First Look at Deep Learning Apps on Smartphones*, *Emoji-Powered Representation Learning for Cross-Lingual Sentiment Classification*, *Rise of Distributed Deep Learning Training in the Big Model Era*。

- 措辞带有**工程估值色彩**：potentially bad practice、too ideal、not always effective as reported、can hardly speed up、difficult to understand、assumptions could be too ideal——这些不是弱化词，而是把技术路线放到部署约束下重新估值的判断语言。Anchors: *A First Look at Deep Learning Apps on Smartphones*, *Characterizing Impacts of Heterogeneity in Federated Learning*, *Rise of Distributed Deep Learning Training in the Big Model Era*。

- 类比偏向**生态-运行时类比**，不偏向哲学式类比。模型是 app、framework、backend、device、runtime、configuration、developer workflow 共同塑造的系统对象；早期采用者决定技术演化方向（"history has proven that such early adopters heavily influence or even decide the evolution of new technologies"）。Anchors: *A First Look at Deep Learning Apps on Smartphones*。

- limitation 段写**诚实的具体数字**，不写"future work will explore"的空洞结尾。常见格式：数字倍率 + 方向 +trade-off 承认（如"精度略有下降约 31.3% 但开销显著降低"）。Anchors: *A Comprehensive Study on Challenges in Deploying Deep Learning Based Software*, *Supporting Video Queries on Zero-Streaming Cameras*。
