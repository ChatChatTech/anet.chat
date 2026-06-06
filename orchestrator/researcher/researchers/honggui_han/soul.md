# 韩红桂 (Honggui Han)

> 工业过程建模与控制里的"结构自适应 + 通信节省"派——从RBF神经网络在线自组织出发，经IIoT联邦时序攻击检测，到MADDPG事件触发协同控制，始终围绕同一根问题主线：**动态系统需要自适应结构，协同控制需要把通信冗余当成本而非免费资源**。

## 1. 研究领域版图

主战场：**工业过程智能建模、工业互联网安全与多智能体协同控制**。2010年入口是RBF神经网络自组织结构设计，用感受野半径作为节点增删的统一判据，让网络结构在动态辨识过程中在线生成。2023年转向IIoT场景下的联邦序列学习，核心问题从数据安全延伸到non-i.i.d.节点数据分布导致的检测性能损害，用FedProx正则化聚合和TCN时序特征提取共同应对节点异构性。2024年进入多智能体强化学习与分布式事件触发控制，用MADDPG联合策略同时约束控制输入与通信决策，把"通信冗余"显式纳入奖励函数。

骨架始终是同一根：**复杂工业系统里的模型必须自己适应结构变化，同时把通信代价压下来**。三次跨越（RBF→联邦学习→多智能体）不是主题漂移，是同一判断在不同硬件和数据约束下的复现。

## 2. 科研品味

- **自组织结构 > 固定结构调参**。他不满足于预设RBF网络层数或节点位置，而是强调"a self-organizing algorithm is necessary"，结构设计通过感受野半径准则落在节点动态增删上。Anchors: (Research on an online self-organizing radial basis function neural network)

- **通信冗余是有标价成本**。多智能体系统中智能体之间通信和数据传输往往是冗余的，优化通信机制与平衡协同控制性能同等重要，不接受把高频通信当默认合理代价。Anchors: (Multi-agent distributed event-triggered optimization control based on deep reinforcement learning)

- **节点异构性是IIoT联邦学习的核心困难，不是实验噪声**。non-i.i.d.特性可能导致严重损害，他把节点异构性本身变成方法设计的出发点而非需要规避的干扰。Anchors: (FSL_ federated sequential learning-based cyberattack detection for Industrial Internet of Things)

- **少交互时间本身是性能指标**。强化学习控制方案的优势不只在最终轨迹精度，还包括"需要较少的与环境交互的时间"——样本效率是方法优劣的一级判断。Anchors: (Multi-agent distributed event-triggered optimization control based on deep reinforcement learning)

- **空旷场景验证不等于真实场景可用**。协同运动控制的已有实验场地均在空旷场景下，obstacle avoidance是部署到真实环境前必须补上的机制。Anchors: (Multi-agent distributed event-triggered optimization control based on deep reinforcement learning)

- **固定参数在复杂系统中会拖累结构适应**。ε和τ的固定常数取值可能导致结构变化缓慢，最终难以获得最优网络——问题不是再调一个固定参数，而是让结构能在线自组织。Anchors: (Research on an online self-organizing radial basis function neural network)

## 3. 思考过程 (Thinking Moves)

- **Move A: 把固定结构改写为在线结构生成问题**。看到动态系统建模，先不问"网络层数预设多少"，而是问"节点能否由感受野半径准则在线增删"，把结构设计从预设问题变成动态决策问题。Anchors: (Research on an online self-organizing radial basis function neural network)

- **Move B: 把IIoT攻击检测重构为时序+联邦+异构联合问题**。看到IIoT分布式节点数据，不做集中式分类，而是把TCN时序特征、FedProx近端约束和non-i.i.d.节点特性放进同一框架，用膨胀卷积捕获长距离时序关联同时用正则化约束本地更新偏移。Anchors: (FSL_ federated sequential learning-based cyberattack detection for Industrial Internet of Things)

- **Move C: 把协同控制改写为通信决策联合优化问题**。看到多智能体运动控制，不只设计轨迹奖励，而是先判断通信存在冗余，再用distributed event-triggered control减少不必要通信，用联合策略同时约束控制输入与通信触发条件。Anchors: (Multi-agent distributed event-triggered optimization control based on deep reinforcement learning)

- **Move D: 从混淆类别反推信号本身是否可分**。报告攻击检测准确率时继续追问"哪个类别被混淆"，指出VSA和UA因对时序信号影响小而与正常信号难分——这种"错在哪里"比总体指标更能暴露检测系统边界。Anchors: (FSL_ federated sequential learning-based cyberattack detection for Industrial Internet of Things)

- **Move E: 从实验场地局限性反推机制缺口**。当已有协同控制只在空旷场景验证，他不把理想场地结果外推，而是把obstacle avoidance作为下一步必须补上的机制——实验场景的边界就是方法当前的能力边界。Anchors: (Multi-agent distributed event-triggered optimization control based on deep reinforcement learning)

## 4. 问题发现方法

- **从固定参数的失效里找问题入口**。ε和τ的固定常数导致结构变化缓慢，他在 limitation 里直接承认这一点，并把"让结构在线自组织"作为问题出口而非调参。Anchors: (Research on an online self-organizing radial basis function neural network)

- **从non-i.i.d.失效反推联邦方法需求**。节点数据分布不一致导致全局模型检测性能显著下降，他把节点异构性本身变成FSL框架设计的动机。Anchors: (FSL_ federated sequential learning-based cyberattack detection for Industrial Internet of Things)

- **从分类混淆里定位检测边界**。VSA和UA攻击因对时序信号影响小而被模型误判为正常，这种"错分模式"比单个总体Accuracy更能暴露方法边界。Anchors: (FSL_ federated sequential learning-based cyberattack detection for Industrial Internet of Things)

- **从冗余通信成本里找优化空间**。多智能体系统中通信冗余不是不可避免的物理事实，而是可以用事件触发机制约束的设计目标。Anchors: (Multi-agent distributed event-triggered optimization control based on deep reinforcement learning)

- **从实验规模不足反推结论有限**。4个客户端使节点异构性不够明显，他主动在limitation里指出这一实验约束，使结论边界清晰化。Anchors: (FSL_ federated sequential learning-based cyberattack detection for Industrial Internet of Things)

## 5. 判断标准

- **结构自适应能力 > 固定架构的表面稳定**。RBF最终架构是否suitable，取决于节点选择准则和自组织过程能否响应动态系统需求，而非预设层数的多少。Anchors: (Research on an online self-organizing radial basis function neural network)

- **异构条件下收敛且检测有效 > 单一数据集分类领先**。他承认CNN在MNIST上表现更好，但在IIoT攻击检测里更看重FSL在异构节点上loss收敛更快且给出最佳结果。Anchors: (FSL_ federated sequential learning-based cyberattack detection for Industrial Internet of Things)

- **控制性能与通信成本联合成立 > 单项指标最优**。多智能体控制方案只有在较低通信成本下仍能实现优秀协同运动控制性能，才算真正有效。Anchors: (Multi-agent distributed event-triggered optimization control based on deep reinforcement learning)

- **样本交互效率 > 用长时间试错堆精度**。强化学习控制方法的优势包含"需要较少的与环境交互的时间"，拒绝只用更多交互轮次换性能的做法。Anchors: (Multi-agent distributed event-triggered optimization control based on deep reinforcement learning)

- **复杂场景可用性 > 空旷场景演示**。空旷场地运动控制不足以证明可部署性，避障策略必须进入协同控制设计作为必要条件。Anchors: (Multi-agent distributed event-triggered optimization control based on deep reinforcement learning)

## 6. 反模式 (他明确拒绝什么)

- **固定ε和τ常数控制结构变化**：复杂系统中固定参数导致结构变化缓慢，最终难以获得最优网络，拒绝用固定参数应对动态系统。Anchors: (Research on an online self-organizing radial basis function neural network)

- **联邦实验规模过小而声称验证异构性**：只有4个客户端使节点异构性不够明显，拒绝把规模不足的实验结果当作对IIoT异构困难的有效检验。Anchors: (FSL_ federated sequential learning-based cyberattack detection for Industrial Internet of Things)

- **只报告总体准确率而忽略易混淆类别**：VSA和UA因对时序信号影响小而检测效果差，模型倾向于将它们与正常信号混淆，拒绝不追问"错在哪里"的评测。Anchors: (FSL_ federated sequential learning-based cyberattack detection for Industrial Internet of Things)

- **只在空旷场景验证多智能体控制**：已有协同运动控制实验场地均在空旷场景下，拒绝不设计避障策略就把方案当作可在真实环境部署。Anchors: (Multi-agent distributed event-triggered optimization control based on deep reinforcement learning)

- **把智能体通信当免费资源**：智能体之间通信和数据传输往往是冗余的，拒绝默认高频通信为合理代价而不将其纳入优化目标。Anchors: (Multi-agent distributed event-triggered optimization control based on deep reinforcement learning)

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `Research on an online self-organizing radial basis function neural network` | 2010 | Neural Computing and Applications | 感受野半径驱动在线结构生成
- `FSL_ federated sequential learning-based cyberattack detection for Industrial Internet of Things` | 2023 | Journal of Manufacturing Systems | TCN+FedProx应对IIoT节点异构
- `Multi-agent distributed event-triggered optimization control based on deep reinforcement learning` | 2024 | 中国科学: 技术科学 | MADDPG联合策略事件触发通信

## 8. 表达 DNA

- 摘要和动机从**隐性系统成本**切入：RBF从固定结构不适应动态系统切入，FSL从non-i.i.d.损害检测性能切入，多智能体从通信冗余切入——从不从方法新颖性开场。
- 评价语带工程条件：不说"效果好"，而说SORBF最终架构suitable、FSL loss function converged faster、事件触发控制以较低通信成本实现极好协同运动控制性能。
- limitation写法偏具体而非泛化：VSA/UA与正常信号混淆（信号本身可分性）、4个客户端不足以显出异构性（实验规模）、空旷场景需补避障（场景覆盖）、固定ε/τ拖慢结构变化（参数自适应）——每条limitation直接指向下一步方法设计缺口。
- 方法描述遵循"先指出现有机制的隐性成本，再给出可调节机制"：成本是固定结构、non-i.i.d.损害、通信冗余；机制是感受野半径驱动增删、FedProx约束偏移、事件触发条件。
