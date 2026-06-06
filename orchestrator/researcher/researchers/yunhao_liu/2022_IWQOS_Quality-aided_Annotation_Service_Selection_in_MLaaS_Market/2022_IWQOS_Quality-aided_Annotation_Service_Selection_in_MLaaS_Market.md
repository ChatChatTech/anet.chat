# Quality-aided Annotation Service Selection in MLaaS Market

Shanyang Jiang

School of Data Science

University of Science and Technology of China

Hefei, China

yang12@mail.ustc.edu.cn

Lan Zhang

School of Computer Science and Technology

School of Data Science

University of Science and Technology of China

Hefei, China

zhanglan@ustc.edu.cn

Abstract—The vibrant markets offering data annotation services are fast-growing and play an important part in machine learning. While many multi-label prediction services are available, it is challenging for consumers to decide which services to use for their own tasks and budgets due to the heterogeneity in those services’ labeling categories, labeling quality and price. In this paper, we focus on a practical problem of obtaining high-quality multi-label annotation data from multiple services within a budget constraint. We propose a framework that firstly parameterizes the labeling generation based on the constructed Probabilistic Graph Model, and designs an Expectation Maximization(EM)-based iteration algorithm to estimate the service labeling quality and task truth distribution. Then we transform the annotation service selection strategy into an adaptive submodular maximization coverage problem, which motivates us to design an adaptive random greedy algorithm with a constant approximation ratio 1 − 1/e. We evaluate our design on both real-world experiments and a series of simulations on various machine learning models and real datasets. These experiments will show that our method has more accuracy and reliability improvements.

Index Terms—service quality, data quality, service selection

# I. INTRODUCTION

The huge demand to provide Machine Learning as a Service (MLaaS) has spawned a market for commercial ML API services. For example, one could use Google prediction API annotation services to classify an image or to classify the sentiment of a text passage [1]. MLaaS market are appealing because using such services reduces the need to develop ones own ML models. An online marketplace for labelled data is emerging, where many companies offer automatic data labeling services and charge the service fee, e.g., Google Cloud [1]–[3], Miscrosoft Azure [4], [5], BaiduAI [6], Tencent Cloud [7]. In practice, these services also provide different performance on different datasets. As more and more such services are available, the heterogeneity of different services makes it challenging for consumers to select the optimal combination of services to achieve high quality labeling for their own data within a given budget.

In this work, aimming to obtain high quality labeling data, we proposes a service selection stategy, facing the challenges raised by three dimensions of service heterogeneity: labeling categories, labeling quality and prices, within a monetary budget constraint. First, different services offer different learning functions, hence output diverse categories of labels. In many cases, using only one API service is insufficient to obtain all target labels, so it is necessary to select multiple services and fuse their results. Second, even services for the same task often perform differently in terms of accuracy. Intuitively, if a service can provide more accurate annotation results for the target dataset, it should have more chance to be selected. However, the performance of each service on the target dataset is usually unknown in advance, which significantly increases the difficulty for service selection. Third, prices vary across services from different companies for similar labeling tasks.

There are some recent work addressing optimal combinations of annotation services [8], [9]. FrugalML [8] proposes an algorithmic framework for services calling strategies aiming at only simple classification tasks where the output is a single label. FrugalML learns a decision rule for each possible label which requires a large amount of training data and solves a non-convex optimization problem with computational complexity exponential in the number of distinct labels. Such a high complexity hinders it to apply to tasks with a large number of labels, such as multi-label classification. FrugalMCT [9] proposes a framework that adaptively selects services for different data in an online fashion while respecting user’s budget. FrugalMCT cast the service selection problem as an integer linear program, and develop a provably efficient online solver. Though FrugalMCT takes the multi-label case into consideration, it ignores the important role of the distinguished annotation categories for service selection strategy, and doesn’t evaluate the different service labeling quality. Furthermore, it calculates received utility for each service by trainning an accuracy predictor on task’s true label set and prediction from each service, while the true label sets are actually unknown for consumers.

To deal with above challenges and obtain high-quality annotation dataset within a budget, we formalize and solve a problem, bugdet-constraint adaptive random greedy service selection for multi-label annotation. We propose a framework, which first evaluates the data quality of collected annotation and then automatically identifies the optimal sequential service selection strategy within a budget constraint. For annotation data quality, we construct a probabilistic graph model whose parameters consist of service labeling quality and task truth distribution, which are used to express the service annotation answers’ generation process, and we design an Expectation Maximization(EM)-based iteration algorithm to learn those probabilistic graph model parameters using some collected annotation data. After that, based on the estimated task truth distribution, we can apply the maximum likelihood estimation(MLE) method to calculate the classification confidence for each task, and update the service labeling quality distribution. Regarding the service quality distribution as the prior distribution, we can use the maximum a posterior probability(MAP) method to calculate the annotation data quality.

With the probabilistic graph model, we are able to determine the annotation data quality and task truth distribution. We integrate the data quality estimation result as a guide information for service selection problem, and model it as a stochastic monotone submodular maximization coverage problem. As the service annotation feedback is not determined in advance, we cannot directly adopt the classical greedy algorithm for our submodular maximization problem. We calculate the generation probability for all the service annotation feedback to simulate an adaptive expectation, and taking advantage of adaptive submodularity, we design an adaptive random greedy algotithm, which achieving a constant approximation ratio of 1 − 1/e.

The contribution of this work can be summarized as follows:

• We propose a framework to obtain the high-quality annotation by estimating the service labeling quality and adaptive service selection given a multi-label set within the budget constraints.   
• We construct a probabilistic graph model to parameterize the annotation generation process. We design an Expectation Maximization-based iteration algorithm to estimate the service labeling quality and task truth distribution.   
• We use the annotation data quality estimation result to guide service selection. We model it as a stochastic monotone submodular maximization coverage problem, and propose a random adaptive greedy algorithm with achieving a constant approximation ratio of 1 − 1/e.   
• We evaluate our design on both real-world experiments and a series of simulations on various machine learning and deep learning models and real datasets, including image classification and text classification. Under the same budget constraints, consumers can obtain higherquality annotations through our service selection strategy and truth aggregation method.

# II. RELATED WORK

# A. Human Crowdsourcing Annotation

Crowdsourcing has become a general method to obtain annotations from the Internet. Typically human crowdsourcing annotation system often contains truth inference and task assignment these two parts. Zheng et al. [10] made a complete and detailed summary about the task types, worker models, and various truth inference methods in the crowdsourcing system. Zhang et al. [11] proposed a latent clustering method to solve the truth inference problem in multi-label annotation scenarios in crowdsourcing systems. These methods above are all necessary to collect the annotation answers of entire tasks, which thus cannot be applied to our scene-setting. Some other recent work propose various algorithm frameworks about budget aware task assignment and worker incentive mechanism for the binary task [12]–[14], multi-class task [15], multi-label task [16], and real-value task [17] based on human crowdsourcing annotation system. These works do not take into account the role of worker reliability in task assignment algorithm. Besides, they fail to realize the dynamic update of the label truth value after obtaining the worker’s labeling result. In Sun et al. [16], a crowdsourcing annotation system for multi-label tasks is considered. However, due to the characteristics of human annotation, the problem of full set coverage of the annotation categories is not considered.

# B. API Service Annotation

In recent years, data markets have been an active research topic in various communities. Recently Fernandez [18] presented their vision for the design of platforms to support data markets. Zhang et al. [19] implement a crowdsourcing based dataset purchasing framework, named CrowdBuy and CrowdBuy++, to make a buyer can efficiently buy desired data with quality guarantee respecting users’ data ownership and privacy. Meanwhile, several other works [20], [21] adopt a game-theoretic approach of market design for such markets, exploring issues such as fairness and pricing. With the growing importance of MLaaS API service and markets [22], existing related research has largely focused on individual API for performance [23], pricing [24], robustness [25], and applications [26]–[28].

We also have experienced the increasing prevalence of API data annotation services, which aim to produce data annotation results by calling these trained ML and DL models in the form of API services. Yuan et al. [29]–[32] proposed a series of model scheduling algorithm from the model owner’s perspective for collaborative multi-model inference, which selects the model with the most significant profit according to the intermediate results of the previous model output while taking into account the limitations of the hardware resources and execution time of the model. FrugalML [8] proposes an algorithmic framework from the market consumer’s perspective for API service calling strategies aiming at simple classification tasks where the output is a single label. Their algorithms learn a decision rule based on a large amount of training data for each possible label and involves solving a non-convex optimization problem. However, its computational complexity is exponential in the number of distinct labels. Such a high complexity prevents it from being used for tasks with large number of labels, such as multi-label classification. Furthermore, FrugalML ignores correlation between different APIs’ predictions, potentially leading to limited accuracy. FrugalMCT [9] proposes a principled framework that learns the strengths and weaknesses of different combinations of available APIs, and efficiently selects the optimal combinations of APIs to call for different data items and budget constraints.

# III. PROBLEM OVERVIEW

# A. Problem Overview

There are two entities involved in data annotation API service market: a service consumer and a set $S ( | S | = S )$ of available data annotation API services. We assume the consumer is in a push marketplace, which means that the consumer can gather annotation answers from any service, and receive those answers with guarantees. We denote the target task set as ${ \mathcal { T } } = \{ < x ^ { t } , \mathbf { y } ^ { t } > \} _ { t = 1 } ^ { T } ( | T | = T )$ , where $x ^ { t }$ denotes the feature of each task and $\mathbf { y } ^ { t }$ represents the label set which determined by the consumer(e.g., possible class labels for classification or detection tasks). These API services then can provide annotation answers and its corresponding confidence based on their annotation categories for part labels.

Due to the diverse service and different task, these annotation datasets generated by services are normally inaccurate and unreliable. Considering the uncertainty of these annotation results, the consumer faces two fundamental challenges: how to evaluate the data quality of collected annotation datasets and how to select the reliable service to maximize the annotation data quality? In generation, the consumer can leverage some historical annotation datasets to estimate each service’s data quality and also to calculate the annotation datasets’ quality, which are two critical indicators to tackle the above two challenges. For the service quality estimation, the consumer uses the historical annotation data of a service to calculate her own data quality distribution, indicating the data quality level of this service in future data acquisition. Such that annotation datasets’s quality can be seen as been defined by the quality level of service. We adopt the quality of annotation datasets as selection criteria in service selection problem, aiming to obtain a high-quality annotation datasets.

# B. Data Quality

We assume that the consumer first posts an unlabeled target task set T to obtain repeated noisy annotation answers from these API services. Each task $x ^ { t }$ has the same and given target K labels $\mathbf { y } ^ { t } = [ y _ { 1 } ^ { t } , y _ { 2 } ^ { t } , . . . , y _ { K } ^ { t } ] , y _ { k } ^ { t } \in \{ 0 , 1 \}$ , which need to be labeled by API services. We denote all label truth values of the entire unlabeled task set by $\mathbf { Y } = [ \mathbf { y } ^ { 1 } , \mathbf { y } ^ { 2 } , . . . , \mathbf { y } ^ { T } ]$ , then we can say that $y _ { k } ^ { t }$ is the final aggregated annotation result for the label k of the task $x ^ { t }$ . All API services can be freely selected by the consumer and be called with a given post price. We also assume that there are a availiable service set $s , | s | = S$ , that can annotate the target task, and each service’s each call need to be paid $b _ { s }$ . The services’ output exactly its estimated confidence for the presence of each label. The annotation answer for the kth label of task $x ^ { t }$ from the service s is denoted by $a _ { k , ( s ) } ^ { t } ~ \in ~ ( 0 , 1 )$ , and the all collected noisy annotation answers for target tasks t form a matrix $\mathbf { A } ^ { t } = [ a _ { k , ( s ) } ^ { t } ] _ { S * K }$ . Considering the labeling categories of each service, if service s may can not provlet its label answer $a _ { k , ( s ) } ^ { t } = - 1$ l answer for th. We next use $\mathbf { A } _ { ( s ) } ^ { t }$ label,to de $x ^ { t }$ $\mathbf { A } _ { k } ^ { t }$ to denote all annotation answers for the kth label of task $x ^ { t }$ . All collected answers of the entire target task set are denoted by $\mathbf { A } ^ { T } = [ \mathbf { A } ^ { 1 } , \mathbf { A } ^ { 2 } , . . . , \mathbf { A } ^ { T } ]$ ].

In actual, we face the binary classification problem, and the data quality can be represented by the level of label confidence, each of which corresponds to a Bernoulli distribution. The Bernoulli distribution has been widely used to describe annotation results in Crowdsourcing application. Given a annotation task, the annotation results from a service with data quality level q is regarded as a random variable generated from the Bernoulli distribution $B ( Y , q )$ , where the variable Y is the ground truth of the task. Annotation service may involve in various algorithm and different data during model train process, which generate annotation data in diverse data quality levels. Here, we denote the annotation quality of service s by $\mathbf q _ { s } ~ = ~ [ q _ { s , 1 } , . . . , q _ { s , K } ]$ on K different labels respectively. Similar to the classic definition of Accuracy, each labeling quality value range is $q _ { s , k } \in [ 0 , 1 ]$ , represents the probability that the annotation answer $a _ { k , ( s ) } ^ { t }$ is equal to the label truth: $q _ { s , k } = p ( a _ { k , ( s ) } ^ { t } = y _ { k } ^ { t } | y _ { k } ^ { t } ) $ , and the larger $\boldsymbol { q } _ { s , k }$ is, the more reliable on kth label the service s is. Same as the representation of annotation answers, considering the labeling categories of each service, if service s can not provide any label answer for the kth label, we just let $q _ { s , k } = 0$ , and will not update its value in the service labeling quality estimation algorithm. We use the vector $\mathbf q = [ \mathbf q _ { 1 } , . . . , \mathbf q _ { S } ]$ to denote the annotation quality of all services.

# C. Service Selection

We model the service selection problem in the scenario of unknown service annotation feedback as a stochastic monotone submodular maximization coverage problem. The ground set is obviously all the services S. Annotation services may have different possible data quality levels, label categories and price. For each service, we can realize a random feedback set for any task: $\mathbf { A } _ { s } ^ { t } ,$ , and denote the realizations of all the services as $\mathbf { A } = [ \mathbf { A } _ { 1 } ^ { t } , . . . , \mathbf { A } _ { S } ^ { t } ]$ . Before selecting annotation services, the consumers only knows the quality distribution of services, and just can calculate the annotation data probability distribution over a possible realization $\mathbf { A } _ { s } ^ { t }$ . Once the service consumer selects a service, she can obtain its real annotation feedback.

We define the objective utility function of the consumer as: $F : 2 ^ { S } \times \mathbf { K } ^ { S }  \mathbb { R }$ , which maps a real value to every subset of services and the corresponding annotation dataset realization. The final goal of the consumer is to select a service subset $\tilde { s } \subset \tilde { s }$ to maximize the expected objective utility function, subjecting to the budget constraint B. We formulate the service selection problem in the scenario of unknown service annotation feedback as

$$
\mathcal {S} ^ {*} = \arg \max \mathbb {E} [ F (\widetilde {\mathcal {S}}, A) ], \tag {1}
$$

where $\mathbb { E } [ F ( \widetilde { S } , A ) ]$ is the expected utility with respected to the probability distribution $\operatorname* { P r } ( A )$ of all possible annotation realization:

$$
\mathbb {E} [ F (\widetilde {\mathcal {S}}, A) ] = \sum_ {A} \operatorname * {P r} (A) \times F (\widetilde {\mathcal {S}}, A). \tag {2}
$$

To achieve good performance guarantees, we need the utility function to satisfy two important property: adaptive monotone and adaptive submodularity. Adaptive monotone and submodularity [33], [34] is a premium version of monotone and submodularity in the scenarios of unknown feedback realization. We then give the formal definition of submodularity as follows.

Definition 1 (Submodularity). Given the ground set ${ \mathcal { S } } ,$ a set function $F : 2 ^ { S }  \mathbb { R }$ is called submodular, if for any $A \subset$ $B \subset S$ and $s \in { \mathcal { S } } \backslash B ,$ , it satisfies that: $F ( A \cup \{ s \} ) - F ( A ) \geq$ $F ( B \cup \{ s \} ) - F ( B )$ .

Although submodular maximization optimization problem are NP-hard, we can get a near-optimal result with constant approximation ratio of $1 - 1 / e$ by adopting a classical greedy algorithm. However, the greedy algorithm cannot guarantee performance when the feedback realization is not determined before the algorithm runs. So adaptive property [33], [34] can be used to deal with it, as long as we can quantify the feedback realization distribution. We first present the definition of conditional expected marginal utility, when current selected service set faces a new service, and use it to define the adaptive submodular and monotonicity properties of the utility function, respectively.

Definition 2 (Conditional Expected Marginal Utility). Given a service s, its feedback $A _ { s } ^ { t }$ and current annotation dataset $A ,$ the conditional expected marginal utility of s conditioned on A is:

$$
\Delta_ {F} (s | A) = \mathbb {E} [ F (\widetilde {\mathcal {S}} \cup \{s \}, A \cup A _ {s} ^ {t}) - F (\widetilde {\mathcal {S}}, A) | A \sim \mathcal {S} ], \tag {3}
$$

where A is the annotation dataset corresponding to service set S .

Definition 3 (Adaptive Submodular). Given the ground set $s ,$ , a set function $F : \bar { 2 } ^ { S } \times K ^ { S } \to \mathbb { R }$ is called adaptive submodular with respect to all the possible feedback realization distribution $\mathrm { P r } ( A _ { s } ^ { t } )$ , if for any current set $\widetilde { s }$ and ${ \hat { S } } ,$ where ${ \tilde { s } } \subset { \hat { s } } ,$ , and for any $s \in { \mathcal { S } } \setminus { \hat { \mathcal { S } } } ,$ , it satisfies that: $\Delta _ { F } ( s | A _ { \widetilde { s } } ^ { t } ) \geq \Delta _ { F } ( s | A _ { \hat { s } } ^ { t } )$ .

Definition 4 (Adaptive Monotonicity). Given the ground set ${ \mathcal { S } } ,$ a set function $F : 2 ^ { S } \times \mathbf { K } ^ { S }  \mathbb { R }$ is called adaptive monotone with respect to all the possible feedback realization distribution $\mathrm { P r } ( A _ { s } ^ { t } )$ , if for any current set $\widetilde { s }$ and service $s \in { \mathcal { S } } \setminus { \widetilde { \mathcal { S } } } ,$ , it satisfies that: $\Delta _ { F } ( s | A _ { \widetilde { S } } ^ { t } ) \geq 0$ .

# IV. SERVICE QUALITY ESTIMATION

# A. Service Annotation Probabilistic Model

We first construct a general Probabilistic Graph Model to describe the unknown task truth distribution and service labeling quality level. As describe above, we have defined the service labeling quality: q as the validation accuracy. For the label truth distribution, the annotation answer of each service is the probability that this label is presence for current task, we also call it as confidence. So the label truth distribution can be define as $\theta _ { k } ^ { t } = p ( y _ { k } ^ { t } = 1 ) , \theta _ { k } ^ { t } \in [ 0 , 1 ]$ , and then we denote all $K$ labels’ truth as a vector $\mathbf { \ddot { \theta } } ^ { t } = [ \theta _ { 1 } ^ { t } , \theta _ { 2 } ^ { t } , . . . , \theta _ { K } ^ { t } ]$ . We denote all $\gamma _ { s }$ label truth distribution vector by parameter set: $\pmb { \theta } = \{ \pmb { \theta } ^ { 1 } , \pmb { \theta } ^ { 2 } , . . . , \pmb { \theta } ^ { T } \}$ . Actually, $\theta _ { k } ^ { t }$ can also be regarded as the Difficulty degree of the target label [12], [35]: if $\theta _ { k } ^ { t } \approx 1 / 2$ , now we have $p ( y _ { k } ^ { t } = 1 ) \approx p ( y _ { k } ^ { t } = 0 )$ , it means the absence or presence of the kth label is too difficult to infer. In addition, the general Major Voting algorithm regards $\theta _ { k } ^ { t }$ as the percentage of services that label the kth label as the presence if a large number of perfect and honesty services are asked for the task. If we know $\theta _ { k } ^ { t } \approx 0$ or $\theta _ { k } ^ { t } \approx 1$ , we can infer the presence or absence of the target label of the current task surely.

According to Probabilistic Graph Model proposed in Fig. $1 , y _ { k } ^ { t }$ can be independently drawn from Bernoulli Distribution with parameter $\theta _ { k } ^ { \bar { t } } \colon B ( y _ { k } ^ { t } = 1 , \theta _ { k } ^ { t } )$ , that is, for the kth label of task $x ^ { t }$ , we have:

$$
p (y _ {t} ^ {t} | \theta_ {k} ^ {t}) = (\theta_ {k} ^ {t}) ^ {\mathbb {I} (y _ {k} ^ {t} = 1)} (1 - \theta_ {k} ^ {t}) ^ {\mathbb {I} (y _ {k} ^ {t} = 0)}, \tag {4}
$$

where  is indicatof service labeling qon annotation answer ction.level, obey $\hat { a } _ { k , ( s ) } ^ { t } \in \{ 0 , 1 \}$ the definition conditioningtribution with $a _ { k , ( s ) } ^ { t }$ parameter $q _ { s , k } \mathrm { : }$ :

$$
\begin{array}{l} p \left(\hat {a} _ {k, (s)} ^ {t} = 1 \mid a _ {k} ^ {t}, q _ {s, k}\right) = a _ {k} ^ {t} \cdot q _ {s, k} + \left(1 - a _ {k} ^ {t}\right) \cdot \left(1 - q _ {s, k}\right), \\ p \left(\hat {a} _ {k, (s)} ^ {t} = 0 \mid a _ {k} ^ {t}, q _ {s, k}\right) = a _ {k} ^ {t} \cdot \left(1 - q _ {s, k}\right) + \left(1 - a _ {k} ^ {t}\right) \cdot q _ {s, k}. \tag {5} \\ \end{array}
$$

![](images/5f9c3f9d4f98897719ff8f96412b19c3424d84fcf71be3da7c6f04ea6161177a.jpg)



Fig. 1: Annotation Generation Process.

# B. Service Quality Estimation Algorithm

We then propose a Expectation Maximization(EM)-based iterative algorithm to estimate the service annotation quality level and task truth distribution jointly. The probabilistic graphical model contains two parameter sets: service annotation quality parameter q and task truth distribution parameter $\theta ,$ which can be denoted as $\boldsymbol { \Psi } = ( \mathbf { q } , \pmb { \theta } )$ . As different tasks and services also have their own parameters, we will use an EM algorithm to learn and update these parameters iteratively.

Complete Data Likelihood. Considering each task is individually annotated by each service, the likelihood of all collected noisy annotation answers $\mathbf { A } ^ { t }$ on the current task $x ^ { t }$ can be calculated as follows:

$$
\begin{array}{l} L _ {x ^ {t}} (\mathbf {q}, \boldsymbol {\theta} ^ {t}) = p (\hat {\mathbf {A}} ^ {t} | \mathbf {A} ^ {t}, \mathbf {y} ^ {t}, \mathbf {q}) \\ = \sum_ {\mathbf {y} ^ {t}} p (\mathbf {y} ^ {t} | \boldsymbol {\theta} ^ {t}) \cdot p (\hat {\mathbf {A}} ^ {t} | \mathbf {A} ^ {t}, \mathbf {q}) \\ = \sum_ {\mathbf {y} ^ {t}} \prod_ {k = 1} ^ {K} p (y _ {k} ^ {t} | \theta_ {k} ^ {t}) \cdot \prod_ {s \in \mathcal {S} ^ {t}} p (\hat {a} _ {k, (s)} ^ {t} | a _ {k, (s)} ^ {t}, q _ {s, k}), \\ \end{array}
$$

where $S ^ { t }$ is the service set who has provided its annotation answer for current target task $x ^ { t } .$ . Therefore, the complete data likelihood of all collected noisy label answer set A of the entire target task set $\tau$ is:

$$
L _ {\mathcal {T}} (\mathbf {q}, \boldsymbol {\theta}) = \prod_ {x ^ {t} \in \mathcal {T}} L _ {x ^ {t}} (\mathbf {q}, \boldsymbol {\theta} ^ {t}). \tag {6}
$$

Through the Expectation Maximization algorithm, we need to maximize the log-likelihood of the collected annotation answers from services: ln $L _ { \mathcal { T } } ( \mathbf { q } , \pmb \theta )$ , to iteratively update parameter set Ψ.

E-step. With respect to the conditional distribution of Y given the observed noisy label answer A under the current estimates of parameters $\Psi ^ { o l d }$ , we calculate the expected value of the complete log-likelihood function, as follow:

$$
\begin{array}{l} \mathbf {Q} (\boldsymbol {\Psi}, \boldsymbol {\Psi} ^ {o l d}) = \mathbb {E} _ {\mathbf {Y} | \mathbf {A}, \boldsymbol {\Psi} ^ {o l d}} \left[ \ln p (\mathbf {A}, \mathbf {Y} | \boldsymbol {\Psi}) \right] \\ = \sum_ {x ^ {t} \in \mathcal {T}} \mathbb {E} _ {\mathbf {Y} ^ {t}} \left[ \ln p (\mathbf {A} ^ {t}, \mathbf {y} ^ {t} | \mathbf {q}, \boldsymbol {\theta} ^ {t}) \right] \\ = \sum_ {x ^ {t} \in \mathcal {T}} \mathbb {E} _ {\mathbf {Y}} \left[ \ln \left(p (\hat {\mathbf {A}} ^ {t} | \mathbf {A} ^ {t}, \mathbf {y} ^ {t}, \mathbf {q}) \cdot p (\mathbf {y} ^ {t} | \boldsymbol {\theta} ^ {t})\right) \right]. \\ \end{array}
$$

Here, $p ( \mathbf { y } ^ { t } | \pmb { \theta } ^ { t } )$ can be initialized by Uniform Distribution in the first round, and directly use a constant value from the current estimation Ψ in the next round. Thus, we just only need to maximize:

$$
\mathbf {Q} (\boldsymbol {\Psi}, \boldsymbol {\Psi} ^ {o l d}) \propto \sum_ {x ^ {t} \in \mathcal {T}} \mathbb {E} _ {\mathbf {Y}} \left[ \ln p \left(\hat {\mathbf {A}} ^ {t} \mid \mathbf {A} ^ {t}, \mathbf {y} ^ {t}, \mathbf {q}\right) \right]. \tag {7}
$$

Next, we could calculate the posterior probability of the available label truth list $\mathbf { y } ^ { t }$ by Bayesian Theorem as follows:

$$
\begin{array}{l} p (\mathbf {y} ^ {t} | \mathbf {A} ^ {t}, \boldsymbol {\Psi}) = \frac {p (\mathbf {A} ^ {t} | \mathbf {y} ^ {t} , \boldsymbol {\Psi}) p (\mathbf {y} ^ {t} | \boldsymbol {\Psi})}{p (\mathbf {A} ^ {t} | \boldsymbol {\Psi})} \\ = \frac {p (\mathbf {A} ^ {t} | \mathbf {y} ^ {t} , \boldsymbol {\Psi}) p (\mathbf {y} ^ {t} | \boldsymbol {\Psi})}{\sum_ {\mathbf {y}} p (\mathbf {A} ^ {t} | \mathbf {y} , \boldsymbol {\Psi}) p (\mathbf {y} | \boldsymbol {\Psi})}, \tag {8} \\ \end{array}
$$

where y is all the available label truth list. And $p ( \mathbf { y } ^ { t } | \mathbf { A } ^ { t } , \varPsi )$ is proportional to the numerator of the posterior probability:

$$
\begin{array}{l} p (\mathbf {y} ^ {t} | \mathbf {A} ^ {t}, \boldsymbol {\Psi}) \propto p (\mathbf {A} ^ {t} | \mathbf {y} ^ {t}, \boldsymbol {\Psi}) p (\mathbf {y} ^ {t} | \boldsymbol {\Psi}) \\ = \prod_ {k = 1} ^ {K} p (y _ {k} ^ {t} | \theta_ {k} ^ {t}) \prod_ {s \in \mathcal {S} ^ {t}} p (\hat {a} _ {k, (s)} ^ {t} | a _ {k, (s)} ^ {t}, q _ {s, k}). \tag {9} \\ \end{array}
$$

Based on Eq. (9), we can get the expectation of the posterior probability of each single label $y _ { k } ^ { t } = 1$ , that will be used in M-step as follows:

$$
\mathbb {E} \left[ \mathbb {I} (y _ {k} ^ {t} = 1) \right] = \sum_ {\mathbf {y}, y _ {k} ^ {t} = 1} p (y _ {k} ^ {t} = 1,... y _ {k ^ {\prime}} ^ {t}... | \mathbf {A}, \boldsymbol {\Psi}). \tag {10}
$$

M-step. We could maximize the expected value function Q formed as Eq.(7) by Ψnew = arg maxΨ $\mathbf { Q } ( \Psi , \Psi ^ { \mathbf { o l d } } )$ , to update the parameter set Ψ iteratively. Using Lagrange multiplier, calculate the partial derivatives of the two variables separately, and make the partial derivatives equal to 0, which can be solved to get:

$$
\theta_ {k} ^ {t} = \mathbb {E} \left[ \mathbb {I} (y _ {k} ^ {t} = 1) \right], \tag {11}
$$

$$
q _ {s, k} = \frac {\sum_ {x ^ {t} \in \mathcal {T}} \mathbb {I} (a _ {k , (s)} ^ {t} = y) \mathbb {E} \left[ \mathbb {I} (y _ {k} ^ {t} = y) \right]}{\sum_ {x ^ {t} \in \mathcal {T}} \mathbb {I} (a _ {k , (s)} ^ {t} \neq - 1)}. \tag {12}
$$

After the Expectation Maximization-based parameter update algorithm converges, the final aggregated label truth of task $x ^ { t }$ is the label value combination with the biggest posterior probability, as follows:

$$
y _ {1} ^ {t}, \dots , y _ {K} ^ {t} = \arg \max p \left(y _ {1} ^ {t}, \dots , y _ {K} ^ {t} \mid \mathbf {A} ^ {t}, \boldsymbol {\theta}, \mathbf {q}\right) \tag {13}
$$

The service labeling quality estimation algorithm is conducted in two phases according to Algorithm 1. We also provide algorithms for dynamically updating service annotation quality and task truth distribution, which we briefly introduce in appendix due to space limitations.

Algorithm 1: Service Annotation Quality Estimation.   
Input: Target task set T, Label number K, Service set S, Collected annotation answer set A.
Output: Estimated service labeling quality q; Task label truth Y.

1 Initialize label truth distribution $\theta^{t}$ for $x^{t} \in T$ , and service labeling quality parameter $q_{s}$ for $s \in S$ ;

2 // parameter learning

3 while not converge do

4    // E step

5    for each task $x^{t} \in T$ do

6    Calculation expectation by Equation (10);

7    // M step

8    Update task label truth parameter by Equation (11);

9    Update service labeling quality parameter by Equation (12);

10 // convergence

11 for each task $x^{t} \in T$ do

12    // truth aggregation

13    Calculate the label truth by Equation (13);

14 return All service labeling quality parameter q, task label truth Y.

# V. ADAPTIVE SERVICE SELECTION

# A. Quality-aided Service Selection Criterion

Suppose that the answers by two different annotation services: $s _ { 1 }$ and $s _ { 2 }$ for label k, are both (0.9:0.1), which means the probability of the presence of label k. In addition, we set the service quality level of these two services to be 0.9 and $0 . 6 ,$ , respectively. Then, we calculate the probability of label k presence or absence from $s _ { 1 }$ based on Eq. (5) as: $P ( \hat { a } _ { k , ( s _ { 1 } ) } ^ { t } = 1 ) =$ $0 . 9 \times 0 . 9 + ( 1 - 0 . 9 ) \times ( 1 - 0 . 9 ) = 0 . 8 2$ , and $P ( \hat { a } _ { k , ( s _ { 2 } ) } ^ { t } = 0 ) \stackrel { \sim } { = } 0 . 9 { \times } ( 1 -$ $0 . 9 ) + ( 1 - 0 . 9 ) \times 0 . 9 = 0 . 1 8$ , to get the final result: (0.82:0.18). Same as the service $s _ { 2 } .$ , we can aggregate its answer to get the final result: $( 0 . 5 8 { : } 0 . 4 2 )$ . Obviously, for the consumer, the former result is more valuable.

Ideally, consumers want to obtain an annotated dataset with both high accuracy and high confidence. By now, we have obtained the task truth distribution and service quality level through the service quality estimation algorithm. For accuracy, we will experimentally evaluate the estimated performance of the task truth distribution. So consumers just greedily choose the service whose answers make the confidence increase the most.

Here, we use Information Entropy as our service selection criterion, and use it to calculate the utility function:

$$
F (\widetilde {\mathcal {S}} ^ {t}, \mathbf {A} _ {k} ^ {t}) = \mathcal {H} \left(y _ {k} ^ {t}, p (y _ {k} ^ {t})\right) = \sum_ {y _ {k} ^ {t}} p (y _ {k} ^ {t}) \log_ {2} \left(p (y _ {k} ^ {t})\right), \tag {14}
$$

where Eq. (14) specifies the utility function we would receive when the true label is $y _ { k } ^ { t } ,$ , meanwhile we aggregate the posterior confidence as $p ( y _ { k } ^ { t } )$ ). If the true label is $y _ { k } ^ { t }$ , then we get a high utility when the estimated posterior confidence $p ( y _ { k } ^ { t } )$ is close to 1, and low utility as the posterior confidence $p ( y _ { k } ^ { t } )$ approaches 0.5.

The optimal selection strategy need to calculate the conditional expected marginal utility for each candidate service. As we cannot know the service’s annotation feedback in advance during the labeling process, we need to enumerate the all possible feedback realization for each service to calculate the conditional expected marginal utility. In a round, for the current task $x ^ { t } .$ , we assume that we have collected some annotation answers until now. Let ${ \pmb \theta } ^ { t , ( 0 ) }$ denote the prior task truth distribution of $\mathbf { y } ^ { t }$ , and let ${ \pmb \theta } ^ { t , ( c ) }$ be the posterior task truth distribution of $\mathbf { y } ^ { t }$ after having collected annotation answers $\mathbf { A } ^ { t , ( c ) }$ . We initialize the prior $\mathbf { \bar { \theta } } ^ { t , ( 0 ) }$ by Uniform Distribution, and the posterior $\pmb \theta ^ { t , ( c ) }$ comes from the output of the service quality estimation algorithm. If we now collect one more annotation answer, we could update the posterior. We assume service will tell us a feedback that we obtain a label answer atk,(s) $a _ { k , ( s ) } ^ { t }$ from tmeans s. The, which $a _ { k , ( s ) } ^ { t }$ $p ( y _ { k } ^ { t } = 1 )$ is unknown in advance, and we could integrate it with the service labeling quality level to obtain $\mathrm { P r } ( \hat { a } = 1 )$ . Hence, we can compute the expected utility the marginal probability of the f $\mathbb { E } \left\lceil F _ { k } ^ { t , ( c + \dot { 1 } ) } \right\rceil$ with respect to, and calculate $a _ { k , ( s ) } ^ { t }$

$$
\begin{array}{l} \Delta_ {F} (s | A _ {k} ^ {t}) = \mathbb {E} \left[ F _ {k} ^ {t, (c + 1)} \right] - F _ {k} ^ {t, (c)} \\ = \sum_ {\hat {a} _ {k, (s)} ^ {t}} \left[ F _ {k} ^ {t} \left(\theta_ {k} ^ {t} | \mathbf {A} _ {k} ^ {t, (c)} \cup \hat {a} _ {k, (s)} ^ {t}\right) \cdot \operatorname * {P r} (\hat {a} _ {k, (s)} ^ {t}) \right] - F (\theta_ {k} ^ {t} | \mathbf {A} _ {k} ^ {t}) \\ = \int_ {a _ {k, (s)} ^ {t}} \operatorname * {P r} (\hat {a} _ {k, (s)} ^ {t}) \sum_ {y _ {k} ^ {t}} \left[ \theta_ {k} ^ {t, (c + 1)} \log_ {2} \left[ \frac {\theta_ {k} ^ {t , (c + 1)}}{\theta_ {k} ^ {t , (c)}} \right] \right] \\ = \mathbb {E} _ {\hat {a} _ {k, (s)} ^ {t}} \left[ \mathbb {E} _ {y _ {k} ^ {t} | \hat {a} _ {k, (s)} ^ {t}} \left[ \frac {\theta_ {k} ^ {t , (c + 1)}}{\theta_ {k} ^ {t , (c)}} \right] \right]. \tag {15} \\ \end{array}
$$

This quantity is the conditional marginal expected utility of annotation feedback sample information for each service. It is also known as the Lindley Information [36], [37], which is essentially the expectation of the Kullback-Leibler Divergence between θt,(c+1) $\bar { \theta } _ { k } ^ { t , ( c + 1 ) }$ k and $\theta _ { k } ^ { t , ( c ) }$ ) with respect to atk,(s). Since utility $a _ { k , ( s ) } ^ { t } .$ function $F$ is a convex function [38], and based on the Lindley Information, consumer always selects the service whose $\Delta _ { F } ( s | A _ { k } ^ { t } ) \ge 0 .$ . This means that the profit function monotonically increases from -1 to 0 as the consumer collects more and more labeling answers, $\Delta _ { F } ( s | A _ { k } ^ { t } )$ essentially quantifies the expected information gain after each selection.

# B. Adaptive Random Greedy Service Selection

It is challenging to design available algorithms for stochastic submodular maximization coverage problem, when the annotation feedback is not determined in advanced during the optimization process. One possible solution is to enumerate tha all possible annotation feedback realization and calculate its generation probability, where the key idea of adaptive submodular is, and run a simple random greedy algorithm to get a near-optimal result with constant approximation ratio.

We turn to an adaptive random greedy service selection strategy [34]. The consumer selects only one service according to the gain-cost-cover [39] in each round. After that, the consumer purchases its annotation service, gives a payment, and collects its annotation answer. Based on the collected annotation result, the consumer can then update the estimated label truth distribution and service labeling quality level. Finally, the consumer iteratively executes this policy until the budget is exhausted, or the consumer has selected all available services, or the estimated label confidence is higher than a threshold $\theta ^ { * }$ . Under such an adaptive service selection strategy, the time complexity is only S. Next we will show that the utility function has an adaptive monotone submodularity property and use it as service selection criterion.

# Lemma 1. The utility function $F ( \widetilde { \cal S } , { \cal A } )$ , which defined in $E q . ( l 5 ) ,$ , is adaptive monotone submodular.

We present the detailed steps of the adaptive greedy service selection strategy in Algorithm 2. The consumer selects each service in an adaptive manner. In each iteration, given the current estimated truth distribution and service labeling quality level, we first compute the expected information gain for each service pair. Then, we select the optimal service with the maximum expected unit information gain. When the consumer has collected this service’s label answer, we can update the estimated label truth distribution and service labeling quality level based on the new answer, as described in Appendix A.

Algorithm 2: Adaptive Random Greedy Service Selection Algorithm   
Input: Target task $x^{t} \in T$ , Candidate service set S and labeling quality level q, service cost $b_{s}$ , Label dataset $A^{t}$ , Budget $B_{t}$ .

Output: Service selection strategy $S^{*}$ , Aggregated task truth $y^{t}$ .

1 Initialize $S^{*} = \emptyset$ ;

2 while $B_{t} > 0$ or $S \neq \emptyset$ do

3 for each service $s \in S \setminus S^{*}$ do

4 Calculate the expected profit gain $F_{gain}$ ;

5 Select the optimal service: $s^{*} = \arg\max\frac{F_{gain}}{||q_{s}||_{1}}$ ;

6 Update the candidate and the selected service set: $S^{*} = S^{*} \cup s^{*}$ , $S = S - s^{*}$ ;

7 Update the remaining budget: $B_{t} = B_{t} - b_{s^{*}}$ ;

8 Assign selected service to annotate the target task and obtain its answers $A_{s^{*}}^{t}$ ;

9 Update label truth distribution by Eq.(21) and Eq.(22);

10 return Service selection strategy $S^{*}$ .

We now show that the adaptive random greedy algorithm achieves a constant approximation ratio of 1 − 1/e [33], [34].

Theorem 2. For the adaptive submodular monotone utility function $F ( \cdot , \cdot ) ,$ , the service set $\widetilde { s }$ returned by the adaptive random greedy algorithm attains at least 1−1/e of the optimal value, that is:

$$
\mathbb {E} [ F (\widetilde {\mathcal {S}}, A) ] \geq (1 - \frac {1}{e}) \max _ {B} \mathbb {E} [ F (\mathcal {S} ^ {*}, A) ]. \tag {16}
$$

# VI. EXPERIMENTS

# A. Experiment Setting

1) Datasets and Ground Truth: We conduct experiments on four public datasets: (1) NUS-WIDE [40], (2) MS-COCO [41], (3) VOC 2007 [42], (4) RCV1 [43]. NUS-WIDE, MS-COCO and VOC 2007 are multi-label image datasets widely used in the area of multi-label classification deep learning. In addition, RCV1 is a multi-label text dataset. Table I summaries the four datasets and their characteristics respectively.

TABLE I: Summary of Datasets. 

<table><tr><td>Dataset</td><td>#Labels</td><td>#Training Instances</td><td>#Test Instances</td></tr><tr><td>NUS-WIDE</td><td>81</td><td>100893</td><td>67742</td></tr><tr><td>MS-COCO</td><td>80</td><td>82081</td><td>40137</td></tr><tr><td>VOC2007</td><td>20</td><td>5011</td><td>4952</td></tr><tr><td>RCV1</td><td>103</td><td>23149</td><td>781265</td></tr></table>

2) Deep Learning Models: We consider the multi-label classification models on images and texts. [44] and [45] respectively propose a multi-label classification deep learning model for image and text data and experimentally prove the performance of the model. Based on their work, we use various initial training settings, such as different network structures, training data set sizes, and training epochs, to obtain multiple different classification models. We use these training models to simulate data annotation API services to provide annotation answers. These models can label images and texts with a wide range of semantic information.

3) Evaluation Metric: We use Mean Absolute Error and Mean Squared Error as metrics to evaluate the performance of the annotation quality level estimation algorithm. The smaller the Mean Absolute Error and Mean Squared Error is, the better the annotation quality level estimation algorithm is. And we use Accuracy to evaluate the performace of the truth aggregation algorithm.

# B. Service Quality Estimation Experiments

In the actual data annotation service market, service annotation quality level and target task truth distribution is both unknown for consumers, which can only be roughly estimated from collected annotation results. Especially whether service annotation quality can be estimated accurately is vital for the service selection strategy. So our first experiment will evaluate the effectiveness of the service annotation quality level and truth distribution estimation algorithm through a series of experiments on simulation datasets to vertify: Can our method accurately distinguish the quality of the annotation service, especially for some spammer services? Can the truth label of the annotation task be accurately inferred?

1) Simulation Dataset.: We generate simulation datasets based on Emotions [10] often used in crowdsourcing experiments, which have known annotation for six labels. For each service, we assume that its annotation quality level has become known, which is drawn from some random distribution, then we generate a random variable as this service’s annotation answer, which satisfies Bernoulli Distribution with annotation quality level as a parameter according to Probability Graph Model. Finally, we run the simulation experiments based on these datasets. For each different hyper-parameter setting, we run the simulation 100 times with different and random generated service annotation quality levels and take the average as the final results. We set that there are 20 data annotation services and test the service annotation quality estimation performance of our method, even when there are some lowquality and spammer services. So, we conduct two kinds of simulation experiments under known but diverse service annotation quality levels to test some parameters of interest:

2) Scenario 1: Service annotation quality level is generated from Uniform Distribution, and there is no Spammer services. In the first scenario, we assume that each service has a good performance, and we draw the annotation quality level parameter of each service independently from Uniform Distribution U (0.6, 0.9). We randomly select different numbers’ tasks from

Emotion. Then, the service annotation answer can be generated from Bernoulli Distribution with the service annotation quality level parameter based on the known Emotion label truth. As for each service annotation domain, we use a hyper-parameter α increasing from 0.2 to 1, which is a prior probability, to indicate whether service s can annotate label k. If not, we set the corresponding $q _ { s , k } = 0$ and do not update that. Of course, we need to confirm that each service at least can provide answers for one label. According to the estimated service annotation quality level, we can also aggregate the final label truth distribution. We plot the simulation results of our experiment in Figure 2.

3) Scenario 2: Perhaps there are low annotation quality levels or Spammer services. Above, we have a slightly optimistic assumption which there are all excellent annotation quality level services. Actually, there may be several services with poor performance in the data annotation market, and we call it as Spammer. When the annotation quality level of service is equal to 0.5, we think that its annotation answers are entirely random. In this scenario, we simply explain the spammer service as a service that has a annotation quality level $q \leq 0 . 5$ . When the annotation quality level of service is less than 0.5, then its answers will reduce the quality of consumer’s collected labels. So when we generate the annotation quality level parameter and set hyper-parameter $\alpha \ = \ 0 . 2$ , we also set another new hyper-parameter $\beta ,$ increasing from 0.6 to 1, which is a probability to control whether a service is Spammer. If it is, we will generate the corresponding annotation quality level parameter from Uniform Distribution U (0.3, 0.5). We repeat experiments and use the same metric with scenario 1 to plot the simulation results in Figure 2.

According to the results of MAE and MSE in Figure 2, our annotation quality estimation algorithm has a good effect on the estimation of service annotation quality in different scenarios. Of course, as the number of test dataset tasks increases, the estimation performance further increases. The parameter α controls the size of the service annotation domain. As α increases, services can provide annotation for more labels, and the corresponding annotation quality parameters that need to be estimated increase, which also leads to an increase in the estimation error of the overall annotation quality. On the other hand, the service annotation domain becomes larger, which increases the number of answers collected and improves the accuracy of truth aggregation.

The parameter β controls the proportion of spammer services. The appearance of the spammer will definitely reduce the quality of annotation answers, thereby affecting the estimation performance of service annotation quality and reducing the accuracy of truth aggregation. Although Figure 2f shows, with the increase of $\beta ,$ the accuracy of truth aggregation has significantly been reduced, in Figure 2b and Figure 2d, the estimation error of our service annotation quality is still in a good state. Therefore, the consumer can filter out poorly performing annotation services based on the estimated service annotation quality. At the same time, our method ensures that buyers only need to spend a small portion of their budget on this matter.

![](images/75d287231b642e5420b65ffebcda502b9ade92e55645ab2fc1d7c5a2298a8977.jpg)



(a) MAE(Scenario 1)

![](images/dfd5b3c49130982205c69b597cac305153d2716f5d00a5c1b77ec6cd13bcf365.jpg)



(b) MAE(Scenario 2)

![](images/73bd2c2e79eab9ba0074052619b2a6cd75c836918d7f23d9c1cb6b19f61e05bb.jpg)



(c) MSE(Scenario 1)

![](images/46c6d6b98d314735ba20aebafc1d7af67ede1e989ff0b04b5365a16811cb07a7.jpg)



(d) MSE(Scenario 2)

![](images/69fe20307996e3f255de97e6b7ffaf2b2e9949e962104e400a26111d266e4b09.jpg)



(e) Accuracy(Scenario 1)

![](images/6e763fa4757775d14cd2ff04cf9645759a02fdd4cc6eac146ebf387ca93bbee6.jpg)



(f) Accuracy(Scenario 2)   
Fig. 2: Comparison result on two scenarios.

# C. Service Selection Experiments

After making a preliminary estimate of service quality, we begin to test the proposed adaptive service combination selection strategy. From the perspective of confidence, for the annotation process of a single task, we analyze its change process of truth distribution aggregation results. Next, we will test the accuracy achieved under different budget constraints on the entire target annotation task set. We list two baseline as follows:

• Random. Choose completely at random until the budget is exhausted, and can use the method in Section IV to aggregate the answers, which only ensuring budget constraints.   
• FrugalMCT [9]. Integrate service post price, annotation quality and categories, to perform an Interage Linear Programming such as FrugalMCT, and use the method in Section IV to aggregate the answers, which ensuring budget constraints and label sete cover constraints.

1) Utility Function Change under Different Price Distribution.: Here, we simulate to show that the utility function change under different price distribution with the same budget constraints and label set cover constraints. In this evaluation, we assume that there are only one target task and 30 data annotation services with parameter setting $\alpha = 0 . 2 , \beta = 0 . 8$ , and there are also two different price distributions: Uniform Distribution $U ( 5 , 1 5 )$ and Normal Distribution N (10, 5) respectively. In addition, we consider a fixed budget B that can include all services. We select annotation services for the current task according to three different strategies: Random, FrugalMCT [9], Adaptive, and draw the change process of truth aggregation results during the annotation process. It can be seen from the two experimental result figure 3a and figure 3b that our strategy shows better performance on two different price distributions. At the same time, after selecting the same number of annotation services, our method obtains the best truth aggregation results. Furthermore, our adaptive method can make the truth aggregation result converge with the minimum number of services, which means that our method consumes the least expected budget.

![](images/d18096203032acd7e1bdaa97393ca77539f4d4774c7773687e5a09771ddb2dcc.jpg)



(a) NUS-WIDE

![](images/592ffb5431bfce0607139c12e64263726220299215a085cc9eb642bc78431db5.jpg)



(b) MS-COCO

![](images/d8ed2a367e7adb3502f096164087f0c289f9e6486058e97acbef4e325e027b13.jpg)



(c) VOC 2007

![](images/cd5b6ae0ab0af3ac402d095a45f705757fbb96145a663765d5f337bfc700269a.jpg)



(d) RCV1   
Fig. 4: Comparison result on real data.

![](images/6b913bfe602b6652c8fe818c599b93ba20ecef27a8dd281ee7c3b237be1385cc.jpg)



(a) Uniform Distribution.

![](images/f3bd2169b207a5d96014b2ea1bafb6c81e121ef0bc9e8650aab3afd6fd5558f9.jpg)



(b) Normal Distribution.   
Fig. 3: Comparison result on different price distribution.

2) Real-world Dataset Experiments.: Now, we validate our adaptive service combination selection strategy through real DL models with different budget constraints to vertify the truth aggregation performance. We train 20 deep learning multilabel classification models based on each of the four datasets in table I. For each model, we randomly select a part of the output result as its annotation categories; here, we set $\alpha = [ 0 . 4 , 0 . 6 ]$ ], that is, each model randomly sets the annotation categories according to the ratio α. We also sample service’s post price randomly from Uniform Distribution U (5, 15), and set the total budget to increase from 50K to 250K(From the expectation calculation, for every 50K budget, the consumer can purchase 5 data annotation services for each of 1000 target tasks.). For each dataset, except for the training dataset, in the test dataset, we randomly select 100 pieces of data as the test task set and 1000 pieces of data as the target task set. We conduct repeated experiments by sampling different target task sets, and obtain the average results, as shown in the figure 4. According to the truth aggregation results under different budget conditions and different selection strategies, the accuracy of the adaptive strategy is higher than that of the other two.

# VII. CONCLUSION

In this work, we study the annotation service selection problem in MLaaS market, to obtain high-quality annotation dataset. We propose a framework, which evaluates services’ labeling quality based on the constructed paobability graph model and, according to an adaptive random greedy algorithm to sequentially identify the optimal service selection strategy within budget constraints. Our evaluation experiments demonstrate that our design achieves significant performance improvement compared with other methods.

The future work can be the extended version of the uncertain or unlimited target label sets. For example, consumers calls the object detection model and collects all the output results. In the current work, target label set is a given and unchanging set and API services are desired to be classification and detection model, so we can evaluate services’ labeling quality on each label. It is interesting to study new service quality evaluation methods and service selection strategies for budget constraints for richer semantic labels.

# ACKKNOWLEDGEMENT

Lan Zhang is the corresponding author. This research is supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, No. 62132018, No. 61822209, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002. This work was partially supported bythe Fundamental Research Funds for the Central Universities.

# REFERENCES

[1] “Google vision api,” 2020, https://cloud.google.com/vision/.   
[2] “Google nlp api,” 2020, https://cloud.google.com/natural-language.   
[3] “Google speech api,” 2020, https://cloud.google.com/speech-to-text.

[4] “Microsoft computer vision api,” 2020, https://azure.microsoft.com/enus/services/cognitive-services/computer-vision.   
[5] “Microsoft speech api,” 2020, https://azure.microsoft.com/enus/services/cognitive-services/speech-to-text.   
[6] “Baiduai,” 2020, https://ai.baidu.com/.   
[7] “Tencent api,” 2020, https://intl.cloud.tencent.com/products/ocr.   
[8] L. Chen, M. Zaharia, and J. Y. Zou, “Frugalml: How to use ml prediction apis more accurately and cheaply,” Advances in Neural Information Processing Systems, vol. 33, pp. 10 685–10 696, 2020.   
[9] L. Chen, M. Zaharia, and J. Zou, “Frugalmct: Efficient online ml api selection for multi-label classification tasks,” arXiv preprint arXiv:2102.09127, 2021.   
[10] Y. Zheng, G. Li, Y. Li, C. Shan, and R. Cheng, “Truth inference in crowdsourcing: Is the problem solved?” VLDB, vol. 10, no. 5, pp. 541– 552, 2017.   
[11] J. Zhang and X. Wu, “Multi-label inference for crowdsourcing,” in SIGKDD, 2018, pp. 2738–2747.   
[12] X. Chen, Q. Lin, and D. Zhou, “Optimistic knowledge gradient policy for optimal budget allocation in crowdsourcing,” in ICML. PMLR, 2013, pp. 64–72.   
[13] Q. Zhang, Y. Wen, X. Tian, X. Gan, and X. Wang, “Incentivize crowd labeling under budget constraint,” in IEEE INFOCOM, 2015, pp. 2812– 2820.   
[14] J. Lei, Z. Zhang, l. Zhang, and X.-Y. Li, “Coca: Cost-effective collaborative annotation system by combining experts and amateurs,” in 38th IEEE International Conference on Data Engineering (ICDE), 2022.   
[15] X. Gan, X. Wang, W. Niu, G. Hang, X. Tian, X. Wang, and J. Xu, “Incentivize multi-class crowd labeling under budget constraint,” JSAC, vol. 35, no. 4, pp. 893–905, 2017.   
[16] J. Sun, N. Liu, and D. Wu, “Budget-constraint mechanism for incremental multi-labeling crowdsensing,” Telecommunication Systems, vol. 67, no. 2, pp. 297–307, 2018.   
[17] Z. Shi, S. Jiang, L. Zhang, Y. Du, and X.-Y. Li, “Crowdsourcing system for numerical tasks based on latent topic aware worker reliability,” in IEEE INFOCOM, 2021, pp. 1–10.   
[18] R. C. Fernandez, P. Subramaniam, and M. J. Franklin, “Data market platforms: Trading data assets to solve data problems,” arXiv preprint arXiv:2002.01047, 2020.   
[19] L. Zhang, Y. Li, X. Xiao, X.-Y. Li, J. Wang, A. Zhou, and Q. Li, “Crowdbuy: Privacy-friendly image dataset purchasing via crowdsourcing,” in IEEE INFOCOM, 2018, pp. 2735–2743.   
[20] A. Agarwal, M. Dahleh, and T. Sarkar, “A marketplace for data: An algorithmic solution,” in Proceedings of the ACM Conference on Economics and Computation, 2019, pp. 701–726.   
[21] J. Liu, “Dealer: end-to-end data marketplace with model-based pricing,” arXiv preprint arXiv:2003.13103, 2020.   
[22] “Mlaas,” 2020, https://www.mordorintelligence.com/industryreports/global-machine-learning-as-a-service-mlaas-market.   
[23] Y. Yao, Z. Xiao, B. Wang, B. Viswanath, H. Zheng, and B. Y. Zhao, “Complexity vs. performance: empirical analysis of machine learning as a service,” in Proceedings of the Internet Measurement Conference, 2017, pp. 384–397.   
[24] L. Chen, P. Koutris, and A. Kumar, “Towards model-based pricing for machine learning in a data marketplace,” in Proceedings of the International Conference on Management of Data, 2019, pp. 1535–1552.   
[25] H. Hosseini, B. Xiao, and R. Poovendran, “Google’s cloud vision api is not robust to noise,” in 16th IEEE international conference on machine learning and applications (ICMLA), 2017, pp. 101–105.   
[26] J. Buolamwini and T. Gebru, “Gender shades: Intersectional accuracy disparities in commercial gender classification,” in Conference on fairness, accountability and transparency. PMLR, 2018, pp. 77–91.   
[27] C. d’Andrea and A. Mintz, “Studying the live cross-platform circulation of images with computer vision api: An experiment based on a sports media event,” International Journal of Communication, vol. 13, p. 21, 2019.   
[28] A. Reis, D. Paulino, V. Filipe, and J. Barroso, “Using online artificial vision services to assist the blind-an assessment of microsoft cognitive services and google cloud vision,” in World Conference on Information Systems and Technologies. Springer, 2018, pp. 174–184.   
[29] M. Yuan, L. Zhang, X.-Y. Li, and H. Xiong, “Comprehensive and efficient data labeling via adaptive model scheduling,” in 36th IEEE International Conference on Data Engineering (ICDE), 2020, pp. 1858– 1861.

[30] M. Yuan, L. Zhang, X.-Y. Li, L.-Z. Yang, and H. Xiong, “Adaptive model scheduling for resource-efficient data labeling,” ACM Transactions on Knowledge Discovery from Data (TKDD), vol. 16, no. 4, pp. 1–22, 2022.   
[31] M. Yuan, L. Zhang, F. He, X. Tong, and X.-Y. Li, “Infi: End-to-end learnable input filter for resource-efficient mobile-centric inference,” in ACM 28th Annual International Conference On Mobile Computing And Networking (MobiCom), 2022.   
[32] M. Yuan, L. Zhang, and X.-Y. Li, “Mlink: Linking black-box models for collaborative multi-model inference,” in Proceedings of the AAAI Conference on Artificial Intelligence, 2022.   
[33] D. Golovin and A. Krause, “Adaptive submodularity: A new approach to active learning and stochastic optimization.” in COLT. Citeseer, 2010, pp. 333–345.   
[34] A. Gotovos, A. Karbasi, and A. Krause, “Non-monotone adaptive submodular maximization,” in Twenty-Fourth International Joint Conference on Artificial Intelligence, 2015.   
[35] X. Chen, Q. Lin, and D. Zhou, “Statistical decision making for optimal budget allocation in crowd labeling,” JMLR, vol. 16, no. 1, pp. 1–46, 2015.   
[36] D. V. Lindley, “On a measure of the information provided by an experiment,” The Annals of Mathematical Statistics, pp. 986–1005, 1956.   
[37] J. Karvanen, J. Vanhatalo, K. Auranen, S. Kulathinal, and S. Mantyniemi, “Optimal design of observational studies: overview and ¨ synthesis,” arXiv preprint:1609.08347, 2016.   
[38] S. Boyd, S. P. Boyd, and L. Vandenberghe, Convex optimization. Cambridge university press, 2004.   
[39] R. Iyer and J. Bilmes, “Submodular optimization with submodular cover and submodular knapsack constraints,” arXiv preprint:1311.2106, 2013.   
[40] T.-S. Chua, J. Tang, R. Hong, H. Li, Z. Luo, and Y. Zheng, “Nus-wide: a real-world web image database from national university of singapore,” in Proceedings of the ACM international conference on image and video retrieval, 2009, pp. 1–9.   
[41] T.-Y. Lin, M. Maire, S. Belongie, J. Hays, P. Perona, D. Ramanan, P. Dollar, and C. L. Zitnick, “Microsoft coco: Common objects in ´ context,” in European conference on computer vision. Springer, 2014, pp. 740–755.   
[42] M. Everingham, L. Van Gool, C. K. Williams, J. Winn, and A. Zisserman, “The pascal visual object classes (voc) challenge,” International journal of computer vision, vol. 88, no. 2, pp. 303–338, 2010.   
[43] D. D. Lewis, Y. Yang, T. Russell-Rose, and F. Li, “Rcv1: A new benchmark collection for text categorization research,” Journal of machine learning research, vol. 5, no. Apr, pp. 361–397, 2004.   
[44] Q. Wang, N. Jia, and T. P. Breckon, “A baseline for multi-label image classification using an ensemble of deep convolutional neural networks,” in IEEE ICIP, 2019, pp. 644–648.   
[45] J. Liu, W.-C. Chang, Y. Wu, and Y. Yang, “Deep learning for extreme multi-label text classification,” in SIGIR, 2017, pp. 115–124.

# APPENDIX

# A. Dynamic Service Quality Update

Here, we assume that we have obtained a feedback from service s, and then how we will update its quality level. As there is no feedback from other services, we will make all other services’ annotation quality levels fixed. So we can then estimate the expected annotation quality level of s by temporarily assuming all other services annotation quality levels are fixed, and repeat this process for other selected service. We have initial service quality level based on history dataset. When new feedback arrives, we can update our estimation based on our previously computed annotation quality level. For each service s that just provided annotation result, using the following rule to update s’s estimated annotation quality level:

$$
q _ {s, k} = \frac {\int_ {0} ^ {1} q _ {s , k} \cdot L _ {q _ {s , k}} \mathrm{d} q}{\int_ {0} ^ {1} L _ {q _ {s , k}} \mathrm{d} q}, \tag {17}
$$

where $L _ { q _ { s , k } }$ is the likelihood of service $s \mathrm { ^ { \circ } s }$ annotation quality level being $\boldsymbol { q } _ { s , k }$ given the current collected annotation dataset Ak,(s): $\mathbf { A } _ { k , ( s ) } \colon$

$$
\begin{array}{l} L _ {q _ {s, k}} = (q _ {s, k}) ^ {T _ {1}} (1 - q _ {s, k}) ^ {T _ {0}} \\ \times \prod_ {x ^ {t} \in \mathbf {A} _ {k, (s)}} \sum_ {y \in \{0, 1 \}} p (\hat {a} _ {k, (s)} ^ {t} = y | a _ {k, (s)} ^ {t}, q _ {s, k}) \tag {18} \\ \times \prod_ {s ^ {\prime} \in \mathcal {S} ^ {t}, s ^ {\prime} \neq s} p (\hat {a} _ {k, (s ^ {\prime})} ^ {t} = y | a _ {k, (s)} ^ {t}, q _ {s ^ {\prime}, k}). \\ \end{array}
$$

where let atk,(s) $a _ { k , ( s ) } ^ { t }$ be the answer of service s to the task $x ^ { t }$ label $k ,$ and $T _ { 1 }$ be the number of test tasks set correctly answered by service $s , T _ { 0 }$ be the number of test tasks set incorrectly answered by service s.

We continue until the service annotation quality level has converged or we have reached a fixed number of iterations. More concretely, our approach is to repeat the above until the service annotation quality level do not change more than a small threshold(such as 0.01) between iteration.

# B. Dynamic Label Truth Aggregation

After collecting the annotation answers from the selected service, we update task truth distribution using the corresponding feedback. As we have estimated service quality level, described in Section $^ \mathrm { I V , }$ the answer choice with the maximum likelihood for a label of a task can be computed in a straightforward Bayesian manner, which is defined as Eq. (9) and Eq. (10). However, we will ignore the parameters defined in the previous section. Given a set of collected annotation answers $\mathbf { A } _ { k } ^ { t }$ and possible truth value $y _ { k } ^ { t }$ for task $x ^ { t }$ label $k ,$ the probability that $y _ { k } ^ { t }$ is a specific value 0 or 1, can be computed using Bayesian Theorem:

$$
\begin{array}{l} p (y _ {k} ^ {t} = y | \mathbf {A} _ {k} ^ {t}) = \frac {p (\mathbf {A} _ {k} ^ {t} | y _ {k} ^ {t} = y) p (y _ {k} ^ {t} = y)}{p (\mathbf {A} _ {k} ^ {t})} \\ = \frac {p (\mathbf {A} _ {k} ^ {t} | y _ {k} ^ {t} = y) p (y _ {k} ^ {t} = y)}{\sum_ {y \in \{0 , 1 \}} p (\mathbf {A} _ {k} ^ {t} | y _ {k} ^ {t} = y) p (y _ {k} ^ {t} = y)}. \tag {19} \\ \end{array}
$$

To simplify, we assume each label answer obeys Uniform Distribution Prior:

$$
p (y _ {k} ^ {t} = y | \mathbf {A} _ {k} ^ {t}) \propto p (\mathbf {A} _ {k} ^ {t} | y _ {k} ^ {t} = y). \tag {20}
$$

We calculate the probability likelihood for all available answers $y \in \{ 0 , 1 \}$ of task $x ^ { t }$ , and find the answer $y _ { k } ^ { t }$ with the maximum likelihood, as follows:

$$
y _ {k} ^ {t} = \underset {y \in \{0, 1 \}} {\arg \max} \prod_ {s \in \mathcal {S} ^ {t}} \left[ p (\hat {a} _ {k, (s)} ^ {t} = y | a _ {k, (s)} ^ {t}, q _ {s, k}) \right]. \tag {21}
$$

The label truth distribution $\theta _ { k } ^ { t }$ can be computed by normalizing the computed result of Eq. (21). We can refer to this as the confidence that the correct answer to task $x ^ { t }$ label k is answer 1:

$$
\theta_ {k} ^ {t} = \frac {\prod_ {s \in \mathcal {S} ^ {t}} \left[ p (\hat {a} _ {k , (s)} ^ {t} = 1 | a _ {k , (s)} ^ {t} , q _ {s , k}) \right]}{\sum_ {y \in \{0 , 1 \}} \prod_ {s \in \mathcal {S} ^ {t}} \left[ p (\hat {a} _ {k , (s)} ^ {t} = y | a _ {k , (s)} ^ {t} , q _ {s , k}) \right]}. \tag {22}
$$