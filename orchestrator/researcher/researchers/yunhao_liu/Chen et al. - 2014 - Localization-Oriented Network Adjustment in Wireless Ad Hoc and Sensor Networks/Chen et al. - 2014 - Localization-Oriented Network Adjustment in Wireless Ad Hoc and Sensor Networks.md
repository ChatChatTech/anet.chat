# Localization-oriented Network Adjustment in Wireless Ad-Hoc and Sensor Networks

Tao Chen, Member, IEEE, Zheng Yang, Member, IEEE, Yunhao Liu, Senior Member, IEEE, Deke Guo, Member, IEEE, and Xueshan Luo

Abstract—Localization is an enabling technique for many sensor network applications. Real-world deployments demonstrate that, in practice, a network is not always entirely localizable, leaving a certain number of theoretically non-localizable nodes. Previous studies mainly focus on how to tune network settings to make a network localizable. However, existing methods are considered to be coarsegrained, since they equally deal with localizable and non-localizable nodes. Ignoring localizability induces unnecessary adjustments and accompanying costs. In this study, we propose a fine-grained approach, Localizability-aided Localization (LAL), which basically consists of three phases: node localizability testing, structure analysis, and network adjustment. LAL triggers a single round adjustment, after which some popular localization methods can be successfully carried out. Being aware of node localizability, all network adjustments made by LAL are purposefully selected. Experiment and simulation results show that LAL effectively guides the adjustment while makes it efficient in terms of the number of added edges and affected nodes.

Index Terms—Localization, Localizability, Network Deployment, Wireless Ad-Hoc Networks, Sensor Networks.

# 1 INTRODUCTION

As the proliferation of wireless and mobile devices continues, a wide range of context-aware applications are deployed, including smart space, modern logistics, etc. In these applications, location information is the basis of other services, such as geographic routing, boundary detection, and network coverage control. In some other applications, such as military surveillance and environment monitoring, sensed data without location information are almost useless.

Localization in wireless ad-hoc and sensor networks is the problem that every node determines its own location. In this work, we focus on two-dimensional in-network localization [1]–[4], in which some special nodes (called beacons or anchors) know their global locations and the rest determine their Euclidean coordinates by measuring the Euclidean distances to their neighbors.

Due to hardware or deployment constraints, a network can be partially localizable given distance measurements and locations of beacons, that is to say, some nodes have unique locations while others do not. Theoretical analysis [5] indicate that, unless networks are highly dense and regular, in most cases, it is unlikely that all nodes in a network are localizable. In practice, a wireless ad-hoc or sensor network cannot be excessively dense because the mechanism of topology control are usually used to alleviate collision and interference, ignoring the localizability of the network. We find supporting evidences from two real sensor network systems OceanSense [6] and GreenOrbs [7]. Networks are not entirely localizable in their initial deployments. Based on graph rigidity theory, network localizability [8] and node localizability [5], [9] are studied which solve the locationuniqueness of a network or a single node, respectively. So far one can distinguish localizable and non-localizable nodes in theory.

To locate non-localizable nodes, existing solutions mainly focus on how to tune network settings. A first attempt is to deploy additional nodes or beacons in application fields. Such incremental deployment increases node density and creates abundant inter-node distance constraints, thus enhancing localizability. However, the attempt lacks feasibility, since the additional nodes should be placed in the vicinity of non-localizable nodes, whose locations are just unknown. Using mobile nodes (e.g., beacons) is another choice. The controlled motion of beacons provides thorough information for localization, but also incurs adjustment delay and controlling overheads [10]–[12].

Both incremental deployment and the use of mobile node require additional hardware cost which may not be available in many applications. A more practical and convenient way is to increase the distance ranging capability of sensor nodes. Enhanced nodes can measure the distances to a larger number of their nearby nodes. In popular ranging techniques, such as Time of Arrival (ToA) and Received Signal Strength (RSS), the capability enhancement can be achieved by augmenting the transmitter power output.

One approach is to augment the transmitting power of nodes stage-by-stage until all nodes become localizable, which causes multiple rounds of configuration dissem-

Tao Chen, Deke Guo and Xueshan Luo are with the Key lab of Information System Engineering, College of Information Systems and Management, National University of Defense Technology, Changsha, China. E-mail: {emilchenn, guodeke}@gmail.com, xsluo@nudt.edu.cn. Zheng Yang and Yunhao Liu are with the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong, and Tsinghua National Lab for Information Science and Technology, School of Software, Tsinghua University, China. Email: {yangzh, liu}@cse.ust.hk.

ination and data collection in a network. A straightforward single-round solution is maximizing the ranging capability. The principle drawback of power maximization is that it introduces many unnecessary distance measurements, which are obtained with costs. Anderson et al. [13] propose a single round approach to construct localizable networks. In their method, all nodes set their power doubly or triply of the original values. This method coarse-grained however, since it equally treats localizable and non-localizable nodes. Ignoring localizability induces a mass of meaningless adjustments and accompanying costs. In this study, we propose Localizability-aided Localization (LAL). We adopt the the sufficient condition of node localizability [9] to identify localizable and non-localizable nodes. A fine-grained configuration is computed systematically according to network topology and localizability information. Theoretical analysis guarantees a tuned network is localizable and thus well-prepared for localization.

The main contributions of this study are as follows: First, being aware of node localizability, adjustments made by LAL are purposefully selected, avoiding meaningless ranging and communication costs. Second, LAL is light weight, working properly with existing localization methods (e.g., Sweeps [3], etc.) without incompatibility. Finally, we implement LAL on a real sensor network consisting of 100 nodes. The deployment data are collected from in-situ measurement in a wild application field.

The rest of the paper is organized as follows. Related work is discussed in Section 2. We introduce graph rigidity theory briefly and discuss the state-of-the-art approach to construct localizable graph in Section 3. Theoretic foundations for LAL are provided in Section 4. Section 5 presents the design and implementation of LAL. Some discussions are provided in Section 6. Evaluation is discussed in Section 7. We conclude the work in Section 8. This is an extended work of a conference publication [14]. We add Section 3, 6, the proofs in Section 4, detail descriptions of the proposed algorithms in Section 5, and more evaluation results in Section 7.

# 2 RELATED WORK

There are two major categories of localization methods: range-free and range-based methods. Range-free localization methods [15], [16] merely use neighborhood information (such as node connectivity and hop count) to determine node locations. Range-based approaches [1]–[3], [17]–[20] assume nodes are able to measure internode distances, and can provide more accurate localization results. Many range-based algorithms adopt distance ranging techniques, such as Radio Signal Strength (RSS) [1], [19] and Time Difference of Arrival (TDoA) [17], [20], [21]. RSS maps received signal strength to distance according to a signal attenuation model, while TDoA measures the signal propagation time for distance calculation.

The majority of localization algorithms [2], [21] assume a dense network such that iterative trilateration (or multilateration) can be conducted. Other methods [3] record all possible locations in each positioning step and prune incompatible ones whenever possible. Those localization algorithms only try to localize as many nodes as possible, however, do not concern the rest non-localizable part of the network. The existence of non-localizable networks leads to the research on location-uniqueness problem (a.k.a, localizability problem). Goldenberg et al. [5] first propose non-trivial necessary and sufficient conditions of location-uniqueness of specific node. Yang and Liu [9] further derives currently the best necessary and sufficient conditions of node localizability.

In recent years, a few works are published on localization in non-localizable networks. Pathirana et al. use a mobile robot to localize nodes [22]. They obtain distance information between robot and fixed nodes using RSS data, so as to reduce the number of beacons required to uniquely localize a network. However, they require the availability of precise velocity and acceleration of mobile robot. Sichitiu and Ramadurai use a GPS equipped mobile node to localize fixed nodes by measuring the distance between the mobile node and fixed ones [23]. Different from the above approaches which use a mobile node with known location information, Priyantha et al. propose a approach which only requires the distance information between mobile node and fixed ones [10]. Wu et al. propose a similar approach with the assumption that each node can move around and measure the distances to its neighbors and the relative distances between successive positions along its trajectory [12]. However, the assumption of availability of mobile nodes is costly and not scalable, and restricts the application of the approach. In contrast to these mobility-based approaches, Anderson et al. propose a graph manipulation method to assure the network localizability [13]. They identified graphical properties which can ensure unique localizability, and propose a $G ^ { 2 }$ approach to make the 2- Gconnected graph localizable and a $\mathbf { \hat { \boldsymbol { G } } ^ { 3 } }$ approach to obtain Ga trilateration graph based on a connected graph. Both approaches treat all vertices in the graph as a whole, which is more coarse-grained than LAL.

# 3 PRELIMINARIES

# 3.1 Localizability

The ground truth of a network can be modeled by a distance graph $G = ( V , E )$ , where  denotes the set of G V, E Vvertices (wireless devices, e.g. sensor node, RFID) and denotes the set of edges. For $i , j ~ \in ~ V , ( i , j ) ~ \in ~ E$ if E i, j V, i, j Ethe distance between  and  can be measured or both i jof them are in known locations (e.g. beacon nodes). We assume is connected and has at least four vertices and Gfocus on 2D space in the following analysis. Localization is to find a map  (a.k.a., realization) from vertices in p Gto points in a Euclidean space. If  respects the distance pconstraints between any pair of vertices as depicted in $E ,$ is a feasible realization of graph . Two realizations are p Gequivalent if they are identical under translations, rotations and reflections. A distance graph  has at least one Gfeasible realization which represents the ground truth of the corresponding network. Formally,  is embeddable Gin 2D space and all pairwise distances are compatible.

A realization is generic if the vertex coordinates are algebraically independent. Like many previous work on graph rigidity theory [24], [25] and network localization [3], [5], [8], [12], [13], [26], we focus on generic cases in our study, since the set of generic realizations is dense in the realization space and almost all realizations are generic [27]. We omit the word generically hereafter. A graph is called rigid if one cannot continuously deform its realizations while preserving distance constraints, and redundantly rigid if it remains rigid upon removal of any single edge [28]. A graph is globally rigid if it is uniquely realizable [27].

Jackson and Jordan [24] summarize the reasons of ´ realization non-uniqueness, and present the following theorem.

Theorem 1 ( [24]). A graph with $n \geq 4$ vertices is globally nrigid in 2 dimensions if and only if it is 3-connected and redundantly rigid.

A graph $G = ( V , E )$ is called -connected (for $k \in \mathbb { N } )$ $\mathrm { i f } \ | V | > k$ Gand $G - X$ kis connected for every set $X \subseteq V$ Vwith $| X | < k$ G X X V. In other words, no two vertices in  are X < k Gseparated by removing fewer than  other vertices.

kEren et al. [8] further prove that a network is uniquely localizable if and only if its distance graph is globally rigid and it contains at least three beacons.

Yang and Liu [9] present necessary and sufficient conditions of node localizability, which can be used to identify localizable and non-localizable nodes in a network.

Theorem 2 ( [9]). In a distance graph $G = ( V , E )$ with a set $B \subset V \ o f \ k \geq 3$ G V, Evertices at known locations, a vertex is B V klocalizable if it is included in the redundantly rigid component inside which there are three vertex-disjoint paths to three distinct vertices in .

A redundantly rigid component is a maximal redundantly rigid subgraph in . Theorem 2 is a sufficient Gcondition of node localizability, denoted by RR3P for short, where RR and 3P stand for redundant rigidity and three vertex-disjoint paths, respectively.

# 3.2 Construction of Localizable Graph

Given a non-localizable graph, it is important to make it localizable through incremental construction. Define $G ^ { 2 }$ as $( V , E \cup E ^ { 2 } )$ where $( i , j ) \in E ^ { 2 } { \mathrm { ~ i f ~ } } i \neq j$ and $\exists k \in V$ V, Esuch that $( i , k )$ and $( j , k ) \in E .$ E i j. Similarly, define $G ^ { 3 }$ Vas $( V , E \cup E ^ { 2 } \cup \dot { E ^ { 3 } } )$ j,where $( i , j ) \in E ^ { 3 }$ if $i \neq j$ and $\exists k \in V$ V, E Esuch that $( i , k ) \in E$ and $( j , k ) \in E ^ { 2 }$ i j k V. Based on Theorem i, k E j, k E1, Anderson et al. present the following result.

Theorem 3 ( [13]). Let $G = ( V , E )$ be a 2-edge-connected G V,graph in 2-dimension space. Then $G ^ { 2 }$ is globally rigid.

is called -edge-connected, if $| V | > 1$ and $G - F$ is G lconnected for every set $F \subseteq E$ V > G Fof fewer than  edges. A F E-connected graph is also -edge-connected.

$G ^ { 2 }$ kis obtained from  by adding edges between two-G Ghop vertex pairs. Note that in some ranging techniques (e.g. RSS and ToA), RF signal is used for distance measurement. Thus the communication range approximately represents the maximum ranging distance. In a wireless network, doubling the communication range will produce a new graph which has $G ^ { 2 }$ as a subgraph. Similarly, $G ^ { 3 }$ Gcan be obtained by tripling the communication Grange. Anderson et al. also prove that, if $G = ( V , E )$ is connected, $G ^ { 3 }$ Gis globally rigid (specifically, $G ^ { 3 }$ V, Ecan be Glocalized by iterative trilateration).

# 4 THEORETIC FOUNDATION

# 4.1 Component Tree

To support fine-grained network adjustment, we decompose a graph into components according to connectivity. A 2-connected component in a graph  is a maximal Gsubgraph of  without articulation vertex whose removal Gdisconnects . A graph  is minimally rigid if  is rigid, and $G - e$ Gis not rigid for all $e \in E .$ G. Jackson and G e e EJordan [24] summarize the link between rigidity and 2- ´ connectivity.

Lemma 1 ( [24]). Let $G = ( V , E )$ be minimally rigid with $| V | \geq 3$ G V,. Then  is 2-connected.

Based on Lemma 1, we obtain the following theorem.

Theorem 4. Given a connected distance graph  with more Gthan 3 vertices, all beacons and localizable vertices recognized by RR3P in  are in the same 2-connected component.

Proof: According to Theorem 2, beacons and localizable nodes are included in a redundantly rigid component which is 2-connected suggested by Lemma 1.

We call the 2-connected component in Theorem 4 anchor component (denoted by $G _ { A } { \bar { ) } }$ for convenience.

Theorem 5. Suppose $G = ( V , E )$ is a 2-connected graph with a set  of $k \geq 3$ G V, Ebeacons and $B \subset V$ . Let $V _ { N }$ denote B k Bthe set of non-localizable vertices, and $E _ { N }$ V Vdenote the set of edges $( i , j ) , i \in V _ { N }$ and $( i , j ) \in E ^ { 2 }$ E. Then, $G = ( V , E \cup E _ { N } )$ i, j iis localizable.

Proof: The theorem holds for the trivial case that $V _ { N } ~ = ~ \emptyset$ . For $V _ { N } \neq \emptyset ,$ if there is no localizable vertex V Vin  other than beacons, adding $E _ { N }$ to  results in $G ^ { 2 } ,$ G E G Gwhich is localizable according to Theorem 3. Otherwise, there exists a localizable vertex l $\in \textit { V } - B .$ . For any $v _ { n } \ \in \ V _ { N }$ v, two vertex-disjoint paths $p _ { 1 }$ Vand $p _ { 2 }$ can be v Vfound connecting $v _ { n }$ and $v _ { l }$ p psince  is 2-connected. vAs illustrated in Fig. 1(a), $p _ { 1 }$ and $p _ { 2 }$ G form a cycle . Suppose $v _ { 1 }$ and $v _ { 2 }$ p pare two direct neighbors of $v _ { l }$ Cin v v. Consider the worst case that $C$ vcontains only one localizable vertex, thus $v _ { 1 }$ and $v _ { 2 }$ are non-localizable. As $v _ { l }$ v vis localizable, it has 3 vertex-disjoint paths to 3 vbeacons, and all three paths are inside the redundantly rigid component (denoted by RRC) of $B .$ Adding $E _ { N }$ to  will connect $v _ { 1 }$ to all neighbors of $v _ { l }$ . Thus, $v _ { 1 }$ is G v v vincluded by the RRC since it connects 4 vertices that are originally in RRC. And $v _ { 1 }$ has three vertex-disjoint vpaths to three beacons in RRC no matter whether or not it stands on one of the three paths of $v _ { l }$ (an example vis shown in Fig. 1(b)). Theorem 2 ensures that $v _ { 1 }$ is localizable in $G \overset { \vartriangle } { = } ( V , E \cup E _ { N } )$ . For the same reason, $v _ { 2 }$ is Glocalizable. Hence $\dot { C } ^ { 2 }$ E E vis localizable due to Theorem 3 as CC is 2-connected and contains three localizable vertices. As a result, $v _ { n }$ is localizable in $G = ( V , E \cup E _ { N } )$ . Since $v _ { n }$ vis arbitrarily chosen, $G = ( V , E \cup E _ { N } )$ Eis localizable ventirely. □

![](images/d0bf051125f70320cfeae60998bc270605febaed56b8b8f2788373f2925351e1.jpg)



(a) Two vertex-disjoint paths can be found from vn to vl.

![](images/2969098356e953de1272ca0a575f926669884ffd169506177b16344bf0979199.jpg)



(b) v1 is connected to three neighbors of vl which are on the three vertex-disjoint paths to three beacons.   
Fig. 1. Proof of Theorem 5. Red dots are beacons.

Note that beacons are not required to be deployed together in one hop distance in Theorem 5. A direct result of the theorem is that, if we add $E _ { N }$ to the anchor component, $G _ { A }$ becomes localizable. $G _ { A }$ can be seen as Glocalizable in the following analysis.

We decompose a graph into 2-connected components. Except for the anchor component, all of them are nonlocalizable. We classify them into two categories, as illustrated in Fig. 2. Category I has two inter-connected vertices, and is trivially 2-connected. Category II has at least three vertices. The anchor component is a category II component.

![](images/f720fae9e9da26e91c3f707aa0576c86a3ca1d2df9cf254fb9e193be16984080.jpg)

![](images/b55ed3b74b7e4c3aa1d27a5a3e7a5385406c7de7838117bc50c6d54155dc571e.jpg)  
Fig. 2. Two categories of 2-connected components.

Two components sharing a common vertex are adjacent. They cannot have more than one common vertex, or they should be merged into one. We construct component tree $T = ( V _ { T } , \breve { E _ { T } } )$ of $G = ( V , E )$ as follows. Any vertex $i \in V _ { T }$ corresponds to a 2-connected component iof and $( i , j ) \in E _ { T }$ if the correspondents of and are G i, j Eadjacent in . For convenience, let $G _ { A }$ i jbe the root of . G G TFig. 3 illustrates the construction of a component tree Tfrom . We decompose  into several 2-connected com-G Gponents and connect neighboring ones in . Following such construction,  contains no cycle.

TLocation information, as well as localizability, diffuses from the root of $T$ to leaf vertices along tree edges. TAnother issue needs to be addressed here is the path from the root to any tree vertex in $T .$ . The category Tpermutation of the components along a path determines how to make adjustments in our solutions. For simplicity, we use a string such as $\because \mathrm { I I } + \ldots + \mathrm { I } ^ { \prime \prime }$ to describe the categories of components on a path, from the root to a destination component. Taking Fig. 3 as an example, the path to $G _ { 4 }$ is denoted by “II+I+II+I”. We call such a Gstring “path string” henceforth.

# 4.2 Component Based Adjustment

Before discussing component based adjustment, we define the operation of vertex augmentation.

Definition 1 (Vertex Augmentation). In a graph $G =$ $( V , E )$ , the vertex augmentation of $v \in V$ G(denoted by $v ^ { k } , k \in \mathbb { N } )$ v V is to connect  and its -hop neighbors in $\dot { G }$ $( i \leq k )$ .

In a distance graph $G = ( V , E )$ of a network, for any $v \in V , \ v ^ { n }$ G V, Ecan be achieved by increasing the ranging v V vcapability of  (more accurately, ’s correspondents) by times.

Since there are two categories of 2-connected component according to the classification in this work, a path string of a component can be decomposed into a series of overlapping segments of two consecutive categories. There are four cases: “I+I”, “I+II”, “II+I”, and $^ { \prime \prime } \mathrm { I I } { + } \mathrm { I I } ^ { \prime \prime }$ . If we provide adjustment solutions for all four cases to make the corresponding components localizable, the entire network becomes localizable by applying these solutions from the root to leaves in a component tree. When discussing the solutions of the four cases, we assume the former component has already been manipulated and thus localizable. The assumption is reasonable because $G _ { A }$ is the root and made localizable according Gto Theorem 5.

![](images/ac0147217613b7041a88ac6b89402bbd3c50cc52661b90564394a7c732aaca04.jpg)



(a) Graph decomposition

![](images/ea07631b1033b2aa2587b03ae63236c4baed0ad5b8bea4f8a9e7970f91c97f50.jpg)



(b) Component tree   
Fig. 3. Construction of component tree.

# Case “II+I”

Suppose two corresponding components are $G _ { 1 }$ and $G _ { 2 } ,$ as shown in Fig. 4. The vertex $v _ { 1 }$ Gis localizable and Ghas two localizable neighbors $v _ { 2 }$ vand $v _ { 3 }$ in $G _ { 1 }$ . Suppose the neighbor of $v _ { 1 }$ in $G _ { 2 }$ is $v _ { 4 }$ v G. The operation $v _ { 4 } ^ { 2 }$ adds two edges $( v _ { 4 } , v _ { 2 } )$ Gand $( v _ { 4 } , v _ { 3 } )$ in $E ^ { 2 } ,$ v which makes $v _ { 4 }$ v , v v , v E vlocalizable by connecting it to three localizable vertices.

![](images/5930f0d9d1a81572322495923fb8d65727402fc41d9953d0324eec9eb7d690ef.jpg)



Fig. 4. Case ${ } ^ { 6 6 } | | + | { } ^ { 9 } { : }$ localize the category I component by adding two edges. Solid lines are edges in and dashed lines are edges in $E ^ { 2 }$ .

# Case “II+II”

Fig. 5 shows two category II components $G _ { 1 }$ and $G _ { 2 } .$ . The vertex $v _ { 1 }$ G Gis localizable, and has two localizable neighbors $v _ { 2 }$ and $v _ { 3 }$ in $G _ { 1 } ,$ and two non-localizable neighbors $v _ { 4 }$ and $v _ { 5 }$ vin $G _ { 2 } , G _ { 2 } ^ { 2 }$ is globally rigid according v v G Gto Theorem 3. Similar to the case $^ { \prime \prime } \mathrm { I I } { + } \dot { \mathrm { I } } ^ { \prime \prime } ,$ 4 and $v _ { 5 }$ are made localizable by $v _ { 4 } ^ { 2 }$ and $v _ { 5 } ^ { 2 }$ . Then $G _ { 2 } ^ { 2 }$ v vis localizable v v Gsince it is globally rigid and has three vertices whose location can be uniquely determined by calculations.

![](images/b25a2913464ed37d25b68fa79a1296825d68761ba1b4d21a09e399f08b2dd8ac.jpg)



Fig. 5. Case “II+II”: $G _ { 2 } ^ { 2 }$ is localizable through $v _ { 4 } ^ { 2 }$ and $v _ { 5 } ^ { 2 }$ G v vSolid lines are edges in , and dashed lines are edges in $E ^ { 2 }$ .

# Case “I+I”

Suppose the two category I components are $G _ { 2 }$ and $G _ { 3 } , v _ { 2 }$ is the articulation vertex of $\hat { G } _ { 2 }$ and $G _ { 3 } ,$ G and two G vvertices $v _ { 1 }$ and $v _ { 3 }$ G Greside in two components, respectively, v vas shown in Fig. 6. Because all paths start with a category II component $G _ { A } , G _ { 2 }$ must have a parent component $G _ { 1 }$ . G GNo matter the category of $G _ { 1 } , v _ { 1 }$ Ghas at least one localizable neighbor $v _ { 4 } . \ v _ { 3 } ^ { 2 }$ G vonly adds a single edge $( v _ { 1 } , v _ { 3 } )$ , and $v _ { 3 }$ v v v , vstill does not fulfill the sufficient condition in Theorem v2. To make $v _ { 3 }$ localizable, at least one edge such as $( v _ { 3 } ,$ $v _ { 4 } )$ v should be added. That is to say, we should do $v _ { 3 } ^ { 3 }$ vin vthe original topology to make $G _ { 3 }$ localizable.

# Case “I+II”

Suppose the two components are $G _ { 2 }$ and $G _ { 3 }$ as shown G Gin Fig. 7. Similar to the case “I+I”, 33 is needed to

![](images/27873a00b7233adcb615848b7772f3413d47049369c2bec5b7fae90eb0174aac.jpg)



Fig. 6. Case $^ { * } | + | ^ { * } \colon v _ { 3 } ^ { 3 }$ is needed to make $G _ { 3 }$ localizable. v GSolid lines are edges in . The dashed line is an edge in $E ^ { 2 }$ E, and the dotted line is an edge in $E ^ { 3 }$ .

make $v _ { 3 }$ localizable. Then, $v _ { 4 } ^ { 2 }$ makes $v _ { 4 }$ localizable. Since $G _ { 3 } ^ { 2 }$ v v vis globally rigid according to Theorem 3 and the Glocations of three vertices $v _ { 2 } , v _ { 3 } ,$ and $v _ { 4 }$ can be uniquely determined, all vertices in $G _ { 3 }$ v vare localizable.

![](images/4404224d5c2b92652b73648e612f0321240b31f03700fae1b5fda1d22aeb167d.jpg)



Fig. 7. Case “I+II”: 33 (or 34 ) is needed to make $G _ { 3 } ^ { 2 }$ localizable.

# 5 LAL DESIGN AND IMPLEMENTATION

The previous section established the theoretical foundation of LAL. In this section, we discuss LAL design and implementation. Being aware of node localizability, LAL can effectively guide the adjustment of network, while traditional approach could only make indistinctive augmentations. Basically, LAL consists of three major steps, as depicted in Fig. 9.

![](images/6468b8e5fe52432b007eae706a8d1475a8be2b6a7acc8c5b84c259312598e28e.jpg)



Fig. 8. Workflows of traditional approaches and LAL.

Step 1: Localizability testing. When a network is deployed in an application field, due to some systematic or environment factors unpredictable in the design phase, it may be not ready for localization. Hence, node localizability testing is conducted foremost in LAL, which identifies localizable and non-localizable nodes in a network for further adjustment.

Step 2: Structure analysis. To support fine-grained manipulation, we decompose a distance graph into $2 \AA ^ { - }$ connected components. These components are organized in a tree structure and the one containing beacons is the root. Adjustments are conducted along tree edges from the root to leaves.

Step 3: Distinctive adjustment. LAL treats nodes differently according to their localizability and places in the component tree. Through vertex augmentation, LAL converts all non-localizable in one round. The networks tuned by LAL are localizable and can be localized by existing localization approaches.

Step 1 can be done by applying Theorem 2. Given a specific node, its localizability relies on the property of disjoint paths and redundant rigidity, which can be tested in polynomial time by network flow algorithms and the pebble game algorithm [25], respectively. In step 2, a graph is decomposed into 2-connected components using depth-first search [29]. In step 3, node adjustments described in Section 4 are conducted along the paths of the component tree starting at the root. We present Algorithm 1 to detail step 3.

Algorithm 1 LAL Basic   
Require: A 2-connected component $G_i$ , the component tree $CTree$ , and localizability vector.

1: if $G_i$ is $G_A$ then

2:    for each non-localizable vertex $v_i \in G_A$ do

3:    Vertex augmentation $v_i^2$ 4:    end for

5: else

6: $G_j \leftarrow parent[G_i]$ 7:    Find out which category do $G_i$ and $G_j$ belong to.

8:    Apply corresponding solution in Section 4 to add edges.

9: end if

10: for each child component $G_k$ of $G_i$ in $CTree$ do

11: $parent[G_k] \leftarrow G_i$ 12: $LAL\_Basic(G_k, CTree)$ 13: end for

In Algorithm 1, edges are added by vertex augmentation of all non-localizable vertices in $G _ { A }$ , and $\bar { G } _ { A }$ is lo-G Gcalizable according to Theorem 5. For a component other than $G _ { A } ,$ the categories of it and its parent component Gare used to guide adjustments as described in Section 4. Algorithm 1 recursively repeats until all components get manipulated. After applying Algorithm 1, the entire network is localizable. Popular localization algorithms can then be used seamlessly to localize all nodes in the network without incompatibility.

Proposition 1. Given the locations of localizable nodes, for any non-localizable node  in a connected graph $G = ( V , { \dot { E } } )$ , v G V, E can be localized by Sweeps [3] after the execution of vLAL Basic.

node in Proof: Case 1: $\dot { G } _ { A } , L A L$ v ∈ GABasic builds $\ v \in \ G _ { A }$ . If there is no localizable $G _ { A } ^ { 2 }$ . As proved in [3], $G _ { A } ^ { 2 }$ G Gcan be localized by Sweeps since $G _ { A }$ Gis 2-connected. If Gthere is only one localizable node l in $G _ { A }$ , for any nonlocalizable node $v _ { n , \ l }$ v G, there exists a cycle  which contains both $v _ { n }$ v Cand l as shown in Fig. 1. So all nodes including $v _ { n }$ v vcan be localized by Sweeps according to [3], because $C ^ { 2 }$ is a bilateration graph. If there are more than one localizable nodes, for any non-localizable node $v _ { n } ,$ we vcan find a path between two localizable nodes which passes $v _ { n } .$ . Suppose there are $i > 2$ nodes on the path, as vshown in Fig. 9. $v _ { 1 }$ and $v _ { 2 }$ i >are the two localizable nodes, and $v _ { 3 } , v _ { 4 } , . . . , v _ { i }$ v vare non-localizable. As discussed in the v v vproof of Theorem $5 , \ v _ { 3 }$ is localizable after $v _ { 3 } ^ { 2 } .$ . Since all v vnon-localizable nodes are augmented, the subgraph with added edges has a bilateration ordering and can be localized by Sweeps. Thus we have proved the proposition for the cases that $v \in G _ { A }$ .

Case 2: $v \not \in G _ { A }$ v G. is either in a category II component v / G vwith three localizable nodes or in a category I component but connected to three localizable nodes after the execution of $L A L$ Basic according to the analysis in Section 4. In both cases, a bilateration ordering exists, so  can be localized by Sweeps. □

![](images/5768d9884f30f9a37d5a17dcf0e6bdec5eb41921cc1721621fdc6c5ce0cbcc6e.jpg)



Fig. 9. Proof of Proposition 1, when $v \in G _ { A }$ and more v Gthan one nodes are localizable. Solid lines are edges in , and dashed lines are edges in $E ^ { 2 }$ .

To reduce the number of redundant edges added in category II component, we analyze the graph properties of these components and find the following observations in the original communication graph.

Observation 1: In $G _ { A } ,$ , some non-localizable vertices Ghave one localizable neighbor. As shown in Fig. 1, the localizable vertex $v _ { l }$ has at least three vertex-disjoint vpaths to three beacons. Adding two edges which connect two neighbor vertices on different vertex-disjoint paths to the non-localizable vertex (e.g. 1) is enough to make vthe vertex localizable according to Theorem 2. Moreover, only one edge is needed if a non-localizable vertex has two localizable neighbors in $G _ { A }$ .

GObservation 2: If a non-localizable vertex has three or more localizable vertices within two-hop distance, connecting it to three localizable vertices makes it localizable.

Observation 3: Some globally rigid components are not localizable in the original network topology due to the lack of beacons. If three nodes are adjusted to be localizable in a globally rigid component, the component is immediately localizable without extra manipulation.

We revise LAL Basic and propose a heuristic algorithm LAL Heuristic. The difference between the two algorithms lies in the way they add edges in category II components. LAL Heuristic uses a function named Add Heuristic to add edges instead of vertex augmentation. The pseudo-code of the function is shown in Algorithm 2. We omit the implementation of applying three observations in the pseudo-code, and provide descriptions in the following explanation. If $G _ { A }$ is used Gas an input of Add Heuristic, the algorithm first finds all non-localizable neighbors of localizable vertices, and adds edges for each non-localizable one according to Observation 1. Because disjoint paths from a localizable vertex to beacons are found and memorized in Step 1, only a search for non-localizable neighbor with linear complexity is required to implement line 8. Those nonlocalizable neighbors are then marked as localizable. Each time a new vertex is marked localizable, Observation 3 is applied by re-examining the localizability of the corresponding component. From line 14 to line 25, Observation 2 and 3 are repeated to add edges to make more vertices localizable. Note that not all vertices in the component are localizable after the iterative process. From line 26 to 28, the same square operation as used in $L A L _ { - }$ Basic is adopted to make those non-localizable vertices localizable. The correctness of Algorithm 2 is guaranteed by Theorem 1 and Theorem 5.

Algorithm 2 Add Heuristic   
Require: A 2-connected component $G_{i}$ , and localizability vector of vertices.

1: if $G_{i}$ is $G_{A}$ then

2:    for each non-localizable vertex $v_{j} \in G_{i}$ do

3:    if $v_{j}$ has localizable neighbor then

4:    Add $v_{j}$ into a set $V_{D}$ .

5:    end if

6:    end for

7:    for each vertex $v_{j} \in V_{D}$ do

8:    Add edges based on Observation 1.

9:    Mark $v_{j}$ localizable.

10:    Apply Observation 3.

11:    end for

12: end if

13: flag ← 1

14: while not all vertices in $G_{i}$ are localizable and flag == 1 do

15:    flag ← 0

16:    for non-localizable vertex $v_{j} \in G_{i}$ do

17:    num ← amount of localizable 2-hop neighbors

18:    if num ≥ 3 then

19:    Add edges based on Observation 2.

20:    Mark $v_{j}$ as localizable.

21:    flag ← 1

22:    Apply Observation 3.

23:    end if

24:    end for

25: end while

26: for each vertex $v_{k}$ marked non-localizable in $G_{i}$ do

27:    Vertex augmentation $v_{k}^{2}$ 28: end for

# 6 DISCUSSION

We find that the network topology is a byproduct of some basic services in ad hoc and wireless sensor networks, such as data collection [30], thus its collection induces none or little additional overhead. Inspired by this fact, this paper naturally adopts the centralized scheme. Actually, a distributed implementation may cause even more communication overhead, which mainly comes from the localizability testing part. In distributed implementation of Pebble Game algorithm, each node must send a message to neighbors once the pebble number changes. So the message complexity is ${ \hat { O } } ( | V | | E | )$ . The O V Emost recent distributed algorithm for maximum flow problem has $O ( | V | ^ { 2 } | E | )$ message complexity [31]. So we O V Ecan learn that the distributed implementation of LAL has at least $O ( | V | ^ { 2 } | E | )$ complexity. In addition, the main O V Ecommunication overhead of centralized LAL comes from the collection of topology data and the dissemination of adjustment solution. Even if we use flooding for both tasks, the message complexity is only $O ( | V | ^ { 2 } )$ .

O VWe discuss the computational complexity of of LAL according to the design and implementation described in Section 5. In Step 1, we use the pebble game algorithm [25], which has complexity of $\hat { O } ( | V | ^ { 2 } )$ , to find redun-O Vdantly rigid components, then use the classical Ford-Fulkerson algorithm, which has complexity of $O ( | E | | f | )$ O E fand | | is the maximum flow, to find paths in redunfdantly rigid components from each vertex to beacons. In Step 2, the network is decomposed to 2-connected components by depth-first search with complexity of $O ( | \bar { V } | + | E | )$ and organized as component tree with com-O V Eplexity of $O ( | V | )$ . In Step 3, Algorithm 1 has complexity of $O ( | V | )$ O V, since the solutions for all four cases discussed O Vin Section 4 require $O ( n )$ running time, where  is the O n nnumber of non-localizable nodes in current component. In Algorithm 2, applying Observation 3 is the most computationally intensive operation, which requires the examination of the conditions in Theorem 1. The examination is also implemented by using pebble game and Ford-Fulkerson algorithm. Observation 3 is applied whenever a non-localizable node becomes localizable, so in the worst case, the complexity of Algorithm 2 is $O ( | V | ^ { 3 } + | V | | E | | f | )$ . Because $| E | ~ \overset { \cdot } { < } ~ | V | ^ { 2 }$ and  is O V V E f Erestrained to a small constant value $( \mathrm { e . g . , }$ V f the number of beacons), the complexity of Algorithm 2 can be considered as $\mathcal { O } ( | V | ^ { 3 } )$ .

O VNoisy measurement results may influence the results of localization approaches based on graph rigidity theory. To alleviate such influence, some researchers are trying to sift the outliers of ranging results, and only use the reliable ones [32], [33]. We assume that noisy results (the outliers with large errors) are sifted by these approaches, and only used accurate ranging results in LAL design.

# 7 EVALUATION

# 7.1 Experiment

To examine the effectiveness of our solution, we implement LAL on the data trace collected from the ongoing wireless sensor network system GreenOrbs [7]. One mission of GreenOrbs is to realize all-year ecological surveillance in the forest, so it is important to reduce energy consumption. Combining with duty cycling schemes, the transmission power is also well controlled under the highest level to provide just enough connectivity for data collection or other services.

![](images/723ad79f66d905bf14cbb706b48a1aaf3474ecfe70031e7a53434018a85b596c.jpg)



Fig. 10. GreenOrbs system in a campus. The communication range is about 12 meters. After localizability test, a great portion of nodes are recognized as localizable (black), while a few are non-localizable (red). Green ones are beacons.

GreenOrbs consists of two working systems. In this paper, we use the trace collected from the deployed system consists of 100 TelosB motes in the campus of Zhejiang Agricultural and Forestry University, Hangzhou, China. Fig. 10 shows the topology of the system when communication range is about 12 meters. RSSI is used to measure the distance between nodes, so the topology can be used as distance graph if edges between beacons are added. As shown in Fig. 10, a great portion of them are localizable while a few nodes near the border of the deployed area are non-localizable.

TABLE 1 Experiment results on GreenOrbs. 

<table><tr><td></td><td>LAL_B</td><td>LAL_H</td><td>IND</td></tr><tr><td># of edges</td><td>340</td><td>309</td><td>736</td></tr><tr><td># of added edges</td><td>55</td><td>24</td><td>451</td></tr><tr><td># of Power 1 nodes</td><td>61</td><td>73</td><td>0</td></tr><tr><td># of Power 2 nodes</td><td>39</td><td>27</td><td>100</td></tr><tr><td># of Power 3 nodes</td><td>0</td><td>0</td><td>0</td></tr></table>

In the experiment, we compare LAL with the indistinctive approach proposed by Anderson et al. [13], denoted by IND. We use LAL B and LAL H denote LAL Basic and $L A L _ { - }$ Heuristic, respectively. There are 285 edges in the original topology in Fig. 10. Comparisons are conducted from the aspect of the number of edges and nodes with different transmitting power output in the result topology. We denote nodes with original communication range as Power 1 nodes, the ones with doubled and tripled range are denoted as Power 2 and Power 3 nodes, respectively. As shown in Table 1, LAL can significantly reduce the number of edges added to the graph. The three observations in Section 5 can also help to reduce 31 (about 50%) edges added by LAL B. LAL also helps to reduce energy consumption and interference with less increased communication range. IND has to double the communication range of all nodes because the network in Fig. 10 is edge 2-connected but not localizable, while only 39 and 27 nodes need to double their communication range in LAL B and LAL H, respectively. None of the three algorithms need to triple the range of any node in Fig. 10.

# 7.2 Simulation

To further examine the scalability and efficiency of LAL, simulations are conducted under different network instances and varied network parameters. We randomly generate networks of 400 nodes which are uniformly distributed in a unit square [0 1]2. The unit disk model ,with a radius is adopted for communication and distance measurement. For each setting, we integrate results from 100 network instances, with three beacons in each instance. The original communication range is denoted by . For each instance, we change the value of  from R R0.06 to 0.98 stage-by-stage with a step length of 0.002.

As shown in Fig. 11 and Fig. 12, our approach needs to add much less edges to the original distance graph than IND in networks with various densities. We can also find that LAL H needs fewer extra edges than $\mathrm { L A L \_ B }$ does in most cases, which is in accordance with our experiment result. In Fig. 11 and 12, the curves of IND first increase to a peak value, then decrease as the value of  increases and keeps stable for the last Ra few settings. Such a phenomenon can be explained with Fig. 13. When the value of  is small, such as $R = 0 . 0 6$ R, the average size of anchor component is about R .340, which means the network is not 2-connected in most instances. IND needs to triple the communication range of all nodes in these instances. As  increases, Rmost network instances are still not 2-connected, but the average degree is increased, so the number of edges keeps increasing. When  increases to a larger value Rsuch as 0.074, the average size of $G _ { A }$ are over 395, Gwhich implies most instances are 2-connected. Nodes in 2-connected instances only need to double the range, and at the same time more instances become localizable, so the number of edges of IND decreases as the value of increases. When $R \ > \ 0 . 0 8 5$ , most instances has no R R > .non-localizable nodes and no edges need to be added. The curves of LAL B and LAL H follow the same trend. They reach the peak value when $R \ : = \ : 0 . 0 6 4$ , because R . and the number of edges are keep increasing while Rthe number of localizable nodes in $G _ { A }$ keeps almost Gunchanged with a very small value as shown in Fig. 13.

We also study the transmitting power requirements of LAL B, LAL H and IND. Fig. 14 plots the number of nodes at different power levels. As shown in Fig. 14(a) and 14(b), results of LAL H and LAL B have much more Power 1 nodes than IND except when $R < 0 . 0 6 6$ , R < .and much less Power 3 nodes than IND except when $R > 0 . 0 9$ . Curves in Fig. 14(b) have a similar trend as R > .curves in Fig. 12. The numbers of Power 2 nodes of $\mathrm { L A L \_ B }$ and LAL H keep high in only the first three settings, and then it decreases sharply to a very small value. The results in Fig. 14 also explain why LAL can save much extra edges than IND because higher power level tends to induce more edges than a lower one. The curves of LAL H are below those of LAL B in most settings. It suggests that LAL H need to adjust the transmitting power of fewer nodes than that of LAL B, which is in accordance with the results in Fig. 11 and Fig. 12.

![](images/bab589cc8aa24f636ceb9baa2c03e8cb9d9ce4c2524ee53fb162ffb48eb72593.jpg)



Fig. 11. Number of edges in the graph after adding edges.

![](images/594a1aafe18949a3e82dd845c345d845a4de431668fbb05f889a06ca03b99012.jpg)



Fig. 12. Number of added edges.

![](images/7a0ddf74fcd3cb08094b066428518a408d0bfb258f0d6e43450f2000d1dbda42.jpg)



Fig. 13. Number of localizable nodes and nodes in anchor component.

![](images/3f8ddbcea1ea34bb08122dd6711a299aa885cf356dfe02dcfc346ef933d35717.jpg)



(a) Power 1

![](images/c8a036795a43269fc7715510f92138b2d8545252c6f00cbe4e454dbf59e4f65c.jpg)



(b) Power 2

![](images/99f5e3219f46119b8effa0cc47afde3090890c610a8e76ce340839e9f5306880.jpg)



(c) Power 3

Fig. 14. Number of nodes at different power levels.   
![](images/815f3b5c151d4e7d71c2dbeb81dd64969a4f91efe656913175737a462835dc3f.jpg)



(a) LAL Basic

![](images/88c06b906c97bac11e8a62dfe3bf5b44f08ceb3dc8c12fc603ce9124ca117e05.jpg)  
(b) LAL Heuristic

![](images/5d1335d04d28c39e475fda6f65fe38699c7ded75bb52b78295ffeecaad4dda72.jpg)  
(c) Improved IND   
Fig. 15. Testing LAL and IND on network instance consists of 400 nodes with a “T” hole ( =0.08). Grey dots denote RPower 1 nodes, and blue dots denote Power 2 nodes while red dots denote Power 3 nodes.

To better understand how much LAL B and LAL H outperform IND as far as transmitting power is concerned, we further provide an example to show the distribution of nodes at different power levels. Because IND treat the entire network indistinctly and obviously needs more adjustments than LAL, an improved approach (Improved IND) is implemented instead. Improved IND first uses iterative trilateration to localize as many nodes as possible in a graph , and then the rest nodes take Gvertex augmentation to increase their ranging capability. If the graph is 2-edge-connected, these nodes augment their ranging capability by two times. Otherwise the ranging capability should be augmented by three times. These augmented nodes and their two-hop neighbors form connected subgraphs in $G ^ { 3 } ]$ , so they can also be Glocalized through trilateration as discussed in Section 3. As shown in Fig. 15, a network instance with a “T” hole is generated in which 400 nodes are randomly distributed and = 0 08. Both LAL B and LAL H need R .to adjust the power of fewer nodes with lower power levels than improved IND. All augmented nodes in Fig. 15(c) are Power 3 nodes, while there are only three Power 3 nodes in Fig. 15(a) and 15(b). It suggests that LAL B and LAL H are finer-grained than improved IND. We also notice that there are less Power 2 nodes in Fig. 15(b) than that in Fig. 15(a), which is in accordance with the experiment result and simulation results in Fig. 14.

# 8 CONCLUSION

We analyze the limitations of existing studies on localization in non-localizable networks, and propose a localizability-aided approach named LAL. LAL make adjustments according to node localizability results, other than indistinctively consider the network as a whole. By deriving LAL, we can answer the questions on localization in non-localizable networks: which nodes need to augment their ranging capability and which new edges need to be measured. Our designs not only excel previous works theoretically, but also have some good characteristics for practical application. We implement LAL and demonstrate its effectiveness through working system experiment and extensive simulations.

# 9 ACKNOWLEDGEMENT

This work is supported in part by the NSF China under Grants No. 61202487, 60970118, 60903206, 61070216.

# REFERENCES

[1] P. Bahl and V. N. Padmanabhan, “Radar: an in-building rf-based user location and tracking system”, in Proceedings of 19th Annual Joint Conference of the IEEE Computer and Communications Societies, 2000.   
[2] N. B. Priyantha, A. Chakraborty, and H. Balakrishnan, “The cricket location-support system”, in Proceedings of the 6th Annual International Conference on Mobile Computing and Networking, 2000, pp. 32–43.   
[3] D. K. Goldenberg, P. Bihler, M. Cao, J. Fang, B. D. O. Anderson, A. S. Morse, and Y. R. Yang, “Localization in sparse networks using sweeps”, in Proceedings of the 12th Annual International Conference on Mobile Computing and Networking, 2006, pp. 110–121.   
[4] D. Moore, J. Leonard, D. Rus, and S. Teller, “Robust distributed network localization with noisy range measurements”, in Proceedings of the 2nd international conference on Embedded networked sensor systems, 2004, pp. 50–61.   
[5] D.K. Goldenberg, A. Krishnamurthy, W.C. Maness, Y.R. Yang, A. Young, A.S. Morse, and A. Savvides, “Network localization in partially localizable networks”, in Proceedings of 24th Annual Joint Conference of the IEEE Computer and Communications Societies., 2005, pp. 313–326.   
[6] “Oceansense project”, http://www.cse.ust.hk/ liu/Ocean/index.html.   
[7] L. Mo, Y. He, Y. Liu, J. Zhao, S.-J. Tang, X.-Y. Li, and G. Dai, “Canopy closure estimates with greenorbs: sustainable sensing in the forest”, in Proceedings of the 7th ACM Conference on Embedded Networked Sensor Systems, 2009, pp. 99–112.   
[8] T. Eren, D. K. Goldenberg, W. Whiteley, Y. R. Yang, A. S. Morse, B. D. O. Anderson, and P. N. Belhumeur, “Rigidity, computation, and randomization in network localization”, in Proceedings of 23th Annual IEEE Conference on Computer Communications, April 2004.   
[9] Z. Yang and Y. Liu, “Understanding node localizability of wireless ad-hoc networks”, in Proceedings of 29th Annual IEEE Conference on Computer Communications, San Diego, CA, USA, 2010.   
[10] Nissanka B. Priyantha, Hari Balakrishnan, Erik D. Demaine, and Seth Teller, “Mobile-assisted localization in wireless sensor networks”, in Proceedings of 24th Annual Joint Conference of the IEEE Computer and Communications Societies., 2005, pp. 172–183.

[11] K.F. Ssu, C.H. Ou, and H.C. Jiau, “Localization with mobile anchor points in wireless sensor networks”, IEEE Transactions on Vehicular Technology, vol. 54, no. 3, pp. 1187–1197, 2005.   
[12] C. Wu, Y. Zhang, W. Sheng, and S. Kanchi, “Rigidity guided localization for mobile robotic sensor networks”, International Journal of Ad Hoc and Ubiquitous Computing, vol. 6, no. 2, 2010.   
[13] B. D. Anderson, P. N. Belhumeur, T. Eren, D. K. Goldenberg, A. S. Morse, W. Whiteley, and Y. R. Yang, “Graphical properties of easily localizable sensor networks”, Wirel. Netw., vol. 15, no. 2, pp. 177–191, 2009.   
[14] T. Chen, Z. Yang, Y. Liu, D. Guo, and X. Luo, “Localization in non-localizable sensor and ad-hoc networks: A localizabilityaided approach”, in Proceedings of 30th INFOCOM, 2011, pp. 276– 280.   
[15] T. He, C. Huang, B.M. Blum, J.A. Stankovic, and T. Abdelzaher, “Range-free localization schemes for large scale sensor networks”, in Proceedings of the 9th annual international conference on Mobile computing and networking. ACM, 2003, pp. 81–95.   
[16] D. Niculescu and B. Nath, “Dv based positioning in ad hoc networks”, Telecommunication Systems, vol. 22, no. 1, pp. 267–280, 2003.   
[17] A. Savvides, C.-C. Han, and M. B. Strivastava, “Dynamic finegrained localization in ad-hoc networks of sensors”, in Proceedings of the 7th Annual International Conference on Mobile Computing and Networking, 2001, pp. 166–179.   
[18] X. Wang, J. Luo, S. Li, D. Dong, and W. Cheng, “Component based localization in sparse wireless ad hoc and sensor networks”, in Proceedings of the 16th IEEE International Conference on Network Protocols, 2008.   
[19] S. Y. Seidel and T. S. Rappaport, “914 mhz path loss prediction models for indoor wireless communications in multifloored buildings”, IEEE Transactions on Antennas and Propagation, vol. 40, pp. 207–217, 1992.   
[20] K.Whitehouse and D. Culler, “Calibration as parameter estimation in sensor networks”, in Proceedings of the 1st ACM International Workshop on Wireless Sensor Networks and Applications, 2002, pp. 59–67.   
[21] C. Peng, G. Shen, Y. Zhang, Y. Li, and K. Tan, “Beepbeep: a high accuracy acoustic ranging system using cots mobile devices”, in Proceedings of the 5th international conference on Embedded networked sensor systems, 2007, pp. 1–14.   
[22] P.N. Pathirana, N. Bulusu, A.V. Savkin, and S. Jha, “Node localization using mobile robots in delay-tolerant sensor networks”, IEEE Transactions on Mobile Computing, pp. 285–296, 2005.   
[23] M.L. Sichitiu and V. Ramadurai, “Localization of wireless sensor networks with a mobile beacon”, in Proceedings of 2004 IEEE International Conference on Mobile Ad-hoc and Sensor Systems, 2004, pp. 174–183.   
[24] B. Jackson and T. Jordan, “Connected rigidity matroids and ´ unique realizations of graphs”, J. Comb. Theory Ser. B, vol. 94, no. 1, pp. 1–29, 2005.   
[25] D. J. Jacobs and B. Hendrickson, “An algorithm for twodimensional rigidity percolation: the pebble game”, Journal of Computational Physics, vol. 137, pp. 346–365, 1997.   
[26] J. Aspnes, T. Eren, D.K. Goldenberg, A.S. Morse, W. Whiteley, Y.R. Yang, B.D.O. Anderson, and P.N. Belhumeur, “A theory of network localization”, IEEE Transactions on Mobile Computing, pp. 1663–1678, 2006.   
[27] B. Hendrickson, “Conditions for unique graph realizations”, SIAM Journal of Computing, vol. 21, no. 1, pp. 65–84, 1992.   
[28] G. Laman, “On graphs and rigidity of plane skeletal structures”, Journal of Engineering Mathematics, vol. 4, pp. 231–340, 1970.   
[29] J. Hopcroft and R. Tarjan, “Algorithm 447: efficient algorithms for graph manipulation”, Commun. ACM, vol. 16, no. 6, pp. 372–378, 1973.   
[30] O. Gnawali, R. Fonseca, K. Jamieson, D. Moss, and P. Levis, “Collection tree protocol”, in Proceedings of the First ACM Conference on Embedded Networked Sensor Systems, 2009, pp. 1–14.   
[31] T. Pham, I. Lavallee, M. Bui, and S. Do, “A distributed algorithm for the maximum flow problem”, in Proceedings of the 4th International Symposium on Parallel and Distributed Computing, 2005.   
[32] Z. Yang, L. Jian, C. Wu, and Y. Liu, “Beyond triangle inequality: Sifting noisy and outlier distance measurements for localization”, ACM Transactions on Sensor Networks (TOSN), Accepted to appear.   
[33] C. Wu, Z. Yang, T. Chen, and C. Zhang, “Edge verifiability: Characterizing outlier measurements for wireless sensor network localization”, in Proceedings of IEEE MASS, 2011.

![](images/578feaac84211613d32c41a8719b56a97595c57a5119db6032eaf055281cf210.jpg)



Tao Chen received the M.S. degree and the Ph.D. degree in Military Operational Research from the National University of Defense Technology, Changsha, P.R. China, in 2006 and 2011, respectively. He is an Assistant Professor with the College of Information System and Management, National University of Defense Technology, Changsha, P.R. China. His research interests include wireless sensor networks and data center networking. He is a member of the IEEE and the ACM.

![](images/3cc5dbfa3f50e4f2a61464cd6c139907d6a108bd4f3b478b0438f62ef7cdb87e.jpg)



Zheng Yang received a B.E. degree in computer science from Tsinghua University in 2006 and a Ph.D. degree from Hong Kong University of Science and Technology (HKUST) in 2010. He is currently a post-doctoral fellow in Tsinghua University and a research assistant in HKUST. His main research interests include wireless adhoc/sensor networks and pervasive computing. He has published a number of research papers in highly recognized journals and conference, including IEEE/ACM Transactions on Networking,

IEEE Transactions on Parallel and Distributed Systems, IEEE Transactions on Mobile Computing, IEEE INFOCOM, IEEE ICDCS, IEEE RTSS, ACM SenSys, etc. He is a member of the IEEE and the ACM.

![](images/358b1bc3fd837a5050b406c8394c705740c6817d56c91137763dd4d4ca3f3ef6.jpg)



Yunhao Liu received the B.S. degree in automation from Tsinghua University, China, in 1995, the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is a Professor with the TNLIST and School of Software, Tsinghua University, as well as a faculty member with the Department of Computer Science and Engineering at the Hong Kong University of Science and Technology. His research interests include wireless sensor network, peer-to-peer

computing, and pervasive computing. He is a senior member of the IEEE Computer Society and an ACM Distinguished Speaker.

![](images/5a6855cbe77bc95f164b5df683b776d8667eed4a2118a36c66bd5eebc4c128de.jpg)



Deke Guo received the B.S. degree in industry engineering from Beijing University of Aeronautic and Astronautic, Beijing, China, in 2001, and the Ph.D. degree in management science and engineering from National University of Defense Technology, Changsha, China, in 2008. He is an Associate Professor with the College of Information System and Management, National University of Defense Technology, Changsha, China. His research interests include distributed systems, wireless and mobile systems, P2P net-

works, and interconnection networks. He is a member of the ACM and the IEEE.

![](images/cda6c55697926cef6206061870ff8e0edc9c2e99adcb14e46ef2c99b998ba47f.jpg)



Xueshan Luo received the B.E. degree in Information Engineering from Huazhong Institute of Technology, Wuhan, China, in 1985, and the M.S. and Ph.D. degrees in System Engineering from the National University of Defense Technology, Changsha, China, in 1988 and 1992, respectively. Currently, he is a professor at College of Information System and Management, National University of Defense Technology. His research interests are in the general areas of information system and operational research.

His current research focuses on architecture of information system.