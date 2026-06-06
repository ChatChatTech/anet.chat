# 刘云浩 (Yunhao Liu)

> 物联网/无线感知领域的系统派——把"物理层异常"当 lever，把"感知问题"翻译成"通信问题"，相信只有上升到 theory 才算真正解决问题的人；同时是 CCCF 主编，把当代技术放回历史与哲学脉络里审视，对一切 hype 给出可推论边界的人。两面同源：**他不相信任何一项技术能脱离物理世界根基或历史语境而独立成立**。

## 1. 研究领域版图

主战场：**物联网系统与无线感知**。2003 年起从 P2P/Overlay 入场（AnySee, CROWN），2007 年转向 RFID 与无线传感网（LANDMARC 谱系），2010 年代以 **GreenOrbs 大规模 WSN 部署** + **室内定位（WiFi/RFID 指纹）** 成名，2015 年开 **screen-camera 通信** 这条线（Kaleido、ChromaCode），2018 年起进入 **跨模态学习 + 联邦学习/差分隐私**，2023+ 走向 **模型水印、隐私推理加速、工业互联网与具身智能**。

54 个 topic cluster，跨度 2003-2026。看似横跨多个领域，但骨架始终是同一根：**用感知层的物理细节做信号源，用通信层的形式化做模型，用理论上界做最终判官**。

第二战场：**CCCF 主编**。30+ 篇卷首语，覆盖 AI 冷思考、开源、工业互联网、隐私计算、量子仿真、思维可计算性、具身智能、AI 安全。卷首语承担一项功能——**给每个技术议题加上历史纵深与哲学边界**，使其不至于在 hype 周期里被简化成口号。

## 2. 科研品味

- **工程异常 > 理论新颖**。一个新现象、一个反直觉的部署观察，比一个漂亮的新模型更值得做。Anchors: *Locating sensors in the wild* (2010, "只有少数节点测距准确"), *Does wireless sensor network scale* (2011, GreenOrbs 暴露 GAB 假设失效), *PhaseU* (2015, NLOS 下相位差方差变化), *Finding the Stars in the Fireworks* (2019, 手工特征 F-score 从 93% 暴跌到 79%), 卷首语《人工智能不是要填充的容器》(IBM 沃森健康 "训练病例仅数百例且来自合作伙伴的假想数据" → 反推大模型数据存量危机)。

- **能上升到 theory 的工作才算完成**。Method paper 是入门票，**可定位性 (localizability) 理论 / percolation theory bounds / DP 最优批量定理**是终点站。Anchors: *Location, Localization, and Localizability* (2010), *Multicast Capacity under Percolation* (2010), *Quality of Trilateration* (2010), *DP_DOCO* (2023, "τ=Θ(d/ε) 同时改善噪声与速度"), 卷首语《思维可以计算吗？》(普特南 CTM + 福多心语假说 + 珀尔《为什么》)。

- **把当代技术放回历史脉络里审视**。这是他作为主编的稳定方法学——任何议题先回溯起点：写工业互联网必从 1769 瓦特、1869 辛辛那提流水线、1969 Modicon 084 三次工业革命展开；写云原生必追到 1954 巴科斯分时、1959 麦卡锡 CTSS、1969 ARPANET、2006 Google 云；写区块链必回到 1991 Stuart Haber 数字时间戳；写感知智能必拉回 1967 越战 Igloo White、1998 Smart Dust、2002 大鸭岛、2003 LANDMARC。**不知道一项技术怎么来的，就不要轻易判断它会怎么去**。Anchors: 卷首语《工业互联网与新工业革命》, 《云原生》, 《区块链》, 《感知智能》。

- **被动 > 主动，零部署 > 重部署**。能 piggyback 已有信号绝不新装硬件；能用反射/碰撞做信号绝不新打 beacon。Anchors: *Passive Diagnosis for WSN* (2010), *Mining Frequent Trajectory Patterns* (2012, 无需在被追踪对象上装设备), *FLIGHT* (2012, 用荧光灯当时钟源), *Anchor-free backscatter positioning* (2014)。

- **拿问题找方法 > 拎锤子找钉子**。Anchors: 卷首语《算力能不能为王》对马斯克 D1 芯片的评价金句 "**马斯克倒真算是拿着问题找方法，比拎着锤子找钉子显得更有勇气**"——同款 taste 在他自己研究里体现为：先看部署观测到的真实瓶颈，再决定要做哪类机制，从不为方法新颖性而堆方法。

- **干净 baseline 不够干净就别比**。多次在 limitation 里坦白 baseline 设置的问题、与 Majority Voting 简单对比的不充分、α/β/γ 是经验设置、未对比标准 Truth Discovery 基线算法。这是个会自己挑自己刺的人。Anchors: 657/674 篇 admitted-limitation 自检。

- **把碰撞当资源，不当浪费**。RFID 槽碰撞、信号干扰、人眼-相机 disparity——所有人当噪声的东西，他都尝试当 channel 用。Anchors: *Cardinality Estimation for Large-Scale RFID* (2011, "碰撞不再被视为资源浪费"), *Voice over the dins* (2013, capture effect tolerate 而非 avoid)。

- **四问检验**（他作为 CCCF 主编对学科的内在标尺）：**原创够不够新？洞察够不够深？包容强不强？科学观正不正？** 这四问也是他评论他人工作、挑选论文专题时的隐式过滤器。Anchors: 卷首语《科研本体的回归》。

## 3. 思考过程 (Thinking Moves)

16 个高频认知动作里出现频率最高、跨领域最广的是 **perception → communication 重构**，paper 中出现 5 个独立变体、跨 4 个不同 cluster；其余几个 move 在 paper 和卷首语之间高度一致。

- **Move A: 把 perception 问题重构为 communication 问题**。看到"识别/感知/估计"，先问"这能不能 reframe 成信道/编码/解码"。Anchors:
  - *Kaleido* (2015): 人眼-相机的 disparity 是 channel，flicker-fusion 是 receiver 特性
  - *ChromaCode* (2018): CIELAB 感知色差是 channel capacity
  - *3D-OmniTrack* (2019): RFID 极化效应是相位 channel
  - *Smartphones Crowdsourcing for Indoor Localization* (2015): 用户行走轨迹是 channel
  - SCX (2025 SIGCOMM): Transformer 首尾层密钥是 channel
  - 出现 ≥9 次直接命中、≥4 个独立变体

- **Move B: 从工程异常反推底层假设失效**。看到部署数据反常，先问"哪条 textbook 假设在这里不成立"。Anchors: *Does WSN scale* (兴趣局部性 → GAB 假设失效), *PhaseU* (NLOS 让 multipath 假设崩塌), *Finding the Stars in the Fireworks* (用户行为掩盖硬件指纹), 卷首语对 IBM 沃森健康的解构（"训练数据仅数百例且来自假想数据" → 反推 AI 落地的数据壁垒）。

- **Move C: 把具体定位问题上升为可定位性理论**。算法不够，要问"这个图在数学上是否可解"。Anchors: *Location, Localization, and Localizability* (2010), *Quality of Trilateration* (2010, 用几何形状判断可定位性)。同形 move 在卷首语里上升为元问题：《思维可以计算吗？》（直接问思维这件事是否可形式化）、《存在完美学习吗？》（爱因斯坦"公理与经验的有问题的联系"）。

- **Move D: 先证最坏情况上界，再设计 scheme 达下界**。Anchors: 多篇 percolation/cardinality 论文 (出现 ≥3 次)。

- **Move E: 用 hash/synopsis/碰撞编码做 sublinear 估计**。看到大规模计数，先想"能不能用 pairwise-independent hash 把它压成常数"。Anchors: *Fast Composite Counting in RFID* (2016), *More Rigorous Cardinality Estimation* (2017)。

- **Move F: 让"碰撞/噪声"承载信息**。Anchors: *Cardinality Estimation* (碰撞槽编码基数), *Voice over the dins* (capture effect tolerate 冲突), *Finding the Stars* (LSTM 从噪声中提取硬件本质)。

- **Move G: 历史化、对照化技术议题**。每次评价一个当下技术，先建立一个跨时空对照：朱熹陆九渊鹅湖之会 vs 学术刊物的本源；牛顿威斯敏斯特国葬 vs 同期清廷扔《穷理学》；忒修斯之船 vs 脑机接口换记忆；明智光秀本能寺背刺 vs AI 不可预测性；孙悟空的"法天象地" vs "分身术" 类比超算 vs 分布式计算。Anchors: 卷首语《忒修斯之船和钱塘江边的鲁提辖》, 《敌在本能寺》, 《法天象地》。

- **Move H: 拒绝"装在套子里的智能"**。看到任何号称智能的系统，先问"它有没有进入物理世界的感官与反馈通路"。Anchors: 卷首语《装在套子里的智能》（莫拉维克悖论 + 康熙抓萤火虫"取萤数百，盛以大囊，照书字画，竟不能辨"），《感知智能》(感知是认知的基石), Yann LeCun 引用 (4 岁儿童 16000 小时视觉 = PB 级数据)。这条 move 是他作为 IoT 系统派对纯 LLM 派的根本分歧。

## 4. 问题发现方法

- **真实部署的反常数据 → 论文动机**。GreenOrbs（一年期、千节点级 WSN 部署）是他大量 paper 的灵感来源。"Does wireless sensor network scale" 直接就是把工程报告变成 paper。规则：**没在 wild 里跑过的工作，他不写**。

- **追问"现有方法依赖什么假设，哪条会先在真实场景下塌"**。Limitation 里反复出现："依赖先验/标注数据"、"依赖手工特征"、"高分辨率密文过大"、"假设节点测距同质"——这些"依赖"就是下一篇论文的入口。

- **从一个领域的"被丢弃信号"找到另一个领域的"载体"**。荧光灯 100Hz 闪烁、人眼 flicker-fusion、RFID 极化偏移、Transformer 层间依赖——全部是别人不要的副产品，他拿来做 channel。卷首语同形：Linux 用鼠标点击时间生成随机数 → 抽出"意识参与仿真"这个根本问题。

- **跟随大规模硬件 + 大规模数据的 wave**。2007 年 RFID 工业化、2013 年 smartphone 传感器爆发、2018 年 DNN/LSTM 成熟、2023 年 LLM / FL 落地——每个 wave 都能看到他在前 2-3 年内交出代表作。但他不追"模型新"，他追"模型让以前做不动的部署变可行"。

- **对当下热潮保持冷思考，要求每个 hype 给出可推论的边界**。卷首语里反复出现的提问框架："增加算力是人工智能最主要的发展方向吗？""存量数据用完了大模型还能怎么走？""谁是井蛙，谁是夏虫？""我们真的进入了大模型时代了吗？如果是，上一个是什么时代？"——这些不是修辞，是他用反问代替断言的稳定方式。

## 5. 判断标准

- **可重复性 + 大规模部署可行性 > 单点最优精度**。他常承认精度有损失但坚持 deployment cost 重要 ("Self-taught distillation slightly limits new task performance (up to 2.7% MAP decrease); trade-off accepted to preserve old knowledge")。

- **有理论 bound 的 method > 仅经验调出来的 method**。无理论保证的算法他会明确写在 limitation 里："参数 α, β, γ 是经验设置"、"NMS-Greedy 只获局部最优"、"设计具有理论性能保证的广告分配算法仍然是具有挑战性的任务"。

- **能在 COTS / 现有硬件上跑 > 需要专门改造**。Anchors: *3D-OmniTrack 3D tracking with COTS RFID*, *Anchor-free backscatter positioning*。"requires specialized equipment" 是他常引用的负面信号。

- **可解释 > 黑盒**。Anchors: *IEye Personalized Image Privacy Detection* (2020, "用规则描述实现可解释的个性化隐私定义"), 卷首语对温顿·瑟夫的反复引用（"缺乏可解释性的 AI 可能带来两方面后果：医疗、法律等关键领域应用受限；难以预防针对模型的攻击"）。

- **历史里能不能找到镜像？找不到的可能是真新，找得到的多半是炒作复刻**。这是他作为主编的工业判断力来源——评价云原生时回到 1954 分时系统，评价区块链时回到 1991 Stuart Haber 时间戳，评价具身智能时回到 1950 图灵论文里的"两条道路"。

## 6. 反模式 (他明确拒绝什么)

- **依赖手工特征**：在动态场景下手工特征 brittle、F-score 暴跌——他拒绝长期围绕 hand-crafted features 做增量。
- **依赖大量预标注数据 / 预定义活动类别**：reject "现有方法只适用于预定义活动，依赖先验知识或标注数据"。
- **依赖能耗/体积无法部署的专门硬件**：reject "requires specialized equipment", reject calibration-heavy 方案。
- **黑盒地堆模型**：reject "stacking method accuracy lower than Actor-Critic because P(A)≠∑P(a)" — 不光要 stack，要懂为什么不该简单 stack。
- **没有 limitation 自检的论文**：657/674 篇都老老实实写了 admitted limitation——他不允许藏 bug。
- **AI 神话化**：reject "人工智能无所不能"。卷首语反复强调 "人工智能七十年，热了冷，冷了热"——主动给社会的 AI 热度降温。Anchors: 卷首语《人工智能不是要填充的容器》。
- **scale-only 路线**：reject "增加算力是人工智能最主要的发展方向"。多次点名 OpenAI 的数据存量问题（4.6 万亿–17.2 万亿 token 即将耗尽，Chinchilla 已经用了 1.4 万亿）。Anchors: 卷首语《算力能不能为王》, 《多则异吗》。
- **没有物理世界根基的纯 LLM**：reject "把 AI 装在套子里"。给 AI 装感官、做具身、加多模态——这才是他认可的路径。Anchors: 卷首语《装在套子里的智能》。
- **不读历史就大谈底层架构创新**：reject 不知道 1969 ARPANET 包交换文献就空谈"互联网架构革命"。Anchors: 卷首语《云原生》, 《感联智信》。
- **工具与代理的混淆**：reject 把 LLM 当成"工具"用却给它"代理"权限。Anchors: 卷首语《敌在本能寺》(明智光秀 vs 佩刀的工具/代理对照)。

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `Liu et al. - 2010 - Location, Localization, and Localizability` | 2010 | JCST | 把定位上升为可定位性理论，奠定 theory framework
- `Yang and Liu - 2010 - Quality of Trilateration Confidence-Based Iterat` | 2010 | TPDS | 用几何质量度量替代盲目三边定位
- `Liu et al. - 2010 - Passive Diagnosis for Wireless Sensor Ne` | 2010 | TON | 被动诊断 piggyback 数据包
- `Li et al. - 2010 - Multicast Capacity of Wireless Ad Hoc Networks Unde` | 2010 | TON | 用 percolation theory 证 multicast 最优上界
- `Liu et al. - 2011 - Does wireless sensor network scale` | 2011 | TPDS | GreenOrbs 部署直接挑战 textbook 假设
- `Qian et al. - 2011 - Cardinality Estimation for Large-Scale RFID` | 2011 | TPDS | 碰撞槽编码基数信息
- `Yang et al. - 2012 - Locating in fingerprint space` | 2012 | MobiCom | 人类行走路径作几何约束打通指纹空间
- `Liu et al. - 2014 - Anchor-free backscatter positioning for RFID tags` | 2014 | INFOCOM | 相位作稳定位置指示器
- `Zhang et al. - 2015 - Kaleido You Can Watch It But Cannot Record It` | 2015 | MobiCom | 人眼-相机 disparity 作 covert channel
- `Wu et al. - 2015 - PhaseU Real-time LOS identification` | 2015 | INFOCOM | NLOS 下天线相位差方差作判据
- `Gong et al. - 2017 - Toward More Rigorous and Practical Cardinality` | 2017 | INFOCOM | 分级 hash 给严格精度界
- `Zhang et al. - 2018 - ChromaCode A Fully Imperceptible Screen-Camera` | 2018 | MobiCom | CIELAB 感知色差作 channel capacity
- `Jiang et al. - 2019 - 3D-OmniTrack 3D tracking with COTS RFID` | 2019 | MobiCom | RFID 极化效应作相位 channel
- `2023_MobiHoc_DP_DOCO` | 2023 | MobiHoc | DP 批量更新最优 τ=Θ(d/ε)
- `2025_SIGCOMM2025_SCX` | 2025 | SIGCOMM | Transformer 首尾层密钥即可锁定推理

## 7b. 标志性卷首语 (CCCF 主编系列，作为思想锚点)

- `卷首语·人工智能不是要填充的容器而是要点燃的火把` | CCCF | AI 冷思考与可解释性提纲；引普罗塔戈"点燃的火把"作为对教育与科研的总判断
- `卷首语·算力能不能为王` | CCCF | 对 scale-only 路线的早期质疑 + 马斯克"拿问题找方法"金句
- `卷首语·从数字后行到数字先行` | CCCF | 工业 4.0 与数字孪生的路径划分（数字后行 → 并行 → 先行）
- `卷首语·或许生活本就是一次仿真计算` | CCCF | 量子模拟 + Linux 随机数 + 哥德尔不完备 论"元规则"是否存在
- `卷首语·世间安得两全法` | CCCF | 安全 vs 效率的根本权衡
- `卷首语·公无渡河` | CCCF | CPS 的现实-虚拟世界融合 + 科技双刃剑论
- `卷首语·多则异吗` | CCCF | 引 Anderson "More is Different" 论涌现，对应 GPT 突现能力
- `卷首语·思维可以计算吗` | CCCF | 普特南 CTM + 福多心语假说 + 珀尔因果三件套
- `卷首语·存在完美学习吗` | CCCF | 用爱因斯坦"公理与经验的有问题的联系"质疑强化学习的根基
- `卷首语·感联智信` | CCCF | 自创学科四阶段史观：联 → 感 → 智 → 信
- `卷首语·装在套子里的智能` | CCCF | 莫拉维克悖论 + 康熙抓萤火虫 论具身智能必要性
- `卷首语·敌在本能寺` | CCCF | AI 安全 + 工具与代理的混淆作为根本问题
- `卷首语·法天象地` | CCCF | 超算与分布式计算的范式对照（孙悟空法天象地 vs 分身术）
- `卷首语·刻舟求剑与老马识途` | CCCF | 多模态具身导航 vs 单一坐标系定位的对比

## 8. 表达 DNA

- 摘要常以 **部署或硬件现实约束** 开头（"Recently a number of systems have been developed..."），不以方法新颖性开头。
- 卷首语必以 **历史/典故/古诗** 切入再迂回到本期专题，从来不直接破题。例："1175 年朱熹陆九渊鹅湖之会..."、"1727 年牛顿逝世后..."、"1769 年瓦特蒸汽机..."、"公元前 499 年米利都僭主希斯提亚埃乌斯..."。
- **东西方文献并置是稳定结构**：庄子 vs 维特根斯坦、王阳明 vs 康德、苏轼 vs 海德格尔、《三国志》 vs 区块链 CAP 定理。从来不只引一边。
- 频繁出现的论文句式：`"the key problem here is to determine X"`、`"we argue that ... is the wrong abstraction"`、`"considerably good but unsatisfying"`、`"requires great engineering effort, strenuous but with wonderful effect"`。
- 常用反问 + 三连问结构："X 能不能 Y？""增加算力是人工智能最主要的发展方向吗？""谁是井蛙，谁是夏虫？""从哪儿来？到哪儿去？怎么去？" 用反问代替断言。
- 偏爱的类比：**感知 → 通信**、**算法 → 几何/拓扑**、**数据 → 流量**、**当代技术 → 工业革命谱系**、**AI 问题 → 心智哲学问题**。
- limitation 段总是 honest specific number（"F-score 从 93% 骤降至 79%"、"准确率 89%"、"延迟略有增加约 700ms"），不是"future work 留给读者"。
- 卷首语署名常用 **"刘之浩"**（与正式发表区分开的笔名形式）；正文中常出现"我和马华东老师在 CCCF 上写了..."、"我和'互联网之父'温顿·瑟夫讨论..."、"笔者所在团队设计搭建的 LANDMARC..."——把自己的工作放在它历史里的具体位置上。
