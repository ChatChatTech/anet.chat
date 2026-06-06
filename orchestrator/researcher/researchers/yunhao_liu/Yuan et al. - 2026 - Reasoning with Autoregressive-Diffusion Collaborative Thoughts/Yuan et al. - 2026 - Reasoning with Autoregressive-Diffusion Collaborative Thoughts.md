# Reasoning with Autoregressive-Diffusion Collaborative Thoughts

Mu Yuan1∗, Liekang Zeng1∗, Guoliang Xing1, Lan Zhang2, Yunhao Liu3

1The Chinese University of Hong Kong

2University of Science and Technology of China

3Tsinghua University

muyuan@cuhk.edu.hk, lkzeng@cuhk.edu.hk, glxing@cuhk.edu.hk

zhanglan@ustc.edu.cn, yunhao@tsinghua.edu.cn

# Abstract

Autoregressive and diffusion models represent two complementary generative paradigms. Autoregressive models excel at sequential planning and constraint composition, yet struggle with tasks that require explicit spatial or physical grounding. Diffusion models, in contrast, capture rich spatial structure through highdimensional generation, but lack the stepwise logical control needed to satisfy complex, multi-stage constraints or to reliably identify and correct errors.

We introduce Collaborative Thoughts, a unified collaborative framework that enables autoregressive and diffusion models to reason and generate jointly through a closed-loop interaction. In Collaborative Thoughts, autoregressive models perform structured planning and constraint management, diffusion models instantiate these constraints as intermediate visual thoughts, and a vision-based critic module evaluates whether the visual thoughts satisfy the intended structural and physical requirements. This feedback is then used to iteratively refine subsequent planning and generation steps, mitigating error propagation across modalities. Importantly, Collaborative Thoughts uses the same collaborative loop regardless of whether the task is autoregressive question answering or diffusion-based visual generation. Through representative examples, we illustrate how Collaborative Thoughts can improve the reliability of spatial reasoning and the controllability of generation.

# 1 Introduction

Reasoning constitutes the fundamental capability of general-purpose artificial intelligence, enabling systems to decompose complex problems, formulate structured plans, and execute multi-step solutions. Beyond direct answer (Figure 1a), the Chain-of-Thought (CoT) paradigm [16] has significantly advanced this frontier, empowering Large Language Models (LLMs) to tackle intricate tasks through intermediate verbal reasoning (Figure 1b). While effective for semantic deduction, this reliance on symbolic abstraction creates a "blind spot" for tasks requiring explicit spatial awareness or physical common sense: LLMs often struggle to verify geometric structures or simulate physical interactions, leading to hallucinations that are linguistically coherent but physically implausible [2, 14, 17].

To bridge this disconnect, emerging research has pivoted toward visualizing text thoughts [7, 17], a paradigm that seeks to externalize reasoning through visual formats (Figure 1c). These approaches augment LLMs with the capacity to generate schematic diagrams or intermediate imagery to serve as cognitive scaffolding. However, in these approaches, generated visual contents are typically treated as immutable ground truth rather than provisional hypotheses. Without an explicit feedback mechanism, errors introduced during visual generation cannot be effectively detected or corrected, leading to irreversible error propagation. Moreover, most prior methods focus on annotating or interpreting static visual inputs, leaving the potential of an iterative, self-correcting interaction between reasoning and generation largely unexplored.

![](images/4f14ab1b098f7821acf80fae9ff4533eae1b9cac05151438cf4de93313d4f019.jpg)



(a) Direct Answer

![](images/4855ba3ec769e0b5c4156769ae2548efa67708602d0acd06884cde35ac3436c0.jpg)



(b) Chain of Thoughts

![](images/8658f3cbdddbcf690565bc30935c435813ad8c730371ad0bb9f3f964703da702.jpg)



(c) Visualiza on of Thoughts

![](images/fc30363141d475985c1c340a7446b7bc83e97e59920337238eab34c0a8be279b.jpg)



(d) Collabora ve Thoughts (Ours)   
Figure 1: Traditional chain-of-thought (CoT) [16] ponders queries via only text, and Visualization of Thoughts (VoT) [17, 7] relies on visual input to initiate the visualization of thinking traces. Collaborative Thoughts orchestrates autoregressive and diffusion models to collaboratively think via multimodal reasoning traces.

To address these limitations, we explore to synergizing two complementary yet fundamentally different generative paradigms: autoregressive models and diffusion models. Autoregressive (AR) models, exemplified by LLMs, excel at symbolic composition and sequential constraint management but struggle to faithfully represent high-dimensional geometric structures (Figure 2, AR-Only). Diffusion models, in contrast, define the state-of-the-art in high-dimensional visual synthesis and act as powerful generators of spatially coherent visual content [3, 19]. Combining the both worlds, we propose Collaborative Thoughts, a closed-loop framework that enables sustained collaboration between autoregressive and diffusion paradigms through iterative planning, generation, and refinement. This perspective is inspired by Dual Coding Theory [11], which posits that human cognition integrates sequential symbolic reasoning with spatial mental imagery. When solving complex geometric or physical problems, humans repeatedly construct mental images, evaluate them against physical constraints, and revise their reasoning accordingly. Motivated by this cognitive process, rather than viewing generation as a one-shot process, our framework treats intermediate outputs as hypotheses that can be inspected and refined.

Concretely, as shown in Figure 1d, autoregressive models are responsible for structured planning and constraint composition, decomposing tasks into a sequence of visualizable requirements. Diffusion models instantiate these requirements as intermediate visual blueprints that explicitly capture spatial structure. A critic module then evaluates the generated visual thoughts against the intended constraints and provides feedback that guides subsequent planning and generation steps. This iterative Simulate-Critic-Refine cycle mitigates error propagation from modality misalignment and enables continuous correction across reasoning and generation.

Importantly, Collaborative Thoughts is agnostic to the task’s final output modality. For tasks that require symbolic or textual answers, diffusion models primarily serve to generate intermediate visual references that ground autoregressive reasoning. For tasks that require visual generation, autoregressive models assist diffusion by providing stepwise planning and refinement, while the tidiffusion model produces the final output. In both cases, the same closed-loop interaction governs simulate, critic, and refinement, offering a unified treatment of reasoning and generation across paradigms.

tiAs a proof of concept, in this work, we focus on representative examples that illustrate the capabilities and opportunities enabled by this collaborative framework. These examples demonstrate how autoregressive-diffusion collaboration can improve the reliability of spatial reasoning and the controllability of generative processes, pointing toward a broader research direction on collaborative reasoning across generative paradigms.

# 2 Related Work

Autoregressive-Guided Visual Planning and Layout Generation. A line of work integrates autoregressive models into text-to-image generation pipelines to alleviate the limitations of fixed text encoders by introducing intermediate planning or layout representations. Representative approaches such as LLM-grounded Diffusion [8] and LayoutLLM [13] decompose user prompts into explicit spatial layouts or bounding boxes that condition subsequent diffusion generation. RPG [18] further extends this idea by using multimodal autoregressive models to perform multi-step planning for regionlevel generation, enabling better handling of compositional attributes. DiffusionGPT [12] explores routing prompts through structured reasoning paths before generation. Despite their effectiveness, these approaches are predominantly sequential: planning is performed once, and the generated visual output is treated as a fixed realization of that plan. In contrast, our framework emphasizes interaction, where intermediate visual outputs are explicitly checked and used to refine subsequent planning steps.

Iterative Visual Refinement with Feedback. To mitigate errors in generative models, several studies introduce iterative refinement mechanisms based on visual feedback. Self-correcting diffusion pipelines use autoregressive detectors to compare generated images against textual requirements and issue corrective signals for subsequent generations. More general frameworks, such as Iterative Prompt Refinement [6], leverage vision-language models to adjust prompts based on discrepancies observed in generated visuals. Related work on visual reasoning, including Visual Sketchpad and Visual Chain-of-Thought [5], shows that intermediate visual artifacts can support geometric and logical inference. While effective at reducing generation errors, these methods typically treat visual outputs as auxiliary signals for validation. Our approach differs in that visual generation is integrated as a central intermediate state in the reasoning process, enabling planning decisions to be directly informed by verified visual structure rather than post hoc correction alone.

Simulation-Based Reasoning and Physical Grounding. Simulation has also been explored as a means to ground reasoning in physical dynamics. The Mind’s Eye framework [9] employs external physics engines, such as MuJoCo [15], to simulate outcomes for physical reasoning tasks. Recent advances in video generation have inspired approaches like PhysGen [10] and InterDyn [1], which use diffusion-based video models to predict object dynamics and interactions. In robotics, methods such as CoT-VLA [21] and Vidarc [4] leverage imagined future visual states to guide control policies. However, these approaches often rely on a single simulation modality and lack mechanisms for structured, stepwise verification across reasoning and generation. Our work complements this line of research by focusing on collaborative interaction between autoregressive planning and diffusion-based visual generation, enabling iterative verification and refinement without assuming access to precise physical simulators.

# 3 Method

Collaborative Thoughts is a framework that synergizes autoregressive reasoning with diffusionbased visual simulation, mainly comprising three main components (Figure 1d). Unlike rigorous open-loop generation, our approach treats visual synthesis as an iterative optimization process guided by semantic constraints.

# 3.1 Problem Formulation

Let Q be a natural language query requiring spatial or physical reasoning, and A be the target answer. We model the reasoning process as a sequential decision-making problem over T steps. At each step t, the system maintains a reasoning state $S _ { t } = \{ P _ { t } , R _ { t } , F _ { t } \}$ , consisting of a textual thought $P _ { t }$ (i.e., for visual prompt), a generated visual thought $\bar { R _ { t } }$ (e.g., image), and textual feedback $F _ { t }$ . Assuming the knowledge of the physical world aligns with the distribution $p _ { \mathrm { w o r l d } }$ , our goal is to maximize the joint probability of the correct answer $\mathcal { A }$ with respect to $p _ { \mathrm { w o r l d } }$ given the query and the evolved visual thoughts:

$$
\mathcal {A} ^ {*} = \arg \max _ {\mathcal {A}} \mathcal {M} (\mathcal {A} \mid \mathcal {Q}, R ^ {*}) \sim p _ {\text { world }}, \tag {1}
$$

where $R ^ { * }$ is the optimal visual simulation selected from the iterative trajectory. The framework comprises three coupled agents: the Planner (autoregressive model), the Simulator (diffusion model), and the Critic (autoregressive model).

# 3.2 The Planner: Semantic-to-Visual Translation

The Planner, denoted as $\mathcal { M } _ { p l a n } .$ is an autoregressive LLM responsible for reasoning decomposition and prompt engineering. In the initial step $( t = 0 )$ , the Planner analyzes Q to extract implicit spatial constraints $( \mathrm { e . g . }$ , "object A must support object $\mathbf { B ^ { \prime \prime } } )$ and generates an initial scene description prompt $P _ { 0 }$ . In subsequent steps $( t > 0 )$ , the Planner acts as a refiner. It receives the feedback $F _ { t - 1 }$ from the Critic, which details the discrepancies between the previous simulation $I _ { t - 1 }$ and the physical constraints. The Planner then updates the prompt to rectify these errors:

$$
P _ {t} = \mathcal {M} _ {\text { plan }} (\mathcal {Q}, F _ {t - 1}, H _ {t - 1}), \tag {2}
$$

where $H _ { t - 1 }$ represents the conversation history, enabling the model to perform in-context learning from past failures.

# 3.3 The Simulator: Physical Instantiation

The Simulator $\mathcal { M } _ { \mathrm { s i m } }$ serves as the external "world model". It maps the semantic instructions $P _ { t }$ into a pixel-space representation $R _ { t }$ . To mitigate the stochastic instability of diffusion models, layout-guided generation strategies (e.g., ControlNet [20]) may be employed. This ensures that the global spatial structure adheres to the Planner’s intent while allowing the diffusion model to fill in fine-grained physical details (texture, lighting, occlusion):

$$
R _ {t} = \mathcal {M} _ {\text { sim }} (P _ {t} | \mathcal {C}) \sim p _ {\text { world }}. \tag {3}
$$

Here, C denotes optional structural constraints (such as bounding boxes or depth maps) generated by the Planner to enforce geometric stability. The generation of the diffusion model $\mathcal { M } _ { \mathrm { s i m } }$ conveys its physical knowledge to $\bar { \boldsymbol { R } } _ { t }$ by approximating the distribution of the real world $p _ { \mathrm { w o r l d } } .$

# 3.4 The Critic: Visual-Logic Alignment

The Critic, $\mathcal { M } _ { \mathrm { c r i t i c } } .$ , is an autoregressive model (e.g., VLM) tasked with supervision. It closes the reasoning loop by perceiving the generated visual thought $R _ { t }$ and comparing it against the original query requirements. As shown in Equation (4), the Critic performs two functions: 1) Verification Score (vt): A scalar score $v _ { t } \in [ 0 , 1 ]$ indicating the degree of constraint satisfaction (e.g., checking for object hallucinations, floating objects, or incorrect relative positions); 2) Corrective Feedback $( F _ { t } ) \colon$ If $v _ { t }$ falls below a confidence threshold τ , the Critic generates natural language feedback describing the specific violation $( \mathrm { e . g . }$ , "The red cube is floating; it must rest on the table surface").

$$
v _ {t}, F _ {t} = \mathcal {M} _ {\text { critic }} (R _ {t}, \mathcal {Q}). \tag {4}
$$

# 3.5 Termination and Inference

The iterative process terminates when one of the following conditions is met: 1) Convergence: The verification score exceeds the threshold $( v _ { t } > \tau ) ; 2 )$ ) Budget Exhaustion: The iteration count reaches the maximum limit $( t \geq T _ { m a x } ) ; 3 )$ Deadlock: Semantic oscillation is detected in consecutive prompts.

Upon termination, the critic synthesizes the final answer A based on the validated visual thought $R ^ { * }$ (or the highest-scoring reference $R _ { \mathrm { b e s t } }$ in the trajectory), effectively grounding the verbal reasoning in verified visual simulation.

# 4 Demonstrations

Figure 2 qualitatively demonstrates the superiority of the proposed AR-Diffusion collaborative thinking framework over uni-architecture approaches in handling complex spatial reasoning tasks. The demonstration involves a multi-step geometric problem requiring the sequential cutting of a square and the subsequent identification of the resulting sub-regions. As illustrated in the $\ " { \mathrm { A R - O n l y } } "$ panel, purely text-based autoregressive models struggle with spatial abstraction; despite receiving clear instructions, they hallucinate incorrect geometric compositions (e.g., miscounting triangles and quadrilaterals) due to a lack of visual grounding. Conversely, the "Diffusion-Only" approach (right panel) attempts to generate the visual solution in a single pass. However, it fails to adhere to the strict structural logic required, resulting in imprecise cuts and geometric distortions that render the output unusable for accurate reasoning. In contrast, the central panel highlights the efficacy of our collaborative framework. By leveraging the AR model as a high-level planner and the diffusion model as an external visualizer, the system decomposes the query into a discrete chain of visual steps—ranging from the initial vertical cut to the final coloring of sub-regions. This step-by-step visual refinement process creates a precise "blueprint," effectively preventing error propagation. Consequently, the system correctly identifies the complex final configuration (3 triangles, 1 rectangle, 2 quadrilaterals, and 1 pentagon), validating the necessity of interleaving reasoning and generation for spatial tasks.

![](images/a8f034e4c56764c1872d75344cc16edd207732cfeb058a09b6027faa042ea176.jpg)



Figure 2: While text-based reasoning (AR-Only) struggles with spatial abstraction and direct generation (Diffusion-Only) lacks structural logic, our framework leverages the complementary strengths of both. The autoregressive (AR) model acts as a planner to break down the diffusion process into four discrete steps. This step-by-step visual verification prevents the error propagation seen in the baselines, allowing for accurate identification of the final geometric shapes.

Complementing the topological decomposition task in Figure 2, Figure 3 further illustrates the versatility of the Collaborative Thoughts framework in the context of Euclidean geometry problem solving. This demonstration specifically highlights the framework’s ability to bridge the gap between accurate visual generation and efficient logical inference. As depicted in the $\ " \mathrm { A R - O n l y " }$ panel (left), while advanced Large Language Models (e.g., Gemini-1.5-Pro, DeepSeek-R1) can deductively solve for the target angle $\angle \bar { A } G \bar { B }$ , the process is computationally expensive. Relying solely on textual Chain-of-Thought requires parsing complex geometric relationships without visual grounding, resulting in excessive token consumption (up to 14,035 tokens) to reach the correct conclusion. Conversely, the "Diffusion-Only" baseline (right) attempts to generate the diagram via direct instruction but suffers from "geometric hallucination," failing to preserve essential constraints such as perpendicularity $( D E \bot B C )$ or precise intersections, rendering the image useless for reasoning. The central panel demonstrates how the proposed collaborative framework resolves these limitations. By utilizing the autoregressive model to plan a sequential construction, the system guides the diffusion model to generate a geometrically rigorous intermediate diagram. This highfidelity visualization allows the reasoning model to bypass lengthy textual derivations, grounding its answer directly in the visual data. The result is a dramatic optimization in inference efficiency: the reasoning cost is reduced by orders of magnitude (e.g., from 14,035 tokens to a single token) while maintaining 100% accuracy. Together, Figures 1 and 2 validate that Collaborative Thoughts not only prevents error propagation in complex spatial tasks but also provides a scalable, low-latency paradigm for geometric reasoning.

# 5 Discussion

Why does Collaborative Thoughts work? The efficacy of our framework partially stems from leveraging the diffusion model as a data-driven implicit world model that complements the abstract logic of LLMs. Having internalized vast phenomenological knowledge (e.g., occlusion, gravity, material properties) from large-scale pre-training, the diffusion model acts as a ’Physical Consistency Filter’, forcing the planner’s symbolic hypotheses to confront the statistical realities of pixel space. By grounding textual reasoning in these robust visual priors, the system effectively bridges the gap between semantic coherence and physical viability, rejecting logically sound but physically implausible solutions.

![](images/96b91b1750a6a5651c6e119b2d653553e967e24a3bbfc8afdd1b045490ea4c40.jpg)



Figure 3: Illustration of reasoning paradigms for geometric problem solving. The proposed AR-Diffusion Collaborative Thoughts (center) creates intermediate visual blueprints to bridge the gap between text and vision. This approach corrects the geometric hallucinations observed in Diffusion-Only methods (right) and significantly improves inference efficiency compared to the AR-Only textual chain-of-thought (left), reducing computational costs by orders of magnitude.

The "Soft Simulator" Paradigm. Collaborative Thoughts empirically grounds Dual Coding Theory[11] in computational systems by mutually coupling autoregressive LLMs and diffusion models in an iterative loop. Unlike rigid physics engines (e.g., MuJoCo [15]) that require precise parameterization, our framework establishes diffusion models as "soft simulators", which also suffer from the "sim-to-real" gap. This trades absolute numerical precision for semantic universality, enabling physical reasoning in open-domain scenarios (e.g., "stacking heterogeneous household objects") where formal modeling is intractable.

Simulator and Critic Bottlenecks. The iterative nature of the "Simulate-Critic-Refine" cycle introduces significant computational overhead from the diffusion-based visual generation. Also, the reasoning upper bound is constrained by the diffusion model’s physical understanding and generation capabilities, as well as the critic’s verification correctness.

# 6 Conclusion

We presented Collaborative Thoughts, a framework that bridges the chasm between autoregressive semantic planning and diffusion-based visual simulation. By treating visual simulation as an iterative reasoning step rather than a final output, we demonstrated that a closed "Generation-Reasoning" loop effectively grounds abstract logic in pixel-level physical priors, mitigating the spatial hallucinations common in pure LLMs. Our findings substantiate a broader paradigm shift: robust spatial intelligence arises not from a single omnipotent model, but from a synergistic cognitive architecture where the logical rigor of CoT and the phenomenological intuition of diffusion-based simulation continuously critique and refine one another.

For future work, we explore to address the inference overhead of the iterative cycle to accelerate the feedback loop. Furthermore, we aim to extend the "simulator" from 2D static visual content to 3D assets and video dynamics, paving the way for embodied agents that can mentally rehearse physical actions before real-world execution.

# References

[1] R. Akkerman, H. Feng, M. J. Black, D. Tzionas, and V. F. Abrevaya. Interdyn: Controllable interactive dynamics with video diffusion models. In Proceedings of the Computer Vision and Pattern Recognition Conference, pages 12467–12479, 2025.   
[2] B. Chen, Z. Xu, S. Kirmani, B. Ichter, D. Sadigh, L. Guibas, and F. Xia. Spatialvlm: Endowing visionlanguage models with spatial reasoning capabilities. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 14455–14465, 2024.   
[3] F.-A. Croitoru, V. Hondru, R. T. Ionescu, and M. Shah. Diffusion models in vision: A survey. IEEE transactions on pattern analysis and machine intelligence, 45(9):10850–10869, 2023.   
[4] Y. Feng, C. Xiang, X. Mao, H. Tan, Z. Zhang, S. Huang, K. Zheng, H. Liu, H. Su, and J. Zhu. Vidarc: Embodied video diffusion model for closed-loop control. arXiv preprint arXiv:2512.17661, 2025.   
[5] Y. Hu, W. Shi, X. Fu, D. Roth, M. Ostendorf, L. Zettlemoyer, N. A. Smith, and R. Krishna. Visual sketchpad: Sketching as a visual chain of thought for multimodal language models. In Advances in Neural Information Processing Systems (NeurIPS), 2024.   
[6] J. Jeon, J. Oh, H. Lee, and B.-J. Lee. Iterative prompt refinement for safer text-to-image generation. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing (EMNLP), 2025.   
[7] C. Li, W. Wu, H. Zhang, Y. Xia, S. Mao, L. Dong, I. Vulic, and F. Wei. Imagine while reasoning in space: ´ Multimodal visualization-of-thought. In Forty-second International Conference on Machine Learning.   
[8] L. Lian, B. Li, A. Yala, and T. Darrell. Llm-grounded diffusion: Enhancing prompt understanding of text-to-image diffusion models with large language models. Transactions on Machine Learning Research, 2024.   
[9] R. Liu, J. Wei, S. S. Gu, T.-Y. Wu, S. Vosoughi, C. Cui, D. Zhou, and A. M. Dai. Mind’s eye: Grounded language model reasoning through simulation. In International Conference on Learning Representations (ICLR), 2023.   
[10] S. Liu, Z. Zhang, J. Zhang, D. Xu, and J.-Y. Zhu. Physgen: Rigid-body physics-grounded image-to-video generation. In European Conference on Computer Vision (ECCV), 2024.   
[11] A. Paivio. Dual coding theory: Retrospect and current status. Canadian Journal of Psychology/Revue canadienne de psychologie, 45(3):255, 1991.   
[12] J. Qin, J. Wu, W. Chen, Y. Ren, H. Li, H. Wu, X. Xiao, R. Wang, and S. Wen. Diffusiongpt: Llm-driven text-to-image generation system. arXiv preprint arXiv:2401.10061, 2024.   
[13] L. Qu, S. Wu, H. Fei, L. Nie, and T.-S. Chua. Layoutllm-t2i: Eliciting layout guidance from llm for text-to-image generation. In Proceedings of the 31st ACM International Conference on Multimedia, 2023.   
[14] K. Ranasinghe, S. N. Shukla, O. Poursaeed, M. S. Ryoo, and T.-Y. Lin. Learning to localize objects improves spatial reasoning in visual-llms. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 12977–12987, 2024.   
[15] E. Todorov, T. Erez, and Y. Tassa. Mujoco: A physics engine for model-based control. In 2012 IEEE/RSJ international conference on intelligent robots and systems, pages 5026–5033. IEEE, 2012.   
[16] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems, 35:24824–24837, 2022.   
[17] W. Wu, S. Mao, Y. Zhang, Y. Xia, L. Dong, L. Cui, and F. Wei. Mind’s eye of llms: visualization-of-thought elicits spatial reasoning in large language models. Advances in Neural Information Processing Systems, 37:90277–90317, 2024.   
[18] L. Yang, Z. Yu, C. Meng, M. Xu, S. Ermon, and B. Cui. Mastering text-to-image diffusion: Recaptioning, planning, and generating with multimodal llms. In International Conference on Machine Learning (ICML), 2024.   
[19] L. Yang, Z. Zhang, Y. Song, S. Hong, R. Xu, Y. Zhao, W. Zhang, B. Cui, and M.-H. Yang. Diffusion models: A comprehensive survey of methods and applications. ACM computing surveys, 56(4):1–39, 2023.

[20] L. Zhang, A. Rao, and M. Agrawala. Adding conditional control to text-to-image diffusion models. In Proceedings of the IEEE/CVF international conference on computer vision, pages 3836–3847, 2023.   
[21] Q. Zhao, Y. Lu, M. J. Kim, Z. Fu, Z. Zhang, Y. Wu, M. Li, Q. Ma, S. Han, C. Finn, A. Handa, M.-Y. Liu, D. Xiang, G. Wetzstein, and T.-Y. Lin. Cot-vla: Visual chain-of-thought reasoning for vision-languageaction models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2025.