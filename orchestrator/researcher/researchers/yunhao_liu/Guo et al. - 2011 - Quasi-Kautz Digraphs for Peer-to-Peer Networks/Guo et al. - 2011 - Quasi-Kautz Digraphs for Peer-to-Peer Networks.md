# Quasi-Kautz Digraphs for Peer-to-Peer Networks

Deke Guo, Member, IEEE, Jie Wu, Fellow, IEEE, Yunhao Liu, Senior Member, IEEE, Hai Jin, Senior Member, IEEE, Hanhua Chen, Member, IEEE, and Tao Chen, Member, IEEE

Abstract—The topological properties of peer-to-peer overlay networks are critical factors that dominate the performance of these systems. Several nonconstant and constant degree interconnection networks have been used as topologies of many peer-to-peer networks. The Kautz digraph is one of these topologies that have many desirable properties. Unlike interconnection networks, peer-topeer networks need a topology with an arbitrary order and degree, but the Kautz digraph does not possess these properties. In this paper, we propose MOORE: the first effective and practical peer-to-peer network based on the quasi-Kautz digraph with Oðlogd nÞ diameter and constant degree under a dynamic environment. The diameter and average routing path length, respectively, are shorter than that of CAN, butterfly, and cube-connected cycle, and are close to that of the de Bruijn and Kautz digraphs. The message cost of node joining and departing operations are at most 2:5d logd n and $( 2 . 5 d + 1 ) \log _ { d } n$ , and only d and 2d nodes need to update their routing tables. MOORE can achieve optimal diameter, high performance, good connectivity, and low congestion, evaluated by formal proofs and simulations.

Index Terms—Constant degree networks, Kautz digraphs, peer-to-peer networks.

# 1 INTRODUCTION

TRUCTURED peer-to-peer (P2P) networks have emerged as Sa good candidate infrastructure for building novel largescale and robust network applications [1], [2], [3], [4], [5], [6] in which participating peers share resources as equals. They impose a certain topology structure on the overlay network and control the placement of data, thus exhibiting several unique properties that unstructured P2P networks lack. In general, the topological properties of structured P2P networks are critical factors that dominate the performance of these systems. The most common concerns about topological properties are peer degree and network diameter. The degree of a peer denotes the number of overlay connections attached to it. The diameter indicates the largest number of hops that must be traversed in order to transmit a message between any two peers in the worst case.

Several nonconstant and constant degree interconnection networks have been used as the ideal topology of structured

D. Guo is with the School of Computer Science and Technology, Huazhong University of Science and Technology, Wuhan 430074, P.R. China, and the Key laboratory of Information System Engineering, School of Information System and Management, National University of Defense Technology, Changsha 410073, P.R. China. E-mail: guodeke@gmail.com.   
. J. Wu is with the Department of Computer and Information Sciences, Temple University, 1805 N. Borad Street, Philadelphia, PA 19122. E-mail: jiewu@temple.edu.   
. Y. Liu is with the Computer Science Department, Hong Kong University of Science and Technology, Hong Kong, P.R. China. E-mail: liu@cse.ust.hk.   
. H. Jin and H. Chen are with the School of Computer Science and Technology, Huazhong University of Science and Technology, Wuhan 430074, P.R. China. E-mail: {hjin,chenhanhua}@hust.edu.cn.   
. T. Chen is with the Key Laboratory of Information System Engineering, School of Information System and Management, National University of Defense Technology, Changsha 410073, P.R. China. E-mail: emilchenn@gmail.com.

Manuscript received 25 Mar. 2010; revised 22 June 2010; accepted 28 June 2010; published online 24 Aug. 2010.

Recommended for acceptance by M. Parashar. For information on obtaining reprints of this article, please send e-mail to: tpds@computer.org, and reference IEEECS Log Number TPDS-2010-03-0176. Digital Object Identifier no. 10.1109/TPDS.2010.161.

P2P networks. The degree and diameter increase logarithmically with respect to the order of the network for nonconstant degree interconnection networks, such as hypercube [7] and ring digraph. The diameter increases logarithmically with respect to the order of the network, whereas the degree of each node remains fixed, regardless of the order of the network, for constant degree interconnection networks, such as cube-connected cycle [8] (CCC), butterfly [5], d-dimensional torus [7], de Bruijn [9], and Kautz digraph [10]. Among existing structured P2P networks, Chord [2], Pastry [3], Tapestry [11], and Kademlia [4] are based on the hypercube topology; Viceroy [5] and Ulysses [12] are based on the butterfly topology [13]; Cycloid [14] is based on the CCC topology; CAN [1] is based on the d-dimensional torus topology; Koorde [6], Distance Halving [15], D2B [16], ODRI [17], and Broose [18] are based on the de Bruijn topology; and FissionE [19] is based on the Kautz topology.

The degree of a node in the Butterfly network is four, whereas that in Ulysses is Oðlog nÞ. The degree of a node in Viceroy or Cycloid is seven and cannot be a general constant integer. The expected degree of a node in D2B is constant, but its high probability bound is Oðlog nÞ, i.e., some peers would be of degree Oðlog nÞ. Koorde and distance-halving embed a de Bruijn network on a ring and employ equivalent connection rules. The only difference is that the node degree of distance-halving must be two, whereas that of Koorde can be an arbitrary integer. ODRI is another scheme based on the de Bruijn network, whereas the details are still under investigation. Broose is a de Bruijn version of Kademlia that was proposed to increase the reliability of de-Bruijn-based structured P2P networks. Among the known structured P2P networks, only the degree of a node in CAN and Koorde definitely remains fixed and can be an arbitrary integer.

In the design of structured P2P networks, there are two important requirements. First, P2P networks always pursue a topology with arbitrary order and degree in order to deal with the uncontrolled dynamic operations of nodes, such as joining, departing, and failing. Second, P2P networks attempt to design a topology with the smallest diameter given n nodes and fixed degree d since reducing the diameter can improve the performance of structured P2P networks due to the following fact. The P2P networks are overlay networks in which one hop transmission usually traverses many links and devices in the underlying physical networks, and consequently, has nontrivial overhead of delay and traffic.

It is well known that constant degree interconnection networks can satisfy the second requirement, and the Kautz digraph obtains the smallest diameter compared to others. The reason is that the Kautz digraph almost achieves the Moore bound [20], the order n of a digraph with maximum out-degree d and diameter D meets the constraint: $n \leq$ $( d ^ { D + 1 } - 1 ) / ( d - 1 )$ (with more details in Section 2). Unfortunately, constant degree interconnection networks impose an inherent constraint on the number of vertices they can support. For example, the order of a Kautz digraph must be $\stackrel { \cdot } { d } ^ { D - 1 } ( d + 1 )$ for a given degree d and any value of diameter D. In other words, it can be one of a series of discrete integers, but cannot cover all possible integers. The Kautz digraph, therefore, cannot satisfy the first requirement and cannot be directly used to design a structured P2P network. Although the generalized Kautz digraph extends the Kautz digraph for a general number of vertices, it is required to reconstruct the whole topology once the number of vertices changes [21], [22]. Due to the frequent changes of peers in P2P networks, the generalized Kautz digraph is also not suitable for structured P2P networks.

In this paper, we design a quasi-Kautz digraph with an arbitrary network order and node degree which can satisfy the above two requirements and still retain the key properties of a Kautz digraph. We then propose MOORE: the first effective and practical P2P network based on the quasi-Kautz digraph with $O ( \log _ { d } n )$ diameter and constant degree under a dynamic environment. The diameter and average routing path are $\textstyle \lceil \log _ { d } \frac { n } { d + 1 } + 1 \rceil$ and $\log _ { d } n ,$ respectively. They are shorter than that of CAN, butterfly, and CCC, but close to that of the de Bruijn and Kautz digraphs. The message costs of node joining and departing operations are at most $2 . 5 d \log _ { d } n$ and $( 2 . 5 d + 1 ) \log _ { d } n ,$ respectively. MOORE can achieve optimal diameter, high performance, good connectivity, and low congestion.

The main contributions of this paper are as follows:

1. We present the definition, construction procedure, and theoretical results of a quasi-Kautz digraph with arbitrary order and node degree. It satisfies the two important requirements and retains desirable properties of a Kautz digraph, such as optimal diameter, constant out-degree, simple routing scheme, and low congestion.   
2. We design a novel structured peer-to-peer network based on the quasi-Kautz digraph, and a suitable resource distribution policy, production methods of resource and node identifier, and a shortest path routing scheme.   
3. We propose some essential algorithms to handle the dynamic operations of nodes, such as node joining and departing and network expanding and shrinking. These algorithms can preserve the desirable

![](images/d5dabf18f84af4ce903f9664845d2959a9899b9a9498092db822cea6e78c07b2.jpg)



Fig. 1. 1-factorization of a Kautz digraph Kð2; 2Þ.

structure of the backbone subnetwork and guarantee the correctness and performance of MOORE.

4. We evaluate the performance and cost of MOORE through formal analysis and simulation, and compare it with mainstream structured peer-to-peer networks based on other constant degree topologies.

The rest of this paper is organized as follows: Section 2 surveys the definition and emulation methods of the Kautz digraph. Section 3 proposes the theory of a quasi-Kautz digraph and its construction procedure. Section 4 describes the detailed design of MOORE. Section 5 presents strategies to expand and shrink the entire topology. Section 6 analyzes and evaluates the characteristics of MOORE. The conclusions and future work are discussed in Section 7.

# 2 RELATED WORK

# 2.1 Kautz Digraph

The topology of a structured P2P network is usually modeled by a graph or digraph in which vertices stand for nodes, while edges represent overlay connections. Many efforts have been made to address the degree/diameter problem, which determines the largest graphs or digraphs of given maximum degree and given diameter. The order n of a digraph with maximum out-degree d and diameter D is not larger than a general Moore bound [20], [23] as follows:

$$
n \leq d ^ {D} + d ^ {D - 1} + \dots + d ^ {2} + d + 1 = (d ^ {D + 1} - 1) / (d - 1). \tag {1}
$$

Many research activities related to the degree/diameter problem have proved that nonexistence of digraphs achieves the general upper bound for the parameters $d \geq$ 3 and $D \geq 3 ~ [ 2 4 ]$ . The best lower bound on the order of digraphs of maximum out-degree d and diameter D is as follows: For maximum out-degree $d = 2$ and diameter $D \geq 4 , n \geq 2 5 \times 2 ^ { D - 4 }$ . For the remaining values of maximum d and diameter $D ,$ a general lower bound is $n \geq$ $d ^ { D } + d ^ { D - 1 }$ [20]. Among existing nontrivial digraphs, this best lower bound is only obtained by Kautz digraphs defined using an alphabet as follows:

Definition using an alphabet. Let $Z _ { d } = \{ 0 , 1 , \ldots , d \}$ be an alphabet of $d + 1$ letters, and $Z _ { d } ^ { D } = \{ x _ { 1 } \dots x _ { D - 1 } x _ { D } | x _ { i } \in Z _ { d }$ $x _ { i } \neq x _ { i + 1 }$ and $1 \leq i < D \}$ is a Kautz identifier space consisting of all Kautz identifiers with length D and base d. The vertex set and arc set of the Kautz digraph are $Z _ { d } ^ { D }$ and

$$
E (K (d, D)) = \{\langle x _ {1} x _ {2} \dots x _ {D}, x _ {2}, \dots x _ {D} \alpha \rangle \mid \alpha \in Z _ {d}, \alpha \neq x _ {D} \}.
$$

Fig. 1 plots an example of Kautz ð2; 2Þ.

Besides the degree/diameter problem, structured P2P networks also focus on the order/degree problem, which determines the smallest diameter in a digraph of order n and maximum out-degree d. Based on the Moore bound of the degree/diameter problem, a lower bound of the order/ degree problem can be derived as

$$
D \geq \lceil \log_ {d} (n (d - 1) + 1) \rceil - 1.
$$

In practice, all existing digraphs cannot achieve this lower bound for the parameters $d \geq 3$ and $D \geq 3 ~ [ 2 4 ]$ . The best upper bound on the diameter of digraphs of maximum out-degree d and order n is $\textstyle \lceil \log _ { d } { \frac { \bar { n } } { d + 1 } } + 1 \rceil$ . Among all existing nontrivial digraphs, the best upper bound is only possessed by the Kautz digraph.

# 2.2 Emulation of Kautz Digraph

The topology is incrementally extendable if its definition allows graphs of arbitrary order and degree. According to the above definition, the Kautz digraph is not incrementally extendable.

The most related research work revolves around FISSIONE, which uses a Kautz graph $K ( 2 , D )$ as its static topology and proposes some emulation methods of $K ( 2 , D )$ to deal with the dynamic operations of nodes. It, however, cannot support Kautz digraphs with arbitrary degree, except degree 2, and suffers from poor lookup performance and weak connectivity since the degree of each peer is too small. Furthermore, the emulation methods of $\bar { K } ( 2 , D )$ are not suitable to a general Kautz graph $K ( d , D )$ , where $d > 2$ . Thus, FISSIONE is not incrementally extendable.

MOORE attains the best upper bound of the order/degree problem mentioned above. Even the order is an arbitrary value. However, it only works well under a relative static or moderately dynamic environment and suffers from low robustness in highly dynamic environments due to maintaining topology. To address these issues, we improved MOORE by introducing another structured P2P network based on a balanced Kautz tree and Kautz ring in [26]. Recently, Zhang et al. reconsidered the design problem of structured P2P networks mentioned in this work, and also employed a linear digraph to emulate the Kautz digraph [27]. They adopted a fully distributed manner to maintain the node identifier space at the cost of high overhead, while MOORE prefers centralized servers.

# 3 QUASI-KAUTZ DIGRAPH

# 3.1 Definition of Quasi-Kautz Digraph

Let $G = ( V , E )$ be a strongly connected digraph. The vertex set and arc set are denoted as $V = V ( { \bar { G } } )$ and $E = E ( G )$ , respectively. An arc from vertex u to v is denoted as $\langle u , v \rangle$ . The arc is said to be incident from vertex u and incident on vertex v. The set of vertices incident on vertex u is denoted as $\Gamma _ { G } ^ { - } ( u ) = \{ v \in V ( G ) \mid \langle v , u \rangle \in E ( G ) \}$ , and $\delta _ { G } ^ { - } ( u ) = | \Gamma _ { G } ^ { - } ( u ) |$ is the in-degree of vertex u. Similarly, the set of vertices incident from u is denoted as $\Gamma _ { G } ^ { + } ( u ) = \{ v \in V ( G ) \mid$ $\langle u , v \rangle \in E ( G ) \}$ , and $\delta _ { G } ^ { + } ( u ) = | \Gamma _ { G } ^ { + } ( u ) |$ is the out-degree of vertex u.

Given a Kautz digraph $K ( d , D )$ , we construct an arc set $E ^ { \prime } \in E ( K ( d , D ) )$ such that each vertex of $K ( d , D )$ appears as the head and tail of at least one arc of $E ^ { \prime } ,$ , where $| E ^ { \prime } | = n$ and $d ^ { D } + d ^ { D - 1 } < n < d ^ { D + 1 } + d ^ { D }$ .

Definition 1. A digraph of fixed out-degree d and order $n , I K ( d , n )$ , is a quasi-Kautz digraph if:

1. $I K ( d , n )$ has arcs of $E ^ { \prime }$ as vertices.   
2. For each arc $( u , v )$ in $E ^ { \prime } ,$ check the following: For each w in $( v , w )$ in E, $i f ( v , w ) \in E ^ { \prime } ,$ , then add an --arc from vertex $( u , v )$ to vertex ðv; wÞ in $I K ( d , n ) ;$ otherwise, select z such that $( z , w ) \in E ^ { \prime }$ , then add an -arc from vertex $( u , v )$ to vertex $( z , w )$ in $I K ( d , n )$ .

The Kautz digraphs $K ( d , D )$ and $K ( d , D + 1 )$ are called the predecessor and successor Kautz digraph of $I K ( d , n ) ,$ , respectively. According to Definition 1, each arc $\langle u , v \rangle$ in $E ^ { \prime }$ can be denoted as a vertex labeled as $u v = u _ { 1 } u _ { 2 } u _ { D } v _ { D }$ of $I K ( d , n )$ , where $u _ { 2 } u _ { 3 } \ldots u _ { D }$ equals to $v _ { 1 } v _ { 2 } \ldots v _ { D - 1 }$ . In this paper, we will not distinguish strictly between an arc of $K ( d , D )$ and its corresponding vertex in $I K ( d , n )$ . In other words, we may use $\langle u , \bar { v } \rangle$ to denote a vertex of $I K ( d , n )$ . It is clear that the out-degree of any vertex of $I K ( d , n )$ is d. Note that the method used to choose z from multiple candidates will be discussed in Section 4.1.

According to Definition 1, it is straightforward to design a quasi-Kautz digraph $I K ( d , n )$ through the following general construction procedure:

1. Discover the largest Kautz digraph $K ( d , D )$ satisfying that $d ^ { D } + d ^ { D \mp 1 } < n$ .   
2. Construct a subset $E ^ { \prime }$ of $E ( K ( d , D ) )$ Þ such that $E ^ { \prime } = n$ and the constraint on $E ^ { \prime }$ mentioned above is satisfied.   
3. Produce all vertices of $I K ( d , n )$ by presenting each arc of $E ^ { \prime }$ as a vertex. Then, establish links among vertices according to the constraint mentioned in Definition 1.

The general procedure can result in different quasi-Kautz digraphs, with the same number of vertices, due to a different arc set $E ^ { \prime } .$ . The procedure ensures that the minimum in-degree of nodes in the resulting quasi-Kautz digraph is not less than one. It alone, however, is not enough to ensure that the quasi-Kautz digraph can inherit desirable properties of the Kautz digraph. Therefore, a method for careful selection of the arc set $\mathbf { \bar { \boldsymbol { E } } ^ { \prime } }$ is necessary.

# 3.2 Construction of Quasi-Kautz Digraph

Let $G = ( V , E )$ be a strongly connected digraph. An arc a covers a vertex x if a is incident from x. An arc set $E ^ { \prime } \subset E$ is an arc-covering of G if every vertex of G is covered by at least one arc of E0 . If $| E ^ { \prime } | = | \dot { V } | , E ^ { \prime }$ is called a 1-arc-covering. If $\forall u \in V ; \delta _ { G ^ { \prime } } ^ { - } ( u ) = \delta _ { G ^ { \prime } } ^ { + } ( u ) = 1$ for $G ^ { \prime } = ( V , E ^ { \prime } )$ , then E0 is called a 1-factor of G. Hence, a 1-factor is a spanning 1-regular subdigraph and consists of cycles and possibly loops. A digraph G has a 1-factorization if its arc set can be partitioned into some arc-disjoint 1-factors. Theorem 1 proves that the Kautz digraph has a 1-factorization, which will be used to derive a special construction procedure of the quasi-Kautz digraph. Before in-depth analysis, we first introduce several definitions as follows:

Definition 2. Let Lshift denote a binary operation such that $\mathrm { L s h i f t } ( x _ { 1 } \ldots x _ { D - 1 } x _ { D } , i ) = x _ { 1 } \ldots x _ { D - 1 } x _ { D } ^ { \prime } , w h e r e 0 \leq i \leq$ $d - 1 . \quad I f \quad ( x _ { D - 1 } + i - d - 1 ) < x _ { D - 1 } < x _ { D } \quad o r$ $\begin{array} { r l } { \textit { o r } } & { { } x _ { D - 1 } > } \end{array}$ xD and $x _ { D - 1 } > x _ { D } + i ,$ , t h e n $\boldsymbol { x } _ { D } ^ { \prime } = \left( \boldsymbol { x } _ { D } + \boldsymbol { i } \right)$ mod $( d + 1 )$ . Otherwise, $x _ { D } ^ { \prime } = \left( x _ { D } + i + 1 \right)$ mod $( d + 1 )$ [25].

Definition 3. Let Rshift denote a binary operation such that $\mathrm { R s h i f t } ( x _ { 1 } x _ { 2 } \ldots x _ { D - 1 } x _ { D } , i ) = x _ { 1 } ^ { \prime } x _ { 2 } \ldots x _ { D - 1 } x _ { D } ,$ , where $0 \leq i \leq$ $d - 1 . I f x _ { 2 } + i - d - 1 < x _ { 1 } < x _ { 2 } o r x _ { 1 } > x _ { 2 } a n d x _ { 1 } - i > x _ { 2 } f$ , then $x _ { 1 } ^ { \prime } = ( x _ { 1 } - i )$ mod ðd þ 1Þ. Otherwise, $x _ { 1 } ^ { \prime } = ( x _ { 1 } - i -$ 1Þ mod $\left( d + 1 \right) [ 2 5 ]$ .

Definition 4. For any vertex $x = x _ { 1 } x _ { 2 } \ldots x _ { D }$ in $K ( d , D )$ and $0 { \leq } i { \leq } d - 1 ,$ the left k-shift operation and right k-shift operation, denoted as $\sigma _ { k } ^ { i }$ and $\sigma _ { k } ^ { - i }$ , respectively, are defined as follows:

$$
\sigma_ {1} ^ {i} (x) = \left\{ \begin{array}{l l} \operatorname{Lshift} \left(x _ {2} \dots x _ {D} x _ {1}, i\right), & \text { if } x _ {1} \neq x _ {D}, \\ \operatorname{Lshift} \left(x _ {2} \dots x _ {D} x _ {2}, i\right), & \text { if } x _ {1} = x _ {D}, \end{array} \right. \tag {2}
$$

$$
\sigma_ {k} ^ {i} = \sigma_ {k - 1} ^ {i} \left(\sigma_ {1} ^ {i}\right) \tag {3}
$$

$$
\sigma_ {1} ^ {- i} (x) = \left\{ \begin{array}{l} \operatorname{Rshift} \left(x _ {D} x _ {1} \dots x _ {D - 1}, i\right), \text {   if   } x _ {1} \neq x _ {D}, \\ \operatorname{Rshift} \left(x _ {D - 1} x _ {1} \dots x _ {D - 1}, i\right), \text {   if   } x _ {1} = x _ {D}, \end{array} \right. \tag {4}
$$

$$
\sigma_ {k} ^ {- i} = \sigma_ {k - 1} ^ {- i} \left(\sigma_ {1} ^ {- i}\right). \tag {5}
$$

For any vertex $x ,$ vertices $\sigma _ { 1 } ^ { i } ( x )$ and $\sigma _ { 1 } ^ { - i } ( x )$ are its $( i + 1 ) \mathrm { t h }$ successor and predecessor, respectively. Furthermore, $\langle x , \sigma _ { 1 } ^ { i } ( x ) \rangle$ and $\langle \sigma _ { 1 } ^ { - i } ( x ) , x \rangle$ denote its $( i + 1 ) \mathrm { t h }$ out-arc and in-arc. In fact, the $( i + 1 )$ th out-arc and in-arc of each vertex are unique under the $\boldsymbol { \sigma } _ { 1 } ^ { i }$ and $\sigma _ { 1 } ^ { - i }$ operations.

Theorem 1. The arc set $E ( K ( d , D ) )$ can be partitioned into d arc-disjoint 1-factors $F ^ { 0 } , \ldots , F ^ { d - 1 }$ under the corresponding left 1-shift operation $\sigma _ { 1 } ^ { i } ( 0 \leq i \leq d - 1 )$ . That is, $K ( d , D )$ has a 1-factorization.

Proof. Let any vertex, as the beginning point, take a walk through $\dot { K } ( d , D )$ . For each vertex x under this walk, it always walks along the $( i + 1 )$ th out-arc $\langle x , \sigma _ { 1 } ^ { i } ( x ) \rangle$ under the left 1-shift operation $\sigma _ { 1 } ^ { i }$ . The walk will meet a covered vertex after at most $d ^ { D } + \stackrel { \cdot } { d ^ { D - 1 } }$ steps. This walk will not meet any inner vertex because the $( i + 1 )$ th in-arc of each inner vertex in the walk is unique and has been used by its predecessor in this walk. Therefore, this walk will get back to the beginning vertex along its ði þ 1Þth in-arc, and finally, form a cycle.

As discussed above, each vertex of $K ( d , D )$ is covered by at least one cycle under the operation $\boldsymbol { \sigma } _ { 1 } ^ { i }$ . Let us suppose that there is a common vertex y covered by a pair of cycles under operation $\sigma _ { 1 } ^ { i }$ . It is easy to conclude that the two cycles must also cover the vertex satisfying the fact that its $( i + 1 )$ th out-arc is incident on vertex y. From the point of recursive operation, we can conclude that the two cycles are identical. Therefore, each vertex is covered by only one cycle under operation $\sigma _ { 1 \cdot } ^ { i }$ , and cycles are mutually vertex disjointed. The cycles under operation $\boldsymbol { \sigma } _ { 1 } ^ { i }$ form a spanning 1-regular subdigraph and produce a 1-factor $\dot { F } ^ { i }$ of $\bar { K } ( d , D )$ . Furthermore, for any vertex x of $K ( d , D )$ , the arc covering it is different in different 1-factors. Therefore, these 1-factors are mutually arc-disjoint, and $K ( d , D )$ has a factorization. Therefore, Theorem 1 holds. tu

As shown in Fig. 1, all arcs of a Kautz digraph $K ( 2 , 2 )$ can be partitioned into two arc-disjoint 1-factors. The Kautz digraph $K ( 2 , 2 )$ , therefore, has a 1-factorization. According to Definition 1, the corresponding arc of each vertex $x =$ $x _ { 1 } \ldots x _ { D } x _ { D + 1 }$ of a $I K ( d , n )$ is contained by a unique 1-factor in the predecessor Kautz digraph of the $I K ( d , n )$ . The identifier or label of that 1-factor can be calculated by $F ( x ) = D i s t a n c e ( \sigma _ { 1 } ^ { 0 } ( x _ { 1 } x _ { 2 } \dots x _ { D } ) , x _ { 2 } x _ { 3 } \dots x _ { D + 1 } )$ , where the function Distance is given by Algorithm 1.

Algorithm 1. Distance(y; z)

Require: y and z are different d-ary Kautz identifiers with length $D + 1 .$ .

1: if $D = 0$ then

2: $j \gets ( z _ { D + 1 } - y _ { D + 1 } )$ mod ðd þ 1Þ  1

3: else

4: if min $( y _ { D + 1 } , z _ { D + 1 } ) < y _ { D } < \operatorname* { m a x } ( y _ { D + 1 } , z _ { D + 1 } )$ then

5: $\mathbf { i f } \ z _ { D + 1 } > y _ { D + 1 }$ then

6: $j \gets z _ { D + 1 } - y _ { D + 1 } - 1$

7: else

8: $j \gets z _ { D + 1 } - y _ { D + 1 } + d + 1$

9: else

10: if zDþ1 > yDþ1 $z _ { D + 1 } > y _ { D + 1 }$

11: $j \gets z _ { D + 1 } - y _ { D + 1 }$

12: else

13: $j \gets z _ { D + 1 } - y _ { D + 1 } + d$

14: return j

According to the Definition 1 and Theorem 1, we obtain the following theorem:

Theorem 2. The quasi-Kautz digraph $I K ( d , n )$ induced by any k 1-factors of Kautzðd; DÞ is a d-regular digraph for all $1 \leq k \leq d ,$ where $n = k ( d ^ { D } + d ^ { D - 1 } )$ .

The general construction method of $I K ( d , n )$ does not propose any method for the selection of the arc set $E ^ { \prime }$ . Random selection cannot ensure that the connectivity of a quasi-Kautz digraph is close to that of its predecessive Kautz digraph. We will use the results of Theorems 1 and 2 to construct the arc set $E ^ { \prime }$ and enable the resulting $I K ( d , n )$ to achieve better connectivity. Specifically speaking, the ideal arc set $E ^ { \prime }$ and $I K ( d , n )$ can be achieved by a special construction procedure based on the 1-factorization of $K ( d , D )$ as follows:

1. In order to construct an $I K ( d , n )$ , where $k ( d ^ { D } + { \bf \Phi }$ $d ^ { D - 1 } ) \leq n \leq ( k + 1 ) ( d ^ { D } + d ^ { D - 1 } ) ,$ we start with a dregular quasi-Kautz digraph $I K ( d , d ^ { D } + d ^ { D - 1 } )$ induced by the 1-factor ${ \dot { F } } ^ { 0 }$ of $K ( d , D )$ through Algorithm 5. The $K ( d , D )$ can be achieved from an initial Kautz digraph by invoking this procedure repeatedly.   
2. We add vertices corresponding to all arcs of $k - 1$ 1- factors $F ^ { 1 } , F ^ { 2 } , \dots , F ^ { k - \hat { 1 } }$ to the d-regular digraph produced in the first step, and then, achieve a new d-regular digraph $I K \hat { ( } d , k ( d ^ { D } + d ^ { D - 1 } ) )$ by using Algorithm 3 recursively.   
3. We then add vertices corresponding to $n - k ( d ^ { D } + { }$ $d ^ { D - 1 } )$ arcs, denoted as $F ^ { k ^ { \prime } }$ , of another 1-factor $F ^ { k }$ to the new d-regular digraph by using Algorithm 3 recursively.

Note that Theorem 2 guarantees the correctness of the first step. The last step is based on proper choice of the added arcs as discussed in Section 4. In order to achieve higher connectivity, the arc selection polices must make the minimum in-degree of the final digraph as large as possible. Theorem 3 shows the low and upper bounds on the minimum in-degree of a resulting $I K ( d , \bar { n ) }$ .

Theorem 3. Given any value of n, any quasi-Kautz digraph $I K ( d , n )$ always holds that $k \leq \delta ^ { - } ( I K ( d , n ) ) \leq d ,$ where $k ( d ^ { \acute { D } } + d ^ { D - 1 } ) \acute { \leq } n \leq ( k + 1 ) ( d ^ { D } + d ^ { \acute { D - 1 } } ) a n d 1 \leq k < d .$

![](images/c9e39902be8cb5c0ca56172ee25ec39f44bedd55aa1e6e64e674b4eab76db8da.jpg)



(a)

![](images/bbc0f6075e45e3c14f62c2b8ba08819e1bee8d23366b9863c5798e412a11efff.jpg)



(b)   
Fig. 2. Two different shapes of a quasi-Kautz digraph $I K ( 2 , 9 )$ .

Proof. We know that the number of 1-factors of $K ( d , D )$ used to produce the $I K ( d , n )$ is k þ 1. For the sake of generality, we select the first k þ 1 1-factors $F ^ { 0 } , F ^ { 1 } \ldots , \bar { F ^ { k } }$ , but the result is the same for any k þ 1 1-factors. The special construction procedure can produce the needed quasi-Kautz digraph mentioned in this theorem. Theorem 2 can also guarantee that the quasi-Kautz digraph induced by any k 1-factors of $K ( d , \bar { D ) }$ is a d-regular digraph.

Adding any vertex x induced by $F ^ { k ^ { \prime } }$ has an effect on one out-arc of at most d existing nodes. Node x needs to inform its ði þ 1Þth predecessor to update the ði þ 1Þth out-arc (a  arc) with a new --out-arc incident on node x where $0 \leq i \leq k - 1$ . As a result, the in-degree of the node at the other end of the original $( i + \dot { 1 } )$ th out-arc of the ði þ 1Þth predecessor of vertex x decreases by one. If the arc corresponding to its ðk þ 1Þth predecessor has been added previously, node x also informs this predecessor to add an --arc to itself. For k $\ : + 1 \leq i \leq d - 1 \ :$ , other d  $k - 1$ predecessors of node x are induced by 1-factors $F ^ { i }$ and do not exist in $I K ( d , n )$ . There, however, exists a $\beta$ arc from a node corresponding to an arc $\langle \sigma _ { 1 } ^ { - k } ( \sigma _ { 1 } ^ { - i } ( x _ { 2 } \dots x _ { D + 1 } ) )$ ; $\sigma _ { 1 } ^ { - i } ( x _ { 2 } \dots x _ { D + 1 } ) \rangle$ to the node x if that arc is in $F ^ { k ^ { \prime } }$ .

According to the above analysis, the in-degree of vertices induced by $F ^ { k ^ { \prime } }$ is at least $k ,$ but less than $d ,$ except when $k = d - \bar { . }$ 1 and arcs of $F ^ { i }$ form cycles. The indegree of vertices induced by previous k 1-factors should not be less than d  1 and can reach d in some scenarios such as in Fig. 2b. Thus, $k \leq \delta ^ { - } ( I K ( d , n ) ) \leq d ,$ and Theorem 3 holds.

![](images/b20c2e18c53629b75ca677cd2eb3d0f0ac15f13d2c3ab07a1dc658cad413ca63.jpg)

# 4 MOORE DESIGN

We propose the following strategies to organize peers into an efficient overlay network which can guarantee the logarithmic network diameter and constant out-degree of each peer. First, each peer obtains a logical identifier from an identifier space and uses its IP address as a physical identifier. Second, each peer maintains d neighbor peers according to a topology rule. Third, any resource gets an identifier from an identifier space which contains the identifier space of peers. Resources are distributed to given peers based on the longest prefix matching rule. Based on the above three strategies, we propose a routing scheme to support different operations effectively, such as resource distribution, resource querying, and topology maintenance.

MOORE uses the quasi-Kautz digraph as its topology structure, which evolves from an initial Kautz digraph in a distributed manner. The Kautz digraph can be constructed through many mature centralized methods, so we do not consider related details in this paper. In practice, MOORE needs to deal with the following dynamic operations: topology expanding, topology shrinking, and node joining and departing. It is these operations that drive the evolution of MOORE. We will first propose essential algorithms to implement the two dynamic operations of peers in this section, and then, explain how to expand and shrink the MOORE topology corresponding to a Kautz digraph in Section 5.

# 4.1 Overview

The quasi-Kautz digraph inherits many desirable characteristics of the Kautz digraph and is more practical than the Kautz digraph because its order can be of an arbitrary order. Therefore, MOORE selects the quasi-Kautz digraph as its topology in a dynamic environment. There is an injection mapping from nodes in MOORE to vertices in a corresponding quasi-Kautz digraph. The topology of MOORE evolves from an initial Kautz digraph through dynamic operations of nodes and must always satisfy the constraints mentioned in Definition 1.

As mentioned in the latter, the ith out-neighbor of an existing node $x = x _ { 1 } x _ { 2 } \ldots x _ { D }$ is $\langle x _ { 2 } x _ { 3 } \ldots x _ { D } , \sigma _ { 1 } ^ { i } ( x _ { 2 } x _ { 3 } \ldots x _ { D } ) \rangle$ i. In practice, the ith desired out-neighbor might not appear in MOORE. In this situation, node x must select a substitute for its ith desired out-neighbor from at most d existing nodes labeled as $\langle \sigma _ { 1 } ^ { - j } ( \sigma _ { 1 } ^ { i } ( \bar { x } _ { 2 } x _ { 3 } \dots x _ { D } ) ) , \sigma _ { 1 } ^ { i } ( x _ { 2 } x _ { 3 } \dots x _ { D } ) \rangle$ , where $0 \leq j < d .$ Recall that Definition 1 does not point out a method to choose the substitute from multiple existing candidates. To deal with this issuenode as a substitute labeled as $\sigma _ { 1 } ^ { - F ( x ) } ( \sigma _ { 1 } ^ { i } ( x _ { 2 } x _ { 3 } \dots x _ { D } ) )$ e ; $\sigma _ { 1 } ^ { i } \left( x _ { 2 } x _ { 3 } \dots x _ { D } \right) \rangle$ i if it exists. Otherwise, MOORE chooses one randomly from those candidates.

For any resource to be distributed in MOORE, it is assigned a long d-ary identifier $x = x _ { l } x _ { 2 } \ldots x _ { l }$ according to its value of single- or multiple-dimension attributes. We use two Kautz identifier spaces $Z _ { d } ^ { l } = \left\{ x _ { 1 } \ldots x _ { l - 1 } x _ { l } | x _ { i } \in \right.$ $\{ 0 , 1 , \ldots , d - 1 \} \}$ and $Z _ { d } ^ { m }$ as the resources identifier space and nodes identifier space of MOORE. The length of a resource identifier should be larger than that of a node nfer th, where $m = \lceil \log _ { d } ^ { n _ { n } ^ { \cup } } - \log _ { d } ^ { ( 1 + 1 / d ) } \rceil$ ð1þ1=dÞ and ximu $l = \lceil \log _ { d } ^ { n _ { r } } -$ $\log _ { d } ^ { ( 1 + 1 / d ) } ]$ $n _ { n }$

Assume that the successor Kautz digraph of $I K ( d , n )$ is $K ( d , D )$ , a resource labeled as $x _ { 1 } x _ { 2 } \ldots x _ { D } \ldots x _ { l }$ is stored and maintained by its preferred host labeled as $x _ { 1 } x _ { 2 } \dots x _ { D }$ if this node exists in $I K ( d , n )$ . Otherwise, the resource will be taken over by its second host labeled as $\langle x _ { 1 } x _ { 2 } \dots x _ { D } .$ 1; $\sigma _ { 1 } ^ { s } ( x _ { 1 } x _ { 2 } \dots x _ { D - 1 } ) \rangle$ in $I K ( d , n )$ . In the remainder of this paper, let s denote the identifier of the 1-factor that was selected to induce the quasi-Kautz digraph with the same order as $K ( d , D - 1 )$ Þ. MOORE can ensure that at least the second host of each resource appears in MOORE. In general, the default value of s is 0, and the second host of resource x is labeled as $x _ { 1 } x _ { 2 } \ldots x _ { D - 1 } x _ { 1 } ( \mathrm { i f } x _ { 1 } \ne x _ { D - 1 } )$ or $x _ { 1 } x _ { 2 } \ldots x _ { D - 1 } x _ { 1 } { + } 1 \ ( \mathrm { i f } \ x _ { 1 } = x _ { D - 1 } )$ . For example, it is the node

210 that stores a resource labeled as 212120212 when the node 212 does not appear in MOORE, as shown in Fig. 2.

# 4.2 Mapping Resources onto Resources’ Identifier Space

Each resource accessible through MOORE will receive an identifier from the identifier space $Z _ { d } ^ { l } .$ Different resources are allowed to receive the same identifier. The mapping of resources onto $Z _ { d } ^ { l }$ can be implemented in several ways. Literature [19] proposed a determinate algorithm to generate an identifier with two as a base for each resource. In reality, the base of a quasi-Kautz digraph used by MOORE is often larger than two for the sake of decreasing its diameter and improving its connectivity. Therefore, this paper considers another Kautz hash algorithm to generate an identifier with any base for each resource. The Kautz hash uses three parameters: key denotes the original identifier of the resource, such as name or keyword; d and l denote the base and length of expected Kautz strings, respectively. Kautz hash is detailed below.

First of all, it produces a long binary string by hashing the key according to a given consistent hash function, for example, $S H A - 1$ . Then, it converts the resulting binary string to a new string $S _ { 0 }$ with base d and substitutes all substrings consisting of any identical number with a single one. If the length of $S _ { 0 }$ is less than $l ,$ it appends $i = 1$ to key and achieves a new Kautz string $S _ { i }$ with base $d ,$ and then, appends $S _ { i }$ to $S _ { 0 } .$ If the length of $S _ { 0 }$ is still less than $l ,$ it appends the value of $i + 1$ to key and repeats the procedure again until the length of $S _ { 0 }$ becomes larger than l. Finally, the substring consisting of the first l numbers of $S _ { 0 }$ from left to right is returned as the identifier.

# 4.3 Mapping Nodes onto Nodes’ Identifier Space

In practice, MOORE starts with $d ^ { m _ { 0 } } + d ^ { m _ { 0 } - 1 }$ initial nodes and forms a structured P2P network according to a Kautz digraph $K ( d , m _ { 0 } )$ , then enlarges or shortens its scale through a series of dynamic operations at runtime. Thus, the nodes’ identifier space should not be a static one compared to the resources’ identifier space. It will be better if we start with an initial identifier space, and then, enlarge or shorten it with the increase or decrease of the number of nodes, respectively. Let $Z _ { d } ^ { m _ { 0 } }$ denote the initial identifier space, where $m _ { 0 } < m$ . Each identifier of this space will be allocated to a unique node. If all identifiers of $Z _ { d } ^ { m _ { 0 } }$ were allocated and new nodes apply to participate in MOORE, the initial identifier space should be extended to $Z _ { d } ^ { m _ { 0 } + 1 }$ so as to allocate free identifiers to new nodes. Note that the new identifier space is a d multiple of the old one and can be achieved according to Definition 1.

As a direct result of this operation, the original identifiers of initial nodes also need to be updated by the first $d ^ { m _ { 0 } } +$ $d ^ { m _ { 0 } - 1 }$ new identifiers induced by the 1-factor $F ^ { 0 }$ of $K ( d , m _ { 0 } )$ , then the initial nodes form another d-regular quasi-Kautz digraph $I K ( d , d ^ { m _ { 0 } } + d ^ { m _ { 0 } - 1 } )$ according to Algorithm 5. As discussed later, this process does not cause additional overhead except $d ^ { m _ { 0 } } + { \bf \bar { \it d } } ^ { m _ { 0 } - 1 }$ messages to start the process. In order to maintain better topological properties under a dynamic environment, we must focus on the policy used to allocate identifiers to new nodes, and this policy is equivalent to the arc choice policy used by the special construction procedure of the quasi-Kautz digraph mentioned above. Any arc choice policy first takes the arcs of the second 1-factor $\dot { F } ^ { 1 } .$ , then takes the arcs of the third 1-factor $F ^ { 2 } ,$ , and so on. But, existing policies are different in the selection order of arcs in each 1-factor.

The arc choice policy proposed in literature [25] suggests to take arcs of one cycle in each 1-factor, then arcs of another cycle, and so on. The random choice policy, denoted as factorRandom, selects arcs randomly from a given 1-factor. The difference between these two policies is that the former can make the in-degree of more new vertices reach k þ 1. The n denotes the number of existing nodes in MOORE, and k satisfies that $k ( d ^ { m _ { 0 } } + d ^ { m _ { 0 } - 1 } ) \leq n \leq ( k + 1 ) ( d ^ { m _ { 0 } } + d ^ { m _ { 0 } - 1 } )$ . We propose an enhanced policy, denoted as cycleSequence, which takes arcs of one cycle along its direction continuously, then the second cycle, and so on. Our new policy can make more vertices reach $k + 1$ in-degree than the policy proposed in literature [25]. The reason is that the $( k + \bar { 1 } )$ Þth predecessor of a newly added arc has been added previously unless it is the first selected arc of a cycle.

# Algorithm 2. Route $( y ,$ message, scheme)

Require: Identifier $y$ is not less than x

1: $z \gets y$   
2: if the length of y is larger than D then   
3: $y  y _ { 1 } y _ { 2 } \dotsc y _ { D }$   
4: if $x = y \mathrm { o r } x _ { 1 } x _ { 2 } \dots x _ { D - 1 } = y _ { 1 } y _ { 2 } \dots y _ { D - 1 }$ then   
5: Process the message locally, and return success.   
6: $x ^ { \prime } \gets$ forward orientationðyÞ   
7: if $x ^ { \prime } \neq$ null then   
8: return x0 :Routeðz; message; schemeÞ   
9: else

10: return failure to the source node.

# forward\_orientation(y)

1: Let u be the largest integer such that $x _ { D - u + i } = y _ { i }$ for $1 \leq i \leq u ,$ and result null   
2: for $i = 0$ to d do   
3: w routingtalbe½i:identifier   
4: if $u = 0$ and $w = y$ then   
5: return w   
6: else if $w _ { D - u - 1 + i } = y _ { i }$ for $1 \leq i \leq u + 1$ then   
7: result w   
8: if result ¼ null and scheme ¼ resource then   
9: return $\langle x _ { 1 } x _ { 2 } \dots x _ { D - 1 } , \sigma _ { 1 } ^ { s } ( x _ { 1 } x _ { 2 } \dots x _ { D - 1 } ) \rangle$   
11: return result

# 10: else

Recall that the in-degree of at most k nodes induced by previous k 1-factors decreases by one once a new node x joins MOORE. Here, the $( k + 1 )$ th out-arc of existing peer $\sigma _ { 1 } ^ { - i } ( x )$ incidents on one of those k nodes, where $0 \leq i \leq k - 1$ . As shown in Fig. 2a, the original -out-arc from vertex 012 to 021 will be updated with an --out-arc from vertex 012 to 121 once a vertex 121 participates $I K ( d , n )$ . Thus, the in-degree of vertex 021 decreases by one. No existing arc choice policies focus on this problem. Therefore, we propose a different policy denoted as inDegreePreserved to deal with it. The basic idea is to allocate the identifier of the ðk þ 1Þth predecessor of existing nodes, once their ðk þ 1Þth in-arc is canceled by the previous node’s adding operation, and reestablish its $( k + 1 ) \operatorname { t h }$ in-arc with an --arc incident from its ðk þ 1Þth predecessor. This policy tries to preserve the in-degree regularity of nodes induced by previous k 1-factors and is very efficient if $k = d - 1 \mathrm { o r } d = 2 .$ . Thus, MOORE can achieve the best topological properties if it combines the policies inDegreePreserved and cycleSequence.

On the other hand, an identifier allocated to a node may become free if the node failed or departed from the network and did not recover during a given time interval. All arc choice policies should give these kinds of identifiers priority when they allocate an identifier to a new node. If this identifier is induced by previous $F ^ { i }$ for $0 \leq i \leq k - 1$ , this operation is helpful to preserve the desirable structure of the backbone subnetwork consisting of nodes induced by previous k 1-factors. Otherwise, this operation can make the in-degree of more nodes reach k þ 1 for the cycleSequence policy.

# 4.4 Routing Scheme

In order to route messages to destinations correctly, each node x must establish links with selected neighbors and construct a routing table when it joins MOORE using Algorithm 3. In addition, each node should update its links and routing table when other nodes join, depart, or fail. The routing table consists of d entries, and each entry includes the identifier and address (such as IP and port number) of one neighbor node. Furthermore, node x may initiate a lookup message to find a given resource or node with identifier y or initiate an insert message to distribute its resource with identifier y to a responsible node. We propose Algorithm 2 to route these kinds of messages to their destinations along the shortest paths.

Algorithm 3. Node joins (x,y,k)   
1: $k \leftarrow F(x)$ 2: for i = 0 to d
3: if $i \leq k$ then
4: Node y finds the address of node labeled z. Then node x adds $\langle z, address, \alpha \rangle$ as its $(i + 1)^{th}$ routing entry, and establishes a link to this node, where $z = \langle x_2 x_3 \ldots x_{D+1}, \sigma_1^i(x_2 x_3 \ldots x_{D+1}) \rangle$ ,
5: else
6: Node x asks node y to find the address of node z labeled $\langle \sigma_1^{-k}(\sigma_1^i(x_2 x_3 \ldots x_{D+1})), \sigma_1^i(x_2 x_3 \ldots x_{D+1}) \rangle$ 7: if node z does not exist then
8: Node x asks node y to find the address of a node z labeled $\langle \sigma_1^{-j}(\sigma_1^i(x_2 x_3 \ldots x_{D+1})), \sigma_1^i(x_2 x_3 \ldots x_{D+1}) \rangle$ . The random integer j satisfies that $0 \leq j < k$ and node z exists.
9: Node x adds $\langle z, address, \beta \rangle$ as the $(i + 1)^{th}$ entry of its routing table, and establishes a link to node z.
10: for i = 0 to d do
11: if $i \leq k$ then
12: $w \leftarrow \langle \sigma_1^{-i}(x_1 x_2 \ldots x_D), x_1 x_2 \ldots x_D \rangle$ 13: else
14: $w \leftarrow \langle \sigma_1^{-k}(\sigma_1^{-i}(x_2 \ldots x_{D+1})), \sigma_1^{-i}(x_2 \ldots x_{D+1})$ 15: Node w updates one original $\beta$ link with an $\alpha$ or $\beta$ link incident on node x, then updates its routing table.
16: Node x gets resources satisfied that x is their prefix of identifier from node $\langle x_1 x_2 \ldots x_D, \sigma_1^s(x_1 x_2 \ldots x_D) \rangle$ .

Fiol proposed a method to achieve a short path from x to y in [28]: find the largest suffix u of x that coincides with a prefix of y, then walk toward a neighbor z of x such that its largest suffix v coincides with a prefix of y and the length of v is larger than that of u. Note that the exhibited path does not necessarily have the shortest length due to the existence of -out-arcs. As an example, node 021 needs to route to node 012 along the short path $0 2 1  2 1 0  1 0 1  0 1 2 , \quad$ as shown in Fig. 2a. The shortest path, however, should be $0 2 1  0 1 2 ,$ resulting from a -out-arc incident from node 021. In order to deal with this problem, Algorithm 2 will check whether there is a routing entry corresponding to node y if the length of u is zero. As shown in our simulation results, Algorithm 2 can achieve low congestion as the longpath routing scheme does [10], [19].

Algorithm 2 uses three parameters: y denotes the identifier of a aimed resource or node; message denotes the real message needed to be routed; and scheme denotes the type of message and can be resource (lookup or insert resource) or node (find the address of node). Recall that the resource distribution policy of the quasi-Kautz digraph is different from that of the Kautz digraph because any resource has two possible exclusive destination nodes. Therefore, if scheme ¼ resource and the method forward\_orientation in Algorithm 2 does not find the node whose identifier is a prefix of the identifier of an aimed resource, it will forward the message to another destination node defined by the resource distribution policy mentioned above.

# 4.5 Node Joining

To ensure that our routing scheme executes correctly after a new peer participates MOORE, all routing entries of each peer must keep up to date. MOORE handles this issue by a series of local operations that each new peer runs when it joins. The joining procedure includes receiving a node identifier, redistributing resources, and updating routing tables. These operations can be implemented by Algorithm 3.

As for most P2P networks, we assume that there are some existing nodes as entry points of MOORE, which can receive and process the node joining message. Let $y = y _ { 1 } y _ { 2 } \dots y _ { D + 1 }$ denote an entry point of MOORE. Before participating MOORE, a new peer consults node y for its logical identifier $x = x _ { 1 } x _ { 2 } \ldots x _ { D + 1 }$ and the identifier k of a current 1-factor according to the management policy of nodes’ identifier space. In reality, there exist at least two cases of node joining operations. The first case is $F ( x ) = k ,$ , which means that the new node belongs to the current 1-factor $F ^ { k }$ . The second case is $F ( x ) < k ,$ which means that the new node belongs to the previous 1-factor and a node with the same identifier has joined MOORE, but failed or departed.

In both cases, node x needs to find its successors for establishing out-links and a routing table, then inform at most d existing predecessors to update their links and routing tables, and finally, take over its responsible resources from an existing node. The details have been proposed when proving Theorem 3. Given an integer k such that $k ( d ^ { D } + d ^ { D - 1 } ) \leq n \leq ( k + 1 ) ( d ^ { D } + d ^ { D - 1 } )$ , we know that the ði þ 1Þth predecessor and successor of node x exist for $0 \leq i \leq k - 1$ . Furthermore, its ðk þ 1Þth successor does not exist except that node x is mapped to the last arc of the current cycle, and its ðk þ 1Þth predecessor exists except that node x is mapped to the first arc selected from a cycle.

![](images/94edd2753f31a9fde39c5290bb052af87ca9bbc84702bc535334397cc71bb6b7.jpg)



(a)

![](images/7cafc7c86a18ff31d6b13f69c4ef255bb35e2c7cec60fac3db41a109de253308.jpg)



(b)   
Fig. 3. The topology of MOORE before and after adding a peer 121.

The other jth successor of node x does not exist for $k + 1 < j \leq d ,$ , and it needs to find a substitute from nodes belonging to 1-factor $F ^ { k } ,$ , even from nodes belonging to previous 1-factors, in order to keep a constant out-degree. The other jth predecessors of node x also do not exist for $k + 1 < j \leq d .$ . Therefore, node x should find a substitute for its jth predecessor for $k + 1 < j \leq d$ from nodes belonging to 1-factor $F ^ { k }$ . Node x, however, does not select substitutes for predecessors from nodes belonging to previous 1-factors in order to not increase the in-degree of nodes belonging to previous 1-factors.

The resulting topology of MOORE after adding a new node can be represented pictorially and an example is illustrated in Fig. 3. If a node 121 joins MOORE, whose topology is shown in Fig. 3a, the resulting topology of MOORE is plotted by Fig. 3b.

# 4.6 Node Departing

The correctness and effectiveness of MOORE rely on the fact that predecessors and successors of each node are up to date. An incorrect neighbor might increase the delay of routing a message, and even fail to deliver messages correctly. Therefore, a node departing voluntarily should repair the topology through the following procedures before it leaves:

Let $x = x _ { 1 } x _ { 2 } \ldots x _ { D + 1 }$ denote a node departing from MOORE, and k denote the identifier of the current 1-factor. In practice, there exist at least two cases of node departing operations. The first case is $F ( x ) = k ,$ which means that node x belongs to the current 1-factor $F ^ { k } . F ( x ) < k$ is another case, which means that node x belongs to the previous 1-factors. The node departing operation harms the topology structure and results in unsuccessful message routing. Algorithm 4 can compensate for the negative impact of the node leaving operation. For example, If node 121 departs from MOORE, whose topology is shown in Fig. 3b, the resulting topology of MOORE is plotted by Fig. 3a.

# Algorithm 4. Node departs $( x , k )$

1: if $F ( x ) k$ then   
2: $y \gets f i n d S u b s t i t u t e ( x )$   
3: update(y; k; F ðxÞ)   
4: Node x transfers its resources and routing table to node $y ,$ then departs from MOORE. Node y updates its identifier, routing table, and links with that of node $x ,$ and informs in-neighbors about its change of address.   
5: else

6: Node x transfers its resources to node corresponding to arc $\left. y _ { 1 } y _ { 2 } \dots y _ { m - 1 } , \sigma _ { 1 } ^ { s } ( y _ { 1 } y _ { 2 } \dots y _ { m - 1 } ) \right.$ before departing.

7: update(x; k; F ðxÞ)

# update(z; k; l)

1: for $i = 0$ to d do   
2: if $i < k$ then   
3: $w \gets \langle \sigma _ { 1 } ^ { - i } ( z _ { 1 } z _ { 2 } \dots z _ { D } ) , z _ { 1 } z _ { 2 } \dots z _ { D } \rangle$   
4: Informs node w to update the link to node x with a new $\beta$ link to node $\langle \sigma _ { 1 } ^ { - i } ( z _ { 2 } z _ { 3 } \ldots z _ { D + 1 } ) , z _ { 2 } z _ { 3 } \ldots z _ { D + 1 } \rangle$ .

5: else

6: $w  \langle \sigma _ { 1 } ^ { - l } ( \sigma _ { 1 } ^ { - i } ( z _ { 2 } \ldots z _ { D + 1 } ) ) , \sigma _ { 1 } ^ { - i } ( z _ { 2 } \ldots z _ { D + 1 } ) \rangle$

7: Informs node w to update the link to node x with a new $\beta$ link to node $\langle \sigma _ { 1 } ^ { - j } ( z _ { 2 } z _ { 3 } \ldots z _ { D + 1 } ) , z _ { 2 } z _ { 3 } \ldots z _ { D + 1 } \rangle$ , where j is a random integer satisfied $0 \leq j < k$ such that the new destination node exists.

In the first case, node x needs to inform its in-neighbors to update the link incident on node x and transfers its resources to another responsible node defined by the resource distribution policy. In the second case, node x needs to find a node y to replace it and inform the in-neighbors of node y to update related links and routing entries. Then, node y takes over the identifier, resources, links, and routing table of node x; and its original identifier becomes free. Finally, node y updates its links according to the new routing table and informs its in-neighbor about the change of its address. Node y should be selected from nodes belonging to 1-factor $F ^ { k } ,$ , then 1-factor $F ^ { k - 1 }$ , and so on. This policy can preserve the desired topology of a backbone subnetwork consisting of nodes belonging to previous 1-factors.

# 5 TOPOLOGY ADJUSTMENTS

# 5.1 Problem Statements

In general, the topology of MOORE is a quasi-Kautz digraph $I K ( d , n )$ , where the number of nodes n is covered by a unique range $[ d ^ { D } + d ^ { D - 1 } , d ^ { D + 1 } + d ^ { D } )$ . In practice, the topology becomes a Kautz digraph $K ( d , D )$ , if n reaches the upper boundary of this range. In this situation, if other nodes apply to join MOORE, it needs to expand the topology to a new quasi-Kautz digraph whose order equals to the lower boundary of a new range $[ d ^ { D + 1 } + d ^ { D } , d ^ { \dot { D + } 2 } +$ $d ^ { D + 1 } )$ . If the number of nodes reaches $\stackrel { \smile } { d ^ { D + 2 } } + d ^ { D + 1 }$ , a quasi-Kautz digraph becomes a Kautz digraph and is ready to be expanded further.

It is easy to derive a quasi-Kautz digraph $I K ( d , d ^ { D + 1 } +$ $d ^ { D } )$ from its predecessive Kautz digraph $K ( d , D )$ by using Definition 1 with the 1-factor $F ^ { 0 }$ of $\check { K } ( \dot { d } , D )$ as the arc set $E ^ { \prime } .$ . To expand the topology of MOORE similarly, we propose two strategies to update logical identifier of each node and associated algorithms to update out-neighbors and routing tables of each node.

For the first strategy, each node $x = x _ { 1 } x _ { 2 } \ldots x _ { D }$ updates its logical identifier with $\langle x , \sigma _ { 1 } ^ { s } ( x ) \rangle$ such that the new identifier and the original identifier have a common prefix with length D. This strategy is also called the prefix-preserved expansion strategy. For the second strategy, each node x updates its logical identifier with $\langle \sigma _ { 1 } ^ { - s } ( x ) , x \rangle$ such that the new identifier and the original identifier have a common suffix with length D. This strategy is also called the suffix-preserved expansion strategy. For the two strategies, existing nodes form the same topology structure. As analyzed later, the two strategies, however, produce different network overhead during the topology expansion process.

The number of nodes in MOORE sometimes decreases to the lower boundary of the range $[ d ^ { D } + d ^ { D - 1 } , d ^ { D + 1 } + d ^ { D } )$ in practice. In this situation, if some existing nodes want to leave, MOORE needs to shrink its topology to its predecessive Kautz digraph. If the number of nodes in MOORE decreases to $d ^ { D - 1 } + d ^ { \dot { D } - 2 } .$ , the quasi-Kautz digraph might be shrunken further. The shrink operation can be performed by updating the logical identifier, out-neighbors, and routing table of each existing node. There are two possible strategies to update logical identifiers of existing nodes. For the prefix-preserved shrink strategy, each existing node $x =$ $x _ { 1 } x _ { 2 } \ldots x _ { D - 1 } x _ { D }$ updates its original logical identifier with $x _ { 1 } x _ { 2 } \ldots x _ { D - 1 }$ such that the new and original identifiers have a common prefix with length $D - 1$ . For the suffix-preserved shrink strategy, each node x updates its logical identifier with $x _ { 2 } x _ { 3 } \ldots x _ { D }$ .

# 5.2 Prefix-Preserved Adjustment Strategy

The prefix-preserved expansion strategy can be implemented by Algorithm 5. The parameter s in this algorithm denotes the identifier of the 1-factor that was selected to induce the quasi-Kautz digraph with the same order as $K ( d , D )$ , where the default value of s is 0. For each node $x = x _ { 1 } x _ { 2 } \ldots x _ { D } ,$ it constructs a temporary routing table by the following operations:

1. Updates its logical identifier with $\langle x , \sigma _ { 1 } ^ { s } ( x ) \rangle$ .   
2. Updates the logical identifier of its $( s + 1 ) ^ { t h }$ outneighbor node $\sigma ^ { s } ( x )$ with $\langle \sigma _ { 1 } ^ { s } ( x ) , \sigma _ { 2 } ^ { s } ( x ) \rangle$ .   
3. Updates the logical identifier of its $( i + 1 )$ th outneighbor node $\sigma ^ { i } ( x )$ with $\langle \sigma _ { 1 } ^ { - s } ( \sigma _ { 1 } ^ { i } ( \sigma _ { 1 } ^ { s } ( x ) ) , \sigma _ { 1 } ^ { i } ( \sigma _ { 1 } ^ { s } ( x ) ) \rangle$ , where $0 \leq i < d$ and $i \neq s .$   
4. Discovers the address of a node which updates its logical identifier $\sigma _ { 1 } ^ { - s } ( \sigma _ { 1 } ^ { i } ( \sigma _ { 1 } ^ { s } ( x ) )$ with $\langle \sigma _ { 1 } ^ { - s } \hat { ( } \sigma _ { 1 } ^ { i } ( \sigma _ { 1 } ^ { s } ( x ) )$ ; $\sigma _ { 1 } ^ { i } ( \sigma _ { 1 } ^ { s } ( x ) ) \rangle$ i, where $0 \leq i < d$ and $i \neq s$ .

# Algorithm 5. Prefix-preserved Expansion $( K ( d , D ) , s )$

Require: $K ( d , D )$ is a d-regular Kautz digraph withdiameter D.

1: for each node x labeled $x _ { 1 } x _ { 2 } \ldots x _ { D }$ in $K ( d , D )$ do   
2: x:label hx; s1ðxÞi   
3: Node x constructs a temporary routing table.   
4: for i ¼ 0 to $d - 1$ do   
5: if s ¼ i then   
6: $z = z _ { 1 } z _ { 2 } \ldots z _ { D + 1 }  \langle \sigma _ { 1 } ^ { s } ( x ) , \sigma _ { 2 } ^ { s } ( x ) \rangle$   
7: address x:routing½s:address   
8: Node x adds $\langle z , a d d r e s s , \alpha \rangle$ as the $( i + 1 ) ^ { t h }$ entry of the temporary routing table.

9: else

10: $z = z _ { 1 } z _ { 2 } \ldots z _ { D + 1 }  \langle \sigma _ { 1 } ^ { - s } ( \sigma _ { 1 } ^ { i } ( \sigma _ { 1 } ^ { s } ( x ) ) , \sigma _ { 1 } ^ { i } ( \sigma _ { 1 } ^ { s } ( x ) ) \rangle$   
11: $a d d r e s s \gets \mathrm { R o u t e } ( \sigma _ { 1 } ^ { - s } ( \sigma _ { 1 } ^ { i } ( \sigma _ { 1 } ^ { s } ( x ) ) , \mathrm { n o d e } ) )$   
12: Node x adds $\langle z , a d d r e s s , \beta \rangle$ as the $( i + 1 ) ^ { t h }$ entry of the temporary routing table.   
13: for each node x in $K ( d , D )$ do   
14: Updates its routing table with the temporary routing table, then updates links according to new routing table.

![](images/c070d373ee725117d267ec48b4fb994bb8d9c21533e81610fef545b73d85d224.jpg)



(a)

![](images/8b7b5235b8273700825900545845e6cd48de9cc7564a2bdf8dae4fd862ee767a.jpg)



(b)   
Fig. 4. The topology of MOORE before and after expanding the topology if using the prefix-preserved expansion strategy.

For $0 \leq i < d$ and $i \neq s ,$ the fresh and original $( i + 1 )$ th outneighbors of node x are not the same node, and hence, node x must discover the physical address of its new out-neighbor by initiating a query. The new $( s + 1 )$ Þth out-neighbor of node x is just the original $( s + 1 )$ Þth out-neighbor. Therefore, node x is not necessary to send a query for the physical address of its new $( s + 1 )$ Þth out-neighbor. After all existing nodes finish these operations, each of them updates its routing table with the temporary routing table, and finally, updates links according to its new routing table. As an example, Fig. 4a becomes Fig. 4b through this algorithm. Theorem 4 proves the network overhead of this type of topology expansion strategy.

Theorem 4. In the case of the prefix-preserved expansion strategy, the expansion of the entire overlay network causes $n \times ( d - 1 ) \log _ { d } n$ additional network overhead.

Proof. As mentioned above, each node must explore physical addresses of $d - 1$ neighbors by initiating $d - 1$ query messages. It is clear that each of these messages will be routed to a destination within at most $\log _ { d }$ n hops. Therefore, the total number of messages caused by expanding the overall topology is at most $n ~ \times$ $( \bar { d } - 1 ) \bar { \log _ { d } { n } } .$ . Thus, Theorem 4 holds. tu

In contrast to expanding the overlay, MOORE shrinks its topology when the number of existing nodes decreases to the order of the predecessive Kautz digraph. For the prefixpreserved shrink strategy, each node $x = x _ { 1 } x _ { 2 } \ldots x _ { D - 1 } x _ { D }$ constructs a temporary routing table by the following operations:

1. Updates its logical identifier with $x _ { 1 } x _ { 2 } \ldots x _ { D - 1 } .$   
2. Updates the logical identifier $y _ { 1 } y _ { 2 } \ldots y _ { D - 1 } y _ { D }$ of its $( i + 1 )$ Þth out-neighbor node with $y _ { 1 } y _ { 2 } \ldots y _ { D - 1 }$ where $0 \leq i < d .$ .   
3. Discovers the physical address of a node which updates its logical identifier $y _ { 1 } y _ { 2 } \ldots y _ { D - 1 } y _ { D }$ with $y _ { 1 } y _ { 2 } \dots y _ { D - 1 } .$ .

For $0 \leq i > d ,$ the new and original ði þ 1Þth neighbors of node x are not necessarily the same node. Actually, only one neighbor of node x does not change after performing the topology shrink operation. The node x therefore must discover the physical address of each new neighbor by routing a query to the node. After all existing nodes finish those operations, each of them updates its routing table with the temporary routing table, and finally, updates links according to its new routing table. As an example, Fig. 4b becomes Fig. 4a after performing this type of topology shrink operation. Theorem 5 proves the network overhead of this operation.

Theorem 5. In the case of the prefix-preserved shrink strategy, the shrink of the entire overlay network results in $n \times ( d -$ 1Þ $\log _ { d } n$ additional network overhead.

Proof. As discussed above, each node must explore physical addresses of $d - 1$ new neighbors by initiating $d - 1$ query messages. It is clear that each of these messages will be routed to a destination within at most $\log _ { d } n$ hops. Therefore, the total number of messages caused by expanding the overall topology is at most $n \times ( d - 1 )$ logd n. Thus, Theorem 5 holds. tu

# 5.3 Suffix-Preserved Adjustment Strategy

As mentioned in Theorems 4 and 5, the topology expansion and shrink operations based on the prefix-preserved strategy suffer from large network overhead. To address this problem, we adopt the suffix-preserved strategy. In this situation, the expansion of the entire topology is implemented by the following local operations at each existing node $x = x _ { 1 } x _ { 2 } \ldots x _ { D }$ in MOORE.

1. Updates its logical identifier with $\langle \sigma _ { 1 } ^ { - s } ( x ) , x \rangle$   
2. Updates the logical identifier of its $( s + 1 )$ th outneighbor node $\sigma _ { 1 } ^ { s } ( x )$ with $\langle x , \sigma _ { 1 } ^ { s } ( x ) \rangle$ .   
3. Updates the identifier of its $( i + 1 )$ th out-neighbor node $\sigma _ { 1 } ^ { i } ( x )$ with $\langle \sigma _ { 1 } ^ { - s } ( \sigma _ { 1 } ^ { i } ( x ) ) , \sigma _ { 1 } ^ { i } ( x ) \rangle$ , where $0 \leq i < i$ and $i \neq s$ .

After finishing this kind of topology expansion, resources at each node must be transferred to another node if we keep on distributing resources based on the longest prefix matching policy. To avoid costly movements of resources among nodes during the process of expanding the topology, MOORE distributes resources according to the longest suffix matching policy instead of the longest prefix matching policy.

A resource labeled as $x _ { l } \ldots x _ { D } \ldots x _ { 2 } x _ { 1 }$ is stored and maintained by its preferred host labeled as $x _ { D } \ldots x _ { 2 } x _ { 1 }$ if this node exists in MOORE. Otherwise, the resource will be taken over by its second host labeled as $\langle \sigma _ { 1 } ^ { - s } ( x _ { D - 1 } \dots x _ { 2 } x _ { 1 } )$ ; $x _ { D - 1 } \ldots x _ { 2 } x _ { 1 } \rangle$ . The topology construction and maintenance strategies ensure that at least the second host of each resource appears in MOORE. In this case, Theorem 6 shows that each resource stays at the original node after expanding the overall topology.

Theorem 6. In the case of the suffix-preserved expansion strategy, the expansion of the entire network does not cause additional network overhead, except $d ^ { D } + d ^ { D - 1 }$ messages to start the process.

Proof. In the case of MOORE based on a Kautz digraph $K ( d , D )$ , each resource $x _ { l } \ldots x _ { D } \ldots x _ { 2 } x _ { 1 }$ is hosted by its preferred node $x = x _ { D } \ldots x _ { 2 } x _ { 1 }$ . After expanding the overall topology of MOORE, node x updates its identifier with $\langle \sigma _ { 1 } ^ { - s } ( x ) , x \rangle = x _ { D + 1 } x _ { D } \dots x _ { 2 } x _ { 1 }$ . Node x is still the preferred host of resources whose identifiers have a suffix $x _ { D + 1 } x _ { D } \ldots x _ { 2 } x _ { 1 } ,$ and becomes the second host of other resources stored in it before expanding the

![](images/a7dddec85c8066204b934f73afe57e91f605abaa4a7f761016dac35658585d0a.jpg)



(a)

![](images/021f80103aba8cf2477b11b77485266a491784abf033e2f4929ddc7864a984e3.jpg)



(b)   
Fig. 5. The topology of MOORE before and after expanding the topology if using the suffix-preserved expansion strategy.

topology. Therefore, each resource stays at the original node after expanding the topology and does not introduce any overhead.

On the other hand, each node $x = x _ { D } \ldots x _ { 2 } x _ { 1 }$ maintains links to its out-neighbors $x _ { D - 1 } \ldots x _ { 1 } \alpha ,$ where $\alpha \in \{ 0 , 1 , 2 , \ldots , d \} - \{ x _ { 1 } \}$ . After expanding the topology, the node obtains a new logical identifier $\langle \sigma _ { 1 } ^ { - s } ( \bar { x } ) , x \rangle =$ $x _ { D + 1 } x _ { D } \ldots x _ { 2 } x _ { 1 }$ and maintains links to nodes $x _ { D } ^ { \prime } \ldots x _ { 2 } x _ { 1 } \beta ,$ where $\beta \in \{ 0 , 1 , 2 , \ldots , d \} - \{ x _ { 1 } \}$ and the value of $x _ { D } ^ { \prime }$ obeys to the topology construction rule of the quasi-Kautz digraph mentioned above. For $\forall \beta \in \{ 0 , 1 , \bar { 2 } , \ldots ,$ $d \} - \ \{ x _ { 1 } \}$ , the identifier of an out-neighbor $x _ { D } ^ { \prime } \ldots x _ { 2 } x _ { 1 } \beta$ of node $x _ { D + 1 } x _ { D } \ldots x _ { 2 } x _ { 1 }$ is $x _ { D - 1 } \ldots x _ { 2 } x _ { 1 } \beta$ before expanding the topology. It is clear that all out-neighbors of node $x _ { D + 1 } \ldots x _ { 2 } x _ { 1 }$ are the same out-neighbors of node $x _ { D } \ldots x _ { 2 } x _ { 1 }$ although their logical identifiers are updated.

In other words, the links maintained by each node do not change, and no network overhead is further incurred. For example, node A is labeled 21 and has out-neighbor B with identifier 12 and C with identifier 10, before expanding the entire topology, as shown in Fig. 5a. After expanding the entire topology, the identifiers of node A; B, and C are updated as 021, 012, and 210, respectively. As shown in Fig. 5b, the outneighbors of node A are still the nodes B and C. Thus, Theorem 6 holds. tu

In the case of the suffix-preserved strategy, the shrink of the entire topology is implemented by the following local operations at each existing node $x = x _ { 1 } x _ { 2 } \ldots x _ { D } \colon$

1. Updates its logical identifier with $x _ { 2 } x _ { 3 } \ldots x _ { D } .$   
2. Updates the logical identifier $y _ { 1 } y _ { 2 } \dots y _ { D }$ of its $( i + 1 ) \mathrm { t h }$ out-neighbor node with $y _ { 2 } y _ { 3 } \dots y _ { D }$ where $0 \leq i < d .$   
3. Discovers the physical address of a node which updates its logical identifier $y _ { 1 } y _ { 2 } \dots y _ { D }$ with $y _ { 2 } y _ { 3 } \dots y _ { D }$ .

After all existing nodes finish those operations, each of them updates its routing table with the temporary routing table, and finally, updates links according to its new routing table. The longest suffix matching policy of resource distribution ensures that each resource stays at the original node after shrinking the overall topology.

Theorem 7. In the case of the suffix-preserved shrink strategy, the shrink of the entire overlay network does not cause additional network overhead, except $d ^ { D } + d ^ { D - 1 }$ messages to start the process.

Proof. Each existing node $x = x _ { D } \ldots x _ { 2 } x _ { 1 }$ maintains links to its out-neighbors $x _ { D - 1 } ^ { \prime } \ldots x _ { 1 } \alpha ,$ where $\alpha \in \left\{ 0 , 1 , 2 , \ldots , d \right\} -$ $\{ x _ { 1 } \}$ and the value of $\boldsymbol { x } _ { D } ^ { \prime }$ obeys Definition 1. After shrinking the topology, the node obtains a new logical identifier $x _ { D - 1 } \ldots x _ { 2 } x _ { 1 }$ and maintains links to nodes $x _ { D - 2 } \ldots x _ { 2 } x _ { 1 } \beta ,$ , w h e r e $\beta \in \{ 0 , 1 , 2 , \ldots , d \} - \{ x _ { 1 } \}$ . F o r $\forall \alpha \in \{ 0 , 1 , 2 , \ldots , d \} - \{ x _ { 1 } \}$ , the identifier of an out-neighbor $x _ { D - 1 } ^ { \prime } \ldots x _ { 2 } x _ { 1 }$ - of node $x = x _ { D } \ldots x _ { 2 } x _ { 1 }$ is updated with $x _ { D - 2 } \ldots x _ { 2 } x _ { 1 } \alpha$ after shrinking the topology. It is clear that all out-neighbors of node $x _ { D - 1 } \ldots x _ { 2 } x _ { 1 }$ are the same outneighbors of node $x _ { D } \ldots x _ { 2 } x _ { 1 }$ although their logical identifiers are updated.

In other words, the links maintained by each node do not change, and no network overhead is further incurred. For example, node A is labeled 021 and has out-neighbor B with identifier 012 and C with identifier 210 before shrinking the entire topology, as shown in Fig. 5b. After shrinking the entire topology, the identifiers of node $A , B ,$ and C are updated as 21, 12, and 10, respectively. As shown in Fig. 5a, the out-neighbors of node A are still the nodes B and C. Thus, Theorem 7 holds. tu

# 6 ANALYSIS AND EVALUATION

We use PeerSim to implement MOORE. PeerSim is a P2P simulation framework aimed at developing and testing any kind of P2P protocols in a dynamic environment. Our simulations are cycle-based, and the MOORE topology with any order is evolved from the smallest Kautz digraph $K ( d , 1 )$ through those dynamic operations of nodes mentioned above. In this section, we will evaluate the following characteristics of MOORE: degree distribution, diameter, average routing path length, and congestion. The value of each characteristic under different network configurations is the average value of a sample achieved from at least 100 rounds of simulations.

# 6.1 Degree Distribution of MOORE

Property 1. MOORE is d-regular and has a constant degree if its order equals to k multiple of $n _ { 0 }$ for $1 < k \leq d ,$ where n0 denotes the order of its predecessor Kautz digraph. Otherwise, it is d-out-regular and has a constant degree. Its index of expandability is not larger than $\delta ^ { - } \left( I K ( d , n ) \right)$ .

Proof. The proof has been proposed in Section 3.

Theorem 3 proposes the bound on its minimum indegree. In this section, we focus on the in-degree distribution of MOORE with orders 7,680 and 18,000 under node identifier choice policies factorRandom and cycleSequence.

Fig. 6 shows that the in-degree of most nodes is adjacent to d and that of the remaining nodes is close to the trail of its in-degree distribution figure. The in-degree of more nodes is close to d and far away from the trail of its in-degree distribution if MOORE adopts the cycleSequence policy rather than factorRandom policy. Thus, cycleSequence is more suitable to MOORE for improving its connectivity and robustness, especially if the order is close to that of its predecessor Kautz digraph.

![](images/4db0118643315fadfb792073fbfc4b41f7e2157c7916165c1acd4c41a9696d4a.jpg)



(a)

![](images/84e7c0f1d453ab54924898ae28fa699f10ff19cdaa76c9738de5e17460cdd8de.jpg)



(b)   
Fig. 6. The in-degree distribution of IKð4; 7;680Þ and IKð4; 18;000Þ. (a) The in degree of peers in a network with order 7,680. (b) The in degree of peers in a network with order 18,000.

We know that the order of $I K ( 4 , 7 , 6 8 0 )$ and $I K ( 4$ ; $^ { 1 8 , 0 0 0 ) }$ is covered by ranges $( n _ { 0 } , 2 n _ { 0 } ]$ and $[ 3 n _ { 0 } , 4 n _ { 0 } ] .$ , where $n _ { 0 }$ denotes the order of $K ( 4 , 6 )$ and $4 n _ { 0 }$ equals that of $K ( 4 , 7 )$ . Thus, the least in-degrees of $I K ( \bar { 4 } , 7 , 6 8 0 )$ and IKð4; 18;000Þ are 1 and 3 according to Theorem 3, as shown in Fig. 6. Furthermore, the in-degree of most nodes is around d and that of few nodes is around the tail of its indegree distribution figure, if the order of MOORE is adjacent to any multiple of $n _ { 0 }$ .

# 6.2 Diameter and Path Length Distribution of MOORE

In an overlay network, the length of a routing path denotes the number of hops from the source to the destination along the routing path.

Property 2. Given a MOORE with arbitrary order n and outdegree $d ,$ its diameter is $\begin{array} { r } { D _ { l } = \lceil \log _ { d } \frac { n } { d + 1 } + 1 \rceil } \end{array}$ .

Proof. First, let’s calculate D such that $d ^ { D - 2 } ( d + 1 ) < n <$ < $d ^ { D - 1 } ( d + 1 )$ . Thus, the length of the node identifier must be $D ,$ and we can always find a pair of vertices at distance D. Thus, $\begin{array} { r } { D _ { l } = \lceil \log _ { d } \frac { n } { d + 1 } + 1 \rceil } \end{array}$ . tu

According to the well-known results of the order/diameter problem, we know that $D _ { l }$ is the smallest diameter for any number of vertices n where $d ^ { D - 1 } + d ^ { D - 2 } \leq n \leq d ^ { D } + d ^ { D - 1 }$ . A lookup for a resource or node initiated by any node can reach its destination in $O ( \log _ { d } n )$ hops. The same result holds for publishing resources.

We evaluate the diameter and average path length of MOORE in different scales (from 256 to 22,528 peers) and compare it with other constant degree digraphs with the same degree $^ { 4 , }$ such as 2D CAN, 3D CAN, 4D butterfly, de Bruijn, and Kautz digraph. In each experiment, we sample at least $n ^ { \prime } = \lceil n / 2 \rceil$ nodes randomly, and let each sampled node launch a routing to other $n - 1$ nodes, then analyze the average path length over $n ^ { \prime } ( n - 1 )$ routings.

As shown in Figs. 7 and 8, the curves of butterfly, de Bruijn, and Kautz digraphs are dashed lines or discrete points since their orders are discrete sequences, while that of MOORE and CAN are solid lines because of their arbitrary orders. In Fig. $^ { 7 , }$ the diameter of MOORE is less than $1 . 2 \log _ { 4 } n$ and that of butterfly and CAN at the whole order axis. In Fig. 8, the average path length of MOORE is also less than $1 . 2 \log _ { 4 } n$ and that of butterfly and CAN at the whole order axis. In the two figures, we do not compare MOORE with k-dimensional CCC directly since the degree of CCC is 3 irrespective of the value of k. In reality, the diameter and average path length of MOORE with out-degree 3 are also less than that of CCC, respectively. Furthermore, the average path length of MOORE under different scales is trivially different if the scales are covered by an identical range, such as [320, 1,280), [1,280, 5,120), [5,120, 20,480) in Fig. 8.

![](images/91ef8048e1ff0ddfe6457b4c95edb7b0c8c90889e903e33d1069bfa9c4a413bd.jpg)



Fig. 7. The diameter of several topologies under different configurations.   
![](images/246c42eec91fd6f03eee846a10a79cb25308ec5e4704b407c60e94c4a786a277.jpg)

Fig. 8. The average path length of several topologies under different configurations.   
![](images/9ff141359848d7dc3269c7ffb92863c46ab95fb03a5b2349994ead5985d48cd1.jpg)



Fig. 9. The path length distribution of IKð4; 12;800Þ and IKð4; 10;240Þ.

Property 3. With the shortest path routing scheme, MOORE can achieve low congestion.

Proof. Fig. 9 shows the distribution of the routing path length of IKð4; 12;800Þ and IKð4; 10;240Þ. We can observe that more than 90 percent of routing path lengths are close to the diameter of MOORE. We also find that there exists a similar result under any scale of MOORE. This is closer to the result of the long path routing scheme used by [10], [19]. Therefore, it is reasonable that MOORE can also achieve the similar low congestion characteristic discussed by Xu et al. [12] and Li et al. [19] although our algorithm adopts a shortest path routing scheme. tu

Property 4. Messages caused by node joining and departing operations are at most 2:5d logd n and $( 2 . 5 d + 1 ) \log _ { d } n .$ . Only d and 2d nodes need to update routing tables when dealing with a new node and a departed node, respectively.

Proof. Recall that Algorithm 3 must find d out-neighbors in order to construct its routing table, and inform d inneighbors to update their routing table. Algorithm 4 may need to find a substitute node first. Therefore, the former part of Property 4 holds because the routing length is less than 1:2 log n, and the latter part also holds according to the two algorithms. tu

Ideally, there should also be a discussion on one of the biggest problems of P2P systems, i.e., performance under churn. This is partially addressed through the discussion in Section 5; though which level of churn would still be sustainable for MOORE is not being discussed.

# 7 CONCLUSION

MOORE is the first efficient structured P2P network based on the quasi-Kautz digraph and is $O ( \log _ { d } n )$ in diameter with a constant node out-degree. It constructs an overlay digraph for all network sizes and any constant degree, and achieves optimal diameter, high performance, good connectivity, and low congestion. In the future, we will improve MOORE to support more types of queries, such as range and multiattribute queries, and consider the locality of the physical network to reduce latency.

# ACKNOWLEDGMENTS

The authors would like to thank anonymous reviewers for their constructive comments. The work of Deke Guo is supported in part by the National Science Foundation of China under Grant No. 60903206, the China Postdoctoral Science Foundation under Grant No. 20100480898, and the Preliminary Research Foundation of National University of Defense Technology. The work of Hai Jin is supported in part by the NSFC/RGC Joint Research Foundation under Grant No. 60731160630.

# REFERENCES

[1] S. Ratnasamy, P. Francis, M. Handley, R. Karp, and S. Shenker, “A Scalable Content Addressable Network,” Proc. ACM SIGCOMM, pp. 161-172, 2001.   
[2] I. Stoica, R. Morris, D.R. Karger, M.F. Kaashoek, and H. Balakrishnan, “Chord: A Scalable Peer-to-Peer Lookup Service for Internet Applications,” IEEE/ACM Trans. Networking, vol. 11, no. 1, pp. 17-32, Feb. 2003.   
[3] A. Rowstron and P. Druschel, “Pastry: Scalable, Decentralized Object Location, and Routing for Large-Scale Peer-to-Peer Systems,” Lecture Notes in Computer Science, pp. 329-350, Springer, 2001.

[4] P. Maymounkov and D. Mazieres, “Kademlia: A Peer-to-Peer Information System Based on the XOR Metric,” Proc. Int’l Peer-to-Peer Symp., pp. 53-65, Mar. 2002.   
[5] D. Malkhi, M. Naor, and D. Ratajczak, “Viceroy: A Scalable and Dynamic Emulation of the Butterfly,” Proc. 21st ACM Symp. Principles of Distributed Computing (PODC), pp. 183-192, Aug. 2002.   
[6] F. Kaashoek and D. Karger, “Koorde: A Simple Degree-Optimal Distributed Hash Table,” Proc. Int’l Peer-to-Peer Symp., pp. 98-107, Feb. 2003.   
[7] J. Xu, Topological Structure and Analysis of Interconnection Networks. Kluwer Academic Publishers, 2001.   
[8] S. Banerjee and D. Sarkar, “Hypercube Connected Rings: A Scalable and Fault-Tolerant Logical Topology for Optical Networks,” Computer Comm., vol. 24, no. 11, pp. 1060-1079, 2001.   
[9] K.N. Sivarajan and R. Ramaswami, “Lightwave Networks Based on De Bruijn Graphs,” IEEE/ACM Trans. Networking, vol. 2, no. 1, pp. 70-79, Feb. 1994.   
[10] G. Panchapakesan and A. Sengupta, “On a Lightwave Networks Topology Using Kautz Digraphs,” Computer, vol. 48, no. 10, pp. 1131-1137, Oct. 1999.   
[11] B.Y. Zhao, J. Kubiatowicz, and A.D. Joseph, “Tapestry: A Fault-Tolerant Wide-Area Application Infrastructure,” ACM SIGCOMM Computer Comm. Rev., vol. 32, no. 1, p. 81, 2002.   
[12] J. Xu, A. Kumar, and X.X. Yu, “On the Fundamental Tradeoffs between Routing Table Size and Network Diameter in Peer-to-Peer Networks,” IEEE J. Selected Areas in Comm., vol. 22, no. 1, pp. 151-163, Jan. 2004.   
[13] M.G. Hluchyj and M.J. Karol, “Shufflenet: An Application of Generalized Perfect Shuffles to Multihop Lightwave Networks,” Proc. IEEE INFOCOM, pp. 379-390, 1988.   
[14] H. Shen, C. Xu, and G. Chen, “Cycloid: A Constant-Degree and Lookup-Efficient P2P Overlay Network,” Performance Evaluation, vol. 63, no. 3, pp. 195-216, 2006.   
[15] M. Naor and U. Wieder, “Novel Architecture for P2P Applications: The Continuous-Discrete Approach,” Proc. ACM Symp. Parallel Algorithms and Architectures, pp. 50-59, June 2003.   
[16] P. Fraigniaud and P. Gauron, “D2B: A De Bruijn-Based Content-Addressable Network,” Theoretical Computer Science, vol. 355, no. 1, pp. 65-79, 2006.   
[17] D. Loguinov, J. Casas, and X. Wang, “Graph-Theoretic Analysis of Structured Peer-to-Peer Systems: Routing Distances and Fault Resilience,” IEEE/ACM Trans. Networking, vol. 13, no. 5, pp. 1107- 1120, Oct. 2005.   
[18] A.T. Gai and L. Viennot, “Broose: A Practical Distributed Hash Table Based on the De Bruijn Topology,” Proc. Int’l Conf. Peer-to-Peer Computing, pp. 167-174, Aug. 2004.   
[19] D. Li, X. Lu, and J. Wu, “FISSIONE: A Scalable Constant Degree and Low Congestion DHT Scheme Based on Kautz Graphs,” Proc. IEEE INFOCOM, pp. 1677-1688, Mar. 2005.   
[20] M. Miller and J. Siran, “Moore Graphs and Beyond: A Survey of the Degree/Diameter Problem,” Electronic J. Combinatorics, vol. 61, pp. 1-63, Dec. 2005.   
[21] M. Imase and M. Itoh, “Design to Minimum Diameter on Building-Block Network,” IEEE Trans. Computers, vol. C-30, no. 6, pp. 439-442, June 1981.   
[22] M. Imase and M. Itoh, “A Design for Directed Graphs with Minimum Diameter,” IEEE Trans. Computers, vol. C-32, no. 8, pp. 782-784, Aug. 1983.   
[23] N. Alon, S. Hoory, and N. Linial, “The Moore Bound for Irregular Graphs,” Graphs and Combinatorics, vol. 18, no. 1, pp. 53-57, 2002.   
[24] R.M. Damerell, “On Moore Graphs,” Proc. Cambridge Philosophical Soc., pp. 227-236, 1973.   
[25] P. Tvrdik, “Partial Kautz Line Digraphs with Maximal Connectivity,” Research Report 94-15, LIP ENSL, Apr. 1994.   
[26] D. Guo, Y. Liu, and X. Li, “BAKE: A Balanced Kautz Tree Structure for Peer-to-Peer Networks,” Proc. 27th IEEE INFOCOM, Apr. 2008.   
[27] Y. Zhang, D. Li, and X. Lu, “Distributed Line Graphs: A Universal Framework for Building DHTs Based on Arbitrary Constant-Degree Graphs,” Proc. IEEE 28th Int’l Conf. Distributed Computing Systems (ICDCS), pp. 152-159, June 2008.   
[28] M.A. Fiol and A.S. Llado, “The Partial Line Digraph Technique in the Design of Large Interconnection Networks,” IEEE Trans. Computers, vol. 41, no. 7, pp. 848-857, July 1992.

![](images/79fe56f52864d93117672f906c9f3704e5da4071a8ca2b7b9d89b667203546b2.jpg)



Deke Guo received the BS degree in industry engineering from Beijing University of Aeronautic and Astronautic, China, in 2001, and the PhD degree in management science and engineering in 2008 from the National University of Defense Technology, Changsha, P.R. China, where he is now an associate professor of information system and management. He was a visiting scholar in the Department of Computer Science and Engineering at The Hong Kong University of

Science and Technology from January 2007 to January 2009. His current research interests include peer-to-peer computing, Bloom filters, data center networking, and wireless networks. He is a member of the ACM and the IEEE.

![](images/1ccdabde50f813bf1e230b79b4c58c6e55e953517053121f795059f4af0fc99d.jpg)



Jie Wu is the chair and a professor in the Department of Computer and Information Sciences, Temple University. Prior to joining Temple University, he was a program director at the US National Science Foundation (NSF). His research interests include wireless networks and mobile computing, routing protocols, fault-tolerant computing, and interconnection networks. He has published more than 550 papers in various journals and conference proceedings.

He serves on the editorial board of the IEEE Transactions on Computers, IEEE Transactions on Mobile Computing, and the Journal of Parallel and Distributed Computing. Dr. Wu is program cochair for IEEE INFOCOM 2011. He was also general cochair for IEEE MASS 2006, IEEE IPDPS 2008, ACM WiMD 2009, and IEEE/ACM DCOSS 2009. He also served as panel chair for ACM MobiCom 2009. He has served as an IEEE Computer Society distinguished visitor. Currently, he is the chair of the IEEE Technical Committee on Distributed Processing (TCDP) and ACM distinguished speaker. Dr. Wu is a fellow of the IEEE.

![](images/777ca45f96ff89e92de8a8488603ced634183ce34fa3bfe28ef6dc7d0a3332d9.jpg)



Yunhao Liu received the BS degree from the Automation Department, Tsinghua University, P.R. China, in 1995, the MA degree from Beijing Foreign Studies University, China, in 1997, and the MS and the PhD degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is a member of Tsinghua National Lab for Information Science and Technology, and the director of Tsinghua National MOE Key Lab for Information Security.

He is also a faculty in the Department of Computer Science and Engineering, The Hong Kong University of Science and Technology. He is a senior member of the IEEE and also an ACM distinguished speaker.

![](images/9930fce31175e653388fac4c1779aec6943f0579cb1fdfb8daf58f43f1845347.jpg)



Hai Jin received the PhD degree in computer engineering in 1994 from Huazhong University of Science and Technology (HUST), P.R. China, where he is currently the Cheung Kong professor and the dean of the School of Computer Science and Technology. In 1996, he was awarded a German Academic Exchange Service Fellowship to visit the Technical University of Chemnitz, Germany. He worked at the University of Hong Kong between 1998 and 2000, and as a visiting

scholar at the University of Southern California between 1999 and 2000. He was awarded the Distinguished Young Scholar Award from the National Science Foundation of China, in 2001. He is the chief scientist of ChinaGrid, the largest grid computing project in China. He has coauthored 15 books and published more than 400 research papers. His research interests include computer architecture, virtualization technology, cluster computing and grid computing, peer-to-peer computing, network storage, and network security. He is a senior member of the IEEE and a member of the ACM. He is a member of the Grid Forum Steering Group (GFSG).

![](images/6e434372dd9c1ae2e33fce11c64f1f82991e3e36ba8c3bcfcd506fe106ab8025.jpg)



Hanhua Chen received the PhD degree in computer science and engineering in 2010 from Huazhong University of Science and Technology, P.R. China, where he worked as an associate professor. He worked at The Hong Kong University of Science and Technology as a visiting scholar between 2007 and 2009, and as a research associate between 2009 and 2010. His research interests include peer-to-peer computing and wireless sensor networks. He is

a member of the IEEE and the IEEE Computer Society.

![](images/261efd18cc968129bf5616d0517df9790466fd729e20e3670814e18ede9fefa4.jpg)



Tao Chen received the BS degree in military science and the MS degree in military operational research from the National University of Defense Technology, Changsha, P.R. China, in 2004 and 2006, respectively. He is currently working toward the PhD degree in the School of Information System and Management, National University of Defense Technology, Changsha, P.R. China. His current research interests include wireless sensor networks, peer-to-peer comput-

ing, and data center networking. He is a member of the IEEE.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.