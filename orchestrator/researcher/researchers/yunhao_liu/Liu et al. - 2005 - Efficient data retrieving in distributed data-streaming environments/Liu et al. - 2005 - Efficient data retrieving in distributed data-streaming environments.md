# Efficient Data Retrieving in Distributed Datastreaming Environments

Yunhao Liu, Jun Miao, Lionel M. Ni, and Jinsong Han

Department of Computer Science

Hong Kong University of Science and Technology

Clear Water Bay, Kowloon, Hong Kong

{ liu, miaojun, ni, jasonhan }@cs.ust.hk

Abstract— In a potential distributed application, Automobile Tracking System (ATS), automobile location data is continuously generated, kept in a distributed manner. As large amount of traffic will be incurred during search process, it is critical to construct an efficient overlay multicast structure for the ATS so as to distribute traffic to all the physical links evenly, as well as balance the load among group members. In this paper, we propose a distributed protocol, MMT scheme, in which end hosts self-organize into multiple multicast trees. We evaluate the performance of MMT with comprehensive simulations. Experimental results show that MMT outperforms existing approaches in load balance, and its performance penalties are low from the network and the application perspectives.

Keywords: automobile tracking system, overlay multicast, load balance, multiple multicast tree (MMT) scheme.

# I. INTRODUCTION

Along with the proliferation of low-cost sensor networks, our capability is extended to observe environments of interests. It brings a wide variety of exciting applications into realization, such as target tracking, intrusion detection, wildlife habitat monitoring, climate control, and disaster management [1]. In this paper, we focus on a potential multicast application, Automobile Tracking System (ATS), which provides automobile location information service. The basic idea of ATS is illustrated in Fig. 1, where the sensors [7] are attached with RFID readers, and the RFID transponders are built in automobiles. The RFID transponders contain the information of automobiles, e.g., the registration/model numbers. The sensors are put along the roads, and distributed in a wide area of the city. One or several sensors are attached to a base station. The sensors can read the contents in the transponders as they pass by, and then send the information to the nearby base station through a wired or wireless network connection. The base station is composed of a computer, connected to the Internet, with a large storage space and computational capacity.

Users of ATS are people who want to find the location of any automobile with an RFID transponder, and they may issue queries from the Internet. The response to their query contains the locations and timestamps of the tracked automobile. To avoid a single point of failure and to balance the system load, the base stations will not send the continuously collected records to a central database; instead, they keep the records locally. Therefore, each query should be multicast to all the base stations. Once a base station receives the query, it searches for the automobile records locally. When corresponding records are found, the base station directly sends them back to the user who issued the query.

In ATS, the number of the base stations can be large, e.g., hundreds or thousands in a city, while all the base stations are relatively stable comparing with the popular peer-to-peer systems. We intend to employ a multicast-based protocol to serve ATS.

To address most problems associated with IP multicast, overlay multicast is employed to provide explicit multicast support at the end system layer, or application layer. In overlay multicast, end hosts self-organized into an overlay structure and accomplish multicast by relaying data to each other via unicast. An end host can carry out sophisticated operations and contribute various resources such as CPU power, storage space, and access bandwidth to support multicast. The advantage of overlay multicast is that it does not need to change the network layer infrastructure. The disadvantages include consuming more bandwidth, sustaining longer latency, and keeping more states at end hosts.

![](images/172653152c7a1c88f2e3f4ecb14fa394056f67f47d869c968a16eb1661ea5444.jpg)



Figure 1. Automobile Tracking System

Overlay multicast shifts the multicast support from the network layer to the application layer, which causes the performance penalty. Communication between end hosts involves traversing other end hosts. The routing path from the source to the destination in overlay multicast may not match the optimal routing path at the IP layer. Therefore, overlay multicast incurs longer end-to-end delay as well as larger traffic than IP multicast. In overlay multicast, the overlay links may share the common physical links at random.

Although many overlay multicast schemes are proposed, how to balance the load in the overlay multicast has not been investigated thoroughly. Only some naive degree bound heuristics were proposed to achieve load balance among group members. The objective of this research is to design an overlay multicast protocol for the ATS, which balances the load among the physical links as well as among the group members.

The rest of this paper is organized as follows. Section 2 discusses related work. Section 3 describes the proposed distributed multiple multicast tree protocol, MMT. Section 4 provides simulation results of the distributed MMT protocol. Section 5 concludes this work.

# II. RELATED WORK

Overlay multicast approaches can be classified as centralized and distributed algorithms. ALMI [10, 12] and HBM [11] are two similar centralized approaches. ALMI employs a centralized control unit called controller. The controller periodically calculates a minimum spanning tree based on the measurement updates received from all the members. The link length used to calculate a minimum spanning tree can be any application specific metric which is computed by members in a distributed way and reported to the controller. Being simple and easy to approach the global optimal solution, ALMI has a single point of failure and poor scalability.

The distributed approaches differ in the way of constructing the overlay topology. The tree-first approaches include YOID [9], TBCP [16], HMTP [2], and NICE [4]. TBCP and HMTP rely on a recursive algorithm to build the tree. A newcomer first contacts the tree root, chooses the best node among the root’s children, and repeats this top-down process until it finds an appropriate parent. The mesh-first approaches, such as Narada [5] and Bayeux [13], first constructs a rich and efficient mesh among members. It then constructs the spanning trees of the mesh and each tree is a source specific using a DVMRPlike [14] routing algorithm. Every member maintains a list of all other members in the group.

Almost all the overlay multicast protocols employ load balancing mechanisms. In ALMI, two routing algorithms [6] build the multicast tree to match the available bandwidth and to balance the load. The routing problem is first modeled as a minimum diameter, degree-limited spanning tree problem (MDDL). For MDDL problem, a compact tree (CT) algorithm is proposed, which is very similar to Prim’s algorithm for MST [3]. The degree constraints are used to achieve load balance among multicast group members. The routing problem can be also modeled as a limited diameter, residual balanced spanning tree problem (LDRB). For LDRB problem, a balanced compact tree (BCT) algorithm is proposed. Both CT and BCT are centralized algorithms. They require large amount of computation and cannot react quickly to the network dynamics. In Narada, to match the available bandwidth and to balance the load, the number of the neighbors in the mesh is constrained, e.g., 3 to 6.

To the best of our knowledge, existing approaches simply pay attention to the load balance among the group members in the overlay layer. However, the load balance among physical links is also critical to the performance of applications, but not considered. Our approach, MMT, focuses on the load balance among the physical links as well as achieving this balance among group members.

# III. MULTIPLE MULTICAST TREES ALGORITHM

In designing our protocol, we have following objectives in mind.

Load balance. To balance the load on the Internet is our main objective. From the network perspective, the constructed overlay must ensure that redundant transmission on physical links is kept minimal and the transmission is distributed evenly on the Internet.   
Overlay efficiency. The tree constructed must be efficient from the application perspective. Our application requires low link stress, even node degree, and low end to end delay.   
Robust. The construction of the overlay tree must be robust to dynamic changes of multicast membership.   
Adaptive to network dynamics. The overlay must adapt to the variations on the Internet.

In this design, a number of multicast trees are built to disseminate the queries to balance the load. As several multicast trees are built simultaneously, we name this approach Multiple Multicast Trees (MMT). Each query is distributed to one of the roots of the multicast trees. The distribution rule is based on the situations of the workload and bandwidth of the roots, and the delay to the roots.

MMT constructs the tree by fragment combination. The roots of the multicast trees are selected randomly from the group members. In case of two end hosts sharing the same gateway router, they should not be selected as roots simultaneously. To make different trees have even chance to select good overlay links, they combine in a round robin manner.

The following is the main process of building one multicast tree. For a multicast tree, each node is a fragment at the beginning. Then each fragment selects one good outgoing link, and combines with another fragment through this link. When two fragments are combined together, the whole number of fragments is decreases by one. When there is only one fragment remaining, the algorithm terminates and the tree is built.

Build\_MMT\_Distributed ( )

{ 1. Randomly select the current tree id;   
2. For current tree, while not all the fragments are connected {   
3. Select $p _ { 1 }$ nodes with the smallest degree in the current fragment;   
4. Randomly select p2 nodes which do not belong to the current fragment;   
5. For each node in $p _ { 2 }$ nodes, select the minimum of all the length from this node to $p _ { 1 }$ nodes as the length from the node to the current fragment;   
6. From $p _ { 2 }$ nodes, select the node nearest to the current fragment, combine current fragment with the fragment containing the node;   
7. Refresh the node degrees, take next tree as the current tree; } }

Figure 2. Distributed algorithm to build MMT

When one fragment selects another fragment and the corresponding links to combine with, it first selects $p _ { 1 }$ nodes with the smallest degree among all the nodes in the current fragment. These $p _ { 1 }$ nodes will be the candidate nodes to extend the fragment. The fragment then selects $p _ { 2 }$ nodes among all the nodes in the other fragments randomly, which become candidate nodes to be combined with. For each node in $p _ { 2 }$ nodes, it takes the minimum of all the lengths from this node to $p _ { 1 }$ nodes as the length to the fragment. The two fragments are combined through this link. The algorithm executed in each multicast group member is described in Fig. 2.

We use an example to illustrate the MMT heuristic. Figure 3 illustrates a small physical topology and each node is a host or router and each link is a physical link. The circle-shaped nodes represent the multicast group members, e.g., nodes 2, 4, 6 and 7. The square-shaped nodes represent the other hosts or routers in the network, e.g., 1, 3 and 5.

Figure 3 (a) illustrates an example of having one multicast tree. The root is node 7 and the tree edges are overlay links (7, 6), (6, 2) and (7, 4). We can observe that the physical links (7, 6), (6, 1), (1, 2) and (7, 4) are used in the multicast tree. That means all the traffic will go though each of these links.

Figure 3 (b) illustrates the case of having two multicast trees. The first tree is rooted at node 7 and the tree edges are overlay links (7, 6), (6, 2) and (7, 4). The second tree is rooted at node 2 and the tree edges are overlay links (2, 7), (2, 4) and (4, 6). We can observe that the physical links (7, 6), (6, 1), (1, 2), (7, 4), (2, 7), (2, 3), (3, 4), (4, 5), (5, 6) are used in the multicast trees. That means all the traffic is shared by these links. Compared with the one multicast tree case, more physical links are used and less traffic would go though each of these links in multiple multicast trees. We can conclude that one multicast tree only use a small part of all the physical links, while multiple multicast trees have a chance to use more physical links to balance the load among all of them.

We propose two heuristics: Non Root Heuristic, which uses estimated hop number as link length, and Root Heuristic, which uses estimated hop number between two hosts and estimated hop number from the joining host to the root as link length.

Figure 4 (a) gives an example in which node 1 is the root, nodes 2, 3, 4 are tree nodes. Nodes 5 and 6 want to join the tree. In Non Root Heuristic, the link lengths are 5 and 4, respectively, as shown in Fig. 4 (b). If we use Root Heuristic and define w1=w2=0.5, where w1 and w2 are the set of nonnegative weights, and added up to 1, the link lengths are 6 and 7, respectively, as shown in Fig. 4 (c).

![](images/eaaf146c1d0ee29662e5771778ccad9d971114a998fb364b9f97e11e7d815784.jpg)



(a) One multicast tree   
![](images/d7b07c362ea882ca4dd9d910e35e1a9f024046adb6a61547fbe0798cccb74206.jpg)



(b) Two Multicast Trees   
Figure 3. Example of Multiple Multicast Tree

![](images/19255354dcf8bd359e108fef1ec22048b4ac3130db60d6514f974377cc66af69.jpg)



(a) Topology

![](images/31e8405e2c7e7b1b86dbd8bd0364429528a67c5bb698b6e416387ee0d6bca106.jpg)



(b) Non-root Heuristic

![](images/e852bcbeae29fc0ba8a7d2ed273253cab36ebe825503d7e2b8b9beb4a47f5957.jpg)



(c) Root Heuristic   
Figure 4. Example of different metrics as link length

The message exchange and decision making process is very similar to distributed MST algorithm [15]. We start by describing how a fragment finds its outgoing edge to combine with another fragment.

First, we consider the trivial special case of a zero level fragment, which is a single node. Initially, each node is in a quiescent state called sleeping. There are three possible node states: the initial state sleeping, the state find while participating in a fragment’s search for the suitable outgoing edge, and the state found at other times.

The sleeping node either spontaneously awakens or is awakened by receiving any message from another node. The fragment first chooses its suitable outgoing edge, marks this edge as a branch of the multicast tree, sends a message called connect over this edge, and goes into the state found, waiting for a response from the fragment at the other end of the selected edge.

The process of selecting the suitable outgoing edge is as follows. Suppose a new fragment at level L has just been formed by the combination of two level (L-1) fragments sharing the selected edge, it becomes the core of the new fragment. The two nodes adjacent to the core start the new cycle by broadcasting an initiate message to other nodes of the fragment. When a node receives an initiate message, it starts to find a suitable outgoing edge. Each node classifies its adjacent edges into one of three possible states: branch, if the edge is an selected overlay edge in the current fragment; reject, if the edge is not a branch but has been discovered to join two nodes of the fragment; and basic, if the edge is neither a branch nor reject.

In order to find a suitable outgoing edge, a node selects the branch edge and sends a test message on it. When a node receives such a test message, it checks whether or not its own fragment identity agrees with that of the test message. If the identities agree, the node sends the rejection message back to the sender of the test message, and both nodes put the edge in the reject state. The node sends the test message to the next best edge. If the node receiving a test message has a different identity from that of the test message, or the fragment level of receiving node is greater than or equal to that of the test message, the message accept is sent back to the sending node, certifying that the edge is an outgoing edge from the fragment of the sending node. If on the other hand the receiving node’s fragment level is less than the level of the test message, the receiving node delays making the response. When no node has outgoing edges, the algorithm is completed, and the fragment is the multicast tree.

Each leaf node of the fragment, which is adjacent to only one fragment branch, sends the message report (W) on its inbound branch, where W is the length of the outgoing edge. Each interior node of the fragment waits until it has both found its own selected edge and received message on all outbound fragment branches. Then the node denotes the edge and reports it to its inbound branch. Eventually, the two nodes adjacent to the core send report messages on the core branch, allowing each of these nodes to determine both the length of the selected outgoing edge and the side of the core on which this edge lies. After the two core nodes have exchanged report messages, the best edges saved by the fragment nodes make it possible to trace the path from the core to the node having the outgoing edge. The message change-core is sent over each branch of this path, and the inbound edge for each of these nodes is changed to correspond to the outgoing edge. When this message reaches the node with the outgoing edge, the inbound edges form a rooted tree, rooted at this node. Finally, the node sends the message connected (L) over the outgoing edge, where L is the level of the fragment. If the two fragments at level L have the same outgoing edge, then each of them sends the message connected (L) over the edge, one in each direction. This will cause the edge to become the core of a level (L+1) fragment and causes new initiate messages with the new level and fragment identity to be sent out.

# IV. PERFORMANCE EVALUATION

We study the performance of the distributed MMT algorithm through simulation experiments. We compare our load balance heuristic with existing load balance heuristics. The network topologies for these experiments are generated using the Transit-Stub graph model of the GT-ITM topology generator [8].

The network topologies are composed of 10,100 nodes with average degree of 4. Among all the nodes, there are 100 transit nodes, and 100 stub networks which have totally 10,000 nodes. The multicast group size is 100. Multicast group members are nodes randomly selected in the stub networks.

We employ three set of simulations. (1) Root Heuristic vs. Non Root Heuristic in Distributed algorithm; (2) Distributed MMT algorithm; (3) Distributed MMT heuristic vs. existing distributed load balance heuristics.

We use different performance criteria in our simulation as follows.

Total physical traffic is the totally used network resource to deliver one packet in the multicast structure. In our simulation, it is represented by the sum of the physical hop numbers per packet.   
Average node stress is the degree in the multicast trees for each multicast group member.   
Node stress deviation is the deviation of node stress of all the multicast group members. The node stress deviation indicates the load balance among group members.   
Average link stress indicates the average load on the physical links.   
Largest delay is the delay from the source to the farthest receiver. In our simulation, it is represented by the hop numbers from the source to the farthest receiver.   
Average delay is the average delay from the source to all the receivers.

![](images/f3d673f87107004865489b2b916b0fe9bc0d5a2d77594f6d776ed7510ddee800.jpg)



![](images/cb42f93bb52a6c929686c718e9c15c394f7189fb86963069dc1354b8c7685a67.jpg)



Figure 5. Largest and average delay

We first compare the distributed algorithms using two different metrics as the link length as described above. We can find in Fig. 5 when we use Root Heuristic, the largest and average delay is much less than that of Non Root Heuristic. Other criteria are slightly degraded in Root Heuristic as the tradeoff. Fig. 6 shows that in Root Heuristic, the physical traffic is a little larger and the physical links number is a little smaller than that of Non Root Heuristic. We employ Root Heuristic in MMT as it can achieve shorter delay than Non Root Heuristic.

In our next simulation, we compare five different approaches. They all build multiple multicast trees except the third approach, which only builds one multicast tree.

Random MST uses multiple random MST, in which shortest link is always selected whatever it has already been selected by other trees or not. This heuristic results in small total physical traffic while the overlay links could be overlapped. Besides, the delay is not considered in this approach.   
Multiple disjoint MST always selects the shortest link which has not been selected by any other trees. This approach can guarantee that all the overlay links are distinct. The total physical traffic is a little larger than the Random MST approach, because longer length links are selected to avoid overlapping. The delay is not considered in this approach.   
Single degree constrained tree, in which the shortest link is always selected when the degree of the nodes is under a specific constraint. This heuristic is used in many multicast protocols to provide the load balance among group members.   
Multiple degree constrained tree scheme uses multiple degree constrained trees.

![](images/d040826913cbd8fd53efa3f8afabd52495fe7bbf115c6518716d9d50cfa16a8e.jpg)



![](images/ec24ddf87748be16a15599f7980059e6f49dc919a13f73bcf17b546fdc70515b.jpg)



Figure 6. Physical traffic and number of physical links used.

MMT. The fifth is our proposed distributed MMT approach.

In Fig. 7, we can observe that they have similar total traffic. Our MMT has a little higher totally used physical link number. The degree constrained single tree approach only builds one tree, so its total physical links number is much lower than other multiple tree approaches. In the node stress deviation, MMT is the lowest among all the approaches. This indicates that our MMT can balance the load among group members much more evenly than all the other approaches.

In Fig. 8, we can see that MMT has larger low link stress part, while it has much smaller high link stress part than other approaches. The largest stress of MMT is only half of the values of other approaches.

In Figures 9 and 10, the average link stress of MMT approach is small among the five approaches. In MMT, the cumulative distribution of physical link stress approaches 100% much earlier than other approaches. This implies that MMT outperforms other approaches in load balance among the physical links.

# V. CONCLUSION

In this paper, we proposed a multiple multicast tree structure to support our data streaming application, ATS. The major design goal of this work is to balance the load on the network. The proposed distributed Multiple Multicast Tree (MMT) protocol is practical for implementation. We evaluate MMT by comprehensive simulations. The results demonstrate that our heuristic significantly outperforms existing approaches in the load balance.

We are currently working on a Peer-to-Peer live streaming project at our lab. In future work, we are going to employ MMT scheme in P2P and IP-TV designs, and further evaluate its performance in real environments.

![](images/24db9ff44cd1505b3dd0446570030a0773475f544e097d9511fab355b12cd57e.jpg)



![](images/2168d1d4554753e11e6549255fecabded7dc84f970f61a97cdef626b01a1017f.jpg)



Figure 7. Physical traffic, physical links number and node stress deviation

![](images/003a97c6009a51ebea83d296f575a9fcfbe77a04bc2c3a6a5864246e0f144497.jpg)



Figure 9. Average physical link stress

![](images/652c7595eb9b5b88c2197720355ed5b6aba0f7335c32e6d37b7b6f22f7f74dae.jpg)



![](images/cd83ee1727199518ee6e5a0bbed2eff766a0fcffff9556f17f5c1ececd075f6d.jpg)



Figure 8. Physical link stress distribution

![](images/8345fe94993d218e30e2ddad051e584da17bd81a61a898312cce42f55223fb47.jpg)



Figure 10. Cumulative distribution of physical link stress

# ACKNOWLEDGMENT

This work was supported in part by the by Microsoft Research Asia, by Hong Kong RGC Grants DAG 04/ 05.EG01, HKUST6264/04E, and China 973 No.2003CB317008.

# REFERENCE

[1] I. F. Akyildiz, W. Su, Y. Sankarasubramaniam, and E. Cayirci, "A survey on sensor networks", IEEE Communications Magazine, 2002   
[2] S. Banerjee, B. Bhattacharjee, and C. Kommareddy, "Scalable application layer multicast", In Proceedings of ACM SIGCOMM, Pittsburgh, Pennsylvania, 2002   
[3] V. Chankong and Y. Y. Haimes, Multiobjective Decision Making: Theory and Methodology, Elseviker-North Holland, New York, 1983   
[4] Y. Chawathe, "Scattercast: an architecture for Internet broadcast distribution as an Infrastructure service." Ph.D Thesis, University of California, Berkeley, 2000   
[5] Y. H. Chu, S. G. Rao, and H. Zhang, "A case for end system multicast", IEEE Journal on Selected Areas in Communications, 2002   
[6] T. H. Cormen, C. E. Leiserson, and R. L. Rivest, Introduction to Algorithms, MIT Press, 1990   
[7] K. Finkenzeller, RFID Handbook: Fundamentals and Applications in Contactless Smart Cards and Identification, Wiley, Chichester, England, 2003

[8] Y. Liu, Z. Zhuang, L. Xiao, and L. M. Ni, "A distributed approach to solving overlay mismatching problem", In Proceedings of IEEE ICDCS 2004, Tokyo, Japan, 2004   
[9] L. Mathy, R. Canonico, and D. Hutchison, "An overlay tree building control protocol", In Proceedings of the Third International COST264 Workshop on Networked Group Communication, London, UK, 2001   
[10] D. Pendarakis, S. Shi, D. Verma, and M. Waldvogel, "An application level multicast infrastructure", In Proceedings of Usenix Symposium on Internet Technologies & Systems (USITS 2001), San Francisco, CA, USA, 2001   
[11] V. Roca and A. El-Sayed, "A host-based multicast (HBM) solution for group communications", In Proceedings of the First International Conference on Networking, 2001   
[12] S. Shi, "Design of overlay networks for internet multicast", Ph.D Thesis, Department of Computer Science, Washington University, 2002   
[13] S. Y. Shi and J. S. Turner, "Routing in overlay multicast networks", In Proceedings of IEEE INFOCOM, New York, NJ, USA, 2002   
[14] D. Waitzman, C. Partrideg, and S. E. Deering, "Distance vector multicast routing protocol. RFC 1075", 1988   
[15] E. W. Zegyra, K. L. Calvert, and S. Bhattacharjee, "How to model an internetwork", In Proceedings of IEEE INFOCOM, San Francisco, CA, USA, 1996   
[16] B. Zhang, S. Jamin, and L. ZhangB, "Host multicast: a framework for delivering multicast to end users", In Proceedings of IEEE INFOCOM, New York, NJ, USA, 2002