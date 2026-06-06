# IoT-Brain: Grounding LLMs for Semantic-Spatial Sensor Scheduling

Zhaomeng Zhou1, Lan Zhang1,2,\*, Junyang Wang1, Mu Yuan3, Junda Lin1, Jinke Song4

1University of Science and Technology of China

2Institute of Artificial Intelligence, Hefei Comprehensive National Science Center

3The Chinese University of Hong Kong 4The Hong Kong University of Science and Technology

{zhouzhm, iswangjy, linjunda}@mail.ustc.edu.cn, zhanglan@ustc.edu.cn

muyuan@cuhk.edu.hk, jikesog@gmail.com

# ABSTRACT

Intelligent systems powered by large-scale sensor networks are shifting from predefined monitoring to intent-driven operation, revealing a critical Semantic-to-Physical Mapping Gap. While large language models (LLMs) excel at semantic understanding, existing perception-centric pipelines operate retrospectively, overlooking the fundamental decision of what to sense and when. We formalize this proactive decision as Semantic–Spatial Sensor Scheduling (S3) and demonstrate that direct LLM planning is unreliable due to inherent gaps in representation, reasoning, and optimization. To bridge these gaps, we introduce the Spatial Trajectory Graph (STG), a neurosymbolic paradigm governed by a "verify-beforecommit" discipline that transforms open-ended planning into a verifiable graph optimization problem. Based on STG, we implement IoT-Brain, a concrete system embodiment, and construct TopoSense-Bench, a campus-scale benchmark with 5,250 natural-language queries across 2,510 cameras. Evaluations show IoT-Brain boosts task success rate by 37.6% over the strongest search-intensive methods while running nearly 2× faster and using 6.6× fewer prompt tokens. In real-world deployment, it approaches the reliability upper bound set by reducing 4.1× network bandwidth, providing a foundational framework for LLMs to interact with the physical world with unprecedented reliability and efficiency.

# CCS CONCEPTS

• Computing methodologies → Artificial intelligence;   
• Computer systems organization → Sensor networks.

\* Lan Zhang is the corresponding author.

![](images/90b09ecc795544850570496f0d3e9c049ba5b02f0795d8cb5ef16de603c98264.jpg)

This work is licensed under a Creative Commons Attribution 4.0 International License.

MobiCom ’26, Austin, TX, USA

© 2026 Copyright held by the owner/author(s).

ACM ISBN 979-8-4007-2505-0/26/10

https://doi.org/10.1145/3795866.3796695

# KEYWORDS

Large Language Models, IoT Networks, Sensor Scheduling

# ACM Reference Format:

Zhaomeng Zhou1, Lan Zhang1,2,\*, Junyang Wang1, Mu Yuan3,, Junda Lin1, Jinke Song4 . 2026. IoT-Brain: Grounding LLMs for Semantic-Spatial Sensor Scheduling. In The 32nd Annual International Conference on Mobile Computing and Networking (MobiCom ’26), October 26–30, 2026, Austin, TX, USA. ACM, New York, NY, USA, 16 pages. https://doi.org/10.1145/3795866.3796695

# 1 INTRODUCTION

The proliferation of large-scale sensor networks in smart cities and industries is catalyzing a paradigm shift towards intelligent automation[40, 47, 54]. This leap from traditional coverage-driven optimization[11, 31, 57, 74] to real-time semantic goal satisfaction introduces a profound, yet underexplored challenge. A simple request like "Can you help me check my wallet between the library and the gym?" exposes a stark divide between the vagueness of human language and the precise physical operations a sensor network must execute. We term this the Semantic-to-Physical Mapping Gap (Fig. 1(a)), a fundamental hurdle that renders conventional task-specific models and rigid scripts ineffective.

The advent of large language models (LLMs) has provided a powerful engine for semantic interpretation [18, 25, 48, 51], offering a promising path forward. Recent work on "Penetrative AI" further shows that LLMs can reason directly over raw sensor data [17, 58, 75, 80]. Yet these advances largely remain within operates retrospectively, assuming the relevant sensor streams are already available, what we term Reactive Perception (Fig.1(c)). This perspective overlooks a more fundamental upstream challenge, Proactive Scheduling, that is paramount in large-scale deployments. Before any meaningful perception can occur, LLMs must decide what to sense and when to attend. The decision precedes and enables all subsequent perception but has received limited systematic study [5, 34, 41]. We formalize this pivotal challenge as the Semantic–Spatial Sensor Scheduling (S3) problem.

![](images/ac3fa7cc6cf1b1967a12e65bcd0e2c517f332f72886f1a822d08821a003d08cf.jpg)



(a) The Semantic-to-Physical Mapping Gap.

![](images/e1319be7a8cff8c5bb965adb23e90b97acdf0eb9c7a7ee20235242b326fec394.jpg)



(b) Limitations of conventional approaches.   
![](images/3fff3ca7c891fc0fadffd5e25225c2a9508009108163028eae5878247c439107.jpg)



(c) LLM-driven Perception and Scheduling.   
Figure 1: The challenge of the S3 problem.

Solving the S3 problem with off-the-shelf LLMs is far from straightforward. Our preliminary study (§2.2) tasks an LLM with end-to-end scheduling in a real-world topological environment, revealing three fundamental challenges:

(1) Symbol-to-Semantic Chasm. LLMs’ native shortcoming in comprehending raw, machine-oriented symbolic topologies prevents them from building an effective world model, slashing their planning success by over 5× compared to when provided with structured, human-readable knowledge.   
(2) Inferential Leap from Points to Paths. LLMs’ profound difficulty in inferring topological relationships like connectivity from disconnected symbols causes even a perfectly informed model to achieve merely 26% trajectory coverage, leading to fragmented and unsound paths.   
(3) Optimization Shortfall in LLM Planning. The inherent "satisficing" nature of LLMs leads to resource-heavy plans, exhibiting up to 45% redundant sensor overlap even with structured guidance and compounding to a staggering 48× token overhead when processing raw symbolic data.

Core idea: verify-before-commit. This work aims to bridge the gap between an LLM’s high-level semantic reasoning and the need for resource-efficient, physically grounded sensor scheduling. Our insight stems from observing LLMs’ native behavior on the S3 problem, showing that their plans are often ungrounded and glaringly misaligned with sensornetwork constraints. By contrast, when supplied with prevetted, task-relevant topological knowledge, LLM-derived plans become both reliable and efficient. Such oracle-like access, however, is infeasible in dynamic deployments. In resource-sensitive environments, executing a speculative, unverified plan is prohibitively expensive. We therefore adopt a paradigm in which the LLM must proactively and autonomously discover and validate the necessary grounding knowledge through direct interaction with the physical world before any operational decision is taken. We term this disciplined approach "verify-before-commit", a principle requiring that all semantic hypotheses be fully validated against reality before they are deemed executable.

STG design. The "verify-before-commit" principle’s progressive translation of high-level intent into concrete action inherently embodies a search for an optimal topological pathway within semantic constraints. This complex search process mirrors the established paradigm of graph construction[14, 69, 77], which we formalize as the Spatial Trajectory Graph (STG), a neurosymbolic paradigm that operates through a systematic, multi-stage workflow. The paradigm first mandates the structuring of ambiguous intent into a verifiable, hypothesized graph. It then requires grounding of the graph through an iterative validation loop against a physical world model, methodically transforming uncertainty into verified facts. Finally, the paradigm concludes with the optimization of the now-verified graph into a resource-aware, dynamic execution plan. This principled decomposition systematically separates semantic interpretation from deterministic validation and scheduling.

IoT-Brain Implementation. We implement the STG paradigm in IoT-Brain, a system engineered for robust, realworld interaction. Instead of a monolithic pipeline, IoT-Brain adopts a modular architecture that leverages an LLM’s advanced tool-calling and programming capabilities[33, 56]. It employs a reactive, tool-based loop to continuously ground its semantic reasoning against our physical world model, effectively transforming abstract hypotheses into verifiable facts. This design strategically decouples the LLM’s highlevel semantic inference from the deterministic, resourceconscious tasks of scheduling and sensor control. The entire workflow is further accelerated by shared memory modules that cache executable reasoning evidence, amortizing the cost of interaction across sessions. To evaluate IoT-Brain, we also constructed TopoSense-Bench, a large-scale benchmark tailored to the S3 problem featuring a university-scale digital twin with 2,510 cameras and 5,250 real-world queries.

Contributions of our work are summarized as follows:

• We identify and formalize the S3 problem, a critical yet overlooked challenge in intent-driven sensor networks, and introduce the Spatial Trajectory Graph (STG), a neurosymbolic paradigm that grounds LLM reasoning in a verifiable, physical-world structure.   
• We design and implement IoT-Brain, our concrete system instantiation of STG, and we construct and release TopoSense-Bench, a large-scale benchmark with 5,250 realworld queries to catalyze future research in this domain.   
• We conduct evaluations of IoT-Brain on our TopoSense-Bench and a physical testbed. Experimental results demonstrate the superiority of STG. On the benchmark’s most complex tasks, IoT-Brain boosts task success by 37.6% over the strongest search-intensive methods[13, 55] while running nearly 2× faster and using 6.6× fewer prompt tokens. Furthermore, in live deployments, our system approaches the reliability of a resource-agnostic upper-bound approach while consuming 4.1× less network bandwidth.

# 2 BACKGROUND & MOTIVATION

We first survey the sensor-scheduling landscape, contrasting coverage-driven methods with emerging LLMs’ capabilities to expose a critical gap (§2.1). Then we present a preliminary study that decomposes LLM-based proactive scheduling into three fundamental gaps (§2.2). Next, we motivate a new planning paradigm that addresses these gaps (§2.3).

# 2.1 Background

Classical research in sensor networks has centered predominantly on coverage-driven optimization tasks, such as maximizing sensor coverage or tracking objects within a static, pre-defined field-of-view [11, 12, 36]. While effective for welldefined engineering objectives, this paradigm is fundamentally ill-suited for intent-driven queries specified in ambiguous natural language. In practice, such ad-hoc semantic tasks are often relegated to rudimentary solutions, typically relying on laborious human-in-the-loop operations [27, 45, 53] or brittle fixed-topology scripts [10, 29]. As illustrated in Fig. 1(b), both approaches break down in large-scale, dynamic settings [63, 66, 73]. Manual operation does not scale [19], and hard-coded scripts fail to generalize to the fluid and unpredictable nature of human intent [49, 68].

The emergent semantic understanding of LLMs offers a promising route beyond these historical limits. Pioneering systems show LLMs can parse complex sensor data and interact with the physical world, opening a new frontier for AIoT [17, 22, 58, 61, 80]. Yet, the current LLM-for-AIoT landscape is structurally imbalanced. As shown in Fig. 1(c), most work concentrates on Reactive Perception, where models passively analyze pre-collected sensor streams. We instead tackle Proactive Scheduling, the upstream problem of deciding precisely which sensors to activate and when. This shift from passive interpretation to active, goal-directed participation is essential for truly autonomous AIoT systems, and the transition is nontrivial, exposing fundamental challenges in reliably grounding LLM reasoning in the physical world.

# 2.2 Preliminary Study

To dissect why the leap from perception to scheduling is challenging for LLMs, we conducted a preliminary study designed to answer a core question. Can LLMs effectively plan routes and schedule sensors when given raw, symbolic topological data? To investigate this, we constructed a dedicated testbed using real-world topological data from Open-StreetMap (OSM) [26], encompassing five multi-scenario buildings and a set of 373 manually curated queries that require both spatial understanding and path planning.

We compared two approaches. In the Naive setting, the LLM is prompted directly with machine-oriented OSM text (e.g., XML-like nodes and ways), and is asked to produce a sensor activation plan. In the Oracle setting, which serves as an upper bound, the same symbolic data is preprocessed into a structured, human-readable knowledge base that makes locations, connections, and salient features explicit (see Fig. 2(a)) for which the LLM then uses for reasoning. We assessed each approach on its ability to produce correct and efficient schedules, measuring scenario coverage, trajectory coverage, resource overlap, and token consumption. The results, summarized in Fig. 2(b), reveal three tightly coupled gaps that together impede reliable LLM-based scheduling.

Gap 1: Symbol-to-Semantic Chasm. The disparity between the Naive and Oracle settings reveals a fundamental representation mismatch. The quantitative impact of this chasm is stark. When the LLM is provided with structured, human-readable knowledge, scenario coverage boosts by over 2.1× on single-scenario tasks and a remarkable 5× on multi-scenario tasks compared to the baseline Naive approach. Because LLMs are trained on natural language rather than machine-oriented symbolic topologies, they struggle to effectively parse OSM-style structures [20, 21, 59] and therefore cannot assemble a usable world model. Planning performance consequently collapses, underscoring the need for a dedicated symbol-to-semantic translation layer.

Gap 2: Inferential Leap from Points to Paths. Trajectory coverage lays bare a deeper reasoning failure. In the Naive setting, it is essentially zero. Even with an explicit, intelligible map, the Oracle reaches only 26% on multi-scenario tasks. This shortfall reflects a deficit in multi-step path formation across large topologies. LLMs can reference named places and operate over simple pre-specified graphs, yet they rarely assemble the connectivity constraints that turn local doorways into a valid end-to-end route. Rather than simply providing structured data and expecting a correct plan, a practical system must actively scaffold reasoning by constructing connectivity, verifying reachability, and validating long-horizon trajectories within the spatial graph.

![](images/07359866d28eccbf7a39301378abb5f78c8fd7ec1338d4f1938dff149188f996.jpg)



(a) From raw symbols to structured knowledge.

![](images/41d9b62f5d972ed733675270f595dc7bb00be90994cabce6a454a3b538a241eb.jpg)



![](images/85b011bcbcafa15c6da91f2642a5d21815daf934f80ed8e8cbf5988b35dd0e3c.jpg)



(b) Empirical planning failures.   
Figure 2: The representation gap and resulting planning failures.

Gap 3: Optimization Shortfall in LLM Planning. Beyond representation and reasoning, planning quality falters at the optimization level. Even with perfect topological semantics, the Oracle still yields inefficient schedules, with overlap reaching 45%. Without structured guidance, the inefficiency compounds dramatically. On multi-scenario tasks, the Naive setting expends a staggering 48× more tokens than the Oracle. These patterns clearly indicate LLMs inherently tend to satisfice rather than optimize, producing plausible yet resource-heavy plans [42, 72]. Therefore, a practical system should capitalize on LLM’s semantic strengths while delegating global resource efficiency to deterministic algorithms[6].

# 2.3 Motivation & Core Ideas

The preceding findings yield a crucial insight that constructing a reliable and efficient semantic scheduling system cannot simply treat the LLM as an unconstrained, end-to-end black-box planner. These inherent, fundamental gaps in representation, reasoning, and optimization necessitate a novel paradigm to explicitly structure and guide the LLM’s role.

This motivates our core idea to replace monolithic opaque planning with a structured and verifiable workflow centered on the Spatial Trajectory Graph (STG). Our neurosymbolic STG paradigm decomposes the intractable scheduling problem into a principled three-stage process, each instantiated by a corresponding phase in our IoT-Brain system. 1) Intent Formalization (§4.2) first leverages an LLM’s semantic competence to translate a user’s ambiguous query into a hypothesized STG, a structured but unverified blueprint of intent. 2) Feasibility Grounding (§4.3) then enters an iterative "verify-before-commit" loop where each element of the blueprint is systematically validated against the physical world model until a fully consistent and grounded STG is produced. 3) Optimal Synthesis (§4.4) finally compiles the now-verified blueprint into a resource-optimal sensor activation plan and executes it adaptively using a perception-in-the-loop mechanism to handle unfolding real-world dynamics. The multistage process provides a systemically verifiable solution for LLM-based grounding, making a significant step towards enabling truly intelligent AIoT systems.

# 3 S3 AND STG FORMULATION

We first formally define the Semantic–Spatial Sensor Scheduling (S3) problem as a principled mapping from high-level user intent to a resource-aware dynamic activation plan (§3.1). Building on this formulation, we introduce the Spatial Trajectory Graph (STG), a paradigm that grounds free-form language into an optimization-ready spatial graph to systematically address this fundamental challenge (§3.2).

# 3.1 The S3 Problem

Environment and Query. We consider a large, densely instrumented site where a user issues a natural language query $Q _ { N L }$ . The environment is represented by a comprehensive world model $W = ( \mathcal { G } _ { \mathrm { s p a t i a l } } , \mathcal { G } _ { \mathrm { s e n s o r } } , \Phi )$ where $\mathcal { G } _ { \mathrm { s p a t i a l } }$ is a labeled spatial graph of locations and traversability, $\mathcal { G } _ { \mathrm { s e n s o r } }$ is a device graph of sensors and their capabilities, and Φ links the two by encoding sensor visibility and geometry.

Semantic Compilation. Given $Q _ { \mathrm { N L } }$ and ?? , semantic compilation yields a set of verifiable spatiotemporal predicates $\Omega ( Q _ { \mathrm { N L } }$ , ?? ) specifying anchors, regions, relational constraints, and temporal bounds $( \mathbf { e . g . , } ^ { \mathsf { " } } 1 1 . 3 0 \mathrm { a . m . " } )$ . Let Π(Ω) denote the spatiotemporal witnesses, the trajectories that must be observed within a specific timeframe to satisfy the query.

Plans and Objective. Answering the query requires generating a dynamic activation plan $P ( t )$ , a time-varying set of sensors intended to reconstruct a witness trajectory $\tau \in \Pi ( \Omega )$ . A plan is feasible if its collective observation over time, denoted as $\textstyle { \mathcal { P } } = \bigcup _ { t } P ( t )$ , completely covers at least one witness ??. The objective is to find an optimal plan $P ^ { * } ( t )$ that maximizes a fidelity-cost trade-off, formalized as:

$$
P ^ {*} (t) = \underset {P (t) \subseteq \mathcal {G} _ {\text { sensor }}} {\arg \max} \left(\mathcal {F} (\mathcal {P}; \Pi (\Omega), \Phi) - \lambda \int \operatorname{Cost} (P (t)) d t\right), \tag {1}
$$

where fidelity $\mathcal { F }$ measures the quality of the reconstructed trajectory, monotonically increasing with its completeness and accuracy. The $\mathrm { C o s t } ( P ( t ) )$ function captures all resource expenditures, including the number of active sensors, activation duration, and redundant spatial overlap.

Inherent Requirements. While Eq. 1 specifies the optimization objective, solving it directly with off-the-shelf LLMs is intractable given the model’s intrinsic computational limits. Informed by our preliminary study (§2.2), a viable LLM-based approach must satisfy three fundamental requirements to align model capability with rigorous problem demands. 1) Semantic Grounding. The solution must anchor the LLM’s linguistic outputs to the physical world. Fuzzy descriptions like "near the main entrance" must be unambiguously resolved to concrete spatial entities in $W$ to become actionable. 2) Topological Feasibility. The solution must enforce topological validity on the LLM’s generated plans. Any long-horizon trajectory ?? must be explicitly verified as physically traversable within $\mathcal { G } _ { s p a t i a l }$ , precluding the LLM from simply hallucinating impossible paths. 3) Resource Efficiency. The solution must decouple planning from optimization. Given that LLMs are satisficers, not optimizers, a practical system must delegate the selection of a resource-efficient schedule to specialized deterministic algorithms. These requirements motivate a paradigm that structures and constrains the LLM’s role, moving beyond brittle end-to-end planning.

# 3.2 The STG Paradigm

End-to-end sensor selection couples semantics, topology, resources, and timing, hindering verification of intermediate assumptions. To make decisions verifiable and cost-aware, we introduce STG. STG decouples semantic interpretation, topological grounding, and resource optimization by inserting an explicit spatiotemporal trajectory graph where candidate hypotheses are checked before commitment. This blueprint transforms a user’s intent into a structured trajectory, the trajectory into verified spatiotemporal facts, and these facts into an optimized, dynamic activation schedule.

STG Definition. An STG is a quadruple $G = ( V , E , \tau _ { V } , \sigma _ { t } )$ that provides a verifiable specification for a dynamic plan. It comprises: (i) a connected subgraph $( V , E )$ of relevant locations; (ii) a verified spatial witness path $\tau _ { V } = \left( v _ { 1 } , \dots , v _ { m } \right)$ that satisfies the spatial predicates; and (iii) a dynamic sensor scheduling function $\sigma _ { t } ,$ , which maps each spatial node $v _ { i } \in \tau _ { V }$ to a set of sensors to be activated at a dynamically determined time $t _ { i }$ . The induced dynamic plan is thus $P ( t ) = \sigma _ { t } ( v _ { i } )$ for $t = t _ { i } . \mathrm { A n } S T G$ is hypothesized $\left( G _ { 0 } \right)$ when its spatial path $\tau _ { V , 0 }$ is unverified, and becomes grounded $( G _ { \star } )$ only after $\tau _ { V }$ is validated against the world model ?? .

Objective Reparameterization. The STG structure recasts the original optimization over dynamic plans $P ( t )$ as a more tractable, two-stage process. First, it searches over the space of grounded spatial paths $( \mathcal { G } _ { \star } )$ to find an optimal $\tau _ { V } ^ { * }$ . Second, it determines the optimal temporal scheduling $( \sigma _ { t } ^ { * } )$ along that path. The objective is formalized as:

$$
(\tau_ {V} ^ {*}, \sigma_ {t} ^ {*}) = \arg \max _ {(\tau_ {V}, \sigma_ {t})} \Big (\mathcal {F} (\tau_ {V}, \sigma_ {t}) - \lambda   \mathrm{Cost} (\tau_ {V}, \sigma_ {t}) \Big), \tag {2}
$$

where the optimal dynamic plan $P ^ { * } ( t )$ is derived from $( \tau _ { V } ^ { * } , \sigma _ { t } ^ { * } )$ This reframing is pivotal because it separates the verifiable, static spatial planning from the adaptive, online temporal scheduling, making the problem tractable.

Principled Inference Workflow. The reframing supports a three-stage workflow guided by the "verify-before-commit" principle. i) Intent Formalization. From the user query, construct an ungrounded graph $G _ { 0 }$ populated with candidate locations and a hypothesized spatial path $\tau _ { V , 0 } .$ . ii) Feasibility Grounding. Enter an iterative loop that validates spatial hypotheses in $\tau _ { V , 0 }$ against the world model $W ,$ disambiguates semantics, and enforces topological feasibility until a fully grounded spatial path $G _ { \star }$ emerges. iii) Optimal Synthesis. On the grounded path $G _ { \star } ,$ , compute the optimal dynamic scheduling function $\sigma _ { t } ^ { * }$ maximizes the objective in Eq. 2. This yields a verifiably resource-aware dynamic activation plan $P ^ { * } ( t )$ . Within this workflow, the LLM proposes and refines spatial hypotheses, while the correctness of the spatial path and the optimality of the spatiotemporal schedule are secured by explicit checks and deterministic solvers.

# 4 IOT-BRAIN SYSTEM ARCHITECTURE

To instantiate the STG paradigm, we implemented IoT-Brain, a modular framework that turns high-level semantic queries into verifiable, resource-aware sensor activation plans. As depicted in Fig. 3, IoT-Brain follows a three-stage pipeline comprising Semantic Structuring (§4.2), Symbolic Grounding (§4.3), and Adaptive Execution and Perception (§4.4).

# 4.1 System Workflow

IoT-Brain takes two inputs, a natural language query $Q _ { \mathrm { N L } }$ and a world model ?? combining detailed spatial knowledge with a sensor-network map, and processes them through a structured and verifiable three-stage pipeline.

Semantic Structuring. The workflow employs three LLM agents as one-shot planners using system prompts. First, the Topological Anchor ➊ extracts geographical entities to map textual mentions in $Q _ { \mathrm { N L } }$ to spatial graph nodes, seeding a scaffold. Building on this, the Semantic Decomposer ➋ factors the goal into a logical witness walk of atomic sub-tasks. To bridge high-level plans and physical constraints, the Spatial Reasoner ➌ analyzes transitions to formulate verifiable hypotheses regarding topological connectivity and attributes.

Symbolic Grounding. To validate these hypotheses, the Grounding Verifier ➍ operates as an agent in an iterative Thought-Action-Observation loop [79]. It translates abstract hypotheses into concrete checks by invoking our customcrafted deterministic Verifying Toolkit, a Python library designed to query the explicit geometry and sensor coverage within ?? . This rigorous loop prunes topologically infeasible branches until a consistent grounded graph emerges. Verified facts are cached as system-wide topological consensus in Spatial Memory ➎ to accelerate future lookups.

![](images/1d03e1b0cadc5c3840311fd729f836fac9220bf8686258627ae3ad6feaf0e983.jpg)



Figure 3: The system overview and workflow of IoT-Brain.

Adaptive Execution and Perception. With the verified graph, the Scheduling Synthesizer ➏ acts as a graph-to-code compiler, generating a Python script that invokes heuristic solvers from the Execution API Pool for resource-optimal scheduling. Successful scripts are cached in Programming Memory ➐ for in-context reuse [43, 82]. The Perception Aligner ➑ then executes this schedule through a coordinated pipeline: a VLM first grounds the text description to a visual target, passing the visual embedding to a Re-ID network for crosscamera association, while a Kalman-ETA filter [3] predicts arrival times to trigger downstream sensors just-in-time.

# 4.2 Intent-to-Blueprint Structuring

The initial phase of IoT-Brain converts the unstructured user query ??NL into a structured representation of intent and context. This process, termed Semantic Structuring, progressively builds a hypothesized STG, which is a machine-interpretable blueprint derived from the query but not yet verified against the world model. Fig. 4 depicts the three-agent pipeline, illustrated using the "lost backpack" query.

➊ Topological Anchor. The pipeline begins with the Topological Anchor, a coarse-grained parser that identifies the spatial scope of the user’s intent. By leveraging topological priors, the agent instantiates a candidate subgraph containing both explicitly mentioned locations and implicitly required transition points. For the running example, the agent identifies the defined starting public communication area

![](images/8413c8f5205b01506c5e483aec1307445f2209a9bab49c2687000fd08715e773.jpg)



Figure 4: Dataflow of the Semantic Structuring phase.

and the target destination testing laboratory, while simultaneously deducing necessary intermediate connectors, such as the Library elevator (shown as node\_2 in Fig. 4), required to bridge the vertical floor transition. These explicit and implicit geographical entities collectively form the initial, unverified vertices $V _ { 0 }$ and edges $E _ { 0 }$ of a nascent STG, effectively representing the initial structural hypothesis of the user’s underlying intended spatial context.

➋ Semantic Decomposer. While the Anchor provides disconnected spatial candidates, the Semantic Decomposer imposes order by factoring high-level intent into a sequence of atomic operations mapped to these nodes. This step ensures topological coherence by constructing a valid traversal that chains these entities, such as planning a continuous route from the starting Library 4F through inferred connectors like the Elevator to the Hospital 1F. This process defines the spatial witness walk $\tau _ { V , 0 } = ( v _ { 1 } , \dots , v _ { m } )$ , enriching the graph with a hypothesized trajectory and task annotations.

![](images/26a1f715fdf850d607f8136fa3914175180fa6191906399d14b7d51f24152e54.jpg)



Figure 5: Workflow of the Hypothesis-Verification Loop.

➌ Spatial Reasoner. However, this planned trajectory remains speculative as it relies on topological priors rather than grounded facts. Implicit assumptions arise wherever the semantic logic of the planner might diverge from strict physical availability (e.g., assuming a specific door is unlocked or a pathway is currently traversable). The Spatial Reasoner systematically bridges this gap by scrutinizing the entire generated trajectory to convert these implicit assumptions into explicit, verifiable hypotheses. In the context of the library-to-hospital transition, it detects potential ambiguity and hypothesizes that a specific, valid exit must be confirmed. Similarly, for the area covering task, it formulates hypotheses regarding the existence of specific facilities (e.g., "study desks") to narrow the sensing scope precisely.

Each hypothesis is cast as a concrete, verifiable proposition regarding the world model, defined with explicit scope and admissible evidence sources. This three-agent pipeline collectively returns a comprehensive hypothesized spatial path, encapsulated in an initial STG, $G _ { 0 } = ( V _ { 0 } , E _ { 0 } , \tau _ { V , 0 } , \emptyset )$ , fully ready for the Symbolic Grounding phase.

# 4.3 Hypothesis-to-Fact Grounding

A detailed hypothesized graph remains non-actionable as long as its elements are unverified. The Symbolic Grounding phase converts the speculative STG, ??0 into a grounded STG, $G _ { \star }$ by rigorously testing each hypothesis against the world model ?? . As shown in Fig. 5, a "verify-before-commit" loop promotes facts, prunes contradictions, and resolves ambiguities until the graph is verifiably consistent with ?? .

➍ The Hypothesis-Verification Loop. Grounding hinges on a rigorous verification loop executed by the Grounding Verifier, operating as a tool-using agent capable of querybased interaction with the physical world model. Its primary responsibility is to eliminate ambiguity by converting semantic assumptions into verifiable topological facts. Through a Thought-Action-Observation cycle [64, 79], the agent addresses specific node hypotheses, such as identifying

a valid exit in the Library, translating them into designing a corresponding topological verification query. It executes this design via invoking the crafted Verifying Toolkit (e.g., doors\_verify()) to retrieve concrete spatial data. The resulting observation serves as ground truth, enabling the agent to define the precise sensor scheduling logic for that location and progressively transform the speculative skeleton into a fully grounded STG.

Resolving Ambiguity. A critical challenge emerges when the retrieved observation is not definitive, such as the toolkit returning multiple valid exits for the Library. To resolve the uncertainty deterministically, IoT-Brain employs a recursive reasoning strategy based on topological consistency. Upon detecting multiple potential exits, the agent initiates a secondary check to evaluate the connectivity of each candidate relative to the subsequent waypoint (the Hospital). By filtering out exits that lack a valid traversable path to the destination, the system autonomously identifies the topologically sound option. This heuristic ensures the final plan is physically executable without human intervention, though an optional interactive strategy is available for extreme cases where user clarification is preferred.

➎ Amortized Verification via Caching. Throughout the iterative process, successfully verified facts are cached according to their associated locations in a Spatial Memory module, a technique inspired by classic indexing and memoization [38]. This mechanism amortizes the cost of repeated queries for the same entities (e.g., retaining the validated Library exit details for future requests), significantly accelerating future verification. The verification loop terminates once all hypotheses in $G _ { 0 }$ are resolved. The final output $G _ { \star }$ represents a verified spatial blueprint where every node, edge, and the contained spatial path ???? are consistent with the physical world, providing a reliable foundation for the subsequent scheduling optimization.

# 4.4 From Plan to Optimized Action

With a fully grounded spatial blueprint $G _ { \star }$ in place, the final phase of IoT-Brain translates it into dynamic action and perception in the physical world. The workflow comprises two components to achieve resource optimization synergistically. The first is a deterministic compiler that synthesizes an executable and resource-aware plan. The second is an adaptive executor that manages real-time operation.

![](images/3d7c76345fa7593fe6cc1121e7d88c9ba8a80093722e161cb28bd726c408fbd3.jpg)



Figure 6: Workflow of the Perception Aligner.

➏ Scheduling Synthesizer. With the verified spatial blueprint $G _ { \star }$ established, the Scheduling Synthesizer translates the plan into optimized action. Functioning as a graph-tocode compiler, it transforms the grounded nodes and edges into an executable Python script. This stage operationalizes the resource optimization objective in Eq. 2 by mapping the verified sub-tasks to specialized functions within our Execution API Pool. Consequently, the validated path segment inside the Library is processed by generating a call to indoor\_path\_camera\_search(), which utilizes a deterministic set-cover algorithm [86] to select the minimal sensor set required for full visibility. By embedding these solvers within a deterministic API layer, the compiler ensures the final schedule strictly honors the topological constraints verified in the previous phase while maximizing resource efficiency. Successful query–script pairs are cached in Programming Memory ➐ to accelerate future compilations on semantically-related tasks.

➑ Perception Aligner. A static script is insufficient for dynamic, real-world execution. The Perception Aligner therefore operates as an online executor, tightly coupling perception with control to keep only necessary sensors active. As depicted in Fig. 6, the process commences with target grounding, where a VLM anchors the user’s textual description of the "white backpack" to a specific visual instance in an initial video frame [32, 65]. To solve the association problem of maintaining the target’s identity across a distributed camera network, we employ a robust feature extractor (e.g., a Re-ID network) to match visual appearances [28]. Concurrently, a predictive model (e.g., a Kalman filter) estimates arrival times at downstream viewpoints along the planned route, enabling just-in-time sensor activation to optimize resource

usage [8, 76, 81]. Finally, the same VLM performs continuous verification, conducting frame-level reasoning to evaluate task predicates. This allows the system to intelligently decide when the query is satisfied, triggering early termination to conserve resources [4]. This unified loop reduces overhead by activating sensors only when needed and deactivating them once sufficient proof is obtained.

# 5 EVALUATION ON TOPOSENSE-BENCH

We conduct a comprehensive evaluation on our large-scale benchmark, TopoSense-Bench, to empirically validate the STG paradigm and quantify the performance of IoT-Brain. Our highlights are as follows:

• IoT-Brain delivers superior reliability and efficiency. On complex tasks, it boosts task success by up to 7.4× over the classical Hierarchical planner[23, 62] and runs nearly 2× faster with 6.6× fewer prompt tokens than the searchintensive Backtracking planner[13, 55] (§5.2).   
• IoT-Brain scales and generalizes well. Its verification overhead grows near-linearly with query complexity, not exponentially. Furthermore, its performance gains persist across diverse foundation models, confirming the benefits stem from our architecture, not a specific backbone (§5.3).   
• IoT-Brain derives strength from the full STG pipeline. Ablations confirm the synergy of its core components and reveal that unverified hypotheses are actively harmful, reinforcing "verify-before-commit" as a prerequisite for reliable physical-world planning (§5.4).

# 5.1 Experimental Setup

The TopoSense-Bench Benchmark. To rigorously evaluate our systems, we constructed TopoSense-Bench, a largescale benchmark for the $S ^ { 3 }$ problem. Its central design principle is semantic textualization, transforming raw OSM data into a structured knowledge base. We normalize ontological tags [2], generate hierarchical human-readable names [1, 37], and project geodetic coordinates into a site-local Cartesian frame, creating a unified substrate where physical topology and sensor capabilities are jointly considered. The benchmark instantiates a realistic campus spanning 33 buildings, 161 floor plans, and a dense network of 2,510 cameras.

Layered on this environment is a suite of 5,250 natural language queries grounded in the operational realities of large-scale sensor networks. Since providing spatiotemporal anchors is a realistic prerequisite for initiating tasks, the core $S ^ { 3 }$ challenge focuses on reasoning over the topological knowledge base to infer the complete, optimal sensor path between these points. To ensure high data quality, we employed a rigorous three-stage construction pipeline. Domain experts first authored ∼200 base templates per tier to cover realistic scenarios. Using these as seeds, GPT-o3 [52] synthesized thousands of distinct queries by instantiating diverse semantic intents across the complex campus topology.

![](images/b5ff8ddb8cdc83bfb3fdf09c4408c1da236cabeb9d5a0ba4b98e2a5673c81b4c.jpg)

Figure 7: Conceptual workflow comparison of agentic paradigms. We contrasts the brittle Hierarchical approach, the myopic Reactive agent, and the costly Backtracking planner with our structuring verifiable STG paradigm.   
![](images/769ef18c0b72fe5635ea5987feebaeb1fbf7ca2f43f807f12dc36798d00f58d0.jpg)  
Figure 8: The overall performance on TopoSense-Bench. We evaluate Hierarchical (Hi.), Reactive (Re.), Backtracking (Ba.), and IoT-Brain (Io.) across five task categories: T1.F (Focal Scene), T1.P (Panoramic), T2 (Intra-Building), T3.O (Open-Space), and T3.H (Hybrid). Metrics include task success rate, blueprint correctness, token usage, iteration rounds, and end-to-end latency. The legend displays the average performance for each paradigm.

Table 1: Statistics & Taxonomy of TopoSense-Bench. 

<table><tr><td>Knowledge Base Statistics</td><td>Value</td></tr><tr><td>Buildings / Floor Plans / Outdoor Segments</td><td>33 / 161 / 53</td></tr><tr><td>Total Topological Scenarios / Deployed Cameras</td><td>7,832 / 2,510</td></tr><tr><td>Query Dataset Statistics</td><td>Count (%)</td></tr></table>

Tier 1: Intra-Zone Perception 

<table><tr><td>T1.a: Focal Scene Awareness</td><td>1,433 (27.3%)</td></tr><tr><td colspan="2">e.g., &quot;verify activity near the door to room 5F 1&quot;</td></tr><tr><td>T1.b: Panoramic Coverage</td><td>1,129 (21.5%)</td></tr><tr><td colspan="2">e.g., &quot;how many people are in the conference hall?&quot;</td></tr></table>

Tier 2: Intra-Building Coordination 

<table><tr><td>T2: Intra-Building Coordination</td><td>988 (18.8%)</td></tr><tr><td colspan="2">e.g., &quot;I lost a notebook between lab-8 and lab-7&quot;</td></tr></table>

Tier 3: Inter-Building Coordination 

<table><tr><td>T3.a: Open-Space Coordination</td><td>946 (18.0%)</td></tr><tr><td colspan="2">e.g., &quot;track my path from the west gate to the tennis court&quot;</td></tr><tr><td>T3.b: Hybrid Indoor-Outdoor</td><td>754 (14.4%)</td></tr><tr><td colspan="2">e.g., &quot;I walked from building-1 to building-2...&quot;</td></tr></table>

Crucially, every resulting query underwent rigorous manual expert verification and ground-truth annotation to guarantee logical soundness and topological solvability, which ensures the benchmark’s high fidelity.

Compared Paradigms. We benchmark IoT-Brain against agentized implementations of three influential LLM planning paradigms. To ensure comparability, all systems use the same foundation LLMs and API toolkits, differing only in their reasoning and execution policies. (1) The Hierarchical

planner [23, 62] follows a decompose-then-execute strategy. It produces a complete, high-level plan upfront without intermediate verification, yielding speed at the cost of brittleness. (2) The Reactive planner [16, 79] instantiates the Thought-Action-Observation loop. It operates step-by-step, making it highly adaptive but often myopic on long-horizon tasks. (3) The Backtracking planner [13, 55] is inspired by depth-first search over a decision tree. It improves reliability by exploring multiple branches, but this expanded search typically incurs prohibitive inference costs and can commit to locally optimal yet globally inefficient paths. Fig. 7 contrasts these workflows with our STG approach.

Evaluation Metrics. We assess each paradigm’s performance from the dual perspectives of reliability and efficiency. We use a suite of standardized metrics: For reliability, we measure (1) task success rate (TSR), the percentage of queries yielding a functionally correct final answer, and (2) blueprint correctness (BC), which evaluates if a pre-execution plan is logically sound and topologically feasible, scored via an LLM-as-a-Judge protocol [83]. For efficiency, we quantify (3) inference cost, measured in total LLM tokens; (4) interaction rounds, the number of agent–LLM turns; and (5) end-to-end latency, the total time from query submission to final answer.

# 5.2 End-to-End Performance

Reliability Analysis. Fig. 8(a-b) presents the TSR and BC across all task categories and difficulty tiers. A key observation is that while baseline planners often struggle to translate symbolically correct plans into real-world success, IoT-Brain consistently maintains high TSR, especially as task complexity increases to long-horizon settings. This empirically demonstrates the STG paradigm’s effectiveness in resolving the fundamental gaps that plague end-to-end LLM planning.

![](images/0b69961dfd4fd185aa1dbf357069457b97e25d4826e89694c4d702f48746433e.jpg)



(d) Combined Component Ablation

![](images/fd81f285bb6146dbaa8cd537c7ceb64db6d3b5cce48bbed22dbd0425e4a6163d.jpg)



(e) Cached Scenarios

![](images/be78915a397abb49372fa39eac7186fe00c2332d7083dd21bd5a38d7ac536b85.jpg)



(f) Unverified Scenarios   
Figure 9: (a) & (d): Ablation study of IoT-Brain’s core components on single and multi scenario tasks. (A.: Anchor, R.: Reasoner, V.: Verifier, M.: Memory, S: Single-Scenario, M: Multi-Scenario). (b) & (c): Sensitivity to different LLMs. (GL.: GLM-4, Q.: Qwen-Max, D.: DeepSeek-V3, Ge.: Gemini-2.5-Flash). (e) & (f): Scalability with query complexity.

A notable paradox emerges on simple Tier 1 tasks. The plan-less Reactive planner achieves a strong TSR, demonstrating for simple tasks, adaptive tool-use can suffice in easy settings. The Hierarchical planner, by contrast, highlights the critical gap between symbolic planning and physical execution. It frequently produces plausible blueprints with high BC scores, yet achieves markedly lower TSR. This discrepancy reflects the representation and reasoning gaps, where a plan is logically sound on paper proves physically unrealizable without grounding in the real world. This confirms a correct blueprint is necessary but not sufficient for success.

As complexity escalates to Tier 2 and 3, the necessity of structured grounding becomes indisputable. The performance of all baseline planners degrades sharply, which is a clear manifestation of the reasoning gap. Their inability to construct coherent, long-horizon plans leads to systemic failure. In stark contrast, on the most complex T3.Hybrid task, IoT-Brain achieves a 46.1% TSR. This not only represents a more than 7.4× improvement over the Hierarchical planner’s 6.2% but also surpasses the strongest search-intensive alternative, the Backtracking planner, by 37.6%. This sustained performance is a direct result of STG’s "verify-before-commit" process, which constructs a globally coherent blueprint and systematically closes the reasoning gap.

Efficiency Analysis. Reliability must also be delivered efficiently. The computational overhead for each framework is reported in Fig. 8(c–d) show that the cost escalates with task complexity for unstructured planners, exposing an optimization gap. The Hierarchical planner is fast yet unreliable, while Reactive and Backtracking exhibit rapidly increasing token consumption and latency as complexity grows. In pursuit of reliability through exhaustive search, Backtracking reaches nearly 600 s on the most complex Tier 3 task.

IoT-Brain closes this gap by casting planning as constrained optimization on a verified graph, yielding a markedly different efficiency profile. Its resource use grows more smoothly with complexity. The principled verification loop is more focused than the brute-force exploration of Backtracking and less myopic than the trial-and-error of Reactive. While delivering superior reliability, IoT-Brain is nearly 2× faster on the most complex tasks and uses, on average, 6.6× fewer prompt tokens than Backtracking. These results show that the STG paradigm not only improves reliability but also provides a scalable path to computational efficiency, achieving a win-win in both correctness and cost.

# 5.3 Scalability and Sensitivity Analysis

Sensitivity to Foundation Models. To demonstrate that the benefits of STG are not tied to a single proprietary model, we evaluate IoT-Brain’s performance across four foundation LLMs. As expected, more powerful models yield higher endto-end reliability (Fig. 9(b)), confirming that the quality of the underlying LLM is a significant factor. More importantly, the efficiency profile shows no orders-of-magnitude variation in latency and token cost across models (Fig. 9(c)). While different APIs exhibit distinct latency characteristics, the token consumption remains relatively stable. These results indicate STG supplies a strong scaffold that channels reasoning into verifiable structure, allowing less capable models to perform competitively and confirming that observed gains arise from our architecture, not from any specific LLM’s capabilities.

Scalability with Query Complexity. We investigate how IoT-Brain’s computational verification overhead scales with query complexity, a key determinant of real-world usability.

For cached scenarios, verification overhead grows sublinearly, as the system intelligently reuses entries from Spatial Memory to amortize costs (Fig. 9(e)). In stark contrast, for novel, unverified scenarios, the number of verification rounds increases in a near-linear fashion purely dependent on the count of distinct locations referenced in the query, rather than the global environment size (Fig. 9(f)). This predictable and bounded growth stands in sharp contrast to the exponential combinatorial blowup typical of unconstrained planning and demonstrates the inherent scalability of our structured, hypothesis-driven verification process.

# 5.4 Ablation Study

Impact of Individual Components. Fig. 9(a) quantitatively shows the indispensable role of each component. Notably, removing the Grounding Verifier is catastrophic, causing the multi-scenario TSR to plummet below 10%, confirming the necessity of a "verify-before-commit" loop to prevent hallucination-prone planning. Removing the Spatial Reasoner also severely degrades performance, especially on complex tasks, as the Verifier is consequently forced into computationally expensive exhaustive checks without the Reasoner’s focused hypotheses. Similarly, omitting the Topological Anchor nearly halves multi-scenario TSR, underscoring its importance in providing the initial scaffolding for long-horizon plans. Finally, eliminating the Memory modules, while not impacting single-run TSR, nearly doubles latency in complex settings, demonstrating their critical value in efficiently amortizing repetitive verification costs.

Synergy of Combined Components. Fig. 9(d) underscores the components’ tight complementarity. A variant lacking all core modules performs as poorly as the Hierarchical baseline, with its multi-scenario TSR collapsing to 6.4%, confirming that the full pipeline is indispensable for robust behavior. More tellingly, a variant that isolates the Spatial Reasoner by removing its structuring and verification counterparts performs even worse, with its multi-scenario TSR dropping to a mere 5.1%. This result reveals a crucial, counter-intuitive insight that without validity checks, the Reasoner’s unverified hypotheses are not merely neutral but actively harmful, introducing strong, misleading biases that derail the entire planning process. Collectively, these results powerfully validate our philosophy that a structured, verifiable grounding process is not an add-on, but the fundamental prerequisite for safe and reliable physical-world planning.

# 6 EVALUATION ON A PHYSICAL TESTBED

We complement our benchmark results with an end-to-end evaluation of IoT-Brain in a large-scale, physical testbed. The experiments confirm the STG paradigm’s effectiveness in a real-world deployment, yielding a near-optimal balance of reliability and resource efficiency. Our highlights are:

![](images/1f71ed3207d54d8920182139610689faa49164ea35b24f8a501df4b191cdd8b4.jpg)



![](images/67af354590678179d7694a5a0c0adf6bd020882d241844768b3be19fe1c5370e.jpg)



Figure 10: The real-world testbed environment.

• IoT-Brain demonstrates strong resource efficiency, achieving a 49.84% TCR that approaches the reliability upper bound while using 4.1× less bandwidth and processing 4.2× fewer frames than the resource-agnostic method (§6.2).   
• IoT-Brain’s architecture is both efficient and robust. Latency profiling confirms its planning engine is swift, with dominant costs arising from task-intrinsic complexity. Being model-agnostic, the framework allows practitioners to flexibly balance performance, cost, and privacy by integrating diverse VLM backbones (§6.3).

# 6.1 Testbed Configuration

Physical Environment. Our real-world testbed is a largescale university campus instrumented with 2,510 Hikvision IP cameras distributed across 11 major areas. This diverse environment presents significant heterogeneity, where coverage ranges from sparse outdoor road networks to dense indoor deployments, with the Lab Building alone hosting 268 cameras covering complex topologies (see Fig. 10).

System Deployment. The IoT-Brain1 system runs on a centralized server equipped with two NVIDIA A100 GPUs. Its core planning engine utilizes the Gemini-2.5-Flash API[24] for efficient reasoning, while the Perception Aligner executes on-premises using a compact and efficient visual stack that includes YOLOv8[67] for real-time detection and PersonViT-B/16[30] for robust image re-identification. All components communicate over the standard campus Wi-Fi infrastructure, reflecting a practical deployment setting constrained by realistic bandwidth fluctuations.

# 6.2 Real-World Deployment Results

Evaluation Protocol. We evaluated end-to-end performance on 587 annotated real-world trajectories across three paradigms. In addition to our IoT-Brain framework, we considered two baselines to benchmark against both common practice and a theoretical optimum: (1) Static Scheduling, which mirrors conventional security practice by triggering downstream sensors using a constant-velocity pedestrian model[60], and (2) Naive Parallel Scheduling, a resource-agnostic upper bound that activates all potentially relevant cameras simultaneously. To ensure a controlled comparison, all vision–language queries were handled by a locally deployed Qwen-VL-Chat model[7].

Table 2: Real-World Scheduling Paradigm Comparison. 

<table><tr><td>Paradigm</td><td>TCR (%)</td><td>Latency (s)</td><td>Bandwidth (GB)</td><td>TFP (frames)</td></tr><tr><td>Static Scheduling</td><td>3.61</td><td>403.42</td><td>0.138</td><td>179</td></tr><tr><td>Naive Parallel</td><td>65.64</td><td>927.99</td><td>0.540</td><td>704</td></tr><tr><td>IoT-Brain (Ours)</td><td>49.84</td><td>413.69</td><td>0.131</td><td>166</td></tr></table>

Performance was measured using a comprehensive suite of metrics, including task completion rate (TCR), end-to-end latency, network bandwidth, and total frames processed (TFP). Performance Analysis. Tab. 2 highlights the trade-off between reliability and resource use. Static Scheduling is frugal yet brittle, reaching only 3.61% TCR and failing systematically whenever a target deviates from its pre-defined coverage. At the other extreme, Naive Parallel establishes an empirical upper bound on reliability at 65.64% TCR, but does so at untenable cost, consuming 4.1× more bandwidth and processing 4.2× more frames than our system.

IoT-Brain strikes an optimal balance within this trade-off. Driven by the STG paradigm for intelligent planning and the Perception Aligner for just-in-time execution, it achieves a high TCR of 49.84%, approaching the empirical upper bound, while keeping a resource footprint comparable to the far less reliable static strategy that uses the least bandwidth and processing the fewest frames among all paradigms. Its sequential, plan-informed activation prevents the heavy data and processing burden of parallel operation. The results confirm that verifiable planning coupled with perception-aligned execution yields a near-optimal balance, delivering robust reliability with exceptional efficiency. The remaining performance gap stems primarily from inherent semantic ambiguities, where vague user descriptions preclude deterministic grounding to the static topology. Furthermore, perception limitations contribute to sporadic failures, as the underlying VLM faces challenges in identifying targets under complex real-world lighting or occlusion.

# 6.3 System Analysis and Sensitivity

Latency Breakdown. We profiled the end-to-end latency for the IoT-Brain pipeline to characterize its temporal behavior. The breakdown in Fig. 11(a) clarifies the cost structure of complex semantic scheduling. The two dominant phases are Symbolic Grounding and V–L Inference, which account for most of the execution time on challenging Tier 2 & 3 tasks. The high cardinality of scenarios necessitates extensive verification cycles during grounding, while a larger scheduled sensor set increases the volume of frames for VLM inference. By contrast, the initial Semantic Structuring stage is remarkably efficient. Overall, this analysis reveals that the primary latency drivers are not inefficiencies in our planning engine, but rather the intrinsic complexity of the tasks, which demands substantial verification and perception effort. Sensitivity to VLM Foundation Models. The framework’s end-to-end performance is naturally influenced by the VLM selected within the Perception Aligner. To demonstrate architectural generality, we evaluate our framework with a spectrum of both local open-source and proprietary API-based VLMs. As shown in Fig. 11(b), the results reveal a clear and quantifiable performance–latency trade-off. Cloud-hosted API-based models such as Qwen-VL-Max achieve higher TCR but introduce significant network latency, whereas the lightweight open-source Qwen-VL-Chat offers lower latency with a corresponding reduction in TCR. This outcome underscores our framework’s inherent robustness. The STG paradigm, by decoupling planning from perception, is fundamentally model-agnostic, providing a stable planning scaffold that functions effectively regardless of the underlying VLM. The choice of foundation model thus becomes a configurable trade-off for deployers, allowing them to flexibly balance performance, cost, and data privacy.

![](images/deb8526397fd172b65c3cbfe712fbc61c162cc41473034c01ab33c01983a9519.jpg)



![](images/88d77567b6eecf388ec2f7eb2df79b03622f6a48cb8177c8087cf4d07e31b350.jpg)



Figure 11: System performance analysis.

# 7 DISCUSSION

Principles of Generalizability. Although our current instantiation centers on a camera network, the STG paradigm operates on a robust sensor-agnostic abstraction layer where nodes represent generic spatial coverage requirements rather than specific hardware interfaces. The LLM reasoning engine deals exclusively with logical predicates (e.g., is\_covered(location)), while the adaptation to specific sensing modalities occurs entirely within the deterministic Verifying Toolkit, which encapsulates the physical constraints. For instance, replacing a camera with a microphone array or a thermal sensor only requires updating the toolkit’s geometric calculation function to validate attributes like an acoustic detection radius or thermal sensing range instead of a visual field-of-view, while the high-level semantic planning logic remains structurally identical. This modularity empowers the framework to extend to diverse IoT scenarios (e.g., audio sensing [70] or thermal sensing [50]) without expensive retraining or fine-tuning of the core reasoning engine, though deployment in highly dynamic settings with frequent sensor outages would necessitate continual state updates [35].

System Deployment Effort. IoT-Brain is explicitly designed to streamline practical deployment and minimize engineering overhead through three strategic design choices.

First, regarding topological knowledge construction, our pipeline parses standard OSM data to semi-automatically generate the sensor-integrated topological representation (encoding attributes like FOV and sensing radius), limiting manual intervention primarily to the binding of specific sensor IDs. Second, regarding model tuning, the framework is fundamentally training-free by leveraging the one-shot or few-shot prompting strategies detailed in §4, thereby eliminating the need for expensive data collection or fine-tuning. Third, regarding algorithmic integration, the system adopts a "composition over creation" approach by wrapping existing off-the-shelf solutions. Specifically, it invokes standard optimization algorithms (e.g., ILP solvers) via the API pool and integrates established models (e.g., YOLO, ReID) into the perception module, significantly reducing the overall development and maintenance complexity.

Architectural Privacy-by-Design. Beyond simple policy compliance, privacy in IoT-Brain is an inherent result of its decoupled architecture. First, we enforce a principle of symbolic isolation where the planning LLM, even if cloud-based, operates solely on abstract text symbols such as Sensor\_01. Crucially, the model never accesses raw privacy-sensitive sensor streams like video, audio, or thermal data, effectively creating a structural privacy air-gap. Second, the system ensures rigorous data minimization through its optimization objective. This mechanism mathematically enforces that sensors are activated only for the strictly necessary spatiotemporal windows verified by the graph, rather than performing invasive persistent monitoring. This structural guarantee remains valid regardless of the sensing modality, providing a robust blueprint for privacy-preserving intelligent sensing aligned with strict organizational requirements [44, 46].

# 8 RELATED WORK

LLMs for Sensor System Control. Recent pioneering works have begun to explore using LLMs to translate high-level human intent into executable sensor actions, typically operating within strictly constrained smart-home settings [5, 34, 41]. To mitigate the model’s unpredictability, these approaches often rely on formal grammars or predefined API templates to enhance plan robustness. However, while such methods ensure syntactic validity, they fail to address the complexity of large-scale spatial reasoning. Our work differs fundamentally by tackling the twin challenges of campusscale scalability and physical-world grounding. We shift the research focus from ensuring small-scale execution robustness to achieving verifiable, resource-optimal scheduling in massive deployments, where resource contention and topological constraints are paramount.

LLM-based Agentic Planning. The advent of LLMs has catalyzed the development of sophisticated agentic planning frameworks, most notably including the Hierarchical [23, 62], Reactive [64, 79], and Backtracking [9, 55, 78] paradigms. These approaches excel at reasoning within reliable digital substrates, which are typically exemplified by software APIs or coding environments where execution feedback is immediate and deterministic. However, such methods lack the mechanisms to handle the ambiguity inherent in the physical world. Our work centers on grounding language-based reasoning in this noisy reality. To achieve this, STG functions as a rigorous neurosymbolic scaffold that constrains the LLM’s reasoning process through verifiable graph construction. This architecture supplies the essential guarantees needed for reliability in high-stakes embodied settings.

Language-Guided Perception. Historically, research in person re-identification has centered primarily on metric learning for image-to-image retrieval [15, 84, 85]. The recent introduction of large language models has enabled powerful cross-modal alignment, facilitating text-to-image reidentification and language-guided tracking in continuous video streams [39, 71]. Yet, most such studies presume a predefined, passive sensor stream or an exhaustively broad search space. Our Perception Aligner fundamentally challenges this passive paradigm by operating within a proactively scheduled, on-demand feed. It provides just-in-time verification to drive the next sensor activation, ensuring the system performs efficient, closed-loop active perception rather than relying on persistent, resource-intensive, and often unscalable open-domain tracking mechanisms.

# 9 CONCLUSION

We formalize Semantic-Spatial Sensor Scheduling (S3) and reveal critical gaps in LLM planning. To address these, we introduce STG, a "verify-before-commit" neurosymbolic paradigm that decouples semantic inference from deterministic scheduling. Our implementation, IoT-Brain, evaluated on our TopoSense-Bench benchmark and real-world deployment, demonstrates significant gains in both reliability and efficiency over representative planners. These contributions provide a practical blueprint for LLMs to translate high-level intent into correct physical action robustly.

# ACKNOWLEDGEMENTS

We thank the anonymous MobiCom reviewers and shepherd for their constructive comments. This research was supported by the China National Natural Science Foundation with No. 623B2093, No. 62441228 and Science and Technology Tackling Program of Anhui Province No.202423k09020016.

# REFERENCES

[1] 2025. Nominatim API Manual (latest). https://nominatim.org/releasedocs/latest/api/Overview/.   
[2] 2025. OpenStreetMap Taginfo. https://taginfo.openstreetmap.org/.   
[3] Avinash Achar, Dhivya Bharathi, B. Anil Kumar, and Lelitha Devi Vanajakshi. 2020. Bus Arrival Time Prediction: A Spatial Kalman

Filter Approach. IEEE Transactions on Intelligent Transportation Systems 21 (2020), 1298–1307. https://api.semanticscholar.org/CorpusID: 182478323   
[4] Aishwarya Agrawal, Jiasen Lu, Stanislaw Antol, Margaret Mitchell, C. Lawrence Zitnick, Devi Parikh, and Dhruv Batra. 2015. VQA: Visual Question Answering. International Journal of Computer Vision 123 (2015), 4 – 31. https://api.semanticscholar.org/CorpusID:3180429   
[5] Harith Al-Safi, Harith S. Ibrahim, and Paul Steenson. 2025. Vega: LLM-Driven Intelligent Chatbot Platform for Internet of Things Control and Development. Sensors (Basel, Switzerland) 25 (2025). https://api. semanticscholar.org/CorpusID:279531727   
[6] Raghav Arora, Shivam Singh, Karthik Swaminathan, Ahana Datta, Snehasis Banerjee, B. Bhowmick, Krishna Murthy Jatavallabhula, Mohan Sridharan, and Madhava Krishna. 2024. Anticipate & Act: Integrating LLMs and Classical Planning for Efficient Task Execution in Household Environments†. 2024 IEEE International Conference on Robotics and Automation (ICRA) (2024), 14038–14045. https: //api.semanticscholar.org/CorpusID:271799905   
[7] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou. 2023. Qwen-VL: A Frontier Large Vision-Language Model with Versatile Abilities. ArXiv abs/2308.12966 (2023). https://api.semanticscholar.org/CorpusID: 263875678   
[8] Stefano Basagni, Federico Ceccarelli, Chiara Petrioli, Nithila Raman, and Abhimanyu Venkatraman Sheshashayee. 2019. Wake-up Radio Ranges: A Performance Study. 2019 IEEE Wireless Communications and Networking Conference (WCNC) (2019), 1–6. https: //api.semanticscholar.org/CorpusID:202548980   
[9] Maciej Besta, Nils Blach, Ale Kubek, Robert Gerstenberger, Lukas Gianinazzi, Joanna Gajda, Tomasz Lehmann, Michal Podstawski, Hubert Niewiadomski, Piotr Nyczyk, and Torsten Hoefler. 2023. Graph of Thoughts: Solving Elaborate Problems with Large Language Models. In AAAI Conference on Artificial Intelligence. https://api.semanticscholar. org/CorpusID:261030303   
[10] Will Brackenbury, Abhimanyu Deora, Jillian Ritchey, Jason Vallee, Weijia He, Guan Wang, Michael L. Littman, and Blase Ur. 2019. How Users Interpret Bugs in Trigger-Action Programming. Proceedings of the 2019 CHI Conference on Human Factors in Computing Systems (2019). https://api.semanticscholar.org/CorpusID:140242523   
[11] Jiarui Cai, Mingze Xu, Wei Li, Yuanjun Xiong, Wei Xia, Zhuowen Tu, and Stefan 0 Soatto. 2022. MeMOT: Multi-Object Tracking with Memory. 2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2022), 8080–8090. https://api.semanticscholar. org/CorpusID:247839756   
[12] Ai Chen, Santosh Kumar, and Ten-Hwang Lai. 2007. Designing localized algorithms for barrier coverage. In ACM/IEEE International Conference on Mobile Computing and Networking. https://api.semanticscholar. org/CorpusID:2864152   
[13] Junzhi Chen, Juhao Liang, and Benyou Wang. 2024. Smurfs: Multi-Agent System using Context-Efficient DFSDT for Tool Planning. In North American Chapter of the Association for Computational Linguistics. https://api.semanticscholar.org/CorpusID:269635774   
[14] Liyi Chen, Panrong Tong, Zhongming Jin, Ying Sun, Jieping Ye, and Huixia Xiong. 2024. Plan-on-Graph: Self-Correcting Adaptive Planning of Large Language Model on Knowledge Graphs. ArXiv abs/2410.23875 (2024). https://api.semanticscholar.org/CorpusID:273707190   
[15] Yanbei Chen, Xiatian Zhu, and Shaogang Gong. 2017. Person Reidentification by Deep Learning Multi-scale Representations. 2017 IEEE International Conference on Computer Vision Workshops (ICCVW) (2017), 2590–2600. https://api.semanticscholar.org/CorpusID:4729614   
[16] Ziyang Chen, Zhangli Zhou, Lin Li, and Zheng Kan. 2024. Active Inference for Reactive Temporal Logic Motion Planning. 2024 IEEE

International Conference on Robotics and Automation (ICRA) (2024), 2520–2526. https://api.semanticscholar.org/CorpusID:271798591   
[17] Ye Cheng, Minghui Xu, Yue Zhang, Kun Li, Ruoxi Wang, and Lian Yang. 2024. AutoIoT: Automated IoT Platform Using Large Language Models. IEEE Internet of Things Journal 12 (2024), 13644–13656. https: //api.semanticscholar.org/CorpusID:274131336   
[18] DeepSeek-AI. 2025. DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning. arXiv:2501.12948 https://arxiv. org/abs/2501.12948   
[19] Fiona M. Donald, Craig H. M. Donald, and Andrew Thatcher. 2015. Work exposure and vigilance decrements in closed circuit television surveillance. Applied ergonomics 47 (2015), 220–8. https: //api.semanticscholar.org/CorpusID:25574518   
[20] J. Feng, Yuwei Du, Tianhui Liu, Siqi Guo, Yuming Lin, and Yong Li. 2024. CityGPT: Empowering Urban Spatial Cognition of Large Language Models. ArXiv abs/2406.13948 (2024). https://api.semanticscholar.org/ CorpusID:270619725   
[21] J. Feng, Shengyuan Wang, Tianhui Liu, Yanxin Xi, and Yong Li. 2025. UrbanLLaVA: A Multi-modal Large Language Model for Urban Intelligence with Spatial Reasoning and Understanding. ArXiv abs/2506.23219 (2025). https://api.semanticscholar.org/CorpusID: 280010693   
[22] Yi Gao, Kaijie Xiao, Fu Li, Weifeng Xu, Jiaming Huang, and Wei Dong. 2024. ChatIoT: Zero-code Generation of Trigger-action Based IoT Programs. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 8 (2024), 1 – 29. https://api.semanticscholar. org/CorpusID:272563565   
[23] Yingqiang Ge, Wenyue Hua, Kai Mei, Jianchao Ji, Juntao Tan, Shuyuan Xu, Zelong Li, and Yongfeng Zhang. 2023. OpenAGI: When LLM Meets Domain Experts. ArXiv abs/2304.04370 (2023). https://api. semanticscholar.org/CorpusID:258049306   
[24] Google DeepMind. 2025. Gemini 2.5 Flash: Model Card. Technical Report. Google. https://storage.googleapis.com/model-cards/documents/ gemini-2.5-flash.pdf   
[25] Google DeepMind. 2025. Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities. arXiv abs/2507.06261 (2025). https: //arxiv.org/abs/2507.06261   
[26] Mordechai (Muki) Haklay and Patrick Weber. 2008. OpenStreetMap: User-Generated Street Maps. IEEE Pervasive Computing 7 (2008), 12–18. https://api.semanticscholar.org/CorpusID:16588111   
[27] Helen M. Hodgetts, François Vachon, Cindy Chamberland, and Sébastien Tremblay. 2017. See No Evil: Cognitive Challenges of Security Surveillance and Monitoring. Journal of applied research in memory and cognition 6 (2017), 230–243. https://api.semanticscholar. org/CorpusID:261257329   
[28] Bin Hu, Xinggang Wang, and Wenyu Liu. 2024. PersonViT: Large-scale Self-supervised Vision Transformer for Person Re-Identification. Mach. Vis. Appl. 36 (2024), 32. https://api.semanticscholar.org/CorpusID: 271854919   
[29] Justin Huang and Maya Cakmak. 2015. Supporting mental model accuracy in trigger-action programming. Proceedings of the 2015 ACM International Joint Conference on Pervasive and Ubiquitous Computing (2015). https://api.semanticscholar.org/CorpusID:207225561   
[30] HUST Vision and Learning Group. 2025. PersonViT. https://github. com/hustvl/PersonViT. GitHub repository.   
[31] Riheng Jia, Jinhao Wu, Xiong Wang, Jianfeng Lu, Feilong Lin, Zhonglong Zheng, and Minglu Li. 2023. Energy Cost Minimization in Wireless Rechargeable Sensor Networks. IEEE/ACM Transactions on Networking 31 (2023), 2345–2360. https://api.semanticscholar.org/ CorpusID:257298122

[32] Jiayu Jiang, Changxing Ding, Wentao Tan, Junhong Wang, Jin Tao, and Xiangmin Xu. 2025. Modeling Thousands of Human Annotators for Generalizable Text-to-Image Person Re-identification. 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2025), 9220–9230. https://api.semanticscholar.org/CorpusID:276961622   
[33] Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. 2024. A Survey on Large Language Models for Code Generation. ArXiv abs/2406.00515 (2024). https://api.semanticscholar.org/CorpusID: 270214176   
[34] Evan King, Haoxiang Yu, Sangsu Lee, and Christine Julien. 2024. Sasha: Creative Goal-Oriented Reasoning in Smart Homes with Large Language Models. Proc. ACM Interact. Mob. Wearable Ubiquitous Technol. 8, 1, Article 12 (2024), 38 pages. doi:10.1145/3643505   
[35] Tomavs Krajnik, Jaime Pulido Fentanes, Marc Hanheide, and Tom Duckett. 2016. Persistent localization and life-long mapping in changing environments using the Frequency Map Enhancement. 2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS) (2016), 4558–4563. https://api.semanticscholar.org/CorpusID: 4969989   
[36] Santosh Kumar, Ten-Hwang Lai, and Anish Arora. 2005. Barrier coverage with wireless sensors. Wireless Networks 13 (2005), 817–834. https://api.semanticscholar.org/CorpusID:565989   
[37] Carolin Lawrence and Stefan Riezler. 2016. NLmaps: A Natural Language Interface to Query OpenStreetMap. In COLING 2016 System Demonstrations.   
[38] Patrick Lewis, Ethan Perez, Aleksandara Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Kuttler, Mike Lewis, Wen tau Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. 2020. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. ArXiv abs/2005.11401 (2020). https://api.semanticscholar.org/CorpusID: 218869575   
[39] Yunhao Li, Xiaoqiong Liu, Luke Liu, Heng Fan, and Libo Zhang. 2024. LaMOT: Language-Guided Multi-Object Tracking. ArXiv abs/2406.08324 (2024). https://api.semanticscholar.org/CorpusID: 270391880   
[40] Jie Lin, Wei Yu, Nan Zhang, Xinyu Yang, Hanlin Zhang, and Wei Zhao. 2017. A Survey on Internet of Things: Architecture, Enabling Technologies, Security and Privacy, and Applications. IEEE Internet of Things Journal 4 (2017), 1125–1142. https://api.semanticscholar.org/ CorpusID:31245252   
[41] Kaiwei Liu, Bufang Yang, Lilin Xu, Yunqi Guo, Guoliang Xing, Xian Shuai, Xiaozhe Ren, Xin Jiang, and Zhenyu Yan. 2025. TaskSense: A Translation-like Approach for Tasking Heterogeneous Sensor Systems with LLMs. Proceedings of the 23rd ACM Conference on Embedded Networked Sensor Systems (2025). https://api.semanticscholar.org/ CorpusID:278326090   
[42] Zhaoyang Liu, Zeqiang Lai, Zhangwei Gao, Erfei Cui, Xizhou Zhu, Lewei Lu, Qifeng Chen, Yu Qiao, Jifeng Dai, and Wenhai Wang. 2023. ControlLLM: Augment Language Models with Tools by Searching on Graphs. ArXiv abs/2310.17796 (2023). https://api.semanticscholar.org/ CorpusID:264555643   
[43] Huan Ma, Changqing Zhang, Yatao Bian, Lemao Liu, Zhirui Zhang, Peilin Zhao, Shu Zhang, H. Fu, Qinghua Hu, and Bing Wu. 2023. Fairness-guided Few-shot Prompting for Large Language Models. ArXiv abs/2303.13217 (2023). https://api.semanticscholar.org/ CorpusID:257687840   
[44] Tinashe Magara and Yousheng Zhou. 2024. Internet of Things (IoT) of Smart Homes: Privacy and Security. J. Electr. Comput. Eng. 2024 (2024), 1–17. https://api.semanticscholar.org/CorpusID:269065642   
[45] Alexandre Marois, Daniel Lafond, Alexandre Williot, François Vachon, and Sébastien Tremblay. 2020. Real-Time Gaze-Aware Cognitive Support System for Security Surveillance. Proceedings of the Human

Factors and Ergonomics Society Annual Meeting 64 (2020), 1145 – 1149. https://api.semanticscholar.org/CorpusID:231876226   
[46] Francesca Meneghello, Matteo Calore, Daniel Zucchetto, Michele Polese, and Andrea Zanella. 2019. IoT: Internet of Threats? A Survey of Practical Security Vulnerabilities in Real IoT Devices. IEEE Internet of Things Journal 6 (2019), 8182–8201. https://api.semanticscholar. org/CorpusID:201889124   
[47] Hamid Menouar, Ismail Guvenc, Kemal Akkaya, Arif Selcuk Uluagac, Abdullah Kadri, and Adem Tuncer. 2017. UAV-Enabled Intelligent Transportation Systems for the Smart City: Applications and Challenges. IEEE Communications Magazine 55 (2017), 22–28. https://api.semanticscholar.org/CorpusID:38330180   
[48] Meta AI. 2023. Llama 2: Open Foundation and Fine-Tuned Chat Models. arXiv abs/2307.09288 (2023). https://arxiv.org/abs/2307.09288   
[49] Phillip L. Morgan, Emily Collins, Tasos Spiliotopoulos, David J. Greeno, and Dylan M. Jones. 2022. Reducing risk to security and privacy in the selection of trigger-action rules: Implicit vs. explicit priming for domestic smart devices. Int. J. Hum. Comput. Stud. 168 (2022), 102902. https://api.semanticscholar.org/CorpusID:251341078   
[50] Naser Hossein Motlagh. 2021. How Low Can You Go? Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 5 (2021), 1 – 22. https://api.semanticscholar.org/CorpusID:248245897   
[51] OpenAI. 2023. GPT-4 Technical Report. arXiv:2303.08774 [cs.CL] doi:10.48550/arXiv.2303.08774   
[52] OpenAI. 2025. o3 and o4-mini System Card. System Card. OpenAI. https://cdn.openai.com/pdf/2221c875-02dc-4789-800be7758f3722c1/o3-and-o4-mini-system-card.pdf   
[53] Serge Pelletier, Joel Suss, François Vachon, and Sébastien Tremblay. 2015. Atypical Visual Display for Monitoring Multiple CCTV Feeds. Proceedings of the 33rd Annual ACM Conference Extended Abstracts on Human Factors in Computing Systems (2015). https: //api.semanticscholar.org/CorpusID:304177   
[54] Kai Peng, Hualong Huang, Muhammad Bilal, and Xiaolong Xu. 2023. Distributed Incentives for Intelligent Offloading and Resource Allocation in Digital Twin Driven Smart Industry. IEEE Transactions on Industrial Informatics 19 (2023), 3133–3143. https://api.semanticscholar. org/CorpusID:249911526   
[55] Yujia Qin, Shi Liang, Yining Ye, Kunlun Zhu, Lan Yan, Ya-Ting Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, Sihan Zhao, Runchu Tian, Ruobing Xie, Jie Zhou, Marc H. Gerstein, Dahai Li, Zhiyuan Liu, and Maosong Sun. 2023. ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs. ArXiv abs/2307.16789 (2023). https://api.semanticscholar.org/CorpusID:260334759   
[56] Changle Qu, Sunhao Dai, Xiaochi Wei, Hengyi Cai, Shuaiqiang Wang, Dawei Yin, Jun Xu, and Jirong Wen. 2024. Tool Learning with Large Language Models: A Survey. ArXiv abs/2405.17935 (2024). https: //api.semanticscholar.org/CorpusID:270067624   
[57] Brian Reily, Terran Mott, and Hao Zhang. 2020. Adaptation to Team Composition Changes for Heterogeneous Multi-Robot Sensor Coverage. 2021 IEEE International Conference on Robotics and Automation (ICRA) (2020), 9051–9057. https://api.semanticscholar.org/CorpusID: 229297612   
[58] Zhiwei Ren, Junbo Li, Minjia Zhang, Di Wang, Xiaoran Fan, and Longfei Shangguan. 2025. Toward Sensor-In-the-Loop LLM Agent: Benchmarks and Implications. Proceedings of the 23rd ACM Conference on Embedded Networked Sensor Systems (2025). https://api. semanticscholar.org/CorpusID:278326126   
[59] Stefano De Sabbata, Stefano Mizzaro, and Kevin Roitero. 2025. Geospatial Mechanistic Interpretability of Large Language Models. ArXiv abs/2505.03368 (2025). https://api.semanticscholar.org/CorpusID: 278339325

[60] Christoph Schöller, Vincent Aravantinos, Florian Samuel Lay, and Alois Knoll. 2019. The Simpler the Better: Constant Velocity for Pedestrian Motion Prediction. ArXiv abs/1903.07933 (2019). https: //api.semanticscholar.org/CorpusID:83458829   
[61] Leming Shen, Qian Yang, Xinyu Huang, Zijing Ma, and Yuanqing Zheng. 2025. GPIoT: Tailoring Small Language Models for IoT Program Synthesis and Development. Proceedings of the 23rd ACM Conference on Embedded Networked Sensor Systems (2025). https: //api.semanticscholar.org/CorpusID:276742179   
[62] Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, Weiming Lu, and Yue Ting Zhuang. 2023. HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face. ArXiv abs/2303.17580 (2023). https://api.semanticscholar.org/CorpusID:257833781   
[63] Kyujin Shim, Sungjoon Yoon, Kangwook Ko, and Changick Kim. 2021. Multi-Target Multi-Camera Vehicle Tracking for City-Scale Traffic Management. 2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW) (2021), 4188–4195. https://api.semanticscholar.org/CorpusID:235632675   
[64] Noah Shinn, Federico Cassano, Beck Labash, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2023. Reflexion: language agents with verbal reinforcement learning. In Neural Information Processing Systems. https://api.semanticscholar.org/CorpusID:258833055   
[65] Wentao Tan, Changxing Ding, Jiayu Jiang, Fei Wang, Yibing Zhan, and Dapeng Tao. 2024. Harnessing the Power of MLLMs for Transferable Text-to-Image Person ReID. 2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2024), 17127–17137. https: //api.semanticscholar.org/CorpusID:269626531   
[66] Zheng Tang, Milind R. Naphade, Ming-Yu Liu, Xiaodong Yang, Stan Birchfield, Shuo Wang, Ratnesh Kumar, D. Anastasiu, and Jenq-Neng Hwang. 2019. CityFlow: A City-Scale Benchmark for Multi-Target Multi-Camera Vehicle Tracking and Re-Identification. 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2019), 8789–8798. https://api.semanticscholar.org/CorpusID:85459559   
[67] Ultralytics. 2025. Ultralytics YOLOv8. https://github.com/ultralytics/ ultralytics. GitHub repository.   
[68] Blase Ur, Melwyn Pak Yong Ho, Stephen Brawner, Jiyun Lee, Sarah Mennicken, Noah Picard, Diane Schulze, and Michael L. Littman. 2016. Trigger-Action Programming in the Wild: An Analysis of 200,000 IFTTT Recipes. Proceedings of the 2016 CHI Conference on Human Factors in Computing Systems (2016). https://api.semanticscholar.org/ CorpusID:10883440   
[69] Hanqing Wang, Wenguan Wang, Wei Liang, Caiming Xiong, and Jianbing Shen. 2021. Structured Scene Memory for Vision-Language Navigation. 2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2021), 8451–8460. https://api.semanticscholar. org/CorpusID:232135021   
[70] Jiang Wang, Yuanzheng He, Daobilige Su, Katsutoshi Itoyama, Kazuhiro Nakadai, Junfeng Wu, Shoudong Huang, Youfu Li, and He Kong. 2024. SLAM-Based Joint Calibration of Multiple Asynchronous Microphone Arrays and Sound Source Localization. IEEE Transactions on Robotics 40 (2024), 4024–4044. https://api.semanticscholar.org/ CorpusID:270123565   
[71] Dongming Wu, Wencheng Han, Tiancai Wang, Xingping Dong, Xiangyu Zhang, and Jianbing Shen. 2023. Referring Multi-Object Tracking. 2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (2023), 14633–14642. https://api.semanticscholar.org/ CorpusID:257365320   
[72] Duo Wu, Jinghe Wang, Yuan Meng, Yanning Zhang, Le Sun, and Zhi Wang. 2024. CATP-LLM: Empowering Large Language Models for Cost-Aware Tool Planning. ArXiv abs/2411.16313 (2024). https://api. semanticscholar.org/CorpusID:274234379

[73] Minghu Wu, Yeqiang Qian, Chunxiang Wang, and Ming Yang. 2021. A Multi-Camera Vehicle Tracking System based on City-Scale Vehicle Re-ID and Spatial-Temporal Information. 2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW) (2021), 4072–4081. https://api.semanticscholar.org/CorpusID:235702604   
[74] Sixu Wu, Haipeng Dai, Linfeng Liu, Lijie Xu, Fu Xiao, and Jia Xu. 2024. Cooperative Scheduling for Directional Wireless Charging With Spatial Occupation. IEEE Transactions on Mobile Computing 23 (2024), 286–301. https://api.semanticscholar.org/CorpusID:253343259   
[75] Huatao Xu, Liying Han, Qirui Yang, Mo Li, and Mani B. Srivastava. 2023. Penetrative AI: Making LLMs Comprehend the Physical World. Proceedings of the 25th International Workshop on Mobile Computing Systems and Applications (2023). https://api.semanticscholar.org/ CorpusID:264145826   
[76] Antoine Yang, Antoine Miech, Josef Sivic, Ivan Laptev, and Cordelia Schmid. 2022. Learning to Answer Visual Questions From Web Videos. IEEE Transactions on Pattern Analysis and Machine Intelligence 47 (2022), 3202–3218. https://api.semanticscholar.org/CorpusID:248570072   
[77] Fan Yang, Dung-Han Lee, John Keller, and Sebastian A. Scherer. 2021. Graph-based Topological Exploration Planning in Large-scale 3D Environments. 2021 IEEE International Conference on Robotics and Automation (ICRA) (2021), 12730–12736. https://api.semanticscholar.org/ CorpusID:232428138   
[78] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, and Karthik Narasimhan. 2023. Tree of Thoughts: Deliberate Problem Solving with Large Language Models. ArXiv abs/2305.10601 (2023). https://api.semanticscholar.org/CorpusID:258762525   
[79] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. 2022. ReAct: Synergizing Reasoning and Acting in Language Models. ArXiv abs/2210.03629 (2022). https: //api.semanticscholar.org/CorpusID:252762395   
[80] Xiaofan Yu, Lanxiang Hu, Benjamin Z. Reichman, Dylan Chu, Rushil Chandrupatla, Xiyuan Zhang, Larry Heck, and Tajana Rosing. 2025. SensorChat: Answering Qualitative and Quantitative Questions during Long-Term Multimodal Sensor Interactions. ArXiv abs/2502.02883 (2025). https://api.semanticscholar.org/CorpusID:276116215   
[81] Zhou Yu, D. Xu, Jun Yu, Ting Yu, Zhou Zhao, Yueting Zhuang, and Dacheng Tao. 2019. ActivityNet-QA: A Dataset for Understanding Complex Web Videos via Question Answering. ArXiv abs/1906.02467 (2019). https://api.semanticscholar.org/CorpusID:69645185   
[82] Tony Zhao, Eric Wallace, Shi Feng, Dan Klein, and Sameer Singh. 2021. Calibrate Before Use: Improving Few-Shot Performance of Language Models. In International Conference on Machine Learning. https://api. semanticscholar.org/CorpusID:231979430   
[83] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Haotong Zhang, Joseph E. Gonzalez, and Ion Stoica. 2023. Judging LLMas-a-judge with MT-Bench and Chatbot Arena. ArXiv abs/2306.05685 (2023). https://api.semanticscholar.org/CorpusID:259129398   
[84] Kaiyang Zhou, Yongxin Yang, Andrea Cavallaro, and Tao Xiang. 2019. Learning Generalisable Omni-Scale Representations for Person Re-Identification. IEEE Transactions on Pattern Analysis and Machine Intelligence 44 (2019), 5056–5069. https://api.semanticscholar.org/ CorpusID:204575830   
[85] Kaiyang Zhou, Yongxin Yang, Andrea Cavallaro, and Tao Xiang. 2019. Omni-Scale Feature Learning for Person Re-Identification. 2019 IEEE/CVF International Conference on Computer Vision (ICCV) (2019), 3701–3711. https://api.semanticscholar.org/CorpusID:145050804   
[86] Xiaojian Zhu, Mengchu Zhou, and Abdullah M. Abusorrah. 2022. Optimizing Node Deployment in Rechargeable Camera Sensor Networks for Full-View Coverage. IEEE Internet of Things Journal 9 (2022), 11396– 11407. https://api.semanticscholar.org/CorpusID:243947717