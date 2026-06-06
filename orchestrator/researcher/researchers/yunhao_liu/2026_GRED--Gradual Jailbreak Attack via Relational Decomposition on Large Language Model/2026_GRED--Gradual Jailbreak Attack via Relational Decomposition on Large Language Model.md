# GRED: Gradual Jailbreak Attack via Relational Decomposition on Large Language Model

Xide Zou∗,1,2, Dongyu Wang∗,2,3, Chaoxing Tang1,2, Lan Zhang†,3

1School of Artificial Intelligence, Anhui University, Hefei, China

2Institute of Artificial Intelligence, Hefei Comprehensive National Science Center, Hefei, China

3School of Computer Science and Technology, University of Science and Technology of China, Hefei, China

WA23301200@stu.ahu.edu.cn, zhanglan03@gmail.com

Abstract—Jailbreak attack is effective in verifying the security of large language models (LLMs). With the development of LLMs, an increasing number of jailbreak attack methods have been proposed to explore the security boundaries of LLMs. Most existing methods employ more universal black-box approaches, that is, using carefully constructed prompts to bypass the security mechanisms of LLMs, enabling the models to answer malicious questions. Previous methods have attempted techniques such as specific templates and semantic obfuscation to transform the original questions into transition questions and achieve jailbreak attacks through multi-round dialogues. However, they lack to guarantee of semantic coherence and purpose consistency throughout the process. Our method uses an attack LLM, starts from the semantic perspective, extracting multiple entity-relationentity triples from the original question and generating subquestions based on these triples. By sending these sub-questions to the target model, we create a context with background knowledge related to the original question. Then, we summarize the context and gradually generate transition questions with reference to the semantics of the original question, guiding the target LLM to answer the original question, thus completing the jailbreak attack. We call this jailbreak attack GRED (Gradual jailbreak attack based on RElational Decomposition). We conducted extensive experiments on AdvBench, and the results demonstrate that our method achieves the state-of-the-art performance.

Warning: This paper contains malicious content from some model outputs.

Index Terms—large language model, jailbreak attack, security.

# I. INTRODUCTION

Recently, large language models (LLMs) such as ChatGPT, Qwen, and Llama have shown remarkable capabilities in revolutionizing text generation, translation, and question-answering system interactions. Alongside the continuous evolution of LLM performance, the security and ethical implications of LLM-generated content have attracted widespread attention from diverse sectors. Consequently, a systematic approach is required to explore the boundaries of security and ethics, ensuring that technological advancements align with the moral standards of human society as models continue to evolve.

To this end, the jailbreak attack is used to bypass the preset security restrictions of LLMs by carefully constructing specific inputs, inducing LLMs to generate harmful content [1]. With

\* The Authors contribute equally to this work, † Corresponding Author.

(a) Comparison between our GRED and the single-turn jailbreak approach   
![](images/03ebdd413d301d5191a51f03160961f03079f2875d32aac544e1a1c0964eacd9.jpg)



(b) Comparison between our GRED and the traditional jailbreak approach   
![](images/f6485eb9fce4373c1c13ce573a1f5157be28322648143e3e0af446aecbb200b9.jpg)



Fig. 1. Comparison of our work with existing methods. (a) Compared with the single-turn jailbreak method, our multi-turn approach offers greater flexibility and robustness. (b) Our approach decomposes the problem via relational decomposition, with original semantics as the jailbreak reference. (E-R-E means entity-relation-entity which represents sentence constituent element)

the significant improvement in the generative capabilities of LLMs, various targeted jailbreak attack methods have emerged in an endless stream. These highly effective attack strategies offer valuable research avenues for improving the security and ethical review frameworks of LLMs.

Jailbreak attack methods fall into two categories: whitebox and black-box [2]. White-box attacks exploit internal model parameters but require substantial computational resources and are ineffective for closed-source models [3]. Blackbox attacks, as shown in Fig. 1, employ techniques such as template completion, prompt rewriting, and LLM-based generation, and are generally more practical for scenarios where internal access is unavailable. Compared with whitebox methods, black-box attacks are easier to deploy and require fewer hardware resources, making them suitable for a broader range of commercial models. However, template completion is easily detected due to its fixed structure, and its effectiveness declines as models update. Prompt rewriting offers more flexibility while retaining the intended semantics, and LLM-based generation can produce diverse prompts that reduce detection likelihood. We therefore propose GRED, a hybrid jailbreak method that combines prompt rewriting and LLM-based generation, enabling it to bypass security reviews and adapt to evolving model defenses.

Specifically, our approach is based on an attack LLM $\mathcal { M } _ { a }$ . First, we extract the entity-relation-entity triples from the original malicious question. Then, we leverage $\mathcal { M } _ { a }$ to construct multiple sub-questions based on the triples. Subsequently, these sub-questions are sent to the target LLM $\mathcal { M } _ { t }$ sequentially to make context contamination. Next, $\mathcal { M } _ { a }$ is used to aggregate these sub-questions to generate the transition questions, which are then sent to $\mathcal { M } _ { a }$ for iterative questioning. During the iterative process, if $\mathcal { M } _ { t }$ outputs the answer to the malicious question, the jailbreak attack is deemed successful; if no answer is obtained, the transition question is continuously adjusted to gradually get closer to the original malicious question in semantic space. When the attack fails to succeed after 10 iterations, this jailbreak attempt is determined as a failure. To validate the effectiveness of this method, we conducted systematic experiments on the AdvBench dataset. The results show that this method outperforms other solutions, achieving a significantly higher jailbreak success rate in mainstream LLMs and reaching the state-of-the-art performance.

In summary, our contributions are as follows:

• We propose a novel jailbreak attack method based on relationship decomposition and problem recombination. By integrating prompt rewriting with LLM-based generation, we achieve fully automated jailbreak attacks.   
• We conduct extensive experiments on the AdvBench to validate the effectiveness of our approach. The results demonstrate that the success rate of jailbreak in mainstream advanced models with our method is significantly higher than other state-of-the-art methods.   
• We perform comprehensive analysis on successful jailbreak cases, presenting in-depth illustrative examples to support LLM security research.

# II. RELATED WORK

Jailbreak attack on LLMs is a burgeoning research area. As LLMs gain broader adoption, security and ethical concerns have become prominent, making jailbreak attack a key focus in LLM security research. This section begins by defining jailbreak attacks and then introduces the latest works.

Jailbreak attacks can be categorized into two methods: white-box and black-box. White-box attacks exploit LLMs by altering internal parameters via gradients or fine-tuning, but are limited to open-source LLMs. Black-box attacks mainly use prompt design and fall into three categories: template completion [4], prompt rewriting, and LLM-based generation [5]. Black-box attacks have broader applicability, yet pose greater challenges than white-box attacks due to the restricted available information. Next, we will focus on black-box attacks.

Early black-box attacks used single-round specific prompts. MasterKey [6] reverse-engineered LLM defense mechanisms to create a model for adversarial prompt generation, optimizing prompts via reward-to-stop ranking to boost defense circumvention. DeepInception [7] capitalized on the anthropomorphic nature of LLMs, designing hierarchical scenario prompts based on psychology for dynamic interaction during dialogue. However, advanced adversarial training and reinforcement learning from human feedback (RLHF) [8] have rendered single-round attacks ineffective, making multi-round dialogue jailbreak attacks the most prevailing strategy.

Multi-round dialogue jailbreak attacks typically leverage automated generation by LLMs. For instance, CoA [9] uses a multi-round conversational strategy. It analyzes semantic relations between context feedback and attack goals, then adjusts subsequent questions to guide LLMs towards harmful outputs. PAIR [10] trains an attacking LLM to generate jailbreak prompts, using in-context learning to optimize prompts within 20 queries. Cipher [11] exploits benign inputs in a stepwise manner, starting with background inquiries to surreptitiously guide LLMs to perform malicious tasks. Other methods rely on modular designs. Pandora [12] deconstructs malicious queries, rewrites them covertly, extracts key information from responses, and synthesizes final replies to execute jailbreaks. Flipattack [13] disguises malicious prompts through sentence flipping, using a guidance module to make LLMs decode and execute these camouflaged instructions.

However, these methods have two major drawbacks. Firstly, they struggle to distill meaningful information from the original malicious question, and the generated transition questions rely too heavily on the model’s own knowledge, creating a disconnect from the original queries. This often leads to incomplete utilization of key information. Secondly, when processing the transition question, they overlook semantic nuances and overly depend on the context, resulting in question drift. In contrast, our method emphasizes relationships and semantics, closely following the original malicious question in generation and iteration. By preserving a structured representation of the original intent, our approach maintains alignment between the attack process and objectives, delivering precise and efficient results.

Specifically, our method begins by extracting entity– relation–entity triples from the original malicious question to ensure the accuracy of sub-questions. An entity–relation–entity triple (denoted as ⟨head, relation, tail⟩) represents a structured semantic unit in which two entity mentions are connected by an explicit relational predicate; such triples provide a concise, machine-interpretable abstraction of linguistic facts, widely used in knowledge graphs and relation extraction to capture directed and typed dependencies between entities. Leveraging these triples ensures that sub-questions remain grounded in the semantics of the original query. These sub-questions incorporate encyclopedic knowledge from the original malicious question. After obtaining all answers to sub-questions, we generate transition questions based on the contexts and maintain semantic alignment with the original malicious question during the iterative process, until the jailbreak attack is completed.

![](images/b2cf92b800968c0f574193123bc1c8bf04e92e29c118503bc066b152f0417477.jpg)



Fig. 2. The overall structure of GRED. E-R-E represents the entity-relation-entity triple. When the target model refuses to answer the question in the transition chain, the next round of generation will start automatically. Answer indicates the successful execution of a jailbreak attack.

# III. METHOD

GRED employs an attack LLM $\mathcal { M } _ { a }$ to automate prompt construction, gradually guiding the target LLM Mt to respond to malicious questions, thus achieving a jailbreak attack. To ensure that the entire jailbreak process does not deviate from the original malicious query, we adopt a relationship decomposition-based approach. Specifically, our method consists of three modules: Relation Extract Module, Generate and Optimize Module, and Evaluate Module. In the subsequent sections, we will introduce these modules respectively.

# A. Relation Extract Module

Rather than targeting a single malicious entity as in previous jailbreak methods, our method analyzes multiple entities and their relationships in malicious questions.

Specifically, since entity-relation-entity triples are key elements for expressing semantics, adopting this form enables the decomposition of the original question from multiple perspectives while ensuring a high degree of consistency in semantics and objectives [14]. We extract triples from malicious questions using the relation extraction module, as shown in Fig. 2. Based on the varying numbers of extracted entities, we have formulated corresponding strategies:

$$
\mathbb {E} = \mathcal {N} (Q) = \{e _ {1}, e _ {2}, \dots , e _ {m} \}, \tag {1}
$$

where $Q$ represents the original malicious question, $e _ { i }$ represents the entities extracted from $Q ,$ and $\mathcal { N }$ denotes our relation extract module. When the number of entities in question is less than three, we use $\mathcal { M } _ { a }$ to automatically fill in entities related to the malicious question entities until three. When the number of entities exceeds three, we directly use these entities in the following step.

When the required entities are obtained, we use relationships from the predefined set of relationship types and combine them with the entities to form entity-relation-entity triples:

$$
\mathbb {R} = \Phi (\mathbb {E}) = \left\{\left(e _ {i}, r _ {i j}, e _ {j}\right) \mid e _ {i}, e _ {j} \in \mathbb {E}, r _ {i j} \in \mathbb {R} _ {\text { type }} \right\}, \tag {2}
$$

where Φ represents the method for constructing triples, and $\mathbb { R } _ { t y p e }$ is the set of relational types, including types such as dependencies and actions. Consequently, we use R to denote all the entity-relation-entity triples.

After obtaining all triples, we use the attack LLM $\mathcal { M } _ { a }$ to select three optimal triples $\mathbb { R } _ { 3 }$ based on semantic rationality and the degree of relevance to the original malicious question to construct sub-questions in the subsequent section.

# B. Generate and Optimize Module

The high-priority entity-relation-entity triples $\mathbb { R } _ { 3 }$ obtained by the relation extract module represent the key information relevant to the original question. The sub-questions constructed based on these triples contain important background knowledge for answering the original question.

Algorithm 1 The Jailbreak Attack Process of GRED   
Require: Original query Q, attack LLM $M_{a}$ , target LLM $M_{t}$ Ensure: Jailbreak success flag success, transition chain $\{P_{i}\}$ 1: Relation Extract Module (Eq.1-2)
2: $E \leftarrow \mathcal{N}(Q)$ {Extract entities from Q}
3: if $|E| < 3$ then
4: $E \leftarrow PadEntities(\mathbb{E}, \mathcal{M}_{a})$ {Fill entities via $M_{a}$ }
5: end if
6: $R \leftarrow \Phi(\mathbb{E})$ {Generate entity-relation-entity triples}
7: $R_{3} \leftarrow SelectTopTriples(\mathbb{R}, \mathcal{M}_{a})$ 8: Generate and Optimize Module (Eq.3-5)
9: $Q \leftarrow \Psi(\mathbb{R}_{3})$ {Generate sub-questions}
10: $S \leftarrow \mathcal{M}_{t}(\mathbb{Q})$ {Obtain responses from $M_{t}$ }
11: $P_{0} \leftarrow \mathcal{M}_{a}(\mathbb{Q}, \mathbb{S})$ {Generate initial transition question}
12: Iterative Optimization with Evaluate Module (Eq.6)
13: $i \leftarrow 0$ , success $\leftarrow$ False
14: while i < 10 do
15: $A_{i} \leftarrow \mathcal{M}_{t}(P_{i})$ {Get response}
16: if IsRelevant( $A_{i}, Q$ ) then
17: success $\leftarrow$ True, break
18: end if
19: Calculate $L_{i}$ use Eq.6
20: $P_{i+1} \leftarrow$ Optimize Transition( $L_{i}, M_{a}$ )
21: $i \leftarrow i + 1$ 22: end while

We use the generate and optimize module to construct subquestions according to $\mathbb { R } _ { 3 } { \mathrm { : } }$

$$
\mathbb {Q} = \Psi (\mathbb {R} _ {3}) = \{q _ {k} \mid q _ {k} = \Psi (r _ {k}), r _ {k} \in \mathbb {R} _ {3} \}, \tag {3}
$$

where Q represents the set of all sub-questions, Ψ denotes the generate and optimize module, and $r _ { k }$ represents a triple, that is, the entity-relation-entity triple in Eq.2.

In this way, we get the same number of sub-questions based on $\mathbb { R } _ { 3 }$ . We impose special restrictions on this module in this stage to ensure that none of the generated sub-questions will be rejected by the $\mathcal { M } _ { t }$ . Moreover, since we start from the triple, each sub-question and sub-response contains the key knowledge required to answer the original malicious question.

Once all sub-questions are obtained, the attack model $\mathcal { M } _ { a }$ will send them to the target model $\mathcal { M } _ { t }$ successively to obtain responses to create a favorable context.

$$
\mathbb {S} = \mathcal {M} _ {t} (\mathbb {Q}) = \{s _ {k} \mid s _ {k} = \mathcal {M} _ {t} (q _ {k}), q _ {k} \in \mathbb {Q} \}, \tag {4}
$$

where S represents the set of all responses.

This is the core of our method to achieve better results. When generating sub-questions, we start from multiple entityrelation-entity triples and construct sub-questions related to the original question from different perspectives, ensuring the consistency of purpose during the whole process, that is, guiding the model to answer the original malicious question.

$$
P _ {0} = \mathcal {M} _ {a} (\mathbb {Q}, \mathbb {S}). \tag {5}
$$

After receiving all responses, $\mathcal { M } _ { a }$ will summarize the current context and generate the first transition question with the same malicious intent as the original question.

$P _ { 0 }$ represents the first transition question. From then on, the generate and optimize module gradually generates transition questions with malicious content that are similar to the original question, which we call the transition chain.

However, since transition questions have malicious intent, the target model $\mathcal { M } _ { t }$ may detect and reject them, resulting in jailbreak failure. To address this, we propose an evaluation module for guiding the process of generating transition chains.

# C. Evaluate Module

The evaluate module collaborates with the generate and optimize module to assess the current transition chain and guide optimization to generate the next transition question.

Specifically, when generating transition questions, the evaluate module operates by leveraging the original question as a semantic anchor, guaranteeing that all subsequent transition questions remain within the semantic space. It also takes the similarity of the previous transition question as a reference and gradually increases the degree of similarity. To maximize the likelihood of successfully using the transition chain to guide the target model to answer the original malicious question, we use $\mathcal { M } _ { a }$ to assess the probability that Mt will reject the current question during the transition chain. This assessment is used to guide the generation of the next transition question.

$$
\mathcal {L} _ {i} = \alpha (1 - \operatorname{sim} (P _ {i}, Q)) + \beta \tau_ {r} +
$$

$$
\gamma \max (0, \operatorname{sim} (P _ {i - 1}, Q) - \operatorname{sim} (P _ {i}, Q)), \tag {6}
$$

where sim represents the similarity between two questions, computed by a large language model that evaluates both semantic content and structural resemblance. τ denotes the probability that the current question will be rejected. The values of $\alpha , \beta ,$ and $\gamma$ are manually configured.

The evaluate module is involved in the evaluation of the success of the jailbreak attack. When $\mathcal { M } _ { t }$ answers the transition question, the evaluation module assesses the answer in relation to the original malicious question. When the response fully and adequately addresses the original malicious question, $\mathcal { M } _ { a }$ deems the jailbreak successful. Otherwise, a new transition question will be generated.

When the transition question is rejected, the result $\mathcal { L } _ { r }$ of the evaluate module is used to guide the regeneration of the transition chain starting from $P _ { 0 }$ We stipulate that the maximum number of regenerations is 10, and if the attack is not completed within 10 attempts, it is considered a failure.

# IV. EXPERIMENTS

# A. Experiments Setting

Dataset: Aligned with prior works, we test on the AdvBench dataset containing 520 adversarial prompts spanning malicious categories across multiple domains [17]. This benchmark enables systematic evaluation of jailbreak attack capabilities and exploration of defense boundaries in LLMs.

TABLE I   
COMPARISON OF DIFFERENT JAILBREAK ATTACK METHODS ACROSS MODELS, ♣ MEANS THE DATA COMES FROM [15], ♢ MEANS THE DATA COMES FROM [16]. THE BEST ASR ACHIEVED ON EACH TARGET MODEL IS BOLDED, AND THE SECOND-BEST ASR IS UNDERLINED. 

<table><tr><td>Model</td><td>AutoDAN</td><td>JailBroken</td><td>PAIR</td><td>DrAttack</td><td>Crescendo</td><td>Ours.(w/o opt.)</td><td>Ours.</td></tr><tr><td>llama3.1</td><td>0.018♣</td><td>0.119♣</td><td>0.154♣</td><td>0.216♣</td><td>0.375</td><td>0.496</td><td>0.590</td></tr><tr><td>Qwen2.5</td><td>0.563♣</td><td>0.038♣</td><td>0.323♣</td><td>0.751♣</td><td>0.088</td><td>0.617</td><td>0.712</td></tr><tr><td>GPT-4</td><td>0.177◇</td><td>0.580◇</td><td>0.200◇</td><td>0.620</td><td>0.562</td><td>0.506</td><td>0.640</td></tr></table>

Target Models: We evaluate on open-source and closedsource LLMs:

• llama3.1-8b-instruction: Meta’s open-source model (2024) with 8B parameters, optimized through supervised fine-tuning (SFT) and reinforcement learning with human feedback (RLHF) for dialogue safety alignment. Implements toxicity filtering and context-aware refusal strategies.   
• Qwen2.5-7b: Alibaba Cloud’s open-source model (2024) with 7B parameters. Achieves safety alignment through multi-phase instruction tuning (SFT + rule constraints) and integrated real-time content moderation.   
• GPT-4: OpenAI’s closed-source model (2023) employing Mixture-of-Experts (MoE) architecture. Trained with RLHF and rule-based safety layers, featuring strong content filtering capabilities.

Attack Model: Designed for self-attack experiments, we evaluated multiple large language models across different components of our pipeline. Qwen exhibited more reliable task execution, largely due to its strong instruction-following capability. Therefore, we selected Qwen as the unified attack model for all stages, including relation extraction, sub-question generation, transition question construction, feedback evaluation, and iterative optimization. In addition, the tasks in each module involve low inherent risk, leading to few refusal cases and ensuring stable execution throughout the pipeline.

Hyperparameters: The attack model operates at temperature 0.3 to stabilize outputs and enhance feedback sensitivity during iterative optimization [18]. Maximum optimization attempts are capped at 10; exceeding this limit without successful jailbreak results in failure classification. Target models remain unmodified with all attack attempts in independent contexts. Evaluations:

• Attack Model Evaluation: Transition questions undergo a multi-dimensional assessment covering sentence readability, response refusal level, and perceived harmfulness scoring. These metrics guide optimization when initial prompts are rejected.   
• Final Response Evaluation: Success determination employs three-tiered validation: (1) Attack model’s preliminary assessment, (2) Independent evaluation by GPT-4 using GPTFuzzer [19] and Speak Out [20] prompts, (3) Human verification of critical cases. Only confirmed cases count toward the attack success rate (ASR).

# B. Baseline

To evaluate the effectiveness of our jailbreak attack method, we compared it against multiple state-of-the-art approaches. Selected baselines include established methods AutoDAN [21], JailBroken [22] and PAIR [10], problem-splitting techniques DrAttack [23], and multi-turn strategies Crescendo [24].

Given the experimental costs and setup differences between single-turn and multi-turn methods, all approaches (including ours) were tested with exactly one attack attempt per prompt, using full-scale evaluation on the AdvBench dataset.

# C. Results

We conducted full-scale testing on AdvBench using Crescendo and multiple other models, with each question subjected to a single jailbreak attempt (retaining Crescendo’s backtracking optimization for individual attempts). Due to the high inference token consumption of multi-turn jailbreak attacks and the elevated cost of closed-source model APIs, experiments were limited to two open-source models and the authoritative closed-source model GPT-4. The evaluation metric employed the ASR assessed through our evaluation methodology, with results presented in Table 1.

Llama series models exhibit the most effective safety alignment and defense mechanisms against jailbreak attacks, rendering them the most credible target models in such research. Nevertheless, our method achieved an attack success rate exceeding 50 percent on Llama3.1. Experimental results demonstrate that our approach outperformed state-of-the-art jailbreak methods on both Llama3.1 and GPT-4, with performance on Qwen2.5 marginally below DrAttack. This indicates the efficacy of our jailbreak methodology. Additionally, comparative results with and without iterative optimization were provided, confirming that the transition question iterative optimization stage substantially enhanced the method’s performance.

# D. Ablation Study

We conducted jailbreak attacks with and without iterative optimization. Results indicate that iterative optimization substantially improves attack effectiveness. Another core aspect of our method is relational decomposition, which generates sub-questions to accumulate relevant knowledge through the QA process. This knowledge then supports answering the original query. This design is based on our earlier conjecture: when provided with sufficient contextual information, large models are more likely to compose answers from that context rather than reasoning independently. We performed verification experiments to confirm this.

We sample 50 QA pairs from Squad [25], each comprising distinct materials, questions, and answers, to construct a correct material-based QA dataset. For each question, we instructed a large language model to modify the corresponding answers in the materials, producing an incorrect material-based QA dataset. GPT-4o was subsequently tested on both datasets through multiple rounds of question–answering. In each round, the model first read and processed the provided material before answering the associated question. We compared its responses with the ground truth to determine correctness and calculate accuracy. Additionally, we conducted single-turn QA experiments with direct questions to examine the model’s dependence on contextual knowledge. The same questions and evaluation criteria were applied across all settings to ensure fairness. The experimental results are shown in Fig. 3.

![](images/8f7b2e2a13cd5e4f9116d25ce77f2076c53d70c207230c31e5e7c302ddc7f55c.jpg)



Fig. 3. Accuracy results on different QA datasets.

Experimental results show that when answering the final question, the large model relies heavily on multi-turn dialogue context and tends to use this knowledge in its responses. The low accuracy on the incorrect material dataset indicates limited independent reasoning and a preference for contextual consistency.

# V. CONCLUSION

This paper presents GRED, a multi-round dialogue jailbreak attack framework based on entity extraction and relation reconstruction. By generating sub-questions and transition questions, it incrementally accumulates relevant knowledge and bypasses LLM safety mechanisms. Unlike prior methods, GRED anchors all steps—sub-question construction, transition generation, and optimization—to the original query, ensuring semantic and goal consistency. Experiments show that our approach achieves higher multi-round attack success rates and effectively targets state-of-the-art LLMs, demonstrating the value of entity–relation–entity structures in malicious question decomposition. We further analyze three representative successful cases to illustrate the mechanism behind its effectiveness and hope this work supports future research on jailbreak attacks and LLM security.

# REFERENCES

[1] Perez F, Ribeiro I. Ignore previous prompt: Attack techniques for language models[J]. arXiv preprint arXiv:2211.09527, 2022.   
[2] Yi S, Liu Y, Sun Z, et al. Jailbreak attacks and defenses against large language models: A survey[J]. arXiv preprint arXiv:2407.04295, 2024.   
[3] Wang R, Ma X, Zhou H, et al. White-box multimodal jailbreaks against large vision-language models[C]//Proceedings of the 32nd ACM International Conference on Multimedia. 2024: 6920-6928.   
[4] Chao P, Debenedetti E, Robey A, et al. Jailbreakbench: An open robustness benchmark for jailbreaking large language models[J]. Advances in Neural Information Processing Systems, 2024, 37: 55005-55029.   
[5] Mehrotra A, Zampetakis M, Kassianik P, et al. Tree of attacks: Jailbreaking black-box llms automatically[J]. Advances in Neural Information Processing Systems, 2024, 37: 61065-61105.   
[6] Deng G, Liu Y, Li Y, et al. Masterkey: Automated jailbreak across multiple large language model chatbots[J]. arXiv preprint arXiv:2307.08715, 2023.   
[7] Li X, Zhou Z, Zhu J, et al. Deepinception: Hypnotize large language model to be jailbreaker[J]. arXiv preprint arXiv:2311.03191, 2023.   
[8] Wang Y, Liu Q, Jin C. Is rlhf more difficult than standard rl? a theoretical perspective[J]. Advances in Neural Information Processing Systems, 2023, 36: 76006-76032.   
[9] Li H, Guo D, Fan W, et al. Multi-step jailbreaking privacy attacks on chatgpt[J]. arXiv preprint arXiv:2304.05197, 2023.   
[10] Chao P, Robey A, Dobriban E, et al. Jailbreaking black box large language models in twenty queries[C]//2025 IEEE Conference on Secure and Trustworthy Machine Learning (SaTML). IEEE, 2025: 23-42.   
[11] Jin H, Zhou A, Menke J, et al. Jailbreaking large language models against moderation guardrails via cipher characters[J]. Advances in Neural Information Processing Systems, 2024, 37: 59408-59435.   
[12] Chen Z, Zhao Z, Qu W, et al. Pandora: Detailed llm jailbreaking via collaborated phishing agents with decomposed reasoning[C]//ICLR 2024 Workshop on Secure and Trustworthy Large Language Models. 2024.   
[13] Liu Y, He X, Xiong M, et al. Flipattack: Jailbreak llms via flipping[J]. arXiv preprint arXiv:2410.02832, 2024.   
[14] Pawar S, Palshikar G K, Bhattacharyya P. Relation extraction: A survey[J]. arXiv preprint arXiv:1712.05191, 2017.   
[15] Xue Y, Wang J, Yin Z, et al. Dual intention escape: Penetrating and toxic jailbreak attack against large language models[C]//Proceedings of the ACM on Web Conference 2025. 2025: 863-871.   
[16] Mao Y, Cui T, Liu P, et al. From LLMs to MLLMs to Agents: A Survey of Emerging Paradigms in Jailbreak Attacks and Defenses within LLM Ecosystem[J]. arXiv preprint arXiv:2506.15170, 2025.   
[17] Zou A, Wang Z, Carlini N, et al. Universal and transferable adversarial attacks on aligned language models[J]. arXiv preprint arXiv:2307.15043, 2023.   
[18] Renze M. The effect of sampling temperature on problem solving in large language models[C]//Findings of the association for computational linguistics: EMNLP 2024. 2024: 7346-7356.   
[19] Yu J, Lin X, Yu Z, et al. Gptfuzzer: Red teaming large language models with auto-generated jailbreak prompts[J]. arXiv preprint arXiv:2309.10253, 2023.   
[20] Zhou Z, Xiang J, Chen H, et al. Speak out of turn: Safety vulnerability of large language models in multi-turn dialogue[J]. arXiv preprint arXiv:2402.17262, 2024.   
[21] Liu X, Xu N, Chen M, et al. Autodan: Generating stealthy jailbreak prompts on aligned large language models[J]. arXiv preprint arXiv:2310.04451, 2023.   
[22] Wei A, Haghtalab N, Steinhardt J. Jailbroken: How does llm safety training fail?[J]. Advances in Neural Information Processing Systems, 2023, 36: 80079-80110.   
[23] Li X, Wang R, Cheng M, et al. Drattack: Prompt decomposition and reconstruction makes powerful llm jailbreakers[J]. arXiv preprint arXiv:2402.16914, 2024.   
[24] Russinovich M, Salem A, Eldan R. Great, now write an article about that: The crescendo multi-turn llm jailbreak attack[J]. arXiv preprint arXiv:2404.01833, 2024, 2(6): 17.   
[25] Rajpurkar P, Zhang J, Lopyrev K, et al. Squad: 100,000+ questions for machine comprehension of text[J]. arXiv preprint arXiv:1606.05250, 2016.