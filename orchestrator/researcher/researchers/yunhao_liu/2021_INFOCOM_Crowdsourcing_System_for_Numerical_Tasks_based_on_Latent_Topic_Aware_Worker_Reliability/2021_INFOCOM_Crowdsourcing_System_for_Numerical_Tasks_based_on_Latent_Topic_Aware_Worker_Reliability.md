# Crowdsourcing System for Numerical Tasks based on Latent Topic Aware Worker Reliability

Zhuan Shi⇤, Shanyang Jiang⇤, Lan Zhang⇤, Yang Du†, Xiang-Yang Li⇤

⇤School of Computer Science and Technology, University of Science and Technology of China, Hefei, China

†School of Computer Science and Technology, Soochow University, Suzhou, China

Abstract—Crowdsourcing is a widely adopted way for various labor-intensive tasks. One of the core problems in crowdsourcing systems is how to assign tasks to most suitable workers for better results, which heavily relies on the accurate profiling of each worker’s reliability for different topics of tasks. Many previous work have studied worker reliability for either explicit topics represented by task descriptions or latent topics for categorical tasks. In this work, we aim to accurately estimate more fine-grained worker reliability for latent topics in numerical tasks, so as to further improve the result quality. We propose a bayesian probabilistic model named Gaussian Latent Topic Model(GLTM) to mine the latent topics of numerical tasks based on workers’ behaviors and to estimate workers’ topic-level reliability. By utilizing the GLTM, we propose a truth inference algorithm named TI-GLTM to accurately infer the tasks’ truth and topics simultaneously and dynamically update workers’ topic-level reliability. We also design an online task assignment mechanism called MRA-GLTM, which assigns appropriate tasks to workers with the Maximum Reduced Ambiguity principle. The experiment results show our algorithms can achieve significantly lower MAE and MSE than that of the state-of-the-art approaches.

# I. INTRODUCTION

Crowdsourcing is a widely adopted technique to obtain information or results of a task from a large, relatively open group of participants, e.g., image annotation [1], [2], sentiment analysis [3], answering database-hard queries [4]. Many crowdsourcing platforms, such as Amazon Mechanical Turk (AMT) [5] and CrowdFlower [6], provide convenient interfaces for requesters to post different types of crowdsourcing tasks. These platforms then assign micro-tasks to workers and pay them for answers. Fusing collected answers, results of those tasks are delivered to the requesters.

How to achieve high-quality results is one of the core challenges in crowdsourcing systems, since workers may provide low-quality answers or even erroneous ones due to their incompetence in the assigned tasks or dishonesty. To improve the quality of results, most previous efforts have been devoted to solving the following three problems:

1. How to estimate the reliability of workers accurately? Worker probability model [4], [7], [8] assumes that each worker has a consistent reliability on all tasks and treats his/her reliability as a constant value. This assumption is too strong, since a worker’s reliability usually varies with different tasks due to his/her different familiarity with various topics. To relax the assumption, some fine-grained reliability models have been proposed. Confusion matrix model [9] assumes that each worker shows the same reliability on the tasks with the same truths and models the probabilities that a worker provides an answer a given a truth d. Recently, latent domain model [10]–[12] divides tasks into different domains based on the text description and assumes each worker has a consistent reliability in each domain.

2. How to infer the truth of a task based on workers’ answers? The most intuitive approaches are majority voting for categorical tasks and average/median value for numerical tasks. It treats all answers equally and neglects the highly diverse reliability levels of workers. A series of approaches [13]–[18] have been designed to estimate worker reliability and infer the truth using an Expectation-Maximization (EM) strategy. Those methods all apply the same principle that workers with higher reliability would provide answers with higher quality.

3. How to assign a task to most suitable workers online? Early work usually adopts the Round-Robin (RR) strategy that randomly assigns a task to a worker when the worker arrives [4], [8], [19]. Recently, a series of online task assignment strategies also take workers’ reliability into consideration. For example, QASCA [9] uses both worker probability model and confusion matrix model to capture workers’ reliability and assign tasks with maximum accuracy or F1-score gains to each arriving worker. DOCS [11] uses a domain-aware reliability model and divide tasks into different domains, then the online task assignment is conducted based on workers’ domain-level expertise.

Estimating each worker’s reliability on the target task is the cornerstone of most state-of-the-art crowdsourcing systems. Those solutions model the reliability on the domain-level and assume that tasks sharing the same description or truth belong to the same domain. Du et al. [20], [21] reveal that even in the same domain, each worker may still show unstable reliability due to multiple latent topics in the domain. They design a latent topic model to estimate topic-level reliability, and simply use correct or incorrect to measure each answer. A worker’s reliability is the ratio of his/her correct answer. This binary measurement based model is only applicable to categorical tasks such as image classification, however, cannot be adopted for various numerical tasks, e.g., collecting location based temperature information, where a worker’s answer can be any number within a range.

In this work, we aim to answer the aforementioned three questions for numerical crowdsourcing tasks with latent topics, which is not a trivial extension of categorical tasks due to the following challenges: First, numerical tasks require a more precise worker reliability model, which considers the latent topics and infinite values of answers. Different from conventional domain-level models classifying tasks by explicit description texts, however, tasks of different latent topics may share the same text description and truth. Therefore, tasks’ latent topics are implicit and difficult to discover without any knowledge of topic distribution and truth distribution. Second, there may be some dishonest workers showing erratic reliability. Even honest workers’ reliability could change with their familiarity with these topics. We need to dynamically adjust workers’ topic-level reliability on the basis of their answers, without knowing the truth. Third, we also need novel truth inference and online task assignment mechanisms to cope with such a fine-grained dynamic reliability model. To match given tasks with continuously arriving workers, we need to accurately estimate not only each worker’s reliability on these tasks, but also the gain for each possible assignment, so as to maximize the overall accumulated gains.

Facing these challenges, we make the following main contributions:

•To the best of our knowledge, we propose the first latenttopic-aware worker reliability model for numerical tasks. We design a Gaussian latent topic model to divide tasks into latent topics based on workers’ behaviors and initialize each worker’s reliability on different latent topics.   
•We design a novel expectation-maximization based iterative method for truth inference, which first takes current reliability and answers as inputs to simultaneously estimate the truth and the distribution of latent topics, and then dynamically updates each worker’s topic-level reliability. Updated reliability will be used to further improve the estimation of truth and topic distribution.   
•To optimize the online task assignment to continuously arriving workers, we leverage entropy to measure the ambiguity of each task’s current truth distribution and propose to assign tasks to workers towards maximum reduced ambiguity.   
•We empirically show that based on our latent-topic-aware reliability model, our proposed truth inference method and online task assignment mechanism outperform the state-ofthe-art approaches by achieving significantly lower MAE and MSE on both a simulated dataset and a real world dataset.

The rest of the paper is organized as follows. In Section II-A, we formulate the problem and present the overview of our design. We introduce the Gaussian latent topic estimation in Section III. In Section IV and Section V, we demonstrate the truth inference mechanism and online task assignment mechanism. The experimental results are reported in Section VI. We review related work in Section VII and conclude our work in Section VIII.

# II. PROBLEM AND DESIGN OVERVIEW

# A. Problem Description

We consider a typical crowdsourcing system consisting of three parties: task requesters, the crowdsourcing platform and a dynamic collection of workers. Task requesters publish tasks on the platform. The platform assigns those tasks to workers and accumulates their answers to produce the results for requesters. Let $\mathcal { W } = \{ w _ { 1 } , w _ { 2 } , . . . , w _ { M } \}$ denote the complete set of M workers. Each worker $w \in \mathcal { W }$ arrives at a random time within a time window and has a capacity $w . \tau ( \mathrm { i } . { \bf e } . ,$ the maximum number of tasks he/she can complete). In this work, we focus on numerical tasks and consider two types of tasks: 1) N target tasks $\mathcal { T } = \{ t _ { 1 } , t _ { 2 } , . . . , t _ { N } \}$ are published by requesters without any ground truth, and we use $\hat { d } _ { t }$ to denote the estimated truth of each task $t \in \mathcal { T } ; 2 ) \ N ^ { * }$ golden tasks $\mathcal { T } ^ { * } = \{ t _ { 1 } ^ { * } , t _ { 2 } ^ { * } , . . . , t _ { N ^ { * } } ^ { * } \}$ and each golden task $t ^ { * } \in T ^ { * }$ has a ground truth $d _ { t ^ { * } }$ maintained by the platform. N is usually far greater than $N ^ { * }$ . Our aim to solve a fundamental challenging issue: how to assign diverse tasks to the most suitable workers and achieve accurate results, even facing coarse-grained task descriptions and some dishonest workers.

TABLE I NOTATIONS 

<table><tr><td>Notation</td><td>Description</td></tr><tr><td> $\mathcal{T},\mathcal{T}^{*},\mathcal{W}$ </td><td>Target task set, golden task set, and worker set</td></tr><tr><td> $N,N^{*},M$ </td><td>Number of target tasks, golden tasks and workers</td></tr><tr><td> $w.\tau$ </td><td>Worker  $w$ &#x27;s capacity</td></tr><tr><td> $d_{t},\hat{d}_{t},\mathcal{C}_{t}$ </td><td>Task  $t$ &#x27;s truth, estimated truth, and candidate answer set</td></tr><tr><td> $\mathcal{A},\mathcal{A}^{*}$ </td><td>Workers&#x27; answer set for target tasks and golden tasks</td></tr><tr><td> $\mathcal{B}$ </td><td>Workers&#x27; mapping answer set for target tasks</td></tr><tr><td> $w(a_{i}),t(a_{i})$ </td><td>Answer  $a_{i}$ &#x27;s corresponding worker and task</td></tr><tr><td> $\mathcal{L},K$ </td><td>Topic label set, and number of latent topics</td></tr><tr><td> $\vec{\phi}_{t},\vec{s}_{t}$ </td><td>Task  $t$ &#x27;s latent topic distribution, and truth distribution</td></tr><tr><td> $x_{i},z_{i}$ </td><td>answer  $a_{i}$ &#x27;s bias and its topic label</td></tr><tr><td> $\sigma_{w,k}^{2}$ </td><td>Worker  $w$ &#x27;s reliability for the tasks belonging to topic  $k\in\mathcal{L}$ </td></tr><tr><td> $\vec{\alpha}$ </td><td>Dirichlet hyper-parameters</td></tr><tr><td> $\beta,\gamma$ </td><td>Inverse-Gamma hyper-parameters</td></tr><tr><td> $\mathcal{M}_{t}$ </td><td>Task  $t$ &#x27;s distribution matrix</td></tr><tr><td> $m_{t,k,l}$ </td><td>The possibility that the task  $t$ &#x27;s belongs to topic  $k$ and its truth is  $c_{t,l}\in\mathcal{C}_{t}$ </td></tr></table>

# B. System Design Overview

To achieve our goal, we divide the whole problem into the following three subproblems:

1. Topic-level worker reliability estimation: Profiling workers’ reliability (i.e., expertise and honesty) is the cornerstone for accurate truth inference and optimal task assignment. When a worker w arrives, similar to existing work [22], the platform could assign him/her a set of golden tasks and initialize his/her reliability by his/her answers. However, we notice that many tasks have only coarse-grained descriptions which are neither adequate to profile each worker’s expertise nor to determine optimal task assignment. To achieve more fine-grained reliability, the platform should mine the collection of latent topics L of numeric tasks and then estimate each worker w’s reliability $\sigma _ { w , k } ^ { 2 }$ for each latent topic $k \in { \mathcal { L } }$ .   
2. Truth inference: Given current workers’ reliability and answer set $\mathcal { A }$ for target tasks, the platform needs to calculate the estimated truth $d _ { t }$ of each task t to minimize its expected deviation to the ground truth $d _ { t } ,$ , as well as to estimate the distribution of latent topics and update each worker’s

![](images/d7cdf4c03ae405f32079d4240eab98f30a6ca7c033465b0b1f1593d3480571a8.jpg)



①Target tasks, required answer range and precision ②Capacity ③Golden tasks ④Answers for golden tasks ⑤Topical-level reliability ⑥Target tasks ⑦Answers for target tasks ⑧Topic distribution ŢEstimated truth

Fig. 1. System design overview.

reliability. As more and more answers arrive, the platform should iteratively update the estimated truth, topic distribution and worker reliability.

3. Online task assignment: Given workers’ estimated topiclevel reliability and tasks’ estimated truth, the platform needs to assign each arrived worker the most suitable tasks under his/her capacity constraint, in order to maximize the accuracy of the estimated truth.

As illustrated in Fig. 1, we design a crowdsourcing system consisting of three main modules to address the three subproblems above: Gaussian Latent Topics Estimation(GLTE), Truth Inference(TI) and Online Task Assignment(OTA). The system works as follows:

Step (1): Each task requester publishes a collection of numerical tasks with the same text description, valid answer range, and acceptable precision on the platform.

Step (2)-(5): When a worker w joins the platform, he/she claims his/her capacity w.⌧ , i.e., the maximum number of tasks he/she can perform within a time window, and waits for task assignments. GLTE assigns a small collection of golden tasks to all new workers and collects their answers. GLTE determines the number of topics and divides golden tasks into latent topics according to deviations of collected answers from the ground truth, then initializes each new worker’s topical-level reliability and sends reliability values to OTA and TI. After obtaining answers of target tasks from OTA and estimated truth and topic distribution from TI, GLTE dynamically divides target tasks into latent topics so as to updates each worker’s reliability, and then sends each worker’s updated reliability to OTA and TI.

Step (6)-(7): OTA maintains the answer sets for all tasks. For each available worker w, OTA takes w’s reliability as input and predicts all the answers w may give and how w’s answer will change the truth. OTA utilizes entropy to measure the ambiguity of the predicted truth distribution. It computes entropy of the current truth distribution and the predicted truth distribution for each task, and assigns most suitable tasks to w following the Maximum Reduced Ambiguity principle under the constraint of capacity w.⌧ . Workers complete designated tasks and send their answers to OTA, then OTA sends answers to GLTE and TI.

Step (8)-(9): After obtaining answers of target tasks and workers’ reliability, TI estimates the topic distribution and truth for target tasks. Considering some workers may be dishonest, TI sends the estimated truth and topic distribution to GLTE for updating workers’ reliability.

# III. GAUSSIAN LATENT TOPIC ESTIMATION

In this section, we first discuss the intuitions behind our latent topic based worker reliability model, then we describe the details of our model, the model parameter estimation method based on Gibbs-EM algorithm and the criterion for determining the number of topics.

# A. Intuitions

1) Latent Topics of Tasks: In [20], Du et al. conducted an analysis experiment on BlueBird dataset which was collected by asking 39 workers to provide judgments for 108 images that whether a given image contains a duck. His experiment results inspire us that there exists a finer clustering structure among the tasks with the same truth or text description. In real crowdsourcing systems, it is common that a task description is simple and lacks sufficient information to characterize the fine-grained topic. As an example, a task collecting Wi-Fi signal strength may have latent topics which are clusters for different device types and different frequency bands. Modeling such fine-grained topics obviously can help us to achieve better understanding of workers’ reliability and more accurate final results. However, without explicit description and training data, it is non-trivial to accurately discover such latent topics.

2) Reliability of Workers: Considering the characteristic of numerical tasks, we assume that worker reliability should naturally correspond to how close their answers are to the truth. Following the idea of [15], we use a Gaussian distribution to describe the probability of observing each answer for a task, where the mean parameter is the truth of the task and the variance parameter actually controls how likely answers deviate from the mean, which exactly relates to the reliability of the worker who gives the answer. The challenge here is how to achieve the latent topic-level reliability without knowing the truth.

# B. Model Details

![](images/bbc817a16c4b0d4c4bc61a8c217b0f72db5429392d0f0ded1c7efea708586e04.jpg)



Fig. 2. The probabilistic graphical model of GLTM.

In Fig.2, we show the graphical representation of our GLTM model. Since GLTM is a generative model, we will describe the generation process of each variable, i.e., latent topics of each task, topic-level reliability of each worker, the observed value of each answer, and how they work in our model.

1) Latent Topics: We assume that the tasks could be divided into K topics, in the way that each task belongs to one topic, based on workers’ behaviors. Then we use $\vec { \phi _ { t } } = \{ \phi _ { t , k } \} _ { k = 1 } ^ { K }$ to denote each task $t \mathbf { \bar { s } }$ topic distribution, where each element $\phi _ { t , k }$ denotes the probability that task t belongs to the k-th topic. For each task t, we generate its topic distribution $\vec { \phi _ { t } }$ from a prior Dirichlet distribution with parameters $\vec { \alpha } ,$ formally $\vec { \phi _ { t } } \sim D i r ( \vec { \alpha } )$ .

For answer $a _ { i }$ that the worker $w ( a _ { i } )$ provides for task $t ( a _ { i } )$ , we use a latent topic label $z _ { i }$ to denote which topic $t ( a _ { i } )$ belongs to. $\phi _ { t ( a _ { i } ) , k }$ represents the possibility that $z _ { i }$ is equal to $k .$ In other words, $, z _ { i }$ follows a Categorical distribution parameterized by $\phi _ { t ( a _ { i } ) } ^ { \phantom { } } { } ^ { ' }$ , formally $z _ { i } \sim C a t e g o r i c a l ( \overrightarrow { \phi _ { t ( a _ { i } ) } } )$ .

2) Topic-level reliability: We modified LDA [23] by employing a Gaussian distribution to model the relationship between the bias and their topic-level reliability. We use $\{ \sigma _ { w , k } ^ { 2 } \} _ { k = 1 } ^ { K }$ to represent worker $w ^ { \prime } \mathbf { s }$ topic-level reliability worker where $\sigma _ { w , k } ^ { 2 }$ $w ,$ k  we generate its topic-level reliability denotes $w \mathbf { \bar { s } }$ reliability on the k-th topic. For each $\sigma _ { w , k } ^ { 2 }$ from a prior inverse Gamma distribution with hyper-parameter $( \beta , \gamma )$ where $\beta$ is the shape parameter and $\gamma$ is the scale parameter:

$$
\begin{array}{l} \sigma_ {w, k} ^ {2} \sim I G (\beta , \gamma) \\ \sim \left(\sigma_ {w, k} ^ {2}\right) ^ {- \beta - 1} \exp \left(- \frac {\gamma}{\sigma_ {\mathrm{w} , \mathrm{k}} ^ {2}}\right) \tag {1} \\ \end{array}
$$

The inverse Gamma distribution is adopted becausethe conjugate prior of the Gaussian distribution with $\sigma _ { w , k } ^ { 2 }$ as variance. As a result, the posterior of $\sigma _ { w , k } ^ { 2 }$ w,kis also an inverse Gamma distribution and the MAP inference is more efficient. Its parameter $\beta$ and $\gamma$ controls the prior belief about the distribution of worker topic-level reliability, e.g., the expectation of $\sigma _ { w , k } ^ { 2 }$ is given by $\frac { \gamma } { \beta }$ .

3) Observation of answers: Suppose worker $w ( a _ { i } )$ provided an answer $a _ { i }$ for task $t ( a _ { i } )$ whose truth is $d _ { t ( a _ { i } ) }$ , the bias of $a _ { i }$ is $x _ { i } = a _ { i } - d _ { t ( a _ { i } ) }$ . Based on the latent topic indicator $z _ { i }$ of task $t ( a _ { i } )$ , we can generate $a _ { i }$ from a Gaussian distribution with the truth $d _ { t ( a _ { i } ) }$ as the mean, and the topic-level reliability  2w(ai),zi $\sigma _ { w ( a _ { i } ) , z _ { i } } ^ { 2 }$ as the variance:

$$
a _ {i} \sim N (d _ {t (a _ {i})}, \sigma_ {w (a _ {i}), z _ {i}} ^ {2}) \tag {2}
$$

# C. Parameter Estimation

As mentioned above, we estimate the parameters by assigning the golden tasks to the workers. After receiving the answers of golden tasks, we can calculate the bias X of these answers to the ground truths. Then we can divide the tasks into latent topics based on workers’ biases on golden tasks and initialize workers’ topic-level reliability.

For simplicity, we use $\Omega = \{ \beta _ { w , k } , \gamma _ { w , k } \} _ { w = 1 , k = 1 } ^ { M , K }$ to denote the hyper-parameters of workers’ topic-level reliability distribution. Given the construction of GLTM, the complete likelihood of observed data and unknown parameters given the hyper-parameters can be written as $p ( X | \vec { \alpha } , \Omega )$ . Our objective is to learn the optimal model parameters (\~↵, ⌦) which maximize $p ( X | \vec { \alpha } , \Omega )$ . However, it is difficult to directly compute the likelihood $p ( X | \vec { \alpha } , \Omega )$ . Therefore, We propose our parameter estimation method based on Gibbs-EM [24], [25] to find the optimal model parameters by iteratively sampling latent variables and update the parameters.

Algorithm 1: Parameter Estimation   
Input: Golden task set $\mathcal{T}^*$ , Ground truth set $\{d_{t^*}\}_{t^* \in \mathcal{T}^*}$ , Worker set $\mathcal{W}$ , Answer set $\mathcal{A}^*$ , Latent topic number $K$ Output: Tasks' topic distribution $\vec{\phi}_t$ , Worker topic-level expertise $\{\sigma_{w,k}^2\}_{w=1,k=1}^{M,K}$ 1 Initialize latent variable $X$ where each element $x_i$ denotes the deviation between the answer and the ground truth;

2 Initialize latent topic labels $Z$ and the hyper-parameter $\vec{\alpha}$ and $\{\beta_{w,k}, \gamma_{w,k}\}_{w=1,k=1}^{M,K}$ ;

3 while not converge do

4 // E-step

5 for each observation $a_i \in \mathcal{A}^*$ do

6 Sample the latent topic label $z_i$ according to Equation (4);

7 end

8 // M-step

9 Update $\vec{\alpha}$ by using Newton's method $\vec{\alpha}_{new} = \vec{\alpha}_{old} - H^{-1}g\vec{\alpha}$ ;

10 Update $\vec{\phi}$ according to Equation (5);

11 Update $\beta, \gamma$ according to Equation (6);

12 Update $\sigma_{w,k}^2$ according to Equation (7);

13 end

14 return $\{\sigma_{w,k}^2\}_{w=1,k=1}^{M,K}$ for each worker $w \in \mathcal{W}$ , $\vec{\phi}_t$ for each golden task $t^* \in \mathcal{T}^*$ .

In the E-step, we employ a Gibbs sampler to sequentially sample each latent variables $z _ { i }$ from the distribution over this variable given the bias X and all other latent variables Z i. The conditional posterior of $z _ { i }$ can be computed:

$$
\begin{array}{l} p \left(z _ {i} = k \mid Z _ {\neg i}, X, \vec {\alpha}, \Omega\right) = \frac {p (Z , X \mid \vec {\alpha} , \Omega)}{p \left(Z _ {\neg i} , X _ {\neg i} \mid \vec {\alpha} , \Omega\right)} \tag {3} \\ \propto \frac {p (Z | \vec {\alpha})}{p (Z _ {\neg i} | \vec {\alpha})} \frac {p (X | Z , \Omega)}{p (X _ {\neg i} | Z _ {\neg i} , \Omega)} \\ \end{array}
$$

Given the Dirichlet-Multinomial conjugacy and Inverse Gamma-Gaussian conjugacy, we can sequentially sample zi:

$$
\begin{array}{l} p \left(z _ {i} = k \mid Z _ {\neg i}, X, \vec {\alpha}, \Omega\right) \propto \left(n _ {t \left(a _ {i}\right), z _ {i}} + \alpha_ {z _ {i}}\right) \tag {4} \\ \cdot N (x _ {i}; 0, \sigma_ {w (a _ {i}), z _ {i}} ^ {2}) \\ \end{array}
$$

In the M-step, we update the model parameters $( \vec { \alpha } , \Omega )$ with sampled latent variables. letting $\{ Z ^ { ( r ) } \} _ { r = 1 } ^ { R }$ be the generated latent variables, we firstly estimate the hyper-parameters of Dirichlet-Multinomial distribution \~↵. Following the idea of [20], [24], we use the Newton’s method to update the ${ \vec { \alpha } } ,$ formally $\overrightarrow { \alpha _ { n e w } } \ = \ \overrightarrow { \alpha _ { o l d } } - H ^ { - 1 } g \overrightarrow { \alpha }$ . Here, $H ^ { - 1 }$ denotes the

Hessian matrix and $g \vec { \alpha }$ denotes the gradient of the loglikelihood $p ( Z | \vec { \alpha } )$ . [24] gives the detail of how to compute $H ^ { - 1 }$ and $g \vec { \alpha } ,$ we omit it due to the space limitation.

Then, based on the properties of multinomial distribution, the probability that a task t belongs to the k-th topic can be computed by:

$$
\phi_ {t, k} = \frac {n _ {t , k} + \alpha_ {k}}{n _ {t} + \sum_ {k = 1} ^ {K} \alpha_ {k}} \tag {5}
$$

Here $n _ { t }$ denotes the number of answers that are collected for the task t and $n _ { t , k }$ denotes the times that t is assigned with the latent topic label k.

At last, we can update the hype-parameters of workers’ topic-level reliability $\mathrm { \dot { \{ \beta _ { w , k } , \gamma _ { w , k } \} } } _ { w = 1 , k = 1 } ^ { \dot { M } , \dot { K } }$ as follows:

$$
\begin{array}{l} \beta_ {w, k} ^ {\text { new }} = \beta_ {w, k} ^ {\text { old }} + \frac {n _ {w , k}}{2} \\ \gamma_ {w, k} ^ {\text { new }} = \gamma_ {w, k} ^ {\text { old }} + \frac {\sum_ {t \in T _ {w , k} ^ {*}} x _ {t , w , k}}{2} \tag {6} \\ \end{array}
$$

Here $n _ { w , k }$ is the times that the worker w answers the tasks belonging to the k-th topic, $x _ { t , w , k }$ is the bias that w answers the task t belonging to the k-th topic and $T _ { w , k } ^ { * }$ is the set of golden tasks that w has answered which are belonging to the k-th topic.

Based on the properties of Inverse Gamma distribution, w’s reliability on the k-th topic can be estimated by

$$
\sigma_ {w, k} ^ {2} = \frac {\gamma_ {w , k}}{\beta_ {w , k}} \tag {7}
$$

# D. Topic Number Selection

The selection of the topic numbers K is crucially important. We introduce the integrated completed likelihood(ICL) [26] to help us determine the topic numbers, which computes the expectation of the joint probability of the observations and latent variables. Formally, the ICL value of a fixed topic number K can be computed by:

$$
\begin{array}{l} I C L (K) = \log \int_ {(\vec {\alpha}, \Omega)} p (X, Z | \vec {\alpha}, \Omega) p (\vec {\alpha}, \Omega) d \vec {\alpha} d \Omega \tag {8} \\ = \log \int_ {(\vec {\alpha}, \Omega)} p (X | Z, \Omega) p (Z | \vec {\alpha}) p (\vec {\alpha}, \Omega) d \vec {\alpha} d \Omega \\ \end{array}
$$

We use $\hat { \vec { \alpha } } , \hat { \Omega }$ to represent the estimation of Bayesian model parameters obtained by the Gibbs-EM algorithm. As in literature [27], we use the MAP estimations to replace the latent variables Z, formally as $: \hat { Z } = \arg \operatorname* { m a x } _ { Z } p ( Z | X , \hat { \vec { \alpha } } , \hat { \Omega } )$ .

Following the idea of [20], [28], we employ the Bayesian information criterion (BIC) to obtain a BIC-like approximation for ICL:

$$
\begin{array}{l} I C L (K) \simeq \log p (\hat {Z} | \hat {\vec {\alpha}}) + \log p (X | \hat {Z}, \hat {\Omega}) \\ - \frac {K}{2} \log | X | - K \sum_ {w = 1} ^ {W} \log \left| X ^ {w (a _ {i})} \right| \tag {9} \\ \end{array}
$$

Here $\left| X ^ { w ( a _ { i } ) } \right|$ is the number of answers that worker w has submitted.

# IV. TRUTH INFERENCE

The intuition of our truth inference mechanism is twofold: (1) For a task t, if a worker has a high reliability on the topic of t, it is more likely that the truth of task t is closer to his/her answer; (2) For a worker w, if w’s answers often have low biases for a certain topic, this worker should have a high reliability level on this topic. Therefore, our truth inference method, namely TI-GLTM, has two steps: firstly, we infer the truth and topic distribution based on workers’ topic-level reliability and their answers; secondly, we update worker topic-level reliability based on the biases between their answers and the inferred truth in the first step.

Step 1: Inferring the truth and topic. Based on workers’ topical-level reliability and their answers for a task t, we need to estimate the truth and topic distribution of t.

The complete likelihood of observed data and unknown parameters is:

$$
\begin{array}{l} p (A ^ {(t)}, Z | d _ {t}, \vec {\phi_ {t}}) \\ = \prod_ {i = 1} ^ {| A ^ {(t)} |} p (a _ {i}, z _ {i} | d _ {t}, \vec {\phi_ {t}}) \\ = \prod_ {i = 1} ^ {| A ^ {(t)} |} \prod_ {k = 1} ^ {K} [ \phi_ {t, k} \cdot N (a _ {i}; d _ {t}, \sigma_ {w (a _ {i}), k} ^ {2}) ] ^ {\mathbb {I} (z _ {i} = k)} \tag {10} \\ = \prod_ {k = 1} ^ {K} \phi_ {t, k} ^ {\sum_ {i = 1} ^ {| A (t) |} \mathbb {I} (z _ {i} = k)} \prod_ {i = 1} ^ {| A (t) |} [ N (a _ {i}; d _ {t}, \sigma_ {w (a _ {i}), k} ^ {2}) ] ^ {\mathbb {I} (z _ {i} = k)} \\ \end{array}
$$

Here, $\mathbb { I } ( z _ { i } = k )$ is an indicator function which returns 1 if $z _ { i } = k$ and otherwise return 0.

Next, we will briefly describe an EM algorithm that estimates truth $d _ { t }$ and topic distribution $\vec { \phi _ { t } }$ for t.

In the E step, we compute the expectation of the completedata log-likelihood function, with respect to the conditional distribution of latent variable Z under the current estimation of parameters $( d _ { t } , \vec { \phi _ { t } } )$ :

$$
\begin{array}{l} Q (d _ {t} ^ {n e w}, \vec {\phi_ {t}} ^ {n e w} | d _ {t} ^ {o l d}, \vec {\phi_ {t}} ^ {o l d}) = E _ {Z} [ \ln p (A ^ {(t)}, Z | d _ {t}, \vec {\phi_ {t}}) ] \\ = \sum_ {k = 1} ^ {K} [ (\sum_ {i = 1} ^ {| A ^ {(t)} |} E [ \mathbb {I} (z _ {i} = k) | a _ {i}, d _ {t} ^ {o l d}, \vec {\phi_ {t}} ^ {o l d} ]) \cdot \ln \phi_ {t, k} \\ + \sum_ {i = 1} ^ {| A ^ {(t)} |} E [ \mathbb {I} (z _ {i} = k) | a _ {i}, d _ {t} ^ {o l d}, \vec {\phi_ {t}} ^ {o l d} ] \cdot (- \ln (2 \pi) - \frac {1}{2} \ln \sigma_ {w (a _ {i}), k} \\ \left. - \frac {\left(a _ {i} - d _ {t}\right) ^ {2}}{2 \sigma_ {w \left(a _ {i}\right) , k} ^ {2}}\right) ] \tag {11} \\ \end{array}
$$

Based on this equation, we can introduce the conditional probability of latent variable Z:

$$
\begin{array}{l} E [ \mathbb {I} (z _ {i} = k) | a _ {i}, d _ {t} ^ {o l d}, \vec {\phi} _ {t} ^ {o l d} ] = \\ \phi_ {t, k} ^ {\text {old}} * N (a _ {i}; d _ {t} ^ {\text {old}}, \sigma_ {w (a _ {i}), k} ^ {2}) \tag {12} \\ \overline {{\sum_ {k = 1} ^ {K} \phi_ {t , k} ^ {o l d} * N (a _ {i} ; d _ {t} ^ {o l d} , \sigma_ {w (a _ {i}) , k} ^ {2})}} \\ \end{array}
$$

In the M step, we compute the truth $d _ { t }$ by solving @Q = 0, $\begin{array} { r } { \frac { \partial Q } { \partial d _ { t } } = 0 . } \end{array}$ @dt which is :

$$
d _ {t} ^ {\text { new }} = \frac {\sum_ {i = 1} ^ {| A ^ {(t)} |} \sum_ {k = 1} ^ {K} \frac {E [ \mathbb {I} (z _ {i} = k) | a _ {i} , d _ {t} ^ {\text { old }} , \vec {\phi} _ {t} ^ {\text { old }} ] * a _ {i}}{\sigma_ {w (a _ {i}) , k} ^ {2}}}{\sum_ {i = 1} ^ {| A ^ {(t)} |} \sum_ {k = 1} ^ {K} \frac {E [ \mathbb {I} (z _ {i} = k) | a _ {i} , d _ {t} ^ {\text { old }} , \vec {\phi} _ {t} ^ {\text { old }} ]}{\sigma_ {w (a _ {i}) , k} ^ {2}}} \tag {13}
$$

Similarly we can get the optimal estimate for $\vec { \phi _ { t } }$ by solving @[Q+ ( PKk=1  t,k 1)] = 0, which is : $\begin{array} { r } { \frac { \partial [ Q + \lambda ( \sum _ { k = 1 } ^ { K ^ { ^ { \prime } } } \phi _ { t , k } - 1 ) ] } { \partial \phi _ { t , k } } = 0 } \end{array}$ @ t,k

$$
\phi_ {t, k} ^ {\text { new }} = \frac {\sum_ {i = 1} ^ {| A ^ {(t)} |} E [ \mathbb {I} (z _ {i} = k) | a _ {i} , d _ {t} ^ {\text { old }} , \vec {\phi} _ {t} ^ {\text { old }} ]}{| A ^ {(t)} |} \tag {14}
$$

Step 2: Updating worker topic-level reliability. According to Equation (13) and (14), we can obtain the estimated truth and current topic distribution of each task. TI module will send them to the GLTE module for updating the workers’ topiclevel reliability. After receiving the truth and current topic distribution from TI module and answers of all tasks from OTA module, GLTE module will sample the latent variables $z _ { i }$ from the topic distribution for each observation $x _ { i }$ and then update workers’ topical-level reliability according to Equation (6) and Equation (7) in Section III-C.

# V. ONLINE TASK ASSIGNMENT MECHANISM

In this section, we first describe our preprocessing step to map the workers’ continuous answers to discrete candidate answers. Then we show the computation process of current distribution matrix. Finally, we propose an online task assignment mechanism MRA-GLTM which dynamically assigns tasks to incoming workers according to the Maximum Reduced Ambiguity principle.

# A. Preprocessing

For the online task assignment, we need to consider the possible answers the arriving worker may give and how each answer will affect the result. However, for numerical tasks, the possible answer can be any number within a range. Given the answer range and precision by the requester, we map workers’ continuous answers to discrete candidate answers so as to enumerate all the possible answers that the arriving worker may provide. For each target $t , \ [ e _ { t , m i n } , e _ { t , m a x } ]$ denotes the answer range and $\delta _ { t }$ denotes the precision. We consider $a _ { i }$ as an invalid value when $a _ { i } \notin [ e _ { t , m i n } , e _ { t , m a x } ]$ . The following function is used to map $a _ { i }$ to the discrete value:

$$
F (a _ {i}) = e _ {t, m i n} + \left\lfloor \frac {a _ {i} - e _ {t , m i n}}{\delta_ {t}} \right\rfloor \tag {15}
$$

Let $C _ { t } = \{ c _ { t , 1 } , c _ { t , 2 } , . . . , c _ { t , l _ { t } } \}$ be the set of candidate answers and $l _ { t }$ be the number of candidate answers. After the mapping, we use $\boldsymbol { B }$ to represent the set of discrete workers’ answers. For each discrete answer $b _ { i } \in B , w ( b _ { i } )$ denotes the worker who gives the discrete answer $b _ { i }$ and $t ( b _ { i } )$ is the tasks associated to the answer $b _ { i }$ .

# B. Distribution Matrix

Based on the workers’ topic-level reliability and their answers on a task t, we can estimate the truth and topic distribution of t. Inspired by [20], we use a distribution matrix to store the estimated distribution of truth and topic.

Definition 1 (Distribution matrix): For a task t, let K be the number of latent topics and $\boldsymbol { C _ { t } } ~ = ~ \{ c _ { t , 1 } , c _ { t , 2 } , . . . , c _ { t , l _ { t } } \}$ be the candidate answers. We use a matrix $\mathcal { M } _ { t }$ to store the distribution of task $t \mathbf { \hat { s } }$ topic and truth, where each element $m _ { t , k , l }$ represents the possibility that the topic of t is k and the truth of t is $c _ { t , l } .$ .

For each target task $t ,$ we use $X _ { t \vert c _ { t , l } }$ to denote the bias of answers $B ^ { ( t ) }$ given truth $c _ { t , l }$ and then show how to compute each element $m _ { t , k , l }$ in the distribution matrix $\mathcal { M } _ { t }$ .

$$
m _ {t, k, l} = p (z _ {t} = k, d _ {t} = c _ {t, l} | B ^ {(t)}, \Omega)
$$

$$
= p (z _ {t} = k, d _ {t} = c _ {t, l}, B ^ {(t)} | \Omega) p (B ^ {(t)} | \Omega)
$$

$$
\propto p (z _ {t} = k, d _ {t} = c _ {t, l}, B ^ {(t)} | \Omega) \tag {16}
$$

$$
\propto p (z _ {t} = k, d _ {t} = c _ {t, l}) p (X _ {t | c _ {t, l}} | z _ {t} = k, \Omega)
$$

$$
\cdot p (B ^ {(t)} | d _ {t} = c _ {t, l}, z _ {t} = k, X _ {t | c _ {t, l}})
$$

In Equation (16), $p ( d _ { t } \ = \ c _ { t , l } , z _ { t } \ = \ k )$ represents the prior probability that a task with truth $d _ { t , l }$ belongs to a topic $k .$ Combining Equation (2) and the definition of topic-level reliability, we can further compute each element $m _ { t , k , l }$ as follows:

$$
m _ {t, k, l} = p (d _ {t} = c _ {t, l}, z _ {t} = k) \prod_ {b _ {i} \in \mathcal {B} ^ {(t)}} N (b _ {i} | c _ {t, l}, \sigma_ {w (b _ {i}), k} ^ {2}) \tag {17}
$$

To keep the sum of the elements in the distribution matrix $M ^ { ( t ) }$ to 1, we normalize the $m _ { t , k , l }$ as follows:

$$
m _ {t, k, l} = \frac {m _ {t , k , l}}{\sum_ {k = 1} ^ {K} \sum_ {l = 1} ^ {l _ {t}} m _ {t , k , l}} \tag {18}
$$

For a task t, we use $\vec { s _ { t } } = \left\{ s _ { t , 1 } , s _ { t , 2 } , . . . , s _ { t , l _ { t } } \right\}$ to denote $t \mathbf { \bar { s } }$ truth distribution, where $s _ { t , l }$ represents the probability that $c _ { t , l }$ is the truth for t. Combining Definition 1 and the definition of truth distribution, $\vec { s _ { t } }$ can be computed by considering all latent topics, formally st,l = PKk=1 mt,k,l. $\begin{array} { r } { s _ { t , l } = \sum _ { k = 1 } ^ { K } m _ { t , k , l } } \end{array}$

# C. MRA-GLTM

To address the online task assignment problem, we need to evaluate the benefit of an assignment. Inspired by [11], our mechanism MRA-GLTM considers the ambiguity can be reduced by assigning a task to the arriving worker and assigns the arriving worker a set of tasks with maximum reduced ambiguity (MRA). Before demonstrating the reduced ambiguity, we first define the ambiguity of the truth distribution.

Definition 2 (Ambiguity of truth distribution): For a task t, let $\vec { s _ { t } } = \left\{ s _ { t , 1 } , s _ { t , 2 } , . . . , s _ { t , l _ { t } } \right\}$ be the distribution of t’s truth. The ambiguity of the truth distribution $\vec { s _ { t } }$ is defined as entropy of $\vec { s _ { t } } ,$ , which is $\begin{array} { r } { H ( \vec { s _ { t } } ) = - \sum _ { l = 1 } ^ { l _ { t } } s _ { t , l } \cdot \ln { s _ { t , l } } } \end{array}$ .

As Definition 2 shows, for each task t, we could compute the current ambiguity of t’s truth distribution $H ( \vec { s _ { t } } ) . H ( \overrightarrow { s _ { t } ^ { \psi } } )$ is the ambiguity of the updated truth distribution of t if it is assigned to a worker w. However, $H ( \vec { s _ { t } ^ { w } } )$ is not easy to compute since we cannot estimate $\overrightarrow { s _ { t } ^ { \psi } }$ before t is really answered by w. Assuming the answer that w provides for t is $b _ { t , w } ,$ we can update the truth distribution with w’s topic-level reliability. Letting $\overrightarrow { s _ { t } , w }$   !bt,w denote the updated truth distribution of t after receiving can be computed by w’s answer $b _ { t , w }$ , the ambiguity of updated truth distribution $\begin{array} { r } { H ( s _ { t } ^ { b _ { t } , w } ) = - \sum _ { l = 1 } ^ { l _ { t } } s _ { t , l } ^ { b _ { t , w } } \cdot \ln s _ { t , l } ^ { b _ { t , w } } } \end{array}$ s bt,w ·ln s bt, w . We use the weighted sum of the ambiguity of task t’s truth distribution when worker w provides different answers to compute $H ( \overrightarrow { s _ { t } ^ { w } } )$ :

$$
H \left(\overrightarrow {s _ {t} ^ {w}}\right) = \sum_ {b _ {t, w} \in C _ {t}} p \left(b _ {t, w} \mid B ^ {(t)}, \left\{\sigma_ {w, k} ^ {2} \right\} _ {k = 1} ^ {K}\right) \cdot H \left(\overrightarrow {s _ {t} ^ {b _ {t , w}}}\right) \tag {19}
$$

Here $p ( b _ { t , w } | B ^ { ( t ) } , \{ \sigma _ { w , k } ^ { 2 } \} _ { k = 1 } ^ { K } )$ represents the probability that a worker w provides an answer $b _ { t , w }$ for a task t when the current collected answers are $B ^ { ( t ) }$ . Based on w’s topical-level reliability, we can obtain the probability that w submits $b _ { t , w }$ by enumerating all the topics and truth:

$$
\begin{array}{l} p (b _ {t, w} | B ^ {(t)}, \{\sigma_ {w, k} ^ {2} \} _ {k = 1} ^ {K}) \\ = \sum_ {k = 1} ^ {K} \sum_ {l = 1} ^ {l _ {t}} p (b _ {t, w} | z _ {t} = k, d _ {t} = c _ {t, l}, \sigma_ {w, k} ^ {2}) \cdot m _ {t, k, l}. \tag {20} \\ \end{array}
$$

where $p ( b _ { t , w } | z _ { t } ~ = ~ k , d _ { t } ~ = ~ c _ { t , l } , \sigma _ { w , k } ^ { 2 } )$ can be computed according to Equation (2).

To compute $H ( s _ { t } ^ { b _ { t } , w } )$   !bt,w , we should first update the distribution matrix and normalize it as follows:

$$
\begin{array}{l} m _ {t, k, l} ^ {b _ {t, w}} \propto m _ {t, k, l} \cdot p (b _ {t, w} | z _ {t} = k, d _ {t} = c _ {t, l}, \sigma_ {w, k} ^ {2}) \\ = \frac {m _ {t , k , l} \cdot p (b _ {t , w} | z _ {t} = k , d _ {t} = c _ {t , l} , \sigma_ {w , k} ^ {2})}{\sum_ {k = 1} ^ {K} \sum_ {l = 1} ^ {B _ {t}} m _ {t , k , l} \cdot p (b _ {t , w} | z _ {t} = k , d _ {t} = c _ {t , l} , \sigma_ {w , k} ^ {2})}. \tag {21} \\ \end{array}
$$

Then based on the definition of truth distribution, we have $\begin{array} { r } { s _ { t , l } ^ { b _ { t , w } } = \sum _ { k = 1 } ^ { K } m _ { t , k , l } ^ { b _ { t , w } } } \end{array}$ s t,l bt,w PKk=1 m t,k,l bt,w and compute

$$
\begin{array}{l} H (\overrightarrow {s _ {t} ^ {b _ {t , w}}}) = - \sum_ {l = 1} ^ {l _ {t}} s _ {t, l} ^ {b _ {t, w}} \cdot \ln s _ {t, l} ^ {b _ {t, w}} \\ = - \sum_ {l = 1} ^ {l _ {t}} (\sum_ {k = 1} ^ {K} m _ {t, k, l} ^ {b _ {t, w}}) \cdot \ln (\sum_ {k = 1} ^ {K} m _ {t, k, l} ^ {b _ {t, w}}). \\ \end{array}
$$

Finally, we substitute Equation (20) and Equation (22) into Equation (19) to compute $\bar { H } ( \overrightarrow { s _ { t } ^ { u } } )$ .

Letting $G _ { t } ^ { w }$ be the reduce ambiguity of task t’s truth distribution when t is assigned to a worker w, it can be computed as follows:

$$
G _ {t} ^ {w} = H (\vec {s _ {t}}) - H (\overrightarrow {s _ {t} ^ {w}}). \tag {23}
$$

Based on the reduced ambiguity, MRA-GLTM assigns a set of tasks $V _ { w }$ to the arriving worker to obtain maximal reduced ambiguity, with the constraint that the number of assigned tasks $| V _ { w } |$ | can not exceed the worker capacity w.⌧ . In Algorithm 2, we present the details of our MRA-GLTM method.

Algorithm 2: Online Task Assignment: MRA-GLTM   
Input: Capacity $w.\tau$ , Topic-level Reliability $\sigma_{w,k}^{2}$ , unsigned target task set $U_w$ , task current information ( $M_t, \vec{s}_t$ )
Output: Task Assignment $V_w$ for worker $w$ 1 Initialize assignment set $V_w := \emptyset$ ;
2 for each task $t \in U_w$ do
3    compute reduced ambiguity of task $t$ 's truth distribution $G_t^w$ if task $t$ assigned to worker $w$ by using Equation (23);
4 end
5 while $|V_w| < s_w$ do
6    Select the optimal task $t \in U_w - V_w$ with maximum reduced ambiguity $G_t^w$ ;
7    Add task $t$ to assignment set $V_w$ so that $V_w := V_w \cup \{t\}$ ;
8 end
9 Assign the tasks within task set $V_w$ to worker $w$ ;

# VI. EVALUATION RESULTS

In this section, we conduct a series of experiments on a simulated dataset and a real crowdsourcing dataset. We first describe our experimental setup, then evaluate our truth inference method TI-GLTM and online task assignment mechanism MRA-GLTM by comparing with the state-of-the-art approaches.

# A. Experimental Setup

1) Datasets: A simulated dataset and a real crowdsourcing dataset Valence [29] are used for our experiments.

Simulated dataset: We generate a simulated dataset based on a real numerical dataset [30], which records the PM2.5 data from different places collected by crowd workers. We randomly select 150 places and regard the PM2.5 data of each place as the ground truth of each task. We assume there are 4 latent topics among the tasks and 30 workers are willing to answer the tasks. For each task t, we generate its latent topic distribution from a prior Dirichlet distribution Dir(1, 1, 1, 1) and then sample the latent topic $z _ { t }$ from this latent topic distribution. For each worker, we generate his topic-level reliability Based on the latent to $\delta _ { w , k } ^ { 2 }$ when the variance is 1 and 10.nd workers’ topical-level reliability, we generate the answer $a _ { i }$ that worker $w ( a _ { i } )$ gives for task $t ( a _ { i } )$ by sampling a value from the Gaussian distribution with ground truth $d _ { t ( a _ { i } ) }$ as the mean and $\delta _ { w , z _ { i } } ^ { 2 }$ as the variance.

Valence: Valence [29] is a set of numeric ratings in the interval [-100,100], each of which denotes the overall positive or negative valence of the emotional content of the headline and is collected on the AMT platform. It contains 100-headline sample tasks, and collects 10 answers for each of the headline from all 38 worker.

2) Comparisons: We compare TI-GLTM with Average, Median, KDEm [31] and GTM [15], which study truth inference on numerical tasks. Average regards the truth of a task as the average value of all answers. Median regards the truth of a task as the median of all answers. KDEm is a nonparametric approach, which is proposed to estimate the opinion distribution and worker reliability score simultaneously. GTM models each worker’s reliability as the variance of a uni-Gaussian distribution and iteratively infers the truth and workers’ reliability based on EM algorithm.

We compare MRA-GLTM with RR-MV [32], MEG-LTM [20], MEPG-LTM [20] and Optimal assignment, which study online task assignment. RR-MV uses majority voting method to infer the truth and randomly selects tasks for the incoming worker. Du et al. [20] designed latent topic model (LTM) to capture workers’ fine grained reliability and then dynamically assign each incoming worker a set of tasks with the maximum expected gain (MEG) and the maximum expected potential gain (MEPG). Optimal assignment is the best assignment when we know the answers and truth of all the tasks.

3) Performance Metric: Considering the characteristic of numerical tasks, we use Mean Absolute Error(MAE) and Mean Square Error(MSE) to evaluate our truth inference method TI-GLTM and online task assignment method MRA-GLTM. Besides, we add the metric Number of Assignments for MRA-GLTM.

Mean Absolute Error(MAE) measures the overall absolute error between each method’s outputs and the ground truth, which is computed by averaging the absolute difference over all tasks :

$$
M A E = \frac {1}{n} \sum_ {t = 1} ^ {n} \| d _ {t} ^ {\text { new }} - d _ {t} \| \tag {24}
$$

• Mean Square Error(MSE) is computed by taking the square of the mean difference between each method’s outputs and the ground truth :

$$
M S E = \frac {1}{n} \sum_ {t = 1} ^ {n} \| d _ {t} ^ {\text { new }} - d _ {t} \| ^ {2} \tag {25}
$$

Number of Assignment is used to record the number of votes that an online task assignment mechanism collects in an experiment.

# B. Performance of Truth Inference

In this section, we evaluate TI-GLTM by conducting several experiments on simulated and real dataset. For simulated dataset, we compare the performance of truth inference method when the answers for each task change. For real dataset Valence, we first determine the number of the latent topics by computing the ICL value and then compare TI-GLTM with other methods.

Simulated dataset. We compare the performance of truth inference methods on the simulated dataset when the answers for each task vary from 5 to 30 and plot the results in Fig.3 and Fig.4. We have the following observations: (1) MAE and MSE of all methods decrease as the number of workers’ answers for each target task increases and TI-GLTM performs better than other methods with lower MAE and MSE. (2) Average and Median perform worse than TI-GLTM since they do not consider the worker reliability; (3) KDEm and GTM do not consider the latent topics among the tasks so they have higher MAE and MSE than TI-GLTM.

![](images/387cbb5116babaf7ce4e1f5e54869804c2ea31cee92e07cd7208249ee23f5008.jpg)



![](images/b72cd08c211c7d6f7469925f2a8da0ec53713d4d9cbe2ee6f52ffeffb6245a07.jpg)



Fig. 3. MAE w.r.t. the number of Fig. 4. MSE w.r.t. the number of worker answer worker answer

Valence. We first need to determine the number of latent topics in Valence. According to Section III-D, we use ICL to select the most suitable number of latent topics. We run the parameter estimation algorithm and calculate the ICL value when the number of latent topics varies from 1 to 5. As table II shows, ICL gets the maximum value when K = 2. Therefore, we assume the dataset Valence has 2 latent topics.

TABLE II ICL VALUE ON VALENCE 

<table><tr><td>K</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td></tr><tr><td>ICL</td><td>-608.39</td><td>-567.93</td><td>-584.17</td><td>-659.85</td><td>-706.33</td></tr></table>

Next, we evaluate five methods on the Valence dataset. Table III shows that TI-GLTM has clearly lower MAE and MSE than other methods on the Valence dataset.

TABLE III TI RESULT ON VALENCE 

<table><tr><td>Method</td><td>Average</td><td>Median</td><td>KDEm</td><td>GTM</td><td>TI-GLTM</td></tr><tr><td>MAE</td><td>21.6</td><td>26.4</td><td>29.9</td><td>27.2</td><td>20.5</td></tr><tr><td>MSE</td><td>665</td><td>968</td><td>1295</td><td>1091</td><td>611</td></tr></table>

# C. Performance of Online Task Assignment

In the experiments, we generate a training set on the simulated dataset with 20 golden tasks to estimate workers’ topicallevel reliability and generate a test set which contains workers’ answers for 100 simulated target tasks. We first conduct the preprocessing to map all the answers to discrete candidate answers. We set answer range as [1, 30] and precision as 1, so the candidate answer set is the integer in [1, 30] and the number of candidate answers is 30. Then we utilize the random permutation model [33] to determine a fixed arrival order. To evaluate an online task assignment mechanism with a worker capacity, we first estimate workers’ topic-level reliability on the training set, then perform the task assignment mechanism with the fixed arrival order on the test set, and finally evaluate the mechanism by its average performance over 1000 rounds of simulations.

In Fig.5, Fig.6 and Fig.7, we compare the performance of online task assignment mechanism when the worker capacity varies from 10 to 100. We have the following observations: (1) As Fig.5 and Fig.6 show, MAE and MSE of all the methods have a downward trend when the capacity increases. RR-MV performs worst as it does not consider the worker’s reliability and tasks’ information. MEG-LTM and MEPG-LTM perform better since they consider the latent topic among tasks, but their worker reliability model is not suitable for numeric tasks. Our proposed online task assignment mechanism outperforms other three methods but a little worse than Optimal. (2) As Fig.7 shows, comparing with other three methods, our MRA-GLTM uses the least number of assignments to achieve the best performance given the same capacity.

![](images/865454bd8d70efd7694a63241968877019e5be362f962e91eeec889fac8cc39c.jpg)



Fig. 5. MAE w.r.t. capacity

![](images/8ff92472840cc984beabdbf4511562788a0092518e7dd9da44ed9d622400c5a8.jpg)



Fig. 6. MSE w.r.t. capacity

![](images/1fc144cc83438304744ac8c27612a8ef74fbc3c0015fc7a09b565735f59dbcfa.jpg)



Fig. 7. Number of Assignments w.r.t. capacity

# VII. RELATED WORK

Worker reliability model. Most of early work [16], [34], [35] utilized the worker probability model to capture the worker reliability which regards the worker reliability as a single value and assumes workers have the same reliability on all tasks. [36] and [37] utilized confusion matrix to model workers’ reliability on labels and infer the correct label. Ma et al. [10] modified the LDA [23] to divide tasks into different domains based on the task descriptions and further capture workers’ domain-level reliability. Du et al. [12], [20] proposed latent topic model to divide tasks into topics based on workers’ behavior and estimate workers’ topic-level expertise. Different from existing work, we propose a new worker reliability model named Gaussian Latent topic model to divide numerical tasks into latent topics based on worker bias between their answers and the truth and estimate workers’ topic-level reliability.

Truth Inference. Average and Median is the most intuitive methods for numerical tasks to infer the truth, which selects the average and median value as the estimated truth. Considering the workers’ reliability, many truth inference approaches [15], [16], [31] have been proposed to estimate workers’ reliability and infer the truth iteratively based on Expectation-Maximization (EM) strategy. Although these methods could be applied on numerical tasks, none of them consider the latent topics among tasks with the same description and ignore that workers have different reliability levels on different topics.

Task Assignment. Early work usually employs Round-Robin(RR) that randomly assigns tasks for the incoming workers. [32] incorporated the worker probability model to estimate incoming workers’ performance on the tasks. QASCA [9] employed the confusion matrix model to conduct the task assignment by allocating the tasks with maximum accuracy (or F1-score) gains to each incoming worker. [11] proposes Domain-aware reliability model to divide tasks into different domains based on the existing knowledge base and further conducts task assignments based on workers’ domain-level expertise. Du et al. [20] proposed a latent topic model to divide tasks into latent topics based on workers’ behavior and propose two online task assignment mechanisms MEG-LTM and MPEG-LTM, which utilize incoming workers’ topiclevel expertise to compute task assignment plans so that the Maximum Expected Gain (MEG) or Maximum Expected Potential Gain (MPEG) can be achieved. Different from existing methods, considering the characteristics of numerical tasks, we propose a novel worker reliability model GLTM to capture workers’ topic-level reliability and design an online task assignment MRA-GLTM to assign appropriate tasks to the incoming worker.

# VIII. CONCLUSION

In this paper, we propose a solution to improve the result quality of crowdsourced numerical tasks by building a fine-grained worker reliability model named Gaussian Latent Topic Model(GLTM), which mines latent topics of numerical tasks and quantifies each workers’ topical-level reliability. A novel expectation-maximization based iterative method for truth inference is designed to first estimate the truth and the distribution of latent topics, and then dynamically update each worker’s reliability. Finally, we design an online task assignment mechanism to assign each worker a set of tasks with maximum reduced ambiguity principle. We conduct experiments on a simulated dataset and a real-world dataset, which testify the merits of our solution.

# IX. ACKNOWLEDGMENTS

Lan Zhang and Xiang-Yang Li are the contact authors. The research is supported by National Key R&D Program of China 2017YFB1003003, National Natural Science Foundation of China with No. 61822209, No.61625205No. 61932016, No. 61751211, No. 61520106007, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002, the Fundamental Research Funds for the Central Universities.

# REFERENCES

[1] A. Kittur, E. H. Chi, and B. Suh, “Crowdsourcing user studies with mechanical turk,” in Proceedings of the SIGCHI conference on human factors in computing systems, 2008, pp. 453–456.   
[2] M. Marge, S. Banerjee, and A. I. Rudnicky, “Using the amazon mechanical turk for transcription of spoken language,” in 2010 IEEE International Conference on Acoustics, Speech and Signal Processing. IEEE, 2010, pp. 5270–5273.   
[3] X. Liu, M. Lu, B. C. Ooi, Y. Shen, S. Wu, and M. Zhang, “Cdas: a crowdsourcing data analytics system,” arXiv preprint arXiv:1207.0143, 2012.   
[4] M. J. Franklin, D. Kossmann, T. Kraska, S. Ramesh, and R. Xin, “Crowddb: answering queries with crowdsourcing,” in Proceedings of the 2011 ACM SIGMOD International Conference on Management of data, 2011, pp. 61–72.   
[5] G. Paolacci, J. Chandler, and P. G. Ipeirotis, “Running experiments on amazon mechanical turk,” Judgment and Decision making, vol. 5, no. 5, pp. 411–419, 2010.   
[6] T. Finin, W. Murnane, A. Karandikar, N. Keller, J. Martineau, and M. Dredze, “Annotating named entities in twitter data with crowdsourcing,” in Proceedings of the NAACL HLT 2010 Workshop on Creating Speech and Language Data with Amazons Mechanical Turk, 2010, pp. 80–88.   
[7] G. Demartini, D. E. Difallah, and P. Cudre-Mauroux, “Zencrowd: ´ leveraging probabilistic reasoning and crowdsourcing techniques for large-scale entity linking,” in Proceedings of the 21st international conference on World Wide Web, 2012, pp. 469–478.   
[8] Y. Zheng, R. Cheng, S. Maniu, and L. Mo, “On optimality of jury selection in crowdsourcing.” in EDBT, 2015, pp. 193–204.   
[9] Y. Zheng, J. Wang, G. Li, R. Cheng, and J. Feng, “Qasca: A qualityaware task assignment system for crowdsourcing applications,” in Proceedings of the 2015 ACM SIGMOD international conference on management of data, 2015, pp. 1031–1046.   
[10] F. Ma, Y. Li, Q. Li, M. Qiu, J. Gao, S. Zhi, L. Su, B. Zhao, H. Ji, and J. Han, “Faitcrowd: Fine grained truth discovery for crowdsourced data aggregation,” in Proceedings of the 21th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2015, pp. 745– 754.   
[11] Y. Zheng, G. Li, and R. Cheng, “Docs: a domain-aware crowdsourcing system using knowledge bases,” Proceedings of the VLDB Endowment, vol. 10, no. 4, pp. 361–372, 2016.   
[12] Y. Du, Y.-E. Sun, H. Huang, L. Huang, H. Xu, Y. Bao, and H. Guo, “Bayesian co-clustering truth discovery for mobile crowd sensing systems,” IEEE Transactions on Industrial Informatics, vol. 16, no. 2, pp. 1045–1057, 2019.   
[13] A. P. Dawid and A. M. Skene, “Maximum likelihood estimation of observer error-rates using the em algorithm,” Journal of the Royal Statistical Society: Series C (Applied Statistics), vol. 28, no. 1, pp. 20– 28, 1979.   
[14] V. S. Sheng, F. Provost, and P. G. Ipeirotis, “Get another label? improving data quality and data mining using multiple, noisy labelers,” in Proceedings of the 14th ACM SIGKDD international conference on Knowledge discovery and data mining, 2008, pp. 614–622.   
[15] B. Zhao and J. Han, “A probabilistic model for estimating real-valued truth from conflicting sources,” Proc. of QDB, 2012.   
[16] X. Yin, J. Han, and S. Y. Philip, “Truth discovery with multiple conflicting information providers on the web,” IEEE Transactions on Knowledge and Data Engineering, vol. 20, no. 6, pp. 796–808, 2008.   
[17] H. Jin, L. Su, and K. Nahrstedt, “Theseus: Incentivizing truth discovery in mobile crowd sensing systems,” in Proceedings of the 18th ACM International Symposium on Mobile Ad Hoc Networking and Computing, 2017, pp. 1–10.   
[18] X. Lin and L. Chen, “Domain-aware multi-truth discovery from conflicting sources,” Proceedings of the VLDB Endowment, vol. 11, no. 5, pp. 635–647, 2018.   
[19] J. Wang, T. Kraska, M. J. Franklin, and J. Feng, “Crowder: Crowdsourcing entity resolution,” arXiv preprint arXiv:1208.1927, 2012.   
[20] Y. Du, Y.-E. Sun, H. Huang, L. Huang, H. Xu, and X. Wu, “Qualityaware online task assignment mechanisms using latent topic model,” Theoretical Computer Science, vol. 803, pp. 130–143, 2020.   
[21] Y. Du, H. Xu, Y.-E. Sun, and L. Huang, “A general fine-grained truth discovery approach for crowdsourced data aggregation,” in International

Conference on Database Systems for Advanced Applications. Springer, 2017, pp. 3–18.   
[22] D. Oleson, A. Sorokin, G. Laughlin, V. Hester, J. Le, and L. Biewald, “Programmatic gold: Targeted and scalable quality assurance in crowdsourcing,” in Workshops at the Twenty-Fifth AAAI Conference on Artificial Intelligence, 2011.   
[23] D. M. Blei, A. Y. Ng, and M. I. Jordan, “Latent dirichlet allocation,” Journal of machine Learning research, vol. 3, no. Jan, pp. 993–1022, 2003.   
[24] T. Minka, “Estimating a dirichlet distribution,” 2000.   
[25] C. Andrieu, N. De Freitas, A. Doucet, and M. I. Jordan, “An introduction to mcmc for machine learning,” Machine learning, vol. 50, no. 1-2, pp. 5–43, 2003.   
[26] C. Keribin, V. Brault, G. Celeux, and G. Govaert, “Estimation and selection for the latent block model on categorical data,” Statistics and Computing, vol. 25, no. 6, pp. 1201–1216, 2015.   
[27] C. Biernacki, G. Celeux, and G. Govaert, “Assessing a mixture model for clustering with the integrated completed likelihood,” IEEE transactions on pattern analysis and machine intelligence, vol. 22, no. 7, pp. 719– 725, 2000.   
[28] G. Schwarz et al., “Estimating the dimension of a model,” The annals of statistics, vol. 6, no. 2, pp. 461–464, 1978.   
[29] R. Snow, B. Oconnor, D. Jurafsky, and A. Y. Ng, “Cheap and fast–but is it good? evaluating non-expert annotations for natural language tasks,” in Proceedings of the 2008 conference on empirical methods in natural language processing, 2008, pp. 254–263.   
[30] X. Liang, T. Zou, B. Guo, S. Li, H. Zhang, S. Zhang, H. Huang, and S. X. Chen, “Assessing beijing’s pm2. 5 pollution: severity, weather impact, apec and winter heating,” Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences, vol. 471, no. 2182, p. 20150257, 2015.   
[31] M. Wan, X. Chen, L. Kaplan, J. Han, J. Gao, and B. Zhao, “From truth discovery to trustworthy opinion discovery: An uncertainty-aware quantitative modeling approach,” in Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2016, pp. 1885–1894.   
[32] A. R. Khan and H. Garcia-Molina, “Crowddqs: Dynamic question selection in crowdsourcing systems,” in Proceedings of the 2017 ACM International Conference on Management of Data, 2017, pp. 1447–1462.   
[33] N. R. Devanur and T. P. Hayes, “The adwords problem: online keyword matching with budgeted bidders under random permutations,” in Proceedings of the 10th ACM conference on Electronic commerce, 2009, pp. 71–78.   
[34] Q. Li, Y. Li, J. Gao, L. Su, B. Zhao, M. Demirbas, W. Fan, and J. Han, “A confidence-aware approach for truth discovery on long-tail data,” Proceedings of the VLDB Endowment, vol. 8, no. 4, pp. 425–436, 2014.   
[35] X. L. Dong, L. Berti-Equille, and D. Srivastava, “Integrating conflicting data: the role of source dependence,” Proceedings of the VLDB Endowment, vol. 2, no. 1, pp. 550–561, 2009.   
[36] A. Augustin, M. Venanzi, J. Hare, A. Rogers, and N. Jennings, “Bayesian aggregation of categorical distributions with applications in crowdsourcing.” AAAI Press/International Joint Conferences on Artificial Intelligence, 2017.   
[37] E. Simpson, S. Roberts, I. Psorakis, and A. Smith, “Dynamic bayesian combination of multiple imperfect classifiers,” in Decision making and imperfection. Springer, 2013, pp. 1–35.