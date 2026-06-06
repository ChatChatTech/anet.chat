# Sherlock Is Around: Detecting Network Failures with Local Evidence Fusion

Qiang Ma, Member, IEEE, Kebin Liu, Member, IEEE, Xin Miao, Member, IEEE, and Yunhao Liu, Senior Member, IEEE

Abstract—Traditional approaches for wireless sensor network diagnosis are mainly sink-based. They actively collect global evidences from sensor nodes to the sink so as to conduct centralized analysis at the powerful back-end. On the one hand, long distance proactive information retrieval incurs huge transmission overhead; On the other hand, due to the coupling effect between diagnosis component and the application itself, sink often fails to obtain complete and precise evidences from the network, especially for the problematic or critical parts. To avoid large overhead in evidence collection process, self-diagnosis injects fault inference modules into sensor nodes and let them make local decisions. Diagnosis results from single nodes, however, are generally inaccurate due to the narrow scope of system performances. Besides, existing self-diagnosis methods usually lead to inconsistent results from different inference processes. How to balance the workload among the sensor nodes in a diagnosis task is a critical issue. In this work, we present a new in-network diagnosis approach named Local-Diagnosis (LD2), which conducts the diagnosis process in a local area. LD2 achieves diagnosis decision through distributed evidence fusion operations. Each sensor node provides its own judgements and the evidences are fused within a local area based on the Dempster-Shafer theory, resulting in the consensus diagnosis report. We implement LD2 on TinyOS 2.1 and examine the performance on a 50 nodes indoor testbed.

Index Terms—Wireless sensor network, diagnosis, evidence fusion

# 1 INTRODUCTION

WIRELESS sensor networks (WSNs) have been widelyused in many critical application domains such as used in many critical application domains such as environment monitoring, infrastructure protection, and habitat tracing [1], [2]. These systems often need to sustain for years, and operate reliably in the context of real world communications. Sensor nodes, however, are error-prone and subject to component faults, performance degradations and even major system failures in real world deployments [3], [4], [5], [6], [7], [8]. Thus, accurate and real-time fault diagnosis plays a very important role in WSN system operations. Compared to conventional networks, it is more challenging to explore the root causes for WSNs when abnormal symptoms are observed. First, due to the negative impact of noisy environments and the ad-hoc feature of WSNs, it is difficult for developers to deeply delve into the in-network behaviors among the sensor nodes, especially for large-scale networks in which the forwarding infrastructure dynamically changes as topology or sensor activity varies [9]. Second, the sensor nodes have limited power and computing capability to carry out advanced network diagnosis programs. Third, the existence of a large variety of specific protocols for WSNs also exacerbates the debugging and diagnosis problems.

This work is motivated from our ongoing urban carbon dioxide sensing project, CitySee. CitySee carries out several

applications such as carbon emissions monitoring and atmospheric concentrations of carbon dioxide estimating. Fig. 1 shows a part of the CitySee system with 494 sensor nodes (CitySee totally deploys 1,196 nodes). During the operation period, we observe frequent abnormal symptoms in the network such as high data loss, temporary disconnection of nodes in a certain region, and the like. To troubleshoot the root causes of these symptoms, we have applied different failure detection approaches. Existing approaches are generally sink-based. They expect to retrieve detailed metrics from managed nodes such as remaining energy, MAC layer backoff, neighbor table, routing table, etc. The network administrators then conduct comprehensive analysis at the back-end.

In practice, however, it is difficult to apply sink-based approaches in large-scale WSNs. On the one hand, a largescale WSN usually consists of hundreds or thousands of sensor nodes, such that most of the nodes have to forward their packets to the sink through many hops. Besides, most existing sink-based approaches require to collect more diagnosis data than application data. Therefore, proactive information retrieval in a large-scale network generally incurs huge transmission overhead. On the other hand, due to the unreliable nature of wireless communications, sink often fails to obtain complete evidences from the network. In addition, it is more difficult to retrieve expected information from a problematic region.

Instead of back-end analysis, self-diagnosis approaches inject fault inference modules into sensor nodes and let them make local decisions. These approaches, however, may suffer from the narrow scope of single node. Some of the self-diagnosis methods like TinyD2 propose to let fault detectors travel among different sensors [10]. Such a method, however, does not well handle the diverse judgements from different nodes so that it leads to inconsistent diagnosis reports at different network regions. Since single node only has limited computation and energy resources, we have to balance the workload among nodes in an in-network diagnosis process, while guarantee that an integrated judgement can be achieved.

![](images/73ff5ef4783a72149e598b75c9db64a804e120eedf978316f0a39bb4a9d074e2.jpg)



Fig. 1. A part of CitySee deployment.

To address these issues, we present a new in-network diagnosis approach called local-diagnosis (LD2). Instead of retrieving the system state information to sink, LD2 carries out the diagnosis process in a local area. We first select some sensor nodes in a local area where abnormal symptoms are observed. We then conduct a process of evidence fusion to explore the most possible root causes. Eventually a diagnosis report is generated and sent to the sink. Compared with existing approaches, LD2 achieves very high energy efficiency. In CitySee, we observe that almost all the root causes can be partly reflected by the sensor nodes within a neighborhood, while each single sensor node has very limited knowledge to complete a comprehensive diagnosis process. Therefore, LD2 actually not only avoids a large transmission overhead and information loss on the way to sink, but also achieves high diagnosis accuracy. Moreover, it provides intime diagnosis results since it utilizes the first-hand evidence without delay in the collection process.

In order to deal with the narrow scope of single nodes and inconsistent judgements from different nodes, we train a Naive Bayesian Classifier (NBC) which encodes the probabilistic correlation between a set of state attributes and root causes. We insert this Bayesian classifier into the sensor nodes to compute the posterior probability distribution of possible root causes according to their states. That is, each node translates its local evidences (i.e., state attributes) into our communication model which is based on Dempster-Shafer theory (D-S theory). Using D-S theory, we design a novel strategy to fuse the judgements from all the sensor nodes within a neighborhood in a flexible and load-balanced manner. Once a node has detected some abnormal symptoms, it constructs a tree in a local area to strictly depict the fusion order, so as to ensure diagnosis coverage and make fusion process as a long string of sequential operations. The advantages of this serial manner are twofold. First, instead of collecting all the information on one certain node, we divide the work of evidence fusion into many steps, thus each node can summarize the evidences of its child nodes. That is, we let all the nodes in a local area share the responsibility of diagnosis. Second, the contribution of each node converges on the root node of the tree, so that we can easily ensure a local consensus to the final diagnosis result. Moreover, our diagnosis result is consistent, regardless of the fusion order.

The rest of this paper is organized as follows. Section 2 summarizes the related work. Section 3 describes the system framework. Section 4 presents our design and provides additional techniques to deal with several practical issues on implementation. Section 5 describes the implementation and shows performance evaluation results from real indoor testbed experiments. Section 6 concludes the work.

# 2 RELATED WORK

Most existing approaches for sensor network diagnosis are sink-based, in which each sensor reports its state information to the sink by periodically transmitting specific control messages. Sympathy [5] and Emstar [11] rely heavily on an add-in protocol that generates a large amount of status information from individual sensor nodes to the sink, introducing high overhead to the resource constrained sensor networks. In order to minimize the overhead, some researchers propose to establish certain inference models by marking the data packets [12], [4], and then parse the results at the sink to infer the network status. Claivoyant [13] is a notable tool which focuses on debugging sensor nodes at the source-level, and enables developers to wirelessly connect to remote sensors and execute debugging commands. Declarative TracePoints [14] allows the developers to insert a group of action-associated checkpoints at runtime. Luo et al. [15] leverages an advanced approach to source-level debugging called record and replay, which claims that all I/ O operations are logged during execution and later replayed for central debugging purposes. Based on record and replay, [16] presents a debug tool MDB to support the debugging of macroprograms. Find [17] detects faculty nodes by ranking sensing readings collected from natural event detection while the network performs its routine tasks. Agnostic Diagnosis [18] discovers the silent failures by tracking the changes and anomalies of correlation graphs between the system metrics. MintRoute [19] visualizes the network topology by collecting neighbor tables from sensor nodes. LiveNet [20] provides a set of tools and techniques for reconstructing complex dynamics of live sensor networks. In [21], [22], the authors use monitoring paths and cycles to localize single link and Shared Risk Link Group failures. Self-diagnosis [10] plants a finite state machine into each sensor node, enabling them to accordingly change the diagnosis state. Nevertheless, it proves difficult to achieve consensus between the nodes as each node can change the state whenever it receives the diagnosis requests.

Data fusion techniques are also related to this work. Koks and Challa [23] outlines the ideas of D-S theory and presents the basic D-S fusion equation. It also mentions that D-S theory becomes unavailable when the evidences are significantly conflicting with each other. The authors of [24], [25], [26] discuss how to change the combination rules to eliminate the impact of conflicting evidences, while [27], [28] claim that a better way is to modify the evidences, e.g., adding a basic confidence to describe the importance for each evidence.

![](images/67b8a93e3ea1858d608bdebf02f0e5aaccc9c9651285886ac242d319d5248443.jpg)



Fig. 2. The system framework of LD2.

# 3 SYSTEM FRAMEWORK

In this section, we introduce the general idea of our approach and show an overview of the system framework. As illustrated in Fig. 2, our main idea is to conduct the diagnosis process in a local area where abnormal symptoms are observed. Unlike the traditional sink-based approaches, innetwork diagnosis has following challenges. First, the diagnosis process is in a distributed manner, which means, all nodes in this neighborhood are required to be involved into the diagnosis task. To make the nodes be able to cooperate with each other, a feasible communication model for evidence delivery among the nodes must be well designed. The most naive design is to select a cluster head which collects all the state attributes from local nodes. Then some light-weight diagnosis algorithms can be leveraged to find out the root causes. Nevertheless, this way is proved unfeasible as we can hardly find such a diagnosis algorithm that it can be well planted in a resource-limited sensor node as well as performs good accuracy. Second, as mentioned above, to avoid putting all the workload of diagnosis on a certain sensor, the diagnosis process should be dividable so that we are able to let each node join in the diagnosis work but not just deliver their local information to others. Third, for one sensor, its original local information only includes the state attributes such as energy, MAC layer backoff, neighbor table, routing table, etc. There must be some algorithms for the nodes to refine those rough data, so as to generate some kinds of data for the fusion work.

The data-flow of LD2 is illustrated in Fig. 2. As we can see, the basic module applies a Naive Bayesian Model which encodes the probabilistic correlation between a set of state attributes and root causes. After the transition, we get basic probability assignment on the root causes. The module of diagnosis trigger determines whether some abnormal symptoms exist. If so, it needs to start a new diagnosis process. For example, if some local state values experience abnormal changes or some special events occur like a neighbor node has been removed from the neighbor for a long time, the trigger module motivates a new diagnosis process to check that whether this neighbor has crashed or not.

At the very beginning of a diagnosis process, a fusion tree rooted by this sensor node is established. Each node within this diagnosis area is involved in this tree. Actually the diagnosis process is divided into several operations of evidence fusion. Following this fusion tree, the diagnosis process is partly executed by the intermediate nodes. The evidence fusion module is based on D-S theory which is also known as the theory of belief functions. D-S theory is a generalization of the Bayesian theory of subjective probability. By combining the unique characters of WSNs, we design an improved approach by assigning basic confidence to the evidences according to their different significances for the fusion system.

After the root node finishing the fusion work, it has to decide whether it needs to send the diagnosis reports back to the sink according to the results. The diagnosis report at each node is handled by the report processor. The report processor caches each report for a certain period and delivers them to the sink eventually. We also deploy some sniffers in the network. In cases that current node doesn’t have a route to sink, it broadcasts the reports to the sniffer, thus the managers can manually fetch the results from the storage of sniffer.

At the sink side, there is a network management component which monitors the system performance such as packet delivery ratio and network traffic at real time. Sink can also trigger a local-diagnosis process when it detects performance degradation. With the diagnosis reports and selective state information obtained from the network, network managers can also conduct integrated fault analysis and provide recovery plans at the back-end. Many existing fault inference techniques can be applied to network diagnosis and our approach is complementary with these methods.

# 4 MAIN DESIGN

In this design, we consider both diagnosis efficiency and diagnosis accuracy. On the one hand, in order to avoid long distance evidence retrieval which leads to large communication overhead, we claim to carry out the diagnosis process locally but not at the back-end. On the other hand, to improve our diagnosis accuracy, we need to take judgements from all nodes within a local area into consideration, as one single node only has limited scope and computation ability. To make the nodes cooperate with each other to complete the diagnosis work, a series of interfaces and protocols need to be designed like in-node data processing, innetwork communication model. In the following sections, we show the design details of LD2.

# 4.1 Overview

Sink-based approaches retrieve state information from the network so as to conduct centralized analysis. They believe that a big picture of network is greatly helpful for network diagnosis, as many evidences can be leveraged to validate the diagnosis result. In CitySee, however, we observe that almost all the root causes can be partly reflected by the sensor nodes within a neighborhood. For example, if a sensor node has crashed, its neighbors must realize that it stops sending beacon messages for neighbor discovering. When a route loop occurs, by checking the network layer sequence number (e.g., CTP [29] sequence number), the nodes in the loop can realize that some packets are repeatedly forwarded. Locally diagnosing the network achieves real-time diagnosis, avoiding information lost on the collection path to the sink. At the same time, compared to one node, LD2 integrates more evidences to validate the result and thus achieves higher accuracy.

# 4.2 Diagnosis Trigger

Every diagnosis process is triggered by sensor nodes which detect abnormal symptoms based on their local evidences. We expect to design a light-weight detection approach for a resource-limited node. We believe that some abnormal symptoms take place only when a critical parameter experiences a sharp change. In this work, we find the most related parameters for each possible symptom. Once these parameters change more significantly than a threshold, the sensor nodes are reminded that some symptoms happen. We generate those threshold values by studying field cases in City-See. Generally, the threshold is set by intrinsic hardware conditions, running protocols and deployment configurations. For example, in CitySee we let each node broadcast a neighbor beacon every 512 ms in the period of initiating network topology. That is, if a node detects that one of its neighbors stops broadcasting beacons for 1 minute, i.e., about 120 beacons, it may crash already. Similarly, a route loop is likely to exist in the network if a node repeatedly forwards a packet; a radio performs abnormal if a node starts to run out of battery. Planting trigger model in sensor nodes encourages each node to observe the symptoms, so as to proactively diagnose the network.

# 4.3 Naive Bayesian Classifier

Considering the resource limitation of sensor nodes, fault detection within one single node should be achieved in energy efficient way and many existing models can be applied. For example, we can leverage simple rule-based models to make decision based on the local evidences. Light-weight probabilistic classifiers like the Naive Bayesian Classifier can also be applied. We use a binary variable R to denote each type of root cause and $P ( R )$ and $P ( \neg R )$ are the ð Þ ð: Þprobabilities that this failure occurs or not. This classifier is designed to guarantee that one network parameter is utilized to assess only one root cause. Then in a diagnosis process, sensor node is able to calculate the posterior probability of R given its local evidences, according to the Naive Bayesian model:

$$
P (R \mid F _ {1}, F _ {2}, \dots , F _ {n}) = \frac {1}{P (F _ {1} , F _ {2} , \dots , F _ {n})} P (R) \prod_ {i = 1} ^ {n} P (F _ {i} \mid R).
$$

Where $P ( F _ { 1 } , F _ { 2 } , \ldots , F _ { n } )$ is a scaling factor which only ð Þdepends on the evidences $( F _ { 1 } , F _ { 2 } , \ldots , { \bar { F } } _ { n } ) . ( F _ { 1 } , F _ { 2 } , \ldots , F _ { n } )$ ð Þ ð Þdenotes the metrics of current sensor node as well as its neighbors. During the training stage, we should estimate the value of $P ( R ) , P ( \neg R )$ and $P ( F _ { i } | R )$ . These parameter values ð Þ ð: Þ ð j Þcan be learned from the historical data. The storage cost of Naive Bayesian classifier is $( 1 + 2 n r )$ parameters for each ð þ Þfailure type where n denotes the number of metrics and each metric has r discrete values (Considering the computation capability of sensor nodes, we discretize the continuous metrics in this work to simplify the probability computation).

# 4.4 Evidence Fusion

How to make multiple nodes within a local area cooperate with each other to detect network failures is non-trivial. The main challenges are three-fold. First, communication about evidence transferring must use channel itself, which means, we have no out-of-band channel for diagnosis. If we incur a large amount of transmission overhead during the evidence fusion, new network failures may happen, which is also known as Heisenbug. Second, complicated fusion algorithms are not applicable for the system as a sensor node is resource limited. For the same reason, the algorithm should be dividable to avoid putting much data at one node. Third, the algorithm must ensure a local consensus to the final diagnosis report. Moreover, to achieve real-time diagnosis, the period of diagnosis process must be short.

# 4.4.1 Improved Dempster-Shafer Theory

D-S theory is a generalization of the Bayesian theory of subjective probability. It is based on two ideas: the idea of obtaining degrees of belief for one question from subjective probabilities for a related question, and Dempster’s rule for combining such degrees of belief when they are based on independent items of evidence.

Suppose $m _ { 1 }$ and $m _ { 2 }$ are two basic probability assignments $( \mathrm { i . e . , }$ , mass function) over the frame of discernment W . Intuitively, $m _ { i } ( U )$ describes the extent to which the evidence supports $U ,$ Þwhere $U \in { 2 ^ { W } } , i = 1 , 2$ . The fusion formula by D-S theory is:

$$
m _ {1 2} (X _ {i}) = \left\{ \begin{array}{l l} \frac {\sum_ {A _ {j} \wedge B _ {k} = X _ {i}} m _ {1} (A _ {j}) m _ {2} (B _ {k})}{1 - \sum_ {A _ {j} \wedge B _ {k} = \phi} m _ {1} (A _ {j}) m _ {2} (B _ {k})} & \text { if } X _ {i} \neq \phi , \\ 0 & \text { if } X _ {i} = \phi . \end{array} \right.
$$

Where $X _ { i } , A _ { j } , B _ { k } \in 2 ^ { W }$ .

$\begin{array} { r } { k _ { 1 2 } = \sum _ { A _ { j } \wedge B _ { k } = \phi } m _ { 1 } ( A _ { j } ) m _ { 2 } ( B _ { k } ) } \end{array}$ is called conflict factor of ¼ ^ ¼ ð Þ ð Þtwo evidences m and m . Notably, there can be two evidences $m _ { 1 }$ and $m _ { 2 }$ which are totally conflicting such that $k _ { 1 2 } = 1 .$ , therefore mass functions are not always combin-¼able. What is more, even if they are not totally conflicting but highly conflicting, that is, $k _ { 1 2 }  1$ , the combination !result always goes against the practical sense. In the network, some nodes may misbehave and then provide wrong evidences. Therefore, it is necessary to reduce the impact of those incorrect and fringe evidences. Many works are proposed to address this issue. In general, they can be classified into two types. One is to modify the combination rules, while the other one is to improve the evidence models.

The methods to modify the combination rules discuss two cases when the evidences are reliable and unreliable respectively. Nevertheless, they both mainly consider how to assign the conflicting evidence, like how to decide the ratio between the event possibilities when conflict happens. In [24], the authors propose that on the basis of reliable evidences, the main reason of conflict is the incompleteness in the frame of discernment, $\mathrm { i . e . , }$ some unknown event possibilities exist. The authors of [25], [26] all believe that not all the evidences are reliable. They propose that the conflicting part between the evidences should be discarded or reassigned to the other possibilities. In practice, when there are a large amount of evidences need to join in the fusion task, we hope that the evidences can be grouped by some metrics such that we can conduct the fusion task regardless of the fusion order to reduce the computation work. Unfortunately, above improved methods all fail to support associative law. This work fully combines the unique characters of WSNs, and designs following improved D-S theory for LD2.

Suppose the frame of discernment in our evidence model is $W \overset { \vartriangle } { = } \{ R _ { 0 } , R _ { 1 } , \ldots , R _ { n } \}$ . W consists of different root causes $\{ R _ { 1 } , R _ { 2 } , \ldots , R _ { n } \}$ gin the network. Besides, it also has a basic f gevent “no problem” $R _ { 0 } ,$ , which indicates that no exact diagnosis result is produced. We let each node $N _ { i }$ only generates possibility value $m _ { i } ( R _ { j } )$ for each single root cause $R _ { j }$ ð Þaccording to its own local information. That is, $m _ { i } ( U ) = { \bar { 0 } }$ for any $\breve { U } \in 2 ^ { W }$ and $\begin{array} { r } { | U | > 1 . \sum _ { 0 \leq j \leq n } m _ { i } ( R _ { j } ) = 1 } \end{array}$ .

Definition 1. The distance between $m _ { 1 }$ and m is:

$$
d (m _ {1}, m _ {2}) = \sqrt {\frac {1}{2} \left(M _ {1} - M _ {2}\right) ^ {T} \left(M _ {1} - M _ {2}\right)}.
$$

Where $M _ { i } = [ m _ { i } ( R _ { 0 } ) , m _ { i } ( R _ { 1 } ) , \ldots , m _ { i } ( R _ { n } ) ] ^ { T } , \quad i = 1 , 2 ,$ , and we also have $0 \leq d ( m _ { 1 } , m _ { 2 } ) \leq 1 ;$ :

$$
\begin{array}{l} d (m _ {1}, m _ {2}) = \sqrt {\frac {1}{2} \sum_ {0 \leq j \leq n} \left(m _ {1} (R _ {j}) - m _ {2} (R _ {j})\right) ^ {2}} \\ = \sqrt {\frac {1}{2} \sum_ {0 \leq j \leq n} \left(m _ {1} ^ {2} (R _ {j}) + m _ {2} ^ {2} (R _ {j}) - 2 m _ {1} (R _ {j}) m _ {2} (R _ {j})\right)} \\ \leq \sqrt {\frac {1}{2} \sum_ {0 \leq j \leq n} \left(m _ {1} ^ {2} (R _ {j}) + m _ {2} ^ {2} (R _ {j})\right)} \\ \leq \sqrt {\frac {1}{2} \left[ \left(\sum_ {0 \leq j \leq n} m _ {1} (R _ {j})\right) ^ {2} + \left(\sum_ {0 \leq j \leq n} m _ {2} (R _ {j})\right) ^ {2} \right]} = 1. \\ \end{array}
$$

Definition 2. The similar degree of $m _ { 1 }$ and m2 is:

$$
s (m _ {1}, m _ {2}) = 1 - d (m _ {1}, m _ {2}).
$$

As we can see, the greater similar degree of $m _ { 1 }$ and $m _ { 2 } ,$ , the more similar analysis two evidences describe. If we have one evidence which is similar to all the others, then we believe that this evidence is important. Suppose we have N evidences $e _ { 1 } , e _ { 2 } , \ldots , e _ { N }$ , and their corresponding basic probability assignments are $m _ { 1 } , m _ { 2 } , \ldots , m _ { N }$ .

Definition 3. The basic confidence of $e _ { i } ( i = 1 , 2 , \dots , N )$ is:

$$
\beta_ {i} = \sum_ {1 \leq j \leq N, j \neq i} s (m _ {i}, m _ {j}).
$$

To avoid huge computation cost, sometimes we can also randomly sample some evidences to compose a standard set $S ,$ hence every evidence $m _ { i }$ computes the total similar degree to S as its basic confidence: $\begin{array} { r } { \beta _ { i } = \sum _ { s _ { i } \in S , m _ { i } \ne s _ { i } } s ( m _ { i } , s _ { j } ) } \end{array}$ .

¼ j2 i6¼ j ðAfter normalization, we get the relative importance of $m _ { i }$ to the evidence which has the greatest basic confidence: $\psi _ { i } = \beta _ { i } / \mathrm { m a x } _ { 1 \leq j \leq N } \beta _ { j }$ . The normalization could be omitted ¼  when the fusion task is divided into small ones and a global maximum value is unknown, i.e., $\psi _ { i } = \beta _ { i }$ . Then we transfer ¼the basic probability assignments by multiplying the basic confidence, making them of equal importance in new fusion system:

$$
m _ {i} ^ {\prime} (R _ {j}) = \psi_ {i} m _ {i} (R _ {j}) \quad \forall 1 \leq j \leq n,
$$

$$
m _ {i} ^ {\prime} (R _ {0}) = \psi_ {i} m _ {i} (R _ {0}) + (1 - \psi_ {i}).
$$

Notably, if there are only two evidences involved in the fusion task. Because $s ( m _ { i } , m _ { j } ) = s ( m _ { j } , m _ { i } )$ , they have the ð Þ ¼ ð Þsame basic confidence even if one of them provides inaccurate evidence. To address this issue, we need to set a threshold $F _ { t }$ such that more than $F _ { t }$ evidences are allowed to utilize Definition 3 to conduct evidence fusion. In our implementation, we set $F _ { t }$ equals 4.

In this new fusion system, for $R _ { i } \ ( i = 1 , 2 , \ldots , n )$ , we ¼reduce the impact of those evidences with less importance. That is, to confirm whether $R _ { i }$ happens or not mainly relies on the other evidences. On the contrary, for $R _ { 0 }$ we increase the impact of those evidences with less importance, so as to average the confidence to the other root causes. After transferring the basic probability assignments, all the evidences are of equal importance, then we can utilize D-S theory to conduct evidence fusion. Our improved D-S theory is designed for LD2’s evidence model. We choose not to change the combination rules but refine the evidences. It also satisfies that the fusion result keeps the same even if we change the fusion order, i.e., supports associative law. It is very important for our design, as we can’t ensure that the fusion tree has the same architecture all the time (details in section Fusion Algorithm).

Theorem 1. $m _ { ( 1 2 ) 3 } ^ { \prime } ( X _ { i } ) = m _ { 1 ( 2 3 ) } ^ { \prime } ( X _ { i } )$ .

Proof.

$$
\begin{array}{l} m _ {(1 2) 3} ^ {\prime} (X _ {i}) = \frac {\sum_ {A _ {j} \wedge B _ {k} = X _ {i}} m _ {1 2} ^ {\prime} (A _ {j}) m _ {3} ^ {\prime} (B _ {k})}{1 - \sum_ {A _ {j} \wedge B _ {k} = \phi} m _ {1 2} ^ {\prime} (A _ {j}) m _ {3} ^ {\prime} (B _ {k})} \\ = \frac {\sum_ {A _ {j} \wedge B _ {k} = X _ {i}} \left(\frac {\sum_ {C _ {l} \wedge D _ {t} = A _ {j}} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t})}{1 - \sum_ {C _ {l} \wedge D _ {t} = \phi} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t})}\right) m _ {3} ^ {\prime} (B _ {k})}{1 - \sum_ {A _ {j} \wedge B _ {k} = \phi} \left(\frac {\sum_ {C _ {l} \wedge D _ {t} = A _ {j}} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t})}{1 - \sum_ {C _ {l} \wedge D _ {t} = \phi} m _ {1} ^ {\prime} (C _ {l}) m _ {3} ^ {\prime} (D _ {t})}\right) m _ {3} ^ {\prime} (B _ {k})} \\ = \frac {\sum_ {A _ {j} \wedge B _ {k} = X _ {i}} \left(\frac {\sum_ {C _ {l} \wedge D _ {t} = A _ {j}} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t})}{1 - \sum_ {C _ {l} \wedge D _ {t} = \phi} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t})}\right) m _ {3} ^ {\prime} (B _ {k})}{\sum_ {A _ {j} \wedge B _ {k} \neq \phi} \left(\frac {\sum_ {C _ {l} \wedge D _ {t} = A _ {j}} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t})}{1 - \sum_ {C _ {l} \wedge D _ {t} = \phi} m _ {1} ^ {\prime} (C _ {l}) m _ {1} ^ {\prime} (D _ {t})}\right) m _ {3} ^ {\prime} (B _ {k})} \\ = \frac {\sum_ {C _ {l} \wedge D _ {t} \wedge B _ {k} = X _ {i}} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t}) m _ {3} ^ {\prime} (B _ {k})}{\sum_ {C _ {l} \wedge D _ {t} \wedge B _ {k} \neq \phi} m _ {1} ^ {\prime} (C _ {l}) m _ {2} ^ {\prime} (D _ {t}) m _ {3} ^ {\prime} (B _ {k})} \\ \end{array}
$$

Similarly, we can prove that:

$$
\begin{array}{l} m _ {1 (2 3)} ^ {\prime} \left(X _ {i}\right) = \frac {\sum_ {C _ {l} \wedge D _ {t} \wedge B _ {k} = X _ {i}} m _ {1} ^ {\prime} \left(C _ {l}\right) m _ {2} ^ {\prime} \left(D _ {t}\right) m _ {3} ^ {\prime} \left(B _ {k}\right)}{\sum_ {C _ {l} \wedge D _ {t} \wedge B _ {k} \neq \phi} m _ {1} ^ {\prime} \left(C _ {l}\right) m _ {2} ^ {\prime} \left(D _ {t}\right) m _ {3} ^ {\prime} \left(B _ {k}\right)} \\ = m _ {(1 2) 3} ^ {\prime} (X _ {i}). \\ \end{array}
$$

# 4.4.2 Fusion Algorithm (Algorithm 1)

In this part we present our specific algorithms for evidence fusion. First we introduce the fusion tree. Every diagnosis process is rooted by a node (as shown in Fig. 3), which detects abnormal network symptoms such as node crash, traffic contention, route loop and so on. It triggers a diagnosis model as well as determines the diagnosis area, then broadcasts diagnosis request beacons (DREQ) to establish the fusion tree. Basically we need to determine the diagnosis area for each symptom. For example, to find out whether a node has crashed or not can ask for one-hop neighbors’ evidences, while to find out whether a route loop exists or not should visit all the nodes transmitting the relevant packets. All the information must be involved in DREQ for the nodes to know about the details of diagnosis task. To the other nodes, after receiving DREQ, they are involved in the fusion tree if they locate in the diagnosis area. Once they join in the fusion tree, they should keep broadcasting DREQ to inform other related nodes. In the process of constructing fusion tree, each node records its parent node and child nodes for following evidence collection.

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

Notably, in the process of establishing fusion tree, the root also needs to sample a standard set for following evidence fusion. As mentioned above, utilizing standard set can reduce the computation cost. Besides, in our fusion system, it greatly reduces the transmission overhead as we have no need to collect all the evidences to assign a global basic

![](images/551c3e748d6426462d0d9a2b9a25e1e6b1c1503537a12fc12ae17cbbe0f01936.jpg)



Fig. 3. Fusion tree establishment from root node.

confidence. In LD2, we make the standard set consist of the evidences from the root node and its direct child nodes. Every DREQ packet contains standard set such that each node in the fusion tree is able to calculate its own basic confidence respectively.

The establishment of fusion tree finishes until no DREQ is transmitted. What follows is the evidence fusion process (Algorithm 2, 3). First all the leaf nodes send out a leafquery beacon (LQUE) to make sure that it indeed has no child node in the fusion tree. Actually LQUE is used to make up the lost DREQ. If there is no reply to the LQUE, it transfers its local evidence (DEVI) to its parent node in the tree (as shown in Fig. 4). Otherwise it updates its child set and waits for the evidences from the child nodes. To the intermediate nodes, they must collect all the evidences from its child nodes and finally sends the fusion result to its parent node. To avoid evidence lost, each intermediate node is able to “remind” its child nodes by broadcasting childquery beacons (CQUE), hence the lost evidences can be retransmitted.

Algorithm 2 Evidence Fusion Algorithm   
1: if $S_{children}$ is empty (leaf node) then
2: Broadcast leaf-query beacon (LQUE) to ensure that it is a leaf node.
3: if No reply to LQUE then
4: Transmit local evidence (DEVI) to its parent.
5: else
6: Update the child set $S_{children}$ .
7: end if
8: else
9: Collect_and_Fusion
10: end if
11: if Receive LQUE then
12: Check the source ID of this LQUE, denoted as p.
13: if p = parentID then
14: Reply to this LQUE.
15: end if
16: end if
17: if Receive CQUE then
18: Transmit local DEVI.
19: end if

![](images/494294ac87da19292ae9607ee5f710cbcfb3c7b1f79c075cab2ed5d50e1495f7.jpg)



Fig. 4. Evidence fusion from leaf nodes.

Algorithm 3 Collect\_and\_Fusion   
1: Maintain an evidence set $S_{evidence}$ to record the received evidences from the child nodes.
2: Add local evidence into $S_{evidence}$ .
3: while Receive DEVI do
4: Add this DEVI into $S_{evidence}$ .
5: end while
6: for each $Child_{i}$ in $S_{children}$ do
7: if $S_{evidence}$ does not contain the DEVI from $Child_{i}$ then
8: Transmit child-query beacon (CQUE) to $Child_{i}$ .
9: end if
10: end for
11: if Has Collected all the evidences from child nodes then
12: Evidence Fusion.
13: Transmit $S_{evidence}$ to parent node.
14: end if

As we can see, the structure of fusion tree has much dynamics as we connect the nodes by broadcasting DREQ. What is more, the fusion order strictly follows the fusion tree from leaf nodes to the root node. Fortunately, in Theorem 1 it proves that the fusion result of LD2 keeps consistent, regardless of the fusion order. That means, when network topology changes, the diagnosis area automatically changes, the related nodes will be required to provide evidences. This character helps our fusion system greatly reduce the maintenance overhead of fusion tree, as well as enable to ignore the impact of network topology.

# 5 EVALUATION

We evaluate LD2 through a real indoor testbed consisting of 50 TelosB motes. Two metrics are mainly used for evaluating LD2’s accuracy: false negative rate (i.e., miss detection rate) and false positive rate (i.e., false alarm rate). False negative rate is defined as the proportion of faulty cases which are detected as normal, while false positive rate is defined as the proportion of normal cases which are detected as faulty.

Basically we implement a CTP application in the network, for the analysis of impact with different diagnosis approaches. In this work, we implement two modules for diagnosing the network: LD2 and TinyD2. TinyD2 presents

![](images/7bc364408c49aba4d2599013c00814170524852a939ae6b774d7362ec62015bc.jpg)



(a) Network Topology with 50 nodes   
![](images/a9492552dbbbcdfde222aa7ce6bd87cb56d09873c453d7d4b01b5769f1f9c31a.jpg)  
(b)36%

![](images/7b8d7ef7caa1db4d3db315c2359e2580dc131116d5848269c17a47785f56b9e4.jpg)  
(c)31%

![](images/4e7c838b8bef2ee3fb4a8d3f891f3c1a90a755c38aa13290e0071b1465054135.jpg)  
(d) 18%

![](images/153fdc77338b854b25bd907dc9b3b066f6686783c2cdf8e9da2017766ee880f2.jpg)  
(e) 9%   
Fig. 5. Testbed topology. We inject three failures in (a) respectively, making their diagnosis area the same: node 25 (red mote) is crashed; traffic contention occurs at node 25; a route loop (blue arrows) exists among node 25’s neighbors (green motes). Besides, we let node 13 (i.e., the blue mote in (b), (c), (d), (e)) trigger the diagnosis process. The tree structure of (b), (c), (d) and (e) respectively occurs 36, 31, 18 and 9 percent in all the cases.

the concept of self-diagnosis which encourages each sensor node to run a embedded finite state machine to find out the root cause. During the tests, we manually inject three types of failures: node crash, traffic contention and the route loop. For each failure, we conduct 60 cases. We also change the power level to discuss the performance of two approaches in different diagnosis densities (i.e., the number of neighbor nodes).

# 5.1 Implementation

We implement LD2 based on TinyOS 2.1. Besides the trigger component and Naive Bayesian Classifier, the LD2 module provides two interfaces: FTree and EFusion. FTree is used to establish fusion tree, while EFusion implements the core computation of evidence fusion. In FTree, the two commands insertChild and removeChild are used to manage the child set. The command sendBeacon(addr, msg, len) (parameter addr means node address, msg is the packet, len is the packet length) is called to broadcast the beacons while the event beaconReceive is signaled when the beacon is received. Command sample is for sampling evidences. In EFusion, command fusion is used to conduct evidence fusion, while insertDEVI and remove-DEVI are used to manage the evidences collected. After we add this module to a benchmark CTP application, the ROM cost increases to 26,369 bytes from 20,442 bytes, which indicates LD2 module consumes approximately 5.8 KB ROM, which is acceptable compared to 48 KB ROM in TelosB.

![](images/d45a7be3b875146993b63f3bcc599201b1aeaec2c2cc291702a2c006caf92e4a.jpg)



Fig. 6. Time cost of sampling evidences and establishing fusion tree.

![](images/72fc396d568c1113e6dbca10bb6529a2d417d30cd5e22b3f72ac8fc4f707e24d.jpg)



Fig. 7. CDF of evidence fusion’s time cost.

# 5.2 Time Cost

Fig. 5a illustrates the network topology of our testbed consisting of 50 motes. First we discuss the time cost during the diagnosis process. Generally we divide the cost into two parts: fusion tree establishment and evidence fusion process. As mentioned in Section 4, the fusion tree is related to the diagnosis area which is determined by the symptoms. In the experiments, we make above three network failures have the same diagnosis area. Node 25 (i.e., the red mote) has 16 neighbors (i.e., the green motes). When node 25 crashes or traffic contention occurs at node 25, the diagnosis area involves all its neighbors. Besides, we let a routing loop exist among all these neighbors (i.e., the blue arrows). That is, their diagnosis area is the neighbors of node 25. We also make node 13 as the root node of fusion tree.

Figs. 5b, 5c, 5d and 5e describe four of most frequent structures when we are establishing the fusion tree. Fig. 6 shows the time cost of sampling evidences and establishing fusion tree. As mentioned in Section 4, the process of sampling evidences is used to assign a local basic confidence to each node in evidence fusion, while establishing fusion tree mainly includes broadcasting and receiving beacons. As we can see, the time cost is stable for all the tree structures, i.e., about 19 ms in sampling evidences and 39 ms in establishing fusion tree. Fig. 7 shows the CDF of the time cost of evidence fusion in three diagnosis processes. In 80 percent of cases for detecting node crash, LD2 finishes evidence fusion in a 16-node area within 95 ms. For traffic contention, it costs more than 133 ms for 60 percent of cases as the DEVI packet contains three possible root causes (i.e., ingress overflow, egress overflow, bad link) thus more combination work is needed. Fig. 8 depicts the CDF of the total time cost for diagnosing node crash, traffic contention and route loop respectively. We observe similar trends in two CDF figures as the process of evidence fusion costs most of time in LD2.

![](images/436fcf80a6d30eedf88e8848c036b530e07506f4d48368a71e2974ea4ebeabee.jpg)



Fig. 8. CDF of total time cost.

In Table 1, we compare LD2 with TinyD2 [10] and Sympathy [5] on the time cost from beginning collecting network evidence till generating diagnosis report at the backend. For three kinds of network failures, we conduct four experiments. For detecting node crash, LD2 costs 1.95 s while Sympathy needs 4.86 s, it is because even for a simple network fault, Sympathy collects a large amount network information from all the nodes. These experiments run in the testbed. When the network scales, the difference will be more obvious.

# 5.3 Diagnosis Accuracy

Figs. 9 14 illustrate the diagnosis results of detecting node crash, traffic contention and route loop with LD2 and TinyD2 respectively. According to Fig. 9, LD2 enables to troubleshoot more than 92 percent of crashed nodes, and the false negative rate decreases when the number of neighbors increases. It is well understood that once a node is crashed, its neighbor must find that it is removed from the neighbor tables for a long period. Therefore, the more neighbors, the more determinate diagnosis. As showed in Fig. 12, the false positive rate of LD2 is around 12 percent over varying diagnosis densities. For detecting route loop, each node produces its evidence by checking the CTP sequence number. As illustrated in Fig. 11 and 14, LD2 indeed maintains low false negative rate and false positive rate, i.e., 5 and 6 percent, which means that LD2 can successfully explore about 95 percent of route loops. By contrast, TinyD2 performs unstable to detect crashed nodes and route loops under different diagnosis densities. When the density increases, TinyD2 often fails to achieve a consensus among the nodes, such that hardly determines a root cause.

TABLE 1 The Total Time Cost (Second) from Beginning Collecting Network Evidence Till Generating Diagnosis Report at the Back-End 

<table><tr><td></td><td>#11</td><td>#12</td><td>#13</td><td>#14</td><td>mean</td><td>#21</td><td>#22</td><td>#23</td><td>#24</td><td>mean</td><td>#31</td><td>#32</td><td>#33</td><td>#34</td><td>mean</td></tr><tr><td>Sympathy</td><td>5.02</td><td>4.83</td><td>4.93</td><td>4.67</td><td>4.86</td><td>5.32</td><td>5.03</td><td>5.12</td><td>4.87</td><td>5.09</td><td>5.90</td><td>5.51</td><td>5.67</td><td>5.70</td><td>5.70</td></tr><tr><td>TinyD2</td><td>2.78</td><td>2.50</td><td>2.54</td><td>2.35</td><td>2.54</td><td>2.78</td><td>2.89</td><td>2.87</td><td>2.83</td><td>2.84</td><td>3.23</td><td>3.18</td><td>3.15</td><td>3.05</td><td>3.15</td></tr><tr><td>LD2</td><td>1.87</td><td>1.93</td><td>2.21</td><td>1.80</td><td>1.95</td><td>2.87</td><td>3.06</td><td>3.03</td><td>2.77</td><td>2.93</td><td>1.92</td><td>2.11</td><td>1.87</td><td>2.01</td><td>1.97</td></tr></table>

#11  #14 are for node crash, #21  #24 are for network contention, #31  #34 are for route loop.

![](images/2be1d492f4eb5697516438483e41ccff5739ce49614339ec28de931917eba6e2.jpg)



Fig. 9. False negative rate for node crash.

![](images/51ba98f16bb93667487902122ffb326807c339d21cc854b85292c463ab2423a2.jpg)



Fig. 12. False positive rate for node crash.

![](images/bdd30206069614a9dfe7c09a8b7a854397f60d4033720fa9fa189473c115c76d.jpg)



Fig. 10. False negative rate for traffic contention.

![](images/70e9ca4eccb97430e94ef0d7133292dfec2c561fd88bcefd45a611ef16961457.jpg)



Fig. 13. False positive rate for traffic contention.

![](images/f264cda2e5b3c1a441f14e38d3c34ac4dcedc3f2e34d12c5b9accec25d4c61ed.jpg)



Fig. 11. False negative rate for route loop.

![](images/5ab6701da9e31b721ab1ddb8c95bf44681a43f7d1424ba51bbba0767512c86fb.jpg)



Fig. 14. False positive rate for route loop.

According to Fig. 10, LD2 correctly explores about 86 percent of traffic contention, while TinyD2 is able to find out 78 percent of cases when the number of neighbors is 16. Traffic contention occurs due to some reasons, such as egress overflow, ingress overflow and bad link. It proves difficult for TinyD2 to use finite state machine to achieve an accept state. In Fig. 13, as we can see, TinyD2’s false positive rate increases to 22 percent when the number of neighbors is 16, while LD maintains around 16 percent under different diagnosis densities. In Fig. 15, we investigate the case when multiple diagnosis processes are running. Three failures are injected into the networks with different density. As we can see, more than 80 percent of faults are correctly detected, and the results keep consistent with that when only one network failure exists.

![](images/e1127494d00a2c43ce3d46ca1744bf5915d84b8e6accbaf3a9678051a1fd7da0.jpg)



Fig. 15. The detection rate when conducting three diagnosis processes simultaneously.

# 5.4 Coupling Effect with Application

Finally we discuss the coupling effect between the application and network diagnosis. We observe that most of sink-based approaches needs to retrieve more network information than that generated by the application. It proves unreasonable because some network failures such as traffic contention, bad routing, can occur due to frequent large-amount collection. In CitySee, we implement Sympathy [5]. However, the network yield performs very unstably (see Fig. 17), because too much network resources are required by Sympathy.

TinyD2 reduces the transmission overhead by broadcasting fault detector in the air. In practice, however, it lacks of a specific order to control the diagnosis and ensure a consensus result. What is more, once it can’t achieve the accept state, much extra transmissions are required. In fact, when we utilize TinyD2 to conduct the diagnosis process in the local area around timeline 30,000, 40,000 and 50,000 ms, most application packets will be lost. The main reason must be channel resource is shared by other packet transmissions. To find out the root cause, we also sniffer the beacons in this area. As illustrated by Fig. 16, in the diagnosis process, every node in TinyD2 generates about 28 beacons within 200 ms, which probably causes a local traffic contention. By contrast, the root node and intermediate nodes in LD2 only cause about 15 and 10 beacons in 200 ms. The leaf node costs only 8.2 beacons in average, it is because they are at the bottom of fusion tree, some beacons in communication with child nodes are unnecessary.

![](images/14928b25184eb919d37cbc2af1c1e89c11e06a41ee74856aa95d20c4932991b6.jpg)



Fig. 16. Beacon transmissions in diagnosis process.

![](images/c0442d6d99a1b2e16d6cf3cea64d607ffd4e22302a4251a2f272856e6e7de3ee.jpg)



Fig. 17. Network yield while running Sympathy.

# 6 CONCLUSION

Long distance proactive information retrieval in traditional sink-based approaches to diagnosing WSNs often incurs a large amount of transmission overhead. What is more, sink-based approaches cannot afford real-time diagnosis. Conversely, sensor nodes have the first-hand evidences to conduct diagnosis process, but due to the narrow scope of system state information, diagnosis results from single nodes are generally inaccurate. To balance this tradeoff, this work presents LD2, which conducts the diagnosis process in a local area. LD2 claims to distribute the diagnosis workload to the sensor nodes within a diagnosis area. By constructing a fusion tree, each node summarizes the evidences of its child nodes, such that the contribution of each node converges on the root node. Thus, a local consensus to the final diagnosis report is generated and reported to the sink. We also implement LD2 on TinyOS 2.1 and evaluate the performance on a real indoor testbed consisting of 50 nodes.

# ACKNOWLEDGMENTS

This research was supported in part by the NSFC Distinguished Young Scholars Program under Grant No. 61125202, and the NSFC under Grant No. 61103187.

# REFERENCES

[1] J. Kong, J. Cui, D. Wu, and M. Gerla, “Building underwater ad-hoc networks and sensor networks for large scale real-time aquatic applications,” in Proc. IEEE Military Commun. Conf., Atlantic City, NJ, USA, 2005, pp. 1535–1541.   
[2] N. Xu, S. Rangwala, K. Chintalapudi, D. Ganesan, A. Broad, R. Govindan, and D. Estrin, “A wireless sensor network for structural monitoring,” in Proc. 2nd Int. Conf. Embedded Netw. Sens. Syst., Baltimore, MD, USA, 2004, pp. 13–24.   
[3] K. Xing, F. Liu, X. Cheng, and D. Du, “Real-time detection of clone attacks in wireless sensor networks,” in Proc. IEEE 28th Int. Conf. Distrib. Comput. Syst., Beijing, China, 2008, pp. 3–10.   
[4] E. Magistretti, O. Gurewitz, and E. Knightly, “Inferring and mitigating a link’s hindering transmissions in managed 802.11 wireless networks,” in Proc. 16th Annu. Int. Conf. Mobile Comput. Netw., Chicago, IL, USA, 2010, pp. 305–316.

[5] N. Ramanathan, K. Chang, R. Kapur, L. Girod, E. Kohler, and D. Estrin, “Sympathy for the sensor network debugger,” in Proc. 3rd Int. Conf. Embedded Netw. Sensor Syst., San Diego, CA, USA, 2005, pp. 255–267.   
[6] X. Wang, L. Fu, and C. Hu, “Multicast performance with hierarchical cooperation,” IEEE/ACM Trans. Netw., vol. 20, no. 3, pp. 917–930, Jun. 2012.   
[7] S. Liu, G. Xing, H. Zhang, J. Wang, J. Huang, M. Sha, and L. Huang, “Passive interference measurement in wireless sensor networks,” in Proc. IEEE 18th Int. Conf. Netw. Protocols, Kyoto, Japan, 2010, pp. 52–61.   
[8] R. Tan, G. Xing, Z. Yuan, X. Liu, and J. Yao, “System-level calibration for fusion-based wireless sensor networks,” in Proc. IEEE Real-Time Syst. Symp., San Diego, CA, USA, 2010, pp. 215–224.   
[9] Z. Li, Y. Liu, M. Li, J. Wang, and Z. Cao, “Exploiting ubiquitous data collection for mobile users in wireless sensor networks,” IEEE Trans. Parallel Distrib. Syst., vol. 24, no. 2, pp. 312–326, Feb. 2013.   
[10] K. Liu, Q. Ma, X. Zhao, and Y. Liu, “Self-diagnosis for large scale wireless sensor networks,” in Proc. IEEE Conf. Comput. Commun., Shanghai, China, 2011, pp. 1539–1547.   
[11] L. Girod, J. Elson, A. Cerpa, T. Stathopoulos, N. Ramanathan, and D. Estrin, “Emstar: A software environment for developing and deploying wireless sensor networks,” in Proc. USENIX Annu. Tech. Conf., Boston, MA, USA, 2004, pp. 283–296.   
[12] Y. Liu, K. Liu, and M. Li, “Passive diagnosis for wireless sensor networks,” IEEE/ACM Trans. Netw., vol. 18, no. 4, pp. 1132–1144, Aug. 2010.   
[13] J. Yang, M. Soffa, L. Selavo, and K. Whitehouse, “Clairvoyant: A comprehensive source-level debugger for wireless sensor networks,” in Proc. 5th Int. Conf. Embedded Netw. Sensor Syst., Sydney, Australia, 2007, pp. 189–203.   
[14] Q. Cao, T. Abdelzaher, J. Stankovic, K. Whitehouse, and L. Luo, “Declarative tracepoints: A programmable and application independent debugging system for wireless sensor networks,” in Proc. 6th ACM Conf. Embedded Netw. Sensor Syst., Raleigh, NC, USA, 2008, pp. 85–98.   
[15] L. Luo, T. He, G. Zhou, L. Gu, T. Abdelzaher, and J. Stankovic, “Achieving repeatability of asynchronous events in wireless sensor networks with envirolog,” in Proc. IEEE Conf. Comput. Commun., Barcelona, Catalunya, Spain, 2006, pp. 1–14.   
[16] T. Sookoor, T. Hnat, P. Hooimeijer, W. Weimer, and K. Whitehouse, “Macrodebugging: Global views of distributed program execution,” in Proc. 7th ACM Conf. Embedded Netw. Sensor Syst., Berkeley, CA, USA, 2009, pp. 141–154.   
[17] S. Guo, Z. Zhong, and T. He, “Find: Faulty node detection for wireless sensor networks,” in Proc. 7th ACM Conf. Embedded Netw. Sensor Syst., Berkeley, CA, USA, 2009, pp. 253–266.   
[18] X. Miao, K. Liu, Y. He, D. Papadias, Q. Ma, and Y. Liu, “Agnostic diagnosis: Discovering silent failures in wireless sensor networks,” IEEE Trans. Wireless Commun., vol. 12, no. 12, pp. 6067–6075, Dec. 2013.   
[19] A. Woo, T. Tong, and D. Culler, “Taming the underlying challenges of reliable multihop routing in sensor networks,” in Proc. 1st Int. Conf. Embedded Netw. Sensor Syst., Los Angeles, CA, USA, 2003, pp. 14–27.   
[20] B. Chen, G. Peterson, G. Mainland, and M. Welsh, “Livenet: Using passive monitoring to reconstruct sensor network dynamics,” in Proc. 4th IEEE Int. Conf. Distrib. Comput. Sensor Syst., Santorini Island, Greece, 2008, pp. 79–98.   
[21] S. Ahuja, S. Ramasubramanian, and M. Krunz, “Single-link failure detection in all-optical networks using monitoring cycles and paths,” IEEE/ACM Trans. Netw., vol. 17, no. 4, pp. 1080–1093, Aug. 2009.   
[22] S. Ahuja, S. Ramasubramanian, and M. Krunz, “SRLG failure localization in all-optical networks using monitoring cycles and paths,” in Proc. IEEE 27th Conf. Comput. Commun., Phoenix, AZ, USA, 2008, pp. 700–708.   
[23] D. Koks and S. Challa, “An introduction to Bayesian and Dempster-Shafer data fusion,” Australian Dept. Defence Sci. Technol. Organisation, Canberra, Australia, Tech. Rep. DSTOTR1436, 2003.   
[24] P. Smets, “The combination of evidence in the transferable belief model,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 12, no. 5, pp. 447–458, May 1990.   
[25] R. Yager, “On the Dempster-Shafer framework and new combination rules,” Inf. Sci., vol. 41, no. 2, pp. 93–137, 1987.

[26] E. Lefevre, O. Colot, P. Vannoorenberghe, and D. De Brucq, “A generic framework for resolving the conflict in the combination of belief structures,” in Proc. Int. Conf. Inf. Fusion, Paris, France, 2000, pp. MOD4/11–MOD4/18.   
[27] R. Haenni, “Are alternatives to Dempster’s rule of combination alternatives? comments on ‘about the belief combination and the conflict management problem’,” Int. J. Inf. Fusion, vol. 3, no. 3, pp. 237–241, 2002.   
[28] C. Murphy, “Combining belief functions when evidence conflicts,” Decision Support Syst., vol. 29, no. 1, pp. 1–9, 2000.   
[29] O. Gnawali, R. Fonseca, K. Jamieson, D. Moss, and P. Levis, “Collection tree protocol,” in Proc. 7th ACM Conf. Embedded Network. Sensor Syst., 2009, pp. 90–100.

![](images/84e199b496a0bdb7371c5dd6641fc9e160b07fbfc4c20bff24d492266fa9db36.jpg)



Qiang Ma received the BS degree from the Department of Computer Science and Technology from Tsinghua University, China, in 2009, and the PhD degree from the Department of Computer Science and Engineering at the Hong Kong University of Science and Technology in 2013. He is currently a postdoc researcher in the School of Software, Tsinghua University, China. His research interests include sensor networks, network diagnosis, and management and mobile computing. He is a member of the IEEE.

![](images/505ee2760ffcf2df40dbab51bae9c3d4f0d1c12b1bd6128f01e3184d72363225.jpg)



Kebin Liu received the BS degree from the Department of Computer Science from Tongji University, in 2004, and the MS and PhD degrees from the Department of Computer Science and Engineering, Shanghai Jiaotong University, in 2007 and 2010, respectively. He is currently an assistant researcher in the School of Software and TNLIST, Tsinghua University. His research interests include sensor networks and distributed systems. He is a member of the IEEE.

![](images/29d11805c9974b30576eea2f6ef9fca8b59412d04b4051eda09f70e1533f9598.jpg)



Xin Miao received the BS degree from the Department of Computer Science and Technology from Tsinghua University, China, in 2005, and the PhD degree from the Department of Computer Science and Engineering, the Hong Kong University of Science and Technology in 2013. He is currently a postdoc researcher in the School of Software, Tsinghua University, China. His research interests include sensor networks and RFID. He is a member of the IEEE.

![](images/dac451ecc1a9a97bac79e0f5b4afdf5a5fddf0ca1040caed0c4d85ff2969d2bd.jpg)



Yunhao Liu received the BS degree from Automation Department, Tsinghua University, China, in 1995, and the MS and PhD degrees from the Department of Computer Science and Engineering at Michigan State University in 2003 and 2004, respectively. He is currently Chang Jiang professor and the dean of School of Software, Tsinghua University, China. He is a senior member of the IEEE.

" For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.