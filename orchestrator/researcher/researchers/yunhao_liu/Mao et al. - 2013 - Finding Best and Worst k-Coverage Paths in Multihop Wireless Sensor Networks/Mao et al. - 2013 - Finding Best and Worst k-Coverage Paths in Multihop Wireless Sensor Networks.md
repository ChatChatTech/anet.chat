# Finding Best and Worst k-Coverage Paths in Multihop Wireless Sensor Networks

Xufei Mao, Member, IEEE, Yunhao Liu, Senior Member, IEEE, Shaojie Tang, Student Member, IEEE, Huafu Liu, Jiankang Han, and Xiang-Yang Li, Senior Member, IEEE

Abstract—Coverage is a fundamental problem in wireless sensor networks (WSNs). From both economic and applicable concerns, designers always would like to provide guaranteed QoS of coverage of WSNs. In this paper, we address two path-coverage problems in WSNs, maximum k-support path coverage (a.k.a. best case coverage) and minimum kbreach path coverage (a.k.a. worst case coverage), in which every point on the desired resultant path is covered by at least k sensors simultaneously while optimizing certain objectives. We present two polynomial-time approaches to find optimal solutions for both maximum k-support coverage problem and minimum k-breach coverage problem. The time complexity of both algorithms are O k2n  n where n is the number of deployed sensor nodes and k is the coverage degree. In addition, a number of properties of kth-nearest Voronoi diagram which is new to the literature are presented.

Index Terms—Optimum k-Coverage, k-Support path, k-Breach path, Wireless Sensor Networks.

# 1 INTRODUCTION

Being a major benchmark when applying wireless sensor networks (WSNs) into real applications, coverage-related problems of WSNs have drawn considerable research interests in the past two decades while posing many new challenging research questions. In most WSNs, two seemingly contradictory, yet related viewpoints of coverage exist: best case coverage and worst case coverage [10]. Generally speaking, the optimization objective of a best case coverage problem is to make areas, paths or points have much observability from deployed sensors, on the contrary, less observability from deployed sensors when we solve a worst case coverage problem. Here, the observability of an area, a path or a point from a sensor node can be explained as the sensing ability of the sensor to the area, a path or a point. For instance, for a sensor node v equipped with a temperature sensor, the observability of a point p (within the valid coverage range of v) from v indicates the accuracy when we use the reading value of v to denote the temperature of the point p. Generally speaking, the closer v and p are, the more accurate the reading

• X. Mao, Y. Liu and J. Han are with CNLIST, School of Software, Tsinghua University and CSE Dept. Hongkong University of Science and Technology. Email: xufei@greenorbs.com, yunhao@greenorbs.com   
• H. Liu is with the Department of Computer Science and Technology, Changsha University China. Email: hfliu9063@163.com   
• S. Tang and X.Y. Li are with Computer Science Dept., Illinois Institute for Technology. Email: stang7@iit.edu, xli@cs.iit.edu

is. When the observability is limited to one sensor node, it is usually called -coverage problem; When the observability is 1determined by k (k is usually, but not limit to, a constant) sensor nodes simultaneously, it belongs to the k-coverage problem.

Let us consider the following application scenario which typically belongs to a k-coverage problem. Assume that there are a group of anchor sensor nodes deployed in some area used to track the movement of a mobile sensor node inside this area. When some Fading Effects-based approach (e.g., using Received Signal Strength Indicator) is used to localize the moving sensor, generally, we need at least  anchor sensors 3which are able to detect (communicate with) the moving sensor node directly at any time without further hardware assistance in a real-time manner. In addition, since the QoS of observability of the moving sensor node from an anchor node is kind of proportional to the Euclidean distance between them (Fading Effects’ property), it is better to restrict the longest distance between the moving sensor and any one of anchor nodes during its movement. In other words, 3the QoS is kind of limited by the furtherest node (the rd 3nearest node in this case) such that we would like to bound the longest distance between the mobile node and its rd-3nearest anchor node all the time during its movement. This kind of problem belongs to the family of best case coverage problems, i.e., maximum support coverage problem, more precisely, maximum k-support coverage problem where k is a critical parameters ( or say coverage degree) determining the QoS of coverage. Let us take another application scenario as an example. Assuming there are some soldiers who have to sneak through some area. Unfortunately, the enemies have deployed a bunch of sensor nodes which are able to detect the movement of objects in this area. Clearly, the soldiers should move forwarder following a path which is keeping away from deployed sensor nodes. This type of problems belongs to the family of worst case coverage whose objective is to decrease the observability from sensor nodes.

In this paper, we aim to solve the following two k-coverage path problems.

1) optimum k-support path problem: finding a path connecting any given source/destination pair of points S and T inside the given area, which maximizes the smallest observability of all points along the path [10]; and   
2) optimum k-breach path problem: finding a path connect-

ing any given source/destination pair of points S and $T$ inside the given area, which minimizes the largest observability of all points along the path.

Here, the definition of observability of a point p depends on different applications. For instance, some existing work [8]– [10] focus on the -coverage problem and assume that the 1observability of a point $p$ is simply the shortest Euclidean distance from $p$ (on the region or path) to the set of sensors $U ,$ , i.e., v∈U -pv-. In this paper, we consider the more mingeneral case, i.e., k-coverage problems, $i . e . ,$ given a set U of sensors deployed in a -dimensional region , we would 2 Ωlike to determine how well the area is k-covered through Ωinvestigating the observability of paths connecting any given source/destination pairs of points. In this case, the observability of a point $p$ from sensor node set U is defined as the shortest Euclidean distance from p to the $k ^ { t h }$ nearest sensor out of U . From now on, we will use distance to denote Euclidean distance when there is no confusion.

To the best of our knowledge, [11], [3] and [15] are the only work so far which aim at addressing the problem of finding an optimal k-covered path. In [11], Mehta et.al suggested that the worst case k-coverage problem may be addressed by adopting the $k ^ { t h }$ nearest point Voronoi diagram. However, no algorithm and theoretical results were given. In [3], Fang et.al gave a polynomial time algorithm to identify a k-covered path based on binary search and growing disk techniques. Unfortunately, their algorithms cannot guarantee an optimum solution. This is because the binary search method in their algorithm may not return the optimal k-support path when $k ^ { t h }$ -distance of some point on the path is not integer. Furthermore, they assumed that k is a given constant, which reduces the generality of the algorithm since the value of k could be up to the number of sensor nodes n depending on different applications and QoS requirements. Clearly, the -coverage problem is an special case of the proposed problem in the paper where $k = 1$ .

The main contributions of our paper are as follows.

1) We present and prove a number of theoretical results about the properties of $k ^ { t h }$ Nearest Point $( k ^ { t h } { - } \mathrm { N P } )$ Voronoi diagram, which are new to the literature and have independent interests.   
2) We further propose an efficient algorithm to generate the $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram by combining computational geometry techniques with graph theoretical and algorithmic techniques.   
3) We designed and implemented centralized polynomial time algorithms, which are able to find optimum ksupport and k-breach paths in sensor networks with general k. We further proposed a distributed algorithms for k-support path problem. Both our algorithms run in polynomial time $O ( k ^ { 2 } n \log n )$ where n is the number of ( log )wireless sensor nodes and k is the coverage degree.   
4) To the best of our knowledge, this is the first work that presents polynomial time algorithms finding optimal ksupport paths and optimal k-breach paths for a general k .

The rest of the paper is organized as follows. In Section $^ { 2 , }$ we define terms, notations and problems studied, following which we detail the procedure of computing the $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram of the given sensor node set U . We present the polynomial time algorithms that solve the optimum ksupport path problem efficiently in Section 3, and further propose the distributed algorithm which can obtain an optimal k-support path in Section 4. Section 5 describes the details solving the optimum k-breach path problem efficiently. We give the running procedure of our algorithms with some simulation results in Section 6. We review the some related work in Section 7 and conclude our paper in Section 8. In the supplementary file (Appendix), we further discuss the methods to find both k-support and k-breach paths when each sensor node has (different) bounded sensing range, provide detailed proofs of theorems and lemmas and give more simulation results respectively.

# 2 PRELIMINARIES

In this section, we formally define the terms, notations used throughout the paper and give the formal definitions of questions to be studied.

# 2.1 Problem Formulation

Assume that there is a connected WSN consisting of n identical and stationary wireless sensor nodes $U = \{ u _ { 1 } , u _ { 2 } , . . . , u _ { n } \}$ =deployed inside a continuous two-dimensional field  where the location $( x _ { i } , y _ { i } )$ of each sensor node $u _ { i } : 1 \leq i \leq n$ is ( ) : 1known a priori. Here, the location information of each sensor node could be measured by precise GPS equipments when deployed. Since the localization problem of wireless sensor nodes is out of the scope of this work, we assume the location information of each wireless sensor node is precise.

In addition, we assume that each sensor node v has enough sensing range such that it is able to observe any point p in where the observability of $p$ Ωfrom v depends on the distance ||vp|| between them. Generally speaking, the sensing ability of a sensor node to a point has monotone decreasing property with the increment of the distance between an object (point) being sensed and the sensor node’s location. In this paper, we use Euclidean distance as the measurement of QoS. Before we formulate the questions to be studied in this paper, we introduce some definitions which will be used in the paper.

Definition 1: Given a point $p$ in the field and the set of sensors $U ,$ , the $k ^ { t h }$ -distance of $p ,$ Ω with respect to $U ,$ denoted as $\ell _ { k } ( p , U )$ , is defined as the Euclidian distance from $p$ to its $k ^ { t h }$ ( )nearest sensor node in U .

Definition 2: Given a path P connecting a source point S and a destination point T , the k-support of $P ,$ denoted by $S _ { k } ( P )$ , is defined as the maximum $\bar { k ^ { t h } }$ -distance of all points on $P , i . e . , S _ { k } ( P ) = \operatorname* { m a x } _ { p \in P } \ell _ { k } ( p , U )$ where $p$ is a point on the path $P .$ .

Definition $3 ;$ Given a path P connecting a source point S and a destination point $T _ { \ast }$ , the k-breach of $P ,$ denoted by $B _ { k } ( P )$ , is defined as the minimum $k ^ { t h }$ -distance of all points ( )on P , i.e., $\begin{array} { r } { B _ { k } ( P ) = \operatorname* { m i n } _ { p \in P } \ell _ { k } ( p , U ) } \end{array}$ where $p$ is a point on the path P .

The main questions studied in the paper are as follows.

Question 1: Optimal k-Support Path (Best Case Coverage) Problem: Given a pair of points S and $T$ in the region , finding a path $P$ inside to connect S and $T$ such that $S _ { k } ( P )$ is minimized.

( )Question 2: Optimal k-Breach Path (Worst Case Coverage) Problem: Given a pair of points S and $T$ in the region $\Omega ,$ finding a path $P$ inside the field  to connect S and $T$ Ωsuch that $B _ { k } ( P )$ is maximized.

( )In the remaining part of this section, we present some key concepts that are critical to our polynomial solutions.

# 2.2 The $k ^ { t h }$ Nearest Point Voronoi Diagram

Definition 4: Given a set of identical sensor nodes $U =$ $\{ u _ { 1 } , u _ { 2 } , \cdots , u _ { n } \}$ =deployed in the field , we assign a geometry point p in  to the sensor node $u _ { i } \in U$ if $u _ { i }$ is the $k ^ { t h }$ Ωnearest sensor node of $p .$ Following this assignment rule, we assign all points in the field to at least one sensor node in U . As a result, we obtain a collection of regions associated with sensor nodes in $U ,$ denoted by $\mathbb { V } _ { k } = \{ V _ { k } ( u _ { 1 } ) , . . . V _ { k } ( u _ { n } ) \}$ , = ( )which forms a tessellation. We call the tessellation $\mathbb { V } _ { k }$ (the $k ^ { t h }$ Nearest Point Voronoi Diagram $( k ^ { t h }  – N P$ Voronoi Diagram) of $U ,$ , and the region $V _ { k } ( u _ { i } )$ the $k ^ { t h } - N P$ Voronoi region of node $u _ { i }$ .

Clearly, according to the definition of $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram, all points inside region $V _ { k } ( u _ { i } )$ have the same $k ^ { t h }$ nearest sensor node $u _ { i } ~ \in ~ U$ ( ). It is worth observing that $V _ { k } ( u _ { i } )$ may consist of several independent polygons. Here we ( )call each independent polygon as the $k ^ { t h }  – N P$ Voronoi cell (denoted by $C _ { k } ( u _ { i } ) )$ of node $u _ { i }$ and name $u _ { i }$ as the $k ^ { t h } .$ - ( )owner (abbreviated to owner) of $C _ { k } ( u _ { i } )$ . In addition, an edge of some $k ^ { t h }$ (-NP Voronoi cell is called a $k ^ { t h }  – N P$ Voronoi edge and the intersection point of any two $k ^ { t h }  – \mathrm { N P }$ Voronoi edges is named as the $k ^ { t h }  – N P$ Voronoi vertex. When some point $( \mathrm { e . g . }$ , falling on some $k ^ { t h }$ -NP Voronoi edge) has multiple owners, it randomly chooses one of them as the owner.

Definition 5 (Perfect Support Location): The perfect support location of a $k ^ { t h }  – \mathrm { N P }$ Voronoi edge is defined as the point with the minimum $k ^ { t h }$ -distance on the edge, i.e., point $p$ is the perfect support location of the $k ^ { t h }  – \mathrm { N P }$ Voronoi edge e iif $\begin{array} { r } { \vert \vert p u _ { i } \vert \vert = \operatorname* { m i n } _ { \forall p \in e } \{ \vert \vert p u _ { i } \vert \vert \} } \end{array}$ where $u _ { i } \in U$ is the owner of e.

= minIt is worth mentioning that for each $k ^ { t h }  – \mathrm { N P }$ Voronoi edge, it has one and only one perfect support location.

# 2.3 Difference Between $k ^ { t h }$ -NP Voronoi Diagram and Order-k Voronoi Diagram

Since most of our results are based on $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram, most properties of which are unknown to the literature, it is helpful to briefly discuss the differences between $k ^ { t h }$ - NP Voronoi diagram and another well-known concept, order-k Voronoi diagram [2].

Definition 6 (The Order-k Voronoi Diagram $I 2 J .$ The order-k Voronoi diagram is a partition of the plane into regions such that points in each region have the same k closest sensor nodes in set $U ^ { [ k ] }$ where $U ^ { [ k ] }$ is a subset of nodes in U with cardinality k. Each polygon is named order-k Voronoi cell $C _ { o k } ( U ^ { [ k ] } )$ corresponding to the subset $U ^ { [ k ] }$ of U .

According to the Definition 4 and Definition $^ { 6 , }$ the $k ^ { t h }$ -NP Voronoi diagram of a set of sensor nodes U partitions the plane into cells such that all points in the same cell have the same $k ^ { t h }$ nearest sensor node $\in U$ while the order-k Voronoi diagram [2] of a set of sensor nodes $U$ partitions the plane into cells such that all points in the same cell have the same set (maybe in different distance orders) of k nearest sensors out of U . Please refer to the examples shown in Fig. 5 (in Appendix) for illustration.

# 2.4 Compute the $k ^ { t h }$ -NP Voronoi Diagram in Polynomial Time

We first present the method to compute the $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram with respect to sensor node set U in polynomial time since the $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram plays an important role in our solutions.

Definition 7 (The Farthest Point Voronoi Diagram): The farthest point Voronoi diagram is a special case of $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram when $k = n$ . It is a partition of the plane =into polygons such that points in the same polygon have the same farthest sensor node $u _ { i }$ out of U with cardinality n. Each polygon is called a farthest Voronoi cell.

Lemma 1: For any point $p$ in the plane $\Omega , p \in C _ { k } ( u _ { i } )$ if Ωand only if p is located in some order-k Voronoi cell $C _ { o k } ( U ^ { [ k ] } )$ where ${ \dot { u } } _ { i } \in U ^ { [ k ] }$ and $u _ { i }$ is $p \mathrm { ^ { \circ } s }$ ( ) farthest sensor node among all k sensor nodes in $U ^ { [ k ] }$ .

Proof: Please refer to the supplementary file.

![](images/98248ea64025702da113abc2d6a8966ef05c9ddc51752e7c02604cca8cfd583c.jpg)

Based on Lemma 1, we propose the following Alg. 1 with time complexity $O ( k ^ { 2 } n \lg n )$ (proved in Lemma 6) to compute the $k ^ { t h }  – \mathrm { N P }$ ( lg ) Voronoi diagram of the sensor node set $U .$ . The main idea of our method is as follows.

1) Compute the order-k Voronoi diagram of the given sensor nodes set U using the algorithm given in [7].   
2) For each order-k Voronoi cell $C _ { o k } ( U ^ { [ k ] } )$ (defined in ( )[7]), we compute the farthest Voronoi diagram of its corresponding k sensor nodes set $U ^ { [ k ] }$ following the method in $[ 1 4 ] ;$ and for each sensor node $u _ { i } ~ \in ~ U ^ { [ k ] }$ , return the corresponding farthest Voronoi cell as a part of $u _ { i } { { \bf \bar { s } } } k ^ { t h }$ -NP Voronoi cell.   
3) For each sensor node $u _ { i } ,$ , we union any two $k ^ { t h }$ -NP Voronoi cells computed in step  as one $k ^ { t h }  – \mathrm { N P }$ Voronoi 2cell if they both have the same owner and share at least one edge. After the union operation, we get $k ^ { t h }$ -NP Voronoi diagram $G$ of $U$ .

Now we are ready to present our polynomial time algorithms computing the optimal k-support path and the optimal k-breach path within $O ( k ^ { 2 } n \log n )$ time.

Given a set of sensor nodes U with cardinality n and the continuous field , our algorithm computing the optimum $k \mathrm { - }$ Ωsupport path mainly consists of two phases. In the first phase, we use Algorithm 1 to compute the $k ^ { \bar { t } h }  – \mathrm { N P }$ Voronoi diagram G in time $\bar { O ( } k ^ { 2 } n \log n )$ . During the second phase, we construct ( log )a new weighted graph $G ^ { \prime }$ based on $k ^ { t h }  – \dot { \mathrm { N P } }$ Voronoi diagram $\mathbb { V } _ { k } = \{ V _ { k } ( u _ { 1 } ) , . . . V _ { k } ( u _ { n } ) \}$ (output of Alg. 1) and then compute = ( ) ( )the optimal k-support path on $G ^ { \prime }$ in time $O ( k ^ { 2 } n \log n )$ .

Algorithm 1 Computing $k ^ { t h }  – \mathrm { N P }$ Voronoi Diagram   
Input: The set of sensor nodes U.
Output: The $k^{th}$ -NP Voronoi diagram G of U.
1: Compute U's order-k Voronoi diagram;
2: for Each order-k Voronoi cell $C_{ok}(U^{[k]})$ do
3: Compute the farthest point Voronoi diagram using corresponding k sensor nodes in $U^{[k]}$ ;
4: end for
5: for Each $k^{th}$ -NP Voronoi edge e do
6: if If two polygons having the same owner share e then
7: Merge these two polygons into one polygon;
8: end if
9: end for
10: for Each sensor node $u_{i}$ do
11: Return the union of all polygons belongs to $u_{i}$ as $u_{i}$ 's $k^{th}$ -NP Voronoi cells;
12: end for

# 3 BEST CASE COVERAGE: OPTIMAL $k \mathrm { - }$ SUPPORT PATH

In this section, we address the optimal k-support path problem, $i . e .$ , for any source/destination pair of points S and $T$ in the given area , finding a path with minimum k-support among Ωall possible paths connecting S and T in .

# 3.1 Preliminaries

Before we introduce the main idea of our solutions, we first present some useful theoretical results which are useful for proving the correctness of our algorithms.

Theorem 2: Given any path $P _ { 1 }$ connecting a source node S and a destination node T inside region  , we can always construct another (maybe same) path $P _ { 2 }$ Ωconsisting of only a finite number of line segments such that

$$
S _ {k} (P _ {2}) \leq S _ {k} (P _ {1})
$$

Proof: Please refer to the supplementary file.

Based on Theorem 2, we further prove the following Theorem 3 and 4.

Theorem 3: Given any path $P _ { 1 }$ connecting the source S and the destination T inside of region , we can always find a path $P _ { 3 }$ Ωconsisting of line segments whose end points are perfect support locations only such that

$$
S _ {k} (P _ {3}) \leq S _ {k} (P _ {1}).
$$

Proof: Please refer to the supplementary file.

Theorem 4: There is one optimal k-support path consisting of only line segments whose end points are located exactly at some perfect support locations of $k ^ { t h }  – \mathrm { N P }$ Voronoi edges.

Proof: Please refer to the supplementary file.

# 3.2 Compute the Optimum k-Support Path

As shown in Theorem 4, there must exists at least one optimum k-support path connecting the given source/destination pair of points S and $T ,$ which consists of only line segments whose end points are the perfect support locations of some $k ^ { t h }$ -NP Voronoi edges. Hence, we can limit the solution space to all paths consisting of only line segments, which connect perfect support locations of $k ^ { \mathrm { { } } \bar { t } h } \mathrm { { - N P } }$ Voronoi edges. Among all paths consisting of these line segments, the one with the minimum k-support must be one of the desired optimal k-support path. The main idea is as follows. First, we construct a new graph $G ^ { \prime }$ based on $k ^ { t h }$ -NP Voronoi diagram G as follows:

1) For each $k ^ { t h }$ -NP Voronoi edge e in $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram V, we add a new node $v ^ { \prime }$ (to $V [ G ^ { \prime } ] )$ whose [ ]location is the perfect support location of e. Notice that when multiple $\cdot \ k ^ { t h } { \bf - } \ N P$ Voronoi edges share the same perfect support location, we only add one node. In other words, we establish a one-to-one (or many-to-one) mapping between each $k ^ { t h }  – \mathrm { N P }$ Voronoi edge e in V and each node $v ^ { \prime } \in V [ G ^ { \prime } ]$ . Finally, we add the source and [ ]destination points S and $T$ to $V [ G ^ { \prime } ]$ .   
[ ]2) Use the following rules to assign weight to each node in $V [ G ^ { \prime } ]$ . If node $\bar { v ^ { \prime } } \in V [ G ^ { \prime } ]$ is S or $T ,$ , the weight of $v ^ { \prime }$ [ ](denoted by $w ( v ^ { \prime } ) )$ [ ] is equal to the $k ^ { t h }$ -distance of S or $T$ in V $( i . e . , \ w ( v ^ { \prime } ) = \ell _ { k } ( S , U )$ if $v ^ { \prime } = S$ or $w ( v ^ { \prime } ) =$ $\ell _ { k } ( D , U )$ if $v ^ { \prime } = D )$ = ( ). Otherwise, $w ( v ^ { \prime } )$ ( ) =is equal to the $k ^ { t h }$ ) = ( )-distance of the perfect support location of edge $e \in \mathbb { V }$ where $e \in \mathbb { V }$ is corresponding to $v ^ { \prime } \in G ^ { \prime }$ in the one-toone (or many-to-one) mapping.   
3) Divide all nodes in $V [ G ^ { \prime } ]$ into groups such that a bunch [ ]of nodes (including S and T ) are in the same group iff their mapping $\hat { k ^ { t h } }$ -NP Voronoi edges in V belong to the same $k ^ { t h }  – \mathrm { N P }$ Voronoi cell. Notice, different groups may contain same node(s) since multiple $k ^ { t h }  – \mathrm { N P }$ Voronoi edges may map to the same node in $G ^ { \prime }$ . For each group of nodes, we sort all nodes by their weights in decreasing (or increasing) order. After that, we add an edge to $E [ G ^ { \prime } ]$ [ ]between each pair of adjacent two nodes in the sorted list such that we have a simple graph $G ^ { \prime }$ .   
4) Assign each edge $u ^ { \prime } v ^ { \prime } \in E [ G ^ { \prime } ]$ with weight $w ( u ^ { \prime } , v ^ { \prime } )$ which is equal to $\{ w ( u ^ { \prime } ) , w ( v ^ { \prime } ) \}$ .

Next, we use Algorithm 2, which originates from Dijkstra’s shortest path algorithm, to find a minimum weight path $P ^ { \prime }$ in $G ^ { \prime }$ to connect $\bar { S }$ and T . Here, the weight of a path is equal to the maximum weight of all edges it contains and a path $P ^ { \prime }$ (connecting S to T ) in $G ^ { \prime }$ is said to be a minimum weight path iff $P ^ { \prime }$ has the minimum weight among all paths connecting S to T . Finally, we get one optimum k-support path $P$ in G by directly applying $P ^ { \prime }$ to $G .$

# 3.3 Correctness

We show the correctness of our algorithm by proving the following theorem.

Theorem 5: Given any source/destination pair of points S and T inside the region  where sensor nodes in set U have Ωbeen deployed, the path P returned by algorithm 2 is an optimal k-support path.

Proof: Please refer to the supplementary file.

Remembering that we have claimed that there are multiple approaches for connecting all perfect support locations inside one $k ^ { t h } { \bf - N P }$ Voronoi cell such that we may have multiple choices of graph $G ^ { \prime } .$ For example, we can connect all perfect support locations in a complete graph manner, $i . e .$ , adding an edge between each pair of perfect support locations (assume that the resultant graph is $G ^ { \prime \prime } )$ . Clearly, running Algorithm  on $G ^ { \prime \prime }$ 2definitely returns an optimum k-support path as well since $G ^ { \prime \prime }$ is a complete graph containing all edges connecting each pair of perfect support locations. The reason for us to connect perfect support locations linearly, i.e., connecting them after sorted, is that we try to reduce the time complexity of our algorithm since the smaller the number of edges in $G ^ { \prime }$ is, the less running time is.

Algorithm 2 The Optimal k-Support Path Algorithm   
Input: $G'$ , source node S, destination node T.
Output: Minimum k-support Path Connecting S to T.
1: for each vertex $v'$ in graph $G'$ do
2:    k-support[ $v'$ ] ← infinity
3:    previous[ $v'$ ] ← undefined
4: end for
5: k-support[S'] ← w(S)
6: Q ← all nodes in graph $G'$ 7: while Q is not empty do
8: $u' \leftarrow$ node in Q with smallest k-support
9:    remove $u'$ from Q
10:    for Each neighbor $v'$ of $u'$ : do
11:    alt ← max{w( $u'$ , $v'$ ), k-support[ $u'$ ]}
12:    if alt < k-support[ $v'$ ] then
13:    k-support[ $v'$ ] ← alt
14:    previous[ $v'$ ] ← $u'$ 15:    end if
16:    end for
17: end while
18: Return $P'$ which is the minimum weighted path connecting S to T

# 3.4 Time Complexity Analysis

In this subsection, we prove that the time complexity of our algorithm is $O ( k ^ { 2 } n$ n , which is better than that of the ( log )work [15]. Here, n is the number of deployed sensor nodes and k is the coverage degree. As shown before, our algorithm is composed by two phases, one is to compute the $\bar { k } ^ { t h }  – \mathrm { N P }$ Voronoi diagram, and the other one is to find the optimal k-support path based on the solution of the first phase. We analyze the time complexity of these two phases one by one. We first give a bound of the time complexity for the first phase.

Lemma $6 { : }$ The time complexity of Algorithm 1 computing the $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram is $O ( k ^ { 2 } n \lg n )$ where $n$ is the ( lg )cardinality of the set U containing all deployed sensor nodes and k is the coverage degree.

Proof: Please refer to the supplementary file.

![](images/91220acf81e5c99916aabdfa69099b9756641ad5f8676d4f8efaf2d3ed2d98db.jpg)

Next, we show the time complexity of the second phase. Since the time complexity of the second phase is determined by the number of $k ^ { t \bar { h } } \ – \mathrm { N P }$ Voronoi cells and the number of $k ^ { t h }$ - NP Voronoi edges, we first prove some properties of $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram, which is new to the literature.

Lemma $7 ;$ For a set of sensor nodes in U with cardinality n on the field  and its $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram $\mathbb { V } ,$ the total number of $k ^ { t h }$ -NP Voronoi edges is bounded by $O ( k ^ { 2 } n )$ and the number of edges of each $\bar { k ^ { t h } } \ – \mathrm { N P }$ ( Voronoi cell is $O ( n )$ .

Proof: Please refer to the supplementary file.

![](images/97e3d8840c2e1ebbbbbc9f692b5a040a644169357fed308c9991979fdf488ae3.jpg)

Lemma 8: The time complexity of our algorithm to compute the optimum k-support path based on $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram is $O ( k ^ { 2 } n \log n )$ .

( log )Proof: Please refer to the supplementary file.

![](images/8753069e998cbb80ced6424200b400116775c1e20630970bff38308bee4fb4a7.jpg)

Combining Lemma 6 and Lemma 8 together, we have the following theorem.

Theorem $g _ { \dot { \cdot } }$ The time complexity of our algorithm to find an optimum k-support path is $O ( k ^ { 2 } n \log n )$ where n is the cardinality of the set $U$ ( log )containing all deployed sensor nodes and k is the coverage degree.

# 4 DISTRIBUTED ALGORITHM FOR COMPUT-ING THE OPTIMAL k-SUPPORT PATH

In this section, we present the distributed algorithm to compute the optimal k- support path after getting the $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram of $U$ by Algorithm 1. First, we let each sensor node record its owned $k ^ { t h }$ -NP Voronoi cells, including the geometry information of each edge of each $k ^ { t h }  – \mathrm { N P }$ Voronoi cell. Here we assume that each $k ^ { t h }  – \mathrm { N P }$ Voronoi edge is assigned with an unique identity. It is worth observing that every $k ^ { t h }  – \mathrm { N P }$ Voronoi edge may belong to one or two cells such that it can have multiple owners. The main idea of our distributed algorithm is based on Theorem 4.

First, we construct a new graph $G ^ { \prime }$ based on $k ^ { t h }  – \mathrm { N P }$ Voronoi diagram G in a distributed manner. Our key point is to let each sensor node $u _ { j } \ ( 1 \leq j \leq n )$ construct a new graph $G _ { \mathcal { C } _ { i } } ^ { u _ { j } }$ locally (1for each of its own $k ^ { t h }  – \mathrm { N P }$ Voronoi cells $\mathcal { C } _ { i } .$ . And $\dot { G } ^ { \prime }$ is the union of all such new constructed local graphs, $i . e .$ ,

$$
G ^ {\prime} = \bigcup_ {u _ {j} o w n s \mathcal {C} _ {i}} G _ {\mathcal {C} _ {i}} ^ {u _ {j}}: \forall u _ {j} \in U
$$

For each cell $\mathcal { C } _ { i }$ owned by the sensor node $u _ { j } , \ u _ { j }$ constructs a local graph for cell $\mathcal { C } _ { i }$ by the following steps.

• Initially, the vertex set $V ( G _ { \mathcal { C } _ { i } } ^ { u _ { j } } )$ and the link set $E ( G _ { \mathcal { C } _ { i } } ^ { u _ { j } } )$ are initiated to be empty.   
• Foby $k ^ { t h }  – \mathrm { N P }$ Voronoi edge e belona corresponding point $\mathcal { C } _ { i }$ (own. Let $u _ { j } ) , u _ { j }$ $v ^ { \prime }$ $G _ { \mathcal { C } _ { i } } ^ { u _ { j } }$ $v ^ { \prime }$ utilize the perfect support location of e as its location and let the weight of $v ^ { \prime } ,$ , denoted by $w ( v ^ { \prime } )$ , be equal to the $k ^ { t h }$ ( )-distance of the perfect support location of edge $e _ { * }$ I n addition, we let the node $v ^ { \prime }$ has the same unique ID as its corresponding edge.   
• If the source point S or the destination point $T$ (or both) is owned by $u _ { j } , u _ { j }$ adds the source point $S$ or the destination point $T$ (or both) to $G _ { \mathcal { C } _ { i } } ^ { u _ { j } }$ as well. The weight of S (resp. T ) is equal to the $k ^ { t h }$ -distance of $S$ (resp. T ) in $\mathbb { V } .$ .   
• Sort all vertices of $G _ { \mathcal { C } _ { i } } ^ { u _ { j } }$ in decreasing (or increasing) order by their weights. Add an edge between each pair of adjacent two vertices in the sorted list to $E ( G _ { C _ { i } } ^ { u _ { i } } )$ . In other words, the graph $G _ { \mathcal { C } _ { i } } ^ { u _ { j } }$ ( i )consists of a series of continuous line segments.

• Assign weight to each newly added edge $e ^ { \prime } , w ( e ^ { \prime } ) =$ max $\{ w ( v _ { 1 } ^ { \prime } ) , w ( v _ { 2 } ^ { \prime } ) \}$ where $v _ { 1 } ^ { j }$ and $v _ { 2 } ^ { \prime }$ ( ) =are two end points mof $e ^ { \prime } .$ .

Clearly, the graph $\begin{array} { r } { G ^ { \prime } = \bigcup _ { u _ { j } \ o w n s \ \mathscr { C } _ { i } } G _ { \mathscr { C } _ { i } } ^ { u _ { j } } \ : \forall u _ { j } \in U } \end{array}$ is a =   :connect graph. Then we run a distributed minimum weight path algorithm (modification from work in [19]) on graph $G ^ { \prime }$ to compute the minimum weighted path connecting S and $T$ since all sensor nodes construct a connect network and they can exchange information via one- or multi-hop. A path is said to be a minimum weighted path connecting S and $T$ if the maximum weight of all its line segments is minimized among all paths connecting S and T .

Then, we use Algorithm 3, which originates from Dijkstra’s shortest path algorithm, to identify a path $P ^ { \prime }$ in $G ^ { \prime }$ to connect S and T such that the maximum weight among its edges’ is minimized. Finally, by applying $P ^ { \prime }$ to graph G directly, we get an optimum k-support path $P .$

Algorithm 3 Distributed Optimum k-Support Path Algorithm

Input: the $k ^ { t h }$ -NP Voronoi diagram $\mathbb { V }$ of the sensor node set U , the source point S and destination point $T .$ .

Output: the minimum k-support path connecting S and T .

1: $V [ G ^ { \prime } ]  \varnothing ; E [ G ^ { \prime } ]  \varnothing ;$   
[ ] [ ]2: for Each sensor node $u _ { i } \in U$ do   
3: for Each $k ^ { t h }  – \mathrm { N P }$ Voronoi cell $\mathcal { C } _ { j }$ owned by $u _ { i }$ do   
4: Use Alg. 4 to distributively construct a new graph $G _ { \mathcal { C } _ { i } } ^ { u _ { i } } .$ .   
5: $V [ \Breve { G } ^ { \prime } ] = V [ G ^ { \prime } ] \cup V [ G _ { \mathcal { C } _ { j } } ^ { u _ { i } } ] .$ . (The vertices with same [ ] = [ ] [ ]ID will be merge to one single vertex after union.)   
6: $E [ G ^ { \prime } ] = E [ G ^ { \prime } ] \mathsf { \bar { U } } E [ G _ { \mathcal { C } _ { j } } ^ { u _ { i } } ]$   
[ ]7: end for   
8: end for   
9: Run distributed minimum weighted path algorithm (in [19]) on $G ^ { \prime }$ to get an minimum weight path $P ^ { \ j }$ connecting S and T .   
10: Return $P ^ { \prime }$

# 5 WORST CASE COVERAGE: OPTIMAL k-BREACH PATH

In this section, we address the optimum k-breach path problem. By taking advantages of the previous work [10], we prove that an optimal k-breach path lies along the $k ^ { t h }  – \mathrm { N P }$ Voronoi edges only except the sup-path connecting S (resp. T ) to some point on some $\bar { k } ^ { t h } \ – \mathrm { N P }$ Voronoi edge if S (resp. T ) lies inside some $k ^ { t h }$ -NP Voronoi cell rather than on some $k ^ { t h }  – \mathrm { N P }$ Voronoi edge. The first step of finding an optimal k-breach path is to compute the $k ^ { t h }$ -NP Voronoi diagram of the sensor node set U , which can be computed by algorithm 1.

# 5.1 Preliminaries

Before we go through the details of the algorithm to solve the optimal k-breach path problem, we give some theoretical results in advance, which illustrate the main idea and the correctness of our algorithm.

Algorithm 4 Distributed Constructing New Graph $\overline { { G ^ { \prime } } }$

Input: Sensor node $u _ { i } ~ \in ~ U$ and a $k ^ { t h }$ -NP Voronoi cell $\mathcal { C } _ { j }$ owned by $u _ { i }$

Output: New constructed graph $G _ { \mathcal { C } _ { j } } ^ { u _ { i } } .$

1: $V [ G _ { \mathcal { C } _ { j } } ^ { u _ { i } } ] \gets \emptyset ; E [ G _ { \mathcal { C } _ { j } } ^ { u _ { i } } ] \gets \emptyset ;$   
[ ]2: for Each $k ^ { t h }$ [ ]-NP Voronoi edge $e \in \mathcal { C } _ { j }$ do   
3: $u _ { i }$ adds a new vertex $v ^ { \prime }$ at the perfect support location point of $e ;$   
4: Assign $v ^ { \prime }$ with the same unique ID as that of $e ;$   
5: Consider the $k ^ { t h }$ -distance of the perfect support location of e as the weight of vertex $v ^ { \prime } \ ( w ( v ^ { \prime } ) ) ;$   
6: end for   
7: if $u _ { i }$ owns S or $T$ (or both) then   
8: Add the source vertex S or the destination vertex $T$ (or both);   
9: Let the weight of S (resp. T ) in $G _ { C _ { i } } ^ { u _ { i } }$ be equal to the $k ^ { t h }$ distance of S (resp. T ) in $\mathbb { V } .$   
10: end if   
11: Sort all new added vertices by their weights. Add an edge between each adjacent pairs of vertices in the sorted list.   
12: Let the weight of each new added edge be equal to the bigger one of its two end vertices’ weights.   
13: Return $G _ { { \mathcal { C } } _ { j } } ^ { u _ { i } } ,$

Theorem 10: Given any path $P _ { 1 }$ connecting source point S and the destination point $T _ { \ast }$ , we can always construct another (maybe same) path $P _ { 4 }$ which only uses $k ^ { \hat { t h } }$ -NP Voronoi edges (neglecting the sub-path from $S$ or $T$ to one of edges of the $k ^ { t h }  – \mathrm { N P }$ Voronoi cell containing S or T ) such that

$$
B _ {k} (P _ {4}) \geq B _ {k} (P _ {1})
$$

Proof: Please refer to the supplementary file.

Obviously, the following theorem immediately follows:

Theorem 11: There is one maximum k-breach path which lies along the $k ^ { t h }$ -NP Voronoi edges (except the first edge or last edge when S or $T$ is not on some Voronoi edge).

# 5.2 Compute the Maximum k-Breach Path

We are now ready to present our algorithm to compute the optimum k-breach path. For any given set of sensor nodes U and source/destination pair of points S and T , The main idea of our approach is as follows.

1) Use Algorithm 1 to generate $k ^ { t h }$ -NP Voronoi diagram V of U .   
2) Add all $k ^ { t h }$ -NP Voronoi vertices (including S and T ) and all $k ^ { t h }$ -NP Voronoi edges to new graph $G ^ { \prime }$ .   
3) Each $k ^ { t h }$ -NP Voronoi vertex $ { \boldsymbol { v } } \in  { \mathbb { V } }$ is assigned a weight w v which is equal to the $k ^ { t h }$ -distance of v, i.e., $\ell _ { k } ( v , U )$ .   
( )4) If S (resp. T ) is inside some $k ^ { t h }$ -NP Voronoi cell $\mathcal { C } _ { k } ( u _ { i } )$ , rather than on some $k ^ { t h }  – \mathrm { N P }$ ( ) Voronoi edge, we draw a line from $u _ { i }$ to S (resp. T ), where $u _ { i }$ is the owner of the $k ^ { t h }  – \mathrm { N P }$ Voronoi cell $\mathcal { C } _ { k } ( u _ { i } )$ . We further extend this (line segment to some edge of $\mathcal { C } _ { k } ( u _ { i } )$ (assuming that the ( )intersection point is a). We add an edge between S (resp.

T ) and a along with the point a itself to $G ^ { \prime }$ . When S (resp. T ) exists inside some $k ^ { t h }  – \mathrm { N P }$ Voronoi cell whose edges contain part of the boundary of , we can add an Ωedge between S (resp. T ) to each perfect support location of this cell (explained later).

5) For each edge $\mathbf { \Sigma } ( u , v ) \ ( \ ( u , v )$ may be a newly added edge or a $k ^ { t h }  – \mathrm { N P }$ ( ) ( ) Voronoi edge in $G ^ { \prime } )$ , we let the weight of $( u , v )$ be equal to the minimum $k ^ { t h }$ -distance among all ( )points on $( u , v )$ .   
( )6) Finally, by applying Algorithm 5 to $G ^ { \prime }$ , we get one optimal k-breach path connecting S to T .

Algorithm 5 Compute the Optimum k-Breach Path   
Input: G, source point S, destination point T.
Output: An optimum k-breach path connecting S to T.
1: for each vertex v in graph G do
2:    k-breach[v] ← infinity
3:    previous[v] ← undefined
4: end for
5: k-breach[S] ← w(S)
6: Q ← the set of all nodes in graph G
7: while Q is not empty do
8:    u ← node in Q with largest k-breach[]
9:    remove u from Q
10:    for each neighbor v of u: do
11:    alt ← min{w(u,v), k-breach[u]}
12:    if alt > k-breach[v] then
13:    k-breach[v] ← alt
14:    previous[v] ← u
15:    end if
16:    end for
17: end while
18: Return P, which is the maximum weighted path connecting S to T

# 5.3 Correctness

Based on Theorem 11, we know that there is one optimal $k \mathrm { - }$ breach path using the $k ^ { t h }  – \mathrm { N P }$ Voronoi edges only (except the first edge and last edge which are used to connect S to $T$ to some $k ^ { t h }  – \mathrm { N P }$ Voronoi edge when $S$ or $T$ is not on some $k ^ { t h }$ -NP Voronoi edge). Since the path P computed by our algorithm has maximize the minimum k-breach of it, $P$ must be the optimal k-breach path among all those paths which lie on the $\bar { k ^ { t h } }$ -NP Voronoi edges.

# 5.4 Time Complexity Analysis

Compared to the algorithm used to identify the optimal $k \mathrm { - }$ support path in the previous section, the procedure of constructing a new graph $G ^ { \prime }$ is simpler. The following Theorem 12 gives us an upper bound on the time complexity of our method.

Theorem 12: The time complexity of our algorithm computing an optimum k-breach path is $O ( k ^ { 2 } n \log n )$ .

( log )Proof: Please refer to the supplementary file.

![](images/fead603231a36d41b95235cb8d7c6bc15ea4a43ae97fac818b9fdf3235643c67.jpg)

# 6 RUNNING PROCEDURE

In this section, we give the details of entire running procedure of proposed algorithms, including all the intermediate and final results. We implement and test our proposed k-support and $k \mathrm { - }$ breach algorithms to find the optimum k-support and k-breach paths by Matlab R2006a [1].

# 6.1 Experimentation Platform - Sample Results

In the simulation, a set of wireless sensor nodes with cardinality n (n varies from  to  with step ) is randomly 5 20 1and uniformly deployed in the target square region with size × met $e r ^ { 2 } .$ . We change the coverage degree k from  to 900 900 3 with step  for different cases. For each round, we randomly 10 1generate the position of each wireless sensor node. After that, we run Alg.1 to obtain order-k Voronoi diagram (intermediate results), based on which we get the corresponding $k ^ { t h }$ -NP Voronoi diagram. (Some detailed examples are given in the Appendix.)

Next, we show how to find the optimum k-support path and the optimum k-breach path respectively. Figure 1 describes a complete procedure for obtaining an optimum -support path connecting source/destination pair of S and $T$ in a $9 0 0 ~ \times$ $9 0 0 \ m e t e r ^ { 2 }$ 900square region where  wireless nodes have been 900 10randomly deployed. Given the area, deployed sensor nodes and the positions of S and T , we first get the $3 ^ { r d }$ -NP Voronoi 3diagram which is shown in Fig. 1(a). We use different colors to distinguish $3 ^ { r d } .$ -NP Voronoi cells for different sensors such that a $3 _ { r d } { \bf - N P }$ 3 Voronoi cell has the same color as its owner’s. 3The two black nodes inside of the square region denote the positions of S and T respectively.

As we can see from Fig. 1(a), each sensor could have several corresponding $3 ^ { r d } { \bf - N P }$ Voronoi cells. Next, we find the perfect 3support location for each $3 ^ { t h }  – \mathrm { N P }$ Voronoi edge. For all perfect 3support locations (including S and T ) belonging to the same $3 ^ { t \bar { h } }$ -NP Voronoi cell, we sort them in decreasing order by their $3 ^ { r d } .$ -distance, and use line segments to connect them one-by-3one, thus get a graph $G ^ { \prime }$ (shown in Fig. 1(b)). Here, the node set of $G ^ { \prime }$ consists of source/destination pair of vertices $S$ and $T ,$ and perfect support locations for all $\bar { k ^ { t h } } \ – \mathrm { N P }$ Voronoi edges, and the edge set consists of line segments connecting the sorted perfect support locations inside each $k ^ { t h }  – \mathrm { N P }$ Voronoi cell. As we can see, all boundaries in the original $3 _ { r d }$ nearest point Voronoi cell turn into points in the new graph $G ^ { \prime }$ as well. One thing needs to be mentioned that when the boundaries of are not available, our algorithm still gets correct solutions. ΩThen, we assign weights to the edges of graph $G ^ { \prime }$ such that the weight of each edge is equal to the bigger one of two $3 ^ { r d } .$ - 3distance of its two end points’. By considering S and T as the source/destination pair of vertices in graph $G ^ { \prime }$ , the problem becomes to find a minimum weighted path connecting S and $T$ in $G ^ { \prime }$ where the weight of a path is equal to the maximum one among all weights of line segments it contains. By running our k-support path algorithm, we obtain the minimum weight path connecting S and $T$ in graph $G ^ { \prime }$ , which is shown in Fig. 1(c) (the solid path). Clearly, this path can be applied to graph G directly, hence it is the final optimal k-support path. It is worth mentioning that there may exist multiple optimum k-support paths depending on the different ways to connect all perfect support locations of a single $k ^ { t h }  – \mathrm { N P }$ Voronoi cell. In our case, we connect all perfect support locations inside a single $k ^ { t h }  – \mathrm { N P }$ Voronoi cell by sorted $\bar { k } ^ { t h }$ -distance of them in decreasing order such that we get a graph $G ^ { \prime }$ with fewer edges (a tree inside each cell) in order to reduce the time complexity of our algorithms. Some other connection methods also can get optimum solutions, for example, we can connect each pair of perfect support locations inside each $k ^ { t h }  – \mathrm { N P }$ Voronoi cell such as to have a clique.

![](images/f804a9f4b74e12e5043d4de3f9f575b086cb86f8bda403ac4c9c98172e39e0be.jpg)



(a)

![](images/7f05f05a9685d272280664e61de9b914c2e8e85aa50c1f1281748318082a32fe.jpg)



(b)

![](images/b51382ee7a5286bff92393c83081e7ef8c840c071b3616e19c655f11b576ea6a.jpg)



Fig. 1. (a) $3 _ { r d }$ nearest point Voronoi cell of  sensors in a $9 0 0 \times 9 0 0$ $m e t e r ^ { 2 }$ square region. The IDs of nodes have 3 10 900been circled and filled with different colors. Each sensor node’s $3 ^ { t h } \mathrm { - N P }$ Voronoi cell have been filled with the same 3color as its owner’s. Two blace nodes are the source point S and destination point $T$ respectively. (b) Perfect support locations (indicated by black vertices) for each $3 ^ { t h } \mathrm { - N P }$ Voronoi edge (indicated by solid line segments). (c) Planar graph $G ^ { \prime }$ 3consisting of perfect support locations and edges (dotted line segments) connecting the perfect support locations inside each cell. Solid line denotes the optimum k-support path. $\left( k = 3 \right)$ in this case.

According to the optimum k-breach path problem, we have proved that there must exist an optimum k-breach path using $\bar { k } ^ { t h }  – \mathrm { N P }$ Voroni edges only (Theorem 11). Hence, the first step is still to get the $\bar { k } ^ { t h } \mathrm { - N P }$ Voronoi diagam, which is the same operation as obtaining a k-support path (shown in Fig. 1(a’)) did. Next, we consider the graph $G ^ { \prime }$ consisting all $k ^ { t h }  – \mathrm { N P }$ Voronoi edges and $k ^ { t h }  – \mathrm { N P }$ Voronoi vertices. Notice that, if $S$ (resp. T ) is inside some $k ^ { t h }  – \mathrm { N P }$ Voronoi cell, we use the method in Section 5.2 to connect S (resp. T ) to some point on some $k ^ { t h }$ -NP Voronoi edge, please refer to the Fig. 2(a) for illustration. Here, since both S and $T$ are falling in some cells whose edges contain part of boundaries of $\Omega ,$ we use two different ways to handle $S$ and $T$ Ωin order to illustrate different cases. For instance, when all boundaries of are Ωavailable, we draw a line from wireless sensor node (assuming with ID ) to $S$ and further extend the line to the boundary. 0If all boundaries of  are not avaialbe, we can add edges Ωconnecting the destination node $T$ to all vertices of the $\bar { k ^ { t h } }$ - NP Voronoi cell containing $T .$ See Fig. 2(b) for details. Next, after assigning a weight to each edge following the method in Section 5.2 and applying Alg. 5 to graph $G ^ { \prime } { } _ { ; }$ , we obtain an optimum k-breach path finally (shown in Fig. 2(b)). As we can see, although our methods for obtaining the k-support path and the k-breach path are based on same $k ^ { \hat { t } h }$ -NP Voronoi diagram, the intermediate graph $G ^ { \prime } \mathrm { s }$ for them are quite different. For k-suppor path problem, the intermediate graph $G ^ { \prime }$ contains perfect support locations only, each of which is not necessarily a $k ^ { t h }  – \mathrm { N P }$ Voronoi vertex, on the contrary, any vertex in the intermediate graph $G ^ { \prime }$ (when we solve k-breach path problem) is exactly a $k ^ { t h }  – \mathrm { N P }$ Voronoi vertex except the source point S and the destination point $T .$ .

We conduct more simulations and show some typical results as follows. In one set of our simulation, we let the number of sensors n increase gradually from  to  with step $5 ,$ 5 30 5and find the optimum k-breach and k-support paths for each $k \in \{ 1 , 3 , 5 \}$ . The results shown in Fig. 3 and Fig. 4 indicate 1 3 5that both optimum k-support and optimum k-breach decrease with the increment of the number of sensors as we expected.

![](images/5f34cea87b7bfbf454d52233a86a44c898f6a7e7dac4c3b24d3cb10a5cdf0b58.jpg)



Fig. 3. Results for k-support paths.

Clearly, this result can be used to estimate the coverage quality when the number of sensors n and the required coverage degree k are given. If the sensing radius for each sensor node is fixed, it is better to deploy more sensor nodes in order to get better coverage quality. On the contrary, if the sensor can adjust its sensing (coverage) radius by power adjustment, the results presented here could be used to estimate the transmission power needed by sensors such that different requirements (k-support or k-breach) can be satisfied. In addition, we found that when the number of sensors exceeds some threshold value (around  in our case), the decreasing 20trend of the curve in Fig. 3 becomes slowly. This illustrates that there is a tradeoff between the number of sensor nodes needed and the desired coverage quality if the sensing radius of each sensor node is fixed.

![](images/ba851b0276b9d3bf991e9f66f80d55f326ee619e44a1478bc5e7f60e3a31c6a5.jpg)



(a)

![](images/22a9cee5ed9fc4e2accd5c9c134858a9ddf7dcaba7a561fa4e448d94a19dc5ca.jpg)



(b)   
Fig. 2. k-breach path when $k = 3$ and $n = 1 0 .$ . (a) Graph $G ^ { \prime }$ consisting of $3 ^ { r d } { \tt \mathrm { - } } { \mathsf { N P } }$ Voronoi vertices and edges including $S , T$ = 3 = 10 3, and corresponding edges incident to them. (b) The Optimum -breach path (solid line segments) based on graph $G ^ { \prime }$ shown in dash line segments.

![](images/fe2d71a1c330874035c6b296b04d81f579790110f4eced9f44178513ee404e36.jpg)



Fig. 4. Results for k-breach paths.

# 7 RELATED WORK

In order to evaluate the quality of coverage of the sensor network, Meguerdichian et.al [10] formulated the  coverage 1problem under two extreme cases: the best case coverage (maximum support) problem and the worst case coverage (minimum breach) problem. In [10] the authors observed that an optimal solution for the maximum support problem is a path which lies along the edges of the Delaunay triangulation [2] [13], and an optimal solution for the minimum breach problem is a path which lies along the edges of the Voronoi diagram [2] [13]. They further proposed centralized algorithms for both problems. Later, Mehta et.al [11] improved these algorithms and made them more computational efficient.

There were some other work which aimed at solving the 1coverage problem formulated in [10] in a distributed manner. Li et.al [8] showed that the maximum support path can be constructed by only using edges of the relative neighborhood graph (RNG) of the sensor node set. They attempted to address best case  coverage problem in distributed manner. 1This is an improvement since the RNG is a subgraph of the Delaunay triangulation and can be constructed locally. On the other side, Meguerdichian et.al [10] implied that a variation of the localized exposure algorithm presented in [13] can be used to solve the worst case coverage problem locally. Another localized algorithm with more practical assumptions was proposed by Huang et.al [4].

For the general coverage problem, Huang et.al [4] studied the problem of determining if the area is sufficiently kcovered, i.e., every point in the target area is covered by at least k sensors. In [4], the authors formulated the problem as a decision problem and proposed a polynomial algorithm which can be easily translated to distributed protocols. They further extended this problem to three-dimensional sensor networks and proposed the solution in [5]. The connected k-coverage problem was studied and addressed in [18] by Zhou et.al. They studied the problem of selecting a minimum set of sensors which are connected and each point in a target region is covered by at least k distinct sensors. They gave both a centralized greedy algorithm and a distributed algorithm for this problem and showed that their centralized greedy algorithm is near-optimal. Xing et.al [17] explored the problem concerning energy conservation while maintaining both desired coverage degree and connectivity. They studied the integrated work between the coverage degree and the connectivity and proposed a flexible coverage configure protocol.

Some studies focused on the relationship between the coverage degree k, the number of sensors n and the sensing radius r of sensor nodes. Kumar et.al [6] studied the problem of determining the appropriate number of sensors that are enough to provide k-coverage of a region under the condition that sensors are allowed to sleep during most of their lifetime. In [16], Wan et.al analyzed the probability of the k-coverage when the sensing radius or the number of sensors changes while taking the boundary effect into account. To the best of our knowledge, [11], [3] and [15] are the only work which aims to find an optimal k-covered path. In [11], Mehta et al., suggested that the worst case k-coverage problem can be addressed by adopting the kth-NP Voronoi diagram. However, no details of the proposed algorithm were given. In [3], Fang et.al gave a polynomial time algorithm to identify a k-covered path based on binary search and growing disk techniques. Unfortunately, the time complexity of their algorithm can not be bounded if an optimum solution is required. Furthermore, they assume that k is some constant which may reduce the generality of their algorithm. In one of our previous work [15], we designed a centralized polynomial time algorithm which can find optimum k-support path efficiently for general k. In this work, we further improved the time complexity of our centralized algorithms and proposed a distributed algorithm to solve this problem.

# 8 CONCLUSION

In this paper, we proposed polynomial time algorithms for two k-coverage problems, i.e., the optimum k-support path problem and the optimum k-breach path problem in wireless sensor networks. Our algorithms can efficiently find a path connecting two points in a given area where a sensor network is randomly deployed with the best observability (i.e., maximizing the minimum observability of all points on the path), and the worst observability (i.e., minimizing the maximum observability of all points on the path). We proposed a number properties for $k ^ { t h }$ -NP Voronoi diagram, which are new to the literature. These properties may be of independent interests.

# REFERENCES

[1] http://www.mathworks.com/.   
[2] M. de Berg, M. van Kreveld, M. Overmars, and O. Schwarzkopf. Computational geometry: Algorithms and applications. In Spinger, New York, 1997.   
[3] C. Fang and C.P. Low. Redundant coverage in wireless sensor networks. In Proceedings of IEEE ICC, 2007.   
[4] C. Huang and Y. Tseng. The coverage problem in a wireless sensor network. In ACM International Workshop on Wireless Sensor Networks and Applications (WSNA), 2003.   
[5] C. Huang, Y. C. Tseng, , and L. Lo. The coverage problem in threedimensional wireless sensor networks. In Proceedings of IEEE GLOBECOM, 2004.   
[6] S. Kumar, T. Lai, and J. Barlogh. On k-coverage in a mostly sleeping sensor network. In Proceedings of ACM MobiCom pp. 144-158, 2004.   
[7] D. Lee. On k-nearest neighbor voronoi diagrams in the plane. In IEEE Transactions on Computers, 1982.   
[8] X. Li, P. Wan, and O. Frieder. Coverage in wireless ad-hoc sensor networks. In IEEE Transaction on Computers, vol. 52, no. 6, pp. 753- 763, Jun. 2003.   
[9] S. Megerian, F. Koushanfar, M. Potkonjak, and M. Srivastava. Worst and best case coverage in sensor networks. In IEEE Transaction on Mobile Computing, vol. 4, no. 1, pp. 84-92, 2005.   
[10] S. Meguerdichian, F. Koushanfar M. Potkonjak, and M. B. Srivastava. Coverage problems in wireless ad-hoc sensor networks. In Proceedings of IEEE INFOCOM, pp. 139-150, 2001.   
[11] DP. Mehta, MA. Lopez, and L. Lin. Optimal coverage paths in ad-hoc sensor networks. In IEEE International Conference on Communications, volume 1, 2003.   
[12] A. Okabe, B. Boots, K. Sugihara, and S.N. Chiu. Spatial tessellations. In Wiley Series in Probability and Statics, 2000.   
[13] J. O. Rourke. Computational geometry in c. In Cambridge University Press, New York, 1998.   
[14] S. Skyum. A sweepline algorithm for generalized delaunay triangulations. In Technical Report, DAIMI PB-373, CS Dept., Aarhus University,, 1991.

[15] S. Tang, X. Mao, and X.Y. Li. Optimal k-support coverage paths in wireless sensor networks. In IQ2S Workshop of PerCom, 2009.   
[16] P. Wan and C. Yi. Coverage by randomly deployed wireless sensor networks. In IEEE Transactions on Information Theory, vol. 52, pp. 2658-2669, 2006.   
[17] G. Xing, X. Wang, Y. Zhang, C. Lu, R. Pless, and C. Gill. Integrated coverage and connectivity configuration for energy conservation in sensor networks. In ACM Transactions on Sensor Networks, vol. 1, pp. 36-72, 2005.   
[18] Z. Zhou, S. Das, and H. Gupta. Connected k-coverage problem in sensor networks. In Proceedings of ICCCN, 2004.   
[19] S. Zhu and M. Huang. A new parallel and distributed shortest path algorithm for hierarchically clustered data networks. In IEEE Transactions on Parallel and Distributed System, 1998.

![](images/c9fac4d48fe551e001eac838ca885abb8155f86eaf3de9a396d20a8f699b27aa.jpg)



Xufei Mao(M10) is a post doctor in School of Software, Tsinghua University China. He hold PhD(2010) degree at Computer Science from Illinois Institute of Technology. He received MS(2003) and Bachelor degree(1999) at Northeastern University and Shenyang University of Technology respectively. His research interests span wireless ad hoc networks, wireless sensor networks and game theory, etc.

![](images/f40102aec6d2375470894664ae29d8ad232b08dea723652a6777f28895904ac7.jpg)



Yunhao Liu (M02, SM06) received the B.S. degree in automation from Tsinghua University, Beijing, China, in 1995, and the M.S. and Ph.D. degrees in computer science and engineering from Michigan State University, East Lansing, in 2003 and 2004, respectively. He is a Professor with the Tsinghua National Lab for Information Science and Technology, School of Software, and the Director of the MOE Key Lab for Information Security, Tsinghua University. He is also a faculty member with the Department of

Computer Science and Engineering, Hong Kong University of Science and Technology, Hong Kong.

![](images/f97671d24351a2f6c84c41b982a0490923c35c75d1c9517feda841818eb62cba.jpg)



ShaoJie Tang has been a PhD student of Computer Science Department at the Illinois Institute of Technology since 2006. He received BS degree in Radio Engineering from Southeast University, China, in 2006. His research interests include algorithm design and analysis for wireless ad hoc networks, wireless sensor networks, and online social networks.

![](images/aed0c6b1d0817c9327e127a0ab7d8eee470b2221d25041e8a1d25a45d14c6505.jpg)



Huafu Liu is a professor in the Department of Computer Science and Technology Changsha University China. His main research interests include the design and implementation of wireless sensor networks, pattern recognition and etc.

![](images/d11f298efc59ebc6da083080091c2223c72b91df19cbfb0278feb150d28dc691.jpg)



Jiankang Han is an engineer of Tsinghua National Lab of Information Science and Technology. He received BS (2009) and Master (2012) degree in Computer Science from Haishi University, China and Beijing University of Posts and Telecommunications respectively. His research interests include hardware design and implement of wireless sensor networks.

![](images/c8cba2f482abf788cd0ae7ffeaba6b3324d872dcde962e7a0f71c2c0ab1529b9.jpg)



Xiang-Yang Li (M99, SM08)) has been an Associate Professor (since 2006) and Assistant Professor (from 2006) of Computer Science at the Illinois Institute of Technology. He received MS (2000) and PhD (2001) degree at Dept. of CS from University of Illinois at Urbana-Champaign. He received the Bachelor degree at Department of Computer Science and Bachelor degree at Department of Business Management from Tsinghua University, China, both in 1995.