# A Framework to Provide Trust and Incentive in CROWN Grid for Dynamic Resource Management

Yu Zhang $^{1}$ , Jinpeng Huai $^{1}$ , Yunhao Liu $^{2}$ , Li Lin $^{1}$ , Baijian Yang $^{3}$

$^{1}$ Dept. of Computer Science and Technology

Beihang University,

Beijing, China

zhangyu@act.buaa.edu.cn

$^{2}$ Dept. of Computer Science, Hong Kong University of Science &

Technology

liu@cs.ust.hk

$^{3}$ Dept. of Industry and Technology,

Ball State University

byang@bsu.edu

Abstract—In order to maximize resource utilization as well as providing trust management in grid, we propose a novel framework – Trust-Incentive Resource Management (TIM). Having child model, club model, bid model and trust model, TIM dynamically manages grid resource by integrating values of prices, trust, and incentive. In this mechanism, providers set the price according to demand and supply, and consumers maximize the surplus upon budget and deadline. A weighted voting scheme is also proposed to secure the grid system by declining the join request from malicious nodes. A TIM prototype has been successfully implemented in a real grid system, CROWN grid. We evaluate the proposed approach through comprehensive experiments and achieve improved results in resource allocation efficiency, system completion time, and aggregated resource utilization.

Keywords-resource allocation; incentive; trust; CROWN

# I. INTRODUCTION

A dilemma in grid computing area is that when every participating node tries to maximize its own utility, the overall utility of the collaboration might drop. In the worst case scenario, grid resources are easily depleted due to selfish users taking free rides without offering any sharing resource. Unfortunately, such “tragedy of the commons” phenomenon also happens in a number of existing grid systems where cooperated scientific research grid systems emphasize on sharing resource voluntarily. Apparently, certain resource management scheme has to be implemented on grid systems to achieve better scalability[1-4,17].

To encourage resource sharing, several previous works adopt soft incentive schemes[5-7], which is essentially a reputation system. Nodes get higher degree of trust by sharing more resources, and thus have the permission to access other resources. Soft incentive cannot meet the requirement of grid systems in that providers not only care about the reputation, but also wish to gain benefit by providing resources. Other works adopt hard incentive scheme[1, 4], in which nodes get virtual currency by selling their resources, and then use the currency to bid for other resources. However, the assumption, wealthy nodes are more trustful, is not always valid. Simply considering the bid price in resource allocation cannot satisfy the security concerns from different participating organizations.

In order to tackle the mentioned above issues, we combine the soft incentive and hard incentive schemes and propose a Trust-Incentive Compatible Dynamic Resource Management framework, called TIM. The primary goals of TIM are securing shared resources, promoting users to share valuable resources, maintaining the balance of supply and demand in competitive grid resource market, and finally maximizing aggregate resource utilization. Major contributions are summarized as follows.

(1) By adopting a continual exchange process and matching user resource requests with available resources, we propose the TIM model which can maximize aggregate resource utilization in an economically and computationally efficient manner. In this model, users can get more only if they are willing to share more and having higher degree of trust. As a result, it promotes collaborators to share more valuable resources and avoid malicious waste.   
(2) In a grid system, price fluctuates when resource supply and demand changes. We separate the role of providers and consumers and apply different strategies to each role. Providers simply mark their price based on supply and demand while consumers offer their bids upon deadline and budget constraints. Because the resource dynamics are included in our management model, the workload of providers is balanced and the efficiency of grid system is improved.   
(3) Nodes may join or leave a grid system randomly. To prevent a system from being attacked by malicious nodes, we employ a weighted voting scheme in TIM, such that a secure environment is constructed.   
(4) We have successfully implemented TIM in the key project of our lab, CROWN grid. Our implementation experiences and experimental results are valuable to research peers.

# II. RELATED WORK

The objective of resource incentive is to promote users to share more resources. Generally speaking, there are two incentive schemes: Soft Incentive[5-7] and Hard Incentive [1, 4, 8-10].

Soft incentive includes two models, Peer-Approved and Service-Quality. Peers in [5] are allowed to access resources only from others with a lower or equal ratings, and the QoS provided to these peers also can be differentiated. Feldman [6] proposes a Reciprocative decision function, and introduces the notion of generosity. Richard et al. [7] present an allocation mechanism for bandwidth resource and introduce the notion of contribution to maximize utilization. In essence, soft incentive in above work is a reputation system where the reputation [5] (or generosity[6], contribution[7]) of a peer is consistent with the utility and quantity of resources supplied by the peer, but no price mechanism is involved in above systems.

There have been many researches in resource management approach which are based on economic models $[1, 4, 8-10]$ . Resource management based on price scheme can be treated as hard incentive, which adopts a Token-Exchange approach. Each first-time user might be allotted a fixed number of tokens, but once these run out, the user has to serve resources to earn tokens. Chun $[1]$ allocates resources using a combinatorial auction that allows users to express preferences with complementarities. Feldman $[8]$ presents a price-anticipating resource allocation mechanism. In their work, each user can reach the Nash equilibrium by iteratively applying a best response algorithm to adapt his bids. Resource allocation in above researches mainly considers the bid price of consumers, that is, the higher price the node bids, the more resources the node gets. However, wealthy nodes are not always with higher degree reputation. Only considering the bid price in resource allocation cannot satisfy the security concerns from different participating organizations.

The TIM we proposed combines features from both soft incentive approach and hard incentive approach. The framework is dynamic oriented and completely distributed. Such design allows better scalability when managing practical grid resources. The weighted voting scheme included in our work can decline suspicious nodes from joining the grid system and therefore maintaining a secure and balanced grid environment.

# III. SYSTEM MODEL

The key project in our lab, CROWN (China R&D Environment Over Wide-area Network), is aiming at empowering in-depth integration of resources and cooperation of researchers nationwide and worldwide. As illustrated in Fig. 1, the distributed resource management in CROWN grid adopts a two-tier peer-to-peer architecture[11-13]. The super layer is the backbone consisting of CDRSes (CROWN Distributed Resource Server); the child layer includes all clients and resource providers. Each club consists of one CDRS and multiple child nodes, such as $Club_{j}$ in Fig. 1. Each CDRS will periodically publish the provision resources. A child node selects the desired resource, generates the corresponding bids, and transmits them to the selected CDRS by its own parent CDRS.

We first propose our TIM model, including four building blocks, i.e. CHILD model, CLUB model, BIDS model, and TRUST model. Suppose that there are p clubs (that is, p CDRSes), and each club may have n types of resources. Let $Club_{j}$ denote the jth Club ( $j=1,\cdots,p$ ), and $Child_{j}^{i}$ denote the ith child node in $Club_{j}$ .

CHILD Model $Child_{j}^{i}$ is defined as $(S_{c_{j}^{i}}, E_{c_{j}^{i}}, Slot_{c_{j}^{i}}$

$$
, d i r e c t t r u s t _ {j} ^ {i}, r e v e n u e _ {j} ^ {i}): S _ {c _ {j} ^ {i}} = \left(s _ {c _ {j} ^ {i}} ^ {1}, s _ {c _ {j} ^ {i}} ^ {2}, \dots , s _ {c _ {j} ^ {i}} ^ {n}\right), E _ {c _ {j} ^ {i}} = \left(e _ {c _ {j} ^ {i}} ^ {1}, e _ {c _ {j} ^ {i}} ^ {2}, \dots , e _ {c _ {j} ^ {i}} ^ {n}\right),
$$

$Slot_{c_{j}^{i}}=(slot_{c_{j}^{i}}^{1},slot_{c_{j}^{i}}^{2},\cdots,slot_{c_{j}^{i}}^{n})$ to denote supply vector, excess vector, and time slot vector of $Child_{j}^{i}$ . $s_{c_{j}^{i}}^{t},e_{c_{j}^{i}}^{t},slot_{c_{j}^{i}}^{t}(t=1,\cdots,n)$ denotes supply quantity, demand quantity, and time slot of the tth resource type; a direct trust value $directtrust_{j}^{i}\in[0,1]$ in $Club_{j}$ ; a node revenue $revenue_{j}^{i}\in\mathbb{R}$ .

CLUB Model $Club_j$ is defined as $(num_j, S_j, D_j, E_j, P_j, \overline{P_j^{node}}$ , $Bids_j, RecTrust_j$ ): a children number $num_j \in N$ ; $S_j = (s_j^1, s_j^2,$

$$
\dots , s _ {j} ^ {n}), D _ {j} = (d _ {j} ^ {1}, d _ {j} ^ {2}, \dots , d _ {j} ^ {n}), E _ {j} = (e _ {j} ^ {1}, e _ {j} ^ {2}, \dots , e _ {j} ^ {n}), P _ {j} = (p _ {j} ^ {1},
$$

$p_{j}^{2},\cdots,p_{j}^{n})$ to denote supply vector, demand vector, excess vector, and price vector of the resources in $Club_{j}$ , respectively, where $s_{j}^{t},d_{j}^{t},e_{j}^{t},p_{j}^{t}$ ( $t=1,\cdots,n$ ) denote supply quantity, demand quantity, excess quantity and price of the $t$ th resource type; an average price of child node $\overline{P_{j}^{node}}=\sum_{t=1}^{n}s_{j}^{t}p_{j}^{t}/num_{j}$ ; a bids vector $Bids_{j}=(bids_{j}^{1},bids_{j}^{2},\cdots,bids_{j}^{m})$ received by $Club_{j}$ , and $bids_{j}^{q}$ is the $q$ th bid; a recommendation trust value vector $RecTrust_{j}=(rectrust_{j1},rectrust_{j2},\cdots,rectrust_{jp})$ , $rectrust_{ji}\in[0,1]$ is the recommendation trust value from CDRS in $Club_{j}$ to CDRS in $Club_{i}$ .

BIDS Model Bids is defined as $(cid, pid, et, Q, (q^{1}, q^{2}, ..., q^{n}), directtrust, C, V)$ : $cid \in \{1, \cdots, p\}$ , $pid \in N$ to denote the bid coming from $Child_{cid}^{pid}$ ; a estimated job execution time et; a desired quantity $Q \geq 1$ of nodes; $q^{1}, q^{2}, ..., q^{n}$ to denote the tth $(t = 1, \cdots, n)$ type resource quantity required by the consumer; a direct trust value $directtrust \in [0, 1]$ of the $Child_{cid}^{pid}$ ; a set of constraints C, such as deadline and budget, etc; and a bidding price V that the consumer is willing to pay.

![](images/fffe8590eb990bd3633a4ec494e6e59b5a1d8f0839873a7188d2f93742c962c8.jpg)



Figure 1. The two-tier architecture of TIM

TRUST Model We adopt the trust model used in [14]. If $T_{1}$ denotes a recommendation trust value from A to B, and $T_{2}$ denotes a direct trust value from B to C, then the trust value from A to C is $1 - (1 - T_{2})^{T_{1}}$ . We suppose that nodes in the same club have direct trust relations, nodes in different clubs have indirect trust relations, and CDRSes have recommendation trust relations. We get the following trust inference.

(1) Direct trust computing. After nodes in $Club_{i}$ use the resources of $Child_{i}^{k}$ to execute jobs, the nodes will report positive or negative experiences to the CDRS in $Club_{i}$ . A direct trust relationship will set up only if all experiences with $Child_{i}^{k}$ that the CDRS in $Club_{i}$ knows about are positive experiences. Let q be the number of positive experiences, then the direct trust value from the CDRS to $Child_{i}^{k}$ is $directtrust_{i}^{k}=1-\lambda^{q}$ , where $\lambda$ is the probability of reliability with a single task;   
(2) Recommendation trust computing. After nodes in $Club_{j}$ have used the resources of nodes in $Club_{i}$ to execute jobs, the nodes in $Club_{j}$ will report positive or negative experiences to the CDRS in $Club_{j}$ . Given numbers of positive and negative experiences p and n, the recommendation trust value from the CDRS of $Club_{j}$ to the CDRS of $Club_{i}$ is:

$$
\operatorname{rectrust} _ {j i} (p, n) = \left\{ \begin{array}{l l} 1 - \lambda^ {p - n} & \text { if   } p > n \\ 0 & \text { else } \end{array} \right.;
$$

(3) The trust value from $Club_j$ to $Child_i^k$ is :

$$
t r u s t _ {i} ^ {k} = 1 - (1 - d i r e c t t r u s t _ {i} ^ {k}) ^ {r e c t r u s t _ {j i}}.
$$

# IV. DESIGN OF TIM

In this section, we present our TIM framework to manage shared resources in CROWN.

# A. Provider price strategy

Smale Theorem [15]: For a market with n (n≥2) types of commodity, $P = (p_{1}, \cdots, p_{n})$ is the price vector at some moment, where $p_{i} \geq 0 (i = 1, \cdots, n)$ is the price of the ith commodity. Let D, S, E denote supply vector, demand vector, and excess vector of commodities (E=D-S), and D, S, E be the functions on the price vector P. If the equilibrium point of market exists, then $\mathrm{E}(\mathrm{P}^{*})=0$ , where $P^{*}$ denotes the equilibrium price. By default, the equilibrium point cannot be reached automatically. Rather, it can be reached only by continually adjusting the price according to $D_{E}(P)\times\frac{dP}{dt}=\mu E(p)$ , where $D_{E}(P)=(\frac{\partial e_{l}}{\partial p_{m}})_{n\times n}$ , $\frac{\partial e_{l}}{\partial p_{m}}$ denotes the partial derivative of the excess quantity of the lth type commodity to the price of the mth type commodity, and $\mu$ denotes a coefficient with the same sign as $D_{E}(P)$ .

In particular, it is impossible to use Smale's method directly [9] because grid economy is inherently discrete and the partial derivatives that the method requires do not exist. However, we are able to get good approximations for the partials at a given price vector. Starting with a price vector, the preferences at price vectors can be obtained by fixing all but one price and varying the remaining price slightly. Once achieving a "secant" approximation for each commodity, we substitute these approximations for the values of the partial derivatives in the matrix $D_E(P)$ , discretize with respect to time, solve for a price vector, and iterate.

Definition Let $S_{j}, D_{j}, E_{j}, P_{j}$ denote supply vector, demand vector, excess vector, and price vector in $Club_{j}$ , respectively. Obviously, $E_{j} = D_{j} - S_{j}$ , and $S_{j}, D_{j}, E_{j}$ are the functions of $P_{j}$ . If $E_{j}(P_{j}^{*}) = 0$ , then $Club_{j}$ reaches the balance, where $P_{j}^{*}$ is the equilibrium price. The unit of price is given in “grid dollars” (G\$).

In the grid, let the coefficient $\mu$ be 1, $dt$ be the step length of the time for adjusting per unit price, and $dP$ be the difference of two continues price. For example, suppose there are four types of resource in $Club_{j}$ , CPU, memory, disk, and bandwidth. The current price and excess vector are $P_{j}=(2G$, 6G$, 9G$, 4G$)$ and $E_{j}=(200, 0, 300, 100)$ . With the resource exchange records, the CDRS in $Club_{j}$ find that when the price of some resource is increased one unit, the increased supply quantity is 20 units, and the decreased demand quantity is 30 units. The decreased demand quantity of other types of resource is 10 units.

$$
\left[ \begin{array}{c c c c} - 2 0 - 3 0 & - 1 0 & - 1 0 & - 1 0 \\ - 1 0 & - 2 0 - 3 0 & - 1 0 & - 1 0 \\ - 1 0 & - 1 0 & - 2 0 - 3 0 & - 1 0 \\ - 1 0 & - 1 0 & - 1 0 & - 2 0 - 3 0 \end{array} \right] \left[ \begin{array}{l} \Delta p ^ {1} \\ \Delta p ^ {2} \\ \Delta p ^ {3} \\ \Delta p ^ {4} \end{array} \right] = \left[ \begin{array}{c} 2 0 0 \\ 0 \\ - 3 0 0 \\ 1 0 0 \end{array} \right]
$$

Thus, $\Delta p^1 = -5$ , $\Delta p^2 = 0$ , $\Delta p^3 = 7.5$ , $\Delta p^4 = -2.5$ . We use the following formula $max\{\varepsilon, p^k + \Delta p^k\}$ to determine a new resource price, where $\varepsilon > 0$ is a small constant preventing prices to approach zero value.

# B. Consumer price strategy

Each grid user generates the combination of resources for its tasks according to their requirements, and submits the corresponding combination to a selected CDRS that the user will bid for. The goal of each grid user is to maximize its own surplus upon deadline and budget constraints. Given the average price $\overline{P_{j}^{node}}$ of each node in the $Club_{j}$ and the completion time constraint T, the utility function of each grid user can be expressed as follows:

$$
U (V) = K (T - L \overline {{{{P _ {j} ^ {n o d e}}}}} / V) - V
$$

in which L is the length of the job, V is the payment value of the user, $LP_{j}^{node}/V$ is the estimated job execution time, and K is a constant coefficient defined by the user. Thus, the utility optimization problem above can be written as:

$$
\left\{ \begin{array}{l} \text {Max} U (V) \\ \text {s.t.} g (V) \geq 0 \end{array} \right. (g (V) = T - L \overline {{P _ {j} ^ {\text {node}}}} / V)
$$

By using the multiplicator method, we obtain the approximative optimal solution $V^{*} = 3L \overline{P_{j}^{node}} / (2T - K)$ as the bidding price, that is, the value V in BIDS model.

# C. Trust-incentive compatible resource allocation algorithm

After collecting the consumers' bids, the CDRS of each club uses the TIM mechanism to allocate resources as the following greedy algorithm.

TABLE I. TIM ALGORITHM 

<table><tr><td>1: Calculate the per unit valuation bid $_{j}^{i}$ =V $_{j}^{i}$ /(Q $_{j}^{i}$ ×et $_{j}^{i}$ ) for each bid in Club $_{j}$ </td></tr><tr><td>2: Scale each bid $_{j}^{i}$  using the formula b $_{j}^{i}$ =bid $_{j}^{i}$ /bid $_{j}^{max}$ </td></tr><tr><td>3: Calculate the evaluation value of each bid by evlbid $_{j}^{i}$ =α×b $_{j}^{i}$ +(1-α)×trust $_{cid}^{pid}$ , α∈[0,1] is risk degree of Club $_{j}$ </td></tr><tr><td>4: Sort all bids in descending order according to evlbid $_{j}^{i}$ </td></tr><tr><td>5: for all bids in the sorted bid list do</td></tr><tr><td>6: if the resource request for a bid can be fulfilled with the remaining node resources then</td></tr><tr><td>7: allocate the resources to the bid.</td></tr><tr><td>8: end if</td></tr><tr><td>9: end for</td></tr></table>

# D. Dynamic management for nodes

Nodes may join and leave the collaboration dynamically, or transfer from one club to another club. Thus, some CDRSes maybe have the trust records for a child node. In our TIM approach, the more resources a

node provides, the higher degree of trust a node has. Obviously, every node is willing to cooperate with a node with higher trust value.

As illustrated in Fig. 1, when the CDRS in $Club_{j}$ receives the join request, it will propagate the join request to other CDRSes. Since each club may have different trust records and recommendation trust value, it may have different opinions about the requesting node. In our proposal, this is solved by employing a weighted voting scheme to decide whether to accept the requesting node or not. After receiving the vote request, the CDRSes make their own decisions as:

$$
\text { vote } _ {i} = \left\{ \begin{array}{l l} 1 & \text { trust } > \tau \\ 0 & \text { no   trust   value   record } \\ - 1 & \text { trust } <   \tau \end{array} \right.
$$

where $\tau \in [0,1]$ is the configuration threshold value used by each CDRS. The result will then be returned to the voting sponsor. According to the majority principle, the CDRS in $Club_{j}$ uses the constraint in equation $\sum_{i=1}^{p} rectrust_{ji}vote_{i} \geq 0$ to make the final decision.

# V. IMPLEMENTATION

We have implemented the TIM approach in CROWN system with Java. The cooperation facility among nodes is provided by CROWN grid, a fully decentralized grid middleware infrastructure. In the setup phase, we created five clubs $[16]$ , and each club has a CDRS and 40-50 virtual child nodes.

# A. Efficiency of allocation mechanism

We first conduct an experiment with a set of five peers with varying currency and trust value, bidding for some portion of 200 unit resources. In the experiment, the amount of resource that each bid i can obtain is determined by $TotalResources \times evlbid^{i} / \sum_{i} evlbid^{i}$ . We adopt this distribution policy to protect light users against starvation from heavy users when the demand is over the supply. To evaluate TIM, we first define a metric named allocation\_ratio for each bid as follows.

$$
a l l o c a t i o n \_ r a t i o = a l l o c a t i o n \_ q u a n t i t y / t o t a l \_ r e q u e s t \_ q u a n t i t y
$$

In this experiment, we assume that the total request quantity of each node is 100 units. There are five curves in Figures 2 and 3, where x-axis represents the bids times, and y-axis represents the allocation ratio. We first set the risk degree $\alpha = 1$ in Fig. 2 and consider the security factor and set the risk degree $\alpha = 0.2$ in Fig. 3. The symbol S in both figures denotes the ratio of providing resources, for example, the first node provides 90 percent of local resources to other nodes. The symbol T in Fig. 3 denotes the trust value of bidding nodes. In the first three periods, only two nodes request for resources and the supply meets the demand. Thus the allocation ratios for the two nodes are all 100 percent. After the third period, the increasing bids outnumbered the supply.

![](images/7059bd034170f550f7a2b6e562821e34fd0eb3ff001ab280c16c8f4d26a2e28a.jpg)



Figure 2. .Incentive compatible allocation

![](images/37f3a37a9c084fb9167d58ebb4daf4b8b291a5d3364bfb9ea73af4cc7f86ea3e.jpg)



Figure 3. Trust incentive allocation

![](images/3ebcd0fb2253168602eac0bda5e01526aeb78d80d873026be0ffc06a08d4a591.jpg)



Figure 4. Completion ratio vs. dynamic system load

As shown in Fig. 2, without the security consideration, the nodes providing the same resources nearly obtain the same allocation ratio. However, if considering the trust value in Fig. 3, we can see that the provision ratio of node 3 (60%) is less than that of node 1 (90%), but node 3 has a higher trust value (T=0.6) and thus obtains more resources than node 1. Similarly, node 2 and node 4 have the same provision ratio: 30%. Node 2 obtains more resources than node 4 at the sixth bid in Fig. 3, because the trust value of node 2 (T=0.8) is far greater than that of node 4 (T=0.1).

# B. Impact of TIM price strategy

This experiment is to study characteristics of price setting strategy with Round-Robin strategy in terms of job completion time, which is measured from accessing the requested grid resources till task is accomplished. Three clubs are the resource providers, with each having 200 unit resources. Resource requests are generated by the child nodes and the bid is generated at an interval of 350 time units. We change the system load from 0.1 to 0.9 with a step of 0.1, where system load is defined as a ratio of aggregate bids load to aggregated capability of providers. The initial value of the resource price is 50G\$, and each CDRS re-publishes the resource price with an interval of 500 time units. In Fig. 4, we contrast the performance between TIM price direction strategy and Round-Robin strategy with system load at 0.4, 0.6, and 0.8, respectively. From Fig.4, we can see that TIM price setting strategy has better efficiency and spends less time to complete tasks compared with the Round-Robin strategy, especially at higher bids. At 10,000 time units, the completion ratio for Round-Robin strategy is only around 64%, while our price direction strategy can score 83% of the completion ratios.

# C. Evaluation of trust model

Malicious nodes may exist in grid environments to disturb resource exchange. We consider the security problem from both sides, including malicious consumers and malicious providers. On one hand, when bidding for resources, a malicious consumer can either set a higher bit value arbitrarily or does not give the corresponding payment. Such behaviors adversely affect the interests of resource providers. On the other side, a malicious provider can boast of having more resources to get more currency. It makes good providers losing the bids.

![](images/aa5618063976d020927b0398224d04cf12d517a2e6b9739deb27baba54648890.jpg)



Figure 5. Prevention of malicious consumers

![](images/3ff4d41fcf009400f67ffd5f0fa642297a569a766a2eb6e70f4f748332fbd957.jpg)



Figure 6. Prevention of malicious providers

![](images/6f6121c4659c8d9454b75b48a97aad0b5d4b9c582b858c406b4358454fd724d4.jpg)



Figure 7. Recommendation trust varying of CDRSes

We first study how malicious consumers affect the grid system. In this experiment, there are three clubs and 40 nodes in each club are resource providers. 100 nodes from the other two clubs act as consumers and generate bids. We let the three providing clubs receive the 100 bids each time by varying the percentage of malicious consumers from 0 to 0.9 with a step of 0.1. For each scenario, a set of risk degree $\alpha$ in TIM are configured: 0, 0.5, and 1. As shown in Fig. 5, the club considering both benefit and security factors ( $\alpha = 0.5$ ) obtains more revenue after the percentage of malicious consumers is over $20\%$ . When the percentage of malicious consumers is over $80\%$ , the club considering only the security factors will get more revenue.

We then study how malicious providers affect the grid system. In the simulations, $Club_{1}$ implements admission control based on the TIM weighted voting scheme, while $Club_{2}$ dose not. Both clubs have 40 resource providers and are handling 40 bids. Consider the case when 40 nodes from the other three clubs want to join $Club_{1}$ and $Club_{2}$ . Still, we set the percentage of malicious join peers from 0 to 0.9 with a step of 0.1. The CDRS in $Club_{1}$ set the admission policy $\tau=0.3$ , which means that the node whose trust value is lower than 0.3 will not be accepted. As a result, few malicious nodes are able to join $Club_{1}$ , while many of them can join $Club_{2}$ .

As Shown in Fig. 6, when the percentage of malicious join increases, the revenue of both clubs decreases. But the revenue of $Club_{2}$ without TIM is suffering much more than $Club_{1}$ with TIM. At the extreme case when all the new nodes are malicious nodes, the revenue of $Club_{2}$ is only 60 percent of the revenue of $Club_{1}$ . Fig. 7 shows that as more malicious nodes enter $Club_{2}$ , the recommendation trust value of the CDRS in $Club_{2}$ without TIM de crease rapidly.

# VI. CONCLUSION

Proving trust and incentive in grid computing environments are of great importance. This paper presents a Trust-Incentive Compatible Dynamic Resource Management, TIM, on the basis of economy model and trust model. By introducing the price strategy, trust-incentive compatible resource allocation mechanism and the weighted voting scheme, TIM encourages nodes to share more resources, ensures the balance of supply and demand, enhances the aggregated resource utilization, and maintains the secure environment of a grid computing system.

TIM scheme has been successfully implemented in our key project, CROWN grid environment. We evaluate our proposed approach by comprehensive experiments and achieved much improved results in resource allocation, system completion time and aggregated resource utilization.

In the future, we will widely deploy our TIM approach in the CROWN grid to construct a more secure and balanced collaborative grid environment.

# ACKNOWLEDGMENT

This work is supported by grants from the China National Science Foundation (Project No.90412011, No.60573053), China 863 High-tech Programme (Project No.2005AA115420) and China Major State Basic Research Development Program (Project No. 2005CB321803).

# REFERENCES

[1] B. Chun, J. Albrecht, D. Parkes, and A. Vahdat, "Computational Resource Exchanges for Distributed Resource Allocation," Technical Report, 2004.   
[2] Z. Zhu and X. Zhang, "Look-Ahead Architecture Adaptation to Reduce Processor Power Consumption," IEEE Micro, 2005.   
[3] K. Shen, H. Tang, T. Yang, and L. Chu, “Integrated Resource Management for Cluster-based Internet Services,” In Proceedings of the 5th symposium on Operating Systems Design and Implementation, 2002.   
[4] C. Yeo and R. Buyya, "Pricing for Utility-driven Resource Management and Allocation in Clusters," In Proceedings of the 12th International Conference on Advanced Computing and Communication, 2004.   
[5] K. Ranganathan, M. Ripeanu, A. Sarin, and I. Foster, “To Share or not to Share: an Analysis of Incentives to Contribute in Collaborative File Sharing Environments,” In Proceedings of Workshop on Economics of Peer to Peer Systems, 2003.   
[6] M. Feldman, K. Lai, I. Stoica, and J. Chuang, “Robust Incentive Techniques for Peer-to-Peer Networks,” In Proceedings of ACM E-Commerce Conference, 2004.   
[7] T. Ma, S. Lee, J. Lui, and D. Yau, "A Game Theoretic Approach to Provide Incentive and Service Differentiation in P2P Networks," In Proceedings of ACM SIGMETRICS/PERFORMANCE, 2004.   
[8] M. Feldman, K. Lai, and L. Zhang, "A Price-Anticipating Resource Allocation Mechanism for Distributed Shared Clusters," In Proceedings of ACM E-Commerce Conference, 2005.   
[9] R. Wolski, J. Brevik, J. S. Plank, and T. Bryan, "Grid Resource Allocation and Control Using Computational Economies," In Proceedings of Grid Computing: Making the Global Infrastructure a Reality, 2003.   
[10] A. Das and D. Grosu, “Combinatorial Auction-Based Protocols for Resource Allocation in Grids,” In Proceedings of the 19th IEEE International Parallel and Distributed Processing Symposium, 2005.   
[11] Z. Zhuang, Y. Liu, and L. Xiao, “Dynamic Layer Management in Super-peer Architectures,” In Proceedings of the 33th International Conference on Parallel Processing, 2004.   
[12] S. Banerjee, C. Kommareddy, K. Kar, B. Bhattacharjee, and S. Khuller, "Construction of an Efficient Overlay Multicast Infrastructure for Real-time Applications," In Proceedings of INFOCOM, 2003.   
[13] R. Ranjan, A. Harwood, and R. Buyya, “Grid Federation: An Economy Based, Scalable Distributed Resource Management System for Large-Scale Resource Coupling,” Grid Computing and Distributed Systems Laboratory, University of Melbourne, Australia, Technical Report, 2004.   
[14] T. Beth, B. Malte, and K. Birgit, “Valuation of Trust in Open Networks,” In Proceedings of the Conference on Computer Security, 1994.   
[15] S. Smale, “Dynamic in General Equilibrium Theory,” American Economic Review, 1976.   
[16] J. Huai, Y. Zhang, X. Li, and Y. Liu, “Distributed Access Control in CROWN Groups,” In Proceedings of the 34th International Conference on Parallel Processing, 2005.   
[17] Y. Liu, X. Liu, L. Xiao, L. Ni, and X. Zhang, "Location-Aware Topology Matching in P2P Systems," IEEE INFOCOM, Hong Kong, March 2004.