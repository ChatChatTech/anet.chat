# Online Pricing with Limited Supply and Time-Sensitive Valuations

Shaoang Li∗, Lan Zhang†, Xiang-Yang Li†

∗†School of Computer Science and Technology, the CAS Key Laboratory of Wireless-Optical Communications,

University of Science and Technology of China, Hefei, China.

∗lishaoa@mail.ustc.edu.cn, †{zhanglan, xiangyangli}@ustc.edu.cn

Abstract—Many efforts have been devoted to online pricing mechanism design for different settings. In this work, we consider a common but challenging setting where the buyers have private time-sensitive valuations and the seller has limited supply. The seller offers a take-it-or-leave-it posted price for each arriving buyer and aims to maximize the expected total revenue. The unknown distribution of time-sensitive valuations and limited supply significantly increase the difficulty of searching the optimal dynamic posted prices. Given B identical items to sell, when the time-dependent valuations can be estimated with a factor of α, we prove Ω(log(1/α)) lower bound with respect to the optimal fixed distribution over prices and design an algorithm achieving tight O(log(1/α)) competitive ratio. When the seller has no information about the future trends of buyers’ valuations, we prove Ω(log B) lower bound and show that there is an algorithm with tight O(log B) competitive ratio by modeling the problem as adversarial bandits with knapsacks optimization. Extensive simulation studies show that our algorithm outperforms previous mechanisms in various settings.

# I. INTRODUCTION

Online pricing mechanisms have been widely applied to various applications such as crowdsourcing [1], online advertising [2], and data pricing [3]. Most conventional pricing mechanisms only consider buyers having flat valuations and neglect the time-sensitive nature of many resources. As examples, in fashion retail, a customer’s valuation of a product usually decreases over time; in the antique market, the older the collectibles, the more expensive; in the fresh market, the valuation of food fluctuates with complex factors. Pricing mechanisms dealing with time-sensitive valuations are not only important for e-commerce, but also increasingly important for offline business. As the electronic price tag becomes more and more popular in supermarkets, convenience stores, etc, it allows merchants to actively implement online pricing mechanisms to increase their revenue. Recently, some mechanisms have been designed for online auction with time-variant valuations [4]–[6], which assume unlimited resource supply. However, a general model considering a more realistic setting of realworld markets, both unknown time-sensitive valuations and limited supply, has barely been explored.

In this work, we study revenue maximization for detail-free posted price online mechanism with limited supply and private time-sensitive valuations. A seller has finite identical items and interacts with a sequence of buyers in an online manner. Each buyer wants to buy one item and has a time-sensitive valuation for the item. The seller offers a take-it-or-leave-it price for each buyer, aiming to maximize the expected total revenue.

It is nontrivial to design an online pricing mechanism with performance guarantee for this problem due to the following major challenges. First, the algorithm needs to estimate the expected total revenue over the whole time horizon rather than the per-round revenue. Conventional detail-free posted price mechanisms usually rely on learning the underlying distribution of buyers’ valuations through historical decisions. However, the resource constraint and the unknown timevariant valuation severely limit the learning ability of those mechanisms or make them quickly exhaust the inventory, hence they no longer guarantee optimal total expected revenue. Second, even without considering the time-sensitive nature, for the problem of dynamic pricing with limited supply , the optimal fixed distribution policy, i.e. sampling the posted price from the optimal fixed distribution over candidate prices in each round, is believed to perform significantly better than the optimal fixed price policy [7]. Therefore, the algorithm needs to search over all possible distributions which is a much larger search space and may consumes more inventory in the exploration phase. Last but maybe the thorniest, the algorithm has to decide the amount of inventory to save for the future while the valuations are time-sensitive and the historical results are insufficient for accurate forecasting. All these challenges add up to make it very difficult to optimize the total revenue.

Facing the aforementioned challenges, we model this online pricing problem with limited supply and time-sensitive valuations as adversarial bandits with knapsacks (adversarial BwK) optimization and design algorithms that choose among a fixed set of candidate prices (arms) in each round to achieve a good tradeoff between exploration and exploitation. We consider two settings: 1) the estimator case in which the timedependency can be estimated with a factor α; and 2) the nonestimator case in which the seller has no information about the time-sensitive functions. For the estimator case, we propose a two-phase algorithm and prove that our algorithm achieves tight O(log(1/α)) competitive ratio w.r.t optimal fixed distribution benchmark. For the non-estimator case, we show that based on the high-probability adversarial BwK algorithm [8] and taking the discretization error into consideration, there is an algorithm achieving tight O(log B) competitive ratio. We also prove the Ω(log(1/α)) and Ω(log B) lower bounds on competitive ratio for estimator case and non-estimator case, respectively. The lower-bound construction shows that the algorithm’s every decision is highly risky for the future.

When assuming the value of the optimal fixed distribution $\mathrm { O P T _ { F D } }$ is known and the number of knapsacks is constant, there exist algorithms achieving O(1)-competitive ratio [8], [9]. Inspired by this fact, we relax the assumption to make it more practical, and the main idea of our two-phase algorithm is to estimate the expected revenue of $\mathrm { O P T } _ { \mathrm { F D } }$ to guide the selection of candidate prices. The first phase is the pure exploration phase where the algorithm aims to estimate $\mathrm { O P T _ { F D } }$ roughly by constructing a picture of the underlying base demand function according to concentration inequality. Our theoretical analysis shows that $\mathrm { O P T } _ { \mathrm { F D } }$ could be estimated up to the factor $\textstyle { \frac { 1 } { \alpha ^ { 2 } } } $ through the pure exploration phase. The second phase is the adaptive exploitation phase which relates to the adversarial BwK optimization. The algorithm performs the exploration-exploitation tradeoff to collect revenue as much as possible by guessing $\mathrm { O P T _ { F D } }$ more precisely based on the output of the first phase. We prove that the adaptive exploitation phase achieving $O ( \log ( 1 / \alpha ) )$ ) competitive ratio if $\mathrm { O P T _ { F D } }$ is known up to the factor $O ( \textstyle { \frac { 1 } { \alpha ^ { c } } } )$ where c is a constant, while previous works only consider the fully unknown or known setting. And our result matches the $O ( 1 )$ result when the value of $\mathrm { O P T _ { F D } }$ is known [8], [9]. Given N buyers, compared with related high probability algorithm in [8], which has to compute linear program $O ( N ^ { 2 } )$ times during the game, our algorithm only needs to compute linear program $O ( N \log N )$ times. Therefore, from the perspectives of both problem assumption and algorithm complexity, our design is obliviously more practical than the existing methods.

Notice that our algorithm is based on finite action space (i.e. the number of arms is finite). To deal with continuous pricing case, we also provide the theoretic discretization error for modeling the online pricing problem with adversarial BwK by lower-bounding the expected total consumption during the time horizon.

We compare our algorithm with three widely used or state-of-the-art algorithms including UCB1 [10], CappedUCB [11], and EXP3.P [12] by numerical evaluations. Experiments results show that the performance and robustness of our algorithm are superior to previous mechanisms in various settings. For example, for the linear decreasing and linear increasing time-sensitive environments , our algorithm achieves 127.7% and 352.2% total revenue w.r.t. UCB1, respectively.

In summary, the main contributions of this work are as follows:

• We study a new challenging setting of online pricing mechanism, where the seller sells identical items with limited supply against buyers whose values are unknown and time-variant.   
• We consider two cases: for the estimator case, we propose an algorithm with tight $O ( \log ( 1 / \alpha ) )$ ) competitive ratio w.r.t. the optimal fixed distribution benchmark; for the non-estimator case, we show that there is an algorithm achieves tight ${ \cal O } ( \log B )$ competitive ratio.

• We prove respectively $\Omega ( \log ( 1 / \alpha ) )$ and $\Omega ( \log B )$ lower bounds for estimator case and non-estimator case w.r.t. the optimal fixed distribution benchmark, respectively.   
• Simulation studies show that our algorithm outperforms previous mechanisms in various settings.

# II. RELATED WORK

Mechanism design have been widely applied in various area [13]–[17] and a great amount of efforts have been devoted to pricing mechanisms [18]–[20]. In recent years, online pricing mechanisms have attracted increasing interests for different settings [21]–[24]. [25] first studied the online posted-price auction with unlimited supply and unknown valuation distribution. They considered the problem as a special case of the MAB problem and applied the UCB1 strategy defined by [10]. However, those online mechanisms do not consider the timesensitive valuations. Recently, [26] investigated online auctions for gradually expiring items to maximize social welfare. [4] proposed a strategy-proof online auction with time-discounting values and assumed the seller knows the discounting functions. [5] studied dynamic pricing with time-variant rewards. BiasedUCB [6] is an online pricing mechanism for revenue maximization with unlimited supply and unknown time-discounting valuations. Those mechanisms explore the pricing policies for time-variant valuations, however, a general but challenging online pricing model with limited supply and unknown timesensitive valuations has barely been investigated.

Another set of literatures relevant to this paper are bandits optimization, in which an agent selects arms sequentially and learns from the rewards, in order to maximize the expected cumulative rewards over a number of trials. Bandits problem has been an active area of research in recent years [27]– [29] and arise in a variety of domains [30]–[35]. [7] first introduced the problem of stochastic bandits with knapsacks and optimally solved it. The most relevant MAB problem is defined by [8], which considers adversarial BwK optimization. There are some subsequent work [9], [36], [37].

# III. PROBLEM FORMULATION AND PREPROCESSING

# A. Problem Formulation

There are B identical items and N buyers, indexed by $[ B ] =$ $\{ 1 , 2 , . . . , B \}$ and $[ N ] = \{ 1 , 2 , . . . , N \}$ , respectively. So the time horizon can be divided into N rounds. Each buyer has a timesensitive valuation $v _ { i } ( t ) \in [ 0 , 1 ]$ . In each round t, the seller interacts with a buyer $b _ { i }$ and offers a take-it-or-leave-it posted price $p _ { t } .$ , which only depends on the historical buyers’ binary decisions. The buyer buys the item if and only if $v _ { i } ( t ) \geq p _ { t }$ , and in case he/she buys the item he/she pays $p _ { t }$ . The setting that one buyer buys one item per round is very common in reality and widely adopted in online pricing research [6], [7], [11]. The game stops once B items are sold out at some round $\tau _ { a l g } \leq N$ or it reaches the N -th round. The objective of the algorithm is to maximize the seller’s expected total revenue.

Many existing online pricing mechanisms assume that for the given item each buyer’s valuation is time-invariant and drawn independently from the same distribution, i.e. $v _ { i } ( t ) = v _ { i }$ and $v _ { i } \sim \mathcal { F }$ . In our work, to characterize the time-sensitive nature of valuations, we introduce the time-sensitive function $g _ { i } ( t ) \in [ 0 , 1 ]$ to represent the changing “value” of the item for each buyer over time:

$$
v _ {i} (t) = v _ {i} \cdot g _ {i} (t) \tag {1}
$$

We call $v _ { i }$ the original value for each buyer $b _ { i }$ . Specifically, we assume there is a base distribution ${ \mathcal F } ,$ and each buyer’s original valuation drawn independently from F before Round 1, i.e. $v _ { i } \sim \mathcal { F }$ . For the convenience of analysis, we assume $\mathcal { F }$ has bounded support [0, 1], which is very common in the literature of online pricing [11]. We use $\mathcal { G }$ to represent the set of time-sensitive functions. We assume the time-sensitive function $g _ { i } ( t )$ is deterministic and oblivious, meaning that it has already been determined before Round 1. Note that, both the base distribution $\mathcal { F }$ and the time-sensitive function set G are unknown to the seller. An instance of our online pricing problem with limited supply and time-sensitive valuations could be denoted as a quadruple $\langle B , N , { \mathcal { F } } , { \mathcal { G } } \rangle$ .

We consider both estimator case and non-estimator case. We first introduce the estimator case. In practice, the buyers usually can be divided into several categories and we use κ to denote the number of categories, i.e.

$$
\forall i \in [ N ], i \in \mathcal {I} _ {j}, j \in [ \kappa ]
$$

$$
s. t. \bigcup_ {j = 1} ^ {j = \kappa} \mathcal {I} _ {j} = [ N ], \qquad \mathcal {I} _ {j _ {1}} \cap \mathcal {I} _ {j _ {2}} = \emptyset , \forall j _ {1}, j _ {2} \in [ \kappa ].
$$

The buyers in each category usually have similar perspectives over the value of the item and their time-sensitive functions are not far away from each other. i.e. $\forall i \in { \mathcal { T } } _ { j }$ , we have $g _ { i } \in \mathcal { G } _ { j }$ , by defining

$$
\mathcal {G} _ {j} = \{f | \alpha_ {j} \leq \frac {g _ {i} (t)}{f (t)} \leq \frac {1}{\alpha_ {j}}, f (t) \in (0, 1 ],
$$

$$
\forall i \in \mathcal {I} _ {j}, t \in [ N ], \alpha_ {j} \in (0, 1 ] \}.
$$

We call $\alpha _ { j }$ the biased rate for $\mathcal { G } _ { j }$ and let $\alpha = \mathrm { m i n } _ { j \in [ \kappa ] } \alpha _ { j }$ . For the estimate case, we assume the seller knows which category the buyer $b _ { i }$ belongs to (for example, $\mathcal { T } _ { j } )$ and has an estimate function $\tilde { g } _ { j } \in \mathcal { G } _ { j }$ . For convenience, we use $\tilde { \mathcal { G } } : = \{ \tilde { g } _ { j } , j \in [ \kappa ] \}$ to denote the set of estimate functions. For the non-estimate case, the seller knows nothing about $\mathcal { F }$ and ${ \mathcal { G } } .$

Letting $\mathcal { F } ( x )$ represent the cumulative distribution function of ${ \mathcal F } .$ From the definition (1), there is a distribution $\mathcal { F } _ { i , t }$ such that $v _ { i } ( t ) \sim \mathcal { F } _ { i , t }$ and we have $\mathcal { F } _ { i , t } ( g _ { i } ( t ) \cdot x ) = \mathcal { F } ( x )$ for round t. Let $r _ { t } ( p _ { t } )$ and $c _ { t } ( p _ { t } )$ denote the revenue and consumption for round t, respectively. Let $\begin{array} { r } { R e v ( \mathcal { A } ) ~ = ~ \sum _ { t \in \left[ \tau _ { a l q } \right] } r _ { t } ( p _ { t } ) } \end{array}$ denote the total revenue collected by an algorithm A for the problem and OPT denote the benchmark. We compare our algorithms to benchmarks using the competitive ratio framework and we say the algorithm is $\beta .$ -competitive ratio if $\begin{array} { r } { R e v ( \mathcal { A } ) \ge \frac { \mathrm { O P T } } { \beta } - \overset { \cdot } { o } \left( \mathrm { O P T } \right) } \end{array}$ .

# B. Benchmarks

Here we analyze four common benchmarks for the pricing problem, then establish proper benchmarks for our work:

• Optimal dynamic policy benchmark $\scriptstyle ( \mathrm { O P T } _ { \mathrm { D P } } ) :$ is the expected revenue of the optimal policy, which is the best algorithm in hindsight and allowed to change prices arbitrarily in each round. For the theoretical analysis, as discussed in the adversarial BwK problem [8], this benchmark is too strong for our online pricing problem with limited supply and timesensitive valuations.

• Optimal fixed distribution policy benchmark $( \mathrm { O P T _ { F D } ) \mathrm { \cdot } }$ : is the expected revenue of the best fixed distribution over prices.   
• Optimal fixed price benchmark $( \mathrm { O P T } _ { \mathrm { F P } } ) { \mathrm { : } }$ is the expected revenue of best fixed price and is a very weak benchmark for our problem setting. Even if the valuations are time-invariant, it is much weaker than the fixed distribution policy for the problem of dynamic pricing with limited supply [7].   
• Offline benchmark $( \mathrm { O P T _ { O F } ) }$ : knows the valuation of each buyer in each round and is the strongest benchmark. It is easy to calculate in experiments.

For the theoretical analysis, since $\mathrm { O P T _ { D P } }$ is too strong and $\mathrm { O P T } _ { \mathrm { F P } }$ is too weak, we mainly consider the benchmark of optimal fixed distribution policy. For the experimental evaluation, we mainly consider the offline benchmark.

# C. Preadjusted Discretization

In this work, we model our online pricing problem with bandits. However, bandits framework is always defined in a finite-action space while online pricing is a continuous problem defined in an infinite-action space. Therefore, as the first step, we need to discretize the action space of pricing. In each round $t \in [ N ]$ , we assume the seller selects a price from a vector $\hat { \pmb { p } } = ( \hat { p } _ { 1 } , \hat { p } _ { 2 } , . . . , \hat { p } _ { K } )$ , which contains $K$ candidate prices satisfying $0 \le \hat { p } _ { 1 } \le \hat { p } _ { 2 } \le \dots \le \hat { p } _ { K - 1 } \le 1 < \hat { p } _ { K }$ . Each candidate price corresponds to an arm in the bandits problem. Specially, $\hat { p } _ { K }$ corresponds to the “null $\arcsin ^ { \prime \prime }$ , which is common in BwK problems, meaning zero revenue and zero consumption. Let $[ K ]$ stand for $\{ 1 , 2 , . . . , K \}$ and $\Delta _ { K }$ denote the set of all probability distributions on $[ K ]$ . We use the $\epsilon \mathrm { - }$ additive mesh for discretization, thus

$$
\hat {p} _ {k} = \epsilon k, \epsilon = \frac {1}{K - 1}. \tag {2}
$$

We will analyze the discretization error in Section III-D.

# D. Linear Relaxation

We start with the problem insnite price space S, for example, $\langle B , N , { \mathcal { F } } , { \mathcal { G } } \rangle$ ${ \hat { p } } .$ $\mathrm { O P T } _ { \mathrm { F D } } ^ { ( S ) }$ $\bar { r } _ { \tau } ( p ) \ =$ $\textstyle { \frac { 1 } { \tau } } \sum _ { t \in [ \tau ] } r _ { t } ( p )$ and $\begin{array} { r } { \bar { c } _ { \tau } ( p ) = \frac { 1 } { \tau } \sum _ { t \in [ \tau ] } c _ { t } ( p ) } \end{array}$ denote the average per-round revenue and item consumption up to an intermediate round $\tau \in [ N ]$ by offering a price p, respectively. Then we can easily extend these definitions over a price p to those over a price distribution $\begin{array} { r } { \mathcal { D } \in \Delta _ { S } \colon \bar { r } _ { \tau } ( \mathcal { D } ) = \sum _ { v \in S } \bar { r } _ { \tau } ( p ) \mathcal { D } ( p ) } \end{array}$ and $\begin{array} { r } { \bar { c } _ { \tau } ( \mathcal { D } ) = \sum _ { p \in S } \bar { c } _ { \tau } ( p ) \mathcal { D } ( p ) } \end{array}$ , where $\Delta _ { S }$ denotes the set of all probability distributions over $S$ and ${ \mathcal { D } } ( { \boldsymbol { p } } )$ denotes the probability of sampling p according to the distribution $\mathcal { D } .$ Given τ , we can find the best distribution during τ rounds by solving the following linear programming problem:

$$
\begin{array}{l} \max \quad \bar {r} _ {\tau} (\mathcal {D}) \\ \text { s.t. } \quad \mathcal {D} \in \Delta_ {S}, \tau \cdot \bar {c} _ {\tau} (\mathcal {D}) \leq B. \\ \end{array}
$$

Let $\mathrm { L P } ( B , \tau )$ denote the optimal value of this linear program. For the problem instances with S, the algorithm seeks the best distribution for all possible end-rounds and the linear relaxation of the problem could be formulated as follows:

$$
\mathrm{OPT} _ {\mathrm{LP}} ^ {(S)} := \max _ {\tau \in [ N ]} \tau \cdot \mathrm{LP} (B, \tau). \tag {4}
$$

To solve (4), we first fix the end round τ and consider a linear program $\operatorname { L P } ( B , \tau )$ , then seek the best distribution for all possible end-rounds.

In another way, considering fixing any distribution $\mathcal { D } \in \Delta _ { S }$ , we have the maximum consumption as follows:

$$
\max \quad \tau \cdot \bar {c} _ {\tau} (\mathcal {D}) \tag {5}
$$

$$
\text { s.t. } \quad \tau \in [ N ], \quad \tau \cdot \bar {c} _ {\tau} (\mathcal {D}) \leq B.
$$

Let $\mathrm { L P } ( B , { \mathcal { D } } )$ denote the the optimal value of (5), then the linear relaxation of the problem is

$$
\mathrm{OPT} _ {\mathrm{LP}} ^ {(S)} = \max _ {\mathcal {D} \in \Delta_ {S}} \mathrm{LP} (B, \mathcal {D}) \sum_ {x \in S} x \cdot \mathcal {D} (x). \tag {6}
$$

We know from [8] that:

$$
\mathrm{OPT} _ {\mathrm{LP}} ^ {(S)} \geq \mathrm{OPT} _ {\mathrm{FD}} ^ {(S)} \tag {7}
$$

Then we consider the problem instance $\langle B , N , { \mathcal { F } } , { \mathcal { G } } \rangle$ with infinite price space X. Due to the bounded support of ${ \mathcal { F } } ,$ , we assume X is bounded by the interval $[ 0 , 1 + \epsilon ]$ , where  is defined in Section III-C. We can define

$$
\mathrm{OPT} _ {\mathrm{LP}} ^ {(X)} = \sup _ {\text { finite } X ^ {\prime} \subset X} \mathrm{OPT} _ {\mathrm{LP}} ^ {(X ^ {\prime})}. \tag {8}
$$

Following discussion in BwK [7], we fix a problem instance and consider the optimal fixed distribution policy which defines a deterministic mapping from only finitely many possible histories to only finite subset $X ^ { \prime } \subset X$ , then we have

$$
\mathrm{OPT} _ {\mathrm{LP}} ^ {(X)} \geq \mathrm{OPT} _ {\mathrm{LP}} ^ {(X ^ {\prime})} \geq \mathrm{OPT} _ {\mathrm{FD}} ^ {(X ^ {\prime})} = \mathrm{OPT} _ {\mathrm{FD}} ^ {(X)} \tag {9}
$$

Therefore, we generalize (7) to the problem instance with infinite price space.

Now we analyze the discretization error caused by the preprocessing in Section III-C. We use the  − additive mesh for discretization, which is a popular type of meshes used in online pricing [7], [25], [38]. [7] provides the preadjusted discretization error analysis of the $\epsilon - a d d i t i v e$ mesh for stochastic BwK by upper-bounding the expected per-round resource consumption and lower-bounding the expected perround reward. However, the problem setting and the theoretical analysis of the discretization error in our work is different from that in [7]. We consider the discretization error for adversarial BwK by lower-bounding the expected total consumption during the time horizon.

Theorem 1. Consider the problem instance $\langle B , N , { \mathcal { F } } , { \mathcal { G } } \rangle$ with infinite price space X, which is bounded by the interval [0, 1+ $\epsilon ] .$ . Let $S \subset X$ be an -additive discretization of X. Then the discretization error

$$
E r r (S | X) = \mathrm{OPT} _ {\mathrm{LP}} ^ {(X)} - \mathrm{OPT} _ {\mathrm{LP}} ^ {(S)}
$$

is $O ( \epsilon B )$

Proof. Consider any finite subset the distribution which maximize $X ^ { \prime } \subset X$ d let . Th $\mathcal { D } _ { X ^ { \prime } }$ denoteonstruct $\mathrm { O P T } _ { \mathrm { L P } } ^ { ( X ^ { \prime } ) }$ the distribution $\mathcal { D } _ { S }$ over S such that

$$
\mathcal {D} _ {S} (x) = \sum_ {y \in [ x, x + \epsilon) \cap X ^ {\prime}} \mathcal {D} _ {X ^ {\prime}} (y), x \in S. \tag {10}
$$

Then consider $\mathrm { L P } ( B , { \mathcal { D } } _ { S } )$ and $\mathrm { L P } ( B , { \mathcal { D } } _ { X ^ { \prime } } )$ . Let $\tau ( \mathcal { D } _ { S } )$ and $\tau ( \mathcal { D } _ { X ^ { \prime } } )$ denote the optimal end-round for $\mathrm { L P } ( B , { \mathcal { D } } _ { S } )$ and $\mathrm { L P } ( B , { \mathcal { D } } _ { X ^ { \prime } } )$ , respectively. We have

$$
\mathrm{LP} (B, \mathcal {D} _ {S}) = \sum_ {t = 1} ^ {\tau (\mathcal {D} _ {S})} c _ {t} (\mathcal {D} _ {S}) \tag {11}
$$

$$
\mathrm{LP} (B, \mathcal {D} _ {X ^ {\prime}}) = \sum_ {t = 1} ^ {\tau (\mathcal {D} _ {X ^ {\prime}})} c _ {t} (\mathcal {D} _ {X ^ {\prime}}) \tag {12}
$$

Then we compare $\mathrm { L P } ( B , { \mathcal { D } } _ { S } )$ with $\mathrm { L P } ( B , { \mathcal { D } } _ { X ^ { \prime } } )$ .

$\begin{array} { r } { \sum _ { t = 1 } ^ { \cdot ( D _ { S } ) } c _ { t } ( \dot { \mathcal { D } } _ { S } ) = B . } \end{array}$

$$
\sum_ {t = 1} ^ {\tau (\mathcal {D} _ {X ^ {\prime}})} c _ {t} (\mathcal {D} _ {X ^ {\prime}}) \leq B = \sum_ {t = 1} ^ {\tau (\mathcal {D} _ {S})} c _ {t} (\mathcal {D} _ {S}) \tag {13}
$$

Case 2: Pτ(DSt=1 $\begin{array} { r } { \pmb { 2 } \colon \sum _ { t = 1 } ^ { \tau ( \mathcal { D } _ { S } ) } c _ { t } ( \mathcal { D } _ { S } ) < B } \end{array}$ . Then we have $\tau ( \mathcal { D } _ { S } ) = N$ From (10), we have $c _ { t } ( \mathcal { D } _ { X ^ { \prime } } ) \leq c _ { t } ( \mathcal { D } _ { S } )$ for all $t \in [ N ]$ . And we have $\tau ( \mathcal { D } _ { X ^ { \prime } } ) \leq N = \tau ( \mathcal { D } _ { S } )$ . Combine them together, we get (13), too.

Summarize these two cases, as well as (11) and (12), then

$$
\mathrm{LP} (B, \mathcal {D} _ {S}) \geq \mathrm{LP} (B, \mathcal {D} _ {X ^ {\prime}}).
$$

Combine it with (6), (8), and (10), we complete the proof.

In the rest of the paper, X denotes the infinite price space of interval $[ 0 , 1 + \epsilon ]$ and S denotes the finite price space of vector ${ \hat { p } } .$ Then $S \subset X$ and S is the -additive discretization of X. As the base distribution $\mathcal { F }$ has the bounded support [0, 1], combining it with (9), OPT(X)LP $\mathrm { O P T } _ { \mathrm { L P } } ^ { ( X ) }$ could bound the best fixed distribution policy benchmark over any infinite prices space.

# IV. MECHANISM FOR ESTIMATOR CASE

We start with the estimator case. In practice, the seller is very likely to have an estimate of the time-sensitive function, especially when the seller has some knowledge about items and buyers. In this section, with the estimate functions set ${ \tilde { \mathcal { G } } } ,$ we propose a novel algorithm, namely Resourceful Rotting Lagrange Algorithm (RRLA), which is detailed in Algorithm 1. Theoretical analysis shows that our algorithm achieves $O ( \log ( 1 / \alpha ) )$ competitive ratio w.r.t. the optimal fixed distribution benchmark, where α is the biased rate defined in Section III-A.

We first introduce the intuition behind our algorithm. Our algorittimate $\mathrm { O P T } _ { \mathrm { F D } } ^ { ( X ) }$ wo-phase algorithm whose main theme is to es- to guide the selection of candidate prices. The first phase (line 1-5) is the pure exploration phase where the algorithm aims to estimate OPT(X)FD $\operatorname { \mathrm { \dot { O } P T } } _ { \mathrm { F D } } ^ { ( X ) }$ roughly by constructing a picture of $\mathcal { F }$ according to $\tilde { \mathcal { G } }$ and concentration inequality, and call it ${ \tilde { \mathcal { F } } } .$ The second phase (line 6-19) is the adaptive exploitation phase where the algorithm does the explorationexploitation tradeoff to collect revenue as much as possible by guessing OPT(X)FD $\mathrm { O P T } _ { \mathrm { F D } } ^ { ( X ) }$ more precisely based on the output of the first phase and the inverse propensity scoring (IPS) technique.

Algorithm 1: RRLA   
Input: parameters n, B, η, ψ, λ, the constant α, adversarial bandits algorithm $A_{adv}$ Output: price $p_t$ 1 for phase ζ = 0, 1, ..., n - 1 do

2    for round k = 1, 2, ..., K - 1 do

3    Offer price $p_t = \min(1, \tilde{g}_{j_t}(t) \cdot \hat{p}_k / \alpha)$ ;

4 Compute $\tilde{F}$ ;

5 Compute the LP value $\widetilde{OPT}_{LP}$ according to $\tilde{F}$ , $\tilde{G}$ ;

6 Initialize $\tilde{\mathcal{R}} = \widetilde{\mathrm{OPT}}_{\mathrm{LP}}$ , $B_1 = \psi(B - Kn)$ , $B_2 = (1 - \psi)(B - Kn)$ ;

7 for each phase do

8    Initialize $B_0 = B_1 / (2 \lfloor -4 \log_\lambda \alpha \rfloor)$ , $N_0 = \tilde{\mathcal{R}} / (3 \lfloor -4 \log_\lambda \alpha \rfloor)$ , $\mathcal{D}^{(adv)}$ and start a new instance of $A_{adv}$ ;

9    Define $R_{old} := R$ ;

10    for each round in the phase do

11    Recompute $R$ ;

12    if $R > \lambda \cdot R_{old}$ then

13    Start a new phase;

14    if consumption in this phase does not exceed $B_0$ then

15 $A_{adv}$ returns the distribution over prices and use it to update $\mathcal{D}^{(adv)}$ ;

16    Return price $\hat{p}_k \in \hat{p}$ according to $\mathcal{D}^{(adv)}$ and report $\mathcal{L}_t(\hat{p}_k)$ to $A_{adv}$ ;

17    else

18    Play distribution $\mathcal{D}^{(adv)}$ with probability $\frac{B_2}{(N-t)\bar{c}(\mathcal{D}^{(adv)})}$ , offer price $p_t = \hat{p}_K$ 19    otherwise;

20    Update $B_2$ ;

We present the algorithm’s specification below. We start with the pure exploration phase. Let $n \in [ N ]$ and $[ N ] ^ { n }$ denote the n-subset of [N ]. Let $i _ { t }$ denote the index of the buyer in round t and $j _ { t }$ denote the index of the category that the buyer $b _ { i _ { t } }$ belong to. η is an arbitrary constant to balance the exploration and exploitation. Let $\tilde { \mathcal { G } }$ denote the case that we use $\tilde { g } _ { j _ { t } } ( t )$ to replace $g _ { i _ { t } } ( t )$ for all $t \in [ N ]$ . By offering price $p _ { t } = \operatorname* { m i n } ( 1 , \tilde { g } _ { j _ { t } } ( t ) \cdot \hat { p } _ { k } / \alpha )$ , define

$$
\operatorname{LCB} (p) := \max \left(0, \frac {\sum_ {t \in [ N ] ^ {n}} c _ {t} (p _ {t})}{n} - \sqrt {\frac {2 \log N}{n}}\right).
$$

For all $p ~ \in ~ \left( \widehat { p } _ { k } , \widehat { p } _ { k + 1 } \right]$ , let $\tilde { \mathcal { F } } ( p ) \ : = \ : 1 \ : - \ : \mathrm { L C B } ( \hat { p } _ { k + 1 } )$ , $k \in$ $[ K - 1 ]$ . We only need $K - 1$ rounds rather than K rounds because $\hat { p } _ { K } > 1$ and $\mathcal { F }$ has the bounded support [0, 1]. Using $\tilde { \mathcal { F } }$ and ${ \tilde { \mathcal { G } } } ,$ , our algorithm calculates the optimal distribution of $\operatorname { O P T } _ { \mathrm { L P } } ^ { ( X ) } ( \tilde { \mathcal { F } } , \tilde { \mathcal { G } } )$ and let $\tilde { \mathcal { D } }$ denote it. Then we construct a distribution $\tilde { \mathcal { D } } ^ { \prime }$ such that $\tilde { \mathcal { D } } ^ { \prime } ( \alpha x ) = \tilde { \mathcal { D } } ( x )$ . Define

$$
\widetilde {\mathrm{OPT}} _ {\mathrm{LP}} := \mathrm{LP} (B, \tilde {\mathcal {D}} ^ {\prime}) \sum_ {x} x \cdot \tilde {\mathcal {D}} ^ {\prime} (x)
$$

Then we complete the specification of the pure exploration phase.

In the adaptive exploitation phase, we use an adversary bandits algorithm $( \mathcal { A } _ { a d v } )$ as the subroutine. The adversarial algorithm updates a distribution over actions, and we assume the distribution does enough uniform exploration over arms. For the feedback, define

$$
\mathcal {L} _ {t} (\hat {p} _ {k}) = r _ {t} (\hat {p} _ {k}) + 1 - \frac {N _ {0}}{B _ {0}} c _ {t} (\hat {p} _ {k})
$$

There are many adversary bandits algorithms for bandit feedback, e.g., EXP3.P [12], which can be adopted as $\boldsymbol { A } _ { a d v } .$ We use $\tilde { \mathcal { R } }$ to denote the guess in this phase and formally define the computation of R˜ below. Let D(adv)t $\tilde { \mathcal { R } }$ $\mathbf { \hat { \mathcal { D } } } _ { t } ^ { ( a d v ) } \in \Delta _ { K }$ denote the distribution chosen by the algorithm $\mathcal { A } _ { a d v }$ in round t. We use

$$
\bar {r} _ {\tau} ^ {(\mathrm{ips})} (\hat {p} _ {k}) = \frac {1}{\tau} \sum_ {t \in [ \tau ]} \frac {\mathbf {1} _ {p _ {t} = \hat {p} _ {k}}}{\mathcal {D} _ {t} ^ {(a d v)} (\hat {p} _ {k})} r _ {t} (\hat {p} _ {k}),
$$

$$
\bar {c} _ {\tau} ^ {(\mathrm{ips})} (\hat {p} _ {k}) = \frac {1}{\tau} \sum_ {t \in [ \tau ]} \frac {\mathbf {1} _ {p _ {t} = \hat {p} _ {k}}}{\mathcal {D} _ {t} ^ {(a d v)} (\hat {p} _ {k})} c _ {t} (\hat {p} _ {k})
$$

to estimate $\bar { c } _ { \tau } ( \hat { p } _ { k } )$ and plug them into (3). Let $\mathrm { L P } ^ { \mathrm { ( i p s ) } } ( B , \tau )$ denote the optimal value of the linear program. Define

$$
[ \widetilde {t} ] = \{2 ^ {x} | x \in [ \lfloor \log t \rfloor ] \}
$$

Then the guess for round t is

$$
\tilde {\mathcal {R}} _ {t} := \max _ {\tau \in [ \widetilde {t} ]} \tau \cdot \mathrm{LP} ^ {(\mathrm{ips})} (B, \tau) \tag {14}
$$

The algorithm only computes linear program $O ( N \log N )$ times during the play, because there are at most 1+log t linear programming computations in round t. We update $B _ { 2 } = B _ { 2 } { - } 1$ if there is an item sold in line 18, to make sure that the algorithm will not run out of the inventories during the play.

Theorem 2. Consider the problem instance $\langle B , N , { \mathcal { F } } , { \mathcal { G } } \rangle$ with the set of estimate functions ${ \tilde { \mathcal { G } } } .$ . Then with probability at least $1 - O ( \delta N )$ , the expected total revenue Rev collected by Algorithm 1 satisfies

$$
R e v \geq \frac {\mathrm{OPT} _ {\mathrm{FD}} ^ {(X)}}{\log (1 / \alpha)} - O (N ^ {7 / 8}) \log (N / \delta) ^ {1 / 4}. \tag {15}
$$

The theorem is meaningful when $\mathrm { O P T } _ { \mathrm { F D } } ^ { ( X ) } > \tilde { \Omega } ( N ^ { 7 / 8 } )$

# A. Proof of Theorem 2

Through Lemma 1-4, we prove that $\mathrm { O P T } _ { \mathrm { F D } } ^ { ( X ) }$ can be estimated up to the factor α 2 $\textstyle { \frac { 1 } { \alpha ^ { 2 } } }$ after the pure exploration phase. Based on the result of Lemma $^ { 4 , }$ we prove that the revenue collected by our algorithm satisfies $O ( 1 / \alpha )$ competitive ratio w.r.t. $\mathrm { O P T } _ { \mathrm { F D } } ^ { \overline { { ( } } X ) }$ with high probability.

For the convenience of theoretical analysis, let $\eta \ : = \ : 2$ . Ideally, with G, by offering the price $p _ { t } = g _ { i _ { t } } ( t ) \cdot p$ in each round $t \in [ N ] ^ { n }$ , according to Hoeffding inequality, we have:

$$
\mathbb {P} \left\{\left| 1 - \mathcal {F} (p) - \frac {\sum_ {t \in [ N ] ^ {n}} c _ {t} \left(p _ {t}\right)}{n} \right| \leq \sqrt {\frac {2 \log N}{n}} \right\} \geq 1 - \frac {2}{N ^ {4}} \tag {16}
$$

However, we can only use the estimate function set ${ \tilde { \mathcal { G } } } .$ .

Lemma 1. For each price $p \in [ 0 , 1 ] ,$ , by offering price $p _ { t } =$ min $( 1 , \tilde { g } _ { j _ { t } } ( t ) \cdot p / \alpha )$ in each round $t \in [ N ] ^ { n }$ , it holds that

$$
\mathbb {P} \left\{1 - \mathcal {F} (p) \geq \frac {\sum_ {t \in [ N ] ^ {n}} c _ {t} \left(p _ {t}\right)}{n} - \sqrt {\frac {2 \log N}{n}} \right\} \geq 1 - \frac {1}{N ^ {4}} \tag {17}
$$

and by offering price $p _ { t } = \alpha \cdot \tilde { g } _ { j _ { t } } ( t )$ ·p in each round $t \in [ \dot { N } ] ^ { n }$ it holds that

$$
\mathbb {P} \left\{1 - \mathcal {F} (p) \leq \frac {\sum_ {t \in [ N ] ^ {n}} c _ {t} \left(p _ {t}\right)}{n} + \sqrt {\frac {2 \log N}{n}} \right\} \geq 1 - \frac {1}{N ^ {4}} \tag {18}
$$

Proof. Because $\tilde { g } _ { j _ { t } } ( t ) / \alpha \geq g _ { i _ { t } } ( t )$ for all $t \in [ N ] , \operatorname { i f } c _ { t } ( p _ { t } ) = 1$ then $c _ { t } ( g _ { i _ { t } } ( t ) \cdot p ) = 1$ . We have

$$
\frac {\sum_ {t \in [ N ] ^ {n}} c _ {t} (p _ {t})}{n} \leq \frac {\sum_ {t \in [ N ] ^ {n}} c _ {t} (g _ {i _ {t}} (t) \cdot p)}{n}, \tag {19}
$$

then plug it into (16), we have (17). Similarly, we could also prove (18). □

Lemma 2. Let $\operatorname { O P T } _ { \mathrm { L P } } ^ { ( X ) } ( \mathcal { F } , \mathcal { G } )$ and $\mathrm { O P T } _ { \mathrm { L P } } ^ { ( S ) } ( \tilde { \mathcal { F } } , \mathcal { G } )$ denote the linear relaxation of two problem instances $\langle B , N , { \mathcal { F } } , { \mathcal { G } } \rangle$ and $\langle B , N , \tilde { \mathcal { F } } , \mathcal { G } \rangle$ with prices space $X$ and S, respectively. Then with probability at least $1 - O ( N ^ { - 2 } )$ ),

$$
\mathrm{OPT} _ {\mathrm{LP}} ^ {(X)} (\tilde {\mathcal {F}}, \mathcal {G}) \geq \alpha^ {2} \cdot \mathrm{OPT} _ {\mathrm{LP}} ^ {(S)} (\mathcal {F}, \mathcal {G}) - O \left(\frac {B}{K} + N \sqrt {\frac {\log N}{n}}\right) \tag {20}
$$

Proof. Assume $\smash { \mathcal { D } ^ { * } \in \Delta _ { K } }$ is the optimal distribution of $\operatorname { O P T } _ { \mathrm { L P } } ^ { \cdot ( S ) } ( \mathcal { F } , \mathcal { G } )$ and let $\tau ^ { * }$ denote the expect end round of $\mathcal { D } ^ { * }$ . Then construct a distribution $\hat { \mathcal { D } } \in \Delta _ { K }$ such that

$$
\hat {\mathcal {D}} (y) = \sum_ {x \in \left[ \frac {y}{\alpha^ {2}}, \frac {y + \epsilon}{\alpha^ {2}}\right)} \mathcal {D} ^ {*} (x). \tag {21}
$$

Plug $\hat { \mathcal { D } }$ into the linear program (5) of problem instance $\langle B , N , \tilde { \mathcal { F } } , \mathcal { G } \rangle$ and let $\hat { \tau }$ denote the end-round $\mathrm { L P } ( B , \hat { \mathcal { D } } )$ Then we have  for the problem in $\mathbb { E } [ \hat { \tau } ~ \cdot$ $\begin{array} { r } { \bar { c } _ { \hat { \tau } } ( \hat { \mathcal { D } } ) ] = \sum _ { t = 1 } ^ { \hat { \tau } } \Big ( 1 - \tilde { \mathcal { F } } \left( \frac { \hat { \mathcal { D } } } { g _ { i _ { t } } ( t ) } \right) \Big ) } \end{array}$ $\langle B , N , \tilde { \mathcal { F } } , \mathcal { G } \rangle$ and $\begin{array} { r } { \mathbb { E } [ \tau ^ { * } \cdot \bar { c } _ { \tau ^ { * } } ( \mathcal { D } ^ { * } ) ] = \sum _ { t = 1 } ^ { \tau ^ { * } } \Big ( 1 - \mathcal { F } \left( \frac { \mathcal { D } ^ { * } } { g _ { i _ { t } } ( t ) } \right) \Big ) } \end{array}$ for the problem instance $\langle B , N , { \mathcal { F } } , { \mathcal { G } } \rangle$ . Then we have

$$
1 - \mathcal {F} \left(\frac {\mathcal {D} ^ {*}}{g _ {i _ {t}} (t)}\right) = \sum_ {x} \left(1 - \mathcal {F} \left(\frac {x}{g _ {i _ {t}} (t)}\right)\right) \mathcal {D} ^ {*} (x) \tag {22}
$$

According to Lemma 1, with probability at least $1 - O ( N ^ { - 4 } )$ , we have

$$
1 - \mathcal {F} \left(\frac {x}{g _ {i _ {t}} (t)}\right) \leq \frac {\sum_ {t \in [ N ] ^ {n}} c _ {t} \left(\frac {\alpha \tilde {g} _ {j _ {t}} (t) \cdot x}{g _ {i _ {t}} (t)}\right)}{n} + \sqrt {\frac {2 \log N}{n}} \tag {23}
$$

Because $\begin{array} { r } { \frac { \alpha \tilde { g } _ { j _ { t } } ( t ) \cdot x } { g _ { i _ { t } } ( t ) } \geq \alpha ^ { 2 } x \geq \left\lfloor \frac { \alpha ^ { 2 } x } { \epsilon } \right\rfloor \epsilon } \end{array}$ , we have

$$
\sum_ {t \in [ N ] ^ {n}} c _ {t} \left(\frac {\alpha \tilde {g} _ {j _ {t}} (t) \cdot x}{g _ {i _ {t}} (t)}\right) \leq \sum_ {t \in [ N ] ^ {n}} c _ {t} \left(\left\lfloor \frac {\alpha^ {2} x}{\epsilon} \right\rfloor \epsilon\right) \tag {24}
$$

Combine (21), (22), (23), (24) together, with probability at least $1 - O ( N ^ { - 3 } )$ ), we have

$$
1 - \mathcal {F} \left(\frac {\mathcal {D} ^ {*}}{g _ {i _ {t}} (t)}\right) \leq 1 - \tilde {\mathcal {F}} \left(\frac {\hat {\mathcal {D}}}{g _ {i _ {t}} (t)}\right) + O \left(\sqrt {\frac {\log N}{n}}\right) \tag {25}
$$

Similar with the discussion of comparing the value of two linear programming in the proof of Theorem 1 and apply a union bound, with probability at least $1 - O ( N ^ { - 2 } )$ , we have

$$
\tau^ {*} \cdot \bar {c} _ {\tau^ {*}} (\mathcal {D} ^ {*}) \leq \hat {\tau} \cdot \bar {c} _ {\hat {\tau}} (\hat {\mathcal {D}}) + O \left(N \sqrt {\frac {\log N}{n}}\right) \tag {26}
$$

Combine (2), (5), (6), (21), (26) together, we complete the proof.

Lemma 3. Let $\operatorname { O P T } _ { \mathrm { L P } } ^ { ( X ) } ( \mathcal { F } , \mathcal { G } )$ and $\operatorname { O P T } _ { \mathrm { L P } } ^ { ( X ) } ( \mathcal { F } , \tilde { \mathcal { G } } )$ denote the linear relaxation of two problem instances $\langle B , N , { \mathcal { F } } , { \mathcal { G } } \rangle$ and $\langle B , N , { \mathcal { F } } , { \tilde { \mathcal { G } } } \rangle$ , respectively. Assume that $\mathcal { D } _ { \widetilde { \mathcal { G } } } ^ { * }$ is the optimal distribution of $\operatorname { O P T } _ { \mathrm { L P } } ^ { ( X ) } ( \mathcal { F } , \tilde { \mathcal { G } } )$ . Construct a distribution $\mathcal { D } _ { \tilde { \mathcal { G } } } ^ { ' }$ such that $\mathcal { D } _ { \tilde { G } } ^ { ' } ( \alpha x ) = \mathcal { D } _ { \tilde { G } } ^ { * } ( x )$ . Then for the problem instance $\left. B , N , \mathcal { F } , \mathcal { G } \right.$ with prices space $X ,$ , it holds that

$$
\mathrm{LP} (B, \mathcal {D} _ {\tilde {\mathcal {G}}} ^ {'}) \sum_ {x} x \cdot \mathcal {D} _ {\tilde {\mathcal {G}}} ^ {'} (x) \geq \alpha^ {2} \cdot \mathrm{OPT} _ {\mathrm{LP}} ^ {(X)} (\mathcal {F}, \mathcal {G}) \tag {27}
$$

Proof. Assume $\operatorname { O P T } _ { \mathrm { L P } } ^ { ( X ) } ( \mathcal { F } , \mathcal { G } )$ and let ${ \mathcal { D } } ^ { * }$ is the optimal distribution of $\tau ^ { * }$ denote the optimal end round of $\mathcal { D } ^ { * }$ . Construct a distribution $\mathcal { D } ^ { \prime }$ such that ${ \mathcal { D } } ^ { \prime } ( \alpha x ) = { \mathcal { D } } ^ { * } ( x )$ and a new function set $\mathcal { G } _ { \alpha } ~ = ~ \{ \alpha \cdot g _ { i } | g _ { i } ~ \in ~ \mathcal { G } \}$ . Consider the problem instance $\langle B , N , { \mathcal { F } } , { \mathcal { G } } _ { \alpha } \rangle$ and its linear relaxation OPT(X)( $\mathrm { O P T } _ { \mathrm { L P } } ^ { ( X ) } ( { \mathcal F } , { \mathcal G } _ { \alpha } )$ . Notand that is t $\mathcal { D } ^ { \prime }$ is the optimal distribuoptimal end round of n of, so OPT(X)LP $\operatorname { O P T } _ { \mathrm { L P } } ^ { ( X ) } ( { \mathcal { F } } , { \mathcal { G } } _ { \alpha } )$ $\tau ^ { * }$ $\mathcal { D } ^ { \prime } .$ we have

$$
\mathrm{OPT} _ {\mathrm{LP}} ^ {(X)} (\mathcal {F}, \mathcal {G} _ {\alpha}) = \alpha \cdot \mathrm{OPT} _ {\mathrm{LP}} ^ {(X)} (\mathcal {F}, \mathcal {G}) \tag {28}
$$

Then consider problem instance $\langle B , N , { \mathcal { F } } , { \tilde { \mathcal { G } } } \rangle$ . Let $\tau ( \mathcal { D } ^ { \prime } )$ denote the optimal end round such that maximize $\mathrm { L P } ( B , { \mathcal { D } } ^ { \prime } )$ . Let $c _ { t } ( \tilde { \mathcal { G } } , \mathcal { D } ^ { \prime } )$ and $c _ { t } ( \mathcal { G } _ { \alpha } , \mathcal { D } ^ { \prime } )$ denote the consumption by play distribution $\dot { \mathcal { D } } ^ { \prime }$ in round t for problem instance $\langle B , N , { \mathcal { F } } , { \tilde { \mathcal { G } } } \rangle$ and $\langle B , N , { \mathcal { F } } , { \mathcal { G } } \rangle$ , respectively. We have

$$
\sum_ {t = 1} ^ {\tau (\mathcal {D} ^ {\prime})} c _ {t} (\tilde {\mathcal {G}}, \mathcal {D} ^ {\prime}) \geq \sum_ {t = 1} ^ {\tau^ {*}} c _ {t} (\mathcal {G} _ {\alpha}, \mathcal {D} ^ {\prime}) \tag {29}
$$

Combine (29) with (4), we have

$$
\mathrm{OPT} _ {\mathrm{LP}} ^ {(X)} (\mathcal {F}, \tilde {\mathcal {G}}) \geq \mathrm{OPT} _ {\mathrm{LP}} ^ {(X)} (\mathcal {F}, \mathcal {G} _ {\alpha})
$$

Then according to (28), we have

$$
\mathrm{OPT} _ {\mathrm{LP}} ^ {(X)} (\mathcal {F}, \tilde {\mathcal {G}}) \geq \alpha \cdot \mathrm{OPT} _ {\mathrm{LP}} ^ {(X)} (\mathcal {F}, \mathcal {G}) \tag {30}
$$

Let $\tau _ { \tilde { \mathcal { G } } }$ denote the optimal end round of $\operatorname { O P T } _ { \mathrm { L P } } ^ { ( X ) } ( \mathcal { F } , \tilde { \mathcal { G } } )$ Let $\tau _ { \tilde { \mathcal { G } } } ^ { \prime }$ denote the optimal end round such that maximize $\mathrm { L P } ( \tilde { B , } \tilde { \mathcal { D } _ { \tilde { \mathcal { G } } } } )$ . Let $c _ { t } ( \tilde { \mathcal { G } } , \mathcal { D } _ { \tilde { \mathcal { G } } } ^ { * } )$ and $c _ { t } ( \mathcal { G } , \mathcal { D } _ { \tilde { \mathcal { G } } } ^ { ' } )$ denote the consumption by play distribution $\mathcal { D } _ { \tilde { \mathcal { G } } } ^ { * }$ and $\mathcal { D } _ { \tilde { \mathcal { G } } } ^ { ' }$ in round t for problem instance $\langle B , N , { \mathcal { F } } , { \tilde { \mathcal { G } } } \rangle$ and $\langle B , N , { \mathcal { F } } , { \mathcal { G } } \rangle$ , respectively. We have

$$
\sum_ {t = 1} ^ {\tau_ {\tilde {\mathcal {G}}} ^ {\prime}} c _ {t} (\mathcal {G}, \mathcal {D} _ {\tilde {\mathcal {G}}} ^ {\prime}) \geq \sum_ {t = 1} ^ {\tau_ {\tilde {\mathcal {G}}}} c _ {t} (\tilde {\mathcal {G}}, \mathcal {D} _ {\tilde {\mathcal {G}}} ^ {*}) \tag {31}
$$

Combine (31) with (4), we have

$$
\mathrm{LP} (B, \mathcal {D} _ {\tilde {\mathcal {G}}} ^ {\prime}) \sum_ {x} x \cdot \mathcal {D} _ {\tilde {\mathcal {G}}} ^ {\prime} (x) \geq \alpha \cdot \mathrm{OPT} _ {\mathrm{LP}} ^ {(X)} (\mathcal {F}, \tilde {\mathcal {G}}) \tag {32}
$$

Combine (30) with (32), we complete the proof.

![](images/b5fba6dc38c3928e5763aa639f4ea48b3c8a9a819341492fa800aa8f42fa7083.jpg)

Lemma 4. For the problem instance $\langle B , N , { \mathcal { F } } , { \mathcal { G } } \rangle$ with prices space $X ,$ , with probability at least $1 - O ( N ^ { - 2 } )$ , we have

$$
\mathrm{OPT} _ {\mathrm{FD}} ^ {(X)} \in \left[ \widetilde {\mathrm{OPT}} _ {\mathrm{LP}}, \frac {\widetilde {\mathrm{OPT}} _ {\mathrm{LP}}}{\alpha^ {4}} + O \left(\frac {B}{K} + N \sqrt {\frac {\log N}{n}}\right) \right]
$$

Proof. From the construction of $\tilde { \mathcal { D } } ^ { \prime }$ , we know that it is also $\mathrm { O P T } _ { \mathrm { F D } } ^ { ( X ) }$ ution in the price space X. We have . According to Theorem 1, Lemma 2, $\widetilde { \mathrm { O P T } } _ { \mathrm { L P } } \leq$ $^ { 3 , }$ we have $\begin{array} { r } { \mathrm { O P T } _ { \mathrm { F D } } ^ { ( X ) } \leq \frac { \widetilde { \mathrm { O P T } } _ { \mathrm { L P } } } { \alpha ^ { 4 } } + O \left( \frac { B } { K } + N \sqrt { \frac { \log N } { n } } \right) } \end{array}$ . Then we complete the proof.

Then we prove Theorem 2.

We first prove the algorithm will not run out of the inventories during the play. Forthe algorithm costs at most $K n$ pure exploitems. If $\mathrm { O P T } _ { \mathrm { F D } } ^ { ( { \dot { X } } ) } >$ $\begin{array} { r } { \tilde { \Omega } \left( \frac { B } { K } + N \sqrt { \frac { \log N } { n } } \right) } \end{array}$ , during the adaptive exploitation phase, there are at most $1 ^ { ' } - 4 \lfloor \log _ { \lambda } \alpha \rfloor$ sub-phases according to the stopping condition and Lemma 4. Define

$$
\Lambda := 1 - \left\lfloor 4 \log_ {\lambda} \alpha \right\rfloor \tag {33}
$$

Then the adversarial algorithm $\mathcal { A } _ { a d v }$ consumes at most $\psi ( B -$ $K n )$ items. Additional consumption in Algorithm 1 line 18 be bounded by $( 1 - \psi ) ( B - K n )$ because of the update of $B _ { 2 } .$ . The sum consumption of two phases is at most B during the play.

Then we prove that $\tilde { \mathcal { R } } _ { t }$ will converge to $\mathrm { O P T } _ { \mathrm { F D } } ^ { ( S ) }$ with high probability. We start with the following equation

$$
\mathcal {R} _ {t} ^ {*} := \max _ {\tau \in [ t ]} \tau \cdot \mathrm{LP} ^ {(\mathrm{ips})} (B, \tau) \tag {34}
$$

and let D(ips) $\mathcal { D } _ { t } ^ { \mathrm { ( i p s ) } }$ and $\tau _ { t } ^ { \mathrm { ( i p s ) } }$ denote the optimal distribution and optimal end-round for it, respectively. Then we consider round t. Notice that $\mathcal { D } _ { t } ^ { \mathrm { ( i p s ) } }$ is a feasible distribution for $\mathrm { L P } ^ { \mathrm { ( i p s ) } } ( B , 2 ^ { \lfloor \log \tau _ { t } ^ { \mathrm { ( i p s ) } } \rfloor } )$ t), we have

$$
\tilde {\mathcal {R}} _ {t} \geq 2 ^ {\lfloor \log \tau_ {t} ^ {(\mathrm{ips})} \rfloor} \cdot \mathrm{LP} ^ {(\mathrm{ips})} (B, 2 ^ {\lfloor \log \tau_ {t} ^ {(\mathrm{ips})} \rfloor}) \geq \frac {1}{2} \mathcal {R} _ {t} ^ {*} \tag {35}
$$

The optimal distribution and optimal end-round for (14) is also feasible for (34), then we have

$$
\tilde {\mathcal {R}} _ {t} \leq \mathcal {R} _ {t} ^ {*} \tag {36}
$$

Define

$$
\Phi := O \left(\frac {K N ^ {7 / 4}}{B} \sqrt {\log \frac {N}{\delta}}\right) \tag {37}
$$

And define

$$
\mathrm{OPT} _ {\mathrm{LP}} ^ {[ \tau ]} := \max _ {t \in [ \tau ]} t \cdot \mathrm{LP} (B, t)
$$

From [8], assume $\delta > \Omega ( N ^ { - 3 } )$ , then with probability at least $1 - \delta N$ it holds that

$$
\forall \tau \in [ N ], | \mathcal {R} _ {\tau} ^ {*} - \mathrm{OPT} _ {\mathrm{LP}} ^ {[ \tau ]} | \leq \Phi \tag {38}
$$

Combine (35), (36), (38) together, we have

$$
\forall \tau \in [ N ], | \tilde {\mathcal {R}} _ {\tau} - \mathrm{OPT} _ {\mathrm{LP}} ^ {[ \tau ]} | \leq \frac {1}{2} \mathcal {R} _ {\tau} ^ {*} + \Phi \tag {39}
$$

Case 1: The stopping condition $\tilde { \mathcal { R } } > \lambda \cdot \tilde { \mathcal { R } } _ { o l d }$ has been fired during the game. Consider the last sub-phase whose stopping condition has fired, and let $t _ { 1 }$ and $t _ { 2 }$ denote the index of the start-round and end-round of this sub-phase. Let $\begin{array} { r } { { \bar { r } } _ { [ t _ { 1 } , t _ { 2 } ] } ( { \mathcal D } ) ~ = ~ \frac { 1 } { t _ { 2 } - t _ { 1 } + 1 } \sum _ { t = t _ { 1 } } ^ { t _ { 2 } } r _ { t } ( { \mathcal D } ) } \end{array}$ and $\bar { c } _ { [ t _ { 1 } , t _ { 2 } ] } ( \mathcal { D } ) ~ =$ $\begin{array} { r } { \frac { 1 } { t _ { 2 } - t _ { 1 } + 1 } \sum _ { t = t _ { 1 } } ^ { t _ { 2 } } c _ { t } ( \mathcal { D } ) } \end{array}$ t2 denote the average per-round revenue and consumption in the rounds interval $[ t _ { 1 } , t _ { 2 } ]$ by playing distribution D, respectively. Consider the following linear program

$$
\max \quad \bar {r} _ {[ t _ {1}, t _ {2} ]} (\mathcal {D}) \tag {40}
$$

$$
\mathrm{s.t.} \quad \mathcal {D} \in \Delta_ {S}, \tau \cdot \bar {c} _ {[ t _ {1}, t _ {2} ]} (\mathcal {D}) \leq B
$$

Let $\mathrm { L P } ( B , [ t _ { 1 } , t _ { 2 } ] )$ denote the optimal value of this linear program. According to (39), we have

$$
\mathrm{LP} (B, [ t _ {1}, t _ {2} ]) \geq \tilde {\mathcal {R}} _ {t _ {2}} - 2 \tilde {\mathcal {R}} _ {t _ {1}} - \Phi \tag {41}
$$

Because the stopping condition has been fired, we get

$$
\frac {\mathrm{LP} (B , [ t _ {1} , t _ {2} ])}{\tilde {\mathcal {R}} _ {N}} \geq \left(\frac {1}{\lambda} - \frac {2}{\lambda^ {2}}\right) - \frac {\Phi}{\tilde {\mathcal {R}} _ {N}} \tag {42}
$$

Combine (39), (42) together, we get

$$
\mathrm{LP} (B, [ t _ {1}, t _ {2} ]) \geq \left(\frac {1}{2 \lambda} - \frac {1}{\lambda^ {2}}\right) \mathrm{OPT} _ {\mathrm{LP}} ^ {(S)} - \Phi \tag {43}
$$

According to [8], using algorithm EXP3.P with uniform exploration parameter $N ^ { \overline { { - } } 1 / \overline { { 4 } } }$ for $\mathcal { A } _ { a d v }$ , we have

$$
\sum_ {t = t _ {1}} ^ {t _ {2}} r _ {t} (p _ {t}) \geq \frac {\psi (B - K n)}{\Lambda} \min \left(\frac {\tilde {\mathcal {R}} _ {t _ {1}}}{3}, \mathrm{LP} (B, [ t _ {1}, t _ {2} ]) - \frac {\tilde {\mathcal {R}} _ {t _ {1}}}{3}\right)
$$

$$
- \Phi \sqrt {K} \tag {44}
$$

From the stop condition and Eq. (39), we have

$$
\tilde {\mathcal {R}} _ {t _ {1}} \geq \frac {1}{2 \lambda^ {2}} \mathrm{OPT} _ {\mathrm{LP}} ^ {(S)} - \Phi \tag {45}
$$

Combine Theorem 1, (33), (37), (43), (44), (45) together, we get (15).

Case 2: The stopping condition $\tilde { \mathcal { R } } > \lambda \cdot \tilde { \mathcal { R } } _ { o l d }$ has not been fired during the game. Let $t _ { 1 } = K n + 1$ and $t _ { 2 } = N$ . We could easily deduce that

$$
\mathrm{LP} (B, \left[ t _ {1}, t _ {2} \right]) \geq \frac {B - K n}{B} \mathrm{OPT} _ {\mathrm{LP}} ^ {(S)} \tag {46}
$$

Because the stopping condition has not been fired, according to (39), we have

$$
\tilde {\mathcal {R}} _ {t _ {1}} \geq \frac {1}{2 \lambda} \mathrm{OPT} _ {\mathrm{LP}} ^ {(S)} - \Phi \tag {47}
$$

Combine Theorem 1, (33), (37), (44), (46), (47) together, we get (15).

# V. MECHANISM FOR NON-ESTIMATOR CASE

When the seller knows nothing about the base distribution $\mathcal { F }$ and the time-sensitive function set G, to solve this problem, we model it as an adversarial BwK optimization by discretizing the price space and considering each candidate price as an arm. [8] designs an algorithm achieving $O ( d \cdot \log T )$ competitive ratio relative to optimal fixed distribution benchmark with high probability for adversarial BwK with time horizon $T$ and d limited resource. [9] improves the competitive ratio to $O ( \log d \cdot \log T )$ . Based on the high-probability algorithm in [8], by modifying the range of the guess of $\mathrm { O P T } _ { \mathrm { F D } } ^ { ( { \cal \breve { S } } ) }$ to [0, B] and taking the discretization error into consideration, there is an algorithm achieving tight ${ \cal O } ( \log B )$ competitive ratio.

Theorem 3. Consider the problem instance $\langle B , N , { \mathcal { F } } , { \mathcal { G } } \rangle$ , by transforming the problem to an adversarial BwK and using the high-probability algorithm in $I 8 J ,$ , with probability at least $1 - O ( \delta N )$ the total revenue is:

$$
R e v \geq \frac {\mathrm{OPT} _ {\mathrm{FD}} ^ {(X)}}{O (\log B)} - O (N ^ {7 / 8}) \log (N / \delta) ^ {1 / 4}.
$$

The theorem is meaningful when OPT $\begin{array} { r } {  { \mathcal { N } } _ { \mathrm { F D } } ^ { ( X ) } > \tilde { \Omega } ( N ^ { 7 / 8 } ) . } \end{array}$

Proof. From [8], using EXP3.P [12] as $\mathcal { A } _ { a d v }$ , with uniform exploration parameter $N ^ { - 1 / 4 }$ , with probability at least $1 - O ( \delta N )$ the total revenue obtained the high-probability algorithm in [8] is:

$$
R e v \geq O \left(\frac {1}{\text {ratio}}\right) \mathrm{OPT} _ {\mathrm{FD}} ^ {(S)} - O \left(\frac {K N ^ {7 / 4}}{B}\right) \sqrt {\log \frac {N}{\delta}}
$$

One idea of the algoproblem the ratio is ${ \cal O } ( \log B )$ imilar to “doublin because we have $\mathrm { \bar { o r } T } _ { \mathrm { F D } } ^ { ( X ) } \le B$ Combine it with theorem 1 we complete the proof. □

# VI. COMPETITIVE RATIO LOWER BOUNDS

We prove the $\Omega ( \log ( 1 / \alpha ) )$ and $\Omega ( \log B )$ lower bounds w.r.t the best fixed distribution benchmark for estimator case and non-estimator case, respectively.

Theorem 4. Consider any randomized algorithm for the problem instance $\langle B , N , { \mathcal { F } } , { \mathcal { G } } \rangle$ without knowing $\mathcal { F }$ and G and let $R e v ( { \cal A } )$ represent its expected total revenue.

1) For estimator case, we have $\mathrm { O P T } _ { \mathrm { F D } } ^ { ( X ) } / R e v ( { \cal A } ) \geq$ $\Omega ( \log ( 1 / \alpha ) )$ for some problem instance.   
2) For non-estimator case, we have $\mathrm { O P T } _ { \mathrm { F D } } ^ { ( X ) } / R e v ( \mathcal { A } ) \geq$ Ω(log B) for some problem instance.

Proof. We start with the non-estimator case and the idea of estimator case’s analysis is similar.

There are ω problem instances $\mathcal { I } _ { m } : \langle B , N , \mathcal { F } , \mathcal { G } ^ { ( m ) } \rangle$ and they have same B, N and $\mathcal { F }$ and different G. Let $B = 2 ^ { \omega } , N =$ $B ^ { 2 }$ . Construct $\mathcal { F }$ as the following: the buyer’s original value for an item is $\begin{array} { r } { v _ { j } = \frac { 2 ^ { \frac { j - 1 } { 2 } } } { 2 ^ { j } - 1 } } \end{array}$ with probability $\frac { 1 } { 2 ^ { \omega - j + 1 } } , j \in [ \omega ]$ , and $v = 0$ with the remaining probability. Considering the problem instance without time sensitive function, notice that it only make sense to offer price $p _ { j } = v _ { j }$ , then the expected per-round revenue and expected per-round consumption by offering price $\begin{array} { r } { p _ { j } = \frac { 2 ^ { \frac { j - 1 } { 2 } } } { 2 ^ { j } - 1 } } \end{array}$ j− are and , $r ( p _ { j } ) = 2 ^ { \frac { j - 2 \omega - 1 } { 2 } }$ $\begin{array} { r } { c ( p _ { j } ) = \frac { 2 ^ { j } - 1 } { 2 ^ { \omega } } , \forall j \in [ \omega ] } \end{array}$ respectively. Then for each instance $\mathcal { I } _ { m } , m \in [ \omega ]$ , assume $\begin{array} { r } { \tau _ { m } = \lceil \frac { \bar { N } } { 2 ^ { m } - 1 } \rceil } \end{array}$ . If round $t \leq \tau _ { m } , g _ { i _ { t } } ( t ) = 1$ , and if round $t > \tau _ { m } , g _ { i _ { t } } ( t ) = 0$ .

For each instance $\mathcal { I } _ { m }$ , there is a policy $\pi _ { m }$ that offers a fixed price $p _ { j }$ and $j ~ = ~ m$ . Follow [11], we have $p _ { j } B ~ - ~ O ( p _ { j } \sqrt { B \log B } ) ~ \leq ~ R e v ( \pi _ { m } ) ~ \leq ~ p _ { j } B$ . Of course, $\mathrm { O P T } _ { \mathrm { F D } } \geq R e v ( \pi _ { m } )$ . Then fix any randomized algorithm ${ \mathcal { A } } ,$ we will prove that there is at least one instance $\mathcal { I } _ { m } .$ , it has the competitive ratio $R e v ( \pi _ { m } ) / R e v ( A ) \geq \Omega ( \log B )$ .

Note that, algorithm A could not collect any revenue after the round $\tau _ { m }$ for the problem instance $\mathcal { I } _ { m } .$ . For a thought experiment, consider a version of A that could “ignore” the time sensitive function, which means it could still collect revenue after $\tau _ { m }$ . We call it $\mathcal { A } ^ { \prime } .$ , then A is a “part” of $\mathcal { A } ^ { \prime } \colon$ for each problem instance $\mathcal { I } _ { m }$ , the expected revenue of $\mathcal { A }$ is equal to the expected revenue of A0 for the first $\tau _ { m }$ rounds.

Fix any algorithm ${ \mathcal A } ^ { \prime } ,$ , it only makes sense to offer price $p _ { j } , ~ j ~ \in ~ [ \omega ]$ for each round $t \in \ [ N ]$ . So for each round, $\mathcal { A } ^ { \prime }$ plays a distribution over $\pi _ { m }$ . Observe that $\mathcal { A } ^ { \prime \prime } \mathrm { s }$ expected consumption is $O ( B )$ in N rounds. Algorithm $\mathcal { A } ^ { \prime }$ stops once B items are sold at some round $\tau _ { A ^ { \prime } } \leq N$ . Consider the total consumption of $\mathcal { A } ^ { \prime }$ when it offers price $p _ { j }$ over the total time horizon and let $c _ { j }$ denote it. Let’s start with problem instance $\mathcal { I } _ { 1 }$ . If $R e v ( \pi _ { 1 } ) / R e v ( A ^ { \prime } ) < \Omega ( \log B )$ , then $\begin{array} { r } { c _ { 1 } > \Omega \left( \frac { B } { \log B } \right) } \end{array}$ or $\begin{array} { r } { c _ { 2 } > \Omega \left( \frac { B } { \log B } \right) } \end{array}$ ... Notice that this sequence is not infinite because the $\dot { p } _ { j }$ is falling exponentially and the inventories is limited. Then we extend it to all problem instances $\mathcal { I } _ { m }$ , there have to exist $\begin{array} { r } { c _ { k } > \Omega \left( \frac { B } { \log B } \right) , k \in [ \omega ] } \end{array}$ and $| k - m | < c ,$ where c is $O ( 1 )$ . Then the total consumption would exceed $B ,$ which leads to a contradiction. And we complete the proof for the non-estimator case.

For the estimator case, we provide the core constructions below. There are ω problem instances $\mathcal { I } _ { m } : \langle B , N , \mathcal { F } , \mathcal { G } ^ { ( m ) } \rangle$ i with different $\tilde { \mathcal { G } } ^ { ( m ) }$ . Let $\begin{array} { r } { \omega = \big \lceil \frac { 1 } { \alpha ^ { 2 } } \big \rceil , B = C \cdot 2 ^ { \omega } , N = C } \end{array}$ · $2 ^ { 2 \omega }$ and $C$ is a large enough constant. Construct $\mathcal { F }$ as the following: the buyer’s original value for an item is $\begin{array} { r } { v _ { j } = \frac { 2 ^ { \frac { j - 1 } { 2 } } } { 2 ^ { j } - 1 } } \end{array}$ with probability $\frac { 1 } { 2 ^ { \omega - j + 1 } } , j \in [ \omega ]$ , and $v = 0$ with the remaining probability. And for each instance $\mathcal { I } _ { m } , m \in [ \omega ]$ , assume $\tau _ { m } =$ $\left\lceil { \frac { N } { 2 ^ { m } - 1 } } \right\rceil$ l N2m−1 m. If round t ≤ τm, git (t) = 1, gjt = α, and if round $t \leq \tau _ { m } , g _ { i _ { t } } ( t ) = 1 , g _ { j _ { t } } = \alpha$ $i > \tau _ { m } ; g _ { i _ { t } } ( t ) = \alpha ^ { 2 } , g _ { j _ { t } } = \alpha .$ .

# VII. NUMERICAL EVALUATIONS

We conduct a series of experiments to compare our algorithm with a set of widely used or state-of-the-art algorithms including: UCB1 [10], CappedUCB [11], EXP3.P [12]. UCB1 is one of the most popular MAB algorithms, which always chooses the optimal arm based on optimistic estimates. CappedUCB is designed for the dynamic pricing problem with limited supply and it is an index-based bandit-style algorithm. EXP3.P solves the problem of bandits optimization in adversary environments. We also compare the revenue to $\mathrm { O P T _ { O F } }$ , which is the sum of the largest B valuations of N buyers.

Let $f ( t )$ denote the estimate function and for each buyer $b _ { i } .$ , we set $g _ { i } ( t ) ~ = ~ \alpha _ { i } f ( t )$ . We set $\alpha ~ = ~ 0 . 9$ and $\alpha _ { i }$ is uniformly sampled from α to $1 / \alpha$ . We consider four different kinds of time-sensitive functions: a linear decreasing function $\begin{array} { r } { f ( t ) = 1 - \frac { t - 1 } { N } } \end{array}$ , a linear increasing function $\begin{array} { r } { f ( t ) = \frac { t - 1 } { N } } \end{array}$ t−1N , an exponential decreasing function $f ( t ) = ( 1 - 5 \times 1 0 ^ { - 4 } ) ^ { t } .$ and an exponential increasing function $f ( t ) = 1 - ( 1 - 5 \times 1 0 ^ { - 4 } ) ^ { t }$ , $t \in [ N ]$ . The original valuations range from 0 to 1, which are drawn from a Gaussian distribution $\mathcal { F }$ with $\mathcal { N } ( 0 . 7 , 0 . 1 ^ { 2 } )$ . There are $1 \times 1 0 ^ { 4 }$ items and $1 0 ^ { 5 }$ time slots. We set $K = 5 1$ for the discretization and use the -additive mesh as described in Section III-C. We use EXP3.P as subroutine and set $\gamma = 0 . 0 1$ for the subroutine. Other parameters are: $n = 5 0 , \eta = 0 .$ , $\psi = 1 , \lambda = 3$ for RRLA, c = 2 for UCB1, $\alpha = 0 . 4 ( \log N )$ for CappedUCB, $\gamma = 0 . 0 1$ for EXP3.P. All results are the averages over 20 runs. Figure 1 shows that the overall performance of our algorithm is superior to all other three algorithms , and significantly outperforms other algorithms when the time function are increasing. We show the results and briefly analysis it below.

![](images/a8cc286a025855f2fb93809416e7961504162629fbca78432549045dd1b349b0.jpg)



![](images/426dc90be4715e0b60699ed7db14fa4fb9e96407da9aa226de6c63f98612ede5.jpg)



![](images/9c0d075e04fe8042c96cd2a2448c6934a1482dc44873f55d5c7c3e9d1aec3d16.jpg)



![](images/6f170f2ef677323fe2fc2bee2aef397c369834813167b1d1d69acb7c9adb5b7c.jpg)



![](images/dfa19abacf3d09a3dbb6d97972ca42c957b1c8dbbf171073a6e717d731472bd0.jpg)



![](images/82227a50a134079208b5021752ddb392ba33ac4b69ef3216600eff52c6433ffa.jpg)



![](images/d10235aec7a4cd5da08b8e123518a8dddb70c3c97a5cc83e0a5547499455ce1a.jpg)



![](images/77c101e3894da099e77780348e91558bdd4e47f796cf2d52916ae518c0760472.jpg)



Fig. 1. Performance comparisons for (a) linear decreasing function with Gaussian distribution; (b) linear increasing function with Gaussian distribution; (c) exponential decreasing function with Gaussian distribution; (d) exponential increasing function with Gaussian distribution; (e) linear decreasing function with uniform distribution; (f) linear increasing function with uniform distribution; (g) linear and exponential decreasing functions with Gaussian distribution; (h) linear and exponential increasing functions with Gaussian distribution.

a) Different time-sensitive functions: For the linear decreasing function, our algorithm achieves 76.34% and 127.7% total revenue w.r.t. $\mathrm { O P T _ { O F } }$ and UCB1 (Figure 1(a)); for the linear increasing function, our algorithm achieves 71.99% and 352.2% total revenue w.r.t. $\mathrm { O P T _ { O F } }$ and UCB1 (Figure 1(b)); for the exponential decreasing function, our algorithm achieves 64.30% and 118.7% total revenue w.r.t. the offline benchmark and UCB1(Figure 1(c)); for the exponential increasing function, our algorithm achieves 70.76% and 121.4% total revenue w.r.t. the offline benchmark and CappedUCB (Figure 1(d)). From the results, we observe that CappedUCB can not adapt to time-sensitive valuations well; UCB1 is relatively more robust but still performs worse than our algorithm; EXP3.P consumes items too fast under the resource constraint.   
b) Different valuation distributions: Keeping other setting of Figure 1(a)-(b) unchanged, Figure 1(e)-(f) present the results when the original valuations are drawn from a uniform distribution. For the linear decreasing function, our algorithm achieves 72.23% and 152.5% total revenue w.r.t. $\mathrm { O P T _ { O F } }$ and UCB1 (Figure 1(e)); for the linear increasing function, our algorithm achieves 68.69% and 299.9% total revenue w.r.t. the offline benchmark and UCB1(Figure 1(f)). Overall, our algorithm still performs better than other three algorithms.

c) Buyers with two categories: Figure $1 ( \mathrm { g } ) \substack { \mathrm { - } } ( \mathrm { h } )$ show the cases with two categories: all buyers can be divided into two categories $\mathcal { T } _ { 1 } , \mathcal { T } _ { 2 }$ . We assign one buyer to $\mathcal { T } _ { 1 }$ with probability 0.5, similar with $\mathcal { T } _ { 2 }$ . So there are two kinds of estimate timesensitive functions. For the linear and exponential decreasing functions, our algorithm achieves 73.79% and 136.1% total revenue w.r.t. $\mathrm { O P T _ { O F } }$ and UCB1 (Figure 1(g)); for the linear increasing function, our algorithm achieves 76.53% and 135.7% total revenue w.r.t. the offline benchmark and CappedUCB(Figure 1(h)). The results show that our algorithm works robustly for different environments.

# VIII. CONCLUSION

We design online pricing mechanisms with limited supply and unknown time-sensitive valuations to maximize the total revenue. For the estimator case, we prove the $\Omega ( \log ( 1 / \alpha ) )$ lower bound w.r.t. the optimal fixed distribution benchmark and design an algorithm achieving tight $O ( \log ( 1 / \alpha ) )$ competitive ratio. For the non-estimator case, we prove the Ω(log B) lower bound and show that there is an algorithm achieving tight ${ \cal O } ( \log B )$ competitive ratio by modeling the problem as an adversarial bandits with knapsacks optimization. Simulation results testify the efficiency of our algorithms.

# ACKNOWLEDGMENTS

Xiang-Yang Li and Lan Zhang are the corresponding authors. The research is supported by National Key R&D Program of China 2018YFB0803400, China National Funds for Distinguished Young Scientists with No.61625205, China National Natural Science Foundation with No. 61822209, No. 62132018, No. 61932016, Key Research Program of Frontier Sciences, CAS. No. QYZDY-SSW-JSC002, The University Synergy Innovation Program of Anhui Province with No. GXXT-2019-024.

# REFERENCES

[1] Z. Hu and J. Zhang, “Optimal posted-price mechanism in microtask crowdsourcing.” in IJCAI, 2017.   
[2] H. Sumita, Y. Kawase, S. Fujita, T. Fukunaga, and R. Center, “Online optimization of video-ad allocation.” in IJCAI, 2017.   
[3] Z. Zheng, Y. Peng, F. Wu, S. Tang, and G. Chen, “An online pricing mechanism for mobile crowdsensing data markets,” in MobiHoc, 2017.   
[4] F. Wu, J. Liu, Z. Zheng, and G. Chen, “A strategy-proof online auction with time discounting values.” in AAAI, 2014.   
[5] L. Xu, C. Jiang, Y. Qian, Y. Zhao, J. Li, and Y. Ren, “Dynamic privacy pricing: A multi-armed bandit approach with time-variant rewards,” IEEE Transactions on Information Forensics and Security, vol. 12, no. 2, pp. 271–285, 2016.   
[6] W. Mao, Z. Zheng, F. Wu, and G. Chen, “Online pricing for revenue maximization with unknown time discounting valuations.” in IJCAI, 2018.   
[7] A. Badanidiyuru, R. Kleinberg, and A. Slivkins, “Bandits with knapsacks,” in FOCS, 2013.   
[8] N. Immorlica, K. A. Sankararaman, R. Schapire, and A. Slivkins, “Adversarial bandits with knapsacks,” in FOCS, 2019.   
[9] T. Kesselheim and S. Singla, “Online learning with vector costs and bandits with knapsacks,” in COLT, 2020.   
[10] P. Auer, N. Cesa-Bianchi, and P. Fischer, “Finite-time analysis of the multiarmed bandit problem,” Machine learning, vol. 47, no. 2-3, pp. 235–256, 2002.   
[11] M. Babaioff, S. Dughmi, R. Kleinberg, and A. Slivkins, “Dynamic pricing with limited supply,” ACM Transactions on Economics and Computation, vol. 3, no. 1, pp. 1–26, 2015.   
[12] P. Auer, N. Cesa-Bianchi, Y. Freund, and R. E. Schapire, “The nonstochastic multiarmed bandit problem,” SIAM journal on computing, vol. 32, no. 1, pp. 48–77, 2002.   
[13] M.-Y. Kao, X.-Y. Li, and W. Wang, “Towards truthful mechanisms for binary demand games: A general framework,” in EC, 2005, pp. 213–222.   
[14] P. Xu and X.-Y. Li, “Tofu: Semi-truthful online frequency allocation mechanism for wireless networks,” IEEE/ACM Transactions on Networking, vol. 19, no. 2, pp. 433–446, 2010.   
[15] H. Huang, Y.-e. Sun, X.-Y. Li, Z. Chen, W. Yang, and H. Xu, “Nearoptimal truthful spectrum auction mechanisms with spatial and temporal reuse in wireless networks,” in MobiHoc, 2013, pp. 237–240.   
[16] L. Zhang, X.-Y. Li, J. Lei, J. Sun, and Y. Liu, “Mechanism design for finding experts using locally constructed social referral web,” IEEE Transactions on Parallel and Distributed Systems, vol. 26, no. 8, pp. 2316–2326, 2014.   
[17] D. Zhao, X.-Y. Li, and H. Ma, “Budget-feasible online incentive mechanisms for crowdsourcing tasks truthfully,” IEEE/ACM Transactions on Networking, vol. 24, no. 2, pp. 647–661, 2014.   
[18] W. Mao, Z. Zheng, and F. Wu, “Pricing for revenue maximization in iot data markets: An information design perspective,” in INFOCOM, 2019.   
[19] C. Courcoubetis and A. Dimakis, “Throughput and pricing of ridesharing systems,” in INFOCOM, 2019.   
[20] M. Siew, K. Guo, D. Cai, L. Li, and T. Q. Quek, “Let’s share vms: Optimal placement and pricing across base stations in mec systems,” in INFOCOM, 2021.   
[21] X. Wang and L. Duan, “Dynamic pricing and capacity allocation of uav-provided mobile services,” in INFOCOM, 2019.   
[22] H. Yi, Q. Lin, and M. Chen, “Balancing cost and dissatisfaction in online ev charging under real-time pricing,” in INFOCOM, 2019.   
[23] H. Jin, H. Guo, L. Su, K. Nahrstedt, and X. Wang, “Dynamic task pricing in multi-requester mobile crowd sensing with markov correlated equilibrium,” in INFOCOM, 2019.   
[24] W. Liu, Y. Yang, E. Wang, and J. Wu, “Dynamic user recruitment with truthful pricing for mobile crowdsensing,” in INFOCOM, 2020.   
[25] R. Kleinberg and T. Leighton, “The value of knowing a demand curve: Bounds on regret for online posted-price auctions,” in FOCS, 2003.   
[26] R. Lavi and N. Nisan, “Online ascending auctions for gradually expiring items,” pp. 1146–1155, 2005.   
[27] F. Li, J. Liu, and B. Ji, “Combinatorial sleeping bandits with fairness constraints,” IEEE Transactions on Network Science and Engineering, vol. 7, no. 3, pp. 1799–1813, 2019.   
[28] Z. Qin, X. Gan, J. Liu, H. Wu, H. Jin, and L. Fu, “Exploring best arm with top reward-cost ratio in stochastic bandits,” in INFOCOM, 2020.   
[29] Y. Jianyi and R. Shaolei, “Bandit learning with predicted context: Regret analysis and selective context query,” in INFOCOM, 2021.

[30] L. Chen and J. Xu, “Task replication for vehicular cloud: Contextual combinatorial bandit with delayed feedback,” in INFOCOM, 2019.   
[31] I. Aykin, B. Akgun, M. Feng, and M. Krunz, “Mamba: A multi-armed bandit framework for beam tracking in millimeter-wave systems,” in INFOCOM, 2020.   
[32] A. Verma and M. K. Hanawal, “Stochastic network utility maximization with unknown utilities: Multi-armed bandits approach,” in INFOCOM, 2020.   
[33] G. Gao, J. Wu, M. Xiao, and G. Chen, “Combinatorial multi-armed bandit based unknown worker recruitment in heterogeneous crowdsensing,” in INFOCOM, 2020.   
[34] S. Yiwen and J. Haiming, “Minimizing entropy for crowdsourcing with combinatorial multi-armed bandit,” in INFOCOM, 2021.   
[35] G. Gao, H. Huang, M. Xiao, J. Wu, Y. Sun, and S. Zhang, “Auctionbased combinatorial multi-armed bandit mechanisms with strategic arms,” in INFOCOM, 2021.   
[36] A. Rangi, M. Franceschetti, and L. Tran-Thanh, “Unifying the stochastic and the adversarial bandits with knapsack,” in IJCAI, 2019.   
[37] A. R. Cardoso, J. Abernethy, H. Wang, and H. Xu, “Competing against nash equilibria in adversarially changing zero-sum games,” in ICML, 2019.   
[38] O. Besbes and A. Zeevi, “Dynamic pricing without knowing the demand function: Risk bounds and near-optimal algorithms,” Operations Research, vol. 57, no. 6, pp. 1407–1420, 2009.