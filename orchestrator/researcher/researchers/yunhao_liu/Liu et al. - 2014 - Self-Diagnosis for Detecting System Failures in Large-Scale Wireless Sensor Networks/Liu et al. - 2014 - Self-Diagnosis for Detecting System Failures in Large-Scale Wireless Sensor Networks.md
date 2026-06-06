# Self-Diagnosis for Detecting System Failures in Large-Scale Wireless Sensor Networks

Kebin Liu, Member, IEEE, Qiang Ma, Wei Gong, Xin Miao, and Yunhao Liu, Member, IEEE

Abstract—Existing approaches to diagnosing sensor networks are generally sink based, which rely on actively pulling state information from sensor nodes so as to conduct centralized analysis. First, sink-based tools incur huge communication overhead to the traffic-sensitive sensor networks. Second, due to the unreliable wireless communications, sink often obtains incomplete and suspicious information, leading to inaccurate judgments. Even worse, it is always more difficult to obtain state information from problematic or critical regions. To address the given issues, we present a novel self-diagnosis approach, which encourages each single sensor to join the fault decision process. We design a series of fault detectors through which multiple nodes can cooperate with each other in a diagnosis task. Fault detectors encode the diagnosis process to state transitions. Each sensor can participate in the diagnosis by transiting the detector’s current state to a new state based on local evidences and then passing the detector to other nodes. Having sufficient evidences, the fault detector achieves the Accept state and outputs a final diagnosis report. We examine the performance of our self-diagnosis tool called TinyD2 on a 100-node indoor testbed and conduct field studies in the GreenOrbs system, which is an operational sensor network with 330 nodes outdoor.

Index Terms—Self-diagnosis, wireless sensor networks (WSNs), network diagnosis.

# I. INTRODUCTION

W IRELESS sensor networks (WSNs) that enable manysurveillance applications [6], [11], [25], [27] usually surveillance applications [6],[11],[25],[27] usually consist of a large number of sensor nodes deployed in the wild. Accurate and real-time fault diagnosis is of great significance for ensuring the system functionality and reliability. A few faulty nodes can heavily degrade the system performance [12] and shorten the network lifetime. Nevertheless, diagnosis for a large scale and in-situ sensor network is quite challenging. As the network size increases, the interactions among sensors within a network are extremely complicated. Meanwhile, the ad hoc working manner of WSNs prevent network administrators from looking into the in-network structures and behaviors of nodes, so it is difficult to pinpoint the root causes when abnormal symptoms are observed.

Manuscript received September 29, 2013; revised January 21, 2014 and June 6, 2014; accepted June 19, 2014. Date of publication July 8, 2014; date of current version October 8, 2014. This work was supported in part by the NSFC Distinguished Young Scholars Program under Grant 61125202 and in part by the NSFC under Grant 61103187. The associate editor coordinating the review of this paper and approving it for publication was L. Libman.

The authors are with the School of Software, Tsinghua National Lab for Informatics Science & Technology (TNList), Tsinghua University, Beijing 100084, China (e-mail: kebin@greenorbs.com; maq@greenorbs.com; gw@ greenorbs.com; miao@greenorbs.com; yunhao@greenorbs.com).

Color versions of one or more of the figures in this paper are available online at http://ieeexplore.ieee.org.

Digital Object Identifier 10.1109/TWC.2014.2336653

This work is motivated from our ongoing forest surveillance project GreenOrbs [15] with more than 330 sensor nodes deployed in the wild. GreenOrbs enables several applications such as canopy closure estimation and atmospheric concentrations of carbon dioxide monitoring in the forest. During the 10 months deployment period, we experience frequent abnormal symptoms in the network such as high data loss, temporary disconnection of nodes in a certain region, rapid energy depletion of some nodes and error readings. The failures can be categorized into two main classes, system and communication related failures such as node crash, poor link quality, routing loops, et al., and data errors due to the malfunction of sensors. Troubleshooting root causes in such a large network is crucial while time consuming, so efficient and accurate fault diagnosis tools are necessary for ensuring the system performance and lifetime.

In this research, we focus on handling system related failures. Existing approaches to diagnosing system errors in WSNs are mainly sink-based. They adopt the idea from traditional enterprise networks which periodically “pull” state information from all nodes and conduct fault inference process at the back-end. For example, Sympathy [18] collects status information from sensor nodes such as connectivity metrics and flow metrics. According to these metrics, sink troubleshoots the root causes with a decision tree. Zhao et al. [28] propose the energy scan scheme in which the residual energy and other parameter aggregates on sensor nodes are reported to sink. WSNs, however, are quite different from traditional networks in many aspects such as the extremely limited bandwidth resource of sensor nodes, very high network dynamics, remotely deployment, ad hoc manner and invisible network interactions to administrators. Therefore, sink-based approaches are not feasible in a large scale sensor network due to the following shortages. Firstly, proactive information collection leads to large communication overhead that heavily shortens the system lifetime. Based on the experience in our GreenOrbs deployment, we have found that collection of basic system states [18] can even consume more bandwidth than our forest surveillance application. Secondly, due to the large network scale and the unreliable wireless communications, the fault inference engine on the back-end generally obtains incomplete and uncertain information which significantly deteriorates the diagnosis accuracy. Finally, the diagnosis delay of sink-based approaches is high.

To address these issues, we propose to let every single sensor to be involved in the diagnosis process. Different from existing sink-based approaches, we “push” some diagnosis tasks to sensor nodes so they can join the fault inference and troubleshoot the root causes based on local evidences. The advantages of self-diagnosis are threefold. First, self-diagnosis can save a large amount of transmissions by applying local decision. Second, self-diagnosis avoids information loss on the way to sink and thus improves the accuracy. Finally, it provides realtime diagnosis results.

In spite of all these benefits, employing a self-diagnosis strategy in a large scale WSN is challenging. First, it is well known that the computation and storage resources at each sensor are limited, so the components injected to nodes have to be light-weight. Second, a sensor only has very narrow scope on the system state and in many cases it can hardly determine the root causes simply based on local evidences. Hence how to make multiple sensors cooperate with each other to detect network failures needs to be addressed.

In this study, we present our new self-diagnosis tool called TinyD2. We introduce our fault detectors based on the Finite State Machines (FSMs). The fault detectors encode the diagnosis process to state transitions. Each fault detector has several states, each of which indicates an intermediate step of the fault diagnosis process. Taking the local information from each node as input, the fault detector switches its state. Thus, a sensor can participate in the diagnosis by transiting the state of the fault detector to a new one based on local evidences and then deliver the detector to other nodes. Fault detectors travel among sensor nodes and continuously collect new evidences. When a detector achieves its Accept state, the fault is pinpointed and a diagnosis report can be formed accordingly. During the fault inference process, sensor nodes cooperate with each other to achieve the final diagnosis report that can assist network administrators in conducting further diagnosis or failure recovery actions. The detectors are light-weight in terms of storage space and computation overhead. During the diagnosis process, messages exchanged among sensors include not full detectors but only the current state of them which is necessarily small in size. We also form the diagnosis trigger as a change-point detection problem and present a triggering strategy based on the cumulative sum charts and a bootstrap scheme.

The major contributions of this work are as follows:

1) We study the problem of fault diagnosis in an operational sensor network and present a novel self-diagnosis framework for large scale WSNs.   
2) We design new fault detectors based on Finite State Machines, through which multiple nodes cooperate with each other and achieve diagnosis results.   
3) We form the diagnosis triggering as a change-point detection problem and address it based on cumulative sum charts and a bootstrap scheme.   
4) We implement our self-diagnosis approach TinyD2 and conduct intensive experiments to examine its effectiveness in a 100 nodes testbed and a 330 nodes working system.

The rest of this paper is organized as follows. Section II introduces existing efforts that are related to this work. Section III describes the fault detectors and the self-diagnosis process. We discuss the implementation details of TinyD2 in Section IV, and present the experimental results in Section V. We conclude the work in Section VI.

# II. RELATED WORK

Both debugging and diagnosing approaches are related to this work. Debugging tools [12], [19] aim at finding software bugs and even agnostic failures in sensor networks. Clairvoyant [26] enables the source-level debugging for WSNs which allows people remotely execute standard debugging commands such as step and break. Dustminer [9] focuses on troubleshooting unknown interactive bugs by mining the logs from sensor nodes. Dustminer aims to find event sequences that are rare to see when the system works well and frequently appear when system performance degrees. Then the administrators look into these suspicious sequences and locate the underlying root causes. Debugging tools are powerful at finding network faults, however, in cost of incurring huge control overhead, so they are generally used in the pre-deployment scenarios. Besides, debugging tools usually require human involvement. Instead, TinyD2 does not focus on exploring agnostic failures in pre-deployed systems but aims to provide lightweight and efficient diagnosis services for operational WSNs.

However, a post-deployment WSN may experience many failures even when there is no bug in its software system. The focus of this research is troubleshooting performance failures in networking and many existing efforts are related to our work. Some researchers propose to periodically scan parameters like residual energy [28] on sensor nodes. MintRoute [23] visualize the network topology by collecting neighbor tables from sensor nodes and thus help to find link and route failures. SNMS [20] constructs network infrastructure for logging and retrieving state information at runtime and EmStar [2] supports simulation, emulation and visualization of operational sensor networks. Other researchers employ varying inference strategies for troubleshooting network faults. Sympathy [18] actively collects metrics such as data flow and neighbor table from sensor nodes and determines the root causes based on a tree-like fault decision scheme. It can find faults on both node side and sink side. PAD [13] proposes the concept of passive diagnosis which leverages a packet marking strategy to derive network state and deduces the faults with a probabilistic inference model. PAD is designed to detect node and link level errors. Megan et al. [21] present Visibility, a new protocol design that aims at reducing the diagnosis overhead. PD2 [1] is a data-centric approach that tries to pinpoint the root causes of application performance problems. Nevertheless, most of the existing diagnosis solutions are sink-based and in this work we focus on a novel self-diagnosis approach which encourages sensor nodes to join the fault decision process. Some existing works have considered to perform self-diagnosis to identify faults by measuring local parameters. For example, Harte et al. [5] propose to determine if the node is vulnerable to hardware malfunctions by measuring accelerometers. Some researchers use battery voltage scanning [17] to estimate the power status of sensor nodes as well as predict the nodes’ residual lifetime. These approaches, however, mainly consider measurements within single node which are insufficient in many diagnostic tasks. Instead, TinyD2 introduces new fault detectors by which multiple sensors can collaborate in diagnosis process.

In this work, we focus on detecting system and communication related failures such as node crash, poor link quality, routing loops, and the like. In fact, there are other categories of failures. Note that even if the communication system works well and sensing data can be delivered to sink successfully, some sensors could malfunction and output wrong readings [29]. Different from performance failures, these errors, are data related which can also severely hurt the upper layer applications. Thus, besides the functional failures, many researchers also tackle the problem of detecting faulty sensing data [4]. Rajagopal et al. [16] propose an online scheme for detecting faulty readings. They explore the data correlation among neighboring sensors. SensorRank [24] explores a Markov Chain to rate sensors in terms of their correlation, thus faulty readings are detected through voting. The proposed voting scheme consists of a self-diagnosis phase in which current sensor reading is compared with the last correct reading from the same sensor and a neighbor-diagnosis phase that explores the spatial correlation among neighboring sensors. Network diagnosis techniques for large scale enterprise networks and Internet are also related to this work. SCORE [10] and Shrink [7] diagnose the network failures based on shared risk modeling. Giza [14] tries to address the performance diagnosis problem in a large IPTV network and NetMedic [8] enables detailed diagnosis in enterprise networks. Due to the ad hoc nature of sensor networks, enterprise network oriented approaches are normally infeasible for WSNs.

# III. IN-NETWORK FAULT DECISION

In this section, we describe our self-diagnosis scheme for in-network fault decision. In TinyD2, we propose the selfdiagnosis concept in which the root causes of faults are determined within the network. In-network fault decision exhibits many advantages such as saving traffic cost, higher accuracy, and realtime information. In the following subsections, we show the details of our self-diagnosis design.

# A. Motivation and Main Ideas

Obviously, letting all sensor nodes deliver their detailed system information and interactions with all other sensor nodes at realtime is impractical in a large scale sensor network, our idea is encouraging the sensor nodes to join the fault diagnosis process, as the sensor nodes have the first-hand evidences. Nevertheless, pushing fault inference tasks to sensor nodes will bring additional computation and storage cost as well as message exchanging overhead in local area to sensors. Besides, as single sensor node only has limited scope on the system state, self-diagnosis without centralized control may face more challenges compared with traditional back-end fault inference solutions.

A straightforward approach for achieving self-diagnosis is to assign several thresholds on each sensor and make the sensor nodes continuously monitor local system information, and report a failure when the threshold is exceeded. Such a method is easy to implement and efficient in detecting some types of local problems like low battery power. Unfortunately, it often fails to deal with the following two situations. Firstly, as sensor nodes only have limited scope on the system state, it cannot detect the root causes of many interactive problems that are caused by the interactive behaviors among multiple sensor nodes. Secondly, problematic sensors, for example the crashed nodes themselves are usually incapable to detect and report their problems to the sink. In this case, we can only infer their failures from the neighbors.

Another choice is to leverage the clustering schemes and make sensor nodes report their information to cluster heads where the fault diagnosis process is performed. Such an approach can employ existing inference methods at the head nodes, while it has the limitation that it can only be applied in clustering networks. Otherwise, it will be quite costly to maintain such infrastructures. Besides, the overhead of collecting information from sensor nodes to cluster heads is non-negligible.

Instead, we present a new self-diagnosis solution which makes multiple sensors cooperate with each other to deter-mine the diagnosis results. We propose a series of fault detectors that can act as glue and stick different sensors to a diagnosis task. After the system is deployed, each sensor continuously monitors its local system information. If some exceptions occur, the sensor creates a new fault detector. Detailed diagnosis triggering scheme will be discussed in Section III-D.

During the diagnosis process, sensor nodes only transmit the current state of the fault detector and the detector structures are stored in each sensor. Once a final diagnosis decision is achieved, the sensor node will cache the report for a specified period. The report handling actions includes reporting the diagnosis decision to sink as well as starting the active state collection components if more information is required by the sink.

TinyD2 is designed for different kinds of ad hoc networks with varying network topologies. For failures that are caused by local errors such as the low battery power or system reboot, our approach can pinpoint the root causes from the local evidences only. In this case, diagnosis process is finished within one single node. For some exceptions appear during the interactions among multiple sensors, TinyD2 requires several nodes to collaborate with each other. In this scenario, we assume that neighboring nodes have connections with each other directly or through multi-hop paths.

# B. Fault Detector Design

In TinyD2, the fault detectors encode the fault inference process to state transition. Our detectors are based on the Finite State Machines (FSMs) model. A FSM model consists of a finite number of states and transitions between these states. A transition in FSM means a state change which will be enabled when specified condition is fulfilled. Current state is determined by the historical states of the system, so it indicates the series of inputs to the system from the very beginning to present moment. Our fault detectors generalize the FSM model and use local evidences on each sensor node as inputs. Each state can be seen as an intermediate diagnosis decision and if the local evidences support certain conditions on current state we transit the detector to the corresponding new state.

As there will be different kinds of failure cases, one fault detector cannot cover all of them. To address this issue, we group the exceptions into different categories and the classification of an exception is according to its symptom. We then design fault detectors for different categories of faults. We consider three classes of symptoms. The first category of symptoms is caused by local errors such as the low battery power or system reboot, which means we can pinpoint the root causes from the local evidences only. The second category relates to failures on other nodes, for example if current node detects that a neighbor has just been removed from its neighbor table, it will issue a fault detector to neighborhood to make sure whether this neighbor is still alive. The third category of symptoms can be caused by local or external problems while multiple nodes interact with each other. For example, when two nodes are interacting with each other and the sender experiences a high retransmission ratio on its current link. The node, however, is unable to know whether it is because of the poor link quality or the congestion at the receiver. To deal with unknown type of failures, our solution provides an open framework that can scale to new fault types by developing and disseminating new fault detectors to sensor nodes.

![](images/c3fb1b25addcb17503c5fcbd429f97bc38f7982a2749bd5897b4822842d8438b.jpg)



Fig. 1. An example of the FSM-based fault detector. (a) A partial network topology. (b) The data structure of an FSM-based fault detector.

Now we take the high retransmission ratio as an example to describe our fault detector design. The fault detector for this exception is shown in Fig. 1.

In Fig. 1(a), we illustrate a partial network topology in which sensor node A is transmitting packets to node B, {Ci} denotes a group of sensors in the neighboring region of A and B that can communicate with A and B. At the very beginning, A detects that the retransmission ratio on link $A - > B$ abruptly turns to be significantly high, so A creates a new fault detector as shown in Fig. 1(b). Formally, the fault detector M is represented as a quintuple $M = ( E , S , S _ { 0 } , f , F )$ where E denotes the set of input evidences, S is the set of states in which $S _ { 0 }$ is called the Start state, F denotes a subset of S that includes all Accept states, f are the set of state-transition functions which specify the conditions for state switching. In the example of Fig. 1(b), cyclic vertices $S _ { i }$ denote states in $S ,$ each arc indicates a possible transition from one state to another and annotations on the arcs specify the transition conditions. Note that some states may have self-loops. States denoted by double cycles are the Accept states which represent final diagnosis decisions. When a fault detector reaches an Accept state, we can conclude the fault type and root causes.

![](images/117209295cfe0a18a069b1cca8ae64f5ff85f9a5ee07806a7894b68b4036f05f.jpg)



Fig. 2. State transitions of the fault detector in a self-diagnosis process.

Now we describe the details of a diagnosis process with the detector shown in Fig. 2. Assume that A detects an abnormal retransmission ratio change on its link $A - > B ,$ , it creates a new fault detector which is now at the Start state. In this detector, the Start state has the meaning that some node A finds that its transmission performance experiences problems on link $A - > B _ { }$ . A then broadcasts the current state together with the detector type to its neighbors. Two categories of nodes may receive and handle this state, the first category includes the receiver $B$ and the second category contains a group of nodes that have recently transmits packets to A or $B$ denoted as $\{ C _ { i } \}$ . Based on their local knowledge, they can make different transitions. In this example, if B receives the Start state, it checks its local evidences for the fact that if it has just received many duplicated data packets from A. Since recording all detailed acknowledgment information is costly, here the duplicate reception is used as an indication of whether B has received and acknowledged the data packets from A. If B has acknowledged A but still receives the same data packet from $A ,$ it means that A successfully sends the packets to B but fails to receive the acknowledgment from $B ,$ , otherwise it means that B has difficulties in receiving data packets from $A .$ The arcs with conditions $B - / - > A$ and $A - / - > B$ represent the two situations, respectively. Based on $B \mathrm { ^ { * } s }$ local evidences, we can change the state from Start to $S _ { 1 }$ or $S _ { 2 } .$ . In this example, as illustrated by the blue arc in Fig. 2, B does not receive enough data packets from $A ,$ so $B$ transits the state to $S _ { 2 }$ and rebroadcast this state. $S _ { 2 }$ can be handled by nodes in $\{ C _ { i } \}$ . If the local information of $C _ { i }$ shows that the data delivery from $C _ { i }$ to B is successful, it can be inferred that the poor link quality on link $A - > B$ leads to the high packet loss (frequent retransmissions). In this case, $C _ { i }$ transits the detector state to an Accept state $L _ { A - > B }$ which indicates a poor link quality on link $A - > B$ . Otherwise, if $C _ { i }$ can hardly transmit data packets to B as well, the state is transited to $S _ { 7 }$ as shown by the blue arc. Note that the state $S _ { 7 }$ has self-loops on condition $C _ { i } - / - > B$ . if the state with self-loops has an output arc labeled with $N U M$ , it indicates that this state has a threshold on the maximum number of loops. Take $S _ { 7 }$ for example, if more than a certain number of nodes say that they have problems in communicating with $B ( C _ { i } - / - > B )$ , we transit the state to the Accept state $B _ { c }$ which indicates that there are severe contention at B and node B is probably congested.

One potential issue in this design lies in the fact that the diagnosis messages can also be lost due to the network failures. For example, as shown in Fig. 1 if node B is congested, it may have difficulties in receiving data packets as well as diagnosis message (state of a fault detector) from A. However, our fault detectors are not intended for single node, all neighbors which heard the detector can join the diagnosis process as long as it has related evidence. In the above example, though node B fails to hear the diagnosis message from A due to the congestion, some other nodes $\{ C _ { i } \}$ may forward the diagnosis process and reach the conclusion that B is congested.

Another issue is that it is difficult to make different sensor nodes achieve consistent diagnosis results due to the distributive manner of TinyD2. Since different nodes have different views of the network, they would reach different conclusions for the same fault detector. In this case, sink will tolerate all these results and conduct further analysis by querying more information.

# C. Message Exchanging and Report Handling

The message exchanged during the diagnosis process include four major parts, the source node ID that creates the fault detector, the detector type, current state of the detector and other supplementary information. In the example of Fig. 2, we add the ID of node B as the supplementary information to a diagnosis message.

Upon receiving the state of a new fault detector, the sensor node will check whether it can contribute to this fault diagnosis task. If it has some knowledge, the sensor will transit the state of the corresponding fault detector and propagate the new state, otherwise it simply drops or broadcasts the state to other nodes according to the lifetime of this detector. Note that each fault detector has a limitation (similar to TTL) on the number of hops it is delivered.

When the final diagnosis decision is made at some node, it will try to report the decision to sink. If further information is required by the sink, the corresponding sensor nodes will start the active information collection components.

# D. Diagnosis Process Triggering

Frequent diagnosis processes can lead to high transmission and computation cost in a local region. There is a trade-off between the diagnosis performance and the cost: triggering more fault detectors can improve the fault detection ratio and reduce the detection delay at the cost of higher overhead. To address this issue, we propose a triggering strategy based on the change-point analysis method.

We investigate two categories of evidences for detecting abnormal symptoms and triggering diagnosis. The first category of evidences are the occurrences of special events, such as the sensor node changes its parent, a neighbor has just been removed from the neighbor table of current node, local error events are detected, and the like. Once these specified events are detected, we directly trigger a new diagnosis process. The second category of evidences come from the changing of certain parameter values, such as the retransmission frequency, ingress and egress traffic, routing metrics like ETX, and the like.

Abnormal values of these parameters are related to network failures. These parameters, however, can have varying values for different nodes. For example, sensor nodes in different network region can exhibit varying traffic measurements while all of them are healthy. Therefore, it is infeasible to set fixed thresholds on these parameters for diagnosis triggering. Instead, we observe that the network errors take place when certain parameters experience a significant change trend in its value. For example, the ingress traffic of a node significantly decreases for a certain time period or the retransmission frequency on a link remarkably rises. Then a new fault detector is created for diagnosing the root causes. As state parameters observed by a node may deviate from routine values due to temporary fluctuations in the network, it is very challenging to decide whether the state deviations are caused by a new failure or just jitters. The major issue during this process is to determine whether a significant change has taken place in the parameter values. In this work, we form this problem as a change-point detection problem by regarding the sampled values of a parameter during the last period as a time series. Change-points are defined as the abrupt variations in the generative parameters of a time series and by recognizing these variations we can know whether there are apparent changes in the parameter values. There are many existing solutions for change-point detection and analysis. Considering the limited computation and storage resources in sensor nodes, in this work we apply a light-weight approach which combines the cumulative sum charts (CUSUM) and bootstrapping to detect changes.

Cumulative Sum Charts: We take the traffic data as an example to illustrate the diagnosis triggering scheme. In TinyD2, we apply a window-based scheme for caching the latest parameter values. As shown in Fig. 3(a), assume that the window size is 12 and thus a sensor node stores 12 latest data points of its ingress traffic. At the first step, we calculate the cumulative sum charts of this data sequence. Let $\{ X _ { i } \} i = 1 , 2 , \dots , 1 2$ denote the data points in this stream and X be the mean of all values. The cumulative sums are represented as $\{ C _ { i } \} i = 0 , 1 , \dots , 1 2$ . Here we define $C _ { 0 } = 0$ and then the other cumulative sums are calculated by adding the difference between current value and the mean value to the prior sum.

$$
C _ {i} = C _ {j - 1} + (X _ {i} - \overline {{{X}}}) \tag {1}
$$

The CUSUM series are illustrated in Fig. 3(b). The CUSUM reaches zero at the end. An increase of the CUSUM value indicates that the values in this period are above the overall average value and a descending curve means that values in the corresponding period are below the overall average.

![](images/c760d9525d2cca0583427773e3fd95a93a8d01c3da4077b52fabe0a8ee6770b9.jpg)



(a）

![](images/4b3812877b403d01e9c912f11be20f061569b01522d48e701dba9ae583482a92.jpg)



(b)   
Fig. 3. Cumulative sum charts.

A straight line in the cumulative sum charts indicates that the original values are relatively stable. In contrast, bowed curves are caused by variations in the initial values. The CUSUM curve in Fig. 3(b) turns in direction around $C _ { 6 }$ and we can infer that there is an abrupt change. Besides making decision directly according to the CUSUM charts, we also propose to assign a confidence level to our determination by a bootstrap analysis.

Bootstrap Strategy: Before discussing the bootstrap scheme, we firstly introduce an estimator $( D _ { c } )$ of the change which is defined as the difference between maximum value and minimum value in $\{ C _ { i } \}$ .

$$
D _ {c} = \max (C _ {i}) - \min (C _ {i}) \tag {2}
$$

In each bootstrap, we randomly reorder the original values and obtain a new data sequence, that is, $\{ X _ { i } ^ { j } \} j = 1 , 2 , \dots m$ where m denote the number of bootstraps we performed. Then the cumulative sums $\{ C _ { i } ^ { j } \}$ as well as the corresponding $D _ { c } ^ { j }$ are calculated based on the new sequence $\{ X _ { i } ^ { j } \}$ .

The idea behind bootstrap is that randomly reordered data sequences simulate the behavior of CUSUM if no change has occurred. With multiple bootstrap samples we can estimate the distribution of $D _ { c }$ without value changes. We then derive the confidence level by comparing the $D _ { c }$ calculated from values in original order with that from the bootstrap samples.

$$
\text { Confidence } = \text { NumberOf } (D _ {c} > D _ {c} ^ {j}) / m \tag {3}
$$

Where $D _ { c }$ is calculated from the original data sequence and $D _ { c } ^ { j }$ is derived from a bootstrap, m is the total number of bootstraps performed. If the confidence is above a pre-specified threshold, for example 90%, we decide that there is an apparent change in the parameter values.

Localizing the Change-Point: After determining the occurrence of a change, we localize the position of the change with a simple strategy by finding $C _ { i }$ with the largest abstract value. In this example, $C _ { 6 }$ has the largest abstract value, so we decide that the value change occurs between $X _ { 6 }$ and $X _ { 7 }$ . Note that this method can easily be generalized to find multiple changes, however, in this work we only cache and process parameter values in a short period, so we only pick out the major change and trigger a diagnosis process.

TABLE I DEPLOYMENTS OF THE FOREST MONITORING PROJECT 

<table><tr><td>Place</td><td>Area</td><td>Duration</td><td>Size</td><td>Network Diameter</td></tr><tr><td>Campus woodland</td><td> $20000m^{2}$ </td><td>10 months</td><td>120 nodes</td><td>10 hops</td></tr><tr><td>Campus woodland</td><td> $40000m^{2}$ </td><td>Ongoing(2009.12~)</td><td>330 nodes</td><td>12 hops</td></tr><tr><td>Tianmu Mountain</td><td> $200000m^{2}$ </td><td>1.5 months(2009)</td><td>50 nodes</td><td>10 hops</td></tr><tr><td>Tianmu Mountain</td><td> $200000m^{2}$ </td><td>Ongoing(2009.10~)</td><td>200 nodes</td><td>20 hops</td></tr></table>

# IV. TINYD2 IMPLEMENTATION

We have implemented the TinyD2 on the Telosb mote with a MSP430 processor and CC2420 transceiver. On this hardware platform, the program memory is 48 K bytes and the RAM is 10 K bytes. We apply the TinyOS 2.1 as our software development platform and the application and TinyD2 diagnosis functionalities are implemented as different components. In the following subsections, we will firstly introduce the application background and the protocol design of our GreenOrbs project, and then we show the details of integrating TinyD2 with GreenOrbs.

# A. The GreenOrbs Sensor Network System

We launch our forest monitoring sensor network system which targets several urgent applications in forestry such as canopy closure estimates, carbon sequestration, research on biodiversity and the fire risk prediction. Table I illustrates our main deployment experiences up to now.

The software on the sensor nodes is developed on the TinyOS 2.1 which is the most widely used platform for sensor networks. Fig. 4 illustrates the major components in our system. We apply some components from the TinyOS library which provide low layer functionalities such as the basic wireless communication, the timing service and methods for accessing the external flash. The Data Collector is in charge of sampling the sensing data and sending them to sink through multi-hop routes. Our routing protocol is design based on the CTP [3]. The Synchronization Component provides the network-wide synchronization service and thus enables the synchronized duty cycles. We also include a Logger that can record local events in external flash and the logged data may aid the software debugging process.

![](images/15467739071cbf872ff4a1be3ebbe9138897fe5575e9452b4ddb7eefbc0b85ed.jpg)



Fig. 4. Software diagram of the GreenOrbs system with TinyD2.

# B. Integrate TinyD2 With GreenOrbs

In the diagram of Fig. 4, components in the gray region belong to TinyD2. The Information Collection component collects and caches system information from other components. The Diagnosis Triggering component dynamically examines the system information and starts a fault diagnosis process when abnormal situations detected. The Local Diagnosis Controlling component transits the state of fault detectors according to the information from the Information Collection component and thus to advance the diagnosis process. The Message Exchanging component takes responsible for exchanging intermediate detector states with other sensor nodes. The Report Processing component is in charge of dealing with the final diagnosis report. When a final diagnosis decision is made at current node, the Report Processing component firstly tries to deliver the diagnosis results to sink. If the route between current node and sink is unavailable, the Report Processing component will broadcast the reports to its neighbors. For some fault types, sink needs to retrieve further information from sensor nodes, in this case the Report Processing component will handle these queries. The above 5 components provide interfaces of their corresponding functions and DiagnosisC component uses these interfaces and provides the integrated interface Diagnosis. After we integrate the TinyD2 with GreenOrbs, the ROM usage increases by 7.3 K bytes.

# V. EXPERIMENTS

In the section, we describe performance evaluation results of our TinyD2 approach as well as our deployment experiences with TinyD2 in a large scale operational sensor network. In the first stage, we conduct experiments to test the accuracy and energy efficiency of TinyD2 with manually injected faults in a 100 nodes test bed. The results are presented in Section V-A. We then discuss field studies in GreenOrbs with TinyD2 in Section V-B.

# A. Performance Evaluation

In the first stage, we test the performance of TinyD2 in a test bed with 100 sensor nodes. These sensor nodes are powered by the USB hardware interface. We implement TinyD2 on sensor motes and evaluate its performance and overhead by manually injecting varying types of errors. We employ two metrics for measuring the diagnosis performance of TinyD2, the detection ratio and the false alarm ratio. The detection ratio is defined as the ratio between the number of faults detected and the number of all faults. Higher detection ratio can help the network managers recover more failures. The false alarm ratio is the ratio between false alarms and all diagnosis reports. A low false alarm ratio indicates that the diagnosis tool has a high accuracy.

In our experiments, we compare the performance of TinyD2 with PAD, one of the recent diagnosis approaches for sensor networks. PAD proposes the concept of passive diagnosis which collects the network information by marking routine data packets and deduces the root cause with a probabilistic inference model. PAD is efficient both in diagnosis performance and the energy consumption. During these tests, we manually inject three types of failures, the node crash, link failures and the bad routes. We also vary the network size from 20 to 100.

Fig. 5 shows the results of node crash detection. According to Fig. 5(a), TinyD2 successfully finds more than 90% of the crashed nodes and the detection ratio keeps stable as the network size increases. PAD achieves a more than 90% detection ratio in a small network, however, when network size increases its detection ratio decreases to around 80% (in the network with 100 nodes). As shown in Fig. 5(b), the false alarm ratio of TinyD2 is around 10% over varying network sizes and PAD has more false alarms in larger networks.

This is because PAD relies on the probabilistic inference model to deduce the root cause, when the network size increases, the model turns to be more complicated and thus incurs more wrong results. Instead, TinyD2 encourages all sensor nodes to join the diagnosis process and makes decisions based on the local evidences of the sensor nodes and thus can provide stable diagnosis results in spite of the overall network size.

Fig. 6(a) and (b) illustrate the detection ratio and false alarm ratio of the two approaches on diagnosing the link failures over different network sizes. We observe similar trends in these results. TinyD2 achieves a higher detection ratio and lower false alarm ratio than PAD and the performance of TinyD2 is more stable. In Fig. 7(a) and (b), we show the results of diagnosing the bad routes failures. As the probabilistic inference model in PAD doesn’t output the bad routes failure directly, so we only present the results of TinyD2. According to the results in Figs. 5–7, we can conclude that TinyD2 achieves similar performances on detecting all these three types of failures.

![](images/9b2f324d6bdc2562cc41ba6f165ec8ec194fbcfda67c28ea8457852157f98ddd.jpg)



![](images/38b09d077ecf1fb0b819a070144a57057f861ec3c22bdd424004cffa44f8d690.jpg)



![](images/fca4b2e029df3b6b623d1b008c7fbbc05f020685ad32ce3342ce0a8e1abc7d54.jpg)



(b)

![](images/5f77ab9e6c751c37db78d0525d3ece01bf03690a45e3c05105778c77f9e2b80d.jpg)



Fig. 7 (a) The detection ratio for bad routes V.S. network size. (b) The false alarm ratio for bad routes V.S. network size.

Fig. 5 (a) The detection ratio for node crash V.S. network size. (b) The false alarm ratio for node crash V.S. network size.   
![](images/d9fe6ac878d3e842d98e86ee4af2c1a8393857cd82eb10614cf7b6bef6641da3.jpg)



![](images/a71ecb0c2fb276288f3085597fccdd0259115d86b888416af5d05eb7bc2980cc.jpg)



Fig. 8. Overhead (TinyD2 V.S. PAD).

![](images/2a4f7c445368d94bd3f6404092fca6275d82774a85cd5a4eba3e2ec04efdf1fc.jpg)



Fig. 6 (a) The detection ratio for link failures V.S. network size. (b) The false alarm ratio for link failures V.S. network size.

We then evaluate the overhead of TinyD2. We firstly compare the traffic overhead of TinyD2 with that of PAD. PAD is very lightweight in the bandwidth consumption since it obtains network information only by marking routine data packets. Note that it is difficult to directly measure the energy consumption of the diagnosis services from an operational sensor network without extra hardware. As radio communications dominate the power consumption [22] of diagnosis approaches, we use the traffic incurred by different diagnosis approaches to estimate their energy cost. We apply the ratio between diagnosis traffic and the overall network traffic to quantify the overhead. Fig. 8 shows the CDF of the two approaches’ traffic overhead. The X axis shows the percentage of traffic that a diagnosis tool takes in total network traffic and Y axis illustrates the cumulative probability. For example, a data point <5%, 0.9> means that at 90% of cases the diagnosis tool takes less than 5% of the total traffic. The curve of TinyD2 is on the left of the curve of PAD which indicates that the cumulative overhead of TinyD2 is less than PAD. For example, according to Fig. 8, at 80% of the cases the TinyD2 only uses less than 3.5% of overall network traffic while PAD uses less than 6%. Note that typical sinkbased approaches such as Sympathy [18] can incur even more traffic cost than the initial sensory data acquisition applications and thus their traffic usages can exceed 50%. Reasons to explain the results are three-folds. First, TinyD2 mainly explores local information exchange with sporadic reports to sink and in sink-based approaches, system metrics from all nodes are delivered to sink over long paths. Second, TinyD2 uses short messages, which contains the state of a detector only. Sinkbased methods, however, need to transmit a large number of parameters. Finally, in TinyD2, only the problematic regions trigger a diagnosis process while sink-based schemes require all nodes periodically report their information.

![](images/b16ee15ab8329bda5859eaf30878cca8f5928bb54977b13eca317f5728f38d10.jpg)



Fig. 9. Overhead over time.

We also evaluate the overhead of TinyD2 over time. As shown in Fig. 9, we find that the overhead of TinyD2 exhibits high variations over time. In this figure, X axis is the timeline and the Y axis shows the traffic overhead. In some timestamps, the diagnosis overhead is less than 1% and in some other timestamps the overhead can reach to nearly 4%. This is because the TinyD2 is an on-demand approach which only works when network failures occur.

# B. Field Studies

In this section, we discuss our field studies with TinyD2 in our GreenOrbs system. A part of the logical topology of our network is illustrated in Fig. 10. During the deployments, we measure the system performance by the Packet Delivery Ratio which is the ratio between the number of packets received by sink and the number of packets sent by all sensor nodes. We also randomly sample two local metrics on some sensor nodes, the Link Reception Ratio and Traffic.

As illustrated in Fig. 11(a), when the network contains 100 and 200 nodes, nearly 80% of the packets are reported to sink in time. When the network size is 330 nodes, the Packet Delivery Ratio is around 60%. Fig. 11(b) shows the average Packet Delivery Ratio of nodes that have varying hop distances to sink. According to the results, we can conclude that the farther the node is away from sink, the less data they deliver to sink. Meanwhile, Fig. 11(b) also presents the average Link Reception Ratio of nodes that have different hop distances to sink. From the results in Fig. 11(b), we find that more than 90% transmissions on our sampled links can successfully reach the receiver in varying areas of the network. Note that the communication protocol applied in our current system has a link layer retransmission strategy, so we believe that poor link qualities are not the major cause of the system performance degradation.

![](images/30e0d15bbe8982e016d27c984ee0b1d7151cdf38b7bc2bf0d2d17b7e2af36341.jpg)



Fig. 10. Part of logical topology of the forest monitoring sensor system.

With the help of TinyD2, we summarize four major categories of network faults that are responsible for the poor Packet Delivery Ratio in our system. We analyze the occurrence frequency of these failures as well as their hazard rating to the network performance. We also propose advice on potential recovery methods.

The first category of failures is node crash, including both software and hardware errors. The crashed nodes do not send or respond to any message. These fatal errors are caused by the unreliability of the software system and physical damages. For example, the rain can short-circuit the batteries of sensor nodes and thus destroy the nodes’ power supply. Nodes that experience a software crash can be recovered by manually reboot and physical damages can only be resolved by changing the hardware. TinyD2 detects that around 3% of nodes may be crashed during a long term deployment. The occurrences of node crash randomly distribute over the whole deployment regions.

The second category of network faults are ingress drops or message pool overflow drops. Ingress drop means that the receiver has successfully acknowledged a packet but drops the packet before processing it. In our current system, the received packets are firstly cached in a message pool of the sensor node, and then being processed and forwarded to the parent node. If the message pool overflows, the ingress drop occurs. The message pool will overflow if the incoming traffic is higher than the node processing capability. Besides, ingress drops can also result from some software bugs. According to the results from TinyD2, only a few nodes (around 2% of all sensor nodes) have the ingress drop problem. They, however, severely deteriorate the system performance. For example, during our deployment one sensor nodes that experience ingress drop contributes nearly 10% of all packet losses. With further investigation, we find that this node directly drops all incoming packets due to a software bug. In our current routing protocol, parent selection is only based on ETX. As this node successfully sends its own packets to sink and thus exhibits a relatively low ETX value, many downstream nodes choose this node as parent, so a significant amount of packets are lost. By this way, this node steals the traffic in our network. Based on this observation, we are trying to fix this bug as well as redesigning our routing strategy to avoid such problems.

![](images/8710150666c510ac320c17025d0777987f277c269f3ecd933171d42488a62bd9.jpg)



(@)

![](images/4508d9cbb1e478e849cd2f1fdb5af41657b174d75739433557ae895a06830041.jpg)



(b)   
Fig. 11. (a) Packet delivery ratio V.S. network size. (b) Packet delivery ratio and link reception ratio V.S. number of hops.

The third source of packet losses are link related failures or egress drops. We have a retransmission strategy in our link layer protocols to ensure the reliability of the packet transmission. If the sender doesn’t receive the acknowledgement of a data packet for a specified period, it will retransmit this packet. There is a threshold for the maximum number of retransmissions and if the threshold is reached, sender will drop this packet. Based on the results from TinyD2, egress drop can be caused by two major reasons, the poor link quality and collision. During our deployment, more than 50% of sensor nodes have experienced egress drops, however, the number of lost packets by egress drops is not very large and most of sensors only drop very few packets.

The last major category of faults is bad routes, that is, sensor nodes cannot find a path to sink. Bad routes usually lead to network partition when they occur at some critical nodes. Here we use the term critical nodes to represent nodes that have many children nodes and these children don’t have other alternative parents. Although we have carefully assigned the positions of sensor nodes to avoid critical nodes or critical positions during the deployment stage, however, there are still many such critical points. Based on the results from TinyD2, we find many bad routes cases in which a group of sensor nodes are separated from the network. In the bad routes cases, we usually detect routing loops as well.

In order to address the bad routes problem, the first possible solution is to refine the deployments and thus to reduce the critical nodes. The second strategy is to detect the bad routes problem at real time with diagnosis tools like TinyD2 and redeploy more nodes on these critical regions.

# VI. CONCLUSION

In this work, we propose a novel self-diagnosis approach TinyD2 for large scale sensor networks. Existing diagnosis approaches are mainly sink-based which suffer from the high communication overhead and the incomplete diagnosis information. Instead, TinyD2 employs the self-diagnosis concept which encourages all sensor nodes to join the diagnosis process. To address the issue of single nodes having insufficient information for determining the root causes for many failures, TinyD2 presents a series of novel fault detectors through which multiple nodes can cooperate with each other in a diagnosis task. The fault detectors encode the diagnosis process to state transitions. Through comprehensive experiments in both indoor testbed and a 330 nodes outdoor sensor system, we compare this design with existing approaches.

# REFERENCES

[1] Z. Chen and K. G. Shin, “Post-deployment performance debugging in wireless sensor networks,” in Proc. IEEE RTSS, 2009, pp. 313–322.   
[2] L. Girod et al., “EmStar: A software environment for developing and deploying wireless sensor networks,” in Proc. USENIX Annu. Tech. Conf., 2004, pp. 283–296.   
[3] O. Gnawali, R. Fonseca, K. Jamieson, D. Moss, and P. Levis, “Collection tree protocol,” in Proc. ACM SenSys, 2009, pp. 1–14.   
[4] S. Guo, Z. Zhong, and T. He, “FIND: Faulty node detection for wireless sensor networks,” in Proc. ACM SenSys, 2009, pp. 253–266.   
[5] S. Harte and A. Rahman, “Fault tolerance in sensor networks using selfdiagnosing sensor nodes,” in Proc. IEE Int. Workshop Intell. Environ., 2005, pp. 7–12.   
[6] T. He et al., “Energy-efficient surveillance system using wireless sensor networks,” in Proc. ACM MobiSys, 2004, pp. 270–283.   
[7] S. Kandula, D. Katabi, and J.-P. Vasseur, “Shrink: A tool for failure diagnosis in IP networks,” in Proc. MineNet Workshop ACM SIGCOMM, 2005, pp. 173–178.   
[8] S. Kandula et al., “Detailed diagnosis in enterprise networks,” in Proc. ACM SIGCOMM, 2009, pp. 243–254.   
[9] M. M. H. Khan, H. K. Le, H. Ahmadi, T. F. Abdelzaher, and J. Han, “Dustminer: Troubleshooting interactive complexity bugs in sensor networks,” in Proc. ACM SenSys, 2008, pp. 99–112.   
[10] R. R. Kompella, J. Yates, A. Greenberg, and A. C. Snoeren, “IP fault localization via risk modeling,” in Proc. USENIX NSDI, 2005, pp. 57–70.   
[11] M. Li and Y. Liu, “Underground structure monitoring with wireless sensor networks,” in Proc. IEEE/ACM IPSN, 2007, pp. 69–78.   
[12] P. Li and J. Regehr, “T-Check: Bug finding for sensor networks,” in Proc. IEEE/ACM IPSN, 2010, pp. 174–185.   
[13] K. Liu et al., “Passive diagnosis for wireless sensor networks,” in Proc. ACM SenSys, 2008, pp. 113–126.   
[14] A. Mahimkar et al., “Towards automated performance diagnosis in a large IPTV network,” in Proc. of ACM SIGCOMM, 2009.   
[15] L. Mo et al., “Canopy closure estimates with GreenOrbs: Sustainable sensing in the forest,” in Proc. ACM SenSys, 2009, pp. 99–112.   
[16] R. Rajagopal, X. Nguyen, S. C. Ergen, and P. Varaiya, “Distributed online simultaneous fault detection for multiple sensors,” in Proc. IEEE/ACM IPSN, 2008, pp. 133–144.   
[17] D. Rakhmatov and S. B. Vrudhula, “Time-to-failure estimation for batteries in portable electronic systems,” in Proc. Int. Symp. Low Power Electron. Des., 2001, pp. 88–91.

[18] N. Ramanathan et al., “Sympathy for the sensor network debugger,” in Proc. ACM SenSys, 2005, pp. 255–267.   
[19] T. Sookoor, T. Hnat, P. Hooimeijer, W. Weimer, and K. Whitehouse, “Macrodebugging: Global views of distributed program execution,” in Proc. ACM SenSys, 2009, pp. 141–154.   
[20] G. Tolle and D. Culler, “Design of an application-cooperative management system for wireless sensor networks,” in Proc. IEEE EWSN, 2005, pp. 121–132.   
[21] M. Wachs et al., “Visibility: A new metric for protocol design,” in Proc. ACM SenSys, 2007, pp. 73–86.   
[22] Q. Wang, M. Hempstead, and W. Yang, “A realistic power consumption model for wireless sensor network devices,” in Proc. IEEE SECON, 2006, pp. 286–295.   
[23] A. Woo, T. Tong, and D. Culler, “Taming the underlying challenges of reliable multihop routing in sensor networks,” in Proc. ACM SenSys, 2003, pp. 14–27.   
[24] X. Y. Xiao, W. C. Peng, C. C. Hung, and W. C. Lee, “Using sensorranks for in-network detection of faulty readings in wireless sensor networks,” in Proc. 6th ACM Int. Workshop Data Eng. Wireless Mobile Access, 2007, pp. 1–8.   
[25] N. Xu et al., “A wireless sensor network for structural monitoring,” in Proc. ACM SenSys, 2004, pp. 13–24.   
[26] J. Yang, M. L. Soffa, L. Selavo, and K. Whitehouse, “Clairvoyant: A comprehensive source-level debugger for wireless sensor networks,” in Proc. ACM SenSys, 2007, pp. 189–203.   
[27] Z. Yang, M. Li, and Y. Liu, “Sea depth measurement with restricted floating sensors,” in Proc. IEEE RTSS, 2007, pp. 469–478.   
[28] J. Zhao, R. Govindan, and D. Estrin, “Residual energy scan for monitoring sensor networks,” in Proc. IEEE WCNC, 2002, pp. 356–362.   
[29] R. Zhang, P. Ji, D. Mylaraswamy, M. Srivastava, and S. Zahedi, “Cooperative sensor anomaly detection using global information,” Tsinghua Sci. Technol., vol. 18, no. 3, pp. 209–219, Jun. 2013.

![](images/0c694df3ee8efae2712d37169f05dc9ba31a5eacf32ed1240a6aed25dd8a6e0e.jpg)



Qiang Ma received the B.S. degree from the Department of Computer Science and Technology, Tsinghua University, Beijing, China, in 2009 and the Ph.D. degree in computer science and engineering from Hong Kong University of Science and Technology, Kowloon, Hong Kong, in 2013. He is now a Postdoctoral Researcher with the School of Software, Tsinghua University. His research interests include sensor networks and diagnosis.

![](images/38126c220c46d71d4e82a8e1a1406a3feaac3f6c6279d40686f68eb597b2211e.jpg)



Wei Gong received the B.S. degree from the Department of Computer Science and Technology, Huazhong University of Science and Technology, Wuhan, China, in 2003 and the M.S. and Ph.D. degrees from the School of Software and the Department of Computer Science and Technology, Tsinghua University, Beijing, China, in 2007 and 2012, respectively. His research interests include WSNs, RFID, and mobile computing.

![](images/1ffb954082936f0e4776a43a0d1663b7dff3a1e97241e11aea0c6796d8581f4a.jpg)



Xin Miao received the B.S. degree from the Department of Computer Science and Technology, Tsinghua University, Beijing, China, in 2005 and the Ph.D. degree in computer science and engineering from Hong Kong University of Science and Technology, Kowloon, Hong Kong, in 2013. He is currently a Postdoctoral Researcher with the School of Software, Tsinghua University. His research interests include sensor networks and RFID.

![](images/84b1c8804e6c936bf3e64e113de29bc32d55bb628bf3561badff9673c73e6196.jpg)



Kebin Liu (M’08) received the B.S. degree from the Department of Computer Science, Tongji University, Shanghai, China, in 2004 and the M.S. and Ph.D. degrees from Shanghai Jiao Tong University, Shanghai, in 2007 and 2010, respectively. He is currently an Assistant Researcher with the School of Software and TNLIST, Tsinghua University, Beijing, China. His research interests include WSNs and distributed systems.

![](images/8378017854ad68099b888391b27e04c6bf8cab61518d02e569ae11aa78b95bed.jpg)



Yunhao Liu (SM’06) received the B.S. degree from the Department of Automation, Tsinghua University, Beijing, China, in 1995 and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, East Lansing, MI, USA, in 2003 and 2004, respectively. He is currently a Chang Jiang Professor and the Dean of the School of Software at Tsinghua University.