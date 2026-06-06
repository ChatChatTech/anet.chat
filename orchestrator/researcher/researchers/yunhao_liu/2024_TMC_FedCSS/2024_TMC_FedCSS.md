# Joint Client-and-Sample Selection for Federated Learning via Bi-level Optimization

Anran Li, Guangjing Wang, Ming Hu, Jianfei Sun, Lan Zhang, Luu Anh Tuan, Han Yu

Abstract—Federated Learning (FL) enables massive local data owners to collaboratively train a deep learning model without disclosing their private data. The importance of local data samples from various data owners to FL models varies widely. This is exacerbated by the presence of noisy data that exhibit large losses similar to important (hard) samples. Currently, there lacks an FL approach that can effectively distinguish hard samples (which are beneficial) from noisy samples (which are harmful). To bridge this gap, we propose the joint Federated Meta-Weighting based Client and Sample Selection (FedMW-CSS) approach to simultaneously mitigate label noise and hard sample selection. It is a bilevel optimization approach for FL client-and-sample selection and global model construction to achieve hard sample-aware noise-robust learning in a privacy preserving manner. It performs meta-learning based online approximation to iteratively update global FL models, select the most positively influential samples and deal with training data noise. To utilize both the instance-level information and class-level information for better performance improvements, FedMW-CSS efficiently learns a class-level weight by manipulating gradients at the class level, e.g., it performs a gradient descent step on class-level weights, which only relies on intermediate gradients. Theoretically, we analyze the privacy guarantees and convergence of FedMW-CSS. Extensive experiments comparison against eight state-of-the-art baselines on six real-world datasets in the presence of data noise and heterogeneity shows that FedMW-CSS achieves up to 28.5% higher test accuracy, while saving communication and computation costs by at least 49.3% and 1.2%, respectively.

Index Terms—Sample selection, federated learning, noisy data detection, bi-level optimization

# 1 INTRODUCTION

F EDERATED Learning (FL) is an emerging learningparadigm that performs distributed training of models on data owners, a.k.a. FL clients with potentially sensitive local data [1], [2], [3], [4]. A large number of data owners collaboratively train a global model by aggregating their local models without exposing their data to any third party. It has been widely adopted in various applications such as safety monitoring [5], [6] and clinical decision support model for COVID-19 [7]. However, due to the complexity of the algorithm, resource overhead incurred by data owners (e.g., local computation and communication cost) has become a bottleneck hindering the training of large-scale FL models. During FL training process, it is observed that not all local samples are equally important [8], [9], [10]. On one hand, knowledge embedded within some samples has been extracted after multiple training epochs. These samples can then be disregarded without affecting the global model. On the other hand, many participants may hold erroneous data (e.g., data with label noise), leading to a detrimental effect on the performance of the global model [11], [12]. Such data samples should be excluded from training.

In this work, we focus on identifying the most positively

Anran Li is with the Department of Biomedical Informatics and Data Science, School of Medicine at Yale University. E-mail: {anran.li@yale.edu}.   
Guangjing Wang is with the Department of Computer Science and Engineering, University of South Florida. E-mail: wanggu22@msu.edu.   
Ming Hu and Jianfei Sun are with the Singapore Management University, Singapore. E-mail: sjf215.uestc@gmail.com.   
Luu Anh Tuan and Han Yu are with the School of Computer Science and Engineering of Nanyang Technological University, Singapore. E-mail: {anhtuan.luu, han.yu}@ntu.edu.sg.   
• Lan Zhang is with the School of Computer Science and Technology of University of Science and Technology of China, China. E-mail: zhanglan@ustc.edu.cn.

influential clients and the most influential samples within these clients so that the usage of limited computation and communication resources can be optimized to achieve fast convergence and obtain good FL model accuracy. Existing works utilize client selection [13], [14] or sample-level data selection [15], [16] either through Shapley values [17], [18] or through diverse statistical selection metrics such as differences of model weight updates [19], [20] or training losses [14]. However, these approaches have the following limitations. Firstly, methods based on Shapley values are extremely computationally expensive, making them difficult to scale in practical federated settings. Secondly, techniques based on statistical metrics either ignore the presence of label noise, or simply employ hand-designed loss or gradient norm thresholds to filter out noisy clients or samples. Nevertheless, prior knowledge of the thresholds for distinguishing noisy samples from non-noisy ones for various models training on different datasets is not available in practice, which renders these methods inapplicable. Moreover, these techniques cannot be applied to distinguish positively influential clients and local samples from noisy ones. This is because to mitigate noisy labels, models often favor samples with small training losses as they are more likely to be clean data. Conversely, when attempting to identify positively influential samples, models prioritize those with high training losses, as they induce large changes in model parameters, thereby accelerating convergence.

To address these limitations, we propose a novel clientsample bilevel selection scheme - the federated metaweighting based client and sample selection (FedMW-CSS) approach. It accelerates the training of FL models by focusing the limited computation and communication resources on the most positively influential samples, while dealing with label noise. To learn general forms of training set noise and positively influential samples, FedMW-CSS leverages a small clean validation to guide FL training, which is not uncommon in practical FL scenarios [12], [21]. It jointly solves the sample selection problem and global FL model construction problem as a bilevel optimization problem: the inner objective aims to contruct the optimal global FL model, while the outer objective aims to learn the optimal selection probabilities for data samples. Our key contributions are summarized as follows.

• We propose FedMW-CSS to accomplish joint clientand-sample selection to accelerate global model training and prediction accuracy by selecting the most positively influential samples and dealing with label noise. The proposed solution enables efficient and privacy-preserving identification of most positively influential samples through a hierarchical influence estimation based on bilevel optimization.

• We firstly formulate the sample selection and global model construction as a bilevel optimization problem. We propose a meta-weight learning for bilevel FL optimization method based on approximating differentiation through online first-order approximation over few communication rounds. It achieves highly efficient sample selection probability estimation by bypassing expensive global Hessian computations through the inner loop learning process. We leverage differential private (DP) mechanism on FedMW-CSS to prevent the transmission parameters from leaking clients’ data information. Theoretical analysis illustrate that FedMW-CSS converges to the globally optimal model in a privacy-preserving manner.

• Compared with our previous conference version [22], we further explore a class-level weighting and selecting mechanism through the gradient manipulation to utilize both the class-level and instance-level information for better hard sample-aware noise robust federated training. To obtain class-level weights efficiently, we manipulate intermediate gradients to update class-level weights via a gradient descent step without introducing any extra computational cost during bilevel optimization. Besides, we propose a client weight perturbation approach for FedMW-CSS to achieve differential privacy for local training data. In these ways, FedMW-CSS privately determine the selected clients and samples and produces an optimal global model with higher accuracy and fast convergence.

• We evaluate FedMW-CSS via extensive experiments across various FL tasks using six datasets with real-world workloads. The experiment results show that compared to the nine state-of-the-art approaches, FedMW-CSS can efficiently handle various data distribution across thousands of data owners. It improves test accuracy by 1.2%-26.4%, while incurring 41.5%-93.3% lower computation cost and 1.2%- 79.6% lower communication cost, thereby achieving the best efficiency and accuracy in the presence of data noise.

# 2 RELATED WORK

# 2.1 Sample selection in centralized learning

There are two main categories of sample selection methods for centralized learning. The first one focuses on the dynamic selection of hard samples that are important to the model to form a training batch so as to accelerate the training and improve inference accuracy. Approaches based on curriculum learning (CL) [23], [24] attempt to train a model with easier samples in early training stages and gradually using more difficult training samples in later training stages. However, since CL requires a reference model to determine the hardness of samples, which is not readily available in FL scenarios and makes it difficult to apply. Importance sampling methods [9], [25], [26] have been proposed to prioritize samples that can induce significant changes in the parameters which reduce the variance of the gradient estimates. These methods employ either the gradient norm or the loss to compute the importance of each sample. However, these methods either overlook the existence of data noise, or select samples with high training losses without distinguishing whether they are hard samples or noisy ones. The second category mitigates data noise via data resampling or generally by reweighting every instance and minimizing a weighted training loss [27]. They estimate pseudo labels for noisy instances with a meta set, and treat labels as learnable parameters. Although these methods can tackle label noise, they introduce huge amounts of learnable parameters and thus cannot scale to large datasets.

There are few works dealing with the identification of hard samples and noise data simultaneously [28], [29]. They generally leverage an auxiliary teacher deep network to supervise the training of a student network by focusing on probably correct samples. However, they are not applicable to FL due to the following problems. Firstly, the auxiliary network suffers from cumulative errors due to sample selection bias [30]. Secondly, they require direct access to all training samples which violates the privacy preservation requirements of FL. In addition, training the large extra auxiliary network incurs significant computation and communication overhead, rendering its applications in in resource constrained FL devices.

# 2.2 Client and Sample Selection in FL

FL Client Selection. Existing FL client selection methods can be divided into two branches. One branch utilizes the client contribution evaluation results [17], [18], e.g., calculated through Shapley values, to select clients and optimize the global model aggregation. However, since Shapley value-based methods account for complex dependencies, they are prohibitively expensive to calculate and scale in real FL applications. The other branch introduces diverse statistical selection metrics such as differences of model updates [19], [20], [31], local losses [14] or utilities [13] calculated on local losses, and measure the metric values of clients to make selections. However, these methods treat all samples from a selected client as equally significant and thus lead to a waste of communication and computation resources when updating local models on unimportant samples, resulting in suboptimal model performance.

FL Sample-level Selection. As for sample-level data selection in FL, one category [21], [32], [33] proposes to distributedly select relevant data before FL training based on a benchmark model, without considering dynamic data importance during training. The other category dynamically selects samples to compose local batch during training.

TABLE 1 Motivation for class-level weighting and selection. 

<table><tr><td>Gradient flow information</td><td>‘not cat’</td><td>‘dog’</td><td>‘not bird’</td></tr><tr><td>Instance weighting</td><td colspan="3">0.4</td></tr><tr><td>Class-level weighting</td><td>0.2</td><td>0.4</td><td>0.62</td></tr></table>

The work [15] prioritizes local samples with high importance using gradient norm upper bound to achieve fast convergence speed. Another work [16] proposes a deadline control strategy for FL that predicts the deadline for each round with different client training data. These methods, however, either ignore noise data, or simply use pre-defined thresholds to filter out noisy clients or samples. However, in practical FL systems, there is no prior knowledge about the thresholds for different datasets training on different models, which makes them inapplicable.

Further, our recent instance-level weighting method, FedCSS [22], attempts to simultaneously solve the problem of identification of noisy samples and hard samples. However, it cannot fully utilize class-level information within each instance, resulting in the potential loss of useful information. For example, in a three-class (‘cat’, ‘dog’, ‘bird’) classification task, every instance has three logits. As shown in Table 1, every logit corresponds to a class-level gradient flow which stems from the loss function and backward propagation. These gradient flows represent three kinds of information: ‘not cat’, ‘dog’, and ‘not bird’. FedCSS alleviates label noise by down-weighting all the gradient flows of the instance while discarding three kinds of information simultaneously. However, down-weighting the ‘not bird’ gradient flow is a waste of information. Similarly, in hardsample selection scenarios, different gradient flows represent different class-level information. Consequently, these issues inspire us to design a hard sample-aware noiserobust FL approach to efficiently and privately train highperformance models taking both class-level and instancelevel information for reweighting and sample selection in the presence of training set noise.

# 3 PROBLEM DESCRIPTIONS

# 3.1 Basics of Federated Learning

Let there be K FL clients $\{ 1 , 2 , \cdots , K \}$ each $k \in [ K ]$ holding a local dataset $D _ { k } \ = \ \{ z _ { k , 1 } , z _ { k , 2 } , \cdot \cdot \cdot , z _ { k , n _ { k } } \}$ , consisting of $n _ { k }$ data samples, where $z _ { k , i } ~ = ~ ( x _ { k , i } , y _ { k , i } ) \in \mathcal { X } \times \mathcal { V } \left[ 3 4 \right]$ $\begin{array} { r } { N = \sum _ { k = 1 } ^ { K } \widehat { n } _ { k } } \end{array}$ is the total number of all clients’ samples, and the number of classes is denoted as C. The goal of a standard federated optimization problem is to find:

$$
\theta^ {*} = \arg \min _ {\theta} \sum_ {k = 1} ^ {K} \frac {n _ {k}}{N} L _ {k} (\theta), \text { where } L _ {k} (\theta) = \frac {1}{n _ {k}} \sum_ {i = 1} ^ {n _ {k}} l (z _ {k, i}; \theta), \tag {1}
$$

where $l ( z _ { k , i } ; \cdot ) , L _ { k } ( \cdot )$ represent loss functions of an individual sample $z _ { k , i } ,$ and of a client k on its local model, respectively. This optimization problem can be solved via iterative stochastic optimization, $e . g . ,$ , stochastic gradient decent (SGD). In the t-th iteration, given the fraction ϕ of FL clients to be selected, the FL server S randomly selects a subset $U _ { t }$ of $\begin{array} { r } { u = \operatorname* { m a x } \{ \vert \phi \cdot K \vert , 1 \} } \end{array}$ clients and distributes the parameters of the current model $\theta _ { t }$ to them. Each selected client $k \in U _ { t }$ trains a local model $\theta _ { t + 1 } ^ { k } = \theta _ { t } - \eta _ { k } \nabla L _ { k } ( \theta _ { t } )$ with learning rate $\eta _ { k } ,$ , and sends $\theta _ { t + 1 } ^ { k }$ to the FL server. The server aggregates the received updates from the selected clients and updates the global FL model as $\begin{array} { r } { \theta _ { t + 1 } = \frac { 1 } { u } \sum _ { k \in U _ { t } } \theta _ { t + 1 } ^ { k } } \end{array}$ . This process is repeated until the global FL model converges $( i . e . ,$ a convergence criterion is met). Then, the global FL model $\theta ^ { * }$ is obtained.

# 3.2 Problem Formulation

There are two types of entities involved in a typical FL scenario: an FL server $S ,$ and K distributed clients $\{ 1 , 2 , \cdots , K \}$ . Each client k possesses a local dataset $D _ { k }$ . Under the coordination of the server, all clients collaboratively train a global model $\theta ^ { * } \in \mathbb { R } ^ { d }$ by sharing their local models updated by their private datasets. Our goal is to construct high-performance FL models in the presence of noisy training data $( e . g .$ , data noises, or data heterogeneity) which can lead to slow convergence speed and reduced prediction accuracy. Specifically, we aim to enable FL participants to collaboratively select the most positively influential samples for model training, while solving training set noise problems by eliminating negatively influential samples. The goal of client-sample selection in FL is to dynamically select a subset of clients and their individual samples, and construct an optimal global model $\theta ^ { * }$ based on the selected clients and samples. The selection of samples and clients, and choice of global parameters can be evaluated by minimizing the following risk:

$$
\theta^ {*} (P, p) = \arg \min _ {\theta} \mathbb {E} _ {k \sim P _ {k}} \mathbb {E} _ {z _ {k, i} \sim p _ {k, i}} [ l (z _ {k, i}; \theta) ], \tag {2}
$$

where $0 ~ \le ~ P _ { k } , p _ { k , i } ~ \le ~ 1 , k ~ \in ~ [ K ]$ are the probabilities that client k and the i-th sample of client k are selected. We assume that all FL participants are semi-honest, $e . g .$ , they follow the protocol of FL and client-sample selection faithfully, but may be curious about others’ private data.

# 4 THE PROPOSED FEDCSS APPROACH

# 4.1 Sample Selection via FL Bilevel Learning

Firstly, to achieve accurate client selection and sample selection while simultaneously training the global FL model in the presence of training set noise, we need to dynamically quantify the influences of clients and samples on the global FL model during training, and increase the sampling probabilities for highly influential clients and their highly influential samples. Thus, we formulate the objective (Eq. (2)) into a bilevel optimization problem, with learning the optimal selection probabilities $\hat { P } ^ { * } , p ^ { * }$ as the outer problem and the optimal global FL model $\theta ^ { * }$ as the inner problem. Specifically, assume that there is a small clean validation set $\begin{array} { r } { \hat { D _ { v } } = \{ z _ { i } ^ { \bar { v } } = ( x _ { i } ^ { v } , y _ { i } ^ { v } ) \in \mathcal { X } \times \mathcal { Y } \} , i \in [ M ] . } \end{array}$ , and $M \ll N ,$ stored at the FL server. Then, the objective in $\operatorname { E q . } \left( 2 \right)$ can be re-expressed as:

$$
\theta^ {*} (P, p) = \arg \min _ {\theta} \sum_ {k = 1} ^ {K} \frac {n _ {k}}{N} P _ {k} L _ {k} (\theta), \tag {3}
$$

$$
\text { where } L _ {k} (\theta) = \frac {1}{n _ {k}} \sum_ {i = 1} ^ {n _ {k}} p _ {k, i} l (z _ {k, i}; \theta),
$$

with P and p being unknown at beginning. The optimal selection of P and p are calculated based on the performance of the model on the validation set with the objective:

$$
P ^ {*}, p ^ {*} = \arg \min _ {P, p} \frac {1}{M} \sum_ {i = 1} ^ {M} l (z _ {i} ^ {v}; \theta^ {*} (P, p)), \tag {4}
$$

where $l ( z _ { i } ^ { v } ; \cdot )$ is the loss function of the validation sample $z _ { i } ^ { v }$ . However, calculating the optimal $P ^ { * } , p ^ { * }$ and $\theta ^ { * }$ requires two nested optimizations, and each can be prohibitively resource intensive, especially for large-scale FL systems and resourceconstrained FL clients. The motivation of our approach is to adapt online probabilities $P , p$ through a single optimization loop. That is, for each training iteration, we inspect the descent direction of some clients and their training examples locally on the training loss surface and reweight them according to their similarity to the descent direction of the validation loss surface. Thus, each iteration involves computing the gradients $\nabla _ { P } l ( z _ { i } ^ { v } ; \theta ( P , p ) ) , \nabla _ { p } l ( z _ { i } ^ { v } ; \theta ( P , p ) ) , i \in$ [M ]. Taking the calculation of the gradient $\nabla _ { p } l \big ( z _ { i } ^ { v } ; \theta ( P , p ) \big )$ of the validation loss w.r.t. the probability p as an example:

$$
\nabla_ {p} l (z _ {i} ^ {v}; \theta (P, p)) = \nabla_ {\theta} l (z _ {i} ^ {v}; \theta (P, p)) ^ {\top} \nabla_ {p} \theta (P, p), \tag {5}
$$

where $\nabla _ { p } \theta ( P , p )$ is a $d \times N { \mathrm { - s i z e } }$ Jacobian matrix with $\theta \in$ $\mathbb { R } ^ { d } , \ p \in \mathrm { ~ \bar { \mathbb { R } } ^ { \dot { N } } ~ }$ . The second term $\nabla _ { p } \theta ( P , p )$ in Eq. 5 can be derived through the implicit differentiation method [35], as illustrated below,

$$
\nabla_ {p} \theta (P, p) = - P _ {k} \nabla_ {\theta} l (z _ {k, i}; \theta) \cdot \left(\frac {1}{K} \sum_ {i = 1} ^ {K} H _ {k}\right) ^ {- 1}, \tag {6}
$$

where Hk = ∇2θ 1nk $\begin{array} { r } { H _ { k } = \nabla _ { \theta } ^ { 2 } \frac { 1 } { n _ { \ast } } \sum _ { i = 1 } ^ { n _ { k } } l ( z _ { k , i } ; \theta ) } \end{array}$ is the Hessian matrix of client $k \in [ K ]$ . The gradient $\nabla _ { P } l ( z _ { i } ^ { v } ; \theta ( P , p ) ) , i \in [ M ]$ can be calculated in a similar way.

# 4.2 System Design Motivations

The online approximation method for bilevel FL optimization (Eq. (5)) enables us to learn the selection probabilities of all clients and their local training samples so as to construct the optimal global model. However, there are many challenges in solving this optimization problem. Firstly, evaluating Eq. (6) requires forming and inverting the client Hessian matrices, which requires $\check { O (} N d ^ { 2 } + d ^ { 3 } )$ computational operations [12], [36] with N denoting the total number of training samples and $\boldsymbol { \theta } \in \mathbb { R } ^ { d }$ . Secondly, it also requires all clients to upload $H _ { k } , k \in [ K ]$ to the FL server, which incurs $O ( K d ^ { 2 } )$ communication costs. Considering the large N, d typically involved in training deep FL models, the calculation of Eq. (5) incurs unacceptable computation and communication overhead. One similar work [37] in the bilevel optimization literature use implicit Hessian-vector products (HVPs) to approximate $\begin{array} { r } { \big ( \frac { 1 } { K } \dot { \sum _ { i = 1 } ^ { K } } H _ { k } \big ) ^ { - 1 } \nabla _ { \theta } l _ { i } ^ { v } \big ( \theta ^ { * } ( \dot { P _ { , } } p ) \big ) } \end{array}$ ). However, with both outer functions and inner functions to learn in [37], clients would cost prohibitively high computation cost, $e . g . , O ( K d )$ operations, and more communication cost, e.g., $O ( N d )$ parameters per training round as it requires transferring matrix-vector products for all of the training data at each FL training round. Thirdly, as illustrated in Table 1, a scalar weight for every instance cannot capture classlevel information for reweighting and sample selection. A class-level weights for different gradient flows is desired for better hard sample-aware noise-robust federated training.

![](images/297c792c278debd325a56d317a5a9eeda60787e9a8cf8c650d0ac395557f0775.jpg)



Fig. 1. System overview of FedMW-CSS. Notations: ⃝1 meta model ϵt and global model validation data and ⃝4 $\theta _ { t } , \mathbf { \Omega } ( 2 )$ local modemeta model $\theta _ { t + 1 } ^ { k } , \circledast$ average gradient of $\boldsymbol { \epsilon } _ { t + 1 } ^ { k }$

To this end, we design our system, FedMW-CSS, with the following two approaches:

(1) Replacing 2nd-Order Calculations with 1st-Order Gradient-based Approximation. FedMW-CSS leverages meta-learning based online approximation for FL bilevel optimization to iteratively update selection probabilities and the global FL model. In this way, the optimization can be efficiently conducted in conjunction with gradient approximation, thus avoiding expensive calculations of 2nd-order Hessian matrices.

(2) Reducing Unnecessary Influence Computation via Hierarchical Analysis. To calculate the selection probabilities of the data samples, each FL client needs to upload the gradients of all its samples to the FL server, which incurs $O ( N d )$ communication overhead. To improve efficiency and preserve privacy, we design a hierarchical selection approach. It first identifies positively influential FL clients. Then, it only requires these clients to update sample influences with the meta network by using the class-level weights generated by gradient manipulation, and select positively influential local samples to update the local models. In this way, FedMW-CSS only needs to transfer the gradient of the validation data, the meta model, and client influence scores. The communication overhead is reduced to $O ( d + d ^ { \prime } + 1 )$ , where d′ ≪ d is the size of the meta model.

# 4.3 System Overview

The overall architecture of FedMW-CSS is shown in Fig. 1. It consists of two main steps.

1) Hierarchical Influence Estimation and Sample Selection. In each training iteration t, given the selection probabilities of FL clients, the FL server first selects a batch of clients to update their sample influences and participate in FL training. Each selected client updates the influence scores of its samples with the meta model based on the similarities between the descent direction of sample’s loss surface and the validation loss surface, as well as the gradient flow manipulation. These influence scores are summed up and the average is taken as the influence score of the client. The clients then select their most positively influential local data samples to be used for FL model training.

2) Influence-based Model Updating. With the influence estimation and client-and-sample selection results, each selected client updates its local model and sends the updated meta model, client weight (i.e., client influence score) and updated local model to the FL server. The server then aggregates these local models to obtain the global FL model and updates client selection probabilities.

# 4.4 Algorithm Overview

Joint Client and Sample Selection. The proposed FedMW-CSS approach is illustrated in Algorithm 1. Specifically, the FL server initializes a global model $\theta _ { 0 }$ and a meta model $\epsilon _ { \mathrm { 0 } } .$ The K clients and their local samples start with the same initial selection probability $\begin{array} { r }  P _ { 0 } ^ { k } = \frac { 1 } { K } , p _ { 0 } ^ { k , i } = \frac { 1 } { n _ { k } } , k \in \frac { } \end{array}$ nk $[ K ] , i \in [ n _ { k } ]$ . In the t-th iteration, the server calculates the intermediate gradients $g _ { t } ^ { k }$ of validation loss w.r.t. weights $\tau _ { k , i } ,$ selects u clients (forming a selected client set $U _ { t } )$ according to their selection probabilities $\{ P _ { t } ^ { 1 } , \cdots , P _ { t } ^ { K } \}$ and distributes the global model $\theta _ { t }$ and meta model $\epsilon _ { t }$ to them (Line 4-7). Each selected client $k \ \in \ U _ { t }$ then updates its sample selection probabilities and local model as follows. Firstly, it updates the sample weight $w _ { t } ^ { k , i }$ through wk,it = $e ( l ( z _ { k , i } ; \theta _ { t } ) , \bar { \epsilon } _ { t } )$ for sample $z _ { k , i } ,$ and calculates probability distribution {pt , pt , $\{ p _ { t } ^ { k , 1 } , p _ { t } ^ { k , 2 } , \dot { \cdot } \cdot \cdot , p _ { t } ^ { k , n _ { k } } \}$ k,1 k,2 pk,nkt } for all its samples (Line 14-16). Then, client k selects a batch $B _ { k }$ of samples with the probability distribution and updates the local model over

Algorithm 1: FedMW-CSS   
Input : Initial selection probability $P_{0}^{k} = \frac{1}{K}$ , $p_{0}^{k} = \frac{1}{n_{k}}$ , $k \in [K]$ , $i \in [n_{k}]$ , validation set $D_{v}$ Output: The optimal global model $\theta^{*}$ 1 // At the FL Server:

2 Initialize global model $\theta_{0}$ , meta model $\epsilon_{0}$ ;

3 for each round $t \in \{0, 1, \cdots, T\}$ do

4 $U_{t} \leftarrow \text{select } u \text{ clients } k \sim P_{t}$ ;

5 $g_{t}^{k} = \frac{1}{b} \sum_{i=1}^{b} \nabla_{\tau_{k,i}} l(z_{i}^{v}; \theta_{t}(\epsilon_{t}))$ ;

6 for each client $k \in U_{t}$ do

7 $\theta_{t+1}^{k}, W_{t+1}^{k} \leftarrow \text{LocalUpdate}(k, \theta_{t}, \epsilon_{t}, g_{t}^{k})$ ;

8 $\theta_{t+1} = \frac{1}{u} \sum_{k \in U_{t}} \theta_{t+1}^{k}$ ; // update global model

9 $P_{t+1}^{k} = \frac{W_{t+1}^{k}}{\sum_{k=1}^{K} W_{t+1}^{k}}, \forall k \in [K]$ ; // Update probability

10 $g_{t}^{v} = \eta \frac{1}{b} \sum_{i=1}^{b} \frac{\partial l(z_{i}^{v}); \theta_{t}}{\partial \theta}$ ;

11 $\epsilon_{t+1} \leftarrow \text{LocalMeta}(k, g_{t}^{v})$ ; // Update meta model

12 // At FL Client $k \in [K]$ :

13 Function LocalUpdate ( $k, \theta_{t}, \epsilon_{t}, g_{t}^{k}$ ):
14 $\theta_{t}^{k,0} = \theta_{t}, \tau_{k,i}^{rt} = \tau_{k,i}^{t} - \eta_{\tau} \frac{g_{t}^{k}}{| |g_{t}^{k}| | _{1}}$ ;

15 $w_{t}^{k,i} = e(l(z_{k,i}; \theta_{t}), \epsilon_{t}), W_{t}^{k} = \frac{1}{n_{k}} \sum_{i=1}^{n_{k}} w_{t}^{k,i}$ ;

16 $p_{t}^{k,i} \leftarrow w_{t}^{k,i}, \forall i \in [n_{k}]$ ; // Update probability

17 for each local epoch j from 1 to E do

18 Select a batch of $b_{k}$ samples $z_{k,i} \sim p_{t}^{k,i}$ ;

19 $\theta_{t}^{k,j} = \theta_{t}^{k,j-1} - \eta_{k} \sum_{i=1}^{n_{k}} \nabla_{\theta} l(z_{k,i}; \theta_{t}^{k,j-1})$ ;

20 Return $\theta_{t}^{k,E}, W_{t}^{k}$ ;

21 Function LocalMeta ( $k, g_{t}^{v}$ ):
22 Randomly select a batch of $b_{k}$ training samples;

23 $c_{t+1}^{k} = c_{t} - n_{k} \frac{1}{b_{k}} \sum_{j=1}^{b_{k}} g_{t}^{v} \frac{\partial l(z_{k,j}; \theta_{t})}{\partial \theta} \frac{\partial f(l(z_{k,j}; \theta_{t}), c_{t})}{\partial c}$ ;

24 Return $c_{t+1}^{k}$ ;

![](images/5e9812c501a63e3f734dcc91eff0671340c2b22f9a0650bbcb1c29571a27047a.jpg)



(a) MNIST

![](images/467ece7abec73cf16b8c0e102ebc45444b4773b7ccd34ed9f8ce83b4cc482428.jpg)



(b) CIFAR-10   
Fig. 2. Federated meta network functions learned by FedMW-CSS on datasets with 40% mislabeling samples.

multiple local training steps. To utilize the class-level information for local training, the local parameters are updated on the batch $B _ { k }$ with the class-level weighted loss. Then, client k updates its weight $\boldsymbol { W } _ { t } ^ { k }$ and sends the local model $\theta _ { t } ^ { k , E }$ and weight $\boldsymbol { W } _ { t } ^ { k }$ to the server (Line 17-20).

Influence-based Model Updating. The server aggregates local models to obtain the global FL model $\theta _ { t + 1 } =$ $\begin{array} { r } { \frac { 1 } { u } \sum _ { k \in \left[ U _ { t } \right] } \theta _ { t } ^ { k , E } } \end{array}$ Pk∈[Ut] , and updates the client selection probabilities by normalizing the weights of all clients so that they sum to 1 (Line 8-9). Then, the server calculates the average gradient $g _ { t } ^ { v }$ of the batch validation samples, and sends it to client $k \in U _ { t }$ . Then, client k randomly selects a batch of samples and updates the meta model $\epsilon _ { t }$ following Eq. (19), and sends it to the server (Line 22-24). Finally, the server updates and obtains the meta model $\epsilon _ { t + 1 }$ . This way, the server and FL clients collaboratively select the most positively influential samples to construct the global FL model $\theta ^ { * }$ . Besides, we can adopt epoch-fixed embedding staleness [38] to achieve staleness-aware client and sample selection.

# 4.5 Meta-weight Learning for Bilevel FL Optimization

As we aim to obtain the optimal client and sample selection probabilities $P ^ { * }$ and $p ^ { * }$ that minimize the objective function in Eq. (3), we instead consider what the influence of each client and each training sample is on the validation set performance at training iteration $\textit { t } ( e . g . ,$ , validation accuracy or validation loss). Then, the probabilities that clients and samples are selected are determined by their corresponding influence scores $( i . e . ,$ the probability shall be proportional to the influence). Further, inspired from existing works [12], [39], [40], which posit that the influence of a set is the sum of influences of its constituent samples, we define the influence score of client k as “the average of the influence scores of its local samples which are selected for FL training”. These inspire us to design a hierarchical influence analysis method that identifies influential clients $( i . e .$ , influential subsets) first to save a significant portion of the cost incurred during the sample-level influence analysis stage.

# 4.5.1 Class-level Weighting by Gradient Manipulation

To utilize class-level information for better hard sampleaware noise-robust federated training, we learn a class-level weight for each gradient flow instead of only one scalar weight for all gradient flows. To estimate the influence or the weight of each sample, we first denote the weight of sample $z _ { k , i } \ { \mathrm { a s } } \ w _ { k , i } ,$ and the weight of client $k \in [ K ]$ is denoted as $\begin{array} { r } { W _ { k } = \frac { 1 } { n _ { k } } \sum _ { i = 1 } ^ { n _ { k } } w _ { k , i } \left[ 4 0 \right] } \end{array}$ nk Pnki=1 wk,i [40]. Applying the chain rule, we unroll the gradient of the loss $\nabla _ { \theta } l \big ( z _ { k , i } ; \theta ( P , p ) \big )$ w.r.t. θ for sample $z _ { k , i }$ as,

$$
\nabla_ {\theta} l (z _ {k, i}; \theta) = \frac {\partial l (z _ {k , i} ; \theta)}{\partial \theta} = \frac {\partial l (z _ {k , i} ; \theta)}{\partial I _ {k , i}} \frac {\partial I _ {k , i}}{\partial \theta} = J _ {1} J _ {2} \tag {7}
$$

where $I _ { k , i } \in \mathbb { R } ^ { C }$ represents the predicted logit vector of the instance $z _ { k , i }$ and C is the number of classes. We introduce class-level weights $\tau _ { k , i } \in \mathbb { R } ^ { C }$ and denote the j-th component of $\tau _ { k , i }$ as $\tau _ { k , i } ^ { j }$ . To indicate the importance of each gradient flow, we perform an element-wise product $f _ { \tau } ( \cdot )$ on $J _ { 1 }$ with $\tau ,$ and the gradient becomes,

$$
f _ {\tau} (\nabla_ {\theta} l (z _ {k, i}; \theta)) = (\tau_ {k, i} \otimes \frac {\partial l (z _ {k , i} ; \theta)}{\partial I _ {k , i}}) \frac {\partial I _ {k , i}}{\partial \theta} = J _ {1} ^ {\prime} J _ {2}, \tag {8}
$$

where $\otimes$ denotes the element-wise product of two vectors. Obviously, instance-level weight is a special case of classlevel weight when elements of $\tau _ { k , i }$ i are the same. Since we adopt softmax cross-entropy loss in our federated classification task, we have $J _ { 1 } = \hat { y } _ { k , i } - y _ { k , i } ,$ where $\hat { y } _ { k , i } \in \mathbb { R } ^ { C }$ denotes the probability vector output by softmax and $y _ { k , i } \in \mathbb { R } ^ { C }$ denotes the one-hot label of the instance $z _ { k , i }$ of client $k \in [ K ]$ .

To preserve the softmax cross-entropy loss structure, i.e., $\hat { y } _ { k , i } - y _ { k , i }$ form, we impose a zero-mean constraint on $J _ { 1 } ^ { \prime }$ after the operation. We first analyze the j-th element of $J _ { 1 } ^ { \prime } ,$ ,

$$
\tau_ {k, i} ^ {j} (\hat {y} _ {k, i} ^ {j} - y _ {k, i} ^ {j}) = (\sum_ {c = 1} ^ {C} \tau_ {k, i} ^ {c} \hat {y} _ {k, i} ^ {c}) \hat {y} _ {k, i} ^ {\prime j} - \tau_ {k, i} ^ {t} y _ {k, i} ^ {j} \tag {9}
$$

$$
\tau_ {k, i} ^ {j} \left(\hat {y} _ {k, i} ^ {j} - y _ {k, i} ^ {j}\right) = \tau_ {k, i} ^ {n} \left(\hat {y} _ {k, i} ^ {\prime j} - y _ {k, i} ^ {j}\right) + \left(\sum_ {c = 1} ^ {C} \tau_ {k, i} ^ {c} \hat {y} _ {k, i} ^ {c} - \tau_ {k, i} ^ {n}\right) \hat {y} _ {k, i} ^ {\prime j}, \tag {10}
$$

where yˆ′jk,i $\begin{array} { r } { \hat { y } _ { k , i } ^ { \prime j } = \frac { \tau _ { k , i } ^ { \jmath } \hat { y } _ { k , i } ^ { \prime \jmath } } { \sum _ { c = 1 } ^ { C } \tau _ { k , i } ^ { c } \hat { y } _ { k , i } ^ { c } } } \end{array}$ is the weighted probability, and $\tau _ { k , i } ^ { n }$ c=1 k,i k,idenotes the class-level weight at the target position n. We observe that the first term of Eq. (10) satisfies the structure of the gradient of the softmax cross-entropy loss, and thus propose to eliminate the second term which messes the structure. Specifically, we let

$$
\sum_ {c = 1} ^ {C} \tau_ {k, i} ^ {c} \hat {y} _ {k, i} ^ {c} - \tau_ {k, i} ^ {n} = 0 \Rightarrow \tau_ {k, i} ^ {n} = \frac {\sum_ {j \neq n} ^ {C} \tau_ {k , i} ^ {j} \hat {y} _ {k , i} ^ {\prime j}}{1 - \hat {y} _ {k , i} ^ {n}}, \tag {11}
$$

where $\begin{array} { r } { \sum _ { j = 1 } ^ { C } \tau _ { k , i } ^ { j } y _ { k , i } ^ { j } = \tau _ { k , i } ^ { n } , } \end{array}$ $\hat { y } _ { k , i } ^ { n }$ is the probability of the target class. Note that , then we have $\begin{array} { r } { \sum _ { j = 1 } ^ { C } \tau _ { k , i } ^ { j } ( \hat { y } _ { k , i } ^ { j } - y _ { k , i } ^ { j } ) = 0 } \end{array}$ This restrict the mean of $J _ { 1 } ^ { \prime }$ to be zero, then we have $J _ { 1 } ^ { \prime } =$ $\tau _ { k , i } ^ { n } ( \hat { y } _ { k , i } - y _ { k , i } )$ . This equation indicates that $\tau _ { k , i }$ contains gradient information in two levels, $i . e . ,$ instance level and class level. Namely, the scalar $\tau _ { k , i } ^ { n }$ acts as the instance-level weight in our previous method, and the $\tau _ { k , i } ^ { j } \mathrm { ' s }$ are the classlevel weights manipulating the gradient flows by adjusting the predicted probability from $\hat { y } _ { k , i }$ to $\hat { y } _ { k , i } ^ { \prime }$ .

The reasons of using the zero-mean constraint are as follows. Denote the true target as tt and one of the nontarget labels as nt. The gradient can be unrolled as,

$$
f _ {\tau} \left(\nabla_ {\theta} l\right) = \tau_ {k, i} ^ {n} \sum_ {j = 1} ^ {C} \left(\hat {y} _ {k, i} ^ {\prime j} - y _ {k, i} ^ {j}\right) \nabla_ {\theta} l _ {j} + \left(\sum_ {c = 1} ^ {C} \tau_ {k, i} ^ {c} \hat {y} _ {k, i} ^ {c} - \tau_ {k, i} ^ {n}\right) \sum_ {j = 1} ^ {C} \hat {y} _ {k, i} ^ {\prime j} \nabla_ {\theta} l _ {j}, \tag {12}
$$

If $\textstyle \sum _ { c = 1 } ^ { C } \tau _ { k , i } ^ { c } \hat { y } _ { k , i } ^ { c } - \tau _ { k , i } ^ { n }$ τ k ,i is positive and the learning rate is small enough, $\begin{array} { r } { ( \sum _ { c = 1 } ^ { C } \tau _ { k , i } ^ { c } \hat { y } _ { k , i } ^ { c } - \tau _ { k , i } ^ { n } ) \hat { y } _ { k , i } ^ { \prime t t } } \end{array}$ 1 contributes to the decrease of the true target logit $l _ { t t }$ after a gradient descent step. If negative, $\begin{array} { r l r } {  { ( \sum _ { c = 1 } ^ { C } \top _ { k , i } ^ { c } \hat { y } _ { k , i } ^ { c } - \tau _ { k , i } ^ { n } ) \hat { y } _ { k , i } ^ { \prime n t } } } \end{array}$ contributes to the decrease of the true target logit $l _ { n t }$ . Therefore, without the zero-mean constraint, the second term of Eq. may hurt the performance of the global model.

# 4.5.2 Efficient Meta-weight Learning and Model Updating

To estimate the class-level weight of each sample, we propose a meta-weight learning network, with which we manipulate gradient flows and optimize model parameters. Specifically, we formulate the weights $w = \{ \bar { w _ { 1 } } , \cdot \cdot \cdot , w _ { k } \}$ , where $w _ { k } ~ = ~ \{ w _ { k , 1 } , \cdot \cdot \cdot , w _ { k , n _ { k } } \}$ as a meta network w = $e ( l ; \epsilon )$ (e.g., Multi-layer Perceptron (MLP) networks with only one hidden layer), which takes the losses of samples as the inputs and outputs the corresponding scalar weights w, where ϵ are parameters contained in them (see Fig. 2). To guarantee the output weights are within [0, 1], the output passes through a Sigmoid activation function. At this time, the selection probabilities $P _ { k } , p _ { k , i }$ are equal to the weights $W _ { k } , w _ { k , i } ,$ respectively. Then, the global model $\theta ^ { * }$ is optimized by minimizing the instance-level weighted loss in $\operatorname { E q . }$ . (3) can be re-expressed as:

$$
\theta^ {*} (P, p) = \arg \min _ {\theta} \sum_ {k = 1} ^ {K} \frac {n _ {k}}{N} W _ {k} L _ {k} (\theta), \tag {13}
$$

$$
\text { where } L _ {k} (\theta) = \frac {1}{n _ {k}} \sum_ {i = 1} ^ {n _ {k}} w _ {k, i} l (z _ {k, i}; \theta).
$$

To obtain the optimal $w _ { k , i } ,$ we propose to automatically learn the parameter ϵ through meta-learning:

$$
\epsilon^ {*} = \arg \min _ {\epsilon} \frac {1}{M} \sum_ {i = 1} ^ {M} l (z _ {i} ^ {v}; \theta^ {*} (\epsilon)). \tag {14}
$$

Updating FL Models and Class-level Weights. Since the optimization for $\theta ^ { * }$ and $\epsilon ^ { * }$ is nested, we adopt an online approximation strategy based on class-level weights to update θ and ϵ. We employ SGD to optimize Eq. (14). Specifically, in the t-th training iteration, given the fraction ϕ of FL clients to be selected, and the weight distribution $\dot { W } = \{ W _ { t } ^ { 1 } , \cdots , W _ { t } ^ { K } \}$ of clients being selected, the FL server selects a subset $U _ { t }$ of $u \gets \operatorname* { m a x } \bar { \{ \phi \cdot K , 1 \} }$ clients, and distributes the parameters of the current FL model $\theta _ { t }$ to them. Each selected client $k \in U _ { t }$ then selects a mini-batch $w _ { t } ^ { k } = \{ w _ { t } ^ { k , 1 } , \cdot \cdot \cdot , w _ { t } ^ { k , n _ { k } } \}$ $B _ { k }$ of size $b _ { k }$ according to the sample weight distribution , where $w _ { t } ^ { k , \hat { i } } = e ( l ( z _ { k , i } ; \theta _ { t } ) , \epsilon _ { t } ) , i \in$ $[ n _ { k } ] .$ , is the output of the meta network in each local epoch.

To utilize the class-level information, the local model $\theta _ { t + 1 } ^ { k }$ is updated on the mini-batch $B _ { k }$ with the class-level weighted loss. Explicitly, client k calculates the class-level weights $\boldsymbol { \tau } _ { k , i } ^ { t } = \dot { w _ { k , i } ^ { t } } \mathbf { 1 }$ by cloning the output of the metaweight network for C times, where C is the number of classes. Then, it clips the weight $\tau _ { k , i } ^ { t }$ by using the intermediate gradients $g _ { t } ^ { k }$ of validation loss w.r.t. weights $\tau _ { k , i } .$ That , is, $\begin{array} { r } { g _ { t } ^ { k } = \frac { 1 } { b } \sum _ { i = 1 } ^ { b } \dot { \nabla } _ { \tau _ { k , i } } l ( z _ { i } ^ { v } ; \theta _ { t } ( \epsilon _ { t } ) ) . } \end{array}$ b , where b is the size of the mini-batch $B$ of validation instances. Then, we have:

$$
\tau_ {k, i} ^ {\prime t} = \tau_ {k, i} ^ {t} - \eta_ {\tau} \frac {g _ {t} ^ {k}}{\left| \left| g _ {t} ^ {k} \right| \right| _ {1}}, \tag {15}
$$

![](images/4412d929c62bf19e4de1c90b618bfba46518e13807b03476f55afffd9dd6df62.jpg)



(a) MNIST

![](images/55f55bb044582f18df5edf08096ea261535654d9efae16cbcc32bfa168daabaa.jpg)



(b) CIFAR-10   
Fig. 3. Weight distributions of FedMW-CSS on randomly sampled batch from datasets with 40% mislabeling samples.

where $\vert \vert g _ { t } ^ { k } \vert \vert _ { 1 }$ 1 denotes the $l _ { 1 }$ norm of class-level weights within the mini-batch B. Then, client k performs the zeroconstraint proposed in Eq. (11) on $\tau _ { k , i } ^ { \prime t }$ . Note that the twostage class-level weight generation does not incur extra computation and communication cost compared to [22] since it only utilizes the intermediate gradients during the backward propagation. Then, client k utilizes the clipped class-level weights $\tau _ { k , i } ^ { \prime t }$ to manipulate gradients and update its local parameters, which equals to the updates as follows:

$$
\theta_ {t + 1} ^ {k} (\epsilon) = \theta_ {t} (\epsilon) - \eta_ {k} \sum_ {i = 1} ^ {n _ {k}} e (l (z _ {k, i}; \theta_ {t})) \nabla_ {\theta} L _ {k} (\theta) \Bigg | _ {\theta_ {t}}, \tag {16}
$$

$$
\mathrm{where} \nabla_ {\theta} L _ {k} (\theta) = f _ {\tau_ {k, i} ^ {\prime t} (\epsilon_ {t})} (\nabla_ {\theta} l (z _ {k, i}; \theta)) \bigg | _ {\theta_ {t}},
$$

where $f _ { \tau _ { k } ^ { \prime t } , i } \left( \cdot \right)$ is the gradient manipulation operation introduced in Eq. (8). Then, the global FL model is updated as:

$$
\theta_ {t + 1} (\epsilon) = \frac {1}{u} \sum_ {k \in U _ {t}} \theta_ {t + 1} ^ {k} (\epsilon). \tag {17}
$$

Updating Federated Meta-Weight Models. Then, the updated $\theta _ { t + 1 } ( \epsilon )$ is employed to update the parameter ϵ of the meta-weight network by taking multiple gradient decent steps on a mini-batch B of b validation samples w.r.t. $\epsilon _ { t } ,$ as:

$$
\epsilon_ {t + 1} = \epsilon_ {t} - \eta \frac {1}{b} \sum_ {i = 1} ^ {b} \nabla_ {\epsilon} l (z _ {i} ^ {v}; \theta_ {t + 1} (\epsilon)) \bigg | _ {\epsilon_ {t}}, \tag {18}
$$

which, in turn, is used to update the sample and client weights and selection probabilities. η is the descent step size on the meta-weight model ϵ. To update the meta-weight model parameters and calculate the selection probabilities in the t-th iteration, the server needs to calculate the gradients of the validation loss w.r.t. the model ϵ. Instead of calculating the above gradients on all samples, we leverage a batch of $b _ { k }$ samples from a randomly selected client k to estimate them. In this way, the gradient of the validation loss w.r.t. ϵ can be calculated as:

$$
\left. \sum_ {i = 1} ^ {b} \nabla_ {\epsilon} l \left(z _ {i} ^ {v}; \theta_ {t + 1} (\epsilon)\right) \right| _ {\epsilon_ {t}} \tag {19}
$$

$$
= - \eta_ {k} \sum_ {j = 1} ^ {b _ {k}} (\frac {1}{b} \sum_ {i = 1} ^ {b} \Gamma_ {i, j} \frac {\partial f (l (z _ {k , j} ; \theta_ {t}) , \epsilon)}{\partial \epsilon} \bigg | _ {\epsilon_ {t}},
$$

where $\begin{array} { r } { \Gamma _ { i , j } = \frac { \partial l ( z _ { i } ^ { v } ; \theta ) } { \partial \theta } \bigg | _ { \theta _ { t } } ^ { \top } f _ { \tau _ { k , i } ^ { \prime } ( \epsilon _ { t } ) } \big ( \frac { \partial l ( z _ { k , j } ; \theta ) } { \partial \theta } \big ) \bigg | _ { \theta _ { t } } } \end{array}$ fτ ′k,i(ϵt)( . Then, the meta θt model $\epsilon _ { t + 1 }$ can be updated as:

$$
\epsilon_ {t + 1} = \epsilon_ {t} - \eta \eta_ {k} \frac {1}{b _ {k}} \sum_ {j = 1} ^ {b _ {k}} (\frac {1}{b} \sum_ {i = 1} ^ {b} \Gamma_ {i, j}) \frac {\partial f (l (z _ {k , j} ; \theta_ {t}) , \epsilon)}{\partial \epsilon} \bigg | _ {\epsilon_ {t}}. \tag {20}
$$

Updating Selection Probabilities. After updating meta model $\epsilon _ { t + 1 } ,$ the weights of sample selections can be updated as $\begin{array} { r } { w _ { t + 1 } ^ { k , i } = e ( l \big ( z _ { k , i } ; \theta _ { t } ) , \epsilon _ { t + 1 } \big ) , W _ { t + 1 } ^ { k } = \frac { 1 } { n _ { k } } \sum _ { i = 1 } ^ { n _ { k } } w _ { t + 1 } ^ { k , i } , } \end{array}$ 1 nk nk whereas the selection probabilities of sample $z _ { k , i }$ and of client k can be updated as pk,it+1 $\textstyle W _ { t + 1 } ^ { k } / \sum _ { k = 1 } ^ { K } W _ { t + 1 } ^ { k }$ $k$ W k , which can be normalized. $p _ { t + 1 } ^ { k , i } ~ = ~ \stackrel { { \bf \bar { w } } _ { t + 1 } ^ { k , i } } { { \bf \Phi } } , P _ { t + 1 } ^ { k } ~ =$ wt+1, P t+1

Estimation Overhead Analysis. Computing the sampling distribution from Eq. (20) is more than an order of magnitude faster compared to computing the second-order derivative for each sample. Specifically, in each iteration, each selected client optimizes the meta-weight network with $O ( d )$ operations in contrast with the original $O ( N d ^ { 2 } + d ^ { 3 } )$ operations as illustrated in Section 4.1. Meanwhile, the communication costs are only $O ( d + d ^ { \prime } ) , d ^ { \prime } \ll d$ parameters for each selected client, in contrast with the original $O ( K d ^ { 2 } )$ parameters. For the sample influence score calculation, each client locally conducts the forward prorogation to output the influence score, which only introduces a constant factor of computation cost and no communication cost. Thus, in each iteration, the computation cost of FedMW-CSS is $O ( \mu d + N )$ , while the communication cost is $O ( \mu ( d + d ^ { \prime } ) )$ .

# 4.6 Convergence Analysis

We present convergence analysis results for FedMW-CSS. For simplicity, we denote loss function $l ( z _ { k , i } ; \theta )$ of sample $z _ { k , i }$ as $l _ { k , i } ,$ , and $l ( z _ { i } ^ { v } ; \theta )$ of validation sample $z _ { i } ^ { v }$ as $l _ { i } ^ { v }$ .

Assumption 1. The validation loss functions are β-Lipschitz continuous with $\| \nabla l _ { i } ^ { v } - \nabla l _ { j } ^ { v } \| \leqslant \beta \| \dot { z _ { i } ^ { v } } - z _ { j } ^ { v } \| , \forall z _ { i } ^ { v } , z _ { j } ^ { v } \in D _ { v } .$

Assumption 2. The loss function $L _ { k } , k \in [ K ]$ has σ-bounded gradients with $\begin{array} { r } { \big | \big | \nabla L _ { k } ( \theta ) \big | \big | \leqslant \sigma } \end{array}$ .

FedMW-CSS leverages useful information from both the training set and validation set, and converges to an appropriate distribution favored by the validation set. This helps it achieve improved generalization and robustness against biases in the training set (as illustrated in our experiments).

Lemma 1. (Convergence of FedMW-CSS.) Under the above assηk s, and let the learning rate , the validation loss monoto $\eta _ { k }$ for client k satisfiesally decreases for any $\leqslant \frac { 2 b _ { k } } { \beta \sigma ^ { 2 } }$ sequence of training batches,

$$
L _ {v} (\theta_ {t + 1}) \leqslant L _ {v} (\theta_ {t}), \tag {21}
$$

where $\begin{array} { r } { L _ { v } ( \theta _ { t } ) \ = \ \frac { 1 } { M } \sum _ { i = 1 } ^ { M } l _ { i } ^ { v } ( \theta _ { t } ( P , p ) ) } \end{array}$ is the total validation loss. Besides, in expectation, the equality in Eq. (22) holds only when the gradient $\nabla L _ { v } ( \theta _ { t } ) = \mathrm { ~ 0 ~ }$ at some step t, namely $\mathbb E _ { t } [ \bar { L } _ { v } ( \theta _ { t + 1 } ) ] = L _ { v } ( \theta _ { t } )$ if and only $i f \nabla L _ { v } ( \theta _ { t } ) = \dot { 0 } ,$ , where the expectation is computed over all batches at step t.

We present the detailed convergence proof in Appendix.

# 5 EXPERIMENTAL EVALUATION

# 5.1 Experimental Settings

Implementation. We implemented FedMW-CSS and Fed-CSS and in an FL system consisting of one server and 10 clients. To further investigate the performance of FedMW-CSS and FedCSS in large-scale FL systems, we also tested it in an environment with up to 1,000 clients. Our implementation is based on Python 3.9 and Pytorch 1.8.1 [41]. All the experiments are performed on Ubuntu 16 operating system equipped with two 20-core Intel(R) Xeon(R) CPU, 512G of RAM and 8 Tesla V100 GPUs.

Datasets. As presented in Table 2, we use six real-world datasets of different scales and different modalities for our FL tasks. 1) MNIST [42]: It is used for handwritten recognition task with digits between 0 and 9. 2) FEMNIST [43]: It consists of a federated version of the MNIST, maintained by the LEAF project [44]. This dataset has 62 different classes and contains a total of 817,851 images. 3) CIFAR-10 [45]: It consists of 60,000 colour images in 10 classes, with 6,000 images per class. 4) CIFAR-100 [46]: It is a subset of the Tiny Images dataset and consists of 60,000 color images in 100 classes. 5) KDD99 [47]: It is used for the third international knowledge discovery and data mining tools competition, which contains 23 categories. 6) AGNews [48]: It is a collection of news articles which have been gathered from more than 2000 news sources. For these datasets, we randomly select 1,000 instances from the training sets as the validation sets without introducing new data. We take the corrupted mislabeled data as the training set noise. Specifically, given a mislabeling ratio r, the label of each sample is independently changed to a random class with probability (1 − r) following the same setting in [27].

TABLE 2 Datasets for different FL tasks. 

<table><tr><td>Modality</td><td>Dataset</td><td>Notation</td><td>Size</td><td>Description</td></tr><tr><td rowspan="16">Image</td><td rowspan="4">MNIST</td><td> $D_M$ </td><td>60,000</td><td rowspan="4">original training data of MNIST $D_M$  with 10%-70% mislabeled samplesimages randomly select from  $D_M$ original testing data of MNIST</td></tr><tr><td> $D_M^m$ </td><td>60,000</td></tr><tr><td> $D_M^v$ </td><td>1,000</td></tr><tr><td> $D_M^I$ </td><td>10,000</td></tr><tr><td rowspan="4">FEMNIST</td><td> $D_F$ </td><td>736,066</td><td rowspan="4">original training data of FEMNIST $D_F$  with 10%-70% mislabeled samplesimages randomly select from  $D_F$ original testing data of FEMNIST</td></tr><tr><td> $D_F^m$ </td><td>736,066</td></tr><tr><td> $D_F^v$ </td><td>1,000</td></tr><tr><td> $D_F^T$ </td><td>81,785</td></tr><tr><td rowspan="4">CIFAR-10</td><td> $D_C$ </td><td>50,000</td><td rowspan="4">original training data of CIFAR-10 $D_C$  with 10%-70% mislabeled samplesimages randomly select from  $D_C$ original testing data of CIAFR-10</td></tr><tr><td> $D_C^m$ </td><td>50,000</td></tr><tr><td> $D_C^v$ </td><td>1,000</td></tr><tr><td> $D_C^T$ </td><td>10,000</td></tr><tr><td rowspan="4">CIFAR-100</td><td> $D_I$ </td><td>50,000</td><td rowspan="4">original training data of CIFAR-100 $D_I$  with 10%-70% mislabeled samplesimages randomly select from  $D_I$ original testing data of CIFAR-100</td></tr><tr><td> $D_I^m$ </td><td>50,000</td></tr><tr><td> $D_I^v$ </td><td>1,000</td></tr><tr><td> $D_I^T$ </td><td>10,000</td></tr><tr><td rowspan="4">Tabular</td><td rowspan="4">KDD99</td><td> $D_K$ </td><td>4,898,431</td><td rowspan="4">original training data of KDD99 $D_K$  with 10%-50% mislabeled samplesimages randomly select from  $D_K$ original testing data of KDD99</td></tr><tr><td> $D_K^m$ </td><td>4,898,431</td></tr><tr><td> $D_K^v$ </td><td>1,000</td></tr><tr><td> $D_K^T$ </td><td>311,029</td></tr><tr><td rowspan="4">Text</td><td rowspan="4">AGNews</td><td> $D_A$ </td><td>120,000</td><td rowspan="4">original training data of AGNews $D_A$  with 10%-70% mislabeled samplesimages randomly select from  $D_A$ original testing data of AGNews</td></tr><tr><td> $D_A^m$ </td><td>120,000</td></tr><tr><td> $D_A^v$ </td><td>1,000</td></tr><tr><td> $D_A^T$ </td><td>7,600</td></tr></table>

Data Distribution. We partitioned dataset Dm over 10 clients in both iid (independent and identically distributed) and non-iid (non-independent and identically distributed) settings following the setting in [1]. We divided images of sorted digits into 600 shards of size 100 and assigned each client 60 shards. When the 60 shards contain images of 10 different digits, this is referred to as the iid setting; otherwise, non-iid one. Specifically, according to the mislabelled data distribution, we consider two iid settings (e.g., iid (1), iid (2)) and two non-iid settings. They are: 1) same noisy data distributions, in which we distribute the mislabeled data samples randomly to all clients for both iid and non-iid settings; and 2) different noisy data distributions, in which we distribute the mislabeled data samples randomly to five clients for both iid and non-iid settings. We denote non-iid $[ c ] , e . g . , 1 \leq c \leq 1 0 .$ , to indicate that each client has samples from c random categories out of all ten categories. We set $c = 0 . 6 * C$ where C is the number of categories, and further evaluate how FedMW-CSS and FedCSS behave as c varies. We partitioned other training datasets in both iid and noniid settings as for dataset $D _ { M } ^ { \bar { m } }$ (see Table 3). The validation sets and testing sets are located at the server.

TABLE 3 Experiment settings for training different models. 

<table><tr><td>Model</td><td>Dataset</td><td>Setting</td><td>Noise ratio</td></tr><tr><td rowspan="2">Fed-MNIST</td><td rowspan="2"> $D_M^m$ </td><td>iid (1)/ non-iid (1)</td><td>40%</td></tr><tr><td>iid (2)/ non-iid (2)</td><td>30%</td></tr><tr><td rowspan="2">Fed-FEMNIST</td><td rowspan="2"> $D_F^m$ </td><td>iid (1)/ non-iid (1)</td><td>40%</td></tr><tr><td>iid (2)/ non-iid (2)</td><td>30%</td></tr><tr><td rowspan="2">Fed-CF10</td><td rowspan="2"> $D_C^m$ </td><td>iid (1)/ non-iid (1)</td><td>40%</td></tr><tr><td>iid (2)/ non-iid (2)</td><td>30%</td></tr><tr><td rowspan="2">Fed-CF100</td><td rowspan="2"> $D_I^m$ </td><td>iid (1)/ non-iid (1)</td><td>20%</td></tr><tr><td>iid (2)/ non-iid (2)</td><td>15%</td></tr><tr><td rowspan="2">Fed-KDD</td><td rowspan="2"> $D_K^m$ </td><td>iid (1)/ non-iid (1)</td><td>40%</td></tr><tr><td>iid (2)/ non-iid (2)</td><td>40%</td></tr><tr><td rowspan="2">Fed-AGNews</td><td rowspan="2"> $D_A^m$ </td><td>iid (1)/ non-iid (1)</td><td>40%</td></tr><tr><td>iid (2)/ non-iid (2)</td><td>40%</td></tr></table>

FL Models. We have implemented FedMW-CSS (Algorithm 1) and four residual networks based on ResNet-32 [49]: Fed-MNIST, Fed-FEMNIST, Fed-CF10 and Fed-CF100 for classifying images in MNIST, FEMNIST, CIFAR-10 and CIFAR-100, a three-layer MLP network [50]: Fed-KDD for classifying instances in dataset KDD99, and a transformer-based neural network [51]: Fed-AGNews for classifying texts in AGNews. During model training, we set the fraction of selected clients to $\phi = 0 . 4$ , each client has a learning rate of $\eta = 0 . 0 1$ (without learning rate decay), a momentum of 0.5 for $D _ { M } ^ { m }$ M , DmC in iid setting, 0.9 in noniid setting, and 0.9 for $D _ { F } ^ { m } , D _ { I } ^ { m }$ , and batch size of 100 for both the local and meta learning. We conduct FL until a prespecified test accuracy is reached, or a maximum number of iterations has elapsed. For all experiments, we perform 5-fold cross validation and report the average results.

Comparison Baselines. We compare FedMW-CSS and FedCSS against eight state-of-the-art baselines, including: 1) FedAvg [1]: FedAvg with random client and sample selection. 2) Loss-based: FedAvg with client selection that prioritizes clients with high losses, which is similar with existing works [13], [14]. 3) FOCUS [52]: It performs credit weighted FL model aggregation to mitigate label noise by assigning credibility values to clients. 4) CAreFL [17]: It utilizes participant contribution evaluation results to optimize the global model aggregation. 5) FocalLoss [53]: A robust learning method that focuses training on a set of hard examples and prevents easy negatives from overwhelming the predictor during training. We extended it into FL settings. 6) ImpCSS: FedAvg with sample-level data selection that prioritizes samples with high importance derived from sample losses [9], [15]. 7) ActPerFL [54]: an active personalized FL solution that guides local training and global aggregation via inter- and intra-client uncertainty quantification. 8) FedNest [37]: Federated bilevel optimization with HVPbased approximations. Among these baselines, two methods CAreFL and FedNest require validation sets.

![](images/7760a78c5643434c98fe540536cd9acdf29270aa0771d7fe9323da6ccf65c474.jpg)



(a) Fed-MNIST, round-to-accuracy

![](images/80fa0aa43ff430d34b39885bae3114b8245296b7c6a1029bcb40c01920fd9ad2.jpg)



(b) Fed-CF10, round-to-accuracy

![](images/f53e3c00da05ffed1e1819e1175c130b58a54362c076d9e8c3a942c048228f7f.jpg)



(c) Fed-MNIST, time-to-accuracy

![](images/7ad096f24bef98fa59a3f8a04f89a9ccb580f26f406277a13c05eef12abc35e5.jpg)



(d) Fed-CF10, time-to-accuracy   
Fig. 4. Test accuracy of different communication rounds and different time periods for training various models.

TABLE 4 Test accuracy comparison under different settings for different datasets. 

<table><tr><td>Dataset</td><td>Setting</td><td colspan="10">Test accuracy (%) ± standard deviations</td></tr><tr><td rowspan="5"> $D_{M}^{m}$ </td><td></td><td>FedAvg</td><td>Loss-based</td><td>FOCUS</td><td>CAreFL</td><td>FocalLoss</td><td>ImpCSS</td><td>ActPerFL</td><td>FedNest</td><td>FedCSS</td><td>FedMW-CSS</td></tr><tr><td>iid (1)</td><td>96.95± 0.27</td><td>94.98± 0.03</td><td>97.23± 0.05</td><td>97.02± 0.09</td><td>96.07± 0.22</td><td>93.76± 0.32</td><td>97.11± 0.13</td><td>96.25± 0.28</td><td>98.28± 0.11</td><td>98.36± 0.08</td></tr><tr><td>iid (2)</td><td>96.70± 1.02</td><td>93.82± 0.05</td><td>94.82± 0.11</td><td>97.32± 0.47</td><td>94.73± 2.92</td><td>94.2± 2.52</td><td>95.41± 0.19</td><td>95.32± 0.23</td><td>98.32± 0.06</td><td>98.38± 0.07</td></tr><tr><td>non-iid (1)</td><td>96.01± 0.34</td><td>89.98± 0.69</td><td>96.23± 0.12</td><td>90.47± 7.62</td><td>95.67± 0.93</td><td>94.43± 0.57</td><td>95.51± 0.06</td><td>94.78± 0.18</td><td>98.18± 0.09</td><td>98.21± 0.04</td></tr><tr><td>non-iid (2)</td><td>93.07± 0.34</td><td>81.42± 0.32</td><td>95.13± 0.13</td><td>79.98± 1.62</td><td>92.28± 1.23</td><td>93.42± 0.37</td><td>95.32± 0.27</td><td>93.61± 0.16</td><td>98.03± 0.18</td><td>97.80± 0.10</td></tr><tr><td rowspan="4"> $D_{F}^{m}$ </td><td>iid (1)</td><td>87.58± 0.21</td><td>86.23± 0.22</td><td>88.04± 0.16</td><td>86.54± 0.12</td><td>88.02± 0.21</td><td>87.31± 0.24</td><td>86.83± 0.17</td><td>86.62± 0.03</td><td>88.22± 0.16</td><td>89.12± 0.12</td></tr><tr><td>iid (2)</td><td>88.40± 0.62</td><td>87.79± 0.12</td><td>88.23± 0.13</td><td>85.25± 0.16</td><td>88.07± 1.22</td><td>87.52± 1.27</td><td>86.12± 0.12</td><td>87.01± 0.08</td><td>88.62± 0.12</td><td>88.98± 0.1</td></tr><tr><td>non-iid (1)</td><td>84.82± 0.41</td><td>75.51± 1.18</td><td>84.31± 0.21</td><td>59.89± 1.05</td><td>84.14± 0.83</td><td>81.23± 0.17</td><td>83.54± 0.27</td><td>84.05± 0.12</td><td>86.10± 0.14</td><td>87.61± 0.03</td></tr><tr><td>non-iid (2)</td><td>83.10± 0.41</td><td>75.05± 1.18</td><td>84.31± 0.21</td><td>58.78± 1.65</td><td>80.04± 0.83</td><td>82.12± 0.17</td><td>82.89± 0.72</td><td>83.19± 0.13</td><td>85.51± 0.14</td><td>87.21± 0.11</td></tr><tr><td rowspan="4"> $D_{C}^{m}$ </td><td>iid (1)</td><td>47.99± 0.83</td><td>39.49± 0.42</td><td>46.26± 1.83</td><td>48.44± 1.65</td><td>47.86± 0.13</td><td>48.06± 1.30</td><td>45.88± 0.19</td><td>46.82± 0.31</td><td>53.73± 0.46</td><td>55.81± 0.17</td></tr><tr><td>iid (2)</td><td>44.01± 3.98</td><td>41.53± 3.06</td><td>50.52± 1.32</td><td>52.08± 6.01</td><td>49.61± 0.88</td><td>51.21± 1.22</td><td>51.76± 0.08</td><td>50.61± 0.27</td><td>56.83± 1.12</td><td>58.32± 0.83</td></tr><tr><td>non-iid (1)</td><td>41.29± 1.21</td><td>36.79± 1.51</td><td>43.69± 1.51</td><td>41.08± 1.40</td><td>42.12± 1.29</td><td>36.73± 0.24</td><td>44.01± 0.16</td><td>43.91± 0.81</td><td>45.60± 0.45</td><td>46.71± 0.13</td></tr><tr><td>non-iid (2)</td><td>39.01± 2.34</td><td>29.33± 1.69</td><td>39.23± 1.13</td><td>29.81± 1.62</td><td>38.42± 1.73</td><td>39.10± 2.07</td><td>39.98± 0.72</td><td>38.92± 0.24</td><td>40.65± 0.12</td><td>40.12± 0.21</td></tr><tr><td rowspan="4"> $D_{I}^{m}$ </td><td>iid (1)</td><td>26.12± 0.27</td><td>17.61± 0.21</td><td>27.03± 0.16</td><td>27.83± 0.68</td><td>26.41± 0.23</td><td>27.18± 0.56</td><td>25.08± 0.28</td><td>26.91± 0.71</td><td>33.51± 0.35</td><td>34.16± 0.28</td></tr><tr><td>iid (2)</td><td>27.27± 0.48</td><td>17.97± 0.26</td><td>27.87± 0.34</td><td>22.95± 0.17</td><td>29.71± 0.28</td><td>29.87± 0.32</td><td>27.85± 0.21</td><td>28.01± 0.17</td><td>35.06± 0.23</td><td>36.67± 0.15</td></tr><tr><td>non-iid (1)</td><td>22.41± 1.22</td><td>14.69± 1.52</td><td>23.12± 2.32</td><td>17.91± 2.42</td><td>23.16± 2.27</td><td>24.17± 1.38</td><td>24.04± 0.49</td><td>24.56± 0.29</td><td>28.73± 1.31</td><td>29.96± 0.82</td></tr><tr><td>non-iid (2)</td><td>25.01± 1.34</td><td>16.11± 2.69</td><td>24.83± 1.03</td><td>17.21± 2.02</td><td>25.14± 1.93</td><td>25.42± 1.27</td><td>25.57± 0.35</td><td>23.86± 0.12</td><td>28.27± 1.07</td><td>28.65± 0.62</td></tr><tr><td rowspan="4"> $D_{K}^{m}$ </td><td>iid (1)</td><td>74.12± 0.21</td><td>73.61± 0.13</td><td>72.03± 0.32</td><td>73.83± 0.61</td><td>75.61± 0.23</td><td>73.18± 0.56</td><td>74.08± 0.17</td><td>74.23± 0.41</td><td>75.51± 0.31</td><td>75.76± 0.25</td></tr><tr><td>iid (2)</td><td>72.27± 0.48</td><td>73.97± 0.26</td><td>74.17± 0.34</td><td>72.95± 0.14</td><td>73.71± 0.28</td><td>73.87± 0.02</td><td>73.85± 0.21</td><td>72.01± 0.12</td><td>75.98± 0.23</td><td>77.12± 0.26</td></tr><tr><td>non-iid (1)</td><td>73.41± 0.22</td><td>72.69± 0.52</td><td>74.12± 0.32</td><td>72.91± 0.42</td><td>73.16± 0.27</td><td>72.17± 1.38</td><td>73.21± 0.12</td><td>73.89± 0.05</td><td>74.23± 1.31</td><td>76.57± 0.91</td></tr><tr><td>non-iid (2)</td><td>72.89± 0.34</td><td>71.11± 0.69</td><td>72.98± 1.03</td><td>73.21± 0.32</td><td>71.14± 0.93</td><td>25.42± 1.27</td><td>72.57± 0.35</td><td>72.25± 0.04</td><td>73.07± 1.07</td><td>73.58± 0.56</td></tr><tr><td rowspan="4"> $D_{A}^{m}$ </td><td>iid (1)</td><td>82.33± 0.17</td><td>81.61± 0.21</td><td>84.51± 0.07</td><td>80.83± 0.15</td><td>83.54± 0.26</td><td>82.75± 0.56</td><td>84.01± 0.08</td><td>83.46± 0.26</td><td>84.09± 0.05</td><td>85.26± 0.17</td></tr><tr><td>iid (2)</td><td>81.27± 0.18</td><td>81.57± 0.62</td><td>81.87± 0.14</td><td>80.43± 0.16</td><td>81.43± 0.16</td><td>80.87± 0.12</td><td>81.19± 0.16</td><td>80.86± 0.29</td><td>82.26± 0.21</td><td>82.78± 0.19</td></tr><tr><td>non-iid (1)</td><td>81.41± 0.22</td><td>82.67± 0.31</td><td>81.12± 0.32</td><td>80.05± 0.19</td><td>82.43± 0.21</td><td>81.17± 0.38</td><td>82.67± 0.18</td><td>80.26± 0.19</td><td>82.73± 0.31</td><td>83.81± 0.14</td></tr><tr><td>non-iid (2)</td><td>79.71± 0.41</td><td>80.14± 0.61</td><td>80.83± 0.09</td><td>79.62± 0.17</td><td>80.14± 0.26</td><td>79.42± 0.27</td><td>79.96± 0.17</td><td>78.76± 0.28</td><td>80.27± 0.27</td><td>80.71± 0.19</td></tr></table>

![](images/e8fe388dc1ee5be2fd069ce27ab7f0824dc31a43c1faf126237f23e530a9ea9a.jpg)



Fig. 5. Confusion matrices of Fed-CF10.

![](images/ee8196c5b432c545be6efb06594c828a9a3e728b41269fe23e484be345e24d11.jpg)



Fig. 6. Test accuracy with imbalanced validation set.

![](images/3c4bb6bd85c29388db34c613a11a569fc0f31975d16376dd69ca57b690c1b8bd.jpg)



(a) Computation cost

![](images/56ed4c04c4a2de1f48c1f57f77f6a17b151aec11fbbcefa54e5a5e1a00d7faed.jpg)



(b) Communication cost   
Fig. 7. The average computation cost and communication cost for each client for training models under the setting of iid (1).

# 5.2 Results and Discussion

FedMW-CSS and FedCSS improve accuracy. We evaluate the test accuracy of the global models under both iid and non-iid settings. It shows that FedMW-CSS outperforms all other methods in terms of both test accuracy and convergence speed in all scenarios. For example, in the 100- th round of training the Fed-CF10 model on dataset DmC in the iid (1) setting, the test accuracy of FedMW-CSS is 55.86%, outperforming the best baseline CAreFL by 2.66%. Besides, we note that the Loss-based and ImpCSS methods are much more vulnerable to noisy samples, because these two methods prioritize clients and samples with large losses, whereas such clients and samples can be erroneous ones. Although these methods filter out noisy samples by setting loss thresholds, those thresholds are hard to determine in practice due to i.e., different proportions of noisy data. Further, we note that the CAreFL method performs worse than other methods on the large dataset, e.g., DmF , especially in non-iid settings due to limited number of monte-carlo sampling, which makes it inapplicable in largesize datasets. We present the test accuracy of global models and the standard deviations in Table 4. Here, we adopt the early stop strategy to keep track of the prediction accuracy (i.e., we terminate the procedure when the accuracy stops increasing for 10 consecutive epochs). The results in Table 4 show that FedMW-CSS achieves higher test accuracy than all other baseline methods. Further, we evaluate the test accuracy of the final global models using FedMW-CSS for all individual categories. We present the confusion matrix results of Fed-CF10 in Fig.5, which shows that FedMW-CSS achieves high test accuracy among all categories.

![](images/e9ff883782fde865dc3574278010231192d10a8f2b0130551fae170a111c0303.jpg)



(a) Noise levels

![](images/c52e7277ff3c6042f88b68695700510103adf472c53e89f4253b64b945ce4a04.jpg)



(b) (ρ, δ)-DP values

![](images/226bf2dab80dabe5ef30a302c1b4231533e8d763f90ef415b83c266f575b43d3.jpg)



(c) Number of validation samples

![](images/b68cb7163ba976eaa5ac8e63fab578e8273b96a1f137bb28017f3e0815fbca13.jpg)



(d) Non-iid degree   
Fig. 8. Sensitivity analysis of test accuracy trained on different models under various factor settings.

TABLE 5 Class-level weights in an iteration for a noisy instance. 

<table><tr><td>Gradient flow information</td><td>‘not cat’</td><td>‘dog’</td><td>‘not bird’</td></tr><tr><td>Initial weight</td><td colspan="3">0.46</td></tr><tr><td>FedCSS</td><td colspan="3">0.43</td></tr><tr><td>FedMW-CSS</td><td>0.24</td><td>0.41</td><td>0.65</td></tr></table>

TABLE 6 Test accuracy of models trained with various ablation baselines. 

<table><tr><td>Dataset</td><td colspan="4">Test accuracy (%) ± standard deviations</td></tr><tr><td></td><td>FedAvg</td><td>FedCSS1</td><td>FedCSS2</td><td>FedMW-CSS</td></tr><tr><td> $D_{M}^{m}$ </td><td>96.95±0.27</td><td>97.03±0.45</td><td>97.34±0.32</td><td>98.36±0.08</td></tr><tr><td> $D_{F}^{m}$ </td><td>87.58±0.21</td><td>88.05±0.56</td><td>88.56±0.41</td><td>89.12±0.12</td></tr><tr><td> $D_{C}^{m}$ </td><td>47.99±0.83</td><td>48.34±0.45</td><td>50.56±0.37</td><td>55.81±0.17</td></tr><tr><td> $D_{I}^{m}$ </td><td>26.12±0.27</td><td>27.23±0.24</td><td>30.12±0.37</td><td>34.16±0.28</td></tr><tr><td> $D_{k}^{m}$ </td><td>74.12±0.21</td><td>74.53±0.31</td><td>75.02±0.36</td><td>75.76±0.25</td></tr><tr><td> $D_{A}^{m}$ </td><td>82.33±0.17</td><td>83.02±0.24</td><td>83.76±0.42</td><td>85.26±0.17</td></tr></table>

![](images/ce8d17dfceb2454bea678126d616cecd690968bcb28cc402cebf7f38a52d7a8b.jpg)



(a) Computation cost

![](images/735e3db0aecfc8a169cdb0734a291036d60c516026795f28d41f756770a95338.jpg)



(b) Communication cost   
Fig. 9. The average computation cost and communication cost for each client for training models for various ablation baselines.

FedMW-CSS and FedCSS improve efficiency. We present the average computation cost and communication cost for each local client which includes both the FL training and the meta weight learning. Similarly, we adopt the early stop strategy under both iid and non-iid settings. That is to say, we run FL either until a pre-specified test accuracy is reached (96.0% for $D _ { M } ^ { m }$ , 80.0% for $D _ { F } ^ { m }$ , 47.0% for $D _ { C } ^ { \dot { m } } .$ , 25.0% for $D _ { I } ^ { m } .$ , 74.0% for $D _ { K } ^ { m }$ and 82.0% for $D _ { A } ^ { m } )$ for 10 consecutive communication rounds. The example results of the average computation cost and communication cost of each client are shown in Fig. 7 for training Fed-MNIST and Fed-CF10 under iid settings. The average computation cost and communication cost for training Fed-FEMNIST and Fed-CF100 are quite similar to that in Fig. 7. It shows that FedMW-CSS achieves significantly higher saving of both computation and communication costs than the first seven baselines and is comparable to that of the FedCSS method. As an example, for model Fed-CF10 training on $D _ { C } ^ { m }$ in the setting of iid (2), the runtime of FedCSS and FedMW-CSS is only 73.7s and 65.1s, which is 1.95× and 2.34× faster runtime than the best performing baseline. The communication cost of FedCSS and FedMW-CSS is only 455.3 MB and 385.4 MB, which is 40.1% and 49.3% lower than the best performing baseline. The reasons for the faster convergence of FedCSS and FedMW-CSS are as follows. Since some baseline methods can easily overfit the training noise, the training is unstable and the model converges slowly. In contrast, through selecting important clients and samples and filtering noisy ones, FedMW-CSS achieves much faster convergence speed and reduces computation and communication cost.

Working mechanism. It is beneficial to understand how FedMW-CSS learns robust FL models. We use a pre-trained model (trained at half of the total rounds) and measure the example weight distribution of a randomly selected client with mislabeled samples on training images. As shown in Fig. 3, FedMW-CSS can correctly distinguish clean and noisy samples. Most of the large weights belong to clean samples, while noisy sample weights are much smaller than that of clean samples. FedMW-CSS selects clean samples with higher probabilities than noisy samples for FL training. Further, in Table 5, we show the change of class-level weights in an iteration for a noisy instance, i.e., a cat image mislabeled as ‘dog’ in CIFAR10 dataset. The gradient flows of ‘not cat’ and ‘dog’ contain harmful information and thus are downweighted by FedMW-CSS and upweights the valuable ‘not bird’ gradient flow from 0.46 to 0.65. In contrast, since FedCSS ignores class-level information, it downweights all gradient flows from 0.46 to 0.43, which leads to information loss on the ‘not bird’ gradient flow.

# 5.3 Ablation Study

We perform various ablation studies to show the effectiveness of each component of FedMW-CSS. We compare FedMW-CSS against the following baselines: 1) FedAvg; 2) FedCSS1: it only conducts noisy data detection [33] before FL training without hard sample selection during FL training; and 3) FedCSS2: It performs both noisy data detection before FL training and hard sample selection during FL training by using the loss-based importance sampling method [15]. We train various FL models using these ablation baselines and present the test accuracy in Table 6 and show the total communication costs in Fig. 9. The results show that FedMW-CSS achieves better performance, e.g., for the model Fed-CF10, it achieves 0.56% higher test accuracy than the best performing baseline while saving 83.43% computation cost and 81.82% communication cost.

TABLE 7 Test accuracy comparison under different datasets with various noise ratios. 

<table><tr><td>Dataset</td><td>Method</td><td colspan="7">Various noise ratios</td></tr><tr><td rowspan="11"> $D_{M}^{m}$ </td><td></td><td>0.1</td><td>0.2</td><td>0.3</td><td>0.4</td><td>0.5</td><td>0.6</td><td>0.7</td></tr><tr><td>FedAvg</td><td>98.20± 0.07</td><td>97.80± 0.02</td><td>97.22± 0.21</td><td>97.10± 0.34</td><td>96.29± 0.05</td><td>93.85± 0.55</td><td>88.69± 3.67</td></tr><tr><td>Loss-based</td><td>96.64± 0.01</td><td>95.28± 0.01</td><td>95.01± 0.01</td><td>94.97± 0.02</td><td>91.72± 0.02</td><td>90.65± 0.03</td><td>82.66± 0.32</td></tr><tr><td>FOCUS</td><td>98.48± 0.04</td><td>98.11± 0.08</td><td>97.51± 0.06</td><td>97.23± 0.05</td><td>95.86± 0.04</td><td>93.08± 0.11</td><td>88.21± 0.12</td></tr><tr><td>CAreFL</td><td>98.36± 0.02</td><td>98.22± 0.17</td><td>97.22± 0.13</td><td>97.01± 0.09</td><td>96.31± 0.05</td><td>93.61± 0.36</td><td>92.05± 0.03</td></tr><tr><td>FocalLoss</td><td>97.97± 0.06</td><td>97.57± 0.23</td><td>97.24± 0.17</td><td>96.08± 0.22</td><td>94.43± 0.01</td><td>93.69± 0.58</td><td>89.74± 2.38</td></tr><tr><td>ImpCSS</td><td>96.07± 0.01</td><td>94.64± 0.23</td><td>94.0± 0.21</td><td>93.78± 0.32</td><td>92.04± 0.75</td><td>89.18± 1.64</td><td>83.43± 1.22</td></tr><tr><td>ActPerFL</td><td>98.27± 0.08</td><td>97.85± 0.13</td><td>97.34± 0.12</td><td>97.11± 0.13</td><td>96.15± 0.15</td><td>93.12± 0.34</td><td>89.13± 0.32</td></tr><tr><td>FedNest</td><td>97.37± 0.13</td><td>96.89± 0.12</td><td>96.61± 0.11</td><td>96.25± 0.28</td><td>93.56± 0.15</td><td>90.12± 0.27</td><td>88.47± 0.27</td></tr><tr><td>FedCSS</td><td>98.38± 0.08</td><td>98.43± 0.06</td><td>98.19± 0.06</td><td>98.24± 0.17</td><td>98.0± 0.03</td><td>97.79± 0.04</td><td>96.73± 0.05</td></tr><tr><td>FedMW-CSS</td><td>98.67± 0.12</td><td>98.58± 0.08</td><td>98.19± 0.11</td><td>98.36± 0.08</td><td>98.21± 0.06</td><td>98.05± 0.10</td><td>97.69± 0.03</td></tr><tr><td rowspan="10"> $D_{C}^{m}$ </td><td>FedAvg</td><td>56.46± 0.84</td><td>55.6± 1.56</td><td>51.52± 0.90</td><td>47.99± 0.83</td><td>41.52± 0.26</td><td>34.34± 0.50</td><td>31.12± 0.82</td></tr><tr><td>Loss-based</td><td>46.63± 0.93</td><td>44.73± 0.14</td><td>43.23± 1.26</td><td>39.49± 0.42</td><td>36.54± 0.35</td><td>33.60± 2.07</td><td>29.61± 0.93</td></tr><tr><td>FOCUS</td><td>55.42± 0.56</td><td>53.02± 0.78</td><td>50.03± 0.57</td><td>46.16± 0.83</td><td>42.57± 0.34</td><td>37.47± 0.42</td><td>30.04± 0.65</td></tr><tr><td>CAreFL</td><td>57.73± 0.54</td><td>56.86± 0.47</td><td>52.91± 0.67</td><td>48.44± 0.95</td><td>43.60± 0.34</td><td>41.1± 1.14</td><td>35.64±1.86</td></tr><tr><td>FocalLoss</td><td>55.38± 2.65</td><td>52.19± 4.20</td><td>48.05± 0.91</td><td>47.86± 0.13</td><td>45.71± 0.59</td><td>40.03± 1.16</td><td>35.89± 1.71</td></tr><tr><td>ImpCSS</td><td>55.41± 0.80</td><td>52.63± 0.50</td><td>49.39± 0.56</td><td>48.06± 1.30</td><td>43.35± 1.91</td><td>41.1± 0.06</td><td>32.14± 0.58</td></tr><tr><td>ActPerFL</td><td>53.12± 0.12</td><td>50.15± 0.15</td><td>47.32± 0.26</td><td>45.88± 0.19</td><td>43.05± 1.01</td><td>41.3± 0.16</td><td>31.87± 0.43</td></tr><tr><td>FedNest</td><td>54.47± 0.18</td><td>50.62± 0.16</td><td>48.32± 0.16</td><td>46.82± 0.31</td><td>44.15± 0.51</td><td>41.24± 0.16</td><td>33.45± 0.62</td></tr><tr><td>FedCSS</td><td>62.05± 0.11</td><td>59.53± 1.00</td><td>57.01± 0.04</td><td>53.73± 0.57</td><td>50.38± 0.01</td><td>46.56± 1.20</td><td>40.66± 0.68</td></tr><tr><td>FedMW-CSS</td><td>65.12± 0.06</td><td>61.76± 0.16</td><td>58.17± 0.14</td><td>55.81± 0.57</td><td>52.64± 0.21</td><td>48.98± 0.32</td><td>43.77± 0.18</td></tr></table>

TABLE 8 Test accuracy comparison on imbalanced classes. FedMW-CSS uses a small balanced validation split of 10 samples. 

<table><tr><td>Imbalance</td><td colspan="10">Test accuracy (%) ± standard deviations</td></tr><tr><td></td><td>FedAvg</td><td>Loss-based</td><td>FOCUS</td><td>CAreFL</td><td>FocalLoss</td><td>ImpCSS</td><td>ActPerFL</td><td>FedNest</td><td>FedCSS</td><td>FedMW-CSS</td></tr><tr><td>20</td><td>87.85± 0.19</td><td>70.92± 1.92</td><td>90.63± 0.23</td><td>88.28± 0.81</td><td>89.98± 0.72</td><td>86.62± 0.24</td><td>88.98± 0.21</td><td>87.86± 0.08</td><td>96.95± 0.45</td><td>97.68± 0.12</td></tr><tr><td>15</td><td>88.92± 0.85</td><td>80.02± 0.29</td><td>91.33± 0.24</td><td>89.73± 0.73</td><td>91.34± 0.62</td><td>88.01± 0.73</td><td>91.02± 0.09</td><td>89.67± 0.13</td><td>95.23± 0.63</td><td>96.86± 0.34</td></tr><tr><td>10</td><td>90.01± 0.51</td><td>87.61± 0.62</td><td>93.16± 0.73</td><td>90.12± 0.25</td><td>92.41± 0.34</td><td>91.17± 0.58</td><td>92.13± 0.23</td><td>91.20± 0.27</td><td>96.59± 0.52</td><td>98.12± 0.31</td></tr><tr><td>5</td><td>92.37± 0.42</td><td>91.28± 0.38</td><td>94.89± 0.43</td><td>91.35± 0.57</td><td>94.07± 0.23</td><td>93.08± 0.46</td><td>94.78± 0.12</td><td>93.86± 0.18</td><td>98.05± 0.23</td><td>98.31± 0.16</td></tr></table>

TABLE 9 Test accuracy comparison under different sample distribution among individual classes. 

<table><tr><td>Dataset</td><td colspan="10">Test accuracy (%) ± standard deviations</td></tr><tr><td rowspan="2"> $D_{M}^{m}$ </td><td>FedAvg</td><td>Loss-based</td><td>FOCUS</td><td>CAreFL</td><td>FocalLoss</td><td>ImpCSS</td><td>ActPerFL</td><td>FedNest</td><td>FedCSS</td><td>FedMW-CSS</td></tr><tr><td>96.20± 0.34</td><td>91.33± 2.69</td><td>96.33± 0.13</td><td>95.47± 2.62</td><td>94.88± 0.93</td><td>95.02± 0.07</td><td>94.87± 0.14</td><td>94.15± 0.27</td><td>97.84± 0.17</td><td>98.25± 0.21</td></tr><tr><td> $D_{C}^{m}$ </td><td>39.01± 0.24</td><td>39.04± 1.72</td><td>38.13± 0.62</td><td>31.08± 0.40</td><td>37.12± 1.29</td><td>37.33± 0.45</td><td>36.75± 0.26</td><td>35.87± 0.51</td><td>47.20± 0.56</td><td>49.32± 0.28</td></tr></table>

![](images/b1fca2bcb683777705af84871746633c3a6f5dcc5af708f59044584431fcbd9b.jpg)



(a) Test accuracy, Fed-MNIST

![](images/d0886fe92a9cf44754a65d848458835eb65b9174e677db110cc92e8548dff2d5.jpg)



(b) Test accuracy, Fed-CF10

![](images/4f1b860e2c2e305ea53650ca62b0884961eef20eaef6facd8d00b1ee29cbac37.jpg)



(c) Computation cost, Fed-MNIST

![](images/1365c18035638ebb520780ac59888156a060c38b9bffb39d69c80329be997e87.jpg)



(d) Communication cost, Fed-MNIST   
Fig. 10. The performance of models trained on datasets with mislabeling ratios of 40% for a large number of clients.

# 5.4 Sensitivity Analysis

Impact of noise ratio r. We investigate how robust FedMW-CSS is against a variety of noise levels from 0.1 to 0.7. We train Fed-MNIST, Fed-CF10 on $D _ { M } ^ { m }$ and $D _ { C } ^ { m }$ with different ratios of mislabeled samples. The results are shown in Table 7. It can be observed that FedMW-CSS achieves the highest test accuracy in almost all cases. For instance, with a noise ratio of 0.1, the test accuracy of Fed-CF10 trained with FedMW-CSS is 4.32% higher than the best performing baseline. For the only case where FedMW-CSS performs second best with the ratio being 0.1 on $\operatorname { F e d - M N I S T } ,$ in which the performance of FedMW-CSS is comparable to that of FOCUS. In addition, the test accuracy of FedMW-CSS only drops 1.65% when the noise ratio is increased from 0.1 to 0.7 of $D _ { M } ^ { m }$ , whereas that of the other six methods dropped by between 6.31% to 12.54%. In summary, FedMW-CSS is highly robust against different noisy data ratios.

Impact of $( \rho , \delta ) \mathbf { - D P }$ values. We show the superior performance of FedMW-CSS under DP noise settings. We train models under different noise levels, $i . e . ,$ with different $\sigma$ values from the Gaussian distribution ${ \mathcal { N } } ( 0 , \sigma ^ { 2 } )$ given various ρ values and $\delta = 1 0 ^ { - 4 }$ . The test accuracy of different training rounds are shown in Fig. 8(a). It shows that as noise increases, $i . e . , \rho$ decrease, the test accuracy decreases gradually, and the model converges slower. Besides, with some moderate noises, the drop in test accuracy is much small, e.g., 0.01%, 0.34% with $\rho = 8 , 1 0$ . We also present the test accuracy for different $( \rho , \delta ) { \cdot } \mathrm { D P }$ pairs in Fig. 8(b), where each curve corresponds to the test accuracy for different $\rho$ values and a fixed δ as it varies between $1 0 ^ { - 5 }$ and $\mathrm { i 0 ^ { - 2 } }$ . It shows that FedMW-CSS achieves high test accuracy under moderate privacy guarantees, e.g., it achieves 96.89%, 96.01% accuracy with $\rho = 4$ and $\delta = 1 \breve { 0 } ^ { - 3 } , 1 0 ^ { - 2 }$ .

Impact of imbalanced distribution. We use MNIST dataset and subsample it to generate a class-imbalanced dataset that reduces the number of training samples per class according to an exponential function $n \ = \ n _ { i } v _ { i }$ , where i is the class index, $n _ { i }$ is the original number of training images of class i and $v _ { i } ~ \in ~ [ 0 , 1 ]$ . The imbalance factor is defined as the number of training samples in the largest class divided by that of the smallest class. Table 8 presents the test accuracy of Fed-MNIST under different methods. It shows that even when the dataset is imbalanced, the balanced validation set enables FedMW-CSS to achieve higher test accuracy than all baselines. Similarly, we generate the imbalanced validation set using CIFAR-10 and present the test accuracy of the trained Fed-CF10 models with noise ratios $r ~ = ~ 0 . 2 , 0 . 4$ in Fig. $^ { 6 , }$ when the imbalance factor of the validation set is varied from 2 to 5. It shows that as the imbalance factor increases, the test accuracy decreases slightly.

Impact of the size of validation set, M . We further investigate how FedMW-CSS behaves as the size of validation set varies to explore the tradeoff between model performance and acquisition cost for the validation set. Fig. 8(c) presents the test accuracy of the trained Fed-CF10 models on $D _ { C } ^ { m }$ with noise ratios $r = 0 . 2 , 0 . 4$ , with the size of validation set varying from 0 to 4,000. It shows that using 20 validation samples on the server for all classes brings 1.2% and 6.87% performance improvement, respectively. The test accuracy stops increasing after the validation size increases beyond 1,000. Thus, FedMW-CSS can achieve good FL model performance using a small validation set, which is advantageous in real-world application as it incurs low data acquisition.

Impact of non-iid degree c. We also evaluate how FedMW-CSS behaves as the non-iid degree c is varied from 1 to $^ { 9 , }$ where c indicates the non-iid setting category number for each client. Fig. 8(d) presents the test accuracy of the trained Fed-MNIST models on dataset $D _ { M } ^ { m }$ with noise ratio r = 0.4. It can be observed that FedMW-CSS achieves the highest test accuracy in almost all cases, and is highly robust against different non-iid degree settings.

# 5.5 Large-scale Experiment Results

To evaluate the scalability of FedMW-CSS, we conduct largescale client engagement experiments for training models with 100 to 1,000 clients, $\bar { D _ { C } ^ { m } }$ with 100 to 500 clients and $D _ { K } ^ { m }$ with 100 to 10,000 clients. We present the test accuracy of models Fed-MNIST, Fed-CF10 with different number of clients in Fig. 10(a), 10(b). Fig. 10(a) shows that the test accuracy of FedMW-CSS is consistently high, e.g., above 95.0% for $D _ { M } ^ { m } ,$ , as the number of client increases to 1,000 and outperforms all baselines. As an example, in the 1,000 client setting of $D _ { M } ^ { m }$ , the average test accuracy of FedMW-CSS is 1.05% higher than the best performing baseline. Further, we present two examples of computation and communication costs for each local client under 500 and 1,000 client settings of Fed-MNIST in Fig. 10(c), 10(d), and the costs of other settings are quite similar in Fig. 10(c), 10(d). Similarly, we use the early stop strategy in which we run FL either until a pre-specified test accuracy (e.g., 95.0%) is reached for 10 consecutive communication rounds, or until a maximum number of rounds $( e . g .$ , 500 rounds) have elapsed. The results show that FedMW-CSS significantly saves both computation and communication costs. For example, in the 1,000 client setting, FedCSS and FedMW-CSS achieve 53.05%, 66.35% lower runtime and 27.54%, 39.0% lower communication cost than the best performing baseline. In summary, under large-scale experiment settings, FedMW-CSS still achieves the highest test accuracy most efficiently.

# 6 CONCLUSIONS AND FUTURE WORK

In this work, we proposed an efficient bilevel optimization approach, FedMW-CSS, for jointly selecting high quality FL clients and high quality local data samples in order to build high-performance FL models. It leverages metalearning based online approximation to iteratively update the global FL model, while selecting the most positively influential samples in the presence of training set biases in a privacy-preserving manner. To utilize class-level information, we propose to generalize data weighting from instance level to class level by reweighting gradient flows. Besides, the proposed hierarchical analysis technique helps it reduce unnecessary influence computation, thereby saving both the computation and communication overhead. To the best of our knowledge, it is the first FL approach which is simultaneously hard sample-aware and noise-robust. Its working mechanism of boosting the selection probabilities of the positively influential data owners and samples, while suppressing those for biased ones is interpretable.

# ACKNOWLEDGMENTS

This research is supported by Nanyang Technological University (NTU), under SUG Grant (020724-00001); the National Research Foundation, Prime Ministers Office, National Cybersecurity R&D Program (No. NRF2018NCR-NCR005-0001), NRF Investigatorship NRF-NRFI06-2020- 0001; the National Research Foundation, Singapore and DSO National Laboratories under the AI Singapore Programme (AISG Award No: AISG2-RP-2020-019); Alibaba Group through Alibaba Innovative Research (AIR) Program and Alibaba-NTU Singapore Joint Research Institute (JRI) (Alibaba-NTU-AIR2019B1), NTU, Singapore; the RIE 2020 Advanced Manufacturing and Engineering Programmatic Fund (No. A20G8b0102), Singapore; NTU Nanyang Assistant Professorship, Future Communications Research & Development Programme (FCP-NTU-RG-2021-014), the National Key R&D Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, and “the Fundamental Research Funds for the Central Universities” WK2150110024.

# REFERENCES

[1] B. McMahan, E. Moore, and Ramage, “Communication-efficient learning of deep networks from decentralized data,” in ICML, 2017.   
[2] A. Li, L. Zhang, F. Han, and X.-Y. Li, “Privacy-preserving efficient federated-learning model debugging,” IEEE Transactions on Parallel and Distributed Systems, vol. 33, no. 10, pp. 2291–2303, 2021.   
[3] M. Hu, E. Cao, H. Huang, M. Zhang, X. Chen, and M. Chen, “Aiotml: A unified modeling language for aiot-based cyberphysical systems,” IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, 2023.   
[4] M. Hu, Z. Xia, D. Yan, Z. Yue, J. Xia, Y. Huang, Y. Liu, and M. Chen, “Gitfl: Uncertainty-aware real-time asynchronous federated learning using version control,” in 2023 IEEE Real-Time Systems Symposium (RTSS). IEEE, 2023, pp. 145–157.   
[5] G. Wang, H. Guo, A. Li, X. Liu, and Q. Yan, “Federated iot interaction vulnerability analysis,” in 2023 IEEE 39th International Conference on Data Engineering (ICDE). IEEE, 2023, pp. 1517–1530.   
[6] J. Tan, L. Zhang, Y. Liu, A. Li, and Y. Wu, “Residue-based label protection mechanisms in vertical logistic regression,” in 2022 8th International Conference on Big Data Computing and Communications (BigCom). IEEE, 2022, pp. 356–364.   
[7] I. Dayan, H. R. Roth, A. Zhong, A. Harouni, A. Gentili, A. Z. Abidin, A. Liu, A. B. Costa, B. J. Wood, C.-S. Tsai et al., “Federated learning for predicting clinical outcomes in patients with covid-19,” Nature medicine, vol. 27, no. 10, pp. 1735–1743, 2021.   
[8] A. Li, Y. Chen, J. Zhang, M. Cheng, Y. Huang, Y. Wu, A. T. Luu, and H. Yu, “Historical embedding-guided efficient large-scale federated graph learning,” Proceedings of the ACM on Management of Data, vol. 2, no. 3, pp. 1–24, 2024.   
[9] A. Katharopoulos and F. Fleuret, “Not all samples are created equal: Deep learning with importance sampling,” in International conference on machine learning. PMLR, 2018, pp. 2525–2534.   
[10] Y. Cheng, L. Zhang, and A. Li, “Gfl: Federated learning on noniid data via privacy-preserving synthetic data,” in 2023 IEEE International Conference on Pervasive Computing and Communications (PerCom). IEEE, 2023, pp. 61–70.   
[11] A. Li, H. Peng, L. Zhang, J. Huang, Q. Guo, H. Yu, and Y. Liu, “Fedsdg-fs: Efficient and secure feature selection for vertical federated learning,” in IEEE INFOCOM 2023-IEEE Conference on Computer Communications. IEEE, 2023, pp. 1–10.   
[12] A. Li, L. Zhang, J. Wang, J. Tan, F. Han, Y. Qin, N. M. Freris, and X.-Y. Li, “Efficient federated-learning model debugging,” in IEEE ICDE. IEEE, 2021, pp. 372–383.   
[13] F. Lai, X. Zhu, H. V. Madhyastha, and M. Chowdhury, “Oort: Efficient federated learning via guided participant selection,” in 15th {USENIX} Symposium on Operating Systems Design and Implementation ({OSDI} 21), 2021, pp. 19–35.   
[14] Y. J. Cho, J. Wang, and G. Joshi, “Client selection in federated learning: Convergence analysis and power-of-choice selection strategies,” arXiv preprint arXiv:2010.01243, 2020.   
[15] A. Li, L. Zhang, J. Tan, Y. Qin, and X.-Y. Li, “Sample-level data selection for federated learning,” in IEEE INFOCOM 2021-IEEE Conference on Computer Communications. IEEE, 2021, pp. 1–10.   
[16] J. Shin, Y. Li, Y. Liu, and S.-J. Lee, “Sample selection with deadline control for efficient federated learning on heterogeneous clients,” arXiv preprint arXiv:2201.01601, 2022.   
[17] Z. Liu, Y. Chen, Y. Zhao, H. Yu, Y. Liu, R. Bao, J. Jiang, Z. Nie, Q. Xu, and Q. Yang, “Contribution-aware federated learning for smart healthcare,” in Proceedings of the 34th Annual Conference on Innovative Applications of Artificial Intelligence (IAAI-22), 2022.   
[18] J. Wang, L. Zhang, and H. Cheng, “Efficient participant contribution evaluation for horizontal and vertical federated learning,” in IEEE ICDE. IEEE, 2022, pp. 911–923.   
[19] H. Wang, Z. Kaplan, D. Niu, and B. Li, “Optimizing federated learning on non-iid data with reinforcement learning,” in IEEE IN-FOCOM 2020-IEEE Conference on Computer Communications. IEEE, 2020, pp. 1698–1707.   
[20] M. Ribero and H. Vikalo, “Communication-efficient federated learning via optimal client sampling,” arXiv preprint arXiv:2007.15197, 2020.   
[21] L. Nagalapatti and R. S. Mittal, “Is your data relevant?: Dynamic selection of relevant data for federated learning,” 2022.   
[22] A. Li, Y. Cao, J. Guo, H. Peng, Q. Guo, and H. Yu, “Fedcss: Joint client-and-sample selection for hard sample-aware noise-robust federated learning,” Proceedings of the ACM on Management of Data, vol. 1, no. 3, pp. 1–24, 2023.

[23] Y. Bengio, J. Louradour, R. Collobert, and J. Weston, “Curriculum learning,” in Proceedings of the 26th annual international conference on machine learning, 2009, pp. 41–48.   
[24] A. Graves, M. G. Bellemare, J. Menick, R. Munos, and K. Kavukcuoglu, “Automated curriculum learning for neural networks,” in international conference on machine learning. PMLR, 2017, pp. 1311–1320.   
[25] J. Byrd and Z. Lipton, “What is the effect of importance weighting in deep learning?” in International Conference on Machine Learning. PMLR, 2019, pp. 872–881.   
[26] G. Alain, A. Lamb, C. Sankar, A. Courville, and Y. Bengio, “Variance reduction in sgd by distributed importance sampling,” arXiv preprint arXiv:1511.06481, 2015.   
[27] M. Ren, W. Zeng, B. Yang, and R. Urtasun, “Learning to reweight examples for robust deep learning,” in International conference on machine learning. PMLR, 2018, pp. 4334–4343.   
[28] C. Zhu, W. Chen, T. Peng, Y. Wang, and M. Jin, “Hard sample aware noise robust learning for histopathology image classification,” IEEE Transactions on Medical Imaging, vol. 41, no. 4, pp. 881– 894, 2021.   
[29] L. Jiang, Z. Zhou, T. Leung, L.-J. Li, and L. Fei-Fei, “Mentornet: Learning data-driven curriculum for very deep neural networks on corrupted labels,” in International conference on machine learning. PMLR, 2018, pp. 2304–2313.   
[30] B. Han, Q. Yao, X. Yu, G. Niu, and Xu, “Co-teaching: Robust training of deep neural networks with extremely noisy labels,” Advances in neural information processing systems, vol. 31, 2018.   
[31] R. Balakrishnan, T. Li, T. Zhou, N. Himayat, V. Smith, and J. Bilmes, “Diverse client selection for federated learning via submodular maximization,” in International Conference on Learning Representations, 2021.   
[32] T. Tuor, S. C. Wang, and K. K. Leung, “Data selection for federated learning with relevant and irrelevant data at clients,” 2020.   
[33] T. Tuor, S. Wang, B. J. Ko, C. Liu, and K. K. Leung, “Overcoming noisy and irrelevant data in federated learning,” in 2020 25th International Conference on Pattern Recognition (ICPR). IEEE, 2021, pp. 5020–5027.   
[34] A. Li, J. Huang, J. Jia, H. Peng, L. Zhang, L. A. Tuan, H. Yu, and X.-Y. Li, “Efficient and privacy-preserving feature importancebased vertical federated learning,” IEEE Transactions on Mobile Computing, 2023.   
[35] J. Lorraine, P. Vicol, and D. Duvenaud, “Optimizing millions of hyperparameters by implicit differentiation,” in International Conference on Artificial Intelligence and Statistics. PMLR, 2020, pp. 1540–1552.   
[36] P. W. Koh and P. Liang, “Understanding black-box predictions via influence functions,” in International conference on machine learning. PMLR, 2017, pp. 1885–1894.   
[37] D. A. Tarzanagh, M. Li, C. Thrampoulidis, and S. Oymak, “Fednest: Federated bilevel, minimax, and compositional optimization,” arXiv preprint arXiv:2205.02215, 2022.   
[38] J. Peng, Z. Chen, Y. Shao, Y. Shen, L. Chen, and J. Cao, “Sancus: sta le n ess-aware c omm u nication-avoiding full-graph decentralized training in large-scale graph neural networks,” Proceedings of the VLDB Endowment, vol. 15, no. 9, pp. 1937–1950, 2022.   
[39] R. D. Cook and S. Weisberg, “Characterizations of an empirical influence function for detecting influential cases in regression,” Technometrics, vol. 22, no. 4, pp. 495–508, 1980.   
[40] P. W. W. Koh, K.-S. Ang, H. Teo, and P. S. Liang, “On the accuracy of influence functions for measuring group effects,” Advances in neural information processing systems, vol. 32, 2019.   
[41] Pytorch, “Pytorch,” Public online, 2022. [Online]. Available: https://pytorch.org/   
[42] Y. LeCun, “The mnist database of handwritten digits,” http://yann.lecun.com/exdb/mnist/.   
[43] S. Caldas, S. M. K. Duddu, P. Wu, T. Li, J. Konecnˇ y, H. B. \` McMahan, V. Smith, and A. Talwalkar, “Leaf: A benchmark for federated settings,” arXiv preprint arXiv:1812.01097, 2018.   
[44] S. M. K. D. Sebastian Caldas, “Leaf: A benchmark for federated settings,” https://leaf.cmu.edu/.   
[45] A. Krizhevsky, G. Hinton et al., “Learning multiple layers of features from tiny images,” semanticscholar, 2009.   
[46] A. K. et al, “Cifar-100 dataset,” cs.toronto.edu/ kriz/cifar.html.   
[47] T. U. K. Archive, “Kdd cup 1999 data data set,” https://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html.   
[48] A. Gulli, “Ag’s corpus of news articles,” http://groups.di.unipi.it/gulli/AG-corpus-of-news-articles.html.

[49] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2016, pp. 770–778.   
[50] M. Riedmiller and A. Lernen, “Multi layer perceptron,” Machine Learning Lab Special Lecture, University of Freiburg, pp. 7–24, 2014.   
[51] B. Trevett, “Sentiment analysis,” https://github.com/bentrevett/pytorchsentiment-analysis/blob/master/6%20- %20Transformers%20for%20Sentiment%20Analysis.ipynb.   
[52] Y. Chen, X. Yang, X. Qin, H. Yu, B. Chen, and Z. Shen, “Focus: Dealing with label quality disparity in federated learning,” arXiv preprint arXiv:2001.11359, 2020.   
[53] T.-Y. Lin, P. Goyal, R. Girshick, K. He, and P. Dollar, “Focal loss ´ for dense object detection,” in Proceedings of the IEEE international conference on computer vision, 2017, pp. 2980–2988.   
[54] H. Chen, J. Ding, E. Tramel, S. Wu, A. K. Sahu, S. Avestimehr, and T. Zhang, “Actperfl: Active personalized federated learning,” 2022.   
[55] R. C. Geyer, T. Klein, and M. Nabi, “Differentially private federated learning: A client level perspective,” arXiv preprint arXiv:1712.07557, 2017.   
[56] C. Xie, S. Koyejo, and I. Gupta, “Asynchronous federated optimization,” arXiv preprint arXiv:1903.03934, 2019.   
[57] C. Dwork, A. Roth et al., “The algorithmic foundations of differential privacy,” Foundations and Trends® in Theoretical Computer Science, vol. 9, no. 3–4, pp. 211–407, 2014.   
[58] Y. Li, Y. Shen, and L. Chen, “Camel: Managing data for efficient stream learning,” in Proceedings of the 2022 International Conference on Management of Data, 2022, pp. 1271–1285.

![](images/fb6792540cb3be2dfd707a73cf0f252e5fc44d18c15418b3c5f5d51cba954830.jpg)



Jianfei Sun is currently a Research Fellow with the School of Computer Science and Engineering, Nanyang Technological University, Singapore. He received his Ph.D. degree from University of Electronic Science and Technology of China, China. His research interests include federated learning and IoT data management.

![](images/da4c7078035f55a64d0edf4127e74dd6f371b0bd22179bc279f45f3e05af1ea1.jpg)



Lan Zhang is currently a Professor at the School of Computer Science and Technology, University of Science and Technology of China. She received her Ph.D degree and Bachelor degree from Tsinghua University, China. Her research interests include mobile computing, privacy protection, and data sharing and trading.

![](images/75bcbab4083d5009b43eb73c47fef0572f60b2526757e339f586d4e59c4a9be5.jpg)



Anran Li is a research fellow in the School of Computer Science and Engineering, Nanyang Technological University, Singapore. She received her Ph.D. degree from University of Science and Technology of China, China, in 2021. Her research interests mainly focus on data quality assessment, federated learning, interpretation and mobile computing.

![](images/34c93da304f77ed1b21a9eb860bcecd85b1869a6d4518334c51839b9b7ae8c61.jpg)



Guangjing Wang is currently pursuing the Ph.D. degree at School of Computer Science and Engineering, Nanyang Technological University, Singapore. His research interests include AI security and privacy, deep reinforcement learning, computer vision and pre-trained language model. He received the B.E. degree from the University of Electronic Science and Technology of China in 2015, and the M.E. degree from Tianjin University in 2019.

![](images/66fe7116511daa0e67bc2b825b218e5cdae3fb9355ea514c060fe6e48727f116.jpg)



Luu Anh Tuan is currently an Assistant Professor at Nanyang Technological University, Singapore. Prior than that, he was a Research Fellow at MIT from 2018 to 2020. Luu’s research interests lie in the intersection of AI, Deep Learning, and NLP. Dr. Luu also served as the Senior Area Chair of EMNLP 2020, Area Chair of ACL 2021-2023, Area Chair of ICLR 2022, Area Chair of NeurIPS 2023, Senior Program Committee of IJCAI 2020-2021, and Program Committee member of ICLR, ICML, AAAI, etc.

![](images/89bc9a879944dc455c646d0fb6e7553ab5dfc44e76b4df857aa76612d92071db.jpg)



Ming Hu is a research fellow in the School of Computer Science and Engineering, Nanyang Technological University, Singapore. He received his Ph.D. and B.E. degree from the School of Computer Science and Software Engineering, East China Normal University, Shanghai, China, in 2022 and 2017. His research interests include federated learning, program analysis, design automation of cyber-physical systems, and software testing.

![](images/a06205d235f49bf5523f9aaf622bf2f52ab14a5251448fe7e991a870943eb7d0.jpg)



Han Yu is a Nanyang Assistant Professor in the School of Computer Science and Engineering, Nanyang Technological University (NTU), Singapore. He held the prestigious Lee Kuan Yew Post-Doctoral Fellowship from 2015 to 2018. He obtained his PhD from the School of Computer Science and Engineering, NTU. His research focuses on federated learning and algorithmic fairness. His research works have won multiple awards from conferences and journals. He is a Senior Member of AAAI, CCF and IEEE.

# APPENDIX A ANALYTICAL EVALUATION

Here, we first analyze the privacy property of FedMW-CSS. Then, we show that, under mild conditions, FedMW-CSS achieves a convergence rate of ${ \cal O } ( 1 / \varepsilon ^ { 2 } )$ , where $0 \leqslant \varepsilon \leqslant 1$ is a constant.

# A.1 Privacy Preservation

FedMW-CSS preserves each client’s local training data from exposure to other parties, including the FL server, during the selection and updating processes. Firstly, the training process of FL models and meta models strictly follows the standard FL training protocol. Hence, no local training data are transmitted during training [1]. Secondly, during the sample selection process, no local training data are transmitted. During the client selection process, the clients transmit the weights (influence scores) to the FL server without revealing the raw data or the loss distribution of individual samples. In scenarios where even a client’s weight raises privacy concerns, clients can add noise to their weight values before uploading them, similar to existing local differential privacy (DP) approaches [55]. [56]

We propose a differentially private FedMW-CSS method to prevent the transmission parameters $( e . g . \mathrm { ~ }$ , local client weights) from leaking clients’ data information during the training and selection procedure. Specifically, we mask the client weight $\boldsymbol { W } _ { t } ^ { k }$ via a differentially private mechanism with a additive noise calibrated to $W _ { t } ^ { k \prime } \mathbf { s }$ sensitivity $\boldsymbol { S _ { W } }$ . Here, $\begin{array} { r } { S _ { W } ~ = ~ \mathrm { m a x } _ { z _ { k , i } , z _ { k , i } ^ { \prime } } | { \frac { 1 } { n _ { k } } } \sum _ { i = 1 } ^ { n _ { k } } ( \dot { e } ( l ( z _ { k , i } ) ; \theta _ { t } ) - \dot { e } ( l ( z _ { k , i } ^ { \prime } ) ; \theta _ { t } ) ) | } \end{array}$ |, where $z _ { k , i }$ and $z _ { k , i } ^ { \prime }$ are neighboring inputs, $k \in [ K ]$ and $i \in n _ { k }$ . Since the output weight $e ( l ( \bar { z } _ { k , i } ) ; \theta _ { t } )$ is within $[ 0 , 1 ] ,$ , the sensitivity $\boldsymbol { S _ { W } }$ equals to one. Thus, client k can add noise $\mathcal { N } ( 0 , \sigma ^ { \tilde { 2 } } )$ to the weight $\it { W _ { k } ^ { t } }$ before uploading them to the server. If we choose σ to be $\sqrt { 2 \ln { 1 . 2 5 } / { \delta } } / { \rho } ,$ then by standard augment [57], FedMW-CSS achieves $( \rho , \delta ) \ – \mathrm { D P } .$

# A.2 Convergence Analysis

We present convergence analysis results for FedMW-CSS. For simplicity, we denote the loss function $l ( z _ { k , i } ; \theta )$ of sample $z _ { k , i }$ as $l _ { k , i } ,$ and $l ( z _ { i } ^ { v } ; \theta )$ of validation sample $z _ { i } ^ { v }$ as $l _ { i } ^ { v } ,$ respectively.

Assumption 3. The validation loss functions are β-Lipschitz continuous with $| | \nabla l _ { i } ^ { v } - \nabla l _ { j } ^ { v } | | \leqslant \beta | | \dot { z _ { i } ^ { v } } - z _ { j } ^ { v } | | , \forall z _ { i } ^ { v } , z _ { j } ^ { v } \in D _ { v } .$ .

Assumption 4. The loss function $L _ { k } , k \in [ K ]$ has σ-bounded gradients with $\begin{array} { r } { \big | \big | \nabla L _ { k } ( \theta ) \big | \big | \leqslant \sigma } \end{array}$ .

FedMW-CSS leverages useful information from both the training set and validation set, and converges to an appropriate distribution favored by the validation set. This helps it achieve improved generalization and robustness against biases in the training set (as illustrated in our experiments).

Lemma 2. (Convergence of FedMW-CSS.) Under the above ns, and let the learning rate  , the validation loss monoto $\eta _ { k }$ for client k satisfiesally decreases for any $\eta _ { k } \leqslant \frac { 2 b _ { k } } { \beta \sigma ^ { 2 } }$ sequence of training batches,

$$
L _ {v} (\theta_ {t + 1}) \leqslant L _ {v} (\theta_ {t}), \tag {22}
$$

where $\begin{array} { r } { L _ { v } ( \theta _ { t } ) \ = \ \frac { 1 } { M } \sum _ { i = 1 } ^ { M } l _ { i } ^ { v } ( \theta _ { t } ( P , p ) ) } \end{array}$ is the total validation loss. Besides, in expectation, the equality in Eq. (22) holds only when the gradient $\nabla L _ { v } ( \theta _ { t } ) = \mathrm { ~ 0 ~ }$ at some step t, namely $\mathbb E _ { t } [ \bar { L } _ { v } ( \theta _ { t + 1 } ) ] = L _ { v } ( \theta _ { t } )$ if and only $i f \nabla L _ { v } ( \theta _ { t } ) = 0 ,$ , where the expectation is computed over all batches at step t.

Proof. Since $M \ll N$ , we assume that the validation dataset is a subset of the training dataset, and is distributed to client k. During training, client k takes a mini-batch ofsamples at each iteration. Then, the local para $b _ { k }$ traiters $\theta _ { t + 1 } ^ { k }$ are updated as:

$$
\theta_ {t + 1} ^ {k} = \theta_ {t} - \eta_ {k} \frac {1}{b _ {k}} \sum_ {i = 1} ^ {b _ {k}} \max \{\nabla L _ {v} ^ {\top} \nabla l _ {k, i}, 0 \} \nabla l _ {k, i}. \tag {23}
$$

The FL server aggregates updates from local clients, and applies the upd $\begin{array} { r } { \theta _ { t + 1 } = \frac { 1 } { u } \sum _ { k \in U _ { t } } \theta _ { t + 1 } ^ { k } } \end{array}$ . Since all gradients $\theta _ { t } ,$ $\theta _ { t }$ validation loss $L _ { v } ( \theta )$ is β-Lipschitz continuous, we have,

$$
L _ {v} (\theta_ {t + 1}) \leqslant L _ {v} (\theta_ {t}) + \nabla L _ {v} ^ {\top} \Delta \theta + \frac {\beta}{2} | | \Delta \theta | | ^ {2} \tag {24}
$$

Substituting Eq. (23) into Eq. (24), we have:

$$
L _ {v} (\theta_ {t + 1}) \leqslant L _ {v} (\theta_ {t}) - I _ {1} + I _ {2}, \tag {25}
$$

where,

$$
I _ {1} = \frac {1}{u} \sum_ {k \in U _ {t}} \eta_ {k} \frac {1}{b _ {k}} \sum_ {i = 1} ^ {b _ {k}} \max \{\nabla L _ {v} ^ {\top} \nabla l _ {k, i}, 0 \} ^ {2}, \tag {26}
$$

and,

$$
I _ {2} \leqslant \frac {\beta}{2 u} \sum_ {k \in U _ {t}} \frac {\eta_ {k} ^ {2}}{b _ {k} ^ {2}} \sum_ {i = 1} ^ {b _ {k}} \max \{\nabla L _ {v} ^ {\top} \nabla l _ {k, i}, 0 \} ^ {2} \sigma^ {2}. \tag {27}
$$

If we denote $\begin{array} { r } { \alpha _ { t } = \sum _ { i = 1 } ^ { b _ { k } } \operatorname* { m a x } \{ \nabla L _ { v } ^ { \top } \nabla l _ { k , i } , 0 \} ^ { 2 } } \end{array}$ for the t-th iteration, then:

$$
L _ {v} (\theta_ {t + 1}) \leqslant L _ {v} (\theta_ {t}) - \frac {1}{u} \sum_ {k \in U _ {t}} \frac {\eta_ {k}}{b _ {k}} \alpha_ {t} \left(1 - \frac {\beta \eta_ {k} \sigma^ {2}}{2 b _ {k}}\right). \tag {28}
$$

Note that by definition, $\alpha _ { t }$ is non-negative. Since $\begin{array} { r } { \eta _ { k } \leqslant \frac { 2 b _ { k } } { \beta \sigma ^ { 2 } } } \end{array}$ , it follows that $L _ { v } ( \theta _ { t + 1 } ) \leqslant L _ { v } ( \theta _ { t } )$ for any t. Then, we prove that $\mathbb { E } _ { t } [ \alpha _ { t } ] = 0$ if and only if $\nabla L _ { v } = \dot { 0 } ,$ , and $\mathbb { E } _ { t } [ \alpha _ { t } ] > 0$ if and only if $\nabla L _ { v } \neq 0 .$ , where the expectation is computed over all training batches in the t-th iteration. It is obvious that when $\nabla L _ { v } ^ { \smile } = 0 , \mathbb { E } _ { t } [ \alpha _ { t } ] = 0 . \operatorname { I f } \nabla L _ { v } \ne 0 .$ , we observe that there exists a validation sample $z _ { j } ^ { v } , j \in [ M ]$ such that $\nabla L _ { v } ^ { \top } \nabla l _ { j } ^ { v } > 0$ as follows:

$$
0 <   | | \nabla L _ {v} | | ^ {2} = \nabla L _ {v} ^ {\top} \nabla L _ {v} = \frac {1}{M} \sum_ {i = 1} ^ {M} \nabla L _ {v} ^ {\top} \nabla l _ {j} ^ {v}. \tag {29}
$$

Then, there exists a none-zero possibility p to sample a batch $B _ { k }$ that contains data $z _ { j } ^ { v }$ :

$$
\mathbb {E} _ {t} \left[ \alpha_ {t} \right] \geqslant p \sum_ {i \in B _ {k}} \max \left\{\nabla L _ {v} ^ {\top} \nabla l _ {i} ^ {v}, 0 \right\} ^ {2} \geqslant p \left\{\nabla L _ {v} ^ {\top} \nabla l _ {j} ^ {v}, 0 \right\} ^ {2}. \tag {30}
$$

Therefore, if we take expectation over the batch on both sides of Eq. (28), we can conclude that:

$$
\mathbb {E} _ {t} \big [ L _ {v} (\theta_ {t + 1}) \big ] \leqslant L _ {v} (\theta_ {t}), \tag {31}
$$

where the inequality holds if and only if ∇ $L _ { v } = 0$ . Thus, we have proven the convergence of FedMW-CSS.

Moreover, we can prove the convergence rate of FedMW-CSS is ${ \cal O } ( 1 / \varepsilon ^ { 2 } )$ .

Theorem 1. (Convergence rate of FedMW-CSS.) Suppose $L _ { v } , L _ { k }$ and ηk satisfy the above conditions, then FedMW-CSS achieves $\mathbb { E } [ | | \dot { \nabla } L _ { v } ( \dot { \theta _ { t } } ) | | ^ { 2 } ] \leqslant \varepsilon i n O ( 1 / \varepsilon ^ { 2 } )$ steps,

$$
\min _ {0 <   t <   T} \mathbb {E} [ | | \nabla L _ {v} (\theta_ {t}) | | ^ {2} ] \leqslant \frac {C}{\sqrt {T}}, \tag {32}
$$

where C is a constant. Thus, we can achieve the error ε in ${ \cal O } ( 1 / \varepsilon ^ { 2 } )$ steps compared to directly solving the Eq. (6).

Proof. From the proof of Lemma 2, we have:

$$
\frac {1}{u} \sum_ {k \in U _ {t}} \frac {\eta_ {k}}{b _ {k}} \mathbb {E} _ {0 \sim t} [ \alpha_ {t} ] (1 - \frac {\beta \eta_ {k} \sigma^ {2}}{2 b _ {k}}) \leqslant \tag {33}
$$

$$
\mathbb {E} _ {0 \sim t - 1} [ L _ {v} (\theta_ {t}) ] - \mathbb {E} _ {0 \sim t} [ L _ {v} (\theta_ {t + 1}) ].
$$

Here, ${ \mathbb E } _ { 0 \sim t }$ denotes that the expectation is computed over all batches from step 0 to t. Let $\begin{array} { r } { \bar { \zeta } = ( 1 - \frac { \beta \eta _ { k } \sigma ^ { 2 } } { 2 b _ { k } } ) \frac { \eta _ { k } ^ { - } } { b _ { k } } > 0 , } \end{array}$ βηkσ2 2bk ) ηk > 0, then, bk

$$
\zeta \sum_ {t = 0} ^ {T} \mathbb {E} _ {0 \sim t} [ \alpha_ {t} ] \leqslant \mathbb {E} _ {0} [ L _ {v} (\theta_ {0}) ] - \mathbb {E} _ {0 \sim T} [ L _ {v} (\theta_ {T + 1}) ] \tag {34}
$$

$$
\leqslant L _ {v} (\theta_ {0}) - L _ {v} (\theta^ {*}),
$$

where $L _ { v } ( \theta ^ { * } )$ is the global minimum of function $L _ { v }$ . Therefore, there exists an iteration ψ such that:

$$
\mathbb {E} _ {0 \sim \psi} [ \alpha_ {t} ] \leqslant \frac {L _ {v} (\theta_ {0}) - L _ {v} (\theta^ {*})}{\zeta T}. \tag {35}
$$

Then, we prove that the square of the gradient $\mathbb { E } _ { 0 \sim \psi - 1 } \big [ | | \nabla \tilde { L _ { v } } ( \theta _ { \psi } ) | | ^ { 2 } \big ]$ is smaller than $O ( 1 / \sqrt { T } )$ . Considering there are M none-zero sampling probabilities $\{ p _ { 1 } , p _ { 2 } , \cdots , p _ { M } \}$ to sample batches $\mathsf { \backslash } \{ B _ { 1 } , \bar { B } _ { 2 } , \cdots , B _ { M } \}$ such that $B _ { j }$ contains $x _ { j } ,$ and we denote $\begin{array} { r l } { p } & { { } = } \end{array}$ min $\{ p _ { 1 } , p _ { 2 } , \cdots , p _ { M } \}$ . Then, we have:

$$
\begin{array}{l} M \mathbb {E} _ {0 \sim \psi} [ \alpha_ {\psi} ] = \mathbb {E} _ {0 \sim \psi - 1} \bigg [ M \mathbb {E} _ {\psi} [ \alpha_ {\psi} ] \bigg ] \\ \geqslant \frac {p}{M} \left(\sum_ {i = 1} ^ {M} \mathbb {E} _ {0 \sim \psi - 1} \left[ \max \left\{\nabla L _ {v} ^ {\top} f _ {j}, 0 \right\} \right]\right) ^ {2} \tag {36} \\ \end{array}
$$

Therefore,

$$
\sum_ {i = 1} ^ {M} \mathbb {E} _ {0 \sim \psi - 1} [ \max \left\{\nabla L _ {v} ^ {\top} f _ {j}, 0 \right\} ] \leqslant M \sqrt {\frac {L _ {v} \left(\theta_ {0}\right) - L _ {v} \left(\theta^ {*}\right)}{p \zeta}} \sqrt {\frac {1}{T}}, \tag {37}
$$

and,

$$
\mathbb {E} _ {0 \sim \zeta - 1} [ | | \nabla L _ {v} (\theta_ {\zeta}) | | ^ {2} ] = \mathbb {E} _ {0 \sim \zeta - 1} [ | | \nabla L _ {v} ^ {\top} \frac {1}{M} \sum_ {i = 1} ^ {M} \nabla f _ {i} | | ^ {2} ] \tag {38}
$$

$$
\leqslant \sqrt {\frac {L _ {v} (\theta_ {0}) - L _ {v} (\theta^ {*})}{p \zeta}} \sqrt {\frac {1}{T}}
$$

Thus, we conclude that FedMW-CSS can achieve min $_ { 0 < t < T } \mathbb { E } [ | | \nabla L _ { v } ( \theta _ { t } ) | | ^ { 2 } ] \leqslant O ( \sqrt { 1 / T } )$ in T iterations.

# A.3 Comparison with Centralized Baselines

We compare our design with state-of-the-art works for centralized learning: Camel [58], which selects a coreset from each streaming data batch by solving the submodular maximization problem and uses the coreset for model updating. We use Camel and FedMW-CSS in centralized scenarios, named CentralSS, to train models on datasets $D _ { M } ^ { m }$ and $D _ { C } ^ { m }$ with various noise ratios. The results in Table 10 show that FedMW-CSS complements to the centralized work and achieves better performance.

TABLE 10 Test accuracy comparison with centralized baselines. 

<table><tr><td>Dataset</td><td>Method</td><td colspan="4">Test accuracy (%) ± standard deviations</td></tr><tr><td rowspan="3"> $D_{M}^{m}$ </td><td></td><td>0.1</td><td>0.3</td><td>0.5</td><td>0.7</td></tr><tr><td>Camel</td><td>98.35± 0.07</td><td>97.51± 0.02</td><td>96.89± 0.14</td><td>91.13± 0.31</td></tr><tr><td>CentralSS</td><td>98.89± 0.06</td><td>98.56± 0.03</td><td>98.42± 0.07</td><td>97.31± 0.05</td></tr><tr><td rowspan="2"> $D_{C}^{m}$ </td><td>Camel</td><td>80.03± 0.24</td><td>76.16± 0.57</td><td>69.52± 0.30</td><td>58.89± 0.12</td></tr><tr><td>CentralSS</td><td>89.78± 0.23</td><td>87.91± 0.18</td><td>80.95± 0.23</td><td>68.27± 0.46</td></tr></table>