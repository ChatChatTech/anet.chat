# OLearning: A Geo-Distributed System for Device-Cloud Collaborative Computing

Min Fang1(\*), Zhihui Fu1(\*), Xiangmou Qu1, Ruiguang Pei1, Jun Wang1(), and Lan Zhang2

1 OPPO Research Institute, Shenzhen, China mfang.cs@gmail.com, {luca, lokinko, peiruiguang}@oppo.com, junwang.lu@gmail.com

2 University of Science and Technology of China, Hefei, China zhanglan@ustc.edu.cn

Abstract. Device-cloud collaborative computing (e.g., federated learning) is an efficient model training paradigm to combine the cloud and distributed edge devices without leaking the raw data. A co-computing round includes: 1) devices get the latest model weights from the cloud and train locally; 2) the cloud aggregates model delta weights from devices into a new model. However, existing systems ignore the heterogeneity of devices under geo-distribution, introducing three new challenges: 1) devices span multiple time zones, the cloud may need one day to collect enough delta weights, greatly slowing down a training round; 2) devices have various data distribution, pre-assigning tasks to maximize training efficiency is difficult; 3) massive delta weights may arrive at unpredictable times, the cloud must reserve huge resources for peak requests. To fill the gap, we propose OLearning, a geo-distributed production system. Specifically, OLearning 1) applies a two-layer multi-zone architectural design. The first layer performs inter-zone model weight aggregation from multiple zones of the second layer, while the second layer performs intra-zone model weight aggregation from selected devices. 2) avoids pre-assigning training tasks and instead adds a profit indicator for each task, allowing devices to decide task scheduling orders by themselves. 3) deploys a shared-task resource cluster for aggregating millions of weights over undetermined arrived times. Comprehensive experiments on the public dataset show the effectiveness and robustness of OLearning.

Keywords: Device-cloud · Co-computing · Geo-distribution.

# 1 Introduction

With the growing demand for personal privacy and the introduction of various rigorous data protection regulations (such as GDPR), cross-device collaborative computing (e.g., federated learning) has become a research hotspot in both industry [1, 2] and academia [3, 4]. This paradigm uses a large-scale edge device (distributed worldwide) to collaboratively train high-quality models, while devices only share model updates with the cloud rather than raw data. A standard co-computing process consists of multiple rounds of device-to-cloud interactions until the target model accuracy is reached. In each round, a device first pulls the latest model weight from the cloud, then executes the assigned co-computing task to obtain model weight updates. After collecting enough weight updates, the cloud aggregates them as the next round model weight [2]. Within a round, the cloud usually has two core parts, namely 1) Selection: cherry-picking participants for a co-computing round via a given selection mechanism (e.g., random [1]); 2) Aggregation: aggregating updates reported by participants via a given aggregation mechanism (e.g., FedAvg [5]) for next co-computing round.

Although there are already some open-source frameworks, such as FedML [6] and Flower [7], they all overlook the geo-distribution uniqueness of edge devices in their design, introducing three new challenges as follows.

1) Unacceptable single-round co-computing time. In the traditional single-layer case, devices participating in a co-computing round may be distributed across multiple time zones. Hence, the cloud needs at least a full day to collect enough delta weight updates and generate a new model.

2) Inefficient resource utilization with multiple time zones. In a cross time zones scenario, it is difficult for the cloud to assess the data quantifies of edge devices in each zone. Although some works [3,4] propose better-performing participant selection mechanisms from data and system heterogeneity, they ignore the heterogeneity in the available time window of devices under geo-distribution.

3) Long-term enormous resource allocation in the cloud. Due to the huge differences in device available time windows caused by geographical locations, the cloud resources may be idle most of the time. Meanwhile, the pre-configured resources may not effectively handle sudden spikes from devices.

To address the above challenges, we design and implement a novel devicecloud collaborative computing system, named OLearning. OLearning adopts a two-layer multi-zone architectural design, where devices within each zone can perform multiple rounds of local computing, and global aggregation periodically aggregates weights across zones. Further, OLearning introduces a decentralized selector, which only announces task rewards based on training contributions across zones and training processes within each zone. Then, devices select the optimal task set to register into selector by further evaluating their data quality and available time. Lastly, OLearning implements a shared-task computing cluster and addresses inefficiencies in multi-task scenarios by enabling resource sharing. The main contributions of this paper are summarized as follows:

– We propose OLearning, a novel two-layer device-cloud collaborative computing system that first integrates geo-distribution factors into its design.

– We design a decentralized selector mechanism to optimize task assignment based on training contributions and device-specific factors.

– We deploy a shared-task computing cluster to improve resource utilization in the multi-task scenario.

We conduct extensive experiments to evaluate the performance and effectiveness of OLearning. The experiments present that OLearning can outperform the state-of-the-art work, and fully utilize the resources both in devices and cloud.

# 2 Related Work

As awareness of data privacy and security grows, the device-cloud computing paradigm has shifted from a cloud-centric one to a device-centric one, which enhances privacy protection and improves response speed. Furthermore, it is gradually evolving to device-cloud co-computing to integrate multi-party knowledge from enormous edge devices. These three paradigms have satisfied diverse application needs [8], and Fig. 1 illustrates their typical workflows.

Cloud-centric computing: a centralized computing paradigm, as shown in Fig. 1(a), where devices report data to the cloud, all training and inference are done in the cloud-side, and only inference results are returned to devices. Currently, this one is widely used in multiple scenarios, e.g., the recommendation system in short-form video applications. However, it faces high data privacy risks and cannot be applied in critical applications, e.g., face recognition.

Device-centric computing: a distributed computing paradigm, as shown in Fig. 1(b), where the cloud publishes the pre-trained model to devices, then devices train and infer locally without sharing the raw data, e.g., on-device text-toimage search [9]. Although this one can mitigate privacy leakage risk, the model cannot benefit from other device data due to information isolation.

Device-cloud co-computing: a hybrid computing paradigm, as shown in Fig. 1(c), where the cloud issues the global model to devices for local execution (device-centric computing), and only parameters are returned for aggregation (cloud-centric computing), e.g., Apple’s automatic speech recognition [2]. Since this one introduces a significant burden in handling device faults and managing cloud computing resources, many co-computing frameworks [1, 2, 6, 7] have emerged. These frameworks mainly optimize two core components:

1. A precise selector to choose participating devices for each training round based on factors such as device availability, data quality, and more.   
2. An efficient aggregator to aggregate delta weights updates from edge devices and maximize the utilization of cloud computing resources.

However, existing frameworks cannot efficiently support geo-distributed scenarios due to the lack of consideration for uncertain device availability and cloud computing resource requirements across different time zones. The importance of these considerations is discussed in §3.

![](images/3b337a22bd45a385bafc51cf8d6ca12cc253c9861d8d8fc4faa0d0d56282f6ef.jpg)



(a) Cloud-centric.

![](images/bd1a403da5c418c80ea6216c42fabf5e235b3987232c20c900b64b4da45e19e1.jpg)



(b) Device-centric.

![](images/98011744ded7ec96c4ccc02ae23b40d231268cce6cdf45937acf20dabd76e933.jpg)



(c) Device-cloud.   
Fig. 1: Device-cloud computing paradigm.

# 3 Motivation

This section depicts key limitations of existing technologies that motivated ours. Limitation#1: Lack of attention to geo-distribution in participant selection. Existing participant selection methods [1, 3, 4] overlook the heterogeneous behavior of enormous edge devices in real device-cloud collaboration scenarios, e.g., having different available time windows due to different time zones. Nevertheless, the geo-distribution of participants plays a crucial role in a crossdevice co-computing task, for the following main reasons:

– Availability. Due to the uncertainty of geo-distribution, the active time of devices may vary greatly. If the server selects inactive devices as participants, the task may not be responded to promptly, affecting co-computing efficiency.   
– Synchronization. In a co-computing process, each participant must return results within a specified time. If the location factor is ignored, some devices may be unable to upload local updates in time, resulting in high latency.   
– Fairness. If the server ignores location factors when selecting participants, devices in certain time zones may be chosen more frequently, while those in other time zones are overlooked. Undoubtedly, this may raise issues of fairness.

Therefore, the geo-distribution factor may have a negative impact on the effectiveness of co-computing and should be considered when picking participants. Limitation#2: Larger cloud-side resource wastage in multi-tasking. Existing cloud-side aggregation services are designed to be strongly correlated with the number of tasks [1, 2], i.e., allocating specific aggregation service resources to each task at initialization, resulting in the required resources growing linearly with the number of tasks. Fig.2 shows an example, where multiple persist aggregators are created and assigned to each task individually based on available public resources. However, in real-world application deployment, due to geographical differences, the available time windows of edge devices have obvious heterogeneity. Thus, the aggregation services bound to tasks are not always busy and the corresponding allocated resources are idle, cause a huge resource wastage. Besides, the initialized resource configuration method makes it difficult for existing work to effectively respond to variable traffic peaks from participants.

# 4 Overview of OLearning

This section first shows the system overview of OLearning, and then describes the whole device-cloud co-computing process of OLearning.

# 4.1 Architecture

Fig.3 illustrates the architecture of OLearning, including globally distributed edge devices, a centralized Global Coordinator, and multiple Zone Coordinators organized by geo-location (e.g., time zones).

![](images/2393fea52569949acb4f1cd4987ddd30d3b11b3ac4a19f68a4679de603f4f177.jpg)



Fig. 2: Traditional aggregator

![](images/f8edf237dbcd625794d6b348e91d0b2f856150488f9fb7c7c3aec59b0ea082a8.jpg)



Fig. 3: System architecture of OLearning

Global Coordinator integrates three core modules to manage system-wide operations: 1) Configurator handles task assignment and device management; 2) Global Selector evaluates and prioritizes the contributions of different zones for each task, guiding task distribution; 3) Global Aggregator collects updates from all zones to product the final global model, enabling cross-zone collaboration.

Each Zone Coordinator runs independently and contains two key components: 1) Zone Selector evaluates tasks training processes at one round and assigns it as rewards to devices; 2) Zone Aggregator aggregates updates from devices to get the zone-level model, supporting iterative training within the zone.

Edge devices are distributed worldwide in vast numbers. They exhibit significant data heterogeneity and are dynamically associated with specific zones based on their geo-location. As devices move across zones, they seamlessly transition between zones to maintain continuous participation in OLearning.

# 4.2 Co-computing Process across Zones

In geo-distributed applications, OLearning implements a two-layer co-computing mechanism to effectively utilize zone-specific variations in available time windows and data distributions. By integrating inter-zone and intra-zone collaboration, the framework supports decentralized decision-making, enhancing scalability, adaptability, and task execution efficiency in dynamic real-world scenarios.

Inter-zone Co-computing Interaction. OLearning adopts an epoch-based inter-zone co-computing flow, where an epoch is a user-defined interval defined by criteria such as time windows or computation rounds in a zone. Shorter epochs allow more frequent global aggregation, enabling finer-grained synchronization and adaptability. The inter-zone process, shown in Fig.4(a), has three key stages:

❶ Preparation: Global Selector evaluates the potential contribution of each zone to the task and assigns a reward score accordingly (see §5.1). Then, Global Coordinator disseminates task details (e.g., model structure), aggregated weights from the last epoch, and zone-specific reward scores to all participating zones.   
❷ Execution: Zones engage in inter-zone collaborative computation for the current epoch, conducting multiple rounds of local computing and coordination.   
❸ Finalization: Global Aggregator collects updates from all selected zones and performs aggregation to generate the model weights for the next epoch.

![](images/eec6db096f7f5001ea77ad6f2c8af31c5102630f1ad21aca9f91b05c6ae533fd.jpg)



![](images/2ca80ad144fdbb67767f5ef5b219e0ca5e2af4f44e0f45d536ca9c925525b6d0.jpg)



Fig. 4: Description of the whole process

Intra-zone Co-computing Interaction. OLearning uses a round-based intrazone co-computing flow, where tasks are trained iteratively until the epoch stop condition is met. The intra-zone process, shown in Fig.4(b), has four key stages:   
① Reward Announcement: Zone Selector evaluates task progress and sets reward scores, a lower score means that the task is closer to convergence (see §5.1).   
② Registration: Devices receive reward scores from Global Selector and Zone Selector s and get final task-specific rewards by incorporating local data quality. Using this, each device determines an optimal task set based on its availability window and registers for selected tasks via Zone Coordinator (see §5.2). Once enough devices register for a task, other registration attempts are rejected, prompting those devices to select another task. To prevent low-priority tasks from starving, Zone Selector adds rewards for such tasks in subsequent rounds.   
③ Computation: Registered devices perform local computing via a predefined task scheduling policy and upload the got update weights to Zone Aggregator.   
④ Aggregation: Zone Aggregator merges local updates from devices to get nextround zone model. This iterative continues until the epoch concludes (see §6).

# 5 Decentralized Selector

To address uncertainty in data quality and availability for geo-distributed devices, OLearning designs a decentralized selection mechanism. Specifically, a task is first scored independently by Global Selector, Zone Selector, and device (§5.1). Then, each device selects the optimal task set based on its local status (§5.2).

# 5.1 Announce Task Reward

The reward of task t depends on: 1) the training profit of $z o n e _ { i }$ against other zones; 2) the training progress of round $r _ { j }$ in zonei; 3) the data quality of devicek.

Global Selector Reward. Global Selector quantifies the relative contribution of zonei by measuring how far its weights, $\mathbf { W } ^ { z o n e }$ i , deviate from the global aggregated weights, $\mathbf { W } ^ { g l o b a l }$ . This deviation is calculated using the L2 norm of the difference between ${ \bf W } ^ { z o n e _ { i } }$ and $\mathbf { W } ^ { g l o b a l }$ . To ensure comparability of contributions across zones and tasks, Eqn.1 normalizes the deviation of zonei by the total deviation of all n zones. $C o n t r i b ( z o n e _ { i } )$ is the proportion of each zone’s influence on the task. A smaller Contrib(zonei) means that the model matches the data in zonei better, and the profit from further training in zonei is smaller.

$$
C o n t r i b (z o n e _ {i}) = \frac {| \mathbf {W} ^ {z o n e _ {i}} - \mathbf {W} ^ {g l o b a l} | _ {2}}{\sum_ {i = 1} ^ {n} | \mathbf {W} ^ {z o n e _ {i}} - \mathbf {W} ^ {g l o b a l} | _ {2}} \tag {1}
$$

Zone Selector Reward. Zone Selector evaluates the training progress of zonei at round $r _ { j }$ . Specifically, it uses Eqn.2 to capture reductions in both gradient magnitude and loss value between consecutive iterations. In Eqn.2, ∇Wzoneir denotes the gradient of the weight vector for zonei at round $r _ { j } ,$ while $L o s s _ { r _ { i } } ^ { z o n e _ { i } }$ is the corresponding loss value. The first term in Eqn.2 calculates the relative reduction in gradient magnitude, providing a measure of convergence stability. The second term quantifies the proportional reduction in loss value, ensuring that only non-negative improvements contribute to the progress metric. To address potential numerical instability, a small constant ϵ is added to the denominators of both terms. A smaller $P r o g r e s s ( r _ { j } )$ means that the training process in zonei has slowed down, and further training in $z o n e _ { i }$ may yield diminishing profit.

$$
P r o g r e s s (r _ {j}) = \left(\frac {| \nabla \mathbf {W} _ {r _ {j} - 1} ^ {z o n e _ {i}} | _ {2} - | \nabla \mathbf {W} _ {r _ {j}} ^ {z o n e _ {i}} | _ {2}}{| \nabla \mathbf {W} _ {r _ {j} - 1} ^ {z o n e _ {i}} | _ {2} + \epsilon}\right) ^ {2} \times \max \left(0, \frac {L o s s _ {r _ {j} - 1} ^ {z o n e _ {i}} - L o s s _ {r _ {j}} ^ {z o n e _ {i}}}{L o s s _ {r _ {j} - 1} ^ {z o n e _ {i}} + \epsilon}\right) (2)
$$

Device Reward. Eqn.3, derived from Oort [3], evaluates the data quality of a device by considering the amount of data, denoted as |Data|, and the associated loss values. It measures the potential contribution of a device to a training round.

$$
Q u a l i t y (d e v i c e _ {k}) = | D a t a | \sqrt {\frac {1}{| D a t a |} \sum_ {d \in D a t a} L o s s (d) ^ {2}} \tag {3}
$$

Task Final Reward. Eqn.4 defines the total profit of a devicek within a zonei during an intra-zone round $r _ { j }$ as the product of the above three factors.

$$
P r o f i t (z o n e _ {i}, r _ {j}, d e v i c e _ {k}) = C o n t r i b (z o n e _ {i}) P r o g r e s s (r _ {j}) Q u a l i t y (d e v i c e _ {k}) \tag {4}
$$

Further, the reward of task t (rewardt) applies a logarithmic transformation to the profit, which compresses large values to maintain numerical stability and reduce the impact of outliers, while preserving the relative ordering of profits.

$$
r e w a r d _ {t} = \frac {\log (1 + P r o f i t (z o n e _ {i} , r _ {j} , d e v i c e _ {k}))}{1 + \log (1 + P r o f i t (z o n e _ {i} , r _ {j} , d e v i c e _ {k}))} \tag {5}
$$

# 5.2 Determine Preregistered Task

Given a set of tasks and their rewards, the device calculates the optimal subset of tasks based on its available time. Generally, a device has m different available time slots (the longest continuous available time window), which can be predicted based on the historical operation by an on-device model. To simplify on-device task management, each task must be completed within a single and continuous time slot. Then, we can define a action $r e g ( t , s l o t _ { i } ) \in \{ 0 , 1 \}$ as whether the device executes task t at the available time sloti $( i = 1 , . . . , m )$ . A task t executes at most once across all slots, which can be formulated as the constraint in Eqn.6.

$$
r e g (t, s l o t _ {i}) \in \{0, 1 \}, t \in T, i = 1, \dots , m; \sum_ {i = 1} ^ {m} r e g (t, s l o t _ {i}) \leqslant 1, t \in T \quad (6)
$$

Meanwhile, a device can execute at most one task at a time to reduce resource contention. The total time of tasks in a slot must be less than its available time, which can be formulated as the constraint in Eqn.7. The timet depends on the amount of data on the device and the training speed for the on-device model.

$$
\sum_ {i = 1} ^ {m} \text { time } _ {t} \cdot \text { reg } (t, \text { slot } _ {i}) \leqslant \text { slot } _ {i}, i = 1,..., m \tag {7}
$$

Therefore, the on-device multi-task scheduling problem is to select a subset of disjoint tasks from T that maximizes the total reward of the selected tasks, which can be formally defined as follows:

$$
\max \sum_ {t \in T} \sum_ {i = 1} ^ {m} r e w a r d _ {t} \cdot r e g (t, s l o t _ {i}) \tag {8}
$$

Combine constraints in Eqn.6 and Eqn.7 with objective goal Eqn.8, we construct a standard 0-1 Multiple Knapsack Problem (MKP) [10], which is NP-hard. In OLearning, we solve it with a constraint programming solver [11] for smallscale scenarios and a greedy strategy [12] for large-scale scenarios.

# 6 Elastic Aggregator

In geo-distributed applications, the real-time availability status of devices varies with user activities, leading to large variations in the number of devices and total computational load across different tasks. Thus, we cannot predict in advance the size of the total aggregation resources required for each task, nor can we allocate the corresponding persistent aggregators. Given this, OLearning employs an elastic aggregator manager to schedule a set of shared-task aggregators, and integrates a multi-actor design to cope with concurrent aggregation requests.

Shared-Task Aggregator. OLearning adopts a unified shared-task aggregator design, with task allocation and tracking coordinated by a global manager. This architecture is supported by a shared pool of computing resources accessible to all aggregators. Within the shared resource pool, each actor can receive task-specific weights. A proxy component routes device requests to actors by consistent hashing [13], leveraging device IDs as hash keys. This mechanism ensures load balancing and minimizes the likelihood of actor hotspots. Upon receiving weights, each actor determines the running aggregator according to the manager’s instructions. Once an actor finishes the weight aggregation for a task, it transmits the intermediate results to a leader actor designated by the manager. The leader actor then performs the final aggregation to get the task’s output. This design ensures that all aggregators share computing resources while balancing weight storage at the actor level. If an actor crashes, the system relies on participants of the task to re-upload the lost weights.

Real-Time Aggregated Task Scheduling. The elastic aggregator manager periodically collects metadata from all actors, including the weight arrival rate and remaining unaggregated weights for each task. Using this global view, the manager prioritizes tasks across all actors based on the following criteria:

1. Arrival Rate: Tasks with higher weight arrival rates are given priority to ensure efficient processing of incoming data.   
2. Remaining Workload: For tasks with equal arrival rates, priority is assigned based on the number of remaining unaggregated weights to reduce the overall average aggregation completion time.

This scheduling strategy ensures that the system efficiently utilizes shared computing resources while minimizing the latency of task aggregation. By dynamically adjusting priorities based on real-time metrics, OLearning achieves a balanced trade-off between resource sharing and aggregation performance.

# 7 Experiments

In this section, we evaluate the effectiveness of OLearning from multiple dimensions and target to answer the following questions:

– Q1 (§7.1): Does the selection mechanism in OLearning outperform the stateof-the-art work for various cross-devices co-computing applications?   
Q2 (§7.2): How effective is the on-device multi-task scheduling employed in OLearning when facing multi-task scenarios?   
– Q3 (§7.3): How is the resource overhead of shared-task aggregation methods when deploying OLearning on real production environment?

# 7.1 Performance of Selection Mechanism

All evaluations for this set of experiments are conducted using 4 NVIDIA GeForce RTX 3090 GPUs, each used to simulate one zone. The details are as follows.

Datasets and models. We evaluate OLearning on two public datasets designed for cross-device co-computing applications at different scales:

– Google Speech3: The dataset for speech recognition, consisting of about 100, 000 audio commands from more than 2, 000 clients. Based on the dataset, we train the ResNet-34 [14] model for a 20-class speech recognition task.   
– HARBox4: The 9-axis IMU data about human daily activity recognition, which is collected from 121 users’ smartphones via crowdsourcing. We train the lightweight customized DNN model in PyramidFL here.

![](images/5bee968a07d901d3bda117847fcb57f1f3408dd7baf1cc479b78a603c2e69954.jpg)



(a) 2 zones

![](images/6afb963d36f9a89b35ce48ba9416a6d0c9bff120f7328cdf7e51a7438efbdc13.jpg)



(b) 3 zones

![](images/265b9933da0ef98c7afa6a67fb6cf22191b42955ae1aa360629c44ee66994cf5.jpg)



(c) 4 zones

Fig. 5: Day-to-accuracy for speech recognition on Google Speech dataset   
![](images/b858bef1fb9436a497a9082ecc43ceb09013d6860c73647e6710d9183fbd2a81.jpg)



(a) 2 zones

![](images/78d3ac7283500c7404a825648975a3e87f1455b16891812d1f3c6aaad08034a4.jpg)



(b) 3 zones

![](images/782bb2aa987fba96bce1e4d83ace137acf14936bf8b44d393f854cfa9e446333.jpg)



(c) 4 zones   
Fig. 6: Day-to-accuracy for human activity recognition on HARBox dataset

Baselines and optimizers. We compare the participant selection strategy of OLearning with the state-of-the-art PyramidFL [4]. Yogi [15] and Prox [16] are used to assess the generality of the designed method across different optimizers.

Metrics. We use day-to-accuracy as a metric to measure OLearning, i.e., the total simulation day for a model training task on the testing set to reach a target accuracy. For each experiment, we report the average accuracy over 3 runs.

Parameters. In OLearning, the inter-zone epoch E=100 simulates the time zone differences under geo-distributed, where one epoch represents a day. Besides, inter-zone updates are uploaded to Global Aggregation only when Zone Aggregator completes 10 rounds aggregation. Thus, there are $R { = } E * 1 0 { = } 1 0 0 0$ intra-zone rounds in OLearning, and others is R=E. For a task requiring |Z| ∗ K (K=20) participants, we collect updates from the first K completed participants out of 1.3K during each intra-zone round to alleviate the impact of stragglers. All settings related to selection strictly follow the baseline PyramidFL [4].

Accuracy with different number of zones. We compare the accuracy change of OLearning with PyramidFL on the Google Speech and HARBox datasets over the simulation days, as shown in Fig.5 and 6. Results show that OLearning can always reach the final accuracy in a shorter simulation day, and then begin to fluctuate slightly. For PyramidFL, 100 simulation days are not enough to converge. Based on this, OLearning can greatly reduce the time cost of co-computing by applying an early exit mechanism [17], while ensuring high accuracy and usability of the final model. Multiple tests with different numbers of zones further demonstrate the strong horizontal scalability of OLearning. Compared to HAR-Box with a smaller data size, OLearning performs significantly better than PyramidFL on Speech dataset. From Fig.5, ResNet-34 performs better on Prox over

![](images/203a8b887ef248d576170ee385c17740b1470acf58f0fe6988d7bd2fe786aa3b.jpg)



(a) m=10

![](images/03d220d8b3323076e315ab674615e7014a5b4edfbc2139998b210d05e91d24ab.jpg)



(b) m=30

![](images/02f753d13d6b282142869ee4f29f011a9ae6f05f3ecac6d9877c65feafefed2e.jpg)



(c) m=50

Fig. 7: Total profit under $n _ { d _ { k } }$ free time slots against the number of tasks   
![](images/55c341cff05e4eeabf0edfefe626dd07de184950cd81ffbc325fb3f56e426c32.jpg)



(a) m=10

![](images/b5220598396327e860853ace186f186b0fa87826ff1f2e32260e6fd47de428d6.jpg)



(b) m=30

![](images/1e12c5f946582a00a8c97419afc01159a38e5b81afdbf94d057698dafab4674d.jpg)



(c) m=50   
Fig. 8: Total profit under $n _ { d _ { k } }$ free time slots against the solve time limit

Yogi with Speech dataset. Yet, regardless of the optimizer used, OLearning can always reach a local optimum in about 30 simulation days for varying numbers of zones. Taking 4 zones in Fig.5(c) as an example, the accuracy improves about 37.82% for Prox and 30.95% for Yogi against PyramidFL. For the customized DNN with HARBox dataset in Fig.6, although Yogi outperforms Prox, OLearning still outperforms PyramidFL and reaches a local optimum at about 30 simulation days. Similarly, for 4 zones in Fig.6(c), compared with PyramidFL, OLearning gets about 15.04% improvement for Prox and 16.62% for Yogi. In summary, Fig.5 and 6 demonstrate the robust speedup of OLearning, which is not impacted by different optimizers under the same model and datasets.

# 7.2 Robustness of On-device Multi-task Scheduling

We use Linux machine configured with i9-10900K 3.70G 20c/64g/1T as virtual device and conduct experiments to verify the effectiveness of our multi-task scheduling mechanism in §5.2. Recall that there are m available time slots in a device. In the experiment, each slot is randomly from 1-10min, and the reward of each task is randomly from 0.01-1. With varying numbers of tasks and m, we count the profit on the device under different methods, i.e., MKP with Google OR-Tools [11] and profit-maximizing greedy [12]. Fig.7 and 8 give detailed results, where each value averages over 5 runs.

Since the solver may get different optimal solutions under the varying solving time limits, we limit the upper bound of the MKP solve time in Fig.7 to 2s, an acceptable time range for a device. The Max in Fig.7 is a globally optimal solution obtained with 60s solve time limit. Results show that, when the number of tasks is small (≤ 150), MKP is basically equal to Max regardless of the value of $n _ { d _ { k } }$ . The difference between MKP and Max is only obvious when m and the number of tasks increases, since the large scale of solving the problem. In contrast, Greedy can reach the same effect as MKP and Max with larger m and smaller tasks (Fig.7(b) and $7 ( \mathrm { c } ) )$ , but it performs poorly with smaller $\left( { \mathrm { F i g . 7 ( a ) } } \right)$ m or larger tasks $\mathrm { ( F i g . 7 ( b ) }$ and 7(c)). Although MKP may be subject to the solve time limit, results in Fig.8 show that the optimal solution is obtained in less than 2s. Note that the value 0 in Fig.8(b) and 8(c) means the solver cannot get an optimal solution under the given time limit. MKP-T# or Greedy-T# denotes the number of tasks is $\#$ for the method. Besides, MKP can achieve an effect comparable to Greedy with a shorter time limit when m is small. However, as the problem complexity rises, such as in Fig.7(c) and 8(c) when m=50 with tasks exceed 200, 2s solve time limit is no longer sufficient for the solver to get a optimal solution. Thus, in real design, one should dynamically choose between MKP or Greedy according to m and the number of tasks to achieve max profits.

![](images/7f402b80e9d07219f3bc382c3bb554bcc2726aee5fe56f09ffb6dc94c5fe5ef1.jpg)



Fig. 9: Storage Consumption

# 7.3 Aggregation In Production

This set of experiments thoroughly evaluates the robustness and efficiency of the aggregation module in OLearning when facing a real production environment.

Comparison of Aggregator. We have collected statistics on the storage resource occupancy of cloud aggregation services over 24 hours on the OPPO device-cloud co-computing online business platform, as shown in Fig.9. The vertical axis represents the resource usage percentage, calculated with the peak value of 100%. In the traditional task-oriented aggregation mechanism, messages reported by edge devices are first cached until certain conditions are met before aggregation begins. This not only leads to idle computing resources during the waiting process, but also causes long-term over-occupation of storage resources, as shown in Fig.9. Conversely, our shared-task aggregation starts computing once receiving messages, thereby smoothing out the computational peaks, and minimizing the time overhead and resource occupancy. Besides, we measure the performance improvement of shared-task aggregation in real-world online industrial scenarios and found that in most cases, it can achieve efficiency improvement of over 40% to 50%, while requiring fewer computational resources.

# 8 Conclusion

In this paper, we present OLearning, a novel device-cloud collaborative computing framework leveraging a two-layer multi-zone architecture, decentralized task selection, and shared-task resource optimization. By integrating geo-distribution factors and enhancing resource utilization, our experiments presents that OLearning effectively addresses key inefficiencies in multi-task and distributed scenarios.

# References

1. Bonawitz, K., Eichner, H., et al.: Towards federated learning at scale: System design. Proceedings of machine learning and systems 1, 374–388 (2019)   
2. Paulik, M., Seigel, M., Mason, H., et al.: Federated evaluation and tuning for ondevice personalization: System design & applications. arXiv:2102.08503 (2021)   
3. Lai, F., Zhu, X., Madhyastha, H.V., Chowdhury, M.: Oort: Efficient federated learning via guided participant selection. In: OSDI. pp. 19–35 (2021)   
4. Li, C., Zeng, X., Zhang, M., Cao, Z.: Pyramidfl: A fine-grained client selection framework for efficient federated learning. In: MobiCom. pp. 158–171 (2022)   
5. McMahan, B., et al.: Communication-efficient learning of deep networks from decentralized data. In: Artificial intelligence and statistics. pp. 1273–1282 (2017)   
6. Next-Gen Cloud Services for LLMs & Generative AI: (2023), https://fedml.ai/   
7. Flower: A Friendly Federated Learning Framework: (2023), https://flower.dev/   
8. Yao, J., Zhang, S., Yao, Y., Wang, F., et al.: Edge-cloud polarization and collaboration: A comprehensive survey for ai. IEEE TKDE 35(7), 6866–6886 (2022)   
9. Copy and translate text from photos on your iPhone or iPad: (2023), https://support.apple.com/en-sg/HT212630   
10. Martello, S., Toth, P.: A bound and bound algorithm for the zero-one multiple knapsack problem. Discrete Applied Mathematics 3(4), 275–288 (1981)   
11. Google: OR-Tools (2024), https://developers.google.com/optimization/pack   
12. Martello, S., Toth, P.: Algorithm 632: A program for the 0–1 multiple knapsack problem. ACM Trans. Math. Softw. 11(2), 135–140 (Jun 1985)   
13. Karger, D., et al.: Consistent hashing and random trees: Distributed caching protocols for relieving hot spots on the world wide web. In: STOC. pp. 654–663 (1997)   
14. He, K., Zhang, X., Ren, S., Sun, J.: Deep residual learning for image recognition. In: CVPR. pp. 770–778 (2016)   
15. Reddi, S., Charles, Z., Zaheer, M., Garrett, Z., Rush, K., Konečn\`y, J., Kumar, S., McMahan, H.B.: Adaptive federated optimization. arXiv:2003.00295 (2020)   
16. Li, T., Sahu, A.K., Zaheer, M., et al.: Federated optimization in heterogeneous networks. Proceedings of Machine learning and systems 2, 429–450 (2020)   
17. Schuster, T., Fisch, A., Gupta, J., Dehghani, M., Bahri, D., Tran, V., Tay, Y., Metzler, D.: Confident adaptive language modeling. NeurIPS 35, 17456–17472 (2022)