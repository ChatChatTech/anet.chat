# Building Efficient Overlays

Yunhao Liu1, Li Xiao2, Lionel M. Ni1 and Yunhuai Liu1

1Department of Computer Science, Hong Kong University of Science and Technology, Kowloon, Hong Kong E-mail: {liu,ni,yunhuai}@cs.ust.hk   
2Department of Computer Science and Engineering, Michigan State University, East Lansing, MI 48824, USA E-mail: lxiao@cse.msu.edu

Key words: Adaptive overlay topology optimization (AOTO), Grid computing, Location-aware topology matching (LTM), Peer-to-peer, Search efficiency, Topology mismatch

# Abstract

Peer-to-peer (P2P) and Grid computing systems have emerged as popular models aiming at further utilizing Internet information and resources, complementing the available client–server services. However, the mechanism of peers randomly choosing logical neighbors without any knowledge about underlying physical topology can cause a serious topology mismatch problems between the overlay network and the physical underlying network. The topology mismatch problem brings a great stress in the Internet infrastructure and greatly limits the performance gain from various search or routing techniques in P2P and Grid systems. Aiming at alleviating the mismatch problem and reducing the unnecessary traffic, we have proposed two approaches, adaptive overlay topology optimization (AOTO) and location-aware topology matching (LTM) techniques, to reduce the total traffic cost and average query response time. Both AOTO and LTM are scalable and completely distributed in the sense that they do not require any global knowledge of the whole overlay network when each node is optimizing the organization of its logical neighbors. This paper shows the effectiveness of AOTO and LTM and compares the performance of these two approaches through simulation studies.

# 1. Introduction

Peer-to-peer (P2P) and Grid computing are two emerging approaches in the past several years, and many researchers believe that people will witness the convergence of P2P and grid computing before long [9]. In this paper, we discuss approaches on building efficient overlays by addressing mismatch problem in both of the systems. For simplicity of the discussion, we take P2P system as the example, and we argue that the proposed approaches could be employed in both P2P and grid computing systems.

In decentralized unstructured P2P systems, such as Gnutella [3] and KaZaA [5], file placement is random in these systems, which has no correlation with the network topology [30]. Unstructured P2P systems are most commonly used in today’s Internet. The most popular search mechanism in use is to blindly “flood” a query to the network among peers (such as in Gnutella) or among supernodes (such as in KaZaA). A query is broadcast and rebroadcast until a certain criterion is satisfied. If a peer receiving the query can provide the requested object, a response message will be sent back to the source peer along the inverse of the query path. This mechanism ensures that the query will be “flooded” to as many peers as possible within a short period of time in a P2P overlay network. A query message will also be dropped if the query message has visited the peer before.

Studies in [26] and [25] have shown that P2P traffic contributes the largest portion of the Internet traffic based on their measurements on some popular P2P systems, such as FastTrack (including KaZaA and Grokster) [2], Gnutella, and DirectConnect. Measurements in [22] have shown that even given that 95% of any two nodes are less than 7 hops away and the message time-to-live (TTL = 7) is preponderantly used, the flooding-based routing algorithm generates 330 TB/month in a Gnutella network with only 50,000 nodes. A large portion of the heavy P2P traffic caused by inefficient overlay topology and the blind flooding is unnecessary, which makes the unstructured P2P systems being far from scalable [23]. The mechanism of a peer randomly choosing logical neighbors without any knowledge about the underlying physical topology causes topology mismatch between the P2P logical overlay network and physical underlying network. Because of the mismatch problem, the same message may traverse the same physical link multiple times, causing a large amount of unnecessary traffic.

We had proposed two distributed approaches to address the topology mismatch problem: adaptive overlay topology optimization (AOTO) [14] and locationaware topology matching (LTM) scheme [11]. The goal of this paper is to compare these two approaches. AOTO is an algorithm of building a minimum spanning tree (MST) among each source node and its direct logical neighbors. Having the MST, query messages will only be forwarded to the direct neighbors on the MST, and the original neighbors who are not source node’s direct neighbor will be treated as non-flooding neighbors so as to reduce unnecessary message duplications. AOTO then alleviates the mismatch problem by choosing closer nodes to replace the non-flooding neighbors, while retaining the search scope. LTM is another algorithm in which each peer issues a detector in a small region so that the peers receiving the detector can record relative delay information. Based on the delay information, a receiver which receives duplicated detector messages can cut the inefficient and redundant logical links which cause the message duplications, and add closer nodes as its direct neighbors to solve mismatch problem. We compare these two approaches in terms of reduction ratio and convergent speed in dynamic P2P environments.

The rest of the paper is organized as follows. Section 2 presents related work. Section 3 discusses unnecessary traffic cost and topology mismatch problems. Section 4 introduces the adaptive overlay topology optimization (AOTO) and location-aware topology matching (LTM) schemes. Section 5 describes our simulation methodology. Performance comparison of the AOTO and LTM is presented in Section 6, and we conclude the work in Section 7.

# 2. Related Work

Many efforts have been made to avoid the large volume of unnecessary traffic incurred by the floodingbased search in decentralized unstructured P2P systems. In general, three types of approaches have been proposed to improve search efficiency in unstructured P2P systems: forwarding-based, cache-based, and overlay optimization. In forwarding-based approaches, instead of relaying the query messages to all its logical neighbors except the incoming peer, a peer selects a subset of its neighbors to relay the query [15, 30, 31]. The second approach is cache-based including data index caching and content caching [16, 17, 19, 25, 27, 30]. The third approach is based on overlay topology optimization that is closely related to what we are presenting in this paper [11–13, 21, 28, 29]. The three different kinds of approaches can be used together to complement each other.

There are mainly three types of solutions in topology optimization based approaches. End system multicast, Narada, was the first one to construct a rich connected graph on which to further construct shortest path spanning trees. Each tree is rooted at the corresponding source using well-known routing algorithms. This approach introduces large overhead when forming the graph and trees in a large scope, and does not consider the dynamic joining and leaving characteristics of peers. The overhead of Narada is proportional to the multicast group size. Researchers have also considered to cluster close peers based on their IP addresses (e.g., [10, 18]). Recently, researchers in [29] have proposed to measure the latency between each peer to multiple stable Internet servers called “landmarks”. The measured latency is used to determine the distance between peers. This measurement is conducted in a global P2P domain. In contrast, our measurement is conducted in many small regions, significantly reducing network traffic with high accuracy.

# 3. Topology Mismatch Problem

In a P2P system, all participating peers form a P2P network over a physical network. A P2P network is an abstract, logical network called an overlay network. Maintaining and searching operations of a Gnutella peer are specifically described in [4]. When a new peer wants to join a P2P network, a bootstrapping node provides the IP addresses of a list of existing peers in the P2P network. The new peer then tries to connect with these peers. If some attempts succeed, the connected peers will be the new peer’s neighbors. Once this peer connects into a P2P network, the new peer will periodically ping the network connections and obtain the IP addresses of some other peers in the network. These IP addresses are cached by this new peer. When a peer leaves the P2P network and then wants to join the P2P network again, the peer will try to connect to the peers whose IP addresses have already been cached. The mechanisms that a peer joins the P2P network by randomly picking some peers as its logical neighbors, and the nature of flooding search make an inefficient mismatched overlay network and cause large amount of unnecessary traffic.

![](images/298b2faed9f5e58e3fdae884dd17540ce33ad22e52f07255b5a0333ffc0f1bec.jpg)



Figure 1. Two examples of P2P overlay networks.

Figure 1 shows two examples of P2P overlay topology (A, B, and D are three participating peers) and physical topology (nodes A, B, C, and D) mappings, where solid lines denote physical connections and dashes lines denote overlay (logical) connections. Consider the case of a message delivery from peer A to peer B. In the left figure, A and B are both P2P neighbors and physical neighbors. Thus, only one communication is involved. In the right figure, since A and B are not P2P neighbors, A has to send the message to D before forwarding to B. This will involve 5 communications as indicated in Figure 1. Clearly, such a mapping creates much unnecessary traffic and lengthens the query response time. We refer to this phenomenon as topology mismatch problem.

# 4. AOTO and LTM

Before comparing the two approaches, in this section we first introduce AOTO and LTM, respectively.

# 4.1. AOTO

In most flooding-based decentralized P2P networks, such as Limeware (Gnutella), each peer forwards a query message to all of its logical neighbors. Most supernode-based P2P systems, such as KaZaA, also flood queries among supernodes. Figure 2(a) depicts an example of the underlying physical network topology, where the cost of each link is labeled by the link. Let node 1 be the source peer that will send flooding messages to other peers. For simplicity, we only consider total traffic (or cost) generated reaching nodes 2, 3, and 4 on three different P2P overlay topologies as shown in Figures 2(b), 2(c), and 2(d), respectively. We assume that a node reaches to another node through a shortest physical path based on the link cost, i.e. the end-to-end delay. Note that the two shaded nodes in Figure 2(a) are non-participating nodes in the P2P network.

In Figure 2(b), nodes 2, 3 and 4 are immediate logical neighbors of node 1. The shortest physical path from node 1 to node 4 is $1 \to 5 \to 2 \to s \to 4$ with a total cost of 9. Similarly, the costs from node 1 to nodes 2 and 3 are 3 and 15, respectively. Thus, the total cost of flooding a message from node 1 to nodes 2, 3, and 4 is $3 + 1 5 + 9 \ = \ 2 7$ . In Figure 2(c), node 3 is the only immediate logical neighbor of node 1 and nodes 2 and 4 are immediate logical neighbors of node 3. A message will be flooded from node 3 to nodes 2 and 4. The total cost from node 1 to nodes 2, 3, and 4 is $1 5 + 1 2 + 6 = 3 3$ , which is worse than the case of Figure 2(b). In Figure 2(d), node 1 can flood the message to all its neighbors, thus nodes 2, 3, and 4. However, node 2 does not know that node 3 will receive the message and will flood the message to node 3 as well. Similarly, node 4 will also flood the message to node 3. Thus, the total cost is $3 + 1 5 + 9 + 1 2 + 6 = 4 5 .$ .

Clearly, all the three inefficient overlay topologies generate a large amount of unnecessary traffic. Optimizing inefficient overlay topologies can fundamentally improve P2P search efficiency. One attempt is to build an overlay multicast tree among a node and its logical neighbors. In the case of Figure 2(d), an improved mechanism is shown as thick lines in Figure 2(e) in which the total cost from node 1 to nodes 2, 3, and 4 is $3 + 1 2 + 6 = 2 1$ . Although the cost is not as low as the optimal IP-level multicast, which is 15, the total cost has already been significantly reduced. This is the motivation that we propose the Adaptive Overlay Topology Optimization (AOTO) technique.

![](images/2240d49471d13097b8ff637035f0d5df30a4652d245d572dc29a8b81aa95c2e4.jpg)



(a)

![](images/3846c92991dca97b759b8853c69c60daa39d0ecfff96bea95a199ba7b4fe3094.jpg)



![](images/fa1c77c0e7b20f023b24dbc74dbffe73b5fc7bca4569d2c94591b99332756799.jpg)



![](images/09aa71f96e934067f51a991422eca5a88a0cbb1a164f11dfd74f461d422e6d0d.jpg)



(d)

![](images/b8029519194a9bb699864b6e6aac7d44aac6357512ba02c9b4d2b8500f0e92df.jpg)



Figure 2. Examples of different overlay topologies: (a) physical topology; (b) overlay topology 1; (c) overalay topology 2; (d) overalay topology 3; (e) an optimized topology.

While retaining the desired prevailing unstructured architecture of P2P systems, the goal of AOTO is to dynamically optimize the logical topology to improve the overall performance of P2P systems, which can be measured as query response time. AOTO includes two steps: Selective Flooding (SF) and Active Topology (AT). Selective Flooding is to build an overlay multicast tree among each peer and its immediate logical neighbors, and route messages on the tree to reduce flooding traffic without shrinking the search scope. Thus, some neighbors become non-flooding neighbors. Active Topology is the second step in AOTO for each peer to independently make optimization on the overlay topology to alleviate topology mismatch problem by replacing non-flooding neighbors with closer nodes as direct logical neighbors.

In the first step, instead of flooding to all neighbors, SF uses a more efficient flooding strategy to selectively flood a query on an overlay multicast tree. This tree can be formed using a minimum spanning tree algorithm among each peer and its immediate logical neighbors. In order to build the minimum spanning tree, a peer has to know the costs to all its logical neighbors and the costs between any pair of the neighbors. We use network delay between two nodes as a metric for measuring the cost between nodes. We modify the Limewire implementation of Gnutella 0.6 P2P protocol by adding one routing message type. Each peer probes the costs with its immediate logical neighbors and forms a neighbor cost table. Two neighboring peers exchange their neighbor cost tables so that a peer can obtain the cost between any pair of its logical neighbors. Thus, a small overlay topology of a source peer and all its logical neighbors is known to the source peer.

Compared with the flooding traffic, the traffic generated in SF due to exchanging neighbor cost tables is insignificant because such exchanges only occur between immediate neighbors. For a branching factor (i.e., average number of direct logical neighbors) of m and TTL (the number of times a message will be forwarded) of k, the flooding traffic is O(mN) for each query, where N is the total number of peers, which is typical in the range of millions and m is in the range of tens. The traffic increased due to exchanging neighbor cost tables is O(m) that is trivial. Based on obtained neighbor cost tables, a minimum spanning tree then can be built by simply using an algorithm like PRIM which has a computation complexity of O(m2). Now the message routing strategy of a peer is to select the peers that are the direct neighbors in the multicast tree to send its queries.

In the example of Figure 2(e), node 1 sends a message only to node 2 and expects that node 2 will forward the message to nodes 3 and 4. Note that in this step, even node 1 does not flood its query message to nodes 3 and 4 any more, node 1 still retains the connections with nodes 3 and 4 and keeps exchanging the neighbor cost tables. We call nodes 3 and 4 non-flooding neighbors, which are the peers to be optimized in the next step.

The second step of AOTO, AT, reorganizes the topology based on the information and the existing multicast tree produced by SF to effectively enlarge search scope. The idea of AT is to find peers that are closer to a source peer to replace the source peer’s nonflooding neighbors. Specifically in this design, node 1 will start AT from the farthest, non-flooding logical neighbor, such as node 3 in Figure 2. The next step is that node 1 needs to find another peer to replace node 3. Our strategy is finding a peer from node 3’s neighbor list. We have two reasons to do so. First, node 1 has node 3’s neighbor cost table with all the costs between node 3 and node 3’s logical neighbors. Second, it is easy to evaluate the new candidate’s property because node 1 knows the cost from this candidate to node 3 and the cost from node 3 to node 1. Node 1 then creates a connection with the candidate peer and probes the cost to the candidate. There are three circumstances for node 1 to decide if the candidate peer will be selected as its neighbor. We still take Figure 2(d) as an example.

It is obvious that we hope that the closest peer is chosen in the first time, such as node 5. If node 5 is chosen, the cost from node 1 to node 5 is only 1 (see the physical topology in Figure 2(a)) that is much smaller than the cost of 15 from node 1 to 3. In this case, node 1 will disconnect the connection with node 3 immediately, and select node 5 as its new direct logical neighbor.

If node 6 is chosen, the cost from node 1 to 6 is 20. Node 1 will not replace node 3 with node 6 since the cost to node 6 is larger than to node 3. When node 1 finds that the cost between node 3 and 6 is even larger, which is 30, node 1 will not disconnect the new connection with node 6. Since AT is conducted in each peer independently, node 1 cannot inform node 3 to disconnect the connection with node 6. However, as long as node 1 keeps both nodes 3 and 6 as its logical neighbors, we may expect that node 6 must become a non-flooding neighbor of node 3 after node 3 finishes its SF step since node 3 expects node 1 to forward messages to node 6 to reduce unnecessary traffic. Node 3 will try to find another peer to replace node 6 as its neighbor. After knowing that the connection of node 3 and 6 has been tore down from periodically exchanged neighbor cost tables from node 3 (or from node 6), node 1 will disconnect its connection with node 3 though it has already stopped sending query messages to node 3 for a period of time since the multicast tree is built for node 1.

If node 7 is taken, node 1 will not keep the connection with node 7 when node 1 finds out that the cost to node 7 is 21, larger than the cost between node 1 and 3, and the cost between node 3 and 7. Node 1 will then try another node 3’s logical neighbor that is not the logical neighbor of node 1.

# 4.2. LTM

Location-aware topology matching (LTM) consists of three operations: TTL2 detector flooding, low productive connection cutting, and source peer probing.

The first operation in LTM is TTL2-detector flooding. Based on Gnutella 0.6 P2P protocol, we design a new message type called TTL2-detector. In addition to the Gnutella’s unified 23-byte header for all message types, a TTL2-detector message has a message body in two formats. The short format is used in the source peer, which contains the source peer’s IP address and the timestamp to flood the detector. The long format is used in a one-hop peer that is a direct neighbor of the source peer, which includes four fields: Source IP Address, Source Timestamp, TTL1 IP Address, TTL1 Timestamp. The first two fields contain the source IP address and the source timestamp obtained from the source peer. The last two fields are the IP address of the source peer’s direct neighbor who forwards the detector and the timestamp to forward it. In the message header, the initial TTL value is 2. The payload type of the detector can be defined as 0 × 82.

Each peer floods a TTL2-detector periodically. We use d(i, S, v) to denote the TTL2-detector who has the message ID of i with TTL value of v and is initiated by S. We use N(S) to denote the set of direct logical neighbors of S, and use $N ^ { 2 } ( S )$ to denote the set of peers being two hops away from S. A TTL2- detector can only reach peers in N(S) and $N ^ { 2 } ( S )$ . We use network delay between two nodes as a metric for measuring the cost between nodes. The clocks in all peers can be synchronized by current techniques in an acceptable accuracy [6]. By using the TTL2- detector message, a peer can compute the cost of the paths to a source peer. As an example in Figure 3(a), when peer P receives a d(i, S, 1), it can calculate the cost of link SP from Source Timestamp and the time P receives the d(i, S, 1) from S. When P receives a d(i, S, 0), it can calculate the cost of link $\mathrm { S F _ { 1 } }$ from TTL1 Timestamp and Source Timestamp, and $\mathrm { F } _ { 1 } \mathrm { P }$ from TTL1 Timestamp and the time P receives the d(i, S, 0) from F1. As we can see in an inefficient overlay topology, the peers in set $N ^ { 2 } ( S )$ may receive d(i, S, v) more than once, such as peer P in Figure 3. If a peer receives d(i, S, v) multiple times, it will conduct the operations in the second step of LTM, low productive connection cutting.

In the second operation, low productive connection cutting, there are three cases for any peer P who receives d(i, S, v) multiple times.

![](images/8c4bd81518ceb2c4895e05ea45ba73237c58f1a353897a6cfd2a068c3d71a5a1.jpg)  
Figure 3. Peer P receives d(i, S, v) multiple times in LTM.

Case 1. P receives both d(i, S, 1) and d(i, S, 0) as shown in Figure 3(a). In this case, d(i, S, 1) comes from path SP, while d(i, S, 0) comes from $\mathrm { { S F _ { 1 } P _ { \cdot } } }$ The costs of $\mathrm { S P } , \mathrm { S F } _ { 1 }$ , and $\mathrm { F _ { 1 } P }$ can be calculated from the timestamps recorded in d(i, S, 0) and $d ( i , S , 1 )$ . If SP or $\mathrm { F } _ { 1 } \mathrm { P }$ has the largest cost among the three connections, P will put the respective connection into its will-cut list that is a list of connections to be cut later. If $\mathrm { S F _ { 1 } }$ has the largest cost, P will do nothing. Note that LTM is fully distributed and all peers do the same LTM operations. In the case of $\mathrm { S F _ { 1 } }$ having the largest cost, F1 will put this connection into $\mathrm { F } _ { 1 }$ ’s will-cut list. A peer will not send or forward queries to connections in its will-cut list, but these connections have not been cut in order for query responses to be delivered to the source peer along the inverse search path.

Case 2. P receives multiple d(i, S, 0)s from different paths. In LTM, P randomly takes two of the paths, such as $\mathrm { S F _ { 1 } P }$ and $\mathrm { S F } _ { 2 } \mathrm { P }$ in shown in Figure 3(b), to process at each time. Other paths, if any, will be handled in the next round of optimization. Thus, one important factor to affect the performance of LTM is the frequency for each peer to issue TTL2-detector messages. Simulation results in [11] show that the optimal LTM frequency is determined by the average peer lifetime and query frequency. Peer P can calculate the costs of $\mathrm { S F } _ { 1 } , \mathrm { S F } _ { 2 } , \mathrm { F } _ { 1 } \mathrm { P }$ and $\mathrm { F } _ { 2 } \mathrm { P } .$ If $\mathrm { P F } _ { 1 }$ or $\mathrm { P F } _ { 2 }$ has the largest cost, P will put it into its will-cut list. If $\mathrm { S F _ { 1 } }$ or SF2 has the largest cost, P will do nothing. As we have discussed above, $\mathrm { S F _ { 1 } }$ or $\mathrm { S F } _ { 2 }$ having the largest cost will be cut by one of the other three nodes.

Case 3. P receives one d(i, S, 1) and multiple d(i, S, 0)s as shown in Figure 3(c). In this case, P will process the path receiving d(i, S, 1) and one path randomly selected from the multiple paths of $d ( i , S , 0 ) \mathrm { s }$ forming a scenario of Case 1.

The third operation is source peer probing. For a peer P who receives only one d(i, S, 0) during a certain time period (e.g., 10 seconds), and

$$
\mathrm{P} \in \big (N ^ {2} (S) - N (S) \big),
$$

it will try to obtain the cost of PS by checking its cut list first. If S is not in the list, P will probe the distance to S (see Figure 4). After obtaining the cost of PS, P will compare this cost with the costs of SF1 and PF1. If PS has the largest cost, P will not keep this connection. Otherwise, this connection will be created. In the Internet, the cost of SP and the cost of PS may not be the same. We use the cost of PS to estimate the cost of SP.

# 4.3. Traffic Overhead of AOTO and LTM

The simplicity of blind flooding makes it very popular in practice. This mechanism relays a query message to all its logical neighbors, except the incoming peer. For each query, each peer records the neighbors that relay the query to it. Therefore, in the worst case, the same query message can be sent on each link at most twice as illustrated in Figure 1. For an overlay network with n peers, we use $c _ { n }$ to denote the average number of neighbors, and use $c _ { e }$ to denote the average cost of the logical links. The total traffic caused by a query is less than or equal to $n c _ { n } c _ { e }$ . In a typical P2P system, the value of n (more than millions) is much greater than $c _ { n }$ (less than tens) [26]. So we can view both $c _ { n }$ and $c _ { e }$ as constant numbers. Thus, in the flooding-based search, the traffic incurred by one query from an arbitrary peer in a P2P network is $O ( n )$ . As observed in [27], each peer issues 0.3 queries per minute in average. Thus, the per minute traffic incurred by a P2P network with n peers is $O ( n ^ { 2 } )$ .

![](images/b9710f4ec5209ba152362d458c8a8a3384ee482fc42d04c6fcc40d71cdfe27f3.jpg)



Figure 4. Source peer probing.

One optimization step of AOTO includes all peers probing neighbor distance and reporting cost table. In the worst case each peer P needs to probe every neighbor of non flooding neighbor’s neighbor N(G). Here we assume the traffic overhead of peer A probing peer B is equal to a query message traversing the connection AB twice. If each peer conducts AOTO optimization operation k times per minute, the total traffic overhead per minute is $2 k n c _ { n }$ .

Recall that each $d ( i , S , \upsilon )$ has a TTL value of 2 in a source peer. So the traffic for one time LTM optimization in all peers is at most $2 n c _ { n } ^ { 2 } c _ { e }$ . If each peer conducts LTM k times per minute, the total traffic is $2 k n c _ { n } ^ { 2 } c _ { e }$ .

We find the best value for k is 2 or 3. Thus, the per minute traffic overhead incurred by both AOTO and LTM to the P2P network is O(n). However, the hiding factor of AOTO’s overhead is smaller than LTM.

# 5. Simulation Methodology

A well-designed search mechanism should seek to optimize both efficiency and Quality of Service (QoS). Efficiency focuses on better utilizing resources, such as bandwidth and processing power, while QoS focuses on user-perceived qualities, such as number of returned results and response time. In unstructured P2P systems, the QoS of a search mechanism generally depends on the number of peers being explored (queried), response time, and traffic overhead. If more peers can be queried by a certain query, it is more likely that the requested object can be found. So we use two performance metrics: average traffic cost versus search scope and query response time.

Traffic cost is one of the parameters seriously concerned by network administrators. Heavy network traffic limits the scalability of P2P networks [23] and is also a reason why a network administrator may prohibit P2P applications. We define the traffic cost as network resource used in an information search process of P2P systems, which is mainly a function of consumed network bandwidth and other related expenses. Specifically, in this work, we assume all the messages have the same length, so when messages traverse an overlay connection during the given time period, the traffic cost $( T _ { \mathrm { c } } )$ is given by: $T _ { \mathrm { c } } = M \cdot L$ , where M is the number of messages that traverse the overlay connection, and L represents the number of physical links in this overlay connection.

Response time of a query is one of the parameters concerned by P2P users. We define response time of a query as the time period from when the query is issued until when the source peer received a response result from the first responder.

We first generate network topologies. Based on generated networks, we simulate P2P flooding search, host joining/leaving behavior, AOTO, and LTM. Two types of topologies, physical topology and logical topology, are generated in our simulation. BRITE [1] is a topology generation tool that provides the option to generate topologies based on the AS Model. Using BRITE, we generate two physical topologies each with 20,000 nodes. The logical topologies are generated with the number of peers (nodes) ranging from 2,000 to 8,000. The average number of neighbors of each node is ranging from 4 to 10.

Content popularity of a publisher follows Zipf-like distribution (aka Power Law) [7, 8], where the relative probability of a request for the ith most popular page is proportional to $1 / i \alpha .$ , with α typically taking on some value less than unity. The observed value of the exponent varies from trace to trace. The request distribution does not follow the strict Zipf’s law (for which $\alpha = 1 )$ , but instead does follow a more general Zipf-like distribution. In our simulation, we simulate flooding search used in Gnutella network by conducting the Breath First Search algorithm from a specific node, and the initial TTL value is defined as 7.

In dynamic P2P environment, every node issues 0.3 queries per minute, which is calculated from the observation data shown in [27], i.e., 12,805 unique IP addresses issued 1,146,782 queries in 5 hours. When a peer joins, a lifetime in seconds will be assigned to the peer. The lifetime of a peer is defined as the time period the peer will stay in the system. The lifetime is generated according to the distribution observed in [24]. The mean of the distribution is chosen to be 10 minutes [26].

# 6. Performance Comparison

We compare AOTO and LTM by simulations in this section. Our simulation results on overlay networks of 2,000 nodes, 3,000 nodes, 5,000 nodes, and 8,000 nodes on top of 20,000-nodes Internet-like physical networks are consistent. Due to the page limitation, we only present the results based on the overlay network with 8,000 nodes.

# 6.1. AOTO and LTM in Static Environments

In our first simulation, we study the effectiveness of AOTO and LTM in a static P2P environment where the peers do not join and leave frequently. This will show that without changing the overlay topology, how many optimization steps are required to reach a better topology matching.

The first goal of AOTO and LTM schemes is to reduce traffic cost as much as possible while retaining the same search scope. Figures 5 and 6 show the traffic cost reduction of AOTO and LTM, respectively.

In these figures, the curve of $\mathbf { \dot { c } } _ { n } n e i g h ^ { \prime }$ shows the average traffic cost caused by a query to cover the search scope in x-axis, where in the system the average number of logical neighbors is $c _ { n } .$ . We can see that the traffic cost decreases when AOTO and LTM are conducted multiple times, where the search scope is all 8000 peers. They both reach a threshold after several steps of optimization. AOTO may reduce traffic cost by around 65% while LTM reduces traffic cost by 85%. AOTO converges in around 10 steps while LTM can be converged as fast as in 2–3 steps. In this sense, LTM outperforms AOTO.

Short query response time is always desirable in P2P systems. The simulation results in Figures 7 and 8 show that AOTO can shorten the query response time by about 35% after 10 steps while the LTM will reduce response time by more than 60% in only 3 steps. The tradeoff between query traffic cost and response time has been discussed in [31]. P2P systems with a large number of average connections offer a faster search speed while increasing traffic. One of the strengths of AOTO and LTM schemes is that it reduces both query traffic cost and response time without decreasing the query success rate. Query success rate here is defined as the ratio of the queries for which at least one good answer is found in the system and successfully delivered to the requester.

# 6.2. AOTO and LTM in Dynamic Environments

We further evaluate the effectiveness of AOTO and LTM in dynamic P2P systems. In this simulation, we assume that peer average lifetime in a P2P system is 10 minutes; 0.3 queries are issued by each peer per minute; and the frequency for AOTO and LTM at

![](images/6c06c441fbbf3acb457a75b6f892582a444fbeb4e306845a9b94e22bba54e0ba.jpg)



Figure 5. Traffic reduction vs. optimization step in AOTO.

![](images/838a6bae04b96b4ea441082a4dc9702326d961ef00c73b18adb4da050dc952c8.jpg)



Figure 6. Traffic reduction vs. optimization step in LTM.

![](images/73c71e5876f8735277b2cdbdf139b51ae975f1f37884a2d7d5db43b00ec3edb6.jpg)



Figure 7. Average response time vs. opt. step in AOTO.

![](images/12026737f8aeb99d60edebd5bdbb762cbbabf86a8f143b160878335f9402237f.jpg)



Figure 8. Average response time vs. opt. step in LTM.

every peer to conduct optimization operations is twice per minute. Figure 9 shows the average traffic cost per query of Gnutella-like P2P systems, AOTO enabled Gnutella and LTM enabled Gnutella. Note that here the traffic cost includes the overhead needed by each operation in the optimization steps. Both AOTO and LTM could significantly reduce the traffic cost while retaining the same search scope. In order to keep the same search scope, AOTO and LTM may need a larger initial value of TTL. Figure 10 shows that with reduction of the traffic, the queries’ average response times of AOTO and LTM are also reduced in a dynamic environment.

In a dynamic P2P environment, we simulate AOTO and LTM employed together with other approaches, such as response index caching scheme or some forwarding based strategies [11]. We also obtained very good results. For example, using a 200 item size cache at each peer, AOTO with index cache will reduce 75% of the traffic cost and 70% of the response time, while LTM plus index caching could reduce traffic cost by more than 10 times and reduce average response time by 7 times.

![](images/ed112c5d37a0fa8b0ed9c62c74164858ba36a73b78bfc149a7261f0e988e18f7.jpg)



Figure 9. Average traffic cost comparison of AOTO and LTM in a dynamic P2P environment.

![](images/f76e88b3348e9076f932c9a77e888ce534ecfcbd207b4089098b178add68c046.jpg)



Figure 10. Average response time comparison of AOTO and LTM in a dynamic P2P environment.

# 7. Conclusion and Future Work

We have evaluated our proposed AOTO and LTM overlay topology matching algorithms in both static and dynamic environments. They are both fully distributed and scalable in that they do not need any global knowledge, and each peer conducts the algorithm independently. AOTO and LTM can be employed in both P2P and grid computing systems. Compared with traffic cost savings, the overhead incurred by these two algorithms is trivial.

LTM does show more advantages than AOTO. However, LTM creates slightly more overhead and requires that all peer clocks be synchronized, which requires additional overhead to run a clock synchronization protocol, such as NTP.

Future work will lead in two directions. One is to investigate the possibility of integrating AOTO and LTM with other existing advanced search approaches to further improve search performance. The other one is to deploy and test an AOTO and LTM prototype based on current version of Gnutella open source code in PlanetLab [20], an open, shared testbed for developing wide area network services.

# Acknowledgements

This work was partially supported by the US National Science Foundation (NSF) under grant ACI-0325760, by Michigan State University IRGP Grant 41114 and Hong Kong RGC Grants HKUST6264/04E.

# References

1. “BRITE”, http://www.cs.bu.edu/brite/   
2. “Fasttrack”, http://www.fasttrack.nu   
3. “Gnutella”, http://gnutella.wego.com/   
4. “The Gnutella Protocol Specification 0.6”, http: //rfc-gnutella.sourceforge.net   
5. “KaZaA”, http://www.kazaa.com   
6. “NTP: The Network Time Protocol”, http://www.ntp.org/   
7. V. Almeida, A. Bestavros, M. Crovella and A. d. Olivera, “Characterizing Reference Locality in the WWW”, in Proceedings of the IEEE Conference on Parallel and Distributed Information Systems (PDIS), 1996.   
8. L. Breslau, P. Cao, L. Fan, G. Phillips and S. Shenker, “Web Caching and Zipf-Like Distributions: Evidence and Implications”, in Proceedings of IEEE INFOCOM, 1999.   
9. I. Foster and A. Iamnitchi, “On Death, Taxes, and the Convergence of Peer-to-Peer and Grid Computing”, in Proceedings of 2nd International Workshop on Peer-to-Peer Systems (IPTPS), 2003.   
10. B. Krishnamurthy and J. Wang, “Topology Modeling via Cluster Graphs,” in Proceedings of SIGCOMM Internet Measurement Workshop, 2001.   
11. Y. Liu, X. Liu, L. Xiao, L. M. Ni and X. Zhang, “Location-Aware Topology Matching in Unstructured P2P Systems”, in Proceedings of IEEE INFOCOM, 2004.   
12. Y. Liu, L. Xiao and L.M. Ni, “Building a Scalable Bipartite P2P Overlay Network”, in Proceedings of 18th International Parallel and Distributed Processing Symposium (IPDPS), 2004.

13. Y. Liu, Z. Zhuang, L. Xiao and L.M. Ni, “AOTO: Adaptive Overlay Topology Optimization in Unstructured P2P Systems”, in Proceedings of IEEE GLOBECOM, 2003.   
14. Y. Liu, Z. Zhuang, L. Xiao and L.M. Ni, “A Distributed Approach to Solving Overlay Mismatch Problem”, in Proceedings of the 24th International Conference on Distributed Computing Systems (ICDCS), 2004.   
15. Q. Lv, P. Cao, E. Cohen, K. Li and S. Shenker, “Search and Replication in Unstructured Peer-to-Peer Networks”, in Proceedings of the 16th ACM International Conference on Supercomputing, 2002.   
16. E.P. Markatos, “Tracing a Large-Scale Peer-to-Peer System: An Hour in the Life of Gnutella”, in Proceedings of the 2nd IEEE/ACM International Symp. on Cluster Computing and the Grid, 2002.   
17. D.A. Menasce and L. Kanchanapalli, “Probabilistic Scalable P2P Resource Location Services”, ACM SIGMETRICS Performance Evaluation Review, Vol. 30, pp. 48–58, 2002.   
18. V.N. Padmanabhan and L. Subramanian, “An Investigation of Geographic Mapping Techniques for Internet Hosts”, in Proceedings of ACM SIGCOMM, 2001.   
19. S. Patro and Y.C. Hu, “Transparent Query Caching in Peerto-Peer Overlay Networks”, in Proceedings of the 17th International Parallel and Distributed Processing Symposium (IPDPS), 2003.   
20. L. Peterson, D. Culler, T. Anderson and T. Roscoe, “A Blueprint for Introducing Disruptive Technology into the Internet”, in Proceedings of HOTNETS, 2002.   
21. S. Ratnasamy, M. Handley, R. Karp and S. Shenker, “Topologically-Aware Overlay Construction and Server Selection”, in Proceedings of IEEE INFOCOM, 2002.   
22. M. Ripeanu, A. Iamnitchi and I. Foster, “Mapping the Gnutella Network”, IEEE Internet Computing, 2002.   
23. Ritter, “Why Gnutella Can’t Scale. No, Really”, http://www. tch.org/gnutella.html   
24. S. Saroiu, P. Gummadi and S. Gribble, “A Measurement Study of Peer-to-Peer File Sharing Systems”, in Proceedings of Multimedia Computing and Networking (MMCN), 2002.   
25. S. Saroiu, K.P. Gummadi, R.J. Dunn, S.D. Gribble and H.M. Levy, “An Analysis of Internet Content Delivery Systems”, in Proceedings of the 5th Symposium on Operating Systems Design and Implementation, 2002.   
26. S. Sen and J. Wang, “Analyzing Peer-to-Peer Traffic across Large Networks”, in Proceedings of ACM SIGCOMM Internet Measurement Workshop, 2002.   
27. K. Sripanidkulchai, “The Popularity of Gnutella Queries and Its Implications on Scalability”, http://www2.cs.cmu.edu/ \~kunwadee/research/p2p/gnutella.html   
28. M. Waldvogel and R. Rinaldi, “Efficient Topology-Aware Overlay Network”, in Proceedings of ACM HotNets, 2002.   
29. Z. Xu, C. Tang and Z. Zhang, “Building Topology-Aware Overlays Using Global Soft-State”, in Proceedings of the 23rd International Conference on Distributed Computing Systems (ICDCS), 2003.   
30. B. Yang and H. Garcia-Molina, “Efficient Search in Peer-to-Peer Networks”, in Proceedings of the 22nd International Conference on Distributed Computing Systems (ICDCS), 2002.   
31. Z. Zhuang, Y. Liu, L. Xiao and L.M. Ni, “Hybrid Periodical Flooding in Unstructured Peer-to-Peer Networks”, in Proceedings of International Conference on Parallel Processing (ICPP), 2003.