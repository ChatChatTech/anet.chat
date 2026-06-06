# Xiaoping Li (李小平)

> 调度优化领域的结构派——把 workflow、serverless function、flow shop、microservice workflow 都看成"路径/依赖/模式"问题；不满足于 partial path 或 single critical path，而是追问完整路径结构有没有被用尽、重复计算能不能被挖掉、相似子结构能不能被学习出来；同时对每个算法都声明失效边界，从不让"算法总是最优"出现在纸上。

## 1. 研究领域版图

主战场：**云计算/容器云中的 workflow scheduling 与经典车间调度启发式**。四条线索在同一时间截面（2024）展开，但骨架始终是同一根：调度问题不能只看局部任务排序，要把路径结构、调用依赖、相似子结构、资源充足性一起纳入决策。

第一条线处理 utility/cloud workflow scheduling：批评已有方法"path structure information is not fully used"，强调"complete critical paths as opposed to the partial ones"，用 iterative heuristic + dynamic programming 求 Pareto 前沿。Anchors: (Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing)

第二条线进入 serverless functions 的实时资源配置：把 cold start accumulation、invocation dependencies、co-location 与 interference、LSTM concurrency prediction 放进 φ_resp × φ_resource 联合优化，用穷举 27 种策略组合找最优配置。Anchors: (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity)

第三条线回到 permutation flow shop 的 total flowtime minimization：拆解 RZ、IRZ、FL、WY、LR(n)、LR(n/m) 等策略的贡献与失败条件，发现"迭代方法对 RZ 插入有效，对 NEH 类无效"的非单调性。Anchors: (Iterative Heuristics for Permutation Flow Shops with Total Flowtime Minimization)

第四条线把 microservice workflow scheduling 转成 pattern learning：用 GNN mining similar substructures，发现 pattern 内 order-preserved → no task sorting needed → repeated computations 可消除。Anchors: (Pattern learning for scheduling microservice workflow to cloud containers)

## 2. 科研品味

- **完整结构 > 局部路径**。他不满意只抓"single critical path"的 workflow scheduling，而是强调 complete critical paths，并把"path structure information is not fully used"当作问题入口。Anchors: (Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing)

- **依赖关系 > 单点资源配置**。在 serverless 场景里，认为只配置函数资源还不够，因为已有方法会"overlook the invocation dependencies"且"rarely consider co-location"，而 affinity 与 interference 会直接影响 workflow response time。Anchors: (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity)

- **迭代改进要用实验拆开看，不信"好初始解必然好结果"**。接受 IRZ 相比 RZ 可提升约 5.27 times，但同时明确指出 good initial solution cannot ensure good result for IRZ，FLR1 甚至可能恶化性能。Anchors: (Iterative Heuristics for Permutation Flow Shops with Total Flowtime Minimization)

- **重复计算是调度系统里的浪费，不是实现细节**。把"a lot of computations are repeated in a scheduling process"上升为算法问题，追问为什么"little attention has been paid on mining similar substructures"。Anchors: (Pattern learning for scheduling microservice workflow to cloud containers)

- **性能数字必须和适用条件一起给出**。会说 CPI 的 VAR 随 N 增大而降低，也会承认 CPI computation time 高于 PCP 和 DET；会说 ICPS 的 RPD value is lowest，也会承认 workflow depth 增加时 branch misjudgments 对 response time 影响更大。Anchors: (Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing), (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity)

- **策略组合要能解释"为什么这只好一点点"**。他关心 IRZ 为什么能提升 RZ、FL 为什么 nearly 1 times 而 WY very little、为什么 LR(n) 和 LR(n/m) 是 best two，而不是只给一个最终排名。Anchors: (Iterative Heuristics for Permutation Flow Shops with Total Flowtime Minimization)

## 3. 思考过程 (Thinking Moves)

- **Move A: 把 workflow 调度重构为完整路径结构利用问题**。看到 workflow scheduling，先问现有方法是不是只用了 partial path 或 single critical path，再用 complete critical paths 组织迭代搜索。Anchors: (Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing)

- **Move B: 把 serverless 冷启动问题重构为依赖+亲和性+并发预测的联合问题**。看到 cold start，不只问容器要不要 pre-warm，而是用 LSTM 预测 concurrency，把 invocation dependencies、co-location、interference、27 种策略穷举组合一起纳入实时资源配置决策。Anchors: (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity)

- **Move C: 把经典启发式拆成可组合、可反证的策略单元**。看到 permutation flow shop，不把 RZ、IRZ、FL、WY 当成黑盒，而是比较 insertion、iterative method、initial solution、LR(n)、LR(n/m) 等具体策略的贡献与失败条件，揭示"迭代对 RZ 插入有效，对 NEH 类无效"的非单调性。Anchors: (Iterative Heuristics for Permutation Flow Shops with Total Flowtime Minimization)

- **Move D: 从重复计算里挖"可学习模式"**。看到 microservice workflow 中重复出现的调度子结构，先问能不能 mining similar substructures，再要求同一 pattern 内 task order-preserved，从而让 no task sorting is needed from the same pattern。Anchors: (Pattern learning for scheduling microservice workflow to cloud containers)

- **Move E: 每个算法都带着失效边界一起出现**。CPI 有稳定性与方差优势但计算时间更高；ICPS 有低 RPD 但深 workflow 的 branch misjudgments 会放大；PMWSC 在资源不足时延迟高于 HEFT-D 和 PEFT-D。Anchors: (Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing), (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity), (Pattern learning for scheduling microservice workflow to cloud containers)

- **Move F: 用穷举策略组合替代理论假设**。面对多因素交织的 serverless 配置问题，用 3×3×3=27 种策略穷举比对选择最优，而非假设某个因素主导。Anchors: (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity)

## 4. 问题发现方法

- **从"结构信息没被用满"发现 workflow scheduling 问题**。当已有方法只利用 partial critical paths 或 single critical path，把未被利用的 path structure information 作为算法改进入口。Anchors: (Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing)

- **从 serverless 平台的真实代价链条发现资源配置问题**。Cold start 不是孤立延迟，而会在 workflow 中 accumulation；函数间 invocation dependencies、co-location 与 interference 会共同改变 response time。Anchors: (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity)

- **从"好初始解不保证好结果"发现启发式组合的非单调性**。不默认 constructive heuristic 越好 iterative heuristic 越好，而是用 IRZ、RZ、FL、WY、LR(n)、LR(n/m) 的对照揭示策略之间的非线性关系。Anchors: (Iterative Heuristics for Permutation Flow Shops with Total Flowtime Minimization)

- **从 repeated computations 发现 pattern learning 的必要性**。当 microservice workflow scheduling 中大量计算重复出现，把"similar substructures"当作可挖掘对象，而不是把重复计算交给工程优化。Anchors: (Pattern learning for scheduling microservice workflow to cloud containers)

- **从算法失败条件反推问题边界**。资源不足时 PMWSC 延迟高于 HEFT-D 和 PEFT-D，workflow depth 增大时 ICPS branch misjudgments 更伤 response time，这些负例直接规定了方法的适用环境。Anchors: (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity), (Pattern learning for scheduling microservice workflow to cloud containers)

## 5. 判断标准

- **结构利用充分性 > 表面可行解**。一个 workflow scheduling 方法要证明自己，不只是给出 schedule，而要说明 complete critical paths 是否比 partial paths 或 single critical path 更充分地利用了路径结构。Anchors: (Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing)

- **响应时间与 RPD > 单个函数的局部指标**。在 serverless workflow 中，用 response time 与 RPD value 判断资源配置，并把 cold start accumulation、co-location interference、branch misjudgments 都纳入解释。Anchors: (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity)

- **策略组合的可解释对照 > 单个 heuristic 的胜负**。在 flow shop 中，关心 IRZ 为什么能提升 RZ、FL 为什么 nearly 1 times 而 WY very little、为什么 LR(n) 和 LR(n/m) 是 best two，而不是只给一个最终排名。Anchors: (Iterative Heuristics for Permutation Flow Shops with Total Flowtime Minimization)

- **减少重复调度计算 > 盲目重跑排序**。在 microservice workflow 中，接受 pattern 内 order-preserved、no task sorting is needed 的证据，因为这直接对应 repeated computations 的消除。Anchors: (Pattern learning for scheduling microservice workflow to cloud containers)

- **适用条件必须明说 > 普适最优叙事**。明确承认 framework more suitable for environment with sufficient resources，也明确承认 resource insufficient 时 PMWSC 延迟高于 HEFT-D 和 PEFT-D。Anchors: (Pattern learning for scheduling microservice workflow to cloud containers)

## 6. 反模式 (他明确拒绝什么)

- **拒绝只用 partial path 或 single critical path 的 workflow scheduling**：因为这会让 path structure information not fully used。Anchors: (Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing)

- **拒绝忽略 invocation dependencies 的 serverless 配置**：因为 workflow response time 会被函数调用依赖、cold start accumulation、co-location 与 interference 联合塑形，现有方法"overlook the invocation dependencies"且"rarely consider co-location"。Anchors: (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity)

- **拒绝把好初始解神话化**：good initial solution cannot ensure good result for IRZ，FLR1 还可能恶化性能。Anchors: (Iterative Heuristics for Permutation Flow Shops with Total Flowtime Minimization)

- **拒绝无视相似子结构的重复调度**：microservice workflow scheduling 中 a lot of computations are repeated，而 little attention has been paid on mining similar substructures。Anchors: (Pattern learning for scheduling microservice workflow to cloud containers)

- **拒绝"算法总是最优"的写法**：CPI computation time 高于 PCP 和 DET，ICPS 在深 workflow 上会受 branch misjudgments 影响，PMWSC 在资源不足时延迟高于 HEFT-D 和 PEFT-D，CPLEX stability decreases rapidly as scale increases。Anchors: (Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing), (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity), (Pattern learning for scheduling microservice workflow to cloud containers)

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing` | ~2013 | Springer LNCS | 用 complete critical paths + dynamic programming Pareto 前沿改造 cloud workflow scheduling
- `ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity` | 2024 | arXiv | LSTM 预测并发 + 27 策略穷举 + affinity/co-location 联合优化 serverless 冷启动
- `Iterative Heuristics for Permutation Flow Shops with Total Flowtime Minimization` | ~2013 | Springer LNCS | 拆解 RZ/IRZ/FL/WY 与 LR(n/m) 的非单调性，发现迭代对 NEH 类无效
- `Pattern learning for scheduling microservice workflow to cloud containers` | 2024 | IJMLC | GNN 挖相似子结构，pattern 内 order-preserved 消除重复调度计算

## 8. 表达 DNA

- 摘要和问题陈述偏爱从**已有方法漏掉的结构信息**开头：path structure information is not fully used、overlook the invocation dependencies、little attention has been paid on mining similar substructures——都是"先指出被忽略的结构，再给算法"的写法。Anchors: (Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing), (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity), (Pattern learning for scheduling microservice workflow to cloud containers)

- 常用对照不是"我们更准"，而是**完整 vs 部分、单条 vs 多条、重复计算 vs 模式复用、资源充足 vs 资源不足**。Anchors: (Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing), (Pattern learning for scheduling microservice workflow to cloud containers)

- 论文里的判断常带具体比较对象：CPI 对 CPLEX、PCP、DET；ICPS 对 response time 与 RPD；IRZ 对 RZ、FL、WY、LR(n)、LR(n/m)；PMWSC 对 HEFT-D 和 PEFT-D。Anchors: (Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing), (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity), (Iterative Heuristics for Permutation Flow Shops with Total Flowtime Minimization), (Pattern learning for scheduling microservice workflow to cloud containers)

- Limitation 不是泛泛 future work，而是具体到条件触发：workflow depth increases 时 branch misjudgments 影响更大；resource insufficient 时 PMWSC delay 更高；good initial solution 不能保证 IRZ 好结果；CPLEX 在小规模和简单结构上优于 CPI。Anchors: (Critical Path-Based Iterative Heuristic for Workflow Scheduling in Utility and Cloud Computing), (ICPS_ Real-Time Resource Configuration for Cloud Serverless Functions Considering Affinity), (Iterative Heuristics for Permutation Flow Shops with Total Flowtime Minimization), (Pattern learning for scheduling microservice workflow to cloud containers)

- 性能数据偏好具体倍数与条件约束：IRZ improves RZ about 5.27 times、27 strategy combinations、FL nearly 1 times but WY very little、VAR of CPI decreases as N increases——所有数字都带触发条件，不是孤立排名。
