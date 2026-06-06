# FedWM: Federated Crowdsourcing Workforce Management Service for Productive Laziness

Zhuan Shi∗, Zhenyu Yao†, Liping Yi‡, Han Yu§, Lan Zhang∗, Xiang-Yang Li∗

∗ School of Computer Science and Technology, University of Science and Technology of China, China

† Department of Mathematical Sciences, Univerisity of Liverpool, United Kingdom

‡ College of Computer Science, Nankai University, China

§ School of Computer Science and Engineering, Nanyang Technological University, Singapore

zhuanshi@mail.ustc.edu.cn, sgzyao7@liverpool.ac.uk, yiliping@nbjl.nankai.edu.cn,

han.yu@ntu.edu.sg, zhanglan03@gmail.com, xiangyangli@ustc.edu.cn

Abstract—Federated crowdsourcing, as a dynamic privacypreserving distributed machine learning approach, has attracted significant research attention recently. Compared to federated learning (FL), clients can dynamically collect and label fresh data as required, and train model on the updated data. Existing research has mainly focused on incentivizing clients to spend more effort on data collection and labelling in order to improve FL model performance. However, as data collection and labeling require human effort, they need to balance work and rest. This need has been overlooked by existing federated crowdsourcing research. In this paper, we propose the Federated Workforce Management (FedWM) approach to bridge this important gap. It first measures the contribution of each client to the FL model, and estimates the urgency collecting new labelled data based on the rate of change of the contribution. Then, FedWM computes the working time taking into account of the client’s maximum productivity and self-reported mood. Finally, it takes both the urgency level of obtaining new data and clients’ productivity into consideration to provide scheduling services that advise the clients on work-rest balance in a given time slot based on Lyapunov optimization. Through theoretical analysis, we provide the performance bounds of FedWM. Through extensive experiments based on real-world datasets, we demonstrate that FedWM achieves significantly more advantageous tradeoffs between client rest and FL model performance compared to existing approaches. To the best of our knowledge, it is the first federated crowdsourcing framework designed to achieve productive laziness.

Index Terms—Federated Crowdsourcing, Workforce management service, Lyapunov optimization, Dynamic scheduling, Data collection

# I. INTRODUCTION

Federated learning (FL) [1], [2], as a privacy-preserving collaborative machine learning paradigm, has attracted significant attention from industry and academia alike in recent years. Currently, most researches on federated learning assume that the training data owned by FL clients are static. This is inconsistent with many practical scenarios (e.g., healthcare) where local data are continuously updated. To support dynamic local data in FL training, the federated crowdsourcing paradigm has emerged [3]. Under federated crowdsourcing, FL clients can collect and label new local data when necessary. Then, the local training and global model aggregation steps of federated learning typically follow.

Recently, studies exploring service provision under the federated crowdsourcing paradigm are emerging [4]. In [3], the potential benefits of federated crowdsourcing (e.g., increased scalability, reduced costs) have been reviewed and highlighted. Nevertheless, as this field is relatively new, there are still a number of research challenges remaining open. One of them concerns workforce management in federated crowdsourcing. To motivate FL clients to build a high-quality global model in an efficient manner, [5] proposed an incentive mechanism that encourages them (who are simultaneously playing the role of “crowd workers”) to constantly collect fresh data in order to train accurate local models which, in turn, boost global model performance. It models the incentive-based interaction between the crowdsourcing platform and participating workers as a Stackelberg game in which each side maximizes its own profit, and computes the optimal solutions for both sides by deriving the Nash Equilibrium of the game. Instead of collecting fresh data, [6] studied federated crowdsourcing with crowdsourced data labels. The local data of each participating FL client are progressively labelled manually by the client over multiple training rounds. Incentive mechanisms have been designed to motivate strategic FL clients to devote truthful efforts as desired by the FL server into data labelling and local model computation, as well as reporting the true local models to the FL server based on the derived performance bound.

Existing federated crowdsourcing workforce management decision support approaches mainly focus on maximizing the FL clients’ (a.k.a. crowd workers’) effort output in order to improve system efficiency and/or FL model performance. However, they overlook the fact that those who need to carry out federated crowdsourcing activities are human beings who need to balance between work and rest in the long run. The longterm success of the system depends on clients accomplishing tasks productively and resting well. As people generally experience periods of high and low productivity throughout different times in a day, it is important to opportunistically schedule work and rest to leverage such changes. In [7], the author proposed a distributed Computational Productive Laziness (CPL) approach to achieve this goal for crowd workers. It leverages the fact that workers’ mood can reflect their productivity, and utilizes only local information concerning a worker’s capability and situational factors to incorporate opportunistic resting. In this way, it operationalizes the concept of productive laziness [8], which posits that workers can accomplish their tasks productively while staying well rested if properly scheduled, in the field of crowdsourcing. However, CPL cannot be applied in the federated crowdsourcing setting as it uses the work backlog to describe the urgency of work, whereas in federated crowdsourcing, the urgency of the tasks is not described in this way.

To bridge this important gap in the literature, we propose the Federated Workforce Management (FedWM) approach with the aim to achieve productive laziness for FL clients. Based on the urgency for collecting and labelling new local data (i.e., the rate of change in client contribution) as well as FL clients’ self-reported mood, it computes the work-rest schedule for each client. Our main contributions are as follows:

1) A dynamic scheduling method based on Lyapunov optimization is devised to guide clients to dynamically determine the optimal effort output for collecting and labelling local data in a given time period.   
2) We provide rigorous and complete theoretical analysis of the performance boundary of FedWM.   
3) To the best of our knowledge, FedWM is the first federated crowdsourcing workforce management decision support approach that balances performance considerations with FL clients’ need to rest in order to achieve productive laziness.

Through extensive experiments based on real-world datasets, we demonstrate that FedWM achieves significantly more advantageous trade-offs between client rest and FL model performance compared to existing approaches.

# II. RELATED WORK

Our work is interdisciplinary in nature. It is closely related to the fields of federated crowdsourcing and AI-powered workforce management. In this section, we provide a literature review on relevant works from these two fields.

Federated crowdsourcing has distinct advantages over federated learning since clients can collect and label new data as needed, thereby supporting the training of FL models that reflect the latest data distributions. Recently, researchers have carried out preliminary explorations on this emerging FL paradigm. Wang et al. 2020 [3] is the first work to summary the benefits and challenges of federated crowdsourcing. In [5], an incentive mechanism was proposed to encourage FL clients to continuously spend effort to collect fresh data in order to train more accurate local models and boosts the global FL model performance. In [6], a truthful incentive mechanism was proposed which motivates strategic clients to spend effort as desired by the FL server on data labeling and local model computation, and also report local models to the server in a truthful manner. Although the data collection labelling tasks are primarily performed by human operators manually, none of the existing federated crowdsourcing approaches takes their need for work-rest balance into consideration.

There has been a growing body of research on workforce management, which aims to optimize the recruitment, allocation and motivation of workers to improve the quality and efficiency of crowdsourcing. In [9]–[17], tasks are dynamically allocated to workers based on their skills, experience and availability. In [18]–[30], various incentive mechanisms (e.g., gamification, financial rewards, reputation) have been proposed to encourage workers to spend more effort and stay committed to their tasks. However, these works did not consider workers’ need for work-rest balance. Recently, [7], [31] started to explore opportunistic work-rest scheduling. In [31], changes in workers’ mood are leveraged to reflect variations in their productivity to facilitate dynamic work-rest scheduling. However, it did not account for the urgency of the tasks. To overcome this drawback, [7] jointly considers workers’ mood, workload and elapse time of the tasks in their backlogs to plan personalized work-rest schedules. Nevertheless, it is not suitable for federated crowdsourcing directly as the FL server does not know any information about the clients other than the local model updates. The proposed FedWM approach addresses these limitations.

# III. PROBLEM AND DESIGN OVERVIEW

We consider a typical federated crowdsourcing framework consisting of an FL server and N FL clients.

• A client is associated with a personal profile. (1) Each client i has maximum productivity $\mu _ { i } ^ { \mathrm { m a x } }$ which indicates the maximum amount of new data i can collect and label over any given round t. (2) Each client has mood $m _ { i } ( t ) \ \in \ [ 0 , 1 ]$ during t. $m _ { i } ( t ) = 1$ denotes the most positive mood, whereas $m _ { i } ( t ) ~ = ~ 0$ denotes the most negative mood. The mood may affect client productivity during t, which is computed as $m _ { i } ( t ) \mu _ { i } ^ { \mathrm { m a x } }$ following [7]. Here, in each round of federated crowdsourcing, each client labels the newly collected data themselves. We assume that the clients collect uniformly distributed highquality data from external data sources, and the labels provided by the clients are correct. The mood of the clients in each round only affects the efficiency of their data collection and labeling.

• The server knows the maximum productivity $\mu _ { i } ^ { \mathrm { m a x } }$ of each client i. This can be achieved through statistical estimation over past interactions with analytics tools such as Turkalytics [32].

A typical federated crowdsourcing framework incorporated with the proposed FedWM approach is shown in Figure 1. FedWM operates in the following steps during each round t.

(1): Each client uploads the locally trained model parameters to the FL server.   
(2): Once the client model updates are received, the server aggregates all of them to obtain the global FL model following an aggregation approach such as FedAvg [33], [34].   
(3): The server then sends the updated global model to all clients.

![](images/61cfa00b10051859c3844f99a52e8d00f8c5760f3ec51086490235c48361f049.jpg)



Fig. 1: An overview of FedWM in federated crowdsourcing.

(4): The server sends the local models and updated global model to the Contribution Assessment module to assess the contribution made by each client.   
(5): The Contribution Assessment module uses an efficient approximate algorithm (e.g., GTG-Shapley [35]) to evaluate the contribution $c _ { i } ( t )$ made by each client in round t. It also computes the rate of change in contribution $b _ { i } ( t )$ by comparing $c _ { i } ( t )$ with $c _ { i } ( t - 1 )$ . Then, it sends $b _ { i } ( t )$ for all i and global model to FedWM.   
(6): After receiving $b _ { i } ( t )$ , FedWM updates the virtual queue parameters $Q _ { i } ( t )$ for each client (to be explained in more details in the next section). Then, it sends requests to all clients to report their updated mood information.   
(7): Each client sends his/her current mood index $m _ { i } ( t + 1 )$ ) to the FedWM module on the FL server at the beginning of round $( t + 1 )$ , which then calculates the work-rest index $\Phi _ { i } ( t )$ . This is further converted into a decision metric $x _ { i } ( t { + } 1 )$ and sent to each client i to guide his/her decision on working or resting during round $( t + 1 )$ .

We aim to design such an opportunisitic personalized workrest scheduling service to enable federated crowdsourcing systems to achieve superlinear collective productivity.

# IV. THE PROPOSED FedWM APPROACH

To achieve the design goal, we first introduce a virtual queue $Q _ { i } ( t )$ for each local client i. The queuing dynamics of client $i \ ' s$ virtual queue can be expressed as:

$$
Q _ {i} (t + 1) = \max \left[ 0, Q _ {i} (t) + a _ {i} (t) - x _ {i} (t) \right]. \tag {1}
$$

It reflects the level of urgency to collect and label new data for client i over a given round t. Here, $x _ { i } ( t ) \in \{ 0 , 1 \}$ indicates whether client i shall collect and label new data in round t $( 1 = \mathrm { y e s , ~ 0 = n o ) . ~ } a _ { i } ( t ) \in [ 0 , 1 ]$ is defined as follows:

$$
a _ {i} (t) = \frac {b _ {i} (t)}{\sum_ {i = 1} ^ {N} b _ {i} (t) I _ {[ b _ {i} (t) <   0 \& x _ {i} (t) = 0 ]}} I _ {[ b _ {i} (t) <   0 \& x _ {i} (t) = 0 ]} \tag {2}
$$

Here, $b _ { i } ^ { ( t ) }$ is the rate of change in contribution for client i produced by the Contribution Assessment module:

$$
b _ {i} (t) = \frac {c _ {i} (t) - c _ {i} (t - 1)}{| c _ {i} (t - 1) |}. \tag {3}
$$

where $c _ { i } ( t )$ is the contribution made by i to the performance of the global FL model determined by the Contribution Assessment module. $I _ { [ \mathrm { c o n d i t i o n } ] }$ is an indicator function. $I = 1$ if condition is satisfied; otherwise, $I = 0 .$ . The dynamics of $Q _ { i } ( t )$ are as follows:

1) $Q ( 0 ) = 0$ , which means it is initially empty.   
2) If client i’s contribution $c _ { i } ( t )$ decreases and client i does not collect new labelled data in round t, $Q _ { i } ( t )$ increases. This is to ensure that cumulative urgency to collect and label new data increases if the client continues to train models on the existing dataset as the relative contribution declines.   
3) If client i collects new labelled data in the round t, $Q _ { i } ( t )$ decreases by 1. This is reasonable because when client i collects new data in round t, the available local dataset is expanded. The model trained on the enlarged local dataset is likely to improve the relative contribution made by the client to the FL model. In this way, the cumulative urgency for client i to collect new data in round (t + 1) decreases.

According to Eq. (1), we can obtain:

$$
Q _ {i} (t + 1) \geq Q _ {i} (t) + a _ {i} (t) - x _ {i} (t). \tag {4}
$$

Re-organizing the terms yields:

$$
Q _ {i} (t + 1) - Q _ {i} (t) \geq a _ {i} (t) - x _ {i} (t). \tag {5}
$$

By summing both sides of the above inequality over $t \in$ $\{ 0 , \ldots , T - 1 \}$ , we have:

$$
\sum_ {t = 0} ^ {T - 1} [ Q _ {i} (t + 1) - Q _ {i} (t) ] \geq \sum_ {t = 0} ^ {T - 1} [ a _ {i} (t) - x _ {i} (t) ]. \tag {6}
$$

Thus, we can obtain:

$$
Q _ {i} (T) - Q _ {i} (0) \geq \sum_ {t = 0} ^ {T - 1} [ a _ {i} (t) - x _ {i} (t) ]. \tag {7}
$$

Since $Q _ { i } ( 0 ) = 0$ , the above inequality can be re-expressed as:

$$
\frac {Q _ {i} (T)}{T} \geq \frac {1}{T} \sum_ {t = 0} ^ {T - 1} a _ {i} (t) - \frac {1}{T} \sum_ {t = 0} ^ {T - 1} x _ {i} (t). \tag {8}
$$

In order to prevent $Q _ { i } ( T )$ from growing indefinitely, inspired by [36], the virtual queues of all clients must satisfy the following condition during federated crowdsourcing:

$$
\lim _ {T \to \infty} E [ Q _ {i} (T) ] / T = 0. \tag {9}
$$

Thus, based on Eq. (8) and Eq. (9), the queuing stability requirement can be expressed as:

$$
\frac {1}{T} \sum_ {t = 0} ^ {T - 1} x _ {i} (t) \geq \frac {1}{T} \sum_ {t = 0} ^ {T - 1} a _ {i} (t). \tag {10}
$$

To satisfy $\operatorname { E q . }$ (10), we leverage Lyapunov optimization to bound each increase of $Q _ { i } ( t )$ . We first define a quadratic Lyapunov function as:

$$
L (t) = \frac {1}{2} \sum_ {i = 1} ^ {N} Q _ {i} ^ {2} (t) \geq 0. \tag {11}
$$

L(t) can measure the overall distribution of clients’ urgency to collect new labelled data. A larger $L ( t )$ reflects either that only a few clients frequently collect new labelled data and/or the urgency levels have been high for a number of rounds. Both scenarios are undesirable and shall be avoided as much as possible.

Next, we formulate the Lyapunov drift between two consecutive rounds as:

$$
\Delta (t) = L (t + 1) - L (t). \tag {12}
$$

The Lyapunov drift $\Delta ( t )$ is a measure of fluctuation of the overall urgency level in the system. By minimizing $\Delta ( t )$ , we aim to limit the growth of the all $Q _ { i } ( t )$ by dynamically advising clients to collect new labelled data so as not to over emphasis on resting to the point of adversely affecting FL model quality. Combining Eq. (11) and Eq. (12), we have:

$$
\begin{array}{l} \Delta (t) = \frac {1}{2} \sum_ {i = 1} ^ {N} \left(Q _ {i} ^ {2} (t + 1) - Q _ {i} ^ {2} (t)\right) \\ = \frac {1}{2} \sum_ {i = 1} ^ {N} \left(\max \left[ 0, Q _ {i} (t) + a _ {i} (t) - x _ {i} (t) \right] ^ {2} - Q _ {i} ^ {2} (t)\right) \\ \leq \frac {1}{2} \sum_ {i = 1} ^ {N} \left[ \left(Q _ {i} (t) + a _ {i} (t) - x _ {i} (t)\right) ^ {2} - Q _ {i} ^ {2} (t) \right] \\ \leq \sum_ {i = 1} ^ {N} \left(Q _ {i} (t) \left[ a _ {i} (t) - x _ {i} (t) \right] + \theta\right). \tag {13} \\ \end{array}
$$

For simplicity of expression, we set $\begin{array} { r } { \theta = \frac 1 2 ( a _ { i } ^ { \operatorname* { m a x } } ) ^ { 2 } + \frac 1 2 ( x _ { i } ^ { \operatorname* { m a x } } ) ^ { 2 } } \end{array}$ , where $a _ { i } ^ { \mathrm { m a x } } = 1$ and $x _ { i } ^ { \mathrm { m a x } } = 1$ are the respective upper bounds for all $a _ { i } ( t )$ and $x _ { i } ( t )$ .

Another goal of the proposed FedWM approach is to help FL clients rest more. To achieve this goal, we design the approach to suggest them to collect new labelled data during their respective periods of high productivity, and suggest them to increase their rest time during their respective periods of low productivity, while maintaining model quality.

We define the utility function $U ( t + 1 )$ to reflect the overall working time of all clients in round (t + 1) as:

$$
U (t + 1) = \sum_ {i = 1} ^ {N} \frac {\Gamma}{m _ {i} (t) \mu_ {i} ^ {\max}} x _ {i} (t + 1). \tag {14}
$$

Here, Γ is the amount of labelled data a client can collect in each round which is same and fixed for all clients. The coefficient $\begin{array} { r } { \phi _ { i } ( t + 1 ) = \frac { \Gamma } { m _ { i } ( t ) \mu _ { i } ^ { \mathrm { m a x } } } } \end{array}$ reflects the time spent by client i on collecting data round (t + 1). Intuitively, $U ( t +$ 1) calculates the total time spent by all clients in collecting new labelled data in round (t + 1). We aim to minimize the {working time + drift} objective function:

$$
\sum_ {t = 0} ^ {T - 1} [ \sigma U (t + 1) + \Delta (t) ]. \tag {15}
$$

The parameter σ is a tuning parameter, which can be set by the FL system administrator to indicate to the algorithm his/her preference between the two components of the objective. Substituting Eq. (13) and Eq. (14) into Eq. (15) yields:

$$
\begin{array}{l} \frac {1}{T} \sum_ {t = 0} ^ {T - 1} [ \sigma U (t + 1) + \Delta (t) ] \\ \leq \frac {1}{T} \sum_ {t = 0} ^ {T - 1} \sum_ {i = 1} ^ {N} [ \sigma \phi_ {i} (t + 1) x _ {i} (t + 1) \tag {16} \\ \left. + Q _ {i} (t) a _ {i} (t) - Q _ {i} (t) x _ {i} (t) + \theta \right]. \\ \end{array}
$$

As FedWM aims to provide personalized work-rest schedules to FL clients in round (t + 1), we only need to focus on the terms containing the control variable $x _ { i } ( t + 1 )$ ). Thus, the optimization problem is re-expressed as:

$$
\min \quad \frac {1}{T} \sum_ {t = 0} ^ {T - 1} \sum_ {i = 1} ^ {N} x _ {i} (t + 1) [ \sigma \phi_ {i} (t + 1) - Q _ {i} (t) ]. \tag {17}
$$

$$
s. t. \quad x _ {i} (t + 1) \in \{0, 1 \}. \tag {18}
$$

For simplicity of expression, we define $\delta _ { i } ( t { + } 1 ) = \sigma \phi _ { i } ( t { + } 1 ) -$ $Q _ { i } ( t )$ as the Work-Rest Index (WRI), which can be used to support workforce management module to efficiently compute the personalized schedule for client i in round $( t + 1 )$ (i.e., whether client i needs to collect new labelled data in round $( t + 1 ) )$ .

# Algorithm 1: FedWM

Input: Tuning parameter σ, maximum productive $\mu _ { i } ^ { \mathrm { m a x } }$ for each client i, mood $m _ { i } ( t + 1 )$ in round $t + 1 ,$ , and virtual queue $Q _ { i } ( t )$ for each client i in round t.

Output: Work-rest recommendation $x _ { i } ( t + 1 )$ for each client i

1 for i = 1 to N do
2 Calculate the Work-Rest Index: $\delta_{i}(t+1) = \sigma \phi_{i}(t+1) - Q_{i}(t);$ 3 if $\delta_{i}(t+1) < 0$ then
4 | Set $x_{i}(t+1) = 1;$ 5 else
6 | Set $x_{i}(t+1) = 0;$ 7 end
8 end
9 return $\{x_{i}(t+1) | \forall i\}$ ;

Algorithm 1 shows how FedWM calculates the WRI based on the virtual queue $Q _ { i } ( t )$ and the client $i \mathbf { \ ' } _ { \mathbf { S } }$ mood, and then returns the decision $x _ { i } ( t + 1 )$ for each client i. If $\delta _ { i } ( t + 1 ) < 0$ , client i is advised to collect new labelled data in round $( t + 1 )$ to expand the local dataset. If $\delta _ { i } ( t + 1 ) \geq 0$ , client i is advised to rest in round (t + 1) and continue to train the local model using the existing dataset. The time complexity of Algorithm 1 is $O ( N )$ , which gives it high computational efficiency and scalability.

# V. ANALYSIS

In this section, we analyze the performance bounds of FedWM. Let $U ^ { * }$ be the optimal value of the total working time of the clients in a training round. The time that the clients spend on data collection shall not exceed $U ^ { * }$ too much. By adjusting the parameter $\sigma ,$ we can make the clients’ working time close to $U ^ { * }$ . Nevertheless, we also need to balance it with the length of the virtual queue $Q _ { i } ( t )$ . Assume that there exist constants $\sigma , \epsilon > 0 , \zeta \geq 0 .$ , and the target value $U ^ { * }$ such that the following condition holds for all t and all $Q _ { i } ( t )$ :

$$
\sigma U (t + 1) + \Delta (t) \leq \sigma U ^ {*} - \epsilon \sum_ {i = 1} ^ {N} Q _ {i} (t) + \zeta . \tag {19}
$$

Theorem V.1. Under FedWM, the upper bound on the average expected working time for all clients satisfies:

$$
\frac {1}{T} \sum_ {t = 0} ^ {T - 1} \sum_ {i = 1} ^ {N} \frac {\Gamma}{m _ {i} (t) \mu_ {i} ^ {\max}} x _ {i} (t + 1) \leq U ^ {*} + \frac {\zeta}{\sigma}. \tag {20}
$$

Proof. By substituting Eq. (12), Eq. (14) into Eq. (19), we have:

$$
\begin{array}{l} \sigma \sum_ {i = 1} ^ {N} \frac {\Gamma}{m _ {i} (t) \mu_ {i} ^ {\max}} x _ {i} (t + 1) + L (t + 1) - L (t) \tag {21} \\ \leq \sigma U ^ {*} - \epsilon \sum_ {i = 1} ^ {N} Q _ {i} (t) + \zeta . \\ \end{array}
$$

Summing both sides of the above inequality over the T rounds, we have:

$$
\begin{array}{l} \sigma \sum_ {t = 0} ^ {T - 1} \sum_ {i = 1} ^ {N} \frac {\Gamma}{m _ {i} (t) \mu_ {i} ^ {\max}} x _ {i} (t + 1) + L (T) - L (0) \tag {22} \\ \leq \sigma T U ^ {*} - \epsilon \sum_ {t = 0} ^ {T - 1} \sum_ {i = 1} ^ {N} Q _ {i} (t) + T \zeta . \\ \end{array}
$$

Since $Q _ { i } ( t ) \geq 0 , L ( \cdot ) \geq 0$ and $L ( 0 ) = 0$ for all i and t, we then have:

$$
\begin{array}{l} \sigma \sum_ {t = 0} ^ {T - 1} \sum_ {i = 1} ^ {N} \frac {\Gamma}{m _ {i} (t) \mu_ {i} ^ {\max}} x _ {i} (t + 1) \tag {23} \\ \leq \sigma T U ^ {*} - \epsilon \sum_ {t = 0} ^ {T - 1} \sum_ {i = 1} ^ {N} Q _ {i} (t) - L (T) + T \zeta . \\ \end{array}
$$

Dividing both sides of the above inequality by $T \sigma > 0$ yields:

$$
\begin{array}{l} \frac {1}{T} \sum_ {t = 0} ^ {T - 1} \sum_ {i = 1} ^ {N} \frac {\Gamma}{m _ {i} (t) \mu_ {i} ^ {\max}} x _ {i} (t + 1) \\ \leq U ^ {*} - \frac {\epsilon}{T \sigma} \sum_ {t = 0} ^ {T - 1} \sum_ {i = 1} ^ {N} Q _ {i} (t) - \frac {1}{T \sigma} L (T) + \frac {\zeta}{\sigma} \tag {24} \\ \leq U ^ {*} + \frac {\zeta}{\sigma}. \\ \end{array}
$$

Therefore, we have proven that, under FedWM, the upper bound of the expected average client working time exceeds the optimal value $U ^ { * }$ by at most $O ( { \textstyle { \frac { 1 } { \sigma } } } )$ . □

Theorem V.2. Under FedWM, the upper bound on the average virtual queue length for all clients satisfies:

$$
\frac {1}{T} \sum_ {t = 0} ^ {T - 1} \sum_ {i = 1} ^ {N} Q _ {i} (t) \leq \frac {\sigma}{\varepsilon} U ^ {*} + \frac {\zeta}{\varepsilon}. \tag {25}
$$

Proof. Since $Q _ { i } ( t ) \geq 0 , L ( \cdot ) \geq 0$ and $L ( 0 ) = 0$ for all i and t. By re-arranging $\operatorname { E q . } \ ( 1 )$ , we have:

$$
\begin{array}{l} \frac {1}{T} \sum_ {t = 0} ^ {T - 1} \sum_ {i = 1} ^ {N} Q _ {i} (t) \leq \frac {\sigma}{\varepsilon} U ^ {*} - \frac {\sigma}{\varepsilon T} \sum_ {t = 0} ^ {T - 1} \sum_ {i = 1} ^ {N} \frac {\Gamma}{m _ {i} (t) \mu_ {i} ^ {\max}} x _ {i} (t + 1) \\ + \frac {\zeta}{\varepsilon} - \frac {L (T)}{\varepsilon T} \leq \frac {\sigma}{\varepsilon} U ^ {*} + \frac {\zeta}{\varepsilon}. \tag {26} \\ \end{array}
$$

Thus, we have shown that the average virtual queue length for all clients under FedWM is upper bounded by O(σ). □

According to Theorem.V.1, larger values of σ will bring the average expected client working time closer to the optimal value. However, according to Theorem.V.2, larger values of σ will result in longer virtual queues for all clients. This means that the frequency at which clients update their local datasets is low, which in turn, might negatively impact FL model performance. This way, FedWM enables system administrators to set their desired trade-offs between the two objectives.

# VI. EXPERIMENTAL EVALUATION

In this section, we conduct experiments based on real-world datasets to evaluate the proposed FedWM approach against state-of-the-art existing methods.

# A. Experimental Settings

We evaluate the performance of the comparison approaches on two image classification datasets: 1) MNIST [37]: a collection of 60,000 hand-written digits (0-9) as training examples and 10,000 additional examples for testing, and 2) CIFAR-10 [38]: a collection of 60,000 32 × 32 color images of 10 different classes, with 6,000 images per class. A total of 10 FL clients are created, each with an initial local dataset size of 10,000 images. In order to evaluate the effectiveness of the methods in realistic settings, two types of client data splits are considered.

1) IID local datasets: Before training begins, images are randomly sampled from the entire training set and allocated to each client. During the training process, when new labelled data need to be collected, each client uniformly and randomly selects 1,000 new sample data from the entire training set to augment its local dataset.   
2) Non-IID local datasets: We adjust the proportions of samples for each class in every client’s dataset to simulate data heterogeneity. In each client’s dataset, 40% of the data belong to a specific class. The remaining local training samples are uniformly and randomly selected from the corresponding classes in the entire training set. When a client needs to collect data, the newly collected data follow the same class distribution. During each round of data collection, a client’s local dataset is incremented by 1,000 new samples.

Base Model and Hyperparameters: In the PyTorch FL environment, we use two different convolutional neural networks to perform classification tasks on the two datasets. The learning rates on MNIST and CIFAR-10 are set to be $\alpha = 0 . 0 1$ and 0.005, respectively. The preference tuning parameters are set as $\sigma = 0 . 4 , \theta _ { 1 } = 0 . 5 , \theta _ { 2 } = 0 . 6 , k _ { 1 } = 4$ and $k _ { 2 } = 1$ . The maximum productivity of a client $\mu _ { i } ^ { m a x }$ and the mood index $m _ { i } ( t )$ follow a uniform distribution UNI(0, 1) and are randomly generated during the experiments.

# B. Comparison Approaches

We compared FedWM with the following approaches:

1) Maximum Work (MW): Under this method, a client collects new labelled data and updates his/her local dataset in every training round until FL model convergence. The clients work maximally without rest.   
2) Random Work (RW): Under this method, a client spends effort to collect new labelled data in each training round with a probability of $p = 0 . 5$ and rest with a probability of $( 1 - p )$ , until FL model convergence.   
3) Maximum Potential Payoff (MP): This method is based on the truthful incentive mechanism [6] to achieve maximum client payoff in federated crowdsourcing. It considers the loss of the local model trained by each client on the test set. Let $f ( \theta _ { i } ( t ) )$ be the loss of the local model $\theta _ { i } ( t )$ trained by the client i after expanding his/her dataset in round t. The potential payoff $r _ { i } ( t + 1 )$ for client i to expand his/her dataset in round $t + 1$ is $\begin{array} { r } { r _ { i } ( t + 1 ) = k _ { 1 } f ( \bar { \theta } _ { i } ( t ) ) - k _ { 2 } \frac { \Gamma } { m _ { i } ( t ) \mu _ { i } ^ { \mathrm { m a x } } } } \end{array}$ 2 Γmi(t)µmaxi . Here, k1f (θi(t)) $k _ { 1 } f ( \theta _ { i } ( t ) )$ reflects the potential reward client i can receive by collecting new labelled data. k2 Γmi(t)µmax $k _ { 2 } \frac { \Gamma } { m _ { i } ( t ) \mu _ { i } ^ { \operatorname* { m a x } } }$ reflects the time client i needs to spend on data collection. $k _ { 1 }$ and $k _ { 2 }$ are tunable parameters of the system. Clients collect new data if their potential payoffs are positive; otherwise, they rest.

![](images/6b298277bbf7791378a490f88dabbc6fd151ff371badd2f03d99afcc36ccf645.jpg)



(a)

![](images/5f0ed1ecc4857f6e1fe638817b990f19100a95ceb297a6af2bbd78e74d712000.jpg)



(b)   
Fig. 2: Test accuracy at convergence under IID data split.

# C. Evaluation Metrics

1) Test Accuracy: When the testing loss of the global FL model stabilizes after multiple rounds of training, the FL server evaluates the test accuracy on its test set to measure model performance. The higher the test accuracy, the better the model performance.   
2) Average Working Time: The total time spent by each client on data collection until the global FL model converges, averaged across all clients. A lower value indicates more time for clients to rest.

# D. Results and Discussion

We first evaluate FedWM with all the comparison baselines in terms of test accuracy and average working time. Then, we compare the trade-off between test accuracy and average working time by various approaches.

![](images/23056ea9020c77629fa4d8fd7260aec40f7cd6521f8d7cfb0d76534b7ec02e62.jpg)



(a)

![](images/6866c348e2eb21983069d46c912e8b0c171c5097849a11d7dbdf5da690145989.jpg)



(b)

Fig. 3: Test accuracy at convergence under Non-IID data split.   
![](images/d79920b02673de5ebc65ba8ecc753515d2f2b690631a00ce8abb805ea456c7ac.jpg)



(a) IID

![](images/8c078873e1d779821b686eed67eb0488f3a910285c011740b5c3e346fa064ab5.jpg)



(b) Non-IID

Fig. 4: Average working time per client until convergence.   
![](images/ad6ecff089f012e63f06650b412d213200c0ab9eee17f6ea1bceb6f4be695d18.jpg)



(a) MNIST IID

![](images/d14c717a6b04a5e0d2594df8aa80a9756c0fc3574a2a1431d4de316f8bb81875.jpg)



(b) CIFAR-10 IID

![](images/22d66277cb9b5858df666162c7a95269453a8698c1753e8a2dd32eb7b4bcefdf.jpg)



(c) MNIST non-IID

![](images/6c32c4d3f0b957daff758fdc0903e044317b22a10142bd3f03480a2d148d944b.jpg)



(d) CFAR-10 non-IID   
Fig. 5: Trade-off between Test accuracy and Working Time.

1) Test Accuracy: From Table I, Table II, Figure 2 and Figure 3, it can be observed that FedWM achieves test accuracy values that are close to MW which represents the upper bound of the FL model performance achievable by the clients without taking any rest. The test accuracy performance of FedWM is significantly better than RW and MP under both the IID and Non-IID settings. FedWM outperforms MP as it only utilizes the local model test loss after local training as the potential gain to determine whether data collection is necessary in the next round. It does not consider that clients will receive the global aggregated model after each round of training. As the number of training rounds increases, the

TABLE I: Comparison results for test accuracy and working time on MNIST and CIFAR-10 under IID distribution. 

<table><tr><td rowspan="2">Method</td><td colspan="2">MNIST</td><td colspan="2">CIFAR-10</td></tr><tr><td>Acc</td><td>Working Time</td><td>Acc</td><td>Working Time</td></tr><tr><td>MW</td><td>97.08</td><td>100.65</td><td>76.25</td><td>152.59</td></tr><tr><td>RW</td><td>95.26</td><td>61.51</td><td>73.56</td><td>87.49</td></tr><tr><td>MP</td><td>95.68</td><td>39.29</td><td>73.68</td><td>66.13</td></tr><tr><td>FedWM</td><td>96.21</td><td>38.8</td><td>75.33</td><td>58.24</td></tr></table>

TABLE II: Comparison results for test accuracy and working time on MNIST and CIFAR-10 under non-IID distribution. 

<table><tr><td rowspan="2">Method</td><td colspan="2">MNIST</td><td colspan="2">CIFAR-10</td></tr><tr><td>Acc</td><td>Working Time</td><td>Acc</td><td>Working Time</td></tr><tr><td>MW</td><td>96.08</td><td>106.58</td><td>75.78</td><td>171.76</td></tr><tr><td>RW</td><td>94.26</td><td>63.61</td><td>73.44</td><td>104.85</td></tr><tr><td>MP</td><td>94.68</td><td>49.08</td><td>73.68</td><td>79.3</td></tr><tr><td>FedWM</td><td>95.25</td><td>44.74</td><td>74.32</td><td>68.17</td></tr></table>

local test loss of the model will continue to decrease. This increases the mood index required for the client to obtain positive potential payoff, leading to a decrease in the frequency of data collection by some clients in the later stages of training. This negatively affects the convergence rate of the global FL model. In contrast, FedWM utilizes the changes in relative contribution to measure the urgency for a client to perform data collection, which effectively avoids this problem and boosts the convergence rate of the global FL model.

2) Average Working Time: From Table I, Table II and Figure 4, it can be observed that FedWM achieves significantly lower average working time than other approaches under both data splits, as it opportunistically balances the need for more data by the system with the need for rest by the FL clients to optimize the scheduling of work and rest. In contrast, MW does not allocate any rest time for clients during the training process. RW randomly selects clients to work without considering whether rest is suitable at the given point in time. e.g., when client i has a low maximum productivity $\mu _ { i } ^ { \mathrm { { m a x } } }$ or has very negative mood $m _ { i } ( t )$ .

3) Performance-Rest Trade-off: In Figure 5, we plot the trade-off result between test accuracy and average working time achieved by all approaches. The closer to the lower right corner, the better the trade-off. It can be observed that FedWM consistently achieves the best trade-off under all experiment conditions.

# E. Ablation Study

We further conduct the ablation experiment on FedWM to investigate the impact of various design components. By controlling how the mood information and the virtual queue are utilized, we obtain the following variants of FedWM.

1) FedWM with Mood Threshold (FedWM(MT)): Under this version of FedWM, we only consider clients’ mood to determine whether they shall perform data collection in any given round. If client i’s mood satisfies $m _ { i } ( t ) \geq \theta _ { 1 }$ , he/she shall perform data collection; otherwise, he/she rests.

2) FedWM with Queue Threshold (FedWM(QT)): Under this version of FedWM, we only consider the virtual queue values to determine whether clients shall perform data collection. At the end of the t-th round of training, if $Q _ { i } ( t + 1 ) \geq \theta _ { 2 }$ , client i shall perform data collection in round t + 1; otherwise, he/she rests.

TABLE III: Ablation study results on MNIST and CIFAR-10 under IID distribution. 

<table><tr><td rowspan="2">Method</td><td colspan="2">MNIST</td><td colspan="2">CIFAR-10</td></tr><tr><td>Acc</td><td>Working Time</td><td>Acc</td><td>Working Time</td></tr><tr><td>FedWM(MT)</td><td>94.46</td><td>30.48</td><td>71.46</td><td>42.82</td></tr><tr><td>FedWM(QT)</td><td>94.89</td><td>50.21</td><td>72.44</td><td>73.19</td></tr><tr><td>FedWM</td><td>96.21</td><td>38.8</td><td>75.33</td><td>58.24</td></tr></table>

TABLE IV: Ablation study results on MNIST and CIFAR-10 under non-IID distribution. 

<table><tr><td rowspan="2">Method</td><td colspan="2">MNIST</td><td colspan="2">CIFAR-10</td></tr><tr><td>Acc</td><td>Working Time</td><td>Acc</td><td>Working Time</td></tr><tr><td>FedWM(MT)</td><td>93.46</td><td>40.49</td><td>71.46</td><td>62.49</td></tr><tr><td>FedWM(QT)</td><td>93.85</td><td>55.03</td><td>72.43</td><td>91.37</td></tr><tr><td>FedWM</td><td>95.25</td><td>44.74</td><td>74.32</td><td>68.17</td></tr></table>

From Table III and Table IV, it can be observed that FedWM(MT) achieves the lowest average working time. However, without considering the need for new data by the FL system, it consistently achieves the lowest test accuracy. FedWM(QT) achieves slightly higher test accuracy than FedWM(MT), but with significantly longer average working time. In summary, our proposed FedWM achieves the most advantageous trade-off between test accuracy and average working time compared to these variants.

# VII. CONCLUSIONS

In this paper, we proposed the FedWM workforce management approach to help federated crowdsourcing systems dynamically schedule work and rest for clients to achieve time averaged optimal effort output for collecting new labelled data. We provide rigorous and complete theoretical analysis of the performance bounds of FedWM. Extensive experiments show that FedWM achieves the best trade-off between model performance and clients’ rest time. To the best of our knowledge, it is the first federated crowdsourcing workforce management decision support approach that balances performance considerations with FL clients’ need to rest in order to achieve productive laziness.

# ACKNOWLEDGEMENTS

Yu Han, Lan Zhang and Xiang-Yang Li are the corresponding authors. The research is supported, in part, by the National Key R&D Program of China (No. 2021ZD0110400 and 2021YFB2900103); Innovation Program for Quantum Science and Technology (2021ZD0302900); China National Natural Science Foundation (No. 62132018 and No. 61932016); Pioneer and Leading Goose R&D Program of Zhejiang (2023C01029); the Fundamental Research Funds for the Central Universities (WK2150110024); National Research Foundation Singapore and DSO National Laboratories under the AI Singapore Programme (AISG Award No: AISG2- RP-2020- 019); the RIE 2020 Advanced Manufacturing and Engineering (AME) Programmatic Fund (No.A20G8b0102), Singapore; Nanyang Technological University, Nanyang Assistant Professorship (NAP); and the Joint SDU-NTU Centre for Artificial Intelligence Research (C-FAIR).

# REFERENCES

[1] Q. Yang, Y. Liu, T. Chen, and Y. Tong, “Federated machine learning: Concept and applications,” ACM Transactions on Intelligent Systems and Technology, vol. 10, no. 2, pp. 1–19, 2019.   
[2] Q. Yang, Y. Liu, Y. Cheng, Y. Kang, T. Chen, and H. Yu, Federated Learning. Springer, Cham, 2020.   
[3] L. Wang, H. Yu, and X. Han, “Federated crowdsensing: framework and challenges,” arXiv preprint arXiv:2011.03208, 2020.   
[4] Y. Zheng, H. Yu, L. Cui, C. Miao, C. Leung, and Q. Yang, “SmartHS: An ai platform for improving government service provision,” in Proceedings of the 30th AAAI Conference on Innovative Applications of AI (IAAI-18), 2018, pp. 7704–7711.   
[5] X. Kang, G. Yu, J. Wang, W. Guo, C. Domeniconi, and J. Zhang, “Incentive-boosted federated crowdsourcing,” arXiv preprint arXiv:2211.14439, 2022.   
[6] Y. Zhao, X. Gong, and S. Mao, “Truthful incentive mechanism for federated learning with crowdsourced data labeling,” in Proceedings of the 2023 IEEE International Conference on Computer Communications (INFOCOM’23), 2023.   
[7] H. Yu, C. Miao, Y. Zheng, L. Cui, S. Fauvel, and C. Leung, “Ethically aligned opportunistic scheduling for productive laziness,” in Proceedings of the 2019 AAAI/ACM Conference on AI, Ethics, and Society (AIES’19), 2019, pp. 45–51.   
[8] P. Taylor, The Lazy Project Manager. Infinite Ideas Limited, Oxford, UK, 2009.   
[9] W. Mason and D. J. Watts, “Collaborative learning in networks,” Proceedings of the National Academy of Sciences of USA, vol. 109, no. 3, pp. 764–769, 2012.   
[10] H. Yu, C. Miao, B. An, C. Leung, and V. R. Lesser, “A reputation management approach for resource constrained trustee agents,” in Proceedings of the 33rd International Joint Conference on Artificial Intelligence (IJCAI’13), 2013, pp. 418–424.   
[11] H. Yu, C. Miao, Z. Shen, C. Leung, Y. Chen, and Q. Yang, “Efficient task sub-delegation for crowdsourcing,” in Proceedings of the AAAI Conference on Artificial Intelligence (AAAI-15), 2015, pp. 1305–1311.   
[12] H. Yu, C. Miao, C. Leung, Y. Chen, S. Fauvel, V. R. Lesser, and Q. Yang, “Mitigating herding in hierarchical crowdsourcing networks,” Scientific Reports, vol. 6, no. 1, p. 4, 2016.   
[13] H. Yu, C. Miao, Y. Chen, S. Fauvel, X. Li, and V. R. Lesser, “Algorithmic management for improving collective productivity in crowdsourcing,” Scientific Reports, vol. 7, no. 1, p. 12541, 2017.   
[14] Z. Shi, S. Jiang, L. Zhang, Y. Du, and X.-Y. Li, “Crowdsourcing system for numerical tasks based on latent topic aware worker reliability,” in Proceedings of the 2021 IEEE International Conference on Computer Communications (INFOCOM’21), 2021, pp. 1–10.   
[15] C. Cen, S.-F. Cheng, H. C. Lau, and A. Misra, “Towards cityscale mobile crowdsourcing: Task recommendations under trajectory uncertainties,” in Proceedings of the 24th International Conference on Artificial Intelligence (IJCAI’15), 2015, pp. 1113–1119.   
[16] A. Zenonos, S. Stein, and N. Jennings, “An algorithm to coordinate measurements using stochastic human mobility patterns in large-scale participatory sensing settings,” in Proceedings of the 30th AAAI Conference on Artificial Intelligence (AAAI-16), 2016, pp. 3936–3942.   
[17] D. Zhai, Y. Sun, A. Liu, Z. Li, G. Liu, L. Zhao, and K. Zheng, “Towards secure and truthful task assignment in spatial crowdsourcing,” World Wide Web, vol. 22, pp. 2017–2040, 2019.   
[18] H. Yu, Z. Shen, C. Miao, and A.-H. Tan, “A simple curious agent to help people be curious,” in Proceedings of the 10th International Conference on Autonomous Agents and Multi-Agent Systems (AAMAS’11), 2011, pp. 1159–1160.   
[19] A. Mao, E. Kamar, Y. Chen, E. Horvitz, M. Schwamb, C. Lintott, and A. Smith, “Volunteering versus work for pay: Incentives and tradeoffs in crowdsourcing,” in Proceedings of the 2013 AAAI Conference on Human Computation and Crowdsourcing (HCOMP’13), vol. 1, 2013, pp. 94–102.

[20] H. Yu, Z. Shen, C. Leung, C. Miao, and V. R. Lesser, “A survey of multi-agent trust management systems,” IEEE Access, vol. 1, pp. 35– 50, 2013.   
[21] C. Miao, H. Yu, Z. Shen, and C. Leung, “Balancing quality and budget considerations in mobile crowdsourcing,” Decision Support Systems, vol. 90, pp. 56–64, 2016.   
[22] Z. Shi, L. Zhang, Z. Yao, L. Lyu, C. Chen, L. Wang, J. Wang, and X.-Y. Li, “Fedfaim: A model performance-based fair incentive mechanism for federated learning,” IEEE Transactions on Big Data, 2022.   
[23] T. Song, Y. Tong, and S. Wei, “Profit allocation for federated learning,” in Proceedings of the 2019 IEEE International Conference on Big Data (BigData’19), 2019, pp. 2577–2586.   
[24] Y. Sarikaya and O. Ercetin, “Motivating workers in federated learning: A stackelberg game perspective,” IEEE Networking Letters, vol. 2, no. 1, pp. 23–27, 2019.   
[25] D. Ye, R. Yu, M. Pan, and Z. Han, “Federated learning in vehicular edge computing: A selective model aggregation approach,” IEEE Access, vol. 8, pp. 23 920–23 935, 2020.   
[26] J. Kang, Z. Xiong, D. Niyato, S. Xie, and J. Zhang, “Incentive mechanism for reliable federated learning: A joint optimization approach to combining reputation and contract theory,” IEEE Internet of Things Journal, vol. 6, no. 6, pp. 10 700–10 714, 2019.   
[27] Y. Zhan, P. Li, Z. Qu, D. Zeng, and S. Guo, “A learning-based incentive mechanism for federated learning,” IEEE Internet of Things Journal, vol. 7, no. 7, pp. 6360–6368, 2020.   
[28] L. Lyu, X. Xu, Q. Wang, and H. Yu, “Collaborative fairness in federated learning,” in Federated Learning: Privacy and Incentive, Q. Yang, L. Fan, and H. Yu, Eds. Springer, Cham, 2020, pp. 189–204.   
[29] X. Xu, L. Lyu, X. Ma, C. Miao, C. S. Foo, and B. K. H. Low, “Gradient driven rewards to guarantee fairness in collaborative machine learning,” in Proceedings of the 35th Conference on Neural Information Processing Systems (NeurIPS’21), 2021, pp. 16 104–16 117.   
[30] X. Xu and L. Lyu, “Towards building a robust and fair federated learning system,” arXiv preprint arXiv:2011.10464, 2020.   
[31] H. Yu, Z. Shen, S. Fauvel, and L. Cui, “Efficient scheduling in crowdsourcing based on workers’ mood,” in Proceedings of the 2017 IEEE International Conference on Agents (ICA’17), 2017, pp. 121–126.   
[32] P. Heymann and H. Garcia-Molina, “Turkalytics: analytics for human computation,” in Proceedings of the 20th International Conference on World Wide Web (WWW’11), 2011, pp. 477–486.   
[33] S. Wang, T. Tuor, T. Salonidis, K. K. Leung, C. Makaya, T. He, and K. Chan, “When edge meets learning: Adaptive control for resourceconstrained distributed machine learning,” in Proceedings of the 2018 IEEE International Conference on Computer Communications (INFO-COM’18), 2018, pp. 63–71.   
[34] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-efficient learning of deep networks from decentralized data,” in Proceedings of the 20th International Conference on Artificial Intelligence and Statistics (AISTATS’17), 2017, pp. 1273–1282.   
[35] Z. Liu, Y. Chen, H. Yu, Y. Liu, and L. Cui, “GTG-Shapley: Efficient and accurate participant contribution evaluation in federated learning,” ACM Transactions on Intelligent Systems and Technology, vol. 13, no. 4, pp. 1–21, 2022.   
[36] M. J. Neely, Stochastic network optimization with application to communication and queueing systems. Morgan & Claypool Publishers, 2010.   
[37] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, “Gradient-based learning applied to document recognition,” Proceedings of the IEEE, vol. 86, no. 11, pp. 2278–2324, 1998.   
[38] A. Krizhevsky and G. Hinton, “Learning multiple layers of features from tiny images,” Master’s Thesis, Department of Computer Science, University of Toronto, 2009.