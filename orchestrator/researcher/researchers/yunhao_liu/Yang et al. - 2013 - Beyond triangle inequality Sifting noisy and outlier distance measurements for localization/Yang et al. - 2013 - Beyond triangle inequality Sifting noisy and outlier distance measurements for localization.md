# Beyond Triangle Inequality: Sifting Noisy and Outlier Distance Measurements for Localization

ZHENG YANG, Tsinghua University and Hong Kong University of Science and Technology LIRONG JIAN, Hong Kong University of Science and Technology

CHENSHU WU, Tsinghua University

YUNHAO LIU, Tsinghua University and Hong Kong University of Science and Technology

Knowing accurate positions of nodes in wireless ad hoc and sensor networks is essential for a wide range of pervasive and mobile applications. However, errors are inevitable in distance measurements and we observe that a small number of outliers can degrade localization accuracy drastically. To deal with noisy and outlier ranging results, triangle inequality, is often employed in existing approaches. Our study shows that triangle inequality has many limitations, which make it far from accurate and reliable. In this study, we formally define the outlier detection problem for network localization and build a theoretical foundation to identify outliers based on graph embeddability and rigidity theory. Our analysis shows that the redundancy of distance measurements plays an important role. We then design a bilateration generic cycles-based outlier detection algorithm, and examine its effectiveness and efficiency through a network prototype implementation of MicaZ motes as well as extensive simulations. The results show that our design significantly improves the localization accuracy by wisely rejecting outliers.

Categories and Subject Descriptors: C.2.2 [Computer-Communication Networks]: Network Protocols

General Terms: Design, Algorithms, Performance

Additional Key Words and Phrases: Wireless sensor networks, localization, outlier detection

# ACM Reference Format:

Yang, Z., Jian, L., Wu, C., and Liu, Y. 2013 Beyond triangle inequality: Sifting noisy and outlier distance measurements for localization. ACM Trans. Sensor Netw. 9, 2, Article 26 (March 2013), 20 pages.

DOI: http://dx.doi.org/10.1145/2422966.2422983

# 1. INTRODUCTION

Growing convergence among mobile computing devices and embedded technologies is stimulating the development and deployment of a wide range of location-aware applications, including smart space, intrusion detection, inventory management, mobile peer-to-peer computing, wireless sensor networks (WSNs) Surveillance, and so on. A number of localization approaches have been proposed in the literature and used in practice to locate wireless devices.

In recent years, novel schemes have been proposed for in-network localization, in which some special nodes (called beacons or anchors) know their global locations and

A preliminary version of this article appeared in Proceedings of the 29th Annual International Conference on Computer Communications (IEEE-INFOCOM 2010).

This work is supported in part by the NSFC under grant 61171067 and 61170213, China Postdoctoral Science Foundation under grant 2011M500331, NSFC Major Program 61190110, the NSFC Distinguished Young Scholars Program under Grant 61125202, and National High-Tech R&D Program of China (863) under grant No. 2011AA010100.

Authors’ addresses: email: {yang, jian, wu, yunhao}@greenorbs.com.

Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies show this notice on the first page or initial screen of a display along with the full citation. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, to republish, to post on servers, to redistribute to lists, or to use any component of this work in other works requires prior specific permission and/or a fee. Permissions may be requested from Publications Dept., ACM, Inc., 2 Penn Plaza, Suite 701, New York, NY 10121-0701 USA, fax +1 (212) 869-0481, or permissions@acm.org.

-c 2013 ACM 1550-4859/2013/03-ART26 \$15.00

DOI: http://dx.doi.org/10.1145/2422966.2422983

![](images/f6cfcf1fade63f7c64925f567a132289c07c8ece6c7f2d84a82adcab60d066bd.jpg)



(a) Ground truth.

![](images/58789aab410c9ada6c5d3354612a865fcc5be4b183aec52bd5fb9bf48d54815d.jpg)



(b) Estimated location.   
Fig. 1. Multilateration with an outlier measurement, where A, B, C, and D are at corners of a square of  2, and E is at the center of that square.

the rest determine their locations by measuring the Euclidean distances to their neighbors. Several distance ranging methods, such as Radio Signal Strength (RSS) [Seidel and Rappaport 1992] and Time Difference of Arrival (TDoA) [Savvides et al. 2001], are adopted in practical systems. Based on these techniques, the ground truth of a wireless ad hoc network can be modeled as a weighted graph $\dot { G } = \langle \overset { \vartriangle } { V } , E , W \rangle$ , where V is the set of wireless nodes, E is the set of links, and W(u, v) is the distance measurement between a pair of nodes u and v. The problem of localization is to figure out the locations of other nodes based on internode distance measurements and global locations of beacon nodes.

In practice however, noise and outliers are inevitable in distance ranging. The outlier ranging results generally come from the following three sources.

Hardware malfunction or failure. Distance measurements will be meaningless when encountering ranging hardware malfunction. Besides, incorrect hardware calibration and configuration also deteriorate ranging accuracy, which has not been much emphasized in previous studies. For example, RSS suffers from transmitter, receiver, and antenna variability, and the inaccuracy of clock synchronization results in ranging errors for TDoA.

Environmental factors. RSS is sensitive to channel noise, interference, and reflection, all of which have significant impacts on signal amplitude. The irregularity of signal attenuation remarkably increases, especially in complex indoor environments. In addition, for the propagation time-based ranging measurements, the signal propagation speed often exhibits variability as a function of temperature and humidity, so we cannot assume the propagation speed is constant across a large field.

Adversary attacks. As location-based services become more and more prevalent, the localization infrastructure is becoming the target of adversary attacks. By reporting fake location or ranging results, an attacker, for example a compromised (malicious) node, can completely distort the coordinate system. Different from previous cases, the outliers here are intentionally generated by adversaries.

Ignoring their existence is not a suitable way to deal with outliers. Figure 1 shows an example of how outliers destroy localization accuracy. As shown in Figure 1, nodes A, B, C, and D (the black boxes) are beacons at known positions (four vertices of a square of length $\sqrt { 2 } )$ and Node E (the white circle in the center of the square) is to be located. Suppose the accurate distance measurements are $| \mathbf { A B } | = | \mathbf { B C } | = | \mathbf { C D } | = | \mathbf { A D } | = { \sqrt { 2 } }$ and $| \mathbf { A E } | = | \mathbf { B E } | = | \mathbf { C E } | = | \mathbf { D E } | = 1$ . Apparently, the calculated location of E is just the same as its real location when distance measurements are correct. Now suppose an outlier ranging result occurs: the distance between E and B is wrongly measured as $2 \left( | \mathbf { B } \mathbf { E } | = 2 \right)$ . In this case, if all ranging results are indiscriminately used to locate E, the estimated location E’ (the white circle in Figure 1(b) calculated by multilateration [Savvides et al. 2001; Yang and Liu 2010]) is away from the real location E. However, if we layout the outlier ranging, a better estimated location that is the same as the real location of E can be achieved.

To detect outliers, a straight forward solution is to judge graph embeddability based on triangle inequality. A graph-violating triangle inequality cannot be embeddable. However, triangle inequality has in the following two drawbacks.

Coarse granularity. In the case of Figure 1(b), the outlier ranging |BE| cannot be detected by triangle inequality since the triangle $\triangle \tt A B E$ (the distance between A and B is ${ \sqrt { 2 } } ,$ implied by their locations) is still embeddable under the incorrect rangings. Actually in this case all triangles in Figure 1(b), including $\triangle \mathrm { A B E } .$ , ACE, ADE, BCE, BDE and CDE, are embeddable and triangle inequality fails to detect outliers.

Identification. Triangle inequality just indicates the existence of outliers, but cannot identify them. Formally, for a triangle violating the inequality, we are sure that one or more distance measurements are incorrect but have no idea which they are.

Such limitations motivate us to design a novel approach to identify outlier distance measurements beyond triangle inequality. We notice that a rigid graph has discrete and finite realizations. A graph is called rigid if one cannot continuously deform the graph embedded in the plane while preserving distance constraints [Laman 1970]. Thus for a graph G and a pair of neighboring vertices u and $v ,$ if $G - ( u ,$ , v) is rigid, the distance between them $( W ( u , v ) )$ is accordingly discrete and finite under different realizations of $G - ( u , v )$ . Although we artificially exclude and ignore $( u , v )$ , we still have some idea of how to partially figure out $W ( u , \bar { v } )$ . Such redundancy in internode distances is an excellent starting point to detect noise and outliers in distance ranging.

The main contributions of this work are as follows. We formally define the problem of outlier detection for localization and analyze the limitations of existing methods that are based on triangle inequality. Based on graph embeddability and rigidity, we establish the theoretical foundations for detecting outliers. An algorithm based on bilateration and generic cycles is accordingly designed to eliminate outliers during the localization process. To validate this design, a network prototype consisting of 25 MicaZ motes is constructed and extensive simulations are conducted to examine the effectiveness and efficiency of our solution.

The rest of this article is organized as follows. In Section 2, we build the network model and formulate the problem of outlier detection. Section 3 presents the theoretical foundation for identifying outliers and an algorithm based on graph embeddability and rigidity is designed in Section 4. Section 5 analyzes some practical issues of the algorithm. Sections 6 and 7 present the evaluation results from extensive simulations and field experiments. We summarize the related work in Section 8, and conclude the work in Section 9.

# 2. PROBLEM FORMULATION

In this section, we present the network model and formulate outlier detection for localization in wireless ad hoc and sensor networks.

# 2.1. Network Model

We assume that each node is located at a distinct physical location in some region of a plane and associated with a specific set of neighboring nodes. Let N be a network of n nodes labeled $v _ { 1 } , v _ { 2 } , \ldots , v _ { n }$ . Let $\pi ( v _ { i } )$ denote the ground truth position of $v _ { i }$ , and we suppose a small portion of nodes, called beacons, are at known locations.

We generate a weighted grounded graph [Saxe 1979; Eren et al. 2004] $G = \langle V , E , W \rangle$ to represent the geometric constraints of Network N, where each vertex denotes a node in the network and each edge e indicates the neighborhood of its two endpoint nodes.

The distance between two neighboring nodes (or any pair of beacons) is available and defined by $W ( e )$ .

# 2.2. Error Model of Distance Ranging

Given a weighted grounded graph $G = \langle V , E , W \rangle$ , W is determined by the observed information, such as measured internode distances and positions of beacons. We call W measured distance in the rest of this article. Because of the presence of noise, the measurements would be corrupted. Formally, for some edge $e = ( v _ { i } , v _ { j } ) \in E _ { : }$ , W (e) is not necessarily equal to the ground truth distance between nodes $v _ { i }$ and $v _ { j }$ , that is $\| \pi ( v _ { i } ) - \pi ( v _ { j } ) \|$ .

In general, there are two kinds of ranging errors in a localization system: normal error and outlier error. Coming from limitations of hardware and computation precision, normal errors are moderate and predictable, and have attracted a lot of research effort [Moore et al. 2004; Liu et al. 2006]. By contrast, outlier errors are much more severe and unpredictable. They are caused by hardware malfunction or failure, adversary attacks, and so on. We formulate two such kinds of errors as normal edges and outlier edges, respectively, as follows.

Definition 2.1. Given a weighted grounded graph $G = \langle V , E , W \rangle$ , if an edge $e =$ $( v _ { i } , v _ { j } ) \in E$ is a normal edge, then $W ( e ) = \| \pi ( v _ { i } ) - \pi ( \bar { v } _ { j } ) \|$ ; otherwise, e is an outlier edge, and $\dot { W } ( e ) = \lVert \pi ( v _ { i } ) - \pi ( v _ { j } ) \rVert + \epsilon$ , where  is an arbitrary continuous random variable.

In the error model, we assume normal edges contain no ranging noise, which is a good starting point for addressing the outlier detection problem. This assumption and abstraction is also accepted in Addressing Kung et al. [2009], Berger et al. [1996], and Moore et al. [2004]. In Section 5, by introducing an error threshold, the proposed algorithm can handle a more practical error model, where normal edges have moderate ranging errors.

# 2.3. Outlier Detection Problem

Since outlier errors have seriously negative impacts, detecting and eliminating them is essential for highly accurate localization. We formulate the problem of outlier detection as follows.

Problem 2.2 (Outlier Detection). Given a weighted grounded graph $G = \langle V , E , W \rangle$  consisting of normal edges and outlier edges, identify the outlier edges in $G .$ .

Each edge $e \in E$ corresponds to a measured distance or a pair of beacons at known positions. An outlier edge indicates, in the former case, the distance measurement has a large error, while in the latter, the global positions of two corresponding beacons are corrupted.

All normal edges are compatible, for example, satisfying triangle inequality, since they are telling the truth, while it is quite probable that an outlier edge is inconsistent with other normal edges and outlier edges, for example, violating triangle inequality, because it is just a random variable independent of the ground truth. This observation motivates us to detect outlier edges through exposing geometric inconsistency.

# 3. THEORETICAL FOUNDATION

In this section, we analyze the relationship between outlier edges and graph embeddability, and apply rigidity theory to build a theoretical foundation for outlier detection.

# 3.1. Embeddability of Weighted Graphs

In Saxe [1979], the problem of embeddability of weighted graphs is formally defined, and its computational complexity is also discussed.

![](images/c1381636ae71cf3baa4e7614bb4923ad9d28ff1af10e95da294982ce58e4b533.jpg)  
(a) Ground truth

![](images/440fea5594126b5e16bacc3d26a9a875b821310240147da8ed5a8c7f28bc5d41.jpg)  
(b) Realization 1

![](images/29b264012b5ed72ccf5bd99a08dfd8dd68ca76e7f0c188be113d91e6ace8b20a.jpg)  
(c) Realization 2   
Fig. 2. Remaining rigid after removing (u, v).

Definition 3.1. Given a weighted graph, $G = \langle V , E , W \rangle$ , a realization (embedding) of G in the k-dimensional Euclidean space, $\dot { \mathbb R } ^ { k }$ , is a function r, mapping V into $\mathbb { R } ^ { k }$ , such that for each edge $e = ( v _ { i } , v _ { j } ) \in E , W ( \bar { e } ) = \| r ( v _ { i } ) - r ( v _ { j } ) \|$ .

Problem 3.2 (Embeddability). Given a weighted graph, $G = \langle V , E , W \rangle$ , determine whether G is k-embeddable, which means whether there is a realization (embedding) r of G in $\mathbb { R } ^ { k }$ .

Note that, rather than planar embeddability, in this work embeddability means the existence of a realization of a graph in a 2D a plane that satisfies all internode measured distances. Since we focus on networks in a 2D plane, the term embeddable is used instead of 2-embeddable in the following discussion for simplicity. The following theorem reveals a close relationship between outlier existence and graph embeddability.

THEOREM 3.3. Given a weighted grounded graph $G = \langle V , E , W \rangle$ , if G is unembeddable, then E contains at least one outlier edge.

PROOF. Assume that E contains no outlier edge, that is all the edges of G are normal edges. By the definition, for any normal edge $e = ( v _ { i } , v _ { j } ) \in E$ , we have $W ( e ) = \| { \boldsymbol { \pi } } ( v _ { i } ) -$ $\pi ( v _ { j } ) |$ . Let $r ( v _ { k } ) = \pi ( v _ { k } )$ for every vertex $\overset { \mathcal { - } } { v _ { k } } \in V , k = \overset { \mathcal { - } } { 1 } , 2 , \dotsc , n$ , then $W ( e ) = \| r ( v _ { i } ) -$ $r ( v _ { j } ) \|$ . Thus, G is embeddable, contradicting that G is unembeddable.

Theorem 3.3 has overcome the issue of coarse granularity associated with triangle inequality. Recall Figure 1(b), where triangle inequality fails to detect outliers. But Theorem 3.3 succeeds, since the underlying graph is unembeddable. However, similar to triangle inequality, it is also impossible for Theorem 3.3 to tell which edges are outliers or which are not outliers. Generally, under an arbitrary error model, for any given weighted grounded graph, the inverse of Theorem 3.3 doesn’t hold, namely, even if G contains outliers, it can still be embeddable. One extreme example is illustrated as follows. Let $G = \langle V , E , W \rangle$ , and for every edge $e = ( v _ { i } , v _ { j } ) \in E$ , let $\begin{array} { r } { W ( e ) = \frac { 1 } { 2 } \| \pi ( v _ { i } ) - } \end{array}$ $\pi ( v _ { j } ) \|$ . Thus, every edge in E is an outlier, but apparently, G is embeddable. However, compared with an arbitrary error model, we are more interested in whether under the normal edge and outlier edge error model, there is some kind of weighted graph whose being embeddable would imply no outlier.

Suppose the graph G shown in Figure 2(a) is embeddable and we are interested in whether the edge $\boldsymbol { e } = \left( u , v \right)$ is an outlier. After removing e, while preserving the remaining distance constraints, there are only two feasible options for the distance between u and v, corresponding to the two realizations illustrated in Figures 2(b), and 2(c), respectively. Thus, the embeddability of G suggests that $W ( u , v )$ is one of the two options, and what’s more, $e = ( u , v )$ is a normal edge that is telling the truth, as it is with probability of 0 that the measured distance of an outlier edge is in a set consisting of two discrete values. This conclusion makes the quadrilateral structure play an important role in robust localization [Liu et al. 2005; Li et al. 2005] and phantom node filtering [Hwang et al. 2007].

As aforementioned, the inverse of Theorem 3.3 doesn’t hold for all network structures. Suppose the graph G shown in Figure 3(a) is embeddable. After removing edge $\boldsymbol { e } = \left( u , v \right)$ , while preserving the remaining distance constraints, the graph structure can continuously flex, as illustrated in Figures 3(b) and 3(c), which means the distance between u and v can continuously vary in an interval having a non-zero measurement. Similar to Figure 2, the embeddability of G implies that the measured distance of e falls into the feasible interval. However, since that interval has a non-zero measurement, it is with probability greater than 0 that e is an outlier edge and the measured distance of e falls into that interval. Thus, we cannot claim that e is not an outlier even knowing G is embeddable.

![](images/deb464fbb9b7198ccad9ee8fd0716515d80e4ea02f3232b051a062e8cd057d97.jpg)  
(a) Ground truth

![](images/395856b21c209a5d1a399cbe1a8d068594a35ecf9105f12437dc82db505ea8c8.jpg)



(b) Flexing 1

![](images/7655866f62a5f64b3a280b0908b7f789f33fc22cda51ddd13bb91b901c162c42.jpg)



(c) Flexing 2   
Fig. 3. Flexing after removing (u, v).

# 3.2. Redundant Rigidity

Previous studies have shown that the network localizability problem [Eren et al. 2004; Goldenberg et al. 2006] is closely related to graph rigidity. In this article, we will show that the outlier detection problem also has a close relationship with graph rigidity. A graph is generically rigid (or just called rigid) if it has no continuous deformation other than global rotation, translation, and reflection, while preserving distance constraints [Laman 1970]; otherwise, it is flexible. Here the word “generically” means the distances are algebraically independent, that is, no degeneracy. A graph is called generically redundantly rigid (or just called redundantly rigid) if it remains rigid after removing any single edge. Figure 3(a) shows a rigid but not redundantly rigid graph, since after removing $e = ( u , v )$ , this graph becomes flexible, as illustrated in Figures 3(b) and 3(c). It is also easy to check that after removing any edge of the graph shown in Figure 2(a), for example, $e = ( u , v )$ , the graph still has no continuous deformation, while preserving the remaining distance constraints. Thus, it is redundantly rigid.

Before presenting the relationship between the outlier detection problem and graph rigidity, we first give out the definition of outlier disprovable as follows.

Definition 3.4. Given a weighted graph $G = \langle V , E , W \rangle$ , G is outlier disprovable if and only if the embeddability of G implies that it contains no outlier edge.

LEMMA 3.5. Given a redundantly rigid weighted graph G, if it is embeddable, then with probability of 1, G contains no outlier edge.

PROOF. Let $\boldsymbol { e } = \left( u , v \right)$ be an outlier edge in G, and G is embeddable. Because of the redundant rigidity of G, after removing e, it is still rigid, which means there are finite discontinuous realizations up to congruence for $\tilde { G } = \overline { { G } } - \{ e \}$ . In each realization of ${ \tilde { G } } ,$ the distance between node u and node v is fixed. So, there are finite discrete values, denoted by set S, for the distance between u and v. As G is embeddable and $e \in E _ { \mathrm { : } }$ , the measured distance of e is in S. However, as an outlier edge, the measured distance of e is a continuous random variable, which means that with probability of $0 , W ( e ) \in S .$ , since S has measure zero. So, with probability of 1, there is no outlier edge in G.

![](images/6a0aba255a0de0a7a6741351469b89272aeecc1c20599e84d91dcdc14998553e.jpg)  
(a)

![](images/526fa781660681d1702dc073a7fc13ce5841c57b068388dbf4752943d875ddac.jpg)  
(b)

![](images/852d3d898245880e81c2e1eacec644f40d1125d9edab451d2cfc3d64db34b94f.jpg)  
(c)

![](images/3a4e4f6c4c689d75ffd6a884fc1108bbb19144855339bb0c04a2139a90a4f9c7.jpg)  
Fig. 4. Redundantly rigid components in a graph with outlier edge (u, v).

To analyze the necessary condition for outlier disprovability, we present a proposition first proved by Hendrickson [1992].

PROPOSITION 3.6. If a graph G is flexible, then for almost all realizations r of G, the flexing space of r contains a submanifold that is diffeomorphic to the circle.

LEMMA 3.7. Given a weighted graph G, if G is outlier disprovable, then G is redundantly rigid.

PROOF. Assume the only interesting case is that G is rigid but not redundantly rigid. Thus, some edge $\boldsymbol { e } ~ = ~ ( u , v )$ exists, whose removal produces a flexible graph G˜ . By Proposition 3.6, for almost all realizations r of ${ \tilde { G } } ,$ , the flexing space of r contains a submanifold diffeomorphic to the circle. The distance between nodes u and v will be a multivalued function for almost every point on this circle. Hence, the set of distances between u and v corresponding to r, denoted by $S _ { d ( u , v ) } ( r )$ , has nonzero measure. So, even e is an outlier, with probability greater than $0 , W ( e ) \in S _ { d ( u , v ) } ( r )$ , resulting in G is embeddable. Therefore, G is not outlier disprovable.

Combining Lemma 3.5 and Lemma 3.7, we obtain the following theorem.

THEOREM 3.8. Given a weighted graph G, G is outlier disprovable if and only if G is redundantly rigid.

By Theorem 3.3 and Theorem 3.8, we present a framework for outlier detection, which is outlined by Algorithm 1. We explain the framework through an example shown in Figure 4, where solid lines denote normal edges and the outlier is denoted by the dashed line. Figure 4(a) is the ground truth, call it G. Besides Figure 4(a), there are three other redundantly rigid components, shown in Figures 4(b), 4(c), and 4(d), respectively. Intuitively, Figures 4(a), 4(b), and 4(c) are unembeddable, since they all contain $\boldsymbol { e } = \left( u , v \right)$ , the outlier edge. Following our algorithm, all the edges of G are marked outlier edges before checking the embeddability of Figure 4(d). As Figure 4(d) does not contain the outlier edge, it is embeddable. All the edges in Figure 4(d) are marked normal edges. Finally, we mark all the edges of G except $\boldsymbol { e } = \left( u , v \right)$ as normal edges, leaving e marked as an outlier edge.

Algorithm 1 addresses the outlier detection problem from the perspective of components: if a redundantly rigid component is embeddable, then all its edges are normal edges. Now, let us look at the problem from another perspective: a single edge, call it e. Intuitively, by Theorem 3.8, through checking all redundantly rigid components containing e, if one is embeddable, then we know that e is a normal edge. The question is whether it is really necessary to check all the redundantly rigid components containing e, especially when e is actually an outlier edge.

Figure 5 illustrates an example for which we want to verify edge $e = ( u , v )$ . There are two redundantly rigid components containing e: the whole graph G and the component H highlighted by the dashed circle. If H is embeddable, then e is definitely marked as a normal edge; otherwise, G is also unembeddable as it contains H, and finally e is marked as an outlier. Thus, whether we can verify e, is only determined by the embeddability of H, and has nothing to do with G. Actually, for any edge in $G ,$ checking the embeddability of G is meaningless. This example suggests that for a single edge $e ,$ there are some minimally redundantly rigid components containing e such that the identity of e is only determined by the embeddabilities of these components.

![](images/30e83ee4a97de9921db4d1a956524ce5b8305a4074e73995d3def2f4e3fe5d21.jpg)



Fig. 5. One edge contained in more than one redundantly rigid component.

![](images/b80bde48e728ab441ca80f05e8e12d080518e6291debbccb0ff9a89529ed4977.jpg)



(a)

![](images/f7a38250622a804fe491f910a6752b22b138339e68bfa06c8e92bdf28b045c1b.jpg)



(b)

![](images/33b7bf91b22328e45c330c2c6c0c4cd2d67105cee998ae3561b8bda38f25c113.jpg)  
(c)

Fig. 6. Examples of generic cycles.   
ALGORITHM 1: Component-based Outlier Detection.   
1: for all redundantly rigid component H in G do
2:    if H is embeddable then
3:    mark every edge $e \in H$ a normal edge.
4:    else
5:    for all edge $e \in H$ not marked a normal edge do
6:    mark e an outlier edge.
7:    end for
8:    end if
9: end for

# 3.3. Generic Cycle

Definition 3.9 ([Jackson and Jord ´an 2005; Berg and Jordan 2002]). A graph $G \ =$ $\langle V , E \rangle$ with $| V | \geq 4$ is called a generic cycle if $| E | = 2 | V | - 2$ and G satisfies

$$
i (X) \leq 2 | X | - 3 \text {   for   all   } X \subset V \text {   with   } 2 \leq | X | \leq | V | - 1, \tag {1}
$$

where i(X) denotes the number of edges induced by X in G.

Three instances of generic cycle are illustrated in Figures 6(a), 6(b), and 6(c). By the Laman condition [Laman 1970] and the definition of redundant rigidity, a generic cycle is minimally redundantly rigid. Here the word “minimally” means containing no redundantly rigid proper subgraph.

![](images/ce2bd8cbd76a58e98dc153c724b5d97372260e2cf227176f86d593056d9cea9d.jpg)



Fig. 7. A chain of n redundantly rigid components.

The following lemma shows the relationship between generic cycles and redundantly rigid graphs.

LEMMA 3.10 ([JACKSON AND JORDAN´ 2005]). A graph G is redundantly rigid if and only if G is rigid and each edge of G belongs to a generic cycle in G.

THEOREM 3.11. Let $G _ { 1 } = \langle V _ { 1 } , E _ { 1 } \rangle$ and $G _ { 2 } = \langle V _ { 2 } , E _ { 2 } \rangle$ be two redundantly rigid graphs with $| V _ { 1 } \cap V _ { 2 } | \geq 2$ . Then $G _ { 1 } \cup G _ { 2 }$ is redundantly rigid.

PROOF. By the Laman condition [Laman 1970] and the rigidity of $G _ { 1 }$ and $G _ { 2 }$ , let $H _ { 1 }$ and $H _ { 2 }$ be a minimally rigid spanning subgraph of $G _ { 1 }$ and $G _ { 2 }$ , respectively. Since $| V _ { 1 } \cap V _ { 2 } | \geq 2$ , then $H _ { 1 } \cup { \dot { H } } _ { 2 }$ is rigid [Jackson and Jordan 2005]. Furthermore, ´ $H _ { 1 } \cup H _ { 2 }$ is a spanning subgraph of $G _ { 1 } \cup \bar { G } _ { 2 }$ . Thus, $G _ { 1 } \cup G _ { 2 }$ is rigid. For any e in $G _ { 1 } \cup G _ { 2 }$ , without loss of generality, let $e \in E _ { 1 }$ , according to Lemma 3.10, there is a generic cycle $\tilde { H }$ in $G _ { 1 }$ containing e. Apparently, H˜ is in $G _ { 1 } \cup G _ { 2 }$ . Therefore, $G _ { 1 } \cup G _ { 2 }$ is redundantly rigid, by Lemma 3.10.

By Theorem 3.11, Algorithm 1 suffers from a problem of computational prohibitiveness, termed as combinatorial explosion. Figure 7 shows an example of the inefficiency of Algorithm 1, where n basic redundantly rigid components, that is, RR1, RR2, $\mathrm { R R } _ { n - 1 }$ , and $\mathrm { R R } _ { n } ,$ compose a chain, and every pair of neighboring basic redundantly rigid components have more than one common vertex. According to Theorem 3.11, there are $n + ( n - 1 ) + \ldots + 1 = { \textstyle { \frac { 1 } { 7 } } } n ( n - 1 )$ redundantly rigid subgraphs by the combination of those n basic redundantly rigid components, all embeddabilities of which are checked by Algorithm 1. This is significantly inefficient, because as long as the embeddabilities of those n basic redundantly rigid subgraphs have been examined, others’ embeddabilities can be implied and totally meaningless for outlier detection.

Based on Lemma 3.10, from the perspective of a single edge, we propose another framework for outlier detection as Algorithm 2, recall Figure 5. For every edge $e \in G ,$ through employing Algorithm 2, only the embeddability of the complete graph $K _ { 4 }$ containing e, which is the smallest generic cycle, needs to be checked. And the embeddability of G would never be considered. By the redundant rigidity of generic cycles and Lemma 3.10, we obtain the following theorem, which shows that Algorithm 1 and Algorithm 2 are equivalent.

THEOREM 3.12. Given a weighted graph $G = \langle V , E , W \rangle$ , for any edge $e \in E ,$ e is marked a normal edge by Algorithm 1 if and only if e is also marked a normal edge by Algorithm 2.

PROOF. Sufficiency. e is marked a normal edge by Algorithm 2 if and only if there is an embeddable generic cycle H containing e. Because of the redundant rigidity of a generic cycle, the embeddability of H is also checked in Algorithm 1 and e is marked a normal edge.

Necessity. e is marked a normal edge by Algorithm 1 if and only if there is a embeddable redundantly rigid component H containing e. By Lemma 3.10, there is a generic cycle $\tilde { H }$ of H containing e. As H is embeddable, $\tilde { H }$ is also embeddable. Therefore, e is also marked a normal edge by Algorithm 2.

ALGORITHM 2: Edge-based Outlier Detection.   
1: for all e not marked in G do
2:    if there is a generic cycle H containing e is embeddable then
3:    mark any edge $\in H$ , including e, a normal edge.
4:    else
5:    mark e an outlier edge.
6:    end if
7: end for

In Algorithm 2, each edge only cares about how to verify itself. Accordingly, in a wireless ad hoc network, the task of a node is to verify its incident edges. Thus, Algorithm 2 is actually a framework for distributed outlier detection. Since distributed methods are more appealing to large scale wireless ad hoc network applications than centralized methods, that is Algorithm 1, in the rest of this article, we focus on the implementation of Algorithm 2.

# 4. ALGORITHM DESIGN AND IMPLEMENTATION

Two key challenges exist in the implementation of Algorithm 2: how to find those generic cycles containing edge e and check their embeddabilities. Saxe [1979] proved that deciding embeddability of a given weighted graph with exact Euclidean norm edge lengths is strongly NP-hard in k dimensions, for any $k \geq 1$ . In particular, even with the Unit Disk Graph (UDG) model, this problem is still weakly NP-hard [Bdoiu et al. 2004]. A basic approach to decide embeddability is to find a realization, namely, localization. Apparently, localization is not easier than deciding embeddability. However, some classes of graphs are computationally efficient to localize quadrilateration [Moore et al. 2004], trilateration [Eren et al. 2004], and bilateration [Goldenberg et al. 2006] graphs. Compared to quadrilateration and trilateration, bilateration has the following advantages.

—No trilateration graphs are generic cycles except $K _ { 4 }$ , but many of them are bilateration graphs.   
—Trilateration requires the network to be dense, while bilateration can be carried out in sparse networks, as suggested in Goldenberg et al. [2006].   
—Trilateration is an LS-based statistics method, which would hide outliers [Hampel et al. 2005]; by contrast, bilateration would effectively expose geometric inconsistency.

Based on this analysis, our target now becomes bilateration generic cycles. We define the problem as follows.

Problem 4.1 (Bilateration Generic Cycles Search). Given a bilateration ordering l of a graph G, find out those subgraphs H of G such that H is a generic cycle with a bilateration ordering ˜l that is a subsequence of l.

Before presenting our algorithm to find bilateration generic cycles, we first prove their properties.

LEMMA 4.2. A bilateration graph $G = \langle V , E \rangle$ is a generic cycle if and only if there is a bilateration ordering $l = \langle v _ { 1 } , v _ { 2 } , v _ { 3 } , . . . , v _ { n } \rangle$ of V , such that for all $1 \leq i \leq n ,$ the degree of vi $d ( v _ { i } ) \geq 3$ , and for all $3 \leq i \leq ( n - 1 ) ,$ , vi is adjacent to exactly two distinct vertices v j , with $j < i ,$ , and $v _ { n }$ is adjacent to exactly three distinct vertices $v _ { j }$ with, $j < n .$ .

ALGORITHM 3: Bilateration Generic Cycles Search   
BGCS(List order)
1: for all vertex x with more than 2 neighbors earlier in order do
2: List ancestors = (neighbors of x earlier in order)
3: for all all triple (u,v,w) in ancestors do
4: SortedList visited = new SortedList
5: visited.add(u,v,w)
6: Graph cycle = new Graph
7: cycle.add(u,(u,x),v,(v,x),w,(w,x))
8: Traceback(cycle, visited, order)
9: end for
10: end for

Traceback(Graph cycle, SortedList visited, List order)
1: Node x = visited.pop()
2: List ancestors = (neighbors of x earlier in order)
3: if visited.length()==1 and x and visited[0] are neighbors then
4: cycle.add((x,visited[0]))
5: output cycle as a generic cycle
6: ancestors.remove(visited[0])
7: end if
8: for all pair(u,v) in ancestors do
9: visited.add(u,v)
10: cycle.add(u,(u,x),v,(v,x))
11: Traceback(cycle,visited,order)
12: end for

PROOF. Sufficiency. The number of edges of G is $2 ( n - 3 ) + 3 + 1 = 2 n - 2 .$ . Assume there are some subsets S of V such that $\check { | } S | \geq 4$ and $i _ { G } ( S ) \geq 2 | S | - 2$ . Let X denote one such S with minimal cardinality, and $k = | X |$ . Let $X = \langle v _ { i _ { 1 } } , v _ { i _ { 2 } } , \dots , v _ { i _ { k } } \rangle$ , where $1 \leq i _ { 1 } <$ < $i _ { 2 } < \cdots < i _ { k } \le n ,$ . The only interesting case is where $k < n .$ . Let $p$ denote the maximal i such that $v _ { i } \not \in X .$ If $p = n ,$ , according to the property of l, the degree of $v _ { i _ { k } }$ in the subgraph induced by X in G, $\dot { d } _ { G ( X ) } ( v _ { i _ { k } } ) \leq 2$ . Since $i _ { G } ( X ) \overset { \cdot } { \geq } 2 | \dot { X } | - 2 , i _ { G } ( \dot { X ^ { - } } \{ v _ { i _ { k } } \} ) \overset { \cdot } { \geq } 2 | X - \{ v _ { i _ { k } } \} | \overset { - } { - } 2 ,$ , which contradicts the minimal cardinality of X. Thus, $i _ { k } = n .$ . We rewrite X in another way, $X = \langle v _ { i _ { 1 } } , v _ { i _ { 2 } } , \ldots , v _ { i _ { k - ( n - p ) } } , v _ { p + 1 } , v _ { p + 2 } , \ldots , v _ { n } \rangle$ . We show that $X ^ { \prime } = \langle v _ { i _ { 1 } } , v _ { i _ { 2 } } , \dotsc , v _ { i _ { k - ( n - p ) } } \rangle$ is satisfying $i _ { G } ( X ) \geq 2 | X | - \mathrm { \hat { 2 } }$ , which also contradicts the minimal cardinality of X. Since $d ( v _ { p } ) \geq 3$ in G, and $v _ { p }$ is adjacent to at almost two distinct vertices $v _ { j }$ with $j < p$ (since $p \neq n ) .$ , there must be some $j > p$ and $v _ { j }$ is adjacent to $v _ { p } .$ Thus, through removing $v _ { p + 1 } , v _ { p + 2 } , \ldots , v _ { n }$ from X to get X
 , we have $\mathop { i _ { G } ( X ) } - \mathop { i _ { G } ( X ^ { \prime } ) } \leq 2 \mathop { ( n - p - 1 ) } + 3 - 1 = 2 ( n - p )$ . Since $\dot { \iota } _ { G } ( X ) \geq 2 | X | - 2 , i _ { G } ( \bar { X } ) \geq i _ { G } ( X ) - 2 ( n - p ) \geq 2 | X | - 2 - 2 ( \bar { n } - p ) = 2 | X | - 2 \delta = 1$ .

Necessity. Let G be a generic cycle with a bilateration ordering $l = \langle v _ { 1 } , v _ { 2 } , v _ { 3 } , \ldots , v _ { n } \rangle$ . Thus, for all $1 \leq i \leq n , d ( v _ { i } ) \geq 3$ , and for all $3 \le i \le n , v _ { i }$ is adjacent to at least two distinct vertices $v _ { j }$ with $j < i$ . Besides, there must be some $v _ { i }$ adjacent to at least three distinct vertices $v _ { j }$ with $j < i$ . Let k denote the minimal of such i. Apparently, $k \geq 4 .$ . Let $X = \langle v _ { 1 } , v _ { 2 } , v _ { 3 } , . . . , v _ { k } \rangle$ . Assume the only interesting case is that $v _ { k }$ is adjacent to exactly three distinct vertices $v _ { j } ,$ with $j < k$ and for all $1 \leq i \leq k , d _ { G ( X ) } ( v _ { i } ) \geq 3$ . By the first part of this proof, the subgraph G(X) induced by X in G is a generic cycle. So, $G ( X ) = \bar { G }$ and $X = V$ .

Based on Lemma 4.2, an algorithm for bilateration generic cycles search is given in Algorithm 3. Before proving the correctness of Algorithm 3, we give an example to illustrate it, shown in Figure 8, where Figure 8(a) shows the bilateration ordering $l ~ = ~ \langle v _ { 1 } , v _ { 2 } , v _ { 3 } , v _ { 4 } , v _ { 5 } , v _ { 6 } \rangle$ . Because $v _ { 4 }$ has 3 neighbors, $v _ { 1 } , \ v _ { 2 } .$ , and $v _ { 3 }$ , earlier in $l , \textbf { a }$ bilateration generic cycles search procedure begins. At the first beginning, cycle $= ( v _ { 1 } , v _ { 2 } , v _ { 3 } , v _ { 4 } , ( v _ { 1 } , v _ { 4 } ) , ( v _ { 2 } , v _ { 4 } ) , ( v _ { 3 } , v _ { 4 } ) )$ , and visited ${ \bf \underline { { \theta } } } = ( v _ { 3 } , v _ { 2 } , v _ { 1 } )$ . Through checking v3, we add $( v _ { 1 } , v _ { 3 } )$ and $( v _ { 2 } , v _ { 3 } )$ into the cycle, and update visited as $( v _ { 2 } , v _ { 1 } )$ . Since v1 and v2 are neighbors, after adding $( v _ { 1 } , v _ { 2 } )$ into the cycle, we get a generic cycle, illustrated in Figure 8(b). Since there is no other neighbor of $v _ { 2 }$ earlier in $l ,$ this search terminates. Another bilateration generic cycles search begins at $v _ { 6 }$ . Initially, cycle $= ( v _ { 3 } , v _ { 4 } , v _ { 5 } , v _ { 6 } , ( v _ { 3 } , v _ { 6 } ) , ( v _ { 4 } , v _ { 6 } ) , ( v _ { 5 } , v _ { 6 } ) )$ and visited $\mathbf { \nu } = ( v _ { 5 } , v _ { 4 } , v _ { 3 } )$ . After tracing back to $v _ { 5 } , ( v _ { 3 } , v _ { 5 } )$ and $( v _ { 4 } , v _ { 5 } )$ are inserted into the cycle, and visited = (v4, v3). Again, since v3 and $v _ { 4 }$ are neighbors, after inserting $( v _ { 3 } , v _ { 4 } )$ into the cycle, we get the second generic cycle, shown in Figure 8(c). Besides v3, v4 still has the other two neighbors earlier in l, $v _ { 1 }$ and v2. After removing $( v _ { 3 } , v _ { 4 } )$ from the cycle, the search procedure continues. And finally, this search procedure ends with the third generic cycle, shown in Figure 8(d). These three generic cycles are all the bilateration generic cycles in $G$ with respect to $l = \langle v _ { 1 } , v _ { 2 } , v _ { 3 } , v _ { 4 } , v _ { 5 } , v _ { 6 } \rangle$ .

![](images/855b99c8bbc8942d9aaa63717213a5cd6a9a0200bfe6747f389ed063793f794c.jpg)



(a) Bilateration ordering

![](images/59d2108e31ef2ab0d7b59a79a4b51522429b0b4e52ebcd54a73d9325da720668.jpg)



(b) First bilateration generic cycle

![](images/61a7c434cfb094f54d4008bfa72e86bf315173ed68c87ac4547d2cba382b8225.jpg)



(c) Second bilateration generic cycle

![](images/de592b5b89ba401c1192e0b740d12d312488d9cf1d894a41683079834cd04cab.jpg)



(d) Third bilateration generic cycle   
Fig. 8. Bilateration generic cycles search.

THEOREM 4.3. Given a graph G with a bilateration ordering l, Algorithm 3 identifies all bilateration generic cycles in G with respect to l.

PROOF. Correctness. Let $C = \langle V , E \rangle$ denote a cycle identified by Algorithm 3. Apparently, $m = | V | \geq 4$ . Reversing the tracing back order in Algorithm 3, we get an ordering of vertices of $C , l ^ { \prime } = \langle v _ { i _ { 1 } } , v _ { i _ { 2 } } , \dots , v _ { i _ { m } } \rangle$ , where $1 \leq i _ { 1 } < i _ { 2 } < \cdot \cdot \cdot < i _ { m } \leq n$ such that $v _ { i _ { 1 } }$ and $v _ { i _ { 2 } }$ are neighbors and for all $3 \leq k \leq ( m - 1 ) , v _ { i _ { k } }$ has exactly two neighbors earlier in $l ^ { \prime } ,$ , and $v _ { i _ { m } }$ has exactly three neighbors earlier in $l ^ { \prime } .$ . In particular, for all $1 \leq k \leq ( m - 1 )$ , there must be some j with $\bar { k } \overset { = } \mathcal { j } \leq m$ and $v _ { i _ { j } }$ and $v _ { i _ { k } }$ are neighbors; otherwise, $v _ { i _ { k } }$ would never be inserted into C. Thus, for all $3 \leq \dot { k } \leq m , d _ { C } ( v _ { i _ { k } } ) \geq 3$ . Similarly, we can prove both $d _ { C } ( v _ { i _ { 1 } } )$ and $d _ { C } ( v _ { i _ { 2 } } ) \geq 3$ . By Lemma 4.2, C is a bilateration generic cycle.

Optimality. By Lemma 4.2, every bilateration generic cycle C in G with respect to l has a bilateraion ordering $l ^ { \prime } = \langle v _ { i _ { 1 } } , v _ { i _ { 2 } } , \ldots , v _ { i _ { m } } \rangle$ , which is a subsequence of l, such that $m \geq 4$ , and for all $1 \leq k \leq m , d _ { C } ( \bar { v } _ { i _ { k } } ) \geq 3 ;$ and for all $3 \le k \le ( \bar { m } - 1 ) , v _ { \bar { i } _ { k } }$ has exactly two neighbors earlier in $l ^ { \prime } { } .$ and $v _ { i _ { m } }$ has exactly 3 neighbors earlier in l 
 . From following Algorithm 3 and the first part of this proof, we can see that Algorithm 3 outputs all such bilateration orderings.

Algorithm 3 solves the first issue, how to find generic cycles, in Algorithm 2. Through employing Sweeps [Goldenberg et al. 2006], we can check the embeddabilities of generic cycles based on localization, which addresses the second issue.

# 5. DISCUSSION

In this section, we discuss some practical issues of the proposed algorithm and solutions to address them.

# 5.1. Distributed Implementation

Since Algorithm 2 is a framework for outlier detection from the point of view of a single edge, it is not difficult to implement it in a distributed fashion. From every single edge, after exploring a bilateration ordering l, Algorithm 3 can identify all bilateration generic cycles with respect to l. In the exploring procedure, l uses the start edge as its ID, and every involved node remembers its order in l. Once a node finds that it has more than 2 neighbors earlier in l, a bilateration generic cycles search procedure is initiated. After identifying a bilateration generic cycle, a distributed solution, Sweeps [Goldenberg et al. 2006], can be implemented to test the embeddability of the generic cycle.

# 5.2. Practical Error Model

We assume normal edges are without any ranging errors. This abstraction is impractical in real world networks, where ranging errors always exist. Our basic algorithm fails in this situation, since it is almost impossible for those generic cycles identified by Algorithm 3 to be embeddable. We introduce an error threshold δ to handle this problem. Given a bilateration generic cycle $C = \langle V , E , W \rangle$ , Sweeps computes all realizations r of C. Define additive distortion [Bdoiu et al. 2004] as

$$
\epsilon = \min _ {r} \left\{\max _ {(u, v)} \{| W ((u, v)) - \| r (u) - r (v) \| | \} \right\} \tag {2}
$$

for every $( u , v ) \in E . \operatorname { I f } \epsilon \leq \delta$ , then we say C is embeddable; otherwise, it is unembeddable. The value of δ has direct impact on the performance of the proposed algorithm, and should be determined according to the ranging accuracy. The introduction of δ, however, raises another issue: a generic cycle with outlier edges may be claimed embeddable; namely, there are false negative results. However, under such a model (normal edges containing mild errors), normal edges no longer mean that the measuring value is exactly equal to a real value. Instead, an edge with bounded error is treated as a normal edge. It is true that our solution will accept some measurements with mild errors, but they are actually defined to be normal when it is assumed that errors exist in normal edges. Hence, our solution is able to identify outlier measurements under this model, but cannot tell whether a normal edge is accurate or slightly erroneous (no probabilistically true conclusion on this point).

If false negative results are unacceptable in some scenarios, such as security applications, besides choosing a tighter δ, we can require that a normal edge be contained in more than one embeddable generic cycle.

Another issue induced by ranging errors is that the performance will decay rapidly by error accumulation. It is possible that the aggregation of mild errors conceals a gross error. Results from Bdoiu et al. [2004] show that even for a complete graph it is not an easy problem, let alone sparse graphs, that is, a generic cycle. One way to address this issue is to limit the size of a generic cycle. Of course, the most effective way to solve this problem is improving the ranging accuracy.

# 5.3. Computation Complexity

In the generic cycles search procedure, by Theorem 4.3, Algorithm 3 is an outputsensitive method, whose computation complexity is determined by the number of generic cycles and their sizes, that is, the size of the output. Due to the minimal redundant rigidity of generic cycles, from the perspective of verifying normal edges, it is necessary to check the embeddability of every generic cycle in the worst case. Thus, Algorithm 3 is optimal.

After identifying a generic cycle, Sweeps [Goldenberg et al. 2006] is employed to test the embeddability of that generic cycle. Although in the worst case, the requirement of computational time and space increases exponentially with the sizes of generic cycles, the results from Goldenberg et al. [2006] and our experiments show that Sweeps is effective in practice. What’s more, even if we limit the maximal size of a generic cycle, that is, to 16 nodes, most normal edges can still be verified. Of course, it is a tradeoff between theoretical guarantees and computational complexity, which should be determined by practical application requirements and resource constraints of wireless devices.

# 6. EVALUATION

# 6.1. Normal Edges with Precise Distance Measurements

We first evaluate the performance of the proposed algorithm when normal edges have precise distance measurements. We generate random networks of 400 nodes in a square region [0, 1]2. We do not consider outlier edges, as here we are only interested in how many normal edges can be verified, which is only determined by the topological structure of the network consisting of normal edges. We aggregate the results from 100 network instances at each sensing radius and compute 95th-percentile confidence intervals for the quantity of interest.

Figure 9 plots the performance of the proposed algorithm, which is based on Bilateration Generic Cycles, and a Quadrilateral-based speculative filtering algorithm [Hwang et al. 2007], the state of the art outlier detection algorithm, in which all edges in a quadrilateral would be verified. By Theorem 3.8, through identifying all the redundantly rigid components using the Pebble Game algorithm [Jacobs and Hendrickson 1997], we can figure out all the edges that are theoretically possible to verify. We find that the quadrilateral-based speculative filtering algorithm always verifies fewer edges than the proposed method, because a quadrilateral is the smallest bilateration generic cycle. Specifically, the proposed algorithm verifies at least 80% of theoretically verifiable edges when the network density varies widely. For comparison, the quadrilateral-based algorithm guarantees verification of only 50% of edges. We limit the size of the largest bilateration generic cycle (at most 16 nodes) to ensure the needed computational space and time doesn’t exceed the capacity of off-the-shelf sensor nodes, such as Telos or Mica motes; otherwise, the performance gap would be even larger. The result suggests that in scenarios where networks are sparse or networks are dense but with a large fraction of outlier edges, the proposed algorithm outperforms the quadrilateral-based algorithm.

![](images/7c1c2c3b7f8694f9d3a01d5454b0b2b5531fa8aa656cf5109198117ad8b3b58b.jpg)



Fig. 9. Ratios of the number of normal edges verified to the number of normal edges that are theoretically possible to verify.

# 6.2. Normal Edges with Moderate Ranging Errors

To examine the effectiveness of the practical error model, where normal edges have moderate ranging errors, we implement the proposed outlier detection on the data trace collected from the ongoing ecological surveillance system GreenOrbs [Mo et al. 2009], as illustrated in Figure 13. In this system, commercial off-the-shelf sensor motes are programmed, enclosed, and deployed in the forest. With each node equipped with multiple sensors, such as light, temperature, and humidity, GreenOrbs supports various ecological applications. Localization is one of the most important issues in the project since sensing data without location information is almost meaningless.

Based on the data collected on June 15, 2009, we extract the network topology, shown in Figure 14. Besides light, temperature, and humidity information, each packet also contains the first 10 discovered neighbors of one node in the latest measurement interval. To decrease the uncertainty caused by dynamic environmental factors, for each pair of neighboring nodes (u, v) depicted in Figure 14, we require that there are at least three packets of u containing v as their neighbor, and vice versa. Nevertheless, the resulting topology still greatly differs from the UDG model, because of the complicated forest environment. Based on this network topology, we conduct extensive simulations to investigate how outlier detection can improve localization accuracy. The ranging errors of outlier edges are 10 times that of normal edges. We integrate the results from 100 instances.

The proposed outlier detection algorithm doesn’t serve as a localization algorithm, but an intermediate component between measuring internode distances and localizing wireless devices based on such ranging information. We utilize AHLoS [Savvides et al. 2001] as the basic localization method, and compare the localization performance of three strategies towards outliers: sifting, ignoring (the basic AHLoS approach), and eliminating completely (the idealized case). Note that our outlier detection algorithm works well with arbitrary localization methods. We choose AHLoS since it delegates a major class of widely used multilateration (trilateration)-based localization techniques.

Figure 10 reports the result for σ = 5% outlier edges. For all strategies, the average location error increases linearly with increasing ranging error. In the idealized case, labeled as Without Outlier, the location errors are much less than the ignoring case labeled as No Sifting, while employing Algorithm 2 to sift outliers achieves a median location accuracy, which is close to the idealized case and also much better than the basic AHLoS approach. In particular, when the distance ranging error is 0.25 m, the proposed algorithm improves the localization accuracy from 19 m to 14 m, which is close to 12 m, the result of the idealized case.

![](images/f6dce71a8407231a0821b37cd78bfd8fc361eba85c36b7f193e22c09a4bb41fb.jpg)



Fig. 10. The impact of ranging error on accuracy.

![](images/e7df217ebcbee40317d2331c998b3a0fbae0d0f14db48e017f5bf38e4b65b1ac.jpg)



Fig. 11. Localization errors of sensor nodes.

![](images/5e157a3d5a0cd24f148bf8f9403b9a9075d47811d9c8d8d0f37afbc268c515c2.jpg)



Fig. 12. Empirical cumulative function of location errors.

We also study the typical localization errors for every single node, illustrated in Figure 11. For all 19 nodes, the location accuracy has been improved by sifting outliers. Figure 12 plots the characteristics of error propagation. As shown, nearly 90% of nodes have at most 15 m error and 80% have at most 10 m error by sifting outliers, while for the basic AHLoS algorithm, only 80% of nodes have less than 15 m error and 65% of nodes have less than 10 m error.

# 7. FIELD EXPERIMENT AND RESULTS

We conduct a localization experiment using MicaZ motes in an indoor environment. In the experiment, a network prototype consisting of 25 MicaZ motes is constructed in a 5 × 5 grid on the floor, with grid spacing of 2 feet. Each MicaZ mote is augmented with a ranging sensor board that detects distance between two nodes by measuring the time of flight of specified acoustic pulses. Due to the reflections from walls and ceilings, which gives rise to null regions, the network connectivity is unexpectedly irregular and unsymmetrical, as illustrated in Figure 15(a).

# 7.1. Pairwise Ranging Measurements

Each ranging sensor board has a sounder, which can generate 4kHz fixed frequency acoustic signals, and a microphone that detects the tone produced by the sounder. In our experiment, even after employing robust statistical methods to filter some outliers caused by unexpected events, we find that qualities of pairwise ranging measurements still vary. Most are stable, with variances less than 4 cm, while some are highly uncertain, with variances as large as 25 cm, two of which are shown in Figure 15(a), colored red.

![](images/2e8d51c6fb957ac6cd1f4b87832aec165b598b9fb91ed9dc69933168c198622e.jpg)



![](images/7231752f84985e3ffcb21502419bacb27151055f5e06a2f84e8cf6945c26826b.jpg)



Fig. 13. The deployment and enclosure of motes.

![](images/1a394f2b41af42ef7f8bd276ff7c9c6e1899f4d7d6a623cb8687c026098d59ad.jpg)



Fig. 14. The network topology

# 7.2. Localization Experiment Results

We have done six sets of experiments using the 5 × 5 setting with the connectivity graph as in Figure 15(a). For each dataset, we have performed the following four types of AHLoS [Savvides et al. 2001] localization.

—NSNM: no outlier sifting, no malicious beacon;   
—SNM: with outlier sifting, no malicious beacon;   
—NSM: no outlier sifting, with a malicious beacon;   
—SM: with outlier sifting, with a malicious beacon.

For NSNM and SNM, there are three honest beacons, which broadcast their true locations, and for NSM and SM, we have four beacons, one of which is malicious and fakes its location. As dicussed in Section 2, the proposed method is capable of detecting malicious beacons. Table I presents the average location errors of these scenarios. Regardless of whether there is a malicious beacon, the proposed algorithm largely improves the location accuracy by rejecting outliers during the localization process. We further provide two examples to demonstrate the effectiveness of the proposed outlier detection method. Figure 15(b) shows the location results of NSNM and SNM, and

Table I. Localization Results 

<table><tr><td>Data Sets</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td></tr><tr><td>NSNM</td><td>15.73</td><td>12.43</td><td>10.64</td><td>10.80</td><td>9.78</td><td>11.42</td></tr><tr><td>SNM</td><td>12.52</td><td>11.95</td><td>8.72</td><td>9.54</td><td>9.74</td><td>12.57</td></tr><tr><td>NSM</td><td>18.95</td><td>26.24</td><td>20.79</td><td>18.29</td><td>14.03</td><td>14.70</td></tr><tr><td>SM</td><td>10.94</td><td>16.00</td><td>11.18</td><td>10.20</td><td>13.34</td><td>12.21</td></tr></table>

The reported data is in centimeters.

![](images/571a8addb6bf5ee4a32814f2c29552f60a9bcc65f4d69dc9ff446c2de4df2c6f.jpg)



(a) Connectivity graph

![](images/8d793f7adb80e4a02da873f7fac1dfbb63c97d92122deab7a58a9a28bd7dd4d5.jpg)



(b) NSNM vs. SNM

![](images/7f4f4bf3fab0395294e50d05c7a8936aaf149e51a5232e71ef7b90b6d6cddfd5.jpg)



(c) NSM vs. SM   
Fig. 15. The experimental network prototype and results, where black circles are true locations, and red and green diamonds represent the estimates of NSNM (NSM) and SNM (SM), respectively.

Figure 15(c) gives those of NSM and SM, where the node at the top right corner is a malicious beacon.

# 8. RELATED WORK

Location information is essential for a wide range of pervasive and mobile applications [Li and Liu 2009; Mo et al. 2009; Li et al. 2011; Wang et al. 2011]. In the literature of wireless ad hoc and sensor networks, many localization methods have been proposed and used in real-world positioning systems. In general, we can classify these methods into two major categories: range-based and range-free. Range-based methods usually assume sensor nodes have the capability to measure distances, based on Radio Signal Strength (RSS) [Seidel and Rappaport 1992] and Time Difference of Arrival (TDOA) [Savvides et al. 2001; Priyantha et al. 2000], and/or relative orientations of neighbor nodes, that is, Angle of Arrival (AOA) [Niculescu and Nath 2003; Chang et al. 2008]. By contrast, range-free methods use only node connectivity and hop-count [He et al. 2003; Lederer et al. 2009; Li and Liu 2010]. To build a full theoretical foundation, some works [Eren et al. 2004; Goldenberg et al. 2005] show that network localizability has a close relationship with graph rigidity theory. Recent work [Yang et al. 2010] employs wheel structure to study node localizability.

Because of the inevitability of noise in practice, how to control error accumulation in localization also attracts a lot of research. Error management [Liu et al. 2006] uses error registries to select nodes that participate in the localization procedure based on their relative contribution to the localization accuracy, and Moore et al. [2004] requires “robust quadrilaterals” to prevent large location errors introduced by flip ambiguities. From the perspective of security, outlier-resistant localization has also been studied. Minimum Mean Square Estimation (MMSE) is used to identify and remove malicious nodes in Liu et al. [2005], and Least Median of Squares (LMS), an estimator with high breakdown point, is adopted in Li et al. [2005]. A speculative filtering algorithm is designed in Hwang et al. [2007] to detect phantom nodes. Deriving inspiration from robust statistics, the recent work, SISR [Kung et al. 2009], uses a residual shaping influence function to deemphasize the bad nodes and bad links during the localization procedure. Besides requiring dense links, SISR is a centralized algorithm, which may prevent it from applying to large-scale deployments.

Different from those methods that require dense networks, the proposed outlier detection algorithm pays more attention to exploring and utilizing the topological structure, and thus works properly in networks that have moderate connectivity, which to the best of our knowledge, cannot be realized by existing approaches.

# 9. CONCLUSION

We have shown that noisy and outlier distance measurements greatly degrade the location accuracy of existing localization approaches. Hence, outlier detection serves as an essential and prior component for all range-based localization approaches. Based on graph embeddability and rigidity theory, we build the theoretical foundation for identifying outliers and accordingly design a bilateration generic cycle-based algorithm. The results of a network prototype and extensive simulations show that the proposed algorithm largely improves the location accuracy by modestly and wisely rejecting outliers during the localization process.

# REFERENCES

BDOIU, M., DEMAINE, E., HAJIAGHAYI, M., AND INDYK, P. 2004. Low-dimensional embedding with extra information. In Proceedings of the 20th Annual Symposium on Computational Geometry. 320–329.   
BERG, A. AND JORDAN, T. 2002. A proof of Connelly’s conjecture on 3-connected generic cycles. J. Comb. Theory B.   
BERGER, B., KLEINBERG, J., AND LEIGHON, T. 1996. Reconstructing a three-dimensional model with arbitrary errors. In Proceedings of the 28th Annual ACM Symposium on Theory of Computing. 449–458.   
CHANG, H., TIAN, J., LAI, T., CHU, H., AND HUANG, P. 2008. Spinning beacons for precise indoor localization. In Proceedings of the 6th ACM Conference on Embedded Network Sensor Systems. 127–140.   
EREN, T., GOLDENBERG, O., WHITELEY, W., YANG, Y., MORSE, A., ANDERSON, B., AND BELHUMEUR, P. 2004. Rigidity, computation, and randomization in network localization. In Proceedings of IEEE INFOCOM. Vol. 4. 2673–2684.   
GOLDENBERG, D., BIHLER, P., CAO, M., FANG, J., ANDERSON, B., MORSE, A., AND YANG, Y. 2006. Localization in sparse networks using sweeps. In Proceedings of the 12th Annual International Conference on Mobile Computing and Networking. 110–121.   
GOLDENBERG, D., KRISHNAMURTHY, A., MANESS, W., YANG, Y., YOUNG, A., MORSE, A., AND SAVVIDES, A. 2005. Network localization in partially localizable networks. In Proceedings of IEEE INFOCOM. vol. 1, 313–326.   
HAMPEL, F., RONCHETTI, E., ROUSSEEUW, P., AND STAHEL, W. 2005. Robust Statistics: The Approach Based on Influence Functions. Wiley Series in Probability and Statistics.   
HE, T., HUANG, C., BLUM, B. M., STANKOVIC, J. A., AND ABDEL ZAHER, T. 2003. Range-free localization schemes for large scale sensor networks. In Proceedings of the 9th Annual International Conference on Mobile Computing and Networking (MobiCom). 81–95.   
HENDRICKSON, B. 1992. Conditions for unique graph realizations. Siam J. Comput. 21, 1, 65–84.   
HWANG, J., HE, T., AND KIM, Y. 2007. Detecting phantom nodes in wireless sensor networks. In Proceedings of IEEE INFOCOM. 2391–2395.   
JACKSON, B. AND JORDAN´ , T. 2005. Connected rigidity matroids and unique realizations of graphs. J. Combin. Theory B 94, 1, 1–29.   
JACOBS, D. AND HENDRICKSON, B. 1997. An algorithm for two-dimensional rigidity percolation: The pebble game. J. Comput. Phys. 137, 2, 346–365.   
KUNG, H., LIN, C., LIN, T., AND VLAH, D. 2009. Localization with snap-inducing shaped residuals (SISR): Coping with errors in measurement. In Proceedings of the 15th Annual International Conference on Mobile Computing and Networking. 333–344.   
LAMAN, G. 1970. On graphs and rigidity of plane skeletal structures. J. Eng. Math. 4, 4, 331–340.   
LEDERER, S., WANG, Y., AND GAO, J. 2009. Connectivity-based localization of large-scale sensor networks with complex shape. ACM Trans. Sen. Net. 5, 4, 1–32.

LI, M., CHENG, W., LIU, K., HE, Y., LI, X., AND LIAO, X. 2011. Sweep coverage with mobile sensors. IEEE Trans. Mobile Comput. 10, 11, 1534–1545.   
LI, M. AND LIU, Y. 2009. Underground coalmine monitoring with wireless sensor networks. ACM Trans. Sen. Net. 5, 2.   
LI, M. AND LIU, Y. 2010. Rendered path: Range-free localization in anisotropic sensor networks with holes. ACM Trans. Network. 18, 1, 320–332.   
LI, Z., TRAPPE, W., ZHANG, Y., AND NATH, B. 2005. Robust statistical methods for securing wireless localization in sensor networks. In Proceedings of the 4th International Symposium on Information Processing in Sensor Networks. 91–98.   
LIU, D., NING, P., AND DU, W. 2005. Attack-resistant location estimation in sensor networks. In Proceedings of the 4th International Symposium on Information Processing in Sensor Networks.   
LIU, J., ZHANG, Y., AND ZHAO, F. 2006. Robust distributed node localization with error management. In Proceedings of the 7th ACM International Symposium on Mobile Ad Hoc Networking and Computing. 250–261.   
MO, L., HE, Y., LIU, Y., ZHAO, J., TANG, S., LI, X., AND DAI, G. 2009. Canopy closure estimates with greenorbs: Sustainable sensing in the forest. In Proceedings of the 7th ACM Conference on Embedded Networked Sensor Systems. 99–112.   
MOORE, D., LEONARD, J., RUS, D., AND TELLER, S. 2004. Robust distributed network localization with noisy range measurements. In Proceedings of the 2nd International Conference on Embedded Networked Sensor Systems. 50–61.   
NICULESCU, D. AND NATH, B. 2003. Ad hoc positioning system (APS) using AOA. In Proceedings of IEEE INFOCOM. 1734–1743.   
PRIYANTHA, N., CHAKRABORTY, A., AND BALAKRISHNAN, H. 2000. The cricket location-support system. In Proceedings of the 6th Annual International Conference on Mobile Computing and Networking. 32–43.   
SAVVIDES, A., HAN, C., AND STRIVASTAVA, M. 2001. Dynamic fine-grained localization in ad hoc networks of sensors. In Proceedings of the 7th Annual International Conference on Mobile Computing and Networking. 166–179.   
SAXE, J. 1979. Embeddability of weighted graphs in k-space is strongly NP-hard. Carnegie-Mellon University, Department of Computer Science.   
SEIDEL, S. AND RAPPAPORT, T. 1992. 914 MHz path loss prediction models for indoor wireless communications in multifloored buildings. IEEE Trans. Antennas Propag. 40, 2, 207–217.   
WANG, X., FU, L., TIAN, X., BEI, Y., PENG, Q., GAN, X., YU, H., AND LIU, J. 2011. Converge-cast: On the capacity and delay tradeoffs. IEEE Trans. Mobile Comput. 99, 1.   
YANG, Z. AND LIU, Y. 2010. Quality of trilateration: Confidence-based iterative localization. IEEE Trans. Parallel Distrib. Syst. 21, 5, 631–640.   
YANG, Z., LIU, Y., AND LI, X. 2010. Beyond trilateration: On the localizability of wireless ad hoc networks. IEEE/ACM Trans. Network. 18, 6, 1806–1814.

Received September 2011; revised January 2012; accepted March 2012