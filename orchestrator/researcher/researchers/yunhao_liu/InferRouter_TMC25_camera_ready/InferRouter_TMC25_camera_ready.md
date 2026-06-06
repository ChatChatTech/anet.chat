# Mitigating Tail Latency for On-Device Inference with Load-Balanced Heterogeneous Models

Mu Yuan, Lan Zhang, Di Duan, Liekang Zeng, Miao-Hui Song, Zichong Li, Guoliang Xing, Fellow, IEEE and Xiang-Yang Li, Fellow, IEEE

Abstract—Serving machine learning models on edge, mobile, and embedded devices places stringent requirements on inference latency. From operating a real enterprise service, we observed that even a fully optimized model could lead to severe violations of latency objectives when the load surges. A straightforward and mature approach is to auto-scale multiple models to balance the load. However, unlike cloud clusters, edge or mobile devices usually cannot afford to deploy multiple model replicas. Therefore, in this paper, we explore a new idea: in addition to the original model, we deploy one (or more) heterogeneous model(s) with much smaller resource overhead on the device, and perform load balancing among all models. We overcame the technical challenges posed by performance dynamics and developed InferRouter based on queuing theory. We implement and evaluate InferRouter on three real on-device inference systems, covering mobile sensing, video analytics, and natural language processing applications. Experimental results show that compared with strong baselines, InferRouter can decrease 85.2% P99 latency (5.8x faster) and improve 5.9% accuracy on the mobile workload. For a traffic video analytics task, InferRouter achieves 55.1% higher accuracy with zero deadline misses. InferRouter also shows its advantages in saving resources compared with auto-scaling and offloading approaches.

Index Terms—on-device machine learning, model inference, load balancing, queueing theory

# 1 INTRODUCTION

From IoT and embedded systems [1], [2] to mobile and edge devices [3]–[6], inference services of machine learning (ML) models are ubiquitous [7], [8]. High accuracy and low latency are two typical service-level objectives (SLOs) shared by most on-device inference services [9]–[11].

Existing techniques for efficient on-device inference have evolved significantly to address the challenges posed by limited resources and the need for real-time processing. Many works [12] have designed lightweight neural network structures for mobile and embedded devices. Another prominent approach is model compression [13], [14], which includes techniques such as quantization, pruning, and knowledge distillation. Additionally, frameworks like TensorFlow Lite [15] facilitate the deployment of optimized models on mobile and edge devices. The network systems community has also contributed many ideas to optimize inference efficiency, including input filtering [16]– [18], approximate caching [19], pipeline selection [20]–[22], speculative inference [23] early-exit neural networks [24], etc. These techniques collectively contribute to making ondevice inference more feasible and efficient in real-world systems.

![](images/699fe4e4f2e8b4bdb7a960858d73eb60ac77f11ba6bbae391b9937db8a9bfa58.jpg)



Fig. 1: Illustration of our idea: load balancing on heterogeneous models.

High tail latency in real-system traces. In developing smartwatch action recognition and edge traffic video analytics systems, we applied existing optimization techniques [13], [15], [16], [20] and obtained models with satisfactory throughput and accuracy. However, we observed high tail latency from the system operation logs. As shown in Fig. 2, we plot the inference latency under some selected time segments. By manually checking the data content, we realized that after applying input filtering (InFi [16]) and pipeline selection (Chameleon [20]), the inference load is quite dynamic, rather than uniform. The reason is that these optimization algorithms leverage the temporal correlation of online data to eliminate computational redundancy. When the smartwatch user is exercising vigorously or vehicles in the video are moving quickly, changes between consecutive data are significant, and model inference needs to be performed frequently. Therefore, the inference load bursts, causing congestion in the inference queue. This dynamic behavior highlights a critical challenge in real-time processing systems, where the variance in online workload can lead to unpredictable latency bursts. Such tail latency is particularly detrimental in applications requiring timely responses, such as health monitoring in smartwatches, where delays could impact user safety, or in traffic analytics, where real-time decisions are crucial for traffic management.

![](images/40d6d6c8318e8581380bea4935c0780ed4d0c69d14764a83138337dfe2f7b6a2.jpg)



(a) Mobile Action Recognition on Smartwatch

![](images/ddc1c44a94f69e1ac110a001f37296e57e29e7272273ab2bc8b8a2c20943b97b.jpg)



(b) Edge Vehicle Counting on Jetson Orin   
Fig. 2: With no awareness of load, on-device inference has intolerable latency when unpredictable load bursts arrive.

Utilizing heterogeneous small models. In data centers [25]–[27], load balancing is a classic approach to handling load bursts and reducing tail latency. Traditional methods have focused on scaling up resources automatically for non-ML services. Some works [22], [28]–[32] have also explored auto-scaling techniques for model inference in cloud clusters. However, mobile and edge devices are typically resource-scarce, so deploying additional model replicas is often prohibitive [33] due to constraints on processing power, memory, and battery life. On the other hand, heterogeneous model selection [34]–[36] methods aim to choose the most appropriate model from a pool of models with different accuracy-latency trade-offs, often based on input difficulty or confidence thresholds. However, a key limitation of such approaches is that they make decisions on a per-query basis without considering system-level dynamics such as load bursts. Consequently, they are ill-suited for scenarios where query arrival rates are unpredictable. In contrast to traditional load balancing or model selection, our goal is to adapt to workload variations rather than only adapt to input complexity. Therefore, in this work, we propose a new idea: As Fig. 1 shows, instead of auto-scaling the original model, we deploy one or more additional heterogeneous small models. Here, we define a small model as one with much smaller resource overheads compared with the original model. When encountering load bursts, we balance the load among these heterogeneous models. This approach allows for a more agile response to varying loads without the extensive resource demands of scaling up a single large model. By carefully distributing queries to these small models, we can significantly accelerate inference with negligible additional memory and energy overheads. Tab. 1 illustrates the novelty of our proposed idea (InferRouter) compared with existing methods. These methods are selected since they are representative and used as baselines in our experiments.

Challenges. Designing an effective load-balancing algorithm for heterogeneous inference models on mobile devices involves two key technical challenges:

TABLE 1: Comparison of our proposed InferRouter and existing methods for serving model inference. InFi [16], FoggyCache [19] and Chameleon [20] are three input filtering approaches, while INFaaS [30] is an auto-scaling approach for ML model serving in the cloud. 

<table><tr><td>Methods</td><td>Load Aware</td><td>Acc. Aware</td><td>Task Agnostic</td><td>Target Devices</td></tr><tr><td>InFi</td><td>✗</td><td>Offline</td><td>✗</td><td>Mobile/Edge</td></tr><tr><td>FoggyCache</td><td>✗</td><td>Offline</td><td>✗</td><td>Mobile</td></tr><tr><td>Chameleon</td><td>✗</td><td>Online</td><td>✗</td><td>Mobile</td></tr><tr><td>INFaaS</td><td>√</td><td>Offline</td><td>√</td><td>Cloud Cluster</td></tr><tr><td>InferRouter</td><td>√</td><td>Online</td><td>√</td><td>Mobile/Edge</td></tr></table>

(1) Online and task-agnostic accuracy1 awareness. While the deployed small models incur lightweight overhead, their inference results may significantly differ from those of the original model. If queries are directed to these small models based solely on load considerations without accurate profiling of their performance, it can lead to substantial accuracy degradation. This is particularly concerning because data distributions in production environments often deviate from those in curated test datasets [38]. Consequently, there exists a considerable gap between the offline profiled accuracy and the actual online accuracy observed during inference. INFaaS [30] proposed a scheduling method for different model variants, but the accuracy of each variant is tested on an offline validation dataset. This will waste a lot of optimization opportunities: the accuracy of small models on some online data may be much higher than the offline test results. Existing works also provide some task-specific approaches for online accuracy profiling, e.g., leveraging geographical and temporal correlations of video streams [20]. However, to support various on-device inference tasks, we need to design a task-agnostic online accuracy profiling method.

(2) High-frequency routing decisions. Real-time inference queries may arrive at a rate of more than 100 queries per second. Therefore, our load balancing needs to be able to make routing decisions at a high frequency. However, for our formulated problem, even with only two models, the overhead of traditional dynamic programming-based algorithms is still too high to be used on mobile devices (over 100 ms on a smartwatch). Such slow routing will even make the inference queue more congested. Worse, the overhead grows exponentially with the number of models, making existing algorithms impractical for on-device inference tasks.

InferRouter. Faced with these challenges, we first use a traffic model based on queuing theory to formulate the load balancing problem for on-device inference. Then we analyze the algorithmic structure of the optimal policy, from which we conclude two key gaps between theoretical results and real-world applications: adaptability and resource feasibility. To bridge these gaps, we propose a task-agnostic accuracy profiling method, a model prioritizing approach that returns provably optimal priorities, and a lightweight heuristic algorithm to make routing decisions. Based on these techniques, we develop InferRouter, a load-balancing system for heterogeneous on-device inference models. InferRouter has online and task-agnostic accuracy awareness and can make high-frequency routing decisions efficiently.

![](images/538e355c67c53a34f685b7c282c3a06fc94b5010e58211519dbf5685cb0b6183.jpg)



![](images/e46d6fa7e03cedff5be81ae23a4ca38dd620ab5d759f8bf61962d8eeb77b5380.jpg)



Fig. 3: Costs and performance of running one model, two model replicas, and two heterogeneous models.

The main contributions of this work are as follows:

• We propose an idea to address load bursts for ondevice inference tasks, that is routing queries to heterogeneous inference models. We analyze the algorithmic structure and present a prioritizing method that is provably optimal.   
• We developed InferRouter, a lightweight load balancing module for on-device inference, with task-agnostic awareness of both model accuracy and load.   
• Evaluations of InferRouter on three representative on-device inference tasks show that InferRouter significantly outperforms complementary state-of-the-art approaches [16], [19], [20] in both accuracy and P99 latency metrics.

# 2 DATA-DRIVEN MOTIVATION

This section introduces our research motivation in a datadriven way. Intuitively, it mainly answers the following four questions:

• Why load balancing is needed for online on-device model inference?   
• Why are cloud-centric auto-scaling methods not suitable for on-device inference?   
• Why do we use heterogeneous small models?   
• How to generate small model(s)?

Observation of inference load bursts. Unlike offline tests, where we can adjust the batch size to optimize performance, serving inference online presents unique challenges due to stochastic query traffic and unpredictable load bursts. For instance, in our analysis of a global bank’s customer service Q&A system, we identified a staggering peak-tovalley load gap of over 45 times, illustrating the extreme variability in demand. Similarly, in our traffic video surveillance system, we found that the peak query frequency for a single edge node can reach 50 frames per second (FPS), while the average load is below 10 FPS. This disparity highlights the inherent unpredictability of real-time inference workloads. Public inference query traces have corroborated these findings, revealing similar stochastic patterns and bursts in query traffic [29]. Such load bursts can cause very high tail latency and thus we need effective load balancing for inference.

![](images/4744dc66c846438607853a0c2504c54e9200a76d1d91656c32e8c18b5c1d66e5.jpg)



(a) MSCOCO Dataset

![](images/e3f4a2bad44a0a75cd366d79d6123a3af258f842aa8ef64a401cfd1f309e1996.jpg)



(b) Surveillance Camera Trace   
Fig. 4: Performance of 14 heterogeneous object detection models on a curated test dataset and real-world IP camera videos.

Scaling model replicas is too costly for mobile and edge devices. Load balancing has been comprehensively studied in data centers [25]–[27] and recent works [22], [28]– [32] have proposed auto-scaling techniques for model inference in cloud clusters. However, the memory and energy costs of scaling model replicas are typically prohibitive for mobile and edge devices. As shown in Fig. 3, running two LSTM replicas incurs more than twice the overhead, which is often unacceptable for mobile devices.

For some queries, small models are fast and accurate. Heterogeneous small models have much fewer resource costs. On a smartwatch, a decision tree model [14] is 61x faster and 9.9x lighter than an LSTM neural network. While on an edge device, an approximate cache [19] achieves 338x throughput and saves 99.8% GPU memory than a BERTbased [39] model. Of course, there is no free lunch for efficiency gain. Both decision tree and cache models bring a certain accuracy drop on the test datasets. Fortunately, we observed that the accuracy drop is dynamic and datadependent: for some input queries, the accuracy loss could be very low. Taking object detection as an example, we test 14 different models and plot their performance in Fig. 4a, from which we can see the obvious difference in overhead and accuracy. However, as shown in Fig. 4b, during processing 24h videos from 10 cameras in parallel, there are many time segments that even the most lightweight model (YOLOv3Tiny-320) has over 99% accuracy.2 And this dynamic is more obvious with finer granularity. As shown in Fig. 5, for the lightweight model, when the segment granularity changes from 1 minute to 10 seconds, its maximum segment-level accuracy increases from 50% to 90%. The higher the maximum segment-level accuracy, the greater the chance that we can save overhead by distributing those queries to lightweight models without compromising accuracy.

Small model(s) can be flexibly generated on demand. Generating smaller, efficient models on demand can be achieved through techniques like quantization, pruning, knowledge distillation, or model slicing. Quantization [40], [41], for instance, reduces the precision of model weights and activations (e.g., from 32-bit floating point to 8-bit integers), significantly lowering memory usage and computational requirements while maintaining acceptable performance. Pruning [13] removes less significant weights or neurons, reducing the model’s size without drastically affecting accuracy. Knowledge distillation [14], [42] involves training a smaller student model to mimic the behavior of the larger teacher model, enabling the smaller model to retain much of the original’s knowledge. Additionally, slicing [43] allows deploying only relevant sub-components of the pre-trained model, tailoring its capacity to specific tasks or resource constraints. These methods provide flexibility in scaling down models without the need for retraining from scratch, ensuring that we are able to find a suitable small model to accompany the original model for inference.

![](images/0368350e34e2b36d045722b9e7d9bc95fff54923a662ab1d62f3ac191ec031f0.jpg)



(a) YOLOv3Tiny-320

![](images/300f67235266882aa30c951045209c2d5ee866bd3d84c80c8e0e3566bfec3913.jpg)



(b) YOLOv3-608   
Fig. 5: CDF of segment-level accuracy with 10s and 1min granularity.

On the feasibility of deploying multiple models. These observations inspire us to design a controller that can dynamically capture the accuracy of different models, so as to distribute data to the appropriate small model when the load surges. InferRouter builds upon the assumption that multiple heterogeneous models are preloaded on the device. This is aligned with many recent trends in model compression and early-exit [24], [44], [45], where developers generate a family of models with different accuracy-latency tradeoffs for adaptive execution. These models are typically derived from a common backbone and share structural similarities, allowing for efficient memory reuse (e.g., via partial weight sharing or layer fusion). In our implementation, the models are statically compiled into the binary and loaded selectively, and we ensure the peak memory usage is within practical bounds. As shown in Fig. 3, on a smartwatch, in addition to the original LSTM model, running an additional DTree model only brings less than 10% additional memory and energy overheads, but can significantly reduce the latency. Thus, InferRouter introduces minimal runtime memory overhead beyond what compressed model ensembles already require.

# 3 FORMULATION AND ANALYSIS

This section defines our load balancing problem, describes the design space, analyzes the algorithmic structure of an optimal policy, and discusses the gap between theory and practice.

# 3.1 Definition

Following prior work on load balancing [27], [46], we formalize the problem as follows. Consider an inference system with K models denoted by $\{ f _ { i } \} _ { i \in [ K ] } ,$ , where [K] is the set $\{ 1 , 2 , . . . , K \}$ . Queries arrive at a single and infinite queue according to a Poisson process with a request rate λ (the number of queries arrived per unit time). Service times of inference models are independent and have a constant service rate $\mu _ { i }$ (the number of queries processed per unit time) for $f _ { i } .$ . Once model $f _ { i }$ completes an inference computation, it returns either a correct inference result with probability $1 - \alpha _ { i }$ , or a wrong inference result with probability $\alpha _ { i } { } ^ { 3 }$ . To ensure stability, we assume that $\begin{array} { r } { \sum _ { i \in [ K ] } \bar { \mu } _ { i } > \lambda , } \end{array}$ otherwise, the long-run average latency is infinite [47]. We follow the First-In-First-Out queuing discipline.

The performance metrics of interest are (1) latency, i.e., the expected sojourn time (waiting time plus processing time), denoted by E(S), and (2) accuracy. Let $T _ { i }$ denote the ratio of queries that are distributed to model $f _ { i } .$ Then the average error rate can be calculated by $\textstyle \sum _ { i \in [ K ] } \alpha _ { i } T _ { i }$ .

To achieve an adjustable trade-off between minimizing the latency and maximizing the accuracy, we formulate a two-objective optimization problem. Since the error rate and latency can easily be normalized and the policy space is convex [48], we adopt the weighted-sum method that is widely used in multi-objective optimizations [49] as follows:

$$
\min \left(\sum_ {i \in [ K ]} \alpha_ {i} T _ {i} + c E (S)\right), \tag {1}
$$

where the coefficient $c \ ( c \geq 0 )$ adjusts the relative importance given to the sojourn time compared to the error rate. Through adjusting the coefficient $c ,$ different preferences can be expressed flexibly by developers. Our problem formalization is the first attempt to consider both load awareness and accuracy awareness for on-device model inference.

# 3.2 Design Space

We make several assumptions to claim our design space.

Pre-loaded models. We assume that all models are preloaded into memory prior to inference, eliminating the overhead associated with loading and unloading models during runtime. This approach ensures no additional computational or latency cost, as queries can be efficiently routed to the preloaded model without waiting for it to load. By keeping all models readily available, the system can focus solely on selecting the best-suited model for each query based on resource and accuracy requirements.

Non-anticipating policy. To handle load bursts in realworld services, we assume that the queries are unpredictable. Thus the load balancing algorithm should be reactive, rather than predictive. Previous work on autoscaling [28] in data centers have shown that the reactive policy can surpass predicative ones in both efficiency and robustness.

Non-interchangeable computation. Unlike general job processors that can continue subsequent computations left by others [27], model inference is typically not interchangeable. For example, a decision tree and an LSTM model share no intermediate results. So we assume a noninterchangeable processing mode, otherwise, the queueing

3. Parameters α may change dynamically in real applications, and we propose an accuracy profiling method in Sec. 4.1 to update them for just-in-time adaptability.

TABLE 2: Summary of Notations 

<table><tr><td colspan="2">Parameters</td></tr><tr><td> $K$ </td><td>number of models ( $i \in \{1, ..., K\}$ )</td></tr><tr><td> $f_i$ </td><td>inference model- $i$ </td></tr><tr><td> $\lambda$ </td><td>request rate</td></tr><tr><td> $\mu_i$ </td><td>service rate of model- $i$ </td></tr><tr><td> $\alpha_i$ </td><td>error rate of model- $i$ </td></tr><tr><td> $T_i$ </td><td>ratio of queries assigned to model- $i$ </td></tr><tr><td> $c$ </td><td>coefficient of relative importance</td></tr><tr><td colspan="2">Markov Decision Process</td></tr><tr><td> $x$ </td><td>number of queries in the queue</td></tr><tr><td> $W$ </td><td>subset of working models ( $W \subseteq [K]$ )</td></tr><tr><td> $V_n$ </td><td>state transition function over  $n$  steps</td></tr><tr><td> $U_n$ </td><td>action function over  $n$  steps</td></tr></table>

model can be converted to a single-model with an adjustable service rate [50].

Gold standard assumption. In real-world applications, it is common to have an inference model that has satisfactory accuracy before deployment. Therefore, we assume, like previous work [16], [20], the existence of a gold-standard model, which is generally the original model that has been deployed. We regard the outputs of the gold-standard model as ground-truth results, i.e., zero error rate.

# 3.3 Algorithmic Structure of Optimal Policy

We formulate the defined load balancing problem as a Markov decision process. Let x denote the number of queries in the queue, $x \ge 0$ . We define the state of the inference system as the set of working models. For example, {1, 3} is a state where models $f _ { 1 } , f _ { 3 }$ are working and the others are idle. At every moment when at least one query waits in the queue and one model is idle, the controller can take an action: either distribute a query to an idle model or keep the query waiting. We formulate value functions over n steps with state transitions $( V _ { n } ( \cdot , \cdot ) )$ and actions $( U _ { n } ( \cdot , \cdot ) )$ separated. Let $\begin{array} { r } { P = \lambda + \sum _ { i \in [ K ] } \mu _ { i } . } \end{array}$ . The state transition function:

$$
\begin{array}{l} V _ {n + 1} (W, x) = \frac {c}{\lambda} (x + | W |) \\ + \sum_ {i \in W} \left(\frac {\mu_ {i}}{P} \left(U _ {n} (W \setminus \{i \}, x) + \alpha_ {i}\right)\right) \\ + \frac {\lambda}{P} U _ {n} (W, x + 1) \\ + \sum_ {i \in [ K ] \backslash W} \left(\frac {\mu_ {i}}{P} U _ {n} (W, x)\right), \\ \end{array}
$$

where $W ~ \subseteq ~ [ K ]$ denotes the subset of working models. Intuitively, the first part is the holding cost of queries in the system until the next query arrives. And three events can happen with different probabilities and transit the state: (1) One working model $( { \dot { f } } _ { i } , i \in W )$ finishes its inference. The probability is $\mu _ { i } / P$ and the working subset changes to $W \setminus \left\{ i \right\}$ . The finished inference brings $\alpha _ { i }$ error cost. (2) One query arrives with probability $\lambda / P . \breve { ( 3 ) }$ Idle models make no changes to the system state. These three events correspond to the last three parts in the $V _ { n }$ function. An optimal controller should take the available action that minimizes the objective value $( \mathrm { E q . ~ } 1 )$ . So we define the action function as follows:

$$
U _ {n} (W, x) = \min _ {A \subseteq ([ K ] \backslash W), | A | \leq x} V _ {n} (W \cup A, x - | A |).
$$

The controller needs to decide which subset of x queries should be distributed to currently idle models. Tab. 2 summarizes notations used in problem definitions and MDP analysis.

Iterating the two-step value functions forms a dynamic programming (DP) algorithm, which is optimal when the value converges as n tends to infinity. When $K = 2 ,$ it has been proved that the optimal routing policy is of threshold type [46], i.e., there exists a threshold $u \left( u > 0 \right)$ on the queue length x such that:

• $\mathrm { I f } \ x < u ,$ the optimal action is to choose one prioritized model to process queries and the other model with lower priority remains idle;   
• If $x \geq u ,$ the optimal action is to have both models work.

For cases with $K > 2 ,$ the algorithmic structure is an open problem. Fortunately, with gold-standard assumption, we can decompose the problem with any K into $\hat { K } - 1$ 2-model sub-problems (see Sec. 4.2 for details) thus the threshold structure still holds.

# 3.4 Theory-Practice Gap

The above theoretical analysis helps us understand the algorithmic structure of the optimal load-balancing controller. However, there are two major gaps that need to be bridged.

(1) Adaptability. In real systems, parameters required by the DP policy (e.g., query arrival rate and error rates of models) are typically dynamic, thus a set of instrumentation is required to monitor them. The arrival rate can be efficiently estimated by off-the-shelf monitoring tools [51], while existing work has not studied how to monitor the dynamic accuracy of heterogeneous inference models. Naively, we can offline profile the initial accuracy of deployed models, just as INFaaS [30] did. But our experimental results show that such an offline accuracy profile quickly becomes suboptimal in an online serving system (see Fig. 10).

(2) Resource efficiency on mobile. Although we already know that the optimal policy is of threshold type, there is no simple criterion to prioritize models and no closedform expression for the threshold u on queue length [46]. The DP-based method has to iterate the value functions until convergence to get the exact optimal priorities and threshold. When scaling to more models, the search space increases exponentially with the number of available models. The iteration process needs to re-execute once any involved parameter (e.g., model accuracy and queue length) changes, which will become prohibitive in online inference serving. Our experiments show that the time overhead of this iterative process easily exceeds an acceptable latency, e.g., over 100 ms on a smartwatch with only two models.

# 4 INFERROUTER DESIGN

This section presents the detailed design of InferRouter. As shown in Fig. 6, InferRouter maintains a queue of online queries and has three main modules: (1) A load balancing algorithm (§ 4.3) that decides which inference model(s) to send each query to; (2) An accuracy profiler (§ 4.1) that updates the error rate of inference models; (3) A model prioritizer (§ 4.2) that considers both the system state and user demands (accuracy-latency preference c and gold-standard model index i∗) to prioritize heterogeneous inference models.

![](images/bcb3565bfcc6581ce1a3f4b894be9088c161ae749705f976b3648b03d3f6691f.jpg)



Fig. 6: Overview of InferRouter. The user demand consists of accuracy-latency preference c and the user-specified index of gold-standard model i∗.

# 4.1 Accuracy Profiling

We design the accuracy profiling to be feedback-based and in an anti-idling way that does not compromise the latency.

Feedback-based. The inherent reason for dynamic accuracy is the distributional discrepancy of online queries [38]. One direct way to capture the dynamics is using the side information, like the wall-clock time and geographical location [20]. For example, there are fewer vehicles in the video late at night, so the accuracy of the low-resolution model is very close to that of the high-resolution model. However, side information-based approaches have poor generality and cannot support ubiquitous inference tasks. Another series of approaches is input-based, which profiles the dynamic performance based on handcrafted [17] or deep features [52] of input. However, these pre-processing approaches depend on input modality and require expensive feature engineering. Motivated by the success of feedback control systems [53], we design a feedback-based (or output-based) approach that profiles the dynamic accuracy of inference models based on their outputs. Specifically, we calculate the ratio of the outputs that are consistent with the gold standard as the accuracy of a model. Note that we aim to profile the accuracy in the current time window for just-in-time adaptability, instead of the overall accuracy.

Anti-idling. Intuitively, our policy aims to avoid model idleness as much as possible without compromising the latency of future queries. Unlike traditional load balancing tasks [25], [27], where distributing the same query to multiple servers has no benefit other than duplicated outputs, in our task, the inference results on the same queries can be used for accuracy profiling. So we design an anti-idling accuracy profiling (AAP) method. Specifically, when the gold-standard model is chosen to process a query, AAP sends the query to models that satisfy two conditions: (1) the model is idle; (2) the model has a higher service rate than the current arrival rate. The second condition comes from the idea that these models are expected to finish processing before the next query arrives. This anti-idling idea has demonstrated effectiveness in optimizing bandwidth usage, e.g., AWStream [54] opportunistically profile accuracy only when there is spare bandwidth. Experimental results show that our AAP method achieves effective adaptability to dynamic accuracy without compromising latency.

# 4.2 Model Prioritizing

The threshold-type algorithmic structure first requires a prioritized list of inference models. Existing work [46] show that the priorities do not depend on queue length and arrival rate. But there is no simple closed-form expression and we have to iterate the DP process until convergence. Worse yet, the complexity increases exponentially with respect to the number of models. Our opportunity to address these difficulties lies in the gold-standard assumption, by which we can prove the following lemma by induction and decompose a K-model prioritizing problem into $( K - 1 )$ gold-pair prioritizing (GPP) sub-problems.

Lemma 1. Given two models $f _ { 1 } , f _ { 2 }$ with $\alpha _ { 1 } = 0$ (assume $f _ { 1 }$ is the gold-standard model), the following function

$$
p (i) = \alpha_ {i} + \omega (\mu_ {1}) c / \mu_ {i} \tag {2}
$$

provides an optimal priority measure, where ω is a scalar that only depends on $\mu _ { 1 }$ .

Proof. Since the priorities do not depend on the queue length, we set $x \ = \ 0$ . Given $K = 2 ,$ , the value function of selecting the two models is as follows:

$$
V _ {n + 1} (\{1 \}, 0) = \frac {c}{\lambda} + \frac {\mu_ {1}}{P} (V _ {n} (\emptyset , 0)) + \frac {\lambda + \mu_ {2}}{P} V _ {n} (\{1 \}, 0)
$$

$$
V _ {n + 1} (\{2 \}, 0) = \frac {c}{\lambda} + \frac {\mu_ {2}}{P} (V _ {n} (\emptyset , 0) + \alpha_ {2}) + \frac {\lambda + \mu_ {1}}{P} V _ {n} (\{2 \}, 0)
$$

To prioritize them, we care about the boundary condition where choosing both models has the same value. With the initial value ${ \cal V } _ { n } ( \emptyset , 0 ) = 0 ,$ , we have:

$$
\begin{array}{l} 0 = V _ {n + 1} (\{1 \}, 0) - V _ {n + 1} (\{2 \}, 0) \\ = - \frac {\mu_ {2} \alpha_ {2}}{P} + \frac {(\lambda + \mu_ {2}) V _ {n} (\{1 \} , 0) - (\lambda + \mu_ {1}) V _ {n} (\{2 \} , 0)}{P} \\ \end{array}
$$

When the value function converges, the boundary condition also holds for $V _ { n } , { \mathrm { i . e . , ~ } } V _ { n } ( \{ 1 \} , 0 ) = V _ { n } ( \{ 2 \} , 0 )$ . So we have $0 = - \mu _ { 2 } \alpha _ { 2 } + ( \mu _ { 2 } - \mu _ { 1 } ) V _ { n } ( \{ 1 \} , 0 )$ , from which we can see that priorities do not depend on λ. If function $p ( i )$ holds for $n , \mathrm { i . e . , } V _ { n } ( \{ 1 \} , 0 ) = \alpha _ { 1 } + \omega c / \mu _ { 1 } ,$ then we have $0 = - \alpha _ { 2 } \mu _ { 2 } +$ $\begin{array} { r } { \frac { \mu _ { 2 } } { \iota \iota _ { 1 } } \omega c - \omega c , } \end{array}$ and prio $\begin{array} { r } { V _ { n + 1 } ( \{ 1 \} , 0 ) - V _ { n + 1 } ( \{ 2 \} , 0 ) = ( \frac { \omega c } { \mu _ { 1 } } ) - ( \alpha _ { 2 } + } \end{array}$ $\frac { \omega _ { c } } { \mu _ { 2 } } \Big )$

The weight $\omega ( \mu _ { 1 } )$ only depends on the service rate of the gold-standard model and can be found by offline searching. Experimental results show that using only one offline point to fit, our GPP can generate optimal priorities.

Linear scaling. For the general K-model problem, we decompose it into (K−1) 2-model sub-problems, comparing the gold standard with the other $K \bar { \bf \Phi } - 1 \bar { \bf \Phi }$ models. Since ω only depends on the gold standard’s service rate, priorities calculated by $p ( i )$ have a total order (any two elements are comparable).

# 4.3 Threshold Control

After prioritizing inference models, the next is to control the threshold u. Compared with prioritizing, the threshold control task depends on two more parameters: queue length and arrival rate. We found that the dependency roots in the contribution of waiting time in the objective function. In Eq. 1, the first part $\sum _ { i \in [ K ] } \alpha _ { i } T _ { i }$ considers the error rate.

![](images/4c3edce26233366c0468213b3ce36e8f3ae909c8d394f6d3acf9acf63df04c15.jpg)



(a) Waiting-Based

![](images/02145eea2c1013e7f860f867db1eaafbb85f7f1968a1f3b9388a74e0af664fd7.jpg)



(b) RL-Based   
Fig. 7: Threshold control methods. InferRouter uses the waiting-based method by default.

The second part is the expected sojourn time, which consists of the waiting time in the queue and the service time by models. Since the service time only depends on $\mu _ { i } ,$ the dependency on x, λ lies in the waiting time.

Definition 1 (Activated models). We define the set of top $k \leq K$ prioritized models as k activated models A(k).

Given x queries in the queue and k activated models are idle, the average waiting for the x queries is $( 0 + 1 + . . . + ( x - 1 ) ) / ( \bar { x } \mu _ { [ k ] } ) = ( \bar { x } - 1 ) / 2 \mu _ { [ k ] } .$ . The service rate $\mu _ { [ k ] }$ is the average value of k activated models, i.e., $\begin{array} { r } { \mu _ { [ k ] } \ = \ \frac { 1 } { k } \sum _ { f _ { i } \in \mathcal A ( k ) } \mu _ { i } . } \end{array}$ . Take the arrival rate into account, by the Pollaczek–Khinchine formula [55], the additional waiting time is $( \lambda / \mu _ { [ k ] } + \lambda \mu _ { [ k ] } V a r ) / ( 2 ( \mu _ { [ k ] } - \lambda ) )$ , where V ar is the variance of service time. In our formulation, the service time is a constant (zero variance), so that it is simplified to $\lambda / ( 2 \mu _ { [ k ] } ( \mu _ { [ k ] } - \lambda ) )$ , which only holds when $\mu _ { [ k ] } \ > \ \lambda$ . However, in practice the condition cannot be always satisfied, so we smooth this with a Sigmoid-like function: $\tau / ( 1 + e ^ { \mu _ { [ k ] } - \lambda } )$ . So we define the waiting time as follows:

$$
w (k) = \frac {x - 1}{2 \mu_ {[ k ]}} + \frac {\tau}{1 + e ^ {\mu_ {[ k ]} - \lambda}}. \tag {3}
$$

We propose to use the parameter τ as the threshold on the waiting time to control the number of activated models. So the boundary condition is $w ( k ) = \tau ,$ , from which we can get the threshold on the queue length:

$$
x = \frac {2 \mu_ {[ k ]} \tau}{1 + e ^ {\lambda - \mu_ {[ k ]}}} + 1. \tag {4}
$$

τ can be set manually as the maximal allowed waiting time.

At any control event, we check the boundary conditions using the current models and one less model. Note that the boundary is monotonic with respect to the number of activated models. So we have three disjoint cases: (1) If the current waiting time exceeds the threshold, i.e., $w ( k ) > \tau ,$ then we add one more model to use; (2) If $w ( k - 1 ) \leq \tau ,$ We use one less model to use; (3) Otherwise we keep using the current models. See Fig. 7a for an illustration of state transitions. We call the above method as waiting-based.

Learning-based. We noticed that recent work explored reinforcement learning-based (RL) approaches for network load balancing, including fog networks [56], SDN [57] and so on. However, for end-to-end load balancing, the action space is typically the fixed set of models. So it requires retraining when changes occur (e.g., a new model comes or

Algorithm 1: InferRouter Load Balancing   
input: query queue Q, the number of activated models k, gold standard index i*

when query q arrives do
    /* Waiting-Based Threshold Control */
    if w(min(1, k-1)) ≤ τ then
    k ← min(1, k-1);
    else
    if w(k) > τ then k ← max(K, k+1);
    i' ← arg max_{i∈A(k),Idle(f_i)} p(i);
    send q to model f_{i'};
    if i = i* then
    /* Anti-Idling Accuracy Profiling */
    for j ∈ [K] do
    if Idle (f_j) and μ_j ≥ λ then
    send q to model f_j;

when model f_i returns do
    if i = i* then
    collect matched results and update accuracy;
    /* Gold-Pair Prioritizing */
    re-prioritize models by p(i);
    if Q is not empty then
    q ← Q.dequeue();
    distribute q using the first when procedure;

a model fails), resulting in poor flexibility and scalability. We reformulate the problem under our threshold-type structure and only use RL to control the number of activated models. Fig. 7b shows the workflow. We define three actions: one less model, keep the current model, one more model. We use a multi-layer perception as the agent. The reward is set as the change value of the objective function (Eq. 1). Although this design overcomes the scalability issue, experimental results show that it does not work properly when traffic patterns change. As shown in Fig. 12, given a traffic pattern that is different from training samples, the RL-based controller performs a poor trade-off, resulting in high latency. Based on reformulated action space, the proposed controller designs have the ability to continue working when one or more models fail and are elastic to expand. InferRouter uses the waiting-based approach by default, considering its advantages in robustness and efficiency.

Adaptive batching. The term batch size refers to the number of samples fed into the model in one inference round. Adaptively adjusting the batch size can improve the inference throughput by amortizing the memory-reading overheads across more queries [58]. However, adaptive batching is not perfect for real-time applications [59], since it will substantially increase latency. We adopt an adaptive batching policy in InferRouter: We first test the latency using different batch sizes offline; Then we greedily use the batch size that minimizes the average waiting time for online serving.

TABLE 3: Summary of experimental setup: applications, data modalities, devices, and inference models. 

<table><tr><td>Application</td><td>Modality</td><td>Device</td><td>Original Model</td><td>Small Model(s)</td></tr><tr><td>Mobile Action Recognition</td><td>Motion Signal</td><td>Smartwatch</td><td>LSTM</td><td>Knowledge Distilled DTree</td></tr><tr><td>Traffic Video Analytics</td><td>IP Camera Video</td><td>Jetson Orin</td><td>YOLOv5x6-1280</td><td>YOLOv3-320/608, YOLOv5-640</td></tr><tr><td>Customer Service Q&amp;A</td><td>Natural Language</td><td>Edge Device</td><td>BERT</td><td>KNN-based Approximate Cache</td></tr></table>

# 4.4 Putting It All Together

Once a query arrives, InferRouter first determines whether the expected waiting time exceeds the threshold. If not, use one less model, otherwise add one more model. Then, the model with the highest priority is selected to process the query. If the selected model is the gold standard, the query will be sent to other models that are currently idle. These duplicated inference results are used to update the accuracy profiles. After updating the accuracy profiles, InferRouter will re-prioritize models. Alg. 1 demonstrates the complete process of InferRouter.

# 5 EVALUATION

We evaluate InferRouter prototype on mobile and edge inference workloads using real traces and public datasets.

# Our highlights are as follows:

• InferRouter outperforms state-of-the-art methods by 5.9% higher inference accuracy and 5.8× better P99 latency.   
• InferRouter is robust to involved variables including window length, accuracy dynamics, and importance coefficient.   
• InferRouter shows its advantages in saving resources compared with auto-scaling and offloading approaches.

# 5.1 Implementation

We implemented InferRouter in Python using a clientrouter-servers architecture. We use gRPC for communication among the user client, InferRouter, and model servers. The client simply sends data queries to the router, and Infer-Router maintains a single input queue in its main process. In our experiments, we use gRPC to encapsulate an API call interface for each model server. Mainstream model-serving software, such as TensorFlow Serving and Triton Inference Server, typically supports RPC and RESTful APIs to expose the inference function. InferRouter can seamlessly work as a plug-in to existing model serving systems, as long as Infer-Router can connect to their inference APIs. Developers only need to configure the addresses of RPC/RESTful APIs and the original ML program needs no modification. On Linux devices, inference models can run in Docker containers and virtual machines. On Android devices, we created the package using Kivy Python-for-Android [60] and converted ML models using TensorFlow Lite.

# 5.2 Experiment Setup

Our evaluation covers InferRouter in use with three representative on-device ML applications: human action recognition on mobile devices (mobile HAR), vehicle counting in videos (edge VC), and question-answering (BankQA). Tab. 3 summarizes the setup for these three applications.

Datasets. We used three datasets, covering three data modalities: motion signal, IP camera video, and natural language text. (1) UCI HAR [61], a motion signal dataset collected by 30 subjects who performed six actions while carrying a smartphone. (2) City Intersections. For the edge vehicle counting application, we collected 10x24 hours of 1FPS videos from 10 cameras installed at different intersections in a city. (3) Bank QA. We used a one-day question answering trace from a global bank’s intelligent customer service system. The trace consists of 152,212 user queries and 2670 types of answers.

Inference models. We built heterogeneous inference models using three different mechanisms. (1) For mobile HAR, we trained an LSTM model as the gold-standard model. Then we adopted a knowledge distillation [14] approach to train a decision tree (DTree) as the second inference model. (2) For edge VC, we deployed four offthe-shelf object detection models pre-trained on MSCOCO datasets [62] with different configurations (model architecture and input resolution). 3) For BankQA, we used the BERT-based [39] neural network running in the production environment as the gold-standard model. The BERT-based model was fine-tuned on manually labeled business-related training data. And we deployed a KNN-based cache as the second inference model.

Devices. In order to verify the wide applicability of our design, we tested InferRouter on three different devices. (1) For mobile HAR, we used a Huawei Watch. The average inference speeds of LSTM and DTree models are 31.5 and 19230.8 queries per second (qps). The two models take 437KB and 40KB RAM. (2) For edge VC, we used an NVIDIA Jetson AGX Orin development board. Using a batch size equal to one, the deployed four object detectors perform 312.5 (v3Tiny-320), 38.3 (v3-608), 21.7 (v5x-640), and 9.1 (v5x6-1280) FPS. And their memory footprints range from 17MB to 270MB. (3) For BankQA, we used an edge device (12 Intel Xeon ES-2650 v4 CPUs, one NVIDIA Tesla P100 GPU) that runs Ubuntu 16.04. On average, the throughput of BERT and Cache models are 2.9 and 980.3 qps, which take 1680MB and 0.36MB RAM.

Baselines. To the best of our knowledge, no existing system provides load balancing on heterogeneous inference models like InferRouter. For a fair comparison, we selected state-of-the-art on-device inference approaches dedicated to certain applications. Specifically, we compared InferRouter to the following methods:

(1) InFi [16]: an input filtering approach that trains a binary classifier to decide whether to execute the model inference computation. We used InFi on the mobile HAR task and trained one classifier for the LSTM model.   
(2) Chameleon [20]: a pipeline selection approach for video analytics. The configuration knobs are model architectures (v3Tiny, v3, v5x, v5x6) and image resolutions (320, 608, 640, 1280) We applied Chameleon in the edge VC task.

(3) FoggyCache [19]: an approximate caching approach that uses a kNN-based algorithm to search for the reusable inference results stored in a cache. FoggyCache designs a confidence measurement (called homogeneity factor) for kNN and decides cache hit/miss by setting a threshold on the confidence score.   
(4) Auto-scaling (INFaaS [30]): We adopt the auto-scaling method but assume it can perfectly predict the arrival rate, that is, scaling models by taking the future arrival rate as known information.   
(5) Offloading: we deploy the inference model on the GPU edge, while the smartwatch offloads queries to the edge.

Metrics. We measure InferRouter and compare it with baselines using five standard metrics:

• Accuracy is used to evaluate the inference output. The accuracy is defined as the ratio of obtained outputs that are consistent with the gold-standard model’s outputs. Since the runtime groundtruth cannot be obtained after the model is deployed, this metric based on the consistency of model output is widely adopted in existing work [16], [20], [30].   
• P99 latency refers to the 99th percentile of latency measurements of all queries. InferRouter is mainly designed to optimize this metric.   
• Avg. latency is calculated by summing the total time taken for all queries and then dividing by the number of queries.   
• Peak memory footprint refers to the maximum amount of memory allocated during inference at any given time.   
• Energy consumption is measured as the energy cost (mJ) per inference query. InferRouter is designed for mobile devices, so energy efficiency is an important indicator that affects whether it can be applied to weak devices.

# 5.3 Overall Performance

We first compared InferRouter with state-of-the-art methods on several overall metrics: 99th-percentile (P99) latency, average latency, and average accuracy. Tab. 4 shows that, InferRouter outperforms baselines in all three applications in terms of P99 latency and average accuracy metrics. For InFi, Chameleon, and FoggyCache, we set the accuracy SLO as 90%, while for InferRouter, we normalized the latency values into 0 to 1 and set c as 1. To estimate the potential variance due to system-level non-determinism (e.g., interprocess communication), InferRouter performs 30 repeated runs of the measured latencies. The resulting 95% confidence intervals are extremely narrow, e.g., in edge VC, the P99 latency of InferRouter is 0.496881s ± 0.000256s and the average latency is 0.304648s ± 0.000041s. Since the variance does not affect the conclusion, we do not report all the data in Tab. 4 to save space. For the mobile HAR, compared with InFi, InferRouter decreases 85.2% P99 latency (5.8x faster) and improves 5.9% accuracy. For the edge VC, compared with Chameleon, InferRouter takes only 0.38% P99 latency (262.1x faster) while achieving 0.1% higher inference accuracy; For the BankQA, compared with FoggyCache, InferRouter achieves 4.5% higher accuracy and decreases 7ms P99 latency. Only for the BankQA task, InferRouter has a higher average latency. The reason is obvious: InferRouter tends to use the BERT-based model for higher accuracy when the load is light, bringing relatively higher latency than using the cache.

TABLE 4: Overall Performance on Different Applications 

<table><tr><td>Method</td><td>P99 Lat.</td><td>Avg. Lat.</td><td>Peak Mem.</td><td>Acc.</td></tr><tr><td colspan="5">Mobile HAR</td></tr><tr><td>InFi</td><td>0.707s</td><td>0.042s</td><td>457 KB</td><td>92.6%</td></tr><tr><td>Auto-Scale</td><td>0.031s</td><td>0.031s</td><td>3209 KB</td><td>100%</td></tr><tr><td>InferRouter</td><td>0.104s</td><td>0.041s</td><td>480 KB</td><td>98.5%</td></tr><tr><td colspan="5">Traffic Video Analytics</td></tr><tr><td>Chameleon</td><td>119.1s</td><td>27.5s</td><td>574 MB</td><td>95.7%</td></tr><tr><td>Auto-Scale</td><td>0.11s</td><td>0.11s</td><td>2160 MB</td><td>100%</td></tr><tr><td>InferRouter</td><td>0.496s</td><td>0.304s</td><td>574 MB</td><td>95.8%</td></tr><tr><td colspan="5">NLP Question Answering</td></tr><tr><td>FoggyCache</td><td>0.59s</td><td>0.144s</td><td>1680 MB</td><td>93.9%</td></tr><tr><td>Auto-Scale</td><td>0.34s</td><td>0.34s</td><td>5040 MB</td><td>100%</td></tr><tr><td>InferRouter</td><td>0.583s</td><td>0.293s</td><td>1680 MB</td><td>98.4%</td></tr></table>

Comparison with auto-scaling. Another way to deal with the dynamic load is auto-scaling, which adaptively adjusts the number of parallel service instances. We applied a vanilla auto-scaling method that scales the original model according to the current instrumented arrival rate. As shown in Tab. 4, experimental results show that, Auto-Scale method costs significantly higher peak memory, which is not feasible on mobile devices.

Improvement brought by load awareness. Compared with these approaches, only InferRouter has load awareness, thus InferRouter avoids serious latency accumulation when facing bursty loads. For accuracy profiling, the three baselines design ad-hoc approaches, e.g., the homogeneity factor used in FoggyCache, while InferRouter leverages the feedback-based accuracy profiling. The resulting gains in accuracy show that our profiling method can make more timely responses thus enabling InferRouter to make better load-balancing decisions.

# 5.4 Integration with Complementary Methods

Several existing approaches have been proposed to optimize inference latency from various perspectives. LegoDNN [36] adapts DNN execution under arbitrary latency constraints via dynamic model slicing. BAND [63] and Niagara [64] improve end-to-end inference latency in distributed settings. Apparate [45] dynamically adjusts early-exit thresholds to meet latency SLOs during runtime. Our proposed method, InferRouter, is orthogonal to these approaches. It focuses on load-aware online query routing and can serve as a complementary component in these frameworks. We present two case studies to demonstrate this complementarity: LegoDNN + InferRouter and Apparate + InferRouter.

LegoDNN+InferRouter. Following the experimental setup of LegoDNN, we conduct experiments on three datasets with common CV models: CIFAR10 with VGG16, ImageNet2012 with ResNet18, and COCO2017 with YOLOv3. We compare three configurations: (1) DNN (sparsity=0.0): Standard full-precision model without compression. (2) DNN (sparsity=0.5): Model compressed via LegoDNN’s structured pruning. (3) LegoDNN+InferRouter: Our system dynamically routes queries to either the full or compressed model based on current load. As shown in Fig. 8, this integration effectively mitigates latency spikes under load surges, while maintaining high prediction accuracy. Across all datasets, accuracy degradation compared to full DNN remains modest (only 1.5–4.7%, see Fig. 8d).

![](images/48d55dbd98494de14305992009d399565978fc2967a51cd57f162ed78b5819b1.jpg)



(a) CIFAR10 (λ=7.0)

![](images/0518efc38ee0321545384b7861496e22fdc7c38de7c2b4fe8c7780e4d5ad5deb.jpg)



(b) ImageNet2012 (λ=4.0)

![](images/05a5e6bf0ea1b6c51c8f482246d0fe5325cda714706062b232c2eaee6119174f.jpg)



(c) COCO2017 (λ=3.5)

![](images/371870c75ffaf405c208b30794e635a5f026bef4f8f1585b923d93585aee4c05.jpg)



(d) Acc. Summary

Fig. 8: InferRouter can complementarily work with LegoDNN to provide online load awareness. λ denotes the request rate.   
![](images/b16331b74335872aeaeb010808605cbfe434039a79f7f604f420eb7e882990da.jpg)



(a) DistilBERT (λ=11)

![](images/55ca4631bd6b19294f32b4ab0a2435445f8162f5fc5179e820121eb10a17bf88.jpg)



(b) BERT (λ=2.5)

![](images/719e4baea67b32a3b7b656de7eaac7c3c9dd6d8166d0d781ccaeb19f8ed32ad4.jpg)



(c) GPT2 (λ=1)

![](images/2f3b48684433fa79e43121cd9f33ad36cc219117fb9888b9b326841b352293b2.jpg)



(d) Acc. Summary   
Fig. 9: InferRouter can complementarily work with Early-Exit methods (e.g., Apparate) to provide online load awareness. λ denotes the request rate.

Apparate+InferRouter. We further integrate InferRouter with Apparate for early-exit optimization. We select three representative NLP models: DistilBERT, BERT, and GPT2. Using Apparate, we construct two early-exit pipelines per model, denoted as EE-1 and EE-2, providing faster but less accurate inference paths. We then apply InferRouter to route queries among the full model and the two earlyexit versions based on system load. As shown in Fig. 9, Apparate+InferRouter consistently achieves the lowest p99 latency under load surges—less than 3s, compared to over 10s with a fixed early-exit strategy. Fig. 9d further confirms that the accuracy trade-off is minimal (0.4–2% degradation), demonstrating the practicality of integrating our router with latency-adaptive models.

Benefit of introducing model-level load balancing. A key contribution of InferRouter lies in achieving model-level load balancing among heterogeneous models. While load balancing at this level may not always directly reduce the instantaneous end-to-end latency, it plays a crucial role in handling dynamic workloads, especially during traffic bursts. Existing dynamic inference methods, such as LegoDNN or Apparate, are designed for latency adaptability but typically assume fixed offline configurations or latency SLOs. These methods do not account for real-time load variations during deployment. InferRouter is orthogonal and complementary to them: it introduces load awareness into the inference pipeline, allowing more robust and adaptive model selection under varying traffic conditions.

# 5.5 Micro-benchmarks

We now present the evaluation of three modules separately.

Accuracy profiling. For a modular evaluation of accuracy profiling, we applied three load balancing policies that do not depend on accuracy as follows: (1) Flooding. Distributing queries to every inference model. Thus it can collect matched inference results for every query and profile exact accuracy.

(2) Round robin with initial profiling. Initially profiling accuracy using flooding policy then distributing queries to each inference model in turn. Thus it keeps using the initial accuracy profile and cannot update it.   
(3) Round robin with AAP. Combining round robin policy with the proposed anti-idling accuracy profiling method. Recall that, AAP sends queries that are assigned to the goldstandard model to idling models if they are expected to finish the inference before the next query comes.

We did simulation experiments with two inference models, one as the gold standard and the other returning correct results with time-varying probability. As shown in Fig. 10, although the flooding policy profiles the exact accuracy pattern, it brings high inference latency. The accuracy pattern captured by our AAP is close to the exact one and the AAP has a negligible impact on latency. The average latency using round robin with AAP is 71.5 ms, which is greatly less than the flooding policy (1979 ms). And the average accuracy over all queries captured by AAP is the same as the flooding, both are 30%. On the other hand, the initial profiling result is 82.5% accuracy. A such biased profile will lead to unwise accuracy-aware load balancing decisions.

Sensitivity to the window length. AAP estimates the accuracy using the latest l (window length) matched results. We tested different values of l from 1 to 100 and experimental results show that a longer window returns more smooth profiles, resulting in a less speculative policy. InferRouter sets l = 10 by default unless otherwise specified.

![](images/5ceace72b5a20bcd329c20ce907514c0d0e183b7e0592c1f364c41417a669c9e.jpg)



(a) Accuracy Profiling Trace

![](images/e363c6de9e7961d739528977c2650db33eb4386a54b85c29ddf3d93ed4df961c.jpg)



(b) Query Latency

Fig. 10: Performance of anti-idling accuracy profiling on two-model workload with simulated query trace.   
![](images/ccc8aad4cbee8f28937fd16367989ac04572ec2c6caf698a7a2976bc2e1c544e.jpg)



(a) Fix c = 1

![](images/202c94607a501d2791c7e4a0d27b48083278354848473235a6511e4fab7d0194.jpg)



(b) Fix α2 = 0.1   
Fig. 11: Gold-pair prioritizing generates provably optimal results. DP denotes the dynamic programming-based optimal priorities.

Profiling multiple sources with adversarial performance. An inherent assumption of feedback-based profiling is the stability of performance over a period of time. We generated two input sources that have adversarial accuracy patterns, i.e., the sum of the error rates on the two sources over a period of time is 1, and fed them to the same input queue for inference. Obviously, this adversarial trace renders the AAP method ineffective. In real applications, domain shifts of different data sources may pose a similar problem. We can solve it by simply using InferRouter for each source independently, but this solution loses global load awareness. Profiling methods that can handle multisource inputs with adversarial accuracy patterns are our future work.

Model prioritizing. We now show that our gold-pair prioritizing (GPP) generates the optimal model priorities, as we have proved in Lemma. 1. Setting the 1st model as the gold standard, i.e., $\alpha _ { 1 } = 0$ and we adjusted its service rate $\mu _ { 1 }$ . We fit the parameter ω using only one optimal point. By Eq. 2, we have the equation: $\begin{array} { r } { \mu _ { 2 } = \frac { { \bf { \bar { \omega } } } \omega c \mu _ { 1 } } { \omega c - \mu _ { 1 } \alpha _ { 2 } } } \end{array}$ . We plot the prioritizing curves in Fig. 11. The small differences in decimal places are due to the limited number of fitting points. GPP requires only one numerical calculation to achieve the optimal, while DP needs to iterate more than one hundred rounds to converge.

Threshold control: learning vs. heuristics. Next, we compared our two threshold control methods: waitingbased and learning-based. We generated two different query load patterns: (1) Low-High: First low load (λ = 1) then high load $( \lambda = 2 ) ;$ (2) High-Low: First high load then low load. We simulated two inference models with service rates 1.0, 5.0 and error rates 0.0, 0.2, and we set $c = 0 . 1$ . We trained a twolayer DQN [65] with 128 and 64 dense units using a 0.001 learning rate and 20 batch size for 50 epochs. Then we tested its performance on both Low-High and High-Low traces. As shown in Fig. 12, the DQN agent achieves a good trade-off when tested on the same load pattern. However, it failed to reduce the latency when the test pattern was changed to High-Low. On the other hand, the waiting-based approach achieves good trade-offs on both load patterns.

![](images/b599a470702c04bcc7b1f890d9c9bfdc3f1bc42ad88f466ba6f2c792fd2fdf4d.jpg)



(a) DQN-based

![](images/8d2510b14e1f2027c3954d8da25a5cc9863061340d5d252ff79150638b13dac3.jpg)



(b) Waiting-Based   
Fig. 12: Reinforcement learning-based and waiting-based methods on threshold control when the load pattern shifts.

Threshold control: heuristics vs. optimum. We compared thresholds generated by our waiting-based approach and optimal ones. Experimental results show that our approach achieves threshold control performance that is close to the optimal dynamic programming. For different arrival rates, the average threshold generated by our waiting-based heuristics has only 0.5 and 1.3 mean absolute error, given c = 0.01, 0.005 respectively. The parameter $\tau = 5 . 0$ was obtained by fitting only one optimal point and robust to varying query arrival rates. Compared to the huge cost gap between the optimal solution and our heuristics, this small error in threshold is well worth it.

# 5.6 InferRouter in On-Device Inference

Mobile HAR. We set the 1-1000 and 1500-2947 queries to arrive in 10 qps and 1000-1500 queries to arrive in 200 qps to generate a trace with a bursty load. As shown in Fig. 13, if we only used the LSTM model, the latency will accumulate to more than 10s when the bursty load comes. Using InFi, in order to keep high accuracy, the latency still climbs to around 1s. Our proposed InferRouter significantly outperforms InFi and standalone serving policies: the p99 latency is only 0.104s, 5.8X faster than InFi, and 132.5X faster than serving LSTM standalone. For accuracy, InferRouter brings only 1.5% degradation, while InFi brings 7.4%. Compared with serving DTree standalone (89.7%), using InferRouter improves 8.8% accuracy on average.

Robustness to accuracy dynamics. In the above experiments, the accuracy of DTree is relatively stable due to the random order of the query. We tested query traces with dynamic accuracy. Instead of randomly shuffling queries, we put the queries with more errors in the middle and use the Min-Load [66] (send each query to the model with minimal load) policy as a comparison. On average, InferRouter achieves 95.1% accuracy while Min-Load is 93%. In terms of the lowest accuracy of time segments, InferRouter is 90%, 9% higher than the Min-Load (only 81%). InferRouter’s accuracy awareness helps it better balance the accuracy when the DTree’s performance fluctuates.

![](images/622706ca7ee211d311db11bad4cf4022536b7f182fd668c9f3ab53696e441aad.jpg)



![](images/3abeb79909226136d66e9d8b6584ee75859289b883d56edbbac4fdd9b65e715f.jpg)



Fig. 13: Performance in Mobile HAR. Tested on a Smartwatch.

![](images/4a7d0057d592e4114772290d1c7d0e2d9daca6495733858062c4b9fe8bac2f26.jpg)



![](images/d1cea528dcf7540e13fdb04e3530dd28c8652e0f050890109f40aa5f89f0528b.jpg)



Fig. 15: Performance in BankQA. Tested on an NVIDIA P100 edge device.

![](images/cc0999b3a54ef7b437165b38c66ea55f9a8cdd3bc75d5ec743a3d322e2c6e2fd.jpg)



![](images/92f5be1facd3550bb43865c86a84756fb518b18c66d8108b0e2c6d34ceaf1924.jpg)



Fig. 14: Performance in Edge VC. Tested on an Orin development board.

Edge VC. As shown in Fig. 14, InferRouter significantly outperforms Chameleon in keeping a low inference latency. Note that, we only plot the standalone policies of v5x-640 and v3Tiny-320 for a clear illustration. InferRouter achieves 0.495s P99 latency and 0.304s average latency, 260.8X and 90.3X faster, compared with Chameleon. And InferRouter achieves slightly higher accuracy, 95.8%, than Chameleon (95.7%). We also considered another practical setting: when the latency exceeds a threshold, we discarded the inference result. Then we adopt a different accuracy metric that takes the missed queries as error too. Under this setting, using 1s as the threshold, InferRouter achieves a 0 deadline miss rate. Compared with Chameleon which returns only 40.7% accuracy with a 55.4% deadline miss rate, InferRouter improves 55.1% inference accuracy.

Single-source vs. multi-source processing. Recall that in Sec. 5.5, adversarial multi-source performance compromises the effectiveness of AAP. In the Edge VC application, we tested InferRouter using both single-source and multisource processing modes. Experimental results show that multi-source processing has a slight accuracy degradation (< 1%). The reason is that the accuracy patterns under cameras at different intersections follow a similar temporal distribution, e.g., during the morning rush hour, the lightweight model often misses some vehicles. Still, in the middle of the night, the accuracy of each model is very close.

BankQA. Using one-day trace in a global bank’s QA system, we evaluated InferRouter on two inference model: the BERT-based model and an approximate cache. As shown in Fig. 15, without any optimization, standalone serving BERT will bring latency higher than 10s. And if we only use the approximate cache, the average accuracy is only 80.2%. Compared with FoggyCache, InferRouter achieves a better trade-off: 7ms less P99 latency and 4.5% higher inference accuracy.

Comparison with offloading. Instead of collaboratively using heterogeneous models, offloading methods deploy the heavy model on a powerful device and send queries to it. For mobile HAR, when deploying the LSTM model on the edge, inference latency is around 20 ms per query ( 12ms lower than inference on a smartwatch). However, cellular-based / WLAN-based communication between the smartwatch and edge can exceed 50ms / 10ms, respectively. Offloading results in more than 20s p99 latency in this case, and InferRouter significantly reduces it to 0.104s. Our single-device computing model avoids issues about network communication delay and data privacy. It is worth noting that in actual applications, there may be a situation where the latency of offloading to the edge is still lower even after adding the communication overhead. For example, when we want to deploy a large model with hundreds of millions of parameters, it may require hundreds of milliseconds of latency on a mobile device, while high-end GPUs on the edge can complete it in around 10 ms. In these cases, deploying large models on the powerful edge can obviously create more optimization space for InferRouter’s load balancing. Although not dedicated to offloading, our RPC-based implementation actually supports this offloading deployment.

Sensitivity to parameter c. The only manually set parameter in InferRouter is the importance factor c in the objective function Eq. 1. We tested several different values of parameter c, from 0 to 10. Experimental results show that, for extreme values like c = 0, InferRouter only cares the accuracy and used the gold-standard model only. And when c is large, InferRouter sets the queue length threshold as 1, i.e., once any query arrives InferRouter will forward it to the model with second priority, if the top-prioritized model is not idle. Our best practice is: Typically applications will have a latency budget, and we can use that budget to calculate the maximal number of waiting queries in the queue given a load burst. Then we can search for a proper c

TABLE 5: On-device latency and scaling complexity comparisons of InferRouter and baselines. K denotes the number of models and I denotes the number of iterations to converge. 

<table><tr><td>Module</td><td>Latency</td><td>Complexity</td></tr><tr><td>Dynamic Programming</td><td>368.3 ms</td><td> $\Theta(2^{K}I)$ </td></tr><tr><td>LSTM Inference</td><td>31.7 ms</td><td> $\Theta(1)$ </td></tr><tr><td>DTree Inference</td><td>52  $\mu$ s</td><td> $\Theta(1)$ </td></tr><tr><td>InFi Skip-NNs [16]</td><td>25.8 ms</td><td> $\Theta(K-1)$ </td></tr><tr><td>model Prioritizing</td><td>0.8  $\mu$ s</td><td> $\Theta(K-1)$ </td></tr><tr><td>Threshold Control</td><td>1.2  $\mu$ s</td><td> $\Theta(2)$ </td></tr></table>

TABLE 6: Energy consumption on smartwatch. 

<table><tr><td>Module</td><td>InferRouter</td><td>InFi</td><td>LSTM</td><td>DTree</td></tr><tr><td>Energy (mJ/query)</td><td>9.5</td><td>56.2</td><td>524.4</td><td>23.5</td></tr></table>

by DP.

Overheads. We tested latency on mobile and edge devices and reported the worst latency on the Huawei Watch. For K models, DP computes $\Theta ( 2 ^ { K } \breve { I } )$ value functions, where I is the number of iterations to converge. Our prioritizing approach only requires $\Theta ( K - 1 )$ computations of Eq. 2 and our threshold control only needs Θ(2) evaluations of Eq. 3. As shown in Tab. 5, prioritizing and threshold control can be done within $2 \mu \mathrm { s } ,$ which is much faster than DP and InFi. Running DP is infeasible since its decisions are even slower than the gold-standard inference model. We also report the additional energy consumption of InferRouter on a smartwatch: less than 10 mJ per query, see Tab. 6. As a comparison, InFi [16] baseline brings 56.2 mJ per query and the gold-standard LSTM brings 524.4 mJ per query. And our design methodology can be extended for balancing accuracy and energy.

# 6 RELATED WORK

Adaptive resource provisioning for ML. Adaptive resource provisioning aims to dynamically adjust the computing resources for ML inference to meet the latency and other SLOs. INFaaS [30] exemplifies this by automatically selecting model variants—such as neural networks optimized through quantization and layer fusion—and provisioning resources in alignment with high-level goals specified by developers. Similarly, InferLine [31] emphasizes resource management across various stages of inference pipelines, ensuring compliance with latency constraints throughout the process. Mark [32] introduces SLO-aware scheduling and provisioning strategies tailored for ML models, particularly for accommodating load bursts that can occur in realtime applications. Cocktail [22] takes a unique approach by dynamically selecting models from an ensemble and making auto-scaling decisions for cloud-based model inference, thereby enhancing resource efficiency.

Different from these works, InferRouter considers heterogeneous inference models that have a huge gap in resource requirements. For on-device inference in mobile applications, the resource demands of scaling original models are prohibitive. For example, deploying only one tiny CNN model into an MCU already requires very elaborate development [67]. So an advantage of InferRouter is that it can be applied to IoT and mobile devices.

Leveraging heterogeneous models. Prior work has explored leveraging heterogeneous models for inference to balance performance and resource efficiency in various domains. For example, VideoEdge [68] proposes a hierarchical approach to processing video streams by deploying models of varying complexity across edge and cloud clusters, optimizing latency and resource usage. Similarly, Focus [69] introduces a system for querying large-scale video datasets using a combination of lightweight and heavyweight models to achieve low latency and low cost. While these approaches effectively utilize heterogeneous models, they primarily focus on distributed systems involving edgecloud architectures or large-scale dataset processing. In contrast, our work is the first attempt to leverage on-device heterogeneous models for load balancing, where multiple preloaded models operate locally on a single device. Our design targets scenarios with strict latency requirements and limited offloading capabilities, introducing novel strategies to dynamically route queries among preloaded models, achieving efficient resource utilization and accuracy tradeoffs directly on the device.

Resource-accuracy trade-off inference. Rich literature [6], [70], [71] provides diverse mechanisms to generate inference models with resource and accuracy trade-offs. We now briefly introduce four canonical generation mechanisms: (1) Model compression [13], [40], [72] reduces the size of ML models and improves inference speed, by pruning parameters and connections that are less related to the accuracy. Knowledge distillation [14] is one type of compression approach and has received more attention recently. It aims to transfer the functionality of a large unwieldy model or set of models (the “teacher(s)”) to a single smaller model (the “student”). (2) Approximate caching [16], [17], [19] stores previously processed (input, output) entries, like a cache, and returns a fast response by approximately matching new inputs with cached ones. Based on the low-level feature (Reducto [17]) or learned input embedding (FoggyCache [19] and InFi [16]), approximate caching replaces exact matching with approximate matching, without significantly diminishing accuracy. (3) Pipeline selection [20], [21] adjusts taskspecific configurable knobs (e.g., frame resolution [41] and backbone neural network in video analytics) to balance the efficiency and accuracy. (4) Early-exit neural network [24], [44] is a type of architecture designed to dynamically balance inference speed and accuracy by allowing intermediate outputs at certain layers, enabling predictions to be made without traversing the entire network. This technique introduces “exit points” at various depths in the model, where simpler tasks or easier inputs can produce confident predictions early on, reducing computation time and resource consumption. For more complex inputs, the model continues deeper for improved accuracy.

InferRouter works as complementary to those works and provides a mechanism-agnostic load-balancing algorithm that adaptively distributes inference queries on those heterogeneous models.

Resource orchestration and VNF/task placement. Complementary to our work, there is a rich body of literature addressing the dynamic orchestration and placement of computational tasks or Virtual Network Functions (VNFs) across edge-cloud infrastructures. For instance, HELICON [73] uses hierarchical reinforcement learning for dynamic VNF placement in edge-cloud environments, achieving strong performance under varying workloads. iOn-Profiler [74] profiles VNFs via multi-objective reinforcement learning to optimize performance across multiple resource types. GTN-LA [75] applies graph transformers and attention-based LSTMs to predict multi-step workloads by modeling inter-VNF dependencies. While these systems primarily focus on network service management, their insights into dynamic scheduling and model profiling are highly relevant and can be integrated with inference-level decision-making. Our work differs in that we operate at the inference routing granularity within a single device but shares the overarching goal of optimizing resource-performance trade-offs under dynamic conditions.

# 7 DISCUSSION

Applicability to multi-device scenarios. InferRouter is designed for on-device inference scenarios where multiple heterogeneous models are dynamically selected to process latency-sensitive queries. This design addresses environments such as mobile devices, IoT, or edge gateways, where offloading is limited and lightweight, local decision-making is essential. In multi-device settings, InferRouter can complement distributed orchestration systems by serving as a local model selection module within each node. Its decision latency and resource footprint make it feasible to scale horizontally across edge clusters.

Scalability with input sources. Our current experiments focus on the inference dynamics of a single input stream. For scenarios with multiple input sources, InferRouter remains applicable by integrating with a batching mechanism. Since its decision process is stateless and model-aware, it can be extended to more complex input routing pipelines with minimal modification.

# 8 CONCLUSION

This work starts from our experience developing on-device inference systems, where we observed high tail latency caused by load bursts. To address the limitations of scaling the original model, we proposed an idea to route queries to a heterogeneous model that costs much fewer resources. We formulated this problem and analyzed the algorithmic structure of the optimal policy using a queueing model. We presented InferRouter with several designs that enable adaptability and scalability, including anti-idling accuracy profiling, gold-pair prioritizing, and waiting-based threshold control. Extensive evaluations on real on-device inference systems show the effectiveness and wide applicability of our design. InferRouter outperforms five strong baselines on P99 latency (up to 262.1x faster) and inference accuracy (up to 5.9% higher) metrics on all three systems.

# ACKNOWLEDGMENTS

The research is partially supported by National Key R&D Program of China under Grant No. 2021ZD0110400, 2021YFB2900103, Innovation Program for Quantum Science and Technology 2021ZD0302900, China National Natural Science Foundation with No. 623B2093, 62132018, 62231015, Pioneer and Leading Goose R&D Program of Zhejiang, 2023C01029 and 2023C01143, the Fundamental Research Funds for the Central Universities WK2150110024, Science and Technology Tackling Program of Anhui Province, No.202423k09020016, and RGC Theme-based Research Scheme No.2400070.

# REFERENCES

[1] Y. Zhao, S. S. Afzal, W. Akbar, O. Rodriguez, F. Mo, D. Boyle, F. Adib, and H. Haddadi, “Towards battery-free machine learning and inference in underwater environments,” in Proceedings of the 23rd Annual International Workshop on Mobile Computing Systems and Applications, 2022, pp. 29–34.   
[2] L. Jiang, Q. Song, R. Tan, and M. Li, “Primask: Cascadable and collusion-resilient data masking for mobile cloud inference,” in Proceedings of the 20th ACM Conference on Embedded Networked Sensor Systems, 2022, pp. 164–178.   
[3] R. Liang, T. Cao, J. Wen, M. Wang, Y. Wang, J. Zou, and Y. Liu, “Romou: Rapidly generate high-performance tensor kernels for mobile gpus,” in Proceedings of the 28th Annual International Conference on Mobile Computing And Networking, 2022, pp. 487–500.   
[4] F. Jia, S. Jiang, T. Cao, W. Cui, T. Xia, X. Cao, Y. Li, Q. Wang, D. Zhang, J. Ren et al., “Empowering in-browser deep learning inference on edge through just-in-time kernel optimization,” in Proceedings of the 22nd Annual International Conference on Mobile Systems, Applications and Services, 2024, pp. 438–450.   
[5] Z. Zhou, B. Wu, Z. Liang, G. Sun, C. Xu, and G. Luo, “{SaFace}: Towards scenario-aware face recognition via edge computing system,” in 3rd USENIX Workshop on Hot Topics in Edge Computing (HotEdge 20), 2020.   
[6] X. Li, Y. Li, Y. Li, T. Cao, and Y. Liu, “Flexnn: Efficient and adaptive dnn inference on memory-constrained edge devices,” in Proceedings of the 30th Annual International Conference on Mobile Computing and Networking, 2024, pp. 709–723.   
[7] M. Wang, S. Ding, T. Cao, Y. Liu, and F. Xu, “Asymo: scalable and efficient deep-learning inference on asymmetric mobile cpus,” in Proceedings of the 27th Annual International Conference on Mobile Computing and Networking, 2021, pp. 215–228.   
[8] T. Lee, Z. Lin, S. Pushp, C. Li, Y. Liu, Y. Lee, F. Xu, C. Xu, L. Zhang, and J. Song, “Occlumency: Privacy-preserving remote deep-learning inference using sgx,” in The 25th Annual International Conference on Mobile Computing and Networking, 2019, pp. 1– 17.   
[9] D.-S. Kang, E. Baek, S. Son, Y. Lee, T. Gong, and H.-S. Kim, “Mirror: Towards generalizable on-device video virtual try-on for mobile shopping,” Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, vol. 7, no. 4, pp. 1–27, 2024.   
[10] C. Zhang, M. Yu, F. Yan et al., “Enabling cost-effective, slo-aware machine learning inference serving on public cloud,” IEEE Transactions on Cloud Computing, 2020.   
[11] L. Liu, R. Zhong, W. Zhang, Y. Liu, J. Zhang, L. Zhang, and M. Gruteser, “Cutting the cord: Designing a high-quality untethered vr system with low latency remote rendering,” in Proceedings of the 16th Annual International Conference on Mobile Systems, Applications, and Services, 2018, pp. 68–80.   
[12] D. Ghimire, D. Kil, and S.-h. Kim, “A survey on efficient convolutional neural networks and hardware acceleration,” Electronics, vol. 11, no. 6, p. 945, 2022.   
[13] T. Choudhary, V. Mishra, A. Goswami, and J. Sarangapani, “A comprehensive survey on model compression and acceleration,” Artificial Intelligence Review, vol. 53, no. 7, pp. 5113–5155, 2020.   
[14] X. Liu, X. Wang, and S. Matwin, “Improving the interpretability of deep neural networks with knowledge distillation,” in 2018 IEEE International Conference on Data Mining Workshops (ICDMW). IEEE, 2018, pp. 905–912.   
[15] R. David, J. Duke, A. Jain, V. Janapa Reddi, N. Jeffries, J. Li, N. Kreeger, I. Nappier, M. Natraj, T. Wang et al., “Tensorflow lite micro: Embedded machine learning for tinyml systems,” Proceedings of Machine Learning and Systems, vol. 3, pp. 800–811, 2021.

[16] M. Yuan, L. Zhang, F. He, X. Tong, and X.-Y. Li, “Infi: End-to-end learnable input filter for resource-efficient mobile-centric inference,” in 28th Annual International Conference On Mobile Computing And Networking (MobiCom ’22), 2022.   
[17] Y. Li, A. Padmanabhan, P. Zhao, Y. Wang, G. H. Xu, and R. Netravali, “Reducto: On-camera filtering for resource-efficient realtime video analytics,” in Proceedings of the Annual conference of the ACM Special Interest Group on Data Communication on the applications, technologies, architectures, and protocols for computer communication, 2020, pp. 359–376.   
[18] M. Yuan, L. Zhang, X. You, and X.-Y. Li, “Packetgame: Multi-stream packet gating for concurrent video inference at scale,” in Proceedings of the ACM SIGCOMM 2023 Conference, ser. ACM SIGCOMM ’23. New York, NY, USA: Association for Computing Machinery, 2023, p. 724–737. [Online]. Available: https://doi.org/10.1145/3603269.3604825   
[19] P. Guo, B. Hu, R. Li, and W. Hu, “Foggycache: Cross-device approximate computation reuse,” in Proceedings of the 24th Annual International Conference on Mobile Computing and Networking, 2018, pp. 19–34.   
[20] J. Jiang, G. Ananthanarayanan, P. Bodik, S. Sen, and I. Stoica, “Chameleon: scalable adaptation of video analytics,” in Proceedings of the 2018 Conference of the ACM Special Interest Group on Data Communication, 2018, pp. 253–266.   
[21] H. Zhang, G. Ananthanarayanan, P. Bodik, M. Philipose, P. Bahl, and M. J. Freedman, “Live video analytics at scale with approximation and {Delay-Tolerance},” in 14th USENIX Symposium on Networked Systems Design and Implementation (NSDI 17), 2017, pp. 377–392.   
[22] J. R. Gunasekaran, C. S. Mishra, P. Thinakaran, B. Sharma, M. T. Kandemir, and C. R. Das, “Cocktail: A multidimensional optimization for model serving in cloud,” in 19th USENIX Symposium on Networked Systems Design and Implementation (NSDI 22), 2022, pp. 1041–1057.   
[23] T. Li, J. Huang, E. Risinger, and D. Ganesan, “Low-latency speculative inference on distributed multi-modal data streams,” in Proceedings of the 19th Annual International Conference on Mobile Systems, Applications, and Services, 2021, pp. 67–80.   
[24] H. Rahmath P, V. Srivastava, K. Chaurasia, R. G. Pacheco, and R. S. Couto, “Early-exit deep neural network-a comprehensive survey,” ACM Computing Surveys, vol. 57, no. 3, pp. 1–37, 2024.   
[25] J. Zhang, F. R. Yu, S. Wang, T. Huang, Z. Liu, and Y. Liu, “Load balancing in data center networks: A survey,” IEEE Communications Surveys & Tutorials, vol. 20, no. 3, pp. 2324–2352, 2018.   
[26] X. Xu, S. Fu, Q. Cai, W. Tian, W. Liu, W. Dou, X. Sun, and A. X. Liu, “Dynamic resource allocation for load balancing in fog environment,” Wireless Communications and Mobile Computing, vol. 2018, 2018.   
[27] Y.-C. Chow et al., “Models for dynamic load balancing in a heterogeneous multiple processor system,” IEEE Transactions on Computers, vol. 100, no. 5, pp. 354–361, 1979.   
[28] A. Gandhi, M. Harchol-Balter, R. Raghunathan, and M. A. Kozuch, “Autoscale: Dynamic, robust capacity management for multi-tier data centers,” ACM Transactions on Computer Systems (TOCS), vol. 30, no. 4, pp. 1–26, 2012.   
[29] Q. Weng, W. Xiao, Y. Yu, W. Wang, C. Wang, J. He, Y. Li, L. Zhang, W. Lin, and Y. Ding, “MLaaS in the wild: Workload analysis and scheduling in large-scale heterogeneous GPU clusters,” in 19th {USENIX} Symposium on Networked Systems Design and Implementation ({NSDI} 22), 2022.   
[30] F. Romero, Q. Li, N. J. Yadwadkar, and C. Kozyrakis, “INFaaS: Automated model-less inference serving,” in 2021 USENIX Annual Technical Conference (USENIX ATC 21). USENIX Association, Jul. 2021, pp. 397–411. [Online]. Available: https: //www.usenix.org/conference/atc21/presentation/romero   
[31] D. Crankshaw, G.-E. Sela, X. Mo, C. Zumar, I. Stoica, J. Gonzalez, and A. Tumanov, “Inferline: latency-aware provisioning and scaling for prediction serving pipelines,” in Proceedings of the 11th ACM Symposium on Cloud Computing, 2020, pp. 477–491.   
[32] C. Zhang, M. Yu, W. Wang, and F. Yan, “{MArk}: Exploiting cloud services for {Cost-Effective},{SLO-Aware} machine learning inference serving,” in 2019 USENIX Annual Technical Conference (USENIX ATC 19), 2019, pp. 1049–1062.   
[33] K. Huang and W. Gao, “Real-time neural network inference on extremely weak devices: agile offloading with explainable ai,” in Proceedings of the 28th Annual International Conference on Mobile Computing And Networking, 2022, pp. 200–213.

[34] B. Taylor, V. S. Marco, W. Wolff, Y. Elkhatib, and Z. Wang, “Adaptive deep learning model selection on embedded systems,” ACM Sigplan Notices, vol. 53, no. 6, pp. 31–43, 2018.   
[35] V. S. Marco, B. Taylor, Z. Wang, and Y. Elkhatib, “Optimizing deep learning inference on embedded systems through adaptive model selection,” ACM Transactions on Embedded Computing Systems (TECS), vol. 19, no. 1, pp. 1–28, 2020.   
[36] R. Han, Q. Zhang, C. H. Liu, G. Wang, J. Tang, and L. Y. Chen, “Legodnn: block-grained scaling of deep neural networks for mobile vision,” in Proceedings of the 27th Annual International Conference on Mobile Computing and Networking, 2021, pp. 406–419.   
[37] Ultralytics, “Yolov5,” https://github.com/ultralytics/yolov5, 2022.   
[38] Y. Chang, A. Mathur, A. Isopoussu, J. Song, and F. Kawsar, “A systematic study of unsupervised domain adaptation for robust human-activity recognition,” ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, vol. 4, no. 1, pp. 1–30, 2020.   
[39] J. D. M.-W. C. Kenton and L. K. Toutanova, “Bert: Pre-training of deep bidirectional transformers for language understanding,” in Proceedings of NAACL-HLT, 2019, pp. 4171–4186.   
[40] K. Wang, Z. Liu, Y. Lin, J. Lin, and S. Han, “Haq: Hardware-aware automated quantization with mixed precision,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2019, pp. 8612–8620.   
[41] S. Kim, M. Kim, and Y. Lee, “A joint analysis of input resolution and quantization precision in deep learning,” in Proceedings of the 29th Annual International Conference on Mobile Computing and Networking, 2023, pp. 1–3.   
[42] T. Fukuda, M. Suzuki, G. Kurata, S. Thomas, J. Cui, and B. Ramabhadran, “Efficient knowledge distillation from an ensemble of teachers.” in Interspeech, 2017, pp. 3697–3701.   
[43] S. Cai, G. Chen, B. C. Ooi, and J. Gao, “Model slicing for supporting complex analytics with elastic inference cost and resource constraints,” Proc. VLDB Endow., vol. 13, no. 2, p. 86–99, Oct. 2019.   
[44] Z. Liu, Q. Lan, and K. Huang, “Resource allocation for multiuser edge inference with batching and early exiting,” IEEE Journal on Selected Areas in Communications, vol. 41, no. 4, pp. 1186–1200, 2023.   
[45] Y. Dai, R. Pan, A. Iyer, K. Li, and R. Netravali, “Apparate: Rethinking early exits to tame latency-throughput tensions in ml serving,” in Proceedings of the ACM SIGOPS 30th Symposium on Operating Systems Principles, 2024, pp. 607–623.   
[46] B. Legros and O. Jouini, “Routing in a queueing system with two heterogeneous servers in speed and in quality of resolution,” Stochastic Models, vol. 33, no. 3, pp. 392–410, 2017.   
[47] D. G. Kendall, “Stochastic processes occurring in the theory of queues and their analysis by the method of the imbedded markov chain,” The Annals of Mathematical Statistics, pp. 338–354, 1953.   
[48] D. M. Roijers, P. Vamplew, S. Whiteson, and R. Dazeley, “A survey of multi-objective sequential decision-making,” Journal of Artificial Intelligence Research, vol. 48, pp. 67–113, 2013.   
[49] N. Gunantara, “A review of multi-objective optimization: Methods and its applications,” Cogent Engineering, vol. 5, no. 1, p. 1502242, 2018.   
[50] J. M. George and J. M. Harrison, “Dynamic control of a queue with adjustable service rate,” Operations research, vol. 49, no. 5, pp. 720–731, 2001.   
[51] V. Kalavri, J. Liagouris, M. Hoffmann, D. Dimitrova, M. Forshaw, and T. Roscoe, “Three steps is all you need: fast, accurate, automatic scaling decisions for distributed streaming dataflows,” in 13th USENIX Symposium on Operating Systems Design and Implementation (OSDI 18), 2018, pp. 783–798.   
[52] W. Zhang, Z. He, L. Liu, Z. Jia, Y. Liu, M. Gruteser, D. Raychaudhuri, and Y. Zhang, “Elf: accelerate high-resolution mobile deep vision with content-aware parallel offloading,” in Proceedings of the 27th Annual International Conference on Mobile Computing and Networking, 2021, pp. 201–214.   
[53] J. C. Doyle, B. A. Francis, and A. R. Tannenbaum, Feedback control theory. Courier Corporation, 2013.   
[54] B. Zhang, X. Jin, S. Ratnasamy, J. Wawrzynek, and E. A. Lee, “Awstream: Adaptive wide-area streaming analytics,” in Proceedings of the 2018 Conference of the ACM Special Interest Group on Data Communication, 2018, pp. 236–252.   
[55] J. W. Cohen, The single server queue. Elsevier, 2012.   
[56] J.-y. Baek, G. Kaddoum, S. Garg, K. Kaur, and V. Gravel, “Managing fog networks using reinforcement learning based load balancing algorithm,” in 2019 IEEE Wireless Communications and Networking Conference (WCNC). IEEE, 2019, pp. 1–7.

[57] S. Yeo, Y. Naing, T. Kim, and S. Oh, “Achieving balanced load distribution with reinforcement learning-based switch migration in distributed sdn controllers,” Electronics, vol. 10, no. 2, p. 162, 2021.   
[58] A. Ali, R. Pinciroli, F. Yan, and E. Smirni, “Batch: Machine learning inference serving on serverless platforms with adaptive batching,” in SC20: International Conference for High Performance Computing, Networking, Storage and Analysis, 2020, pp. 1–15.   
[59] F. Ahmad, H. Qiu, R. Eells, F. Bai, and R. Govindan, “{CarMap}: Fast 3d feature map updates for automobiles,” in 17th USENIX Symposium on Networked Systems Design and Implementation (NSDI 20), 2020, pp. 1063–1081.   
[60] kivy, “Python-for-android,” https://github.com/kivy/ python-for-android, 2022.   
[61] D. Anguita, A. Ghio, L. Oneto, X. Parra Perez, and J. L. Reyes Ortiz, “A public domain dataset for human activity recognition using smartphones,” in Proceedings of the 21th international European symposium on artificial neural networks, computational intelligence and machine learning, 2013, pp. 437–442.   
[62] T.-Y. Lin, M. Maire, S. Belongie, J. Hays, P. Perona, D. Ramanan, P. Dollar, and C. L. Zitnick, “Microsoft coco: Common objects in ´ context,” in European conference on computer vision. Springer, 2014, pp. 740–755.   
[63] J. S. Jeong, J. Lee, D. Kim, C. Jeon, C. Jeong, Y. Lee, and B.-G. Chun, “Band: coordinated multi-dnn inference on heterogeneous mobile processors,” in Proceedings of the 20th Annual International Conference on Mobile Systems, Applications and Services, 2022, pp. 235–247.   
[64] D. Xu, Q. Li, M. Xu, K. Huang, G. Huang, S. Wang, X. Jin, Y. Ma, and X. Liu, “Niagara: Scheduling dnn inference services on heterogeneous edge processors,” in International Conference on Service-Oriented Computing. Springer, 2023, pp. 67–85.   
[65] V. Mnih, K. Kavukcuoglu, D. Silver, A. A. Rusu, J. Veness, M. G. Bellemare, A. Graves, M. Riedmiller, A. K. Fidjeland, G. Ostrovski et al., “Human-level control through deep reinforcement learning,” nature, vol. 518, no. 7540, pp. 529–533, 2015.   
[66] K. Salchow, “Load balancing 101: Nuts and bolts,” White Paper, F5 Networks, Inc, 2007.   
[67] J. Lin, W.-M. Chen, Y. Lin, C. Gan, S. Han et al., “Mcunet: Tiny deep learning on iot devices,” Advances in Neural Information Processing Systems, vol. 33, pp. 11 711–11 722, 2020.   
[68] C.-C. Hung, G. Ananthanarayanan, P. Bodik, L. Golubchik, M. Yu, P. Bahl, and M. Philipose, “Videoedge: Processing camera streams using hierarchical clusters,” in 2018 IEEE/ACM Symposium on Edge Computing (SEC). IEEE, 2018, pp. 115–131.   
[69] K. Hsieh, G. Ananthanarayanan, P. Bodik, S. Venkataraman, P. Bahl, M. Philipose, P. B. Gibbons, and O. Mutlu, “Focus: Querying large video datasets with low latency and low cost,” in 13th USENIX Symposium on Operating Systems Design and Implementation (OSDI 18), 2018, pp. 269–286.   
[70] N. D. Lane, S. Bhattacharya, P. Georgiev, C. Forlivesi, L. Jiao, L. Qendro, and F. Kawsar, “Deepx: A software accelerator for low-power deep learning inference on mobile devices,” in 2016 15th ACM/IEEE International Conference on Information Processing in Sensor Networks (IPSN). IEEE, 2016, pp. 1–12.   
[71] X. Tang, Y. Wang, T. Cao, L. L. Zhang, Q. Chen, D. Cai, Y. Liu, and M. Yang, “Lut-nn: Empower efficient neural network inference with centroid learning and table lookup,” in Proceedings of the 29th Annual International Conference on Mobile Computing and Networking, 2023, pp. 1–15.   
[72] C. Tai, T. Xiao, Y. Zhang, X. Wang, and E. Weinan, “Convolutional neural networks with low-rank regularization,” in 4th International Conference on Learning Representations, ICLR 2016, 2016.   
[73] M. Bunyakitanon, X. Vasilakos, R. Nejabati, and D. Simeonidou, “Helicon: Orchestrating low-latent & load-balanced virtual network functions,” in ICC 2022-IEEE International Conference on Communications. IEEE, 2022, pp. 353–358.   
[74] X. Vasilakos, S. Moazzeni, A. Bravalheri, P. Jaisudthi, R. Nejabati, and D. Simeonidou, “ion-profiler: Intelligent online multiobjective vnf profiling with reinforcement learning,” IEEE Transactions on Network and Service Management, vol. 21, no. 2, pp. 2339– 2352, 2024.   
[75] Y. Wu, J. Liu, C. Wang, X. Xie, and G. Shi, “Graph transformer and lstm attention for vnf multi-step workload prediction in sfc,” IEEE Transactions on Network and Service Management, 2024.

![](images/74fa0451e094d731954666ead4499801d276a541f937cd1d66e1f2031d8c90ba.jpg)



Mu Yuan is currently a Postdoc Fellow at the Department of Information Engineering, The Chinese University of Hong Kong. He received his PhD and Bachelor’s degrees from the University of Science and Technology of China. His research interests include AIoT, mobile and edge computing, and privacy and security of AI.

![](images/51a98975006a2ff9c810f7a581f2432476be4ce3adc3b8831370b1ef910d0b98.jpg)



Lan Zhang is currently a Professor at the School of Computer Science and Technology, University of Science and Technology of China. She received her Ph.D degree and Bachelor degree from Tsinghua University, China. Her research interests include mobile computing, privacy protection,and data sharing and trading.

![](images/d4e2f77bd6f5fcbdfea33ecc5eb245b28d76673fb7efe26e1b44f6cf958d1d5d.jpg)



Di Duan , Ph.D., is currently a Postdoctoral Fellow in the Department of Information Engineering at The Chinese University of Hong Kong (CUHK). He received his Ph.D. in Computer Science from the City University of Hong Kong (CityU). His research lies at the intersection of mobile computing, human-computer interaction, and wearable sensing, with a special focus on system-enabled novel applications such as tracking, reconstruction, interaction, and healthcare.

![](images/7e6ce5af14cf58262277c17f9721b86098cedbcc457258a6964c27eb4fe41a94.jpg)



Liekang Zeng (Member, IEEE) received the Ph.D. and the B.E. degrees from Sun Yat-sen University, Guangzhou, China. His current research interests include edge intelligence, mobile computing, and distributed machine learning systems.

![](images/9237ed331e66a6c66adddef19ab302fa41e7ff1ca5e9f7b9db4f7017f1869df9.jpg)



Miao-Hui Song is a PhD candidate at the School of Computer Science and Technology, University of Science and Technology of China. She received a bachelor’s degree in computer science and technology from Chongqing University. Her research interests include active learning and data-labeling systems.

![](images/85772989f3d90b27bca80113d40162e2c821cec379186ffc861fc86c9b497931.jpg)



Zichong Li is a Ph.D. candidate at the H. Milton Stewart School of Industrial and Systems Engineering, Georgia Institute of Technology. He received his bachelor’s degree and master’s degree from the University of Science and Technology of China. His research interests include sequence data and language model.

![](images/8390bbf0bdd6ed3e01ead256b4308dd7b7204b210a0ac66f577075fa68826352.jpg)



Guoliang Xing (Fellow, IEEE) is currently a Professor in the Department of Information Engineering at The Chinese University of Hong Kong, an IEEE Fellow, and received his Ph.D. from Washington University in St. Louis in 2006. He was previously a faculty member at Michigan State University, USA, from 2008-2017. He received the US NSF CAREER Award in 2010, the Withrow Distinguished Faculty Award from Michigan State University in 2014, and the Research Excellence Award and the Outstanding Fellow Award from CUHK in 2024. Prof. Xing’s group currently leads several large-scale Embedded AI projects on urban smart infrastructure, autonomous driving, and smart health. His work has received six Best Paper Awards, four Best Demo/Poster Awards, and seven Best Paper Finalist honors at premier international conferences including MobiCom, MobiSys, SenSys, ICNP, and IPSN.

![](images/3d6affbb4dfd9e38dbf20f068284b76ff2abb132dc2308b42da3898008d9f8ee.jpg)



Xiang-Yang Li (Fellow, IEEE) is a professor and Executive Dean at School of Computer Science and Technology, USTC. He is an ACM Fellow (2019), IEEE fellow (2015), an ACM Distinguished Scientist (2014). He was a full professor at Computer Science Department of IIT and co-Chair of ACM China Council. Dr. Li received M.S. (2000) and Ph.D. (2001) degree at Department of Computer Science from University of Illinois at Urbana-Champaign. He received a Bachelor degree at Department of Computer Science from Tsinghua University, P.R. China, in 1995. His research interests include Artificial Intelligence of Things (AIOT), privacy and security of AIOT, and data sharing and trading.