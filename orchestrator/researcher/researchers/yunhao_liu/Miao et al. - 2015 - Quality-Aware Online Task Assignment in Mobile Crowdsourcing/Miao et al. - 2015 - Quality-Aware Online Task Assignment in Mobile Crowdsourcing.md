# Quality-Aware Online Task Assignment in Mobile Crowdsourcing

Yanrong Kang $^{*}$ , Xin Miao $^{\dagger}$ , Kebin Liu $^{\dagger}$ , Lei Chen $^{*}$ , Yunhao Liu $^{\dagger}$

\*Dept. of Computer Science and Engineering, Hong Kong University of Science and Technology

$^{\dagger}$ School of Software and TNLIST, Tsinghua University

Abstract—Mobile crowdsourcing (MCS) has grown to be a powerful computation paradigm to harness human power to solve real-world problems. Many commercial MCS platforms have arisen, enabling various novel applications. As crowd workers can be unreliable, a critical issue of these platforms is quality control. Many task assignment approaches have been proposed to increase the quality of crowdsourced tasks by matching workers and tasks in a bipartite graph. However, they fail to apply to MCS platforms where tasks are bound with locations. This paper considers the quality-aware online task assignment problem with location-based tasks. The goal is to optimize tasks' overall quality by assigning appropriate sets of tasks to workers in an online manner. To solve this problem, we propose a probabilistic quality measurement model and a hitchhiking model to characterize workers' behavior. Then we design a polynomial-time online assignment algorithm and prove that the proposed algorithm approximates the offline optimal solution with a competitive ratio of 10/7. Through extensive simulations, we demonstrate the efficiency and effectiveness of our solution.

Keywords-mobile crowdsourcing; online task assignment; location based task;

# I. INTRODUCTION

With the rapid development of wireless networks and the proliferation of mobile devices, mobile crowdsourcing (M-CS) has emerged as an economic and effective computation paradigm to collect and analyze real-world data. It attracts much attention from the academic and industrial circles and inspires numerous applications $[1]$ – $[3]$ . In order to fully exploit the capability of mobile crowdsourcing, a surge of commercial platforms have been built, such as Field Agent $[4]$ and Gigwalk $[5]$ . In specific, a MCS platform operates by receiving requests form requestors and outsourcing them to workers from the crowd in the form of small tasks. Workers then submit their answers of assigned tasks and earn small amounts of money as rewards. As an example, Field Agent $[4]$ provides services for clients in need of real-time business information. It works by paying crowd agents to complete tasks like taking photos of certain stores, reporting prices etc.

A critical issue of MCS platforms is quality control. As a crowdsourcing platform attracts a diverse pool of workers, there is no guarantee that all of these workers are qualified to complete the assigned tasks at a satisfactory level of quality. Plus workers' carelessness or misjudgment, answers collected from crowd are often noisy and unreliable. To address this issue, many task assignment schemes have been proposed in web-based crowdsourcing [6]. The basic idea is to assign one task to multiple workers and then aggregate their answers using mechanisms like majority voting [7].

However, most of these approaches fail to apply to MCS platforms where tasks are bound with locations $[8]$ . Such location-based tasks require workers to reach certain places to provide information. For example, a traffic monitoring task need workers to report whether there are jams at several points-of-interest and an asset monitoring task wants the worker to verify the existence of certain property, like a manhole cover. The location based character makes the assignment problem in MCS platforms distinct from web-based ones in several perspectives. 1) Workers are restricted to tasks satisfying spatial constraints, while in web-based settings, a worker can perform any task on the platform. 2) When it comes to multiple tasks for a single worker, the location based character incurs travel cost. This makes the assignment problem for location-based tasks different from bipartite graph matching, which is the basic model of most existing approaches. 3) The location-based character which involves issues like location privacy, renders common single worker evaluation approaches difficult, making it hard to assess answer's reliability by its contributor's quality.

In this paper, we consider the optimization problem of online task assignment in real-time location-based MCS platforms. Our goal is to optimize the overall quality of location-based tasks by assigning proper tasks to each contributing worker under various constraints of both workers and tasks. We focus on tasks in the common form of bisection choice queries and consider situations where workers are anonymous individuals and no workers' behaviour is tracked [9]–[11]. So we build task quality model on the basis of crowd reliability and integrate workers' answers using majority voting. Each online arriving worker has a capacity constraint and a travel constraint. The capacity constraint denotes the maximal number of tasks he is willing to execute. And the travel constraint is modeled in a hitchhiking style, taking workers' original locations, destinations and travel budgets into account. The hitchhiking style encourages crowd workers commit tasks on their way from current locations to predefined destinations and thus has advantage of larger spatial coverage and lower cost. Based on these models, we formulate our Quality-Aware Online Task Assignment problem to maximize overall quality. Although the intuitive quality model seems to be simple, the task assignment problem turns out to be NP-hard even for the static version. After analyzing the characteristics of the problem, we design an efficient online assignment algorithm. The proposed algorithm employs a dynamic programming method to speed up calculation and we prove that it yields competitive results compared with the optimal offline solution.

![](images/b3f94ebd11806f6071c958b3a993ec4beecc25ff9d69d5f26acf4ebde92b95d9.jpg)



Figure 1. Architecture of A Mobile Crowdsourcing Platform

In summary, this paper makes following contributions:

- We adopt an intuitive probabilistic quality measurement model to aggregate noisy answers from the crowd without tracking users.   
- We mathematically formulate the quality-aware online task assignment problem in which worker's travel behavior is modeled in a hitchhiking style. Hitchhiking better fits human's intent and enjoys benefits of lower cost and larger spatial coverage.   
- We propose an online algorithm for our quality-aware task assignment problem and prove that it has competitive ratio of $\frac{10}{7}$ compared to the offline optimal solution.

This paper is organized as the following: Section II presents the system model and problem formulation. In section III, we develop an online approximation algorithm to solve the problem and analyze its performance. Section IV extensively evaluates the proposed algorithm and demonstrate its effectiveness. Related work is presented in section V and finally Section VI concludes this paper.

# II. SYSTEM MODEL AND PROBLEM FORMULATION

# A. System Architecture

Fig. 1 illustrates the way a mobile crowdsourcing platform works. Conceptually it consists of three parts, the Requesters, the Workers and the TaskManager. Requesters and Workers are platform users who are connected to the Internet through cellular networks or Wi-Fi. The TaskManager, usually played by the platform itself, resides in the cloud. When they have need, Requesters submit their crowdsourcing tasks to the platform in required form. Workers from the crowd register to the platform requesting to perform tasks and upload their answers to get payments. The TaskManager, as an vital component of the platform, is responsible for receiving tasks from requesters, organizing tasks, assigning tasks to workers, and collecting answers from workers. In a real-time system, both workers and tasks generated by requesters arrive at the platform online in sequence. The TaskManager must react in response to each incoming request without knowledge of future inputs.

# B. Task Model and Quality Measurement

In a crowdsourcing platform, requesters can submit their tasks at anytime. And in the context of mobile crowdsourcing, each task $\tau_{j}$ is associated with a location $l_{j}$ . To complete $\tau_{j}$ , workers have to travel to $l_{j}$ physically and submit their answers to the platform. In this paper, we focus on structured tasks in the form of bisection choice queries, like "Is the Hang Seng Bank open today?", "Are there many people at the Walmart market?".

To ensure tasks' quality, each task is assigned to multiple workers and its final result is inferred from collected answers. Due to the concern of location privacy in mobile crowdsourcing, in this paper we target at situations where workers are anonymous and single worker's contributing history is not tracked.

With anonymous workers, we adopt a quality measurement model based on crowd assessment inspired by Liu et al. [12]. In this model, each task $\tau_{j}$ is associated with a real value $p_{j}$ in [0, 1]. $p_{j}$ is the probability that a randomly selected worker from the crowd provides a correct answer for $\tau_{j}$ . $p_{j}$ reflects the difficulty of the task and the overall reliability of the crowd. One way to estimate $p_{j}$ is to collect information from similar historical tasks. If no such tasks exist, we can estimate $p_{j}$ with a few results using method in [13]. In this paper we assume the availability of $p_{j}$ and focus on the afterwards optimization problem of task assignment. Further we assume that for all tasks, $p_{j}$ is above 0.5. This is because that for tasks with $p_{j}$ below 0.5, we can reverse workers' results and get the right answer with probability greater than 0.5.

Without knowledge of single worker's reliability, we infer the final result using majority voting. Suppose a task is assigned to $k$ workers, we accept the result that comes from at least $\left\lceil \frac{k}{2} \right\rceil$ workers. In special, if there are even number of workers and either choice is made by exactly $\frac{k}{2}$ workers, we make a random guess and the probability of guessing right is 0.5. Formally, we define the quality measurement function as the following:

Definition 1. The quality of task $\tau_{j}$ , denoted as $A_{p_{j}}(k)$ , is the probability of deriving correct result from k crowd workers using majority voting.

$A_{p_{j}}(k)$ is determined by $p_{j}$ and the number of assigned workers k. If k is odd, $A_{p_{j}}(k)$ is the probability that at least $\lceil \frac{k}{2} \rceil$ workers provide right results. If k is even, $A_{p_{j}}(k)$ is the probability that at least $\frac{k}{2} + 1$ workers answer correctly plus the probability that only $\frac{k}{2}$ workers answer correctly and we guess rightly. To be specific,

If $k$ is odd,

$$
A _ {p _ {j}} (k) = \sum_ {r = \frac {k + 1}{2}} ^ {k} \binom {k} {r} p _ {j} ^ {r} (1 - p _ {j}) ^ {k - r} \tag {1}
$$

else,

$$
\begin{array}{l} A _ {p _ {j}} (k) = \sum_ {r = \frac {k}{2} + 1} ^ {k} \binom {k} {r} p _ {j} ^ {r} (1 - p _ {j}) ^ {k - r} \tag {2} \\ + \frac {1}{2} \binom {k} {\frac {k}{2}} p _ {j} ^ {\frac {k}{2}} (1 - p _ {j}) ^ {\frac {k}{2}} \\ \end{array}
$$

# C. Worker Model

Arriving workers deliver their wishes of carrying out tasks to the platform and submit their restraints on tasks. After receiving a worker's request for tasks, the TaskManager assigns certain tasks to him without violating his requirements. A worker's constraints are denoted by a set of attributes: $\varpi_{i} = (M_{i}, l_{s_{i}}, l_{d_{i}}, B_{i})$ . $M_{i}$ , which is called the worker's capacity, is the maximal number of tasks he is willing to perform. $l_{s_{i}}$ , $l_{d_{i}}$ and $B_{i}$ are the worker's original location, destination and travel budget respectively. These three attributes form the worker's travel constraint modeled in a hitchhiking style. That is, the worker is currently located at $l_{s_{i}}$ and intends to go to $l_{d_{i}}$ . He is willing to help executing tasks on his way from $l_{s_{i}}$ to $l_{d_{i}}$ . But as performing tasks may need him to make a detour and thus yields addition travel cost, the total travel cost should not exceed $B_{i}$ . The travel cost can be any function measuring the expense to go from one location to another. For example, it can be the distance between two places, or the estimated travel time from one place to the other during a certain period. An example of the worker model is shown in Fig 1. A worker is currently located at below to the left of the map and wants to go to the destination in the middle of the map. While the shortest path is $P_{1}$ , the TaskManager assigns him path $P_{2}$ of length less than $B_{i}$ such that he can perform two tasks on the way.

Hitchhiking enjoys many benefits compared to existing location-related constraints like nearby region constraint in $[14]$ and travel budget constraint in $[15]$ . First it takes travel cost into consideration for both single and multiple tasks. Second people move with intent and this hitchhiking style better matches people's behavior. Third hitchhiking encourages people to commit tasks on the way to somewhere else rendering lower cost compared with worker traveling to tasks' locations for tasks only. At last people's travel space is far larger than space people stay. So hitchhiking could enjoy better coverage.

# D. Problem Formulation

The online assignment problem runs in the following context. Tasks $\{\tau_{1},\tau_{2},..., \tau_{n}\}$ arrive in sequence. The subscript denotes the arriving order, which means that $\tau_{1}$ comes first and then $\tau_{2}$ comes, etc. It's the same with online arriving workers $\{\varpi_{1},\varpi_{2},..., \varpi_{m}\}$ . When a worker $\varpi_{i}$ arrives to the platform, the TaskManager assigns a sequence of tasks $S_{i}$ to him. The assignment is based on the available task set on the platform at the time, tasks that have arrived and not expired. Suppose $S_{i}=\{\tau_{i_{1}},\tau_{i_{2}},..., \tau_{i_{|S_{i}|}}\}$ . As worker needs to travel to tasks' locations to perform them, $S_{i}$ implies a path $P_{i}=\{l_{s_{i}},l_{i_{1}},...,l_{i_{|S_{i}|}},l_{d_{i}}\}$ for the worker. $P_{i}$ originates at $l_{s_{i}}$ , ends at $l_{d_{i}}$ and connects tasks in $S_{i}$ one by one. The assignment must obey worker and tasks' requirements. To be specific, $S_{i}$ and corresponding $P_{i}$ should satisfy following constraints.

• Worker capacity constraint

$$
\left| S _ {i} \right| \leq M _ {i} \tag {3}
$$

\- Worker's travel cost budget constraint

$$
T (P _ {i}) = \sum_ {r = 0} ^ {| S _ {i} |} c (l _ {i _ {k}}, l _ {i _ {k + 1}}) \leq B _ {i} \tag {4}
$$

$i_0 = s_i$ , $i_{n_i + 1} = d_i$ . And $c(l_{i_k}, l_{i_{k+1}})$ is the travel cost between $l_{i_k}$ and $l_{i_{k+1}}$ .

Let $H = \{S_1, S_2, ..., S_m\}$ be an assignment scheme in which sequence $S_i$ is assigned to worker $\varpi_i$ . We use decision variables $x_{i,j}$ to denote whether task $\tau_j$ is assigned to worker $\varpi_i$ . $x_{i,j} = 1$ if $\tau_j$ is assigned to $\varpi_i$ . Otherwise, $x_{i,j} = 0$ . So the number of workers assigned to task $\tau_j$ is $\sum_i x_{i,j}$ . Our goal is to maximize the expectation of the number of correctly answered tasks, which can be rewritten as the sum of accuracies of all tasks. Formally, given attributes of tasks and workers, our Quality-Aware Online Task Assignment problem (QAOTA) aims to

$$
\text { Maximize } A (H) = \sum_ {j = 1} ^ {n} A _ {p _ {j}} (\sum_ {i = 1} ^ {m} x _ {i, j}) \tag {5}
$$

in which

$$
x _ {i, j} = \left\{ \begin{array}{l l} 1, & \text { if } \tau_ {j} \in S _ {i} \\ 0, & \text { otherwise } \end{array} \right. \tag {6}
$$

and for each assigned sequence $S_{i}$ , constraints of inequality (3) (4) are satisfied.

# III. ONLINE ASSIGNMENT ALGORITHM DESIGN

The QAOTA problem is a NP-hard combinatorial optimization problem. To efficient solve it, first we have a close look into the characteristics of the quality function $A_{p_{j}}(k)$ . Based on that we propose an assignment mechanism of polynomial running time and prove that it is competitive with offline optimal solution with ratio $\frac{10}{7}$ . The complexity analysis of the QAOTA problem and the proof of all lemmas can be found in our technique report.

![](images/cbbe15728c214df7238a5f6dfb8235716fc43ced7f42a40b62aedb5a346588e7.jpg)



Figure 2. the Quality and Auxiliary Function with $p_j = 0.65$

A. Analysis of the Quality Function

Function $A_{p_j}(k)$ has the following property:

Lemma 1. For any integer $k \geq 1$ ,

$$
A _ {p _ {j}} (2 k) = A _ {p _ {j}} (2 k - 1) \tag {7}
$$

$$
\frac {A _ {p _ {j}} (2 k + 3) - A _ {p _ {j}} (2 k + 2)}{A _ {p _ {j}} (2 k + 1) - A _ {p _ {j}} (2 k)} = 4 p _ {j} (1 - p _ {j}) \frac {2 k + 1}{2 k + 2} \tag {8}
$$

From Lemma 1, we can tell that when $p_j > 0.5$ and $k$ is odd, the quality increases with $k$ and the increment becomes smaller when $k$ grows larger. But when $k$ is even, this property does not hold, as illustrated in Fig. 2. Specially when $k$ is even, $A_{p_j}(k)$ is equal to $A_{p_j}(k - 1)$ . Let $\Delta A_{p_j}(k) = A_{p_j}(k + 1) - A_{p_j}(k)$ be the potential quality increment with one more worker. We have, for any integer $k \geq 0$ , $\Delta A_{p_j}(2k + 1) = 0$ . Such a property impedes the design and analysis of assignment algorithms. To help ease this situation, we modify $\Delta A_{p_j}(k)$ as

$$
\Delta F _ {p _ {j}} (k) = \left\{ \begin{array}{l l} \Delta A _ {p _ {j}} (k), & \text { if   } k = 0 \\ \frac {\Delta A _ {p _ {j}} (k)}{2}, & \text { if   } k \text {   is   odd } \\ \frac {\Delta A _ {p _ {j}} (k - 1)}{2}, & \text { otherwise } \end{array} \right. \tag {9}
$$

We use $\Delta F_{p_{j}}(k)$ as a metric to guide our online assignment algorithm and with the help of Lemma 1, the usage of $\Delta F_{p_{j}}(k)$ also provides an alternative method to calculate $A_{p_{j}}(k)$ .

# B. Online Assignment Algorithm

We design an efficient online algorithm for our QAOTA problem on the basis of above analysis results. Our algorithm takes $\Delta F_{p_{j}}(k_{j})$ as assignment metric. When a worker arrives, it tries to assign him tasks with maximal sum of $\Delta F_{p_{j}}(k_{j})$ . Although $\Delta F_{p_{j}}(k_{j})$ is different from $\Delta A_{p_{j}}(k_{j})$ , we prove that the assignment scheme our algorithm derives is still competitive with the offline optimal solution that optimizes overall quality $\sum A_{p_{j}}(\sum x_{i,j})$ .

Taking advantage of Lemma 1 and the relationship between $\Delta F_{p_j}(k_j)$ and $\Delta A_{p_j}(k_j)$ , our algorithm adopts a dynamic programming method to speed up the calculation of $\Delta F_{p_j}(k_j)$ and $A_{p_j}(k)$ .

Setting out from Lemma 1, $\Delta F_{p_j}(k)$ can be calculated as

$$
\Delta F _ {p _ {j}} (k) = \left\{ \begin{array}{l l} p _ {j} - 0. 5, & \text { if   } k = 0 \\ \Delta F _ {p _ {j}} (k - 1) * p _ {j} (1 - p _ {j}), & \text { else   if   } k = 1 \\ \Delta F _ {p _ {j}} (k - 1), & \text { else   if   } k \text {   is   even } \\ \Delta F _ {p _ {j}} (k - 1) * 4 p _ {j} (1 - p _ {j}) * \frac {k}{k + 1}, & \text { otherwise } \end{array} \right. \tag {10}
$$

Further from the definition of $\Delta F_{p_{j}}(k)$ , the quality $A_{p_{j}}(k)=A_{p_{j}}(0)+\sum_{r=0}^{k-1}\Delta A_{p_{j}}(r)$ , can be calculated as

$$
A _ {p _ {j}} (k) = \left\{ \begin{array}{l l} 0. 5, & \text { if   } k = 0 \\ p _ {j}, & \text { else   if   } k = 1 \\ A _ {p _ {j}} (k - 1), & \text { else   if   } k \text {   is   even } \\ A _ {p _ {j}} (k - 2) + 2 \Delta F _ {p _ {j}} (k - 2), & \text { otherwise } \end{array} \right. \tag {11}
$$

Using Equation (10) and (11), $\Delta F_{p_{j}}(k)$ is calculated from $\Delta F_{p_{j}}(k-1)$ and k, while $A_{p_{j}}(k)$ is computed with $\Delta F_{p_{j}}(k)$ . This frees us from computing $F_{p_{j}}(k)$ using its definition, which is a far more complex procedure.

Algorithm 1 Quality-Aware Online Task Assignment   
Input: Online arriving tasks $\{\tau_{1},\tau_{2},..., \tau_{n}\}$ and workers $\{\varpi_{1},\varpi_{2},..., \varpi_{m}\}$ .
Output: A sequence of tasks $S_{i}$ for each worker $\varpi_{i}$ .
1: if Task $\tau_{j}=\{l_{j},p_{j}\}$ arrives then
2: $T\Leftarrow\{\tau_{j}\}\bigcup T$ 3: $k_{j}\Leftarrow0$ 4: $A(\tau_{j})\Leftarrow0.5$ 5: $\Delta F_{p_{j}}\Leftarrow(p_{j}-0.5)*0.5$ 6: if Task $\tau_{j}$ expires then
7: $T\Leftarrow T-\tau_{j}$ 8: if Worker $\varpi_{i}=\{l_{s_{i}},l_{d_{i}},B_{i},M_{i}\}$ arrives then
9: $S_{i}\Leftarrow HSWA(\{(l_{j},t_{j},\Delta F_{\tau_{j}})\}_{\tau_{j}\in\mathcal{T}},\{l_{s_{i}},l_{d_{i}},B_{i},M_{i}\}$ 10: for each task $\tau_{j}$ in $S_{i}$ do
11: $k_{j}\Leftarrow k_{j}+1$ 12: if $k_{j}$ is odd then
13: $A_{p_{j}}\Leftarrow A_{p_{j}}+2*\Delta F_{p_{j}}$ 14: $\Delta F_{p_{j}}\Leftarrow\Delta F_{p_{j}}*4p_{j}(1-p_{j})*\frac{k_{j}}{k_{j}+1}$ return $\{S_{i}\}$

As the quality function approximately increases with k and the increment diminishes when k grows, we employ the greedy strategy to help design our algorithm. The basic idea is that, when a worker arrives, we try to assign him a set of tasks such that the overall quality after this time of allocation is maximized, subject to existing assignments of previous workers. However the quality function only increases at odd points, so we adopts $\Delta F_{p_{j}}(k)$ which covers the contribution of workers at even points, as the greedy metric. Each time a worker $\varpi_{i}$ arrives, among all feasible task sets that meets the requirements of this worker and the tasks, our algorithm assigns $\varpi_{i}$ the set with maximal sum of $\Delta F_{p_{j}}(k)$ . Formally, let $\Delta F(S)=\sum_{\tau_{j}\in S}\Delta F_{\tau_{j}}$ and $S_{i}$ be the set of all feasible task sets for $\varpi_{i}$ , then $S_{i}=\arg\max_{S\in\mathcal{S}_{i}}F(S)$ .

Our quality-aware online task assignment algorithm is illustrated in Algorithm 1. The TaskManager keeps the active task set T. At the same time, TaskManager maintains three state variables for each task: $k_{j}$ the number of workers assigned to it, $\Delta F_{p_{j}}$ the potential quality increment with one more worker, and its quality $A(\tau_{j})$ . When a task arrives, it is added to T in line 2 and its state variables are initialized in line 3-5. When a task expires, it is removed from T in line 7. Each time a worker $\varpi_{i}$ arrives, a subprocess called Hitchhiking Single Worker Assignment (HSWA) is employed in line 9 to compute the task sequence with maximal $\Delta F(S_{i})$ under the restriction of both worker and tasks. Then the worker is assigned task set $S_{i}$ given by HSWA and the TaskManager updates value of $k_{j}$ , $A_{p_{j}}$ and $\Delta F_{p_{j}}$ for tasks in $S_{i}$ in line 10-14.

The HSWA process computes the task sequence with maximized total potential quality increment for each arriving worker $\varpi_{i}$ . The input to HSWA is composed of two parts. One part is $\varpi_{i}$ 's constraints, including original location $l_{s_{i}}$ , destination $l_{d_{i}}$ , travel distance budget $B_{i}$ , and capacity $M_{i}$ . The other part is the information of tasks on the platform. Each task $\tau_{j}$ is associated with a location $l_{j}$ and a potential quality increment $\Delta F_{p_{j}}$ . We assume that HSWA has access to a digital map which provides the travel distance between any two locations $c(l_{r}, l_{s})$ . The goal of HSWA is to find a sequences of tasks no more than $M_{i}$ to collect most increments and the length of the corresponding path from $l_{s_{i}}$ to $l_{d_{i}}$ connecting all tasks in the sequence is no more than $B_{i}$ .

We propose a Branch and Bound algorithm with effective pruning strategies shown in Algorithm 2 to solve HSWA. The search space of the Branch and Bound algorithm is a tree with $l_{s_i}$ as root node and all its leaf nodes are $l_{d_i}$ . The path from the root node to each leaf node represents a feasible path for the worker. The basic idea of Branch and Bound is a depth-first search with pruning. Starting from the root, we compute a candidate task set for each node in line 8 with Function CALCANDIDATE. The candidate set are tasks that can be reached from the current node without exceeding travel budget. Using the triangle inequality of the traveling time between tasks, a node's candidate set is a subset of its parent's. So to calculate a node's candidate set, we traverse its parent's candidate set and filter out tasks violating the travel budget constraint in line 21-23. $c(P)$ and $tail(P)$ are the total distance and the last task of current path $P$ . With the help of candidate set, an upper bound on the total increments of the current path is calculated in line 24. Let $\Delta F(P)$ be the total increments of current path. The upper bound is calculated as $\Delta F(R)$ plus the sum of increments of top M tasks where M is the maximal number of remaining tasks allowed by $M_{i}$ . We keep lb\_global as the global lower bound on the optimal total increments and updates it in line 13-15 when we find a feasible path with larger increments sum. Any node with ub lower than lb\_global is pruned in line 9-10 and thus search space is reduced. At each node, the search tree is branched in the candidates set in the descending order of their potential quality increments (line 11-12).

Algorithm 2 Branch and Bound Algorithm for HSWA   
Input: Tasks' information $\{(l_{j}, t_{j}, \Delta F_{\tau_{j}})\}_{\tau_{j} \in T}$ , worker $\varpi_{i}$ 's constraints $\{l_{s_{i}}, l_{d_{i}}, B_{i}, M_{i}\}$ Output: A sequence of tasks $S_{i} \subseteq T$ 1: $S_{i} \Leftarrow \emptyset$ 2: lb_global $\Leftarrow 0$ 3: Sort T in the descending order of $\Delta F_{\tau_{j}}$ 4: BB_Search( $\emptyset, T, M_{i}, B_{i}$ )

5: return $S_{i}$ 6:

7: function BB_SEARCH(P, C, M, B)

8: $\{C', ub\} \Leftarrow CalculateCandidate(P, C, M, B)$ 9: if $C'$ is empty or $ub \leq lb\_global$ then

10: return R

11: for each task $\tau_{j}$ in $C'$ do

12: $P' \Leftarrow BB\_Search(P + \tau_{j}, C' - \tau_{j}, M - 1, B)$ 13: if $\Delta F(P') \geq lb\_global$ then

14: $lb\_global \Leftarrow \Delta F(P')$ 15: $S_{i} \Leftarrow P'$ 16: return

17:

18: function CALCANDIDATE(P, C, M, B)

19: $C' \Leftarrow \emptyset$ 20: if $M \leq 0$ then return $\{\emptyset, \Delta F(P)\}$ 21: for each task $\tau_{j}$ in C do

22: if $c(P) + c(tail(P), l_{j}) + c(l_{j}, l_{d_{i}}) \leq B$ then

23: $C' \Leftarrow C' + \tau_{j}$ 24: $ub \Leftarrow \Delta F(P) + \sum_{top M tasks in C'} \Delta F_{\tau_{j}}$ 25: return $\{C', ub\}$

The computation complexity of Algorithm 2 is $O(n^{M_{i}})$ . Note that $M_{i}$ is the maximum number of tasks a worker would like to perform, which should be bounded by a small constant M.

# C. Theoretical Analysis

In this section, we prove that our QAOTA algorithm is competitive with the offline optimal solution with constant ratio $\frac{10}{7}$ .

Theorem 1. To maximize tasks' overall quality, assignment scheme derived from our Quality-Aware Online Task Assignment algorithm has competitive ratio of $\frac{10}{7}$ , compared with the offline optimal solution..

The optimal offline algorithm takes all information of tasks and workers as input, including the arriving time of all tasks and workers, and output an optimal assignment solution to maximize overall quality. Theorem 1 states that whatever the arriving order of workers and tasks, the resultant overall quality of assignment scheme from our online algorithm is no less than $\frac{7}{10}$ of the overall quality of the optimal offline solution.

It should be noticed in the offline algorithm, even though the global information about tasks and worker is known beforehand, tasks that arrive later than worker $\varpi_{i}$ can not be allocated to him. In other words, in both online and offline scenarios, for any arriving worker $\varpi_{i}$ , his available task set T is the same. But the offline algorithm could take advantage of future information like what kind of workers and tasks are coming afterwards to further optimize the goal function.

To help our analysis, we define an auxiliary function $F_{p_{j}}(k)$ as

$$
F _ {p _ {j}} (k) = F _ {p _ {j}} (0) + \sum_ {r = 0} ^ {k - 1} \Delta F _ {p _ {j}} (r) \tag {12}
$$

It's easy to show that

$$
F _ {p _ {j}} (k) = \left\{ \begin{array}{l l} A _ {p _ {j}} (k), & \text { if   } k = 0 \text {   or   } k \text {   is   odd } \\ \frac {A _ {p _ {j}} (k - 1) + A _ {p _ {j}} (k + 1)}{2}, & \text { otherwise } \end{array} \right. \tag {13}
$$

$F_{p_{j}}(k)$ approximates $A_{p_{j}}(k)$ , and $F_{p_{j}}(k)$ replaces the values of $A_{p_{j}}(k)$ with the average of $A_{p_{j}}(k-1)$ and $A_{p_{j}}(k+1)$ , when k is even and not zero. This replacement makes $F_{p_{j}}(k)$ monotonic and submodular.

Lemma 2. If $p_j \in (0.5,1]$ , the auxiliary function $F_{p_j}(k)$ is monotonic and submodular over number of assigned workers $k$ , i.e., for any $0 \leq r \leq t$ , $F_{p_j}(r) \leq F_{p_j}(t)$ and $F_{p_j}(r + 1) - F_{p_j}(r) \geq F_{p_j}(t + 1) - F_{p_j}(t)$ .

An assignment scheme H can be denoted as either the worker sets assigned to tasks $\{U_{j}\}_{j=1}^{n}$ or the task sets assigned to workers $\{S_{i}\}_{i=1}^{m}$ , where $U_{j}$ is the worker set that is assigned to task $\tau_{j}$ and $S_{i}$ is the task set assigned to worker $\varpi_{i}$ . Thus, the overall quality of assignment scheme H can be denoted as $A(H)=\sum_{j=1}^{n}A_{p_{j}}(U_{j})$ , which is also a function of assigned task sets $\{S_{i}\}_{i=1}^{m}$ . Let L be the set of all feasible task sets, in which each set is associated with a worker. It is the same with the auxiliary function. Similarly, we let $F(H)=\sum_{j=1}^{n}F_{p_{j}}(\sum_{i=1}^{m}x_{i,j})$ and it is also a function of $\{S_{i}\}_{i=1}^{m}$ . For $F(H)$ , the following property holds.

Lemma 3. The overall auxiliary function $F(H)$ is monotonic and submodular over L.

Lemma 3 states that $\forall L_{a} \subseteq L_{b} \subseteq \mathcal{L}, \forall S \in \mathcal{L}$ ,

• Monotonicity: $F(L_{a} \cup \{S\}) \geq F(L_{a})$   
- Submodularity: $F(L_{a} \cup \{S\}) - F(L_{a}) \geq F(L_{b} \cup \{S\}) - F(L_{b})$

This property lays the foundation to prove the effectiveness of our online assignment scheme. Using result from work of Kapralov etc. in [16], we have the following theorem.

Theorem 2. If the goal function $G(H)$ is non-negative, monotonic and submodular over $\mathcal{L}$ , then for the online optimization problem to maximize $G(H)$ , the Greedy algorithm is $\frac{1}{2}$ competitive.

In Theorem 2, the Greedy algorithm works by assigning each arriving worker task set with maximal $\Delta G(S)$ and its result is at least half of the optimal $G(H)$ . Theorem 2 fails to apply to our QAOTA algorithm, since $A(H)$ is not submodular and we use $\Delta F_{p_{j}}(k)$ as the greedy metric instead of $\Delta A_{p_{j}}(k)$ . As $F(H)$ can be regarded as an approximation of $F(H)$ , Theorem 2 provides us insight into how well our QAOTA algorithm works to maximize $A(H)$ .

Before analyzing the performance of our assignment algorithm, the relationship between $A_{p_{j}}(k)$ and $F_{p_{j}}(k)$ is further stated in Lemma 4.

Lemma 4. For any $p_j \in (0.5,1]$ , $k > 0$ , $F_{p_j}(k) \geq A_{p_j}(k) \geq 0.5$ and $\frac{F_{p_j}(k) - \frac{1}{2}}{A_{p_j}(k) - \frac{1}{2}} \in [1, \frac{5}{4}]$ .

On the basis of Lemma 4 and previous analysis results, we prove that the assignment scheme generated by our QAOTA algorithm using $\Delta F_{p_j}(k)$ as greedy metric, is competitive with the offline optimal solution which takes overall quality $A(H)$ as goal and the competitive ratio is $\frac{10}{7}$ .

Proof of Theorem 1: Suppose the assignment scheme generated by our QAOTA algorithm is $L$ and the optimal offline assignment scheme is $O$ . We need to prove that $A(L) \geq \frac{7}{10} A(O)$ .

Define $F_{p_j}'(k) = F_{p_j}(k) - 0.5$ . Obviously, the resulting assignment scheme of Greedy algorithm with $F_{p_j}'(k)$ as goal function is the same with $L$ . And $F'(L) = F(L) - \frac{n}{2}$ . Let $I$ be the optimal offline result to maximize $F'(H)$ . According to the definition of $F_{p_j}'(k)$ , it is still monotonic and submodular. Besides, when $k \geq 0$ , $F_{p_j}'(k) \geq F_{p_j}'(0) = 0$ . It satisfies the three requirements in Theorem 2. So according to the Theorem 2, we have

$$
F ^ {\prime} (L) \geq \frac {1}{2} F ^ {\prime} (I)
$$

As $I$ is the optimal assignment scheme to maximize $F'(H)$ , $F'(I) \geq F'(O)$ . With $F'(L) = F(L) - \frac{n}{2}$ and $F'(O) = F(O) - \frac{n}{2}$ , we get

$$
F (L) - \frac {n}{2} \geq \frac {1}{2} [ F (O) - \frac {n}{2} ]
$$

From Lemma 4, we know that

$$
F (O) \geq A (O)
$$

$$
A (L) - \frac {n}{2} \geq \frac {4}{5} [ F (L) - \frac {n}{2} ]
$$

Then,

$$
A (L) - \frac {n}{2} \geq \frac {2}{5} [ A (O) - \frac {n}{2} ]
$$

From the definition of $A_{p_j}(k)$ , we know that $A_{p_j}(k) \in (0.5,1]$ and $A(O) \leq n$ . Thus,

$$
A (L) \geq \frac {7}{1 0} A (O)
$$

Specially if approximation algorithms are used in HSWA, then the competitive ratio will change. To be specific, we have Theorem 3. The proof of Theorem 3 is similar to the proof of Theorem 1 and we omit it here.

Theorem 3. If an $\alpha$ -approximate algorithm is used to solve HSWA in the QAOTA algorithm, then the competitive ratio becomes $\frac{10(\alpha+1)}{5\alpha+9}$ .

# IV. EXPERIMENTAL EVALUATION

In this section, we evaluate the performance and scalability of our proposed task assignment method based on synthetic and real data set.

# A. Experimental Setup

To simulate online behavior of workers and tasks, we produce synthetic and trace-based datasets with varied parameters. In our experiment, all algorithms are implemented in Java and run on a Intel 2.60GHz PC with 4G RAM. For each parameter setting, 20 datasets are generated and results are averaged upon them.

Parameters are generated as follows. $p_{j}$ of task $\tau_{j}$ follows a normal distribution with mean value $\mu_{p}$ and standard deviation $\sigma_{p}$ . The lasting time of task follows normal distribution $N(\mu_{t},\sigma_{t})$ and the expiration time is calculated as task's arriving time plus its lasting time. Similarly worker's capacity follows $N(\mu_{M},\sigma_{M})$ . Worker's travel budget is computed as $B_{i}=c(l_{s_{i}},l_{d_{i}})*\alpha_{i}$ and $\alpha_{i}$ follows $N(\mu_{\alpha},\sigma_{\alpha})$ . Values of $\alpha_{i}$ below 1 are deserted and for $M_{i}$ , values below 1 or above M are deserted. Table I illustrates the default value for these parameters.

For trace-based datasets, we use location traces collected from around 4000 taxis in Shanghai, China as used in prior work [17]. With these traces, we extract the starting time, location and ending location of each passenger's trip to mimic workers' behavior. Specifically, we take trips within a 2 hour time window and the number of trips in it is around 10000. Among them, $m$ trips are randomly selected as tasks. A trip's starting time is regarded as task's arriving time and its starting location is the task's location. Similarly the rest trips play workers going from the starting location to the ending location.

For synthetic datasets, the arrivals of dynamic tasks and workers are generated with Poisson distributions of rates $\lambda_{\tau}$ and $\lambda_{\varpi}$ in a time window of length W. Their corresponding locations are uniformly sampled from a square region.

Table I
DEFAULT PARAMETER SETTING 

<table><tr><td>Parameter</td><td>Value</td></tr><tr><td>Simulation Time Length W</td><td>10 or 1000</td></tr><tr><td>Task Arriving Rate λτ</td><td>1.0</td></tr><tr><td>Worker Arriving Rate λω</td><td>1.0</td></tr><tr><td>Task Probability pj</td><td>μp=0.8, σp=0.15</td></tr><tr><td>Task Lasting Time Tj</td><td>μ=100, σ=30</td></tr><tr><td>Worker Capacity Mi</td><td>μM=3, σM=2</td></tr><tr><td>Worker Capacity Bound M</td><td>8</td></tr><tr><td>Worker Budget αi</td><td>μα=1.5, σα=0.5</td></tr></table>

![](images/8f88be71c5ce45d372b151bc9e745cadcc6601051f5c25ea17c2c59350acaf09.jpg)



![](images/5d34a896b6cf2465dadabdb911726bdbaa8e7d3aee1c437a761a7b27cc8d37b6.jpg)



Figure 3. Average Quality of Synthetic Simulation with W = 10

# B. Performance Evaluation

To evaluate the performance of the QAOTA algorithm, we compare it against the offline optimal solution and three heuristic algorithms, namely GreedyNumber, Nearest, and LeastExpiration. When a worker arrives online, GreedyNumber tries its best to allocate him most tasks while not violating his constraint. Nearest iteratively picks task closest to worker's location until worker's capacity or travel budget is exceeded or no feasible task left. LeastExpiration works in the similar manner of Nearest while it picks tasks with least expiration time first. We use the average quality of tasks $\frac{A(H)}{n}$ as metric to measure and compare the performance of different assignment approaches. Tasks' average quality is equivalent to our goal function $A(H)$ within same dataset. Experimental results illustrate that our QAOTA algorithm approximates the optimal solution. Further it outperforms the three heuristic algorithms under different parameter settings as they don't take tasks' quality into consideration.

1) Comparison with Optimal Solution using Synthetic Small Dataset: We take parameters in Table I with $W$ set to 10 as the default setting and vary parameter $\lambda_{\varpi}$ and $\lambda_{\tau}$ from 0.7 to 1.3 with step of 0.2 separately to generate small datasets. So in these small datasets, the expected number of tasks or workers is in range [7, 13] and we can afford computing the offline optimal solution. We run QAOTA, Optimal and three heuristic algorithms on generated datasets. Task's average accuracies under different settings are recorded and plotted in Fig. 3. It illustrates that our QAOTA algorithm achieve approximate results with the offline optimal solution and outperforms the others.

2) Comparison with Benchmark Solutions using Synthetic Large Dataset: By setting W to 1000 and varying other parameters in Table I, we generate large datasets and apply QAOTA and three heuristic algorithms to them. The results are plotted in Fig 4. In all settings, QAOTA outperforms the three heuristic algorithms. Because only QAOTA considers tasks' quality. Specifically, Nearest and GreedyNumber produce similar results as Nearest depends on the randomly generated task and worker location. LeastExpiration takes task's expiration time into consideration and obtains better results than GreedyNumber and Nearest, especially when task's lasting time is short.

![](images/e99989419d4ac86c53bfd9c4df4ca35c6c363dfce0b8b69daac321c1971be010.jpg)



![](images/3aa440bf99b6fdfdfefe9a4507ea22b41432954b9d039244f921b01ef95b2f7f.jpg)



![](images/0979131c7e8dfcf186ec3d81bcf0a0bdf864cf874347f3b7c0f789e5ad8ac9a8.jpg)



![](images/0dce4463f07e9f8a46dfaa73e82d048c09ec0b39efe3e96f57d6030b0d714d17.jpg)



Figure 4. Average Quality of Synthetic Simulation with W = 1000

![](images/d7a6d20e0506db47a908245859f879f71cb768c1497acec32c842cf1064892cd.jpg)



![](images/b09a91af53f2d7a128267ab499017b0af74e6bb1909c772ff623d1210565d2fd.jpg)



Figure 5. Average Quality with Trace-based Datasets

3) Comparison with Benchmark Solutions using Trace-based Dataset: With trace-based dataset, we vary the value of task number m and workers' travel budget parameter $\alpha$ . The results are plotted in Fig 5. We can tell that with datasets based on real traces, out algorithm still outperforms the three heuristic algorithms.

# C. Scalability Evaluation

The scalability of our online task assignment mechanism mainly depends on the single worker assignment process HSWA. To test HSWA's running time, we generate tasks with locations uniformly sampled from $R$ and set worker's original location and destination at (25, 25) and (75, 75). Task's $\Delta F_{p_j}$ follows uniform distribution in (0, 0.5). We set tasks' arriving time to be 0 and their expiration time to be infinite, which potentially increases the search space and thus results in higher running time. We vary task number, worker's travel budget parameter $\alpha$ . The results are shown in Fig 6. We can tell that the running time of HSWA increases with task number. But it is still below 1.5s when there are 6000 active tasks. Worker's travel budget has little effect on the running time.

![](images/82d4ba48776636854917b8582bebe5c7ccb5eab0fdf799e0394b7d2bc4246247.jpg)



![](images/2245c0b593a676148b5c25e2b8bc10acd135aaa18fd80d05663e287abe328a0d.jpg)



Figure 6. Running Time of HSWA

# V. RELATED WORK

Task assignment in web-based crowdsourcing has been extensively studied. Ioannis [6] aimed to meet real-time demands and return high quality results by efficiently determining the most appropriate set of workers to assign to each incoming task. Karger et al. [18] and [19] proposed an assignment algorithm based on random graph generation and inference algorithms inspired by belief propagation and low-rank matrix approximation. Ho et al. [20] took advantage of "gold standard tasks" to evaluate workers and adaptively assigned tasks using online primal-dual techniques. However, these work neglected the location restriction in MCS scenarios and used bipartite graph matching as the basic model which fails to apply to location-based tasks.

Most work on location-based task assignment do not provide quality-aware online algorithms. He et al. [15] assumed that there is a profit when a worker performs a task and provided an offline algorithm to maximize additive profits. The goal of Kazemi et al. [14], Pournajaf et al. [11] and Shirani-Mehr et al. [21] is to maximize coverage or the number of assigned tasks without considering quality. To our best knowledge, the most related work to our problem are Kazemi et al. [22] and Riahi et al. [23]. But they only proposed heuristic algorithms without performance guarantee. This paper considers the online assignment problem of bisection tasks to maximize quality and an algorithm with competitive ratio $\frac{10}{7}$ is derived.

There are some studies on incentive mechanism design to stimulate smartphone users to join mobile crowdsourcing activities. Yang Dejun et al. [24] provided two incentive mechanisms for a user-centric model and a platform centric model. Zhao Dong et al. [25] designed two online mechanism based on online auction model, aiming to select a subset of workers before specified deadline to maximize the services value under a budget constraint. Similar work on incentive mechanism includes Zhu et al. [26] [27]etc. However they didn't consider the quality control issue while in crowdsourcing answers contributed by workers are unreliable. In this paper, we focus on maximizing quality and leave quality-based incentive mechanism design for future work.

# VI. CONCLUSION

In this paper, we study the quality-aware online task assignment problem in location-based mobile crowdsourcing. An intuitive quality measurement model is adopted without the need of tracking workers and workers' behavior are modeled in a hitchhiking style. We mathematically formulate the problem and propose an efficient online algorithm and analyze its performance theoretically. We prove that the proposed algorithm has competitive ratio of $\frac{10}{7}$ .

In this paper we only consider bisection tasks with anonymous workers and the problem formulation has many limitations. For real-valued or multiple choice tasks and workers with reputation, more comprehensive quality measurement and more efficient assignment algorithms are required. We leave those problems for further study.

# REFERENCES

[1] P. Mohan, V. N. Padmanabhan, and R. Ramjee, “Nericell: rich monitoring of road and traffic conditions using mobile smartphones,” in Proceedings of SenSys, 2008.   
[2] Z. Yang, C. Wu, and Y. Liu, “Locating in fingerprint space: wireless indoor localization with little human intervention,” in Proceedings of Mobicom, 2012.   
[3] Y. Wang, X. Liu, H. Wei, G. Forman, C. Chen, and Y. Zhu, "Crowdatlas: Self-updating maps for cloud and personal use," in Proceeding of MobiSys, 2013.   
[4] “Field agent,” http://www.fieldagent.net/.   
[5] “Gigwalk,” http://gigwalk.com/.   
[6] B. Ioannis and k. Vana, “On task assignment for real-time reliable crowdsourcing,” in Proceedings of ICDCS, 2014.   
[7] C. C. Cao, J. She, Y. Tong, and L. Chen, “Whom to ask?: jury selection for decision making tasks on micro-blog services,” 2012.   
[8] Y. Chon, N. D. Lane, Y. Kim, F. Zhao, and H. Cha, "Understanding the coverage and scalability of place-centric crowdsensing," in Proceedings of Ubicomp, 2013.   
[9] J. Heinzelman and C. Waters, Crowdsourcing crisis information in disaster-affected Haiti. US Institute of Peace, 2010.   
[10] D. Wang, T. Abdelzaher, L. Kaplan, and C. C. Aggarwal, "Recursive fact-finding: A streaming approach to truth estimation in crowdsourcing applications," in Proceedings of ICDCS. IEEE, 2013.   
[11] L. Pournajaf, L. Xiong, V. Sunderam, and S. Goryczka, "Spatial task assignment for crowd sensing with cloaked locations," in Proceedings of MDM, 2014.

[12] X. Liu, M. Lu, B. C. Ooi, Y. Shen, S. Wu, and M. Zhang, “C-das: a crowdsourcing data analytics system,” in Proceedings of the VLDB Endowment, 2012.   
[13] J. Gao, X. Liu, B. C. Ooi, H. Wang, and G. Chen, “An online cost sensitive decision-making method in crowdsourcing systems,” in Proceedings of SIGMOD, 2013.   
[14] L. Kazemi and C. Shahabi, “Geocrowd: enabling query answering with spatial crowdsourcing,” in Proceedings of GIS, 2012.   
[15] S. He, D.-H. Shin, J. Zhang, and J. Chen, “Toward optimal allocation of location dependent tasks in crowdsensing,” in Proceedings of Infocom, 2014.   
[16] M. Kapralov, I. Post, and J. Vondrák, “Online submodular welfare maximization: Greedy is optimal,” in Proceedings of SODA, 2013.   
[17] K. Liu, M. Li, Y. Liu, X.-Y. Li, and H. Ma, “Exploring the hidden connectivity in urban vehicular networks,” in ICNP. IEEE, 2010.   
[18] D. R. Karger, S. Oh, and D. Shah, “Iterative learning for reliable crowdsourcing systems,” in Proceedings of NIPS, 2011.   
[19] D. Karger, S. Oh, and D. Shah, “Efficient crowdsourcing for multi-class labeling,” in Proceedings of SIGMETRICS, 2013.   
[20] C.-J. Ho, S. Jabbari, and J. W. Vaughan, “Adaptive task assignment for crowdsourced classification,” in Proceedings of ICML, 2013.   
[21] H. Shirani-Mehr, F. Banaei-Kashani, and C. Shahabi, “Efficient viewpoint assignment for urban texture documentation,” in Proceedings of GIS, 2009.   
[22] L. Kazemi, C. Shahabi, and L. Chen, “Geotrucrowd: trustworthy query answering with spatial crowdsourcing,” in Proceedings of GIS, 2013.   
[23] M. Riahi, T. G. Papaioannou, I. Trummer, and K. Aberer, "Utility-driven data acquisition in participatory sensing," in Proceedings of EDBT, 2013.   
[24] D. Yang, G. Xue, X. Fang, and J. Tang, “Crowdsourcing to smartphones: incentive mechanism design for mobile phone sensing,” in Proceedings of Mobicom. ACM, 2012.   
[25] D. Zhao, X.-Y. Li, and H. Ma, “How to crowdsource tasks truthfully without sacrificing utility: Online incentive mechanisms with budget constraint,” in Proceedings of Infocom. IEEE, 2014, pp. 1213–1221.   
[26] Z. Feng, Y. Zhu, Q. Zhang, L. M. Ni, and A. V. Vasilakos, "Trac: Truthful auction for location-aware collaborative sensing in mobile crowdsourcing," in Proceedings of Infocom. IEEE, 2014.   
[27] Y. Zhu, Q. Zhang, H. Zhu, J. Yu, J. Cao, and L. M. Ni, "Towards truthful mechanisms for mobile crowdsourcing with dynamic smartphones," in Proceedings of ICDCS. IEEE, 2014.