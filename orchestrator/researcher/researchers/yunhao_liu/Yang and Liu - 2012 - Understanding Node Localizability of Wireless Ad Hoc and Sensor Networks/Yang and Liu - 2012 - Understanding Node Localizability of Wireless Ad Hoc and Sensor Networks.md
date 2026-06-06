# Understanding Node Localizability of Wireless Ad Hoc and Sensor Networks

Zheng Yang, Member, IEEE, and Yunhao Liu, Senior Member, IEEE

Abstract—Location awareness is highly critical for wireless ad-hoc and sensor networks. Many efforts have been made to solve the problem of whether or not a network can be localized. Nevertheless, based on the data collected from a working sensor network, it is observed that the network is not always entirely localizable. Theoretical analyses also suggest that, in most cases, it is unlikely that all nodes in a network are localizable, although a (large) portion of the nodes can be uniquely located. Existing studies merely examine whether or not a network is localizable as a whole; yet two fundamental questions remain unaddressed: First, given a network configuration, whether or not a specific node is localizable? Second, how many nodes in a network can be located and which are them? In this study, we analyze the limitation of previous works and propose a novel concept of node localizability. By deriving the necessary and sufficient conditions for node localizability, for the first time, it is possible to analyze how many nodes one can expect to locate in sparsely or moderately connected networks. To validate this design, we implement our solution on a real-world system and the experimental results show that node localizability provides useful guidelines for network deployment and other location-based services.

Index Terms—Localization, localizability, graph rigidity, wireless sensor networks, ad hoc networks.

# 1 INTRODUCTION

HE proliferation of wireless and mobile devices has Tfostered the demand for context-aware applications, in which location is viewed as one of the most significant contexts.

A number of methods have been proposed in the literature and used in practice to locate wireless devices. One method to determine the location of a device is through manual configuration, which may not be feasible for largescale deployments or mobile systems. Another possibility is Global Positioning System (GPS). Although it is a popular system, it is not suitable for indoor environments and suffers from high hardware cost.

In recent years, several approaches have been proposed for in-network localization, in which some special nodes (called beacons or seeds) know their global locations and the rest determine their locations by measuring the euclidean distances to their neighbors. Based on distance ranging techniques [1], [2], the ground truth of a wireless ad hoc network can be modeled by a distance graph $G = ( V , E )$ , where V denotes the set of wireless communication devices (e.g., laptop, RFID, or sensor node) and there is an unweighted edge $( i , j ) \in E$ if the distance between a pair of vertices i and j, denoted by $d ( i , j )$ , can be measured or both of them are in known locations, e.g., beacon nodes.

For localization, an essential question occurs as to whether or not a network is localizable given its distance graph. This is called the network localizability problem. A graph $G = ( V , E )$ with possible additional constraints I

. The authors are with the School of Software, TNLIST, Tsinghua Unviersity, and The Hong Kong University of Science and Technology. E-mail: yangzheng@tsinghua.edu.cn, yunhao@greenorbs.com.

Manuscript received 7 Dec. 2010; revised 27 Feb. 2011; accepted 8 Apr. 2011; published online 26 May 2011. For information on obtaining reprints of this article, please send e-mail to: tmc@computer.org, and reference IEEECS Log Number TMC-2010-12-0556. Digital Object Identifier no. 10.1109/TMC.2011.122.

(such as the known locations of some beacon nodes) is localizable if there is a unique location pðiÞ of every node i such that the distance $d ( i , j ) = d ( p ( i ) , p ( j ) )$ for all links $( i , j ) \in E$ and the constraint I is preserved. Previous studies have shown that the network localizability problem is closely related to graph rigidity [3], [4], [5], [6]. Based on rigidity theory, Jackson and Jordan [5] first present the necessary and sufficient condition for network localizability and design a polynomial algorithm for localizability testing.

The above conclusion, however, is NOT the end of the localizability story. This work is motivated by the observation from an ongoing sea monitoring project [7]. We launched a working sensor network consisting of a hundred of nodes continuously collecting scientific data. Due to tide and wind under natural conditions, the network topology is highly dynamic. Checking the collected network trace, to our surprise and disappointment, we find that almost always the network fails to be localizable. Hence, localizability test only gives the “fail” answer. The situation recurs for static sensor networks: theoretical analyses [8] indicate that, unless networks are highly dense and regular, in most cases, it is unlikely that all nodes in a network are localizable, but a (large) portion of nodes can be uniquely located. Thus, the network localizability testing is less meaningful in practice, considering the fact that many applications can function properly as long as a sufficient number of nodes are aware of their locations [8].

Although the theory for network localizability is complete, the following two fundamental questions cannot be answered by existing methods:

1. Given a network configuration, whether or not a specific node is localizable?   
2. How many nodes in a network can be located and which are them?

![](images/9f53c81ee3bcfc13ef3e0342dee571d5cf47f2fd189271ea3fc28ec702aea828.jpg)



(a)u is localizable.

![](images/c3d61257301fc29485669d0d68a081091567571dad9dce3525817559794d50c7.jpg)



(b) Graph decomposing.

![](images/b511622cee0b5e8e4b88e3f6593ebae0dadf015df7cb31650a1b66bd4274538c.jpg)

![](images/a7a36ecdc82c5288daa2b366b331e11d0a0e0857116c02b409afe9d376f7ade1.jpg)  
(c) 2 realizations of the left subgraph.   
Fig. 1. An example showing that the result from network localizability fails to identify node u as localizable.

Answering the above questions not only helps localization itself, but also provides instructive directions to some location-based services, such as topology control, mobility control, and node distribution. Therefore, the node localizability problem is considered in this study, which focuses on the location-uniqueness of a single node. Given a network configuration, a node is localizable if, in all realizations of the network that satisfy all internode distances, it has a unique computed location with respect to beacons. Indeed, network localizability is a special case of node localizability in which all nodes are localizable. Thus, node localizability is a more general issue.

The first major challenge for studying node localizability is to identify uniquely localizable nodes. Following the results for network localizability, an obvious solution is to find a localizable subgraph from the distance graph, and identify all the nodes in the subgraph localizable. Unfortunately, such a straightforward attempt misses some localizable nodes and wrongly identifies them as nonlocalizable, since some conditions (e.g., 3-connectivity) essential to network localizability are no longer necessary to node localizability. As shown in Fig. 1a, the node u can be uniquely located under this network configuration but not included in the 3-connected component of beacons. The uniqueness of u’s location is explained in Figs. 1b and 1c where we decompose the network into two subgraphs. As u connects two beacons in the right component, it has two possible locations denoted by u and u0 . If we adopt u0 as its location, it is impossible to embed the left subgraph into the plane. Specifically, the left subgraph has two realizations, but neither is compatible with u0 . Hence, u is uniquely localizable, although the 3-connectivity property does not hold. Motivated by the example, it is clear that the results derived for network localizability cannot be directly applied and we have to reconsider the conditions for node localizability.

The main contributions of this work are as follows: Motivated by a real deployed sensor network, we analyze the limitations of existing works on or related to node localizability, scattered over different literatures. Based on that, we derive so far the best necessary and sufficient conditions for node localizability which largely improves existing solutions both theoretically and practically. A localizability testing algorithm is accordingly designed, so that it is possible for the first time to observe how many nodes one can expect to be localizable in sparsely or moderately connected wireless networks. To validate this design, prototype implementation and large-scale simulations are conducted to examine the effectiveness and efficiency. Experimental results show that being aware of node localizability provides useful guidelines for network deployment and other location-based services.

The rest of the paper is organized as follows: We discuss the state of the art on network localizability and graph rigidity in Section 2. Necessary and sufficient conditions are presented for node localizability in Sections 3 and 4, respectively. The prototype implementation and simulations are discussed in Section 5. We summarize the related work in both network localization and graph rigidity literatures in Section 6, and conclude the work in Section 7.

# 2 PRELIMINARY

The ground truth of a network can be modeled by a distance graph G. We assume G is connected and has at least four vertices in the following analysis.

A realization of a graph G is a function p that maps the vertices of G to points in a euclidean space (this study assumes 2-dimension space). Generally, realizations are referred to the feasible ones that respect the pairwise distance constraints between a pair of vertices i and j if the edge $( i , j ) \in E$ . That is to say, $d ( p ( i ) , p ( j ) ) = d ( i , j )$ for all $( i , j ) \in E$ . Two realization of G are equivalent if they are identical under translations, rotations, and reflections in 2D plane. A distance graph G has at least one feasible realization which represents the ground truth of the corresponding network. Formally, G is embeddable in 2D space and all pairwise distances are compatible.

A graph is called generically rigid if one cannot continuously deform its realizations while preserving distance constraints [6]. A realization is generic if the vertex coordinates are algebraically independent. Since the set of generic realizations is dense in the realization space, almost all realizations are generic and we omit this word hereafter. A graph is globally rigid if it is uniquely realizable [4].

For a distance graph, there are several distinct manners in which the nonuniqueness of realization can appear. A graph is flexible if it can be continuously deformed while still satisfying all distance constraints, as shown in Fig. 2a; otherwise it is rigid. Hence, rigidity is a necessary condition for global rigidity.

Rigid graphs, however, are still susceptible to discontinuous flex. Specially, they can be subject to flip (or fold) ambiguities in which a set of nodes have two possible configurations corresponding to a “reflection” across a set of mirror nodes (e.g., v and w in Fig. 2b). This type of ambiguity is not possible in 3-connected graphs. A graph is said to be 3-connected if there does not exist any set of two vertices whose removal disconnects the graph.

Fig. 2c further shows that a 3-connected and rigid graph becomes flexible upon removal of an edge. After the removal of the edge $( u , v )$ , a subgraph can swing into a different configuration in which the removed edge constraint is satisfied and then reinserted. This type of ambiguity is eliminated by redundant rigidity, the property that a graph remains rigid upon removal of any single edge.

![](images/a240afbba1adb33dba072d68257fc5c833745fd9565e78d3ebd06182ca42eb94.jpg)



(a) Not rigid

![](images/d617cdd7e4305015d0ea61304a529859987bbba4bdd915e68dae95c439bd80c8.jpg)



(b) Not 3-connected

![](images/a5aa192afcdc608a8ba21388071362bf2b8614b0376434a3810f373d41758263.jpg)

![](images/f52195ddd3fbf8a828eddbe0241394e93c906ddef2a513caf531d446c9d7b796.jpg)



![](images/4df52e5f9876f86ee4a499bb66b39b47364ed6709a907f65948f010e744eed6a.jpg)



(c) Not redundantly rigid   
Fig. 2. Realization nonuniqueness.

Summarizing the above observations, Jackson and Jordan provide the necessary and sufficient condition for global rigidity in the following theorem.

Theorem 1 [5]. A graph with $n \geq 4$ vertices is globally rigid in 2 dimensions if and only if it is 3-connected and redundantly rigid.

Based on Theorem 1, global rigidity can be tested in polynomial time by combining existing algorithms for rigidity [4], [9] and 3-connectivity [10].

If fixing any group of three vertices to avoid trivial variations in 2D plane (i.e., translation, rotation, and reflection), a globally rigid graph is uniquely realizable. Accordingly, a network with at least three beacons is localizable if and only if its distance graph is globally rigid [3]. For node localizability, however, no such conclusion is presented so far.

# 3 NECESSARY CONDITIONS FOR NODE LOCALIZABILITY

Based on previous studies on network localizability, in this section, we will explore the necessary graph properties for node localizability.

# 3.1 Necessity of Three Vertex-Disjoint Paths

We have observed that some conditions essential to network localizability (e.g., 3-connectivity) are no longer necessary to node localizability.

To deal with the exception shown in Fig. 1, Goldenberg et al. [8] propose the first nontrivial necessary condition: if a vertex is localizable, it has three vertex-disjoint paths to three beacons. We denote such a condition as 3P for short. Suppose a vertex has only two vertex-disjoint paths to beacons. It definitely suffers from a potential flip ambiguity by reflecting along the line of a pair of cut vertices. Nevertheless, it is easy to find an example graph in which some nonlocalizable vertices satisfy the 3P condition. In Fig. 3, the vertex u is flexible although it has three vertexdisjoint paths to three distinct beacon vertices.

# 3.2 Necessity of Redundant Rigidity

It is clear that rigidity is necessary but not sufficient for node localizability. As shown in Fig. 2b, the vertex u is nonlocalizable although the graph is rigid. Generally, for any rigid graph $G ,$ almost all realizations of G are not unique if G is not redundantly rigid.

To analyze the necessity of redundant rigidity, we present Lemma 1 which is first proved by Hendrickson [4].

Lemma 1. If a graph G is flexible, then for almost all realizations r of G, the finite flexing of r contains a submanifold that is diffeomorphic to the circle.

Inspired by Lemma 1, we explore implicit graph structures and obtain the main result of this section.

Theorem 2 (Necessity of redundant rigidity). In a distance graph $G = ( V , E )$ with a set $B \subset V$ of $k \geq 3$ vertices at known locations, if a vertex is localizable, it is included in the redundantly rigid component that contains B.

Proof. Assume the only interesting case that G is rigid but not redundantly rigid. Suppose RRC is the redundantly rigid component containing B and a vertex $u \not \in R R C .$ . There is an edge $\boldsymbol { e } = ( v , w )$ whose removal results in u and B belonging to different rigid components in $G - e .$ . Accordingly, there is a continuous flexing in which u changes its location relative to B. By Lemma 1, any realization of $G - e$ contains a submanifold diffeomorphic to the circle. The distance between v and w will be a multivalued function for almost every point on this circle. Hence, there exists another realization of $G - e$ that keeps the distance between v and w unchanged according to the generic graph assumption. Adding e back, it forms a realization of G in which the location of u is changed. Therefore, u is nonlocalizable. tu

Now we have obtained a better necessary condition for node localizability by combining 3P (three vertex-disjoint paths) and Theorem 2 (redundant rigidity), which we call RR-3P for short. Clearly, RR-3P is still not sufficient as illustrated in Fig. 4a. Considering the vertex $u ,$ it satisfies the RR-3P condition but not localizable due to the discontinuous flexing in which u can reflect along the axis denoted by the dashed line in Fig. 4b.

![](images/b6247b2076ac3f0a91c3c3d0fc79080db4ce43864e9bc272068f8a3b89953a42.jpg)



Fig. 3. The condition of three paths is not sufficient.

![](images/c31f888897e15c70f23354c7759ce79fe5daa7f645f2228912a9fd581839e1fe.jpg)



(a) The vertex u satisfies RR-3P.

![](images/b3a884170b27dc8e2396e7784f2aab0b67f05098e65713fe80a78af68f6e6d88.jpg)



(b) u suffers a discontinuous flexing.   
Fig. 4. RR-3P is not sufficient.

# 4 SUFFICIENT CONDITIONS FOR NODE LOCALIZABILITY

# 4.1 Extended Distance Graph

Based on Theorem 1, an obvious sufficient condition to node localizability is as follows: if a vertex belongs to the globally rigid subgraph of G that contains at least three beacon vertices, it is uniquely localizable [8]. For convenience, we denote this condition as RRT standing for Redundant Rigidity and Tri-connected.

Note that a localizable vertex does not necessarily satisfy RRT, as shown in Fig. 5a. The graph consists of three beacon vertices (denoted by white circles) and three nonbeacon vertices (denoted by black ones). It is clear that u is not in the 3-connected component of three beacon vertices. However u’s location can be uniquely determined under the configuration. The possible reason is the distance between u and v is actually fixed although no edge connects them. If we add the edge $( u , v )$ to $G ,$ u can be easily identified as localizable since the distances from u to 3 beacon vertices are available. This observation leads us to explore the implicit edges for identifying localizable vertices.

Let R denote the set of all realizations of G. For simplicity, let $d _ { r } ( u , v )$ instead of $d ( r ( u ) , r ( v ) )$ denote the euclidean distance between the two vertices u and v in a specific realization $r \in R$ .

Let $\begin{array} { r } { D _ { G } ( u , v ) = \bigcup _ { r \in R } \left\{ d _ { r } ( u , v ) \right\} } \end{array}$ . For a rigid graph $G , R$ is finite although jRj can be exponential to the size of G. As a result, $D _ { G } ( u , v )$ is finite since the number of distinct values of $D _ { G } ( u , v )$ is at most $| R |$ .

Definition 1 (Implicit edge). In a distance graph $G = ( V , E )$ , an edge $( u , v )$ is implicit $i f \left( u , v \right) \notin E$ and in all realizations of $G ,$ the distances between u and v are the same.

If $( u , v )$ is an implicit edge, it is equivalent to the fact that $D _ { G } ( u , v )$ contains a unique value. Based on the concept of implicit edge, we define the extended distance graph of a distance graph.

Definition 2 (Extended distance graph). For a distance graph $G = ( V , E )$ , its extended distance graph is $G ^ { I } = ( V , E \bar { \cup } \dot { E ^ { I } } )$ where $E ^ { I }$ is a set of implicit edges of G.

For any single implicit edge $\boldsymbol { e } = ( u , v )$ , adding e to G does not make any change to R since $D _ { G } ( u , v )$ contains only one value. Hence, vertices being localizable in $G ^ { I }$ are also localizable in G. Although the set of localizable vertices in G is identical to $G ^ { I }$ , being aware of $G ^ { I }$ does help to identify localizable vertices. Recalling the example shown in Fig. 5, u can be easily marked as localizable by trilateration when $( u , v )$ is inserted. Now, the problem becomes finding the implicit edges for a given graph G. Nevertheless, the definition of implicit edges does not really help for actually finding them.

![](images/ac18a3a88c23a43c8fbf8b8187d51f297baebd2d90717e6646fc6fdae45049fc.jpg)



(a) $\scriptstyle ( u , \nu )$ is implicit

![](images/d930c29175d44801508d1eda20604bc6057ce1ef7e476ca8a0f0fc36d3aaa32c.jpg)



(b) 2 rigid subgraphs   
Fig. 5. Implicit edge.

Let $( E _ { 1 } , E _ { 2 } )$ be a partition of $E \ ( { \mathrm { i . e . , } } \ E _ { 1 } \cup E _ { 2 } = E$ and $E _ { 1 } \cap E _ { 2 } = \phi )$ and let $V _ { i }$ be the set of endpoint vertices of all edges in $E _ { i } , i = 1 , 2$ . Normally, there are some vertices $V _ { c }$ covered by both $E _ { 1 }$ and $E _ { 2 }$ so that $V _ { c } = V _ { 1 } \cap V _ { 2 }$ . For any partition $( E _ { 1 } , E _ { 2 } )$ of $E , V _ { c }$ contains at least one vertex if G is connected, or at least two vertices if G is rigid.

Lemma 2. In a graph $G = ( V , E )$ with two subgraphs $G _ { 1 } =$ $( V _ { 1 } , E _ { 1 } )$ and $G _ { 2 } = ( V _ { 2 } , E _ { 2 } )$ , where $( E _ { 1 } , E _ { 2 } )$ is a partition of $E ,$ for any two vertices $\{ u , v \} \subset V _ { c } ,$ if both u and v belong to a rigid component in $G _ { 1 }$ and a rigid component in $G _ { 2 , }$ , the edge $( u , v )$ is implicit $i f \left( u , v \right) \notin E$ .

Proof. First, let d denote the distance between u and v in the ground truth realization of $G ;$ thus, $d \in D _ { G } ( u , v )$ . Second, we want to show that $D _ { G } ( u , v )$ contains the only element d. Let $R C _ { 1 }$ and $R C _ { 2 }$ denote the rigid components in $G _ { 1 }$ and $G _ { 2 } ,$ respectively. Since $R C _ { 1 }$ and $R C _ { 2 }$ are rigid, both $D _ { R C 1 } ( u , v )$ and $D _ { R C 2 } ( u , v )$ are finite. For notation simplicity, we omit $^ { \prime \prime } ( u , v ) ^ { \prime \prime }$ hereafter. As $E _ { 1 } \cap E _ { 2 } = \phi .$ , the values in $D _ { R C 1 } - \{ d \}$ and $D _ { R C 2 } - \{ d \}$ are chosen independently in the possible distance space where $D _ { R C 1 }$ and $D _ { R C 2 }$ have measure zero. Hence, for almost every point p in the distance space, $p \in \{ D _ { R C 1 } - \{ d \} \}$ implies $p \notin \{ D _ { R C 2 } -$ $\{ d \} \}$ with probability 1. As $D _ { G } \subseteq D _ { R C 1 } \cap D _ { R C 2 } ,$ d is the only value in $D _ { G }$ and ðu; vÞ is thus implicit if $( u , v ) \notin E . \boxed { \cdot }$

Lemma 2 provides an approach to identify implicit edges and it is possible to construct the extended distance graph $G ^ { I }$ . Back to the example shown in Fig. 5a, we decompose the entire graph into two subgraphs, as illustrated in Fig. 5b. Since both subgraphs are rigid, $( u , v )$ is an implicit edge according to Lemma 2.

Combining Theorem 1 and the concept of implicit edges, we achieve the following theorem.

Theorem 3. Let $G ^ { I }$ denote the extended distance graph of $G =$ $( V , E )$ which has a set $B \subset V$ of $k \geq 3$ vertices at known locations. If a vertex belongs to a globally rigid subgraph of $G ^ { I }$ that contains at least three vertices in B, it is uniquely localizable in $G .$

![](images/9ad8d2a5cd41999df11d2708af19305b0b64b298687b7aa9a0c6129f147a2e5e.jpg)



(a) Before replacement.

![](images/cf23123b53fe88f06f495d72b1bdcf31c58b2bab66d52cc552094ebdcba90fd8.jpg)



(b) After replacement.   
Fig. 6. Edge replacement (1).

# 4.2 Sufficiency of RR3P Condition

Theorem 3 provides so far the best sufficient condition for node localizability. However, it requires the knowledge of implicit edges which incurs combinational number of graph partitions. In this section, we propose an equivalent combinatorial condition to Theorem 3 without actually calculating and using implicit edges. Specifically, we want to show that a vertex is localizable if it belongs to the redundantly rigid component that includes three vertexdisjoint paths connecting it to three beacon vertices. We call this condition RR3P for short. Note that RR3P is fundamentally different from the previously mentioned RR-3P. RR3P requires the three paths strictly residing in the redundantly rigid component to avoid the unexpected case in Fig. 4. We use the similar terms to show their close relationship.

Due to the necessity of redundant rigidity, for convenience, we assume G is redundantly rigid; otherwise let G denote the redundantly rigid component containing B. If G is 3-connected, it is trivial that all vertices are localizable since G itself is globally rigid, so we focus on the only interesting case that G is not 3-connected. There exist two vertices v and w whose removal disconnects G. As a result, as shown in Fig. 6a, G can be divided into several overlapped and connected components $G _ { i }$ such that

$$
G = \bigcup_ {i} G _ {i} \text {   and   } V (G _ {i} \cap G _ {j}) = \{v, w \} \text {   for   all   } i \neq j.
$$

For any specific $G _ { i , }$ , we replace other components $G _ { j } ( j \neq i )$ by an edge $\boldsymbol { e } = ( v , w )$ . This operation, as illustrated in Fig. 6, is defined as edge replacement.

Lemma 3. In a graph $G = ( V , E )$ that is redundantly rigid but not 3-connected, there exists a pair of cut vertices $\{ v , w \} \subset V$ and G can be divided into a number of connected and overlapped subgraphs $G _ { i }$ . According to edge replacement,

1. $G _ { i } + e$ is redundantly rigid and $\boldsymbol { e } = ( v , w )$ is an implicit edge in G if e 62 E;   
2. If a vertex u has three vertex-disjoint paths to three pairwise connected vertices B in $G ,$ , u and B are in the same subgraph $G _ { i } ,$ and there still exist three vertexdisjoint paths connecting u to B in $G _ { i } + e .$ .

Proof. For part 1, suppose to the contrary that for some $i ,$ $G _ { i } + e$ is not redundantly rigid. Thus, there exists some edge e0 in $G _ { i } + e$ whose removal results in the remaining graph, $G _ { i } + e - e ^ { \prime }$ , nonrigid. Since e cannot be the only one edge whose removal destroys the rigidity of a graph that is not redundantly rigid, we assume $e ^ { \prime } \neq e$ hereafter. Considering the entire graph $G ,$ as a result, $G - e ^ { \prime }$ is not rigid, contradicting the fact that G is redundantly rigid. Hence, $G _ { i } + e$ is redundantly rigid. It follows that all $G _ { i }$

![](images/26a51a87e1241bd082e8840fd0c164084c3df0291e8acc7839d6fd49325c5eb9.jpg)



(a) $p _ { 3 }$ traverses beyond $G _ { i } .$

![](images/ab9d7c28300078460cfe15d1db007ee437173178b41538a925baafd206bd3326.jpg)



(b) A shortcut in $p _ { 3 }$   
Fig. 7. Edge replacement (2).

are rigid and $e$ is accordingly an implicit edge due to Lemma 2.

For part 2, since B is fully connected, it is entirely included in some $G _ { i } .$ In addition, u is in $G _ { i }$ otherwise it cannot have three nonintersecting paths to B. Let $p _ { i } ( i =$ 1; 2; 3Þ denote three vertex-disjoint paths from u to B in G. If none of $p _ { i }$ traverses beyond $G _ { i } ,$ then all $p _ { i }$ still exist in $G _ { i } + e .$ Otherwise, WLOG, assume $p _ { 3 }$ traverses $G _ { j } ,$ as shown in Fig. 7a. It should enter $G _ { j }$ at one of fv; wg and exit at the other. We make a shortcut by replacing the path segment in $G _ { j }$ by a single edge e, as illustrated in Fig. 7b. The new path still connects u and B and does not intersect the other two paths. Therefore, u has three vertex-disjoint paths to B in $G _ { i } + e .$ . tu

Lemma 3 shows that edge replacement preserves the redundant rigidity and connectivity properties in the remaining graph $G _ { i } + e$ .

Now we show that the reverse process of an edge replacement also preserves the two properties. Suppose $G _ { i } + \epsilon$ is redundantly rigid and $\boldsymbol { e } = ( v , w )$ is an implicit edge. Note that e is added only when v and w are cut vertices and both $G _ { i }$ and some $G _ { j }$ are rigid according to Lemma 3. Adding e to $G _ { j } ,$ a redundantly rigid component $C _ { j }$ can be found in $G _ { j } + e$ and $C _ { j }$ contains v and $w ,$ as shown in Fig. 8. We replace e by $C _ { j }$ leading to the graph $G _ { i } + C _ { j } - e ,$ reversing the edge replacement.

First, we need to show that if a vertex u has three nonintersecting paths to B in $G _ { i } + e ,$ there still exist three nonintersecting paths connecting u to B in $G _ { i } + C _ { j } - e .$ . The difficulty is that one of the paths in $G _ { i } ,$ say $p ,$ may contain the implicit edge e that do not appear in $G _ { i } + C _ { j } - e$ . We observe that v and w should be connected in $C _ { j } - e$ since $C _ { j } - e$ is rigid. We replace e by any v  w path in $C _ { j } - e .$ . Since all vertices in the v  w path do not appear in $G _ { i } ,$ , the new path is still nonintersecting with others after the replacement. Second, we need to show that $G _ { i } + C _ { j } - e$ is redundantly rigid. Suppose to the contrary that there exists an edge $e ^ { \prime }$ whose removal results in $G _ { i } + C _ { j } - e$ nonrigid. Both of the end vertices of $e ^ { \prime }$ are in either $G _ { i }$ or $C _ { j } - e .$ . WLOG, we assume $e ^ { \prime }$ in $G _ { i }$ . In this case, $G _ { i } + e - e ^ { \prime }$ cannot be rigid, contradicting that $G _ { i } + e$ is redundantly rigid.

![](images/c7616fcf19ba65b9d6162bd973b0d7b40d818164a11c63f3ae0c276f162fe849.jpg)



(a) Before replacement

![](images/2b3a30ec342616254492f354e8583043350a2e7af51f726469c33c1bc5f3d42c.jpg)



(b) After replacement   
Fig. 8. Reverse process of edge replacement.

![](images/8747be8bdd98be62b73a6f2b608a398d3916bc02ee3f6b9f23165194f64b5b8b.jpg)



Fig. 9. $G ^ { R }$ contains implicit edges.

Theorem 4. In a distance graph $G = ( V , E )$ with a set $B \subset$ V of $k \geq 3$ vertices at known locations, a vertex belongs to the redundantly rigid component containing B in which it has three vertex-disjoint paths to three distinct vertices in B, if and only if it belongs to a globally rigid subgraph of $G ^ { \dot { I } }$ that contains at least three vertices in B, where $\bar { G } ^ { I }$ is the extended distance graph of G.

Proof. (RR3P ) Global Rigidity) We assume G is redundantly rigid but not 3-connected. Based on an edge replacement, both u and B are included in the same subgraph $G _ { i } + e ,$ , where e is an implicit edge of G. If, WLOG say $G _ { 1 } + e ,$ is not 3-connected, it can be further decomposed into several connected components by figuring out a pair of cut vertices in $G _ { 1 } + e .$ . We repeat the edge replacement operations until the remaining graph (containing at least four vertices including u and B) is 3-connected. Note that it is redundantly rigid due to Lemma 3. Since the remaining graph is a subgraph of $G ^ { I } .$ , u belongs to a globally rigid subgraph of $G ^ { \bar { I } }$ .

(RR3P ( Global Rigidity) Let $G ^ { R }$ denote the globally rigid subgraph of $G ^ { I }$ that contains u and B, as shown in Fig. 9. We perform the reverse process of edge replacement on a particular implicit edge e in $\breve { G ^ { R } }$ . According to the previous analysis, this operation preserves the redundant rigidity and connectivity between u and B. By repeatedly replacing the implicit edges in $G ^ { R } ,$ , we finally obtain a redundantly rigid subgraph of G without any implicit edge in which there exist three nonintersecting paths from u to B. tu

Combining Theorem 3 and Theorem 4, we obtain the sufficient condition RR3P. RR3P explains the example in Fig. 4a in which the vertex u is not localizable. Although there exist 3 vertex-disjoint paths from u to 3 beacons, one of them is not included in the redundantly rigid component of u and all beacons. Also, RR3P explains the location uniqueness of u in the example graph shown in Fig. 5a.

So far, we obtain the major result of this study: if a node satisfies the RR3P condition, it is localizable; if a node, on the other hand, does not satisfy the RR-3P condition, it is nonlocalizable. This conclusion answers the fundamental questions about node localizability previously mentioned in the introduction section. Given a specific node, its localizability relies on the property of disjoint paths and redundant rigidity, which can be tested in polynomial time by the network flow algorithm and the pebble game algorithm [9], respectively.

![](images/076d38c0167b24705aa1a9ad5a283bdd0bfbe8f34eb36431d9500c6ae0e5f1e5.jpg)



Fig. 10. System Deployment. The upper right figure shows the encapsulated waterproof sensor mote. The Localizability test is carried out on a particular network instance from the collected data trace. A large portion of nodes are localizable (black) while a small number of border ones (red) are nonlocalizable.

# 5 PERFORMANCE EVALUATIONS

# 5.1 Experiment

To examine the effectiveness, we implement the proposed node localizability testing on the data trace collected from the ongoing sea monitoring system [7], [11], as illustrated in Fig. 10. The system consists of 100 wireless sensors that float on the surface of the sea and collect environmental data such as temperature, humidity, ambient illumination, sea depth, etc. Localization is one of the most important issues in the project since sensory data without locations are almost meaningless. The system also collects the network topology that is dynamic due to ocean current, wind blow, tide, etc.

We equip a small portion of nodes with GPS receivers and adopt the RSS-based ranging technique. Based on these beacons, iterative trilateration is employed as a basic localization scheme. Our proposed localizability algorithm relies on neither any particular localization approach nor any particular ranging technique.

By using the derived conditions, we are able to explore the localizability of the collected network topologies. We observe that, from Fig. 11, almost all the time the network is not entirely localizable. However, a large portion, on average nearly 80 percent, of nodes are actually localizable $( \mathrm { i . e . , }$ identified by the RR3P condition). Specifically, 90 percent of network topologies have at least 60 percent of nodes localizable; and more than 25 percent of topologies have at least 90 percent of nodes localizable. These results suggest the necessity and importance of the concept of node localizability.

![](images/5d88f4edbfb348cd9bd06e2b5b3c0fa3a0cf81a7edcfe4d92b13e4a398bacda0.jpg)



Fig. 11. A large portion of nodes are localizable.

![](images/8a9ef967ff76ca8ec8c0e2bf1cf3d9a8fe6983f1d35e623e479175423e408060.jpg)



Fig. 12. Localizability assists network deployment.

Other than figuring out localizable nodes, being aware of node localizability greatly helps network deployments. Generally speaking, for those nonlocalizable networks, we expect to make them localizable by adjusting some network parameters. Traditional solutions include augmenting ranging capability, increasing node density, or equipping more nodes with GPS. Such measures can be more targeted and effective with the knowledge of node localizability. For example, the adjustments can focus on nonlocalizable nodes only instead of blindly exerting on all nodes.

Similar to existing localization approaches, the improved localization approach can be divided into two stages: data pre-processing and location computation. As a rule, the deployment adjustment is included in the preprocessing stage so as to intensify network localizability or reduce the computation complexity of localization. As shown in Fig. 12, the major difference of the improved flow is that the task of localizability testing is added to assist deployment adjustment. In detail, the testing algorithm is carried out on the initial network deployment and the results are used to instruct the subsequent adjustments.

In the experiment, we enhance distance ranging capability through augmenting signal power. More specifically, we keep those localizable nodes unchanged while increase distance ranging of nonlocalizable ones from 5 to 25 percent.

As shown in Fig. 13a, these changes gradually upgrade the localizability and result in an increasing number of newly localizable nodes. Practically, we augment the ranging capability of all nonlocalizable nodes by 10 percent, which achieves nearly 96 percent of nodes localizable. The node degree varies from 6.2 to 12.4 when we increase the distance ranging by -10 to 25 percent. In the initial deployment, the average node degree is 7.6.

The improved method also decreases interference and energy consumption, which can be recognized by link reducing and energy saving as shown in Fig. 13b. To achieve the same level of localizability, this method requires less number of links by 10 percent than traditional methods when increasing the ranging capability by 5 percent. The improvement is more notable along with the augmentation of ranging capability. It is observed that 30 percent link reduction can be achieved if the ranging capability goes up by 25 percent. The similar trend recurs for energy consumption. To make the nonlocalizable nodes localizable, the improved method no longer blindly augments the ranging capability of all nodes. As a result, more than 90 percent of power consumption is saved, as shown in Fig. 13b. In the experiment, we only consider the power consumption of distance ranging and message exchanges during the network construction and adjustments. We believe that the system can be further benefited than the results shown in Fig. 13b if data communication and retransmissions are taken into consideration.

![](images/a2a6699be5531176b55d576249c25b1cca46972141e31217e8cde9afba937cd7.jpg)



(a) Localizable nodes and average node degree

![](images/4e936eb110819ace807c36536134683e09cc08b4eb0c44c5ec4a9cfe50986ab6.jpg)



(b) Link reducing and energy saving   
Fig. 13. Performance of the improved method.

Due to the characteristics of the project, localization is not a one-time job as in static networks, but one of the major tasks that contributes a considerate amount of workload and power consumption. Assisted by localizability testing, we are able to accurately figure out “location desert” before really carrying out localization, which makes the adjustments of network parameters more targeted and effective. Experiment results show that the improved method not only increases the localizability, but also decreases energy consumption and avoids communication interference and unnecessary redundancy as much as possible.

# 5.2 Large-Scale Simulation

Large-scale simulations are further conducted to examine the scalability of this design under varied network parameters. We randomly generate networks of 400 nodes, uniformly deployed in a unit square ½0; 1 2 . The unit disk model with a radius is adopted for communication and distance ranging. For each evaluation, we integrate results from 100 network instances.

Fig. 14 shows the relationship between connectivity and rigidity. The curve $r _ { i }$ denotes the percentage of i-connected networks in varied radius while $r _ { g }$ denotes globally rigid networks. Like many other properties for random geometric necessary condition 3P and the widely used sufficient condition TRI [12], which is the theoretical upper bound of trilateration-based approaches [13], [14], [15]. Testing TRI is equivalent to find a trilateration ordering of vertices that costs OðnÞ time where n is the number of vertices [12].

![](images/a812757ba4e5a0b2890f1541b39c9145ea7575267f4dd724d7061b6aeeda4a9d.jpg)



Fig. 14. Relationship of connectivity and rigidity.

![](images/b0bf4bafc92f928a8307c451646ec6b265da9798dda6665e3d862e6412d2b99c.jpg)  
(a) Sparse

![](images/8c857da1c306684298942fbfd1bc45b8ae68ab257664469b0e1f00baabd53ce7.jpg)



(a) The capability of 3P and TRI.

![](images/ae6efca4161bc1ae07dbbb48a29b246f65061a4f0b13aaf11afede6fec02ae10.jpg)  
(b) Medium

![](images/25a0ba988f411977eef0265b42e8705111e80b42171ac3c3ddcca694ba921307.jpg)



(b) The capability of RR-3P and RR3P.   
Fig. 16. Comparison between necessary conditions. 3P and RR-3P.

Fig. 15a shows the amount of nodes marked by 3P and TRI. As we know, nodes above the curve of 3P are nonlocalizable while those below the curve of TRI are localizable. In addition, the other ones between two curves are unknown at present based on 3P and TRI. Specifically, almost 70 percent of nodes left unknown at radius 0.18. Contrastively, Fig. 15b shows the results if we adopt the proposed RR-3P and RR3P. Clearly, two curves are close to each other and the gap between them is always narrow along with the variation of network connectivity, indicating a smaller number of nodes whose localizability cannot be determined.

We also study the performance of node localizability for sparsely and moderately connected networks. In this evaluation, the percentage of localizable and nonlocalizable nodes in 100 network instances is shown in Figs. 16 and 17 with communication radius $r = 0 . 1 2$ and 0.16. According to Figs. 16a and 16b, RR-3P and 3P have nearly similar capabilities to recognize nonlocalizable nodes at both sparse and medium network connectivity, except for a few cases in which RR-3P successes much. For sufficient conditions, as shown in Fig. 17a, RR3P identifies 30 percent nodes as

Fig. 15. Improvements of proposed RR-3P and RR3P.

graphs, both connectivity and rigidity have transition phenomena. Also, it can be seen that $r _ { g }$ lies between $r _ { 3 }$ and $r _ { 6 }$ and is closer to $r _ { 3 }$ . This observation reflects the theoretical conclusion that 3-connectivity is a necessary condition while 6-connectivity is a sufficient one for global rigidity.

We then study the improvements of our proposed conditions to existing ones for node localizability. Note that the necessary conditions and the sufficient ones can be used to identify nonlocalizable and localizable nodes in a network, respectively. Other than the proposed RR-3P and RR3P, for comparison, we introduce the best previous localizable while TRI cannot work at all due to sparseness. When $r = 0 . 1 6$ in Fig. 17b, RR3P recognizes, on average, more than 70 percent localizable nodes in 78 cases while TRI only marks less than 10 percent localizable ones in 91 cases. Such observations show that RR3P remarkably outperforms TRI at a specific range of communication radius.

![](images/12df9f095f5c7f1c677caf1a9a2394896e6f35c7eb4f7af11a0099939c4d2957.jpg)



(a) Sparse

![](images/f80bacdab70c86535a0864366e4bc1d55b54659a48583711366bd5e6472d3c73.jpg)



(b) Medium   
Fig. 17. Comparison between sufficient conditions. TRI and RR3P.

We further provide two examples to show how RR-3P and RR3P outperform 3P and TRI. In Fig. 18, a particular network with a “Z” hole is generated in which 400 nodes are randomly distributed. The red dots denote the localizable nodes marked by TRI while blues denote the nonlocalizable nodes marked by 3P. Neither TRI nor 3P can recognize the remaining gray ones. As shown in Fig. 19, similar evaluations are conducted on the same data sets and we use RR3P and RR-3P instead of TRI and 3P, respectively. The comparison between Figs. 18 and 19 suggest that the proposed algorithm successfully step over geographic gaps, such as borders or barriers, and identifies more nodes than previous approaches. We conduct more simulations and the results are consistent, as shown in Figs. 20 and 21.

# 6 RELATED WORK

# 6.1 Localization Literature

Localization is essential for many environment monitoring or surveillance applications [16], [17]. Existing solutions fall into two categories. Range-based approaches assume nodes are able to measure internode distances; while range-free ones merely use neighborhood information.

Many localization algorithms are range-based [1], [14], [18], [19], adopting distance ranging techniques, such as Received Signal Strength (RSS) [2] and Time Difference of Arrival (TDoA) [1]. RSS maps received signal strength to distance according to a signal attenuation model, while TDoA measures the signal propagation time for distance calculation. In practice, RSS-based ranging measurements contain noises on the order of several meters [2]. On the contrast, TDoA is impressively accurate and obtains centimeter accuracy for node separations under several meters in indoor environments [18], [20]. Recent results show that TDoA can further achieve 1-2 cm accuracy within a range of more than ten meters [17], but it often has a much higher cost.

![](images/e7b8d9d99135e5238dbe6623a27a4003815a36c27b73eaedbd5c03045271e1d7.jpg)



(a) Case 1

![](images/526f9328dd7cb691d85e014ded8331201a8490660f8c48196ec0598f044638be.jpg)



(b) Case 2

![](images/a09b889c71015573e7e20782ad9c32cde494c1a13a5cb212b2ae1226ce848df5.jpg)  
(c)Case 3

Fig. 18. Testing 3P and TRI on network instances with “Z” holes.   
![](images/f39628d757d0baa4534ac2187c5d68534dae15f0151c2c86fd348d9118a4d2f6.jpg)



(a) Case 1

![](images/95b677ed77b4cea9d7324a7883d19f204c78205f2077a09fd352a1e15e921995.jpg)  
(b) Case 2

![](images/0e6526198c604c006a99be3168ac53df7a037065342c7001598ead2f8a007e32.jpg)



(c) Case 3   
Fig. 19. Testing RR-3P and RR3P on network instances with $^ { 6 6 } Z ^ { n }$ holes.

![](images/5418121808e4d2e4a76e373345de5a9751fc06540787a2ce500e643c5c937712.jpg)



(a) Case 1

![](images/83b1323c590463ddab2ae1b759f3b4ad7211f0e03a9dd38b5b4a0d7581193e7c.jpg)



(b)Case 2

![](images/31452da33f41017c57251c69afcb9757bf21c6e1bb789675cfc6112d76f5dda8.jpg)  
(c) Case 3   
Fig. 20. Carrying out 3P and TRI on network instances with $" C "$ holes.

The majority of localization algorithms [1], [14], [18], [20] assume a dense network such that iterative trilateration (or multilateration) can be conducted. Other methods [21] record all possible locations in each positioning step and prune incompatible ones whenever possible, which, in the worst case, can result in an exponential space requirement. Besides, some works [3], [8], [22] study the relationship between network localization and rigidity properties of ground truth graphs. Eren et al. [22] propose the concept of localization in subnetworks, which is weaker than the RR3P condition.

Error analysis and control are critical issues for localization. Robust quadrilateral [13] considers the geometric relationship of nodes during positioning, in which trilaterations are used only when they satisfy the robustness condition. The robustness condition is designed based on geometric element (such as line segment and angle) in order to avoid flip ambiguity as much as possible. In addition, the mechanism of error management [23] has been introduced for iterative localization to prevent error propagation.

Due to the hardware limitations and energy constraints of wireless communication devices, range-free approaches are cost-effective alternatives. Most existing range-free approaches largely depend on connectivity measurements with a high density of seeds [24], [25]. They, however, would fail in anisotropic network deployments, where holes exist among nodes. In anisotropic networks [26], the euclidean distances between a pair of nodes may not correlate closely with the hop counts between them because the path connecting them may have to curve around intermediate holes, resulting poor localization accuracy. To deal with such unexpected, a distributed method [27] has been proposed to detect hole boundary by using only the connectivity information. Based on that work, REP [28] partially solves the “distance mismatch” problem in anisotropic networks. Recently, a method [29] of exploring rigid topology structure without distance is proposed which provides a novel view for range-free localization.

The focus of this paper is range-based localization in which the ground truth of network deployments can be modeled by distance graphs.

# 6.2 Graph Rigidity Literature

Graph rigidity has been well studied in mathematics and structural engineering [4], [6], [30], having a surprisingly large number of applications in many areas.

In rigidity literature, many efforts have been made to explore the combinatorial conditions for rigidity. Laman [6] first pointed out that a graph $G = ( V , E )$ is generically rigid if it has a induced subgraph in which edges are “independently” distributed. The statement also leads to an $O ( | V | ^ { 2 } )$ 号 algorithm [9] for rigidity test. For global rigidity, a sufficient and necessary condition [5] is presented based on the results in [4] by combining both redundant rigidity and 3- connectivity. Recently, Jackson and Jordan [31] prove a sufficient condition of six mixed connectivity, which improves a previous result of 6-connectivity by Lovasz and Yemini [32].

![](images/6fd0d52ba0b144b9ffa4478770c7b82c3e9f7e91602811b8632e460e258b5c26.jpg)



(a) Case 1

![](images/d8721d90994e1bd8c85fda04d57ffec433c07c4f94c46418db731f1a85a03c53.jpg)  
(b)Case2

![](images/953344bf073ad19e7951d02284932b2010d49871931439132b76b8e6c9f7c046.jpg)



(c) Case 3   
Fig. 21. Carrying out RR-3P and RR3P on network instances with “C” holes.

There are also some results for random geometric graphs. Assuming the unit disk model, many researchers [33], [34], [35], [36], [37], [38], [39] considered critical conditions for graph connectivity. Simulation results [3] ensure that the hitting radius of global rigidity is between 3- and 6- connectivity in probability sense. In addition, the asymptotic hitting radius for trilateration graphs is given in [3].

# 7 CONCLUSIONS

We analyze the limitations of network localizability and propose a novel concept of node localizability. By deriving the necessary and sufficient conditions for node localizability, we can answer the fundamental questions on localization: which node is indeed localizable in a network. Our designs not only excel previous ones theoretically, but also achieve a decent performance for practical uses.

From intensive simulations, it is observed that there exists a very small portion of nodes cannot be identified as either RR-3P or RR3P condition. We believe that a node is localizable if and only if it can be identified by RR3P. We leave the necessity of RR3P as a future work, which is both challenging and worthwhile.

A direction of future research with good potential is localizability with distance measuring errors. Previous studies have shown that measurement errors play an important role on localization. Some nodes uniquely localizable under perfect distance ranging may suffer from location ambiguities in a practical scenario of ranging errors. We envision this point in order to increase the robustness of localizability testing.

# ACKNOWLEDGMENTS

This work was supported in part by the NSFC Major Program 61190110, the NSFC under grants 61171067 and 61133016, and the National High-Tech R&D Program of China (863) under grant no. 2011AA010100.

# REFERENCES

[1] N.B. Priyantha, A. Chakraborty, and H. Balakrishnan, “The Cricket Location-Support System,” Proc. ACM MobiCom, 2000.   
[2] S.Y. Seidel and T.S. Rappaport, “914 MHz Path Loss Prediction Models for Indoor Wireless Communications in Multifloored Buildings,” IEEE Trans. Antennas and Propagation, vol. 40, no. 2, pp. 209-217, Feb. 1992.   
[3] T. Eren, D.K. Goldenberg, W. Whiteley, Y.R. Yang, A.S. Morse, B.D.O. Anderson, and P.N. Belhumeur, “Rigidity, Computation, and Randomization in Network Localization,” Proc. IEEE IN-FOCOM, 2004.   
[4] B. Hendrickson, “Conditions for Unique Graph Realizations,” SIAM J. Computing, vol. 21, no. 1, pp. 65-84, 1992.   
[5] B. Jackson and T. Jordan, “Connected Rigidity Matroids and Unique Realizations of Graphs,” J. Combinatorial Theory Series B, vol. 94, no. 1, pp. 1-29, 2005.   
[6] G. Laman, “On Graphs and Rigidity of Plane Skeletal Structures,” J. Eng. Math., vol. 4, pp. 331-340, 1970.   
[7] “OceanSense Project,” http://www.cse.ust.hk/\~liu/Ocean/ index.html, 2010.   
[8] D. Goldenberg, A. Krishnamurthy, W. Maness, Y.R. Yang, A. Young, A.S. Morse, A. Savvides, and B. Anderson, “Network Localization in Partially Localizable Networks,” Proc. IEEE INFOCOM, 2005.

[9] D.J. Jacobs and B. Hendrickson, “An Algorithm for Two-Dimensional Rigidity Percolation: The Pebble Game,” J. Computational Physics, vol. 137, pp. 346-365, 1997.   
[10] J.E. Hopcroft and R.E. Tarjan, “Finding The Triconnected Components of a Graph,” Technical Report TR 140, Dept. of Computer Science, Cornell Univ., 1972.   
[11] Z. Yang, M. Li, and Y. Liu, “Sea Depth Measurement with Restricted Floating Sensors,” Proc. IEEE 28th Int’l Real-Time Symp. (RTSS), 2007.   
[12] J. Aspnes, T. Eren, D.K. Goldenberg, A.S. Morse, W. Whiteley, Y.R. Yang, B.D.O. Anderson, and P.N. Belhumeur, “A Theory of Network Localization,” IEEE Trans. Mobile Computing, vol. 5, no. 12, pp. 1663-1678, Dec. 2006.   
[13] D. Moore, J. Leonard, D. Rus, and S. Teller, “Robust Distributed Network Localization with Noisy Range Measurements,” Proc. ACM Second Int’l Conf. Embedded Networked Sensor Systems (SenSys), 2004.   
[14] A. Savvides, C. Han, and M.B. Strivastava, “Dynamic Fine-Grained Localization in Ad-Hoc Networks of Sensors,” Proc. ACM MobiCom, 2001.   
[15] Z. Yang and Y. Liu, “Quality of Trilateration: Confidence Based Iterative Localization,” IEEE Trans. Parallel and Distributed Systems, vol. 21, no. 5, pp. 631-640, May 2010.   
[16] L. Mo, Y. He, Y. Liu, J. Zhao, S. Tang, X.-Y. Li, and G. Dai, “Canopy Closure Estimates with GreenOrbs: Sustainable Sensing in the Forest,” Proc. ACM Seventh ACM Conf. Embedded Networked Sensor Systems (SenSys), 2009.   
[17] M. Li and Y. Liu, “Underground Coal Mine Monitoring with Wireless Sensor Networks,” ACM Trans. Sensor Networks, vol. 5, no. 2, 2009.   
[18] P. Bahl and V.N. Padmanabhan, “RADAR: An In-Building RF-Based User Location and Tracking System,” Proc. IEEE INFO-COM, 2000.   
[19] Z. Yang, Y. Liu, and X.-Y. Li, “Beyond Trilateration: On the Localizability of Wireless Ad-Hoc Networks,” Proc. IEEE INFO-COM, 2009.   
[20] C. Peng, G. Shen, Y. Zhang, Y. Li, and K. Tan, “BeepBeep: A High Accuracy Acoustic Ranging System Using COTS Mobile Devices,” Proc. ACM Int’l Conf. Embedded Networked Sensor Systems (SenSys), 2007.   
[21] D. Goldenberg, P. Bihler, M. Cao, J. Fang, B. Anderson, A.S. Morse, and Y.R. Yang, “Localization in Sparse Networks Using Sweeps,” Proc. ACM MobiCom, 2006.   
[22] T. Eren, W. Whiteley, and P.N. Belhumeur, “Further Results on Sensor Network Localization Using Rigidity,” Proc. European Workshop Sensor Networks, 2005.   
[23] J. Liu, Y. Zhang, and F. Zhao, “Robust Distributed Node Localization with Error Management,” Proc. ACM MobiHoc, 2006.   
[24] T. He, C. Huang, B.M. Blum, J.A. Stankovic, and T.F. Abdelzaher, “Range-Free Localization Schemes in Large Scale Sensor Networks,” Proc. ACM MobiCom, 2003.   
[25] Y. Shang, W. Ruml, Y. Zhang, and M.P.J. Fromherz, “Localization from Mere Connectivity,” Proc. ACM MobiHoc, 2003.   
[26] H. Lim and J.C. Hou, “Localization for Anisotropic Sensor Networks,” Proc. IEEE INFOCOM, 2005.   
[27] Y. Wang, J. Gao, and J. Mitchell, “Boundary Recognition in Sensor Networks by Topological Methods,” Proc. ACM MobiCom, 2006.   
[28] M. Li and Y. Liu, “Rendered Path: Range-Free Localization in Anisotropic Sensor Networks with Holes,” Proc. ACM MobiCom, 2007.   
[29] S. Lederer, Y. Wang, and J. Gao, “Connectivity-Based Localization of Large Scale Sensor Networks with Complex Shape,” Proc. IEEE INFOCOM, 2008.   
[30] W. Whiteley, “Rigidity and Scene Analysis,” Handbook of Discrete and Computational Geometry, J. Goodman and J.O. Rourke, eds., pp. 893-916, CRC Press, 1997.   
[31] B. Jackson and T. Jordan, “A Sufficient Connectivity Condition for Generic Rigidity in the Plane,” Technical Report TR-2008-01, Operations Research Dept., Eotvos Univ., Budapest, 2008.   
[32] L. Lovasz and Y. Yemini, “On Generic Rigidity in the Plane,” SIAM J. Algebraic and Discrete Methods, vol. 3, no. 1, pp. 91-98, 1982.   
[33] C. Bettstetter, “On the Minimum Node Degree and Connectivity of a Wireless Multihop Network,” Proc. ACM MobiHoc, 2002.   
[34] H. Dette and N. Henze, “Some Peculiar Boundary Phenomena for Extremes of rth Nearest Neighbor Links,” Statistics & Probability Letters, vol. 10, no. 5, pp. 381-390, 1990.

[35] P. Gupta and P. Kumar, “Critical Power for Asymptotic Connectivity in Wireless Networks,” Stochastic Analysis, Control, Optimization and Applications, vol. 16, pp. 347-358, 1998.   
[36] X.-Y. Li, Y. Wang, P.-J. Wan, and C.-W. Yi, “Fault Tolerant Deployment and Topology Control for Wireless Ad Hoc Networks,” Proc. ACM MobiHoc, 2003.   
[37] M. Penrose, “The Longest Edge of the Random Minimal Spanning Tree,” Annals of Applied Probability, vol. 7, pp. 340-361, 1997.   
[38] M. Penrose, “On k-Connectivity for a Geometric Random Graph,” J. Random Structures and Algorithms, vol. 15, pp. 145-164, 1999.   
[39] F. Xue and P. Kumar, “The Number of Neighbors Needed for Connectivity of Wireless Networks,” Wireless Networks, vol. 10, no. 2, pp. 169-181, 2004.

![](images/1b0045af0ce02410367958a1c87624a0bd102c5ff0633c7fc7b21aed427b25fe.jpg)



Zheng Yang received the BE degree in computer science from Tsinghua University in 2006 and the PhD degree from the Hong Kong University of Science and Technology (HKUST) in 2010. He is currently with School of Software and the Tsinghua National Laboratory for Information Science and Technology (TNList) at Tsinghua University. His main research interests include wireless ad hoc/sensor networks and pervasive computing. He has published a

number of research papers in highly recognized journals and conferences, including the IEEE/ACM Transactions on Networking, IEEE Transactions on Parallel and Distributed Systems, IEEE Transactions on Mobile Computing, IEEE INFOCOM, IEEE ICDCS, IEEE RTSS, and ACM SenSys. He is a member of the IEEE and the ACM.

![](images/1af75bbfd69b58cdb06518b1a24cd22dbc55d9453fff3f601ff1360c766a0b73.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, and the MS and PhD degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is now the EMC Chair Professor at Tsinghua University, as well as a faculty member with the Hong Kong University of Science and Technology. His research interests include wireless sensor networks, peer-to-peer comput-

ing, and pervasive computing. He is a senior member of the IEEE.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.