# Edge Self-Monitoring for Wireless Sensor Networks

Dezun Dong, Student Member, IEEE Computer Society, Xiangke Liao, Yunhao Liu, Senior Member, IEEE Computer Society, Changxiang Shen, and Xinbing Wang, Member, IEEE Computer Society

Abstract—Local monitoring is an effective mechanism for the security of wireless sensor networks (WSNs). Existing schemes assume the existence of sufficient number of active nodes to carry out monitoring operations. Such an assumption, however, is often difficult for a large-scale sensor network. In this work, we focus on designing an efficient scheme integrated with good self-monitoring capability as well as providing an infrastructure for various security protocols using local monitoring. To the best of our knowledge, we are the first to present the formal study on optimizing network topology for edge self-monitoring in WSNs. We show that the problem is NP-complete even under the unit disk graph (UDG) model and give the upper bound on the approximation ratio in various graph models. We provide polynomial-time approximation scheme (PTAS) algorithms for the problem in some specific graphs, for example, the monitoring-setbounded graph. We further design two distributed polynomial algorithms with provable approximation ratio. Through comprehensive simulations, we evaluate the effectiveness of our design.

Index Terms—Sensor networks, self-monitoring, security, NP-complete.

# 1 INTRODUCTION

WIRELESS sensor networks (WSNs) are emerging as apromising platform for many important applications promising platform for many important applications such as military surveillance, homeland security, emergency response, forest fire monitoring, etc. Security is crucial for mission-critical applications, which work in unattended and even hostile environment. One of the most severe security threats in sensor networks is node compromise. Once some nodes are compromised, the attackers can use them to mount a variety of attacks. It is rather challenging to provide effective security mechanisms against compromised nodes in resource-limited WSNs [1], [2].

Based on local monitoring (or watchdog) technique [3], [4], [5], [6], many approaches have been proposed to protect sensor networks in face of compromised nodes. The basic idea of local monitoring is illustrated in Fig. 1. The dashed circle denotes the transmission range of a node. Nodes M1 and M2 monitor the link from S to R, as they are able to monitor the traffic that R receives from S and forwards out. By analyzing traffic flows, monitoring nodes are able to detect malicious behaviors, such as delaying, dropping, modifying, or fabricating packets, etc. To meet the requirements, we sometimes require multiple nodes to conduct

D. Dong and X. Liao are with the School of Computer, National University of Defense Technology, Changsha, Hunan 410073, P.R. China. E-mail: dezundong@gmail.com, xkliao@nudt.edu.cn.   
. Y. Liu is with the TNLIST, School of Software, Tsinghua University, Beijing, P.R. China. E-mail: yunhao@greenorbs.com.   
. C. Shen is with the Naval Institute of Computing Technology, Beijing, P.R. China. E-mail: shenchx@cae.cn.   
. X. Wang is with the Department of Electronic Engineering, Shanghai Jiaotong University, Shanghai, P.R. China. E-mail: xwang8@sjtu.edu.cn.

Manuscript received 26 June 2008; revised 19 June 2009; accepted 18 Sept. 2009; published online 2 Apr. 2010.

Recommended for acceptance by M. Singhal.

For information on obtaining reprints of this article, please send e-mail to: tpds@computer.org, and reference IEEECS Log Number TPDS-2008-06-0243. Digital Object Identifier no. 10.1109/TPDS.2010.72.

monitoring. In the local monitoring scheme, a number of nodes are employed for watching the specific area in the network. These monitoring nodes are normal nodes and can perform basic operations of communication and sensing in addition to monitoring.

In WSNs, local monitoring exploits the convenience of overhearing due to the broadcast nature in wireless communication and dense deployment of large-scale systems. On the other hand, as a promising security mechanism as well as an effective complement for cryptographic mechanisms, however, local monitoring also incurs extra energy cost since it requires monitoring nodes to keep active and oversee network behaviors. Hence, to employ as few nodes as possible is highly desirable.

Previous schemes often assume the existence of sufficient nodes to carry out the monitoring function. Such a requirement is practically difficult. Consider the edge selfmonitoring problem by a simple example shown in Fig. 2. The dots and solid lines denote the active sensor nodes and communication links between them. The circles and dot lines denote the sleeping nodes and potential communication links between sleeping and active nodes. Suppose we require every communication link be monitored by at least three nodes except for the end nodes of the link. The requirement cannot be satisfied in current active network, since there are not enough (three) active nodes neighboring to these links. Hence, additional sleeping nodes have to be activated. Fig. 2a shows the results of a random selection. Three additional nodes, labeled with boxes, are activated to meet the requirement. If we adopt an optimal strategy, only one node is needed, as shown in Fig. 2b.

The requirement for optimized local monitoring is indeed motivated by the needs of our ongoing project, including GreenOrbs and OceanSense [7]. Due to the unattended nature of these systems, they are prone to many faults, safety, and security problems, as well as disturbances from natural environments, incidental, or deliberate damages from intruders, etc. Hence, we desire to design some regular and lightweight mechanisms to online monitor and diagnose the network problems. Optimized local monitoring scheme provides a possible choice to gather and analyze network traffic, as well as building selfdiagnosis and self-monitoring mechanisms while maximizing the network lifetime. Local monitoring scheme can be potentially integrated into our network diagnosis system [7] and auxiliarily provide a distributed manner to label, monitor, and parse the traffic.

![](images/2c738012dddeb67fd54f16509536bfd067346aed54f16471c929fa0937c2ded3.jpg)



Fig. 1. Local monitoring.

In this paper, we focus on the fundamental issue of designing an edge self-monitoring topology, where every transmission link can be monitored by nodes within the network. We show that finding an optimal edge selfmonitoring topology is NP-complete even by modeling the communication network as a unit disk graph (UDG) with a geometric representation. We provide the approximability results in centralized scenario and prove the existence of polynomial-time approximation scheme (PTAS) for this problem when restricted in some specific graphs.

We propose two distributed approximation algorithms with provable approximation ratio and time complexity guarantee for large-scale sensor networks. Moreover, we conduct extensive simulations to examine the effectiveness of this design.

The rest of the paper is organized as follows: Related work is presented in Section 2, and problem definition is given in Section 3. Hardness of the problem and approximability results are presented in Section 4. Distributed algorithms are presented in Section 5. Performance evaluation is presented in Section 6. We have some discussions in Section 7, and conclude this work in Section 8.

# 2 RELATED WORK

WSNs are vulnerable to a wide range of security attacks such as wormhole, black hole, spoofed, altered, replayed routing information, selective forwarding, Sybil attack, DoS, etc. [8]. There have been many proposals using cryptography to ensure secure communications. See [9] for more references.

Cryptography provides an efficient mechanism to achieve data confidentiality, integrity, node authentication, and secure routing. Nevertheless, cryptography alone is not sufficient for node compromise attacks and unanticipated misbehaviors in sensor networks [6]. Researchers, therefore, attempt to use noncryptographic techniques to solve the problems beyond the capability of cryptographic approaches [3], [4], [5], [6].

The idea of watchdog or local monitoring is first introduced by Marti et al. in ad hoc networks for detecting mischievous nodes [10]. Since then extensive efforts have been made in ad hoc and sensor networks. For secure routing, a lightweight protocol called DICAS is proposed by Khalil et al. [3], which mitigates the control and data traffic attacks in sensor networks with the help of local monitoring. Khalil et al. also design a countermeasure for wormhole attacks, called LITEWORP [4], which uses guard nodes to attest the source of each transmission. Neighbor watch [5] is employed by a hop-by-hop resilient packet-forwarding scheme. For reputation and trust-based systems, neighbor watch is employed to monitor neighborhoods and collect information to build trust relationships among nodes in the network, such as RFSN [6], CONFIDANT [11], etc.

![](images/833e0450f8ab8a1dd78cbdb82948dcd56905f7abf0b49221b5443f591573900b.jpg)



(a)

![](images/9e0de4888879a4f07143dd16425b6e0bd5a12943946c9b03c9a1fdb6bc30181b.jpg)



(b)   
Fig. 2. Comparison of random and optimal selections. (a) Random selection. (b) Optimal selection.

Local monitoring scheme places new requirement to a sensor connectivity topology. Generally, building and maintaining connectivity topology are the main task of topology control techniques, and their goal is to achieve energy-efficient communication. Topology control schemes aim at extending network lifetime, enhancing network utilization and capacity, minimizing interference, reducing high end-to-end packet delays, and increasing the robustness to node failures. They do not construct and optimize topologies with local monitoring properties.

Recently, Khalil et al. [12] propose an on-demand sleepwake protocol, called SLAM, to shorten the time a node needs to be awake for the purpose of monitoring. They do not, however, consider the optimized selection of monitoring nodes in the network, but focusing on how to schedule nodes to meet the monitoring requirement for given communication links. Hence, SLAM focuses on shortening the monitoring time of a guard node, while our work considers reducing the number of nodes. This work and SLAM optimize the local monitoring scheme in two different aspects, and are complementary to each other.

Other interesting issues related to this work in sensor networks include node self-monitoring [13] and self-protection [14], [15]. The node self-monitoring mechanism proposed by Hsin and Liu [13] focuses on the system-level fault diagnosis of a network, especially detecting node failures to reveal inside events, e.g., malfunctioning, energy depletion, etc., or external events like fires, intrusion destructions, etc. Self-protection problem uses nodes to provide protection to nodes themselves (both sleep and active nodes) so as to resist the attacks. Hence, the node self-monitoring and selfprotection both focus on using nodes to monitor nodes, which is different with local monitoring scheme using nodes to monitor links. They do not deal with misbehaviors related with communication links as what are considered in the local monitoring scheme [3], [4], [5].

# 3 SELF-MONITORING PROBLEM

We consider static sensor networks in which all communication links are bidirectional. We define the communication graph on the network as a directed graph $\boldsymbol { G } _ { c } ,$ where sensors are represented by vertices. A pair of opposite directed edges $< u , v >$ and $< v , u >$ exists if there is a direct communication channel between node u and v. We define the active network created and scheduled by topology control algorithm as active working topology, which is a subgraph of communication graph $G _ { c }$ . In the rest of the paper, we use EðGÞ and VðGÞ to denote the edge and vertex set of a graph G, respectively. Node/vertex, as well as link/ edge, will be used interchangeably. It is important to note that the assumption about the bidirectional communication links is for convenient presentation of the algorithm. Indeed, all definitions and theorems in the paper are still applicable when the communication links are directional.

Definition 3.1. Given a directed edge $e = < v _ { 1 } , v _ { 2 } > \in E ( G _ { c } )$ , $v \in V ( G _ { c } ) \backslash v _ { 1 } , \ i f \ < v _ { 1 } , v > , < v _ { 2 } , v > \in E ( G _ { c } )$ , we say that v can monitor edge e. Given an edge set $E \subseteq E ( G _ { c } )$ , a vertex set $V \subseteq V ( G _ { c } ) , \bar { k } \in \mathbb { N }$ , if any edge e in E can be monitored by at least k different vertices in V, we say that V can k-monitor the edge set E.

Definition 3.2. Given a graph $G \subseteq G _ { c }$ and an edge set （4号 $E \subseteq E ( G )$ , let $b \in \mathbb { Z } _ { 0 , + } ^ { E }$ , if for any $e \in E ,$ , there are b(e) different vertices in V(G) that can monitor e, we say that G has the b-self-monitoring capability about edge set E. Further, if given $k \in \mathbb { N } ,$ , for any ${ \dot { e } } \in E , b ( e ) \geq k ,$ we say that G has the kself-monitoring capability about edge set E.

The construction of connectivity topology of WSNs is usually optimized for multiple objectives, such as required connectivity and coverage [16], more specific [17] and application-oriented requirements, etc. Self-monitoring capability is a new requirement for connectivity topology, for which we need to integrate the self-monitoring subobjective with previous ones. To have our algorithm generally applicable, we treat self-monitoring as an independent function module, that is, we study how to convert a general connectivity topology into a topology with self-monitoring capability at the lowest cost. We formalize the transition as follows:

Definition 3.3 (Minimum Self-Monitoring Topology Problem (MSMTP)). Given $G _ { c } , G _ { 0 } \subseteq G _ { c } , k \in \mathbb { N } ,$ , finding a subgraph $G _ { 1 } \subseteq G _ { c } ,$ such that $G _ { 0 } \subseteq G _ { 1 } , V ( G _ { 1 } )$ can k-monitor $\operatorname { E } ( G _ { 0 } )$ and $| \mathrm { V } ( G _ { 1 } ) |$ is minimized.

It is worth noting that in Definition $3 . 3 , \mathrm { V } \left( G _ { 1 } \right)$ is requested to k-monitor $\operatorname { E } ( G _ { 0 } )$ instead of $\operatorname { E } ( G _ { 1 } )$ . This is because in the local monitoring scheme, communication links in $G _ { 0 }$ are the targets to be monitored and protected. There are (almost) no communications between guard and working nodes; thus, links between those nodes are not targets.

Fig. 3a shows an example of MSMTP. Dots and circles represent active and sleep nodes in the network, respectively. Lines denote active edges that need to be monitored. Each edge has its own monitored degree in the current network according to Definition 3.1. For example, edge $( a , b )$ can be monitored by c; thus, current network has 1-self-monitoring capability on edge $( a , b )$ . The numbers in Fig. 3a show monitored degree of all the edges. Suppose our requirement is to achieve k-self-monitoring $\left( k = 3 \right)$ on all the edges in Fig. 3a. Note that the objective of MSMTP is to minimize the total number of activated nodes while providing 3-selfmonitoring capability. Clearly, additional sleep nodes have to be scheduled, as shown in Fig. 3b, where the numbers describe the gap from the current monitoring capability to 3- self-monitoring for all the edges. Thus, MSMTP is equivalent to activating minimum number of sleep nodes to let all the edges to be 3-monitored. Hence, Definition 3.3 can be transformed into Definition 3.4, where parameter b is the gap of monitoring capability.

![](images/e3a8c0c74e3f983546d1ee48b7374b67305b1dcc0e94dab2a7bb965b46aa5565.jpg)



(a)

![](images/550dd961e7ba07da2ebc471533d2fc152dfa217f3bb962068535e2785ec8cbd5.jpg)



(b)   
Fig. 3. Transform from MSMTP to MPMSP. (a) Self-monitoring capability. (b) Monitoring requirement gap to 3 edge self-monitoring.

Definition 3.4 (Minimum Patching Monitoring Set Problem (MPMSP)). Given $G _ { c }$ and G, an edge set $E _ { p } \subseteq \operatorname { E } ( G )$ which denotes the edges that cannot be k-monitored in $G ,$ let $b \in \mathbb { N } ^ { E _ { p } }$ be the monitoring requirement gap for $E _ { p } ,$ then $V _ { p }$ denote $\mathrm { V } ( G _ { c } ) \backslash \mathrm { V } ( G )$ , finding a subset of vertices $V \subseteq V _ { p }$ such that V can b-monitor $E _ { p }$ and jV j is minimized.

The MPMSP can be extended to the case that each vertex has a nonnegative weight, where the constraints for the feasibility of a solution remain the same, and the objective function is altered to the weighted sum of the patching vertices instead of the cardinality of patching set. We call the vertex-weighted MPMSP as Weighted Minimum Patching Monitoring Set Problem (WMPMSP). In later discussions, we let $\bar { W } _ { p }$ denote the vertex weight function on $V _ { p } .$ . Note that in Definition 3.1, node $v _ { 1 }$ is not considered as the monitoring node for the directed edge $< v _ { 1 } , v _ { 2 } >$ . If we modify the definition to allow $v _ { 1 }$ monitor edge $< v _ { 1 } , v _ { 2 } > ,$ the self-monitoring capability of each link is increased by one in a bidirectional network. Such difference does not affect the definition of MPMSP.

# 4 PROBLEM HARDNESS AND APPROXIMATION

In this section, we first prove that the MPMSP problem is NPcomplete even the communication graph is restricted to be UDG with a geometric representation. We present the bounds on approximation ratio for MPMSP in various graph models. We also discuss some extended results about WMPMSP.

![](images/43a1f95a3c86baebba292321adb6cc4ef9da89705ffed7eac95ceb0cec77c228.jpg)



Fig. 4. Locally redraw a grid unit.

# 4.1 Problem Hardness

The hardness of MPMSP largely depends on the graph model for representing communication topology of a sensor network. Among those models, UDG is probably the simplest one [18]. Our discussion will start from proving that MPMSP is NP-complete in UDG with a geometric representation, and we then extend it to generalized models.

We use the proximity model to define UDG, that is, points in the plane form a UDG with a vertex corresponding to a point, and an edge between two vertices exists if and only if the euclidean distance between the two points is at most a constant bound C. Before presenting the proof, related definitions and notations are listed as follows:

Definition 4.1. Given $( G _ { c } , G , E _ { p } , V _ { p } , b )$ of an MPMSP, we define the monitoring degree of a vertex v in $V _ { p }$ as the number of edges in $E _ { p }$ that can be v monitored, denoted by $\delta ( v ) ,$ ; the monitored degree of an edge e in $E _ { p }$ is defined as the number of vertices in $V _ { p }$ that can monitor $e ,$ denoted by $\lambda ( e ) ;$ and we denote the maximum monitoring degree as $\Delta = m a x \{ \delta ( v ) , v \in V _ { p } \}$ , and maximum monitored degree as $\Lambda = m a x \{ \lambda ( e ) , e \in E _ { p } \}$ .

Theorem 4.1. When $\Delta \geq 3$ , MPMSP is NP-complete in UDG with a geometric representation.

Proof. It is sufficient to show that MPMSP is NP-complete if we prove that when the monitoring requirement number b is specialized to a constant $k \geq \bar { 2 } .$ , the problem is NPcomplete. We write such a specialized MPMSP as a k MPMSP. Clearly, kMPMSP belongs to NP, as the solution certificate can be verified in polynomial time. The NPhardness is proved by a reduction from the well-known NP-complete vertex cover in planar graph with maximum degree 3. We will present a polynomial-time transformation that takes an arbitrary planar graph $G _ { a }$ of maximum degree 3 and constructs a $\mathrm { \bar { \it k M P M S P } } \left( \hat { G } _ { c } , G , E _ { p } , \right.$ $V _ { p } , ~ k )$ in UDG with a geometric representation and $\Delta \geq 3$ . Moreover, knowing minimum patching monitoring set of $\left( G _ { c } , \ G , \ E _ { p } , \ V _ { p } , \ k \right)$ , we are able to compute minimum vertex cover of $G _ { a }$ in polynomial time. The key issue for the construction of UDG $G _ { c }$ is the proper selection of points set and the unit distance ${ \dot { C } } .$ The construction is carried out in two steps.

Step 1. We first draw $G _ { a }$ in the plane by using a planar orthogonal grid embedding algorithm [19]. The embedding maps 1) vertices to distinct grid points and 2) edges to nonintersecting grid paths. All vertices and bends are located on integer grid points. Such a construction does exist and can be finished in polynomial time $O ( | \mathrm { V } ( G _ { a } ) | )$ [19]. Second, we enlarge the scale of the grid to make the unit length of grid to be $2 m + 1 \geq 9$ . Thus, the length $| e _ { i } |$ of any edge $e _ { i }$ in $\operatorname { E } ( G _ { a } )$ is a multiple of $2 m + 1$ . Third, if $| e _ { i } |$ is even, we select a segment of unit grid in $e _ { i }$ and redraw it locally to make jeij be an odd by incrementing one, as illustrated in Fig. 4. We delete the segment $( i _ { m - 1 } , i _ { m + 1 } )$ of length 2 in one grid unit and reconnect $i _ { m }$ 1

![](images/8a3140d91eadfc3614b126308477163bdddbccf0144c441714a474c149a67f2e.jpg)



Fig. 5. Gadget W.

and $i _ { m + 1 }$ by three segments of length 1, $( i _ { m - 1 } , i _ { m , a } ) ,$ , $( i _ { m , a } , i _ { m , b } ) .$ , and $( i _ { m , b } , i _ { m + 1 } )$ , and then, insert all the vertices of $G _ { a }$ to G and $G _ { c } .$

Step 2. For an edge $e _ { i }$ in $\operatorname { E } ( G _ { a } ) .$ , we place a number $L = | e _ { i } | - 1$ of vertices on $e _ { i }$ by making the interspaces of two adjacent vertices be equal to 1, and denote them as $v _ { i , l } , l \in [ 1 , L ]$ . We add all these vertices into G and $G _ { c } .$ . Since jeij is odd, $| e _ { i } | - 1$ is even. Let $v _ { i , 0 }$ and $v _ { i , L + 1 }$ denote the endpoints of $e _ { i } .$ Now, for each vertex $v _ { i , l }$ in $G , l \in [ 1 , \bar { L } ]$ , we add a vertex $u _ { i , l }$ such that $d ( v _ { i , l } , u _ { i , l } ) < R ,$ where R is a constant. We add all these vertices $u _ { i , l }$ to $G _ { c } .$ . If we set $R = 0 . 1$ and $C = 1 . 1 .$ , it is straightforward to verify that the following inequations are satisfied:

1.

$$
\forall e _ {i} \in \mathrm{E} (G _ {a}), l \in [ 1, L ],
$$

$$
d \left(u _ {i, l}, v _ {i, l - 1}\right), d \left(u _ {i, l}, v _ {i, l}\right), d \left(u _ {i, l}, v _ {i, l + 1}\right) <   C,
$$

$$
d (v _ {i, l}, v _ {i, l - 1}), d (v _ {i, l}, v _ {i, l + 1}) <   C.
$$

2.

$$
\forall e _ {i} \in \mathrm{E} (G _ {a}), l \in [ 1, L ],
$$

$$
\forall v \in \mathrm{V} (G) \backslash \left\{v _ {i, l - 1}, v _ {i, l}, v _ {i, l + 1}, u _ {i, l} \right\} d \left(u _ {i, l}, v\right) > C.
$$

3.

$$
\forall e _ {i} \in \mathrm{E} (G _ {a}), l \in [ 1, L ],
$$

$$
\forall v \in V (G) \backslash \{v _ {i, l - 1}, v _ {i}, v _ {i, l + 1} \} d (v _ {i, l}, v) > C.
$$

Step 3. We first construct a gadget $W ,$ as shown in Fig. 5, where the lines denote the connection relationship. Let VW be the vertex sequence $\left[ x _ { 1 } , x _ { 2 } , y _ { 1 } , y _ { 2 } , m _ { 1 } , \ldots , m _ { \mathrm { k } } \right]$ . For each edge in $G ,$ say $( v _ { i , l } , v _ { i , l + 1 } ) ,$ we place vertices $m _ { i , l , 1 } , \ldots ,$ ; $m _ { i , l , \mathrm { k } } , y _ { i , l , 1 } , y _ { i , l , 2 }$ close to the edge. Let $S _ { i }$ be the node sequence $[ v _ { i , l } , v _ { i , l + 1 } , y _ { i , l , 1 } , y _ { i , l , 2 } , m _ { i , l , 1 } , \dots , m _ { i , l , \mathrm { k } } ]$ or $[ v _ { i , l + 1 } , v _ { i , l }$ ; $y _ { i , l , 1 } , y _ { i , l , 2 } , m _ { i , l , 1 } , . . . , m _ { i , l , \mathrm { k } } ]$ . We adjust the location of those vertices properly such that the vertex set $S _ { i }$ sequentially corresponds to $V _ { W } .$ , and the subgraph induced by vertex set $S _ { i }$ is isomorphic to gadget $W$ if neglecting edges set $\{ ( m _ { i , l , r } , m _ { i , l , s } ) | r , s \in [ 1 , k ] \}$ .

Note that each $m _ { i } , i \in [ 2 , k ]$ , is connected to $x _ { 1 } , x _ { 2 } , y _ { 1 } ,$ , and $y _ { 2 } ,$ , but not all the lines are drawn for concision. We restrict that only one of the two vertices, $v _ { i , l }$ and $v _ { i , l + 1 } ,$ to be qualified for mapping to $x _ { 2 }$ in $W ,$ , and write it as $x _ { i , l , 2 }$ and the other as $x _ { i , l , 1 }$ . We insert all the vertices into $\boldsymbol { G } _ { c } ,$ , while only insert yi;l;1 and $y _ { i , l , 2 }$ into G. Also, we constrain that the edge $\left( y _ { i , l , 1 } , y _ { i , l , 2 } \right)$ is only able to form a triangle with vertices $m _ { i , l , 1 } , \ldots , m _ { i , l , \mathrm { k } }$ among all vertices in $\boldsymbol { G } _ { c } ,$ and $m _ { i , l , 1 } , \ldots , m _ { i , l , k }$ is only able to form a triangle with edges $( x _ { i , l , 1 } , x _ { i , l , 2 } ) , ( x _ { i , l , 2 } , y _ { i , l , 1 } )$ , and $\left( { { y } _ { i , l , 1 } } , { { y } _ { i , l , 2 } } \right)$ among all edges in G. Clearly, all the constraints can be achieved by properly adjusting the positions of new added vertices when setting the parameter values R and C as in step 2.

So far, we have finished the polynomial transformation. Moreover, our constructed graph $G _ { c }$ and G are both connected UDG with the geometric representation, and G is a subgraph of $G _ { c } .$ . We can check that G has the 0-selfmonitoring capability about any edge in $\operatorname { E } ( G )$ . To make G have the k-self-monitoring capability about $E _ { p } = \operatorname { E } ( G ) ,$ , we can set $V _ { p } = \mathrm { V } ( G _ { c } ) \backslash \mathrm { V } ( \dot { \mathrm { G } } )$ . Thus, we obtain the constructed k MPMSP instance $( G _ { c } , G , E _ { p } , V _ { p } , k )$ , where the maximum monitoring degree $\Delta$ is 3. It is easy to verify that $G _ { a }$ has a vertex cover set of size N if and only if $( \dot { G _ { c } } , G , E _ { p } , V _ { p } , k )$ has a patching monitoring set of size $M = N + \bar { \Sigma } _ { e _ { i } \in E ( G _ { a } ) } ( k + 1 / 2 ) ( | e _ { i } | - 1 )$ . tu

Corollary 4.2. When $\Delta \geq 3 ,$ , WMPMSP is NP-complete in UDG with a geometric representation.

The UDG model is idealistic. Some researchers have proposed other relaxed models for sensor network, such as quasi-UDG, growth-bounded graph, and general graph [18]. We call those graphs extended UDG since UDG is a subgraph of them.

Corollary 4.3. When $\Delta \geq 3 ,$ MPMSP and WMPMSP are NPcomplete in extended UDG.

Theorem 4.4. When $\Delta \le 2 _ { \cdot }$ , WMPMSP is polynomial-time solvable in general graph.

Proof. When $\Delta \leq 2 ,$ WMPMSP can be formalized as the simple b-edge covers in multigraph, which is polynomialtime solvable [20]. Given WMPMSP $( G _ { c } , G , \mathbf { \hat { E } } _ { p } , \mathbf { \hat { V } } _ { p } , b , W _ { p } )$ where $W _ { p }$ denotes the vertex weight function on $V _ { p } ,$ the procedures of constructing edge-weighted multigraph $G _ { m }$ are as follows: An edge $\bar { e } \in \bar { E _ { p } }$ corresponds to a vertex $v _ { e } \in V ( G _ { m } )$ . If a vertex $v \in V _ { p }$ can monitor only one edge $e \in E _ { p . }$ , we add a distinct loop to $v _ { e } \in \mathrm { V } ( \mathrm { G } _ { \mathrm { m } } )$ . If a vertex $y \in V _ { p }$ can monitor both edge $f , g \in E _ { p } ,$ we also add a distinct edge $( v _ { f } , v _ { g } ) _ { y }$ to $G _ { m }$ . Each edge in $G _ { m }$ derives its weight from that of corresponding vertex. tu

Corollary 4.5. When $\Delta \le 2 ,$ , MPMSP is polynomial-time solvable in general graph.

From the above theorems, we can see that $\Delta = 3$ is the tight threshold to distinguish the complexity of MPMSP, since MPMSP is NP-complete even in the simplest graph model for $\Delta \geq 3 ,$ , while the weighted MPMSP keeps to be polynomial-time solvable in general graph when $\bar { \Delta } \leq 2$ .

# 4.2 PTAS in UDG with Representation

In this section, we design a shifting strategy [21] to approximate MPMSP in UDG with a geometric representation. The algorithm provides a PTAS and its main procedures are presented in Algorithm 1.

Algorithm 1. PTAS for MPMSP (with representation)

Input: MPMSP $( G _ { c } , G , E _ { p } , V _ { p } , b )$ , geometric representation of UDG $G _ { c }$ in region $R , \varepsilon > 0$ .

Output: ð1 þ "Þ-approx. minimum patching monitoring set H.

1: Compute minimum even $m \in \mathbb { N }$ such that $( 1 2 / m ) \leq \varepsilon ;$

2: $H = \varnothing ;$

3: for $i : = 2$ to m and i is even, do

4: for $j : = 2$ to m and j is even, do

5: Partition R along the $\lceil m / 2 \rceil \times \lceil m / 2 \rceil$ sized squares yielding sets $S _ { i , j } = \{ \lvert l , l + 2 \rvert \times \lvert t , t + 2 \rvert |$ $l \equiv i$ mod $m , t \equiv j$ mod mg;

6: for each $s \in S _ { i , j }$ , compute a minimum patching set for s in $\boldsymbol { G } _ { c } ,$ and combine these vertices into $H _ { i , j } ;$

7: if $| H | > | H _ { i , j } |$ then $H : = H _ { i , j } ;$

8: endfor

9: endfor

Given an MPMSP $( G _ { c } , G , E _ { p } , V _ { p } , b )$ where $G _ { c }$ is a UDG with geometric representation. All vertices that can monitor the same edge lie in the lune region, which is the intersection of two disks with their centers being the endpoints of the monitored edge. As a result, every edge e in $E _ { p }$ is corresponding to (one-to-one) a lune $l _ { e }$ in the plane, and the MPMSP can be considered as selecting minimum size of vertices set from $V _ { p }$ to hit the lunes such that each lune $l _ { e }$ is hit $b ( e )$ times.

Let R denote the least rectangular region in which graph $G _ { c }$ can be drawn. For the given input ", we precompute the minimum even number $\stackrel { \cdot } { m } \geq 1 2 / \varepsilon .$ . Note that we use the disk radius as unit length by default. For each pair of even integers $( i , j )$ , where $2 \doteq i , j \le m$ , we partition the region R into squares by horizontal lines at $l \equiv i$ mod m and vertical lines at $t \equiv j$ mod m. A lune is said to be belonging to a square if and only if its geometric center lies in the square. Let $S _ { i , j }$ denote the set of squares for a fixed pair $i , j .$ In Step $^ { 6 , }$ for each square in $S _ { i , j } ,$ an optimal solution is given by complete enumeration, and the union of those sets gives a candidate hitting set $H _ { i , j }$ for fixed $i , \ j .$ By changing the parameters i and j, we have the minimum set H.

Theorem 4.6. Algorithm 1 gives a PTAS for MPMSP in UDG with a geometric representation.

Proof. Let $H _ { o }$ be an optimal hitting set, and let H be the set obtained from the shifting strategy. For fixed i and ${ j , }$ let $H _ { o } ( i , ^ { * } ) , H _ { o } ( ^ { * } , j )$ , and $H _ { o } ( ^ { * } , ^ { * } )$ be the vertices set in $H _ { o }$ and they lie in lunes intersecting horizontal active lines, vertical active lines, and either horizontal or vertical active lines. For square $s \in S _ { i , j } ,$ let $L ( s )$ denote the set of lunes belonging to the square s. Let $H _ { o } ( s )$ be vertices in $H _ { o }$ and $L ( s ) , { \bar { O P T } } ( s )$ be the optimum hitting set for lunes $L ( s )$ .

We have the following inequations for any i and $j \colon$

$$
| H | \leq | \cup_ {s \in S _ {i, j}} O P T (s) | \leq \sum_ {s \in S _ {i, j}} | O P T (s) | \leq \sum_ {s \in S _ {i, j}} | H _ {o} (s) |.
$$

Since vertices in lunes that hit an active line can be used in at most four squares, we have

$$
\sum_ {s \in S _ {i, j}} | H _ {o} (s) | \leq 3 | H _ {o} (^ {*}, ^ {*}) | + | H _ {o} |.
$$

Note that we set the shifting step be two units as shown in Step 3 and 4, so that all lunes that hit one horizontal (or vertical) active line do not intersect with lunes that hit another horizontal (or vertical) active line. Thus, we obtain the following inequations:

$$
\begin{array}{l} \sum_ {2 \leq i \leq m} | H _ {o} (i, ^ {*}) | \leq | H _ {o} |, \\ \sum_ {2 \leq j \leq m} | H _ {o} (^ {*}, j) | \leq | H _ {o} |. \\ \end{array}
$$

There exist some choices of $( i , j )$ such that

$$
\left| H _ {o} \left(i, ^ {*}\right) \right| \leq 2 \left| H _ {o} \right| / m,
$$

$$
| H _ {o} (^ {*}, j) | \leq 2 | H _ {o} | / m.
$$

For the choice of ði; jÞ, we have

$$
| H _ {o} (^ {*}, ^ {*}) | = | H _ {o} (i, ^ {*}) \cup H _ {o} (^ {*}, j) | \leq | H _ {o} (i, ^ {*}) | + | H _ {o} (^ {*}, j) |
$$

$$
\leq 4 \left| H _ {o} \right| / m.
$$

And then,

$$
| H | \leq (1 + 1 2 / m) | H _ {o} | \leq (1 + \varepsilon) | H _ {o} |.
$$

We now prove that the algorithm runs in polynomial time by showing that an optimal solution in each square nodes can be computed in polynomial time by complete enumeration. For a given constant m, we will show that the size of optimal patching set in each square is bounded by $\scriptstyle { \dot { O } } ( m ^ { 2 } )$ . Therefore, an optimal solution in $S _ { i , j }$ with n nodes can be computed in $\cdot n ^ { O ( m ^ { 2 } ) }$ .

Suppose there are n edges $\{ e _ { i } | i \in [ 1 , n ] \}$ in a square region $s ,$ and each edge $e _ { i }$ needs to be hit $b ( e _ { i } ) \geq 1$ times. Let $b _ { M } = M a x ( b )$ be the maximum value in b. We can consider that there exist $b ( e _ { i } )$ number of superposed lunes corresponding to edge $e _ { i } .$ Thus, the total number of lunes is $\sum { \hat { b } } ( l _ { i } ) ^ { * } | l _ { i } |$ . Logically, these lunes can be partitioned into $b _ { M }$ groups in a manner such that each group contains $L _ { k }$ number lunes, $k \in [ 1 , b _ { M } ] ,$ , with $L _ { k + 1 } \leq L _ { k }$ . For each group, we define the shadow area of these $L _ { k }$ lunes as $\begin{array} { r } { A _ { s } ( L _ { k } ) = \hat { | } \cup _ { i = 1 } ^ { L _ { k } } l _ { j } | . } \end{array}$ , which is the aggregate area of the region overlapped by the lunes. It is clear that $A _ { s } \mathbf { \bar { ( } } L _ { k } ) \leq ( m + \mathbf { \bar { 1 } } ) ^ { 2 }$ , and m is the side length of the square region s. We know that the area of smallest lune in a square is equal to $\alpha = 2 \pi / 3 - \sin ( 2 \pi / 3 ) \cong 1 . 2 2 8 4$ . Considering that each vertex is able to hit only one among the superposed lunes corresponding to the same edge, we need at most $A _ { s } ( L _ { k } ) / \alpha$ vertices to hit the $L _ { k }$ number lunes. The number of total vertices to hit all the lunes is bounded by $\begin{array} { r } { \sum _ { k } A _ { s } ( L _ { k } ) / \alpha \leq b _ { M } ( m + 1 ) ^ { 2 } / \alpha < b _ { M } ( m + 1 ) ^ { 2 } } \end{array}$ . Thus, the optimal solution is bounded by $O ( m ^ { 2 } )$ . tu

# 4.3 PTAS in Monitoring-Set-Bounded Graph

We have exploited the geometric representation of communication network and designed a shifting strategy to yield a PTAS. In the case without geometric representations, however, shifting strategy is not available. Indeed, given a UDG, computing its corresponding representation is NPhard [18]. Moreover, approaches based on shifting strategy need centralized mechanisms to select the optimal solution among candidates. Such approaches are inherently centralized. Hence, it is desirable to design a PTAS algorithm that is independent of the geometric representation and favors distributed design. Now we present a PTAS algorithm in monitoring-set-bounded graph. The idea is inspired by previous works for maximum independent set [18]. We will also show that polynomially monitoring-set-bounded graphs indeed formulate a more general family of graphs, which covers UDGs or quasi-UDGs [18].

Definition 4.2 (Monitoring-Set-Bounded Graph). For every vertex v in $\mathrm { V } ( G _ { c } )$ and a positive integer i, let $G _ { c } ( \Gamma _ { i } ( v ) )$ denote the vertex-induced subgraph of $G _ { c }$ with $\Gamma _ { i } ( v )$ that is the i-hop neighborhood of v. If there exists a polynomial function $f ( x )$ such that the optimal solution for the reduced MPMSP in graph $G _ { c } ( \Gamma _ { i } ( v ) )$ is of at most fðiÞ size, we say that $G _ { c }$ is monitoring-set-bounded.

Lemma 4.7. UDG is monitoring-set-bounded graph.

Proof. Let v be any vertex in UDG $G , u \in \Gamma _ { r } ( v )$ , and $d _ { u , v }$ denote the euclidean distance between u and v in the plane. Clearly, we have $d _ { u , v } \leq r$ . Considering all the lunes that are in the $\Gamma _ { r } ( v )$ and v reside in the big disk with center v and radius $r + 1$ . Hence, the optimal solution that needs to hit all these lunes is bounded by $O ( \left( r + 1 \right) ^ { 2 } )$ Þ. The proof is similar as in Theorem 4.6 by correspondingly displacing ðm $+ \ : 1 ) ^ { 2 }$ with $\pi ( r + 1 ) ^ { 2 } )$ . tu

It is not difficult to show that quasi-UDG is also a monitoring-set-bounded graph. We now present the Algorithm 2 that gives the PTAS for MPMSP in polynomially monitoring-set-bounded graph without representations.

Algorithm 2. PTAS for MPMSP (without representation) Input: MPMSP $( G _ { c } , G , E , V , b )$ , monitoring-set bounded graph $G _ { c } , \varepsilon > 0 .$

Output: ð1 þ "Þ-approx. minimum patching monitoring set H

1: $H = \emptyset$ 2: while $E \neq \emptyset$ do
3: select $v \in V$ 4: for $r_v = 1$ to $r^*$ 5: compute minimum patching set $H_r(v)$ in $G_c(\Gamma_r(v))$ and $H_{r+1}(v)$ in $G_c(\Gamma_{r+1}(v))$ ;
6: if $H_{r+1}(v) \leq (1 + \varepsilon)H_r(v)$ , break;
7: endif
8: endfor
9: $H := H \cup H_{r+1}(v)$ ;
10: $E := E \backslash G_c(\Gamma_{r-1}(v)); V := V \backslash G_c(\Gamma_{r-1}(v))$ ;
11: endwhile

Given an MPMSP $( G _ { c } , G , E , V , b )$ , algorithm II starts by selecting one arbitrary vertex $v \in V ( G ( E ) )$ and considers its rth neighborhoods $\dot { \Gamma _ { r } } ( v )$ and the reduced MPMSP in the graph $\bar { G } _ { c } ( \Gamma _ { i } ( v ) )$ . For the reduced problem instance, optimal patching sets $H _ { r } ( v ) = H _ { \ i }$ in $\Gamma _ { r } ( v )$ can be computed by complete enumeration. We increase the $r$ from 1 to $2 , \ldots$ until the inequation (1) is violated. We iteratively perform the above processes to achieve an patching set for $( G _ { c } , G , E , V , \bar { b } )$ . Each time we remove the neighborhood vertices $\Gamma _ { r - 1 } ( v )$ from G and combine $H _ { r + 1 }$ with the current partial solution H. The details are described in Algorithm II. Notation $r ^ { * }$ denotes the maximum possible value of r:

$$
\left| H _ {r + 1} \right| > (1 + \varepsilon) \left| H _ {r} \right|. \tag {1}
$$

Lemma 4.8. Given an MPMSP $( G _ { c } , G , E , V , b ) ,$ , and $G _ { c }$ be a graph of polynomially monitoring-set-bounded graph. There exists a constant c such that $r ^ { * } \leq c .$

Proof. Let the graph $G _ { c }$ be monitoring-set-bounded with polynomial function $f ( x )$ . For any vertex v in $G _ { c }$ and the reduced problem MPMSP in $G _ { c } ( \Gamma _ { i } ( v ) )$ , we have optimal patching sets with size $| H _ { r } ( v ) | = | H _ { r } | \leq f ( r )$ by the definition of monitoring-set-bounded graph. Further, for the given approximation parameter ", we have the following inequations:

$$
\left| H _ {r} \right| > (1 + \varepsilon) \left| H _ {r - 1} \right| > \dots > (1 + \varepsilon) ^ {r - 1} \left| H _ {1} \right|,
$$

$$
f (r) > (1 + \varepsilon) ^ {r - 1} | H _ {1} | \geq (1 + \varepsilon) ^ {r - 1}.
$$

Since $r ^ { * }$ is the supremum of set $\{ r | f ( r ) > ( 1 + \varepsilon ) ^ { r - 1 } \} _ { { } } \nonumber$ , there exists a constant $c ( f , \varepsilon )$ such that $r ^ { * } \leq c ( f , \varepsilon )$ . tu

We now show that Algorithm II terminates in polynomial time and achieves ð1 þ "Þ approximation for MPMSP. As in each iterative procedure, we select a new central vertex to construct local neighborhoods, the number of iterative times is bounded by $\overset { \cdot } { n } = \left| V \right|$ . Let the running time of each iteration be $T _ { i }$ . It is clear that $T _ { i } \leq r ^ { * } n ^ { f ( r ^ { * } ) } \leq$ $c n ^ { f ( c ) }$ from Lemma 4.8. Hence, the execution time of Algorithm II is bounded in $c n ^ { f ( c ) + 1 }$ polynomial time of $n .$

Theorem 4.9. Algorithm II gives ð1 þ "Þ approximation $f o r$ MPMSP in polynomially monitoring-set-bounded graph without representation.

Proof. Let $H _ { o }$ denote the optimal solution. By inductive argumentation over the execution of algorithm, we have

$$
| H | = \left| \cup_ {v} H _ {r + 1} (v) \right| \leq \sum_ {v} \left| H _ {r + 1} (v) \right| = (1 + \varepsilon) ^ {*} \sum_ {v} \left| H _ {r} (v) \right|.
$$

While

$$
\begin{array}{l} \left| H _ {o} \right| \geq \left| \left(\cup_ {v} H _ {o} (v)\right) \cap H _ {o} \right| = \left| \cup_ {v} \left(H _ {o} (v) \cap H _ {o}\right) \right| \\ = \sum_ {v} | H _ {o} (v) \cap H _ {o} | = \sum_ {v} | H _ {r} (v) |. \\ \end{array}
$$

Hence, $| H | \leq ( 1 + \varepsilon ) ^ { * } | H _ { o } |$ .

![](images/b784ea77b41daf4a4ebb6c6d8479945ecbc8696ec8f62af3f08e192ff05094dd.jpg)

# 4.4 Weighted MPMSP and General Graph

For the weighted version of the problem WMPMSP, the PTAS approaches are not applicable due to the fact that the cardinality of a weighted patching set in a given region cannot be bounded. Alternately, we present some restricted version of WMPMSP. Specifically, the ratio of the maximum and minimum weight, max $( W _ { p } ) / m i n ( W _ { p } )$ , is bounded by a constant. Recall that $W _ { p }$ denotes vertex weight function on $V _ { p }$ . In this case, the cardinality of a weighted patching set in a given region is still bounded. It is not difficult to modify the Algorithms I and II and adapt the corresponding proofs to the weighted problem of restricted version. Such modifications will replace the cardinality of the subsets with their respective weights. Hence, Algorithms I and II can still give the PTAS for the restricted WMPMSP mentioned above.

Theorem 4.10. There exists -approximation algorithm for $M P M S P$ and WMPMSP in general graph, where $\rho = m i n ( H ( \Delta ) , \Lambda )$ .

Proof. Clearly, in general graph, the MPMSP (or WMPMSP) can be formalized as the set multicover problem. Hence, we can acquire the approximation ratio from set multicover [22]. $\begin{array} { r } { \dot { \mathbf { \mu } } ( n ) = \dot { \sum } _ { i = 1 } ^ { n } 1 / i } \end{array}$ is the nth harmonic number. tu

# 5 DISTRIBUTED ALGORITHM

As a large-scale sensor network typically works in a distributed and ad hoc manner, in this section, we present two localized algorithms for the MPMSP problem, called local maximal element (LME) and locally dual feasible (LDF). None of them uses location information, and they are independent of communication models. Meanwhile, our algorithms also set a good trade-off between the performance (the theoretic bound of approximation algorithm) and the complexity of implementation (simple to run).

For a general communication network $G \subseteq G _ { c } ,$ we assume that the self-monitoring requirements for each link are known for all the nodes, or are specified by the upper layer protocols using the self-monitoring as an underlying function.

Each node in G exchanges the neighbor list with one-hop neighbors. Thus, a node $P$ can determine which links can be monitored by it and which nodes can monitor the links adjacent (connecting) to $P .$ The links do not meet the selfmonitoring requirement form the $E _ { p } ,$ and monitoring number of each link b is determined accordingly. All nodes in $\mathrm { V } ( G _ { c } ) \backslash V ( G )$ form the set $V _ { p } .$ .

Given $G _ { c }$ and $G ,$ an MPMSP $( G _ { c } , G , E , V , b )$ is denoted as MPMSP (E, V , b) in which two vertices in V are said to be adjacent if they monitor the same edge in E. The adjacent vertex set of $v ,$ denoted as $\mathbf { A } ( v )$ , is the set of all the vertices adjacent to v in V . Let us recall some notions given in Definition 4.1. The monitoring degree of $v ,$ denoted as $\delta ( v )$ , is the number of edges in E that can be monitored by v. The monitored degree of edge e is denoted as $\lambda ( e )$ . Moreover, we let $\operatorname { E } ( v )$ denote all edges that can be monitored by v and $\mathrm { V } ( e )$ denote all vertices that can monitor e.

# 5.1 Local Maximal Element (LME) Algorithm

In LME, a candidate vertex is chosen only if it is optimal within its adjacent vertex set. The priority of a vertex depends on its monitoring degree. It means that a vertex has higher priority if its monitoring degree is high. We break the tie by selecting the vertex with the largest ID among vertices.

LME is carried out in a parallel manner. In each round, all the locally optimal vertices are selected. The monitored degree of every edge and candidate monitoring vertex set are updated accordingly. LME runs iteratively until the solution is found or the candidate monitoring vertex set V is empty. A loosely synchronous clock among local vertices is sufficient for LME. We describe our approximation algorithm in Algorithm 3.

# Algorithm 3. LME (code for vertex v)

Input: MPMSP $( G _ { c } , G , E , V , b )$

Output: patching monitoring set S

1: while $\delta ( v ) > 0$ do

2: v exchange its priority with those of $\operatorname { A } ( v ) ;$   
3: if v has the highest priority among A(v)   
4: Add v to S;   
5: Inform each edge e in E(v) to update their monitored number, $\lambda ( e ) = \lambda ( e ) + 1 ;$ If ðeÞ is equal to $b ( e )$ , Edge e informs each node u in VðeÞ to decrease its monitoring number, and $E = E \backslash e ;$

![](images/5b3e09052b5ab520458abed00ae96f320124689a11a8c30780a009fde90ba3f7.jpg)



Fig. 6. Local maximal element algorithm.

$6 { : }$ elseif v receive an updated message from one edge in $\operatorname { E } ( v )$ to decrease its monitoring number.   
7: $\delta ( v ) = d ( v ) - 1$ , calculate updated priority of $v ;$   
8: endif   
9: endwhile

We illustrate the execution steps of LME in Fig. 6, where the communication graph is modeled as UDG. The bold lines denote the edges that do not meet the 1-self-monitoring requirement. The circles denote the sensor nodes, and the lines denote the links in the connectivity topology. The vertex having higher monitoring degree means that it falls into the overlap field of more lunes. In the first round, nodes 18, 22, and 24 are selected since they have locally maximal priority and are able to monitor more edges than their neighbors. Now, seven edges are monitored as drawn with double line. Note that nodes 12 and 18 both have the highest monitoring degree, 4, while node 18 is selected since it has a larger ID. The same case happens to nodes 21 and 22. All the other candidate nodes are either adjacent to or dependent on the three nodes, thus cannot be selected in this round. In the second round, node 12 is selected. In the third round, nodes 9 and 11 are selected and LME terminates successfully. In this example, LME runs in three rounds and gives a solution size of 6. The squares denote the found solution, that is, nodes 9, 11, 12, 18, 22, and 24.

Theorem 5.1. The LME algorithm computes an $H ( \Delta )$ approximation for MPMSP in general graph within $O ( \Delta )$ rounds w.h.p.

Given an instance $( E , V , b ) ,$ each element in V has a priority value. Now we define a strict partial order relationship $^ { \prime \prime } \succ ^ { \prime \prime }$ on V . Relationship $^ { \prime \prime } \succ ^ { \prime \prime }$ is irreflexive and transitive, defined by: for $u , v \in \bar { V } ,$ if the priority of u is higher than that of v and the selection of one will decrease the priority of the other directly, then $u \succ v .$ . If $u \succ v$ and $v \succ w$ for $u , v , w \in V .$ , then $v \succ w .$ . Thus, set V with the strict order $^ { \prime \prime } \succ ^ { \prime \prime }$ forms a poset. Apparently, such a poset is not necessarily total. Intuitively, the strict order $\prime \prime \mathrm { _ { \it V } } \mathrm { _ { \it I \mathrm { ^ { \prime } \mathrm { ^ { \prime } \mathrm { } } } } }$ symbolizes the direct or indirect dependence relationship among candidate nodes in V . We further define a term top-antichain as the set of all maximal elements1 in $V .$ .

Given $( E , V , b )$ , we use $( E ( v ) , \ V ( v ) , b ( v ) )$ to denote the reduced problem instance after adding the vertex $v \in V$ into the patching monitoring set.

1. $u \in V$ is a maximal element means that there does not exist $v \in V$ such that $v \succ u .$

Lemma 5.2. Given $( E , V , b )$ , let $C _ { 1 } = [ c _ { 1 } , c _ { 2 } , \ldots , c _ { k - 1 } , c _ { k }$ ; $c _ { k + 1 } , \hdots , c _ { N } ]$ be a greedy solution sequence for $( E , V , b )$ and $c _ { k }$ be a maximal element in $V ,$ then $C _ { 2 } = [ c _ { 1 } , c _ { 2 } , \ldots ,$ ; $c _ { k - 1 } , c _ { k + 1 } , \ldots , c _ { N } ]$ is a greedy solution sequence $f o r \ ( E ( c _ { k } )$ , $V ( c _ { k } ) , b ( c _ { k } ) )$ .

Proof. We use $( E _ { 1 , i } , V _ { 1 , i } , b _ { 1 , i } )$ to denote the reduced problem of $( E , V , b )$ after selecting the vertices of $\{ c _ { l } \in C _ { 1 } , \stackrel { \cdot } { l } \in [ 1 , i ] \}$ and adding them into the patching monitoring set, and let $P _ { 1 , i } ( v )$ denote the priority of node v in $( E _ { 1 , i } , V _ { 1 , i } , b _ { 1 , i } )$ . We use $( E _ { 2 , i } , V _ { 2 , i } , b _ { 2 , i } )$ to denote the reduced problem of $( E ( c _ { k } ) , V ( c _ { k } ) , b ( c _ { k } ) )$ Þ after selecting the vertices of $\{ c _ { l } \in$ $C _ { 2 } , l \in [ 1 , i ] , l \neq k \}$ and adding them into the patching monitoring set, and let $P _ { 2 , i } ( v )$ denote the priority of node v in $( E _ { 2 , i } , V _ { 2 , i } , b _ { 2 , i } )$ .

Since $C _ { 1 }$ is a solution for $( E , V , b )$ , it is clear that $C _ { 2 }$ is a solution sequence for $( E ( c _ { k } ) , V ( c _ { k } ) .$ , and $b ( c _ { k } ) )$ Þ. Thus, we only need to show that $C _ { 2 }$ is a greedy sequence, that ${ \mathrm { i } } \mathbf { s } ,$ , $P _ { 2 , i } ( c _ { i } ) > P _ { 2 , i } ( c _ { j } )$ for $c _ { i } , c _ { j } \in C _ { 2 }$ and $i < j .$ Since $c _ { k }$ is a maximal element in $V ,$ , the selection of $c _ { k }$ will not change the priority of $c _ { i }$ for $i \in [ 1 , k - 1 ]$ . Otherwise, let $c _ { t } , \ t \in$ $[ 1 , k - 1 ]$ be the first element in $C _ { 1 }$ which can change the priority of $c _ { k } ,$ we have $P _ { 1 , 1 } ( c _ { t } ) \geq P _ { 1 , t } ( c _ { t } ) > P _ { 1 , t } \bar { ( } c _ { k } ) =$ $P _ { 1 , 1 } ( c _ { k } ) , ~ c _ { t } \succ c _ { k }$ in V so that $c _ { k }$ will not be a maximal element in $V ,$ contradiction. Hence, $P _ { \mathrm { 2 } , i } ( c _ { i } ) = P _ { \mathrm { 1 } , i } ( c _ { i } )$ Þ for $i \in [ 1 , k - 1 ]$ . Moreover, we have $P _ { 2 , i } ( c _ { i } ) = P _ { 1 , i } ( c _ { i } )$ for $i \in [ k , N ]$ . Note that $C _ { 1 }$ is a greedy sequence for $( E , V , b ) .$ , so $P _ { 2 , i } ( c _ { i } ) = P _ { 1 , i } ( c _ { i } ) > P _ { 1 , j } ( c _ { j } ) = P _ { 1 , j } ( c _ { j } )$ for $i , j \in [ 1 , k$  $1 ] \cup [ k , N ]$ and $i < j .$ . tu

Lemma 5.3. Let $C _ { 1 } = [ c _ { 1 } , c _ { 2 } \ldots c _ { k - 1 } , c _ { k } , c _ { k + 1 } \ldots . . . c _ { N } ]$ be a greedy solution sequence for $( E , V , b ) , T \subseteq C _ { 1 }$ is a top-antichain in $V ,$ then $\dot { C } _ { 2 } = \dot { C _ { 1 } } \backslash T$ is a greedy solution sequence for $( E ( T ) , V ( T ) , b ( T ) )$ .

Proof. Through exercising Lemma 5.2 recursively.

Theorem 5.4. LME runs in Oð-Þ rounds w. $i . p . ,$ , and the solution of LME is equivalent to that of centralized greedy algorithm.

Proof. Given an MPMSP ðE; V ; bÞ, let the solution of centralized greedy be $C ,$ the solution of LME be D, and LME runs in N rounds. Let $R _ { i }$ denote the selection of LME in ith round, we have $D = \cup _ { i = 1 } ^ { N } R _ { i }$ . Further, let $( E _ { i } , V _ { i } , b _ { i } )$ denote the reduced problem after selecting nodes set $\cup _ { l = 1 } ^ { i - 1 } R _ { l }$ , and $C _ { i }$ be greedy solution sequence for $( E _ { i } , V _ { i } , b _ { i } )$ . Apparently, $( E _ { 1 } , \bar { V } _ { 1 } , b _ { 1 } )$ is the same to $( E , V , b )$ .

First, we show that $R _ { i }$ is a top-antichain in $V _ { i }$ by proving that: 1) $\forall r \in R _ { i } , r$ is a maximal element of $V _ { i }$ and $2 ) \forall s \in V _ { i }$ if s is a maximal element of $V _ { i } , s \in R _ { i }$ . Since all nodes that can affect r must be in $\mathrm { A } ( r ) \cap V _ { i }$ and the priority of r is the highest in $\mathrm { A } ( r ) \cap V _ { i } ,$ r is a maximal element in poset $( V _ { i } , \stackrel { } { \succ } )$ . Also, $\forall s \in V _ { i }$ if s is a maximal element in ${ \bar { V } } _ { i } ,$ , which means that the priority of s is the highest in $\mathrm { A } ( s ) \cap V _ { i }$ , so s will surely be selected by LME algorithm in ith round. We have $s \in R _ { i }$ .

Second, we show that $R _ { i } \subseteq C _ { i }$ and $C _ { i + 1 } = C _ { i } \backslash R _ { i }$ . $\forall r \in R _ { i } ,$ , for an edge which can be monitored by $r , r$ will hold the highest priority among all the vertices that can monitor the edge, so centralized greedy will definitely select r to monitor that edge, thus $r \in C _ { i }$ i and $R _ { i } \subseteq C _ { i }$ . Likewise, $R _ { i }$ is a top-antichain in $V _ { i } ;$ therefore, from Lemma $5 . 3 ,$ we know that $C _ { i } \backslash R _ { i }$ is a greedy solution sequence for $E _ { i } ( R _ { i } ) = E _ { i + 1 }$ and $C _ { i + 1 } = C _ { i } \backslash R _ { i }$ .

Third, we show that $D = C .$ Since LME ends in N rounds, when LME runs in the Nth round, for instance, $( E _ { N } , V _ { N } , b _ { N } )$ , it is clear that $D _ { N } = R _ { N } = C _ { N }$ . Hence,

$$
\begin{array}{l} C = C _ {1} = R _ {1} \cup C _ {2} = R _ {1} \cup R _ {2} \cup C _ {3} \\ = \dots = R _ {1} \cup \dots \cup R _ {N - 1} \cup C _ {N} \\ = R _ {1} \cup \dots \cup R _ {N - 1} \cup D _ {N} \\ = R _ {1} \cup \dots \cup R _ {N - 1} \cup R _ {N} = D. \\ \end{array}
$$

Finally, we show that N is at most $O ( \Delta )$ . Since $R _ { i }$ is a top-antichain in $V _ { i } ,$ we have $\forall r _ { i + 1 } \in R _ { i + 1 } , r _ { i } \in R _ { i } ,$ , such that $r _ { i + 1 } \succ r _ { i }$ in Vi. We say that $r _ { i }$ is the tight upper vertex of $r _ { i + 1 }$ . Let $\delta _ { i } ( r )$ denote the monitoring degree of r in ith round, then $\delta _ { i + 1 } ( r _ { i + 1 } ) \leq \delta _ { i } ( r _ { i + 1 } ) \leq \delta _ { i } ( \bar { r } _ { i } )$ . From choosing an arbitrary vertex $r _ { N } \in R _ { N }$ , we can derive the tight upper vertices $r _ { N - 1 } \in R _ { N - 1 }$ of $r _ { N } .$ Recursively, the tight upper vertices $r _ { N - 2 } , \ldots r _ { 1 }$ are obtained sequentially. Thus, we get the following inequation: $1 \le \delta _ { N } ( r _ { N } ) \le \cdots \le$ $\delta _ { i } ( r _ { i } ) \leq \cdot \cdot \cdot \leq \delta _ { 1 } ( r _ { 1 } ) \leq \bar { \Delta }$ . Let the length of maximum equivalence sequence among $\delta _ { i } ( r _ { i } )$ be $L ,$ we have $\bar { N _ { \mathrm { } } } \leq \Delta L$ . If we assume that the nodes are deployed randomly, such that node IDs are distributed randomly, the expectation of L is Oð1Þ. tu

Theorem 5.1 can be obtained from Theorem 5.4 since the approximation ratio of sequential greedy algorithm is $\bar { H ( \Delta ) }$ , as shown in Theorem 4.10. Note that the bound $H ( \Delta )$ is asymptotically reachable, and such problem instances can be constructed by properly modifying the proof of Theorem 5 [23].

Liang et al. have partially observed the similar results we prove here. Their proof [24], however, is not strict but based on intuitive arguments. Indeed, their major statement is equivalent to our work of $R _ { i } \subseteq C _ { i }$ , as shown in the second step of the proof for Theorem 5.4, while our proof is more general.

# 5.2 Locally Dual-Feasible (LDF) Algorithm

The LDF algorithm is different from LME in that LME considers the solution from the monitoring nodes, while the LDF deals with the problem from the view of the monitored edges.

An important technique in LDF is the construction of the edge-dependent graph. An edge-dependent graph $G _ { e }$ is derived from the problem instance $( E , V , b )$ and is constructed as follows: A vertex in $\mathrm { V } ( G _ { e } )$ corresponds to an edge in $E ,$ and an edge between any two vertices in $\mathrm { V } ( G _ { e } )$ exists if the two edges in E can be monitored by a common vertex in V .

LDF is also carried out in rounds, and each round consists of four steps. Let $( E ^ { \prime } , V ^ { \prime } , b ^ { \prime } )$ denote the reduced problem instance for the current round. First, the derived edge-dependent graph of $( E ^ { \prime } , V ^ { \prime } , b ^ { \prime } )$ is constructed. Second, we calculate a maximal independent set (MIS) of the derived edge-dependent graph in a distributed manner [25]. The calculated MIS is in one-to-one correspondence with an edge subset of $E ^ { \prime }$ . We call such an edge subset maximal independent edge set (MIES) of $E ^ { \prime }$ . Third, for each edge, say $e ,$ in MIES, constructed in step two, an expected number of vertices are selected among all the vertices in $V ^ { \prime }$ that are able to monitor the edge. The expected number is equal to the current monitoring number of the edge $\boldsymbol { e } , \boldsymbol { b } ^ { \prime } ( \boldsymbol { e } )$ . Fourth, each

![](images/ca1da881a538d736ef367027321eb6499562661617fbe67e76ef7f1df771e781.jpg)



Fig. 7. Locally dual-feasible algorithm.

edge in $E ^ { \prime }$ updates its monitored degree according to the newly selected monitoring vertices in step 3. At the same time, $E ^ { \prime } , \ V ^ { \prime } ,$ and b0 are all updated accordingly. The LDF algorithm terminates when the edge set $E ^ { \prime }$ is empty. The details are given in Algorithm 4.

# Algorithm 4. LDF (code for edge e)

Input: MPMSP $( G _ { c } , G , E , V , b )$

Output: patching monitoring set S

1: while $E \neq \emptyset$ do   
2: Construct the edge-dependent graph, and maximal independent edge set (MIES).   
3: if e is in MIES,   
4: if $| \mathrm { V } ( e ) | \geq b ( e ) - \lambda ( e ) .$ , randomly select $b ( e ) - \lambda ( e )$ number of vertices $\mathrm { V } ^ { \prime }$ from $\mathrm { V } ( e ) .$ , add $\mathrm { V } ^ { \prime }$ into S. Otherwise, make the selected vertices $V ^ { \prime }$ be all the vertices in $\mathrm { V } ( e )$ , and report that edge e cannot be monitored properly;   
5: $\boldsymbol { E } = \boldsymbol { E } \backslash e ;$   
6: Inform those edges that are monitored by $\mathrm { V } ^ { \prime }$ to update their monitored degree;   
7: elseif e receives an updated message from one of its neighboring node   
8: $\lambda ( e ) = \lambda ( e ) + 1 ;$   
9: endif   
10: endwhile

Fig. 7 illustrates LDF algorithm in the same example with LME, as shown in Fig. 6. To achieve 1-self-monitoring requirement in UDG, in the first round, an MEIS of size six is calculated as shown by double line. For each edge, a node is selected, including nodes 4, 12, 16, 19, 21, and 24. After the selection of these nodes, only one edge that does not meet the 1-self-monitoring requirement is left. In the second round, node 14 is selected. LDF in the example runs in two rounds and obtains the solution of size 7.

We discuss the approximation ratio and time complexity of LDF algorithm as follows: Let $T _ { M }$ denote the maximal time of constructing an MIS in each round.

Theorem 5.5. The LDF algorithm provides an -approximation for MPMSP in $O ( ( \Lambda + 1 ) T _ { M } )$ times.

Proof. The approximation ratio can be acquired from the similar proof for the set multicover [22]. We mainly consider the time complexity here. We only need to determine for how many rounds the edge-dependent graph will be empty. Let v be a vertex in the derived edge-dependent graph and its degree be d(v). We claim that vertex v must be selected into one MIS within dðvÞ þ 1 round. If vertex v is not selected into MIS in a round, there must be at least a vertex neighboring to v in edgedependent graph that will be selected into the MIS. Hence, even assuming that v is the last one being selected among its neighbors, all neighbors of v will be selected within at most dðvÞ rounds, and finally, v will be selected within at most dðvÞ þ 1 rounds. Obviously, the maximal degree of the derived edge-dependent graph is . Hence, LDF will end within at most  þ 1 rounds. tu

![](images/250d5f81951a53a5af90075a8b8a89892e0980a721985658f61f0855f6d2715f.jpg)



Fig. 8. Local maximal element algorithm.

# 6 PERFORMANCE EVALUATION

In this section, we conduct extensive simulations on random networks to examine the performances of our algorithms. Throughout the simulations unless otherwise specified, we deploy the nodes in a square field, and assume that each node has the same transmission range. We generate the node locations within the field according to two-dimensional uniform random distribution. For each simulation setup, we take 100 runs and report the average.

# 6.1 Self-Monitoring Capability of Random Topology

First, we study the relationship between edge self-monitoring capability and working topology density in a random graph. Working topology density (TD) is defined as the average number of one node’s active neighbors. In this simulation, we deploy 400 nodes as the active working topology and change the average node degree by varying the transmission radius. Since in the simulations, all the nodes are activated, average node degree is TD. Fig. 8 illustrates the self-monitoring capability against TD from 5 to 10. The y-coordinate values denote the Cumulative Distributed Function (CDF) of monitored degree of an edge. Each line corresponds to one TD value. We can see that as TD increases, the corresponding topology provides higher monitored degree for edges. For example, TD of 5 yields 80 percents of edges with monitored degree of 1.5 (and below), while TD of 9 yields 80 percents of edges with monitored degree of 4.0 (and below), which means for a given self-monitoring degree requirement, the higher topology density, the lower proportion of edges needs the additional patching nodes, and vice versa. This is consistent with our intuitions. Note that high node degree generally cannot guarantee the edge self-monitoring capability of a network. It is not difficult to give a counterexample such that there exist edges that cannot be monitored in a network with high minimal node degree.

![](images/6ba071399da944aac61d12c816aa981eea7ec1b2a98f536d027a463c7b78fba2.jpg)



Fig. 9. Patching set size of different algorithm.

# 6.2 Comparison of LME and LDF

In these simulations, we deploy two kinds of nodes in the network, active nodes and sleep nodes, which is different with the network generation in Section 6.1. For the convenience to adjust the working topology density and the number of sleep nodes as candidate monitoring nodes, we generate a network in two steps. We first randomly deploy nodes to create an active working topology according to a given TD. We then add sleep nodes into the same region. We control the number of sleep nodes by a parameter called, worker ratio (WR), which is defined as the ratio of the node number in active working topology to total number of nodes in the network. For example, WR ¼ 2 means that proportion between active working nodes and sleep nodes is one to one. By default, we set that the number of active working nodes is 100, and WR is 6 in the simulations. Another two important parameters are monitoring number and patching set size. Monitoring number (MN) quantifies the monitoring requirement, the expected number of nodes monitoring one edge. Patching set size is defined as the ratio of the number of selected sleep nodes by the algorithms to the number of nodes in the initial active working topology.

We compare LME and LDF algorithms with the optimal solution and a random algorithm without considering any optimizations. The optimal solution is obtained by Matlab binary integer programming tools since the MSMTP can be easily addressed as an integer program problem. The random algorithm used for comparison purpose is called random independent selection (RIS) algorithm. In RIS, for a given edge, the required number of nodes is selected randomly among all the surrounding nodes that can monitor the edge, and all of the edges that need to be monitored make their decisions independently and simultaneously, and add all the selected nodes into the patching monitoring set.

In Fig. 9, we plot the CDF of set size for four algorithms when TD ¼ 8, MN ¼ 4, and WR ¼ 5. The results suggest that LME and LDF are very close to the optimal solution in terms of patching set size. Furthermore, from Fig. 9, we can see that the Optimal, LME, and LDF demonstrate good threshold phenomenon. The average performance is better than the theoretical worst case greatly. Obviously, RIS is the worst, and hence, it is worthy and necessary to use our algorithms to select the patching monitoring nodes.

![](images/689d79671c6260f385982e3ae992e931be37955f2504a12fc501be4e2eee56d4.jpg)



Fig. 10. A detailed comparison of LME and LDF.   
![](images/2ae6bc30a6c929c16429cdab2ce63bc39fde39b0ed4c791658233f259350482a.jpg)



Fig. 11. Patching set size against topology density of LME.   
![](images/e3fcfcd9be4dc5273f6c4fa88757430168e9d4a3c7bbdaf5444aee547ed88d90.jpg)



Fig. 12. Patching set size against topology density of LDF.

Fig. 10 further contacts LME and LDF when changing the TD and MN. The left two lines denote the results when TD ¼ 6, MN ¼ 2, and ${ \mathrm { W R } } = 5 ,$ and the right two lines denote the results when TD ¼ 8, MN ¼ 4, and $\mathrm { W R } = 5 .$ . In both cases, LME generates better performance than LDF. According to our results, in most of circumstance, LME is superior to LDF, but not always.

# 6.3 Impact of Topology Density and Monitoring Number

Since the self-monitoring capability of a topology changes with ${ \mathrm { T D } } ,$ as shown in Fig. 8, and the patching set size depends on the TD, we present the simulation results on the patching set size against TD. Figs. 11 and 12 show the results where TD changes from 5 to 10 with MN from 1 to 6. The error bars show 95 percent confidence intervals. From the two figures, we can see that the patching set sizes of LME and LDF decrease with the increase of TD, which matches the intuition. Since higher TD means fewer edges to be monitored and the same number of nodes can monitor more edges. Further, we can observe that with the increase

![](images/4b82dab0d694bd589e4fb053e1b0112110951c78e532591ec2763dd289448854.jpg)



Fig. 13. Patching set size against monitoring number of LME.   
![](images/e2a40a5f3675cdfd5aff5cdcecdc7b3ad277c3923ee00c43eb79bc8229a1bf11.jpg)



Fig. 14. Patching set size against monitoring number of LDF.

of TD, the gap of LME and LDF is gradually diminished, because when TD grows, the edges to be monitored decrease, and more isolated edges or small connected branches emerge, so the solution space that can be exploited for optimization shrinks accordingly.

Similarly, we present the patching set size against monitoring number. In Figs. 13 and 14, we can see that the output of LME and LDF almost increase linearly with monitoring number when $\mathrm { M N } \geq 3 ,$ but grow mildly from 1 to 2, especially for relatively higher $\mathrm { T D } \geq 9 .$ . This is due to the fact that when TD is relatively high, only a small part of edges, about 10 percent and less, have the monitored degree less than 2, while most of the edges, about 80 percent and more, have the monitored degree less than or equal to $^ { 4 , }$ as shown in Fig. 8.

Further, from Figs. 13 and 14, we can see that to achieve two-edge self-monitoring topology, we only need to add a small size of patching nodes, changing with topology density. It means that edge self-monitoring can be accommodated in sensor network with the modest number of extra nodes, especially when TD is relatively high.

# 6.4 Time Complexity

We simulate the LME and LDF in the synchronous running manner to investigate their time complexity. For the algorithm of distributed construction of MIS in LDF, we use a greedy method. We assign a distinct ID to each to be monitored edge, and the edge with the maximal ID first adds itself into the MIS.

As shown in Figs. 15 and 16, we can see that the running rounds of LME and LDF increase with the monitor number. This is because more edges need to be monitored when the monitor number increases. The performance of LME and LDF, however, is quite different from each other, especially when MN and TD increase. LME always decreases with the increase of TD and increases with MN, while LDF increases with TD when MN is relatively large. This is because when TD increases, the degree of vertex in derived edgedependent graph also increases greatly. Hence, the size of MIS of the derived graph in each round will decrease. As a result, the rounds of the LDF will rise. To summarize, the LME runs faster when TD is relatively lower, and LDF performs better when TD is relatively higher.

![](images/491d57ba290ef1f414d92b225c39a646de1e1d61465177c36153f86cb6068c0f.jpg)



Fig. 15. Rounds against monitoring number of LME.   
![](images/749b23fcbd2483ab984910c224b903dd595df939074960e4c779238ff799650c.jpg)



Fig. 16. Rounds against monitoring number of LDF.

# 6.5 Extended Connectivity Models

In previous simulations, the result is given under UDG models. It is worth pointing out that our algorithms are merely based on the connectivity information. To demonstrate the effectiveness of our algorithms in more general communication models, in this set of simulations, we test LME and LDF in quasi-UDG model with varying parameter $\rho ,$ denoted as $\rho { \mathrm { - Q U D G } }$ model. In a $\rho { \mathrm { - } } \mathrm { Q U D G }$ model [18], two nodes do not have a link if their distance is greater than 1, have a link if their distance is less than $\rho ,$ and have a link with probability if their distance is between $\rho$ and 1.

Again, we contrast LME and LDF algorithms with the optimal solution and RIS. Fig. 17 plots the CDF of patching set size found by the four methods in networks of 0.5- QUDG with TD ¼ 5, MN ¼ 2, and $\mathrm { W R } = 5$ . The results suggest that LME is still very close to the optimal solution in terms of patching set size in QUDG. We further vary $\rho \mathrm { - }$ $\mathrm { Q U D G }$ , MN to compare the four methods. Fig. 18 shows the result where MN ¼ 3, $\rho = 0 . 4$ and the y-coordinate shows the ratio of set sizes of LME, LDF, and RIS to that of optimal solution. Fig. 19 shows the average set size of different algorithms against the varying parameter $\rho$ with $\mathrm { T D } = 5$ and $\mathrm { M N } = 2 .$ . From above observations, we can summarize that LME and LDF are also applicable in extended connectivity models of QUDG.

![](images/a95d66658f8758cb350308b7e524a9db8c46e68cb08eaaae8f6daddf8886c21b.jpg)



Fig. 17. Patching set size of different algorithm in 0.5-QUDG.   
![](images/0d638f07157cc387022d746f5e62d34ac4fb2679c1a38d665af259e3477aad55.jpg)



Fig. 18. Patching set size against topology density in $0 . 4 { \cdot } \mathsf { Q } \mathsf { U } \mathsf { D } \mathsf { G }$ .   
![](images/6f41c85e69272adddcd0c32e188645b7670027627b38ff707c166701b92a9f16.jpg)



Fig. 19. Ration of patching set size of different algorithms of against the optimal.

Finally, we change the number of deployed nodes to examine the scalability of the LME and LDF. LME and LDF show good scalability on solution size and time complexity. See [9] for more such results.

# 7 DISCUSSIONS

# 7.1 Practical Applications

Continuous monitoring of each node in a network may incur high energy cost in practical applications. For energyconstrained WSNs, we may need to implement the selfmonitoring with other energy conservation strategy such as scheduling, adaptive duty cycle, etc., as considered in existing works using local monitoring schemes [3], [4], [12]. For example, each node in the network can schedule itself to switch into monitoring state as fixed or random periods. The nodes may also be scheduled by the upper protocols using the local monitoring function. As such, the selfmonitoring capability in the network can be on demand. For example, monitoring nodes are scheduled to be awaken only when they are close to the links that there are data transmission through [12]. Moreover, when the network is in a lower security alert, each node may be in monitoring state in a shorter time; while when the network has higher requirements, more nodes can carry out monitoring operations. Hence, the self-monitoring topology can be tailored to cater the different requirements and offer the assurance to other techniques using local monitoring, and can be implemented flexibly in practice.

# 7.2 Interference

In the real wireless network, interference is an important factor for all approaches using local monitoring schemes, as collisions in the wireless channel can cause a high error rate for overhearing. If two links transmit data simultaneously, the node that monitors the two links may overhear nothing due to the interference. Hence, interference also affects the node selection strategy. There are several methods to deal with interference in our algorithms. For example, we can evaluate and calculate the interference level of candidate monitoring nodes according to the number of potential interference nodes. We can make that the candidate nodes with a lower interference level have higher priority to be selected. Or we restrict nodes with interference level above a threshold being excluded during the preprocess stages for construction of self-monitoring topology. Thus, only the nodes with a low interference level are considered as candidates.

Indeed, it is difficult to eliminate the interference effect in the local monitoring scheme. Fortunately, interference has the stochastic feature and interference intensity could be changed over traffics and time. If a node potentially suffers interference in some time slots, it still can monitor the links in other time slots. Hence, instead of eliminating the effect of interference, current works [3], [4], [12] often consider tolerating interference and stochastic faults. For example, monitoring (guard) nodes watch a link and gather the packets into a watch buffer. Guard nodes depend on characteristics of the malicious activity detected to analyze the watch buffer, and generate alert messages. The number of alerts about a suspicious node in a guard node is cumulative over time. It also needs a certain number of guard nodes to report the malice of a node before responding to and isolating a malicious node. Such measures mitigate the faults in wireless networks due to interference and unstable radio, etc.

# 7.3 Security

Security is another hinged issue for practical applications. The selection of patching monitoring nodes should be able to withstand a hostile attack against itself. We notice that we cannot eliminate the possibility of selecting malicious nodes, but we can manage to have the malicious nodes without higher possibility to become a patching monitoring node. The key issue is to validate the monitoring degree of a node which itself claims to have. This can be disposed by some cryptographic mechanisms, for example, authenticate the neighbor relation of a node.

In this paper, we mainly study edge self-monitoring from an algorithmic view. We can consider accommodating some security-specific constraints in our algorithms. For example, each node can be associated with a trust value in the reputation-based system [6], [11]. The trust value of node can be used as a weight of node selection. One node with a higher trust value has large weight and more chance to be selected. As we mention, the MPMSP can be extended to the case that each vertex has a nonnegative weight. We can also add the trust value or other security-specific factors into the node weight, and extend the algorithms in this work into its weighted version.

# 8 CONCLUSIONS

We address the issue of the optimal topology integrated with self-monitoring capability to meet the local monitoring requirements. We present a formal study on the problem of adding the minimum number of monitoring nodes into a large-scale sensor network, and show that the problem is NP-complete. We also provide the upper bounds on the approximation ratio in a centralized scenario. We further design two distributed algorithms with provable approximation ratio and time complexity guarantee. Through comprehensive simulations, we present the performance comparison of our distributed algorithms and show that the optimized selection of monitoring nodes can decrease the number of monitoring nodes significantly.

Future work will involve three directions. First, we will design secure node selection protocols to prevent malicious nodes from joining set of patching monitoring nodes and colluding. Second, we will investigate how real radio models affect the selection strategy of monitoring nodes. Third, since the monitoring nodes are selected in determinate approaches, an adversary might be able to determine which nodes to attack, so as to control or compromise a section of the sensor network. Hence, we may want to insert more uncertainty during selections.

# ACKNOWLEDGMENTS

The work is supported in part by the NSFC/RGC Joint Research Scheme N\_HKUST 602/08, the National Basic Research Program of China (973 Program) under grants No. 2006CB303000, 2010CB328000, and 2011CB302705, the National High Technology Research and Development Program of China (863 Program) under grants No. 2002AA1Z2101, No. 2007AA01Z177, and No. 2007AA01Z180, and NSFC under grants No. 60621003, No. 90718040, No. 60736016, No. 60702046 and No. 60832005. The authors are grateful for a variety of constructive comments from the anonymous reviewers. The first author would like to thank Yongan Wu, Shanshan Li, and Weifang Cheng for the valuable discussions in the early stage of this work. A preliminary version of this paper was presented at the ACM MobiHoc, 2008.

# REFERENCES

[1] H. Chan and A. Perrig, “Security and Privacy in Sensor Networks,” Computer, vol. 36, no. 10, pp. 103-105, Oct. 2003.   
[2] V. Giruka, M. Singhal, J. Royalty, and S. Varanasi, “Security in Wireless Sensor Networks,” Wiley Wireless Comm. and Mobile Computing, vol. 8, pp. 1-24, 2008.

[3] I. Khalil, S. Bagchi, and C. Nina-Rotaru, “DICAS: Detection, Diagnosis and Isolation of Control Attacks in Sensor Networks,” Proc. IEEE First Int’l Conf. Security and Privacy for Emerging Areas in Comm. Networks (SecureComm), 2005.   
[4] I. Khalil, S. Bagchi, and N. Shroff, “LITEWORP: A Lightweight Countermeasure for the Wormhole Attack in Multihop Wireless Networks,” Proc. IEEE/IFIP Int’l Conf. Dependable Systems and Networks (DSN), 2005.   
[5] S.-B. Lee and Y.-H. Choi, “A Resilient Packet-Forwarding Scheme against Maliciously Packet-Dropping Nodes in Sensor Networks,” Proc. ACM Workshop Security of Ad Hoc and Sensor Networks (SASN), 2006.   
[6] S. Ganeriwal, L.K. Balzano, and M.B. Srivastava, “Reputation-Based Framework for High Integrity Sensor Networks,” ACM Trans. Sensor Networks, vol. 4, 2008.   
[7] K. Liu, M. Li, Y. Liu, M. Li, Z. Guo, and F. Hong, “Passive Diagnosis for Wireless Sensor Networks,” Proc. ACM Conf. Embedded Networked Sensor Systems (SenSys), 2008.   
[8] C. Karlof and D. Wagner, “Secure Routing in Wireless Sensor Networks: Attacks and Countermeasures,” Elsevier Ad Hoc Networks, vol. 1, pp. 293-315, 2003.   
[9] D. Dong, Y. Liu, and X. Liao, “Self-Monitoring for Sensor Networks,” Proc. ACM MobiHoc, 2008.   
[10] S. Marti, T.J. Giuli, K. Lai, and M. Baker, “Mitigating Routing Misbehavior in Mobile Ad Hoc Networks,” Proc. ACM MobiCom, 2000.   
[11] S. Buchegger and J.-Y.L. Boudec, “Performance Analysis of the CONFIDANT Protocol: Cooperation of Nodes Fairness in Distributed Ad-Hoc Networks,” Proc. ACM MobiHoc, 2002.   
[12] I. Khalil, S. Bagchi, and N.B. Shroff, “SLAM: Sleep-Wake Aware Local Monitoring in Sensor Networks,” Proc. IEEE/IFIP Conf. Dependable Systems and Networks (DSN), 2007.   
[13] C. Hsin and M. Liu, “Self-Monitoring of Wireless Sensor Networks,” Elsevier Computer Comm., vol. 29, pp. 462-476, 2006.   
[14] D. Wang, Q. Zhang, and J. Liu, “The Self-Protection Problem in Wireless Sensor Networks,” ACM Trans. Sensor Networks, vol. 3, 2007.   
[15] Y. Wang, X.Y. Li, and Q. Zhang, “Efficient Algorithms for p-Self-Protection Problem in Static Wireless Sensor Networks,” IEEE Trans. Parallel and Distributed Systems, vol. 19, no. 10, pp. 1426- 1438, Oct. 2008.   
[16] J. Wu, M. Cardei, F. Dai, and S. Yang, “Extended Dominating Set and Its Applications in Ad Hoc Networks Using Cooperative Communication,” IEEE Trans. Parallel and Distributed Systems, vol. 17, no. 8, pp. 851-864, Aug. 2006.   
[17] X.Y. Li, “Multicast Capacity of Wireless Ad Hoc Networks,” IEEE/ ACM Trans. Networking, vol. 17, no. 3, pp. 950-961, June 2009.   
[18] F. Kuhn, T. Moscibroda, T. Nieberg, and R. Wattenhofer, “Local Approximation Schemes for Ad Hoc and Sensor Networks,” Proc ACM Workshop Discrete Algorithms and Methods for MOBILE Computing and Comm. (DIALM-POMC), 2005.   
[19] R. Tamassia and I.G. Tollis, “Planar Grid Embedding in Linear Time,” IEEE Trans. Circuits and Systems, vol. 36, no. 9, pp. 1230- 1234, Sept. 1989.   
[20] A. Schrijver, Combinatorial Optimization—Polyhedra and Efficiency (Part III). Springer, 2003.   
[21] D.S. Hochbaum and W. Maass, “Approximation Schemes for Covering and Packing Problems,” J. ACM, vol. 32, pp. 130-136, 1985.   
[22] D.S. Hochbaum, Approximation Algorithms for NP-Hard Problems, Chapter 3. PWS Publishing Company, 1997.   
[23] P.J. Wan, K.M. Alzoubi, and O. Frieder, “Distributed Construction of Connected Dominating Set in Wireless Ad Hoc Networks,” ACM/Springer Mobile Networks and Applications, vol. 9, pp. 141-149, 2004.   
[24] B. Liang and Z.J. Haas, “Virtual Backbone Generation and Maintenance in Ad Hoc Network Mobility Management,” Proc. IEEE INFOCOM, 2000.   
[25] Y. Wang, W. Wang, and X. Li, “Efficient Distributed Low-Cost Backbone Formation for Wireless Networks,” IEEE Trans. Parallel and Distributed Systems, vol. 17, no. 7, pp. 681-693, July 2006.

![](images/968af0c62e318e513a7b79a5cc04936ac74cd84abb30ac1ca44af3d6a2689742.jpg)



Dezun Dong received the BS and MS degrees in 2002 and 2004, respectively, from the National University of Defense Technology (NUDT), China, where he is currently working toward the PhD degree at the School of Computer. He is visiting in the Department of Computer Science and Engineering, Hong Kong University of Science and Technology. His research interests include network security, wireless ad hoc, and sensor networks. He is a

student member of the IEEE Computer Society.

![](images/370ed77103fc899ef9e21bad966313a1279cc012dac8e80588ef73ce61ef14ef.jpg)



Xiangke Liao received the BS degree in computer science from Tsinghua University in 1985, and the MS degree in 1988 from the National University of Defense Technology (NUDT), China, where he is now a professor and the dean in the School of Computer. His research interests include parallel and distributed computing, high-performance computer systems, operating system, and networked embedded system.

![](images/78832917bd4161040d878c925895735fc582e9c4bf941843924f8f1d81e142ed.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, and the MS and PhD degrees in computer science and engineering from Michigan State University, in 2003 and 2004, respectively. He is now a professor at TNLIST, School of Software, Tsinghua University, as well as a faculty member with the Department of Computer Science and Engineering at the Hong Kong University of Science and Technology. His

research interests include wireless sensor network, peer-to-peer computing, and pervasive computing. He is a senior member of the IEEE Computer Society and an ACM Distinguished Speaker.

![](images/f2f0c03fa080e5aef553a99303a9d6bd79734ac07880ddae4dce89d62d374877.jpg)



Changxiang Shen received the BS degree from Zhejiang University, China, in 1965. Currently, he is a professor in the Naval Institute of Computing Technology, Beijing, and an adjunct professor in the School of Computer, National University of Defense Technology, China. He is a member of Chinese Academy of Engineering. His research interests include information security, trusted computing, and operating system.

![](images/37cb9c4bc52f494a50a61e5ff7f14becd13a6e7806ede540c5ed1a6d635f6d49.jpg)



Xinbing Wang (M’06) received the BS degree (with hons) from the Department of Automation, Shanghai Jiaotong University, China, in 1998, the MS degree from the Department of Computer Science and Technology, Tsinghua University, Beijing, China, in 2001, and the PhD degree, major from the Department of Electrical and Computer Engineering and minor from the Department of Mathematics, North Carolina State University, Raleigh, in 2006. Currently,

he is a faculty member in the Department of Electronic Engineering, Shanghai Jiaotong University, China. His research interests include resource allocation and management in mobile and wireless networks, TCP asymptotics analysis, wireless capacity, cross-layer call admission control, asymptotics analysis of hybrid systems, and congestion control over wireless ad hoc and sensor networks. He has been a member of the Technical Program Committees of several conferences including the IEEE ICC 2007, IEEE Globecom 2007, IEEE WCNC 2007, IEEE ICCCN 2007, and IEEE IPCCC 2007. He is a member of the IEEE Computer Society and the ACM.