# Understanding Node Localizability of Wireless Ad-hoc Networks

Zheng Yang and Yunhao Liu Hong Kong University of Science and Technology {yangzh, liu}@cse.ust.hk

Abstract — Location awareness is highly critical for wireless ad-hoc and sensor networks. Many efforts have been made to solve the problem of whether or not a network can be localized. Nevertheless, based on the data collected from a working sensor network, it is observed that the network is NOT always entirely localizable. Theoretical analyses also suggest that, in most cases, it is unlikely that all nodes in a network are localizable, although a (large) portion of the nodes can be uniquely located. Existing studies merely examine whether or not a network is localizable as a whole; yet two fundamental questions remain unaddressed: First, given a network configuration, whether or not a specific node is localizable? Second, how many nodes in a network can be located and which are them? In this study, we analyze the limitation of previous works and propose a novel concept of node localizability. By deriving the necessary and sufficient conditions for node localizability, for the first time, it is possible to analyze how many nodes one can expect to locate in sparsely or moderately connected networks. To validate this design, we implement our solution on a real-world system and the experimental results show that node localizability provides useful guidelines for network deployment and other location-based services.

# I. INTRODUCTION

The proliferation of wireless and mobile devices has fostered the demand for context-aware applications, in which location is viewed as one of the most significant contexts.

In recent years, several approaches have been proposed for in-network localization, in which some special nodes (called beacons or seeds) know their global locations and the rest determine their locations by measuring the Euclidean distances to their neighbors. Based on distance ranging techniques [17, 19], the ground truth of a wireless ad-hoc network can be modeled by a distance graph G = (V, E), where V denotes the set of wireless communication devices (e.g., laptop, RFID, or sensor node) and there is an un-weighted edge (i, j)∈E if the distance between i and j, denoted by d(i, j), can be measured or both of them are in known locations, e.g., beacon nodes.

For localization, an essential question occurs as to whether or not a network is localizable given its distance graph. This is called the network localizability problem. A graph $G = ( V , E )$ with possible additional constraints I (such as the known locations of some beacon nodes) is localizable if there is a unique location p(v) of every node v such that the distance $d ( u , \nu ) = d ( p ( u ) , p ( \nu ) )$ for all links in E and constraint I is preserved. Previous studies have shown that the network localizability problem is closely related to graph rigidity [3, 7, 9, 12]. Based on rigidity theory, Jackson and Jordan [9] first present the necessary and sufficient condition for network localizability and design a polynomial algorithm for localizability testing.

The above conclusion, however, is NOT the end of the localizability story. This work is motivated by the observation from an ongoing sea monitoring project [1]. We launched a working sensor network consisting of a hundred of nodes continuously collecting scientific data. Due to tide and wind under natural conditions, the network topology is highly dynamic. Checking the collected network trace, to our surprise and disappointment, we find that almost always the network fails to be localizable. Hence, the existing network localizability test only gives the “fail” answer. The situation recurs for static sensor networks: theoretical analyses [6] indicate that, unless networks are highly dense and regular, in most cases, it is unlikely that all nodes in a network are localizable, but a (large) portion of nodes can be uniquely located. Thus, the network localizability testing is meaningless in practice, considering the fact that many applications can function properly as long as a sufficient number of nodes are aware of their locations [6].

Although the theory for network localizability is complete, the following two fundamental questions cannot be answered by existing methods:

1. Given a network configuration, whether or not a specific node is localizable?   
2. How many nodes in a network can be located and which are them?

Answering the above questions not only helps localization itself, but also provides instructive directions to some location-based services, such as topology control, mobility control, and node distribution. Therefore, the node localizability problem is considered in this study, which focuses on the location-uniqueness of a single node. Indeed, network localizability is a special case of node localizability in which all nodes are localizable. Thus, node localizability is a more general issue.

The first major challenge for studying node localizability is to identify uniquely localizable nodes. Following the results for network localizability, an obvious solution is to find a localizable subgraph from the distance graph, and identify all the nodes in the subgraph localizable. Unfortunately, such a straightforward attempt misses some localizable nodes and wrongly identifies them as non-localizable, since some conditions (e.g., 3-connectivity) essential to network localizability are no longer necessary to node localizability. As shown in Figure 1(a), the node u can be uniquely located under this network configuration but not included in the

3-connected component of beacons. The uniqueness of u's location is explained in Figure 1(b) and (c) where we decompose the network into 2 subgraphs. As u connects 2 beacons in the right component, it has 2 possible locations denoted by u and u'. If we adopt u' as its location, it is impossible to embed the left subgraph into the plane. Specifically, the left subgraph has 2 realizations, but neither is compatible with u'. Hence, u is uniquely localizable, although the 3-connectivity property does not hold. Motivated by the example, it is clear that the results derived for network localizability cannot be directly applied and we have to reconsider the conditions for node localizability.

The main contributions of this work are as follows. Motivated by a real deployed sensor network, we analyze the limitations of existing works on or related to node localizability, scattered over different literatures. Based on that, we derive so far the best necessary and sufficient conditions for node localizability which largely improves existing solutions both theoretically and practically. A localizability testing algorithm is accordingly designed, so that it is possible for the first time to observe how many nodes one can expect to be localizable in sparsely or moderately connected wireless networks. To validate this design, prototype implementation and large-scale simulations are conducted to examine the effectiveness and efficiency. Experimental results show that being aware of node localizability provides useful guidelines for network deployment and other location-based services.

The rest of the paper is organized as follows. We discuss the state-of-the-art on network localizability and graph rigidity in Section 2. Necessary and sufficient conditions are presented for node localizability in Section 3 and 4, respectively. The prototype implementation and simulations are discussed in Section 5. We summarize the related work in both network localization and graph rigidity literatures in Section 6, and conclude the work in Section 7.

# II. PRELIMINARY

The ground truth of a network can be modeled by a distance graph G. We assume G is connected and has at least 4 vertices in the following analysis.

A realization of a graph G is a function p that maps the vertices of G to points in a Euclidean space (this study assumes 2-dimension space). Generally, realizations are referred to the feasible ones that respect the pairwise distance constraints between a pair of vertices i and j if the edge (i, $j ) \in E .$ That is to say, $d ( p ( i ) , p ( j ) ) = d ( i , j )$ for all $( i , j ) { \in } E $ . Two realization of G are equivalent if they are identical under translations, rotations, and reflections in 2D plane. A distance graph G has at least one feasible realization which represents the ground truth of the corresponding network. Formally, G is embeddable in 2D space and all pairwise distances are compatible.

A graph is called generically rigid if one cannot continuously deform its realizations while preserving distance constraints [12]. A realization is generic if the vertex coordinates are algebraically independent. Since the set of generic realizations is dense in the realization space, almost all realizations are generic and we omit this word hereafter. A graph is globally rigid if it is uniquely realizable [7].

![](images/fea3ad8a9fa8fec943f76150a26396897d8b336f150cebdbe32ec1c1d81ffde8.jpg)



(a) u is localizable.

![](images/d0ca824bf948c6ab62b45fb83c7425ac4dbb416a4ba8f22474b796aa9a547f7f.jpg)



(b) Graph decomposing.

![](images/45473e0b13d41ba4b1a66c2979ec6bc09371a810d97c3f8c3f00caac04e50db3.jpg)



(c) 2 realizations of the left subgraph.   
Figure 1: An example showing that the result from network localizability fails to identify node u as localizable.

For a distance graph, there are several distinct manners in which the non-uniqueness of realization can appear. A graph that can be continuously deformed while still satisfying all the constraints is said to be flexible, as shown in Figure 2(a); otherwise it is rigid. Hence, rigidity is a necessary condition for global rigidity.

Rigid graphs, however, are still susceptible to discontinuous flex. Specially, they can be subject to flip (or fold) ambiguities in which a set of nodes have two possible configurations corresponding to a “reflection” across a set of mirror nodes (e.g., v and w in Figure 2(b)). This type of ambiguity is not possible in 3-connected graphs. A graph is said to be 3-connected if there does not exist any set of two vertices whose removal disconnects the graph.

Figure 2(c) further shows a 3-connected and rigid graph which becomes flexible upon removal of an edge. After the removal of the edge (u, v), a subgraph can swing into a different configuration in which the removed edge constraint is satisfied and then reinserted. This type of ambiguity is eliminated by redundant rigidity, the property that a graph remains rigid upon removal of any single edge.

Summarizing the above observations, Jackson and Jordan provides the necessary and sufficient condition for global rigidity in the following theorem.

# Theorem 1. [9]

A graph with $n \geq 4$ vertices is globally rigid in 2 dimensions if and only if it is 3-connected and redundantly rigid.

Based on Theorem 1, global rigidity can be tested in polynomial time by combining existing algorithms for rigidity [7, 11] and 3-connectivity [8].

As we know, a globally rigid graph can be uniquely determined if fixing any group of 3 vertices to avoid trivial variation in 2D plane, such as translation, rotation, or reflection. Hence, a network with at least 3 beacons is entirely localizable if and only if its distance graph is globally rigid. For node localizability, however, no such conclusion is presented so far.

![](images/328fba90f1a75b9612683f35f4525b19c0b02995fd87ad66b7e82815b2931ff7.jpg)  
Figure 2: Realization non-uniqueness.

# III. NECESSARY CONDITIONS FOR NODE LOCALIZABILITY

Based on previous studies on network localizability, in this section, we will explore the necessary graph properties for node localizability.

# A. Necessity of 3 Vertex-disjoint Paths

We have observed that some conditions essential to network localizability (e.g., 3-connectivity) are no longer necessary to node localizability.

To deal with the exception shown in Figure 1, Goldenberg et al. [6] propose the first non-trivial necessary condition: if a vertex is localizable, it has 3 vertex-disjoint paths to 3 beacons. We denote such a condition as 3P for short. Suppose a vertex has only 2 vertex-disjoint paths to beacons. It definitely suffers from a potential flip ambiguity by reflecting along the line of a pair of cut vertices. Nevertheless, it is easy to find an example graph in which some non-localizable vertices satisfy the 3P condition.

# B. Necessity of Redundant Rigidity

It is clear that rigidity is necessary but not sufficient for node localizability. As shown in Figure 2(b), the vertex u is non-localizable although the graph is rigid. Generally, for any rigid graph G, almost all realizations of G are not unique if G is not redundantly rigid.

To analyze the necessity of redundant rigidity, we present Lemma 1 which is first proved by Hendrickson [7].

# Lemma 1.

If a graph G is flexible, then for almost all realizations r of G, the finite flexing of r contains a submanifold that is diffeomorphic to the circle.

Inspired by Lemma 1, we explore implicit graph structures and obtain the main result of this section.

# Theorem 2. (Necessity of redundant rigidity)

In a distance graph G = (V, E) with a set B⊂V of k ≥ 3 vertices at known locations, if a vertex is localizable, it is included in the redundantly rigid component that contains B.

Proof: Assume the only interesting case that G is rigid but not redundantly rigid. Suppose RRC is the redundantly rigid component containing B and a vertex u∉RRC. There is an edge e=(v, w) whose removal results in u and B belonging to different rigid components in G-e. Accordingly, there is a continuous flexing in which u changes its location relative to B. By Lemma 1, any realization of G-e contains a submanifold diffeomorphic to the circle. The distance between v and w will be a multi-valued function for almost every point on this circle. Hence, there exists another realization of G-e that keeps the distance value unchanged according to the generic graph assumption. Adding e back, it forms a realization of G in which the location of u is changed. Therefore, u is non-localizable. □

Now we have obtained a better necessary condition for node localizability by combining 3P (3 vertex-disjoint paths) and Theorem 2 (redundant rigidity), which we call RR-3P for short. Clearly, RR-3P is still not sufficient as illustrated in Figure 3(a). Considering the vertex u, it satisfies the RR-3P condition but not localizable due to the discontinuous flexing in which u can reflect along the axis denoted by the dashed line in Figure 3(b).

![](images/32dc261bdd9de8f707062bfd3f0ff0d0a0de5899911b73673f447b158aa994d0.jpg)  
Figure 3: RR-3P is not sufficient.

# IV. SUFFICIENT CONDITIONS FOR NODE LOCALIZABILITY

# A. The Extended Distance Graph

Based on Theorem 1, an obvious sufficient condition to node localizability is as follows: if a vertex belongs to the globally rigid subgraph of G that contains at least 3 beacon vertices, it is uniquely localizable [6]. For convenience, we denote this condition as RRT standing for redundant rigidity and tri-connected.

Note that a localizable vertex does not necessarily satisfy RRT, as shown in Figure 4(a). The graph consists of 3 beacon vertices (denoted by white circles) and 3 non-beacon vertices (denoted by black ones). It is clear that u is not in the 3-connected component of 3 beacon vertices. However u’s location can be uniquely determined under the configuration.

The possible reason is the distance between u and v is actually fixed although no edge connects them. If we add the edge $( u , \nu )$ to $G ,$ , u can be easily identified as localizable since the distances from u to 3 beacon vertices are available. This observation leads us to explore the implicit edges for identifying localizable vertices.

![](images/6291fd9c1ba22b1c219a81cd8747c9654e720ec790e05fa9aeecdbd1adcedd98.jpg)



(a) (u,v) is implicit

![](images/3e90755b335b8f8abe803f7275daa2c5507c499d642ba3b51ca715ba0cc58f14.jpg)



(b) 2 rigid subgraphs   
Figure 4: Implicit edge.

Let R denote the set of all realizations of G. For simplicity, let $d _ { r } ( u , \nu )$ instead of d(r(u), r(v)) denote the Euclidean distance between the two vertices u and v in a specific realization $r \in R$ .

Let $D _ { G } ( u , \nu ) = \bigcup _ { r \in R } d _ { r } ( u , \nu )$ . For a rigid graph G, R is finite although |R| can be exponential to the size of G. As a result, $D _ { G } ( u , \nu )$ is finite since the number of distinct values of $D _ { G } ( u , \nu )$ is at most |R|.

# Definition 1: Implicit edge

In a distance graph $G = ( V , E )$ , an edge (u,v) is implicit if $( u , \nu ) \not \in E$ and in all realizations of G, the distances between u and v are the same.

$\operatorname { I f } \left( u , \nu \right)$ is an implicit edge, it is equivalent to the fact that $D _ { G } ( u , \nu )$ contains a unique value. Based on the concept of implicit edge, we define the extended distance graph of a distance graph.

# Definition 2: Extended distance graph

For a distance graph $G = ( V , E )$ , its extended distance graph is $G ^ { I } = ( V , E \cup \breve { E } ^ { I } )$ where $E ^ { I }$ is a set of implicit edges of G.

For any single implicit edge $e { = } ( u , \nu )$ , adding e to G does not make any change to R since $D _ { G } ( u , \nu )$ contains only one value. Hence, vertices being localizable in $G ^ { I }$ are also localizable in G. Although the set of localizable vertices in $G$ is identical to $G ^ { I } ,$ being aware of $G ^ { I }$ really helps to identify localizable vertices. Recalling the example shown in Figure 4, u can be easily marked as localizable by trilateration in $G ^ { I }$ . Now, the problem becomes finding the implicit edges for a given graph G. Nevertheless, the definition of implicit edges does not really help for actually finding them.

Let $( E _ { 1 } , E _ { 2 } )$ be a partition of $E ( \mathrm { i . e . , } E _ { 1 } \cup E _ { 2 } { = } E$ and $E _ { 1 } \cap E _ { 2 }$ $\scriptstyle = \phi )$ and let $V _ { i }$ be the set of endpoint vertices of all edges in $E _ { i } ,$ $i { = } 1 , 2$ . Normally, there are some vertices $V _ { c }$ covered by both $E _ { 1 }$ and $E _ { 2 }$ so that $V _ { c } { = } V _ { 1 } { \cap } V _ { 2 }$ . For any partition $( E _ { 1 } , E _ { 2 } )$ of $E ,$ $V _ { c }$ contains at least 1 vertex if G is connected, or at least 2 vertices if G is rigid.

# Lemma 2.

In a graph $G = ( V , E )$ with 2 subgraphs $G _ { 1 } = ( V _ { 1 } , E _ { 1 } )$ and $G _ { 2 } =$ $( V _ { 2 } , \bar { E } _ { 2 } )$ , where $( E _ { 1 } , E _ { 2 } )$ is a partition of E, for any 2 vertices $\{ u , \nu \} { \subset V } _ { c }$ , if both u and v belong to a rigid component in $G _ { 1 }$ and a rigid component in $G _ { 2 } ,$ the edge $( u , \nu )$ is implicit if (u, v)∉E.

Proof: First, let d denote the distance between u and v in the ground truth realization of $G ;$ thus, d∈DG(u, v). Second, we want to show that $D _ { G } ( u , \nu )$ contains the only element d. Let $R C _ { 1 }$ and $R C _ { 2 }$ denote the rigid components in $G _ { 1 }$ and $G _ { 2 } ,$ respectively. Since $R C _ { 1 }$ and $R C _ { 2 }$ are rigid, both $D _ { R C 1 } ( u , \nu )$ and $D _ { R C 2 } ( u , \nu )$ are finite. For notation simplicity, we omit $" ( u ,$ $\nu ) "$ hereafter. As $E _ { 1 } \cap E _ { 2 } { = } \phi ,$ , the values in $\dot { D } _ { R C 1 } - \{ d \}$ and $D _ { R C 2 } \mathrm { - } \{ d \}$ are chosen independently in the possible distance space where $D _ { R C 1 }$ and $D _ { R C 2 }$ have measure zero. Hence, for almost every point p in the space, p∈ $\{ D _ { R C 1 } - \{ d \} \}$ implies p∉ $\{ D _ { R C 1 } - \{ d \} \} . \mathrm { A s } D _ { G \subseteq } D _ { R C 1 } \cap D _ { R C 2 } , d$ is the only value in $D _ { G }$ and $( u , \nu )$ is thus implicit if (u, v)∉E. □

Lemma 2 provides an approach to identify implicit edges and it is possible to construct the extended distance graph $\mathbf { \bar { \boldsymbol { G } } } ^ { I }$ . Back to the example shown in Figure 4(a), we decompose the entire graph into two subgraphs, as illustrated in Figure 4(b). Since both subgraphs are rigid, (u, v) is an implicit edge according to Lemma 2.

Combining Theorem 1 and the concept of implicit edges, we achieve the following theorem.

# Theorem 3.

Let $G ^ { I }$ denote the extended distance graph of $G = ( V , E )$ which has a set $B { \subset } V$ of $k \geq 3$ vertices at known locations. If a vertex belongs to a globally rigid subgraph of $G ^ { I }$ that contains at least 3 vertices in B, it is uniquely localizable.

# B. The Sufficiency of RR3P Condition

Theorem 3 provides so far the best sufficient condition for node localizability. However, it requires the knowledge of implicit edges which incurs combinational number of graph partitions. In this section, we propose an equivalent combinatorial condition to Theorem 3 without actually calculating and using implicit edges. Specifically, we want to show that a vertex is localizable if it belongs to the redundantly rigid component of B in which there exists 3 vertex-disjoint paths connecting it to 3 beacon vertices. We call this condition RR3P for short. Note that RR3P is fundamentally different from the previously mentioned RR-3P. RR3P requires the 3 paths strictly residing in the redundantly rigid component to avoid the unexpected case in Figure 3.

Due to the necessity of redundant rigidity, for convenience, we assume G is redundantly rigid; otherwise let G denote the redundantly rigid component of B. If G is 3-connected, it is trivial that all vertices are localizable since G itself is globally rigid, so we focus on the only interesting case that G is not 3-connected. There exist 2 vertices v and w whose removal disconnects G. As a result, as shown in Figure 5, G can be divided into several overlapped and connected components $G _ { i }$ such that

$$
G = \bigcup_ {i} G _ {i} \text {   and   } V (G _ {i} \cap G _ {j}) = \{v, w \} \text {   for   all   } i \neq j.
$$

For any specific $G _ { i } ,$ we replace other components $G _ { j } \left( j { \neq } i \right)$ by an edge $e { = } ( \nu , w )$ . This operation is defined as edge replacement that is essential to the construction of a globally rigid subgraph.

![](images/f327789c9d138e52a1392f9dc12097fa1685381c8d0a763e1b0ec6573dcf7c2d.jpg)



(a) Before replacement.

![](images/a198a66b54ee2f1452fe986f987524464fa8ae12889f0e940294b6becf4fa72c.jpg)  
(b) After replacement.

Figure 5: Edge replacement (1).   
![](images/7bee6c5425abab6afd0680e88d669d1ef26e3337655b4a6a7386ae8b76ea6e11.jpg)



(a) $p _ { 3 }$ traverses beyond

![](images/0e33ee9c5dfeb0dfdc94a34fe72e880e50d073dba3a89471bb8a058f35597b9d.jpg)



(b) A shortcut in $p _ { 3 }$   
Figure 6: Edge replacement (2).

# Lemma 3.

In a graph $G = ( V , E )$ that is redundantly rigid but not 3-connected, there exists a pair of cut vertices $\{ \nu , w \} { \subset V }$ and G can be divided into a number of connected and overlapped subgraphs $G _ { i } .$ . According to edge replacement,

(a) $G _ { i } { + } e$ is redundantly rigid and $e { = } ( \nu ,$ w) is an implicit edge in G if e∉ $E ;$ ;

(b) If a vertex u has 3 vertex-disjoint paths to 3 pairwise connected vertices B in G, u and B are in the same subgraph $G _ { i }$ and there still exist 3 vertex-disjoint paths connecting u to B in $G _ { i } { + } e$ .

Proof: For part (a), suppose to the contrary that for some $i ,$ $G _ { i }$ +e is not redundantly rigid. Thus, there exists some edge $e ^ { \prime }$ in $G _ { i } { + } e$ whose removal results in the remaining graph, $G _ { i } \mathrm { + } e \mathrm { - } e _ { \mathrm { : } } ^ { \prime }$ , non-rigid. Since e cannot be the only one edge whose removal destroys the rigidity of a graph that is not redundantly rigid, we assume e'≠e hereafter. Considering the entire graph $G ,$ as a result, $G { - } e ^ { \prime }$ is not rigid, contradicting the fact that G is redundantly rigid. Hence, $G _ { i } { + } e$ is redundantly rigid. It follows that all $G _ { i }$ are rigid and e is accordingly an implicit edge due to Lemma 2.

For part (b), since B is fully connected, it is entirely included in some $G _ { i } .$ In addition, u is in $G _ { i }$ otherwise it cannot have 3 non-intersecting paths to B. Let ${ p _ { i } } ( i \mathrm { { = } } 1 , 2 , 3 )$ denote 3 vertex-disjoint paths from u to B in G. If none of $p _ { i }$ traverses beyond $G _ { i , }$ then all $p _ { i }$ still exist in $G _ { i } { + } e .$ . Otherwise, WLOG, assume $p _ { 3 }$ traverses $G _ { j } .$ It should enter $G _ { j }$ at one of {v, w} and exit at the other. We make a shortcut by replacing the path segment in $G _ { j }$ by a single edge e, as illustrated in Figure 6(b). The new path still connects u and B and does not intersect the other two paths. Therefore, u has 3 vertex-disjoint paths to B in $G _ { i } { + } e$ . □

Lemma 3 shows that edge replacement preserves the redundant rigidity and connectivity properties in the remaining graph $G _ { i } { + } e _ { \cdot }$

Now we show that the reverse process of edge replacement also preserves the two properties. Suppose $G _ { i } { + } e$ is redundantly rigid and $e { = } ( \nu , w )$ is an implicit edge. Note that e is added only when v and w are cut vertices and both $G _ { i }$ and some $G _ { j }$ are rigid according to Lemma 3. Adding e to $G _ { j } ,$ , a redundantly rigid component $C _ { j }$ can be found in $G _ { j }$ +e and $C _ { j }$ contains v and w. We replace e by $C _ { j }$ leading to the graph

$G _ { i } { + } C _ { j } { - } e$ , reversing the edge replacement.

First, we need to show that if a vertex u has 3 non-intersecting paths to $B$ in $G _ { i } { + } e _ { ; }$ , there still exist 3 non-intersecting paths connecting u to B in $G _ { i } { + } C _ { j } { - } e$ . The difficulty is that one of the paths in $G _ { i , }$ say p, may contain the implicit edge e that do not appear in $G _ { i } { + } C _ { j } { - } e$ . We observe that v and w should be connected in $C _ { j } – e$ since $C _ { j } – e$ is rigid. We replace e by any v-w path in $C _ { j ^ { - } } e$ . Since all vertices in the v-w path do not appear in $G _ { i ; }$ , the new path is still non-intersecting with others after the replacement. Second, we need to show that $G _ { i } { ^ { + } C } _ { j } { - } e$ is redundantly rigid. Suppose to the contrary that there exists an edge $e ^ { \prime }$ whose removal results in $G _ { i } { + } C _ { i } { - } e$ non-rigid. Both of the end vertices of e' are in either $G _ { i } { \bf o r } { \breve { C } } _ { j ^ { - } } e$ WLOG, we assume $e ^ { \prime }$ in $G _ { i } .$ . In this case, $G _ { i } \mathrm { + } e \mathrm { - } e ^ { \uparrow }$ cannot be rigid, contradicting that $G _ { i } { + } e$ is redundantly rigid.

# Theorem 4.

In a distance graph $G = ( V , E )$ with a set $B { \subset } V { \mathrm { o f } } k \geq 3$ vertices at known locations, a vertex belongs to the redundantly rigid component of B in which it has 3 vertex-disjoint paths to 3 distinct vertices in $B _ { z }$ , if and only if it belongs to a globally rigid subgraph of $G ^ { I }$ that contains at least 3 vertices in $B ,$ where $G ^ { I }$ is the extended distance graph of $G .$ .

Proof: (RR3P⇒GR) We assume G is redundantly rigid but not 3-connected. Based on edge replacement, both u and B are included in the same subgraph $G _ { i } { + } e _ { i }$ , where e is an implicit edge of G. If, WLOG say $G _ { 1 } { + } e _ { \mathrm { i } }$ , is not 3-connected, it can be further decomposed into several connected components by figuring out a pair of cut vertices in $G _ { 1 } { + } e$ . We repeat the edge replacement operations until the remaining graph (containing at least 4 vertices including u and $B )$ is 3-connected. Note that it is redundantly rigid due to Lemma 3. Since the remaining graph is a subgraph of ${ \cdot } { G } ^ { I } ,$ u belongs to a globally rigid subgraph of $G ^ { l }$ .

(RR3P⇐GR) Let $\dot { G } ^ { R }$ denote the globally rigid subgraph of $\overleftarrow { G } ^ { I }$ that contains u and $B ,$ , as shown in Figure 8. We perform the reverse process of edge replacement on a particular implicit edge e in $G ^ { R }$ . According to the previous analysis, this operation preserves the redundant rigidity and connectivity between u and B. By repeatedly replacing the implicit edges in $G ^ { R }$ , we finally obtain a redundantly rigid subgraph of G without any implicit edge in which there exist 3 non-intersecting paths from u to B. □

![](images/8c99920700f54567c929ad0e84b5bcdd070a5da330289d56eff112f6d258b5c7.jpg)  
(a) Before replacement

![](images/a451e7f18c2bb1973bca718e37d1cc2463726173b1bf1fdd2146c0872c9eeb1c.jpg)



(b) After replacement

Figure 7: Reverse process of edge replacement.   
![](images/a25d1b537936faeb92dce48a4ce4236c1609397ba77fd49909fd4b0a44f2ce50.jpg)



Figure 8: $G ^ { R }$ contains implicit edges.

Combining Theorem 3 and Theorem 4, we obtain the sufficient condition RR3P. RR3P explains the example in Figure 3(a) in which the vertex u is not localizable. Although there exist 3 vertex-disjoint paths from u to 3 beacons, one of them is not included in the redundantly rigid component of u and all beacons. Also, RR3P explains the location uniqueness of u in the example graph shown in Figure 3(a).

So far, we obtain the major result of this study: if a node satisfies the RR3P condition, it is localizable; if a node, on the other hand, does not satisfy the RR-3P condition, it is non-localizable. This conclusion answers the questions previously mentioned in the introduction section. Given a specific node, its localizability relies on the property of disjoint paths and redundant rigidity, which can be tested in polynomial time by the network flow algorithm and the pebble game algorithm [11], respectively.

# V. PERFORMANCE EVALUATIONS

# A. Experiment

To examine the effectiveness, we implement the proposed node localizability testing on the data trace collected from the ongoing sea monitoring system [1, 21], as illustrated in Figure 9. The system consists of 100 wireless sensors that float on the surface of the sea and collect environmental data such as sea depth, ambient illumination, pollution, etc. Localization is one of the most important issues in the project since sensory data without locations are almost meaningless. The system also collects the network topology that is dynamic due to ocean current, wind blow, tide, etc.

We equip a small portion of nodes with GPS receivers and adopt the RSS-based ranging technique. Based on these beacons, iterative trilateration is employed as a basic localization scheme. Our proposed localizability algorithm relies on neither any particular localization approach nor any particular ranging technique.

By using the derived conditions, we are able to explore the localizability of the collected network topologies. We observe that almost all the time the network is not entirely localizable. However, a large portion, on average nearly 80%, of nodes are actually localizable (i.e., identified by the RR3P condition). Specifically, 90% of network topologies have at least 60% of nodes localizable; and more than 25% of topologies have at least 90% of nodes localizable. These results suggest the necessity and importance of the concept of node localizability.

Other than figuring out localizable nodes, being aware of node localizability greatly helps network deployments. Generally speaking, for those non-localizable networks, we expect to make them localizable by adjusting some network parameters. Traditional solutions include augmenting ranging capability, increasing node density, or equipping more nodes with GPS. Such measures can be more targeted and effective with the knowledge of node localizability. For example, the adjustments can focus on non-localizable nodes only instead of blindly exerting on all nodes.

Similar to existing localization approaches, the improved localization approach can be divided into 2 stages: data pre-processing and location computation. As a rule, the deployment adjustment is included in the pre-processing

![](images/cfa403b0fb9274cb8de02cda0f2527a9069fa48db6f8399194e7a2a3fea8b1db.jpg)



Figure 9: System Deployment. The upper right figure shows the encapsulated waterproof sensor mote. The Localizability test is carried out on a particular network instance from the collected data trace. A large portion of nodes are localizable (black) while a small number of border ones (red) are non-localizable.

![](images/5fb87b91e9d720a394f854724c39edda3b8eb0ccc1c06205dceb48d635880bfe.jpg)



Figure 10: Localizability assists network deployment.

stage so as to intensify network localizability or reduce the computation complexity of localization. As shown in Figure 10, the major difference of the improved flow is that the task of localizability testing is added to assist deployment adjustment. In detail, the testing algorithm is carried out on the initial network deployment and the results are used to instruct the subsequent adjustments.

In the experiment, we increase the distance ranging capability by augmenting signal transmitting power. More specifically, those localizable nodes keep their states unchanged while others augment their distance ranging capability from 5% to 25% stage-by-stage.

As shown in Figure 11(a), these changes gradually upgrade the localizability and results in an increasing number of newly localizable nodes that are previously non-localizable. Practically, we augment the ranging capability of all non-localizable nodes by 10%, which achieves nearly 96% of nodes localizable. The node degree varies from 6.2 to 12.4 when we increase the distance ranging by -10% to 25%. In the initial deployment, the average node degree is 7.6.

The improved method also decreases interference and energy consumption, which can be recognized by link reducing and energy saving as shown in Figure 11(b). To achieve the same level of localizability, this method requires less number of links by 10% than traditional methods when increasing the ranging capability by 5%. The improvement is more notable along with the augmentation of ranging capability. It is observed that 30% link reduction can be achieved if the ranging capability goes up by 25%. The similar trend recurs for energy consumption. To make the non-localizable nodes localizable, the improved method no longer blindly augments the ranging capability of all nodes. As a result, more than 90% of power consumption is saved, as shown in Figure 11(b). In the experiment, we only consider the power consumption of distance ranging and message exchanges during the network construction and adjustments. We believe that the system can be further benefited than the results shown in Figure 11(b) if data communication and re-transmissions are taken into consideration.

Due to the characteristics of the project, localization is not a one-time job as in static networks, but one of the major tasks that contributes a considerate amount of workload and power consumption. Assisted by localizability testing, we are able to accurately figure out "location desert" before really carrying out localization, which makes the adjustments of network parameters more targeted and effective. Experiment results show that the improved method not only increases the localizability, but also decreases energy consumption and avoids communication interference and unnecessary redundancy as much as possible.

# B. Large-scale Simulation

Large-scale simulations are further conducted to examine the scalability of this design under varied network parameters. We randomly generate networks of 400 nodes, uniformly deployed in a unit square [0, 1]2 . The unit disk model with a radius is adopted for communication and distance ranging. For each evaluation, we integrate results from 100 network instances.

We then study the improvements of our proposed conditions to existing ones for node localizability. Note that the necessary conditions and the sufficient ones can be used to identify non-localizable and localizable nodes in a network, respectively. Other than the proposed RR-3P and RR3P, for comparison, we introduce the best previous necessary condition 3P and the widely used sufficient condition TRI, which is the theoretical upper bound of trilateration based approaches. Figure 12(a) shows the amount of nodes marked by 3P and TRI. As we know, nodes above the curve of 3P are non-localizable while those below the curve of TRI are localizable. In addition, the other ones between two curves are unknown at present based on 3P and TRI. Specifically, almost 70% of nodes left unknown at radius 0.18. Contrastively, Figure 12(b) shows the results if we adopt the proposed RR-3P and RR3P. Clearly, two curves are close to each other and the gap between them is always narrow along with the variation of network connectivity, indicating a smaller number of nodes whose localizability cannot be determined.

We also study the performance of node localizability for sparsely and moderately connected networks. In this evaluation, the percentage of localizable and non-localizable nodes in 100 network instances is shown in Figure 13 and Figure 14 with communication radius r=0.12 and 0.16. According to Figure 13(a) and (b), RR-3P and 3P have nearly similar capabilities to recognize non-localizable nodes at both sparse and medium network connectivity, except for a few cases in which RR-3P successes much. For sufficient conditions, as shown in Figure 14(a), RR3P identifies 30% nodes as localizable while TRI cannot work at all due to sparseness. When r = 0.16 in Figure 14(b), RR3P recognizes,

![](images/a1bbe102dbdbd3fb99929ea4b54de8aec6bc27f25f74f4f5a4ae97acc76ef85c.jpg)



(a) Localizable nodes and average node degree

![](images/5bb47b390d547feb9f2aea7f72ab1b139cc11c4487e7fc0980096494c14d5ae9.jpg)



(b) Link reducing and energy saving   
Figure 11: Performance of the improved method.

on average, more than 70% localizable nodes in 78 cases while TRI only marks less than 10% localizable ones in 91 cases. Such observations show that RR3P remarkably outperforms TRI at a specific range of communication radius.

We further provide two examples to show how RR-3P and RR3P outperform 3P and TRI. In Figure 15, a particular network with a “Z” hole is generated in which 400 nodes are randomly distributed. The red dots denote the localizable nodes marked by TRI while blues denote the non-localizable nodes marked by 3P. Neither TRI nor 3P can recognize the remaining gray ones. As shown in Figure 16, similar evaluations are conducted on the same data sets and we use RR3P and RR-3P instead of TRI and 3P, respectively. The comparison between Figure 15 and Figure 16 suggests that the proposed algorithm successfully step over geographic gaps, such as borders or barriers, and identifies more nodes than previous approaches. We conduct more simulations and the results are consistent.

# VI. RELATED WORK

# A. Localization Literature

Localization is essential for many environment monitoring or surveillance applications [13, 15]. Existing solutions fall into two categories. Range-based approaches assume nodes are able to measure inter-node distances; while range-free ones merely use neighborhood information.

Many localization algorithms are range-based [2, 17, 18, 22], adopting distance ranging techniques, such as Radio Signal Strength (RSS) [19] and Time Difference of Arrival (TDoA) [17]. RSS maps received signal strength to distance according to a signal attenuation model, while TDoA measures the signal propagation time for distance calculation. In practice, RSS-based ranging measurements contain noise on the order of several meters [2], especially in rigorous environments. On the contrast, TDoA is impressively accurate and obtains close to centimeter accuracy for node separations under several meters in indoor environments [18, 20]. Recent results show that TDoA can further achieve one or two centimeters accuracy within a range of more than ten meters [17], but it often has a much higher cost.

![](images/86dd9df2e710d5542931e821aaee94db1fe4b402d40ee5cdb2f3c15bd0216140.jpg)



(a) The capability of 3P and TRI.

![](images/3f09dc829b444c59d547d0e3329ac2791ca2173a6ca2dcee71de8179d113ebc8.jpg)  
(a) Sparse

![](images/3bc2865b05d99d058b7f79da0f40c3de92e153bb2c0c5a8aad0c5604b68af974.jpg)



(a) Sparse

![](images/d3b06026289f4b2f2a40588a67053f317d57093a53ac7afda59352da272fa466.jpg)



(b) The capability of RR-3P and RR3P.

![](images/b52f571574dd59e73346ebbbaf84077da636a24df0c07fc47e9e01616d9d6ed1.jpg)  
(b) Medium

![](images/2aa92f1474fd237b9665b744aaf3b315bb336a7cf783c88a2594515d6a5755b4.jpg)



(b) Medium   
Figure 12: Improvements of proposed RR-3P and RR3P.   
Figure 13: Comparison between necessary conditions: 3P and RR-3P.   
Figure 14: Comparison between sufficient conditions: TRI and RR3P.

The majority of localization algorithms [2, 16-18] assume a dense network such that iterative trilateration (or multilateration) can be conducted. Other methods [5] record all possible locations in each positioning step and prune incompatible ones whenever possible, which, in the worst case, can result in an exponential space requirement. Besides, some works [3, 4, 6] study the relationship between network localization and rigidity properties of ground truth graphs. Eren et al. [4] propose the concept of localization in subnetworks, which is weaker than the RR3P condition.

# B. Graph Rigidity Literature

Graph rigidity has been well studied in mathematics and structural engineering [7, 12, 20], having a surprisingly large number of applications in many areas.

In rigidity literature, many efforts have been made to explore the combinatorial conditions for rigidity. Laman [12] first pointed out that a graph G(V, E) is generically rigid if it has a induced subgraph in which edges are “independently” distributed. The statement also leads to an $O ( | V | ^ { 2 } )$ algorithm [11] for rigidity test. For global rigidity, a sufficient and necessary condition [9] is presented based on the results in [7] by combining both redundant rigidity and 3-connectivity. Recently, Jackson and Jordan [10] prove a sufficient condition of 6 mixed connectivity, which improves a previous result of 6-connectivity by [14].

# VII. CONCLUSIONS

We analyze the limitations of network localizability and propose a novel concept of node localizability. By deriving the necessary and sufficient conditions for node localizability, we can answer the fundamental questions on localization: which node is indeed localizable in a network. Our designs not only excel previous ones theoretically, but also achieve a decent performance for practical uses.

A direction of future research with good potential is localizability with distance measuring errors. Previous studies have shown that measurement errors play an important role on localization. Some nodes uniquely localizable under perfect distance ranging may suffer from location ambiguities in a practical scenario of ranging errors. We envision this point in order to increase the robustness of localizability testing.

# ACKNOWLEDGMENT

This work is supported in part by NSFC/RGC Joint Research Scheme N\_HKUST602/08, National High Technology Research and Development Program of China (863 Program) under grant No.2007AA01Z180, National Basic Research Program of China (973 Program) under Grant No.2006CB303000, and NSF China 60970118 and 60736016.

![](images/54a1d6a417fd411cc0dba2e199038c1c9fc4c88d838f3ccf233d344ec3133820.jpg)  
(a) Case 1

![](images/239ffe7fada5f7bec3a06969378c38b292510ebe7f0a8ea4d0968d8c59b2ba77.jpg)



(b) Case 2

![](images/4e889688e5295fcf38a696f3eaa3da8ce2c308065365cbd9d52c555670597ea1.jpg)  
(c) Case 3

Figure 15: Testing 3P and TRI on network instances with “Z” holes.   
![](images/723dd1ebcd35969610990937cf66a44a39e3f53d12991b79303666fbb7323a6d.jpg)



(a) Case 1

![](images/84e3097ae6c33bbe3c76aa9f7c9eb2c7e8ad01a65c4ce3fd9ad47f85199f10e3.jpg)



(b) Case 2

![](images/9cbfb193b966017ef0f8fa7ef11bfab89a66e68ad9989407b63638e1c2e75eb5.jpg)



(c) Case 3   
Figure 16: Testing RR-3P and RR3P on network instances with “Z” holes.

# Reference

[1] "OceanSense Project," in   
http://www.cse.ust.hk/\~liu/Ocean/index.html.   
[2] P. Bahl and V. N. Padmanabhan, "RADAR: An in-building RF-based user location and tracking system," in Proceedings of IEEE INFOCOM, 2000.   
[3] T. Eren, D. K. Goldenberg, W. Whiteley, Y. R. Yang, A. S. Morse, B. D. O. Anderson, and P. N. Belhumeur, "Rigidity, computation, and randomization in network localization," in Proceedings of IEEE INFOCOM, 2004.   
[4] T. Eren, W. Whiteley, and P. N. Belhumeur, "Further results on sensor network localization using rigidity," in Proceedings of European Workshop on Sensor Networks, 2005.   
[5] D. Goldenberg, P. Bihler, M. Cao, J. Fang, B. Anderson, A. S. Morse, and Y. R. Yang, "Localization in sparse networks using sweeps," in Proceedings of ACM MobiCom, 2006.   
[6] D. Goldenberg, A. Krishnamurthy, W. Maness, Y. R. Yang, A. Young, A. S. Morse, A. Savvides, and B. Anderson, "Network localization in partially localizable networks," in Proceedings of IEEE INFOCOM, 2005.   
[7] B. Hendrickson, "Conditions for unique graph realizations," SIAM Journal of Computing, vol. 21, no. 1, pp. 65-84, 1992.   
[8] J. E. Hopcroft and R. E. Tarjan, "Finding The Triconnected Components of a Graph," Department of Computer Science, Cornell University TR 140, 1972.   
[9] B. Jackson and T. Jordan, "Connected rigidity matroids and unique realizations of graphs," Journal of Combinatorial Theory Series B, vol. 94, no. 1, pp. 1-29, 2005.   
[10] B. Jackson and T. Jordan, "A sufficient connectivity condition for generic rigidity in the plane," Operations Research Department, Eotvos University, Budapest TR-2008-01, 2008.   
[11] D. J. Jacobs and B. Hendrickson, "An algorithm for

two-dimensional rigidity percolation: The pebble game," Journal of Computational Physics, vol. 137, no., pp. 346-365, 1997.   
[12] G. Laman, "On graphs and rigidity of plane skeletal structures," Journal of Engineering Mathematics,, vol. 4, no., pp. 331-340, 1970.   
[13] M. Li and Y. Liu, "Underground coal mine monitoring with wireless sensor networks," ACM Transactions on Sensor Networks (TOSN), vol. 5, no. 2, 2009.   
[14] L. Lovasz and Y. Yemini, "On generic rigidity in the plane," SIAM Journal on Algebraic and Discrete Methods, vol. 3, no. 1, pp. 91-98, 1982.   
[15] L. Mo, Y. He, Y. Liu, J. Zhao, S. Tang, X.-y. Li, and G. Dai, "Canopy Closure Estimates with GreenOrbs: Sustainable Sensing in the Forest," in Proceedings of ACM SenSys, 2009.   
[16] C. Peng, G. Shen, Y. Zhang, Y. Li, and K. Tan, "BeepBeep: A high accuracy acoustic ranging system using COTS mobile devices," in Proceedings of ACM SenSys, 2007.   
[17] N. B. Priyantha, A. Chakraborty, and H. Balakrishnan, "The cricket location-support system," in Proceedings of ACM Mobi-Com, 2000.   
[18] A. Savvides, C. Han, and M. B. Strivastava, "Dynamic fine-grained localization in ad-hoc networks of sensors," in Proceedings of ACM MobiCom, 2001.   
[19] S. Y. Seidel and T. S. Rappaport, "914 MHz path loss prediction models for indoor wireless communications in multifloored buildings," IEEE Transactions on Antennas and Propagation, vol. 40, no. 2, pp. 209-217, 1992.   
[20] W. Whiteley, "Rigidity and scene analysis," in Handbook of Discrete and Computational Geometry,, J. Goodman and J. O. Rourke, Eds.: CRC Press, 1997, pp. 893-916.   
[21] Z. Yang, M. Li, and Y. Liu, "Sea depth measurement with restricted floating sensors," in Proceedings of IEEE RTSS, 2007.   
[22] Z. Yang, Y. Liu, and X.-Y. Li, "Beyond trilateration: on the localizability of wireless ad-hoc networks," in Proceedings of IEEE INFOCOM, 2009.