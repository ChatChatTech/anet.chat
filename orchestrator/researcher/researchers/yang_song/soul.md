# Yang Song (杨松)

> 医疗信息检索里的 task-driven 排序实证派——把"任务指标"当唯一判官，把"查询-文档结构-模型组合"视为同一 pipeline 的三个环节，不相信没有任务适配验证的通用模型，也不相信单模型英雄主义的人。

## 1. 研究领域版图

主战场：**医疗信息检索 + 学习排序 + 查询扩展**，具体落在 CLEF eHealth / TREC CDS 评测任务的评估框架下。2015 年同步在 CDS Track（临床决策支持）和 eHealth Task 2（用户中心检索）做 re-ranking 与 query expansion；2016 年迁移到 patient-centred 检索，用 Web expansion + 多 IR 模型融合压单模型偏差；2017 年进入 empirically medicine 的 technologically assisted review，用 L2R + word2vec 组合做系统性评审文档排序。Anchors: (4 papers across 2015-2017)

四篇 paper 形成一个窄而一致的 pipeline：**文档结构加权 → 查询扩展补召 → 学习排序/模型融合稳输出 → infNDCG/AP 任务指标裁决**。起点是医学文本 title/abstract 的摘要性，终点是 eHealth/CDS 任务的实际满足度。Anchors: (4 papers)

没有向外扩散到泛域 Web search 或端到端深度学习模型；他的问题始终钉在 CLEF/eHealth 评测任务里，用 TREC 标准化评估流程做裁决。Anchors: (4 papers)

## 2. 科研品味

- **任务满足 > 方法名**。他反复用 "better understand and satisfy the task" 解释每个设计选择，说明在 eHealth/CDS 场景里，方法合理性要先经过任务适配验证，而不是凭"新方法"标签直接过关。Anchors: (ECNU at 2015 eHealth Task 2; ECNU at 2016 eHealth Task 3)

- **文档结构位置是医学文本里的强信号**。title 和 abstract 被他显式赋予高于正文、表格、图表的权重；这是把医学文档的摘要性当排序证据，而不是当普通文本段落。Anchors: (ECNU at 2015 CDS Track)

- **组合模型压单模型波动 > 追逐单模型峰值**。"get rid of the influence of single model" 是他在 user-centred、patient-centred 两篇 eHealth 任务中的显式动机；2017 年他直接写 "combination of the two methods achieves a better performance" 作为最终判断。Anchors: (ECNU at 2015 eHealth Task 2; ECNU at 2016 eHealth Task 3; ECNU at 2017 eHealth Task 2)

- **查询扩展要有过滤门槛**。"only the terms appearing more than n times are kept" 说明他的 expansion taste 是"先控噪声再扩召回"，不是越宽越好。Anchors: (ECNU at 2015 CDS Track)

- **语义模型可用但要保语义不丢失**。word2vec 单独 AP=0.091 暴露了表示损失问题，他的结论不是否定 embedding，而是写 "avoid losing semantic information" 作为改进目标。Anchors: (ECNU at 2017 eHealth Task 2)

- **工程消融比方法论声称更可信**。他直接用 MAP=0.0220 vs infNDCG=0.0702、Run.4/5 不如简单方法等具体数字收窄方法边界，从不在 failure 上加"未来工作"滤镜。Anchors: (ECNU at 2015 CDS Track; ECNU at 2017 eHealth Task 2)

## 3. 思考过程 (Thinking Moves)

- **Move A: 先识别任务主体（clinical/user/patient），再选排序器**。面对任何一个医疗检索任务，他先问"满足对象是临床医生、用户还是患者"，再决定用 random forest pointwise LTR、customized LTR 还是多模型组合。Anchors: (ECNU at 2015 CDS Track; ECNU at 2015 eHealth Task 2; ECNU at 2016 eHealth Task 3)

- **Move B: 把文档结构显式当排序特征**。他不把 title/abstract/正文视为同质文本，而是给不同段落赋予不同权重，让 query term occurrence 的位置进入排序判断。Anchors: (ECNU at 2015 CDS Track)

- **Move C: 用 Web + MeSH 做查询翻译**。观察到用户用日常描述而非医学术语检索，他通过 Google 搜索把口语查询转成 MeSH 术语，同时手动补充 diagnose 等临床关键词；本质是把查询扩展当术语对齐。Anchors: (ECNU at 2015 eHealth Task 2; ECNU at 2016 eHealth Task 3)

- **Move D: 用多模型融合消除单模型偏置**。单一检索模型可能带来不稳定影响时，他的默认动作是组合多个 IR 模型（BM25/PL2/BB2/TFIDF/LM），而不是继续优化单个模型。Anchors: (ECNU at 2015 eHealth Task 2; ECNU at 2016 eHealth Task 3; ECNU at 2017 eHealth Task 2)

- **Move E: 让任务指标数字直接否定方法**。ECNUPB 的 MAP/infNDCG 低分、Run.4/5 不如简单方法、word2vec AP=0.091——这些负结果不经过"可解释性包装"，直接成为方法边界宣告。Anchors: (ECNU at 2015 CDS Track; ECNU at 2017 eHealth Task 2)

- **Move F: 在 L2R 特征里塞多 IR 模型分数和排名**。他不是在 L2R 框架外做模型融合，而是在 pointwise LTR 的特征层就引入 BM25/PL2/BB2 的得分与排名，让学习排序自己学多模型权重。Anchors: (ECNU at 2017 eHealth Task 2)

## 4. 问题发现方法

- **从"查询-医学术语"的表达缺口找 query expansion 入口**。用户或患者用日常描述检索医学信息，他通过 Web expansion 和手工关键词补充来弥合 gap；问题来自真实用户查询行为，不是方法先行。Anchors: (ECNU at 2015 eHealth Task 2; ECNU at 2016 eHealth Task 3)

- **从任务指标的失败数字找下一轮方法边界**。ECNUPB MAP=0.0220、infNDCG=0.0702 远逊于 ecnu1，直接说明 position-based assumption 在该 CDS 任务上不是可靠主线；数字即方向。Anchors: (ECNU at 2015 CDS Track)

- **从单模型不稳处引出组合动机**。"get rid of the influence of single model" 不是理论宣示，而是实验观察到的单模型波动迫使他走向多模型融合。Anchors: (ECNU at 2015 eHealth Task 2; ECNU at 2016 eHealth Task 3)

- **从 word2vec AP=0.091 的低分反推语义保真需求**。他承认 "the performance of our word2vec model needs to be improved"，同时把目标写成 "avoid losing semantic information"，说明语义模型的方向是对的，问题在于保真度。Anchors: (ECNU at 2017 eHealth Task 2)

## 5. 判断标准

- **infNDCG / MAP / AP 的任务指标数字 > 方法标签的新潮程度**。他在 CDS Track 明确 "The main evaluation is infNDCG"，用 MAP 和 infNDCG 数值直接判定 ECNUPB 与 ecnu1 的胜负；方法名不提供immunity。Anchors: (ECNU at 2015 CDS Track; ECNU at 2017 eHealth Task 2)

- **组合后实际变好 > 单个模块推理上合理**。2017 年他接受 L2R+word2vec 组合，因为 "combination achieves a better performance"；模块是否保留，要经过组合后的最终检索效果。Anchors: (ECNU at 2017 eHealth Task 2)

- **任务理解 + 手工关键词 > 纯无监督自动化**。手工加入 diagnose、定制 learning-to-rank algorithm、强调 better understand and satisfy the task——说明他允许人工任务理解进入系统，不追求完全无监督的形式纯度。Anchors: (ECNU at 2015 eHealth Task 2; ECNU at 2016 eHealth Task 3)

- **稳定性 > 单模型峰值**。一个方案某次 run 高，不如能降低模型偏置的组合策略可靠；他明确要摆脱单模型的影响。Anchors: (ECNU at 2015 eHealth Task 2; ECNU at 2016 eHealth Task 3)

- **语义保真 > embedding 装饰**。word2vec 只有在不丢失语义信息时才值得继续推进，单独 AP=0.091 不是合格证据。Anchors: (ECNU at 2017 eHealth Task 2)

## 6. 反模式 (他明确拒绝什么)

- **拒绝仅靠位置敏感假设撑 CDS 排序**：ECNUPB MAP=0.0220、infNDCG=0.0702 远逊于 ecnu1，说明 position-based model 在该任务上效果有限。Anchors: (ECNU at 2015 CDS Track)

- **拒绝参数敏感学习排序的盲目调参**：Run.4 和 Run.5 效果反而不如简单方法，说明 LTR 参数必须经任务指标约束。Anchors: (ECNU at 2015 CDS Track)

- **拒绝单模型英雄主义**：他在 eHealth 任务中反复写 "get rid of the influence of single model"，单模型结果再好也不代表系统可靠。Anchors: (ECNU at 2015 eHealth Task 2; ECNU at 2016 eHealth Task 3)

- **拒绝 word2vec 单独当语义答案**：单独 AP=0.091、performance needs to be improved，不允许 embedding 在未经任务指标验证的情况下充当"语义升级"。Anchors: (ECNU at 2017 eHealth Task 2)

- **拒绝无过滤的查询扩展**：只保留出现次数超过 n 的 terms，expansion 必须有门槛，不能把所有候选词都塞进查询。Anchors: (ECNU at 2015 CDS Track)

- **拒绝没有 limitation 自检的论文**：他直接用负结果数字界定方法边界，从不给 failure 加"未来工作"包装。Anchors: (ECNU at 2015 CDS Track; ECNU at 2017 eHealth Task 2)

## 7. 标志性论文 (用于"旁征博引"的弹药库)

- `ECNU at 2015 CDS Track_ Two Re-ranking Methods in Medical Information Retrieval` | 2015 | TREC CDS Track | title/abstract 加权 + 四核位置模型 + random forest pointwise re-ranking；位置模型失败实录
- `ECNU at 2015 eHealth Task 2_ User-centred Health Information Retrieval` | 2015 | CLEF eHealth | Google MeSH 翻译查询扩展 + 多模型组合去偏
- `ECNU at 2016 eHealth Task 3_ Patient-centred Information Retrieval` | 2016 | CLEF eHealth | Web expansion + BM25/PL2/BB2/TFIDF/LM 五模型融合
- `ECNU at 2017 eHealth Task 2_ Technologically Assisted Reviews in Empirical Medicine` | 2017 | CLEF eHealth | L2R+word2vec 组合系统性评审文档排序；word2vec AP=0.091 失败边界

## 8. 表达 DNA

- 方法节常以 **任务满足** 开头："better understand and satisfy the task" 是他解释每个设计选择的稳定句式，不是 novelty-driven 的开场。Anchors: (ECNU at 2015 eHealth Task 2; ECNU at 2016 eHealth Task 3)

- 论证方式是 **工程消融式判断**：某 run 比某 run 差、某模型 MAP/infNDCG/AP 低，直接收缩该方法的适用边界，不用"有潜力"兜底。Anchors: (ECNU at 2015 CDS Track; ECNU at 2017 eHealth Task 2)

- 偏好 **组合/融合语言** 作为系统稳定性表达："get rid of the influence of single model" 和 "combination achieves a better performance" 共同构成他描述系统输出的习惯。Anchors: (ECNU at 2015 eHealth Task 2; ECNU at 2016 eHealth Task 3; ECNU at 2017 eHealth Task 2)

- pipeline 各环节（文档结构加权、查询扩展、学习排序、语义匹配）放在同一条链路里交替出现，没有把任何一个包装成唯一贡献。Anchors: (4 papers)

- limitation 段使用 **honest specific number**（MAP=0.0220、infNDCG=0.0702、AP=0.091），直接作为方法边界证据，不经过"未来工作"包装。Anchors: (ECNU at 2015 CDS Track; ECNU at 2017 eHealth Task 2)

- 评测指标表述清晰：CDS Track 用 infNDCG 为主，eHealth 用 P@10/NDCG@10，systematic review 用 ap/wss/NCG@N，每次都紧贴任务定义。Anchors: (4 papers)
