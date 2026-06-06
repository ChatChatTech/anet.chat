# Differentially Private Distributed Online Convex Optimization Towards Low Regret and Communication Cost

Jiandong Liu, Lan Zhang, Xiaojing Yu, Xiang-Yang Li

University of Science and Technology of China

Hefei, China

jdliu@mail.ustc.edu.cn,zhanglan@ustc.edu.cn,yxjing@mail.ustc.edu.cn,xiangyangli@ustc.edu.cn

# ABSTRACT

Distributed online convex optimization (DOCO) has emerged as a promising approach in scenarios where multiple learners collaboratively serve sequential (possibly untrusted) clients using AI models. However, ensuring clients’ privacy and minimizing regret while keeping the communication cost reasonable poses a significant challenge. To address this issue, we propose private DOCO algorithms, termed PDOM, for both oblivious and stochastic settings. Our approach involves a mini-batch strategy that optimally balances the effects of slower model updates and differential privacy (DP) perturbation. Our theoretical analysis shows that compared to state-of-the-art algorithms, PDOM reduces the regret bounds and communication cost by an O (??/??) factor for the oblivious setting. For the stochastic setting, the impact of DP perturbation becomes negligible if the learning time $T = \Omega ( d ^ { 4 } / ( n \epsilon ^ { 4 } ) )$ ) provided that the loss functions are Lipschitz, convex, and smooth, where ?? is the model dimension, ?? is the number of learners, and ?? is the privacy budget. Our evaluations validate these results, demonstrating that PDOM can reduce classification error rates of the state-of-the-art methods by up to 20% in distributed online logistic regression tasks while achieving communication savings of above 90%.

# CCS CONCEPTS

• Networks → Network performance analysis; • Computing methodologies → Online learning settings; • Theory of computation → Online learning theory; Multi-agent learning; • Security and privacy → Privacy-preserving protocols.

# KEYWORDS

Distributed online convex optimization, differential privacy

# ACM Reference Format:

Jiandong Liu, Lan Zhang, Xiaojing Yu, Xiang-Yang Li. 2023. Differentially Private Distributed Online Convex Optimization Towards Low Regret and Communication Cost. In The Twenty-fourth International Symposium on Theory, Algorithmic Foundations, and Protocol Design for Mobile Networks and Mobile Computing (MobiHoc ’23), October 23–26, 2023, Washington, DC, USA. ACM, New York, NY, USA, 10 pages. https://doi.org/10.1145/3565287.3610257

Xiang-Yang Li is the corresponding author.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

MobiHoc ’23, October 23–26, 2023, Washington, DC, USA

© 2023 Copyright held by the owner/author(s). Publication rights licensed to ACM.

ACM ISBN 978-1-4503-9926-5/23/10. . . \$15.00

https://doi.org/10.1145/3565287.3610257

# 1 INTRODUCTION

Distributed online convex optimization (DOCO) [4, 17, 30] has proven to be an effective approach for collaborative learning using feedback data from a large number of sequential clients. The goal of the learners in DOCO is to acquire AI models with satisfactory utility while keeping the communication cost low. However, privacy considerations are also critical, as releasing service data to a client could reveal private information from previous clients’ feedbacks. For instance, in communication-constrained AIoT systems such as health management [18] and network monitoring [21], networked devices collaborate to improve their AI models’ quality of service. In such systems, it is crucial to ensure that the service data given to each client does not leak private information from other clients contributing feedback data to update models. Similarly, in distributed online diagnosis, multiple hospitals/clinics collaborate to improve their treatment strategies based on feedbacks from their patients [16]. However, directly adjusting the treatment strategy based on one patient’s feedback can reveal personal health information. In this context, ensuring privacy protection is crucial.

The current literature provides several private DOCO (PDOCO) algorithms [19, 29, 31] based on differential privacy (DP) [6]. Regret loss, which measures the utility of the models, is a standard metric used to analyze these algorithms. The current regret bounds match the state-of-the-art results for non-private algorithms [30] in the learner number ?? and learning time ?? . However, the regret loss increases sharply for scarce DP budgets ?? or high model dimensions ??, rendering these algorithms unsuitable for scenarios with stringent privacy requirements or high model dimensions. Furthermore, the communication costs of existing works are proportional to the network’s edge number and learning time, which makes them costly for applications with large networks and lengthy learning times.

To address these issues, this work proposes PDOCO algorithms with lower regret loss and communication cost. The regret loss is measured as the accumulated loss incurred by each learner’s models and that incurred by a fixed optimal model. The learners communicate through a connected undirected learner network, and the communication cost is evaluated based on the number of transmitted messages, i.e., the message complexity [3].

The regret loss in PDOCO is affected by both the model update strategy and the noise added to ensure differential privacy. If the learners do not effectively utilize the feedback data for updating their models, the resulting models may lead to higher regret loss. However, if the models contain too much sensitive feedback information, additional noise needs to be introduced to ensure privacy, which can also increase the regret loss. In addition to the regret loss, the model update strategy also impacts the communication cost of PDOCO algorithms.

Table 1: Regret bounds and communication cost for PDOCO. ?? is the DP budget, ?? is the dimension of the model, ?? is the number of learners, and ?? is the learning time. $\lambda _ { 2 } ( A ) \in [ 0 , 1 )$ is the second largest eigenvalue of the gossip matrix ?? of the learner network, as defined in [14]. The DOCO algorithm in the stochastic setting with Lipschitz and strongly convex loss functions is implemented using the no-communication algorithm from [4] with the gradient descent update rule from [10]. The original algorithm in [31] is for PDOCO with unconstrained feasible regions and additional assumptions on the DP noise. To enable a fair comparison, we project the updated models onto a constrained feasible region (cf. Theorem 1 with batch size ?? = 1). 

<table><tr><td rowspan="2">Feedback settings</td><td rowspan="2">Assumptions on loss functions</td><td colspan="2">DOCO (non-private) [4, 10, 30]</td><td colspan="2">SOTA for PDOCO [31]</td><td colspan="2">PDOM (our work)</td></tr><tr><td>Regret bound</td><td>Comm.</td><td>Regret bound</td><td>Comm.</td><td>Regret bound</td><td>Comm.</td></tr><tr><td rowspan="2">Oblivious</td><td>Lipschitz and convex</td><td> $O\left(\frac{n^{3/2}\sqrt{T}}{1-\lambda_2(A)}\right)$ </td><td> $O(n^2T)$ </td><td> $O\left(\frac{n^{3/2}d^2\sqrt{T}}{\epsilon^2(1-\lambda_2(A))}\right)$ </td><td> $O(n^2T)$ </td><td> $O\left(\frac{n^{3/2}d\sqrt{T}}{\epsilon(1-\lambda_2(A))}\right)$ </td><td> $O\left(\frac{\epsilon n^2T}{d}\right)$ </td></tr><tr><td>Lipschitz and strongly convex</td><td> $O\left(\frac{n^{3/2}\ln T}{1-\lambda_2(A)}\right)$ </td><td> $O(n^2T)$ </td><td> $O\left(\frac{n^{3/2}d^2\ln T}{\epsilon^2(1-\lambda_2(A))}\right)$ </td><td> $O(n^2T)$ </td><td> $O\left(\frac{n^{3/2}d\ln T}{\epsilon(1-\lambda_2(A))}\right)$ </td><td> $O\left(\frac{\epsilon n^2T}{d}\right)$ </td></tr><tr><td rowspan="2">Stochastic</td><td>Lipchitz, convex, and smooth</td><td> $O(n^2+\sqrt{nT})$ </td><td> $O(n^{5/3}T^{2/3})$ </td><td>-</td><td></td><td> $O\left(n^2+\sqrt{nT}+\frac{d^{2/3}(nT)^{1/3}}{\epsilon^{2/3}}\right)$ </td><td> $O\left(\frac{n^{5/3}(\epsilon T)^{2/3}}{d^{2/3}}\right)$ </td></tr><tr><td>Lipschitz and strongly convex</td><td> $O(n\ln T)$ </td><td>0</td><td>-</td><td></td><td> $O\left((n^2+\frac{d}{\epsilon})\ln T\right)$ </td><td> $O\left(\frac{\epsilon n^2T}{d}\right)$ </td></tr></table>

We aim to strike a balance between the regret incurred by model update strategies and the DP noise while also reducing the communication cost. To achieve this, we employ mini-batch model updates, where learners communicate and update models after collecting a batch of feedback data. Mini-batch updates are known to reduce the noise level required to ensure DP since fewer data are exposed [16]. However, existing works employ heuristic batch sizes and do not fully understand their impact. We recognize that, although reducing the noise level, mini-batch updates slow down the model updates, which results in extra regret loss. Hence, finding the optimal batch size that balances the noise level and model update speed is critical. Another advantage of the mini-batch algorithm is that it reduces the communication cost compared to the non-batch algorithm [16, 31] as learners communicate less frequently.

The main challenge to determining the optimal batch size in PDOCO is that it varies drastically for different learning and privacy parameters and feedback settings. To understand its dependence on parameter settings, we establish the regret bounds of PDOCO with all possible batch size ??, explicitly dependent on DP budgets ??, learner numbers ??, learning times ?? , and model dimensions ??. Consequently, the optimal batch size can be determined by minimizing the regret bounds with respect to ??. This leads to the development of the algorithm named PDOCO with the optimal mini-batch (PDOM). Besides the parameters, the optimal batch size also varies a lot for different feedback settings. Formally, we consider two popular feedback settings: oblivious and stochastic. The oblivious setting considers arbitrary feedbacks that are independent of historical models. This general setting covers applications where the feedbacks of different learners at different times vary drastically (e.g., distributed tracking of moving targets [2]). In this case, the optimal batch size is constant in ?? to avoid the current model performing poorly in the future. In the stochastic setting, all feedbacks follow a common distribution, often encountered in statistical learning [17]. This setting can tolerate larger batch sizes for larger ?? . Our algorithm for the stochastic setting features a distinct design from gossip-based algorithms in PDOCO literature [16, 31], offering reduced regret and communication cost compared to its oblivious counterpart.

Our PDOM algorithm offers significant theoretical advantages over existing state-of-the-art methods as summarized in Table 1. Specifically, in the oblivious setting, our approach reduces both the regret and communication cost by a factor of $O ( d / \epsilon )$ , where ?? is the model dimension and ?? is the DP budget. This reduction makes our PDOM algorithm particularly attractive in situations with strict privacy requirements or high-dimensional models. Additionally, we present the first PDOCO algorithm specifically designed for the stochastic setting. Our PDOM algorithm’s regret bound matches the non-private one for sufficiently large ?? , provided that the loss functions are Lipschitz, convex, and smooth. Moreover, similar to the oblivious setting, our PDOM algorithm is particularly communication-efficient when the model dimension ?? is high or the DP budget ?? is close to zero.

We evaluate our approach on network traffic and diagnosis datasets: KDDCup99[11] and Diabetes[24]. In the oblivious setting, our algorithm reduces classification error rates of existing methods by up to 20% with above 90% communication savings for tasks with varying DP budgets. In the stochastic setting, our algorithm achieves error rates similar to those of the non-private algorithm when the DP budget $\epsilon \geq 1$ and the regularization term is zero.

# 2 PRELIMINARIES

In this section, we formalize the problem setting.

Distributed online convex optimization (DOCO): In DOCO, ?? learners communicate in a connected undirected network. Each learner ?? ∈ [??] serves an incoming client at time $t \in [ T ]$ based on an AI model. The client then sends the feedback data $\xi _ { t } ^ { i }$ to learner ??.

![](images/c283dc71c2549e50369f6ec2c2a7cdf6fa8cb115f722094e11d38bc20406c8ff.jpg)



![](images/de34faae1374857e0aa23741f713bf4db32125c221dbb3bb28a6dd6d5260962e.jpg)



(b)   
Figure 1: System model of PDOCO. Fig. (a) is an example learner network; Fig. (b) is the service pattern of learner ??.

Learner ??’s model at time ?? is parameterized by $x _ { t } ^ { i } \in C \subset \mathbb { R } ^ { d }$ , where C is the feasible region. The performance of models at time ?? , i.e., $\boldsymbol { x } _ { t } ^ { i }$ for ?? ∈ [??], is measured by the loss function $f _ { t } ( \cdot ) = \Sigma _ { i = 1 } ^ { n } f _ { t } ^ { i } ( \cdot )$ where $f _ { t } ^ { i } ( \cdot ) = F ( \cdot ; \xi _ { t } ^ { i } )$ for some function ?? . At each time ?? , learner ?? can update $\boldsymbol { x } _ { t } ^ { i }$ based on $f _ { s } ^ { i }$ for $s \leq t$ and messages from neighbors in the learner network.

Private DOCO (PDOCO): In PDOCO, learners serve clients and update models similar to non-private DOCO. As to the privacy threat model, we assume the learners to be honest and not disclose any private information other than the released service data. On the other hand, clients are assumed to be semi-honest. They follow the learning algorithm but may try to infer other clients’ private information. We also assume all communication channels to be secure, such that an outside adversary cannot obtain private information via eavesdropping. In PDOCO, we need to ensure that the updated models over the learning time do not leak too much information related to $\xi _ { t } ^ { i }$ (or equivalently, $f _ { t } ^ { i } )$ for $i \in [ n ]$ and $t \in [ T ]$ .

In this work, we measure the privacy leakage using differential privacy (DP) [6]. DP considers two input collections, ?? and ??, as neighboring (denoted by $x \simeq y )$ if they differ in a single element. DP measures the privacy loss of an algorithm by comparing the distributions of its outputs on neighboring inputs.

Definition 1 (Differential Privacy). For $\epsilon \geq 0 .$ , an algorithm $\mathcal { A }$ is ??-differentially private if for all sets ?? and neighboring input collections $x \simeq y \mathrm { : }$

$$
\operatorname * {P r} [ \mathcal {A} (x) \in S ] \leq \exp (\epsilon) \operatorname * {P r} [ \mathcal {A} (y) \in S ]. \tag {1}
$$

Denote the loss sequence $\mathcal { F } \triangleq \{ f _ { t } ^ { i } \} _ { i \in [ n ] , t \in [ T ] }$ . We say a PDOCO algorithm A is ??-differentially private if for all ${ \bf \dot { \mathcal { F } } } \simeq \mathcal { F } ^ { \prime }$ , the distributions of $\mathcal { A } ( \mathcal { F } ) \triangleq \{ x _ { t } ^ { i } \} _ { t \in [ T ] , i \in [ n ] }$ and $\mathcal { A } ( \mathcal { F } ^ { \prime } )$ satisfy Eq. (1).

Performance metrics: We consider two typical feedback settings in PDOCO, oblivious and stochastic. In the oblivious setting, each feedback $\xi _ { t } ^ { i }$ is arbitrary but independent of historical models. Each learner ?? aims to minimize the expected regret loss [30, 31]:

$$
\mathcal {R} _ {i} (T) \triangleq \mathbb {E} \left[ \Sigma_ {t = 1} ^ {T} f _ {t} (x _ {t} ^ {i}) \right] - \min _ {x \in C} \Sigma_ {t = 1} ^ {T} f _ {t} (x). \tag {2}
$$

In the stochastic setting, each feedback $\xi _ { t } ^ { i }$ follows the same distribution P. We denote $\bar { F } ( x ) \triangleq \mathbb { E } _ { \xi \sim \mathbb { P } } [ F ( x ; \dot { \xi } ) ]$ . The performance of learner ?? is measured by the expected pseudo regret loss [4]:

$$
\bar {\mathcal {R}} _ {i} (T) \triangleq n \Sigma_ {t = 1} ^ {T} \mathbb {E} \left[ \bar {F} (x _ {t} ^ {i}) \right] - n T \min _ {x \in \mathcal {C}} \bar {F} (x). \tag {3}
$$

Another performance criterion in PDOCO is the communication cost. We measure the communication cost using message complexity [3], i.e., the number of messages transmitted in the algorithm.

Assumptions on loss functions: In this paper, we focus on loss functions satisfying the following standard assumptions [4, 16, 31].

Definition 2 (Lipschitz and strong convexity). A function ?? is ??-strongly convex and Lipschitz continuous inside a convex compact set C if for all $\begin{array} { r } { x , y \in C , f ( y ) - f ( x ) \geq \langle \nabla f ( x ) , y - x \rangle + \frac { \alpha } { 2 } \| y - x \| _ { 2 } ^ { 2 } } \end{array}$ and $| f ( x ) - f ( y ) | \leq L \left\| x - y \right\| _ { 2 }$ , where ??, $L > 0$ .

The Lipschitz and convexity assumption is a special case for $\alpha = 0$ in Definition 2.

Definition 3 (Smoothness). A function ?? is smooth if for ??, $y \in$ $C , \| \nabla f ( x ) - \nabla f ( y ) \| _ { 2 } \leq L _ { G } \left\| x - y \right\| _ { 2 } .$ , where $L _ { G } > 0$ .

In the oblivious setting, we assume that the loss functions $f _ { t } ^ { i } , i \in$ $[ n ] , t \ \in \ [ T ]$ satisfy Definition 2 with common ?? and ??. In the stochastic setting, we assume that the function $F ( \cdot ; \xi )$ for any $\xi \sim \mathbb { P }$ satisfies Definitions 2 and 3 with fixed $\alpha , L ,$ and $L _ { G }$ .

# 3 PDOCO WITH THE OPTIMAL MINI-BATCH

In this section, we present the design of our novel algorithm, PDOCO with the optimal mini-batch (PDOM), which simultaneously reduces the regret loss and communication cost of the current stateof-the-art method [31]. The algorithm’s update and service pattern is depicted in Figure 2. The main challenge in PDOM is identifying the optimal batch size ?? that yields the minimum regret bound. We introduce two variants of PDOM, namely PDOM-O and PDOM-S, for oblivious and stochastic settings, respectively. We provide a detailed analysis of these algorithms to determine their communication efficiency under different scenarios. Furthermore, as our algorithms are mini-batch versions of those in [4, 31], their computation cost at each time does not exceed that of existing algorithms.

![](images/91a1fc42ff2bd5bf36540ada1bd4c59b93755322c0f938d9823a7f8e67ce4a79.jpg)



Figure 2: Model update and service pattern of learner $i \in [ n ]$ in PDOM during the ??-th batch.

# 3.1 PDOM for the Oblivious Setting

We first introduce PDOM-O (Alg. 1), the algorithm designed for the oblivious setting, in which the feedbacks are arbitrary but independent of historical models. Initially, we compute the gossip matrix ?? as the input of PDOM-O, which represents a weighted adjacency matrix for the learner network, as previously introduced in the literature [15, 20]. PDOM-O determines the optimal batch size ?? based on the selection algorithm specified in Corollary 1. Every ?? timeslots, each learner communicates with their neighbors and averages their mini-batch gradients using ??. The learners then update their models using gradient descent with perturbed gradients to ensure differential privacy. PDOM-O reduces the communication cost of the non-batch algorithm [31] by a factor of ??.

We analyze PDOM-O with different batch sizes ?? in Theorem 2. The detailed proof is deferred to Section 4.1.

Theorem 1. PDOM-O satisfies ??-DP. If the loss functions satisfy Definition 2, by choosing ???? = 1?????? $\begin{array} { r } { \eta _ { k } = \frac { 1 } { \alpha k \tau } } \end{array}$ in Alg. 1, the regret bound for learner $i \in [ n ]$ is:

$$
\mathcal {R} _ {i} (T) = O \left(\frac {n ^ {3 / 2} L \| C \| _ {2}}{1 - \lambda_ {2} (A)} \left(\tau + \frac {d}{\epsilon}\right) + \frac {n ^ {3 / 2} L ^ {2} \ln T}{\alpha (1 - \lambda_ {2} (A))} \left(\tau + \frac {d ^ {2}}{\epsilon^ {2} \tau}\right)\right),
$$

where $\| C \| _ { 2 }$ ≜ max $x , y \in C \| x - y \| _ { 2 } ,$ and $\lambda _ { 2 } ( A )$ denotes the second largest eigenvalue of the gossip matrix ?? of the learner network.

If the loss functions satisfy Definition 2 with $\alpha = 0 .$ , by choosing $\eta _ { k } \equiv 1 / \sqrt { T }$ , the regret bound for learner $i \in [ n ]$ is:

$$
\mathcal {R} _ {i} (T) = O \left(\frac {n ^ {3 / 2} L \| C \| _ {2}}{1 - \lambda_ {2} (A)} \left(\tau + \frac {d}{\epsilon}\right) + \frac {n ^ {3 / 2} L ^ {2} \sqrt {T}}{1 - \lambda_ {2} (A)} \left(\tau + \frac {d ^ {2}}{\epsilon^ {2} \tau}\right) + n \| C \| _ {2} ^ {2} \sqrt {T}\right).
$$

Algorithm 1: PDOM for the Oblivious Setting (PDOM-O; run by each learner $i \in [n]$ )
Input: DP budget $\epsilon$ , convex set $C$ , and gossip matrix $A$ 1 Initialize $\hat{x}_1^i$ randomly from $C$ ;
2 Batch Selection: Compute $\tau = B(\epsilon, d) // B$ is a batch selection algorithm specified in Corollary 1;
3 for $k = 1$ to $\lceil T / \tau \rceil$ do
4    Initialize $g_k^i = 0$ ;
5    for $t = (k - 1)\tau + 1$ to min $\{k\tau, T\}$ do
6    Model Release: Respond with $x_t^i = \hat{x}_k^i$ to the client at time $t$ ; obtain $f_t^i$ from the client;
7    Gradient Summation: $g_k^i \leftarrow g_k^i + \nabla f_t^i (\hat{x}_k^i)$ ;
8    end
9    Model Averaging: Transmit $\hat{x}_k^i$ to learner $i$ 's neighbors at time min $\{k\tau, T\}$ ; compute $v_k^i = \Sigma_{j=1}^n A_{ji} \hat{x}_k^j$ ;
10    Model Update: $\hat{x}_{k+1}^i \leftarrow \Pi_C(v_k^i - \eta_k(g_k^i + b_k^i))$ , where $\Pi_C(x) \triangleq \arg \min_{y \in C} \|y - x\|_2$ and $b_k^i$ follows the $d$ -dimensional Laplace distribution with parameter $2\sqrt{d}L/\epsilon$ , denoted by $Lap^d(2\sqrt{d}L/\epsilon)$ ;
11 end

The communication cost of PDOM-O is $O ( n ^ { 2 } T / \tau )$ .

By choosing the batch size ?? optimally in Theorem 1, the regret bounds for PDOM-O are summarized in Corollary 1.

Corollary 1. In PDOM-O, choose $\tau = \Theta ( d / \epsilon )$ . If the loss functions satisfy Definition 2, the regret bound for learner ?? ∈ [??] is:

$$
\mathcal {R} _ {i} (T) = \mathcal {O} \bigg (\frac {n ^ {3 / 2} L d}{\epsilon (1 - \lambda_ {2} (A))} \bigg (\| C \| _ {2} + \frac {L}{\alpha} \ln T \bigg) \bigg),
$$

If the loss functions satisfy Definition 2 with $\alpha = 0 ,$ the regret bound for learner ?? ∈ [??] is:

$$
\mathcal {R} _ {i} (T) = O \left(\frac {n ^ {3 / 2} L d}{\epsilon \left(1 - \lambda_ {2} (A)\right)} \left(\| C \| _ {2} + L \sqrt {T}\right) + n \| C \| _ {2} ^ {2} \sqrt {T}\right).
$$

The communication cost of PDOM-O with $\begin{array} { r } { \tau = \Theta ( d / \epsilon ) \ i s { \cal O } ( \frac { \epsilon n ^ { 2 } T } { d } ) } \end{array}$

We provide an analysis of the regret incurred by PDOM-O for various batch sizes ?? in Theorem 1 and determine the optimal batch size in Corollary 1. Our results show that the optimal batch size for both convex and strongly convex loss functions is $\Theta ( d / \epsilon )$ , which aligns with our intuition. It is worth noting that differential privacy introduces more noise when the model dimension ?? is large or the privacy budget ?? is limited. Hence, a larger batch size is necessary to mitigate the impact of DP noise for larger ?? or smaller ??.

Impact of network topologies: In PDOM-O, the network topology affects the regret bound through the second largest eigenvalue $\lambda _ { 2 } ( A )$ of the gossip matrix ??. According to [20], for arbitrary connected networks, $1 / ( 1 - \lambda _ { 2 } ( A ) ) = O ( n ^ { 2 } )$ , implying that the regret loss scales as $O ( n ^ { 7 / 2 } )$ in terms of the number of learners ??. However, for special networks like fully-connected and expander ones [20], $1 / ( 1 - \lambda _ { 2 } ( A ) ) = O ( 1 )$ , resulting in a regret bound of $O ( n ^ { 3 / 2 } )$ in ??.

Comparison with existing works: PDOM-O significantly reduces both the regret bound and communication cost of the stateof-the-art non-batch algorithm [31] by a factor of $O ( d / \epsilon )$ . This reduction makes PDOM-O particularly suitable for tasks with high

Algorithm 2: PDOM for the Stochastic Setting (PDOM-S; run by each learner $i \in [n]$ )
Input: DP budget $\epsilon$ , convex set $C$ , runtime of vector-sum $\mu$ , and a random initial model $\hat{x}_1 \in C$ Batch Selection: Compute $\tau = B(\epsilon, d, \mu, n, T) // B$ is a selection algorithm specified in Corollary 2;
for $k = 1$ to $\lceil T / \tau \rceil$ do
Initialize $g_k^i = 0$ ;
for $t = (k - 1)\tau + 1$ to min $\{k\tau - \mu, T\}$ do
Model Release: Respond with $x_t^i = \hat{x}_k$ to the client at time $t$ ; obtain $f_t^i$ from the client;
Gradient Summation: $g_k^i \leftarrow g_k^i + \nabla f_t^i(\hat{x}_k)$ ;
end
Gradient Averaging: Call vector-sum to compute $\bar{g}_k = \frac{1}{n(\tau - \mu)} (\Sigma_{i=1}^n g_k^i + b_k)$ where $b_k$ follows Lapd(2√dL/ε);
set $x_t^i = \hat{x}_k$ from time min $\{k\tau - \mu + 1, T\}$ to min $\{k\tau, T\}$ ;
Model Update: $\hat{x}_{k+1} \leftarrow \Pi_C(\hat{x}_k - \eta_k \bar{g}_k)$ , where $\Pi_C(x) \triangleq \arg \min_{y \in C} \| y - x \|_2$ ;
end

model dimensions and strict privacy requirements. It is worth noting that the non-batch algorithm [31] is a special case of PDOM-O with ?? = 1, but this choice is sub-optimal according to Corollary 1.

# 3.2 PDOM for the Stochastic Setting

For the stochastic setting where the feedback data are i.i.d. distributed, we present the algorithm, PDOM-S in Alg. 2. In PDOM-S, we adopt a vector-sum protocol [4], which serves to aggregate all learners’ input vectors. Every ?? timeslots, the learners run vectorsum to aggregate their local gradients and a noise vector $b _ { k } .$ . Vectorsum returns the noisy gradient to all learners, and the learners then update the model using gradient descent.

Compared with PDOM-O, PDOM-S can be more communicationefficient partially because the learners share gradients using vectorsum, which requires fewer communications than broadcasting in all learners’ neighborhoods. Each run of vector-sum takes $O ( n )$ communication cost. The runtime of vector-sum ?? is proportional to the network’s diameter, which is upper bounded by O (??). We neglect the ?? feedbacks during each run of vector-sum. This would not enlarge the regret too much by taking the batch size much larger than ?? since the loss functions are i.i.d. We then tune the batch size depending on ??, ??, ??, and ?? to obtain the optimal regret.

We analyze PDOM-S with different batch sizes ?? in Theorem 2 and provide the detailed proof in Section 4.2.

Theorem 2. PDOM-S satisfies ??-DP. If the loss satisfies Definition 2, by choosing $\begin{array} { r } { \eta _ { k } = \frac { 1 } { \alpha k } } \end{array}$ in Alg. 2, the regret bound for learner ?? ∈ [??] is:

$$
\bar {\mathcal {R}} _ {i} (T) = O \bigg (\frac {L ^ {2} \ln T}{\alpha} \Big (n \tau + \frac {d ^ {2} \tau}{n (\tau - \mu) ^ {2} \epsilon^ {2}} \Big) \bigg).
$$

If the loss functions satisfy Definitions 2 and 3 with $\alpha = 0 ,$ by choosing $\eta _ { k } ~ = ~ 1 / \left( \bar { \sigma } \sqrt { 2 k } / \| C \| _ { 2 } + L _ { G } \right)$ , where $\begin{array} { r } { \bar { \sigma } ^ { 2 } ~ = ~ \frac { L ^ { 2 } } { n ( \tau - \mu ) } + ~ \frac { 2 \dot { d } \sigma ^ { 2 } } { n ^ { 2 } ( \tau - \mu ) ^ { 2 } } } \end{array}$ ??2 and $\sigma = 2 \sqrt { d } L / \epsilon$ , the regret bound for learner ?? ∈ [??] is:

$$
\begin{array}{l} \bar {\mathcal {R}} _ {i} (T) = \mathcal {O} \left(n \tau \left(L \| \mathcal {C} \| _ {2} + L _ {G} \| \mathcal {C} \| _ {2} ^ {2}\right) + \right. \\ L \left\| C \right\| _ {2} \sqrt {n T} \Big (1 + \sqrt {\frac {\mu}{\tau - \mu}} \Big) \Big (1 + \frac {d}{\epsilon \sqrt {n (\tau - \mu)}} \Big) \Big), \\ \end{array}
$$

where $\begin{array} { r } { \| C \| _ { 2 } \triangleq \operatorname* { m a x } _ { x , y \in C } \| x - y \| _ { 2 } } \end{array}$ . The communication cost $i s O ( n T / \tau )$ .

A corollary of Theorem 2 with the optimal ?? is as follows.

Corollary 2. If the loss functions satisfy Definition 2, choose $\begin{array} { r } { \tau = 2 \mu + \Theta \big ( \frac { d } { n \epsilon } \big ) } \end{array}$ in PDOM-S. The regret bound for learner ?? ∈ [??] is: $\begin{array} { r } { \bar { \mathcal { R } } _ { i } ( T ) = O \left( \frac { L ^ { 2 } \ln T } { \alpha } \left( n \mu + \frac { d } { \epsilon } \right) \right) } \end{array}$ . The communication cost is $O ( \frac { \epsilon n ^ { 2 } T } { d } )$ .

If the loss functions satisfy Definitions 2 and 3 with $\alpha = 0$ choose $\begin{array} { r } { \tau = 2 \mu + \Theta \big ( \frac { d ^ { 2 / 3 } T ^ { 1 / 3 } } { ( n \epsilon ) ^ { 2 / 3 } } \big ) } \end{array}$   ??2/3?? 1/3(???? )2/3  . Then the regret bound for learner ?? ∈ [??] is: (d2/3T1/3 $i \in [ n ]$

$$
\bar {\mathcal {R}} _ {i} (T) = \mathcal {O} \left(L \| C \| _ {2} \sqrt {n T} + \left(n \mu + \frac {d ^ {2 / 3} (n T) ^ {1 / 3}}{\epsilon^ {2 / 3}}\right) \left(L \| C \| _ {2} + L _ {G} \| C \| _ {2} ^ {2}\right)\right).
$$

The communication cost is $O ( \frac { n ^ { 5 / 3 } ( \epsilon T ) ^ { 2 / 3 } } { d ^ { 2 / 3 } } )$ ??2/3 .

PDOM in the stochastic setting outperforms its counterpart in the oblivious setting for both convex, Lipschitz, and smooth loss functions and strongly convex and Lipschitz loss functions. Notably, for the former, the impact of the DP budget ?? on the optimal regret bound can be disregarded for sufficiently large ?? , as stated in Corollary 2. Regarding communication cost, PDOM-S’s advantage over the non-batch algorithm [31] is particularly significant in scenarios with high model dimensions or limited DP budgets. Furthermore, for convex, Lipschitz, and smooth loss functions, the communication advantage grows with the learner number or learning time.

Impact of network topologies: In Corollary 2, the runtime of vector-sum ?? is proportional to the network’s diameter, which ranges from $O ( 1 ) \tan O ( n )$ . For instance, $\mu = O ( 1 )$ for star networks and $\mu = { \cal { O } } ( n )$ for cycle networks. According to Corollary 2, the regret bound of PDOM-S scales as $O ( n ^ { 2 } )$ on cycle networks and decreases to $O ( n )$ on star networks for the dependence of ??.

Comparison with existing works: PDOM-S is the first PDOCO algorithm specially tailored for the stochastic setting. PDOM-S achieves the privacy-free regret $O ( n ^ { 2 } + { \sqrt { n T } } )$ for $T = \Omega ( d ^ { 4 } / ( n \epsilon ^ { 4 } ) )$ 号 for Lipschitz, convex, and smooth loss functions. This implies that PDOM-S performs essentially the same as the non-private algorithm [4] in terms of regret, given a sufficiently long learning time, and is, therefore, highly attractive for PDOCO applications.

# 4 PRIVACY AND REGRET PROOFS

In this section, we provide detailed proofs for Theorems 1 and 2.

# 4.1 Analysis of PDOM for the Oblivious Setting

This subsection presents several inequalities in Lemma 1, measuring the difference of key variables in PDOM-O. We then prove Theorem 1 by analyzing the DP property and bounding the regret based on Lemma 1. We let $\sigma \triangleq 2 \sqrt { d } L / \epsilon$ and $t _ { k } \triangleq$ min $1 + \left( k - 1 \right) \tau , T + 1 )$ 号 for $k \in [ m + 1 ]$ , where $m = \lceil T / \tau \rceil$ . Denote, for $i \in [ n ]$ and $k \in [ m ]$ , $\tilde { x } _ { k } ^ { i } \triangleq v _ { k - 1 } ^ { i } - \eta _ { k - 1 } ( g _ { k - 1 } ^ { i } + b _ { k - 1 } ^ { i } ) , r _ { k } ^ { i } \triangleq \hat { x } _ { k } ^ { i } - \tilde { x } _ { k } ^ { i }$ ${ \hat { f } } _ { k } ^ { i } \triangleq \Sigma _ { t = t _ { k } } ^ { t _ { k + 1 } - 1 } f _ { t } ^ { i }$ $v _ { k } ^ { i }$ ${ \hat { x } } _ { k } \triangleq { \textstyle \frac { 1 } { n } } \Sigma _ { i = 1 } ^ { n } { \hat { x } } _ { k } ^ { i }$ ???? and ˆ???? ≜ Σ????=1 ˆ?? ???? . ${ \hat { f } } _ { k } \triangleq \Sigma _ { i = 1 } ^ { n } { \hat { f } } _ { k } ^ { i }$

Lemma 1. If the loss functions satisfy Definition 2 with $\alpha \ge 0 , f o r$ PDOM-O in Alg. 1, it holds that for ?? ∈ [??] and $i \in [ n ]$ :

$$
\left\{ \begin{array}{l} \mathbb {E} \left\| \hat {x} _ {k} - v _ {k} ^ {i} \right\| _ {2} \leq \| C \| _ {2} \sqrt {n} \lambda_ {2} (A) ^ {k} + 2 \gamma \sqrt {n} \sum_ {s = 1} ^ {k - 1} \eta_ {k - s} \lambda_ {2} (A) ^ {s} \\ \mathbb {E} \left\| \hat {x} _ {k} - \hat {x} _ {k} ^ {i} \right\| _ {2} \leq \| C \| _ {2} \sqrt {n} \lambda_ {2} (A) ^ {k - 1} + 2 \gamma \sqrt {n} \sum_ {s = 1} ^ {k - 1} \eta_ {k - s} \lambda_ {2} (A) ^ {s - 1} \\ \mathbb {E} \langle \hat {x} _ {k} - \tilde {x} _ {k + 1} ^ {i}, r _ {k + 1} ^ {i} \rangle \leq \beta \eta_ {k} ^ {2} + \gamma \eta_ {k} \mathbb {E} \left\| \hat {x} _ {k} - v _ {k} ^ {i} \right\| _ {2}, \end{array} \right. \tag {4}
$$

where $\gamma = \tau L + \sqrt { 2 d } \sigma$ and $\beta = \tau ^ { 2 } L ^ { 2 } + 2 d \sigma ^ { 2 }$ .

Proof. Denote $X _ { k } \ \triangleq \ [ \hat { x } _ { k } ^ { 1 } , . . . , \hat { x } _ { k } ^ { n } ] , G _ { k } \ \triangleq \ [ g _ { k } ^ { 1 } , . . . , g _ { k } ^ { n } ] , B _ { k } \ \triangleq$ $[ b _ { k } ^ { 1 } , \ldots , b _ { k } ^ { n } ]$ , and $R _ { k } \triangleq [ r _ { k } ^ { 1 } , \cdots , r _ { k } ^ { n } ]$ for ?? ∈ [??]. By ${ \mathrm { A l g . ~ } } 1 , X _ { k } =$ $X _ { k - 1 } ^ { \ " } A - \ " \eta _ { k - 1 } ( G _ { k - 1 } + B _ { k - 1 } ) + \ddot { R _ { k } }$ and $V _ { k } = X _ { k } A$ . It follows that:

$$
{X _ {k}} {= X _ {1} A ^ {k - 1} - \Sigma_ {s = 1} ^ {k - 1} [ \eta_ {k - s} (G _ {k - s} + B _ {k - s}) - R _ {k - s + 1} ] A ^ {s - 1}.} {(5)}
$$

$[ 1 0 ] , \| \Pi _ { C } ( x + y ) - ( x + y ) \| _ { 2 } \leq \| y \| _ { 2 }$ $x \in C , y \in \mathbb { R } ^ { d } . \mathrm { B y } v _ { k + 1 } ^ { i } = \Sigma _ { j = 1 } ^ { n } A _ { j i } \hat { x } _ { k + 1 } ^ { j } \in C \mathrm { ~ a n d ~ } r _ { k + 1 } ^ { i } \triangleq \hat { x } _ { k + 1 } ^ { i } - 1$ $\tilde { x } _ { k + 1 } ^ { i } = \Pi _ { C } ( v _ { k } ^ { i } - \eta _ { k } ( g _ { k } ^ { i } + b _ { k } ^ { i } ) ) - ( v _ { k } ^ { i } - \eta _ { k } ( g _ { k } ^ { i } + b _ { k } ^ { i } ) )$ , we obtain

$$
\left\| r _ {k + 1} ^ {i} \right\| _ {2} \stackrel {(i)} {\leq} \left\| - \eta_ {k} (g _ {k} ^ {i} + b _ {k} ^ {i}) \right\| _ {2} \stackrel {(i i)} {\leq} \eta_ {k} \tau L + \eta_ {k} \left\| b _ {k} ^ {i} \right\| _ {2}, \tag {6}
$$

where the second inequality follows from triangle inequality and Definition 2. By Jensen’s inequality and $\mathbb { E } \| b _ { k } ^ { i } \| _ { 2 } ^ { 2 } = 2 \dot { d } \sigma ^ { 2 }$ [6] for $b _ { k } ^ { i } \sim L a p ^ { d } ( \sigma )$ , it holds that

$$
\mathbb {E} \| b _ {k} ^ {i} \| _ {2} \leq \sqrt {\mathbb {E} \| b _ {k} ^ {i} \| _ {2} ^ {2}} = \sqrt {2 d} \sigma . \tag {7}
$$

Denote ???? as the ??-th basis vector in $\mathbb { R } ^ { d }$ and ?? as the all-one vector. It holds that $\begin{array} { r } { \hat { x } _ { k } - v _ { k } ^ { i } = X _ { k } \big ( \frac { e } { n } - A e _ { i } \big ) } \end{array}$ . It follows that:

$$
\begin{array}{l} \mathbb {E} \| \hat {x} _ {k} - v _ {k} ^ {i} \| _ {2} \leq \| C \| _ {2} \left\| \frac {e}{n} - A ^ {k} e _ {i} \right\| _ {1} + \sum_ {s = 1} ^ {k - 1} 2 \gamma \eta_ {k - s} \left\| \frac {e}{n} - A ^ {s} e _ {i} \right\| _ {1} \tag {8} \\ \leq \| C \| _ {2} \sqrt {n} \lambda_ {2} (A) ^ {k} + \Sigma_ {s = 1} ^ {k - 1} 2 \gamma \eta_ {k - s} \sqrt {n} \lambda_ {2} (A) ^ {s}, \\ \end{array}
$$

where the first inequality follows from Definition 2, Eqs. $( 5 ) \AA - \textcircled { 7 }$ , triangle inequality, and the fact that the gossip matrix ?? satisfies $A e = e [ 1 4 ]$ , and the second inequality follows from $\| { \frac { e } { n } } - A ^ { k } e _ { i } \| _ { 1 } \leq$ $\sqrt { n } \lambda _ { 2 } ( A ) ^ { k } \ [ 2 8 ]$ for $i \in [ n ]$ .

The second inequality in Eq. (4) follows from $\begin{array} { r } { \hat { x } _ { k } - \hat { x } _ { k } ^ { i } = X _ { k } \left( \frac { e } { n } - e _ { i } \right) } \end{array}$ and a similar line of analysis as for Eq. (8). For the last inequality in Eq. (4), by $\tilde { x } _ { k + 1 } ^ { i } \triangleq v _ { k } ^ { i } - \dot { \eta } _ { k } ( g _ { k } ^ { i } + b _ { k } ^ { i } )$ , it holds that

$$
\left\| \hat {x} _ {k} - \tilde {x} _ {k + 1} ^ {i} \right\| _ {2} \leq \left\| \hat {x} _ {k} - v _ {k} ^ {i} \right\| _ {2} + \eta_ {k} \left\| g _ {k} ^ {i} + b _ {k} ^ {i} \right\| _ {2}, \tag {9}
$$

By the Cauchy-Schwarz inequality, we obtain:

$$
\begin{array}{l} \mathbb {E} \langle \hat {x} _ {k} - \tilde {x} _ {k + 1} ^ {i}, r _ {k + 1} ^ {i} \rangle \leq \mathbb {E} \left\| \hat {x} _ {k} - \tilde {x} _ {k + 1} ^ {i} \right\| _ {2} \left\| r _ {k + 1} ^ {i} \right\| _ {2} \\ \leq \eta_ {k} \mathbb {E} \big [ \left\| g _ {k} ^ {i} + b _ {k} ^ {i} \right\| _ {2} \left\| \hat {x} _ {k} - v _ {k} ^ {i} \right\| _ {2} \big ] + \eta_ {k} ^ {2} \mathbb {E} \left\| g _ {k} ^ {i} + b _ {k} ^ {i} \right\| _ {2} ^ {2} \\ \leq \eta_ {k} (\tau L + \mathbb {E} \left\| b _ {k} ^ {i} \right\| _ {2}) \mathbb {E} \left\| \hat {x} _ {k} - v _ {k} ^ {i} \right\| _ {2} + \eta_ {k} ^ {2} \tau^ {2} L ^ {2} + \eta_ {k} ^ {2} \mathbb {E} \left\| b _ {k} ^ {i} \right\| _ {2} ^ {2}, \\ \end{array}
$$

where the second inequality follows from inequality (??) in Eq. (6) and $\operatorname { E q . } \left( 9 \right)$ , and the last inequality holds by triangle inequality and the fact that $b _ { k } ^ { i }$ is independent of the value of $\hat { x } _ { k } - v _ { k } ^ { i }$ and $g _ { k } ^ { i } .$ The last inequality in Eq. (4) then follows from Eqs. (7) and (8). □

Proof of Theorem 1. For the privacy analysis, consider neighboring loss sequences $\mathcal { F }$ and $\mathcal { F } ^ { \bar { \prime } }$ , differing only at the ?? -th loss function of learner ??, where $t _ { k } ~ \leq ~ t ~ \leq ~ t _ { k + 1 } - 1$ . Let $\hat { x } _ { k } ^ { j }$ and $g _ { k } ^ { j }$ $( \hat { x } _ { k } ^ { j ^ { \prime } }$ and $g _ { k } ^ { j ^ { \prime } } )$ for $j ~ \in ~ [ n ]$ and $k \in [ m ]$ be the models and gradients evaluated by Alg. 1 on $\mathcal { F } \left( \mathcal { F } ^ { \prime } \right)$ . Before time $t _ { k + 1 } ,$ , the distributions of updated model sequences for $\mathcal { F }$ and ${ \mathcal { F } } ^ { \prime }$ are identical, preventing privacy leakage. Without loss in generality, assume the updated model sequences are identical. At time $t _ { k + 1 }$ , by the Lipschitz assumption and triangle inequality, $\| g _ { k } ^ { i } - g _ { k } ^ { i } ^ { \prime } \| _ { 1 } \leq$ $\sqrt { d } ( \| \nabla f _ { t } ^ { i } ( \hat { x } _ { k } ^ { i } ) \| _ { 2 } + \| \nabla f _ { t } ^ { i ^ { \prime } } ( \hat { x } _ { k } ^ { i ^ { \prime } } ) \| _ { 2 } ) \leq 2 \sqrt { d } L$ . By Theorem 3.6 in [6], sampling $b _ { k } ^ { i }$ from $L a p ^ { d } ( 2 \sqrt { d } L / \epsilon )$ guarantees that the distributions of $g _ { k } ^ { i } + b _ { k } ^ { i }$ and $g _ { k } ^ { i } { } ^ { \prime } + b _ { k } ^ { i }$ satisfy ??-DP. By the post-processing property of DP [6], the distributions of $\hat { x } _ { k + 1 } ^ { i }$ 1 and ??ˆ????+ $\hat { x } _ { k + 1 } ^ { i } \prime$ 1 satisfy ??-DP. The other learners’ models remain identical for F and ${ \mathcal { F } } ^ { \prime }$ . Using PDOM and the same loss sequence, we derive the other models for F and ${ \mathcal { F } } ^ { \prime }$ based on models at time $t _ { k + 1 }$ , which satisfy ??-DP. The whole model sequences satisfy $\textstyle \epsilon { \mathrm { - D P } } ,$ as per the post-processing property, for arbitrary ?? and ??.

For the regret analysis for loss satisfying Definition 2, we first consider ?? $\begin{array} { r } { \lceil \bar { T } . \mathrm { B y } \hat { x } _ { k + 1 } ^ { i } = v _ { k } ^ { i } - \eta _ { k } \big ( g _ { k } ^ { i } + b _ { k } ^ { i } \big ) + r _ { k + 1 } ^ { \bar { i } } , v _ { k } ^ { i } = \Sigma _ { j = 1 } ^ { n } A _ { j i } \hat { x } _ { k } ^ { j } , } \end{array}$ and $A e = e [ 1 4 ]$ , we obtain $\begin{array} { r } { \hat { x } _ { k + 1 } = \hat { x } _ { k } - \frac { 1 } { n } \Sigma _ { i = 1 } ^ { n } \big [ \eta _ { k } ( g _ { k } ^ { i } + b _ { k } ^ { i } ) - r _ { k + 1 } ^ { i } \big ] } \end{array}$ ]. Then,

$$
\begin{array}{l} \mathbb {E} \left\| \hat {x} _ {k + 1} - x \right\| _ {2} ^ {2} - \mathbb {E} \left\| \hat {x} _ {k} - x \right\| _ {2} ^ {2} = - \frac {2 \eta_ {k}}{n} \Sigma_ {i = 1} ^ {n} \mathbb {E} \left\langle g _ {k} ^ {i}, \hat {x} _ {k} - x \right\rangle + \tag {10} \\ \mathbb {E} \bigg \| \frac {1}{n} \Sigma_ {i = 1} ^ {n} [ \eta_ {k} (g _ {k} ^ {i} + b _ {k} ^ {i}) - r _ {k + 1} ^ {i} ] \bigg \| _ {2} ^ {2} + \frac {2}{n} \Sigma_ {i = 1} ^ {n} \mathbb {E} \langle \hat {x} _ {k} - x, r _ {k + 1} ^ {i} \rangle , \\ \end{array}
$$

where the equality follows from the fact that $b _ { k } ^ { i }$ is independent of the value of $\hat { x } _ { k } - x$ . For the RHS of Eq. (10), first, by Definition $^ { 2 , }$

$$
\begin{array}{l} - \left\langle g _ {k} ^ {i}, \hat {x} _ {k} - x \right\rangle = - \left\langle g _ {k} ^ {i}, \hat {x} _ {k} - \hat {x} _ {k} ^ {i} \right\rangle - \left\langle g _ {k} ^ {i}, \hat {x} _ {k} ^ {i} - x \right\rangle \\ \leq \tau L \left\| \hat {x} _ {k} - \hat {x} _ {k} ^ {i} \right\| _ {2} + \hat {f} _ {k} ^ {i} (x) - \hat {f} _ {k} ^ {i} (\hat {x} _ {k} ^ {i}) - \frac {\tau \alpha}{2} \left\| \hat {x} _ {k} ^ {i} - x \right\| _ {2} ^ {2} \\ \leq 2 \tau L \left\| \hat {x} _ {k} - \hat {x} _ {k} ^ {i} \right\| _ {2} - \frac {\tau \alpha}{2} \left\| \hat {x} _ {k} ^ {i} - x \right\| _ {2} ^ {2} + \hat {f} _ {k} ^ {i} (x) - \hat {f} _ {k} ^ {i} (\hat {x} _ {k}). \\ \end{array}
$$

By $\begin{array} { r } { \hat { x } _ { k } = \frac { 1 } { n } \Sigma _ { i = 1 } ^ { n } \hat { x } _ { k } ^ { i } } \end{array}$ , it follows that

$$
\begin{array}{l} - \Sigma_ {i = 1} ^ {n} \left\langle g _ {k} ^ {i}, \hat {x} _ {k} - x \right\rangle \leq 2 \tau L \Sigma_ {i = 1} ^ {n} \left\| \hat {x} _ {k} - \hat {x} _ {k} ^ {i} \right\| _ {2} - \tau \alpha n (11) \\ \frac {\tau \alpha n}{2} \| \hat {x} _ {k} - x \| _ {2} ^ {2} + \hat {f} _ {k} (x) - \hat {f} _ {k} (\hat {x} _ {k}). (11) \\ \end{array}
$$

For the second term of the RHS in Eq. (10), by Jensen’s inequality,

$$
\mathbb {E} \left\| \frac {1}{n} \Sigma_ {i = 1} ^ {n} \left(\eta_ {k} \left(g _ {k} ^ {i} + b _ {k} ^ {i}\right) - r _ {k + 1} ^ {i}\right) \right\| _ {2} ^ {2} \leq \frac {1}{n} \Sigma_ {i = 1} ^ {n} \mathbb {E} \left\| \eta_ {k} \left(g _ {k} ^ {i} + b _ {k} ^ {i}\right) - r _ {k + 1} ^ {i} \right\| _ {2} ^ {2} \tag {12}
$$

$$
\leq \frac {4 \eta_ {k} ^ {2}}{n} \sum_ {i = 1} ^ {n} \mathbb {E} \left\| g _ {k} ^ {i} + b _ {k} ^ {i} \right\| _ {2} ^ {2} \leq 4 \eta_ {k} ^ {2} \tau^ {2} L ^ {2} + 8 d \eta_ {k} ^ {2} \sigma^ {2},
$$

where the second inequality follows from inequality (i) in Eq. (6) and the Cauchy-Schwarz inequality, and the last inequality follows from the fact that $b _ { k } ^ { i }$ is independent of $\cdot _ { \boldsymbol { g } _ { k } ^ { i } }$ , Definition 2, and Eq. (7). By [30], it holds that the projection operator $\Pi _ { C }$ satisfies $\left. \tilde { x } - \right.$ $x , \Pi _ { C } ( \tilde { x } ) - \tilde { x } \rangle \ \leq \ 0$ for arbitrary $\tilde { x } \in \bar { \mathbb { R } } ^ { d }$ and $x \in C$ . By $r _ { k + 1 } ^ { i } =$ $\Pi _ { C } ( \tilde { x } _ { k + 1 } ^ { i } ) - \tilde { x } _ { k + 1 } ^ { i }$ , it follows that for ?? ∈ C,

$$
\begin{array}{l} \mathbb {E} \left\langle \hat {x} _ {k} - x, r _ {k + 1} ^ {i} \right\rangle = \mathbb {E} \left\langle \hat {x} _ {k} - \tilde {x} _ {k + 1} ^ {i}, r _ {k + 1} ^ {i} \right\rangle + \mathbb {E} \left\langle \tilde {x} _ {k + 1} ^ {i} - x, r _ {k + 1} ^ {i} \right\rangle \tag {13} \\ \leq \mathbb {E} \langle \hat {x} _ {k} - \tilde {x} _ {k + 1} ^ {i}, r _ {k + 1} ^ {i} \rangle , \\ \end{array}
$$

which is then upper bounded as in the last inequality in Eq. (4). By plugging Eqs. (11)-(13) into Eq. (10), it holds that

$$
\begin{array}{l} \mathbb {E} \left[ \hat {f} _ {k} (\hat {x} _ {k}) - \hat {f} _ {k} (x) \right] \leq \frac {n}{2 \eta_ {k}} \left[ (1 - \tau \alpha \eta_ {k}) \mathbb {E} \| \hat {x} _ {k} - x \| _ {2} ^ {2} - \right. \\ \mathbb {E} \left. \left\| \hat {x} _ {k + 1} - x \right\| _ {2} ^ {2} \right] + (\tau L + \sqrt {2 d} \sigma) \Sigma_ {i = 1} ^ {n} \mathbb {E} \left\| \hat {x} _ {k} - v _ {k} ^ {i} \right\| _ {2} + \tag {14} \\ 2 \tau L \Sigma_ {i = 1} ^ {n} \mathbb {E} \left\| \hat {x} _ {k} - \hat {x} _ {k} ^ {i} \right\| _ {2} + n \eta_ {k} \big (3 \tau^ {2} L ^ {2} + 6 d \sigma^ {2} \big). \\ \end{array}
$$

Taking $\begin{array} { r } { \eta _ { k } = \frac { 1 } { \tau \alpha k } } \end{array}$ and summing Eq. (14) over $k ,$ , we obtain:

$$
\begin{array}{l} \mathbb {E} \left[ \sum_ {k = 1} ^ {m} \left(\hat {f} _ {k} (\hat {x} _ {k}) - \hat {f} _ {k} (x)\right) \right] \leq \left(3 \tau^ {2} L ^ {2} + 6 d \sigma^ {2}\right) \frac {n + n \ln (m)}{\alpha \tau} + \\ \Sigma_ {k = 1} ^ {m} \Sigma_ {i = 1} ^ {n} \left[ (\tau L + \sqrt {2 d} \sigma) \mathbb {E} \left\| \hat {x} _ {k} - v _ {k} ^ {i} \right\| _ {2} + 2 \tau L \mathbb {E} \left\| \hat {x} _ {k} - \hat {x} _ {k} ^ {i} \right\| _ {2} \right] \tag {15} \\ \leq O \left(\frac {n ^ {3 / 2} \| C \| _ {2} (\tau L + \sqrt {d} \sigma)}{1 - \lambda_ {2} (A)} + \frac {n ^ {3 / 2} \ln T}{(1 - \lambda_ {2} (A)) \alpha} \left(\tau L ^ {2} + \frac {d \sigma^ {2}}{\tau}\right)\right), \\ \end{array}
$$

where the second inequality follows from Eq. (4) and the AM-GM inequality. For $j \in [ n ]$ , by Definition 2, it holds that:

$$
\begin{array}{l} \mathbb {E} \left[ \Sigma_ {k = 1} ^ {m} \Sigma_ {i = 1} ^ {n} (\hat {f} _ {k} ^ {i} (\hat {x} _ {k} ^ {j}) - \hat {f} _ {k} ^ {i} (\hat {x} _ {k})) \right] \leq n \tau L \Sigma_ {k = 1} ^ {m} \mathbb {E} \left\| \hat {x} _ {k} ^ {j} - \hat {x} _ {k} \right\| _ {2} \\ \leq O \left(\frac {n ^ {3 / 2} \tau L \| C \| _ {2}}{1 - \lambda_ {2} (A)} + \frac {L n ^ {3 / 2}}{(1 - \lambda_ {2} (A)) \alpha} (\tau L + \sqrt {d} \sigma) \ln T\right), \tag {16} \\ \end{array}
$$

where the second inequality follows from Eq. (4). By summing Eqs. (15) and (16) and plugging $\sigma = 2 \sqrt { d } L / \epsilon .$ , the result follows. For $\tau \nmid T$ , we let $T ^ { \prime } \triangleq \left\lceil \frac { \bar { T } } { \tau } \right\rceil$ ?? and $\begin{array} { r } { f _ { t } ^ { i } \equiv \frac { 1 } { n T } \Sigma _ { t = 1 } ^ { T } f _ { t } ( x ) } \end{array}$ for $T + 1 \leq t \leq$ $T ^ { \prime } , i \in [ n ]$ . Then, by $\dot { T } ^ { \prime } = O ( T )$ , the same regret bound holds by upper bounding $\mathcal { R } _ { i } ( T )$ using $\mathcal { R } _ { i } ( T ^ { \prime } )$ . The proof for loss functions satisfying Definition 2 with $\alpha = 0$ follows a similar line of analysis via $\operatorname { E q . } \left( 1 4 \right)$ with $\alpha = 0$ and $\eta _ { k } \equiv 1 / \sqrt { T }$ .

For the communication cost, each learner $i \in [ n ]$ conducts ⌈?? /??⌉ broadcasts in its neighborhood and each broadcast takes $O ( n )$ communication cost. The overall communication cost is $O ( \frac { n ^ { 2 } T } { \tau } )$ . □

# 4.2 Analysis of PDOM for the Stochastic Setting

This subsection analyzes the regret of PDOM-S in Lemma 2, assuming noisy gradients with bounded variance. We then prove Theorem 2 by analyzing its DP property and bounding the regret using Lemma 2. Let $t _ { k } \triangleq$ min $\big ( 1 + \big ( k - 1 \big ) \tau , T + 1 \big )$ for $k \le m = \lceil T / \tau \rceil$

Lemma 2. Let ??¯ > 0 satisfy $\mathbb { E } \left\| \bar { g } _ { k } - \nabla \bar { F } ( \hat { x } _ { k } ) \right\| _ { 2 } ^ { 2 } \leq \bar { \sigma } ^ { 2 }$ for all ?? . For loss satisfying Definition 2, by choosing $\begin{array} { r } { \eta _ { k } = \frac { 1 } { \alpha k } } \end{array}$ in PDOM-S, it holds that $\begin{array} { r } { \bar { \mathcal { R } } _ { i } ( T ) = O \bigl ( \frac { L ^ { 2 } + \bar { \sigma } ^ { 2 } } { \alpha } } \end{array}$ ???? ln ?? for ?? ∈ [??]. If the loss satisfies Definitions 2 and 3 with ?? = 0, by choosing ???? = 1???? +??¯√2??/∥ C∥2 , $\alpha = 0 ,$ $\begin{array} { r } { \eta _ { k } = \frac { 1 } { L _ { G } + \bar { \sigma } \sqrt { 2 k } / \| C \| _ { 2 } } , } \end{array}$ it holds that $\bar { \mathcal { R } } _ { i } ( T ) = O ( n \tau ( L \| C \| _ { 2 } + L _ { G } \| C \| _ { 2 } ^ { 2 } + \| C \| _ { 2 } \bar { \sigma } \sqrt { m } ) )$ .

Proof. For loss satisfying Definitions 2 and 3 with $\alpha = 0 _ { ; }$ , Lemma 2 follows from Theorem 1 in [4]. For loss satisfying Definition 2 with $\alpha > 0 _ { : }$ , denote $\begin{array} { r } { \bar { f } _ { k } = \frac { 1 } { n ( t _ { k + 1 } - t _ { k } ) } { \sum _ { t = t _ { k } } ^ { t _ { k + 1 } - 1 } } f _ { t } } \end{array}$ ) Σ????+1 −1?? =???? ???? . By Theorem 3.3 in [10],

$$
\left\{ \begin{array}{l} \bar {f} _ {k} (\hat {x} _ {k}) - \bar {f} _ {k} (x) \leq \langle \nabla \bar {f} _ {k} (\hat {x} _ {k}), \hat {x} _ {k} - x \rangle - \frac {\alpha}{2} \| \hat {x} _ {k} - x \| _ {2} ^ {2} \\ \langle \bar {g} _ {k}, \hat {x} _ {k} - x \rangle \leq \frac {1}{2 \eta_ {k}} [ \| \hat {x} _ {k} - x \| _ {2} ^ {2} - \| \hat {x} _ {k + 1} - x \| _ {2} ^ {2} ] + \frac {\eta_ {k} \| \bar {g} _ {k} \| _ {2} ^ {2}}{2}. \end{array} \right.
$$

As each $\bar { f } _ { k }$ is an unbiased estimator of ${ \bar { F } } ,$ and $\nabla \bar { f } _ { t } ( \hat { x } _ { k } )$ and $\bar { g } _ { k }$ are unbiased estimators of $\nabla \bar { F } ( \hat { x } _ { k } )$ , taking expectations over the inequalities above yields that for ?? ∈ [??],

$$
\bar {\mathcal {R}} _ {i} (T) \leq \frac {n \tau}{2 \alpha} \Sigma_ {k = 1} ^ {m} \frac {1}{k} \mathbb {E} \| \bar {g} _ {k} \| _ {2} ^ {2} \leq \frac {n \tau}{2 \alpha} (L ^ {2} + \bar {\sigma} ^ {2}) (1 + \ln m),
$$

where the first inequality follows from Eq. (3) and $\begin{array} { r } { \eta _ { k } = \frac { 1 } { \alpha k } } \end{array}$ and the second inequality follows from E $\| \bar { g } _ { k } \| _ { 2 } ^ { 2 } = \mathbb { E } \| \nabla F ( \hat { x } _ { k } ) \| _ { 2 } ^ { 2 } + \mathbb { E } \| \bar { g } _ { k } -$ $\nabla F ( \hat { x } _ { k } ) \| _ { 2 } ^ { 2 } \leq L ^ { 2 } + \bar { \sigma } ^ { 2 }$ . □

Proof of Theorem 2. Similarly, as in the proof of Theorem 1, for arbitrary $k \in [ m ]$ , the noise vector $b _ { k }$ ensures that the noisy gradient $\bar { g } _ { k }$ satisfies ??-DP. PDOM-S then satisfies ??-DP by the postprocessing property of DP via a similar line of analysis to Theorem 1. For the regret part, ${ \mathrm { i f } } \tau \mid T ,$ for $k \in [ m ]$ ,

$$
\mathbb {E} \left\| \bar {g} _ {k} - \nabla \bar {F} (\hat {x} _ {k}) \right\| _ {2} ^ {2} = \mathbb {E} \Bigg \| \frac {1}{n (\tau - \mu)} \big (\Sigma_ {i = 1} ^ {n} \Sigma_ {t = (k - 1) \tau + 1} ^ {k \tau - \mu} \nabla f _ {t} ^ {i} (\hat {x} _ {k}) + b _ {k} \big) -
$$

$$
\nabla \bar {F} (\hat {x} _ {k}) \Big \| _ {2} ^ {2} \leq \frac {L ^ {2}}{n (\tau - \mu)} + \frac {2 d \sigma^ {2}}{n ^ {2} (\tau - \mu) ^ {2}} = \bar {\sigma} ^ {2},
$$

where the inequality holds from Definition $2 , \mathbb { E } \Vert b _ { k } ^ { i } \Vert _ { 2 } ^ { 2 } = 2 d \sigma ^ { 2 } \ [ 6 ] .$ and the fact that $\nabla f _ { t } ^ { i } ( \hat { x } _ { k } ) - \nabla \bar { F } ( \hat { x } _ { k } )$ and $b _ { k }$ are independent. Theorem 2 then follows from Lemma 2 and $\sigma = 2 \sqrt { d } L / \epsilon . \operatorname { I f } \tau \ n \uparrow T .$ , Theorem 2 follows from $\bar { \mathcal { R } } _ { i } ( T ) \leq \bar { \mathcal { R } } _ { i } ( \tau \lceil T / \tau \rceil )$ , where $\tau \lceil T / \tau \rceil = \Theta ( T )$ .

For the communication cost, learners run vector-sum for $\lceil T / \tau \rceil$ times and each run takes $O ( n )$ communication cost [4]. □

# 5 EVALUATIONS BY EXPERIMENTS

In this section, we present a comparative study between our PDOM algorithm and state-of-the-art algorithms in the context of distributed online classification tasks. Our evaluation criteria mainly include error rates and communication cost.

# 5.1 Implementation Details

We perform distributed online (regularized) logistic regression and average the error rates of all learners’ model sequences. The error rates reflect the regret normalized by ???? using the error indicator loss function, indicating whether the classification result is correct. The (regularized) logistic loss function is a Lipschitz, smooth, and (strongly) convex proxy to the error indicator function [4].

Datasets and preprocessing: We conduct experiments on two real-world datasets, namely KDDCup99 [11] and Diabetes [5, 24]. KDDCup99 contains metadata and labels of approximately $5 \times 1 0 ^ { 6 }$ network connections, indicating whether they are intrusions, while Diabetes consists of around $\bar { 1 0 ^ { 5 } }$ diagnosis records and labels, indicating whether patients were readmitted to the hospital within 30 days. We preprocess the datasets by removing columns with missing values, converting categorical attributes into binary vectors [12], and scaling each feature to [−1, 1] and each sample to unit length. After preprocessing, each sample’s dimension in KDDCup99 and Diabetes is 117 and 841, respectively.

For the stochastic setting, we randomly split the data into equalsize blocks and assign them to learners in random order. For the oblivious setting, we assign positive samples to learners with smaller ?? ∈ [??] and negative samples to the others. We split the learning time into three equal-length intervals and flip the labels in the second interval. This approach ensures that the data distributions vary for different learners and intervals.

Baselines: We compare PDOM with the following baselines:

(1) PDOCO: This baseline refers to the state-of-the-art PDOCO algorithm that achieves the currently lowest regret bound in the oblivious setting [31].   
(2) no-comm: It is a baseline for PDOCO in the stochastic setting inspired by the no-communication algorithm in [4]. In nocomm, each learner updates its models based on its own loss sequence without communicating with others using the state-of-the-art private online convex optimization (POCO) algorithms [9, 25] ([9] and [25] achieve the lowest regret bounds for general and strongly convex loss, respectively).1   
(3) non-pri: This is a non-private baseline. For the oblivious setting, we use the algorithm in [30]. For the stochastic setting, non-pri with $\alpha = 0$ and $\alpha > 0$ refer to the distributed

Table 2: Error rates for distributed online regularized logistic regression with different regularization parameters $\alpha > 0 .$ . The lowest error rate for each algorithm is in bold. 

<table><tr><td> $\alpha$ </td><td> $10^{-1}$ </td><td> $10^{-2}$ </td><td> $10^{-3}$ </td><td> $10^{-4}$ </td><td> $10^{-5}$ </td></tr><tr><td colspan="6">KDDCup99, Oblivious</td></tr><tr><td>non-pri</td><td>0.304</td><td>0.129</td><td>0.038</td><td>0.016</td><td>0.055</td></tr><tr><td>PDOC0</td><td>0.393</td><td>0.450</td><td>0.497</td><td>0.497</td><td>0.498</td></tr><tr><td>PDOM</td><td>0.315</td><td>0.273</td><td>0.368</td><td>0.390</td><td>0.390</td></tr><tr><td colspan="6">KDDCup99, Stochastic</td></tr><tr><td>non-pri</td><td>0.199</td><td>0.034</td><td>0.006</td><td>0.027</td><td>0.217</td></tr><tr><td>no-comm</td><td>0.324</td><td>0.289</td><td>0.286</td><td>0.282</td><td>0.284</td></tr><tr><td>PDOM</td><td>0.195</td><td>0.087</td><td>0.219</td><td>0.360</td><td>0.394</td></tr><tr><td colspan="6">Diabetes, Oblivious</td></tr><tr><td>non-pri</td><td>0.220</td><td>0.128</td><td>0.119</td><td>0.144</td><td>0.158</td></tr><tr><td>PDOC0</td><td>0.494</td><td>0.498</td><td>0.499</td><td>0.499</td><td>0.498</td></tr><tr><td>PDOM</td><td>0.331</td><td>0.315</td><td>0.345</td><td>0.343</td><td>0.352</td></tr><tr><td colspan="6">Diabetes, Stochastic</td></tr><tr><td>non-pri</td><td>0.112</td><td>0.112</td><td>0.117</td><td>0.157</td><td>0.199</td></tr><tr><td>no-comm</td><td>0.376</td><td>0.325</td><td>0.318</td><td>0.324</td><td>0.322</td></tr><tr><td>PDOM</td><td>0.121</td><td>0.129</td><td>0.183</td><td>0.246</td><td>0.242</td></tr></table>

mini-batch algorithm (DMA) [4] and the no-communication gradient-descent algorithm [4, 10], respectively.

Implementations: We choose the model’s feasible region C as the $\ell _ { 2 }$ ball with radius 10 and evaluate each error rate by averaging the results in 100 runs. For PDOM, we take the batch sizes in Corollaries 1 and 2 with the constant factors hidden by Θ as 1 by default. For the choice of $\alpha > 0$ in regularized logistic regression, we evaluate the error rates of all algorithms with ?? $\in \ \bar { \{ 1 0 ^ { - 1 } , 1 0 ^ { - 2 } , 1 0 ^ { - 3 } , 1 0 ^ { - 4 } , 1 0 ^ { - 5 } \} }$ and $\epsilon = 1$ on the 8-node cycle network where each node has two neighbors [28]. We choose $T = 1 . 2 5 \times 1 0 ^ { 4 }$ for Diabetes and $T = 2 \times 1 0 ^ { 4 }$ for KDDCup99. For each algorithm and dataset, we choose ?? that minimizes the error rates in Table 2 in experiments with $\alpha > 0$ in the rest of this section.

# 5.2 Results for the Oblivious Setting

We present the experimental results of PDOM and the baselines in Figs. 3(a)-3(d) and Figs. 4(a)-4(b). Overall, PDOM achieves consistently lower error rates than PDOCO in most cases, aligning with our theoretical results in Table 1. The error rates of PDOM decrease as ?? or ?? increases, consistent with Corollary 1. We observe that PDOM exhibits significantly lower communication cost compared to non-pri and PDOCO. The communication cost ratio of PDOM to non-pri and PDOCO is constant in ?? for each dataset. Specifically, on KDDCup99, the communication cost of PDOM is approximately 0.08%, 0.8%, and 8% of that of non-pri and PDOCO when ?? is set to 0.1, 1, and 10, respectively. On Diabetes, PDOM yields communication cost of approximately 0.01%, 0.1%, and 1% of non-pri and PDOCO under the same ?? values. Furthermore, we empirically evaluate the impact of batch sizes of PDOM in Figs. 3(e)-3(h). PDOM’s error rates initially decrease and then increase with increasing batch sizes. This implies that as communication costs increase, the regret initially decreases and then increases, consistent with Theorem 1.

Impact of ?? and ?? : The evaluation on the 8-node cycle network in Figs. 3(a)-3(d) demonstrates that the advantage of PDOM over PDOCO is prominent in most cases when the error rates are reasonable (< 0.5). This is consistent with the results in Table 1.

![](images/df54eba84e2e603f8d6ecac0cbd58ed09bdccd7b4c9638f68ea94f40786ca684.jpg)



(a) Diabetes (α > 0)

![](images/153909a996fbb96dbb6d98911cf998d9930725a6754501eff0f03dfff9821bd3.jpg)



(c) Diabetes (α = 0)

![](images/fde6bcdff272a59a426aa8833f1791feb563eee288dca5e6b44b25a652df01c7.jpg)



(e) Diabetes (α > 0)

![](images/a2343fe3328ec28cf59ff6efd63672e0af8e948d6798f2f1ec2a91e39bfa923b.jpg)



(g) Diabetes (α = 0)

Figure 3: Distributed online classification error rates in the oblivious setting. ?? is the regularization parameter.   
![](images/53b1443c8bad9c6f9eed8596171710832a72095250d8587b28fcef6c51c2e38e.jpg)



(a) Oblivious (α > 0)

![](images/5980c48b0d4a868e54efb66135b722a907c1355d48c70a349521ad6ed2a7d9f5.jpg)



(c) Stochastic (α > 0)   
(d) Stochastic (α = 0)

Figure 4: Distributed online classification error rates on different networks. ?? is the regularization parameter. The error rates of no-comm and non-pri with ?? > 0 remain the same for different networks.   
![](images/8185774136a8e27e8f4cd82f1cbc4310252fa6b663d6994c66a7825ccea0a9ff.jpg)



(a) Diabetes (α > 0)

![](images/5f16a735849d271b9fc4248f1238e87c8228e6a047dc71d72bb67581a2592415.jpg)



(c) Diabetes (α = 0)

![](images/897e9c4d0bde973cfd58e220b380b1ec984805398ed61475b08d4e1d8dde6d86.jpg)



(e) Diabetes (α > 0)

![](images/7d4f7af1df12875f1f51c976fdb3f96d2ce55af674013cc2cb9ff88e9f678685.jpg)



(g) Diabetes (α = 0)   
(d) KDDCup99 (α = 0)   
Figure 5: Distributed online classification error rates in the stochastic setting. ?? is the regularization parameter.

Specifically, for ?? = 1, PDOM achieves 10% ∼ 20% lower error rates than PDOCO on both datasets for sufficiently large ?? .

Impact of the network topology: As Diabetes is not sufficiently large for experiments with larger ?? and ??, we evaluate the impact of network topologies on KDDCup99. We fix ?? = 1 and present the error rates on two networks: the 64-node cycle and hypercube networks, where each learner has 6 neighbors [30]. Figs. 4(a)-4(b) show that on both networks, PDOM outperforms PDOCO. Interestingly, the error rates on the cycle network are higher than those on the hypercube network for all algorithms. This observation agrees with the results in Table 1, as the hypercube network has a smaller ??2(??) [20, 30]. Compared to the results on the 8-node cycle network with ?? = 1 in Figs. 3(b) and 3(d), the accuracy of PDOM deteriorates on the 64-node cycle network. This is consistent with Corollary 1, where the regret normalized by ???? increases in ??.

Impact of the batch size: We study the impact of batch sizes on PDOM’s accuracy on the 8-node cycle network and show the results in Figs. 3(e)-3(h). The optimal batch size increases as ?? approaches 0 on both datasets, consistent with Corollary 1. Furthermore, the optimal batch size for Diabetes with a higher dimension is larger than that for KDDCup99 in most cases, also consistent with Corollary 1.

# 5.3 Results for the Stochastic Setting

For the stochastic setting, we present the error rates and communication costs in different parameter settings in Figs. 4(c)-4(d) and 5-8. The results show that PDOM consistently outperforms no-comm and is even comparable to non-pri for $\epsilon \geq 1$ and $\alpha = 0$ in terms of accuracy, confirming our theoretical results in Table 1. Similarly, as in the oblivious case, the error rates of PDOM decrease as ?? or ?? increases, and they initially decrease and then increase with increasing batch size, aligning with Theorem 2 and Corollary 2. Additionally, the communication savings of PDOM over PDOCO are above 95% throughout our parameter settings.

![](images/01b46e9994c3c5ad437ad26cfeeec822a14b01d810793e1ca23143d1443395ca.jpg)



Figure 6: Comm. ratios of PDOM and non-pri $( \alpha ~ = ~ 0 )$ to PDOCO in the stochastic setting.

![](images/b52876f8c52b1593d5e8bf531aac3ce0eec8b4a20bed8e262970f41c4423e00a.jpg)



Figure 7: Comm. ratios of PDOM and non-pri $( \alpha ~ = ~ 0 )$ to PDOCO in the stochastic setting on different networks.

![](images/e74677bf299e74d7e73cfc5893f7e2d135c13d97f8c16e5ad0e2e8f45dbd8e7a.jpg)



Figure 8: Distributed online classification error rates of PDOM with different batch sizes in the stochastic setting with $n = 6 4 .$

Impact of ?? and ?? : Figs. 5(a)-5(d) show that on the 8-node cycle network, the accuracy of PDOM is clearly superior to that of nocomm. For $\alpha = 0$ and $\epsilon \geq 1$ , PDOM achieves similar error rates to non-pri (with gaps < 0.04 for sufficiently large ?? ). To evaluate the communication efficiency of PDOM and non-pri (for $\alpha = 0 ;$ note that non-pri for $\alpha > 0$ is a no-communication algorithm), we plot their communication cost ratios to PDOCO in Fig. 6. Both PDOM and non-pri with $\alpha = 0$ achieve communication savings of > 95% compared to PDOCO for all ?? and ?? . Moreover, for $\alpha = 0 ,$ , PDOM features a clear communication-saving over non-pri.

Impact of the network topology: Figs. 4(c)-4(d) present the error rates in the stochastic setting on 64-node cycle and hypercube networks with ?? = 1 on KDDCup99. On both networks, PDOM clearly outperforms no-comm. On the hypercube network, PDOM achieves lower error rates than on the cycle network. This agrees with Corollary 2 as ?? scales as Θ(ln ??) for hypercube networks and as $\Theta ( n )$ for cycle networks [30]. Compared to the results on the 8-node cycle network in Figs. 5(b) and 5(d) when $\epsilon = 1$ , on the 64-node cycle network, the gap between the error rates of PDOM and non-pri narrows down. This confirms the results in Table 1, as the regret gap between PDOM and non-pri normalized by ???? decreases in ?? for small ?? and large ?? . Regarding communication cost, Fig. 7 shows that PDOM incurs $\leq ~ 2 \%$ communication cost of PDOCO on both networks when $\epsilon = 1 \AA$ . For $\alpha = 0 ,$ , PDOM also reduces the communication cost of non-pri by around 50%.

Impact of the batch size: In the stochastic setting, as depicted in Figs. $5 ( \mathrm { e } ) { - } 5 ( \mathrm { h } )$ , on the 8-node cycle network, the optimal batch size increases as ?? tends to 0. On Diabetes, PDOM achieves the optimal error rates for a wide range of batch sizes for some parameter settings. In other cases, the optimal batch sizes on Diabetes are generally larger than on KDDCup99. Moreover, in these cases, the optimal batch size is larger for larger ?? when $\alpha = 0 ,$ consistent with Corollary 2. Notably, Corollary 2 also suggests that the optimal batch size depends on learner numbers. To validate this result, we conduct experiments on the 64-node cycle network on KDDCup99 and present the results in Fig. 8. When $\epsilon = 1 0 ,$ , the optimal batch size for $n = 6 4$ is larger than that for $n = 8 ,$ since in this case, the optimal batch size is dominated by $\mu = { \cal { O } } ( n )$ in Corollary 2. As ?? approaches 0, the optimal batch size for $n = 8$ becomes comparable or even larger than $n = 6 4$ , consistent with Corollary 2 for small ??.

# 6 RELATED WORK

Private online convex optimization (POCO): Online convex optimization (OCO) is an important branch of machine learning that has drawn significant research attention [10, 23, 26]. However, Jain et al. pointed out the potential privacy leakage in OCO [13] and introduced the notion of POCO using DP [6]. Thakurta et al. achieved the state-of-the-art regret bound for POCO in the adversarial setting, including oblivious and non-oblivious settings where the loss functions can depend on historical models [25]. For strongly convex loss functions, the regret bound is $\tilde { O } ( d / \epsilon )$ , while for general convex loss functions, it is $\tilde { O } ( \sqrt { d T } / \epsilon )$ . In the stochastic setting, Han et al. proposed an algorithm that achieves an $\tilde { O } ( d / \epsilon ^ { 2 } )$ regret for strongly convex loss functions and an ${ \tilde { O } } ( { \sqrt { T } } + { \sqrt { d } } / \epsilon )$ regret for general convex loss [9]. Notably, the latter regret bound nearly matches the non-private minimax regret $O ( { \sqrt { T } } )$ when $T = \Omega ( d / \epsilon ^ { 2 } )$ ).

Private distributed online convex optimization (PDOCO): DOCO is an important research direction in machine learning, especially in scenarios where multiple learners collaborate to improve their models’ performance [8, 15, 17, 28]. However, as in OCO, privacy concerns are a significant consideration in DOCO, as a client may seek to infer others’ privacy through updated models [16]. To address this issue, several PDOCO algorithms have been proposed. In the oblivious setting, Zhu et al. proposed a PDOCO algorithm that achieves the state-of-the-art regret bounds for static undirected learner networks [31] (cf. Table 1). Their algorithm also works for time-varying balanced directed networks, where each learner has an equal number of in-neighbors and out-neighbors. Recently, Lü et al. and Xiong et al. extended the PDOCO algorithm to handle unbalanced directed learner networks [19, 29].

Besides regret loss, communication cost is another critical criterion in (private) DOCO. In the adversarial setting, Wan et al. proposed the distributed block online conditional gradient (D-BOCG) algorithm, which achieves a message complexity of $O ( n ^ { 2 } \sqrt { T } )$ [28]. For convex loss functions, D-BOCG achieves a regret bound of O ( 1−??2 (??) ) $\begin{array} { r } { O ( \frac { \sqrt { n } T ^ { 3 / 4 } } { 1 - \lambda _ { 2 } ( A ) } ) } \end{array}$ √???? 3/4 . In the stochastic setting, the distributed mini-batch algorithm [4] achieves a regret bound of $O ( n ^ { 2 } + { \sqrt { n T } } )$ for convex and smooth loss functions with a message complexity of $O ( n ^ { 5 / 3 } T ^ { 2 / 3 } )$ Another line of research [1, 22, 27] focused on reducing the bit complexity of DOCO, which refers to the bit-length of all transmitted messages in the algorithm run. One common technique to reduce bit complexity is gradient quantization [1].

Despite the significant progress made in the design of PDOCO algorithms, current approaches suffer from high regret and communication cost, as evidenced by the results in Table 1. Furthermore, there is a lack of tailored PDOCO algorithms for the stochastic setting, which could potentially lead to reduced regret and communication cost. We fill the gap by proposing PDOM-S designed for the stochastic setting. Meanwhile, our PDOM-O improves the performance of existing PDOCO algorithms in the oblivious setting.

# 7 CONCLUSION AND FUTURE WORK

PDOCO is a crucial framework for learning from massive learners’ streaming data while ensuring privacy, low regret, and low communication cost. Our mini-batch strategy in PDOCO strikes a balance between DP perturbation and model updates, and we study optimal batch size selection to minimize regret subject to ??-DP. Our PDOM algorithm outperforms the state-of-the-art [31] in terms of regret and communication cost, reducing regret bound and communication cost by an O (??/??) factor in the oblivious setting. In the stochastic setting, PDOM achieves privacy-free regret for sufficiently large learning time ?? when loss functions are Lipschitz, convex, and smooth. Extensive evaluations demonstrate the effectiveness of our algorithms.

Generalizing our work, we note that the optimal choice for ?? in Theorem 1 is independent of the network topology, making our analysis for PDOM in the oblivious setting applicable to scenarios with time-varying or directed learner networks [19, 29, 31]. We plan to explore privacy and regret analysis of PDOM on time-varying and directed learner networks in future work. Additionally, we plan to investigate the benefits of non-uniform batch sizes in PDOM, inspired by recent work that achieved minimax regret with fewer batches [7] in stochastic bandit optimization.

# ACKNOWLEDGMENTS

The research is partially supported by National Key R&D Program of China under Grant No. 2021ZD0110400 and No. 2021YFB2900103, Innovation Program for Quantum Science and Technology 2021ZD030 2900, China National Natural Science Foundation with No. 62132018 and No. 61932016, “Pioneer” and “Leading Goose" R&D Program of Zhejiang 2023C01029, the Fundamental Research Funds for the Central Universities WK2150110024, and the University Synergy Innovation Program of Anhui Province under Grant GXXT-2022- 049.

# REFERENCES

[1] Jayadev Acharya, Chris De Sa, Dylan J. Foster, and Karthik Sridharan. 2019. Distributed Learning with Sublinear Communication. In ICML, Vol. 97. PMLR, 40–50.   
[2] Aamir Ahmad, Guilherme Lawless, and Pedro U. Lima. 2017. An Online Scalable Approach to Unified Multirobot Cooperative Localization and Object Tracking. IEEE Trans. Robotics 33, 5 (2017), 1184–1199.   
[3] Khaled M. Alzoubi, Peng-Jun Wan, and Ophir Frieder. 2002. Message-optimal connected dominating sets in mobile ad hoc networks. In MobiHoc. ACM, 157– 164.

[4] Ofer Dekel, Ran Gilad-Bachrach, Ohad Shamir, and Lin Xiao. 2012. Optimal Distributed Online Prediction Using Mini-Batches. J. Mach. Learn. Res. 13 (2012), 165–202.   
[5] Dheeru Dua and Casey Graff. 2017. UCI Machine Learning Repository.   
[6] Cynthia Dwork, Aaron Roth, et al. 2014. The algorithmic foundations of differential privacy. Foundations and Trends® in Theoretical Computer Science 9, 3–4 (2014), 211–407.   
[7] Hossein Esfandiari, Amin Karbasi, Abbas Mehrabian, and Vahab S. Mirrokni. 2021. Regret Bounds for Batched Bandits. In AAAI. AAAI Press, 7340–7348.   
[8] Nima Eshraghi and Ben Liang. 2020. Distributed Online Optimization over a Heterogeneous Network with Any-Batch Mirror Descent. In ICML, Vol. 119. PMLR, 2933–2942.   
[9] Yuxuan Han, Zhicong Liang, Zhipeng Liang, Yang Wang, Yuan Yao, and Jiheng Zhang. 2022. Private Streaming SCO in ℓ?? geometry with Applications in High Dimensional Online Decision Making. In ICML, Vol. 162. PMLR, 8249–8279.   
[10] Elad Hazan. 2016. Introduction to Online Convex Optimization. Found. Trends Optim. 2, 3-4 (2016), 157–325.   
[11] S. Hettich and S. D. Bay. 1999. The UCI KDD Archive.   
[12] Roger Iyengar, Joseph P. Near, Dawn Song, Om Thakkar, Abhradeep Thakurta, and Lun Wang. 2019. Towards Practical Differentially Private Convex Optimization. In SP. IEEE, 299–316.   
[13] Prateek Jain, Pravesh Kothari, and Abhradeep Thakurta. 2012. Differentially Private Online Learning. In COLT, Vol. 23. JMLR.org, 24.1–24.34.   
[14] Anastasia Koloskova, Sebastian Stich, and Martin Jaggi. 2019. Decentralized Stochastic Optimization and Gossip Algorithms with Compressed Communication. In ICML, Vol. 97. PMLR, 3478–3487.   
[15] Jinlong Lei, Peng Yi, Yiguang Hong, Jie Chen, and Guodong Shi. 2020. Online Convex Optimization Over Erdos-Renyi Random Networks. In NeurIPS. 15591– 15601.   
[16] Chencheng Li, Pan Zhou, Li Xiong, Qian Wang, and Ting Wang. 2018. Differentially Private Distributed Online Learning. IEEE Trans. Knowl. Data Eng. 30, 8 (2018), 1440–1453.   
[17] Sen Lin, Mehmet Dedeoglu, and Junshan Zhang. 2021. Accelerating Distributed Online Meta-Learning via Multi-Agent Collaboration under Limited Communication. In MobiHoc. ACM, 261–270.   
[18] Xin Liu, Pan Zhou, Tie Qiu, and Dapeng Oliver Wu. 2020. Blockchain-Enabled Contextual Online Learning Under Local Differential Privacy for Coronary Heart Disease Diagnosis in Mobile Edge Computing. IEEE J. Biomed. Health Informatics 24, 8 (2020), 2177–2188.   
[19] Qingguo Lü, Xiaofeng Liao, Tao Xiang, Huaqing Li, and Tingwen Huang. 2021. Privacy Masking Stochastic Subgradient-Push Algorithm for Distributed Online Optimization. IEEE Trans. Cybern. 51, 6 (2021), 3224–3237.   
[20] Angelia Nedic, Alex Olshevsky, and Michael G. Rabbat. 2018. Network Topology and Communication-Computation Tradeoffs in Decentralized Optimization. Proc. IEEE 106, 5 (2018), 953–976.   
[21] Amin Shahraki, Mahmoud Abbasi, Amir Taherkordi, and Anca Delia Jurcut. 2022. A comparative study on online machine learning techniques for network traffic streams analysis. Comput. Networks 207 (2022), 108836.   
[22] Ohad Shamir. 2014. Fundamental Limits of Online and Distributed Algorithms for Statistical Learning and Estimation. In NeurIPS. 163–171.   
[23] Jianhan Song, Gustavo de Veciana, and Sanjay Shakkottai. 2022. Online learning for multi-agent based resource allocation in weakly coupled wireless systems. In MobiHoc. ACM, 111–120.   
[24] Beata Strack, Jonathan P DeShazo, Chris Gennings, Juan L Olmo, Sebastian Ventura, Krzysztof J Cios, and John N Clore. 2014. Impact of HbA1c measurement on hospital readmission rates: analysis of 70,000 clinical database patient records. BioMed research international 2014 (2014).   
[25] Abhradeep Guha Thakurta and Adam D. Smith. 2013. (Nearly) Optimal Algorithms for Private Online Learning in Full-information and Bandit Settings. In NeurIPS. 2733–2741.   
[26] Vishrant Tripathi and Eytan H. Modiano. 2021. An Online Learning Approach to Optimizing Time-Varying Costs of AoI. In MobiHoc. ACM, 241–250.   
[27] Dirk van der Hoeven, Hédi Hadiji, and Tim van Erven. 2022. Distributed Online Learning for Joint Regret with Communication Constraints. In ALT, Vol. 167. PMLR, 1003–1042.   
[28] Yuanyu Wan, Wei-Wei Tu, and Lijun Zhang. 2020. Projection-free Distributed√ Online Convex Optimization with ?? ( ?? ) Communication Complexity. In ICML, Vol. 119. PMLR, 9818–9828.   
[29] Yongyang Xiong, Jinming Xu, Keyou You, Jianxing Liu, and Ligang Wu. 2020. Privacy-Preserving Distributed Online Optimization Over Unbalanced Digraphs via Subgradient Rescaling. IEEE Trans. Control. Netw. Syst. 7, 3 (2020), 1366–1378.   
[30] Feng Yan, Shreyas Sundaram, S. V. N. Vishwanathan, and Yuan (Alan) Qi. 2013. Distributed Autonomous Online Learning: Regrets and Intrinsic Privacy-Preserving Properties. IEEE Trans. Knowl. Data Eng. 25, 11 (2013), 2483–2493.   
[31] Junlong Zhu, Changqiao Xu, Jianfeng Guan, and Dapeng Oliver Wu. 2018. Differentially Private Distributed Online Algorithms Over Time-Varying Directed Networks. IEEE Trans. Signal Inf. Process. over Networks 4, 1 (2018), 4–17.