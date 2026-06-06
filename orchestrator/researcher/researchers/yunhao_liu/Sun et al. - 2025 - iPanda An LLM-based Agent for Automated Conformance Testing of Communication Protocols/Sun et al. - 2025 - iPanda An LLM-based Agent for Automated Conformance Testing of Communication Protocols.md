# iPanda: An LLM-based Agent for Automated Conformance Testing of Communication Protocols

Xikai Sun∗, Fan Dang†B, Shiqi Jiang‡, Jingao Xu§, Kebin Liu∗, Xin Miao∗, Zihao Yang¶, Weichen Zhang∗, Haimo Lu∗, Yawen Zheng∗, Yunhao Liu∗B

∗Tsinghua University †Beijing Jiaotong Universi ‡Microsoft Research Asia

§Carnegie Mellon University ¶Yanshan University B Corresponding Authors

Abstract—Conformance testing is essential for ensuring that protocol implementations comply with their specifications. However, traditional testing approaches involve manually creating numerous test cases and scripts, making the process labor-intensive and inefficient. Recently, Large Language Models (LLMs) have demonstrated impressive text comprehension and code generation abilities, providing promising opportunities for automation. In this paper, we propose iPanda, the first framework that leverages LLMs to automate protocol conformance testing. Given a protocol specification document and its implementation, iPanda first employs a keyword-based method to automatically generate comprehensive test cases. Then, it utilizes retrieval-augmented generation and customized CoT strategy to effectively interpret the implementation and produce executable test programs. To further enhance programs’ quality, iPanda incorporates an iterative optimization mechanism to refine generated test scripts interactively. Finally, by executing and analyzing the generated tests, iPanda systematically verifies compliance between implementations and protocol specifications. Comprehensive experiments on various protocols show that iPanda significantly outperforms pure LLM-based approaches, improving the success rate (P ass@1) of test-program generation by factors ranging from 4.675× to 10.751×.

Index Terms—Conformance Testing, LLMs, Automated Testing.

# I. INTRODUCTION

Communication protocols such as MQTT, CoAP, Web-Socket form the backbone of today’s information-driven society, playing critical roles in internet data transmission, IoT connectivity, and cloud computing services. Ensuring the stability and efficiency of protocol implementations is therefore paramount and necessitates rigorous testing procedures. Conformance testing, specifically designed to verify adherence of protocol implementations to their official standards and specifications, is one of the essential methods employed in validating communication protocols. In typical scenarios, testers might spend weeks manually writing extensive test scripts utilizing protocol implementation libraries, and individually verifying compliance with protocol requirements. For instance, a typical compliance check for the CoAP protocol involves developing hundreds of script-based tests, to verify its message grammar, stateful interactions and operational sequences, as mandated by over 200 MUST and SHOULD requirements in RFC7252. With the increasing complexity of protocols, traditional manual testing methods have become inefficient, cumbersome, and difficult to generalize. This situation underscores an urgent need for automated testing solutions that minimize human intervention while enhancing efficiency and coverage.

Concurrently, large language models (LLMs) have shown impressive capabilities in language comprehension, reasoning, and performing sophisticated tasks. Trained on extensive datasets, LLMs effectively generalize to novel tasks, parse complex inputs, and maintain context, making them ideal for automating intricate operations. For instance, in IoT fuzz testing, LLM-driven automation enhances protocol message generation, increasing vulnerability detection effectiveness and uncovering previously undetected issues [1]. Similarly, in mobile device automation, LLMs combine general reasoning with domain-specific expertise, facilitating complex tasks without extensive manual scripting [2], [3]. These examples demonstrate the transformative potential of LLMs in turning labor-intensive procedures into efficient automated solutions.

Given this context, a compelling question arises: Can we leverage the capabilities of LLMs to address the challenges inherent in conformance testing of communication protocols? Realizing this vision in practice, however, entails overcoming several key obstacles:

• Specification-to-test-case derivation. In contrast to fuzzing, conformance testing is intrinsically driven by specifications, requiring the translation of often ambiguous textual specifications into structured, executable test logic.   
Knowledge adaptation and grounding. LLMs struggle to bridge the gap between abstract rules described in test cases and the concrete APIs provided by specific implementation libraries, making it difficult to generate valid and contextaware test programs.   
• Practical executability and reliability. Beyond syntactic correctness, test programs must be semantically aligned with the target library’s API to ensure they are both executable and trustworthy in real-world testing scenarios.

Addressing these challenges is essential not only to resolve the immediate practical issues but also to establish foundational methodologies as LLM technologies continue to advance in network protocol testing.

While LLMs have achieved remarkable success in domains such as code generation and dialogue systems, they fall short in addressing the unique demands of protocol conformance testing. We bridge this gap with iPanda, an Intelligent Protocol Testing and Debugging Agent. As the first

LLM-based solution for automating communication protocol conformance testing, iPanda streamlines the entire workflow. It autonomously parses a protocol specification to generate comprehensive test cases, translates them into executable programs for a target implementation library, and then executes these tests to systematically identify compliance violations, thereby significantly reducing manual effort.

Especially, we introduce multiple mechanisms in iPanda to overcome the above challenges. To efficiently generate test cases aligned with precise testing requirements, we propose a novel keyword-based test-case generation approach grounded in the inherent characteristics of protocol specifications. It automatically locates the specific specifications that need to be tested based on keywords, and generates formatted test cases. Moreover, to ensure the adaptation of iPanda to varying protocol libraries, we introduce code-oriented retrieval-augmented generation (RAG), which is deeply coupled with the test program generation process. This mechanism iteratively queries the knowledge base at different stages of program synthesis, providing just-in-time, context-specific guidance. Additionally, to enable LLMs to handle complex test cases, we design a customized chain-of-thought (CoT) strategy that operationalizes a divide-and-conquer methodology. It guides iPanda to first decompose the complex task case into logical sub-tasks and solve them individually, before integrating these modular solutions into a complete, high-quality test program. Finally, We introduce testing platform and iterative optimization mechanism to achieve automated testing and program correction, ensuring the program’s executability and reliability.

iPanda also supports natural-language commands and demonstrates reasoning capabilities for complex state transitions, making it effective for dynamic, heterogeneous network environments where traditional methods frequently fall short. By significantly reducing the dependency on human expertise and fully automating test execution, iPanda presents a transformative advancement in protocol conformance testing.

Our contributions are as follows:

• To the best of our knowledge, we present the first automated protocol conformance testing framework integrating LLMs with domain-specific expertise, including keyword-based test case generation, customized CoT strategy, and iterative optimization mechanism for test-program refinement.   
• We design and implement iPanda, an intelligent, LLMpowered agent capable of autonomously extracting test cases from protocol specifications, invoking protocol implementation libraries, executing and debugging tests, and identifying conformance issues.   
• As an example, we using iPanda to perform conformance testing on CoAP and RSocket, and present two test case sets, i.e., CoAP-set and RSocket-set. Comprehensive experiments demonstrate that, compared to the pure LLM-based method, iPanda improves the P ass@1 of test program generation by 4.675× to 10.751×.

Upon acceptance of this paper, we will publicly release the associated source code and datasets.

# II. BACKGROUND AND MOTIVATION

# A. Conformance Testing of Protocols

Conformance testing for communication protocols is a method used to verify whether a protocol implementation complies with the requirements defined by the protocol specification. Its primary goal is to ensure that the protocol implementation behaves in a conformant manner across various scenarios and input conditions, thereby guaranteeing compatibility and interoperability between different protocol implementations. A complete protocol conformance testing process typically includes the following key steps:

• Specification analysis. Thoroughly understand and analyze the protocol’s standard documents to extract explicitly defined behaviors and requirements.   
• Test case design. Develop comprehensive test cases based on the protocol specifications.   
• Test case implementation. Write test scripts or programs using the protocol implementation under test to concretely realize the test cases.   
• Test execution. Run the test case programs in a properly configured testing environment and collect results.   
• Result analysis and evaluation. Analyze the test results to determine whether the system under test complies with the specified requirements.

# B. Uniqueness of Conformance Testing

Traditional testing, like unit testing and integration testing, is fundamentally implementation-driven. Whether verifying individual code components (unit testing) or the interactions between modules (integration testing), the design, execution, and evaluation of test cases are all rooted in the implementation’s source code and architecture. In short, it aims to ensure that the existing implementation works as expected. In contrast, specification-based conformance testing differs fundamentally in its methodology. Its goal is to verify whether an implementation strictly adheres to an external, authoritative specification (e.g., a technical standard or an official API document). Its uniqueness is reflected mainly in two aspects:

• Shift in the source of truth. In conformance testing, the source of truth shifts from the internal code to the external specification. It does not concern itself with implementation details but focuses solely on whether the behavior aligns with what is described in the specification.   
• Systematic specification-driven process. Conformance testing requires a top-down process. It begins with systematically interpreting and decomposing the specification text into verifiable requirements. Based on these extracted requirements, test cases are then generated and executed to map precisely to actual API calls.

Essentially, traditional testing verifies what the code does, whereas conformance testing verifies whether the code does what the specification requires it to do. This makes conformance testing a systematic endeavor that demands holistic understanding (inferring the functional points to be tested from the specification), careful planning (designing tests that can validate these points), and rigorous execution (generating test programs to implement these tests). It is not merely a straightforward check of code functionality. For this reason, traditional testing tools are inadequate for conformance testing.

# C. Integrating LLM and Conformance Testing

The current conformance testing process has significant limitations, primarily due to its heavy reliance on manual effort. It involves a vast number of detailed test cases that must be manually written, making the process labor-intensive and time-consuming. Additionally, implementing these test cases requires extensive test program development, further increasing the cost of development and maintenance. These limitations significantly reduce the efficiency and flexibility of conformance testing.

At present, no conformance testing tool exists that seamlessly integrates protocol documents, implementations, and test results. The exceptional text comprehension and code generation capabilities of LLMs offer new possibilities for addressing these shortcomings. By leveraging the powerful abilities of LLMs, test case design and test program development can be automated or semi-automated, substantially reducing the manual workload. Therefore, this work aims to integrate LLMs into the conformance testing process for communication protocols. We propose an LLM-based conformance testing agent framework to enhance the efficiency and effectiveness of conformance testing.

# III. DESIGN OF IPANDA

In this section, we present the design of iPanda in detail, which is specifically designed for conformance testing of communication protocol. iPanda can dynamically generate test case sets for conformance testing based on protocol specification documents. For a given protocol implementation library, it can generate test case programs, interact with the implementation in a simulated communication environment, perform testing and debugging, and analyze execution results to identify potential deficiencies in the implementation.

The overview of iPanda is shown in Fig. 1. Taking the RSocket protocol [4] as an example, suppose a user wants to verify whether its Python implementation rsocket-py [5] conforms to its specification. iPanda first extracts key functional points from the protocol document and automatically generates standardized test cases using the LLM generator, optionally applying a filter to remove anomalous cases. For each test case, guiding by customized CoT strategy, iPanda generates executable test program using the target implementation library. To generate high-quality program, it retrieves relevant context from the implementation library. To ensure executability, the generated program undergoes validation; if issues are detected, iPanda initiates iterative refinement using historical context and error information, dynamically adjusting prompts to debug the program. Once the generation yields executable program or reaches a retry limit, iPanda compiles a final debugging report and evaluates test outcomes, determining compliance with the protocol’s conformance requirements.

![](images/c445950883578bbb727cf15da218bf5720411204a44afbc30be4fb733cdb3fb5.jpg)



Fig. 1: The overview of iPanda.

To address the challenges mentioned in Sec. I and enhance iPanda’s effectiveness, we have designed several optimization methods. The following sub-sections will provide detailed descriptions of these methods.

# A. Keyword-based Test Case Generation

In conformance testing, the generation of test cases has traditionally relied heavily on manual effort. For example, in the FIDO2 Conformance Test Tool for the FIDO protocol, developers manually extract as many test requirements as possible from the specification documents and then write corresponding test cases to integrate into the tool [6]. Although some efforts have emerged to automate the parsing of specifications (For instance, RFCSCAN attempts to treat individual RFC sections as test units and directly compare them with the implementation [7]), these approaches remain limited to coarse-grained, section-level parsing. As a result, they lack the capability for more fine-grained analysis of the documents, making it challenging to automatically generate test cases targeting specific functional points.

Insight: The majority of protocol documents follow strict format requirements and are structured using specific terminology to define and organize key concepts.

Taking CoAP as an example, we reviewed a total of 32 RFC documents related to CoAP and found that 87.5% of them comply with RFC 2119 [8], [9]. These documents use uppercase keywords such as MUST, REQUIRED, SHALL, to define and emphasize critical protocol specifications and requirements (named the functional points). Even the documents that do not strictly follow RFC 2119 still use similar auxiliary verbs as keywords to highlight protocol functional points.

Preliminary Experiment: Furthermore, we examine the coverage when using keywords to locate functional points.

Prompt: I will give you a new function point requirement about the <{protocol}>, and you should think step by step and output a test case to verify this new function point. The test case start with "<<<" and ends with ">>>" . Note that you should pay attention to learn the organization structure of the test case examples.

# Test Case Examples:

?? :As the OPTIONS and TRACE methods are not supported in CoAP, a 501 (Not Implemented) error MUST be returned to the client.

????:<<<

Test Case: Verify that the CoAP server returns a 501 error for unsupported OPTIONS and TRACE requests.

1. Test Preconditions: …   
2. Test Steps:   
3. Test Assertion: …   
4. Precautions: …>>> (????, ????) , (????, ????)…

![](images/4a98401e7e74794b0c8dbc8ea9d4602a31251fd8be77e5f910e3bb6a227f0679.jpg)

??????????: { The HEAD thod is identical to GET cept that the server MUST OT return a message-body he response. }

![](images/efabe1274c850d4f4ac3bf379a4c7297721afd2264c3a45b3d6382ea92210012.jpg)

??????????: <<<

Test Case: Verify the

HEAD method in the CoAP .

1. Test Preconditions: …   
2. Test Steps: …   
3. Test Assertion: …   
4. Precautions: …>>>

Fig. 2: Example of generating test cases using few-shot incontext learning. The contents in the red, blue, green, and black boxes represent the guidance, example, input functional point, and output test case, respectively.

Assuming the keyword set is K, and following RFCSCAN, we take the smallest subsections $s _ { i } , i = 1 , . . . , N$ as the evaluation units. The section coverage C is then defined as follows:

$$
C = \frac {\sum_ {i = 1} ^ {N} L (s _ {i}) \cdot I (s _ {i})}{\sum_ {i = 1} ^ {N} L (s _ {i})}, \tag {1}
$$

where the function $L ( s _ { i } )$ measures the string length of $s _ { i } ,$ since sections vary in length and longer sections are more likely to contain additional functional points. $I ( s _ { i } )$ is the indicator function, defined as follows:

$$
I (s _ {i}) = \left\{ \begin{array}{l l} 1, & \exists k \in K, k \in s _ {i}, \\ 0, & \text { otherwise }. \end{array} \right. \tag {2}
$$

The experiment shows that for 32 CoAP-related RFC documents (considering only the main body), the overall section coverage reaches 87.50%, with 10 documents achieving a section coverage of 100%. These results demonstrate that using keywords to locate functional points can parse documents at a finer granularity while ensuring high section coverage.

Inspired by the above insight and experiment, we design a novel specification-driven test case generation method named keyword-based test case generation (keyword-based TCG). This method is integrated into the test case generation module, as shown in Fig. 1. Keyword-based TCG combines heuristic rules with the idea of generating datasets using LLMs. Specifically, this method first detects whether the document follows RFC 2119. If it does, keyword-based TCG uses regular expressions to extract paragraphs containing uppercase keywords; if not, it defaults to case-insensitive keyword extraction. Each extracted paragraph is a complete natural paragraph to preserve as much contextual semantic information as possible. We define these paragraphs as functional points.

Based on these functional points, keyword-based TCG calls the LLM to generate test cases. To ensure a standardized format for the test cases, we introduce few-shot incontext learning into the LLM. Specifically, we construct a prompt p with input-output example $\{ \langle x _ { i } , y _ { i } \rangle \} _ { i = 1 } ^ { k }$ , where $x _ { i }$ represents a functional point, and $y _ { i }$ is a standardized test case. These input-output pairs are concatenated in the format: $\left\{ \langle x _ { 1 } , y _ { 1 } \rangle , \langle x _ { 2 } , y _ { 2 } \rangle , \dots , \langle x _ { k } , y _ { k } \rangle \right\}$ . During reasoning, the test $x _ { t e s t }$ is appended to the prompt, and the LLM learns the structure from the provided examples, generating an output $y _ { t e s t }$ in the same format, as illustrated in Fig. 2. The test cases generated by the LLM comprise four components: test preconditions, test steps, test assertions, and precautions. The test steps describe in detail the procedure for testing the selected functional point, and the test assertions define the criteria for judging test success, which serve as the basis for evaluating the results. To ensure the test cases are both domain-relevant and effective, we adopt standard processes of data generation [10], introducing a filter to review the functional points and their corresponding test cases, removing any anomalous test cases.

Remark: It is important to note that the test case generation module is optional, meaning that test cases do not necessarily have to be generated by this module. iPanda allows users to import their own test cases, meanwhile still providing compatibility with subsequent program generation and conformance verification functionalities. The main purposes of the test case generation module are twofold: to facilitate the rapid generation of effective test cases directly from protocol documents, reducing the workload for users; and to provide standardized experimental datasets for this work, enabling a quantitative evaluation of iPanda’s performance.

# B. Automated Program Synthesis

Although LLMs have demonstrated exceptional performance, their outputs are not entirely reliable. For conformance testing, even when restricting the scope to a certain protocol implementation library, LLMs still exhibit the following issues during generating test programs:

• LLM’s limited understanding of code libraries. Firstly, LLM’s training data is inherently outdated. As Tab. I shows, even recent models have knowledge cutoffs several months in the past, leaving them unaware of new libraries. Secondly, the scarcity of open-source examples for implementation libraries also results in the lack of training data, hindering effective code generation. This phenomenon will be further demonstrated in subsequent experiments.   
• Hallucinations in LLM-generated code. LLM hallucinations refer to instances where the LLM generates outputs that appear realistic and credible but are actually incorrect, fabricated, or baseless. This issue, an inherent artifact of the model’s probabilistic nature, is difficult to completely eliminate. In this work, we define code hallucinations as generated code that: (1) calls non-existent library classes or attributes, (2) uses classes or methods incorrectly, or (3) configures required parameters improperly.

TABLE I: LLM training data cutoff time 

<table><tr><td>LLM</td><td>Release date</td><td>cutoff</td></tr><tr><td>GPT-o3-pro [11]</td><td>2025/6/10</td><td>2024/6/1</td></tr><tr><td>GPT-4o(2024-11-20) [12]</td><td>2024/11/20</td><td>2023/10</td></tr><tr><td>Deepseek-R1-0528 [13]</td><td>2025/5/28</td><td>unknown</td></tr><tr><td>Deepseek-V3-0324 [14]</td><td>2025/3/25</td><td>unknown</td></tr><tr><td>Claude-opus-4 [15]</td><td>2025/5/14</td><td>2025/3</td></tr><tr><td>Gemini-2.5-pro [16]</td><td>2025/6/17</td><td>2025/1</td></tr><tr><td>Qwen2.5-Coder-32B [17]</td><td>2024/11/6</td><td>unknown</td></tr></table>

1 The statistics were collected on 2025/7/15.

These issues lead to inefficiencies when blindly relying on LLMs to generate task-specific programs based on a given implementation library.

To address these issues, we first introduce code-oriented RAG into the long-term memory repository. We collect all code and examples files related to the implementation. These files naturally contain high-quality, protocol-specific knowledge that LLMs may lack. iPanda then uses OpenAI’s text embedding model to convert these code files into semantic vector representations and builds a local vector database using Chroma [18]. When generating test programs for the test cases, the long-term memory repository first retrieves code files with high similarity to the given test case based on cosine similarity. These retrieved results serve as contexts to help the LLM better understand how to use the implementation.

Moreover, to enable the LLM to generate high-quality test programs, we design a customized CoT method to guide the LLM in the reasoning module to perform step-by-step reasoning [19]. This process simulates how a human developer incrementally develops test subprograms, thereby enhancing the reasoning module’s capability to handle complex test cases.

CoT1: test case understanding. The LLM first decomposes the test case into multiple subtasks based on the test preconditions specified in the case. Specifically, for a test case that involves the collaboration of multiple participants (e.g., clients and servers), the LLM derives a clear and ordered subtask for each participant role and determines the required number of instances for each role. Each role instance comprises a sequence of atomic operations (e.g., connecting to the server rather than connecting and sending data).

CoT2: subprogram generation. Given an instance subtask, the LLM is required to generate the corresponding subprogram, strictly aligning with the subtask operations. The LLM uses the contexts by RAG to understand the implementation and then defines the specific behavior of each role instance in the subprogram. All subprograms are encapsulated as independent executable scripts and stored locally.

CoT3: determining the subprogram execution order. This step orchestrates the independent subprograms into a complete test execution flow. Although each role instance is independent, there are causal dependencies among them. For example, a server cannot accept a connection before a client requests it; a server typically starts before the client and remains in a listening state. Therefore, after all subprograms have been generated, the LLM infers the correct startup sequence based on the test steps defined in the test case.

CoT4: program integration. Once the startup order of the subprograms has been determined, the LLM leverages its incontext learning capability to integrate all subprograms and their corresponding execution order into a single, structured execution blueprint. This blueprint is output as a JSON string, which offers high readability, is easy to parse, and ensures cross-platform compatibility.

# C. Optimizing Test Programs

Automated Test Execution. When conducting automated tests, once the reasoning module generates the integrated program, testers typically need to manually launch all subprograms sequentially. This frequent user intervention is both cumbersome and time-consuming. To address this issue, we develop an automated testing platform within the execution module. This platform automatically parses program texts in JSON format and adaptively launches subprograms in an isolated virtual environment, ensuring that the subprograms are executed safely and under control. If an execution error occurs (e.g. missing attributes and syntax errors), iPanda embeds the execution log into the prompt and initiates its iterative optimization mechanism to debug the program code until the generated program executes successfully. Once the program runs without errors, the LLM evaluates the success of the test by comparing the test assertions defined in the test case with the executed program and its results.

Iterative Optimization Algorithm. Error logs encountered during program execution serve as a naturally accessible and high-quality source of knowledge. They can effectively guide the LLM in refining and debugging. Therefore, iPanda utilizes automated testing platform to iteratively validate and refine its output through human-like interaction [20]. This process continues until either executable program is generated or the maximum number of retries is reached.

Specifically, given the reasoning module’s LLM model M and the input test case x, the initial program solution $\hat { y } _ { 0 }$ is generated by the prompt ℘ as $\hat { y } _ { 0 } \sim \mathbb { P } _ { \mathcal { M } } ( \cdot | \boldsymbol { \wp } + \boldsymbol { x } + \boldsymbol { r } _ { 0 } )$ . The automated testing platform T then tests this initial solution, producing feedback $c _ { 0 } = \mathcal { T } ( \hat { y } _ { 0 } )$ . For the (i + 1)-th iteration $( i \geq 0 )$ , the LLM’s output iterates as:

$$
\begin{array}{l} \hat {y} _ {i + 1} \sim \mathbb {P} _ {\mathcal {M}} (\wp + x \\ + \left(r _ {i - m + 1} + \hat {y} _ {i - m + 1} + c _ {i - m + 1} + \wp^ {\prime}\right) \\ + \left(r _ {i - m + 2} + \hat {y} _ {i - m + 2} + c _ {i - m + 2} + \wp^ {\prime}\right) \tag {3} \\ + \dots \\ + \left(r _ {i} + \hat {y} _ {i} + c _ {i} + \wp^ {\prime}\right) \\ \left. + r _ {i + 1}\right), \\ \end{array}
$$

where $\wp ^ { \prime }$ is a prompt template designed to guide the LLM in debugging. The parameter $1 ~ \leq ~ m ~ \leq ~ i + 1$ represents the window size of the short-term memory cache, preventing the input length from exceeding the maximum text length that the LLM can handle (e.g., GPT-4o supports up to 128K tokens [12]). When $m = i + 1$ , it considers all historical interaction information. The $r _ { i }$ is the context retrieved from long-term memory repository by R, specifically as:

$$
r _ {i} = \left\{ \begin{array}{l l} \mathcal {R} (\wp + x), & i = 0, \\ \mathcal {R} (c _ {i - 1} + \wp^ {\prime}), & i \geq 1. \end{array} \right. \tag {4}
$$

This optimization process continues until the generated program meets specific execution success criteria or the maximum step of iterations is reached. The pseudocode for iterative optimization algorithm is shown in Alg. 1.

Algorithm 1 Iterative Optimization Algorithm   
Require: Input x, initial prompt $\wp ,$ iteration prompt $\wp ^ { \prime } ,$ LLM $\mathcal { M } ,$ testing platform $\tau ,$ retriever $\mathcal { R } _ { : }$ , maximum step n   
Ensure: output $\hat{y}$ from M
1: $r \leftarrow \mathcal{R}(\wp + x)$ 2: $seq \leftarrow \wp + x + r$ 3: Generate initial output $\hat{y}_{0} \sim \mathbb{P}_{\mathcal{M}}(\cdot | seq)$ 4: for $i \leftarrow 0$ to $i \leftarrow n - 1$ do
5: $c \leftarrow \mathcal{T}(\hat{y}_{i})$ 6: if c indicates that $\hat{y}_{i}$ is correct then
7: return $\hat{y}_{i}$ 8: end if
9: $r \leftarrow \mathcal{R}(\wp' + c)$ 10: $seq \leftarrow seq + \hat{y}_{i} + c + \wp' + r$ 11: Generate $(i + 1)$ -th output $\hat{y}_{i+1} \sim \mathbb{P}_{\mathcal{M}}(\cdot | seq)$ 12: end for
13: return $\hat{y}_{n}$

Remark: During the iteration, the test program is continuously refined. As the number of iterations increases, the length of the input context grows linearly, which in turn increases the reasoning load on the LLM. Therefore, it is crucial to set an appropriate cache window size to limit the context length. Additionally, the more iterations, the smaller the marginal benefit of program correction. Hence, selecting an optimal maximum step of iterations is essential. Based on experimental observations, we set the default maximum step to 6.

# D. Summarizing Bugs

The summarization module performs two key functions:

• Summarizing program generation experience. With appropriate prompt guidance, the module generates experience sˆ by analyzing the program testing process $\wp + x + ( \hat { y } _ { 0 } +$ $c _ { 0 } ) + \cdot \cdot \cdot + ( \hat { y } _ { t - 1 } + c _ { t - 1 } ) + \hat { y } _ { t }$ . The experience is stored in the long-term memory repository as valuable knowledge to continuously enhance iPanda’s overall performance. By leveraging the accumulated experience, the iterative optimization algorithm can refine program corrections more efficiently, ensuring that iPanda continuously learns and improves its ability to handle similar tasks in the future with greater efficiency and accuracy.   
• Ensuring conformance between protocol and its implementation. With prompts guidance, the module also reviews the test cases and the usage of the protocol implementation. It evaluates whether the tested protocol implementation

adheres to the specifications embedded in the test cases, and generates corresponding conformance testing reports.

A primary challenge is distinguishing genuine conformance testing results from incidental code generation errors. Due to inherent randomness and the imperfect adherence to instructions, the LLM may erroneously report on its own code generation errors (e.g., incorrect parameter passing or invalid attribute calls) instead of actual conformance violations. To isolate the true conformance test results, we implement a two-stage filtering process. Firstly, a keyword-based filter automatically removes reports containing terms associated with common generation bugs, including incorrect parameter passing (e.g., incorrectly binding to any-address) and incorrect method or attribute calling (e.g., some attribute does not exist). Subsequently, the remaining reports undergo manual review to verify their relevance and accuracy.

# IV. EVALUATION

In the section, we present our experimental setup, results and analyses, to demonstrate iPanda’s effectiveness.

# A. Experimental Setup

1) Experimental platform: We implemented the iPanda using Python and deployed it on our local server. All target protocol implementations, along with their required libraries, were pre-installed in a local virtual environment. For LLM, we used GPT-4o [12], DeepSeek-V3 [21], and Qwen2.5-Coder-32B [17]. These models represent the most advanced base models, differing in architecture, size, and pretraining focus.   
All LLMs were configured with short-term memory window size $m = 1 0 ,$ temperature = 0, and top ${ \it p } = 0 . 1$ . For RAG, we utilized OpenAI’s text-embedding-3-large as embedding model [18]. For simplicity and generality, the testing environment was configured locally, using the local IP address and different ports to simulate network conditions.   
2) Tested protocols and Implementations: We selected the following protocols and their Python implementations:

• CoAP & aiocoap [22]. The Constrained Application Protocol (CoAP) is a lightweight network communication protocol designed for resource-constrained devices, primarily used for IoT devices. It was standardized in 2014 as RFC 7252 [8]. As of March 2025, there are 32 RFC documents related to CoAP [9]. We selected aiocoap, the Python implementation of CoAP, as the target for conformance testing. As of March 2025, aiocoap fully or partially supports 9 CoAP-related RFC documents.

• RSocket & rsocket-py. RSocket is an application protocol that provides reactive stream semantics over an asynchronous, binary boundary. As of March 2025, RSocket has not yet been formalized as a RFC standard. However, it has a well-established specification [4] (adhering to RFC 2119) and implementations across various programming languages. We selected rsocket-py, the Python implementation of RSocket, as the target for conformance testing.

The key reason for selecting them is that they meet important criteria for conformance testing: (1) the protocols have established mature specifications, but their implementations have only recently developed; (2) only partial specifications have been implemented in the implementations; (3) there are no mature conformance testing tools for these implementations.

Notably, LLMs possess varying levels of pre-existing knowledge about specific protocols. Therefore, the RAG was adapted based on the LLM’s prior knowledge of each library. A preliminary assessment revealed that the LLM has extensive built-in knowledge of aiocoap, so we deactivated the longterm memory repository to isolate its inherent capabilities. Conversely, for rsocket-py, a more recent library with limited open-source examples, the LLM lacked sufficient knowledge. Therefore, we retained the long-term memory repository and augmented it with the library’s source code to provide the necessary context.

3) Dataset: Using the keyword-based TCG in Sec. III-A, we introduced two test case sets for CoAP and RSocket:

• CoAP-set. We selected 11 RFC documents directly related to CoAP to generate the CoAP-set, which consists of 231 uniformly formatted test cases.   
• RSocket-set. We generated the RSocket-set using RSocket document, having 62 test cases.

All test cases underwent professional manual review and selection to ensure their authenticity and validity. Each test case follows a standardized format comprising five components: test case name, test preconditions, test steps, test assertions, and precautions. Notably, the core of our work is on the accuracy of iPanda’s code generation and the effectiveness of its conformance testing. Therefore, rather than pursuing exhaustive specification coverage, our work prioritizes the validity and relevance of individual test cases. To ensure the consistency and comparability of our findings, we employ the same test cases across all experiments.

4) Baseline: Specification-driven conformance testing methods typically require the development of protocol-specific conformance testing tools. Unfortunately, no open-source conformance testing tools currently exist for CoAP and RSocket. Moreover, our work is the first to employ LLMs for conformance testing in a protocol-agnostic manner. To reasonably evaluate iPanda’s performance, we selected a pure-LLM baseline approach in which the LLM generates test program in a single step (using the same prompt and setup). This corresponds to the startup stage of iPanda with the memory module disabled, serving as our experimental baseline.

5) Metrics: Pass@k. This metric is commonly used to evaluate the correctness and reliability in generating code for a given programming task, which is a core sub-task of iPanda. P ass@k measures the probability that at least one of the k generated code solutions is correct. Specifically, for a test set containing N cases $\{ T _ { 1 } , T _ { 2 } , \dots , T _ { N } \}$ , the P ass@k metric for

an LLM M is defined as:

$$
P a s s @ k = \frac {\sum_ {i = 1} ^ {N} \left(\phi_ {1} (T _ {i}) \oplus \phi_ {2} (T _ {i}) \oplus \cdots \oplus \phi_ {k} (T _ {i})\right)}{N}, \tag {5}
$$

where ⊕ denotes the XOR operator, and $\phi _ { j } ( \cdot ) ~ \in ~ \{ 0 , 1 \}$ represents the evaluation of the j-th generated solution. It takes a value of 1 if the solution is correct and 0 otherwise.

Conformance testing results. To evaluate the effectiveness of iPanda in conformance testing, we conduct a qualitative assessment of the generated programs compliance with specifications. The assessment categorizes results into two types:

• Positive samples: The generated program is executable and functions in accordance with the specification.   
• Negative samples: The code fails to execute or functionally violates the protocol requirements.

# B. Marginal Benefit Analysis

As the number of iterations increases, the marginal benefit of program correction gradually decreases. To achieve the optimal marginal benefit, we must first determine an appropriate maximum step of LLM iterative reasoning. In our experiments, we set the upper limit for reasoning iterations to 10. iPanda was tested on the CoAP-set, which contains more test samples. To analyze the required number of reasoning iterations for successfully generating executable program, we constructed a histogram depicting the cost of successful generations. The experimental results are shown in Fig. 3. It can be observed that in most cases, no more than 6 steps are required to generate executable program. Specifically, when setting the maximum step to 10, using GPT-4o, iPanda successfully tested 195 cases in the CoAP-set (classified as positive samples), among which 187 cases required no more than 6 iterations, accounting for $1 8 7 / 1 9 5 = 9 5 . 9 0 \%$ . Using DeepSeek-V3, the corresponding proportion was $1 3 2 / 1 4 3 = 9 2 . 3 1 \%$ . Using Qwen2.5-Coder-32B, the proportion was $7 4 / 9 4 = 7 8 . 7 2 \%$ . Under the influence of the scaling law, large-scale foundation models such as GPT-4o and DeepSeek-V3 (both exceeding 100B parameters) exhibit stable performance in program generation and correction. As the number of iterations increases, both marginal benefit steadily declines. However, for Qwen2.5-Coder-32B, which has only 32B parameters, the marginal benefit is relatively unstable. This may be attributed to the model’s smaller scale, leading to weaker program generation capabilities. Resultly, we set the maximum step of iterations to 6 in subsequent experiments to achieve the optimal marginal benefit.

# C. Performance Analysis of Program Generation

We conducted experiments using the baseline and iPanda supported by the three LLMs to evaluate their code generation performance on the CoAP-set. The P ass@1 experimental results for all methods are shown in Tab. II. Experimental results show that under the same LLM conditions, iPanda significantly enhances program generation capabilities compared to the baseline. P ass@1 is improved by 4.675×(GPT-4o), 6×(Deepseek-V3), and 10.751×(Qwen2.5-Coder-32B)

![](images/4d9a4b1ddb5da2c1d6deaf99fb09a330814c2dab23fc5278f28880e99c2f0cd0.jpg)



(a) GPT-4o

![](images/bc52f38e019fe9b16316955d52986e15d3208975e8a67164787b20d1faf40b93.jpg)



(b) Deepseek-V3

![](images/9b137ba7bf19b6ccee1b6c79009f96039626f64bc3cf787c6bb9048ea1e4b941.jpg)



(c) Qwen2.5-Coder-32B   
Fig. 3: The number of code successfully generated within the maximum iteration step limit, using (a) GPT-4o, (b) Deepseek-V3, and (c) Qwen2.5B-Coder-32B.

respectively. For example, when using the GPT-4o, the baseline achieves only a P ass@1 of 17.32%. In contrast, iPanda improves this by 4.675×, reaching 80.95%. This strongly validates that aiocoap aligns with the specifications underlying these test cases, reducing the likelihood of nonconformances and narrowing the focus for critical testing. Even with the smallest model Qwen2.5-Coder-32B, iPanda’s P ass@1 is nearly twice that of the baseline using the most advanced model GPT-4o. These results confirm the success of the iterative optimization algorithm. With its support, even smallerscale LLMs can be stimulated to exhibit stronger program generation capabilities, achieving performance comparable to or even surpassing larger, more advanced LLMs.

TABLE II: P ass@1 comparison on CoAP-set 

<table><tr><td>Used-LLM</td><td>Baseline</td><td>iPanda</td></tr><tr><td>GPT-4o</td><td>17.32%</td><td>80.95%</td></tr><tr><td>Deepseek-V3</td><td>9.52%</td><td>57.14%</td></tr><tr><td>Qwen2.5-Coder-32B</td><td>3.03%</td><td>32.03%</td></tr></table>

![](images/c4ec7abe1c6c3b52bcec2bd7f0a0008df38472eb01e7fb1a47b1a240b9dc9f90.jpg)



(a)   
Fig. 4: (a) The joint experiment of maximum reasoning step $S _ { m a x }$ and repetition numbers k. The numbers in squares represent the number of executable program generated by iPanda under the $S _ { m a x }$ and k. (b) Statistics of RFC documents containing failed test cases under $S _ { m a x } = 6$ and $k = 6$ . The size of the sector reflects how many failed test cases the RFC document contains.

Due to the inherent randomness in LLM-generated content, multiple repeated tests are typically required for program generation, and performance is often evaluated using P ass@k. Therefore, we conducted a joint experiment to examine the impact of the maximum reasoning iteration step $S _ { \mathrm { m a x } }$ and the number of repeated tests k. Given the strong performance of GPT-4o, we selected it as the default LLM for iPanda. The experiment was configured with $S _ { \mathrm { m a x } } = \{ 1 , 2 , 3 , 4 , 5 , 6 \}$ and $k = \{ 1 , 2 , 3 , 4 , 5 , 6 \}$ . The experimental results on the CoAPset are shown in Fig. 4-(a), where the numbers in squares represent the number of executable program generated by iPanda under the current $S _ { m a x }$ and k. When setting $S _ { \mathrm { m a x } } = 6$ and $k = 1$ , the experiment degenerates into the setup of Fig. 3- (a). When setting $S _ { \mathrm { m a x } } ~ = ~ 1$ and $k \ = \ 6 ,$ the experiment degenerates into the baseline $P a s s @ 6$ evaluation. From the results, we observe that increasing the reasoning iteration step significantly improves iPanda’s performance. Additionally, repeated testing can also enhance the success rate of program generation, though its impact is considerably smaller than increasing reasoning iterations. For instance, increasing the number of repeated tests by five (i.e., k = 6 instead of k = 1) raises the number of positive samples from 31 to 89. Increasing the number of inference iterations by five $( \mathrm { i . e . , ~ } S _ { \mathrm { m a x } } ~ = ~ 6 $ instead of $S _ { \mathrm { m a x } } = 1 )$ raises the number of positive samples from 31 to 182. These results validate the rationality of our decision to adopt a sequential strategy (i.e., iterative program generation using a single LLM), rather than a parallel strategy (i.e., involving multiple LLMs generating program simultaneously). While the former has a higher interaction cost per step due to increased context, this additional context contains valuable execution feedback, providing richer information to guide the LLM in refining the generated program.

# D. Ablation Study

To validate the effectiveness of the methods used in iPanda, we conducted an ablation study to analyze the contributions of code-oriented RAG and iterative optimization algorithm. The experimental results are presented in Tab. III. Since LLMs have a deep understanding of CoAP and aiocoap, the long-term memory repository was frozen, disabling the code-oriented RAG. As a result, RAG does not impact the testing outcomes for this protocol, leading to only two experimental configurations in the ablation study. To evaluate the effectiveness of code-oriented RAG, we introduced additional tests for the RSocket protocol and its Python implementation, rsocket-py. In this setup, iPanda was preloaded with the open-source code of rsocket-py for use in RAG. Experimental results on the RSocket-set revealed that the inclusion of code-oriented RAG significantly improved LLM’s ability to understand and correctly utilize rsocket-py. This resulted in an increase in P ass@1 from 14.51% to 38.71%.

TABLE III: Ablation study on P ass@1 

<table><tr><td>Approach</td><td>CoAP-set</td><td>RSocket-set</td></tr><tr><td>iPanda</td><td>80.95%</td><td>38.71%</td></tr><tr><td>iPanda, w/o code-oriented RAG</td><td>80.95%</td><td>14.51%</td></tr><tr><td>iPanda, w/o iterative optimization</td><td>17.32%</td><td>3.23%</td></tr><tr><td>Baseline</td><td>17.32%</td><td>11.29%</td></tr></table>

When the iterative optimization algorithm is removed, iPanda degrades into the baseline that only incorporates code-oriented RAG. Experimental results show that, on both datasets, the performance of iPanda drops significantly without the iterative optimization algorithm. This phenomenon has been extensively studied in previous experiments. Nevertheless, on the RSocket-set, even without the iterative optimization algorithm, iPanda still outperforms the baseline. This further demonstrates the effectiveness of code-oriented RAG.

Remark: The primary goal of iPanda is to support conformance testing for multiple communication protocols. Therefore, it must exhibit protocol compatibility. Meanwhile, we also expect iPanda’s performance to improve as the underlying LLMs advance, requiring it to maintain model compatibility. The extensive performance and ablation experiments conducted above confirm that iPanda demonstrates strong compatibility with both different protocols and different LLMs.

# E. Results Analysis of Conformance Testing

According to the joint experiment results in Sec. IV-C, maximizing the number of iterations and repetitions yields the highest number of positive samples, indicating that aiocoap conforms to the majority of protocol specifications. For negative samples, we analyzed the documents they belong to, as shown in Fig. 4-(b). Notably, Most of the negative samples are concentrated in the CoAP’s RFC 9177. This suggests that aiocoap has likely not yet implemented the specifications outlined in RFC 9177. This hypothesis aligns with the author’s introduction on GitHub [22], which specifies the standards supported by aiocoap, confirming that RFC 9177 has not yet been implemented in aiocoap. By generating as many positive samples as possible, iPanda can effectively reduce the scope of conformance testing. In addition, the test results of negative samples also guide further testing.

# V. RELATED WORK

Traditional testing tools. Several tools have been developed for protocol testing. Testing and Test Control Notation version 3 (TTCN-3) is a widely used language for rigorous conformance certification in mobile communications, and IoT protocols [23]. Scapy enables flexible construction and transmission of custom packets via scripting, aiding tests of protocol edge cases and exception handling, particularly in security assessments [24]. Protocol fuzz testing tools, such as Fairfuzz and Boofuzz, have demonstrated strong capabilities in uncovering vulnerabilities and testing robustness [25]– [27]. However, these tools are typically applied at specific stages within existing testing workflows and heuristic-based approaches [28]. A major limitation remains their dependence on the manual creation of test cases and scripts, requiring substantial developer effort. Currently, no tool seamlessly integrates protocol documentation, implementation, and tests into one conformance testing process. Addressing this gap is precisely the focus of our work.

LLM-based automated testing tools. Automated testing tools based on LLMs have gained increasing attention in recent years. Researchers have begun exploring LLM-powered agents for automating testing tasks. In code testing, some studies leveraged LLMs to generate high-coverage unit tests, such as those for the JUnit testing framework [29], [30]. PENTESTGPT, an penetration testing tool, effectively identifies common vulnerabilities and analyzes source code for flaws [31]. DB-GPT integrates the Tree-of-Thought method into LLMs to systematically analyze database anomalies [32]. In fuzz testing, existing tools often struggle with message format obfuscation and dependencies between messages. To address this, LLMIF [1] integrates LLMs into IoT fuzz testing to automate the extraction of protocol formats and device response inference. However, those LLM-driven testing tools typically target isolated tasks and do not effectively support conformance testing. RFCScan is most similar to our work. It builds semantic indexes for both implementation code and specifications to detect conformances between the code and the RFC specifications at the semantic level. However, this approach focuses on static comparisons between code and specifications, rather than simulating how developers write test cases to verify the actual runtime behavior of the protocol, which is precisely where our work differs. To address this research gap, we introduce iPanda, an LLM-based agent tailored specifically for protocol conformance testing.

Augmented LLMs. Although LLMs excel in tasks such as question answering and text generation, their performance remains constrained by the limitations of pre-trained datasets and the context provided during inference. As a result, they may perform poorly in certain specialized tasks. To address these limitations, researchers have explored various tools to enhance LLM capabilities, including Web browsers [33]–[35], RAG [36]–[38], programming tools [20], [39], other deep neural network models [40], and so on [41]–[43]. Similarly, in our work, iPanda incorporates RAG and programming tools to enhance the effectiveness of LLMs, improving their ability to analyze protocol specifications, generate test cases, and interact with protocol implementation libraries.

# VI. CONCLUSION

We present iPanda, the first LLM-based intelligent agent for automated conformance testing of communication protocols.

iPanda leverages the keyword-based TCG method to efficiently generate test cases from protocol documents, and employs code-oriented RAG and customized CoT strategy to enhance its understanding of tested protocol implementation and generate test program. Furthermore, the ierative optimization algorithm is integrated for iterative program refinement in automated testing platform. Through execution-based validation, iPanda assesses whether the protocol implementation adheres to the specified protocol requirements. Experimental results prove the effectiveness and high efficiency of iPanda in conformance testing.

# REFERENCES

[1] J. Wang, L. Yu, and X. Luo, “Llmif: Augmented large language model for fuzzing iot devices,” in 2024 IEEE Symposium on Security and Privacy (SP). IEEE, 2024, pp. 881–896.   
[2] H. Wen, Y. Li, G. Liu, S. Zhao, T. Yu, T. J.-J. Li, S. Jiang, Y. Liu, Y. Zhang, and Y. Liu, “Autodroid: Llm-powered task automation in android,” in Proceedings of the 30th Annual International Conference on Mobile Computing and Networking, 2024, pp. 543–557.   
[3] H. Wen, S. Tian, B. Pavlov, W. Du, Y. Li, G. Chang, S. Zhao, J. Liu, Y. Liu, Y.-Q. Zhang et al., “Autodroid-v2: Boosting slm-based gui agents via code generation,” arXiv preprint arXiv:2412.18116, 2024.   
[4] rsocket. (2024) Rsocket. [Online]. Available: https://rsocket.io/about/ protocol/   
[5] rsocket py. (2025) rsocket-py. [Online]. Available: https://github.com/ rsocket/rsocket-py   
[6] A. V. Grammatopoulos, I. Politis, and C. Xenakis, “Blind softwareassisted conformance and security assessment of fido2/webauthn implementations.” J. Wirel. Mob. Networks Ubiquitous Comput. Dependable Appl., vol. 13, no. 2, pp. 96–127, 2022.   
[7] M. Zheng, C. Wang, X. Liu, J. Guo, S. Feng, and X. Zhang, “An llm agent for functional bug detection in network protocols,” arXiv preprint arXiv:2506.00714, 2025.   
[8] Z. Shelby, K. Hartke, and C. Bormann, “Rfc 7252: The constrained application protocol (coap),” 2014.   
[9] R. Editor. (2025) Rfc editor. [Online]. Available: https://www.rfc-editor. org/search/rfc search detail.php?page=All&title=coap   
[10] X. Guo, H. Okamura, and T. Dohi, “Automated software test data generation with generative adversarial networks,” IEEE Access, vol. 10, pp. 20 690–20 700, 2022.   
[11] OpenAI. (2025) gpt-o3-pro. [Online]. Available: https://platform.openai. com/docs/models/o3-pro   
[12] A. Hurst, A. Lerer, A. P. Goucher, A. Perelman, A. Ramesh, A. Clark, A. Ostrow, A. Welihinda, A. Hayes, A. Radford et al., “Gpt-4o system card,” arXiv preprint arXiv:2410.21276, 2024.   
[13] Deepseek. (2025) deepseek-r1. [Online]. Available: https://api-docs. deepseek.com/news/news250528   
[14] — —. (2025) deepseek-v3. [Online]. Available: https://api-docs. deepseek.com/news/news250325   
[15] Anthropic. (2025) claude-opus-4. [Online]. Available: https://docs. anthropic.com/en/docs/about-claude/models/overview   
[16] Google. (2025) Gemini-2.5-pro. [Online]. Available: https://cloud. google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-pro   
[17] B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang, B. Yu, K. Lu et al., “Qwen2. 5-coder technical report,” arXiv preprint arXiv:2409.12186, 2024.   
[18] OpenAI. (2024) text-embedding-3-large. [Online]. Available: https: //openai.com/index/new-embedding-models-and-api-updates/   
[19] L. Shen, Q. Yang, Y. Zheng, and M. Li, “Autoiot: Llm-driven automated natural language programming for aiot applications,” arXiv preprint arXiv:2503.05346, 2025.   
[20] A. Alinezhad, J. Khalili, A. Alinezhad, and J. Khalili, “Critic method,” New methods and applications in multiple attribute decision making (MADM), pp. 199–203, 2019.   
[21] A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan et al., “Deepseek-v3 technical report,” arXiv preprint arXiv:2412.19437, 2024.   
[22] aiocoap. (2025) aiocoap. [Online]. Available: https://github.com/chrysn/ aiocoap

[23] J. Grabowski, D. Hogrefe, G. Rethy, I. Schieferdecker, A. Wiles, and ´ C. Willcock, “An introduction to the testing and test control notation (ttcn-3),” Computer Networks, vol. 42, no. 3, pp. 375–403, 2003.   
[24] R. Rohith, M. Moharir, G. Shobha et al., “Scapy-a powerful interactive packet manipulation program,” in 2018 international conference on networking, embedded and wireless systems (ICNEWS). IEEE, 2018, pp. 1–5.   
[25] J. Pereyda, “boofuzz documentation,” THIS REFERENCE STILL NEEDS TO BE FIXED, 2019.   
[26] C. Lemieux and K. Sen, “Fairfuzz: A targeted mutation strategy for increasing greybox fuzz testing coverage,” in Proceedings of the 33rd ACM/IEEE international conference on automated software engineering, 2018, pp. 475–485.   
[27] H. Peng, Y. Shoshitaishvili, and M. Payer, “T-fuzz: fuzzing by program transformation,” in 2018 IEEE Symposium on Security and Privacy (SP). IEEE, 2018, pp. 697–710.   
[28] F. Makhmudov, D. Kilichev, U. Giyosov, and F. Akhmedov, “Online machine learning for intrusion detection in electric vehicle charging systems,” Mathematics, vol. 13, no. 5, p. 712, 2025.   
[29] M. L. Siddiq, J. C. Da Silva Santos, R. H. Tanvir, N. Ulfat, F. Al Rifat, and V. Carvalho Lopes, “Using large language models to generate junit tests: An empirical study,” in Proceedings of the 28th International Conference on Evaluation and Assessment in Software Engineering, 2024, pp. 313–322.   
[30] V. Guilherme and A. Vincenzi, “An initial investigation of chatgpt unit test generation capability,” in Proceedings of the 8th Brazilian Symposium on Systematic and Automated Software Testing, 2023, pp. 15–24.   
[31] G. Deng, Y. Liu, V. Mayoral-Vilches, P. Liu, Y. Li, Y. Xu, T. Zhang, Y. Liu, M. Pinzger, and S. Rass, “Pentestgpt: An llm-empowered automatic penetration testing tool,” arXiv preprint arXiv:2308.06782, 2023.   
[32] X. Zhou, G. Li, and Z. Liu, “Llm as dba,” arXiv preprint arXiv:2308.05481, 2023.   
[33] X. Deng, Y. Gu, B. Zheng, S. Chen, S. Stevens, B. Wang, H. Sun, and Y. Su, “Mind2web: Towards a generalist agent for the web,” Advances in Neural Information Processing Systems, vol. 36, pp. 28 091–28 114, 2023.   
[34] R. Nakano, J. Hilton, S. Balaji, J. Wu, L. Ouyang, C. Kim, C. Hesse, S. Jain, V. Kosaraju, W. Saunders et al., “Webgpt: Browserassisted question-answering with human feedback,” arXiv preprint arXiv:2112.09332, 2021.   
[35] Z. Chen, Y. Ma, M. Liu et al., “Weinfer: Unleashing the power of webgpu on llm inference in web browsers,” in THE WEB CONFERENCE 2025, 2025.   
[36] X. Du, G. Zheng, K. Wang, J. Feng, W. Deng, M. Liu, B. Chen, X. Peng, T. Ma, and Y. Lou, “Vul-rag: Enhancing llm-based vulnerability detection via knowledge-level rag,” arXiv preprint arXiv:2406.11147, 2024.   
[37] C. Jeong, “Generative ai service implementation using llm application architecture: based on rag model and langchain framework,” Journal of Intelligence and Information Systems, vol. 29, no. 4, pp. 129–164, 2023.   
[38] K. K. Y. Ng, I. Matsuba, and P. C. Zhang, “Rag in health care: a novel framework for improving communication and decision-making by addressing llm limitations,” NEJM AI, vol. 2, no. 1, p. AIra2400380, 2025.   
[39] J. Lu, L. Yu, X. Li, L. Yang, and C. Zuo, “Llama-reviewer: Advancing code review automation with large language models through parameterefficient fine-tuning,” in 2023 IEEE 34th International Symposium on Software Reliability Engineering (ISSRE). IEEE, 2023, pp. 647–658.   
[40] Y. Shen, K. Song, X. Tan, D. Li, W. Lu, and Y. Zhuang, “Hugginggpt: Solving ai tasks with chatgpt and its friends in hugging face,” Advances in Neural Information Processing Systems, vol. 36, pp. 38 154–38 180, 2023.   
[41] X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdhery, and D. Zhou, “Self-consistency improves chain of thought reasoning in language models,” arXiv preprint arXiv:2203.11171, 2022.   
[42] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao, “React: Synergizing reasoning and acting in language models,” in International Conference on Learning Representations (ICLR), 2023.   
[43] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, “Reflexion: Language agents with verbal reinforcement learning,” Advances in Neural Information Processing Systems, vol. 36, pp. 8634–8652, 2023.