# Detecting Outlier Measurements Based on Graph Rigidity for Wireless Sensor Network Localization

Zheng Yang, Member, IEEE, Chenshu Wu, Student Member, IEEE, Tao Chen, Member, IEEE, Yiyang Zhao, Wei Gong, Member, IEEE, and Yunhao Liu, Senior Member, IEEE

Abstract—A majority of localization approaches for wireless sensor networks rely on the measurements of internode distance. Errors are inevitable in distance measurements, and we observe that a small number of outliers can drastically degrade localization accuracy. To deal with noisy and outlier ranging results, a straightforward method, known as triangle inequality, has often been employed in previous studies. However, triangle inequality has its own limitations that make it far from accurate and reliable. In this paper, we first analyze how much information is needed to identify outlier measurements. Applying the rigidity theory, we propose the concept of verifiable edges and derive the conditions for an edge to be verifiable. On this basis, we design a localization approach with outlier detection, which explicitly eliminates ranges with large errors before location computation. Considering the entire network, we define verifiable graphs in which all edges are verifiable. If a wireless network meets the requirements of graph verifiability, it is not only localizable but outlier resistant as well. Extensive simulations are conducted to examine the effectiveness of the proposed approach. The results show remarkable improvement in location accuracy by sifting outliers.

Index Terms—Localization, outlier detection, verifiability, wireless sensor networks.

# I. INTRODUCTION

HE proliferation of wireless and mobile devices has fostered the demand for context-aware applications, in which location is viewed as one of the most significant contexts. For wireless sensor networks, location information provides essential contexts for data interpretation and network operations.

In recent years, a number of techniques have been proposed for in-network localization, in which a portion of special nodes (called beacons or anchors) know their global locations, and the rest determine their locations by measuring the Euclidean distances to their neighbors. Several distance-ranging methods, such as radio signal strength (RSS) [1] and time difference of

Manuscript received February 16, 2012; revised May 23, 2012 and August 29, 2012; accepted September 6, 2012. Date of publication September 28, 2012; date of current version January 14, 2013. This work was supported in part by the National Natural Science Foundation of China under Grant 61171067, Grant 61133016, Grant 61202487, and Grant 61272429. The review of this paper was coordinated by Dr. G. Mao.

Z. Yang, C. Wu, Y. Zhao, W. Gong, and Y. Liu are with the School of Software and TNList, Tsinghua University, Beijing 100084, China (e-mail: hmilyyz@gmail.com; wucs32@gmail.com; zhaoyiyang@gmail.com; weigongthu@gmail.com; yunhaoliu@gmail.com).

T. Chen is with the Key Laboratory of Information System Engineering, College of Information System and Management, National University of Defense Technology, Changsha 410073, China (e-mail: emilchenn@gmail.com).

Color versions of one or more of the figures in this paper are available online at http://ieeexplore.ieee.org.

Digital Object Identifier 10.1109/TVT.2012.2220790

arrival (TDoA) [2], have been adopted in practical systems. Based on these techniques, the ground truth of a wireless ad hoc network can be modeled as a distance graph $G = \langle V , E , W \rangle$ , where V is the set of wireless nodes, E is the set of links, and W (u, v) is the distance measurement between a pair of nodes u and v. The problem of localization is to figure out the locations of other nodes based on internode distance measurements and global locations of those beacons.

In practice, however, noises and outliers are inevitable in distance ranging. The ranging errors generally come from the following three sources.

Hardware malfunction or failure. Distance measurements are meaningless when encountering hardware malfunction. In addition, incorrect hardware calibration and configuration also deteriorate ranging accuracy, which is hardly emphasized by previous studies. For example, RSS suffers from transmitter, receiver, and antenna variability, and inaccurate clock synchronization results in ranging errors for TDoA.

Environmental factors. RSS is sensitive to channel noise, interference, and reflection, all of which have significant impacts on signal amplitude. The irregularity of signal attenuation, particularly in complex indoor environments, remarkably increases. In addition, the signal propagation speed often exhibits variability as a function of temperature and humidity for the propagation-time-based ranging measurements and cannot be assumed to be constant across a large field.

Adversary attacks. As location-based services become much more prevalent, the localization infrastructure is becoming the target of adversary attacks. By reporting fake location or ranging results, an attacker, e.g., a compromised (malicious) node, can completely distort the coordinate system. Different from the previous cases, the outliers here are intentionally generated by adversaries.

Ignoring the existence of outliers is not a choice to deal with them. To detect outliers, a straightforward solution is to judge graph embeddability based on triangle inequality. A graph-violating triangle inequality is, by no means, embeddable. Triangle inequality, however, has serious drawbacks in the following two aspects.

Coarse granularity. For a triangle $\triangle \mathrm { A B C } , | \mathrm { A B } | = 5 , | \mathrm { A C } | = 5 ,$ , and |BC| = 5. Suppose that, for some reason, the distance between B and C is wrongly measured as 1 or 9, i.e., |BC| = 1 or 9. For both cases, ABC is embeddable, and triangle inequality fails to detect the outlier measurement |BC|. Triangle inequality is only a coarse-grained evidence of the inexistence of outliers and cannot guarantee the correctness of satisfied measurements.

Identification. Triangle inequality only indicates the existence of outliers but cannot identify them. Formally, a triangle that violates this inequality implies that at least one distance measurement is incorrect but does not indicate which distance is the offending one.

Such limitations motivate us to design a novel approach to detect outlier distance measurements beyond triangle inequality. We notice that a network can uniquely be located without using all internode distances. Thus, for a graph G and a pair of neighboring vertices u and v, if $G - ( u , v )$ contains enough correct information on the location u and v, the measured distance between u and v [denoted by $W ( e )$ , where $\boldsymbol { e } = ( u , v ) ]$ is not necessarily used for localization but can further be used for verification. That is, supposing that we intentionally ignore $W ( e )$ , we still have some ideas to figure it out from $G - ( u , v )$ . Such redundant information in internode distances is a good starting point to characterize noises and outliers in distance measurements.

In this paper, we analyze how much information is needed to identify outlier measurements and how to use them. Applying the rigidity theory, we propose the concept of verifiable edges and derive the conditions for an edge to be verifiable. On this basis, we design a localization approach with outlier detection, which explicitly eliminates the rangings with large errors before location computation, thus increasing location accuracy. Considering the entire network, we define verifiable graphs in which all edges are verifiable. If a wireless network meets the requirements of verifiable graph, it is not only localizable but outlier resistant as well. Extensive simulations are conducted to examine the effectiveness of the proposed approach. The results show the remarkable improvements of location accuracy by sifting outliers. To the best of our knowledge, this is the first paper that establishes the theoretical foundation for the outlier detection problem based on the graph rigidity theory.

The rest of this paper is organized as follows. We first summarize the related work in Section II. In Section III, we build the network model and investigate the theory of network localization. Section IV presents the overview of edge verifiability. To identify outliers, we propose the concept of verifiable edges in Section V. The conditions for an edge to be verifiable are also studied in this section. In Section VI, extending the results from a single edge to entire networks, we discuss verifiable graphs. Section VII presents the evaluation results from extensive simulations. Finally, we conclude this paper in Section VIII.

# II. RELATED WORK

# A. Localization Literature

Location information is essential for many environmental monitoring or surveillance applications [17], [18], [33]. According to a comprehensive survey [32], localization provides essential contexts for data interpretation and network operations [34], [35]. Existing solutions fall into two categories: Range-based approaches assume that nodes can measure internode distances, whereas range-free approaches merely use neighborhood information. Many localization algorithms are range based [2], [12], [19], [20], adopting distance-ranging techniques such as RSS [1] and TDoA [12]. RSS maps received signal strength to distance according to a signal attenuation model, whereas TDoA measures the signal propagation time for distance calculation. In practice, RSS-based ranging measurements contain noise on the order of several meters [19], particularly in rigorous environments. In contrast, TDoA is impressively accurate and obtains close-to-centimeter accuracy for node separations under several meters in indoor environments [2], [22]. Due to the hardware limitations and energy constraints of wireless communication devices, range-free approaches are cost-effective alternatives. Most existing rangefree approaches compute node locations according to network connectivity measurements [28], [29].

The majority of localization algorithms [2], [12], [19] assume a dense network such that iterative trilateration (or multilateration) can be conducted. Other methods [23] record all possible locations in each positioning step and prune incompatible ones whenever possible, which, in the worst case, can result in an exponential space requirement. In addition, some works [13], [24], [25] study the relationship between network localization and rigidity properties of ground-truth graphs. Recently, network and node localizability are studied [20], [30] and are applied to aid for localization and deployment in wireless networks [31].

# B. Graph Rigidity Literature

Graph rigidity has been well studied in mathematics and structural engineering [4], [15], [21], having a surprisingly large number of applications in many areas. In the rigidity literature, many efforts have been made to explore the combinatorial conditions for rigidity. Laman [15] first pointed out that a graph $G = ( V , E )$ is generically rigid in 2-D if it has an induced subgraph in which edges are “independently” distributed. The statement also leads to an $O ( | V | ^ { 2 } )$ algorithm [5] for rigidity testing. For global rigidity in 2-D, a sufficient and necessary condition [3] is presented based on the results in [4] by combining both redundant rigidity and 3-connectivity. Recently, Jackson and Jordan [10] have proved a sufficient condition of six mixed connectivity for global rigidity, which improves a previous result of 6-connectivity in [11].

# C. Error-Control Literature

Error management [7] uses error registries to select nodes that participate in the localization procedure based on their relative contribution to the localization accuracy, and [8] requires “robust quadrilaterals” to prevent large location errors that are introduced by flip ambiguities. From the perspective of security, outlier-resistant localization has also been studied. Minimum mean square estimation is used to identify and remove malicious nodes in [8], and least median of squares, which is an estimator with high breakdown point, is adopted in [26]. A speculative filtering algorithm is designed in [9] to detect phantom nodes. Deriving inspiration from robust statistics, the recent work known as snap-inducing shaped residuals (SISR) [27] uses a residual shaping influence function to deemphasize the “bad nodes” and “bad links” during the localization procedure. Although most conventional techniques attempt to realize robust localization with measurement errors based on statistical methods, our approach, edge verification, determinately sifts outlier edges.

![](images/9aadab297a2af44533a2acd6ac6fecabac6dedc182be3322f02c24f4da2ebfe3.jpg)  
Fig. 1. Realization nonuniqueness. (a) Not rigid. (b) Not 3-connected. (c) Not redundantly rigid.

# III. PRELIMINARIES

# A. Network Model

We suppose that each node is located at a distinct location in some region of a plane and associated with a specific set of “neighboring” nodes. Let N be a network of n nodes labeled $v _ { 1 } , v _ { 2 } , \ldots , v _ { n }$ . Let $\pi ( v _ { i } )$ denote the ground-truth position of $v _ { i }$ . In addition, we assume that a small portion of nodes, called beacons, are at known locations.

A network N can be modeled by a distance graph $G =$ $\langle V , E , W \rangle$ , where each vertex $v _ { i } \in V$ denotes a node in the network, and each edge $e \in E$ indicates the neighborhood of its two endpoint nodes. The measured distance between two neighboring nodes (including beacons) is defined by $W ( e )$ (or $W ( v _ { i } , v _ { j } ) )$ for $e = ( v _ { i } , v _ { j } ) \in E$ .

# B. Graph Rigidity and Realization

A realization of a graph G is a pair $( G , p )$ , where $G =$ $\langle V , E , W \rangle$ , and $p$ is a function that maps the vertices in V to points in a Euclidean space (this paper assumes 2-D space). In general, realizations are referred to the feasible ones, in which the pairwise distance constraints between a pair of vertices u and v if $( u , v ) \in E$ are maintained. That $\operatorname { i s } , \| p ( u ) - p ( v ) \| =$ $W ( u , v )$ for all $( u , v ) \in E$ in $( G , p )$ , where $\| \cdot \|$ denotes the Euclidean norm in $\mathbb { R } ^ { d }$ . A distance graph G has at least one feasible realization that represents the ground truth of the corresponding network. Formally, G is embeddable in 2-D space, and all pairwise distance constraints are compatible with each other and can coexist in the embedment.

Two realizations $( G , p )$ and $( G , q )$ are equivalent if corresponding edges have the same lengths, $\mathrm { i . e . , i f } \parallel p ( u ) - p ( v ) \parallel =$ $\| q ( u ) - q ( v ) \|$ holds for all pairs u, v with $( u , v ) \in E$ . The realizations $( G , p ) , ( G , q )$ are congruent if $\| p ( u ) - p ( v ) \| =$ $\| q ( u ) - q ( v ) \|$ holds for all pairs u, v with $u , v \in V$ . This is the same as saying that $( G , q )$ can be obtained from $( G , p )$ by an isometry of $\mathbb { R } ^ { d }$ . We shall say that $( G , p )$ is $g l o b a l l y$ rigid or $( G , p )$ is a unique realization of G if every realization that is equivalent to $( G , p )$ is congruent to $\left( G , p \right) \left[ 3 \right]$ . In other words, a graph is globally rigid if it is uniquely realizable [4]. A realization is generic if the vertex coordinates are algebraically independent. Because the set of generic realizations is dense in the realization space, almost all realizations are generic, and we omit this word hereafter.

There are several distinct manners in which the nonuniqueness of realization can appear. A graph that can continuously be deformed while still satisfying all the constraints is said to be $\begin{array} { r } { \iiint e x i b l e , } \end{array}$ as shown in Fig. 1(a); otherwise it is rigid. Hence, rigidity is a necessary condition for global rigidity. Rigid graphs, however, are still susceptible to discontinuous flex. In particular, they can be subject to flip (or fold) ambiguities in which a set of nodes have two possible configurations that correspond to a “reflection” across a set of mirror nodes [e.g., v and w in Fig. 1(b)]. This type of ambiguity is not possible in 3-connected graphs. A graph is said to be 3-connected if there does not exist any set of two vertices whose removal disconnects the graph. Fig. 1(c) further shows a 3-connected and rigid graph that becomes flexible upon the removal of an edge. After removing edge $( u , v )$ , a subgraph can swing into a different configuration in which the removed edge constraint is satisfied and then reinserted. This type of ambiguity is eliminated by redundant rigidity, the property that a graph remains rigid upon the removal of any single edge.

Summarizing the aforementioned observations, Jackson and Jordan provides the necessary and sufficient condition for global rigidity in the following theorem.

Theorem 1 [3]: A graph with $n \geq 4$ vertices is globally rigid in two dimensions if and only if it is 3-connected and redundantly rigid.

Based on Theorem 1, global rigidity can be tested in polynomial time by combining existing algorithms for rigidity [4], [5] and 3-connectivity [6]. As we know, a globally rigid graph can uniquely be determined if fixing any group of three vertices to avoid trivial variation in 2-D plane, such as translation, rotation, or reflection. Hence, a network with at least three beacons is entirely and uniquely localizable if and only if its distance graph is globally rigid [14].

# IV. OVERVIEW

# A. Outlier Distance Measurement

Given a distance graph $G = \langle V , E , W \rangle$ , W is determined by the observed information, such as measured internode distances and positions of beacons. Because of the presence of noises, those measurements could be corrupted. Formally, for some edge $e = ( u , v ) \in E$ , W (e) is not necessarily identical with the ground-truth distance between nodes u and v, i.e., $\lVert \boldsymbol { \pi } ( \boldsymbol { u } ) - \boldsymbol { \underline { } }$ $\pi ( v ) \|$ . In this paper, we assume that only nonbeacon nodes can produce error measurements. The beacons, with known locations, always broadcast their true position information, resulting in accurate distance measurement.

![](images/7b61005b52eaa510272d03c7df202cadf9fb2e0149c5c151020158c08f086891.jpg)  
(a)

![](images/2183547f81bf9fce06e42e1b606bc36d1f929991319d80128959e8b096544d3d.jpg)  
(b)

![](images/c1bfe07ea75fa762f8ef9fbdd8dbd9472f3163c1904e66f8d4fc270845a25ad8.jpg)  
（c）  
Fig. 2. Three cases of $G - ( u , v ) . ( { \mathrm { a } } ) G - ( u , v )$ is flexible. $( \boldsymbol { \mathsf { b } } ) G - ( u , v )$ is rigid. $( \mathsf { c } ) G - ( u , v )$ is globally rigid.

In general, ranging errors in a localization system are classified into the following two kinds: 1) noisy error and 2) outlier error. Coming from environment factors and computation precision, noisy errors are moderate and predictable. Noisy errors can be alleviated by some optimization approaches such as those in [7]–[9]. By contrast, outlier errors are much severe and more unpredictable, caused by hardware malfunction or failure and adversary attacks. In this paper, we focus on outlier errors that should be eliminated for high-accuracy localization.

Definition 1: Given a distance graph $G = \langle V , E , W \rangle$ , an edge $e = ( u , v ) \in E$ is a normal edge if $W ( e ) = \| \pi ( u ) -$ $\pi ( v ) \|$ ; otherwise, e is an outlier edge.

In this definition, we assume that no ranging noise is contained in normal edges, which proves to be an excellent starting point to characterize outlier measurements. In practice, we introduce error tolerance and define a normal edge e as $| W ( e ) - \| \pi ( u ) - \pi ( v ) \| | < \epsilon$ . The parameter  is dynamically adjusted according to various ranging techniques and application requirements.

Note that an outlier edge is defined based on the groundtruth location π that is unknown. Under noisy measurements, localization produces a feasible solution that fits the distance constraints well. However, the real locations of nodes are still not guaranteed. Without the ground-truth information, we turn to the redundant information of G, which can be used to tell whether an edge is an outlier.

# B. Redundant Information in G

When a node u obtains the distance between itself and one of its neighbors v, how can we know whether this measurement is correct? To verify $\boldsymbol { e } = ( u , v )$ , we need to exploit the remaining graph $G - e$ after the removal of e. If $G - e$ provides enough correct information, it is possible to verify e. In particular, for a realization $\left( G - e , p \right)$ of $G - e ,$ the value of $\| p ( u ) - p ( v ) \|$ can be used to verify e.

The graph $G - e$ falls into three cases, as shown in Fig. 2, where $G - ( u , v )$ means that the subgraph with edge $\boldsymbol { e } = \left( u , v \right)$ is deleted. In the first case, the removal of e results in a flexible graph, in which u and v can continuously deform. Accordingly, in any realization $\left( G - e , p \right)$ ), the value of $\| p ( u ) - p ( v ) \|$ should be within a number of continuous intervals. Taking Fig. 2(a) as an example, $\| p ( u ) - p ( v ) \|$ must satisfy the triangle inequality of both triangles. In the second case, $G - e$ remains rigid, and in any realization $( G - e , p ) , \| p ( u ) - p ( v ) \|$ has a discrete series of values, because $( G - e , p )$ only allows discrete deformations. In Fig. 2(b), u can flip over to the right side, yielding two possible values of $\| p ( u ) - p ( v ) \|$ . In the last case, $G - e$ is globally rigid, and $\| p ( u ) - p ( v ) \|$ has a unique value for all $( G - e , p )$ . Such a unique value, comparing with $W ( e )$ , can be used as an important evidence of outlier existence or inexistence. To summarize, the first two cases indicate whether e is reasonable, i.e., $W ( e )$ in a reasonable range. The third case guarantees the correctness (or incorrectness) of $W ( e )$ . This paper focuses on the third case: $G - e$ is globally rigid, or more rigorously, $\| p ( u ) - p ( v ) \|$ has a unique value over all realizations p of $G - e$ .

# V. VERIFIABLE EDGE

In this section, we analyze how we can determine whether an edge is normal or an outlier without ground-truth information. Applying graph rigidity, we define edge verifiability and study the conditions for an edge to be verifiable.

# A. Definition

For an edge $\boldsymbol { e } = ( u , v )$ , if the internode distance measurements, excluding $W ( e )$ , are sufficient to figure out the distance between u and $v , W ( e )$ is verifiable. We formulate the edge verifiability by utilizing the redundant information in $G$ as follows.

Definition 2: Given a distance graph $G = \langle V , E , W \rangle$ , an edge $e = ( u , v ) \in E$ is referred to as verifiable if $\| p ( u ) -$ $p ( v ) \| = \| q ( u ) - q ( v ) \|$ holds for any two equivalent realizations $\left( G - e , p \right)$ and $( G - e , q )$ of $G - e$ .

Considering an edge $\boldsymbol { e } = ( u , v )$ that is not verifiable, there exist at least two distinct values of $\| p ( u ) - p ( v ) \|$ for all $( G -$ $e , p )$ . Thus, the correctness of $W ( e )$ cannot be judged with assurance.

# B. Conditions for Edge Verifiability

This section discusses the conditions for an edge to be verifiable.

Theorem 2: In a graph $G = \langle V , E , W \rangle$ , an edge $e = ( u , v ) \in$ E is verifiable in $G \operatorname { i f } G - e$ is globally rigid or the two ends u and v are included in at least one globally rigid subgraph of $G - e$ .

Proof: Let C denote one globally rigid subgraph in $G - e$ that contains u and v. By definition, for any two equivalent realizations $( G - e , p )$ and $( G - e , q ) , \| p ( v _ { i } ) - p ( v _ { j } ) \| =$ $| | q ( v _ { i } ) - q ( v _ { j } ) |$  holds for all $( v _ { i } , v _ { j } ) \in E$ and $( v _ { i } , v _ { j } ) \neq ( u , v )$ . Because $C \subset G - e ,$ we have $\| p ( v _ { i } ) - p ( v _ { j } ) \| = \| q ( v _ { i } ) -$ $q ( v _ { j } ) \|$ for all $( v _ { i } , v _ { j } ) \in E ( C )$ . According to the global rigidity of $C ,$ the fact that $\| p ( v _ { i } ) - p ( v _ { j } ) \| = \| q ( v _ { i } ) - q ( v _ { j } ) \|$ for all $( v _ { i } , v _ { j } ) \in E ( C )$ suggests $\| p ( u ) - p ( v ) \| = \| q ( u ) - q ( v ) \|$ , where p and q are any equivalent realizations of $G - e$ . Thus, $\boldsymbol { e } = ( u , v )$ is verifiable by Definition 2.

As illustrated in Fig. 3(a), edge $( u , v )$ , colored in red, is verifiable, because $G - ( u , v )$ is globally rigid. The fact that an edge $\boldsymbol { e } = ( u , v )$ is verifiable does not require $G - e ,$ , even G, to globally be rigid. Theorem 2 only requires the existence of a globally rigid subgraph that contains u and v when $G - e$ is not globally rigid. Fig. 3(b) demonstrates an example of such a situation. In this case, $G - ( u , v )$ is not globally rigid, but $( u , v )$ is verifiable, because u and v are both contained in a globally rigid subgraph $G - ( u , v ) - w$ .

![](images/9644ee5efb8680b43bf6cf58a7ab40e3733f0e1f7a947a8cdbe8365e5f6b6b33.jpg)  
(a)

![](images/89a794f3f690541d410c66f1b3b4379c436ad99b59198f5fcf03d73463238886.jpg)  
(b)

Fig. 3. Two examples of verifiable edges. (a) G and $G - ( u , v )$ are both globally rigid. (b) G and $G - ( u , v )$ are not globally rigid, whereas $G -$ $( u , v ) - w$ is a globally rigid subgraph.   
![](images/b2907579d4ff2e7229f63bb901e0ba412d82494efebf3498fc37a5e3db42edd3.jpg)



(@）

![](images/0cfbe1e9af5f61ed89e91627ac18845df54f16c2031f8fab13e1d4ce3adb9161.jpg)



(b)   
Fig. 4. Edge $( u , v )$ is verifiable, yet the entire graph is not globally rigid and contains no globally rigid subgraphs. (a) G and $\bar { G } - ( u , v )$ are not globally rigid. (b) Distances between u and v are the same in all realizations.

Nevertheless, the condition in Theorem 2 is sufficient but not necessary. In other words, an edge can be verifiable even when the remaining graph contains no globally rigid subgraph that holds the two ends of the edge. As shown in Fig. 4, the graph itself is not globally rigid, and the remaining graph upon the removal of edge $\boldsymbol { e } = ( u , v )$ contains no globally rigid subgraph. However, edge e is verifiable, because the distances between u and v are consistent for all possible realizations of the graph. In other words, $\| p ( u ) - p ( v ) \| = \| q ( u ) - q ( v ) \|$ holds for any two realizations p and q of the graph. Thus, by Definition 2, $\boldsymbol { e } = ( u , v )$ is verifiable. With regard to these cases, the sufficient and necessary conditions of edge verifiability remain an open problem, which should deeply be probed into in future work. In the following context, we exploit the verifiability problem by excluding such cases.

According to Theorem 1, to check the global rigidity of a graph $G = ( V , E )$ , it suffices to test the triconnectivity and redundant rigidity of G. With respect to the triconnectivity, an $O ( | V | + | E | )$ algorithm is designed in [6] using the method of depth-first search (DFS). With regard to redundant rigidity, Hendrickson et al. present an $O ( | V | ^ { \bar { 2 } } )$ ) algorithm in [4] and [5] based on the Pebble game algorithm. Combining Theorems 1 and 2, we present a framework for edge verifiability detection, which is outlined by Algorithm 1. Note that Algorithm 1 not only detects the verifiability of a specific edge but also returns all the globally rigid subgraphs that can verify it. The complexity of finding triconnected components (line 2 in Algorithm 1) is $O ( | V | + | E | )$ . The judgment of edge verifiability based on a set of globally rigid subgraphs (lines 8–12) takes constant time. For each triconnected component $T _ { i }$ with $| V _ { i } |$ vertices, it takes $O ( | V _ { i } | ^ { 2 } )$ time to test the global rigidity (line 4). In the worst case, the vertices u and v are included in all $T _ { i }$ so that the complexity of lines 3–7 will be $\Sigma _ { i } O ( | V _ { i } | ^ { 2 } )$ . Because $T _ { i }$ and $T _ { j } ( i \neq j )$ have at most two common vertices, $\Sigma _ { i } O ( | V _ { i } | ^ { 2 } ) =$ $\dot { O } ( | V | ^ { 2 } )$ . Hence, to sum up, the worst-case running time of Algorithm 1 is $O ( | V | ^ { 2 } )$ .

Algorithm 1: Edge verifiability detection algorithm.

1: $G ^ { \prime } = G - e \quad e = ( u , v )$   
2: Find all triconnected components $T _ { i }$ of $G ^ { \prime } .$   
3: for all $T _ { i }$ that contain u and v do   
4: if $T _ { i }$ is globally rigid then   
5: Add Ti to the globally rigid subgraphs set $C .$   
6: end if   
7: end for   
8: if C is empty then mark e as unverifiable.   
9: else mark e as verifiable.   
10: end if

# VI. VERIFIABLE GRAPHS

In this section, we expand the concept of verifiability from edges to graphs.

# A. Definition

In general, verification should be carried out not only for several specific edges but also for the entire graph. This leads us to the problem of graph verifiability, in which all edges in a graph must be verified, except for the known accurate ones such as the edges that connect two beacons.

Definition 3: Given a distance graph $G = \langle V , E , W \rangle$ , G is verifiable if e is verifiable for all $e \in E$ .

Based on Theorem 2, the endpoints of a verifiable edge $e \in E$ are contained in a globally rigid subgraph in $G - e .$ . We assume that G is globally rigid in this section; otherwise, G is not entirely localizable, and measurement verification for nonlocalizable nodes is less important. If G is globally rigid, we have the following theorem.

Theorem 3: Given a globally rigid graph $G = \langle V , E , W \rangle , G$ is verifiable if and only if $G - e$ is globally rigid for all $e \in E$ .

Proof: Because $G - e$ is globally rigid for all $e \in E .$ , all edges in G are verifiable, and by Definition 3, G is verifiable. For the necessity, we suppose the contrary that $G - e$ is not globally rigid for some edge e. The fact that e is verifiable implies that the endpoints of e must reside in one globally rigid subgraph of $G - e$ . Hence, adding e back, G not being globally rigid is a contradiction. -

# B. Conditions for Graph Verifiability

To check whether a graph is verifiable, the straightforward method is to judge the edge verifiability for all edges in the graph. In the following context, we study the conditions of graph verifiability through general graph properties.

Jackson et al. have presented two sufficient conditions for global rigidity in terms of the network connectivity and vertex degree of G in [10] and [3], respectively.

![](images/450cd8d2d233c87c753b3464930c440fb763ce8d262e3abeadeb860b1f6f6d37.jpg)



(a)

![](images/d0ac9332f453b2dcfb7462dd5d857184b89b7740c00235e7b2886465c453794a.jpg)  
(b)   
Fig. 5. Relationships between degree and global rigidity. (a) G is not globally rigid as it suffers from a flip ambiguity by reflecting along the line $( u , v )$ . $\delta \check { ( } G ) = n / 2 .$ . (b) The remaining graph of G is not globally rigid upon removing any edge. $\dot { \delta } ( G ) = ( n + 1 ) / 2$ .

Lemma 1 [10]: Let $G = ( V , E )$ be a 6-mixed-connected graph. Then, $G - e$ is globally rigid for all $e \in E$ .

Lemma 2 [3]: Let $G = ( V , E )$ be a graph on $n \geq 4$ vertices with $\delta ( G ) \geq ( n + 1 ) / 2$ , where $\delta ( G )$ denotes the minimum degree in G. Then, G is globally rigid.

In Lemma 1, mixed vertex and edge connectivity is used. Let $G = ( V , E )$ be a graph. A pair $( U , D )$ with $U \subset V$ and $D \subset E$ is a mixed cut in G if $G - \dot { U } - \dot { D }$ is not connected. We say that G is 6-mixed-connected if $2 | U | + | D | \geq 6$ for all mixed cuts (U, D) in G. Equivalently, G is 6-mixed-connected if G is 6-edge-connected, $G - v$ is 4-edge-connected for all $v \in V$ , and $G - \{ u , v \}$ is 2-edge-connected for all pairs u, $v \in V$ . We also know that 6-vertex-connectivity is sufficient for 6-mixed-connectivity. Note that, in the graph theory, a graph $G = ( V , E )$ is said to be k-vertex-connected (or k-connected) if the graph remains connected whenever fewer than k vertices are removed from the graph. Similarly, a graph $G = ( V , E )$ is k-edge-connected if G remains connected on the removal of fewer than k edges. We formulate the aforementioned discussions in the following corollaries.

Corollary 1: If a graph G is 6-vertex-connected or 6-mixedconnected, G is verifiable.

The conclusion on vertex connectivity is the best possible and cannot be reduced from six to five. The examples of 5-vertex-connected graphs being not globally rigid are given in [11].

Corollary 2: For a graph $G = \langle V , E , W \rangle$ on $n > 4$ vertices, if $\delta ( G ) \geq ( n + 3 ) / 2$ , where $\delta ( G )$ denotes the minimum degree in G, G is verifiable.

The lower bound on the minimum degree in Lemma 2 is the best possible lower bound, guaranteeing the global rigidity of G, as shown in Fig. 5(a) by two complete graphs of equal size with two vertices in common. It is easily deduced from theh condition of $\delta ( G ) \geq ( n + 3 ) / 2$ that $\delta ( G - e ) \geq ( n + 1 ) / 2$ for any $e \in E$ , which indicates $G - e$ is globally rigid for all $e \in E$ by Lemma 2. Thus, G is verifiable. In the following analysis, we provide a smaller lower bound on the minimum degree of $G ,$ , which ensures its verifiability. For a graph on n vertices, if $n \leq 4 ,$ even the complete graph is not verifiable. If $n = 5 .$ , Fig. 5(b) shows that the minimum degree of 4 is required. Other cases $( n > 5 )$ are complicated and discussed as follows.

Lemma 3: For a graph $G = \langle V , E , W \rangle$ on $n > 5$ vertices, if $\delta ( G ) \geq ( n + 1 / 2$ , where $\delta ( G )$ denotes the minimum degree in $G , G - e$ is globally rigid for all $e \in E$ .

Proof: According to Lemma 2, G is globally rigid as $\delta ( G ) \geq ( n + 1 ) / 2$ . Because $\delta ( G ) \geq ( n + 1 ) / 2$ , we have $\delta ( G - e ) \geq ( n - 1 ) / 2$ , and all but at most two nonadjacent vertices have degree at least $( n + 1 ) / 2$ . To prove that $G - e$ is globally rigid, it suffices to show that $G - e$ is 3-connected and redundantly rigid for all $e = ( u , v ) \in E$ .

3-connectivity. For a contrary, suppose that $G - e$ has a vertex cut of size less than 3. This vertex cut, denoted by C and $| V ( C ) | \leq 2$ divides $G - e$ into a number of overlapped components, which denotes the disconnected components obtained by cutting C plus C. Thus, all overlapped component share common vertices of C. Let H be the one with the minimum number of vertices among all; then, we have $5 \leq 2 | V ( H ) | - | V ( C ) | \leq | V | , { \mathrm { i . e . , ~ } } 3 \leq | V ( H ) | \leq n / 2 +$ 1; otherwise, if $| V ( H ) | > n / 2 + 1$ , the vertex number of $G - e ,$ which is known as $| V | = n$ , will be at least $2 | V ( H ) | - | V ( C ) | > n$ , which is a contradiction. Obviously, H contains at most one of u and $v ;$ otherwise, C is still a cut in $G ,$ and G is not globally rigid. We know that the complete graph of |V | vertices has degree at most $| V | - 1 . \mathrm { ~ I f ~ } | H | \leq ( n - 1 ) / 2 \mathrm { ~ o r ~ } | V ( H ) | = 3 , \delta ( G - e ) \geq$ $( n - 1 ) / 2$ that implies at least one edge that connects a vertex in H (but not in C) and a vertex outside H. Otherwise, $( n - 1 ) / 2 < | V ( H ) | \leq n / 2 + 1$ , and $| V ( H ) | \geq 4$ , because at most one vertex with degree $( n - 1 ) / 2$ and others at least $( n + 1 ) / 2$ in $V ( H )$ , we know that at least one edge connects a vertex in H (but not in C) and a vertex outside H. Both cases contradict that C is a vertex cut. Hence, $G - e$ is 3-connected.

Redundant rigidity. In the following context, we will show that $G - e$ is redundantly rigid. Because G is globally rigid, $G - e$ is rigid. We suppose to the contrary that $H = G -$ $e - f$ is not rigid for some edge $f = ( s , t ) \in E - e$ . We have the following two cases of $\delta ( H )$ .

1) $\delta ( H ) \geq ( n - 3 ) / 2$ . In this case, one vertex has a degree of $( n - 3 ) / 2$ , two vertices have a degree of $( n - 1 ) / 2$ , and other vertices have at least $( n + 1 ) / 2$ .   
2) $\delta ( H ) \geq ( n - 1 ) / 2$ . In this case, four vertices have a degree of $( n - 1 ) / 2$ , and other vertices have at least $( n + 1 ) / 2 .$ .

Define a rigid component of a graph $G = ( V , E )$ to be a maximal rigid subgraph of G. Let C be a rigid component of H with minimum vertices. We know that C contains at most one of s and t. Put $D = H - V ( C )$ . Because distinct rigid components share at most one vertex and the constraints of $\delta ( H )$ , we have $| V ( D ) | \geq 4$ and $| V ( C ) | \leq$ $( n - 1 ) / 2$ (otherwise, $| V ( D ) | < ( n + 1 ) / 2$ , and thus, every vertex in D has at most degree $( n + 1 ) / 2 )$ ). Because C is a rigid component of H, each vertex of $D$ is adjacent to at most one vertex of C in H. Hence, we have the following two cases of δ(D).

1) $\delta ( D ) \geq ( n - 5 ) / 2$ . In this case, one vertex has a degree of $n - 5 / 2$ , two vertices have a degree of $( n - 3 ) / 2$ , and other vertices have at least $( n - 1 ) / 2$ .   
2) $\delta ( D ) \geq ( n - 3 ) / 2$ . In this case, four vertices have a degree of $n - 3 / 2$ , and other vertices have at least $( n - 5 ) / 2 .$ .

In both cases, we can construct a graph D¯ by adding two edges to D such that $\delta ( \bar { D } ) \geq ( n - 1 ) / 2$ . Because $| V ( C ) | \ge 2$ , we have $| V ( D ) | \leq n - 2$ . We may now use induction on n to deduce that $\bar { D } - g$ is globally rigid for any edge $g \in { \bar { D } }$ . Hence, because $| V ( D ) | \geq 4 , \bar { D } - g$ is redundantly rigid and suggests that D is rigid.Because $| V ( D ) | \geq 4$ , considering $| V ( C ) |$ and $\delta ( H )$ , we have the following three cases.

![](images/2c77f6984c387f85a1eee123d79ffbc03bfd39f962dc03c3d68aa145bbedce41.jpg)



(a)

![](images/7835e92847b45935d82d8f84d83f8623dd666eecb41470669a57cfb4cabe5384.jpg)



![](images/7f0b5b56a757d0f5de5aee203a88bfb3072f76a3eabfa50831873cd2a11766b8.jpg)



（c）

![](images/27fb83125d7a15d145c87d479411195fe7eb99f62a39c1a6a001ca48a36ac868.jpg)



(d）

![](images/31a051e5ca950adcc9b05a4590763b25b05d6e4fe90c6898d67fcaed59b0de1c.jpg)



(e）  
Fig. 6. Different cases of H. (a) $| V ( C ) | = 2 $ , and δ(H) ≥ (n − 3)/2. (b) |V (C)| = 2, and δ(H) ≥ (n − 1)/2. (c) |V (C)| = 3, and δ(H) ≥ (n − 3/2. (d) $| \bar { V } ( C ) | = 3 .$ , and δ(H) ≥ (n − 1/2. (e) |V (C)| ≥ 4.

1) $| V ( C ) | = 2$ . We have n $, = | V ( C ) | + | V ( D ) | \geq 6$ . In case of $\delta ( H ) \geq ( n - 3 ) / 2$ , one vertex in C has a degree of at least 3, and the other vertex has a degree of at least 2. In case of $\delta ( H ) \geq ( n - 1 ) / 2$ , both vertices of C have degrees of at least 3. Hence, in both cases, one vertex is adjacent to at least two vertices in D, and one is adjacent to at least one or two vertices in D, as shown in Fig. $6 ( \mathrm { a } ) \mathrm { o r } ( \mathrm { b } )$ . Thus, H is rigid.   
2) $| V ( C ) | = 3$ . We have $n \geq 7$ . In case of $\delta ( H ) \geq$ $( n - 3 ) / 2 ,$ , at least one vertex has a degree at least 4, and the other two vertices have degrees of at least 3 and 2, respectively. Thus, at least one vertex in C is adjacent to two vertices in D, and at least one vertex is adjacent to another vertex in D, as shown in Fig. 6(c). In the other case, $\delta ( H ) \geq ( n - 1 ) / 2$ , all three vertices in C have a degree of at least 3. Thus, all vertices are adjacent to at least one vertex in D (note that there will not be two vertices of C that connect to the same vertex in D, because C is a rigid component), as shown in Fig. 6(d). H is rigid.   
3) $| V ( C ) | \geq 4$ . We know that vertices in C can have degrees of at most $n - 3 / 2$ , because $| V ( C ) | \leq ( n -$ 1)/2. Because C can include at most one of s and t, in both cases of δ(H), at least one vertex in C has a degree at least $( n + 1 ) / 2 .$ , and at least one vertex has a degree at least $( n - 1 ) / 2$ . Thus, the former must be adjacent to at least two vertices in D, and the latter must be adjacent to at least one vertex in D, as shown in Fig. 6(e). Hence, H is also rigid.

In all cases, H is rigid, which is a contradiction.

According to Lemma 3, we formulate the requirements on degree for verifiable graphs as follows.

Theorem 4: For a graph $G = \langle V , E , W \rangle$ on $n > 5$ vertices, if $\delta ( G ) \geq ( n + 1 ) / 2$ , where $\delta ( G )$ denotes the minimum degree in G, then G is verifiable.

# C. Easily Verifiable Graphs

The verification of edges and graphs relies on graph realization. It is usually prerequisite to localize $G - e$ to achieve the value of $\| p ( u ) - p ( v ) \|$ to verify e. However, network localization is an NP-hard problem in general cases, even when networks are localizable. Consequently, a large portion of verifiable graphs are not easily verifiable. Similarly, that an edge e is verifiable does not mean that it can easily be verified in practice, because calculating $\| p ( u ) - p ( v ) \|$ (or, equivalently, localizing $G - e )$ is usually computationally infeasible.

We find that, if $G - e$ is an easily localizable graph such as a trilateration graph (TRI), where all node locations are easily obtained through iterative trilateration, the edge e is easily verified. The basic principle of trilateration is that the position of an object can uniquely be determined by measuring the distances to three reference positions. Theoretically, a trilateration ordering of a graph $G = ( V , E )$ is an ordering $( v _ { 1 } , v _ { 2 } , \ldots , v _ { n } )$ of V , in which the first three vertices are pairwise connected, and at least three edges connect each vertex $v _ { j } , 4 \leq j \leq n$ to the set of the first j − 1 vertices. A graph is a trilateration extension if it has a trilateration ordering. It is shown that trilateration extensions are globally rigid [13], [14].

Definition 4: Graph $G = \langle V , E , W \rangle$ is easily verifiable if $G - e$ is easily localizable for all $e \in E$ .

Similar to trilateration, a quadrilateration graph $G = ( V , E )$ has a quadrilateration ordering $( v _ { 1 } , v _ { 2 } , \ldots , v _ { n } )$ of $V ,$ , in which the first four vertices are pairwise connected, and at least 4 edges connect each vertex $v _ { j } , 5 \leq j \leq n$ to the set of the first $j - 1$ vertices. Using quadrilateration graphs, we have the following theorem.

Theorem 5: If G is a quadrilateration graph, G is easily verifiable.

Theorem 5 holds, because $G - e$ is a TRI if G is a quadrilateration graph.

# D. MGRS

Recall the assumption in Section IV-B that the graph $G - e$ provides enough and correct information to verify e. In practice, however, outlier edges may also be contained in $G - e .$ . Consequently, how we can wisely avoid incorrect information in $G - e$ is a significant issue that lies ahead.

To deal with this problem, we propose the concept of minimally globally rigid subgraph (MGRS). A graph $G = ( V , E )$ is minimally globally rigid if G is globally rigid and no proper subgraph of G is globally rigid. An MGRS is a minimally globally rigid subgraph of G, which will become not globally rigid upon the removal of any vertices or edges. According to the definition, the MGRSs that contain u and v (but no edge $( u , v ) )$ can verify edge $\boldsymbol { e } = ( u , v )$ ; meanwhile, they involve the minimal amount of measurements. This implies that MGRS, to the largest extent, limits the possibility of the existence of outliers in the information for verification. As illustrated in Fig. 7, each $G _ { r }$ indicates such an MGRS of $G - e$ for verifying edge $e = ( u , v ) \in E$ . During the procedure of edge verification, we follow the MGRS rule, which means verifying each edge using one of its MGRSs. Despite the benefit of verification accuracy and reliability, the following two key challenges exist to implement the MGRS rule: 1) how we can find an MGRS that contains both ends of the edge to be verified and 2) if such MGRSs may not be unique.

![](images/a244e3c7c0958e8537a3852dcce51c53b9fcee686182e4dca41748435a891477.jpg)  
(a)

![](images/684bc3e3906fb4805ab9ee40f7c8cf586ec0540191f04122f85849d91252eea3.jpg)



![](images/5a7e788b7f9350961c0693e730a059c901ff377ced52f4ee0636497ac6349e03.jpg)



![](images/7f42ed4bacf50422b51f68135e41c9f10178adad19170a5bd07613011cc80c95.jpg)

![](images/9386de2730ee3174448ae57833b15942971be29b698205140198009cda71521b.jpg)  
(b)   
Fig. 7. MGRS. G is the grounded graph, where the dashed red edge is to be verified. Each $G _ { r }$ indicates an MGRS. (a) MGRS. (b) Nonuniqueness of MGRS.

Multiple MGRSs may result in inconsistent judgments for a specific measurement. In other words, one MGRS may report an edge e as an outlier, whereas MGRS suggests it to be normal. We propose a voting algorithm to deal with the problem, which assigns each judgment a specific weight. In particular, each negative judgment that votes an edge as outlier is assigned with −1 whereas the positive one gets 1. The negative or positive signs of the sum of weights of all judgments indicate whether the measurement is an outlier. The detailed algorithm is outlined in Algorithm $^ { 2 , }$ which is with linear-time complexity in terms of the number of MGRSs.

The other issue, finding a MGRS, is complicated. To the best of our knowledge, there are no existing theories and methods for finding an MGRS yet. In this paper, we tentatively take a globally rigid subgraph that contains relatively fewer vertices and edges instead of the optimal one, which also results in a melioration of using less outlier edges during verification. In particular, we use global rigidity testing methods [4]–[6] to find globally rigid subgraphs and select the minimal one. It is a good direction for future research to establish theoretical foundations and design algorithms for MGRS searching.

![](images/f67f46827df0652bd0c754178ba93060eb2c5fcd8b0101ff28389d78ab3c7db1.jpg)



(a)

![](images/cddbff65080d06a6b06f7ca3adea22076bde47e0b52ebc216a8f5ae9fa21e3db.jpg)



(b)   
Fig. 8. Percentage of verifiable edges in different node densities. (a) Percentage of verifiable edges versus R. (b) Percentage of verifiable edges versus average degree.

# VII. EVALUATION

We evaluate the performance of the proposed edge- and graphverifying approaches through extensive simulations.We randomly generate networks of 100 nodes that are uniformly distributed in a unit square [0, 1] 2. The disk model with a radius is adopted for distance measurement. The communication range is denoted by R. For each network instance, we change the value of R from 0.12 to 0.22 stage by stage, with a step length of 0.04. For each setting, we integrate results from 100 network instances.

Fig. 8 plots the percentage of verifiable edges in different node densities. As shown in Fig. 8(a), more edges are verifiable in denser networks, because sufficient distance constraints are available. To understand the relationship between the average degree and percentage of verifiable edges, Fig. 8(b) shows that only a few edges are verifiable when the average degree is below 4, but the percentage of verifiable edges sharply increases to more than 90% as the average degree grows from 4 to 6. All edges are verifiable when the average degree is about 10.

As a concrete example to show the network topology, we depict an instance of these networks with different node connectivity in Fig. 9, where the blue edges denote globally rigid subgraphs, and the red lines indicate verifiable edges. The node connectivity in Fig. 9(a)-(d) is gradually increased. The percentage of verifiable edges reveals the same trend.

To examine the relationship between node connectivity and graph verifiability, we change the value of R from 0.17 to 0.26 and rerun the simulations. The results are plotted in Fig. 10. When the network is sparse $( R < 0 . 1 7 )$ , no instance is verifiable. The percentage of verifiable graphs increases near linearly as R grows from 0.18 to 0.24. Simulation results also show that all instances are verifiable only when the networks are dense. In Fig. 10(b), all graphs are verifiable when the average degree is more than 14.

Edge verification can be used to sift outlier ranging information and improve the accuracy of localization. We use multilateration as the basic localization method and compare the localization performance of the two strategies of outlier sifting and no sifting. Note that our outlier detection approach works well with arbitrary localization methods. We employ multilateration, because it is widely known and used.

Algorithm 2: Voting algorithm.   
1: $G' = G - e$ $e = (u, v)$ 2: Let $\theta$ be the error tolerance.
3: for all MGRSs $M_{i}$ that contain u and v do
4: Determine the locations $p(u)$ and $p(v)$ in $M_{i}$ .
5: $d_{i} = \|p(u) - p(v)\|$ 6: if $|d_{i} - w(e)| \leq \theta$ then $w_{i} = 1$ 7: else $w_{i} = -1$ 8: end if
9: end for
10: if $\Sigma w_{i} \geq 0$ then mark e as a normal edge
11: else mark e as an outlier
12: end if

![](images/0531c4695747c6afbc9d9db952791112f7954b308ede241c61ee20704e89d680.jpg)



(a)

![](images/6f2acfc24767c044ea473229870ee9a2b3b3b7bb8bdd70b95e6c66ad8be1e40b.jpg)



(b)

![](images/e3d2117870d32f94061e02198ffee7a25d5c8faf8d44e93f1d3e954ee8da3346.jpg)



（c）

![](images/26e34ecbfa6a2d98a0cbd7fc43862a97b6f87f7dd6e9c4fe95082b5798d6f3d5.jpg)



Fig. 9. Network topology.   
![](images/beeb83a1d2802166e8365f6e1bf645404f95b8188195f8d4836db1a92c230d92.jpg)



![](images/6835b9c392a345c3a847de74396da221c063d050b2f164d71e8bd75b2b695f1d.jpg)



Fig. 10. Percentage of verifiable graphs in different node densities. (a) Percentage of verifiable graphs versus R. (b) Percentage of verifiable graphs versus average degree.   
![](images/0ac7878a50335dcaefd9daa3b7ee7b491f579ea89d84b16f1e33f355a66f84e3.jpg)



![](images/7027ae2b683f823746c5a6f1d0bd8383c93c8bdbcc587aca6d3704d8ac8e5fc8.jpg)



(b)   
Fig. 11. Benefit of sifting outliers. (a) b = 0.5. (b) a = 0.1.

Two parameters that influence the localization performance are the percentage of outliers in the graph (denoted by a) and the error of outliers (denoted by b). Let $D _ { 1 }$ denote the measured distance and $D _ { 2 }$ denote the actual distance. We use $| D _ { 1 } - D _ { 2 } | / D _ { 2 }$ to calculate the value of b. We set $a = 0 . 1$ , $b = 0 . 5$ as the basic scenario and change the value of a and b, respectively, to run the simulation. For edges other than outliers, we add a random ranging noise (error tolerance ), which is less than 1% of the actual distance to them. Note that this error tolerance can be changed, and the effect is similar to parameter b.

As shown in Fig. 11, without sifting, the average location error tends to increase as the values of a or b increase. In contrast, the curves labeled Sifting stay almost unchanged, which means that the location error is almost unacted upon on the influence of outlier measurements because most of them are correctly sifted. In addition, the average location error with sifting is much smaller than the location error without sifting. The gap between these two cases reaches up to 40% when $a = 0 . 1$ and when $b = 0 . 5$ .

# VIII. CONCLUSION

To eliminate the negative impact of inaccurate measurements, outlier detection serves as an essential and prior component for all range-based localization approaches. In this paper, we have explored how we can identify outliers by using redundant distance information. Applying the graph rigidity theory, we establish the theoretical foundation of the outlier detection problem and analyze the conditions of a specific measurement being an outlier. The evaluation results show that the proposed method improves the location accuracy by modestly and wisely rejecting outliers during localization.

A direction of future research with good potential is to further exploit the redundant information in a graph, particularly when $G - e$ is not rigid. In this case, the constraints of e are more diversified and complicated. This paper is a good starting point to deterministically apply the graph rigidity theory to identify outlier distance measurements, and we envision that more results will be discovered on this basis.

# REFERENCES

[1] S. Seidel and T. Rappaport, “914-MHz path-loss prediction models for indoor wireless communications in multifloored buildings,” IEEE Trans. Antennas Propag., vol. 40, no. 2, pp. 207–217, Feb. 1992.   
[2] A. Savvides, C. Han, and M. Strivastava, “Dynamic fine-grained localization in ad hoc networks of sensors,” in Proc. ACM MobiCom, 2001, pp. 166–179.   
[3] B. Jackson and T. Jordán, “Connected rigidity matroids and unique realizations of graphs,”J. Comb. Theory, Ser. B, vol. 94, no. 1, pp. 1–29, May 2005.   
[4] B. Hendrickson, “Conditions for unique graph realizations,” SIAM J. Comput., vol. 21, no. 1, pp. 65–84, Feb. 1992.   
[5] B. Hendrickson and D. Jacobs, “An algorithm for two-dimensional rigidity percolation: The pebble game,” J. Comput. Phys., vol. 137, no. 2, pp. 346–365, Nov. 1997.   
[6] J. E. Hopcroft and R. E. Tarjan, “Finding the triconnected components of a graph,” Cornell Univ., Ithaca, NY, Tech. Rep., 1972.   
[7] J. Liu, Y. Zhang, and F. Zhao, “Robust distributed node localization with error management,” in Proc. ACM MobiHoc, 2006, pp. 250–261.   
[8] D. Moore, J. Leonard, D. Rus, and S. Teller, “Robust distributed network localization with noisy range measurements,” in Proc. ACM SenSys, 2004, pp. 50–61.   
[9] J. Hwang, T. He, and Y. Kim, “Detecting phantom nodes in wireless sensor networks,” in Proc. IEEE INFOCOM, 2007, pp. 2391–2395.   
[10] B. Jackson and T. Jordán, “Note: A sufficient connectivity condition for generic rigidity in the plane,” Discrete Appl. Math., vol. 157, no. 8, pp. 1965–1968, Apr. 2009.   
[11] L. Lovász and Y. Yemini, “On generic rigidity in the plane,” SIAM J. Algebr. Discrete Method, vol. 3, pp. 91–98, 1982.   
[12] N. Priyantha, A. Chakraborty, and H. Balakrishnan, “The cricket locationsupport system,” in Proc. ACM MobiCom, 2000, pp. 32–43.   
[13] T. Eren, O. Goldenberg, W. Whiteley, Y. Yang, A. Morse, B. Anderson, and P. Belhumeur, “Rigidity, computation, and randomization in network localization,” in Proc. IEEE INFOCOM, 2004, pp. 2673–2684.   
[14] J. Aspnes, T. Eren, D. Goldenberg, A. Morse, W. Whiteley, Y. Yang, B. Anderson, and P. Belhumeur, “A theory of network localization,” IEEE Trans. Mobile Comput., vol. 5, no. 12, pp. 1663–1678, Dec. 2006.

[15] G. Laman, “On graphs and rigidity of plane skeletal structures,” J. Eng. Math., vol. 4, no. 4, pp. 331–340, Oct. 1970.   
[16] A. Lee, I. Streinu, and L. Theran, “Graded sparse graphs and matroids,” J. Univ. Comput. Sci., vol. 13, no. 11, pp. 1671–1679, 2007.   
[17] M. Li and Y. Liu, “Underground coal mine monitoring with wireless sensor networks,” ACM Trans. Sens. Netw., vol. 5, no. 2, pp. 1–29, Mar. 2009.   
[18] L. Mo, Y. He, Y. Liu, J. Zhao, S. Tang, X. Li, and G. Dai, “Canopy closure estimates with GreenOrbs: Sustainable sensing in the forest,” in Proc. ACM SenSys, 2009, pp. 99–112.   
[19] P. Bahl and V. Padmanabhan, “RADAR: An in-building RF-based user location and tracking system,” in Proc. IEEE INFOCOM, 2000, pp. 775–784.   
[20] Z. Yang, Y. Liu, and X. Li, “Beyond trilateration: On the localizability of wireless ad hoc networks,” IEEE/ACM Trans. Netw., vol. 18, no. 6, pp. 1806–1814, Dec. 2010.   
[21] W. Whiteley, “Rigidity and scene analysis,” in Handbook of Discrete and Computational Geometry, J. Goodman and J. ORourke, Eds. Boca Raton, FL: CRC, 1997, pp. 893–916.   
[22] C. Peng, G. Shen, Y. Zhang, Y. Li, and K. Tan, “BeepBeep: A highaccuracy acoustic ranging system using COTS mobile devices,” in Proc. ACM SenSys, 2007, pp. 1–14.   
[23] D. Goldenberg, P. Bihler, M. Cao, J. Fang, B. Anderson, A. Morse, and Y. Yang, “Localization in sparse networks using sweeps,” in Proc. ACM MobiCom, 2006, pp. 110–121.   
[24] T. Eren, W. Whiteley, and P. Belhumeur, “Further results on sensor network localization using rigidity,” in Proc. 2nd Eur. Workshop IEEE Wireless Sens. Netw., 2005, pp. 405–409.   
[25] D. Goldenberg, A. Krishnamurthy, W. Maness, Y. Yang, A. Young, A. Morse, and A. Savvides, “Network localization in partially localizable networks,” in Proc. IEEE INFOCOM, 2005, pp. 313–326.   
[26] Z. Li, W. Trappe, Y. Zhang, and B. Nath, “Robust statistical methods for securing wireless localization in sensor networks,” in Proc. IEEE IPSN, 2005, pp. 91–98.   
[27] H. Kung, C. Lin, T. Lin, and D. Vlah, “Localization with snap-inducing shaped residuals (SISR): Coping with errors in measurement,” in Proc. ACM MobiCom, 2009, pp. 333–344.   
[28] M. Li and Y. Liu, “Rendered path: Range-free localization in anisotropic sensor networks with holes,” IEEE/ACM Trans. Netw., vol. 18, no. 1, pp. 320–332, Feb. 2010.   
[29] Y. Shang, W. Ruml, Y. Zhang, and M. P. J. Fromherz, “Localization from mere connectivity,” in Proc. ACM MobiHoc, 2003, pp. 201–212.   
[30] Z. Yang and Y. Liu, “Understanding node localizability of wireless ad hoc and sensor networks,” IEEE Trans. Mobile Comput., vol. 11, no. 8, pp. 1249–1260, Aug. 2012.   
[31] T. Chen, Z. Yang, Y. Liu, D. Guo, and X. Luo, “Localization in nonlocalizable sensor and ad hoc networks: A localizability-aided approach,” in Proc. IEEE INFOCOM, 2011, pp. 276–280.   
[32] G. Mao, B. Fidan, and B. D. O. Anderson, “Wireless sensor network localization techniques,” Comput. Netw., vol. 51, no. 10, pp. 2529–2553, Jul. 11, 2007.   
[33] P. Zhou, Y. Zheng, and M. Li, “How long to wait?: Predicting bus arrival time with mobile-phone-based participatory sensing,” in Proc. ACM MobiSys, 2012, pp. 379–392.   
[34] X. Wang, W. Huang, S. Wang, J. Zhang, and C. Hu, “Delay and capacity tradeoff analysis for MotionCast,” IEEE/ACM Trans. Netw., vol. 19, no. 5, pp. 1354–1367, Oct. 2011.   
[35] Y. Liu, Q. Zhang, and L. M. Ni, “Opportunity-based topology control in wireless sensor networks,” IEEE Trans. Parallel Distrib. Syst., vol. 21, no. 3, pp. 405–416, Mar. 2010.

![](images/85dd2f2bbbf123488dd33cb0014e29108742730be2f7e07e6d3df13d65e6a422.jpg)



Chenshu Wu (S’12) received the B.S. degree from Tsinghua University, Beijing, China, in 2010. He is currently pursuing the Ph.D. degree with the Department of Computer Science and Technology, Tsinghua University.

His research interests include wireless ad hoc/ sensor networks and mobile computing.

Mr. Wu is a Student Member of the Association for Computing Machinery.

![](images/ef9f52963fff9ff58248e2fc23ec5543be4e8c80ec4304f1c5ed4670eb22e190.jpg)



Computing Machinery.

Tao Chen (M’12) received the M.S. and Ph.D. degrees in military operational research from the National University of Defense Technology, Changsha, China, in 2006 and 2011, respectively.

He is currently an Assistant Professor with the Key Laboratory of Information System Engineering, College of Information System and Management, National University of Defense Technology. His research interests include wireless sensor networks and data center networking.

Dr. Chen is a member of the Association for

![](images/c122f62df88c2ab80750ad4dd000ff20350078a1aea2c4e0dd565e555f85da97.jpg)



Yiyang Zhao received the B.S. degree from Tsinghua University, Beijing, China, in 1998, the M.Phil. degree from the Chinese Academy of Sciences, Beijing, in 2001, and the Ph.D. degree in computer science from the Hong Kong University of Science and Technology, Kowloon, in 2010.

He is currently with the School of Software, Tsinghua University. His research interests include radio-frequency identification, pervasive computing, distributed systems, embedded systems, and highspeed networking.

Dr. Zhao is a member of the IEEE Computer Society and the Association for Computing Machinery.

![](images/dc170f7bc62ecdf1a8f6a56518946e2100566dd3c862c07bab09bd8cbb8316c8.jpg)



Wei Gong (M’12) received the B.S. degree from Huazhong University of Science and Technology, Wuhan, China, in 2003 and the M.S. and Ph.D. degrees from Tsinghua University, Beijing, China, in 2007 and 2012, respectively.

He is currently a Postdoctoral Fellow with the Tsinghua National Laboratory for Information Science and Technology, Tsinghua University. His research interests include wireless sensor networks, radio-frequency identification systems, and mobile computing.

![](images/618508c2f9f61f4e027f8d1822a77b9f20f69b193617bd539dc19bbd314f29fc.jpg)



Zheng Yang (M’11) received the B.E. degree in computer science from Tsinghua University, Beijing, China, in 2006 and the Ph.D. degree in computer science from the Hong Kong University of Science and Technology, Kowloon, Hong Kong, in 2010.

He is currently an Assistant Professor with the School of Software, Tsinghua University. His research interests include wireless ad hoc/sensor networks and mobile computing.

Dr. Yang is a member of the Association for Computing Machinery.

![](images/04961e130c12a9e82a2b81e18cddd536221e05ee4db4940774365e3152625063.jpg)



Yunhao Liu (SM’12) received the B.S. degree in automation from Tsinghua University, Beijing, China, in 1995 and the MS and Ph.D. degrees in computer science and engineering from Michigan State University, East Lansing, in 2003 and 2004, respectively.

He is currently the EMC Chair Professor with Tsinghua University and a Faculty Member with the Hong Kong University of Science and Technology, Kowloon, Hong Kong. His research interests include wireless sensor networks, peer-to-peer computing, and pervasive computing.