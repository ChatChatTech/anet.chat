# Towards Efficient Mechanisms for Mobile Crowdsensing

Xinglin Zhang, Member, IEEE, Zheng Yang, Member, IEEE, Yunhao Liu, Fellow, IEEE, Jianqiang Li, and Zhong Ming

Abstract—Mobile crowdsensing systems aim at providing various novel applications by employing pervasive smartphones. A key factor to enable such systems is substantial participation of normal smartphone users, which requires effective incentive mechanisms. In this paper, we investigate incentive mechanisms for online scenarios, where users arrive and interact with a task requester in a random order, and they have preferences (e.g., photographing) or limits (e.g., travel distance) over the sensing tasks. In existing online mechanisms, the task requester has limited power in assigning tasks to the selected users, i.e., it has to pay for the whole bunch of tasks specified by the selected users, even though some of these tasks are of little value. To accommodate this, we investigate a more flexible setting, where the requester can actively assign most valuable tasks to the selected users. We design two online incentive mechanisms motivated by sampling-accepting process and weighted maximum matching. We prove that the designed mechanisms achieve computational efficiency, individual rationality, budget feasibility, truthfulness, consumer sovereignty, and constant competitiveness. By carrying out extensive experiments on two real-world geographical datasets, we demonstrate the practical applicability of the proposed mechanisms.

Keywords-Crowdsensing; Incentive Mechanism; Crowdsourcing; Auction

# I. INTRODUCTION

Mobile crowdsensing [1] is an emerging problem solving paradigm that employs large amounts of normal smartphone users to collect diverse information, such as images, sounds, locations, and mobilities. With the collected data, researchers are able to implement various sensing applications that penetrate into multiple aspects of people’s life [2], such as traffic monitoring [3], pollution monitoring [4], location-based queries [5], and indoor localization [6], [7].

The enabling factors for mobile crowdsensing are twofold: large quantity of smartphone users and technology improvement of smartphones and communications. On one hand,

Copyright (c) 2015 IEEE. Personal use of this material is permitted. However, permission to use this material for any other purposes must be obtained from the IEEE by sending a request to pubs-permissions@ieee.org.

This work was supported in part by the National Natural Science Foundation of China under Grant No. 61502178, Natural Science Foundation of Guangdong Province under Grant No. 2016A030313480, and the China Postdoctoral Science Foundation under Grant No. 2015M572318. (Corresponding author: Zhong Ming.)

X. Zhang is with the College of Computer Science and Software Engineering, Shenzhen University, China, and the School of Computer Science and Engineering, South China University of Technology, China. E-mail: zhxlinse@gmail.com.

Z. Yang and Y. Liu are with the School of Software and National Lab for Information Science and Technology (TNLIST) , Tsinghua University, China. E-mail: {yang, yunhao}@greenorbs.com.

J. Li and Z. Ming are with the College of Computer Science and Software Engineering, Shenzhen University, China. E-mail: {lijq, mingz}@szu.edu.cn.

according to International Data Corporation (IDC), the shipment of smartphones reached 1 billion in 2013 [8], which implies a large crowd of potential participants for mobile crowdsensing applications. On the other hand, besides the powerful computation and communication capability, off-theshelf smartphones are equipped with multiple sensors. Along with users round-the-clock, smartphones have become a multimodal interface between users and environments. Hence the smartphone users may constitute a large scale sensing network that can be used to accomplish the aforementioned sensing applications.

A critical observation is that, only when the above enabling factors are bridged effectively, i.e., a large amount of users indeed participate in sensing tasks by using their smartphones, can the crowdsensing systems operate normally and benefit people. However, smartphone users may be reluctant to participate due to resource consumption and privacy risk. Therefore, researchers have delved into designing effective auction-based incentive mechanisms to motivate users [9], [10].

Early mechanisms for crowdsensing [11], [12] assume an offline scenario, where the concurrent presence of users submitting their bidding profiles is required. Then the task requester selects a subset of users based on all submitted bidding profiles to maximize its utility. In practice, however, users usually arrive online in a random order, making the mechanisms for the offline setting invalid. Considering this fact, recent studies [13], [14] start to investigate online incentive mechanisms, in which the task requester makes an irrevocable decision on whether to accept a user, based on the information of the users who have arrived earlier. These incentive mechanisms have been proved to satisfy desirable properties of a good mechanism. Yet they restrain the selection power of the task requester, and hence prevent the requester from maximizing its value. Specifically, in these mechanisms, it is assumed that each user submits a bidding price for a subset of designated tasks based on her preferences (e.g., photographing) or limits (e.g. travel distance). The requester can only select a user and pay for the whole bunch of tasks specified by that user, even though some of these tasks are of little value.

In this work, we consider a more flexible online setting, where the task requester can actively assign tasks to the selected users, such that it can receive more value and the mechanism can achieve higher social efficiency. In our model, a task requester, who has a set of heterogenous sensing tasks and a limited budget, aims at selecting a subset of online users and assigning them most valuable tasks before a specified deadline, such that its total value is maximized. There is a pool of users to do the tasks. Each user is interested in a subset of tasks, and has a minimum cost for doing a task. The users are assumed to be game-theoretic. Hence they would like to maximize their utilities, by strategically reporting untruthful bidding profiles. This model is widely applicable to crowdsensing applications, such as reporting traffic conditions on road segments of interest, taking photos of landmarks, and monitoring the parking space in different spatial regions, where car drivers and passengers are potential users. Users’ destinations and available time influence the sets of tasks that they are willing to complete; while the task requester can actively determine which user to recruit and which task should be assigned in order to achieve maximum utility.

Under this setting, we design two effective online incentive mechanisms by adopting a sampling-accepting process. Generally, we observe a fraction of the online users (sampling stage). These observed users and the tasks they are interested in are organized as a bipartite graph. Then we find the weighted maximum matching under the budget constraint. This matching includes the key information, with which we can make an informed decision on recruiting users (accepting stage). Furthermore, the whole process is implemented in an iterative manner to ensure some desirable properties. In summary, we prove that the proposed online incentive mechanisms satisfy the following properties: computational efficiency, individual rationality, budget feasibility, truthfulness, consumer sovereignty, and constant competitiveness. Informally, computational efficiency makes the mechanism applicable in real time; Individual rationality and consumer sovereignty guarantee user benefits by ensuring nonnegative utility and nonzero probability for being selected; Truthfulness, on the other hand, pushes users to reveal their true parameters to the requester; Budget feasibility and constant competitiveness ensure that the requester’s budget is not violated and its total value obtained by the mechanism is close to the optimal solution obtained in the offline scenario.

We also evaluate the performance of the designed mechanisms by conducting extensive experiments on two real-world geographical datasets (Gowalla and T-drive). The experimental results demonstrate the practical applicability of the proposed mechanisms.

The rest of the paper is organized as follows. We first formulate the problem in Section II. In Section III and Section IV, the proposed mechanisms are illustrated and analyzed in detail. We carry out extensive experiments to evaluate the performance of the proposed mechanisms in Section V. Finally, we discuss related work in Section VI and conclude our work in Section VII.

# II. PROBLEM FORMULATION

In this section, we first illustrate the crowdsensing model and basic assumptions. Then we introduce the structure of our incentive mechanisms based on the online auction and the mechanism design principles.

![](images/969700fce023e9cfdf40f823a1ebe7ea9e5d3900c6af127f1715468a04ea3b0e.jpg)



Fig. 1. Interaction flow of online incentive mechanisms. Users are divided into 3 types. Type 1 submits a bid but fails; Type 2 does not submit a bid; Type 3 submits a bid and wins.

# A. Crowdsensing Model

Fig. 1 sketches the basic interaction flow between a sensing task requester and a set of online users. The task requester may reside on the cloud or consist of several sensing servers. The requester possesses a set of heterogeneous sensing tasks $\mathcal { Q } = \{ 1 , 2 , . . . , m \}$ , a budget B, and a recruitment deadline $T$ for selecting users. Each task $j \in \mathcal { Q } ,$ if completed by a user, will bring a fixed profit $v _ { j }$ to the requester.

A crowd of users $\mathcal { U } = \{ 1 , 2 , . . . , n \}$ appear randomly online to submit their bidding profiles to the requester, where n is unknown. Users can connect with the requester through wireless network technologyies, such as cellular networks and WiFi connections. The true value (or truthful) profile of user i is a tetrad $\theta _ { i } = \{ a _ { i } , d _ { i } , c _ { i } , \mathcal { Q } _ { i } \}$ , where $a _ { i } \in \{ 1 , 2 , . . . , T \}$ denotes the arrival time, $d _ { i } \in \{ 1 , 2 , . . . , T \}$ denotes the departure time, $c _ { i }$ is the true cost of accomplishing one sensing task, and $\mathcal { Q } _ { i } \subseteq \mathcal { Q }$ is the subset of designated tasks that user i is willing to complete. Note that a user’s preference or limit over certain tasks relies on various factors, such as the location of the task, the labor intensity of the task, and the type of the task [15]. Similar to existing work [5], [16], we assume that each user will be assigned at most one sensing task in one round of the auction, based on the following observations. First, for some application scenarios, users can only complete one sensing task. For example, when a user is moving towards a destination and the tasks she can complete are scattered in different routes, she will do one task at a time to avoid an expensive detour. Such tasks include taking photos of landmarks on different streets and reporting parking space over different regions. Second, whenever a user finishes a task, she is able to participate in the sensing auction again, hence it is also convenient for the user to control her participation level.

We consider two models with respect to the interval between

the arrival time and the departure time of a user:

• Zero arrival-departure interval model (Z-model): Each user i arrives and departs at the same time, i.e. $a _ { i } = d _ { i }$ .   
• General arrival-departure interval model (G-model): Each user i may depart immediately or stay in connection with the task requester for a period after arriving, i.e., $a _ { i } \leq d _ { i }$ .

Z-model is a special case of G-model. We discuss Z-model separately as mechanism design for Z-model is simpler and focuses on a key problem of cost truthfulness (introduced in Section II-C). Then we consider G-model, where we need to consider both cost and time truthfulness (introduced in Section II-C). As we have solved the cost truthfulness problem in Z-model, we pay more attention on time truthfulness in Gmodel. From the application aspect, Z-model is suitable for the scenario where the decision has to be made immediately. For example, in LiFS [6], users may receive task descriptions when they enter the targeted building. Then they submit bidding profiles and expect the system to reply immediately, since they may not want to be disturbed anymore when they are working or shopping in that building. Nevertheless, in other scenarios, smartphone users may be patient and stay in connection with the task requester for some time interval. For example, when a user is staying in a traffic tool or drinking at a coffee shop, she may play with the requester for some time. In such scenarios, we apply G-model, where the requester will put off the decision until when the user leaves.

# B. Online Auction

The incentive mechanism is modeled as an online auction. A user will submit a bidding profile upon receiving task lists, demonstrating her sensing capacity and cost. Then the task requester has to make an online decision whether to recruit this user or not. If the user is selected, the requester determines which task is assigned to the user and how much is paid in exchange before the user departs. Note that the requester has a total budget B, which serves as the maximum amount that can be paid to the selected users. The requester expects to maximize the total value obtained from the selected users under the budget.

We assume that users who participate in the bidding process are game-theoretic and tend to strategically submit their bidding profiles in order to maximize payments for them. When interacting with the requester, the true cost and arrival/departure time of user i are private and only known to herself. In Z-model, user i can only manipulate her bidding price $b _ { i }$ strategically so as to achieve a higher utility. While in G-model, we adopt the online direct revelation mechanism [17], where user i can declare a bidding profile $\theta _ { i } ^ { \prime } = \{ a _ { i } ^ { \prime } , d _ { i } ^ { \prime } , b _ { i } , \mathcal { Q } _ { i } \}$ , where $a _ { i } \leq a _ { i } ^ { \prime } \leq d _ { i } ^ { \prime } \leq d _ { i }$ . In other words, user i cannot report an earlier arrival (or a later departure) time than her true arrival (or departure) time. Note that the task subset Qi is selected by user i based on her preferences (such as taking pictures of her interest, or doing tasks on her way home), which inherently optimizes her utility. Therefore, we assume that users reveal preferred tasks truthfully.

Formally, an online mechanism $\mathcal { M } = ( f , g )$ consists of two components, an allocation function f and a payment function g. The allocation function f decides whether to select each arrived user and which task to be assigned to each selected user based on the knowledge of the users who arrive earlier. The payment function g returns a vector $p = \{ p _ { 1 } , p _ { 2 } , . . . , p _ { n } \}$ of payments to users.

We model the relation between users and tasks as a bipartite graph $\mathcal { G } ( \{ \mathcal { U } , \mathcal { Q } \} , E )$ , where U is the set of users, Q is the set of heterogenous sensing tasks, and E is the set of all edges. Each edge $e = ( i , j ) \in E$ in the graph $\mathcal { G }$ represents that user $i \in \mathcal { U }$ is interested in doing sensing task $j \in \mathcal { Q } .$ . For simplicity, we use $\mathcal { G } ( E )$ to represent $\mathcal { G } ( \{ \mathcal { U } , \mathcal { Q } \} , E )$ in the following. We also denote $\mathcal { U } ( E )$ and Q(E) as the set of users and tasks that have adjacent edges in E, respectively. The objective of selecting users and assigning them tasks is equivalent to finding a matching in the bipartite graph. Let $M \subseteq E$ be the matching returned by running an online incentive mechanism. Then the utility of user i is

$$
u _ {i} = \left\{ \begin{array}{l l} p _ {i} - c _ {i}, & \text { if } i \in \mathcal {U} (M), \\ 0, & \text { otherwise }, \end{array} \right. \tag {1}
$$

where $\boldsymbol { \mathcal { U } } ( \boldsymbol { M } )$ is the set of user nodes in the matching M , and $p _ { i }$ is the payment for user i.

The total value of the requester is simply the sum of the values of completed tasks, $\begin{array} { r } { { \boldsymbol { u } } ( { \boldsymbol { M } } ) ~ = ~ \sum _ { j \in { \mathcal { Q } } ( { \boldsymbol { M } } ) } { \boldsymbol { v } } _ { j } } \end{array}$ , where $\mathcal { Q } ( M )$ is the set of assigned tasks in the matching M . Then the objective of the mechanism is to maximize the total utility under the budget B:

$$
\max u (M) \text {   s.t.   } \sum_ {i \in \mathcal {U} (M)} p _ {i} \leq B. \tag {2}
$$

# C. Design Principles

As is common to algorithm mechanism design, the goal of our online incentive mechanisms is manifold [13], [14], [18]. Specifically, we seek online mechanisms that satisfy:

• Computational Efficiency: An online mechanism is computationally efficient if the allocation and payment functions can be computed in polynomial time.   
• Individual Rationality: Each participating user i will get a nonnegative utility upon completing the sensing task, i.e., $u _ { i } \geq 0$ .   
• Budget Feasibility: The requester’s total payment should not exceed the given budget, i.e., $\begin{array} { r } { \sum _ { i \in \mathcal { U } ( M ) } p _ { i } \le B } \end{array}$ .   
• Truthfulness: A mechanism is called cost-truthful and time-truthful if reporting the true cost and arrival/departure time is a dominant strategy for each user. In other words, a user cannot improve her utility by submitting a bidding price or arrival/departure time deviating from her true value in spite of others’ bidding profiles.   
• Consumer Sovereignty: A mechanism satisfies consumer sovereignty when each user has a chance to be selected if only her bidding price is sufficiently low while others’ bids are fixed.   
• Competitiveness: To evaluate the performance of a designed mechanism considering value maximization, we compare its solution with the optimal solution in the offline setting, where the requester has the full knowledge

of users’ truthful profiles. A mechanism is $O ( g ( n ) ) .$ - competitive if the ratio between the solution of the designed mechanism and the optimal solution is $O ( g ( n ) )$ . Ideally, we would like to seek O(1)-competitive mechanisms.

# III. MECHANISM UNDER Z-MODEL

In this section, we design an online Incentive Mechanism for Crowdsensing systems under Z-model (IMC-Z), where the arrival time of each user coincides with the departure time. In this case, achieving time-truthfulness is trivial, as users cannot report a later arrival time or an earlier departure time. We assume that no two users arrive at the same time. This assumption can be removed in the mechanism developed for G-model.

Algorithm 1 IMC-Z   
Input: Budget B, Deadline T, Task set Q
Output: Matching M, Payment vector p
1: $(t, T', B', \rho) \leftarrow (1, \frac{T}{2^{\lfloor \log_{2} T \rfloor}}, \frac{B}{2^{\lfloor \log_{2} T \rfloor}}, \epsilon);$ 2: $(\mathcal{G}(E), M, M') \leftarrow (\emptyset, \emptyset, \emptyset);$ 3: while $t \leq T$ do
4: if there is a user i arriving at time t then
5: Add user i, task set $Q_i$ , and edge set $\{(i, j) | j \in Q_i\}$ to $\mathcal{G}(E);$ 6: $(M, p_i) \leftarrow \text{Selection}(\mathcal{Q}_i, b_i, M, M', \rho);$ 7: end if
8: if $t = \lfloor T' \rfloor$ then
9: $(M', \rho) \leftarrow \text{GetThreshold}(B', \mathcal{G}(E));$ 10: $T' \leftarrow 2T'; B' \leftarrow 2B';$ 11: end if
12: $t \leftarrow t + 1;$ 13: end while

# A. IMC-Z Design

The challenges of designing an online inventive mechanism are manifold. For the task requester, the total payment cannot exceed the given budget and the recruitment process cannot exceed the deadline. For the users, the mechanism needs to encourage them to bid honestly and cope with the online arrival behavior. A common approach is to observe a fraction of the online users (sampling stage) and then use their bidding profiles to make an informed decision on the rest of the users (accepting stage). We use a similar strategy with multiple sampling-accepting stages: it dynamically increases the sample size, as well as the stage budget it uses for recruitment at each stage, and learns threshold parameters for the following stages. The potential of the strategy lies in that, if designed carefully, it is possible to achieve consumer sovereignty and a good approximation ratio. Therefore, we follow this structure and design IMC-Z.

Algorithm 1 sketches the recruitment process of IMC-Z. The total time interval is divided into the following stages: $1 , 2 , . . . , \lfloor \log _ { 2 } T \rfloor , \lfloor \log _ { 2 } T \rfloor + 1$ . Each stage i ends at time step $T ^ { \prime } = \bar { ( 2 ^ { i - 1 } T / 2 ^ { \lfloor \log _ { 2 } T \rfloor } } )$ . Accordingly, the budget distributed for stage i is $B ^ { \prime } = \lfloor 2 ^ { i - 1 } B / 2 ^ { \lfloor \log _ { 2 } T \rfloor } \rfloor$ . If there is a user i arriving at time step t, the mechanism integrates user i, as well as her preferred tasks and the corresponding edges, into the bipartite graph $\mathcal { G } ( E )$ (line 5), which is used to compute the threshold parameters at the end of each stage (line 9). Also, it checks whether user i is worth recruiting by a thorough checking (line 6).

We now explain the parameter construction scheme (Algorithm 2) and user selection procedure (Algorithm 3). Algorithm 2 is adapted from [19]. It takes a stage budget $B ^ { \prime }$ and a current bipartite graph $\mathcal { G } ( E )$ as inputs, and tries to find the maximum matching $M ^ { \prime }$ by using a uniform payment strategy, i.e., all the selected users are paid an equal amount. The key concept here is the buck per bang (b/b) rate of a matching, which represents the amount of money that the mechanism is willing to pay per unit of value. Formally, the b/b rate of an edge $e \ : = \ : ( i , j )$ , denoted by $b b ( e )$ , is defined by $b _ { i } / v _ { j }$ . We sort the edges of $\mathcal { G } ( E )$ as $e _ { 1 } , e _ { 2 } , . . . , e _ { | E | }$ , where the edges are listed in non-ascending order with respect to their b/b rates. We also add an isolated dummy edge $e _ { 0 }$ before $e _ { 1 } .$ , and let e0 has b/b equal to infinity. Then, the algorithm starts with $\rho = b b ( e _ { 0 } )$ .

The user nodes are visited one by one in users’ arrival order. When user i is visited, she is assigned with the task of the highest value among the available tasks linked to her. $M ^ { \prime }$ represents the matching produced after running through all the users in $\mathcal { U } ( E ^ { \prime } )$ , which is the dynamic set of users who have adjacent edges (lines 4–7). If $b b ( e _ { k } ) \cdot u ( M ^ { \prime } ) > B ^ { \prime }$ , it means that we cannot afford the matching and we decrease the b/b rate slightly (line 12). This procedure repeats until we find a satisfied matching.

In Algorithm 3, when user i arrives, we first sort her preferred tasks with respect to the task values in non-ascending order. Then we start selection from the most valuable task. We examine user $i \ ' s$ b/b rate. If $\dot { b } _ { i } / v _ { j } \le \rho ,$ where $\rho$ is calculated in Algorithm 2, we further check whether the remaining budget is sufficient to pay user i and, necessarily, whether task j has been assigned to another user (line 3). The qualified user will be paid according to the threshold, and the matching M are updated accordingly (line 5). Note that when the time step t is larger than $\lfloor T / 2 \rfloor$ , we need to ensure that the selected task has to be in the matching $M ^ { \prime }$ calculated by the profiles of users arriving before $\lfloor T / 2 \rfloor$ . This operation is useful for guaranteeing the competitiveness of the mechanism in the proof of Lemma 6.

# B. IMC-Z Analysis

First we show that IMC-Z is computationally efficient.

Lemma 1: IMC-Z is computationally efficient.

Proof: We consider each time step t. The most time consuming operations are the user selection procedure (Algorithm 3) and the threshold calculation (Algorithm 2). In Algorithm 3, the available tasks for user i are sorted with respect to task values in non-ascending order, which takes $O ( m \log m )$ time. Also, verifying a matched task takes at most $O ( m )$ time. In total, it takes $O ( m ^ { 2 } \log m )$ time for selection procedure. In Algorithm 2, sorting the edges of graph $\mathcal { G } ( E )$ takes $O ( n \log n )$ time. The outer for-loop (line 2) is bounded by mn, assuming that at each time step there is an arriving user and each user can do all tasks. The inner for-loop (line 4) is also bounded by mn, as the selected set $| \mathcal { U } ( E ^ { \prime } ) | \leq$ n and $| \mathcal { Q } _ { i } | \le m$ . Therefore, Computing the threshold takes ${ \dot { O } } ( m ^ { 2 } n ^ { 2 } )$ time. In summary, the time complexity of IMC-Z is dominated by the threshold computing operation. □

Algorithm 2 GetThreshold   
Input: Budget $B'$ , Graph $\mathcal{G}(E)$ Output: Matching $M'$ , Threshold $\rho$ 1: $E' \leftarrow E; \rho \leftarrow \infty;$ 2: for $k \leftarrow 1$ to $|E|$ do

3: $M' \leftarrow \emptyset;$ 4: for $i \in \mathcal{U}(E')$ in arrival order do

5: Find available task $j \in Q_i$ with the highest value;

6: $M' \leftarrow M' \cup (i, j);$ 7: end for

8: if $bb(e_k) \cdot u(M') \leq B'$ then

9: $\rho \leftarrow \min(\frac{B}{u(M')}, bb(e_{k-1}));$ 10: break;

11: end if

12: $E' \leftarrow E' - \{e_k\};$ 13: end for

Lemma 2: IMC-Z is individually rational.

Proof: The payment is determined in Algorithm 3. If user i is not selected to participate, she will receive zero payment (line 1). Otherwise, according to the condition $b _ { i } \leq \rho \cdot v _ { j }$ , the payment $p _ { i } = \rho \cdot v _ { j } \geq b _ { i }$ (line 5). ■

Algorithm 3 Selection   
Input: User i's task set $Q_{i}$ and bidding price $b_{i}$ , Matching M, $M'$ , Threshold $\rho$ Output: Matching M, Payment $p_{i}$ 1: $p_{i} \leftarrow 0$ ;

2: for $j \in Q_{i}$ in non-ascending order w.r.t. $v_{j}$ do

3: if $b_{i} \leq \rho \cdot v_{j} \leq B' - \sum_{i' \in \mathcal{U}(M)} p_{i'}$ and $j \notin \mathcal{Q}(M)$ then

4: if $t < \lfloor \frac{T}{2} \rfloor$ or ( $t \geq \lfloor \frac{T}{2} \rfloor$ and $j \in \mathcal{Q}(M')$ ) then

5: $p_{i} \leftarrow \rho \cdot v_{j}; M \leftarrow M \cup (i, j)$ ;

6: break;

7: end if

8: end if

9: end for

Lemma 3: IMC-Z is budget feasible.

Proof: To prove the budget feasibility, it suffices to show that at each stage, the payment $\textstyle \sum _ { i ^ { \prime } \in { \mathcal { U } } ( M ) } p _ { i ^ { \prime } }$ does not exceed the distributed budget $B ^ { \prime } .$ , which is guaranteed in Algorithm 3 by the user selection condition $\begin{array} { r } { B ^ { \prime } - \sum _ { i ^ { \prime } \in \mathcal { U } ( M ) } p _ { i ^ { \prime } } \geq \rho \cdot v _ { j } } \end{array}$ (line 3) and the payment assignment scheme (line 5).

Lemma 4: IMC-Z satisfies consumer sovereignty.

Proof: At each sampling stage $1 , 2 , . . . , \lfloor \log _ { 2 } T \rfloor$ , despite aggregating the information of the observed users for constructing an informed b/b threshold, we also distribute a budget for actually selecting some winning users and pay them accordingly. Therefore, no user is automatically rejected during each sampling stage. Each user with a higher b/b than that of the stage threshold will be selected if the distributed budget has not been exhausted.

Note that under Z-model, the truthfulness is equivalent to cost-truthfulness. To facilitate proving the truthfulness of an online mechanism, we need the concept of bid-independence.

Definition 1 (Bid-independence): An online mechanism $\mathcal { M } = ( f , g )$ is bid-independent if the payment function for user i depends only on the previous bidding users, and not on $b _ { i } .$ .

In other words, for the sequence of bids $b _ { 1 } , b _ { 2 } , . . . , b _ { i - 1 }$ and the two choices for user $i \ ' s$ bid, $b _ { i }$ and $b _ { i } ^ { \prime } ,$ the payment $p _ { i }$ for user i satisfies $p _ { i } ( b _ { 1 } , . . . , b _ { i - 1 } , b _ { i } ) \ = \ p _ { i } ( b _ { 1 } , . . . , b _ { i - 1 } , b _ { i } ^ { \prime } )$ . The following proposition presents the link between bidindependence and truthfulness.

Proposition 1: (Proposition 2.1 [20]) An online auction is truthful if and only if it is bid-independent.

Therefore, we only need to prove that Algorithm 1 designs a bid-independent payment scheme.

Lemma 5: IMC-Z is truthful.

Proof: Consider user i arriving at time step t. If the budget has been exhausted at t, which means that the previous users have shared all the budget, then the payment for user i is zero. If the budget left is sufficient, we have two cases: 1) User i is not selected due to the conditions in Algorithm 3 (line 3) based on the information of previous users, then the payment given to user i is zero; 2) User i is selected and is paid $p _ { i } = \rho \cdot v _ { j }$ , where $\rho$ is the b/b threshold computed from the previous stages. In summary, the payment for user i is determined by the sequence of previous bidding users, and hence Algorithm 1 is bid-independent.

We analyze the competitiveness of IMC-Z by using the property of the threshold computation scheme in Algorithm 2. Note that given a fixed weighted bipartite graph $\mathcal { G } ( E )$ and a budget B, using b/b as a uniform payment rate in finding the maximum matching in Algorithm 2 gives a 3-competitive result compared to the optimal solution.

Lemma $6 \mathrm { : }$ IMC-Z is constant competitive.

Proof: We first show that at $\begin{array} { r } { t = \lfloor \frac { T } { 2 } \rfloor } \end{array}$ ⌋, Algorithm 2 returns a matching $M _ { 1 } ^ { \prime }$ that has an approximation of 6 given the budget $\begin{array} { l } { { \frac { B } { 2 } } } \end{array}$ and the bidding information of the observed users before t (bipartite graph $\mathcal { G } ( E ^ { t } ) )$ , compared to the optimal matching $M ^ { * }$ obtained with all the bidding users’ information (global bipartite graph $\mathcal { G } ( E ^ { T } ) )$ . Let $M _ { 1 } \stackrel { - } { = } E ^ { t } \cap M ^ { * }$ and $M _ { 2 } = M ^ { \ast } \cap$ $( \bar { E } ^ { T } \backslash E ^ { t } )$ . As users arrive in a random order, the sample edge set $E ^ { t }$ is a random set of all edges. Therefore, the number of edges from $M ^ { * }$ in $E ^ { t }$ follows a hypergeometric distribution $H ( n / 2 , | M ^ { * } | , n )$ . Thus, we have

$$
\mathbb {E} [ | M _ {1} | ] = \mathbb {E} [ | M _ {2} | ] = \frac {| M ^ {*} |}{2}.
$$

The value of each edge can be seen as an i.i.d. random variable, and due to the linearity of the requester’s value $u ( M )$ , we have

$$
\mathbb {E} [ u (M _ {1}) ] = \mathbb {E} [ u (M _ {2}) ] = \frac {u (M ^ {*})}{2}.
$$

The expected total payments for users (or edges) from $M _ { 1 }$ and $M _ { 2 }$ are $B / 2 .$ . Since $u ( M _ { 1 } ^ { \prime } )$ is computed with the budget $B / 2$ by Algorithm 2, it can be derived that

$$
3 \mathbb {E} [ u (M _ {1} ^ {\prime}) ] \geq \mathbb {E} [ u (M _ {1}) ] = \frac {u (M ^ {*})}{2}.
$$

Therefore, we have

$$
\mathbb {E} [ u (M _ {1} ^ {\prime}) ] \geq \frac {u (M ^ {*})}{6}.
$$

At the last recruitment stage, i.e. after the time step $t =$ $\lfloor { \frac { T } { 2 } } \rfloor$ , for each task node $j \in \mathcal { Q } ( M _ { 1 } ^ { \prime } )$ , there is a probability of $\frac { 1 } { 2 }$ that its least-cost adjacent edge is in the period $( \lfloor \frac { T } { 2 } \rfloor , T )$ . Therefore, according to the comparison conditions in line 4 of Algorithm 3, we guarantee that

$$
\mathbb {E} [ u (M _ {2} ^ {\prime}) ] \geq \frac {1}{2} \mathbb {E} [ u (M _ {1} ^ {\prime}) ] \geq \frac {u (M ^ {*})}{1 2},
$$

where $M _ { 2 } ^ { \prime }$ is the matching returned by IMC-Z during the period $( \lfloor \frac { \bar { T } } { 2 } \rfloor , T )$ .

Theorem 1: IMC-Z possesses the desirable properties of computational efficiency, individual rationality, budget feasibility, consumer sovereignty, truthfulness, and constant competitiveness.

# IV. MECHANISM UNDER G-MODEL

In this section, We propose an online Incentive Mechanism for Crowdsensing systems under G-model (IMC-G). The users now stay in connection with the task requester until they depart. In this case, the truthfulness of the mechanism includes both time- and cost-truthfulness, while the other properties are the same as those in Z-model.

# A. IMC-G Design

To preserve the desirable properties of the mechanism, we adopt the same structure as IMC-Z to design IMC-G. Note that the key difference between the two settings lies in the connection duration between the bidding users and the requester, which leads to several principles. First, bid independence is more difficult to maintain as the user’s duration interval may span multiple stages. Note that the payment is updated at the end of each stage, the strategy to prevent users from affecting their payment computation is that the users are added to the observed set only when they depart. Second, at each time step, there may be several users competing to win. We hence greedily select a user according to her available task with the highest value, given that her b/b is qualified. In this way, we can hold the bid-independence. Third, at each new time step, we need to check the set of users who are still connecting with the requester, and conduct user selection according to the b/b under the budget constraint. The payment for each selected user, which is the maximum price attained during the user’s reported arrival-departure time interval, is given at her departure time.

Algorithm 4 illustrates the process of IMC-G which conforms to the above principles. At each time step t, we first add all new users who just arrive to the online active set of bidding users O (line 4). If the time step t is not the end of a stage, the b/b threshold remains the same and we select the users satisfying the same conditions as in Algorithm 1

(lines 5–8). Then we remove all users departing at the time step t from the online candidate set O, and add these users, as well as their links to the tasks, to the observed graph $\mathcal { G } ( E )$ (line 9), which is used for calculating the stage b/b threshold.

Algorithm 4 IMC-G   
Input: Budget B, Deadline T, Task set Q
Output: Matching M, Payment vector p
1: $(t, T', B', \rho) \leftarrow (1, \frac{T}{2^{\lfloor \log_{2} T \rfloor}}, \frac{B}{2^{\lfloor \log_{2} T \rfloor}}, \epsilon);$ 2: $(\mathcal{G}(E), M, M', \mathcal{O}) \leftarrow (\emptyset, \emptyset, \emptyset, \emptyset);$ 3: while $t \leq T$ do
4: add users arriving at t to the online active user set O;
5: $\mathcal{O}' \leftarrow \mathcal{O} \backslash \mathcal{U}(M);$ 6: for $i \in O'$ do
7: $(M, p_i) \leftarrow \text{Selection}(\mathcal{Q}_i, b_i, M, M', \rho);$ 8: end for
9: Remove all users departing at time t from O, and add them, as well as their edges, to the graph $\mathcal{G}(E);$ 10: if $t = \lfloor T' \rfloor$ then
11: $(M', \rho) \leftarrow \text{GetThreshold}(B', \mathcal{G}(E));$ 12: $T' \leftarrow 2T'; B' \leftarrow 2B';$ 13: $(M, p) \leftarrow \text{UpdatePayment}(B', \mathcal{O}, M, M', \rho);$ 14: end if
15: $t \leftarrow t + 1;$ 16: end while

If the time step t is the end of a stage, we need to recompute the b/b threshold (line 11) and update the payments for the selected users who haven’t departed yet. Also, as the b/b is updated, the users in the candidate set are checked against this new rate. The qualified ones will then be selected too (line 13).

Specifically, in Algorithm 5, we first check the selected users in the online candidate set in the order of non-ascending values of the assigned tasks (lines 1–7). For each user $i ,$ if the new threshold $\rho$ is greater than $\begin{array} { r } { \frac { b _ { i } } { v _ { j } } , } \end{array}$ the payment for user i is updated as $p _ { i } = \rho \cdot v _ { j }$ . As for the candidate users that haven’t been selected, we examine their quality by using the new threshold $\rho$ and the new budget $B ^ { \prime }$ (lines 8–11).

Algorithm 5 UpdatePayment   
Input: Budget $B'$ , Online user set $\mathcal{O}$ , Matching $M, M'$ , Threshold $\rho$ Output: Matching $M$ , Payment vector $p$ 1: $\mathcal{O}' \leftarrow \mathcal{O} \cap \mathcal{U}(M)$ ;

2: for $i \in \mathcal{O}'$ do

3: Find the assigned task $j$ of user $i$ in $M$ ;

4: if $p_i \leq \rho \cdot v_j \leq B' - \sum_{i' \in \mathcal{U}(M) \setminus \{i\}} p_{i'}$ then

5: $p_i \leftarrow \rho \cdot v_j$ ;

6: end if

7: end for

8: $\mathcal{O}' \leftarrow \mathcal{O} \backslash \mathcal{U}(M)$ ;

9: for $i \in \mathcal{O}'$ do

10: $(M, p_i) \leftarrow \text{Selection}(\mathcal{Q}_i, b_i, M, M', \rho)$ ;

11: end for

# B. IMC-G Analysis

Due to the similar strategies as IMC-Z in Algorithm 1, it is intuitive to prove that IMC-G is individually rational, consumer sovereign, and constant competitive. We next show that IMC-G also satisfies the remaining desirable properties, i.e., computational efficiency, budget feasibility, and cost and time truthfulness.

Lemma 7: IMC-G is computationally efficient.

Proof: At each time step, the mechanism needs to compute the assignments and payments of available online candidates. The computation for each user takes $O ( m ^ { 2 }$ log m) time, and there are at most n users. So the for-loop (lines 6– 8) takes $O ( m ^ { 2 } n \log m )$ time. The threshold computation in line 11 has the same complexity as that of Algorithm 1, i.e., $O ( m ^ { 2 } n ^ { 2 } )$ ). The payment update operation in line 13, as can be easily seen from Algorithm 5, has the time complexity of $O ( m ^ { 2 } n \log m )$ . In short, the computation complexity of Algorithm 4 is polynomial.

Lemma 8: IMC-G is budget feasible.

Proof: There are two cases considering the time step t. If the current time t is not a stage change point, the selection procedure guarantees that the the total payment does not exceed the budget for the current stage as proved in Lemma 3. If t is a stage change point, the b/b threshold is updated (line 11) and the budget is increased (line 12). The payments for the available users, including selected and non-selected users, are examined again using the new threshold and budget by calling Algorithm 5 (line 13), which indeed guarantees that the new payments do not exceed the new budget.

Lemma 9: IMC-G is cost- and time-truthful.

Proof: Consider user i with the truthful profile $\theta _ { i } \ =$ $\{ a _ { i } , d _ { i } , c _ { i } , Q _ { i } \}$ and bidding profile $\theta _ { i } ^ { \prime } = \{ a _ { i } ^ { \prime } , d _ { i } ^ { \prime } , b _ { i } , Q _ { i } \}$ . In Algorithm $^ { 4 , }$ user i may be examined at each time step $t \in [ a _ { i } ^ { \prime } , d _ { i } ^ { \prime } ]$ . Let $T _ { t } ^ { \prime } , B _ { t } ^ { \prime } , \rho _ { t }$ , and $\mathcal { U } ( M _ { t } )$ denote the end time of the current stage, the remaining budget for the current stage, the b/b threshold for the current stage, and the set of selected users before examining user i at time step t, respectively. Let $\theta _ { - i } ^ { \prime }$ represent the strategy profiles of all users excluding user i. It suffices to prove the lemma by verifying the following two parts.

With fixed $b _ { i }$ and $\theta _ { - i } ^ { \prime } ,$ reporting the true arrival and departure time is a dominant strategy for user i. Note that in Algorithm 4, user i is paid the maximum threshold price during her reported arrival-departure time interval if she is selected as a winner. Assume that user i obtains the maximum payment at time step $t \in [ a _ { i } ^ { \prime } , d _ { i } ^ { \prime } ] \subseteq [ a _ { i } , d _ { i } ]$ . Then reporting an earlier arrival time or a later departure time than t does not increase the payment of user i. If user i reports a later arrival or an earlier departure time than t, then she will receive a lower payment.

With fixed $[ a _ { i } ^ { \prime } , d _ { i } ^ { \prime } ]$ and $\theta _ { - i } ^ { \prime }$ , reporting the true cost is a dominant strategy for user i. We discuss it in two steps. First, reporting a false cost at time step $t \in [ a _ { i } ^ { \prime } , d _ { i } ^ { \prime } ]$ cannot improve the payment of user i at that time step. This statement is intuitive to prove as the payment at time step t is determined by the b/b threshold $\rho _ { t }$ and the current available task with the largest value. These two factors are not affected by user i.

Second, reporting a false cost at time step $t \in [ a _ { i } ^ { \prime } , d _ { i } ^ { \prime } )$ cannot improve the payment of user i at time step $t ^ { \prime } \in ( t , d _ { i } ^ { \prime } ]$ . If user i is selected as a winner by reporting her true type, i.e., $b _ { i } = c _ { i }$ . Then we know that bi ≤ ρ∗ · vj∗ and B′ − ∑i′∈U(M ) pi′ ≥ $b _ { i } \leq \rho ^ { * } \cdot v _ { j } ,$ $\begin{array} { r } { B ^ { \prime } - \sum _ { i ^ { \prime } \in \mathcal { U } ( M ) } p _ { i ^ { \prime } } \geq } \end{array}$ $\rho ^ { \ast } \cdot v _ { j \ast }$ , where $\rho ^ { * }$ is the maximum b/b threshold during the time interval $[ a _ { i } ^ { \prime } , d _ { i } ^ { \prime } ]$ and task $j ^ { * }$ is the most valuable one that can be assigned to user i. Hence the payment for user i is equal to $\rho ^ { * } \cdot v _ { j ^ { * } }$ . Therefore, reporting a bidding price deviating from her true cost cannot improve her payment. If user i is not selected as a winner by reporting her true cost, i.e., we have $c _ { i } > \rho ^ { \prime } \cdot v _ { j ^ { \prime } }$ or $\begin{array} { r } { B ^ { \prime } - \sum _ { i ^ { \prime } \in \mathcal { U } ( M ) } p _ { i ^ { \prime } } < \rho ^ { \prime } \cdot v _ { j ^ { \prime } } } \end{array}$ , where $\rho ^ { \prime }$ is the minimum b/b rate during $[ a _ { i } ^ { \prime } , d _ { i } ^ { \prime } ]$ and task $j ^ { \prime }$ is the least valuable one that can be assigned to user i. In case $c _ { i } > \rho ^ { \prime } \cdot v _ { j ^ { \prime } }$ , if user i submits a bidding price $b _ { i } > \rho ^ { \prime } \cdot v _ { j ^ { \prime } }$ , then the outcome remains unchanged. If user i reports a bid $b _ { i } \leq \rho ^ { \prime } \cdot v _ { j ^ { \prime } }$ , then she will be selected and be paid an amount of $\rho ^ { \prime } \cdot v _ { j ^ { \prime } ; }$ , which is less than $c _ { i } .$ . Hence user i receives a negative utility. In case $\begin{array} { r } { B ^ { \prime } - \sum _ { i ^ { \prime } \in \mathcal { U } ( M ) } p _ { i ^ { \prime } } < \rho ^ { \prime } \cdot v _ { j ^ { \prime } } } \end{array}$ , reporting a false cost cannot affect the outcome at time step t or the residual budget $B _ { t ^ { \prime } } ^ { \prime }$ at time step $t ^ { \prime } .$ . In summary, reporting a false cost cannot improve user i’s payment at time step $t ^ { \prime } .$

Theorem 2: IMC-G possesses the desirable properties of computational efficiency, individual rationality, budget feasibility, consumer sovereignty, truthfulness, and constant competitiveness.

# V. PERFORMANCE EVALUATION

In this section, we carry out experiments to examine the practical performance of the proposed mechanisms on two real-world datasets: Gowalla [21] and T-drive [22], [23].

# A. Experimental Setup

We evaluate the performance of the proposed mechanisms by comparing against the state-of-the-art algorithms OMZ and OMG, as well as two benchmarks serving as an upper bound and a lower bound of the requester’s values:

• OMZ is an online incentive mechanism designed for selecting crowdsensing users based on submodular objective functions [14]. It applies to the zero arrival-departure interval model as the proposed IMC-Z in this paper. The requester’s value and running time of OMZ and IMC-Z are compared in this section.   
• OMG is the extended version of OMZ designed for the general non-zero arrival-departure interval model as the proposed IMC-G in this paper. The requester’s value and running time of OMG and IMC-G are compared in this section.   
• UNIFORM is an offline mechanism which assumes the availability of all workers at the same time. In other words, UNIFORM knows the costs and accessible tasks of all users a priori. It uses the same strategy as Algorithm 2 to find the weighted maximum matching under the given budget. This is a three factor approximation of the optimal solution, and hence we use it as an upper bound of the online mechanisms considering the requester’s obtained value.

![](images/5b53f630cf4d4975977937c8f41226f951c8727c0bfa645f2feb2004170ce328.jpg)



(a) Gowalla Users

![](images/484953674631ed8f006802dd9859265038040a22530fae4d47aca3438708d712.jpg)



(b) T-drive Users   
Fig. 2. Requester’s obtained values.

• HEURISTIC is an online mechanism that uses a twostage recruitment strategy. Specifically, it observes the first 1/e fraction of users’ bidding profiles and constructs a mean price from these observations. Then this mean price is used as the fixed payment for the users coming later: a user is selected and paid if her bidding price is smaller than this payment, and has an available task to be assigned. We use this two-stage strategy as a lower bound for the proposed multi-stage online incentive mechanisms considering the requester’s obtained value.

The experiments are conducted on Gowalla and T-drive datasets. Gowalla is a location-based social network, where users can check in at various places in their community. We use the check-ins within a community of California, and picked 100,000 check-ins during one month in 2010 for the sensing tasks. Intuitively, checking in a spot represents that the spatial task in that location is completed. We assumed that the registered users in Gowalla are interested in doing tasks. The value of each sensing task is inversely proportional to the number of check-ins of its spot, as the more users for a spot, the more chances may the task be completed. Also, the cost of each user is inversely proportional to the check-in frequency of that user with a small random noise, where we assume that users largely tend to do tasks with lower cost expectation if they check in frequently.

T-drive contains the GPS traces of 10,357 taxis in Beijing for a duration of one week in 2008. We take each taxi as a crowdsensing user equipped with multiple built-in sensors, and assume that each user can complete a spatial sensing task along her route. In the experiment, we generate a number of sensing tasks in the road networks. Specifically, the road network is consisted of road segments, which has the attributes of segment ID, segment length, and the GPS coordinates of the head and end of the segment. The sensing task is randomly generated among the GPS coordinates of the segment ends. We employ an HMM algorithm [24] to perform map matching, which maps each GPS point of a user’s trace to the corresponding road segment. As a result, a user’s trajectory is converted to a sequence of road segments. We then obtain the preferred tasks of all users by matching the road segments. Similar to the Gowalla data, the value of each sensing task is inversely proportional to the frequency of taxis passing by. The cost of each user is inversely proportional to the tasks she can complete. A random noise is added to reflect individual difference.

Without loss of generality, for both Gowalla and T-drive data, we adopt the setting that there is a user bidding at each time step. So the recruitment deadline is equivalent to the size of candidates. For IMC-G and OMG, each user’s arrival-departure interval is uniformly distributed over [0, 150] time steps. OMZ and OMG select users based on the total marginal values of their preferred tasks and associated costs. All experiments are run on a PC with 2.3GHz CPU and 8 GB memory.

# B. Results

1) Requester’s obtained value: Fig. 2 illustrates the results of the overall value by varying budgets for compared methods. As shown in the two figures, the values of all methods increase with the requester’s budgets. On Gowalla data, The values obtained by IMC-Z increase on average 57.6% and 90.3% compared to the values obtained by OMZ and HEURISTIC, respectively; while the values obtained by IMC-G increase on average 56.8% and 59.1% compared to that of OMG and HEURISTIC, respectively. On T-drive data, IMC-Z achieves an increment of 53.4% and 129.4% compared to OMZ and HEURISTIC, respectively; while IMC-G obtains an increment of 48.4% and 117.5% compared to OMG and HEURISTIC, respectively. In summary, the obtained values of IMC-Z (or IMC-G) are evidently larger than that of OMZ (or OMG) and HEURISTIC. On the other aspect, the performance of IMC-Z and IMC-G is within a margin of 23.4% and 33.8% compared to that of UNIFORM, which assumes unrealistic access to true costs of all users beforehand. It implies that the competitive ratios of the proposed mechanisms are smaller than the theoretical ratios we have proved in Section III and IV. Also, we can see that IMC-G sacrifices some value to achieve the time-truthfulness compared to IMC-Z on both datasets.

2) Running time: The running time of an online mechanism needs to fulfil the real-time application scenarios. Fig. 3 shows the running time of IMC-Z, IMC-G, OMZ, and OMG at different threshold payment computation stages. Note that UNIFORM is not shown as it is an offline algorithm; while

![](images/841837df40259f751ab69b4baed7277e7a25b6640e81537fd1d28ec0463ac569.jpg)



(a) Gowalla Users

![](images/411c67529b9c5676a22940dc2b8f2b72d4449d401b706c4e6c8a07e7e7376fb7.jpg)



(b) T-drive Users   
Fig. 3. Running time comparison.

HEURISTIC does not need the threshold payment computation process. It selects a user almost instantly after receiving the bidding profile and hence the running time is negligible. It can be seen from the figures that, OMZ and OMG run faster than the proposed IMC-Z and IMC-G. However, the maximum running time of the proposed methods is less than 0.25 seconds in the two settings, which indicates the potential of the proposed mechanisms to meet the requirement of realtime user selection.

3) Cost and time truthfulness: We first investigate the cost truthfulness of OMZ. We randomly select two users (No. 321 and 418) from Gowalla data and two users (No. 263 and 284) from T-drive data, and allow them to manipulate their bidding prices. Fig. 4 shows the results of the obtained utility of these four users. The blue stars in the figures denote the true costs of users. It can be seen that users achieve their optimal utility when bidding truthfully. User 321 and user 263 can be selected and achieve positive utility; while user 418 and user 284 achieve maximal utility equalling to zero (i.e., they are not selected as they have high true costs). If they submit a bidding price smaller than the true cost, they will receive negative utility. Note that the payment strategy of IMC-G is the same as IMC-Z, therefore we only verify the time truthfulness of IMC-G in the following. We randomly pick one user (No. 271) from Gowalla data and one user (No. 178) from T-drive data, and allow them to report their arrival/departure times that are different from the true values. As shown in Fig. 5a and Fig. 5c, user 271 and user 178 receive their optimal utility if they report their true arrival times. Fig. 5b and Fig. 5d show that user 271 and user 178 achieve the optimal utility if they report their true departure times.

# VI. RELATED WORK

In the context of mobile crowdsourcing, incentive mechanisms have been studied in offline and online settings. In offline settings, Lee and Hoh [11] proposed a reverse auction based dynamic price incentive mechanism, where users can claim their bidding prices for selling the sensed data. Yang et al. [12] designed an auction based mechanism and proved several desirable properties. Wen et al. [25] further took into account the quality of sensing in designing incentives. All of these results did not emphasize on the properties of online arriving users. Hence they cannot be directly applied to online settings.

Recently, researchers started to focus on designing incentive mechanisms for the online setting. Feng et al. [26] studied an online model to maximize the social welfare by assigning most valuable tasks. However, they did not take users’ limits and preferences into account and hence their model could not assign appropriate tasks to users in crowdsensing. Zhao et al. [14], [27] studied online incentive mechanisms for selecting users based on submodular objective functions. They adopted a similar multi-stage recruitment process as the proposed methods in this paper. However, they focused on modeling the sensing problem as a coverage problem, and designed the mechanisms using submodular properties; while the proposed mechanisms focused on assigning specific tasks to the most suitable users, so as to achieve weighted maximum matching given a fixed budget. Therefore, the potential application types and theoretic foundations for proving the desirable properties of the two works are different. Zhang et al. [13] also designed online incentive mechanisms by using submodular functions. Yet their model did not use a budgeted recruitment framework as proposed in this work. Instead they sought to select a fixed number of users to maximize the objective function. Sun and Ma [28] modelled the user recruitment problem as a restless multi-armed bandit process, which is different from the proposed auction-based mechanisms. The authors assumed that a user is associated with a belief state transition probability matrix, based on which the incentive mechanism is designed; while in our model, the incentive mechanism is designed based on users’ bidding profiles. Furthermore, Sun and Ma [28] sought to satisfy the sensing coverage constraint for continuous sensing; while in this paper, we focused on assigning location-based sensing tasks to the most suitable users. Singer and Mittal [29], [30] addressed task pricing in online crowdsourcing markets to maximize the number of assigned tasks, and they did not differentiate tasks. This is different from the setting in this work, where we need to determine which task is most suitable for a specific user. Furthermore, they did not study the general arrival-departure models as proposed in this paper. Jaims et al. [31] considered a dynamic setting where the auction is conducted in multiple rounds. In each round, they used virtual participation credit to motivate users who lost in the previous rounds. Our model differs in that, we consider one round of auction and focus on the online arrival of each user.

This work is also related to the budget feasible mechanism design which was initiated in [18]. One subsequent direction has improved the current results and extended them to diverse models and applications [19], [32]–[34]. Goel et al. [19] designed an offline task assignment scheme with matching constraints, which is generalized to the online crowdsensing setting in this work. The generalization is nontrivial as the online mechanism poses different challenges in ensuring the essential properties such as truthfulness, sovereignty, and competitiveness.

![](images/4fffe7e04cb638ea18442684022d3f2ee4b8c9215483b4b2fc6b57d8b0b7c544.jpg)



(a) Gowalla User 321: $c _ { 3 2 1 } = 0 . 4 8 0 2$

![](images/a7c57b85076f2387a35909eff635e9f99bdfcd9ee36db486bb2b1c05439c3fb2.jpg)



(b) Gowalla User 418: $c _ { 4 1 8 } = 0 . 8 2 5 3$

![](images/d681be7a772ee61a5483a9c09abf7ab87ffb0adf8221eef24ca8ada874ee35df.jpg)



(c) T-drive User 263: $c _ { 2 6 3 } = 0 . 5 6 2 4$

![](images/555dc7b487d1eb32594a46bdc1f700819204c893a89b4241eee9d6a8fde4dc33.jpg)



(d) T-drive User 284: $c _ { 2 8 4 } = 1 . 1 8 6 1$   
Fig. 4. Cost truthfulness of IMC-Z.

Several task assignment problems in crowdsensing are also related to our work. iCrowd [35] is a generic sensing task assignment framework, which contains an incentive mechanism part. The goals of iCrowd are to maximize k-depth coverage given an incentive budget and minimize incentive payments given a k-depth coverage constraint. The incentive methods adopt base and bonus payments based on users participation cycles. Yet in our model, we focused on designing auctionbased incentive mechanisms, which allow users to submit bidding prices for completing specific tasks. $E M C ^ { 3 }$ [36] is a crowdsensing framework that intends to reduce energy consumption of users when assigning tasks with sensing area coverage constraint. It uses users’ call and mobility information to make informed selection decisions, which make the most of potential users for sensing. Similarly, Pournajaf et al. [37] aimed at maximizing the sensing area coverage and minimizing the travelling cost by predicting the mobility of users. In comparison, we did not select users based on their mobilities, but recruited users and assigned tasks based on their explicit bidding profiles, and sought to achieve maximum utility given a budget by designing online incentive mechanisms. Pournajaf et al. [38] considered protecting users’ location privacy when assigning sensing tasks, which is indirectly helping to motivate users to participate in completing tasks. From this perspective, protection of user identities may also stimulate participation [39], [40]. In this work, we considered directly modelling the incentive mechanisms where users can submit bidding prices for completing tasks.

# VII. CONCLUSION

In this paper, we have designed two efficient online incentive mechanisms for crowdsensing systems. The mechanisms take into account users’ preferences and limits in crowdsensing systems, and are able to select and map users to the most valuable tasks, such that the requester can achieve high value. We have proved that the designed mechanisms possess the following desirable properties: computational efficiency, individual rationality, budget feasibility, truthfulness, consumer sovereignty, and constant competitiveness. Experimental results show that the mechanisms perform well on two realworld datasets. In future work, we plan to extend the mechanisms to the scenario where users have different costs for different tasks, undertake multiple tasks, or have complicated arrival patterns.

# REFERENCES

[1] R. K. Ganti, F. Ye, and H. Lei, “Mobile crowdsensing: Current state and future challenges,” IEEE Communications Magazine, vol. 49, no. 11, pp. 32–39, 2011.   
[2] M. Y. A. Wazir Zada Khan, Yang Xiang and Q. Arshad, “Mobile phone sensing systems: A survey,” IEEE Communications Surveys and Tutorials, vol. 15, no. 1, 2013.   
[3] E. Koukoumidis, L.-S. Peh, and M. R. Martonosi, “Signalguru: leveraging mobile phones for collaborative traffic signal schedule advisory,” in Proceedings of ACM international conference on Mobile systems, applications, and services (MobiSys), 2011, pp. 127–140.   
[4] N. Maisonneuve, M. Stevens, M. Niessen, and L. Steels, “Noisetube: Measuring and mapping noise pollution with mobile phones,” Information Technologies in Environmental Engineering, pp. 215–228, 2009.   
[5] L. Kazemi and C. Shahabi, “Geocrowd: enabling query answering with spatial crowdsourcing,” in Proceedings of ACM International Conference on Advances in Geographic Information Systems (GIS), 2012.   
[6] C. Wu, Z. Yang, and Y. Liu, “Smartphones based crowdsourcing for indoor localization,” IEEE Transactions on Mobile Computing, vol. 14, no. 2, pp. 444–457, 2015.   
[7] X. Zhang, Z. Yang, C. Wu, W. Sun, Y. Liu, and K. Xing, “Robust trajectory estimation for crowdsourcing-based mobile applications,” IEEE Transactions on Parallel and Distributed Systems, vol. 25, no. 7, pp. 1876–1885, 2014.   
[8] Http://www.idc.com/getdoc.jsp?containerId=prUS 24645514.  
[9] L. Jaimes, I. Vergara-Laurens, and A. Raij, “A survey of incentive techniques for mobile crowd sensing,” IEEE Internet of Things Journal, vol. 2, no. 5, pp. 370–380, 2015.   
[10] X. Zhang, Z. Yang, W. Sun, Y. Liu, S. Tang, K. Xing, and X. Mao, “Incentives for mobile crowd sensing: A survey,” IEEE Communications Surveys and Tutorials, vol. 18, no. 1, pp. 54–67, 2016.   
[11] J.-S. Lee and B. Hoh, “Sell your experiences: a market mechanism based incentive for participatory sensing,” in Proceedings of IEEE International Conference on Pervasive Computing and Communications (PerCom), 2010, pp. 60–68.

![](images/ae00b64be28aa375be833c41412b84dbc68f1c6af0c1a1a8ef31321320f659e8.jpg)



(a) Gowalla User $2 7 1 \colon d _ { 2 7 1 } ^ { \prime } = 1 9 2 .$ , $b _ { 2 7 1 } = 0 . 4 0 8 7$

![](images/08b27018b2144633396119f21836b09b7ada0def222dc3862ce8a144fb4e348f.jpg)



(b) Gowalla User 271: $a _ { 2 7 1 } ^ { \prime } = 1 2 0 ,$ , b271 = 0.4087

![](images/df3f94a41b5a35046807dca66b585e925f02923bb25f9ddfa0cc0f2522117994.jpg)



(c) T-drive User 178: $d _ { 1 7 8 } ^ { \prime } = 3 1 4 , b _ { 1 7 8 } = 0 . 4 5 7 3$

![](images/b6e58a840efd3040a3578e65626e85e552e7d3282aa1ee1b1a09282e77f426d4.jpg)



(d) T-drive User 178: $a _ { 1 7 8 } ^ { \prime } = 2 1 1 , b _ { 1 7 8 } = 0 . 4 5 7 3$   
Fig. 5. Time truthfulness of IMC-G. (a)-(b): Gowalla user $2 7 1 \colon ( a _ { 2 7 1 } , d _ { 2 7 1 } , c _ { 2 7 1 } ) = ( 1 2 0 , 1 9 2 , 0 . 4 0 8 7 )$ ; (c)-(d): T-drive user 178: $( a _ { 1 7 8 } , d _ { 1 7 8 } , c _ { 1 7 8 } ) =$ (221, 314, 0.4573).

[12] D. Yang, G. Xue, X. Fang, and J. Tang, “Crowdsourcing to smartphones: incentive mechanism design for mobile phone sensing,” in Proceedings of ACM international conference on Mobile computing and networking (MobiCom), 2012.   
[13] X. Zhang, Z. Yang, Z. Zhou, H. Cai, L. Chen, and X. Li, “Free market of crowdsourcing: Incentive mechanism design for mobile sensing,” IEEE Transactions on Parallel and Distributed Systems, vol. 25, no. 12, pp. 3190–3200, 2014.   
[14] D. Zhao, X.-Y. Li, and H. Ma, “How to crowdsource tasks truthfully without sacrificing utility: Online incentive mechanisms with budget constraint,” in Proceedings of IEEE International Conference on Computer Communications (INFOCOM), 2014, pp. 1213–1221.   
[15] M. Musthag and D. Ganesan, “Labor dynamics in a mobile micro-task market,” in Proceedings of ACM SIGCHI Conference on Human Factors in Computing Systems, 2013, pp. 641–650.   
[16] P. Cheng, X. Lian, Z. Chen, R. Fu, L. Chen, J. Han, and J. Zhao, “Reliable diversity-based spatial crowdsourcing by moving workers,” Proceedings of the VLDB Endowment, vol. 8, no. 10, pp. 1022–1033, 2015.   
[17] N. Nisan, T. Roughgarden, E. Tardos, and V. V. Vazirani, Algorithmic game theory. Cambridge University Press Cambridge, 2007, vol. 1.   
[18] Y. Singer, “Budget feasible mechanisms,” in Proceedings of IEEE Symposium on Foundations of Computer Science (FOCS), 2010, pp. 765–774.   
[19] G. Goel, A. Nikzad, and A. Singla, “Matching workers expertise with tasks: Incentives in heterogeneous crowdsourcing markets,” in NIPS Workshop on Crowdsourcing, 2013.   
[20] Z. Bar-Yossef, K. Hildrum, and F. Wu, “Incentive-compatible online auctions for digital goods,” in Proceedings of ACM-SIAM symposium on Discrete algorithms (SODA), 2002, pp. 964–970.   
[21] Https://snap.stanford.edu/data/loc-gowalla.html.   
[22] J. Yuan, Y. Zheng, X. Xie, and G. Sun, “Driving with knowledge from the physical world,” in Proceedings of ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD), 2011.   
[23] J. Yuan, Y. Zheng, C. Zhang, W. Xie, X. Xie, G. Sun, and Y. Huang, “T-drive: driving directions based on taxi trajectories,” in Proceedings of ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (GIS), 2010.   
[24] P. Newson and J. Krumm, “Hidden markov map matching through noise and sparseness,” in Proceedings of ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (GIS), 2009.   
[25] Y. Wen, J. Shi, Q. Zhang, X. Tian, Z. Huang, H. Yu, Y. B. Cheng, and X. Shen, “Quality-driven auction based incentive mechanism for mobile crowd sensing,” IEEE Transactions on Vehicular Techonology, vol. 64, no. 9, pp. 4203–4214, 2015.   
[26] Z. Feng, Y. Zhu, Q. Zhang, H. Zhu, J. Yu, J. Cao, and L. M. Ni, “Towards truthful mechanisms for mobile crowdsourcing with dynamic

smartphones,” in Proceedings of IEEE International Conference on Distributed Computing Systems (ICDCS), 2014, pp. 11–20.   
[27] D. Zhao, X.-Y. Li, and H. Ma, “Budget-feasible online incentive mechanisms for crowdsourcing tasks truthfully,” IEEE/ACM Transactions on Networking, 2015.   
[28] J. Sun and H. Ma, “Heterogeneous-belief based incentive schemes for crowd sensing in mobile social networks,” Journal of Network and Computer Applications, vol. 42, pp. 189–196, 2014.   
[29] Y. Singer and M. Mittal, “Pricing tasks in online labor markets.” in Human Computation, 2011.   
[30] ——, “Pricing mechanisms for crowdsourcing markets,” in Proceedings of the international conference on World Wide Web (WWW), 2013, pp. 1157–1166.   
[31] L. G. Jaimes, I. Vergara-Laurens, and M. A. Labrador, “A location-based incentive mechanism for participatory sensing systems with budget constraints,” in Proceedings of International Conference on Pervasive Computing and Communications (PerCom), 2012, pp. 103–108.   
[32] N. Chen, N. Gravin, and P. Lu, “On the approximability of budget feasible mechanisms,” in Proceedings of ACM-SIAM Symposium on Discrete Algorithms (SODA), 2011, pp. 685–699.   
[33] X. Bei, N. Chen, N. Gravin, and P. Lu, “Budget feasible mechanism design: from prior-free to bayesian,” in Proceedings of ACM Symposium on Theory of Computing (STOC), 2012.   
[34] A. Singla and A. Krause, “Incentives for privacy tradeoff in community sensing,” in Proceedings of AAAI Conference on Human Computation and Crowdsourcing (HCOMP), 2013.   
[35] H. Xiong, D. Zhang, G. Chen, L. Wang, V. Gauthier, and L. Barnes, “icrowd: Near-optimal task allocation for piggyback crowdsensing,” IEEE Transactions on Mobile Computing, 2015.   
[36] H. Xiong, D. Zhang, L. Wang, and H. Chaouchi, “Emc3: Energyefficient data transfer in mobile crowdsensing under full coverage constraint,” IEEE Transactions on Mobile Computing, vol. 14, no. 7, pp. 1355–1368, 2015.   
[37] L. Pournajaf, L. Xiong, and V. Sunderam, “Dynamic data driven crowd sensing task assignment,” Procedia Computer Science, vol. 29, pp. 1314–1323, 2014.   
[38] L. Pournajaf, L. Xiong, V. Sunderam, and S. Goryczka, “Spatial task assignment for crowd sensing with cloaked locations,” in Proceedings of IEEE International Conference on Mobile Data Management (MDM), 2014.   
[39] J. Chen, G. Wu, and Z. Ji, “Secure interoperation of identity managements among different circles of trust,” Computer Standards & Interfaces, vol. 33, no. 6, pp. 533–540, 2011.   
[40] J. Chen, G. Wu, L. Shen, and Z. Ji, “Differentiated security levels for personal identifiable information in identity management system,” Expert Systems with Applications, vol. 38, no. 11, pp. 14 156–14 162, 2011.

![](images/ace446b7b5708dcd61d71a663bbd8fa91b036a4503655da0a247e4c5358afef9.jpg)



Xinglin Zhang received a B.E. degree in School of Software from Sun Yat-sen University in 2010 and a Ph.D. degree in the Department of Computer Science and Engineering from Hong Kong University of Science and Technology in 2014. He is currently with the College of Computer Science and Software Engineering of Shenzhen University, and South China University of Technology. His research interests include wireless ad-hoc/sensor networks, mobile computing and crowdsourcing. He is a member of the IEEE and the ACM.

![](images/ec2b6f7cfe900258bb682bb27af2ba8f2dbfb210b803ee13fe128b2ad24f0f6a.jpg)



Jianqiang Li received his B.S and Ph.D. Degree from South China University of Technology in 2003 and 2008. He is an associate professor at the College of Computer Science and Software Engineering of Shenzhen University. He led a project of the National Natural Science Foundation, and a project of the Natural Science Foundation of Guangdong province,China. His major research interests include hybrid systems, internet of thing and embedded Systems.

![](images/bfc36eec4dc2296868fe318594d6a692ce22d2c58d88c5a10b4d82bd8d48041b.jpg)



Zheng Yang received a B.E. degree in computer science from Tsinghua University in 2006 and a Ph.D. degree in computer science from Hong Kong University of Science and Technology in 2010. He is currently an associate professor at Tsinghua University. His main research interests include wireless ad-hoc/sensor networks and mobile computing. He is a member of the IEEE and the ACM.

![](images/4d48ca56cc9db4058b86b6a13c39adf70386f2ac7b4556d042219ea8d1c9a57c.jpg)



Zhong Ming is a professor at the College of Computer and Software Engineering of Shenzhen University. He is a senior member of the Chinese Computer Federation. He led three projects of the National Natural Science Foundation, and two projects of the Natural Science Foundation of Guangdong province, China. His major research interests include home networks, internet of thing and cloud computing.

![](images/f5751eee187ce346c55d7696c1f670c8c18f2a31dfcc9fe0b355b8c4b28c4dfe.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is Chang Jiang Chair Professor and Dean of the School of Software at Tsinghua University. His research interests include wireless sensor network, peer-to-peer computing, and pervasive computing. He is a fellow of the IEEE and a fellow of the ACM.