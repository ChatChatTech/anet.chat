# Communication-Efficient Regret-Optimal Distributed Online Convex Optimization

Jiandong Liu, Lan Zhang, Fengxiang He, Chi Zhang, Shanyang Jiang, and Xiang-Yang Li, Fellow, IEEE

Abstract—Online convex optimization in distributed systems has shown great promise in collaboratively learning on data streams with massive learners, such as in collaborative coordination in robot and IoT networks. When implemented in communicationconstrained networks like robot and IoT networks, two critical yet distinct objectives in distributed online convex optimization (DOCO) are minimizing the overall regret and the communication cost. Achieving both objectives simultaneously is challenging, especially when the number of learners n and learning time T are prohibitively large. To address this challenge, we propose novel algorithms in typical adversarial and stochastic settings. Our algorithms significantly reduce the communication complexity of the algorithms with the state-of-the-art regret by a factor√ of $\mathcal { O } ( n ^ { 2 } )$ and O˜( nT ) in adversarial and stochastic settings, respectively. We are the first to achieve nearly optimal regret and communication complexity simultaneously up to polylogarithmic factors. We validate our algorithms through experiments on real-world datasets in classification tasks. Our algorithms with appropriate parameters can achieve $9 0 \% \sim 9 9 \%$ communication saving with close accuracy over existing methods in most cases.

Index Terms—Communication complexity, distributed online learning, convex optimization

# I. INTRODUCTION

D ISTRIBUTED online convex optimization (DOCO) [1]–[4] has shown promising performance in collaborative [4] has shown promising performance in collaborative learning on feedback data from clients served sequentially by massive learners. Besides loss or accuracy, a crucial criterion for DOCO algorithms is communication cost, especially in communication-constrained networks like robot and IoT networks. The energy cost of communications is orders of magnitude higher than that of local computation in these networks [5]–[7]. In distributed real-time coordination and localization in robot networks [8], [9], for example, robots collaborate to minimize the accumulated loss, measured by the difference between their predictions and the streaming observations of targets. High communication costs can render the algorithm impractical since bandwidth or communication power is typically limited

Manuscript received June 3, 2023; revised May 12, 2024. The research is partially supported by National Key R&D Program of China under Grant No. 2021ZD0110400, Innovation Program for Quantum Science and Technology 2021ZD0302900, China National Natural Science Foundation with No. 62132018, “Pioneer” and “Leading Goose” R&D Program of Zhejiang 2023C01029, the Fundamental Research Funds for the Central Universities WK2150110024, and Key Laboratory of Internet and industrial integration and innovation (CAICT), MIIT (Corresponding author: Xiang-Yang Li.)

Jiandong Liu, Lan Zhang, Chi Zhang, Shanyang Jiang, and Xiang-Yang Li are with the LINKE Lab, University of Science and Technology of China, Hefei, China (jdliu@mail.ustc.edu.cn, zhanglan@ustc.edu.cn, gzhnciha@mail.ustc.edu.cn, yang12@mail.ustc.edu.cn, xiangyangli@ustc.edu.cn).

Fengxiang He is with Artificial Intelligence and its Applications Institute, School of Informatics, University of Edinburgh, UK (F.He@ed.ac.uk). in these applications, leading to quick energy depletion among resource-constrained robots [10].

Existing works have designed several DOCO algorithms with low regret loss, a standard metric for the loss of models [11]–[13], or reduced communication complexity [2], [14]. However, the literature lacks a general theory for DOCO algorithms that can simultaneously achieve low regret loss and communication complexity. This work aims to achieve this challenging goal to make DOCO algorithms practical in communication-constrained networks. Each learner measures its (pseudo) regret loss as the difference between the (expected) accumulated loss incurred by its models and that incurred by the best single model. The algorithm’s communication complexity is evaluated by the message complexity [12], [15], which refers to the number of messages transmitted in the algorithm.

We consider two typical settings in DOCO: adversarial and stochastic. In the adversarial setting, feedback data can be arbitrary or adaptive to historical models. This setting covers applications where feedbacks vary vastly over time, such as in distributed tracking of moving targets in sensor networks [8]. In the stochastic setting, each learner’s feedback data follow a fixed distribution.1 This setting has wide applications in statistical learning, inference, and coordination in networks [1], [16].

To understand the limitations of DOCO, we establish communication complexity lower bounds to achieve the minimax regret loss, which represents the optimal worst-case regret loss for DOCO algorithms on arbitrary connected learner networks with arbitrary loss functions. We consider DOCO algorithms with n learners and learning time T . For adversarial DOCO, we prove that the lower bound is linear in T . For stochastic DOCO, the lower bound is nearly linear in n. Generally, the learning time T is significantly greater than the number of learners n. Therefore, our theory implies that algorithms in stochastic DOCO may be considerably more communication-efficient than those in adversarial DOCO.

Based on the above understanding, we propose novel DOCO algorithms that utilize each communication more effectively. For the adversarial setting, we design the dualblock BFS-tree-aided DOCO (DB-TDOCO) algorithm. DB-TDOCO updates models twice in two fine-tuned blocks each time the learners gather their gradients in a Breadth-First Search (BFS) tree. Compared with the traditional distributed mini-batch algorithm [13], DB-TDOCO enables more frequent

1The distributions of each learner’s obtained feedbacks in stochastic DOCO can be different. We include the results of the i.i.d. stochastic setting where all feedbacks are sampled from the same distribution in Appendix B in the supplementary material.

TABLE I: Minimax regret bounds, communication complexity lower bounds for regret-optimal DOCO, currently state-ofthe-art (SOTA) communication complexity for DOCO with the state-of-the-art regret, and our algorithms’ communication complexity. The Ω˜ (O˜) notation hides polylogarithmic factors in the number of learners n and learning time T when $T \gg n$ . 

<table><tr><td></td><td>Adversarial</td><td>Stochastic</td></tr><tr><td>Minimax regret</td><td> $\mathcal{O}(n^{3/2}\sqrt{T})$  (Cor. 1)</td><td> $\mathcal{O}(\sqrt{nT})$  [13]</td></tr><tr><td>Comm. lower bounds</td><td> $\Omega(T)$  (Cor. 1)</td><td> $\tilde{\Omega}(n)$  (Cor. 2)</td></tr><tr><td>SOTA algs.’ comm.</td><td> $\mathcal{O}(n^2T)$  [11]</td><td> $\mathcal{O}(n^{3/2}\sqrt{T})$  [13]</td></tr><tr><td>Our algs.’ comm.</td><td> $\mathcal{O}(T)$  (Cor. 3)</td><td> $\tilde{\mathcal{O}}(n)$  (Thm. 4)</td></tr></table>

and effective model updates. For the stochastic setting, we devise the distributed batch-to-online (DB2O) algorithm. DB2O significantly reduces communication complexity since the learners infrequently update models. Each updated model is obtained from a parallel run of a communication-efficient distributed batch optimization algorithm.

Our proposed algorithms offer notable theoretical advantages. DB-TDOCO and DB2O achieve nearly optimal communication complexity and regret bounds for adversarial and stochastic DOCO, respectively. This is the first time that such results have been achieved. Our results significantly reduce the state-of-theart communication complexity [11], [13] for algorithms with the currently state-of-the-art regret (cf. Table I). In Section VI, we show that our algorithms outperform the state-of-the-art on typical cycle, grid, and clique networks. In Appendix C, we additionally discuss the communication complexity on networks with specific diameters and establish our algorithms’ optimality.

In this paper, we address DOCO within a distributed computing framework [12], [17], where learners can decide when and with whom to communicate. Our algorithms involve learners coordinating to run convergecast and broadcast protocols [17] for exchanging gradients or models. This communication model is pertinent in networks like robot and IoT networks [8], [9], where broadcast and convergecast are applicable across wired or wireless devices [6], [8], [18], [19]. DOCO algorithms in [13], [20] are tailored to this paradigm. In contrast, an alternative body of literature [2], [11], [21] has devised decentralized DOCO algorithms, following the gossip pattern, for networks lacking coordination (e.g., unstable wireless networks [12], [22]). In the gossip framework, learners communicate with neighbors and locally average their models, representing a specific instance within our broader communication model.

We assess our algorithms by conducting distributed online logistic regression on real-world datasets [23], [24]. Results show that our algorithms achieve substantial communication savings, up to 95% compared to the state-of-the-art [11], [25], while maintaining comparable accuracy in the adversarial setting. In the stochastic setting, communication savings range from 90% to 99% compared to the state-of-the-art [13], with comparable accuracy, achieved through appropriate parameter selection.

# II. RELATED WORK

DOCO has been widely adopted in distributed learning systems that require real-time AI service [1]–[4], [26]. As many distributed systems operate on communication-constrained networks, communication-efficient and effective learning algorithms have become highly attractive [2], [4], [27]. In adversarial DOCO, the decentralized gossip algorithm [11], [12] currently achieves the state-of-the-art regret of $\mathcal { O } ( \Gamma n ^ { 3 / 2 } \sqrt { T } )$ , where Γ measures the connectivity of the learner network, ranging from $\mathcal { O } ( 1 )$ to $\mathcal { O } ( n ^ { 2 } )$ for different networks. The worstcase communication cost of gossip is $\mathcal { O } ( n ^ { 2 } T )$ . Wan et al. [2] introduced the decentralized block online conditional gradient algorithm (D-BOCG), which offers communication savings over gossip by a factor of $\mathcal { O } ( \sqrt { T } )$ , with a regret enlarged by a factor of $\mathcal { O } ( T ^ { 1 / 4 } )$ . For stochastic DOCO, the distributed mini-batch algorithm (DMA) [13] achieves the minimax regret with the currently state-of-the-art communication cost of $\mathcal { O } ( n ^ { 3 / 2 } \sqrt { T } )$ . Although DMA was originally designed for i.i.d. stochastic data, it naturally works for learners with diverse feedback distributions and the same bounds hold. Besides message complexity, van der Hoeven et al. [28], Acharya et al. [14], and Tu et al. [4] investigate DOCO with reduced bit complexity based on gradient quantization, a common technique for compressing message bit-length in learning tasks.

Another area of research focuses on the communication complexity lower bound of DOCO. Wan et al. [29] demonstrate that, for the dependence on T , the learners need Ω(T ) communication cost to achieve the minimax regret in adversarial DOCO. van der Hoeven et al. [28] consider a DOCO problem where one learner wakes up at each time and serves a client. They establish the regret lower bounds for this DOCO problem with different budgets for bit complexity. Wang et al. [25] proved the $\Omega ( n )$ communication complexity lower bound of distributed stochastic bandits to achieve the minimax regret.

Some of our analysis is inspired by online convex optimization with delayed feedback (OCOD) [20], [30], [31] and batched bandits [32]–[34]. On the one hand, OCOD provides an algorithmic framework for online learning in scenarios where feedback data are delayed due to networking or communication constraints as we encounter in DOCO. On the other hand, batched bandits investigate the regret of bandit online optimization where the update times of models are limited. These works provide insights into the regret analysis of DOCO, where learners cannot update models frequently due to a lack of information under communication constraints.

Despite great contributions in various aspects, the literature lacks a comprehensive analysis of the communication complexity lower bounds for regret-optimal DOCO. Furthermore, there is a lack of algorithms that attain these lower bounds.

# III. PROBLEM FORMULATION

We formalize the problem settings for online convex optimization (OCO) and distributed OCO (DOCO).

Online convex optimization: In OCO, an agent acts as a learner at each time step $t \in [ T ]$ ] to optimize an AI model using streaming data. More specifically, the learner handles incoming clients based on a model parameter $x _ { t } \in { \mathcal { C } } .$ , where $\mathcal { C } \subset \mathbb { R } ^ { d }$ is the feasible region. The client then provides feedback data $\xi _ { t }$ to the learner. The learner derives the loss function $f _ { t } ( \cdot ) = f ( \cdot ; \xi _ { t } )$ from a function f and updates $x _ { t + 1 }$ based on $f _ { t } ( \cdot )$ .

Distributed OCO: DOCO extends OCO in distributed settings, where n agents collaborate in learning using their data streams. These n learners communicate in a connected network, as shown in Fig. 1. At each time $t \in [ T ]$ , each learner $i \in [ n ]$ serves a client using $x _ { t } ^ { i } \in \mathcal { C }$ , with $\mathcal { C } \subset \mathbb { R } ^ { d }$ denoting the feasible region. The client then sends feedback data $\xi _ { t } ^ { i }$ to learner $i ,$ which may vary for different i due to clients’ unique preferences or noisy feedbacks $( \mathrm { e . g . }$ , in distributed tracking based on noisy observations). The performance of $\boldsymbol { x } _ { t } ^ { i }$ is evaluated by the cumulative loss function across all client feedbacks at time t. More precisely, given a predefined function $f ( \cdot ; \xi )$ with $\xi$ being an arbitrary feedback, the loss function is expressed as $\begin{array} { r } { \bar { f _ { t } } ~ = ~ \sum _ { i = 1 } ^ { n } \bar { f _ { t } ^ { i } } } \end{array}$ , where $f _ { t } ^ { i } ( \cdot ) ~ = ~ f ( \cdot ; \xi _ { t } ^ { i } )$ . Learner i can communicate with neighbors and update $x _ { t + 1 } ^ { i }$ using a partial loss function $f _ { t } ^ { i } = f ( \cdot ; \xi _ { t } ^ { i } )$ and messages from neighbors.

![](images/f17f4ab374e88696ea32d0a1e9abfa291c1ae695fe6472dee2f9893752483c0c.jpg)



Fig. 1: An example learner network in DOCO and the service pattern of learner $i \in [ n ]$ in the network.

Feedback Settings: In DOCO, two typical feedback settings are considered: adversarial and stochastic. In adversarial DOCO, the clients at time t select feedback $\xi _ { t } ^ { i } , ~ i ~ \in ~ [ n ]$ , arbitrarily or adaptively, even based on historical models and messages. In stochastic DOCO, the feedback $\xi _ { t } ^ { i }$ is sampled from a distribution $\mathbb { P } _ { i }$ for $i \in [ n ]$ ].

Network Topology: Similar to existing DOCO algorithms [2], [11], [13], we consider network topologies as arbitrary undirected connected graphs. Typical topologies in DOCO applications include cycles, grids, and cliques [2], [11], [22].

Communication Pattern: We focus on DOCO algorithms employing the standard static communication pattern [1], [2], [13]. In this setup, learners operate within a static communication pattern, where neighboring learners i and j for $i , j \in [ n ]$ communicate at specific time points t, determined by the learner network and the total learning time T .

Within this pattern, learners can coordinate to exchange messages such as gradients or models. Two widely adopted communication protocols in DOCO are convergecast and broadcast [13], [20], facilitating the aggregation and distribution of messages in a BFS tree of the network. The procedures of convergecast and broadcast are presented in Fig. 2. Both protocols involve an ${ \mathcal { O } } ( n )$ communication cost and a delay proportional to the network’s diameter. Example applications include distributed real-time localization [8], [9], where robots can convergecast gradients evaluated on the current localization model to a single unit for updates, followed by broadcasting the updated model.

Performance Metrics: The performance of each learner’s model sequence is measured using the (pseudo) regret loss. In the adversarial setting, each learner $i \in [ n ]$ aims to minimize the regret loss [11], [12]:

$$
\mathcal {R} _ {i} (T) \triangleq \Sigma_ {t = 1} ^ {T} f _ {t} (x _ {t} ^ {i}) - \min _ {x \in \mathcal {C}} \Sigma_ {t = 1} ^ {T} f _ {t} (x). \tag {1}
$$

1: procedure CONVERGECAST({yi}i∈[n], T )   
2: Each leaf learner i in $\tau$ sends $z _ { i } \stackrel { \cdot } { = } y _ { i }$ to its parent   
3: Upon receiving $\{ z _ { i } \} _ { i \in N _ { j } }$ from all its children, each learner $j$ computes

$$
z _ {j} \leftarrow y _ {j} + \Sigma_ {i \in N _ {i}} z _ {i},
$$

where $N _ { j }$ denotes the children set of learner j

4: After computing $z _ { j } ,$ learner j sends $z _ { j }$ to its parent if learner $\bar { j }$ is non-root

5: end procedure   
6: procedure BROADCAST $( y , \tau )$   
7: The root learner in T sends y to its children   
8: Upon receiving y from its parent, each non-leaf learner j sends y to its children   
9: end procedure

Fig. 2: Convergecast and Broadcast procedures in a BFS tree T of the learner network [17], where $y _ { i }$ represents the vector owned by learner $i \in [ n ]$ and $y$ is owned by the root learner.

In the stochastic setting, let $\bar { f } _ { i } ( x ) \triangleq \mathbb { E } _ { \xi \sim \mathbb { P } _ { i } } [ f ( x ; \xi ) ]$ and ${ \bar { f } } ( x ) \triangleq$ $\textstyle \sum _ { i = 1 } ^ { n } { \bar { f } } _ { i } ( x )$ n . Each learner i seeks to minimize the expected pseudo regret loss [13]:

$$
\bar {\mathcal {R}} _ {i} (T) \triangleq \mathbb {E} \left[ \Sigma_ {t = 1} ^ {T} \left[ \bar {f} \left(x _ {t} ^ {i}\right) - \min _ {x \in \mathcal {C}} \bar {f} (x) \right] \right]. \tag {2}
$$

For instance, in distributed real-time localization, the loss function quantifies the sum of distances between a prediction of the localization model and all robots’ noisy observations. Each robot aims to minimize the regret loss to reduce its cumulative localization error. In this paper, we focus on algorithms with the minimax regret, i.e., the optimal regret loss achieved by DOCO algorithms under worst-case networks and feedbacks (or feedback distributions in the stochastic setting).

Another performance metric of a DOCO algorithm is its communication complexity. In this paper, the communication complexity is quantified by the number of transmitted messages, i.e., the message complexity [12], [17]. In DOCO algorithms, a message typically represents a gradient or model parameter.

Conditions on Loss Functions: This paper considers standard loss functions that are Lipschitz, convex, smooth, and bounded. The feasible region C for the models is assumed to be convex, compact, and adhere to a fatness condition.

Definition 1 (Convexity). A function f is convex within a convex compact set $\mathcal { C } \subset \mathbb { R } ^ { d }$ if, for all $x , y \in { \mathcal { C } } ,$ ,

$$
f (y) - f (x) \geq \langle \nabla f (x), y - x \rangle .
$$

Definition 2 (Lipschitz). A function f is L-Lipschitz for some L > 0 in a convex compact set C if, for all $x , y \in { \mathcal { C } } ,$ ,

$$
| f (x) - f (y) | \leq L \| x - y \|.
$$

Here, ∥·∥ denotes the Euclidean norm.

Definition 3 (Smoothness). A function f is LG-smooth for some $L _ { G } > 0 ~ i f ,$ for all $x , y \in { \mathcal { C } }$ ,

$$
\left\| \nabla f (x) - \nabla f (y) \right\| \leq L _ {G} \| x - y \|.
$$

Definition 4 (Bounded function and fat set [35]). A function $f$ is bounded $i f \left| f ( x ) \right| \leq M$ for all $x \in { \mathcal { C } } ,$ , where $M > 0 .$ . A set C is fat if it contains an $\ell _ { \infty } { - } b a l l$ of radius $\Omega \left( p o l y ( \textstyle { \frac { 1 } { d } } ) \right)$ .

The assumptions of Lipschitz, convexity, smoothness, and boundedness on the loss functions, and the convexity and compactness assumptions on the feasible region C, are widely adopted in the DOCO literature [1], [2], [12], [13]. The fatness assumption is essential for cutting-plane-based algorithms [35], [36], ensuring sufficient interior space for search. By the analysis in [35], this assumption holds for sets of the form $\{ x \in \mathbb { R } ^ { d } : h _ { i } ( x ) \leq 0 , i \in [ k ] \}$ , where each $h _ { i } ( \cdot )$ is Lipschitz and smooth for $i \in [ k ] .$ . However, this assumption does not hold for constraints containing equalities, e.g., a surface in $\mathbb { R } ^ { d }$ We can adapt our analysis and algorithms to these regions by operating on the low-dimensional manifold induced by these equalities, which we leave for future work.

Many real-world loss functions satisfy Definitions 1-4. Logistic loss functions [20] and smoothed hinge loss functions [37] with bounded regions and samples, widely adopted in classification tasks [2], [13], [20], [37], and ridge regression functions utilizing bounded regions and samples [20] popular in regression tasks [1], [20], [38], align with these definitions. A specific instance of loss functions satisfying Definitions 1–4 is the linear function with a constant dimension $d > 1$ :

$$
\begin{array}{l} \begin{array}{l} f (x) = \langle x, z \rangle \text {   for   some   } z \in [ 0, 1 ] ^ {d}, \\ \mathcal {C} _ {n} = \{\dots , \mathbb {R} ^ {d} | 1, 2 \| _ {n - 1} \} \end{array} \tag {3} \\ \mathcal {C} = \{x \in \mathbb {R} _ {\geq 0} ^ {d} | 1 \leq \| x \| _ {1} \leq 2 \}. \\ \end{array}
$$

In adversarial DOCO, we assume that $f _ { t } ^ { i }$ for $i \in [ n ]$ and $t \in [ T ]$ satisfy Definitions 1–4 with common parameters $L , L _ { G }$ , and M. In stochastic DOCO, we assume that $f ( x ; \xi )$ for all possible $\xi \sim \mathbb { P } _ { i } , i \in [ n ]$ , satisfies Definitions 1–4. Specifically, in stochastic DOCO, we also consider broader non-Lipschitz functions satisfying the following milder condition.

Definition 5 (Bounded gradient variance and expected initialization risk [13]). Functions $f ( x ; \xi ) , \xi \sim \mathbb { P } _ { i } f o r ~ i \in [ n ]$ , have bounded gradient variance $\sigma ^ { 2 } > 0$ and expected initialization risk $R > 0$ in a compact convex C $i f , f o r \ x \in \mathcal { C } , i \in [ n ]$ ,

$$
\left\{ \begin{array}{l} \mathbb {E} _ {\xi \sim \mathbb {P} _ {i}} \| \nabla f (x; \xi) - \nabla \bar {f} _ {i} (x) \| ^ {2} \leq \sigma^ {2} \\ \bar {f} _ {i} (\hat {x}) - \bar {f} _ {i} (x ^ {*}) \leq R \end{array} \right.
$$

where $\bar { f } _ { i } ( x ) = \mathbb { E } _ { \xi \sim \mathbb { P } _ { i } } [ f ( x ; \xi ) ] , \ x ^ { * } \ \triangleq \arg \operatorname* { m i n } _ { x \in \mathcal { C } } \Sigma _ { i = 1 } ^ { n } \bar { f } _ { i } ( x ) ,$ and ${ \hat { x } } \triangleq \arg \operatorname* { m i n } _ { x \in { \mathcal { C } } } \| x \| .$ .

The condition above is a relaxed version of the Lipschitz condition as $f ( x ; \boldsymbol { \xi } ) , \boldsymbol { \xi } ~ \sim ~ \mathbb { P } _ { i }$ for $\textit { i } \in \ [ n ]$ have gradient variance $L ^ { 2 }$ and expected initialization risk $L \| \mathcal C \|$ if it is $L _ { - }$ Lipschitz, where $\| \mathcal { C } \| \triangleq \operatorname* { m a x } _ { x , y \in \mathcal { C } } \| x - y \|$ . This condition can accommodate broader loss functions like logistic and ridge regression loss functions with noisy gradients [4], [39].

# IV. COMMUNICATION COMPLEXITY LOWER BOUNDS

To determine the limits of DOCO, we establish lower bounds on the communication complexity for regret-optimal algorithms. Let r denote the communication budget, i.e., the maximum number of messages that can be transmitted by the learners. We construct hard instances for DOCO where any algorithm will experience suboptimal regret when r falls below a lower bound. In our analysis, we make no assumptions on the bit-lengths of the messages. Consequently, our lower bounds remain valid even when the bit-lengths of the messages are unbounded. This is because we utilize information-theoretic analysis on feedback information. The learners must acquire information related to feedbacks at specific times and promptly update models to achieve the minimax regret. We present brief outlines of the proofs for our theoretical results in this section and defer the full proofs to Appendices D and E in the supplementary material.

![](images/5c2fa3027ed0a9920e51f7bcf888d12a3184ea04f3e65967a61242407ab6186e.jpg)



Fig. 3: Claw-shaped network. $n ^ { \prime } = \lceil n / 2 \rceil$ .

# A. Communication Complexity for Adversarial DOCO

We begin by examining the communication complexity of adversarial DOCO. We construct a hard instance where the regret loss is $\Omega ( n ^ { 3 / 2 } T / \sqrt { r } )$ for communication budgets r that are not sufficiently large, as presented in Theorem 1.

Theorem 1. Consider adversarial DOCO with linear loss functions (cf. Eq. (3)) and static communication patterns. There exists a learner network and functions $\{ f _ { t } ^ { i } \} _ { t \in [ T ] , i \in [ n ] }$ such that:

$$
\mathcal {R} _ {1} (T) = \Omega \big (n ^ {3 / 2} \max \{\sqrt {T}, T / \sqrt {r} \} \big), \tag {4}
$$

where n is the number of learners, T is the learning time, and r is the communication budget.

As a corollary of Theorem 1, we need $r = \Omega ( T )$ to achieve the minimax regret $\mathcal { O } ( n ^ { 3 / 2 } \sqrt { T } )$ .

Corollary 1. Consider adversarial DOCO with loss functions satisfying Definitions 1–4 and static communication patterns. The communication complexity to achieve the minimax regret $\mathcal { O } ( n ^ { 3 / 2 } \sqrt { T } )$ is $\Omega ( T )$ with respect to n and T .

The theory demonstrates that the necessary communication cost in adversarial DOCO increases at a minimum rate of linearly with respect to the learning time T . This result is substantiated by constructing a specific problem instance in which any algorithm will experience suboptimal regret if the communication budget is inadequate. On one hand, the $\Omega ( T )$ lower bound is disheartening as it indicates that the learners must communicate frequently during the course of the algorithm. On the other hand, the bound is encouraging as it is independent of the number of learners $n .$ Our bound suggests that the currently state-of-the-art communication complexity of $\mathcal { O } ( n ^ { 2 } T )$ (cf. Table I) may be suboptimal with regard to n. Proof sketch of Theorem 1.

1) Constructing the network: We construct the learner network as a claw-shaped one in Fig. 3. In this network, the transmission of each message from a learner $i > n ^ { \prime }$ to learner 1 requires $\Omega ( n )$ timeslots and communication budget. By the analysis in OCO with delayed feedback [30], the $\Omega ( n )$ delay can magnify learner 1’s regret by an $\Omega ( { \sqrt { n } } )$ factor. This attribute is critical for establishing the $\Omega ( n ^ { 3 / 2 } \sqrt { T } )$ regret lower bound when the communication budget r is sufficiently large.   
2) Constructing loss functions: Let $t _ { k } + 1$ be the first time learner 1 receives information from learner $i > n ^ { \prime }$ sent at time $t _ { k - 1 } < t \leq t _ { k }$ , and m be the number of such $t _ { k }$ . Let

TABLE II: Regret bounds, communication complexity, and assumptions on loss function for DOCO algorithms for the dependence of the number of learners n and learning time $T$ when $T \gg n .$ . gossip [11], [12] and D-BOCG [2] respectively achieve state-of-the-art regret and communication complexity in adversarial DOCO. The parameter Γ in gossip and D-BOCG is the inverse of the spectral gap of the network’s gossip matrix [40], ranging from O(1) to $O ( n ^ { 2 } )$ . DMA [13] is the stochastic DOCO algorithm achieving both state-of-the-art metrics. Our DB-TDOCO algorithm has two variants: one with parameters independent of the network topology, and the other dependent on network diameter $D < n$ . $\mathrm { D B } 2 0 _ { a }$ and $\mathrm { D B 2 O } _ { c }$ are two variants of our DB2O algorithm with cutting-plane [35] and accelerated gradient descent [41] update rules.

<table><tr><td>Feedbacks</td><td>DOCO algorithm</td><td>Communication complexity</td><td>Regret bounds</td><td>Assumptions on loss functions</td></tr><tr><td rowspan="4">Adversarial</td><td>gossip [11], [12]</td><td> $\mathcal{O}(n^{2}T)$ </td><td> $\mathcal{O}(n^{3/2}\Gamma\sqrt{T})$ </td><td rowspan="4">Definitions 1 and 2</td></tr><tr><td>D-BOCG [2]</td><td> $\mathcal{O}(n^{2}\sqrt{T})$ </td><td> $\mathcal{O}(n^{3/2}\Gamma T^{3/4})$ </td></tr><tr><td>DB-TDOCO(topology-independent)</td><td> $\mathcal{O}(T)$ </td><td> $\mathcal{O}(n^{3/2}\sqrt{T})$ </td></tr><tr><td>DB-TDOCO(diameter-dependent)</td><td> $\mathcal{O}(nT/D)$ </td><td> $\mathcal{O}(n\sqrt{DT})$ </td></tr><tr><td rowspan="3">Stochastic</td><td>DMA [13]</td><td> $\mathcal{O}(n^{3/2}\sqrt{T})$ </td><td> $\mathcal{O}(\sqrt{nT})$ </td><td rowspan="2">Definitions 1, 3, and 5</td></tr><tr><td>DB2Oa</td><td> $\tilde{\mathcal{O}}(n^{5/4}T^{1/4})$ </td><td> $\tilde{\mathcal{O}}(\sqrt{nT})$ </td></tr><tr><td>DB2Oc</td><td> $\tilde{\mathcal{O}}(n)$ </td><td> $\tilde{\mathcal{O}}(\sqrt{nT})$ </td><td>Definitions 1, 4, and 5</td></tr></table>

$t _ { 0 } = 0$ and $t _ { m + 1 } = T$ . We construct linear loss functions as in Eq. (3). For learner $i > n ^ { \prime } .$ , we sample $\hat { z } _ { k }$ uniform in $\{ 0 , 1 \} ^ { d }$ for $k \in [ m + 1 ]$ , and set $f _ { t } ^ { i } ( x ) = \langle x , { \hat { z } } _ { k } \rangle$ for $t _ { k - 1 } < t \leq t _ { k }$ . The constructed loss for learner $i \leq n ^ { \prime }$ is zero. Learner 1 then incurs high regret loss since its models are independent of the functions of learners $n ^ { \prime } + 1$ to $n .$ .

3) Lower bounding the regret: We establish that:

$$
\mathbb {E} [ \mathcal {R} _ {1} (T) ] = \Omega (n T / \sqrt {m})
$$

based on our loss functions. In the claw-shaped network, $m =$ $\mathcal { O } ( \operatorname* { m i n } ( T / n , r / n ) )$ . Theorem 1 can then be deduced.

Comparison with existing works: Our lower bound on communication complexity improves upon the result in [29], which proves a lower bound of $\Omega ( T )$ based on a hard instance satisfying Definitions 1-4. Notably, their work does not consider the dependence on the number of learners $n ,$ and hence does not reveal the suboptimality of the state-of-the-art algorithm’s communication complexity of $\mathcal { O } ( n ^ { 2 } T )$ [11]. While Wan et al. [29] employ similar loss functions to ours (cf. Eq. (3)), which rely on specific communication time points $t _ { k }$ for $k \in [ m ]$ , they do not consider the influence of transmission delays and network topologies in their construction. In contrast, we obtain tighter bounds by selecting $t _ { k }$ based on the communication budget and transmission delays in a sophisticated network.

# B. Communication Complexity for Stochastic DOCO

For the stochastic setting, we prove that a hard instance exists where the regret loss is $\omega ( { \sqrt { n T } } )$ for a low communication budget r. We summarize the result in Theorem 2.

Theorem 2. Consider stochastic DOCO with linear loss functions (cf. $E q . \ ( 3 ) )$ and static communication patterns. There exists a learner network and loss functions $f ( x ; \xi _ { t } ^ { i } ) f o r ~ i \in [ n ]$ and $t \in [ T ]$ , where $\xi _ { t } ^ { i } \sim \mathbb { P } _ { i } f o r$ some distribution $\mathbb { P } _ { i } ,$ , such that:

$$
\bar {\mathcal {R}} _ {1} (T) = \Omega \left(\max \left\{\min \left\{n ^ {2}, n T \right\}, (n T) ^ {\frac {1}{2 - 2 ^ {- 2 r / n}}} \right\}\right), \tag {5}
$$

where n is the number of learners, T is the learning time, and r is the communication budget.

Via similar arithmetic computations as in batched bandits [32], we need $r = \Omega ( n \ln T )$ to make $\bar { \mathcal { R } } _ { 1 } ( T )$ in Eq. (5) equal to $\mathcal { O } ( \sqrt { n T } )$ , the minimax regret, when $T \gg n$ .

Corollary 2. Consider stochastic DOCO with loss functions satisfying Definitions 1–4 and static communication patterns. The communication complexity to achieve the minimax regret $\mathcal { O } ( \sqrt { n T } )$ is $\Omega ( n \ln \ln T )$ with respect to n and T .

The theory shows that for stochastic DOCO, the lower bound on communication complexity required to attain the minimax regret is $\tilde { \Omega } ( n )$ , which is almost insensitive to T . We establish this bound with an instance where any algorithm fails to achieve the optimal regret if their communication budget is below our lower bound. Initially, the tightness of this bound may appear dubious as the regret seems to rise swiftly in $T$ if the communication cost is nearly constant in T . Nevertheless, once this bound is reached, it is highly advantageous as the learning time tends to be lengthy in real-world applications [1], [13].

# Proof sketch of Theorem 2.

1) Constructing the network: Similarly, as in adversarial DOCO, we take the claw-shaped learner network in Fig. 3.   
2) Constructing loss functions: We sample ℓ uniformly from $[ d ]$ . The loss functions are as in Eq. $( 3 ) , \mathrm { i . e . , } f ( x ; \xi _ { t } ^ { i } ) = \left. x , \xi _ { t } ^ { i } \right.$ . For learner $i \leq n ^ { \prime } , \xi _ { t } ^ { i }$ is an all-zero vector. For learner $i > n ^ { \prime } ,$ the ℓ-th coordinate of $\xi _ { t } ^ { i }$ is drawn from the Bernoulli distribution with mean $\begin{array} { r } { \frac { 1 } { 2 } - \epsilon , } \end{array}$ and the other coordinates are uniform in {0, 1}. We tune the parameter ϵ to maximize learner 1’s regret.   
3) Lower bounding the regret: Let $t _ { k } , k \in [ m ]$ be the time points we defined in the proof sketch of Theorem 1. By optimally tuning the parameter ϵ in the loss, we derive that:

$$
\mathbb {E} _ {\ell} [ \bar {\mathcal {R}} _ {1} (T) ] = \Omega (n \min \{n, T \} + n ^ {\frac {1}{2 - 2 - m}} T ^ {\frac {1}{2 - 2 - m}}).
$$

It holds that $m \leq r / n ^ { \prime } \leq 2 r / n$ in the claw-shaped network. Theorem 2 then follows.

Comparison with existing works: To our best knowledge, this is the first work that analyzes the communication complexity for general DOCO in the stochastic setting.

# V. COMMUNICATION-EFFICIENT DOCO ALGORITHM

Building on the insights from our lower bound analysis, we design two novel DOCO algorithms: dual-block BFS-tree-aided DOCO (DB-TDOCO) and distributed batch-to-online (DB2O). These algorithms optimize communication resource utilization, achieving optimal regret and communication complexity in the number of learners n and learning time $T ,$ as outlined in

Section IV, within polylogarithmic factors. Proof sketches of these results are presented in this section, with details deferred to Appendices G and H in the supplementary material.

In Table II, we compare the performance of our algorithms with state-of-the-art [2], [11]–[13]. Our DB-TDOCO and $\mathrm { D B } 2 0 _ { a }$ algorithms notably reduce communication complexity while maintaining comparable or lower regret, under the same assumptions as gossip and DMA, respectively, which achieve top-tier regret for adversarial and stochastic DOCO. They reduce the communication cost of gossip and DMA by $\mathcal { O } ( n ^ { 2 } )$ and $\tilde { \mathcal { O } } ( ( n T ) ^ { 1 / 4 } )$ factors, respectively. Furthermore, our DB2Oc reduces the communication cost of DMA by an $\tilde { \mathcal { O } } ( \sqrt { n T } )$ factor, assuming bounded loss functions and a fat feasible region (cf. Definition 4) while relaxing the smoothness assumption (cf. Definition 3). Notably, our algorithms handle broader functions with milder assumptions compared to those in Section IV. Specifically, DB-TDOCO accommodates convex and Lipschitz loss functions, including non-smooth and unbounded ones like hinge loss functions with bounded regions and samples in SVMbased classifications [11], even with additive noise. Meanwhile, DB2Oc is suitable for convex and bounded functions with bounded gradient variance, such as hinge loss with noisy gradients [39]. Finally, DB-TDOCO and $\mathrm { D B } 2 0 _ { a }$ apply to nonfat feasible regions, such as the constrained simplex in linear programming [42], [43]. Our bounds in Section IV remain valid for these milder assumptions as we construct hard instances under stricter conditions that inherently fulfill the milder ones.

# A. Algorithm Design for the Adversarial Setting

Our adversarial DOCO algorithm is inspired by online convex optimization with delayed feedback (OCOD) [30]. OCOD research shows that a feedback delay of $\Theta ( n )$ time points leads to regret loss increasing by an $\mathcal { O } ( \sqrt { n } )$ factor. This is due to difficulties in the model catching up with variations in other learners’ collected adversarial feedbacks in time. In DOCO, through convergecast (cf. Fig. 2), learners can aggregate their gradients at each time to a single learner, requiring ${ \mathcal { O } } ( n )$ time points and communication cost. Then, this learner updates and broadcasts models, achieving a minimax regret of $\mathcal { O } ( n ^ { 3 / 2 } \sqrt { T } )$ . Nonetheless, this approach incurs a communication cost of $\mathcal { O } ( n T )$ . To minimize communication cost to (T ), learners communicate gradients in blocks, with the block size finely tuned to maintain the minimax regret.

Building on the aforementioned insight, we propose the dualblock BFS-tree-aided DOCO (DB-TDOCO) algorithm, which achieves improved performance by updating models in finely tuned blocks. We divide the learning time into m + 1 intervals $[ t _ { k - 1 } + 1 , t _ { k } ] , k \in [ m + 1 ]$ ], where $t _ { 0 } = 0$ and $t _ { m + 1 } = T$ Each interval $[ t _ { k - 1 } + 1 , t _ { k } ]$ is further divided into two blocks: $I _ { 2 k - 1 } \triangleq \left[ t _ { k - 1 } + 1 , t _ { k } - 2 \mu \right]$ and $I _ { 2 k } \triangleq [ t _ { k } - 2 \mu + 1 , t _ { k } ]$ , where $\mu$ denotes the height of a Breadth-First Search (BFS) tree of the learner network. Within each interval $[ t _ { k - 1 } + 1 , t _ { k } ]$ , learners update models twice in blocks $I _ { 2 k - 1 }$ and $I _ { 2 k }$ based on gradients of previous blocks communicated in the BFS tree. The model update process of DB-TDOCO is illustrated in Fig. 4, and the detailed algorithm is presented in Alg. 1.

The dual-block model updates in DB-TDOCO enable all loss functions to contribute to updating models. The traditional minibatch updates [13] cannot achieve this target, which neglects feedbacks when learners convergecast/broadcast messages (i.e., during $\left[ t _ { k } - 2 \mu , t _ { k } \right]$ for $k \in [ m ] )$ . DB-TDOCO achieves the minimax regret. Besides, we make DB-TDOCO communicationefficient by tuning the number of intervals m + 1 optimally.

![](images/84725eec4d507128666ffe15f81c85d341c61c9e4abe51cca3baba2eed5b347e.jpg)



Fig. 4: Model updates in DB-TDOCO. $\hat { f } _ { 2 k - 2 }$ and $\hat { f } _ { 2 k - 1 }$ represent block loss functions within blocks $I _ { 2 k - 2 } \triangleq [ t _ { k - 1 } -$ $2 \mu + 1 , t _ { k - 1 } ]$ and $I _ { 2 k - 1 } \triangleq \left[ t _ { k - 1 } + 1 , t _ { k } - 2 \mu \right]$ , respectively. Here, size. $\begin{array} { r } { \hat { f } _ { \ell } \triangleq \frac { 1 } { n \mathbb { Z } } \sum _ { s \in I _ { \ell } } f _ { s } } \end{array}$ for each ight of th $\ell ,$ where I is the largest block learner network’s BFS tree. $\Pi _ { \mathcal { C } }$ projects models onto the feasible region .

# Theoretical advantages of DB-TDOCO.

We study the regret and communication complexity of DB-TDOCO with arbitrary m and $\{ t _ { k } \} _ { k \in [ m ] }$ in Theorem 3.

Theorem 3. Let the loss functions $\{ f _ { t } ^ { i } \} _ { t \in [ T ] , i \in [ n ] }$ satisfy Definitions 1 and $^ { 2 , }$ and the time points $\{ t _ { k } \} _ { k \in [ m ] }$ satisfy

$$
t _ {k} - t _ {k - 1} > 2 \mu + 1 \text {   for   } k \in [ m + 1 ].
$$

DB-TDOCO features $\mathcal { O } ( n \mathbb { Z } \sqrt { m } )$ regret with $\mathcal { O } ( m n )$ communication cost, where $2 m + 2$ is the number of blocks and I is the largest length of blocks $\left\{ I _ { k } \right\} _ { k \in [ 2 m + 2 ] } .$ .

Leveraging the results from Theorem 3, DB-TDOCO can attain the optimal regret and communication complexity, as established in Corollary 2, by selecting a specific value of m and $\{ t _ { k } \} _ { k \in [ m ] }$ . We provide the details in Corollary 3.

Corollary 3. Let the loss functions $\{ f _ { t } ^ { i } \} _ { t \in [ T ] , i \in [ n ] }$ satisfy Definitions 1 and 2. In DB-TDOCO, by choosing

$$
m = \left\lfloor T / (2 n) \right\rfloor - 1 \text {   and   } t _ {k} = 2 n k \text {   for   } k \in [ m ] \tag {7}
$$

in Alg. 1, the regret bound is $\mathcal { R } _ { i } = \mathcal { O } ( n ^ { 3 / 2 } \sqrt { T } ) ~ f o r ~ i \in [ n ] .$ and the communication cost is O(T ).

Furthermore, we discover that DB-TDOCO can surpass the minimax regret $\mathcal { O } ( n ^ { 3 / 2 } \sqrt { T } )$ by selecting a different value of m and $\{ t _ { k } \} _ { k \in [ m ] }$ for networks with specific diameters D.

Corollary 4. Let the loss functions $\{ f _ { t } ^ { i } \} _ { t \in [ T ] , i \in [ n ] }$ satisfy Definition 1 and 2. In DB-TDOCO, by choosing

$$
m = \left\lfloor T / (3 \mu) \right\rfloor - 1 \text {   and   } t _ {k} = 3 \mu k \text {   for   } k \in [ m ], \tag {8}
$$

we obtain the regret $\mathcal { R } _ { i } = \mathcal { O } ( n \sqrt { D T } )$ for $i \in [ n ]$ , and the communication cost is $\mathcal { O } ( n T / D )$ , where $\mu$ is the BFS tree’s height and D is the network’s diameter.

As shown in Corollary 4, DB-TDOCO with parameters specified in Eq. (8) reduces the minimax regret by a factor of $\mathcal { O } ( \sqrt { n / D } )$ , where the diameter D varies from 1 to $n - 1$ . Furthermore, we demonstrate in Appendix C in the supplementary material that the regret and communication cost of DB-TDOCO in the diameter-dependent setting is optimal.

Algorithm 1 Dual-Block BFS-tree-aided DOCO (DB-TDOCO)   
1: Input: BFS tree T, number of intervals $m+1$ , and time sequence $0 = t_{0} < t_{1} < \ldots < t_{m+1} = T$ 2: Initialization:
3: Each learner sets, for $k \in [m+1]$ , $\left\{\begin{aligned}I_{2k-1} &\leftarrow[t_{k-1}+1,t_{k}-2\mu]\\ I_{2k} &\leftarrow[t_{k}-2\mu+1,t_{k}\right],\end{aligned}\right.$ where $\mu$ is the height of T
4: Each learner sets $\tilde{I} \leftarrow \max_{\ell \in [2m+2]} |I_{\ell}|$ 5: Each learner i initializes: $x_{t}^{i} = \hat{x}_{0} = \hat{x}_{1} = \hat{x}_{2} \leftarrow \arg\min_{x \in C} \|x\|$ for $t \in I_{1} \cup I_{2}$ 6: for k=1 to m do
7: Convergecast:
8: At time $t_{k}-2\mu$ , the learners run: $\left\{\begin{aligned}\text{Convergecast}(\{\nabla\hat{f}_{2k-2}^{i}(\hat{x}_{2k-2})\}_{i \in [n]}, \mathcal{T})\\ \text{Convergecast}(\{\nabla\hat{f}_{2k-1}^{i}(\hat{x}_{2k-1})\}_{i \in [n]}, \mathcal{T}),\end{aligned}\right.$ where $\hat{f}_{\ell}^{i} \triangleq \frac{1}{n\mathcal{I}} \Sigma_{s \in I_{\ell}} f_{s}^{i}$ for each $\ell$ and i
9: At time $t_{k}-\mu$ , the root learner in T obtains: $\left\{\begin{aligned}\nabla\hat{f}_{2k-2}(\hat{x}_{2k-2}) &= \Sigma_{i=1}^{n}\nabla\hat{f}_{2k-2}^{i}(\hat{x}_{2k-2})\\ \nabla\hat{f}_{2k-1}(\hat{x}_{2k-1}) &= \Sigma_{i=1}^{n}\nabla\hat{f}_{2k-1}^{i}(\hat{x}_{2k-1})\end{aligned}\right.$ 10: Global Update:
11: At time $t_{k}-\mu$ , the root learner in T updates: $\left\{\begin{aligned}\hat{x}_{2k+1} &\leftarrow\Pi_{C}(\hat{x}_{2k-2}-\eta\nabla\hat{f}_{2k-2}(\hat{x}_{2k-2}))\\ \hat{x}_{2k+2} &\leftarrow\Pi_{C}(\hat{x}_{2k-1}-\eta\nabla\hat{f}_{2k-1}(\hat{x}_{2k-1})),\end{aligned}\right.$ where $\Pi_{C}(x) \triangleq \arg\min_{y \in C} \|y-x\|$ , and $\eta = \Theta(1/\sqrt{m})$ 12: Broadcast:
13: At time $t_{k}-\mu$ , the learners run: $\left\{\begin{aligned}\text{Broadcast}(\hat{x}_{2k+1}, T)\\ \text{Broadcast}(\hat{x}_{2k+2}, T)\end{aligned}\right.$ 14: Local Update:
15: At time $t_{k}+1$ , each learner i updates: $\left\{\begin{aligned}x_{t}^{i} &\leftarrow\hat{x}_{2k+1}\text{ for } t \in I_{2k+1}\\ x_{t}^{i} &\leftarrow\hat{x}_{2k+2}\text{ for } t \in I_{2k+2}.\\\end{aligned}\right.$ 16: end for

# Proof sketch of Theorem 3.

In DB-TDOCO, for each iteration ℓ, the root learner updates:

$$
\hat {x} _ {\ell + 1} = \Pi_ {\mathcal {C}} (\hat {x} _ {\ell - 2} - \eta \nabla \hat {f} _ {\ell - 2} (\hat {x} _ {\ell - 2})),
$$

where $\eta = \mathcal { O } ( 1 / \sqrt { m } )$ and $\begin{array} { r } { \hat { f } _ { \ell } \triangleq \frac { 1 } { n \mathbb { Z } } \sum _ { s \in I _ { \ell } } f _ { s } } \end{array}$ . In other words, the next model $\hat { x } _ { \ell + 1 }$ is updated using the delayed loss function $\hat { f } _ { \ell - 2 }$ and model $\hat { x } _ { \ell - 2 }$ via gradient descent. By applying the regret analysis of OCOD [30], [44], we can establish that:

$$
\Sigma_ {k = 1} ^ {2 m + 2} \hat {f} _ {k} (x _ {k}) - \min _ {x \in \mathcal {C}} \Sigma_ {k = 1} ^ {2 m + 2} \hat {f} _ {k} (x) = \mathcal {O} (\sqrt {m}).
$$

By multiplying the equation above by $n \mathcal { L } ,$ , we can obtain the regret bound $\mathcal { R } _ { i }$ for $i \in [ n ]$ . As for the communication cost, during each interval $[ t _ { k - 1 } + 1 , t _ { k } ]$ for $k \in [ m ]$ , the learners convergecast two averaged gradients by recursively aggregating their children’s gradients and broadcast two models. Each run of convergecast or broadcast takes $n - 1$ communication cost. Hence, the communication cost of DB-TDOCO is $\mathcal { O } ( m n )$ .

Comparison with existing works: By Table II, gossip [11], [12] and D-BOCG [2] respectively achieve state-of-the-art regret and communication complexity for adversarial DOCO with convex and Lipschitz loss functions. Under the same assumptions, DB-TDOCO with parameters in Eq. (7) significantly reduces both the worst-case regret and communication cost of gossip by an $\mathcal { O } ( n ^ { 2 } )$ factor. With parameters in Eq. (8), DB-TDOCO minimizes regret in networks with small diameters $D _ { \colon }$ , while incurring a communication cost of $\mathcal { O } ( n T / D )$ . Given that gossip incurs a communication cost of $\Omega ( n T )$ [12], DB-TDOCO reduces this cost by an $\Omega ( D )$ factor. Compared to D-BOCG, which boasts the state-of-the-art communication cost ranging from $\Omega ( n \sqrt { T } )$ to $\mathcal { O } ( n ^ { 2 } \sqrt { T } )$ , DB-TDOCO reduces its worst-case regret by an $\mathcal { O } ( n ^ { 2 } T ^ { 1 / 4 } )$ factor. However, this improvement comes at the expense of an increased communication cost by a factor of $\mathcal { O } ( \sqrt { T } / n )$ and $\mathcal { O } ( \sqrt { T } / D )$ when employing parameters in Eqs. (7) and (8), respectively.

DB-TDOCO under milder assumptions: DB-TDOCO can broaden its scope to accommodate milder assumptions, such as unknown Lipschitz constants and unbounded feasible regions $\mathbb { R } ^ { d }$ , by replacing the model update rule in Eq. (6) with gradient methods from [45], [46]. These gradient algorithms yield equivalent regret bounds to gradient descent concerning n and $T ,$ with an additional dependence on the norm of the optimal model. Leveraging these gradient algorithms allows DB-TDOCO to achieve comparable regret bounds and communication complexity in DOCO scenarios with unbounded feasible regions $\mathbb { R } ^ { d }$ and gradient norms.

The analysis above assumes the BFS tree is pre-built. If the tree is not built beforehand, it can be constructed with $O ( n ^ { 2 } )$ communication cost in ${ \mathcal { O } } ( n )$ timeslots $( \mathrm { e . g . }$ , using the megamerger and flooding algorithms [47]). In this case, the learners incur $\mathcal { O } ( n ^ { 2 } )$ extra regret by choosing models as the initialized one before building the tree. The extra communication cost and regret are negligible in DB-TDOCO when $T \gg n$ .

# B. Algorithm Design for the Stochastic Setting

In the stochastic setting, the well-known online-to-batch conversion scheme [48] shows that online algorithms converge favorably in batch optimization. We extend this concept in the opposite direction, utilizing batch optimization algorithms to develop DOCO algorithms. While a batch algorithm may not ensure low loss for all constituent models, it does yield a final model with low loss, suitable for DOCO tasks. Hence, we require learners to update local models as the output of a batch algorithm runs before the current time point. The key insight behind achieving low regret and communication cost stems from the rapid convergence of the batch algorithm’s output to the optimal model as the feedback data increase. Consequently, frequent updates of learners’ local models are unnecessary. Instead, we only require learners to train a small number of communication-efficient batch optimization algorithms, which output models at carefully selected time points.

Based on this intuition, we propose the distributed batchto-online (DB2O) algorithm, which utilizes infrequent but effective model updates to achieve reduced regret and communication cost. Specifically, we leverage a general framework for communication-efficient distributed batch convex optimization (DBCO), namely BFS-tree-aided DBCO (T-DBCO). The learners execute m instances of T-DBCO, with each instance parallelly training models based on convergecast gradients and loss values. At time $t _ { k } ,$ the k-th instance returns a model $x _ { k , \nu _ { k } + 1 }$ for $k \in [ m ]$ , and each learner i then locally updates $x _ { t } ^ { i } = x _ { k , \nu _ { k } + 1 }$ . We provide the model update chart of DB2O in Fig. 5 and detailed algorithmic descriptions in Alg. 2.

![](images/5250357c5a54df172aa2c04139fa87e2489ef68a6cdfebbb37f987645c4e7b77.jpg)



Fig. 5: Model updates in DB2O. The k-th T-DBCO instance yields $x _ { k , \nu _ { k } + 1 }$ as learners’ local models from time $t _ { k } + 1$ to $t _ { k + 1 }$ , where $k \in [ m ] . \mathcal { A }$ represents the model update rule in T-DBCO. $p _ { k , \ell }$ and $\hat { f } _ { k , \ell }$ denote the parameters of $\mathcal { A }$ and the average loss functions, respectively, within the ℓ-th mini-batch $( [ t _ { k , \ell - 1 } + 1 , t _ { k , \ell } - 2 \mu ] )$ of the k-th T-DBCO instance.

We implement DB2O by employing communication-efficient T-DBCO updates with a limited number of T-DBCO instances m. Specifically, by adopting the cutting-plane [35] or AGD [41] update rule A, DB2O achieves optimal regret, with polylogarithmic factors in n and T , where $m = \tilde { \mathcal { O } } ( 1 )$ . Moreover, DB2O, when integrated with cutting-plane or AGD, significantly reduces the state-of-the-art communication cost [13] by approximately a factor of $\tilde { \mathcal { O } } ( ( n T ) ^ { \alpha } )$ for $\alpha > 0$ .

# Theoretical advantages of DB2O.

We analyze the regret and communication cost of DB2O with cutting-plane and AGD in Theorems 4 and 5. The details of update and initialization rules of cutting-plane and AGD are deferred to Appendix A in the supplementary material.

Theorem 4. Let the loss functions $f ( x ; \xi ) , \xi \sim \mathbb { P } _ { i } ~ f o r ~ i ~ \in$ [n] satisfy Definitions 1, 4, and 5. We choose update and initialization rules  and $\mathcal { A } _ { i n i t }$ as in cutting-plane, the number of T-DBCO instances $m = 1 + \lceil \ln \ln T \rceil$ , the time sequence as

$$
\left\{\begin{array}{l}t _ {1} = \lceil (2 \mu + 2) C _ {1} d \ln (n T) \rceil\\t _ {k} = t _ {1} + \left\lceil (T - t _ {1}) ^ {\frac {2 - 2 ^ {- k + 2}}{2 - 2 ^ {- m + 1}}} \right\rceil , f o r 2 \leq k \leq m,\end{array}\right.
$$

and the batch size as

$$
b _ {k} = \left\lfloor t _ {k} / \left(C _ {1} d \ln \left(d n / \epsilon_ {k}\right)\right) \right\rfloor f o r k \in [ m ],
$$

where $\mu$ is the BFS tree’s height, $C _ { 1 } ~ > ~ 0$ is a constant, and $\epsilon _ { k } = d ^ { 3 / 2 }$ ln $\begin{array} { r } { \left( n t _ { k } \right) \sqrt { \frac { n } { t _ { k } - ( 2 \mu + 1 ) C _ { 1 } d \ln ( n t _ { k } ) } } } \end{array}$ . Then, the regret

Algorithm 2 Distributed Batch-to-Online (DB2O)   
1: Input: Update rule A, initialization rule $A_{init}$ for A, BFS tree T, number of T-DBCO instances m, time sequence $0 = t_{0} < \ldots < t_{m+1} = T$ , and batch sizes $\{b_{k}\}_{k \in [m]}$ ▷ Details of A and $A_{init}$ are deferred to Appendix A

2: Initialization:
3: Each learner i initializes: $x_{t}^{i} = \hat{x}_{1} \leftarrow \arg\min_{x \in C} \|x\| \text{ for } t \in [1, t_{1}]$ 4: Each learner sets $\mu$ as the height of T

5: Each learner sets, for $k \in [m]$ , $\begin{cases} x_{k,1} \leftarrow \hat{x}_{1} \\ t_{k,\ell} \leftarrow \ell \cdot b_{k} \text{ for } \ell \leq \nu_{k} = \lfloor t_{k}/b_{k} \rfloor \\ p_{k,1} \leftarrow \mathcal{A}_{init}(\nu_{k}) \end{cases}$ 6: for each k in [m] do

7: T-DBCO Update:
8: for $\ell = 1$ to $\nu_{k}$ do

9: Convergecast:
10: At time $t_{k,\ell} - 2\mu$ , the learners run: $\begin{cases} \text{Convergecast}(\{\hat{f}_{k,\ell}^{i}(x_{k,\ell})\}_{i \in [n]}, T) \\ \text{Convergecast}(\{\nabla\hat{f}_{k,\ell}^{i}(x_{k,\ell})\}_{i \in [n]}, T), \end{cases}$ where $\hat{f}_{k,\ell}^{i} = \frac{1}{b_{k}-2\mu} \Sigma_{s=t_{k,\ell-1}+1}^{t_{k,\ell}-2\mu} f_{s}^{i}$ 11: At time $t_{k,\ell} - \mu$ , the root learner obtains: $\begin{cases} \hat{f}_{k,\ell}(x_{k,\ell}) = \Sigma_{i=1}^{n} \hat{f}_{k,\ell}^{i}(x_{k,\ell}) \\ \nabla\hat{f}_{k,\ell}(x_{k,\ell}) = \Sigma_{i=1}^{n} \nabla\hat{f}_{k,\ell}^{i}(x_{k,\ell}) \end{cases}$ 12: Global Update:
13: At time $t_{k,\ell} - \mu$ , the root learner in T updates: $x_{k,\ell+1}, p_{k,\ell+1} \leftarrow \mathcal{A}(x_{k,\ell}, \hat{f}_{k,\ell}(x_{k,\ell}), \nabla\hat{f}_{k,\ell}(x_{k,\ell}), p_{k,\ell}).$ 14: Broadcast:
15: At time $t_{k,\ell} - \mu$ , the learners run: $Broadcast(x_{k,\ell+1}, T)$ 16: end for

17: Local Update:
18: At time $t_{k} + 1$ , each learner i updates: $x_{t}^{i} \leftarrow x_{k,\nu_{k}+1} \text{ for } t \in [t_{k} + 1, t_{k+1}]$ 19: end for

bound of DB2O is $\tilde { \mathcal { O } } ( d n ^ { 2 } { + } d ^ { 3 / 2 } \sqrt { n T } )$ , and the communication cost is $\tilde { \mathcal { O } } ( d n )$ , where n is the number of learners, T is the learning time, and d is the model dimension.

Theorem 5. Let the loss functions $f ( x ; \xi ) , \xi \sim \mathbb { P } _ { i }$ for $i \in [ n ]$ satisfy Definitions 1, 3, and 5. We choose update and initialization rules A and $\mathcal { A } _ { i n i t }$ as in AGD, the number of T-DBCO instances $m = \lceil \ln \ln n \rceil + \lceil \ln \ln T \rceil$ , the time sequence as

$$
\left\{\begin{array}{l}t _ {k} = 2 \mu + n + \left\lfloor n ^ {1 + \frac {2}{3} \cdot \frac {2 ^ {k} - 1}{2 ^ {m ^ {\prime}} - 1}} \right\rfloor ,   f o r k \leq m ^ {\prime}\\t _ {k} = t _ {m ^ {\prime}} + \left\lceil (T - t _ {m ^ {\prime}}) ^ {\frac {2 - 2 ^ {- k + 1 + m ^ {\prime}}}{2 - 2 - m + m ^ {\prime}}} \right\rceil ,   f o r k > m ^ {\prime},\end{array}\right.
$$

and the batch sizes as

$$
\left\{ \begin{array}{l} b _ {k} = 2 \mu + n, f o r k \leq m ^ {\prime} \\ b _ {k} = \max \Big \{2 \mu + n, \Big \lfloor \frac {t _ {k}}{C _ {2} n ^ {1 / 4} t _ {k} ^ {1 / 4} + 1} \Big \rfloor \Big \}, f o r k > m ^ {\prime}, \end{array} \right.
$$

where $\mu$ is the BFS tree’s height, $m ^ { \prime } = \left\lceil \ln \ln n \right\rceil$ , and $C _ { 2 } > 0$ is a constant. Then, the regret bound of DB2O is ${ \tilde { \mathcal { O } } } ( n ^ { 2 } + { \sqrt { n T } } )$ , and the communication cost is $\tilde { \mathcal { O } } ( n ^ { 5 / 3 } + n ^ { 5 / 4 } T ^ { 1 / 4 } )$ .

DB2O facilitates learners in achieving nearly optimal regret by parallelizing a few instances of communication-efficient T-DBCO. By Theorem 4, DB2O with cutting-plane almost attains the optimal regret and communication complexity in n and $T$ (the primary focus of this paper) established in Corollary 2 when $T \ \gg \ n .$ Notably, it stands as the first algorithm to achieve almost optimal regret and communication complexity that is nearly independent of T . However, its regret and communication complexity do additionally depend on the model dimension $d ,$ which proves to be suboptimal when compared to the state-of-the-art DMA algorithm with no dependence on d [13], cf. Table I. In contrast, DB2O with AGD nearly achieves optimal regret in n, T , and d. While its communication cost is not optimal in n and T , it remains independent of d and outperforms the state-of-the-art [13], offering a potential advantage in high-dimensional DOCO tasks.

# Proof sketch of Theorems 4 and 5.

For DB2O with cutting-plane, denote the risk of model $x \in { \mathcal { C } }$ as $\begin{array} { r } { \operatorname { R i s k } ( x ) \triangleq \bar { f } ( x ) - \operatorname* { m i n } _ { x ^ { * } \in \mathcal { C } } \bar { f } ( x ^ { * } ) } \end{array}$ , where ${ \bar { f } } ( x ) =$ $\Sigma _ { i = 1 } ^ { n } \mathbb { E } _ { \xi \sim \mathbb { P } _ { i } } [ f ( x ; \xi ) ]$ . By Eq. (2), we obtain, for $j \in [ n ]$ :

$$
\bar {\mathcal {R}} _ {j} (T) = \mathbb {E} \left[ \operatorname{Risk} \left(\hat {x} _ {1}\right) t _ {1} \right] + \mathbb {E} \left[ \Sigma_ {k = 1} ^ {m} \operatorname{Risk} \left(x _ {k, \nu_ {k} + 1}\right) \left(t _ {k + 1} - t _ {k}\right) \right] \tag {9}
$$

$$
= \mathcal {O} (n t _ {1}) + \mathbb {E} \big [ \Sigma_ {k = 1} ^ {m} \mathrm{Risk} (x _ {k, \nu_ {k} + 1}) (t _ {k + 1} - t _ {k}) \big ],
$$

where the second equality follows from $\mathrm { R i s k } ( \hat { x } _ { 1 } ) = \mathcal { O } ( n )$ according to Definition 5. For cutting-plane, $b _ { k }$ specified in Theorem 4 ensures that:

$$
\mathbb {E} \left[ \operatorname{Risk} (x _ {k, \nu_ {k} + 1}) \right] \leq \mathcal {O} (1) \cdot \epsilon_ {k}.
$$

Plugging the values of $t _ { k }$ and the risk of $x _ { k , \nu _ { k } + 1 }$ for $k \in [ m ]$ into Eq. (9), we obtain that $\bar { \mathcal { R } } _ { j } ( T ) = \tilde { \mathcal { O } } ( d n ^ { 2 } + d ^ { 3 / 2 } \sqrt { n T } )$ .

Each run of T-DBCO requires $\mathcal { O } ( t _ { k } / b _ { k } )$ convergecast and broadcast operations and the communication cost of convergecast/broadcast is ${ \mathcal { O } } ( n )$ . The communication cost for each run of T-DBCO in Alg. 2 equals $\mathcal { O } ( n t _ { k } / b _ { k } ) = \tilde { \mathcal { O } } ( d n )$ and Alg. 2 runs O(ln ln T ) instances of T-DBCO. Thus the overall communication cost is $\tilde { \mathcal { O } } ( d n )$ .

In DB2O with AGD, $b _ { k }$ specified in Theorem 5 ensures that:

$$
\left\{ \begin{array}{l} \mathbb {E} \big [ \operatorname{Risk} (x _ {k, \nu_ {k} + 1}) \big ] = \mathcal {O} \Big (\frac {n ^ {3}}{(t _ {k} - 2 \mu - n) ^ {2}} \Big) \text {   if   } t _ {k} \leq 2 \mu + n + n ^ {5 / 3} \\ \mathbb {E} \big [ \operatorname{Risk} (x _ {k, \nu_ {k} + 1}) \big ] = \mathcal {O} \Big (\sqrt {\frac {n}{t _ {k} - 2 \mu - n}} \Big), \text {   otherwise. } \end{array} \right.
$$

The rest of the proof is similar to that for cutting-plane.

Comparison with existing works: DB2O significantly reduces the communication complexity of the state-of-the-art DMA algorithm [13] concerning n and T . Firstly, DB2O with cutting-plane reduces DMA’s communication complexity by a factor of $\tilde { \mathcal { O } } ( \sqrt { n T } / d )$ while maintaining minimax regret within polylogarithmic factors in n and T and factors in $d ^ { 3 / 2 }$ . This advantage is particularly evident in scenarios with numerous learners and prolonged learning times. Compared to DMA, DB2O with cutting-plane requires bounded loss functions and a fat feasible region, relaxing the smoothness assumption (cf. Table II). Secondly, DB2O with AGD nearly achieves minimax regret and reduces DMA’s communication complexity by a factor of $\tilde { \mathcal { O } } ( ( n T ) ^ { 1 / 4 } )$ for loss functions under the same assumptions. This reduction is dimension-free, making DB2O with AGD more advantageous over DMA in high-dimensional tasks compared to DB2O with cutting-plane.

DB2O under milder assumptions: For DB2O with cuttingplane, the strict requirements on loss functions outlined in Definitions 1, 4, and 5 can be relaxed without compromising effectiveness. This relaxation involves ensuring that the expected loss function $\bar { f } ( x ) = \Sigma _ { i = 1 } ^ { n } \mathbb { E } _ { \xi \sim \mathbb { P } _ { i } } [ f ( x ; \xi ) ]$ adheres to Definitions 1 and 4, while bounding the variances of both the loss values and gradients of $f ( x ; \xi ) , \xi \sim \mathbb { P } _ { i }$ for $i \in [ n ]$ [35]. Consequently, the regret and communication complexity of the corresponding DB2O implementation remain unaffected. Similarly, for DB2O with AGD, the prerequisites on feasible regions to be compact can be relaxed, enabling it to operate in scenarios with an unbounded feasible region $\mathbb { R } ^ { d }$ [41]. This relaxation aligns with the analysis in Theorem 5 concerning n and T , allowing DB2O with AGD to maintain the same regret and communication complexity under these relaxed conditions.

Similar to the adversarial setting, if the BFS tree is not built beforehand, it will incur $O ( n ^ { 2 } )$ extra communication cost and regret loss when building the tree and using the initialized model. In this case, the communication cost of DB2O with cutting-plane becomes ${ \tilde { O } } ( n ^ { 2 } + d n )$ , which is still the lowest in terms of n and T in the literature.

# VI. ALGORITHM ANALYSIS ON TYPICAL NETWORKS

In this section, we compare the regret loss and communication cost of our algorithms with the state-of-the-art [2], [11]– [13] on typical cycle, grid, and clique networks. We present the networks in Fig. 6 and summarize the comparisons of regret bounds and communication complexity in Table III. It shows that our proposed algorithms achieve reduced communication cost in n and T without compromising regret on these networks compared to algorithms with state-of-the-art regret [11]–[13].

![](images/895e9eeb69b62b7d095e06e8a67652038c009e426381fba42d48df1789254c7c.jpg)  
(a) Cycle network

![](images/1b11fab7e284b724a98d723cd0de7b96def34cf9732a4ce7be6d34d591de16e5.jpg)  
(b) Grid network

![](images/84cd1c08a23bb8220443759fe576326c1ec34d86a814fc920087e27bb5fada59.jpg)  
(c) Clique network   
Fig. 6: Illustration of some typical network topologies.

# A. DOCO for the Adversarial Setting

In the adversarial setting, we assess the performance of DB-TDOCO against gossip [11], [12] and D-BOCG [2], which respectively achieve the state-of-the-art regret and communication complexity. The impact of network topologies differs between gossip (D-BOCG) and DB-TDOCO. According to the analysis in [2], [11], [22], gossip and D-BOCG’s regret and communication complexity are influenced by network connectivity, measured by the spectral gap of the network’s gossip matrix [40] and the number of edges. However, DB-TDOCO’s performance remains unaffected by the network topology when parameters in Eq. (7) are chosen. Conversely, with parameters in Eq. (8), DB-TDOCO’s performance is governed by the network’s diameter.

TABLE III: Regret bounds and communication complexity for DOCO algorithms on n-node cycle, grid, and clique networks for the dependence of the number of learners n and learning time T when $T \gg n$ . Topology-independent and diameter-dependent DB-TDOCO variants are implemented with parameters in Eqs. (7) and (8), respectively. DB2Oc and $\mathrm { D B } 2 0 _ { a }$ refer to DB2O with cutting-plane and AGD, respectively.

<table><tr><td rowspan="2">Feedbacks</td><td rowspan="2">DOCO algorithms</td><td colspan="3">Regret bounds</td><td colspan="3">Communication complexity</td></tr><tr><td>Cycle</td><td>Grid</td><td>Clique</td><td>Cycle</td><td>Grid</td><td>Clique</td></tr><tr><td rowspan="4">Adversarial</td><td>gossip [11], [12]</td><td> $\mathcal{O}(n^{7/2}\sqrt{T})$ </td><td> $\tilde{\mathcal{O}}(n^{5/2}\sqrt{T})$ </td><td> $\mathcal{O}(n^{3/2}\sqrt{T})$ </td><td> $\mathcal{O}(nT)$ </td><td> $\mathcal{O}(nT)$ </td><td> $\mathcal{O}(n^2T)$ </td></tr><tr><td>D-BOCG [2]</td><td> $\mathcal{O}(n^{7/2}T^{3/4})$ </td><td> $\tilde{\mathcal{O}}(n^{5/2}T^{3/4})$ </td><td> $\mathcal{O}(n^{3/2}T^{3/4})$ </td><td> $\mathcal{O}(n\sqrt{T})$ </td><td> $\mathcal{O}(n\sqrt{T})$ </td><td> $\mathcal{O}(n^2\sqrt{T})$ </td></tr><tr><td>DB-TDOCO(topology-independent)</td><td> $\mathcal{O}(n^{3/2}\sqrt{T})$ </td><td> $\mathcal{O}(n^{3/2}\sqrt{T})$ </td><td> $\mathcal{O}(n^{3/2}\sqrt{T})$ </td><td> $\mathcal{O}(T)$ </td><td> $\mathcal{O}(T)$ </td><td> $\mathcal{O}(T)$ </td></tr><tr><td>DB-TDOCO(diameter-dependent)</td><td> $\mathcal{O}(n^{3/2}\sqrt{T})$ </td><td> $\mathcal{O}(n^{5/4}\sqrt{T})$ </td><td> $\mathcal{O}(n\sqrt{T})$ </td><td> $\mathcal{O}(T)$ </td><td> $\mathcal{O}(\sqrt{n}T)$ </td><td> $\mathcal{O}(nT)$ </td></tr><tr><td rowspan="3">Stochastic</td><td>DMA [13]</td><td> $\mathcal{O}(\sqrt{nT})$ </td><td> $\mathcal{O}(\sqrt{nT})$ </td><td> $\mathcal{O}(\sqrt{nT})$ </td><td> $\mathcal{O}(n^{3/2}\sqrt{T})$ </td><td> $\mathcal{O}(n^{3/2}\sqrt{T})$ </td><td> $\mathcal{O}(n^{3/2}\sqrt{T})$ </td></tr><tr><td>DB2O $_c$ </td><td> $\tilde{\mathcal{O}}(\sqrt{nT})$ </td><td> $\tilde{\mathcal{O}}(\sqrt{nT})$ </td><td> $\tilde{\mathcal{O}}(\sqrt{nT})$ </td><td> $\tilde{\mathcal{O}}(n)$ </td><td> $\tilde{\mathcal{O}}(n)$ </td><td> $\tilde{\mathcal{O}}(n)$ </td></tr><tr><td>DB2O $_a$ </td><td> $\tilde{\mathcal{O}}(\sqrt{nT})$ </td><td> $\tilde{\mathcal{O}}(\sqrt{nT})$ </td><td> $\tilde{\mathcal{O}}(\sqrt{nT})$ </td><td> $\tilde{\mathcal{O}}(n^{5/4}T^{1/4})$ </td><td> $\tilde{\mathcal{O}}(n^{5/4}T^{1/4})$ </td><td> $\tilde{\mathcal{O}}(n^{5/4}T^{1/4})$ </td></tr></table>

The regret bound of gossip scales as $\mathcal { O } ( \Gamma n ^ { 3 / 2 } \sqrt { T } )$ , where Γ measures the connectivity of the network [22]. Specifically, in gossip, the network topology is parameterized by its gossip matrix A [40], a weighted adjacency matrix of the learner network. The parameter Γ is the inverse of A’s spectral gap, which equals $\frac { 1 } { 1 - \lambda _ { 2 } ( A ) }$ , where $\lambda _ { 2 } ( A )$ denotes the second largest eigenvalue of A. Values of Γ for n-node cycle, grid, and clique networks are presented in Table IV [22]. The communication cost of gossip is linear in the network’s edge number E and learning time T . Note that $E = \mathcal { O } ( n )$ for cycle and grid networks and $E = \mathcal { O } ( n ^ { 2 } )$ for the clique network. The regret bounds and communication complexity of gossip in Table III then follow. D-BOCG reduces gossip’s communication cost by a factor of $\mathcal { O } ( \sqrt { T } )$ but increases the regret by a factor of $\mathcal { O } ( T ^ { 1 / 4 } )$ .

TABLE IV: Connectivity parameter Γ for gossip [11], [12] in adversarial DOCO in n-node cycle, grid, and clique networks.

<table><tr><td>Network topology</td><td>Connectivity parameter Γ</td></tr><tr><td>Cycle</td><td> $\mathcal{O}(n^{2})$ </td></tr><tr><td>Grid</td><td> $\mathcal{O}(n \ln n)$ </td></tr><tr><td>Clique</td><td> $\mathcal{O}(1)$ </td></tr></table>

DB-TDOCO’s regret bounds and communication complexity are established in Corollaries 3 and 4. When using parameters in Eq. (7), DB-TDOCO’s performance is independent of the network topology. With parameters in Eq. (8), DB-TDOCO’s performance depends on the network’s diameter D. Note that $D = { \mathcal { O } } ( n )$ for the cycle network, $D = \mathcal { O } ( \sqrt { n } )$ for the grid network, and $D = \mathcal { O } ( 1 )$ for the clique network. The regret bounds and communication complexity of DB-TDOCO in this case then follow from Corollary 4.

Table III shows that both variants of DB-TDOCO require lower communication cost than gossip. DB-TDOCO with parameters in Eq. (7) reduces the communication cost proportionally to the network’s edge number. With parameters from Eq. (8), DB-TDOCO reduces the communication cost by a factor of $\begin{array} { r } { \mathcal { O } ( \frac { E \cdot D } { n } ) } \end{array}$ , where n is the number of learners, E is the edge number of the network, and D is the diameter of the network. Regarding regret, DB-TDOCO with Eq. (7) matches gossip’s regret on the clique network. In other settings, DB-TDOCO reduces gossip’s regret by a factor of $\mathcal { O } ( n ^ { \alpha } )$ , where α ranges from 0.5 to 2. Compared to D-BOCG, DB-TDOCO reduces its regret by a factor ranging from $\mathcal { O } ( T ^ { 1 / 4 } )$ to $\mathcal { O } ( n ^ { 2 } T ^ { 1 / 4 } )$ , with the communication cost enlarged by a factor of $\mathcal { O } ( \sqrt { T } / n ^ { \alpha } )$ for $0 . 5 \leq \alpha \leq 2$ .

# B. DOCO for the Stochastic Setting

The DOCO algorithms in the stochastic setting are not affected by the networks’ topologies. The regret bounds and communication complexity of our DB2O and DMA algorithms remain unchanged on all three networks in Fig. 6. As summarized in Table III, DB2O reduces the communication complexity of DMA by an $\tilde { \mathcal { O } } ( ( n T ) ^ { \alpha } )$ ) factor in terms of the number of learners n and learning time T , where $\alpha = 0 . 5$ for DB2O with cutting-plane and $\alpha = 0 . 2 5$ for DB2O with AGD. These results demonstrate that the advantage of our DB2O algorithms is consistent and significant regardless of the network topologies.

# VII. EXPERIMENTS

In this section, we present experimental results comparing the communication efficiency of our algorithms and the stateof-the-art in achieving comparable classification accuracy.

# A. Implementation Details

We conduct distributed online logistic regression tasks. Each learner’s error rate at each time is evaluated on the current data. We average all learners’ error rates across the learning time as the algorithm’s online classification error rate.

Data and preprocessing: We utilize two real-world datasets from the LIBSVM repository [49]: covtype.binary (covtype for short) [23] and epsilon [24]. The covtype dataset contains 581, 012 samples with 54 features, while ${ \tt e p s i l o n }$ is a high-dimensional dataset with 2, 000 features and 500, 000 samples. We preprocess each dataset by scaling all features to [−1, 1] and each sample to unit length. We assign positive samples to half of the learners and negative samples to the other half in uniform size.2 For the stochastic settings, we randomly order each learner’s dataset and reveal the t-th sample to them at each time t. The default learning time equals each learner’s data size. In the adversarial setting, we generate the data streams inspired by [50] as follows: 1) we divide the learning time into three equal-length phases; 2) we reveal one sample with its label flipped to each learner at each time during the second phase, while revealing the original samples during the first and third phases. With this construction, the optimal model varies in different phases.

![](images/6fd39ce20dae0b781ee74945154863c706fe98776db543f8d3063a9b9b078ac4.jpg)  
Fig. 7: Online classification error rates in DOCO. The line indicates the averages, and the shaded area is where all error rates lie in across 10 runs.

![](images/063e2a77f985e526fcd25645ed36b209a9a925f2582fc4b586176c4996c9c690.jpg)  
Fig. 8: Communication cost to achieve the target error rates. The curves are the minimum communication cost to achieve the error rates specified by the bars. The target error rate is the maximum of the evaluated algorithms’ optimal error rates for each T and network.

Baselines: We compare our algorithms with DMA [13] and the mini-batch gossip algorithm [11].3These baselines achieve state-of-the-art regret loss with the currently state-of-the-art communication cost. Additionally, we include D-BOCG [2] as a baseline for the adversarial setting, which achieves the currently state-of-the-art communication complexity with a suboptimal regret bound.

Implementations: We conduct experiments on networks with representative topologies, including the cycle network where

3We modify gossip [11] into a mini-batch version, where the learners communicate and update models every τ timeslots using their averaged gradients, and τ represents the batch size.

each learner has two neighbors and the all-connected clique network. Based on [13], [22] and our analysis in Section V, the evaluated algorithms achieve the best theoretical regret bounds on the clique network with high communication cost. They feature higher regret bounds on the loosely connected cycle network with lower communication cost. We choose the feasible region  as an Euclidean ball with a radius of 20. Similar to [2], we set the stepsize parameter as $c T ^ { - 3 / 4 }$ for D-BOCG, where c is chosen optimally from $\{ 1 0 ^ { - 2 } , 1 0 ^ { - 1 } , \dots , 1 0 ^ { 5 } \}$ in each run. For DB-TDOCO and gossip [11], we take the stepsize $c T ^ { - 1 / 2 }$ with the optimal c in $\{ 1 0 ^ { - 2 } , 1 0 ^ { - 1 } , \dots , 1 0 ^ { 5 } \}$ . For DB2O with AGD and cutting-plane (referred to as $\mathrm { D B } 2 0 _ { a }$ and DB2Oc) and DMA, we use the hyperparameters as specified in [13], [41], [51]. To adjust the communication budget of gossip, D-BOCG, and DMA, we modify the batch size used to compute the minibatch gradients. For DB-TDOCO, we adjust the communication budget by modifying the interval size $t _ { 1 } = t _ { 2 } - t _ { 1 } = . . . =$ $t _ { m } - t _ { m - 1 }$ in Alg. 1. Similarly, for $\mathrm { D B 2 O } _ { c }$ and $\mathrm { D B } 2 { \mathrm { O } } _ { a } ,$ we tune the communication budget by modifying the constants $C _ { 1 }$ and $C _ { 2 }$ in Theorems 4 and 5.

# B. Experimental Results

DOCO for the adversarial setting: We investigate how the error rates evolve with the communication budget on 8-node and 32-node learner networks in the adversarial setting. Figs. 7a-7d demonstrate that DB-TDOCO requires only around 5% of the communication cost of gossip and D-BOCG to achieve a target error rate of $\leq 0 . 4$ on all networks and datasets. Furthermore, on the 32-node cycle network, DB-TDOCO converges to lower error rates than gossip and D-BOCG as the budget increases.

We further analyze the evolution of the communication cost of the algorithms required to achieve a low target error rate with respect to the learning time T . For this analysis, we utilize the covtype dataset. In Fig. 8a, we observe that on 8-node networks, DB-TDOCO incurs less than 5% of the communication cost of gossip (D-BOCG) across various values of T and network topologies. Similarly, on 32-node networks,

Fig. 8b illustrates that DB-TDOCO necessitates less than 1% of the communication cost incurred by both gossip and D-BOCG.

DOCO for the stochastic setting: Figs. 7e-7h illustrate that on 8-node networks, $\mathrm { D B } 2 0 _ { a }$ and $\mathrm { D B 2 O } _ { c }$ require only around 10% and 1% of the communication cost of DMA to converge to close and steady error rates. On 32-node networks, $\mathrm { D B } 2 0 _ { a }$ and $\mathrm { D B 2 O } _ { c }$ generally need approximately 50% and 10% of the communication cost of DMA to converge to a low error rate $\leq 0 . 3 .$ The advantages of $\mathrm { D B } 2 0 _ { a }$ and $\mathrm { D B 2 O } _ { c }$ are more prominent on 8-node networks since the learning time T is significantly larger than the number of learners n (cf. Theorems 4 and 5). On the 32-node cycle network and epsilon dataset, DB2Oc produces higher error rates than $\mathrm { D B } 2 0 _ { a }$ and DMA because $T$ is not large enough to mitigate the impact of the high dimension d.

Consequently, we investigate the necessary communication cost of these algorithms to achieve a low target error rate, considering different $T$ on various networks using covtype. Fig. 8c illustrates that on 8-node networks, $\mathrm { D B } 2 0 _ { a }$ and $\mathrm { D B 2 O } _ { c }$ require approximately 10% and 5% of the communication cost of DMA, respectively. On the 32-node clique network, Fig. 8d shows that the communication costs of $\mathrm { D B } 2 0 _ { a }$ and $\mathrm { D B 2 O } _ { c }$ consistently remain lower than DMA. Their communication savings peak at $T \ = \ 1 8 , 0 0 0$ , surpassing 80% and 97%, respectively. However, on the 32-node cycle network, $\mathrm { D B } 2 0 _ { a }$ and $\mathrm { D B 2 O } _ { c }$ fail to save on communication over DMA for $T \leq 7$ , 200 as the update times are not sufficient to mitigate the impact of high dimension d and learner count n. Nevertheless, as $T$ reaches 18,000, $\mathrm { D B } 2 0 _ { a }$ and DB2Oc achieve over 60% and 80% savings compared to DMA.

# VIII. CONCLUSION

DOCO provides effective algorithmic frameworks for learning tasks with numerous learners and streaming data. Two significant performance bottlenecks for DOCO are regret loss and communication complexity when implemented in communication-constrained networks. It is challenging to simultaneously achieve low regret and communication complexity, especially when the number of learners n and learning time $T$ are extensive. In this paper, we design novel algorithms in typical adversarial and stochastic settings. Our algorithms nearly achieve the minimax regret and reduce the state-of-theart algorithms’ communication cost by a factor of $O ( n ^ { 2 } )$ and $\tilde { \mathcal { O } } ( \sqrt { n T } )$ in adversarial and stochastic settings, respectively. Furthermore, we prove that the communication complexity of our algorithms is nearly optimal. Extensive experiments validate that our proposed algorithms can achieve 90% 99% communication saving over the state-of-the-art with close accuracy in most cases.

# REFERENCES

[1] S. Lin, M. Dedeoglu, and J. Zhang, “Accelerating distributed online metalearning via multi-agent collaboration under limited communication,” in MobiHoc, pp. 261–270, ACM, 2021.   
[2] Y. Wan, W. Tu, and L. Zhang, “Projection-free distributed online√ convex optimization with O( T ) communication complexity,” in ICML, pp. 9818–9828, 2020.   
[3] S. Hosseinalipour, A. Nayak, and H. Dai, “Power-aware allocation of graph jobs in geo-distributed cloud networks,” IEEE Trans. Parallel Distributed Syst., vol. 31, no. 4, pp. 749–765, 2020.

[4] Z. Tu, X. Wang, Y. Hong, L. Wang, D. Yuan, and G. Shi, “Distributed online convex optimization with compressed communication,” in NeurIPS, 2022.   
[5] J. L. Williams and J. W. F. III, “Approximate dynamic programming for communication-constrained sensor network management,” IEEE Trans. Signal Process., vol. 55, no. 8, pp. 4300–4311, 2007.   
[6] J. Xu, K. Li, and G. Min, “Reliable and energy-efficient multipath communications in underwater sensor networks,” IEEE Trans. Parallel Distributed Syst., vol. 23, no. 7, pp. 1326–1335, 2012.   
[7] K. Yuan, Q. Ling, and Z. Tian, “Communication-efficient decentralized event monitoring in wireless sensor networks,” IEEE Trans. Parallel Distributed Syst., vol. 26, no. 8, pp. 2198–2207, 2015.   
[8] A. Ahmad, G. Lawless, and P. U. Lima, “An online scalable approach to unified multirobot cooperative localization and object tracking,” IEEE Trans. Robotics, vol. 33, no. 5, pp. 1184–1199, 2017.   
[9] G. Zhan and W. Shi, “LOBOT: low-cost, self-contained localization of small-sized ground robotic vehicles,” IEEE Trans. Parallel Distributed Syst., vol. 24, no. 4, pp. 744–753, 2013.   
[10] A. Serra-G ´ omez, B. Brito, H. Zhu, J. J. Chung, and J. Alonso-Mora, ´ “With whom to communicate: Learning efficient communication for multirobot collision avoidance,” in IROS, pp. 11770–11776, IEEE, 2020.   
[11] F. Yan, S. Sundaram, S. V. N. Vishwanathan, and Y. A. Qi, “Distributed autonomous online learning: Regrets and intrinsic privacy-preserving properties,” IEEE Trans. Knowl. Data Eng., vol. 25, no. 11, pp. 2483– 2493, 2013.   
[12] J. Lei, P. Yi, Y. Hong, J. Chen, and G. Shi, “Online convex optimization over erdos-renyi random networks,” in NeurIPS, 2020.   
[13] O. Dekel, R. Gilad-Bachrach, O. Shamir, and L. Xiao, “Optimal distributed online prediction using mini-batches,” J. Mach. Learn. Res., vol. 13, pp. 165–202, 2012.   
[14] J. Acharya, C. D. Sa, D. J. Foster, and K. Sridharan, “Distributed learning with sublinear communication,” in ICML, pp. 40–50, 2019.   
[15] B. Sidik, R. Puzis, P. Zilberman, and Y. Elovici, “PALE: time bounded practical agile leader election,” IEEE Trans. Parallel Distributed Syst., vol. 31, no. 2, pp. 470–485, 2020.   
[16] G. Best, M. Forrai, R. R. Mettu, and R. Fitch, “Planning-aware communication for decentralised multi-robot coordination,” in ICRA, pp. 1050–1057, IEEE, 2018.   
[17] N. Santoro, Design and analysis of distributed algorithms. Wiley series on parallel and distributed computing, Wiley, 2007.   
[18] Z. Qin, D. Wu, Z. Xiao, B. Fu, and Z. Qin, “Modeling and analysis of data aggregation from convergecast in mobile sensor networks for industrial iot,” IEEE Trans. Ind. Informatics, vol. 14, no. 10, pp. 4457–4467, 2018.   
[19] J. Bassil, A. Makhoul, B. Piranda, and J. Bourgeois, “Distributed sizeconstrained clustering algorithm for modular robot-based programmable matter,” ACM Trans. Auton. Adapt. Syst., vol. 18, no. 1, pp. 1:1–1:21, 2023.   
[20] A. Agarwal and J. C. Duchi, “Distributed delayed stochastic optimization,” in CDC, pp. 5451–5452, IEEE, 2012.   
[21] D. Yuan, Y. Hong, D. W. C. Ho, and S. Xu, “Distributed mirror descent for online composite optimization,” IEEE Trans. Autom. Control., vol. 66, no. 2, pp. 714–729, 2021.   
[22] A. Nedic, A. Olshevsky, and M. G. Rabbat, “Network topology and communication-computation tradeoffs in decentralized optimization,” Proc. IEEE, vol. 106, no. 5, pp. 953–976, 2018.   
[23] R. Collobert, S. Bengio, and Y. Bengio, “A parallel mixture of svms for very large scale problems,” Neural Comput., vol. 14, no. 5, pp. 1105– 1114, 2002.   
[24] G. Yuan, C. Ho, and C. Lin, “An improved GLMNET for l1-regularized logistic regression,” J. Mach. Learn. Res., vol. 13, pp. 1999–2030, 2012.   
[25] Y. Wang, J. Hu, X. Chen, and L. Wang, “Distributed bandit learning: Nearoptimal regret with efficient communication,” in ICLR, OpenReview.net, 2020.   
[26] X. Wang, Z. Ning, L. Guo, S. Guo, X. Gao, and G. Wang, “Online learning for distributed computation offloading in wireless powered mobile edge computing networks,” IEEE Trans. Parallel Distributed Syst., vol. 33, no. 8, pp. 1841–1855, 2022.   
[27] X. Su, Y. Zhou, L. Cui, and J. Liu, “On model transmission strategies in federated learning with lossy communications,” IEEE Trans. Parallel Distributed Syst., vol. 34, no. 4, pp. 1173–1185, 2023.   
[28] D. van der Hoeven, H. Hadiji, and T. van Erven, “Distributed online learning for joint regret with communication constraints,” in ALT, vol. 167, pp. 1003–1042, PMLR, 2022.   
[29] Y. Wan, G. Wang, W.-W. Tu, and L. Zhang, “Projection-free distributed online learning with sublinear communication complexity,” CoRR, vol. abs/2103.11102v2, 2022.

[30] P. Joulani, A. Gyorgy, and C. Szepesv ¨ ari, “Online learning under delayed ´ feedback,” in ICML, pp. 1453–1461, 2013.   
[31] I. Bistritz, Z. Zhou, X. Chen, N. Bambos, and J. H. Blanchet, “Online EXP3 learning in adversarial bandits with delayed feedback,” in NeurIPS, pp. 11345–11354, 2019.   
[32] H. Esfandiari, A. Karbasi, A. Mehrabian, and V. S. Mirrokni, “Regret bounds for batched bandits,” in AAAI, pp. 7340–7348, 2021.   
[33] Z. Gao, Y. Han, Z. Ren, and Z. Zhou, “Batched multi-armed bandits problem,” in NeurIPS, pp. 501–511, 2019.   
[34] V. Perchet, P. Rigollet, S. Chassang, and E. Snowberg, “Batched bandit problems,” in COLT, p. 1456, 2015.   
[35] I. Usmanova, M. Kamgarpour, A. Krause, and K. Y. Levy, “Fast projection onto convex smooth constraints,” in ICML, vol. 139, pp. 10476–10486, PMLR, 2021.   
[36] S. Bubeck, “Convex optimization: Algorithms and complexity,” Found. Trends Mach. Learn., vol. 8, no. 3-4, pp. 231–357, 2015.   
[37] D. van der Hoeven, “Exploiting the surrogate gap in online multiclass classification,” in NeurIPS 2020, 2020.   
[38] A. Koppel, F. Y. Jakubiec, and A. Ribeiro, “A saddle point algorithm for networked online convex optimization,” IEEE Trans. Signal Process., vol. 63, no. 19, pp. 5149–5164, 2015.   
[39] C. Li, P. Zhou, L. Xiong, Q. Wang, and T. Wang, “Differentially private distributed online learning,” IEEE Trans. Knowl. Data Eng., vol. 30, no. 8, pp. 1440–1453, 2018.   
[40] A. Koloskova, S. U. Stich, and M. Jaggi, “Decentralized stochastic optimization and gossip algorithms with compressed communication,” in ICML, vol. 97, pp. 3478–3487, PMLR, 2019.   
[41] C. Hu, J. T. Kwok, and W. Pan, “Accelerated gradient methods for stochastic optimization and online learning,” in NeurIPS, pp. 781–789, Curran Associates, Inc., 2009.   
[42] Z. Lei, X. Ye, Y. Wang, D. Li, and J. Xu, “Efficient online model adaptation by incremental simplex tableau,” in AAAI, pp. 2161–2167, AAAI Press, 2017.   
[43] A. Destounis, D. Tsilimantos, M. Debbah, and G. S. Paschos, “Learn2mac: Online learning multiple access for urllc applications,” in INFOCOM WKSHPS, pp. 1–6, IEEE, 2019.   
[44] S. Bubeck, “Introduction to online optimization,” Lecture Notes, 2011.   
[45] A. Jacobsen and A. Cutkosky, “Unconstrained online learning with unbounded losses,” in ICML, vol. 202, pp. 14590–14630, PMLR, 2023.   
[46] A. Cutkosky, “Artificial constraints and hints for unbounded online learning,” in COLT, vol. 99, pp. 874–894, PMLR, 2019.   
[47] B. Awerbuch, “Optimal distributed algorithms for minimum weight spanning tree, counting, leader election and related problems (detailed summary),” in STOC, pp. 230–240, 1987.   
[48] S. Shalev-Shwartz, “Online learning: Theory, algorithms, and applications,” The Hebrew University of Jerusalem. PH.d. thesis, July 2007.   
[49] C.-C. Chang and C.-J. Lin, “LIBSVM: A library for support vector machines,” ACM Transactions on Intelligent Systems and Technology, vol. 2, pp. 27:1–27:27, 2011.   
[50] G. Wang, D. Zhao, and L. Zhang, “Minimizing adaptive regret with one gradient per iteration,” in IJCAI, pp. 2762–2768, 2018.   
[51] K. M. Anstreicher, “Towards a practical volumetric cutting plane method for convex programming,” SIAM J. Optim., vol. 9, no. 1, pp. 190–206, 1998.

![](images/4904c7fa665507328c9e2066b926ba447d049c51f69f730735195a19ab84548f.jpg)



Jiandong Liu received the B.S. degree in Information Security from Xidian University, Xi’an, China in 2018 and the M.S. degree in Cybersecurity from University of Science and Technology of China, Hefei, China in 2021. He is currently working toward the Ph.D. degree in Cybersecurity with the School of Cybersecurity, University of Science and Technology of China, Hefei, China. His research interests include online learning and privacy-preserving computation.

![](images/59e73d1ff9fd8fae5b20b34eaf3bfcd00f5a0e9aef2efc37128bc24b1adce44c.jpg)



Lan Zhang is currently a Professor at the School of Computer Science and Technology, University of Science and Technology of China. She received her Ph.D degree and Bachelor degree from Tsinghua University, China. Her research interests include mobile computing, privacy protection, and data sharing and trading.

![](images/4d0e0ab497811e343d8a6b4f6e9c65db7042731caf48d8c2e4898159bffe0ab4.jpg)



Fengxiang He is a Lecturer at Artificial Intelligence and its Applications Institute, School of Informatics, University of Edinburgh. He received his BSc in statistics from the University of Science and Technology of China, MPhil and PhD in computer science from the University of Sydney. His research interest is trustworthy AI, including deep learning theory, privacy-preserving machine learning, decentralised learning, etc., and their applications in economics and finance. He is an Area Chair of ICML, NeurIPS, UAI, AISTATS, and ACML.

![](images/a3257739e0db94d4491ce332ffb5ef48dfe27e274b9e06ccebe0266f16a2d429.jpg)



Networking.

Chi Zhang received his B.Eng. degree in Computer Science and Technology from University of Science and Technology of China (USTC) with the honor of The Talent Program in Computer and Information Science and Technology in 2017. Then, he got his Ph.D. degree in Computer Science and Technology from USTC in 2023. His main research interest is data center networking, edge computing and algorithms. Many of his works have been published in top conferences and journals such as IEEE INFOCOM, ACM MobiHoc and IEEE/ACM Transactions on

![](images/b805e425cd98ed4cf184a61a68825f2d1fd4bc62b460429d7f096eb0b515f935.jpg)



Shanyang Jiang received the B.S. degree in Internet of Things Engineering from Hefei University of Technology, Hefei, China in 2018 and the M.S. degree in School of Data Science from University of Science and Technology of China, Hefei, China in 2021. He is currently working toward the Ph.D degree in School of Data Science from University of Science and Technology of China, Hefei, China. His research intersets include crowdsourcing and mechanism design.

![](images/301c264d125e9a98bbdab9a76180b0557187a2776277dc57b6eb72d7e9acdce2.jpg)



Xiang-Yang Li is a professor, the Executive Dean of College of Information Science and Artificial Intelligence, the Executive Dean of School of Computer Science and Technology, University of Science and Technology of China. He is an ACM Fellow (2019), IEEE fellow (2015), an ACM Distinguished Scientist (2014). He was a full professor at Computer Science Department of IIT. He served as a co-Chair of ACM China Council and editors of several premium journals. Dr. Li received MS (2000) and PhD (2001) degree at Department of Computer Science from

University of Illinois at Urbana-Champaign. He received a Bachelor degree at Department of Computer Science from Tsinghua University, P.R. China, in 1995. His research interests include Artificial Intelligence of Things(AIOT), privacy and security of AIOT, and data sharing and trading.

# APPENDIX A

ALGORITHMIC DESCRIPTIONS OF cutting-plane AND AGD

In this section, we present formal descriptions of the cuttingplane and AGD algorithms utilized in Section V-B in Algs. 3 and 4, respectively. The cutting-plane algorithm employed in this paper is a stochastic version of the algorithm proposed in [35]. Meanwhile, the AGD algorithm used in this paper is a constrained version of the algorithm presented in [41]. In Algs. 3 and 4, the procedures $\mathcal { A } _ { i n i t }$ and A correspond to the initialization and update rules in Alg. 2.

Algorithm 3 Cutting Plane Algorithm [35]   
1: Input: Compact convex set C and number of iterations $\nu$ 2: Initialize the model $x_{1} \leftarrow \arg \min_{x \in C} \|x\|$ 3: Initialize the auxiliary parameters for cutting-plane: $(\mathcal{M}_{1}, k, \nu, S_{x}, S_{f}) \leftarrow \mathcal{A}_{init}(\nu)$

4: for $k = 1$ to ν do

5: Call a value-gradient oracle ${ \mathcal { O } } _ { v , g }$ to obtain:

$$
(\hat {f} _ {k} (x _ {k}), \nabla \hat {f} _ {k} (x _ {k})) \leftarrow \mathcal {O} _ {v, g} (\hat {f} _ {k}, x _ {k}),
$$

where ${ \hat { f } } _ { k } ( \cdot )$ is an unbiased estimator for the objective loss function $\bar { f } ( \cdot )$

▷ Completed in Convergecast in Alg. 2

6: Update the model and parameters:

$$
x _ {k + 1}, (\mathcal {M} _ {k + 1}, k + 1, \nu , S _ {x}, S _ {f}) \leftarrow
$$

$$
\mathcal {A} (x _ {k}, \hat {f} _ {k} (x _ {k}), \nabla \hat {f} _ {k} (x _ {k}), (\mathcal {M} _ {k}, k, \nu , S _ {x}, S _ {f}))
$$

7: end for

8: return $\bar { x } = x _ { \nu + 1 }$

9: procedure $\mathbf { \mathcal { A } } _ { i n i t } ( \nu )$

10: Set $x_{1} \leftarrow \arg \min_{x \in \mathcal{C}} \| x\|$ 11: Set $\mathcal{M}_1 \leftarrow \{x \in \mathbb{R}^d : \| x - x_1 \|_\infty \leq \| \mathcal{C} \|\}$ $\triangleright \mathcal{M}_1$ can be any other $\ell_\infty$ -ball containing $\mathcal{C}$ 12: return $(\mathcal{M}_1, 1, \nu, \{x_1\}, \{\})$

13: end procedure

14: procedure $\boldsymbol { \mathcal { A } } ( \hat { x } , f ( \hat { x } ) , \nabla f ( \hat { x } ) , ( \boldsymbol { \mathcal { M } } , k , \nu , S _ { x } , S _ { f } ) )$

15: Construct $\mathcal { M } ^ { \mathrm { ( i ) } }$ using Vaidya’s method [51] such that:

$$
\{x \in \mathcal {M}: \langle \nabla f (\hat {x}), x - \hat {x} \rangle \leq 0 \} \subseteq \mathcal {M} ^ {(1)}
$$

16: Choose $\boldsymbol { x } ^ { ( 1 ) } \in \mathcal { M } ^ { ( 1 ) }$ using the centering method [51]

17: Set $\ell \gets 1$

18: while $x ^ { ( \ell ) } \notin { \mathcal { C } }$ do

19: Compute the vector w such that:

$$
\mathcal {C} \subseteq \left\{x \in \mathbb {R} ^ {d}: \left\langle w, x - x ^ {(\ell)} \right\rangle \leq 0 \right\}
$$

20: Construct $\mathcal { M } ^ { ( \ell + 1 ) }$ via Vaidya’s method such that:

$$
\left\{x \in \mathcal {M} ^ {(\ell)}: \left\langle w, x - x ^ {(\ell)} \right\rangle \leq 0 \right\} \subseteq \mathcal {M} ^ {(\ell + 1)}
$$

21: Choose $x ^ { ( \ell + 1 ) } \in \mathcal { M } ^ { ( \ell + 1 ) }$ via the centering method 22: Update $\ell \gets \ell + 1$

23: end while

24: Update ${ \overline { { S _ { x } } } }  S _ { x } \cup \{ x ^ { ( \ell ) } \}$ and $S _ { f } \cup \{ f ( \hat { x } ) \}$

25: $\mathbf { i f } ^ { \cdot } k < \nu$ then

26: return $\overline { { ( x ^ { ( \ell ) } } } , ( \mathcal { M } ^ { ( \ell ) } , k + 1 , \nu , S _ { x } , S _ { f } ) )$

27: else

28: Set $\bar { x }  S _ { x } [ k ^ { * } ]$ , where $k ^ { * } = \arg \operatorname* { m i n } _ { k \in [ \nu ] } S _ { f } [ k ]$

29: return (¯x $, ( \mathcal { M } ^ { ( \ell ) } , k + 1 , \nu , S _ { x } , S _ { f } ) )$

30: end if

31: end procedure

Algorithm 4 Accelerated Gradient Descent (AGD) [41]   
1: Input: Compact convex set C, number of iterations $\nu$ , smoothness constant $L_{G}$ for the gradient oracles, and a uniform upper bound $\sigma_{g}^{2}$ for the variance of gradient oracles ▷ In the k-th instance of T-DBCO with AGD in Alg. 2, we take $L_{G}$ as $nL_{G}$ and $\sigma_{g}^{2}$ as $\frac{n\sigma^{2}}{b_{k}-2\mu}$ , where $L_{G}$ and $\sigma^{2}$ are the smoothness constant and bound for gradient variances, respectively, for $f(x;\xi),\xi\sim\mathbb{P}_{i}$ for $i\in[n]$ .
2: Initialize the model $x_{1} \leftarrow \arg \min_{x \in C} \|x\|$ 3: Initialize the auxiliary parameters for AGD:

$$
(y _ {1}, z _ {1}, k, \nu) \leftarrow \mathcal {A} _ {\text { init }} (\nu)
$$

4: for $k = 1$ to ν do

5: Call a gradient oracle ${ \mathcal { O } } _ { g }$ to obtain:

$$
\nabla \hat {f} _ {k} (x _ {k}) \leftarrow \mathcal {O} _ {g} (\hat {f} _ {k}, x _ {k}),
$$

where $\hat { f } _ { k } ( \cdot )$ is an unbiased estimator for the objective function $\breve { f } ( \cdot )$

▷ Completed in Convergecast in Alg. 2

6: Update the model and parameters:

$$
x _ {k + 1}, (y _ {k + 1}, z _ {k + 1}, k + 1, \nu) \leftarrow
$$

$$
\mathcal {A} (x _ {k}, 0, \nabla \hat {f} _ {k} (x _ {k}), (y _ {k}, z _ {k}, k, \nu))
$$

7: end for

8: return $\bar { x } = x _ { \nu + 1 }$

9: procedure $\mathcal { A } _ { i n i t } ( \nu )$

10: Set $y _ { 1 } = z _ { 1 }  \mathrm { a r g }$ minx∈C ∥x∥

11: return $( y _ { 1 } , z _ { 1 } , 1 , \nu )$

12: end procedure

13: procedure $\boldsymbol { \mathcal { A } } ( \hat { x } , f ( \hat { x } ) , \nabla f ( \hat { x } ) , ( \hat { y } , \hat { z } , k , \nu ) )$

▷ f (ˆx) is unused in  for AGD

14: $b \gets \frac { \sqrt { 5 } \sigma _ { g } } { 3 \lVert c \rVert }$ $\| \mathcal { C } \| \triangleq \operatorname* { m a x } _ { x , y \in \mathcal { C } } \| x - y \|$

$L _ { \ell } \gets \ddot { b } \ell ^ { 3 / 2 } + L _ { G }$ and $\begin{array} { r } { \alpha _ { \ell } \gets \frac { 2 } { \ell + 1 } } \end{array}$ for $\ell \in [ \nu ]$

16: Set $\begin{array} { r } { y ^ { \prime } \  \  \Pi _ { \mathcal { C } } ( \hat { x } \ - \ \frac { 1 } { L _ { k } } \nabla f ( \hat { x } ) ) } \end{array}$ , where $\Pi _ { C } ( x ) \triangleq$ arg mi $\mathbf { 1 } _ { y \in \mathcal { C } } \| y - x \|$

17: Set $\begin{array} { r } { z ^ { \prime } \gets \overline { { \Pi _ { \mathcal { C } } ( \hat { z } - \frac { \mathrm { i } } { \alpha _ { k } } ( \hat { x } - y ^ { \prime } ) ) } } } \end{array}$

18: if $k < \nu$ then

19: Set $x ^ { \prime }  ( 1 - \alpha _ { k + 1 } ) y ^ { \prime } + \alpha _ { k + 1 } z ^ { \prime }$

20: return $( x ^ { \prime } , ( y ^ { \prime } , z ^ { \prime } , k + 1 , \nu ) )$

21: else

22: return $( y ^ { \prime } , ( y ^ { \prime } , z ^ { \prime } , k + 1 , \nu ) ) )$

23: end if

24: end procedure

# APPENDIX B

# RESULTS FOR I.I.D. STOCHASTIC DOCO

We analyze the communication complexity lower bound and develop communication-efficient algorithms for stochastic DOCO where all feedbacks are identically and independently distributed (i.i.d.). In this context, it holds that $\mathbb { P } _ { i } \equiv \mathbb { P }$ for a common distribution P, where $\mathbb { P } _ { i }$ represents the feedback distribution for learner $\textit { i } \in \ [ n ]$ . We establish the lower bound in Appendix B-A and introduce communication-efficient algorithms with nearly optimal regret in Appendix B-B. Furthermore, we present experimental results pertaining to i.i.d. stochastic DOCO in Appendix B-C.

# A. Communication Complexity Lower Bounds

The following theorem establishes that there exists an i.i.d. stochastic DOCO instance where any algorithm with a not sufficiently large communication budget r incurs $\omega ( { \sqrt { n T } } )$ regret loss. The detailed proof is deferred to Appendix F.

Theorem 6. Consider i.i.d. stochastic DOCO with linear loss functions (cf. Eq. (3)) and static communication patterns. There exists a learner network and loss functions $f ( x ; \xi _ { t } ^ { i } ) f o r ~ i \in [ n ]$ and $t \in [ T ]$ , where $\xi _ { t } ^ { i } \sim \mathbb { P }$ for some distribution P, such that:

$$
\bar {\mathcal {R}} _ {1} (T) = \Omega \big (\max \{n, n \sqrt {T / r}, \sqrt {n T} \} \big),
$$

where n is the number of learners, T is the learning time, and r is the communication budget.

A direct corollary of Theorem 6 is as follows.

Corollary 5. Consider i.i.d. stochastic DOCO with loss functions satisfying Definitions 1-4 and static communication patterns. The communication complexity to achieve the minimax regret $\mathcal { O } ( \sqrt { n T } )$ is $\Omega ( n )$ with respect to the number of learners n and learning time T .

Similarly, as in the general stochastic case, the communication complexity is linear in the number of learners n but independent of the learning time T .

# Proof sketch of Theorem 6.

In the i.i.d. stochastic setting, we utilize the claw-shaped network and devise the loss functions for each learner in the same manner as learners $n ^ { \prime } + 1$ to n in the general stochastic setting. The analysis follows a similar line of reasoning as the general stochastic DOCO.

Comparison with existing works: Our work is the first to analyze the communication complexity for i.i.d. stochastic DOCO. Wang et al. [25] established that a communication complexity lower bound of Ω(n) is necessary to attain the minimax regret in distributed MAB on star networks, where the arms collection of each learner is i.i.d. stochastic. Our analysis extends the results of [25] to i.i.d. stochastic DOCO with connected networks and general convex loss functions.

# B. Algorithm Design

As i.i.d. stochastic feedbacks represent a special case of general stochastic feedbacks, our DB2O algorithm proposed in Section V is applicable in these scenarios. Prior to our work, the DMA algorithm [13] achieved a minimax regret bound of $\mathcal { O } ( \sqrt { n T } )$ and communication complexity of $\mathcal { O } ( n ^ { 3 / 2 } \sqrt { T } )$ for loss functions satisfying Definitions 1, 3, and 5. By Theorems 4 and 5, our DB2O with AGD achieves the minimax regret up to polylogarithmic factors and reduces the communication complexity of DMA by an $\tilde { \mathcal { O } } ( ( n T ) ^ { 1 / 4 } )$ for loss functions under the same assumptions. Meanwhile, our DB2O with cuttingplane nearly achieves the minimax regret and reduces DMA’s communication complexity by an $\tilde { \mathcal { O } } ( \sqrt { n T } )$ factor. Compared to DMA, DB2O with cutting-plane additionally assumes bounded loss functions and a fat feasible region, relaxing the smoothness assumption.

We proceed to revise DB2O to further reduce the regret bounds by additive terms, specifically tailored for the i.i.d. stochastic scenario. In this setting, all learners’ feedbacks adhere to the same global distribution, enabling each learner to update their local models based solely on their individual data prior to initiating communication. Subsequently, learners proceed to update models as in the general stochastic setting.

In line with this concept, for the i.i.d. stochastic setting, we devise communication-efficient algorithms based on a revised DB2O algorithm. In this section, we assume the loss functions to be $L _ { G } .$ -smooth and the gradient variance to be upper-bounded by $\sigma ^ { 2 } .$ , a commonly adopted assumption in the DOCO literature [1], [13], [20]. In the revised DB2O, for $t \leq t _ { 1 }$ , learner $i \in [ n ]$ updates its local models using online gradient descent (OGD) [13]:

$$
x _ {t} ^ {i} = \Pi_ {\mathcal {C}} \left(x _ {t - 1} ^ {i} - \eta_ {t - 1} \nabla f _ {t - 1} ^ {i} (x _ {t - 1} ^ {i})\right), \text {   for   } t = 2, 3, \dots , t _ {1}, \tag {10}
$$

where $\begin{array} { r } { x _ { 1 } ^ { i } = \hat { x } _ { 1 } , \eta _ { t } = \frac { 1 } { L _ { G } + \sqrt { 2 t } \sigma / \| C \| } } \end{array}$ for each t, and $\| { \mathcal { C } } \| \triangleq$ $\operatorname* { m a x } _ { x , y \in { \mathcal { C } } } \| x - y \|$ . Subsequently, for $t > t _ { 1 }$ , learners update local models using the original DB2O method.

Compared to the original DB2O algorithm, in the revised DB2O for the i.i.d. stochastic setting, learner $i \in [ n ]$ more effectively utilizes its loss function $f _ { t } ^ { i } ( \cdot )$ for $t \leq t _ { 1 }$ . In this setting, the expectation of $f _ { t } ^ { i } ( \cdot )$ is $\textstyle { \frac { 1 } { n } } { \bar { f } } ( \cdot )$ , where $\bar { f } ( \cdot )$ is the optimization objective (cf. Eq. (2)).

# Theoretical advantages of the revised DB2O.

Similarly, as in the general stochastic setting, we implement the revised DB2O using cutting-plane and AGD update rules. The theoretical properties are presented in Theorems 7 and 8.

Theorem 7. In the revised DB2O with cutting-plane, let the loss functions $f ( x ; \xi ) , \xi \sim \mathbb { P } _ { i } f o r i \in [ n ]$ satisfy Definitions $I , 3 ,$ 4, and 5, and $\mathbb { P } _ { i } \equiv \mathbb { P }$ for a common distribution P. We choose update and initialization rules A and $A _ { i n i t }$ as in cutting-plane, the same model update times m, time points $\{ t _ { k } \} _ { k \in [ m ] }$ , and batch sizes $\{ b _ { k } \} _ { k \in [ m ] }$ as in Theorem 4. Then, the regret bound is $\tilde { \mathcal { O } } ( n ^ { 3 / 2 } \sqrt { d } + d ^ { \acute { 3 } / 2 } \sqrt { n T } )$ , and the communication cost is $\tilde { \mathcal { O } } ( d n )$ , where n is the learner number, T is the learning time, and d is the model dimension.

Theorem 8. In the revised DB2O with AGD, let the loss functions $f ( x ; \xi ) , \xi \sim \mathbb { P } _ { i } f o r ~ i \in [ n ]$ ] satisfy Definitions 1, 3, and 5, and $\mathbb { P } _ { i } \equiv \mathbb { P }$ for a common distribution P. We choose update and initialization rules A and $\mathcal { A } _ { i n i t }$ as in AGD, the model update times $m = 1 + \lceil \ln \ln T \rceil$ , the time sequence as

$$
\left\{\begin{array}{l}t _ {1} = 2 \mu + n + \left\lfloor n ^ {\frac {5}{3}} \right\rfloor\\t _ {k} = t _ {m ^ {\prime}} + \left\lceil (T - t _ {m ^ {\prime}}) ^ {\frac {2 - 2 ^ {- k + 2}}{2 - 2 ^ {- m + 1}}} \right\rceil , f o r 2 \leq k \leq m,\end{array}\right.
$$

and the batch sizes as

$$
\left\{ \begin{array}{l} b _ {1} = 2 \mu + n \\ b _ {k} = \max \Big \{2 \mu + n, \Big \lfloor \frac {t _ {k}}{C _ {2} n ^ {1 / 4} t _ {k} ^ {1 / 4} + 1} \Big \rfloor \Big \},   f o r   2 \leq k \leq m, \end{array} \right.
$$

where µ is the BFS tree’s height and $C _ { 2 } > 0$ is a constant. Then, the regret bound $i s \tilde { \mathcal { O } } ( n ^ { 1 1 / 6 } + \sqrt { n T } )$ , and the communication cost is $\tilde { \mathcal { O } } ( n ^ { 5 / 3 } + n ^ { 5 / 4 } T ^ { 1 / 4 } )$ , where n is the learner number and T is the learning time.

Similar to the general stochastic setting, the revised DB2O with cutting-plane or AGD is nearly regret-optimal in terms of $n$ and T . Specifically, the revised DB2O with cutting-plane achieves a communication complexity of $\tilde { \mathcal { O } } ( n )$ , which nearly matches the lower bound in Corollary 5. However, its regret and communication complexity additionally depend on the model dimension $d ,$ which proves to be suboptimal when compared to the state-of-the-art DMA algorithm with no dependence on d [13]. On the other hand, the revised DB2O with AGD achieves the lowest dimension-free communication complexity of ${ \tilde { \cal O } } ( n ^ { 5 / 4 } T ^ { 1 / 4 } )$ for $T \gg n$ .

# Proof sketch of Theorems 7 and 8.

In the revised DB2O, for $t \leq t _ { 1 }$ , the OGD update rule in Eq. (10) ensures that:

$$
\Sigma_ {t = 1} ^ {t _ {1}} \bar {f} (x _ {t}) - t _ {1} \cdot \min _ {x \in \mathcal {C}} \bar {f} (x) = \mathcal {O} (n \sqrt {t _ {1}}).
$$

The regret analysis for $t _ { 1 } < t \leq T$ then follows the same analysis as for Theorems 4 and 5. The regret bounds in Theorems 7 and 8 then follow. The communication analysis for the revised DB2O follows the same line of analysis as in Theorems 4 and 5.

Comparison with existing works: Compared to the original DB2O algorithms, the revised versions reduce regret by additive terms in n while maintaining communication complexity unchanged, up to polylogarithmic factors. This improvement is particularly beneficial in scenarios where $T$ is not significantly larger than $n .$ . When compared to the state-of-the-art DMA algorithm [13], the revised DB2O with cutting-plane reduces communication complexity by a factor of $\tilde { \mathcal { O } } ( \sqrt { n T } )$ in n and T . In contrast to DMA, the revised DB2O with cutting-plane additionally assumes bounded loss functions and a fat feasible region. Meanwhile, the revised DB2O with AGD provides the lowest dimension-free communication complexity, reducing the current state-of-the-art result [13] by a factor of $\tilde { \mathcal { O } } ( n ^ { 1 / 4 } \bar { T } ^ { 1 / 4 } )$ for loss functions under the same assumptions.

The revised DB2O under milder assumptions: The revised DB2O algorithms with cutting-plane and AGD are essentially analogous to the original versions in Section V-B. The primary modification involves employing the OGD update rule (cf. Eq. (10)) for $t \leq t _ { 1 }$ . Subsequently, for $t > t _ { 1 }$ , the revised DB2O algorithms are applicable under the same more lenient assumptions detailed in Section V-B. For $t \leq t _ { 1 }$ , OGD ensures applicability in scenarios with unbounded feasible regions $\mathbb { R } ^ { d }$ , maintaining a regret bound of $\mathcal { O } ( n \sqrt { t _ { 1 } } )$ [13]. By leveraging the relaxed assumptions for OGD [13] and those introduced in Section V-B for DB2O, the revised DB2O with AGD operates effectively in unbounded feasible regions $\mathbb { R } ^ { d }$ . On the other hand, the revised DB2O with cutting-plane caters to scenarios where loss functions are convex and smooth, the expected loss functions satisfy Definition 4, and the variances of loss values and gradients are bounded.

Similar to the general stochastic setting, if the tree is not given, learners in this scenario build the BFS tree using megamerger and flooding algorithms [47] and then run the revised DB2O. This process incurs a communication cost of $\scriptstyle { \mathcal { O } } ( n ^ { 2 } )$ in ${ \mathcal { O } } ( n )$ timeslots. Before building the tree, learners update local models using Eq. (10) with $\eta = \Theta ( 1 / \sqrt { n } )$ . According to [44], the revised DB2O incurs an extra regret of $\mathcal { O } ( n ^ { 3 / 2 } )$ , which is negligible when $T \gg n$ . The revised DB2O with cutting-plane (AGD) remains the most communication-efficient (dimension-independent) algorithm in this scenario.

# C. Experiments

Implementation details: In the experiments for i.i.d. stochastic DOCO, we choose the same datasets as in Section VII. We preprocess each dataset by scaling each feature to [−1, 1] and normalizing each sample to unit length. Each dataset is split randomly in uniform size for the learners. We order each learner’s dataset randomly and reveal the t-th sample to him/her at time t. The baselines and other implementation details remain the same as in Section VII.

Experimental results: We adjust the batch size in DMA to tune its communication budget. We adjust the constants $C _ { 1 }$ and $C _ { 2 }$ in Theorems 7 and 8 to tune the budgets for $\mathrm { D B 2 O } _ { c }$ and $\mathrm { D B } 2 0 _ { a }$ . Fig. 9 depicts that on 8-node networks, $\mathrm { D B } 2 0 _ { a }$ and $\mathrm { D B 2 O } _ { c }$ respectively need around 10% and 1% communication cost of DMA to converge to the optimal error rate. On 32-node networks, $\mathrm { D B } 2 0 _ { a }$ and $\mathrm { D B 2 O } _ { c }$ require around 50% and 10% communication cost required by DMA to converge. Similarly, as in the general stochastic setting, the communication-saving of $\mathrm { D B } 2 0 _ { a }$ and $\mathrm { D B 2 O } _ { c }$ is more prominent on the 8-node networks since the learning time is much larger than the number of learners (cf. Theorems 7 and 8).

Subsequently, we evaluate the necessary communication complexity of both DB2O and DMA to achieve a low error rate for various values of $T$ on 8-node networks using the covtype dataset. The target is determined as the maximum of the optimal error rates among the considered algorithms. Fig. 10a illustrates that on 8-learner networks, $\mathrm { D B } 2 0 _ { a }$ achieves approximately 90% communication savings over DMA for all $T .$ For $T$ values up to $2 . 8 8 \times 1 0 ^ { 4 }$ , DB2Oc exhibits a communication saving of around 95% over DMA, and for $T$ values exceeding $4 . 3 2 \times 1 0 ^ { 4 }$ , the communication saving of $\mathrm { D B 2 O } _ { c }$ over DMA is approximately 98%. On the 32-node clique network, Fig. 10b indicates that $\mathrm { D B } 2 0 _ { a }$ and $\mathrm { D B 2 O } _ { c }$ achieve communication savings ranging from 60% to 90% and 80% to 97%, respectively, as the learning time increases from 3,600 to 18,000. Meanwhile, on the 32-node cycle network, $\mathrm { D B } 2 0 _ { a }$ and $\mathrm { D B 2 O } _ { c }$ achieve communication savings in the range of 25% to 70% and 40% to 90%, respectively, as the learning time increases from 3,600 to 18,000.

# APPENDIX C

# DIAMETER-DEPENDENT COMMUNICATION COMPLEXITY

In this section, we analyze the communication complexity of DOCO algorithms to achieve the minimax regret on learner networks with a diameter of D. The theoretical results are summarized in Table V. Our analysis demonstrates that our proposed algorithms nearly achieve the diameter-dependent minimax regret bound with almost optimal communication complexity. Notably, our results reduce the communication cost of the algorithms with the currently state-of-the-art regret bound for the dependence of n, D, and T . We provide outlines of the proofs of the results in this section and defer the complete details to Appendix J.

![](images/90a15fc805fdc4e99a812b7d326f9a0c775b8b9d983e9d7bb68d2a49293a975f.jpg)



(a) covtype (cycle)

![](images/f1ef331d8543bd4c191ca2c1e929e06eeac22eddd0bf6eb7309d5172f3e60118.jpg)



(b) epsilon (cycle)

![](images/c9080e9d658a4cbe5b47895c1017abcb6cff9991926990d43be5b8072066b3b6.jpg)



(c) covtype (clique)

![](images/2791c161a20b6e0e014b03839ed7685a3a73702880a4950fa6159d0890c285f1.jpg)



(d) epsilon (clique)   
Fig. 9: Online classification error rates in i.i.d. stochastic DOCO. The line indicates the averages, and the shaded area is where all error rates lie in across 10 runs.

TABLE V: Minimax regret bounds, communication complexity lower bounds for regret-optimal DOCO, currently state-of-the-art (SOTA) communication complexity for DOCO with the state-of-the-art regret, and our algorithms’ communication complexity on learner networks with diameter D. The gossip algorithm [11] achieves the currently SOTA communication complexity for the adversarial setting, which is linear in the learner network’s edge number and learning time. In a network with diameter $D ,$ , the edge number equals $\mathcal { O } ( D + ( n - D ) ^ { 2 } )$ ). The $\tilde { \Omega } _ { \mathbf { \lambda } } ( \tilde { \mathcal { O } } )$ notation hides polylogarithmic factors in n and T when $T \gg n$ .

<table><tr><td></td><td>Adversarial</td><td>General stochastic</td><td>i.i.d. stochastic</td></tr><tr><td>Minimax regret bounds</td><td> $\mathcal{O}(n\sqrt{DT})$  (Cor. 6)</td><td colspan="2"> $\mathcal{O}(\sqrt{nT})$  [13]</td></tr><tr><td>Comm. complexity lower bounds</td><td> $\Omega(nT/D)$  (Cor. 6)</td><td> $\Omega(D \ln \ln T + n)$  (Cor. 7)</td><td> $\Omega(n)$  (Cor. 8)</td></tr><tr><td>Currently SOTA comm. complexity</td><td> $\mathcal{O}((D + (n - D)^2)T)$  [11]</td><td colspan="2"> $\mathcal{O}(n^{3/2}\sqrt{T})$  [13]</td></tr><tr><td>Our algs.’ comm. complexity</td><td> $\mathcal{O}(nT/D)$  (Cor. 4)</td><td> $\tilde{\mathcal{O}}(n)$  (Thm. 4)</td><td> $\tilde{\mathcal{O}}(n)$  (Thm. 7)</td></tr></table>

![](images/ab533db7e21e3fcca072276c90919d1effd2baf3ee5d5612967de3d718d2d7b6.jpg)



(a) 8-learner

![](images/8574274e29fd564f1c4047ac114c2dbfa86f0ab78e21add7845f15ab6c98c567.jpg)



(b) 32-learner   
Fig. 10: Communication cost to achieve the target error rates in i.i.d. stochastic DOCO. The curves are the minimum communication cost to achieve the error rates specified by the bars. The target error rate is the maximum of the evaluated algorithms’ optimal error rates for each T and network.

# A. Communication Complexity for Adversarial DOCO

We begin by studying the diameter-dependent communication complexity of adversarial DOCO. In Theorem 9, we prove that there exists a hard instance for which the regret loss equals $\Omega ( n ^ { 3 / 2 } T / \sqrt { r } )$ when the budget r is not sufficiently large.

Theorem 9. Consider adversarial DOCO with linear loss functions (cf. Eq. (3)) and static communication patterns. There exists a learner network with diameter D and loss sequence $\{ f _ { t } ^ { i } \} _ { t \in [ T ] , i \in [ n ] }$ such that:

$$
\mathcal {R} _ {1} (T) = \Omega (\max \{n \sqrt {D T}, n ^ {3 / 2} T / \sqrt {r} \}), \tag {11}
$$

where n is the number of learners, T is the learning time, and r is the communication budget.

Based on Theorem 9, we conclude that an algorithm requires a communication budget of $r ~ = ~ \Omega ( n T / D )$ to achieve the minimax regret of $\mathcal { O } ( n \sqrt { D T } )$ .

Corollary 6. Consider adversarial DOCO with loss functions satisfying Definitions 1-4 and static communication patterns in networks with diameter D. The communication complexity to achieve the minimax regret $\mathcal { O } ( n \sqrt { D T } )$ is $\Omega ( n T / D )$ with respect to the number of learners n, learning time T , and network’s diameter D.

The theory demonstrates that, in the diameter-dependent problem setting, learners require more communication cost to achieve the diameter-dependent minimax regret in networks with smaller diameters. Particularly, in all-connected networks where $D \ = \ 1$ , the minimax regret is $\mathcal { O } ( n \sqrt { T } )$ , and the corresponding communication complexity lower bound is $\Omega ( n T )$ . In this scenario, compared to the problem setting with arbitrary connected networks, the minimax regret is reduced by a factor of $\Theta ( { \sqrt { n } } )$ , while the communication complexity lower bound is increased by a factor of $\Theta ( n )$ .

# Proof sketch of Theorem 9.

1) Constructing the network: We construct the learner network as a claw-shaped network depicted in Fig. 11. In this network, each message transmitted from learner $\textit { i } > n ^ { \prime }$ to learner 1 requires $\geq n ^ { \prime }$ timeslots and communication budget, where $n ^ { \prime } \triangleq \operatorname* { m i n } \{ \lceil n / 2 \rceil , D \}$ . According to the analysis of OCOD in [30], delaying messages by $n ^ { \prime }$ timeslots can increase the regret by an $\bar { \Omega ( \sqrt { n ^ { \prime } } ) } = \bar { \Omega ( \sqrt { D } ) }$ factor. This property is crucial in deriving the $\Omega ( n \sqrt { D T } )$ regret for sufficiently large r.   
2) Constructing loss functions: Let $t _ { k } + 1$ denote the first time at which learner 1 receives information from $\lfloor { \frac { n - n ^ { \prime } } { 2 } } \rfloor$ 2 learners i with $i > n ^ { \prime }$ , and let m be the number of such $t _ { k } .$ . We set $t _ { 0 } = 0$ and $t _ { m + 1 } = T$ . In each interval $[ t _ { k - 1 } + 1 , t _ { k } ]$ for $k \in [ m + 1 ]$ , we identify those learners i whose messages are not received by learner 1 at time $t _ { k }$ and set $f _ { t } ^ { i } ( x ) = \langle x , { \hat { z } } _ { k } \rangle$ ⟩ for $t _ { k - 1 } < t \leq t _ { k }$ . Here, $\hat { z } _ { k }$ is uniform in $\{ 0 , 1 \} ^ { d }$ . For the other

![](images/3e88617925630f0c7f33cd9573e8ccf4b923dc1a0ce5e2a918d47d91c6e26764.jpg)



Fig. 11: Claw-shaped network with diameter D.

learners, the constructed loss is zero. Learner 1 then incurs a high regret since its models are independent of the functions of $\Omega ( n - n ^ { \prime } ) = \Omega ( n )$ learners in each interval.

3) Lower bounding the regret: By analyzing our constructed loss functions, we can derive that:

$$
\mathbb {E} [ \mathcal {R} _ {1} (T) ] = \Omega (n T / \sqrt {m}).
$$

In the claw-shaped network illustrated in Fig. 11, we have $m =$ $\mathcal { O } ( \operatorname* { m i n } ( T / D , r / n ) )$ . Therefore, Theorem 9 can be obtained.

Optimality of DB-TDOCO: According to Corollary 4, when the parameters are set as given by Eq. (8), DB-TDOCO achieves a regret bound of $\mathcal { O } ( n \sqrt { D T } )$ with a communication complexity of $\mathcal { O } ( n T / D )$ . Thus, by applying Corollary 6, we can conclude that DB-TDOCO, with this parameter selection, achieves both the optimal diameter-dependent regret bound and communication complexity.

B. Communication Complexity for General Stochastic DOCO

We proceed to investigate the diameter-dependent communication complexity for general stochastic DOCO algorithms. We establish that a hard instance exists where the regret scales as $\omega ( { \sqrt { n T } } )$ for r that is not sufficiently large, as stated in the following theorem.

Theorem 10. Consider general stochastic DOCO with linear loss functions (cf. Eq. (3)) and static communication patterns. There exists a learner network with diameter D and loss functions $f ( x ; \xi _ { t } ^ { i } )$ for $i \in [ n ]$ and $t \in [ T ]$ , where $\xi _ { t } ^ { i } \sim \mathbb { P } _ { i }$ for some distribution $\mathbb { P } _ { i } ,$ , such that:

$$
\begin{array}{l} \bar {\mathcal {R}} _ {1} (T) = \Omega \big (\max \left\{n \min \left\{n, T \right\}, \right. \\ \left. n \sqrt {T / r}, n ^ {\frac {1}{2 - 2 ^ {- 2 r / D}}} T ^ {\frac {1}{2 - 2 ^ {- 2 r / D}}} \right\}), \tag {12} \\ \end{array}
$$

where n is the number of learners, T is the learning time, and r is the communication budget.

Via similar arithmetic computations as in the proof for Corollary 2, we determine that $r = \Omega ( \operatorname* { m a x } ( D \ln \ln T , n ) )$ is necessary to ensure that $\bar { \mathcal { R } } _ { 1 } ( T )$ in Eq. (12) is smaller than $\mathcal { O } ( \sqrt { n T } )$ , the minimax regret, when $T \gg n$ .

Corollary 7. Consider general stochastic DOCO with loss functions satisfying Definitions 1-4 and static communication patterns in networks with diameter D. The communication complexity to achieve the minimax regret $\mathcal { O } ( \sqrt { n T } )$ is $\Omega ( \operatorname* { m a x } \{ D$ ln ln $T , n \}$ with respect to the number of learners n, learning time T , and network’s diameter D.

Our theoretical analysis suggests that achieving the minimax regret of $\mathcal { O } ( \sqrt { n T } )$ requires a communication complexity of $\tilde { \Omega } ( n )$ for networks with arbitrary diameter D as $D = { \mathcal { O } } ( n )$ Thus, the communication complexity of general stochastic DOCO is insensitive to the network’s diameter.

# Proof sketch of Theorem 10.

1) Constructing the network: Similarly, as in adversarial DOCO, we adopt the claw-shaped learner network in Fig. 11.   
2) Constructing loss functions: Let $n ^ { \prime } = \operatorname* { m a x } \{ \lceil n / 2 \rceil , D \}$ . We uniformly sample ℓ from [d] and define the loss functions as in $\operatorname { E q . } \ ( 3 )$ , which take the form $f ( x ; \xi _ { t } ^ { i } ) = \left. x , \xi _ { t } ^ { i } \right.$ . For learner $i \leq n ^ { \prime }$ , we set $\xi _ { t } ^ { i }$ to be an all-zero vector. For learner $i > n ^ { \prime }$ , the ℓ-th coordinate of $\xi _ { t } ^ { i }$ is drawn from a Bernoulli distribution with mean $\frac { 1 } { 2 } - \epsilon .$ , while the other coordinates are drawn uniformly from {0, 1}. We select the parameter ϵ to maximize the regret of learner 1.   
3) Lower bounding the regret: Let $t _ { k } + 1$ denote the first time that learner 1 receives information from learner $i > n ^ { \prime }$ which is sent at some time $t _ { k - 1 } < t \leq t _ { k }$ , and let m be the number of such $t _ { k }$ . By optimally tuning the parameter ϵ in our constructed loss, we obtain:

$$
\mathbb {E} _ {\ell} [ \bar {\mathcal {R}} _ {1} (T) ] = \Omega (\max \{n \min \{D, T \}, n \sqrt {T / r}, n ^ {\frac {1}{2 - 2 ^ {- m}}} T ^ {\frac {1}{2 - 2 ^ {- m}}} \}).
$$

By the definition of $\{ t _ { k } \} _ { k \in [ m ] }$ , we have m $\leq r / n ^ { \prime } \leq 2 r / D$ in the claw-shaped network shown in Fig. 11. Theorem 10 then follows.

Optimality of DB2O: In the general stochastic setting, the communication complexity lower bound and minimax regret bound in the diameter-dependent setting (cf. Table V) are essentially the same as those in Section IV-B, where arbitrary connected networks are considered. DB2O with cutting-plane using the parameters in Theorem 4 achieves a regret bound and communication complexity that are nearly optimal in the general stochastic setting. Meanwhile, DB2O with AGD using the parameters in Theorem 5 achieves the nearly optimal regret bound and state-of-the-art dimension-free communication complexity in the general stochastic setting.

# C. Communication Complexity for i.i.d. Stochastic DOCO

For the i.i.d. stochastic setting where all learners’ feedbacks are i.i.d. distributed, we establish in the following theorem that the regret is $\omega ( { \sqrt { n T } } )$ for a low communication budget r in a hard instance.

Theorem 11. Consider i.i.d. stochastic DOCO with linear loss functions (cf. Eq. (3)) and static communication patterns. There exists a learner network with diameter D and loss functions $f ( x ; \xi _ { t } ^ { i } )$ for $i \in [ n ]$ and $t \in [ T ]$ , where $\xi _ { t } ^ { i } \sim \mathbb { P }$ for some distribution P, such that:

$$
\bar {\mathcal {R}} _ {1} (T) = \Omega \big (\max \{n, n \sqrt {T / r}, \sqrt {n T} \} \big),
$$

where n is the number of learners, T is the learning time, and r is the communication budget.

The minimum budget r in Theorem 11 to achieve the minimax regret $\mathcal { O } ( \sqrt { n T } )$ is Ω(n).

Corollary 8. Consider i.i.d. stochastic DOCO with loss functions satisfying Definitions 1-4 and static communication patterns in networks with diameter D. The communication complexity to achieve the minimax regret $\mathcal { O } ( \sqrt { n T } )$ is $\Omega ( n )$

with respect to the number of learners $n ,$ learning time $T ,$ , and network’s diameter D.

Similarly, as in the general stochastic setting, the communication complexity of i.i.d. stochastic DOCO algorithms is not sensitive to the network’s diameter.

# Proof sketch of Theorem 11.

We choose the claw-shaped network illustrated in Fig. 11 and construct the loss functions in the same manner as in the proof of Theorem 6. The proof of Theorem 11 follows a similar line of analysis as in Theorem 6.

Optimality of (the revised) DB2O: In the i.i.d. stochastic setting, the communication complexity lower bound and minimax regret bound in the diameter-dependent setting (see Table V) are essentially identical to those in Appendix B-A. DB2O with the cutting-plane update rule and parameters given in Theorem 4 achieves regret and communication complexity that are optimal in terms of n and T in the i.i.d. stochastic setting up to polylogarithmic factors. Meanwhile, DB2O with the AGD update rule and parameters given in Theorem 5 achieves nearly optimal regret bounds and state-of-the-art dimensionfree communication complexity in the i.i.d. stochastic setting. Furthermore, the revised DB2O with cutting-plane and AGD in Appendix B-B reduce the regret of DB2O with cuttingplane and AGD by additive terms without increasing the communication complexity beyond polylogarithmic factors. The regret and communication complexity of the revised DB2O with cutting-plane are also optimal within polylogarithmic factors.

# APPENDIX D PROOFS IN SECTION IV-A

This section serves to provide the detailed proofs for Theorem 1 and Corollary 1 in Section IV-A. The proof in this section is organized as follows:

1) In Lemma 1, we show that using the construction in Section IV-A,

$$
\mathbb {E} [ \mathcal {R} _ {1} (T) ] = \Omega \big (n \mathbb {E} \big [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} \big ] \big),
$$

where each $\epsilon _ { k , j }$ is uniform in $\{ - 1 , 1 \}$ and $\tau _ { k } \triangleq t _ { k } - t _ { k - 1 }$ for $k \in [ m + \bar { 1 } ] ;$ ;

∈  2) In Lemmas 2-4, we show $\begin{array} { r } { \Omega \big ( n \mathbb { E } \big [ \operatorname* { m a x } _ { j \in [ d ] } \Sigma _ { k = 1 } ^ { m + 1 } \tau _ { k } \epsilon _ { k , j } \big ] \big ) } \end{array}$ is minimized when $| \tau _ { k } - \tau _ { k ^ { \prime } } | \leq \bar { 1 }$ for $k \ne k ^ { \prime } ;$

3) In Lemmas 5-7, we prove that:

$$
\mathbb {E} [ \mathcal {R} _ {1} (T) ] = \Omega \big (n T / m \cdot \mathbb {E} \big [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \epsilon_ {k, j} \big ] \big);
$$

4) In Lemmas 8, we show that:

$$
\mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \epsilon_ {k, j} ] = \Omega (\sqrt {m});
$$

5) At the end of this section, we conclude the proofs of Theorem 1 and Corollary 1.

Recall that in Section IV-A, we construct the learner network as the claw-shaped one in Fig. 3. We construct loss functions depending on specific time points $t _ { k }$ for $k \in [ m ] . ~ t _ { k } + 1$ is the first time learner 1 learns information on $f _ { t } ^ { i } , i > n ^ { \prime }$ for $t _ { k - 1 } < t \leq t _ { k }$ . We let $t _ { 0 } ~ = ~ 0$ and $t _ { m + 1 } = T$ . The loss functions

$$
f _ {t} ^ {i} (x) = \left\langle x, z _ {t} ^ {i} \right\rangle , x \in \mathcal {C} = \{x \in \mathbb {R} _ {\geq 0} ^ {d} | 1 \leq \| x \| _ {1} \leq 2 \}
$$

for learner $i \in [ n ]$ are as follows:

1) For $\textit { i } \leq \textit { n } ^ { \prime }$ , we ensure $f _ { t } ^ { i } \equiv 0$ by setting $z _ { t } ^ { i } \equiv \mathbf { 0 }$ for $t \in [ T ]$ , where 0 denotes the all-zero vector.   
2) For $\textit { i } > n ^ { \prime } .$ , we set $z _ { t } ^ { i } \equiv \hat { z } _ { k }$ for $t _ { k - 1 } < t \leq t _ { k }$ and $k \in [ m + 1 ]$ , where each $\hat { z } _ { k }$ is uniform in $\{ 0 , 1 \} ^ { d }$ .

Lemma 1. In DOCO with the network and loss functions constructed in Section IV-A, it holds that:

$$
\mathbb {E} [ \mathcal {R} _ {1} (T) ] = \Omega \big (n \mathbb {E} \big [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} \big ] \big),
$$

where each $\epsilon _ { k , j }$ is uniform in $\{ - 1 , 1 \}$ and $\tau _ { k } \triangleq t _ { k } - t _ { k - 1 } .$ for $k \in [ m + 1 ]$ .

Proof. Our construction ensures that each $x _ { t } ^ { 1 } \in \mathcal { C }$ is independent of $z _ { t } ^ { i }$ for $i > n ^ { \prime }$ . As each $z _ { t } ^ { i }$ is uniform in $\{ 0 , 1 \} ^ { d }$ for $i > n ^ { \prime } .$ , it follows that $\mathbb { E } [ f _ { t } ^ { i } ( x _ { t } ^ { 1 } ) ] = \mathbb { E } \| x _ { t } ^ { 1 } \| _ { 1 } / 2$ for $i > n ^ { \prime }$ . By $\| { \boldsymbol x } \| _ { 1 } \geq 1$ for $x \in \mathcal { C } = \{ \bar { x } \in \mathbb { R } _ { > 0 } ^ { d } | 1 \leq \| x \| _ { 1 } \leq 2 \}$ , we obtain $\mathbb { E } [ f _ { t } ^ { \bar { i } } ( x _ { t } ^ { 1 } ) ] \geq 1 / 2$ . It follows that:

$$
\begin{array}{l} \mathbb {E} \left[ \mathcal {R} _ {1} (T) \right] \geq \mathbb {E} \left[ \left(n - n ^ {\prime}\right) T / 2 - \min _ {x \in \mathcal {C}} \left\langle x, \Sigma_ {i = n ^ {\prime}} ^ {n} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \hat {z} _ {k} \right\rangle \right] \\ = \Omega \left(n \mathbb {E} \left[ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} \right]\right), \tag {13} \\ \end{array}
$$

where the equality follows from that 
x, Σm+1k=1 τkzˆk , x ∈ C $\left. x , \Sigma _ { k = 1 } ^ { m + 1 } \tau _ { k } \hat { z } _ { k } \right. , x \in \mathcal { C }$ is minimized when x is an indcoordinate that is minimum in $\Sigma _ { k = 1 } ^ { m + 1 } \tau _ { k } \hat { z } _ { k } \in \mathbb { R } ^ { d }$ one non-zero.

We proceed to prove that for fixed $m ,$ the expression maxj∈[d $\begin{array} { r } { \operatorname* { m a x } _ { j \in [ d ] } \sum _ { k = 1 } ^ { m + 1 } \tau _ { k } \epsilon _ { k , j } } \end{array}$ ] Σk=1 τkϵk,j where τk ∈ N, k ∈ [m + 1] and m+1 $\tau _ { k } ~ \in ~ \mathbb { N } , k ~ \in ~ [ m ~ + ~ 1 ]$ Σk=1 τk = T , is minimized when |τk − τk′ | ≤ 1 for k ̸= k′. m+1 $\Sigma _ { k = 1 } ^ { m + 1 } \bar { \tau _ { k } } = T$ $| \tau _ { k } - \tau _ { k ^ { \prime } } | \leq 1$ $k \neq k ^ { \prime }$ We assume, for contradiction, that there exists $\ell , \ell ^ { \prime } \in [ m + 1 ]$ such that:

$$
\tau_ {\ell} - \tau_ {\ell^ {\prime}} \geq 2. \tag {14}
$$

Let $\tau _ { k } ^ { \prime } \in \mathbb { N } , k \in [ m + 1 ]$ be the sequence such that:

$$
\left\{ \begin{array}{l l} \tau_ {\ell^ {\prime}} + 1 = \tau_ {\ell^ {\prime}} ^ {\prime} \leq \tau_ {\ell} ^ {\prime} = \tau_ {\ell} - 1 \\ \tau_ {k} = \tau_ {k} ^ {\prime}, & k \neq \ell^ {\prime}, \ell . \end{array} \right. \tag {15}
$$

Denote the following cumulative distribution functions:

$$
\left\{ \begin{array}{l l} G _ {j} (x) \triangleq \operatorname * {P r} [ \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} \leq x ], & j \in [ d ] \\ G _ {j} ^ {\prime} (x) \triangleq \operatorname * {P r} [ \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} ^ {\prime} \epsilon_ {k, j} \leq x ], & j \in [ d ] \\ \bar {G} (x) \triangleq \operatorname * {P r} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} \leq x ] \\ \bar {G} ^ {\prime} (x) \triangleq \operatorname * {P r} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} ^ {\prime} \epsilon_ {k, j} \leq x ]. \end{array} \right. \tag {16}
$$

Lemma 2. It holds that:

$$
\int_ {- T} ^ {T} g (x) G _ {1} (x) d x \leq \int_ {- T} ^ {T} g (x) G _ {1} ^ {\prime} (x) d x,
$$

where $g ( x ) \in [ 0 , 1 ]$ monotonically increases $f o r \ x \in \mathbb { R } .$

Proof. As $\epsilon _ { k , j } , k \in [ m + 1 ] , j \in [ d ]$ are i.i.d. and uniform in $\{ - 1 , 1 \}$ , it holds that:

$$
\operatorname * {P r} [ \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} = x ] = \operatorname * {P r} [ \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} = - x ]
$$

for each $j \in [ d ]$ and $x \in \mathbb { R }$ . It follows that $G _ { 1 } ( x ) + G _ { 1 } ( - x ^ { - } ) =$ 1 for $x \geq 0$ . Similarly, it holds that $G _ { 1 } ^ { \prime } ( x ) + G _ { 1 } ^ { \prime } ( - x ^ { - } ) = 1$ for $x \geq 0 .$ . Thus, we obtain for $x \geq 0 { : }$

$$
G _ {1} (x) - G _ {1} ^ {\prime} (x) = G _ {1} ^ {\prime} (- x ^ {-}) - G _ {1} (- x ^ {-}). \tag {17}
$$

By Eq. (16), it holds that:

$$
\begin{array}{l} G _ {1} (x) = \Sigma_ {y _ {1} \in \{- 1, 1 \}} \Sigma_ {y _ {2} \in \{- 1, 1 \}} \operatorname * {P r} [ \epsilon_ {\ell^ {\prime}, 1} = y _ {1}, \epsilon_ {\ell , 1} = y _ {2} ]. \\ \operatorname * {P r} \left[ \Sigma_ {k \neq \ell , \ell^ {\prime}} \tau_ {k} \epsilon_ {k, 1} \leq x - \tau_ {\ell^ {\prime}} y _ {1} - \tau_ {\ell} y _ {2} \right] \\ = \frac {1}{4} \Sigma_ {y _ {1} \in \{- 1, 1 \}} \Sigma_ {y _ {2} \in \{- 1, 1 \}} \operatorname * {P r} [ \Sigma_ {k \neq \ell , \ell^ {\prime}} \tau_ {k} \epsilon_ {k, 1} \leq \\ \left. x - \tau_ {\ell^ {\prime}} y _ {1} - \tau_ {\ell} y _ {2} \right], \\ \end{array}
$$

and

$$
\begin{array}{l} G _ {1} ^ {\prime} (x) = \frac {1}{4} \Sigma_ {y _ {1} \in \{- 1, 1 \}} \Sigma_ {y _ {2} \in \{- 1, 1 \}} \operatorname * {P r} [ \Sigma_ {k \neq \ell , \ell^ {\prime}} \tau_ {k} ^ {\prime} \epsilon_ {k, 1} \leq \\ \left. x - \tau_ {\ell^ {\prime}} ^ {\prime} y _ {1} - \tau_ {\ell} ^ {\prime} y _ {2} \right] \\ = \frac {1}{4} \left(\operatorname * {P r} \left[ \Sigma_ {k \neq \ell , \ell^ {\prime}} \tau_ {k} \epsilon_ {k, 1} \leq x - \tau_ {\ell^ {\prime}} - \tau_ {\ell} \right] + \right. \\ \operatorname * {P r} [ \Sigma_ {k \neq \ell , \ell^ {\prime}} \tau_ {k} \epsilon_ {k, 1} \leq x + \tau_ {\ell^ {\prime}} + \tau_ {\ell} ] + \\ \operatorname * {P r} \left[ \Sigma_ {k \neq \ell , \ell^ {\prime}} \tau_ {k} \epsilon_ {k, 1} \leq x - \tau_ {\ell^ {\prime}} + \tau_ {\ell} - 2 \right] + \\ \operatorname * {P r} \left[ \Sigma_ {k \neq \ell , \ell^ {\prime}} \tau_ {k} \epsilon_ {k, 1} \leq x + \tau_ {\ell^ {\prime}} - \tau_ {\ell} + 2 \right] \Big), \\ \end{array}
$$

where the second equality follows from Eq. (15). Then,

$$
G _ {1} (x) - G _ {1} ^ {\prime} (x) =
$$

$$
\frac {1}{4} \big (\operatorname * {P r} [ x - \tau_ {\ell^ {\prime}} + \tau_ {\ell} - 2 <   \Sigma_ {k \neq \ell , \ell^ {\prime}} \tau_ {k} \epsilon_ {k, 1} \leq x - \tau_ {\ell^ {\prime}} + \tau_ {\ell} ] -
$$

$$
\operatorname * {P r} [ x + \tau_ {\ell^ {\prime}} - \tau_ {\ell} <   \Sigma_ {k \neq \ell , \ell^ {\prime}} \tau_ {k} \epsilon_ {k, 1} \leq x + \tau_ {\ell^ {\prime}} - \tau_ {\ell} + 2 ]).
$$

Denote $\begin{array} { r } { \gamma ( x ) = \frac { 1 } { 4 } \operatorname* { P r } [ x < \Sigma _ { k \neq \ell , \ell ^ { \prime } } \tau _ { k } \epsilon _ { k , 1 } \leq x + 2 ] } \end{array}$ . We obtain:

$$
G _ {1} (x) - G _ {1} ^ {\prime} (x) = \gamma (x - \tau_ {\ell^ {\prime}} + \tau_ {\ell} - 2) - \gamma (x + \tau_ {\ell^ {\prime}} - \tau_ {\ell}).
$$

By Eq. (17), we then obtain:

$$
\begin{array}{l} \int_ {- T} ^ {T} g (x) \left(G _ {1} (x) - G _ {1} ^ {\prime} (x)\right) d x = \\ \int_ {0} ^ {T} (G _ {1} (x) - G _ {1} ^ {\prime} (x)) (g (x) - g (- x)) d x \\ = \int_ {0} ^ {+ \infty} (G _ {1} (x) - G _ {1} ^ {\prime} (x)) (g (x) - g (- x)) d x \\ = \int_ {0} ^ {+ \infty} (\gamma (x - \tau_ {\ell^ {\prime}} + \tau_ {\ell} - 2) - \gamma (x + \tau_ {\ell^ {\prime}} - \tau_ {\ell})) \cdot \\ (g (x) - g (- x)) d x, \\ \end{array}
$$

where the second equality follows from $G _ { 1 } ( x ) = G _ { 1 } ^ { \prime } ( x ) = 1$ for $x \ge T$ . Denote ${ \bar { g } } ( x ) \triangleq g ( x ) - g ( - x )$ ). As $g ( x ) \in [ 0 , 1 ]$ monotonically increases, it holds that $\bar { g } ( x ) \in [ 0 , 1 ]$ monotonically increases for $x \geq 0$ . It follows that:

$$
\begin{array}{l} \int_ {- T} ^ {T} g (x) \left(G _ {1} (x) - G _ {1} ^ {\prime} (x)\right) d x = \\ \int_ {0} ^ {+ \infty} (\gamma (x - \tau_ {\ell^ {\prime}} + \tau_ {\ell} - 2) - \gamma (x + \tau_ {\ell^ {\prime}} - \tau_ {\ell})) \bar {g} (x) d x \\ = \int_ {- 2 - \tau_ {\ell^ {\prime}} + \tau_ {\ell}} ^ {+ \infty} \gamma (x) \bar {g} (x + \tau_ {\ell^ {\prime}} - \tau_ {\ell} + 2) d x - \\ \int_ {\tau_ {\ell^ {\prime}} - \tau_ {\ell}} ^ {+ \infty} \gamma (x) \bar {g} (x - \tau_ {\ell^ {\prime}} + \tau_ {\ell}) d x \\ \end{array}
$$

$$
\begin{array}{l} = \int_ {- 2 - \tau_ {\ell^ {\prime}} + \tau_ {\ell}} ^ {+ \infty} \gamma (x) (\bar {g} (x + \tau_ {\ell^ {\prime}} - \tau_ {\ell} + 2) - \bar {g} (x - \tau_ {\ell^ {\prime}} + \tau_ {\ell})) d x \\ - \int_ {\tau_ {\ell^ {\prime}} - \tau_ {\ell}} ^ {- 2 - \tau_ {\ell^ {\prime}} + \tau_ {\ell}} \gamma (x) \bar {g} (x - \tau_ {\ell^ {\prime}} + \tau_ {\ell}) d x \\ \leq 0, \tag {18} \\ \end{array}
$$

where the second equality follows from variable substitution, and the inequality follows from $\gamma ( \boldsymbol { x } ) \ge 0$ , Eq. (14), and $\bar { g } ( x ) \geq$ 0 monotonically increases for $x \geq 0$ . The result then follows from Eq. (18). □

Lemma 3. Let $\Sigma _ { k = 1 } ^ { m + 1 } \tau _ { k } = \Sigma _ { k = 1 } ^ { m + 1 } \tau _ { k } ^ { \prime } = T$ and Eqs. (14) and

$$
\mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} ] \geq \mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} ^ {\prime} \epsilon_ {k, j} ],
$$

where each $\epsilon _ { k , j }$ is uniform in {−1, 1}.

Proof. It holds that:

$$
\begin{array}{l} \mathbb {E} \left[ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} \right] = \int_ {- T} ^ {T} x \bar {G} (d x) \\ = x \bar {G} (x) \Big | _ {- T ^ {-}} ^ {T} - \int_ {- T} ^ {T} \bar {G} (x) d x \\ = T - \int_ {- T} ^ {T} \bar {G} (x) d x, \\ \end{array}
$$

where the second equality holds from integration by parts, and the last equality follows from $\bar { G } ( T ) = 1$ and $\bar { G } ( T ^ { - } ) = 0$ . It follows that:

$$
\mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} ] \geq \mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} ^ {\prime} \epsilon_ {k, j} ]
$$

if $\begin{array} { r } { \int _ { - T } ^ { T } \bar { G } ( x ) d x \leq \int _ { - T } ^ { T } \bar { G } ^ { \prime } ( x ) d x } \end{array}$ . Thus, it suffices to prove that:

$$
\int_ {- T} ^ {T} \bar {G} (x) d x \leq \int_ {- T} ^ {T} \bar {G} ^ {\prime} (x) d x. \tag {19}
$$

Note that:

$$
\begin{array}{l} \operatorname * {P r} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} \leq x ] = \Pi_ {j = 1} ^ {d} \operatorname * {P r} [ \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} \leq x ] \\ = \operatorname * {P r} ^ {d} [ \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, 1} \leq x ], \\ \end{array}
$$

where the last equality follows from the fact that the distributions of the variables Σm+1 $\Sigma _ { k = 1 } ^ { m + 1 } \tau _ { k } \epsilon _ { k , j }$ 1 τkϵk,j and Σm+1k=1 τ $\Sigma _ { k = 1 } ^ { m + 1 } \tau _ { k } \epsilon _ { k , j ^ { \prime } }$ are identical for $j \neq j ^ { \prime }$ . It follows that:

$$
\bar {G} (x) = \Pi_ {j = 1} ^ {d} G _ {j} (x) = G _ {1} ^ {d} (x).
$$

By Eq. (19), it follows that, to prove Lemma 3, it suffices to prove that:

$$
\int_ {- T} ^ {T} G _ {1} ^ {d} (x) d x \leq \int_ {- T} ^ {T} G _ {1} ^ {\prime d} (x) d x.
$$

For $0 \leq k \leq d - 1$ , the function $G _ { 1 } ^ { k } ( x ) G _ { 1 } ^ { \prime d - 1 - k } ( x ) \in [ 0 , 1 ]$ monotonically increases for $x \in \mathbb { R }$ . By Lemma 2, we obtain $\begin{array} { r } { \int _ { - T } ^ { T } \dot { G } _ { 1 } ^ { d } ( x ) d x \ \leq \ \int _ { - T } ^ { T } G _ { 1 } ^ { d - 1 } ( x ) G _ { 1 } ^ { \prime } \dot { ( x ) } d x \ \leq \ \dots \ \leq } \end{array}$ T $\int _ { - T } ^ { T } G _ { 1 } ^ { \prime d } ( x ) d x$ .

Lemma 3 implies that if there exists $\ell , \ell ^ { \prime } \in [ m + 1 ]$ such

that Eq. (14) holds, we can find $\{ \tau _ { k } ^ { \prime } \} _ { k \in [ m + 1 ] }$ such that:

$$
\mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} ] \geq \mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} ^ {\prime} \epsilon_ {k, j} ].
$$

Thus, $\mathbb { E } [ \operatorname* { m a x } _ { j \in [ d ] } \Sigma _ { k = 1 } ^ { m + 1 } \tau _ { k } \epsilon _ { k , j } ]$ is minimized when $| \tau _ { k } - \tau _ { k ^ { \prime } } | \leq$ 1 for any $k , \bar { k ^ { \prime } } .$ . We formalize this result in the following lemma.

Lemma 4. The expression $\tau _ { k } \in \mathbb { N } , k \in [ m + 1 ]$ and $\Sigma _ { k = 1 } ^ { m + 1 } \tau _ { k } = T$ $\mathbb { E } [ \operatorname* { m a x } _ { j \in [ d ] } \Sigma _ { k = 1 } ^ { m + 1 } \tau _ { k } \epsilon _ { k , j } ]$ k=1 k k,j is minimized when where $| \tau _ { k } - \tau _ { k ^ { \prime } } | \leq 1 f o r$ any $k , k ^ { \prime }$ , where each $\epsilon _ { k , j }$ is uniform in $\{ - 1 , 1 \}$ .

We proceed to prove that:

$$
\mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} ] = \Omega (T / m) \cdot \mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \epsilon_ {k, j} ]
$$

in Lemmas 5-7. Let $\tau _ { k } ^ { \Delta } \in \mathbb { N } , k \in [ m + 1 ]$ be the sequence such that there exists $\ell \in [ m + 1 ]$ satisfying:

$$
\left\{ \begin{array}{l l} \tau_ {\ell} ^ {\Delta} = \tau_ {\ell} - 1 \geq 0 \\ \tau_ {k} ^ {\Delta} = \tau_ {k}, & k \neq \ell . \end{array} \right. \tag {20}
$$

Denote:

$$
\left\{ \begin{array}{l l} G _ {j} ^ {\Delta} (x) \triangleq \operatorname * {P r} [ \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} ^ {\Delta} \epsilon_ {k, j} \leq x ] & j \in [ d ] \\ \bar {G} ^ {\Delta} (x) \triangleq \operatorname * {P r} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} ^ {\Delta} \epsilon_ {k, j} \leq x ]. \end{array} \right. \tag {21}
$$

Lemma 5. It holds that:

$$
\int_ {- T} ^ {T} g (x) G _ {1} (x) d x \leq \int_ {- T} ^ {T} g (x) G _ {1} ^ {\Delta} (x) d x,
$$

where $g ( x ) \in [ 0 , 1 ]$ monotonically increases for $x \in \mathbb { R }$ .

Proof. Similarly to Eq. (17), it holds that:

$$
G _ {1} (x) - G _ {1} ^ {\Delta} (x) = G _ {1} ^ {\Delta} (- x ^ {-}) - G _ {1} (- x ^ {-}). \tag {22}
$$

By Eq. (16), it holds that:

$$
\begin{array}{l} G _ {1} (x) = \Sigma_ {y \in \{- 1, 1 \}} \operatorname * {P r} [ \epsilon_ {\ell , 1} = y ] \operatorname * {P r} [ \Sigma_ {k \neq \ell} \tau_ {k} \epsilon_ {k, 1} \leq x - \tau_ {\ell} y ] \\ = \frac {1}{2} \Sigma_ {y \in \{- 1, 1 \}} \operatorname * {P r} [ \Sigma_ {k \neq \ell} \tau_ {k} \epsilon_ {k, 1} \leq x - \tau_ {\ell} y ], \\ \end{array}
$$

and

$$
\begin{array}{l} G _ {1} ^ {\Delta} (x) = \frac {1}{2} \Sigma_ {y \in \{- 1, 1 \}} \operatorname * {P r} [ \Sigma_ {k \neq \ell} \tau_ {k} ^ {\Delta} \epsilon_ {k, 1} \leq x - \tau_ {\ell} ^ {\Delta} y ] \\ = \frac {1}{2} \Sigma_ {y \in \{- 1, 1 \}} \operatorname * {P r} [ \Sigma_ {k \neq \ell} \tau_ {k} \epsilon_ {k, 1} \leq x - \tau_ {\ell} y + y ], \\ \end{array}
$$

where the second equality follows from Eq. (20). It follows that:

$$
\begin{array}{l} G _ {1} (x) - G _ {1} ^ {\Delta} (x) = \frac {1}{2} \left(\operatorname * {P r} \left[ x + \tau_ {\ell} - 1 <   \Sigma_ {k \neq \ell} \tau_ {k} \epsilon_ {k, 1} \leq x + \tau_ {\ell} \right] \right. \\ \left. - \operatorname * {P r} \left[ x - \tau_ {\ell} <   \Sigma_ {k \neq \ell} \tau_ {k} \epsilon_ {k, 1} \leq x - \tau_ {\ell} + 1 \right]\right). \\ \end{array}
$$

The rest of the proof follows the same line of analysis as in Lemma 2. □

Lemma 6. Let $\Sigma _ { k = 1 } ^ { m + 1 } \tau _ { k } = T$ and Eq. (20) hold. It holds that:

$$
\mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} ] \geq \mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} ^ {\Delta} \epsilon_ {k, j} ],
$$

where each $\epsilon _ { k , j }$ is uniform in {−1, 1}.

Proof. Following a similar line of analysis as in Lemma 3,

Lemma 6 holds if $\begin{array} { r l r } { \int _ { - T } ^ { T } G _ { 1 } ^ { d } ( x ) d x } & { { } \leq } & { \int _ { - T } ^ { T } G _ { 1 } ^ { \Delta ^ { d } } ( x ) d x } \end{array}$

By Lemma 5, it holds that $\begin{array} { r l } { \int _ { - T } ^ { T } G _ { 1 } ^ { d } ( x ) d x } & { { } \leq } \end{array}$

$$
\int_ {- T} ^ {T} G _ {1} ^ {d - 1} (x) G _ {1} ^ {\Delta} (x) d x \leq \dots \leq \int_ {- T} ^ {T} G _ {1} ^ {\Delta^ {d}} (x) d x \text {as}
$$

$G _ { 1 } ^ { k } ( x ) G _ { 1 } ^ { \Delta ^ { d - 1 - k } } ( x ) ~ \in ~ [ 0 , 1 ]$ −T  monotonically increases for $x \in \mathbb { R }$ for $0 \leq k \leq d - 1$ . □

Combining Lemmas 4 and 6, we obtain the following lemma.

Lemma 7. Let $\tau _ { k } \in \mathbb { N } f o r \ k \in [ m + 1 ] \ s a t i s f y \ \Sigma _ { k = 1 } ^ { m + 1 } \tau _ { k } = T .$ It holds that:

$$
\mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} ] \geq \left\lfloor \frac {T}{m + 1} \right\rfloor \mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \epsilon_ {k, j} ],
$$

where each $\epsilon _ { k , j }$ is uniform in {−1, 1}.

Proof. By Lemma 4, E[maxj∈[d] Σm+1k=1 τkϵk,j ], where τk ∈ N $k \in [ m + 1 ]$ $\ u _ { \star } , \mathbb { E } [ \operatorname* { m a x } _ { j \in [ d ] } \Sigma _ { k = 1 } ^ { m + 1 } \tau _ { k } \epsilon _ { k , j } ]$ $\Sigma _ { k = 1 } ^ { m + 1 } \bar { \tau _ { k } } \stackrel { . . . } { = } T$ is minimized when . Lemma 7 then fo $\tau _ { k } \in \mathbb { N }$ $\tau _ { k } \in$ $\left\{ \begin{array} { c c c } { \left\lfloor \frac { T } { m + 1 } \right\rfloor , \left\lceil \frac { T } { m + 1 } \right\rceil } \end{array} \right\}$ $k \in [ m + 1 ]$ from Lemma 6.

Lemma 8 (Lemma 6 in [32]). It holds that:

$$
\mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \epsilon_ {k, j} ] = \Omega (\sqrt {m}),
$$

where each $\epsilon _ { k , j }$ is uniform in {−1, 1}.

Proof. The proof is analogous to that of Lemma 6 in [32]. We present detailed proof for completeness. It holds that:

$$
\mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \epsilon_ {k, j} ] \geq \mathbb {E} [ \max _ {j \in [ 2 ]} \Sigma_ {k = 1} ^ {m + 1} \epsilon_ {k, j} ].
$$

It suffices to prove that:

$$
\mathbb {E} [ \max _ {j \in [ 2 ]} \Sigma_ {k = 1} ^ {m + 1} \epsilon_ {k, j} ] = \Omega (\sqrt {m}).
$$

Notice that E[maxj∈[2] $\begin{array} { r } { \mathbb { E } [ \operatorname* { m a x } _ { j \in [ 2 ] } \Sigma _ { k = 1 } ^ { m + 1 } \epsilon _ { k , j } ] + \mathbb { E } [ \operatorname* { m i n } _ { j \in [ 2 ] } \Sigma _ { k = 1 } ^ { m + 1 } \epsilon _ { k , j } ] = } \end{array}$ $\mathbb { E } [ \Sigma _ { k = 1 } ^ { m + 1 } \epsilon _ { k , 1 } ] + \mathbb { E } [ \bar { \Sigma } _ { k = 1 } ^ { m + 1 } \epsilon _ { k , 2 } ] = 0 ,$ j∈[2] . It follows that:

$$
\mathbb {E} [ \max _ {j \in [ 2 ]} \Sigma_ {k = 1} ^ {m + 1} \epsilon_ {k, j} ] = \mathbb {E} \left| \Sigma_ {k = 1} ^ {m + 1} \epsilon_ {k, 1} \right|.
$$

Denote $X \triangleq \Sigma _ { k = 1 } ^ { m + 1 } \epsilon _ { k , 1 }$ . By Holder’s inequality, it holds that:

$$
(\mathbb {E} | X | ^ {4}) ^ {1 / 3} (\mathbb {E} | X |) ^ {2 / 3} \geq \mathbb {E} | X | ^ {2}.
$$

It follows that:

$$
\mathbb {E} \left| X \right| ^ {2} = \Sigma_ {k = 1} ^ {m + 1} \mathbb {E} [ \epsilon_ {k, 1} ^ {2} ] = m + 1,
$$

and

$$
\begin{array}{l} \mathbb {E} \left| X \right| ^ {4} = \Sigma_ {k = 1} ^ {m + 1} \mathbb {E} [ \epsilon_ {k, 1} ^ {4} + 6 \Sigma_ {i <   k} \epsilon_ {i, 1} ^ {2} \epsilon_ {k, 1} ^ {2} ] \\ = m + 1 + 3 m (m + 1) \leq 3 (m + 1) ^ {2}. \\ \end{array}
$$

Then, we obtain:

$$
\mathbb {E} | X | = \Omega (\sqrt {m}),
$$

and the result follows.

□

Proof of Theorem 1. Combining Lemmas 7 and 8, we obtain:

$$
\mathbb {E} [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} ] = \Omega (T / \sqrt {m}),
$$

where each $\epsilon _ { k , j }$ is uniform in $\{ - 1 , 1 \}$ and $\tau _ { k } \triangleq t _ { k } - t _ { k - 1 }$ for $k \in [ m + 1 ]$ . By Eq. (13), we obtain that, in DOCO with the network and loss functions constructed in Section IV-A:

$$
\mathbb {E} [ \mathcal {R} _ {1} (T) ] = \Omega (n T / \sqrt {m}). \tag {23}
$$

Recall that $t _ { k } + 1$ is the first time that learner 1 learns information on $f _ { t } ^ { i } , i > n ^ { \prime }$ for $t _ { k - 1 } < t \leq t _ { k }$ , and m is the number of such $t _ { k }$ . In the claw-shaped network in Fig. 3, each message takes $n ^ { \prime } = \lceil n / 2 \rceil$ timeslots and consumes $n ^ { \prime }$ budget transmitted from learner $i > n ^ { \prime }$ to learner 1. Thus, it holds that:

$$
m \leq \min ((T - 1) / \lceil n / 2 \rceil , r / \lceil n / 2 \rceil). \tag {24}
$$

By plugging Eq. (24) into Eq. (23), it holds that:

$$
\mathbb {E} [ \mathcal {R} _ {1} (T) ] = \Omega (n ^ {3 / 2} \max \{\sqrt {T}, T / \sqrt {r} \}). \tag {25}
$$

Let $\mathbb { P } _ { \mathcal { F } }$ be the distribution of our constructed loss sequence. By Eq. (25), there exists a loss sequence $\{ f _ { t } ^ { i } \} _ { t \in [ T ] , i \in [ n ] }$ in the support of $\mathbb { P } _ { \mathcal { F } }$ such that Eq. (4) holds. □

Proof of Corollary 1. By Eq. (4) in Theorem 1, to ensure that $\mathcal { R } _ { 1 } ( \bar { T } ) = \mathcal { O } ( n ^ { 3 / 2 } \sqrt { T } )$ for the dependence of n and T . We need to set $r = \Omega ( T )$ . □

# APPENDIX E PROOFS IN SECTION IV-B

This section serves to provide the proofs of Theorem 2 and Corollary 2 in Section IV-B. In Lemmas 9 and 10, we lower bound $\mathbb { E } [ \bar { \mathcal { R } } _ { 1 } ( T ) ]$ w.r.t m for the loss functions constructed in Section IV-B. Theorem 2 then follows from Lemma 10 and $m = \mathcal { O } ( \operatorname* { m i n } ( T / n , r / n )$ .

Recall that in Section IV-B, we take the claw-shaped network in Fig. 3. Denote the Bernoulli distribution with mean $p$ as $B e r ( p )$ . We sample ℓ uniformly from [d] and construct the loss function

$$
f (x; \xi_ {t} ^ {i}) = \left\langle x, \xi_ {t} ^ {i} \right\rangle , x \in \mathcal {C} = \{x \in \mathbb {R} _ {\geq 0} ^ {d} | 1 \leq \| x \| _ {1} \leq 2 \}
$$

as follows:

1) For $i \leq n ^ { \prime } { . }$ we ensure $f ( x ; \xi _ { t } ^ { i } ) \equiv 0$ by setting $\xi _ { t , j } ^ { i } \equiv 0$ for $j \in [ d ]$ , where $\xi _ { t , j } ^ { i }$ is the j-th coordinate of $\xi _ { t } ^ { i } ;$   
2) For $i > n ^ { \prime }$ , we sample $\xi _ { t , \ell } ^ { i }$ from $\mathrm { B e r } ( \frac { 1 } { 2 } - \epsilon )$ and $\xi _ { t , \ell ^ { \prime } } ^ { i }$ from $\mathrm { B e r } \left( { \textstyle { \frac { 1 } { 2 } } } \right)$ for $\ell ^ { \prime } \neq \ell ,$ , where ϵ is a controlled parameter.

Lemma 9. The total variation $T V ( B e r ^ { t } ( 1 / 2 ) , B e r ^ { t } ( 1 / 2 - \epsilon ) )$ satisfies:

$$
T V (B e r ^ {t} (1 / 2), B e r ^ {t} (1 / 2 - \epsilon)) \leq \min (\epsilon \sqrt {2 t}, 1),
$$

where $t \in \mathbb { N } , 0 \leq \epsilon \leq 1 / 2 ,$ , and $B e r ^ { t } ( p )$ denotes the distribution of t i.i.d. Bernoulli variables with mean p.

Proof. By Lemma 7.2 in [44], it holds that:

$$
\operatorname{KL} \left(\operatorname{Ber} ^ {t} (1 / 2 - \epsilon), \operatorname{Ber} ^ {t} (1 / 2)\right) \leq 4 \epsilon^ {2} t.
$$

By Pinsker’s inequality [44], it follows that:

$$
\operatorname{TV} \left(\operatorname{Ber} ^ {t} (1 / 2 - \epsilon), \operatorname{Ber} ^ {t} (1 / 2)\right) \leq
$$

$$
\sqrt {\frac {1}{2} \mathrm{KL} (\mathrm{Ber} ^ {t} (1 / 2) , \mathrm{Ber} ^ {t} (1 / 2 - \epsilon))} \leq \epsilon \sqrt {2 t}.
$$

Lemma 10. In stochastic DOCO with linear loss functions constructed in Section IV-B with $d \ \geq \ 2 ,$ , if the learners communicate in the claw-shaped network (cf. Fig. 3) in a static communication pattern and $t _ { k } + 1$ is the first time learner 1 learns information on $\xi _ { t } ^ { i } , i > n ^ { \prime } f o r t _ { k - 1 } < t \leq t _ { k }$ and $k \in [ m ]$ , then, with an appropriate choice of ϵ in the constructed loss, it holds that:

$$
\mathbb {E} [ \bar {\mathcal {R}} _ {1} (T) ] = \Omega \big (\max \left\{n \min \left\{n, T \right\}, n ^ {\frac {1}{2 - 2 ^ {- m}}} T ^ {\frac {1}{2 - 2 ^ {- m}}} \right\} \big).
$$

Proof. Denote the distribution of $\xi _ { t } ^ { i } , ~ i ~ > ~ n ^ { \prime }$ as Berϵℓ for a given ℓ and ϵ. Let $e _ { \ell }$ be the ℓ-th basis of $\mathbb { R } ^ { d } .$ , i.e., $\scriptstyle e _ { \ell } \mathbf { \dot { s } } { \ j } \scriptscriptstyle -$ th coordinate, $e _ { \ell , j }$ , equals 1 if $j = \ell$ and 0 otherwise. By $\mathcal { C } = \{ x \in \mathbb { R } _ { > 0 } ^ { d } | \bar { 1 } \leq \| x \| _ { 1 } \leq 2 \}$ , it holds that the optimal model $x ^ { * } \triangleq$ arg minx∈C ¯f(x) = eℓ if $\xi _ { t } ^ { i } \sim \mathrm { B e r } _ { \ell } ^ { \epsilon }$ for $i > n ^ { \prime }$ . For each $x _ { t } ^ { 1 } \in \mathcal { C }$ , sample $\mathbf { x } _ { t } ^ { 1 } \in \{ e _ { j } \} _ { j = 1 } ^ { d }$ where $\mathrm { P r } [ \mathbf { x } _ { t } ^ { 1 } = e _ { j } ] \propto$ $\boldsymbol { x } _ { t , \mathcal { I } } ^ { 1 }$ and $\boldsymbol { x } _ { t , \ j } ^ { 1 }$ denotes the j-th coordinate of $\boldsymbol { x } _ { t } ^ { 1 }$ . It holds that $\bar { f } ( x _ { t } ^ { 1 } ) = \| x _ { t } ^ { \circ , \prime } \| _ { 1 } \cdot \mathbb { E } [ \bar { f } ( \mathrm { x } _ { t } ^ { 1 } ) ] \geq \mathbb { E } [ \bar { f } ( \mathrm { x } _ { t } ^ { 1 } ) ] . \mathrm { B y ~ } x ^ { * } = e _ { \ell } \mathrm { ~ i f ~ } \xi _ { t } ^ { i } \sim \mathrm { B e r } _ { \ell } ^ { \epsilon }$ for $i > n ^ { \prime }$ , we obtain:

$$
\begin{array}{l} \mathbb {E} \left[ \bar {\mathcal {R}} _ {1} (T) \right] \geq \Sigma_ {t = 1} ^ {T} \left[ \mathbb {E} _ {\ell} \left[ \bar {f} \left(\mathrm{x} _ {t} ^ {1}\right) \right] - \mathbb {E} _ {\ell} \left[ \bar {f} \left(e _ {\ell}\right) \right] \right] \tag {26} \\ \geq \epsilon (n - n ^ {\prime}) \mathbb {E} _ {\ell} [ \Sigma_ {t = 1} ^ {T} \mathbb {P} _ {\ell , \epsilon} ^ {t - 1} [ \mathrm{x} _ {t} ^ {1} \neq e _ {\ell} ] ], \\ \end{array}
$$

where Pt−1 $\mathbb { P } _ { \ell , \epsilon } ^ { t - 1 }$ ℓ,ϵ is the probability distribution induced by the samples from $\mathrm { B e r } _ { \ell } ^ { \epsilon }$ accessible to learner 1 before time t, and ℓthe second inequality follows from $\begin{array} { r } { \xi _ { t , \ell } ^ { i } \sim \mathrm { B e r } ( \frac { 1 } { 2 } - \epsilon ) } \end{array}$ and $\begin{array} { r } { \xi _ { t , \ell ^ { \prime } } ^ { i } \sim \operatorname { B e r } ( \frac { 1 } { 2 } ) } \end{array}$ for $i > n ^ { \prime }$ and $\ell ^ { \prime } \neq \ell .$ .

Denote $\mathbb { U } ^ { \tilde { t } - 1 }$ as the probability distribution induced by the loss functions constructed in Section IV-B with $\epsilon = 0 ~ ( \mathrm { i . e . }$ , $\begin{array} { r } { \xi _ { t , \ell } ^ { i } \sim \mathrm { B e r } ( \frac { 1 } { 2 } ) } \end{array}$ for $\ell \in [ d ] , i > n ^ { \prime }$ , and $t \in [ T ] )$ that are revealed to learner 1 before time t. It holds that for $t \in [ T ]$ ,

$$
\Sigma_ {\ell = 1} ^ {d} \mathbb {U} ^ {t - 1} (\mathrm{x} _ {t} ^ {1} = e _ {\ell}) = 1. \tag {27}
$$

By Eq. (26), we obtain that for $k \in [ m + 1 ]$ ,

$$
\mathbb {E} [ \bar {\mathcal {R}} _ {1} (T) ] \geq \left\lfloor \frac {n}{2} \right\rfloor \frac {\epsilon}{d} \Sigma_ {\ell = 1} ^ {d} \Sigma_ {j = 1} ^ {k} \Sigma_ {t = t _ {j - 1} + 1} ^ {t _ {j}} \big (1 - \mathbb {P} _ {\ell , \epsilon} ^ {t _ {j - 1}} (\mathrm{x} _ {t} ^ {1} = e _ {\ell}) \big)
$$

$$
= \left\lfloor \frac {n}{2} \right\rfloor \frac {\epsilon}{d} \Sigma_ {\ell = 1} ^ {d} \Sigma_ {j = 1} ^ {k} \Sigma_ {t = t _ {j - 1} + 1} ^ {t _ {j}} \left(1 - \frac {1}{d} + \right.
$$

$$
\mathbb {U} ^ {t _ {j - 1}} \left(\mathrm{x} _ {t} ^ {1} = e _ {\ell}\right) - \mathbb {P} _ {\ell , \epsilon} ^ {t _ {j - 1}} \left(\mathrm{x} _ {t} ^ {1} = e _ {\ell}\right)
$$

$$
\geq \left\lfloor \frac {n}{2} \right\rfloor \frac {\epsilon}{d} \Sigma_ {\ell = 1} ^ {d} \Sigma_ {j = 1} ^ {k} \Sigma_ {t = t _ {j - 1} + 1} ^ {t _ {j}} \Big (1 - \frac {1}{d} -
$$

$$
\left. \operatorname{TV} \left(\mathbb {U} ^ {t _ {j - 1}}, \mathbb {P} _ {\ell , \epsilon} ^ {t _ {j - 1}}\right)\right)
$$

$$
\geq \left\lfloor \frac {n}{2} \right\rfloor \frac {\epsilon}{d} \Sigma_ {\ell = 1} ^ {d} \Sigma_ {j = 1} ^ {k} \Sigma_ {t = t _ {j - 1} + 1} ^ {t _ {j}} \left(1 - \frac {1}{d} - \right.
$$

$$
\operatorname{TV} \left(\operatorname{Ber} ^ {\lfloor n / 2 \rfloor \left(t _ {j - 1} - \lceil n / 2 \rceil + 1\right) +} (1 / 2), \right.
$$

$$
\left. \operatorname{Ber} ^ {\lfloor n / 2 \rfloor (t _ {j - 1} - \lceil n / 2 \rceil + 1) +} (1 / 2 - \epsilon))\right)
$$

$$
\geq \left\lfloor \frac {n}{2} \right\rfloor \epsilon \Sigma_ {j = 1} ^ {k} \Sigma_ {t = t _ {j - 1} + 1} ^ {t _ {j}} \left(1 - \frac {1}{d} - \right.
$$

$$
\epsilon \sqrt {2 \lfloor n / 2 \rfloor (t _ {j - 1} - \lceil n / 2 \rceil + 1) _ {+}})
$$

$$
\geq \left\lfloor \frac {n}{2} \right\rfloor \epsilon \Sigma_ {j = 1} ^ {k} \Sigma_ {t = t _ {j - 1} + 1} ^ {t _ {j}} \left(\frac {1}{2} - \right.
$$

$$
\epsilon \sqrt {2 \lfloor n / 2 \rfloor (t _ {j - 1} - \lceil n / 2 \rceil + 1) _ {+}}
$$

$$
\geq \left\lfloor \frac {n}{2} \right\rfloor \epsilon t _ {k} \left(\frac {1}{2} - \epsilon \sqrt {2 \lfloor n / 2 \rfloor (t _ {k - 1} - \lceil n / 2 \rceil + 1) _ {+}}\right), \tag {28}
$$

where $a _ { + } ~ \triangleq \operatorname* { m a x } \{ a , 0 \}$ , the first inequality follows from the fact that ℓ is sampled uniformly in [d] and $t _ { j - 1 } ~ +$ $1 , j ~ \leq ~ k$ is the first time learner 1 learners information on $\{ \xi _ { t } ^ { i } \} _ { i > n ^ { \prime } , t _ { j - 2 } < t \leq t _ { j - 1 } }$ , the equality follows from Eq. (27), the second inequality follows from the definition of the total variation, the third inequality follows from the fact that in the claw-shaped network in Fig. 3, no more than $\lfloor n / 2 \rfloor ( t _ { j - 1 } - \lceil n / 2 \rceil + 1 )$ + loss functions from learners $n ^ { \prime } + 1$ to n can be revealed to learner 1 at time $t \in [ t _ { j - 1 } + 1 , t _ { j } ]$ , the fourth inequality follows from Lemma 9, and the fifth inequality follows from $d \geq 2$ .

Denote $\begin{array} { r } { { \epsilon _ { k } } \triangleq \frac { 1 } { 4 \sqrt { 2 \lfloor { n } / { 2 } \rfloor ( { t _ { k - 1 } } - \lceil { n } / { 2 } \rceil + 1 ) } \vee 4 } } \end{array}$ where $a \vee b \ \triangleq$ $\operatorname* { m a x } \{ a , b \}$ . Taking $\epsilon \in \{ \epsilon _ { k } \} _ { k \in [ m + 1 ] }$ that maximizes the last expression of Eq. (28), we obtain that for all $k \in [ m + 1 ]$ :

$$
\mathbb {E} [ \bar {\mathcal {R}} _ {1} (T) ] \geq \frac {\lfloor n / 2 \rfloor t _ {k}}{4 \sqrt {2 \lfloor n / 2 \rfloor (t _ {k - 1} - \lceil n / 2 \rceil + 1)} \vee 4}. \tag {29}
$$

If $T  \leq \lceil n / 2 \rceil$ , by our constructed claw-shaped network, learner 1 cannot learn any feedback information of learners $i > \lceil n / 2 \rceil$ at time T . Thus, it holds that $m = 0 , t _ { 0 } = 0$ , and $t _ { 1 } = T$ . Taking k = 1 in Eq. (29), we obtain:

$$
\mathbb {E} [ \bar {\mathcal {R}} _ {1} (T) ] \geq \frac {\lfloor n / 2 \rfloor T}{4} \geq \frac {n T}{1 6}, \tag {30}
$$

where the second inequality follows from $n \geq 2$ in DOCO.

If $T \geq \lceil n / 2 \rceil + 1$ , by the choice of $\{ t _ { k } \} _ { k \in [ m + 1 ] }$ , where $t _ { k } + 1$ is the first time learner 1 receives information from learner $i > \lceil n / 2 \rceil$ sent at time $t _ { k - 1 } < t \leq t _ { k }$ , it holds that $t _ { k } \geq \lceil n / 2 \rceil$ for $k \in [ m + 1 ]$ . By $t _ { 0 } = 0$ and $n \geq 2 .$ , we obtain:

$$
\mathbb {E} \left[ \bar {\mathcal {R}} _ {1} (T) \right] \geq \max \left\{\frac {n t _ {1}}{1 6} \right\} \cup \left\{\frac {\sqrt {n} t _ {k}}{1 6 \sqrt {t _ {k - 1} - n / 2 + 1}} \right\} _ {k = 2} ^ {m + 1}. \tag {31}
$$

By $t _ { 1 } \geq \lceil n / 2 \rceil$ , from Eq. (31), it holds that:

$$
\mathbb {E} [ \bar {\mathcal {R}} _ {1} (T) ] \geq \frac {n}{1 6} \cdot \left\lceil \frac {n}{2} \right\rceil \geq \frac {n ^ {2}}{3 2}. \tag {32}
$$

Denote the last term of Eq. (31) as $h ( m + 1 )$ ). We proceed to prove that:

$$
\begin{array}{l} h (m + 1) \triangleq \max \left\{\frac {n t _ {1}}{1 6} \right\} \cup \left\{\frac {\sqrt {n} t _ {k}}{1 6 \sqrt {t _ {k - 1} - n / 2 + 1}} \right\} _ {k = 2} ^ {m + 1} \\ \geq \frac {1}{1 6} n ^ {\frac {1}{2 - 2 ^ {- m}}} t _ {m + 1} ^ {\frac {1}{2 - 2 ^ {- m}}}, \tag {33} \\ \end{array}
$$

which can be done by induction. Concretely, Eq. (33) holds for $m = 0$ . Assume that Eq. (33) holds for $h ( m )$ where $m \geq 1$ . Then for $h ( m + 1 )$ , it holds that:

$$
\begin{array}{l} h (m + 1) = \max \{h (m), \frac {\sqrt {n} t _ {m + 1}}{1 6 \sqrt {t _ {m} - n / 2 + 1}} \} \\ \geq \max \{\frac {1}{1 6} n ^ {\frac {1}{2 - 2 - m + 1}} t _ {m} ^ {\frac {1}{2 - 2 - m + 1}}, \frac {\sqrt {n} t _ {m + 1}}{1 6 \sqrt {t _ {m} - n / 2 + 1}} \} \\ \geq \frac {1}{1 6} \left(\frac {2 ^ {m} - 1}{2 ^ {m + 1} - 1} n ^ {\frac {1}{2 - 2 ^ {- m + 1}}} (t _ {m} - n / 2 + 1) ^ {\frac {1}{2 - 2 ^ {- m + 1}}} \right. \\ \left. + \frac {2 ^ {m}}{2 ^ {m + 1} - 1} \frac {\sqrt {n} t _ {m + 1}}{\sqrt {t _ {m} - n / 2 + 1}}\right) \\ \geq \frac {1}{1 6} n ^ {\frac {1}{2 - 2 ^ {- m}}} t _ {m + 1} ^ {\frac {1}{2 - 2 ^ {- m}}}, \\ \end{array}
$$

where the second inequality follows from $t _ { m } \ge n / 2 \ge 1$ and the fact that ma $\ u [ a , b ) \geq p a + ( 1 - p ) b$ for $a , b \ge 0$ and $0 \leq p \leq 1$ , and the third inequality follows from the AM-GM inequality. Thus, by $t _ { m + 1 } = T$ , it holds that:

$$
\mathbb {E} [ \bar {\mathcal {R}} _ {1} (T) ] \geq h (m + 1) \geq \frac {1}{1 6} n ^ {\frac {1}{2 - 2 ^ {- m}}} T ^ {\frac {1}{2 - 2 ^ {- m}}}. \tag {34}
$$

Combining Eqs. (30), (32), and (34), we obtain:

$$
\mathbb {E} \left[ \bar {\mathcal {R}} _ {1} (T) \right] \geq \max \left\{\frac {n}{1 6} \min \left\{\frac {n}{2}, T \right\}, \frac {1}{1 6} n ^ {\frac {1}{2 - 2 ^ {- m}}} T ^ {\frac {1}{2 - 2 ^ {- m}}} \right\}. \tag {35}
$$

Lemma 10 then follows by omitting constant factors in the equation above. □

Proof of Theorem 2. Similarly, as in the adversarial setting, Eq. (24) holds in our constructed instance for stochastic DOCO. It follows that:

$$
m \leq \min (T / \lceil n / 2 \rceil - 1, r / \lceil n / 2 \rceil) \leq r / \lceil n / 2 \rceil \leq \frac {2 r}{n}.
$$

Theorem 2 then follows from Lemma 10.

![](images/90d00dd6e8d2cf776ef3b3ea0e5c27392484e90d961245a708de242668f1d271.jpg)

Proof of Corollary 2. For Eq. (5) in Theorem 2, note that:

$$
(n T) ^ {\frac {1}{2 - 2 ^ {- 2 r / n}}} / \sqrt {n T} = (n T) ^ {\frac {2 ^ {- 2 r / n - 1}}{2 - 2 ^ {- 2 r / n}}} = 2 ^ {\frac {\ln {(n T) 2 ^ {- 2 r / n - 1}}}{2 - 2 ^ {- 2 r / n}}}.
$$

In order to ensure that $\bar { \mathcal { R } } _ { 1 } ( T ) = \mathcal { O } ( \sqrt { n T } )$ in Eq. (5) when T  n, we need ln (nT )2−2r/n− $T \gg n$ $\begin{array} { r } { \frac { \ln { ( n T ) } 2 ^ { - 2 r / n - 1 } } { \mathrm { ~ \int ~ } \limits _ { - \infty } - 2 r / n } = \mathcal { O } ( 1 ) . \operatorname { A s } 1 \leq 2 - 2 ^ { - 2 r / n } \leq } \end{array}$ 2−2−2r/n 2 for $r \geq 0$ , we need to ensure that ln $( n T ) 2 ^ { - 2 r / n - 1 } =$ $\mathcal { O } ( 1 )$ . Thus, it follows that $r / n = \Omega ( \ln \ln n T ) = \Omega ( \ln \ln T )$ , where the second equality follows from $T \gg n$ . The result of Corollary 1 then follows.

# APPENDIX F PROOFS IN APPENDIX B-A

This section provides the detailed proofs for Theorem 6 and Corollary 5 in Appendix B-A.

Lemma 11. In i.i.d. stochastic DOCO with linear loss functions constructed in Appendix B-A with $d \ \geq \ 2 ,$ , if the learners communicate in a connected network in a static communication pattern, then, with an appropriate choice of ϵ in the constructed loss, it holds that:

$$
\mathbb {E} [ \bar {\mathcal {R}} _ {1} (T) ] = \Omega \big (\max \{n, n \sqrt {T / r}, \sqrt {n T} \} \big).
$$

Proof. Similarly, as in the proof of Theorem 2, for arbitrary $x _ { t } ^ { 1 } \in \mathcal { C } = \{ x \in \bar { \mathbb { R } } _ { > 0 } ^ { d } | 1 \leq \| \dot { x } \| _ { 1 } \leq 2 \}$ , we sample $\mathbf { x } _ { t } ^ { 1 } \in \{ e _ { j } \} _ { j = 1 } ^ { d }$ such that $\mathrm { P r } [ \mathrm { x } _ { t } ^ { 1 } = \overline { { e } } _ { j } ] \propto x _ { t , j } ^ { 1 } ,$ , where $e _ { j }$ is the j-th basis of $\mathbb { R } ^ { d }$ and $\boldsymbol { x } _ { t , j } ^ { 1 }$ denotes the j-th coordinate of $\boldsymbol { x } _ { t } ^ { 1 }$ . It holds that $\bar { f } ( x _ { t } ^ { 1 } ) =$ $\| x _ { t } ^ { 1 } \| _ { 1 } \cdot \mathbb { E } [ { \bar { f } } ( \mathrm { x } _ { t } ^ { 1 } ) ] \geq \mathbb { E } [ { \bar { f } } ( \mathrm { x } _ { t } ^ { 1 } ) ]$ . By $\begin{array} { r } { x ^ { * } \triangleq \arg \operatorname* { m i n } _ { x \in \mathcal { C } } \bar { f } ( x ) = e _ { \ell } } \end{array}$ if $\xi _ { t } ^ { i } \sim \mathrm { B e r } _ { \ell } ^ { \epsilon }$ for $i \in [ n ]$ , it follows that:

$$
\mathbb {E} [ \bar {\mathcal {R}} _ {1} (T) ] \geq \epsilon n \mathbb {E} _ {\ell} [ \Sigma_ {t = 1} ^ {T} \mathbb {P} _ {\ell , \epsilon} ^ {t - 1} [ x _ {t} ^ {1} \neq e _ {\ell} ] ], \tag {36}
$$

where Pt−1 $\mathbb { P } _ { \ell , \epsilon } ^ { t - 1 }$ ℓ,ϵ is the probability distribution induced by the samples from $\mathbf { B e r } _ { \ell } ^ { \epsilon }$ accessible to learner 1 before time t. In DOCO with communication budget r, before time t, learner 1 can learn information of at most max $\{ r + 1 , n \} ( t - 1 )$ loss functions. Following a similar line of analysis as for Eq. (28), we obtain:

$$
\begin{array}{l} \mathbb {E} [ \bar {\mathcal {R}} _ {1} (T) ] \geq \frac {n \epsilon}{d} \Sigma_ {\ell = 1} ^ {d} \Sigma_ {t = 1} ^ {T} \left(1 - \frac {1}{d} - \right. \\ T V (B e r ^ {\max \{r + 1, n \} (t - 1)} (1 / 2), \\ \left. \left. B e r ^ {\max \{r + 1, n \} (t - 1)} (1 / 2 - \epsilon))\right) _ {+} \right. \\ \geq \frac {n \epsilon}{d} \Sigma_ {\ell = 1} ^ {d} \Sigma_ {t = 1} ^ {T} \left(\frac {1}{2} - \epsilon \sqrt {2 \max \{r + 1 , n \} (t - 1)}\right) _ {+} \\ \geq n \epsilon \cdot \max \left\{\frac {1}{2}, T \left(\frac {1}{2} - \epsilon \sqrt {2 \max \{r + 1 , n \} T}\right) _ {+} \right\}, \tag {37} \\ \end{array}
$$

where the second inequality follows from $ { d ^ { \mathrm { ~ ~ ~ \geq ~ ~ 2 ~ } } }$ and Lemma 9, and the last inequality follows from $\begin{array} { r l r } { \sqrt { 2 \operatorname* { m a x } \{ r + 1 , n \} ( t - 1 ) } \quad } & { { } \le \quad } & { \sqrt { 2 \operatorname* { m a x } \{ r + 1 , n \} T } } \end{array}$ for $\begin{array} { r l r } { t } & { { } \le } & { T . } \end{array}$ . Lemma 11 then follows by choosing ϵ ∈ n 12 , 14√2 max{r+1,n}T o $\begin{array} { r } { \epsilon \in \left\{ \frac { 1 } { 2 } , \frac { 1 } { 4 \sqrt { 2 \operatorname* { m a x } \{ r + 1 , n \} T } } \right\} } \\ { \ r { \mathrm { ~ r ~ - ~ } } \llangle _ { 2 } \pi \ r { \mathrm { ~ \ r ~ { ~ \frac ~ { ~ 1 ~ } ~ { ~ 2 ~ } ~ } ~ } } } \end{array}$ that maximizes the last term in Eq. (37).

Proof of Theorem 6. The proof of Theorem 6 follows directly from Lemma 11. □

Proof of Corollary 5. By Theorem 6, to ensure that $\begin{array} { r l } { \bar { \mathcal { R } } _ { 1 } ( T ) = } & { { } } \end{array}$ $\mathcal { O } ( \sqrt { n T } )$ when $T \gg n$ , we need $r = \Omega ( n )$ . □

# APPENDIX G PROOFS IN SECTION V-A

This section provides the detailed analysis of DB-TDOCO in Section V-A.

Proof of Theorem 3. By Theorem 1 in [30] and Theorem 4.1 in [44], it holds that in OCO with delayed feedback (OCOD), a learner updates:

$$
x _ {t + 1} \leftarrow \Pi_ {\mathcal {C}} \left(x _ {t - v} - \eta \nabla f _ {t - v} (x _ {t - v})\right), \text {   for   } t \in [ T ],
$$

where $f _ { t }$ denotes the loss function at time $t , v > 0$ denotes the length of delay in OCOD, and η is the stepsize. By choosing $\eta = \Theta ( \sqrt { \frac { v } { T } } )$ , the learner achieves the regret bound:

$$
\mathcal {R} (T) = \Sigma_ {t = 1} ^ {T} f _ {t} (x _ {t}) - \min _ {x \in \mathcal {C}} \Sigma_ {t = 1} ^ {T} f _ {t} (x) = \mathcal {O} (\sqrt {\nu T}),
$$

if $f _ { t } , t \in [ T ]$ is convex and L-Lipschitz, cf. Definitions 1 and 2. In Alg. 1, we use OCOD with delay $\nu = 2$ to update models based on loss functions $\begin{array} { r } { \hat { f } _ { k } = \frac { 1 } { n \overline { { \tau } } } \dot { \Sigma } _ { s \in I _ { k } } f _ { s } } \end{array}$ for $k \in [ 2 m + 2 ]$ Since each $\hat { f } _ { k }$ is L-Lipschitz, it holds that:

$$
\Sigma_ {k = 1} ^ {2 m + 2} \hat {f} _ {k} (\hat {x} _ {k}) - \min _ {x \in \mathcal {C}} \Sigma_ {k = 1} ^ {2 m + 2} \hat {f} _ {k} (x) = \mathcal {O} (\sqrt {m}).
$$

It follows that for $i \in [ n ]$ ,

$$
\begin{array}{l} \mathcal {R} _ {i} (T) = n \mathcal {I} \cdot \left[ \Sigma_ {k = 1} ^ {2 m + 2} \hat {f} _ {k} (\hat {x} _ {k}) - \min _ {x \in \mathcal {C}} \Sigma_ {k = 1} ^ {2 m + 2} \hat {f} _ {k} (x) \right] \\ = \mathcal {O} (n \mathcal {I} \sqrt {m}), \\ \end{array}
$$

where the first equality follows from Eq. (1) and the definition of $\hat { f } _ { k }$ for $k \in [ 2 m + 2 ]$ . In DB-TDOCO, the learners perform m broadcast and convergecast operations in the BFS tree, and the communication cost for each run of broadcast (convergecast) is ${ \mathcal { O } } ( n )$ . Thus, the communication cost of DB-TDOCO is $\mathcal { O } ( m n )$ . □

Proof of Corollary 3. By choosing $m = \lfloor T / ( 2 n ) \rfloor - 1$ and $t _ { k } = 2 n \cdot k$ for $k \in [ m ]$ , it holds that:

$$
\mathcal {I} \leq \max _ {k \in [ m + 1 ]} \left\{t _ {k} - t _ {k - 1} \right\} = \mathcal {O} (n).
$$

It follows that DB-TDOCO, in this case, features an $\mathcal { O } ( n ^ { 3 / 2 } \sqrt { T } )$ regret bound with the communication cost being $\mathcal { O } ( T )$ .

Proof of Corollary 4. By choosing $m = \lfloor T / ( 3 \mu ) \rfloor - 1$ and $t _ { k } = 3 \mu \cdot k$ for $k \in [ m ]$ , it holds that:

$$
\mathcal {I} \leq \max _ {k \in [ m + 1 ]} \left\{t _ {k} - t _ {k - 1} \right\} = \mathcal {O} (\mu) = \mathcal {O} (D),
$$

where the last equality holds by the fact that the height of a BFS-tree $\mu$ scales as $\Theta ( D )$ . It follows that DB-TDOCO, in this case, features an $\dot { \mathcal { O } } ( \bar { n } \sqrt { D T } )$ regret bound with the communication cost being $\mathcal { O } ( n T / D )$ . □

# APPENDIX H PROOFS IN SECTION V-B

This section serves to provide detailed analyses of Theorem 4 and 5. In Appendix H-A, we provide the risk analysis for cutting-plane and AGD algorithms in batch convex optimization. We then analyze the risk of T-DBCO with cutting-plane and AGD in Appendix H-B. Finally, we present the proofs for Theorems 4 and 5 in Appendix H-C based on the risk analysis in Appendix H-B.

# A. Risk Analysis for cutting-plane and AGD in Batch Convex Optimization

In this section, we present the risk analysis of cutting-plane and AGD algorithms in batch convex optimization. Let ¯f(·) be the objective function that we want to minimize. We denote the risk of model $x \in { \mathcal { C } }$ as

$$
\operatorname{Risk} (x) \triangleq \bar {f} (x) - \min _ {x ^ {*} \in \mathcal {C}} \bar {f} (x ^ {*}),
$$

where  is the feasible region. The upper bounds for the risk of cutting-plane and AGD are established in Lemmas 13 and 14, respectively.

Our risk analysis for cutting-plane in batch optimization relies on the findings presented in Lemma 3.1 of [35]. This lemma offers insights into the risk associated with cuttingplane, particularly in scenarios where the deviations of the oracles for the loss values and gradients are proportional to the objective risk, and the feasible region C includes an $\ell _ { \infty } -$ ball near the optimal model of the loss function ${ \bar { f } } .$ In our analysis, we extend the principles of Lemma 3.1 from [35] to accommodate loss functions that satisfy the conditions outlined in Definitions 1 and 4.

Lemma 12 (Lemma 3.1 in [35]). Let ¯f(x) satisfy Definitions 1 and 4. $I f \left| \hat { f } _ { k } ( x _ { k } ) - \bar { f } ( x _ { k } ) \right| \le \epsilon a n d \left\| \nabla \hat { f } _ { k } ( x _ { k } ) - \nabla \bar { f } ( x _ { k } ) \right\| \le$ ϵ2√d∥C∥ for k ∈ [ν], and the number of iterations ν = $\frac { \epsilon } { 2 \sqrt { d } \| \boldsymbol { C } \| }$ $k ~ \in ~ [ \nu ]$ $\nu =$ $\Theta \left( \ddot { d } \ln \left( \frac { d M \| \mathcal { C } \| } { \epsilon } \right) \right)$ , then the model x¯ returned by the cuttingplane algorithm in Alg. 3 satisfies

$$
\operatorname{Risk} (\bar {x}) = \bar {f} (\bar {x}) - \min _ {x ^ {*} \in \mathcal {C}} \bar {f} (x ^ {*}) \leq \Theta (1) \cdot \epsilon ,
$$

where $\begin{array} { r } { \| \mathcal C \| \triangleq \operatorname* { m a x } _ { x , y \in \mathcal C } \| x - y \| . } \end{array}$ .

Proof. Denote the optimal model $x ^ { * } \triangleq$ arg mi $1 _ { x \in { \mathcal { C } } } { \bar { f } } ( x )$ . For any $0 < \epsilon < 2 M$ where M is as defined in Definition 4, consider the set:

$$
\mathcal {C} ^ {\epsilon / (2 M)} = \{(1 - \epsilon / (2 M)) x ^ {*} + (\epsilon / (2 M)) x \mid x \in \mathcal {C} \},
$$

which is a stretching of C centered at $x ^ { * }$ . By the assumption that C is a compact convex set, it holds that $\stackrel { \cdot } { \mathcal { C } } ^ { \epsilon / ( 2 M ) } \subset \dot { \mathcal { C } }$ . By the assumption that $\mathcal { C }$ contains an $\ell _ { \infty }$ -ball of radius $\Omega ( p o l y ( \textstyle { \frac { 1 } { d } } ) )$ ) and the fact that $\mathcal { C } ^ { \epsilon / ( 2 M ) }$ is a stretching of , it follows that $\mathcal { C } ^ { \epsilon / ( 2 M ) }$ contains an $\ell _ { \infty }$ -ball of radius $\begin{array} { r } { \Omega \big ( \frac { \epsilon } { M } \cdot p o l y ( \frac { 1 } { d } ) \big ) } \end{array}$ .

By the convexity condition (cf. Definition 1), it holds that for $0 \leq \alpha \leq 1$ and $x \in { \mathcal { C } } .$ :

$$
(1 - \alpha) \bar {f} (x ^ {*}) + \alpha \bar {f} (x) \geq \bar {f} ((1 - \alpha) x ^ {*} + \alpha x).
$$

Rearranging the equation above, we obtain:

$$
\bar {f} ((1 - \alpha) x ^ {*} + \alpha x) - \bar {f} (x ^ {*}) \leq \alpha (\bar {f} (x) - \bar {f} (x ^ {*})).
$$

By Definition 4, taking $\alpha = \epsilon / ( 2 M )$ yields that:

$$
\bar {f} ((1 - \epsilon / (2 M)) x ^ {*} + \epsilon / (2 M) x) - \bar {f} (x ^ {*}) \leq \epsilon .
$$

It follows that the set $\{ x \in \mathcal { C } : \bar { f } ( x ) - \bar { f } ( x ^ { * } ) \leq \epsilon \}$ contains the set $\mathcal { C } ^ { \epsilon / ( 2 M ) }$ . By the analysis in the last paragraph, the set $\{ x \ \in \ { \mathcal { C } } \ : \ { \bar { f } } ( x ) - { \bar { f } } ( x ^ { * } ) \ \leq \ \epsilon \}$ contains an $\ell _ { \infty } { - } \mathsf { b a l l }$ of radius $\Omega \big ( \frac { \epsilon } { M } \mathbf { p o l y } \big ( \frac { 1 } { d } \big ) \big )$ . By Lemma 3.1 in [35], it holds that $\mathrm { R i s k } ( \bar { x } ) \leq \ddot { 4 } \epsilon { \mathrm { ~ i f ~ } }$

$$
\nu = \Theta \left(d \ln \left(\frac {M \| \mathcal {C} \|}{\epsilon \cdot \operatorname{poly} (1 / d)}\right)\right) = \Theta \left(d \ln \left(\frac {d M \| \mathcal {C} \|}{\epsilon}\right)\right).
$$

Lemma 12 then follows.

![](images/c6c4f93b959e102abcd284c3a25e271512ab90201fb4da21f6e0ccd8914f354b.jpg)

Lemma 13. Let ${ \bar { f } } ( x )$ satisfy Definitions 1 and 4, $\mathbb { E } \left\| \nabla \hat { f } _ { k } ( x _ { k } ) - \nabla \bar { f } ( x _ { k } ) \right\| ^ { 2 } \leq \sigma _ { g } ^ { 2 } ,$ , and E $\left\| \hat { f } _ { k } ( x _ { k } ) - \bar { f } ( x _ { k } ) \right\| ^ { 2 } \leq$ $\sigma _ { v } ^ { 2 ^ { \prime } } \mathrm { ~ } f o r \mathrm { ~  ~ \cal ~ k ~ } \in \mathrm { ~  ~ \Gamma ~ } [ \nu ] .$ . If the number of iterations $\nu \quad =$ Θ d ln  dM∥C∥ϵ  $\begin{array} { r } { \Theta \left( d \ln { \left( \frac { d M \| \mathcal { C } \| } { \epsilon } \right) } \right) } \end{array}$ for some constant $\epsilon > 0 ,$ , the model x¯ returned by the cutting-plane algorithm in Alg. 3 satisfies

$$
\mathbb {E} [ R i s k (\bar {x}) ] = \mathcal {O} \left(\epsilon + \frac {d ^ {2} \sigma_ {g} ^ {2} \| \mathcal {C} \| ^ {2} + d \sigma_ {v} ^ {2}}{\epsilon} \ln \left(\frac {d M \| \mathcal {C} \|}{\epsilon}\right)\right),
$$

where $\| \mathcal { C } \| ~ \triangleq ~ \operatorname* { m a x } _ { x , y \in \mathcal { C } } \| x - y \|$ and $R i s k ( x ) \ \triangleq \ \bar { f } ( x ) \ -$ $\mathrm { m i n } _ { x ^ { * } \in { \mathcal { C } } } { \bar { f } } ( x ^ { * } )$ .

Proof. By Markov inequality, it holds that for any $y > 0$

$$
\mathbb {P} (\left\| \nabla \hat {f} _ {k} (x _ {k}) - \nabla \bar {f} (x _ {k}) \right\| \leq y) \geq 1 - \frac {\sigma_ {g} ^ {2}}{y ^ {2}},
$$

and

$$
\mathbb {P} (\left\| \hat {f} _ {k} (x _ {k}) - \bar {f} (x _ {k}) \right\| \leq y) \geq 1 - \frac {\sigma_ {v} ^ {2}}{y ^ {2}}.
$$

It follows that:

$$
\mathbb {P} \left(\left\{\| \nabla \hat {f} _ {k} \left(x _ {k}\right) - \nabla \bar {f} \left(x _ {k}\right) \| \leq \epsilon_ {g}, \| \hat {f} _ {k} \left(x _ {k}\right) - \bar {f} \left(x _ {k}\right) \| \leq \epsilon_ {v} \right\} _ {k \in [ \nu ]}\right)
$$

$$
\geq 1 - \nu \left(\frac {\sigma_ {g} ^ {2}}{\epsilon_ {g} ^ {2}} + \frac {\sigma_ {v} ^ {2}}{\epsilon_ {v} ^ {2}}\right).
$$

Taking ϵv = ϵ and ϵg = ϵ2√d∥C∥ $\epsilon _ { v } = \epsilon$ $\begin{array} { r } { \epsilon _ { g } = \frac { \epsilon } { 2 \sqrt { d } \| \mathcal { C } \| } } \end{array}$ in the inequality above, we

obtain:

$$
\begin{array}{l} \mathbb {P} \left(\left\{\| \nabla \hat {f} _ {k} \left(x _ {k}\right) - \nabla \bar {f} \left(x _ {k}\right) \| \leq \frac {\epsilon}{2 \sqrt {d} \| \mathcal {C} \|}, \| \hat {f} _ {k} \left(x _ {k}\right) - \bar {f} \left(x _ {k}\right) \| \leq \epsilon \right\} _ {k \in [ \nu ]}\right) \\ \geq 1 - \nu \left(\frac {4 d \sigma_ {g} ^ {2} \| \mathcal {C} \| ^ {2} + \sigma_ {v} ^ {2}}{\epsilon^ {2}}\right). \\ \end{array}
$$

By Lemma 12 and $\begin{array} { r } { \nu = \Theta \left( d \ln \left( \frac { d M \| \mathcal { C } \| } { \epsilon } \right) \right) } \end{array}$ , it holds that:

Risk $( \bar { x } ) \leq \Theta ( 1 ) \cdot \epsilon w . p$ . max $\begin{array} { r } { \left\{ 1 - \nu \left( \frac { 4 d \sigma _ { g } ^ { 2 } \| \mathcal { C } \| ^ { 2 } + \sigma _ { v } ^ { 2 } } { \epsilon ^ { 2 } } \right) , 0 \right\} } \end{array}$

By the fact that $\begin{array} { r } { \mathrm { R i s k } ( x ) = \bar { f } ( x ) - \operatorname* { m i n } _ { x ^ { * } \in \mathcal { C } } \bar { f } ( x ^ { * } ) \geq 0 } \end{array}$ for any $x \in { \mathcal { C } } ,$ it follows that:

$$
\begin{array}{l} \mathbb {E} \left[ \operatorname{Risk} (\bar {x}) \right] = \int_ {0} ^ {+ \infty} \mathbb {P} \left(\operatorname{Risk} (\bar {x}) \geq y\right) d y \\ \leq \Theta (1) \cdot \epsilon + \int_ {\Theta (1) \cdot \epsilon} ^ {+ \infty} \nu \left(\frac {4 d \sigma_ {g} ^ {2} \| \mathcal {C} \| ^ {2} + \sigma_ {v} ^ {2}}{y ^ {2}}\right) d y \\ = \Theta (1) \cdot \epsilon + \Theta (1) \cdot \nu \left(\frac {4 d \sigma_ {g} ^ {2} \| \mathcal {C} \| ^ {2} + \sigma_ {v} ^ {2}}{\epsilon}\right) \\ = \mathcal {O} \left(\epsilon + \frac {d ^ {2} \sigma_ {g} ^ {2} \| \mathcal {C} \| ^ {2} + d \sigma_ {v} ^ {2}}{\epsilon} \ln \left(\frac {d M \| \mathcal {C} \|}{\epsilon}\right)\right), \tag {39} \\ \end{array}
$$

where the inequality follows from Eq. (38) and $\mathbb { P } \left( \mathrm { R i s k } ( \bar { x } ) \geq y \right) ~ \leq ~ 1$ $y ~ \leq ~ \mathcal { O } ( 1 ) ~ \cdot ~ \epsilon ,$ and the last. $\begin{array} { r } { \nu = \Theta \left( d \ln \left( \frac { d M \| \dot { \mathcal { C } } \| } { \epsilon } \right) \right) } \end{array}$

The AGD algorithm used in this paper (cf. Alg. 4) is a constrained version of the unconstrained algorithm in [41]. The analysis of the risk of Alg. 4 follows a similar line of analysis as for Theorem 1 in [41], with the main difference being that yk and $z _ { k }$ in Alg. 4 for $k \in [ \nu + 1 ]$ are projected into the compact convex set C in our analysis.

Lemma 14 (Theorem 1 in [41]). Let ${ \bar { f } } ( x )$ satisfy Definitions 1 and 3. If the estimated gradient $\nabla \widehat { f } _ { k } ( x _ { k } )$ satisfies $\begin{array} { r } { \mathbb { E } \left\| \nabla \hat { f } _ { k } ( x _ { k } ) - \nabla \bar { f } ( x _ { k } ) \right\| ^ { 2 } \leq \sigma _ { g } ^ { 2 } \ f o r \ k \ \in \ [ \nu ] , } \end{array}$ , the model x¯ returned by AGD (cf. Alg. 4) satisfies

$$
\mathbb {E} [ R i s k (\bar {x}) ] = \mathcal {O} \left(L _ {G} \| \mathcal {C} \| ^ {2} \frac {1}{\nu^ {2}} + \| \mathcal {C} \| \frac {\sigma_ {g}}{\sqrt {\nu}}\right),
$$

where $\begin{array} { r l } { \| \mathcal { C } \| \triangleq \operatorname* { m a x } _ { x , y \in \mathcal { C } } \| x - y \| , x ^ { * } \triangleq } \end{array}$ arg $\operatorname* { m i n } _ { x \in { \mathcal { C } } } { \bar { f } } ( x )$ , and $R i s k ( x ) \triangleq { \bar { f } } ( x ) - { \bar { f } } ( x ^ { * } )$ .

Proof. Denote $\Delta _ { k } \equiv \nabla \hat { f } _ { k } ( x _ { k } ) - \nabla \bar { f } ( x _ { k } )$ and $\delta _ { k } \equiv L _ { k } ( x _ { k } -$ $y _ { k + 1 } )$ . For $k \in [ \nu ]$ and $x \in { \mathcal { C } }$ , by Definitions 1 and 3, it holds that:

$$
\left\{ \begin{array}{l} \bar {f} \left(y _ {k + 1}\right) \leq \bar {f} \left(x _ {k}\right) + \left\langle \nabla \bar {f} \left(x _ {k}\right), y _ {k + 1} - x _ {k} \right\rangle + \\ \frac {L _ {G}}{2} \| y _ {k + 1} - x _ {k} \| ^ {2} \\ = \bar {f} \left(x _ {k}\right) + \left\langle \nabla \bar {f} \left(x _ {k}\right), y _ {k + 1} - x _ {k} \right\rangle + \frac {L _ {G} \| \delta_ {k} \| ^ {2}}{2 L _ {k} ^ {2}} \\ \bar {f} (x) \geq \bar {f} \left(x _ {k}\right) + \left\langle \nabla \bar {f} \left(x _ {k}\right), x - x _ {k} \right\rangle . \end{array} \right. \tag {40}
$$

By Eq. (40), it holds that:

$$
\begin{array}{l} \bar {f} (y _ {k + 1}) \leq \bar {f} (x) + \left\langle \nabla \bar {f} (x _ {k}), y _ {k + 1} - x \right\rangle + \frac {L _ {G} \| \delta_ {k} \| ^ {2}}{2 L _ {k} ^ {2}} \\ = \bar {f} (x) - \left\langle \Delta_ {k}, y _ {k + 1} - x \right\rangle + \frac {L _ {G} \| \delta_ {k} \| ^ {2}}{2 L _ {k} ^ {2}} + \left\langle \nabla \hat {f} _ {k} \left(x _ {k}\right), y _ {k + 1} - x \right\rangle , \tag {41} \\ \end{array}
$$

where the equality follows from $\Delta _ { k } = \nabla \hat { f } _ { k } ( x _ { k } ) - \nabla \bar { f } ( x _ { k } )$ . By Lemma 15 in [48], it holds that $\langle \Pi _ { \cal C } ( \tilde { x } ) - \tilde { x } , \Pi _ { \cal C } ( \tilde { x } ) -$ $x \rangle \leq 0$ for arbitrary $\tilde { \boldsymbol { x } } \in \mathbb { R } ^ { d }$ and $x \in { \mathcal { C } }$ . Thus, by $y _ { k + 1 } =$ $\begin{array} { r } { \Pi _ { \mathcal { C } } \left( x _ { k } - \frac { 1 } { L _ { k } } \nabla \hat { f } _ { k } ( x _ { k } ) \right) } \end{array}$ , we obtain:

$$
\left\langle y _ {k + 1} - \left(x _ {k} - \frac {1}{L _ {k}} \nabla \hat {f} _ {k} (x _ {k})\right), y _ {k + 1} - x \right\rangle \leq 0. \tag {42}
$$

It follows that:

$$
\left\langle \nabla \hat {f} _ {k} (x _ {k}), y _ {k + 1} - x \right\rangle \leq L _ {k} \left\langle x _ {k} - y _ {k + 1}, y _ {k + 1} - x \right\rangle
$$

$$
\leq - \frac {\left\| \delta_ {k} \right\| ^ {2}}{L _ {k}} + \left\langle \delta_ {k}, x _ {k} - x \right\rangle .
$$

Plugging the inequality above into Eq. (41), it holds that:

$$
\begin{array}{l} \bar {f} (y _ {k + 1}) \leq \bar {f} (x) - \left\langle \Delta_ {k}, y _ {k + 1} - x \right\rangle + \frac {\left(L _ {G} - 2 L _ {k}\right) \| \delta_ {k} \| ^ {2}}{2 L _ {k} ^ {2}} + \\ \left\langle \delta_ {k}, x _ {k} - x \right\rangle . \tag {43} \\ \end{array}
$$

By choosing $x = y _ { k }$ in Eq. (43), it follows that:

$$
\begin{array}{l} \bar {f} (y _ {k + 1}) \leq \bar {f} (y _ {k}) - \left\langle \Delta_ {k}, y _ {k + 1} - y _ {k} \right\rangle + \frac {\left(L _ {G} - 2 L _ {k}\right) \| \delta_ {k} \| ^ {2}}{2 L _ {k} ^ {2}} + \\ \left\langle \delta_ {k}, x _ {k} - y _ {k} \right\rangle . \tag {44} \\ \end{array}
$$

Define it holds $\begin{array} { r } { V _ { k } ( x ) \stackrel { \Delta } { = } \langle \delta _ { k } , x - x _ { k } \rangle + \frac { L _ { k } \alpha _ { k } } { 2 } \left. x - z _ { k } \right. ^ { 2 } } \end{array}$ Byis $z _ { k + 1 } = \arg \operatorname* { m i n } _ { x \in { \mathcal { C } } } V _ { k } ( x )$ $V _ { k } ( x )$ $L _ { k } \alpha _ { k ^ { - } }$ strongly convex. It follows that for any $x \in { \mathcal { C } }$ ,

$$
\begin{array}{l} V _ {k} (z _ {k + 1}) \leq V _ {k} (x) - \frac {L _ {k} \alpha_ {k}}{2} \| z _ {k + 1} - x \| ^ {2} \\ = \left\langle \delta_ {k}, x - x _ {k} \right\rangle + \frac {L _ {k} \alpha_ {k}}{2} \left\| x - z _ {k} \right\| ^ {2} - \frac {L _ {k} \alpha_ {k}}{2} \left\| z _ {k + 1} - x \right\| ^ {2} \\ \leq \bar {f} (x) - \bar {f} (y _ {k + 1}) - \left\langle \Delta_ {k}, y _ {k + 1} - x \right\rangle + \frac {\left(L _ {G} - 2 L _ {k}\right) \| \delta_ {k} \| ^ {2}}{2 L _ {k} ^ {2}} \\ + \frac {L _ {k} \alpha_ {k}}{2} \left\| x - z _ {k} \right\| ^ {2} - \frac {L _ {k} \alpha_ {k}}{2} \left\| z _ {k + 1} - x \right\| ^ {2}, \\ \end{array}
$$

where the last inequality follows from Eq. (41). By the fact that

$$
V _ {k} (z _ {k + 1}) = \left\langle \delta_ {k}, z _ {k + 1} - x _ {k} \right\rangle + \frac {L _ {k} \alpha_ {k}}{2} \left\| z _ {k + 1} - z _ {k} \right\| ^ {2},
$$

it follows that:

$$
\begin{array}{l} \bar {f} (y _ {k + 1}) - \bar {f} (x) \leq - \left\langle \Delta_ {k}, y _ {k + 1} - x \right\rangle + \frac {\left(L _ {G} - 2 L _ {k}\right) \| \delta_ {k} \| ^ {2}}{2 L _ {k} ^ {2}} + \\ \frac {L _ {k} \alpha_ {k}}{2} \left\| x - z _ {k} \right\| ^ {2} - \frac {L _ {k} \alpha_ {k}}{2} \left\| z _ {k + 1} - x \right\| ^ {2} - \\ \left\langle \delta_ {k}, z _ {k + 1} - x _ {k} \right\rangle - \frac {L _ {k} \alpha_ {k}}{2} \left\| z _ {k + 1} - z _ {k} \right\| ^ {2}. \tag {45} \\ \end{array}
$$

Multiplying Eq. (44) by $1 - \alpha _ { k }$ and Eq. (45) by $\alpha _ { k } .$ , and adding the results, we obtain:

$$
\begin{array}{l} \bar {f} (y _ {k + 1}) - \bar {f} (x) \leq (1 - \alpha_ {k}) [ \bar {f} (y _ {k}) - \bar {f} (x) ] - \\ \frac {\left(2 L _ {k} - L _ {G}\right) \left\| \delta_ {k} \right\| ^ {2}}{2 L _ {k} ^ {2}} - \frac {L _ {k} \alpha_ {k}}{2} \left\| z _ {k + 1} - z _ {k} \right\| ^ {2} + A + B + C, \tag {46} \\ \end{array}
$$

where $A = \langle \delta _ { k } , \alpha _ { k } ( x _ { k } - z _ { k + 1 } ) + ( 1 - \alpha _ { k } ) ( x _ { k } - y _ { k } ) \rangle , B =$ $\alpha _ { k } \left. \Delta _ { k } , x - y _ { k + 1 } \right. + \left( 1 - \alpha _ { k } \right) \left. \Delta _ { k } , y _ { k } - y _ { k + 1 } \right.$ , and ${ \cal { C } } = $ $\begin{array} { r } { \frac { L _ { k } \alpha _ { k } ^ { 2 } } { 2 } \left\| x - z _ { k } \right\| ^ { 2 } - \frac { L _ { k } \alpha _ { k } ^ { 2 } } { 2 } \left\| x - z _ { k + 1 } \right\| ^ { 2 } } \end{array}$ . Following the same line of analysis as for Proposition 1 in [41] using Eq. (46) via basic arithmetic computations, we obtain:

$$
\begin{array}{l} \mathbb {E} [ \bar {f} (y _ {k + 1}) ] - \bar {f} (x) \leq (1 - \alpha_ {k}) [ \mathbb {E} [ \bar {f} (y _ {k}) ] - \bar {f} (x) ] + \\ \frac {L _ {k} \alpha_ {k} ^ {2}}{2} \mathbb {E} \| x - z _ {k} \| ^ {2} - \frac {L _ {k} \alpha_ {k} ^ {2}}{2} \mathbb {E} \| x - z _ {k + 1} \| ^ {2} + \frac {\sigma_ {g} ^ {2}}{2 (L _ {k} - L _ {G})}. \tag {47} \\ \end{array}
$$

By Alg. 4, it holds that $\bar { x } = y _ { \nu + 1 } , x _ { 1 } = y _ { 1 }$ , and $\left( \alpha _ { k } , L _ { k } \right) =$ $\begin{array} { r } { ( \frac { 2 } { k + 1 } , b k ^ { 3 / 2 } + L _ { G } ) } \end{array}$ for $k \in [ \nu ]$ where $\begin{array} { r } { b = \frac { \sqrt { 5 } \sigma _ { g } } { 3 \| C \| } } \end{array}$ . It follows that:

$$
\begin{array}{l} \mathbb {E} [ \bar {f} (\bar {x}) ] - \bar {f} (x) \leq (1 - \alpha_ {\nu}) [ \mathbb {E} [ \bar {f} (y _ {\nu}) ] - \bar {f} (x) ] + \\ \frac {L _ {\nu} \alpha_ {\nu} ^ {2}}{2} \mathbb {E} \| x - z _ {\nu} \| ^ {2} - \frac {L _ {\nu} \alpha_ {\nu} ^ {2}}{2} \mathbb {E} \| x - z _ {\nu + 1} \| ^ {2} + \frac {\sigma_ {g} ^ {2}}{2 (L _ {\nu} - L _ {G})} \\ \leq 2 \Sigma_ {k = 1} ^ {\nu} \frac {k ^ {5 / 2} b + k L _ {G}}{(\nu + 1) \nu (k + 1)} \left[ \mathbb {E} \| x - z _ {k} \| ^ {2} - \right. \\ \left. \mathbb {E} \| x - z _ {k + 1} \| ^ {2} \right] + \frac {\sigma_ {g} ^ {2}}{2 b} \Sigma_ {k = 1} ^ {\nu} \frac {k + 1}{(\nu + 1) \nu \sqrt {k}}, \tag {48} \\ \end{array}
$$

where the second inequality follows by applying Eq. (47) recursively for $k \in [ \nu ]$ . Let $\begin{array} { r } { \dot { a } _ { k } \triangleq \frac { k ^ { 5 / 2 } b + \bar { k } L _ { G } } { ( \nu + 1 ) \nu ( k + 1 ) } } \end{array}$ for $k \in [ \nu ]$ . Via arithmetic computations, it holds that:

$$
a _ {1} <   a _ {2} <   \dots <   a _ {\nu} <   \frac {b}{\sqrt {\nu}} + \frac {L _ {G}}{\nu^ {2}}.
$$

By Eq. (48), it follows that:

$$
\mathbb {E} [ \bar {f} (\bar {x}) ] - \bar {f} (x) \leq 2 a _ {1} \big [ \mathbb {E} \| x - z _ {1} \| ^ {2} - \mathbb {E} \| x - z _ {\nu + 1} \| ^ {2} \big ] +
$$

$$
2 \Sigma_ {k = 2} ^ {\nu} (a _ {k} - a _ {k - 1}) \left[ \mathbb {E} \| x - z _ {k} \| ^ {2} - \mathbb {E} \| x - z _ {\nu + 1} \| ^ {2} \right] +
$$

$$
\frac {\sigma_ {g} ^ {2}}{2 b} \Sigma_ {k = 1} ^ {\nu} \frac {k + 1}{(\nu + 1) \nu \sqrt {k}}
$$

$$
\leq 2 a _ {\nu} \| \mathcal {C} \| ^ {2} + \frac {\sigma_ {g} ^ {2}}{2 b} \Sigma_ {k = 1} ^ {\nu} \frac {k + 1}{(\nu + 1) \nu \sqrt {k}}
$$

$$
\leq (\frac {2 b}{\sqrt {\nu}} + \frac {2 L _ {G}}{\nu^ {2}}) \| \mathcal {C} \| ^ {2} + \frac {5 \sigma_ {g} ^ {2}}{3 b \sqrt {\nu}}
$$

$$
= \mathcal {O} \Big (L _ {G} \left\| \mathcal {C} \right\| ^ {2} \frac {1}{\nu^ {2}} + \left\| \mathcal {C} \right\| \frac {\sigma_ {g}}{\sqrt {\nu}} \Big),
$$

where the second inequality follows from $\| x - y \| \leq C$ for $x , y \in { \mathcal { C } }$ , the third inequality follows from arithmetic computations, and the last equality follows from $\begin{array} { r } { b = \frac { \sqrt { 5 } \sigma _ { g } } { 3 \| \mathcal { C } \| } } \end{array}$ .

# B. Risk Analysis for T-DBCO with cutting-plane and AGD

In this section, we analyze the risk bound of the model $x _ { k , \nu _ { k } + 1 } , k ~ \in ~ [ m ]$ returned by T-DBCO by choosing the ingredient update rule A in Alg. 2 as the one specified by cutting-plane (cf. $\mathrm { A l g } . \ 3 )$ or AGD (cf. $\mathrm { A l g } . ~ 4 )$ . In T-DBCO, we denote:

$$
\begin{array}{l} \hat {f} _ {k, \ell} (\cdot) \triangleq \frac {1}{b _ {k} - 2 \mu} \Sigma_ {s = (\ell - 1) b _ {k} + 1} ^ {\ell b _ {k} - 2 \mu} f _ {s} (\cdot) \tag {49} \\ = \frac {1}{b _ {k} - 2 \mu} \Sigma_ {s = (\ell - 1) b _ {k} + 1} ^ {\ell b _ {k} - 2 \mu} \Sigma_ {i = 1} ^ {n} f (\cdot ; \xi_ {s} ^ {i}), \\ \end{array}
$$

where $b _ { k }$ is the batch size and $\ell \in [ \nu _ { k } ]$ . In the ℓ-th iteration, T-DBCO updates $x _ { k , \ell + 1 }$ based on the loss value oracle $\hat { f } _ { k , \ell } ( x _ { k , \ell } )$ and gradient oracle $\nabla \widehat { f } _ { k , \ell } ( x _ { k , \ell } )$ using Alg. 3 or Alg. 4. After $\nu _ { k } = \lfloor t _ { k } / b _ { k } \rfloor$ iterations, T-DBCO returns $x _ { k , \nu _ { k } + 1 }$ .

In Lemma 15, we present the analysis for the risk of the T-DBCO with the cutting-plane method.

Lemma 15. Let $f ( x ; \xi )$ for any $\xi \sim \mathbb { P } _ { i } , i \in [ n ]$ satisfy Definitions 1, 4, and 5. By taking the update rule A as cuttingplane (cf. Alg. 3) and $\begin{array} { r } { \dot { b } _ { k } \ = \ \left\lfloor t _ { k } / \left( C _ { 1 } d \ln \left( \frac { d n } { \epsilon _ { k } } \right) \right) \right\rfloor } \end{array}$ / C1d ln  dnϵ  ）） , where k $\begin{array} { r } { \epsilon _ { k } = d ^ { 3 / 2 } \ln ( n t _ { k } ) \sqrt { \frac { n } { t _ { k } - ( 2 \mu + 1 ) C _ { 1 } d \ln \left( n t _ { k } \right) } } } \end{array}$ and $t _ { k }$ is the learning time for T-DBCO, the model $x _ { k , \nu _ { k } + 1 }$ returned by T-DBCO satisfies

$$
\begin{array}{l} \mathbb {E} [ \text { Risk } (x _ {k, \nu_ {k} + 1}) ] = \\ \mathcal {O} \left(d ^ {3 / 2} \ln (n t _ {k}) \sqrt {\frac {n}{t _ {k} - (2 \mu + 1) C _ {1} d \ln (n t _ {k})}}\right), \tag {50} \\ \end{array}
$$

where $\begin{array} { r } { R i s k ( x ) \triangleq \bar { f } ( x ) - \operatorname* { m i n } _ { x ^ { * } \in \mathcal { C } } \bar { f } ( x ^ { * } ) . } \end{array}$ .

Proof. By Definition 5, it holds that for $x \in { \mathcal { C } }$ and $i \in [ n ]$ ,

$$
\mathbb {E} _ {\xi \sim \mathbb {P} _ {i}} \| \nabla f (x; \xi) - \nabla \bar {f} _ {i} (x) \| ^ {2} \leq \sigma^ {2},
$$

where $\bar { f } _ { i } ( x ) \triangleq \mathbb { E } _ { \xi \sim \mathbb { P } _ { i } } [ f ( x ; \xi ) ]$ . It follows that:

$$
\begin{array}{l} \mathbb {E} \left\| \nabla \hat {f} _ {k, \ell} (x _ {k, \ell}) - \nabla \bar {f} (x _ {k, \ell}) \right\| ^ {2} = \\ \Sigma_ {i = 1} ^ {n} \mathbb {E} \left\| \frac {1}{b _ {k} - 2 \mu} \left(\Sigma_ {s = (\ell - 1) b _ {k} + 1} ^ {\ell b _ {k} - 2 \mu} \nabla f (x _ {k, \ell}; \xi_ {s} ^ {i})\right) - \nabla \bar {f} _ {i} (x _ {k, \ell}) \right\| ^ {2} \\ = \frac {1}{b _ {k} - 2 \mu} \Sigma_ {i = 1} ^ {n} \mathbb {E} _ {\xi \sim \mathbb {P} _ {i}} \left\| \nabla f (x _ {k, \ell}; \xi) - \nabla \bar {f} _ {i} (x _ {k, \ell}) \right\| ^ {2} \\ \leq \frac {n \sigma^ {2}}{b _ {k} - 2 \mu}, \tag {51} \\ \end{array}
$$

where the equalities follow from each $\xi _ { s } ^ { i }$ is i.i.d. sampled from $\mathbb { P } _ { i }$ and $\nabla \bar { f } _ { i } ( x ) = \mathbb { E } _ { \xi \sim \mathbb { P } _ { i } } \left[ \nabla f ( x ; \xi ) \right]$ ]. Similarly, it holds that:

$$
\mathbb {E} \left\| \hat {f} _ {k, \ell} (x _ {k, \ell}) - \bar {f} (x _ {k, \ell}) \right\| ^ {2} \leq \frac {n M ^ {2}}{b _ {k} - 2 \mu}.
$$

Denote $\epsilon _ { k } ^ { \prime } \triangleq M \lVert \boldsymbol { \mathcal { C } } \rVert \epsilon _ { k }$ , where $\| \mathcal { C } \| ~ \triangleq ~ \operatorname* { m a x } _ { x , y \in \mathcal { C } } \| x - y \|$ By choosing $\begin{array} { r l r } { b _ { k } } & { { } = } & { \Big \lfloor t _ { k } / \left( C _ { 1 } d \ln \left( \frac { d n M \| \tilde { c } \| } { \epsilon _ { k } ^ { \prime } } \right) \right) \Big \rfloor \quad = } \end{array}$ $\begin{array} { r } { \bigg \lfloor t _ { k } / \left( C _ { 1 } d \ln \left( \frac { d n } { \epsilon _ { k } } \right) \right) \bigg \rfloor } \end{array}$ , it holds that:

$$
\left\{ \begin{array}{l} \mathbb {E} \left\| \nabla \hat {f} _ {k, \ell} (x _ {k, \ell}) - \nabla \bar {f} (x _ {k, \ell}) \right\| ^ {2} \leq \frac {C _ {1} d n \sigma^ {2} \ln \left(\frac {d n}{\epsilon_ {k}}\right)}{t _ {k} - (2 \mu + 1) C _ {1} \left(d \ln \left(\frac {d n}{\epsilon_ {k}}\right)\right)} \\ \mathbb {E} \left\| \hat {f} _ {k, \ell} (x _ {k, \ell}) - \bar {f} (x _ {k, \ell}) \right\| ^ {2} \leq \frac {C _ {1} d n M ^ {2} \ln \left(\frac {d n}{\epsilon_ {k}}\right)}{t _ {k} - (2 \mu + 1) C _ {1} \left(d \ln \left(\frac {d n}{\epsilon_ {k}}\right)\right)}. \end{array} \right. \tag {52}
$$

By Definition 4, it holds that $| \Sigma _ { i = 1 } ^ { n } f ( x ; \xi _ { t } ^ { i } ) | \le n M$ for any $\xi _ { t } ^ { i } , i \ \in \ [ n ]$ and $x \in \mathcal { C }$ for all $t ~ \in ~ [ t _ { k } ]$ . By Lemma 13 $\sigma _ { g } ^ { 2 }$ $\sigma _ { v } ^ { 2 }$ and , we $\nu _ { k } ~ = ~ \left\lfloor t _ { k } / b _ { k } \right\rfloor ~ =$ $\begin{array} { r } { \Theta \left( d \ln \left( \frac { d n M \| \dot { \mathcal { C } } \| } { \epsilon _ { k } ^ { \prime } } \right) \right) = \Theta \left( d \ln \left( \frac { d n } { \epsilon _ { k } } \right) \right) } \end{array}$

$$
\begin{array}{l} \mathbb {E} [ \operatorname{Risk} (x _ {k, \nu_ {k} + 1}) ] = \\ \mathcal {O} \left(\epsilon_ {k} M \| \mathcal {C} \| + \frac {n (d ^ {3} \sigma^ {2} \| \mathcal {C} \| ^ {2} + d ^ {2} M ^ {2}) \ln^ {2} \left(\frac {d n}{\epsilon_ {k}}\right)}{\epsilon_ {k} M \| \mathcal {C} \| \left(t _ {k} - (2 \mu + 1) C _ {1} d \ln \left(\frac {d n}{\epsilon_ {k}}\right)\right)}\right). \\ \end{array}
$$

$\begin{array} { r l } & { \mathrm { E q . } \qquad ( 5 0 ) \qquad \mathrm { t h e n } \qquad \mathrm { h o l d s } \qquad \mathrm { b y } } \\ & { d ^ { 3 / 2 } \ln ( n t _ { k } ) \sqrt { \frac { n } { t _ { k } - ( 2 \mu + 1 ) C _ { 1 } d \ln ( n t _ { k } ) } } } \end{array}$ taking ϵk d3/2 ln(ntk)q and omitting constant factors in $\sigma , \operatorname { i } \lVert \boldsymbol { c } \rVert$ , and M in the equation above.

Similarly, as in T-DBCO with cutting-pfor T-DBCO with AGD. Thus, we take $\begin{array} { r } { \sigma _ { g } ^ { 2 } = \frac { { \bar { n } } \sigma ^ { 2 } } { b _ { k } - 2 \mu } } \end{array}$ nσ2 ) holdswhen applying AGD (cf. Alg. 4) in T-DBCO updates. Meanwhile, by the fact that $f ( x ; \xi )$ for any $\xi \sim \mathbb { P } _ { i } , i \in [ n ]$ satisfy Definition 3, we take the smooth constant as $n L _ { G }$ when using AGD (cf. Alg. 4) in T-DBCO updates. We establish the bound for the risk of T-DBCO with AGD in Lemmas 16 and 17.

Lemma 16. Let $\bar { f } ( x ) = \Sigma _ { i = 1 } ^ { n } \mathbb { E } _ { \xi \sim \mathbb { P } _ { i } } [ f ( x ; \xi ) ]$ and $f ( x ; \xi )$ for any $\xi \sim \mathbb { P } _ { i } , i \in [ n ]$ satisfy Definitions 1, 3, and 5. By taking the update rule A as AGD (cf. Alg. 4), the model $x _ { k , \nu _ { k } + 1 }$ returned by T-DBCO with AGD with the batch size $b _ { k }$ and the learning time $t _ { k }$ satisfies

$$
\mathbb {E} \left[ \operatorname{Risk} \left(x _ {k, \nu_ {k} + 1}\right) \right] = \mathcal {O} \left(\frac {n b _ {k} {} ^ {2}}{\left(t _ {k} - b _ {k}\right) ^ {2}} + \sqrt {\frac {n b _ {k}}{\left(t _ {k} - b _ {k}\right) \left(b _ {k} - 2 \mu\right)}}\right), \tag {53}
$$

where $\begin{array} { r } { R i s k ( x ) \triangleq \bar { f } ( x ) - \operatorname* { m i n } _ { x ^ { * } \in \mathcal { C } } \bar { f } ( x ^ { * } ) . } \end{array}$

Proof. By the equation that $\nu _ { k } = \lfloor t _ { k } / b _ { k } \rfloor$ in T-DBCO, it holds that:

$$
\nu_ {k} \geq t _ {k} / b _ {k} - 1.
$$

By Lemma 14 and the fact that $\Sigma _ { i = 1 } ^ { n } f ( x ; \xi _ { t } ^ { i } )$ is $n L _ { G }$ -smooth for any $\xi _ { t } ^ { i } , i \in [ n ]$ , it follows that:

$$
\begin{array}{l} \mathbb {E} \left[ \operatorname{Risk} \left(x _ {k, \nu_ {k} + 1}\right) \right] = \\ \mathcal {O} \left(n L _ {G} \| \mathcal {C} \| ^ {2} \frac {b _ {k} {} ^ {2}}{\left(t _ {k} - b _ {k}\right) ^ {2}} + \| \mathcal {C} \| \sigma_ {g} \sqrt {\frac {b _ {k}}{t _ {k} - b _ {k}}}\right), \tag {54} \\ \end{array}
$$

where $\begin{array} { r } { \| \mathcal { C } \| \triangleq \operatorname* { m a x } _ { x , y \in \mathcal { C } } \| x - y \| } \end{array}$ . Similarly, as in T-DBCO with the cutting-plane method, Eq. (51) provides an upper bound for $\sigma _ { g } ^ { 2 }$ in T-DBCO with AGD. Eq. (53) then holds by plugging Eq. (51) into Eq. (54) and omitting constant factors in $\sigma , L _ { G }$ , and ∥C∥. □

Lemma 17. Let $\bar { f } ( \boldsymbol { x } ) = \Sigma _ { i = 1 } ^ { n } \mathbb { E } _ { \boldsymbol { \xi } \sim \mathbb { P } _ { i } } [ f ( \boldsymbol { x } ; \boldsymbol { \xi } ) ] , \ f ( \boldsymbol { x } ; \boldsymbol { \xi } )$ for any $\xi \sim \mathbb { P } _ { i } , i \in [ n ]$ satisfy Definitions 1, 3, and ${ } ^ { 5 , }$ and $t _ { k }$ be the learning time. $\dot { I f } t _ { k } \le 2 \mu + n + n ^ { 5 / 3 }$ , by choosing $b _ { k } = 2 \mu + n ,$ the model $x _ { k , \nu _ { k } + 1 }$ returned by T-DBCO with AGD satisfies

$$
\mathbb {E} [ \text { Risk } (x _ {k, \nu_ {k} + 1}) ] = \mathcal {O} \left(\frac {n ^ {3}}{(t _ {k} - 2 \mu - n) ^ {2}}\right), \tag {55}
$$

where $\begin{array} { r } { R i s k ( x ) \triangleq \bar { f } ( x ) - \operatorname* { m i n } _ { x ^ { * } \in \mathcal { C } } \bar { f } ( x ^ { * } ) . I f t _ { k } \geq 2 \mu + n + n ^ { 5 / 3 } } \end{array}$ , by choosing $\begin{array} { r } { b _ { k } = \operatorname* { m a x } \left\{ 2 \mu + n , \left\lfloor \frac { t _ { k } } { C _ { 2 } n ^ { 1 / 4 } t _ { k } ^ { 1 / 4 } + 1 } \right\rfloor \right\} } \end{array}$ where $C _ { 2 } >$

0, it holds that:

$$
\mathbb {E} [ \text { Risk } (x _ {k, \nu_ {k} + 1}) ] = \mathcal {O} \left(\sqrt {\frac {n}{t _ {k} - 2 \mu - n}}\right). \tag {56}
$$

Proof. If $t _ { k } \le 2 \mu + n + n ^ { 5 / 3 }$ , by $b _ { k } = 2 \mu + n$ and Lemma 16, it holds that:

$$
\mathbb {E} [ \operatorname{Risk} (x _ {k, \nu_ {k} + 1}) ] = \mathcal {O} \left(\frac {n ^ {3}}{(t _ {k} - 2 \mu - n) ^ {2}} + \sqrt {\frac {n}{t _ {k} - 2 \mu - n}}\right),
$$

where the equality follows from $\mu = \mathcal { O } ( n )$ . By the inequality that $t _ { k } - 2 \bar { \mu } - n \stackrel { \cdot } { \leq } n ^ { 5 / 3 }$ , it holds that:

$$
\begin{array}{l} \frac {n ^ {3}}{(t _ {k} - 2 \mu - n) ^ {2}} = \frac {n ^ {3}}{\sqrt {t _ {k} - 2 \mu - n}} \cdot \frac {1}{(t _ {k} - 2 \mu - n) ^ {3 / 2}} \\ \geq \sqrt {\frac {n}{t _ {k} - 2 \mu - n}}. \\ \end{array}
$$

It follows that for $t _ { k } \le 2 \mu + n + n ^ { 5 / 3 }$ ,

$$
\mathbb {E} [ \operatorname{Risk} (x _ {k, \nu_ {k} + 1}) ] = \mathcal {O} \left(\frac {n ^ {3}}{(t _ {k} - 2 \mu - n) ^ {2}}\right).
$$

If $t _ { k } \ge 2 \mu + n + n ^ { 5 / 3 }$ , by choosing $b _ { k } = \operatorname* { m a x } \left\{ 2 \mu + \right.$ $\begin{array} { r } { n , \left\lfloor \frac { t _ { k } } { C _ { 2 } n ^ { 1 / 4 } t _ { k } ^ { 1 / 4 } + 1 } \right\rfloor \ge 2 \mu + n , } \end{array}$ , from Lemma 16, it holds that:

$$
\mathbb {E} [ \text { Risk } (x _ {k, \nu_ {k} + 1}) ] = \mathcal {O} \left(\frac {n b _ {k} ^ {2}}{(t _ {k} - b _ {k}) ^ {2}} + \sqrt {\frac {n}{t _ {k} - b _ {k}}}\right). \tag {57}
$$

On the one hand, if $b _ { k } \ = \ 2 \mu + n .$ , by the inequality that $t _ { k } - 2 \mu - n \geq n ^ { 5 / 3 }$ , it holds that:

$$
\begin{array}{l} \frac {n ^ {3}}{(t _ {k} - 2 \mu - n) ^ {2}} = \frac {n ^ {3}}{\sqrt {t _ {k} - 2 \mu - n}} \cdot \frac {1}{(t _ {k} - 2 \mu - n) ^ {3 / 2}} \\ \leq \sqrt {\frac {n}{t _ {k} - 2 \mu - n}}. \\ \end{array}
$$

It follows that:

$$
\begin{array}{l} \mathbb {E} \left[ \operatorname{Risk} \left(x _ {k, \nu_ {k} + 1}\right) \right] = \mathcal {O} \left(\frac {n ^ {3}}{\left(t _ {k} - 2 \mu - n\right) ^ {2}} + \sqrt {\frac {n}{t _ {k} - 2 \mu - n}}\right) \\ = \mathcal {O} \left(\sqrt {\frac {n}{t _ {k} - 2 \mu - n}}\right). \\ \end{array}
$$

On the other hand, if $\begin{array} { r } { b _ { k } = \left\lfloor \frac { t _ { k } } { C _ { 2 } n ^ { 1 / 4 } t _ { k } ^ { 1 / 4 } + 1 } \right\rfloor \le \frac { t _ { k } } { C _ { 2 } n ^ { 1 / 4 } t _ { k } ^ { 1 / 4 } + 1 } , } \end{array}$ , it holds that:

$$
\frac {n b _ {k} {} ^ {2}}{(t _ {k} - b _ {k}) ^ {2}} = \frac {n}{(t _ {k} / b _ {k} - 1) ^ {2}} \leq \frac {1}{C _ {2} ^ {2}} \sqrt {\frac {n}{t _ {k}}} = \mathcal {O} \left(\sqrt {\frac {n}{t _ {k}}}\right). \tag {59}
$$

Since for $n \geq 1$ and $\begin{array} { r } { t _ { k } \geq 1 , b _ { k } = \frac { t _ { k } } { C _ { 2 } n ^ { 1 / 4 } t _ { k } ^ { 1 / 4 } + 1 } \leq \frac { t _ { k } } { C _ { 2 } + 1 } } \end{array}$ . It follows that:

$$
\sqrt {\frac {n}{t _ {k} - b _ {k}}} \leq \sqrt {\frac {(C _ {2} + 1) n}{C _ {2} t _ {k}}} = \mathcal {O} \left(\sqrt {\frac {n}{t _ {k}}}\right). \tag {60}
$$

By plugging Eqs. (59) and (60) into Eq. (57), it follows that if $\begin{array} { r } { b _ { k } = \left\lfloor \frac { t _ { k } } { C _ { 2 } n ^ { 1 / 4 } t _ { k } ^ { 1 / 4 } + 1 } \right\rfloor } \end{array}$ C2n1/4t1/4k +

$$
\mathbb {E} [ \text { Risk } (x _ {k, \nu_ {k} + 1}) ] = \mathcal {O} \left(\sqrt {\frac {n}{t _ {k}}}\right) = \mathcal {O} \left(\sqrt {\frac {n}{t _ {k} - 2 \mu - n}}\right). \tag {61}
$$

By Eqs. (58) and (61), Eq. (56) holds for $t _ { k } \geq 2 \mu + n + n ^ { 5 / 3 }$ , by choosing $\begin{array} { r } { b _ { k } = \operatorname* { m a x } \left\{ 2 \mu + n , \left\lfloor \frac { t _ { k } } { C _ { 2 } n ^ { 1 / 4 } t _ { k } ^ { 1 / 4 } + 1 } \right\rfloor \right\} } \end{array}$ .

# C. Proofs for Theorems 4 and 5

In this section, we provide the proofs for Theorems 4 and 5. Proof of Theorem 4. By the definition of expected pseudo regret given in Eq. (2), we obtain, for $i \in [ n ]$ :

$$
\bar {\mathcal {R}} _ {i} (T) = \mathbb {E} \left[ \Sigma_ {t = 1} ^ {T} \operatorname{Risk} \left(x _ {t} ^ {i}\right) \right]
$$

$$
= \mathbb {E} \left[ \operatorname{Risk} \left(\hat {x} _ {1}\right) t _ {1} \right] + \mathbb {E} \left[ \Sigma_ {k = 1} ^ {m} \operatorname{Risk} \left(x _ {k, \nu_ {k} + 1}\right) \left(t _ {k + 1} - t _ {k}\right) \right], \tag {62}
$$

where the first equality follows from Risk $\mathbf { \bar { \mathbf { \Lambda } } } ( x ) \ \triangleq \ \bar { f } ( x ) \ -$ mi $1 _ { x ^ { * } \in { \mathcal { C } } } { \bar { f } } ( x ^ { * } )$ and the second equality follows from $x _ { t } ^ { i } = \hat { x } _ { 1 }$ for $t \in [ t _ { 1 } ]$ , and $x _ { t } ^ { i } = x _ { k , \nu _ { k } + 1 }$ for $t \in [ t _ { k } + 1 , t _ { k + 1 } ]$ and $k \in [ m ]$ in DB2O.

In DB2O with cutting-plane, we take $t _ { 1 } = \ u \ u \left\lceil ( 2 \mu \right. +$ $2 ) C _ { 1 } d \ln ( n T )  \quad$ and $t _ { k } = t _ { 1 } + \left\lceil ( T - t _ { 1 } ) ^ { \frac { 2 - 2 ^ { - k + 2 } } { 2 - 2 ^ { - m + 1 } } } \right\rceil$ 2−2−k+2 for $k =$ $2 , 3 , \ldots , m$ . During the interval $[ 1 , t _ { 1 } ]$ , the models for each learner are initialized as $\hat { x } _ { 1 } . \mathrm { \textbf { B y } }$ Definition 4, the regret loss incurred by each learner until time $t _ { 1 }$ is:

$$
\begin{array}{l} \mathbb {E} \left[ \operatorname{Risk} \left(\hat {x} _ {1}\right) \cdot t _ {1} \right] = \mathcal {O} (n M t _ {1}) \\ = \mathcal {O} (n M \mu d \ln (n T)) = \mathcal {O} (d n ^ {2} \ln (n T)), \tag {63} \\ \end{array}
$$

where the last equality follows from $\mu \leq n - 1$ and omitting constant factors in M . By Lemma 15, it holds that:

$$
\mathbb {E} [ \operatorname{Risk} (x _ {k, \nu_ {k} + 1}) ] =
$$

$$
\mathcal {O} \left(d ^ {3 / 2} \ln (n t _ {k}) \sqrt {\frac {n}{t _ {k} - (2 \mu + 1) C _ {1} d \ln (n t _ {k})}}\right)
$$

$$
= \mathcal {O} \left(d ^ {3 / 2} \ln (n T) \sqrt {\frac {n}{t _ {k} - (2 \mu + 1) C _ {1} d \ln (n T)}}\right),
$$

where the second equality follows from $t _ { k } \leq T$ for $k \in [ m ]$ . By setting $x _ { t } ^ { i } = x _ { k , \nu _ { k } + 1 }$ for $t \in [ t _ { k } + 1 , t _ { k + 1 } ] , k \in [ m ] ,$ , the regret loss incurred during the interval $[ t _ { k } + 1 , t _ { k + 1 } ]$ equals:

$$
\mathbb {E} \left[ \operatorname{Risk} \left(x _ {k, \nu_ {k} + 1}\right) \left(t _ {k + 1} - t _ {k}\right) \right] =
$$

$$
\mathcal {O} \left(d ^ {3 / 2} \ln (n T) \sqrt {n} \frac {t _ {k + 1} - t _ {k}}{\sqrt {t _ {k} - (2 \mu + 1) C _ {1} d \ln (n T)}}\right) \tag {64}
$$

$$
= \mathcal {O} \left(d ^ {3 / 2} \ln (n T) \sqrt {n} \frac {t _ {k + 1} - t _ {1}}{\sqrt {t _ {k} - t _ {1}}}\right)
$$

$$
= \mathcal {O} \left(d ^ {3 / 2} \ln (n T) \sqrt {n} (T - t _ {1}) ^ {\frac {1}{2 - 2 ^ {- m + 1}}}\right),
$$

where the equalities follow from $t _ { 1 } = \Big \lceil ( 2 \mu + 2 ) C _ { 1 } d \ln ( n T ) \Big \rceil$ and $t _ { k } = t _ { 1 } + \left\lceil ( T - t _ { 1 } ) ^ { \frac { 2 - 2 ^ { - k + 2 } } { 2 - 2 ^ { - m + 1 } } } \right\rceil$ 2−2−k+2 for $k = 2 , 3 , \hdots , m .$ . By plugging Eqs. (63) and (64) into Eq. (62), the regret loss of each learner $i \gamma _ { \mathrm { s } }$ models during the whole learning time is:

$$
\bar {\mathcal {R}} _ {i} (T) = \mathcal {O} \left(d n ^ {2} \ln (n T) + m d ^ {3 / 2} \ln (n T) \sqrt {n} (T - t _ {1}) ^ {\frac {1}{2 - 2 ^ {- m + 1}}}\right).
$$

By plugging $m - 1 = \lceil \ln \ln T \rceil$ into the equation above, it holds that:

$$
\begin{array}{l} \bar {\mathcal {R}} _ {i} (T) = \mathcal {O} \left(d n ^ {2} \ln (n T) + d ^ {3 / 2} \ln (n T) \sqrt {n T} \ln \ln T\right) \\ = \tilde {\mathcal {O}} \left(d n ^ {2} + d ^ {3 / 2} \sqrt {n T}\right). \\ \end{array}
$$

In DB2O with cutting-plane, for the k-th instance of T-DBCO with cutting-plane where $k \in [ m ]$ , the learners conduct $\begin{array} { r } { \left\lfloor t _ { k } / b _ { k } \right\rfloor \ = \ \mathcal { O } \big ( d \ln \big ( \frac { d n } { \epsilon _ { \iota } } \big ) \big ) \ = \ \mathcal { O } \big ( d \ln ( n T ) \big ) } \end{array}$ broadcast and convergecast operations in the BFS tree, where each run of broadcast (convergecast) takes ${ \mathcal { O } } ( n )$ communication cost. Overall, the communication cost of DB2O with cutting-plane is $\mathcal { O } ( d n m \ln { ( n T ) } ) = \tilde { \mathcal { O } } ( d n )$ as $m = 1 + \lceil \ln \ln T \rceil$ . □

Proof of Theorem 5. Similarly, as in DB2O with cutting-plane, Eq. (62) holds in this case. In DB2O with AGD, for $k \leq m ^ { \prime }$ , we choose the batch size $b _ { k } = 2 \mu + n$ in T-DBCO. By Lemma 17 and $t _ { k } = 2 \mu + n + \left\lfloor n ^ { 1 + \frac 2 3 \cdot \frac { 2 ^ { \kappa } - 1 } { 2 ^ { m ^ { \prime } } - 1 } } \right\rfloor \le 2 \mu + n + n ^ { 5 / 3 } \mathrm { f o r } k \in [ m ^ { \prime } ]$ n1+ 23 · 2k −12m′ −1 , it holds that:

$$
\begin{array}{l} \mathbb {E} \left[ \operatorname{Risk} \left(x _ {k, \nu_ {k} + 1}\right) \right] = \mathcal {O} \left(\frac {n ^ {3}}{\left(t _ {k} - 2 \mu - n\right) ^ {2}}\right) \tag {65} \\ = \mathcal {O} \left(n ^ {1 - \frac {4}{3} \frac {2 ^ {k} - 1}{2 ^ {m ^ {\prime}} - 1}}\right). \\ \end{array}
$$

During the interval $[ 1 , t _ { 1 } ]$ , the regret loss for learner $i \in [ n ]$ is:

$$
\mathbb {E} [ \operatorname{Risk} (\hat {x} _ {1}) \cdot t _ {1} ] = \mathcal {O} (n R t _ {1}) = \mathcal {O} \left(n ^ {2 + \frac {2}{3} \frac {1}{2 ^ {m ^ {\prime}} - 1}}\right), \tag {66}
$$

where the first equality follows from Definition 5, and the second equality follows from $t _ { 1 } = 2 \mu + n + \left\lfloor n ^ { 1 + \frac { 2 } { 3 } \cdot \frac { 1 } { 2 ^ { m ^ { \prime } } - 1 } } \right\rfloor =$ n 1+ 23 · $\mathcal { O } \left( n ^ { 1 + \frac { 2 } { 3 } \cdot \frac { 1 } { 2 ^ { m ^ { \prime } } - 1 } } \right)$ and omitting constant factors in R. For $1 \leq$ $k \overset { \cdot } { \leq } m ^ { \prime } - 1$ , the regret during the interval $[ t _ { k } + 1 , t _ { k + 1 } ]$ equals:

$$
\begin{array}{l} \mathbb {E} \left[ \operatorname{Risk} \left(x _ {k, \nu_ {k} + 1}\right) \left(t _ {k + 1} - t _ {k}\right) \right] = \mathcal {O} \left(n ^ {1 - \frac {4}{3} \frac {2 ^ {k} - 1}{2 ^ {m ^ {\prime}} - 1}} \left(t _ {k + 1} - t _ {k}\right)\right) \\ = \mathcal {O} \left(n ^ {1 - \frac {4}{3} \frac {2 ^ {k} - 1}{2 ^ {m ^ {\prime}} - 1}} (t _ {k + 1} - 2 \mu - n)\right) \\ = \mathcal {O} \left(n ^ {2 + \frac {2}{3} \frac {1}{2 ^ {m ^ {\prime}} - 1}}\right), \\ \end{array}
$$

where the equalities follow from $t _ { k } = 2 \mu + n + \lfloor n ^ { 1 + \frac { 2 } { 3 } \cdot \frac { 2 ^ { k } - 1 } { 2 ^ { m ^ { \prime } } - 1 } } \rfloor$ for $k \leq m ^ { \prime }$ .

During the interval $[ t _ { m ^ { \prime } } + 1 , t _ { m ^ { \prime } + 1 } ]$ , the regret loss is:

$$
\begin{array}{l} \mathbb {E} \left[ \operatorname{Risk} \left(x _ {m ^ {\prime}, \nu_ {m ^ {\prime}} + 1}\right) \left(t _ {m ^ {\prime} + 1} - t _ {m ^ {\prime}}\right) \right] = \mathcal {O} \left(n ^ {- \frac {1}{3}} \left(t _ {m ^ {\prime} + 1} - t _ {m ^ {\prime}}\right)\right) \\ = \mathcal {O} \left(\sqrt {n} (T - t _ {m ^ {\prime}}) ^ {\frac {1}{2 - 2 ^ {- m + m ^ {\prime}}}}\right), \tag {68} \\ \end{array}
$$

where the first equality follows from Eq. (65), and the second equality follows from $t _ { k } = t _ { m ^ { \prime } } + \left\lceil ( T - t _ { m ^ { \prime } } ) ^ { \frac { 2 - 2 ^ { - k + 1 + m ^ { \prime } } } { 2 - 2 ^ { - m + m ^ { \prime } } } } \right\rceil \geq$ 2−2−k+1+m′ $2 \mu + n + n ^ { 5 / 3 }$ for $k \geq m ^ { \prime } + 1$ .

For $\begin{array} { r l r } { k } & { { } \ge } & { m ^ { \prime } + 1 } \end{array}$ , we choose $\begin{array} { r c l } { b _ { k } } & { = } & { \operatorname* { m a x } \Big \{ 2 \mu \ + } \end{array}$ n, $\begin{array} { r } { n , \lfloor \frac { t _ { k } } { C _ { 2 } n ^ { 1 / 4 } t _ { k } ^ { 1 / 4 } + 1 } \rfloor \} } \end{array}$ C2n1/4t1/4k +1 ′ 2−2−k+1+m . By Lemma 16 and $t _ { k } = t _ { m ^ { \prime } } + \vert ( T -$ $t _ { m ^ { \prime } } ) ^ { \frac { 2 - 2 ^ { \mathrm { ~ \tiny ~ s ~ t ~ i ~ r ~ } } } { 2 - 2 ^ { - m + m ^ { \prime } } } } \Big ] \geq 2 \mu + n + n ^ { 5 / 3 } \mathrm { ~ f o r ~ } k = m ^ { \prime } + 1 , m ^ { \prime } +$ $2 , \ldots , m$ , it holds that:

$$
\begin{array}{l} \mathbb {E} [ \operatorname{Risk} (x _ {k, \nu_ {k} + 1}) ] = \mathcal {O} \left(\sqrt {\frac {n}{t _ {k} - 2 \mu - n}}\right) \\ = \mathcal {O} \Big (\sqrt {\frac {n}{t _ {k} - t _ {m ^ {\prime}}}} \Big) \\ = \mathcal {O} \Big (\sqrt {n} (T - t _ {m ^ {\prime}}) ^ {- \frac {1 - 2 ^ {- k + m ^ {\prime}}}{2 - 2 ^ {- m + m ^ {\prime}}}} \Big), \\ \end{array}
$$

where the second equality follows from $t _ { m ^ { \prime } } \geq 2 \mu + n $ , and the third equality follows from the choice of $t _ { k }$ for $k > m ^ { \prime }$ . The regret loss during the interval $[ t _ { k } + 1 , t _ { k + 1 } ]$ for $k \geq m ^ { \prime } + 1$ is:

$$
\begin{array}{l} \mathbb {E} \left[ \operatorname{Risk} \left(x _ {k, \nu_ {k} + 1}\right) \left(t _ {k + 1} - t _ {k}\right) \right] = \\ \mathcal {O} \left(\sqrt {n} \left(T - t _ {m ^ {\prime}}\right) ^ {- \frac {1 - 2 ^ {- k + m ^ {\prime}}}{2 - 2 ^ {- m + m ^ {\prime}}}} \left(t _ {k + 1} - t _ {k}\right)\right) \\ = \mathcal {O} \left(\sqrt {n} \left(T - t _ {m ^ {\prime}}\right) ^ {- \frac {1 - 2 - k + m ^ {\prime}}{2 - 2 - m + m ^ {\prime}}} \left(t _ {k + 1} - t _ {m ^ {\prime}}\right)\right) \tag {69} \\ = \mathcal {O} \left(\sqrt {n} (T - t _ {m ^ {\prime}}) ^ {\frac {1}{2 - 2 ^ {- m + m ^ {\prime}}}}\right). \\ \end{array}
$$

Plugging Eqs. (66)-(69) into Eq. (62), we obtain that for learner $i \in [ n ]$ ,

$$
\bar {\mathcal {R}} _ {i} (T) = \mathcal {O} \left(n ^ {2 + \frac {2}{3} \frac {1}{2 m ^ {\prime} - 1}} m ^ {\prime} + \sqrt {n} T ^ {\frac {1}{2 - 2 - m + m ^ {\prime}}} (m - m ^ {\prime} + 1)\right). \tag {70}
$$

By plugging $m ^ { \prime } = \left\lceil \ln \ln n \right\rceil$ and $m - m ^ { \prime } = \lceil \ln \ln T \rceil$ into Eq. (70), it follows that:

$$
\bar {\mathcal {R}} _ {i} (T) = \mathcal {O} \left(n ^ {2} \ln \ln n + \sqrt {n T} \ln \ln T\right) = \tilde {\mathcal {O}} (n ^ {2} + \sqrt {n T}).
$$

For the communication complexity analysis of DB2O with AGD, for $k \leq m ^ { \prime } .$ the k-th instance of T-DBCO with AGD conducts $\left\lfloor t _ { k } / b _ { k } \right\rfloor \ = \ \mathcal { O } ( n ^ { 2 / 3 } )$ broadcast and convergecast operations in the BFS tree. For $k \geq m ^ { \prime } + 1$ , the k-th instance of T-DBCO with AGD conducts $\lfloor t _ { k } / b _ { k } \rfloor ~ = ~ \mathcal { O } ( n ^ { 1 / 4 } T ^ { 1 / 4 } )$ broadcast and convergecast operations. The communication cost for each run of broadcast (convergecast) in the BFS tree is ${ \mathcal { O } } ( n )$ . Thus, the communication cost of DB2O with AGD is $\mathcal { O } \big ( n ^ { 5 / 3 } m ^ { \prime } + n ^ { 5 / 4 } T ^ { 1 / 4 } ( m - m ^ { \prime } ) \big ) = \tilde { \mathcal { O } } \big ( n ^ { 5 / 3 } + n ^ { 5 / 4 } T ^ { 1 / 4 } \big )$ as $m ^ { \prime } = \left\lceil \ln \ln n \right\rceil$ and $m - m ^ { \prime } = \lceil \ln \ln T \rceil$ . □

# APPENDIX I PROOFS IN APPENDIX B-B

We provide detailed proofs for Theorems 7 and 8 in this section.

Proof for Theorem 7. By the definition of expected pseudo regret given in Eq. (2), we obtain, for $i \in [ n ]$ :

$$
\begin{array}{l} \bar {\mathcal {R}} _ {i} (T) = \mathbb {E} \left[ \Sigma_ {t = 1} ^ {T} \operatorname{Risk} \left(x _ {t} ^ {i}\right) \right] \\ = \mathbb {E} \left[ \Sigma_ {t = 1} ^ {t _ {1}} \operatorname{Risk} \left(x _ {t} ^ {i}\right) \right] + \mathbb {E} \left[ \Sigma_ {k = 1} ^ {m} \operatorname{Risk} \left(x _ {k, \nu_ {k} + 1}\right) \left(t _ {k + 1} - t _ {k}\right) \right], \tag {71} \\ \end{array}
$$

where the first equality follows from $\operatorname { R i s k } ( x ) ~ \triangleq ~ { \bar { f } } ( x ) ~ -$ $\mathrm { m i n } _ { x ^ { * } \in { \mathcal { C } } } { \bar { f } } ( x ^ { * } )$ and the second equality follows from $x _ { t } ^ { i } =$ $x _ { k , \nu _ { k } + 1 }$ for $t \in [ t _ { k } + 1 , t _ { k + 1 } ]$ and $k \in [ m ]$ in the revised DB2O.

In the revised DB2O with cutting-plane, for $t \leq t _ { 1 }$ , we apply OGD (cf. Eq. (10)) to update xit for $i \in [ n ]$ . By Theorem 1 in [13], it holds that, if $f ( x ; \xi ) , \xi \sim \mathbb { P } _ { i }$ for learner $i \in [ n ]$ satisfy Definitions 3 and 5, then for $i \in [ n ]$ :

$$
\Sigma_ {t = 1} ^ {t _ {1}} \mathbb {E} \left[ \bar {f} _ {i} (x _ {t} ^ {i}) - \min _ {x \in \mathcal {C}} \bar {f} _ {i} (x) \right] = \mathcal {O} (R + L _ {G} \| \mathcal {C} \| ^ {2} + \sigma \| \mathcal {C} \| \sqrt {t _ {1}}), \tag {72}
$$

where $\bar { f } _ { i } ( x ) \triangleq \mathbb { E } _ { \xi \sim \mathbb { P } _ { i } } [ f ( x ; \xi ) ]$ and $\| \mathcal { C } \| \triangleq \operatorname* { m a x } _ { x , y \in \mathcal { C } } \| x - y \|$ For the i.i.d. stochastic setting, it holds that $\mathbb { P } _ { i } \equiv \mathbb { P }$ and ${ \bar { f } } = n { \bar { f } } _ { i }$ for $i \in [ n ]$ . It follows that for $i \in [ n ] \colon$

$$
\begin{array}{l} \mathbb {E} \left[ \Sigma_ {t = 1} ^ {t _ {1}} \operatorname{Risk} \left(x _ {t} ^ {i}\right) \right] = \Sigma_ {t = 1} ^ {t _ {1}} \mathbb {E} \left[ \bar {f} \left(x _ {t} ^ {i}\right) - \min _ {x \in \mathcal {C}} \bar {f} (x) \right] \\ = \mathcal {O} (n R + n L _ {G} \| \mathcal {C} \| ^ {2} + n \sigma \| \mathcal {C} \| \sqrt {t _ {1}}) \tag {73} \\ = \mathcal {O} (n ^ {3 / 2} \sqrt {d \ln (n T)}), \\ \end{array}
$$

where the last equality follows from $\begin{array} { r l } { t _ { 1 } } & { { } = } \end{array}$ $\begin{array} { r l r } { \left\lceil ( 2 \mu + 2 ) C _ { 1 } d \ln ( n T ) \right\rceil } & { { } = } & { \mathcal { O } ( d n \ln ( n T ) ) } \end{array}$ and omitting constant factors in $R , \sigma , L _ { G }$ and ∥C∥.

For $t > t _ { 1 } .$ , we update each $\ v { x } _ { t } ^ { i }$ as in the general stochastic setting. Thus, Eq. (64) holds in this case. Plugging Eqs. (73) and (64) into Eq. (71), we obtain for i  [n]:

$$
\begin{array}{l} \bar {\mathcal {R}} _ {i} (T) = \\ \mathcal {O} (n ^ {3 / 2} \sqrt {d \ln (n T)} + m d ^ {3 / 2} \ln (n T) \sqrt {n} (T - t _ {1}) ^ {\frac {1}{2 - 2 ^ {- m + 1}}}) \\ = \tilde {\mathcal {O}} (n ^ {3 / 2} \sqrt {d} + d ^ {3 / 2} \sqrt {n T}), \\ \end{array}
$$

where the last equality follows from $m \mathrm { ~ - ~ } 1 \mathrm { ~ = ~ } \left\lceil \ln \ln T \right\rceil$ . In the communication complexity analysis, the learners conduct O(md ln (nT )) = O(d ln (nT ) ln ln T ) convergecast and broadcast operations in the BFS tree. The communication cost of each run of convergecast and broadcast is ${ \mathcal { O } } ( n )$ . Thus the communication cost of the revised DB2O with cutting-plane is O(dn ln (nT ) ln ln $T ) = { \tilde { \mathcal { O } } } ( d n )$ . □

Proof of Theorem 8. In the revised DB2O with AGD, similarly to the revised DB2O with cutting-plane, Eq. (71) holds, and Eq. (72) holds for $t \leq t _ { 1 }$ . Similarly, as in the analysis for Eq. (73), it follows that:

$$
\mathbb {E} [ \Sigma_ {t = 1} ^ {t _ {1}} \operatorname{Risk} (x _ {t} ^ {i}) ] = \mathcal {O} (n \sqrt {t _ {1}}) = \mathcal {O} (n ^ {1 1 / 6}),
$$

where the last equality follows from $t _ { 1 } = 2 \mu + n + \lfloor n ^ { 5 / 3 } \rfloor =$ $\mathcal { O } ( n ^ { 5 / 3 } )$ .

For $t > t _ { 1 }$ , following a similar line of analysis as for Eq. (69) in the general stochastic setting, it holds that for $k \geq 2 .$ ,

$$
\mathbb {E} \left[ \operatorname{Risk} \left(x _ {k, \nu_ {k} + 1}\right) \left(t _ {k + 1} - t _ {k}\right) \right] = \mathcal {O} \left(\sqrt {n} \left(T - t _ {1}\right) ^ {\frac {1}{2 - 2 ^ {- m + 1}}}\right).
$$

By Eq. (71), it holds that for $i \in [ n ] \colon$

$$
\begin{array}{l} \bar {\mathcal {R}} _ {i} (T) = \mathcal {O} \left(n ^ {1 1 / 6} + m \sqrt {n} (T - t _ {1}) ^ {\frac {1}{2 - 2 ^ {- m + 1}}}\right) \\ = \tilde {O} (n ^ {1 1 / 6} + \sqrt {n T}), \\ \end{array}
$$

where the last equality follows from $m - 1 = \lceil \ln \ln T \rceil$ . For the communication complexity analysis, in the first instance of T-DBCO with AGD for deriving $x _ { 1 , \nu _ { 1 } + 1 } ,$ , the learners perform $\mathcal { O } ( n ^ { 2 / 3 } )$ convergecast and broadcast operations in the BFS tree. The communication cost is $\mathcal { O } ( n ^ { \bar { 5 } / 3 } )$ . In the k-th instance of T-DBCO with AGD where $2 \leq k \leq m =$ $1 + \lceil \ln \ln T \rceil$ , the communication cost is $\mathcal { O } ( n ^ { 5 / 4 } T ^ { 1 / 4 } )$ . Overall, the communication cost of the revised DB2O with AGD is $\mathcal { O } ( n ^ { 5 / 3 } + n ^ { 5 / 4 } T ^ { 1 / 4 } \ln \ln T ) = \tilde { \mathcal { O } } ( n ^ { 5 / 3 } + n ^ { 5 / 4 } T ^ { 1 / 4 } )$ . □

# APPENDIX J PROOFS IN APPENDIX C

In this section, we provide the detailed proofs for the analysis of diameter-dependent communication complexity in Appendix C.

Proof of Theorem 9. In this diameter-dependent problem setting, we construct the learner network as the claw-shaped one with a given diameter D in Fig. 11. We set $n ^ { \prime } =$ min $\{ \lceil n / 2 \rceil , D \}$ and select the times $t _ { k }$ and the user sets $S _ { k }$ for $k \in [ m ]$ in an iterative way using Alg. 5.

Algorithm 5 Selection algorithm for the time sets $\{ t _ { k } \} _ { k \in [ m ] }$ and user sets $\{ S _ { k } \} _ { k \in [ m ] }$ in an adversarial DOCO algorithm with a static communication pattern

1: Input: An adversarial DOCO algorithm with a static communication pattern, the claw-shaped learner network in Fig. 11
2: Initialization:
3: Set $\varsigma_0 \leftarrow \emptyset$ , $t_0 \leftarrow 0$ , and $\ell \leftarrow 1$ 4: Set $n' \leftarrow \min\{\lceil n/2 \rceil, D\}$ , where $n$ and $D$ are defined in Fig. 11
5: for $t = 1$ to $T$ do
6: $\varsigma_t \leftarrow \varsigma_{t-1}$ 7: for $i = n' + 1$ to $n$ do
8: if learner 1 learns information on $f_s^i$ for $t_{k-1} < s \leq t - 1$ then
9: $\varsigma_t \leftarrow \varsigma_t \cup \{i\}$ 10: end if
11: end for
12: if $|\varsigma_t| \geq \left\lfloor \frac{n-n'}{2} \right\rfloor$ then
13: $\varsigma_t \leftarrow \emptyset$ , $t_\ell \leftarrow t - 1$ , $S_\ell \leftarrow \varsigma_{t-1}$ , and $\ell \leftarrow \ell + 1$ 14: end if
15: end for
16: return $\{t_k\}_{k \in [m]}$ and $\{S_k\}_{k \in [m]}$ , where $m = \ell - 1$

By Alg. 5, it holds that $\begin{array} { r } { | S _ { k } | < \lfloor \frac { n - n ^ { \prime } } { 2 } \rfloor } \end{array}$ for $k \in [ m ]$ . Besides, each time we update ℓ to ℓ + 1, learner 1 learns information from ≥ ⌊ n−n′ $\begin{array} { r } { \lfloor \frac { n - n ^ { \prime } } { 2 } \rfloor + n ^ { \prime } - 1 \geq \lfloor \frac { n - 1 } { 2 } \rfloor } \end{array}$ $\geq \ \lfloor { \frac { n - n ^ { \prime } } { 2 } } \rfloor$ i with  comm $i > n ^ { \prime }$ , which consun budget since $n ^ { \prime } \geq 1$ Thus, it holds that:

$$
r / m \geq \lfloor \frac {n - 1}{2} \rfloor .
$$

Combining the inequality above with the fact that each message takes $n ^ { \prime }$ timeslots transmitted from learners $n ^ { \prime } + 1 \sim n$ to learner 1 in the claw-shaped network in Fig. 11, it holds that:

$$
\begin{array}{l} m \leq \min \left\{(T - 1) / n ^ {\prime}, r / \lfloor \frac {n - 1}{2} \rfloor \right\} \\ = \min \left\{\max \left\{(T - 1) / \lceil n / 2 \rceil , (T - 1) / D \right\}, r / \lfloor \frac {n - 1}{2} \rfloor \right\}. \tag {74} \\ \end{array}
$$

Let $t _ { 0 } = 0 , t _ { m + 1 } = T$ , and $S _ { m + 1 } = \varnothing$ . For each $k \in [ m + 1 ]$ , we select an arbitrary user set $U _ { k } \subseteq \{ n ^ { \prime } + 1 , n ^ { \prime } + 2 , \ldots , n \} \backslash S _ { k }$ such that $\begin{array} { r } { | U _ { k } | = \lceil \frac { n - n ^ { \prime } } { 2 } \rceil } \end{array}$ . Then, we construct the loss functions

$$
f _ {t} ^ {i} (x) = \left\langle x, z _ {t} ^ {i} \right\rangle , x \in \mathcal {C} = \{x \in \mathbb {R} _ {\geq 0} ^ {d} | 1 \leq \| x \| _ {1} \leq 2 \}
$$

for each interval $[ t _ { k - 1 } + 1 , t _ { k } ]$ for $k \in [ m + 1 ]$ as follows:

1) For $i \in [ n ] \backslash U _ { k } .$ , we ensure $f _ { t } ^ { i } \equiv 0$ by setting $z _ { t } ^ { i } \equiv \mathbf { 0 }$ for $t _ { k - 1 } < t \leq t _ { k }$ , where 0 denotes the all-zero vector.   
2) For $i \in U _ { k }$ , we set $z _ { t } ^ { i } \equiv \hat { z } _ { k }$ for $t _ { k - 1 } < t \leq t _ { k }$ , where each $\hat { z } _ { k }$ is uniform in $\{ 0 , 1 \} ^ { d }$ .

Let each $\epsilon _ { k , j }$ be a random variable uniform in {−1, 1} and $\tau _ { k } \triangleq t _ { k } - t _ { k - 1 }$ for $k \in [ m + 1 ]$ . Then following the same line of analysis as for Eq. (13), it holds that:

$$
\begin{array}{l} \mathbb {E} \left[ \mathcal {R} _ {1} (T) \right] \geq \mathbb {E} \left[ \left\lceil \frac {n - n ^ {\prime}}{2} \right\rceil T / 2 - \min _ {x \in \mathcal {C}} \left\langle x, \Sigma_ {k = 1} ^ {m + 1} \Sigma_ {i \in U _ {k}} \tau_ {k} \hat {z} _ {k} \right\rangle\right] \\ = \Omega \big (n \mathbb {E} \big [ \max _ {j \in [ d ]} \Sigma_ {k = 1} ^ {m + 1} \tau_ {k} \epsilon_ {k, j} \big ] \big), \\ \end{array}
$$

where the equality follows from $n ^ { \prime } \leq \lceil n / 2 \rceil$ . By Lemmas 7 and 8, it holds that:

$$
\mathbb {E} [ \mathcal {R} _ {1} (T) ] = \Omega (n T / \sqrt {m}).
$$

By plugging Eq. (74) and the equation that $D = { \mathcal { O } } ( n )$ into the equation above, Eq. (11) then follows. □

Proof of Theorem 10. To prove Theorem 10, we choose the claw-shaped network in Fig. 11 and present two candidate constructions of the set of loss functions $\{ f ( \boldsymbol { x } ; \boldsymbol { \xi } _ { t } ^ { i } ) \} _ { i \in [ n ] }$ , where $\xi _ { t } ^ { i } \sim \mathbb { P } _ { i }$ for some distribution $\mathbb { P } _ { i }$ .

The first construction is the same as the one in the proof for Lemma 11 (note that the i.i.d. stochastic setting is a special case for $\mathbb { P } _ { i } \equiv \mathbb { P }$ in the general stochastic setting). By Lemma 11, it holds that:

$$
\mathbb {E} \left[ \bar {\mathcal {R}} _ {1} (T) \right] = \Omega \big (\max \{n, n \sqrt {T / r}, \sqrt {n T} \} \big). \tag {75}
$$

In the second construction, we let $n ^ { \prime } = \operatorname* { m i n } \{ \lceil n / 2 \rceil , D \}$ . Then, we construct the loss functions for learner i with $i \leq n ^ { \prime }$ and $i > n ^ { \prime }$ in the same way as in Section IV-B in the main text. Similarly, as in Section IV-B, we let $t _ { k } + 1$ be the first time learner 1 learns information on $\xi _ { t } ^ { i } , i > n ^ { \prime }$ for $t _ { k - 1 } < t \leq t _ { k }$ and $k \in [ m ]$ (for simplicity, denote $t _ { 0 } = 0$ and $t _ { m + 1 } = T )$ . In this case, each message takes $n ^ { \prime }$ timeslots and consumes $\geq n ^ { \prime }$ budget transmitted from learners $n ^ { \prime } + 1 \sim n$ to learner 1 in the claw-shaped network in Fig. 11. Thus, it holds that:

$$
m \leq \min \{(T - 1) / n ^ {\prime}, r / n ^ {\prime} \} \leq 2 r / D, \tag {76}
$$

where the second inequality follows from $n ^ { \prime } \quad = \quad$ min $\{ \lceil n / 2 \rceil , D \} \ge \operatorname* { m i n } \{ \lceil D / 2 \rceil , D \} \ge D / 2 .$ Via a similar line of analysis as for Eq. (28), it holds that for $k \in [ m + 1 ]$ ,

$$
\begin{array}{l} \mathbb {E} [ \bar {\mathcal {R}} _ {1} (T) ] \geq \\ (n - n ^ {\prime}) \epsilon t _ {k} \left(\frac {1}{2} - \epsilon \sqrt {2 (n - n ^ {\prime}) (t _ {k - 1} - n ^ {\prime} + 1) _ {+}}\right). \tag {77} \\ \end{array}
$$

Then, following the arguments for Eqs. (29)-(35), it holds that:

$$
\begin{array}{l} \mathbb {E} [ \bar {\mathcal {R}} _ {1} (T) ] = \\ \Omega \left(\max \left\{\left(n - n ^ {\prime}\right) \min \{n ^ {\prime}, T \}, \left(n - n ^ {\prime}\right) ^ {\frac {1}{2 - 2 ^ {- m}}} T ^ {\frac {1}{2 - 2 ^ {- m}}} \right\}\right) \\ = \Omega \left(\max \left\{n \min \{D, T \}, n ^ {\frac {1}{2 - 2 ^ {- m}}} T ^ {\frac {1}{2 - 2 ^ {- m}}} \right\}\right) \\ \end{array}
$$

by choosing ϵ and $t _ { k }$ for $k \in [ m ]$ that maximizes the last expression in Eq. (77), where the second equality follows from $n - n ^ { \prime } \ge \lfloor n / 2 \rfloor = \Omega ( n )$ and $n ^ { \prime } = \Theta ( D )$ as $n ^ { \prime } =$ min $\{ \lceil n / 2 \rceil , D \} \in [ \lceil D / 2 \rceil , D ]$ . By Eq. (76), it follows that:

$$
\mathbb {E} \left[ \bar {\mathcal {R}} _ {1} (T) \right] = \Omega \left(\max \left\{n \min (D, T), n ^ {\frac {1}{2 - 2 ^ {- 2 r / D}}} T ^ {\frac {1}{2 - 2 ^ {- 2 r / D}}} \right\}\right). \tag {78}
$$

Theorem 10 then follows by taking the maximum of the righthand sides of Eqs. (75) and (78). □

Proof of Theorem 11. In the proof of Theorem 11, we choose the claw-shaped network in Fig. 11 and construct the loss functions in the same way as in the proof of Theorem 6. Then Theorem 11 follows from Lemma 11, which provides a lower bound for $\bar { \mathcal { R } } _ { 1 } ( T )$ in the i.i.d. stochastic setting on any connected networks. □