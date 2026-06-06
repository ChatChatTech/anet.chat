# Vehicle-Based Bi-Objective Crowdsourcing

Xinglin Zhang , Member, IEEE, Zheng Yang, Member, IEEE, and Yunhao Liu, Fellow, IEEE

Abstract— Mobile crowdsourcing is an emerging complex problem solving paradigm that makes use of pervasive mobile devices equipped with multi-functional sensors. Recently, vehicles have also been increasingly adopted for mobile crowdsourcing, as the vehicles, as well as drivers, can provide diverse sensing capability and predictable mobility. Existing mobile crowdsourcing algorithms mostly recruit workers to complete one kind of sensing tasks, i.e., location-based query tasks or automatic sensing tasks. In this paper, we investigate the possibility of recruiting a set of vehicles to simultaneously complete these two categories of tasks, so as to maximize the sensing utility of each participant. We first model the worker recruitment for vehiclebased crowdsourcing as a bi-objective optimization problem with respect to the sensing capability and predictable mobility of vehicles. The recruitment problem is proven to be NP-hard, and we design two heuristic algorithms based on the bi-objective greedy strategy and the multi-objective genetic algorithm to find the solutions. The experimental results with a real-world traffic trace data set show that the proposed algorithms outperform some existing algorithms in finding solutions that maximize both objectives.

Index Terms— Mobile crowdsoucing, vehicle-based crowdsourcing, worker recruitment, task reliability, sensing coverage.

# I. INTRODUCTION

M OBILE crowdsourcing employs pervasive mobiledevices, such as smartphones and tablets, to collect TOBILEcrowdsourcing employspervasive mobile various sensed data via the embedded sensors and construct a variety of applications [1]. In this paradigm, large amounts of ordinary mobile users participate in sensed data collection at their convenience, and thus the cost of data collection can be significantly reduced compared with the traditional paradigms that recruit experts. In addition, the ubiquity of mobile devices and convenient communication networks make it promising to build large-scale applications via mobile crowdsourcing. Therefore, mobile crowdsourcing attracts more and more attention across multi-disciplinary communities. Typically, vehicle-based mobile crowdsoucing is

Manuscript received April 28, 2017; revised August 24, 2017; accepted October 22, 2017. This work was supported in part by the National Natural Science Foundation of China under Grant 61502178 and Grant 61632013, and in part by the Natural Science Foundation of Guangdong province under Grant 2016A030313480. The Associate Editor for this paper was N. Papanikolopoulos. (Corresponding author: Zheng Yang.)

X. Zhang is with the School of Computer Science and Engineering, South China University of Technology, Guangzhou 510006, China (e-mail: zhxlinse@gmail.com).

Z. Yang and Y. Liu are with the School of Software, Tsinghua University, Beijing, China, and also with the Tsinghua National Laboratory for Information Science and Technology, Tsinghua University, Beijing 100084, China (e-mail: yang@greenorbs.com; yunhao@greenorbs.com).

Color versions of one or more of the figures in this paper are available online at http://ieeexplore.ieee.org.

Digital Object Identifier 10.1109/TITS.2017.2766769

![](images/1283fd11948f1cb082cde15da5dcfb7714b89ed291fa1de7754c54f2a288cda4.jpg)



Fig. 1. An example of vehicle-based bi-objective crowdsourcing: two workers are traveling in the area of the sensing task, at the same time query tasks locate in the vicinity of their routes. In this scenario, workers can turn on their sensors for the automatic sensing task and complete the query tasks when passing by the corresponding locations.

proliferating rapidly. The vehicle-mounted sensors and smartphones carried by drivers possess great potentials for complex problem solving. Various crowdsourcing applications based on vehicles thus have been investigated, such as road condition monitoring [2], map updating [3], environment monitoring [4], urban monitoring [5], parking spot monitoring [6], and vehicle Internet access [7].

Generally, a vehicle-based crowdsourcing system consists of two roles: the worker and the recruiter. Workers are a group of vehicles and drivers who are willing to participate in the crowdsourcing tasks based on their sensing capabilities. They usually require a certain amount of rewards from the recruiter [8], [9]. The goal of the recruiter, usually with a limited budget, is to select a subset of available workers, such that the selected workers can provide sufficient sensed data for building high-quality applications. Therefore, one essential problem for vehicle-based crowdsourcing is to seek a trade-off between the recruitment budget and the quality of application.

Two categories of mobile crowdsourcing tasks have received extensive attention in research communities. The first category emphasizes on the automatic sensing capability of mobile devices for data collection. For example, in some road condition monitoring applications, the sensed data, such as accelerator and GPS readings, are continuously recorded for later processing. In such applications, a common objective is to find a subset of workers to cover as many roads as possible within the region of interest. The other category of tasks, however, requires that workers actively respond to location-based query tasks. For example, in some parking spot monitoring applications, workers are required to report the vacant parking space via actively taking pictures. This kind of applications usually lean upon worker redundancy to ensure task completion quality.

Existing research works mostly studied these two categories of mobile crowdsourcing tasks separately. In this work, we propose a new bi-objective crowdsourcing system, where one automatic sensing task and one location-based query task are combined and assigned to a set of workers. The rationality of the combination lies in a key link between the two categories of tasks: when a worker is traveling towards a destination, his trajectory of sensed data provides useful coverage for specific sensing tasks, and he can actively complete some query tasks that are located along his route (see Fig. 1). For example, a road condition monitoring task and a parking spot monitoring task can be integrated and completed by the same set of workers, who are willing to contribute automatic sensing capability during the journey, and are willing to take a picture of parking state when arriving at the destination. Intuitively, this combination is more efficient in fully using the active and passive sensing capabilities of each worker. In contrast, in existing solutions, a worker has to commit to two applications when he can complete two kinds of tasks.

To efficiently recruit workers for the bi-objective crowdsourcing tasks, we first propose the budget-constrained optimization models for both automatic sensing and locationbased query tasks. For the automatic sensing task, the sensing quality highly depends on recruiting a set of workers with widely distributed trajectories. We resort to the predictability of vehicle mobilities [10]–[13] for coverage evaluation in this paper. For the location-based query task, we try to maximize the probability that each query task can be completed correctly. After constructing the bi-objective model, we study its structure properties, and propose two effective schemes to solve the recruitment problem. Our main contributions can be summarized as follows:

• We formulate the vehicle-based bi-objective crowdsourcing problem as an optimization problem and prove that it is NP-hard. To the best of our knowledge, this is the first attempt that accommodates two optimization objectives in vehicle-based crowdsourcing.   
• We propose a greedy heuristic algorithm and a genetic algorithm to efficiently solve the recruitment problem by taking into account the sensing and query quality requirement.   
• We evaluate the proposed algorithms using a real-world traffic trace dataset. The experimental results show the superiority of our algorithms when considering the sensing and query quality simultaneously.

The rest of the paper is organized as follows. Section II summarizes the related works. Section III introduces the main definitions and demonstrate the vehicle-based bi-objective crowdsourcing problem. Section IV and Section V propose two efficient algorithms in detail to solve the proposed problem. In section VI, we evaluate the proposed algorithms and discuss the results. Finally, the conclusions are drawn in Section VII.

# II. RELATED WORK

Location-based query task assignment in mobile crowdsourcing aims to efficiently match tasks to mobile workers [14]. He et al. [15] proposed to allocate query tasks to workers by modeling the task completion redundancy and traveling distance constraint so as to achieve high efficiency. Liu et al. [16] studied two optimization problems: maximizing the total number of accomplished tasks or minimizing the total incentive payments, given that the total traveling distance is minimized. Reddy et al. [17] made use of workers’ geographic and temporal availability, and their habits of participation, to recognize a set of well-suited workers. Kazemi et al. [18] studied efficient assignment schemes to obtain high completion quality of query tasks in the scenario where worker quality is accessible. Zhang et al. [19] optimized the task assignment by considering the tradeoff of task quality and recruitment budget. In addition to the worker quality, Cheng et al. [20] and Guo et al. [21] modeled the spatial-temporal diversity requirement of some query tasks that are influenced by the various observation angles. Guo et al. [22] studied the worker selection based on workers’ intentional movement for timesensitive tasks and unintentional movement for delay-tolerant tasks.

TABLE I MAIN NOTATIONS 

<table><tr><td>Symbol</td><td>Description</td></tr><tr><td> $t_{i}, W_{i}$ </td><td>a location-based query task and its assigned worker set</td></tr><tr><td> $T, W$ </td><td>the query task set and the worker set</td></tr><tr><td> $m, n$ </td><td>the number of query tasks and the number of workers</td></tr><tr><td> $S$ </td><td>the selected worker set for both query and sensing tasks</td></tr><tr><td> $w_{j}, c_{j}, p_{j}, R_{j}$ </td><td>a mobile worker (vehicle), and his cost, confidence, and trajectory</td></tr><tr><td> $F_{t_{i}}(\cdot), F(\cdot)$ </td><td>the query reliability function for task  $t_{i}$ , the average query reliability function</td></tr><tr><td> $G(\cdot)$ </td><td>the sensing coverage function</td></tr><tr><td> $B$ </td><td>the recruiter&#x27;s budget</td></tr></table>

The above works tackle the batch task assignment, where a set of tasks and workers are present for the system. Recently some researchers also studied an online setting, where tasks and workers are appearing to the system dynamically. Zhang et al. [23] considered the scenario where workers are arriving and submitting bids for tasks dynamically, while Tong et al. [24] examined the setting where both workers and tasks are appearing online. Xiao et al. [25] designed greedy task assignment algorithms for both offline and online tasks in mobile social networks.

Another direction of mobile crowdsourcing is to recruit suitable workers to achieve high coverage for sensing tasks. Sensing tasks typically emphasize on applying the embedded sensors of mobile devices to continuously collect and aggregate sensed data. By using the historical traces of workers, CrowdRecruiter [26] tried to select a subset of workers to satisfy the probabilistic coverage constraints for multiple sensing cycles. Xiong et al. [27] also studied a dual problem where the recruiter intended to maximize the probabilistic coverage given a fixed budget. Zhang et al. [28] used the relative positions of workers and query tasks to estimate the joint coverage of a set of workers. Differently, Ahmed et al. [29] and Hachem et al. [30] used worker mobility models to select a minimal number of workers to satisfy the coverage requirement. Wang et al. [31] proposed to minimize subarea selection for sensing by applying compressive sensing and Bayesian inference techniques. He et al. [32] applied predictable trajectories in vehicle-based crowdsourcing to select workers with high coverage.

Mobile crowdsourcing has been applied for developing some applications in the area of environment and traffic monitoring. In the Mobile Millennium project [33], workers with mobile phones are recruited to collect and upload realtime traffic information to a service server, which can build prediction models for the future traffic condition based on the reported data. Similarly, The CalTel [34] and Nericell [2] systems are designed to aggregate traffic and road condition information by using the smartphone sensors and vehicle-mounted sensors. By employing both traditional wireless sensor networks and mobile workers with smartphones, DroneSense [4] provides an environmental monitoring service. Yu et al. [35] proposed travel package recommendation solutions based on crowdsourced user footprints. To facilitate intelligent transportation, GreenGPS [36] leverages sensed data to build a navigation application, which guides drivers to follow the most fuel-efficient routes between arbitrary end-points.

The aforementioned works mostly focus on either query tasks or sensing tasks for mobile crowdsourcing. In this work, we consider the scenario where a worker in vehicle-based crowdsourcing can complete both categories of tasks, such that the recruiter can make full use of the capability of each worker and thus maximize the system utility.

# III. PROBLEM STATEMENT

This section presents the main definitions and the formulated problem. For clarity, the main notations are summarized in Table I.

The objective of vehicle-based bi-objective crowdsourcing (VBC) is to recruit the most suitable workers from the candidate worker set to complete sensing and query tasks simultaneously under the recruiter’s budget. The recruitment process of VBC is assumed to be organized in periods (e.g., five two-hour cycles per day from 08:00 to 18:00). In each cycle, the workers with predicted trajectories and accessible query tasks are evaluated and selected based on the optimization objectives.

At the beginning of each period, the recruiter pools the valid query tasks and candidate workers, and tries to match query tasks to the suitable workers. We assume that each worker can be assigned with one query task in each period and he may participate in multiple periods [14]. After being assigned with a query task $t _ { i } ,$ a worker $w _ { j }$ sometimes may be unable to answer the query correctly (e.g. taking a wrong photo). Thus, each worker $w _ { j }$ is associated with a confidence $p _ { j }$ , which is the reliability (or skill) that the worker $w _ { j }$ can successfully complete the task. The confidence of a worker can be inferred from the historical data of performing tasks [37], [38]. As learning worker confidence is not the focus of this paper, we assume that the system has acquired the confidence values before assigning tasks. The formal definition of a worker in the VBC problem is given as follows.

Definition 1 (Worker): A worker $w _ { j }$ is a vehicle equipped with multi-functional sensors for the automatic sensing task, and is willing to complete location-based query tasks that are located along his traveling route $R _ { j }$ in the given period. Worker $w _ { j }$ is associated with a cost $c _ { j }$ for participation, and a confidence value $p _ { j }$ indicating the probability that he can successfully complete the assigned query task.

With this definition, the goal of VBC considering query tasks is to guarantee that each task can be completed by the assigned workers with a high probability.

Definition 2 (Query Reliability): Given a query task $t _ { i } ,$ and the worker set Wi assigned to ti , the completion reliability of $t _ { i }$ is defined as:

$$
F _ {t _ {i}} (W _ {i}) = 1 - \prod_ {w _ {j} \in W _ {i}} (1 - p _ {j}). \tag {1}
$$

Note that $\textstyle \prod _ { w _ { i } \in W _ { i } } ( 1 - p _ { j } )$ is the probability that no assigned worker correctly complete the query task $t _ { i }$ . Therefore, $F _ { t _ { i } } ( W _ { i } )$ reflects that at least one assigned worker can successfully complete $t _ { i } .$ . The overall quality of query tasks thus can be reflected by the average value of the query quality of each task:

$$
F (S) = \frac {1}{m} \sum_ {t _ {i} \in T} F _ {t _ {i}} (W _ {i}), \tag {2}
$$

where $S = \cup _ { t _ { i } \in T } W _ { i }$ , and m is the size of the query task set.

The other objective of VBC is to maximize the sensing coverage of the area of interest. The coverage of workers is evaluated by their trajectories. In the context of vehicle-based crowdsourcing, the trajectory of vehicles can be obtained via several techniques. For example, the public transportation with fixed schedules (e.g., buses) has predetermined routes; Vehicles using navigation services usually follow the suggested paths [10]; And trajectory prediction [11], [12] and destination prediction methods [13] can be employed to predict the trajectory. Therefore, in this study, we assume that the candidate workers’ trajectories have been obtained by the recruiter. The sensing coverage of a set of workers thus can be defined as follows.

Definition 3 (Sensing Coverage): Given a selected worker set $S = \cup _ { t _ { i } \in T } W _ { i }$ (where T is the set of all query tasks), and the predicted trajectory $R _ { j } = \{ r _ { 1 } , r _ { 2 } , . . . , r _ { k _ { j } } \}$ for each worker $w _ { j } \in W _ { i }$ (where $k _ { j }$ is the number of units covered by $w _ { j } )$ , the joint sensing coverage of S is defined as:

$$
G (S) = | \cup_ {w _ {j} \in S} R _ {j} |. \tag {3}
$$

Note that the sensing measurement metrics can be changed according to the specific application scenarios. In this paper, we adopt the cardinality of covered units (e.g., road segments and cellular towers) as the metric.

With the basic concepts illustrated above, we now define our VBC problem below.

Definition 4 (Vehicle-Based Bi-Objective Crowdsourcing $( V B C ) ) \mathrm { : }$ Given a candidate worker set $W = \{ w _ { 1 } , w _ { 2 } , . . . , w _ { n } \}$ (where n is the number of workers), each worker $w _ { j } ~ \in ~ W$ is associated with a trajectory $R _ { j } = \{ r _ { 1 } , r _ { 2 } , . . . , r _ { k _ { j } } \}$ in the region of the sensing task. A set of location-based query tasks $T = \{ t _ { 1 } , t _ { 2 } , \ldots \ldots , t _ { m } \}$ (where m is the number of query tasks) are located along the trajectories. The problem of VBC is to solve the following optimization problem:

$$
\max _ {S \subseteq W} (F (S), G (S)) \quad \text { s.t. } \quad \sum_ {w _ {j} \in W _ {i}, \forall t _ {i} \in T} c _ {j} \leq B, \tag {4}
$$

where $S = \cup _ { t _ { i } \in T } W _ { i } \ \subseteq \ W$ is the selected subset of workers, and $w _ { j } \in W _ { i }$ represents that the selected worker $w _ { j }$ is assigned to the query task $t _ { i }$ located along his trajectory.

According to Definition 4, the VBC problem is a constrained optimization problem with two objectives: maximizing the average reliability of all query tasks and maximizing the joint trajectory coverage of all recruited workers, given that the total cost of the worker recruitment does not exceed the recruiter’s budget. The challenge of tackling the VBC problem is that, with m query tasks and n workers, in the worst case, there exist an exponential number of possible task matching strategies (i.e., with time complexity of $O ( m ^ { n } ) )$ . In fact, we can show that the VBC problem is NP-hard. Therefore, it is impractical to enumerate all possible matching strategies.

Lemma 1: The VBC problem is NP-hard.

Proof: Please refer to Appendix A.

# IV. GREEDY ALGORITHM FOR VBC

In this section, we derive the properties of each objective function of the VBC problem, and then propose an efficient greedy algorithm to approximately solve the VBC problem.

# A. Properties of optimization goals

1) Query Reliability: First, we give the property of the reliability upon assigning a new worker.

Lemma 2: The reliability function $F _ { t _ { i } } ( W _ { i } )$ for each query task $t _ { i }$ is nondecreasing w.r.t. the assigned worker set $W _ { i }$ .

Proof: Please refer to Appendix B.

Based on Lemma 2 and the fact that adding a worker $w _ { j } \in$ $W _ { i } \subseteq S$ only influences the reliability function value $F _ { t _ { i } } ( W _ { i } )$ , we can obtain the following lemma:

Lemma 3: The average reliability function F(S) is nondecreasing w.r.t. the selected worker set S.

2) Sensing Coverage: Next, we demonstrate the property of the sensing coverage upon adding a new worker.

Lemma 4: The sensing coverage function G(S) is nondecreasing w.r.t. the selected worker set S.

Note that Lemma 4 can be directly derived from the arguments showing that the sensing coverage function G(S) is monotone in the proof of Lemma 1.

# B. The greedy algorithm

Based on Lemma 3 and Lemma 4, we propose a greedy algorithm, named VBC-Greedy (Algorithm 1), to select and assign workers iteratively to achieve the two optimization goals simultaneously.

Initially, we set the assigned worker set $W _ { i }$ for each task $t _ { i } \in T$ and the recruited worker set S to be empty, as there is no worker assignment yet. We also introduce a variable C to denote the current cost of the selected workers (Line 1). We then identify all the valid query task and worker pairs $( t _ { i } , w _ { j } )$ in the system (Line 2). The validity here means that the worker $w _ { j } \mathrm { ' s }$ trajectory covers the location of the query task ti , hence he is able to complete $t _ { i }$ during the journey. Then, we would like to incrementally select the best workers and assign them to the suitable query tasks given the system budget constraint, such that the query quality and sensing coverage are always maximized (Lines 3-18).

Algorithm 1 VBC-Greedy   
Require: Budget B, Query task set T, Worker set W
Ensure: Assigned worker set $W_{t_i}, \forall t_i \in T$ 1: $S \leftarrow \emptyset, W_i \leftarrow \emptyset, C \leftarrow 0;$ 2: compute all the available pairs of query tasks and workers $M \leftarrow \{(t_i, w_j) | t_i \in T, w_j \in W\}$ ;

3: while $M \neq \emptyset$ do

4: for $w_j \in W$ do

5: if $c_j + C \geq B$ then

6: $W \leftarrow W \setminus \{w_j\}, M \leftarrow M \setminus \{(t_i, w_j) | t_i \in T\}$ ;

7: end if

8: end for

9: for $(t_i, w_j) \in M$ do

10: compute the weighted increment pair $(\Delta_{w_j} F_{t_i}, \Delta_{w_j} G)/c_j;$ 11: end for

12: prune $(\Delta_{w_j} F_{t_i}, \Delta_{w_j} G)/c_j$ dominated by others;

13: rank the pairs by their scores (i.e., the number of dominated pairs);

14: if $M \neq \emptyset$ then

15: select a pair $(t_i, w_j)$ with the highest score;

16: $W_i \leftarrow W_i \cup \{w_j\}, S \leftarrow S \cup \{w_j\}, C \leftarrow C + c_j, M \leftarrow M \setminus \{(t_i, w_j) | t_i \in T\}$ ;

17: end if

18: end while

In each selection iteration, we first examine the cost of each candidate, and remove the workers who will cause the violation of the budget constraint once recruited (Lines 4-8). Then, for every query task and worker pair $( t _ { i } , w _ { j } )$ , we can calculate the weighted increment of the query quality and sensing coverage $( \Delta _ { w _ { j } } F _ { t _ { i } } , \Delta _ { w _ { j } } G ) / c _ { j }$ , where $\Delta _ { w _ { j } } F _ { t _ { i } } = F _ { t _ { i } } ( W _ { i } \cup \{ w _ { j } \} ) - F _ { t _ { i } } ( W _ { i } )$ , and $\Delta _ { w _ { j } } G = G ( S \cup$ $\{ w _ { j } \} ) - G ( S )$ . As guaranteed by Lemma 2 and Lemma 4, here the two optimization operations are nondecreasing.

To select the most valuable pair, we first filter out the pairs dominated by others (Line 12). A pair $( t _ { i } ^ { \prime } , w _ { j } ^ { \prime } )$ is said to be dominated by a pair $( t _ { i } , w _ { j } )$ , if $\Delta _ { w _ { j } } F _ { t _ { i } } / c _ { j } \stackrel { \prime } { > } \Delta _ { w _ { i } ^ { \prime } } F _ { t _ { i } ^ { \prime } } / c _ { j } ^ { \prime }$ and $\Delta _ { w _ { j } } G / c _ { j } \geq \Delta _ { w _ { i } ^ { \prime } } G / c _ { j } ^ { \prime }$ , or $\Delta _ { w _ { j } } F _ { t _ { i } } / c _ { j } \ge \Delta _ { w _ { j } ^ { \prime } } F _ { t _ { i } ^ { \prime } } / c _ { j } ^ { \prime }$ and $\Delta _ { w _ { j } } G / c _ { j } ~ > ~ \Delta _ { w _ { i } ^ { \prime } } G / c _ { j } ^ { \prime }$ . The remaining pairs after pruning can be ranked according to the number of pairs that they are dominating [39] (Line 13). The pair with a higher rank indicates that this assignment is more available than other assignments. Therefore, we select a pair $( t _ { i } , w _ { j } )$ with the highest score, and remove all pairs $\{ ( t _ { i } , w _ { j } ) | t _ { i } \in T \}$ containing the worker $w _ { j }$ (Lines 14-17).

# V. GENETIC ALGORITHM FOR VBC

The VBC problem belongs to the family of constrained multi-objective optimization problems. In general, there are a set of optimal solutions (largely known as Pareto-optimal solutions). Without any further information, it is nontrivial to say that one of these pareto-optimal solutions is better than the others. Therefore, it is helpful to find as many pareto-optimal solutions as possible in some situations. From this optimization point of view, we apply a multi-objective genetic algorithm, named NSGA-II [40], to find pareto-optimal solutions for the VBC problem. Then we can select the solution that maximizes both query and sensing objectives from these pareto-optimal solutions. As a by-product, other pareto-optimal solutions put different weights on the two objective functions, which may be useful in some scenarios when the recruiter wants to emphasize on one objective.

A genetic algorithm generally contains the following aspects: genetic representation, fitness evaluation, and genetic operations. We illustrate our approach considering these aspects in the following.

# A. Genetic Representation

A genetic algorithm requires a chromosome to encode the candidate solutions of an optimization problem. In the VBC problem, we use an array of length n, where n is the number of candidate workers, to represent the solutions. The index of the array represents the ID of a worker, and the entry value of the array represents the ID of the assigned query task for that worker. The task ID is determined locally according to each worker’s accessible task set. As normally a worker is able to complete a small subset of the query tasks, this coding strategy saves the effort of searching for a suitable assigned task ID for a worker when compared with the unified coding for the whole set of tasks. In this strategy, the task ID ranges from one to the size of accessible tasks for a worker, and the value zero represents that no task is assigned to the worker. Fig. 2a shows an example, where the array presents that workers w1, w2, w4, w6, and w7 are assigned to the accessible tasks with local IDs 2, 3, 5, 2, and 1, respectively.

# B. Fitness Evaluation

A fitness function in a genetic algorithm represents how well a chromosome fits the optimization goal. In the VBC problem, we have two objective fitness functions, i.e., Eq. (2) and (3). To jointly optimize these two goals, we define a partial order to compare chromosomes:

Definition 5 (Partial Order ≺): Given two solutions (i.e., worker assignment arrays) $S = \cup _ { t _ { i } \in T } W _ { i }$ and $S ^ { \prime } = \cup _ { t _ { i } \in T } W _ { i } ^ { \prime } ,$ the partial order of S and $S ^ { \prime }$ is defined as: $S \prec S ^ { \prime }$ if and only if $F ( S ) > F ( S ^ { \prime } )$ and $G ( S ) \ge G ( S ^ { \prime } )$ , or $F ( S ) \ge F ( S ^ { \prime } )$ and $G ( S ) > G ( S ^ { \prime } )$ . We say that S dominates $S ^ { \prime }$ if $S \prec S ^ { \prime }$ .

Since the recruiter has a budget for the worker recruitment, a feasible solution must satisfy that the total cost of the assigned workers does not exceed the given budget. Also, in the chromosome representation, each entry value of a feasible chromosome has to be constrained to the local task ID range. Considering these requirements, we further define a constrained partial order to compare different chromosomes.

![](images/23d9d2cab422d67a0cb0750d6972c26f2f908d19b7843a97c82184ddc279c13c.jpg)



Fig. 2. The components of genetic algorithm for VBC. (a) Using a numeric array to represent an assignment solution; (b) Crossover of two assignment solutions; (c) Mutation of an assignment solution.

Definition 6 (Constrained Partial Order $\prec _ { c } ) \colon$ Given two solutions $\begin{array} { r c l } { S } & { = } & { \cup _ { t _ { i } \in T } W _ { i } } \end{array}$ and $\begin{array} { r c l } { S ^ { \prime } } & { = } & { \cup _ { t _ { i } \in T } W _ { i } ^ { \prime } } \end{array}$ , the constrained partial order of S and $S ^ { \prime }$ is defined as: $S \prec _ { c } S ^ { \prime }$ if any of the following conditions is true.

• Solutions S and $S ^ { \prime }$ are feasible, and $S \prec S ^ { \prime } ;$   
• Solution S is feasible, and solution $S ^ { \prime }$ is infeasible;   
• Solutions S and $S ^ { \prime }$ are infeasible, and S has a smaller overall cost.

We say that S constrained-dominates $S ^ { \prime }$ if $S \prec _ { c } S ^ { \prime }$ .

# C. Genetic operations

The initial population of solutions is generated by randomly constructing a certain amount of chromosomes. To generate a new population, a genetic algorithm generally adopts three operations: selection, crossover, and mutation. First, selection operation chooses individual chromosomes for later breeding. We apply the tournament selection strategy which repeatedly chooses the best individual (with respect to the fitness evaluation) of a randomly chosen subset of the remaining chromosomes for later operations. Crossover represents the genetic recombination in nature. We use two solutions after the aforementioned selection and swap their genetic representations to generate new solutions. For example, in Fig. 2b, given two task assignment solutions {4,0,1,1,3,0,5} and {2,3,0,5,0,2,1} for the seven workers, the crossover operation divides the solutions and recombines the four parts to generate new individuals. Mutation is applied to alter the content in a solution from its initial state. This operation is analogous to biological mutation, which maintains genetic diversity of the chromosomes. Fig. 2c shows an example of mutation, where the assignment for worker w2 and w5 are changed to form a new solution.

# D. The Genetic Algorithm

Combining the aforementioned components, the proposed algorithm is sketched in Algorithm 2. Line 1 generates

# Algorithm 2 VBC-GA

Require: Budget B, Query task set T , Worker set W

Ensure: Ranked assignment sets P

1: generate initial population $P _ { 0 }$ of size N ;   
2: $Q _ { 0 } \gets N E W P O P ( P _ { 0 } )$   
3: $k = 0 ;$   
4: while Termination Rule is not met do   
5: $R _ { k } \gets P _ { k } \cup Q _ { k } ;$   
6: evaluate the fitness of $R _ { k }$ according to the objectives Eq. (2) and (3);   
7: $P _ { k + 1 } $ first N solutions w.r.t. the ranking (Definition 6) by nondominated sorting [40];   
8: $Q _ { k + 1 }  N E W P O P ( P _ { k + 1 } ) ;$   
9: $P \gets P _ { k + 1 } ;$   
10: $k \gets k + 1 ;$   
11: end while

![](images/13f72417f40eff235ac589716eeb1877ee715e9a27b3f8c149ba0a58c69afb49.jpg)



(a)

![](images/ab3b245b5ae96fcbf43ef3a9bc2f75abf7600a349da11c463df36255c1278179.jpg)



(b)   
Fig. 3. Road network of Beijing. (a) A map scene of Beijing. (b) The digital road network of Beijing.

initial populations with a specified size N, and the function N E W P O P(·) in Line 2 forms candidate individuals by adopting the above genetic operations. Then, the main loop (Lines 4-11) iteratively selects better individuals as survivals for finding the best solutions. Lines 6-7 rank solutions via nondominated sorting by using the constrained partial order rule defined above. The loop ends when the termination rule is met. Typically, a genetic algorithm terminates when the predefined maximum number of iterations completes. The parameters for the genetic algorithm are empirically set following the suggestions in the literature [40].

# VI. EXPERIMENT

In this section, we evaluate the performance of the proposed algorithms based on a real-world traffic trace dataset. We first introduce the experiment settings and compared algorithms, and then show the results with discussion.

# A. Settings

1) Dataset: We use the real-world dataset, T-drive [41], [42], to conduct the experiment. T-drive contains the GPS traces of 10,357 taxis in Beijing for a period of one week in 2008. There are around 15 million GPS sampling points collected. We consider each taxi as a mobile worker, who is equipped with sufficient multi-functional sensors for both automatic sensing and location-based query tasks. The confidence and cost of a worker is randomly generated according to the uniform distribution within the range [0.5, 0.9].

As depicted in Fig. 3, the road network of Beijing is used as the area for a sensing task (such as noise map generation or road condition monitoring). We generate location-based query tasks in the road network of Beijing. Specifically, the road network is a connected network of road segments. Each road segment is associated with several attributes, including segment length, segment ID, and the GPS coordinates of the head and end of the segment. An HMM algorithm [43] is employed to perform the map matching process, which assigns GPS points of a worker’s trajectory to the road network, i.e., the corresponding road segment sequence. The query task is randomly generated among the GPS coordinates of the segment ends that have been visited by at least one taxi. In this generation approach, after we determine the number of query tasks, the number of candidate workers is fixed.

The recruitment process is organized in two-hour periods. The road segment attached by the first GPS coordinate of each worker in a period is the starting position of the worker. The road segment sequence in that period is the coverage trace of the worker. Specifically, the coverage function value of a worker is the number of segments that have not been covered by others. A worker is able to complete a query task whose GPS coordinate is traversed by the worker’s trace. In this way, we can obtain the task and worker sets with necessary attributes.

2) Comparisons: We evaluate the proposed algorithms by comparing with the following algorithms:

• The first algorithm (named C-Greedy in this paper) tries to maximize the joint coverage of the recruited workers under the recruitment budget constraint [27]. The algorithm uses a weighted greedy strategy, where the worker is iteratively selected based on the coverage increment scaled by the cost. After selecting a worker, we assign the most valuable query task to the worker for the query task evaluation in the experiment.   
• The second algorithm (named Q-Greedy in this paper) intends to maximize the average query reliability value of the location-based query tasks [19]. After a worker is selected, we record the coverage increment by adding the worker’s trajectory and update the total coverage of the selected workers.

In the experiment, the average query reliability is adopted to evaluate the performance of the algorithms considering the location-based query tasks. For the sensing coverage, as the number of candidate workers and budgets vary in different settings, the number of covered segments are not convenient for illustration. Therefore, we use the ratio of the number of covered segments to that of the total segments of the candidate workers as the measurement for the automatic sensing tasks.

# B. Results

1) The Effect of the Query Task Number: First, we fix B = 400 and set m = {200, 250, 300, 350, 400}. VBC-GA is able to find a set of nondominated solutions. Fig. 4 shows two examples of the generated nondominated solutions by VBC-GA, as well as the solutions generated by the other three algorithms. As can be seen, all solutions generated by the four algorithms are located approximately along a nondominated frontier from the perspective of multi-objective optimization. However, the goal of the worker assignment for VBC is to achieve high performance considering both objectives in this paper. Therefore, we prefer solutions that are closer to the right-upper corner in the figure. Therefore, in the detailed performance comparison in the following, we only use one representative solution of VBC-GA that achieves both high sensing and query values.

![](images/0ba72081f85438dd08a7867c1365bdebd1590f62add398bf20d307b7c416c7bb.jpg)



![](images/a135c1a8e3471ce3e07d44e6812144ca299f756ac2681b3c1c4ff7ba9f50cb73.jpg)



(b)

Fig. 4. Nondominated Solutions (B = 400). (a) m = 200. (b) m = 400.   
![](images/8bc5dc3daf53d8384c3ed5a6111bba3606b9bd3cbab2f7a90a7f4d97cc76e041.jpg)



![](images/cd167c03b9d00cc48904f19554b318414bbd37e38b8b075afa654a92f6001112.jpg)



(b）)

Fig. 5. Performance of Sensing Coverage. (a) Sensing coverage. (b) Coverage performance comparison.   
![](images/25f16343c243feff97b9a5c115120a69ab528cf1c75fd0ea48c8e772c5f96e8c.jpg)



(a)

![](images/2f5082c86ac758e82999a99ee25cd7871c6168e9fd2ad3dced712ac8e02f7d07.jpg)



Fig. 6. Performance of Query Reliability. (a) Query reliability. (b) Reliability performance comparison.

In Fig. 5a, we can see that the sensing coverage of all algorithms decrease with the increment of query task numbers. This trend is due to the fact that, when the number of query tasks increases, the candidate worker size also increases. Thus, when the recruitment budget is fixed, the recruited workers’ joint coverage ratio slightly decreases. Fig. 5b shows the coverage comparison between different algorithms. VBC-GA and VBC-Greedy achieve comparable coverage values, which are slightly smaller (less than 5%) than that of C-Greedy, and are larger (more than 15%) than that of Q-Greedy.

On the other hand, the query reliability values of the four algorithms decrease with the increment of query task numbers (Fig. 6a). It is because that the recruitment budget is fixed, and thus the average budget per task is reduced with the increment of task numbers. The detailed reliability comparison is shown in Fig. 6b. We can see that, again, VBC-GA and VBC-Greedy have similar reliability values, which are slightly smaller (less than 4%) than that of Q-Greedy, and are larger (ranging from 15% to 38%) than that of C-Greedy.

![](images/0488df67445d3b9f2ff3cb8d5f5cdd3e78481302e20fc8d91f05ce516a9c75bd.jpg)



(a）

![](images/782dfc41c12a041c70fa3eec578600bf23be8387ed993b4a4379542a24945e58.jpg)



(b)

Fig. 7. Percent of Shared Workers among Different Algorithms (B = 400). (a) m = 200. (b) m = 400.   
![](images/d265f0d47c759ca5d14c9428e38d3eaed6683198eef08f2f1ca84625dff37314.jpg)



![](images/61b947c0e38bfa86f59b1da2ecaa45b7e6e2e81bc5f9b40d9c8871e3e8ae518f.jpg)



Fig. 8. Performance of Sensing Coverage. (a) Sensing coverage. (b) Coverage performance comparison.

The performance differences can also be reflected by the shared workers selected by the four algorithms. Fig. 7 shows two examples of matrix diagrams corresponding to the percentage of common workers recruited by algorithms in each row and algorithms in each column (taking the number of workers selected by algorithms in each row as the denominator). For example, Fig. 7a shows that around 82% of workers selected by VBC-Greedy are shared with VBC-GA, while on average 32% and 33% of workers selected by C-Greedy and Q-Greedy are shared with VBC-GA. Also C-Greedy and Q-Greedy have only around 20% of workers shared by each other. These results implicate that VBC-GA and VBC-Greedy may perform comparably with respect to the bi-objective optimization goals, while the two compared algorithms may have extreme performances. A similar phenomenon can be observed in Fig. 7b.

In summary, the proposed VBC-GA and VBC-Greedy algorithms achieve more competitive results with respect to the two objectives, while C-Greedy and Q-Greedy have marked shortages considering query reliability and sensing coverage, respectively.

2) The Effect of the Recruiter’s Budget: We now investigate the effect of the recruitment budget by fixing m = 300 and varying $B ~ = ~ \{ 3 0 0 , 3 5 0 , 4 0 0 , 4 5 0 , 5 0 0 \}$ . Fig. 8a shows that with the increment of the recruitment budget, the sensing coverage values of the four algorithms gradually increases.

![](images/50039931cd19fd02ee53aca9dcc9734897a533106d6149d46a06e6632b68da75.jpg)



(a)

![](images/b0fb0083bfd5fa33d70c4b9e275149e27846a82163b014fbc8d6d8834c2bd429.jpg)



(b）

Fig. 9. Performance of Query Reliability. (a) Query reliability. (b) Reliability performance comparison.   
![](images/98b582de6095425a5f2930a17778b96d86bc174a7922477e43f77a1316fccd0a.jpg)



![](images/3b36dc8a8b9419edb63c5796a6c0ca377be0b06e4aeecb9885dd1d2325d01c89.jpg)



(b)   
Fig. 10. Percent of Shared Workers among Different Algorithms $( m = 3 0 0 )$ (a) B = 300. (b) B = 500.

This is intuitive that, with more budgets, the system can select and recruit more workers to provide a larger coverage value. Fig. 8b depicts the coverage performance comparison among different algorithms. It can be seen that the proposed VBC-GA and VBC-Greedy have similar results, which are around 20% better than the coverage of Q-Greedy with different budgets. At the same time, the coverage values of the proposed algorithms are slightly smaller (around 5%) than that of C-Greedy.

Fig. 9a shows the performance trends considering the query task reliability. Given a fixed number of query tasks, all compared algorithms are able to improve the task reliability values when more budgets are provided. The detailed comparison among different algorithms is shown in Fig. 9b. Again, the proposed VBC-GA and VBC-Greedy achieve similar results. The proposed algorithms have marked advantages than C-Greedy, with increment ratio ranging from around 40% to 20%. It can be seen that the ratio decreases with the increment of budgets. The reason is that, when the budget is small, the proposed algorithms achieve the reliability of more than 0.85 and C-Greedy has a value around 0.6. Thus the room for improvement is much smaller for the proposed algorithms compared to C-Greedy. On the other hand, the proposed algorithms obtain smaller reliability values than than that of Q-Greedy. The ratios exhibit an decreasing trend from around 5% to 2%, which indicate that with more budgets, the proposed algorithms have larger performance increment than Q-Greedy with respect to the query reliability. The percent of shared workers among different algorithms (Fig. 10) also indicates the performance differences demonstrated above.

To summarize, the proposed algorithms achieve more competitive and balanced performance considering both optimization objectives with different budgets compared with C-Greedy and Q-Greedy.

# VII. CONCLUSION

In this paper, we propose the problem of recruiting workers for vehicle-based bi-objective crowdsourcing (VBC), which matches workers to a location-based query task and an automatic sensing task simultaneously, such that the sensing capability of each worker is maximized and the recruiter’s utility is optimized. We prove that the VBC problem is NP-hard, and thus we design two approximation algorithms based on the greedy strategy and genetic algorithm to find the solutions. Extensive experiments have been conducted based on a realworld traffic dataset. The results confirm the superiority of our proposed algorithms compared with existing algorithms considering the query task completion quality and sensing area maximization.

# APPENDIX

# A. Proof of Lemma 1

Proof: A submodular maximization problem with cardinality constraints (SMCC) is NP-hard [44], and can be described as follows: Given a ground set $\begin{array} { r l } { U } & { { } = } \end{array}$ $\{ u _ { 1 } , u _ { 2 } , \dotsc , u _ { | U | } \}$ , a monotone submodular function f defined on U, and a cardinality value K . The objective is to maximize f (U  ), where $U ^ { \prime } \subseteq U$ , and $| U ^ { \prime } | \leq K$ . We prove the lemma by reducing the SMCC problem to an instance of VBC problem. Specifically, we consider that there is only one query task, for which all available workers travel through the position of this query task. In this case, each selected worker will be assigned to this query task. We assume that each worker holds the same confidence and the unit cost for participation. Therefore, the objective of this VBC instance is equivalent to maximizing the joint trajectory coverage of the selected workers given the recruitment budget, i.e., max $s { \subseteq } W G ( S )$ s.t. $\sum _ { w _ { i } \in S } c _ { j } \ \le \ B$ . We then show that G(S) is a monotone submodular function by definition. For any $S _ { 1 } \subseteq S _ { 2 } \subseteq W$ and $w \in \boldsymbol { W } \backslash S _ { 2 }$ , we have $\cup _ { w _ { j _ { 1 } } \in S _ { 1 } } R _ { j _ { 1 } } \subseteq \cup _ { w _ { j _ { 2 } } \in S _ { 2 } } R _ { j _ { 2 } }$ by the definition of the worker trajectory. Therefore,

$$
G (S _ {2} \cup \{w \}) - G (S _ {2}) = | \cup_ {w _ {j _ {2}} \in \{S _ {2} \cup \{w \} \}} R _ {j _ {2}} | - | \cup_ {w _ {j _ {2}} \in S _ {2}} R _ {j _ {2}} |
$$

$$
\leq | \cup_ {w _ {j _ {1}} \in \{S _ {1} \cup \{w \} \}} R _ {j _ {1}} | - | \cup_ {w _ {j _ {1}} \in S _ {1}} R _ {j _ {1}} |
$$

$$
= G (S _ {1} \cup \{w \}) - G (S _ {1}).
$$

The inequality here comes from the basic property of set operations, i.e., adding elements to a set A results in a smaller or equal cardinality increment than adding the same elements to a subset $A ^ { \prime } \subseteq A .$ . In addition, we can see that $G ( S _ { 2 } \cup \{ w \} ) -$ $G ( S _ { 2 } ) \geq 0 .$ It completes the proof that the sensing coverage function G(S) is a monotone submodular function. The results of solving the SMCC problem (by mapping G to f , W to U , and B to K ) are also the results of the above VBC instance, which conpletes our proof.

# B. Proof of Lemma 2

Proof: Given a query task ti and its assigned worker set Wi , for a new worker $w _ { k }$ added to Wi ,

we have:

$$
\begin{array}{l} F _ {t _ {i}} (W _ {i} \cup \{w _ {k} \}) - F _ {t _ {i}} (W _ {i}) \\ = 1 - \prod_ {w _ {j} \in W _ {i} \cup \{w _ {k} \}} (1 - p _ {j}) - (1 - \prod_ {w _ {j} \in W _ {i}} (1 - p _ {j})) \\ = \prod_ {w _ {j} \in W _ {i}} (1 - p _ {j}) \cdot (1 - (1 - p _ {k})) \\ = \prod_ {w _ {j} \in W _ {i}} (1 - p _ {j}) \cdot p _ {k} \\ \geq 0, \\ \end{array}
$$

which completes our proof.

# REFERENCES

[1] G. Chatzimilioudis, A. Konstantinidis, C. Laoudias, and D. Zeinalipour-Yazti, “Crowdsourcing with smartphones,” IEEE Internet Comput., vol. 16, no. 5, pp. 36–44, Sep. 2012.   
[2] P. Mohan, V. Padmanabhan, and R. Ramjee, “Nericell: Rich monitoring of road and traffic conditions using mobile smartphones,” in Proc. ACM Int. Conf. Embedded Netw. Sensor Syst. (SenSys), 2008, pp. 323–336.   
[3] Y. Wang, X. Liu, H. Wei, G. Forman, C. Chen, and Y. Zhu, “CrowdAtlas: Self-updating maps for cloud and personal use,” in Proc. ACM Int. Conf. Mobile Syst., Appl., Services (MobiSys), 2013, pp. 27–40.   
[4] W. Sun, Q. Li, and C.-K. Tham, “Wireless deployed and participatory sensing system for environmental monitoring,” in Proc. IEEE Int. Conf. Sens., Commun., Netw. (SECON), Jun./Jul. 2014, pp. 158–160.   
[5] F. Calabrese, M. Colonna, P. Lovisolo, D. Parata, and C. Ratti, “Realtime urban monitoring using cell phones: A case study in Rome,” IEEE Trans. Intell. Transp. Syst., vol. 12, no. 1, pp. 141–151, Mar. 2011.   
[6] B. Hoh, T. Yan, D. Ganesan, K. Tracton, T. Iwuchukwu, and J.-S. Lee, “TruCentive: A game-theoretic incentive platform for trustworthy mobile crowdsourcing parking services,” in Proc. IEEE Int. Conf. Intell. Transp. Syst. (ITSC), Sep. 2012, pp. 160–166.   
[7] D. Wu, Y. Zhang, L. Bao, and A. C. Regan, “Location-based crowdsourcing for vehicular communication in hybrid networks,” IEEE Trans. Intell. Transp. Syst., vol. 14, no. 2, pp. 837–846, Jun. 2013.   
[8] X. Zhang et al., “Incentives for mobile crowd sensing: A survey,” IEEE Commun. Surveys Tuts., vol. 18, no. 1, pp. 54–67, 1st Quart., 2016.   
[9] X. Zhang, Z. Yang, Z. Zhou, H. Cai, L. Chen, and X. Li, “Free market of crowdsourcing: Incentive mechanism design for mobile sensing,” IEEE Trans. Parallel Distrib. Syst., vol. 25, no. 12, pp. 3190–3200, Dec. 2014.   
[10] J. Huang and H.-S. Tan, “Vehicle future trajectory prediction with a DGPS/INS-based positioning system,” in Proc. Amer. Control Conf., Jun. 2006, p. 6.   
[11] H. Jeung, M. L. Yiu, X. Zhou, and C. S. Jensen, “Path prediction and predictive range querying in road network databases,” Int. J. Very Large Data Bases, vol. 19, no. 4, pp. 585–602, 2010.   
[12] P. N. Pathirana, A. V. Savkin, and S. Jha, “Location estimation and trajectory prediction for cellular networks with mobile base stations,” IEEE Trans. Veh. Technol., vol. 53, no. 6, pp. 1903–1913, Nov. 2004.   
[13] X. Li, M. Li, Y.-J. Gong, X.-L. Zhang, and J. Yin, “T-DesP: Destination prediction based on big trajectory data,” IEEE Trans. Intell. Transp. Syst., vol. 17, no. 8, pp. 2344–2354, Aug. 2016.   
[14] L. Kazemi and C. Shahabi, “GeoCrowd: Enabling query answering with spatial crowdsourcing,” in Proc. ACM Int. Conf. Adv. Geograph. Inf. Syst. (GIS), 2012, pp. 189–198.   
[15] S. He, D.-H. Shin, J. Zhang, and J. Chen, “Toward optimal allocation of location dependent tasks in crowdsensing,” in Proc. IEEE Int. Conf. Comput. Commun. (INFOCOM), Apr./May 2014, pp. 745–753.   
[16] Y. Liu, B. Guo, Y. Wang, W. Wu, Z. Yu, and D. Zhang, “TaskMe: Multitask allocation in mobile crowd sensing,” in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput., 2016, pp. 403–414.   
[17] S. Reddy, D. Estrin, and M. Srivastava, “Recruitment framework for participatory sensing data collections,” in Pervasive Computing. Berlin, Germany: Springer, 2010, pp. 138–155.   
[18] L. Kazemi, C. Shahabi, and L. Chen, “GeoTruCrowd: Trustworthy query answering with spatial crowdsourcing,” in Proc. ACM SIGSPATIAL Int. Conf. Adv. Geograph. Inf. Syst. (GIS), 2013, pp. 314–323.   
[19] X. Zhang, Z. Yang, Y. Liu, and S. Tang, “On reliable task assignment for spatial crowdsourcing,” IEEE Trans. Emerg. Topics Comput., to be published, doi: 10.1109/TETC.2016.2614383.

[20] P. Cheng et al., “Reliable diversity-based spatial crowdsourcing by moving workers,” in Proc. VLDB Endowment, 2015, vol. 8. no. 10, pp. 1022–1033.   
[21] B. Guo, H. Chen, Q. Han, Z. Yu, D. Zhang, and Y. Wang, “Workercontributed data utility measurement for visual crowdsensing systems,” IEEE Trans. Mobile Comput., vol. 16, no. 8, pp. 2379–2391, Aug. 2017.   
[22] B. Guo, Y. Liu, W. Wu, Z. Yu, and Q. Han, “ActiveCrowd: A framework for optimized multitask allocation in mobile crowdsensing systems,” IEEE Trans. Human–Mach. Syst., vol. 47, no. 3, pp. 392–403, Jun. 2016.   
[23] X. Zhang, Z. Yang, Y. Liu, J. Li, and Z. Ming, “Toward efficient mechanisms for mobile crowdsensing,” IEEE Trans. Veh. Technol., vol. 66, no. 2, pp. 1760–1771, Feb. 2017.   
[24] Y. Tong, J. She, B. Ding, L. Wang, and L. Chen, “Online mobile microtask allocation in spatial crowdsourcing,” in Proc. IEEE 32nd Int. Conf. Data Eng. (ICDE), May 2016, pp. 49–60.   
[25] M. Xiao, J. Wu, L. Huang, Y. Wang, and C. Liu, “Multi-task assignment for crowdsensing in mobile social networks,” in Proc. IEEE Int. Conf. Comput. Commun. (INFOCOM), Apr./May 2015, pp. 2227–2235.   
[26] D. Zhang, H. Xiong, L. Wang, and G. Chen, “Crowdrecruiter: Selecting participants for piggyback crowdsensing under probabilistic coverage constraint,” in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput. (Ubicomp), 2014, pp. 703–714.   
[27] H. Xiong, D. Zhang, G. Chen, L. Wang, V. Gauthier, and L. E. Barnes, “iCrowd: Near-optimal task allocation for piggyback crowdsensing,” IEEE Trans. Mobile Comput., vol. 15, no. 8, pp. 2010–2022, Aug. 2015.   
[28] X. Zhang, Z. Yang, Y.-J. Gong, Y. Liu, and S. Tang, “SpatialRecruiter: Maximizing sensing coverage in selecting workers for spatial crowdsourcing,” IEEE Trans. Veh. Technol., vol. 66, no. 6, pp. 5229–5240, Jun. 2017.   
[29] A. Ahmed, K. Yasumoto, Y. Yamauchi, and M. Ito, “Distance and time based node selection for probabilistic coverage in people-centric sensing,” in Proc. IEEE Commun. Soc. Conf. Sensor, Mesh Ad Hoc Commun. Netw. (SECON), Jun. 2011, pp. 134–142.   
[30] S. Hachem, A. Pathak, and V. Issarny, “Probabilistic registration for large-scale mobile participatory sensing,” in Proc. IEEE Int. Conf. Pervasive Comput. Commun. (PerCom), Mar. 2013, pp. 132–140.   
[31] L. Wang et al., “CCS-TA: Quality-guaranteed online task allocation in compressive crowdsensing,” in Proc. ACM Int. Joint Conf. Pervasive Ubiquitous Comput., 2015, pp. 683–694.   
[32] Z. He, J. Cao, and X. Liu, “High quality participant recruitment in vehicle-based crowdsourcing using predictable mobility,” in Proc. IEEE Int. Conf. Comput. Commun. (INFOCOM), Apr./May 2015, pp. 2542–2550.   
[33] Mobile Millennium. Accessed: Mar. 20, 2017. [Online]. Available: http://traffic.berkeley.edu/   
[34] B. Hull et al., “CarTel: A distributed mobile sensor computing system,” in Proc. ACM Int. Conf. Embedded Netw. Sensor Syst. (SenSys), 2006, pp. 125–138.   
[35] Z. Yu, H. Xu, Z. Yang, and B. Guo, “Personalized travel package with multi-point-of-interest recommendation based on crowdsourced user footprints,” IEEE Trans. Human–Mach. Syst., vol. 46, no. 1, pp. 151–158, Feb. 2016.   
[36] F. Saremi et al., “Experiences with GreenGPS—Fuel-efficient navigation using participatory sensing,” IEEE Trans. Mobile Comput., vol. 15, no. 3, pp. 672–689, Mar. 2016.   
[37] C.-J. Ho and J. W. Vaughan, “Online task assignment in crowdsourcing markets,” in Proc. AAAI, 2012, pp. 45–51.   
[38] C.-J. Ho, S. Jabbari, and J. W. Vaughan, “Adaptive task assignment for crowdsourced classification,” in Proc. ICML, 2013, pp. 534–542.   
[39] M. L. Yiu and N. Mamoulis, “Efficient processing of top-κ dominating queries on multi-dimensional data,” in Proc. 33rd Int. Conf. Very Large Data Bases (VLDB), 2007, pp. 483–494.   
[40] K. Deb, A. Pratap, S. Agarwal, and T. Meyarivan, “A fast and elitist multiobjective genetic algorithm: NSGA-II,” IEEE Trans. Evol. Comput., vol. 6, no. 2, pp. 182–197, Apr. 2002.   
[41] J. Yuan, Y. Zheng, X. Xie, and G. Sun, “Driving with knowledge from the physical world,” in Proc. ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining (KDD), 2011, pp. 316–324.   
[42] J. Yuan et al., “T-drive: Driving directions based on taxi trajectories,” in Proc. ACM SIGSPATIAL Int. Conf. Adv. Geograph. Inf. Syst. (GIS), 2010, pp. 99–108.   
[43] P. Newson and J. Krumm, “Hidden Markov map matching through noise and sparseness,” in Proc. ACM SIGSPATIAL Int. Conf. Adv. Geograph. Inf. Syst. (GIS), 2009, pp. 336–343.   
[44] G. L. Nemhauser, L. A. Wolsey, and M. L. Fisher, “An analysis of approximations for maximizing submodular set functions—I,” Math. Programm., vol. 14, no. 1, pp. 265–294, 1978.