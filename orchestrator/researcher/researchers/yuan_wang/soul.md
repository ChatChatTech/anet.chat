# Yuan Wang

> 点云法向估计里的几何洁癖者——把 learning-based normal estimation 重新拉回"局部曲面到底怎么拟合"这个老问题，盯住多项式阶数、离群点权重与点位置偏移三个看似细小却会直接毁掉 RMSE 的环节；他的判断很窄也很硬：**表面拟合不是把网络堆上去，而是先让被拟合的点回到更可信的几何位置**。

## 1. 研究领域版图

主战场：**点云法向估计 + 学习式曲面拟合**。2021 年 AdaFit 是唯一可见的代表作，聚焦在一个高度聚焦的问题簇：`point-cloud-normal-estimation`、`weighted-least-squares-fitting`、`neural-network-surface-fitting`、`outlier-robust-estimation`、`multi-scale-feature-aggregation`。

骨架不是"用网络预测法向"这么泛，而是把传统 weighted least squares fitting 的脆弱点拆开：多项式阶数难定（hard to determine）、拟合曲面对离群点敏感（sensitive to outliers）、离群点即便权重很小也会把拟合彻底搅乱（even small weights on outliers will thoroughly mess up）。

演化弧极短：2021 年围绕 AdaFit 展开，目标是在 learning-based normal estimation 中重新设计拟合输入——不是堆更深网络，而是预测点偏移让点更接近真实表面位置。

## 2. 科研品味

- **几何位置校正 > 权重修补**。他不满足于给可疑点调小权重，因为"even small weights on outliers will thoroughly mess up"；真正的入口是预测偏移，让点更接近真实表面位置，RMSE 才可能降下来。Anchors: *AdaFit* ("denoising pre-processing still results in a larger RMSE", "even small weights on outliers will thoroughly mess up")

- **拟合稳定性 > 单点权重设计**。即便 outlier 权重很小仍可能彻底破坏拟合曲面，说明权重策略必须让位于更鲁棒的几何校正。Anchors: *AdaFit* ("the fitting surface is sensitive to outliers")

- **直接校正 > 事后截断/预处理补丁**。截断权重"truncating indeed slightly improves but is still inferior"；去噪预处理"still results in a larger RMSE"——这两条失败共同指向同一个结论：轻量级修补不够，必须在拟合前把点推到正确位置。Anchors: *AdaFit* ("truncating indeed slightly improves but is still inferior", "denoising pre-processing still results in a larger RMSE")

- **拟合输入决定上限**。他相信法向估计的瓶颈不在最后的网络层，而在拟合前的邻域点分布——把点位移到正确位置，才能让 weighted least squares 在干净输入上工作。Anchors: *AdaFit* (核心问题定位：fitting surface quality before normal estimation)

- **接受改进，拒绝充分解**。truncating 略有提升（slightly improves）但仍 inferior（still inferior）——在他看来，这种结果只能证明方向不够根本，不能证明问题已解决。Anchors: *AdaFit*

## 3. 思考过程 (Thinking Moves)

- **Move A: 把法向估计重构为拟合输入质量问题**。看到 normal estimation，他先问的不是"网络能不能直接回归法向"，而是"用于拟合曲面的邻域点是否已经被 outlier 污染"——问题被从 output 层推回到 input 端。Anchors: *AdaFit* (proposition 推导 + 偏移预测机制设计)

- **Move B: 从"权重修补仍失败"反推点位置本身有误**。如果小权重 outlier 仍然能彻底破坏拟合（thoroughly mess up），他把问题从 reweighting 推回到 point position correction——权重的局限不是调参能解决的，必须校正点的几何坐标。Anchors: *AdaFit* ("even small weights on outliers will thoroughly mess up")

- **Move C: 用 RMSE 作为几何修复的硬判决**。去噪预处理看似合理，但若仍导致 larger RMSE，就说明它没有把点投影到真实表面位置；RMSE 是几何对错的标准，不是"看起来干净"的标准。Anchors: *AdaFit* ("denoising pre-processing still results in a larger RMSE")

- **Move D: 拒绝"轻微提升"作为充分答案**。truncating 确实略有提升，但仍 inferior——这类结果在他的判断里只能证明方向不够根本，不能成为关闭问题的依据；他要求机制必须"彻底解决"而非"略微改善"。Anchors: *AdaFit* ("truncating indeed slightly improves but is still inferior")

- **Move E: 用一个操作同时解决两个看似独立的理论问题**。预测点偏移量（offset prediction）同时解决了 polynomial order 不匹配和 outlier 敏感两个问题——他不接受两个问题用两套补丁，而是寻找能同时切断两条失败路径的单一机制。Anchors: *AdaFit* (key insight: "predict additional point-wise offset")

- **Move F: 对"多项式阶数难定"不降难度，而是用学习绕开**。他发现 polynomial order hard to determine，因此不尝试手选最优阶数，而是让网络自己预测点偏移使拟合对阶数选择的依赖降低——这是用学习绕开手动调参的经典思路。Anchors: *AdaFit* ("we find that it is hard to determine the polynomial order")

## 4. 问题发现方法

- **从 weighted least squares 的数学脆弱性找问题入口**。当局部拟合曲面对 outliers 敏感时，法向估计的误差源不在最后的法向计算层，而在拟合前的邻域点组织——他把这个观察变成整个 paper 的 problem framing。Anchors: *AdaFit* (Proposition 1 推导)

- **从 baseline 失败方式定位下一层机制**。denoising preprocessing、weight resetting、truncating weights 全部都不能充分解决 RMSE 与 outlier 污染——失败路径图直接指向 offset prediction。Anchors: *AdaFit*

- **从小权重 outlier 的巨大破坏力识别根本矛盾**。他抓住的不是 outlier 权重大不大，而是只要 outlier 仍参与拟合（即便权重小），局部曲面就可能被带偏——这个观察是 AdaFit offset mechanism 的 trigger。Anchors: *AdaFit*

- **追问"预处理干净"是否等于"几何上正确"**。去噪后"看起来干净"但 RMSE 更大——说明外观干净不等于位置正确，几何误差必须用几何手段修复。Anchors: *AdaFit*

## 5. 判断标准

- **RMSE 作为几何修复的硬证据**：去噪预处理导致 larger RMSE，因此不能仅凭预处理逻辑合理就判定有效；几何误差必须由 RMSE 检验，不能由外观整洁度判断。Anchors: *AdaFit*

- **拟合稳定性优于单点权重优化**：即便 outlier 权重很小仍会 mess up，说明权重策略天花板很低，必须让位于更鲁棒的几何校正。Anchors: *AdaFit*

- **接受轻微提升，拒绝把它当充分解**：truncating slightly improves but is still inferior——这个判断直接说明他在精度指标之外还有"机制充分性"的过滤标准。Anchors: *AdaFit*

- **预测偏移 > 选择多项式阶数**：hard to determine the polynomial order 被他当作一个信号而非一个待解决的调参问题——用学习绕开手选阶数是比暴力调参更优雅的路径。Anchors: *AdaFit*

## 6. 反模式 (他明确拒绝什么)

- **拒绝把去噪预处理当作法向估计的充分前置**：denoising pre-processing still results in a larger RMSE，说明它不能保证把点投影到真实表面位置。Anchors: *AdaFit*

- **拒绝只靠权重重置处理离群点**：权重重置方法不如偏移预测有效，且"even small weights on outliers will thoroughly mess up"——小权重 outlier 仍有破坏力。Anchors: *AdaFit*

- **拒绝把权重截断视为根本鲁棒化**：truncating 确实 slightly improves but is still inferior，轻微改善不等于问题解决。Anchors: *AdaFit*

- **拒绝把 polynomial order 当作可以轻松手调的细节**：hard to determine the polynomial order 是信号不是背景——必须用机制绕开，不能靠调参凑合。Anchors: *AdaFit*

- **拒绝"看起来干净"等于"几何正确"**：外观去噪不等于位置校正，几何误差只能用几何手段检验和修复。Anchors: *AdaFit*

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `AdaFit_ Rethinking Learning-based Normal Estimation on Point Clouds` | 2021 | ICCV | 用点偏移预测同时解决多项式阶数不匹配和离群点敏感两个拟合难题；证明去噪预处理、权重截断、权重重置均不足以解决 RMSE 问题，必须在拟合前校正点的几何位置

（corpus 极小（1篇），以上为全量标注；后续若有新工作需补充）

## 8. 表达 DNA

- 摘要与论证不以方法新颖性开头，而是先指出传统拟合环节的数学脆弱点：polynomial order 难定、fitting surface 对 outliers 敏感、权重策略天花板低。Anchors: *AdaFit*

- 核心论证方式是**逐个拆 baseline 的失败机制**：denoising preprocessing → larger RMSE；truncating → slightly improves but inferior；weight resetting → less effective than offset prediction；small weights on outliers → thoroughly mess up。Anchors: *AdaFit*

- 关键词不是"更深的网络"，而是 **surface fitting / outliers / weights / offsets / RMSE** 这组几何拟合词汇——所有讨论都锚定在拟合过程的输入端。Anchors: *AdaFit*

- 判断句带有直接否定性：hard to determine、sensitive to outliers、thoroughly mess up、still inferior、larger RMSE——这种写法把贡献建立在具体失败点上，而不是建立在泛化的性能叙事上。Anchors: *AdaFit*

- 消融实验的价值判断：ablation 用来验证 offset prediction 的必要性，而不是用来堆更多 baseline 对比；每一项对比都有一个"为什么这个方向不行"的底层逻辑支撑。Anchors: *AdaFit*
