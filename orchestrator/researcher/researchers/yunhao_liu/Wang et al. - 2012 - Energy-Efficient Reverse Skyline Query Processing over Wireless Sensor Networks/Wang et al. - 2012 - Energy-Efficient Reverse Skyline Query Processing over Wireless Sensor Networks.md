# Energy-Efficient Reverse Skyline Query Processing over Wireless Sensor Networks

Guoren Wang, Junchang Xin, Lei Chen, and Yunhao Liu, Senior Member, IEEE

Abstract—Reverse skyline query plays an important role in many sensing applications, such as environmental monitoring, habitat monitoring, and battlefield monitoring. Due to the limited power supplies of wireless sensor nodes, the existing centralized approaches, which do not consider energy efficiency, cannot be directly applied to the distributed sensor environment. In this paper, we investigate how to process reverse skyline queries energy efficiently in wireless sensor networks. Initially, we theoretically analyzed the properties of reverse skyline query and proposed a skyband-based approach to tackle the problem of reverse skyline query answering over wireless sensor networks. Then, an energy-efficient approach is proposed to minimize the communication cost among sensor nodes of evaluating range reverse skyline query. Moreover, optimization mechanisms to improve the performance of multiple reverse skylines are also discussed. Extensive experiments on both real-world data and synthetic data have demonstrated the efficiency and effectiveness of our proposed approaches with various experimental settings.

Index Terms—Reverse skyline, wireless sensor network, query processing, multiple queries optimization.

# 1 INTRODUCTION

AS an important and popular query operator for multi-ple criteria decision making, skyline [1] and its S an important and popular query operator for multivariants, such as constrained skyline [2], dynamic skyline [3], [4], [5], and reverse skyline [5], [6], [7], have been applied in many applications. Given a data set $P ,$ a traditional skyline retrieves all the points in P that are not dominated by others. A point $p _ { 1 }$ dominates another point $p _ { 2 } ,$ , if $p _ { 1 }$ is not worse than $p _ { 2 }$ for each dimension i (i.e., $p _ { 1 } [ i ] \leq p _ { 2 } [ i ] )$ , and $p _ { 1 }$ is better than $p _ { 2 }$ for at least one dimension $j \left( \mathrm { i . e . , } p _ { 1 } [ j ] < p _ { 2 } [ j ] \right)$ . Fig. 1a shows an example of traditional skyline in 2D space and points $p _ { 1 } , p _ { 2 } ,$ and $p _ { 6 }$ are the skyline points.

In addition to traditional skyline, dynamic skyline [3], [4], [5] with respect to qðdenoted as $D S ( q , P ) )$ has been proposed to retrieve all the points that are not dynamically dominated by others. For the sake of simplicity, we adopt the definition of dynamic attributes proposed in [5], [6]. A point $p _ { 1 }$ dynamically dominates $p _ { 2 }$ with respect to qðdenoted as $p _ { 1 } \preceq _ { q } p _ { 2 } )$ , if it holds that: 1) $| p _ { 1 } [ i ] ^ { - } q [ i ] | \leq$ $| p _ { 2 } [ i ] - q [ i ] |$ , for each dimension $i \in D ,$ , and 2) there exists at least one dimension $j \in D ,$ , such that $| p _ { 1 } [ j ] - q [ j ] | < | p _ { 2 } [ j ] -$ q½j-j. In Fig. 1a, points $p _ { 1 } , p _ { 3 } , p _ { 4 } ,$ and $p _ { 5 }$ are the dynamic skyline points of q. For each point $p _ { i } = ( p _ { i } [ 1 ] , p _ { i } [ 2 ] )$ in 2D space, it is transformed to $\tilde { p _ { i } } ^ { \prime } = ( | p _ { i } [ 1 ] - q [ 1 ] | , | p _ { i } [ 2 ] - q [ 2 ] | )$ where query is $q = ( q [ 1 ] , q [ 2 ] )$ Þ. Another topic of interest is reverse skyline [5], [6], [7]. Given a data set P , a reverse skyline with respect to qðdenoted as $R S ( q , P ) )$ retrieves all the points $p \in P$ such that $q \in D S ( p , P )$ . As illustrated in Fig. 1, q belongs to the dynamic skyline of p1 (Fig. 1b), so p1 is a reverse skyline point of q. For the same reason, points $p _ { 3 }$ and $p _ { 5 }$ are also reverse skyline points of q (Fig. 1c).

Recently it is found that wireless sensor networks (WSNs) offer a very economic and effective platform to monitor the environment. To satisfy different application demands, we conduct various types of queries over WSNs, for example min, max [8], top-k [9], [10], and skyline [11], [12]. The de facto limit to processing queries in WSNs is the energy constraint, since sensor nodes are generally battery powered, and in many WSNs (e.g., an unattended and hard-to-reach environment), it is impossible or at least very difficult to change their batteries. Wireless communication is the major energy consumer in WSNs, and therefore, if we can reduce the amount of communication during query processing, the energy consumption can be significantly reduced and the lifetime of the WSNs as a whole can be prolonged.

Each type of query has its unique properties, only after understanding the properties of all kinds of queries we can handle the energy-efficient processing of multiple types of queries. Thus, almost all existing work has focused on reducing the communication cost for a specific type of query [8], [9], [10], [11], [12]. As one of the important operators in WSN applications, the energy-efficiency of RS query processing also needs to be studied in depth. Therefore, in this work, we study energy-efficient approaches to answer reverse skyline (RS) queries over WSNs.

RS is very useful for environmental monitoring applications. We have deployed a real sensor system to monitor the forest environment. By consulting the experienced forestry

G. Wang and J. Xin are with College of Information Science and Engineering, Northeastern University, Wenhua Road 11-3, Heping District, Shenyang, Liaoning 110819, China. E-mail: wanggr@mail.neu.edu.cn, xinjunchang@ise.neu.edu.cn.   
. L. Chen is with the Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong, China. E-mail: leichen@cse.ust.hk.   
. Y. Liu is with the Department of Computer Science and Engineering, Hong Kong University of Science and Technology and the School of Software, Tsinghua University, Beijing 110084, China. E-mail: yunhaoliu@greenorbs.com.

![](images/ec871deef2ed61de016d4c189c88660c6ffa697e8f5cb344bc1a260dde2f5a29.jpg)



(a)

![](images/1242475b81d1c178bd0675502538a85b12802c66f9f85f4c94601e0aec01b8ac.jpg)



(b)

![](images/599af1cbfda021572149944d14e9ef22e08357dd54f1fe71847a6b686efd4353.jpg)



（c)  
Fig. 1. Examples of Skylines. (a) $D S ( q , P _ { 1 } )$ . (b) $D S ( p _ { 1 } , P _ { 1 } )$ . (c) $R S ( q , P _ { 1 } )$ .

workers and experts, for certain dangerous patterns, we can get the critical values of the environment parameters. With these critical values, we can monitor the potential dangers may happen in the sensor networks. That is, the closer the values collected by the sensors to these critical values, the higher probability that a danger may happen in the area monitored by those sensors. In fact, we can treat each of these critical values as a “signature” of a potential danger and use these critical values as the query points, the regions where the query points are in the skyline of their sensor readings can be identified as high-risk areas. Based on the results of the RS query, further steps can be taken to minimize the risks and costs.

Another example that demonstrates the usefulness of the reverse skyline can be found, when studying the behavior of various bird species, ornithologists utilize feeder sensors to determine the places where birds appear most frequently. The sensor reading (temperature, humidity, etc.) collected by WSN reflects the preferences of the birds. If a bird prefers a place, it may prefer the places of the dynamic skyline of the place. If a new location for breeding birds is sought, the results of reverse skyline querying can be employed to identify suitable areas.

Unfortunately, implementing the reverse skyline operator in WSNs is nontrivial since RS is not decomposable (observation 1 in Section 3). This means that we cannot simply distribute tasks (i.e., RS queries) to subsets of data points and then compute the union of the returned RS answers, since the union is not the RS answer over all data points. Thus, existing techniques such as in-network aggregation (e.g., TAG [8]) cannot be used in WSNs to answer RS queries. In order to tackle this problem, in this paper, we propose a novel concept, called semidominance, which uses half distance between a query and a data point to define the dominance relationship. Based on this concept, we define full dominance and in turn full skyline, which can convert the RS problem into a full skyline problem. Interestingly, we prove that the full skyline query is decomposable. As a result, we can utilize in-network processing to reduce communication costs. Furthermore, we define a full skyband and use it to remove false positives during in-network processing. Several variants of RS, such as range RS and multiple RS are studied by adapting the proposed RS solutions.

In summary, we make the following contributions in this paper.

1. We propose an energy-efficient approach to evaluate reverse skyline query in WSNs, based on the full skyband which contains all necessary information for the base station to reconstruct the reverse skyline. Then, the transmission of nonfull skyline points is avoided by pointing out which full skyline points belong to the reverse skyline. Furthermore, the proposed approaches are also extended to support range reverse skyline and multiple reverse skyline queries.

2. We theoretically analyze the relationship between reverse skylines on different dimensional spaces or query ranges, and propose two optimization mechanisms, vertical and horizontal optimizations, to improve the performance of multiple reverse skyline evaluation in WSNs.   
3. Lastly, our extensive experimental studies using both real-world data and synthetic data show that the proposed approach can significantly reduce the communication cost among sensor nodes and save the energy consumption during the evaluation of RS queries in WSNs.

The rest of the paper is organized as follows: Section 2 briefly reviews the related work. The details of traditional and range reverse skyline query evaluation are introduced in Section 3 and Section 4, respectively. Section 5 discusses how to evaluate multiple reverse skyline queries energy efficiently. The experimental results to show the effectiveness of the proposed approaches are reported in Section 6. Finally, Section 7 concludes this paper and discusses the future work.

# 2 RELATED WORK

In the WSN literature, energy-efficient query processing technique has received considerable attention in the past few years. Madden et al. [8] proposed TAG, a typical innetwork aggregation approach for WSNs. TAG first organizes all sensor nodes into a routing tree structure rooted at the base station. When a user query arrives, it sends the query along the routing tree to all sensor node, and then collects the data from the leaf nodes to the root. While processing the query, each intermediate node has to wait for messages from all its children before computing and transmitting the partial aggregation up the network. Chen et al. [11] addressed the problem of continuous skyline monitoring in WSNs and presented a hierarchical threshold-based approach, MINMAX, to minimize the transmission traffic. Xin et al. [13] investigated the problem of maintaining sliding windows skylines over WSNs, in which several types of filters are installed within each sensor to reduce the amount of data transmitted among sensor nodes. Liang et al. [14] proposed distributed algorithms for skyline evaluation and maintenance in WSNs. The proposed algorithms are based on a new concept, local skyline certificate, which has been used to find a global filter. Recently, Xin et al. [12] proposed an Energy-Efficient Multi-Skyline Evaluation algorithm (EMSE) to evaluate multiple skyline queries effectively in WSNs. EMSE utilizes both global and local optimization mechanisms to eliminate unnecessary data transmission. However, the existing works usually focus on decomposable query processing (aggregation, skyline etc.), whereas ours concentrates on the undecomposable reverse skyline query processing in WSNs.

![](images/29d89f9fc1dc78ef7990991b39860dae8b9c48dd9f772386bc70202a9a47867f.jpg)



(a)

![](images/473844af2a471f04c4a73f2d2e6ec360b9971751468d846d692f447da847ecfb.jpg)



(b)

![](images/12d93d613d18666b6b2586533aa70a9f20680c12041dae1b142ab5cf2cecc82d.jpg)



Fig. 2. Observations 1. (a) $R S ( q , P _ { 2 } )$ . (b) $R S ( q , P _ { 1 } \cup P _ { 2 } )$ . (c) RSðq; RSðq; P1Þ [ RSðq; P2ÞÞ.

The concept of dynamic skyline, skyline in the mapped data space, was first introduced by Papadias et al. [3], and the dynamic attributes of each mapped point were defined by several dimension functions. Deng et al. [4] studied the multisource skyline query in road networks, in which the dynamic attributes of each mapped point were defined as the relative network distances to multiple query points. Dellis and Seeger [5] considered the case that all the mapped attributes are the absolute distances to the query point. Based on dynamic skyline, Dellis and Seeger [5] proposed the reverse skyline, retrieving points whose dynamic skyline sets contain the given query point. Furthermore, they proposed a novel concept, called global skyline, which is an upper bound of the actual reverse skyline set. The proposed branch-and-bound algorithm firstly computes the global skyline as the set of candidate reverse skyline points, and then runs a window query for each global skyline point to verify whether it is a reverse skyline point or not. Lian and Chen [6] modeled the probabilistic reverse skyline query on uncertain data, in both monochromatic and bichromatic cases, and proposed effective pruning methods to reduce the search space of query processing. Wu et al. [7] investigated the bichromatic reverse skyline on precise data and proposed several nontrivial heuristics that can optimize the access order of the R-tree to reduce the I/O cost considerably. The reverse skyline processing techniques above are all proposed in a centralized scenario. To our best knowledge, there is no prior work to address reverse skyline queries over WSNs. In this paper, we explore how to energy efficiently evaluate reverse skyline queries in WSNs.

# 3 REVERSE SKYLINE QUERY PROCESSING OVER WSNS

A naive approach for answering reverse skyline queries in WSNs would be a centralized one. That is, all the sensor nodes in the WSN transmit the sensed data to the base station, and then the base station computes the reverse skyline. Obviously, this centralized approach is the most “expensive,” since it needs to transmit all the sensed data back to the base station while the reverse skyline is only a small subset of the sensed data. As we know, if a query is decomposable, in-network aggregation techniques (e.g., TAG [8]) can be used to improve the performance [13]. Formally, we say a query operator $o p$ is decomposable if op has the following properties [15]:

Definition 1. An operator op is decomposable, if it can be computed by another operator g as follows: $\textstyle o p ( \bigcup _ { i = 1 } ^ { n } D _ { i } ) =$ $g ( \bigcup _ { i = 1 } ^ { n } o p ( D _ { i } ) )$ .

For example, skyline and top-k queries are decomposable query operators. As shown in Fig. 3, the top-2 results of $D _ { 1 } , \ D _ { 2 }$ and $D _ { 3 }$ are $\{ 7 , 3 \} , \{ 8 , 6 \}$ , and f9; 5g, respectively. Obviously, the top-2 result of $\textstyle \bigcup _ { i = 1 } ^ { n } D _ { i }$ is f9; 8g, and the top-2 result of $\{ 7 , 3 \} \cup \{ 8 , 6 \} \cup \{ 9 , 5 \}$ is also f9; 8g. They are equal, so the top-2 query is decomposable.

Unfortunately, an RS query is not decomposable. Consider the example in Fig. 2, where the data set involved in Fig. 1a is marked as $P _ { 1 }$ , and that in Fig. 2a is $P _ { 2 }$ . Since $p _ { 1 0 }$ is the only point in $P _ { 2 } ,$ , the reverse skyline of q in $P _ { 2 }$ is $\{ p _ { 1 0 } \}$ . The reverse skylines in data set $P _ { 1 } \cup P _ { 2 }$ are given by $\{ p _ { 1 } , p _ { 3 } , p _ { 5 } \}$ (shown in Fig. 2b), whereas that in the union of reverse skyline sets $R S ( q , P _ { 1 } )$ and $R S ( q , P _ { 2 } )$ is $\{ p _ { 1 } , p _ { 3 } , p _ { 5 } , p _ { 1 0 } \}$ (shown in Fig. 2c). We can see that they are not equal. Thus, we have the following observation.

Observation 1. If $P = P _ { 1 } \cup P _ { 2 } \cup \cdot \cdot \cdot \cup P _ { n } ,$ , then $R S ( q , P ) \neq$ $R S ( q , \cup _ { i = 1 } ^ { n } R S ( q , P _ { i } ) )$ .

In order to enable efficient RS query processing over WSNs, in this section, we first define two novel concepts, semidominance and full dominance, between two data points. Then, based on full dominance, we further define full skyline, which is proven to be a decomposable operator. Interestingly, it can be proven that all the points in the full skyline form a superset of the reverse skyline set. Therefore, we can conduct a full skyline query over a WSN, and derive the RS from the returned full skyline.

![](images/d8503ae63107d18a02816b24f8f943e22f3224e13797efec471553c4954094d3.jpg)



Fig. 3. Decomposability of top-2 query.

![](images/74acd988c2eecd0695ad068e9e7304148ba2455e25b2418861d9e62aa20af71d.jpg)



Fig. 4. Semidominance.

Nonetheless, it is annoying that we cannot completely distinguish the actual RS answers from non-RS answers in the retrieved full skyline set. To eliminate such an obstacle $( \mathrm { i . e . , }$ to filter out all RS false positives), we carefully identify the reasons for RS false positives in the full skyline set, and propose a novel approach that obtains a (decomposable) full skyband set, instead of full skyline (which is a special case of full skyband, i.e., 1-full-skyband). We prove that by returning 2-full-skyband, it is enough to return all the RS answer yet distinguishing RS from non-RS answers in the 2- full-skyband set. This way, we can successfully convert our problem of searching undecomposable RS answers into an operator that finds decomposable (2-full-skyband) operators over WSNs.

# 3.1 Semidominance

In this section, we propose a novel concept, namely semidominance, for the purpose of adapting our RS problem to the WSN environment (discussed later). We use the example depicted in Fig. 4 to illustrate this concept. In particular, we denote q as a query point, and other data points $( \mathrm { i . e . , } p _ { 4 } , p _ { 7 } , p _ { 8 }$ and $p _ { 9 } )$ are to the top-right quadrant of $q .$ Let points $m _ { 4 } , \ m _ { 8 } ,$ , and $m _ { 9 }$ be the midpoints of line segments $q p _ { 4 } , q p _ { 8 } ,$ , and $q p _ { 9 } ,$ , respectively.

Since $m _ { 8 }$ is located in the rectangle (including its borders) with q and $p _ { 7 }$ as its diagonal corner points, it can be proven that point $p _ { 8 }$ dynamically dominates $q$ with respect to $p _ { 7 }$ . In other words, $p _ { 7 }$ cannot be a reverse skyline point of $q .$ Point $p _ { 7 }$ should be a reverse skyline point only when there is no other point’s midpoint contained in the rectangle.

The phenomenon that the midpoint $( \mathrm { e . g . , } m _ { 8 } )$ between a data point $\left( p _ { 8 } \right)$ and a query point $q$ is located in a rectangle with diagonal points from another point $( \mathrm { e . g . , } p _ { 7 } )$ and $q ,$ w e will call semidominance.

Specifically, we say a value $v _ { 1 }$ is semi-no-worse than $v _ { 2 }$ with respect to o (denoted as $v _ { 1 } \dot { \leq } _ { o } v _ { 2 } )$ , if it holds that $( v _ { 1 } - o )$  $\left( v _ { 2 } - o \right) \ge 0$ and $| v _ { 1 } - o | \leq 2 | v _ { 2 } - o | ;$ the value $v _ { 1 }$ is said to be semibetter than $v _ { 2 }$ with respect to o (denoted as $v _ { 1 } \dot { < } _ { o } v _ { 2 } )$ , if it holds that $( v _ { 1 } - o ) \cdot ( v _ { 2 } - \bar { o } ) > 0$ and $| v _ { 1 } - o | < 2 | v _ { 2 } - o |$ . We give the formal definition of semidominance1 as follows:

Definition 2 (Semidominance). A point $p _ { 1 }$ semidominates another point $p _ { 2 }$ with respect to qðdenoted as $p _ { 1 } { \stackrel { . } { = } } q p _ { 2 } )$ , if it

1. The major difference with [5] is that we use $" \leq "$ while they use $^ { \prime \prime } < \cdot ^ { \prime \prime }$ The introduction of $" = "$ leads the necessary and sufficient condition fulfilled, so we can use it to prune non-RS points and return RS points directly. While only the necessary condition in the Lemma 2 of [5] can help to prune non-RS points. If we need RS points, a further verification step has to be taken. For example, we cannot drop $p _ { 7 }$ using Lemma 2 in [5], since there is no point satisfying the condition. A DS query is needed to verify whether q is in the DS of p7. Compared to [5], we improve the retrieval efficiency of RS results.

holds that: 1) $p _ { 1 } [ i ] { \dot { \leq } } _ { q [ i ] } p _ { 2 } [ i ] .$ , for all dimensions $i \in D ,$ , and 2) there exists at least one dimension $j \in D ,$ , such that $p _ { 1 } [ j ] { \dot { < } } _ { q [ j ] } p _ { 2 } [ j ]$ .

In the example of Fig. 4, we know that $p _ { 8 }$ semidominates $p _ { 7 } .$ The following theorem shows that we can make use of semidominance to conduct reverse skyline queries.

Theorem 1. Given a data set $P ,$ any point $p \in P$ is a reverse skyline point of q, iff there does not exist any other point $p ^ { \prime } \in P$ such that $p ^ { \prime } { \overset { \cdot } { \ = } } q p .$ .

Proof. 1. We prove the sufficient condition using reduction to absurdity. Assume $p ~ \notin ~ R S ( q , P )$ , that is $q \not \in$ $D S ( p , P )$ , then we can infer $\exists p ^ { \prime } \in P , p ^ { \prime } \preceq _ { p } q .$ . Therefore, $\forall i \in D , | p ^ { \prime } [ i ] - p [ i ] | \leq | q [ i ] - p [ i ] |$ , and $\exists \bar { j } \in D , | p ^ { \prime } [ j ] -$ $p [ j ] | < | q [ j ] - p [ j ] |$ .

$$
\begin{array}{l} \left| p ^ {\prime} [ i ] - p [ i ] \right| \leq \left| q [ i ] - p [ i ] \right| \Rightarrow \left(q [ i ] - p [ i ]\right) ^ {2} - \left(p ^ {\prime} [ i ] - p [ i ]\right) ^ {2} \geq 0 \\ \Rightarrow (q [ i ] - p ^ {\prime} [ i ]) \cdot (q [ i ] + p ^ {\prime} [ i ] - 2 p [ i ]) \geq 0 \\ \Rightarrow (q [ i ] - p ^ {\prime} [ i ]) \cdot (2 q [ i ] - 2 p [ i ] - q [ i ] + p ^ {\prime} [ i ]) \geq 0 \\ \Rightarrow 2 (q [ i ] - p ^ {\prime} [ i ]) \cdot (q [ i ] - p [ i ]) \geq (q [ i ] - p ^ {\prime} [ i ]) ^ {2} \\ \end{array}
$$

Thus, 8i $\in D , ( p ^ { \prime } [ i ] - q [ i ] ) \cdot ( p [ i ] - q [ i ] ) \geq 0 .$

According to the triangle inequality, we can get $| p ^ { \prime } [ i ] - q [ i ] | \leq | q [ i ] - p [ i ] | + | \check { p ^ { \prime } } [ i ] - p [ i ] |$ . Since it holds that $| p ^ { \prime } [ i ] - p [ i ] | \leq | q [ i ] - p [ i ] |$ , we can get $| p ^ { \prime } [ i ] - q [ i ] | \leq$ $2 | p [ i ] - q [ i ] |$ .

S i m i l a r l y , $| p ^ { \prime } [ j ] - q [ j ] | \leq | q [ j ] - p [ j ] | + | p ^ { \prime } [ j ] - p [ j ] |$ Since $| p ^ { \prime } [ j ] - p [ j ] | < | q [ j ] - p [ j ] |$ holds, we can infer $| p ^ { \prime } [ j ] - q [ j ] | < 2 | p [ j ] - q [ j ] |$ .

$\operatorname { M o r e o v e r , w e ~ h a v e } | p ^ { \prime } [ j ] - p [ j ] | < | q [ j ] - p [ j ] | \Rightarrow p ^ { \prime } [ j ] \neq$ $q [ j ]$ . Thus, $| p ^ { \prime } [ j ] - q [ j ] | > 0$ and $| p [ j ] - q [ j ] | > 0 .$ .

According to Definition $^ { 2 , }$ we have $p ^ { \prime } { \overset { \cdot } { \ = } } q p .$ This contradicts with $\overline { { { \mathcal { A } } } } p ^ { \prime } , \ p ^ { \prime } { \preceq } _ { q } p .$ . Therefore, the sufficient condition must be held.

2. We prove the necessary condition also using reduction to absurdity. Assume $\mathbf { \bar { \exists } } p ^ { \prime } \in P , p ^ { \prime } { \preceq } _ { q } p ,$ according to Definition $^ { 2 , }$ we can infer $\forall i \in D , \ p ^ { \prime } [ i ] { \dot { \leq } } _ { q [ i ] } p [ i ] .$ , and $\exists j \in D , p ^ { \prime } [ j ] { \dot { < } } _ { q [ j ] } p [ j ] .$

Since we have $p ^ { \prime } [ i ] { \dot { \leq } } _ { q [ i ] } p [ i ] .$ , we can infer $( p ^ { \prime } [ i ] - q [ i ] )$  $( p [ i ] - q [ i ] ) \geq 0 .$ , and $| p ^ { \prime } [ i ] - q [ i ] | \leq 2 | p [ i ] - q [ i ] |$ , then we can get $( p ^ { \prime } [ i ] - q [ i ] ) ^ { 2 } \leq 2 ( p ^ { \prime } [ i ] - q [ i ] ) ( p [ i ] - q [ i ] )$ .

Moreover, $( p ^ { \prime } [ i ] - p [ i ] ) ^ { 2 } = ( p ^ { \prime } [ i ] - q [ i ] - p [ i ] + q [ i ] ) ^ { 2 } =$ $( p ^ { \prime } [ i ] - q [ i ] ) ^ { 2 } + ( p [ i ] - q [ i ] ) ^ { 2 } - 2 ( p ^ { \prime } [ i ] - q [ i ] ) ( p [ i ] - q [ i ] )$ .

So, we can infer $\begin{array} { r } { ( p ^ { \prime } [ i ] - p [ i ] ) ^ { 2 } \leq ( p [ i ] - q [ i ] ) ^ { 2 } } \end{array}$

Therefore, $| p ^ { \prime } [ i ] - p [ i ] | \leq | q [ i ] - p [ i ] |$ .

Similarly, since $p ^ { \prime } [ j ] { \dot { < } } _ { q [ j ] } p [ j ]$ , we can infer $| p ^ { \prime } [ j ] - p [ j ] | <$ $| q [ j ] - p [ j ] |$ .

Thus, we can conclude that $\boldsymbol { p ^ { \prime } } \preceq _ { p } \boldsymbol { q }$ and $q ~ \notin ~ D S ( p , P ) .$ , therefore, $p ~ \notin ~ R S ( q , P )$ . This conflicts with condition $p \in R S ( q , P )$ , therefore $\bar { \lambda } p ^ { \prime } \in P , p ^ { \prime } \dot { \preceq } _ { q } p .$ tu

According to Theorem 1, we can rewrite the definition of reverse skyline, and obtain its equivalent semidominance based definition below.

Definition 3 (Reverse Skyline). Given a data set P and a query point q, a reverse skyline query ðdenoted as $R S ( q , P ) )$ retrieves all the points in P that are not semidominated by others with respect to q.

# 3.2 Full Dominance and Full Skyline

Giving rise to the undecomposability of reverse skyline query, the semidominance relation does not have transitivity. Thus, we cannot make use of in-network aggregation techniques. In order to tackle this serious problem over WSNs, our goal is to carefully and properly adjust the relation of semidominance, such that the modified relation becomes transitive (in turn, the query becomes decomposable). After that, we are able to take the advantage of in-network aggregation techniques to efficiently get the query results. This way, the base station can calculate reverse skyline without introducing false dismissals.

In order to achieve the goal above, we introduce another novel concept, namely full dominance, between any two data points. Specifically, we say that a value $v _ { 1 }$ is $f u l l { - } n o -$ worse than another one v2 with respect to o (denoted as $v _ { 1 } \bar { \leq _ { o } } v _ { 2 } )$ , if it holds that $( v _ { 1 } - o ) \cdot ( v _ { 2 } - o ) \geq 0$ and $| v _ { 1 } - o | \leq$ $| v _ { 2 } - o | ;$ the value $v _ { 1 }$ is said to be full better than $v _ { 2 }$ with respect to o (denoted as $v _ { 1 } \bar { < } _ { o } v _ { 2 } )$ , if it holds that $( v _ { 1 } - o )$  $\left( v _ { 2 } - o \right) > 0$ and $| v _ { 1 } - o | < | v _ { 2 } - o |$ . We give the full dominance definition below.

Definition 4 (Full Dominance). A point $p _ { 1 }$ fully dominates another point $p _ { 2 }$ with respect to qðdenoted as $p _ { 1 } { \stackrel { - } { \ = } } q p _ { 2 } )$ , if it holds that: 1) $p _ { 1 } [ i ] { \bar { \leq } } _ { q [ i ] } p _ { 2 } [ i ]$ , for all dimensions $i \in D ,$ , and 2) there exists at least one dimension $j \in D ,$ , such that $p _ { 1 } [ j ] \bar { < } _ { q [ j ] } p _ { 2 } [ j ]$ .

From the definition of full dominance above, we next propose a novel skyline type, called full skyline,2 which is useful for retrieving RS answers over WSNs.

Definition 5 (Full Skyline). Given a data set P and a query point $q ,$ a full skyline query ðdenoted as $F S ( q , P ) )$ retrieves all the points in P that are not full-dominated by others with respect to $q .$

Fig. 5 illustrates a simple example of the full skyline query over data set $P _ { 1 }$ in a 2D temperature-and-humidity space. We can see that point $p _ { 7 }$ full-dominates $p _ { 8 } ,$ , since $p _ { 7 }$ has smaller distance to $q$ than $p _ { 8 }$ on both dimensions. Similarly, point $p _ { 4 }$ full-dominates $p _ { 9 } ,$ and point $p _ { 5 }$ fulldominates $p _ { 6 } .$ . Since points $p _ { 1 } - p _ { 5 }$ and $p _ { 7 }$ are not fulldominated by any other points, we call them full skyline points.

Interestingly, the full-dominance relation is transitive, and the resulting full skyline query is also decomposable. Below, Lemma 1 and Theorem $^ { 2 , }$ respectively, guarantee the correctness of these two assertions.

Lemma 1. If $p _ { 1 } \bar { \preceq } _ { q } p _ { 2 }$ and $p _ { 2 } { \preceq } _ { q } p _ { 3 }$ , then $p _ { 1 } { \preceq } _ { q } p _ { 3 }$ .

2. The detailed definition of global skyline in [5] is shown as follows: a point p1 globally dominates another point p2 with respect to q, if it holds that: 1) 8i 2 $\check { D ^ { \prime } } \left( p _ { 1 } [ i ] ^ { \prime } - q [ i ] \right) \cdot ( p _ { 2 } [ i ] - q [ i ] ) \stackrel { \cdot } { > } 0 , 2 \mathsf { \bar { j } } \forall i \in D , | p _ { 1 } ^ { \cdot } [ i ] - q [ i ] | \leq | p _ { 2 } [ i ] - q [ i ] | ,$ and $3 ) \ \exists j \in { \tilde { D } } , \ | p _ { 1 } [ j ] - q [ j ] | < | { \tilde { p _ { 2 } } } [ j ] - q [ j ] | .$ . The global skyline of a point q contains those points which are not globally dominated by another point with respect to q.

The global dominance requires $\forall i \in D , ( p _ { 1 } [ i ] - q [ i ] ) \cdot ( p _ { 2 } [ i ] - q [ i ] ) > 0 ,$ , while full dominance only requires $\forall i \in D , ( p _ { 1 } [ \dot { i } ] - \dot { q } [ \dot { i } ] ) \cdot ( p _ { 2 } [ \dot { i } ] - \dot { q } [ \dot { i } ] ) \geq 0$ and $\exists j \in D , ( p _ { 1 } [ j ] - q [ j ] ) \cdot { \bar { ( p _ { 2 } [ j ] \cdot { \bar { q } } [ j ] ) } } > 0 .$ . Thus, full skyline is a subset of global skyline. In contrast to the full skylines in Fig. 5, global skylines not only contain all full skyline points $( p _ { 1 } - p _ { 5 }$ and $p _ { 7 } ) ,$ but also contain the nonfull skyline point $p _ { 9 }$ which is not globally dominated by $p _ { 4 } .$ .

![](images/82ef9a4139ff5977104de2c6b02210e9cfe0e19e09436610234ebff0dbcaf2f5.jpg)



Fig. 5. $F S ( q , P _ { 1 } )$ .

Proof. For detailed proofs see Appendix, which can be found on the Computer Society Digital Library at $\mathrm { h t t p } { : } / $ doi.ieeecomputersociety.org/10.1109/2011.64. tu

Theorem 2. If

$$
P = P _ {1} \cup P _ {2} \cup \dots \cup P _ {n}, F S (q, P) = F S (q, \bigcup_ {i = 1} ^ {n} F S (q, P _ {i})).
$$

Proof. 1. We prove $F S ( q , P ) \subseteq F S ( q , \bigcup _ { i = 1 } ^ { n } F S ( q , P _ { i } ) )$ using reduction to absurdity. Assume $p \notin F S ( q , \bigcup _ { i = 1 } ^ { n } F S ( q ,$ ; $P _ { i } ) )$ , then $\exists p ^ { \prime } \in \bigcup _ { i = 1 } ^ { n } F S ( q , P _ { i } ) , \ p ^ { \prime } { \bar { \preceq } } _ { q } p .$ Since $\textstyle \bigcup _ { i = 1 } ^ { n } F S ( q .$ ; $P _ { i } ) \subset P ,$ , we can infer $p ^ { \prime } \in P$ . Therefore, $p \notin \ F S ( q , P )$ .

2. We prove $F S ( q , \bigcup _ { i = 1 } ^ { n } F S ( q , P _ { i } ) ) \subseteq F S ( q , P )$ also using reduction to absurdity. Assume $p \notin \ F S ( q , P ) ,$ , then according to Lemma 1, $\exists p ^ { \prime } \in F S ( q , P ) , p ^ { \prime } { \bar { \preceq } } _ { q } p .$ Since $p ^ { \prime } \in F S ( q , P )$ , we can infer $p ^ { \prime } \in \bigcup _ { i = 1 } ^ { n } F S ( q , P _ { i } )$ . Therefore, $p \ \not \in \ F S ( q , \bigcup _ { i = 1 } ^ { n } F S ( q , P _ { i } ) )$ . tu

Note that, since full dominance has a tighter constraint than semidominance, point $p _ { 1 }$ full-dominating point $p _ { 2 }$ can imply that $p _ { 1 }$ semidominates point $p _ { 2 }$ . Inversely, if a point $p _ { 2 }$ is not semidominated by $p _ { 1 , }$ , then $p _ { 2 }$ is not fulldominated by $p _ { 1 }$ . Therefore, the set of reverse skyline points is a subset of full skylines, which can be summarized in the following theorem.

Theorem 3. $R S ( q , P ) \subseteq F S ( q , P )$ .

Proof. We prove the theorem using reduction to absurdity.

Assume $p ~ \notin ~ F S ( q , P )$ , then $\exists p ^ { \prime } \in P , \ p ^ { \prime } { \bar { \preceq } } _ { q } p$ . Obviously, $p ^ { \prime } \bar { \preceq } _ { q } p \Rightarrow p ^ { \prime } \dot { \preceq } _ { q } p .$ . Thus, $p ~ \notin ~ R S ( q , P )$ .

Therefore, $R S ( q , P ) \subseteq F S ( q , P ) .$ .

Theorem 3 indicates that the two sets $R S ( q , P )$ and $F S ( q , P )$ have containment relationship.

However, if we conduct a reverse skyline query in the full skyline set $F S ( q , P )$ , the resulting set of RS answers is not exactly $R S ( q , P )$ . This is summarized by Observation 2 below.

Observation 2. $R S ( q , P ) \neq R S ( q , F S ( q , P ) )$ .

As an example in Fig. 6, we have a number of reverse skylines obtained from the full skyline of $\begin{array} { r l } { P _ { 1 } } & { { } ( \mathrm { i . e . , } } \end{array}$ $ R S ( q , F S ( q , P ) ) )$ . In contrast to reverse skylines in Fig. 1c $( \mathbf { i . e . } , \ R S ( q , P ) )$ , we can see that not only data points in $R S ( q , P )$ , but also points like $p _ { 4 }$ and $p _ { 7 }$ are included in $R S ( q , F S ( q , P ) )$ . We give a theorem below, indicating that sets $R S ( q , P )$ and $R S ( q , F S ( q , P ) )$ have the containment relationships.

![](images/b5efa571d0c1dde0c16e43512e61147fc0880945c0800b060db39b9f27b5adf3.jpg)



Fig. 6. $R S ( q , F S ( q , P _ { 1 } ) )$ .

Theorem 4. $R S ( q , P ) \subseteq R S ( q , F S ( q , P ) )$ .

Proof. Let $p \in R S ( q , P )$ , then according to Theorem $^ { 3 , }$ $p \in F S ( q , P )$ .

Since we have $p \in R S ( q , P )$ , we can infer $\nexists p ^ { \prime } \in P ,$ $p ^ { \prime } { \overset { \cdot } { \ = } } q p .$

Moreover, since $F S ( q , P ) \subseteq P ,$ we can get $\bar { \boldsymbol { \mu } } \boldsymbol { p ^ { \prime } } \in$ $F S ( q , P ) , p ^ { \prime } \dot { \preceq } _ { q } p$ . Therefore, $p \in R S ( q , F S ( q , P ) )$ . tu

From Theorem 4, we observe that $R S ( q , F S ( q , P ) )$ is a superset of $R S ( q , P )$ , which means that the set $R S ( q ,$ $F \bar { S } ( q , P ) )$ does not miss any points belonging to the RS set. On the other hand, the set $\bar { R S } ( q , F S ( q , \bar { P ) } )$ does contain points not belonging to the set $R S ( q , P )$ . These points cannot be automatically identified. To overcome this problem, we introduce the Full Skyband operator below.

# 3.3 Full Skyband

In order to return the exact RS answer set over WSNs, we now analyze the reason behind the fact that false positives exist in ${ \cal R } S ( q , F S ( q , P ) )$ Þ. We provide the key factor in the following lemma/theorem:

Lemma 2. $I f p _ { 1 } { \preceq } _ { q } p _ { 2 }$ and $p _ { 2 } { \stackrel { . } {  } } q p _ { 3 } ,$ , then $p _ { 1 } { \stackrel { . } {  } } q p _ { 3 }$ .

Proof. For detailed proofs see Appendix, available in the online supplemental material. tu

Theorem 5. Let p be a point not in $R S ( q , P )$ but in $R S ( q , F S ( q , P ) )$ . Then, there must exist another point $p ^ { \prime } \notin$ $F S ( q , P )$ such that $p { \stackrel { - } { = } } q p ^ { \prime }$ and $p ^ { \prime } { \overset { \cdot } { \ = } } q p .$ .

Proof. Since we have $p ~ \notin ~ R S ( q , P )$ , we can infer $\exists p ^ { \prime } \in P .$ $p ^ { \prime } { \overset { \cdot } { \ = } } q p .$ .

Moreover, since we have $p \in R S ( q , F S ( q , P ) )$ , we can infer $p ^ { \prime } \notin F S ( q , P )$ .

Since we have $p ^ { \prime } \notin F S ( q , P )$ , we can also infer $\exists p ^ { \prime \prime } \in F S ( q , P ) , p ^ { \prime \prime } { \overset { . } { \preceq } } _ { q } p ^ { \prime } .$ .

Assume $p ^ { \prime \prime } \neq p ,$ then according to Lemma 2, based on $p ^ { \prime \prime } { \preceq } _ { q } p ^ { \prime }$ and $p ^ { \prime } \dot { \preceq } _ { \boldsymbol { q } \boldsymbol { p } , }$ , we can infer $p ^ { \prime \prime } { \overset { \cdot } { \mathop { \preceq } } } _ { q } p .$ . According to Theorem $1 , p \notin \mathop { R S } ( q , F S ( q , P ) )$ . It contradicts with the condition, so we can conclude that $\boldsymbol { p } ^ { \prime \prime } = \boldsymbol { p }$ holds. Therefore, $p { \stackrel { - } { = } } q p ^ { \prime }$ . tu

For the sake of brevity, we call those points fully dominated by ${ \textit { p } } ^ { \prime \prime } f u l l -$ -dominated points of ${ p , \prime \prime }$ and $p$ is the “full-dominating $p o i n t ^ { \prime \prime }$ of its full-dominated points. Note that, some full skyline points are only semidominated by their full-dominated points, and such full-dominated points have not been included in the full skyline set. As a result, the full skyline points above cannot be pruned during reverse skyline processing using the full skyline results (i.e., $R S ( q , F S ( \dot { q } , P ) ) \big )$ . As shown in Fig. 5, $p _ { 7 }$ is the fulldominating point of $p _ { 8 } ,$ , and $p _ { 8 }$ is the full-dominated point of $p _ { 7 }$ . Although point $p _ { 8 }$ semidominates $p _ { 7 } , \ p _ { 7 }$ is still a reverse skyline point of $F S ( q , P _ { 1 } )$ , because of the absence of $p _ { 8 }$ in $F S ( { \dot { q } } , P _ { 1 } )$ .

In order to eliminate false positives in the full skyline set, we make the following observation: if we can send those data points that are fully dominated by at most one point to the base station, the problem of false positives in the set $R S ( q , F S ( q , P ) )$ can still be easily solved. Inspired by this observation, we propose the concept of full skyband (Definition 6), which is similar to the skyband concept in [3] but with a different dominance semantic. By retrieving full skybands over WSNs, we can obtain the exact RS answers at the base station.

We firstly give the definition of full skyband below.

Definition 6 (Full Skyband). Given a data set P and a query point q, a k-full-skyband query ðdenoted as $F S B ^ { k } ( q , P ) )$ 号 retrieves all points in P that are full-dominated by at most $( k - 1 )$ points with respect to $q .$

In the example of Fig. 5, the 2-full-skyband includes not only all full skyline points, but also the points fulldominated by exactly one point (i.e., p6, p8, and $p _ { 9 } )$ . Thus, all reverse skyline points and full skyline points are included in the 2-full-skyband.

Theorem 6. $R S ( q , P ) = R S ( q , F S B ^ { 2 } ( q , P ) )$ .

Proof. 1. Let $p \in R S ( q , P )$ , according to Theorem 3, we can get $p \in F S ( q , P )$ . Therefore, $p \in \mathring { F S B } ^ { 2 } ( q , P ) )$ .

Based on $F S B ^ { 2 } ( q , P ) \subseteq P$ and $q \in D S ( p , P )$ , we can i n f e r $q \in D S ( p , F S B ^ { 2 } ( q , P ) )$ . T h e r e f o r e , $p \in R S ( q ,$ $F S B ^ { 2 } ( q , P ) )$ .

2. Let $p ~ \notin ~ R S ( q , P )$ , then we can get $\exists p ^ { \prime } \neq p , p ^ { \prime } { \dot { \preceq } } _ { q } p .$

If $p ^ { \prime } \in F S B ^ { 2 } ( q , P )$ , we can infer $\exists p ^ { \prime } \in F S B ^ { 2 } ( \bar { q , + } P ) .$ $p ^ { \prime } { \overset { \cdot } { \ = } } q p .$

If $p ^ { \prime } \notin \mathit { F S B } ^ { 2 } ( q , P ) .$ , according to Definition 6, we can infer $\exists p ^ { \prime \prime } \neq p , p ^ { \prime \prime } \bar { \preceq } _ { q } p ^ { \prime }$ . According to Lemma 2, since $p ^ { \prime \prime } { \overset { \bar { \prec } } { \mathop {  } } } q p ^ { \prime }$ and $p ^ { \prime } { \preceq _ { q } } p ,$ we can get $p ^ { \prime \prime } { \overset { \cdot } { \mathop { \preceq } } } _ { q } p$ . Therefore, $p \notin R S ( q ,$ $F S B ^ { 2 } ( q , \bar { P } ) )$ .

In conclusion, $R S ( q , P ) = R S ( q , F S B ^ { 2 } ( q , P ) )$ .

Note that Theorem 6 indicates that it is sufficient to issue the 2-full-skyband query over WSNs to compute the RS query.

Similar to full skyline, the full skyband is also decomposable, which is shown by the following theorem.

Theorem 7. If $P = P _ { 1 } \cup P _ { 2 } \cup \cdots \cup P _ { n } ,$ then $\begin{array} { r l } { { F S B } ^ { k } ( q , P ) = } \end{array}$ $F S B ^ { k } ( q , \bigcup _ { i = 1 } ^ { n } F S B ^ { k } ( q , P _ { i } ) )$ .

Proof. Immediately deduct from Definition 6.

# 3.4 Reverse Skyline Processing over WSNs

After illustrating the conversion of our RS problem over WSNs into a decomposable 2-full-skyband operator, we are now ready to give our detailed query processing approach in Algorithm 1. Specifically, a sensor node first merges the 2-full-skyband results from its child nodes into its local data set (Lines 1-2). Then, if the intermediate node is the base station, it computes the reverse skylines according to the merged data set (Lines 3-4), otherwise it obtains the 2-fullskyband answers from the merged data set (Lines 5-6). Finally, the node returns the result to the user or its parent node (Line 7).

Algorithm 1: InNetworkRS   
input: $q$ : query point, $P$ : local data set, $R_{i}$ : 2-FSB result of child sensor node $n_i$ . output: $R$ : local result.

1 for the result $R_{i}$ of each child node $n_i$ do
2 $P = P \cup R_i$ 3 if it is the base station then
4 $R = RS(q, P)$ 5 else
6 $R = FSB^2(q, P)$ 7 return $R$ ;

In contrast to full skyline, full skyband also sends those points having only one full-dominating point. Those points certainly do not belong to reverse skyline, since they only have the ability to semidominate their full-dominating points in the full skyline.

According to Lemma 2, the points which can be semidominated by point $p$ can also be semidominated by $p ^ { \prime } \mathbf { s }$ full-dominating point, except for $p ^ { \prime } \mathbf { s }$ full-dominating point itself. Hereby, a point having one full-dominating point cannot affect the reverse skyline judgment of points in another data set, only points in the full skyline are enough, as shown in Theorem 8.

Theorem 8. Let $P _ { 1 }$ and $P _ { 2 }$ be two data sets, and p be a point in $P _ { 1 } .$ . Then, $p \in R S ( q , R S ( q , P _ { 1 } ) \cup F S ( q , P _ { 2 } ) )$ , iff $p \in R S ( q ,$ $P _ { 1 } \cup P _ { 2 } )$ .

Proof. 1. The proof of sufficient condition is similar with Theorem 4. Detail is omitted due to page limitations.

2. We prove the necessary condition using reduction to absurdity. Assume $p \notin \ R S ( q , P _ { 1 } \cup P _ { 2 } )$ , then $\exists p ^ { \prime } \in$ $P _ { 1 } \cup P _ { 2 } , p ^ { \prime } \dot { \vec { \le } } _ { q } p .$ .

There are three conditions for point $p ^ { \prime } { : }$

1. If $p' \in RS(q, P_1) \cup FS(q, P_2)$ , we can directly infer $p \notin RS(q, RS(q, P_1) \cup FS(q, P_2))$ .
2. If $p' \in P_1 - RS(q, P_1)$ , we can infer $p \notin RS(q, P_1)$ . Thus, $p \notin RS(q, RS(q, P_1) \cup FS(q, P_2))$ .
3. If $p' \in P_2 - FS(q, P_2)$ , we can infer $\exists p'' \in FS(q, P_2)$ , $p'' \preceq_q p'$ . According to Lemma 2, we can infer $p'' \preceq_q p$ . So we can get $p \notin RS(q, RS(q, P_1) \cup FS(q, P_2))$ . □

According to Theorem $^ { 8 , }$ we can use a flag to indicate whether a full skyline point is also a reverse skyline point on a sensor node. Then, the parent node can validate whether such reverse skyline points are also reverse skyline points of the sub-tree only with the help of other sibling nodes’ full skylines.

The full skyline having the $f l a g$ to indicate which one belongs to reverse skyline is called the marked full skyline (denoted $F S ^ { * } ( q , P ) )$ . Theorem 9 validates the correctness

TABLE 1 Processing Details on Data Set $P _ { 1 }$ 

<table><tr><td>point</td><td> $R$ </td><td> $F$ </td><td> $D$ </td><td> ${D}^{\prime }$ </td></tr><tr><td> ${p}_{1}$ </td><td> $\left\{  {{p}_{1}}\right\}$ </td><td>0</td><td>0</td><td>0</td></tr><tr><td> ${p}_{5}$ </td><td> $\left\{  {{p}_{1},{p}_{5}}\right\}$ </td><td>0</td><td>0</td><td>0</td></tr><tr><td> ${p}_{2}$ </td><td> $\left\{  {{p}_{1},{p}_{5},{p}_{2}}\right\}$ </td><td>0</td><td>0</td><td>0</td></tr><tr><td> ${p}_{4}$ </td><td> $\left\{  {{p}_{1},{p}_{5},{p}_{2},{p}_{4}}\right\}$ </td><td>0</td><td>0</td><td>0</td></tr><tr><td> ${p}_{9}$ </td><td> $\left\{  {{p}_{1},{p}_{5},{p}_{2}}\right\}$ </td><td> $\left\{  {{p}_{4}}\right\}$ </td><td> $\left\{  {{p}_{4}}\right\}$ </td><td> $\left\{  {{p}_{4}}\right\}$ </td></tr><tr><td> ${p}_{3}$ </td><td> $\left\{  {{p}_{1},{p}_{5},{p}_{3}}\right\}$ </td><td> $\left\{  {{p}_{4},{p}_{2}}\right\}$ </td><td>0</td><td> $\left\{  {{p}_{2}}\right\}$ </td></tr><tr><td> ${p}_{7}$ </td><td> $\left\{  {{p}_{1},{p}_{5},{p}_{3},{p}_{7}}\right\}$ </td><td> $\left\{  {{p}_{4},{p}_{2}}\right\}$ </td><td>0</td><td>0</td></tr><tr><td> ${p}_{6}$ </td><td> $\left\{  {{p}_{1},{p}_{5},{p}_{3},{p}_{7}}\right\}$ </td><td> $\left\{  {{p}_{4},{p}_{2}}\right\}$ </td><td>0</td><td>0</td></tr><tr><td> ${p}_{8}$ </td><td> $\left\{  {{p}_{1},{p}_{5},{p}_{3}}\right\}$ </td><td> $\left\{  {{p}_{4},{p}_{2},{p}_{7}}\right\}$ </td><td> $\left\{  {{p}_{7}}\right\}$ </td><td> $\left\{  {{p}_{7}}\right\}$ </td></tr></table>

of utilizing the marked full skyline to reconstruct the reverse skyline.

Theorem 9. If $P = P _ { 1 } \cup P _ { 2 } \cup \cdot \cdot \cdot \cup P _ { n } ,$ , then $R S ( q , P ) = R S ( q$ $\textstyle \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( q , P _ { i } ) )$ .

Proof. 1. Obviously, $\begin{array} { r } { R S ( q , P ) \subseteq R S ( q , \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( q , P _ { i } ) ) } \end{array}$ .

2. We prove $R S ( q , \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( q , P _ { i } ) ) \subseteq R S ( q , P )$ using reduction to absurdity. Assume $p ~ \notin ~ R S ( q , P )$ , we can infer $\exists p ^ { \prime } , p ^ { \prime } { \preceq } _ { q } p$ . Without loss of generality, we assume $p \in P _ { j }$ . There are two cases for $p ^ { \prime }$ that need to be considered:

1. If $p ^ { \prime } \in P _ { j }$ , we can infer $p \in \overline { { R S } } ( q , P _ { j } )$ . From this, we can further infer p 62 $R S ( q , \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( q , P _ { i } ) )$ .   
2. If $p ^ { \prime } \notin { \cal P } _ { j } ,$ we can infer $p ^ { \prime } \in \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( q , P _ { i } )$ or $\exists p ^ { \prime \prime } \in \bigcup _ { i = 1 } ^ { n ^ { \cdot } } F S ^ { * } ( q , P _ { i } ) , p ^ { \prime \prime } \bar { \preceq } _ { q } p ^ { \prime } .$

Whether $p ^ { \prime } \in \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( q , P _ { i } )$ or $\exists p ^ { \prime \prime } \in \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( q , P _ { i } ) ,$ , we can infer $p \ \notin \ R S ( q , \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( q , P _ { i } ) )$ . tu

According to Theorems 2 and 9, an intermediate node can get both full skyline and reverse skyline correctly merely by depending on the marked full skylines of its child nodes.

The computational process for the marked full skyline is given in Algorithm 2. The program scans the data points in data set P in a presorted ord $\mathrm { e r } ^ { 3 }$ (Line 1), which ensures that the later point cannot fully dominate the former one. Let F denote the set of points belonging to the full skyline but not belonging to the reverse skyline. If data point p is not dominated by any point in F (Line 2), we compute its full-dominating point set D from the reverse skyline candidate set R (Line 3). If D is empty, it means that point $p$ is a full skyline point (Line 4). Next, we compare p with all the full skyline points in $( F \cup R )$ (Line 5). If $p$ is semidominated by any point in $( F \cup R ) , \ p$ is a non-RS point, and we thus add $p$ to $F$ (Line 6). Otherwise, if $p$ is not semidominated by any point in $( F \cup R ) , \ p$ is an RS candidate, and we add it to R (Lines $7 – 8 )$ . If $p$ has only one full-dominating point, it means that $p$ is not a full skyline point but belongs to 2-full-skyband (Line 9). Next, we obtain those points which are semidominated by p in $R ,$ and then move those points from R to F (Lines 10-12). Finally, the algorithm returns the results of both the reverse skyline $( \mathbf { i . e . } , \ R S ( q , P ) )$ as well as the full skyline excluding the reverse skyline $( { \mathrm { i . e . , ~ } } \ F S ( q , P ) - R S ( q , P ) )$

3. Any monotone scoring function would be fine. In this paper, we use the euclidean distance between the data poin $p$ and query point q.

![](images/77af1c5f4f1c41f3e7a308d7b8c3ca9964791de5e09bee063c88f2649520a735.jpg)



Fig. 7. Range reverse skyline.

(Line 13). Table 1 shows the computational process on data set P1 given in the example depicted in Fig. 5.

Algorithm 2:LocalRS&FS   
input : q : query point,
    P : pre-sorted data set.
output: R : RS(q, P),
    F : FS(q, P) - RS(q, P).

1 for each data point p in P do
2    if p.isDominatedBy(F) == false then
3    D = p.getDominating(R);
4    if |D| = 0 then
5    if p.isSemiDominatedBy(F ∪ R) then
6    | F = F ∪ {p};
7    else
8    R = R ∪ {p};
9    if |D| ≤ 1 then
10    D' = p.getSemiDominated(R);
11    R = R - D';
12    F = F ∪ D';
13 return;

# 4 RANGE REVERSE SKYLINE

When a user continuously asks for the reverse skyline while moving around, a better alternative is to submit a single query around the current location into WSN to fetch all possible results for this area. Similar to range nearest neighbor query [16], we propose a range reverse skyline query, which retrieves the reverse skyline for every point in a querying region. The range reverse skyline can solve the problem of the continuous RS mentioned above.

Definition 7 (Range Reverse Skyline). Given a data set P and a querying region Q, a range reverse skyline query ðdenoted as $R S ( Q , P ) )$ retrieves the union of reverse skylines of P with respect to every query point in Q.

Fig. 7 gives an example of range reverse skyline on data set $P _ { 1 }$ . Points $p _ { 1 } - p _ { 5 }$ and $p _ { 7 }$ belong to at least one reverse skyline with respect to the query points in query range $Q .$ Thus, all of these are $Q ^ { \prime } \mathbf { s }$ range reverse skyline points, and the union of these points forms the range reverse skyline of $Q .$ .

![](images/52813faf23f435c48fafa3cab7983494262c9a0b7120aa1ba953af50255686cc.jpg)  
Fig. 8. Range relations.

Since the number of points in query range $Q$ is infinite, it is impossible to carry out the range reverse skyline by first computing the reverse skyline of each point in $Q$ and then merging all of them. As an extension of traditional reverse skyline, we want to explore if the range reverse skyline query has the same characteristics.

We denote the interval $[ o ^ { - } , o ^ { + } ]$ as O. Let $v _ { 1 } \dot { \leq } _ { O } v _ { 2 }$ stand for $\forall o \in O , v _ { 1 } \dot { \leq } _ { o } v _ { 2 } ,$ and $v _ { 1 } \dot { < } _ { O } v _ { 2 }$ stand for $\forall o \in O , v _ { 1 } \dot { < } _ { o } v _ { 2 }$ . Then, similar to the semidominance, we can define a concept, called range semidominance, as given in Definition 8 below.

Definition 8 (Range Semidominance). A point $p _ { 1 }$ range semidominates $p _ { 2 }$ with respect to Qðdenoted as $p _ { 1 } { \overset { . } { \mathop {  } } } _ { Q } p _ { 2 } )$ , if it holds that: 1) $p _ { 1 } [ i ] { \dot { \leq } } _ { Q [ i ] } p _ { 2 } [ i ] ,$ , for all dimensions $i \in D ,$ , and 2) there exists at least one dimension $j \in D , p _ { 1 } [ j ] { \dot { < } } _ { Q [ j ] } p _ { 2 } [ j ]$ .

In interval $O ,$ since the possible value of o is infinite, it is difficult to judge whether or not $v _ { 1 } \dot { \leq } _ { O } v _ { 2 } ( v _ { 1 } \dot { < } _ { O } v _ { 2 } )$ is fulfilled.

Let us first consider the example in Fig. 8. We find that $v _ { 1 } \dot { \leq } _ { O } v _ { 2 }$ holds, if and only if at least one of the three cases below holds: 1) $\begin{array} { r } { \left) v _ { 1 } \leq o ^ { - } , v _ { 2 } \leq o ^ { - } \right. } \end{array}$ and $o ^ { - } - v _ { 1 } \le 2 ( o ^ { - } - v _ { 2 } ) ; 2 ) o ^ { + } \le v _ { 1 }$ , $o ^ { + } \leq v _ { 2 }$ and $v _ { 1 } - o ^ { + } \leq 2 ( v _ { 2 } - o ^ { + } )$ ; and $3 ) o ^ { - } \leq v _ { 1 } = v _ { 2 } \leq o ^ { + }$ . If none of the above cases hold, then we can find an $o \in O$ that can make $v _ { 1 } \dot { \leq _ { o } } v _ { 2 }$ not be fulfilled. The above properties are summarized in Lemma 3.

Lemma 3. Given an interval $O = [ o ^ { - } , o ^ { + } ]$ , it holds that $v _ { 1 } \dot { \leq } _ { O } v _ { 2 } ,$ iff we have: 1) $v _ { 1 } \dot { \leq } _ { o ^ { - } } v _ { 2 } , 2 ) \ v _ { 1 } \dot { \leq } _ { o ^ { + } } v _ { 2 } ,$ and $3 ) \ ( v _ { 1 } - o ^ { - } ) \cdot ( v _ { 1 } -$ $o ^ { + } ) \geq 0 o r v _ { 1 } = v _ { 2 } .$

Proof. For detailed proofs see Appendix, available in the online supplemental material. tu

The operator $v _ { 1 } \dot { < } _ { O } v _ { 2 }$ is defined similarly to $v _ { 1 } \dot { \leq } _ { O } v _ { 2 }$ . Clearly, $v _ { 1 } \dot { < } _ { O } v _ { 2 }$ is not fulfilled on $v _ { 1 } { \dot { \leq } } _ { O } v _ { 2 } { ' }$ condition 2. Thus, in order to make $v _ { 1 } \dot { < } _ { O } v _ { 2 }$ fulfilled, one of the two following conditions is needed: 1) $v _ { 1 } < o ^ { - } , ~ v _ { 2 } < o ^ { - }$ and $o ^ { - } - v _ { 1 } <$ $2 ( o ^ { - } - v _ { 2 } ) ;$ or 2) $\ : o ^ { + } < v _ { 1 } , o ^ { + } < v _ { 2 } \ :$ and $v _ { 1 } - o ^ { + } < 2 ( v _ { 2 } - o ^ { + } )$ . The above properties are summarized in Lemma 4.

Lemma 4. Given an interval $O = [ o ^ { - } , o ^ { + } ] ,$ , it holds that $v _ { 1 } \dot { < } _ { O } v _ { 2 } , i f f$ we have: $1 ) ~ v _ { 1 } \dot { < } _ { o ^ { - } } v _ { 2 } , ~ 2 ) ~ v _ { 1 } \dot { < } _ { o ^ { + } } v _ { 2 }$ , and 3) $( v _ { 1 } - o ^ { - } )$  $\left( v _ { 1 } - o ^ { + } \right) > 0 .$ .

Proof. For detailed proofs see Appendix, available in the online supplemental material. tu

Lemmas 3 and 4 make the judgement of rangesemidominance feasible and much easier. Theorem 10 below illustrates the consanguineous relationship between range reverse skyline and range semidominance.

Theorem 10. Given a data set $P ,$ point $p \in P$ is a range reverse skyline point of Q, iff there does not exist any other point $p ^ { \prime } \in P$ such that $p ^ { \prime } { \preceq _ { Q P } } .$

Proof. 1. We prove the sufficient condition using reduction to absurdity. Assume $p \notin R S ( Q , P )$ .

For each dimension $i \in D ,$ the value of point p must satisfy one of the following three conditions: 1) $p [ i ] \geq$ $Q [ i ] ^ { + } , 2 ) ~ p [ i ] \leq Q [ i ]$ , or 3) $\smile ( i ) ^ { - } < p [ i ] < Q [ i ] ^ { + }$ .

Then, we construct a query point $q ^ { \prime }$ as follow:

I $\left. \begin{array} { r l } & { [ \mathbf { \lambda } ] ) , q ^ { \prime } [ i ] = Q [ i ] ^ { + } , \mathbf { i f } \mathbf { \lambda } 2 ) \widehat { , } q ^ { \prime } [ i ] \widehat { = } Q [ i ] ^ { - } , \mathbf { i f } \mathbf { \lambda } 3 ) , q ^ { \prime } [ i ] = p [ i ] . } \end{array} \right.$

Obviously, the constructed query point satisfies that $q ^ { \prime } \in Q$ .

Since we assumed that $p ~ \notin ~ R S ( Q , P )$ , we can infer $p ~ \notin ~ R S ( q ^ { \prime } , P )$ , thus $\exists p ^ { \prime } , p ^ { \prime } { \preceq } _ { q ^ { \prime } } p .$

Since $p ^ { \prime } { \preceq } _ { q ^ { \prime } } p ,$ we can get $\forall i \in D , p ^ { \prime } [ i ] { \dot { \leq } } _ { q ^ { \prime } [ i ] } p [ i ]$ and $\exists j \in D , p ^ { \prime } [ j ] { \dot { < } } _ { q ^ { \prime } [ j ] } p [ j ]$ .

If $p [ i ] \geq Q [ i ] ^ { + }$ , we can get $q ^ { \prime } [ i ] = Q [ i ] ^ { + }$ . Moreover, we have $p ^ { \prime } [ i ] { \dot { \leq } } _ { q ^ { \prime } [ i ] } p [ i ]$ , we can further infer $p ^ { \prime } [ i ] \geq Q [ i ] ^ { + }$ .

If $\begin{array} { r } { p [ i ] \le Q [ i ] ^ { - } . } \end{array}$ , we can get $q ^ { \prime } [ i ] = Q [ i ] ^ { - }$ . Moreover, we have $p ^ { \prime } [ i ] { \dot { \leq } } _ { q ^ { \prime } [ i ] } p [ i ] ,$ , we can further infer $p ^ { \prime } [ i ] \leq Q [ i ] ^ { - }$ .

If $Q [ i ] ^ { - } < p [ i ] < Q [ i ] ^ { + }$ , we can get $q ^ { \prime } [ i ] = p [ i ]$ . Moreover, we have $p ^ { \prime } [ i ] { \dot { \leq } } _ { q ^ { \prime } [ i ] } p [ i ]$ , we can further infer $p ^ { \prime } [ i ] = p [ i ]$ .

According to Lemma 3, we can infer $p ^ { \prime } [ i ] { \dot { \leq } } _ { Q [ i ] } p [ i ]$ . Similarly, according to Lemma 4, we can also infer $p ^ { \prime } [ j ] { \dot { < } } _ { Q [ j ] } p [ j ]$ , therefore, we have $p ^ { \prime } { \preceq } _ { Q p . }$ .

2. We prove the necessary condition using reduction to absurdity. Assume $\exists p ^ { \prime } \in \dot { P } , p ^ { \prime } { \dot { \preceq } } _ { Q P }$ , we can infer $\forall i \in$ $D , p ^ { \prime } [ i ] { \dot { \leq } } _ { Q [ i ] } { \dot { p } } [ i ]$ and $\exists j , p ^ { \prime } [ j ] \dot { < } _ { Q [ j ] } p [ j ]$ .

Since we have $p ^ { \prime } [ i ] { \dot { \leq } } _ { Q [ i ] } p [ i ]$ , we can infer $\forall q [ i ] \in$ $Q [ i ] , p ^ { \prime } [ i ] \dot { \leq } _ { q [ i ] } p [ i ]$ .

Since we have $p ^ { \prime } [ j ] { \dot { < } } _ { Q [ j ] } p [ j ]$ , we can infer $\forall q [ j ] \in Q [ j ]$ ; $p ^ { \prime } [ j ] { \dot { < } } _ { q [ j ] } p [ j ]$ .

Thus, we get $\forall q \in Q , p ^ { \prime } { \overset { . } { \mathop {  } } } _ { Q } p ,$ , therefore, we can conclude that $q ~ \notin \ R S ( Q , P )$ . tu

According to Theorem 10, range reverse skyline is the set of points in P that are not range semidominated with respect to Q. It is obvious that range reverse skyline query is not decomposable either. Similar to the RS query, we can utilize a series of concepts with respect to the range reverse skyline query, such as range full dominance, range full skyline, and range full skyband to solve this problem.

Specifically, let $v _ { 1 } \bar { \leq } _ { O } v _ { 2 }$ stand for $\forall o \in O , ~ v _ { 1 } \underline { { { \bar { \zeta } } } } _ { o } v _ { 2 } ,$ and $v _ { 1 } \bar { < } _ { O } v _ { 2 }$ stand for $\forall o \in O , v _ { 1 } \bar { < } _ { o } v _ { 2 }$ . We have:

Definition 9 (Range Full Dominance). A point $p _ { 1 }$ range fulldominates $p _ { 2 }$ with respect to Qðdenoted as $p _ { 1 } { \bar { \preceq } } _ { Q } p _ { 2 } )$ , if it holds that: 1) $p _ { 1 } [ i ] { \bar { \leq } } _ { Q [ i ] } p _ { 2 } [ i ]$ for all dimensions $i \in D ,$ , and 2) there exists at least one dimension $j \in D , p _ { 1 } [ j ] \bar { < } _ { Q [ j ] } p _ { 2 } [ j ]$ .

Definition 10 (Range Full Skyline). Given a data set P and a q u e r y i n g r e gi o n Q, a r a nge f ul l s kyl i ne que ry ðdenoted as $F S ( Q , P ) )$ retrieves all the points in P that are not range full-dominated by others with respect to Q.

Definition 11 (Range Full Skyband). Given a data set P and a querying region Q, a k-range-full-skyband query ðdenoted $\bar { F S B ^ { k } ( Q , P ) } )$ retrieves all the points in P that are range full-dominated by at most $( k - 1 )$ points with respect to Q.

As illustrated in Fig. 8, in order to fulfill $v _ { 1 } \bar { \leq _ { O } } v _ { 2 }$ , we need to consider three cases: 1) $v _ { 2 } \leq v _ { 1 } \leq o ^ { - } ; ~ 2 ) ~ o ^ { + } \leq v _ { 1 } \leq v _ { 2 } ;$ and 3) $o ^ { - } \leq v _ { 1 } = v _ { 2 } \leq o ^ { + }$ . However, to fulfill $v _ { 1 } \bar { < } _ { O } v _ { 2 } .$ , we only need to consider two cases: 1) $v _ { 2 } < v _ { 1 } < o ^ { - } ;$ and 2) $o ^ { + } <$ < $v _ { 1 } < v _ { 2 }$ . Theorem 11 formally presents this property.

Theorem 11. Given an interval $O = [ o ^ { - } , o ^ { + } ] , ~ v _ { 1 } \bar { \leq } _ { O } v _ { 2 }$ , iff it holds that: $1 ) \ v _ { 1 } \underline { { { \zeta } } } _ { o ^ { - } } v _ { 2 } ,$ and $2 ) \ v _ { 1 } \bar { \leq } _ { o ^ { + } } v _ { 2 } . \ v _ { 1 } \bar { < } _ { O } v _ { 2 }$ , iff it holds that: 1) $v _ { 1 } \dot { < } _ { o ^ { - } } v _ { 2 } ,$ , and $2 ) \ v _ { 1 } \bar { < } _ { o ^ { + } } v _ { 2 }$ .

Proof. The proof is similar to that of Lemmas 3 and 4. tu

Through further analysis, range semidominance and range full dominance have similar properties, compared with semidominance and full dominance (discussed in Section 3), respectively. The details are given below.

Theorem 12. $R S ( Q , P ) = R S ( Q , F S B ^ { 2 } ( Q , P ) )$ .

Proof. 1. Let $p \in R S ( Q , P )$ , we can get $p \in F S ( Q , P )$ . Based on this, we have $p \in F S B ^ { 2 } ( Q , P ) )$ .

Since we have $p \in R S ( Q , P ) .$ , we can infer $\nexists p ^ { \prime } \in P ,$ ; $p ^ { \prime } { \preceq _ { Q } } p$ . Based on this, we have $\mathrm { \bar { \it { A } } } p ^ { \prime } \in F S B ^ { 2 } ( Q , P ) , \dot { p ^ { \prime } } \dot { \vec { \it { \Delta } } } _ { Q } p ,$ , therefore, $p \in R S ( Q , F S B ^ { 2 } ( q , P ) )$ .

2. We prove $R S ( Q , F S B ^ { 2 } ( Q , P ) ) \subseteq R S ( Q , P )$ using reduction to absurdity. Assume $p \notin \ R S ( Q , P ) .$ , we can get $\exists p ^ { \prime } \neq p , p ^ { \prime } { \dot { \preceq } } _ { Q } p .$ .

If $p ^ { \prime } \in F S B ^ { 2 } ( Q , P )$ , we can get $\exists p ^ { \prime } \in F S B ^ { 2 } ( Q , P ) .$ $p ^ { \prime } { \preceq } _ { Q p . }$ .

If $p ^ { \prime } \notin \mathit { F S B ^ { 2 } } ( Q , P )$ , according to Definition 11, we can infer $\exists p ^ { \prime \prime } \neq p , p ^ { \prime \prime } { \vec { \preceq } } _ { Q } p ^ { \prime } .$ .

According to Lemma 2, based on $p ^ { \prime \prime } { \overset { \bar { \prec } } { \mathop {  } } } q p ^ { \prime }$ and $p ^ { \prime } { \preceq _ { Q P } } ,$ we have $p ^ { \prime \prime } { \overset { . } { \preceq } } _ { Q } p .$ . Therefore, $p \ \notin \ R S ( Q , F S B ^ { 2 } ( Q , P ) )$ .

In conclusion, $R S ( Q , P ) = R S ( Q , F S B ^ { 2 } ( Q , P ) ) ,$

tu

Theorem 13. If $P = P _ { 1 } \cup P _ { 2 } \cup \dots \cup P _ { n } , \ R S ( Q , P ) = R S ( Q _ { : }$ $\textstyle \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( Q , P _ { i } ) )$ . Where $F S ^ { * } ( Q , P _ { i } )$ is the marked range full skyline with respect to Q.

Proof. 1. Clearly, $\begin{array} { r } { R S ( Q , P ) \subseteq R S ( Q , \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( Q , P _ { i } ) ) } \end{array}$ .

2. We prove $R S ( Q , \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( Q , \hat { P _ { i } } ) \big ) \subseteq R S ( Q , P )$ using reduction to absurdity. Assume $p \notin \ R S ( Q , P ) .$ , we can infer $\exists p ^ { \prime } , p ^ { \prime } { \preceq } _ { Q } p .$ . Without loss of generality, we assume $p \in P _ { j }$ . There would be two cases for $p ^ { \prime } { : }$

1. If $p ^ { \prime } \in P _ { j } ,$ we can infer $p \in { \overline { { R S } } } ( Q , P _ { j } ) . 5 \mathrm { o } ,$ , we can further infer $p \ \notin \ R S ( Q , \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( { \dot { Q } } , P _ { i } ) )$ .

2. If $p ^ { \prime } \notin P _ { j } ,$ we can infer $p ^ { \prime } \in \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( Q , P _ { i } )$ or $\exists p ^ { \prime \prime } \in \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( Q , P _ { i } ) , p ^ { \prime \prime } { \overset { - } { \preceq } } _ { Q } p ^ { \prime } .$

3. Whether

$$
p ^ {\prime} \in \bigcup_ {i = 1} ^ {n} F S ^ {*} (Q, P _ {i}) \text {or} \exists p ^ {\prime \prime} \in \bigcup_ {i = 1} ^ {n} F S ^ {*} (Q, P _ {i}),
$$

we can both infer $p \notin R S ( Q , \bigcup _ { i = 1 } ^ { n } F S ^ { * } ( Q , P _ { i } ) )$ .

tu

Range reverse skyline has all the attractive properties that traditional reverse skyline has. Thus, optimization techniques used by traditional reverse skyline can be also applied in range reverse skyline directly. The only difference is that traditional relation/query needs to be replaced by range relation/query. Because the optimization principle is identical, as a particular case of range reverse skyline, traditional reverse skyline can also be processed by this algorithm without leading to any additional computational cost and data transmission.

Because of this, range reverse skyline and traditional reverse skyline are unified. Unless otherwise specified, we will not make distinction between them and both will go by the general name of reverse skyline in the following discussions.

![](images/48c28f84857d0d828e34d2ea86f099d15c81d0e02f3236975e9b59080633ee51.jpg)



Fig. 9. $R X ( q , P _ { 1 } )$

# 5 MULTIPLE REVERSE SKYLINES

In real applications, different users may have different preferences, and it is quite common to have multiple queries in different subspaces which are posed into the WSN simultaneously to gather interesting information [12]. It is not efficient to individually evaluate them especially in a WSN environment where the power consumption should be minimized.

In this section, first, the basic principles of an optimization technique are introduced. Then, the optimization mechanism of multiple reverse skylines is proposed based on these basic principles.

# 5.1 Optimization Principles

In this section, we propose an effective optimization technique, called Vertical Optimization, for multiple queries by using the relationship between reverse skylines with respect to different subspaces but the same query range. Then, we will illustrate another technique, namely Horizontal Optimization, by using the relationship between reverse skylines with the same subspace but different query ranges.

# 5.1.1 Vertical Optimization

When two reverse skyline queries have the same range and their subspaces have the inclusion relationship, their RS results do not directly have the inclusion relationship.

As shown in Fig. 1, the RS set of data set $P _ { 1 }$ in 1D temperature space is $\{ p _ { 4 } , p _ { 9 } \}$ , whereas that in 2D temperature-and-humidity space is $\{ p _ { 1 } , p _ { 3 } , p _ { 5 } \}$ . Thus, we cannot achieve the goal of optimization by simply merging the two queries into one.

Similar to the processing procedure for multiple skylines [17], [12], we convert semidominance into strict semidominance, resulting in the extended reverse skyline. Thus, the reverse skyline in all subspaces are included in the result set of the extended reverse skyline.

Definition 12 (Strict Semidominance). A point $p _ { 1 }$ strictly semidominates $p _ { 2 }$ in a subspace D with respect to Qðdenoted as $p _ { 1 } { \dot { \prec } } _ { Q } ^ { D } p _ { 2 } )$ , if it holds that $p _ { 1 } [ i ] { \dot { < } } _ { Q [ i ] } p _ { 2 } [ i ] , f o r$ all dimensions $i \in D$ .

Definition 13 (Extended Reverse Skyline). Given a data set P and a querying region Q, an extended reverse skyline query in a subspace Dðdenoted as $R X ( Q , P , D ) )$ retrieves all the points in P that are not strictly semidominated by others with respect to Q in subspace D.

![](images/601f54110e3845c0de0f4af34d3101f1edd989ed68ac094a0fe7835da1894122.jpg)



Fig. 10. $F X ( q , P _ { 1 } )$

As shown in Fig. 9, compared with reverse skyline, the extended reverse skyline includes not only reverse skyline points $p _ { 1 } , p _ { 3 } ,$ , and $p _ { 5 } ,$ , but also those semidominated but not strictly semidominated data points $p _ { 4 } , p _ { 7 } ,$ and $p _ { 9 } .$ . Except for those points, no matter in which subspaces, other data points always have one extended reverse skyline point that can strictly semidominate it. The following theorem describes the above property in details.

Theorem 14. If $D _ { 1 } \subseteq D _ { 2 }$ , then we have $R S ( Q , P , D _ { 1 } ) \subseteq$ $R X ( Q , P , D _ { 2 } )$ .

Proof. We prove the theorem using reduction to absurdity. Assuming Since w $p \notin R X ( Q , P , D _ { 2 } )$ , we canan infer $\exists p ^ { \prime } \in P , p ^ { \prime } { \dot { \prec } } _ { Q } ^ { D _ { 2 } } { \dot { p } } .$ $p ^ { \prime } \dot { \prec } _ { Q } ^ { D _ { 2 } } p ,$ $\forall i \in D _ { 2 } , p ^ { \prime } [ i ] \dot { < } _ { Q [ i ] } \check { p } [ i ]$ Since we also have $D _ { 1 } \subseteq D _ { 2 } ,$ , we can infer $\forall i \in D _ { 1 }$ $p ^ { \prime } [ i ] { \dot { < } } _ { Q [ i ] } p [ i ]$ . According to Definition 12, we have D $p ^ { \prime } { \dot { \prec } } _ { Q } ^ { D _ { 1 } } p .$ ½ -Based on this, we can further infer $p ^ { \prime } { \dot { \preceq } } _ { Q } ^ { D _ { 1 } } p .$ Q . Therefore, $p \notin { R S } ( Q , P , D _ { 1 } )$ . tu

Since the extended reverse skyline is only a simple expansion of reverse skyline, we can use the same algorithm to solve it. The difference is that, we should use extended full skyline with strict full dominance, rather than the full skyline as mentioned earlier. The definitions of strict full dominance and extended full skyline4 are given as follows:

Definition 14 (Strict Full Dominance). A point $p _ { 1 }$ strictly full-dominates p2 in a subspace D with respect to Qðdenoted $p _ { 1 } { \dot { \prec } } _ { Q } ^ { D } p _ { 2 } )$ , if it holds that $p _ { 1 } [ i ] \bar { < } _ { Q [ i ] } p _ { 2 } [ i ] .$ , for all dimensions $i \in \dot { D }$ .

Definition 15 (Extended Full Skyline). Given a data set P and a querying region Q, an extended full skyline query in a subspace Dðdenoted $F X ( Q , P , D ) )$ retrieves all the points in P that are not strictly full-dominated by others with respect to Q in subspace D.

Fig. 10 gives an example of the extended full skyline, compared with full skyline. There are some points that are not strictly full-dominated, such as point $p _ { 9 } .$ .

We can use the marked extended full skyline to accurately obtain the extended reverse skyline in WSN. However, while calculating, only the strict semidominance

4. The global dominance [5] requires 8i 2 $D , ( p _ { 1 } [ i ] - q [ i ] ) \cdot ( p _ { 2 } [ i ] - q [ i ] ) >$ 0 and jp $[ i ] - q [ i ] | \leq | p _ { 2 } [ i ] - \bar { q } [ i ] | ,$ while strict-full-dominance requires 8i 2 $D , \ \bar { ( } p _ { 1 } \bar { [ i ] } - q [ i ] ) \cdot ( \bar { p } _ { 2 } [ i ] - q [ i ] ) ^ { * } > 0$ and $| p _ { 1 } [ i ] - q [ i ] | < | p _ { 2 } [ i ] - q [ i ] |$ j. Thus, the extended full skyline is a a super set of the global skyline.

relationship in space D is reserved. Moreover, the semidominance relation in the subspace is not completely reserved. Thus, we cannot obtain reverse skyline in each subspace accurately.

Clearly, 2-full-extended-skyband (denoted as $F X B ^ { 2 } ( Q ;$ $P , D )$ can solve this problem. We can find another point $p ^ { \prime } \in F X B ^ { 2 } ( Q , P , D )$ that fulfills $p ^ { \prime } { \overset { \bar { \jmath } } { = } } _ { Q } ^ { D ^ { \prime } } p$ for any point $p \in P ,$ , satisfying $\exists D ^ { \prime } \subseteq D , p \ \not \in \ R S ( Q , P , D ^ { \prime } )$ .

The purpose of transmitting points in $F X B ^ { 2 } ( Q , P , D ) -$ $F X ( Q , P , D )$ is to judge whether or not its strict-fulldominating point belongs to the reverse skylines in some subspaces. We can optimize its transmission processes separably. These points can be divided into three possible categories:

1. Those points whose strict-full-dominating point is strictly semidominated by some point in $F X B ^ { 2 } ( { \dot { Q } } , P , D )$ do not need to be transmitted, but its strict-full-dominating point however will be marked as such.   
2. Those points that cannot semidominate their strictfull-dominating point in any subspace do not need to be transmitted in WSNs, because they make no contributions to the calculation of reverse skyline.   
3. Since the remaining points may semidominate its strict-full-dominating point in some subspace, we need to transmit them back to the base station.

Through the above processing procedure, we can guarantee that the parent node can accurately compute the full skyline and reverse skyline in any subspace according to the obtained data, while keeping data transmission cost low.

# 5.1.2 Horizontal Optimization

According to Definition 7, when the two reverse skyline queries have the same subspace and their query ranges have the inclusion relationship, their results also have the inclusion relation, as shown in the theorem below.

Theorem 15. If $Q _ { 1 } \subseteq Q _ { 2 } ,$ , then we have $R S ( Q _ { 1 } , P , D ) \subseteq$ $R S ( Q _ { 2 } , P , D )$ .

Proof. According to Definition 7, we have $R S ( Q _ { 1 } , P , D ) =$ $\textstyle \bigcup _ { q \in Q _ { 1 } } R S ( q , P , D )$ and $\begin{array} { r } { R S ( Q _ { 2 } , P , D ) = \bigcup _ { q \in O _ { \circ } } R S ( q , P , D ) } \end{array}$ .

2 1 Since we have $Q _ { 1 } \subseteq Q _ { 2 }$ 2 2 , we can infer $\textstyle \bigcup _ { q \in Q _ { 1 } } R S ( q .$ $\textstyle P , D ) \subseteq \bigcup _ { q \in Q _ { 2 } } R S ( q , P , D )$ .

${ \mathrm { T h e r e f o r e } } , R S ( Q _ { 1 } , P , D ) \subseteq R S ( Q _ { 2 } , P , D ) .$

From Sections 3 and 4, we know that, by utilizing marked full skyline, reverse skyline can be calculated accurately in WSNs. However, the reverse skyline of a random subrange cannot be calculated accurately, since only semidominance relationships in the large range Q are taken into account while in the small range are not preserved.

Similar to the discussions in Section 5.1.1, 2-full-skyband can resolve the above problem. With regard to any point $p \in P$ satisfying $\exists Q ^ { \prime } \subseteq Q , p \not \in R S ( Q ^ { \prime } , P , D )$ , we can find another point $p ^ { \prime } \in F S B ^ { 2 } ( Q , P , D )$ that meets $p ^ { \prime } \bar { \preceq } _ { { Q ^ { \prime } } } ^ { \bar { D } } p .$

Equivalently, the points in $F S B ^ { 2 } ( Q , P , D ) - F \check { S } ( Q , P , D )$ are used to help determine whether its dominating points belong to reverse skyline in some subranges. Its transmission can be optimized according to the practical situation. There are three categories for these points.

1. If its full-dominating point can be semidominated by some point in $F S B ^ { 2 } ( \bar { Q } , P , D )$ , then it can be affiliated its full-dominating point with mark, therefore, these points need not to be transmitted.   
2. If points cannot semidominate its full-dominating point in any subrange,5 they do not need to be transmitted. This is because they have no contributions to the reverse skyline computation.   
3. The remaining points need to be transmitted, since they may semidominate its full-dominating point in some subranges.

As a result, the above procedure not only ensures that the parent node can accurately compute full skyline and reverse skyline in any subrange by utilizing the given data, but also reduces the volume of the transmitted data.

# 5.2 Optimization Mechanism

In the same dimensional space, the query result in a small query range can be included by that in large query range; similarly, in the same query range, the query result in a space can be included by that in its superspace. Taking these aspects into account, one straightforward method is to first combine all the queries into a new one employing the largest range covered and using the highest dimensional space, and then calculate actual query results from the retrieved answers from the WSN. However, this method is not efficient. Although the number of queries is reduced by combining the subspaces or the subranges, the cardinality of the new query result increases remarkably. Therefore, it is difficult to determine directly whether or not we really should combine the queries. Thus, during the optimization, we should compare the transmission cost before and after the combination, and then choose the plan with the smallest transmission cost.

It is an important step in optimization to estimate the transmission cost of a query. The communication cost of queries cannot be estimated directly, because this cost has consanguineous relationship with the particular routing structure of the WSN. Generally speaking, the communication cost exhibits a linear relationship with cardinality of the query results, so it can be weighed by the size of query result. According to our reverse skyline query, (extended) full skyline query (sometimes, 2-full-skyband) is frequently executed in the WSNs. As such, the cardinality of the (extended) full skyline result determines the communication cost.

As shown in Fig. 11, the (extended) full skyline consists of the subresults of regions I, II, and III. Depending on the subregion as depicted in Fig. 11, we can estimate the total transmission cost as following:

Region I: No mater Q is a full skyline query or an extended full skyline query, all points in this region belong to the results of Q. The cardinality of this region can be estimated by multiplying the capacity of this region with the data distributing density.

Region II: According to the definition of the full skyline query, the set of points in this region is distributed between

![](images/0324e00a92dc4dc5acb047f93042c2ba10ed9e456515038ed6ca20b1b09628a2.jpg)



Fig. 11. Cost estimation.

$Q [ i ] ^ { - }$ and $Q [ i ] ^ { + }$ in the space $D ^ { \prime } \neq \varnothing ,$ , and distributed out of $Q [ i ] ^ { - }$ and $Q [ i ] ^ { + }$ in the space $( D - D ^ { \prime } )$ containing other dimensions. $\textrm { I f a }$ point $p _ { 1 }$ full-dominates $p _ { 2 } ,$ then it must satisfy $\forall i \in D ^ { \prime } , p _ { 1 } [ \dot { i } ] = p _ { 2 } [ i ]$ . Denote the quantity of the data set $P$ as $N ,$ data duplicate ratio in dimension i as $\rho _ { i } ,$ and the number of points with the same value in the space $D ^ { \prime }$ as $\begin{array} { r } { N _ { e } = N \cdot \prod _ { i \in D ^ { \prime } } \rho _ { i } } \end{array}$ . Then, the number of distinct points in $P$ is $\begin{array} { r } { N _ { n e } = 1 / \prod _ { i \in D ^ { \prime } } \rho _ { i } } \end{array}$ . By utilizing sampling or existing estimation methods [18], [19], the skyline cardinality of each distinct point $p _ { i } , ~ S _ { i } ,$ can be estimated. Therefore, the total number of results in region II can be estimated as $N _ { n e } \cdot S _ { i }$ . Repeating the calculations above, all possible situations in region II can be enumerated, and the cardinality in this region can be obtained by accumulating the subresults. In practice, since $\rho _ { i }$ is small, $N _ { e }$ is small as well which makes $N _ { s } \doteq N _ { e }$ . So the cardinality of query result is close to the number of data points in this region.

According to the definition of the extended full skyline query, all the points in this region completely belong to the result, so the quantity of data points in this region is the cardinality of the final results.

Region III: The cardinality of the points in this region needs to be estimated by utilizing sampling or other existing estimation methods [18], [19].

During the optimization procedure, the data structures and corresponding algorithms for the maintenance of the original query and the synthetic query are similar to that of [12]. The only difference is in the procedure performed after a suitable super-space query is found. After some synthetic queries are found whose query spaces include the new query’s subspace, we do not add the new query into any synthetic query directly, but estimate the costs before and after the combination, choosing the most suitable synthetic query to add.

# 6 EXPERIMENTAL EVALUATION

In this section, we evaluate the query performance of our proposed approaches, based on tree-based structure using both real-world and synthetic sensor data sets.

For single reverse skyline query, the following three algorithms are evaluated.

Centralized: the naive approach described at the beginning of Section 3.   
Skyband: skyband based approach.   
Marked: marked full skyline based approach.

TABLE 2 Experimental Parameters 

<table><tr><td>Parameter</td><td>Default</td><td>Range</td></tr><tr><td>dimensionality</td><td>4</td><td>2, 3, 4</td></tr><tr><td>size of range</td><td>0.025</td><td>0.1,0.05,0.025,0.0125,0.00625</td></tr><tr><td>number of queries</td><td>30</td><td>10, 20, 30, 40, 50</td></tr></table>

For multiple reverse skyline queries, the following two algorithms are tested.

Naive: evaluating multiple queries one by one.   
Opt: algorithm with optimization mechanism.

# 6.1 Real Traces

The real-world sensor data set adopted is obtained from a forest environment monitoring project. In the project, we adopt the TelosB Mote [20] with a MSP430 processor and CC2420 transceiver, and each mote is equipped with two 2;200 mAh batteries. One-hundred twenty motes are deployed in a region of $2 0 { , } 0 0 0 \mathrm { m } ^ { 2 }$ . We used the data collected in September 2009, which include temperature (½10; 50-), humidity (½10%; 90%-), light (½0 KLux; 150 KLux-), and voltage (½0 V; 3 V-). There are around 30,000 sensory data items for each type, so we have enough data for running the algorithms multiple times with different data to verify their efficiency. We test our proposed solution on this real-world data set under various parameters. Table 2 summarizes the parameters under real-world data set investigation, along with their ranges and default values. In each experiment, we vary a single parameter, while setting the remainders to their default values.

# 6.1.1 Traditional Reverse Skyline

First, we investigate the performance of traditional reverse skyline query processing. In the experiments, we randomly generate 100 query points in the domain of the data set and report their average communication cost.

Fig. 12 shows that the communication cost of all the testing approaches is proportional to the increase of dimensionality. The reason is that an increase of dimensionality leads to the increase of the size of the individual tuples, and thus will increase the total communication costs. Though the total number of tuples transmitted in Centralized approach is fixed, the number of messages increases accordingly due to the increase of communication cost per tuple. The increase of dimensionality also incurs a larger amount of full skyband/skyline results. Among the testing approaches, the Centralized approach has the highest transmission costs, whereas the Marked has the lowest cost. This indicates that our algorithm is efficient in reducing the communication cost.

![](images/fd2b6adbec00522b996a223ea2517e780b8d118506f11a4dbaed096a558f902e.jpg)



Fig. 12. Traditional reverse skyline versus dimensionality.

![](images/79f1958cc25aef605e861537904f7b56cec13877a120b0fbfb5de612deb0d4bc.jpg)



Fig. 13. Range reverse skyline versus dimensionality.

# 6.1.2 Range Reverse Skyline

Next, we consider the influence of different parameters to the range reverse skyline query processing. We use the same set of query points generated for the traditional reverse skyline experiments. The query range on each attribute is calculated by multiplying its domain size with the size of the range.

As shown in Fig. 13, with the change of dimensionality, the communication cost trends of the three algorithms are similar, with only some slight difference in the communication cost. Since range reverse skyline is the generalization of traditional reverse skyline, their properties and regularity are similar. Range reverse skyline is the union of a set of traditional reverse skylines that have more overlaps, and thus the transmission cost increases as the dimensionality increases.

Fig. 14 illustrates the influence of query range. The communication cost of Centralized approach is stable, while that of Skyband and Marked decreases with decreasing the size of query range. When the query range varies, the amount of sensing points remains the same. Therefore, the communication cost of Centralized approach does not change. Meanwhile, the shrinking of query range leads to the decrease of the number of range full skyband/skyline points, so the communication costs drop. The cost of Centralized is always the highest, and that of Marked is always lower than that of Skyband, which further proves the utility of our proposed techniques.

# 6.1.3 Multiple Reverse Skylines

Next, we conduct a comprehensive performance evaluation of the multiple reverse skylines optimization. In these experiments, we mainly consider two kinds of query point distributions (uniform and clustered) and two kinds of query dimensional space distributions (uniform and Zipf). In total, there are four combinations in terms of the query point distributions and the query dimensional space distributions. Due to the similar performance, we only report the results of the two query point distributions, in the Zipf query dimensional space. The query range on each attribute is calculated by multiplying its domain size by a randomly generated decimal between zero and the size of the range.

![](images/d308aa2c2176ae0ae312f1740bcbfd4b35253badcbb6bb217a129077e3c42916.jpg)



Fig. 14. Range reverse skyline versus query range size.

Fig. 15 shows that the communication cost of each algorithm in multiple queries is increasing with the increase of dimensionality. Simultaneously, the communication cost of Opt is always lower than that of Naive, which illustrates that optimization mechanism is effective in avoiding the transmission of unnecessary data.

Fig. 16 shows the performance of the algorithms by changing the numbers of queries. While the number of queries increases, the communication cost of Naive also increases. This is because more queries lead to the increase of the number of query results, which in turn increases the communication cost. The communication cost of Opt is increasing slowly with the growth of the queries. Compared to Naive, Opt is more stable, which indicates that the influence of the query number on the query performance is small by using our optimization mechanism.

![](images/fe56b916e691bb88f81aef868115590d23f8ecf46bfc0e113f1ded0f89e67320.jpg)



(a)

![](images/ecfdf66082641415a023bbbe67a5be0d57b4875dd1715ec16c28a8f471c8d164.jpg)



(b)   
Fig. 15. Multiple reverse skyline versus dimensionality. (a) Uniform. (b) Clustered.

![](images/49bb43634191a3bbed9667e0f941a90336345da968b0dae65c57d0a603189044.jpg)



(a)   
![](images/9021534f1ae5f2f0577b03383116ef1e081538bc0a893ee3fa0c74049bf05c65.jpg)



(b)   
Fig. 16. Multiple reverse skyline versus the number of queries. (a) Uniform. (b) Clustered.

Fig. 17 shows the communication cost when the maximal query range varies. Because of the reduction of the maximal range, the average range of each query is reduced, which implies that the probability that a point is range dominated is increasing. As such the number of the results is reduced. Either the cost of Naive or that of Opt is declining with the reduction of the query range. The performance of Opt is better than that of Naive, which further confirms that the optimization mechanism is effective.

# 6.2 Synthetic Traces

Due to the limited number of sensor nodes and dimensionality in the real-world sensor data, for testing the scalability of our proposed approaches, we have conducted comprehensive performance experiments using a synthetic data set. We perform our synthetic analysis with a simulator developed in C++. The simulator allows us to adjust network parameters, such as the number of nodes and the communication radius. For the sake of experimental unification, we randomly place n sensors in an area of ${ \sqrt { n } } \times { \sqrt { n } }$ units. Under these conditions, each node contains one unit space on average. The communication radii of sensor nodes are set to $2 \sqrt { n }$ units. Meanwhile, we enforce that the maximal length of packets transmitted in the network is limited to 48 bytes. All the experiments are run on a PC with 1:86 GHz Intel Core 2 CPU, 1 GB memory, and 80 GB hard disk.

The synthetic data are generated by standard data set generator for reverse skyline queries [5], including the uniform distributed data points and the clustered distributed data points. The uniform data set consists of the points randomly generated on a unit square. However, the clustered data set comprises 10 randomly centered clusters, each of these contains equal number of points and follows a Multivariate Gaussian Distribution whose covariance matrix is a 0.05-diagonal matrix and mean vector is equal to the associated centroid. Due to the similar performance, the results of uniform data are omitted. Table 3 summarizes the parameters under synthetic investigation.

![](images/2d1b25fdafb9dae129c2ea2daa0b57c5539c16023cd91b5e549809a3b43c67d0.jpg)



(a)   
![](images/161d470c75bb8c63c4420d993d7077cd55c2904e9abeea4c1352af9d5b1dbeee.jpg)



(b)   
Fig. 17. Multiple reverse skyline versus query range size. (a) Uniform. (b) Clustered.

As shown in Figs. 18a, 19a, and 20a, the communication cost with respect to the dimensionality, in each algorithm for the synthetic data set is similar to that on the real-world data set. Figs. 18b, 19b, and 20b show that the communication cost of all approaches increase along with the increase of the number of nodes. This is because the increase of the number of nodes means an increase in the number of the sensed data points. The increase of the number of points usually incurs a larger amount of full skyband/skyline results. The performance relation of the proposed algorithms is similar to that in previous experiments, which can validate the effectiveness of our proposed approaches.

Fig. 21 shows the cardinality of the query results of Full Skyband (FSB), Full Skyline (FS), and Reverse Skyline with varying the dimensionality. Among the three query algorithms, the cardinality of the FSB result set is the highest, while the cardinality of the RS result set is the lowest. The inclusion relationships among the three queries can well explain this phenomenon. Since a RS query is not decomposable, even though the cardinality of RS is much lower than those of both FSB and FS, we still need to transmit the marked full skyline, whose cardinality is a little higher than that of FS but lower than that of FSB to ensure that the RS results can be calculated accurately at the base station.

TABLE 3 Simulation Parameters 

<table><tr><td>Parameter</td><td>Default</td><td>Range</td></tr><tr><td>dimensionality</td><td>5</td><td>3, 4, 5, 6, 7</td></tr><tr><td>number of nodes</td><td>8000</td><td>6000, 7000, 8000, 9000, 10000</td></tr></table>

![](images/3974ccd4cc4f712e280907f77a47eb0a412aef42c57663e50421a83035328923.jpg)



(a)   
![](images/70588ae24304078a96fbe4e5476ff27cb877efa02cb4e802355e1f8e0e57215a.jpg)



(b)   
Fig. 18. Scalability of reverse skyline. (a) Dimensionality. (b) Number of sensor nodes.

# 6.3 Performance on Local Sensor Node

We implemented the branch and bound RS algorithm (BBRS) in [5] and the semidominance based RS algorithm (SDRS) using C++. As shown in Fig. 22, SDRS is much faster

![](images/ee94e78aad6e92e4b5313c15d228befbd91a36a0006474aa834e6fea84109a2f.jpg)



(a)

![](images/825c4c84ea38948732629e4ac6d8ddcc8114751c23b53dfcecee970af797bddd.jpg)



(b)   
Fig. 19. Scalability of range reverse skyline. (a) Dimensionality. (b) Number of sensor nodes.

![](images/534923aa753f31b1bee8783eaf7397ea1aef00fb2e0da9e41c9d12d67c1bad45.jpg)



(a)

![](images/9e3cd4d063445bc946de4f4dd5e7c19ee8dec698430e269048a6517e4ec25457.jpg)



(b)   
Fig. 20. Scalability of multiple reverse skylines. (a) Dimensionality. (b) Number of sensor nodes.

than BBRS, because it only needs to traverse the R-tree index one round, while BBRS needs to traverse the R-tree index multiple rounds (one round for a boolean window query).

# 6.4 Summary

From the experiments on both real-world and synthetic data sets, we can conclude that for traditional reverse skyline, range reverse skyline and multiple reverse skylines, our proposed approaches can achieve robust query performance with respect to various parameters, and they are energy efficient to be carried out in WSNs.

# 7 CONCLUSIONS AND FUTURE WORK

Energy is one of precious resources in WSNs, and it is mainly consumed by the wireless communication. Therefore, it has become an essential problem for sensing applications to minimize the communication cost. In this paper, we perform a comprehensive study on reverse skyline query processing in WSNs. First, we theoretically analyze the properties of reverse skyline, and introduce an energy-efficient approach based on full skyband to suppress any unnecessary data transmission. Next, the proposed approach is extended to support range reverse skyline queries. Then, optimization mechanisms for multiple reverse skyline queries are developed to save both the query propagation cost and the redundant results transmission cost. Finally, we have conducted extensive experimental studies to evaluate the performance of the proposed approaches on both real-world data and synthetic data. The experimental results show that our proposed approaches can effectively reduce communication cost and reduce the energy consumption of RS queries in WSNs.

![](images/c8750638998538e5ff4ba4b616d21741f47b32cb8239825265732333cf272987.jpg)



Fig. 21. Cardinalities of different queries.

![](images/8aa6566fb490528553387d9f562a161fcd5e56e377047c91ec505975b1d396c3.jpg)



(a)   
![](images/75ddc3d8a1c4ad40a68bc49fe14993fbfcc34427ef94d971db70312063a1d3ff.jpg)



(b)   
Fig. 22. Performance on local sensor node. (a) Dimensionality. (b) Cardinality.

Since data uncertainty is an inherent characteristic of WSNs [21], it is an interesting direction for our future research work to conduct queries and extract useful information from massive uncertain sensor readings.

# ACKNOWLEDGMENTS

This research is supported by the National Natural Science Foundation of China (Grant No. 60873011, 60933001, and 61025007), the National Natural Science Foundation for Young Scientists of China (Grant No. 61100022), National Basic Research Program of China (973, Grant No. 2011CB302200-G), the 863 High Technology Program (Grant No. 2009AA01Z150), and the Fundamental Research Funds for the Central Universities (Grant No. N090104001 and N090304007).

# REFERENCES

[1] S. Borzsonyi, K. Stocker, and D. Kossmann, “The Skyline Operator,” Proc. 17th Int’l Conf. Data Eng., pp. 421-430, 2001.

[2] E. Dellis, A. Vlachou, I. Vladimirskiy, B. Seeger, and Y. Theodoridis, “Constrained Subspace Skyline Computation,” Proc. 15th ACM Int’l Conf. Information and Knowledge Management (CIKM ’06), pp. 415-424, 2006.   
[3] D. Papadias, Y. Tao, G. Fu, and B. Seeger, “An Optimal and Progressive Algorithm for Skyline Queries,” Proc. ACM SIGMOD Int’l Conf. Management of Data (SIGMOD ’03), pp. 467-472, 2003.   
[4] K. Deng, X. Zhou, and H.T. Shen, “Multi-Source Skyline Query Processing in Road Networks,” Proc. IEEE 23rd Int’l Conf. Data Eng. (ICDE ’07), pp. 796-805, 2007.   
[5] E. Dellis and B. Seeger, “Efficient Computation of Reverse Skyline Queries,” Proc. 33rd Int’l Conf. Very Large Data Bases (VLDB ’07), pp. 291-302, 2007.   
[6] X. Lian and L. Chen, “Monochromatic and Bichromatic Reverse Skyline Search over Uncertain Databases,” Proc. ACM SIGMOD Int’l Conf. Management of Data (SIGMOD ’08), pp. 213-226, 2008.   
[7] X. Wu, Y. Tao, R.C.-W. Wong, L. Ding, and J.X. Yu, “Finding the Influence Set through Skylines,” Proc. 12th Int’l Conf. Extending Database Technology: Advances in Database Technology (EDBT ’09), pp. 1030-1041, 2009.   
[8] S. Madden, M.J. Franklin, J.M. Hellerstein, and W. Hong, “TAG: A Tiny Aggregation Service for Ad-Hoc Sensor Networks,” Proc. Fifth Symp. Operating Systems Design and Implementation (OSDI ’02), pp. 131-146, 2002.   
[9] A. Silberstein, R. Braynard, C.S. Ellis, K. Munagala, and J. Yang, “A Sampling-Based Approach to Optimizing Top-k Queries in Sensor Networks,” Proc. 22nd Int’l Conf. Data Eng. (ICDE ’06), p. 68, 2006.   
[10] M. Wu, J. Xu, X. Tang, and W.-C. Lee, “Top-k Monitoring in Wireless Sensor Networks,” IEEE Trans. Knowledge and Data Eng., vol. 19, no. 7, pp. 962-976, July 2007.   
[11] H. Chen, S. Zhou, and J. Guan, “Towards Energy-efficient Skyline Monitoring in Wireless Sensor Networks,” Proc. 4th European Conf. Wireless Sensor Networks (EWSN ’07), pp. 101-116, 2007.   
[12] J. Xin, G. Wang, L. Chen, and V. Oria, “Energy-Efficient Evaluation of Multiple Skyline Queries over a Wireless Sensor Network,” Proc. 14th Int’l Conf. Database Systems for Advanced Applications (DASFAA ’09), pp. 247-262, 2009.   
[13] J. Xin, G. Wang, L. Chen, X. Zhang, and Z. Wang, “Continuously Maintaining Sliding Window Skylines in a Sensor Network,” Proc. 12th Int’l Conf. Database Systems for Advanced Applications (DASFAA ’07), pp. 509-521, 2007.   
[14] W. Liang, B. Chen, and J.X. Yu, “Energy-Efficient Skyline Query Processing and Maintenance in Sensor Networks,” Proc. 17th ACM Conf. Information and Knowledge Management (CIKM ’08) pp. 1471- 1472, 2008.   
[15] J. Considine, F. Li, G. Kollios, and J. Byers, “Approximate Aggregation Techniques for Sensor Databases,” Proc. 20th Int’l Conf. Data Eng. (ICDE), pp. 449-460, 2004.   
[16] H. Hu and D.L. Lee, “Range Nearest-Neighbor Query,” IEEE Trans. Knowledge and Data Eng., vol. 18, no. 1, pp. 78-91, Jan. 2006.   
[17] A. Vlachou, C. Doulkeridis, Y. Kotidis, and M. Vazirgiannis, “SKYPEER: Efficient Subspace Skyline Computation over Distributed Data,” Proc. IEEE 23rd Int’l Conf. Data Eng. (ICDE), pp. 416-425, 2007.   
[18] S. Chaudhuri, N.N. Dalvi, and R. Kaushik, “Robust Cardinality and Cost Estimation for Skyline Operator,” Proc. 22nd Int’l Conf. Data Eng. (ICDE ’06), p. 64, 2006.   
[19] Z. Zhang, Y. Yang, R. Cai, D. Papadias, and A.K.H. Tung, “Kernel-Based Skyline Cardinality Estimation,” Proc. 35th SIGMOD Int’l Conf. Management of Data (SIGMOD), pp. 509-522, 2009.   
[20] J. Polastre, R. Szewczyk, and D.E. Culler, “Telos: Enabling Ultra-Low Power Wireless Research,” Proc. Fourth Int’l Symp. Information Processing in Sensor Networks (IPSN ’05), pp. 364-369, 2005.   
[21] R. Cheng and S. Prabhakar, “Managing Uncertainty in Sensor Databases,” SIGMOD Record, vol. 32, no. 4, pp. 41-461, 2003.

![](images/f6b1d4d0d47af9488b78e569d9826c212c77bb9e91bd09445f0532df266fe19f.jpg)



Guoren Wang received the BSc, MSc, and PhD degrees from the Department of Computer Science, Northeastern University, China, in 1988, 1991, and 1996, respectively. Currently, he is a professor in the Department of Computer Science, Northeastern University, China. His research interests include XML data management, query processing and optimization, bioinformatics, high-dimensional indexing, parallel database systems, and P2P data management.

He has published more than 100 research papers.

![](images/b73ee431f764b9d33a2985a35bbe29afb259bdf15fa69960f08ccdff17bfb891.jpg)



Lei Chen received the bachelor’s degree in computer science at Tianjin University, China, in 1994, and the master’s degree in computer science at the Asian Institute of Technology in 1997. He received the PhD degree in computer science at University of Waterloo, Canada. He is currently an assistant professor of computing science at Hong Kong University of Science and Technology, China. His research interests include multimedia databases, graph databases,

uncertain and probabilistic databases.

![](images/efa980e7735d50b0f545f565ddbf843678e462465ff6f7f05f2cf054b400f289.jpg)



Junchang Xin received the BSc, MSc, and PhD degrees in computer science and technology from the Northeastern University, China, in July 2002, March 2005, and July 2008, respectively. He is currently a lecturer in the Department of Computer Science, Northeastern University, China. His research interests include data management over wireless sensor network and uncertain data management.

![](images/ab14adb05413a67a35c101ac913b709da92a9429f6b389c2dc85548c20c959cb.jpg)



Yunhao Liu received the BS degree in automation from Tsinghua University, China, in 1995, the MS, and a PhD degrees in computer science and engineering from Michigan State University in 2003 and 2004, respectively. He is a member of Tsinghua National Lab for Information Science and Technology, professor in the School of Software at Tsinghua University, and the director of the Tsinghua National MOE Key Lab for Information Security. He is also a faculty

in the Department of Computer Science and Engineering at the Hong Kong University of Science and Technology. He is a senior member of the IEEE, and is also an ACM Distinguished Speaker.

. For more information on this or any other computing topic, please visit our Digital Library at www.computer.org/publications/dlib.