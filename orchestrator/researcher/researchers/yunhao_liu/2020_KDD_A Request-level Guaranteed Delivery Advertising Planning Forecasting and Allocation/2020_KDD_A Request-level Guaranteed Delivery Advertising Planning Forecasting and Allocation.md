# A Request-level Guaranteed Delivery Advertising Planning: Forecasting and Allocation

Hong Zhang

keyzhzhang@tencent.com

Tencent

Lan Zhang∗

zhanglan@ustc.edu.cn

University of Science and Technology of China

Lan Xu

lanxu@tencent.com

Tencent

Xiaoyang Ma

xiaoyangma@tencent.com

Tencent

Zhengtao Wu

wzt@mail.ustc.edu.cn

University of Science and Technology of China.

Cong Tang

tangcong@mail.ustc.edu.cn

University of Science and Technology of China.

Wei Xu

davidxu@tencent.com

Tencent

Yiguo Yang

justinyang@tencent.com

Tencent

# ABSTRACT

The guaranteed delivery model is widely used in online advertising. The publisher sells impressions in advance by promising to serve each advertiser an agreed-upon number of target impressions that satisfy specific attribute requirements over a fixed time period. Previous efforts usually model the service as a crowd-level or userlevel supply allocation problem and focus on searching optimal allocation for online serving, assuming that forecasts of supply are available and contracts are already signed. Existing techniques are not sufficient to meet the needs of today’s industry trends: 1) advertisers pursue more precise targeting, which requires not only user-level attributes but also request-level attributes; 2) users prefer more friendly ad serving, which imposes more diverse serving constraints; 3) the bottleneck of the publisher’s revenue growth lies in not only the ad serving, but also the forecast accuracy and sales strategy. These issues are non-trivial to address, since the scale of the request-level model is orders of magnitude larger than that of the crowd-level or user-level models. Facing the challenges, we present a holistic design of a request-level guaranteed delivery advertising planning system with careful optimization for all three critical components including impression forecasting, selling and serving. Our system has been deployed in the Tencent online guaranteed delivery advertising system serving billion level users for nearly one year. Evaluations on large-scale real data and the

performance of the deployed system both demonstrate that our design can significantly increase the request-level impression forecast accuracy and delivery rate.

# CCS CONCEPTS

• Information systems → Computational advertising; • Theory of computation → Models of learning.

# KEYWORDS

Guaranteed Delivery Advertising; Request-level Impression Forecasting; Advertisement Allocation

# ACM Reference Format:

Hong Zhang, Lan Zhang, Lan Xu, Xiaoyang Ma, Zhengtao Wu, Cong Tang, Wei Xu, and Yiguo Yang. 2020. A Request-level Guaranteed Delivery Advertising Planning: Forecasting and Allocation. In Proceedings of the 26th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD ’20), August 23–27, 2020, Virtual Event, CA, USA. ACM, New York, NY, USA, 9 pages. https://doi.org/10.1145/3394486.3403348

# 1 INTRODUCTION

A large portion of online display advertising is sold in a guaranteed delivery way. During a typical process of guaranteed delivery advertising, the advertiser places an order for a certain number of ad impressions to be shown to users with certain attributes over a specified period in the future. The publisher needs to accomplish the following three tasks in some (nearly) optimal way: 1) forecasting inventory (the eligible impression opportunities) in the specified period; 2) selling forecasted inventory by determining the maximum amount of impression opportunities that can be guaranteed for the order months/weeks in advance and signing the contract; 3) serving ad in real time when an actual user request arrives by determining which of the thousands of eligible contracts should be displayed for each opportunity in a split-second latency. Even a few percent improvement in the quantity of the sale or delivery rate can increase the publisher revenue by tens of millions of dollars, as well as increase the return on investment for advertisers. Overselling, however, will result in underdelivery and a penalty.

![](images/eec797d5b7cc63f03cefc37d3d7f42b8b9ea4988cc21672e5c9cf3c441cac878.jpg)



Figure 1: Example of user requests and orders. Each user may have heterogeneous requests with different numbers of impressions. The dash line indicates an impression in the request is eligible to the connected order.

Many efforts have been devoted to optimizing guaranteed delivery advertising [2, 4, 5, 7, 8, 10, 12]. However, industry trends show that existing approaches cannot fulfill the needs of advertisers, users and publishers in the following aspects: First, most work formulate and solve the forecasting and allocation problems at the crowd level [2, 4, 7, 8, 10, 12]. Some recent work begin to consider the user-level allocation [5]. In reality, advertisers always pursue more precise targeting. For example, an advertiser may target Shanghai female iPhone users watching a specified popular TV show through a Wi-Fi connection. As the example in Figure 1, each user may have heterogeneous requests and different requests may have different numbers of impression opportunities. Serving such advertisers requires not only crowd-level/user-level attributes but also request-level attributes, such as the name of the content and the network condition. Based on the statistics of Tencent online video advertising, 45% orders require request-level targeting. The scale of attribute combinations at the request level is several orders of magnitude larger than that at the user level, making existing methods inefficient to solve the forecasting and allocation problems. Second, previous work in the guaranteed delivery advertising mainly focus on how to efficiently achieve optimal allocation for online serving, assuming that impression forecasts and contracts are already available. Though impression forecast errors and sales strategy have non-ignorable effects on the performance of ad serving [2, 4, 5, 12], few work has delved into the large-scale impression opportunity forecasting and selling problems at the user level[10], let alone at the request level. Third, more customized and user-friendly serving constraints are desired by both advertisers and users. Most allocation algorithms are tailored for specific constraints, thus difficult to support customized constraints.

Motivated by the industry trends towards more precise advertising targeting and more user-friendly serving constraints, we design a Request-level guaranteed delivery Advertising Planning system (RAP) from a more holistic perspective, which aims to optimize all three critical components including impression forecasting, selling and serving. Figure 2 illustrates the structure of our system. The main components focus on addressing the following two challenging problems:

![](images/53936abffceb819dca5a12618fa888a10ff844ff9a016338dcbc4b7635dda5dd.jpg)



Figure 2: Structure of our request-based guaranteed delivery advertising planning system RAP.

1. Large-scale request-level impression forecasting. Large-scale high-dimensional data forecasting is a recognized challenging problem. In our case, the dimensionality of the request-level attribute combinations are orders of magnitude larger than that in the stateof-the-art work [10]. In Tencent advertising system, there are billion level impressions per day. The number of valid user attribute combinations is 63,901, and the number of valid request attribute combinations is 4,254,119, which results in an extremely large space for possible targeting. Moreover, the historical impressions are very sparse due to heterogeneous user behaviors. Therefore, forecasting request-level impression requires substantial computing resources and non-trivial features to characterize sparce and diverse requests.

2. Large-scale request-level impression allocation for selling and serving under customized linear constraints. Even we have got perfect forecasts, the scale of the allocation problem is the Cartesian product of tens of billions of impressions and thousands of contracts, which makes it very challenging to achieve (nearly) optimal allocation within a short latency. In the selling stage, the latency of allocating days of impressions should be less than a minute. In the serving stage, the latency of allocation should be less than hundreds of milliseconds. Arbitrary customized serving constraints further increase the difficulty of solving the large-scale optimization problem.

Our contribution can be summarized as follows.

(1) We present a holistic design of a large-scale request-level guaranteed delivery advertising planning system, including finegrain impression forecasting and allocation optimization for selling and serving. Our design allows the granularity of the target attributes be much finer, from user-level to request-level, resulting in more precise advertising. It also supports more complex customized ad serving constraints. This added flexibility without sacrifices of efficiency, we expect, will greatly benefit advertisers, users, as well as the publisher.   
(2) We propose a method combining clustering and tensor factorization to achieve accurate request-level impression forecasting and obviously reduce the time complexity. For large-scale allocation, we solve the optimization problem with a set of customized linear constraints and design a parallel algorithm based on parameter sharing and a GPU-accelerated method to significantly speed up the problem solving. We carefully design the objective functions for both impression selling and ad serving. Based on our algorithms, we leverage a lambda architecture to support selling and serving in

a short latency. We also incorporate real-time feedbacks to improve the allocation for online serving.

(3) RAP has been deployed in the Tencent online guaranteed delivery advertising system for nearly one year. We extensively evaluate our system on real data of billions of user requests and thousands of contracts. Both the experimental and online results show that our forecasting method outperforms state-of-the-art methods and our allocation solutions achieve a significant improvement on delivery rate and play rate, which have brought a considerable revenue growth.

# 2 RELATED WORK

Our work is related to two categories of existing work: time series forecasting and guaranteed delivery advertising allocation.

Time series forecasting. Traditional time series forecasting methods have been shown not suitable to deal with sparse highdimensional data [10]. Recently, Matrix factorization models [1, 3] have been proposed to solve time series forecasting problems. Yu et al. [1] design a temporal regularized matrix factorization (TRMF) framework for high-dimensional noisy data forecasting. Ma et al. [10] propose a spatial temporal tensor factorization model (ST-TF), which achieves the state-of-the-art performance on large-scale high-dimensional data. In [10], it solves the crowd-level user visits forecasting and the scale of the forecasted tensor is ten thousands. In our request-level impression forecasting problem the scale of the tensor is orders of magnitude larger, making those existing methods infeasible.

Guaranteed delivery advertising allocation. The allocation problem is usually considered as a stochastic optimization problem, where there have been many foundational research work [6, 9, 11]. Inspired by these work, many practical algorithms have been proposed to address the allocation problem in guaranteed display advertising. Assuming a perfect forecast of future inventory, [12] can create a compact provably optimal allocation plan. Standard methods are too slow for large-scale commercial advertising applications. High Water Mark (HWM)[4] is a more efficient algorithm based on a greedy heuristic, which sacrifices optimality. To achieve a better tradeoff between running time and optimality, SHALE[2] incorporates optimal dual values to design a two-stage iterative algorithm so as to quickly approximate the optimal solution. Ali Hojjat et al.[7] [8] employ a column generation scheme to solve the problem with reach and frequency constraints. Zhang et al.[14] propose a consumption minimization model whose core is to minimize the user traffic consumed to satisfy all contracts. Recently, Fang et al.[5] present a personalized delivery framework, which models the allocation problem at the user level with individual frequency and slot constraints. All those work model the allocation at the crowd level or user level and many of them depend on the accuracy of inventory forecast. In our problem, we consider the request-level targeting, which significantly increase the scale and complexity of both forecasting and allocation problems. Besides, most allocation methods are tailored for ad serving and specified constraints. They can neither be directly adopted to solve the allocation in the selling stage (the problem formulation and objectives are different), nor easily support various customized serving constraints. Actually those user-level models with specific constraints like [5] are special cases of our request-level model with customized constraints.

# 3 PROBLEM AND SYSTEM OVERVIEW

A typical advertising planning problem can be represented with a bipartite graph, as shown in Figure 1. On the supply side, there are impression opportunities provided by user requests. The profile of these impression opportunities is composed of attributes of the user (e.g., gender, age, income level and area) and attributes of the request itself (e.g., time, network condition, content type and content name). User requests are heterogeneous, even for one single user. For example, the user  is a female user from Shanghai. Her irequests of type  is for TV series through a Wi-Fi connection. In jthis type of request, she creates three impression opportunities. $s _ { i j }$ sijdenotes the total amount of impressions provided by the requests of type  of user . Note that a type of requests is a set of requests j iwith the same attributes. On the demand side, each order targets a specific type of impressions. In Figure 1, the order  targets impressions in user requests for movies. It requests a certain amount $d _ { k }$ of impressions. is the set of serving constraints (e.g., reach dk qkand frequency). An edge from a supply node to a demand node is added if and only if the impression represented by this supply node is eligible for the order represented by the demand node. In guaranteed delivery advertising, advertisers order the impression opportunities months/weeks in advance and specify the ad serving durations. So the publisher needs to forecast the inventory and allocate impression opportunities to each order in the selling stage as well as allocate actual impressions to each signed contract in the serving stage. $x _ { i j k }$ denotes the proportion of impressions in the i jkrequests of type  of the user allocated to the order/contract . The ultimate goal of the publisher is to optimize his revenue as well as the experience of both advertisers and users by selling and serving as many eligible impressions as possible under serving constraints.

To achieve this goal, we provide a comprehensive system design for request-level guaranteed display advertising planning (in Figure 2), named RAP, containing the following core components:

(1) Impression forecasting: given the historical impressions, before signing a contract, the publisher conducts a long-term forecasting to estimate the available inventory $s _ { i j }$ in the ad serving sijduration of orders; before serving ads, the publisher also needs a short-term forecast of $s _ { i j }$ to optimize the ad allocation.

sij(2) Impression allocation for selling: when a new order arrives, given on the long-term forecast of $s _ { i j }$ k, the publisher should find the optimal faction $x _ { i j k }$ sijto best fulfill the new demand $d _ { k }$ under the constraint $q _ { k }$ xijk dkas well as minimize the negative impact on existing contracts.

(3)Impression allocation for serving: to achieve optimal ad serving, the publisher needs to generate a compact allocation plan $x _ { i j k }$ based on the short-term forecast of  . When a request arrives, i jk i jgiven a set of eligible contracts, the allocation plan and the real-time feedbacks, the publisher must decide the optimal contracts to serve the impressions in the request.

# 4 IMPRESSION FORECASTING

Both optimal selling and serving of guaranteed delivery advertising are based on the impression forecasting. In this section, we present our efficient request-level impression forecasting method.

In general, guaranteed delivery advertising is sold on a daily basis, so in our forecasting problem we take the day as the smallest unit of time. Let $s _ { i j } ^ { t }$ denote the total impressions of the requests of type  of the user  on the -th day. The total inventory on the -day jis a set $D ^ { t } = ( s _ { i j } ^ { t } | i \in I , j \in J )$ t.  and  are sets of indices of users and D (si j i I , j J ) I Jrequest types respectively. Given the historical -day inventory $D ^ { 1 ^ { - } } , D ^ { 2 } , \cdots , D ^ { N }$ N, our goal is to predict the future -day inventory $D ^ { \prime N + 1 } , D ^ { \prime N + 2 } , \cdot , D ^ { \prime N + M }$ M , which should minimize the loss function $L ( D ^ { \prime N + 1 } , \cdot , D ^ { \prime N + M } )$ .

![](images/1ae006a4f3df3b32c81fadea7d89d39344448b25342f2a7d141f3bb4131eae0d.jpg)



Figure 3: Request-level impression opportunity forecasting based on clustering and tensor factorization.

(D , , D )Intuitively, the loss function can be defined as the $L _ { 1 }$ difference Lbetween the real impressions and the forecasted impressions:

$$
L (D ^ {\prime N + 1}, \dots , D ^ {\prime N + M}) = \frac {1}{M} \frac {1}{| I |} \frac {1}{| J |} \sum_ {t = 1} ^ {M} \sum_ {I} \sum_ {J} | s _ {i j} ^ {\prime N + t} - s _ {i j} ^ {N + t} |,
$$

where $s _ { i j } ^ { \prime }$ is the number of forecasted impressions.

ijTheoretically, we can solve the forecasting problem by minimizing the loss function following the idea of tensor factorization. As depicted in Figure 3, we can represent impressions ′1 ′2 · · · ′N +M $D ^ { \prime 1 } , D ^ { \prime 2 } , \cdot \cdot \cdot , D ^ { \prime N + M }$ by a 3-rd order tensor $D \in \overline { { \mathbb { R } } } ^ { I * J * T }$ D , D , , Dwith three modes, namely user, request attribute combination (request type) and date. Here  and respectively denote the numbers of users $( \sim 1 0 ^ { 9 } )$ and request attribute combinations $( \sim 1 0 ^ { 7 } ) . 7$ means there are  days data in total. Then $s _ { i j } ^ { t }$ T Tis an element of D. We can predict the unknown inventory $\{ s _ { i j } ^ { t } | t > N \}$ (the blue part in tensor D Figure 3) by exijploring the optimal tensor factorization that minimizes the loss function. However, the loss function is impractical and existing tensor factorization models $( \mathrm { e . g . } ,$ the state-of-the-art work $S \mathrm { T } \mathrm { - } \mathrm { T F } [ 1 0 ] )$ （2号 cannot be directly adopted. The reason is that the dimension of the request-level tensor D in our problem is several orders of magnitude larger than that in $S \mathrm { T - T F } [ 1 0 ]$ and much sparser, making existing models infeasible.

To deal with the high dimensionality and sparsity, we incorporate clustering into tensor factorization, and improve the loss function according to the targeting of existing contracts.

Tensor Factorization with clustering. As shown in Figure 3, we decompose the original tensor D into two time-independent factor matrices $\boldsymbol { A } \in \mathbb { R } ^ { \breve { I } * K _ { 1 } }$ and $c \in \mathbb { R } ^ { K _ { 2 } * J }$ , and a smaller tensor $\pmb { { B } } \in \mathbb { R } ^ { K _ { 1 } * K _ { 2 } * T }$ . We treat the newly added dimension $K _ { 1 }$ as the clus-Ktering of users and A as the conditional probability distribution of each user in the user clusters. Similarly, we treat the newly added dimension $K _ { 2 }$ as the clustering of user requests and C as the conditional probability distribution of each request attribute combination in the request clusters. Then we can consider the tensor B as the joint probability distribution of the clusters of users and clusters of requests changing with time. In this way, we decompose the original forecasting problem into two clustering problems and one lower-dimensional forecasting problems

Reweighting forecast errors for target attribute combinations. Considering that advertisers are interested in the impressions of target attribute combinations, the accuracy of every $s _ { i j } ^ { \prime }$ shouldn’t weight equally. Let $\gamma$ ijbe a set of target user and request attribute γcombinations determined by contracts. $\begin{array} { r } { S ^ { t } ( \gamma ) = \sum _ { ( i , j ) \in \gamma } s _ { i j } ^ { t } } \end{array}$ defines (i, j ) γ i jthe actual total impressions of the target attribution combinations in  on the -th day. $S ^ { \prime t } ( \gamma )$ is the estimated value corresponding to $S ^ { t } ( \gamma ) . \pi ( \gamma )$ t S (γ ) is the probability distribution of target attribute combinations. Then we can have the reweighted loss function to measure the forecast error for target attribute combinations:

$$
L _ {R} = \frac {1}{M} \sum_ {t = 1} ^ {M} \sum_ {\gamma \in \Gamma} \pi (\gamma) | \sum_ {(i, j) \in \gamma} s _ {i j} ^ {\prime N + t} - \sum_ {(i, j) \in \gamma} s _ {i j} ^ {N + t} | \tag {1}
$$

t γ Γ (i, j) γ (i, j) γThis loss indicates the possible underdelivery and is our major minimization objective.

User clustering. To obtain matrix A, we put all individual users into groups $( \sim 1 0 ^ { 4 } )$ determined by popular target user attribute combinations in existing contracts. For example, we put female iPhone users from Shanghai into the same user group. Let G be set of all user groups. $G ( i ) \in \mathbb { G }$ represents the group of user . The G (i ) itotal impressions of user group  on the -th day is P{ : = } t , $\sum \{ i \colon G ( i ) = g \} \ s _ { i j } ^ { t } .$ i G (i) д ijwhich contains denser impressions and is easier to forecast. Based on the user clustering, we can define the following loss measuring the structural error of forecasted impressions of user groups:

$$
L _ {U} = \frac {1}{M} \frac {1}{| \mathbb {G} |} \frac {1}{| J |} \sum_ {t = 1} ^ {M} \sum_ {J} \sum_ {g \in \mathbb {G}} \left| \sum_ {\{i: G (i) = g \}} s _ {i j} ^ {\prime N + t} - \sum_ {\{i: G (i) = g \}} s _ {i j} ^ {N + t} \right|. \tag {2}
$$

This loss is used to prevent the model from over-fitting on the target attribute combinations of historical contracts.

Request clustering. To efficiently obtain the matrix C, we cluster actual daily impression vectors of each user into $K _ { 2 }$ clusters. Here, daily impression vectors of a user are daily histograms of his/her actual impressions in the popular target attribute combinations (that are predefined based on the statistics of historical contracts). Let the set of all users’ daily impression vectors be , which will be divided into $K _ { 2 }$ clusters $V _ { 1 } , V _ { 2 } , \cdots , V _ { K _ { 2 } }$ . Let $\mu _ { c }$ Vbe the center vector of cluster . $\Sigma _ { c } ^ { - 1 }$ K c represents the covariance matrix of c Σccluster . Then the objective function of clustering can be defined cby Euclidean distance as

$$
L _ {C} = \sum_ {c = 1} ^ {K} \sum_ {x _ {i} \in V _ {c}} (x _ {i} - \mu_ {c}) ^ {2}. \tag {3}
$$

If we consider a hybrid soft clustering, the objective function of the clustering task can also be defined by the Mahalanobis distance as $\begin{array} { r } { L _ { c } = \sum _ { c = 1 } ^ { K } \sum _ { x _ { i } \in V _ { c } } ( x _ { i } - \mu _ { c } ) ^ { T } \Sigma _ { c } ^ { - 1 } ( x _ { i } - \mu _ { c } ) } \end{array}$ . We conduct clustering Lc cto minimize $L _ { C }$ V (xi µc ) Σc (xi µc )and obtain the matrix C. In our implementation, LCwe determine the number of clusters using the algorithm in [13] and get 15 clusters by k-means. We use two months of real historical data (from October to November in 2018) to evaluate the consistency of the clustering results. The weekly clustering results show that at least 12/15 cluster centers overlap between any two weeks. It conforms to our design that the clustering is relatively stable and time-independent. Therefore, the matrix C doesn’t need to be updated frequently.

Multi-objective loss function and forecasting. Combing Eq.(1), $\operatorname { E q . } ( 2 )$ and Eq.(3), we obtain the complete objective:

$$
L _ {F} = L _ {R} + \lambda_ {u} L _ {u} + \lambda_ {c} L _ {c}. \tag {4}
$$

Here, $\lambda _ { u }$ and $\lambda _ { c }$ are parameters balancing multiple objectives. Since λu λcthe scale of tensor B is much smaller than the original tensor D, we can use a deep spatial-temporal tensor factorization model (ST-TF) in [10] to forecast unknown values in B (the blue part in tensor B in Figure 3) to minimize the objective function $L _ { F } .$ The forecasted LFvalues indicate the joint probability distribution of user group and request cluster in the future. Now we have obtained matrices A and C and tensor B, thus we can calculate the blue part in the original tensor, which are the forecasted -day inventory.

MImplementation. In our implementation, we do not need to build the original tensor based on all historical users. We only focus on the recently active users, which result in a smaller . For the deep Ilearning model training, we sample one from every thousand users within a time window as the training samples to reduce the size of training data. Our design significantly reduces the time complexity for large tensor factorization and mitigates the difficulty of highdimensional sparse data forecasting. The forecast accuracy of our deployed system is 88% ∼ 92%, which significantly benefits the request-level impression selling and serving.

# 5 IMPRESSION ALLOCATION

Now we have obtained the forecasted impressions $s _ { i j } .$ . In this section, sijwe will introduce how to optimally allocate these impressions to advertisers’ contracts in the selling and serving stages. First, we will present the formulation of the basic allocation optimization problem. Then we design a novel method to efficiently solve a large-scale optimal allocation. In the end, we define the allocation problems for ad selling and serving, and present the system design.

# 5.1 Basic Allocation Problem Formulation

Recall that the ad allocation problem is usually modeled as a variant of the bipartite matching problem with some additional constraints, as the example in Figure 1. In guaranteed delivery advertising, a demand contract  usually has a penalty coefficient ${ \mathit { p } } _ { k }$ for underdelivery $u _ { k } \ ( \mathrm { i . e . }$ k pk, the number of impressions delivered less than $d _ { k } )$ uk. We need to determine the optimal allocation $x _ { i j k } .$ , that is the dkfraction of impressions $s _ { i j }$ xijkis allocated to contract . An allocation si j kis feasible if it satisfies the basic demand and supply constraints [2] as well as some additional constraints like frequency. The optimal allocation is a feasible allocation that minimizes some objective function. A typical objective of guaranteed delivery advertising is a tradeoff between maximizing the representativeness and minimizing the penalty. We aim to support arbitrary customized linear constraints and achieve efficient problem solving for large-scale problems, especially impression selling and ad serving. Here, taking frequency constraint as an example, we define a basic optimal allocation problem as follows:

$$
\min \quad f (x _ {i j k}) = \frac {1}{2} \sum_ {k} \sum_ {i, j \in \Gamma (k)} \frac {V _ {k} s _ {i j}}{\theta_ {k}} (x _ {i j k} - \theta_ {k}) ^ {2} + \sum_ {k} p _ {k} u _ {k} \tag {5}
$$

$\forall k \sum _ { i , j \in \Gamma ( k ) } x _ { i j k } s _ { i j } + u _ { k } \geq d _ { k }$ demand constraint

$\forall i , j \sum _ { k \in \Gamma ( i , j ) } x _ { i j k } \leq 1$ supply constraint

$\forall i , k \sum _ { j \in \Gamma _ { ( } k ) } x _ { i j k } s _ { i j } \leq q _ { k }$ frequency constraint

$\forall i , j , k \quad x _ { i j k } \geq 0 , u _ { k } \geq 0$ non-negativity constraint

i, j, k xijk , ukHere,  is the neighborhood of demand node , likewise, $\Gamma ( i , j )$ Γ(k) k Γ(i, j)is the neighborhood of supply node . In the objective function, ijthe first term is the non-representativeness that measures the $L _ { 2 }$ distance from the allocation $x _ { i j k }$ to a target $\theta _ { k }$ L. Similar to existing work, we set = $\begin{array} { r } { \theta _ { k } = \frac { d _ { k } } { \sum _ { ( i , j ) \in \Gamma ( k ) } s _ { i j } } . \ V _ { k } } \end{array}$ is the relative priority of the k ( , ) Γ( ) s kcontract . The second term in objective function is the total penalty kfor underdelivery.

Constraints. The frequency constraint controls the maximum/minimum number of times each user should see the ads from the same contract. In our design, the contract frequency constraint can be easily replaced by other linear constraints, such as the advertiser frequency constraint (the maximum/minimum number of times each user should see the ads from the same advertiser), slot constraint (the maximum number of ads from the same contract/advertiser in each user request), reach (the minimum number of unique individuals who should see an advertiser’s ads) and daily demand constraint of contracts.

# 5.2 Optimization Algorithm

The allocation problem in Eq.(5) is a convex optimization problem with linear constraints. There exist a set of solutions $x _ { i j k } = 0$ that xijkhold the constraints. Therefore, we can find the optimal solution for the primal problem by solving its dual problem based on the KKT conditions. For problem in Eq.(5), the Lagrangian function is

$$
\begin{array}{l} L (x, u, \alpha , \beta , \gamma , \eta , \psi) \\ = \frac {1}{2} \sum_ {k} (\sum_ {i, j \in \Gamma (k)} \frac {V _ {k} s _ {i j}}{\theta_ {k}} (x _ {i j k} - \theta_ {k}) ^ {2} + \sum_ {k} p _ {k} u _ {k}) \\ - \sum_ {k} \alpha_ {k} (\sum_ {i, j \in \Gamma (k)} x _ {i j k} s _ {i j} + u _ {k} - d _ {k}) + \sum_ {i} \sum_ {j} \beta_ {i j} (\sum_ {k \in \Gamma (i, j)} x _ {i j k} s _ {i j} - s _ {i j}) \\ + \sum_ {i} \sum_ {k} \gamma_ {i k} (\sum_ {j \in \Gamma_ {j} (k)} x _ {i j k} s _ {i j} - q _ {k}) - \sum_ {i} \sum_ {j} \sum_ {k} \eta_ {i j k} x _ {i j k} - \sum_ {k} \psi_ {k} u _ {k}. \\ \end{array}
$$

According to the stationary conditions $\begin{array} { r } { \frac { \partial L } { \partial x _ { i j k } } = 0 } \end{array}$ ∂Li jk aL and $\begin{array} { r } { \frac { \partial L } { \partial u _ { k } } = 0 } \end{array}$ ∂Lk we have $\begin{array} { r } { x _ { i j k } = \theta _ { k } \big ( 1 + \frac { \alpha _ { k } - \beta _ { i j } - \gamma _ { i k } - \eta _ { i j k } } { V _ { k } } \big ) , 0 \le \alpha _ { j } \le \mathtt { p } _ { j } } \end{array}$ ∂u. Because $\eta _ { i j k } = 0$ i or $x _ { i j k } = 0$ V, the allocation is

$$
x _ {i j k} = \max \{0, \theta_ {k} (1 + \frac {\alpha_ {k} - \beta_ {i j} - \gamma_ {i k}}{V _ {k}}) \}. \tag {6}
$$

To solve the dual variables $\alpha _ { k } , \beta _ { i j } , \gamma _ { i k }$ k, we can obtain the gradients of these dual variables: $\begin{array} { r } { \frac { \partial L } { \partial \alpha _ { k } } = d _ { k } - \sum _ { ( i , j ) \in \Gamma ( k ) } x _ { i j k } , \frac { \partial L } { \partial \beta _ { i j } } = } \end{array}$ ∂Lk =  − P ∈  , ∂ Li j = $\begin{array} { r } { \sum _ { k \in \Gamma ( i , j ) } x _ { i j k } - 1 , \frac { \partial L } { \partial \gamma _ { i k } } = \sum _ { j \in \Gamma _ { j } ( k ) } x _ { i j k } s _ { i j } - q _ { k } } \end{array}$ ∂Lik ∂β. Using a coordinate k Γ(i, j) ijk ∂γ j Γ (k ) ijk ij kdescent or gradient descent method, we can solve the problem iteratively until the objective function converges. In each iteration we first calculate $\alpha , \beta , \gamma$ and then get $x _ { i j k }$ . Since every linear conijkstraint has a corresponding dual variable, we can solve optimization problems with other linear constraints in the same manner.

# 5.3 Efficient Algorithm Implementation

Theoretically, the gradient descent algorithm is able to find the optimal allocation. When it comes to the real applications, however, the extremely large scale of the problem poses severe challenges to the implementation of the algorithm.

Observations. In the case that user is not eligible for contract , we have $\forall j , x _ { i j k } = 0$ . Because we have $\begin{array} { r } { \gamma _ { i k } = 0 \mathrm { o r } \sum _ { j \in \Gamma _ { j } ( k ) } x _ { i j k } s _ { i j } = } \end{array}$ $q _ { k } ,$ , then $r _ { i k } = 0$ ik j Γ (k ) i jk i j in this case. In the case request  is not eligible qk rikfor contract $k ,$ we have $\forall i , x _ { i j k } = 0$ j. Based on the statistics of our deployed system, $\frac { | \{ x _ { i j k } | x _ { i j k } \dot { \neq } 0 \} | } { | I | | J | | k | } < 2 . 7 \% .$ , and $\frac { | \{ \gamma _ { i k } | \gamma _ { i k } \neq 0 \} | } { | I | | k | } \ < \ 3 \%$ I J kTherefore, the dual variable $\gamma _ { i k }$ < . I k <are very sparse, so as the edges in γikthe bipartite graph. Moreover, the scale of $\alpha _ { k }$ is relatively small. Only the variable $\beta _ { i j }$ αkis dense due to the reason that almost every ijuser  has a number of requests so that $s _ { i j } \neq 0$ . These observations i sijmotivate us to implement our algorithm by leveraging the power of parallel computing and GPU-accelerated computing, which significantly speed up the problem solving.

Parallel algorithm. We employ a group of workers to efficiently solve this problem in a distributed manner that each worker computes a subset of $\beta _ { i j }$ locally and shares $\alpha _ { k }$ and non-zero $\gamma _ { i k }$ βij αkwith each other through a parameter server. Since the scale of $\alpha _ { k }$ ikis small and $\gamma _ { i k }$ αkis very sparse, the cost for parameter sharing is small. γikSpecifically, all users are divided into  groups and each group is wassigned to a worker. Then the computation is conducted parallelly as the following loop: 1) each worker downloads the newest $\alpha _ { k }$ and non-zero $\gamma _ { i k }$ kfrom the parameter server; 2) each worker computes $x _ { i j k }$ γikfor its own group of users according to $\operatorname { E q . } ( 6 )$ and updates and xijklocal $\beta _ { i j } ; 3 )$ each worker computes and upload $\Delta \alpha _ { k }$ and non-zero $\Delta \gamma _ { i k }$ βij ∆αkto the parameter server; 4) the parameter server aggregates $\Delta \alpha _ { k }$ and $\Delta \gamma _ { i k }$ from all workers to generate new $\alpha _ { k }$ and $\gamma _ { i k }$ . This k ik kloop continues until the objective function converges.

GPU-Accelerated Computing. For each worker, computing the value of $x _ { i j k } \ ( \mathrm { E q . } ( 6 ) )$ one by one is the most time-consuming ijkstep. To further speed up the computation, we treat $x _ { i j k }$ as a tensor and packed all parameters $\alpha _ { k } , \beta _ { i j }$ and $\gamma _ { i k }$ xijkinto three equal size αk βij γiktensors. In this way, each worker can efficiently compute the tensor of $x _ { i j k }$ by leveraging the power of GPU. Considering that $x _ { i j k }$ ijk ijkis very sparse, based on the edges in the bipartite graph, we can compress the tensor to only retain those non-zero dimensions. In this way, the computation cost is significantly reduced.

# 5.4 Allocation for Selling

In the selling stage, orders of advertisers arrive one at a time. The publisher allocates forecasted inventory to each new order and sign the contract. The major objective is to best fulfill the demand of existing contracts. The secondary objective is to maximize the saleable impressions for a new order. To deal with months of impressions and thousands of contracts in a short latency, we leverage a lambda architecture consisting of three layers: offline allocation, online allocation and a serving layer for responding to orders.

Offline allocation for selling. The offline allocation has sufficient time to search the global optimal solution for signed contracts. When selling months of impressions, a better temporal smoothness is an important guarantee for a better pacing for ad serving. Therefore, we add a daily demand constraint and a penalty for daily underdelivery to the basic allocation problem in $\operatorname { E q . } ( 5 )$ . The objective function of offline allocation for selling is

$$
\begin{array}{l} \min f (x _ {i j k}) - \sum_ {t} \sum_ {k \in \Gamma (t)} p _ {k} ^ {t} w _ {k} ^ {t} \\ s. t. \quad \forall k, t \quad \sum_ {i, j \in \Gamma (k, t)} x _ {i j k} s _ {i j} + w _ {k} ^ {t} \geq d _ {k} ^ {t}. \tag {7} \\ \end{array}
$$

Here, $d _ { k } ^ { t }$ is the guaranteed delivery amount of impressions for kcontract  on the -th day. It can be specified by the advertiser or kpublisher. $w _ { k } ^ { t }$ tis the underdelivery of contract  on the -th day. $\boldsymbol { p } _ { k } ^ { t }$ kis the penalty coefficient of contract  on the -th day. $\boldsymbol { p } _ { k } ^ { t }$ kis usually k t pka decreasing function of . We solve this problem using the GPU cluster based parallel algorithm in Section 5.3.

Online allocation for selling. The online allocation processes a newly arrived order in a sub-minute latency. The publisher aims to best fulfill the demand of the new order with minimal negative impact on the allocation of existing contracts. We add objective and constraints for the new order to the basic problem:

$$
\begin{array}{l} \min f (x _ {i j k}) - \sum_ {I} \sum_ {J} y _ {i j} \\ s. t. \quad \forall i, j \sum_ {k \in \Gamma (i, j)} x _ {i j k} + y _ {i j} \leq 1, \sum_ {j \in \Gamma (y)} y _ {i j} s _ {i j} \leq q, \quad y _ {i j} \geq 0 \tag {8} \\ \end{array}
$$

Here, $y _ { i j }$ is the proportion of the supply $s _ { i j }$ assigned to the new yij sijorder. is the frequency constraint of the new order. Based on the qoffline global optimal solution, this problem can be solved with a small number of iterations, so as to achieve a short response latency.

# 5.5 Allocation for Serving

During serving, user requests arrive one at a time and each request provides several impressions. The publisher allocates each impression to a contract in real time to optimize the objectives. In our design, we add a secondary goal to the basic allocation problem $( \operatorname { E q . } ( 5 ) )$ ) to improve the total click through rate (CTR). The objective function is

$$
\min \quad f (x _ {i j k}) - \lambda \sum_ {k} \sum_ {i, j \in \Gamma (k)} \omega_ {k} x _ {i j k} c t r _ {i j k}. \tag {9}
$$

Here $c t r _ { i j k }$ is the CTR for contract  on the impressions $s _ { i j } . c t r _ { i j k }$ ijk ij ijkis provided by the CTR prediction component of an advertising system. $\omega _ { k }$ be the weight of CTR for contract .  is the hyper ωkparameter balancing different objectives.

Based on the forecasted impressions one day in advance, we generate an allocation plan using the method in Section 5.3 to guide the ad serving. To better cope with the impression forecast errors and real-time demand changes caused by newly arrived orders, we need frequent corrections of the allocation plan according to the realtime feedbacks. According to $\operatorname { E q . } ( 6 )$ , let $\begin{array} { r } { \rho _ { i j k } = 1 + \frac { \alpha _ { k } - \beta _ { i j } - \gamma _ { i k } } { V _ { k } } } \end{array}$ , we have $x _ { i j k } = \operatorname* { m a x } \{ 0 , \theta _ { k } \rho _ { i j k } \}$ . Here $\rho _ { i j k }$ ijk Vis determined by the bipari jk k i jk i jktite graph. It needs to be updated every minute.  = P dki j ∈ k i j $\begin{array} { r } { \theta _ { k } = \frac { d _ { k } } { \sum _ { ( i , j ) \in \Gamma ( k ) } s _ { i j } } } \end{array}$ needs to be updated according to the real-time $d _ { k }$ and $s _ { i j }$ ( , ) Γ( ) s. Towards dk sijminimizing the objective function, online serving takes the following steps. 1) We generate a bipartite graph based on the forecasted impressions and signed contracts. It is sufficient to update the bipartite graph every hour considering that the basic unit of time for both impression forecast and demand is the day. 2) According to the real-time (millisecond level) statistics of impressions and contracts, we update $d _ { k } , s _ { i j }$ and $\theta _ { k } . 3 )$ Given the bipartite graph and real-time $d _ { k }$ and $s _ { i j }$ k sij θk, the online allocation component solves the dk sioptimization problem $( \operatorname { E q . } ( 9 ) )$ and outputs tensor $x _ { i j k }$ and tensor $\rho _ { i j k } .$ xijk. This computation is conducted every minute. 4) The online ijkserving component takes as input $\rho _ { i j k }$ and $\theta _ { k }$ to compute the final $x _ { i j k }$ and serve ads accordingly.

# 6 SYSTEM EVALUATION

We have implemented RAP and deployed it in the Tencent online guaranteed delivery advertising system for nearly one year. This system serves billion level users with a variety of ads, including video ads, in-feed ads, splash ads, etc. The deployment of RAP has brought a significant revenue growth.

# 6.1 Datasets

In this section, we extensively evaluate RAP with real impression and contract data of Tencent online video site.

Dataset for forecasting. There are a billion of impressions per day. Each impression has four types of user attributes and 17 types of request attributes. User attributes include platform (with 7 options such as iPhone and PC), area (with 396 options such as Shanghai), age and gender. Request attributes include content type (with more than 300 options such as movie and TV), content name (with more than 3,400,000 options such as “Spider-Man” and “Friends”), network (5 options such as Wi-Fi and 4G), target time (with 48 options, every half an hour is an option), etc. The training data is from June 1, 2018 to November 30, 2019 and the testing data is from December 1, 2019 to December 31, 2019.

Datasets for allocation. To evaluate the allocation for selling, we use 650,223 sampled impressions and 5,753 contracts on January 1, 2020. To evaluate the allocation for serving, we use two datasets on December 31, 2019. A large dataset contains 726,390 sampled impressions and 5,782 contracts. A small dataset contains 9,087 sampled impressions and 104 contracts from Shanghai.

Unless otherwise specified, evaluations were conducted on a server with a Tesla P40 GPU and a Intel Xeon CPU E5-2680 v4.

# 6.2 Impression Forecasting

Models for comparison. The evaluation results in [10] show that traditional time series forecasting methods are not competent to deal with sparse high-dimensional data. Hence, we implement the following state-of-the-art high-dimensional time series forecasting models for comparison:ST-TF[10], TRMF[1], a CNN model and LSTM. The structures and parameters of those models are all consistent with that in [10].

If we consider all valid attributes of impressions, the number of attribute combinations will be too large for previous models to handle. For fair comparison, we first consider only the three most popular attributes, namely platform, area and content type (PAC). Then we consider the five most popular attributes, namely platform, area and network, gender and content type (PANGC). In this end we evaluate our method on all target attribute combinations of real contracts.

Forecasting impressions N days in advance on PAC attribute combinations. Let $N = \{ 1 , 2 , \cdots 2 8 \}$ , Figure 4 illustrates forecast N , ,accuracy of different methods changing against . Table 1 presents Ntheir 28-day average forecast accuracy. The results show that our design achieves significantly better accuracy than TRMF, CNN and LSTM. Overall, the performance of RAP is better than ST-TF. The 28-day average accuracy of RAP is 87.76% while that of ST-TF is 86.53%. When  is small, ST-TF has slightly better accuracy. As Nincreases, the accuracy of RAP gradually exceeds that of ST-TF.

<table><tr><td>Method</td><td>Accuracy</td><td># of Parameters</td><td>Training Time (s)</td></tr><tr><td>RAP</td><td>0.8776</td><td>137,462</td><td>1,393</td></tr><tr><td>ST-TF</td><td>0.8653</td><td>61,850</td><td>942</td></tr><tr><td>TRMF</td><td>0.8139</td><td>1,800,879</td><td>1,127</td></tr><tr><td>CNN</td><td>0.8028</td><td>174,748</td><td>815</td></tr><tr><td>LSTM</td><td>0.6858</td><td>8,716</td><td>1,213</td></tr></table>

Table 1: 28-day average forecasting accuracy for different models on PAC attribute combinations.

Performance on PANGC attribute combinations. The scale is 15 times larger that in the PAC case. Facing the high-dimensional tensor, TRMF, CNN and LSTM fail to converge within an acceptable training time. Figure 5 illustrates the training process of ST-TF in the PAC and PANGC cases. In the PAC case, the loss of ST-TF steadily declines and converges after 700 steps. In the PANGC case, after a decline the loss oscillates around 0.2 and has difficulty to converge. Adding two attributes (network and gender) decreases the accuracy of ST-TF by about 6%. The more attributes are considered, the worse ST-TF performs. The results show that those state-of-the-art methods cannot handle high-dimensional sparse data, thus are not capable of solving our request-level impression forecasting task.

Performance on all target attribute combinations. In this case, we consider all attribute combinations that have been targeted by real contracts. Except RAP, all other models fail to generate forecast results. Table.2 presents the forecast accuracy of RAP. When equals 1, 7 and 14, the accuracy is 90.13%, 91.76% and 89.87% respectively, which are even slightly better than the accuracy in the PAC case. In our deployed system, the forecast accuracy on all target attribute combinations is 88% ∼ 92%. The results verify that our design can achieve efficient and accurate large-scale request-level impression forecast.

Comparison with sampling methods. As aforementioned, existing deep learning based methods do not work when considering all attributes combinations. In industrial applications, it is common to adopt sampling results on historical data as forecasts. Thus, we compare our method with the following widely used sampling methods: 1)Traditional sampling (TS) samples a certain proportion of daily historical data; 2)Smooth sampling (SS) uses a 30-day sliding window to sample the average value of multi-day historical data. Table.2 presents the forecast accuracy of different sampling methods on the PAC attribute combinations and all target attribute combinations. Our method achieves a clear improvement compared with two sampling methods and performs the best in all cases.

# 6.3 Impression Allocation

# 1) Allocation for Selling

Recall that RAP leverages a lambda architecture and solves the offline allocation problem (in Eq.(7)) and online allocation problem (in Eq.(7)) to optimize the impression allocation for orders. We compare our selling strategy with the following methods:

![](images/171223b095b4ab0f27fa14c5ec01eaa09ab0cbf6f7253ae48331e2d447b4e0fe.jpg)



Figure 4: Impression forecast accuracy  days in advance on PAC attribute combinations. 

<table><tr><td rowspan="2">Method</td><td colspan="3">Contract Targets</td><td colspan="3">PAC</td></tr><tr><td>1</td><td>7</td><td>14</td><td>1</td><td>7</td><td>14</td></tr><tr><td>RAP</td><td>90.13</td><td>91.76</td><td>89.87</td><td>89.04</td><td>90.65</td><td>87.95</td></tr><tr><td>SS</td><td>74.03</td><td>73.91</td><td>74.27</td><td>74.03</td><td>73.91</td><td>74.27</td></tr><tr><td>TS</td><td>87.84</td><td>86.10</td><td>87.61</td><td>86.98</td><td>84.39</td><td>77.62</td></tr></table>

Table 2: Forecast accuracy -day in advance on different target attribute combinations.

<table><tr><td></td><td>Time (s)</td><td># of Saleable Impressions</td></tr><tr><td>FIFO</td><td>0.1</td><td>182</td></tr><tr><td>Heuristic-HWM</td><td>1</td><td>3688</td></tr><tr><td>RAP</td><td>30</td><td>4906</td></tr></table>

Table 3: Average number of saleable impressions allocated for new orders by different methods.

•FIFO: a newly arrived order has a lower priority than all singed contracts. Therefore, keeping the allocation to signed contracts unchanged, only remaining eligible impressions can be assigned to the new order.

•Heuristic-HWM: We adopt HWM[4] to allocate impressions to a new order. Specifically, we first determine the upper and lower bounds of the impressions available for the new order. The upper bound is the total impression count, and the lower bound is the result of FIFO. Then we give the new order a reservation amount between the upper and lower bounds by binary search to turn the selling problem into a series of typical delivery problems. We solve each delivery problem by HWM until we find the maximum available inventory that does not increase the underdelivery rate of signed contracts.

Given the real 650,223 impressions and 5,753 contracts on January 1, 2020, we randomly select 100 orders from the 5,753 contracts as new orders and let other contracts remain signed. Table. 3 presents the average number of saleable impressions allocated to each new order by different methods. FIFO performs the worst. Compared with Heuristic-HWM, RAP increase the number of saleable impressions for new orders by 33%, which implies 33% revenue increase. The allocation time cost of RAP for each new order is 30 seconds, that of Heuristic-HWM is 1 second. In our deployed system, sub-minute latency is acceptable for most orders, therefore RAP has brought a significant revenue improvement. For some latency-sensitive orders, we use Heuristic-HWM to achieve an immediate response.

# 2) Allocation for Severing

We evaluate the following metrics for different serving methods:

![](images/9bc6941efb7e5fd6f488189b2798d84db142f20bc89d8b2c7385dffb2a13d6ca.jpg)



Figure 5: The training process of ST-TF in the PAC and PANGC cases.

•Underdelivery rate: represents the under-delivered impressions as a proportion of the total guaranteed demand. It is the main minimizing objective and defined as  = Pk uk . $\begin{array} { r } { U = \frac { \sum _ { k } u _ { k } } { \sum _ { k } d _ { k } } } \end{array}$

d•Play rate: represents the delivered impressions as a proportion of the total impressions. A higher play rate represents a better utilization of ad opportunities, thus higher profit of the publisher. The play rate is defined as  = Pk Pi, j ∈Γ(k ) si j xi jk $\begin{array} { r } { P = \frac { \sum _ { k } \sum _ { i , j \in \Gamma ( k ) } s _ { i j } x _ { i j k } } { \sum _ { i } \sum _ { j } s _ { i j } } } \end{array}$

$\mathbf { \sigma } \cdot L _ { 2 }$ sdistance: measures how much the generated allocation de-Lviates from a representative allocation as defined in the objective function 2 = 12 P P ∈ $\begin{array} { r } { L _ { 2 } = \frac 1 2 \sum _ { k } \sum _ { i , j \in \Gamma ( k ) } \frac { V _ { k } s _ { i j } } { \theta _ { k } } ( x _ { i j k } - \theta _ { k } ) ^ { 2 } } \end{array}$ V sk k i j .

k i, j Γ(k ) θ i jk k•Click through rate (CTR): is the total clicks divided by the total number of delivered impressions.

•Time cost: includes the initialization time cost and average time cost of each iteration.

Methods for comparison. We implement the following stateof-the-art methods and compare them with our method: HWM[4], SHALE[2] and ALI[5]. Specially, we consider three variants of ALI[5]: 1) the original ALI uses a gradient descent method and a coordinate descent method to compute the dual variables  and respectively; 2) ALI\_CD uses only a coordinate descent method; 3) ALI\_GD uses only a gradient descent method. We also consider four variants of RAP: 1) RAP\_CD: uses a coordinate descent method to solve dual variables $\alpha , \beta$ and  of the basic problem in Eq.(5); 2) RAP\_GD: uses a gradient descent method to solve the basic problem ; 3)RAP\_CD\_ CTR: uses a coordinate descent method to solve the refined problem in Eq.(9) with the secondary objective to maximize the CTR. RAP\_GD\_CTR: users a gradient descent method to solve the refined problem.

Figure 6 and Figure 7 illustrate the underdelivery rate and play rate changing with iterations on the large dataset (726,390 impressions and 5,782 contracts). The results on the small dataset are quite similar. Table. 4 and Table. 5 present all metrics of different methods after 100 iterations. Since HWM has only one iteration, it costs the least time but results in the worst underdelivery rate. The three variants ALI and SHALE achieve similar underdelivery rate, play rate and $L _ { 2 }$ distance. But the variants of ALI cost much less time Lthan SHALE. As shown by the obvious gaps in Figure 6 and Figure 7, the variants of RAP achieve significant improvements compared with existing methods and have the lowest underdelivery rate and highest play rate. For our deployed system, the underdelivery rate is 3% ∼ 5%. For example, the underdelivery rate of RAP\_GD\_CTR is 1.34% on the large dataset, which is 4.34% lower than that of ALI\_GD. The play rate of RAP\_GD\_CTR is

![](images/274b6554420fb59db9ccd2d45beec86194ccedc3c2c2b51cbc8172602c1bb9d2.jpg)



Figure 6: The underdelivery rate changes with iterations on the large dataset.

<table><tr><td>Algorithm</td><td>U</td><td>P</td><td>CTR</td><td> $L_2$ </td><td>Init Time</td><td>Avg Time</td></tr><tr><td>HWM</td><td>0.1463</td><td>0.4141</td><td>0.0312</td><td> $0.0292 \times 10^4$ </td><td>114.8751</td><td>-</td></tr><tr><td>SHALE</td><td>0.0588</td><td>0.4566</td><td>0.0312</td><td> $6.0951 \times 10^4$ </td><td>114.8361</td><td>0.9116</td></tr><tr><td>ALI</td><td>0.0573</td><td>0.4573</td><td>0.0327</td><td> $6.2012 \times 10^4$ </td><td>148.4866</td><td>0.2411</td></tr><tr><td>ALI_CD</td><td>0.0578</td><td>0.4571</td><td>0.0327</td><td> $6.2486 \times 10^4$ </td><td>144.7784</td><td>0.9112</td></tr><tr><td>ALI_GD</td><td>0.0568</td><td>0.4575</td><td>0.0327</td><td> $6.0871 \times 10^4$ </td><td>146.9235</td><td>0.0494</td></tr><tr><td>RAP_CD</td><td>0.0134</td><td>0.4786</td><td>0.0312</td><td> $8.5062 \times 10^4$ </td><td>251.9034</td><td>1.1356</td></tr><tr><td>RAP_GD</td><td>0.0137</td><td>0.4784</td><td>0.0312</td><td> $7.8719 \times 10^4$ </td><td>258.9217</td><td>0.0689</td></tr><tr><td>RAP_CD_CTR</td><td>0.0134</td><td>0.4786</td><td>0.0327</td><td> $8.5250 \times 10^4$ </td><td>248.8460</td><td>1.1285</td></tr><tr><td>RAP_GD_CTR</td><td>0.0137</td><td>0.4785</td><td>0.0327</td><td> $7.9012 \times 10^4$ </td><td>261.8263</td><td>0.0709</td></tr></table>

Table 4: Performance of different methods on the large dataset after 100 iterations ( is underdelivery rate,  is play U Prate, Avg Time is the average time for each iteration).

<table><tr><td>Algorithm</td><td>U</td><td>P</td><td>CTR</td><td> ${L}_{2}$ </td><td>Init Time</td><td>Avg Time</td></tr><tr><td>HWM</td><td>0.1847</td><td>0.8336</td><td>0.0309</td><td> ${0.564} \times {10}^{3}$ </td><td>0.5602</td><td>-</td></tr><tr><td>SHALE</td><td>0.0862</td><td>0.9343</td><td>0.0308</td><td> ${2.789} \times {10}^{3}$ </td><td>2.3205</td><td>0.0504</td></tr><tr><td>ALI</td><td>0.0902</td><td>0.9302</td><td>0.0324</td><td> ${2.205} \times {10}^{3}$ </td><td>2.3772</td><td>0.0156</td></tr><tr><td>ALI_CD</td><td>0.0861</td><td>0.9345</td><td>0.0324</td><td> ${2.495} \times {10}^{3}$ </td><td>2.3343</td><td>0.0526</td></tr><tr><td>ALI_GD</td><td>0.0894</td><td>0.9311</td><td>0.0324</td><td> ${2.082} \times {10}^{3}$ </td><td>2.3300</td><td>0.0034</td></tr><tr><td>RAP_CD</td><td>0.0453</td><td>0.9762</td><td>0.0309</td><td> ${3.449} \times {10}^{3}$ </td><td>4.1851</td><td>0.0695</td></tr><tr><td>RAP_GD</td><td>0.0484</td><td>0.9731</td><td>0.0309</td><td> ${3.048} \times {10}^{4}$ </td><td>4.1926</td><td>0.0047</td></tr><tr><td>RAP_CD_CTR</td><td>0.0453</td><td>0.9761</td><td>0.0324</td><td> ${3.435} \times {10}^{4}$ </td><td>4.2138</td><td>0.0698</td></tr><tr><td>RAP_GD_CTR</td><td>0.0484</td><td>0.9730</td><td>0.0324</td><td> ${3.040} \times {10}^{4}$ </td><td>4.3696</td><td>0.0026</td></tr></table>

Table 5: Performance of different methods on the small dataset after 100 iterations ( is underdelivery rate,  is play rate, Avg Time is the average time for each iteration).

47.86% on the large dataset, which is 2.11% higher than that of ALI\_- GD. The play rate of RAP\_GD\_CTR on the small dataset achieves 97.61%. The $L _ { 2 }$ distance of RAP is slightly larger than SHALE and LALI, which means a little loss of representativeness. Among the variants of RAP, we can see that using a gradient method can reduce the time cost by a order of magnitude with negligible loss of underdelivery rate and play rate. As an example, RAP\_GD\_CTR costs only 6.3% time of RAP\_CD\_CTR. For 100 iterations, RAP\_GD\_CTR costs 7.1s on the large dataset and 0.26s on the small dataset. Results in Table. 4 and Table. 5 also show that adding the secondary CTR maximization objective in Eq.(9) slightly improves CTR by 0.15% on both datasets.

Time cost. For the basic CPU solution (in Section 5.2) we use 56 cores of Intel Xeon CPU E5-2680 v4, it costs 43.68 seconds per iteration. For the GPU-accelerated parallel solution in Section 5.3 we use 4 Tesla P40 GPU, it costs 0.809 second per iteration. The results show that our design can save 98.1% time cost.

# 7 CONCLUSION

We present a holistic design of a large-scale guaranteed delivery advertising planning system, which supports efficient request-level impression forecasting and allocation. Our system empowers advertisers to achieve sufficiently precise targeting while keeping high delivery rate and play rate, which can significantly increase the publisher revenue and return on investment of advertisers. It can also provide more user-friendly ad serving with the ability to handle a set of customized linear serving constraints.

![](images/b917051194ec5d1376af6c02dfb1e38cf314ca5e4c23a28bd422fdd829387492.jpg)



Figure 7: The play rate changes with iterations on the large dataset.

# ACKNOWLEDGMENTS

This research is supported by the National Key R&D Program of China 2017YFB1003003, NSF China under Grants No. 61822209, 61932016, 61751211, China National Funds for Distinguished Young Scientists with No.61625205, the Fundamental Research Funds for the Central Universities.

# REFERENCES

[1] Mohammad Taha Bahadori, Qi Rose Yu, and Yan Liu. 2014. Fast multivariate spatio-temporal analysis via low rank tensor learning. In NIPS. 3491–3499.   
[2] Vijay Bharadwaj, Peiji Chen, Wenjing Ma, Chandrashekhar Nagarajan, John Tomlin, Sergei Vassilvitskii, Erik Vee, and Jian Yang. 2012. Shale: an efficient algorithm for allocation of guaranteed display advertising. In ACM SIGKDD. 1195–1203.   
[3] Preeti Bhargava, Thomas Phan, Jiayu Zhou, and Juhan Lee. 2015. Who, what, when, and where: Multi-dimensional collaborative recommendations using tensor factorization on sparse user-generated data. In WWW. ACM.   
[4] Peiji Chen, Wenjing Ma, Srinath Mandalapu, Chandrashekhar Nagarjan, Jayavel Shanmugasundaram, Sergei Vassilvitskii, Erik Vee, Manfai Yu, and Jason Zien. 2012. Ad serving using a compact allocation plan. In 13th ACM Conference on Electronic Commerce. 319–336.   
[5] Zhen Fang, Yang Li, Chuanren Liu, Wenxiang Zhu, Yu Zheng, and Wenjun Zhou. 2019. Large-Scale Personalized Delivery for Guaranteed Display Advertising with Real-Time Pacing. In ICDM. IEEE, 190–199.   
[6] Jon Feldman, Aranyak Mehta, Vahab Mirrokni, and Shan Muthukrishnan. 2009. Online stochastic matching: Beating 1-1/e. In 50th Annual IEEE Symposium on Foundations of Computer Science. IEEE, 117–126.   
[7] Ali Hojjat, John Turner, Suleyman Cetintas, and Jian Yang. 2014. Delivering guaranteed display ads under reach and frequency requirements. In AAAI.   
[8] Ali Hojjat, John Turner, Suleyman Cetintas, and Jian Yang. 2017. A unified framework for the scheduling of guaranteed targeted display advertising under reach and frequency requirements. Operations Research 65, 2 (2017), 289–313.   
[9] Chinmay Karande, Aranyak Mehta, and Pushkar Tripathi. 2011. Online bipartite matching with unknown distributions. In 43rd annual ACM symposium on Theory of computing. 587–596.   
[10] Xiaoyang Ma, Lan Zhang, Lan Xu, Zhicheng Liu, Ge Chen, Zhili Xiao, Yang Wang, and Zhengtao Wu. 2019. Large-scale User Visits Understanding and Forecasting with Deep Spatial-Temporal Tensor Factorization Framework. In ACM SIGKDD. 2403–2411.   
[11] Vahab S Mirrokni, Shayan Oveis Gharan, and Morteza Zadimoghaddam. 2012. Simultaneous approximations for adversarial and stochastic online budgeted allocation. In 23rd annual ACM-SIAM symposium on Discrete Algorithms. SIAM, 1690–1701.   
[12] Erik Vee, Sergei Vassilvitskii, and Jayavel Shanmugasundaram. 2010. Optimal online assignment with forecasts. In 11th ACM conference on Electronic commerce. 109–118.   
[13] Ulrike Von Luxburg et al. 2010. Clustering stability: an overview. Foundations and Trends® in Machine Learning 2, 3 (2010), 235–274.   
[14] Jia Zhang, Zheng Wang, Qian Li, Jialin Zhang, Yanyan Lan, Qiang Li, and Xiaoming Sun. 2017. Efficient delivery policy to minimize user traffic consumption in guaranteed advertising. In AAAI.