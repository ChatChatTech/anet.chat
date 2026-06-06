# Self-Monitoring for Sensor Networks

Dezun Dong

Yunhao Liu

Xiangke Liao

# ABSTRACT

Local monitoring is an effective mechanism for the security of wireless sensor networks (WSNs). Existing schemes assume the existence of sufficient number of active nodes to carry out monitoring operations. Such an assumption, however, is often difficult for a large scale sensor network. In this work, we focus on designing an efficient scheme integrated with good self-monitoring capability as well as providing an infrastructure for various security protocols using local monitoring. To the best of our knowledge, we are the first to present the formal study on finding optimized self-monitoring topology for WSNs. We show the problem is NPcomplete even under the unit disk graph (UDG) model, and give the upper bound on the approximation ratio. We further propose two distributed polynomial algorithms with provable approximation ratio to address this issue. Through comprehensive simulations, we evaluate the effectiveness of this design.

# Categories and Subject Descriptors

C.2.0 [Computer-Communication Networks]: General – Security and Protection. F.2.2 [Analysis of Algorithms and Problem Complexity]: Nonnumerical Algorithms and Problems – Complexity of proof procedures.

# General Terms

Algorithms, Theory, Security.

# Keywords

Wireless Sensor Network, Security, Self-Monitoring, NP-Complete.

# 1. INTRODUCTION

Wireless sensor networks (WSNs) are emerging as a promis-

Dezun Dong is a PHD student at the School of Computer in National University of Defense Technology, Changsha, Hunan, China, dong@ nudt.edu.cn. He is co-supervised by Dr. Yunhao Liu.

Yunhao Liu is with the department of Computer Science in Hong Kong University of Science and Technology, liu@cse.ust.hk. He is also a professor at Xi’an Jiaotong University.

Xiangke Liao is a professor at the School of Computer in National University of Defense Technology, Changsha, Hunan, China, xkliao@ nudt.edu.cn.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee.

MobiHoc’08, May 26-30, 2008, Hong Kong SAR, China.

Copyright 2008 ACM 978-1-60558-073-9/08/05...\$5.00.

![](images/0bcc344c39ad4dc51fc271f536758fa5e3d3e4fe68b4a1361677c5cd37117d2b.jpg)



Figure 1. Local monitoring.

ing platform for many important applications such as military surveillance, homeland security, emergency response, forest fire monitoring, etc. Security is important for mission-critical applications which work in unattended and even hostile environment [1, 2]. One of the most severe security threats in sensor networks is node compromise. Once some nodes are compromised, the attackers can use them to mount a variety of attacks. It is rather challenging to provide effective security mechanisms against compromised nodes in resource-limited WSNs [3].

Based on local monitoring (or watchdog) technique [4-7], many approaches have been proposed to secure sensor networks in face of compromised nodes. The basic idea of local monitoring is illustrated in Fig. 1. The dashed circle denotes the transmission range of a node. Node S, M1, M2 monitor the link from S to R, since they are able to monitor the traffic that R receives from S and sends to others.

In WSNs, local monitoring is a promising security mechanism as an effective complement for cryptographic mechanisms. Existing local monitoring schemes assume the existence of sufficient nodes to carry out the monitoring function. Such a requirement is often practically difficult when we consider minimizing the number of monitoring nodes selected for a large scale WSN.

For example, as shown in Fig. 2, the dots and lines denote the active sensor nodes and communication links between them. The circles denote the sleeping nodes. We desire that every communication link is monitored by two other nodes except for the end nodes of the link. Note that this requirement cannot be satisfied since there are not enough (two) active nodes neighboring to links. Hence, we have to select additional sleeping nodes and activate them. For independent selection for each link, the nodes are selected randomly among those that are able to monitor a link. Figure 2(a) shows the results of random selection, where 38 additional nodes are selected. As shown in Figure 2(b), only 10 nodes are needed, if we adopt an optimal strategy. The nodes within box are the additional nodes selected to satisfy one communication link monitored by two nodes.

We focus on the fundamental problem of designing a selfmonitoring topology, where each communication link can be monitored by nodes within the network. We prove that finding an optimal self-monitoring topology is NP-complete even when we model the communication network as a unit disk graph (UDG) with a geometric representation. We provide the approximability results in centralized scenario, and prove the existence of polynomial-time approximation scheme (PTAS) for this problem when restricted in some specific graphs. We develop two efficient and distributed approximation algorithms with provable approximation ratio and time complexity guarantee for large scale sensor networks. Moreover, we conduct extensive simulations to demonstrate the effectiveness of this design.

![](images/87edb030b418630b72f190fa56c99a82d6efd8f2ae2be99302c816bbae2edfcd.jpg)



(a) Random selection

![](images/49e9b02cbef18dc291a3028cedc7a2f253e25ae2ed4b8b8fbd7f6b6af51f95f3.jpg)



(b) Optimal selection   
Figure 2. Comparison of random and optimal selection.

The rest of the paper is organized as follows. Related work is presented in Section II, and problem definition is given in Section III. Hardness of the problem and approximability results are presented in Section IV. Distributed algorithms are presented in Section V. Performance evaluation is presented in Section VI. We have some discussions in VII, and conclude this work in Section VIII.

# 2. RELATED WORK

WSNs are vulnerable to a wide range of security attacks including wormhole, black hole, spoofed, altered, replayed routing information, selective forwarding, sybil attack, DoS, etc. [2, 3]. There have been many proposals using cryptography to ensure secure communication such as SPINS[1], etc.

Cryptography provides an efficient mechanism to achieve data confidentiality, data integrity, node authentication, and secure routing. Nevertheless, cryptography alone is not sufficient for node compromise attacks and novel misbehaviors in sensor networks [6]. Researchers therefore attempt to use non-cryptographic techniques to solve the problems beyond the capability of cryptographic security [4-7].

Previous studies introduce the concept of watchdog or local monitoring to mitigate attacks in sensor and ad hoc networks [4-9]. The idea of watchdog is first introduced by Marti et al. in ad hoc networks for detecting mischievous nodes [10]. Since then extensive efforts have been made in ad hoc [11-13] and sensor networks [4-7], falling into three categories: secure routing, reputation and trust systems, and intrusion detection.

For secure routing, a lightweight protocol called DICAS is proposed by Khalil et al. [4], which mitigates the control and data traffic attacks in sensor networks with the help of local monitoring. They design a countermeasure for wormhole attacks, called LITEWORP [5], which uses guard nodes to attest the source of each transmission. Neighbor watch [7] is employed by a hop-byhop resilient packet-forwarding scheme. For reputation and trustbased systems, neighbor watch is used as a component to monitor neighborhoods and collect information to build trust relationships among nodes in the network, such as RFSN[6], CONFIDANT[11], CORE[13], etc. For intrusion detection systems, local monitoring is used to build decentralized protocols [9, 12].

Local monitoring scheme places new requirement to a sensor connectivity topology. There are two existing topology control schemes: radio power control and wake/sleep schedule, including LEACH [14], SPAN [15], STEM [16], etc. The main goal of those schemes, however, is to achieve energy efficient communication. They aim at extending network lifetime, enhancing network utilization and capacity, minimizing interference, reducing high end-to-end packet delays, and increasing the robustness to node failures. They do not construct and optimize topologies with local monitoring properties.

Recently, Khalil et al. [17] propose a on-demand sleep-wake protocol to shorten the time a node needs to be awake for the purpose of monitoring. They do not, however, consider the optimized selection of monitoring nodes in the network, but focusing on how to schedule nodes to meet the monitoring requirement for given communication links.

It is worth noting that the focus of the self-monitoring mechanism proposed by Hsin et al. [18] is completely different from this work. They pay more attention on the system-level fault diagnosis of the network, especially detecting node failures. They do not deal with malicious behaviors as what are considered in the works [4, 5, 7]. On the other hand, our study emphasizes the optimized node selection for the local monitoring scheme.

# 3. SELF-MONITORING PROBLEM

We consider static (dense) sensor networks in which all the communication links are bidirectional. We define the communication graph on the network as a directed graph $G _ { c } ,$ where sensors are represented by vertices. A pair of opposite directed edges $< u , \nu >$ and <v,u> exist if there is a direct communication channel between node u and v. We define the active network created and scheduled by topology control algorithm as topology graph, which is a subgraph of communication graph $G _ { c } .$ In the rest of the paper, we use E(G) and V(G) to denote the edge and vertex set of a graph G, respectively. Node/vertex, as well as link/edge will be used interchangeably. It is important to note that the assumption about the bidirectional communication links is just for convenient presentation of algorithm. Indeed all definitions and theorems in the paper are still applicable when the communication links are directional.

Definition 3.1 Given a directed edge $e ~ = < \nu _ { I } , \nu _ { 2 } > \in \mathrm { ~ E } ( G _ { c } ) .$ , $\nu \in \mathrm { V } ( G _ { c } ) \backslash \nu _ { I } , \mathrm { i f } < \nu _ { I } , \nu > , < \nu _ { 2 } , \nu > \in \mathrm { E } ( G _ { c } )$ , we say v can monitor edge e. Given an edge set $E \subseteq \operatorname { E } ( G _ { c } )$ , a vertex set $V \subseteq \mathrm { V } ( G _ { c } ) , k \in \mathbb { N }$ , if any edge e in E can be monitored by at least k different vertices in $V ,$ we say V can k-monitor the edge set E.

Definition 3.2 Given a graph $G \subseteq G _ { c } ,$ and an edge set $E \subseteq \operatorname { E } ( G ) .$ , let $b \in \mathbb { Z } _ { 0 , + } ^ { E }$ + , if for any $e \in E ,$ there are just $b ( e )$ different vertices in V(G) that can monitor e, we say G has the b-self-monitoring capability about edge set E. Further, if given k∈ \` , for any e∈ $E ,$ b(e)≥k, we say G has the k-self-monitoring capability about edge set E.

The construction of connectivity topology of WSNs is often optimized for multiple objectives, such as required connectivity and coverage, more specific and application-oriented requirements, and so on. Self-monitoring capability is a new requirement for connectivity topology, for which it is necessary to investigate how to integrate the self-monitoring sub-objective with previous ones. To have our algorithms generally applicable, we treat selfmonitoring as an independent function module, that is, we investigate how to convert a general connectivity topology into a topology with self-monitoring capability at lowest cost. We formalize the transition as follows.

Definition 3.3 Minimum Self-Monitoring Topology Problem (MSMTP):Given $G _ { c } , G _ { \theta } \subseteq G _ { c } , k \in \mathbb { N }$ , finding a subgraph $G _ { I } \subseteq G _ { c }$ , such that $G _ { \theta } \subseteq G _ { I } , \ \mathsf { V } ( G _ { I } )$ can k-monitor $\operatorname { E } ( G _ { \theta } )$ and $| \mathrm { V } ( G _ { I } ) |$ is minimized.

Definition 3.3 is equivalent to adding minimum number of vertices in $\mathsf { V } ( G _ { c } ) \backslash \mathrm { V } ( G )$ to satisfy the k-monitoring requirement, as formally listed in Definition 3.4.

Definition 3.4 Minimum Patching Monitoring Set Problem (MPMSP): Given $G _ { c }$ and $G ,$ an edge set $E _ { p } \subseteq \operatorname { E } ( G )$ which denotes the edges that cannot be k-monitored in G, let $b \in \mathbb { N } ^ { E _ { p } }$ be the monitoring number for $E _ { p , \mathrm { ~ } } V _ { p }$ denote $\mathsf { V } ( G _ { c } ) \backslash \mathsf { V } ( G )$ , finding a subset of vertices $V \subseteq V _ { p }$ such that V can b-monitor $E _ { p }$ and |V| is minimized.

# 4. PROBLEM HARDNESS AND APPROXIMATION

In this section, we first prove that the MPMSP problem is NPcomplete even the communication graph is restricted to be UDG with a geometric representation. We the discuss the bounds on approximation ratio for MPMSP.

# 4.1 Problem Hardness

The hardness of MPMSP largely depends on the graph model for representing communication topology of a sensor network. Among those models, UDG is probably the simplest one [19]. Hence, this discussion will start from proving MPMSP is NPcomplete in UDG with a geometric representation, and then extend it to generalized models.

We use the proximity model [20] to define UDG, that is, points in the plane form a UDG with a vertex corresponding to a point and an edge between two vertices exists if and only if the Euclidean distance between the two points is at most a constant bound C. Before presenting the proof, related definitions and notations are listed as follows.

Definition 4.1 Given $( G _ { c } , G , E _ { p } , V _ { p } , b )$ of a MPMSP, we define the monitoring degree of a vertex v in $V _ { p }$ as the number of edges in $E _ { p }$ that can be v monitored, denoted by d(v); the monitored degree of an edge e in $E _ { p }$ is defined as the number of vertices in $V _ { p }$ that can monitor $e ,$ denoted by l(e); and we denote the maximum monitoring degree as D=max{d(v), v∈ $\mathnormal { V } _ { p } \mathnormal  \}$ , and maximum monitored degree as L=max $\{ \lambda ( e ) , e \in E _ { p } \}$ .

THEOREM 4.1. When D¥3, MPMSP is NP-complete in UDG with a geometric representation.

PROOF. To show MPMSP is NP-complete, it is sufficient if we prove that when the monitored number b is specialized to a constant $k { \geq } 2 .$ , the problem is NP-complete. We denote it as kMPMSP.

To show that kMPMSP belongs to NP, we need to show whether every edge, $e ,$ in $E _ { p }$ is k-monitored by some vertices in $V \subseteq V _ { p } ,$ , which can be accomplished in polynomial time.

To prove that kMPMSP in UDG is NP-hard, we can show that the Vertex Cover problem in planar graph with maximum degree 3 is polynomial-time reducible to kMPMSP, as the former is wellknown NP-complete [21].

![](images/f7fda9cfd24083b93e542a2abe9de52cd839f5a17c4ce056b1b748e1b2975b99.jpg)



Figure 3. Locally redraw a grid unit.

![](images/10645a8acb5686d8124349b3f0be4b724025bb8fdc4f5a362b363e86dc51eff4.jpg)



Figure 4. Gadgets W .

Hence, we will present a polynomial-time transformation that takes an arbitrary planar graph $G _ { a }$ of maximum degree 3 and constructs a kMPMSP $( G _ { c } , G , E _ { p } , V _ { p } , k )$ in UDG with a geometric representation and D¥3. Moreover, knowing minimum patching monitoring set of $( G _ { c } , G , E _ { p } , V _ { p } , k )$ , we are able to compute mini -mum vertex cover of $G _ { a }$ in polynomial time.

The key issue for the construction of UDG $G _ { c }$ is the selection of points set and the distance bound $C ,$ which can be carried out in two steps.

Step 1. We first draw $G _ { a }$ in a plane by constructing a planar orthogonal grid embedding [22] for it. The embedding maps (1) vertices to distinct grid points, and (2) edges to nonintersecting grid paths. All vertices and bends are located on integer grid points. Such a construction of a planar orthogonal grid embedding does exist [23] and can be finished in polynomial time $O ( | \mathrm { V } ( G _ { a } ) | ) [ 2 2 ]$ . Second, we enlarge the scale such that the unit length of grid is 2m+1, m∈ \` , and m¥4. Let |e| denote the length of embedding image of $e \in \operatorname { E } ( G _ { a } )$ , for any $e _ { i } \in \operatorname { E } ( G _ { a } )$ , |ei| is a multiple of 2m+1. Here we use one notation to denote both vertex/edge and its drawing. Third, for any $e _ { i } \in \operatorname { E } ( G _ { a } )$ , if |ei| is even, we select a segment of unit grid in $e _ { i }$ and redraw it locally such that |ei| increments by 1 and becomes an odd, as illustrated in Fig. 3. The line segment of length 2m+1 from $i _ { 0 }$ to $i _ { 2 m + \mathrm { 1 } }$ denote a grid unit. Delete the segment $\left( i _ { m - l } , \ i _ { m + l } \ \right)$ of length $^ { 2 , }$ reconnect $i _ { m - I } ,$ $i _ { m + 1 }$ 1 by three segments of length $1 , ( i _ { m - l } , i _ { m , a } ) , ( i _ { m , a } , i _ { m , b } ) , ( i _ { m , b } , i _ { m + l } ) .$ After redrawing, the embedding of $G _ { a }$ is no more an orthogonal grid embedding. We then insert all the vertices of $G _ { a }$ to G and $G _ { c } .$

Step 2. For an edge $e _ { i } \in \operatorname { E } ( G _ { a } )$ , we place a number $\scriptstyle { L = | e _ { i } | - 1 }$ of vertices on $e _ { i }$ by making the interspaces of two adjacent vertices be equal to 1, and denote them as $\nu _ { i , l } \in [ 1 , L ]$ . We add all these vertices into $G$ and $G _ { c } .$ . Since |ei| is odd, $| e _ { i } | - 1$ is even. Let $\nu _ { i , 0 } ,$ $\nu _ { i , L + I }$ denote the endpoints of $e _ { i \cdot }$ Now, for each vertex $\nu _ { i , l }$ in $G ,$ $l \in [ 1 , L ]$ , we add a vertex $u _ { i , l }$ such that $\mathrm { d } ( \nu _ { i , l } , u _ { i , l } ) { < } R$ , where R is a constant. We discuss the value of R later. We add all these vertices $u _ { i , l }$ to $G _ { c }$ . If we set $R { = } 0 . 1 , C { = } 1 . 1$ , it is straightforward to verify that the following inequations can be satisfied:

$$
\begin{array}{l} 1) \forall e _ {i} \in \mathrm{E} (G _ {a}), l \in [ 1, L ], \\ d (u _ {i, l}, v _ {i, l - 1}), d (u _ {i, l}, v _ {i, l}), d (u _ {i, l}, v _ {i, l + 1}) <   C \\ d \left(v _ {i, l}, v _ {i, l - 1}\right), d \left(v _ {i, l}, v _ {i, l + 1}\right) <   C \\ 2) \forall e _ {i} \in \mathrm{E} (G _ {a}), l \in [ 1, L ], \forall v \in \mathrm{V} (G) \backslash \left\{v _ {i, l - 1}, v _ {i, l}, v _ {i, l + 1}, u _ {i, l} \right\} \\ d (u _ {i, l}, v) > C \\ \end{array}
$$

$$
\begin{array}{l} 3) \forall e _ {i} \in \mathrm{E} (G _ {a}), l \in [ 1, L ], \forall v \in \mathrm{V} (G) \backslash \{v _ {i, l - 1}, v _ {i}, v _ {i, l + 1} \} \\ d (v _ {i, l}, v) > C \end{array}
$$

Step 3. For each edge in $G ,$ say $( \nu _ { i , l } , \nu _ { i , l + I } )$ , we place vertices $m _ { i , l , 1 } , . . . , m _ { i , l , \mathrm { k } } , y _ { i , l , 1 } , y _ { i , l , 2 }$ nearby the edge, and adjust the location of those vertices properly such that $G r a p h [ \nu _ { i , l } , \nu _ { i , l + l } , \ y _ { i , l , 1 } , \ y _ { i , l , 2 } ,$ $m _ { i , l , \mathrm { l } } , . . . , m _ { i , l , \mathrm { k } } ]$ (or $G r a p h [ \nu _ { i , l + l } , \nu _ { i , l } , y _ { i , l , 1 } , y _ { i , l , 2 } , m _ { i , l , 1 } , . . . , m _ { i , l , \mathrm { k } } ] )$ with neglecting edges $( m _ { i , l , r } , m _ { i , l , s } ) , r , s \in [ 1 , k ]$ , is isomorphic to gadgets $W [ x _ { 1 } , x _ { 2 } , y _ { 1 } , y _ { 2 } , m _ { 1 } , . . . , m _ { \mathrm { k } } ]$ as shown in Fig. 4. The lines denote the connection relationship. Note that each $m _ { i } , i \in [ 2 , k ]$ , is connected to $x _ { 1 } , x _ { 2 } , y _ { 1 } , y _ { 2 }$ , but not all the lines are drawn for concision. We restrict that only one of the two vertices, $\nu _ { i , l }$ and $\nu _ { i , l + l , }$ to be qualified for mapping to $x _ { 2 }$ in $W ,$ and we denote it as $x _ { i , l , 2 }$ and the other as $x _ { i , l , 1 }$ . We insert all the vertices into $G _ { c } ,$ while only insert $y _ { i , l , 1 } .$ $y _ { i , l , 2 }$ into G. Also, we constrain that the edge $( y _ { i , l , 1 } , y _ { i , l , 2 } )$ is only able to form a $K _ { 3 }$ graph with vertices $m _ { i , l , 1 } , . . . , m _ { i , l , \mathrm { k } }$ among all vertices in $G _ { c } ,$ and $m _ { i , l , 1 } , . . . , m _ { i , l , \mathbf { k } }$ is only able to form a $K _ { 3 }$ with edges $( x _ { i , l , 1 } , \ x _ { i , l , 2 } \ ) , ( x _ { i , l , 2 } \ , \ y _ { i , l , 1 } ) , ( y _ { i , l , 1 } , \ y _ { i , l , 2 } )$ among all edges in $G .$ Clearly, all the constraints can be achieved by properly adjusting the positions of new added vertices when setting the parameter values R and C as in step 2.

Till now we have finished the transformations in polynomial time. Moreover, our constructed graph $G _ { c }$ and G are both connected UDG with the geometric representation, and G is a subgraph of $G _ { c }$ . We can check that G has the 0-self-monitoring capability about any edge in $E ( G )$ . To make G have the k-selfmonitoring capability about $E _ { p } { = } \mathrm { E } ( G )$ , we can set $V _ { p } { = } \mathrm { V } ( G _ { c } ) \backslash \mathrm { V } ( G )$ . Thus, we obtain the kMPMSP $( G _ { c } , G , E _ { p } , V _ { p } , k )$ . It is trivial to verify that maximum monitoring degree D is 3 in our constructed problem instance.

Finally, it is easy to verify that $G _ { a }$ has a vertex cover set of size N if and only if there is a patching monitoring set of $\begin{array} { r } { M { = } N { + } \sum _ { e _ { i } \in E ( G _ { a } ) } ( k { + } 1 / 2 ) ( | e _ { i } | - 1 ) } \end{array}$ size for the kMPMSP $( G _ { c } , G , E _ { p } , V _ { p }$ , k). Thus, the NP-completeness of kMPMSP is proved. É

The UDG model is idealistic. Some researchers have proposed other relaxed models for sensor network, such as, quasi unit disk graph model, bounded independence graph, unit ball graph, UDG with hop interference, and general graph [24]. We call those graphs extended UDG since UDG is a subgraph of them.

COROLLARY 4.2. When D¥3, MPMSP is NP-complete in extended UDG.

THEOREM 4.3. When D§2, MPMSP is polynomial-time solvable in general graph.

PROOF. When $\Delta \le 2$ , MPMSP can be formalized as the simple bedge covers on multigraph, which is polynomial-time solvable [25]. Given MPMSP $( \bar { G } _ { c } , \bar { G } , E _ { p } , V _ { p } , b ) .$ , the procedures of constructing multigraph $G _ { m }$ are as follows. An edge $e \in E _ { p }$ corresponds to a vertex $\nu _ { e } \in \mathrm { V } ( G _ { m } )$ . If a vertex v ∈ $V _ { p }$ can monitor only one edge $e \in E _ { p } ,$ we add a distinct loop to $\nu _ { e } \in \mathrm { V } ( G _ { m } )$ . If a vertex y ∈ $V _ { p , }$ can monitor both edge $f , g \in E _ { p } ,$ we also add a distinct edge (vf, vg)y to Gm. $G _ { m }$

# 4.2 Approximability Results

THEOREM 4.4. There exists r-approximation algorithm for MPMSP in general graph, where $\rho = m i n ( H ( \Delta ) , \Lambda )$ .

PROOF. When we disposal the MPMSP in general graph model, clearly, the MPMSP can be formalized as the set multi-cover problem. Hence we can acquire the approximation ratio from set multi-cover [26]. $\begin{array} { r } { H ( n ) = \sum _ { i = 1 } ^ { n ^ { * } } 1 / i } \end{array}$ is the nth harmonic number. É

THEOREM 4.5. There exists a polynomial-time approximation scheme for MPMSP in UDG with a geometric representation.

PROOF. Given $( G _ { c } , G , E _ { p } , V _ { p } , b )$ , when $G _ { c }$ is a UDG with geometric representation, all vertices that can monitor the same edge lie in the lune region which is the intersection of two disks with their centers the endpoints of the monitored edge. As a result, every edge e in $E _ { p }$ is corresponding to (one-to-one) a lune $l _ { e }$ in the plane, and the MPMSP can be considered as selecting minimum size of vertices set from $V _ { p }$ to hit the lunes such that each lune, say $l _ { e } ,$ is hit $b ( e )$ times.

We design a shifting strategy [27] to approximate MPMSP. Let R denote the least rectangular region in which graph $G _ { c }$ can be drawn. For a positive integer m>0, and even integers $i , j ,$ where 2§i, j§m, we partition the region R into squares by horizontal lines at $l \equiv i$ mod m and vertical lines at $t \equiv j$ mod m. Let $S _ { i , j }$ denote the set of squares for a fixed pair $i , j .$ . Let S denote the union of all the $S _ { i , j \cdot } \operatorname { A }$ lune is said to be belonging to a square if and only if its geometric centre lies in the square. For square s ∈ $S _ { i , j } ,$ let $L ( s )$ denote the set of lunes belonging to the square s.

We assume the node density of the network has an upper bound, so the number of nodes in each $m \times m$ square is $O ( m ^ { 2 } )$ . Thus, the optimal solution in each square can be found in polynomial time using complete enumeration for a given constant m. The union of those sets gives a candidate hitting set for fixed $i , j .$ By changing the parameter $i , j ,$ we have the minimum set.

Now we analyze the approximation ratio. Let $H _ { o }$ be an optimal hitting set, and let H be the set obtained by the shifting strategy. For fixed $i , j ,$ let $H _ { o } ( i , ^ { * } ) , H _ { o } ( ^ { * } , j ) , H _ { o } ( i , j )$ respectively be the vertices set in $H _ { o }$ and lie in lunes intersecting horizontal active lines, vertical active lines, and both horizontal and vertical active lines. Let $H _ { o } ( s )$ be vertices in $H _ { o }$ and in $L ( s ) , O P T ( s )$ be the optimum hitting set for lunes $L ( s )$ . We have

$$
\mid H \mid \leq \mid \bigcup_ {s \in S _ {i, j}} O P T (s) \mid \leq \sum_ {s \in S _ {i, j}} \mid O P T (s) \mid \leq \sum_ {s \in S _ {i, j}} \mid H _ {o} (s) \mid
$$

Since vertices in lunes that hit an active line can be used in at most four squares, we have

$$
\sum_ {s \in S _ {i, j}} | H _ {o} (s) | \leq 3 | H _ {o} (i, j) | + | H _ {o} |
$$

Note that we set the shifting step be two units, so that all lunes that hit one horizontal(or vertical) active line do not intersect with lunes that hit another horizontal(or vertical) active line. Consequently, we obtain the following inequations,

$$
\sum_ {2 \leq i \leq m} | H _ {o} (i, *) | \leq | H _ {o} |, \sum_ {2 \leq i \leq m} | H _ {o} (*, j) | \leq | H _ {o} |
$$

There exist some choices of $( i , j )$ , such that

$$
\left| H _ {o} (i, *) \right| \leq 2 \left| H _ {o} \right| / m, \left| H _ {o} (*, j) \right| \leq 2 \left| H _ {o} \right| / m
$$

For the choice of $( i , j )$ , we have

$$
\left| H _ {o} (i, j) \right| = \left| H _ {o} (i, *) \bigcup H _ {o} (*, j) \right| \leq \left| H _ {o} (i, *) \right| + \left| H _ {o} (*, j) \right| \leq 4 \left| H _ {o} \right| / m
$$

And then,

$$
\mid H \mid \leq (1 + 1 2 / m) \mid H _ {o} \mid
$$

Hence, given $\varepsilon > 0 _ { ; }$ , let $m { > } 0$ be the smallest even integer such that $( 1 2 / m ) { \leq } \varepsilon$ , the solution H has 1+ ε approximation ratio. É

# 5. DISTRIBUTED ALGORITHM

As a large-scale sensor network typically work in a distributed and ad hoc manner, in this section we present two localized algorithms for the MPMSP problem, called local maximal element (LME) and locally dual-feasible (LDF). None of them uses location information, and they are independent of communication models.

For a general communication network $G \subseteq G _ { c } ,$ we assume that the self-monitoring requirements for each link is known for all the nodes, or is specified by the upper layer protocols using the selfmonitoring as an underlying function.

Each node in $G$ exchanges the neighbor list with one-hop neighbors. Thus, a node $P$ can determine which links can be monitored by $P$ and which nodes can monitor the links adjacent (connecting) to P. The links that are lower to the self-monitoring requirement form the $E _ { p } ,$ , and monitoring number of each link, $b ,$ is determined accordingly. All nodes in $\mathsf { V } ( G _ { c } ) \backslash \mathsf { V } ( G )$ form the set $V _ { p . }$

Given $G _ { c }$ and G, a MPMSP $( G _ { c } , G , E , V , b )$ is denoted as MPMSP $( E , V , b )$ , in which two vertices in $V$ are said to be adjacent if they are monitoring the same edge in E. The adjacent vertex set of $\nu ,$ denoted as $\mathbf { A } ( \nu )$ , is the set of all the vertices adjacent to v in $V .$ The monitoring degree of $\nu ,$ denoted as d(v), is the number of edges in E that can be monitored by v.

# 5.1 Local Maximal Element Algorithm

For a MPMSP (E,V,b), LME deals with the problem from the candidate vertices in V. A candidate vertex is chosen only if it is optimal within its adjacent vertex set. The priority of a vertex depends on its monitoring degree. It means that a vertex has higher priority if its monitoring degree is high. We break the tie by selecting the vertex with the largest ID among these vertices.

LME is carried out in a parallel manner. In each round, all the locally optimal vertices are selected. The monitored degree of every edge and candidate monitoring vertex set are updated accordingly. LME is run iteratively until the solution is found or the candidate monitoring vertex set V is empty. Note that a loosely synchronous clock among local vertices is adequate for LME, instead of a global synchronization.

As illustrated in Fig. 5, where the communication graph are modeled as UDG, the vertex having higher monitoring degree means it falls into the overlap field of more lunes. The circles denote the sensor nodes, and the lines denote the links in the connectivity topology. The bold lines denote the edges that do not meet the 1-self-monitoring requirement. The node v that falls in the overlap of 4 lunes with borderline is first selected into the patching monitoring set, for it can monitor more edges than its adjacent nodes. The squares denote a solution found by LME for 1-self-monitoring.

THEOREM 5.1. The LME algorithm computes a $H ( \Delta )$ approximation for MPMSP in general graph within O(D) rounds w. $h . p .$ .

We later will present a strict proof to show LME is a faithful implementation of the sequential greedy algorithm. The conclusion somehow counters to the intuition, since sequence greedy selects the globally optimal node in each step while LME only selects locally maximal nodes in each round.

Given an instance $( E , V , b )$ , each element in V has a priority value. Now we define a strict partial order relationship $^ { \alpha \zeta \zeta } \succ ^ { \zeta \zeta }$ on V. Relationship $^ { \mathfrak { c } \mathfrak { c } } \succ ^ { \mathfrak { n } }$ is irreflexive and transitive, defined by: for u, v ∈ $V ,$ if the priority of u is higher than that of v and the selection of one will decrease the priority of the other directly, then $u \succ \nu . \mathrm { I f } u \succ \nu ,$ v ; w for $u , \nu , w \in V ,$ then $\nu \succ \mathbf { w }$ . Thus, set $V$ with the strict order $^ { \ast \mathfrak { c } } \succ ^ { \mathfrak { n } }$ forms a poset. Apparently, such a poset is not necessarily total. Intuitively, the strict order “ ; ” symbolizes the direct or indirect dependence relationship among candidate nodes in V. We further de fine a term top-antichain as the set of all maximal elements1 in $V .$

![](images/f4aaa6ae2d21fbddfc37726567a21420ead54bf29d837df9f813afd7736c28fd.jpg)



Figure 5. Local maximal element algorithm.

Given $( E , V , b ) ,$ , we use $( E ( \nu ) , \ V ( \nu ) , \ b ( \nu ) )$ to denote the reduced problem instance after adding the vertex v ∈ V into the patching monitoring set.

LEMMA 5.2. Given $( E , V , b )$ , let $C _ { I } = [ c _ { I } , c _ { 2 } , . . . , c _ { k - I } , c _ { k } , c _ { k + I } , . . . , c _ { N } ]$ be a greedy solution sequence $f o r ( E , V , b ) .$ , ck be a maximal element in $V ,$ then $C _ { 2 } = [ c _ { I } , c _ { 2 } , . . . , c _ { k - I } , c _ { k + I } , . . . \ , c _ { N } ]$ is a greedy solution sequence $f o r \left( E ( c _ { k } ) , V ( c _ { k } ) , b ( c _ { k } ) \right)$ .

PROOF. We use $( E _ { I , i } , V _ { I , i } , b _ { I , i } )$ to denote the reduced problem of (E, $V ,$ b) after selecting the vertices of $\{ c _ { l } \in C _ { l } , \ l \in [ 1 , i ] \}$ and adding them into the patching monitoring set, and use $P _ { I , i } ( \nu )$ to denote the priority of node v in $( E _ { I , i } , V _ { I , i } , b _ { I , i } )$ . We use $( E _ { 2 , i } , V _ { 2 , i } , b _ { 2 , i } )$ to denote the reduced problem of $( E ( c _ { k } ) , V ( c _ { k } ) , b ( c _ { k } ) )$ after selecting the vertices of $\{ c _ { l } \in C _ { 2 } , l \in [ 1 , i ] , l \neq k \}$ and adding them into the patching monitoring set, and use $P _ { 2 , i } ( \nu )$ to denote the priority of node v in $( E _ { 2 , i } ,$ $V _ { 2 , i } , b _ { 2 , i } )$ .

Since $C _ { 1 }$ is a solution for $( E , V , b )$ , it is clear C2 is a solution sequence for $( E ( c _ { k } ) , V ( c _ { k } ) , b ( c _ { k } ) )$ . Thus we only need to show that $C _ { 2 }$ is a greedy sequence, that is, $P _ { 2 , i } ( c _ { i } ) – P _ { 2 , i } ( c _ { j } )$ for $c _ { i } , c _ { j } \in C _ { 2 }$ and $i { < } j .$ . Since $c _ { k }$ is a maximal element in $V ,$ the selection of $c _ { k }$ will not change the priority of $c _ { i }$ for $i \in [ 1 , k { - } 1 ]$ . Otherwise, let $c _ { t } , t \in [ 1 , k - 1 ]$ be the first element in $C _ { I }$ which can change the priority of $c _ { k } ,$ we have $P _ { I , I } ( c _ { t } ) \geq P _ { I , t } ( c _ { t } ) > P _ { I , t } ( c _ { k } ) = P _ { I , I } ( c _ { k } ) , c _ { t } \succ c _ { k }$ in V, so that $c _ { k }$ will not be a maximal element in $V ,$ contradiction. Hence, $P _ { 2 , i } ( c _ { i } ) = P _ { I , i } ( c _ { i } )$ for $i \in [ 1 , k { - } 1 ]$ . Moreover, we have $P _ { 2 , i } ( c _ { i } ) = P _ { I , i } ( c _ { i } )$ for $i \in [ k , N ]$ . Note that $C _ { 1 }$ is a greedy sequence for $( E , V , b ) ,$ so $P _ { 2 , i } ( c _ { i } ) = P _ { I , i } ( c _ { i } ) > P _ { I , j } ( c _ { j } )$ $= P _ { I , j } ( c _ { j } ) \mathrm { f o r } i , j \in [ 1 , k \mathrm { - } 1 ] \cup [ k , N ]$ and i<j. É

LEMMA 5.3. Let $\boldsymbol { C } _ { 1 } = [ c _ { I } , c _ { 2 } . . . c _ { k - I } , c _ { k } , c _ { k + I } . . . c _ { N } ]$ be a greedy solution sequence for $( E , V , b ) , T \subseteq C _ { 1 }$ is a top-antichain in $V ,$ then $C _ { 2 }$ $= C _ { 1 } \backslash T$ is a greedy solution sequence for $( E ( T ) , V ( T ) , b ( T ) )$ .

PROOF: Through exercising Lemma 5.2 recursively. É

THEOREM 5.4. LME runs in O(D) rounds w. $\imath . p .$ , and the solution of LME is equivalent to that of centralized greedy algorithm.

PROOF. Given a MPMSP $( E , V , b ) ;$ let the solution of centralized greedy be C, the solution of LME be D, and LME runs in N rounds. Let Ri denote the selection of LME in ith round, we have $D { = } \cup _ { i = 1 } ^ { N } R _ { i }$ . Further, let $( E _ { i } , V _ { i } , b _ { i } )$ denote the reduced problem after selecting nodes set $\textstyle \bigcup _ { l = 1 } ^ { i - 1 } R _ { l } ,$ and $C _ { i }$ be greedy solution sequence for $( E _ { i } , V _ { i } , b _ { i } )$ . Apparently, $( E _ { I } , V _ { I } , b _ { I } )$ is same to (E,V,b).

Firstly, we show that $R _ { i }$ is a top-antichain in $V _ { i }$ by proving that (1) $\forall r \in R _ { i } , r$ is a maximal element of $V _ { i \mathrm { s } }$ and $( 2 ) \forall s \in V _ { i } { \mathrm { i f } } s$ is a maximal element of $V _ { i } , s \in R _ { i } .$ Since all nodes that can affect r must be in $\mathbf { A } ( r ) \cap V _ { i } ,$ and the priority of r is the highest in $\mathbf { A } ( r ) \cap V _ { i } , r$ is a maximal element in poset $( V _ { i } , \succ )$ . Also, $\forall s \in V _ { i }$ if s is a maximal element in $V _ { i \mathrm { s } }$ which means that the priority of s is the highest in $\mathbf { A } ( s ) \cap V _ { i }$ , so s will surely be selected by LME algorithm in ith round. We have $s \in R _ { i }$ .

Secondly, we show that $R _ { i } \subseteq C _ { i }$ and $C _ { i + 1 } = C _ { i } \backslash R _ { i } . \forall r \in R _ { i } ,$ for an edge which can be monitored by $r , r$ will hold the highest priority among all the vertices that can monitor the edge, so centralized greedy will definitely select r to monitor that edge, thus $r \in C _ { i } ,$ $R _ { i } \subseteq C _ { i }$ . Likewise, $R _ { i }$ is a top-antichain in $V _ { i \mathrm { s } }$ therefore, from Lemma $5 . 3$ we know $C _ { i } R _ { i }$ is a greedy solution sequence for $E _ { i } ( R _ { i } ) = E _ { i + I } ,$ , $C _ { i + 1 } { = } C _ { i } \backslash R _ { i }$ .

Thirdly, we show $D { = } C$ Since LME ends in N rounds, when LME runs in the Nth round for instance $( E _ { N } , \ V _ { N } , \ b _ { N } )$ , it is clear that $D _ { N }$ $\ b = { \cal R } _ { N } \ b = { \cal C } _ { N }$ . Hence, $C = C _ { I } = R _ { I } \cup C _ { 2 } = R _ { I } \cup R _ { 2 } \cup C _ { 3 } = \ldots = R _ { I } \cup \ldots \cup R _ { N } .$ ${ } _ { 1 } \sqcup C _ { N } = R _ { I } \sqcup \ldots \sqcup R _ { N - 1 } \sqcup D _ { N } = R _ { I } \sqcup \ldots \sqcup R _ { N - 1 } \sqcup R _ { N } = D .$ .

Finally, we show that N is at most $O ( \Delta )$ . Since $R _ { i }$ is a topantichain in $V _ { i \mathrm { s } }$ we have $\forall r _ { i + 1 } \in R _ { i + 1 } , \exists r _ { i } \in R _ { i }$ such that $r _ { i + 1 } \succ r _ { i }$ in $V _ { i \cdot }$ We say $r _ { i }$ is the tight-upper vertex of $\dot { \boldsymbol { r } } _ { i + 1 }$ . Let $\delta _ { i } ( r )$ denote the monitoring degree of r in ith round, then $\delta _ { i + I } ( r _ { i + 1 } ) \leq \delta _ { i } ( r _ { i + 1 } ) \leq \delta _ { i } ( r _ { i } )$ . If we first choose an arbitrary vertex $r _ { N } \in R _ { N }$ , then select the tight-upper vertices of $r _ { N } ,$ denoted as $r _ { N - I } .$ . Similarly, the tight-upper vertices $r _ { N \mathrm { - } }$ $2 \cdots r _ { I }$ are obtained recursively. Thus, we get the following inequation: $1 \le \delta _ { N } ( r _ { N } ) \le \ldots \le \delta _ { i } ( r _ { i } ) \le \ldots \le \delta _ { I } ( r _ { I } ) \le \Delta$ . Let the length of maximum equivalence sequence among $\delta _ { i } ( r _ { i } )$ be L, we have $N \leq \Delta L$ . If we assume that the nodes are deployed randomly, such that node IDs are distributed randomly, clearly the expectation of L is O(1). É

It is not difficult to see that Theorem 5.1 can be obtained from Theorem 5.4 since the approximation ratio of sequential greedy algorithm is $H ( \Delta )$ as shown in Theorem 4.4. Note that the bound $H ( \Delta )$ is asymptotically reachable, and such problem instances can be constructed by properly modifying the proof of Theorem 5 [28].

Liang et. al have partially observed the similar results we prove here. Their proof [29], however, has some defects, and is not strict but based on intuitive arguments. Indeed, their major statement is equivalent to our work of $R _ { i } \subseteq C _ { i } ,$ as shown in the second step of the proof for Theorem 5.4, while our method of proof is more general.

# 5.2 Local Dual-Feasible Algorithm

The LDF algorithm is different from LME in that the LME considers the solution from the monitoring nodes, while the LDF algorithm deals with the problem from the view of the monitored edges.

An important technique in LDF is the construction of the edgedependent graph. An edge-dependent graph $G _ { e }$ is derived from the problem $( E , V , b )$ , and is constructed as follows. A vertex in $\mathrm { V } ( G _ { e } )$ corresponds to an edge in E, and an edge between any two vertices in $\mathrm { V } ( G _ { e } )$ exists if the two edges in E, which corresponding to the two vertices, can be monitored by a common vertex in V.

LDF is also carried out in rounds, and each round consists of four steps. Let $( E ^ { \prime } , V ^ { \prime } , b ^ { \prime } )$ denote the reduced problem instance for the current round. First, the derived edge-dependent graph of $( E ^ { \prime } , V ^ { \prime } , b ^ { \prime } )$ is constructed. Second, calculate a maximal independent set (MIS) of the derived edge-dependent graph in a distributed manner (There is a substantial research literature on MIS construction). Note that since the vertices in derived edge-dependent graph are one-to-one with an edge in $E _ { \textrm { , } } ^ { \prime }$ a subset of $E ' _ { \ast }$ , which corresponds to the calculated MIS, can be obtained accordingly. We call such a subset maximal independent edge set (MIES) of $E ^ { \prime }$ . Third, for each edge, say $e ,$ in MIES constructed in step two, an expected number of vertices are selected among all the vertices in $V ^ { \prime }$ that are able to monitor the edge. The expected number is equal to the current monitoring number of the edge $e , b ^ { \prime } ( e )$ . Fourth, each edge in $E '$ updates its monitored degree according to the newly selected monitoring vertices in step three. At the same time, $\bar { E ^ { ; } , V ^ { \ } }$ and $b '$ are all updated accordingly. The LDF algorithm terminates when the edge set $E ^ { \prime }$ is empty.

Let $T _ { M }$ denote the maximal time of constructing an MIS in each round. We discuss the approximation ratio and time complexity of LDF algorithm as follows.

THEOREM 5.5. The LDF algorithm provides a L-approximation $f o r M P M S P i n O ( ( \Lambda ^ { + } 1 ) T _ { M } )$ times.

PROOF. The approximation ratio can be acquired from the similar proof for the set multi-cover [30]. We will mainly consider the time complexity. We only need to determine for how many round the edge-dependent graph will be empty. Let v be a vertex in the derived edge-dependent graph and its degree be d(v). We claim vertex v must be selected into one MIS within d(v)+1 round. If vertex v is not selected into MIS in a round, there must be at least a vertex neighboring to v in edge-dependent graph which will be selected into the MIS. Hence, even assuming that v is the last one being selected among all its neighbors, all neighbors of v will be selected within at most d(v) rounds, and finally v will be selected within at most d(v)+1 rounds. Obviously the maximal degree of the derived edge-dependent graph is L. Hence, LDF will ends within at most $\Lambda { + } 1$ rounds. É

It is worth noticing the difference between LME and LDF on approximation ratio and running time. When changing the problem instances, neither one will be always better than the other one about the approximation ratio and running time. When the maximum monitored degree L is small (e.g. L=2 or 3) and the maximum monitoring degree D is relatively large, the LDF with the approximation ratio L has an advantage over LME with the logarithmic ratio H(D). Whereas H(D) is often preferred rather than L for other instances. To some extent, the two algorithms complement each other in the sense of approximation ratio and running time. For example, it is not difficult to check that LDF works very well for the worst case of LME, and vice versa.

# 6. PERFORMANCE EVALUATION

We are not able to simulate the infinite large network, so the objective of our simulations and evaluations is to provide some intuitive results under a feasible range.

Throughout the simulations, we distribute the nodes in a square field, and assume each node has the same transmission radius. We generate the node locations within the field according to twodimensional uniform random distribution. Initially, for a given topology density, we create the general connectivity topology by randomly selecting some nodes from all the nodes. Topology density (TD) is defined as the average number of one node’s neighbors in the active connectivity topology. The worker ratio (WR) is defined as the ratio of the total number of nodes to the

![](images/fb27063c6f01cfef5e31d3ed6f7c9041037a8b71b2c6b9b3c3d1202a8ec9be2e.jpg)



Figure 6. Monitored degree of edges in different topology density.

![](images/1cd42cb037cd2cbebb770976a2228df62f00b98b64f3ceab8d3f6cdeda886b8b.jpg)



Figure 8. A detailed comparison of LME and LDF.

number of nodes in connectivity topology. Another important parameter is the monitoring number (MN), which is set a positive integer in the simulations. We run 100 experiments independently to obtain the simulation results as follows. By default, we set the WR to be 6.

# 6.1 Self-Monitoring Capability of Random Topology

We illustrate the self-monitoring capability through the relationship between monitored degree of edge and TD. We set the working topology size of 400 nodes and increase TD from 5 to 10. Figure 6 shows the Cumulative Distributed Function (CDF) of monitored degree of an edge. We can see that as TD increases, the corresponding topology provides more monitored degree for edges. For example, TD of 5 yields 80 percents of edges with monitored degree of 1.5 (and below), and TD of 9 yields 80 percents of edges with monitored degree of 4.0 (and below), which means for a given self-monitoring degree requirement, the higher topology density, the lower proportion of edges needs the additional patching nodes, and vice versa. This is consistent with our intuitions.

# 6.2 Comparison of LME and LDF

We compare our LME and LDF algorithms with the optimal solution and a random algorithm. The optimal solution is obtained by Matlab Binary Integer Programming tools. The random algorithm used for comparison purpose is called Random Independent Selection (RIS) algorithm. In RIS, for a given edge, the required number of nodes is selected randomly among all the surrounding nodes that can monitor the edge, and all of the edges that need to be monitored make their decisions independently and simultaneously, and add all the selected nodes into the patching monitoring set. Define patching set size as the ratio of the number of nodes in patching monitoring set size to the number of nodes in the initial connectivity topology.

![](images/54328f5f68d2282437c48bd711bc6a6b1b543f2cc54ccbf40c34484279133ab4.jpg)



Figure 7. Patching set size of different algorithm.

![](images/266929fd23b316d926a353ec311eae2760c4203f828aabed7449338f9f91d4c2.jpg)



Figure 9. Patching set size against topology density.

In Fig. 7, we simulate the CDF of set size for four algorithms when TD=8, WN=100, MN=4, WR =5. The results suggest that our LME and LDF are very close to the optimal solution in terms of patching set size. Furthermore, from Fig. 7, we can see the Optimal, LME and LDF demonstrate good threshold phenomenon. We can see that the average performance is better than the theoretical worst case greatly. At the same time, obviously, RIS is the worst and hence it is worthy and necessary to use our algorithm to select the patching monitoring nodes. We summarize the average set size and the ratio against the optimal solution in Table 1. LME and LDF yield very close set size to the optimal size, but RIS’s size is more than 3 times compared to the optimal one.

Figure 8 further illustrates the comparison of LME and LDF when changing the TD and MN. The left two lines denote the results when TD=6, MN=2, WR=5, the right two lines denote the results when TD=8, MN=4, WR=5. In both cases, LME generates better performance than LDF. According to our results, in most of circumstance, LME is superior to LDF, but not always. We change the number of deployed nodes to check the scalability ofthe algorithms. Figure 11 shows the patching set size patching set size against the number of nodes from 600 to 15000 with TD=8, MN=4 and WR=6. We can see that the results of our two algorithms keep stable when the network scale becomes large.

![](images/15b167b35929e2adda13564ce716a5875f22afc3974a595646e8f7758ad564de.jpg)



Figure 10. Patching set size against monitoring number.

![](images/b915305109698edbc2728c9cd53f0ad12cd7f09cee144c0beb24e2dd57fbdc11.jpg)



Figure 12. Rounds of LME against monitoring number.

Table 1. Patching Set Size and Ratio 

<table><tr><td></td><td>Optimal</td><td>LME</td><td>LDF</td><td>RIS</td></tr><tr><td>Patching Set size</td><td>0.6760</td><td>0.7196</td><td>0.8508</td><td>2.1110</td></tr><tr><td>Ratio</td><td>1.0000</td><td>1.0645</td><td>1.2586</td><td>3.1229</td></tr></table>

# 6.3 Impact of Topology Density and Monitoring Number

Since the self-monitoring capability of a topology change with TD as shown in Fig. 6, and the patching set size depends on the TD, we present the simulation results on the patching set size against TD. Figure 9 shows the results where TD changes from 5

![](images/397e2b2d1464904f4bee6b42541104a1f7c00ec1f522ebcaca4b008a60e7c086.jpg)



Figure 11. Patching set size against the network size.

![](images/d15754c0b161c48b7d00aa640499ec42cabfa8628676cdc7372f71db5d9120ad.jpg)



Figure 13. Rounds of LDF against monitoring number.

to 8 with MN=2,4,6, WR=6. From Fig. 9, we can see the patching set sizes of LME and LDF decrease with the increase of TD, which matches the intuition. Since higher TD means fewer edges to be monitored and the same number of nodes can monitor more edges. Further, we can observe that with the increase of TD, the gap of LME and LDF is gradually diminished, because when TD grows, the edges to be monitored decrease, and more isolated edges or small connected branches emerge, so the solution space that can be exploited for optimization shrinks accordingly. Intuitively, for these isolated edges, the results of two algorithms will be closed to each other.

Similarly, we present the patching set size against monitoring number. In Fig. 10, we can see that the output of LME and LDF almost increase linearly with monitoring number when MN≥3, but grow mildly from 1 to 2, especial for relatively higher TD= 8 and 10. This is due to that when TD=8 and 10, only a small part of edges, about 10% and less, have the monitored degree less 2, while most of the edges, about 80% and more, have the monitored degree less than and equal 4, as shown in Fig. 6.

Further, from Fig. 10, we can see that to achieve 2-selfmonitoring topology, we only need to add a small size of patching nodes, changing with topology density. It means that selftopology can be accommodated in sensor network with the modest number of extra nodes, especially when TD is relatively high.

![](images/646d8a325b72c53e44b970bf2c9b063ee30ac9381d690f9e190d863a331d6bc2.jpg)



Figure 14. Rounds of LME and LDF against network size.

# 6.4 Time Complexity

We simulate the LME and LDF in the synchronous running manner to investigate their time complexity. For the algorithm of distributed construction of MIS in LDF, we use a simply greedy method. We assign a distinct ID to each to be monitored edge, and the edge with the maximal ID first adds itself into the MIS.

As shown in Fig. 12 and 13, we can see that the running rounds of LME and LDF increase with the monitor number. This is because there are more edges need to be monitored when the monitor number increases. The performance of LME and LDF, however, is quite different from each other, especially when MN and TD increase. LME always decreases with the increase of TD, and increases with MN, while LDF increases with TD when MN is relatively large. This is because that when TD increases, the degree of vertex in derived edge-dependent graph also increases greatly. Hence, the size of MIS of the derived graph in each round will decrease. As a result, the rounds of the LDF will rise. To summary, the LME runs faster when TD is relatively lower, and LDF does better when TD is relatively higher.

In addition, we change the number of deployed nodes to check the scalability of the algorithms running times. From Fig. 14, we can see that our two algorithms both increase slow with network scale and has good scalability about times complexity.

# 6.5 More Realistic Connectivity Models

In the simulation, though the result is given in the UDG models, it is sufficient to demonstrate the necessity of optimization the selection of monitoring nodes. Notice that our algorithms are just based on the connectivity informations and work for more general graph model with theory guarantee.

# 7. DISCUSSIONS

# 7.1 Practical Applications

Since continuous monitoring of each node in the network may incur high energy cost, for energy-constrained WSNs, we may implement the self-monitoring with other energy conservation strategy such as scheduling, adaptive duty cycle, etc. Our goal to provide an underlying infrastructure for the upper layer protocols. In practical applications, we can take many manners to save the energy without the expense of the quality of self-monitoring. For example, each node in the network can schedule itself to switch into monitoring state as fixed or random periods. The nodes may also be scheduled by the upper protocols using the local monitoring function. As such, the self-monitoring capability in the network can be on demand. When the network is in a lower security alert, each node may be in monitoring state in a shorter time; while when the network has a much higher security alert or requirements, more nodes can carry out monitoring operations.

The self-monitoring topology can be tailored to cater the different requirements and offer the fundamental assurance to other techniques using local monitoring, and can be implemented flexibly in practice.

# 7.2 Interference

In the real wireless network, interference may affect the selection strategy greatly, because collisions in the wireless channel can cause a high error rate for overhearing. If two links transmit data in the same time, the node that monitors the two links may overhear nothing due to the interference. Nevertheless, this does not affect our algorithms. There are several methods to deal with this situation. For example, we can evaluate and calculate and the interference level of candidate nodes, and restrict that a node with higher interference level being excluded during the preprocess stages for construction of self-monitoring topology. Only the nodes with a lower interference level are considered as candidates.

Indeed, interference has the stochastic feature and the level could be changed over time. If a node potentially suffers interference in some time slots, it still can monitor the links in other time slots.

# 7.3 Security

Security is another hinged issue for practical applications. The selection of patching monitoring nodes should be able to withstand a hostile attack against itself. We notice that we cannot eliminate the possibility of selecting malicious nodes, but we can manage to have the malicious nodes without higher possibility to become a patching monitoring node. The key problem is to validate the monitoring degree of a node which itself claims to have. This can be disposed by some cryptographic mechanisms, for example, authenticate the neighbor relation of a node.

# 7.4 Dynamic Maintenance

We assume that the active nodes in the network topology keep unchanged in most of the time. Certainly, after the generation of a topology, the active working topology might be subject to change due to node failures, etc. Our self-monitoring topology can also be updated correspondingly. If there is no major topology change, no update needs to be launched until some preset timer expires. On the other hand, for some major topology changes, an on-demand update can be performed. Notice that since our algorithms are completely distributed, the update process can be performed only in a local area where the change occurs.

# 7.5 Bounds for Approximation Algorithm

If additional information, such as location, power, etc, are available, more efficient heuristic algorithms for node selection can be obtained. An interesting question is that how to design constant-factor approximation algorithm for the MPMSP without using node location information. Our two algorithms set a good tradeoff between the performance (the theoretic bound of approximation algorithm) and the complexity of implementation (simple to run).

# 8. CONCLUSIONS

We address the issue of the optimal topology integrated with self-monitoring capability to meet the local monitoring requirements. We present a formal study on the problem of adding the minimum number of monitoring nodes into a large scale sensor network, and show that the problem is NP-complete. We also provide the upper bounds on the approximation ratio in a centralized scenario. We further design two distributed algorithms with provable approximation ratio and time complexity guarantee. Through comprehensive simulations, we present the performance comparison of our distributed algorithms and show that the optimized selection of monitoring nodes can decrease the number of monitoring nodes significantly.

Future work will involve the followings. First is to design secure node selection protocols to prevent malicious nodes from joining set of patching monitoring nodes and colluding. Second, we will investigate how real radio models can affect the selection strategy of monitoring nodes.

# 9. ACKNOWLEDGMENTS

This work is supported in part by the National Basic Research Program of China (973 Program) under grant No. 2006CB303000, the National High Technology Research and Development Program of China (863 Program) under grant No.2007AA01Z177 and 2007AA01Z180, NSFC Key Project grants No. 60533110 and 60736016, the Hong Kong RGC grant HKUST6169/07E, HKUST Nansha Research Fund NRC06/07.EG01, and Nokia APAC research grant.

# 10. REFERENCES

[1] A. Perrig, "SPINS: security protocols for sensor networks," In Proc. of ACM MobiCom, 2001.   
[2] C. Karlof and D. Wagner, "Secure routing in wireless sensor networks: attacks and countermeasures," Elsevier AdHoc Networks, vol. 1, 2003.   
[3] H. Chan and A. Perrig, "Security and privacy in sensor networks," in IEEE Computer, vol. 36, 2003, pp. 103-105.   
[4] I. Khalil, S. Bagchi, and C. Nina-Rotaru, "DICAS: detection, diagnosis and isolation of control attacks in sensor networks," In Proc. of IEEE SecureComm, 2005.   
[5] I. Khalil, S. Bagchi, and N. Shroff, "LITEWORP: a lightweight countermeasure for the wormhole attack in multihop wireless networks," In Proc. of IEEE/IFIP DSN, 2005.   
[6] S. Ganeriwal and M. B. Srivastava, "Reputation-based framework for high integrity sensor networks," In Proc. of ACM SASN, 2004.   
[7] S.-B. Lee and Y.-H. Choi, "A resilient packet-forwarding scheme against maliciously packet-dropping nodes in sensor networks," In Proc. of ACM SASN, 2006.   
[8] A. Silva, M. Martins, B. Rocha, A. Loureiro, L. Ruiz, and H. Wong, "Decentralized intrusion detection in wireless sensor networks," In Proc. of ACM IWQoS, 2005.   
[9] K. Ioannis, T. Dimitriou, and F. C. Freiling, "Towards intrusion detection in wireless sensor networks," In Proc. of the 13th European Wireless Conference, 2007.   
[10] S. Marti, T. J. Giuli, K. Lai, and M. Baker, "Mitigating routing misbehavior in mobile ad hoc networks," In Proc. of ACM MobiCom, 2000.

[11] S. Buchegger and J.-Y. L. Boudec, "Performance analysis of the CONFIDANT protocol: cooperation of nodes fairness in distributed ad-hoc networks," In Proc. of ACM MobiHoc, 2002.   
[12] Y. Huang and W. Lee, "A cooperative intrusion detection system for ad hoc networks," In Proc. of ACM SASN, 2003.   
[13] P. Michiardi and R. Molva, "CORE: a collaborativereputation mechanism to enforce node cooperation in mobile ad hoc networks," In Proc. of the IFIP Sixth Joint Working Conference on Communications and Multimedia Security, 2002.   
[14] W. R. Heinzelman, A. Chandrakasan, and H. Balakrishnan, "Energy-efficient communication protocol for wireless microsensor networks," In Proc. of the 33rd Hawaii International Conference on System Sciences, 2000.   
[15]B. Chen, K. Jamieson, H. Balakrishnan, and R. Morris, "Span: An energy-efficient coordination algorithm for topology maintenance in ad hoc wireless networks," In Proc. of ACM MobiCom, 2001.   
[16] C. Schurgers, V. Tsiatsis, S. Ganeriwal, and M. Srivastava, "Topology management for sensor networks: exploiting latency and density," In Proc. of ACM MobiHoc, 2002.   
[17] I. Khalil, S. Bagchi, and N. B. Shroff, "SLAM: sleep-wake aware local monitoring in sensor networks," In Proc. of IEEE/IFIP DSN, 2007.   
[18] C. Hsin and M. Liu, "Self-monitoring of wireless sensor networks," Elsevier Computer Communications, vol. 29, pp. 462-476, 2006.   
[19] F. Kuhn, R. Wattenhofer, and A. Zollinger, "AdHoc networks beyond unit disk graphs," In Proc. of ACM DIALM-POMC, 2003.   
[20] B. N. Clark, C. J. Colbourn, and D. S. Johnson, "Unit disk graphs," Discrete Mathematics, vol. 86, pp. 165-177, 1990.   
[21] M. R. Garey and D. S. Johnson, "The rectilinear Steiner tree problem is NP-complete," SIAM Journal on Applied Mathematics, vol. 32, pp. 826-834, 1977.   
[22] R. Tamassia and I. G. Tollis, "Planar grid embedding in linear time," IEEE Transactions on Circuits and Systems, vol. 36, pp. 1230-1234, 1989.   
[23] L. G. Valiant, "Universality considerations in VLSI circuits," IEEE Transaction on Computers, vol. C-30, pp. 135-140, 1981.   
[24] S. Schmid and R.Wattenhofer, "Algorithmic models for sensor networks," In Proc. of the 14th International Workshop on Parallel and Distributed Real-Time Systems, 2006.   
[25] A. Schrijver, Combinatorial optimization - polyhedra and efficiency (Part III): Spring, 2003.   
[26] D. S. Hochbaum, Approximation algorithms for NP-hard problems (Chapter 3, page:100-102): PWS Publishing Company, 1997.   
[27] D. S. Hochbaum and W. Maass, "Approximation schemes for covering and packing problems," Journal of the ACM, vol. 32, pp. 130-136, 1985.   
[28] P.-J. Wan, K. M. Alzoubi, and O. Frieder, "Distributed construction of connected dominating set in wireless ad Hoc networks," In Proc. of IEEE INFOCOM, 2002.   
[29] B. Liang and Z. J. Haas, "Virtual backbone generation and maintenance in ad hoc network mobility management," In Proc. of IEEE INFOCOM, 2000.   
[30] D. S. Hochbaum, Approximation algorithms for NP-hard problems (Chapter 3, page:109-111): PWS Publishing Company, 1997.