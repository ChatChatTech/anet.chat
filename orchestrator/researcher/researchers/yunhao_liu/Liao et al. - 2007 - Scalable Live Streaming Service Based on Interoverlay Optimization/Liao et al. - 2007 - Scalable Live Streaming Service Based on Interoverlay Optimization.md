# Scalable Live Streaming Service Based on Interoverlay Optimization

Xiaofei Liao, Member, IEEE, Hai Jin, Senior Member, IEEE, Yunhao Liu, Senior Member, IEEE, and Lionel M. Ni, Fellow, IEEE

Abstract—In order to provide scalable live streaming services, we propose an Interoverlay Optimization scheme, IOO. Instead of selecting better paths in the same overlay, IOO constructs efficient paths using peers in different overlays so as to 1) improve global resource utilization of peer-to-peer (P2P) streaming networks, 2) assign resources based on their locality and delay, 3) guarantee streaming service quality by using the nearest peers, even when such peers might belong to different overlays, and 4) balance the load among the group (streaming overlay) members. We compare the performance of IOO with existing approaches through trace-driven simulations. Results show that IOO outperforms previous schemes in terms of resource utilization and the quality of service (QoS) of streaming services. The IOO scheme has been implemented in an Internet-based live streaming system, called AnySee. AnySee was successfully released in the summer of 2004 in the China Educational Research Network (CERNET). More than 60,000 users enjoy massive entertainment programs, including TV programs, movies, and academic conferences videos.

Index Terms—Peer-to-peer, live streaming, interoverlay optimization, start-up delay, P2P topology discovery.

# 1 INTRODUCTION

WITH the improvement of network bandwidth, multi- media services based on streaming live media have gained much attention. Significant progress has been made on the efficient distribution of live streams in a real-time manner over a large population of spectators with good QoS [8], [9]. Due to the practical issues of routers, IP multicast has not been widely deployed. Therefore, researchers have expended a lot of effort in building efficient overlay multicast schemes based on peer-to-peer (P2P) models, in which spectators behave as routers for other users. Scalable live streaming overlay constructions [5] have become a hot topic. Different from traditional distributed systems, streaming overlays focus on the following four metrics: start-up delay, the delay to display the first image for users, including the logical media dada transmission time and decoding preparing time; source-to-end delay, the delay to receive the first media data block directly or indirectly from the source; playback continuity, the number of segments that arrive before playback deadlines over the total number of the segments; and resource utilization, the ratio between the used bandwidth to the total bandwidth. These metrics have a direct bearing on the interactive usability of a live streaming system. Large delays would exhaust user patience and unplanned interruptions will spoil the entertainment value.

. X. Liao and H. Jin are with the School of Computer Science and Technology, Huazhong University of Science and Technology, Wuhan, China. E-mail: {xfliao, hjin}@hust.edu.cn.   
. Y. Liu and L.M. Ni are with the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Kowloon, Hong Kong. E-mail: {liu, ni}@cse.ust.hk.

In order to improve the above metrics, previous studies [6] focused on intraoverlay optimizations, in which each node joins at most one overlay. With the help of localityaware strategies [7] and optimization schemes such as DONet in Coolstreaming [8] and Narada in End System Multicast (ESM) [9], the QoS of live streaming P2Ps have significantly improved. Nevertheless, they still suffer from a long delay and unplanned interruptions, especially when a large number of peers join the network simultaneously.

Fig. 1 shows an example of intraoverlay optimization with two logical streaming overlays. Peers A, B, C, and D join the stream originating at $\mathrm { S } _ { 1 } ,$ and peers E, F, G, H, and K join the stream originating at S2. The number on each edge represents the cost of the link between two nodes. In traditional intraoverlay optimization schemes, two multicast trees are established as shown in Figs. 1a and 1b, respectively. There are two obvious drawbacks. First, such overlay construction is not globally optimal. Considering peer D in Fig. 1a, the cost of $S _ { 1 }  D$ is 8, whereas if path $S _ { 1 } \stackrel { } {  } S _ { 2 }  D$ is used, the cost is only 4. Second, the resource utilization of traditional approaches is relatively low and imbalanced. The resources of edge peers cannot be utilized to provide services for other peers. Most of the existing protocols are tree based. Consequently, all leaf nodes fail to contribute any bandwidth or CPU cycles to the multicast trees.

We propose an interoverlay optimization scheme, IOO, in which resources can join multiple overlays simultaneously so as to

1. improve the global resource utilization of a P2P live streaming network,   
2. assign resources based on their locality and delay,   
3. guarantee streaming service quality by using the nearest peers, even if such peers might belong to different overlays, and   
4. balance the load among the group (streaming overlay) members to avoid the traffic bottlenecks.

![](images/dccfb3729f6bd01b83498dc840bfd39414cf24635757610ca39ac4cc04849342.jpg)



Fig. 1. Intraoverlay optimization. (a) Optimal multicast tree rooted at S1. (b) Optimal multicast tree rooted at $\mathrm { S _ { 2 } } .$ (c) Physical topology.

After IOO optimization on the example shown in Fig. 1, better overlays can be constructed as illustrated in Fig. 2.

For a distributed approach like IOO, however, to reach the above design goal without global network knowledge is not trivial. Several key issues, including efficient neighbor discovery, resource assignment, overlay construction, and optimization, must be addressed.

To prove the effectiveness of the IOO scheme, we conduct comprehensive trace-driven simulations based on topologies obtained from real P2P networks. Results show that the IOO scheme outperforms previous schemes in resource utilization and the streaming QoS. A public implementation, AnySee v1.1 [2], was released in June 2004. It has been used to broadcast live streaming media, including TV programs, movies, and the 2004 International Conference on Grid and Cooperative Computing (GCC) held in Wuhan, China, to tens of thousands of end users in the China Education and Research Network (CERNET). During the last months (till March 2006), over 60,000 users from 40 universities and 20 cities in China have tested AnySee streaming services. The source-to-end delay, resource utilization, and the start-up delay were all quite encouraging.

The rest of this paper is organized as follows: Section 2 discusses the related work. Section 3 presents the interoverlay optimization and IOO. Section 4 describes our simulation methodology and performance analysis. We describe implementation experiences and show our observations and measurements on AnySee in Section 5. We conclude this work in Section 6.

# 2 RELATED WORK

Many efforts have been made in the field of P2P live streaming system design. The most important issue of such schemes is to design a streaming overlay with high service quality and good scalability. In general, there are three types of schemes for optimizing live streaming overlays: tree-based [12], [13], mesh-based [8], [15], [19], and hybrid overlays [20], [21].

# 2.1 Tree-Based

Borrowing ideas from IP multicast, tree-based protocols are simple and easy to implement. The main target of the tree-based approach is to construct overlay spanning trees directly—that is, members explicitly select their parents from the members they know. There are two types of tree-based protocols: single-tree protocols such as ESM, Application Level Multicast Infrastructure (ALMI) [13], NICE [17], and ZIGZAG [16], and multiple-tree protocols such as SplitStream [10], Bullet [11], and multiple description coding (MDC) [12].

![](images/da69d90c76c2c852ae690271956ad6ce1171e0ecadf77dd9466d1812b1fcf27f.jpg)



Fig. 2. IOO: interoverlay optimization.

Single-tree protocols focus on building a scalable multicast spanning tree with high efficiency. In ESM, nodes are organized into an overlay tree over the existing IP network, and streaming data are distributed along the tree. The bandwidth requirement for a media server is shared among the peering nodes so as to reduce the burden of the media server. In ESM, the leaf nodes of a distribution tree only receive streaming media and do not contribute to the content distribution. ALMI [13] employs a topology-maintaining center to collect the topology information of trees. Any peer intending to join a group must first contact the center to get the corresponding group information and then choose one as its parent. NICE [17] and ZIGZAG [16] first organize peers into different logical layers. All peers belonging to the zeroth layer are divided into different clusters via their network locations. One leader is selected from a cluster in the layer i and automatically becomes the member of a cluster in the layer i þ 1. The source is the leader of the highest layer. Clearly, no leaf peer supports services for others. Considering that the “upstream” bandwidth of one peer on the Internet is limited in general, the resources, especially bandwidth, of some leaf peers in these systems are underutilized.

Multiple-tree protocols emphasize the overall resilience and the load balance of the entire streaming network. The main idea is to divide the video of one stream into several parts based on the “layer concept” in CoopNet or patching ideas [18]. The leaving or crash behavior of upper layer nodes, however, often causes buffer underflow. They also fail to provide backup services and waste spare resources.

# 2.2 Mesh-Based

In mesh-based protocols, peers accept media data from multiple “parents,” as well as provide services for multiple “children,” such as Coolstreaming [8], PROMISE [15], and GNUStream [19]. For example, PROMISE [15], based on CollectCast, operates at the application level, but also infers and exploits properties including the topology and performance of the underlying network. CollectCast reflects the P2P philosophy of dynamically and opportunistically aggregating the limited capacity of peers to perform streaming tasks traditionally performed by media servers. The resource utilization of a mesh is higher than that of a tree. Meshes based on the Gossip protocol can find fresh peers in the single mesh with low management overhead but not in global P2P networks. Due to the random algorithm for neighbors’ selection, the start-up delay cannot be guaranteed. Also, to decrease the impact from the autonomy of peers, a large buffer space, as used in Coolstreaming [8], is often necessary.

![](images/7aa394f816ad495d90f3c3960b2f451fc87f4c1d08593fad733219e73b25eab8.jpg)



Fig. 3. Concept structure of IOO.

# 2.3 Hybrid Overlays

Zhang et al. proposed a distributed hash table (DHT)-based P2P resource pool, the Self-Organized Metadata Overlay (SOMO) [20], to manage global resources and optimize multiple Application Layer Multicast (ALM) sessions. The main idea is to structure all peers strictly [21], ignoring the features of specific applications. The huge maintenance overhead, however, makes these approaches far from scalable. Indeed, even if we have global knowledge of a P2P network, finding an optimal assignment of resources is NP-hard.

Based on a completely distributed heuristic, our proposed IOO scheme selects streaming paths and uses backup links or peers as potential providers. Interoverlay optimization is employed to complement traditional intraoverlay strategies.

# 3 DESIGN OF SCHEME

To achieve good performance in P2P live streaming systems, the IOO scheme faces the following challenges:

1. to find paths with low delays, including source-toend delay and start-up delay, in a large-scale P2P network,   
2. to maintain the service continuity and stability, decreasing the impact of flash crowd and churn caused by peers leaving and joining and network fluctuations,   
3. to determine the frequency of optimization operations, and   
4. to reduce the control overhead.

# 3.1 Overview

As illustrated in Fig. 3, the basic workflow of the IOO scheme is as follows: First, an efficient mesh-based overlay is constructed. A location-detector-based algorithm is employed to match the overlay with the underlying physical topology [22]. Second, the single overlay manager, which is based on traditional intraoverlay optimization such as Narada [9], DONet, or nearcast [26], deals with the join/ leave operations of peers. Third, the interoverlay optimization manager explores appropriate paths, builds backup links, and cuts off paths with low QoS for each end peer. Fourth, the key node manager allocates the limited resources, and the buffer manager manages and schedules the transmission of media data.

![](images/936eae73381269f9f67812c575fade8265ccc092ddf5eda29b32e7c3319a1a32.jpg)



Fig. 4. Road map of the detector message initiated by peer MS.

# 3.2 Mesh-Based Overlay Manager

In IOO, all peers belonging to different streaming overlays will join one substrate, the mesh-based overlay first, to construct an under layer. In this layer, all peers can reach each other directly or indirectly. The function of the meshbased overlay manager is to provide information about the connections for the interoverlay optimizations. Every peer, with a unique identifier, first connects the bootstrapping peers and selects one or several peers to construct logical links. Every peer maintains a group of logical neighbors. The key issue here is to let the mesh-based overlay match with the underlying physical topology [23]. The mesh-based overlay manager, a key component of IOO, uses a scheme called the Location-aware Topology Matching (LTM) technique [22] to optimize the overlay, find the closest neighbors, and eliminate slow connections. There are two major operations: flooding-based detection with limited Time To Live (TTL) and updating logical connections.

In the first operation, each peer periodically floods a message, defined as dmðid; MS; T T L; bodyÞ, to its neighbors. The message dmðid; MS; T T L; bodyÞ means that the peer MS initiates a message with an ID value to peers at most T T L hops away. Since our purpose is to find the closest neighbors of peer MS, we define T T L ¼ 2. To detect the distance of peers, the message body has four parts: sourceIP (the IP address of the source peer), sourceTimestamp (the time stamp1 when the source forwards the message), DirectIP (the IP address of one neighbor within one hop), and DirectTimestamp (the time stamp when the neighbor within one hop gets the message). Fig. 4 shows the road map of one message from MS. Obviously, a message is broadcast to direct neighbors and two-hop-away neighbors.

In the second step, logical links are updated. With the help of the time stamps on peers, peer P 1 compares the distance between two paths, $M S \to P 1 , ~ M S \to N 1 _ { \mathit { \Omega } }$ , and $N 1  P 1$ . If the former length is smaller, the link $N 1  P 1$ will be cut off, and the direct path between MS and $P 1$ is established. All peers do the same operations as those of peer MS. After several operations, the peers would connect with their close neighbors [22].

# 3.3 Single Overlay Manager

The single overlay manager is responsible for peers leaving and joining operations based on the under layer, the meshbased overlay. Before interoverlay optimization, one peer joins one streaming overlay and receives media contents from multiple providers or a single provider according to intraoverlay optimization schemes. Here, we apply one scheme, named the “locality-aware” tree-based overlay construction scheme [26], to build an optimized single overlay.

Generally, each peer maintains one active streaming path set and one backup streaming path set. Initially, all streaming paths are managed by the single overlay manager.

Specifically, when a peer $\bar { P }$ is subscribing the media data from media source MS, MS will return the streaming rate $r a t e ( M S )$ of the media program to peer $P .$ Then, P maintains 1) an active streaming path set with threshold size $\delta _ { a } ( P , M S )$ and 2) a backup streaming path set with threshold size $\delta _ { b } ( P , M S )$ . For the ith streaming path $S P _ { i }$ from MS to $P ,$ it has two parameters: $d e l a y ( S P i , M S , P )$ is the source-to-end delay from source MS to peer P on the path SPi. When a media block is delivered from the media source to $P$ on the path $S P _ { i } ,$ , the single overlay manager records the time stamp and stores it into the media block’s header. Upon receiving the media block with the initial time stamp, $P$ computes the difference of the initial time stamp and the arriving time stamp. The little difference is the value of $d e l a y ( S P i , M S , P )$ , and $r a t e ( S P i , M S , P )$ is the streaming rate in the last hop of the path. Clearly, we have

$$
\begin{array}{l} \sum_ {i = 1} ^ {\delta_ {a} (P, M S)} \text {rate} \left(S P _ {i}, M S, P\right) \geq \text {rate} (M S), \tag {1} \\ \sum_ {i = 1} ^ {\delta_ {b} (P, M S)} r a t e (S P _ {i}, M S, P) = q \sum_ {i = 1} ^ {\delta_ {a} (P, M S)} r a t e (S P _ {i}, M S, P). \\ \end{array}
$$

In (1), the parameter q means that how many times the total downloading bandwidth from the backup streaming path set is bigger than that from the active streaming path set. Let $D ( M S )$ denote the threshold for the delay, which is related to the requested quality of the streaming service only. The higher the requested quality of streaming service, the less the threshold of delay will be. In this design, a new attribute called LastDelay is introduced, which is the minimal of all source-to-end delays from the current node to the streaming source on different paths. We have

$$
\text { LastDelay } = \operatorname{Min} (\text { delay } (S P _ {i}, M S, P)) \tag {2}
$$

$$
1 \leq i \leq \delta_ {a}.
$$

![](images/408fef5c80821c3eef5d476f3064dd43611e7fb39ebf118165c1cd9e971e8fb0.jpg)



Fig. 5. Structure of the message ProbM.

With LastDelay, each path to the media source can be measured. Peers can evaluate the QoS of streaming paths and adjust the directed neighbors according to LastDelay. The adjustment of the streaming path set can be done with the management of direct connected neighbors in the same overlay. Using the Gnutella protocol, peers find new neighbor candidates. Comparing pair delays, the fastest neighbors are selected to build direct connections from the candidates. Based on the streaming path sets of all directly connected neighbors, a new streaming path set can be created. Because each direct connected neighbor has maintained $x = \delta _ { a } ( P , M S ) + \delta _ { b } ( P , M S )$ streaming paths and the delays to all y neighbors can be calculated, the new streaming paths with the smallest source-to-end delays can be selected after the following calculations:

$$
\begin{array}{l} D S _ {y} (x) = \left[ \begin{array}{c} D _ {1, 1}, D _ {1, 2}, \dots , D _ {1, x} \\ D _ {2, 1}, D _ {2, 2}, \dots , D _ {2, x} \\ \vdots \\ D _ {y, 1}, D _ {y, 2}, \dots , D _ {y, x} \end{array} \right],   D S _ {y} = \left[ \begin{array}{c} D _ {1}, D _ {1}, \dots , D _ {1} \\ D _ {2}, D _ {2}, \dots , D _ {2} \\ \vdots \\ D _ {y}, D _ {y}, \dots , D _ {y} \end{array} \right], \\ D S (y \times x) = D S _ {y} (x) + D S (y). \tag {3} \\ \end{array}
$$

In (3), the parameter $D _ { i , j }$ denotes the source-to-end delay on the streaming path j of neighbor $i , D _ { i }$ denotes the direct delay to the neighbor $i , D S _ { y } ( x )$ is the delay matrix of all neighbors’ streaming paths. $D S ( y \times x )$ is the delay matrix of all potential streaming paths. From $y \times x$ streaming paths, we can choose $\delta _ { a } ( P , M S )$ active streaming paths and $\delta _ { b } ( P , M S )$ backup streaming paths.

# 3.4 Interoverlay Optimization Manager

When the number of backup streaming paths is less than a threshold, IOO is conducted to find appropriate streaming paths in the global P2P network with the help of the meshbased overlay. When one active streaming path is cut off, a new streaming path is selected from the backup set.

We also design a probing message named ProbM as shown in Fig. 5. This message includes two major parts: 1) initial information, including Seq.: sequence number, $P e e r \_ { 0 } .$ initial peer ID, Timestamp0: message issuance time, Source: media source ID of the initial peer, LastDelay, current value of LastDelay, and $T T L$ : current value of TTL; 2) an array with the size of TTL to record the peer ID and the arriving time stamp of the message. Considering that 95 percent of peers in the Gnutella system could be reached within seven hops by pure flooding [23], the maximal TTL is set to 7.

![](images/70a7f0f44468dfc3190a4a0d24566b587117403a82276609c9b6d0d4784da7a2.jpg)



![](images/db3ac19f4e68aad2369c68eb38f881710824bdb31e61d026056545621d412884.jpg)



(b)   
Fig. 6. An example of the reverse tracing algorithm. (a) Each peer forwards to three neighbors. (b) Each peer forwards to two neighbors. (a) LastDelay ¼ 8; j ¼ 3. (b) LastDelay ¼ 8; j ¼ 2.

The interoverlay optimization manager mainly has two tasks, backup streaming path set management and active streaming path set management.

# 3.4.1 Management of the Backup Streaming Path Set

The major operation in this component is a probing procedure, called the reverse tracing algorithm. This algorithm starts when the size of the backup set is less than $\delta _ { b } ( P , M S )$ . Peer\_0 sends out a ProbM message to j of its random neighbors with the recording array empty. Each receiver records the message arrival time and its ID into the message body of the received message, as shown in Fig. 5. The receiver will stop forwarding the message if 1) it finds that the delay from the initial peer Peer\_0 to this peer is greater than LastDelay or 2) the receiver is the source of this streaming service. Otherwise, the message would be forwarded to j of its random neighbors.

With the help of the reverse tracing algorithm, the media source is able to analyze the arrived messages with ID (Seq.) periodically and explore the best path from the source to the message issuance peer. Informed by the source, the peer then constructs an overlay path accordingly. Fig. 6 shows an example of the reverse tracing algorithm based on the overlay shown in Fig. 1, when j ¼ 3 and j ¼ 2, respectively. In this figure, all delays are replaced with the cost of two peers. Peer D sends out a message, and the possible routes of the message are shown. Some routes are cancelled due to a longer delay than LastDelay. Eventually, a good path $S _ { 1 }  \mathsf { \bar { S } } _ { 2 }  D$ is found. Then, LastDelay is updated. As a large portion of ProbM messages are stopped during forwarding process, the overhead is acceptable.

A streaming path of Peer D is treated as invalid if 1) the source-to-end delay is larger than a given threshold DðMSÞ or 2) the direct parent of Peer D on the path leaves. In this design, we only disconnect the overlay link between the end peer to its parent node. There are two reasons: 1) the other connections on the path can be reserved to provide support for new incoming peers, and 2) frequent disconnections incur a lot of unnecessary traffic.

# 3.4.2 Management of the Active Streaming Path Set

There are three operations: maintaining the states of active streaming paths, cutting off invalid paths, and adding new active paths from a backup set. When the total bit rates from active streaming paths are lower than rate(MS), the manager will check whether a better path should be activated to replace the current one.

This manager has the following characteristics:

1. it employs a heuristic algorithm to optimize the system step by step,   
2. probing procedures are originated from the normal peers, not the source peer, so that the control overhead can be distributed,   
3. the number of forwarding neighbors, j, is chosen to balance the trade-off between the effectiveness and the overhead, and   
4. the frequency of probing and optimization is dynamic.

In IOO, the probing procedure is feedback-driven based on delay. Log data from AnySee, the prototype of IOO scheme to be discussed in Section 5.4, show that when peers are watching highly popular movies, they are willing to tolerate a larger delay. Hence, it is reasonable that different programs define different DðMSÞ.

# 3.5 Key Node Manager

Admission control is useful when there are too many requests. The goal of the key node manager is to determine the number of requests that a peer should have. Suppose that a peer has Q unused connection slots. All requests will be classified into W types according to the different popularities of the target media, and each falls into one of W queues. When we assign the Q slots to W queues, there are two interesting cases. First, some queues are assigned with more than one connection slot, which can be modeled as an M/M/m/K queuing model. Second, some queues only receive one connection, which follows an M/M/1/K queuing model [25].

Our goal is given as follows: Suppose that the arriving rate of queue j is $\lambda _ { j } ,$ and all arriving rates satisfy $\lambda _ { 1 } \leq . . . \leq \lambda _ { j } \leq . . . \leq \lambda _ { W }$ . Assume that the service rate to assign one connection slot is $\mu ,$ and each connection processor can buffer k requests ðk ut 1Þ. If the probability that n requests follow the M/M/m/K queuing model is $p _ { n } ,$ we have

$$
p _ {n} = \left\{ \begin{array}{l l} \frac {(m \rho) ^ {n}}{n !} p _ {0} & n = 0, 1 \dots m - 1 \\ \frac {m ^ {m} \rho^ {n}}{m !} p _ {0} & n = m, m + 1 \dots K, \end{array} \right. \tag {4}
$$

where $\begin{array} { r } { \rho = \frac { \lambda } { m \mu } . } \end{array}$ ; we also have

$$
p _ {0} = \left\{ \begin{array}{l l} \left[ \sum_ {i = 0} ^ {m - 1} \frac {(m \rho) ^ {i}}{i !} + \frac {(m \rho) ^ {m}}{m !} \frac {1 - \rho^ {K - m + 1}}{1 - \rho} \right] ^ {- 1} & \rho \neq 1 \\ \left[ \sum_ {i = 0} ^ {m - 1} \frac {(m) ^ {i}}{i !} + \frac {(m) ^ {m}}{m !} (K - m + 1) \right] ^ {- 1} & \rho = 1. \end{array} \right. \tag {5}
$$

Thus, the average utilization of W spare connections of one peer can be given by

$$
\bar {\rho} = \rho (1 - \rho k) = \rho \left(1 - \frac {m ^ {m} \rho^ {K} p _ {0}}{m !}\right). \tag {6}
$$

One connection processor can buffer k requests. Then, $K = m k$ . When the probability that n requests are following the $\mathrm { M } / \mathrm { M } / 1 / \mathrm { K }$ queuing model is $p _ { n } ^ { ' } ,$ we have

$$
p _ {n} ^ {\prime} = \left\{ \begin{array}{l l} \frac {(1 - \rho) \rho^ {n}}{1 - \rho^ {K + 1}} & \rho \neq 1 \\ \frac {1}{K + 1} & \rho = 1 \end{array} \quad 0 \leq n \leq K \right. \tag {7}
$$

and $\begin{array} { r } { \rho = \frac { \lambda } { \mu } } \end{array}$ . Then, the average utilization of Q spare connections of one peer can be given by

$$
\tilde {\rho} = 1 - p _ {0} ^ {\prime} = \rho \left(\frac {1 - \rho^ {K}}{1 - \rho^ {K + 1}}\right) \tag {8}
$$

and $p _ { K } ^ { \prime }$ is the failure probability of requests. Then, the target, resource utilization, can be expressed as

$$
\operatorname{Max} \left(\rho \left(Q _ {1}, Q _ {2}, \dots Q _ {W}\right)\right) = \operatorname{Max} \left(\sum_ {1 \leq i, j \leq W} ^ {i \neq k} \left(\tilde {\rho} _ {i} + \tilde {\rho} _ {j}\right)\right) \tag {9}
$$

$$
\text { Subject   to } \quad \sum_ {i = 1} ^ {W} Q _ {i} = Q \quad 1 \leq Q _ {i} <   Q.
$$

Here, $Q _ { i }$ is the number of connection slots assigned to the request queue with ID i. The optimization problem in (9) can be divided into two parts. First, we enumerate all (W, 1)-partitions (W queues and each should be allocated at least 1 connection slot) of Q spare connections such that the best allocation can be found to maximize $\rho ( Q _ { 1 } , Q _ { 2 } , . . . Q _ { W } )$ . Second, for all H partitions of Q slots, we compute all H results of the average resource utilization and select the best partition. In the first phase, we can get H, the number of partitions of Q, by

$$
H = \binom {Q - 1} {W - 1} = \frac {(Q - 1) !}{(W - 1) ! (Q - W) !}, Q \geq W. \tag {10}
$$

From (10), the complexity of the first algorithm is $O ( Q )$ . The second algorithm is to select the maximal one from H results with the complexity of $O ( C _ { W - 1 } ^ { Q - 1 } ) = O ( Q )$ . Overall, this optimization problem has a complexity of OðQÞ. Considering one normal peer with a 10-Mbps bandwidth and an average streaming rate of 300 Kbps, Q should be set less than 33.

# 3.6 Buffer Manager

This manager is responsible for receiving valid media data from multiple providers in the active streaming path set and keeping the media playback. IOO employs a similar heuristic as used in the Coolstreaming system to fetch expected media segments in a dynamic and heterogeneous network to meet two constraints: the playback deadline for each segment and the heterogeneous streaming bandwidth from partners. As Coolstreaming does not employ any interoverlay optimization, peers often fail to find the closest neighbors to provide services. Consequently, to keep the media playback continuously, a big buffer must be used in Coolstreaming. With the help of IOO, a small buffer space is enough, which also means a shorter start-up delay. For example, the average start-up delay of the AnySee system based on the IOO scheme is about 10 seconds.

TABLE 1 Simulation Parameters 

<table><tr><td>Abbreviate</td><td>Comment</td></tr><tr><td>S</td><td>number of streaming overlays</td></tr><tr><td>M</td><td>number of neighbors</td></tr><tr><td>N</td><td>size of one overlay</td></tr><tr><td>r</td><td>streaming playback rate</td></tr><tr><td>BW</td><td>total bandwidth in Mbps</td></tr></table>

# 4 SIMULATION

Before introducing the implementation of IOO in the real AnySee system, we evaluate this design with simulations so that we can contrast its performance with a recent live streaming system, Coolstreaming. We are mainly concerned with the metrics of Resource utilization and Continuity index.

# 4.1 Simulation Setup

We consider two types of topologies, physical topology and logical P2P topology. The physical topology should represent a real topology with Internet characteristics. The logical topology represents the overlay P2P topology built on top of the physical topology. All P2P nodes are in a subset of nodes in the physical topology.

We have developed a crawler to collect the topology information of the Gnutella network [1]. According to Gnutella, a ping message with TTL ¼ 2 and $\mathrm { { H O P } = 0 }$ is regarded as a crawler ping, and peers, upon receiving a crawler ping, would respond with appropriate pong messages. Based on this mechanism, we explore the Gnutella topology by performing a breadth-first search on the network. From our experience and observations, we find that some clients such as Gnucleus and Morpheus (based on GnucDNA) do not respond to the crawler ping appropriately. Fortunately, those clients send an information page summarizing the servants’ status to any Web browser trying to connect to it. Motivated by this, we also developed a Web spider as a means of collecting topology information from these clients and integrated the Web spider into the crawler, which accelerates the crawling process significantly. The crawler is written in Java based on Limewire’s [3] open source client and runs in parallel using 40 threads. Our crawler can discover more than 50,000 peers within half an hour. In this simulation, we use three data sets, obtained from different time slots. For the physical topology, we use BRITE [4], generating three topologies, each of which has 5,000 nodes.

The major parameters in our simulations are listed in Table 1. In each run, peers randomly join one of S streaming overlays $\left( \mathrm { S } = 1 , 4 , 8 , \hat { 1 } 2 \right)$ . A peer has bandwidth BW, ranging from 1 to 10 Mbps, and maintains M neighbors. The size of an overlay is N (N< 500). Each stream is 1,800 seconds long, and the streaming rate is r, normally 300 Kbps. Based on the delay values from the trace, we set the bandwidths for peers. For simplicity, the threshold DðMSÞ is set to 25 seconds, which is estimated from the logs of our AnySee implementation. The adjustment factor p is set to 1, which means that we provide one backup streaming path for each active streaming path.

![](images/9a4d514f3987208c17ffdfb87ec08dce1bebfb3e5e034eab3e299b0e969e8b3f.jpg)



Fig. 7. Continuity index versus streaming rates when $\mathrm { { N } = 4 0 0 , \mathrm { { S } = 1 2 } }$ and the initial buffer size is 40 seconds.

# 4.2 Simulation Results

The first set of simulations is conducted in a static environment, in which peers do not leave after joining the overlays. For each simulation setup, we take 100 runs and report the average.

Fig. 7 plots the continuity index against the streaming rate, where we contrast IOO with Coolstreaming. When the streaming rate is increased, the continuity of the IOO scheme is not changed much, whereas the continuity of Coolstreaming is degraded. There are two reasons. First, the IOO scheme can find neighbors from all peering nodes to request services, whereas Coolstreaming is only able to find suppliers from the same overlay. Second, the necessary buffer size of the IOO scheme is 40 seconds, whereas Coolstreaming often needs a 120-second buffer.

Fig. 8 shows the scalability of IOO. We can see that the continuity improves with the increasing number of overlays. Our implementation results also show that the larger overlay size often leads to better QoS. In Fig. 8, we also see that the IOO scheme outperforms Coolstreaming, even if they have the same number of overlays.

![](images/95b0f66f3b9d6fe38f3bf98d8897ed133456c38681176a80e1669724162fa9e5.jpg)



Fig. 9. Resource utilization: overlay size versus the number of streaming overlays when M ¼ 12 and r ¼ 300 Kbps.

Figs. 9 and 10 contrast resource utilization. As seen in Fig. 9, a larger number of overlays have a greater impact on the performance of the IOO scheme, but no obvious influence on that of Coolstreaming. In Fig. 10, the resource utilization is improved with the increasing number of neighbors. Under the same condition, the performance of the IOO scheme is better than that of Coolstreaming. We then allow peers to leave and join freely. We define the lifetime of each peer in the overlay from 100 to 800 seconds. The peer average lifetime is exponentially distributed with an average of T seconds. We can see in Figs. 11 and 12 that a longer lifetime leads to better service quality and higher resource utilization. As our proposed IOO scheme has a backup path management design and the reverse tracing component keeps finding better paths dynamically, the IOO scheme always outperforms Coolstreaming.

![](images/ef6d6e5ab80652c63443c91da043347bd8f3bd6c17c9aa0972978a6dafed8d18.jpg)



Fig. 8. Continuity index versus the number of streaming overlays when N ¼ 400, r ¼ 300 Kbps, and the initial buffer size is 40 seconds.

![](images/7aa154b9477cb8b58c98ef7fe9c122558c61925238a64c18c00727591728788e.jpg)



Fig. 10. Resource utilization: the number of neighbors versus the number of streaming overlays when N ¼ 400 and r ¼ 300 Kbps.

![](images/57de30ab56e6a64416cd9f023d0288cab62bfc92eb6ee388e8c783a1437ff766.jpg)



Fig. 11. Continuity index under dynamic environment when $\mathrm { M } = 5 ,$ N ¼ 400, r ¼ 300 Kbps, and the initial buffer size is 40 seconds.   
![](images/9e91c7235cd658e8d900c4ebf673dc72df25f7c25648d2629a80177715310712.jpg)



Fig. 12. Resource utilization under a dynamic environment when M ¼ 5, N ¼ 400, and r ¼ 300 Kbps.

# 5 ANYSEE: PRACTICAL IMPLEMENTATION OF THE IOO SCHEME

We have implemented the public free system AnySee and released several versions (v1.1, v2.0, and v3.0) to provide a scalable live streaming service platform based on interoverlay optimization in CERNET. CERNET is funded by the Chinese government to support network services for people in universities. Now, more than 15 million PCs and 26 million users have been connected to CERNET to share information. From June 2004 to February 2005, there were over 60,000 connections to the AnySee platform, and more than 40 universities and 20 cities in China were in the service map, as illustrated in Fig. 13. AnySee2 is implemented with Java and is platform independent.

2. The AnySee system has three main versions as of March 2007. The version we discussed is 1.1. The updated version 3.0 is published on the Web site www.anysee.net, which is in CERNET. The latest version adds time-shift functions.

![](images/17e1c0df87fae67a4799bbef0ec44a0331fdb0bcb4e5b907cafc34253195d29c.jpg)



Fig. 13. Service map of AnySee in CERNET (red center point: Huazhong University of Science and Technology (HUST), Wuhan, China).   
![](images/e1dd25ebc7539b8425204259348dea275095c246a17c9c1c14bda1001e82cf74.jpg)



Fig. 14. Topology of AnySee in CERNET.

# 5.1 Architecture Overview

AnySee is comprised of four major components as illustrated in Fig. 14. They are

1. a rendezvous point,   
2. a media source,   
3. a log server, and   
4. peers.

Each peer contains several important modules: an IP-tonetwork-coordinates database (INCD), which is prebuilt and integrated into the peer’s software, for optimizing the underlying mesh-based overlay according to the group ID (GID) scheme; the topology manager, including the underlying mesh manager, tree manager, and interoverlay manager; a buffer manager; a media player, decoding streaming data; and a local HTTP/Real-Time Streaming Protocol (RTSP) server, receiving media data from the buffer and sending them to the media player using HTTP or RTSP.

Normally, the bandwidths of the upstream and downstream for each peer in CERNET are 10 to 100 Mbps. One peer can provide streaming services for multiple ones in AnySee. In our log, we can see that each peer is often able to maintain five neighbors with the streaming rate from 300 to 550 Kbps, which means it joins five streaming overlays simultaneously.

# 5.2 Implementation Experiences

We discuss two interesting issues in the AnySee implementation, the GID-based scheme and locality-aware buffer management scheme, which are not included in IOO.

# 5.2.1 GID-Based Scheme

Low latency and high bandwidth are always desirable in streaming services. Due to the fact that all peers in AnySee are in the same CERNET so that the physical network map is known, the distance among pairs of peers can be easily computed by the IP addresses. Hence, AnySee requires each peer to maintain an INCD such that every peer has a position named. The GID value of an end host is a 128-bit integer encoded by the four-layer geometrical information corresponding to ISPs, cities, campuses, and buildings, respectively. With the help of the GID-based scheme, a peer can find closer peers to build connections instead of randomly selecting neighbors. Consequently, LTM (described in Section 3.2) needs less management resources than ever to build a mesh-based overlay.

# 5.2.2 Locality-Aware Buffer Management Scheme

In the IOO scheme, the buffer size is simply defined as 40 seconds. As the behavior of peers in the upper layers of a tree often have a larger impact on QoS than that of peers in the lower layers, AnySee employs a layer-aware buffer management mechanism. Each peer computes its appropriate buffer space size based on its layer number. In AnySee, the size of the buffer for peer A at the xth layer is given by

$$
T _ {A} = f (x) = \varepsilon \times T L _ {A} + T D _ {A}, \tag {11}
$$

where $T L _ { A }$ denotes the total link delay, $T D _ { A }$ is the total transmission delay, and " is the average disconnection times of one connection.

Suppose that the probability of a link or node failure is $P _ { b }$ , and a peer needs $t _ { b }$ time to explore a new parent, the shift delay, the average time to replace the removed parent with a new one, is $t _ { l } = P _ { b } \times t _ { b } ,$ and the link delay $T L _ { A }$ is the accumulation of all shift delays. Suppose that the transmission delay per hop is $\gamma ,$ and the total hops between the source peer and peer A is $x ,$ the total transmission delay of peer A is $\bar { T } { \cal D } _ { A } = \gamma \mathrm { ~  ~ \times ~ } x .$ If the path from the source peer to peer A is $l _ { S  A } = \{ l _ { S  a _ { 1 } } , l _ { a _ { 1 }  a _ { 2 } } , \ldots , l _ { a _ { m - 1 }  A } \}$ , the path has the following properties:

1. the source peer would persist all the time, and path $l _ { S  a _ { 1 } }$ would not break,   
2. peer A would also stay in the network, and path $l _ { a _ { m - 1 }  A }$ would exist,   
3. the influence that multiple borders break down simultaneously is the accumulation of influence that multiple borders break down one by one, and   
4. if peer $a _ { i }$ leaves, a new peer would join the tree and replace the position of $a _ { i } .$ .

The total link delay can be computed by

$$
T L _ {A} = \sum_ {i = 1} ^ {i = x - 1} t _ {l _ {a _ {i} \rightarrow a _ {i + 1}}}
$$

![](images/b0a7908735f047777dfc3b5353ebc31f976bafa8ea83dd5259f8dbce81130f43.jpg)



Fig. 15. Tree height versus size.

and

$$
t _ {l _ {a _ {i} \rightarrow a _ {i + 1}}} = (1 - P _ {b}) ^ {i - 1} \times t _ {l},
$$

then

$$
T L _ {A} = t _ {l} + (1 - P _ {b}) \times t _ {l} + \dots + (1 - P _ {b}) ^ {x - 2} \times t _ {l},
$$

$$
T L _ {A} = t _ {l} \times \frac {1 - (1 - P _ {b}) ^ {x - 1}}{P _ {b}} = t _ {b} \times \left(1 - (1 - P _ {b}) ^ {x - 1}\right). \tag {12}
$$

Thus, we have

$$
T _ {A} = \varepsilon \times t _ {b} \times \left(1 - (1 - P _ {b}) ^ {x - 1}\right) + \gamma \times x. \tag {13}
$$

Given the estimation of the above parameters in (13), the maximum buffer size to offset dynamic factors for A at the xth layer is computed based on the layer number x.

# 5.3 Performance

We select to show the log data from 13 August 2004 to 29 August 2004, during which period 7,200 users from 40 universities in 14 cities in China received streaming services from AnySee. We analyze the performance of the multiple multicast trees every 10 minutes.

Fig. 15 plots the average height of AnySee trees against the tree size. The height increases when more peers join, but it is always less than 7 even when up to a thousand peers are included in one tree. Such a property significantly shortens the source-to-end delay, shown in Fig. 16. We can see that the maximal value of the source-to-end delay increases with the incensement of the tree size, whereas the average delay is typically at the level of around 200 ms.

Fig. 17 plots the start-up delay. This delay of most peers is less than 20 seconds. We have also implemented a simple prototype, getting media services from the Coolstreaming network, and we observe the start-up delays for 50 times. Mostly, the start-up delay of Coolstreaming is around 60 seconds.

Based on the results shown in Fig. 16, we set  to 200 ms and define $t _ { b } = 3 5 0 , P _ { b } = 0 . 4 ,$ and " ¼ 10. Fig. 18 shows the corresponding values of buffer sizes in different layers. The maximal number of layers is not exceeding 8. When the buffer sizes are set based on the values in Fig. 18, AnySee is not influenced much by frequent peer joining and leaving.

![](images/2fa20f6f75fa39b52157defd32f729f82eb479edd631507cb7b84f46941fd618.jpg)



Fig. 16. Source-to-end delay versus tree size.

![](images/2270b39cba1ed8c2ca97a32cb66b873d5b3ff1ab3a3bf61fa9c8ee5d2caf2e61.jpg)



Fig. 19. Number of peers.

![](images/d7615773ef7f5afbc901ded2b9983c7ae20ab75f915507e2e4d90530fc2f17c0.jpg)



Fig. 17. Start-up delay in AnySee.

![](images/456b24f57657eb8e07a18827f56b20fee87d1a15f8810f25f272201cd5255993.jpg)



Fig. 20. Percentage of leaving peers.

![](images/b7c1f64f6332870c4c4b501d3458ce00e75dbb0b19019be956f72a1ecfd86d03.jpg)



Fig. 18. Buffer size versus layer number.

![](images/47445b140e850241abc704fa6e94637eba7b1c261e34002c823ee5792d4d40d0.jpg)



Fig. 21. Average delay.

# 5.4 User Behaviors

Intuitively, if we know more about the user behaviors, we can better optimize the system. By analyzing the log data, we try to get many parameters, including the total number of peers, the average delay (source-to-end delay), and the leaving peer percentage in different “hot” periods.

Figs. 19, 20, and 21 show the maximum number of peers, the maximum percentage of leaving peers, and the average delay of three programs, a, b, and c, for one hour. The results show that the overlays with popular movies attract more users to join and stay but cause large delays. From the figures, we have the following interesting observations. First, a larger delay is not always the major reason that causes people to leave the service. For example, the leaving percentage of Program a is not the largest, whereas its average delay is the longest. Peers have more patience if the program is popular and attractive. Second, delays from 20 to 30 seconds will not be the killer for the live streaming services. Most people will stay in the overlay even if there is a 30-second delay from the source peer.

TABLE 2 ADLs in Hot Periods of Different Programs 

<table><tr><td>Num.</td><td>Program-a</td><td>Program-b</td><td>Program-c</td></tr><tr><td>1</td><td>0.5217</td><td>0.4706</td><td>0.6363</td></tr><tr><td>2</td><td>0.4583</td><td>0.5000</td><td>0.4167</td></tr><tr><td>3</td><td>0.7000</td><td>0.5238</td><td>0.4545</td></tr><tr><td>4</td><td>0.7143</td><td>0.5455</td><td>0.8462</td></tr><tr><td>5</td><td>0.5600</td><td>0.6190</td><td>0.6429</td></tr><tr><td>6</td><td>0.6154</td><td>0.5217</td><td>0.6667</td></tr><tr><td>7</td><td>0.5862</td><td>0.4642</td><td>0.6875</td></tr><tr><td>Average</td><td>0.5937</td><td>0.5213</td><td>0.6215</td></tr></table>

Based on the above observations, AnySee determines the optimization frequency according to the average delay together with the percentage of leaving peers. The parameter “optimization index,” ADL, is given by

$$
\mathrm{ADL} = 1 0 0 \times \frac {\text { leaving   percent }}{\text { average   delay }}. \tag {14}
$$

Three ADLs from different periods are shown in Table 2. In Table 2, the average ADLs for the above programs are 0.5937, 0.5213, and 0.6215, respectively. AnySee uses a threshold on ADL to determine whether an optimization operation is needed.

# 6 CONCLUSION AND FUTURE WORK

Efficient and scalable live-streaming overlay construction is a hot topic. In this paper, we propose an interoverlayoptimization-based live streaming scheme, IOO. Instead of selecting better paths in the same overlay, IOO constructs efficient paths using peers in different overlays. We evaluate the performance of the IOO scheme by comprehensive simulations. Our experimental results show that the IOO scheme outperforms existing intraoverlay live streaming schemes. In future research, we will provide a reputation-based incentive mechanism encouraging users to contribute resources.

The practical AnySee system, a prototype of the IOO scheme, has been released for several months, and its client code is free to be downloaded in CERNET. To date, over 60,000 users benefit from AnySee to enjoy two international academic conferences, GCC ’04 and 2004 IFIP International Conference on Network and Parallel Computing (NPC), and other massive entertainment programs. Logs from AnySee show that users have great patience for live streaming services with a relatively large delay if they have enough interest on the programs. We hope the AnySee system can serve more people and attain better quality in the future.

We are also building a large-scale P2P video-on-demand (VoD) service. We are going to observe more user behaviors to further improve the system performance.

# ACKNOWLEDGMENTS

This work was supported in part by the China National Natural Science Foundation (NSFC) Grants 60642010, 60703050, and 60433040, the National Basic Research Program of China (973 Program) under grant No. 2007CB310904, the Research Fund for the Doctoral Program of Higher Education Grant 20050487040, the Hong Kong RGC Grants HKUST6264/04E and HKUST 6152/06E, and the National High Technology Research and Development Program of China (863 Program) under grant No. 2007AA01Z180. The preliminary result of this paper was published in the Proceedings of IEEE INFOCOM 2006.

# REFERENCES

[1] The Gnutella Protocol Specification 0.6, http://rfc-gnutella. sourceforge.net, 2007.   
[2] AnySee, a Live Streaming Peer-to-Peer Platform, http://grid. hust.edu.cn/p2p, 2007.   
[3] Limewire, http://www.limewire.com, 2007.   
[4] BRITE, http://www.cs.bu.edu/brite, 2007.   
[5] S. Banerjee, C. Kommareddy, K. Kar, B. Bhattacharjee, and S. Khuller, “Construction of an Efficient Overlay Multicast Infrastructure for Real-Time Applications,” Proc. IEEE INFOCOM, 2003.   
[6] K. Sripanidkulchai, A. Ganjam, B. Maggs, and H. Zhang, “The Feasibility of Peer-to-Peer Architectures for Large-Scale Live Streaming Application,” Proc. ACM SIGCOMM, 2004.   
[7] Q. Zhang, F. Yang, W. Zhu, and Y.-Q. Zhang, “A Construction of Locality-Aware Overlay Network: mOverlay and Its Performance,” IEEE J. Selected Areas in Comm., special issue on recent advances on service overlay networks, Jan. 2004.   
[8] X. Zhang, J. Liu, B. Li, and P. Yum, “DONET: A Data-Driven Overlay Network for Efficient Live Media Streaming,” Proc. IEEE INFOCOM, 2005.   
[9] Y. Chu, G. Rao, and H. Zhang, “A Case for End System Multicast,” Proc. ACM SIGMETRICS, 2000.   
[10] M. Castro, P. Druschel, A. Kermarrec, A. Nandi, A. Rowstron, and A. Singh, “SplitStream: High-Bandwidth Content Distribution in Cooperative Environments,” Proc. 19th ACM Symp. Operating Systems Principles (SOSP), 2003.   
[11] D. Kostic, A. Rodriguez, J. Albrecht, and A. Vahdat, “Bullet: High Bandwidth Data Dissemination Using an Overlay Mesh,” Proc. 19th ACM Symp. Operating Systems Principles (SOSP), 2003.   
[12] V.N. Padmanabhan, H.J. Wang, P.A. Chou, and K. Sripanidkulchai, “Distributing Streaming Media Content Using Cooperative Networking,” Proc. 12th ACM Network and Operating System Support for Digital Audio and Video (NOSSDAV), 2002.   
[13] D. Pendarakis, S. Shi, D. Verma, and M. Waldvogel, “ALMI: An Application Level Multicast Infrastructure,” Proc. Third Usenix Symp. Internet Technologies and Systems (USITS), 2001.   
[14] B. Zhang, S. Jamin, and L. Zhang, “Host Multicast: A Framework for Delivering Multicast to End Users,” Proc. IEEE INFOCOM, 2002.   
[15] M. Hefeeda et al., “PROMISE: Peer-to-Peer Media Streaming Using CollectCast,” Proc. 11th ACM Int’l Conf. Multimedia (Multimedia), 2003.   
[16] D. Tran, K. Hua, and S. Sheu, “ZIGZAG: An Efficient Peer-To-Peer Scheme for Media Streaming,” Proc. IEEE INFOCOM, 2003.   
[17] S. Banerjee, B. Bhattacharjee, and C. Kommareddy, “Scalable Application Layer Multicast,” Proc. ACM SIGCOMM, 2002.   
[18] Y. Guo, K. Suh, J. Kurose, and D. Towsley, “P2Cast: P2P Patching Scheme for VoD Service,” Proc. 12th Int’l World Wide Web Conf. (WWW), 2003.   
[19] X. Jiang, Y. Dong, and B. Bhargava, “GNUSTREAM: A P2P Media Streaming System Prototype,” Proc. IEEE Int’l Conf. Multimedia and Expo (ICME), 2003.   
[20] Z. Zhang, S. Shi, and J. Zhu, “SOMO: Self-Organized Metadata Overlay for Resource Management in P2P DHT,” Proc. Second IEEE Int’l Workshop Peer-to-Peer Systems (IPTPS), 2003.   
[21] S. Ratnasamy, P. Francis, M. Handley, R. Karp, and S. Shenker, “A Scalable Content-Addressable Network,” Proc. ACM SIGCOMM, 2001.

[22] Y. Liu, L. Xiao, X. Liu, L.M. Ni, and X. Zhang, “Location-Aware Topology Matching in P2P Systems,” Proc. IEEE INFOCOM, 2004.   
[23] M. Ripeanu and I. Foster, “Mapping Gnutella Network,” IEEE Internet Computing, 2002.   
[24] NTP: The Network Time Protocol, http://www.ntp.org/, 2007.   
[25] L. Kleinrock, Queuing Systems. John Wiley & Sons, 1974.   
[26] X. Tu, H. Jin, D. Deng, C. Zhang, and Q. Yuan, “Design and Deployment of Locality-Aware Overlay Multicast Protocol for Live Streaming Services,” Proc. IFIP Int’l Conf. Network and Parallel Computing (NPC), 2005.

![](images/735b0d2080bc66860ee0a26778fffd3b6654eb3aa838954a5bd2e3ba8f2a2379.jpg)



Xiaofei Liao received the PhD degree in computer science and engineering from the Huazhong University of Science and Technology (HUST), China, in 2005. He is now an associate professor in the School of Computer Science and Engineering, HUST. His research interests are in the areas of peer-to-peer systems, cluster computing, and streaming services. He is a member of the IEEE and the IEEE Computer Society.

![](images/55e76c57d4d56aa0c38f596339685d2454619afd67e007a6a24757803738eb39.jpg)



Hai Jin received the BS, MA, and PhD degrees in computer engineering from the Huazhong University of Science and Technology (HUST), China, in 1988, 1991, and 1994, respectively. Now, he is a professor of computer science and engineering and the dean of the School of Computer Science and Technology, HUST. In 1996, he received a German Academic Exchange Service (DAAD) fellowship for visiting the Technical University of Chemnitz, Germany.

He worked for the University of Hong Kong (HKU) from 1998 to 2000 and participated in the HKU Cluster project. He worked as a visiting scholar at the University of Southern California from 1999 to 2000. He is the chief scientist of the largest grid computing project, ChinaGrid, in China. His research interests include cluster computing and grid computing, peer-topeer computing, network storage, network security, and high assurance computing. He is a senior member of the IEEE and a member of the ACM. He is a member of Grid Forum Steering Group (GFSG).

![](images/33d018e5c8d03185d5ef5214223a641f956dc84155d11dbaf03629c70a9076da.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MA degree from Beijing Foreign Studies University, China, in 1997, and the MS and PhD degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is now an assistant professor in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research interests include peer-

to-peer computing, sensor networks, and pervasive computing. He is a senior member of the IEEE and the IEEE Computer Society.

![](images/e60accf949224130bacb4d23f6c9ccc76c77ae98e28e1559b4480cc14b3012fa.jpg)



Lionel M. Ni received the PhD degree in electrical and computer engineering from Purdue University, West Lafayette, Indiana, in 1980. He is a chair professor at the Hong Kong University of Science and Technology (HKUST) and heads the Computer Science and Engineering Department. He is also the director of the HKUST China Ministry of Education/Microsoft Research Asia IT Key Laboratory and the director of the HKUST Digital Life Research

Center. He is a fellow of the IEEE. He has chaired many professional conferences and has received a number of awards for authoring outstanding papers. He is a coauthor of the book Interconnection Networks: An Engineering Approach (with Jose Duato and Sudhakar Yalamanchili) published by Morgan Kaufmann in 2002, the book Smart Phone and Next Generation Mobile Computing (with Pei Zheng) published by Morgan Kaufmann in 2006, and the book Professional Smartphone Programming (with Baijian Yang and Pei Zheng) published by Wrox Publishing Inc. in 2007.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.