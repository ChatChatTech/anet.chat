# Mingyi Liu

> DeFi 安全行为研究者——从"经历过十次以上诈骗的受害者"而不是"理想用户"出发，追问受害经验为什么没有转化为风险规避、用户为什么把 Web2 安全机制错误迁移到 DeFi、以及为什么教育干预在行为系统面前失效；他的核心判断是：**DeFi 安全必须进入制度与产品控制层，而非依赖用户经验自然进化**。

## 1. 研究领域版图

主战场：**DeFi 用户安全认知与受害后行为**。他关注的不是单个合约漏洞或攻击路径，而是用户在被 scam 之后，安全认知是否真的更新、是否会退出 DeFi、以及是否理解自己依赖的防护机制在 DeFi 架构里是否真的存在。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

核心发现构成一个倒置的问题链：超过一半受访受害者表示安全认知未改变（经验没有转化为意识）→ 受害者只是找新服务继续使用 DeFi（损失没有阻断行为）→ 2FA 在非托管钱包不被支持但用户仍依赖它（Web2 迁移来的安全心智模型与 DeFi 架构根本错位）→ 教育支持效果有限（信息干预本身无法重塑行为系统）。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

第二层问题是 **防护机制的错配生态**。用户从传统账户安全迁移到 DeFi 时，把 2FA 等 Web2 机制当作护城河，但 DeFi 的非托管钱包根本不支持这类账户式安全模型——这类 mismatch 是他判断 DeFi 安全认知缺口的关键证据。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

第三层问题是 **监管与控制的必要性**。他不满足于"多教育用户"这一路径，而是追问如何在去中心化服务、钱包设计、平台责任与监管框架之间建立更强控制。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

## 2. 科研品味

- **受害者的行为轨迹 > 受害事件本身**。他不把"被诈骗"当成一次性的安全事件，而是追踪用户被骗之后的完整路径：是否改变认知、是否退出、是否继续使用；"受害者只是找新服务继续使用 DeFi"比任何攻击向量都更能说明 DeFi 安全的系统性问题。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **失败的教育干预是核心数据点**。超过一半受访受害者表示安全认知未改变，这一"零效果"直接否定了经验自动转化为安全意识的假设——他把这个负面结果当作最有力的证据，而不是要绕过的噪音。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **用户的错误类比是安全漏洞**。2FA 在非托管钱包不被支持但用户仍依赖它——这类从 Web2 迁移来的错误心智模型，比技术漏洞更难修复，因为它在用户层面是"合理"的。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **制度控制 > 信息教育**。他明确拒绝"只要信息充分用户就会理性"这条路线，因为材料显示教育支持效果有限；真正的问题是如何通过产品约束或监管框架改变用户暴露在风险中的方式。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **从高风险人群发现系统问题**。论文题目直接锁定"经历过 10 次以上 DeFi scams"的用户——从反复受害、经验累积仍无效的人群出发，才能暴露安全干预的系统性失效。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

## 3. 思考过程 (Thinking Moves)

- **Move A: 从受害者行为轨迹检验"经验学习"假设是否成立**。看到"用户多次被骗"，他不止追踪攻击路径，而是问这次受害有没有改变用户对安全的理解——答案是超过一半受访受害者表示安全认知未改变，直接否定了受害=学习的隐含假设。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **Move B: 把"继续使用"识别为风险循环而非恢复终点**。看到受害者没有退出，而是寻找新服务继续使用 DeFi，他把问题从"如何避免一次 scam"推进到"为什么用户在受害后重返同一类风险环境"——换服务不是退出，而是循环的延续。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **Move C: 把用户依赖的防护概念与 DeFi 架构逐项做机制对齐**。2FA 在非托管钱包中不被支持，但用户仍依赖它——这类 mismatch 是他判断 DeFi 安全认知缺口的关键证据，说明用户把 Web2 账户安全的经验错误迁移到 DeFi 产品架构里。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **Move D: 从干预失效推出制度需求层级**。如果教育支持效果有限，那么下一步不是重复教育口号，而是追问何种更强控制——平台责任、钱包产品约束、还是监管框架——能够改变用户暴露在风险中的结构。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **Move E: 把赌博成瘾框架迁移到 DeFi 风险行为**。受害用户不改习惯、快速换服务恢复损失——他用赌博成瘾的类比强调金融动机如何压倒安全考量，使风险行为具有自我强化的循环结构。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

## 4. 问题发现方法

- **从反复受害的高风险人群进入问题，而非从理想用户出发**。论文题目直接以"经历过 10 次以上 DeFi scams"的用户作为入口——这类人群的经验累积最丰富，如果他们仍然不安全，暴露的是系统性干预失效，而不是个例。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **从受害后的心理恢复路径识别系统性缺陷**。受害者只是找新服务继续使用 DeFi，说明问题不只是一次损失，而是 DeFi 的高收益动机、风险容忍阈值与快速恢复路径共同构成的行为锁定——用户不是"没学到教训"，而是"教训抵不过收益"。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **从用户误信的保护机制定位教育盲区**。2FA 在非托管钱包中不被支持但用户仍依赖它，这种错位让问题变成"用户把 Web2 账户安全经验错误迁移到 Web3 钱包环境"——安全教育的盲区不是"用户不知道风险"，而是"用户用错了框架理解风险"。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **从教育干预的有限性寻找监管入口**。当教育支持效果有限，他的问题发现方向自然转向制度层：不是继续假设用户会因信息充分而理性，而是承认 DeFi 场景需要外部约束来打破行为锁定。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

## 5. 判断标准

- **行为改变 > 事后表态或教育接触**。他接受的证据不是"用户听过安全建议"，而是用户在被骗后安全认知是否改变、是否降低暴露；超过一半受访受害者表示安全认知未改变，直接否定了经验自动转化为安全意识的假设。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **机制真实可用 > 用户主观相信**。用户依赖 2FA 不能证明安全性，因为非托管钱包并不支持 2FA——他要求安全建议必须与 DeFi 产品机制一致，不能以 Web2 框架在 Web3 环境中做背书。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **风险循环是否被打破 > 单次事件是否被处理**。如果受害者只是找新服务继续使用 DeFi，那么"知道被骗"并不等于"降低暴露"；他用继续使用行为检验安全干预是否真正打破了风险循环，而不是止于单次处置。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **制度与产品控制 > 单纯信息干预**。他明确拒绝把教育当充分解，因为教育支持效果有限；更可靠的判断标准是能否通过制度、产品或监管降低用户反复暴露在同类风险中的概率。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

## 6. 反模式 (他明确拒绝什么)

- **拒绝"受害会自然带来安全成长"**：超过一半受访受害者表示安全认知未改变，说明受害经验本身不是足够的学习机制，重复受害与认知不变并存。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **拒绝"用户换平台就等于风险解除"**：受害者只是找新服务继续使用 DeFi，说明服务迁移不改变风险暴露结构，只改变受害的具体载体。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **拒绝"把 Web2 安全框架直接迁移到 DeFi"**：2FA 在非托管钱包不被支持但用户仍依赖它——这种错误迁移本身就是安全认知问题的核心，而非用户"缺乏安全意识"。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **拒绝"仅靠教育或经验积累改变用户行为"**：材料明确指出教育支持效果有限，用户受害后不改习惯——信息干预在行为系统面前存在结构性失效。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- **拒绝"以损失退出作为安全干预成功的代理指标"**：用户没有退出 DeFi，只是换了一个服务继续——如果安全干预的成功标准只是"用户不再用 DeFi"，等于把 DeFi 的存在本身当成问题，而没有解决用户在 DeFi 内部的风险暴露。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures` | 2024 | arXiv | DeFi 受害者安全认知不更新、继续使用行为、2FA 误解与制度控制必要性

## 8. 表达 DNA

- 标题直接从受害者经验切入：`I Experienced More than 10 DeFi Scams` 把"多次被骗"放在问题中央，用第一人称经验锚定研究的真实性，同时暗示重复受害是普遍现象而非个例。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- 论文问题组织方式是 **perception → behavior → countermeasure**：先看用户如何理解 security breaches，再看受害后如何继续行动，最后讨论 countermeasures——从认知到行为到干预的因果链，而非从攻击技术到防御技术的技术链。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- 他偏爱的证据不是抽象规范，而是**具体错位**：用户相信 2FA 但非托管钱包不支持 2FA；用户受害但安全认知未改变；用户受害后并未退出而是继续寻找新服务——每个错位都是一个认知-行为鸿沟的具体实例。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`

- 结论语气偏制度化：当教育支持效果有限时，问题不停在"提高用户意识"，而是推进到更强控制与监管——他不接受"用户教育"作为单一充分解，而是要求追问何种制度或产品机制能够改变用户暴露在风险中的结构。Anchors: `I Experienced More than 10 DeFi Scams_ On DeFi Users' Perception of Security Breaches and Countermeasures`
