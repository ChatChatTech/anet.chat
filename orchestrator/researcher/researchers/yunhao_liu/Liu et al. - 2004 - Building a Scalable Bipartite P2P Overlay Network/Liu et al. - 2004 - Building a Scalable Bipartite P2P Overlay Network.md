# Building a Scalable Bipartite P2P Overlay Network

Yunhao Liu, Li Xiao

Dept. of Computer Science and Engineering

Michigan State University

East Lansing, MI 48824, USA

{liuyunha, lxiao}@cse.msu.edu

Lionel M. Ni

Dept. of Computer Science

Hong Kong University of Science & Technology

Kowloon, Hong Kong, China

ni@cs.ust.hk

# Abstract

In unstructured peer-to-peer (P2P) systems, the stochastic peer connection and peers' randomly joining and leaving a P2P network without any knowledge about underlying physical topology can cause serious topology mismatching between the P2P overlay network and the physical underlying network. Some existing techniques have been proposed to address topology mismatching problem without shrink search scope. However, these techniques involve considerable amount of overhead, and have other disadvantages, such as slow convergence speed and synchronization requirement. To address the limits of existing solutions, we propose a scalable bipartite overlay (SBO) among peers in Gnutella-like systems or among the super-peers in KaZaA-like systems. SBO employs an efficient strategy to reduce optimization overhead by intelligently distributing optimization tasks in different peers. Our evaluations show that the total traffic and response time of the queries can be significantly reduced by optimized SBO without shrinking the search scope.

# 1. Introduction

In a peer-to-peer system, each peer acts as both a client who requests information and services, and a server who produces and/or provides information and services. Decentralized unstructured P2P systems, such as Gnutella [3] and KaZaA [5], are commonly used in practice. File placement is random in these systems, which has no correlation with the network topology [27]. The most popular search mechanism in use is to blindly “flood” a query to the network among peers (such as in Gnutella) or among super-peers (such as in KaZaA).

Studies in $[17, 20, 22]$ have shown that P2P traffic contributes the largest portion of the Internet traffic based on their measurements on some popular P2P systems $[2]$ . A large portion of the heavy P2P traffic caused by inefficient overlay topology and the blind flooding is unnecessary, which makes the unstructured P2P systems being far from scalable [18]. The stochastic peer connection and peers' randomly joining and leaving a P2P network without any knowledge about the underlying physical topology form the inefficient overlay that mismatches with the underlying physical network.

Most existing overlay topology optimization studies use different techniques (e.g., [11, 16, 26]) to identify physical closer nodes to connect as overlay neighbors. These approaches could significantly shrink the search scope, which is not feasible in unstructured P2P systems. Two techniques have been proposed to address the topology mismatching problems without shrinking search scope, Adaptive Connection Establishment (ACE) [13] and Location-aware topology matching (LTM) [12]. In ACE, every single peer builds an overlay multicast tree among itself (source node) and the peers within a certain diameter from the source peer, and then optimizes the neighbor connections that are not on the tree, while retaining the search scope. In LTM, each peer issues a detector in a small region so that the peers receiving the detector can record relative delay information. Based on the delay information, a receiver can detect and cut most of the inefficient and redundant logical links, and add closer nodes as its direct neighbors. Both ACE and LTM can optimize the overlay without shrink search scope. However, ACE has a very slow convergence speed. LTM requires all the peering nodes to be synchronized, thus needs time synchronization protocol to support, such as NTP [6]. Both techniques also involve considerable amount of overhead because of the information exchanging among all pairs of neighbors.

To address the limits of existing solutions, we propose a scalable bipartite overlay (SBO) among peers in Gnutella-like systems or among the super-peers in Ka-ZaA-like systems. SBO employs an efficient strategy to distribute optimization tasks in peers with different colors. In SBO, each joining peer is assigned a color so that all peers are divided into two groups with white and red colors, respectively. Each peer is only connected with peers in a different color. Each white peer probes neighbor distances and reports the information to the red neighbors. Each red peer computes efficient forwarding paths. A white peer that is not on forwarding paths of a red peer then tries to find a more efficient red peer to replace this red neighbor. The average optimization overhead for each peer is reduced compared with other techniques since the optimization tasks are undertaken by peers with different colors. Our evaluations show that the total traffic and response time of the queries can be significantly reduced by optimized SBO without shrinking the search scope.

Our proposed SBO can be used to complement other search techniques, such as forwarding-based search mechanisms $[9, 10, 27]$ or cache-based schemes $[8, 14, 15]$ . In this paper, we will show this effectiveness by a case study of combining SBO and response index caching scheme, in which query responses are cached in passing peers along the returning path. Our study shows that to cover the same number of peers, the traffic cost is reduced by about 12 times and the average response time is reduced by around 5 times.

The rest of this paper is organized as follows. Section 2 analyzes the inefficient P2P overlay topologies. Section 3 presents the design of SBO and its optimization operations. Section 4 describes our simulation methodology. Performance evaluation of SBO is presented in Section 5, and we conclude the work in Section 6.

# 2. Inefficient Overlay Topologies

In a P2P system, all participating peers form a P2P network on top of an underlying physical network. A P2P network is an abstract, logical network called an overlay network. Maintaining and searching operations of a Gnutella peer are specifically described in $[4]$ . When a new peer wants to join a P2P network, a bootstrapping node provides the IP addresses of a list of existing peers in the P2P network. The new peer then tries to connect with some of these peers. If some attempts succeed, the connected peers will be the new peer's neighbors. Once this peer connects into a P2P network, the new peer will periodically ping the network connections and obtain the IP addresses of some other peers in the network. These IP addresses are cached by this new peer. When a peer leaves the P2P network and then wants to join the P2P network again (no longer the first time), the peer will try to connect to the peers whose IP addresses have already been cached. The mechanism that a peer joins a P2P network, the fact of a peer randomly joining and leaving, and the nature of flooding search make an inefficient mismatched overlay network and cause large amount of unnecessary traffic. In this section, we first use examples to explain the message duplications and the mismatching problem. We then describe our proposed scalable bipartite overlay (SBO) in detail.

# 2.1 Unnecessary Message Duplications in Overlay Connections

Figure 1 shows some examples of P2P overlay topologies where solid lines denote overlay connections among logical P2P neighbors. Consider the case when node A issues a query. A solid arrow represents a delivery of the query message along one logical connection. In Gnutella, a peer forwards an incoming query message to all of its directly connected peers, except the one that delivered the incoming query. Thus, as shown in Figure 1(a), A's query is relayed by nodes B and C. Peer B forwards the query to C, while C also forwards the query to B. In this case, the pair of transmission between B and C is unnecessary message duplication. We can easily observe that the other three overlays shown in Figure 1(b)-(d) have less message duplications, while retaining the same search scope for this query.

![](images/9ab16f6db272722fab73d639122d29e92405f20b2e4004e00e3738320871f14d.jpg)



(a)

![](images/7405c544713ba9a22702ec4a27d2a65c00e76a4219e1dd84ea25a422962649fc.jpg)



(b)

![](images/dd8a7b5b12c083bf95e88bb6e7a14320d561eb8abbfd7dfbf2e754b3d5e6d96b.jpg)



(c)

![](images/b3c75ad3303ee6e33691df4782eba89c737c364f13dc5e2c95ca9422110ae362.jpg)



(d)   
Figure 1: Examples of P2P overlay topologies

However, we cannot draw the conclusion that the overlays in Figure 1(b)-(d) are better than the one in Figure 1(a) because the above discussion only takes message and traffic cost into consideration. In fact, compared with Figure 1(a), the overlays in Figure 1(b)-(d) have less overlay connections, but may cause longer average query response times/query latencies. For example, when A issues larger amount of queries and D has most of the desired data, the query response time/query latency in the overlay in Figure 1(b) will be much longer than that in other three overlays.

Generally, as long as cycles exist in search paths, there must be message duplications in overlay connections. Some peers, such as B and C, are visited by the same query message multiple times. If a peer receives a query message with the same Message ID (GUID) as the one it has received before, the peer will discard the message. Since a peer is aware of this kind of revisit, we call it a Revisit Known (RK) problem. The price of reducing RK duplications is the increment of query latency. Our first motivation of SBO is to reduce message duplications and attack RK problems with minimal increment of query response time, while retaining the same search scope of queries.

# 2.2 Message Duplications in Physical Links and Topology Mismatching Problem

We have discussed message duplications in overlay connections. However, for an overlay without RK problem, the same message still can traverse the same physical link multiple times, causing large amount of unnecessary traffic and increasing query response time. Here is an example. Suppose Figure 2(a) illustrates the underlying physical network of the overlay shown in Figure 1(b), where A, B, C and D are peering nodes and node Y is not a peering node. We can see that the query message along the overlay path A→B→C→D traverses physical link YB twice. Node Y is visited twice.

![](images/c76c3e4746e2ebbff5f093f92f9469658495b88ec1953d13537883e479c82046.jpg)



(a)

![](images/d85bf6677b10bd3858832205222ac44f5089cbb5117227603cd14a2ed0ba02a0.jpg)



(b)   
Figure 2: Example of physical topologies

Since node Y is not a peering node, the message duplication (revisit to Y) cannot be avoided. We may reduce the duplication between link YB by creating a direct connection between A and C, and disconnecting the logical link BC, as shown in Figure 1(d), but new duplications may occur in other links, such as YA. Later discussions in this paper will show that SBO will carefully choose the most efficient overlay connections under this situation by comparing the delay of logical connections and observing the behavior of each peering node.

Figure 2(b) shows another underlying physical network of the overlay shown in Figure 1(b). For a query message along the overlay path A→B→C→D, D is visited three times. Node D is a peering node, but in the first two visits, D is visited as a non-peering node. These first two visits are not known by the P2P application. We call this kind of revisits as a Revisit Not known (RN) problem. In this case, three physical links have been traverses twice, as shown in Figure 2(b), a topology mismatching problem occurs.

It is more effective to solve RN problems than RK problems since RN problems will not only increase message duplications/traffic cost as RK problems, but also increase query response time. In Figure 2(b), node D has been visited by the same query message twice before it ‘formally’ receives the query as a peering node. If we can replace the overlay in Figure 1(b) by the one in Figure 1(c) for physical topology in Figure 2(b), there will be no message duplications at all, and the response time from D to A will be decreased significantly. Our second motivation of SBO is to improve search performance by alleviating RN problems.

In fact, the stochastic peer connection and peers' randomly joining and leaving a P2P network can cause large amount of topology mismatching between the P2P logical overlay network and the physical underlying network. Studies in $[17]$ have shown that only 2 to 5 percent of Gnutella connections link peers within a single autonomous system (AS). But more than 40 percent of all Gnutella peers are located within the top 10 ASes. This means that most Gnutella-generated traffic crosses AS borders so as to increase topology mismatching costs. Our simulation results show that 744,734 out of 1,000,000 query responses traverse along mismatched paths, in each of which at least one of the peering nodes is visited as a non-peering node for more than once.

# 3. Scalable Bipartite Overlay

Optimizing inefficient overlay topologies can fundamentally improve P2P search efficiency. All the existing approaches, such as forwarding based and cache based improvement strategies, could be used on top of an efficient overlay. In this paper, we propose a design of scalable bipartite overlay (SBO) that effectively avoids RK and RN problems to improve search efficiency in unstructured P2P networks.

# 3.1 Design of Scalable Bipartite Overlay

Instead of flooding queries to all neighbors, SBO employs an efficient strategy to select query forwarding path and logical neighbors. In the first phase of SBO, each joining peer is randomly assigned a color so that all peers are divided into two groups with white or red colors, respectively. Each peer is only connected with peers in a different color. In the second phase, each white peer probes its distances with all its red neighbors and reports the information to the red neighbors. In the third phase, each red peer computes efficient forwarding paths so that the same search scope can be retained without the need to flood a query to all neighbors. In the fourth phase, a white peer who is not on the forwarding path tries to find a more efficient red peer to replace its current neighbor. Thus, the topology construction and optimization of SBO consist of four phases: bootstrapping a new peer, neighbor distance probing and reporting, forwarding connections computing, and direct neighbor replacement.

# Phase 1: bootstrapping a new peer

A typical unstructured P2P system provides several permanent well-known bootstrap hosts to maintain a list of recently joined peers so that a new incoming peer can find an initial host to start its first connection by contacting the bootstrap hosts. In the design of SBO, when a new peer is joining the P2P system, it will randomly take an initial color: red or white. A peer should keep its color until it leaves, and again randomly select a color when it rejoins the system. Thus, each peer has a color associated with it, and all peers are separated into two groups, red and white. In SBO, a bootstrap host will provide the joining peer a list of active peers with color information. The joining peer then tries to create connections to the different color peers in the list. Figure 3 illustrates a new peer's joining process. In such a way, all the peers form a bipartite overlay, in which a red peer will only have white peers as its direct neighbors, and vice versa.

![](images/8df768703be608f0632b839368c27a5b16f5031734a62e8fe5a27650e2c0652b.jpg)



Figure 3: Bootstrapping a new peer

Once a peer has joined the P2P system, it will periodically ping the network connections and obtain the IP addresses of other peers in the network, which will be used to make new connections for the peer's rejoining or in the case that the peer loses some of the connections with its neighbors due to the neighbors' departure or failure, or the faults in the underlying networks.

# Phase 2: neighbor distance probing and reporting by white peers

We use network delay between two peers as a metric for measuring the traffic cost between peers. We modify the Limewire implementation of Gnutella 0.6 P2P protocol [4] by adding one routing message type for a peer to probe the cost with its neighbors. Each white peer probes the costs with its immediate logical neighbors and forms a neighbor cost table, and sends this table to all its neighbors who are all red peers. The impact of the frequency of the white peers' probing and cost table reporting operation will be discussed in more detail in Section 5.

We use N(S) to denote the set of direct logical neighbors of node S, and use $N^{2}(S)$ to denote the set of peers being two hops away from S. Since each red peer, P, receives the cost table from its white neighbors about its all red neighbors, the red peer P has the information to obtain the overlay topology including P itself, N(P), and $N^{2}(P)$ , as illustrated in Figure 4(a). Note that in SBO the overlay forms a bipartite topology, so there is no connections between any pairs of peers in $N^{2}(P)$ . Thus, we only require all the white peers to probe the costs to their neighbors and send out the cost tables. There is no need for the red peers to probe the distance.

# Phase 3: forwarding connections computing by red peers

Based on obtained neighbor cost tables, a minimum spanning tree (MST) can be built by each red peer, such as P in Figure 4(b). Since a red peer builds a MST in a two-hop diameter, a white peer does not need to build a MST. The thick lines in the MST are selected as forwarding connections (FC), while the rest lines are non-forwarding connections (NFC). Queries are only forwarded along FCs. For example, in Figure 4(b), P will send/forward queries to A, B and F, but not E. Peer P also informs E that E is a non-forwarding neighbor. This information will be used by E in Phase 4, i.e., direct neighbor replacement.

Figure 4(c) illustrates how the query message from P is flooded along the connections based on Figure 4(a). We can see many message duplications, i.e. RK problem. The total traffic cost incurred by the query is: $3+6+5+5+12+3+5+6+9+9+15+11+11=100$ .

After FC computing in Figure 4(b), the traffic cost incurred by this query becomes: $3+6+5+3+5+6+15=43$ as shown in Figure 4(d).

Although FC computing can reduce a lot of traffic while retaining the same search scope, as we described earlier, the price is to sacrifice query response time, or the query latency. For instance, P issues a query, and E has the desired data. The response time in Figure 4(c) is $2 \times 12 = 24$ . After FC computing, the response time becomes $2 \times (3 + 6 + 5) = 28$ . Based on this observation, we will further improve our FC selecting algorithm later in this section.

![](images/601972b1fd2b99d7eb291b60fc2a971e1ac18c185d6de876a2d500f155adc62d.jpg)



(a)

![](images/c7c0898817d082613a4a6fa46e4147e73e7e3c6af88bf270885a2aa2c4f7e6d5.jpg)



(b)

![](images/134613282d6e6ace0da6c9df717fe6776832d2d40aa18f44a40440eb0180388f.jpg)



(c)

![](images/1f0791232d8ec9c6635b2370f54957367f07c87d3f929039b026f1c9f9a9d8f0.jpg)



(d)   
Figure 4: A red peer P has a small overlay topology of N(P) and $N^{2}(P)$ , and computes the efficient forwarding paths

# Phase 4: direct neighbor replacement by white peers

This operation is only conducted by white peers. The goal of neighbor replacement is to alleviate the topology mismatching problem, or RN problems. As we have explained, solving RN problem is essential since it will not only reduce message duplications and traffic cost, but also shorten the response times.

After computing a MST among the peers within two hops, a red peer P is able to send its queries to all the peers within two hops. Some white peers become non-forwarding neighbors, such as E in Figure 4. In this case, for peer E, P is no longer its neighbor. In the phase of direct neighbor replacement, a non-forwarding neighbor, E, will try to find another red peer being two hops away from P to replace P as its new neighbor.

Peer P will send the neighbor cost tables it collected from A, B and F to the non-forwarding neighbor E so that E has enough information to find another neighbor to form a more efficient topology. Having received the cost tables, E can obtain the overlay topology among P and the peers N(P) and $N^{2}(P)$ . In the design of SBO, E will probe the round trip times (RTTs) to all the red peers in $N^{2}(P)$ and sort the red peers according to their RTTs. Peer E then selects the one with the smallest RTT, e.g., peer D in Figure 5(a). There are three cases for peer E who finds D as its nearest red peer.

![](images/ee7821774ff8e2886300d9193714289de788af8b2b85b8c40f74f113fb1ee686.jpg)



![](images/fdb3d30cd936cae6b571c10a2769f7831d7bc30f0cd72048051be539cec7b183.jpg)



![](images/b2b994b9a8fd17d9a6e9d872348e6493d9bcd872d66cf96357ee1d516df7330b.jpg)



![](images/ea18a8c9810881e7c4589a14449ff4475ff478bfdae88630ff547d3864024b86.jpg)



Figure 5: An example of neighbor replacement

Case 1: The delay of ED is smaller than that of EP. The connection of ED will be created, and D becomes E's direct logical neighbor. The connection EP will be cut. Figure 5(b) is the topology after E connects with D, and disconnects with P.

Case 2: The delay of ED is larger than that of EP, but is smaller than the larger one of PF and FD. For example, if ED=13 in Figure 5(c), 12 < ED < 15. In this case, E will create the connection of ED and treat D as its direct neighbor. Peer E will not cut EP until it sends its neighbor cost table to D so that D still thinks the connection of EP exists. Note that the algorithm is fully distributed. Thus, when red peer D conducts the FC computing, F will become D's none-forwarding neighbor. The white peer F will conduct the same operations as what peer E has done, and may try to find a better red peer to replace node D as its neighbor.

Case 3: If ED has the largest delay among EP, PF and FD, peer E will pick the second nearest peer in $N^{2}(P)$ , such as C in Figure 5(d), and repeat the above process until it finds a better node to replace P as its neighbor, or until it has tried all the peers in $N^{2}(P)$ .

# 3.2 Further Improvements

Previous studies have shown that queries and queried data have significant locality $[21, 25]$ . A small number of peers issue a large portion of the queries and the 5% of the files accounts for 50% of all transfers. Peers' behaviors are different in the query frequency and response frequency. We define a query-heavy peer who issues queries frequently, and a response-heavy peer who often responds queries. We have discussed in the previous section that reducing RK duplication may lead to increase query response time. To avoid disconnecting a path from/to a query/response heavy peer, we further improve SBO by keeping some single direction connections (SDC).

Query-heavy peer: If the number of queries that a peer have issued or forwarded is 5 times more than the average number of queries in last minute (the number of 5 times is selected based on our simulation), it is defined as a query-heavy peer. In our simulation, with an average number of neighbors being 6, initial TTL=7, average peer lifetime of 10 minutes, and query frequency of 0.3 queries issued per peer per minute, we measured that the average number of queries processed (issued and forwarded) by each peer is about 15 to 25 per second. Thus, a peer is identified as a query-heavy peer if it processed more than 75 queries per second.

Response-heavy peer: In Gnutella protocol v0.6 [4], QueryHit (response) messages are sent along the same path that carried the incoming query message. In our simulation, a peer delivers or forwards 3 responses per minute in average. In SBO, a peer processed more than 20 responses in last minute is defined as a response-heavy peer (The number of 20 responses is selected based on our simulation).

Single Direction Connections (SDC): Every peer in SBO will monitor its own status. If a peer finds itself a query/response-heavy peer, it will report its status to all its neighbors. Thus, when a red peer computes FCs to form the forwarding paths, a white neighbor who is not a forwarding peer may be a query- or response-heavy peer. The connection between the red peer and the white peer will be set as a SDC. For example, if peer E in Figure 4(b) is a response-heavy peer, instead of setting PE as a non-forwarding connection, it will set PE as a SDC: P→E, where P will send/forward query messages to E while E will not send/forward any query messages to P. In this case, E will still do its neighbor replacement operation. The SDC: P→E will be disabled when E is no longer a response-heavy peer. If E is a query-heavy peer, connection PE will be set as SDC: E→P, where E will send/forward query messages to P while P will not send/forward any query messages to E.

The simulation results in Section 5 will show that the design of SDC further improves the system search performance.

# 3.3 Traffic Overhead of SBO Optimizations

The simplicity of blind flooding makes it very popular in practice. This mechanism relays a query message to all its logical neighbors, except the incoming peer. For each query, each peer records the neighbors that relay the query to it. A peer will discard a query message that has been received before. Therefore, in the worst case, the same query message can be sent on each logical link at most twice. For an overlay network with n peers, we use $c_{n}$ to denote the average number of neighbors, and use $c_{e}$ to denote the average number of physical links in each logical link. The total traffic caused by a query is less than or equal to $nc_{n}c_{e}$ . In a typical P2P system, the value of n (more than millions) is much larger than $c_{n}$ (less than tens) [22], so we can view both $c_{n}$ and $c_{e}$ as constant numbers. Thus, in the flooding-based search, the traffic incurred by one query from an arbitrary peer in a P2P network is $O(n)$ . As observed in [23], each peer issues 0.3 queries per minute in average. Thus, the per minute traffic incurred by a P2P network with n peers is $O(n^{2})$ .

One optimization step of SBO includes all white peers' neighbor distance probing/reporting and neighbor replacement. In the worst case, each white peer, P, needs to probe every peer in $N^{2}(P)$ . It is reasonable to assume that the traffic overhead of peer A probing peer B is equal to a query message traversing the connection AB twice. If each peer conducts SBO optimization operation k times per minute, the total traffic overhead per minute is:

$$
k \times \left(\frac {n}{2} \times \left(2 c _ {n} c _ {e} + c _ {n} c _ {e} + 2 c _ {n} ^ {2} c _ {e}\right)\right) = \frac {k c _ {n} c _ {e} (3 + 2 c _ {n})}{2} n
$$

Our simulation results will show that the optimal value for k is less than 1, so the per minute traffic overhead incurred by SBO to the P2P network is $O(n)$ . Compared with the query traffic savings, the traffic overhead from SBO optimization is relatively trivial.

# 4. Simulation Methodology

We use two performance metrics: average traffic cost, and query response time. Traffic cost is defined as network resource used in an information search process of P2P systems, which is mainly a function of consumed network bandwidth and other related expenses. Response time of a query is defined as the time period from when the query is issued until when the source peer received a response result from the first responder. We also define search scope as the number of peers that queries have reached in an information search process. Thus, with the same traffic cost, we aim to maximize the search scope; while with the same search scope, we aim to minimize the traffic cost.

Two types of topologies, underlying physical topology and overlay logical topology, are generated in our simulation. All P2P nodes in the overlay are in a subset of nodes in the physical topology. Previous studies have shown that both large scale Internet physical topologies $[24]$ and P2P overlay topologies $[19]$ follow the small world and power law properties. The study in $[19]$ found that the topologies generated using the AS Model have the properties of the small world and power law. BRITE $[1]$ is a topology generation tool that provides the option to generate topologies based on the AS Model. Using BRITE, we generate three physical topologies each with 27,000 nodes. The logical topologies are generated with the number of peers (nodes) ranging from 3,000 to 8,000. The average number of neighbors of each node is ranging from 4 to 10.

In our simulation, we simulate flooding search used in Gnutella network by conducting the Breath First Search algorithm from a specific node. A search operation is simulated by randomly choosing a peer as the sender. In our first simulation, 1,000,000 search operations are simulated.

P2P networks are highly dynamic with peers joining and leaving frequently. We simulate the joining and leaving behavior of peers via turning on/off logical peers. In our simulation, every node issues 0.3 queries per minute, which is calculated from the observation data shown in [23]. When a peer joins, a lifetime in seconds will be assigned to the peer. The lifetime of a peer is defined as the time period the peer will stay in the system. The lifetime is generated according to the distribution observed in [19]. The mean of the distribution is chosen to be 10 minutes [22]. The value of the variance is chosen to be half of the value of the mean. The lifetime will be decreased by one after passing each second. A peer will leave in next second when its lifetime reaches zero. During each second, there are a number of peers leaving the system. We then randomly pick up (turn on) the same number of peers from the physical network to join the overlay.

To investigate whether SBO could be employed together with other approaches, we also simulate a strategy of using index caching scheme on top of SBO, in which query responses are cached in passing peers along the returning path. In our simulation, each peer keeps a local cache and a response index cache. The size of a response index cache is bounded by 200 items. The average number of neighbors is 6.

# 5. Performance Evaluation

We present our simulation results in this section. Our simulation results on overlay networks of 3,000 nodes, 5,000 nodes, 7,000 nodes, and 8,000 nodes on top of 27,000-nodes Internet-like physical networks are consistent. Thus, we only present the results based on the overlay network with 7,000 nodes.

# 5.1 Effectiveness of SBO in Static Environments

We study the effectiveness of SBO in a static P2P environment where the peers do not join and leave frequently. This will show that without changing the overlay topology, how many SBO optimization steps are required to reach a better topology matching. Here one step we mean each red peer collects the neighbor cost tables from its neighboring white peers, and computes the efficient forwarding connections, and its neighbors finish neighbor replacement operations, if needed.

Note that in the design of SBO, if the reported information from all neighbors including neighbor status and cost tables are not changed, the red peer will not compute FCs. Consequently the neighboring white peers will not do the neighbor replacement operations.

The goal of SBO is to reduce traffic cost as much as possible while retaining the same search scope. We generate 500,000 queries, and simulate flooding search for different topologies with average neighbor number as 4, 6, 8 and 10 after each SBO optimization step. Figure 6 shows that the traffic cost decreases when optimization operations of SBO are conducted multiple times, where the search scope is all 7,000 peers. To cover the same search scope, SBO reduces the traffic cost significantly in first two optimization steps. We can see that the traffic cost reduction reaches to a threshold after eight to ten steps of SBO optimization.

Short query response time is always desirable in P2P systems. The simulation results in Figure 7 show that SBO can effectively shorten the query response time by about 60% in first 10 optimization steps. The tradeoff between query traffic cost and response time has been discussed in [28]. P2P systems with a large number of average connections offer a faster search speed while increasing traffic. One of the strengths of SBO is that it reduces both query traffic cost and response time without decreasing the query success rate.

Our other simulation results also show that different densities of logical peers or physical nodes will not impact the effectiveness of SBO. The average traffic cost is only proportional to the average number of neighbors and average cost of logical links, which is consistent with previous analysis.

# 5.2 SBO in Dynamic Environments

We further evaluate the effectiveness of SBO in dynamic P2P systems and explore the best frequency for each peer to conduct SBO optimization operations. The average number of logical neighbors we use is 6.

Compared with a Gnutella-like system, Figures 8 and 9 show the effectiveness of SBO on reducing average traffic cost and query response time as time goes. Since SBO optimizations add some traffic overhead due to the neighbor distance probing, cost table reporting and direct neighbor replacement, there exists an optimal frequency for each peer to conduct these operations independently.

In SBO, there are two ways for a white peer to decide when to conduct neighbor probing and reporting, namely periodic and event-driven. In periodic approach, each white peer conducts neighbor distance probing at every certain period of time, q. After probing the distances to all the neighbors, a white peer sends the cost table to its neighboring red peers. In event-driven approach, a white peer produces and sends an updated cost table to its neighboring red peers only if there is a change on its logical connections with its neighbors, such as on a neighbor's leaving or on a peer's joining as its new neighbor.

![](images/3f44a7ca176e68e359b1fa4e837d5f6607b3de1e814950bfcb16ac15963d6a6c.jpg)



Figure 6: Traffic reduction vs. optimization steps

![](images/ca5c68d172bea0863d90559d311fe6c1bf8acab6c77e408fff061fab221215cf.jpg)



Figure 7: Response time vs. optimization steps

![](images/fc5c07706da0f2c9370ecf94523b5fc5c37ea0d9e913b4b280a382c3ad280a5b.jpg)



Figure 8: Traffic cost reduction of SBO in a dynamic P2P environment

The value q is a critical factor for the performance of periodic approach. We have investigated the impact of different values of q ranging from 20s to 600s. Figures 8 and 9 show the results on some representative samples of q at 30s, 60s, 90s, and 120s, respectively, where x-axis indicates the time elapsed since the first probing or event occurred. A small q leads to a fast convergent speed. However, if q is too small, e.g. q=30, peers will conduct the optimization operations too often, making the overhead keep growing when the reduction of the traffic cost and response time have already reached a threshold. On the other hand, if q is too large, e.g. q=120, the frequency of optimization operations will not be enough to catch the changes of peers' frequent joining and leaving. Thus, the convergent speed is slow, and the reduction of traffic cost and response time is limited. We define the value of q to be optimal if it incurs the smallest traffic cost, which is the sum of the query flooding traffic and optimization operation overhead traffic, and the difference between its average response time and the response time threshold is no more than 5%. Figures 8 and 9 suggest that q=90s is optimal with about 85% reduction on traffic cost and 60% reduction on response time for the simulation setup with the given physical topology, average peer lifetime (10 minutes) and query frequency (0.3/minute). Our results for different setups show that the optimal q ranges from 60s to 90s as long as the average peer lifetime keeps at 10 minutes.

The value of q should be adaptive to the average peer lifetime in order to achieve optimal performance. Figures 8 and 9 also show that the periodic approach with q=90s outperforms even-driven approach on traffic reduction.

As we have mentioned, different values of average peer lifetime have been presented by previous studies [7, 19]. We further tune the average peer lifetime in our

![](images/f39a34ca27a3c6cd4db92581eb58d9a7a493fb6b39916d7eb8c4e820162e4c27.jpg)



Figure 9: Response time reduction in a dynamic P2P environment

![](images/39c07a001093973475eea1bcd7e8c1a07ff3be533185d2dca5799d3ff595e6a4.jpg)



Figure 10: Optimal SBO optimization time interval

simulation. Figure 10 shows that SBO optimization operations can be conducted less frequently if average peer lifetime is longer. From our simulation results, we find that if the average peer lifetime is longer than 37 minutes, the event-driven policy will outperform periodic policy.

In a super-peer P2P system, such as KaZaA, flooding based search is only employed among super peers. The mechanism to select super peers makes the super peers more stable than leaf peers. Thus, an event-driven policy is highly recommended when SBO is implemented among super peers.

# 5.3 SBO with SDC and Index Caching

We have discussed the design of SDC in Section 3.2 to further improve SBO. In this part, we evaluate SDC on top of SBO and a strategy of combining SBO with response index caching scheme. We compare the traffic cost and response time in a Gnutella-like system without any optimization, with query index caching only, with SBO optimization only, with SDC enabled SBO optimization, and with SDC enabled SBO optimization plus response index caching in Figures 11 and 12. The design of SDC can further improve average response time of SBO by about 25% with very trivial traffic cost increment. Also compared with SBO, by combining SDC enabled SBO with response index caching the traffic cost is reduced by about 50% without shrinking the search scope, and the average query response time is reduced by about 42%.

![](images/ba3e91ae16b76a6170cc0e8ec7f7271865098398088e7895ed30f6b535292f19.jpg)



Figure 11: Average traffic cost of five schemes

# 6. Conclusion

We have evaluated our proposed Scalable Bipartite Overlay, SBO, and its optimization operations in both static and dynamic environments. Simulations in static P2P environments show that the significant performance benefit of SBO is consistent with various network sizes and average numbers of neighbors. In simulation studies of dynamic environments, we have investigated the optimal SBO optimization policy and frequency in a more realistic P2P environment. The results show that SBO achieves about 85% reduction on traffic cost and about 60% reduction on query response time. The significant reduction of network traffic implies a better scalability of the proposed SBO optimization.

The impacts of peer average lifetime on optimal SBO optimization frequency have also been studied. We also show that our design of the single direction connection can further improve the performance of SBO. The ability that SBO can complement other advanced search approaches has been showed by a combination strategy of SBO with response index caching.

# References

[1] BRITE, http://www.cs.bu.edu/brite/   
[2] Fasttrack, http://www.fasttrack.nu   
[3] Gnutella, http://gnutella.wego.com/   
[4] The Gnutella protocol specification 0.6, http://rfc-gnutella.sourceforge.net   
[5] KaZaA, http://www.kazaa.com   
[6] NTP: The Network Time Protocol, http://www.ntp.org/

![](images/36cb6430f1dac6ed13bdfd12b5588aafa9b256c76823e7468bfe0b4f7aa7cf8e.jpg)



Figure 12: Average response time of five schemes

[7] R. Bhagwan, S. Savage, and G. M. Voelker, "Understanding Availability," Proceedings of the 2nd International Workshop on Peer-to-Peer Systems (IPTPS '03), 2003.   
[8] E. Cohen and S. Shenker, "Replication strategies in unstructured peer-to-peer networks," Proceedings of SIGCOMM, 2002.   
[9] S. Jiang, L. Guo, and X. Zhang, "LighFlight: An Efficient Flooding Scheme for File Search in Unstructured Peer-to-Peer Systems," Proceedings of International Conference on Parallel Processing (ICPP), 2003.   
[10] S. Jiang and X. Zhang, "FloodTrail: an efficient file search technique in unstructured peer-to-peer systems," Proceedings of IEEE GLOBECOM, 2003.   
[11] B. Krishnamurthy and J. Wang, "Topology modeling via cluster graphs," Proceedings of SIGCOMM Internet Measurement Workshop, 2001.   
[12] Y. Liu, X. Liu, L. Xiao, L. M. Ni, and X. Zhang, "Location-Aware Topology Matching in Unstructured P2P Systems," Proceedings of IEEE INFOCOM, 2004.   
[13] Y. Liu, Z. Zhuang, L. Xiao, and L. M. Ni, "A Distributed Approach to Solving Overlay Mismatch Problem," Proceedings of the $24^{th}$ International Conference on Distributed Computing Systems (ICDCS), 2004.   
[14] E. P. Markatos, "Tracing a large-scale peer to peer system: an hour in the life of gnutella," Proceedings of the 2nd IEEE/ACM International Symposium on Cluster Computing and Grid 2002, 2002.   
[15] D. A. Menasce and L. Kanchanapalli, "Probabilistic Scalable P2P Resource Location Services," ACM SIGMETRICS Performance Evaluation Review, vol. 30, pp. 48-58, 2002.   
[16] V. N. Padmanabhan and L. Subramanian, "An investigation of geographic mapping techniques for Internet hosts," Proceedings of ACM SIGCOMM, 2001.   
[17] M. Ripeanu, A. Iamnitchi, and I. Foster, "Mapping the Gnutella Network," IEEE Internet Computing, 2002.

[18] Ritter, “Why Gnutella can't scale. No, really”, http://www.tch.org/gnutella.html   
[19] S. Saroiu, P. Gummadi, and S. Gribble, "A Measurement Study of Peer-to-Peer File Sharing Systems," Proceedings of Multimedia Computing and Networking (MMCN), 2002.   
[20] S. Saroiu, K. P. Gummadi, R. J. Dunn, S. D. Gribble, and H. M. Levy, "An Analysis of Internet Content Delivery Systems," Proceedings of the 5th Symposium on Operating Systems Design and Implementation(OSDI), 2002.   
[21] M. T. Schlosser and S. D. Kamvar, "Availability and locality measurements of peer-to-peer file systems," Proceedings of ITCom: Scalability and Traffic Control in IP Networks, 2002.   
[22] S. Sen and J. Wang, "Analyzing peer-to-peer traffic across large networks," Proceedings of ACM SIGCOMM Internet Measurement Workshop, 2002.   
[23] K. Sripanidkulchai, “The popularity of Gnutella queries and its implications on scalability”, http://www-2.cs.cmu.edu/\~kunwadee/research/p2p/gnutella.html

[24] H. Tangmunarunkit, R. Govindan, S. Jamin, S. Shenker, and W. Willinger, "Network Topology Generators: Degree-Based vs. Structural," Proceedings of SIGCOMM, 2002.   
[25] Y. Xie and D. O'Hallaron, "Locality in Search Engine Queries and Its Implications for Caching," Proceedings of IEEE INFOCOM, 2002.   
[26] Z. Xu, C. Tang, and Z. Zhang, "Building topology-aware overlays using global soft-state," Proceedings of the $23^{rd}$ International Conference on Distributed Computing Systems (ICDCS), 2003.   
[27] B. Yang and H. Garcia-Molina, "Efficient search in peer-to-peer networks," Proceedings of the $22^{nd}$ International Conference on Distributed Computing Systems (ICDCS), 2002.   
[28] Z. Zhuang, Y. Liu, L. Xiao, and L. M. Ni, "Hybrid Periodical Flooding in Unstructured Peer-to-Peer Networks," Proceedings of International Conference on Parallel Processing (ICPP), 2003.