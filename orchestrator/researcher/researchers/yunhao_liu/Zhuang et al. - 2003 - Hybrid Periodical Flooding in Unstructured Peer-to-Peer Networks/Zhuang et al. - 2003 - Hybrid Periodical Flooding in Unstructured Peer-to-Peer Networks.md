# Hybrid Periodical Flooding in Unstructured Peer-to-Peer Networks\*

Zhenyun Zhuang $^{1}$ , Yunhao Liu $^{1}$ , Li Xiao $^{1}$ and Lionel M. Ni $^{2}$

$^{1}$ Department of Computer Science and Engineering, Michigan State University, U.S.A. $^{2}$ Department of Computer Science, Hong Kong University of Science and Technology, Hong Kong {zhuangz1, liuyunha, lxiao}@cse.msu.edu, ni@cs.ust.hk

# Abstract

Blind flooding is a popular search mechanism used in current commercial P2P systems because of its simplicity. However, blind flooding among peers or superpeers causes large volume of unnecessary traffic although the response time is short. Some improved statistics-based search mechanisms can reduce the traffic volume but also significantly shrink the query coverage range. In some search mechanisms, not all peers may be reachable creating the so-called partial coverage problem. Aiming at alleviating the partial coverage problem and reducing the unnecessary traffic, we propose an efficient and adaptive search mechanism, Hybrid Periodical Flooding (HPF). HPF retains the advantages of statistics-based search mechanisms, alleviates the partial coverage problem, and provides the flexibility to adaptively adjust different parameters to meet different performance requirements. The effectiveness of HPF is demonstrated through simulation studies.

# 1 Introduction

In an unstructured P2P system, such as Gnutella [7] and KaZaA [8], file placement is random, which has no correlation with the network topology [17]. Unstructured P2P systems are most commonly used in today's Internet. In an unstructured P2P system, when a source peer needs to query an object, it sends a query to its neighbors. If a peer receiving the query cannot provide the requested object, it may relay the query to its own neighbors. If the peer receiving the query can provide the requested object, a response message will be sent back to the source peer along the inverse of the query path. The most popular query operation in use, such as Gnutella and KaZaA (among supernodes), is to blindly "flood" a query to the network. A query is broadcast and rebroadcast until a certain criterion is satisfied. This mechanism ensures that the query will be "flooded" to as many peers as possible within a short period of time in a P2P overlay network. However, flooding also causes a lot of network traffic and most of which is unnecessary. Study in [13] shows that P2P traffic contributes the largest portion of the Internet traffic based on their measurements on three popular P2P systems, FastTrack (including KaZaA and Grokster) [5], Gnutella, and DirectConnect. The inefficient blind flooding search technique causes the unstructured P2P systems being far from scalable [11].

To avoid the large volume of unnecessary traffic incurred by flooding-based search, many efforts have been made to improve search algorithms for unstructured P2P systems. One typical approach is statistics-based, in which instead of flooding to all immediate overlay neighbors, a peer selects only a subset of its neighbors to query based on some statistics information of some metrics and heuristic algorithms. When handling a query message (either relayed from its neighbor or originated from itself) in a statistics-based search algorithm, the peer determines the subset of its logical neighbors to relay the query message. Statistics-based search mechanisms may significantly reduce the traffic volume but may also reduce the query coverage range so that a query may traverse a longer path to be satisfied or cannot be satisfied. In some search mechanisms, not all peers may be reachable creating the so-called partial coverage problem. Our objective is trying to alleviate the partial coverage problem and reduce unnecessary traffic.

In this paper, Section 2 will give an overview and classification of known search mechanisms. The concept of our proposed periodical flooding method will be introduced in Section 3. Based on periodical flooding and weighted metrics in selecting relay neighbors, the hybrid periodical flooding (HPF) method is detailed in Section 3. The proposed HPF can improve the efficiency of blind flooding by retaining the advantages of statistics-based search mechanisms and by alleviating the partial coverage problem. Section 4 describes our simulation method and the performance metrics. Performance evaluation of our proposed HPF method against other search methods is described in Section 5. Section 6 concludes the paper.

# 2 Search Mechanisms

In unstructured P2P systems, the placement of objects is loosely controlled and each peer has no hint where the intended objects are stored. Without having the global knowledge of the dynamic overlay network and the locations of target peers, a source peer has to send a query message to explore as many peers as possible in the overlay network. A well-designed search mechanism should seek to optimize both efficiency and Quality of Service (QoS). Efficiency focuses on better utilizing resources, such as bandwidth and processing power, while QoS focuses on user-perceived qualities, such as number of returned results and response time. In unstructured P2P systems, the QoS of a search mechanism generally depends on the number of peers being explored (queried), response time, and traffic overhead. If more peers can be queried by a certain query, it is more likely that the requested object can be found. In order to avoid having query messages flowing around the network forever, each query message has a TTL (time-to-live: the number of times a query will be forwarded) field. A TTL value is set to limit the search depth of a query. Each time a peer receives a query, the TTL value is decremented by one. The peer will stop relaying the query if TTL becomes zero. A query message will also be dropped if the query message has visited the peer before. Note that the query messages are application-level messages in an overlay network.

In statistics-based search mechanisms, a peer selects a subset of its neighbors to relay the query based on some statistics information of some metrics and heuristic algorithms. Based on the number of selected logical query neighbors and the criteria in selecting logical query neighbors, the statistics-based search algorithms in unstructured P2P systems can be roughly classified into two types: uniformed selection of relay neighbors and weighted selection of relay neighbors.

# 2.1 Uniformed Selection of Relay Neighbors

In this approach, all logical neighbors are equally treated when selected to relay the query message.

Blind flooding. Blind flooding mechanism relays the query message to all its logical neighbors, except the incoming peer. This mechanism is also referred as breadth-first search (BFS) and is used among peers in Gnutella or among supernodes in KaZaA. For each query, each node records the neighbors which relay the query to it. Thereby on each link, at most two query messages can be sent across it. For an overlay network with m peers and average n neighbors per peer, the total traffic caused by a query is mn if the value of TTL is no less than the diameter of the overlay network. Note that in a typical P2P system, the value of m (more than millions) is much greater than n (less than tens) [13]. In this approach, the source peer can reach its target peer (object) through a shortest path. However, the overhead of blind flooding is very large since flooding generates large amount of unnecessary traffic, wasting bandwidth and processing resource. The simplicity of blind flooding makes it very popular in practice.

Depth-first search (DFS). Instead of sending queries to all the neighbors, a peer just randomly selects a single neighbor to relay the query message when the TTL value is not zero and waits for the response. This search mechanism is referred to as depth-first search (DFS) and is used in Freenet [6]. DFS can terminate timely when the required object has been found, thus avoiding sending out too many unnecessary queries. In DFS, the value of TTL should be set sufficiently large to increase the probability of locating the object. The maximum number of peers that a query message will visit is TTL. Thus, setting a proper TTL value is a key issue to determine the search quality. The response time could be unbearably large due to the nature of its sequential search process. Because of the random selection of relay neighbors, it is possible that an object can hardly be found.

K-walker. In k-walker query algorithm proposed in [10], a query is sent to k different walkers (relay neighbors) from the source peer. For a peer in each walker, it just randomly selects one neighbor to relay the query. For each walker, the query processing is done sequentially. For k walkers with up to TTL steps, each query can reach up to $k \times TTL$ peers in the P2P network. We can view k-walker search mechanism as a multiple of DFS. It has been shown that k-walker mechanism creates less traffic than that of BFS and provides shorter response time than that of DFS. However, k-walker suffers limited query coverage range due to the randomness nature in selecting query neighbors.

# 2.2 Weighted Selection of Relay Neighbors

Instead of randomly selecting relay neighbors, some mechanisms have been proposed to select relay neighbors more objectively so that neighbors who are most likely to return the requested results are selected. Some statistics information is collected based on some metrics when selecting relay neighbors. Possible metrics include delay of the link to the corresponding neighbor, the processing time of the neighbor, the computing power, the cost (if possible), the amount of sharing data, and the number of neighbors, etc.

Directed BFS (DBFS). Each peer maintains statistic information based on some metrics, such as the number of results received from neighbors from previous queries or the latency of the connection with that neighbor. A peer selects a subset of the neighbors to send its query based on some heuristics, such as selecting the neighbors that have returned the largest number of results from previous queries or selecting the neighbors that have the smaller latency.

Routing indices (RI). The concept of routing indices (RI) was proposed in [3]. Each peer keeps a local RI that is a detailed summary of indices, such as the number of files on different topics of interests along each path. When a peer receives a query, it forwards the query to the neighbor that has the largest number of files under a particular topic, rather than selecting relay neighbors at random or flooding to all neighbors.

Some weighted-selection search mechanisms have demonstrated performance improvement compared with uniformed-selection search mechanisms. However, weighted-selection search mechanisms have the partial coverage problem to be illustrated in Section 2.4.

# 2.3 Other Approaches

In addition to the aforementioned search policies, there are other techniques that may be used to improve search performance. For example, a peer can cache query responses in hoping that subsequent queries can be satisfied quickly by the cached indices or responses $[14, 16, 17]$ . Peers can also be clustered based on different criteria, such as similar interests $[14]$ , location information $[9]$ , and associative rules $[4]$ . Our proposed statistics-based technique can be used to complement these techniques.

# 2.4 Partial Coverage Problem

Statistics-based search algorithms indeed can reduce network traffic. For example, compared with blind flooding, DBFS can reduce the aggregate processing and bandwidth cost to about 28% and 38%, respectively with 40% increase in the response time [17]. However, our study will show that statistics-based search mechanisms may leave a large percentage of the peers unreachable no matter how large the TTL value is set. We call this phenomena partial coverage problem. This problem is illustrated in Fig.1(a). The number by an edge is the latency between two logical nodes and the number in each node is the number of shared files on that peer. Suppose the size of selected neighbor subset is one and the metric used to select the neighbor is based on the number of shared files. We consider the scenario when the query source is A who has four neighbors (B, C, D, E). It will only send its query to C since C has the largest number of shared files (170). Similarly, C selects D who has the largest number of shared files in all C's neighbors (B, D, F, G) to relay A's query. Then D selects A in the same way, which leads to a loop query path: $A \rightarrow C \rightarrow D \rightarrow A$ . Thus, only three nodes are queried in the whole query process while all other nodes are invisible from the query source A. If we change the metric to be the smallest latency, the problem still exists because another loop is formed from source A, $A \rightarrow C \rightarrow B \rightarrow A$ . It is very possible that the query cannot be satisfied in the loop. This problem can be less serious when the size of the query subset increases, which will be discussed in Section 3.

![](images/6ce019307096681d3342b206b836b646f2c05c63bbc7ce2426d4aaff137d3384.jpg)



(a) Query path loops

![](images/b11cc847bece596c397ac747fa60392ca12eb41de5b14da0075a11fa86f9b614.jpg)



(b) Non-optimal query path   
Figure 1. The partial coverage problem

Many statistics-based search approaches use only one metric to collect statistics information to select relay neighbors, which does not always lead to an optimal search path. Figure 1(b) shows an example in which A is still the source node. When the search metric is the volume of shared data, the query path would be $A \rightarrow D \rightarrow E$ along which the query will check 250 files in 200 unit of time. But obviously if the query path is $A \rightarrow C \rightarrow G \rightarrow F \rightarrow H$ , the query can check 500 files in 20 units of time. The first path selected using one search metric is not as good as the second one.

# 3 Hybrid Periodical Flooding

In order to effectively reduce the traffic incurred by flooding-based search and alleviate the partial coverage problem, we propose Hybrid Periodical Flooding (HPF). Before discuss HPF, we first define Periodical Flooding.

# 3.1 Periodical flooding (PF)

We notice that in all the existing statistics-based search techniques, the number of relay neighbors, h, does not change at all peers along the query path. In the case of blind flooding, the phenomenon exhibits traffic explosion. The concept of periodical flooding tries to control the number of relay neighbors based on the TTL value along the query path. More specifically, given a peer with n logical neighbors and the current value of TTL, the number of relay neighbors, h, is defined by the following function $h=f(n,TTL)$ . Thus, in blind flooding (BFS), we have $h=f_{\mathrm{BFS}}(n,TTL)=n$ . In DFS, we have $h=f_{\mathrm{DFS}}(n,TTL)=1$ .

The function $h=f(n,TTL)$ can be viewed as a periodical function that changes as TTL changes. We call a search mechanism using a periodical function as periodic flooding (PF), in which the query mechanism is divided into several phases that are periodically repeated. We call the number of different repeated phases as a cycle, C. In all existing statistics-based search techniques, they all have a cycle of C=1, which are special cases of PF. We can ask the following questions in order to design an efficient search mechanism. In what conditions does a search mechanism with C=1 behave better than a search mechanism with C>1? What is the optimal value of C in terms of a desired performance metric under different underlying physical network topologies? For a given C, what is the optimal number of relay neighbors? One example of PF functions with C=2 is shown below:

$$
f (n, T T L) = \left\{ \begin{array}{l l} \left[ \frac {1}{2} n \right], & \text { if   } T T L \text {   is   odd } \\ \left[ \frac {1}{3} n \right], & \text { if   } T T L \text {   is   even } \end{array} \right.
$$

![](images/25df9a06c30c0c9cbc43015594b2cb3a594ddc4946dc6da83a44e277240c2b6e.jpg)



(a) BFS

![](images/515d14ac7c1cd0a9cd908c20335fc06984c01c0b457f719547ea2d252996238c.jpg)



(b) PF   
Figure 2. Comparison between BFS and a PF

We compare BFS and the example PF in Fig. 2. Suppose peer O initiates a query. Blind flooding (BFS) is employed in Fig. 2(a) where the query is sent or forwarded 36 times to reach all the nodes. We use thin connections to represent the links on which the query traverses once and thick connections to represent the links on which the query traverses twice. We have explained that for each query, each peer records the neighbors, which forward the query to it. Thereby on each link, at most two query messages can be sent across it. When a link is traversed twice, the unnecessary traffic is incurred. For example, one of the messages from A to B and from B to A is unnecessary. These redundant messages are shown in Fig. 2(a) using dotted arrows.

Figure 2(b) illustrates the query process of the example PF. Peer O has 4 neighbors and has TTL=7. We randomly select relay neighbors. Peer O will select 2 nodes (that is n/2=2 since TTL=7 that is odd), peers A and C, as relay neighbors. Peer A has 5 neighbors. It will select 2 neighbors (G and I) to relay the query initiated from peer O since TTL=6 and $h=\lceil n/3\rceil=2$ . Similarly, peer C relays the query to peer B and N (TTL=6 and $h=\lceil n/3\rceil=2$ ). Although the redundancy problem still exists in PF (such as the traffics from B to J and from I to J), it is significantly reduced compared with that of BFS.

Table 1. PF and Blind Flooding 

<table><tr><td></td><td>TTL</td><td>Query Msg</td><td>New Peers</td><td>Msg Per Peer</td></tr><tr><td rowspan="3">BFS</td><td>7</td><td>4</td><td>4</td><td>1.00</td></tr><tr><td>6</td><td>17</td><td>8</td><td>2.12</td></tr><tr><td>5</td><td>15</td><td>2</td><td>7.50</td></tr><tr><td rowspan="3">PF</td><td>7</td><td>2</td><td>2</td><td>1.00</td></tr><tr><td>6</td><td>4</td><td>4</td><td>1.00</td></tr><tr><td>5</td><td>9</td><td>8</td><td>1.12</td></tr></table>

Table 1 compares the redundancy degree of both PF and BFS. It presents the query messages relayed to new peers. For example, in BFS, peers with TTL=5 relay the query to 15 peers, but only 2 of the 15 peers receive the query first time. In PF, peers with TTL=5 relay the query to 9 peer of which 8 are first time receivers. That means for peers with TTL=5, BFS sends 7.5 queries to one new queried peer in average, while PF only sends 1.12 queries to one new queried peer in average. An efficient mechanism should query more peers using less messages. Thus PF is much more efficient than BFS in terms of traffic volume.

# 3.2 Hybrid Periodical Flooding

# HPF Overview

After determining the number of relay neighbors $(h)$ , a peer decides which h nodes should be selected. A simple approach called Random Periodical Flooding (RPF) selects h relay neighbors at random. Selecting relay neighbors more objectively may result in better performance. For example, we may use the shared data volume as a metric to select query neighbors if we find that peers with more shared data are more likely to satisfy queries. By selecting the neighbors with larger number of shard data, a query is more likely to succeed in less number of hops than that of random selection. We may also use the latency between the peer and its neighbors as a metric to select neighbors. In this case, for a given TTL value, a query will experience a shorter delay. If we consider multiple metrics in relay neighbor selection, the search mechanism is expected to have better performance. This motivates us to propose Hybrid Periodical Flooding (HPF) in which the number of relay neighbors can be changed periodically based on a periodical function and the relay neighbors are selected based on multiple metrics in a hybrid way.

HPF differentiates with RPF in that RPF selects relay neighbors randomly, and differentiates with DBFS in that DBFS only uses one metric to select relay neighbors. HPF selects neighbors based on multiple metrics and provides flexibility to justify different parameters to improve overall performance. Let h denote the expected number of relay neighbors, which is given by $h = h_{1} + h_{2} + \ldots + h_{t}$ , where t is the number of metrics used in relay neighbor selection and $h_{i}$ is the number of relay neighbors selected by metric i.

# Metrics

There are many metrics that may be used to select relay neighbors, such as communication cost, bandwidth, number of returned results from the neighbor, average number of hops from the neighbor to peers who responded the previous queries, and so on. These metrics may have different weights for a system with different query access patterns or different performance requirements. For example, we may give higher weights to some metrics that are more sensitive to the performance in a specific system. We have $\sum_{i=1}^{t} w_{i} = 1$ , where $w_{i}$ is the weight assigned to metric $i (1 \leq i \leq t)$ . To alleviate the partial coverage problem, we select relay neighbors in a hybrid way. We select $h_{i}$ neighbors using metric i, where $h_{i}$ is determined by $h_{i} = \left\lceil h \times w_{i} \right\rceil$ . Let $S_{i}$ denote the set of neighbors selected based on the metric i. The complete set of relay neighbors is $S = \bigcup_{i=1}^{t} S_{i}$ , where $h_{i} = |S_{i}|$ . Note that a neighbor may be selected by more than one metric. Thus, the actual number of relay neighbors selected may be less than h.

# Termination of Search Queries

A query process is terminated when a pre-set TTL value has been decreased to zero. Choosing an appropriate TTL value is very difficult. A large TTL may cause higher traffic volume, while a small TTL may not respond with enough number of query results. Furthermore there are no mutual feedbacks between the source peer and the peers who forward or respond the query. Thus it is hard for peers to know when to stop forwarding the query before the TTL value is reduced to zero.

Iterative Deepening [17] made an effort to address this problem in some degree. In Iterative Deepening, a policy P is used to control the search mechanism, which provides a sequence of TTLs so that a query is flooded from a very small TTL, and if necessary, to a gradually enlarged scope. For example, one policy can be $P=\{a, b, c\}$ , where P has three iterations. A query starts to be flooded with TTL=a. If the query cannot be satisfied, it will be flooded with TTL=b-a from all peers that are a hops away from the source peer. Similarly if the query still cannot be satisfied, it will be flooded with TTL=c-b from all peers that are b hops away from the source peer. In this policy, c is the maximal length of a query path. Iterative Deepening is a good mechanism in the sense that it alleviates the process time of middle nodes between iterations.

In HPF, we use this policy to terminate the successful queries without incurring too much unnecessary traffic. Since the combination is quite straightforward and the performance of Iterative Deepening policy has been evaluated in $[17]$ , this policy will not be re-evaluated in this paper.

# 4 Simulation Methodology

We use simulation to evaluate the performance of RPF and HPF and analyze the effects of the parameters.

# 4.1 Topology Generation

Two types of topologies, physical topology and logical topology, have to be generated in our simulation. The physical topology should represent the real topology with Internet characteristics. The logical topology represents the overlay P2P topology built on top of the physical topology. All P2P nodes are in the node subset of the physical topology. The communication cost between two logical neighbors is calculated based on the physical shortest path between this pair of nodes. To simulate the performance of different search mechanisms in a more realistic environment, the two topologies must accurately reflect the topological properties of real networks in each layer.

Previous studies have shown that both large scale Internet physical topologies $[15]$ and P2P overlay topologies follow small world and power law properties. Power law describes the node degree while small world describes characteristics of path length and clustering coefficient $[2]$ . Studies in $[12]$ found that the topologies generated using the AS Model have the properties of small world and power law. BRITE $[1]$ is a topology generation tool that provides the option to generate topologies based on the AS Model. Using BRITE, we generate 10 physical topologies each with 10,000 nodes. The logical topologies are generated with the number of peers ranging from 1,000 to 5,000. The average number of edges of each node is ranging from 6 to 20.

# 4.2 Simulation Setup

The total network traffic incurred by queries and average response time of all queries are two major metrics that we use to evaluate the efficiency of a search mechanism. High traffic volume will limit system scalability and long response time is intolerable for users. Network administrators care more about how much network bandwidth consumed by a P2P system, while users care more about the response time of queries, which is viewed as a part of service quality of the system.

![](images/844bddcf9139b293dba74ce91a237a5c2381c12dff8e8b3306246a2581ce9073.jpg)



Figure 3. Node distribution vs. coverage size. (h=1, metric 2)

![](images/eadaa2866039ea7b45e99c1ffaa9ffe66b61ca45b05942192fe2459598c56b8f.jpg)



Figure 4. Node distribution vs. coverage size. (h=2, metric 2)

![](images/1731a33a9c3b4280bfe2a2c679f68ca88166b82df8ddce807118ca5421f7a741.jpg)



Figure 5. Node distribution vs. coverage size. (h=1, metric 1)

In our simulation, we consider two metrics with the same weight to select relay neighbors in HPF. In practice, more metrics could be used for neighbor selection. The two metrics are the communication cost (metric 1) that is the distance between a peer and its neighbor and the shared number of files (metric 2) on each node. Based on the first metric, a peer will select the neighbors with the less communication costs. Based on the second metric, a peer will select the neighbors with the larger amount of shared data.

For each given search criterion, we distribute 100 files satisfying the search on the peers in a generated P2P topology. That means there are totally 100 possible results for a specific query in the whole P2P network. The distribution of the 100 files on the network is random. For each peer, we generate a number within 1 to 1000 as the number of shared files in this peer. Based on the second metric in selecting relay neighbors, a neighbor with more shared files is more likely to return a response than a neighbor with less shared files.

# 5 Performance Evaluation

In this section, we present the simulation results to show the effectiveness of HPF compared with DBFS and BFS.

# 5.1 Partial Coverage Problem

Based on $[3, 17]$ , statistics-based search mechanisms are more efficient and incur less traffic to the Internet compared with blind flooding. However, statistics-based search mechanisms have partial coverage problem as we discussed in Section 2.4. We quantitatively illustrate the partial coverage problem in this section.

We first illustrate the case in which only one relay neighbor is selected to send/forward a query $(h=1)$ based on the number of shared files in neighbors. We set TTL as infinity. Figure 3 shows the node distribution versus the number of peers being queried, which is defined as coverage size. For example, queries initiated from 8% of peers can only reach 10 other peers. Most of peers can only push their queries to 10 to 30 other peers. This means that loops are formed and only a very small number of peers can be reached for any queries. Note that the overlay network has 1000 nodes and the physical network has 10,000 nodes. Figure 4 illustrates the node distribution versus the coverage size, where h=2 and TTL=infinity. The coverage size is about 400 peers in average, which is still a small number in a P2P network.

Figure 5 shows node distribution versus coverage size when we use network latency as the metric to select relay neighbors. Again, we see the partial coverage problem. The partial coverage problem will disappear when h=n, which is the case of blind flooding. We did the same group of simulations on different topologies using different metrics. The results are quite consistent. Figure 6 shows the percentage of covered peers to total peers versus the number of relay neighbors (h=1, 2, n/5, n/4, n/3, n/2, and $Sqrt(n)$ ). The percentage of coverage is larger for a larger h. A larger h means a smaller chance for all reached peers to form a loop.

![](images/8bab921bd08dab67aa7f91538598702e2944937b1ac1ee453b81c89104c4198e.jpg)



Figure 6. Percentage of coverage vs. the number of relay neighbors

# 5.2 Performance of Random PF

We have evaluated network traffic and average response time of RPF that selects relay neighbors at random. We can use many different periodical flooding functions to determine the number of relay neighbors. These functions should not be over complicated. We have tried tens of periodical flooding functions with different C.

![](images/25de7208bdd97af2ea45d9034558f768f02fd31fe0dde4c2d22b9b85d69802ff.jpg)



Figure 7. Normalized traffic of RPF

![](images/4b59ae5532fb4e24592777452fbf04ffa8dc80700d3f12237f5395f4b708e006.jpg)



Figure 8. Normalized response time of RPF

![](images/b4f3a3df31e99d3cd366e065858618d9f4f349607398e85416f0fac52df9204f.jpg)



Figure 9. Normalized traffic comparison

Figures 7 and 8 show the normalized network traffic cost and normalized average response time versus the required number of response results. The traffic and average response time always perform in opposite way. If a search mechanism causes low traffic, it will suffer from high response time and vice versa. RPF is designed to provide an opportunity to have a tradeoff between total traffic and average response time, thus obtaining a better overall search performance. We may expect a search mechanism to reduce a large amount of traffic by increasing a little more response time or vice versa. How to quantitatively measure the overall performance based on the tradeoff is an issue.

It's hard to find the best search mechanism. We define $p$ to measure the overall performance, where $p = \lambda_{C} \text{traffic} + \lambda_{R} \text{time}$ , traffic and time are normalized value of total network traffic and average response time, $\lambda_{C}$ and $\lambda_{R}$ are the weight parameters for network traffic and response time, and $\lambda_{C} + \lambda_{R} = 1$ . We seek an asymptotically periodical flooding function $f_{a}(n,TTL)$ such that $p$ can be minimal or close to minimal. If a system emphasizes more on low network traffic, we can set $\lambda_{C} > \lambda_{R}$ ; otherwise, we can set $\lambda_{C} < \lambda_{R}$ for a system emphasizing more on quick response time.

Based on different topologies with different number of average connections, and different values of $\lambda_{C}$ and $\lambda_{R}$ , the functions of $f_{a}(n,TTL)$ may be derived differently. In our simulation of HPF, the average number of edge connections is 10. We choose $\lambda_{C}=0.6$ and $\lambda_{R}=0.4$ . Thus, the corresponding period function is derived as:

$$
f (n, T T L) = \left\{\begin{array}{l}\left\lceil \frac {1}{2} n \right\rceil , \text {if} T T L \text {is odd}\\\left\lceil \frac {1}{4} n \right\rceil , \text {if} T T L \text {is even}\end{array}\right.
$$

# 5.3 Effectiveness of HPF

HPF selects relay neighbors based on multiple metrics in a hybrid way. We use communication cost and the volume of shared data as two metrics to select relay neighbors.

Based on the simulation over 10,000 queries, Figure 9 shows the normalized network traffic versus the required number of response results of four different search mechanisms: BFS, RPF, DBFS and HPF. DBFS reduces the network traffic by 30\~50% compared with BFS. HPF outperforms DBFS by up to 20%. Figure 10 compares the normalized response time of four different search mechanisms over 10,000 queries versus the required number of response results. HPF performs the best compared with RPF and DBFS, but still worse than BFS. DBFS selects relay neighbors who have the largest volume of shared files. Each query may get more results by reaching fewer peers. HPF needs to query more peers to obtain the same amount of results than DBFS but much less than BFS and RPF. That is because we use multiple metrics instead of a single metric used in DBFS, expecting to obtain better overall performance, which has been shown in Figs. 9 and 10.

# 5.4 Alleviating the Partial Coverage Problem

HPF can effectively address the partial coverage problem discussed in Section 2.4. Figure 11 shows the percentage of queried peers as TTL increases. BFS can quickly cover 100% peers, while DBFS can only cover up to 77% peers in our simulation because of the partial coverage problem. DBFS still covers only around 77% when the value of TTL is set to infinity in our simulation. However, HPF and RPF can cover more than 96% peers as TTL is increased to 10.

Figure 12 compares the peer coverage size of DBFS and HPF. In DBFS, most nodes can cover 760-780 peers out of 1,000 nodes. The coverage size is increased to 950-970 in HPF.

![](images/9a1fbcbfc9806d685e5e3dd62951c573154d869b7454dd58f6a309c942d8f52c.jpg)



Figure 10. Normalized response time comparison

![](images/e73a88ceb20621f385a47c45a6f1cf69a86ba42cc92bde0d5228c53e4318dfc6.jpg)



Figure 11. Coverage percentage comparison

![](images/530ab4d6ee038e15509fa1fa62f1aec60844d39c17af42541a0b01cd918cb724.jpg)



Figure 12. Partial coverage comparison

# 6 Conclusion

In this paper, we have proposed an efficient and adaptive search mechanism, Hybrid Periodical Flooding. HPF improves the efficiency of blind flooding by retaining the advantages of statistics-based search mechanisms and by alleviating the partial coverage problem. We summarize our contributions as follows:

- Analyze the current search mechanisms used and proposed in unstructured P2P networks.   
- Qualitatively and quantitatively analyze the partial coverage problem caused by statistics-based search mechanisms, such as DBFS.   
- Propose to use a periodical flooding function to define the number of relay neighbors, which can be adaptively changed. This is the first technique used in HPF.   
- Propose to use multiple metrics to select relay neighbors to obtain better overall performance or adaptively meet different performance requirements, which is the second technique used in HPF.

We have shown the performance of HPF using two metrics to select relay neighbors. HPF provides the flexibility to use more metrics and allows the application to define multiple metrics and give them different weights, thereby the algorithm is more flexible in practice to meet different performance requirements.

# References

[1] BRITE, http://www.cs.bu.edu/brite/.   
[2] T. Bu and D. Towsley, On distinguishing between Internet power law topology generators, In Proceedings of IEEE INFOCOM'02 Conference, 2002.   
[3] A. Crespo and H. Garcia-Molina, Routing indices for peer-to-peer systems, In Proceedings of 22nd International Conference on Distributed Computing Systems, 2002.

[4] E. Cohen, A. Fiat, and H. Kaplan, Associative search in peer to peer networks: harnessing latent semantics, In Proceedings of the IEEE INFOCOM'03, 2003.   
[5] Fasttrack, http://www.fasttrack.nu/.   
[6] Freenet, http://freenet.sourceforge.net.   
[7] Gnutella, http://gnutella.wego.com/.   
[8] KaZaA, http://www.kazaa.com.   
[9] B. Krishnamurthy and J. Wang, Automated traffic classification for application-specific peering, In Proceedings of ACM SIGCOMM Internet Measurement Workshop, November 2002.   
[10] Q. Lv, et al., Search and replication in unstructured peer-to-peer networks, In Proceedings of the 16th ACM International Conference on Supercomputing, 2002.   
[11] Ritter, Why Gnutella can't scale. No, really. http://www.tch.org/gnutella.html.   
[12] S. Saroiu, P. Gummadi, and S. Gribble, A measurement study of peer-to-peer file sharing systems, In Proceedings of Multimedia Computing and Networking (MMCN), 2002.   
[13] S. Sen and J. Wang, Analyzing peer-to-peer traffic across large networks, In Proceedings of ACM SIGCOMM Internet Measurement Workshop, 2002.   
[14] K. Sripanidkulchai, B. Maggs, and H. Zhang, Efficient content location using interest-based locality in peer-to-peer systems, In Proceedings of INFOCOM'03, 2003.   
[15] H. Tangmunarunkit, et al., Network topology generators: degree-based vs. structural, In Proceedings of In Proceedings of SIGCOMM'02, 2002.   
[16] B. Yang and H. Garcia-Molina, Designing a super-peer network, In Proceedings of the 19th International Conference on Data Engineering (ICDE), March 2003.   
[17] B. Yang and H. Garcia-Molina, Efficient search in peer-to-peer networks, In Proceedings of ICDCS'02, 2002.