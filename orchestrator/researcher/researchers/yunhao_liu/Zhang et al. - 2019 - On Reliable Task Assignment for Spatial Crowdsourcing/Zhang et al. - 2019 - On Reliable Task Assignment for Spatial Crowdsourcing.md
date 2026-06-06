# On Reliable Task Assignment for Spatial Crowdsourcing

Xinglin Zhang, Member, IEEE, Zheng Yang, Member, IEEE, Yunhao Liu, Fellow, IEEE, and Shaohua Tang, Member, IEEE

Abstract—The large quantity of mobile devices equipped with various built-in sensors and the easy access to the high-speed wireless networks have made spatial crowdsourcing receive much attention in the research community recently. Generally, the objective of spatial crowdsourcing is to outsource location-based sensing tasks (e.g., traffic monitoring and pollution monitoring) to ordinary mobile workers (e.g., users carrying smartphones) efficiently. In this paper, we study a reliable task assignment problem for spatial crowdsourcing in a large worker market. Specifically, we use worker confidence to represent the reliability of successfully completing the assigned sensing tasks, and we formulate two optimization problems, maximum reliability assignment (MRA) under a recruitment budget and minimum cost assignment (MCA) under a task reliability requirement. We reveal the special structure properties of these problems, based on which we design effective approaches to assign tasks to the most suitable workers. The performances of the proposed algorithms are verified by theoretic analysis and experimental results on both real and synthetic datasets.

Keywords—Spatial Crowdsourcing, Task Assignment, Reliability, Budget, Minimum Cost

# I. INTRODUCTION

The proliferation of mobile devices equipped with built-in sensors and the ubiquity of high-speed wireless networks have enabled a promising distributed problem solving paradigm, spatial crowdsourcing [1], in which ordinary mobile users are requested to perform location-based sensing tasks, such as traffic monitoring [2], [3], pollution monitoring [4], and geographical data generation [5]. With the large volume and various types of data (e.g., location, time, picture, audio, and video) that can be collected from spatial crowdsourcing, more and more sensing applications that can greatly benefit people’s life are going to be developed in both the academic and industrial communities.

Generally, a spatial crowdsourcing system consists of three characters: task requester, spatial crowdsourcing server (SCserver), and mobile worker. Task requesters and workers first

register with the SC-server. Then task requesters can outsource sensing tasks to the SC-server, which subsequently determines the task assignment to workers according to certain predefined criteria. Finally, workers complete the assigned tasks by physically travelling to the specified locations of interest and send the results back to requesters through the SC-server.

The goal of spatial crowdsourcing is to achieve high social efficiency by matching tasks and workers effectively. The evaluation metrics vary with the task assignment models. Most existing work deal with the situation that the number of tasks and workers are comparable, and the proposed methods strive to maximize the number of successful assignments, given the reliability of assigned tasks and the spatial-temporal constraints, such as worker travelling distance and task expiration time [1], [6]–[8]. In this paper, we study the task assignment for spatial crowdsourcing in a large worker market, i.e., the number of workers is sufficiently large that a subset of workers are sufficient for completing sensing tasks. As an example, in road condition detection (e.g., reporting potholes on the road), the number of vehicles and passengers (i.e. workers) is more than enough for the road segments of interest. Another example comes from an emergency response scenario, where the requester (e.g., Red Cross) intends to collect pictures or videos of specific damaged locations. The available workers in the vicinity are usually abundant and a subset of them can complete the tasks.

Under the aforementioned realistic scenario, we propose the task-and-worker assignment by considering the measurement of reliability. The intuition is that answers provided by workers are sometimes incorrect (e.g., the uploaded photos/videos might be fake), or workers may fail to complete the tasks before task expiration time. Thus, we will take into account the confidence of workers, and define the reliability of each sensing task as the confidence that at least one worker assigned to this task can give correct answers. Workers are assumed to have preferences over the sensing tasks broadcasted by the SCserver. For example, some workers might only accept tasks that are within the predefined walking distance, while others might accept tasks on the way to their destinations (e.g., home).

The assignment frameworks we present here are designed for two main objectives: maximizing the reliability of the assigned tasks under a recruitment budget given by requesters, and minimizing the number of assigned workers for a given reliability requirement of the assigned tasks. We formulate the problems by constructing bipartite graphs between tasks and workers, and then investigate the structure properties of the formulations, based on which we propose effective algorithms

with theoretical guarantees.

To summarize, the main contributions of this work are as follows:

We propose a reliable task assignment problem, which guarantees the quality of sensing tasks, for spatial crowdsourcing systems with large worker markets.   
We investigate the structure properties of the proposed problems, based on which we propose effective algorithms with theoretical guarantees.   
We conduct extensive experiments on both synthetic and real datasets and show the effectiveness of the proposed methods.

The rest of the paper is organized as follows. Section II presents the related work. The problem definitions are given in Section III. Then we discuss the solutions for the two assignment objectives in Section IV and V, respectively. The experimental results are illustrated in Section VI and finally the conclusion is drawn in Section VII.

# II. RELATED WORK

# A. Spatial Crowdsourcing

Spatial crowdsourcing is closely related to participatory sensing [9], which aims at exploiting mobile users to actively collect and report data by using their mobile devices equipped with various sensors for a given campaign. Participatory sensing is mostly application oriented. The Mobile Millennium project [10] employs mobile phones to collect and upload traffic information to a server in real time. Based on the reported traffic data, the server then builds prediction models for the future traffic condition. With the same spirit, researchers designed CalTel [11] and Nericell [12] to pool information about traffic and road conditions by leveraging smartphones and mobile sensors mounted on vehicles. DroneSense [13] is an environmental monitoring system that integrates traditional wireless sensor networks and participating users with smartphones. GreenGPS [14] offers a navigation service that allows drivers to follow the most fuel-efficient routes customized for their vehicles between arbitrary end-points by leveraging sparse sensed data. GreenGPS is not only fuel-efficient, but also economic and easy to deploy.

Spatial crowdsourcing [1] generalizes the aforementioned participatory sensing applications by using a general management framework. In spatial crowdsourcing, multiple campaigns can be processed efficiently and the goal is to assign tasks efficiently. Kazemi and Shahabi [1] proposed a maximum task assignment problem. They designed heuristic algorithms to maximize the number of assigned tasks for a given time interval. He et al. [15] modeled the travelling distance constraint and the task completion redundancy to ensure high efficiency when allocating location dependent tasks to mobile workers. In [6], Kazemi et al. explicitly considered modeling the worker quality, and designed efficient assignment protocols to pursue high completion quality of assigned tasks. Reddy et al. [16] developed a recruitment framework that can identify wellsuited participants based on their geographic and temporal availability as well as participation habits. Pournajaf et al. [17] studied the assignment scenario that workers are able to utilize spatial cloaking to obfuscate locations. To et al. [7] tried to obtain multiple objectives, i.e., minimizing the travelling distance of a worker, maximizing task assignment success rate, and protecting worker location privacy, by designing a task assignment scheme. Cheng et al. [8] considered reliability and spatial-temporal diversity of the tasks that rely on multiple observation angles. The common assumption of these work is that the numbers of tasks and workers are comparable, and the frugality of assignment is not incorporated. In this paper, we study the application scenario with a large worker market, for which we accommodate the assignment efficiency and frugality.

The frameworks discussed above concern the overall assignment efficiency. Another direction is to maximize a single worker’s utility. Deng et al. [18] considered workers’ perspectives for task selection, and designed a method to maximize the total number of a worker’s selected tasks under the travelling budget.

# B. Crowdsensing

Spatial crowdsourcing is also related to crowdsensing [19]– [21] that emphasizes on using the built-in sensors of mobile devices to continuously collect sensed data in the background. Pioneer crowdsensing applications include LiFS [22] and TrM-CD [23] for indoor localization, FlierMeet [24] for Cross-Space Public Information Reposting, Tagging, and Sharing, and SmartTrace [25] for 3G/WiFi discovery. The fundamental objective of such applications is to select a set of workers that can cover a large spatial area in the region of interest. In [26], Cardone et al. proposed a Mobile Crowdsensing platform, where a simple participant selection mechanism is adopted to maximize the sensing area coverage with a recruitment budget. Zhang et al. [27] and Xiong et al. [28] tried to satisfy sensing requirement by selecting as few workers as possible. Trajectory histories are used to evaluate the coverage potential of a worker. Differently, user mobilities are used by Ahmed et al. [29] and Hachem et al. [30] to select a minimal number of mobile users to meet the coverage requirement.

The above crowdsensing applications emphasize on the automatic sensing capability of smartphones, while spatial crowdsourcing studied in this work highlights people’s intellectual capability and mobility in completing location-based query tasks that are difficult for passive sensing with smartphones.

# C. Incentive Mechanisms

Incentive mechanisms offer ordinary workers benefits to compensate for their contribution of sensing effort. Jaimes et al. [31] considered the mechanism design based on user locations, the coverage, and the platform budget. Sun and Tham [32] proposed an information-driven incentive mechanism with consumer demand awareness. An information utility metric is adopted to measure the quality of a worker’s sensor information according to the consumer demand. The proposed mechanism can select and incentivize the most informative workers, which maximize the satisfaction of the consumers with fewer number of workers. Wen et al. [33] incorporated the sensing quality and workers’ willingness for participation in the mechanism. Recently, coverage functions with the property of submodularity are applied to construct efficient incentive mechanisms for user selection in crowdsensing [34]–[37]. These incentive methods are mostly designed for a single coverage application in passive sensing, hence they are different from the models in spatial crowdsourcing, where sensing tasks are of large quantity and efficient task assignment is required.

# D. Internet of Things

Spatial crowdsourcing is part of the emerging Internet of Things (IoT) networking architecture [38]. On one hand, the workers equipped with mobile devices in spatial crowdsourcing forms a powerful set of mobile sensors, which can not only collect various sensing data with the built-in sensors, but also connect with the traditional sensor networks deployed in the environment. In this way, spatial crowdsourcing enhance the Objects Layer and the sensing capability of the IoT [38]. On the other hand, Device-to-Device (D2D) communication in LTE-A networks [39], [40] is promising to facilitate the implementation of the task assignment for spatial crowdsourcing. As an example, a worker can deliver the sensed data to nearby available workers through D2D communication if s/he cannot transmit the data through cellular networks [41], [42]. This alternative transmission can help improve the task completion rate, and in consequence, improve the quality of experience and service for spatial crowdsourcing.

# III. PROBLEM DEFINITION

In this paper, we study the case that a spatial task is associated with a specific location and a valid time duration. For example, in order to monitor the air quality condition at a specified location L, we construct sensing tasks in the form of “please report the air quality condition at the location L at nine o’clock”. The location and time resolution here is application dependent and can be varied. A worker’s report beyond the specified location and time is considered invalid. The formal definitions of a spatial task and a worker are given in the following.

Definition 1 (Spatial task) A spatial task j of form $( l _ { j } , q _ { j } , s _ { j } , e _ { j } )$ is a sensing query $q _ { j }$ to be answered at location $l _ { j }$ between the valid time interval $[ s _ { j } , e _ { j } ]$ .

It indicates from the definition that, the sensing query qj $q _ { j }$ of a spatial task $j$ can be answered by a mobile worker only if s/he travels physically to the location $l _ { j }$ in the given time interval, where a worker is defined as:

Definition 2 (Worker) A worker i is a registered mobile user in the SC-server, who is currently located at position $l _ { i } ,$ and has requested to perform a spatial task by setting the task preference prefi. Each worker i is associated with a confidence $p _ { i , j } $ , which indicates the reliability of the worker i to complete the assigned task $j .$ .

Note that a worker i may want to do spatial tasks on the way to some destinations, or perform spatial tasks that are located within a walking distance from the current location of

![](images/e7697e8d226f0de6b40fefc3a46352a0ce9a4615d86ca0a85e18a2912fb012ad.jpg)



Fig. 1. An example of the set notations. The ground set $E = \{ ( i _ { 1 } , j _ { 1 } )$ , $( \bar { i _ { 2 } } , \bar { j _ { 1 } } ) , ( \bar { i _ { 3 } } , \bar { j _ { 2 } } ) , ( \bar { i _ { 5 } } , \bar { j _ { 1 } } ) \}$ . Define $A = \{ ( i _ { 1 } , j _ { 1 } ) , ( i _ { 3 } , j _ { 2 } ) , ( i _ { 5 } , j _ { 1 } ) \} ,$ , then $A _ { n } ~ = ~ \{ i _ { 1 } , i _ { 3 } , i _ { 5 } \} , ~ A _ { m } ~ = ~ \{ j _ { 1 } , j _ { 2 } \} , ~ A _ { n } ^ { j _ { 1 } } ~ = ~ \{ i _ { 1 } , i _ { 5 } \} , ~ A _ { n } ^ { j _ { 2 } } ~ = ~ \{ i _ { 3 } \}$ , $A _ { m } ^ { i _ { 1 } } \ = \ \{ j _ { 1 } \} , \ A _ { m } ^ { i _ { 3 } } \ = \ \{ j _ { 2 } \} , \ A _ { m } ^ { i _ { 5 } } \ = \ \{ j _ { 1 } \}$ . Given $t b \ = \ 2$ , then $A ^ { \prime } =$ $\{ ( i _ { 1 } , j _ { 1 } ) , ( i _ { 3 } , j _ { 2 } ) \}$ is a legitimate assignment.

the worker. The worker designates such preference $p r e f _ { i }$ to the SC-server, such that s/he will only be assigned tasks that are possible to be completed.

AAThe SC-server processes spatial tasks in a periodical fashion (e.g., two-hour cycles from 08:00 to 20:00 per day). At the beginning of each period, the SC-server pools the valid tasks and available workers, and assign tasks to appropriate workers. We assume that each worker can be assigned with one task in each period and s/he can participate in multiple periods [1]. After being assigned with a spatial task j, a worker i sometimes may be unable to answer the query correctly (e.g. taking a wrong photo). Thus, each worker i is associated with a confidence $p _ { i , j }$ , which is the reliability (or skill) that the worker i can successfully complete the task j. The confidence of a worker can be inferred from historical data of performing tasks [43], [44]. As learning worker confidence is not the focus of this paper, we assume that the system has acquired the confidence values before assigning tasks.

With the definitions of spatial tasks and workers, we are ready to present our reliable spatial task assignment problems. The reliability of a spatial task indicates the confidence that at least some workers assigned to this task can successfully finish the task. Intuitively, assigning more workers to a task will lead to higher reliability, which in turn will result in great confidence of completing the task successfully in a large worker market. However, workers usually require compensations, or incentives, to perform tasks. Even in self-motivated scenarios, assigning too many workers to a task also leads to a waste of social energy. Therefore, we take into account the frugality in modeling the assignment problems we adopt a uniform cost model, where the payment for each task/worker is fixed and is typically specified by the task requester. One example adopting this payment model is the popular crowdsourcing platform Amazon’s Mechanical Turk. Under this model, researchers have treated workers equally expensive and studied efficient task assignment schemes without budgets [6], [8] and with budgets [43], [44] (where budgets are the total number of recruited workers). Under this model, we aim to maximize the overall task reliability for assigned tasks under the budget constraint, and minimize the number of assigned workers under the reliability requirement. The two problems are defined as follows.

# Definition 3 (Maximum reliability assignment (MRA))

Given a total recruitment budget tb of the SC-server and the confidence $p _ { i , j }$ for each worker i and task $j ,$ the maximum reliability assignment (MRA) problem is to maximize the overall expected task reliability by assigning tasks to workers under the budget constraint.

Definition 4 (Minimum cost assignment (MCA)) Given a completion reliability threshold ϵ for each task and the confidence $p _ { i , j }$ for each worker i and task $j ,$ the minimum cost assignment (MCA) problem is to minimize the number of assigned workers under the constraint that each task achieves a completion reliability of at least ϵ.

# IV. RELIABILITY MAXIMIZATION

In this section, we formulate the MRA problem from the perspective of set function optimization. Define a set element in the form of an ordered worker-task pair $( i , j )$ , which represents that the task j is in the preference set of the worker i. The ground set E is the set of all possible elements, i.e., $E = \{ ( \breve { i } , j ) | i \in [ n ] , j \in [ m ] \}$ , where $[ n ]$ and $[ m ]$ represent the worker set of size n and the task set of size m, respectively. Given a set $A \subseteq E ,$ we construct a set function

$$
f (A) = \sum_ {j \in A _ {m}} (1 - \prod_ {i \in A _ {n} ^ {j}} (1 - p _ {i, j})), \tag {1}
$$

where $A _ { n }$ and $A _ { m }$ represent the worker and task dimensions in $A , \mathrm { i . e . , } A _ { n } = \{ i | ( i , j ) \in A \}$ and $A _ { m } = \{ j | ( i , j ) \in A \}$ . We use $A _ { n } ^ { j }$ to represent the set of workers that can be assigned to the task j in $A _ { n }$ . It can be induced that $\textstyle \prod _ { i \in A _ { n } ^ { j } } ( 1 - { \overline { { p } } } _ { i , j } )$ is the probability that all the assigned workers for the task j cannot finish the task $j .$ Thus, the term $\begin{array} { r } { 1 - \prod _ { i \in A _ { n } ^ { j } } \left( 1 - p _ { i , j } \right) } \end{array}$ is the probability that the task $j$ ∈ ncan be successfully performed by at least one assigned worker. Then the function $f ( \cdot )$ is the reliability metric that we would like to maximize for the overall assignment. As the SC-server has a recruitment budget tb and each user can accomplish one task at a time, a legitimate assignment A must satisfy that $| A | \leq t b ,$ and $| A _ { m } ^ { i } | \leq 1 , \forall i \in$ $A _ { n } ,$ where $A _ { m } ^ { i }$ represents the set of tasks assigned to worker i. Fig. 1 is an example illustrating the set notations and a legitimate assignment.

By constructing the above terms, the MRA problem is equivalent to solving the following constrained optimization problem:

$$
\left| A _ {m} ^ {i} \right| \leq 1, \forall i \in A _ {n}.
$$

To solve the problem, we propose a greedy strategy to select the most valuable element in an iterative manner. Note that the objective function $f ( \cdot )$ is decomposable with respect to the summation of the terms of task reliability, i.e., adding an element $( i ^ { \prime } , j ^ { \prime } )$ only influences the reliability of task $j ^ { \prime } .$ With this observation, we can simplify the computation process of finding the element with the largest marginal increment value. Specifically, given a worker i′, we calculate the marginal increment value by matching it to a task $j ^ { \prime }$ :

Algorithm 1 Greedy MRA (G-MRA)   
1: $A \leftarrow \emptyset, A_n \leftarrow \emptyset;$ 2: $\pi_j \leftarrow 1, \forall j \in [m];$ 3: for idx = 1 to tb do
4:    for $j \in [m]$ do
5: $\sigma_j \leftarrow \max_{i \in [n] \setminus A_n} p_{i,j} \cdot \pi_j;$ 6:    end for
7: $j^* \leftarrow \arg \max_{j \in [m]} \sigma_j;$ 8: $A \leftarrow A \cup \{(i(\sigma_{j^*}), j^*)\}$ 9: $A_n \leftarrow A_n \cup \{i(\sigma_{j^*})\};$ 10: $\pi_{j^*} \leftarrow \pi_{j^*} \cdot (1 - p_{i(\sigma_{j^*}), j^*});$ 11: end for

$$
\begin{array}{l} f (A \cup \{(i ^ {\prime}, j ^ {\prime}) \}) - f (A) \\ = \left(1 - \prod_ {i \in A _ {n} ^ {j ^ {\prime}}} \left(1 - p _ {i, j ^ {\prime}}\right) \cdot \left(1 - p _ {i ^ {\prime}, j ^ {\prime}}\right)\right) - \left(1 - \prod_ {i \in A _ {n} ^ {j ^ {\prime}}} \left(1 - p _ {i, j ^ {\prime}}\right)\right) \\ = \prod_ {i \in A _ {n} ^ {j ^ {\prime}}} (1 - p _ {i, j ^ {\prime}}) \cdot p _ {i ^ {\prime}, j ^ {\prime}}. \\ \end{array}
$$

After calculating all legitimate marginal increment values, the task with the largest marginal increment value will be taken as a candidate for real assignment.

Algorithm 1 sketches the procedure of the proposed greedy strategy. Lines 4–6 compute the largest marginal increment value for each task $j .$ . Note that $\begin{array} { r } { \pi _ { j } = \prod _ { i \in A _ { n } ^ { j } } \left( 1 - p _ { i , j } \right) } \end{array}$ , where $A _ { n } ^ { j }$ is the set of workers that have been assigned to task $j$ in the previous steps. In the current step, $\sigma _ { j }$ is the maximum marginal increment value for the task $j .$ . We use $i ( \sigma _ { j } )$ to record the corresponding matched worker. In line 7, the algorithm returns the task $j ^ { * }$ with the largest marginal value with respect to all available tasks. Lines 8–10 update the selected workertask pair set A and the corresponding worker set $A _ { n }$ , as well as the probability product term. Considering the time complexity of Algorithm 1, the inner loop (lines 4–6) takes time $O \bar { ( } m \cdot n \bar { ) }$ . Line $\bar { 7 }$ has time complexity of $O ( m )$ . The remaining operations inside the outer loop have constant time complexity. Therefore, the time complexity of Algorithm 1 is $O ( t { \bar { b } } \cdot m \cdot n )$ .

To analyze the performance of the proposed algorithm, we resort to the theory of submodular functions. We first prove the following lemma regarding the objective function f(·).

Lemma 1 The set function $f ( \cdot )$ defined in Eq. (1) is monotone submodular.

Proof: We prove the lemma by using the definition of submodular functions.

Definition 5 (Submodular function) Given a ground set E, a function $g : 2 ^ { \Omega } \to \mathbb { R }$ is submodular if for any $X \subseteq Y \subseteq \Omega$ , and $e \in \Omega \backslash Y _ { \mathrm { ~ : ~ } }$ , we have

$$
g (X \cup \{e \}) - g (X) \geq g (Y \cup \{e \}) - g (Y),
$$

and $g$ is monotone $i f g ( X ) \leq f ( Y )$ .

Given $A \subseteq B \subseteq E$ and a new worker-task pair $( i ^ { \prime } , j ^ { \prime } ) \in$ $E \backslash B$ , we certify the inequality given by the definition in three

![](images/8ad9393dd76c553dda41ac40a32869a4802bbcd1752e167f6080bb4bac736c41.jpg)  
Fig. 2. The relation between the new element and the sets.

cases:

$j ^ { \prime } \notin B _ { m }$ . In this case, there are three possibilities of the new worker element $\overline { { i ^ { \prime } } }$ with respect to the worker sets $A _ { n }$ and $B _ { n }$ (Fig. 2a-2c). As can be seen in all the three subcases, $j ^ { \prime }$ is a new task and has no matched workers in sets $B _ { n }$ and $A _ { n } ,$ therefore we can easily get

$$
f (B \cup \{(i ^ {\prime}, j ^ {\prime}) \}) - f (B) = 1 - (1 - p _ {i ^ {\prime}, j ^ {\prime}}) = p _ {i ^ {\prime}, j ^ {\prime}}
$$

$$
= f (A \cup \{(i ^ {\prime}, j ^ {\prime}) \}) - f (A).
$$

$j ^ { \prime } \in B _ { m }$ and $j ^ { \prime } \notin A _ { m }$ . There is only one option for i′ in this case (Fig. 2d) due to the constraint ${ \bar { A } } _ { n } \subseteq B _ { n }$ . Without loss of generality, we assume that task $j ^ { \prime }$ has one matched worker with the reliability p in $B _ { n }$ . Then we can compute the marginal increment as

$$
\begin{array}{l} f (B \cup \{(i ^ {\prime}, j ^ {\prime}) \}) - f (B) \\ = (1 - (1 - p) \left(1 - p _ {i ^ {\prime}, j ^ {\prime}}\right)) - (1 - (1 - p)) \tag {2} \\ = (1 - p) p _ {i ^ {\prime}, j ^ {\prime}} \leq p _ {i ^ {\prime}, j ^ {\prime}} \\ = f (A \cup \{(i ^ {\prime}, j ^ {\prime}) \}) - f (A). \\ \end{array}
$$

$j ^ { \prime } \in A _ { m }$ . As shown in Fig. 2e, $i ^ { \prime } \notin A _ { n }$ in this case. $\mathbf { A } \mathbf { s } { \textbf { } } A \subseteq B$ , the number of matched workers of task $j ^ { \prime }$ in $B _ { n }$ is at least as many as that in $A _ { n } .$ . Following the same computation process as the second case, we can conclude that $f ( B ^ { ' } \cup \{ ( i ^ { \prime } , j ^ { \prime } ) \} ) - f ( B ) \leq f ( A \cup$ $\{ ( i ^ { \prime } , j ^ { \prime } ) \} ) - f ( A )$ .

Next we show that f is also monotone. In fact, as $A \subseteq B$ , each task $j ^ { \prime } \in A _ { m }$ has more matched workers in $B _ { m }$ , i.e., $A _ { m } ^ { j ^ { \prime } } \subseteq B _ { m } ^ { j ^ { \prime } }$ . By the same computation process in Eq. (2), we can conclude that the reliability of $j ^ { \prime }$ for B is higher than the reliability for A. The final reliability is a summation of the reliability of each task, hence $f ( B ) \supseteq f ( A )$ .

The feasible solutions of the MRA problem has a special structural property which can be derived by using the matroid theory [45].

Definition 6 (Matroid) A matroid $M = \{ \Omega , \boldsymbol { \tau } \}$ is an ordered pair that consists of a finite set Ω and a non-empty collection

I of subsets of Ω satisfying the following conditions: (1) If $Y \in \mathcal { I }$ and ${ \dot { X } } \subseteq Y$ , then $X \ \in \ \mathbb { Z } ;$ (2) If X, $Y \in \mathcal { T }$ and $| X | < | Y |$ , then there exists an element $e \in Y \backslash X$ such that $\dot { X } \cup \{ e \} \in \mathcal { I }$ .

In the above definition, Ω is called the ground set of M. In the context of optimizing the function $f ( \cdot )$ , Ω is exactly the set $E = \{ ( i , j ) | i \in \mathbf { \bar { \Gamma } } [ n ] , j \in \mathbf { \bar { \Gamma } } [ m ] \}$ , which consists of all legitimate worker-task pairs, and I is the collection of all subsets of E, which indeed includes all possible assignments of maximizing unconstrained $f ( \cdot )$ .

The two constraints in the MRA problem shrink the solution space, which can be depicted by uniform and partition matroids.

Definition 7 (Uniform matroid) A matroid $M = \{ \Omega , \boldsymbol { \tau } \}$ is a uniform matroid if there exists some integer $k ,$ so that $\dot { X } \in \mathcal { I }$ if and only $i f \left| X \right| \leq k .$ .

Definition 8 (Partition matroid) A matroid $M = \{ \Omega , \boldsymbol { \tau } \}$ is a partition matroid if there exists a partition $Y _ { 1 } , Y _ { 2 } ,  { , } Y _ { K }$ of Ω, so that $X \in \mathcal { T } \mathrm { ~ } i f$ and only $i f | X | \overset { \cdot } { \cap } Y _ { k } | \leq 1 f o r$ all $k \in [ K ]$ .

According to these definitions, the constraint $| A | \leq t b$ in the MRA problem makes an assignment A lie in a uniform matroid. Let $B ^ { i } = \{ ( i , j ^ { \prime } ) | j ^ { \prime } \in \bar { E } _ { m } ^ { i } ) \} , \forall i \in E _ { n }$ , which is a partition of E, as $B ^ { i } \cap B ^ { i ^ { \prime } } = \varnothing , \forall i , i ^ { \prime } \in E _ { n }$ and $\cup _ { i \in E _ { n } } B ^ { i } = E$ . Then the constraint $A _ { m } ^ { i } \leq 1 , \forall i \in A _ { n }$ can be restated as $| A \cup$ $B ^ { i } | \leq 1 , \forall i \in E _ { n }$ . Therefore, the solution A is also restricted to a partition matroid. In brief, we connect the solution of the MRA problem and the matroid by the following lemma.

Lemma 2 The feasible solution space of the MRA problem constitutes an intersection of a uniform matroid and a partition matroid.

As algorithm 1 returns a greedy solution for the MRA problem, combined with the results of Lemmas 1–2 and Theorem 2.1 in [46], it can be readily derived that algorithm 1 returns a 3-approximation solution compared to the optimal solution.

Theorem 1 Algorithm 1 is a 3-approximation algorithm for the MRA problem.

Note: The above results can be easily generalized to the scenarios where spatial tasks have different weights. Specifically, assume that each task j is associated with a weight $w _ { j }$ , which reflects the utility of finishing the task j. Then the objective function in Eq. (1) can be rewritten as:

$$
f (A) = \sum_ {j \in A _ {m}} w _ {j} (1 - \prod_ {i \in A _ {n} ^ {j}} (1 - p _ {i, j})).
$$

The submodular property of this function is exactly the same as Eq. (1), hence the derivation and greedy heuristic in this section naturally apply to the weighted objective function.

# V. COST MINIMIZATION

By adopting the set notations as the MRA problem, we formulate the MCA problem as a constrained set cardinality minimization problem:

$\begin{array} { l l } { \mathrm { m i n i m i z e } _ { A \subseteq E } } & { \left| A \right| } \\ { \mathrm { s u b j e c t ~ t o } } & { 1 - \displaystyle \prod _ { i \in A _ { n } ^ { j } } ( 1 - p _ { i , j } ) \geq \epsilon , \forall j \in A _ { m } , } \end{array}$

$$
\left| A _ {m} ^ {i} \right| \leq 1, \forall i \in A _ {n}.
$$

We design a greedy algorithm based on the link between the formulated MCA problem and the monotone submodular function.

Theorem 2 The formulated MCA problem is reducible to the submodular coverage problem with a matroid constraint.

Proof: Consider a set of functions $f ^ { j } ( A ) \quad = \ 1 \ -$ $\textstyle \prod _ { i \in A _ { n } ^ { j } } ( 1 ^ { ^ { \cdot } } - \operatorname { \it { p } } _ { i , j } )$ . Define a truncated function $h ^ { j } ( A ) \ =$ ∈min $\{ \tilde { f } ^ { j } ( A ) , \epsilon \}$ , and let $\begin{array} { r } { h ( A ) ~ = ~ { \frac { 1 } { m } } \sum _ { j \in [ m ] } h ^ { j } ( A ) } \end{array}$ . A key observation is that:

$$
f ^ {j} (A) \geq \epsilon , \forall j \in [ m ] \Longleftrightarrow h (A) = \frac {1}{m} \sum_ {j \in [ m ]} h ^ {j} (A) = \epsilon . \tag {3}
$$

Following the same argument in the proof of Lemma 1, we can obtain:

Lemma 3 The functions $f ^ { j } ( \cdot ) , h ^ { j } ( \cdot )$ and $h ( \cdot )$ are monotone submodular for all $j \in [ m ]$ .

Therefore, the optimization problem

is equivalent to

which is a submodular coverage problem [47], [48]. We hence complete the proof by combining the inequalities $| A _ { m } ^ { i } | \leq$ 1, $\forall i \ \in \ A _ { n }$ , which have been shown to form a partition matroid in Lemma 2.

Algorithm 2 Greedy MCA (G-MCA)   
1: $A \leftarrow \emptyset, A_n \leftarrow \emptyset, B \leftarrow [m];$ 2: $\pi_j \leftarrow 1, f_j \leftarrow 0, \forall j \in [m];$ 3: while $B \neq \emptyset$ do
4:    for $j \in B$ do
5: $\sigma_j \leftarrow \min\{\epsilon - f_j, \max_{i \in [n] \setminus A_n} p_i, j \cdot \pi_j\};$ 6:    end for
7: $j^* \leftarrow \arg \max_{j \in B} \sigma_j;$ 8: $A \leftarrow A \cup \{(i(\sigma_{j^*}), j^*)\};$ 9: $A_n \leftarrow A_n \cup \{i(\sigma_{j^*})\};$ 10: $f_{j^*} \leftarrow f_{j^*} + p_{i(\sigma_{j^*}), j^*} \cdot \pi_{j^*};$ 11: $\pi_{j^*} \leftarrow \pi_{j^*} \cdot (1 - p_{i(\sigma_{j^*}), j^*});$ 12:    if $f_{j^*} \geq \epsilon$ then
13: $B \leftarrow B \setminus \{j^*\};$ 14:    end if
15: end while

The greedy algorithm has been proved to be efficient for submodular coverage problem, hence we propose a similar greedy heuristic by taking into account the partition matroid constraint. Note that the function $h ( \cdot )$ , akin to $f ( \cdot )$ , is decomposable with respect to spatial tasks. Given a current selected set A and a new element $( i ^ { \prime } , j ^ { \prime } )$ , the marginal increment value is computed as:

$$
\begin{array}{l} h ^ {j ^ {\prime}} (A \cup \{(i ^ {\prime}, j ^ {\prime}) \}) - h ^ {j ^ {\prime}} (A) \\ = \min \left\{\epsilon - f ^ {j ^ {\prime}} (A), f ^ {j ^ {\prime}} \left(A \cup \left\{\left(i ^ {\prime}, j ^ {\prime}\right) \right\}\right) - f ^ {j ^ {\prime}} (A) \right\} \\ = \min \{\epsilon - f ^ {j ^ {\prime}} (A), \prod_ {i \in A _ {n} ^ {j ^ {\prime}}} (1 - p _ {i, j ^ {\prime}}) \cdot p _ {i ^ {\prime}, j ^ {\prime}} \}. \\ \end{array}
$$

G-MCA (Algorithm 2) depicts the procedure computing the assignments. Lines 4–7 select the worker-task pair with the largest marginal increment value according to the derived formulation above. Line 11 updates the probability product term of a task, which is required for fast computing the marginal increment value. Lines 10–14 record the reliability of each task and remove those meeting the threshold requirement. To analyze the time complexity of G-MCA, let us consider the task with the set of least reliable workers. Assume that the smallest confidence value is $p _ { m i n } .$ , and the required number of workers is k. Then we have the inequality

$$
1 - (1 - p _ {m i n}) ^ {k} \geq \epsilon ,
$$

from which we can get k ≥ log1 p ( $k \geq \log _ { 1 - p _ { m i n } } ( 1 - \epsilon )$ . Therefore, for the task linked to the least confident workers, G-MCA requires selecting $\log _ { 1 - p _ { m i n } } ( 1 - \epsilon )$ ) workers to satisfy the reliability constraint. We need to ensure all tasks meet the constraint, which takes $O ( m )$ time (line 4), and selecting each worker takes $O ( n )$ time (line 5). In summary, the time complexity of G-MCA is $O ( m \cdot n \cdot \log _ { 1 - p _ { m i n } } ( 1 - \epsilon ) )$ .

Next we analyze the performance of the greedy heuristic. Let $\Delta _ { e } h ( A ) = \mathsf { \bar { h } } ( A \cup \{ e \} ) - h ( A )$ . To facilitate the proof, we assume that selecting an element e incurs a cost $c ( e )$ . Let $e _ { 1 } , e _ { 2 } , . . . , e _ { k }$ be the sequence of elements selected by the greedy heuristic with respect to $\Delta _ { e } h ( A ) / c ( e )$ , and let $\boldsymbol { S } ^ { \dot { } }$ be a cover with the minimum cost $c ^ { * }$ . Set $\dot { A _ { 0 } } \dot { = } \ddot { \varnothing } , A _ { r } = \{ e _ { t } | 1 \le$ $t \leq r \}$ for each $1 \leq r \leq k$ . Let $l _ { r } = h ( S ) - h ( A _ { r } )$ for each $0 \leq r \leq k .$ . Let α = min $\begin{array} { r } { \frac { \Delta _ { e } h ( A ) } { c ( e ) } , \beta = \frac { \Delta _ { e _ { k } } h ( A _ { k - 1 } ) } { \Delta _ { e _ { 1 } } h ( A _ { 0 } ) } } \end{array}$ , then we have the following theorem:

Theorem 3 Algorithm 2 returns $\begin{array} { r l r } { a } & { { } ( 1 } & { + } & { { \frac { 1 } { \beta } } \ln { \frac { h ( E ) } { \alpha c ^ { * } } } ) } \end{array}$ approximation solution for the MCA problem.

Proof: First, we show that $\begin{array} { r l r } { c ( e _ { r } ) } & { { } \le } & { \frac { c ^ { * } } { \beta l _ { r - 1 } } ( l _ { r - 1 } - l _ { r } ) } \end{array}$ Indeed,

$$
\begin{array}{l} \frac {l _ {r - 1} - l _ {r}}{c \left(e _ {r}\right)} = \frac {\Delta_ {e _ {r}} h \left(A _ {r - 1}\right)}{c \left(e _ {r}\right)} \geq \beta \max _ {e \in S} \frac {\Delta_ {e} h \left(A _ {r - 1}\right)}{c (e)} \\ \geq \frac {\beta \sum_ {e \in S} \Delta_ {e} h (A _ {r - 1})}{\sum_ {e \in S} c (e)} \geq \beta \frac {h (S) - h (A _ {r - 1})}{c ^ {*}} \\ = \frac {\beta l _ {r - 1}}{c ^ {*}}. \\ \end{array}
$$

Since $h ( S ) = l _ { 0 } > l _ { 1 } > \cdots > l _ { k } = 0$ and $h ( S ) ~ \geq ~ \alpha c ^ { * }$ , there exists a unique index t, such that $l _ { t } \geq \alpha c ^ { * } > l _ { t + 1 }$ . For $1 \leq r \leq t + 1$ , we have

$$
\begin{array}{l} \sum_ {r = 1} ^ {t} c (e _ {r}) + \frac {l _ {t} - \alpha c ^ {*}}{l _ {t} - l _ {t + 1}} c (e _ {t + 1}) \\ \leq \frac {c ^ {*}}{\beta} (\sum_ {r = 1} ^ {t} \frac {l _ {r - 1} - l _ {r}}{l _ {r - 1}} + \frac {l _ {t} - \alpha c ^ {*}}{l _ {t}}) \tag {4} \\ \leq \frac {c ^ {*}}{\beta} \int_ {\alpha c ^ {*}} ^ {l _ {0}} \frac {1}{y} d y = \frac {c ^ {*}}{\beta} \ln \frac {l _ {0}}{\alpha c ^ {*}} \\ = \frac {c ^ {*}}{\beta} \ln \frac {h (E)}{\alpha c ^ {*}}. \\ \end{array}
$$

Since $\begin{array} { r } { c ( e _ { k } ) \le \frac { l _ { r - 1 } - l _ { r } } { \alpha } } \end{array}$ , for $t + 1 \leq r \leq k$ , we have

$$
\begin{array}{l} \frac {\alpha c ^ {*} - l _ {t + 1}}{l _ {t} - l _ {t + 1}} c (e _ {t + 1}) + \sum_ {r = t + 2} ^ {k} c (e _ {r}) \\ \leq \frac {1}{\alpha} (\alpha c ^ {*} - l _ {t + 1} + \sum_ {r = t + 2} ^ {k} (l _ {r - 1} - l _ {r})) \tag {5} \\ = c ^ {*}. \\ \end{array}
$$

Combining (4) and (5), we obtain

$$
\begin{array}{l} \sum_ {r = 1} ^ {k} c (e _ {r}) = \sum_ {r = 1} ^ {t} c (e _ {r}) + \frac {l _ {t} - \alpha c ^ {*}}{l _ {t} - l _ {t + 1}} c (e _ {t + 1}) \\ + \frac {\alpha c ^ {*} - l _ {t + 1}}{l _ {t} - l _ {t + 1}} c (e _ {t + 1}) + \sum_ {r = t + 2} ^ {k} c (e _ {r}) \\ \leq (1 + \frac {1}{\beta} \ln \frac {h (E)}{\alpha c ^ {*}}) c ^ {*}. \\ \end{array}
$$

By setting an equal cost for each element e, we can easily notice that $\sum _ { r = 1 } ^ { k } c ( e _ { r } )$ is the number of selected workers by the greedy heuristic, and $c ^ { * }$ is the minimum number of required workers. Thus we have completed the proof.

The greedy heuristic of G-MCA is inspired by the monotone submodular structure of the formulated problem. We can also consider the another property that the objective function $h ^ { j } ( \cdot )$

TABLE I. EXPERIMENT SETTINGS. 

<table><tr><td>Parameter</td><td>Values</td></tr><tr><td>m (synthetic tasks)</td><td>600, 800, 1000, 1200, 1400</td></tr><tr><td>n (synthetic workers)</td><td>6000, 8000, 10000, 12000, 14000</td></tr><tr><td>m (T-drive tasks)</td><td>100, 150, 200, 250, 300</td></tr><tr><td>n (T-drive workers)</td><td>3000, 3500, 4000, 4500, 5000</td></tr><tr><td>dt (distance threshold)</td><td>0.02 0.03 0.04 0.05 0.06</td></tr><tr><td> $[p_{min}, p_{max}]$ </td><td>[0.5,0.7], [0.6, 0.8], [0.7,0.9], [0.8, 1.0]</td></tr><tr><td>tb (synthetic budget)</td><td>1000, 1500, 2000, 2500, 3000</td></tr><tr><td>tb (T-drive budget)</td><td>200, 300, 400, 500, 600</td></tr><tr><td>ε (reliability)</td><td>0.75, 0.8, 0.85, 0.9, 0.95</td></tr></table>

is captioned by the reliability threshold. Therefore, instead of using the absolute marginal increment value of each task’s reliability, we would also like to consider how large is the residual between the current function value and the reliability threshold. Specifically, consider the current selected set A and a new element $( i ^ { \prime } , j ^ { \prime } )$ . Denote the scaled marginal contribution of $( i ^ { \prime } , j ^ { \prime } )$ as $\delta _ { i ^ { \prime } , j ^ { \prime } }$ , and we design a scaled greedy heuristic:

$$
\begin{array}{l} \delta_ {i ^ {\prime}, j ^ {\prime}} = \min \{1, \frac {f ^ {j ^ {\prime}} (A \cup \{(i ^ {\prime} , j ^ {\prime}) \}) - f ^ {j ^ {\prime}} (A)}{\epsilon - f ^ {j ^ {\prime}} (A)} \} \\ = \min \{1, \frac {\prod_ {i \in A _ {n} ^ {j ^ {\prime}}} (1 - p _ {i , j ^ {\prime}}) \cdot p _ {i ^ {\prime} , j ^ {\prime}}}{\epsilon - f ^ {j ^ {\prime}} (A)} \} \\ \end{array}
$$

By replacing the marginal increment value computation in line 5 of Algorithm 2 with the above scaled formulation, we obtain a new algorithm called SG-MCA. Intuitively, SG-MCA gives higher priority to the task whose reliability function value is closer to the threshold.

Note: The above results can be generalized to scenarios where each task has a different reliability threshold. Specifically, we can associate a reliability threshold $\epsilon _ { j }$ for the task $j ,$ and change Eq. (3) to

$$
f ^ {j} (A) \geq \epsilon_ {j}, \forall j \in [ m ] \Longleftrightarrow h (A) = \frac {1}{m} \sum_ {j \in [ m ]} \epsilon_ {j}.
$$

Then the results can be derived similarly as stated in this section.

# VI. PERFORMANCE EVALUATION

In this section, we evaluate the performance of the proposed methods over synthetic and real-world data. We first demonstrate the experiment settings. Then we present the results for MRA and MCA problems.

# A. Experiment Settings

Datasets. For synthetic data, locations of workers and tasks are generated in a 2D data space [0, 1]2, following uniform distribution. The task preference of workers is represented by the distance. Specifically, a worker is interested in performing tasks located within a distance threshold. The confidence of a worker is randomly produced according to uniform distribution within the range $[ p _ { m i n } , p _ { m a x } ]$ .

For real data, we use the T-drive dataset [49], [50]. This dataset contains the GPS traces of 10,357 taxis in Beijing for one week in 2008. There are around 15 million GPS sampling points in the dataset. The total travelling distance is around

![](images/3117fefc140cf20396cb339b96734b150e1be1911ae7dc498960c2b75cff44a2.jpg)



(a) Synthetic Data

![](images/bb04879b3f5f9066348d0622764292c77fd13fea62f4d4890969fc16d175e226.jpg)



(b) T-drive Data

Fig. 3. Effect of the Number of Tasks   
![](images/f387b25fc4e57f65013c638503eb5e92e3a308e1bb8da15f439d9e2168cdc626.jpg)



(a) Synthetic Data

![](images/6762b04dbe466416d7814c3e81858441e769af4ca81da96c3952ea127f142d94.jpg)



(b) T-drive Data

Fig. 4. Effect of the Number of Workers   
![](images/1f358550f37b6a58e8c41e564f02c0433ba2c6198bfa9adb31d92f10e9e4e027.jpg)



(a) Synthetic Data

![](images/507d0097c9f627514fdd804822e9bbcd0cf26d3f4f66dfc20ad1c1ba30573f68.jpg)



(b) T-drive Data   
Fig. 5. Effect of the Total Budget

9 million kilometers. We consider each taxi as a worker, and assume that each worker is interested in taking spatial tasks located along her/his trajectory. Spatial tasks are generated in the road networks of Beijing. Specifically, the road network is a set of road segments with the attributes of segment ID, segment length, and the GPS coordinates of the head and end of the segment. Spatial tasks are randomly generated among the GPS coordinates of the segment ends. We use an HMM algorithm [51] to perform map matching, which maps each GPS point of a worker’s trace to the corresponding road segment. As a result, we can obtain a worker’s preferred tasks by checking the tasks located in the sequence of the worker’s travelling road segments. The reliability of each worker is generated using the same scheme as for the synthetic data.

Configuration. The numerical settings are listed in Table I, where the default values of parameters are in bold font. In each set of experiments, only one parameter is adjusted while the others are fixed to their default values. We implement two schemes, RANDOM and GMM, for comparison. RANDOM selects a task randomly and assigns an available worker to the task if possible. It serves as a baseline for the proposed problems. For the MRA problem, we implement RANDOM by running the random selection and assignment process repeatedly until the budget is used up. For the MCA problem, we execute random selection and assignment process until the predefined reliability of each task is satisfied. GMM is adapted from the greedy strategy for the maximum task assignment problem [1], where the confidence of a worker is considered equal. It is a proper candidate for comparison, as the proposed methods take into account the difference of the worker confidence. For the MRA problem, we execute GMM multiple rounds until the budget is used up. For the MCA problem, we execute GMM multiple rounds until the predefined reliability for each task is satisfied.

![](images/a73497a815973ff9cf63f99c44e03936cd6266a21ba2aade2be351ae8d607f0b.jpg)



(a) Synthetic Data

![](images/eb39981185e6349c35f4330a60bc295d6e9f6577017ddb1b752aa7ffa5042eaf.jpg)



(b) T-drive Data

Fig. 6. Effect of the Range of Worker Confidence   
![](images/8473d4d342581c24eaa3201a2994a4f6a10ab900e915f35057aa3db9625f9cbf.jpg)



Fig. 7. Effect of the Distance Threshold

# B. Results for MRA Problem

Effect of the number of tasks. Fig. 3 illustrates the performance of the algorithms on different number of tasks. With the increment of the number of tasks, the average task reliability decreases. The rationality of this result is that, in a fixed worker market with a budget, the overall capability of performing tasks is restricted. Therefore, more tasks lead to fewer resources per task. The curves in the figure also show that the performance of G-MRA is better than that of GMM and RANDOM in all settings of task sizes.

Effect of the number of workers. Fig. 4 shows the results on different number of candidate workers. In both synthetic and T-drive datasets, the average task reliability obtained by G-MRA is not sensitive to the number of workers. It indicates that, once the worker market is sufficiently large, the algorithm is able to assign tasks to the most suitable workers and achieve high reliability. The results also show that G-MRA performs consistently better than the two compared approaches.

Effect of the budget. Fig. 5 reports the effect of the recruitment budget: A larger budget leads to higher reliability. The G-MRA algorithm has noteworthy advantages compared with the two compared algorithms when the budget is relatively small. This frugal property is important to achieve a good reliability-budget tradeoff.

Effect of the range of worker confidence. Fig. 6 shows the effect of the confidence range $[ p _ { m i n } , p _ { m a x } ]$ of workers on the reliability of the algorithms. The G-MRA algorithms obtains high reliability for different ranges, while GMM and RANDOM have a large deviation (Fig. 6b). This reveals that the two compared algorithms perform well when all workers are of high confidence when there are a few thousands of workers. On the contrary, the G-MRA algorithm can assign tasks efficiently even in a worker market with low confidence.

Effect of the distance. Fig. 7 shows that results of different distance thresholds for the synthetic data. Recall that in the synthetic data, the task preference of a worker is reflected by the distance between the task and the worker. Hence the distance threshold indicates the worker-task link probability. A larger distance threshold leads to a larger preferred task sets of a worker. The figure shows that the performance of the algorithms are not very sensitive to the variation of the size of preferred task sets of workers in the experiment, and the G-MRA performs better than the baseline methods.

# C. Results for MCA Problem

Effect of the number of workers. Fig. 8 shows the results of different numbers of workers. When the number of workers increases, the proposed G-MCA and SG-MCA algorithms require fewer recruited workers to meet the task reliability requirement. On the contrary, GMM and RANDOM require nearly the same amount of workers for different numbers of candidates. The two proposed methods are shown to be effective in saving the number of assignments in comparison with the two baseline methods. Furthermore, G-MCA performs slightly better than SG-MCA when the size of candidates is large. Recall that G-MCA selects a task for assignment based on the absolute marginal increment value of the reliability function, while SG-MCA gives higher priority to the task whose current reliability function value is closer to the threshold. In Fig. 8a, when the size of worker candidate is large (i.e., when the size

![](images/09d5d8063deae5ee0e04f3cd3c7cc3eb920b8c4317ce6562d5e8de58d6fb52fd.jpg)



(a) Synthetic Data

![](images/dff33ddc3cd3be1c3e57fcabf1416726764b99a6d4c64ba807f78613e7ca37aa.jpg)



(b) T-drive Data

Fig. 8. Effect of the Number of Workers   
![](images/1ed1cd1649d68f835c3b6070c0281b6f51edc411ac45bb7f58768e13e687a4b4.jpg)



(a) Synthetic Data

![](images/ac69304208a5c1578e4585683165c076fe40cc17896c284e4c3643ef0d1fa59c.jpg)



(b) T-drive Data

Fig. 9. Effect of the Number of Tasks   
![](images/a8a3a1a3f42ca290efa8efcae10c5e3ce32fa17ad06dce3ae0e5afdd1c851466.jpg)



(a) Synthetic Data

![](images/108a9b3098f64013a01e112e6633d80aaeb95ef840ebb1e3ff74f2746a3ed231.jpg)



(b) T-drive Data   
Fig. 10. Effect of the Range of Worker Confidence

![](images/b58d62034ba421ec8b1232583784d28c83fe0a05e19190bbd957cedb808463b3.jpg)



(a) Synthetic Data

![](images/30facf3f0e0f840b4dddc0afd4e4042a451548a8443eff90f7b258bedb6eee65.jpg)



(b) T-drive Data   
Fig. 11. Effect of the Task Reliability Threshold

is larger than $0 . 8 \times 1 0 ^ { 4 }$ candidates in the experiment), the strategy of G-MCA seems more effective in assignment, as there are more workers who have high confidence, such that selecting these workers may likely make the corresponding task meet the reliability requirement immediately, even though this task is not favored by SG-MCA. Fig. 8b also supports this phenomenon, where the cost of SG-MCA is relatively smaller that that of G-MCA given a smaller candidate size.

Effect of the number of tasks. Fig. 9 reveals the effect of the number of tasks. The required workers of all three algorithms increase with the number of tasks at a similar pace. This is because that, given a sufficiently large worker market and a predefined task reliability, each extra task is assigned with an approximate number of workers for each algorithm. Again, the two proposed algorithms have comparable performance, and are superior to the two compared algorithms.

Effect of the range of worker reliability. Fig. 10 reports the effect of the range of worker confidence. The required numbers of workers by the G-MCA and SG-MCA are smaller than that of GMM and RANDOM in all cases except for the range of [0.7, 0.9]. This is because that, the default task reliability is 0.9, and in the experiments, the $[ p _ { m i n } , p _ { m a x } ]$ is implemented as an open interval, which imposes that G-MCA and SG-MCA need at least two workers per task. On the other hand, two workers with the confidence range of [0.7, 0.9] suffice to ensure a task with a reliability value of 0.9 for GMM and RANDOM.

Effect of the task reliability threshold. Fig. 11 shows the results of fulfilling different task reliability requirements. The number changes of recruited workers by the G-MCA and SG-MCA are less sensitive to the reliability than the GMM and RANDOM. The reason is that the two proposed heuristics are able to select the most confident workers given a worker budget, and hence can fulfill a larger range of task reliability with a fixed number of workers.

Effect of the distance. Fig. 12 shows the effect of different distance thresholds in the synthetic data. The baseline approaches are not sensitive to the variation of the distance threshold, while the G-MCA and SG-MCA perform better with the increment of the distance threshold. As the distance threshold reflects the size of preferred task sets of a worker,

![](images/ad0db7809edd03bdf110e1bf845936ca0f5d803e7f4ed5f83702dee5fed080d3.jpg)



Fig. 12. Effect of the Distance Threshold

the result indicates that the G-MCA and SG-MCA approaches are effective in assigning the most suitable tasks to workers.

# VII. CONCLUSION

In this paper, we propose the problem of reliable spatial crowdsourcing in a large worker market, which aims at assigning tasks to workers efficiently and economically. Specifically, we formulate two assignment problems, maximum reliability assignment (MRA) under a recruitment budget, and minimum cost assignment (MCA) under a task reliability requirement. We prove that the two formulated problems possess submodular properties, based on which we design efficient greedy heuristics with performance guarantees. Extensive experiments have been conducted to validate the efficiency and effectiveness of the proposed approaches on both real and synthetic datasets. In the future, we will investigate to build a crowdsensing system to incorporate the proposed methods.

# REFERENCES

[1] L. Kazemi and C. Shahabi, “Geocrowd: enabling query answering with spatial crowdsourcing,” in Proceedings of ACM International Conference on Advances in Geographic Information Systems (GIS), 2012.

[2] E. Koukoumidis, L.-S. Peh, and M. R. Martonosi, “Signalguru: leveraging mobile phones for collaborative traffic signal schedule advisory,” in Proceedings of ACM international conference on Mobile systems, applications, and services (MobiSys), 2011, pp. 127–140.   
[3] “Waze,” https://www.waze.com/.   
[4] N. Maisonneuve, M. Stevens, M. Niessen, and L. Steels, “Noisetube: Measuring and mapping noise pollution with mobile phones,” Information Technologies in Environmental Engineering, pp. 215–228, 2009.   
[5] “Openstreetmap,” http://www.openstreetmap.org/.   
[6] L. Kazemi, C. Shahabi, and L. Chen, “Geotrucrowd: trustworthy query answering with spatial crowdsourcing,” in Proceedings of ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (GIS), 2013.   
[7] H. To, G. Ghinita, and C. Shahabi, “A framework for protecting worker location privacy in spatial crowdsourcing,” Proceedings of the VLDB Endowment, vol. 7, no. 10, pp. 919–930, 2014.   
[8] P. Cheng, X. Lian, Z. Chen, R. Fu, L. Chen, J. Han, and J. Zhao, “Reliable diversity-based spatial crowdsourcing by moving workers,” Proceedings of the VLDB Endowment, vol. 8, no. 10, pp. 1022–1033, 2015.   
[9] J. Burke, D. Estrin, M. Hansen, A. Parker, N. Ramanathan, S. Reddy, and M. Srivastava, “Participatory sensing,” 2006.   
[10] “University of california berkeley, 2008-2009,” http://traffic.berke ley.edu/.   
[11] B. Hull, V. Bychkovsky, Y. Zhang, K. Chen, M. Goraczko, A. Miu, E. Shih, H. Balakrishnan, and S. Madden, “Cartel: a distributed mobile sensor computing system,” in Proceedings of ACM International Conference on Embedded Networked Sensor Systems (SenSys), 2006.   
[12] P. Mohan, V. Padmanabhan, and R. Ramjee, “Nericell: rich monitoring of road and traffic conditions using mobile smartphones,” in Proceedings of ACM International Conference on Embedded Networked Sensor Systems (SenSys), 2008.   
[13] W. Sun, Q. Li, and C.-K. Tham, “Wireless deployed and participatory sensing system for environmental monitoring,” in Proceedings of IEEE International Conference on Sensing, Communication, and Networking (SECON), 2014, pp. 158–160.   
[14] F. Saremi, O. Fatemieh, H. Ahmadi, H. Wang, T. Abdelzaher, R. Ganti, H. Liu, S. Hu, S. Li, and L. Su, “Experiences with greengps–fuelefficient navigation using participatory sensing,” IEEE Transactions on Mobile Computing, vol. 15, no. 3, pp. 672–689, 2016.   
[15] S. He, D.-H. Shin, J. Zhang, and J. Chen, “Toward optimal allocation of location dependent tasks in crowdsensing,” in Proceedings of IEEE International Conference on Computer Communications (INFOCOM), 2014, pp. 745–753.   
[16] S. Reddy, D. Estrin, and M. Srivastava, “Recruitment framework for participatory sensing data collections,” in Pervasive Computing. Springer, 2010, pp. 138–155.   
[17] L. Pournajaf, L. Xiong, V. Sunderam, and S. Goryczka, “Spatial task assignment for crowd sensing with cloaked locations,” in Proceedings of IEEE International Conference on Mobile Data Management (MDM), 2014.   
[18] D. Deng, C. Shahabi, and U. Demiryurek, “Maximizing the number of worker’s self-selected tasks in spatial crowdsourcing,” in Proceedings of ACM International Conference on Advances in Geographic Information Systems (GIS), 2013.   
[19] B. Guo, Z. Wang, Z. Yu, Y. Wang, N. Y. Yen, R. Huang, and X. Zhou, “Mobile crowd sensing and computing: The review of an emerging human-powered sensing paradigm,” ACM Computing Surveys (CSUR), vol. 48, no. 1, pp. 1–31, 2015.   
[20] B. Guo, C. Chen, D. Zhang, Z. Yu, and A. Chin, “Mobile crowd sensing and computing: when participatory sensing meets participatory social media,” IEEE Communications Magazine, vol. 54, no. 2, pp. 131–137, 2016.   
[21] R. K. Ganti, F. Ye, and H. Lei, “Mobile crowdsensing: Current state and

future challenges,” IEEE Communications Magazine, vol. 49, no. 11, pp. 32–39, 2011.   
[22] C. Wu, Z. Yang, and Y. Liu, “Smartphones based crowdsourcing for indoor localization,” IEEE Transactions on Mobile Computing, vol. 14, no. 2, pp. 444–457, 2015.   
[23] X. Zhang, Z. Yang, C. Wu, W. Sun, Y. Liu, and K. Xing, “Robust trajectory estimation for crowdsourcing-based mobile applications,” IEEE Transactions on Parallel and Distributed Systems, vol. 25, no. 7, pp. 1876–1885, 2014.   
[24] B. Guo, H. Chen, Z. Yu, X. Xie, S. Huangfu, and D. Zhang, “Fliermeet: A mobile crowdsensing system for cross-space public information reposting, tagging, and sharing,” IEEE Transactions on Mobile Computing, vol. 14, no. 10, pp. 2020–2033, 2015.   
[25] C. Costa, C. Laoudias, D. Zeinalipour-Yazti, and D. Gunopulos, “Smarttrace: Finding similar trajectories in smartphone networks without disclosing the traces,” in Proceedings of IEEE ICDE, 2011.   
[26] G. Cardone, L. Foschini, P. Bellavista, A. Corradi, C. Borcea, M. Talasila, and R. Curtmola, “Fostering participaction in smart cities: a geo-social crowdsensing platform,” IEEE Communications Magazine, vol. 51, no. 6, pp. 112–119, 2013.   
[27] D. Zhang, H. Xiong, L. Wang, and G. Chen, “Crowdrecruiter: selecting participants for piggyback crowdsensing under probabilistic coverage constraint,” in Proceedings of ACM International Joint Conference on Pervasive and Ubiquitous Computing (Ubicomp), 2014, pp. 703–714.   
[28] H. Xiong, D. Zhang, G. Chen, L. Wang, and V. Gauthier, “Crowdtasker: maximizing coverage quality in piggyback crowdsensing under budget constraint,” in Proceedings of IEEE International Conference on Pervasive Computing and Communications (PerCom), 2015, pp. 55–62.   
[29] A. Ahmed, K. Yasumoto, Y. Yamauchi, and M. Ito, “Distance and time based node selection for probabilistic coverage in people-centric sensing,” in Proceedings of IEEE Communications Society Conference on Sensor, Mesh and Ad Hoc Communications and Networks (SECON), 2011.   
[30] S. Hachem, A. Pathak, and V. Issarny, “Probabilistic registration for large-scale mobile participatory sensing,” in Proceedings of IEEE International Conference on Pervasive Computing and Communications (PerCom), 2013.   
[31] L. G. Jaimes, I. Vergara-Laurens, and M. A. Labrador, “A location-based incentive mechanism for participatory sensing systems with budget constraints,” in Proceedings of International Conference on Pervasive Computing and Communications (PerCom), 2012, pp. 103–108.   
[32] W. Sun and C.-K. Tham, “An information-driven incentive scheme with consumer demand awareness for participatory sensing,” in Proceedings of IEEE International Conference on Sensing, Communication, and Networking (SECON), 2015, pp. 319–326.   
[33] Y. Wen, J. Shi, Q. Zhang, X. Tian, Z. Huang, H. Yu, Y. B. Cheng, and X. Shen, “Quality-driven auction based incentive mechanism for mobile crowd sensing,” IEEE Transactions on Vehicular Techonology, vol. 64, no. 9, pp. 4203–4214, 2015.   
[34] D. Yang, G. Xue, X. Fang, and J. Tang, “Crowdsourcing to smartphones: incentive mechanism design for mobile phone sensing,” in Proceedings of ACM international conference on Mobile computing and networking (MobiCom), 2012.   
[35] A. Singla and A. Krause, “Incentives for privacy tradeoff in community sensing,” in Proceedings of AAAI Conference on Human Computation and Crowdsourcing (HCOMP), 2013.   
[36] X. Zhang, Z. Yang, Z. Zhou, H. Cai, L. Chen, and X. Li, “Free market of crowdsourcing: Incentive mechanism design for mobile sensing,” IEEE Transactions on Parallel and Distributed Systems, vol. 25, no. 12, pp. 3190–3200, 2014.   
[37] X. Zhang, Z. Yang, W. Sun, Y. Liu, S. Tang, K. Xing, and X. Mao, “Incentives for mobile crowd sensing: A survey,” IEEE Communications Surveys and Tutorials, vol. 18, no. 1, pp. 54–67, 2016.   
[38] A. Al-Fuqaha, M. Guizani, M. Mohammadi, M. Aledhari, and M. Ayyash, “Internet of things: A survey on enabling technologies, pro-

tocols, and applications,” IEEE Communications Surveys and Tutorials, vol. 17, no. 4, pp. 2347–2376, 2015.   
[39] J. Liu, N. Kato, J. Ma, and N. Kadowaki, “Device-to-device communication in lte-advanced networks: a survey,” IEEE Communications Surveys and Tutorials, vol. 17, no. 4, pp. 1923–1940, 2014.   
[40] J. Liu, S. Zhang, N. Kato, H. Ujikawa, and K. Suzuki, “Device-todevice communications for enhancing quality of experience in software defined multi-tier lte-a networks,” IEEE Network, vol. 29, no. 4, pp. 46–52, 2015.   
[41] J. Liu, Y. Kawamoto, H. Nishiyama, N. Kato, and N. Kadowaki, “Device-to-device communications achieve efficient load balancing in lte-advanced networks,” IEEE Wireless Communications, vol. 21, no. 2, pp. 57–65, 2014.   
[42] J. Liu, H. Nishiyama, N. Kato, and J. Guo, “On the outage probability of device-to-device-communication-enabled multichannel cellular networks: An rss-threshold-based perspective,” IEEE Journal on Selected Areas in Communications, vol. 34, no. 1, pp. 163–175, 2016.   
[43] C.-J. Ho and J. W. Vaughan, “Online task assignment in crowdsourcing markets.” in Proceedings of AAAI, 2012.   
[44] C.-J. Ho, S. Jabbari, and J. W. Vaughan, “Adaptive task assignment for crowdsourced classification,” in Proceedings of ICML, 2013, pp. 534–542.   
[45] D. J. Welsh, Matroid theory. Courier Dover Publications, 2010.   
[46] G. L. Nemhauser, L. A. Wolsey, and M. L. Fisher, “An analysis of approximations for maximizing submodular set functionsłi,” Mathematical Programming, vol. 14, no. 1, pp. 265–294, 1978.   
[47] J. Bar-Ilan, G. Kortsarz, and D. Peleg, “Generalized submodular cover problems and applications,” Theoretical Computer Science, vol. 250, no. 1, pp. 179–200, 2001.   
[48] P.-J. Wan, D.-Z. Du, P. Pardalos, and W. Wu, “Greedy approximations for minimum submodular cover with submodular cost,” Computational Optimization and Applications, vol. 45, no. 2, pp. 463–474, 2010.   
[49] J. Yuan, Y. Zheng, X. Xie, and G. Sun, “Driving with knowledge from the physical world,” in Proceedings of ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD), 2011.   
[50] J. Yuan, Y. Zheng, C. Zhang, W. Xie, X. Xie, G. Sun, and Y. Huang, “T-drive: driving directions based on taxi trajectories,” in Proceedings of ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (GIS), 2010.   
[51] P. Newson and J. Krumm, “Hidden markov map matching through noise and sparseness,” in Proceedings of ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (GIS), 2009.

![](images/2c8a8984c69bc6f96b6a12189f44ccea1b9f2da52997a10154a169f9f6f37163.jpg)



Xinglin Zhang received a B.E. degree in School of Software from Sun Yat-sen University in 2010 and a Ph.D. degree in the Department of Computer Science and Engineering from Hong Kong University of Science and Technology in 2014. He is currently with the South China University of Technology. His research interests include wireless ad-hoc/sensor networks, mobile computing and crowdsourcing. He is a student member of the IEEE and the ACM.

![](images/1f5095240089e1f9a225541250e819c8e92b389ddaa3f03d45ea8be639f98faf.jpg)



Zheng Yang received a B.E. degree in computer science from Tsinghua University in 2006 and a Ph.D. degree in computer science from Hong Kong University of Science and Technology in 2010. He is currently an associate professor at Tsinghua University. His main research interests include wireless ad-hoc/sensor networks and mobile computing. He is a member of the IEEE and the ACM.

![](images/446c08257bcdbf70b51751392abfe64615740982b499b2975f04d46059a4c926.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is Chang Jiang Chair Professor and Dean of the School of Software at Tsinghua University. His research interests include wireless sensor network, peer-to-peer computing, and pervasive computing. He is a fellow of the IEEE and a fellow of the ACM.

![](images/db27b76e80d1e5cd71785aa023315002dbda0f4e1c40eded5d5b803f5636294c.jpg)



Shaohua Tang received the B.Sc. and M.Sc. Degrees in applied mathematics, and the Ph.D. Degree in communication and information system all from the South China University of Technology, in 1991, 1994, and 1998, respectively. He has been a full professor with the School of Computer Science and Engineering, South China University of Technology since 2004. His current research interests include information security, networking, and information processing. He is a member of the IEEE and the IEEE Computer Society.