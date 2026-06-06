# CitySee: Urban $C O _ { 2 }$ Monitoring with Sensors

Xufei Mao∗†, Xin Miao†, Yuan He∗†, Xiang-Yang Li∗‡, and Yunhao Liu∗†

∗ MOE Key Lab for Information System Security, School of Software, TNLIST, Tsinghua University, China

† Department of Computer Science and Engineering, HKUST

‡Computer Science Department, Illinois Institute of Technology, USA

Email: {xufei.mao, yunhao}@greenorbs.com, {miao, heyuan}@cse.ust.hk, xli@cs.iit.edu

Abstract—Motivated by the needs of precise carbon emission measurement and real-time surveillance for $C O _ { 2 }$ management in cities, we present CitySee, a real-time $C O _ { 2 }$ -monitoring system using sensor networks for an urban area (around 100 square kilometers). In order to conduct environment monitoring in a real-time and long-term manner, CitySee has to address the following challenges, including sensor deployment, data collection, data processing, and network management. In this discussion, we mainly focus on the sensor deployment problem so that necessary requirements like connectivity, coverage, data representability are satisfied. We also briefly go through the solutions for the remaining challenges. In CitySee, the sensor deployment problem can be abstracted as a relay node placement problem under hole-constraint. By carefully taking all constraints and real deployment situations into account, we propose efficient and effective approaches and prove that our scheme uses additional relay nodes at most twice of the minimum. We evaluate the performance of our approach through extensive simulations resembling realistic deployment. The results show that our approach outperforms previous strategies. We successfully apply this design into CitySee, a large-scale wireless sensor network consisting of 1096 relay nodes and 100 sensor nodes in Wuxi $\mathbf { C i t y , }$ China.

Index Terms $- C O _ { 2 }$ monitoring, relay nodes placement, wireless sensor networks.

# I. INTRODUCTION

With the worsening of Global Warming, the carbon sequestration and emission issues have attracted serious concern of researchers and specialists all over the world. One of the main causes deteriorating global climate is the overemission of $C O _ { 2 } .$ . Most countries, especially massive energyconsuming countries are required to reduce (or restrict) the emission of $C O _ { 2 }$ in order to slow down the steps of Global Warming. Since arguably more than  of $C O _ { 2 }$ emissions 80%originate in urban areas, which occupy less . of land 2 4%mass globally [11], understanding the relationships between the form and pattern of urban development and the carbon cycle is crucial for estimating future trajectories of greenhouse gas concentrations in the atmosphere and facilitates mitigation of climate change. Hence, accurately measuring the emissions of $C O _ { 2 }$ of the interested (or serious) areas is in great demands, especially for those high $C O _ { 2 }$ emission areas, like industrial regions, densely populated places, and etc.

One of the methods estimating $C O _ { 2 }$ emissions is based on raw material (like fossil oil and coal) consumption, which is widely used by European Environment Agency when it ranks countries with their $C O _ { 2 }$ emissions every year [2]. This is reasonable to some extent but less of accuracy and fairness since different countries or cities have different carbon sequestration abilities, which is the opposite of carbon emissions. Another inference-based carbon sensing technology is adopted to measure $C O _ { 2 }$ fluxes [8]. When a radiation $( \mathrm { e . g . }$ , a thermal infrared radiation) travels through the atmosphere, it can be either absorbed or re-emitted. $C O _ { 2 }$ is one of the gases which are responsible for most of the absorption. Consequently, by measuring the radiation above the atmosphere, $C O _ { 2 }$ fluxes could be inferred. Estimation-based and inference-based methods can satisfy the large-scale and real-time requirements for $C O _ { 2 } .$ -monitoring with the cost of sacrificing accuracy. There are some expensive instruments $( e . g .$ , HD-CO2-S [1]) in the market, which are able to measure the $C O _ { 2 }$ fluxes for a location during a fixed time period. However, it is very hard to use them for long-term measurement of $C O _ { 2 }$ emissions due to the constraints like high cost and requiring electronic power support. Indeed, we still lack effective approaches to measure the carbon emissions of large-scale areas accurately and thoroughly in a real-time and long-term manner.

Fortunately, the combination of sensors with mature technology and small individual wireless node show great potential for us to interact with the physical world. On the one hand, the manufacturing of small and low cost sensors and wireless terminals becomes technically and economically feasible. On the other hand, the technologies (like routing protocols, link scheduling protocols, power consumption) of wireless sensor networks (WSNs) become more and more mature. Large-scale, self-organized WSNs consisting of thousands of individual nodes have been applied in real application scenarios, like GreenOrbs [21] and ExScal [4].

The goal of CitySee is to deploy thousands of wireless sensor nodes in an urban area of Wuxi City, China, such that multi-dimensional data including $C O _ { 2 } .$ , temperature, humidity, light, location, and etc. could be collected in a real-time manner for further analysis. Compared with GreenOrbs [21] in the forest environment, the long-term, large-scale, continuous, and synchronized surveillance of huge measurement in urban area is more difficult due to complex geographical environment. The following four issues should be properly solved for CitySee.

1) Sensor deployment: According to the requirement from ecologists, the wireless nodes equipped with different types of sensors should be placed in interesting points inside the monitoring area such that all collected data are representative. More importantly, some relay nodes will be further inserted such that all individual nodes could form a connected WSN.

![](images/1085dbfd6076b2932d483bb8408bcb2bb7a2af8f11a1ac9ab27e5b2245617037.jpg)



(a) SNs.

![](images/ff9c95bd675acecd288b051c03931717064b70b3871fe66281cc46e1754e7449.jpg)



(b) RNs.   
Fig. 1. Two types of wireless nodes. Each SN is equipped with a $C O _ { 2 }$ sensor and each RN has one temperature/humidity sensor and one light sensor on it.

2) Data collection: An agency should be planted into each sensor node in order to sense the environment, package data and send data back to the sink node (may need nodes to work collaboratively).   
3) Data processing: At the base station, all collected data are recorded, formatted, and displayed.   
4) Network diagnosis management: To keep the entire network run, system administrators needs efficient tools to understand the running status, locate the error if any, and further recover from failures.

In this discussion, we focus more on the first issue: how to deploy a large-scale WSN consisting of different types of nodes into the monitoring area for real-time collection of multi-dimensional environment information in CitySee. Basically, we design two types of nodes equipped with $C O _ { 2 }$ sensors and other type of sensors (e.g., temperature, humidity, and light) respectively. Due to the fact that the sensing operation of a $C O _ { 2 }$ sensor is very energy-consuming, a wireless node equipped with a $C O _ { 2 }$ sensor (abbreviated as SN) does not relay packets for any other nodes while the other type of nodes perform both sensing and relaying operations (abbreviated to RN). Please refer to Fig. 1 for illustration. In addition, some special locations where SNs and RNs have to be placed exactly in the area have been chosen a priori by ecologists to ensure that collected data are representative. At the same time, some locations (e.g., buildings) are strictly prohibited to deploy any node due to physical constraints.

When performing deployment, one major benchmark is the connectivity of the network. The phase one of our Carbon Monitoring Project, GreenOrbs [21], is successfully deployed in the forest, which aims at evaluating carbon sequestration ability (an opposite of carbon emissions). The placement for GreenOrbs which aims at evaluating carbon sequestration ability is easier than that for CitySee since the density of obstacles in forests is generally more uniform than that in cities. Through field measurement of communication links among wireless nodes, we found that there are many “black holes” (e.g., buildings) in the urban area, which can “absorb” the wireless signals by blocking, reflecting, interference, and etc. CitySee, must minimize the total number of RNs for maintaining the connectivity of the deployed network from both economic and applicable concerns after the critical locations of a subset of nodes have been chosen. Our solution should also satisfy the following constraints all the time, 1) a SN does not relay data packets for any other node; 2) some locations are not available for deploying RNs; 3) wireless links should avoid “holes”.

The major contributions of this paper are as follows.

1) We report the design and implementation of CitySee, a large-scale ( SNs and  RNs) and long-term $C O _ { 2 }$ 100 1096monitoring WSN in urban area, Wuxi City, China, which is a complementary project of GreenOrbs.   
2) We propose low-cost sensor deployment strategies with guaranteed performance (within -approximation ratio of 2the optimum) which addresses the sensor deployment problem in CitySee.   
3) To the best of our knowledge, we are the first to define geometric version of Group Steiner Tree with Holes problem, which is very helpful to a rich body of sensor deployment problems by considering both the optimization objectives of sensor deployment problems and realistic deployment constraints.   
4) Performance of our proposed approaches has been extensively evaluated through simulations resembling real deployments.

The rest of the paper is organized as follows. We first review related works in Section II. In Section III, we present our network model and formally define the problems to be studied in this paper. We divide the relay nodes deployment problem into several subproblems and propose solutions to them in Section IV. We examine the performance of our approaches in Section V. The procedure of remaining three steps of CitySee are presented briefly in Section VI. We conclude the work in Section VII.

# II. RELATED WORK

Generally speaking, previous work on relay nodes placement according to connectivity can be classified into two categories, i.e., single-tiered node placement and two-tiered node placement.

Single-tiered placement assumes that both SNs and RNs participate in forwarding packets received from other nodes. Lin and Xue defined it as a Steiner minimum tree with minimum number of Steiner points and bounded edge length problem in [19]. They proved its NP-hardness and proposed a -approximation algorithm based on minimum spanning trees. 5Chen et al. [9] studied the same problem and presented a -approximation solution. In [10], Cheng et al. developed 3a faster -approximation algorithm as well as a randomized 3. -approximation algorithm. Lloyd et al. [23] assumed relay 2 5nodes may have a larger communication range than sensor nodes and presented a -approximation algorithm.

In two-tiered node placement, only RNs are able to forward packets received from other nodes while SNs only send packets generated by themselves to some RN(s). In [17], Hao et al. designed an O D  n -approximation algorithm ( log )for -connectivity and distinct communication ranges, where 2n is the network size and D depends on network diameter. Based on the assumption that relay nodes’ communication range is at least four times as large as sensor nodes’ communication range, Tang et al. [27] provided -approximation 6and . -approximation algorithms for -connectivity and - 4 5 1 2connectivity cases respectively. Further results can also be found in [23]. Our work belongs to two-tiered node placement problem with the constraint that there is a set of unavailable locations for deploying RNs.

A bunch of work studied sensor deployment problem from other points of view. For example, [5] proposed a strip-based deployment pattern ensuring both coverage and 2-connectivity. [14] considered the joint optimization of sensor placement and topology construction subject to constraints on the distortion of reconstructed sensing data and network lifetime. In addition, [24] presented a random deployment approach to achieve minimum total energy. Some other works [3], [6] etc. mainly studied data collection problem using a WSN with mobile sink (data mule). Their work focused on data transmission related strategies such as to improve the throughput, reduce the energy consumption and delay. The work in [29] concentrated on capacity and delay tradeoffs for the data collection (convergecast) scenario. [7], [30] studied sensor deployment problem from coverage aspect. In monitoring applications, it is often required that each point of the interesting area is covered by at least  or k sensors.

1Compared to the previous work, the main novelty of our problem is that we study constrained two-tiered relay nodes placement problem to meet connectivity requirement. We consider the joint optimization of sensor placement in an urban area with complicated physical constraints. The large area of required monitored region, complicated physical constraints and the consequent scale of wireless sensor networks render our problem more challenging.

# III. PROBLEM FORMULATION

# A. Network Model

Given two types of wireless sensor nodes RNs and SNs with same transmission range r, we assume that two location (point) sets $P S ~ = ~ \{ p _ { 1 } , p _ { 2 } , \cdot \cdot \cdot ~ , p _ { m } \}$ and $L S ~ = ~ \{ l _ { 1 } , l _ { 2 } , \cdot \cdot \cdot ~ , l _ { n } \} )$ = =where SNs and RNs should be placed are chosen a priori in the two-dimensional map of the deployment region . For Ωsimplicity, we use u to denote the location of the node u if no confusion arises. We use $d ( u , v )$ to denote the Euclidean ( )distance between two points (nodes) u and v in the plane and use $d ( u \sim v )$ to indicate the Euclidean distance of the path ( )connecting nodes u and v. In addition, there are some places in reality where we cannot deploy wireless nodes directly due to physical constraints, e.g., some buildings, we call these kind of places holes in the map. Assume there are totally p holes in region , saying in set $\mathcal { H } = \{ h _ { 1 } , h _ { 2 } , \cdot \cdot \cdot , h _ { p } \}$ . We further assume that each hole $h _ { i }$ is a polygon with constant number of edges and the shapes and positions of all holes in region Ωare known. Since a wireless link between two wireless nodes either is unavailable or has very low transmission rate when there are some explict obstacles between them, we consider that any wireless link going into or across a hole is unavailable.

Regulation 1: A wireless link from u to v exists iff 1) v falls into the transmission range of u; 2) v is a RN; and 3) the line from u to v does not go into or across any hole.

We use the following standard graph theoretic notations: for a graph G, V G denotes the vertex set of G and E G ( ) ( )denotes the edge set of G. Since we would like to deploy sensor nodes on some area with holes, from now on, when we say something under “hole-constraint”, we mean something avoids the holes on the deploy area.

# B. Questions Studied

We give the formal definition of the question studied in this paper.

Question 1: Given the two-dimensional map of deployment region  with a known hole set $\mathcal { H } = \{ h _ { 1 } , h _ { 2 } , \cdot \cdot \cdot , h _ { p } \}$ , assuming that m SNs and n RNs have already been placed at location sets $P S = \{ p _ { 1 } , p _ { 2 } , \cdot \cdot \cdot , p _ { m } \}$ and $L S = \{ l _ { 1 } , l _ { 2 } , \cdots , l _ { n } \}$ = =respectively, the question is how to further deploy minimum number of RNs in  such that all deployed SNs and RNs Ωconstruct a connected WSN following Regulation 1. Here, “connected” means that any SN can send packets to at least one RN and any two RNs can reach each other through some path using RNs only.

After deploying both SNs and RNs following the locations sets P S and LS, there may be some isolated components. In order to using fewer RNs to connect these isolated components into a connected WSN, we need to find some shortest paths under hole-constraint to connect at least one node from each component. Hence, our problem is transferred into geometric version of Group Steiner Tree problem [16] under holeconstraint (defined in Sub-Question 2) by assuming that nodes belonging to the same component form a group. Then, we deploy RNs along the shortest paths we got, we finish our work. However, this may be not always the truth since a SN will not relay data packet for any other node such that a regularly defined component we got after deploying SNs and RNs following P S and LS respectively is actually not connected. For instance, case (a), (b) and (c) in Fig. 2 are not “legally” connected indeed since Regulation 1 is broken.

Clearly, the precondition of solving our problem using aforementioned idea is to find all self-connected components following Regulation 1. Next, we split Question 1 into two sub-questions. The first one is to find all legal components (defined as Sub-Question 1) and the other one is geometric Group Steiner Tree with Holes problem (defined as Sub-Question 2). Here, the output of Sub-Question 1 will be the input of Sub-Question 2.

Sub-Question 1: Given the two-dimensional deployment region  with known hole set $\mathcal { H } = \{ h _ { 1 } , h _ { 2 } , \cdot \cdot \cdot , h _ { p } \}$ , assum-Ω =ing that m SNs and n RNs have already been placed at location sets $P S ~ = ~ \{ p _ { 1 } , p _ { 2 } , \cdot \cdot \cdot , p _ { m } \}$ and $L S ~ = ~ \{ l _ { 1 } , l _ { 2 } , · · · ~ , l _ { n } \}$ = =respectively, the question is how to divide all deployed nodes into self-connected components where each wireless link inside a component satisfies Regulation 1.

![](images/4371b8c16807adf63aca614f2d26b39bcbca808360cecda91ddc17301de8ec1d.jpg)



Fig. 2. (a), (b) and (c) are illegal components and case (d) is legal. Black and white nodes denote SNs and RNs respectively with transmission range r. The solid line segments denote communication links between wireless nodes while dotted line segments are not considered as valid communication links in our case.

Sub-Question 2: Geometric Group Steiner Tree with Holes (G-GSTWH): Given the two-dimensional map of deployment region  with known hole set $\begin{array} { r l } { { \mathcal { H } } } & { { } = } \end{array}$ $\{ h _ { 1 } , h _ { 2 } , \cdots , h _ { p } \}$ Ω =, assuming that there is a collection of groups $G _ { 1 } , G _ { 2 } , \cdots , G _ { d }$ where each group contains a bunch of nodes and $G _ { i } \cap G _ { j } = \phi , 1 \leq i \neq j \leq d ,$ , the problem is to construct a = 1 =minimum edge-weighted (Euclidean distance) tree under holeconstraint, which spans at least one node from each group.

Obviously, if we find the solution of G-GSTWH, a Steiner tree under hole-constraint connecting all groups, we can replace edges of this Steiner tree with the connected communication paths consisting of RNs. Note that, some component $S _ { i } ~ \in ~ \mathcal { S }$ may be not considered in Sub-Question 2 if $S _ { i }$ contains one SN only. For each isolated SN, finding a shortest path under hole-constraint connecting it to its closest RN, we’ve done. The reason for us to do this is because there are few isolated SNs in our case since a location in $P S$ is always surrounded by several locations in LS for $C O _ { 2 }$ accurate fluxes measurement purpose. When there are large number of isolated SNs, the question comes to terminal steiner tree problem, which was solved in [12].

# IV. SOLUTIONS

The main idea to solve Sub-Question 1 is as follows. Basically, what we need is to find all components under holeconstraint among all deployed RNs whose locations correspond to LS without considering any SN. Then we obtain all legal components by adding each SN to some resultant component obeying Regulation 1 if possible. It is not difficult to show that we can obtain all components in $O ( n ^ { 2 } p + m )$ time ( + )where m and n are cardinalities of P S and LS respectively, p is the number of holes in region . (Please refer to [25] for detailed proof.)

After we obtain all legal components (assuming in set $\mathcal { S } )$ , the next step is to deploy minimum number of RNs to connect all pre-deployed SNs and RNs. Assuming that the component set we got is set $\mathcal { S } ~ = ~ \{ S _ { 1 } , S _ { 2 } , \cdot \cdot \cdot ~ , S _ { d } \}$ where $S _ { i } = ( V ( S _ { i } ) , E ( S _ { i } ) )$ is the $i ^ { t h }$ =component. Here, $V ( S _ { i } )$ con-= ( ( ) ( ))tains all sensor nodes belonging to component $S _ { i }$ (and $E ( S _ { i } )$ ( )contains all possible links (obeying Regulation 1) among nodes in $V ( S _ { i } )$ . For instance, in Fig. 3(a), the shadowed area are ( )obstacles (buildings in our case) where we cannot deploy sensor nodes (at least in two-dimensional space). In addition, two sensor nodes within the transmission range of each other may not communicate or with very low transmission ratio due to holes so that this kind of links are unavailable.

Next, we obtain a new group set $\mathcal { G } = \{ G _ { 1 } , G _ { 2 } , \cdot \cdot \cdot , G _ { e } \}$ =by removing all SNs and corresponding edges, i.e., $G _ { i } \ =$ $( V ( G _ { i } ) , E ( G _ { i } ) ) , V ( G _ { i } ) = V ( S _ { i } ) \ \backslash \quad$ {all SNs} and $E ( G _ { i } ) =$ $E ( C _ { i } ) ~ \backslash$ ( )) ( ) = ( ) ( ) = {all edges incident on SNs}. Clearly, if we are able ( )to find a feasible solution to connect all nodes in group set $\mathscr { G } _ { ; }$ , the same solution can be applied to connect all nodes in component set $\mathcal { S }$ since no SNs will be chosen as the bridge point connecting two components.

Now we are ready to solve G-GSTWH problem (Sub-Question 2) using group set $\mathcal { G } \{ g _ { 1 } , g _ { 2 } , \cdots , g _ { k } \}$ . As we have mentioned before, in CitySee, the number of isolated components containing single $C O _ { 2 }$ are very small since any required location for a SN is always close to some required locations for several RNs in order to improve the accuracy of computing $C O _ { 2 }$ fluxes in the air. From now on, we concentrate on the case that the number of isolated components containing single $C O _ { 2 }$ node is within small fraction of all $C O _ { 2 }$ nodes.

Our main idea is as follows. We first use method in [18] to find the shortest path under hole-constraint between each pair of nodes u and v in different groups, i.e., $u \in G _ { i } , v \in G _ { j }$ where $i \neq j$ . Here, if the shortest path under hole-constraint =connecting u and v is a series of continuous line segments (starting from u and ending at v), the Euclidean length of shortest path under hole-constraint between u and v is the summation of Euclidean length of each line segment. Next, we consider each group as a virtual supper node and the shortest path under hole-constraint connecting two virtual supper nodes is defined as the shortest path connecting two sensor nodes from each of two virtual supper nodes (groups), $i . e .$ , the Euclidean length of the shortest path connecting two virtual supper nodes $G _ { i }$ and $G _ { j }$ is $d ( G _ { i } \sim G _ { j } ) = \operatorname * { m i n } \{ d ( u , v )$ $\forall u \ \in \ G _ { i } , \forall v \ \in \ G _ { j } \}$ ( ) = min ( ) :. Hence, we have a complete graph $G _ { g r p } ~ = ~ ( V ( G _ { g r p } ) , \dot { E } ( G _ { g r p } ) )$ where $V ( G _ { g r p } )$ contains all = ( ( ) (virtual supper nodes and $\bar { ( G _ { i } , G _ { j } ) } \in E ( G _ { g r p } )$ )is the shortest path connecting $( G _ { i } , G _ { j } )$ ( ) ( )under hole-constraint (Fig. 3(b)).

( )By using a minimum Euclidean spanning tree (MST) method $( e . g .$ , Prim’s algorithm), we can find a MST to connect all groups. Next, we replace each edge of resultant MST with original continuous line segments. Based on all resultant paths(line segments) connecting all components, we deploy more RNs along these paths where each pair of adjacent nodes are within r. Hence, we have a connected WSN. The details of our algorithm please refer to Algorithm 1.

Lemma 1: The Algorithm 1 has a -approximation ratio of 2the optimum of Sub-Question 2 with time complexity $O ( n +$ ( +m  p2  n  p2  m where m and n are the cardinalities + log + log )of P S and LS respectively, p is the number of holes.

Proof: Given group set $\mathcal { G } ,$ in which each group is a virtual supper node, we show that a MST under hole-constraint spanning all virtual supper node has total length as most twice

![](images/7c92e78a379f097b4a7f90eac61d7431808ede8cab1ecbdaf987aee6f4db0bc2.jpg)



(a)

![](images/c6d8e93529235cd5891f3b260d71a5f2fd2bd728ea0acff18045a3b5f3e51124.jpg)



![](images/0b15a5126680fc11ec515b94a1fdfd04afe85d640ae6b905d009792faec3af5b.jpg)



![](images/5f2ee304652822b98e16e8d0d64a0549fa3bb7ff96e573f57abd8c2df98b40f6.jpg)



(d)   
Fig. 3. (a) Some legal components in the original graph. White nodes and Black nodes denote RNs and SNs respectively. All nodes cycled by dotted curve belong to the same component. The dotted red lines show some shortest path connecting RNs in different components. (b) Complete graph of all virtual super nodes denoting by hexagons. (c) Euler tour spanning all virtual super nodes. (d) Hamiltonian cycle spanning all virtual super nodes. The shadow areas are holes and smaller hexagons indicate steiner nodes.

# Algorithm 1 Shortest Paths Connecting All Components

Input: Given group set $\mathcal { G } = \{ G _ { 1 } , G _ { 2 } , \cdot \cdot \cdot , G _ { d } \}$ and map with known hole set $\mathcal { H }$

Output: Shortest Paths connecting all groups under holeconstraint.

1: for each pair of nodes u and v where $u \in G _ { i } , v \in G _ { j }$ $1 \leq i \neq j \leq d$ do   
2: =Use method in [18] to compute the shortest Euclidean path between u and v under hole-constraint   
3: Assuming each group in set $\mathcal { G }$ is a virtual supper node   
4: for Each pair of virtual supper nodes $G _ { i }$ and $G _ { j }$ in $\mathcal { G }$ where $i \neq j$ do   
5: =Compute the minimum Euclidean path under holeconstraint between $G _ { i }$ and $G _ { j } , i . e . , d ( G _ { i } \sim G _ { j } ) =$ min $\{ d ( u , v ) : \forall u \in G _ { i } , \forall v \in \bar { G } _ { j } \}$   
min ( ) :6: Using Prim’s algorithm to find a MST under holeconstraint to connect all virtual supper nodes.   
7: for Each component which contains one single $C O _ { 2 }$ node only do   
8: Find a shortest path under hole-constraint connecting itself to the nearest RNs (maybe use some new deployed RNs).

of the optimum, i.e., the total length of an minimum edgeweighted group Stein Tree spanning all virtual nodes.

Assuming the optimum Steiner tree under hole-constraint with the minimum total length has cost OP T . By doubling its edges we obtain an Eulerian graph connecting all virtual super nodes and, possibly, some Steiner vertices. Next, we find an Euler tour of this graph, for instance by traversing the edges in depth first search order, see Fig. 3(c) for illustration. Clearly, the cost of this Euler tour is OP T . Then, we obtain a 2Hamiltonian cycle on the vertices (all super nodes and steiner nodes) by traversing the Euler tour and“short-cutting” Steiner vertices and previously visited vertices (all super nodes). By removing an edge from this cycle, we obtain a path that spans G . Noticing that, when we short-cut Steiner vertices during traversing, we use the shortest path under hole-constraint to connect two vertices. For example, in Fig. 3(d), for two virtual supper nodes u and v, the OP T solution use two line segments u, t and t, v , which will be replaced by $( u \sim v )$ (the shortest path connecting u and v) in the Hamiltonian cycle. Since $( u \sim v )$ is the shortest path connecting u and v under ( )hole-constraint, the length of $( u \sim t \sim v )$ is no smaller than $( u \sim v )$ ( ), then the triangle inequality still holds such that the ( )path spanning $\mathcal { S }$ has cost at most $2 \times O P T$ . Remembering 2that this path under hole-constraint is also a spanning tree on ${ \mathcal { S } } ,$ , the MST under hole-constraint has cost at most $2 \times O P T$ .

2Next, we prove the time complexity. First, the cardinality of component set $\mathcal { S }$ and resultant group set $\mathcal { G }$ is at most n. Next, computing the shortest path between each pair of nodes in different groups takes $O ( n + p ^ { 2 } \log n )$ time [18]. Clearly, ( + log )computing the shortest distance under hole-constraint between each pair of virtual super nodes will take $O ( n ^ { 2 } )$ time since we ( )at most have n groups. Using Prim’s algorithm to find a MST among all groups takes us $O ( n ^ { 2 } \log { n } )$ time since the number ( log )of edges of the complete graph among all groups is $O ( n ^ { 2 } )$ . Finally, to find a shortest path connecting each isolate $C O _ { 2 }$ to its nearest RN is take $O ( m + p ^ { 2 } \log m )$ by [18]. Hence, the total running time is $O ( n + m + p ^ { 2 } \log n + p ^ { 2 } \log m )$ .

# V. EXPERIMENTS

# A. Deployment of RNs in CitySee

We successfully apply the solution for RNs replacement to CitySee using the G-GSTWH-based algorithm. In CitySee, location sets P S and LS with cardinality  and respectively are given a priori in the required deployment region. By the G-GSTWH-based algorithm, we further deploy RNs to connect all SNs and RNs whose locations are 696corresponding to P S and LS. We deploy both types of sensor nodes in trees and telegraph poles around . meters Euclidean 2 5distance to the ground. See Fig. 4 for illustration.

Part of deployment area and the resulting topology (obtained from real data trace) is shown in Fig. 5, from which we can see that the impact on valid wireless links by holes are obvious. For instance, we have some valid wireless links with Euclidean distance around  meters in some open territories while 150some nodes do not construct valid links even they are close enough due to “holes”.

# B. Simulations

We conduct extensive simulations to verify the efficiency of our approaches. Besides the main G-GSTWH based algorithm, we also implement two baseline algorithms Simple MST-based and Random-based. Simple MST-based strategy first places a RN at each location in P S such that every SN has at least one RN (at the same location) to help to relay data packets. It then constructs a minimum spanning tree under hole-constraint spanning all RNs whose locations are corresponding to the P S and LS sets. More RNs are further deployed along edges (of the MST) with length larger than r. Random-based strategy randomly sprays RNs into the monitored area  until each ΩSN in P S and each RN in LS are able to find a path to the sink, which consists of RNs only. We implement all three algorithms in C  and all simulations are performed in the + +same software environment on a Pentium R 2.7GHz machine.

![](images/c56ba94baffb2a4bd199d3cca5379240706721c544ecd8a23e720ff00b340891.jpg)



Fig. 4. RNs and SNs hanged on telegraph poles and trees.

![](images/7f1bbcc5c6e1193e7fda3efc8c54138728177115f6f83aa1aade22a757057895.jpg)



Fig. 5. Partial deployment area and the resultant topology (a snapshot of real data trace). Red nodes and yellow nodes denotes SNs and RNs respectively.

For all test cases, we first randomly and uniformly generate a hole set in a rectangle region with area of  meters 5000×  meters. Then, the location sets P S and LS are 4000generated in this region without any hole i.i.d. After that, we investigate the number of RNs required for different algorithms by adjusting five parameters: (i) m: cardinality of location set P S; (ii) n: cardinality of location set LS; (iii) r: transmission range of a sensor node; (iv) p: number of holes; and (v) the size of holes. Unless specifically mentioned, the default values of parameters are shown in the Table I.

For each set of parameters, we run the simulation for 10times. We do not list the results for random-based algorithms in charts since the average performance is almost  times worse than those of the other two algorithms. We concentrate on comparing G-GSTWH-based algorithm with simple MST-

TABLE I DEFAULT VALUES OF SIMULATION PARAMETERS. 

<table><tr><td>Parameter</td><td>Default Values</td></tr><tr><td>Deployment Area</td><td>5000 (m) × 4000 (m)</td></tr><tr><td>Transmission Range</td><td>100 (m) for all nodes</td></tr><tr><td>Size of Holes</td><td>100 (m) × 80 (m)</td></tr><tr><td>p</td><td>50, randomly deployed</td></tr><tr><td>m</td><td>100, randomly deployed</td></tr><tr><td>n</td><td>500, randomly deployed</td></tr></table>

![](images/2443d01ba664dfe8e6db250abdb85cbc3b8b8c1d093cb963eaf4ca76ee168611.jpg)



(a) m is variant.

![](images/c7df5671c6844ef23219113f23a982529314b0a3ef272efebdea25128ba925c1.jpg)



(b) n is variant.   
Fig. 6. The simulation results when we adjust m, n respectively where fixing other parameters. The size of a hole size is 100 80.

based algorithm. For different test cases, G-GSTWH-based algorithm has better performance (gain from  to ) than that of simple MST-based algorithm.

# C. Impact of SN Density and RN Density

In the first set of simulation, we increase m (the number of pre-deployed SNs) from  to  with step  while 100 600 100other parameters use default values. As we can see from Fig. 6(a), the G-GSTWH-based algorithm outperforms single MSTbased algorithm. Although the total number of new deployed RNs for two algorithms increases with the increment of m, the increment trend of G-GSTWH-based algorithm is slower.

In the second set of simulation, we increase n from  to 500 with step  while fixing other parameters. An interesting 800 50phenomena is that when the number of pre-deployed RNs is larger than , the total number of needed RNs for the G-600GSTWH-based algorithm decreases while that of simple MSTbased algorithm continues to increase. We analyze the reason and realize that the number of “legal” components obtained by our algorithm is stable in this case such that the larger n is, the closer components are, which causes different trends of two algorithms with the increment of n. Please refer to Fig. 6(b) for illustration.

# D. Impact of transmission range r and the number of holes p

In the third set of experiment, we first increase r from 40to  with step  while other parameters use default values. 100 10The results for both algorithms are shown in Fig. 7(a), the decreasing trend of G-GSTWH-based algorithm is faster that of simple MST-based algorithm. In order to verify the impact caused by the number of holes, we run all algorithms by increasing the p from  to  with step . Surprisingly, the total number of new deployed RNs only has slight increment (Fig. 7(b)). We conjecture that the impact of scaling p becomes smaller when r is close to the edge length of holes. Actually, this is verified by the simulation results later.

![](images/f31ef5d1aee3b8a5c1e7dfc5aa0673ea20e09bcd4bbcbaa9aae531d593db0b6f.jpg)



(a) r is variant.

![](images/3b803db81d8107771aeaaec52a5ff93082d1736ce7f98b8bcf12594e2d04aeff.jpg)



(b) p is variant.

Fig. 7. The simulation results when we adjust r, p respectively where fixing other parameters.   
![](images/5d9d54712508aef404767bdaba13860a483625e30e20d87fa3c920c3728b60dc.jpg)



(a) area scales.

![](images/30b47bc3e784656396e561e852e25dea4656f815f27247e427bbbd31d6e678fe.jpg)



(b) p scales.   
Fig. 8. # of nodes needed when system scales.

# E. Scalability

In the forth set of simulation, we scale both the area of deployment region and the number of holes p while fixing other parameters. We adjust the area of deployment region from  to  square kilometers and vary the number 20 10240of holes from  to  while keeping the density of m, n 20 100unchanged. For all these test cases, we randomly generate the shape (length and width) of holes. Both results shown in Fig. 8 and Fig. 9 indicate that for the G-GSTWH algorithm, when the transmission range of sensor nodes is around the edge length of holes, the increment of number of holes does small impact on the scalability. This is note true for the simple MST-based algorithm.

# VI. RECENT ADVANCES

# A. Hardware and Software

The hardware platform in CitySee is based on TelosB. Both SN and RN use MSP430F1611 processor and CC2420 radio such that they are able to exchange data with each other using ZigBee protocol in . GHz. In addition, each SN is equipped with $C O _ { 2 }$ 2 4sensor while every RN has temperature/humidity sensor and light sensor on it. All nodes are encapsulated with industrial grade design in order to adapt to outdoor environment.

We develop software for different types of sensor nodes on top of TinyOS . . , which consists of the following major components. First, we implement the link estimation component using the four bit link estimation method [13] to regularly maintain a neighbor table. Second, we use the default Low Power Listening MAC protocol of TinyOS to reduce the energy consumption. Third, the multi-hop routing component is implemented based on the CTP [15] protocol for data collection.

Fourth, we apply the Drip protocol [28] to disseminate key system parameters in terms of the dissemination component, such as transmission power, sampling frequency, duty cycle and etc. In CitySee, a node is programed to sample the environment data according to different types of sensor in every  minutes, and then sends the data packet to the sink 10node through one- or multi-hops. In addition, a SN drops any data packet from other SNs or RNs.

# B. Data Collection

Collection Tree Protocol CTP [15] is adopted for multi-hop sensing data collection. We collect three types of data packets, each of which is responsible for different types of information. The $C _ { 1 }$ type packet contains two types of information: (1) sensing data, including temperature, humidity, light, or $C O _ { 2 }$ concentration; and (2) routing information, including path-ETX [15] from the original packet-source to the sink node. Thus, we are able to obtain the complete routing path of any packet by piggybacking these information into sensed data. The $C _ { 2 }$ type of packet records local information for each sensor node. Typically, a $C _ { 2 }$ contains the routing table including IDs and RSSI values from its neighbors, the link-ETX estimation value of links to its neighbors. A type $C _ { 3 }$ packet contains more detailed information inside a single wireless node. For instance, the CPU counter records the accumulated task execution time, the radio counter records the accumulated radio-on-time, the transmit counter records the accumulated number of transmitted packets, the receive counter records the accumulated number of received packets, and the loop counter records the accumulated number of detected loops.

In Fig. 10, each individual node is described as a circle whose area indicates the number of packets it has transmitted for the last minutes, and all used wireless links are shown 10as well. Figure 11 displays the accumulated number of tasks each wireless node has executed in a D format based on 3the physical topology of the entire wireless sensor network. In CitySee, the traffic load of wireless sensor nodes with different roles (e.g., relay nodes, sensor nodes) are quite different depending on their physical environment and routing protocols. For example, the number of tasks executed by some node closed to the sink node could be up to  times in minutes while around $\textstyle { \frac { 1 } { 4 } }$ 8742 10of wireless nodes have the average number  only.

# C. Data Processing

We have collected over GB data traces from wireless sensor nodes including all environment-related data for the purpose of $C O _ { 2 }$ emission analysis and network status-related data for the purpose of network management and diagnosis. Combining all three types of data packets, we construct the entire network at the base station using the real map. The D geometric location of each node is obtained when it was deployed. Figure 12 is the snapshot (obtained from real data trace) of CitySee, in which white nodes denote wireless sensor nodes and the rectangles indicate the packets in the air. All links shown are the active links of last  minutes. 10The network diameter of the deployed network by hop count reaches nearly  and the longest hop distance observed in 35CitySee is  hops. In CitySee, the radio duty cycle is . 20 4%Upon all collected data, we design and implement visualization interfaces to depict the changing of environment. For instance, Fig. 13 shows the contour map of $C O _ { 2 }$ concentration in the monitored area, in which the darker the color is, the higher $C O _ { 2 }$ concentration is.

![](images/cafdf30f5501c2b60cf528a3b780ea352c51a1fd11f15045bacd9831d20fd561.jpg)



Fig. 9. Both area and p scale.

![](images/79f1d0ec4e7558b1a9a8b7b826360bec432bab6e96ba096b7e80b074d2bfe72a.jpg)



Fig. 10. Logical topo and traffic.

![](images/524d89933dddd2caa1248fe35c0f062aa0df48d717ccb6d1eb87777693273156.jpg)



Fig. 11. Executed tasks of each node.

# D. Network Management

Since CitySee has the long-term running objective and any physical modification of the network (e.g., replacing individual node) is pretty costly, it is critical and necessary to learn the running status of the entire network as well as each individual node. In order to collect key metrics (such as radio duty cycles, the number of packet transmissions and receptions) and provide visibility into the system, we further design and implement the network management and diagnosis component [20], [22], [26]. In Fig. 14, we show the node management interface by which network administrators are able to trace the node status easily, including its data transmission ratio, neighbor-related information (RSSI, LQI), and etc. Comprehensive consideration, we design several decades of indices to evaluate the healthy of CitySee, e.g., data reception ratio, the total number of tasks executed, routing loops detected, traffic analysis, and etc., which is shown in Fig. 15.

# VII. CONCLUSIONS

We present CitySee, a $C O _ { 2 }$ -monitoring project using a large-scale wireless sensor network in a urban area in Wuxi, China. We focus on the solution of relay node placement problem, one of four major components of CitySee, by formulating the G-GSTWH problem and giving a -approximation 2ratio solution. There are many future works remaining. For example, if LS is empty such that we only consider to deploy some RNs to connect all deployed SNs under the hole-constraint, the question becomes terminal Steiner tree with holes. In addition, our solution only guarantee a - 1connected wireless sensor network. Can we have effective and efficient method to guarantee a k-connected wireless sensor network? Another interesting idea is to use WSNs to construct virtual Carbon Flux Towers, which are utilized to monitor carbon flux accurately but expensively in the real-time manner. However, constructing virtual Carbon Flux Towers raises many challenges at the same time, e.g., multiple vertical layers, -dimensional deployment, longer power-lasting requirement, 3and etc. We leave all these interesting issues for future study.

# VIII. ACKNOWLEDGEMENT

This study is supported by the NSF China Major Program 61190110. We would like to thank other people who also contribute to CitySee, including Zhichao Cao, Dr. Guojun Dai, Wei Gong, Rui Li, Shuo Lian, Dr. Kebin Liu, Junliang Liu, Qiang Ma, Wei Xi, Dr. Panlong Yang, Dr. Zheng Yang, Lan Zhang, Dr. Jizhong Zhao, and etc.

# REFERENCES

[1] co2 detecting instruments. In http://www.szken.com/product/6.html.   
[2] eea. In http://www.eea.europa.eu/.   
[3] ANASTASI, G., CONTI, M., MONALDI, E., AND PASSARELLA, A. An adaptive data-transfer protocol for sensor networks with data mules. In Proceedings of IEEE International Symposium on a World of Wireless, Mobile and Multimedia Networks (2007), pp. 1–8.   
[4] ARORA, A., RAMNATH, R., AND ET AL, E. E. Exscal: Elements of an extreme scale wireless sensor networks. In Proceedings of the 11th IEEE International Conference on Embedded and Real-Time Computing Systems and Applications (2005), pp. 102–108.   
[5] BAI, X., KUMAR, S., XUAN, D., YUN, Z., AND LAI, T. Deploying wireless sensors to achieve both coverage and connectivity. In Proceedings of the 7th ACM international symposium on Mobile ad hoc networking and computing (2006), pp. 131–142.   
[6] BOLONI, L., AND TURGUT, D. Should i send now or send later? a decision-theoretic approach to transmission scheduling in sensor networks with mobile sinks. In Wireless Communications and Mobile Computing (2008), vol. 8.   
[7] BRASS, P. Bounds on coverage and target detection capabilities for models of networks of mobile sensors. In ACM Transactions on Sensor Networks (T OSN ) (2007), vol. 3, pp. 9–es.   
[8] CHEDIN ´ , A., SAUNDERS, R., HOLLINGSWORTH, A., SCOTT, N., MA-TRICARDI, M., ETCHETO, J., CLERBAUX, C., ARMANTE, R., AND CREVOISIER, C. The feasibility of monitoring co2 from high-resolution infrared sounders. In J. Geophys. Res (2003), vol. 108, p. 4064.   
[9] CHEN, D., DU, D., HU, X., LIN, G., WANG, L., AND XUE, G. Approximations for steiner trees with minimum number of steiner points. In Journal of Global Optimization (2000), vol. 18, pp. 17–33.

![](images/e5310d82285b0de4b585384b10f786063ffa42e5a0300e9d663762e9359512cb.jpg)



Fig. 12. A snapshot of CitySee.

![](images/5f9ac99d44c67a40f51435cb5784cddeb5d238eab2800c7bbc922d970ceb1607.jpg)



Fig. 13. Contour map of $C O _ { 2 }$ concentration.

![](images/0a16f1266bd461eea355713b4f4992dc2896436d7f2d62614e2a9c6fb8dc76bf.jpg)



Fig. 14. Node’s running status.

![](images/09ef8df4e772433a2a50f8cb06f250eae6c9a3619e93740e3831a9588c1debc5.jpg)



Fig. 15. System management interface.

[10] CHENG, X., DU, D., WANG, L., AND XU, B. Relay sensor placement in wireless sensor networks. In Wireless Networks (2008), no. 3, pp. 347– 355.   
[11] CHURKINA, G. Modeling the carbon cycle of urban systems. In Ecological Modelling (2008), vol. 216, pp. 107–113.   
[12] DRAKE, D., AND HOUGARDY, S. On approximation algorithms for the terminal steiner tree problem. In Information Processing Letters (2004), vol. 89, pp. 15–18.   
[13] FONSECA, R., GNAWALI, O., JAMIESON, K., AND LEVIS, P. Four-bit wireless link estimation. In Proceedings of the Sixth Workshop on Hot Topics in Networks (HotNetsV I) (2007).   
[14] GANESAN, D., CRISTESCU, R., AND BEFERULL-LOZANO, B. Powerefficient sensor placement and transmission structure for data gathering under distortion constraints. In ACM Transactions on Sensor Networks (T OSN) (2006), vol. 2, pp. 155–181.   
[15] GNAWALI, O., FONSECA, R., JAMIESON, K., MOSS, D., AND LEVIS, P. Collection tree protocol. In Proceedings of the 7th ACM Conference on Embedded Networked Sensor Systems (2009), pp. 1–14.   
[16] HALPERIN, E., KORTSARZ, G., KRAUTHGAMER, R., SRINIVASAN, A., AND WANG, N. Integrality ratio for group steiner trees and directed steiner trees. In Proceedings of the fourteenth annual ACM-SIAM symposium on Discrete algorithms (2003), Society for Industrial and Applied Mathematics, pp. 275–284.   
[17] HAO, B., TANG, H., AND XUE, G. Fault-tolerant relay node placement in wireless sensor networks: formulation and approximation. In IEEE HPSR (2004), pp. 246–250.   
[18] KAPOOR, S., MAHESHWARI, S., AND MITCHELL, J. An efficient algorithm for euclidean shortest paths among polygonal obstacles in the plane. In Discrete & Computational Geometry (1997), no. 4, pp. 377– 383.   
[19] LIN, G., AND XUE, G. Steiner tree problem with minimum number of steiner points and bounded edge-length. In Information Processing Letters (1999), vol. 69, pp. 53–57.   
[20] LIU, K., MA, Q., ZHAO, X., AND LIU, Y. Self-diagnosis for large scale wireless sensor networks. In Proceedings of IEEE INFOCOM (2011), pp. 1539–1547.   
[21] LIU, Y., HE, Y., LI, M., WANG, J., LIU, K., MO, L., DONG, W., YANG, Z., XI, M., ZHAO, J., ET AL. Does wireless sensor network

scale? a measurement study on greenorbs. In Proceedings of IEEE INFOCOM (2011), pp. 873–881.   
[22] LIU, Y., LIU, K., AND LI., M. Passive diagnosis for wireless sensor networks. In IEEE/ACM Transactions on Networking (T ON) (2010), vol. 18, pp. 1132–1144.   
[23] LLOYD, E., AND XUE, G. Relay node placement in wireless sensor networks. In IEEE Transactions on Computers (2007), pp. 134–138.   
[24] MALEKI, M., AND PEDRAM, M. Qom and lifetime-constrained random deployment of sensor networks for minimum energy consumption. In Proceedings of the Fourth IEEE International Symposium on Information Processing in Sensor Networks (2005), pp. 293–300.   
[25] MAO, X., MIAO, X., HE, Y., ZHU, T., WANG, J., DONG, W., LI, X., AND LIU, Y. Citysee: Urban co2 monitoring with sensors. In Technical Report (2012). Http://mypages.iit.edu/∼xmao3/papers/ CitySeeTechReport.pdf.   
[26] MIAO, X., LIU, K., HE, Y., LIU, Y., AND PAPADIAS, D. Agnostic diagnosis: Discovering silent failures in wireless sensor networks. In Proceedings of IEEE INFOCOM (2011), pp. 1548–1556.   
[27] TANG, J., HAO, B., AND SEN, A. Relay node placement in large scale wireless sensor networks. In Computer Communications (2006), vol. 29, pp. 490–501.   
[28] TOLLE, G., AND CULLER, D. Design of an application-cooperative management system for wireless sensor networks. In Proceedings of the Second IEEE European Workshop on Wireless Sensor Networks, (2005), pp. 121–132.   
[29] WANG, X., FU, L., TIAN, X., BEI, Y., PENG, Q., GAN, X., YU, H., AND LIU, J. Converge-cast: On the capacity and delay tradeoffs. In IEEE Transactions on Mobile Computing (2011), no. 99, pp. 1–1.   
[30] WANG, Y., AND TSENG, Y. Distributed deployment schemes for mobile wireless sensor networks to ensure multilevel coverage. In IEEE Transactions on Parallel and Distributed Systems (2008), vol. 19, pp. 1280–1294.