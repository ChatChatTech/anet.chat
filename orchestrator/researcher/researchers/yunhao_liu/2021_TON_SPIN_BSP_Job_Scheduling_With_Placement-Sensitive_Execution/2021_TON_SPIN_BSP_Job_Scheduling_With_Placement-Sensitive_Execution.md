# SPIN: BSP Job Scheduling With Placement-Sensitive Execution

Zhenhua Han , Haisheng Tan , Senior Member, IEEE, Shaofeng H.-C. Jiang , Wanli Cao, Xiaoming Fu , Senior Member, IEEE, Lan Zhang , Member, IEEE, and Francis C. M. Lau

Abstract— The Bulk Synchronous Parallel (BSP) paradigm is gaining tremendous importance recently due to the popularity of computations as distributed machine learning and graph computation. In a typical BSP job, multiple workers concurrently conduct iterative computations, where frequent synchronization is required. Therefore, the workers should be scheduled simultaneously and their placement on different computing devices could significantly affect the performance. Simply retrofitting a traditional scheduling discipline will likely not yield the desired performance due to the unique characteristics of BSP jobs. In this work, we derive SPIN, a novel scheduling designed for BSP jobs with placement-sensitive execution to minimize the makespan of all jobs. We first prove the problem approximation hardness and then present how SPIN solves it with a rounding-based randomized approximation approach. Our analysis indicates SPIN achieves a good performance guarantee efficiently. Moreover, SPIN is robust against misestimation of job execution time by theoretically bounding its negative impact. We implement SPIN on a production-trace driven testbed with 40 GPUs. Our extensive experiments show that SPIN can reduce the job makespan and the average job completion time by up to 3× and 4.68×, respectively. SPIN also demonstrates better robustness to execution time misestimation compared with stateof-the-art heuristic baselines.

Index Terms— Bulk Synchronous Parallel (BSP) jobs, job scheduling, placement-sensitive execution.

Manuscript received June 25, 2020; revised January 4, 2021 and May 8, 2021; accepted May 24, 2021; approved by IEEE/ACM TRANSACTIONS ON NETWORKING Editor T. He. Date of publication June 22, 2021; date of current version October 15, 2021. This work was supported in part by the National Key Research and Development Program of China under Grant 2018YFB0803400; in part by the NSFC under Grant 61772489, Grant 61822209, and Grant 61932016; in part by the Key Research Program of Frontier Sciences (CAS) under Grant QYZDY-SSW-JSC002; in part by the Hong Kong CRF under Grant C7036-15G; and in part by the European Union’s Horizon 2020 Research and Innovation Program through the Grant of Marie Sklodowska-Curie under Grant 824019. A preliminary version of this work titled “Scheduling Placement-Sensitive BSP Jobs with Inaccurate Execution Time Estimation” will appear on Proc. of the 39th Annual IEEE International Conference on Computer Communications (INFOCOM), Beijing, China, April 2020 [1]. (Corresponding author: Haisheng Tan.)

Zhenhua Han is with the LINKE Lab, University of Science and Technology of China (USTC), Hefei 230027, China (e-mail: hzhua201@gmail.com).

Haisheng Tan, Wanli Cao, and Lan Zhang are with the LINKE Lab, USTC, Hefei 230027, China, and also with the CAS Key Laboratory of Wireless-Optical Communications, USTC, Hefei 230027, China (e-mail: hstan@ustc.edu.cn; cwl233@mail.ustc.edu.cn; zhanglan@ustc.edu.cn).

Shaofeng H.-C. Jiang was with the Department of Computer Science, Aalto University, 02150 Espoo, Finland. He is now with the Center on Frontiers of Computing Studies, Department of Computer Science, Peking University, Beijing 100871, China (e-mail: shaofeng.jiang@pku.edu.cn).

Xiaoming Fu is with the Institute of Computer Science, Georg-August-University of Goettingen, 37077 Goettingen, Germany (e-mail: fu@cs.uni-goettingen.de).

Francis C. M. Lau is with the Department of Computing Science, The University of Hong Kong (HKU), Hong Kong (e-mail: fcmlau@cs.hku.hk).

Digital Object Identifier 10.1109/TNET.2021.3087221

# I. INTRODUCTION

M ANY have seen the recent significant progress and suc-cessful applications of distributed machine learning [2] cessful applications of distributed machine learning [2] and graph computation [3], which in most cases make use of very large datasets. In these computations, for faster execution, multiple workers are adopted, where the dataset involved is partitioned and distributed for synchronous parallel iterative processing. Bulk Synchronous Parallel (BSP) is the paradigm for this kind of computation, where computation-intensive jobs and powerful specialized computing device are involved, e.g., GPU, TPU [4], and FPGA. Fig. 1 depicts a general process of the BSP workflow. In an iteration (a mini-batch in machine learning or a superstep in graph processing.), each worker computes the local update based on its own sample batch of data, share the result with the others to aggregate the updates and then move to the next iteration. The following unique characteristics bring new challenges to scheduling BSP jobs:

• Firstly, a job is divided and handled by a number of workers for parallel iterative processing. All the workers must be allocated to the job and scheduled synchronously, which is also called gang scheduling [5].

• Secondly, as multiple workers are involved in processing a job, frequent cross-device communication is required. Therefore, the job execution time is placement-sensitive, e.g., a deep learning job trained on  GPUs within the 4same server would be much faster than if it is on different servers.

Finally, due to the unpredictable performance and contention in computation/communication, it is hard to avoid inaccurate execution time estimation of the jobs. The scheduler might make a poor decision if it is agnostic to such estimation errors. A robust scheduler should be aware and tolerant of estimation errors.

Existing job scheduling approaches [6]–[10] are mainly designed for big-data analytic processing, e.g., Hadoop [11] and Spark [12]. Such big-data jobs usually contain short-lived and fine-grained tasks where gang-scheduling is not required. The frequent task completion will allow the big-data scheduler to redistribute resources efficiently. Also, the state-ofthe-art analysis on big-data jobs in [13] have revealed that representative Spark workloads (including production jobs) are mainly dominated by computation but not I/O. Retrofitting schedulers designed for big-data jobs to our BSP jobs could lead to inefficient executions and a serious waste of precious computing resources.

In this work, we propose a scheduling algorithm to improve cluster efficiency by tailoring our strategy to match the unique characteristics of BSP jobs. Specifically, we are given a set of BSP jobs, where each job could have multiple feasible placements. A job placement involves a set of computing devices to execute the workers and its execution time is placement-sensitive. Our problem is to jointly consider the job placements and scheduling so as to minimize the makespan, i.e., the period of time to finish all jobs, which is a key performance indicator of cluster efficiency. Without insisting on accurate prediction of the job’s execution time as input, our solution is robust against estimation errors. Our contributions can be summarized as follows.

![](images/ac6aa15b01f7d8d609e3197516eab5987de89c3702e7528411bbbbd69c89debf.jpg)



Fig. 1. The bulk synchronous parallel computing paradigm.

• We first formulate the gang scheduling problem for jobs with placement-sensitive execution time and inaccurate execution time estimation. We prove that the problem is approximate-hard within a factor of $\begin{array} { r } { O ( \frac { \log n _ { p } } { 2 \sqrt { \log \log n _ { p } } } ) } \end{array}$ , where $n _ { p }$ ( 2 log log )is the maximum number of workers involved in one BSP job.   
• We derive a novel scheduling algorithm, named SPIN, and prove it has an approximation ratio of $O ( n _ { p } \ln { | \mathcal { M } | } )$ , ( ln )where M is the set of all the computing devices in the cluster. To the best of our knowledge, this is the first approximate algorithm for gang scheduling placement-sensitive jobs.   
SPIN is robust to estimation errors on the job execution time. We theoretically analyze the impact of estimation errors and prove that their negative impact on cluster efficiency can be bounded by SPIN.   
We implement SPIN on Kubernetes [14] and schedule jobs in batches so that SPIN can be applied to schedule online arriving jobs. Based on Microsoft’s production trace of distributed deep learning jobs [15], we conduct extensive experiments on a testbed cluster with 40 NVIDIA P100 GPUs and large-scale simulations of various parameter variations. Evaluation results show that SPIN significantly improves the cluster efficiency by up to × and reduce the average job completion time by up to . × compared with the state-of-the-art heuristic 4 68big-data scheduler. Moreover, our experiments validate that SPIN is robust to the misestimation of job execution time.

Roadmap: The remainder of the paper is organized as follows. In Sec. II, we describe our motivations. In Sec. III, we define the system model and formulate the problem, and prove its approximation hardness. In Sec. IV, we present our algorithm SPIN and analyze its theoretical performance. In Sec. V, we demonstrate the prototype setting and the performance evaluation results. We survey the related works in Sec. VI and conclude this paper in Sec. VII.

![](images/e0085bf6d0c1a63e2cfea66442926db970a974d59c4969b4fe4c7e8f78ead1a7.jpg)



(a) GPU server topology in a cluster

![](images/bbb1ff7486cfff20b85ca261ee5cce5238200f666250518116e796533a4a998c.jpg)



Fig. 2. The topology of a GPU server cluster and the placement-sensitivity of different deep learning models.

# II. MOTIVATION

# A. Placement Sensitivity

With the growing power of specialized hardware (e.g., GPUs), computation becomes much faster and thus communication could become the potential bottleneck [16]. Different aggregation bandwidth will lead to different job performance. Moreover, different jobs could have different levels of sensitivity to their worker placements. For example, as shown in Fig. 2, there are two GPU servers, respectively with and 4 GPUs organized hierarchically and connected via PCI-e 8switches, CPU sockets, cross-socket QPI links and a network. GPUs within the same PCI-e switch, the same CPU socket and across different CPU sockets can leverage isolated PCI-e lanes, shared PCI-e lanes and shared QPI lanes, respectively, with decreasing bandwidth. GPUs across different servers need to communicate via a slower network. It has been observed that the training speed of deep learning training could be sensitive to different placements [17]. The deep learning training of VGG16 model [18] is very sensitive to the GPU topology of different placements. Its training speed drops when the placement is across PCI-e switches/CPU sockets/servers. Even with a very high inter-GPU connection (∼  GB/s for QPI 16link), the cross CPU-socket placement could still lead to 40% speed loss. When the two GPUs are on different server, the VGG16 model could be worsen by ×. The ResNet-1050 model [19] is not sensitive to the intra-server placements, but sensitive to the cross-server placement. The placement sensitivity will be more severe for BSP jobs of geo-distributed data processing. A poor job placement, e.g., deployed on two geologically distant workers, might lead to large communication overhead. However, not all BSP jobs are sensitive to placement. The heterogeneous placement-sensitivity makes the scheduling of BSP jobs more difficult.

![](images/6e29d8ce4f0f1eb4bfdfae275177b0714ee841428829316da1af826e46747eaa.jpg)



Fig. 3. Example: a big-data scheduler is inefficient for BSP jobs.

# B. Inefficiency of Existing Schedulers

Due to the gang-scheduling requirement, a job should be allocated with all the resources requested. However, as it has been observed and discussed in [20] since big-data schedulers allocate resources to the fine-grained tasks, it is possible that a job is only allocated with a part of workers requested, but it will hold the resources and halt. When multiple such jobs exist, the resource deadlock problem could appear (e.g., when there are four GPUs and two 4-GPUs jobs, a deadlock appears when each 4-GPU job holds two GPUs).1 Moreover, the big-data scheduler could make inefficient scheduling decisions when it is agnostic to the placement-sensitivity.

Fig. 3 demonstrates an example of how a big-data scheduler could fail when scheduling distributed deep learning jobs. In the beginning, there come seven 1-GPU jobs with different durations. When the 4-GPU VGG16 job arrives, since there are four available GPUs across two servers, the big-data scheduler would immediately schedule the four GPU workers across two servers that could lead to ∼ × slowdown on its 10training speed. When the 4-GPU ResNet-50 arrives, its GPUs 4cannot be allocated immediately. The big-data scheduler would partially allocate GPUs to let ResNet-50 hold them until 3there are four free GPUs. When the -th GPU is allocated to 4ResNet-50, its four GPU workers have to be scheduled on two servers, which slows down its performance by ∼ ×. However, 2the optimal scheduler would not immediately schedule the 4-GPU VGG16 model to avoid using the fragmented GPUs by waiting for the availability of four GPUs in the same server. The latter arrived 4-GPU ResNet-50 job can also be scheduled on the best placement within a server. Therefore, a smart scheduler needs to be careful to play the trade-offs among queuing delay and placement-sensitivity.

1A workaround solution is to make a job release its resources after a random time-out when it is not further allocated all resources requested, which could mitigate the deadlock problem [20].

# III. PROBLEM FORMULATION

# A. System Model

We consider a system with $\mathcal { M } = \{ m _ { 1 } , \dots , m _ { | \mathcal { M } | } \}$ computing devices $( \mathrm { e . g . }$ = 1., CPU cores, GPUs, TPUs and FPGAs), and a set of $\mathrm { B S P } ^ { 2 }$ jobs $\mathcal { I } = \{ j _ { 1 } , \ldots , j _ { | \mathcal { I } | } \}$ . Each job has a = 1set of feasible placements. Denote as ${ \cal { S } } _ { i } = \{ { s _ { i , 1 } , . . . , s _ { i , | S _ { i } | } } \}$ the feasible placements of job $j _ { i } ,$ = 1, where each placement is a set of computing devices. A job’s workers will be placed on the scheduled computing devices when the job starts. A computing device can run at most one worker at the same time, which is the common practice of specialized hardwares like GPUs. A centralized scheduler is responsible to choose which placement each job will use, and when each job should start its computation.

Due to the fine-grained synchronization of BSP jobs (i.e., synchronizing at every iteration), each job’s workers should be gang-scheduled that the computing devices in the chosen placement should be available simultaneously. The job will also release the computing devices it occupies simultaneously when it finishes. We denote as $p ( s _ { i k } )$ the execution time of the job $j _ { i }$ on the placement $s _ { i k }$ . Without loss of generality, we assume $p ( s _ { i k } )$ is an integer. Due to the overhead and ( )hardness of preemptive scheduling on specialized computing hardware (e.g, lack of hardware support, and modification of computation framework), we focus on non-preemptive scheduling so that a job will run to completion without being preempted. We will discuss in Sec. IV-E how to extend our result when preemption and migration can be supported.

The job execution time under different placements can be estimated via profiling and performance modeling using the techniques similar to Optimus [22]. The estimation errors are usually unavoidable as we have discussed above. Thus, we set $\hat { p } ( s _ { i k } )$ as the estimation value of $p ( s _ { i k } )$ . The scheduler ˆ( )can only observe the value of $\hat { p } ( s _ { i k } )$ ( )instead of $p ( s _ { i k } )$ when ˆ( ) ( )making the scheduling decisions. We assume the estimation is bounded as $\hat { p } ( s _ { i k } ) \in [ \epsilon _ { m i n } \cdot p ( s _ { i k } ) , \epsilon _ { m a x } \cdot p ( s _ { i k } ) ]$ , where $\epsilon _ { m i n } \leq 1$ and $\epsilon _ { m a x } \geq 1$ [ (. Denote as $\begin{array} { r } { \rho \triangleq \frac { \epsilon _ { m a x } } { \epsilon _ { m i n } } } \end{array}$ ( )]the ratio of the 1 1estimation error bounds.

# B. Problem Definition

Based on the above system model, given the set of servers M and jobs ${ \mathcal { I } } ,$ the feasible placements $S _ { i }$ of each job $j _ { i } ,$ , and their estimated execution time (i.e., $\hat { p } ( s _ { i k } ) \ \forall s _ { i k } \in S _ { i } , i \in \mathcal { I } )$ , ˆ( )our problem is to design a scheduling algorithm to choose one feasible placement for each job and decide its start time on each server. Our goal is to optimize the cluster efficiency by minimizing the makespan,3 i.e., the point of time that all jobs finish. A cluster with a smaller makespan means it has higher throughput. Denote as $t _ { i k } ^ { - }$ the start time of the job $j _ { i }$ if it is placed on the devices in $s _ { i k }$ . We first study the offline problem, and then show how we extend SPIN to

2Although we focus on BSP jobs, our result can be extended to other parallel computing paradigms, e.g., Stale Synchronous Parallel (SSP) jobs [21], which are also placement sensitive and gang scheduling required.   
3Makespan is one of the most important metrics of cluster efficiency [8], [10], [23]. It shows the effective processing ability of a cluster.

TABLE I LIST OF IMPORTANT NOTATIONS 

<table><tr><td> $\mathcal{M}$ </td><td>a set of computing devices</td></tr><tr><td> $m_i$ </td><td>the i-th computing device</td></tr><tr><td> $\mathcal{J}$ </td><td>a set of BSP jobs</td></tr><tr><td> $j_i$ </td><td>the i-th job</td></tr><tr><td> $s_{i,k}$ </td><td>the k-th placement of job  $j_i$ </td></tr><tr><td> $\mathcal{S}_i$ </td><td>the feasible placements of job  $j_i$ </td></tr><tr><td> $p(s_{i,k})$ </td><td>the execution time of job  $j_i$  on placement  $s_{i,k}$ </td></tr><tr><td> $\hat{p}(s_{i,k})$ </td><td>the estimated execution time of job  $j_i$  on placement  $s_{i,k}$ </td></tr><tr><td> $\epsilon_{max}$ </td><td>the upper bound of estimation error</td></tr><tr><td> $\epsilon_{min}$ </td><td>the lower bound of estimation error</td></tr><tr><td> $n_p$ </td><td>the maximum number of workers in all jobs&#x27; placements</td></tr><tr><td> $Y_i$ </td><td>the placement of job  $j_i$ </td></tr></table>

schedule online arriving jobs (Sec. IV-E). We formally define the problem as follows

$$
\min _ {x _ {i k}, t _ {i k} ^ {-}} \max _ {j _ {i} \in \mathcal {J}, s _ {i k} \in \mathcal {S} _ {i}} x _ {i k} (t _ {i k} ^ {-} + p (s _ {i k})) \tag {1}
$$

$$
s. t. x _ {i k} \in \{0, 1 \}, \forall j _ {i} \in \mathcal {J}, s _ {i k} \in \mathcal {S} _ {i} \tag {2}
$$

$$
\sum_ {s _ {i k} \in \mathcal {S} _ {i}} x _ {i k} = 1, \forall j _ {i} \in \mathcal {J} \tag {3}
$$

$$
\sum_{\substack{j_{i}\in \mathcal{J},s_{ik}\in \mathcal{S}_{i}\\ s.t. x_{ik} = 1,m_{l}\in s_{ik}}}\mathbf{I}[t_{ik}^{-} <   t\leq t_{ik}^{-} + p(s_{ik})]\leq 1,
$$

$$
\forall m _ {l} \in \mathcal {M}, \forall t \tag {4}
$$

where $x _ { i k }$ is the integer 0-1 variable that equals to  if the job ji is placed on $s _ { i k }$ 1, and  otherwise. I · is an indicator function 0 [ ]that equals to if the condition inside holds, and otherwise. 1 0Constraint (3) guarantees all jobs are placed. Constraint (4) ensures there is at most one job running on each device at any time t. Our goal in eqn. (1) is to minimize the makespan, which is to maximize the cluster efficiency.

# C. Hardness Analysis

As shown in Sec. II, the placement sensitivity and the gang-scheduling requirement make our scheduling problem challenging, not to mention no accurate estimation of job execution time. When each placement only requires one computing device, this problem becomes the traditional makespan scheduling in unrelated servers, which has been proven to be NP-hard [24]. Set $n _ { p }$ as the maximum number of workers involved in one job, i.e., $n _ { p } = \operatorname* { m a x } _ { j _ { i } \in \mathcal { I } , s _ { i k } \in S _ { i } } \left| s _ { i k } \right|$ . We have = maxthe following theorem to show the hardness of designing an approximate algorithm for our problem.

Theorem 1: It is NP-hard to find a solution that is $O ( \frac { \log n _ { p } } { 2 \sqrt { \log \log n _ { p } } } )$ -approximate for the scheduling problem of 2 log logplacement-sensitive BSP jobs, even when accurate estimation of job execution time is available $( i . e . , \ \epsilon _ { m i n } = \epsilon _ { m a x } = 1 )$ .

Proof: Given a graph $G ( V , E )$ = = 1with bounded degree B, ( )which is denoted as the instance I, we can create an instance of the BSP job scheduling problem in polynomial time (denoted as I ). The construction is as follows,

• For every vertex $v ~ \in ~ V$ , we create a job $j _ { v } \in \mathcal { I } .$ . This job has only one placement $s _ { v , 1 }$ , which contains no 1computing device. All jobs have a unit execution time.   
For every edge $( u , v ) \in E$ , add a machine, denoted as $m _ { u , v } ,$ ( ) to M. Also, add $m _ { u , v }$ to the placement of $j _ { u }$ and jv , i.e. $s _ { \underline { { u } } , 1 } = s _ { u , 1 } \cup \{ m _ { u , v } \}$ and $s _ { v , 1 } = s _ { v , 1 } \cup \{ m _ { u , v } \}$ . If the graph $G ^ { \flat } \mathrm { s }$ = 1 1 = 1  maximum degree is no greater than B, then the maximum number of servers involved in each job is also B (i.e. $n _ { \mathscr P } = B )$ . Now, we need to prove $O P T ( I ) = O P T ( I ^ { \prime } ) \colon$

=• Given a solution of $I ^ { \prime } ,$ ( ) = ( ) we can translate it to a vertex coloring of the graph G. As all jobs have a unit execution time, they should be executed inside the time intervals with a unit length (i.e. $[ 0 , 1 ) , [ 1 , 2 ) , \ldots ($ . The jobs in [0 1) [1 2)the same interval can be marked as the same color. So $O P T ( I ) \le O P T ( I ^ { \prime } )$ .

( ) ( ) Given a solution of I, i.e., the coloring of vertices, we can schedule the jobs with the same color in the same interval, thus $O P T ( I ^ { \prime } ) \leq O P T ( I )$ .

Thus we have $\mathop { O P T } ( I ) ~ = ~ \mathop { O P T } ( I ^ { \prime } )$ . With a similar pro-( ) = ( )cedure, we can translate any feasible solution of $I ^ { \prime }$ to a vertex coloring of I with the same cost (i.e., the makespan equals the number of colors). Therefore, if we have a α-approximate solution for the BSP job scheduling problem, we can get an α-approximate solution for the vertex coloring problem. However, Knot [25] has proved it is NP-hard to find a solution of $2 ^ { O ( ( \log K ) ^ { 2 } ) }$ colors for K-colorable graphs 2with degree at most 2(log K)2 . $2 ^ { ( \log K ) ^ { 2 } }$ In other words, with the 2graph of degree at most B (which equals to $n _ { p }$ in $I ^ { \prime } )$ , it is NP-hard to color a  √log log B -colorable graph with 2O B colors. Thus, it is NP-hard to find a solution that is $\begin{array} { r } { { \dot { O } } ( \frac { \log n _ { p } } { 2 \sqrt { \log \log n _ { p } } } ) } \end{array}$ ( log√log log np ) -approximate. 

# IV. SPIN ALGORITHM DESIGN

In this section, we first propose our algorithm, SPIN, for Scheduling Placement-sensitive BSP jobs with INaccurate estimation of execution time, and then analyze its approximation ratio and its robustness to misestimation theoretically.

# A. General Idea

Our strategy SPIN first constructs a relaxation of the BSP scheduling problem by addressing the placement-sensitivity and misestimation on job execution time. Specifically, SPIN relaxes the gang-scheduling constraint to build a polynomial-time solvable Linear Programming (LP) as a relaxed version of the BSP scheduling problem. By solving this LP, SPIN can get the lower bound of the optimal solution. SPIN can further learn each job’s preference on their placements and potential impact on the cluster efficiency of different placements. Then, SPIN will carefully gang-schedule the jobs using a randomized rounding scheme based on the solution given by the relaxed LP. SPIN will guarantee each job’s workers can be started at the same time so that the gang-scheduling requirement is satisfied. SPIN will try to minimize the performance gap between the gang-scheduling solution and the lower bound of the optimal solution. We next elaborate our algorithm SPIN in detail.

# B. Solving a Relaxed Linear Programming

A lower bound on the optimal scheduling could provide helpful insights. To understand the scheduling impact due to the placement sensitivity and the misestimation, we first formulate the following linear programming by relaxing constraints of gang scheduling and allowing fractional placements. Define $T _ { i l }$ as the load of job $j _ { i }$ added on the computing device $m _ { l }$ , i.e., $T _ { i l } ~ = ~ p ( s _ { i k } )$ if the job $j _ { i }$ is placed on $s _ { i k }$ and $m _ { l } ~ \in ~ s _ { i k }$ , otherwise $T _ { i l } ~ = ~ 0$ . The load of the computing = 0device ml is defined as the total job load added on ml, i.e., $\textstyle T _ { l } = \sum _ { j _ { i } \in \mathcal { I } } T _ { i l }$ . Define $T _ { \mathrm { m a x } }$ as the load of the heaviest =loaded computing device, i.e., $T _ { \mathrm { m a x } } = \mathrm { m a x } _ { m _ { l } \in \mathcal { M } } T _ { l }$ . Next, we formulate a relaxed LP (denoted as $L P ( \lambda ) )$ to find a lower bound of $T _ { \mathrm { m a x } }$ ( ), which is also a lower bound of the optimal makespan.

Program 1 (The LP relaxation for job placement):

LP λ  M in  (please refer to footnote4 )

$$
s. t. 0 \leq x _ {i k} \leq 1 \forall j _ {i} \in \mathcal {J}, s _ {i k} \in \mathcal {S} _ {i} (\leq \lambda), \tag {5}
$$

$$
\sum_ {s _ {i k} \in \mathcal {S} _ {i} (\leq \lambda)} x _ {i k} = 1 \forall j _ {i} \in \mathcal {J}, \tag {6}
$$

$$
\sum_ {j _ {i} \in \mathcal {J}} \quad \sum_ {s _ {i k} \in \mathcal {S} _ {i} (\leq \lambda)} x _ {i k} \frac {\hat {p} (s _ {i k})}{\epsilon_ {m a x}} \leq \lambda \forall m _ {l} \in \mathcal {M}, \tag {7}
$$

where $x _ { i k }$ ( )s.t.ml∈sikis the fractional placement variable, $S _ { i } ( \leq \ \lambda )$ denotes the subset of $S _ { i }$ such that $\begin{array} { r } { \frac { \hat { p } ( s _ { i k } ) } { \epsilon _ { m a x } } \le \lambda } \end{array}$ ( ), and λ is the ˆ( )-max target maximum load.

In Program 1, Constraints (5) and (6) guarantee each job is assigned to one feasible placement. Constraint (7) restricts that all jobs should be completed within time λ. Note that, because the scheduler does not know the exact execution time of the job under a specific placement $( \mathrm { i } . \mathrm { e } . , p ( s _ { i k } ) )$ , we aggressively ( )use the lower bound of the job execution time $\begin{array} { r } { \mathrm { ( i . e . , ~ } \frac { \hat { p } \left( s _ { i k } \right) } { \epsilon _ { m a x } } . } \end{array}$ -max which is no greater than $p ( s _ { i k } ) )$ in Constraint (7) to find a lower bound of $T _ { m a x }$ ( ). Our theoretical analysis in Sec. IV-D and experiments in Sec. V show that by using $\frac { \hat { p } ( s _ { i k } ) } { \epsilon _ { m a x } }$ in -max Constraint (7) we can make SPIN robust to the misestimation of execution time.

Program 1 is a relaxation of the original problem. To say it, for any feasible placement with the makespan of $\lambda ^ { \prime } ,$ we can find a feasible solution for $L P ( \lambda ^ { \prime } )$ by setting $x _ { i k } = 1$ if job $j _ { i }$ is placed in $s _ { i k }$ , and $x _ { i k } = 0$ ) = 1otherwise. Constraint (7) is = 0satisfied due to the aggressive estimation $\frac { \hat { p } ( s _ { i k } ) } { \epsilon _ { m a x } }$ .

Note that, we do not directly formulate the linear programming by minimizing the makespan in the objective function. Instead, we check the feasibility of $L P ( \lambda )$ to find the optimal $\lambda *$ ( ). This is because it will introduce an infinite integrality gap if we directly minimize makespan in linear programming. In $L P ( \lambda )$ , we use $S _ { i } ( \leq \ \lambda )$ instead of $S _ { i }$ as the available ( ) ( )placement choices in Program 1. We can construct a case that using $s _ { i }$ could lead to a very small fractional $x _ { i k }$ . This would make some placement feasible in the relaxed solution, but bring an infinite gap in the integral solution. Therefore, if a placement choice for a job has an aggressive estimation larger than $\begin{array} { r } { \lambda \left( \mathbf { e . g . , } \frac { \hat { p } \left( s _ { i k } \right) } { \epsilon _ { m a x } } > \bar { \lambda } \right) } \end{array}$ ˆ( )-max , we exclude it from Program 1 thus

4This program is not to optimize some function, but describe a problem in which we are only interested if a feasible solution with a fixed λ exists.

the job will not consider to be scheduled on this placement. When λ is too small such that all jobs are excluded from Program 1, Constraint (6) cannot be satisfied thus $L P ( \lambda )$ would be infeasible.

Program 1 gives an estimation on the lower bound of the optimal makespan. If no feasible solution to $L P ( \lambda )$ exists, it is impossible to find a placement within the makespan of λ for the origin problem. Hence, via a binary search, we can find the minimum $\lambda ,$ denoted as $\lambda ^ { * }$ , making $L P ( \lambda )$ feasible. Note ( )that λ will not be scaled down to arbitrarily small due to the feasibility constraint.

# C. Randomized Rounding for Gang Scheduling

Then we use a randomized rounding policy to transform the fractional solution of $L P ( \lambda ^ { * } )$ to a feasible gang scheduling ( )plan. The intuitive idea is to prioritize the placements according to the fractional solution given by the LP relaxation. The placement with the highest $x _ { i k }$ will be first considered for scheduling. The whole process of making placement decisions can be considered as a random placement scheme following a probability w.r.t. $x _ { i k }$ . Define $Y _ { i } \in S _ { i }$ as the final placement of the job $j _ { i }$ . We describe the details of our randomized rounding policy for gang scheduling in Algorithm 1.

Algorithm 1 SPINScheduler   
1 Let $\lambda^{*}$ be the minimum $\lambda$ such that Program 1 has a feasible solution;
2 Let $\{x_{ik}^{*}|\forall j_{i}\in\mathcal{J},s_{ik}\in\mathcal{S}_{i}\}$ be a solution of $LP(\lambda^{*})$ ;
3 $Y_{i}=\varnothing\quad\forall j_{i}\in\mathcal{J}$ ;
4 Time $t=0$ ;
5 while $\exists j_{i}\in\mathcal{J},Y_{i}=\varnothing$ do
6 $\mathcal{S}'=\{s_{ik}|s_{ik}\in\mathcal{S}_{i},Y_{i}=\varnothing\}$ ;
7    Sort $\mathcal{S}'$ in the descending order of $x_{ik}^{*}$ ;
8    for the placement $s_{ik}\in\mathcal{S}'$ do
9    if the devices in $s_{ik}$ are all free at time $t$ then
10    Generate a random number $\gamma\in[0,1]$ ;
11    if $\gamma<x_{ik}^{*}$ then
12 $Y_{i}=s_{ik}$ ;
13    Start the job $j_{i}$ on the devices in $s_{ik}$ ;
14    else
15    Remove $s_{ik}$ from $\mathcal{S}_{i}$ ;
16    Scale $x_{ik'}^{*}=\frac{x_{ik'}^{*}}{\sum_{s_{ik''}\in S_i}x_{ik''}^*}\quad\forall s_{ik'}\in\mathcal{S}_i$ ;
17 $t=$ the next time point when a job finishes;

SPIN first finds the optimal maximum load $\lambda ^ { * }$ (Line 1). The fractional $x _ { i k } ^ { * }$ variable reveals the optimal sampling probability of the placement to achieve the minimum (relaxed) makespan in expectation. With the fractional placement $x _ { i k } ^ { * }$ of each job (Line 2), the algorithm uses randomized rounding to choose an available placement for each job in the descending order of $x _ { i k } ^ { * }$ (Line 3 to Line 17). Job $j _ { i }$ will be placed on $s _ { i k }$ with the probability $x _ { i k } ^ { * }$ (Line 10 to Line 13). When the job $j _ { i }$ rejects to be scheduled on $s _ { i k }$ , the placement $s _ { i k }$ will be removed from $\boldsymbol { S } _ { i }$ . The remaining placements in $S _ { i }$ will scale the $x _ { i k } ^ { * }$ accordingly (Line 15 to Line 16). Since Constraint (6) guarantees the sum of $x _ { i k }$ over each job’s placements is , every job would be assigned to a feasible placement.

Let $\lambda _ { m a x }$ be an upper bound of the optimal maximum load $( \mathrm { i . e . , ~ } \lambda _ { m a x } > \lambda ^ { * } )$ , e.g., the sum of maximum execution time of all jobs. A careful implementation of Algorithm 1 can achieve the time complexity of $\begin{array} { r } { O ( L P ( \sum _ { j _ { i } \in \mathcal { I } } | S _ { i } | , | \mathcal { I } | + } \end{array}$ $| \mathcal { M } | ) \cdot \log \lambda _ { m a x } )$ , where $L P ( A , B )$ ( ( +is the time to solve ) log ) ( )a linear programming with A variables and B constraints. Our experiments in Sec. V-C show that SPIN’s scheduling overhead is almost negligible for long-running BSP jobs.

# D. Theoretical Analysis

In this section, we show the performance guarantee of SPIN by deriving its approximation ratio compared with the optimal solution. The proof sketch is as follows

• First, we need to prove the probability of job $j _ { i }$ being placed on $s _ { i k }$ is not impacted by the scheduling of other jobs when SPIN sorts the order of the placements while scheduling.   
• Second, the rounding generated solution will have a maximum load $T _ { m a x }$ whose approximate ratio is $O ( \rho \ln { \frac { | { \mathcal { M } } | } { \delta } } )$ with respect to the optimal maximum load $( \mathrm { i } . \mathrm { e } . , \lambda ^ { * } )$ ) with probability (denoted as w.p. for short) at least $1 - \delta .$ , where δ is a small constant.   
• Third, we prove that the scheduling policy in Algorithm 1 obtains a feasible gang scheduling solution whose makespan is at most $n _ { p } T _ { \mathrm { m a x } }$ .   
max Combining the above, we can finally prove SPIN is $\begin{array} { r } { O ( n _ { p } \rho \ln \frac { | \mathcal { M } | } { \delta } ) } \end{array}$ -approximate $\mathrm { w . p }$ . at least $1 - \delta .$ .

Note that if the job execution times can be accurately estimated (i.e. w.p. $\rho ~ = ~ \frac { \epsilon _ { m a x } } { \epsilon _ { m i n } } ~ = ~ 1 )$ , SPIN is When the e $\begin{array} { r } { O ( n _ { p } \ln \frac { | \mathcal { M } | } { \delta } ) } \end{array}$ -approximatenot accurate, $\ddot { 1 } - \delta$ the approximation ratio of SPIN would at most suffer a factor of $\rho .$ Hence we can say SPIN is robust to the estimation error of job execution time.

Formally, we describe the detailed lemmas as follows. First, it is easy to figure out the distribution of each job’s placement is independent with other jobs under SPIN’s randomized rounding approach.

Lemma 1: Under Algorithm 1, the probability of job $j _ { i }$ being placed on $s _ { i k }$ is independent with the placement of other jobs, i.e., $P r [ Y _ { i } = s _ { i k } ] = P r [ Y _ { i } = s _ { i k } | Y _ { k } ] ~ ( \forall ~ j _ { i } , j _ { k } \in \mathcal { I } _ { : }$ $k \neq i )$ .

= )Then, we analyze the approximation ratio of the maximum load obtained by SPIN in Lemma 2.

Lemma 2: SPIN generates a placement whose maximum load T satisfies $\begin{array} { r } { \bar { T _ { \mathrm { m a x } } } \leq ( 1 + \bar { 2 } \rho \ln { ( \frac { 2 | \mathcal { M } | } { \delta } ) } ) \lambda ^ { * } } \end{array}$ 2|M|δ λ∗ w.p. at least $1 - \delta .$ .

Proof: We first proof the following inequality.

$$
T _ {m a x} \leq \left(1 + 2 \rho \ln (\frac {2 | \mathcal {M} |}{\delta})\right) \lambda^ {*} \quad w. p. \quad 1 - \delta . \tag {8}
$$

Recall the placement policy in Algorithm 1, we first solve the LP in Program 1 and then use randomized rounding to obtain a feasible placement plan. As Program 1 is a linear programming, it can be easily solved optimally with polynomial time complexity. We denote as $x _ { i k } ^ { * } \ ( \forall j _ { i } \in \mathcal { I }$ and $s _ { i k } \in S _ { i } )$ the ( )fractional optimal solution of Program 1. After obtaining $\boldsymbol { x } _ { i k } ^ { * } ,$ the scheduling policy randomly places the job $j _ { i }$ in $s _ { i , k }$ with probability $x _ { i k } ^ { * }$ . We define $T _ { i , l }$ as the random variable of the total aggressive execution time (i.e. $\frac { \hat { p } ( s _ { i , k } ) } { \epsilon _ { m a x } } \big \} )$ -max ) contributed by the job $j _ { i }$ to the server $m _ { l }$ . Thus, the total aggressive execution time of the server ml is $\textstyle \sum _ { j _ { i } \in { \mathcal { I } } } T _ { i , l }$ . The random variable $T _ { i , l }$ has the following properties

• $T _ { i , l }$ :are independent for all job ji;   
• Ti,l ∈ { , ∪si,k i l si,k $\begin{array} { r } { T _ { i , l } \in \{ 0 , \cup _ { s _ { i , k } \in S _ { i } | l \in s _ { i , k } } \frac { \hat { p } \left( s _ { i , k } \right) } { \epsilon _ { m a x } } \} ; } \end{array}$ p si,k -max   
• $\begin{array} { r } { T _ { i , l } = \frac { \hat { p } ( s _ { i , k } ) } { \epsilon _ { m a x } } } \end{array}$ with probability $x _ { i k } ;$   
= -max • The expectation of $\textstyle \sum _ { j _ { i } \in { \mathcal { I } } } T _ { i , l }$ is as follows,

$$
\mathbb {E} \Big [ \sum_ {j _ {i} \in \mathcal {J}} T _ {i, l} \Big ] = \sum_ {j _ {i} \in \mathcal {J}} \sum_ {s _ {i k} \in \mathcal {S} _ {i} | m _ {l} \in s _ {i k}} x _ {i k} ^ {*} \frac {\hat {p} (s _ {i , k})}{\epsilon_ {m a x}},
$$

which is no more than λ∗ due to the constraint (7) in Program 1.

With these properties, we can bound the gap between the total (aggressive) execution time in expectation on each server and its realization after the randomized rounding. We define $\tau$ as a parameter to be fixed latter. If this gap is larger than τ λ on a server, we call the rounding “fails” on this server. Formally, we need to conservatively bound the failing probability for the server ml with the maximum possible job execution time (i.e. $\frac { { \hat { p } } ( s _ { i , k } ) } { \epsilon _ { m i n } } )$ ), which is given as

$$
P r \left[ \frac {\epsilon_ {m a x}}{\epsilon_ {m i n}} \right| \sum_ {j _ {i} \in \mathcal {J}} T _ {i, l} - E [ \sum_ {j _ {i} \in \mathcal {J}} T _ {i, l} ] \bigg | > \tau \lambda^ {*} \bigg ]. \tag {9}
$$

We bound the probability with the following steps,

$$
\begin{array}{l} (9) = P r \left[ \left| \sum_ {j _ {i} \in \mathcal {J}} \frac {T _ {i , l}}{\lambda^ {*}} - E \left[ \sum_ {j _ {i} \in \mathcal {J}} \frac {T _ {i , l}}{\lambda^ {*}} \right] \right| > \frac {\tau}{\rho} \right] \\ \leq 2 \cdot e x p (- \frac {(\tau / \rho) ^ {2}}{2 + (\tau / \rho)}) \\ \leq \frac {\delta}{| \mathcal {M} |}, \tag {10} \\ \end{array}
$$

where $\delta$ is the failure probability. The second inequality is derived from the two-sided Chernoff bound. The last inequality is obtained by substituting $\begin{array} { r } { \tau = 2 \rho \ln { ( \frac { 2 | \mathcal { M } | } { \delta } ) } } \end{array}$ 2|M|δ . By applying the = 2 ln (union bound on each server, we have

$$
\begin{array}{l} P r \left[ \bigcup_ {m _ {l} \in \mathcal {M}} \left(\rho \mid \sum_ {j _ {i} \in \mathcal {J}} T _ {i, l} - E [ \sum_ {j _ {i} \in \mathcal {J}} T _ {i, l} ] \right| > \tau \lambda^ {*}\right) \Bigg ] \\ \leq \sum_ {m _ {l} \in \mathcal {M}} P r \left[ \rho \mid \sum_ {j _ {i} \in \mathcal {J}} T _ {i, l} - E \left[ \sum_ {j _ {i} \in \mathcal {J}} T _ {i, l} \right] \right| > \tau \lambda^ {*} \Bigg ] \\ \leq \delta \tag {11} \\ \end{array}
$$

The inequality (11) indicates the probability is at most $\delta$ that the rounding fails on at least one server. In other words, with probability at least  − δ, the rounding succeeds on 1all servers. Therefore, even when all jobs’ execution time are most underestimated (i.e. $\hat { p } ( s _ { i , k } ) ~ = ~ \epsilon _ { m i n } p ( s _ { i , k } ) ~ \forall i , k )$ , ˆ( ) = ( )the additional execution time brought by the rounding and the estimation error is at most $\tau \lambda ^ { * }$ . Thus, the placement policy is $( 1 + \tau )$ -approximate when the jobs can be executed (1 + )asynchronously, which belongs to $O ( \rho \ln { \dot { \frac { | { \mathcal { M } } | } { \delta } } } )$ . This completes the proof of this lemma. 

Then, in Lemma 3, we bound the gap between the maximum load and the gang scheduling makespan.

Lemma 3: Given a set of $x _ { i k } \ ( \forall i , k )$ whose maximum load is $T _ { m a x } ,$ ( ), Algorithm 1 can gang schedule the jobs with the makespan up to $n _ { p } \cdot T _ { \mathrm { m a x } } .$ .

maxProof: Because the synchronous execution might introduce some idle time intervals on the computing servers, we need to bound the total time of these idle periods on each server.

By fixing a server ml, we denote by $j _ { \pi ( l ) }$ the last job on ( )the server ml with the SPIN’s scheduling policy, where $\pi ( l )$ is its job ID. At any time t before the start of the job $j _ { \pi ( l ) }$ ), there are only three cases

:1) Case 1: the server ml is executing other jobs;   
2) Case 2: the server $m _ { l }$ is idle, but there is at least one server in $Y _ { \pi ( l ) }$ busy.   
( )3) Case 3: all servers in $Y _ { \pi ( l ) }$ are idle.

( )However, with SPIN’s scheduling policy, Case 3 can never happen, because SPIN would start the job $\pi ( l )$ at time t. ( )Thus, with a fixed placement, Algorithm 1 would start the jobs as early as possible.

The makespan on the server $m _ { l }$ is comprised of the total busy time (i.e. Case 1) and the total idle time (i.e. Case 2). According to Case 2, at any idle time t on the server ml, we can find a server $l ^ { \prime }$ busy, which can be defined as a mapping $\boldsymbol { \Lambda _ { l } } ( t ) \ = \ l ^ { \prime }$ . If multiple servers in $Y _ { \pi ( l ) }$ are busy Λ ( ) = ( )at time t, we can pick one of them arbitrarily. We denote by $T _ { l } ^ { i d l e }$ the total idle time on the server $m _ { l }$ , which can be bounded as follows,

$$
\begin{array}{l} T _ {l} ^ {i d l e} = \sum_ {l ^ {\prime} \in Y _ {\pi (l)} | l ^ {\prime} \neq l} \int_ {0} ^ {\infty} \mathbb {1} (\Lambda_ {l} (t) = l ^ {\prime}) d t \\ \leq \sum_ {l ^ {\prime} \in Y _ {\pi (l)} | l ^ {\prime} \neq l} T _ {l ^ {\prime}} \\ \leq \left(\left| Y _ {\pi (l)} \right| - 1\right) T _ {m a x} \\ \leq \left(n _ {p} - 1\right) \cdot T _ {m a x}. \\ \end{array}
$$

Therefore, the idle time on the server $m _ { l }$ is less than $n _ { p } - 1$ times $T _ { m a x }$ 1. Finally, we can bound the makespan of SPIN’s scheduling under synchronous execution

$$
\begin{array}{l} \text { SPIN's   makespan } = \max _ {m _ {l} \in \mathcal {M}} \left(T _ {l} + T _ {l} ^ {i d l e}\right) \\ \leq n _ {p} \cdot T _ {\max} \tag {12} \\ \end{array}
$$

This completes the proof of this lemma.

![](images/894899696912fddebd6d67e32c5037a42dfedb1232617055284c02f77d1c0ceb.jpg)

Finally, by combining the three above lemmas, we can derive the approximation ratio of $\mathrm { S P I N }$ .

Theorem 2: SPIN is $\begin{array} { r }  n _ { p } ( 1 + 2 \rho \ln { ( \frac { 2 | \mathcal { M } | } { \delta } ) } \end{array}$ -approximate w.p. at least $1 - \delta .$ .

1Proof: Denote by $O P T$ the optimal makespan. As the optimal solution of Program 1 uses the aggressive estimation we have $\begin{array} { r } { ( \mathrm { i . e . } \frac { \hat { p } ( s _ { i , k } ) } { \epsilon _ { m a x } } ) } \end{array}$ -max $\bar { \lambda } ^ { \ast } \leq O P T$ and does not consider synchronous execution, . By applying Lemma 2 and Lemma 3, we can bound SPIN’s makespan as follows, w.p.  − δ,

$$
\begin{array}{l} \text { SPIN's   makespan } \leq n _ {p} \cdot T _ {m a x} \leq n _ {p} \left(1 + 2 \ln \left(\frac {2 | \mathcal {M} |}{\delta}\right)\right) \lambda^ {*} \\ \leq n _ {p} \left(1 + 2 \ln \left(\frac {2 | \mathcal {M} |}{\delta}\right)\right) O P T. \tag {13} \\ \end{array}
$$

TABLE II   
THE DURATION OF EXECUTION OF JOBS j1, j2, j3 ON SERVERS m1 AND m2 

<table><tr><td></td><td> $j_1$ </td><td> $j_2$ </td><td> $j_3$ </td></tr><tr><td> $m_1$ </td><td>4.0</td><td>4.0</td><td>3.0</td></tr><tr><td> $m_2$ </td><td>4.8</td><td>4.8</td><td>-</td></tr></table>

Although the approximation ratio in Theorem 2 holds only with a probability, we can boost the success probability in Theorem 2 by executing the rounding operations multiple times (i.e. Line 3−17 in Algorithm 1). By simulating the job execution using their lower bound of real execution time (i.e., $\frac { \hat { p } ( s _ { i k } ) } { \epsilon _ { m a x } } )$ , we can pick the scheduling plan with the minimum makespan. The success probability grows exponentially with the number of repetitions. In other words, SPIN is $n _ { p } ( 1 +$ $2 \rho \ln \big ( \frac { 2 | \mathcal { M } | } { \delta } \big ) \big )$ -approximate w.p. at least $1 - \delta ^ { n }$ (1 +if the rounding 2 ln ( ))is repeated for n times.

Corollary 1: By repeating the randomized rounding (Line $3 - I 7$ in Algorithm 1) multiple times, SPIN is $O ( n _ { p } \rho \ln { | \mathcal { M } | } )$ -approximate with high probability.

( ln )In practice, our experiment shows that the repetitions have little impact on scheduling performance. Even once rounding is often enough to achieve the best performance in our experiments.

The Benefit of Randomized Rounding: We design SPIN as a randomized algorithm instead of a deterministic algorithm because it can improve the performance in expectation.

Here, we show a simple example how the randomized rounding can improve the makespan of scheduling. We assume there are two servers $( m _ { 1 }$ and $m _ { 2 } )$ and three jobs $j _ { 1 } , j _ { 2 } , j _ { 3 } .$ . 1 2 1 2 3Table II shows the execution time of each job on each server. $j _ { 1 }$ and j run faster on m . j can only run on m . When $\lambda \ = \ 6 .$ 2 1 3, the optimal fractional placement is $x _ { 1 1 } ^ { * } =$ $x _ { 2 1 } ^ { * } = 0 . 3 7 5 , x _ { 1 2 } ^ { * } = x _ { 2 2 } ^ { * } = 0 . 6 2 5 , x _ { 3 1 } = 1 . 0$ 11 =. If we use a 21 = 0 375 12 = 22 = 0 625 31 = 1 0deterministic greedy strategy that places the job on the server with the highest $x ^ { * }$ , both $j _ { 1 }$ and $j _ { 2 }$ are placed on $m _ { 2 }$ leading to a makespan of $9 . 6 .$ 1 2. If we randomly place $j _ { 1 }$ and $j _ { 2 }$ following 9the distribution of $x ^ { * }$ 1, the expected makespan is $0 . 3 7 5 ^ { 2 } \times 1 1 +$ $0 . 6 2 5 ^ { 2 } \times 9 . 6 + 0 . 3 7 5 \times 0 . 6 2 5 \times 7 + 0 . 3 7 5 \times 0 . 6 2 5 \times 7 = 8 . 5 7 .$ , 0 625 9 6 + 0 375 0 625 7 + 0 375 0 625 7which is better than the deterministic greedy strategy.

# E. Extensions of SPIN

Batch Scheduling: Although SPIN is an offline solution, we can apply it to schedule online arriving jobs. We pack queuing jobs in the first-in-first-out (FIFO) order to form a batch. When there are enough queuing jobs to fill a batch, we launch SPIN to to minimize the makespan of this batch. As pointed in Firmament [26], scheduling jobs in batches would allow scheduler to jointly consider the job placement to find the best trade-off for the whole batch. Since BSP jobs are usually long-time running, they are not sensitive to the overhead of waiting for other jobs to form a batch. We also set a batch timeout to avoid long time of waiting for enough jobs filling a batch. while the other jobs will stay in the queue to be rescheduled along with the next batches.

For job $j _ { i }$ , which is already running in the cluster, we will add the constraints $x _ { i k } = 1$ in Program 1 to preserve its placement. = 1The occupied computing devices will also be excluded from the available devices in Algorithm 1. Our experiment in Sec. V-C demonstrates the efficiency of our batch scheduling and studies the impact of the batch size.

Exponential Placement Space: In our model, the feasible placements of a job are given and fixed. However, in general cases, the possible placement combinations could theoretically grow exponentially with the number of available computing devices. Fortunately, in most practical scenarios, the choices of placements should be considered based on the type of workload. For deep learning workloads, we first add the strongest affinity (i.e., placing the jobs into the fewest number of servers) to the feasible placement set. During online scheduling, we adaptively add more placements by randomly sampling different combinations of free GPUs in our cluster. 5 Randomly sampling the placements can further help balance the load of a cluster. For each job, the placement sampling only affects which combinations of servers are available in $s _ { i } ,$ but does not decide which one to use. SPIN will globally optimize the makespan when picking the placement for each job by considering the trade-off between the execution time and the queuing delay. We find this approach works well in our experiments. Sec. V-C also shows a sensitivity study on the randomly sampled placements.

Algorithm 2 Extension to Migration & Preemption   
1 Define $\mathcal{J}_q$ and $\mathcal{J}_r$ as the queuing and running jobs, respectively.
2 $\mathcal{J} = \mathcal{J}_q \cup \mathcal{J}_r$ .
3 $\forall j_i \in \mathcal{J}_r$ , define $p^*(s_{sik})$ as the estimated remaining execution time of job $j_i$ .
4 $\forall m_l \in \mathcal{M}$ $T_l^{queuing} = \sum_{j_i \in \mathcal{J}_q} \sum_{\substack{s_{ik} \in \mathcal{S}_i (\leq \lambda) \\ s.t.m_l \in s_{ik}}} x_{ik} \frac{\hat{p}(s_{ik})}{\epsilon_{max}}$ 5 $\forall j_i \in \mathcal{J}_r$ , define $\omega_i(s_{ik})$ as the migration overhead to execute the job $i$ on $s_{ik}$ ( $\omega_i(s_{ik}) = 0$ if $s_i$ is already running on $s_{ik}$ ).
6 $\forall m_l \in \mathcal{M}$ $T_l^{running} = \sum_{j_i \in \mathcal{J}_r} \sum_{\substack{s_{ik} \in \mathcal{S}_i (\leq \lambda) \\ s.t.m_l \in s_{ik}}} x_{ik} \left( \frac{\hat{p}^*(s_{ik})}{\epsilon_{max}} + \omega_i(s_{ik}) \right)$ 7 Execute Algorithm 1 by replacing Program 1 to the following program:
Program 2:

$L P ( \lambda )$

s.t. ,

Min

$$
\forall j _ {i} \in \mathcal {J}, s _ {i k} \in \mathcal {S} _ {i} (\leq \lambda)
$$

$$
T _ {l} ^ {\text { queuing }} + T _ {l} ^ {\text { running }} \leq \lambda \quad \forall m _ {l} \in \mathcal {M}
$$

8 Preempt all jobs in $\mathcal { I } _ { r }$ + but not placed at time  in Line 7.   
9 Migrate all jobs in $\mathcal { I } _ { r }$ 0whose placement in Line 7 is different from the current one.   
10 Schedule jobs in $\mathcal { I } _ { q }$ placed at time  in Line 7.

Incorporating Migration and Preemption: Although we focus on the non-preemptive scheduling here, our method can

5When sampling the placements, we randomly choose the free GPUs to form each placement. If a placement is already in a job’s feasible placement set, we drop it and re-sample the GPUs until a new one is found.

TABLE III PREEMPTION OVERHEAD OF RUNNING THE JOB j4 ON SERVERS m1, m2, m3 

<table><tr><td></td><td> $m_1$ </td><td> $m_2$ </td><td> $m_3$ </td></tr><tr><td>Remaining Time</td><td>3</td><td>3</td><td>1</td></tr><tr><td>Preemption Overhead</td><td>1</td><td>10</td><td>3</td></tr><tr><td>Execution Time of  $j_4$ </td><td>10</td><td>1</td><td>3</td></tr></table>

be extended to support on-demand preemption or migration, i.e., interrupting a job or changing its placement when its processing has already started. Since off-the-shelf deep learning frameworks (e.g., Tensorflow, PyTorch) do not support a low-overhead migration, our extension considers the scenarios that preemption/migration incurs not frequently, e.g., the high-priority job can preempt low-priority jobs. The migration/preemption overhead should be incorporated in SPIN. During online batch scheduling, SPIN can simply add a job into the scheduling batch if it is migrated/preempted. If the job remains on the placement currently running on, its execution time would be the same as previously estimated. Otherwise, its execution time on other placements should be added with the migration/preemption cost due to the overhead and the potential loss of job progress.

Algorithm 2 elaborates the extension of SPIN to support migration and preemption. SPIN treats the queuing jobs as the same as Algorithm 1, whose increase of execution time on machine $m _ { l }$ is defined in Line 4. For the running jobs, we need to consider the impact of migration. For the placement different from a running job’s current placement, it will be preempted and restarted on the new placement. We calculate the migration overhead by considering the loss due to non-checkpointed progress and restarting overhead (Line 5–Line 6). By replacing the constraint of Program 1 to incorporate the cost of migration, we apply Algorithm 1 to get the new scheduling plan (Line 7). Preemption, migration, scheduling actions are executed according to the newly generated scheduling plan (Line 8–Line 10).

Table III shows an example of three servers, each running a low-priority job. For simplicity, we assume these low-priority jobs have the same speed on the three servers. Then, a new high-priority job $j _ { 4 }$ arrives that needs to preempt one of 4low-priority jobs for execution. Although running $j _ { 4 }$ on m or $m _ { 2 }$ has the lowest preemption overhead or execution time, 2respectively, the optimal decision should place $j _ { 4 }$ on $m _ { 3 }$ with a preemption overhead of . The optimal makespan is the sum of the execution time of $j _ { 4 } ,$ , the preemption overhead, and the 4remaining time of the preempted job, which is $3 + 3 + 1 = 7 .$

Note that, the preemption in SPIN is trigger in a low frequency only when high-priority jobs need to preempt low-priority jobs. It is interesting to study the problem of leveraging low-overhead migration to schedule certain types of BSP jobs (e.g., Tiresias [27] for deep learning jobs), which we leave for future work.

![](images/efd5f3d4b5f119c2101afb13e59297a06468574954895e1e6f14f36f3fbfe3c4.jpg)



(a) Cluster Efficiency

![](images/7c08aff76d28daf177ed83974d6485564d6f31120f047f79576dff54299484b8.jpg)



(b）Average Job Completion Time

![](images/22b53d8ae6dc15a96b3870fcacac780a39ac913da7716e9698e15d8c9ff06bf7.jpg)



(c)Distribution of individual job completion time   
Fig. 4. Improvements on the job completion time and cluster efficiency using SPIN compared with TETRIS, Optimus and GREEDY.

# V. PERFORMANCE EVALUATION

We have implemented SPIN on top of Kubernetes 1.9.4 [14]. We evaluate SPIN using experiments in a 40-GPU testbed and large-scale simulations driven by Microsoft’s production trace of deep learning training [15]. Overall, our key findings are

In the testbed experiments, SPIN reduces the makespan (and the average job completion time) by up to . × 4 68(and up to ×) compared with the state-of-the-art big-data scheduler.   
SPIN is robust to the misestimation of the execution time:  jobs are not affected and  jobs are affected 60% 40%by less than  on the change of job completion time.   
50%• Our extensive experiments show that SPIN is robust to various workload and parameter variations.   
• SPIN’s scheduling overhead is negligible to long-running BSP jobs like distributed deep learning training.

# A. Experimental Setup

Testbed: To evaluate SPIN in real deployment, we conduct experiments in a GPU cluster testbed. Our testbed contains 10 servers, each with NVIDIA P100 GPUs (40 GPUs in 4total). Each server has a 12-core Intel Xeon E5-2690@2.6GHz with two 40 Gbps network links, running Ubuntu 16.04.

Workloads: We adopt Microsoft’s production trace of online arriving deep learning training jobs [15]. As stated in Sec. IV-E, SPIN schedules the online arriving jobs in batches (by default, we set the batch size to jobs and the batch 10time-out to minutes.). Since the trace does not provide model 5information, we use a common approach in existing literature (e.g., [17], [22], [27]) to replace them using 11 popular deep learning models (Table IV) in the domains of Natural Language Processing (NLP), Speech, and Computer Vision (CV). The number of jobs in these three domains follows a distribution of 6:3:1 [17]. A job’s training time under its best placement follows the distribution shown in Fig. 5. We measure the iteration time of each model and decide the number of mini-batches to match the execution time in the trace. All models are trained in synchronous data parallelism mode in Tensorflow 1.5. Distributed training uses parameter servers for synchronizing weights. For the jobs demanding more than one GPU, they can be executed in a distributed manner spanning multiple servers. We scale the workloads to fit our cluster size: there are 240 1-GPU jobs, 40 2-GPU jobs, 80 4-GPU jobs, 90 8-GPU jobs, and 20 16-GPU jobs.

![](images/93e5fcb29542aebf31de3fc1e6dea5e1189cb4722a7d6e920df790875040069e.jpg)



Fig. 5. Distribution of the job execution time in the production trace.

TABLE IV NEURAL NETWORK MODELS, DATASETS, AND THEIR FRACTIONS 

<table><tr><td>Fraction</td><td>Neural Network Model</td><td>Type</td><td>Dataset</td></tr><tr><td rowspan="4">10%</td><td>InceptionV3 [28]</td><td>CV</td><td>ImageNet [29]</td></tr><tr><td>ResNet-50 [19]</td><td>CV</td><td>ImageNet</td></tr><tr><td>Alexnet [30]</td><td>CV</td><td>ImageNet</td></tr><tr><td>VGG16 [18]</td><td>CV</td><td>ImageNet</td></tr><tr><td rowspan="4">60%</td><td>Bi-Att-Flow [31]</td><td>NLP</td><td>SQuAD [32]</td></tr><tr><td>Language Model [33]</td><td>NLP</td><td>PTB [34]</td></tr><tr><td>GNMT [35]</td><td>NLP</td><td>WMT16 [36]</td></tr><tr><td>Transformer [37]</td><td>NLP</td><td>WMT16</td></tr><tr><td rowspan="2">30%</td><td>Wavenet [38]</td><td>Speech</td><td>VCTK [39]</td></tr><tr><td>DeepSpeech [40]</td><td>Speech</td><td>CommonVoice [41]</td></tr></table>

Fast-forwarding: To speed up the execution of experiments, we follow the same approach as Gandiva [17] using fastforwarding. We leverage the predictability of machine learning training by estimating a job’s finish time using its training speed (i.e., training time ≈ # of mini-batchesthe average training time per mini-batch ). To mitigate measurement variance due to the warm-up issues, a job’s training speed is only collected when it reaches a stable state. A partial number of training steps will be skipped when there are no scheduling events including job arrival and completion. A model’s training speed under a type of placement will be cached so that, when a future job of the same model runs under the placement with the same GPU topology, we will use the cached training speed instead. This fast-forwarding method has a high fidelity that the difference between real and fast-forwarded experiments is within 7%.

Cluster Scheduler: Each worker of a job, as well as a central cluster scheduler, runs as a container managed by Kubernetes. We implement SPIN and the baseline algorithms in the central cluster scheduler, which can directly use Kubernetes API to get the information of cluster nodes and containers. Our simulator is built on the same central cluster scheduler, which injects simulated events to the scheduler instead of running jobs using real servers.

Performance model: To estimate the execution time of distributed deep learning jobs under different placements, we adopt non-negative least square (NLSS) regression-based approach similar to [22], [42], [43]. We build a linear model as follows

$$
\begin{array}{l} \text { time\_per\_iteration } = c _ {0} + \frac {c _ {1}}{\text { PCIeBW }} \\ + c _ {2} \times \frac {1 - 1 / n _ {\text { server }}}{\text { NetBw }} + c _ {3} \times n _ {\text { max\_worker }}, \\ \end{array}
$$

where PCIeBW is the PCIe bandwidth of a GPU slot, NetBW is the bandwidth of a server NIC, $n _ { \mathrm { s e r v e r } }$ is the number of server in a job’s placement, $n _ { \mathrm { m a x \_ w o r k e r } }$ is the number of workers in the server with most workers, and $c _ { 0 } , c _ { 1 } , c _ { 2 } , c _ { 3 }$ 0 1 2 3are the values to be learned to fit the performance model curve. We sample 10 placements for each job, each runs for 100 mini-batches (about 10-100s for each run). The multiple runs can be executed in parallel. Since the deep learning models usually runs for a long time (usually several hours), the profiling overhead of building the performance model is negligible. Our evaluation shows this method has $\leq ~ 1 5 \%$ estimation error for the models in Table IV.

Baselines: We compare SPIN with two representative job scheduling policies

:• TETRIS-MAKESPAN [23]: the state-of-the-art scheduling algorithm to pack multi-resource tasks for big-data analytic workloads. It calculates placement quality using the dot product of each task’s resource demand and the remaining resource on each server, and place a job to the server with the highest placement quality.   
GREEDY: it is a heuristic strawman algorithm trying to minimize the average job completion time. It places a job to the best placement (the one with the shortest execution time) currently available in the cluster. Within a batch of queuing jobs, it schedules jobs like the shortest-job-first policy by first scheduling the job with the least execution time.   
• OPTIMUS [22]: it is a scheduler designed for deep learning training jobs, which supports gang-scheduling. We implement its job scheduling policy that sorts the jobs in increasing order of their resource demand and schedules the smallest job first.6 It always chooses the placement with the least number of servers.

In this work, since we mainly focus on non-preemptive scheduling, we do not include Gandiva [17] or Tiresias [27] as baselines. Both of them heavily adopt job preemption. To avoid the heavy preemption overhead (e.g., the loss of work due to coarse-grained checkpointing), we need to conduct system modification to machine learning frameworks, which will be considered as our future work.

# B. Testbed Experiments

Improvement on JCT and Cluster Efficiency: Fig. 4(a) shows the cluster efficiency (i.e., the makespan of all jobs)

6Although, Optimus has a performance model to predict the number of workers to use, in our problem setting, the number of worker is given as the input in each job’s placements.

![](images/14dd9f629e4677a69f0bd5dc11c8338be950454556253de944b513938b9c682f.jpg)



(a) Distribution of job queuing time

![](images/8931dbbb1afee054ccfb4c5a162c4ee7085daf5c3f7afe246ebea76a3fd77e91.jpg)



(b） Improvement on execution time   
Fig. 6. Dissecting the improvement from queuing delay and execution time.

of the three algorithms. SPIN provides higher cluster efficiency over TETRIS-MAKESPAN by ×, OPTIMUS by . × 3 1 42and GREEDY by . ×, respectively. TETRIS-MAKESPAN 1 26has the lowest cluster efficiency is mainly due to its unawareness of placement-sensitivity, thus it could schedule a placement-sensitive job to multiple servers that lead to poor training speed then waste the expensive GPUs.

Fig. 4(b) shows the average job completion time (JCT) of the three algorithms. As shown in Fig. 4(b), SPIN achieves $4 . 6 8 \times , ~ 3 . 6 7 \times$ , and . × improvement on the average 4 68 3 67 2 04JCT over TETRIS-MAKESPAN, OPTIMUS and GREEDY, respectively. TETRIS-MAKESPAN was designed for big-data analytic workloads that a job usually contains a large number of small tasks, which do not require gang scheduling. However, TETRIS-MAKESPAN’s scheduling disciplines do not fit the requirement of deep learning training jobs, which has placement-sensitive training performance and needs stringently gang-scheduled resources. GREEDY is aware of the placement-sensitivity thus performs better than TETRIS-MAKESPAN. But its greedy policy could place a job to sub-optimal resources when the cluster is fragmented. OPTI-MUS always wait for the placement with the least number of servers, which also leads to sub-optimal decisions. SPIN is the most efficient by solving an optimization that can jointly consider the placement-dependent performance and the impact of gang scheduling. As shown in Fig. 4(c), SPIN has the strictly better distribution than the two baselines that proves SPIN is the most efficient. It implies that optimizing makespan in a batch is also helpful for reducing individual job completion time.

Next, we investigate the details of the experiments to study why SPIN can achieve better performance.

Dissecting Improvement: We dissect a job’s JCT by showing its two components: job queuing delay (i.e., job scheduling time - job arrival time) and job execution time (i.e., job completion time - job scheduling time). Fig. 6(a) shows the distribution of the queuing delay. Using SPIN, there are 40% jobs scheduled almost instantly. Because of the higher cluster efficiency, SPIN can create more free resources earlier so that the latter arrived jobs can have more choices of placements and start earlier.

Fig. 6(b) depicts the factor of improvement of SPIN over the two baselines on the job execution time. About  of the 80%jobs have the same execution time under the three algorithms.

![](images/d2577f4d8b1837bab6c4a32033b7f3f8a21c4fa724dcadc74e4cffefecc9faa3.jpg)



Fig. 7. The distribution of the change of job completion time (JCT) with various schedulers when the execution times are misestimated.

They are mostly 1-GPU jobs. About  of jobs run slower in the two baselines algorithms compared with SPIN. The factor of improvement varies from . × to . ×. These slower jobs 1 0 3 5are mainly large jobs (demanding many GPUs) with longer training time. Therefore, the slowdown of these large jobs will severely degrade the cluster efficiency that further postpones the start of future jobs.

Impact of Estimation Error: As proven in Theorem 2, SPIN is robust to the misestimation error on job execution time. In the worst case, the impact of the misestimation error on the makespan is up to ρ, which is the ratio of estimation error bounds. To evaluate the impact of estimation error, we adopt a common evaluation approach [8] that add random distortion on the execution time to the algorithms’ inputs. Fig. 7 shows the CDF of the change in JCT under different ranges of misestimation. An error range of low  high means a job’s estimated execution time is uniformly distributed within low,   high × (its real execution time).

\+ 1 + ]Both TETRIS-MAKESPAN and OPTIMUS are not affected by the misestimation since it does not leverage a job’s execution time when making scheduling decisions (the distribution of OPTIMUS is same as TETRIS-MAKESPAN thus we skip it due to limited spaced). GREEDY is heavily affected since the misestimated execution time will mislead the scheduling order and placement according to its scheduling discipline. SPIN is more robust to the misestimation that ∼  of jobs are not 60%affected. The misestimation only changes the JCT by less than ∼  on the affected jobs. This is because SPIN is aware 50%of the estimation error and its scheduling decisions are only affected by -max.

# C. Sensitivity Analysis

To investigate SPIN on a production-level cluster size, and the impact of various factors, we conduct more simulations on a cluster of 600 GPUs (150 4-GPU servers). The workloads are changed adaptively to fit the cluster size.

Impact of Contention: In order to study SPIN’s performance under contented clusters, we increase the contention level by reducing the number of GPUs in the cluster. A × 2contention level means we reduce the number of GPUs by half. Fig. 8 shows the factor of improvement on the average JCT under different contention levels. The improvement on the makespan has a similar phenomenon thus we omit them due to space limitation. When the contention level reaches ×, 6SPIN achieves an improvement of . ×, . ×, and . × compared with GREEDY OPTIMUS, and TETRIS-MAKESPAN, respectively. Under a heavier contention, SPIN will be more careful to find the trade-off between the queuing delay and the execution time.

![](images/4fea2b6b5004b19be69cc4cfe17e3faaeb2c203ed71945f7b2146f855e5be096.jpg)



Fig. 8. [Simulation] SPIN’s improvement on the average JCT over the baselines under varying contention level.

![](images/4c9d5ccbc7f37f6769f51d51c94255900dea95ce654e620f8be0cb8e153fe94b.jpg)



Fig. 9. [Simulation] SPIN’s improvement on the average JCT over the baselines under varying batch size.

Impact of Batch Scheduling: As we have stated in Sec. IV-E, we batch a set of jobs when applying SPIN to schedule the online arriving jobs. Fig. 9 shows the impact of the batch size (i.e., the number of jobs in each batch) on SPIN’s improvement on the average JCT. SPIN has the best performance when the batch size is 10 jobs. When the batch size is greater than 10, the performance becomes slightly worse. This is a trade-off because large batch size can optimize job scheduling with more information but could increase the queuing delay when waiting for enough jobs to fill a batch.

The setting of batch size is a trade-off because a large batch size can better optimize job scheduling with more information but could increase the queuing delay when waiting for enough jobs to fill a batch. In practice, different clusters with different kinds of workloads have different tolerance on queuing delay. Therefore, when most jobs are short, a small batch size is necessary; while for clusters with jobs of long running time, a large batch size can bring better performance with little negative impact.

Impact of Placement Sampling: For some workloads, their placements are not given as an input. Instead, they may specify a structure defining what types of placement are feasible (e.g., any  GPUs in a cluster of 4-GPU servers). It is possible that 8the structure has exponentially growing number of placements. To deal with the exponential placement space, SPIN first adds all placements of the strongest affinity (i.e., the placement with the least number of servers), and then randomly samples more placements in a uniform distribution, which together forms a job’s placement set. Fig. 10 shows the impact of the number of randomly sampled placements on the average JCT. We find the performance is barely affected with more randomly sampled placements. This is because distributed deep learning jobs are usually sensitive to placement. Most jobs are placed on the placement of the strongest affinity to achieve the best training speed. Using other placement not only degrades training speed but also makes the cluster fragmented. Therefore, more randomly sampled placements other than the strongest affinity are barely considered by SPIN.

![](images/a28caaa1cf805c89cc6c9cf845b718e6b55f6a8ab50a25068459f0ad32ca04ac.jpg)



Fig. 10. [Simulation] The impact of placement sampling.   
![](images/7ce793e14ba4102b56da8d286c8839d533a84a1bf60e9504e9988bcd6d73152f.jpg)



Fig. 11. [Simulation] Scheduling overhead under different cluster size.

Scheduling Overheads: SPIN’s scheduling overhead grows linearly with the cluster size. Under a large production-scale GPU cluster (a 1280-GPU cluster), SPIN can make the scheduling decisions within 1.2 seconds per job. The scheduling overhead is almost negligible for long-running BSP jobs, which usually run for many minutes or even hours. However, SPIN is not suitable for scheduling short-running latency-sensitive jobs, which only run for several seconds or even shorter, e.g., machine learning inference.

# VI. RELATED WORK

Schedulers for Big-data Analytics: Big-data analytic frameworks usually employ cluster resource manager, e.g. Mesos [44] and YARN [45], to schedule jobs with different objectives. Dominant Resource Fairness (DRF) [6] aims to provide instantaneous fairness on multi-dimensional resources. Tetris [7] was proposed to increase efficiency and server utilization. Graphene [8] focuses on scheduling jobs with DAG task dependency. QOOP [9] dynamically changes the query plan as reaction to resource changes. Chen et al. [46] studied the fair scheduling of the performance-aware big-data analytic job by exploiting demand elasticity. These works focused on scheduling big-data analytic jobs, which do not require gangscheduling. Our proposed algorithm is for gang-scheduling, which is the stringent requirement of BSP jobs.

Schedulers for Deep Learning: Gang scheduling of placement-sensitive deep learning training jobs has been studied recently. Gandiva [17] proposed four scheduling primitives for deep learning training: time-slicing, migration, growthshrink, and packing. Tiresias [27] heavily relies on the job preemptions to decide the scheduling orders of jobs to minimize the job completion time for deep learning jobs with partial or no a priori knowledge on the job execution time. SPIN is compatible with these works by combining with them to achieve better cluster efficiency. As discussed in Sec. IV-E, SPIN can be incorporated with (Gandiva’s) migration/preemption. Tiresias can be used to first decide the scheduling order and then let SPIN decide the job placement. Optimus [22] builds performance models to help the scheduler to adjust resource allocation and estimate the job execution time, which could be helpful to decide the inputs of SPIN.

Schedulers for HPC jobs: Gang scheduling is the representative requirement of parallel applications in High Performance Computing (HPC) [47]–[49]. Collette et al. [47] studied the gang scheduling problem with deadline sporadic jobs in identical parallel processors. Kato and Ishikawa [48] applied the Earliest Deadline First (EDF) policy to gang scheduling with real-time jobs. Saifullah et al. [49] extended the EDF policy to schedule parallel jobs with a directed acyclic graph (DAG) dependency. However, the gang-scheduling solutions in HPC do not need to consider placement-sensitivity since the computing devices in HPC are usually homogeneous.

Performance Prediction Techniques: Estimating job performance under different placements can help the scheduler to derive the best placement and scheduling decision. A series of performance prediction approaches have been proposed recently for big-data analytics [43], [50], [51] and machine learning applications [22], [52], [53]. SPIN is built upon these performance prediction techniques using the estimated placement-sensitive execution time to make the scheduling decision. Since there is no perfect performance prediction technique that can accurately estimate the job execution time, we design SPIN to be robust to the misestimation so that the negative impact of estimation errors can be bounded.

Scheduling with Inexact Job-size Information: When the job-size information cannot be accurately estimated, many works have studied scheduling under different assumptions. When the distribution of job size is highly skewed, e.g., most jobs are short, Least Attained Service (LAS) [54] or multi-level priority queues [55] can perform well when job-size information is unknown. Wierman and Nuyens [56] generalized the heuristic policies of “favoring small jobs” using inexact job-size information. PSBS [57] generalized fair sojourn protocol (FSP) [58], a fair and efficient size-based scheduling policy, to handle inexact job-size information. Most of these works focus on preemptive scheduling that makes the problem easier than the non-preemptive as a scheduler can timely preempt a job when the job-size information is misestimated. Also, they only considered single-server or big-data analytic jobs without the constraints of gang-scheduling or the placement sensitivity.

# VII. CONCLUSION

In this paper, we study scheduling Bulk Synchronous Parallel (BSP) jobs with placement-sensitivity and inaccurately estimated execution times. We first prove the approximation-hardness of the problem. Then, we propose our novel algorithm, named SPIN, which is $O ( n _ { p } \rho \cdot \ln | \mathcal { M } | ) .$ - approximate. We implement SPIN on Kubernetes [14] and conduct extensive experiments on a testbed cluster with

40 NVIDIA P100 GPUs. Production-trace-driven experiments and large-scale simulations show that SPIN can be robust to the misestimation while dramatically increasing the cluster efficiency and reducing the job completion time. As discussed in Sec. IV-E, our system model assumes the feasible placements for each job are given as input information. It is an interesting open problem to study how to efficiently express and explore placement sensitivity in a more general setting in a large cluster.

# REFERENCES

[1] Z. Han, H. Tan, S. H.-C. Jiang, X. Fu, W. Cao, and F. C. M. Lau, “Scheduling placement-sensitive BSP jobs with inaccurate execution time estimation,” in Proc. IEEE INFOCOM, Jul. 2020, pp. 1053–1062.   
[2] M. Abadi et al., “TensorFlow: A system for large-scale machine learning,” in Proc. OSDI, 2016, pp. 265–283.   
[3] A. Kyrola, G. Blelloch, and C. Guestrin, “GraphChi: Large-scale graph computation on just a PC,” in Proc. OSDI, 2012, pp. 31–46.   
[4] N. P. Jouppi et al., “In-datacenter performance analysis of a tensor processing unit,” in Proc. ISCA, 2017, pp. 1–12.   
[5] D. G. Feitelson and L. Rudolph, “Gang scheduling performance benefits for fine-grain synchronization,” J. Parallel Distrib. Comput., vol. 16, no. 4, pp. 306–318, Dec. 1992.   
[6] A. Ghodsi, M. Zaharia, B. Hindman, A. Konwinski, S. Shenker, and I. Stoica, “Dominant resource fairness: Fair allocation of multiple resource types,” in Proc. NSDI, 2011, p. 24.   
[7] R. Grandl, G. Ananthanarayanan, S. Kandula, S. Rao, and A. Akella, “Multi-resource packing for cluster schedulers,” ACM SIGCOMM Comput. Commun. Rev., vol. 44, no. 4, pp. 455–466, Feb. 2015.   
[8] R. Grandl, S. Kandula, S. Rao, A. Akella, and J. Kulkarni, “GRAPHENE: Packing and dependency-aware scheduling for dataparallel clusters,” in Proc. OSDI, 2016, pp. 81–97.   
[9] K. Mahajan, M. Chowdhury, A. Akella, and S. Chawla, “Dynamic query re-planning using QOOP,” in Proc. OSDI, 2018, pp. 253–267.   
[10] R. Grandl, M. Chowdhury, A. Akella, and G. Ananthanarayanan, “Altruistic scheduling in multi-resource clusters,” in Proc. OSDI, 2016, pp. 65–80.   
[11] K. Shvachko, H. Kuang, S. Radia, and R. Chansler, “The Hadoop distributed file system,” in Proc. MSST, vol. 10, May 2010, pp. 1–10.   
[12] M. Zaharia, M. Chowdhury, M. J. Franklin, S. Shenker, and I. Stoica, “Spark: Cluster computing with working sets,” HotCloud, vol. 10, no. 10, p. 95, Jun. 2010.   
[13] K. Ousterhout, R. Rasti, S. Ratnasamy, S. Shenker, and B.-G. Chun, “Making sense of performance in data analytics frameworks,” in Proc. NSDI, 2015, pp. 293–307.   
[14] B. Burns, B. Grant, D. Oppenheimer, E. Brewer, and J. Wilkes, “Borg, omega, and kubernetes,” Queue, vol. 14, no. 1, pp. 70–93, 2016.   
[15] M. Jeon, S. Venkataraman, A. Phanishayee, J. Qian, W. Xiao, and F. Yang, “Analysis of large-scale multi-tenant GPU clusters for DNN training workloads,” in Proc. USENIX ATC, 2019, pp. 947–960.   
[16] H. Zhang et al., “Poseidon: An efficient communication architecture for distributed deep learning on GPU clusters,” in Proc. USENIX ATC, 2017, pp. 181–193.   
[17] W. Xiao et al., “Gandiva: Introspective cluster scheduling for deep learning,” in Proc. OSDI, 2018, pp. 595–610.   
[18] K. Simonyan and A. Zisserman, “Very deep convolutional networks for large-scale image recognition,” 2014, arXiv:1409.1556. [Online]. Available: http://arxiv.org/abs/1409.1556   
[19] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in Proc. CVPR , Jun. 2016, pp. 770–778.   
[20] Support Gang Scheduling in the AM RM Protocol. Accessed: Jul. 24, 2019. [Online]. Available: https://jira.apache.org/ jira/browse/YARN-624   
[21] Q. Ho et al., “More effective distributed ML via a stale synchronous parallel parameter server,” in Proc. NIPS, 2013, p. 1223.   
[22] Y. Peng, Y. Bao, Y. Chen, C. Wu, and C. Guo, “Optimus: An efficient dynamic resource scheduler for deep learning clusters,” in Proc. EuroSys, Apr. 2018, pp. 1–14.   
[23] R. Grandl, G. Ananthanarayanan, S. Kandula, S. Rao, and A. Akella, “Multi-resource packing for cluster schedulers,” ACM SIGCOMM Comput. Commun. Rev., vol. 44, no. 4, pp. 455–466, Feb. 2015.   
[24] L. A. Hall and D. B. Shmoys, “Approximation schemes for constrained scheduling problems,” in Proc. IEEE FOCS, Oct. 1989, pp. 134–139.

[25] S. Khot, “Improved inapproximability results for MaxClique, chromatic number and approximate graph coloring,” in Proc. IEEE FOCS, Oct. 2001, pp. 600–609.   
[26] I. Gog, M. Schwarzkopf, A. Gleave, R. N. Watson, and S. Hand, “Firmament: Fast, centralized cluster scheduling at scale,” in Proc. OSDI, 2016, pp. 99–115.   
[27] J. Gu et al., “Tiresias: A GPU cluster manager for distributed deep learning,” in Proc. NSDI, 2019, pp. 485–500.   
[28] C. Szegedy, V. Vanhoucke, S. Ioffe, J. Shlens, and Z. Wojna, “Rethinking the inception architecture for computer vision,” in Proc. CVPR , Jun. 2016, pp. 2818–2826.   
[29] J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. Fei-Fei, “ImageNet: A large-scale hierarchical image database,” in Proc. CVPR, Jun. 2009, pp. 248–255.   
[30] A. Krizhevsky, I. Sutskever, and G. E. Hinton, “ImageNet classification with deep convolutional neural networks,” in Proc. NIPS, 2012, pp. 1097–1105.   
[31] M. Seo, A. Kembhavi, A. Farhadi, and H. Hajishirzi, “Bidirectional attention flow for machine comprehension,” 2016, arXiv:1611.01603. [Online]. Available: http://arxiv.org/abs/1611.01603   
[32] P. Rajpurkar, J. Zhang, K. Lopyrev, and P. Liang, “SQuAD: 100,000+ questions for machine comprehension of text,” 2016, arXiv:1606.05250. [Online]. Available: http://arxiv.org/abs/1606.05250   
[33] W. Zaremba, I. Sutskever, and O. Vinyals, “Recurrent neural network regularization,” 2014, arXiv:1409.2329. [Online]. Available: http://arxiv. org/abs/1409.2329   
[34] M. Marcus, B. Santorini, and M. A. Marcinkiewicz, “Building a large annotated corpus of English: The Penn Treebank,” Comput. Linguistics, vol. 19, no. 2, Jun. 1993. [Online]. Available: https://dl.acm.org/doi/10.5555/972470.972475   
[35] Y. Wu et al., “Google’s neural machine translation system: Bridging the gap between human and machine translation,” 2016, arXiv:1609.08144. [Online]. Available: http://arxiv.org/abs/1609.08144   
[36] WMT16 Dataset. Accessed: Aug. 12, 2016. [Online]. Available: http://www.statmt.org/wmt16/   
[37] A. Vaswani et al., “Attention is all you need,” in Proc. Adv. Neural Inf. Process. Syst., 2017, pp. 5998–6008.   
[38] A. van den Oord et al., “WaveNet: A generative model for raw audio,” 2016, arXiv:1609.03499. [Online]. Available: http://arxiv. org/abs/1609.03499   
[39] C. Veaux et al., “CSTR VCTK corpus: English multi-speaker corpus for CSTR voice cloning toolkit,” Univ. Edinburgh., Centre Speech Technol. Res., Edinburgh, Scotland, Tech. Rep., 2017. [Online]. Available: https://datashare.ed.ac.uk/handle/10283/3443, doi: 10.7488/ds/2645.   
[40] A. Hannun et al., “Deep speech: Scaling up end-to-end speech recognition,” 2014, arXiv:1412.5567. [Online]. Available: http://arxiv.org/ abs/1412.5567   
[41] Common Voice Dataset. Accessed: Oct. 8, 2018. [Online]. Available: https://voice.mozilla.org/   
[42] W. Xiao et al., “Scheduling CPU for GPU-based deep learning jobs,” in Proc. ACM Symp. Cloud Comput., Oct. 2018, p. 503.   
[43] S. Venkataraman, Z. Yang, M. Franklin, B. Recht, and I. Stoica, “Ernest: Efficient performance prediction for large-scale advanced analytics,” in Proc. NSDI, 2016, pp. 363–378.   
[44] B. Hindman et al., “Mesos: A platform for fine-grained resource sharing in the data center,” in Proc. NSDI, 2011, p. 22.   
[45] V. K. Vavilapalli et al., “Apache Hadoop YARN: Yet another resource negotiator,” in Proc. SoCC, Oct. 2013, pp. 1–16.   
[46] C. Chen, W. Wang, and B. Li, “Performance-aware fair scheduling: Exploiting demand elasticity of data analytics jobs,” in Proc. IEEE INFOCOM, Apr. 2018, pp. 504–512.   
[47] S. Collette, L. Cucu, and J. Goossens, “Integrating job parallelism in real-time scheduling theory,” Inf. Process. Lett., vol. 106, no. 5, pp. 180–187, May 2008.   
[48] S. Kato and Y. Ishikawa, “Gang EDF scheduling of parallel task systems,” in Proc. IEEE RTSS, Dec. 2009, pp. 459–468.   
[49] A. Saifullah, K. Agrawal, C. Lu, and C. Gill, “Multi-core realtime scheduling for generalized parallel task models,” in Proc. RTSS, Nov. 2011, pp. 217–226.   
[50] A. Verma, L. Cherkasova, and R. H. Campbell, “ARIA: Automatic resource inference and allocation for mapreduce environments,” in Proc. ACM ICAC, 2011, pp. 235–244.   
[51] O. Alipourfard, H. H. Liu, J. Chen, S. Venkataraman, M. Yu, and M. Zhang, “CherryPick: Adaptively unearthing the best cloud configurations for big data analytics,” in Proc. NSDI, 2017, pp. 469–482.

[52] M. Amaral, J. Polo, D. Carrera, S. Seelam, and M. Steinder, “Topologyaware GPU scheduling for learning workloads in cloud environments,” in Proc. Int. Conf. High Perform. Comput., Netw., Storage Anal., Nov. 2017, p. 17.   
[53] Q. Chen, H. Yang, M. Guo, R. S. Kannan, J. Mars, and L. Tang, “Prophet: Precise QoS prediction on non-preemptive accelerators to improve utilization in warehouse-scale computers,” ACM SIGOPS Oper. Syst. Rev., vol. 51, no. 2, pp. 17–32, Apr. 2017.   
[54] I. A. Rai, G. Urvoy-Keller, and E. W. Biersack, “Analysis of LAS scheduling for job size distributions with high variance,” in Proc. ACM SIGMETRICS Int. Conf. Meas. Modeling Comput. Syst., 2003, pp. 218–228.   
[55] L. Guo and I. Matta, “Scheduling flows with unknown sizes: Approximate analysis,” ACM SIGMETRICS Perform. Eval. Rev., vol. 30, no. 1, pp. 276–277, Jun. 2002.   
[56] A. Wierman and M. Nuyens, “Scheduling despite inexact job-size information,” in Proc. ACM SIGMETRICS Int. Conf. Meas. Modeling Comput. Syst., 2008, pp. 25–36.   
[57] M. DellAmico, D. Carra, and P. Michiardi, “PSBS: Practical sizebased scheduling,” IEEE Trans. Comput., vol. 65, no. 7, pp. 2199–2212, Jul. 2016.   
[58] E. J. Friedman and S. G. Henderson, “Fairness and efficiency in Web server protocols,” ACM SIGMETRICS Perform. Eval. Rev., vol. 31, no. 1, pp. 229–237, Jun. 2003.

![](images/be2c2c196defb6ed624f135f19e91b8c1b8c63b6d69f9501be938d887b7c0e2e.jpg)



Zhenhua Han received the B.Eng. degree in electronic and information engineering from the University of Electronic Science and Technology of China in 2014 and the Ph.D. degree of computer science from The University of Hong Kong (HKU) in 2020. He is currently a Researcher at Microsoft Research Asia (Shanghai). Many of his works have been published in top venues, such as IEEE INFOCOM, USENIX OSDI, and IEEE/ACM TRANSACTIONS ON NETWORKING. This work was done when he was visiting at USTC. His research interests include cloud computing, cluster scheduling, and machine learning systems.

![](images/6a9a69b5139116cd5cd059978d15cde8c97cc80f1e7181d1515340831b903197.jpg)



Haisheng Tan (Senior Member, IEEE) received the B.E. degree (Hons.) in software engineering and the B.S. degree (Hons.) in management from the University of Science and Technology of China (USTC), and the Ph.D. degree in computer science with The University of Hong Kong (HKU). He is currently an Associate Professor with USTC. His research interests lie primarily in networking algorithm design and system implementation, where he has published over 60 articles in prestigious journals and over 60 papers in prestigious conferences. He recently received the awards of the ACM China Rising Star (Hefei Chapter), the Distinguished TPC Member of INFOCOM 2019, and the Best Paper Award in WASA’19, CWSN’20 and PDCAT’20.

![](images/be995c9381c419ab4874ab4fb4feba08a81acc2a9fad7d1ee81b2c0b9484c5df.jpg)



Shaofeng H.-C. Jiang received the bachelor’s degree in software engineering from Shandong University in 2013 and the Ph.D. degree from The University of Hong Kong in 2017. He had been a Post-Doctoral Researcher with the Weizmann Institute of Science from 2017 to 2020 and an Assistant Professor with Aalto University from 2020 to 2021. He is currently an Assistant Professor with the Center on Frontiers of Computing Studies, Department of Computer Science, Peking University. His research is generally on theoretical computer science, with an emphasis on massive data sets, approximation algorithms and online algorithms.

![](images/c275850b12c00b75a42f1e7bf1fbcd15b72c9e4f503fff2f35055a3637b6723e.jpg)



Wanli Cao received the bachelor’s degree in software engineering from the University of Electronic Science and Technology of China in 2014, where he is currently pursuing the master’s degree. His research interests include reinforcement learning and edge computing.

![](images/226863472b9b0c16d13e97806a2057bf59851b71ac2d578ebbadf487e399f493.jpg)



Xiaoming Fu (Senior Member, IEEE) received the Ph.D. degree in computer science from Tsinghua University, Beijing, China, in 2000. He was a Research Staff with Technical University of Berlin until joining the University of Gottingen, Germany, in 2002, where he has been a Professor in computer science and heading the Computer Networks Group since 2007. He has spent research visits at the Universities of Cambridge, Uppsala, UPMC, Columbia, UCLA, Tsinghua, Nanjing, Fudan, and PolyU of Hong Kong. His research interests include network architectures, protocols, and applications. He is a Fellow of IET, a member of the Academia Europaea, and an IEEE Communications Society Distinguished Lecturer. He is currently an Editorial Board Member of IEEE Communications Magazine, IEEE TRANSACTIONS ON NETWORK AND SERVICE MANAGEMENT, and Computer Communications (Elsevier), and has served on the organization or program committees for leading conferences, such as INFOCOM, ICNP, ICDCS, MOBICOM, MOBIHOC, CoNEXT, ICN, and COSN.

![](images/96466708379b46c51c6b0d0855afed2fe773f11a56a26ebe7c70c8e9dfac3b3b.jpg)



Lan Zhang (Member, IEEE) received the bachelor’s degree from the School of Software, Tsinghua University, China, in 2007, and the Ph.D. degree from the Department of Computer Science and Technology, Tsinghua University, in 2014. She is currently a Research Professor with the School of Computer Science and Technology, University of Science and Technology of China. Her research interests include data trading, privacy protection, and mobile computing.

![](images/f72d5512a2331397e3529b6e475e5bfa1fe44fb17f835906a2082ec27b51c46a.jpg)



Francis C. M. Lau received the Ph.D. degree from the Department of Computer Science, University of Waterloo. He is currently an Honorary Professor in computer science with The University of Hong Kong, China. His research interests include computer systems, networks, programming languages, and application of computing in arts. He was formerly the Editor-in-Chief of the Journal of Interconnection Networks.