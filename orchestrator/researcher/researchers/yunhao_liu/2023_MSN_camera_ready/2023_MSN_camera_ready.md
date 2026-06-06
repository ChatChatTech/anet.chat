# Adaptive and Efficient Participant Selection in Vertical Federated Learning

Jiahui Huang∗, Lan Zhang∗†, Anran Li∗, Haoran Cheng∗, Jiexin Xu‡, Hongmei Song‡, ∗ School of Computer Science and Technology, University of Science and Technology of China, Hefei, China † Institute of Dataspace, Hefei Comprehensive National Science Center, China ‡ China Merchants Bank, China

{hjh233,anranLi,chr990315}@mail.ustc.edu.cn,{zhanglan}@ustc.edu.cn, {jiexinx,songhongmei}@cmbchina.com

Abstract—Vertical Federated Learning (VFL) enables multiple data owners to collaboratively train a global model, while preserving data privacy. However, significant communication overhead arises during the training phase due to the transmission of massive encrypted intermediate results. Our investigation into the performance of the model with varying participant numbers reveals that increasing participants, especially in larger groups, may not necessarily yield substantial performance improvements. Instead, it tends to introduce additional communication overhead. Therefore, in the context of VFL, participant selection emerges as a crucial strategy to mitigate communication cost, though it remains a relatively unexplored domain. In this work, we propose a novel adaptive participant selection method in VFL, named VFLMG, to dynamically determine the number of selected participants, as well as to identify the group of participants that best strikes a balance between model performance and communication overhead. Evaluations on various datasets show that VFLMG significantly reduces communication overhead while only causing a minimal loss in accuracy. For instance, in the MNIST and Fashion MNIST datasets, VFLMG reduces communication costs by 32.1% and 27.6% respectively, with an accuracy drop of 0.5% and 0.3%.

Index Terms—vertical federated learning, participant selection, communication overhead reduction

# I. INTRODUCTION

Federated learning (FL) [1] is an emerging paradigm in distributed machine learning that facilitates collaborative training of multiple data owners, while preserving privacy of local data. Based on how data is partitioned, FL can be categorized into two types: 1) horizontal FL (HFL) and 2) vertical FL (VFL). Under HFL [2]–[6], different parties share the same feature space but have different sample spaces. Under VFL, data owners share the same sample space, while each possesses unique feature space [7]–[9]. VFL scenarios often arise when companies from different business sectors join forces to train a machine learning model. In a traditional VFL setting, the data owner who holds both the class label and data features is called the active party, while the data owner who has only the data features is called the passive party.

In a typical VFL setting, passive parties are introduced to expand the feature spaces and thereby enhance the performance of the VFL model. In most cases, involving more participants in the training process will yield a VFL model that performs no worse than a model trained with fewer participants [10], [11]. However, this approach also gives rise to the following problems. First, training with massive number of participants would incur an extremely complex VFL model and thus significant computation and communication overhead since each training round involves multiple forward/backward operations and intermediate parameter transfers. As an example, one of our experiments in Section III-B showed that when the number of passive participants increased from 4 to 8, the communication cost of training a VFL classifier using the MNIST dataset increased by 700 GB while the test accuracy improved only by 2.8%. Second, the quality of data owner’s data features directly determines the effectiveness of their local models, thereby affecting the performance of the global VFL model [11]. In practice, some data owners can possess features that are redundant or irrelevant to the learning task. Engaging those low quality parties into training would result in a low quality VFL model. Thus, participant selection for VFL emerges as a crucial issue.

Various participant selection methods have been proposed for HFL [12]–[14], while few work focused on VFL. Participant selection methods for HFL can be divided into two branches. One branch utilizes the participant contribution evaluation results [15], e.g., calculated through Shapley values, to select participants and optimize the global model aggregation. However, since Shapley value-based methods account for complex dependencies, they are prohibitively expensive to calculate. The other branch proposes various statistical selection metrics, e.g., differences of model updates [13] or local losses [3], [14]. Due to the inherent differences in the learning paradigms, participant selection methods for HFL cannot be directly applied to VFL. As for participant selection in VFL, there is only one existing work [16] that employs mutual information and a group testing method to assign a score to each participant and perform selection. However, it assumes prior knowledge on the number of selected participants, making it unsuitable for practical VFL applications. Other relevant approaches consider feature selection for VFL [11], [17] which calculate per-feature relevance scores based on statistical measures. Nonetheless, these approaches can not directly scale to participant-level selection in VFL since the importance of features is not additive.

To enable participant selection in VFL settings, the following key questions need to be addressed. 1) At which stage should we conduct participant selection: before, during or after model training? Since our primary objective is to reduce communication overhead, conducting participant selection during or after model training is not applicable, as it would incur communication cost no less than directly training the VFL model using all participants. Hence, we need to select a group of participants before VFL model training without observation of each participant’s actual performance. 2) How to efficiently and privately quantify the contribution of each group of participants to the VFL model without training the model? Existing work [16] proposes a secure joint mutual information (JMI) computation protocol to evaluate the overall performance of the joint model. However, the straightforward calculation of JMI requires large communication and computation cost, making it less suitable for VFL scenarios with limited resources. 3) How to identify the group of participants that contributes most to the global model among all possible combinations? Directly searching over all possible participant groups is computationally expensive and impractical due to the exponential growth in the number of combinations with the increasing number of participants. How to efficiently identify the group of participants that contributes the most is a crucial issue for the framework design. 4) How to select the set of participants to strike a balance between model accuracy and training overhead? In practice, it has been found that when the number of participants exceeds a certain size, the addition of extra participants leads to marginal improvement in model performance, while causing unnecessary waste of computing and communication resources. Therefore, it is important to dynamically determine the number of participants to achieve the optimal balance between model accuracy and training overhead.

To address the aforementioned questions and the limitations of existing works, we propose an adaptive maximal gainbased participant selection approach for vertical federated learning (VFLMG). It involves computing the gain of a VFL model given a set of selected passive parties. By employing a greedy algorithm to maximize this gain, VFLMG efficiently and dynamically identifies the optimal set of participants. Our contributions are summarized as follows:

• To the best of our knowledge, this is the first work solving the adaptive participant selection for VFL by taking the trade-off between model performance and communication overhead. VFLMG achieves highly efficient and private participant selection as well as high-performance model construction simultaneously through the maximization of participants’ gain values. The definition of the participant’s gain takes into account both the joint mutual information between individual features, target labels and communication cost.

• We design a participant selection method that utilizes a greedy approach with an approximation ratio of $\textstyle { 1 - { \frac { 1 } { e } } }$ to identify the desired set of participants. We have provided a rigorous proof that the selected group of participants achieves the maximum gain value among all possible output participant groups using our algorithm. To accelerate the selection process, we leverage a method that uniformly samples the training data to achieve up to a 5× speedup with a bounded error.

• We evaluate VFLMG via extensive experiments on four datasets including tabular data and images in a VFL system. VFLMG significantly outperforms state-of-the-art approach in terms of achieving accurate and private selection of participants to build high-performance VFL models. Compared to existing approach, VFLMG selects 31.3% fewer participants on average. Specifically, VFLMG incurs 32.1% and 27.6% lower communication cost with only 0.5% and 0.3% accuracy drop in the MNIST and Fashion MNIST datasets respectively.

# II. RELATED WORK

A large amount of previous work has been dedicated to participant selection in federated learning, yet most of them focus on the topic of HFL. Random selection in HFL [2] has been found to exhibit suboptimal model performance and can introduce fairness issues. To address these problems, Fraboni et al. [12] introduce clustered sampling to select more representative clients. Balakrishnan et al. [13] propose to select a small subset of clients that can provide diverse and representative information in gradient space to approximate the full gradient with all clients. Both approaches have been shown to effectively improve model performance. Oort [14] considers a trade-off between client statistical utility and system efficiency, which significantly speeds up the training procedure while also achieving performance gain. Fairness guarantees can be ensured through the utilization of multiarm bandit models [18], [19]. However, all thses methods are specifically designed for HFL and not applicable in VFL.

In the context of participant selection in VFL, Jiang et al. [16] employ mutual information and a group testing method to assign a score to each participant. Based on these scores, a fixed size of participants with the highest scores are then selected. However, this method is based on the assumption that the number of selected participants is predefined, which restricts its applicability in real-world scenarios. Other related research aims to conduct feature selection in VFL, as the quality of features directly influences the performance of the VFL model. A secure federated $\chi ^ { 2 }$ test protocol is introduced in [17], which produces highly consistent results with those in centralized setting. Li et al. [11] propose FedSDG-FS, which leverages a Gaussian stochastic dual-gate to securely and efficiently select features during the training process.

# III. PRELIMINARIES & PROBLEM DESCRIPTION

# A. Basic Setup of VFL

Typically, there are two types of participants involved in VFL: the active party who possesses labels and the passive party who only holds the features. Specifically, we consider n participants $\{ P _ { 1 } , P _ { 2 } , \cdots , P _ { n } \}$ collaborating to train a global VFL model $\theta _ { G } ^ { * }$ by integrating their private datasets. Without loss of generality, we denote the participant $P _ { n }$ as the active party, and the other participants $\{ P _ { 1 } , \cdots , P _ { n - 1 } \}$ as the passive parties. The global model $\theta _ { G } ^ { * }$ can be divided into a top model $\theta _ { T }$ held by the active party and multiple bottom models $\theta _ { B } =$ $\{ \theta _ { b , 1 } , \cdot \cdot \cdot , \theta _ { b , n } \}$ held by each participant. Here we consider a supervised classification task and denote the number of classes as $C .$ The dataset of participant Pi can be formulated as $\mathcal { D } _ { i } =$ $\{ x _ { t } ^ { i } \} _ { t = 1 } ^ { N }$ , where $\boldsymbol { x } _ { t } ^ { i } \in \mathbb { R } ^ { d _ { i } }$ represents the t-th sample with $d _ { i }$ features and N is the total number of samples. The labels owned by the active party $P _ { n }$ are denoted as $Y = \{ y _ { t } \} _ { t = 1 } ^ { N }$ .

In the forward phase, each passive party $P _ { i }$ learns to map a sample $\boldsymbol { x } _ { t } ^ { i }$ to a latent representation $h _ { t } ^ { i } .$ corresponding to the mapping $\mathbb { R } ^ { d _ { i } }  \mathbb { R } ^ { d _ { i } ^ { * } }$ . Here $d _ { i } ^ { * }$ represents the dimension size of the latent representation, and it is typically smaller than $d _ { i }$ . Subsequently, the active party $P _ { n }$ with the top model $\theta _ { T }$ aggregates the latent representations of the samples from all participants and computes $\hat { y } _ { k }$ through the mapping $f _ { \theta _ { T } } ( h _ { t } ^ { 1 } , \cdots , h _ { t } ^ { n } )$ , which is $\mathbb { R } ^ { n \times d _ { i } ^ { * } } \to \mathbf { \bar { \mathbb { R } } } ^ { C }$ . Based on this setup, the objective of VFL can be defined as minimizing:

$$
R (\theta_ {G}) = \sum_ {t = 1} ^ {N} \ell (f _ {\theta_ {T}} (h _ {t} ^ {1}, \dots , h _ {t} ^ {n}), y _ {k}) + \sum_ {i = 1} ^ {n} \Omega (\theta_ {b, i}) + \Omega (\theta_ {T})
$$

$\mathrm { w i t h } h _ { t } ^ { i } = f _ { \theta _ { b , i } } ( x _ { t } ^ { i } ) , i \in \{ 1 , \cdot \cdot \ , n \}$ (1)

where ℓ is the cross entropy loss function, and Ω is a perparticipant regularizer that limits the complexity of the model. In the backpropagation phase, we utilize stochastic gradient descent to minimize Eq. 1 until the global model $\theta _ { G } ^ { * }$ satisfies the convergence criterion.

# B. Motivation Analysis

Here, we conduct data-driven analysis to emphasize the importance of participant selection in VFL. We illustrate this from the perspective that training VFL models with large number of participants would incur significant computation and communication overhead while improving test accuracy only marginally. Specifically, we use the MNIST dataset as training data and conduct experiments in the VFL scenario involving one active party and up to eight passive parties. Here, we randomly assign 10 features from the total 784 features to each participant to simulate real scenarios. We use different numbers of passive parties for joint training and record the model prediction accuracy and the communication overhead during training. Under different numbers of passive parties, we repeated the experiment 5 times with different random seeds and reported the average results in Figure 1.

![](images/1036004874fa92e4675a3965697786a7ea10e0a8825989eec7a514113919f163.jpg)



Fig. 1. Test accuracy and communication cost (GB) with different number of passive parties.

The results show that as the number of participants increases, the communication overhead increases significantly, while the improvement in test accuracy is negligible. For instance, when all eight passive parties participate in VFL model training, the test accuracy increases by only 2.8% compared to the setting with four passive parties, while the communication cost rises substantially to 1400GB, which is twice the cost of four passive parties training. These results show that an efficient and privacy-preserving participant selection method is urgently needed for VFL with massive candidate participants.

# C. Problem Description

We consider a scenario where m passive parties are selected from n − 1 passive ones for model training, so as to obtain a VFL model $\theta _ { G ^ { \prime } } ^ { * }$ whose test accuracy is comparable to $\theta _ { G } ^ { * }$ . This selection procedure aims to reduce communication costs while maintaining a high test accuracy model. It is essential to ensure that the inclusion of the selection procedure does not compromise security and privacy guarantees in the VFL setting. Specifically, original features and labels can not be revealed by any entity other than the data owner itself. Our objective is to minimize the following equation:

$$
\begin{array}{l} R (\theta_ {G ^ {\prime}}) = \sum_ {t = 1} ^ {N} \ell (f _ {\theta_ {T ^ {\prime}}} (h _ {t} ^ {1} \odot s _ {1}, \dots , h _ {t} ^ {n - 1} \odot s _ {n - 1}, h _ {t} ^ {n}), y _ {t}) \\ + \sum_ {i = 1} ^ {n - 1} \Omega (\theta_ {b, i}) \odot s _ {i} + \Omega (\theta_ {b, n}) + \Omega (\theta_ {T ^ {\prime}}) + \lambda m \\ \end{array}
$$

$\mathrm { w i t h } h _ { t } ^ { i } = f _ { \theta _ { b , i } } ( x _ { t } ^ { i } ) , i \in \{ 1 , \cdot \cdot \ , n \}$ (2)

where $S ~ = ~ \{ s _ { 1 } , s _ { 2 } , \ldots , s _ { n - 1 } \} ~ \in ~ \{ 0 , 1 \} ^ { n - 1 }$ represents indicator variables and $\begin{array} { l c l } { { \sum _ { i = 1 } ^ { n - 1 } s _ { i } } } & { { = } } & { { m } } \end{array}$ . Each element $s _ { i }$ indicates whether participant $P _ { i }$ is selected for model training, $i . e . , s _ { i } = 1$ implies participant $P _ { i }$ is selected, $i \in \{ 1 , \cdots , n \}$ . The term λm acts as a regularizer to restrict the number of selected parties.

# IV. PROPOSED METHOD

In this section, we first introduce the system architecture of our proposed method. We then illustrate the key idea that enables participant selection to be performed before model training under VFL settings. Next, we provide comprehensive details of the implementation process and present the the specific idea of the selecting algorithm.

# A. System Overview

Our proposed method focuses on selecting participants before model training (as shown in Figure 2). This is accomplished by first defining the gain for the VFL model and then seeking to identify a subset of participants to maximize the gain. The definition of gain involves JMI and communication cost. To efficiently calculate JMI, we design a sampling protocol as described in Section IV-C. Our participant selection algorithm, named VFLMG, adopts a greedy approach and guarantees that the selected group of participants yields the maximal gain among all possible outputs, as illustrated in Section IV-D.

![](images/d3a87006cdfab30eeba73c8930b3c2bc22494552af231fcad2ba41a614917363.jpg)



Fig. 2. System Overview of FedMG. Notations: ⃝1 : bottom embeddings, $\textcircled{2} :$ intermediate gradients

![](images/c84eaac7774f638bee04022f6eaaa11acc39a4e64999447fa1786a7d254996bb.jpg)



(a) Joint mutual information and corresponding test accuracy of different groups of participants in MNIST dataset.

![](images/1b76eb3dc82c739d72258caffcdfbb855f8cf1b4b79aa54f04d74d60f16c7e0d.jpg)



(b) Joint mutual information and corresponding test accuracy of different groups of participants in Fashion MNIST dataset.   
Fig. 3. Joint mutual information and corresponding test accuracy of different groups of participants in different datasets.

# B. Definition of JMI-based Performance Gain for VFL

Since we aim to perform participant selection before model training, we need answer the question: How can we assess the predicative capability of the VFL model without actual training? Joint Mutual Information (JMI) between the feature space and the label space provides a principled solution by quantifying the significance of the combined features, thereby assessing the contribution of an individual participant or a group of participants to the VFL model. Specifically, JMI serves as a measure of the information that features X provide to labels Y . High JMI values between X and Y indicate strong correlations between them. Consequently, when utilizing features with high JMI, we can anticipate an enhanced ability to predict labels [20], [21]. As depicted in Fig. 3, it becomes evident that as the number of passive parties increases, the JMI between the joint feature space and the label space also increases, subsequently leading to an improvement in the final test accuracy. Consequently, we transform the objective from minimizing $R ( \theta _ { G ^ { \prime } } )$ to the task of maximizing JMI. To constrain the communication overhead, we propose to replace λm in Equation 2 with is measured by the total comm $\begin{array} { r } { C = \beta \times \frac { m } { n - 1 } } \end{array}$ . This new term incurred by the active party and increases linearly with the number of selected passive parties.

We denote the mutual information between all features and labels, i.e., $M I ( \{ X _ { 1 } , \ldots , X _ { n - 1 } , X _ { n } \} ; Y )$ as $M I _ { n }$ , and define the gain by including m passive parties in VFL training as

$$
\begin{array}{l} G (m) = \alpha \frac {\max M I (\{X _ {i 1} , X _ {i 2} , \ldots , X _ {i m} , X _ {n} \} ; Y)}{M I _ {n}} \\ - \beta \times \frac {m}{n - 1}, m = 0, 1, \ldots , n - 1 \\ \end{array}
$$

where α and $\beta$ are empirical parameters.

To determine the value of α and $\beta ,$ we consider two extreme conditions: a) the active party trains a model by itself; b) the active party chooses to train with all passive parties. In the first condition, the communication overhead is zero as the active party trains a model by itself. However, the performance of the locally trained model is expected to be poor. In the second condition, we expect the best model performance as it involves training with all passive parties, which also results in the maximum communication cost. We assume that the gains in these two conditions follow the equation below:

$$
G (0) = \mu G (n - 1) \tag {4}
$$

where $\mu$ is a tunable parameter.

The parameter $\mu$ controls the trade-off between reducing communication cost and improving model performance. A larger value of $\mu$ indicates a higher emphasis on reducing communication cost, while a smaller value of $\mu$ prioritizes improving model performance. The choice of $\mu$ allows for flexibility in finding the desired balance between these two objectives, which allows you to tailor the selection of a group of participants according to your specific requirements and priorities in VFL. According to Equation 4, we have

$$
(1 - \frac {1}{\mu} \frac {M I (X _ {n} ; Y)}{M I _ {n}}) \alpha = \beta \tag {5}
$$

In our case, we prioritize the reduction of communication overhead over model performance, and set $\mu = 1$ . Based on this, we derive the following equation:

$$
\alpha = \frac {M I _ {n}}{M I _ {n} - M I (X _ {n} ; Y)} \beta \tag {6}
$$

This empirical equation has been validated through extensive experiments and $\beta$ is always set to be 1.

The value of m can be determined by solving the following problem:

$$
m = \underset {m} {\arg \max} G (m) \tag {7}
$$

# C. Efficient JMI Calculations with Data Sampling

Here we estimate JMI based on KNN [22]. For dataset $\mathcal { D } =$ $\{ ( x _ { i } , y _ { i } ) \} , i = 1 , 2 , \ldots , N , x _ { i }$ stands for feature of instance i and $y _ { i }$ represents the label. For $\forall i ,$ we first identify k nearest neighbors of data point i from a pool of $N _ { i }$ data points that share the same label as $y _ { i }$ and determine the maximal distance $d _ { i }$ between point i and these k points. Then we calculate the number of points $n _ { i }$ whose distance are less than or equal to $d _ { i }$ in the entire dataset. Based on the obtained values, we compute $I _ { i }$ as follows:

$$
I _ {i} = \psi (N) + \psi (k) - \psi (N _ {i}) - \psi (n _ {i}) \tag {8}
$$

where $\begin{array} { r } { \psi ( z ) = \frac { d } { d z } \ln \Gamma ( z ) \sim \ln z - \frac { 1 } { 2 z } } \end{array}$ is the digamma function. To estimate JMI, we average $I _ { i }$ over all data points.

$$
I (X, Y) = \frac {1}{N} \sum_ {i = 1} ^ {N} I _ {i} \tag {9}
$$

In VFL setting where features are distributed among different parties, it is a necessity to compute JMI in a privacypreserving way. To address this problem, we utilize homomorphic encryption(HE) and adopt the approach described in [16], which introduces a aggregation server and a key server. However, this approach may incur heavy communication cost, particularly when the dataset size N is large since encrypted data of size $O ( N ^ { 2 } )$ needs to be transmitted. To mitigate this, we employ a sampling strategy during JMI computation. Detailed procedure is shown in Algorithm 1 and privacy concerns are analyzed in section IV-E. To demonstrate that the utilization of sampling does not compromise the accuracy of the JMI result, we give the following lemma.

Lemma 1. We denote $\hat { I }$ as the estimated joint mutual information using M instances randomly sampled from $\mathcal { D } =$ $\{ ( x _ { i } , y _ { i } ) \} , i = 1 , 2 , . . . , N$ . Let ${ \cal B } _ { 1 } = \operatorname * { m i n } _ { i } \{ \psi ( M ) + \psi ( k ) -$ $2 \psi ( M _ { i } ) \} , \ B _ { 2 } \ = \ \mathrm { m a x } _ { i } \{ \psi ( M ) + \psi ( k ) - \psi ( M _ { i } ) - \psi ( 1 ) \} \nonumber$ , $B ~ = ~ B _ { 2 } ~ - ~ B _ { 1 } ,$ , we have that for $\delta ~ \in ~ ( 0 , 1 ) , \epsilon ~ > ~ 0 ,$ , $\begin{array} { r } { P r [ | \hat { I } - E [ \hat { I } ] | \ge \epsilon ] \le \delta ~ i f M \ge \frac { B ^ { 2 } \ln \frac 1 \delta } { 2 \epsilon ^ { 2 } } } \end{array}$ .

Proof Sketch. For each data instance $i ,$ we have

$$
I _ {i} = \psi (M) + \psi (k) - \psi (M _ {i}) - \psi (m _ {i}) \in [ B _ {1}, B _ {2} ] \tag {10}
$$

Now that

$$
\hat {I} = \frac {1}{M} \sum_ {i = 1} ^ {M} I _ {i} \tag {11}
$$

According to Hoeffding’s inequality, we have

$$
P r [ | \hat {I} - E [ \hat {I} ] | \geq \epsilon ] \leq e x p (- \frac {2 \epsilon^ {2}}{\frac {B ^ {2}}{M}}) \tag {12}
$$

By having $\begin{array} { r } { e x p \big ( - \frac { 2 \epsilon ^ { 2 } } { \frac { B ^ { 2 } } { M } } \big ) \leq \delta , } \end{array}$ 2 ϵ 2 we have $\begin{array} { r } { M \ge \frac { B ^ { 2 } \ln \frac { 1 } { \delta } } { 2 \epsilon ^ { 2 } } } \end{array}$ M

Specifically, in the MNIST dataset, which has a training set of size 60,000, it is sufficient to randomly sample 23,000 instances to compute JMI while maintaining a satisfactory level of accuracy. This can be achieved by setting $\epsilon = 0 . 1$ and $\delta = 0 . 0 1$ .

# D. Maximum Gain-based Participant Selection

Given the value of $m ,$ , selecting m participants with the highest joint mutual information (JMI) out of n is NP-Hard. However, we can obtain a $( 1 - \frac { 1 } { e } ) - O P T$ solution efficiently in a greedy manner [24]. By utilizing the greedy algorithm, we denote the set of selected i passive parties as $S _ { i }$ . The joint mutual information between the total feature space of the active party with $S _ { i }$ and label space is denoted as $J M I _ { i + 1 }$ and it is calculated as $M I ( \{ X _ { n } \cup _ { k , P _ { k } \in S _ { i } } X _ { k } \} ; Y )$ . We first give the following lemma.

Algorithm 1: JMI Computation with data sampling   
Input: Active Party Initialize: $\epsilon, \delta$ .

Output: JMI between features of specified parties and labels.

1 Key server generates key pairs $(p_{k}, s_{k})$ for HE, distributes $s_{k}$ to active party and $p_{k}$ to aggregation server and all passive parties.

2 Each party shuffles its local data instances using a random seed generated by active party, and treats the shuffled order as the corresponding pseudo ID.

3 Active party $P_{0}$ calculates $M = \min\{\frac{B^{2} \ln \frac{1}{\delta}}{2\epsilon^{2}}, N\}$ , then randomly selects M instances from the original N instances, denotes the index as $Index_{M}$ and sends $Index_{M}$ to all passive parties.

4 for query pair $q = (x_{q}, y_{q}) \in \mathcal{D}_{sampled}$ do

5 Each party $P_{i}$ calculates partial distance $\mathbf{d}_{i} = [(x_{q,i} - x_{j,i})^{2} \text{ for } (x_{j}, y_{j}) \in \mathcal{D}_{sampled}]$ , sorts it in ascending order and transmits the ordered pseudo IDs $pID_{i}$ to aggregation server.

6 Aggregation server utilizes Fagin's algorithm [23] to determine the pseudo IDs of $k'$ samples and sends $pID_{k'}$ to all parties.

7 Each party encrypts partial distances of samples in $pID_{k'}$ using $p_{k}$ and sends them to aggregation server.

8 Active party sends indicator = {0, 1, ..., 1}^{n-1} to aggregation server to indicate whose encrypted distances to aggregate.

9 Aggregation server adds partial distances under encryption and sends the result to active party.

10 Active party decrypts distances using $s_{k}$ and calculates $\hat{I}_{q}$ .

11 Active party calculates the mean value of all $\hat{I}_{q}$ .

12 return $MI(\{X_{n} \cup_{i,indicator[i]=1} X_{i}\}; Y)$

Lemma 2. For $\forall i = 1 , \ldots , n - 2 ,$ we have

$$
J M I _ {i + 2} - J M I _ {i + 1} \leq J M I _ {i + 1} - J M I _ {i} \tag {13}
$$

Proof Sketch. Without loss of generality, we may assume $S _ { i + 1 } = S _ { i } \cup P _ { p } , S _ { i + 2 } = S _ { i + 1 } \cup P _ { q } .$ According to the submodularity of mutual information [24], we have for $\cdot i = 0 , \ldots , n - 3$

$$
\begin{array}{l} J M I _ {i + 3} - J M I _ {i + 2} \tag {14} \\ \leq M I \left(\left\{X _ {n} \cup_ {k, P _ {k} \in S _ {i}} X _ {k} \cup X _ {q} \right\}; Y\right) - J M I _ {i + 1} \\ \end{array}
$$

Now that we select the participants in a greedy manner, we have

$$
J M I _ {i + 2} \geq M I (\{X _ {n} \cup_ {k, P _ {k} \in S _ {i}} X _ {k} \cup X _ {q} \}; Y) \tag {15}
$$

By combining equation 14 and equation 15, we complete the proof.

Based on Lemma 2, we can establish that the difference in JMI of adjacent groups decreases monotonically as the number of selected participants increases. Consequently, the increment in gains also decreases monotonically. This observation allows us to derive an algorithm that effectively determines the value of m and generates the final set of participants for the training procedure.

Algorithm 2: Maximum Gain-based Participant Selection   
Input: Passive parties $P = \{P_{1}, P_{2}, \ldots, P_{n-1}\}$ ,
selected parties $S_{0} = \emptyset$ , indicator variables $S = \{0\}^{n-1}$ , $\beta = 1$ Output: Selected number of passive parties m,
indicator variables S.

1 Calculate $MI_{n}$ , $MI(X_{n}; Y)$ , $\alpha$ , $\hat{G}(0) = \alpha \frac{MI(X_{n}; Y)}{MI_{n}}$ 2 for $i = 1, 2, \ldots, n - 1$ do

3 index =
arg max $_{j, P_{j} \in P} JMI(X_{n} \cup_{k, P_{k} \in S_{i-1}} X_{k} \cup X_{j}; Y)$ 4 Calculate $\hat{G}(i) = \alpha \frac{MI(\{X_{n} \cup_{k, P_{k} \in S_{i-1}} X_{k} \cup X_{index}\}; Y)}{MI_{n}} - \beta \times \frac{i}{n-1}$ 5 if $\hat{G}(i) \leq \hat{G}(i - 1)$ then

6 return m = i - 1, S

7 break

8 $P = P \setminus P_{index}$ , $S_{i} = S_{i-1} \cup P_{index}$ , $s_{index} = 1$ 9 if i = n - 1 then

10 return m = n - 1, S

Proposition 1. For $\forall \alpha , \beta \ > \ 0 ,$ , we have $\begin{array} { r l } { \hat { G } ( m ) } & { { } = } \end{array}$ $\begin{array} { r } { \operatorname* { m a x } _ { j \in \{ 0 , 1 , \ldots , n - 1 \} } \hat { G } ( j ) } \end{array}$ .

Proof Sketch. 1) $m \neq 0 , n - 1 .$ .

Given $\hat { G } ( m + 1 ) \leq \hat { G } ( m )$ , we have

$$
\alpha \frac {J M I _ {m + 2} - J M I _ {m + 1}}{M I _ {n}} \leq \frac {\beta}{n - 1} \tag {16}
$$

According to our algorithm, we have ${ \hat { G } } ( i ) \geq { \hat { G } } ( i - 1 )$ for $i = 1 , . . . , m . \ F o r \ i = m + 2 , . . . , n - 1 ,$ , based on Lemma 2, we have

$$
\begin{array}{l} \alpha \frac {J M I _ {i + 1} - J M I _ {i}}{M I _ {n}} \\ \leq \alpha \frac {J M I _ {m + 2} - J M I _ {m + 1}}{M I _ {n}} \leq \frac {\beta}{n - 1} \\ \end{array}
$$

which indicates ${ \hat { G } } ( i ) \leq { \hat { G } } ( i - 1 )$ . Thus we have $\hat { G } ( m ) =$ $\operatorname* { m a x } _ { j } \hat { G } ( j )$ .

2) Based on the above analysis, we can say that $i f m = 0 ;$ , we have $\hat { G } ( 0 ) \geq \hat { G } ( 1 ) \geq \hat { G } ( 2 ) \geq \cdots \geq \hat { G } ( n - 1 )$ . If $m = n - 1$ , we have ${ \hat { G } } ( 0 ) \leq { \hat { G } } ( 1 ) \leq { \hat { G } } ( 2 ) \leq \cdots \leq$ $\hat { G } ( n - 1 )$ .

According to Proposition 1, instead of traversing all n possible results, we continuously compare the gains of adjacent groups. Once we observe a drop in gain, we obtain the final selected group can conclude that it provides the maximal gain among all possible n outputs, which can reduce computation overhead by avoiding unnecessary evaluations.

# E. Privacy Analysis

Following the setup in previous work [25], we make the assumption that the key server is honest, the aggregation server and all the participants are honest but curious. In our proposed protocol, there are three potential stages where privacy breaches could occur. 1) After calculating the partial distances, the ordered pseudo IDs are transmitted in plain text to the server, yet the server cannot reveal any information about the original user IDs after the shuffling procedure, which ensures the privacy of user identities. 2) Partial distances are transmitted to the aggregation server, however, they are encrypted through homomorphic encryption, ensuring that the semi-honest aggregation server has no access to the distance information of all participants. This preserves the privacy of the participants’ original features. 3) In the sampling step, the active party calculates the minimal number of required instances and distributes IndexM to all passive parties. The former step is performed by the active party alone locally and does not raise any privacy issues as it does not involve the exchange of sensitive information with other parties. After the allocation of $I n d e x _ { M }$ , passive parties are aware of the value of M but they do not have access to the specific values of ϵ and δ. Consequently, they cannot infer the exact values of maxi $N _ { i }$ and mini $N _ { i }$ , which in turn prevents them from deducing the potential distribution of labels. Therefore, the privacy of the label distribution is preserved in the process. In summary, in comparison to the original VFL protocol, our protocol does not introduce any additional privacy leakage.

# V. EVALUATIONS

# A. Experimental Setting

1) Datasets: We evaluate the effectiveness of VFLMG on multiple datasets, including MNIST, Fashion-MNIST, Gisette and COIL20. In the case of the MNIST and Fashion-MNIST datasets, we consider each pixel as a distinct feature. We randomly split the remaining two datasets into training sets and testing sets in a ratio of 8:2. We primarily conduct experiments using two sets of configurations: one with each participant having a small number of features, and another with each participant having a larger number of features. In the first setting, each party is assigned 10,10,20,10 features in $\mathcal { D } _ { M } , \mathcal { D } _ { F M } , \mathcal { D } _ { G } , \mathcal { D } _ { C }$ respectively. In the second setting, each party is allocated 80,80,100,100 features in $\mathcal { D } _ { M } , \mathcal { D } _ { F M } , \mathcal { D } _ { G } , \mathcal { D } _ { C }$ respectively. The first set is used to demonstrate the effectiveness of our greedy algorithm when selecting participants given a fixed $m .$ . The second set of experiments is designed to highlight the adaptivity of VFLMG.

TABLE I DATASET DESCRIPTIONS 

<table><tr><td>Dataset</td><td>Size</td><td>Description</td></tr><tr><td> $\mathcal{D}_{M}$ </td><td>70000</td><td>MNIST dataset [26]</td></tr><tr><td> $\mathcal{D}_{FM}$ </td><td>70000</td><td>Fashion MNIST dataset [27]</td></tr><tr><td> $\mathcal{D}_{G}$ </td><td>7000×5000</td><td>Gisette dataset [28]</td></tr><tr><td> $\mathcal{D}_{C}$ </td><td>1440×1024</td><td>COIL20 dataset [29]</td></tr></table>

TABLE II   
PREDICTION PERFORMANCE WITH SMALL NUMBER OF FEATURES PER PARTICIPANT WITH FIXED m = 4 

<table><tr><td>Dataset</td><td>Full-fledged</td><td>Random</td><td>Lasso</td><td>VF-PS</td><td>VFLMG</td></tr><tr><td> $\mathcal{D}_{M}[10]^{1}$ </td><td>88.14±2.22</td><td>79.75±2.39</td><td>77.73±5.08</td><td>84.04±1.69</td><td>85.05±1.46</td></tr><tr><td> $\mathcal{D}_{FM}[10]$ </td><td>81.57±0.90</td><td>77.31±1.28</td><td>78.43±0.42</td><td>77.81±1.34</td><td>79.29±0.60</td></tr><tr><td> $\mathcal{D}_{G}[20]$ </td><td>89.88±1.06</td><td>84.03±1.84</td><td>81.32±3.54</td><td>88.65±1.89</td><td>88.53±1.81</td></tr><tr><td> $\mathcal{D}_{C}[10]$ </td><td>98.17±0.90</td><td>94.45±1.04</td><td>92.91±1.84</td><td>95.90±0.68</td><td>96.72±0.63</td></tr></table>

1 The number in parentheses represents the number of features per participant owns.

TABLE III PREDICTION PERFORMANCE WITH LARGE NUMBER OF FEATURES PER PARTICIPANT 

<table><tr><td>Dataset</td><td>Full-fledged</td><td>Random</td><td>Lasso</td><td>VF-PS</td><td>VFLMG</td></tr><tr><td> $\mathcal{D}_{M}[80]^{2}$ </td><td>96.61±0.20</td><td>95.69±0.08</td><td>95.64±0.34</td><td>95.95±0.33</td><td>95.41±0.26(3) $^{3}$ </td></tr><tr><td> $\mathcal{D}_{FM}[80]$ </td><td>86.98±0.10</td><td>86.05±0.22</td><td>86.00±0.25</td><td>85.95±0.32</td><td>85.69±0.22(3)</td></tr><tr><td> $\mathcal{D}_{G}[100]$ </td><td>90.81±0.90</td><td>88.58±0.71</td><td>89.15±1.77</td><td>89.11±1.32</td><td>88.48±1.26(3)</td></tr><tr><td> $\mathcal{D}_{C}[100]$ </td><td>99.25±0.42</td><td>98.75±0.48</td><td>98.80±0.23</td><td>98.55±1.16</td><td>97.27±1.20(2)</td></tr></table>

2 The number in parentheses represents the number of features per participant owns.   
3 The number in parentheses represents the number of selected passive parties using VFLMG.   
For other four baseline methods, a fixed number of 4 passive parties are selected for training.

2) VFL Models: We implement a vertical neural network model VFL-NN. During model training, we adopt the Adam optimizer, and set learning rate η = 0.003, batch size b = 100. We conduct VFL until a pre-specified test accuracy is reached, or a maximum number of iterations has elapsed.

3) Comparison Baselines: We compare VFLMG against four baselines following the setting [16]: 1) Full-fledged training: Here the all passive parties are involved in the joint training procedure. 2) RANDOM: We randomly choose a fixed m passive parties out of n − 1 to collaboratively train with the active party. 3) LASSO: We conduct the selection procedure by first training a Lasso model and choose m participants with the highest value of the sum of absolute coefficients. 4) VF-PS: We use mutual information and group testing to choose a fixed m participants with highest scores.

4) Metrics: Our method is primarily evaluated from two perspectives: test accuracy and communication overhead. The latter is quantified by calculating the total amount of encrypted data transmitted from the active party to other entities, such as passive parties and the aggregation server, during both the participant selection and training stages. To assess the acceleration achieved through sampling in JMI computation, we compare the total time required for calculations using the entire dataset against that using the sampled dataset and derive the speedup ratio.

# B. Evaluation Results

In terms of model performance, we compare the test accuracy of VFLMG with those of VF-PS under same communication and computational cost constraint. Additionally, we conduct an analysis to quantify the amount of saved communication cost achieved by VFLMG compared to fullfledged training and VF-PS, while maintaining a similar level of model performance. Finally, we demonstrated the reduction in communication overhead and time savings achieved through

![](images/a1d45a4e78fb839d627600b94bc292735605eb8e9775b9acf095e10ffa731ab9.jpg)



(a) Communication cost (GB) comparison between VFLMG and Full training, where VFLMG encounters at most 2.3% accuracy drop comapred to Full training.

![](images/25e215ae87c8c62c6fa40284962df2c09755e071553c65ded3eb8d48d65b0f1e.jpg)



(b) Communication cost (GB) comparison between VFLMG and VF-PS, where VFLMG encounters at most 1.3% accuracy drop comapred to VF-PS.   
Fig. 4. Compare communication cost (GB) with similar model performance

the utilization of our sampling strategy during the JMI calculation in the participant selection phase. In all experiments, we have a total of 9 participants consisting of 1 active party and 8 passive parties. We set the random seed = 0,1,2,3,4 and repeat the above experiments 5 times.

1) Selection Performance: In the first experimental setting, we fix the value of m to be 4 for both VFLMG and the other baseline methods. As shown in Table II, our proposed method almost consistently outperforms other baselines across all 4 datasets. Specifically, in the MNIST dataset, VFLMG outperforms random selection and VF-PS by 5.3% and 1.0% respectively. Moreover, VFLMG outperforms LASSO by 4.8% across all four datasets on average. These above observations illustrate the effectiveness of our proposed greedy method in selecting a group of participants that significantly enhances model performance when given a fixed value of m.

In the second case where each party owns a relatively large number of features, we utilize VFLMG to determine the required number of passive parties for collaborative training and also obtain the corresponding participant group. For the other three baseline methods, we also set the value of m to be 4. As shown in Table III, the model performances of all three baselines with 4 passive parties exhibit minimal degradation compared to full-fledged training. This is attributed to the fact that each participant already possesses an adequate number of features, rendering the inclusion of additional participants less impactful in terms of performance gain. VFLMG dynamically selects 3,3,3,2 participants from the total of 8 participants in $\mathcal { D } _ { M }$ , $\mathcal { D } _ { F M }$ , $\mathcal { D } _ { G }$ and $\mathcal { D } _ { C }$ respectively, and consistently maintains a high level of accuracy across all four datasets, with a maximum accuracy drop of only 2.3% compared to full-fledged training while achieving substantial communication overhead savings, reaching up to 72.1%. In specific datasets, $e . g .$ , MNIST and Fashion MNIST datasets, VFLMG reduces communication costs by 51.4% and 56.7% respectively, while experiencing an accuracy drop of just 1.2% and 1.3%. Additionally, in comparison to VF-PS, VFLMG saves communication cost by up to 47.4%, while maintaining a maximum accuracy drop of 1.3%. Specifically, in the MNIST and Fashion MNIST datasets, VFLMG reduces communication costs by 32.1% and 27.6% respectively, with an accuracy drop of 0.5% and 0.3%.

TABLE IV COMMUNICATION OVERHEAD (GB) COMPARISON WHEN COMPUTING JMI 

<table><tr><td>Dataset</td><td>VF-PS</td><td>Ours</td><td>Savings in overhead</td></tr><tr><td> $\mathcal{D}_{M}$ </td><td>538.8</td><td>233.7</td><td>56.6%</td></tr><tr><td> $\mathcal{D}_{FM}$ </td><td>178.7</td><td>79.9</td><td>55.3%</td></tr></table>

TABLE V COMPUTATION TIME (S) COMPARISON WHEN COMPUTING JMI IN $\mathcal { D } _ { M }$ 

<table><tr><td># of participants</td><td>VF-PS</td><td>Ours</td><td>speedup</td></tr><tr><td>2</td><td> $29.46 \pm 4.27$ </td><td> $8.02 \pm 0.96$ </td><td> $3.67 \times$ </td></tr><tr><td>3</td><td> $62.29 \pm 8.36$ </td><td> $17.74 \pm 2.00$ </td><td> $3.51 \times$ </td></tr><tr><td>4</td><td> $119.45 \pm 13.62$ </td><td> $29.72 \pm 2.71$ </td><td> $4.02 \times$ </td></tr><tr><td>5</td><td> $224.40 \pm 44.53$ </td><td> $45.41 \pm 7.21$ </td><td> $5.04 \times$ </td></tr></table>

2) Sampling Performance: During JMI computation, the communication overhead primarily comes from the transmission of encrypted partial distances between active party and the aggregation server, which is proportional to $N ^ { 2 } .$ The time complexity for computation is $O ( N ^ { 2 } \log N )$ . By employing the sampling approach, we expect to achieve significant savings in both communication overhead and computation time. In both $\mathcal { D } _ { M }$ and $\mathcal { D } _ { F M }$ , we randomly sample 23,000 instances from the training set to conduct JMI computation, which leads to a communication cost savings of 56.6% for the MNIST dataset and 55.3% for the Fashion MNIST dataset, as shown in Table IV. Moreover, from Table V, we observe that the sampling method achieves an approximate 3.5× to 5× speedup in JMI computation for the MNIST datasets while maintaining high accuracy in the JMI results.

# VI. CONCLUSION

In this work, we focus on participant selection in vertical federated learning. We find that as the number of participants increases in VFL, the communication overhead experiences a significant rise, while the improvement of the predictive capability of the model is negligible. Therefore, we propose VFLMG to dynamically select an unfixed number of participants before training, ensuring a better balance between model performance and communication overhead. The selection process is efficient and secure, and does not introduce extra privacy concerns compared to the traditional VFL setting. Evaluations on various datasets show that the proposed method achieves a notable reduction in communication cost with little accuracy degradation compared to strong baselines.

# VII. ACKNOWLEDGEMENT

Lan Zhang is the corresponding author. This research was supported by the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, ”the Fundamental Research Funds for the Central Universities” WK2150110024, the University Synergy Innovation Program of Anhui Province under Grant GXXT-2022-049.

# REFERENCES

[1] Q. Yang, Y. Liu, T. Chen, and Y. Tong, “Federated machine learning: Concept and applications,” ACM Transactions on Intelligent Systems and Technology (TIST), vol. 10, no. 2, pp. 1–19, 2019.   
[2] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-efficient learning of deep networks from decentralized data,” in Artificial intelligence and statistics. PMLR, 2017, pp. 1273– 1282.   
[3] A. Li, L. Zhang, J. Tan, Y. Qin, J. Wang, and X.-Y. Li, “Sample-level data selection for federated learning,” in IEEE INFOCOM 2021-IEEE Conference on Computer Communications. IEEE, 2021, pp. 1–10.   
[4] A. Li, L. Zhang, J. Wang, F. Han, and X.-Y. Li, “Privacy-preserving efficient federated-learning model debugging,” IEEE Transactions on Parallel and Distributed Systems, vol. 33, no. 10, pp. 2291–2303, 2021.   
[5] A. Li, L. Zhang, J. Wang, J. Tan, F. Han, Y. Qin, N. M. Freris, and X.-Y. Li, “Efficient federated-learning model debugging,” in 2021 IEEE 37th International Conference on Data Engineering (ICDE). IEEE, 2021, pp. 372–383.   
[6] J. Wang, L. Zhang, A. Li, X. You, and H. Cheng, “Efficient participant contribution evaluation for horizontal and vertical federated learning,” in 2022 IEEE 38th International Conference on Data Engineering (ICDE). IEEE, 2022, pp. 911–923.   
[7] T. Chen, X. Jin, Y. Sun, and W. Yin, “Vafl: a method of vertical asynchronous federated learning,” arXiv preprint arXiv:2007.06081, 2020.   
[8] Y. Wu, S. Cai, X. Xiao, G. Chen, and B. C. Ooi, “Privacy preserving vertical federated learning for tree-based models,” arXiv preprint arXiv:2008.06170, 2020.   
[9] S. Feng and H. Yu, “Multi-participant multi-class vertical federated learning,” arXiv preprint arXiv:2001.11154, 2020.   
[10] J. Wang, L. Zhang, Y. Cheng, S. Li, H. Zhang, D. Huang, and X. Lan, “Tvfl: Tunable vertical federated learning towards communicationefficient model serving,” in IEEE INFOCOM 2023-IEEE Conference on Computer Communications. IEEE, 2023.   
[11] A. Li, H. Peng, L. Zhang, J. Huang, Q. Guo, H. Yu, and Y. Liu, “Fedsdgfs: Efficient and secure feature selection for vertical federated learning,” arXiv preprint arXiv:2302.10417, 2023.   
[12] Y. Fraboni, R. Vidal, L. Kameni, and M. Lorenzi, “Clustered sampling: Low-variance and improved representativity for clients selection in federated learning,” in International Conference on Machine Learning. PMLR, 2021, pp. 3407–3416.   
[13] R. Balakrishnan, T. Li, T. Zhou, N. Himayat, V. Smith, and J. Bilmes, “Diverse client selection for federated learning via submodular maximization,” in International Conference on Learning Representations, 2022.

[14] F. Lai, X. Zhu, H. V. Madhyastha, and M. Chowdhury, “Oort: Efficient federated learning via guided participant selection,” in 15th {USENIX} Symposium on Operating Systems Design and Implementation ({OSDI} 21), 2021, pp. 19–35.   
[15] Z. Liu, Y. Chen, Y. Zhao, H. Yu, Y. Liu, R. Bao, J. Jiang, Z. Nie, Q. Xu, and Q. Yang, “Contribution-aware federated learning for smart healthcare,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 36, no. 11, 2022, pp. 12 396–12 404.   
[16] J. Jiang, L. Burkhalter, F. Fu, B. Ding, B. Du, A. Hithnawi, B. Li, and C. Zhang, “Vf-ps: How to select important participants in vertical federated learning, efficiently and securely?” Advances in Neural Information Processing Systems, vol. 35, pp. 2088–2101, 2022.   
[17] L. Wang, Q. Pang, S. Wang, and D. Song, “Fed-χ2: Privacy preserving federated correlation test,” arXiv preprint arXiv:2105.14618, 2021.   
[18] T. Huang, W. Lin, W. Wu, L. He, K. Li, and A. Y. Zomaya, “An efficiency-boosting client selection scheme for federated learning with fairness guarantee,” IEEE Transactions on Parallel and Distributed Systems, vol. 32, no. 7, pp. 1552–1564, 2020.   
[19] T. Huang, W. Lin, L. Shen, K. Li, and A. Y. Zomaya, “Stochastic client selection for federated learning with volatile clients,” IEEE Internet of Things Journal, vol. 9, no. 20, pp. 20 055–20 070, 2022.   
[20] I. Guyon, S. Gunn, M. Nikravesh, and L. A. Zadeh, Feature extraction: foundations and applications. Springer, 2008, vol. 207.   
[21] D. D. Lewis, “Feature selection and feature extraction for text categorization,” in Speech and Natural Language: Proceedings of a Workshop Held at Harriman, New York, February 23-26, 1992, 1992.   
[22] W. Gao, S. Kannan, S. Oh, and P. Viswanath, “Estimating mutual information for discrete-continuous mixtures,” Advances in neural information processing systems, vol. 30, 2017.   
[23] R. Fagin, A. Lotem, and M. Naor, “Optimal aggregation algorithms for middleware,” in Proceedings of the twentieth ACM SIGMOD-SIGACT-SIGART symposium on Principles of database systems, 2001, pp. 102– 113.   
[24] A. Krause, A. Singh, and C. Guestrin, “Near-optimal sensor placements in gaussian processes: Theory, efficient algorithms and empirical studies.” Journal of Machine Learning Research, vol. 9, no. 2, 2008.   
[25] P. Mohassel and Y. Zhang, “Secureml: A system for scalable privacypreserving machine learning,” in 2017 IEEE symposium on security and privacy (SP). IEEE, 2017, pp. 19–38.   
[26] Y. LeCun, “The mnist database,” http://yann.lecun.com/exdb/mnist/.   
[27] H. Xiao, K. Rasul, and R. Vollgraf. (2017) Fashion-mnist: a novel image dataset for benchmarking machine learning algorithms.   
[28] U. machine learning repository, “Handwritten digit recognition problem,” https://archive.ics.uci.edu/ml/datasets/Gisette.   
[29] C. University, “Image classification task,” https://www.cs.columbia.edu/CAVE/software/softlib/coil-20.php.