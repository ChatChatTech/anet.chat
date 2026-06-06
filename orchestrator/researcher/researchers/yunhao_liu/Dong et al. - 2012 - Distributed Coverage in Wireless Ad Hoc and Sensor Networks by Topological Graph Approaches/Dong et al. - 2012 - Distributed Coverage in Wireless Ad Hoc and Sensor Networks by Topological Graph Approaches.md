# Distributed Coverage in Wireless Ad Hoc and Sensor Networks by Topological Graph Approaches

Dezun Dong, Member, IEEE, Xiangke Liao, Kebin Liu, Yunhao Liu, Senior Member, IEEE, and Weixia Xu

Abstract—Coverage problem is a fundamental issue in wireless ad hoc and sensor networks. Previous techniques for coverage scheduling often require accurate location information or range measurements, which cannot be easily obtained in resource-limited ad hoc and sensor networks. Recently, a method based on algebraic topology is proposed to achieve coverage verification using only connectivity information. The topological method sheds some light on the issue of location-free coverage. Unfortunately, the needs of centralized computation and rigorous restriction on sensing and communication ranges greatly limit the applicability in practical largescale distributed sensor networks. In this work, we make the first attempt toward establishing a graph theoretical framework for connectivity-based coverage with configurable coverage granularity. We propose a novel coverage criterion and scheduling method based on cycle partition. Our method is able to construct a sparse coverage set in a distributed manner, using purely connectivity information. Compared with existing methods, our design has a particular advantage, which permits us to configure or adjust the quality of coverage by adequately exploiting diverse sensing ranges and specific requirements of different applications. We formally prove the correctness and evaluate the effectiveness of our approach through extensive simulations and comparisons with the stateof-the-art approaches.

Index Terms—Wireless ad hoc and sensor networks, coverage, distributed, connectivity, topological graph, cycle partition.

# 1 INTRODUCTION

WIRELESS sensor networks are emerging as promisingplatforms for many important applications such as platforms for many important applications such as homeland security, military surveillance, environmental monitoring, target detection and tracking, traffic control, etc. Coverage problem [1], [2], [3], [4], [5] focuses on characterizing how well a region of interest is monitored by a set of working nodes, and is a fundamental issue in wireless ad hoc and sensor networks.

Most existing studies address the coverage problem by employing computational geometry methodology. Those algorithms assume accurate node coordinates are available, and determine the coverage by geometric tools, such as well-known Delaunay triangulations, Voronoi diagrams, and geometric disk graphs, etc. [1], [2]. The assumption on accurate coordinates makes the coverage problem more tractable and enables the design of efficient distributed or

D. Dong and X. Liao are with the School of Computer, National University of Defense Technology (NUDT), Changsha, Hunan, P.R. China 410073, and also with the National Laboratory for Paralleling and Distributed Processing, NUDT. E-mail: {dong, xkliao}@nudt.edu.cn.   
. K. Liu and Y. Liu are with the School of Software, TNLIST, Tsinghua University, and also with the Department of Computer Science and Engineering, The Hong Kong University of Science and Technology, Hong Kong SAR. E-mail: {kebin, yunhao}@greenorbs.com.   
. W. Xu is with the School of Computer, National University of Defense Technology (NUDT), Changsha, Hunan, P.R. China. E-mail: xuwx@nudt.edu.cn.

Manuscript received 31 Mar. 2010; revised 3 July 2011; accepted 26 July 2011; published online 4 Aug. 2011. Recommended for acceptance by S. Fahmy. For information on obtaining reprints of this article, please send e-mail to: tc@computer.org, and reference IEEECS Log Number TC-2010-03-0218. Digital Object Identifier no. 10.1109/TC.2011.149.

localized coverage algorithms. Acquiring accurate locations, however, is practically difficult and expensive for largescale ad hoc networks. First, accurate location measurement requires a large subset of nodes equipped with special hardware like high-precision GPS and ranging devices. Second, networked localization algorithms often output probabilistic results as they suffer from computational complexity, error accumulation, and flip ambiguity, etc. In practice only partial location information with errors is available. It is necessary to relax the ideal assumption on location measurements to enhance the applicability of coverage algorithms in resource-limited wireless ad hoc and sensor networks.

Recently, a considerable attention has been devoted to location-free coverage algorithms. They make successful attempts toward coverage verification or scheduling, either using range measurements [5], [6], [7], [8] or only connectivity information [9], [10], [11]. Those range-based coordinate-free methods [5], [8] relax the restriction of global coordinates by using local relative distances between neighboring nodes. Ghrist and associate [9], [10] explore techniques from algebraic homology and propose the first connectivity-based coverage method. Ghrist and associate’s method lifts the connectivity graph into a topological space, simplicial complex, and determines the coverage by verifying whether the first (relative) homology group of the simplicial complex is trivial. Their method sheds light on the challenging issue of purely location-free coverage, however, still has its limitations. First, their method depends on purely centralized computation, which makes it restricted and impractical in large-scale ad hoc and sensor networks. Second, their method inherently constrains that the minimum coverage unit has to be triangle. This restriction may cause unnecessary wastes in many practical networks, especially when nodes have relatively large sensing ranges. Hence, it is of great interest to design a connectivity-based coverage scheme that supports distributed computation and adjustable coverage granularity. This work aims at enhancing the effectiveness and efficiency of the state-of-the-art connectivity-based coverage algorithms by Ghrist and associate [9], [10]. We make the first attempt toward establishing a graph theoretical framework to achieve distributed connectivity-based coverage with configurable coverage granularity.

The main contributions of this work are as follows: First, we present a connectivity-based coverage scheme, called confine coverage. Confine coverage does not force the communication model be unit disk graph (UDG), and provides a flexible scheme to achieve both full blanket coverage and partial coverage with guaranteed quality of coverage (QoC). Confine coverage supports adjustable confine size to exploit variable sensing ranges and relaxed coverage requirements. Second, we propose an effective criterion for confine coverage determination. Our criterion utilizes cycle-partition techniques, greatly relaxing the homology-group criterion proposed by Ghrist and colleague. For instance, a full coverage network is mistakenly estimated to contain holes by homology-group criterion, but can be correctly determined by our criterion, as explained in Section 4.1. Third, we introduce a graph tool, called void preserving transformation, to test coverage redundancy and perform network reduction. We present a deterministic and distributed algorithm to schedule a sparse coverage set using connectivity information. We formally prove the correctness of our method and show the effectiveness by extensive simulations. To the best of our knowledge, this is the first distributed design being able to determinately achieve generalized blanket coverage with guaranteed worst case quality of coverage, using merely connectivity information.

The remainder of this paper is organized as follows: We discuss related work in Section 2, and formulate the problem in Section 3.2. We present the graph theoretical coverage criterion in Section 4, and describe the design and implementation of the distributed scheduling algorithm in Section 5. Evaluation results are presented in Section 6, followed by the conclusion in Section 7.

# 2 RELATED WORK

Existing deterministic coverage methods can be classified into two categories, location-based and location-free. Locationbased methods assume node locations available, and use computational geometry techniques to perform coverage analysis [1], [2], [3]. Location-free approaches focus on achieving coverage with missing or incomplete location information. Those studies either assumes ranging information [5], [7], [8] or merely connectivity available [9], [10]. Besides coverage with deterministic guarantees, another important line of work [12], [13], [14], [15] studies stochastic coverage in large scale sensor networks. They assume that nodes are distributed according to a spatial random process, and statistically determine the fundamental properties and limitations of coverage schemes. Please refer to those good surveys [16], [17] for more details about previous works. We here pay more attention on connectivity-based methods [9], [10] as our work is in this category.

We first introduce the main ideas of connectivity-based method presented by Ghrist and colleague [9], [10], and analyze its advantages and shortcomings. Their method uses algebraic topology techniques to achieve full coverage. Their method models the network as simplicial complexes, which are well-defined blocks for building topological spaces in algebraic topology. Ghrist and colleague’s method mainly explores the observation that if the relationship between sensing range Rs and communication range Rcp satisfies a specific condition, $R _ { s } \geq 1 / \sqrt { 3 } R _ { c } ,$ , a connectivity triangle guarantees a coverage region without holes. Hence, a full coverage can be verified by the trivial first (relative) homology group of this simplicial complex. A connected simplicial complex having a trivial homology group means that each cycle in the graph can be continuously deformed into a point by moving along edges or triangles in connectivity graph.

Compared with previous location-based and rangebased methods, Ghrist and colleague’s method has its unique advantage, being robust to situations where location information is missing or only partially available. Their method, however, still suffers from several serious limitations. First, the verification of homology group requires global connectivity and a purely centralized computation, which greatly restricts its applicability in distributed wireless networks. Second, Ghrist and colleague’s method constrains a basic coverage unit have to be triangle, which leads to unnecessary resource waste in many practical scenarios, as discussed in Section 3.2. Third, their homology-group coverage criterion is still a rather strong condition, which can cause a full coverage network be mistakenly recognized as one with coverage holes, as explained in Section 4.1. In this work, we relax these limitations of Ghrist and colleague’s method, and propose an efficient distributed coverage scheme that permits adjustable coverage granularity.

# 3 PROBLEM FORMULATION

In this section, we present the basic network configuration and assumptions, and formulate the confine coverage scheme based on connectivity information.

The most studied coverage problem is area coverage, whose objective is to schedule nodes to cover an area of interest. Always-on full area coverage will exhaust network energy rapidly, which is considered to be too expensive in long-duration large-scale applications. Thus, partial coverage is explored to balance event detection quality and energy consumption in many applications, such as, movement target surveillance [18], rare-event detection [19], delay of intrusion detection [20], and trap coverage [21]. Those applications are tolerant of event detection with moderating delay or small probability of missing to improve the network lifetime. Partial coverage can be regarded as a generalized blanket coverage with permitting adjustable quality of coverage. Similar to full coverage, most existing partial coverage schemes also require location information to schedule nodes to guarantee worst-case QoC [18], [22]. To our best knowledge, there is no current work that is able to achieve deterministic partial coverage with guaranteed worstcase QoC in a location-free manner. This work focuses on deterministically achieving generalized blanket coverage from full coverage to partial coverage with guaranteed worst-case QoC, using merely connectivity information.

![](images/0b24b5d0ffcf4c816dbb1dbf3990c4c0b00aefefa9ae8ae1ff16663e26cc4266.jpg)



Fig. 1. One example illustrating network models.

# 3.1 Network Models

We consider a collection of nodes deployed over a plane region, as shown in Fig. 1. Each node can sense specified events in its sensing range $R _ { s }$ . The union of sensing region of all nodes is referred as the network sensing area, $A _ { n e t } ,$ , and it covers the target region that needs to be monitored by the network, referred to as the target area, $A _ { t a r } ,$ which is typically and significantly larger than the sensing range of a single node. A coverage hole is a connected planar region in the target area that cannot be covered by sensing nodes. Each node is only capable of communicating with adjacent nodes in its proximity, within the maximum communication range $R _ { c } .$ Note that we do not force the communication model to be the unit disk graph. Two nodes can or not communicate with each other if their distance is within the maximum communication range $R _ { c } .$ . We assume that the coordinates of nodes are unavailable, in the sense that nodes can determine neither distances nor orientations of other nodes. We use G to denote the connectivity graph of a network communication.

We assume that there is a periphery band [5] of width at least max $\{ R _ { c } , R _ { s } \}$ between the boundary of the network sensing area $A _ { n e t }$ and the edge of the target area $A _ { t a r . }$ , as illustrated in Fig. 1. The existence of periphery band ensures that network sensing area sufficiently covers the target area and the subgraph induced by nodes in periphery band contains proper boundary cycles. This is the reason why similar assumptions on periphery band also appear in other location-free coverage schemes [5], [8], [10], [11]. We refer boundary nodes as those that are located in the periphery band and the others as internal nodes. Although the nodes are not aware of their locations, each node can be assumed to know whether it is a boundary or an internal node by using the mechanisms, like location-free boundary recognition [23], [24], [25], [26] or many other ways discussed in [8]. This is a conventional assumption adopted by almost all location-free methods [5], [8], [10], [11]. By default, the boundaries in this work are found by a modified finegrained boundary algorithm [23].

The definition of QoC of partial coverage varies with different applications. In the applications like surveillance and target tracking, QoC is defined by the maximum distance that a moving target can travel in the network along a straight line while avoiding from detection. In the applications of environment monitoring, QoC often is measured by the maximum diffusion area of events before detection. This work adapts a universal metric for QoC by the diameter of coverage hole. A diameter of a coverage hole is defined as the diameter of the minimum circle circumscribing the coverage hole, which is different from the hole diameter in trap coverage [21]. Clearly, the diameter of a coverage hole sufficiently bounds the maximum straightline distance of escaping detection in the coverage hole, and also provides a diameter to calculate the upper bound of hole area. The worst case QoC is the maximum diameter of coverage holes in the network.

# 3.2 Confine Coverage

We explore communication models to define confine coverage, as shown in Definition 1. Confine coverage establishes a sufficient condition to bound the diameter of coverage hole using connectivity metrics. A valid embedding (or realization) of a connectivity graph G maps vertices in G into points in the euclidean plane such that the distance between two vertices in the plane still follows the communication model of G, e.g., UDG or quasi-UDG embeddings [27].

Definition 1 (Confine Coverage). Given a subgraph $G ^ { \prime }$ of connectivity graph G and a positive integer -, if for all valid embeddings of $G ,$ each point in the target area is surrounded by at least one k-hop cycle in $G ^ { \prime }$ with $k \leq \tau ,$ we say $G ^ { \prime }$ achieves a --confine coverage on the target area, and - is confine size.

We then explain the configurability of confine coverage. We show how to use confine coverage to achieve partial coverage through adjusting the coverage granularity. Coverage granularity builds upon two parameters: confine size and sensing ratio. The sensing ratio $\gamma = R _ { c } / R _ { s }$ between communication range $R _ { c }$ and sensing range $R _ { s }$ has been one important factor in coverage problems [2], [3]. Ratio $\gamma$ is especially important for connectivity-based coveragep schemes. As mentioned previously, $\gamma \leq \sqrt { 3 }$ is a sufficient condition to ensure that a connectivity triangle does not contain inner coverage holes in any valid embeddings, which establishes the foundation of Ghrist’s method [10]. We further consider more thresholds for variable sensing ratio $\gamma .$ . Fig. 2 visually explains the impact of different  on coverage qualities in a sparse network. This work focuses on the cases that confine size - is bounded by a small constant and $\gamma \leq 2 .$ . First, if  is value much less than ${ \sqrt { 3 } } ,$ a communication cycle longer than three will also correspond to a coverage region without holes. For example, if $\gamma = 1 .$ , there are no coverage holes in a 6-hop cycle, and 6-confine coverage also guarantees full coverage. Generally, it is not difficult to show that $\gamma \leq 2 \sin ( \pi / \tau )$ is a sufficient and necessary condition to guarantee full coverage in a --confine scheme. Second, if ${ \sqrt { 3 } } < \gamma \leq 2 ,$ a coverage hole can appear in a 3-hop cycle (triangle), thus a 3-confine coverage does not promise full coverage any more. Given $\gamma \leq 2 .$ , it is not difficult to show that the maximum diameter $D _ { m a x }$ of coverage holes can be bounded by $D _ { m a x } \leq ( \tau - 2 ) R _ { c }$ in a --confine scheme. Hence, confine coverage can provide the configurable granularity to achieve full coverage or partial coverage with worst-case QoC, as summarized in Proposition 1. Note that if $\gamma > 2 ,$ , it is hard for connectivity-based coverage schemes to guarantee bounded coverage holes, as illustrated in Fig. 2e.

![](images/5539da10ba73cb72e63e7c1f83a7dd413237c054ffd3b0a45652096c6144730a.jpg)



(a)

![](images/1755388c13095e4f00d24ddf94493244b589c7397777265a430e6ccc82c5a7d8.jpg)



(b)

![](images/dfe83d9383fad43d483ce20f5c5aae60045aebed7e31be3d2195234385e34190.jpg)



![](images/3086c56f6b027fe91a814dc0186a9e01d2d1fe79fe5eb5e073434f84ae32b365.jpg)



(d)

![](images/f200b0ce14e749d096afb46d61ce6f425744b71ddc8d5b5581f242cf493e5b30.jpg)



(e)   
Fig. 2. Coverage holes in variable sensing ranges, . Figures (a-e) show the cases when sensing range  is equal to $1 , { \sqrt { 2 } } , { \sqrt { 3 } } , 2 ,$ and 4, respectively. Big gray disks denote the sensing regions of nodes, and little circles and lines are nodes and communication links, respectively.

# Proposition 1. A --confine coverage can achieve a

blanket coverage, that is, the maximum holes diameter $D _ { m a x } = 0 , i f 0 \le \gamma \le 2 \sin ( \pi / \tau )$ .   
partial coverage with the maximum holes diameter $D _ { m a x } \leq ( \tau - \bar { 2 } ) R _ { c } , i f 2 \sin ( \pi / \tau ) < \gamma \leq 2 .$

We finally discuss why Ghrist and colleague’s method [10] cannot achieve confine coverage well. Ghrist and colleague’s method is a specific pattern of 3-confine coverage, however, cannot be expended to achieve general --hop cycles, $\tau \geq 4$ . This will reduce the network performance in two aspects. First, if $\gamma \leq 2 \sin ( \pi / \tau )$ , --confine coverage, $\tau \geq 4 ,$ has been ready to achieve full coverage sufficiently. Using larger cycles than triangles as minimum coverage units can potentially reduce the coverage set size greatly. Second, if 2 sin $( \pi / \tau ) < \gamma \leq 2$ and applications permit diameters of coverage holes to be much greater than $R _ { c } / { \sqrt { 3 } } ,$ --confine coverage, $\tau \geq 4 ,$ , still can achieve requirements adequately. In these cases Ghrist’s 3-confine coverage is overqualified for coverage requirements, and increases system overhead.

# 4 CYCLE-PARTITION COVERAGE CRITERION

Previously, the definition of confine coverage is based on the valid embeddings for the network. But apparently we have no idea of the valid embeddings and thus cannot utilize them to decide whether a network satisfies a given confine coverage. In this section, we propose a criterion to determine confine coverage based on merely connectivity information.

We first introduce the main idea of our connectivitybased coverage criterion. The intuition behind the idea can be explained in a geometrical manner as follows: Visually, each cycle of less than --size in the graph is regarded as a filled solid polygon, polygonal surface, while one cycle, if its length is more than -, remains unchanged and keeps to be a polygonal chain. After this transformation, connectivity graph becomes a cycle-filled space. Suppose the cyclefilled space is stitched well by these polygonal cycle surfaces such that its shadow projected in the plane can cover the target region completely. Then, each point in the target area has at least one polygonal surface to cover it and thus is surrounded by at least a cycle not greater than -. We next describe how to truly translate this idea into its mathematical definition.

# 4.1 Establishment of Coverage Criterion

We introduce some notations, which are also useful for presenting other graph tools in the Section 5. Let H be a simple graph with vertex set $V ( H )$ and edge set EðHÞ. A simple cycle C is a subgraph of H if it is connected and each vertex in C has degree two. A cycle C can be identified by its incidence vector $b ( C ) = ( b _ { 1 } , b _ { 2 } , \ldots , b _ { i } , \ldots ) ,$ for $i \in [ 1 , | E ( H ) | ]$ , with $b _ { i } = 1$ iff $e _ { i } \in E ( C )$ and $b _ { i } = 0$ iff $e _ { i } \not \in E ( C )$ . The length jCj of cycle C is the number of its edges, jEðCÞj. The incidence vectors of cycles span a binary vector space, called the cycle space $\mathcal { C } _ { H }$ of H. The addition of two cycles $C _ { 1 }$ and $C _ { 2 }$ is defined as the binary addition of their incidence vectors. It corresponds to the symmetric difference C1  $C _ { 2 } = ( E ( C _ { 1 } ) \bigcup E ( C _ { 2 } ) ) \setminus E ( C _ { 1 } ) \bigcap$ $E ( C _ { 2 } )$ . Given a cycle set $\mathcal { C } = \{ C _ { i } : i = [ 1 , n ] \}$ , the cycle sum of C is $\sum { \mathcal { C } } = C _ { 1 } \oplus C _ { 2 } \oplus \cdots \oplus C _ { n } .$ A cycle basis B of H is a basis of $\mathcal { C } _ { H }$ . The total length ‘ðBÞ of B is the length sum of its cycles: $\begin{array} { r } { \ell ( B ) = \sum _ { C \in B } | C | } \end{array}$ . A minimum cycle basis (MCB for short) of H is a cycle basis with minimum total length. Generally a graph will have many different MCBs. We write the lengths of the shortest and longest cycles in B as $| B | _ { m i n } = m i n \{ | C | : C \in B \}$ and $| B | _ { m a x } = m a x \{ | C | : C \in B \}$ , respectively. The union of all the minimum cycle basis (UMCB for short) of H is denoted as $\Omega ( H ) , \Omega ( H ) = \cup B _ { i } ,$ , where $B _ { i }$ is any one MCB of H.

We then define cycle partition and utilize it to establish the coverage criterion, as given in Propositions 2 and 3. For easy of understanding, we first study the basic version that target area $A _ { t a r }$ is a simply connected plane region in the sense that there are no inner holes in $A _ { t a r }$ . Then, we extend related definitions into general cases that $A _ { t a r }$ is a multiply connected region. By default, we write boundary cycles as $\mathcal { C } _ { B } .$ . For the case of simply connected target region, $\mathcal { C } _ { B }$ only contains one outer boundary cycle $C _ { o u t e r } .$ . Note that $C _ { o u t e r }$ surrounds target area $A _ { t a r }$ according to the assumptions in Section 3.1.

Definition 2 (Cycle Partition). Given a cycle C and a cycle set C in graph H, if C is the sum of cycles in $\begin{array} { r } { \mathcal { C } , C = \sum \mathcal { C } , } \end{array}$ C is a cycle partition of C in G.

Note that cycle C is a trivial cycle partition of itself.

![](images/7b6d70a6a6997f7f8efc71897a04d45a19a7ab29858f935424b7a10050cee492.jpg)  
(a)

![](images/efd1ece84cbe240c69058fdff0cde0b673816a000d81e9e4d19348202b2a9f1f.jpg)  
(b)

![](images/98c08be4fadbab83d420d4fc0f726862669414321b40a4154ebe49041b041bdf.jpg)  
(c)   
Fig. 3. Define the shadow of graph, (a) connectivity graph H with its plane embedding ", (b) H with filled ‘-size cycles, $\ell \leq \tau = 4 ,$ (c) the shadow $S _ { \tau } ^ { \varepsilon } ( H )$ of H.

Definition 3 (--Partitionable Cycle). A cycle C in graph H is --partitionable if there exists one cycle partition $\mathcal { C } o f C$ in H such that the size of longest cycle in C is bounded by a positive integer $\tau , | \mathcal { C } | _ { m a x } \leq \tau .$ .

# Proposition 2 (Coverage Criterion for Simply Connected

Area). Given the graph G and its outer boundary $C _ { o u t e r } , a$ subgraph G0 of G can achieve --confine coverage $i f C _ { o u t e r }$ is - -partitionable in G0 .

Proof. Given any one valid embedding " of graph $G ,$ we extend the shadow mapping defined in [28] into the general case. We fill all ‘-size, $\ell \leq \tau ,$ cycles in G into a solid polygon, as illustrated in Fig. 3 Let $S _ { \tau } ^ { \varepsilon } ( G )$ be the shadow of G. Because $C _ { o u t e r }$ is - -partitionable in G0 , there exists a cycle set C in $G ^ { \prime }$ such that $\begin{array} { r } { C _ { o u t e r } = \sum \mathcal { C } } \end{array}$ and $| { \mathcal { C } } | _ { m a x } \leq \tau .$ . Let $\textstyle S _ { 1 } = \bigcup _ { C \in { \mathcal { C } } } S _ { \tau } ^ { \varepsilon } ( C )$ be the aggregate region of shadows of all cycles in ${ \mathcal { C } } ,$ and $\bar { S _ { 2 } } = \bar { S _ { \tau ^ { \prime } } ^ { \varepsilon } } ( \bar { C _ { o u t e r } } )$ be the shadow of $C _ { o u t e r }$ with $\tau ^ { \prime } = | C _ { o u t e r } |$ . Hence, $ { \boldsymbol { S } } _ { 1 }$ contains $S _ { 2 }$ due to $C _ { o u t e r } = \sum \mathcal { C }$ . Because $C _ { o u t e r }$ surrounds the target area $A _ { t a r } , S _ { 1 }$ contains $A _ { t a r }$ . Hence, for each point $p$ in the target area $A _ { t a r } ,$ , there exists at least one cycle $C _ { p }$ in C such that $S _ { \tau } ^ { \varepsilon } ( C _ { p } )$ surrounds p. tu

Note that Proposition 2 describes a sufficient, but not a necessary condition for determining confine coverage. Consider the example shown in Fig. 4. Although the network can achieve a 4-confine coverage, the outer boundary cycle in the graph is not 4-partitionable.

The network can have multiple boundaries if target areas are complicated and multiply connected. In such circumstances coverage criterion needs to differentiate coverage holes from inner areas that are surrounded by

![](images/2cffd14aacd4650a69b00a650e9877a739af56f3f46c4edb0ad0dbe1d60c778c.jpg)



(a)   
(b)   
Fig. 4. One example explaining that our coverage criterion is not a necessary condition. (a) shows a plane embedding of a network instance. The network can achieve 4-confine coverage for the plane region bounded by cycle $C _ { o u t e r } .$ (b) shows the logical connectivity of the network. The connectivity graph is the combination of an annulus and a Klein bottle. Cycles $C _ { o u t e t }$ and $C _ { 1 }$ are boundaries of the annulus. Klein bottle is tangent to annulus at cycle $\begin{array} { r } { C _ { 1 } . \ C _ { o u t e r } = \sum ( \mathcal { C } \bigcup \{ C _ { 1 } \} ) } \end{array}$ , where C denotes the set of all quadrangles in the graph.

![](images/dec57940642e44d9551c0d7e7c4647c992171c526824dd5cefb016c7b0649809.jpg)



(a)

![](images/f1e396a85cbae1bcdb526e42e1e12a7b26e8d9ad1eac1f7fe08bcff9fd595553.jpg)



(b)   
Fig. 5. A network that looks like a mo¨bius band. (a) shows the logical connectivity of the network, whose 2-simplicial complexes forms a mo¨bius band. (b) shows a valid embedding of the network in the plane, cycle $\langle a , b , c , d , e , f , g , h \rangle$ is the outer boundary and 3-partitionable in the network.

inner boundaries and do not need to be monitored. We thus expend previous criterion to yield a coverage criterion for multiply connected areas, as described in Proposition 3. We extend the definitions of cycle partition and partitionable cycle in Definitions 2 and 3, to handle the cases of multiple cycles. Given multiple cycles $\mathcal { C } _ { M } , \mathrm { ~ a ~ }$ set of cycles C is the cycle partition of $\mathcal { C } _ { M }$ , $\mathrm { i f } \ | \sum ( \mathcal { C } _ { M } \bigcup \mathcal { C } ) | = 0 . \ \mathcal { C } _ { M }$ is --partitionable if for any cycle partition C of $\mathcal { C } _ { M } { \mathrm { ~ } }$ , the size of the longest cycle in C is bounded in a constant $\tau , | \mathcal { C } | _ { m a x } \leq \tau .$ .

# Proposition 3 (Coverage Criterion for Multiply Connected

Area). Given the graph G and its boundaries cycles $\mathcal { C } _ { B } ,$ , a subgraph G0 of G can achieve --confine coverage if $\mathcal { C } _ { B }$ is - -partitionable in G0 .

We next compare our cycle-partition criterion with Ghrist and colleague’s homology-group criterion [10]. Our criterion generalizes homology-group criterion in two aspects. First, our criterion provides a sufficient condition to determine --confine coverage with an adjustable parameter -, while homology-group criterion is only applicable to 3-confine coverage. Second, our criterion relaxes homology-group criterion for the case of 3-confine coverage. Consider the example shown in Fig. 5. The network has a connectivity graph shaped like a mo¨bius strip. There are nop coverage holes in the network if sensing ratio $\gamma \leq \sqrt { 3 }$ . Our criterion can correctly determine that the network can achieve 3-confine coverage and fully cover the target area. The first homology group of this mo¨bius-band network, however, has the same homology type as a circle and is nontrivial. Hence, homology-group criterion cannot correctly determine the full coverage of this network. The homology-group criterion forces all cycles in the graph be shrinkable. Our cycle-partition criterion only requires boundary cycles can be assembled from small cycles, and relaxes the homology-group criterion greatly.

# 4.2 Determination of Confine Size

We need to decide whether a cycle is --partitionable when implementing our coverage criterion. We transform this problem as computing a minimax cycle partition, as shown in Definition 4.

Definition 4 (Minimax Cycle Partition). Given a set of boundary cycles ${ \mathcal { C } } _ { B } ,$ a minimax cycle partition C is cycle partition of $\scriptstyle { \mathcal { C } } _ { B }$ such that for any other cycle partition $\mathcal { C } ^ { \prime } o f \mathcal { C } _ { B } ,$ , $| { \mathcal { C } } | _ { m a x } \leq | { \mathcal { C } } | _ { m a x } .$

We present a polynomial-time algorithm, shown in Algorithm 1, to construct a minimax cycle partition. In particular, given boundary cycles $\mathcal { C } _ { B }$ in $G ,$ our algorithm can calculate a minimax cycle partition C for $\mathcal { C } _ { B }$ . Hence, we can determine that $\mathcal { C } _ { B }$ is - -partitionable in $G , \ \tau = | { \mathcal { C } } | _ { m a x } .$ The main idea of our algorithm is as follows: It first finds the union of all the minimum cycle basis, UMCB, then utilizes UMCB to build a minimax cycle partition in a greedy manner. Specifically, let $\Omega ( G )$ be the UMCB of graph G. -ðGÞ can be calculated in polynomial time by using the algorithm proposed by Vismara [29]. In the greedy step, our algorithm orders all cycles in -ðGÞ by nondecreasing length. For a given -, we select from -ðGÞ all the cycles shorter than -, denoted as $\Omega ( G ) _ { \tau }$ . We test whether there exists a subset of $\Omega ( G ) _ { \tau } , \Omega ( G ) _ { \tau } ^ { \prime } \subseteq \Omega ( G ) _ { \tau }$ , such that boundary cycles $\mathcal { C } _ { B }$ can be represented as the sum of this subset, that is, $\sum { \mathcal { C } } _ { B } = \sum \Omega ( G ) _ { \prime } ^ { \prime }$ . This test can be evaluated by solving a system of linear equations, $\begin{array} { r } { \sum \mathcal { C } _ { B } = \Omega ( G ) _ { \tau } \odot X , } \end{array}$ where X is a binary vector of length $| \Omega ( \overline { { G } } ) _ { \tau } |$ and 	 denotes dot product (or scalar product). The system of linear equations can be finished in polynomial time by Gaussian elimination. Our algorithm increases - from 3 to $| \Omega ( G ) | _ { m a x }$ and terminates until the test of $\sum { \mathcal { C } } _ { B } = \sum \Omega ( G ) _ { \tau } ^ { \prime }$ is satisfied. We next prove the correctness of Algorithm 1, as shown in Theorem 1.

# Algorithm 1. Construct Minimax Cycle Partition

Input: A graph $G ,$ and boundary cycles $\mathcal { C } _ { B }$ .

Output: One minimax cycle partition C.

1: Find the UMCB of $G , \Omega ( G )$ .   
2: Order all cycles in $\Omega ( G )$ by non-decreasing length.   
3: for maximum cycle size -, from 3 to $| \Omega ( G ) | _ { m a x }$ do   
4: Find all the cycles in -ðGÞ that are not longer than $\tau , \Omega ( G ) _ { \tau }$ .   
5: Find the MCB of $\Omega ( G ) _ { \tau } , B _ { \tau }$ .   
6: Solve the linear equations of $\sum { \mathcal { C } } _ { B } = { \mathcal { B } } _ { \tau } \odot X =$ $\begin{array} { r } { \sum x _ { i } C _ { i } , \mathrm { f o r } x _ { i } \in X , C _ { i } \in \mathcal { B } _ { \tau } } \end{array}$ .   
7: if Find a solution for X then   
8: $\Omega ( G ) _ { \tau } ^ { \prime } = B _ { \tau } \odot X .$   
9: Return ${ \mathcal { C } } = \Omega ( G ) _ { \tau } ^ { \prime } .$

10: end if

11: end for

We present Definition 5 and Lemma 1 before proving the Theorem 1. A cycle C is said to be irreducible if it cannot be represented as a sum of shorter cycles, which is originally called as relevant in chemical structural searches [30].

# Definition 5 (Irreducible Cycle Partition, and Void Cycles).

Given a set of boundary cycles ${ \mathcal { C } } _ { B } ,$ a cycle partition C of $\mathcal { C } _ { B }$ is irreducible if all cycles in C are irreducible in G. A cycle in G is a void cycle relative to $\mathcal { C } _ { B }$ if it is contained in an irreducible cycle partition of $\mathcal { C } _ { B } .$ .

Lemma 1. Given boundary cycles $\mathcal { C } _ { B }$ in $G ,$ there exists at least one minimax cycle partition $\mathcal { C } o f \mathcal { C } _ { B }$ in $G ,$ and C is irreducible.

Proof. Given any minimax cycle partition C that is not irreducible, $\dot { c }$ can be transform into an irreducible minimax cycle partition as follows: For any reducible cycle $C$ in $\mathcal { C } , \ \bar { \boldsymbol { C } }$ can be represented as the sum of some irreducible cycles. We replace C by these irreducible cycles, and obtain a new cycle partition $\mathcal { C } ^ { \prime }$ . As a result, $\mathbf { \bar { \boldsymbol { c } } } ^ { \prime }$ is an irreducible minimax cycle partition with $| { \mathcal C } ^ { \prime } | _ { m a x } = | { \mathcal C } | _ { m a x } .$ tu

Theorem 1. Algorithm 1 guarantees to find one minimax cycle partition.

Proof. There exists one irreducible minimax cycle partition C according to Lemma 1. A cycle C is irreducible if and only if it is contained in a minimum cycle basis, following Lemma 1 of Vismara’s work [29]. The union of all the minimum cycle basis $\Omega ( G )$ contains all the irreducible cycles. Our algorithm gradually increases $\tau ,$ $\tau \in [ 3 , | \Omega ( G ) _ { \tau } | _ { m a x } ] ,$ and for each $\tau ,$ selects all cycles $\Omega ( G ) ,$ - that are $\Omega ( G )$ and less or equal to -. Hence, the first found cycle partition C in $\Omega ( G )$ - is irreducible minimax cycle partition. tu

# 5 DISTRIBUTED COVERAGE ALGORITHM

In the previous section, we establish the cycle-partition criterion for confine coverage and its a centralized implementation. In this section, we present a deterministic, polynomial-time, and distributed algorithm to schedule a sparse coverage set using only connectivity information. Fig. 6 illustrates the procedures of this design. Given a connectivity graph G and its boundary shown in Fig. 6a, our algorithm aims at finding a nonredundant coverage set. Figs. 6b, 6c, 6d, and 6e show the results found by our algorithm to achieve 3, 4, 5, 6-confine coverage, respectively. We can visually verify the nonredundancy of these coverage sets, i.e., deleting any node from a coverage set will cause the generated network fail to satisfy its expected coverage granularity.

Although the coverage set is obtained, coverage holes in the network are still invisible to us due to missing location information. In partial coverage schemes it is important to understand the structure of coverage holes, which provides necessary information for many applications, i.e., movement target surveillance [18], rare-event detection [19], delay of intrusion detection [20], etc. We present a distributed method to extract void cycles to capture and locate coverage holes. Fig. 6f illustrates void cycles constructed by our algorithm from the 6-confine coverage set in Fig. 6e.

# 5.1 Void Preserving Transformation

We introduce the void preserving transformation (VPT for short), which is the tool we designed for manipulating graphs in this distributed algorithm. Let X be a vertex (or edge) set in a graph H, we use $H [ X ]$ to denote the vertexinduced (or edge-induced) subgraph by X. Given vertex set $Y \subseteq V ( H )$ , we write $H - Y$ for $\overset { \cdot } { H } [ \overset { \cdot } { V } ( H ) \ \backslash \ \overset { \cdot } { Y } ]$ . Given edge set Z with all its endpoints $V _ { Z } ,$ , we make $H - Z = { \bar { ( V ( H ) } }$ ; $E ( H ) \setminus Z )$ and $H + \overline { { Z } } = ( V ( H ) \bigcup V _ { Z } , E ( H ) \bigcup Z )$ . Let x be a singleton, a vertex or edge, H  fxg (or $H + \{ x \} )$ i s abbreviated to $H - x \ ( \mathrm { o r } \ H + x )$ . We use $N _ { H } ^ { k } ( v )$ to denote the neighbors of a vertex v in H that are away from v within k hops in H. The k-hop neighboring graph of vertex v in H is defined as $\Gamma _ { H } ^ { k } ( v ) = { \hat { H } } [ N _ { H } { \overline { { ( v ) } } } ]$ . Note that $N _ { H } ^ { k } ( v )$ does not contain v itself; Void cycles of graph regarding to the boundary cycles are defined in Definition 5.

Definition 6 (--Void Preserving Transformation). A --void preserving transformation on a graph H is a sequential combination of graph operators, including vertex or edge deletion operator. A vertex (or edge) x of H can be deleted if neighboring graph $\Gamma _ { H } ^ { k } ( x )$ is connected, $k \geq \lfloor \tau / 2 \rfloor$ , and the maximum irreducible cycles in $\Gamma _ { H } ^ { k } ( x )$ are bounded in -.

![](images/26f4145051070a861716f967e1bddd010cdee149d0a44e6fe5bacdc8ec42e82b.jpg)  
Fig. 6. An example illustrating distributed coverage algorithm. Figure (a) is the original network and its outer boundary. Figures (b-e) show the results after maximal vertex deletion for 3, 4, 5, 6 confine coverage, respectively. Figures (g-j) are the results after further maximal edge deletion for 3, 4, 5, 6 confine coverage, respectively. Figure (f) shows the void cycles in the found 6-confine coverage.

VPT needs to calculate the size of maximum irreducible cycles in a graph. The minimum and maximum size of irreducible cycles in a graph can be derived from the minimum cycle basis of the graph, as shown in Lemma 2.

Lemma 2. Given any one minimum cycle basis B of graph H, the minimum and maximum sizes of irreducible cycles of $H , \ell _ { m i n }$ and $\ell _ { m a x } ,$ are equal to $| B | _ { m i n }$ and $| B | _ { m a x } ,$ respectively.

Proof. Let C be the set of all irreducible cycles in H, thus C forms a cycle matroid [31]. The minimum cycle basis B of C can be found by greedy algorithms. Consider to generate B in a greedy fashion as done in Horton’s algorithm [31]. Clearly, at least one shortest irreducible cycle, say $C _ { 1 }$ , is selected into B in the first round. Also, $C _ { 1 }$ stays in $\boldsymbol { B }$ until the greedy algorithm finishes because $C _ { 1 }$ cannot be represented by shorter cycles. Meanwhile, at least one longest cycle in C is selected into B. Otherwise, those longest irreducible cycles in C will be able to be represented as the sum of shorter cycles in B. Hence, the minimum and maximum sizes of irreducible cycles in $H ,$ $\ell _ { m i n } = | \boldsymbol { B } | _ { m i n }$ and $\ell _ { m a x } = | \boldsymbol { B } | _ { m a x }$ . For any other minimum cycle basis $B ^ { \prime }$ of H, $| B ^ { \prime } | _ { m i n } = | B | _ { m i n }$ and $| B ^ { \prime } | _ { m a x } = | B | _ { m a x }$ according to Theorem 3 in previous work [32]. tu

# 5.2 Computing Sparse Coverage Set

We consider to compute a sparse coverage set, and formalize this problem as finding a nonredundant coverage set, as described in Definition 7.

Definition 7 (Nonredundant Coverage Set). Given boundary cycles $\mathcal { C } _ { B }$ of G, a --confine coverage set V in G is nonredundant, if for any proper subset $V ^ { \prime } \subset V , \mathcal { C } _ { B }$ fails to be --partitionable in $G [ V ^ { \prime } ]$ .

A nonredundant coverage set can be constructed through iterative deleting nodes from an initial coverage set. One node can be deleted if its deletion does not bleach the coverage criterion described in Section 4.2. A nonredundant coverage set is obtained when no vertex can be deleted. Such an algorithm is clearly centralized. We next present our distributed scheduling algorithm to construct a sparse coverage set. Each internal node gathers its local connectivity and determines whether itself can be deleted though void preserving transformation. Our algorithm conducts a maximal vertex deletion on original connectivity graph $G ,$ and outputs the reduced coverage graph $G _ { v d }$ . Moreover, if the connectivity graph follows some graph properties, our algorithm can guarantee to find a nonredundant coverage set. Similarly, we first describe the algorithm in simply connected target regions, then extend it into multiply connected cases.

The scheduling algorithm exploits the observation as follows: When an internal node v collects the connectivity $\Gamma _ { G } ^ { k } ( v )$ among its k-hop neighbors, $k = \lfloor \tau / 2 \rfloor$ , it is able to calculate the maximum size of irreducible cycles in graph $\Gamma _ { G } ^ { k } ( v )$ , and thus can locally decide whether it can be deleted according to --void preserving transformation. Moreover, two nodes that are greater than or equal to $k + 1$ hops away from each other can perform the redundancy testing independently. The distributed implementation of this scheduling algorithm is described as follows: The details of this procedure are shown in Algorithm 2. Initially, all the internal nodes are identified as candidate nodes. A maximal independent set (MIS) [33] I is selected among the candidate nodes in a random and distributed manner. Further, I is partitioned into a group of maximal m-hop independent set, $\bar { I } _ { 1 } , \ldots , I _ { r } , \ m = \lfloor \tau / \bar { 2 } \rfloor + \bar { 2 } ,$ r being a constant. A maximal m-hop independent set needs to satisfy two conditions: first, each group $I _ { i } , 1 \leq i \leq r ,$ is an m-hop independent set in $G ;$ second, group $I _ { i } , 1 \le i \le r - 1$ , is maximized in the sense that adding any other nodes in $I \backslash I _ { i }$ into $I _ { i }$ will cause Ii not be an m-hop independent set in G. Node deletion operations iteratively run in r rounds. In ith round, each node v in $I _ { i }$ collects the connectivity $\Gamma _ { G } ^ { k + 1 } ( v )$ among its k þ 1-hop neighbors. Let $N _ { v } = \{ v , N _ { G } ^ { 1 } ( \stackrel { . } { v } ) \}$ denote the union of node v and all its one-hop neighbors. For each node w in $N _ { v } ,$ node v attempts to delete $w ,$ using the connectivity information among the k-hop neighbors of w. Node v selects a maximal (not maximum) number of nodes from $N _ { v }$ that can be deleted, denoted by $N _ { v } ^ { \prime }$ . Node v reports that $N _ { v } ^ { \prime }$ is locally deleted in this round. Nodes in $I _ { i }$ can perform the local deletion operation simultaneously. This procedure runs until that no nodes can be deleted. Nodes in the boundary do not participate in this procedure and keep unchanged. In the later, we show this deletion algorithm produces a correct --confine coverage set. Further the coverage set is nonredundant if the irreducible cycles in the original connectivity graph are bounded in -. Figs. 6b, 6c, 6d, and 6e show the results after maximal vertex deletion for --confine coverage with - from three to six, respectively. We can visually check these practical outputs by our algorithm. Clearly, in these reduced graphs, all void cycles are bounded in the expected constants and no nodes can be deleted any more.

# Algorithm 2. Find Sparse Coverage Set

Input: Connectivity graph $G ,$ interal nodes $V _ { 0 } ,$ confine size - .

Output: A minimal node set of --confine coverage, $V _ { c } .$

1: Construct a maximal independent set I in graph $G [ V _ { 0 } ]$

2: Separate I into a group of m-hop independent set in $G ,$ $I _ { 1 } , \ldots , I _ { r } , m = \lfloor { \tau / 2 } \rfloor + 2 .$

3: Deleted node set $V _ { d } : = \emptyset .$

4: for i ¼ 1 to r do

5: for each node v in $I _ { i }$ do

6: $N _ { v } : = \{ v , N _ { G } ^ { 1 } ( v ) \} , N _ { v } ^ { \prime } : = \emptyset .$

7: for each node w in $N _ { v }$ do

8: v calculates the void size of $\Gamma _ { G } ^ { k } ( w ) - N _ { v } ^ { \prime } ,$ $k = \lfloor \tau / 2 \rfloor$ , and tries to delete w according to -VPT.

9: if w is deletable then

10: $N _ { v } ^ { \prime } : = N _ { v } ^ { \prime } \cup \{ w \}$

11: end if

12: $V _ { d } : = V _ { d } \bigcup N _ { v } ^ { \prime } , G : = G - N _ { v } ^ { \prime } .$

13: end for

14: end for

15: end for

16: Output $V _ { c } : = V _ { 0 } \setminus V _ { d } .$

For the multiply connected target area, the connectivity graph will have multiple boundaries instead of one outer boundary. Suppose there are n $, \geq 2$ numbers of boundaries in the connectivity graph. We randomly select n  1 boundaries by filling a cone onto each boundary. In particular, for every boundary to be filled, we add a virtual node and connect it with all nodes in this boundary. Similar techniques also have been used by Ghrist and colleague [10]. After such repairs on boundaries, we can simply consider multiply connected networks as those only having one outer boundary. A little difference lies in that nodes and edges in the repaired boundaries cannot be deleted in the procedure.

# 5.3 Coverage Void Representations

We propose a distributed method to generate a cycle set to represent and locate holes. We expect that all nodes neighboring to a hole have a consistent view on the representation of this hole, that is, a unique cycle surrounding this hole. One node from its local view, however, often finds multiple different cycles to surround a hole, which may cause nodes identify different cycles to represent the same hole. The multiple representations of holes are mainly due to that network graph contains redundant edges and is overqualified to achieve a given confine coverage. Our main idea is as follows: We maximally delete redundant edges from vertex-reduced graph $G _ { v d }$ to construct an edgereduced graph $G _ { e d } .$ . We then extract a compact and meaningful cycle set $\mathcal { C } _ { v o i d s }$ from $G _ { e d }$ to represent and locate holes. Similar to vertex deletion, edge deletion operator in VPT can be performed in a distributed manner. Each node only needs local connectivity information. Figs. 6g, 6h, 6i, and 6j show the results after maximal edge deletion for confine sizes from three to six, respectively. Boundary edges do not participate in this deletion operation. Each node v further calculates all the void cycles $\Omega _ { v }$ among its local connectivity $\Gamma _ { G } ^ { k } ( v ) , k = \lfloor \tau / 2 \rfloor$ , by using the UMCB finding algorithm [29]. A union of all these void cycles $\mathcal { C } _ { v o i d s }$ is obtained to sufficiently capture all the holes, $\begin{array} { r } { \mathcal { C } _ { v o i d s } = \bigcup _ { v \in V ( G _ { e d } ) } \Omega _ { v . } } \end{array}$ , for each v in $G _ { e d } .$ Fig. 6f shows the union of void cycles calculated from the 6-confine network in Fig. 6g.

# 5.4 Correctness Proof and Complexity Analysis

This section proves the correctness of this distributed algorithm and analyzes the complexity of the algorithm.

We first prove the correctness of algorithm. We mainly consider the case of simply connected target area because a multiply connected case can be transformed into a simply connected case through preprocessing on boundaries. Given the graph G and its outer boundary cycle $C _ { o u t e r }$ that is - -partitionable in $G ,$ we will show that $\dot { C } _ { o u t e r }$ is still --partitionable in the reduced graphs $G _ { v d } ,$ , after performing --void preserving transformation on a graph G. The result is presented in Theorem 2. Hence, our algorithm finds a coverage set that correctly achieves the --confine coverage. We further show the reduced graph is of nonredundancy if the maximum irreducible cycle in G is bounded in $\tau ,$ as presented in Theorem 3.

Theorem 2. Given a --partitionable boundary $C _ { o u t e r }$ in $G , C _ { o u t e r }$ is still --partitionable in the graph after maximal vertex and edge deletions.

Proof. Let V be the nodes that are maximally deleted form G. We prove the case of vertex deletion by induction on the sequential order V . To prove the induction step, we show that $C _ { o u t e r }$ is still a - -partitionable graph in $G - v ,$ , that is, there exists a --cycle partition for B. Let C be any --cycle partition of B in G. If v does not be contained in any cycles in ${ \mathcal { C } } ,$ C is still a - -cycle partition of B in $G - v .$ . Otherwise, let $\mathcal { C } _ { 1 } \subseteq \mathcal { C }$ be the set of cycles in C that contain v. For any cycle $C _ { 1 }$ in ${ \mathcal { C } } _ { 1 } ,$ we know that $| C _ { 1 } | \le \tau$ and all the nodes in the $C _ { 1 }$ are within the k-hops neighbors of $v ,$ $k \leq \lfloor \tau / 2 \rfloor$ . Let $\begin{array} { r } { \mathcal { C } _ { s u m } = \sum \mathcal { C } _ { 1 } . ~ \mathcal { C } _ { s u m } } \end{array}$ can be regarded as a (maybe not simple) cycle as follows: Each cycle in $\mathcal { C } _ { 1 }$ can be considered as a path with both head and tail at v. These cycles $\mathcal { C } _ { 1 }$ are concatenated end-to-end at v and form cycle $\mathcal { C } _ { s u m } .$ . Thus, $\mathcal { C } _ { s u m }$ can be represented as $\sum { \mathcal { C } } _ { 2 }$ such that each cycle $C$ in $\mathcal { C } _ { 2 }$ is a simple cycle in $\Gamma _ { G } ^ { k } ( v )$ and $| C | \le \tau$ , because $\Gamma _ { G } ^ { k } ( v )$ is a --void bounded graph according to void preserving transformation. Hence, we can transform C into $\mathcal { C } ^ { \prime } = \bar { \mathcal { C } } _ { 2 } \bigcup \mathcal { C } \backslash \mathcal { C } _ { 1 }$ , and $\mathcal { C } ^ { \prime }$ is a cycle partition of $C _ { o u t e r }$ in $G - v$ . The case of edge deletion can be discussed similarly as that of vertex deletion. tu

From Theorem 2, we can further know that the void cycles $\mathcal { C } _ { v o i d s }$ obtained from $G _ { e d }$ do contain a cycle partition for $C _ { o u t e r }$ . We next show our constructed reduced graph is of nonredundancy if the maximum irreducible cycle in G is bounded in -.

Theorem 3. The coverage set found by our algorithm is nonredundant for --confine coverage if the maximum irreducible cycle in G is bounded in -.

Proof. Suppose there exists a redundant node v that can be deleted in the centralized algorithm. Let $k \leq \lfloor \tau / 2 \rfloor$ , all irreducible cycles in $\Gamma _ { G } ^ { k } ( v )$ will be less than - if the maximum irreducible cycle in G is bounded in -. Hence, v will be deleted by VPT. tu

We analyze the time complexity of Algorithm 2. We use growth-bounded graph (GBG) during this complexity analysis. GBG is widely accepted as a realistic graph model for wireless networks [34]. Line 1 needs to compute a MIS. Let $T _ { M I S }$ denote the time to compute a MIS. Line 2 selects r number of m-hop independent set from a MIS, which costs at most $r T _ { M I S }$ time and r can be bounded by a constant, as shown in Lemma 3. The initialization in lines 1-3 takes $O ( T _ { M I S } )$ time. Line 4 runs in r number of rounds. In lines 5- 8, each node v in a m-hop independent set simultaneously performs $\tau \mathrm { V P T } ,$ and attempts to delete itself and its 1-hop neighbors $N _ { v } .$ Each node w in $N _ { v } ,$ Node v needs to compute a minimum cycle basis in k-hop neighborhood graph of $w ,$ $\Gamma _ { G } ^ { k } ( w ) , k = \lfloor \tau / 2 \rfloor$ . Let $\Delta$ denote the maximum node degree in the network. $\Gamma _ { G } ^ { k } ( w )$ has at most $O ( \Delta ^ { k + 1 } )$ Þ number of nodes and $O ( \Delta ^ { k + 2 } )$ number of edges. Horton’s algorithm [31] is used to compute the MCB, which has $\hat { O } ( | V | | E | ^ { 3 } )$ time complexity and approximate $O ( | V | ^ { 1 . 5 } | E | )$ space complexity. Hence, line 8 requires at most $O ( \Delta ^ { 4 k + 8 } )$ time, or at most $O ( \Delta ^ { 2 \tau + 8 } )$ time. The total time complexity of Algorithm 2 is $O ( T _ { M I S } + \Delta ^ { 2 \tau + 8 } )$ . When maximum node degree $\Delta$ is assumed to be bounded in a constant, time complexity can be reduced to $O ( T _ { M I S } )$ . Currently, the best distributed deterministic algorithm [35] for MIS runs in $O ( \log ^ { * } n )$ time in GBG model, n being the number of nodes.

Lemma 3. The number of rounds of Algorithm 2 can be bounded by a constant in growth-bounded graphs.

Proof. Given G be a growth-bounded graph with polynomial function $f ( x )$ , let I be a MIS in $G ,$ and $I _ { 1 } , \ldots , I _ { r }$ be a partition of I and a group of maximal m-hop independent set, where $m \geq 1$ is a constant. Because $I _ { i } ,$ $1 \leq i \leq r - 1 .$ , is a maximal m-hop independent set, there is at most $f ( m )$ number of MIS nodes in m-hop neighbors of $v ,$ for each node v in $I _ { i } .$ Hence, $| I _ { i } | f ( m ) \geq$ $| I | ,$ where jIj denotes the number of nodes in I. So $\begin{array} { r } { f ( m ) | I | \geq f ( m ) \sum _ { i = 1 } ^ { r - 1 } | I _ { i } | \geq ( r - 1 ) | I | , } \end{array}$ and we have $r \leq$ $f ( m ) + 1$ . tu

# 6 EVALUATION

We conduct extensive simulations to evaluate the effectiveness of this design. We evaluate our Distributed Confine Coverage algorithm, denoted by DCC, by varying coverage granularity and sensing ratio. We compare this design with the state-of-the-art connectivity-based approach: Homology-Group-based Coverage, denoted as HGC, by Ghrist and colleague [10], which is currently the best centralized methods solely using connectivity information to perform coverage verification.

# 6.1 Impacts of Confine Sizes

We develop a coarse-grained time-slotted simulator in MATLAB. We deploy 1,600 nodes in a square area by a uniformly random distribution in the simulation. To facilitate the comparison with HGC approach, we use UDG model to build the connectivity graph. The average node degree is around 25. The outer boundary is precomputed prior to simulation by using a fine-grained recognition algorithm [23]. The simulator assumes steady network topology and reliable message delivery between nodes. We set the maximum communication range $R _ { c } = 1$ in all the simulations, and adjust sensing ranges according to $\gamma .$ . Under each configuration, our simulation takes 100 runs with random network generation, and reports the average. Ghrist and colleague homology-group coverage criterion is implemented based on a software package for computing simplicial complexes in MATLAB [36].

# 6.1.1 Quality of Partial Coverage

We examine the maximum coverage holes against variable confine sizes. Although confine coverage can achieve full or partial coverage with theoretical guarantees, it is still useful to examine the accurate geometric size of the coverage holes in the network scheduled by this DCC algorithm. In this simulation, we vary the confine sizes from three to nine, and calculate both maximum diameter and maximum area of holes. Figs. 7a and 7c show the experimental results. In comparison, the theoretical upper bounds for maximum diameter and maximum area of holes are also computed for each configuration, shown in Figs. 7b and 7d, respectively.

From the results, we can see that practical maximum diameters and areas are much less than the theoretical upper bounds. For example, a 9-confine coverage found by DCC has approximate maximum diameters equal to those of 6-confine or 7-confine coverage in the worst theoretical cases. This means that a --confine coverage with relatively large value of - often achieves a coverage quality much better than our conservative expectation for it. Comparatively, a confine coverage with small sizes, like $\mathbf { \hat { \rho } } _ { 3 }$ or 4-confine coverage, has less deviation between the worst cases in theory and practice. This phenomenon is not difficult to understand, because triangles and quadrangles are much easier to be embedded to form a convex region than other polygons in practical networks, and these convex embeddings are more likely to reduce the gaps between theory and practice than the nonconvex. An additional interesting observation is that the data lines in Figs. 7a and 7c are relatively smooth. It is mainly due to the following reasons. Node degree distribution tends to match the node spatial distribution in a connectivity graph based on UDG model. Our algorithm performs maximal node deletion while still meeting the coverage requirement, which mainly eliminates redundant nodes in densely deployed region. Hence, nodes in the reduced network exhibits a highly even spatial distribution, which makes maximum area or diameter of holes suffers little statistical fluctuation.

![](images/9bfb917d2cdcc688dd0583fba6c9a6cf83b7818d4ca7c1e2a3b2b2db5433d78a.jpg)



![](images/a1d331fa6031c5384282b020a04639052d587f292d2b6c8646e7f01fae0ebff4.jpg)



![](images/5630b05506b47f4f559052eb97e4fc6fc75beb88e2938c857aac788b7770cad4.jpg)



![](images/960ab9d2644497bab5c0f66b2454f700b87ce3d8bce716b62de177f48a017fba.jpg)



Fig. 7. The geometric size of coverage hole against confine size. The x-axis is the sensing ratio, . Figures (a) and (c) show the maximum diameters and areas of coverage holes in networks found by DCC, respectively; Figures (b) and (d) show the theoretical upper bounds of maximum diameters and areas of coverage holes, respectively. Legends indicate the confine sizes from 3 to 9.

# 6.1.2 Coverage Set Size

We examine the impacts of confine sizes on the coverage set. Intuitively, a confine coverage scheme based on a larger confine size will require less nodes to cover a target region. This simulation validates this intuition definitively, as shown in Fig. 8. The number of nodes in the coverage set decreases significantly with the increasing of confine size. Note that for one same network generation, we normalizedly set the nodes in a 3-confine coverage as one unit to measure the results of other larger confine coverages. The y-axis in Fig. 8 is the ratio of a size of --confine coverage to that of a 3-confine coverage, - from 3 to 9.

We further compare DCC with HGC with both variable ratios $\gamma$ and confine requirements. We change the confine requirements of maximum hole diameter from 0, 0.4, 0.8, and 1.2 while changing  from 2 to 1, that is, increasing $R _ { s }$ from 0:5Rc to $R _ { c }$ . Fig. 9 shows the results. The value of diameter is relative to communication range, that is, 0.4 means $0 . 4 R _ { c }$ due to $R _ { c } = 1$ . Maximum hole diameter of 0 is equivalently a full blanket coverage. The y-axis in Fig. 9 is the number of saved nodes  by DCC in different configurations. The number of saved nodes $\lambda$ is defined as follows: For a given coverage requirement, let $n _ { 1 }$ be the size of a coverage set found by HGC, and $n _ { 2 }$ is the possible minimum size a of coverage set found by DCC.  is equal to $( n _ { 1 } - n _ { 2 } ) / n _ { 1 }$ . We can see from Fig. 9 that our DCC algorithm saves more nodes when we increase the sensing diameter or permit larger confine size. The result verifies that the adjustable confine size of DCC makes DCC profit from both large sensing ranges and relaxed coverage requirements. Relatively, HGC fixes the confine size to be 3 and cannot exploit the variable sensing ranges and relaxed coverage requirements to customize confine sizes. Hence, it is advantageous and necessary to use DCC in these scenarios.

# 6.2 Impacts of Communication Models

In previous simulations, the results are given under the UDG model. It is worth pointing out that our algorithm is merely based on the connectivity information and does not rely on UDG models. To demonstrate the effectiveness of DCC algorithm in more general communication models, in this set of simulations we perform DCC in a network topology generated from practical trace data of GreenOrbs [37], as shown in Fig. 12a. GreenOrbs is an ongoing sensor network system for ecological surveillance in the forest.

![](images/b33aee7758e598a65997b3ff17b195b8311849339c9a5c1a55ebae444b8cdc36.jpg)



Fig. 8. Impacts of confine size.   
![](images/e7209cffe618d27bb7bfcf43c7dbaaed263520dcf4b17ec343545b144071d55e.jpg)



Fig. 9. DDC versus HGC.

![](images/ba968631dcbcd1391280794ef553d24ac1aa903aa7c2e88236577abed18a88d5.jpg)



Fig. 10. CDF of RSSI.   
![](images/871b04e342a49156e456a30601be8cca1d7192a0a7e1bc748a010ef8ee65427e.jpg)



Fig. 11. Trace-based results.

![](images/08b0a282506e5286615a2e15718cef57cf97bb9116597331e1c02c108f83f642.jpg)



(a)

![](images/188b414f5728690fcf8fb80cec6f975dd3e4f10ca57cce99d9758291ff1d8889.jpg)



(b)

![](images/d9db6c29ce8b1a32ade1c5979440a854075a9da52cef61bd4c45b28d29fd7c52.jpg)



(c）)

![](images/a3cd9db75812e410d5f1749696ee0b492adeb08219e4d2ece70e3339684662c9.jpg)



(d)

![](images/1ad8b84bb9ebcb3bdc00305495fa38203e6276ba0c4522bfdb2ee1087764769e.jpg)



(e)

![](images/36edcc8776780d991f596a926a0cb91117fa34851c4bf046446df3d2aec5f23c.jpg)



(f)   
Fig. 12. Perform DCC in practical trace topology. Figure (a) is the original network with 296 nodes plotted as circles and a set (26 number) of boundary nodes plotted as squares. Figures (b-f) show some network snapshots for 3, 4, 5, 6, 7 confine coverage, respectively. 17,8,6,5,4 numbers of inner circle nodes are left in Figures (b-f), respectively.

Currently, approximately 300 of sensors are randomly deployed in the forest. Clearly, such a topology in Fig. 12a significantly deviates from the UDG model.

This trace topology is obtained as follows: We gather all the data packet received from all nodes in a period of time. Each packet contains some (at most 10) records that indicate the neighbors having best received signal strength indication (RSSI) at one node in the moment of the creation of the packet. Hence, each RSSI record indicates one potential directed communication between two sensor nodes. We accumulate all these RSSI records of a period of time (two days) to construct the global communication graph. Finally, those directed edges are eliminated and only undirected edges that have the average RSSI greater than a threshold are reserved. Fig. 10 shows the empirical cumulative distribution function (CDF) of these RSSI associated with all edges. The y-axis represents the proportion of edges that are greater or equal than a threshold in all edges. The threshold of RSSI is selected to be near 85 dBm to utilize 80 percent undirected edges. Finally, a set of connected nodes are manually selected as the network boundary.

We then validate the effectiveness of DCC algorithm in the extracted trace topology. Similarly, we examine the impacts of confine sizes on the sizes of coverage set. The number of left inner nodes in the coverage set also decreases significantly with the increasing of confine size, shown in the Fig. 11. Especially compared with previous simulations shown in Fig. 8, we can observe from Fig. 11 that the number of left nodes decreases remarkably when confine size varies from three to five. This means that 4-confine and 5-confine coverage can contain much less nodes than 3-confine coverage in this trace topology. This phenomenon, we think, is mainly due to two aspects of reasons. First, there exist many links of long range in the trace topology, and thus larger confine size makes DCC have more chance to utilize those long links. Second, long narrow shape of this trace topology makes the boundary take more effects on the result. We further visually check the results generated by DCC. Figs. 12b ,12c, 12d, and 12e show a group of randomly selected results found by DCC for --confine coverage with parameter - from 3 to 7, respectively. These results further validate that DCC can tolerate the irregularity of communication and produce well-behaved outputs in practical network graphs.

# 7 CONCLUSIONS

As a crucial issue in wireless ad hoc and sensor networks, coverage problem is previously addressed either requiring accurate location information, range measurements, or using only connectivity information but forcing centralized computation and critical restriction on sensing and communication models. This work presents a practical graph theoretical framework to connectivity-based coverage problem in wireless ad hoc and sensor networks. We take the first attempt toward designing a distributed coverage algorithm to achieve configurable coverage requirements with using merely connectivity information. We formally prove the correctness of this design and evaluate it through extensive simulations and comparisons with the state-ofthe-art approach.

# ACKNOWLEDGMENTS

The authors are grateful for a variety of valuable comments from the anonymous reviewers. The first author conducted this research when he was visiting scholar at HKUST under supervision of Dr. Yunhao Liu, and is supported in part by NSFC under grants No. 60803040, No. 61003075, and No. 61190110.

# REFERENCES

[1] S. Meguerdichian, F. Koushanfar, M. Potkonjak, and M. Srivastava, “Coverage Problems in Wireless Ad Hoc Sensor Networks,” Proc. IEEE INFOCOM, 2001.   
[2] X. Wang, G. Xing, Y. Zhang, C. Lu, R. Pless, and C. Gill, “Integrated Coverage and Connectivity Configuration in Wireless Sensor Networks,” Proc. ACM First Int’l Conf. Embedded Networked Sensor Systems (SenSys), 2003.   
[3] X. Bai, S. Kumar, D. Xuan, Z. Yun, and T.-H. Lai, “Deploying Wireless Sensors to Achieve both Coverage and Connectivity,” Proc. ACM Int’l Symp. Mobile Ad Hoc Networking and Computing (MobiHoc), 2006.   
[4] H. Zhang and J. Hou, “Maintaining Sensing Coverage and Connectivity in Large Sensor Networks,” J. Ad Hoc and Sensor Wireless Networks, vol. 1, pp. 89-124, 2005.   
[5] G. Kasbekar, Y. Bejerano, and S. Sarkar, “Lifetime and Coverage Guarantees through Distributed Coordinate-Free Sensor Activation,” Proc. ACM MobiCom, 2009.   
[6] C. Zhang, Y. Zhang, and Y. Fang, “Detecting Coverage Boundary Nodes in Wireless Sensor Networks,” Proc. IEEE Int’l Conf. Networking, Sensing and Control (ICNSC), 2006.   
[7] O. Younis, M. Krunz, and S. Ramasubramanian, “Coverage without Location Information,” Proc. IEEE Int’l Conf. Network Protocols (ICNP), 2007.   
[8] Y. Bejerano, “Simple and Efficient K-Coverage Verification without Location Information,” Proc. IEEE INFOCOM, 2008.

[9] R. Ghrist and A. Muhammad, “Coverage and Hole-Detection in Sensor Networks via Homology,” Proc. ACM/IEEE Fourth Int’l Symp. Information Processing in Sensor Networks (IPSN), 2005.   
[10] V. de Silva and R. Ghrist, “Coordinate-Free Coverage in Sensor Networks with Controlled Boundaries via Homology,” Int’l J. Robotics Research, vol. 25, no. 12, pp. 1205-1222, 2006.   
[11] A. Tahbaz-Salehi and A. Jadbabaie, “Distributed Coverage Verification in Sensor Networks without Location Information,” Proc. IEEE 47th Int’l Conf. Decision and Control (CDC), 2008.   
[12] B. Liu and D. Towsley, “A Study of the Coverage of Large-Scale Sensor Networks,” Proc. IEEE Int’l Conf. Mobile Ad-Hoc and Sensor Networks (MASS), 2004.   
[13] S. Kumar, T. Lai, and J. Balogh, “On K-Coverage in a Mostly Sleeping Sensor Network,” Proc. ACM MobiCom, 2004.   
[14] L. Lazos and R. Poovendran, “Stochastic Coverage in Heterogeneous Sensor Networks,” ACM Trans. Sensor Networks, vol. 2, no. 3, pp. 325-358, 2006.   
[15] P. Manohar, S. Ram, and D. Manjunath, “Path Coverage by a Sensor Field: The Nonhomogeneous Case,” ACM Trans. Sensor Networks, vol. 5, no. 2, pp. 1-26, 2009.   
[16] M. Cardei and J. Wu, “Coverage in Wireless Sensor Networks,” Handbook of Sensor Networks: Compact Wireless and Wired Sensing Systems, ch. 19. CRC Press, 2005.   
[17] L. Wang and Y. Xiao, “A Survey of Energy-Efficient Scheduling Mechanisms in Sensor Networks,” ACM/Springer Mobile Networks and Applications, vol. 11, no. 5, pp. 723-740, 2006.   
[18] C. Gui and P. Mohapatra, “Power Conservation and Quality of Surveillance in Target Tracking Sensor Networks,” Proc. ACM MobiCom, 2004.   
[19] Q. Cao, T.F. Abdelzaher, T. He, and J.A. Stankovic, “Towards Optimal Sleep Scheduling in Sensor Networks for Rare-Event Detection,” Proc. ACM/IEEE Fourth Int’l Symp. Information Processing in Sensor Networks (IPSN), 2005.   
[20] O. Dousse, C. Tavoularis, and P. Thiran, “Delay of Intrusion Detection in Wireless Sensor Networks,” Proc. Seventh ACM Int’l Symp. Mobile Ad Hoc Networking and Computing (MobiHoc), 2006.   
[21] P. Balister, Z. Zheng, S. Kumar, and P. Sinha, “Trap Coverage: Allowing Coverage Holes of Bounded Diameter in Wireless SensorNetworks,” Proc. IEEE INFOCOM, 2009.   
[22] S. Ren, Q. Li, H. Wang, X. Chen, and X. Zhang, “Design and Analysis of Sensing Scheduling Algorithms under Partial Coverage for Object Detection in Sensor Networks,” IEEE Trans. Parallel and Distributed Systems, vol. 18, no. 3, pp. 334-350, Mar. 2007.   
[23] D. Dong, Y. Liu, and X. Liao, “Fine-Grained Boundary Recognition in Wireless Ad Hoc and Sensor Networks by Topological Methods,” Proc. 10th ACM Int’l Symp. Mobile Ad Hoc Networking and Computing (MobiHoc), 2009.   
[24] O. Saukh, R. Sauter, M. Gauger, P.J. Marro´ n, and K. Rothermel, “On Boundary Recognition without Location Information in Wireless Sensor Networks,” Proc. ACM/IEEE Int’l Conf. Information Processing in Sensor Networks (IPSN), 2008.   
[25] Y. Wang, J. Gao, and J.S. Mitchell, “Boundary Recognition in Sensor Networks by Topological Methods,” Proc. ACM MobiCom, 2006.   
[26] A. Kro¨ ller, S.P. Fekete, D. Pfisterer, and S. Fischer, “Deterministic Boundary Recognition and Topology Extraction for Large Sensor Networks,” Proc. 17th Ann. ACM-SIAM Symp. Discrete Algorithm (SODA), 2006.   
[27] F. Kuhn, T. Moscibroda, and R. Wattenhofer, “Unit Disk Graph Approximation,” Proc. ACM Joint Workshop Foundations of Mobile Computing (DIALM-POMC), 2004.   
[28] E.W. Chambers, V. de Silva, J. Erickson, and R. Ghrist, “Rips Complexes of Planar Point Sets,” Preprint, ArXiv:0712.0395, 2007.   
[29] P. Vismara, “Union of All the Minimum Cycle Bases of a Graph,” Electronic J. Combinatorics, vol. 4, no. 1, pp. 73-87, 1997.   
[30] M. Plotkin, “Mathematical Basis of Ring-Finding Algorithms in CIDS,” J. Chemical Documentation, vol. 11, no. 1, pp. 60-63, 1971.   
[31] J. Horton, “A Polynomial-Time Algorithm to Find the Shortest Cycle Basis of a Graph,” SIAM J. Computing, vol. 16, no. 2, pp. 358- 366, 1987.   
[32] D. Chickering, D. Geiger, and D. Heckerman, “On Finding a Cycle Basis with a Shortest Maximal Cycle,” Information Processing Letters, vol. 54, no. 1, pp. 55-58, 1995.   
[33] Y. Wang, W. Wang, and X. Li, “Efficient Distributed Low-Cost Backbone Formation for Wireless Networks,” IEEE Trans. Parallel and Distributed Systems, vol. 17, no. 7, pp. 681-693, July 2006.

[34] F. Kuhn, T. Nieberg, T. Moscibroda, and R. Wattenhofer, “Local Approximation Schemes for Ad Hoc and Sensor Networks,” Proc. Third ACM Joint Workshop Foundations of Mobile Computing (DIALM-POMC), 2005.   
[35] J. Schneider and R. Wattenhofer, “A Log-Star Distributed Maximal Independent Set Algorithm for Growth-Bounded Graphs,” Proc. 27th ACM Symp. Principles of Distributed Computing (PODC), 2008.   
[36] P. Perry and V. de Silva, “Plex: Simplicial complexes in MATLAB,” http://comptop.stanford.edu/u/programs/plex.html, 2006.   
[37] L. Mo, Y. He, Y. Liu, J. Zhao, S. Tang, X. Li, and G. Dai, “Canopy Closure Estimates with Greenorbs: Sustainable Sensing in the Forest,” Proc. Seventh ACM Conf. Embedded Networked Sensor Systems (SenSys), 2009.

![](images/bf951e4502999ee76ca73a799bb753cacdf5e99256bb2a5c6f9cc30d8cae6a5c.jpg)



Dezun Dong (S’09-M’10) received the BS, MS, and PhD degrees at National University of Defense Technology (NUDT), China, in 2002, 2004, 2010, respectively. He was a visiting scholar at the Department of Computer Science and Engineering at the Hong Kong University of Science and Technology from November 2008 to May 2010. He is currently an assistant professor at the School of Computer, NUDT, China. His research interests are wireless net-

works, distributed computing, and high-performance computer systems. He is a member of the IEEE.

![](images/6ca824224e009a8cb6c02df45fa45b9bc0517d4f2f177801565945c226ae11dc.jpg)



Xiangke Liao received the BS and MS degrees in computer science from Tsinghua University and National University of Defense Technology (NUDT), China, in 1985 and 1988, respectively. He is now a professor and the dean at the School of Computer, NUDT, China. His research interests include parallel and distributed computing, high-performance computer systems, operating system, and networked embedded system.

![](images/9fc618793c0ab1a0e83752a2d0f6836cb458b254b3fd0fa0644f91f6588a323d.jpg)



Kebin Liu received the BS degree from Tongji University, China, and MS and PhD degrees from Shanghai Jiaotong University, China. He is currently a post doc fellow at the Department of Computer Science and Engineering in the Hong Kong University of Science and Technology. His research interests include pervasive computing and wireless sensor networks.

![](images/cf5e7ac018324b7d7b416f57f687e015707e3d4778a877ec1ede764146f007be.jpg)



Yunhao Liu (M’02-SM’06) received the BS degree from the Automation Department at Tsinghua University, China, in 1995, and the MS and PhD degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is a professor at Tsinghua National Lab for Information Science and Technology, School of Software, and the director of MOE Key Lab for Information Security, Tsinghua University. He is also a

faculty member in the Department of Computer Science and Engineering at the Hong Kong University of Science and Technology. He is senior member of the IEEE.

![](images/e725e99ecc7ff6acedeea69c3049f37e519ca9094a81d11209d15a4a02a4e3c4.jpg)



Weixia Xu received the BS and MS degree in computer science from Nanjing University of Science & Technology and National University of Defense Technology (NUDT), China, in 1984 and 1993, respectively. He is a professor at the School of Computer, NUDT, China. His research interests include high-performance computer systems and microprocessor design.