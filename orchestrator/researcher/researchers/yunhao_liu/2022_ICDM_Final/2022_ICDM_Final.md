# A Unified Guaranteed Impression Allocation Framework for Online Display Advertising

Hong Zhang1, Lan Zhang2, Ju Huang2, Anran Li3, Haoran Cheng2, Dongbo Huang1, and Lan Xu1 1Tencent, Shanghai, China

2School of Computer Science and Technology, University of Science and Technology of China, Hefei, China

3School of Computer Science and Engineering, Nanyang Technological University, Singapore

1{keyzhzhang, andrewhuang, lanxu}@tencent.com, 2zhanglan03@gmail.com, {huangju0731, chr990315}@mail.ustc.edu.cn

3anran.li@ntu.edu.sg

Abstract—In online display advertising, guaranteed delivery (GD) ads and real-time bidding (RTB) are two main ways to sell impressions for a publisher. While RTB has gained increasing popularity, there is still a proportion of revenue generated from GD ads [1]. Existing mainstream impression allocation models deal with the two delivery ways separately, failing to achieve optimal allocation for multi-objective under multi-constraints, e.g., maximizing gross merchandise volume pre mille (GPM) and revenue per mille (RPM), thus limiting the overall revenue for both the publisher and advertisers. To solve the above problems, we propose a unified guaranteed impression allocation framework to optimally allocate impressions for both GD ads and RTB ads simultaneously. Specifically, we formulate the optimization problem as a non-convex quadratically constrained quadratic programming (QCQP) problem. Then we design an end-to-end unified impression allocation framework to approximately solve the QCQP problem. Furthermore, experiments on real data from Tencent News show that our design significantly increases the overall revenue of both the publisher and advertisers, while achieving much faster convergence than the current state-of-theart methods.

Index Terms—Guaranteed Contracts, Real-time Bidding, Unified Guaranteed Allocation, Advertisement Allocation

# I. INTRODUCTION

Online display advertising has become one of the most influential business with \$189.3 billion revenue for FY 2021 [2]. In online display advertising, advertisers acquire the impression opportunities, which are generated when a user visits a publisher, to display their ads at certain costs, and these costs ultimately become the publisher’s revenue. There are two major ways to sell impressions for the publisher in display advertising. 1) Guaranteed delivery (GD) ads [3]–[5]: the advertiser specifies the contract payment amount, the campaign duration and the desired number of ad impressions by signing contract with the publisher before the ad delivery starts. The publisher must guarantee to delivery the agreed number of ad impressions, and would get penalty for under-delivery. 2) Real-time bidding (RTB) [6], [7]: advertisers deliver their bids to compete for each ad impression opportunity, which will be

Lan Zhang is the corresponding author. This research was supported by the National Key RD Program of China 2021YFB2900103, China National Natural Science Foundation with No. 61932016, No. 62132018. This work was partially supported by Tencent Marketing Solution Rhino-Bird Focused Research Program and ”the Fundamental Research Funds for the Central Universities” WK2150110024. allocated to the bidder offering the highest bid, and the cost is the second highest bid [8]. There is no guarantee of the allocated impression volume for any advertiser in RTB.

Since the price per impression of GD is usually much higher than the winning bid of RTB, the publisher adopts a hierarchical advertising mechanism [9]–[12], where GD ads are prioritized to play. For some impressions, however, the bids of RTB are higher than the price of GD [6], where using hierarchical mechanism would reduce the revenue. Few work has considered impression allocation modeling when GD and RTB are both acquiring impressions. The most relevant work [13] proposes a reinforcement learning approach to maximize the revenue of the advertiser under constraints. This work, however, only considers the optimization of the individual ad. Moreover, it cannot maximize the revenue of the publisher and advertisers at the same time. To achieve this goal, we need to address the following main challenges. 1) Maximizing total revenue for both GD ads and RTB ads: The total revenue depends on the revenue from GD and RTB, and the potential contract violation penalties. Designing an end-to-end unified model to allocate impressions considering all these factors simultaneously is non-trivial. 2) Fulfilling demand for both the publisher and advertisers: Under-delivery and low-quality impression allocation would reduce the revenue of the publisher and advertisers. Meanwhile, impression allocation for RTB ads is to maximize the sum value of winning impressions under budget and key performance indicators (KPIs) constraints, e.g., conversion cost.

To address the above challenges, we propose a Unified Guaranteed impression Allocation framework, named UGA, to maximize revenue for both the publisher and advertisers, while ensuring the impression quality for GD ads. The contributions of this work can be summarized as follows.

• We propose the UGA model to portray the optimal impression allocation problem considering both GD ads and RTB ads. To the best of our knowledge, we are the first to unify the allocation for GD ads and RTB ads about the metrics, e.g., optimized cost per mille (oCPM), through a non-convex quadratic constrained quadratic programming problem [14], so as to achieve the optimal overall impression allocation.   
• We design the UGA framework, which consists of fea-

ture transform module and differentiable sorting network module to solve the optimization problem. The feature transform module enables UGA to be generalized in new ads with obtaining better bids. The differentiable sorting network designed with ad indicators enhances the flexibility of ad allocation, which makes it possible to adjust the bids of various ads in dynamic environments.

• We extensively evaluate our design on real data generated from bidding logs on Tencent News advertising platform. The experimental results show that our allocation solutions achieve a significant improvement on many evaluation metrics, e.g., GPM, RPM, click through rate (CTR) and conversion rate (CVR), which have brought a considerable revenue growth. Compared with SOTA methods, UGA achieves a 10.6% revenue growth for the publisher and a 6.54% revenue growth for advertisers.

# II. RELATED WORK

In online advertising, revenue maximization is always the key issue for publishers. Due to the complexity of the online advertising ecosystem, this problem leads to diverse approaches. [15] consider a publisher selling its ads through RTB only, and define strategies for the publisher to set appropriate reserve prices in each auction to optimize its RTB revenue. There are also many algorithms have been proposed to maximize revenue by considering only GD ads. High Water Mark (HWM) [16] and SHALE [3] model allocation at the crowd level or user level, and RAP [5] models allocation at the request level. While these work account for a variety of constraints, in our problem we consider both GD and RTB ads, which significantly increases the complexity of the allocation problem.

Ghosh et al. [10] proposes for the first time to treat guaranteed contract ads as RTB ads, in order to find a compromise solution to minimize the required computing resources and maximize the quality of guaranteed contracts. Assuming that advertisers’ purchase behavior of guaranteed contracts are determined, [11] proposes a revenue maximization model that allocates and prices the future impressions between RTB and guaranteed contracts. On the basis of meeting the needs of the guaranteed contract ads, [17] proposes a stochastic policy to maximize the total revenue for the publisher. [12] presents a optimization algorithm for the publisher to deliver guaranteed contracts while maximizing RTB revenue. However, it does not consider the quality of ads when allocating.

In addition, in recent years, some scholars have noticed that reinforcement learning (RL) can be used as a tool to overcome the dynamic changes of auction environment. For example, Cai et al. [18] formulate the bid decision process as a reinforcement learning problem, where the state space is represented by the auction information and the campaign’s real-time parameters, while an action is the bid price to set. By modeling the state transition via auction competition, they build a Markov Decision Process framework (called RLB) for learning the optimal bidding policy to optimize the advertising performance in the dynamic real-time bidding environment. Specifically, at each time step (triggered by a bid request arriving), the bidding agent first observes a state (about the current RTB environment) and selects a bid action from the action space under the state, where the action is the bid price for the auctioned impression. However, model-based RL approaches proposed by Cai et al. [18] require storing the state transition matrix and using dynamic programming algorithms, whose computational cost is unacceptable in realworld advertising platforms.

In order to avoid expensive computational cost brought by model-based RL approaches, some work [19] [20] seek to solve the markov decision process (MDP) by using a modelfree RL algorithm. Wu et al. [19] train an agent to sequentially regulate the bidding parameter instead of directly producing bids. The agent strives to learn and adapt to the highly nonstationary environment in order to make the bidding parameter always close to the optimal one. Rather than generating bid prices directly, Zhao et al. [20] decide a bidding model for impressions of each hour and perform real-time bidding accordingly.

Unfortunately, the performance of both model-based and model-free bidding strategies is unsatisfactory. According to [21], RLB’s bidding performance is worse than that of budget allocation algorithms. Moreover, the value-based model-free RL algorithms, such as Deep Q Network (DQN) [19], may have convergence issues in practice and all have shown unable to converge to any policy for both simple MDP and simple function approximator [22]. Further, Wu et al. [23] proposes a multi-agent reinforcement learning (MARL) approach to derive optimal policies for the publisher, but the experimental results show that the time cost is difficult to meet the real-time requirements of the advertising system.

In summary, there still lacks an effective solution to optimize overall revenue of the publisher and advertisers from both guarantee contracts and RTB ads simultaneously. And in this paper, we design a unified guaranteed impression allocation framework to optimally allocate impressions for both GD and RTB simultaneously, which can avoid expensive computing costs and meet the real-time requirements of advertising systems.

# III. PROBLEM FORMULATION

The goal of impression allocation is to simultaneously maximize GD revenue, RTB revenue, contract impression quality, and GMV for advertisers, when GD and RTB are both acquiring impressions. The following modeling uses singletarget ocpm as an example, but it can be extended to more RTB scenarios.

# A. Problem Formulation

Suppose there are N ads (including GD and RTB), which indexed by $j ,$ and M impressions indexed by i. Let $A _ { G D }$ , $A _ { R T B }$ be sets of indices of GD ads and RTB ads, and let $\Gamma ( j )$ denote the set of impression indices of ad $j .$ On the one hand, for each GD contract $j ,$ let $t _ { j 1 } , r _ { j 1 } , o _ { j 1 } , u _ { j 1 }$ be the demand of impression amount, the real impression amount, the impression over-delivery amount and the impression underdelivery amount. Let $p _ { j }$ be the violation penalty of underdelivery contract $j$ . Let $C _ { j }$ be the unit price of each impression of contract $j$ . Let $x _ { i j } ~ \in ~ \{ 0 , 1 \}$ be the indicator whether impression i is allocated to ad $j ,$ and obviously $\begin{array} { r } { \sum _ { j \in \Phi ( i ) } x _ { i j } \le 1 } \end{array}$ , where $\Phi ( i )$ denotes all the ads that compete for the impression $i ,$ since an impression can be allocated to at most one ad. Let $q _ { i j }$ be impression $i \mathbf { \ ' } _ { \mathbf { S } }$ quality for contract $j .$ The impression allocation for GD ads is required to fulfill both amount demands and quality demands. Specifically, the revenue from GD ads is,

$$
\begin{array}{l} R _ {G D} = \sum_ {j \in A _ {G D}} \sum_ {i \in \Gamma (j)} x _ {i j} C _ {j} - \sum_ {j \in A _ {G D}} o _ {j 1} C _ {j} \\ - \sum_ {j \in A _ {G D}} p _ {j} u _ {j 1} + \lambda_ {g d} \sum_ {j \in A _ {G D}} \sum_ {i \in \Gamma (j)} q _ {i j} x _ {i j}, \tag {1} \\ \end{array}
$$

where $\lambda _ { g d }$ is the corresponding weight.

On the other hand, RTB will also submit a list of bids to compete for each impression i. Let $B _ { j }$ denote the payment of one conversion of RTB $j ,$ and let $\mathrm { p C V R } _ { i j } , \mathrm { p C T R } _ { i j }$ denote the conversion rate and click through rate when impression i is allocated to ad $j .$ Then the gross merchandise volume for impression i of RTB ad $j$ is ${ \mathrm { G M V } } _ { i j } = B _ { j } \cdot q _ { i j }$ , where $q _ { i j } \ = \ \mathrm { p C T R } _ { i j } \cdot \mathrm { p C V R } _ { i j }$ . The conversion colume of RTB ad $\begin{array} { r } { { \ j \ \operatorname { i s } \sum _ { i \in \Gamma ( j ) } x _ { i j } q _ { i j } } } \end{array}$ . For RTB ad $j ,$ , let $o _ { j 2 } , u _ { j 2 } , t _ { j 2 } , r _ { j 2 }$ denote exceeded conversion cost, deficient conversion cost, target conversion cost, and real conversion cost, and let $o _ { j 3 }$ , $u _ { j 3 } , t _ { j 3 } , r _ { j 3 }$ denote exceeded budgets, unused budgets, target budgets and real budgets of RTB ad $j .$ . We use the second-price auction mechanism [8], and let $\delta _ { i j }$ be the difference between the first price and the second price for impression i when it is allocated to RTB ad $j .$ The bidding price for impression i of ad $j$ is $b _ { i j }$ . The revenue from RTB consists of two parts, one from the publisher and one from advertisers. Therefore, the revenue from RTB ads is,

$$
\begin{array}{l} R _ {R T B} = \lambda_ {g m v} \sum_ {j \in A _ {R T B}} \sum_ {i \in \Gamma (j)} x _ {i j} \cdot \mathrm{GMV} _ {i j} \\ + \lambda_ {r} \left\{\sum_ {j \in A _ {R T B}} \sum_ {i \in \Gamma (j)} x _ {i j} \cdot \left(b _ {i j} - \delta_ {i j}\right) \right\} \tag {2} \\ - \lambda_ {r} \bigl \{\sum_ {j \in A _ {R T B}} o _ {j 3} + \sum_ {j \in A _ {R T B}} o _ {j 2} \sum_ {i \in \Gamma (j)} x _ {i j} q _ {i j} \bigr \}, \\ \end{array}
$$

where $\lambda _ { g m v }$ and $\lambda _ { r }$ are corresponding weights. In Eq. (2), the first line calculates the GMV of RTB ads, the second line calculates total revenue of the publisher, and the third line calculates the sum of exceeded budgets and conversion cost.

By putting the above objectives together, we also need to fulfill the following constraints, the demand constraints of GD impressions (Eq. (4)) and GD clicks (Eq. (5)), the demand constraints of each RTB conversion’s costs (Eq. (6)) and RTB budgets $\left( \operatorname { E q . } \left( 7 \right) \right)$ . Furthermore, we consider price comparison of ads to meet the auction mechanism, e.g., if impression i is allocated to RTB ad $j ,$ then the price of RTB ad j for impression i should be higher than that of contracts (Eq. (8)). The difference between the first price and the second price should be smaller than that between the first price and other prices (Eq. (9)). The optimal impression allocation problem can be summarized as follows,

TABLE I NOTATIONS FOR IMPRESSION ALLOCATIONS 

<table><tr><td>Notations</td><td>Descriptions</td></tr><tr><td> $C_j$ </td><td>Payment of one impression of GD  $j$ </td></tr><tr><td> $B_j$ </td><td>Payment of one conversion of RTB  $j$ </td></tr><tr><td> $x_{ij}$ </td><td>Indicator whether impression  $i$  is allocated to GD  $j$ </td></tr><tr><td> $o_{j1}, u_{j1}, t_{j1}, r_{j1}$ </td><td>Impression over-delivery/ under-delivery/ target/ real amount of GD  $j$ </td></tr><tr><td> $o_{j2}, u_{j2}, t_{j2}, r_{j2}$ </td><td>Exceeded/ deficient/ target/ real conversion cost of RTB ad  $j$ </td></tr><tr><td> $o_{j3}, u_{j3}, t_{j3}, r_{j3}$ </td><td>Exceeded/ unused/ target/ real budget of RTB ad  $j$ </td></tr><tr><td> $o_{j4}, u_{j4}, t_{j4}, r_{j4}$ </td><td>Click over-delivery/ under-delivery/ target/ real amount of GD  $j$ </td></tr><tr><td> $\Gamma(j)$ </td><td>Set of impressions targeted to ad  $j$ </td></tr><tr><td> $\Phi(i)$ </td><td>Set of ads target to impression  $i$ </td></tr><tr><td> $p_j$ </td><td>Violation penalty of under-delivery of contract  $j$ </td></tr><tr><td> $q_{ij}$ </td><td>Impression  $i$ &#x27;s quality for ad  $j$ </td></tr><tr><td> $R_{GD}, R_{RTB}$ </td><td>Total revenue of GD ads and RTB ads</td></tr><tr><td> $b_{ij}$ </td><td>Bidding for impression  $i$  of ad  $j$ </td></tr></table>

$$
\text { maximize } \quad R _ {G D} + R _ {R T B} \tag {3}
$$

$$
\text { s.t. } \quad \sum_ {i \in \Gamma (j)} x _ {i j} - o _ {j 1} + u _ {j 1} = t _ {j 1}, \forall j \in A _ {G D}, \tag {4}
$$

$$
\sum_ {i \in \Gamma (j)} x _ {i j} q _ {i j} - o _ {j 4} + u _ {j 4} = t _ {j 4}, \forall j \in A _ {G D}, \tag {5}
$$

$$
\frac {\sum_ {i} x _ {i j} \cdot (b _ {i j} - \delta_ {i j})}{\sum_ {i \in \Gamma (j)} x _ {i j} q _ {i j}} - o _ {j 2} + u _ {j 2} = t _ {j 2}, \forall j \in A _ {R T B}, \tag {6}
$$

$$
\sum_ {i} x _ {i j} \cdot (b _ {i j} - \delta_ {i j}) - o _ {j 3} + u _ {j 3} = t _ {j 3}, \forall j \in A _ {R T B}, \tag {7}
$$

$$
\begin{array}{l} b _ {i j} + \gamma_ {i j k} \cdot \left(1 - x _ {i j}\right) - \zeta_ {i j k} = b _ {i k}, \\ \text {   (8) } \end{array}
$$

$$
\forall i, \forall j, k \in \Phi (i) \cap (A _ {G D} \cup A _ {R T B})
$$

$$
\delta_ {i j} \cdot x _ {i j} \leq \zeta_ {i j k} \cdot x _ {i j}, \quad \forall i, j, k, \tag {9}
$$

$$
\sum_ {j \in \Phi (i)} x _ {i j} \leq 1, \forall i \tag {10}
$$

$$
\gamma_ {i j k}, \zeta_ {i j k} \geq 0, \forall i, j, k,
$$

$$
\delta_ {i j} \geq 0, \forall i, j, \tag {11}
$$

$$
o _ {j 1}, u _ {j 1}, o _ {j 4}, u _ {j 4} \geq 0, \forall j \in A _ {G D},
$$

$$
o _ {j 2}, u _ {j 2}, o _ {j 3}, u _ {j 3} \geq 0, \forall j \in A _ {R T B},
$$

where $\gamma _ { i j k }$ and $\zeta _ { i j k }$ are deficient price and exceeded price of ad k for impression i compared to the price of ad $j$ for impression i, respectively. $o _ { j 1 } , o _ { j 2 } , o _ { j 3 } , o _ { j 4 } , u _ { j 1 } , u _ { j 2 } , u _ { j 3 } , u _ { j 4 } ,$ , $\gamma _ { i j k }$ and $\zeta _ { i j k }$ are slack variables of constraints. Compared with the existing work [13], which only considers the optimization of individual ads, our formulation takes the influence of any ad’s bid on bids of other ads into considerations, achieving the goal of optimizing the revenue of the publisher and advertisers simultaneously.

In the above optimization problem, the basic variable is the bidding price $b _ { i j } , i \in [ M ] , j \in [ N ]$ , while other variables can be calculated from the basic variable. For the formulation of bidding price, existing work [13] only explored that for individual RTB ads, not considering that for GD ads. For individual GD ad, the following constraints should be met while maximizing its bid. The first is the constraint of revenue, e.g., this GD ad revenue should be greater than other advertising revenue (line 2 of Eq. (12)). The second is the demand constraint of the GD impression (line 3 of Eq. (12)). Thus, we give the formulation of bidding price for the individual GD ad in the following.

$$
\text { maximize } \quad \sum_ {i \in \Gamma (j)} (C _ {j} + \lambda_ {g d} q _ {i j}) x _ {i j},
$$

$$
\text { s.t. } \sum_ {i \in \Gamma (j)} h _ {i j} x _ {i j} \leq p _ {j} \cdot C _ {j} \cdot \sum_ {i j} x _ {i j}, \tag {12}
$$

$$
\sum_ {i j} x _ {i j} \leq t _ {j 1}, x _ {i \in \Gamma (j)} \in \{0, 1 \}, \forall j \in A _ {G D},
$$

where $h _ { i j }$ is the highest bid of other ads except ad $j$ on impression i. To solve the problem of Eq.(12), impressions set are required to be completely known. However, the complete impressions are hard to obtain since each impression arrives online in real applications. To this end, we derive a unified optimal bidding function inspired from the work [13] as the following.

$$
b _ {i j} = w _ {0 j} + w _ {1 j} \cdot q _ {i j}, \tag {13}
$$

where $\begin{array} { r } { w _ { 0 j } = \frac { C _ { j } - \beta _ { j } } { \alpha _ { j } } } \end{array}$ , which is used to adjust the parameters αjwhen overplay or lack of play happens, and $\begin{array} { r } { w _ { 1 j } = \frac { q _ { i j } } { \alpha _ { i } } } \end{array}$ αj , which is the weight of performance indicator of ad $j . \alpha _ { j } , \beta _ { j }$ are dual variables for the revenue constraint and the demand constraint. The optimal bid for RTB ads is $\begin{array} { r } { b _ { i j } = w _ { 0 } + \sum _ { k } w _ { k } \cdot q _ { i j k } \ [ 1 3 ] } \end{array}$ .

The above is our single-target ocpm modeling of this problem. However, deriving the optimal solution to the problem is not straightforward, because the problem is a non-convex quadratic constrained programming problem which is NPhard [14]. To motivate this work, we first perform a variable analysis. Although there are many variables in the optimization function Eq. (3), there is only one basic variable, the bidding price, and it is only related to the order amount. The other variables are non-base variables. Therefore, when the orderrelated variables are determined, the number of basic variables can be determined, and the solution of the problem can be obtained as long as the optimal bidding price is solved. Taking inspiration from this insight, we model the whole allocation process into the deep neural allocation framework, then update the base variables via stochastic gradient decent (SGD) methods.

# IV. DESIGN OF UGA

To solve the overall objective (Eq. (3)), we design the UGA framework as illustrated in Fig. 1, which mainly consists of feature transformation and differential sorting network (DSN). Recall the variable analysis, we can solve the optimization by SGD methods, which coordinate the adjustments of contract bidding functions close to the optimal ones as much as possible.

# A. Feature Transformation

The feature transformation module is mainly composed of matching, feature transformation and multi-layer perception (MLP) network. The output of the module are weights of ads, which are used to calculate the bidding prices in the next module.

1) Matching: Given N ads with dimension $l _ { a d }$ and M impressions with dimension ${ l _ { i m p } } ,$ the publisher matches the impressions with all qualified ads by ads’ targeting condition and the attributes of impressions. For example, if a GD ad is targeted to women in Shanghai, the ad will only be matched to women in Shanghai and not to men in Shanghai or women in Beijing. Through matching, we are able to obtain a bipartite graph $\textit { G } = \ ( V _ { a d } , V _ { i m p } , E )$ , where $V _ { a d } , \ V _ { i m p }$ are sets of nodes consisting of indices of ads and impressions. The edge set E represents the matching relationships among ads and impressions by concatenating corresponding ad features and impression features. Suppose there are $K \ll M \cdot N$ edges $\{ \bar { f _ { k } } \} _ { k = 1 } ^ { K } , f _ { k } \in R ^ { l _ { b i } }$ , where $l _ { b i } \geq l _ { a d } + l _ { i m p } .$

By generating the bipartite graph, candidate ads and impressions are matched to prepare for the generation of individual ads features.

2) Feature Transformation: Then the publisher employs the feature transform module to aggregate individual matching relation features to form a representation set consisting features $\{ f _ { j } ^ { \prime } \} _ { j = 1 } ^ { N }$ for N ads, each aggregated feature $f _ { j } ^ { \prime } \in R ^ { \bar { l } _ { f t } }$ , where $R ^ { l _ { f t } } \ge R ^ { l _ { b i } }$ . Specifically, for ad $j ,$ the publisher filters relation features with the id of ad $j .$ The publisher generates $f _ { j } ^ { \prime }$ by conducting statistical calculation on some interested feature dimensions, e.g., impressions on specific targets.

The purpose of this section is to increase the differentiation between different ads though extending ads features. For example, for ads that differ only in the target cites feature, the influence of this feature should be taken into account when bidding. However, without matching and feature transformation, features of such ads are likely to be the same, which will compromise the accuracy of bids.

3) MLP Network: Then, the publisher employs a fully connected three-layer perception (MLP) network to extract low-dimension embeddings based on the high dimensions of aggregated features , where the outputs are weights of ads. The MLP network consists of three layers, including one hidden layer $\phi _ { 1 }$ and one output layer $\phi _ { 2 } .$ . Each aggregated feature $f _ { j } ^ { \prime }$ is firstly mapped to a set of intermediate hidden states through the shared fully connected layer to obtain $\{ h _ { j } \} _ { j = 1 } ^ { N } .$ $h _ { j } ~ = ~ \sigma ( \phi _ { 1 } ( x _ { j } ) )$ , where σ is an exponential linear unit (ELU) activation function [24]. Then the hidden state $h _ { j }$ is processed with another fully connected layer $\phi _ { 2 }$ obtaining a low-dimension embedding $h _ { j } ^ { \prime } = \phi _ { 2 } ( h _ { j } ) = \phi _ { 2 } ( \sigma ( \phi _ { 1 } ( x _ { j } ) ) )$ . The output set embeddings or saying weights of ads would be sent to the downstream bidding function as an augmented feature for each ad, which helps to calculate each ad’s rank score.

![](images/ef1083dd82b21afa85c4f6334f0b5af6383bb06b49f32c8a9b52ddd949ed908f.jpg)



Fig. 1. UGA framework.

# B. DSN-based Double Loss Functions

Given weights of ads output from the MLP network, and quality scores, we can calculate bid prices with Eq. (13). Here, we use bid prices as unsorted rank scores. Then we leverage DSN [25] to rank advertisers with a non-increasing order according to their unsorted rank scores. Specifically, for impression i, and for all matched ads, the publisher calculates $b _ { i } = w _ { 0 } + w _ { 1 } \cdot q _ { i } $ , where $w _ { 0 }$ and $q _ { i }$ are weights of ads and quality scores; $b _ { i } \in R ^ { l _ { i } } , l _ { i }$ is the number of ads matching the impression i. The top K ads are considered as winning ads. Then we conduct statistical calculation on the winning ads to obtain ad indicators, e.g., the amount of play and conversion cost.

Then we leverage double loss functions, rank loss, and performance metrics loss, to optimize weights of ads. Denote the rank matrix as $\mathbf { r } = [ r _ { i j } ] _ { i \in [ M ] , j \in [ N ] }$ , where $r _ { i j }$ represents the rank of ad $j$ on impression i. The real rank matrix is $\mathbf { r } ^ { * } = [ r _ { i j } ^ { * } ] _ { i \in [ M ] , j \in [ N ] }$ , where $r _ { i j } ^ { * }$ represents the real rank of ad j on impression i, which is ranked by $G M V _ { i j }$ . Therefore, we formulate the impression allocation learning problem as minimizing the sum of top-K ranks for each impression, which is used to optimize the GMV of advertisers,

$$
\mathcal {L} _ {r} = \sum_ {j \in [ N ]} \frac {1}{| A _ {j} |} \sum_ {i \in \Gamma (j)} \frac {1}{l _ {i}} \left| r _ {i j} - r _ {i j} ^ {*} \right|, \tag {14}
$$

where $A _ { j }$ is the set of indices of ads and $l _ { i }$ denotes the amount of candidate ads on impression i. Further, we use the rank matrix r to compute the K-slots expected performance metrics via $\mathbf { r } \cdot { \cal P } _ { a l l }$ , where $P _ { a l l }$ represents the vector of aggregated performance metrics for all ads from real feedback,

$$
P _ {a l l} = [ \sum_ {l \in [ L ]} \beta_ {l} P _ {l 1}, \dots , \sum_ {l \in [ L ]} \beta_ {l} P _ {l N} ] ^ {T}, \tag {15}
$$

where $P _ { l j }$ represents the l-th performance metric for j-th ad from an impression, e.g., CTR, guaranteed ads play rate (GPR), and conversion cost. $\beta _ { l }$ is the weight of the l-th performance metric, so that different performance metric can be given different attention according to the actual situation. We denote $P _ { l j } ^ { * }$ as the l-th target performance metric for $j -$ th ad. Therefore, the loss for performance metrics for each impression is

$$
\mathcal {L} _ {P} = \sum_ {j \in [ N ]} \sum_ {l \in [ L ]} | P _ {l j} - P _ {l j} ^ {*} | \tag {16}
$$

We use a hyperparameter to balance the rank loss $\mathcal { L } _ { r }$ and the performance metrics loss $\mathcal { L } _ { P }$ .

# V. EXPERIMENTAL EVALUATION

In this section, we evaluate UGA with real impressions and contract data of Tencent news. The evaluation of UGA on real data shows a significant revenue growth.

# A. Experimental Setup

1) Datasets: The datasets we use for experiments come from real-world bidding logs on Tencent News advertising platform. Tencent News is one of the top news media platforms in China which has more than two billions impressions per day. Each impression has four types of user attributes and 17 types of request attributes. User attributes include platform (with 7 options such as iPhone and PC), area (with 396 options such as Shanghai), age and gender. Request attributes include content type (with more than 300 options such as movie and TV), content name (with more than 3,400,000 options such as ”Spider-Man” and ”Friends”), network (5 options such as Wifi and 4G), target time (with 48 options, every half an hour is an option), etc. Specifically, we set up different datasets for offline and online experiments.

• Datasets for Offline Evaluation Due to the large number of original impressions, the datasets is randomly sampled. To verify the robustness of our model in different environments, we choose to extract different proportions of guaranteed contracts ads and RTB ads on different days. The details are shown in the Table II.   
• Datasets for Online Evaluation We use a seven-day window to randomly sample the dataset with 64,000 impressions and 3,391 RTB ads and 43 GD ads on September 3, 2021. The dataset is denoted as $\mathcal { D } _ { 4 }$ .

Besides, we conduct the evaluations on a server with a Tesla P40 GPU and a Intel Xeon CPU E5-2680 v4.

TABLE II DATASETS FOR OFFLINE EXPERIMENTS 

<table><tr><td>Dataset</td><td>Impressions</td><td>Proportion of Contract Ads</td><td>Proportion of RTB Ads</td></tr><tr><td> $\mathcal{D}_1$ </td><td>626971</td><td>10%</td><td>90%</td></tr><tr><td> $\mathcal{D}_2$ </td><td>642351</td><td>20%</td><td>80%</td></tr><tr><td> $\mathcal{D}_3$ </td><td>633541</td><td>40%</td><td>60%</td></tr></table>

2) Evaluation Metrics: Our goal is to improve the revenue of platform and advertisers while meeting various constraints. Therefore, we use the following metrics commonly used in online advertising:

• Revenue Per Mille (RPM): revenue per thousand impressions.   
• GMV Per Mille (GPM): GMV per thousand impressions, and GMV is the sum of the value created by traffic for advertisers. For non-OCPX ads, GMV is the consumption of advertising.   
• Click Through Rate (CTR): refers to the actual number of clicks of an advertisement divided by the amount of impressions.   
• Conversion Rate (CVR): refers to the actual conversion rate of advertising display.   
• Guaranteed ads Play Rate(GPR): represents the contract ads playing impressions as a proportion of the total impressions.   
• Effective Cost Per Mile (eCPM): revenue per thousand impressions for RTB ads.

# B. Offline Evaluations

1) Compared Methods: The compared methods in offline experiments include:

• Liner Program (LP): [13] considered the advertising goal, budget and KPI constraints, formulated the common demand of an ad campaign as a unified constrained bidding problem. The winning impressions can be selected by solving the linear programming problem (LP). In addition, this method can achieve the state-of-the-art performance in offline scenarios.   
• High Water Mark (HWM): [16] is a guaranteed delivery model and it generates a compact allocation plan based on the demand and supply of GD ads to decide which matching contract to show for every user visit. The algorithm based on a greedy heuristic, which sacrifices optimality.

• SHALE: [3] is also a delivery model for GD ads. Based on HWM, they design a two-stage iterative algorithm with optimal dual values in order to achieve a better trade-off between running time and optimality, so that they can approach the optimal solution quickly and improve the GPR of the GD ads.

• Request-level guaranteed delivery Advertising Planning (RAP): [5] building on SHALE and further considerations

were taken into account, including the CTR metrics of the ads, enabling advertisers to achieve sufficiently precise targeting while maintaining high delivery and play rates.It is able to handle a set of customized linear serving constraints.

2) Evaluation Results: The metric values of LP is taken as the baseline since it can achieve the state-of-the-art performance in offline scenarios. In order to demonstrate the robustness of our algorithm, we first conduct experiments on the three datasets for offline evaluations to compare the overall performance of HWM, SHALE, RAP and our proposed UGA in terms of the indicator metrics against the baseline. We elaborate improvements achieved by these methods on the indicator metrics 1 compared to LP in Table III.

From Table III, we can observe that (i) UGA significantly outperforms LP on almost all datasets in RPM and eCPM mertics. Further, UGA also outperforms LP in GPR and CVR metrics, while worse only in CTR metrics. This shows that UGA increased the revenue while meeting the quality demand compared to the LP, which also handles both GD and RTB ads. (ii) Although algorithms for impressions allocation to GD ads alone (HWM, SHALE and RAP) are widely used in industry, they have limitations when both GD and RTB ads are present, and they generally underperform LP in terms of metrics RPM, GPM, eCPM, CTR when GD ads are underrepresented. (iii) Regardless of the percentage of GD ads, our proposed UGA outperforms HWM, SHALE, RAP in all metrics, especially in the metrics RPM, eCPM, which indicates that UGA can achieve good performance while ensuring the robustness of the algorithm.

In order to further explore the improvements of UGA in GD ads and RTB ads respectively, without loss of generality, we calculate the improvements achieved by these methods on GD ads and RTB ads separately on dataset D2. The respective result is reported in Table IV and the following conclusions can be drawn (i) For UGA, the metrics RPM, GPM, eCPM show that compared to LP, it achieves a significant increase in revenue for both advertisers and the publisher by substantially increasing their revenue from GD ads and marginally sacrificing their revenue from RTB ads. Meanwhile, the values on the metrics CTR and CVR show that the UGA performs slightly worse than LP in both aspects, mainly due to the worse impression quality allocated to RTB ads, which is consistent with the revenue performance analyzed above. (ii) Compared to HWM, SHALE and RAP, UGA improves its total revenue by increasing the revenue from RTB ads. In addition, UGA has almost identical values to HWM, SHALE and RAP for GD ads in terms of CTR and CVR, while it performs better on these metrics for RTB ads.

In conclusion, the experimental results show that UGA achieves better performance than all other methods in the offline situation, while guaranteeing the quality of the allocated impressions.

TABLE III THE OVERALL IMPROVEMENTS ON INDICATOR METRICS ACHIEVED BY HWM, SHALE, RAP AND UGA COMPARED TO LP IN OFFLINE EXPERIMENTS. 

<table><tr><td>Alog</td><td>Dataset</td><td>RPM</td><td>GPM</td><td>eCPM</td><td>GPR</td><td>CTR</td><td>CVR</td></tr><tr><td rowspan="3">HWM</td><td> $\mathcal{D}_1$ </td><td>-4.34%</td><td>-1.47%</td><td>-4.85%</td><td>18.93%</td><td>-17.25%</td><td>5.28%</td></tr><tr><td> $\mathcal{D}_2$ </td><td>2.22%</td><td>1.19%</td><td>1.71%</td><td>51.65%</td><td>-21.94%</td><td>0.00%</td></tr><tr><td> $\mathcal{D}_3$ </td><td>1.06%</td><td>-0.43%</td><td>0.59%</td><td>36.12%</td><td>-28.92%</td><td>7.59%</td></tr><tr><td rowspan="3">SHALE</td><td> $\mathcal{D}_1$ </td><td>-4.32%</td><td>-1.45%</td><td>-4.83%</td><td>18.93%</td><td>-17.25%</td><td>5.28%</td></tr><tr><td> $\mathcal{D}_2$ </td><td>4.34%</td><td>2.64%</td><td>3.82%</td><td>60.33%</td><td>-23.02%</td><td>-1.20%</td></tr><tr><td> $\mathcal{D}_3$ </td><td>8.98%</td><td>4.99%</td><td>8.45%</td><td>60.02%</td><td>-35.19%</td><td>3.13%</td></tr><tr><td rowspan="3">RAP</td><td> $\mathcal{D}_1$ </td><td>-4.72%</td><td>-1.94%</td><td>-5.23%</td><td>18.93%</td><td>-17.25</td><td>5.28%</td></tr><tr><td> $\mathcal{D}_2$ </td><td>3.97%</td><td>2.19%</td><td>3.45%</td><td>60.33%</td><td>-23.02%</td><td>-1.20%</td></tr><tr><td> $\mathcal{D}_3$ </td><td>8.79%</td><td>4.74%</td><td>8.25%</td><td>60.02%</td><td>-34.84%</td><td>3.57%</td></tr><tr><td rowspan="3">UGA</td><td> $\mathcal{D}_1$ </td><td>10.57%</td><td>-0.72%</td><td>44.58%</td><td>18.93%</td><td>-11.62%</td><td>7.32%</td></tr><tr><td> $\mathcal{D}_2$ </td><td>13.86%</td><td>3.09%</td><td>37.13%</td><td>60.33%</td><td>-18.35%</td><td>0.00%</td></tr><tr><td> $\mathcal{D}_3$ </td><td>13.99%</td><td>5.25%</td><td>26.24%</td><td>60.01%</td><td>-31.71%</td><td>4.46%</td></tr></table>

TABLE IV THE IMPROVEMENTS ON INDICATOR METRICS ACHIEVED BY HWM, SHALE AND UGA COMPARED TO LP IN EACH OF THE THREE AREAS OF OVERALL, GD ADS, AND RTB ADS ON THE DATASET $\mathcal { D } _ { 2 }$ . 

<table><tr><td>Alog</td><td>Type</td><td>RPM</td><td>GPM</td><td>eCPM</td><td>GPR</td><td>CTR</td><td>CVR</td></tr><tr><td rowspan="3">HWM</td><td>Overall</td><td>2.22%</td><td>1.19%</td><td>1.71%</td><td>51.65%</td><td>-21.94%</td><td>0.00%</td></tr><tr><td>RTB</td><td>-53.16%</td><td>-49.16%</td><td>-53.55%</td><td>-</td><td>-45.93%</td><td>0.00%</td></tr><tr><td>GD</td><td>86.86%</td><td>86.86%</td><td>86.86%</td><td>51.65%</td><td>43.58%</td><td>-</td></tr><tr><td rowspan="3">SHALE</td><td>Overall</td><td>4.34%</td><td>2.64%</td><td>3.82%</td><td>60.33%</td><td>-23.02%</td><td>-1.20%</td></tr><tr><td>RTB</td><td>-53.10%</td><td>-49.16%</td><td>-53.49%</td><td>-</td><td>-45.39%</td><td>-1.20%</td></tr><tr><td>GD</td><td>86.26%</td><td>86.26%</td><td>86.26%</td><td>60.33%</td><td>44.28%</td><td>-</td></tr><tr><td rowspan="3">RAP</td><td>Overall</td><td>3.97%</td><td>2.19%</td><td>3.45%</td><td>60.33%</td><td>-23.02%</td><td>-1.20%</td></tr><tr><td>RTB</td><td>-53.68%</td><td>-49.79%</td><td>-54.06%</td><td>-</td><td>-46.29%</td><td>-1.20%</td></tr><tr><td>GD</td><td>86.26%</td><td>86.26%</td><td>86.26%</td><td>60.33%</td><td>49.34%</td><td>-</td></tr><tr><td rowspan="3">UGA</td><td>Overall</td><td>13.86%</td><td>3.09%</td><td>37.13%</td><td>60.33%</td><td>-18.35%</td><td>0.00%</td></tr><tr><td>RTB</td><td>-38.60%</td><td>-48.52%</td><td>-2.98%</td><td>-</td><td>-41.59%</td><td>0.00%</td></tr><tr><td>GD</td><td>86.26%</td><td>86.26%</td><td>86.26%</td><td>60.33%</td><td>48.31%</td><td>-</td></tr></table>

# C. Online Evaluations

1) Compared Methods: In addition to the HWM, SHALE, and RAP mentioned in the offline experiments, the following compared methods are included in online experiments:

• Fixed Parameter (FP): Fixed Parameter Algorithms are an alternative way to deal with NP-hard problems instead of approximation algorithms. FP method is reflected in the application of Eq.13.   
• Model Predictive PID Control (M-PID): M-PID, proposed by [26], tries to maximize the advertising value with the budget and the KPI constraints. Different from PID, M-PID requires expert knowledge and can adjust multiple parameters at the same time. This approach has been widely used in real-world advertising environments.   
• Unified Solution to Constrained Bidding (USCB): USCB proposed by [13] abstracts the core demand of constrained bidding and augments it with a more efficient policy search method. In addition, USCB is the state-of-

the-art algorithm method to dynamically adjust parameters to the optimal ones in non-stationary environment between consecutive days.

2) Evaluation Results: We conduct experiments on the dataset $\mathcal { D } _ { 4 }$ to prove the effectiveness of UGA in real online scenarios. We take the metric values of FP as the baseline and elaborate the improvements achieved by HWM, SHALE, RAP, M-PID, USCB and UGA in Table V. To further explore the performance of these methods on various types of ads, here we also calculate the ratio of improvements achieved on each of their three aspects: overall, RTB ads and GD ads.

Different from offline scenario, there is feedback adjustment between multiple time slices in online scenario. From Table V, we can see that UGA outperforms existing methods on all metrics, including RPM, GPM, eCPM, GPR. To better understand the performances of all methods, we present the analyses on these methods as follows. FP could achieve good results when the allocation environment is stable. However, it obtains the worst results as the environment fluctuates enormously. HWM, SHALE, and RAP are all algorithms for GD ads, so they can only achieve better performance in the metrics related to GD ads (GPR) compared to FP, and far worse performance in all other metrics. The disadvantages of these three methods are more obvious in this part of the experiments than in the offline experiments because in the online scenario, it is more necessary to consider all kinds of advertisements and impressions. Therefore, these methods have great shortcomings in the real scenarios. M-PID could adjust the bidding parameters according to the current bidding result, however, it lacks prior knowledge of the environment. USCB is a reinforcement learning (RL) method that is trained to learn the adjustment of bidding parameters at various state. From the experiment results we can see that it can bring more revenue to both advertisers and publishers compared to FP. However, it only considers maximizing the revenue of individual ads, not the overall revenue.

Compared with the above methods, UGA takes into account the influence of changes in advertising bids on other metrics. Therefore, UGA could obtain much higher overall revenue of the publisher and advertisers at the same time as the above methods. This is mainly due to the fact that while maintaining the performance on GD ads, it significantly increases the revenue coming from RTB ads. UGA can achieve almost the same performance as HWM, SHALE, RAP in GD ads related metrics (GPR), and almost similar performance as M-PID, USCB in RTB ads related metrics (CTR, CVR), which indicates that UGA increased the total revenue while meeting the quality demand.

# D. Converging Efficiency

Since the optimization problem to be solved by UGA is a non-convex quadratic constrained quadratic programming problem, the convergence of the model during training is a key challenge. To demonstrate the convergence of UGA, we compare UGA with USCB and normalize the GPM, RPM values of both on the $\mathcal { D } _ { 4 }$ dataset and plot them in Fig. 2.

TABLE V THE IMPROVEMENTS ON INDICATOR METRICS ACHIEVED BY COMPARED METHODS COMPARED TO FP IN EACH OF THE THREE AREAS OF OVERALL, GD ADS, AND RTB ADS ON THE DATASET $\mathcal { D } _ { 4 }$ . 

<table><tr><td>Alog</td><td>Type</td><td>RPM</td><td>GPM</td><td>eCPM</td><td>GPR</td><td>CTR</td><td>CVR</td></tr><tr><td rowspan="3">HWM</td><td>Overall</td><td>-14.39%</td><td>-13.94%</td><td>-19.87%</td><td>12.80%</td><td>-32.40%</td><td>-14.69%</td></tr><tr><td>RTB</td><td>-30.76%</td><td>-29.44%</td><td>-32.57%</td><td>-</td><td>-10.81%</td><td>-14.69%</td></tr><tr><td>GD</td><td>-3.95%</td><td>-3.95%</td><td>-3.95%</td><td>12.80%</td><td>32.73%</td><td>-</td></tr><tr><td rowspan="3">SHALE</td><td>Overall</td><td>-12.85%</td><td>-12.50%</td><td>-19.30%</td><td>19.26%</td><td>-35.33%</td><td>-15.47%</td></tr><tr><td>RTB</td><td>-30.65%</td><td>-29.46%</td><td>-32.47%</td><td>-</td><td>-10.04%</td><td>-15.47%</td></tr><tr><td>GD</td><td>-4.26%</td><td>-4.26%</td><td>-4.26%</td><td>19.26%</td><td>33.38%</td><td>-</td></tr><tr><td rowspan="3">RAP</td><td>Overall</td><td>-13.19%</td><td>-12.87%</td><td>-19.72%</td><td>19.26%</td><td>-36.34%</td><td>-15.44%</td></tr><tr><td>RTB</td><td>-31.49%</td><td>-30.35%</td><td>-33.31%</td><td>-</td><td>-11.44%</td><td>-15.44%</td></tr><tr><td>GD</td><td>-4.26%</td><td>-4.26%</td><td>-4.26%</td><td>19.26%</td><td>38.06%</td><td>-</td></tr><tr><td rowspan="3">M-PID</td><td>Overall</td><td>-5.78%</td><td>2.42%</td><td>-25.25%</td><td>5.54%</td><td>-3.15%</td><td>2.21%</td></tr><tr><td>RTB</td><td>-13.94%</td><td>4.47%</td><td>-44.82%</td><td>-</td><td>-4.85%</td><td>2.21%</td></tr><tr><td>GD</td><td>-0.21%</td><td>-0.21%</td><td>-0.21%</td><td>5.54%</td><td>11.78%</td><td>-</td></tr><tr><td rowspan="3">USCB</td><td>Overall</td><td>0.75%</td><td>4.06%</td><td>-19.05%</td><td>7.69%</td><td>-2.99%</td><td>2.12%</td></tr><tr><td>RTB</td><td>-0.72%</td><td>7.07%</td><td>-34.50%</td><td>-</td><td>-1.45%</td><td>2.12%</td></tr><tr><td>GD</td><td>-0.69%</td><td>-0.69%</td><td>-0.69%</td><td>7.69%</td><td>9.89%</td><td>-</td></tr><tr><td rowspan="3">UGA</td><td>Overall</td><td>6.75%</td><td>7.25%</td><td>7.00%</td><td>17.01%</td><td>-2.04%</td><td>0.63%</td></tr><tr><td>RTB</td><td>14.73%</td><td>16.06%</td><td>17.97%</td><td>-</td><td>9.44%</td><td>0.63%</td></tr><tr><td>GD</td><td>-3.14%</td><td>-3.14%</td><td>-3.14%</td><td>17.01%</td><td>-6.73%</td><td>-</td></tr></table>

It can be seen that both UGA and USCB converge. Since for normalisation we choose the maximum and minimum values of the two methods. For example, for the GPM values of USCB, the maximum and minimum values of GPM in both UGA and USCB are used for normalisation, and UGA outperforms USCB in both metrics, so that the graph lines of USCB are both below UGA. Moreover, UGA converges much faster than the USCB because it provides better initial weights parameters compared to reinforcement learning model, which means that the saddle point can be reached much faster. In addition, we notice that the UGA model has some small oscillations at high levels in the later stages of training, due to the fact that we are solving a non-convex problem. But from the overall perspective, UGA can still achieve the goal of fast convergence and better performance.

# E. Ablation Study

To estimate the effectiveness of each component of the UGA, we compare the performance of two different versions of the proposed method through ablation studies. We refer to the UGA without the feature transformation module UGA-V1, and the UGA without the DSN module and the rank loss function as UGA-V2. We compare UGA-1 and UGA-2 with the full version of the UGA, showing their percentage decreases in diffierent metrics compared to the UGA in the table VI.

From the table VI we can observe: (i) Compared to the UGA, the UGA-V1 shows a decrease in all metrics, especially in RPM and GPM, indicating that the feature transformation module is effective in achieving greater differentiation between different ads, thus improving the accuracy of bids on ads and creating more revenue for the publisher and advertisers. (ii) UGA-V2 also shows decreases in all metrics, with significant decreases in RPM, GPM and CTR, which demonstrates that the combination of the DSN module and rank loss can lead to more accurate ranking of ads, increased user click-through rates and ultimately increased revenue.

![](images/3a119d64b59f58f3d650316a44751409da18fd973fca00feba83a2637e84d1ee.jpg)



Fig. 2. Convergence of UGA and USCB in online experiments.

In summary, the results of the ablation study show that the feature transformation module of UGA can improve the differentiation between different ads to obtain a better feature representation, and the combination of the DSN module and rank loss allows the model to obtain a more accurate output, greatly improving the revenue for both publishers and advertisers.

TABLE VI THE DECLINE ON INDICATOR METRICS FOR UGA-V1 AND UGA-V2 COMPARED TO UGA. 

<table><tr><td>Alog</td><td>RPM</td><td>GPM</td><td>eCPM</td><td>CTR</td><td>CVR</td></tr><tr><td>UGA-V1</td><td>7.91%</td><td>6.61%</td><td>3.24%</td><td>2.82%</td><td>0.79%</td></tr><tr><td>UGA-V2</td><td>6.40%</td><td>6.34%</td><td>3.66%</td><td>7.05%</td><td>3.57%</td></tr></table>

# VI. CONCLUSION

In this paper, we propose a UGA framework to accomplish optimal impression allocation considering GD and RTB simultaneously. We first formulate the optimization problem into a QCQP problem. Then we design an end-to-end framework to approximately solve the formulated optimization problem. Finally, real data experiments testify that our design significantly increases the overall revenue for both the publisher and advertisers and also achieves good convergence rates.

# REFERENCES

[1] “emarketer webinar: Programmatic advertising 2015 outlook,” 2020, https://www.slideshare.net/eMarketerInc/emarketer-webinarprogrammatic-advertising-2015-outlook.

[2] I. webinar, “Internet advertising revenue report: Full year 2021,” 2021. [Online]. Available: https://www.iab.com/insights/ internet-advertising-revenue-report-full-year-2021/   
[3] V. Bharadwaj, P. Chen, W. Ma, C. Nagarajan, J. Tomlin, S. Vassilvitskii, E. Vee, and J. Yang, “Shale: an efficient algorithm for allocation of guaranteed display advertising,” in Proceedings of the 18th ACM SIGKDD, 2012, pp. 1195–1203.   
[4] A. Hojjat, J. Turner, S. Cetintas, and J. Yang, “Delivering guaranteed display ads under reach and frequency requirements,” in Twenty-Eighth AAAI Conference on Artificial Intelligence, 2014.   
[5] H. Zhang, L. Zhang, L. Xu, X. Ma, Z. Wu, C. Tang, W. Xu, and Y. Yang, “A request-level guaranteed delivery advertising planning: Forecasting and allocation,” in Proceedings of the 26th ACM SIGKDD, 2020, pp. 2980–2988.   
[6] J. Wang and S. Yuan, “Real-time bidding: A new frontier of computational advertising research,” in Proceedings of the Eighth ACM International Conference on Web Search and Data Mining, 2015, pp. 415–416.   
[7] S. Yuan, J. Wang, and X. Zhao, “Real-time bidding for online advertising: measurement and analysis,” in Proceedings of the Seventh International Workshop on Data Mining for Online Advertising, 2013, pp. 1–8.   
[8] B. Edelman, M. Ostrovsky, and M. Schwarz, “Internet advertising and the generalized second-price auction: Selling billions of dollars worth of keywords,” American economic review, vol. 97, no. 1, pp. 242–259, 2007.   
[9] R. J. Oentaryo, E.-P. Lim, J.-W. Low, D. Lo, and M. Finegold, “Predicting response in mobile advertising with hierarchical importance-aware factorization machine,” in Proceedings of the 7th ACM international conference on Web search and data mining, 2014, pp. 123–132.   
[10] A. Ghosh, P. McAfee, K. Papineni, and S. Vassilvitskii, “Bidding for representative allocations for display advertising,” in International workshop on internet and network economics. Springer, 2009, pp. 208–219.   
[11] B. Chen, S. Yuan, and J. Wang, “A dynamic pricing model for unifying programmatic guarantee and real-time bidding in display advertising,” in Proceedings of the Eighth International Workshop on Data Mining for Online Advertising, 2014, pp. 1–9.   
[12] G. Jauvion and N. Grislain, “Optimal allocation of real-time-bidding and direct campaigns,” in Proceedings of the 24th ACM SIGKDD, 2018, pp. 416–424.   
[13] Y. He, X. Chen, D. Wu, J. Pan, Q. Tan, C. Yu, J. Xu, and X. Zhu, “A unified solution to constrained bidding in online display advertising,” in Proceedings of the 27th ACM SIGKDD, 2021, pp. 2993–3001.   
[14] S. Elloumi and A. Lambert, “Global solution of non-convex quadratically constrained quadratic programs,” Optimization methods and software, vol. 34, no. 1, pp. 98–114, 2019.   
[15] S. Yuan, J. Wang, B. Chen, P. Mason, and S. Seljan, “An empirical study of reserve price optimisation in real-time bidding,” in Proceedings of the 20th ACM SIGKDD, 2014, pp. 1897–1906.   
[16] P. Chen, W. Ma, S. Mandalapu, C. Nagarjan, J. Shanmugasundaram, S. Vassilvitskii, E. Vee, M. Yu, and J. Zien, “Ad serving using a compact allocation plan,” in Proceedings of the 13th ACM Conference on Electronic Commerce, 2012, pp. 319–336.   
[17] S. R. Balseiro, J. Feldman, V. Mirrokni, and S. Muthukrishnan, “Yield optimization of display advertising with ad exchange,” Management Science, vol. 60, no. 12, pp. 2886–2907, 2014.   
[18] H. Cai, K. Ren, W. Zhang, K. Malialis, J. Wang, Y. Yu, and D. Guo, “Real-time bidding by reinforcement learning in display advertising,” in Proceedings of the Tenth ACM International Conference on Web Search and Data Mining, 2017, pp. 661–670.   
[19] D. Wu, X. Chen, X. Yang, H. Wang, Q. Tan, X. Zhang, J. Xu, and K. Gai, “Budget constrained bidding by model-free reinforcement learning in display advertising,” in Proceedings of the 27th ACM International Conference on Information and Knowledge Management, 2018, pp. 1443–1451.   
[20] J. Zhao, G. Qiu, Z. Guan, W. Zhao, and X. He, “Deep reinforcement learning for sponsored search real-time bidding,” in Proceedings of the 24th ACM SIGKDD, 2018, pp. 1021–1030.   
[21] M. Liu, W. Yue, L. Qiu, and J. Li, “An effective budget management framework for real-time bidding in online advertising,” IEEE Access, vol. 8, pp. 131 107–131 118, 2020.

[22] O. P. Agrawal, “Formulation of euler–lagrange equations for fractional variational problems,” Journal of Mathematical Analysis and Applications, vol. 272, no. 1, pp. 368–379, 2002.   
[23] D. Wu, C. Chen, X. Yang, X. Chen, Q. Tan, J. Xu, and K. Gai, “A multi-agent reinforcement learning method for impression allocation in online display advertising,” arXiv preprint arXiv:1809.03152, 2018.   
[24] D.-A. Clevert, T. Unterthiner, and S. Hochreiter, “Fast and accurate deep network learning by exponential linear units (elus),” arXiv preprint arXiv:1511.07289, 2015.   
[25] X. Liu, C. Yu, Z. Zhang, Z. Zheng, Y. Rong, H. Lv, D. Huo, Y. Wang, D. Chen, J. Xu et al., “Neural auction: End-to-end learning of auction mechanisms for e-commerce advertising,” arXiv preprint arXiv:2106.03593, 2021.   
[26] X. Yang, Y. Li, H. Wang, D. Wu, Q. Tan, J. Xu, and K. Gai, “Bid optimization by multivariable control in display advertising,” in Proceedings of the 25th ACM SIGKDD, 2019, pp. 1966–1974.