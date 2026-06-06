# Distributed Coverage in Wireless Ad Hoc and Sensor Networks by Topological Graph Approaches

Dezun Dong∗†, Yunhao Liu†§, Kebin Liu‡† and Xiangke Liao∗

∗School of Computer, National University of Defense Technology, China

†Dept. of Computer Science and Engineering, Hong Kong University of Science and Technology

‡Dept. of Computer Science and Engineering, Shanghai Jiaotong University, China

§Tsinghua National Laboratory for Information Science and Technology, China

Abstract—Coverage problem is a fundamental issue in wireless ad hoc and sensor networks. Previous techniques for coverage scheduling often require accurate location information or range measurements, which cannot be easily obtained in resource-limited ad hoc and sensor networks. Recently, a method based on algebraic topology has been proposed to achieve coverage verification using only connectivity information. The topological method sheds some light on the issue of location-free coverage. Unfortunately, the needs of centralized computation and rigorous restriction on sensing and communication ranges greatly limit the applicability in practical large-scale distributed sensor networks. In this work, we make the first attempt towards establishing a graph theoretical framework for connectivity-based coverage with configurable coverage granularity. We propose a novel coverage criterion and scheduling method based on cycle partition. Our method is able to construct a sparse coverage set in a distributed manner, using purely connectivity information. Compared with existing methods, our design has a particular advantage, which permits us to configure or adjust the quality of coverage by adequately exploiting diverse sensing ranges and specific requirements of different applications. We formally prove the correctness and evaluate the effectiveness of our approach through extensive simulations and comparisons with the state-of-the-art approaches.

Keywords-wireless ad hoc and sensor networks; coverage; distributed; connectivity; topological graph; cycle partition;

# I. INTRODUCTION

Wireless ad hoc and sensor networks are emerging as promising techniques for many important applications such as homelands security, military surveillance, environmental monitoring, target detection and tracking, traffic control etc. In such sensing applications, each node is only capable of sensing specific events in its vicinity and of communicating with adjacent nodes. Thus, a sensing system often involves a large number of sensing platforms distributed in a geographical area to collaborate in an ad hoc manner. As a fundamental measurement for understanding and prediction of sensing performance, coverage problem focuses on characterizing how well a region of interest is monitored by a set of working nodes. A lot of recent studies have been carried out to address this problem in large-scale wireless ad hoc and sensor networks [1] [2] [3] [4].

Most existing studies address the coverage problem mainly by employing the computational geometry methodology. Those algorithms assume the accurate node coordinates are available, and thus can determine the coverage by geometric tools, such as well-known Delaunay triangulations, Voronoi diagrams, and geometric disk graphs etc. [1] [2]. The assumption on accurate coordinates, on one hand, makes the coverage problem more tractable and enables the design of efficient distributed or localized coverage algorithms. On the other hand, it substantially limits the applicability of those methods because acquiring accurate location information is practically difficult and expensive for large-scale ad hoc networks. First, accurate location measurement requires a large subset of nodes equipped with special hardware like high-precision GPS and ranging devices. Second, networked localization algorithms often output probabilistic results as they suffers from computational complexity, error accumulation, and flip ambiguity etc. As a result, in practice, only partial location information with errors is available. It is necessary to relax the strong assumption on location measurements to enhance the applicability of coverage algorithms in resource-limited wireless ad hoc and sensor networks.

Recently, a considerable attention has been devoted to location-free coverage algorithms. Those methods make successful attempts towards coverage verification or scheduling, either using range measurements [5] [6] [7] [4] or only connectivity information [8] [9] [10]. Those methods, however, still have serious limitations. Those range-based coordinatefree methods [7] [4] make efforts to relax the restriction of global coordinates by using local relative distances between neighboring nodes. The dependence on precise range measurements still makes those range-based methods remarkably costly. The first purely location-free coverage method is proposed by Ghrist et al. [8] [9]. As a pioneer work, Ghrist et al.’s method lifts the connectivity graph into a topological space, simplicial complex, and determines the coverage by verifying whether the first (relative) homology group of the simplicial complex is trivial. Their method utilizes only connectivity information to achieve provable full blanket coverage in specific sensing ranges and communication model of unit disk graph (UDG). The limitations of their method are mostly in the following three aspects. First, their method depends on purely centralized computation, which makes it restricted and impractical in large-scale ad hoc and sensor networks. Second, although the testing condition based on the first homology group does guarantee the coverage, it is a relatively strong condition, and may introduce false positives, that is, a full coverage network is mistakenly estimated to contain coverage holes. Third, their method inherently constrains that the minimum coverage granularity has to be triangle, which may cause unnecessary wastes in many practical networks with relatively large sensing ranges. Hence, it is of great interests to design a location-free coverage scheme that can be performed in a distributed manner, using only connectivity information and admitting flexible and adjustable coverage granularity.

In this design, we make the first attempt towards establishing a graph theoretical framework to achieve distributed connectivity-based coverage with configurable coverage granularity. The main contributions of this work are as follows. We establish a graph theoretical criterion for coverage determination. Our criterion utilizes the cyclepartition techniques and relaxes the coverage criterion of homology group proposed by Ghrist et al., meanwhile it still can guarantee the coverage sufficiently. We propose a practical distributed algorithm to construct a sparse coverage set. Our algorithm has our desirable and novel characteristics: using only connectivity information, not forcing the communication model to be unit disk graph, using local connectivity to test coverage redundancy, and providing on-demand configurable coverage granularity. We formally prove the correctness of our method and show the effectiveness by extensive simulations.

The remainder of this paper is organized as follows. We discuss related work in Section II, and formulate the problem in Section III. Section IV presents the graph theoretical coverage criterion, and Section V gives the design and implementation of the distributed scheduling algorithm. We present the evaluation in Section VI and conclude this work in Section VII.

# II. RELATED WORK

The coverage problem, as one of the most fundamental issues, has recently attracted significant research attention in ad hoc and sensor networks. We classify the existing coverage methods into two categories: the location-based and location-free, according to whether dependent on location information. Location-free methods further can be classified into two types: the range-based and connectivitybased. We here pay more attention on connectivity-based methods as our work is in this category. More details about range-based methods can be found in recent works [6] [7] [4] and location-based methods can be referred to the good surveys, such as [11] and [12].

We first simply introduce the main ideas of connectivitybased method presented by Ghrist et al. [8] [9], and analyze its advantages and shortages. Their method models the network as a 2-simplicial complex. In algebraic topology, simplicial complexes are well-defined blocks for building topological spaces. A k-simplex σ is a set of $k + 1$ size. A simplicial complex K is a collection of simplices that satisfies the following conditions: (1) Any face of a simplex from K is also in $\kappa ;$ (2) The intersection of any two simplices $\sigma _ { 1 } , \sigma _ { 2 } \in \mathcal { K }$ is a face of both $\sigma _ { 1 }$ and $\sigma _ { 2 } .$ In this coverage problem, we can simply consider the 0, 1, and 2-simpliecs to be vertices, edges, and triangles in the connectivity graph, respectively. Ghrist et al.’s method mainly explores the observation that if the relationship between sensing range $R _ { s }$ and communication range $R _ { c }$ satisfies a specific condition, $R _ { s } \geq 1 / \sqrt { 3 } R _ { c }$ , a connectivity triangle guarantees a coverage region without holes. Further, a full coverage can be verified by the trivial first (relative) homology group of this 2- simplicial complex. A connected simplicial complex having a trivial homology group means that each cycle in the graph can be continuously transformed into a point by moving along faces (edges or triangles) of the simplicial complex without leaving the space.

Compared with previous location-based and range-based methods, Ghrist et al.’s method has its unique advantages that is it avoids both location information and range measurements, which makes their approach robust to situations in which geometric information is missing or is only partially available. Their method, however, still has several limitations that hinder its practicality in wireless ad hoc and sensor networks. First, the verification of first homology group requires global connectivity and a purely centralized computation, which greatly restricts its applicability in distributed wireless networks. Second, the testing of homology group indeed is a rather strong condition, which can lead to that a full coverage network is mistakenly recognized as a network containing coverage holes. One simple example is given to concretely explain such failure cases in Section IV-B. Third, Ghrist et al.’s method inherently constrains that the basic coverage unit has to be triangle, which forces the coverage algorithm to schedule additional nodes and causes unnecessary resource waste in many practical scenarios, as discussed in Section III-C.

# III. PROBLEM FORMULATION

In this section, we present the basic network configuration and assumptions, and formulate a connectivity-based coverage as a confine coverage.

# A. Network Models

We consider a collection of nodes deployed over a plane region. Each node can sense specified events in its sensing range $R _ { s }$ . The union of sensing region of all nodes is referred as the network sensing area, $A _ { n e t }$ , and it covers the target region that needs to be monitored by the network, referred to as the target area, $A _ { t a r }$ , which is typically and significantly larger than the sensing range of a single node. A coverage hole is a connected planar region in the target area that cannot be uncovered by sensing nodes. Each node is only capable of communicating with adjacent nodes in its proximity, within the maximum communication range $R _ { c }$ . Note that we do not force the communication model to be the unit disk graph. Two nodes can or can not communicate with each other if their distance is within the maximum communication range $R _ { c }$ . We assume that the coordinates of nodes are unavailable, in the sense that nodes can determine neither distances nor orientations of other nodes. We use G to denote the connectivity graph of a network communication.

We assume that there is a periphery band of width at least $R _ { c }$ between the boundary of the network sensing area $A _ { n e t }$ and the edge of the target area $A _ { t a r }$ . We refer boundary nodes as those that are located in the periphery band and the others as internal nodes. Although the nodes are not aware of their locations, each node can be assumed to know whether it is a boundary or an internal node by using the mechanisms, like location-free boundary recognition [13] [14], or many other ways discussed in [7]. Note that this is a conventional assumption adopted by almost all existing connectivitybased methods [9] [10], and range-based methods [7] [4]. Note that this work indeed does not need to know the boundary cycles explicitly, and only requires that the graph induced by nodes in one boundary is connected and contain a boundary cycle implicitly. By default, the boundaries in this work are found by a modified fine-grained boundary algorithm [13].

# B. Confine Coverage

Coverage problems have been formulated in different manners in varied applications, including, blanket, point, and barrier coverage, etc. The goal of blanket (or point) coverage focuses on covering all points (or some given points) in an area, while barrier coverage seeks to minimize the probability of undetected network penetrations. Blanket coverage is mainly required in those monitoring applications that need information of all points in the target area or demand immediate response to detected events. Energy efficiency is widely accepted as one of the most critical issues in wireless ad hoc and sensor networks. Always-on full blanket coverage will exhaust network energy rapidly, which is considered to be too expensive in long-duration large-scale applications. Thus, as a practical relaxation of blanket coverage, partial coverage is explored to balance event detection quality and power conservation by many applications, such as, movement target surveillance [15], rare-event detection [16], delay of intrusion detection [17], and trap coverage [18] etc. For example, in the applications like surveillance and target tracking, the metric of quality surveillance is based on the maximum distance that a moving target can travel in the network along a straight line while escaping from detection. In the applications of environment monitoring (such as chemistry pollution of air, water, soil, etc.), the monitoring quality often is measured by the maximum diffusion area of events before detection. Those applications do not pursue zero response time or demand information of all points in the sensing field, and they are tolerant of event detection with moderating delay or small probability of missing to improve the network lifetime.

Partial coverage can be regarded as a generalized blanket coverage with permitting adjustable quality of coverage. The quality of coverage (QoC) of partial coverage is measured in different definitions, such as worst-case detection delay and diffusion area of events mentioned previously. This work adapts a universal metric for QoC by the diameter of coverage hole. A diameter of a coverage hole is defined as the diameter of the minimum circle circumscribing the coverage hole, which is delicately different from the hole diameter in trap coverage [18]. Clearly, the diameter of a coverage hole sufficiently bounds the maximum straight-line distance of escaping detection in the coverage hole, and also provides an diameter to calculate the upper bound of hole area. The worst-case quality of coverage is defined as the maximum diameter of coverage holes in the network. Blanket coverage can be regarded as a special partial coverage with zero worst-case QoC. Similar to blanket coverage, most existing partial coverage schemes also require location information to schedule nodes to guarantee worst-case QoC [15] [19]. Some schemes focus on deriving the asymptotic node degree of randomly deployed (Poisson distribution) large-scale networks to probabilistically guarantee the average-case [17] or worst-case QoC [18]. To our best knowledge, there are no current works that are able to achieve determinate partial coverage with guaranteed worst-case QoC in a location-free manner.

In this work, we focus on determinately achieving generalized blanket coverage from full blanket coverage to partial coverage with guaranteed worst-case QoC, using merely connectivity information. We formulate this problem as confine coverage in Definition 1. Apparently, we cannot accurately know the diameter of one coverage hole without node location information. To circumvent this dependence on location measurements, we define the confine coverage based on communication models and their valid embeddings. Given a communication graph, the legitimate location of nodes in the Euclidean plane meeting the communication model is called as a valid embedding or realization of the networks, like UDG or quasi-UDG embeddings [20]. Given all communication links bounded in the distance $\mathit { R } _ { c } ,$ we can establish the sufficient condition to bound the hole size for all possible valid network realizations, which enables us to confine the coverage hole based on the connectivity metric.

Definition 1: (Confine Coverage) Given a subgraph $G ^ { \prime }$ of connectivity graph $G$ and a positive integer τ , if for any one valid embedding of $G ,$ each point in the target area is surrounded by at least one k-hop cycle in $G ^ { \prime }$ with $k \leq \tau ,$ we say $G ^ { \prime }$ achieves a τ -confine coverage on the target area.

The objective of this work is to select a node subset from the network G to determinately achieve expected confine coverage requirements with using only connectivity information.

# C. Configurability of Coverage Granularity

We explain the configurability of confine coverage, and show the ways we use confine coverage to achieve blanket coverage and QoC guaranteed partial coverage through adjusting the coverage granularity.

Specifically, the coverage granularity of confine coverage lies on two parameters: size of cycles and sensing ratio. The sensing ratio $\gamma = R _ { c } / R _ { i }$ s between communication range $R _ { c }$ and sensing range $R _ { s }$ has been one important factor involved in coverage problems. For example, it is widely used to analyze the property of achieving coverage and connectivity simultaneously [2] [3]. Ratio $\gamma$ becomes especially important for confine coverage, because confine coverage requires to combine both connectivity structures and specific sensing ratio to guarantee sensing coverage, which is also the best possible efforts that can be made by connectivity-based methods. Let us start from one simple instance of 3-confine coverage. Suppose $\gamma \leq \sqrt { 3 }$ and each point in the target area is surrounded by at least one triangle. This 3-confine coverage indeed achieves full blanket coverage sufficiently because if $\gamma \leq { \sqrt { 3 } } .$ , a connectivity triangle in any valid embeddings means a coverage region without inner holes.

We can further consider more thresholds for variable sensing ratio γ from two aspects. In the first aspect, γ is relatively small. Specifically, $\operatorname { i f } \gamma$ is less than ${ \sqrt { 3 } } ,$ , then communication cycles longer than 3 can still mean a coverage without holes. For example, $\gamma = \sqrt { 2 }$ or 1 can guarantee that there are no coverage holes in a 4-hop or 6-hop cycle, respectively. Hence, in such cases, 4-confine or 6-confine coverage also guarantees full blanket coverage. Generally, it is not difficult to show that τ -confine coverage can sufficiently guarantee blanket coverage ${ \mathrm { i f ~ } } \gamma \leq 2 \sin ( \pi / \tau )$ , which indeed is also a necessary condition for worst-case instances. In the second aspect, $\gamma$ is a relatively large value. $\operatorname { I f } \gamma$ is greater than ${ \sqrt { 3 } } ,$ , then a coverage hole can appear in a triangle of connectivity such that a 3-confine coverage does not promise full blanket coverage any more. Further, if $\gamma$ is much larger than 2, no connectivity-based coverage can guarantee bounded coverage holes. Thus, this work mainly considers the cases of $\gamma \le 2$ by default. In these cases, confine coverage provides a partial coverage with bounded hole size. It is not difficult to show that the maximum diameter $D _ { m a x }$ of coverage holes in a τ -confine coverage has the following upper bounds in any valid embeddings, $D _ { m a x } \leq ( \tau - 2 ) R _ { c }$ . Till now, we can summarize the above cases as Proposition 1.

Proposition 1: A τ -confine coverage can achieve a

• blanket coverage, that is, the maximum holes diameter $D _ { m a x } = 0 , \mathrm { i f } \ 0 \le \gamma \le 2 \sin ( \pi / \tau )$ .

• partial coverage with the maximum holes diameter $D _ { m a x } \leq ( \tau - 2 ) R _ { c } , \mathrm { i f } 2 \sin ( \pi / \tau ) < \gamma \leq 2 .$

From the above, we can see confine coverage can provide the configurable granularity to achieve both blanket coverage and partial coverage with worst-case QoC. By adjusting the coverage granularity, confine coverage potentially provides a flexible framework to unite (or bridges the gap of) two general coverage schemes, blanket and barrier. We can consider the barrier coverage as an instance of confine coverage with confine size of network scale. In this work, we focus on the confine coverage where the maximum confine size are bounded in a small constant.

We here explain why Ghrist’s method [9] cannot achieve confine coverage well. Clearly, Ghrist’s method is a specific pattern to achieve 3-confine coverage. As mentioned in previous Section II, in Ghrist’s method the coverage cycles have to be triangles, cannot be expanded into more general τ -hop cycles, $\tau \geq 4$ . This will reduce the network performance in two aspects. $\mathrm { I f ~ } \gamma \le \ 2 \sin ( \pi / \tau )$ and $\tau \geq 4 .$ , then τ - confine coverage has been ready to achieve blanket coverage sufficiently. Clearly, compared with using only triangles, that permitting using larger τ -hop cycles, $\tau \geq 4 ,$ , to cover the region can potentially reduce the number of nodes in the coverage set. Ghrist’s method, however, permanently uses triangles as the basic coverage unit, which will cause unnecessary waste and reduce the network lifetime. On the other hand, for the cases of 2 sin $\begin{array} { r } { \mathrm { \Sigma } _ { \lfloor } ( \pi / \tau ) \ < \ \gamma \ \le \ 2 , } \end{array}$ we can still exploit cycles of $\tau \geq 4$ hops to achieve given requirements adequately, if the applications permit diameters of coverage holes to be much greater than $R _ { c } / { \sqrt { 3 } } .$ . Ghrist’s method, however, will force the maximum hole diameter $D _ { m a x } \leq R _ { c } / \sqrt { 3 } .$ , which still leads to unnecessary wastes.

# IV. CYCLE-PARTITION COVERAGE CRITERION

Previously, the definition of confine coverage is based on the valid embeddings for the network. But apparently we have no idea of the valid embeddings and thus cannot utilize them to decide whether a network satisfies a given confine coverage. In this section, we propose a criterion to determine confine coverage based on merely connectivity information.

We first introduce the main idea of this connectivitybased coverage criterion and then present its mathematical definition. The intuition behind its idea can be explained in a geometrical manner as follows. Based on the communication graph alone, it is difficult to perceive coverage holes. To achieve a τ -confine coverage, we transform the connectivity graph into its τ -cycle filled space. Visually, each cycle of less than τ -size in the graph is regarded as a filled solid polygon, polygonal surface, while one cycle, if its length is more than τ , remains unchanged and keeps to be a polygonal chain. After this transformation, connectivity graph becomes a cycle-filled space. Suppose the cycle-filled space is stitched well by these polygonal cycle surfaces such that its shadow projected in the plane can cover the target region completely (no voids appear in the target region). Then each point in the target area has at least one polygonal surface to cover it and thus is bounded in at least a τ -hop cycle in the graph. We next describe how to truly translate this idea into graph theoretical terms.

# A. Establishment of Coverage Criterion

Before formally presenting the coverage criterion, we need to introduce some notations. These notations are also useful for presenting other graph tools in the Section V. Let H be a simple graph with vertex set $V ( H )$ and edge set $E ( H )$ . A simple cycle C is a subgraph of H if it is connected and each vertex in C has degree two. A cycle C can be identified by its incidence vector $b ( C ) = ( b _ { 1 } , b _ { 2 } , \cdot \cdot \cdot , b _ { i } , \cdot \cdot \cdot )$ , for $i \in [ 1 , | E ( H ) | ]$ , with $b _ { i } = 1$ iff $e _ { i } \in E ( C )$ and $b _ { i } = 0$ iff $e _ { i } \notin E ( C )$ . The length |C| of cycle C is the number of its edges, $| E ( C )$ |. The incidence vectors of cycles span a binary vector space, called the cycle space $\mathcal { C } _ { H }$ of H. The addition of two cycles $C _ { 1 }$ and $C _ { 2 }$ is defined as the binary addition of their incidence vectors. It corresponds to the symmetric difference $C _ { 1 } \oplus C _ { 2 } = ( E ( C _ { 1 } ) \bigcup E ( C _ { 2 } ) ) \setminus E ( C _ { 1 } ) \bigcap E ( C _ { 2 } )$ . Given a cycle set $\mathcal { C } = \{ C _ { i } : i = [ 1 , n ] \}$ , the cycle sum of C is $\Sigma { \mathcal { C } } \ = \ C _ { 1 }$ ⊕ $C _ { 2 } \oplus \cdots \oplus C _ { n } .$ A cycle basis B of H is a basis of $\mathcal { C } _ { H }$ . The total length (B) of B is the length sum of its cycles: $\begin{array} { r } { \ell ( B ) = \sum _ { C \in B } | \dot { C } | } \end{array}$ . A minimum cycle basis (MCB for short) of H is a cycle basis with minimum total length. We write the lengths of the shortest and longest cycles in B as $| B | _ { m i n } = m i n \{ | C | : C \in B \}$ and $| B | _ { m a x } = m a x \{ | C | : C \in B \}$ , respectively.

We then define cycle partition and utilize it to establish the coverage criterion, as given in Proposition 2 and 3. For easy to understand, we first study the basic version that target area $A _ { t a r }$ is a simply connected plane region in the sense that there are no inner holes in $A _ { t a r } .$ . Then, we extend these related conceptions into general cases that $A _ { t a r }$ is a multipleconnected region. By default, we write the boundaries cycles as $\mathcal { C } _ { B }$ . For the case of simply connected target region, $\mathcal { C } _ { B }$ only contains one outer boundary cycle $C _ { o u t e r }$ .

Definition 2: (Cycle Partition) Given a cycle C and a cycle set C in graph H, if C is the sum of cycles in ${ \mathcal { C } } ,$ $C = \sum { \mathcal { C } } ,$ , C is a cycle partition of C in G.

Note that cycle C is trivially a cycle partition of itself.

Definition 3: (τ -Partitionable Cycle) A cycle C in graph H is τ -partitionable if there exists one cycle partition  of C in H such that the size of longest cycle in C is bounded in a positive integer τ , $| { \mathcal { C } } | _ { m a x } \leq \tau$ .

Proposition 2: (Coverage Criterion for Simply-Connected Area) Given the graph G and its outer boundary $C _ { o u t e r } ,$ a subgraph $G ^ { \prime }$ of G can achieve τ -confine coverage if $C _ { o u t e r }$ is τ -partitionable in $G ^ { \prime }$ .

![](images/26c00b169aaa52da37527f08cfe3da3a342c99c48acb7557732df46085763e2f.jpg)



(a)

![](images/bf9992e856bba692052e9f58619de5f2e03f133acbc0ba7599f48683953dd41c.jpg)



(b)   
Figure 1: A network that looks like a mobius band, (a) shows¨ the logical connectivity of the network, and (b) shows a valid embedding of the network in the plane.

From the definition of cycle partition, we can understand the coverage criterion defined in Proposition 2 in a more intuitive manner. Consider the network as a rope net whose outer boundary $C _ { o u t e r }$ surrounds the target area $A _ { t a r }$ in the plane. That $C _ { o u t e r }$ is τ -partitionable means that mesh sizes of the rope net are bounded in a range (related with τ ). Thus any object larger than the largest mesh will be captured and cannot traverse the net. Hence, this coverage criterion is easy to understand and effective. The details of its proof of Proposition 2 are omitted here, which is straightforward. (Hints: we can consider those filled cycles in a cycle partition for any valid embedding of the graph G, and piece them together in this embedding.)

If the target areas are complicated and multi-connected, the network may have multiple boundaries, thus the coverage criterion needs to be able to differentiate real coverage holes from the inner areas that are surrounded by inner boundaries and does not need coverage. We thus expand previous criterion to yield stronger and robust criterion with considering multiple boundary cycles, as defined in Proposition 3. We extend the definitions of cycle partition and partitionable cycle in Definition 2 and 3, to cover the multiple cycles as follows. For multiple cycles $\mathcal { C } _ { M }$ , a set of cycles C is the cycle partition of these multiple cycles $\mathcal { C } _ { M }$ , if $| \sum ( \mathcal { C } _ { M } \bigcup \mathcal { C } ) | = 0$ . Cycle set $\mathcal { C } _ { M }$ is τ -partitionable if for any cycle partition $\textit { \textcircled { } C } _ { M }$ , the size of the longest cycle in is bounded in a constant $\tau , | \mathcal { C } | _ { m a x } \leq \tau$ . Accordingly, the coverage criterion for multiply-connected area is presented, as follows.

Proposition 3: (Coverage Criterion for Multiply-Connected Area) Given the graph G and its boundaries cycles $\mathcal { C } _ { B }$ , a subgraph $G ^ { \prime }$ of $G$ can achieve τ -confine coverage if $\mathcal { C } _ { B }$ is τ -partitionable in $G ^ { \prime }$ .

# B. Comparison with Homology Criterion

Now, we are ready to compare our coverage criterion based on cycle partition with the homology-group criterion proposed by Ghrist et al. [9]. We compare these two criterions in two aspects. First, both cycle-partition criterion and homology-group criterion can provide the sufficient condition for τ -confine coverage with parameter $\tau \ = \ 3 .$ .

![](images/5c8c10e6817f5ae0597897e80e01882e88841a56af76404e93e8002ffb1914b1.jpg)



(a)

![](images/c7ae82cd457565b4f35c358333414733d76dbac295517cc22c6985b544df041c.jpg)



![](images/0f6ea7591bc3f190b3d23d5ab4c649b53facb41912b66671820d1a48fed9975c.jpg)



![](images/bdcedcc95a59016e22405f5cf093facf9b5b35567722d1c8c8ad381f5b0a4883.jpg)



![](images/ed1b2351fec9f622ffdf71dae6c8a1f2b23e3fdc4822923f32bb23ada4a76b19.jpg)



Figure 2: An example found by coverage algorithm. Figure (a) is the original network and its outer boundary. Figures (b-e) shows the results after maximal vertex deletion for $3 , 4 , \bar { 5 } , 6$ confine coverage, respectively.

But in our criterion, τ is an adjustable parameter, while it is non-adjustable in homology-group criterion. Second, our criterion indeed relaxes the homology-group criterions, thus homology-group criterion is a special case of our criterion. We explain the important differences between these two criterions through checking their behaviors in a simple example, shown in Figure 1.

Figure 1 shows a network that forms a mobius band ¨ built by 2-simplicial complexes. The left figure shows the logical connectivity of the network, and the right is one valid embedding of the network in the plane. The cycle $\langle a , b , c , d , e , f , g , h \rangle$ forms the outer boundary in the network, and apparently there are no coverage holes in the network if sensing ratio $\gamma \leq { \sqrt { 3 } } .$ For this example, our cycle-partition criterion can correctly determine that this network is of 3-confine coverage, thus is of full coverage. We can easily verify this because the cycle $\langle a , b , c , d , e , f , g , h \rangle$ is the sum of all the triangles in the network, thus is 3- partitionable. The first homology group of this mobius-band ¨ network, however, is non-trivial, and has the same homology type as a circle, instead of a point. Hence, homologygroup criterion will fail to determine the coverage of this network correctly. The failure of homology-group criterion is because the condition of trivial first homology group is rather strong, and it indeed forces that any cycle in the graph is shrinkable. In this example, the central circle 1, 2, 3, 4 cannot retract into one vertex by continuously adding triangles to itself. Relatively, our cycle-partition criterion only requires the boundary cycles can be assembled from small cycles. Homology-group criterion indeed is a special case of our criterion, because trivial first (relative) homology group can ensure the boundary cycles are 3- partitionable. Our criterion has the advantage that it relaxes the homology-group criterion greatly while still providing a sufficient criterion.

# V. DISTRIBUTED COVERAGE ALGORITHM

In the previous section, we establish the cycle-partition criterion for confine coverage. The cycle-partition criterion merely provides an implicit existence result for determining confine coverage. We will need to address two problems to achieve coverage scheduling. First, we need to design an implementable criterion of confine coverage, that is, a computational procedure to decide whether a cycle is τ - partitionable. Second, if a network not only passes the testing of coverage criterion, but also achieves a much overprovisioned confine coverage, we naturally wonder which nodes can be deleted safely without reducing the coverage quality to prolong the network lifetime. In this section, we present a deterministic, polynomial-time and distributed algorithm to achieve cycle-partition criterion and schedule a sparse coverage set using only connectivity information.

Figure 2 illustrates the procedures of this design. Given the connectivity graph G and boundary of a network shown in Figure 2 (a), our algorithm aims to find a subset of nodes such that the graph induced by these can achieve the expected confine coverage and contains as few as possible nodes. Figures 2 (b-e) show the results found by by our algorithm to achieve 3,4,5,6-confine coverage, respectively. We can visually verify the non-redundancy of these found coverage set, that is, the further deletion of any single node from the set will cause that the generated network fails to satisfy its expected confine coverage.

# A. Void Preserving Transformation

We first introduce the void preserving transformation (VPT for short), which is the tool we designed for manipulating graphs in this distributed algorithm. we first give some notations for later use. Let X be a vertex (or edge) set in a graph H, we use H[X] to denote the vertex-induced (or edge-induced) subgraph by X. Given vertex set $Y \subseteq V ( H )$ , we write H −Y for $H [ V ( H ) \backslash Y ]$ . Given edge set Z with all its endpoints $V _ { Z } ,$ we make $H - Z = ( V ( H ) , E ( H ) \backslash Z )$ and $H + Z = ( V ( H ) \bigcup V _ { Z } , E ( H ) \bigcup Z )$ . Let x be a singleton, a vertex or edge, $H - \{ x \}$ (or $H + \{ x \} )$ is abbreviated to $H - x \ ( \mathrm { o r } \ H + x )$ . We use $N _ { H } ^ { k } ( v )$ to denote the neighbors of a vertex v in H that are away from v within k hops in H. The k-hop neighboring graph of vertex v in H is defined as $\Gamma _ { H } ^ { k } ( v ) = H [ N _ { H } ( v ) ]$ ]. Note that $N _ { H } ^ { k } ( v )$ does not contain v itself; Void cycles of graph regarding to the boundary cycles are defined in Definition 4. We say a cycle C is irreducible if it cannot be represented as a sum of shorter cycles, which is originally introduced in chemical structural searches and called as relevant [21].

Definition 4: (Irreducible Cycle Partition, and Void $C y -$ cles) Given a set of boundary cycles ${ \mathcal { C } } _ { B } ,$ , a cycle partition C of $\mathcal { C } _ { B }$ is irreducible if all cycles in are irreducible in $G .$ A cycle in G is a void cycle relative to $\mathcal { C } _ { B }$ if it is contained in an irreducible cycle partition of $\mathcal { C } _ { B }$ .

Definition 5: (τ -Void Preserving Transformation) $\mathrm { ~ \bf ~ A ~ } \tau -$ void preserving transformation on a graph H is a sequential combination of graph operators, including vertex or edge deletion operator. A vertex (or edge) x of H can be deleted if neighboring graph $\Gamma _ { H } ^ { k } ( x )$ is connected, $k \geq \lfloor \tau / 2 \rfloor$ , and the maximum irreducible cycles in $\Gamma _ { H } ^ { k } ( x )$ are bounded in τ .

The void preserving transformation needs to calculate the size of maximum irreducible cycles in a graph. We present a simple algorithm to calculate the sizes of both maximum and minimum irreducible cycles in a graph. Although the maximum size of irreducible cycles is mainly concerned to guarantee confine coverage, the minimum size of voids also beneficially reflects the quality of coverage, and can be potentially used for different applications. This algorithm can calculate minimum and maximum sizes synchronously without additional costs.

The details are shown in Algorithm 1. The main procedure of the algorithm is to find one minimum cycle basis of a graph. The minimum and maximum void sizes can be further derived from the minimum cycle basis. The minimum cycle basis is calculated using a modified Horton’s algorithm [22]. Horton’s MCB algorithm uses a simple greedy strategy and has the running time of $O ( | E | ^ { 3 } | V | )$ . We next present Theorem 4, whose proof can be deduced from the properties of cycle matroid [22] and Theorem 3 in the previous work [23].

Theorem 4: Algorithm 1 can correctly find the minimum and maximum sizes of irreducible cycles in a graph.

# B. Computing Sparse Coverage Set

We next present the distributed scheduling algorithm based on void preserving transformation to discover a sparse coverage set. We formalize this problem as finding a nonredundant coverage set, as described in Definition 6.

Definition 6: (Non-Redundant Coverage Set) A node set V in G is a non-redundant for τ -confine coverage, if boundary cycles $\mathcal { C } _ { B }$ of G is τ -partitionable in $G [ V ]$ , and for any proper subset $V ^ { \prime } \subset V , \mathcal { C } _ { B }$ fails to be τ -partitionable in $G [ V ^ { \prime } ]$ .

Ideally, we desire that the designed algorithm can be performed in a distributed manner and uses only local connectivity. We next present the details of this scheduling algorithm, which can find a sparse coverage set to achieve a confine coverage by using only local connectivity. Moreover, our algorithm can guarantee to find a non-redundant coverage set when the connectivity graph follows some graph properties. Similarly, we first consider the simplyconnected target region, and then dispose the cases of multiply-connected target region. This procedure conducts a maximal vertex deletion on original connectivity graph G by void preserving transformation. Each internal node gathers its local connectivity and determines whether itself can be deleted. The procedure of vertex deletion terminates until no vertex in G can be deleted, and it outputs the reduced coverage graph $G _ { v d }$ .

Algorithm 1 Find Min. and Max. Sizes of Irreducible Cycles   
Input: A graph H.
Output: Minimum and maximum sizes of irreducible cycles in H: $\ell_{min}$ and $\ell_{max}$ .
1: $C = \emptyset$ .
2: for each $v \in V(H)$ do
3: Construct one shortest path tree of H rooted at v, $T_v$ .
4: for each $e = (x, y) \in E(H) \setminus E(T_v)$ do
5: if Least common ancestor of x and y in $T_v$ is root v then
6: Construct cycle $C(v, x, y)$ and $C = C \cup \{C(v, x, y)\}$ .
7: Order all cycles in C by non-decreasing length.
8: $B = \emptyset$ .
9: $\nu = |E(H)| - |V(H)| + 1$ .
10: while $|B| < \nu$ do
11: Select the shortest cycle $C \in C \setminus B$ .
12: Perform Gaussian elimination on $C \cup B$ .
13: if C is linear independent with B then
14: $B = C \cup B$ .
15: Output $\ell_{min} = |B|_{min}$ and $\ell_{max} = |B|_{max}$ .

The distributed implementation of this procedure is performed as follows. Each internal node v only needs to collect the connectivity $\Gamma _ { G } ^ { k } ( v )$ among its k-hop neighbors, $k \ = \ \lfloor \tau / 2 \rfloor$ . (Note that nodes in the boundary do not participate in this procedure and they keep unchanged.) Then node v can locally decide whether it can be deleted through τ -void preserving transformation. To parallelize the deletion procedure, these deletion operations can iteratively run in rounds. Two nodes that are of $m \ = \ \lfloor \tau / 2 \rfloor + 1$ hops away in the graph can perform the redundancy testing independently. In each round, all nodes that can be locally deleted first form a set of candidate nodes for deletion, then a m-hop maximal independent set (MIS) among these candidate nodes is randomly selected from the networks in a distributed manner. As a result, these MIS nodes can perform the deletion operation simultaneously. This procedure runs until that no nodes can be deleted. In the later part, we show this deletion algorithm produces a correct node set for τ - confine coverage. Further the coverage set is non-redundant if the irreducible cycles in the original connectivity graph are bounded in τ . Figures 2 (b-e) show the results after maximal vertex deletion for τ -confine coverage with parameter τ from

![](images/71af8160dc9397d9bc9020d56a19b23f3bccf6a1a745ed6eb691926d84b0d8a8.jpg)



![](images/5e6af27bfe0cae15125a68273628abea69fb642fc5465e435a263ef2d63b34d5.jpg)



Figure 3: Impacts of confine size Figure 4: Comparison with HGC

![](images/a010abf153b184edd090e6cbe4d26a4e8fac7f917af5833c1755cf030b36b325.jpg)



Figure 5: CDF of RSSI

![](images/24c1ada4b00f96b845023936da8828c38adac6d4bb68caf1eb48eca10603d035.jpg)



Figure 6: Results in trace topology

3 to 6, respectively. We can visually check these practical outputs from our algorithm. Clearly, in these reduced graphs, all void cycles will be bounded in the expected constants and no nodes can be deleted any more.

For the multiply connected target area, the connectivity graph will have multiple boundaries instead of one outer boundary. Note that we assume that each boundary cycle is much greater than the maximum confine size by default. We perform a preprocess on the connectivity graph, and transform it into a graph such that sequentially it can be disposed as in the simply-connected target area. Suppose there are $n \geq 2$ numbers of boundaries in the connectivity graph. We randomly select n−1 boundaries by filling a cone onto each boundary. In particular, for every boundary to be filled, we add a virtual node and connect it with all nodes in this boundary. Similar techniques also have been used by Ghrist et al. [9]. After such repairs on boundaries, we can simply consider multiply-connected networks as those only having one outer boundary. A little difference lies in that nodes and edges in the repaired boundaries cannot be deleted in the procedure.

We prove the correctness of this distributed algorithm. We here mainly consider the case of simply-connected network because a case of multiply-connected network can be transformed correspondingly into a simply-connected case through preprocessing on boundaries. Given the graph G and its outer boundary cycle $C _ { o u t e r }$ that is τ -partitionable in G, We will show that $C _ { o u t e r }$ is still τ -partitionable in the reduced graphs $G _ { v d } ,$ , after performing τ -void preserving transformation on a graph G. The result is presented in Theorem 5. Hence, our algorithm finds a coverage set that correctly achieves the τ -confine coverage. We further show the constructed reduced graph is of non-redundancy if the the maximum irreducible cycle in G is bounded in τ , as presented in Theorem 6. The details of these proofs are omitted due to space limitations.

Theorem 5: Given a τ -partitionable boundary $C _ { o u t e r }$ in $G , C _ { o u t e r }$ is still τ -partitionable in the graph after maximal vertex deletions.

Theorem 6: The found coverage set is non-redundant for τ -confine coverage by our algorithm if the maximum irreducible cycle in G is bounded in τ .

# VI. EVALUATION

We conduct extensive simulations to evaluate the effectiveness of this approach. By varying coverage granularity and sensing ratio, we evaluate our distributed confine coverage algorithm, denoted by DCC, and check the sizes of selected coverage set. We compare this design with the state-of-the-art connectivity-based approach: homologygroup based coverage, denoted as HGC, by Ghrist et al. [9], which is currently the best centralized methods solely using node connectivity to perform the coverage verification.

# A. Impacts of Confine Sizes

In the simulation, we deploy 1600 nodes in a square area by a uniformly random distribution, and the average node degree is around 25. Although our detection approach does not enforce the compliance to specific communication models for the network, for the convenience of comparison, in this set of simulations we assume UDG model to build the network, which is assumed by HGC approach to establish its correctness. We find the outer boundary by using the fine-grained recognition algorithm [13]. For the convenience of comparison between different network configurations, we fix the maximum communication range $R _ { c } ~ = ~ 1$ in all the simulations, and adjust sensing ranges according to γ. Under each configuration, our simulation takes 100 runs with random network generation, and we report the averages.

We examine the impacts of confine sizes on the sizes of coverage set. Intuitively, given a target region, a coverage scheduling based on a larger confine size can utilize less nodes than those based on small confine sizes. This simulation validates this intuition definitively, as shown in Figures 3. The number of nodes in the coverage set decreases significantly with the increasing of confine size. Note that for one same network generation, we normalizedly set the nodes in a 3-confine coverage as one unit to measure the results of other larger confine coverages. The y-axis in Figures 3 is the ratio of a size of τ -confine coverage to that of a 3-confine coverage, τ from 3 to 9.

We further compare DCC with HGC with both variable ratios γ and confine requirements. We change the confine requirements of maximum hole diameter from 0, 0.4, 0.8 and 1.2 while changing γ from 2 to 1, that is, increasing

![](images/6341797129e5cf832ad867dfdfd9fb1501c01504b8aab90d140c87d3aa0ce465.jpg)



![](images/56883424df75cb7f81145830c71c0830c2906d5bfd3a68969aa8615d951d27aa.jpg)



![](images/ed4a2a9f5f3ec83f9b39e146bdced6261f94eba94a62a7690bc8612be7c1e5cd.jpg)



![](images/629ccd2a5e064e671af16d7215b1c3291c85c028ea21dd3724d78587643efd50.jpg)



(d)

![](images/3290cbf48987598f2d4b4e7b8f64a402cd0eedcd4e1465b8aba8fff0df7381b4.jpg)



(e)

![](images/291960ae665cbaaef79a239636b94ba6525521e557c7488223b9369675312fa4.jpg)



(f)   
Figure 7: Perform DCC in practical trace topology. Figure (a) is the original network with 296 nodes plotted as circles and a set (26 number) of boundary nodes plotted as squares. Figures (b-f) show some network snapshots for 3,4,5,6,7 confine coverage, respectively. 17,8,6,5,4 numbers of inner circle nodes are left in Figures (b-f), respectively.

$R _ { s }$ from $0 . 5 R _ { c }$ to $R _ { c }$ . Figure 4 shows the results. The value of diameter is relative to communication range, that is, 0.4 means $0 . 4 R _ { c }$ due to $R _ { c } ~ = ~ 1$ . Maximum hole diameter of 0 is equivalently a full blanket coverage. The y-axis in Figure 4 is the number of saved nodes λ by DCC in different configurations. The number of saved nodes λ is defined as follows. For a given coverage requirement, let $n _ { 1 }$ be the size of a coverage set found by HGC, and $n _ { 2 }$ is the possible minimum size a of coverage set found by DCC. λ is equal to $( n _ { 1 } \mathrm { ~ - ~ } n _ { 2 } ) / n _ { 1 }$ . We can see from Figure 4 that our DCC algorithm saves more nodes when we increase the sensing diameter or permit larger confine size. The result acts in accordance with our intuitions. Because HGC fixes the confine size to be 3, it cannot exploit the variable sensing ranges and relaxed coverage requirements to customize and select specific confine sizes. Relatively, the adjustable confine size of DCC makes DCC profit from both large sensing ranges and relaxed coverage requirements. For example, with the increasing of sensing ranges, DCC can utilize a coverage set of larger confine size to achieve full blanket coverage sufficiently. Hence, it is advantageous and necessary to use DCC in these scenarios.

# B. Impacts of Communication Models

In previous simulations, the results are given under the UDG model. It is worth pointing out that our algorithm is merely based on the connectivity information and does not rely on UDG models. To demonstrate the effectiveness of DCC algorithm in more general communication models, in this set of simulations we perform DCC in a network topology generated from practical trace data of GreenOrbs [24], as shown in Figure 7 (a). GreenOrbs is an ongoing sensor network system for ecological surveillance in the forest. Currently, approximately three hundreds of sensors are randomly deployed in the forest. Clearly, such a topology in Figure 7 (a) significantly deviates from the UDG model.

This trace topology is obtained as follows. We gather all the data packet received from all nodes in a period of time. Each packet contains some (at most ten) records that indicate the neighbors having best received signal strength indication (RSSI) at one node in the moment of the creation of the packet. Hence, each RSSI record indicates one potential directed communication between two sensor nodes. We accumulate all these RSSI records of a period of time (two days) to construct the global communication graph. Finally, those directed edges are eliminated and only undirected edges that have the average RSSI greater than a threshold are reserved. Figure 5 shows the empirical cumulative distribution function (CDF) of these RSSI associated with all edges. The y-axis represents the proportion of edges that are greater or equal than a threshold in all edges. The threshold of RSSI is selected to be near 85 dBm to utilize 80% undirected edges. Finally, a set of connected nodes are selected as the network boundary.

We then validate the effectiveness of DCC algorithm in the extracted trace topology. Similarly, we examine the impacts of confine sizes on the sizes of coverage set. The number of left inner nodes in the coverage set also decreases significantly with the increasing of confine size, shown in the Figure 6. Especially compared with previous simulations shown in Figure 3, we can observe from Figure 6 that the number of left nodes decreases remarkably when confine size varies from 3 to 5. This means that 4-confine and 5- confine coverage can contain much less nodes than 3-confine coverage in this trace topology. This phenomenon, we think, is mainly due to two aspects of reasons. First, there exist many links of long range in the trace topology, and thus larger confine size makes DCC have more chance to utilize those long links. Second, long narrow shape of this trace topology makes the boundary take more effects on the result. We further visually check the results generated by DCC. Figures 7 (b-e) show a group of randomly selected results found by DCC for τ -confine coverage with parameter τ from 3 to 7, respectively. These results further validate that DCC can tolerate the irregularity of communication and produce well-behaved outputs in practical network graphs.

# VII. CONCLUSIONS

As a crucial issue in wireless ad hoc and sensor networks, coverage problem is previously addressed either requiring accurate location information, range measurements, or using only connectivity information but forcing centralized computation and critical restriction on sensing and communication models. This work presents a practical graph theoretical framework to connectivity-based coverage problem in wireless ad hoc and sensor networks. We take the first attempt towards designing a distributed coverage algorithm to achieve configurable coverage requirements with using merely connectivity information. We formally prove the correctness of this design and evaluate it through extensive simulations and comparisons with the state-of-theart approach.

# ACKNOWLEDGMENTS

The authors are grateful for a variety of valuable comments from the anonymous reviewers. This work is supported in part by the NSFC/RGC Joint Research Scheme N HKUST 602/08, the National Basic Research Program of China (973 Program) under grant No.2006CB303000, the National High Technology Research and Development Program of China (863 Program) under grants No. 2002AA1Z2101 and No. 2007AA01Z180, NSFC under grants No. 60621003, No. 90718040, No. 60903223 and No. 60903224.

# REFERENCES

[1] S. Meguerdichian, F. Koushanfar, M. Potkonjak, and M. Srivastava, “Coverage problems in wireless ad hoc sensor networks,” in Proc. of IEEE INFOCOM, 2001.   
[2] X. Wang, G. Xing, Y. Zhang, C. Lu, R. Pless, and C. Gill, “Integrated coverage and connectivity configuration in wireless sensor networks,” in Proc. of ACM SenSys, 2003.   
[3] X. Bai, S. Kumar, D. Xuan, Z. Yun, and T.-H. Lai, “Deploying wireless sensors to achieve both coverage and connectivity,” in Proc. of ACM MobiHoc, 2006.   
[4] G. Kasbekar, Y. Bejerano, and S. Sarkar, “Lifetime and coverage guarantees through distributed coordinate-free sensor activation,” in Proc. of ACM MobiCom, 2009.   
[5] C. Zhang, Y. Zhang, and Y. Fang, “Detecting coverage boundary nodes in wireless sensor networks,” in Proc. of IEEE ICNSC, 2006.   
[6] O. Younis, M. Krunz, and S. Ramasubramanian, “Coverage without location information,” in Proc. of IEEE ICNP, 2007.   
[7] Y. Bejerano, “Simple and efficient k-coverage verification without location information,” in Proc. of IEEE INFOCOM, 2008.   
[8] R. Ghrist and A. Muhammad, “Coverage and hole-detection in sensor networks via homology,” in Proc. of ACM/IEEE IPSN, 2005.

[9] V. de Silva and R. Ghrist, “Coordinate-free coverage in sensor networks with controlled boundaries via homology,” International Journal of Robotics Research, vol. 25, no. 12, pp. 1205–1222, 2006.   
[10] A. Tahbaz-Salehi and A. Jadbabaie, “Distributed coverage verification in sensor networks without location information,” in Proc. of IEEE CDC, 2008.   
[11] M. Cardei and J. Wu, Handbook of Sensor Networks: Compact Wireless and Wired Sensing Systems. CRC Press, 2005, ch. 19, Coverage in Wireless Sensor Networks.   
[12] L. Wang and Y. Xiao, “A survey of energy-efficient scheduling mechanisms in sensor networks,” ACM/Springer Mobile Networks and Applications, vol. 11, no. 5, pp. 723–740, 2006.   
[13] D. Dong, Y. Liu, and X. Liao, “Fine-grained boundary recognition in wireless ad hoc and sensor networks by topological methods,” in Proc. of ACM MobiHoc, 2009.   
[14] Y. Wang, J. Gao, and J. S. Mitchell, “Boundary recognition in sensor networks by topological methods,” in Proc. of ACM MobiCom, 2006.   
[15] C. Gui and P. Mohapatra, “Power conservation and quality of surveillance in target tracking sensor networks,” in Proc. of ACM MobiCom, 2004.   
[16] Q. Cao, T. F. Abdelzaher, T. He, and J. A. Stankovic, “Towards optimal sleep scheduling in sensor networks for rare-event detection,” in Proc. of ACM/IEEE IPSN, 2005.   
[17] O. Dousse, C. Tavoularis, and P. Thiran, “Delay of intrusion detection in wireless sensor networks,” in Proc. of ACM MobiHoc, 2006.   
[18] P. Balister, Z. Zheng, S. Kumar, and P. Sinha, “Trap Coverage: Allowing Coverage Holes of Bounded Diameter in Wireless Sensor Networks,” in Proc. of IEEE INFOCOM, 2009.   
[19] S. Ren, Q. Li, H. Wang, X. Chen, and X. Zhang, “Design and analysis of sensing scheduling algorithms under partial coverage for object detection in sensor networks,” IEEE Transactions on Parallel and Distributed Systems, vol. 18, no. 3, p. 334, 2007.   
[20] F. Kuhn, T. Moscibroda, and R. Wattenhofer, “Unit disk graph approximation,” in Proc. of ACM DIALM-POMC, 2004.   
[21] P. Vismara, “Union of all the minimum cycle bases of a graph,” Electronic Journal of Combinatorics, vol. 4, no. 1, pp. 73–87, 1997.   
[22] J. Horton, “A polynomial-time algorithm to find the shortest cycle basis of a graph,” SIAM Journal on Computing, vol. 16, no. 2, pp. 358–366, 1987.   
[23] D. Chickering, D. Geiger, and D. Heckerman, “On finding a cycle basis with a shortest maximal cycle,” Information Processing Letters, vol. 54, no. 1, pp. 55–58, 1995.   
[24] L. Mo, Y. He, Y. Liu, J. Zhao, S. Tang, X. Li, and G. Dai, “Canopy closure estimates with greenorbs: Sustainable sensing in the forest,” in Proc. of ACM SenSys, 2009.