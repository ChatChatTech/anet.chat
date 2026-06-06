# AndroidLab: Training and Systematic Benchmarking of Android Autonomous Agents

Yifan Xu1∗, Xiao Liu1∗, Xueqiao Sun1, Siyi Cheng2†, Hao Yu1, Hanyu Lai1, Shudan Zhang1, Dan Zhang1, Jie Tang1, Yuxiao Dong1

1Tsinghua University 2Peking University

# Abstract

Autonomous agents have become increasingly important for interacting with the real world. Android agents, in particular, have been recently a frequently-mentioned interaction method. However, existing studies for training and evaluating Android agents lack systematic research on both open-source and closed-source models. In this work, we propose ANDROIDLAB as a systematic Android agent framework. It includes an operation environment with different modalities, action space, and a reproducible benchmark. It supports both large language models (LLMs) and multimodal models (LMMs) in the same action space. ANDROIDLAB benchmark includes predefined Android virtual devices and 138 tasks across nine apps built on these devices. By using the ANDROIDLAB environment, we develop an Android Instruction dataset and train six open-source LLMs and LMMs, lifting the average success rates from 4.59% to 21.50% for LLMs and from 1.93% to 13.28% for LMMs. ANDROIDLAB is open-sourced and publicly available at https://github.com/ THUDM/Android-Lab.

# 1 Introduction

Developing autonomous agents to execute human instructions within mobile operating systems has long been a goal for researchers (Burns et al., 2021; Yang et al., 2023b; Wang et al., 2023a; Hong et al., 2023; Rawles et al., 2023; Li et al., 2020; Romao et al., 2019; Rai et al., 2019). Recently, a significant line of research has focused on using large language models (LLMs) (Zeng et al., 2022; OpenAI, 2023; Anthropic, 2023; Team et al., 2024; GLM et al., 2024) and large multimodal models (LMMs) (OpenAI, 2023; Anthropic, 2023; Hong et al., 2023) as the backbone for these agents (Deng et al., 2023; Rawles et al., 2023; Zhou et al., 2023).

Despite significant advancements, both training and evaluating mobile agents face challenges, with lacking systematic exploration. Previous benchmarks (Rawles et al., 2023; Sun et al., 2022; Li et al., 2020) often rely on reproducible but static environments, where agents are expected to predict actions based on screenshots without actual interaction. AndroidEnv (Toyama et al., 2021) introduced the first interactive environment for mobile agents and later efforts (Lee et al., 2024; Rawles et al., 2024) improved reproducibility but still faced limitations. Moreover, these benchmarks lack systematic evaluation, primarily because almost all recent benchmarks (Yang et al., 2023b; Xing et al., 2024; Lee et al., 2024; Rawles et al., 2024) only tested and implemented prompt-based improvement on closed-source models. This limitation restricts the ability to analyze model behavior, integrate insights, and conduct reinforcement learning experiments effectively. The absence of a unified benchmark comparing open-source and closedsource models across various modalities further exacerbates this issue, limiting opportunities for enhancing open-source solutions.

These issues have motivated us to develop a new Android agent evaluation and training framework. In this paper, we propose ANDROIDLAB, which includes a standard operational environment and a benchmark for agents interacting with Android devices. We define basic operation modes across LLMs and LMMs by aligning actions and objects within different observations of the mobile system: XML and screenshots, termed XML mode and SoM mode, respectively. Additionally, we introduce two modes for each basic mode, ReAct (Yao et al., 2022b) and SeeAct (Zheng et al., 2024). Node information is annotated in the XML for screenshots using set-of-mark (Yang et al., 2023a), ensuring identical actions across modes for a fair comparison. Based on the environment, the AN-DROIDLAB benchmark includes 138 tasks across 9 different apps. By utilizing Android virtual devices with preloaded app operation histories and offline data, ANDROIDLAB ensures reproducibility and eliminates external network or time dependencies.

![](images/8ec07088a083295d2199cac4d9b88e9687505a4389476e94c6e15a836c6c6f81.jpg)  
(a) Overview of the environment and benchmark of ANDROIDLAB.   
(b) Results of Closed Models.   
Figure 1: (a) We design the SoM mode for the multimodal models (LMMs) and the XML mode for the text-only models (LLMs), ensuring an identical action space. We also implement ReAct and SeeAct frameworks in both modes. Based on the environment, we propose the ANDROIDLAB benchmark. (b) ANDROIDLAB benchmark success rates of closed-source models. In the XML mode, GPT-4-1106-Preview has the highest success rate at 31.16%, the same as GPT-4o in the SoM mode.

Previous benchmarks had shortcomings in their evaluation metrics, typically provided standardized sequences of operations (Xing et al., 2024) or device states (Lee et al., 2024; Rawles et al., 2024) as evaluation metrics, which can restrict the diversity of task paths and limit task types to those represented by specific device states. In ANDROIDLAB, each task is divided into multiple required page states as sub-goals, with UI tree structure matching verifying correct traversal. This enables precise assessment of task completion and progress and allows evaluation of nearly all tasks without being constrained by the limitations of system state representations. We also introduce metrics such as reversed redundancy and reasonable operation to evaluate action efficiency.

We have evaluated 17 open-source and closedsource models using the ANDROIDLAB benchmark. Although the GPT series achieved over 30% success rate in both XML and SoM modes, we observed that open-source models performed poorly, with the best reaching only around 5% success rate. Initial attempts to enhance mobile agent performance through more complex reasoning frameworks led to marginal improvements despite significantly increased inference times. Therefore, finetuning small-scale open-source models may bridge the gap to closed-source performance, enhancing mobile agent accessibility.

By using ANDROIDLAB’s operation modes and action space, we have constructed the Android Instruct dataset. We develop an online annotation tool with the same action space, collecting 10.5k traces and 94.3k steps from annotators. Among these, 6208 steps are derived from the Apps included in the ANDROIDLAB benchmark, and we use this portion of the data to fine-tune the model. This dataset includes tasks, phone screen states, XML information, and operations, and has been used to fine-tune six text-only and multimodal models. As shown in Figure 2, fine-tuning with our dataset raises average success rates from 4.59% to 21.50% for LLMs and from 1.93% to 13.28% for LMMs. Our further analysis reveals that fine-tuning improves operational accuracy, efficiency, and reduces redundancy in Android agents.

The contributions are summarized as follows:

• We design the ANDROIDLAB suite, which includes a standard operational environment and a benchmark. This suite unifies the evaluation and training of Android Agents, as shown in Figure 1.   
• We develop ANDROIDLAB benchmark, a reproducible and challenging benchmark for evaluating mobile agent capabilities. It includes a simulated evaluation environment and 138 tasks,

![](images/80afc4e776055f14ce03e623f889d13ad6da6a4879fdff24975b4227d38ad346.jpg)



(a) Overview of Android Instruct data collection.

![](images/60793893961c74b5ff55adb7df2c86b6d118afe455fd3ee3495d8bd70d39b8b9.jpg)



(b) Success Rates of before and after fine-tuning by Android Instruct.   
Figure 2: (a) We have collected over 726 traces containing more than 6208 fully aligned steps of XML and SoM mode training data. (b) By using the Android Instruct dataset, we trained six open-source text-only and multimodal models, achieving an average success rate from 4.59% to 21.50% for LLMs and from 1.93% to 13.28% for LMMs. respectively, reaching a performance level comparable to proprietary models.

as shown in Figure 3 based on text-only or multimodal inputs. ANDROIDLAB benchmark presents significant challenges, as the leading model GPT-4o only achieves 31.16%. Parts of the AndroidLab benchmark’s SoM modes are also included in the VisualAgentBench (Liu et al., 2024) as the VAB-Mobile component.

• We construct an Android Instruct dataset, containing 94.3k operation records for fine-tuning. This dataset supports both text-only and multimodal training, yielding competitive results in LLM and LMM models, as shown in Table 1. We also demonstrate that fine-tuned models achieve comparable scores and offer the best balance of efficiency and accuracy.

# 2 Retated Work

Benchmarks for Agents. Recent advancements in large foundation models have led to new agent benchmarks tailored to these models. Agents interact with external environments primarily through writing code (Chen et al., 2021; Zheng et al., 2023; Zhang et al., 2024; Austin et al., 2021) or invoking APIs (Guo et al., 2024; Li et al., 2023; Peng et al., 2021). Specialized benchmarks have been designed for interaction with operating systems, categorized into Desktop and Mobile. For Desktop, static benchmarks (Mialon et al., 2023; Deng et al., 2023; Kapoor et al., 2024) evaluate agents by single-step operation or operations sequence without a virtual environment. Otherwise, dynamic benchmarks provide interactive web browser (Liu et al., 2018; Zhou et al., 2023; Yao et al., 2022a; Koh et al., 2024) or Unix-like system virtual environment (Hong et al., 2023; Xie et al., 2024), making evaluation more flexible and realistic.

Mobile benchmarks for Android began with static systems like PixelHelp (Li et al., 2020) and MetaGUI (Sun et al., 2022) and later expanded through AITW (Rawles et al., 2023), which provided over 5 million images. AndroidEnv (Toyama et al., 2021) introduced dynamic evaluations, while Android Arena (Xing et al., 2024) added cross-app evaluations. Although task diversity was limited, B-MOCA (Lee et al., 2024) standardized the Android Virtual Device. AndroidWorld (Rawles et al., 2024) offers reward signals for 116 tasks across 20 real-world apps but does not support instructiontuning data construction.

Agents for Interactive System. For Web environments, WebGPT (Nakano et al., 2021) and WebGLM (Liu et al., 2023) integrate LLMs for improved question-answering. MindAct (Deng et al., 2023), WebAgent (Gur et al., 2023), and AutoWebGLM (Lai et al., 2024) focus on executing complex interactive tasks. In mobile agents, early work on Android systems utilized multiple execution modules (Burns et al., 2021; Venkatesh et al., 2023; Li et al., 2020; Zhan and Zhang, 2023). Pixel-Help (Li et al., 2020) mapped actions to images, while Auto-GUI (Zhan and Zhang, 2023) used image and text encoders with LLMs for CoT outputs. CogAgent (Hong et al., 2023) achieved SOTA on AITW (Rawles et al., 2023) by combining modules for action prediction. Recent zero-shot mobile agents using GPT-4V (OpenAI, 2023) have shown strong results (Yang et al., 2023b; Zheng et al., 2024; Yan et al., 2023; Wang et al., 2023a), but planning complexity limits inference speed and practical deployability due to security restrictions.

![](images/d5df6f57b4885816594d31bc86d809f0c024e59bb2b64cc9f682cb7c9c12fa44.jpg)



![](images/dc00a7b46a8dd737aabf6835ee55af2de8e2def3aca0a3f23a119e1ea964d4f7.jpg)



![](images/c0603081a48595ec0a3601c79c5c0beb33604de17aaae6097ecc7336df000c8a.jpg)



![](images/87043800c55ccb04b46823899238bb15f5a66ce17ed950a1bbdd592196f5643a.jpg)



![](images/be76cdde8d27830ef20b86b5a52b6abe8f7a82539b1e93f670c895364df0e154.jpg)



<table><tr><td>Task: Add a contacts whose name is Xu, set the working phone...</td><td>Task: Record an income of 8000 CNY in the books, and mark it as...</td><td>Task: Check the driving distance and time between Bus stop of...</td><td>Task: Sort Pink Floyd&#x27;s songs by duration time in descending order.</td><td>Task: I need set an 10:30PM clock every weekend, and label it...</td></tr><tr><td>Sub-Goals: 
· Name: Xu
· Working phone number
· Mobile phone number</td><td>Sub-Goals: 
· Enter: New income
· Cash: 8000
· Note: ...</td><td>Sub-Goals: 
· Driving distance
· Driving time</td><td>Sub-Goals: 
· Page: ARTISTS
· Artist: Pink Floyd
· Order: Descending</td><td>Sub-Goals: 
· Time: 10:30PM
· Frequency: Weekend
· Label: ...</td></tr></table>

![](images/2b602b066799e4dcb732448ed8f7163216007e21910e9e7395ea712ca98b22e5.jpg)  
Figure 3: Task examples and the distribution of all apps and subcategories in the ANDROIDLAB benchmark. We decomposed each task into sub-goals and evaluated them independently. A task is considered complete only if all sub-goals are correctly addressed.

# 3 ANDROIDLAB

# 3.1 The Operation Environment

ANDROIDLAB defines a set of action spaces and two operation modes, forming the ANDROIDLAB environment. We adopt the main action space from prior work and add a model return value (finish action). The two basic operation modes are SoM (Yang et al., 2023a) and XML-only, differing in whether the agent can access a snapshot of the phone screen. For comparison, we also implement ReAct (Yao et al., 2022b) and SeeAct (Zheng et al., 2024). This framework supports real and virtual Android devices and is compatible with Androidlike mobile operating systems.

Action Space. Based on the action spaces from AppAgent (Yang et al., 2023b) and Android Env (Toyama et al., 2021), we define four basic phone operations: Tap, Swipe, Type, Long Press, along with two shortcut keys, Home and Back, as the core action space. We add the Finish action as the final step, allowing the agent to return execution results or answers. This action space applies to all modes.

XML Mode. XML mode is tailored for textonly input models (LLM). Inspired by Android Arena (Xing et al., 2024), we redesign the XML compression algorithm to convey screen information. The LLM selects corresponding elements directly for operations.

SoM Mode. SoM mode is for multimodal input models (LMM), based on the Set-of-Mark method (Yang et al., 2023a). Each clickable or focusable element is assigned a serial number, and the LMM selects the element by its number. The selected elements in SoM mode align with those in the compressed XML list, allowing both modes to interact with the same action space and objects.

These basic operation modes directly require the agent to output operation commands. Based on these two methods, we further test two novel agent frameworks, ReAct (Yao et al., 2022b) and See-Act (Zheng et al., 2024). These two frameworks allow the agent to observe and reflect on the environment or more easily select specific tasks to execute. Please refer to Appendix B for more details about our operation modes.

ReAct modes. Based on the above two modes, we follow (Yao et al., 2022b) to prompt the model, allowing models to think step by step and output their thought and reasoning process.

SeeAct modes. Following (Zheng et al., 2024), we separate the reasoning and element grounding process. We instruct models to interact for two rounds in a single operation. The models are supposed to generate a detailed description of the desired action and output the real action, respectively.

# 3.2 The Reproducible Benchmark

Based on the environment, ANDROIDLAB benchmark offers a deterministic and reproducible evaluation platform, allowing users to perform fair and challenging comparisons of Android agent capabilities. ANDROIDLAB benchmark introduces the following designs:

• We gathered 138 tasks from nine apps, ensuring reproducibility. These tasks, derived from common mobile scenarios, are divided into two types: (a) Operation Tasks, where agents must complete a series of actions to meet a goal, and (b) Query Tasks, where agents answer queries based on phone information.   
• Using phone XML data, we identify screen information that uniquely defines task completion, making task completion our primary metric. Additionally, we select auxiliary metrics such as the proportion of valid actions and the redundancy of successful operation sequences.

# 3.2.1 Task Formulation

We formalize each task input as a 4-tuple: Task(E, I, F, M ). Here, E represents the execution environment of the task, which, in the context of benchmark testing, is the pre-packaged AVD (Android virtual device) image. This includes a fixed phone screen size, Android version, API level, and a fixed app usage state. I denotes the specific natural language instruction for the task. To avoid confusion during testing, we specify the app required to complete the task in natural language. F represents the agent testing framework. Finally, M denotes the backbone model used to perform the task, primarily referring to LLMs or LMMs.

Thus, we can formally define the two types of tasks included in ANDROIDLAB:

Operation Task. $\mathrm { T } ( E , I , F , M )  ( S _ { 1 } , \ldots , S _ { n } )$ The output of this type of task is a sequence of continuous Android virtual machine states.

Query Task. $\mathrm { T } ( E , I , F , M )  ( S _ { 1 } , . . . , S _ { n } , A )$ . This type of task assesses the agent’s ability to answer specific questions based on the state sequence after exploration. The model must explore the environment to find the answers and output the correct response.

Based on the above formulation, we design 138 tasks, including 93 Operation Tasks and 45 Query Tasks. Please refer to Appendix A for detailed information.

# 3.2.2 Reproducible Designs

To ensure our evaluation reflects real-world agent usage scenarios with an appropriate level of difficulty and full reproducibility, we design the tasks with the following considerations:

• Fixed Evaluation Time and Space: We use ADB commands at the start of each evaluation to set the machine’s time and virtual geolocation to predetermined values.   
• Offline Testing: All test apps function offline, with preloaded usage records in the AVD image to ensure normal usability without an internet connection.   
• Predefined Answers: For query-based tasks, we conduct operations on the corresponding apps in advance to guarantee uniquely determined correct results.

# 3.2.3 Metrics

Previous evaluations with virtual environments have relied on indirect metrics like single-step accuracy and operation path matching, leading to imprecise assessments. In response, ANDROIDLAB benchmark introduces a task-completion-based evaluation system that judges directly from device and screen states. Our key metrics are:

• Success Rate: For Operation Tasks, we divided a complete task into multiple sub-goals and identified the specific page information for each subgoal completion. By checking and matching specific UI tree elements, we assess each sub-goal completion status individually. The task is considered successfully executed when all sub-goals are completed. We have also set up a few tasks that can directly use the device state to determine if they were completed correctly. For Query Tasks, advanced LLMs verify if the model’s predicted results match the standard answers, avoiding errors from direct string comparisons. We provide an example in Fig 4.

![](images/1f73c99aff962368b41eae6f4564a4c97ddd270ec184ed533647f719cbf5d864.jpg)



Figure 4: An example of an agent completing all sub-goals of the entire task. We only present the starting and ending steps, along with the steps where the agent completes each sub-goal. It is essential that we record the completion status of each sub-goal. Without this information, we may not be able to obtain detailed information from the XML of the finished page, which could lead to a misjudgment of the task.

• Sub-Goal Success Rate: Tasks are decomposed into sub-goals, and completion is assessed sequentially. This finer metric rewards models with stronger understanding and operational capabilities. Only Operation Tasks include the Sub-Goal Success Rate.   
• Reversed Redundancy Ratio: As in prior work (Xing et al., 2024), redundancy is measured by comparing the model’s operation path length to a human benchmark. We calculate this for completed tasks and take the reciprocal, so higher values indicate less redundancy. We do not report SR < 5 because there are too few completed tasks, which may be affected by a small number of special values. It should also be emphasized that this metric may exceed 100 because the steps of human operation are not necessarily optimal.   
• Reasonable Operation Ratio: This metric eval-

uates the proportion of operations after which the screen changed. Unchanged screens indicate the operation was ineffective and thus deemed unreasonable.

By incorporating these metrics, our evaluation system provides a comprehensive and precise assessment of an agent’s performance in completing specified tasks.

# 4 Android Instruction Data

Building an open-source, deployable Android operation agent is a significant challenge in AI research. Previous work on Android agents has focused on using powerful closed-source models to design interaction logic (Zheng et al., 2024; Yang et al., 2023b; Wang et al., 2023a), raising concerns about accessibility, privacy, and efficiency. To address this, we aim to build an open-source mobile agent. The main challenge lies in generating training data for mobile operations to handle open-world tasks in diverse environments.

We propose task derivation and expansion methods for task generation, allowing models to generate tasks for specific apps controllably. ANDROID-LAB connects to devices via ADB, enabling compatibility with various real or virtual devices for data generation. Using self-exploration and manual annotation, we generate example operation traces. To make it easier for annotators to work on real devices (rather than emulators), we developed an online annotation tool. This tool uses ADB commands to monitor user interactions on the phone and captures screenshots and page XML before each action. Our Android Instruction data is built on the Task (E, I, F) framework within ANDROID-LAB’s environment.

![](images/dcd7ab8bdbd3a260437fc15a2fd0d1892bfbace960267e090c8509f404c24782.jpg)



(a) Step Distribution Across Tasks

![](images/fec5d0f46e1161c63c90b5953ee56fd81c682d190aa316db1083f23af51275c9.jpg)



(b) Top 20 Words in Instructions.

![](images/cf23b5827b53e1ab9baa08eff51b0de6c7a4bd091fa9a714df2d5c4769a1878c.jpg)



(c) Instruction Length Distribution.

![](images/b3f5046925f22fd82ee95f2800f1588224477ef643345f4db70add82ab31f6f3.jpg)



(d) APP Distribution.

![](images/fa9f5aae9d603976b5cf798766e3249d645f5c80a639eb600de64faca565ee34.jpg)



(e) Actions Distribution.

![](images/16c806f19047683025dbe170d9a60dcf18262bfaabd1930b9aabf138284e3790.jpg)



(f) Average Task Length per App   
Figure 5: Statistics for Android Instruct dataset. We collect 726 traces and 6208 steps across Apps in ANDROIDLAB benchmark.

# 4.1 Data Construction

The primary challenges in data construction include generating executable Android instructions and annotating operation path data. Our approach involves three steps:

1. Task Derivation and Expansion: We use academic datasets (Rawles et al., 2023; Coucke et al., 2018) and manually write instructions to seed task generation. Language models are employed to create additional tasks, which are reviewed and added to the dataset, ensuring realistic and executable instructions.   
2. Self-Exploration: LLMs and LMMs are used for automatic task exploration, outputting finish when done. Initially, manual selection was used to verify results, but a reward model later replaced it after gathering 500 traces.   
3. Manual Annotation: This process involves four steps: (1) Instruction Check, where annotators evaluate the feasibility of the given task; (2)

Preliminary Familiarization, allowing them to explore the app interface before performing tasks; (3) Task Execution, in which the annotators execute and document each task step; and (4) Cross-Verification, where a second annotator reviews the task trace to ensure its accuracy.

This combination of autonomous and manual processes resulted in 10.5k traces and 94.3k steps, and we use 726 traces and 6208 steps derived from the Apps included in the ANDROIDLAB benchmark for training. We provide statistics of the Android Instruct dataset in Fig 5. More details are in Appendix C.

# 4.2 Annotation Tool

To more accurately and efficiently record operation trajectories and page information (XML), we design an annotation tool.

Acquisition of Page Information: Android Debug Bridge (ADB) is currently the most widely used tool for obtaining page information (Yang et al., 2023b; Rawles et al., 2024). ADB is a versatile command-line utility that retrieves the XML data of the current page. However, when dealing with a diverse range of mobile applications, ADB sometimes fails to acquire the XML for certain pages. Specifically, ADB waits for all UI components on the page to become idle before retrieving component information. If this process exceeds a predefined time limit, ADB stops the XML acquisition. This issue is particularly evident on mobile pages with dynamic components, such as playback bars and animations in audio players, where continuously active elements prevent ADB from obtaining the XML. To address this, we reimplemented the XML acquisition functionality using the Android Accessibility Service, allowing annotators to determine the appropriate timing for retrieving page XML.

Recording Operation Trajectories: We mainly need to record three types of user actions: clicks, swipes, and text input. For click actions and swipe actions, annotators complete the actions directly on the phone, while we use ADB commands to capture screen events. Based on the press, release positions, and duration of these events, we determine whether the action was a click or swipe. For text input, we utilize the ADB keyboard to complete the entire input in a single operation, minimizing the number of annotations required. Before each action, the user must first use the annotation tool to record the current page information, ensuring that the recorded page data matches the context observed during human interaction.

# 4.3 Training

To explore the effectiveness of our dataset on lightweight open-source models, we select Llama-3.1-8B-Instruct, GLM-4-9B-Chat, Qwen2-7B-Instruct, Llama-3.2-11B-Vision-Instruct, Qwen2- VL-7B-Instruct and CogVLM2 (cogvlm2-llama3- chat-19B) as the training backbones for LLM and LMM, respectively. Due to our preliminary experiments showing that training agents from base models yield better results, we select the base versions of all models for fine-tuning, except for Qwen2- VL-7B-Instruct (as no open-source base model is available). However, we still report the instruct versions as baselines because the base models cannot follow instructions without further tuning. For all training sessions, we use a batch size of 32 and a maximum sequence length of 4096, training for five epochs. The learning rate is set to 1e-5.

# 5 Experiments

# 5.1 Experiment Setup

Evaluation Settings. In preliminary tests, we found that even though we specified the use of certain apps in the instructions, agents failed to complete tasks because they could not launch the respective apps correctly. To avoid errors caused by a single reason, we start tasks directly within the specified app in the formal experiments and then allow the agent to proceed. Additionally, we set a maximum execution step limit of 25 for each task, with a 3-second interval for the virtual machine to respond to each operation. We generate by greedy search for each task of all models.

Baseline Models. For large language models (LLMs) with text-only input capability, we selected GPT-4o (OpenAI, 2023), GPT-4-1106- Preview (OpenAI, 2023), Gemini-1.5-Pro (Team et al., 2024), Gemini-1.0 (Team et al., 2024), GLM-4-PLUS (GLM et al., 2024), Llama-3.1-8B-Instruct (Touvron et al., 2023), GLM-4-9B-Chat (GLM et al., 2024) and Qwen2-7B-Instruct (Bai et al., 2023) as the baselines for testing in the XML mode. For large multimodal models (LMMs) with image input capability, we chose GPT-4o (OpenAI, 2023), GPT-4-Vision-Preview (OpenAI, 2023), Gemini-1.5-Pro (Team et al., 2024), Gemini-1.0 (Team et al., 2024), Claude-3.5-Sonnet, Claude-3-Opus (Anthropic, 2023), Llama-3.2-11B-Vision-Instruct (Touvron et al., 2023), Qwen2-VL-7B-Instruct (Wang et al., 2024) and CogVLM2 (Wang et al., 2023b) as the baselines for testing in the SoM mode. We also further evaluated the performance of GPT-4o and Gemini-1.5-Pro under the ReAct and SeeAct frameworks in both modes.

# 5.2 Main Results

As shown in Table 1, in the XML mode, GPT-4- 1106-Preview outperforms the other models with a Success Rate (SR) of 31.16%, the highest in this mode while also achieving the best Sub-Goal Success Rate (Sub-SR) at 38.21%. Although GPT-4o exhibits slightly lower SR (25.36%), it achieves the highest Reversed Redundancy Ratio (RRR) at 107.45, indicating its strong ability to reduce unnecessary operations. The ROR metric shows that both models in the GPT-4 series perform comparably, with around 86% of operations being reasonable but with room for improvement in efficiency. Other models, such as Gemini-1.5-Pro, show moderate performance, with ROR around 80, but lag in SR.

In the SoM mode, GPT-4o again shows dominance, reaching an SR of 31.16% and a Sub-SR of 35.02%, the highest in both categories. GPT-4-Vision-Preview follows closely, but models like Claude-3.5-Sonnet exceeded GPT-4o in RRR (113.40), demonstrating a higher efficiency in task completion with fewer redundant steps. The Reasonable Operation Ratio in SoM mode indicates that models such as tuned LLaMA3.2-11B-Vision achieve the best ROR at 92.57%, showing the most effectiveness in this mode.

Table 1: Main Result of XML and SoM modes. SR, Sub-SR, RRR, and ROR stand for Success Rate, Sub-Goal Success Rate, Reversed Redundancy Ratio, and Reasonable Operation Ratio, respectively. For all these metrics, a higher value means better. -ft represents a finetuned model. In each mode, Bold represents the best result. We do not report RRR score if SR < 5. 

<table><tr><td>Mode</td><td>Model</td><td>SR</td><td>Sub-SR</td><td>RRR</td><td>ROR</td></tr><tr><td rowspan="8">XML</td><td>GPT-4o</td><td>25.36</td><td>30.56</td><td>107.45</td><td>86.56</td></tr><tr><td>GPT-4-1106-Preview</td><td>31.16</td><td>38.21</td><td>66.34</td><td>86.24</td></tr><tr><td>Gemini-1.5-Pro</td><td>18.84</td><td>22.40</td><td>57.72</td><td>83.99</td></tr><tr><td>Gemini-1.0</td><td>8.70</td><td>10.75</td><td>51.80</td><td>71.08</td></tr><tr><td>GLM4-PLUS</td><td>27.54</td><td>32.08</td><td>92.35</td><td>83.41</td></tr><tr><td>LLaMA3.1-8B-Instruct</td><td>2.17</td><td>3.62</td><td>-</td><td>52.77</td></tr><tr><td>Qwen2-7B-Instruct</td><td>4.35</td><td>4.95</td><td>-</td><td>67.26</td></tr><tr><td>GLM4-9B-Chat</td><td>7.25</td><td>9.06</td><td>54.43</td><td>58.34</td></tr><tr><td rowspan="3">XML+SFT</td><td>LLaMA3.1-8B-ft</td><td>23.91</td><td>30.31</td><td>75.58</td><td>92.46</td></tr><tr><td>Qwen2-7B-ft</td><td>19.57</td><td>24.40</td><td>77.31</td><td>92.48</td></tr><tr><td>GLM4-9B-ft</td><td>21.01</td><td>26.45</td><td>74.81</td><td>93.25</td></tr><tr><td rowspan="9">SoM</td><td>GPT-4o</td><td>31.16</td><td>35.02</td><td>87.32</td><td>85.36</td></tr><tr><td>GPT-4-Vision-Preview</td><td>26.09</td><td>29.53</td><td>99.22</td><td>78.79</td></tr><tr><td>Gemini-1.5-Pro</td><td>16.67</td><td>18.48</td><td>105.95</td><td>91.52</td></tr><tr><td>Gemini-1.0</td><td>10.87</td><td>12.56</td><td>72.52</td><td>76.70</td></tr><tr><td>Claude-3.5-Sonnet</td><td>28.99</td><td>32.66</td><td>113.41</td><td>81.16</td></tr><tr><td>Claude-3-Opus</td><td>13.04</td><td>15.10</td><td>81.41</td><td>83.89</td></tr><tr><td>CogVLM2</td><td>0.72</td><td>0.72</td><td>-</td><td>17.97</td></tr><tr><td>LLaMA3.2-11B-Vision-Instruct</td><td>1.45</td><td>1.45</td><td>-</td><td>50.76</td></tr><tr><td>Qwen2-VL-7B-Instruct</td><td>3.62</td><td>4.59</td><td>-</td><td>84.81</td></tr><tr><td rowspan="3">SoM+SFT</td><td>CogVLM2-ft</td><td>11.59</td><td>16.06</td><td>57.37</td><td>85.58</td></tr><tr><td>LLaMA3.2-11B-Vision-ft</td><td>10.14</td><td>12.98</td><td>61.67</td><td>87.85</td></tr><tr><td>Qwen2-VL-7B-Instruct-ft</td><td>18.12</td><td>22.64</td><td>65.23</td><td>88.29</td></tr></table>

Fine-tuning improves several models across both modes, notably boosting the Success Rate and ROR of all fine-tuned open-source models. Fine-tuning notably increased the Success Rate (SR) for models like LLaMA3.1-8B and Qwen2-7B, raising their SR from 2.17 to 23.91 and 4.35 to 19.57, respectively. The Reasonable Operation Ratio (ROR) also saw improvements, with models such as CogVLM2 jumping from 17.97 to 85.58 after fine-tuning.

# 5.3 Additional Findings

Influence of Instruction Tuning. Instruction tuning significantly enhances the performance of models across all four metrics in both XML and SoM modes, lifting the average success rates from 4.59% to 21.50% for LLMs and from 1.93% to 13.28% for LMMs. Notably, GLM4-9B’s success rate rose to 21.01%, with its Reasonable Operation Ratio (ROR) improving to 93.25, indicating better operational efficiency. The Reversed Redundancy Ratio (RRR) saw consistent gains, demonstrating reduced unnecessary actions, such as GLM4-9B improving its RRR from 54.43 to 74.81.

In SoM mode, models like CogVLM2, LLaMA3.2-11B, and Qwen2-VL-7B showed significant advancements across all four metrics. Qwen2-VL-7B’s SR increased from 3.62 to 18.12%, and its ROR rose to 88.29. The Sub-SR and RRR also benefited from tuning, marking improved task breakdown and reduced redundancy. After tuning, the best-performing opensource LLMs are approaching the level of GPT-4o, while the top LMMs have surpassed Gemini-1.5- Pro, reflecting comprehensive improvements across success, operational efficiency, and task execution. The tuned models’ effective actions (ROR) have also surpassed those of most closed-source models, demonstrating enhanced precision.

Influence of Windows Size. As shown in Figure 6, experiments with three Android VMs of varying sizes in SoM mode show optimal agent performance on screens matching commonly used smartphones (e.g., Pixel 7 Pro, Pixel 8 Pro). Performance drops on smaller (Pixel 3a) and larger screens (Pixel Fold) due to increased scrolling needs and landscape orientation challenges, respectively.

Table 2: The impact of the ReAct and SeeAct frameworks on SR results. Notably, model performance is significantly improved in XML+ReAct mode. Full results of this table are shown in Appendix D.3 

<table><tr><td>Mode</td><td>Model</td><td>SR</td></tr><tr><td rowspan="2">XML</td><td>GPT-4o</td><td>25.36</td></tr><tr><td>Gemini-1.5-Pro</td><td>18.84</td></tr><tr><td rowspan="2">XML+ReAct</td><td>GPT-4o</td><td>33.33</td></tr><tr><td>Gemini-1.5-Pro</td><td>31.16</td></tr><tr><td rowspan="2">XML+SeeAct</td><td>GPT-4o</td><td>24.64</td></tr><tr><td>Gemini-1.5-Pro</td><td>21.01</td></tr><tr><td rowspan="2">SoM</td><td>GPT-4o</td><td>31.16</td></tr><tr><td>Gemini-1.5-Pro</td><td>16.67</td></tr><tr><td rowspan="2">SoM+ReAct</td><td>GPT-4o</td><td>31.88</td></tr><tr><td>Gemini-1.5-Pro</td><td>15.94</td></tr><tr><td rowspan="2">SoM+SeeAct</td><td>GPT-4o</td><td>30.43</td></tr><tr><td>Gemini-1.5-Pro</td><td>21.01</td></tr></table>

Table 3: Average generation tokens of different modes. We used the LLaMA3 tokenizer for calculation. FT represents instruction tuning models. 

<table><tr><td>Mode</td><td>FT</td><td>XML/SoM</td><td>ReAct</td><td>SeeAct</td></tr><tr><td>#Avg. Gen. Tokens</td><td>4.96</td><td>23.56</td><td>67.89</td><td>129.12</td></tr></table>

Analysis of Agent Frameworks. We assess ReAct and SeeAct frameworks with GPT-4o and Gemini-1.5-Pro in XML and SoM modes. Table2 shows ReAct significantly improves performance only in XML mode. SeeAct does not enhance performance consistently due to the model’s reasoning limitations with multimodal input. We also compare the SoM framework and bbox-only and show SoM is better; please refer to Appendix D.2 for more detail. ReAct and SeeAct frameworks increase token usage, harming efficiency. As per Table 3, XML+ReAct settings produce an average of 67.89 tokens, while models post-Instruction Tuning averaged only 4.96 tokens.

![](images/de5c4348763332590c23fb25e77f34e10462690cf63cd6afafcd44c14b63a428.jpg)



Figure 6: The performance of four models across four different device types is presented. Among these, the Pixel 3a is a smaller-sized phone, the Pixel 7 Pro and Pixel 8 Pro are of sizes comparable to commonly used phones, and the Pixel Fold is akin to a tablet.

# 6 Conclusion

In this paper, we introduced ANDROIDLAB, which includes a standard operational environment and a benchmark for agents interacting with Android devices. By integrating the XML and SoM operation modes, we ensured that the action space was consistent, enabling fair comparisons across different models. ANDROIDLAB benchmark encompasses 138 tasks from nine apps, focusing on reproducibility and real-world relevance, allowing for precise task completion and progress assessment. We also introduced the Android Instruct dataset, comprising 10.5k traces and 94.3k steps, which significantly boosted the performance of open-source models when used for fine-tuning.

Our experiments demonstrated that fine-tuned open-source models have shown considerable improvements while top-performing closed-source models like GPT-4o and Claude-3.5-Sonnet continue to lead in success rates and efficiency. Notably, fine-tuning raised success rates and operational efficiency, helping some models approach or even surpass closed-source counterparts in certain metrics. These findings highlight the potential of open-source models to enhance mobile agent performance, suggesting that further fine-tuning and optimization could narrow the gap between open and closed-source solutions. Future work could explore minimizing redundancy and improving task efficiency, enhancing the practical deployability of Android agents.

# Acknowledgment

We would like to thank Zhipu AI for sponsoring the computation resources and annotation costs used in this work.

# References

Anthropic. 2023. Introducing claude.

Jinze Bai, Shuai Bai, et al. 2023. Qwen technical report.   
Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, and Charles Sutton. 2021. Program synthesis with large language models.   
Andrea Burns, Deniz Arsan, Sanjna Agrawal, Ranjitha Kumar, Kate Saenko, and Bryan A Plummer. 2021. Mobile app tasks with iterative feedback (motif): Addressing task feasibility in interactive visual environments. arXiv preprint arXiv:2104.08560.   
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. 2021. Evaluating large language models trained on code.   
Alice Coucke, Alaa Saade, Adrien Ball, Théodore Bluche, Alexandre Caulier, David Leroy, Clément Doumouro, Thibault Gisselbrecht, Francesco Caltagirone, Thibaut Lavril, Maël Primet, and Joseph Dureau. 2018. Snips voice platform: an embedded spoken language understanding system for privateby-design voice interfaces.   
Xiang Deng, Yu Gu, Boyuan Zheng, Shijie Chen, Samuel Stevens, Boshi Wang, Huan Sun, and Yu Su. 2023. Mind2web: Towards a generalist agent for the web. arXiv preprint arXiv:2306.06070.   
Team GLM, Aohan Zeng, Bin Xu, Bowen Wang, Chenhui Zhang, Da Yin, Diego Rojas, Guanyu Feng, Hanlin Zhao, Hanyu Lai, et al. 2024. Chatglm: A family of large language models from glm-130b to glm-4 all tools. arXiv preprint arXiv:2406.12793.   
Zhicheng Guo, Sijie Cheng, Hao Wang, Shihao Liang, Yujia Qin, Peng Li, Zhiyuan Liu, Maosong Sun, and Yang Liu. 2024. Stabletoolbench: Towards stable large-scale benchmarking on tool learning of large language models.

Izzeddin Gur, Hiroki Furuta, Austin Huang, Mustafa Safdari, Yutaka Matsuo, Douglas Eck, and Aleksandra Faust. 2023. A real-world webagent with planning, long context understanding, and program synthesis. arXiv preprint arXiv:2307.12856.   
Wenyi Hong, Weihan Wang, Qingsong Lv, Jiazheng Xu, Wenmeng Yu, Junhui Ji, Yan Wang, Zihan Wang, Yuxiao Dong, Ming Ding, and Jie Tang. 2023. Cogagent: A visual language model for gui agents.   
Raghav Kapoor, Yash Parag Butala, Melisa Russak, Jing Yu Koh, Kiran Kamble, Waseem Alshikh, and Ruslan Salakhutdinov. 2024. Omniact: A dataset and benchmark for enabling multimodal generalist autonomous agents for desktop and web. arXiv preprint arXiv:2402.17553.   
Jing Yu Koh, Robert Lo, Lawrence Jang, Vikram Duvvur, Ming Chong Lim, Po-Yu Huang, Graham Neubig, Shuyan Zhou, Ruslan Salakhutdinov, and Daniel Fried. 2024. Visualwebarena: Evaluating multimodal agents on realistic visual web tasks. arXiv preprint arXiv:2401.13649.   
Hanyu Lai, Xiao Liu, Iat Long Iong, Shuntian Yao, Yuxuan Chen, Pengbo Shen, Hao Yu, Hanchen Zhang, Xiaohan Zhang, Yuxiao Dong, et al. 2024. Autowebglm: Bootstrap and reinforce a large language model-based web navigating agent. arXiv preprint arXiv:2404.03648.   
Juyong Lee, Taywon Min, Minyong An, Changyeon Kim, and Kimin Lee. 2024. Benchmarking mobile device control agents across diverse configurations.   
Minghao Li, Feifan Song, Bowen Yu, Haiyang Yu, Zhoujun Li, Fei Huang, and Yongbin Li. 2023. Apibank: A benchmark for tool-augmented llms. arXiv preprint arXiv:2304.08244.   
Yang Li, Jiacong He, Xin Zhou, Yuan Zhang, and Jason Baldridge. 2020. Mapping natural language instructions to mobile UI action sequences. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 8198–8210, Online. Association for Computational Linguistics.   
Evan Zheran Liu, Kelvin Guu, Panupong Pasupat, Tianlin Shi, and Percy Liang. 2018. Reinforcement learning on web interfaces using workflow-guided exploration. In International Conference on Learning Representations (ICLR).   
Xiao Liu, Hanyu Lai, Hao Yu, Yifan Xu, Aohan Zeng, Zhengxiao Du, Peng Zhang, Yuxiao Dong, and Jie Tang. 2023. Webglm: Towards an efficient webenhanced question answering system with human preferences. arXiv preprint arXiv:2306.07906.   
Xiao Liu, Tianjie Zhang, Yu Gu, Iat Long Iong, Yifan Xu, Xixuan Song, Shudan Zhang, Hanyu Lai, Xinyi Liu, Hanlin Zhao, et al. 2024. Visualagentbench: Towards large multimodal models as visual foundation agents. arXiv preprint arXiv:2408.06327.

Grégoire Mialon, Clémentine Fourrier, Craig Swift, Thomas Wolf, Yann LeCun, and Thomas Scialom. 2023. Gaia: a benchmark for general ai assistants.   
Reiichiro Nakano, Jacob Hilton, Suchir Balaji, Jeff Wu, Long Ouyang, Christina Kim, Christopher Hesse, Shantanu Jain, Vineet Kosaraju, William Saunders, et al. 2021. Webgpt: Browser-assisted questionanswering with human feedback. arXiv preprint arXiv:2112.09332.   
OpenAI. 2023. Gpt-4 technical report.   
Yun Peng, Shuqing Li, Wenwei Gu, Yichen Li, Wenxuan Wang, Cuiyun Gao, and Michael Lyu. 2021. Revisiting, benchmarking and exploring api recommendation: How far are we?   
Divyanshu Rai, Sumbul Siddiqui, Mahesh Pawar, and Sachin Goyal. 2019. Robotic process automation: the virtual workforce. International Journal on Future Revolution in Computer Science & Communication Engineering, 5(2):28–32.   
Christopher Rawles, Sarah Clinckemaillie, Yifan Chang, Jonathan Waltz, Gabrielle Lau, Marybeth Fair, Alice Li, William Bishop, Wei Li, Folawiyo Campbell-Ajala, Daniel Toyama, Robert Berry, Divya Tyamagundlu, Timothy Lillicrap, and Oriana Riva. 2024. Androidworld: A dynamic benchmarking environment for autonomous agents.   
Christopher Rawles, Alice Li, Daniel Rodriguez, Oriana Riva, and Timothy Lillicrap. 2023. Android in the wild: A large-scale dataset for android device control. arXiv preprint arXiv:2307.10088.   
Mário Romao, Joao Costa, and Carlos J Costa. 2019. Robotic process automation: A case study in the banking industry. In 2019 14th Iberian Conference on information systems and technologies (CISTI), pages 1–6. IEEE.   
Liangtai Sun, Xingyu Chen, Lu Chen, Tianle Dai, Zichen Zhu, and Kai Yu. 2022. Meta-gui: Towards multi-modal conversational agents on mobile gui.   
Gemini Team, Machel Reid, Nikolay Savinov, and Denis Teplyashin et al. 2024. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context.   
Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. 2023. Llama: Open and efficient foundation language models. arXiv preprint arXiv:2302.13971.   
Daniel Toyama, Philippe Hamel, Anita Gergely, Gheorghe Comanici, Amelia Glaese, Zafarali Ahmed, Tyler Jackson, Shibl Mourad, and Doina Precup. 2021. Androidenv: A reinforcement learning platform for android. arXiv preprint arXiv:2105.13231.

Sagar Gubbi Venkatesh, Partha Talukdar, and Srini Narayanan. 2023. Ugif: Ui grounded instruction following.   
Bryan Wang, Gang Li, and Yang Li. 2023a. Enabling conversational interaction with mobile ui using large language models.   
Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, et al. 2024. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. arXiv preprint arXiv:2409.12191.   
Weihan Wang, Qingsong Lv, Wenmeng Yu, Wenyi Hong, Ji Qi, Yan Wang, Junhui Ji, Zhuoyi Yang, Lei Zhao, Xixuan Song, Jiazheng Xu, Bin Xu, Juanzi Li, Yuxiao Dong, Ming Ding, and Jie Tang. 2023b. Cogvlm: Visual expert for pretrained language models.   
Tianbao Xie, Danyang Zhang, Jixuan Chen, Xiaochuan Li, Siheng Zhao, Ruisheng Cao, Toh Jing Hua, Zhoujun Cheng, Dongchan Shin, Fangyu Lei, Yitao Liu, Yiheng Xu, Shuyan Zhou, Silvio Savarese, Caiming Xiong, Victor Zhong, and Tao Yu. 2024. Osworld: Benchmarking multimodal agents for open-ended tasks in real computer environments.   
Mingzhe Xing, Rongkai Zhang, Hui Xue, Qi Chen, Fan Yang, and Zhen Xiao. 2024. Understanding the weakness of large language model agents within a complex android environment. arXiv preprint arXiv:2402.06596.   
An Yan, Zhengyuan Yang, Wanrong Zhu, Kevin Lin, Linjie Li, Jianfeng Wang, Jianwei Yang, Yiwu Zhong, Julian McAuley, Jianfeng Gao, Zicheng Liu, and Lijuan Wang. 2023. Gpt-4v in wonderland: Large multimodal models for zero-shot smartphone gui navigation.   
Jianwei Yang, Hao Zhang, Feng Li, Xueyan Zou, Chunyuan Li, and Jianfeng Gao. 2023a. Set-of-mark prompting unleashes extraordinary visual grounding in gpt-4v.   
Zhao Yang, Jiaxuan Liu, Yucheng Han, Xin Chen, Zebiao Huang, Bin Fu, and Gang Yu. 2023b. Appagent: Multimodal agents as smartphone users. arXiv preprint arXiv:2312.13771.   
Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan. 2022a. Webshop: Towards scalable real-world web interaction with grounded language agents. Advances in Neural Information Processing Systems, 35:20744–20757.   
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. 2022b. React: Synergizing reasoning and acting in language models. arXiv preprint arXiv:2210.03629.   
Aohan Zeng, Xiao Liu, Zhengxiao Du, Zihan Wang, Hanyu Lai, Ming Ding, Zhuoyi Yang, Yifan Xu, Wendi Zheng, Xiao Xia, et al. 2022. Glm-130b:

An open bilingual pre-trained model. arXiv preprint arXiv:2210.02414.

Zhuosheng Zhan and Aston Zhang. 2023. You only look at screens: Multimodal chain-of-action agents. arXiv preprint arXiv:2309.11436.

Shudan Zhang, Hanlin Zhao, Xiao Liu, Qinkai Zheng, Zehan Qi, Xiaotao Gu, Xiaohan Zhang, Yuxiao Dong, and Jie Tang. 2024. Naturalcodebench: Examining coding performance mismatch on humaneval and natural user prompts. arXiv preprint arXiv:2405.04520.

Boyuan Zheng, Boyu Gou, Jihyung Kil, Huan Sun, and Yu Su. 2024. Gpt-4v (ision) is a generalist web agent, if grounded. arXiv preprint arXiv:2401.01614.

Qinkai Zheng, Xiao Xia, Xu Zou, Yuxiao Dong, Shan Wang, Yufei Xue, Zihan Wang, Lei Shen, Andi Wang, Yang Li, et al. 2023. Codegeex: A pre-trained model for code generation with multilingual evaluations on humaneval-x. arXiv preprint arXiv:2303.17568.

Shuyan Zhou, Frank F Xu, Hao Zhu, Xuhui Zhou, Robert Lo, Abishek Sridhar, Xianyi Cheng, Yonatan Bisk, Daniel Fried, Uri Alon, et al. 2023. Webarena: A realistic web environment for building autonomous agents. arXiv preprint arXiv:2307.13854.

# A Details of Tasks

In our experiment, we use various apps to conduct various tests (succinctly presented in Table 4). The following mobile apps are chosen:

• Bluecoins: A personal finance management app used for tracking expenses and income.   
• Calendar: A calendar app helps in organizing schedules and setting reminders.   
• Cantook: An e-book reader for storing, managing, and reading e-books.   
• Clock: A clock app for displaying the time, setting alarms, and using a stopwatch.   
• Contacts: A contact management app for storing and organizing contact information.   
• Maps.me: An offline map app for navigation and exploring locations.   
• PiMusic: A music player app for organizing and playing locally stored music files.   
• Settings: A settings app for configuring device settings and preferences.   
• Zoom: A video conferencing app for hosting and joining online meetings.

The selection of these apps goes through multiple iterations to ensure their suitability for our evaluation purposes. A key criterion for the final selection is that each app functions independently, without requiring an internet connection or user account login. This ensures that the evaluations can be consistently replicated under the same conditions, eliminating external dependencies and reducing the risk of privacy breaches. As a result, this approach maintains the reliability and reproducibility of our results.

# B Detail of Operation Modes

# B.1 XML mode

As shown in Figure 7, in this mode, we prompt models with a task description, interaction history, and current compressed XML information. The models are supposed to output an action in functioncall format. The actions are applied on coordinates shown in XML.

# B.2 SoM mode

As shown in Figure 8, in this mode, we prompt models with a task description, interaction history, and current screenshot with a set of marks(Yang et al., 2023a). The models are also supposed to output an action in function-call format. Different from XML mode, the actions are performed on specified elements via marked indices.

# B.3 ReAct mode

We follow (Yao et al., 2022b) for ReAct prompting. In this mode, we perform both text-only and multimodal testing. The text-only and multi-modal prompts are based on Section B.1 and Section B.2 respectively. We both add prompts that allow models to think step by step before output actions.

# B.4 SeeAct mode

We follow (Zheng et al., 2024) for SeeAct prompting. The raw prompts of SeeAct are designed for web browsers. To adopt that in Android environments, we make some modifications, and the final prompts are shown in Figure 9 for multi-modal testing and Figure 10 for text-only testing.

For multi-modal and text-only testing, the information on mobile phones is given by screenshots and compressed XML respectively. The models are supposed to generate detailed description of the action and its corresponding element and parameters in round 1, and the expected function-call format in round 2.

Table 4: List of Android Eval apps used along with corresponding example task, sub-goals, and the number of tasks. 

<table><tr><td>APP</td><td>Example Task</td><td>Sub-Goals</td><td># tasks</td></tr><tr><td>Bluecoins</td><td>Record an income of 8000 CNY in the books, and mark it as &quot;salary&quot;.</td><td>· type: income· cash: 8000 CNY· note: salary</td><td>15</td></tr><tr><td>Calendar</td><td>Edit the event with title &quot;work&quot;, change the time to be 7:00 PM.</td><td>· title: work· state: editing· date: today· time: 7 PM</td><td>14</td></tr><tr><td>Cantook</td><td>Mark Hamlet as read.</td><td>· book: Hamlet· state: 100% read</td><td>12</td></tr><tr><td>Clock</td><td>I need set an 10:30PM clock every weekend, and label it as &quot;Watch Football Games&quot;.</td><td>· time: 10:30PM· frequency: every weekend· label: Watch Football Games</td><td>27</td></tr><tr><td>Contacts</td><td>Add a contacts whose name is Xu, set the working phone number to be 12345678, and mobile phone number to be 87654321.</td><td>· name: Xu· working phone number: 12345678· mobile phone number: 87654321</td><td>15</td></tr><tr><td>Maps.me</td><td>Check the driving distance and time between Bus stop of 2700 Coast Avenue and Bus Stop Route 51.</td><td>· driving distance: 7.0km· driving time: 8 min</td><td>15</td></tr><tr><td>PiMusic</td><td>Sort Pink Floyd&#x27;s songs by duration time in descending order.</td><td>· page: ARTISTS· artist: Pink Floyd· order: descending by duration</td><td>12</td></tr><tr><td>Setting</td><td>Show battery percentage in status bar.</td><td>· battery percentage: displayed</td><td>23</td></tr><tr><td>Zoom</td><td>I need to join meeting 1234567890 without audio and video.</td><td>· meeting ID: 1234567890· audio: off· video: off</td><td>5</td></tr></table>

<table><tr><td colspan="2"># Setup
You are a professional android operation agent assistant that can fulfill user&#x27;s high-level instructions. Given the XML information of the android screenshot at each step, you plan operations in python-style pseudo code using provided functions, or customize functions (if necessary) and then provide their implementations.
# More details about the code
Your code should be readable, simple, and only &quot;ONE-LINE-OF-CODE&quot; at a time. You are not allowed to use &#x27;while statement and it else&#x27; control. Predefined functions are as follows:</td><td></td></tr><tr><td>System Message</td><td>def dojection, element=None, &quot;kwargs): 
... 
Perform a single operation on an Android mobile device. 
Argo:
action (str): Specifies the action to be performed. Valid options are:
&quot;Tap&quot;, &quot;Type&quot;, &quot;Swipe&quot;, &quot;Long Press&quot;, &quot;None&quot;, &quot;Black&quot;, &quot;Enter&quot;, &quot;Wait&quot;. 
element (str, optional): Define the screen area or starting point for the action.
- For &quot;Tap&quot; and &quot;Long Press&quot;, provide coordinates [x1, y1, x2, y2]
to define a rectangle from top-left (x1, y1 to bottom-right (x2, y2)
- For &quot;Swipe&quot;, provide coordinates either as [x1, y1, x2, y2] for a defined path or [x, y] for a starting point. If omitted, defaults to the screen center. 
Keyword Argo:
bed (str, optional): The text to type. Required for the &quot;Type&quot; action.
direction (str, optional): The direction to swipe. Valid directions are &quot;up&quot;, &quot;down&quot;, &quot;left&quot;, &quot;right&quot;.
Required if action is &quot;Swipe&quot;.
dist (str, optional): The distance of the swipe, with options &quot;long&quot;, &quot;medium&quot;, &quot;short&quot;.
Defaults to &quot;medium&quot;. Required if action is &quot;Swipe&quot; and direction is specified. 
Returns:
None. The device state or the foreground application state will be updated after executing the action. 
--- 
def finish(message=None): 
--- 
Terminates the program. Optionally prints a provided message to the standard output before exiting.
Argo:
message (str, optional): A message to print before exiting. Defaults to None.
Returns:
None 
--- 
# A toy example 
# Task Instruction:
Set an alarm for 9:00 a.m. on Monday 
-- XML .. 
#Analysic: The user wants to set a recurring alarm for 9:00 a.m. on weekdays. First I should open the Clock app, which should contain the alarm clock setting yami. But I can&#x27;t find it in current screen, I should swipe up to find the Clock app.
* Operation: 
... 
dojection=&quot;Swipe&quot;, element=(860, 2016, 760, 2276), direction=&quot;up&quot;, dist=&quot;long&quot;) 
... 
#ML .. 
#Round 5
* Analysis: The user wants to set a recurring alarm for 9:00 a.m. on weekdays. First I should open the Clock app, which should contain the alarm clock setting yami. But I can&#x27;t find it in current screen, I should swipe up to find the Clock app.
* Operation: 
... 
dojection=&quot;Sweep&quot;, element=(863, 390, 1021, 672)# 
* Operation: 
... 
dojection=&quot;Tap&quot;, element=(863, 390, 1021, 672) 
#Round 2
* Analysis: After opening the Clock app, I need to find where to add an alarm. Therefore, I should tap the Alarm tab #66,115[228,192)# 
* Operation: 
... 
dojection=&quot;Tap&quot;, element=(66, 115, 228, 192) 
... 
#ML .. 
#Round 3
* Analysis: In the alarm page, I should tap the &quot;Add Alarm&quot; button to add a new alarm. #408,1626[672,1890)# 
* Operation: 
... 
dojection=&quot;Tap&quot;, element=(408, 1626, 672, 1890)</td><td>&lt; user &gt; 
** XML ... 
#Assistant&gt;
## Round 4
* Analysis: I can set the alarm now. Firstly, I should set the alarm to 9 o&#x27;clock. #000,1170[332,1302]#
* Operation:
dojection=&quot;Tap&quot;, element=(200, 1170, 332, 1302) 
... 
#XML .. 
## Round 5
* Analysis: Then I need to change the clock period toggle to &quot;AM&quot;. #782,543[925,807]#
* Operation:
dojection=&quot;Tap&quot;, element=(782, 543, 925, 807) 
... 
#XML .. 
## Round 6
* Analysis: The alarm is now set, tap &quot;OK&quot; to confirm. #793,1660[969,1792]#
* Operation:
... 
dojection=&quot;Tap&quot;, element=(793, 1660, 969, 1792) 
... 
#XML .. 
#Round 7
* Analysis: Now this alarm will only go off tomorrow. I need to change it to go off once every Monday. #009,694[341,826]#
* Operation:
dojection=&quot;Tap&quot;, element=(209, 694, 341, 826) 
... 
#XML .. 
#Round 8
* Analysis: The alarm has been set to go off once every Monday, which means the task is finished.
* Operation:
finish messages= &quot;The alarm has been set to go off at 9:00 a.m. once every Monday&quot;) 
REMEMBER:
- Only &quot;ONE-LINE-OF-CODE&quot; at a time.
- Don&#x27;t generate an operation element that you do not see in the screenshot.
- You are acting in a real world, try your best not to reject user&#x27;s demand. Solve all the problem you encounter.
- On a dropdown element (Calendar, Nationality, Language, etc.), first try directly typing in the option you want.
- To accomplish the task, try switching to as many different pages as you can, and don&#x27;t stay on the same page too often, based on historical conversation information.
- To complete the task, explore the app fully i.e., tap more on different elements of the app
- Please do not translate proper nouns into English.</td></tr><tr><td colspan="2">Task Instruction (task)</td><td></td></tr><tr><td colspan="2">Omitad XML</td><td>User
Message</td></tr><tr><td colspan="2">Response History</td><td>Model
Message</td></tr><tr><td colspan="2">Omitad XML</td><td>User
Message</td></tr><tr><td colspan="2">Response History</td><td>Model
Message</td></tr><tr><td colspan="2">●
●
●
●</td><td>User
Message</td></tr><tr><td colspan="2">Omitad XML</td><td>User
Message</td></tr><tr><td colspan="2">Response History</td><td>Model
Message</td></tr><tr><td colspan="2">Compressed XML of current screen:
[layout_info]</td><td>User
Message</td></tr></table>

Figure 7: Prompts of XML Mode for Text-only Testing

# C Details of Android Instruction Dataset

# C.1 Details of Human Annotation

In the process of constructing our data, we utilize crowdsourced annotations. To ensure that the privacy information of the annotators is not disclosed, we adopt the following measures:

1. Before the annotation begins, we explicitly inform the annotators that the annotated data will be used to fine-tune models, and part of the data will be open-sourced. Annotators who disagree may opt out of the annotation process.   
2. During the annotation process, all annotated data are first stored locally by the annotators. If an annotator believes that specific data involves privacy disclosure, they may choose not to use it or skip the task.   
3. After the annotation is completed, we mask and replace sensitive information such as usernames and chat logs before using the data for training. Additionally, such data will not be open-sourced.

All annotators sign formal contracts and are compensated according to reasonable standards.

# C.2 Instructions Given To Annotators

We provide the instructions given to the annotators below. Note that our targets are expanded by hand-written instructions or academic datasets with available licenses.

# Task Overview

For each labeling task, a target task will be given, such as: Navigate to XXX using Amap (Gaode Map).

The annotator must complete the task using their phone and follow the labeling process described below to ensure it is accurately executed and recorded.

To perform this annotation task, you must install ADB (Android Device Bridge) on your computer to control the phone and install the corresponding APK. Since the task involves collecting low-level information, we will require the phone to enable multiple permissions. Still, we guarantee that the information will not be transmitted in real-time during collection. The transmitted information includes the operation details, screenshots before and after each operation, and the corresponding XML files (only containing information from the current page). You can review and decide whether to keep the annotation data. If the annotation process involves screenshots or other information that you do

<table><tr><td>System Message</td><td>You are an agent that is trained to complete certain tasks on a smartphone. You will be given a screenshot of a smartphone app. The interactive UI elements on the screenshot are labeled with numeric tags starting from 1.
You can call the following functions to interact with those labeled elements to control the smartphone:
1. tap(index: int)
Taps the UI element labeled with the given number.
Example: tap(5)
2. text(input_str: str)
Inserts the given text into an input field.
Example: text(&quot;Hello, world!&quot;) 
Since we use ADB keyboard, if ADB keyboard ON is displayed on the bottom of the screen, you can use this function.
If you think that the keyboard is displayed after your previous operation, you can try to use this function to input text.
3. long press(index: int)
Long presses the UI element labeled with the given number.
Example: long press(5)
4. swipe(index: int, direction: str, dist: str)
Swipes the UI element in the specified direction and distance. &quot;direction&quot; is a string that represents one of the four directions: up, down, left, right. &quot;dist&quot; determines the distance of the swipe and can be one of the three options: short, medium, long.
Example: swipe(21, &quot;up&quot;, &quot;medium&quot;)
5. back()
Simulates a back button press on the smartphone.
6. home()
Simulates a home button press on the smartphone.
7. wait(interval: int)
Pauses the execution for the given number of seconds. Default is 5 second.
8. finish(message: str)
Ends the task and provides the final output. You can return the final output of the task as a string.
Example: finish(&quot;Task completed&quot;)
Now, given the following labeled screenshot, you need to think and call the function needed to proceed with the task.
Your output should include only action part in the given format:
Action: &lt;The function call with the correct parameters to proceed with the task. If you believe the task is completed or there is nothing to be done, you should use finish function. You cannot output anything else except a function call in this field.&gt;
Whenever you think the task is finished, you should use finish function to avoid extra operations.
If you found yourself in a loop or the task is not proceeding as expected, you might consider changing your operation and try other methods.
If you operate same action 5 times, the program will automatically stop.
If tap operation is not working, you can try long press operation.
You can only take one action at a time, so please directly call the function.
Task Instruction: (task)</td></tr><tr><td>User Message</td><td>Omitted Screenshot</td></tr><tr><td>Model Message</td><td>Response History</td></tr><tr><td>User Message</td><td>Omitted Screenshot</td></tr><tr><td>Model Message</td><td>Response History</td></tr><tr><td>User Message</td><td>Omitted Screenshot</td></tr><tr><td>Model Message</td><td>Response History</td></tr></table>

Figure 8: Prompts of SoM Mode for Multi-modal Testing

<table><tr><td rowspan="5"></td><td>System Message</td><td colspan="2">You are assisting humans doing smartphone navigation tasks step by step. At each stage, you can see the smartphone by a screenshot and know the previous actions before the current step decided by yourself that have been executed for this task through recorded history. You need to decide on the first following action to take.Here are the descriptions of all allowed actions: &quot;Tap&quot;, &quot;Type&quot;, &quot;Swipe&quot;, &quot;Long Press&quot;, &quot;Home&quot;, &quot;Back&quot;, &quot;Enter&quot;, &quot;Wait&quot;.</td></tr><tr><td>User Message</td><td>You are asked to complete the following task:{task}Previous Actions:{previous_actions}The screenshot below shows the smartphone you see. Think step by step before outlining the next action step at the current stage. Clearly outline which element in the smartphone users will operate with as the first next target element, its detailed location, and the corresponding operation.To be successful, it is important to follow the following rules:1. You should only issue a valid action given the current observation.2. You should only issue one action at a time.3. Terminate when you deem the task complete.</td><td><img src="images/c929a44aa5335300de68590036239f7c82384fa0d8e1cfe9ed9acce63aa9f515.jpg"/><img src="images/f2dd891de166d97819ee8663c6d0d4664fa1b435928c299dfeb1012dd17144c9.jpg"/></td></tr><tr><td rowspan="2">Round 1 Model Generation</td><td colspan="2">Action Generation</td></tr><tr><td colspan="2">(Reiteration)First, reiterate your next target element, its detailed location, and the corresponding operation.(Final Answer)Below is a multi-choice question, where the choices are elements in the smartphone. From the screenshot, find out where and what each one is on the smartphone, taking into account both their text content and path details. Then, determine whether one matches your target element if your action involves an element. Choose the best matching one.{option_prompt}Conclude your answer using the format below. Ensure your answer is strictly adhering to the format provided below.Predefined functions are as follow:...def do(action, element=None, **kwargs):***Perform a single operation on an Android mobile device.Args:action (str): Specifies the action to be performed. Valid options are:&quot;Tap&quot;, &quot;Type&quot;, &quot;Swipe&quot;, &quot;Long Press&quot;, &quot;Home&quot;, &quot;Back&quot;, &quot;Enter&quot;, &quot;Wait&quot;.element (list, optional): Defines the screen area or starting point for the action.- For &quot;Tap&quot; and &quot;Long Press&quot;, provide coordinates [x1, y1, x2, y2]to define a rectangle from top-left (x1, y1) to bottom-right (x2, y2).- For &quot;Swipe&quot;, provide coordinates either as [x1, y1, x2, y2] for a defined pathor [x, y] for a starting point. If omitted, defaults to the screen center.</td></tr><tr><td>User Message</td><td colspan="2">Keyword Args:text (str, optional): The text to type. Required for the &quot;Type&quot; action.direction (str, optional): The direction to swipe. Valid directions are &quot;up&quot;, &quot;down&quot;, &quot;left&quot;, &quot;right&quot;.Required if action is &quot;Swipe&quot;:dist (str, optional): The distance of the swipe, with options &quot;long&quot;, &quot;medium&quot;, &quot;short&quot;.Defaults to &quot;medium&quot;. Required if action is &quot;Swipe&quot; and direction is specified.Returns:None. The device state or the foreground application state will be updated after executing the action.***...def finish(message=None):***Terminates the program. Optionally prints a provided message to the standard output before exiting.Args:message (str, optional): A message to print before exiting. Defaults to None.Returns:None......Your code should be readable, simple, and only **ONE-LINE-OF-CODE** at a time. You are not allowed to use &#x27;while&#x27; statement and &#x27;if-else&#x27; control. Please do not leave any explanation in your answers of the final standardized format part, and this final part should be clear and certain.Example if you want to swipe up from an element located at [680,2016][760,2276] with a long distance:do(action=&quot;Swipe&quot;, element=[680, 2016, 760, 2276], direction=&quot;up&quot;, dist=&quot;long&quot;)Example if you deem the task complete and want to finish with a message:finish(message=&quot;The alarm on 9:00 AM weekday has been set&quot;)</td></tr><tr><td colspan="2">Round 2 Model Generation</td><td colspan="2">Action Grounding</td></tr></table>

Figure 9: SeeAct Prompts for Multi-modal Testing

<table><tr><td rowspan="2"></td><td>System Message</td><td>You are assisting humans doing smartphone navigation tasks step by step. At each stage, you can see the smartphone by compressed layout information and know the previous actions before the current step decided by yourself that have been executed for this task through recorded history. You need to decide on the first following action to take.Here are the descriptions of all allowed actions: &quot;Tap&quot;, &quot;Type&quot;, &quot;Swipe&quot;, &quot;Long Press&quot;, &quot;Home&quot;, &quot;Back&quot;, &quot;Enter&quot;, &quot;Wait&quot;.</td></tr><tr><td>User Message</td><td>You are asked to complete the following task: {task}Previous Actions:{previous_actions}The compressed layout information below shows the smartphone you see.{layout_info}Think step by step before outlining the next action step at the current stage. Clearly outline which element in the smartphone users will operate with as the first next target element, its detailed location, and the corresponding operation.To be successful, it is important to follow the following rules:1. You should only issue a valid action given the current observation.2. You should only issue one action at a time.3. Terminate when you deem the task complete.</td></tr><tr><td rowspan="3">Round 1</td><td rowspan="2">Model Generation</td><td>Action Generation</td></tr><tr><td>(Reiteration)First, reiterate your next target element, its detailed location, and the corresponding operation.(Final Answer)Below is a multi-choice question, where the choices are elements in the smartphone. From compressed layout information, find out where and what each one is on the smartphone, taking into account both their text content and path details. Then, determine whether one matches your target element if your action involves an element. Choose the best matching one.{option_prompt}Conclude your answer using the format below. Ensure your answer is strictly adhering to the format provided below.Predefined functions are as follow:...def do(action, element=None, **kwargs):***Perform a single operation on an Android mobile device.Args:action (str): Specifies the action to be performed. Valid options are:&quot;Tap&quot;, &quot;Type&quot;, &quot;Swipe&quot;, &quot;Long Press&quot;, &quot;Home&quot;, &quot;Back&quot;, &quot;Enter&quot;, &quot;Wait&quot;.element (list, optional): Defines the screen area or starting point for the action.- For &quot;Tap&quot; and &quot;Long Press&quot;, provide coordinates [x1, y1, x2, y2]to define a rectangle from top-left (x1, y1) to bottom-right (x2, y2).- For &quot;Swipe&quot;, provide coordinates either as [x1, y1, x2, y2] for a defined pathor [x, y] for a starting point. If omitted, defaults to the screen center.</td></tr><tr><td>User Message</td><td>Keyword Args:text (str, optional): The text to type. Required for the &quot;Type&quot; action.direction (str, optional): The direction to swipe. Valid directions are &quot;up&quot;, &quot;down&quot;, &quot;left&quot;, &quot;right&quot;.Required if action is &quot;Swipe&quot;.dist (str, optional): The distance of the swipe, with options &quot;long&quot;, &quot;medium&quot;, &quot;short&quot;.Defaults to &quot;medium&quot;. Required if action is &quot;Swipe&quot; and direction is specified.Returns:None. The device state or the foreground application state will be updated after executing the action.***...def finish(message=None):***Terminates the program. Optionally prints a provided message to the standard output before exiting.Args:message (str, optional): A message to print before exiting. Defaults to None.Returns:None****...Your code should be readable, simple, and only &quot;ONE-LINE-OF-CODE&quot; at a time. You are not allowed to use &#x27;while&#x27; statement and &#x27;if-else&#x27; control. Please do not leave any explanation in your answers of the final standardized format part, and this final part should be clear and certain.Example if you want to swipe up from an element located at [680,2016][760,2276] with a long distance:do(action=&quot;Swipe&quot;, element=[680, 2016, 760, 2276], direction=&quot;up&quot;, dist=&quot;long&quot;)Example if you deem the task complete and want to finish with a message:finish(message=&quot;The alarm on 9:00 AM weekday has been set&quot;)</td></tr><tr><td>Round 2</td><td>Model Generation</td><td>Action Grounding</td></tr></table>

Figure 10: SeeAct Prompts for Text-only Testing

not want to be used for training, you can:

1. Skip the screenshot or specify that parts of the screenshot be hidden.   
2. Skip the entire target task.   
3. Skip all tasks involving the currently annotated app.

Your data will not be used for purposes other than training the model.

After completing the annotation, you must upload all the tasks you were responsible for in one go. We have designed a plugin to store all the content in a unified folder.

A complete annotation consists of multiple operations called a sequence (trace). Each single-step operation is recorded once, and the definition of a single-step operation is detailed in the annotation documentation.

Please follow the steps below for plugin usage to install the annotation plugin.

# Plugin Usage Instructions

Installing ADB and Connecting Phone to Computer

For your Android phone, you need to perform the following settings:

1. Connect the phone to the computer via a USB cable.   
2. Ensure that the Developer Options and USB Debugging Mode are enabled on the Android phone:

• Go to Settings - Developer Options - Android Debugging. Check the box for Allow USB debugging. If unavailable, go to Settings - System Updates - Developer Options - USB Debugging.   
• If you can’t find the developer options, go to Settings - About Phone and tap the Build Number seven times.   
• If these methods don’t work, search for how to enable developer options and USB debugging specific to your phone model.   
• If you still encounter issues, seek help in the group chat.

3. Reconnect the phone to the computer, and on the phone, click Allow file transfer/USB debugging/higher permissions. Also, allow the connection on the computer (if prompted).

4. After entering Developer Mode, turn off the following animations under Developer Options to increase the success rate of retrieving XML information via ADB commands:

• Window Animation Scale.   
• Transition Animation Scale.   
• Animator Duration Scale.

Follow the steps above until the following result is displayed using the command adb devices:

adb devices

List of devices attached

1a0d5d59 device

The number before device is randomly generated. You should see only one device. If there is more than one, try disconnecting other devices or closing virtual machines.

Installing ADB Keyboard

Download the ADB Keyboard APK.

Run: adb install <APK full path>

Enable permissions on the phone and agree to the installation.

Once the installation is complete, set ADB Keyboard as the default input method in the phone settings. You can try the following two lines of code:

ime enable com.android.adbkeyboard/.AdbIME ime set com.android.adbkeyboard/.AdbIME

If successful, when you open any text box, you’ll see the message ADB Keyboard ON at the bottom of the screen. If unsuccessful, manually change the input method in the settings.

Running Test Script

1. Open the command line, run adb devices, and ensure correct output.   
2. Run the following commands in adb shell:

input keyevent KEYCODE\_BACK input keyevent KEYCODE\_HOME input keyevent KEYCODE\_ENTER

If there’s no error or response, it’s fine. If you see Command execution failed, ensure you’re using the correct method sequence, not Press xxx commands like adb shell input keyevent KEYCODE\_A.

3. Open any text input field and run the following commands in adb shell:

input keyevent KEYCODE\_A

The setup succeeds if the letter "a" appears on the screen.

# Annotation Plugin Usage Instructions

You can perform the following operations on the phone. After completing any one of these operations, do not proceed until the command line shows Operation completed. If the phone has not responded yet (such as loading a new page), wait until the page is fully loaded before clicking the next Begin.

1. Click or Swipe: Perform this directly on the phone. Click slowly, holding for 0.2 to 0.5 seconds.   
2. Text Input: If the ADB Keyboard was successfully installed, you can input text. Before entering text, click on the text box in the previous step and ensure that the ADB Keyboard ON symbol appears at the bottom of the screen. Click the Type button on the GUI interface, enter the desired text in the computer’s input box (Chinese/English), then click OK. You will observe the input on the phone, and the command line will display Simulating typing xxx.   
3. Press xxx: Three preset buttons are defined: Press Home (Home key), Press Back (Back key), and Press Enter (keyboard Enter key). The command line will show Simulating press xxx.   
4. Finish Task: If you believe the task is complete, click the Finish button on the GUI. If the task requires an answer, fill in the response in the popup text box. If not, click OK.

After finishing a task, you can close the command line and GUI windows. If there are no issues with the annotation, you can return to Step 2 to start the next annotation. Otherwise, follow these steps:

1. The command line will output the Save Path, which contains all saved information for the annotation. You may delete the folder if you believe an error occurred or sensitive information was recorded.

2. Each task has a prefix consisting of the first 32 characters of the task name. Ensure that the final submission includes one and only one instance of each non-skipped task.   
3. If certain operations were recorded incorrectly without affecting the phone’s state, you may delete those steps. The step sequence is stored in Save Path/traces/trace.jsonl. Record the steps you need to delete.   
4. If a screen contains sensitive information that can be removed while still being used for training, record the steps and describe the sensitive information in detail.

# Summary of Key Points

1. Always use adb devices before starting the annotation to ensure a successful connection.   
2. Reopen the app\_for\_xxx/dist/label(.exe) for each annotation instruction.   
3. The storage path must not contain Chinese characters.   
4. Click Begin before each operation and wait for the message Begin your operation... to appear before proceeding. If you proceed without waiting, the operation will be invalid. If the state cannot be recovered, you must restart the task. Make sure to click Begin before finishing as well.   
5. After each operation is completed, wait until the corresponding success message appears in the command line and you see the output Operation completed before clicking Begin for the next action. Failure to follow these two key rules may result in invalid data. It’s better to proceed slowly and carefully than rush and make mistakes.

# D Additional Results

# D.1 Detail results across different APPs

Table 5 shows the number of tasks correctly completed by various models across different apps, without employing the ReAct and SeeAct frameworks. This table shows that GPT-4o and GPT-4-1106-Preview perform relatively well, completing 78 and 79 tasks respectively. In the XML mode, GPT-4-1106-Preview stands out as the top performer with 43 tasks completed. Comparatively, in the SoM mode, GPT-4o excels, completing a significantly higher number of tasks than the other models. Most models exhibit high success rates in tasks like "Contacts" and "Setting". Overall, GPT-4o and GPT-4-1106-Preview outperform the other models significantly in both XML and SoM modes, while Gemini-1.5-Pro shows a reasonable number of task completions across various apps.

Table 5: The number of tasks completed by all models across all apps in different modes. 

<table><tr><td>Mode</td><td>Model</td><td>Bluecoins 15</td><td>Calendar 14</td><td>Cantook 12</td><td>Clock 27</td><td>Contacts 15</td><td>Maps.me 15</td><td>PiMusic 12</td><td>Setting 23</td><td>Zoom 5</td><td>Total 138</td></tr><tr><td rowspan="11">XML</td><td>GPT-4o</td><td>1</td><td>0</td><td>3</td><td>8</td><td>5</td><td>5</td><td>2</td><td>10</td><td>1</td><td>35</td></tr><tr><td>GPT-4-1106-Preview</td><td>1</td><td>4</td><td>6</td><td>4</td><td>6</td><td>6</td><td>4</td><td>9</td><td>3</td><td>43</td></tr><tr><td>Gemini-1.5-Pro</td><td>1</td><td>1</td><td>3</td><td>6</td><td>3</td><td>4</td><td>3</td><td>4</td><td>1</td><td>26</td></tr><tr><td>Gemini-1.0</td><td>0</td><td>1</td><td>1</td><td>4</td><td>2</td><td>0</td><td>1</td><td>2</td><td>1</td><td>12</td></tr><tr><td>GLM4-PLUS</td><td>2</td><td>0</td><td>4</td><td>9</td><td>6</td><td>3</td><td>2</td><td>10</td><td>2</td><td>38</td></tr><tr><td>LLaMA3.1-8B-Instruct</td><td>0</td><td>0</td><td>0</td><td>2</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>3</td></tr><tr><td>Qwen2.5-7B-Instruct</td><td>0</td><td>0</td><td>2</td><td>1</td><td>1</td><td>0</td><td>0</td><td>2</td><td>0</td><td>6</td></tr><tr><td>GLM4-9B-Chat</td><td>0</td><td>1</td><td>0</td><td>2</td><td>1</td><td>1</td><td>0</td><td>3</td><td>2</td><td>10</td></tr><tr><td>LLaMA3.1-8B-ft</td><td>3</td><td>1</td><td>6</td><td>7</td><td>6</td><td>5</td><td>0</td><td>4</td><td>1</td><td>33</td></tr><tr><td>Qwen2.5-7B-ft</td><td>1</td><td>1</td><td>3</td><td>4</td><td>7</td><td>4</td><td>1</td><td>6</td><td>0</td><td>27</td></tr><tr><td>GLM4-9B-ft</td><td>0</td><td>1</td><td>5</td><td>7</td><td>5</td><td>2</td><td>0</td><td>8</td><td>1</td><td>29</td></tr><tr><td rowspan="12">SoM</td><td>GPT-4o</td><td>1</td><td>1</td><td>5</td><td>7</td><td>8</td><td>2</td><td>2</td><td>13</td><td>4</td><td>43</td></tr><tr><td>GPT-4-Vision-Preview</td><td>1</td><td>1</td><td>5</td><td>8</td><td>6</td><td>2</td><td>2</td><td>8</td><td>3</td><td>36</td></tr><tr><td>Gemini-1.5-Pro</td><td>0</td><td>0</td><td>5</td><td>2</td><td>5</td><td>0</td><td>1</td><td>7</td><td>3</td><td>23</td></tr><tr><td>Gemini-1.0</td><td>0</td><td>0</td><td>2</td><td>3</td><td>3</td><td>0</td><td>1</td><td>5</td><td>1</td><td>15</td></tr><tr><td>Claude-3.5-Sonnet</td><td>4</td><td>2</td><td>4</td><td>9</td><td>7</td><td>0</td><td>3</td><td>10</td><td>1</td><td>40</td></tr><tr><td>Claude-3-Opus</td><td>1</td><td>0</td><td>1</td><td>2</td><td>4</td><td>0</td><td>3</td><td>7</td><td>0</td><td>18</td></tr><tr><td>CogVLM2</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr><tr><td>LLaMA3.2-11B-Vision-Instruct</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>2</td></tr><tr><td>Qwen2-VL-7B-Instruct</td><td>0</td><td>0</td><td>0</td><td>2</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>5</td></tr><tr><td>CogVLM2-ft</td><td>0</td><td>0</td><td>2</td><td>3</td><td>4</td><td>1</td><td>1</td><td>4</td><td>1</td><td>16</td></tr><tr><td>LLaMA3.2-11B-Vision-ft</td><td>1</td><td>1</td><td>1</td><td>3</td><td>0</td><td>6</td><td>0</td><td>2</td><td>0</td><td>14</td></tr><tr><td>Qwen2-VL-7B-Instruct-ft</td><td>1</td><td>0</td><td>1</td><td>4</td><td>5</td><td>3</td><td>2</td><td>7</td><td>2</td><td>25</td></tr></table>

Table 6: The improvement in model performance after employing the ReAct and SeeAct frameworks, is reflected in the increased number of successfully completed tasks across various apps. 

<table><tr><td>Mode</td><td>Model</td><td>Bluecoins 15</td><td>Calender 14</td><td>Cantook 12</td><td>Clock 27</td><td>Contacts 15</td><td>Maps.me 15</td><td>PiMusic 12</td><td>Settings 23</td><td>Zoom 5</td><td>Total 138</td></tr><tr><td rowspan="2">XML</td><td>GPT-4o</td><td>1</td><td>0</td><td>3</td><td>8</td><td>5</td><td>5</td><td>2</td><td>10</td><td>1</td><td>35</td></tr><tr><td>Gemini-1.5-Pro</td><td>1</td><td>1</td><td>3</td><td>6</td><td>3</td><td>4</td><td>3</td><td>4</td><td>1</td><td>26</td></tr><tr><td rowspan="2">XML+ReAct</td><td>GPT-4o</td><td>2</td><td>0</td><td>4</td><td>12</td><td>7</td><td>6</td><td>2</td><td>11</td><td>2</td><td>46</td></tr><tr><td>Gemini-1.5-Pro</td><td>4</td><td>0</td><td>4</td><td>6</td><td>6</td><td>6</td><td>3</td><td>11</td><td>3</td><td>43</td></tr><tr><td rowspan="2">XML+SeeAct</td><td>GPT-4o</td><td>1</td><td>2</td><td>4</td><td>8</td><td>5</td><td>3</td><td>2</td><td>7</td><td>2</td><td>34</td></tr><tr><td>Gemini-1.5-Pro</td><td>1</td><td>0</td><td>6</td><td>6</td><td>5</td><td>0</td><td>2</td><td>8</td><td>1</td><td>29</td></tr><tr><td rowspan="2">SoM</td><td>GPT-4o</td><td>1</td><td>1</td><td>5</td><td>7</td><td>8</td><td>2</td><td>2</td><td>13</td><td>4</td><td>43</td></tr><tr><td>Gemini-1.5-Pro</td><td>0</td><td>0</td><td>5</td><td>2</td><td>5</td><td>0</td><td>1</td><td>7</td><td>3</td><td>23</td></tr><tr><td rowspan="2">SoM+ReAct</td><td>GPT-4o</td><td>3</td><td>1</td><td>5</td><td>7</td><td>7</td><td>3</td><td>0</td><td>15</td><td>3</td><td>44</td></tr><tr><td>Gemini-1.5-Pro</td><td>1</td><td>1</td><td>3</td><td>2</td><td>4</td><td>1</td><td>2</td><td>7</td><td>1</td><td>22</td></tr><tr><td rowspan="2">SoM+SeeAct</td><td>GPT-4o</td><td>6</td><td>1</td><td>4</td><td>11</td><td>6</td><td>0</td><td>2</td><td>9</td><td>3</td><td>42</td></tr><tr><td>Gemini-1.5-Pro</td><td>1</td><td>0</td><td>6</td><td>6</td><td>5</td><td>0</td><td>2</td><td>8</td><td>1</td><td>29</td></tr></table>

Table 6 shows the performance improvements observed after implementing the ReAct and See-Act frameworks on different models across various apps. Notably, GPT-4o shows significant enhancement, with the number of completed tasks increasing from 35 to 46 in XML+ReAct mode and from 43 to 44 in SoM+ReAct mode. Gemini-1.5-Pro also benefits, increasing from 26 to 43 tasks. The improvements are evident in specific apps like "Bluecoins", and are especially notable in high-complexity, multi-step tasks. GPT-4o leads in performance across all frameworks, showing how ReAct and SeeAct improve the model.

# D.2 Detail results across different multi-modal training mode

We provide a comparison of different multimodal training modes in Table 7. Under the same training data and base model settings, BBOX mode removes specified sets-of-masks from the screen. It is worth mentioning that datasets like AITW only provide click positions rather than bounding boxes (BBOX), and they do not offer a way to reconstruct the clickbox from XML. Therefore, theoretically, data from AITW and similar datasets are more challenging to learn from.

Table 7: Different multi-modal modes of instruction tuning. We use the same set of training data but only add a set-of-mask index on SoM mode. Note that AITW dataset even could not provide accurate bbox, but only point. We use CogVLM2 as base model. 

<table><tr><td>Operation Mode</td><td>SR</td><td>Sub-SR</td><td>RRR</td><td>ROR</td></tr><tr><td>BBOX</td><td>5.79</td><td>6.03</td><td>47.95</td><td>55.05</td></tr><tr><td>SoM</td><td>11.59</td><td>16.06</td><td>57.37</td><td>85.58</td></tr></table>

Table 8: The impact of the ReAct and SeeAct frameworks. Notably, model performance is significantly improved in XML+ReAct mode. 

<table><tr><td>Mode</td><td>Model</td><td>SR</td><td>Sub-SR</td><td>RRR</td><td>ROR</td></tr><tr><td rowspan="2">XML</td><td>GPT-4o</td><td>25.36</td><td>30.56</td><td>107.45</td><td>86.56</td></tr><tr><td>Gemini-1.5-Pro</td><td>18.84</td><td>22.40</td><td>57.72</td><td>83.99</td></tr><tr><td rowspan="2">XML+ReAct</td><td>GPT-4o</td><td>33.33</td><td>38.22</td><td>97.93</td><td>90.74</td></tr><tr><td>Gemini-1.5-Pro</td><td>31.16</td><td>34.54</td><td>92.08</td><td>90.31</td></tr><tr><td rowspan="2">XML+SeeAct</td><td>GPT-4o</td><td>24.64</td><td>27.31</td><td>93.78</td><td>79.62</td></tr><tr><td>Gemini-1.5-Pro</td><td>21.01</td><td>25.53</td><td>75.97</td><td>89.06</td></tr><tr><td rowspan="2">SoM</td><td>GPT-4o</td><td>31.16</td><td>35.02</td><td>87.32</td><td>85.36</td></tr><tr><td>Gemini-1.5-Pro</td><td>16.67</td><td>18.48</td><td>105.95</td><td>91.52</td></tr><tr><td rowspan="2">SoM+ReAct</td><td>GPT-4o</td><td>31.88</td><td>39.19</td><td>104.69</td><td>89.80</td></tr><tr><td>Gemini-1.5-Pro</td><td>15.94</td><td>21.38</td><td>109.81</td><td>84.16</td></tr><tr><td rowspan="2">SoM+SeeAct</td><td>GPT-4o</td><td>30.43</td><td>36.24</td><td>97.45</td><td>88.56</td></tr><tr><td>Gemini-1.5-Pro</td><td>21.01</td><td>25.53</td><td>75.97</td><td>89.06</td></tr></table>

# D.3 Detail results of SeeAct and ReAct methods

We have provided detailed results on the impact of the SeeAct and ReAct frameworks on model performance in Fig 8, including all four metrics.