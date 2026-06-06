# Contour-cast: Location-free Data Dissemination and Discovery for Wireless Sensor Networks

Zhigang Li†‡ , Nong Xiao†, Yunhao Liu‡ , Xue Liu§

†School of Computer, National University of Defense Technology, China

‡ Dept. of Computer Science and Engineering, Hong Kong University of Science and Technology

§School of Computer Science, McGill University, Canada

{lzg,nongxiao}@nudt.edu.cn,liu@cse.ust.hk, xueliu@cs.mcgill.ca

Abstract—Data dissemination and discovery is critical for adhoc wireless sensor networks. Most existing research depends on location information that is not always obtained easily, efficiently and accurately. We propose the concept of Contour-cast, a location-free data dissemination and discovery approach for large-scale wireless sensor networks. One important property of Contour-cast is that it does not depend on physical position or accurate localization services. The other advantage is that each node needs not maintain too much topology information. We evaluate Contour-cast thoroughly using metrics including data retrieval success ratio, storage cost, and load balance. Evaluation results show that Contour-cast can reach comparable functionalities and performance as the other approaches with physical location information.

Keywords-contour-cast, location-free, data discovery, WSN

# I. INTRODUCTION

Large-scale sensor networks are employed in many applications such as scientific data collection, environment monitoring, or military surveillance [1, 2]. A sensor network is composed of many power-constrained and resourcelimited sensors. In traditional applications, it is assumed that a stationary sink node is responsible for data collection and the other nodes send their collected data to the sink node periodically [1, 2, 3]. In many applications, however, it is not necessary to maintain a stationary sink. For example, in a battlefield or a wild zoo, we can scatter a lot of stationary sensors to monitor the environment without deploying a stable sink, instead, a soldier or a zoologist takes a mobile sink into the area of the network at any position of the environment [4, 10]. We call the stationary sensors around mobile sink nodes as consumer proxy nodes. They relay the queries from mobile sink nodes to other stationary nodes and also collect the data from data producer nodes to mobile sink node. In such applications, every stationary node may become a consumer proxy node or data producer node. A consumer proxy node and a data producer node do not know each other in advance, and cannot obtain each other’s information instantly. Therefore, a connection link is needed between a consumer and a producer. How to enable a consumer and a producer to effectively and efficiently discover each other is a challenge issue in a large-scale sensor network.

Much work on data dissemination and discovery in sensor networks have been proposed in recent years, such as TTDD [5], GHT [6] and Double Rulings [7]. The approaches perform well if each node is aware of its location. We classify the existing work into two categories. If a data dissemination and discovery approach needs location information, we call it location-based approach, such as the TTDD, GHT and Double Rulings [5, 6, 7]. Otherwise, if an approach does not depend on location information, we call it location-free approach. The naive flooding approach and Rumor routing [11] can be considered as location-free data dissemination and discovery approaches. In location-based approach, a producer can disseminate its data or meta-data to one node R in a predefined place, such as by GHT, while a consumer can discover the producer’s data by visiting node R. In locationfree approach, every node is blind to its own location and the location of other nodes. If a producer generates data, it does not know which node needs its data or where to disseminate its data without global topology information. In order to maintain global information, however, it needs much energy, computation and storage resources [13]. The motivation of our work is to design a light weight approach to allow sensors to discovery each other without location and much topology information.

In this paper, we propose Contour-cast, a location-free data dissemination and discovery scheme. It only uses two beacons to build two overlapping overlays for the network. It mainly includes two parts, contour overlays establishment and contour-cast routing. A contour is composed of all the nodes with the same hop distance to one beacon. For an single node, it belongs to two contours that belong to different contour overlays. A consumer or a producer can disseminate its queries or data along contours. The contourcast routing algorithm can guarantee a consumer and a producer discover each other with high probability.

Contour-cast achieves the comparable functionalities and performance with Double Rulings in the absence of location information . All the contours in the network are in virtual form that every node only needs to keep a hop number pair rather than much information. They only depend on hop information to the double beacons but not on range or distance information. The Contour-cast routing can also achieve load balance and avoid energy holes such as in a sink-based wireless sensor network [12].

The rest of this paper is organized as follows. Section II shows the overview of Contour-cast and how to build contour overlays by two selected beacons. Then, in Section III and IV, we present the ideal Contour-cast scenario and the random Contour-cast scenario, respectively. In Section V, we present evaluation about the performance of Contourcast. Finally, we conclude the paper by summarizing this work in Section VI.

# II. OVERVIEW OF CONTOUR-CAST

In a resource-constrained large-scale sensor network [8, 9], it is difficult and expensive for a single node to obtain the global network information [13]. For each node, it can only communicate with its neighbors directly. If a node is not aware of its location information, it is more difficult for a node to discover its desired data without flooding queries. In our work, we use double beacons to abstract the topology and connection of the whole network. We call one beacon as Blue Beacon and the other as Red Beacon for simplicity. Both beacons flood hop counter messages to other nodes in the network. Every other node computes the shortest hops to Blue Beacon and Red Beacon respectively. This section mainly presents the establishment and initialization of the contour overlays. We omit the beacons selection procedure in this section. We assume that two beacons have been selected in a large-scale network. The detail of beacons selection process will be discussed in the following sections.

We assign a hop counter number pair $( b , r )$ to each node, where b stands for the hop counter to Blue Beacon named as bluehop number or bluehop and r stands for the hop counter to Red Beacon named as redhop number or redhop. At the beginning, it is $( b _ { m a x } , r _ { m a x } )$ , for example we set $b _ { m a x }$ and $r _ { m a x }$ as 127 in our simulation. Both of them broadcast hop counter messages to its neighbors. A hop contour message only has two tuples. One is a color flag with one bit, such as 1 stands for blue message and 0 stands for red message. The other is a hop counter.

When a node receives a message M, it first checks the color flag of M. Then the node compares its current hop number (with the same color) with the hop counter of M. If its hop number is 2 bigger than M.hop, it modify its hop number to M.hop+1. It is possible that the node may receive several same color messages in a short time span. In this case, it selects the message with the smallest hop counter. If the node has modified one of its hop numbers, it broadcasts a hop counter message with its current hop number to its neighbors. After several iterations, all the nodes obtain the shortest hop number to the corresponding beacon except the isolated nodes.

After the process, every node has a stable and shortest hop number pair $( b , r )$ . We use Red Beacon as an example. All the nodes with the same redhop k will form a contour denoted as $C R _ { k }$ (if Blue Beacon, it is $C B _ { k } )$ . All contours built by Red/Blue Beacon are called as Red/Blue contour overlay. In a dense network, we assume that all sensors in the same contour $C R _ { k }$ (or $C B _ { k } )$ can be connected. The k is also called the radius of $C R _ { k } .$ . For a single node with red hop $k ,$ if it is not the Red Beacon node or the node with maximal red hop, we can classify its neighbors into three types. One type neighbors are k-hop neighbors, which are along the same contour $C R _ { k }$ . One type of neighbors are (k-1)-hop neighbors and the others are (k+1)-hop neighbors. In other words, after the contour overlay establishment the node with hop numbers (b, r) belongs to two contours. One is $C B _ { b }$ for Blue Beacon and one is $C R _ { r }$ for Red Beacon. In reality, no node needs to store the contour information. For simplicity, we can consider the hop numbers (b, r) as one kind of coordinate, while it is more accurate than the Cartesian coordinate obtained by location algorithms. In our protocol, every node uses these two numbers to direct the data dissemination and discovery process. Because all the nodes belong to one contour can be connected, we define a new data forwarding protocol using contours.

Definition 1 ( Contour-cast Routing). : A node with hop number pair (b , r) sends its messages to all the nodes which belong to the same contour $C B _ { b }$ or $C R _ { r }$ .

The Contour-cast Routing can be used to disseminate data replicas and queries in our work. The next section presents the details of the application of Contour-cast in the process of data dissemination and discovery. For simplicity, we also call the data dissemination and discovery process along contours as Contour-cast, such as broadcast or multicast.

# III. IDEAL CONTOUR-CAST SCENARIO

In this section, the sensor network is assumed in a square area with a large number of sensor nodes uniformly scattered in this area. The method in reference [14] can be applied to select the two beacons. In certain cases, we can also fix two nodes as beacons directly. We assume the Blue Beacon locates at the left-top corner of the square area and the Red Beacon locates at the left-bottom corner (Figure 1).

# A. Data Replication Process

When a node with hop number pair (b, r) detects some data, it triggers data replication dissemination process. It makes decision by adopting one of four strategies. The four strategies are: (a) RiB (Red / Min Blue) , (b) RaB (Red / Max Blue), (c) BiR (Blue / Min Red), and (d) BaR (Blue / Max Red).The Figure1 illustrates these four strategies.

![](images/815500a8c39245a6e8ce8a9e934b93ef83dd71d779e2141051d5998ad0ecb042.jpg)



(a) RiB

![](images/81217a0a745886c1f23d98e217bb55d18d56c77f4c5958fcbd4023787b3f484c.jpg)



(b) RaB

![](images/d3e45d7815feaf07f053db4a05349c21ae19d11b05c5fff51b65700daec6faa9.jpg)



(c) BiR

![](images/82ffe2f8a96b08b16d800b1af1046c3419c613ae02d3a666e6342551773b678a.jpg)



(d) BaR   
Figure 1. The four strategies for data replication process (Red/Min Blue, Red/Max Blue, Blue/Min Red and Blue/Max Red). They can also be used for the basic data query process.

The probability that each strategy adopted by any node is 25%. We use RiB strategy as example to explain the four strategies. The node with hop numbers (b, r) first Contourcast along $C R _ { r }$ . During this process, every node along $C R _ { r }$ compares its bluehop with its neighbors. If one node M with hop numbers (m, r) finds that its bluehop m is lower than the bluehop of any of its neighbors, it will startup another Contour-cast along $C B _ { m }$ for dissemination the data replicas. The blue contour and red contour here are concatenated together by node M to be one path called joint Contourcast path or Contour-cast path.

The reason we make four strategies for Contour-cast is for load balance. It is obvious that in theory if the blue contour and red contour (as Figure 2) intersect on the left boundary of the square, the length of the Contour-cast path is about

$$
0. 5 (\pi r _ {1}) + 0. 5 (\pi r _ {2}) \doteq 0. 5 \pi l
$$

where $r _ { 1 }$ is the redhop of N and $r _ { 2 }$ is the bluehop of E. l is the hop between Blue Beacon and Red Beacon.

In theory, the lengths of the Contour-cast paths generated by four strategies are different. We use RiB and RaB as examples as Figure 2 illustrated. In strategy RiB, node N Contour-cast along $C R _ { r _ { 1 } }$ and $C B _ { r _ { 2 } }$ . In strategy RaB, node N Contour-cast along $C R _ { r _ { 1 } }$ and $C B _ { m } .$ . We can move $C B _ { r _ { 2 } }$ from point E and F to point E- and $F ^ { \prime }$ , then we get $C ^ { \prime } B _ { r _ { 2 } }$ Obviously, $C B _ { m }$ is shorter than $C ^ { \prime } B _ { r _ { 2 } }$ . In practice, however, the difference between $C B _ { m }$ and $C ^ { \prime } B _ { r _ { 2 } }$ is insignificant. As Figure 2 illustrated, it is obvious that

$$
\frac {L \left(C B _ {m}\right)}{L \left(C ^ {\prime} B _ {r _ {2}}\right)} > \frac {\left| E ^ {\prime} F ^ {\prime} \right|}{L \left(C ^ {\prime} B _ {r _ {2}}\right)} = \frac {\sqrt {2} r _ {2}}{\frac {1}{2} \pi r _ {2}} > 90 \% \tag{1}
$$

In a real network, $C B _ { m }$ and $C ^ { \prime } B _ { r _ { 2 } }$ are very close. Especially in a grid-link network, $C B _ { m }$ and $C ^ { \prime } B _ { r _ { 2 } }$ are overlapped and all the contours fix line curves rather that arc curves. $C B _ { m }$ and $C ^ { \prime } B _ { r _ { 2 } }$ have one important same property that they have the same ends and intersect with the same red contours. We use this property to prove the data retrieval success guarantee in next section. The $C B _ { m }$ is called as the shadow contour of $C B _ { r _ { 2 } }$ and vice versa.

![](images/b1037019e8c43df2a0e8c183986a4feaea8d9b1af1672d7f087cfa7e7bba3ec8.jpg)



![](images/29d6f62985ceac559860e53f126f143b0494e9de23d17c851e61ce5f1112a662.jpg)



Figure 2. A blue Contour and Figure 3. Double-Contour-cast data its shadow contours. The difference retrieval process. Node Q can disbetween one contour and its shadow seminate its query message along contour is insignificant. both blue Contour and Red Contour.

# B. Data Retrieval Process

When a node needs to discover desired data, it needs to launch its query process. The query process can also use the four strategies as the data replication process. But it can use more flexible strategies.

1) Basic query process: When the data producer P has disseminated its data replicas using any one of the above four strategies, one node Q as a consumer proxy node needs to query this data. The storage Contour-cast path of P contains one red contour $C R _ { r }$ and one blue contour $C B _ { b }$ . The basic query process uses the same strategies as data replication process. Then we prove that the query Contour-cast path intersects with the data Contour-cast path. It means that the query Contour-cast path and data Contour-cast at least share one node. If we consider the Contour-cast path as continuous curve, it is obvious to prove that any two such curves intersect each other at one point. In reality, however, one Contour-cast path is not a continuous curve. But theorem 1 guarantees the existence of intersection node of any Contourcast paths.

Theorem 1. Any two joint Contour-cast paths intersect at least at one node in ideal Contour-cast scenario.

Proof: In the proof, we only use RiB strategy. It is easy to prove that if the theorem is right for the RiB strategy, it is also right for other three strategies. Because the RiB and BiR are symmetric, the $R a B$ and $B a R$ can be transformed to RiB and BiR by moving the blue contour and red contour to their shadow contours. Given any two Contourcast paths $C _ { p }$ and $C _ { q } ,$ the $C _ { p }$ contains one blue contour $C B _ { b _ { 1 } }$ and one red contour $C R _ { r _ { 1 } }$ . The $C _ { q }$ contains one blue contour $C B _ { b } .$ and one red contour $C R _ { r _ { 2 } }$ . If $b _ { 1 } ~ < ~ b _ { 2 } .$ , it is obvious that $r _ { 1 } > r _ { 2 }$ . Then this problem is transformed to prove whether there exists at least one node with hop number pair $( b _ { 2 } \ , r _ { 1 } )$ . It is obvious that all the nodes along contour $C R _ { r _ { 1 } }$ have bluehop number equal or greater than $b _ { 1 }$ . Because all the nodes along contour $C R _ { r _ { 1 } }$ are connected, according to the procedure of Algorithm 1, the bluehop numbers of them are in sequence $( b _ { 1 } , \ b _ { 1 + 1 } , \ b _ { m } ) .$ , where $b _ { m }$ is the greatest bluehop number in $C R _ { r _ { 1 } }$ . If $b _ { m } > b _ { 2 }$ the theorem is right. $C B _ { b _ { m } }$ is the shadow contour of $C B _ { b _ { 1 } }$ by using RaB strategy. $C B _ { b _ { 2 } }$ is between $C B _ { b _ { m } }$ and $C B _ { b + 1 }$ . So $b _ { m } > b _ { 2 }$ , the theorem is right.

The proof of Theorem 1 also shows that if a node needs to discover desired data, it just only checks its neighbors belong to the same contour. It does not need to check all of its neighbors. This can avoid local information flooding.

2) Double-Contour-cast retrieval: The basic query process adopts strategies as data replication process. But we can use another strategy for data retrieval called double-Contourcast retrieval. In double-Contour-cast retrieval, node Q with hop numbers (b, r) Contour-cast its query along both contour $C R _ { r }$ and $C B _ { b }$ . We can prove that at least one contour (either $C R _ { r }$ and $C B _ { b }$ or both) can discover the desired data by Theorem 1.

Proof: In this proof, we also use RiB for data replication process. Given any data Contour-cast path $C _ { p } . ~ C _ { p }$ contains one blue contour $C B _ { b _ { 1 } }$ and one red contour $C R _ { r _ { 1 } }$ . The $C _ { p }$ partition the square area into three sets. Any node in the first set with hop numbers pair $( b , r )$ that $b < b _ { 1 }$ .and $r > r _ { 1 }$ . Any node in the second set with hop numbers pair $( b , \ r )$ that $b > b _ { 1 }$ .and $r \ < \ r _ { 1 }$ . Any node in the first part with hop numbers pair $( b , r )$ that $b > b _ { 1 }$ .and $r > r _ { 1 }$ . If the query node does not locate at the $C _ { p } ,$ it locates at one of the above mentioned set. If it locates at first set, $C R _ { r }$ intersects $C B _ { b _ { 1 } }$ at one node with hop number pair $( b _ { 1 } , r )$ . If it locates at second set, $C B _ { b }$ intersects $C R _ { r _ { 1 } }$ at one node with hop number pair $( b , r _ { 1 } )$ . If it locates at third set, both CRr and $C B _ { b }$ intersect $C _ { p }$ at one node with hop number pair (b1 , r) and one node with hop number pair $( b , r _ { 1 } )$ .

# IV. RANDOM CONTOUR-CAST SCENARIO

In random scenario we randomly select two nodes in inner network area rather than two ideal nodes as in ideal scenario. The protocol for random scenario is similar with the protocol in ideal scenario with a few modifications. In this section we need not assume the shape of network area. For simplicity, we use square area as example.

![](images/a33564267eb7e9d916858fafe417ab98e35aa5381406e13e2a9f27774b065de0.jpg)



(a) Single Contour-cast path

![](images/ad77e9599e5b1f0717844f3800517c7cb9c1abeca92d3609bfd254bb2a07767a.jpg)



(b) Two Contour-cast paths

Figure 4. Contour-cast routing process in Random Contour-cast scenario.   
![](images/805a2c8be8a2ab3cf9f323af7bdf5f498663281e7207cf03502e0a54f103dce2.jpg)



(a)

![](images/9a88f57ecf8db4c11c349a15190250205129d74ba5ee5ab030874f913281b5ca.jpg)



(b)   
Figure 5. (a)In an enough large area network, any pair of tangent blue contour and red contour intersects with each other in the spindly area. (b) if the network area (the rectangular area in b) can not be covered fully by spindly area, the data retrieval success can not be guaranteed.

# A. Beacons selection in random scenario

1) Red Beacon selection: First, one node is randomly selected as red beacon. In practice, maybe several nodes will decide themselves as red beacon without global control. In this situation, these nodes could do a contending process by time or ID, etc. The red beacon will flood its hop counter messages to other nodes in the network. The nodes that can not find next hop sends an ACK to the red beacon, by which the red beacon can compute the max redhop K in the network. 2) Blue Beacon selection: The blue beacon can be selected in the assistance of red beacon. When the red beacon has computed the max redhop K, it will send another message K randomly using one path by gradient routing. When the message reaches a node with $r e d h o p { = } K$ , the message stops. This node is selected as Blue Beacon. The Blue Beacon also floods its hop counter messages to other nodes in the network. At the same time, the message piggybacks the K to other nodes.

During the Red Beacon selection and Blue Beacon selection, double-beacon contour overlays are also built. Each node also has a hop number pair (b , r) as in ideal Contourcast scenario.

# B. Tangent contours strategy (T C)

In random scenario we use tangent contours (T C) replication strategy, which is similar to RiB and BiR in ideal scenario. In this strategy, the producer compares its bluehop and redhop first. If its bluehop is less than redhop, the producer uses BiR strategy. If its redhop is less that bluehop, the producer uses RiB strategy. It is obvious that if we use the same strategy T C for data retrieval (called basic data retrieval strategy), the success ratio can not be guaranteed. By simulation, we find that the success ratio of basic data retrieval strategy is influenced by the positions of the double beacons and the hop distance of them, too. So we present the worst case of T C.

# C. The worst case of T C

In the Blue Beacon selection, we select one node with $r e d h o p = K$ . Because the Red Beacon is randomly selected, the value of K is not a fixed value. But it is easy to prove that in any network, the $K \in [ K _ { d } / 2 , \ K _ { d } ] .$ , where $K _ { d }$ is the radius of the network.In theory, if the network as large as possible, all the contours with radius less than the hop distance $H _ { d }$ between two beacons will form a circle. In spindly area in Figure 5.a, if a red contour and a blue contour are tangent (which means that the common nodes of them with $b l u e h o p + r e d h o p { = } H _ { d } ) .$ , they are called a BR-contour pair. In Figure 5, any two BR-contour pairs intersect with each other in the spindly area. If all the nodes locate at in the spindly area, any pair of tangent red contour and blue contour also guarantees the intersection requirement with at least two nodes. In ideal scenario, the square area covers half of this spindly area. Then we hope more nodes can locate at the area among the two beacons and covered by the spindly area as in Figure 5.a.

Definition 2 (Double-beacon span area). : Two lines pass two beacons separately, which are vertical to the line R B that connecting the two beacons. If the double beacons are in inner area of the network, the two lines separate the whole network area into three parts. All the nodes between these two lines are separated by the line R B into two areas. The greater area is defined as Double-beacon span area, denoted as SA. The other area is called shadow double-beacon span area.(see Figure 6.)

Definition 3 (double-beacon span half spindly area). : The spindly area between two beacons is separated into two equal halves. Both of them are called double-beacon span half spindly area.(see Figure 7.)

Lemma 1. Assume the hop distance between the two beacons is d, where d is less than the radius of the network (which is the hop distance of two nodes nearest to the diagonal corner of the square). When the two beacons locate at one diagonal line of the network area and one of them locate nearest to the corner, the double-beacon span area achieve the minimum value.

Proof: As in Figure 6 illustrated, for any segment $| A B | , { \mathrm { i f ~ } } | A B | = | C D |$ , it is easy to prove that $| E E ^ { \prime } | +$

![](images/4d9fcb555778625d31b00c4bac4e809717df174cbca2e0dd2f6ac05eef54a808.jpg)



![](images/dfc918a8b9191b999c1b21ac061b9ad484c8e51c34fbbd20176d9b99dd0017cb.jpg)



Figure 6. Double-beacon span area of AB and CD.   
Figure 7. Double-beacon span half spindly area of RB.

$$
\begin{array}{l} | F F ^ {\prime} | \geq | G G ^ {\prime} |. S _ {E E ^ {\prime} F F ^ {\prime}} \geq S _ {G G ^ {\prime} D}. S A _ {C D} = S _ {G G ^ {\prime} D} / 2 \leq \\ S _ {E E ^ {\prime} F F ^ {\prime}} / 2 \leq S A _ {A B}. \end{array}
$$

We assume that if adequate nodes locate in the half spindly area, any two tangent contours pairs intersect each other. Every node in the half spindly area can be considered as an intersecting point of two tangent contours pairs. There are two problems here. 1) If the beacons are randomly selected, it can not guarantee that all the nodes are covered by the half spindly area. 2) The nodes covered by the half spindly area may not fulfill the half spindly area. We use the following formulation to approximate the intersection ratio

$$
r = \frac {S _ {c}}{S _ {N}} \cdot \frac {S _ {c}}{S _ {o}} \tag {2}
$$

where $S _ { c } { : }$ The area covered by half spindly area. $S _ { N } \mathbf { : }$ : The whole network area is separated by the line crossing the two beacons. The area of the half network on the same side of the double-beacon span area is $S _ { N } , S _ { o } \colon$ The area of the half spindly area. It is obvious that if the span area is large, the Sc is large too. So by Lemma 1, the worst case is the case as the Lemma 1. In this case, the distance of BR is h,then

$$
r (h) = \left\{ \begin{array}{c} \frac {\frac {\pi}{8} h ^ {2}}{\frac {L ^ {2}}{2}} \cdot \frac {\frac {\pi}{8}}{\frac {\pi}{3} - \frac {\sqrt {3}}{4}}, h \in [ 0, L ] \\ \frac {((\frac {\pi}{4} - \arccos (\frac {L}{h})) \cdot h ^ {2} + (L \sqrt {h ^ {2} - L ^ {2}})) ^ {2}}{L ^ {2} \cdot (\frac {\pi}{3} - \frac {\sqrt {3}}{4}) h ^ {2}}, h \in (L, \sqrt {2} L ] \end{array} \right. \tag {3}
$$

If $0 ~ \leq ~ h ~ \leq ~ L ,$ , the maximum value of $r ( h ) ~ \doteq ~ 5 0 \%$ when $h = L .$ . If $L < h \leq \sqrt { 2 } \ L$ , the maximum value of $r ( h ) \doteq 5 2 \%$ when $r ^ { \prime } ( h ) = 0 , h \doteq 1 . 1 L$ . It means that the worst case or lower bound of the intersection ratio achieves maximum when $h \ \doteq \ 1 . 1 L$ . Because the Red Beacons is randomly selected among all nodes in the network, then $K \in [ K _ { d } / 2 , K _ { d } ]$ .

$$
E (K) = 4 L \int_ {1 / 2} ^ {1} \int_ {1 / 2} ^ {1} \sqrt {x ^ {2} + y ^ {2}} d x d y \doteq 1. 0 7 L \tag {4}
$$

$r ( E ( K ) ) \doteq 5 1 \%$ , it is the expected worst case. Here we only consider the worst case of the intersection ratio of BRcontour pairs. In reality, the intersection ratio can achieve more than 80%. We assume that all the nodes not covered by the double-beacon span half spindly area can not discover any information. For example, even when the two beacons on the same side of the square, which is the ideal scenario, the intersection ratio value is about 60%. The result is much conservative. In reality, if one node is out of double-beacon span half spindly area, it maybe detour to the double-beacon span half spindly area by connected contours. Even if the contour is separated into two segments, the node can also detour to the double-beacon span half spindly area by using nodes on the boundary. Then we propose a new data retrieval approach using boundary nodes.

# D. Data retrieval

In random scenario, it is obvious that if we use the same strategy as data replication process for data retrieval, the retrieve success can not be guaranteed as Figure 5.a illustrated. So besides the basic data retrieval strategy we propose boundary-assistant retrieval. We also present boundary aggregation retrieval for certain applications. Each of them has different properties.

1) Boundary-assistant retrieval: If one consumer node with hop numbers (b , r) and $r < b$ and $r ^ { 2 } + K ^ { 2 } < b ^ { 2 }$ , it means the node does not locates at the spindly area. Then the query travels along the red contour first. When it meets the boundaries, it uses the following conditions to select the next hop: $M a x \{ S _ { n } . r e d h o p | S _ { n } . r e d h o p \ < \ Q . r e d h o p \}$ or $M a x \{ S _ { n } . b l u e h o p | S _ { n } . b l u e h o p \ < \ Q . b l u e h o p \}$ . When it meets again a node with equal redhop to producer’s redhop, it does red Contour-cast again. In the second red Contourcast it finds the minimal bluehop node to trigger blue cast.

2) Boundary aggregation retrieval: The replication contour stops when it can not find another neighbor with the same redhop or bluehop. In a dense network, the termination nodes almost locate at the boundary of the network. So if the query cast around the boundary, it will aggregate all the data. In some applications, it is useful for people and mobile node to travel along the boundary for the inner area where is very hostile. We just assume one user beside one node on the boundary, now he or she can send a query to this node, then this node will cast this query along the boundary and return data also along the boundary. In this scenario, the node selects node with $M a x \{ s u m | s u m = S _ { n } . b l u e h o p + S _ { n } . r e d h o p \}$ .

# V. EVALUATION

In this section, we present the evaluation results of Contour-cast. Because the ideal contour scenario can guarantee data retrieval determinately in theory, we only simulate random Contour-cast scenario. One key concerned performance is the data retrieval success ratio. The other is the storage cost and data retrieval cost. We also show the load balance of Contour-cast. Although the random Contour-cast scenario can be applied in any shape network area, for simplicity, we simulate wireless sensor networks in a square area. The square area is divided into grids. We use perturbed grid topology to deploy sensor nodes. In the perturbed grid topology, each sensor node is deployed in a position departed from original grid, affected by the perturbed parameter s in the range of [1, 10]. We assume that every node does not know its position after the deployment of the network. Contour-cast does not need location information. In order to simulate GHT, we use simple trilateration location algorithm to locate every node’s position with random errors. The radio transmission range of every node is 15m.

# A. Query success ratio

The data retrieval success ratio in random Contour-cast scenario is influenced by the hop distance of two beacons. We deploy 1600 nodes in this test. Firstly 50 data producers and 50 data consumers are randomly generated in the network. Then we randomly select one node as Red Beacon. Then we select one node at each red contour as Blue Beacon. For each pair of Blue beacon and Red Beacon, 50 producers disseminate their data along their Contour-cast path. And consumers retrieve data using basic strategy. The max red hop distance is 39. We find that, when the hop distance of two beacons between 20 and 30 the average success ratio can reach more than 75% as in Figure 8. So we use 25-hop to test boundary-assistant query success ratio comparing with GHT and rumor routing. We consider the location algorithm error in GHT. The location error can influence its success ratio significantly by our simulation. In our simulation, we use Geographic greedy forwarding protocol. But if location information has error for each node, sometimes the message path may be disrupted by some virtual holes. We set the error range for every node is from 1m to 9m. Figure 9 shows that the average data retrieval success ratio of GHT decreases with the error range increasing. The Contour-cast and rumor routing do not depend on position information, so their average data success retrieval ratio has no relation with location error. The average data retrieval success ratio of rumor routing can reach about 67%, while the Contourcast can reach above 80%.

# B. Storage Cost

The other performance concerned is the storage cost of Contour-cast. We compare the Contour-cast with Double Rulings. We deploy different size networks for testing the storage cost performance. For each size, we test 1000 times for randomly. We see that the storage cost of Contour-cast is greater that Double Rulings as in Figure 10. We use Contourcast and Double Rulings scheme to store their replicas. In our simulation, we use local flooding for store data replicas at all the satisfied nodes. The Figure 10 shows the Contourcast needs about 170 nodes to store a producer’s data while Double Rulings need about 140 nodes when the network size is 3000.

# C. Load balance

We use grid network deployment to simulate the load balance of double rulings, Contour-cast and Contour-cast with network coding. The network size is 3600 nodes. In this test we generate 50 data producers randomly in the network, and then we use Double Rulings, Contour-cast and Contourcast with network coding to disseminate their data replicas. Figure 11.a shows the load distribution of Double Rulings. The load of each node in Double Rulings in Figure 11.a is less than 10, while only at the center area, some nodes keeps more data. Figure 11.b shows the load of the Contourcast. The load of each node in Contour-cast is less than 10, too. The average load of all nodes in Contour-cast is more than Double Rulings. But we can use Network Coding to code any pair of original data at one node, the load of each node can reduce to half of the load of Contour-cast without network coding (Figure 11.c).

![](images/c956892080973e37ef4ba726a6301ffa4bf5bc6fe205dba1efd85bc411606c97.jpg)



Figure 8. The average success data retrieval ratio with different hops between the Blue Beacon and Red Beacon.

![](images/b3e4587ff67edfb24312beb01de55d14e4432ade313dd501663352d4eb38e06c.jpg)



Figure 9. The average success data retrieval ratio of DHT, Rumor routing, and Contourcast. $K _ { d } = 3 0 , K = 2 5$ .

![](images/eca326484c419ce1c9013939debb47abfc35ace43d43adbca1b7589958dd4c6c.jpg)



Figure 10. The storage nodes for one producer using Contour-cast and Double Rulings respectively.

![](images/b2f0d822a318cdd3c00d64139ac3382b77be92b317016b5ff41453deacd1284c.jpg)



(a)

![](images/0b7d5a9f3a8ac24d22795031fd8d9623c0654d9a98b8ed48f871dc9f971dac68.jpg)



(b)

![](images/85b7a36a3d6ba007300a4a95e97de4befe055ad76f0aad140e257c5fa9ebb187.jpg)



(c)   
Figure 11. Load comparison on Double Rulings, Contour-cast and Contour-cast with Network Coding.(a)Storage load of Double Rulings.(b)Storage load of Contour-cast without Network Coding. (c)Storage load of Contour-cast with Network Coding.

# VI. CONCLUSION

In this paper we propose Contour-cast, a new location-free data dissemination and discovery approach. One important advantage of Contour-cast is that it does not need assign location information for every node. The location-free nature of Contour-cast makes it suitable for most practical largescale Wireless Sensor Networks. Contour-cast can guarantee data retrieval success ratio with high probability in both ideal and random Contour-cast scenario. Contour-cast can also achieve load balance for data storage. Our future work will focus on Contour-cast in sparse networks.

# ACKNOWLEDGMENT

The research was partially supported by the National Natural Science Foundation of China under Grant No.60573135, the National High Technology Research and Development Program of China (863 Program) under grant No. 2006AA01A106, the National Basic Research Program of China (973 Program) under Grant No.2006CB303004, NSERC Discovery Grant 341823-07 and FQRNT 2010- NC-131844. We would also like to thank the anonymous reviewers for their constructive comments.

# REFERENCES

[1] C. Intanagonwiwat, R. Govindan, and D. Estrin, “Directed Diffusion: A Scalable and Robust Communication Paradigm for Sensor Networks,” In Proceedings of the 6th ACM Annual International Conference on Mobile Computing and Networking (MobiCom), Boston, MA, USA, 2000.   
[2] S. Madden, M. J. Franklin, Wei Hongand J. M. Hellerstein, “TAG: a Tiny AGgregation Service for Ad-Hoc Sensor Networks,” In Proceedings of 5th Sysposium on Operating Systems Design and Implementation (OSDI), Boston, MA, USA, 2002.   
[3] S. Ratnasamy, S. Shenker, B. Karp, R. Govindan, and D. Estrin.,“ Data-centric storage in sensornets,” ACM SIGCOMM Computer Communication Review archive,Vol. 33,pp. 137 - 142, 2002.

[4] Anastasi,G., Conti,M.,Di Francesco,M.“ Data collection in sensor networks with Data Mules: an integrated simulation analysis,”. In Proceedings of the of IEEE ISCC 2008   
[5] H. Luo, F. Ye, J. Cheng, S. Lu, and L. Zhang, “TTDD: Two-Tier Data Dissemination in Large-Scale Wireless Sensor Networks,” Wireless Networks, vol. 11, pp. 161-175, 2005.   
[6] B. Karp, S. Ratnasamy, L. Yin, F. Yu, D. Estrin, R. Govindan, S.Shenker, “GHT: A Geographic Hash Table for DataCentric Storage,” In Proceedings of the First ACM international Workshop on Wireless Sensor Networks and Applications (WSNA), Atlanda, Georgia, USA, 2002   
[7] R. Sarkar, X. Zhu, and J. Gao, “Double Rulings for Information Brokerage in Sensor Networks,” In Proceedings of the 12th ACM Annual International Conference on Mobile Computing and Networking (MobiCom), Los Angeles, CA, USA, 2006.   
[8] X. Liu, Q. Wang, L. Sha, W. He, “Optimal QoS Sampling Frequency Assignment for Real-Time Wireless Sensor Networks,”In Proceedings of the 24th IEEE Real-Time Systems Symposium (RTSS 2003), Cancun, Mexico, 2003.   
[9] W. Shu, X. Liu, Z. Gu, S. Gopalakrishnan, “Optimal Sampling Rate Assignment with Dynamic Route Selection for Real-Time Wireless Sensor Networks, ” In Proceedings of the 29th IEEE Real-Time Systems Symposium (RTSS 2008), Barcelona, Spain, 2008.   
[10] S. Chellappan, X. Bai, B. Ma, D. Xuan and C. Xu, “Mobility Limited Flip-based Sensor Network Deployment”, in IEEE Transactions on Parallel and Distributed Systems , Vol. 18, No. 2, Oct. 2006, pp. 199-211   
[11] D. Braginsky and D. Estrin, “Rumor Routing Algorithm for Sensor Networks,” In Proceedings of the 8th ACM Annual International Conference on Mobile Computing and Networking (MobiCom), Atlanda, Georgia, USA, 2002.   
[12] X.B. Wu, G. Chen and Sajal K. Das, “Avoiding Energy Holes in Wireless Sensor Networks with Nonuniform Node Distribution”, IEEE Transactions on Parallel and Distributed Systems, Vol. 19, No. 5, pp. 710-720, May , 2008,   
[13] W-Z Song, X-Y Li ,O. Frieder and W. Wang “Local Construction of Energy-Efficient and Low-Weighted Topology for Wireless Ad Hoc Networks” IEEE Transaction on Parallel and Distributed Systems, Volume 17, Number 4, page 321-334, April, 2006.   
[14] S. Chessa, A. Caruso, S. De, and A. Urpi, “GPS free coordinate assignment and routing in wireless sensor networks,” In Proceedings of the 24th IEEE Conference on Computer Communications (INFOCOM), Miami, FL, USA, 2005.