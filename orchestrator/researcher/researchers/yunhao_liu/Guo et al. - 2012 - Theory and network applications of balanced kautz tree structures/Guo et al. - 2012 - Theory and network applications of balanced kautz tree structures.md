# Theory and Network Applications of Balanced Kautz Tree Structures

DEKE GUO, National University of Defense Technology

YUNHAO LIU, Tsinghua University

HAI JIN, Huazhong University of Science and Technology

ZhONG LIU and WEIMING ZHANG, National University of Defense Technology

HUI LIU, Xidian University

In order to improve scalability and to reduce the maintenance overhead for structured peer-to-peer (P2P) networks, researchers have proposed architectures based on several interconnection networks with a fixeddegree and a logarithmical diameter. Among existing fixed-degree interconnection networks, the Kautz digraph has many distinctive topological properties compared to others. It, however, requires that the number of peers have the some given values, determined by peer degree and network diameter. In practice, we cannot guarantee how many peers will join a P2P network at a given time, since a P2P network is typically dynamic with peers frequently entering and leaving. To address such an issue, we propose the balanced Kautz tree and Kautz ring structures. We further design a novel structured P2P system, called BAKE, based on the two structures that has the logarithmical diameter and constant degree, even the number of peers is an arbitrary value. By keeping a total ordering of peers and employing a robust locality-preserved resource placement strategy, resources that are similar in a single or multidimensional attributes space are stored on the same peer or neighboring peers. Through analysis and simulation, we show that BAKE achieves the optimal diameter and as good a connectivity as the Kautz digraph does (almost achieves the Moore bound), and supports the exact as well as the range queries efficiently. Indeed, the structures of balanced Kautz tree and Kautz ring we propose can also be applied to other interconnection networks after minimal modifications, for example, the de Bruijn digraph.

Categories and Subject Descriptors: C.2.2 [Computer-Communication Networks]: Network Protocols

General Terms: Design, Algorithms, Performance

Additional Key Words and Phrases: Peer-to-peer networks, distributed hash table, Kautz digraph, Kautz tree

# ACM Reference Format:

Guo, D. K., Liu, Y., Jin, H., Liu, Z., Zhang, W., and Liu. H. 2012. Theory and network applications of balanced kautz tree structures. ACM Trans. Internet Technol. 12, 1, Article 3 (June 2012), 25 pages.

DOI = 10.1145/2220352.2220355 http://doi.acm.org/10.1145/2220352.2220355

The work of D. K. Guo is supported in part by the NSFC under grants 61170284 and 60903206, the China Postdoctoral Science Foundation under grant 201104439, and the Research Foundation of NUDT under grant JC10-05-01. The work of H. Jin is supported in part by the NSFC Major Program under grant 61133006. The work of Y. H. Liu is supported in part by the NSFC Major Program under grant 61190110 and National High-Tech R&D Program of China (863) under grant 2011AA010100. The work of Z. Liu is supported in part by the NSFC under grants 91024006 and 71031007.

Author’s addresses: D. K. Guo, Z. Liu, and W. Z. Zhang, Key Laboratory for Information System Engineering, College of Information System and Management, National University of Defense Technology, Changsha 410073, China; email: guodeke@gmail.com; Y. H. Liu, School of Software, TNLIST, Tsinghua University, Beijing 100084, China; H. Jin, National MOE Key Laboratory for Services Computing Technology and System, School of Computer Science and Technology, Huazhong University of Science and Technology, Wuhan 430074 China; H. Liu, Software Engineering Institute, Xidian University, Xian 710071, China.

Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies show this notice on the first page or initial screen of a display along with the full citation. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, to republish, to post on servers, to redistribute to lists, or to use any component of this work in other works requires prior specific permission and/or a fee. Permissions may be requested from Publications Dept., ACM, Inc., 2 Penn Plaza, Suite 701, New York, NY 10121-0701 USA, fax +1 (212) 869-0481, or permissions@acm.org.

-c 2012 ACM 1533-5399/2012/06-ART3 \$15.00

DOI 10.1145/2220352.2220355 http://doi.acm.org/10.1145/2220352.2220355

# 1. INTRODUCTION

Structured peer-to-peer (P2P) networks impose specific structures on the overlay network and control the placement of data; hence, they exhibit unique properties that unstructured networks lack [Guo et al. 2011; Chandler et al. 2012]. They have already been widely used as good infrastructures for building novel network systems $\left( \mathbf { e . g . } \right.$ , Cassandra [Lakshman and Malik 2010], Pnuts [Cooper et al. 2008], Dynamo [DeCandia et al. 2007], OpenFlow controller [Koponen et al. 2010], and so on).

In general, the topological properties dominate the performance of structured P2P networks, especially the peer out-degree and the network diameter. Traditionally, the peer out-degree and network diameter increase logarithmically with respect to the size n of such a network, such as Chord [Stoica et al. 2003], Pastry [Rowstron and Druschel 2001], Tapestry [Zhao et al. 2002], HyperCup [Schlosser et al. 2002], Kademlia [Maymounkov and Mazieres 2002], SkipNet, and skip list [Harvey et al. 2003]. Those schemes publish and lookup resources within O(log n) hops. They, however, lack scalability, since the number of overlay connections at each peer is bounded by limited resources, and each peer will incur huge overhead to maintain O(log n) overlay connections.

To address such an issue, researchers propose some structured P2P networks based on several fixed-degree interconnection networks. In such interconnection networks, the network diameter grows logarithmically along with the network size, whereas the peer degree remains fixed regardless of the network size. Such networks include butterfly [Malkhi et al. 2002], cube-connected cycle (CCC) [Banerjee and Sarkar 2001], d-dimensional torus [Xu 2001], de Bruijn network [Sivarajan and Ramaswami 1994], Kautz [Tvrdik 1994; Imase and Itoh 1981], and many variants. Among existing structured P2P networks based on fixed-degree interconnection networks, Viceroy [Malkhi et al. 2002] and Ulysses [Xu et al. 2004] emulate the butterfly network, Cycloid [Shen et al. 2004] emulates the CCC network, CAN [Ratnasamy et al. 2001a] emulates the d-dimensional torus network. Koorde [Kaashoek and Karger 2003], Distance Halving [Naor and Wieder 2003], D2B [Fraigniaud and Gauron 2006, 2003], ODRI [Loguinov et al. 2005], and Broose [Gai and Viennot 2004] emulate the de Bruijn network, and FissionE [Li et al. 2005] emulates the Kautz network.

In this article, we aim to design a structured P2P network with the smallest network diameter k given a constant out-degree d, while the network order n is an arbitrary value. The Kautz digraph is the best choice among all of existing nontrivial digraphs, since it almost achieves the Moore bound [Miller and Siran 2005], and has the optimal diameter. The Kautz digraph, however, has an inherent restriction on the number of vertices it can support. That is, the order must be $d ^ { k - 1 } ( d + 1 )$ for any diameter k under a given degree d, but cannot be a general integer. The order of any P2P network, however, can be any uncertain integer. Therefore, the static Kautz digraph cannot simply be used to design a structured P2P network.

We design a balanced Kautz tree and associated Kautz ring structures [Guo et al. 2008]. We then propose, BAKE, a robust and efficient P2P network based on all leaf nodes of a balanced Kautz tree with $\begin{array} { r } { k _ { l } = \lceil \log _ { d } \frac { n } { d + 1 } + 1 \rceil } \end{array}$ network diameter and $d + 2$ peer out-degree in a dynamic environment. The average routing distance is shorter than that of the CAN, butterfly, de Bruijn digraph, and $\log _ { d } n ,$ and is close to that of the complete Kautz digraph. The delay and message cost of joining a new peer are, at most, $2 \bar { k _ { l } } + d + 1$ and $2 \breve { k } _ { l } + 2 \breve { d } + 2$ , respectively. The delay and message cost of handling a leaving peer are, at most, $( d - \mathbf { 1 } ) \times \mathbf { \bar { \mu } } _ { k _ { l } + d }$ and $d \times ( k _ { l } + 1 )$ , respectively. The delay and message cost of handling a failed peer are, at most, $3 k _ { l } + d - 1$ and $3 k _ { l } + d + 1$ , respectively. The delay and message cost to publish or lookup a resource are, at most, kl.

The main contributions of this paper are summarized as follows:

(1) We propose the balanced Kautz tree and Kautz ring structures that emulate the Kautz digraph and ensure the robustness and correctness of structured peer-to-peer networks in dynamic environments. Moreover, the basic idea of the two structures would be applied to other interconnection networks after minimal modifications.   
(2) Based on the balanced Kautz tree and Kautz ring, we design BAKE, an effective and robust P2P network which retains desirable properties of the Kautz digraph, such as the optimal diameter and constant out-degree. We further design a localitypreserving resource placement strategy, an effective and robust routing scheme, and the exact and range query schemes. We also introduce several essential algorithms to deal with the dynamic behaviors of peers.   
(3) We evaluate the topology properties of BAKE, the robustness of the routing scheme, and the delay and message cost of some basic operations through formal analysis and comprehensive simulations. We further compare BAKE with previous P2P designs based on different fixed-degree interconnection networks.

The rest of this article is organized as follows. Section 2 summarizes the definition and emulation methods of the Kautz digraph. Section 3 presents the balanced Kautz tree and associated Kautz ring structures. Section 4 discusses the design of BAKE based on the balanced Kautz tree. Section 5 presents the dynamic operations of peers to maintain the topology. We evaluate BAKE in Section 6, and conclude the work in Section 7.

# 2. RELATED WORK

# 2.1. Kautz Digraph

The degree/diameter problem, which determines the largest graphs or digraphs with a given maximum peer degree and network diameter, is one fundamental challenge in graph theory. Many research activities have proved that the order n of a digraph with the maximum out-degree d and network diameter k is not larger than a general Moore bound [Miller and Siran 2005; Guo et al. 2011], as defined by Formula (1). Additionally, nonexistence of digraphs can achieve the Moore bound when $d \ge 3$ and $k \geq 3$ . The best lower bound is $n \geq d ^ { k } + d ^ { k - 1 }$ , which is only obtained by the Kautz digraph among all of existing nontrivial digraphs.

$$
n \leq d ^ {k} + d ^ {k - 1} + \dots + d ^ {2} + d + 1 = (d ^ {k + 1} - 1) / (d - 1). \tag {1}
$$

Definition 1. A digraph with a fixed vertex out-degree d and a network diameter k is a Kautz digraph, denoted as $K ( d , k ) ,$ , only if it holds the following two conditions [Imase and Itoh 1983; Panchapakesan and Sengupta 1999; Guo et al. 2007].

(1) Exists $d ^ { k } { + } d ^ { k - 1 }$ nodes labeled with string $x _ { 1 } x _ { 2 } \ldots x _ { k }$ over $\{ 0 , 1 , \ldots , d \}$ , where $x _ { i } \neq x _ { i + 1 }$ for $0 \leq i \leq d - 1$ .   
(2) Exists an arc from any node $x _ { 1 } x _ { 2 } \ldots x _ { k }$ to another node $x _ { 2 } , \ldots . x _ { k } \alpha$ for each $\alpha \in$ $\{ 0 , 1 , \ldots , d \} - \{ x _ { k } \}$ . The arc is labeled as $( x _ { 1 } x _ { 2 } \dots x _ { k } , x _ { 2 } , \dots x _ { k } \alpha ) \mathrm { o r } x _ { 1 } x _ { 2 } , \dots x _ { k } \alpha .$

Based on Formula (1), the smallest diameter for a digraph with the order n and the maximum out-degree d can be derived as Formula (2). Nonexistence of digraphs can achieve such a lower bound for $d \ge 3$ and $k \geq 3$ [Damerell 1973]. The best upper bound is $\textstyle \lceil \log _ { d } { \frac { n } { d + 1 } } + 1 \rceil$ , which is only obtained by the Kautz digraph among all existing nontrivial digraphs.

$$
k \geq \lceil \log_ {d} (n (d - 1) + 1) \rceil - 1. \tag {2}
$$

Thus the Kautz digraph has the optimal diameter among all of nontrivial digraphs, including the de Bruijn digraph, in the same setting. Additionally, the Kautz digraph $K ( d , k )$ has a higher connectivity compared to the de Bruijn digraph. More precisely, the Kautz digraph of degree d has connectivity $d ,$ since there exist d node-disjoint paths between any node pair. On the contrary, the connectivity of the corresponding de Brujin graph is $d { - } 1$ . Moreover, the Kautz digraph possesses the lower latency and load balance compared to the de Bruijn digraph [Panchapakesan and Sengupta 1999].

Bearing these points in mind, this article enhances the Kautz digraph by designing the balanced Kautz tree and the Kautz ring structures and proposes a novel P2P network based on the two structures. The basic idea of the two structures introduced in this article would apply to other interconnection networks after minimal modifications—for example, the de Bruijn digraph.

# 2.2. Emulation of the Kautz Digraph

The first related work is FISSIONE [Li et al. 2005], which uses a similar approach to the CAN [Ratnasamy et al. 2001b], to emulate the Kautz digraph K(2, k). Each peer holds a zone in a 2-dimensional Cartesian coordinate space. All zones are organized into an approximate K(2, k), based on their identifiers. FISSIONE suffers from a long routing path, high lookup delay, and weak connectivity, since the degree of each peer is too small. Moreover, FISSIONE cannot support a general Kautz digraph with an arbitrary node degree, except for node degree 2, and whether the emulation method of FISSIONE is suitable for $\bar { K ( d , k ) }$ is still under investigation when $d > 2$ .

In our previous work [Guo et al. 2011], a quasi-Kautz digraph was proposed as the topology of a structured P2P network, called MOORE. The quasi-Kautz digraph retains all advantages of the Kautz digraph K(d, k) where d $\geq 2 .$ , and tackles the limit of the Kautz digraph: the order can only be some given value determined by the node degree and network diameter, such as $\bar { d ^ { + } } 1 , d ( d + \bar { 1 } ) , d ^ { 2 } ( d + 1 ) , \ldots , d ^ { k } ( d + 1 )$ . MOORE attains the best upper bound on the network diameter as mentioned in Formula (2), even the order is an arbitrary value. As mentioned in Guo et al. [2011], the correctness of MOORE relies on the fact that the node joining and departing operations can preserve the desirable structure of a backbone subnetwork. However, such an invariant can be compromised if nodes fail in dynamic environments. An incorrect backbone subnetwork will lead to an incorrect emulation of a general Kautz digraph. Consequently, MOORE may not correctly distribute and retrieve data in the desired manner. In this article, the introduction of the balanced Kautz tree and Kautz ring structures well address such a problem under dynamic environments. The resulting structured peer-to-peer network, called BAKE, has a more robust and flexible topology and routing scheme compared to MOORE.

Definition 2. Let GK(d, n) denote a generalized Kautz digraph with the node degree d and order n. The vertex set and arc set of GK(d, n) are $\mathbf { \bar { \psi } } ( G K ( d , n ) ) = \{ 0 , \dots , n - 1 \}$ and $E ( G K ( d , n ) ) = \{ \langle i , ( - d \times i - \alpha )$ mod n $| 1 \leq \alpha \leq d \}$ , respectively [Xu 2001; Imase and Itoh 1983].

Although the generalized Kautz digraph, as shown in Definition 2, can extend the Kautz digraph for a general number of vertices, it has to reconstruct the entire topology, once the number of vertices changes. Consequently, each vertex has to find its new neighbors and update its links so as to construct a new generalized Kautz digraph. Due to the frequent changes of peers in a P2P network, the generalized Kautz digraph is not practical for structured P2P networks due to the expensive overhead to maintain its topology.

# 3. BALANCED KAUTZ TREE AND KAUTZ RING STRUCTURES

Recall that the kuatz digraph is the optimal topology among all of nontrivial digraphs only if all nodes exist and are stable; hence, it cannot simply be used in dynamic scenarios, for example P2P networks. To address such an issue, we propose the balanced Kautz tree and Kautz ring structures that will help to construct an appropriate Kautz digraph, as shown in Section 4. The two structures can ensure the robustness and correctness of peer-to-peer networks that emulate the Kautz digraph in dynamic scenarios. Moreover, the Kautz ring keeps an order of nodes to support the locality-preserving resource placement in Section 4.

# 3.1. The Definition of Balanced Kautz Tree

Definition 3. A d-ary Kautz tree with depth of k is a rooted tree. The root node has $d + 1$ child nodes, and each inner node has, at most, d children. Each edge at the same level is assigned a unique label. Each node except the root node is allocated a unique label. The label of a node is the concatenation of the labels along the edges on its root path. The label of each edge is assigned based on the following rules.

(1) The edge from the root node to its $i ^ { t h }$ child is labeled as $x _ { 1 } ^ { i } = i - 1$ for $1 \leq i \leq d + 1$ . The $i ^ { t h }$ child of the root node is labeled as $x _ { 1 } ^ { i }$ , and is arranged from left to right.

(2) The edge from a node $x _ { 1 }$ to its $i ^ { t h }$ child is labeled as $x _ { 2 } ^ { i } = ( x _ { 1 } - i )$ mod $( d + 1 )$ for $1 \leq i \leq d$ . The $i ^ { t h }$ child is labeled as $x _ { 2 } ^ { i } x _ { 1 }$ , and is arranged from left to right.

(3) The edge from a node $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ to its first child is labeled as $x _ { k } ^ { 1 }$ where $x _ { k } ^ { 1 } = x _ { 1 }$ if $x _ { 1 } \neq x _ { k - 1 }$ , otherwise $x _ { k } ^ { 1 } = ( x _ { 1 } - 1 )$ ) mod $( d + 1 )$ . The first child is labeled $x _ { k } ^ { 1 } x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ , and is arranged at the leftmost position.

(4) We arrange the values $0 , 1 , \ldots , d$ along a ring in ascending order. If a path from a point $x _ { k } ^ { 1 }$ to a point $x _ { k } ^ { i } = ( x _ { k } ^ { 1 } - i + 1 )$ mod $( d + \bar { 1 } )$ along the anti-clockwise direction does not meet $x _ { k - 1 }$ , the edge from $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ to its $i ^ { t h }$ child is labeled as $x _ { k } ^ { i } =$ $( x _ { k } ^ { 1 } - i + 1 )$ mod $( d + 1 )$ , otherwise it is labeled as $x _ { k } ^ { i } = ( x _ { k } ^ { 1 } - i )$ mod $( d + 1 )$ . The $i ^ { t h }$ child of node $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ is labeled as $x _ { k } ^ { i } x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ for $2 \leq i \leq d ,$ and is arranged from left to right.

Note that the identifier $x _ { k } x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ of each node in a Kautz tree satisfies that $x _ { i + 1 } \neq x _ { i }$ for $1 \leq i \leq k - 1$ . We associate each node in the tree with a unique level. The level of the root node is 0, and its immediate child nodes locate at level 1, and so on. In general, the length of the label of each node represents its level in the tree. Definition 3 provides the mechanism for assigning labels to edges and nodes, however, it does not specify which child nodes of each inner node should appear in the tree. As a result, there may exist many different shapes of a Kautz tree with a given number of nodes, according to Definition 3. In this article we focus on the balanced Kautz tree.

Definition 4. A d-ary Kautz tree with the depth of k is balanced if all leaf nodes are at the level k. A balanced Kuatz tree is a complete Kautz tree KT ree(d, k) only if the parent node of any leaf node has full child nodes, otherwise it is an incomplete Kautz tree I KT ree(d, k, n) with n leaf nodes.

In a d-ary balanced Kautz tree with the depth of k, the root node has d + 1 children; each inner node at level $k - 1$ has at least one child and at most d child nodes; each inner node at the other level has d child nodes; the number of inner nodes at level i is $d ^ { i } + d ^ { i - 1 }$ for $1 \leq i \leq k - 1$ . The number of leaf nodes in an incomplete Kautz tree is at least $d ^ { k - 1 } + d ^ { k - 2 }$ which equals that of a complete Kautz tree $K T \bar { r } e e ( d , k { - } 1 )$ and is at most $d ^ { k } + d ^ { k - 1 }$ if it becomes a complete Kautz tree KT ree(d, k). Figure 1(a), (b), and (c) plot a unbalanced Kautz tree, an incomplete Kautz tree, and a complete Kautz tree, respectively. The white leaf nodes 201, 021, 012, and 102 are the nodes do not appear in Figure 1(b). Once those peers appear, the incomplete Kautz tree becomes a complete one.

![](images/17603f6e467f63e8b4b7fc98f5b0be9566b1caeafa7cf0244f08ec8d388dbea7.jpg)



(a) Unbalanced d-ary Kautz tree

![](images/1f995ea10d07c1f9144dbfdaf83f489cdddd45b3a2d4ce20897c0f9c4be6d25f.jpg)



(b) Incomplete Kautz tree IKTree (2,3,8).

![](images/f11cb5bf57956c0486af1a1ad10be262a2731d7c7298db6e0cdb4bf823d68c29.jpg)



(c) Complete Kautz tree;KTree(2,3)   
Fig. 1. Kautz tree and Kautz rings.

Although the recursive method mentioned in Definition 3 does indeed assign a unique label for each child node of any node $x ,$ , we further propose a fundamental operation $\sigma _ { 1 } ( x )$ to implement the same function in a more efficient and practical manner.

Definition 5. Given any node $x = x _ { k } \ldots x _ { 2 } x _ { 1 } , \sigma _ { 1 } ^ { i } ( x )$ can produce a unique label $\sigma _ { 1 } ^ { i } ( x ) =$ $x _ { k + 1 } ^ { i } x _ { k } \ldots x _ { 2 } x _ { 1 }$ for its $i ^ { t h }$ child node, where $1 \leq i \leq d .$ If one of the following conditions holds, then $x _ { k + 1 } ^ { i } = ( x _ { 1 } - i + 1 )$ mod(d + 1), otherwise $x _ { k + 1 } ^ { i } = ( x _ { 1 } - i ) { \bmod { ( } } d + 1 )$ .

(1) $x _ { k } < x _ { 1 } - i + 1 \leq x _ { 1 }$   
(2) $x _ { 1 } < x _ { k }$ and $x _ { k } - d - 1 < x _ { 1 } - i + 1$

$$
\sigma_ {m} ^ {1} (x) = \sigma_ {1} ^ {1} (\sigma_ {m - 1} ^ {1} (x)) \tag {3}
$$

$$
\sigma_ {m} ^ {d} (x) = \sigma_ {1} ^ {d} (\sigma_ {m - 1} ^ {d} (x)) \tag {4}
$$

The operations $\sigma _ { m } ^ { 1 } ( x )$ and $\sigma _ { m } ^ { d } ( x )$ denote the leftmost and the rightmost nodes when traversing down m steps from the node x, respectively. The operation $\sigma _ { 0 } ^ { i } ( x )$ denotes the peer x itself for any i, for example, $\sigma _ { 0 } ^ { 1 } ( x )$ and $\sigma _ { 0 } ^ { d } ( x )$ in Algorithm 2 are equal to x itself. The traversal process always selects the first child in each step to arrive at the leftmost node, and chooses the last child in each step to reach the rightmost node. For example, $\sigma _ { 2 } ^ { 1 } ( 0 ) , \sigma _ { 2 } ^ { 1 } ( 1 ) , \sigma _ { 2 } ^ { 1 } ( 2 )$ denote nodes 020, 101, 212 in Figure 1(c), and $\sigma _ { 2 } ^ { 2 } ( 0 ) , \sigma _ { 2 } ^ { 2 } ( 1 ) , \sigma _ { 2 } ^ { \hat { 2 } } ( 2 )$ denote nodes 210, 021, 102 in Figure 1(c).

The operation $\sigma _ { 1 } ( x )$ is able to allocate a unique label for each child of node x, as well as rank all the child nodes in ascending order. Although such an operation solves the first obstacle to construct and uses a Kuatz tree, it still cannot locate the position of a node $\sigma _ { 1 } ( x )$ among all child nodes that have the same parent node. The position information of a node $\sigma _ { 1 } ( x )$ is crucial to finding its right and left adjacent nodes at the same level, and to calculate the distances from it to other nodes if there is a total ordering of nodes at the same level. We design Algorithm 1 to address such an issue, as in the following.

# 3.2. The Kautz Ordering of Nodes in a Complete Kautz Tree

There are $d ^ { k } + d ^ { k - 1 }$ nodes, each with a label xkxk−1 . . . x2x1 over $\{ 0 , 1 , \ldots , d \}$ at any level k in a balanced Kautz tree, where $x _ { i + 1 } \neq x _ { i }$ for $1 \leq i < k$ . If there is a linear total ordering of nodes at the same level, these nodes can form a ring and keep their localities. For any level, the left-to-right traversal of nodes at the level can form a total ordering, denoted as the Kautz ordering. We first rank the child nodes of the root node in ascending order, then we rank all the child nodes of each node at level 1, respectively. Note that the nodes at level 2 inherit the order of nodes at level 1. The Kautz ordering of nodes at level 1 is 0, 1, and 2, as shown in Figure 1(c). The Kautz ordering of nodes 20 and 10 must be less than that of nodes 01 and 21. By ranking nodes from levels 1 to k recursively, we can derive a Kautz ordering of nodes at each level. In the remainder of this article, we refer to the Kautz ordering of nodes as a Kautz ring. A Kautz ring of nodes at level i stars from the node $\sigma _ { i } ^ { 1 } ( r o o \bar { t } )$ for $1 \leq i \leq k$ .

ALGORITHM 1: position(x)   
Require: $x = x_{k}x_{k-1} \ldots x_{2}x_{1}$ is a label of a node in a balanced Kautz tree, and the length of it is larger than 1.
1: number $\leftarrow 0$ 2: if $x_{1} = x_{k_{1}}$ then
3: number $\leftarrow (x_{1} - x_{k}) \mod (d + 1)$ 4: else
5: if $x_{1} < x_{k-1}$ then
6: if $x_{1} < x_{k} < x_{k-1}$ then
7: number $\leftarrow x_{1} - x_{k} + d + 1$ 8: else
9: number $\leftarrow (x_{1} - x_{k} + 1) \mod (d + 1)$ 10: else
11: if $x_{k-1} < x_{k} \leq x_{1}$ then
12: number $\leftarrow x_{1} - x_{k} + 1$ 13: else
14: number $\leftarrow (x_{1} - x_{k}) \mod (d + 1)$ 15: Return number

A precondition of the above method is that each node should have global knowledge of the entire tree structure. Such a requirement, however, is difficult to satisfy for distributed applications. To address such an issue, we want to derive a Kautz ring for nodes at the same level by establishing a predecessor and a successor for each node based only on its label.

Definition 6. For any node x, its predecessor is the last existing node anti-clockwise from it in a Kautz ring of all existing nodes at the same level, and its successor is the first existing node clockwise from it in the same Kautz ring. The concept of the left adjacent node is similar to the predecessor, but the Kautz ring consists of all possible nodes, not just existing nodes, as do the right adjacent node and the successor node.

For example, the predecessor and successor of node 212 are nodes 121 and 202 in a Kautz ring consisting of all solid leaf nodes in Figure 1(b), while the left and right adjacent nodes of node 212 are nodes 021 and 012 in a Kautz ring consisting of solid and white leaf nodes.

Via the steps, as in the following, the method can achieve the same result compared to traversing all nodes in the same level from left to right. For the leftmost child node x of the root node, we look for its successor node y, then find the successor node of node y, and so on, and finally get a Kautz ring of nodes at level 1 when meet node x again. The Kautz ring for nodes at other levels can be achieved similarly. In the context of a complete Kautz tree, the predecessor and the left adjacent of each node are the same node, and the successor and right adjacent of each node are also the same node. It is clear that to discover the predecessor and successor nodes for any node, we have to first identify its right adjacent and left adjacent nodes based on its label. We design Algorithm 2 to address this issue.

ALGORITHM 2: Adjacent(xk . . . x2x1)   
Radjacent( $x_{k}\ldots x_{2}x_{1}$ )

1: for i = k - 1 down 1 do
2: $y = x_{i} \ldots x_{2}x_{1}, z = x_{i+1}x_{i} \ldots x_{2}x_{1}, j \leftarrow position(z)$ 3:    if j < d then
4: $Return \sigma_{k-i-1}^{1}\left(\sigma_{1}^{j+1}(y)\right)$ 5: right $\leftarrow (x_{1} + 1) \mod (d + 1)$ 6: Return $\sigma_{k-1}^{1}(right)$ Ladjacent( $x_{k}\ldots x_{2}x_{1}$ )
1: for i = k - 1 down 1 do
2: $y = x_{i} \ldots x_{2}x_{1}, z = x_{i+1}x_{i} \ldots x_{2}x_{1}, j \leftarrow position(z)$ 3:    if 1 < j then
4: $Return \sigma_{k-i-1}^{d}\left(\sigma_{1}^{j-1}(y)\right)$ 5: left $\leftarrow (x_{1} - 1) \mod (d + 1)$ 6: Return $\sigma_{k-1}^{d}(left)$

If a node $x = x _ { k } x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ at level k is not the last child of its parent node, the right adjacent node of the node x can be found after one loop in Algorithm 2. Otherwise, the problem becomes finding the right adjacent node $y _ { k - 1 } \ldots y _ { 2 } y _ { 1 }$ of node $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ at the level $k - 1$ , and then finding the leftmost node when traversing down one step from node $y _ { k - 1 } \ldots y _ { 2 } y _ { 1 }$ . If node $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ is not the last child of its parent node $x _ { k - 2 } \ldots x _ { 2 } x _ { 1 } ,$ Algorithm 2 will find the right adjacent node for it after one loop, and responds to the right adjacent node for node x after two loops. Otherwise, the problem becomes finding the right adjacent node $y _ { k - 2 } \ldots y _ { 2 } y _ { 1 }$ of a node $x _ { k - 2 } \ldots x _ { 2 } x _ { 1 }$ at level $k - 2 ,$ and then finding the leftmost node when traversing down two steps from the node $y _ { k - 2 } \ldots y _ { 2 } y _ { 1 }$ , and so on. If the node x represents the rightmost one among the paths from any node at level k to the root node through node $x _ { 1 } ,$ , Algorithm 2 assigns the right adjacent node for it with another node, which represents the leftmost node among the paths from any node at level k to the root node through node $( x _ { 1 } + 1 )$ mod $( d + 1 )$ . For example, 102 is such a node in Figure 1(c), and its right adjacent node is the node 020 that represents the leftmost one among the paths from all nodes at the level $k = 3$ to the root node. In such a case, the right adjacent node for node x can be found after $k - 1$ loops.

The left adjacent node of node x can be achieved after $k - 1$ loops of the Ladjacent method in Algorithm 2 if the node x is not the first child of its parent node. The Ladjacent method deals with other cases in a similar way as the Radjacent method does. If the node x represents the leftmost one among the paths from any node at level k to the root node, for example, the node 020 in Figure 1(c), its left adjacent node, is the node 102, which represents the rightmost one among the paths from any node at level k to the root node. In such case, the left adjacent node of the node x can be found after $k - 1$ loops.

After obtaining the Kautz ring of all nodes at any level, we need to measure the distance between any two nodes at that level based on their labels. The clockwise distance is calculated by Algorithm 3. The anti-clockwise distance equals $d ^ { k } + d ^ { k - 1 }$ minus the clockwise distance. The objective of these two algorithms is to estimate the lengths of two paths between two nodes in the clockwise and anti-clockwise orders, respectively.

For a complete Kautz tree with height of $k + 1$ , the subtree with any node at level i as the root has number $d ^ { k - i }$ leaf nodes. For example, the subtree with any node at the level 1 as the root has $d ^ { k - 1 }$ leaf nodes. The clockwise distance between any two nodes $x = x _ { k } \ldots x _ { 2 } x _ { 1 }$ and $y = y _ { k } \ldots y _ { 2 } y _ { 1 }$ can be calculated by a recursive manner, as shown in Algorithm 3. Let m denote the length of the longest common suffix of the two nodes. At level $m + 1 ,$ , we first obtain the positions of nodes $x _ { m + 1 } \ldots x _ { 2 } x _ { 1 }$ and $y _ { m + 1 } \ldots y _ { 2 } y _ { 1 }$ among all child nodes of the node $x _ { m } \ldots x _ { 2 } x _ { 1 }$ via Algorithm 1, and then calculate the number of leaf nodes in the subtrees rooted at nodes that locate between the nodes $x _ { m + 1 } \ldots x _ { 2 } x _ { 1 }$ and $y _ { m + 1 } \ldots y _ { 2 } y _ { 1 }$ . We also consider the same issue at the other level j where $m + 2 \leq j \leq k - 1 .$ , respectively. After all nodes located between nodes x and y at the same level are selected by the above process, we know the clockwise and anti-clockwise distances between the two nodes.

ALGORITHM 3: ClockwiseDistance(x, y)   
Require: $x = x_{k} \ldots x_{2}x_{1}$ and $y = y_{k} \ldots y_{2}y_{1}$ are labels of two nodes in a complete Kautz tree.
1: distance $\leftarrow 0$ 2: $u \leftarrow null, v \leftarrow null$ 3: Let m denotes the length of common suffix of x and y.
4: if m = 0 then
5: distance $\leftarrow |x_{1} - y_{1} - 1| \times d^{k-1}$ 6: else
7: if position( $x_{m+1} \ldots x_{1}$ ) < position( $y_{m+1} \ldots y_{1}$ )) then
8: $u \leftarrow x, v \leftarrow y$ 9: else
10: $u \leftarrow y, v \leftarrow x$ 11: $l \leftarrow \min\{position(x_{m+1} \ldots x_{1}), position(y_{m+1} \ldots y_{1})\}$ 12: $r \leftarrow \max\{position(x_{m+1} \ldots x_{1}), position(y_{m+1} \ldots y_{1})\}$ 13: distance $\leftarrow (r - l - 1) \times d^{k-m-1}$ 14: for $i = m + 1$ to k - 1 do
15: distance + $\leftarrow (d - position(u_{i+1} \ldots u_{2}u_{1})) \times d^{k-i}$ 16: distance + $\leftarrow (position(v_{i+1} \ldots v_{2}v_{1}) - 1) \times d^{k-i}$ 17: if u = x then
18: Return distance + 1 {The x is less than y in the order}
19: else
20: Return $(d + 1) \times d^{k-1} - distance - 1$

# 3.3. The Kautz Ordering of Nodes in an Incomplete Kautz Tree

As shown in Figure 1, the predecessor and successor nodes are sometimes not the corresponding left and right adjacent nodes for any leaf node in a IKT ree(d, k, n). The methods above that we proposed can construct a Kuatz ring for all inner nodes at a given level in a I KT ree(d, k, n), but fail to form a Kautz ring of all existing leaf nodes. On the other hand, a complete Kautz tree has a unique shape, but an incomplete one may have many different shapes. Consequently, a leaf node usually cannot deduce its predecessor and successor nodes in a IKT ree(d, k, n) as it does in a KT ree(d, k). In such a setting, if there exists a leaf node that has the global knowledge about the entire tree structure, it can derive the predecessor and successor nodes for other leaf nodes. Otherwise, each leaf node should cooperate with other leaf nodes to discover its predecessor and successor nodes in a distributed manner, as shown in Section 4. For the same reasons, Algorithm 3 cannot always correctly measure the distance between any two leaf nodes in a IKT ree(d, k, n) based only on their labels.

In Section 4, the topology construction rule imposes a constraint on the shape of an incomplete Kautz tree $I K { \bar { T } } r e e ( d , k , n )$ . It allocates the first a child nodes of each inner node at the level $k - 1$ , and then the $( a + 1 ) ^ { t h }$ child node of $n - \alpha \times ( d ^ { k - 1 } + d ^ { k - 2 } )$ inner nodes at the level k− 1 in the Kautz or random order, where $a = \lfloor n / ( d ^ { k - 1 } + d ^ { k - 2 } ) \rfloor$ . For a pair of leaf nodes with the same parent node, the distance between them calculated by Algorithm 3 is equivalent or very close to the real value. For other pairs of leaf nodes, the result from Algorithm 3 is usually larger than the real value. For example, the clockwise distance from node 210 to node 202 is 4 hops in Figure 1(b), but Algorithm 3 responds in 7 hops.

ALGORITHM 4: ApproximateDistance(x, y, a)   
Require: $x = x_{k} \ldots x_{2}x_{1}$ and $y = y_{k} \ldots y_{2}y_{1}$ are labels of two nodes in a balanced Kautz tree.
1: $u \leftarrow x_{k-1} \ldots x_{2}x_{1}$ 2: $v \leftarrow y_{k-1} \ldots y_{2}y_{1}$ 3: if u = v then
4: Return ClockwiseDistance(x, y)
5: distance $\leftarrow$ ClockwiseDistance( $x, \sigma_{1}^{a+1}(u)$ )
6: distance + $\leftarrow$ ClockwiseDistance( $\sigma_{1}^{1}(v), y$ )
7: distance + $\leftarrow (a + 1) \times (\text{ClockwiseDistance}(u, v) - 1)$ 8: Return distance

In order to measure the distance between any pair of leaf nodes as accurately as possible, we designed Algorithm 4 based on Algorithm 3 to support an incomplete as well as a complete Kautz tree. The result will be used to optimize the routing strategy to forward a message along a path that is as short as possible. For a static or moderately dynamic incomplete Kautz tree, the result is close to even equal to the real value.

# 4. BAKE: A BALANCED KAUTZ TREE-BASED OVERLAY NETWORK

We propose three structuring strategies to organize peers into an efficient overlay network that can guarantee the logarithmic network diameter and constant out-degree for each peer. All the structuring strategies are based on the concept of a balanced dary Kautz tree. First, each peer maps to one leaf node in the balanced Kautz tree, and uses the label of the corresponding leaf node and IP address as its logical and physical identifiers, respectively. Second, each peer maintains d+2 neighboring peers according to a topology rule. Third, any resource gets an identifier from an identifier space that contains the identifier space of the peers. Resources are distributed at given peers based on the longest suffix-matching rule. Based on the three strategies above, we further propose a robust routing scheme to support the resource distribution, resource query, and topology.

# 4.1. Topology Construction Rule

As mentioned in Section 3, a balanced Kautz tree is usually an incomplete Kautz tree, and is a complete one only in some specific cases. For a complete Kautz tree KT ree(d, k), $d ^ { k } + d ^ { k - 1 }$ , peers form a desirable topology by the following rule. For any peer $x = x _ { k } . . . x _ { 2 } x _ { 1 }$ , its successor and predecessor are Radjacent(x) and Ladjacent(x), and its $i ^ { t h }$ out-neighbor and in-neighbor are $\varsigma _ { 1 } ^ { i } ( x )$ and $\tau _ { 1 } ^ { i } ( x )$ for $1 \leq i \leq d ,$ respectively. The peer x maintains total d + 2 links to its predecessor, successor, and number of d out-neighbors. On the other hand, its predecessor, successor, and d in-neighbors also maintain a total number of $d + 2$ links to the peer x. The network diameter of such an overlay network is k. The $\varsigma _ { 1 } ^ { i } ( x )$ and $\sigma _ { 1 } ^ { i } ( x )$ are defined as follows.

Definition 7. $\varsigma _ { 1 } ^ { i } ( x )$ denotes an operation such that $\varsigma _ { 1 } ^ { i } ( x ) = x _ { k - 1 } \dots x _ { 1 } x _ { 0 } ^ { i }$ for $1 \leq i \leq d .$ If one of the following conditions is satisfied, then $x _ { 0 } ^ { i } = ( x _ { k } + i - 1 )$ mod (d+1). Otherwise, $x _ { 0 } ^ { i } = ( x _ { k } + i )$ mod $( d + 1 )$ .

(1) $x _ { k } < x _ { k } + i - 1 \leq x _ { 1 } ;$   
(2) $x _ { k } + i - 1 < x _ { 1 } + d + 1$ and $x _ { 1 } < x _ { k }$

Definition 8. Given $\sigma _ { 1 } ^ { i } ( x ) = x _ { k + 1 } ^ { i } \cdot \cdot \cdot x _ { 2 } x _ { 1 } , \tau _ { 1 } ^ { i } ( x )$ denotes an operation such that $\tau _ { 1 } ^ { i } ( x ) =$ $x _ { k + 1 } ^ { i } \ldots x _ { 3 } x _ { 2 }$ for $1 \leq i \leq d$ .

P2P overlays must support an arbitrary number of peers in order to deal with the uncontrolled dynamic operations of peers, such as joining, departing, and failure. Unfortunately, an overlay network based on a d-ary complete Kautz tree holds the desirable topology if the number of peers n equals a series of discrete numbers, such as $d + 1$ , $d ( \dot { d } + \ddot { 1 } ) , \dots , d ^ { k } ( d + 1 )$ , and so on. When n is larger than the number of leaf nodes in KT ree(d, k) but less than that in KT ree(d, $k + 1 )$ for $1 \leq k ,$ each peer loses partial links due to the absence of some out-neighbors and in-neighbors. In such a scenario, a P2P overlay network constructed by the above rules no longer possess the desired features, such as the optimal diameter and efficient routing scheme, and suffers from failed routing between partial pairs of nodes.

To address such an issue, we propose a general overlay network, BAKE, based on an incomplete Kautz tree IKT ree(d, k, n). The number of n peers form an overlay network according to the following rules. For each peer $x = x _ { k } \ldots x _ { 2 } x _ { 1 }$ , it maintains a total number of $\cdot d { \ + 2 }$ links to its predecessor, successor, and d out-neighbors. The predecessor and successor are identified in a distributed manner, as shown in the remainder of this section. The d out-neighbors are the peers satisfying one of the following conditions. For $1 \leq i \leq d _ { \colon }$ , the conditions are as follows.

(1) If a peer $\varsigma _ { 1 } ^ { i } ( x )$ has appeared in the overlay network, it is the $i ^ { t h }$ out-neighbor of the peer x.   
(2) Otherwise, $\mathrm { i f } \varsigma _ { 1 } ^ { i } ( x )$ and its predecessor y have a common suffix with the length $k - 1$ , the peer y is the $i ^ { t h }$ out-neighbor of the peer x.   
(3) Otherwise, if $\varsigma _ { 1 } ^ { i } ( x )$ and its successor z have a common suffix with length of $k - 1$ , the peer z is the $i ^ { t h }$ out-neighbor of the peer x.

THEOREM 1. The above construction rules can ensure that any peer $x = x _ { k } \ldots x _ { 2 } x _ { 1 }$ in BAKE based on $I K T r e e ( d , k , n )$ has d out-neighbors besides its successor and predecessor.

PROOF. All nodes $\varsigma _ { 1 } ^ { i } ( x )$ for $1 \leq i \leq d$ are out-neighbors of node x in a d-ary complete Kautz tree $K T r e e ( d , \bar { k } )$ . For a value of i such that node $\varsigma _ { 1 } ^ { i } ( x ) = x _ { k - 1 } \dots x _ { 2 } x _ { 1 } x _ { 0 } ^ { i }$ does not appear in a d-ary incomplete Kautz tree with the depth of k, Definition 4 can guarantee that at least one child node of node $x _ { k - 2 } \ldots x _ { 2 } x _ { 1 } x _ { 0 } ^ { i }$ exists in the tree and replaces the node $\varsigma _ { 1 } ^ { i } ( x )$ as the $i ^ { t h }$ out-neighbor of the node x. Thus, d nodes act as the out-neighbors of the node x in the tree. If the right adjacent node $y = R a d j a c e n t ( x )$ of the node x does not appear in the tree, then finds the right adjacent node $z = R a d j a c e n t ( y )$ of the node $y .$ If the node z does not appear in the tree, then finds its right adjacent node, and so on. The definition of incomplete Kautz tree makes sure that the successor of each node is, at most, d hops away clockwise from it in a related Kautz ring. The predecessor of node x can be found in a similar method. Therefore, Theorem 1 holds.

Theorem 1 guarantees that each peer has $d$ out-neighbors, a successor, and a predecessor in a static environment. In a dynamic environment, the topology adjustment, peer joining and departing strategies make sure that the $\mathbf { \chi } _ { i ^ { t h } }$ out-neighbor of each peer x is available if no peer fails, where $1 \leq i \leq d .$ . In practice, the $i ^ { t h }$ out-neighbor of peer x becomes unavailable when all peers $\sigma _ { 1 } ^ { j } ( x _ { k - 2 } \dots x _ { 1 } x _ { 0 } ^ { i } )$ have not joined BAKE or failed simultaneously, where $1 \leq j \leq d .$ To deal with the negative impacts of peers that fail randomly or concurrently, two dedicated mechanisms are presented to maintain the topology in the next section. Additionally, a powerful stabilization strategy is introduced to discover failed peers efficiently, and then a flexible peer joining strategy attempts to make the unavailable out-neighbors of each peer to become available.

In summary, the number of out-neighbors of an existing peer in BAKE is usually d in a static or moderately dynamic environment, and is sometimes less than d but becomes d after a recovery period in a highly dynamic environment. The successor and predecessor of each existing peer always exist in any kind of environment.

# 4.2. Resource Placement Based on the Longest Suffix Matching

For any resource to be distributed in BAKE, it is assigned a d-ary identifier $x \ =$ $x _ { l } \ldots x _ { k } \ldots x _ { 2 } x _ { 1 }$ according to its single or multiple attributes. A peer $x _ { k } \ldots x _ { 2 } x _ { 1 }$ is the preferred host of the resource x if the peer has appeared in BAKE, otherwise one existing peer with a suffix $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ acts as the second host. If no peer fails during runtime, the topology-adjusting, peer-joining and departing strategies make sure that at least the peer $\sigma _ { 1 } ^ { \bar { 1 } } ( x _ { k - 1 } \dots x _ { 2 } \bar { x } _ { 1 } )$ always appears in BAKE; hence, the preferred or second host of each resource always exists. Otherwise, if all existing peers with $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ as suffix sometimes fail concurrently, then the preferred and second host peers of each resource might become unavailable.

To address such an issue, we define the predecessor of $x _ { k } \ldots x _ { 2 } x _ { 1 }$ as the third host of the resource x. For example, a resource with identifier 012021 should be stored by its preferred host peer 021 if such a peer exists, but is really taken over by its second host peer 121, that is, the predecessor of the node 021 in a Kautz ring, as shown in Figure 1(b). If peer 121 fails, those incoming resources with 021 as a suffix will be stored by its third host peer 101, that is, the predecessor of peer 121. If the failed peer recovers or is replaced by other new peers, the resource x should be transferred to its first or second host peer.

The resource placement strategy incurs two advantages, as in the following. First, it makes sure that any resource can be stored by an identified peer successfully, even its preferred and second host peers do not appear in BAKE. Second, it guarantees that any resource is stored at a peer as close as possible to its preferred peer, and provides some useful hints to support the exact and range queries about related resources. The details are illustrated in Algorithm 5.

# 4.3. Robust and Effective Routing Scheme

The messages handled by BAKE are partitioned into at least two categories: the messages to publish or query a resource and the messages to maintain the topology. In order to route these kinds of messages to correct destinations effectively, each peer should keep a routing table and establish overlay connections with, at most, $d + \bar { 2 }$ existing peers based on the topology construction rules mentioned above. A routing table of each peer often contains $d + 2$ entries, each of which consists of the logical identifier and physical address (such as IP and port number) of a neighboring peer. [Fiol and Llado 1992] proposed the shortest path routing scheme for a similar routing problem, and we also introduced a more practical routing scheme in our previous work [Guo et al. 2007]. The idea of those schemes to route a message from a peer x to another peer y along the shortest path is as follows. The peer x finds the longest suffix u of x that appears as a prefix of y, and then walks towards a neighbor z such that its longest suffix v coincides with a prefix of y and the length of v is larger than that of u.

Those routing schemes work well in a static environment, but suffer from dynamic P2P networks. For example, peer 202 may fail to route a message to peer 101 along the shortest path $2 0 2  1 2 1 ^ { - }  2 1 0  1 0 1$ , as shown in Figure 1(b), if one peer in the path becomes unavailable. The root cause is that any message is always forwarded towards the unique neighbor that is closer to the destination than itself and its other neighbors. To address such an issue, we propose a robust routing scheme for BAKE, by allowing peers to send a message towards another neighbor when failing to route it along the expected path; refer to Algorithm 5 for more details.

ALGORITHM 5: Route(y, message,model)   
1: if x = y then
2:    if model = peer then
3:    Return available.
4:    else
5:    Process the message locally, and return success.
6: else if Comsuffix(x, y) = k - 1 then
7:    if Comsuffix(x, x.successor) = k - 1 and x.successor is less than y in the kautz ring then
8:    Forward the message to peer x.successor
9:    else
10:    Process the message locally, and return success.
11:    if Comsuffix(x, x.predecessor) = k - 1, and x.predecessor is less than y in the kautz ring then
12:    Forward the message to peer x.predecessor
13:    else
14:    Process the message locally, and return success.
15: else
16:    if Exists, at least, one neighbor z of x such that Common(z, y) is larger than Common(x, y) then
17:    Forward message to the peer which has the largest value of Common(z, y).
18:    else
19:    if common(z, y) = k - 1 then
20:    if model = peer then
21:    Return unavailable
22:    else if Exists a neighbor peer z of peer x such that Comsuffix(z, y) = k - 1 then
23:    Forward the message to peer z.
24:    else
25:    Route(Ladjacent ( $\sigma_{1}^{1}(y_{k-1} \ldots y_{2}y_{1})$ ), message,model).
26:    else
27:    Forward the message to one of existing neighbors because the neighbor towards the destination peer is unavailable.

Comsuffix(x, y)   
1: Return the length of the longest common suffix of $x$ and $y$ .  
Common(x, y)  
1: Let $u$ be the longest suffix of $x$ which appears as a prefix of $y$ .  
2: Return the length of $u$ .

When a peer $x = x _ { k } x _ { k - 1 } . . . x _ { 2 } x _ { 1 }$ publishes or looks-up a resource with an identifier $y _ { l } \ldots y _ { k } \ldots y _ { 2 } y _ { 1 }$ , the preferred destination is a peer $y = y _ { k } \ldots y _ { 2 } y _ { 1 }$ . If the peer y does not exist, the peer x immediately identifies another peer z as the second host of such a resource, and then forwards the message to the peer z. If the peer z does not exist, the peer x routes the message towards its third host peer. For example, in Figure 1, a peer 010 initially routes a resource with an identifier 012021 towards a peer 021 along a path $0 1 0  2 0 2  0 2 1$ . If the peer 202 finds that the preferred host peer 021 does not exist, it then forwards the message to the second host peer 121. If the peer 202 finds that the peer 121 also fails, it routes the message towards the peer 201 along a path 202 → 020 → 201. The resource is finally stored by a more accurate destination, peer 101. Note that the decision on a new destination can be made based only on the local knowledge at each peer.

Algorithm 5 gives a formal and detailed explanation about our routing scheme, and uses three parameters, as in the following. The parameter y denotes an identifier of a resource or destination peer. The parameter message denotes the real message needed to be routed. The parameter model denotes the type of message, which can be peer or resource. If a peer issues a message to detect the status of a peer y, then $m o d e l = p e e r$ . The destination of such a message cannot be changed during the routing process in order to reflect the real status of the peer y. If a message is used to publish or look-up a resource, then model = resource. The destination of the message might be adjusted to locate a suitable destination in a dynamic environment.

If each peer uses all neighboring peers except its predecessor and successor when routing messages, Algorithm 5 exhibits a short path, but not always the shortest path. In other words, the routing scheme routes messages among a majority of peers along the shortest path with, at most, k hops. As mentioned above, the clockwise and anticlockwise distance between two peers can be estimated by Algorithm 4. If each peer also employs its predecessor and successor when routing messages, it can select the shortest one among the traditional paths, a path along its predecessor links and a path along its successor links. For example, a traditional short path from peer 020 to peer 121 is $0 2 0  1 0 1  2 1 2  1 2 1$ , while 020 → 101 → 121 is the shortest path that walks along the successor link of peer 101. The advantage of the new strategy is more remarkable when $d \leq k .$ . Algorithm 5 can reflect such an improvement after minimal modifications. In summary, our routing scheme is effective and robust, and the predecessor and successor of each peer can help to enhance the robustness and efficiency of the routing scheme.

# 4.4. Query Processing

Clearly, BAKE can support exact-match queries of resources in an efficient and robust manner. In order to manage complex resources and support more wide applications, BAKE should also support the complex query operations besides the exact-match query in a graceful fashion: for example, the range query for numerical values. The precondition of a range query in a P2P network is to distribute those resources that keep an order in a single or multiple attribute space to peers in a locality-preserving manner. In other words, those resources with attribute values close to each other should be stored on the same peer or on neighboring peers. To achieve such a goal, BAKE must address the following three critical issues: a total ordering of peers; a locality-preserving naming; and a placement strategy of resources.

The topology construction rule guarantees that each peer u has a successor link to a peer v such that the clockwise distance from u to v is less than that to other peers, and all peers form a Kautz ring through the successor links. On the other hand, each resource is stored on a peer whose identifier has the longest common suffix with the identifier of a resource. BAKE selects the first peer meeting the criteria along the Kautz ring clockwise. Hence, the first two issues are addressed. For the third issue, we recursively partition the attribute space of resources into subspaces in a similar method as constructing a complete Kautz tree. We then associate each subspace with an identifier in the same way as allocating identifiers for nodes in Kautz tree. Each resource finds the smallest subspace that contains its attribute values and uses the identifier of that subspace as its identifier. Therefore, those resources with attribute values close to each other will obtain adjacent identifiers in the Kautz ring, or even the same identifier. Thus they are stored by the same or neighboring peers obeying the locality-preserving placement strategy.

Any peer $x _ { k } \ldots x _ { 2 } x _ { 1 }$ that issues a range query can find the identifier y of the smallest subspace that contains the entire query region. If the length of y is larger than k, a peer whose identifier is the suffix of y will process the query. Otherwise, the query covers multiple peers and will be routed towards the peer that reaches the lower bound of the region first. On receiving the query, the peer sends the query message to its successor peer if it cannot cover the entire query region, so on and so forth. A query message will traverse all intersection peers and collect all resources that satisfy the query constraints.

![](images/b252a4003012dbe111488350f635241dff509e1374e0073565677210315c1984.jpg)



![](images/e8576f53cc7e1a9fc7849e7ed91e2224337c7076961eeded81dd9fde17a47cc2.jpg)



Fig. 2. Achieving IKT ree(2, 3, 6) by expanding KT ree(2, 2).

This method can decrease the message cost caused by transferring the query messages to all intersection peers, but the delay could be a little bit longer than forwarding the query to all related peers simultaneously. There exists a tradeoff between the query delay and the query cost.

# 5. TOPOLOGY MANAGEMENT

# 5.1. Topology Adjustment

A native BAKE based on an initial KT ree(d, k) can be constructed in advance. All leaf nodes of KT ree(d, k) are allocated to $d ^ { k } + \dot { d } ^ { k - 1 }$ peers. When more new peers wanted to join, however, there were no available leaf nodes to be used in $\tilde { K T } r e e ( d , k )$ . In such a situation, we expand the $K T r e e ( d , k )$ to achieve an incomplete Kautz tree $I K T r e e ( d , k + 1 , \stackrel { \cdot } { d ^ { k } } + d ^ { k - 1 } )$ . If the number of existing peers reaches $( d \dot { + } 1 ) \times ( d ^ { k } + d ^ { k - 1 } )$ the incomplete Kautz tree becomes a complete one and is ready to be expanded further.

As shown in Figure 2, it is straightforward to expand $K T r e e ( d , k )$ to achieve an incomplete Kautz tree $I \dot { K } T r e e ( d , k , \breve { d ^ { k } } + d ^ { k - 1 } )$ by adding the first child node of each leaf node into the complete Kautz tree. To expand the topology of BAKE, we introduce an efficient solution that needs only local operations at each existing peer. For an existing one labeled with $x = x _ { k } x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ in BAKE, we

(1) update its logical identifier with $\sigma _ { 1 } ^ { 1 } ( x ) ;$   
(2) update the logical identifier of its successor peer $x ^ { \prime } = x _ { k } ^ { \prime } x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ with $\sigma _ { 1 } ^ { 1 } ( x ^ { \prime } ) ;$ ; the logical identifier of its predecessor peer is updated similarly; and   
(3) update the logical identifier of its out-neighbor peer $\varsigma _ { 1 } ^ { i } ( x )$ with $\sigma _ { 1 } ^ { 1 } ( \varsigma _ { 1 } ^ { i } ( x ) )$ for ${ \textbf { 1 } } { \leq }$ $i \leq d .$ .

Figure 3(a) shows the topological structure of BAKE based on a complete Kautz tree KT ree(2, 2), while Figure 3(b) plots that of BAKE after invoking the topology expanding process.

THEOREM 2. The topology expanding process of the entire overlay network does not cause additional overhead, except for $\breve { d } ^ { k } + d ^ { k - 1 }$ messages to start the process.

PROOF. A resource whose identifier has a suffix $x _ { k } \ldots x _ { 2 } x _ { 1 }$ is stored by a peer $x = x _ { k } \ldots x _ { 2 } x _ { 1 }$ . The peer x updates its logical identifier with $\sigma _ { 1 } ^ { 1 } ( x ) = x _ { k + 1 } ^ { i } x _ { k } . . . \overset { \cdot } { x _ { 2 } x _ { 1 } }$ after expanding. The peer is the preferred host of the resources whose identifiers have a suffix $\sigma _ { 1 } ^ { \mathrm { 1 } } ( x ) _ { \mathrm { : } }$ , and becomes the second host of other resources stored at it before.

![](images/820ca535d9eb08beba5b4a5ab0603d05d41da36f05ec7010a45effc89690f049.jpg)



(a)

![](images/0f3cc890d555f72f20882961887072cbf1782e4d3d7c41aaad6b17cf8a75b772.jpg)



Fig. 3. The topology of BAKE after invoking the topology expanding process.

Therefore, the expanding process does not introduce any network overhead because each resource still stays at the original peer after the process.

Before performing the process, each peer x maintains links to its out-neighbors $x _ { k - 1 } \ldots x _ { 1 } \alpha$ where $\alpha \in \{ 0 , 1 , 2 , \ldots , d \} - \{ x _ { 1 } \}$ . After invoking the expanding process, the peer obtains a new logical identifier $\sigma _ { 1 } ^ { 1 } ( x ) = x _ { k + 1 } ^ { 1 } x _ { k } \dots x _ { 2 } x _ { 1 }$ , and should maintain links to peers $x _ { k } ^ { \prime } \ldots x _ { 2 } x _ { 1 } \beta$ , where $\beta { \in } \{ 0 , 1 , 2 , \dotsc , d \} - \{ \stackrel { \dotsc } { x _ { 1 } } \}$ and the value of $x _ { k } ^ { \prime }$ obeys the topology construction rule of the incomplete Kautz tree mentioned above. Note that the parent nodes of out-neighbors of node $\sigma _ { 1 } ^ { 1 } ( x )$ are $x _ { k - 1 } \ldots x _ { 1 } \beta$ where $\beta \in \{ 0 , 1 , 2 , \dotsc , d \} - \{ x _ { 1 } \}$ , which are the same neighbors before expanding, although their logical identifiers are updated with the labels of their first child nodes. On the other hand, the physical identifiers of the successor and predecessor of peer $\sigma _ { 1 } ^ { 1 } ( x )$ do not change, although the logical identifiers are updated. In other words, the links maintained by each peer do not need to be changed, and no further network overhead is incurred.

Thus, Theorem 2 holds.

In contrast, to expand the overlay, BAKE shrinks its topology when the number of existing peers decreases to the number of leaf nodes in a d-ary complete Kautz tree. More precisely, We shrink an incomplete Kautz tree IKT ree(d, k, $d ^ { k ^ { 2 } } + d ^ { k - 1 } )$ t o a complete Kautz tree KT ree(d, k) by deleting all original leaf nodes. For an existing peer $x = x _ { k + 1 } \ l . . . x _ { 2 } x _ { 1 }$ , we replace its logical identifier with $x _ { k } \ldots x _ { 2 } x _ { 1 }$ , and update the logical identifiers of its predecessor, successor, and out-neighbors in the same way. Obviously, we do not cause much network overhead, except for sending $d ^ { k } + d ^ { k - 1 }$ messages to start the process. Note that Figure 2 and Figure 3 also plot the changes caused by the topology shrinking operation.

The two types of topology adjustments can be implemented in a synchronous or asynchronous manner. In the synchronous case, all peers are not allowed to query or publish resources during relabeling their identifiers. In the asynchronous manner case, each peer has to route received messages before all peers finish relabeling their identifiers. If the message type is resource, the routing policy based on the longest suffix-matching does not suffer from any intermediate peer that has not relabeled its identifier. If the message type is peer and the identifiers of the message and an intermediate node are different in length, the routing scheme still work well by adaptively adjusting the identifier of the message or neighbors of the intermediate node. In summary, the routing scheme proposed in this article can route each message successfully, even when some intermediate peers have not relabeled their identifiers.

![](images/4465827ebae7aae3a4dbc262d4966e27abda9c39261cea9de8cda318415e53f4.jpg)



![](images/f662e37e1c9cf8318a13501b51ade802cb57511ce0b2551f865dca8c762db12b.jpg)



(b)   
Fig. 4. The topological structure of BAKE based on IKT ree(2, 3, 7).

# 5.2. Peer Joining

To ensure that our routing scheme executes correctly after a new peer participates in BAKE, all routing entries of each peer must keep up to date. BAKE handles such an event by a series of local operations that are invoked when each new peer joins.

The peer related to the leftmost leaf node $\sigma _ { k - 1 } ^ { 1 } ( 0 )$ in a d-ary incomplete Kautz tree with depth k acts as the first entry point for BAKE, and its predecessor acts as a synchronous second entry point. The entry points first serve as general peers, and also manage all the labels of leaf nodes in the incomplete Kautz tree. The entry points allocate leaf nodes to peers as follows. First, if a peer x fails and recovers in time, the entry points will still allocate the leaf node that was associated with the peer x before it fails to the node x after it recovers if that leaf node has not yet been assigned. This can prevent the resources stored at a failed peer from being transferred to another peer after that peer recovers. Second, they allocate the leaf node x whose position(x) is 1, implying that it is the first child node of its parent node, and then the leaf node whose position is 2, implying that it is the second child of its parent, and so on. Third, for the leaf nodes with the same position value, it allocates them in the clockwise order at a Kautz ring of their parent nodes, denoted as Korder, or based on the load (storage and accessing load) of their predecessors in descending order, denoted as Border. If all leaf nodes have been allocated, the first entry point starts the topology-expanding process, and may start the topology-shrinking process on demand.

Before participating in BAKE, a new peer consults the first entry point for a logical identifier $x = x _ { k } \ldots x _ { 2 } x _ { 1 }$ , its predecessor y and successor z, and identifies its outneighbors with the following process. Note that the peers that have $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ as the common suffix possess the same out-neighbors. If there exists at least one such peer, the peer x can get a copy of the out-neighbors from its predecessor or successor. Otherwise, the peer x uses Algorithm 6 to discover its out-neighbors obeying the topology rules in the worst case.

The peer x also acts to handle the impact of its participation on other peers. More precisely, it informs the peer $\tau _ { 1 } ^ { i } ( x )$ for $\hat { 1 } \leq i \leq d$ to update an out-of-date neighbor by sending a message. The message is first routed towards peer $u = \tau _ { 1 } ^ { 1 } ( x ) _ { : }$ , and then forwarded to other related peers along the successor links. Figure 3 plots the topology of BAKE based on IKT ree(2, 3, 6), while Figure 4 shows the topology of BAKE after adding new peer 120.

THEOREM 3. For BAKE based on an incomplete Kautz tree IKT ree(d, k, n), to join a new peer x will affect one out-link of, at most, $\lceil 2 + n / ( d ^ { k - 1 } + d ^ { k - 2 } ) \rceil$ existing peers.

PROOF. The first entry point allocates a label of one (i + 1)th child node of an inner node at the level k− 1 to a new peer only if all $i ^ { t h }$ child nodes have been allocated for $1 \leq$ $i \le d - 1$ . The number of $\because t h$ child nodes of all inner nodes at level k− 1 in $K T r e e ( d , k , n )$

ALGORITHM 6: Findneighbor(x)   
1: if $\text{Comsuffix}(\varsigma_{1}^{1}(x), \text{Ladjacent}(\varsigma_{1}^{1}(x))) = k - 1$ then
2: $u \leftarrow \text{Ladjacent}(\varsigma_{1}^{1}(x))$ 3: else
4: $u \leftarrow \text{Radjacent}(\varsigma_{1}^{1}(x))$ 5: Create a message containing $\varsigma_{1}^{i}(x)$ for $1 \leq i \leq d$ , and route it towards peer u based on the routing scheme.
6: The message reaches a peer v such that $Common(u, v) = k - 1$ , and peer v forwards it to peer $\varsigma_{1}^{j}(v)$ for $1 \leq j \leq d$ .
7: Once peer $\varsigma_{1}^{j}(v)$ receives the message, it selects a w from $\varsigma_{1}^{i}(x)$ for $1 \leq i \leq d$ such that $Comsuffix(v, w) = k - 1$ , and then forwards the message to w along the successor links or predecessor links.
8: Peer $\varsigma_{1}^{j}(v)$ selects one from peer w, its predecessor, and its successor according to the topology rules, and returns the selection result as one out-neighbor of peer x.

is $d ^ { k - 1 } + d ^ { k - 2 }$ for $1 \leq i \leq d .$ . The topology rules make sure that at most, $\lceil { n } / ( d ^ { k - 1 } + d ^ { k - 2 } ) \rceil$ peers select the peer x as its one out-neighbor. On the other hand, the peer x also affects its successor and predecessor. In summary, at most, $\lceil 2 + n / ( d ^ { k - 1 } + d ^ { k - 2 } ) \rceil$ peers need to update one routing entry and one overlay link, and thus Theorem 3 holds.

# 5.3. Peer Failures and Stabilizations

The correctness and effectiveness of BAKE relies on the fact that the predecessor, successor, and out-neighbors of each peer are up to date. However, such an invariant can be compromised if peers fail. For example, in Figure 1(b), if a node 120 fails, a node 020 will not know that node 010 becomes its successor, and node 212 will not know that the node 120 is no longer one of its neighbors. An incorrect neighbor will increase the delay in routing a message, and even fail to deliver messages correctly.

To improve the robustness of the topology and sustain high performance in message routing, each peer periodically checks the out-links that are not used in the current round, and identifies failed peers to inform the first entry point. A failed peer would not be found only if $d + 2$ peers that keep links to it fail simultaneously, which is very improbable with modest values of d. In practice, a failed peer is often discovered early during communications before the end of an entire round. A failed peer $x = x _ { k } \ldots x _ { 2 } x _ { 1 }$ affects at most $d { \pm 2 }$ existing peers. Once the failure of peer x is identified, peers keeping links to peer x repair their local topologies according to the rules.

If the predecessor u of the peer x first finds the failure of $x ,$ it will detect peers along a related Kautz ring clockwise, until it finds the first existing peer as its new successor v. By comparing peers $u , x ,$ and $v ,$ the peer u can find a substitute for peer $x ,$ obeying the following rules. If Comsuf $\mathbf { \hat { f } } \mathbf { x } ( u , x ) = k - 1$ , the peer u is the substitute of peer x; else if Comsu $\mathrm { f f i x } ( v , x ) = k - 1$ , peer v is the substitute for peer $x ;$ otherwise peer u is the substitute for peer x. Peer u will notify the change to one in-neighbor peer of the failed peer x, for example, a peer $\tau _ { 1 } ^ { 1 } ( x )$ . If the peer $\tau _ { 1 } ^ { 1 } \breve { ( \boldsymbol { x } ) }$ also fails, the routing schema makes sure that the notification message can be routed to related peers. As long as one in-neighbor of peer x receives such a notification message, it forwards the message to other related peers along the successor and/or predecessor links. Thus, the negative impact of the failed peer x can be discovered and repaired in time. If the successor of peer x first finds the failure, it executes similar actions as peer u does. In order to decrease the delay and cost of the topology adjustment, each peer can keep physical identifiers of multiple successors in the Kautz order, but must establish a link with the first successor only. When the first successor fails, it connects the second successor, and so on. If the number of successors of each peer are of moderate value, those successors are unlikely to fail at the same time.

# 5.4. Peer Departing

BAKE always sustains a stabilization period to repair destroyed routing tables of some peers due to failed peers. A peer departing from BAKE voluntarily, however, can repair the topology actively before it leaves. For example, once peer 120 departs BAKE, as shown in Figure 4, the resultant topology of BAKE is plotted by Figure 3(b).

For a peer x = xk . . . x2x1 that is about to leave, if its predecessor y or successor z has a suffix $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ , it notifies peers $y , z ,$ and the first entry point of BAKE. In turn, the peer y will update its successor with z, and peer z will replace its predecessor with peer y. If peer y has a suffix $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ , peer x transfers its resources to peer y, and notifies its in-neighbor peer $\tau _ { 1 } ^ { i } ( x )$ to replace the link to it with another link to peer y for $1 \leq i \leq d$ . If peer y does not have a suffix $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ while peer z has, peer x transfers its resources to peer z, and notifies its in-neighbor peer $\tau _ { 1 } ^ { i } { \bar { ( x ) } }$ to replace the link to it with another link to peer z for $1 \leq i \leq d .$

If none of the peers y and z have a suffix $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ , then peer x consults the first entry point of BAKE to find a substitute peer w before it departs. The peer w must satisfy the following two constraints: (1) there are other peers that have a common suffix of length $k - 1$ with peer w in BAKE; (2) the value of position(w) should be as large as possible. The peer w will perform a voluntary departure operation, and take over the resources, logical identifier, and routing table of peer x. It then informs neighbors of the peer x to update the physical identifier of peer x. After such a process, the original peer x can depart BAKE. The selection rule of peer w can guarantee that it need not find another substitute peer before it departs.

# 5.5. Further Improvement

BAKE does not introduce additional overhead to expand or shrink the network topology, except for sending n messages to start the two operations, where n denotes the number of peers. Clearly, BAKE conducts fewer and fewer such operations, as the order becomes large during its evolution process. BAKE, however, might often expand and shrink the topology when the value of n fluctuates around $d ^ { k } + d ^ { k - 1 }$ in the worst case. To address such a special case, we propose a delay strategy to decrease the frequency of such operations, as follows. If all logical identifiers have been assigned to existing peers, BAKE allows a new peer to share a logical identifier with an existing peer that suffers from high storage load or accessing load. For example, an existing peer $x = x _ { k } \ldots x _ { 2 } x _ { 1 }$ transfers resources with $\sigma _ { 1 } ^ { 2 } ( x )$ as a suffix to a new peer that shares the same identifier with it. In other words, BAKE only expands its topology when the value of n exceeds $d ^ { k } + d ^ { k - 1 }$ and becomes relatively stable. During this process, peer x updates its identifier with $\sigma _ { 1 } ^ { 1 } ( x )$ , while the peer sharing the identifer with it obtains a new identifier $\sigma _ { 1 } ^ { 2 } ( x )$ .

The above strategy delays the topology-expanding operation, and decreases the load of some peers with the help of new peers. For a similar reason, BAKE only shrinks its topology when the value of n is less than $d ^ { k - 1 } + d ^ { k - 2 }$ and becomes relatively stable.

# 6. PERFORMANCE

We first show that BAKE achieves an optimal diameter and connectivity, as the Kautz digraph does, through analysis and simulation. We then evaluate the robustness of the routing scheme we proposed, and the delay and message cost of major operations.

Table I. The Degree/Diameter Tradeoff of Different Topologies 

<table><tr><td>Topology</td><td>Degree</td><td>Diameter</td><td>Average length of routing path</td></tr><tr><td>Hypercube</td><td> $\log n$ </td><td> $\log n$ </td><td> $1/2\log n$ </td></tr><tr><td> $d$ -torus</td><td> $2d$ </td><td> $1/2dn^{1/d}$ </td><td> $1/4dn^{1/d}$ </td></tr><tr><td> $d$ -dimensional Butterfly</td><td> $d$ </td><td> $2\log_{d}n(1 - o(1))$ </td><td> $\frac{3n(d-1)+2d}{2(n-1)}$ </td></tr><tr><td> $d$ -ary de Bruijn digraph</td><td> $d$ </td><td> $\log_{d}n$ </td><td> $\log_{d}n - 1/(d - 1)$ </td></tr><tr><td> $d$ -ary Kautz digraph</td><td> $d$ </td><td> $\log_{d}n - \log_{d}(1 + 1/d)$ </td><td> $\log_{d}n - \log_{d}(1 + 1/d) - 1/(d + 1)$ </td></tr></table>

![](images/fd48c5c124ca050957238676b160b3fe226a1cf718a40beb8e41b43d2fa19eb7.jpg)



Fig. 5. The diameter of several topologies under different configurations.

# 6.1. Topology Properties

Table I shows the network diameter, the node degree, and average length of the routing paths of the Kautz diraph and relevant topologies. The diameter of BAKE, based on the balanced Kautz tree, is given by Theorem 4.

THEOREM 4. The out-degree of each peer is d + 2 in BAKE with n peers, and the diameter is $\begin{array} { r } { k _ { l } = \lceil \log _ { d } \frac { n } { d + 1 } + \mathbf { \bar { 1 } } \rceil } \end{array}$ .

PROOF. First, we calculate k such that $d ^ { k - 1 } + d ^ { k - 2 } < n < d ^ { k } + d ^ { k - 1 }$ . Thus, the length of the peer identifier must be k, and we can find a pair of peers at the distance k along the shortest path. Thus kl equals $\textstyle \lceil \log _ { d } { \frac { n } { d + 1 } } + 1 \rceil$ , and almost achieves the Moore bound [Miller and Siran 2005].

To understand the diameter property in practice, we simulate BAKE and the relevant topologies where n ranges from 320 to 22528 and d equals 4. The simulation result is shown in Figure 5. Note that the Kautz digraph and BAKE have desirable properties for peer-to-peer networks that stem from their small diameters as shown in Table I and Figure 5. However, the diameter is simply the largest distance between any pair of peers. A much more balanced metric is the average distance between any pair of peers, since this is the performance that a user can expect from the peer-to-peer system when searching for objects. We therefore evaluate the average value and distribution of the length of routing paths among all node pairs. Table I shows the average length of the routing paths of several topologies in theory. To understand this metric in practice, we let each peer issue a message to other n− 1 peers, and then analyze the average length over n(n − 1) routing paths.

Let ard denote the average value of a routing path. We compare BAKE with MOORE [Guo et al. 2007] and other constant-degree topologies in which the out-degree of each peer is 4, such as the 2-dimensional CAN, 4-dimensional butterfly digraph, 4-ary de Bruijn digraph, and 4-ary Kautz digraph. Figure 6 plots the experimental results. The curves of the butterfly, de Bruijn, and Kautz digraphs are dashed lines or discrete points, since their orders are special discrete sequences, while that of BAKE and

![](images/d4267d6a5d76deb08c44eee22a4da248982dc9e7bb05c2f4ac78947adb9a7385.jpg)



Fig. 6. The average routing distance under different configurations.

![](images/ddb05f7fbb3a1024a3387dd0998b81d955da6b453685c5ec52cc7b2eafa8ab8e.jpg)



![](images/f5f1ce3db8ad49ca805c2437e514b75f64c8f2c9495a0d0455430a79e8ace0ef.jpg)



Fig. 7. The routing and in-degree distributions of IKTree(4,7,12800).

MOORE are solid lines. The ard of BAKE and MOORE are shorter than that of butterfly, CAN, $1 . 2 \log _ { 4 } n ,$ , and de Bruijn. The ard of BAKE is less than that of MOORE because of the predecessor and successor of each peer. The ard of BAKE is a little bit less than that of the Kautz digraph when $n = d ^ { i } + d ^ { i - 1 }$ for ${ \bf 1 } \le i { \bf \Phi } _ { ; }$ , since partial routing paths in the Kautz digraph are shortened with the help of the successor and predecessor links of each peer. In summary, BAKE achieves the optimal topology that inherits good properties of the Kautz digraph, even its order is out of $d ^ { k } + d ^ { k - 1 }$ for a given d and any k> 1.

Recall that to improve the fault-tolerant capability of BAKE, we add a predecessor and a successor for each peer besides d out-neighbors. That is to say, the out-degree of each peer is $d + 2$ . Without loss of generality, we compare BAKE with CAN under two different configurations where the out-degree of each peer in BAKE is 6. Let CAN:d = 2 and CAN:d = 3 denote the 2-dimensional CAN and 3-dimensional CAN, respectively. As shown in Figures 5 and 6, BAKE holds a lower diameter and average routing path than CAN under the two scenarios, and the difference for each metric increases with the increases in the number of peers.

The left side of Figure 7 plots the pdf of the routing path length for a BAKE with 12,800 peers $( d = 4 )$ . The length of about 60% of routing paths equals the diameter. If we compare BAKE with MOORE with the same configuration, the length of fewer routing paths for BAKE equal the diameter, and more BAKE routing paths are fewer than the diameter. The right side of Figure 7 indicates that the in-degrees of most peers are adjacent to $d + 2 ,$ , and those of the remaining peers are close to the trail of the curve.

![](images/a140d06c579f6bf205c71cccef7ea70b75f96fb0300a530a7a2c070290dbd1be.jpg)



![](images/c1aa9612fe94e9bf36e2fa1e2b7a4621ce5b36fa4dd68f7b2fb329186ce04846.jpg)



Fig. 8. The fraction of successful queries as a function of the number of peers that failed concurrently.

# 6.2. Robustness of the Routing Scheme

The routing schemes mentioned in Guo et al. [2007] and Fiol and Llado [1992] suffer from the poor robustness of dynamic environments. BAKE addresses this by sending a message to another out-neighbor when failing to forward the message along the shortest path. The connectivity of each peer in BAKE is $d + 2 _ { \mathrm { { i } } }$ , implying that as long as $d + 2$ neighbors and/or links do not fail simultaneously, a message can be delivered to another available peer successfully. In other words, when d is a modest value, any message can reach its destination with high probability even when peers fail concurrently, as shown in Figure 8. BAKE makes sure that a large majority of messages between any peer pair can be routed successfully when $d ,$ even 2d, peers fail concurrently; thus, our routing scheme outperforms existing schemes.

# 6.3. Delay and Message Cost of Basic Operations

We define $\alpha = \lceil n / ( d ^ { k _ { l } - 1 } + d ^ { k _ { l } - 2 } \rceil$ for later analysis. For a message to lookup or publish a resource with an identifier $x = x _ { k } \ldots x _ { 2 } x _ { 1 } .$ , the routing delay is, at most, $t ( \bar { k _ { l } } - 1 ) + k _ { l }$ hops before it reaches an available host $y = y _ { k } \ldots y _ { 2 } y _ { 1 }$ , where t denotes the anti-clockwise distance from the node $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ to the node $y _ { k - 1 } \ldots y _ { 2 } y _ { 1 }$ in the given Kautz ring. In a static system, delay of all queries is kl because the peer $y$ is always the preferred host. In a moderately dynamic system, delay of a majority of queries is $k _ { l }$ because the peer y usually is the preferred or second host. In a highly dynamic system, delay of lots of queries is $\dot { t } ( k _ { l } - 1 ) + k _ { l }$ because peer y is often the third host peer. The value of t is usually one, but is sometimes larger than one.

THEOREM 5. In a static or moderately dynamic environment, the delay and message of joining a peer x are, at most, $k _ { l } + d + 4$ and $k _ { l } + 2 d + 4 ,$ respectively.

PROOF. First, peer x consults the first entry point of BAKE and gets information about its successor and predecessor within two hops. Second, peer x notifies its successor and gets a copy of its out-neighbors within two hops. Third, peer x concurrently establishes links with d out-neighbors within one hop, while its successor notifies its predecessor within one hop. Fourth, peer x notifies one of its in-neighbors $\tau _ { 1 } ^ { 1 } ( x )$ after traversing, at most, kl peers. Finally, peer $\tau _ { 1 } ^ { 1 } ( x )$ notifies, at most, $\alpha - 1$ other in-neighbors of peer x within $\alpha - 1$ hops by adopting the successor link of peer $\tau _ { 1 } ^ { 1 } ( x )$ and all intermediate peers.

In summary, the number of message caused by a new peer is at most $2 + 2 + d + 1 +$ $h _ { l } + \alpha - 1 = h _ { l } + d + \alpha + 4$ , and is less than $k _ { l } + \bar { 2 } d + 4$ . Meanwhile, the delay cost is at most $2 + 2 + 1 + k _ { l } + \alpha - 1 = k _ { l } + \alpha + 4$ hops, and is less than $k _ { l } + d + 4$ . Thus, Theorem 5 holds.

Note that it is not necessary for a new peer to discover all out-neighbors, since it can retrieve from its predecessor or successor in a static or moderately dynamic environment. If BAKE is deployed in a highly dynamic environment, a new peer may need to find d out-neighbors itself, since its predecessor or successor may not have common out-neighbors.

COROLLARY 1. In a highly dynamic environment, we know that peer x might invoke Algorithm 6 to discover its out-neighbors. The delay of joining a peer $x \ i s ,$ at most, $2 \bar { k _ { l } } + d + 1$ hops. The whole process causes at most $2 \bar { k _ { l } } + 2 \bar { d } + 2$ messages.

PROOF. After consulting the first entry point of BAKE, peer x routes a message to its first out-neighbor $\bar { S } _ { 1 } ^ { 1 } ( x )$ . This message reaches a peer v that is one hop away from the destination after, at most, $k _ { l } - 1$ hops. The peer v then concurrently forwards the received messages to its all out-neighbors within one hop. Note that the topology construction rule guarantees that out-neighbors of peer v are just out-neighbors of peer x. During the process of discovering out-neighbors, peer x also notifies its successor within one hop, and the successor also informs the predecessor of peer x within one hop. Finally, the process of notifying in-neighbors of peer x is the same as we discussed in Theorem 5.

In summary, a new peer causes $2 + k _ { l } - 1 + d + 1 + 1 + k _ { l } + \alpha - 1 = 2 k _ { l } + d + \alpha + 2 <$ $2 k _ { l } + 2 d + 2$ messages, and takes $2 + k _ { l } - 1 + 1 + k _ { l } + \alpha - 1 = 2 k _ { l } + \alpha + 1 < 2 k _ { l } + d + 1$ hops. Thus, Corollary 1 holds.

THEOREM 6. In the worst case, the messages caused by handling a failed peer $x = x _ { k } \ldots x _ { 2 } x _ { 1 }$ is $d ( k _ { l } + 1 )$ , and the delay is $( d - 1 ) k _ { l } + d .$ . In the general case, the messages resulting from handling a failed peer is $3 k _ { l } + \alpha ,$ , and the delay is $2 k _ { l } + \alpha$ .

PROOF. In such a scenario, peer u should find a substitute for peer x once it discovers the failure of peer x. Here, peer u can be the predecessor, or successor, or one in-neighbor of peer x. In the worst case, peer u needs to detect $\alpha - 1$ peers at the cost of at most $( \alpha - 1 ) \times k _ { l }$ messages and $( \alpha - 1 ) \times k _ { l }$ hops. Note that those α peers and peer x have a common suffix with length $k - 1$ . In the general case, peer u just detects the left and right adjacent peers of peer x at the cost of $2 k _ { l }$ messages and hops. At the same time, peer u also notifies the first entry point of BAKE at the cost of at most kl hops and messages. Finally, peer u notifies other in-neighbors of peer x at the cost of $\alpha - 1$ hops and messages if it is an in-neighbor of peer x.

In summary, the messages and delay in handing a failed peer are at most $\alpha \times k _ { l } + \alpha <$ $d ( k _ { l } + 1 )$ and $( \alpha - 1 ) k _ { l } + \alpha < ( d - 1 ) k _ { l } + d _ { \ast }$ , respectively. In the general case, the messages and delay are at most $3 k _ { l } + \alpha$ and $2 k _ { l } + \alpha$ , respectively. Thus, Theorem 6 holds.

THEOREM 7. The delay and message in handling a leaving peer $x = x _ { k } \ldots x _ { 2 } x _ { 1 }$ are at most $3 k _ { l } + d - 1$ and $3 k _ { l } + d + 1 _ { \cdot }$ , respectively.

PROOF. Peer x notifies its departure to the first entry point of BAKE within at most, $k _ { l }$ hops, and retrieves a substitute within at most $k _ { 1 }$ hops when the substitute is the only existing peer with a suffix $x _ { k - 1 } \ldots x _ { 2 } x _ { 1 }$ . The peer x then notifies its predecessor and successor in one hop, and one of its in-neighbors within at most kl hops. Once one in-neighbor of peer x receives a notification, it will inform other $\alpha - 1$ in-neighbors of peer x within $\alpha - 1$ hops.

In summary, the number of messages caused by handling a leaving peer is at most $2 k _ { l } + 2 + k _ { l } + \stackrel {  } { \alpha } - 1 = 3 k _ { l } + \alpha + 1 < 3 k _ { l } + d + 1$ , while the delay is at most $2 \bar { k } _ { l } + k _ { l } + \alpha - 1 =$ $3 h _ { l } + \alpha - 1 < 3 h _ { l } + d - 1$ . Thus, Theorem 7 holds.

# 7. CONCLUSION

Structured peer-to-peer networks have been proposed for building large-scale and robust network applications. Researchers have proposed several P2P networks based on interconnection networks with fixed-degree and logarithmical diameter. Among existing fixed-degree interconnection networks, the Kautz digraph has many distinguished topological properties compared to others. In this article, we propose the balanced Kautz tree and Kautz ring structures that ensure the robustness and correctness of structured peer-to-peer networks that emulate the Kautz digraph in dynamic environments. We then design a novel structured P2P network based on the two structures, called BAKE, that has a logarithmical diameter and a constant degree, even the number of peers is an arbitrary value. We further design a locality-preserved resource placement strategy, an effective and robust routing scheme, and several essential algorithms to deal with the dynamic operations of peers. Via analysis and simulation, we show that BAKE achieves the optimal diameter, high performance, and a good connectivity as the Kautz digraph does. Moveover, the structures of balanced Kautz tree and Kautz ring we proposed can also be applied to other interconnection networks after minimal modifications, for example, the de Bruijn digraph.

# REFERENCES

BANERJEE, S. AND SARKAR, D. 2001. Hypercube connected rings: A scalable and fault-tolerant logical topology for optical networks. Comput. Commun. 24, 1060–1079.   
COOPER, B. F., RAMAKRISHNAN, R., SRIVASTAVA, U., SILBERSTEIN, A., BOHANNON, P., JACOBSEN, H.-A., PUZ, N., WEAVER, D., AND YERNENI, R. 2008. Pnuts: Yahoo!’s hosted data serving platform. Proc. VLDB 1, 2, 1277–1288.   
DAMERELL, R. 1973. On Moore graphs. Proc. Cambridge Phil. Soc. 227–236.   
DECANDIA, G., HASTORUN, D., JAMPANI, M., KAKULAPATI, G., LAKSHMAN, A., PILCHIN, A., SIVASUBRAMANIAN, S., VOSSHALL, P., AND VOGELS, W. 2007. Dynamo: Amazon’s highly available key-value store. In Proceedings of the 21st ACM SOSP Conference. ACM, New York, 205–220.   
FIOL, M. A. AND LLADO, A. 1992. The partial line digraph technique in the design of large interconnection networks. IEEE Trans. Comput. 41, 7, 848–857.   
FRAIGNIAUD, P. AND GAURON, P. 2003. An overview of the content-addressable network D2B. In Proceedings of the 22nd ACM POD Conference. ACM, New York, 151.   
FRAIGNIAUD, P. AND GAURON, P. 2006. D2B: A De Bruijn based content-addressable network. Theor. Comput. Sci. 355, 1, 65–79.   
GAI, A. T. AND VIENNOT, L. 2004. Broose: A practical distributed hashtable based on the De Bruijn topology. In Proceedings of the International Conference on Peer-to-Peer. 167–174.   
GUO, D., LIU, Y., AND LI, X. 2008. BAKE: A balanced Kautz tree structure for peer-to-peer networks. In Proceedings of the 27th IEEE INFOCOM. IEEE, Los Alamitos, CA.   
GUO, D., WU, J., CHEN, H., AND LUO, X. 2007. Moore: An extendable peer-to-peer network based on incomplete Kautz digraph with constant degree. In Proceedings of the 26th IEEE INFOCOM. IEEE, Los Alamitos, CA, 821.   
GUO, D., WU, J., LIU, Y., JIN, H., CHEN, H., AND CHEN, T. 2011. Quasi-Kautz digraphs for peer-to-peer networks. IEEE Trans. Parallel Distrib. Syst. 22, 6, 1042–1055.   
HARVEY, N. J. A., JONES, M. B., SAROIU, S., THEIMER, M., AND WOLMAN, A. 2003. Skipnet: A scalable overlay network with practical locality properties. In Proceedings of the. 4th USENIX Symposium on Internet Technologies and Systems.   
IMASE, M. AND ITOH, M. 1981. Design to minimize diameter on building-block network. IEEE Trans. Computers 30, 6, 439–442.   
IMASE, M. AND ITOH, M. 1983. A design for directed graphs with minimize diameter. IEEE Trans. Computers 32, 8, 782–784.   
KAASHOEK, F. AND KARGER, D. 2003. Koorde: A simple degreeoptimal distributed hash table. In Proceedings of the International Peer-to-Peer Symposium. 98–107.   
KOPONEN, T., CASADO, M., GUDE, N., STRIBLING, J., POUTIEVSKI, L., ZHU, M., RAMANATHAN, R., IWATA, Y., INOUE, H., HAMA, T., AND SHENKER, S. 2010. Onix: A distributed control platform for large-scale production networks. In Proceedings of the 9th USENIX OSDI. 351–364.

LAKSHMAN, A. AND MALIK, P. 2010. Cassandra: A decentralized structured storage system. Oper. Syst. Rev. 44, 2, 35–40.   
LI, D., LU, X., AND WU, J. 2005. Fissione: A scalable constant degree and low congestion dht scheme based on Kautz graphs. In Proceedings of the IEEE INFOCOM, IEEE, Los Alamitos, CA, 1677–1688.   
LOGUINOV, D., CASAS, J., AND WANG, X. 2005. Graph-theoretic analysis of structured peer-to-peer systems: Routing distances and fault resilience. IEEE/ACM Trans. Networks 13, 5, 1107–1120.   
MALKHI, D., NAOR, M., AND RATAJCZAK, D. 2002. Viceroy: A scalable and dynamic emulation of the butterfly. In Proceedings of the 21st ACM PODC. ACM, New York, 183–192.   
MAYMOUNKOV, P. AND MAZIERES, D. 2002. Kademlia: A peer-to-peer information system based on the XOR metric. In Proceedings of the International Peer-to-Peer Symposium. 53–65.   
MILLER, M. AND SIRAN, J. 2005. Moore graphs and beyond: A survey of the degree/diameter problem. Electron. J. Combinatorics 61, 1–63.   
NAOR, M. AND WIEDER, U. 2003. Novel architecture for P2P applications: The continuous-discrete approach. In Proceedings of the ACM Symposium on Parallel Algorithms and Architectures. ACM, New York, 50–59.   
PANCHAPAKESAN, G. AND SENGUPTA, A. 1999. On a lightwave networks topology using Kautz digraphs. IEEE Computer 48, 10, 1131–1138.   
RATNASAMY, S., FRANCIS, P., HANDLEY, M., KARP, R., AND SHENKER, S. 2001a. A scalable content addressable network. In Proceedings of the ACM SIGCOMM. ACM, New York, 161–172.   
RATNASAMY, S., FRANCIS, P., HANDLEY, M., KARP, R. M., AND SHENKER, S. 2001b. A scalable content-addressable network. In Proceedings of the ACM SIGCOMM. ACM, New York, 161–172.   
ROWSTRON, A. AND DRUSCHEL, P. 2001. Pastry: Scalable, decentralized object location, and routing for largescale peer-to-peer systems. Lecture Notes in Computer Science, Vol. 2218, Springer, Berlin, 329–350.   
SCHLOSSER, M. T., SINTEK, M., DECKER, S., AND NEJDL, W. 2002. Hypercup - hypercubes, ontologies, and efficient search on peer-to-peer networks. In Proceedings of the 1th International Workshop on Agents and Peerto-Peer Computing. 112–124.   
SHEN, H., XU, C., AND CHEN, G. 2004. Cycloid: A constant-degree and lookup-efficient P2P overlay network. In Proceedings of. the 18th International Parallel and Distributed Processing Symposium.   
SIVARAJAN, K. N. AND RAMASWAMI, R. 1994. Lightwave networks based on De Bruijn graphs. IEEE/ACM Trans. Netw. 2, 1, 70–79.   
STOICA, I., MORRIS, R., KARGER, D. R., KAASHOEK, M. F., AND BALAKRISHNAN, H. 2003. Chord: A scalable peer-topeer lookup service for internet applications. IEEE/ACM Trans. Netw. 11, 1, 17–32.   
TVRDIK, P. 1994. Partial Kautz line digraphs with maximal connectivity. Tech. rep. 94-15, LIP ENSL, Lyon, France.   
XU J. 2001. Topological Structure and Analysis of Interconnection Networks. Kluwer, Amsterdam.   
XU, J., KUMAR, A., AND YU, X. X. 2004. On the fundamental tradeoffs between routing table size and network diameter in peer-to-peer networks. IEEE J. Sel. Areas Comm. 22, 1, 151–163.   
ZHAO, B. Y., KUBIATOWICZ, J., AND JOSEPH, A. D. 2002. Tapestry: A fault-tolerant wide-area application infrastructure. Comput. Comm. Rev. 32, 1, 81.

Received October 2011; accepted April 2012