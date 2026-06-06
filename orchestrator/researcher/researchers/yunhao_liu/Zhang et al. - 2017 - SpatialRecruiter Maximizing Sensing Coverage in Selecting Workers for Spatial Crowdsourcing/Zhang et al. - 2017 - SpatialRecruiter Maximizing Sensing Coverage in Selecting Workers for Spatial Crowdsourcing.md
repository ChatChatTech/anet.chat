# SpatialRecruiter: Maximizing Sensing Coverage in Selecting Workers for Spatial Crowdsourcing

Xinglin Zhang, Member, IEEE, Zheng Yang, Member, IEEE, Yue-Jiao Gong, Member, IEEE, Yunhao Liu, Fellow, IEEE, and Shaohua Tang, Member, IEEE

Abstract—Spatial crowdsourcing and crowdsensing are two emerging crowdsourcing paradigms, which enable a variety of location-based query and sensing tasks. In spatial crowdsourcing, mobile workers are required to travel physically to target locations in order to complete query tasks. Most existing work hence focused on designing efficient query task assignment schemes to maximize the task completion rate under travelling constraints of workers for spatial crowdsourcing systems. In crowdsensing, on the other hand, sensor recordings of workers’ smartphones are of interest and have been collected to build various applications. Therefore, research work concerning crowdsensing strived to maximize the coverage area of sensor trajectories by selecting a set of workers. In this work, we investigate the integration of these two paradigms. We notice a key link between these paradigms: while a worker is travelling to the target location of a query task, his trajectory may provide valuable coverage for a sensing task. Therefore, we propose a task management framework, named SpatialRecruiter, to efficiently match workers to the merged query and sensing tasks. We propose two coverage estimation functions to compute the coverage potential of a worker. Then we design a greedy heuristic to select and assign workers. The experimental results on a real-world dataset demonstrate that the proposed strategies are efficient and effective in meeting the requirements of both paradigms.

Index Terms—Spatial Crowdsourcing, Crowdsensing, Task Assignment, Coverage Maximization

# I. INTRODUCTION

The ubiquity of smartphones and the easy access to ultra-broadband wireless networks has enabled a promising distributed problem-solving paradigm, mobile crowdsourcing [1], in which a crowd of smartphone users can be coordinated to collect multi-modal sensor data and complete location-based tasks. Particularly, two categories of mobile crowdsourcing, namely, spatial crowdsourcing and mobile crowdsensing, have received extensive attention in the research communities.

Spatial crowdsourcing [2] highlights people’s intellectual capability and mobility in completing location-based query tasks that are difficult for passive sensing with smartphones. Specifically, spatial crowdsourcing consists of a platform, task requestors, and mobile workers. The platform is in

X. Zhang and S. Tang are with the School of Computer Science and Engineering, South China University of Technology, China. E-mail: zhxlinse@gmail.com, shtang@ieee.org.   
Y.-J. Gong is with the Department of Computer and Information Science, University of Macau, China. E-mail: gongyuejiao@gmail.com.   
Z. Yang and Y. Liu are with the School of Software and Tsinghua National Lab for Information Science and Technology (TNLIST), Tsinghua University, China. E-mail: {yang, yunhao}@greenorbs.com.

charge of pooling location-based tasks delivered by task requestors and available mobile workers. After determining an assignment scheme, workers need to travel physically to the designated locations to complete assigned tasks (e.g., taking a picture or recording a video of the target of interest). Examples include parking space monitoring systems where the drivers are encouraged to report available parking space in a spatial region [3], [4], and post-disaster recovery systems where smartphone users take pictures of the damage and transfer them to the rescue center [5].

Mobile crowdsensing [6], on the other hand, emphasizes on the automatic sensing capability of mobile devices, especially smartphones. The multi-functional built-in sensors on smartphones (such as camera, gyroscope, accelerometer, compass, and GPS) can record ample information, including images, sounds, mobilities, and locations. With millions of such mobile devices carried by people, researchers are able to build large-scale sensing applications efficiently. Pioneer systems include NoiseTube [7] for noise monitoring, SmartTrace [8] and CityExplorer [9] for 3G/WiFi discovery, and LiFS [10] and TrMCD [11] for indoor localization.

Existing work mainly studies spatial crowdsourcing and mobile crowdsensing separately, underlining different concerns of these two paradigms. Specifically, in spatial crowdsourcing, the key problem is to achieve a maximal number of successful assignments, given the reliability of assigned tasks and the spatial-temporal constraints, such as the travelling distance of a worker and the expiration time of a task [12]–[15]. In mobile crowdsensing, sensing tasks largely require coverage of a spatial region, which indicates that the platform tends to recruit smartphone users, or workers, who have diverse travelling trajectories and can jointly cover a large portion of the region [16]–[18].

Intuitively, recruiting two sets of workers for the two kinds of tasks is not efficient considering the total recruitment number and travelling distance of workers. Specifically, when completing a spatial query task, workers need to travel through some area that may be of interest to certain crowdsensing task. If these workers turn on their sensors while travelling to the query location, they can accomplish query and sensing tasks with one shot and the system saves the number of required workers. Considering this bridging feature of spatial crowdsourcing and crowdsensing, we try to figure out the following issue in this work: Is it feasible to merge spatial crowdsourcing tasks and crowdsensing tasks, such that their requirements are satisfied efficiently?

Typically, we investigate a scenario of hybrid spatial crowdsourcing and crowdsensing, where location-based query and sensing tasks are merged and organized in periods. We assume that workers’ locations are known when they request to complete tasks. No further information about workers, including moving histories and current moving routes, is revealed to the system. We do not enforce workers to follow a specified route, i.e., workers move freely towards the locations with assigned query tasks. Under this setting, we propose a general task management framework, termed SpatialRecruiter, to pool and assign tasks and workers efficiently.

The most challenging part of SpatialRecruiter is to design an efficient assignment scheme that can incorporate query task completion rate, sensing coverage, and travelling distance, such that the requirements of query and sensing tasks can be fulfilled. On the one side, the traditional assignment solutions for spatial crowdsourcing is insufficient for the crowdsensing task, since they do not take into account the coverage of possible routes of recruited workers (i.e., they are ignorant of joint coverage of worker trajectories). On the other side, the worker selection solutions for crowdsensing cannot assign location-based query tasks to workers and hence they are unavailable for the spatial crowdsourcing part. Our intuition lies in the spatial diversity of workers. Positions of query tasks and workers, as well as the constraint of underlying physical routes, provide the opportunity that a subset of workers are able to undertake both query and sensing tasks simultaneously. One fundamental problem in pursuing this goal is to design an effective evaluation method to select workers. We design two functions, angle-based and entropy-based functions, to accommodate this worker evaluation problem. Then we design a heuristic procedure based on a greedy principle. The experimental results using a real-world dataset verify that the proposed framework achieves higher performance than baseline methods.

In summary, the key contributions of this paper are as follows:

We propose a general task management framework to merge and assign query and sensing tasks. To the best of our knowledge, this is the first work to study the combination of location-based query tasks and sensing tasks.   
• We propose two effective functions to estimate the coverage potential of workers, and design an efficient heuristic approach to assign tasks based on these functions.   
• We evaluate the proposed task assignment strategies on a real-world dataset. The results show that the proposed assignment schemes are promising compared to the traditional methods applied for spatial crowdsourcing.

The rest of the paper is organized as follows. Related works are discussed in Section II. Section III introduces system overview and design goals. The sensing coverage estimation functions and recruitment algorithms are illustrated in detail in Section IV and Section V, respectively. Then evaluation results are presented and discussed in Section VI. Finally, Section VII draws the conclusion.

# II. RELATED WORK

# A. Spatial Crowdsourcing

Location-based query tasks are studied in participatory sensing [19] in the early stage. The goal of participatory sensing is to exploit mobile users, for a given campaign, to actively collect and share data by leveraging their sensorequipped mobile devices. Participatory sensing systems mostly focus on a specific goal. For example, the Mobile Millennium project [20] uses mobile phones to collect and upload traffic information to a server in real time. Then the server can process the contributed traffic data and make predictions on the future traffic condition. Similarly, CalTel [21] and Nericell [22] are designed to collect information about traffic and road conditions by using mobile sensors and smartphones mounted on vehicles.

Based on these applications, Kazemi and Shahabi [2] introduced a taxonomy for spatial crowdsourcing, which subsumes participatory sensing by using a general framework. In this framework, multiple campaigns, or query tasks, can be handled simultaneously and mobile workers can be assigned efficiently, such that spatial crowdsourcing can achieve high social welfare. Kazemi and Shahabi [2] studied a maximum task assignment problem, which aims at maximizing the number of assigned tasks during the given time interval. He et al. [13] studied the problem of allocating location dependent tasks to workers by taking into account the travelling distance constraint and the completion redundancy for each task. Kazemi et al. [12] considered modeling the quality of workers, and designed efficient assignment protocols to ensure the task completion quality. Pournajaf et al. [23] studied the task assignment problem when workers utilize spatial cloaking to obfuscate locations. To et al. [14] designed a task assignment scheme to minimize the travelling distance of a worker, maximize task assignment success rate, as well as protect worker location privacy. On the other hand, Deng et al. [15] studied the task selection problem from workers’ perspective, and proposed a method to maximize the number of selected tasks given a worker’s travelling budget.

Given the various assumptions in these works, the common basic goal is to maximize task completion rate. Hence we also incorporate this factor in our model. Note that the travelling routes are not distinguished in these works as they do not affect the results of query task completion rate. On the contrary, we take a new perspective to merge query tasks and sensing tasks, making travelling trajectories of workers valuable to the system.

# B. Crowdsensing

Crowdsensing tasks emphasize on using the built-in sensors of smartphones to continuously collect sensed data during workers’ daily routine. In other words, workers do not need to respond to tasks intentionally once they have turned on the necessary sensors. The fundamental goal of crowdsensing tasks is to select a set of workers that can jointly cover the largest area in the target region. Cardone et al. [24] proposed a Mobile Crowdsensing platform and designed a simple participant selection mechanism to maximize the sensing area coverage of crowdsensing with predefined number of participants. Ahmed et al. [17] and Hachem et al. [25] attempted to select a minimal number of mobile users to cover a certain percentage of the target area by applying a user mobility model. Considering the sensing quality and workers’ willingness for participation, researchers studied incentive mechanisms to select appropriate workers [18], [26]–[29].

In this work, we propose two functions to evaluate the coverage potential of workers, and novelly combine the coverage target with the query task assignment problem.

# C. Optimization for Crowdsensing

Guestrin et al. [30] studied sensor placement for monitoring spatial phenomena. They modeled the phenomena as Gaussian Processes, and used mutual information to select the most informative locations. Similarly, Krause et al. [31] studied community sensing where spatial phenomena were modeled by a stochastic process, and the goal was to find participants that can bring the largest reduction in the predicted variance. These works used submodularity of the objective functions to design sensor selection algorithms. Singla and Kause [32] further considered the location privacy of participants by using adaptive submodularity of the objective function, such that the exact locations of participants were not revealed to the requestor unless they were selected and paid. Our work differs in that, the aforementioned work focused on static location selection, while we studied worker selection and task assignment simultaneously, and the coverage estimation functions were designed to accommodate the unknown mobility of workers.

CrowdRecruiter [16] is a novel participant selection framework for crowdsensing. It aims at selecting a small number of participants to satisfy the probabilistic coverage constraints for multiple sensing cycles. Using the similar framework, CrowdTasker [33] studies a dual problem where the requestor tries to maximize the probabilistic coverage given a fixed budget. iCrowd [34] further synthesizes the above works to form a generic task allocation framework for Piggyback Crowdsensing. These works make use of participants’ historical traces in the model and then design submodular functions to estimate the probability of cell tower coverage. The goal of the model does not involve assigning location-based query tasks to participants. Differently, our work does not assume prior knowledge about workers, and we design coverage estimation metrics with respect to each query task. Specifically, the coverage estimation functions in our work are based on the relative spatial positions of tasks and workers, as well as the potential moving directions of workers towards tasks; while the coverage in the aforementioned works refers to the participant’s presence at the cell tower.

EEMC [35] is a crowdsensing framework for sequential participant selection. The main objective is to minimize the number of selected participants who can return sufficient sensor data. It makes use of participants’ historical call traces to predict the current and future users’ possibilities of returning sensor data. $\mathrm { E M C ^ { 3 } }$ [36] extends EEMC to predict users’ call and mobility to ensure sufficient returned data and area coverage. These two works adopt stochastic sequential decision methods to minimize a regret bound. Our work differs in that, we study multiple cycles of worker selection and task assignment without the prior knowledge of workers’ mobility information, and we make decisions at the beginning of each cycle. In other words, we use a fixed time point to select users, while EEMC and $\mathrm { E M C ^ { 3 } }$ select users dynamically. DOG [37] is a distributed efficient algorithm that solves the online sensor selection problem where the submodular objective function is unknown. It tries to select workers at each cycle, such that after a small number of cycles the average performance of the algorithm coverges to the offline strategy that knows the objective function. Different from DOG, we explicitly model the objective functions for maximizing the completion number of query tasks and coverage of sensing tasks in each cycle. Nevertheless, extending our current model to a sequential decision scenario seems an interesting direction.

# III. SYSTEM OVERVIEW

# A. Terminologies and Framework

The SpatialRecruiter system is a spatial task management system that aims at assigning appropriate tasks to workers in order to achieve high social efficiency. The recruitment process of the system is organized in periods (e.g., five twohour cycles per day from 08:00 to 18:00). We first give the definitions of the spatial task and worker.

Definition 1 (Spatial Task) A spatial task is a combination of a location-based query task and a sensing task. Specifically, the query task is located within the coverage area of sensing tasks, and the completion deadlines of both query and sensing tasks locate in the same recruitment period.

For example, a query task can be “taking a photo of parking places during 3:00 - 4:00 p.m. in shopping mall S of region R”, and the corresponding sensing task can be “using mobile phone to record the noise levels of region R in the afternoon”. These two tasks can be merged to form a spatial task. Note that the specific merging technologies are platform and application dependent, and are not the concern of this work. In the rest of the paper, we assume that the sensing system has provided spatial tasks that need to be assigned and completed, and we design efficient assignment schemes to meet the requirements of both query and sensing components of spatial tasks.

Definition 2 (Worker) A worker in mobile crowdsourcing is a user equipped with mobile devices (e.g., smartphones), who is willing to complete spatial tasks assigned by the sensing system.

![](images/2c5a6aa04f7568f1150b16909d6c71acd5a30500489f7dccd221018d337a60d7.jpg)



Fig. 1. SpatialRecruiter Framework

Intuitively, a worker may want to do tasks on the way to some destinations (e.g., home, company), or take tasks that he is interested in. Therefore, a worker may designate a subset of achievable tasks from the task list provided by the sensing system. The system would only consider assigning a task from this designated set to the worker.

The SpatialRecruiter system contains two components and one communication process that links these components (Fig. 1). In the task merging component, the system aggregates query and sensing tasks in each period based on the shared spatial region, and constructs spatial tasks. Usually, the attributes of a spatial task include the location of the query task, the required sensor set of the sensing task, the payment for doing the task, and the deadline of the task. As the payment scheme (or incentive mechanism) is not the focus of this paper, we assume a simple uniform payment for all workers. The interested readers are referred to the survey paper [38] concerning worker incentives.

After task aggregation, the system communicates with the available workers by sending the task attributes. Upon receiving the task descriptions, a worker selects a subset of tasks based on his preference, as well as the location and time constraints. The selected set of tasks are sent back to the system.

The system then determines task assignment, which is the key concern of this paper, by applying several techniques. It first constructs an overall relation graph among tasks and workers according to workers’ submitted tasks. Then it designs proper functions for worker evaluation and runs the proposed worker selection algorithms.

# B. Design Goals and Performance Metrics

In our model, as workers are undertaking two kinds of tasks simultaneously, it is rational that we take into account the metrics of query and sensing tasks at the same time.

Query tasks usually require workers’ subjective effort, hence there may be a large deviation among different workers. A common strategy to handle this problem is to assign multiple workers to a single task [13], [23], such that the platform can use heuristic answer-aggregation methods, such as majority voting, to get a reliable answer. The multiplicity requirement of workers is called completion number, which is defined as follows.

Definition 3 (Completion Number) A completion number of a query task is a predefined threshold number of workers required to respond to that task.

With this definition, the goal of assigning location-based query tasks is to make most assigned tasks achieve their completion numbers.

On the other hand, crowdsensing requires workers to cover the whole target region with as few workers as possible [16], [17], [25], [33]. The rationality behind this goal is that sensed data collected by smartphones are redundant if the spatial correlation is considered, hence it is less significant to cover a physical plot for multiple times. Therefore, we also intend to maximize the efficiency of the travelling routes of assigned workers, such that the overall efficiency of the system is optimized. In other words, workers’ travelling efforts are minimized while meeting the requirements of spatial tasks.

Combining the goals of the two task paradigms, we focus on the following performance metrics in this work:

• Coverage Area of Sensing Tasks. The travelling routes of workers are unknown a priori, hence it is challenging to guarantee that the assigned workers cover a large spatial area of the target region.   
• Coverage Efficiency. Coverage efficiency of the assigned workers is defined as the ratio of the covered area and the total travelling distance of workers. A larger coverage efficiency value indicates higher social efficiency with respect to the travelling cost.   
• Completion Rate of Query Tasks. Due to the task and worker uncertainty, the platform may fail to assign sufficient workers to each query task. Completion rate measures the ratio of query tasks that achieve completion numbers.

# IV. COVERAGE AREA ESTIMATION

In this section, we discuss the sensing coverage estimation of selected workers, a key component that will be used in designing worker recruitment scheme in Section V. Given that a query task has a completion number k, and each query task t has a sufficient number of candidate workers, the objective of the recruitment process is to guarantee large coverage of the k selected workers.

Note that in some crowdsensing scenarios, the historical trajectory data of workers is assumed to be assessable by the system. By using the historical data and probabilistic models (e.g., Markov chain and Poisson process), some researchers constructed probabilistic coverage models for discretized locations of interest [16], [17], [33], [34]. In this work, we do not assume any prior knowledge about workers, since in many applications, historical data is inconvenient to obtain and maintain as workers are unwilling to reveal their travelling privacy. Therefore, we only make use of the relative spatial positions of workers and tasks to design coverage estimation functions, i.e., angle-based and entropy-based estimation functions.

# A. Angle-based Estimation Function

The intuition of our first coverage estimation function is that, when a worker moves towards a query task location, he tends to move towards the destination by a short route.

![](images/712a8073673565adba7b60deede37aa1af12b994ff6201b95a1276fe47509d0d.jpg)  
(a)

![](images/80a2fea003f20be54bca8c2b53c171a7c472ad40e1bcfd1b85f4bd9d55ab6226.jpg)



(b)   
Fig. 2. Coverage potential of workers.

Though the straight line between the starting location and the destination location may be impassable, the worker may choose the routes not deviating much from this shortest line. Based on this intuition, We can represent the shortroute tendency as a sector radiating from the task (i.e., destination) to the worker: The farther the worker is from the task, the more route choices he has; and the choices decrease as he approaches the task. Typically, as shown in Fig. 2(a), the worker w is assigned to the query task t, the sector covering w and t represents the coverage potential of w, where the potential angle $\varphi$ is a parameter that reflects the route diversity of w. A larger φ indicates that the worker w has more diverse routes to select when travelling towards the target.

With the aforementioned discussion, we can design an angle-based coverage estimation function for the candidate workers. In Fig. 2(b), a set of workers $W =$ $\{ w _ { 1 } , w _ { 2 } , . . . , w _ { n _ { t } } \}$ are available for the query task t, where $n _ { t }$ is the number of available workers. Given the task completion number k and the potential coverage angle $\varphi$ of the sectors, if the sectors of selected workers overlap to a large extent, there is a high probability that the real trajectories of these workers may overlap. Hence we tend to select k workers that cover the largest angular interval around the query task t. In this way, the selected workers may have a higher probability to cover larger area of the target region.

As an example, assume that $k \ = \ 2$ and $n _ { t } ~ = ~ 3$ in Fig. 2(b), it can be induced from the figure that the sectors of $w _ { 1 }$ and $w _ { 2 }$ overlap to a large extent, hence the joint area of these two workers is smaller than that of $w _ { 1 }$ and $w _ { 3 }$ (as the sectors of $w _ { 1 }$ and $w _ { 3 }$ do not overlap). Intuitively, it is more promising to select $w _ { 1 }$ and $w _ { 3 }$ for the query task t. Formally, the coverage of $w _ { i } ( i = 1 , 2 , . . . , n _ { t } )$ on t can be represented by an interval of [0, 2π):

$$
C _ {i} = [ \angle w _ {i} t w _ {0} - \varphi , \angle w _ {i} t w _ {0} + \varphi ], \tag {1}
$$

where $w _ { 0 }$ is a null worker locating in the east of the task t, representing the position with 0 degree. The angles are calculated by arithmetic modulo 2π. The total coverage of the query task t thus can be defined as:

$$
C ^ {t} (W _ {t}) = \cup_ {i \in W _ {t}} C _ {i}, \tag {2}
$$

![](images/e7e2ee7308db038462871d6eaf640451d5414f3c1c07b5bf1c4bdaf32d910b78.jpg)



Fig. 3. Spatial entropy of workers.

where $W _ { t }$ is the set of selected workers for task t. If there are multiple query tasks, each task can be evaluated by a coverage interval as discussed above. The total coverage utility of the assignment is the summation of the coverage of each query task.

# B. Entropy-based Estimation Function

Another perspective of estimating the coverage potential is to model the coverage potential from the overall distribution of the workers around the task instead of selecting workers from scratch as in the angle-based estimation function. The key idea is to maximize the starting position diversity of workers for a specific task, such that these workers may provide a higher probability of choosing different routes when moving towards the task.

A common approach for measuring the diversity, or chaos, of a set of points is entropy. We hence define a spatial entropy of workers assigned to a task following the definition of entropy. As illustrated in Fig. 3, a set of workers $W = \{ w _ { 1 } , w _ { 2 } , . . . , w _ { n _ { t } } \}$ are interested in answering the query task t. We link the physical locations of t and each worker, and obtain an angle between neighboring workers. When we select a subset $W _ { t } \subseteq W$ of k workers to complete the task t (where k is the task completion number), the angles of neighboring selected workers form an angle set $\phi _ { t } .$ . The spatial entropy of the query task t is defined as follows:

$$
E ^ {t} (W _ {t}) = - \sum_ {\varphi \in \phi_ {t}} \frac {\varphi}{2 \pi} \log \frac {\varphi}{2 \pi}, \tag {3}
$$

where $\textstyle \sum _ { \varphi \in \phi _ { t } } \varphi = 2 \pi$ . The overall entropy of all successfully assigned tasks is the summation of the entropy of each task.

We give a simple example to demonstrate the effectiveness of the spatial entropy function. As shown in Fig. 3, we assume that the number of available workers $n _ { t } = 5$ and the task completion number $k = 3 .$ Consider two candidate worker subsets $\boldsymbol { W _ { 1 } } ~ = ~ \{ w _ { 1 } , w _ { 2 } , w _ { 3 } \}$ and $W _ { 2 } ~ = ~ \{ w _ { 2 } , w _ { 4 } , w _ { 5 } \}$ . The angle values are $\angle w _ { 1 } t w _ { 2 } \ =$ $\angle w _ { 2 } t w _ { 3 } = \pi / 3 , \angle w _ { 3 } t w _ { 1 } = 4 \pi / 3 , \angle w _ { 2 } t w _ { 4 } = \angle w _ { 4 } t w _ { 5 } =$ $\angle w _ { 5 } t w _ { 2 } = 2 \pi / 3$ . Then the entropy of worker set $W _ { 1 }$ for task t is

$$
\begin{array}{l} E ^ {t} (W _ {1}) = - 2 * \frac {\pi}{3 * 2 \pi} \log \frac {\pi}{3 * 2 \pi} - \frac {4 \pi}{3 * 2 \pi} \log \frac {4 \pi}{3 * 2 \pi} \\ = 0. 3 8, \\ \end{array}
$$

while the entropy of $W _ { 2 }$ is

$$
\begin{array}{l} E ^ {t} (W _ {2}) = - 3 * \frac {2 \pi}{3 * 2 \pi} \log \frac {2 \pi}{3 * 2 \pi} \\ = 0. 4 8. \\ \end{array}
$$

The result $E ^ { t } ( W _ { 2 } ) > E ^ { t } ( W _ { 1 } )$ complies with the fact that, the workers of $W _ { 2 }$ are more diversely distributed around the task t than the workers of $W _ { 1 }$ , which implies that $W _ { 2 }$ is a more promising candidate set that can provide larger coverage while completing the query task.

# V. RECRUITMENT ALGORITHMS

In this section, we describe the recruitment algorithms for the SpatialRecruiter system. We will first convert the worker-task relation to a bipartite graph, and adopt a degree priority method to pursue a high overall completion rate with respect to query tasks. Then we propose a greedy strategy to maximize the spatial coverage of workers for sensing tasks.

# A. Degree Priority

The task preference of workers can be used to construct a bipartite graph to represent the whole structure between workers and query tasks. Specifically, let W and T denote the set of all available workers and query tasks in the current recruitment period, respectively. Each worker and query task is a node in the graph. If a worker $w \in W$ has preference for a task $t \in T ,$ , we add an edge $e = ( w , t )$ between them. Then all edges constitute the edge set $E ,$ and we can obtain a bipartite graph $G = ( W , T , E )$ . Note that in our model, a worker has preference for several tasks, but is assigned with one task at a time; while a task can be assigned with k workers, where k is the preset completion number. In order to maximize the number of completed query tasks, we sort the query tasks in ascending order with respect to their degrees in the bipartite graph. A smaller degree means that the corresponding task has fewer choices over the available workers, and will be processed earlier in our scheme.

# B. Greedy Selection

After determining a query task for assignment, we design a greedy strategy to iteratively select workers so as to maximize the coverage:

• We first find a worker with the maximal utility among all available workers linked to the current query task, and add this worker to the selected set;   
• Then we find an unselected worker that generates the maximal utility when combined with the selected workers, and add him to the set of selected workers;   
• The algorithm continues this selection process until the number of selected workers reaches the completion number.

Specifically, the utility of a worker is measured by using the coverage estimation functions proposed in Section IV. In order to select a worker with the maximal utility, given the set $W$ of available workers and the selected set $W _ { t }$ for the query task t, we combine each unselected worker $w \in$ $W \backslash W _ { t }$ with the selected set $W _ { t }$ to generate an augmented set $W _ { t } \cup \{ w \}$ . Then we compute the utility of each possible combined set and select the one with the maximal utility. We keep this maximal set as the updated selected set for the next iteration of selection until the stopping criterion is met.

The above greedy strategy provides an efficient approximate solution for the following optimization problem:

$$
\max _ {W _ {t} \subseteq W} F (W _ {t}) \text {   s.t.   } | W _ {t} | = k, \tag {4}
$$

where $F$ is the utility function (angle-based estimation function $C ^ { t }$ or entropy-based estimation function $E ^ { t }$ in Section IV) of workers that are assigned to the query task t, and k is the completion number. We investigate the theoretic performance of the greedy heuristic for this optimization problem by using the following two lemmas.

Lemma 1 The angle-based estimation function is a monotone submodular function.

Proof: We prove that the proposed angle-based estimation function is monotone submodular by definition.

Definition 4 (Monotone Submodular Function) Given a groundset Ω, a function $f : 2 ^ { \Omega } \to R$ is submodular if for any $A \subseteq B \subseteq \Omega$ and an element $e \in \Omega ,$ , we have

$$
f (A \cup \{e \}) - f (A) \geq f (B \cup \{e \}) - f (B).
$$

The function f is also monotone $i f f ( A ) \leq f ( B )$ .

Let W denote the whole set of available workers for task $t . \ W _ { t } ^ { 1 }$ and $W _ { t } ^ { 2 }$ are two sets of selected workers for task t, where $\dot { W } _ { t } ^ { 1 } \subseteq W _ { t } ^ { 2 } \subseteq W$ . According to the equations $( 1 ) ‐ ( 2 )$ , we can derive that $C ^ { t } ( W _ { t } ^ { 1 } ) \subseteq \bar { C } ^ { t } ( W _ { t } ^ { 2 } )$ . Consider a new worker $w \in W \backslash W _ { t } ^ { 2 }$ with the coverage $c = [ \angle w t w _ { 0 } - \varphi , \angle w t w _ { 0 } + \varphi ]$ . By using the set operation rule, we have $c \cap \overline { { C ^ { t } ( W _ { t } ^ { 1 } ) } } ~ \geq ~ c \cap \overline { { C ^ { t } ( W _ { t } ^ { 2 } ) } }$ . Therefore, $C ^ { t } ( W _ { t } ^ { 1 } \cup \{ w \} ) - C ^ { t } ( W _ { t } ^ { 1 } ) - \left( C ^ { t } ( W _ { t } ^ { 2 } \cup \{ w \} ) - C ^ { t } ( W _ { t } ^ { 2 } ) \right) =$ $c \cap \overline { { C ^ { t } ( W _ { t } ^ { 1 } ) } } - c \cap \overline { { C ^ { t } ( W _ { t } ^ { 2 } ) } } \geq 0$ . By the definition given above, we have proved that the function $C ^ { t }$ is monotone submodular. The summation of $C ^ { t }$ for all workers preserves monotone submodularity [39].

Lemma 2 The entropy-based estimation function is a monotone submodular function.

Proof: We prove the lemma by the definition of monotone submodular function (Definition 4). Let W denote the whole set of available workers for task $t . \ W _ { t } ^ { 1 }$ and $W _ { t } ^ { 2 }$ are two sets of selected workers for task t, where $\dot { W _ { t } ^ { 1 } } \subseteq W _ { t } ^ { 2 } \subseteq W$ . The angle sets $\phi _ { t } ^ { 1 }$ and $\phi _ { t } ^ { 2 }$ are formed by the neighboring workers of $W _ { t } ^ { 1 }$ and $W _ { t } ^ { 2 }$ , respectively. Consider a new worker w $\in \ W \backslash W _ { t } ^ { 2 }$ , which divides an angle $\varphi \in \phi _ { t } ^ { 1 }$ into two angles $\varphi _ { 1 }$ and $\varphi - \varphi _ { 1 }$ , and divides an angle $\varphi ^ { \prime } \in \phi _ { t } ^ { 2 }$ into two angles $\varphi _ { 1 } ^ { \prime }$ and $\varphi ^ { \prime } - \varphi _ { 1 } ^ { \prime }$ . Then we need to prove the following inequation to show that $E ^ { t }$ is

submodular:

$$
\begin{array}{l} E ^ {t} (W _ {t} ^ {1} \cup \{w \}) - E ^ {t} (W _ {t} ^ {1}) \\ = - \frac {\varphi_ {1}}{2 \pi} \log \frac {\varphi_ {1}}{2 \pi} - \frac {\varphi - \varphi_ {1}}{2 \pi} \log \frac {\varphi - \varphi_ {1}}{2 \pi} + \frac {\varphi}{2 \pi} \log \frac {\varphi}{2 \pi} \\ \geq - \frac {\varphi_ {1} ^ {\prime}}{2 \pi} \log \frac {\varphi_ {1} ^ {\prime}}{2 \pi} - \frac {\varphi^ {\prime} - \varphi_ {1} ^ {\prime}}{2 \pi} \log \frac {\varphi^ {\prime} - \varphi_ {1} ^ {\prime}}{2 \pi} + \frac {\varphi^ {\prime}}{2 \pi} \log \frac {\varphi^ {\prime}}{2 \pi} \\ = E ^ {t} (W _ {t} ^ {2} \cup \{w \}) - E ^ {t} (W _ {t} ^ {2}). \tag {5} \\ \end{array}
$$

According to the edge positions of $\varphi$ and $\varphi ^ { \prime } ,$ , we discuss in three cases:

• $\varphi$ and $\varphi ^ { \prime }$ have two common edges. It is easy to see that the inequation (5) holds.   
· $\varphi$ and $\varphi ^ { \prime }$ have one common edge. Without loss of generality, we assume that $\varphi _ { 1 } = \varphi _ { 1 } ^ { \prime }$ after adding the new worker w. Then proving the inequation (5) is equivalent to prove the following inequation:

$$
\begin{array}{l} - \frac {\varphi - \varphi_ {1}}{2 \pi} \log \frac {\varphi - \varphi_ {1}}{2 \pi} + \frac {\varphi}{2 \pi} \log \frac {\varphi}{2 \pi} \\ \geq - \frac {\varphi^ {\prime} - \varphi_ {1}}{2 \pi} \log \frac {\varphi^ {\prime} - \varphi_ {1}}{2 \pi} + \frac {\varphi^ {\prime}}{2 \pi} \log \frac {\varphi^ {\prime}}{2 \pi}, \\ \end{array}
$$

where $\varphi _ { 1 } ~ < ~ \varphi ^ { \prime } ~ < ~ \varphi ~ \in ~ ( 0 , 2 \pi )$ , and $\varphi _ { 1 }$ can be treated as a constant. We show that the function $\begin{array} { r } { f ( x ) = x \log x - ( x - \frac { \varphi _ { 1 } } { 2 \pi } ) } \end{array}$ log $\textstyle \left( x - { \frac { \varphi _ { 1 } } { 2 \pi } } \right)$ is monotonically increasing given $x \in { \overline { { ( 0 , 1 ) } } }$ . In fact, the derivative of f (x) is $\begin{array} { r } { f ^ { \prime } ( x ) = \log x - \log ( x - \frac { \varphi _ { 1 } } { 2 \pi } ) > 0 , } \end{array}$ , which proves the inequation (6).

• φ and $\varphi ^ { \prime }$ have no common edge. In this case, we construct a virtual worker set $W _ { t } ^ { 3 }$ that satisfies $W _ { t } ^ { 1 } \subseteq$ $W _ { t } ^ { 3 } \subseteq W _ { t } ^ { 2 }$ , and $W _ { t } ^ { 3 }$ has one common edge with $W _ { t } ^ { 1 }$ and $W _ { t } ^ { 2 }$ in the neighborhood of the new worker w, respectively. Then we can use the proof procedure in the second case twice to achieve the result.

Next we show that $E ^ { t }$ is monotone:

$$
\begin{array}{l} E ^ {t} (W _ {t} ^ {1} \cup \{w \}) - E ^ {t} (W _ {t} ^ {1}) \\ = - \frac {\varphi_ {1}}{2 \pi} \log \frac {\varphi_ {1}}{2 \pi} - \frac {\varphi - \varphi_ {1}}{2 \pi} \log \frac {\varphi - \varphi_ {1}}{2 \pi} + \frac {\varphi}{2 \pi} \log \frac {\varphi}{2 \pi} \\ \geq - \frac {\varphi_ {1}}{2 \pi} \log \frac {\varphi}{2 \pi} - \frac {\varphi - \varphi_ {1}}{2 \pi} \log \frac {\varphi}{2 \pi} + \frac {\varphi}{2 \pi} \log \frac {\varphi}{2 \pi} \\ = - \frac {\varphi_ {1} + \varphi - \varphi_ {1} - \varphi}{2 \pi} \log {\frac {\varphi}{2 \pi}} \\ = 0. \\ \end{array}
$$

The second inequality is due to the fact that log $\textstyle { \frac { \varphi } { 2 \pi } } \leq 0$ $\frac { \varphi - \varphi _ { 1 } } { 2 \pi } \leq$ 2π log wh $\textstyle { \frac { \varphi } { 2 \pi } } \leq 0$ 2π . Therefore we havees the monotonicity $\begin{array} { l l } { \displaystyle { \frac { \varphi _ { 1 } } { 2 \pi } } } & { \displaystyle \leq } \end{array}$ $E ^ { t } ( \tilde { W } _ { t } ^ { 1 } \cup \{ w \} ) \geq E ^ { t } \tilde { ( W } _ { t } ^ { 1 } )$ of $E ^ { t }$ . The summation of $E ^ { t }$ for all workers preserves monotone submodularity [39].

Combining Lemmas 1-2 and the theory of submodular maximization [40], the proposed greedy heuristic is able to find a solution of 0.63-approximation factor compared to the optimal solution for the optimization problem (4).

Deriving from the properties of the angle-based and entropy-based functions, we can also show that the proposed recruitment problem is NP-hard.

![](images/155cb194721786f2d3addf457e96347c1f88556baafa66d3d29e42c3f04c43a7.jpg)



Fig. 4. Average coverage area increment of AGreedy with different $\varphi$

Lemma 3 The proposed recruitment problem for jointly maximizing task completion rate and sensing area coverage is NP-hard given the angle-based and entropy-based estimation functions.

Proof: We prove the lemma by reducing the submodular maximization problem with cardinality constraints (SM-CC) to an instance of the proposed recruitment problem. An SMCC problem is NP-hard [40] and can be described as follows: Given a universe set $U = \{ u _ { 1 } , u _ { 2 } , . . . , u _ { n } \}$ , a monotone submodular function $f$ defined on $U ,$ , and a cardinality value K. The objective is to maximize $f ( U ^ { \prime } )$ , where $U ^ { \prime } \subseteq U$ , and $| U ^ { \prime } | \leq K$ . For a given SMCC problem, we can transform it to an instance of the proposed recruitment problem as follows: Consider that there is only one task t with a set of available workers $W _ { t } = \left\{ w _ { 1 } , w _ { 2 } , . . . , w _ { n _ { t } } \right\}$ , where $n _ { t } ~ > ~ k$ . Then the objective of this instance is to select k workers for task t to maximize the angle-based or entropy-based estimation functions. As we have proved that these two functions are monotone submodular, the results of solving the SMCC problem (by mapping $C ^ { t } / E ^ { t }$ to $f ,$ $W _ { t }$ to $U ,$ and k to K) are also the results of the above recruitment instance, which completes our proof.

# VI. EVALUATION

In this section, we evaluate the proposed recruitment algorithms on a real-world dataset. We first introduce the experiment settings, including the property of the dataset, the evaluation metrics, and the baseline strategy. Then we show the results with discussion.

# A. Settings

Dataset. We evaluate the performance of the proposed task assignment methods by using the real-world dataset, T-drive [41], [42]. This dataset contains the GPS traces of 10,357 taxis in Beijing during a period of one week in 2008. The total number of the GPS sampling points is around 15 million and the total travelling distance of taxis is about 9 million kilometers.

We take each taxi as a worker equipped with necessary functional sensors, and assume that a worker is able to complete a spatial task along his trajectory. Recall that a spatial task is consisted of a query task and a sensing task. In the experiment, we assume that the whole map of Beijing is of interest for a sensing task (e.g., noise monitoring). We generate a number of query tasks in the road networks of Beijing. Specifically, the road network is consisted of road segments, which has the attributes of segment ID, segment length, and the GPS coordinates of the head and end of the segment. The query task is randomly generated among the GPS coordinates of the segment ends. We employ an HMM algorithm [43] to perform map matching, which maps each GPS point of a worker’s trace to the corresponding road segment. As a result, a worker’s trajectory is converted to a sequence of road segments.

![](images/730f25d17ed5ef489a316eb7c36c4aa387b4eba9f0e8b2dec93b37e926a7afa5.jpg)



(a) k = 3

![](images/e53bac36ce06629b7446c75a14de13618f9e1e59aa2be354e2a3458d586d2452.jpg)



(b) $k = 5$

![](images/28bf1cc0ded5e0910ccf30260de871d03b2df9c85ba193d544b97aa06d87550f.jpg)



(c) k = 7

![](images/b840912b019a586b05877fee01278ecd94337ee3f8df959138fc74962c394f56.jpg)



(d) $k = 9$

Fig. 5. Coverage area increment of AGreedy with different φ   
![](images/208e7fac5c051223b8ea8293f5d94960b30fb1330b40f18fc06daab77966e647.jpg)



(a) $k = 3$

![](images/1127e0ba6d623d38ce54d88ba92629bd7fa6a9b61d0061063d2fe6ce1ec77146.jpg)



(b) $k = 5$

![](images/b8c36beca9c8bc70fec5a7e93b1ebc6183518df30312ab5511936ca13fd7ffbb.jpg)



(c) k = 7

![](images/db820ad0403e212980866ca2a14a77f1a8a82fa8246925183eeab92facfd0a03.jpg)



(d) $k = 9$   
Fig. 6. Coverage efficiency of AGreedy with different φ

The recruitment process is divided into two-hour periods. The first GPS position of each taxi in a period is the starting point of the worker, and the trajectory in that period can be regarded as the coverage of the worker. A worker prefers a query task whose GPS location is covered by the worker’s trajectory. In this way, we can get the task and worker sets, as well as the task-worker relation for each period. We eliminate the tasks with insufficient degrees before running the algorithms, as they cannot fulfill the recruitment requirement and can be postponed to the later periods until they receive enough candidates. Specifically, in our experiment, the maximum completion number is set to 10 considering the following facts. First, many query tasks are easy to answer and are time sensitive, hence we do not require many replies per task. Second, crowdsensing systems usually assign hundreds of query tasks in each period. Considering the dataset size of T-drive, we can obtain hundreds of available tasks by setting a relatively small completion number.

Evaluation Metrics. In addition to the completion rate of query tasks, we need to calculate the coverage rate of sensing tasks and the coverage efficiency as discussed in Section III-B. In this experiment, the sensing coverage is measured by the lengths of road segments. Let $W ~ = ~ \{ 1 , 2 , . . . , n \}$ be the set of assigned workers, and $T R _ { i } = \{ ( s _ { i 1 } , l _ { i 1 } ) , ( s _ { i 2 } , l _ { i 2 } ) , . . . , ( s _ { i m _ { i } } , l _ { i m _ { i } } ) \}$ be the set of road segments covered by worker $i \in W$ , where $s _ { i j }$ and $l _ { i j }$ are the j-th road segment ID and length of worker i, respectively. $m _ { i }$ is the number of covered segments of worker i. Then the coverage of the worker set $W$ is defined as:

$$
C (W) = \sum_ {(s, l) \in \cup_ {i \in W} T R _ {i}} l.
$$

The total travelling distance of the worker set W is:

$$
D (W) = \sum_ {i \in W} \sum_ {(s, l) \in T R _ {i}} l.
$$

Combining the above two formulas, the total coverage efficiency is defined as $C E = C ( W ) / D ( W )$ . Note that the evaluation results are computed in average for all 2- hour recruitment periods.

Comparisons. As we proposed two coverage estimation functions, the recruitment algorithm is implemented in two forms. We term the recruitment algorithms adopting anglebased and entropy-based estimation functions as AGreedy and EGreedy, respectively. Also, we select a well-adopted spatial task assignment heuristic [14], [15], nearest neighbor selection (NNS), as the baseline algorithm in the experiment. We consider two distance metrics when applying NNS, the Euclidean distance and City Block distance. We term the NNS with Euclidean and City Block distance as NNSE and NNSCB, respectively. The task degree-based heuristic is also integrated to NNS.

# B. Results

1) Effect of potential angle φ for AGreedy.: We first investigate the effect of the angle parameter $\varphi$ on the

TABLE I COMPLETION RATES OF AGREEDY WITH DIFFERENT φ 

<table><tr><td>#workers</td><td>angles</td><td>100</td><td>140</td><td>180</td><td>220</td><td>260</td><td>300</td><td>340</td><td>avg.</td></tr><tr><td rowspan="4">k=3</td><td>φ=15</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0.9996</td><td>0.9993</td><td>0.9982</td><td>0.9995</td></tr><tr><td>φ=30</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0.9996</td><td>0.9983</td><td>0.9964</td><td>0.9991</td></tr><tr><td>φ=45</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0.9976</td><td>0.9961</td><td>0.9991</td></tr><tr><td>φ=60</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0.9996</td><td>0.9993</td><td>0.9976</td><td>0.9995</td></tr><tr><td rowspan="4">k=5</td><td>φ=15</td><td>0.9990</td><td>0.9971</td><td>0.9866</td><td>0.9750</td><td>0.9623</td><td>0.9380</td><td>0.9085</td><td>0.9666</td></tr><tr><td>φ=30</td><td>0.9990</td><td>0.9971</td><td>0.9861</td><td>0.9727</td><td>0.9557</td><td>0.9250</td><td>0.9041</td><td>0.9628</td></tr><tr><td>φ=45</td><td>1</td><td>0.9957</td><td>0.9894</td><td>0.9781</td><td>0.9580</td><td>0.9390</td><td>0.9070</td><td>0.9667</td></tr><tr><td>φ=60</td><td>1</td><td>0.9985</td><td>0.9916</td><td>0.9790</td><td>0.9584</td><td>0.9360</td><td>0.9073</td><td>0.9672</td></tr><tr><td rowspan="4">k=7</td><td>φ=15</td><td>0.9740</td><td>0.9528</td><td>0.9088</td><td>0.8604</td><td>0.7992</td><td>0.7386</td><td>0.6779</td><td>0.8445</td></tr><tr><td>φ=30</td><td>0.9820</td><td>0.9542</td><td>0.9061</td><td>0.8495</td><td>0.7938</td><td>0.7360</td><td>0.6835</td><td>0.8435</td></tr><tr><td>φ=45</td><td>0.9760</td><td>0.9457</td><td>0.9122</td><td>0.8590</td><td>0.7942</td><td>0.7410</td><td>0.6838</td><td>0.8445</td></tr><tr><td>φ=60</td><td>0.9860</td><td>0.9571</td><td>0.9094</td><td>0.8536</td><td>0.7976</td><td>0.7420</td><td>0.6858</td><td>0.8473</td></tr><tr><td rowspan="4">k=9</td><td>φ=15</td><td>0.8800</td><td>0.7993</td><td>0.7233</td><td>0.6514</td><td>0.5781</td><td>0.5167</td><td>0.4691</td><td>0.6597</td></tr><tr><td>φ=30</td><td>0.8890</td><td>0.8071</td><td>0.7206</td><td>0.6427</td><td>0.5742</td><td>0.5173</td><td>0.4659</td><td>0.6596</td></tr><tr><td>φ=45</td><td>0.9010</td><td>0.8044</td><td>0.7206</td><td>0.6405</td><td>0.5750</td><td>0.5190</td><td>0.4691</td><td>0.6614</td></tr><tr><td>φ=60</td><td>0.8920</td><td>0.8114</td><td>0.7139</td><td>0.6455</td><td>0.5769</td><td>0.5233</td><td>0.4753</td><td>0.6626</td></tr></table>

![](images/b514913b2463b3dccd7d337cf4a1c958763fcb24bc8c2c16154d2ccf602d9b02.jpg)



Fig. 7. Average coverage area increment

performance of AGreedy.

Fig. 4 shows the average sensing area coverage performance of AGreedy with different $\varphi$ by setting different completion numbers. Specifically, we select $\varphi = 1 5$ degrees as the baseline, and obtain the coverage increment ratio curves of 30, 45, and 60 degrees divided by 15 degrees. As can be seen from the figure, the ratio is larger than zero on average, which means that a larger degree returns larger coverage. The result complies with the intuition that a larger degree indicates a larger variance of travelling through different routes. This trend enhances monotonically from 15 to 45 degrees, but the performance of 60 degrees is inferior to that of 45 degrees. This is due to the fact that, when selecting more workers, a large degree is prone to achieving full degree coverage of a task in selecting the first few workers. The workers selected later hence are randomly chosen as all candidates have zero coverage increment in computation. On average, the highest coverage value is achieved when $\varphi \ = \ 4 5$ degrees. In Fig. 5, we present the detailed curve trends by setting the completion number $k = 3 , 5 , 7 , 9$ (Note that the trends reflected by figures and tables which have completion numbers other than $k = 3 , 5 , 7 , 9$ are similar to the trends of figures and tables by setting $k = 3 , 5 , 7 , 9$ , hence we only present the results of $k = 3 , 5 , 7 , 9$ in the paper to keep the figures informative and succinct). It can be seen from the curves that the coverage performance of 45 degrees is consistently better than the other three degrees with different number of task candidates.

Fig. 6 depicts the coverage efficiency trends of different angles. As can be seen, the efficiency values and trends of different angles are similar. Numerically, the average efficiency values of 15, 30, 45, and 60 degrees are 36.16%, 36.48%, 36.78%, and 36.46%, respectively.

The recruitment completion rates of AGreedy with varying parameters are listed in Table I. It can be seen that for each completion number k, the rates obtained by different angles are very close. Typically, from the rightmost column of the table, which is the average rate for each angle, we can see that for each k, the average performance of different angles are similar, and with the increment of k, the rates drop at nearly the same pace for different angles. In summary, varying angles has little influence on the completion rates of AGreedy.

Briefly, the degree $\varphi$ has less impact on the query task completion rate and sensing coverage efficiency of AGreedy, while it has more impact on the coverage area. The result is most significant when the completion number is not very large. The underlying rationality is that when the query task requires many workers, the algorithm is easier to select workers scattering well around the task. In our experiment, the overall performance of AGreedy is best when $\varphi = 4 5$ degrees, hence in the remaining experiments we will set this value for AGreedy.

Note: The optimal angle value $\varphi$ is application dependent. In the ideal case, where we have the knowledge of workers’ historical trajectories, we can obtain the potential angle of each taxi accurately. However, in our studied model, we do not assume any prior information about workers, hence we cannot set a perfect potential angle for each taxi. Instead, we use a common potential angle for all workers. One strategy to find a good candidate angle is similar to our investigation above: We can feed the algorithm with a set of angles for the first few recruitment periods simultaneously. Then we can select the angle value that obtains the best result for the following recruitment periods. As a future direction, we will investigate the possibility of adjusting the angle value automatically and adaptively.

![](images/20d5f7bf15630360e7cbf25c143a61189fd053073d43aea259ae07d6e3cb66e3.jpg)



(a) $k = 3$

![](images/321803d580da4b6c4d786646abb08474436ab5418beaebe1f91247aa75b31bb1.jpg)



(b) k = 5

![](images/76cb36825a6a4849c2f70736def7f65bc5cf3282464a385f41c051ad611115a5.jpg)



(c) k = 7

![](images/056937d0152e1146ce9587ffdb96525862aba623dff318267abc62799d8606fa.jpg)



(d) k = 9

Fig. 8. Coverage area increment   
![](images/250ffab398691b6d2a563ad19fcd65ae10fb81b51c9ca03ec3caefb9d998ba25.jpg)



(a) $k = 3$

![](images/62d858e275d9c6e2d75f903a5141c37a738bc570062b04843a58dbe95a79b0aa.jpg)



(b) $k = 5$

![](images/4f25f6979c602609aa736238a8992c935a07fb5f28ef21d2ed7602737a9af965.jpg)



(c) k = 7

![](images/52bb70984c6bf2e293a66261bdad7254a65540ca3ecd5c23608b486af48ee67a.jpg)



(d) k = 9   
Fig. 9. Coverage efficiency

2) Comparisons of different algorithms.: Fig. 7 shows the average performance considering the coverage area with different completion numbers. We select the coverage area of NNSE as the baseline, and the curves represent the coverage area increment of AGreedy, EGreedy, and NNSCB with respect to NNSE. It can be seen from the figure that AGreedy and EGreedy have large improvements compared to NNSE with respect to coverage area, and AGreedy performs best for all different completion numbers. The average coverage area of AGreedy is larger than that of EGreedy in the experimental results. This phenomenon may be caused by the different strategies to select workers. The entropy-based function adopted by EGreedy selects workers that are scattered around each task to the largest extent. In other words, workers selected for each task are distributed evenly around the task. As some tasks are close to each other, this uniform distribution increases the probability that the workers assigned for close tasks share some routes. On the contrary, the angle-based estimation function adopted by AGreedy selects workers for each task by a local greedy strategy: as long as two workers’ sectors do not overlap much, they can be selected at the same time, even they are located to the similar directions of the task. This property is useful to avoid route overlapping when selecting workers for close tasks, as workers selected for different tasks can reside on different directions when treating the nearby tasks as a whole. Fig. 7 also shows that, with the increment of the completion number k, the coverage increment rates of AGreedy and EGreedy decrease. This is because that, with the increment of the recruitment number, the diversity of workers selected by NNSE and NNSCB increases naturally. Finally, the coverage area increment of NNSCB is close to 0 on average, which indicates that the distance metric does not affect the coverage performance of the nearest neighbor strategy much. Fig. 8 further depicts the detailed trends by fixing the completion number $k = 3 , 5 , 7 , 9$ . It can be seen that, when fixing the completion number, the coverage area trends are similar to that of the average case discussed above.

The coverage efficiency of each algorithm is depicted in Fig. 9. The efficiency curves form two bunches: the higher bunch includes AGreedy and EGreedy, while the lower bunch is comprised of NNSCB and NNSE. Intuitively, the more workers we select in a given area, the more overlapped routes there are. Therefore, the efficiency values of all algorithms in the figure drop with the increment of the candidate size and the completion number. Given this fact, the proposed AGreedy and EGreedy perform consistently better than NNSCB and NNSE in all settings. The average efficiency increment of the bunch of AGreedy and EGeedy compared to the bunch of NNSCB and NNSE is around 5 percent, which indicates that there is still room to improve the coverage efficiency.

The query task completion rates of different algorithms are shown in Table II. The four compared algorithms have similar performance when we change the completion number k and the number of candidate workers. The rightmost column, which shows the average completion rates when we fix k, also certifies that the four algorithms perform comparably.

In summary, AGreedy and EGreedy are more effective than traditional nearest neighbor based strategies considering the sensing task coverage area and coverage efficiency.

# VII. CONCLUSION

In this paper, we introduced a novel spatial task assignment framework named SpatialRecruiter for hybridizing spatial crowdsourcing and crowdsensing. SpatialRecruiter intends to make the most of mobile workers by letting them complete location-based query and sensing tasks at the same time. In order to maximize the coverage area of selected workers, we proposed two coverage estimation functions to compute each worker’s utility for sensing. We then designed a greedy heuristic to select and assign workers by incorporating the completion requirement of query tasks and coverage requirement of sensing tasks. The experimental results on the real-world dataset demonstrated that the proposed techniques are more efficient than baseline approaches. In the future, we will extend our framework to consider the quality of workers as well as the location privacy of workers.

TABLE II COMPLETION RATES OF DIFFERENT ALGORITHMS 

<table><tr><td>#workers</td><td>algorithms</td><td>100</td><td>140</td><td>180</td><td>220</td><td>260</td><td>300</td><td>340</td><td>avg.</td></tr><tr><td rowspan="4">k=3</td><td>AGreedy</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0.9976</td><td>0.9961</td><td>0.9991</td></tr><tr><td>EGreedy</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0.9990</td><td>0.9998</td></tr><tr><td>NNSE</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0.9980</td><td>0.9997</td></tr><tr><td>NNSCB</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0.9971</td><td>0.9995</td></tr><tr><td rowspan="4">k=5</td><td>AGreedy</td><td>1</td><td>0.9957</td><td>0.9894</td><td>0.9781</td><td>0.9580</td><td>0.9390</td><td>0.9070</td><td>0.9667</td></tr><tr><td>EGreedy</td><td>1</td><td>0.9952</td><td>0.9815</td><td>0.9712</td><td>0.9577</td><td>0.9322</td><td>0.9088</td><td>0.9638</td></tr><tr><td>NNSE</td><td>0.9967</td><td>0.9952</td><td>0.9833</td><td>0.9697</td><td>0.9487</td><td>0.9211</td><td>0.8990</td><td>0.9591</td></tr><tr><td>NNSCB</td><td>0.9967</td><td>0.9952</td><td>0.9815</td><td>0.9712</td><td>0.9526</td><td>0.9233</td><td>0.9020</td><td>0.9603</td></tr><tr><td rowspan="4">k=7</td><td>AGreedy</td><td>0.9760</td><td>0.9457</td><td>0.9122</td><td>0.8590</td><td>0.7942</td><td>0.7410</td><td>0.6838</td><td>0.8445</td></tr><tr><td>EGreedy</td><td>0.9600</td><td>0.9405</td><td>0.8944</td><td>0.8364</td><td>0.7744</td><td>0.7200</td><td>0.6745</td><td>0.8286</td></tr><tr><td>NNSE</td><td>0.9600</td><td>0.9500</td><td>0.9019</td><td>0.8485</td><td>0.7936</td><td>0.7400</td><td>0.6902</td><td>0.8406</td></tr><tr><td>NNSCB</td><td>0.9667</td><td>0.9500</td><td>0.9056</td><td>0.8485</td><td>0.7949</td><td>0.7433</td><td>0.6922</td><td>0.8430</td></tr><tr><td rowspan="4">k=9</td><td>AGreedy</td><td>0.9010</td><td>0.8044</td><td>0.7206</td><td>0.6405</td><td>0.5750</td><td>0.5190</td><td>0.4691</td><td>0.6614</td></tr><tr><td>EGreedy</td><td>0.9210</td><td>0.8023</td><td>0.7206</td><td>0.6373</td><td>0.5792</td><td>0.5237</td><td>0.4744</td><td>0.6655</td></tr><tr><td>NNSE</td><td>0.9040</td><td>0.8064</td><td>0.7233</td><td>0.6400</td><td>0.5750</td><td>0.5187</td><td>0.4688</td><td>0.6623</td></tr><tr><td>NNSCB</td><td>0.9030</td><td>0.8064</td><td>0.7256</td><td>0.6423</td><td>0.5773</td><td>0.5210</td><td>0.4709</td><td>0.6638</td></tr></table>

# REFERENCES

[1] G. Chatzimilioudis, D. Zeinalipour-Yazti, A. Konstantinidis, and C. Laoudias, “Crowdsourcing with smartphones,” IEEE Internet Computing, vol. 16, no. 5, pp. 36–44, 2012.   
[2] L. Kazemi and C. Shahabi, “Geocrowd: enabling query answering with spatial crowdsourcing,” in Proceedings of ACM International Conference on Advances in Geographic Information Systems (GIS), 2012.   
[3] B. Hoh, T. Yan, D. Ganesan, K. Tracton, T. Iwuchukwu, and J. Lee, “Trucentive: A game-theoretic incentive platform for trustworthy mobile crowdsourcing parking services,” in Proceedings of IEEE International Conference on Intelligent Transportation Systems (ITSC), 2012.   
[4] X. Chen, E. Santos-Neto, and M. Ripeanu, “Crowdsourcing for on-street smart parking,” in Proceedings of ACM International Symposium on Design and Analysis of Intelligent Vehicular Networks and Applications (DIVANet), 2012.   
[5] H. Gao, G. Barbier, and R. Goolsby, “Harnessing the crowdsourcing power of social media for disaster relief,” IEEE Intelligent Systems, no. 3, pp. 10–14, 2011.   
[6] R. K. Ganti, F. Ye, and H. Lei, “Mobile crowdsensing: Current state and future challenges,” IEEE Communications Magazine, vol. 49, no. 11, pp. 32–39, 2011.   
[7] N. Maisonneuve, M. Stevens, M. Niessen, and L. Steels, “Noisetube: Measuring and mapping noise pollution with mobile phones,” Information Technologies in Environmental Engineering, pp. 215–228, 2009.   
[8] C. Costa, C. Laoudias, D. Zeinalipour-Yazti, and D. Gunopulos, “Smarttrace: Finding similar trajectories in smartphone networks without disclosing the traces,” in Proceedings of IEEE ICDE, 2011.   
[9] S. Matyas, C. Matyas, C. Schlieder, P. Kiefer, H. Mitarai, and M. Kamata, “Designing location-based mobile games with a purpose: collecting geospatial data with cityexplorer,” in Proceedings of ACM ACE, 2008.

[10] C. Wu, Z. Yang, and Y. Liu, “Smartphones based crowdsourcing for indoor localization,” IEEE Transactions on Mobile Computing, vol. 14, no. 2, pp. 444–457, 2015.   
[11] X. Zhang, Z. Yang, C. Wu, W. Sun, Y. Liu, and K. Xing, “Robust trajectory estimation for crowdsourcing-based mobile applications,” IEEE Transactions on Parallel and Distributed Systems, vol. 25, no. 7, pp. 1876–1885, 2014.   
[12] L. Kazemi, C. Shahabi, and L. Chen, “Geotrucrowd: trustworthy query answering with spatial crowdsourcing,” in Proceedings of ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (GIS), 2013.   
[13] S. He, D.-H. Shin, J. Zhang, and J. Chen, “Toward optimal allocation of location dependent tasks in crowdsensing,” in Proceedings of IEEE International Conference on Computer Communications (INFOCOM), 2014, pp. 745–753.   
[14] H. To, G. Ghinita, and C. Shahabi, “A framework for protecting worker location privacy in spatial crowdsourcing,” Proceedings of the VLDB Endowment, vol. 7, no. 10, pp. 919–930, 2014.   
[15] D. Deng, C. Shahabi, and U. Demiryurek, “Maximizing the number of worker’s self-selected tasks in spatial crowdsourcing,” in Proceedings of ACM International Conference on Advances in Geographic Information Systems (GIS), 2013.   
[16] D. Zhang, H. Xiong, L. Wang, and G. Chen, “Crowdrecruiter: selecting participants for piggyback crowdsensing under probabilistic coverage constraint,” in Proceedings of ACM International Joint Conference on Pervasive and Ubiquitous Computing (Ubicomp), 2014, pp. 703–714.   
[17] A. Ahmed, K. Yasumoto, Y. Yamauchi, and M. Ito, “Distance and time based node selection for probabilistic coverage in peoplecentric sensing,” in Proceedings of IEEE Communications Society Conference on Sensor, Mesh and Ad Hoc Communications and Networks (SECON), 2011.   
[18] X. Zhang, Z. Yang, Z. Zhou, H. Cai, L. Chen, and X. Li, “Free market of crowdsourcing: Incentive mechanism design for mobile sensing,” IEEE Transactions on Parallel and Distributed Systems, vol. 25, no. 12, pp. 3190–3200, 2014.   
[19] J. Burke, D. Estrin, M. Hansen, A. Parker, N. Ramanathan, S. Reddy, and M. Srivastava, “Participatory sensing,” 2006.   
[20] “University of california berkeley, 2008-2009,” http://traffic.berke ley.edu/.   
[21] B. Hull, V. Bychkovsky, Y. Zhang, K. Chen, M. Goraczko, A. Miu, E. Shih, H. Balakrishnan, and S. Madden, “Cartel: a distributed mobile sensor computing system,” in Proceedings of ACM International Conference on Embedded Networked Sensor Systems (SenSys), 2006.   
[22] P. Mohan, V. Padmanabhan, and R. Ramjee, “Nericell: rich monitoring of road and traffic conditions using mobile smartphones,” in Proceedings of ACM International Conference on Embedded Networked Sensor Systems (SenSys), 2008.   
[23] L. Pournajaf, L. Xiong, V. Sunderam, and S. Goryczka, “Spatial task assignment for crowd sensing with cloaked locations,” in Proceedings of IEEE International Conference on Mobile Data Management (MDM), 2014.   
[24] G. Cardone, L. Foschini, P. Bellavista, A. Corradi, C. Borcea, M. Talasila, and R. Curtmola, “Fostering participaction in smart

cities: a geo-social crowdsensing platform,” IEEE Communications Magazine, vol. 51, no. 6, pp. 112–119, 2013.   
[25] S. Hachem, A. Pathak, and V. Issarny, “Probabilistic registration for large-scale mobile participatory sensing,” in Proceedings of IEEE International Conference on Pervasive Computing and Communications (PerCom), 2013.   
[26] C. H. Liu, J. Fan, P. Hui, J. Wu, and K. K. Leung, “Towards qoi and energy-efficiency in participatory crowdsourcing,” IEEE Transactions on Vehicular Technology, 2014.   
[27] Z. Song, C. H. Liu, J. Wu, J. Ma, and W. Wang, “Qoi-aware multitask-oriented dynamic participant selection with budget constraints,” IEEE Transactions on Vehicular Technology, vol. 63, no. 9, pp. 4618–4632, 2014.   
[28] Y. Wen, J. Shi, Q. Zhang, X. Tian, Z. Huang, H. Yu, Y. B. Cheng, and X. Shen, “Quality-driven auction based incentive mechanism for mobile crowd sensing,” IEEE Transactions on Vehicular Techonology, vol. 64, no. 9, pp. 4203–4214, 2015.   
[29] D. Yang, G. Xue, X. Fang, and J. Tang, “Crowdsourcing to smartphones: incentive mechanism design for mobile phone sensing,” in Proceedings of ACM international conference on Mobile computing and networking (MobiCom), 2012.   
[30] C. Guestrin, A. Krause, and A. P. Singh, “Near-optimal sensor placements in gaussian processes,” in Proceedings of International Conference on Machine learning (ICML), 2005, pp. 265–272.   
[31] A. Krause, E. Horvitz, A. Kansal, and F. Zhao, “Toward community sensing,” in Proceedings of International Conference on Information Processing in Sensor Networks (IPSN), 2008, pp. 481–492.   
[32] A. Singla and A. Krause, “Incentives for privacy tradeoff in community sensing,” in Proceedings of AAAI Conference on Human Computation and Crowdsourcing (HCOMP), 2013.   
[33] H. Xiong, D. Zhang, G. Chen, L. Wang, and V. Gauthier, “Crowdtasker: maximizing coverage quality in piggyback crowdsensing under budget constraint,” in Proceedings of IEEE International Conference on Pervasive Computing and Communications (PerCom), 2015, pp. 55–62.   
[34] H. Xiong, D. Zhang, G. Chen, L. Wang, V. Gauthier, and L. Barnes, “icrowd: Near-optimal task allocation for piggyback crowdsensing,” IEEE Transactions on Mobile Computing, 2015.   
[35] H. Xiong, D. Zhang, L. Wang, J. P. Gibson, and J. Zhu, “Eemc: Enabling energy-efficient mobile crowdsensing with anonymous participants,” ACM Transactions on Intelligent Systems and Technology, vol. 6, no. 3, pp. 39:1–39:26, 2015.   
[36] H. Xiong, D. Zhang, L. Wang, and H. Chaouchi, “Emc3: Energyefficient data transfer in mobile crowdsensing under full coverage constraint,” IEEE Transactions on Mobile Computing, vol. 14, no. 7, pp. 1355–1368, 2015.   
[37] D. Golovin, M. Faulkner, and A. Krause, “Online distributed sensor selection,” in Proceedings of International Conference on Information Processing in Sensor Networks (IPSN), 2010, pp. 220–231.   
[38] X. Zhang, Z. Yang, W. Sun, Y. Liu, S. Tang, K. Xing, and X. Mao, “Incentives for mobile crowd sensing: A survey,” IEEE Communications Surveys and Tutorials, vol. 18, no. 1, pp. 54–67, 2016.   
[39] F. Bach, “Learning with submodular functions: A convex optimization perspective,” Foundations and Trends in Machine Learning, vol. 6, no. 2–3, pp. 145–373, 2013.   
[40] G. L. Nemhauser, L. A. Wolsey, and M. L. Fisher, “An analysis of approximations for maximizing submodular set functionsłi,” Mathematical Programming, vol. 14, no. 1, pp. 265–294, 1978.   
[41] J. Yuan, Y. Zheng, X. Xie, and G. Sun, “Driving with knowledge from the physical world,” in Proceedings of ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD), 2011.   
[42] J. Yuan, Y. Zheng, C. Zhang, W. Xie, X. Xie, G. Sun, and Y. Huang, “T-drive: driving directions based on taxi trajectories,” in Proceedings of ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (GIS), 2010.   
[43] P. Newson and J. Krumm, “Hidden markov map matching through noise and sparseness,” in Proceedings of ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems (GIS), 2009.

![](images/9d08fd4d50e00a236c72ca198c6447145e6d8eefafe4dc2d59a0725a5ccd71d5.jpg)



Xinglin Zhang received his B.E. degree in School of Software from Sun Yat-sen University, Guangdong, China, in 2010. He is currently with the School of Computer Science and Engineering, South China University of Technology. His research interests include wireless ad-hoc/sensor networks, mobile computing and crowdsensing. He is a member of the IEEE and the ACM.

![](images/868c388061e5f6c259e8c084c17d688e6be807b4f7a3832630ad275ca826a736.jpg)



Zheng Yang received a B.E. degree in computer science from Tsinghua University in 2006 and a Ph.D. degree in computer science from Hong Kong University of Science and Technology in 2010. He is currently an associate professor at Tsinghua University. His main research interests include wireless ad-hoc/sensor networks and mobile computing. He is a member of the IEEE and the ACM.

![](images/7cd06aca2f93437630c6c77aa36c0a6fbdbf886deb77a59873f61064333d724c.jpg)



Yue-Jiao Gong received the B.S. and Ph.D. degree in Computer Science from Sun Yat-sen University, China, in 2010 and 2014, respectively. She is currently a postdoc research fellow with the Department of Computer and Information Science, University of Macau. Her research interests include evolutionary computation, swarm intelligence, and their applications to big data and intelligent transportation scheduling. She is a member of the IEEE and the ACM.

![](images/401982947d3e310c717ddf168bac9eaa2bf89669f7440ea92586d44e9c8f8785.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is Chang Jiang Chair Professor and Dean of the School of Software at Tsinghua University. His research interests include wireless sensor network, peerto-peer computing, and pervasive computing. He is a fellow of the IEEE and a fellow of the ACM.

![](images/d735e3ed241721c157fc40cfa2b930fc3f9cb7996e6c138e289dcba57595d362.jpg)



Shaohua Tang received the B.Sc. and M.Sc. Degrees in applied mathematics, and the Ph.D. Degree in communication and information system from the South China University of Technology, in 1991, 1994, and 1998, respectively. He is a full professor with the School of Computer Science and Engineering, South China University of Technology. His current research interests include information security, networking, and information processing. He is a member of the IEEE and the IEEE Computer Society.