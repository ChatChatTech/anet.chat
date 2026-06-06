# BOND: Exploring Hidden Bottleneck Nodes in Large-Scale Wireless Sensor Networks

Qiang Ma Kebin Liu Tong Zhu Wei Gong Yunhao Liu

School of Software and TNLIST, Tsinghua University

{maq, kebin, tong, gongwei, liu}@greenorbs.com

Abstract— In a large-scale wireless sensor network, thousands of sensor nodes periodically generate and forward data back to the sink. In our recent outdoor deployment, we observe that some bottleneck nodes can greatly determine other nodes’ data collection ratio, and thus affect the whole network performance. To figure out the importance of a node in data collection, the manager needs to understand the interactive behaviors among the parent and child nodes. To address this issue, we present a management tool BOND (BOttleneck Node Detector). We introduce the concept of Node Dependence to characterize how much a node relies on each of its parent nodes. BOND models the routing process as a Hidden Markov Model, and uses a machine learning approach to learn the state transition probabilities in this model based on the observed traces. BOND utilizes Node Dependence to explore the hidden bottleneck nodes in the network. Moreover, we can predict how adding or removing the sensor nodes would impact the data flow, thus avoid data loss and flow congestion in redeployment. We implement our tool on real hardware and deploy it in an outdoor system. Our extensive experiments show that BOND infers the Node Dependence with an average accuracy of more than 85%.

# I. INTRODUCTION

Wireless sensor networks (WSNs) have been applied in a large variety of application domains, from environment monitoring [10], [21], scientific observation [23], [26], habitat tracing [7], [15], to emergency detection [8], field surveillance [22], infrastructure protection [24], etc. In those applications, hundreds and thousands of sensor nodes are envisioned to be deployed in the target area, so as to generate and send the desired data back to the sink in a multi-hop manner. Most of those nodes are required to forward the data for others. That is, once some relay nodes crash or deplete their energy, the network could be separated, i.e., the sink can hardly retrieve data from some nodes far from it.

Understanding and exploring these hidden bottleneck nodes is of great importance for network management. For instance, when network separation happens, it is urgent for the network manager to track the data flow in the isolated region and figure out where the packets are lost. In practice, however, the network information required for fault diagnosis can be hardly retrieved from a disconnected area. Moreover, many applications, such as emergency detection and infrastructure protection, usually require quick recover from data loss. After detecting the hidden bottleneck nodes in a given network, we are able to provide recovery solution in realtime, as well as traffic prediction to guide redeployment thus avoid latent risk of data loss.

In this work, we design BOND, a framework that uses online measurements of network performance to infer the hidden bottleneck nodes which are most likely to cause network separation. Overall, BOND employs a methodology comprising three procedures: i) measurement collection, which gathers reports from each node consisting of some passive measurements; ii) inference, which infers the dependence between a node and each of its parents using the reported measurements. By considering all the nodes and their routing performance, BOND explores the most likely bottleneck nodes in the network; iii) prediction, which utilizes the inferred results to predict how adding or removing the sensor nodes in the current network will impact the data flow.

Particularly, we introduce the concept of Node Dependence to characterize the routing dependence between a node and its parent. How to compute Node Dependence for a given node and its parents is non-trivial. The main challenges are three-fold. First, routing performance varies with the routing strategies even in the same network. Different routing protocols are designed based on different metrics. For instance, Gnawali et al. [5] design Collection Tree Protocol (CTP), in which an estimate of the expected transmission (ETX) cost of each link are exploited. [18] claims that energy inefficiencies would shorten the lifetime of the network, therefore it leverages the node energy as the routing metric. Second, routing performance is influenced by many system factors, such as topology, network density, channel interference, even some unknown environmental conditions. Third, proactive retrieval of large amounts of information from the nodes may greatly impact the routing performance, thus deteriorate the back-end inference. Therefore, to avoid generating coupling effect with original application, the inference tool should inject as little traffic as possible.

We present a universal approach to infer Node Dependence under whatever routing protocols. We model the routing process as a Hidden Markov Model (HMM). For a given node, we describe a serial of collected packets as a state vector. Each state refers to the parent node which forwards the corresponding packet. As we can see, if two consecutive states are different, that means the node changes its parent. In this Markov model, the state transition probability represents the probability from one parent node to another. We claim that, if a node A strongly relies on one of its parents B for routing, then the probability for A to change its parent from B to others should be small, while the probability for A to change its parent from others to B should be large. Different with pure traffic analysis, Node Dependence is computed based on state transition probabilities. To learn this transition matrix and get the optimal approximation, we collect light-weight information passively from each node. After analyzing the dependence distribution for all the nodes, we can explore the hidden bottleneck nodes. In other words, once the network separates, it is most likely that some failures happen on these nodes, which should be carefully examined by the managers. Using the state transition probabilities, network managers can also predict how the data flow changes if some nodes are assumed to be added or removed in the network, which significantly improves the efficiency of redeployment.

![](images/8cd045d6453e15cc1c31e2a2a0415e04da2e8693e9a42034b02323ab05c13e76.jpg)



Fig. 1. An overlook on GreenOrbs deployment

The rest of this paper is structured as follows. Section II describes our motivation from two large-scale outdoor systems. We define Node Dependence, and present the framework of BOND in Section III. We develop a technique to infer the Node Dependence graph for each node, and combine the results to determine bottleneck nodes in Section IV. A flow prediction tool using Node Dependency is described in Section V. Section VI shows performance evaluation from real outdoor deployment. Finally, Section VII summarizes the related work, and Section VIII concludes the paper.

# II. MOTIVATION

This work is motivated from two ongoing WSN projects GreenOrbs and CitySee. GreenOrbs is a consistently operating sensor network system deployed for forest monitoring. Figure 1 plots the real topology. With up to 330 sensor nodes in the wild, GreenOrbs provides an excellent platform for observing sensor network behaviors at scale. During the deployment, we observed that, the sink always failed to retrieve the packets from some parts of the network. For instance, in early January 2010, 23.5% of nodes suddenly stopped sending their packets back. To troubleshoot the root cause, we expected to sample some diagnosis information from this area. Unfortunately, as the same as data packets, no more than 10% of diagnosis packets could be collected. What is more, it also proves difficult for the managers to keep sniffers overhearing and tracking data flow in such dangerous surroundings. Finally, the network was recovered after we rebooted 5 nearby nodes, which located by the river, and played a role of bridge to carry most of the data flow from the disconnected area.

In late May 2011, CitySee, an urban carbon dioxide sensing project, was deployed for carbon emissions monitoring. CitySee totally deploys 1196 nodes. To avoid making a node become the only routing option for some others, we carefully designed the node deployment according to the real road conditions. For instance, at the crossings we put enough nodes, so as to relay possible much data flow. We also considered the link quality in addition to network topology. In the surroundings with many trees or buildings, we properly added some relay nodes to mitigate the effect of signal barrier and multipath. Unfortunately, CitySee also experienced periodical data loss in 20% of deployed areas, and the network was recovered soon after we figured out the critical nodes and rebooted them.

So far, we realized that, to correctly identify which nodes are hidden bottlenecks to the network, it is quite necessary for the managers to analyze the routing performance at network layer. We sought to apply the state-of-the-art approaches in [17], [10], which simply define the nodes carrying much traffic flow as the network bottlenecks. In our experiments, however, even if these nodes are removed, the network still runs well. It is because, these nodes are mainly enforced to forward data by the protocols, which means they are usually selected as the first choice, but not always the only one. Instead, we quantize the dependence among the nodes based on the measurement of parent change events to describe how a node performs when one or more of its parents are unavailable. Specifically, we expect to design a universal approach, which is able to explore the hidden bottleneck nodes under any network configuration, so as to accurately guide the managers to recover the network in case some parts of data are lost.

![](images/22dc8adca7c0703923ad6d15f963e04f664e01ad75397a095d6a04266673140f.jpg)



(a) First hour after deployment

![](images/22024546534edd61c2558f31ad82ac525f823af0e3e6892e76e97b938511fed2.jpg)



(b) Twelve hours after deployment

![](images/514f959a70e8f496b6ea4c53f78f13a20ad146be4fce2797ab57383af9c7789a.jpg)



(c) One day after deployment

![](images/38fc07eb6cdac517f5bd2000fe3f7f0307460a3195af76a313ef4933292353e6.jpg)



(d) Five days after deployment   
Fig. 2. The varying frequency of parent change over time. We draw the node locations according to the real deployment. Each bar value represents the number of parent change in one hour for each node.

# III. THE BOND FRAMEWORK

According to deployment experiences, we have two basic observations. First, the network routing performance varies over time. Usually, as shown in Fig. 2, a node frequently changes its parent in the warm-up stage of routing protocol. After the routing map becomes stable, a node chooses its parent in a relative fixed routing table. In addition, although every node generates the same amount of packets in the network, only a few nodes are always required to forward others’ packets in the collection process. Second, the sensor nodes are regarded as error-prone and subject to component faults, performance degradations and even major system failures in real world deployments [9], [13], [17]. Moreover, a single node’s failure may cause a large amount of packet loss. The main object of BOND is to provide a universal approach to detect the hidden bottleneck nodes, under whatever system settings and routing protocols.

# A. The Node Dependence: How much a node relies on its parent for routing

In this section, we introduce a novel metric Node Dependence, which is used to quantize how much a node relies on its parent for routing. Regularly, a node is supposed to change its parent for the next packet when the current parent is unavaiable. Nevertheless, if this packet still can’t be sent through other parents, the sender could keep waiting for the original parent until it is able to work. This reminds us to compute the probability for a node to change its parent from one to another. Specifically, if a node strongly relies on one parent, then the probability for this node to change routing path from this parent to others should be relatively small, while large in reverse.

We first estimate parent transition probabilities for each node, then compute its local Node Dependence graph, finally identify the critical nodes. Node Dependence is inferred based on the measurements at network layer, therefore it is determined by the routing performance. Actually, the routing performance is influenced by many factors, such as network topology, routing protocol, link quality and so on. Therefore, if we conduct the inference only by exploring the node relationships in network topology, as mentioned in Section II, the analysis must be lack of considering the link quality, routing protocols, etc. Next are two examples to explain the impact of network topology, routing protocol and link quality to routing performance.

The impact of network topology. Let us consider the simple network topology depicted in Fig. 3(a). Before node E is deployed in the network, node A has only one parent A- , that is, all the data packets from A must be forwarded by A- . As a result, A must totally rely on A- . It is the same relationship for the other three pairs B and B- , C and C- , D and D- (the blue dotted lines). After node E is put among the nodes, the routing map changes. Node E shares Node Dependence with A- , B- , C- and D- . From the angle of node A, it has one more choice to send out its packets. Moreover, even if node A- crashes, the data packet can be retrieved at the sink through E and any of B- , C - , D- .

Nevertheless, under some certain routing protocols, all of {A, B, C, D} regard node E as the best parent, thus most of data flow from {A, B, C, D} will go through E, which may cause unexpected transmission delay. This phenomenon should be eliminated, so as to avoid unnecessary flow congestion and improve the network throughput. Using the graph of Node Dependence, we are able to show that node E really plays a critical role in data collection, hence we can redeploy the network as described in Fig. 3(b), where node E- shares the data flow from C and D.

The impact of routing protocol and link quality. In Fig. 4(a), node D is the parent of A and B, while node E is the parent of B and C. We assume that A and C have the same data rate. In energy-based protocol, to balance the residual energy of D and E, node B must distribute its data flow in average to both of its parents. On the other hand, it performs totally different in such link quality based protocols, like CTP. Assume that the quality of link (B, D) and (D, Sink) are much better than that of (B, E) and (E, Sink). Then node B must rely on D for routing more than E. If we consider a large set of nodes $\{ B _ { 1 } , B _ { 2 } , . . . , B _ { n } \}$ instead of node B, as shown in Fig. 4(b), there is still a latent risk of flow congestion at D. Moreover, once node D crashes, E is unable to forward packets from $\{ B _ { 1 } , B _ { 2 } , . . . , B _ { n } , C \}$ because of bad link quality.

![](images/91ac3a01cb639bcdc4763197c6aba1eda39b5dadd6b53d9b271991de527eb4c1.jpg)



(a)

![](images/00635dd653aa9a10574e6e574ebbea4e76f3db9ffe0f81416f83a262b8a97805.jpg)



Fig. 3. The impact of topology. (a): Node E changes the routing map, and carries overmuch flow. (b): Node E- shares some flow with node E.

# B. The Measurements

To infer the local graph of Node Dependence for each sensor node, BOND requires to collect related information from the network. There is a tradeoff between the amount of information and the estimation accuracy of Node Dependence. If it includes complete path traces for each packet, as well as the exact record for each parent change event, the manager could use these reports to construct a global graph, which clearly identifies what the data flow distribution is, and when parent change occurs. Similar to Heisenbug, however, proactive retrieval of a large amounts of information in a largescale network incurs huge transmission overhead, which may change the real data flow in the application, thus impact the back-end analysis [9]. For instance, the traces collected in[17] totally satisfy our requirements, therein each sensor node is required to periodically send a diagnosis report including the connectivity metrics, flow metrics and node metrics, about 80 bytes data.

1) Path Record: In contrast to such solutions that force each node to report a large amount of information periodically, we collect light-weight data passively from the nodes, by embedding the information into the application packets. To compute the distribution of Node Dependence for each node, say v, we expect to know the exact parent node of each packet transmitted by v, but not only the packets generated by v. It is because for most of nodes in the network, they forward much more data for its children than itself, thus our inference may lose its generality if we only consider the minority data flow. In practice, however, it incurs huge overhead if we record each forwarding nodes in the path, since a 20-hop path needs at least 40 bytes for a large-scale network. To address this issue, bloom filter is leveraged in BOND to record packet path.   
2) Bloom Filter: A space-efficient probabilistic data structure and always be used to examine whether an element exists in a set or not. A bloom filter is a bit array of m bits, originally all set to 0. Define k distinct hash functions, each of which maps the elements to one of the m positions in the array with a uniform random distribution. When an element is inserted into bloom filter, we feed it to those k hash functions and obtain k array positions, and set the bits at these positions to

![](images/2be19de9019cdee401d260a0798777c26b59507d9af861d63bd26ce9121156f2.jpg)



(a)

![](images/c0c3644a78db85592c0957b31aad7564266ea6e6b4c085addabfb718bf82685d.jpg)



(b)   
Fig. 4. The impact of protocol. (a): In quality-based protocol, node B relies on D more than E. (b): a latent risk of flow congestion at D.

1. To query for an element, first get k positions by feeding it to k hash functions, then check the bits at those positions. If any of the bits are 0, the element must not be in the set. Otherwise, either the element is in the set, or the bits have been set to 1 when other elements are inserted, resulting in a false positive.

Figure 5 shows an example of bloom filter, in which $m = 1 2$ and $k = 3 .$ . Element x,y and z are inserted into the bloom filter, while element u and v are not in the set. The colored arrows show the corresponding positions in the bit array. When we check any of $\{ x , y , z \}$ , the hashed bits are all set 1, and we say that they are in the set. To check u, we find that it hashes to one position containing 0, therefore we say that u is not in the set. It is noted that, however, false positives are possible. When we check v, the hashed positions are also occupied by $H _ { 1 } ( x )$ , $H _ { 1 } ( y )$ and $H _ { 3 } ( x )$ , then we make a mistake and say that v is also in the set.

In BOND, we put a 32-bit bloom filter, i.e., 4 bytes data into each packet, which is used to record the relay nodes in the path. In general, each application packet already contains the source node ID, therefore we start from the first relay node to the sink in the path. For instance, in Fig. 4(a), all the packets generated by node A must piggyback a bit array containing $H ( D )$ and $H ( S i n k )$ , where H denotes the set of hash functions. To node B, the bit arrays in its packets either includes H(D) and $H ( S i n k )$ , or $H ( E )$ and $H ( S i n k )$ , respectively represent two possible paths to the sink.

# IV. THE INFERENCE TOOL

As mentioned previously, before computing the Node Dependence graph for each node, we need to estimate parent transition probabilities based on collected traces. A Hidden Markov Model (HMM) [16] is a statistical Markov model in which the system being modeled as a Markov chain with unknown parameters, where the states of the Markov chain are not directly visible. HMM is especially known for their applications in temporal pattern recognition such as speech, handwriting recognition, musical score following, part-ofspeech tagging and partial discharges. In this work, we use HMM for inferring the parent transition probabilities.

![](images/2165fb46dc82ab3d72e8411cafbf1267001aeac972d6abffd59534374d8f252f.jpg)



Fig. 5. An example of bloom filter

# A. Network Model

We consider a single-channel wireless sensor network, and abstract it as a connected directed graph $G = \{ V , E \}$ , where the vertices V represent N sensor nodes and the edges E represent a link among the nodes. The existence of a directed link $( i , j ) \in E$ means that node j has forwarded node i’s packets, i.e., node j is one of node i’s parents. Note that, the sink has no outgoing edges, and there may exist loops in the graph, which means that the relationship of parent and child forms a loop within some nodes. We define the parent set of node i as $V _ { p } ( i ) ~ = ~ \{ P _ { i j } | ( i , j ) ~ \in ~ E \}$ . In real implementation, $V _ { p } ( i )$ is defined like the routing table maintained by node i. When node i has a packet to send, it chooses the best parent in current routing table according to the built-in routing protocol. In practice, the routing table’s size is usually limited by an upper bound, e.g., 10 in most applications. In this model we don’t limit the size of $V _ { p } ( i )$ , that is, all the parent-child pairs occur during the observation period are considered. We assume that this logical topology of the graph with respect to E is known to our inference tool, which can be achieved by passive online estimations [10]. In addition, every node v maintains a 2-byte counter $F ( v )$ to record its total traffic during the measurement period, and piggyback it in the application packets.

# B. Formal Specification and Learning

Overall, for each node v, we model its packet transmissions as a Markov chain. Suppose v has L packets to transmit, and $V _ { p } ( v ) = \{ P _ { v 1 } , P _ { v 2 } , . . . P _ { v N } \}$ , that is, v has N parent choices for each transmission. An event of parent change from $P _ { v i }$ to $P _ { v j }$ is described like: for packet s, node v chooses $P _ { v i }$ as the parent. When v intends to transmit packet $s + 1$ , the routing parameter changes, then v changes its parent from $P _ { v i }$ to $P _ { v j }$ according to current network conditions. That is also why we can model these processes as a Markov chain of length $L .$ Each state represents a possible parent node. Therefore, the state transition probabilities refer to the parent transition probabilities. As mentioned in section III-B1, we can’t directly observe which parent node is chosen for each packet. In this Markov model, these states are hidden.

![](images/c2f7e3a36aab4f58674f6d61e3f1504f6ee9bc62f36ebae969e2085f2f7226de.jpg)



(a)

![](images/d8149e5b813e7030fb842d3ef14b3a028f9df1cf644578e8b455eb3f14935d45.jpg)



Fig. 6. Filter out the nodes not in the path with bloom filter. (a): Only one path left after filtering out the nodes with bloom filter. (b): Two or more paths are possible.

For node v, we provide the complete formal specification of HMM using standard notations [16]. The HMM consists of the following:

Set $S _ { v }$ of N states, where $N = | V _ { p } ( v ) | + 1 . \ S _ { v } = \{ S _ { i } | i =$ $0 , 1 , 2 . . . N \}$ , and $\{ S _ { i } | i = 1 , 2 . . . N \} = \{ P _ { v i } | i = 1 , 2 . . . N \}$ and $S _ { 0 }$ represents a virtual state that this packet is not transmitted by v.   
• Set $T _ { v }$ of M observation symbols, where $M = 2 ^ { k }$ , and k is the length of bit-array in designed bloom filter, i.e., 32 in our experiments. $T _ { v } = \{ T _ { i } | i = 0 , 1 , 2 . . . M \}$ .   
• Matrix $A _ { v } = \{ a _ { i j } \}$ of state transition probabilities, where $a _ { i j } \ = \ P ( S _ { j } | S _ { i } ) , 1 \ \le \ i , j \ \le \ N$ , which represents the transition probability from $S _ { i } ~ \mathrm { t o } ~ S _ { j }$ . Note that $A _ { v }$ is unknown at the beginning and will be determined by training the sequences of observations.   
• Matrix $B _ { v } = \{ b _ { i j } \}$ of observation symbol probabilities, where $b _ { i j } = P ( \dot { T } _ { i } | S _ { j } ) , 1 \leq i \leq M , 1 \leq j \leq N$ , which represents the probability that observation is $T _ { i }$ for hidden state $S _ { j }$ . Section IV-C will give the computation details.   
• Vector $\pi _ { v } = \{ \pi _ { i } \}$ of the initial state distribution, where $\pi _ { i }$ is the probability of initial state being $S _ { i }$ . In this work, we simply set $\pi _ { i } = 1 / N , i = 1 , 2 . . . N$ .

# C. Computation of Observation Symbol Probabilities

The main object of computing the observation symbol probabilities is to determine the probability $T _ { i }$ for hidden state $S _ { j } ,$ , where $1 \leq i \leq M , 1 \leq j \leq N$ . In our case, $T _ { i }$ means the bit array in the packet, while $S _ { j }$ represents the parent who forwards this packet. If we calculate the probability only based on the topology and designed hash functions, what really happens would be omitted. Therefore, we combine the real traffic and collected bit arrays to compute the matrix $B _ { v }$ .

1. Node Filtering. As shown in Fig. 6(a), the packet is generated by A. If only based on network topology, there are 5 different paths from A to the sink. In bloom filter, the nodes are recorded in a bit array. After this packet arriving at the sink, we check the bit array and exclude the nodes which must not be in the path. In the example, we assume that node C and F are filtered out from the graph, then this packet must go through node B, $E ,$ finally to the sink.

2. Link Weight Assignment. As shown in Fig. 6(b), due to possible false positives in bloom filter, there may exist two reasonable paths from A to the sink after node filtering. When we analyze which parent node is chosen by A, the probability is divided equally by B and C, that is because only one path exists either from B or C to the sink. Actually, to compute the probability distribution for each relay node, we first assign a weight value to each link l, which equals to the number of paths go through l. Algorithm 1 formalizes the process. It is noted that, if we describe the graph as a tree rooted by the sink, Algorithm 1 runs from the root to the leaves.

Algorithm 1 . Link Weight Assignment   
1: Denote the weight value of a directed link (Source, Destination) as $L(\text{Source}, \text{Destination})$ .
2: For node $v$ , $o(v) = \sum_{u \in V_p(v)} L(v, u)$ .
3: For link $(u, v)$ ,
4: if $v = \text{Sink then}$ 5: $L(u, v) = 1$ .
6: else
7: $L(u, v) = o(v)$ .
8: end if

3. Probability Computation. Figure 7 shows an example to compute the weight value for each link. Assume that no node is excluded after the first stage. It is clear that there are 5 paths from A to the sink, in which 3 paths pass B and the others pass C. That is, for node A, this packet is sent to B for a probability of 60%, while 40% to C. Similarly, for node B, if B receives this packet from A, then for a probability of 66% B will send this packet to E. Note that this packet can be sent to C from the beginning, which means B does not receive this packet at all. That is why we introduce a virtual state $S _ { 0 }$ in the S. In addition, we must check every possible path, and make sure that the bit array produced by this path is as the same as what collected, otherwise this path should be eliminated from the set of solution. Algorithm 2 formalizes the process, which begins at the source node who generates the packet, finally to the sink.

4. Probability Conversion. Until now, we determine $P ( S _ { i } | T _ { j } ) , 1 \ \leq \ i \ \leq \ N , 1 \ \leq \ j \ \leq \ M$ for a given node v. We know that $\begin{array} { r } { P ( T _ { j } | S _ { i } ) = \frac { P ( S _ { i } | T _ { j } ) P ( T _ { j } ) } { P ( S _ { i } ) } . \ : \ : P ( T _ { j } ) } \end{array}$ P (Si|Tj )P (Tj ) . P (T ) can P (Si) be calculated by counting how many times $T _ { j }$ appears in the collected packets. To estimate $P ( S _ { i } )$ , we let each node v count its own transmissions $F ( v )$ (detailed in section IV-A). Therefore, when we compute the dependence graph

![](images/d04bb4fc03731e29e6103a14d0d3e66a8b2138d83bb182906ca2aa23beff2612.jpg)



Fig. 7. Second Stage: Compute the weight value for each link in the subgraph.

for node v, $\begin{array} { r } { P ( S _ { i } ) = F ( S _ { i } ) / { \sum _ { P _ { v j } \in V _ { p } ( v ) } F ( P _ { v j } ) } . } \end{array}$

# D. Computation of Node Dependence Graph

For node v, given the observation sequences $O _ { v } ,$ we learn the model parameters $\lambda _ { v } = ( A _ { v } , B _ { v } , \pi _ { v } )$ to maximize $P ( O _ { v } | \lambda _ { v } )$ , by using the well-known Baum-Welch method, which is based on the forward-backward algorithm [1]. Specifically, it is a 20-iteration process to determine the optimal $\lambda _ { v }$ (the iteration number can be set according to the trade-off between accuracy and time consuming). Note that we don’t readjust the matrix $B _ { v } .$ , since it has been well determined by our analysis in section IV-C. Actually the matrix $A _ { v }$ is what we concern. A large transition probability from $S _ { i }$ to $S _ { j }$ means that, in case $S _ { i }$ is not available, $S _ { j }$ may be chosen as the parent. In other words, if a node is considered as critical, the transition probability from others to itself must not be small. Therefore, we define the Node Dependence for node v to its parent $S _ { i }$ as: $\begin{array} { r } { D ( v , S _ { i } ) = \sum _ { 1 \leq j \leq V _ { p } ( v ) } a _ { j i } / | V _ { p } ( v ) | } \end{array}$ , i.e., the average value of transition probability from all the other parents to $S _ { i } .$ . The larger $D ( v , S _ { i } )$ is, the more important role $S _ { i }$ plays in $v ^ { \prime } { \mathrm { s } }$ transmissions.

Algorithm 2 . Probability Computation   
1: Denote this observation (bit array in this packet) as O.
2: For node v,
3: if v generates this packet then
4: $P(S_0|O) = 0.$ 5: $P(S_i|O) = \frac{L(v, P_{vi})}{\sum_{P_{vj} \in V_p(v)} L(v, P_{vj})}, i > 0.$ 6: else
7: $p_v = \sum_{u | v \in V_p(u)} P(v|O).$ 8: $P(S_0|O) = 1 - p_v.$ 9: $P(S_i|O) = \frac{p_v \cdot L(v, P_{vi})}{\sum_{P_{vj} \in V_p(v)} L(v, P_{vj})}, i > 0.$ 10: end if

# V. THE PREDICTION TOOL

After locating the bottleneck nodes in the network, the managers are able to give a quick solution when some parts of nodes separate from the network. For many reasons, such as severe interference, network partition, sensor hardware failure and so on, sometimes the managers need to add or remove some sensor nodes in the existing network topology. In addition to network diagnosis, BOND is able to provide guidelines to the network redeployment, by predicting the variation of data flow when the network topology changes. In this section, we explain how we predict the data flow changes after only one node is added or removed, and the process repeats if more nodes are concerned.

# A. Removing Sensor Nodes

Suppose node v is going to be removed. Note that if v is critical to some other nodes, like $v ^ { \prime } , { \mathrm { e . g . , ~ } } D ( v ^ { \prime } , v ) > 8 0 \% , v ^ { \prime }$ may be totally separated from the network. Our experiments will discuss this case. The next prediction focuses on the cases without any critical node. For each child node of $v ,$ say u, we first compute how many packets are sent to v. With learned HMM $\lambda _ { u } = \left( A _ { u } , B _ { u } , \pi _ { u } \right)$ and observation sequence $T _ { u } ,$ , we can generate the hidden states $S _ { u }$ which has the highest probability using the Viterbi algorithm. Note that $S _ { u }$ means the series of chosen parent for transmitted packets. Then we are able to compute the ratio of $v ,$ denoted as $R _ { u v }$ . Multiplying $R _ { u v }$ by $F ( u )$ , we get the packets transmitted from u to v:

$$
T P (u, v) = R _ {u v} \cdot F (u) \tag {1}
$$

Next step is predicting where these packets will be sent to if v is not in the network by using the transition probability learned in section IV (without loss of generality, next we assume $v = P _ { u 1 } )$ :

$$
D P (u, P _ {u k}) = T P (u, v) \cdot a _ {1 k} / \sum_ {j \neq 1} a _ {1 j}, \quad k \neq 1 \tag {2}
$$

Where $a _ { 1 j } \ \in \ A _ { u } .$ As we can see, for each of $u ^ { \prime } \mathrm { s }$ other parents, say $P _ { u k }$ , its data flow increases because it requires to deliver ${ D P } ( u , P _ { u k } )$ packets which originally were transmitted by v. Therefore, we also need to consider how this increment be collected to the sink. For simplicity, denote $P _ { u k }$ as w. For each of w- s parents, say t, we first compute the ratio of packets from w to t with Viterbi algorithm, then $t ^ { \prime } \mathrm { s }$ increment can be computed:

$$
D P (w, t) = D P (u, w) \cdot R _ {w t} / \sum_ {i} R _ {w i} \tag {3}
$$

Further, equation 3 repeats until the increment packets arrive at the sink. Note that node w and u can be parent node of each other in a real network. When we are considering the $w ^ { \prime } \mathrm { s }$ increments caused by u, we remove u from w- s parent set, to make sure convergence of our algorithm. Moreover, this consideration excludes the routing loop.

Finally, the decrement data flow of $v ^ { \prime } \mathrm { s }$ parents caused by removing v should be concerned. Similarly, for any of $v ^ { \prime } { \mathrm { s } }$ parents s, we compute the distribution of packet ratio from s to its parents, then decrease the data flow in proportion, like what we deal with increments in equation 3. As the same, the process is repeated until the decrements arrive at the sink.

# B. Adding Sensor Nodes

Different with removing sensor nodes, our prediction of data flow changes after adding sensor nodes is based on the knowledge of physical topology. In fact, a redeployment work usually satisfies this requirement. Suppose node v is going to be added into the network. Find a node $v ^ { \prime }$ which is closest to v within its communication range. Then we predict the data flow changes by treating v as the same as $v ^ { \prime } .$ For each child node of $v ^ { \prime } ,$ say $u ,$ which also locates within $v ^ { \prime } \mathrm { s }$ communication range. We first modify $\lambda _ { u } = ( A _ { u } , B _ { u } , \pi _ { u } )$ .

• For $A _ { u } = \{ a _ { i j } \}$ , where $1 \leq i , j \leq N$ , we add a row and a column for v, because u has one more parent option. Without loss of generality, we assume $\ v { v } ^ { \prime } = \ P _ { u N }$ and $v = P _ { u ( N + 1 ) }$ . Then we change $a _ { i j }$ to $a _ { i j } ^ { \prime }$ as follows:

$$
a _ {i j} ^ {\prime} = \left\{ \begin{array}{l l} a _ {i j} / (a _ {i N} + 1) & \text { if } 1 \leq i \leq N, 1 \leq j \leq N \\ a _ {i N} / (a _ {i N} + 1) & \text { if } 1 \leq i \leq N, j = N + 1 \end{array} \right.
$$

Finally let $a _ { ( N + 1 ) j } ^ { \prime } = a _ { N j } ^ { \prime } , 1 \le j \le ( N + 1 )$ .

• For $B _ { u } = \{ b _ { i j } \}$ , where $1 \leq i \leq M , 1 \leq j \leq N$ , we add a column for v. Then we make $b _ { i ( N + 1 ) } = b _ { i N } , 1 \leq i \leq M$   
• For $\pi _ { u } = \pi _ { i } , 1 \le i \le N$ , we change $\pi _ { i }$ to $\pi _ { i } ^ { \prime }$ as follows:

$$
\pi_ {i} ^ {\prime} = \left\{ \begin{array}{l l} \pi_ {i} / (\pi_ {N} + 1) & \text { if } 1 \leq i \leq N \\ \pi_ {N} / (\pi_ {N} + 1) & \text { if } i = N + 1 \end{array} \right.
$$

Next we verify that our modification is reasonable and satisfies the requirement of HMM setting:

$$
\begin{array}{l} \sum_ {1 \leq j \leq N + 1} a _ {i j} ^ {\prime} = a _ {i (N + 1)} ^ {\prime} + \sum_ {1 \leq j \leq N} a _ {i j} ^ {\prime} \\ = \frac {a _ {i N}}{a _ {i N} + 1} + \frac {\sum_ {1 \leq j \leq N} a _ {i j}}{a _ {i N + 1}} = 1 \\ \end{array}
$$

Similarly, $\begin{array} { r } { \sum _ { 1 \leq i \leq N + 1 } \pi _ { i } ^ { \prime } = 1 ; } \end{array}$ and

$\begin{array} { r } { \sum _ { 1 < i < M } b _ { i ( N + 1 ) } = \sum _ { 1 < i < M } b _ { i N } = 1 } \end{array}$ . Note that HMM $\lambda _ { u }$ needs to be recomputed (as shown in section IV-C) for a new process of detecting hidden bottleneck nodes, because the topology changes. After the modification, we compute and deal with the increment data flow and decrement data flow, like what we do in the cases of removing sensor nodes.

# VI. EVALUATION

In this section, we validate the performance of BOND. The data set used for analysis and evaluation mainly comes from the operational period of CitySee in September, 2011, which totally counts 865901 data packets. In CitySee, we set the data rate of application packet as one packet per ten minutes for each node (more details about system settings of CitySee are described in [14]). In addition, to provide ground truth in our experiments, we also record the packet path for some nodes close to the sink. Our evaluation contains three parts. First we take a field study in GreenOrbs and discuss why BOND needs to reduce collection overhead to guarantee network performance. Then we evaluate two tools. One is about the inference model, which is used to compute the Node Dependence graph for each node. The other is the prediction tool, which predicts the traffic change after the network is redeployed.

![](images/f343581db4267f5b191ca39e12ec311c01b38e06b8598263757034a836e15a73.jpg)  
Fig. 8. Packet collection of node 0-60 during 1 hour in GreenOrbs

![](images/adae0c160ed6fc6a07991190828f17b272caa83faa41670311808cbd828f7e70.jpg)



Fig. 9. Network yield during 10 hours

![](images/55d8c4095533a9ea62203916b23dec5ba18577df28d6133c43e17b0c5de5dd40.jpg)



Fig. 10. Accuracy rate V.S. distance to the sink

![](images/1bf76017650b2d4636f2396e9549f40b165817e2493cd0bfed5aa58814cfc477.jpg)



Fig. 11. Accuracy rate V.S. parent number

# A. Collection Overhead

In GreenOrbs, every node is required to send two packets per hour back to the sink, i.e., sensing packet and status packet. Sensing packet contains the sensing data by the need to monitor forest, while status packet is indeed necessary for network managers to maintain the system. In this experiment, we try to record path for all the packets, by injecting another kind of packet, i.e., path packet, into the network. Figure 8 describes the packet collection of node 0-60 during 1 hour. In normal conditions, three packets are ”bundled” and arrive at the sink (in the first 15 minutes). This out-of-band approach, however, may significantly impact the application itself. As shown in the grey zone, most of sensing packets fail to be collected, even though almost all of path packets and status packets arrive at the sink. It is because, the sensing packet and status packet contain about 50 bytes and 60 bytes data respectively, while the size of a path packet can at most rise to 70 bytes to record 25 hops. Therefore, the task of forwarding path packet consumes large amount of bandwidth, especially for the nodes far away from the sink. Figure 9 directly depicts the network yield, which is defined as the Packet Receive Ratio(PRR) of sensing packets at the sink. As we can see, the network yield is very unstable. In the best case, the sink successfully receives up to 94% of sensing packets, while the accordingly network yield of Fig.8 is only 0.9%. To address this issue and mitigate the coupling effect generated by BOND, we choose to encode a 4-byte bit array for path record and maintain a 2-byte traffic count (detailed in section III-B).

# B. Inference Model

As mentioned in section IV, we passively collect the observation series by using bloom filter to record the paths. Then we infer the parent sequence (i.e., the hidden state sequence), and the state transition probabilities in HMM model. Two network factors mainly influence the inference accuracy of parent sequence. One is the distance to the sink, represented by hop count. If a node is far from the sink, its packets potentially have many paths to the sink, thus increase the false positive rate when we exploit the bloom filter. Figure 10 shows the CDF distribution of accuracy rate. Here we define the accuracy rate as follows: if a node transmits M packets, and BOND correctly infers N parents for these packets, then the accuracy rate is N/M. We group the instances according to different hop counts from sensor nodes to the sink. In the nodes within 3 hops, more than 50% of them have accuracy rate of 85.2%. As expected, the accuracy rate decreases for the nodes farther from the sink. BOND, however, still accurately infers 77.6% parents of the packets for half of the sensor nodes, which at least locate 11 hops from the sink.

The other critical factor is the number of potential parents. It is easy to understand that, if a node only has one parent to choose, then we exactly know the parent for each packet transmitted by this node. By contrast, a large set of parents must introduce error estimate to the bloom filter. As we can see in Fig. 11, BOND successfully achieves an accuracy rate of nearly 90.0% for 60% of nodes which at most have 3 parents. Compare to the factor of distance, the impact caused by parent number is greater. For those nodes which have more than 3 but less than 11 parents, the accuracy rate is at least

![](images/36a549018e5d4090b95a696446aa3dc6ab9c46dae85f6f02916c1c389c4f0e44.jpg)



![](images/4f7c2adb34897f4b4ea6f2d7befa1290990f0ee19d3c4b8beb78aba99f694912.jpg)



![](images/fd337882f0789578176e7a84a947ef6e3c87981b2c35cabdb4a5f089a236fa62.jpg)



Fig. 12. A real case of hidden bottleneck node 40 Fig. 13. Prediction Accuracy V.S. Hop Count after Fig. 14. Prediction Accuracy V.S. Hop Count after a node is removed a node is added

74.3%, and 85.7% at average. While the number of potential parents increases to more than 14, the accuracy rate fall down to 65.4%, and no more than 85%.

To verify the parent transition probabilities, we take a real case in the network. In Fig. 12, we can see the real topology around node 40. Our data set displays that, failure of node 40 causes that a large amount of nodes are separated from the network, including node 48, 56, and etc. We compute the Node Dependence graph for those nodes, and find that all of their Node Dependence value to node 40 are more than 0.6, and node 80 even has a Node Dependence of 0.92 to node 40. In other words, once the managers observe these separated nodes, they can easily find out the bottleneck nodes according to these high Node Dependence values. Noted that this separation phenomenon can extend to the edge of network. In this example, we also find that the Node Dependence value from node 90 to node 80 is 30%. So once node 40 fails, node 80 also fails to forward data for the others, which further makes them disconnected with the network.

# C. Prediction Tool

To verify the prediction tool, we manually remove and add a node in the network, then compare the real traffic change and our prediction results. In section V, our prediction process starts from the 1-hop neighbors, then gradually extends to the farther nodes finally to the sink. So we mainly investigate the performance of nodes which locate at different hop counts. Figure 13 shows the CDF distribution of absolute value of relative error. The absolute value of relative error is computed as follows: Assume the traffic at one node is $T _ { 1 }$ and $T _ { 2 }$ respectively before and after the redeployment. BOND predicts the traffic changes to T3, then ( T3−T1 T2−T1 )/ T2−T1 = T3−T2 $T _ { 3 }$ $\begin{array} { r } { \big ( \frac { T _ { 3 } - { \bf \ddot { T } } _ { 1 } } { T _ { 1 } } - \frac { T _ { 2 } - T _ { 1 } } { T _ { 1 } } \big ) / \frac { T _ { 2 } - { \bf \dot { T } } _ { 1 } } { T _ { 1 } } = \frac { T _ { 3 } - T _ { 2 } } { T _ { 2 } - T _ { 1 } } } \end{array}$ − is what we need. As we can see, three kinds of nodes perform nearly the same, i.e., 25% averagely. The main reason is that, the farther nodes from the removed node is close to the sink, their parent number is limited, which greatly benefits our inference, thus counteract the potential accumulative error in the algorithm. In addition, our algorithm may produce a inaccurate result when we remove a critical node. An example is shown in Fig. 12, though these nodes don’t totally rely on node 40, they all fail to send their packets back to the sink once node 40 is crashed. Figure 14 depicts similar trends for 3 kinds of nodes when we add a node into the network. Noted that BOND performs reliably because adding a node will not break the connectivity of the network.

# VII. RELATED WORK

A number of practical operated network deployments have been reported during the last decade. They also conduct exact performance measurements in these systems. These studies show important observations and guidelines to the protocol design and implementation. To our best understanding, WSNs are not totally reliable for many real applications yet, due to a lot of systematic and environmental factors. That is why network diagnosis and measurement have been extensively studied in recent years.

# A. Sensor Network Measurement

It proves difficult that we simulate all systematical conditions perfectly and predict every network characteristics in the real deployment. Werner-Allen et al. [23] analyze packet loss performance and propose some hypotheses of the causes, e.g. equipment dropout, weather condition and temperature fluctuations. Zhao et al. [27] study packet delivery performance measurement with a medium-sized sensor network in three kinds of different environments. Liu et al. [10] report a measurement study of a large-scale sensor network GreenOrbs in the forest. The authors in [19] explore metrics that shed light on when and why opportunistic routing and network coding protocols perform well or badly. [20] finds that most intermediate links are bursty, i.e, they shift between poor and good delivery.

# B. Sensor Network Diagnosis and Management

Existing diagnosis approaches can be broadly divided into two categories: debugging tools and inference schemes. This work belongs to the later category. Claivoyant [25] and Declarative Tracepoints [2] are two notable tools which focus on debugging sensor nodes at the sourcelevel, and enables developers to wirelessly connect to a remote sensor and execute debugging commands. Existing inference schemes of diagnosis for WSNs like Sympathy [17] periodically collects network information from individual sensor nodes to sink. DustDoctor [6] troubleshoots sensor data fusion systems, by adapting discriminative mining algorithms to analyze provenance graphs, and isolate sources and conditions correlated with anomalous results. LiveNet [3] provides a set of techniques and tools for rebuilding complex dynamics of live sensor networks. To minimize the collection overhead, some researchers propose to establish certain inference models by marking the data packets [13]. Self-diagnosis [9] injects a finite state machine into each sensor node, enabling them to accordingly change the diagnosis state. [11] presents a localdiagnosis approach, which conducts diagnosis process in a local area through distributed evidence fusion operations. [4] minimizes the charging delay in RFID-based wireless sensor node by planning a movement strategy of reader. [12] presents a light-weight and passive approach for faulty link detection. In contrast with those approaches, this work mainly aims to point out the bottleneck nodes after a network is deployed, so as to provide a realtime recovery strategy when network failures occur.

# VIII. CONCLUSION

Network separation becomes a critical issue for large-scale wireless sensor networks. A large amount of data loss greatly impacts the application performance, as well as results in insufficiency of evidence for network diagnosis and management. In our two real outdoor deployments GreenOrbs and CitySee, we observe that there must exist some bottleneck nodes in the network, which greatly determine other nodes’ data collection ratio. To figure out to what extent each sensor node is responsible for the process of data collection, this work presents a management tool BOND to detect these bottleneck nodes. Meanwhile, we introduce a concept of Node Dependence to characterizes how much a node relies on each of its parent nodes. We also develop a technique based on Hidden Markov Model to infer the Node Dependence graph for each node. In addition to detection of bottleneck nodes, Bond is able to predict how adding or removing the sensor nodes would impact the data flow, thus avoid data loss and flow congestion.

# ACKNOWLEGMENT

Thank the anonymous reviewers for their constructive comments. This research is supported in part by the NSFC Distinguished Young Scholars Program under Grant No. 61125202, and the NSFC under Grant No. 61103187.

# REFERENCES

[1] L.E. Baum and JA Eagon. An inequality with applications to statistical estimation for probabilistic functions of markov processes and to a model for ecology. Bull. Amer. Math. Soc, 73(3):360–363, 1967.   
[2] Q. Cao, T. Abdelzaher, J. Stankovic, K. Whitehouse, and L. Luo. Declarative tracepoints: a programmable and application independent debugging system for wireless sensor networks. In Proceedings of ACM SenSys, 2008.

[3] B. Chen, G. Peterson, G. Mainland, and M. Welsh. Livenet: Using passive monitoring to reconstruct sensor network dynamics. In Proceedings of IEEE DCOSS, 2008.   
[4] L. Fu, P. Cheng, Y. Gu, J. Chen, and T. He. Minimizing charging delay in wireless rechargeable sensor networks. In Proceedings of IEEE INFOCOM, 2013.   
[5] O. Gnawali, R. Fonseca, K. Jamieson, D. Moss, and P. Levis. Collection tree protocol. In Proceedings of ACM SenSys, 2009.   
[6] M. M. H. Khan, H. Ahmadi, G. Dogan, K. Govindan, R. K. Ganti, T. Brown, J. Han, Mohapatra P., and Abdelzaher T. F. Dustdoctor: A self-healing sensor data collection system. In Proceedings of ACM/IEEE IPSN, 2011.   
[7] J. Kong, J. Cui, D. Wu, and M. Gerla. Building underwater adhoc networks and sensor networks for large scale real-time aquatic applications. In Proceedings of IEEE MILCOM, 2005.   
[8] M. Li and Y. Liu. Underground coal mine monitoring with wireless sensor networks. ACM Transactions on Sensor Networks, 5(2):10, 2009.   
[9] K. Liu, Q. Ma, X. Zhao, and Y. Liu. Self-diagnosis for large scale wireless sensor networks. In Proceedings of IEEE INFOCOM, 2011.   
[10] Y. Liu, Y. He, M. Li, J. Wang, K. Liu, L. Mo, W. Dong, Z. Yang, M. Xi, J. Zhao, et al. Does wireless sensor network scale? a measurement study on greenorbs. In Proceedings of IEEE INFOCOM, 2011.   
[11] Q. Ma, K. Liu, X. Miao, and Y. Liu. Sherlock is around: Detecting network failures with local evidence fusion. In Proceedings of IEEE INFOCOM, 2012.   
[12] Q. Ma, K. Liu, X. Xiao, Z Cao, and Y. Liu. Link scanner: Faulty link detection for wireless sensor networks. In Proceedings of IEEE INFOCOM, 2013.   
[13] E. Magistretti, O. Gurewitz, and E. Knightly. Inferring and mitigating a link’s hindering transmissions in managed 802.11 wireless networks. In Proceedings of ACM MobiCom, 2010.   
[14] X. Mao, X. Miao, Y. He, T. Zhu, J. Wang, W. Dong, X. LI, and Y. Liu. Citysee: Urban co2 monitoring with sensors. In Proceedings of IEEE INFOCOM, 2012.   
[15] L. Mo, Y. He, Y. Liu, J. Zhao, S.J. Tang, X.Y. Li, and G. Dai. Canopy closure estimates with greenorbs: Sustainable sensing in the forest. In Proceedings of ACM SenSys, 2009.   
[16] L.R. Rabiner. A tutorial on hidden markov models and selected applications in speech recognition. Proceedings of the IEEE, 77(2):257– 286, 1989.   
[17] N. Ramanathan, K. Chang, R. Kapur, L. Girod, E. Kohler, and D. Estrin. Sympathy for the sensor network debugger. In Proceedings of ACM SenSys, 2005.   
[18] C. Schurgers and M.B. Srivastava. Energy efficient routing in wireless sensor networks. In Proceedings of IEEE MILCOM, 2001.   
[19] K. Srinivasan, M. Jain, J.I. Choi, T. Azim, E.S. Kim, P. Levis, and B. Krishnamachari. The κ factor: Inferring protocol performance using inter-link reception correlation. In Proceedings of ACM MobiCom, 2010.   
[20] K. Srinivasan, M.A. Kazandjieva, S. Agarwal, and P. Levis. The β- factor: measuring wireless link burstiness. In Proceedings of ACM SenSys, 2008.   
[21] G. Tolle, J. Polastre, R. Szewczyk, D. Culler, N. Turner, K. Tu, S. Burgess, T. Dawson, P. Buonadonna, D. Gay, et al. A macroscope in the redwoods. In Proceedings of ACM SenSys, 2005.   
[22] P. Vicaire, T. He, Q. Cao, T. Yan, G. Zhou, L. Gu, L. Luo, R. Stoleru, J.A. Stankovic, and T.F. Abdelzaher. Achieving long-term surveillance in vigilnet. ACM Transactions on Sensor Networks, 5(1):9, 2009.   
[23] G. Werner-Allen, K. Lorincz, J. Johnson, J. Lees, and M. Welsh. Fidelity and yield in a volcano monitoring sensor network. In Proceedings of OSDI, 2006.   
[24] N. Xu, S. Rangwala, K.K. Chintalapudi, D. Ganesan, A. Broad, R. Govindan, and D. Estrin. A wireless sensor network for structural monitoring. In Proceedings of ACM SenSys, 2004.   
[25] J. Yang, M.L. Soffa, L. Selavo, and K. Whitehouse. Clairvoyant: a comprehensive source-level debugger for wireless sensor networks. In Proceedings of ACM SenSys, 2007.   
[26] D. Zhang, T. He, F. Ye, R. Ganti, and H. Lei. Eqs:neighbor discovery and rendezvous maintenance with extended quorum system for mobile sensing applications. In Proceedings of ICDCS, 2012.   
[27] J. Zhao and R. Govindan. Understanding packet delivery performance in dense wireless sensor networks. In Proceedings of ACM SenSys, 2003.