# Sherlock is Around: Detecting Network Failures with Local Evidence Fusion

Qiang Ma1, Kebin Liu2, Xin Miao1, Yunhao Liu1,2

1 Department of Computer Science and Engineering, Hong Kong University of Science and Technology

2 MOE Key Lab for Information System Security, School of Software,

Tsinghua National Lab for Information Science and Technology, Tsinghua University

{maq, kebin, miao, liu}@greenorbs.org

Abstract—Traditional approaches for wireless sensor network diagnosis are mainly sink-based. They actively collect global evidences from sensor nodes to the sink so as to conduct centralized analysis at the powerful back-end. On the one hand, long distance proactive information retrieval incurs huge transmission overhead; On the other hand, due to the coupling effect between diagnosis component and the application itself, sink often fails to obtain complete and precise evidences from the network, especially for the problematic or critical parts. To avoid large overhead in evidence collection process, self-diagnosis injects fault inference modules into sensor nodes and let them make local decisions. Diagnosis results from single nodes, however, are generally inaccurate due to the narrow scope of system performances. Besides, existing self-diagnosis methods usually lead to inconsistent results from different inference processes. How to balance the workload among the sensor nodes in a diagnosis task is a critical issue. In this work, we present a new in-network diagnosis approach named Local-Diagnosis (LD2), which conducts the diagnosis process in a local area. LD2 achieves diagnosis decision through distributed evidence fusion operations. Each sensor node provides its own judgements and the evidences are fused within a local area based on the Dempster-Shafer theory, resulting in the consensus diagnosis report. We implement LD2 on TinyOS 2.1 and examine the performance on a 50 nodes indoor testbed.

# I. INTRODUCTION

Wireless sensor networks (WSNs) have been widely used in many critical application domains such as environment monitoring, infrastructure protection, and habitat tracing [8], [23]. These systems often need to sustain for years, and operate reliably in the context of real world communications. Sensor nodes, however, are error-prone and subject to component faults, performance degradations and even major system failures in real world deployments [22], [14], [17], [20], [12], [19]. Thus, accurate and real-time fault diagnosis plays a very important role in WSN system operations. Compared to conventional networks, it is more challenging to explore the root causes for WSNs when abnormal symptoms are observed. First, due to the negative impact of noisy environments and the ad-hoc feature of WSNs, it is difficult for developers to deeply delve into the in-network behaviors among the sensor nodes, especially for large-scale networks in which the forwarding infrastructure dynamically changes as topology or sensor activity varies [10]. Second, the sensor nodes have limited power and computing capability to carry out advanced network diagnosis programs. Third, the existence of a large variety of specific protocols for WSNs also exacerbates the debugging and diagnosis problems.

![](images/b45116b827d31e31a05bca4407113cece6a12f7fd3d64cf1ba6ccfc3ccffba62.jpg)



Fig. 1. A part of CitySee deployment

This work is motivated from our ongoing urban carbon dioxide sensing project, CitySee. CitySee carries out several applications such as carbon emissions monitoring and atmospheric concentrations of carbon dioxide estimating. Figure 1 shows a part of the CitySee system with 494 sensor nodes (CitySee totally deploys 1196 nodes). During the operation period, we observe frequent abnormal symptoms in the network such as high data loss, temporary disconnection of nodes in a certain region, and the like. To troubleshoot the root causes of these symptoms, we have applied different failure detection approaches. Existing approaches are generally sinkbased. They expect to retrieve detailed metrics from managed nodes such as remaining energy, MAC layer backoff, neighbor table, routing table, etc. The network administrators then conduct comprehensive analysis at the back-end.

In practice, however, it is difficult to apply sink-based approaches in large-scale WSNs. On the one hand, a largescale WSN usually consists of hundreds or thousands of sensor nodes, such that most of the nodes have to forward their packets to the sink through many hops. Besides, most existing sinkbased approaches require to collect more diagnosis data than application data. Therefore, proactive information retrieval in a large-scale network generally incurs huge transmission overhead. On the other hand, due to the unreliable nature of wireless communications, sink often fails to obtain complete evidences from the network. In addition, it is more difficult to retrieve expected information from a problematic region.

Instead of back-end analysis, self-diagnosis approaches inject fault inference modules into sensor nodes and let them make local decisions. These approaches, however, may suffer from the narrow scope of single node. Some of the selfdiagnosis methods like TinyD2 propose to let fault detectors travel among different sensors [11]. Such a method, however, does not well handle the diverse judgements from different nodes so that it leads to inconsistent diagnosis reports at different network regions. Since single node only has limited computation and energy resources, we have to balance the workload among nodes in an in-network diagnosis process, while guarantee that an integrated judgement can be achieved.

To address these issues, we present a new in-network diagnosis approach called Local-Diagnosis (LD2). Instead of retrieving the system state information to sink, LD2 carries out the diagnosis process in a local area. We first select some sensor nodes in a local area where abnormal symptoms are observed. We then conduct a process of evidence fusion to explore the most possible root causes. Eventually a diagnosis report is generated and sent to the sink. Compared with existing approaches, LD2 achieves very high energy efficiency. In CitySee, we observe that almost all the root causes can be partly reflected by the sensor nodes within a neighborhood, while each single sensor node has very limited knowledge to complete a comprehensive diagnosis process. Therefore, LD2 actually not only avoids a large transmission overhead and information loss on the way to sink, but also achieves high diagnosis accuracy. Moreover, it provides in-time diagnosis results since it utilizes the first-hand evidence without delay in the collection process.

In order to deal with the narrow scope of single nodes and inconsistent judgements from different nodes, we train a Naive Bayesian Classifier (NBC) which encodes the probabilistic correlation between a set of state attributes and root causes. We insert this Bayesian classifier into the sensor nodes to compute the posterior probability distribution of possible root causes according to their states. That is, each node translates its local evidences (i.e., state attributes) into our communication model which is based on Dempster-Shafer theory (D-S theory). Using D-S theory, we design a novel strategy to fuse the judgements from all the sensor nodes within a neighborhood in a flexible and load-balanced manner. Once a node has detected some abnormal symptoms, it constructs a tree in a local area to strictly depict the fusion order, so as to ensure diagnosis coverage and make fusion process as a long string of sequential operations. The advantages of this serial manner are two-fold. First, instead of collecting all the information on one certain node, we divide the work of evidence fusion into many steps, thus each node can summarize the evidences of its child nodes. That is, we let all the nodes in a local area share the responsibility of diagnosis. Second, the contribution of each node converges on the root node of the tree, so that we can easily ensure a local consensus to the final diagnosis result. Moreover, our diagnosis result is consistent, regardless of the fusion order.

The rest of this paper is organized as follows. Section II summarizes the related work. Section III describes the system framework. Section IV presents our design and provides additional techniques to deal with several practical issues on implementation. Section V shows performance evaluation results from real indoor testbed experiments. Section VI concludes the work.

# II. RELATED WORK

Most existing approaches for sensor network diagnosis are sink-based, in which each sensor reports its state information to the sink by periodically transmitting specific control messages. Sympathy [17] and Emstar [4] rely heavily on an add-in protocol that generates a large amount of status information from individual sensor nodes to the sink, introducing high overhead to the resource constrained sensor networks. In order to minimize the overhead, some researchers propose to establish certain inference models by marking the data packets [13] [14], and then parse the results at the sink to infer the network status. Claivoyant [25] is a notable tool which focuses on debugging sensor nodes at the source-level, and enables developers to wirelessly connect to remote sensors and execute debugging commands. Declarative TracePoints [2] allows the developers to insert a group of action-associated checkpoints at runtime. Find [5] detects faculty nodes by ranking sensing readings collected from natural event detection while the network performs its routine tasks. Agnostic Diagnosis [15] discovers the silent failures by tracking the changes and anomalies of correlation graphs between the system metrics. MintRoute [21] visualizes the network topology by collecting neighbor tables from sensor nodes. LiveNet [3] provides a set of tools and techniques for reconstructing complex dynamics of live sensor networks. In [1], the authors use monitoring paths and cycles to localize single link and Shared Risk Link Group failures. Self-diagnosis [11] plants a finite state machine into each sensor node, enabling them to accordingly change the diagnosis state. Nevertheless, it proves difficult to achieve consensus between the nodes as each node can change the state whenever it receives the diagnosis requests.

Data fusion techniques are also related to this work. [7] outlines the ideas of D-S theory and presents the basic D-S fusion equation. It also mentions that D-S theory becomes unavailable when the evidences are significantly conflicting with each other. [18], [24], [9] discuss how to change the combination rules to eliminate the impact of conflicting evidences, while [6], [16] claim that a better way is to modify the evidences, e.g., adding a basic confidence to describe the importance for each evidence.

![](images/19ff330ed6ee7969abf3b6d04a2dba11dc1569e3ffe8c6b9889833e80b06ab30.jpg)



Fig. 2. The system framework of LD2

# III. SYSTEM FRAMEWORK

In this section, we introduce the general idea of our approach and show an overview of the system framework. As illustrated in Fig. 2, our main idea is to conduct the diagnosis process in a local area where abnormal symptoms are observed. Unlike the traditional sink-based approaches, in-network diagnosis has following challenges. First, the diagnosis process is in a distributed manner, which means, all nodes in this neighborhood are required to be involved into the diagnosis task. To make the nodes be able to cooperate with each other, a feasible communication model for evidence delivery among the nodes must be well designed. The most naive design is to select a cluster head which collects all the state attributes from local nodes. Then some light-weight diagnosis algorithms can be leveraged to find out the root causes. Nevertheless, this way is proved unfeasible as we can hardly find such a diagnosis algorithm that it can be well planted in a resource-limited sensor node as well as performs good accuracy. Second, as mentioned above, to avoid putting all the workload of diagnosis on a certain sensor, the diagnosis process should be dividable so that we are able to let each node join in the diagnosis work but not just deliver their local information to others. Third, for one sensor, its original local information only includes the state attributes such as energy, MAC layer backoff, neighbor table, routing table, etc. There must be some algorithms for the nodes to refine those rough data, so as to generate some kinds of data for the fusion work.

The data-flow of LD2 is illustrated in Fig. 2. As we can see, the basic module applies a Naive Bayesian Model which encodes the probabilistic correlation between a set of state attributes and root causes. After the transition, we get basic probability assignment on the root causes. The module of diagnosis trigger determines whether some abnormal symptoms exist. If so, it needs to start a new diagnosis process. For example, if some local state values experience abnormal changes or some special events occur like a neighbor node has been removed from the neighbor for a long time, the trigger module motivates a new diagnosis process to check that whether this neighbor has crashed or not.

At the very beginning of a diagnosis process, a fusion tree rooted by this sensor node is established. Each node within this diagnosis area is involved in this tree. Actually the diagnosis process is divided into several operations of evidence fusion. Following this fusion tree, the diagnosis process is partly executed by the intermediate nodes. The evidence fusion module is based on D-S theory which is also known as the theory of belief functions. D-S theory is a generalization of the Bayesian theory of subjective probability. By combining the unique characters of WSNs, we design an improved approach by assigning basic confidence to the evidences according to their different significances for the fusion system.

# IV. MAIN DESIGN

In this design, we consider both diagnosis efficiency and diagnosis accuracy. On the one hand, in order to avoid long distance evidence retrieval which leads to large communication overhead, we claim to carry out the diagnosis process locally but not at the back-end. On the other hand, to improve our diagnosis accuracy, we need to take judgements from all nodes within a local area into consideration, as one single node only has limited scope and computation ability. To make the nodes cooperate with each other to complete the diagnosis work, a serial of interfaces and protocols need to be designed like innode data processing, in-network communication model. In the following subsections, we show the design details of LD2.

# A. Overview

Sink-based approaches retrieve state information from the network so as to conduct centralized analysis. They believe that a big picture of network is greatly helpful for network diagnosis, as many evidences can be leveraged to validate the diagnosis result. In CitySee, however, we observe that almost all the root causes can be partly reflected by the sensor nodes within a neighborhood. For example, if a sensor node has crashed, its neighbors must realize that it stops sending beacon messages for neighbor discovering. When a route loop occurs, by checking the network layer sequence number (e.g., CTP sequence number), the nodes in the loop can realize that some packets are repeatedly forwarded. Locally diagnosing the network achieves real-time diagnosis, avoiding information lost on the collection path to the sink. At the same time, compared to one node, LD2 integrates more evidences to validate the result and thus achieves higher accuracy.

# B. Naive Bayesian Classifier

Considering the resource limitation of sensor nodes, fault detection within one single node should be achieved in energy efficient way and many existing models can be applied. For example, we can leverage simple rule-based models to make decision based on the local evidences. Light-weight probabilistic classifiers like the Naive Bayesian Classifier can also be applied. We use a binary variable R to denote each type of root cause and $P ( R )$ and $P ( \neg R )$ are the probabilities that this failure occurs or not. Then in a diagnosis process, sensor node is able to calculate the posterior probability of R given its local evidences, according to the Naive Bayesian model:

$$
P (R | F _ {1}, F _ {2}, \ldots F _ {n}) = \frac {1}{P (F _ {1} , F _ {2} , \ldots F _ {n})} P (R) \prod_ {i = 1} ^ {n} P (F _ {i} | R)
$$

Where $P ( F _ { 1 } , F _ { 2 } , . . . F _ { n } )$ is a scaling factor which only depends on the evidences $( F _ { 1 } , F _ { 2 } , . . . , F _ { n } ) . \ ( F _ { 1 } , F _ { 2 } , . . . , F _ { n } )$ denotes the metrics of current sensor node as well as its neighbors. During the training stage, we should estimate the value of $P ( R ) , P ( \neg R )$ and $P ( F _ { i } | R )$ . These parameter values can be learned from the historical data. The storage cost of Naive Bayesian classifier is $( 1 + 2 n r )$ parameters for each failure type where n denotes the number of metrics and each metric has r discrete values (Considering the computation capability of sensor nodes, we discretize the continuous metrics in this work to simplify the probability computation).

# C. Evidence Fusion

How to make multiple nodes within a local area cooperate with each other to detect network failures is non-trivial. The main challenges are three-fold. First, communication about evidence transferring must use channel itself, which means, we have no out-of-band channel for diagnosis. If we incur a large amount of transmission overhead during the evidence fusion, new network failures may happen, which is also known as Heisenbug. Second, complicated fusion algorithms are not applicable for the system as a sensor node is resource limited. For the same reason, the algorithm should be dividable to avoid putting much data at one node. Third, the algorithm must ensure a local consensus to the final diagnosis report. Moreover, to achieve real-time diagnosis, the period of diagnosis process must be short.

1) Improved Dempster-Shafer Theory: D-S theory is a generalization of the Bayesian theory of subjective probability. It is based on two ideas: the idea of obtaining degrees of belief for one question from subjective probabilities for a related question, and Dempster’s rule for combining such degrees of belief when they are based on independent items of evidence.

Suppose $m _ { 1 }$ and $m _ { 2 }$ are two basic probability assignments $( \mathrm { i . e . }$ , mass function) over the frame of discernment W . Intuitively, $m _ { i } ( U )$ describes the extent to which the evidence supports U , where $U \in { 2 ^ { W } , i = 1 , 2 }$ . The fusion formula by D-S theory is:

$$
m _ {1 2} (X _ {i}) = \left\{ \begin{array}{l l} \frac {\sum_ {A _ {j} \wedge B _ {k} = X _ {i}} m _ {1} (A _ {j}) m _ {2} (B _ {k})}{1 - \sum_ {A _ {j} \wedge B _ {k} = \phi} m _ {1} (A _ {j}) m _ {2} (B _ {k})} & \text {if} X _ {i} \neq \phi \\ 0 & \text {if} X _ {i} = \phi \end{array} \right.
$$

Where $X _ { i } , A _ { j } , B _ { k } \in 2 ^ { W }$ .

$\begin{array} { r } { k _ { 1 2 } = \sum _ { A _ { i } \wedge B _ { k } = \phi } m _ { 1 } ( A _ { j } ) m _ { 2 } ( B _ { k } ) } \end{array}$ is called conflict factor of two evidences $m _ { 1 }$ and $m _ { 2 }$ . Notably, there can be two evidences $m _ { 1 }$ and $m _ { 2 }$ which are totally conflicting such that $k _ { 1 2 } = 1$ , therefore mass functions are not always combinable. What is more, even if they are not totally conflicting but highly conflicting, that is, $k _ { 1 2 }  1$ , the combination result always goes against the practical sense. Many works are proposed to address this issue. In general, they can be classified into two types. One is to modify the combination rules, while the other one is to improve the evidence models.

The methods to modify the combination rules discuss two cases when the evidences are reliable and unreliable respectively. Nevertheless, they both mainly consider how to assign the conflicting evidence, like how to decide the ratio between the event possibilities when conflict happens. In [18], the authors propose that on the basis of reliable evidences, the main reason of conflict is the incompleteness in the frame of discernment, i.e., some unknown event possibilities exist. [24], [9] all believe that not all the evidences are reliable. They propose that the conflicting part between the evidences should be discarded or reassigned to the other possibilities. In practice, when there are a large amount of evidences need to join in the fusion task, we hope that the evidences can be grouped by some metrics such that we can conduct the fusion task regardless of the fusion order to reduce the computation work. Unfortunately, above improved methods all fail to support associative law. This work fully combines the unique characters of WSNs, and designs following improved D-S theory for LD2.

Suppose the frame of discernment in our evidence model is $W ~ = ~ \{ R _ { 0 } , R _ { 1 } , . . . R _ { n } \}$ . W consists of different root causes $\{ R _ { 1 } , R _ { 2 } , . . . R _ { n } \}$ in the network. Besides, it also has a basic event “no problem” $R _ { 0 } .$ , which indicates that no exact diagnosis result is produced. We let each node $N _ { i }$ only generates possibility value $m _ { i } ( R _ { j } )$ for each single root cause $R _ { j }$ according to its own local information. That is, $m _ { i } ( U ) = 0$ for any $U \in 2 ^ { W }$ and $\begin{array} { r } { | U | > 1 . \sum _ { 0 < j < n } m _ { i } ( R _ { j } ) = 1 } \end{array}$ .

Definition 1. The distance between $m _ { 1 }$ and $m _ { 2 }$ is:

$$
d (m _ {1}, m _ {2}) = \sqrt {\frac {1}{2} (M _ {1} - M _ {2}) ^ {T} (M _ {1} - M _ {2})}
$$

Where $M _ { i } = [ m _ { i } ( R _ { 0 } ) , m _ { i } ( R _ { 1 } ) , . . . m _ { i } ( R _ { n } ) ] ^ { T } , i = 1 , 2$ , and we also have $0 \leq d ( m _ { 1 } , m _ { 2 } ) \leq 1 ;$

$$
\begin{array}{l} d (m _ {1}, m _ {2}) = \sqrt {\frac {1}{2} \sum_ {0 \leq j \leq n} (m _ {1} (R _ {j}) - m _ {2} (R _ {j})) ^ {2}} \\ = \sqrt {\frac {1}{2} \sum_ {0 \leq j \leq n} (m _ {1} ^ {2} (R _ {j}) + m _ {2} ^ {2} (R _ {j}) - 2 m _ {1} (R _ {j}) m _ {2} (R _ {j}))} \\ \leq \sqrt {\frac {1}{2} \sum_ {0 \leq j \leq n} (m _ {1} ^ {2} (R _ {j}) + m _ {2} ^ {2} (R _ {j}))} \\ \end{array}
$$

$$
\leq \sqrt {\frac {1}{2} [ (\sum_ {0 \leq j \leq n} m _ {1} (R _ {j})) ^ {2} + (\sum_ {0 \leq j \leq n} m _ {2} (R _ {j})) ^ {2} ]} = 1
$$

Definition 2. The similar degree of $m _ { 1 }$ and $m _ { 2 }$ is:

$$
s (m _ {1}, m _ {2}) = 1 - d (m _ {1}, m _ {2})
$$

As we can see, the greater similar degree of $m _ { 1 }$ and $m _ { 2 }$ , the more similar analysis two evidences describe. If we have one evidence which is similar to all the others, then we believe that this evidence is important. Suppose we have N evidences $e _ { 1 } , ~ e _ { 2 } , ~ . . . ~ e _ { N }$ , and their corresponding basic probability assignments are $m _ { 1 } , m _ { 2 } , \dotsm m _ { N }$ .

Definition 3. The basic confidence of $e _ { i } \ ( i = 1 , 2 . . . N )$ is:

$$
\beta_ {i} = \sum_ {1 \leq j \leq N, j \neq i} s (m _ {i}, m _ {j})
$$

To avoid huge computation cost, sometimes we can also randomly sample some evidences to compose a standard set S, hence every evidence $m _ { i }$ computes the total similar degree to S as its basic confidence: $\begin{array} { r } { \beta _ { i } = \sum _ { s _ { i } \in S , m _ { i } \neq s _ { i } } s ( m _ { i } , s _ { j } ) } \end{array}$ .

∈ \$ After normalization, we get the relative importance of $m _ { i }$ to the evidence which has the greatest basic confidence: $\psi _ { i } = \beta _ { i } / \mathrm { m a x } _ { 1 \leq j \leq N } \beta _ { j }$ . The normalization could be omitted when the fusion task is divided into small ones and a global maximum value is unknown, i.e., $\psi _ { i } = \beta _ { i }$ . Then we transfer the basic probability assignments by multiplying the basic confidence, making them of equal importance in new fusion system:

$$
m _ {i} ^ {\prime} (R _ {i}) = \psi_ {i} m _ {i} (R _ {i}) \quad \forall 1 \leq i \leq n.
$$

$$
m _ {i} ^ {\prime} (R _ {0}) = \psi_ {i} m _ {i} (R _ {0}) + (1 - \psi_ {i})
$$

Notably, if there are only two evidences involved in the fusion task. Because $s ( m _ { i } , m _ { j } ) = s ( m _ { j } , m _ { i } )$ , they have the same basic confidence even if one of them provides inaccurate evidence. To address this issue, we need to set a threshold $F _ { t }$ such that more than $F _ { t }$ evidences are allowed to utilize Definition 3 to conduct evidence fusion. In our implementation, we set $F _ { t }$ equals 4.

In this new fusion system, for $R _ { i } \ ( \mathrm { i } { = } 1 , 2 . . . \ \mathrm { n } )$ , we reduce the impact of those evidences with less importance. That is, to confirm whether $R _ { i }$ happens or not mainly relies on the other evidences. On the contrary, for $R _ { 0 }$ we increase the impact of those evidences with less importance, so as to average the confidence to the other root causes. After transferring the basic probability assignments, all the evidences are of equal importance, then we can utilize D-S theory to conduct evidence fusion. Our improved D-S theory is designed for LD2’s evidence model. We choose not to change the combination rules but refine the evidences. It also satisfies that the fusion result keeps the same even if we change the fusion order, i.e., supports associative law. It is very important for our design, as we can’t ensure that the fusion tree has the same architecture all the time (details in subsection Fusion Algorithm).

Theorem 1. $m _ { ( 1 2 ) 3 } ^ { \prime } ( X _ { i } ) = m _ { 1 ( 2 3 ) } ^ { \prime } ( X _ { i } )$

PROOF. m&(12)3(Xi) = Aj ∧Bk=Xi 12 31− % Aj ∧Bk=φ m"12(Aj )m"3(Bk) $\mathrm { P R O O F . } \quad m _ { ( 1 2 ) 3 } ^ { \prime } ( X _ { i } ) = \frac { \sum _ { A _ { j } \wedge B _ { k } = X _ { i } } m _ { 1 2 } ^ { \prime } ( A _ { j } ) m _ { 3 } ^ { \prime } ( B _ { k } ) } { 1 - \sum _ { A _ { j } \wedge B _ { k } = \phi } m _ { 1 2 } ^ { \prime } ( A _ { j } ) m _ { 3 } ^ { \prime } ( B _ { k } ) }$

$$
= \frac {\sum_ {A _ {j} \wedge B _ {k} = X _ {i}} (\frac {\sum_ {C _ {l} \wedge D _ {t} = A _ {j}} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t})}{1 - \sum_ {C _ {l} \wedge D _ {t} = \phi} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t})}) m _ {3} ^ {\prime} (B _ {k})}{1 - \sum_ {A _ {j} \wedge B _ {k} = \phi} (\frac {\sum_ {C _ {l} \wedge D _ {t} = A _ {j}} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t})}{1 - \sum_ {C _ {l} \wedge D _ {t} = \phi} m _ {1} ^ {\prime} (C _ {l}) m _ {2} (D _ {t})}) m _ {3} ^ {\prime} (B _ {k})}
$$

$$
= \frac {\sum_ {A _ {j} \wedge B _ {k} = X _ {i}} (\frac {\sum_ {C _ {l} \wedge D _ {t} = A _ {j}} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t})}{1 - \sum_ {C _ {l} \wedge D _ {t} = \phi} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t})}) m _ {3} ^ {\prime} (B _ {k})}{\sum_ {A _ {j} \wedge B _ {k} \neq \phi} (\frac {\sum_ {C _ {l} \wedge D _ {t} = A _ {j}} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t})}{1 - \sum_ {C _ {l} \wedge D _ {t} = \phi} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ' (D _ {t})}) m _ {3} ^ {\prime} (B _ {k})}
$$

$$
= \frac {\sum_ {C _ {l} \wedge D _ {t} \wedge B _ {k} = X _ {i}} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t}) m _ {3} ^ {\prime} (B _ {k})}{\sum_ {C _ {l} \wedge D _ {t} \wedge B _ {k} \neq \phi} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t}) m _ {3} ^ {\prime} (B _ {k})}
$$

Similarly, we can prove that:

$$
\begin{array}{l} m _ {1 (2 3)} ^ {\prime} (X _ {i}) = \frac {\sum_ {C _ {l} \wedge D _ {t} \wedge B _ {k} = X _ {i}} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t}) m _ {3} ^ {\prime} (B _ {k})}{\sum_ {C _ {l} \wedge D _ {t} \wedge B _ {k} \neq \phi} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t}) m _ {3} ^ {\prime} (B _ {k})} \\ = m _ {(1 2) 3} ^ {\prime} (X _ {i}) \\ \end{array}
$$

2) Fusion Algorithm: In this part we present our specific algorithms for evidence fusion. First we introduce the fusion tree. Every diagnosis process is rooted by a node, which detects abnormal network symptoms such as node crash, traffic contention, route loop and so on. It triggers a diagnosis model as well as determines the diagnosis area, then broadcasts diagnosis request beacons (DREQ) to establish the fusion tree. Basically we need to determine the diagnosis area for each symptom. For example, to find out whether a node has crashed or not can ask for one-hop neighbors’ evidences, while to find out whether a route loop exists or not should visit all the nodes transmitting the relevant packets. All the information must be involved in DREQ for the nodes to know about the details of diagnosis task. To the other nodes, after receiving DREQ, they are involved in the fusion tree if they locate in the diagnosis area. Once they join in the fusion tree, they should keep broadcasting DREQ to inform other related nodes. In the process of constructing fusion tree, each node records its parent node and child nodes for following evidence collection.

Notably, in the process of establishing fusion tree, the root also needs to sample a standard set for following evidence fusion. As mentioned above, utilizing standard set can reduce the computation cost. Besides, in our fusion system, it greatly reduces the transmission overhead as we have no need to collect all the evidences to assign a global basic confidence. In LD2, we make the standard set consist of the evidences from the root node and its direct child nodes. Every DREQ packet contains standard set such that each node in the fusion tree is able to calculate its own basic confidence respectively.

The establishment of fusion tree finishes until no DREQ is transmitted. What follows is the evidence fusion process. First all the leaf nodes send out a leaf-query beacon (LQUE) to make sure that it indeed has no child node in the fusion tree. Actually LQUE is used to make up the lost DREQ. If there is no reply to the LQUE, it transfers its local evidence (DEVI) to its parent node in the tree. Otherwise it updates its child set and waits for the evidences from the child nodes. To the intermediate nodes, they must collect all the evidences from its child nodes and finally sends the fusion result to its parent node. To avoid evidence lost, each intermediate node is able to “remind” its child nodes by broadcasting child-query beacons (CQUE), hence the lost evidences can be retransmitted.

Algorithm 1 Fusion Tree Establishment Algorithm   
1: Denote the node ID as id.
2: Initiate a null value parentID to record the parent ID.
3: Initiate an empty set $S_{children}$ to record the child nodes.
4: if Trigger component detects abnormal symptoms then
5: Trigger a local-diagnosis process.
6: Determine diagnosis area.
7: Sample the standard set for the fusion system.
8: Broadcast request beacon (DREQ).
9: end if
10: if Receive DREQ then
11: if Already in the tree then
12: Check the parent filed of this DREQ, denoted as p.
13: if p = id then
14: Add the source node of this DREQ into $S_{children}$ .
15: end if
16: else if In the diagnosis area then
17: Assign the source ID of this DREQ to parentID.
18: Update the parent filed value by parentID.
19: Broadcast DREQ.
20: end if
21: end if

As we can see, the structure of fusion tree has much dynamics as we connect the nodes by broadcasting DREQ. What is more, the fusion order strictly follows the fusion tree from leaf nodes to the root node. Fortunately, in Theorem 1 it proves that the fusion result of LD2 keeps consistent, regardless of the fusion order. This character helps our fusion system greatly reduce the maintainance overhead of fusion tree, as well as enable to ignore the impact of network topology.

# V. EVALUATION

We evaluate LD2 through a real indoor testbed consisting of 50 TelosB motes. Two metrics are mainly used for evaluating LD2’s accuracy: false negative rate (i.e., miss detection rate) and false positive rate (i.e., false alarm rate). False negative rate is defined as the proportion of faulty cases which are detected as normal, while false positive rate is defined as the proportion of normal cases which are detected as faulty.

Basically we implement a CTP application in the network, for the analysis of impact with different diagnosis approaches. In this work, we implement two modules for diagnosing the network: LD2 and TinyD2. TinyD2 presents the concept of self-diagnosis which encourages each sensor node to run a embedded finite state machine to find out the root cause.

Algorithm 2 Evidence Fusion Algorithm   
1: if $S_{children}$ is empty (leaf node) then
2: Broadcast leaf-query beacon (LQUE) to ensure that it is a leaf node.
3: if No reply to LQUE then
4: Transmit local evidence (DEVI) to its parent.
5: else
6: Update the child set $S_{children}$ .
7: end if
8: else
9: Maintain an evidence set $S_{evidence}$ to record the received evidences from the child nodes.
10: Add local evidence into $S_{evidence}$ .
11: while Receive DEVI do
12: Add this DEVI into $S_{evidence}$ .
13: end while
14: for each $Child_i$ in $S_{children}$ do
15: if $S_{evidence}$ does not contain the DEVI from $Child_i$ then
16: Transmit child-query beacon (CQUE) to $Child_i$ .
17: end if
18: end for
19: if Has Collected all the evidences from child nodes then
20: Evidence Fusion.
21: Transmit $S_{evidence}$ to parent node.
22: end if
23: end if
24: if Receive LQUE then
25: Check the source ID of this LQUE, denoted as p.
26: if p = parentID then
27: Reply to this LQUE.
28: end if
29: end if
30: if Receive CQUE then
31: Transmit local DEVI.
32: end if

During the tests, we manually inject three types of failures: node crash, traffic contention and the route loop. For each failure, we conduct 60 cases. We also change the power level to discuss the performance of two approaches in different diagnosis densities (i.e., the number of neighbor nodes).

# A. Time Cost

Figure 3(a) illustrates the network topology of our testbed consisting of 50 motes. First we discuss the time cost during the diagnosis process. Generally we divide the cost into two parts: fusion tree establishment and evidence fusion process. As mentioned in section IV, the fusion tree is related to the diagnosis area which is determined by the symptoms. In the experiments, we make above three network failures have the same diagnosis area. Node 25 (i.e., the red mote) has 16 neighbors (i.e., the green motes). When node 25 crashes or traffic contention occurs at node 25, the diagnosis area involves all its neighbors. Besides, we let a routing loop exist among all these neighbors (i.e., the blue arrows). That is, their diagnosis area is the neighbors of node 25. We also make node 13 as the root node of fusion tree.

![](images/80431286d879de825513224906b12b986121bf2bb53338ce74532fa12609af23.jpg)



(a) Network Topology with 50 nodes   
![](images/d8e7272a9568c5c48004d6bafb1f4fda2f452768ca9e0a382777123aa39454c8.jpg)  
(b) 36%

![](images/2250a6206c1a8b118c7ef88dd9cbdb7812ec44342f8db899134e4ec3d37a6895.jpg)  
(c) 31%

![](images/5987624f345b707b6de3aa9fd4db7e90b1c9d1a6f244e22d9cd75f74d304bb12.jpg)  
(d) 18%

![](images/40a3c36354118e66d4a0234f3a46864422937f93b6ad1141de8dbd896b2320db.jpg)  
(e) 9%   
Fig. 3. Testbed topology. We inject three failures in (a) respectively, making their diagnosis area the same: node 25 (red mote) is crashed; traffic contention occurs at node 25; a route loop (blue arrows) exists among node 25’s neighbors (green motes). Besides, we let node 13 (i.e., the blue mote in (b),(c),(d),(e)) trigger the diagnosis process. The tree structure of (b),(c),(d) and (e) respectively occurs 36%,31%,18% and 9% in all the cases.

Figures 3(b) 3(c) 3(d) and 3(e) describe four of most frequent structures when we are establishing the fusion tree. Figure 4 shows the time cost of sampling evidences and establishing fusion tree. As mentioned in section IV, the process of sampling evidences is used to assign a local basic confidence to each node in evidence fusion, while establishing fusion tree mainly includes broadcasting and receiving beacons. As we can see, the time cost is stable for all the tree structures, i.e., about 19ms in sampling evidences and 39ms in establishing fusion tree. Figure 5 shows the CDF of the time cost of evidence fusion in three diagnosis process. In 80% of cases for detecting node crash, LD2 finishes evidence fusion in a 16-node area within 95ms. For traffic contention, it costs more than 133ms for 60% of cases as the DEVI packet contains 3 possible root causes (i.e., ingress overflow, egress overflow, bad link) thus more combination work is needed. Figure 6 depicts the CDF of the total time cost for diagnosing node crash, traffic contention and route loop respectively. We observe similar trends in two CDF figures as the process of evidence fusion costs most of time in LD2.

![](images/99a3e07c2dda9a6b4750ce948332806c8fa2a815af18694ccd8cbb9046720a8e.jpg)



Fig. 4. Time cost of sampling evidences and establishing fusion tree

![](images/41fed98b3cba0dcfd0b2be2802cb8d653ae1d5a88bbf33c0718ec22abb712ee4.jpg)



![](images/13399f14de42131107381d901495df54e32ae3ff6c74f194bd1bf60e0b01c8ea.jpg)



Fig. 5. CDF of evidence fusion’s time cost   
Fig. 6. CDF of total time cost

# B. Diagnosis Accuracy

Figures 7  12 illustrate the diagnosis results of detecting node crash, traffic contention and route loop with LD2 and TinyD2 respectively. According to Fig. 7, LD2 enables to troubleshoot more than 92% of crashed nodes, and the false negative rate decreases when the number of neighbors increases. It is well understood that once a node is crashed, its neighbor must find that it is removed from the neighbor tables for a long period. Therefore, the more neighbors, the more determinate diagnosis. As showed in Fig. 10, the false positive rate of LD2 is around 12% over varying diagnosis densities. For detecting route loop, each node produces its evidence by checking the CTP sequence number. As illustrated in Fig. 9 and 12, LD2 indeed maintains low false negative rate and false positive rate, i.e., 5% and 6%, which means that LD2 can successfully explore about 95% of route loops. By contrast, TinyD2 performs unstable to detect crashed nodes and route loops under different diagnosis densities. When the density increases, TinyD2 often fails to achieve a consensus among the nodes, such that hardly determines a root cause.

According to Fig. 8, LD2 correctly explores about 86% of traffic contention, while TinyD2 is able to find out 78% of cases when the number of neighbors is 16. Traffic contention occurs due to some reasons, such as egress overflow, ingress overflow and bad link. It proves difficult for TinyD2 to use finite state machine to achieve an accept state. In Fig. 11, as we can see, TinyD2’s false positive rate increases to 22% when the number of neighbors is 16, while LD maintains around

![](images/c69b28295866fc115cdf61e313078c9b7c983c690f7267803e29a4f58c2ee5f9.jpg)



Fig. 7. False negative rate for node crash

![](images/c04fb4eea15a9ed065c5f74bef47017c5e2bd2a563c47c68ffb5aa4e85a2dc01.jpg)



Fig. 8. False negative rate for traffic contention

![](images/9b4fbc40db3a7372398c0ea0966cc963150ddb0e20b54ce42351baf5eb6a8b05.jpg)



Fig. 9. False negative rate for route loop

![](images/f573987b7e6b98c27ab11479ef2a162c1901a291c5e0190ed426169f61980db9.jpg)



Fig. 10. False positive rate for node crash

![](images/ea3a0456efee57db33e0ab8b1e2ddf5e154b1afd66ca7cbe51d08d7d7ad6ae87.jpg)



Fig. 11. False positive rate for traffic contention

![](images/8bb1bae9e7a19e1ab8229ca078af3b274674f1fc3af97148478352e8444ef682.jpg)



Fig. 12. False positive rate for route loop

![](images/1e27bfe5f61361b3e8b28e30d9b8ce5538eba46a5d318c8b316f3be94b3264c4.jpg)



Fig. 13. Packet collection in LD2

![](images/b694c7099a2cef8efc8aad64bf7fa99ad26f1f6b10422ece7e4e9a819e71700e.jpg)



Fig. 14. Packet collection in TinyD2

16% under different diagnosis densities.

# C. Coupling Effect with Application

Finally we discuss the coupling effect between the application and network diagnosis. We observe that most of sinkbased approaches needs to retrieve more network information than that generated by the application. It proves unreasonable because some network failures such as traffic contention, bad routing, can occur due to frequent large-amount collection. TinyD2 reduces the transmission overhead by broadcasting fault detector in the air. In practice, however, it lacks of a specific order to control the diagnosis and ensure a consensus result. What is more, once it can’t achieve the accept state, much extra transmissions are required. Figure 13 and 14 depict the packet collection of those nodes in the diagnosis area, and each dot indicates an application packet collected by the sink. As we can see, when we utilize TinyD2 to conduct the diagnosis process in the local area around timeline 30000ms, 40000ms and 50000ms, most application packets are lost. To find out the root cause, we also sniffer the beacons in this area. As illustrated by Fig. 15, in the diagnosis process, every node in TinyD2 generates about 28 beacons within 200ms, which probably causes a local traffic contention. By contrast, the root node and intermediate nodes in LD2 only cause about 15 and 10 beacons in 200ms.

![](images/5189dea9561418ad38d9934aa30028fd7802648b6eeb33d07d51dc3d47de631f.jpg)



Fig. 15. Beacon transmissions in diagnosis process

# VI. CONCLUSION

Long distance proactive information retrieval in traditional sink-based approaches to diagnosing WSNs often incurs a large amount of transmission overhead. What is more, sinkbased approaches can not afford real-time diagnosis. Conversely, sensor nodes have the first-hand evidences to conduct diagnosis process, but due to the narrow scope of system state information, diagnosis results from single nodes are generally inaccurate. To balance this tradeoff, this work presents LD2, which conducts the diagnosis process in a local area. LD2 claims to distribute the diagnosis workload to the sensor nodes within a diagnosis area. By constructing a fusion tree, each node summarizes the evidences of its child nodes, such that the contribution of each node converges on the root node. Thus, a local consensus to the final diagnosis report is generated and reported to the sink. We also implement LD2 on TinyOS 2.1 and evaluate the performance on a real indoor testbed consisting of 50 nodes.

# ACKNOWLEGMENT

This research is supported in part by the NSFC Distinguished Young Scholars Program under Grant No. 61125202, NSFC under Grant No. 61103187, and China Postdoctoral Science Foundation under Grant No. 2011M500330.

# REFERENCES

[1] S.S. Ahuja, S. Ramasubramanian, and M.M. Krunz. Single-link failure detection in all-optical networks using monitoring cycles and paths. IEEE/ACM Transactions on Networking, 17(4):1080–1093, 2009.

[2] Q. Cao, T. Abdelzaher, J. Stankovic, K. Whitehouse, and L. Luo. Declarative tracepoints: a programmable and application independent debugging system for wireless sensor networks. In Proceedings of ACM SenSys, Raleigh, NC, USA, 2008.   
[3] B. Chen, G. Peterson, G. Mainland, and M. Welsh. Livenet: Using passive monitoring to reconstruct sensor network dynamics. In Proceedings of IEEE DCOSS, Santorini Island, Greece, 2008.   
[4] L. Girod, J. Elson, A. Cerpa, T. Stathopoulos, N. Ramanathan, and D. Estrin. Emstar: a software environment for developing and deploying wireless sensor networks. In Proceedings of the USENIX Annual Technical Conference, Boston, MA, 2004.   
[5] S. Guo, Z. Zhong, and T. He. Find: faulty node detection for wireless sensor networks. In Proceedings of ACM SenSys, Berkeley, California, 2009.   
[6] R. Haenni. Are alternatives to dempster’s rule of combination alternatives? comments on “about the belief combination and the conflict management problem”. Int. J. Information Fusion, 3(3):237–241, 2002.   
[7] D. Koks and S. Challa. An introduction to bayesian and dempster-shafer data fusion. Technical Report DSTOTR1436, Australian Department of Defence, 2003.   
[8] J. Kong, J. Cui, D. Wu, and M. Gerla. Building underwater adhoc networks and sensor networks for large scale real-time aquatic applications. In Proceedings of IEEE MILCOM, Atlantic City, New Jersey, 2005.   
[9] E. Lefevre, O. Colot, P. Vannoorenberghe, and D. De Brucq. A generic framework for resolving the conflict in the combination of belief structures. In Proceedings of International Conference on Information Fusion, Paris, France, 2000.   
[10] Z. Li, M. Li, J. Wang, and Z. Cao. Ubiquitous data collection for mobile users in wireless sensor networks. In Proceedings of IEEE INFOCOM, Shanghai, China, 2011.   
[11] K. Liu, Q. Ma, X. Zhao, and Y. Liu. Self-diagnosis for large scale wireless sensor networks. In Proceedings of IEEE INFOCOM, Shanghai, China, 2011.   
[12] S. Liu, G. Xing, H. Zhang, J. Wang, J. Huang, M. Sha, and L. Huang. Passive interference measurement in wireless sensor networks. In Proceedings of IEEE ICNP, Kyoto, Japan, 2010.   
[13] Y. Liu, K. Liu, and M. Li. Passive diagnosis for wireless sensor networks. IEEE/ACM Transactions on Networking, 18(4):1132–1144, 2010.   
[14] E. Magistretti, O. Gurewitz, and E. Knightly. Inferring and mitigating a link’s hindering transmissions in managed 802.11 wireless networks. In Proceedings of ACM MobiCom, Chicago, Illinois, USA, 2010.   
[15] X. Miao, K. Liu, Y. He, Y. Liu, and D. Papadias. Agnostic diagnosis: Discovering silent failures in wireless sensor networks. In Proceedings of IEEE INFOCOM, Shanghai, China, 2011.   
[16] C.K. Murphy. Combining belief functions when evidence conflicts. Decision support systems, 29(1):1–9, 2000.   
[17] N. Ramanathan, K. Chang, R. Kapur, L. Girod, E. Kohler, and D. Estrin. Sympathy for the sensor network debugger. In Proceedings of ACM SenSys, San Diego, USA, 2005.   
[18] P. Smets. The combination of evidence in the transferable belief model. IEEE Transactions on Pattern Analysis and Machine Intelligence, 12(5):447–458, 1990.   
[19] R. Tan, G. Xing, Z. Yuan, X. Liu, and J. Yao. System-level calibration for fusion-based wireless sensor networks. In Proceedings of IEEE RTSS, San Diego, CA, USA, 2010.   
[20] X. Wang, L. Fu, and C. Hu. Multicast performance with hierarchical cooperation. IEEE/ACM Transactions on Networking, 20(3):1–1, 2011.   
[21] A. Woo, T. Tong, and D. Culler. Taming the underlying challenges of reliable multihop routing in sensor networks. In Proceedings of ACM SenSys, Los Angeles, CA, 2003.   
[22] K. Xing, F. Liu, X. Cheng, and D.H.C. Du. Real-time detection of clone attacks in wireless sensor networks. In Proceedings of IEEE ICDCS, Beijing, China, 2008.   
[23] N. Xu, S. Rangwala, K.K. Chintalapudi, D. Ganesan, A. Broad, R. Govindan, and D. Estrin. A wireless sensor network for structural monitoring. In Proceedings of ACM SenSys, Baltimore, Maryland, 2004.   
[24] R.R. Yager. On the dempster-shafer framework and new combination rules. Information sciences, 41(2):93–137, 1987.   
[25] J. Yang, M.L. Soffa, L. Selavo, and K. Whitehouse. Clairvoyant: a comprehensive source-level debugger for wireless sensor networks. In Proceedings of ACM SenSys, Sydney, Australia, 2007.